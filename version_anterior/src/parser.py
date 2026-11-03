"""
MiniHTML Parser - Proyecto Integrador 2026
Materia: Lenguajes Formales y Autómatas - UCC
Basado en los contenidos teóricos de la Clase 7 (GIC) y Clase 8 (Autómatas a Pila).

Este módulo implementa el Analizador Sintáctico de MiniHTML mediante dos estrategias:
1. Autómata Finito con Pila No Determinista con transiciones λ (AFPN-λ) según la
   definición de la Clase 8: M = (Σ, Γ, Q, q0, Z0, F, Δ)
2. Analizador Descendente Recursivo directo de la Gramática Libre de Contexto (G).
"""

import re
import sys
from typing import Dict, List, Optional, Set, Tuple

# Configuración de salida segura UTF-8 en consola
_reconfigurar = getattr(sys.stdout, "reconfigure", None)
if callable(_reconfigurar) and (sys.stdout.encoding or "").lower() != "utf-8":
    try:
        _reconfigurar(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 0. DEFINICIÓN DE LAS ETIQUETAS DEL LENGUAJE
# ==============================================================================

# Etiqueta -> símbolo de pila (Γ). Es la única fuente de verdad del lenguaje:
# el autómata M y la gramática G construyen sus alfabetos a partir de este diccionario.
# Para incorporar una etiqueta nueva (ej: <u>) basta con agregar "u": "U".
ETIQUETAS: Dict[str, str] = {
    "b": "B",
    "i": "I",
    "p": "P",
}


# ==============================================================================
# 1. TOKENIZADOR / ANALIZADOR LÉXICO
# ==============================================================================

# Separa todo lo que empieza con "<" (hasta el ">" o el próximo "<") del texto plano
PATRON_TOKEN = re.compile(r'<[^<>]*>?|[^<]+')
# Etiqueta bien formada: <x> o </x> (se admite <\x> como notación alternativa de cierre)
PATRON_ETIQUETA = re.compile(r'<([/\\]?)([a-zA-Z0-9]+)>')


def tokenizar(cadena: str) -> List[str]:
    """
    Divide la cadena de entrada en una lista de tokens reconocibles:
    Etiquetas: <b>, <i>, <p>, </b>, </i>, </p>
    Texto: fragmentos de texto plano (representados por el token TEXTO)
    Cualquier etiqueta mal formada (ej: "<b", "< b >", "<p class=x>") se conserva
    tal cual, para que el analizador la rechace como error léxico.
    """
    tokens: List[str] = []

    for coincidencia in PATRON_TOKEN.finditer(cadena):
        trozo = coincidencia.group().strip()
        if not trozo:
            continue

        if trozo.startswith("<"):
            etiqueta = PATRON_ETIQUETA.fullmatch(trozo)
            if etiqueta:
                barra = "/" if etiqueta.group(1) else ""
                tokens.append(f"<{barra}{etiqueta.group(2).lower()}>")
            else:
                tokens.append(trozo)
        else:
            # Cada palabra de texto (ya sea la palabra genérica "TEXTO" o texto real
            # como "Hola mundo") se normaliza como un token TEXTO
            tokens.extend("TEXTO" for _ in trozo.split())

    return tokens


# ==============================================================================
# 2. AUTÓMATA A PILA NO DETERMINISTA CON TRANSICIONES λ (AFPN-λ) - CLASE 8
# ==============================================================================

class AutomataPilaMiniHTML:
    """
    Implementación del Autómata Finito con Pila No Determinista con transiciones λ
    (AFPN-λ), definido formalmente como la 7-upla (Clase 8, diapositivas 7-10):
      M = (Σ, Γ, Q, q0, Z0, F, Δ)

    Donde:
      Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
      Γ = { Z0, B, I, P }
      Q = { q0, qf }
      q0: Estado inicial
      Z0: Marcador de fondo de pila
      F = { qf }: Estado de aceptación final
      Δ: Q × (Σ ∪ {λ}) × Γ -> P(Q × Γ*)

    El único punto de no determinismo es la transición espontánea Δ(q0, λ, Z0) = {(qf, Z0)},
    que coexiste con las transiciones de lectura desde q0 con tope Z0.
    """

    def __init__(self):
        # Alfabetos y estados según Clase 8
        self.gamma: Set[str] = {"Z0"}
        self.sigma: Set[str] = {"TEXTO"}
        self.estados: Set[str] = {"q0", "qf"}
        self.q0 = "q0"
        self.z0 = "Z0"
        self.f: Set[str] = {"qf"}

        # Mapeo de etiquetas a símbolos de la pila (construido desde ETIQUETAS)
        self.apertura_a_pila: Dict[str, str] = {}
        self.cierre_a_pila: Dict[str, str] = {}
        for etiqueta, simbolo in ETIQUETAS.items():
            self.agregar_etiqueta(etiqueta, simbolo)

    def agregar_etiqueta(self, etiqueta: str, simbolo_pila: Optional[str] = None):
        """
        Incorpora una etiqueta al lenguaje: agrega <tag> y </tag> a Σ, su símbolo a Γ
        y las transiciones de PUSH/POP correspondientes a Δ.
        Ejemplo: automata.agregar_etiqueta("u", "U") para <u> y </u>
        """
        tag = etiqueta.lower().strip("<>/ ")
        simbolo = simbolo_pila if simbolo_pila else tag.upper()
        self.apertura_a_pila[f"<{tag}>"] = simbolo
        self.cierre_a_pila[f"</{tag}>"] = simbolo
        self.sigma.add(f"<{tag}>")
        self.sigma.add(f"</{tag}>")
        self.gamma.add(simbolo)

    def simular(self, tokens: List[str], imprimir_traza: bool = True) -> Tuple[bool, str, List[str]]:
        """
        Procesa la secuencia de tokens aplicando la función de transición Δ.
        Registra cada paso como una configuración instantánea (q, ω, γ) (Clase 8, pág. 11).
        Devuelve: (es_valida, mensaje_diagnostico, traza_pasos)
        """
        estado = self.q0
        pila = [self.z0]  # El último elemento representa el tope de la pila
        traza: List[str] = []

        def configuracion(idx: int) -> str:
            # (q, ω, γ): estado actual, entrada aún no leída y pila con el tope a la izquierda
            remanente = " ".join(tokens[idx:]) if idx < len(tokens) else "λ"
            return f"({estado}, {remanente}, {' '.join(reversed(pila))})"

        def registrar(prefijo: str, idx: int, detalle: str):
            traza.append(f"{prefijo:<3}{configuracion(idx):<60}  {detalle}")

        def finalizar(valida: bool, mensaje: str) -> Tuple[bool, str, List[str]]:
            if imprimir_traza:
                self._imprimir_traza_consola(traza)
            return valida, mensaje, traza

        registrar("", 0, "Configuración inicial")

        for idx, token in enumerate(tokens):
            tope = pila[-1]

            # 1. Lectura de TEXTO: Δ(q0, TEXTO, X) = {(q0, X)} (No altera la pila)
            if token == "TEXTO":
                registrar("|-", idx + 1, f"Δ({estado}, TEXTO, {tope}) = {{({estado}, {tope})}}")

            # 2. Apertura: Δ(q0, <tag>, X) = {(q0, Y X)} (PUSH)
            elif token in self.apertura_a_pila:
                marcador = self.apertura_a_pila[token]
                pila.append(marcador)
                registrar("|-", idx + 1, f"Δ({estado}, {token}, {tope}) = {{({estado}, {marcador} {tope})}}  PUSH")

            # 3. Cierre: Δ(q0, </tag>, Y) = {(q0, λ)} (POP)
            elif token in self.cierre_a_pila:
                esperado = self.cierre_a_pila[token]
                if tope == esperado:
                    pila.pop()
                    registrar("|-", idx + 1, f"Δ({estado}, {token}, {tope}) = {{({estado}, λ)}}  POP")
                else:
                    if tope == self.z0:
                        msg = f"Error sintáctico: Se intentó cerrar '{token}' sin apertura previa (pila vacía)."
                    else:
                        msg = (f"Error de anidamiento LIFO: Se leyó '{token}' pero en el tope está '{tope}' "
                               f"(se esperaba cerrar '{self._etiqueta_de(tope)}' primero).")
                    traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
                    return finalizar(False, msg)

            # 4. Token no reconocido (fuera del alfabeto Σ)
            else:
                msg = f"Error léxico: El token '{token}' no pertenece al alfabeto Σ del lenguaje."
                traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
                return finalizar(False, msg)

        # Transición espontánea Δ(q0, λ, Z0) = {(qf, Z0)}. Aunque está disponible cada vez
        # que la pila vuelve a Z0, la única rama que puede aceptar es la que la toma con la
        # entrada ya consumida (desde qf no hay transiciones), así que el simulador sigue esa rama.
        if pila == [self.z0]:
            estado = "qf"
            registrar("|-", len(tokens), f"Δ(q0, λ, {self.z0}) = {{(qf, {self.z0})}}  Aceptación")
            return finalizar(True, "Cadena VÁLIDA: procesada exitosamente por el autómata (w ∈ L(M)).")

        pendientes = ", ".join(self._etiqueta_de(simbolo) for simbolo in reversed(pila[1:]))
        msg = f"Error sintáctico: Fin de la entrada con etiquetas sin cerrar (del tope al fondo): {pendientes}."
        traza.append(f"BLOQUEO: Δ({estado}, λ, {pila[-1]}) = ∅. {msg}")
        return finalizar(False, msg)

    def _etiqueta_de(self, simbolo: str) -> str:
        """Devuelve la etiqueta de apertura asociada a un símbolo de pila (ej: 'B' -> '<b>')."""
        for etiqueta, marcador in self.apertura_a_pila.items():
            if marcador == simbolo:
                return etiqueta
        return simbolo

    def _imprimir_traza_consola(self, traza: List[str]):
        """Imprime la traza de pasos en formato tabular claro."""
        print("\n" + "=" * 110)
        print("TRAZA DE CONFIGURACIONES INSTANTÁNEAS (AFPN-λ M - Clase 8)")
        print("=" * 110)
        for paso in traza:
            print(f"  {paso}")
        print("=" * 110)


# ==============================================================================
# 3. ANALIZADOR DESCENDENTE RECURSIVO (GIC - MODELO CLASE 7)
# ==============================================================================

class AnalizadorRecursivoMiniHTML:
    """
    Implementación alternativa basada en la Gramática Libre de Contexto (Clase 7):
      S -> E S | λ
      E -> TEXTO | <b> S </b> | <i> S </i> | <p> S </p>
    """

    def __init__(self, etiquetas_permitidas: Optional[Set[str]] = None):
        self.tags: Set[str] = set(etiquetas_permitidas) if etiquetas_permitidas else set(ETIQUETAS)

    def validar(self, tokens: List[str]) -> Tuple[bool, str]:
        """Verifica recursivamente si la secuencia de tokens pertenece a L(G)."""
        pos = 0

        def es_cierre(tok: str) -> bool:
            return tok.startswith("</") and tok[2:-1] in self.tags

        def parse_S() -> None:
            nonlocal pos
            # S -> E S se aplica mientras haya texto o apertura (la recursión por la
            # derecha se resuelve como iteración); ante un cierre o fin de tokens, S -> λ
            while pos < len(tokens) and not es_cierre(tokens[pos]):
                parse_E()

        def parse_E() -> None:
            nonlocal pos
            tok = tokens[pos]

            if tok == "TEXTO":
                pos += 1  # E -> TEXTO
                return

            nombre_tag = tok[1:-1]
            if not (tok.startswith("<") and tok.endswith(">") and nombre_tag in self.tags):
                raise ValueError(f"Error léxico: el token '{tok}' no es un terminal de la gramática.")
            pos += 1  # Consumir apertura

            # Procesar contenido interno S
            parse_S()

            # Verificar y consumir cierre correspondiente
            esperado = f"</{nombre_tag}>"
            if pos >= len(tokens):
                raise ValueError(f"La etiqueta <{nombre_tag}> nunca fue cerrada (fin de la entrada).")
            if tokens[pos] != esperado:
                raise ValueError(f"Error de anidamiento: se esperaba '{esperado}', pero se encontró '{tokens[pos]}'.")
            pos += 1  # Consumir cierre

        try:
            parse_S()
            if pos < len(tokens):
                raise ValueError(f"Etiqueta de cierre '{tokens[pos]}' sin apertura previa.")
            return True, "Cadena VÁLIDA: generada por la gramática (w ∈ L(G))."
        except ValueError as err:
            return False, f"Error sintáctico en G: {err}"
        except RecursionError:
            return False, "Error en G: anidamiento demasiado profundo para el analizador recursivo."


# ==============================================================================
# 4. FUNCIÓN PRINCIPAL DE ENTRADA Y PRUEBAS
# ==============================================================================

def analizar_cadena(cadena: str, mostrar_traza: bool = True) -> bool:
    """Función de alto nivel para analizar cualquier cadena con el autómata y la gramática."""
    tokens = tokenizar(cadena)
    print(f"\nCadena analizada: \"{cadena}\"")
    print(f"Tokens detectados: {tokens if tokens else ['λ (vacía)']}")

    automata = AutomataPilaMiniHTML()
    valida_ap, mensaje_ap, _ = automata.simular(tokens, imprimir_traza=mostrar_traza)

    recursivo = AnalizadorRecursivoMiniHTML()
    valida_g, mensaje_g = recursivo.validar(tokens)

    print(f"\n[Resultado Autómata a Pila M]: {'ACEPTADA (w ∈ L(M))' if valida_ap else 'RECHAZADA (w ∉ L(M))'}")
    print(f"  Diagnóstico: {mensaje_ap}")
    print(f"[Resultado Gramática G]:      {'ACEPTADA (w ∈ L(G))' if valida_g else 'RECHAZADA (w ∉ L(G))'}")
    print(f"  Diagnóstico: {mensaje_g}")
    print(f"[Equivalencia L(G) = L(M)]:   {'VERIFICADA (Ambos coinciden)' if valida_ap == valida_g else 'DISCREPANCIA'}")

    return valida_ap


def ejecutar_casos_oficiales():
    """Ejecuta las cadenas de prueba requeridas por la consigna de la cátedra."""
    print("=" * 90)
    print("PROYECTO INTEGRADOR: PRUEBAS OFICIALES DE LA CÁTEDRA (FASES 1, 2 Y 3)")
    print("=" * 90)

    casos = [
        ("Cadena alfa (α)", "<p> TEXTO <b> TEXTO </b> </p>"),
        ("Cadena beta (β)", "<p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>"),
        ("Cadena gamma (γ)", "<p> TEXTO TEXTO </p> <i> TEXTO </i>"),
        ("Cadena vacía (λ)", ""),
        ("Cadena Inválida 1 (Anidamiento cruzado)", "<p> <b> TEXTO </p> </b>"),
        ("Cadena Inválida 2 (Etiqueta huérfana)", "<p> TEXTO </p> </b>"),
        ("Cadena Inválida 3 (Sin cerrar al final)", "<p> <b> TEXTO </b>"),
        ("Cadena Inválida 4 (Etiqueta mal formada)", "<p> TEXTO <b </p>")
    ]

    for nombre, texto in casos:
        print(f"\n>>> Probando: {nombre}")
        analizar_cadena(texto, mostrar_traza=False)
        print("-" * 90)


def modo_interactivo():
    """Modo interactivo en consola para ingresar cadenas en vivo durante la defensa oral."""
    print("\n" + "=" * 90)
    print("MODO INTERACTIVO: Analizador Sintáctico de MiniHTML")
    print("Ingrese cadenas para validarlas en tiempo real con el autómata a pila.")
    print("Escriba 'salir' para terminar o 'test' para correr los casos de prueba.")
    print("=" * 90)

    while True:
        try:
            entrada = input("\nIngrese cadena MiniHTML > ").strip()
            if not entrada:
                continue
            if entrada.lower() in ("salir", "exit", "quit"):
                print("Fin de la sesión interactiva.")
                break
            if entrada.lower() == "test":
                ejecutar_casos_oficiales()
                continue

            analizar_cadena(entrada, mostrar_traza=True)

        except (KeyboardInterrupt, EOFError):
            print("\nFin de la sesión.")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        param = sys.argv[1]
        if param == "--test":
            ejecutar_casos_oficiales()
        else:
            analizar_cadena(param, mostrar_traza=True)
    else:
        # Por defecto muestra las pruebas oficiales y abre el modo interactivo
        ejecutar_casos_oficiales()
        modo_interactivo()
