import ast
import fileinput
from fileinput import FileInput
from typing import Tuple, Type


class SwapSubWithMult(ast.NodeTransformer):
    def visit_Sub(self, n):
        return ast.copy_location(ast.Mult(), n)


def custom_eval(
    expression: str,
    node_transformer: Type[ast.NodeTransformer],
    operators: Tuple[str, str],
) -> int:
    new_ast = ast.parse(expression.replace(operators[0], operators[1]), mode="eval")
    return eval(compile(node_transformer().visit(new_ast), "<string>", "eval"))


def handler(raw_expressions: FileInput) -> int:
    total = 0

    for raw_expression in raw_expressions:
        expression_total = custom_eval(
            raw_expression.strip(), SwapSubWithMult, ("*", "-")
        )
        total += expression_total

    return total


if __name__ == "__main__":
    print(handler(fileinput.input()))
