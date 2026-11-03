"""MiniHTML: simulador del autómata a pila M (opción B).
Proyecto Integrador 2026 - Lenguajes Formales y Autómatas - UCC
"""

# Cómo funciona el programa, de punta a punta:
#   1. tokenizar()       pasa el texto a una lista de símbolos de Σ.
#   2. simular()         recorre esa lista aplicando las reglas de δ sobre una pila.
#   3. analizar_cadena() une los dos pasos y muestra el resultado.
#
# Las reglas de M, con la misma numeración que el informe (X es cualquier símbolo de Γ):
#   1  δ(q0, TEXTO, X) = (q0, X)
#   2  δ(q0, <b>, X)   = (q0, BX)       5  δ(q0, </b>, B) = (q0, λ)
#   3  δ(q0, <i>, X)   = (q0, IX)       6  δ(q0, </i>, I) = (q0, λ)
#   4  δ(q0, <p>, X)   = (q0, PX)       7  δ(q0, </p>, P) = (q0, λ)
#   8  δ(q0, λ, Z0)    = (qf, Z0)
#   Cualquier otro caso: δ = ∅, y la cadena se rechaza.

import re   # expresiones regulares, para separar el texto en trozos
import sys  # argumentos de la consola y configuración de la salida

# Para que δ y λ se vean bien también en la consola de Windows.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# --- Datos de M -------------------------------------------------------------

# Etiqueta -> símbolo de pila. Para agregar una etiqueta alcanza con sumarla acá.
ETIQUETAS = {"b": "B", "i": "I", "p": "P"}

# Se arman a partir de ETIQUETAS, así los dos diccionarios nunca quedan desparejos:
#   APERTURAS = {"<b>": "B", "<i>": "I", "<p>": "P"}      qué símbolo apilar al abrir
#   CIERRES   = {"</b>": "B", "</i>": "I", "</p>": "P"}   qué símbolo debe estar en el tope al cerrar
APERTURAS = {f"<{e}>": s for e, s in ETIQUETAS.items()}
CIERRES = {f"</{e}>": s for e, s in ETIQUETAS.items()}


# --- Paso 1: del texto a los símbolos de Σ ----------------------------------

def tokenizar(cadena):
    """Convierte el texto en tokens de Σ. Lo mal escrito queda igual para rechazarlo después."""
    tokens = []
    # La expresión regular corta el texto en dos tipos de trozo e ignora los espacios:
    #   <[^<>]*>?   desde un "<" hasta el ">". El ">" es opcional, así "<b" también se
    #               captura como un trozo y después se informa como error léxico.
    #   [^<\s]+     una palabra: caracteres seguidos que no son "<" ni espacios.
    for trozo in re.findall(r"<[^<>]*>?|[^<\s]+", cadena):
        if trozo.startswith("<"):
            # Es una etiqueta. Se normaliza para aceptar <P> y <\p> como <p> y </p>.
            # No se valida acá: si no está en Σ, la rechaza simular().
            tokens.append(trozo.strip().lower().replace("\\", "/"))
        else:
            # Cada palabra es un símbolo TEXTO: "Hola mundo" son dos.
            tokens.append("TEXTO")
    return tokens


# --- Paso 2: la simulación de M ---------------------------------------------

def configuracion(estado, resto, pila):
    """Arma el texto (q, ω, γ), con el tope de la pila a la izquierda."""
    # Si no queda entrada se muestra λ. La pila se invierte porque en la lista
    # el tope está al final, y en la traza se escribe a la izquierda.
    return f"({estado}, {' '.join(resto) or 'λ'}, {' '.join(reversed(pila))})"


def simular(tokens):
    """Aplica δ token por token. Devuelve (es_valida, mensaje, traza)."""
    # Configuración inicial: estado q0, toda la entrada por leer y Z0 en la pila.
    pila = ["Z0"]  # el tope es el último elemento
    traza = [configuracion("q0", tokens, pila)]

    # Cada vuelta lee un símbolo y aplica una regla. No hace falta una variable para
    # el estado: mientras dura el recorrido, M siempre está en q0.
    for i, token in enumerate(tokens):
        tope = pila[-1]  # la etiqueta abierta más interna, o Z0 si no hay ninguna
        if token == "TEXTO":                  # regla 1: la pila no cambia
            pass
        elif token in APERTURAS:              # reglas 2 a 4: apila
            pila.append(APERTURAS[token])
        elif token not in CIERRES:
            # Ni texto, ni apertura, ni cierre: el símbolo no está en Σ.
            return False, f"Error léxico: '{token}' no pertenece a Σ.", traza
        elif tope == CIERRES[token]:          # reglas 5 a 7: desapila
            pila.pop()
        # Los dos casos que siguen son δ = ∅: es un cierre y no coincide con el tope.
        # En M son lo mismo; el programa los separa para dar un mensaje más claro.
        elif tope == "Z0":
            # Por ejemplo, </p>: no había nada abierto.
            return False, f"Error sintáctico: se cerró '{token}' sin apertura previa.", traza
        else:
            # Por ejemplo, <p> <b> </p>: se cerró una que no es la última abierta.
            return False, f"Error de anidamiento: se leyó '{token}' con {tope} en el tope.", traza
        # La regla se aplicó: se agrega la nueva configuración, sin el símbolo ya leído.
        traza.append(configuracion("q0", tokens[i + 1:], pila))

    # Se terminó la entrada. La regla 8 pide Z0 en el tope: si queda otra cosa,
    # hay etiquetas abiertas y M no puede llegar a qf.
    if pila != ["Z0"]:
        # Se recuperan los nombres desde la pila, de la más interna a la más externa.
        abiertas = [f"<{s.lower()}>" for s in reversed(pila[1:])]
        return False, f"Error sintáctico: etiquetas sin cerrar: {', '.join(abiertas)}.", traza
    # Se llega a qf con toda la entrada leída: M acepta por estado final. Z0 queda en la pila.
    traza.append(configuracion("qf", [], pila))  # regla 8: δ(q0, λ, Z0) = (qf, Z0)
    return True, "Cadena válida (w ∈ L(M)).", traza


# --- Paso 3: unir todo y mostrar el resultado -------------------------------

def analizar_cadena(cadena):
    # Muestra los tokens, la traza (una configuración por línea) y el veredicto.
    tokens = tokenizar(cadena)
    valida, mensaje, traza = simular(tokens)
    print(f"Tokens: {tokens or 'λ'}")
    print("\n⊢ ".join(traza))
    print(f"{'ACEPTADA' if valida else 'RECHAZADA (w ∉ L(M))'}. {mensaje}")


# Esto corre solo al ejecutar el archivo, no cuando los tests lo importan.
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Con una cadena como argumento, la analiza y termina.
        analizar_cadena(sys.argv[1])
    else:
        # Sin argumentos, modo interactivo: pide cadenas hasta que se escriba "salir".
        print("Escribí una cadena (Enter solo = cadena vacía) o 'salir' para terminar.")
        try:
            while (entrada := input("\nCadena MiniHTML > ").strip()).lower() != "salir":
                analizar_cadena(entrada)
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C o Ctrl+D: termina sin mostrar un error.
            pass
