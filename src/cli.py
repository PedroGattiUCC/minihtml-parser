"""
Interfaz de Línea de Comandos (CLI) Interactiva para MiniHTML Parser
Materia: Lenguajes Formales y Autómatas (2026) - UCC
Utiliza la librería Rich para visualización en terminal de árboles sintácticos,
trazas del autómata a pila y reporte de errores.
"""

import sys
import argparse
from typing import List

# Asegurar soporte de caracteres UTF-8 en Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich import print as rprint

from .engine import MiniHTMLParser, ParseResult
from .config import LanguageConfig
from .ast_nodes import DocumentNode, ElementNode, TextNode, ASTNode

console = Console()


def render_rich_ast(node: ASTNode, tree_item: Tree = None) -> Tree:
    """Convierte un ASTNode en una estructura visual de árbol de Rich."""
    if isinstance(node, DocumentNode):
        root = Tree("[bold cyan]Documento MiniHTML (Símbolo Inicial S)[/bold cyan]")
        for child in node.children:
            render_rich_ast(child, root)
        return root
    elif isinstance(node, ElementNode):
        branch = tree_item.add(f"[bold yellow]Elemento <{node.tag}>[/bold yellow] [dim](Línea {node.open_token.line})[/dim]")
        for child in node.children:
            render_rich_ast(child, branch)
        return tree_item
    elif isinstance(node, TextNode):
        tree_item.add(f"[green]TEXTO:[/green] \"[bold white]{node.text}[/bold white]\"")
        return tree_item
    return tree_item


def display_result(result: ParseResult, show_tree: bool = True, show_trace: bool = True):
    """Muestra el resultado completo del análisis en la consola con formato enriquecido."""
    console.print()
    if result.is_valid:
        console.print(Panel(
            f"[bold green]✔ CADENA VÁLIDA (w ∈ L)[/bold green]\n"
            f"[white]Estrategia utilizada:[/white] [cyan]{result.strategy_used}[/cyan]\n"
            f"[white]Tokens procesados:[/white] {len(result.tokens)} tokens\n"
            f"[white]Equivalencia verificada L(G) = L(M):[/white] "
            f"[{'bold green' if result.equivalent_verified else 'yellow'}]{result.equivalent_verified}[/]",
            title="[bold green]Resultado del Análisis Sintáctico[/bold green]",
            border_style="green"
        ))

        # Mostrar Árbol Sintáctico (si está disponible)
        if show_tree and result.ast:
            console.print("\n[bold cyan]Árbol de Análisis Sintáctico (Parse Tree de la GLC):[/bold cyan]")
            rich_tree = render_rich_ast(result.ast)
            console.print(rich_tree)

        # Mostrar Traza de Configuraciones del Autómata a Pila
        if show_trace and result.pda_trace:
            console.print("\n[bold cyan]Traza de Configuraciones Instantáneas (Autómata a Pila M):[/bold cyan]")
            table = Table(title="Computación Paso a Paso en M", show_header=True, header_style="bold magenta")
            table.add_column("Paso", style="dim", width=6)
            table.add_column("Estado", justify="center", width=8)
            table.add_column("Entrada Remanente (w)", style="yellow", width=42)
            table.add_column("Pila (Tope Izq)", style="cyan", width=18)
            table.add_column("Acción / Transición", style="white")

            for step in result.pda_trace:
                table.add_row(
                    str(step.step_number),
                    step.state,
                    step.remaining_input,
                    step.stack_content,
                    step.action_description
                )
            console.print(table)

    else:
        # Cadena inválida
        err = result.error
        err_visual = err.format_visual_error() if err else "Error de sintaxis desconocido."
        console.print(Panel(
            f"[bold red]✘ CADENA INVÁLIDA (w ∉ L)[/bold red]\n\n"
            f"[bold yellow]{err_visual}[/bold yellow]",
            title="[bold red]Fallo Sintáctico Detectado[/bold red]",
            border_style="red"
        ))

        if show_trace and result.pda_trace:
            console.print("\n[bold yellow]Traza de Bloqueo del Autómata a Pila:[/bold yellow]")
            table = Table(show_header=True, header_style="bold red")
            table.add_column("Paso", style="dim", width=6)
            table.add_column("Estado", justify="center", width=8)
            table.add_column("Entrada Remanente", style="yellow", width=38)
            table.add_column("Pila", style="cyan", width=16)
            table.add_column("Evento", style="white")

            for step in result.pda_trace:
                table.add_row(
                    str(step.step_number),
                    step.state,
                    step.remaining_input,
                    step.stack_content,
                    step.action_description
                )
            console.print(table)


def run_benchmark_tests(parser: MiniHTMLParser):
    """Ejecuta la suite oficial de cadenas de prueba."""
    casos = [
        ("Cadena Alfa (α) [Oficial]", "<p> TEXTO <b> TEXTO </b> </p>"),
        ("Cadena Beta (β) [Oficial]", "<p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>"),
        ("Cadena Gamma (γ) [Oficial]", "<p> TEXTO TEXTO </p> <i> TEXTO </i>"),
        ("HTML Real con espacios", "<p>Hola mundo <b>ingenieria</b></p>"),
        ("Documento Vacío (λ)", ""),
        ("Inválida 1: Anidamiento cruzado", "<p> <b> TEXTO </p> </b>"),
        ("Inválida 2: Etiqueta huérfana", "<p> TEXTO </p> </b>"),
        ("Inválida 3: Sin cerrar al final", "<p> <b> TEXTO </p>")
    ]

    console.print(Panel(
        "[bold cyan]EJECUCIÓN DE BATERÍA DE PRUEBAS DE LA CÁTEDRA[/bold cyan]\n"
        "Verificando cadenas válidas e inválidas con correspondencia G y M.",
        border_style="cyan"
    ))

    for nombre, texto in casos:
        console.print(f"\n[bold white]>>> Caso:[/bold white] [yellow]{nombre}[/yellow]")
        console.print(f"[dim]Entrada:[/dim] `{texto}`")
        res = parser.parse(texto, strategy="both")
        display_result(res, show_tree=False, show_trace=False)


def interactive_repl(parser: MiniHTMLParser):
    """Modo interactivo (REPL) para pruebas en vivo durante la defensa oral."""
    console.print(Panel(
        "[bold green]MiniHTML Parser - Consola Interactiva REPL[/bold green]\n"
        "[dim]Escriba una cadena de MiniHTML para validarla en vivo.[/dim]\n"
        "[dim]Comandos especiales: ':tree' (alternar árbol), ':tags' (ver etiquetas), ':salir' (terminar)[/dim]",
        border_style="green"
    ))

    show_tree = True
    show_trace = True

    while True:
        try:
            line = console.input("\n[bold cyan]MiniHTML>[/bold cyan] ").strip()
            if not line:
                continue

            if line in (":salir", ":exit", "exit", "quit"):
                console.print("[yellow]Saliendo de la consola interactiva.[/yellow]")
                break
            elif line == ":tree":
                show_tree = not show_tree
                console.print(f"[cyan]Visualización de árbol:[/cyan] {'Activada' if show_tree else 'Desactivada'}")
                continue
            elif line == ":trace":
                show_trace = not show_trace
                console.print(f"[cyan]Visualización de traza de pila:[/cyan] {'Activada' if show_trace else 'Desactivada'}")
                continue
            elif line == ":tags":
                tags_str = ", ".join(sorted(f"<{t}>" for t in parser.config.allowed_tags))
                console.print(f"[cyan]Etiquetas permitidas actualmente:[/cyan] {tags_str}")
                continue

            result = parser.parse(line, strategy="both")
            display_result(result, show_tree=show_tree, show_trace=show_trace)

        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Sesión finalizada.[/yellow]")
            break


def main():
    arg_parser = argparse.ArgumentParser(
        description="Analizador Sintáctico de MiniHTML (Lenguajes Formales y Autómatas UCC 2026)"
    )
    arg_parser.add_argument("--text", "-t", type=str, help="Cadena de texto a analizar directamente.")
    arg_parser.add_argument("--file", "-f", type=str, help="Ruta a un archivo .html para analizar.")
    arg_parser.add_argument("--test", action="store_true", help="Ejecuta la batería de pruebas de la cátedra.")
    arg_parser.add_argument("--add-tag", type=str, help="Registra una nueva etiqueta en vivo (ej: 'u' o 'h1').")
    arg_parser.add_argument("--strategy", choices=["both", "recursive", "pda"], default="both",
                            help="Estrategia de análisis sintáctico a emplear.")

    args = arg_parser.parse_args()

    config = LanguageConfig()
    if args.add_tag:
        config.register_tag(args.add_tag)
        console.print(f"[bold green]✔ Etiqueta '{args.add_tag}' registrada exitosamente en el lenguaje.[/bold green]")

    parser = MiniHTMLParser(config)

    if args.test:
        run_benchmark_tests(parser)
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
            res = parser.parse(content, strategy=args.strategy)
            display_result(res)
        except Exception as e:
            console.print(f"[bold red]Error al leer archivo:[/bold red] {e}")
    elif args.text is not None:
        res = parser.parse(args.text, strategy=args.strategy)
        display_result(res)
    else:
        interactive_repl(parser)


if __name__ == "__main__":
    main()
