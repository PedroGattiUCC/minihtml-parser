"""
MiniHTML Parser - Proyecto Integrador 2026
Materia: Lenguajes Formales y Autómatas - UCC
Basado en los contenidos teóricos de la Clase 7 (GIC) y Clase 8 (Autómatas a Pila).

Este módulo implementa el Analizador Sintáctico de MiniHTML mediante dos estrategias:
1. Autómata Finito con Pila Determinístico (AFPD) según la definición de la Clase 8:
   M = (Σ, Γ, Q, q0, Z0, F, δ)
2. Analizador Descendente Recursivo directo de la Gramática Libre de Contexto (G).
"""

import sys
import re
from typing import List, Tuple, Optional

# Configuración de salida segura UTF-8 en consola
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. TOKENIZADOR / ANALIZADOR LÉXICO
# ==============================================================================

def tokenizar(cadena: str) -> List[str]:
    """
    Divide la cadena de entrada en una lista de tokens reconocibles:
    Etiquetas: <b>, <i>, <p>, </b>, </i>, </p>
    Texto: fragmentos de texto plano (representados por el token TEXTO)
    """
    # Expresión regular que separa etiquetas <...> del resto del texto
    patron = re.compile(r'(</?[a-zA-Z0-9]+>|[^<]+)')
    tokens = []

    for coincidencia in patron.finditer(cadena):
        trozo = coincidencia.group().strip()
        if not trozo:
            continue

        if trozo.startswith("<") and trozo.endswith(">"):
            tokens.append(trozo.lower())
        else:
            # Si el texto es la palabra genérica "TEXTO", la guardamos tal cual
            # Si es texto real (ej: "Hola mundo"), se normaliza como "TEXTO"
            # permitiendo reconocer tanto la teoría como código HTML real
            palabras = trozo.split()
            for _ in palabras:
                tokens.append("TEXTO")

    return tokens


# ==============================================================================
# 2. AUTÓMATA A PILA DETERMINISTA (AFPD) - MODELO CLASE 8
# ==============================================================================

class AutomataPilaMiniHTML:
    """
    Implementación del Autómata Finito con Pila Determinístico (AFPD)
    Definido formalmente como la 7-upla (Clase 8, diapositiva 3):
      M = (Σ, Γ, Q, q0, Z0, F, δ)
    
    Donde:
      Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
      Γ = { Z0, B, I, P }
      Q = { q0, qf }
      q0: Estado inicial
      Z0: Marcador de fondo de pila
      F = { qf }: Estado de aceptación final
      δ: Función de transición
    """

    def __init__(self):
        # Alfabetos y estados según Clase 8
        self.sigma = {"<b>", "<i>", "<p>", "</b>", "</i>", "</p>", "TEXTO"}
        self.gamma = {"Z0", "B", "I", "P"}
        self.estados = {"q0", "qf"}
        self.q0 = "q0"
        self.z0 = "Z0"
        self.f = {"qf"}

        # Mapeo de etiquetas a símbolos de la pila (Fácilmente extensible)
        self.apertura_a_pila = {
            "<b>": "B",
            "<i>": "I",
            "<p>": "P"
        }
        self.cierre_a_pila = {
            "</b>": "B",
            "</i>": "I",
            "</p>": "P"
        }

    def agregar_etiqueta(self, etiqueta: str, simbolo_pila: str = None):
        """
        Permite incorporar una nueva etiqueta al lenguaje en tiempo de ejecución
        (útil ante pedidos del docente durante la defensa oral).
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
        Procesa la secuencia de tokens aplicando la función de transición δ.
        Registra cada paso como una configuración instantánea (q, ω, γ) (Clase 8, pág. 11).
        Devuelve: (es_valida, mensaje_diagnostico, traza_pasos)
        """
        estado = self.q0
        pila = [self.z0]  # El último elemento representa el tope de la pila
        traza = []

        def obtener_traza_paso(idx: int, accion: str) -> str:
            remanente = " ".join(tokens[idx:]) if idx < len(tokens) else "λ"
            # En la notación formal (Clase 8), el tope se escribe a la izquierda:
            pila_str = " ".join(reversed(pila))
            return f"({estado}, {remanente:<40}, {pila_str:>10})  |-  {accion}"

        traza.append(f"Configuración inicial: ({estado}, {' '.join(tokens) if tokens else 'λ'}, {pila[0]})")

        for idx, token in enumerate(tokens):
            tope = pila[-1]

            # 1. Lectura de TEXTO: δ(q0, TEXTO, X) = (q0, X) (No altera la pila)
            if token == "TEXTO":
                traza.append(obtener_traza_paso(idx, f"Lee TEXTO, conserva tope '{tope}'"))

            # 2. Apertura: δ(q0, <tag>, X) = (q0, Y X) (PUSH)
            elif token in self.apertura_a_pila:
                marcador = self.apertura_a_pila[token]
                pila.append(marcador)
                traza.append(obtener_traza_paso(idx, f"Lee {token}, PUSH '{marcador}'"))

            # 3. Cierre: δ(q0, </tag>, Y) = (q0, λ) (POP)
            elif token in self.cierre_a_pila:
                esperado = self.cierre_a_pila[token]
                if tope == esperado:
                    pila.pop()
                    traza.append(obtener_traza_paso(idx, f"Lee {token}, POP '{esperado}' (cierre correcto)"))
                else:
                    if tope == self.z0:
                        msg = f"Error sintáctico: Se intentó cerrar '{token}' sin apertura previa (pila vacía)."
                    else:
                        msg = (f"Error de anidamiento LIFO: Se leyó '{token}' pero en el tope está '{tope}' "
                               f"(etiqueta no cerrada a tiempo).")
                    traza.append(obtener_traza_paso(idx, f"BLOQUEO: δ({estado}, {token}, {tope}) INDEFINIDA. {msg}"))
                    if imprimir_traza:
                        self._imprimir_traza_consola(traza)
                    return False, msg, traza

            # 4. Token no reconocido (fuera del alfabeto Σ)
            else:
                msg = f"Error léxico: El token '{token}' no pertenece al alfabeto Σ del lenguaje."
                traza.append(obtener_traza_paso(idx, f"BLOQUEO: Token inválido. {msg}"))
                if imprimir_traza:
                    self._imprimir_traza_consola(traza)
                return False, msg, traza

        # Fin de la entrada: transición λ al estado final qf si la pila volvió a Z0
        if pila == [self.z0]:
            estado = "qf"
            traza.append(obtener_traza_paso(len(tokens), "Fin de entrada con pila en Z0 -> Transición λ a estado final qf"))
            if imprimir_traza:
                self._imprimir_traza_consola(traza)
            return True, "Cadena VÁLIDA: procesada exitosamente por el autómata (w ∈ L(M)).", traza
        else:
            pendientes = list(reversed(pila[:-1]))
            msg = f"Error sintáctico: Fin de archivo alcanzado con etiquetas sin cerrar en la pila: {pendientes}."
            traza.append(obtener_traza_paso(len(tokens), f"BLOQUEO: Pila con marcadores pendientes. {msg}"))
            if imprimir_traza:
                self._imprimir_traza_consola(traza)
            return False, msg, traza

    def _imprimir_traza_consola(self, traza: List[str]):
        """Imprime la traza de pasos en formato tabular claro."""
        print("\n" + "=" * 90)
        print("TRAZA DE CONFIGURACIONES INSTANTÁNEAS (AFPD M - Clase 8)")
        print("=" * 90)
        for paso in traza:
            print(f"  {paso}")
        print("=" * 90)


# ==============================================================================
# 3. ANALIZADOR DESCENDENTE RECURSIVO (GIC - MODELO CLASE 7)
# ==============================================================================

class AnalizadorRecursivoMiniHTML:
    """
    Implementación alternativa basada en la Gramática Libre de Contexto (Clase 7):
      S -> E S | λ
      E -> TEXTO | <b> S </b> | <i> S </i> | <p> S </p>
    """

    def __init__(self, etiquetas_permitidas=None):
        self.tags = etiquetas_permitidas if etiquetas_permitidas else {"b", "i", "p"}

    def validar(self, tokens: List[str]) -> Tuple[bool, str]:
        """Verifica recursivamente si la secuencia de tokens pertenece a L(G)."""
        pos = 0

        def parse_S() -> None:
            nonlocal pos
            while pos < len(tokens):
                tok = tokens[pos]
                # Si encontramos un cierre o fin de tokens, aplicamos S -> λ
                if tok.startswith("</"):
                    break
                # Si es apertura o texto, aplicamos S -> E S
                parse_E()

        def parse_E() -> None:
            nonlocal pos
            if pos >= len(tokens):
                raise ValueError("Fin inesperado de la entrada.")

            tok = tokens[pos]

            if tok == "TEXTO":
                pos += 1  # E -> TEXTO
            elif tok.startswith("<") and not tok.startswith("</"):
                nombre_tag = tok.strip("<>/")
                if nombre_tag not in self.tags:
                    raise ValueError(f"Etiqueta <{nombre_tag}> no permitida en la gramática.")
                pos += 1  # Consumir apertura

                # Procesar contenido interno S
                parse_S()

                # Verificar y consumir cierre correspondiente
                if pos >= len(tokens):
                    raise ValueError(f"La etiqueta <{nombre_tag}> nunca fue cerrada (fin de archivo).")

                cierre_tok = tokens[pos]
                esperado = f"</{nombre_tag}>"
                if cierre_tok != esperado:
                    raise ValueError(f"Error de anidamiento: se esperaba '{esperado}', pero se encontró '{cierre_tok}'.")

                pos += 1  # Consumir cierre
            else:
                raise ValueError(f"Token inesperado '{tok}'.")

        try:
            parse_S()
            if pos < len(tokens):
                raise ValueError(f"Etiqueta de cierre '{tokens[pos]}' sin apertura previa.")
            return True, "Cadena VÁLIDA: generada por la gramática (w ∈ L(G))."
        except ValueError as err:
            return False, f"Error sintáctico en G: {err}"


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
        ("Cadena Inválida 3 (Sin cerrar al final)", "<p> <b> TEXTO </p>")
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
