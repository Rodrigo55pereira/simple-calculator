#!/usr/bin/env python3
"""
Exemplos de uso da Calculadora Simples

Este arquivo demonstra como usar a calculadora programaticamente
e mostra vários exemplos de expressões matemáticas.
"""

from simple_calculator import evaluate_expression


def main():
    """Demonstra exemplos de uso da calculadora."""
    
    print("=== Exemplos da Calculadora Simples ===\n")
    
    # Lista de exemplos para demonstrar
    examples = [
        ("2 + 2", "Adição simples"),
        ("10 - 5", "Subtração simples"),
        ("3 * 7", "Multiplicação simples"),
        ("15 / 3", "Divisão simples"),
        ("17 // 5", "Divisão inteira"),
        ("23 % 7", "Módulo (resto da divisão)"),
        ("2 ** 8", "Potenciação"),
        ("(2 + 3) * 4", "Expressão com parênteses"),
        ("10 ** 2 + 5", "Precedência de operadores"),
        ("(8 + 2) / 2", "Expressão complexa"),
        ("2 + 3 * 4", "Precedência: multiplicação antes da adição"),
        ("10 - 5 + 3", "Associatividade da adição/subtração"),
        ("-5 + 3", "Número negativo"),
        ("2.5 * 3", "Números decimais"),
        ("(1 + 2) ** (3 - 1)", "Expressão complexa com parênteses"),
    ]
    
    for expression, description in examples:
        try:
            result = evaluate_expression(expression)
            print(f"{description:40} | {expression:20} = {result}")
        except Exception as e:
            print(f"{description:40} | {expression:20} = ERRO: {e}")
    
    print("\n=== Teste de Erros ===")
    
    # Exemplos que devem gerar erros
    error_examples = [
        ("2 +", "Expressão incompleta"),
        ("abc + 2", "Variável não permitida"),
        ("print('hello')", "Função não permitida"),
        ("2 / 0", "Divisão por zero"),
    ]
    
    for expression, description in error_examples:
        try:
            result = evaluate_expression(expression)
            print(f"{description:30} | {expression:20} = {result}")
        except Exception as e:
            print(f"{description:30} | {expression:20} = ERRO: {e}")


if __name__ == "__main__":
    main()