"""Simple Calculator (Portuguese)

Permite avaliar expressões matemáticas com segurança usando AST, 
suportando: +, -, *, /, //, %, ** e parênteses. 

Uso:
  - Modo argumento: python3 simple_calculator.py "2 + 3 * (4 - 1)"
  - Modo interativo: python3 simple_calculator.py
    - Digite expressões e pressione Enter
    - Comandos para sair: sair | quit | exit | q
"""

from __future__ import annotations

import ast
import operator
import sys
from typing import Any, Callable, Mapping, Optional, Union


class SafeEvaluator(ast.NodeVisitor):
    """Avalia uma expressão matemática simples de forma segura.

    Permite apenas números, operações binárias (+, -, *, /, //, %, **),
    operações unárias (+, -) e parênteses. Qualquer outro elemento (nomes,
    chamadas de função, atribuições etc.) é bloqueado.
    """

    Number = Union[int, float]

    _binary_operators: Mapping[type[ast.AST], Callable[[Number, Number], Number]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    _unary_operators: Mapping[type[ast.AST], Callable[[Number], Number]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def visit_Expression(self, node: ast.Expression) -> Any:  # type: ignore[override]
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Any:  # type: ignore[override]
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)

        if op_type not in self._binary_operators:
            raise ValueError("Operador binário não suportado")

        func = self._binary_operators[op_type]
        return func(left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:  # type: ignore[override]
        operand = self.visit(node.operand)
        op_type = type(node.op)

        if op_type not in self._unary_operators:
            raise ValueError("Operador unário não suportado")

        func = self._unary_operators[op_type]
        return func(operand)

    def visit_Constant(self, node: ast.Constant) -> Any:  # type: ignore[override]
        value = node.value
        if isinstance(value, bool):
            # Evita True/False (subclasses de int)
            raise ValueError("Valores booleanos não são permitidos")
        if not isinstance(value, (int, float)):
            raise ValueError("Apenas números são permitidos")
        return value

    # Compatibilidade com versões antigas do Python
    def visit_Num(self, node: ast.Num) -> Any:  # type: ignore[override]
        return self.visit_Constant(ast.Constant(node.n))

    def generic_visit(self, node: ast.AST) -> Any:  # type: ignore[override]
        raise ValueError(
            f"Expressão contém elemento não permitido: {node.__class__.__name__}"
        )


def evaluate_expression(expression: str) -> float:
    """Avalia a expressão matemática e retorna o resultado como float/int."""
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Expressão inválida") from exc

    evaluator = SafeEvaluator()
    result = evaluator.visit(parsed)
    return result


def _print_header() -> None:
    print("Calculadora Simples (segura)")
    print("Suporta: +, -, *, /, //, %, ** e parênteses")
    print("Comandos: 'menu' volta ao menu, 'sair'|'quit'|'exit'|'q' encerra")


EXIT_COMMANDS = {"sair", "quit", "exit", "q"}
MENU_COMMANDS = {"menu", "m"}

# Mapeamento direto símbolo -> função
OP_SYMBOL_TO_FUNC: Mapping[str, Callable[[SafeEvaluator.Number, SafeEvaluator.Number], SafeEvaluator.Number]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}


def _is_exit(cmd: str) -> bool:
    return cmd.lower() in EXIT_COMMANDS


def _is_menu(cmd: str) -> bool:
    return cmd.lower() in MENU_COMMANDS


def _parse_number_input(prompt: str) -> Optional[SafeEvaluator.Number]:
    """Lê um número do usuário.

    Retorna None quando o usuário pede 'menu'.
    Lança SystemExit quando o usuário pede sair.
    """
    while True:
        s = input(prompt).strip()
        if _is_exit(s):
            raise SystemExit(0)
        if _is_menu(s):
            return None
        try:
            # Aceita int ou float
            value = float(s)
            if value.is_integer():
                return int(value)
            return value
        except ValueError:
            print("Entrada inválida. Digite um número, 'menu' ou 'sair'.")


def _choose_operation() -> Optional[str]:
    """Pergunta ao usuário qual operação deseja.

    Retorna o símbolo da operação (ex: '+').
    Retorna None quando o usuário pede 'menu'.
    Lança SystemExit quando o usuário pede sair.
    """
    ops = " ".join(OP_SYMBOL_TO_FUNC.keys())
    while True:
        s = input(f"Operação ({ops}): ").strip()
        if _is_exit(s):
            raise SystemExit(0)
        if _is_menu(s):
            return None
        if s in OP_SYMBOL_TO_FUNC:
            return s
        print("Operação inválida. Use um dos símbolos listados, 'menu' ou 'sair'.")


def _guided_loop() -> None:
    print("Modo guiado: informe números e operação. ('menu' volta, 'sair' encerra)")
    while True:
        first = _parse_number_input("Primeiro número: ")
        if first is None:
            return  # menu
        op = _choose_operation()
        if op is None:
            return  # menu
        second = _parse_number_input("Segundo número: ")
        if second is None:
            return  # menu
        try:
            func = OP_SYMBOL_TO_FUNC[op]
            result = func(first, second)
            print(f"Resultado: {result}")
        except ZeroDivisionError:
            print("Erro: divisão por zero não é permitida.")


def _expression_loop() -> None:
    print("Modo expressão: digite expressões. ('menu' volta, 'sair' encerra)")
    while True:
        expr = input(">>> ").strip()
        if _is_exit(expr):
            raise SystemExit(0)
        if _is_menu(expr):
            return
        if not expr:
            continue
        try:
            result = evaluate_expression(expr)
        except Exception as exc:  # noqa: BLE001 - CLI amigável
            print(f"Erro: {exc}")
            continue
        print(result)


def main(argv: list[str]) -> int:
    if argv:
        expr = " ".join(argv)
        try:
            result = evaluate_expression(expr)
        except Exception as exc:  # noqa: BLE001 - CLI amigável
            print(f"Erro: {exc}", file=sys.stderr)
            return 1
        else:
            print(result)
            return 0

    _print_header()
    while True:
        try:
            choice = input("Escolha o modo: [1] Guiado | [2] Expressão > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if _is_exit(choice):
            break
        if choice in {"1", "g", "G"}:
            try:
                _guided_loop()
            except SystemExit:
                return 0
        elif choice in {"2", "e", "E"}:
            try:
                _expression_loop()
            except SystemExit:
                return 0
        else:
            print("Opção inválida. Digite 1 (Guiado), 2 (Expressão) ou 'sair'.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


