import fileinput
from dataclasses import dataclass
from typing import Optional

Program = list[int]


@dataclass
class Computer:
    a: int
    b: int
    c: int

    def get_combo_value(self, op: int) -> int:
        """Get the value of the combo operand."""
        if op < 4:
            return op
        elif op == 4:
            return self.a
        elif op == 5:
            return self.b
        elif op == 6:
            return self.c
        else:
            raise ValueError("Invalid combo operand.")

    def execute_instruction(self, opcode: int, operand: int, outputs: list[int]) -> Optional[int]:
        """Execute a single instruction and return the new instruction pointer offset."""
        if opcode == 0:
            # adv: A = A // (2^(combo operand))
            denominator = self.get_combo_value(operand)
            self.a = self.a // 2**denominator
            return 2

        elif opcode == 1:
            # bxl: B = B XOR literal operand
            self.b = self.b ^ operand
            return 2

        elif opcode == 2:
            # bst: B = (combo operand) % 8
            val = self.get_combo_value(operand)
            self.b = val % 8
            return 2

        elif opcode == 3:
            # jnz: if A != 0: jump to operand (absolute), else ip += 2
            if self.a != 0:
                return None
            else:
                return 2

        elif opcode == 4:
            # bxc: B = B XOR C (operand ignored)
            self.b = self.b ^ self.c
            return 2

        elif opcode == 5:
            # out: output (combo operand % 8)
            val = self.get_combo_value(operand) % 8
            outputs.append(val)
            return 2

        elif opcode == 6:
            # bdv: B = A // (2^(combo operand))
            denominator = self.get_combo_value(operand)
            self.b = self.a // 2**denominator
            return 2

        elif opcode == 7:
            # cdv: C = A // (2^(combo operand))
            denominator = self.get_combo_value(operand)
            self.c = self.a // 2**denominator
            return 2

        raise ValueError("Invalid opcode.")


def parse_input(lines: list[str]) -> tuple[Computer, Program]:
    """Parse the input lines containing register values and program."""
    a = int(lines[0].split(":")[1].strip())
    b = int(lines[1].split(":")[1].strip())
    c = int(lines[2].split(":")[1].strip())

    computer = Computer(a=a, b=b, c=c)

    program_str = lines[3].split(":")[1].strip()
    program = [int(x) for x in program_str.split(",")]

    return computer, program


def run_program(computer: Computer, program: Program) -> list[int]:
    """Run the program and return the outputs."""
    outputs: list[int] = []
    instruction_pointer = 0

    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]

        if instruction_pointer + 1 >= len(program):
            break

        operand = program[instruction_pointer + 1]

        # Execute instruction and update instruction pointer.
        instruction_pointer_change = computer.execute_instruction(opcode, operand, outputs)
        if instruction_pointer_change is None and opcode == 3 and computer.a != 0:
            instruction_pointer = operand
        elif instruction_pointer_change is not None:
            instruction_pointer += instruction_pointer_change

    return outputs


def handler(raw_lines: fileinput.FileInput) -> str:
    """Handle input and return comma-separated output values."""
    lines = [line.strip() for line in raw_lines if line.strip()]
    computer, program = parse_input(lines)

    outputs = run_program(computer, program)
    return ",".join(str(o) for o in outputs) if outputs else ""


if __name__ == "__main__":
    print(handler(fileinput.input()))
