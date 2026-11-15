---
tag: SSF77K
kind: technique
slug: meta-tracing
name: Meta-tracing
aliases:
- meta-tracing JIT
area: compilers-and-program-analysis/code-generation-and-jit
level: research
summary: Traces the interpreter that runs a user program instead of the program, so a JIT compiler is derived from an annotated interpreter.
prereqs: [tracing-jit-compilation]
see_also: [tracing-jit-compilation, self-optimizing-ast-interpreter, partial-evaluation, futamura-projections, binding-time-analysis, deoptimization, just-in-time-compilation, constant-folding]
sources:
  - paper: doi:10.1145/1565824.1565827
    title: "Carl Friedrich Bolz, Antonio Cuni, Maciej Fijałkowski and Armin Rigo, Tracing the meta-level: PyPy's tracing JIT compiler, ICOOOLPS 2009, 18-25"
    locator: the problem of applying a tracing JIT compiler to an interpreter, the hints jit_merge_point and can_enter_jit with green and red variables, the closing of a trace when the position in the user program repeats, and the folding of the green values
  - paper: doi:10.1145/2069172.2069181
    title: Carl Friedrich Bolz, Antonio Cuni, Maciej Fijałkowski, Michael Leuschel, Samuele Pedroni and Armin Rigo, Runtime feedback in a meta-tracing JIT for efficient dynamic languages, ICOOOLPS 2011, 1-8
    locator: the hints that turn a run-time value into a constant of the trace (promotion) and that mark functions without side effects whose calls on constants can be folded
  - paper: doi:10.1016/j.scico.2013.02.001
    title: Carl Friedrich Bolz and Laurence Tratt, The impact of meta-tracing on VM design and implementation, Science of Computer Programming 98, 2015, 408-421
    locator: the experience of building a language virtual machine with the RPython meta-tracing system, and the hints the interpreter needs
  - paper: doi:10.1145/1542476.1542528
    title: Andreas Gal and others (16 authors), Trace-based just-in-time type specialization for dynamic languages, PLDI 2009, 465-478
    locator: tracing of a user program in a language interpreter, which meta-tracing moves one level down
---

Meta-tracing applies a [tracing JIT compiler](/tracing-jit-compilation/) to an interpreter instead of to the user program. The language implementer writes an interpreter for a language, in a restricted language such as RPython, and adds a few hints. A generic tracing JIT compiler, built once, records what the *interpreter* does while it runs a hot loop of the user program, and compiles that. Because the trace follows one path of the user loop through the interpreter, the work of decoding and dispatching the user program's instructions depends only on values that are fixed for that loop, and the optimizer folds it away. What is left is close to the code a JIT compiler for the language would have made. Bolz, Cuni, Fijałkowski and Rigo described the technique for PyPy in 2009. The common mistake is to think that the user program is traced. It is not: the tracer never sees the user program as code, only the interpreter that runs it.

## In plain words

Writing a JIT compiler for a language is a big job. Writing an interpreter is much smaller. Meta-tracing gives you the first from the second.

A tracing compiler records what a running program does in a busy loop and turns it into fast code. Meta-tracing points this recorder at the interpreter. While the interpreter runs the user's loop, the recorder writes down every step the interpreter takes: read the next instruction, look up what it means, do it. The interpreter writer marks which variables say "where we are in the user program". With that mark, the recorder knows when the user's loop has gone round once, and it knows that the reading and looking up give the same answer every round. So the optimizer throws those steps away and keeps only the real work.

## When it applies

- You build a language implementation and want a JIT compiler without writing one for each language.
- The interpreter is written in a language that the meta-tracing system can trace, such as RPython, a subset of Python that can be analyzed and translated to C.
- The interpreter has a main dispatch loop, and its state can be split into the position in the user program, which is constant along a user loop, and the data of the user program.
- The user programs spend their time in loops that take the same path most of the time, as for any tracing compiler.

## The template

### The problem with tracing an interpreter naively

A tracing compiler finds loops by watching backward jumps and closes a trace when control is back at the start. In an interpreter, the hottest loop is the dispatch loop itself, and one iteration of it runs one user instruction. A trace of one iteration covers one user instruction and then must guard on the next opcode, which is different every time. Such traces are useless. What should be traced is the *user* loop: many iterations of the dispatch loop, until the user program is back at the same position.

### The hints

In the system of Bolz and others the interpreter writer adds two hints and declares the variables of the dispatch loop as one of two kinds.

- **Green variables** describe the position in the user program, such as the bytecode object and the program counter. They are constant along one path of a user loop.
- **Red variables** are all others, such as the operand stack, the user variables and the frame.
- **`jit_merge_point(greens, reds)`** is placed at the top of the dispatch loop. It tells the tracer where an iteration of the interpreter starts.
- **`can_enter_jit(greens, reds)`** is placed where the user program jumps backward. It tells the tracer where a user loop can close, and the system keeps a counter per value of the green variables there.

Later systems add hints such as *promotion*, which makes a red value a constant of the trace behind a guard, and a mark for functions without side effects, whose calls on constants can be folded.

### The algorithm

1. **Count.** At `can_enter_jit`, the counter for the current green values grows. At a threshold, tracing starts at the next `jit_merge_point`, with those green values as the *key* of the trace.
2. **Record the interpreter.** The tracer runs the interpreter in recording mode and logs the interpreter's own operations: reads of the bytecode array, comparisons of opcodes, operations on the stack, calls to helper functions, with guards at each branch of the interpreter.
3. **Close.** When the tracer reaches `jit_merge_point` again with the same green values as the key, the user loop has gone round once, and the trace ends with a jump to its start.
4. **Fold the green part.** In the trace, the green variables at the start are constants, equal to the key. Every value computed only from green values and immutable data, such as `code[pc]`, is a constant too, and every guard on such a value always passes. Constant folding removes these operations and guards.
5. **Optimize the rest, compile, and store** the trace in a cache under its key. When the interpreter reaches `jit_merge_point` with green values that have a trace, it enters the trace. Side exits go back into the interpreter, as in any tracing compiler.

### Why it is correct

The trace is a trace of the interpreter program $P_I$, so the claim of the page on [tracing JIT compilation](/tracing-jit-compilation/) applies to it: from any state of $P_I$ at the merge point that matches the start of the trace, the trace either does one round of the recorded path and arrives in the matching state, or leaves at a side exit with the exact state of $P_I$. And $P_I$ running a user program $Q$ is, by definition, the meaning of $Q$. So the trace is equivalent to running $Q$ on the paths it covers. Only step 4 needs a separate argument.

**Claim.** If the trace is entered only from states of the interpreter whose green values equal the key, and the data that green values point to is immutable, then removing the operations and guards that depend only on green values and that data does not change the meaning of the trace.

*Proof.* By induction on the position in the trace, every operation whose inputs are green values, constants and reads of immutable data computes the same value as in the recorded run: at the start the green values equal the key, which is the value they had in the recorded run, and each such operation is a function of its inputs. So each of these values can be replaced by the constant seen during recording. A guard on such a value checks a condition that held during recording, so it holds on every run of the trace and never exits. Removing it does not change any run. $\square$

Both conditions are real requirements. The trace cache must be keyed by the green values, so that a trace for `pc = 0` is never entered at `pc = 4`. And the bytecode must not change while traces for it exist, or the system must treat such a change as an invalidation, as in [deoptimization](/deoptimization/).

### A worked example

An interpreter for a tiny accumulator language, with the hints:

```
interpret(code, a):
    pc = 0; acc = 0
    loop:
        jit_merge_point(greens = (code, pc), reds = (a, acc))
        op = code[pc]; arg = code[pc + 1]; pc = pc + 2
        if op = ADD_A:     acc = acc + a
        if op = DECR_A:    a = a - 1
        if op = JUMP_IF_A: if a ≠ 0 then pc = arg; can_enter_jit(greens = (code, pc), reds = (a, acc))
        if op = RETURN:    return acc
```

The user program `code = [ADD_A, 0, DECR_A, 0, JUMP_IF_A, 0, RETURN, 0]` computes $a + (a - 1) + \dots + 1$. With $a = 100$, it returns $5050$, after 100 rounds of its loop.

The trace for the key $(\mathit{code}, 0)$ records three iterations of the dispatch loop:

```
 1  op1 = getitem(code, 0)          10  a1 = a - 1
 2  arg1 = getitem(code, 1)         11  op3 = getitem(code, 4)
 3  pc1 = 0 + 2                     12  arg3 = getitem(code, 5)
 4  guard op1 = ADD_A               13  pc3 = pc2 + 2
 5  acc1 = acc + a                  14  guard op3 = JUMP_IF_A
 6  op2 = getitem(code, 2)          15  c = a1 ≠ 0
 7  arg2 = getitem(code, 3)         16  guard c
 8  pc2 = pc1 + 2                   17  pc4 = arg3
 9  guard op2 = DECR_A              18  jump to start with (code, pc4), (a1, acc1)
```

`code` and `pc` are green, and `code` is immutable, so lines 1 to 4, 6 to 9, 11 to 14 and 17 are folded: `op1` is `ADD_A`, the guard on it always passes, `pc4` is 0, and so on. Of 18 operations, 4 and the jump remain:

```
loop:  acc1 = acc + a;  a1 = a - 1;  c = a1 ≠ 0;  guard c, else exit to the interpreter at pc 6;  jump loop
```

This is the loop a compiler for the tiny language would produce. The one guard that is left tests a red value, the user variable `a`, and it fails once, when $a$ reaches 0, which sends the interpreter to `RETURN` with $\mathit{acc} = 5050$.

## Classic examples

- **PyPy.** The Python interpreter of PyPy is written in RPython, and its JIT compiler is generated from it by the RPython toolchain with meta-tracing. Bolz and others introduced the technique there in 2009, first on small example interpreters and then for Python.
- **Other languages on RPython.** The same toolchain has been used for other languages, among them the Converge language, whose virtual machine Bolz and Tratt describe, with the hints such an interpreter needs.
- **Compared to Truffle.** The Truffle framework reaches the same goal, a compiler from an interpreter, by partial evaluation of a [self-optimizing AST interpreter](/self-optimizing-ast-interpreter/) instead of by tracing. Both are dynamic forms of the first [Futamura projection](/futamura-projections/): specializing an interpreter to a fixed program gives a compiled program.

## Variations

- **Promotion.** A hint that turns a red value, such as the class of an object, into a constant of the trace behind a guard. This is how a meta-tracing interpreter gets the effect of an [inline cache](/inline-caching/) without writing one: the guard on the promoted class is the cache check, and the folded lookup is the cached answer.
- **Pure functions.** A mark that a helper function has no effects and depends only on its arguments, so that a call with constant arguments is folded, for example a method lookup on a promoted class with an unchanged class table.
- **Virtual objects.** Objects allocated in the trace that do not escape it, such as boxed integers of the interpreter, are removed by an escape analysis on the trace and rebuilt only at side exits.
- **Method-based meta-compilation.** Partial evaluation of the interpreter along all paths of a user method, instead of one traced path, is the approach of Truffle and Graal.

## Pitfalls

- **Thinking that the user program is traced.** The tracer sees only interpreter operations. A loop in the user program is found only through the green variables and `can_enter_jit`. Without correct hints, the system traces the dispatch loop and gains nothing.
- **A green variable that is not constant.** If a variable declared green can change along a user loop, for example a mutable bytecode array, folding it is wrong. Green values must be immutable for the life of the trace, or a change must invalidate the trace.
- **Too few green variables.** If the position in the user program is not fully green, the opcode reads are not constant, and the dispatch overhead stays in the trace.
- **Interpreter code that hides constants.** Hash-table lookups, global state and indirect calls in the interpreter can stop folding unless they are marked pure or promoted. Meta-tracing rewards an interpreter written with the tracer in mind.
- **The usual tracing problems.** Branchy user loops, recursion and long traces hurt meta-tracing as they hurt any tracing compiler, and side exits must rebuild the interpreter's state exactly.

## Exercises

1. In the worked example, which operations of the trace remain if `pc` is declared red instead of green? What does the trace then test on every round?
2. Add an instruction `ADD_CONST k` to the tiny language and show the folded trace for a loop that uses it.
3. Explain why the trace cache must be keyed by the values of all green variables, and give a run where keying by `pc` alone is wrong because two code objects share the same `pc`.
4. A user program changes its own bytecode while a trace for it exists. Which step of the claim fails, and what must the system do?
5. Compare promotion of the class of an object with a [polymorphic inline cache](/polymorphic-inline-cache/). What plays the role of the cache entries when a site sees two classes?

## References
