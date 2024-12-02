import ast
import fileinput
from fileinput import FileInput
from typing import Any, List, Tuple, Type


class SwapAddWithMult(ast.NodeTransformer):
    def visit_Add(self, n):
        return ast.copy_location(ast.Mult(), n)

    def visit_Mult(self, n):
        return ast.copy_location(ast.Add(), n)


def custom_eval(
    expression: str,
    node_transformer: Type[ast.NodeTransformer],
    operators: List[Tuple[str, str]],
) -> Any:
    new_expression = []

    for elem in expression:
        new_elem = elem

        for old_op, new_op in operators:
            if new_elem == old_op:
                new_elem = new_op
                break

        new_expression.append(new_elem)

    new_ast = ast.parse("".join(new_expression), mode="eval")

    return eval(compile(node_transformer().visit(new_ast), "<string>", "eval"))


def handler(raw_expressions: FileInput) -> int:
    total = 0

    for raw_expression in raw_expressions:
        expression_total = custom_eval(
            raw_expression.strip(), SwapAddWithMult, [("+", "*"), ("*", "+")]
        )
        total += expression_total

    return total


if __name__ == "__main__":
    print(handler(fileinput.input()))
