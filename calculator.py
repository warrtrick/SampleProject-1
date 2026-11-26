#!/usr/bin/env python3
"""A small command-line calculator."""

from __future__ import annotations

import argparse
import operator
from typing import Callable


OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "^": operator.pow,
}


def calculate(left: float, operation: str, right: float) -> float:
    """Calculate a result for two numbers and an operator."""
    if operation not in OPERATIONS:
        raise ValueError(f"unsupported operation: {operation}")
    if operation in {"/", "%"} and right == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return OPERATIONS[operation](left, right)


def format_result(result: float) -> str:
    return str(int(result)) if result.is_integer() else str(result)


def run_interactive() -> None:
    print("Calculator (+, -, *, /, %, ^). Type 'q' to quit.")
    while True:
        expression = input("> ").strip()
        if expression.lower() in {"q", "quit", "exit"}:
            break
        parts = expression.split()
        if len(parts) != 3:
            print("Use: number operator number (example: 12 / 4)")
            continue
        try:
            result = calculate(float(parts[0]), parts[1], float(parts[2]))
            print(format_result(result))
        except (ValueError, ZeroDivisionError) as error:
            print(f"Error: {error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate two numbers.")
    parser.add_argument("left", nargs="?", type=float)
    parser.add_argument("operation", nargs="?", choices=OPERATIONS)
    parser.add_argument("right", nargs="?", type=float)
    args = parser.parse_args()

    if args.left is None and args.operation is None and args.right is None:
        run_interactive()
        return
    if args.left is None or args.operation is None or args.right is None:
        parser.error("provide all three arguments: number operator number")

    try:
        print(format_result(calculate(args.left, args.operation, args.right)))
    except ZeroDivisionError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
