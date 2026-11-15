# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/activation-record/. The authors are listed in prov/4XG2M7.jsonl.

"""Activation records for a language with nested functions.

A function is ("fun", name, params, locals, body, children). The children
are the functions declared inside it; they can read and write the
parameters and locals of every enclosing function. The program is a
function named main with no parameters. Expressions are:

    ("int", k)  ("var", x)  ("assign", x, e)  ("seq", e1, e2)
    ("add", e1, e2)  ("sub", e1, e2)  ("mul", e1, e2)  ("lt", e1, e2)
    ("if", c, e1, e2)    the test is true when c is not 0
    ("call", f, [e1, ...])

The compiler emits code for a stack machine. A frame (activation record)
starts at the frame pointer FP:

    FP + 0   return address
    FP + 1   dynamic link: the FP of the caller
    FP + 2   static link: the FP of the frame of the enclosing function,
             or the saved display entry in the display variant
    FP + 3   the parameters, then the locals
"""

RA, DL, SL, HEADER = 0, 1, 2, 3


class OutOfFuel(Exception):
    """The program made more calls than the limit allows."""


def find_fun(chain: list, f: str) -> int:
    """The index in chain of the innermost function whose children declare f."""
    for i in range(len(chain) - 1, -1, -1):
        if any(c[1] == f for c in chain[i][5]):
            return i
    raise NameError(f)


def compile_program(main: tuple, mode: str = "static") -> list[tuple]:
    """Compile to stack machine code. mode is "static" (static links) or
    "display" (a display of frame pointers indexed by depth)."""
    code: list[tuple] = []
    labels: dict[str, int] = {}
    fixups: list[tuple] = []
    names: dict[int, str] = {id(main): "main"}
    count = [0]

    def new_label() -> str:
        count[0] += 1
        return "L%d" % count[0]

    def slot(chain: list, x: str) -> tuple[int, int]:
        # (depth of the function that declares x, offset of x in its frame)
        for d in range(len(chain) - 1, -1, -1):
            declared = list(chain[d][2]) + list(chain[d][3])
            if x in declared:
                return d, HEADER + declared.index(x)
        raise NameError(x)

    def access(op: str, chain: list, x: str) -> None:
        d, off = slot(chain, x)
        if mode == "display":
            code.append((op + "D", d, off))
        else:
            code.append((op, len(chain) - 1 - d, off))  # hops along the static links

    def expr(e: tuple, chain: list) -> None:
        k = e[0]
        if k == "int":
            code.append(("PUSH", e[1]))
        elif k == "var":
            access("LOAD", chain, e[1])
        elif k == "assign":
            expr(e[2], chain)
            access("STORE", chain, e[1])
        elif k == "seq":
            expr(e[1], chain)
            code.append(("POP",))
            expr(e[2], chain)
        elif k in ("add", "sub", "mul", "lt"):
            expr(e[1], chain)
            expr(e[2], chain)
            code.append((k.upper(),))
        elif k == "if":
            other, end = new_label(), new_label()
            expr(e[1], chain)
            fixups.append((len(code), other))
            code.append(("JZ", None))
            expr(e[2], chain)
            fixups.append((len(code), end))
            code.append(("JMP", None))
            labels[other] = len(code)
            expr(e[3], chain)
            labels[end] = len(code)
        elif k == "call":
            i = find_fun(chain, e[1])
            callee = next(c for c in chain[i][5] if c[1] == e[1])
            if len(e[2]) != len(callee[2]):
                raise TypeError("wrong number of arguments for " + e[1])
            code.append(("MARK",))
            for a in e[2]:
                expr(a, chain)
            fixups.append((len(code), names[id(callee)]))
            # The callee is declared in chain[i], so its static link is the frame
            # of chain[i], len(chain) - 1 - i hops from the frame of the caller.
            code.append(("CALL", None, len(chain) - 1 - i, len(e[2])))
        else:
            raise ValueError("bad expression: %r" % (e,))

    def function(fn: tuple, chain: list) -> None:
        chain = chain + [fn]
        for c in fn[5]:
            names[id(c)] = "%s.%s.%d" % (names[id(fn)], c[1], len(names))
        labels[names[id(fn)]] = len(code)
        code.append(("ENTER", len(fn[3]), len(chain) - 1))
        expr(fn[4], chain)
        code.append(("RET", len(chain) - 1))
        for c in fn[5]:
            function(c, chain)

    code.append(("MARK",))
    fixups.append((len(code), "main"))
    code.append(("CALL", None, 0, 0))
    code.append(("HALT",))
    function(main, [])
    for at, lab in fixups:
        ins = code[at]
        code[at] = (ins[0], labels[lab]) + ins[2:]
    return code


def run_machine(code: list[tuple], max_calls: int = 1000, follow: str = "static") -> int:
    """Run the code and return the value of main. With follow="dynamic",
    LOAD and STORE follow the dynamic links instead of the static links,
    which is wrong; it is here to show the difference."""
    stack: list[int] = [0, 0, 0]  # the frame of the startup code
    fp, pc, calls = 0, 0, 0
    display: list[int] = [0] * 64
    link = SL if follow == "static" else DL
    uses_display = any(c[0] in ("LOADD", "STORED") for c in code)

    def frame(hops: int) -> int:
        a = fp
        for _ in range(hops):  # @line L7
            a = stack[a + link]
        return a

    while True:
        ins = code[pc]
        pc += 1
        op = ins[0]
        if op == "PUSH":
            stack.append(ins[1])
        elif op == "POP":
            stack.pop()
        elif op in ("ADD", "SUB", "MUL", "LT"):
            b = stack.pop()
            a = stack.pop()
            stack.append({"ADD": a + b, "SUB": a - b, "MUL": a * b, "LT": int(a < b)}[op])
        elif op == "LOAD":
            stack.append(stack[frame(ins[1]) + ins[2]])  # @line L8
        elif op == "STORE":
            stack[frame(ins[1]) + ins[2]] = stack[-1]
        elif op == "LOADD":
            stack.append(stack[display[ins[1]] + ins[2]])
        elif op == "STORED":
            stack[display[ins[1]] + ins[2]] = stack[-1]
        elif op == "JZ":
            if stack.pop() == 0:
                pc = ins[1]
        elif op == "JMP":
            pc = ins[1]
        elif op == "MARK":
            stack += [0, 0, 0]  # @line L1
        elif op == "CALL":
            calls += 1
            if calls > max_calls:
                raise OutOfFuel()
            _, target, hops, nargs = ins
            base = len(stack) - nargs - HEADER  # @line L2
            stack[base + RA] = pc
            stack[base + DL] = fp
            stack[base + SL] = frame(hops)  # @line L3
            fp, pc = base, target
        elif op == "ENTER":
            stack += [0] * ins[1]  # @line L4
            if uses_display:
                stack[fp + SL] = display[ins[2]]  # save the old entry
                display[ins[2]] = fp
        elif op == "RET":
            result = stack.pop()
            ra, dl = stack[fp + RA], stack[fp + DL]  # @line L5
            if uses_display:
                display[ins[1]] = stack[fp + SL]
            del stack[fp:]
            stack.append(result)
            pc, fp = ra, dl  # @line L6
        elif op == "HALT":
            return stack[-1]
        else:
            raise ValueError("bad instruction: %r" % (ins,))


def evaluate(main: tuple, max_calls: int = 1000) -> int:
    """A direct evaluator with environments, for comparison. An environment
    is (function, variables, the environment of the enclosing function)."""
    calls = [0]

    def lookup(env: tuple, x: str) -> dict:
        while x not in env[1]:
            env = env[2]
        return env[1]

    def ev(e: tuple, env: tuple) -> int:
        k = e[0]
        if k == "int":
            return e[1]
        if k == "var":
            return lookup(env, e[1])[e[1]]
        if k == "assign":
            v = ev(e[2], env)
            lookup(env, e[1])[e[1]] = v
            return v
        if k == "seq":
            ev(e[1], env)
            return ev(e[2], env)
        if k in ("add", "sub", "mul", "lt"):
            a, b = ev(e[1], env), ev(e[2], env)
            return {"add": a + b, "sub": a - b, "mul": a * b, "lt": int(a < b)}[k]
        if k == "if":
            return ev(e[2], env) if ev(e[1], env) != 0 else ev(e[3], env)
        if k == "call":
            outer = env
            while not any(c[1] == e[1] for c in outer[0][5]):
                outer = outer[2]
            fn = next(c for c in outer[0][5] if c[1] == e[1])
            args = [ev(a, env) for a in e[2]]
            calls[0] += 1
            if calls[0] > max_calls:
                raise OutOfFuel()
            local = dict(zip(fn[2], args))
            for x in fn[3]:
                local[x] = 0
            return ev(fn[4], (fn, local, outer))
        raise ValueError("bad expression: %r" % (e,))

    calls[0] += 1
    return ev(main[4], (main, {x: 0 for x in main[3]}, None))
