---
tag: NE50NV
kind: theorem
slug: futamura-projections
name: Futamura projections
aliases:
- Futamura's three projections
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Specializing an interpreter to a program gives a compiled program, specializing the specializer to the interpreter gives a compiler.
prereqs: [partial-evaluation, s-m-n-theorem]
see_also: [binding-time-analysis, meta-tracing, self-optimizing-ast-interpreter, just-in-time-compilation, tracing-jit-compilation, supercompilation, kleene-recursion-theorem]
sources:
  - paper: doi:10.1023/A:1010095604496
    title: "Yoshihiko Futamura, Partial evaluation of computation process, an approach to a compiler-compiler, Higher-Order and Symbolic Computation 12(4), 1999, 381-391"
    locator: the reprint of the 1971 paper, with the specialization of an interpreter to a program, of the specializer to an interpreter, and of the specializer to itself
  - book: isbn:9780130202499
    title: Neil D. Jones, Carsten K. Gomard and Peter Sestoft, Partial Evaluation and Automatic Program Generation, Prentice Hall, 1993
    locator: the chapter on the Futamura projections and self-application, generating extensions, the compiler generator, and why self-application needs binding-time analysis
  - paper: doi:10.1007/3-540-15976-2_6
    title: "Neil D. Jones, Peter Sestoft and Harald Søndergaard, An experiment in partial evaluation: the generation of a compiler generator, Rewriting Techniques and Applications (RTA 1985), LNCS 202, 124-140"
    locator: the first specializer that generated compilers and a compiler generator by self-application, with an annotation of the specializer computed before specialization
  - paper: doi:10.1145/243439.243447
    title: Neil D. Jones, An introduction to partial evaluation, ACM Computing Surveys 28(3), 1996, 480-503
    locator: the three projections derived from the mix equation, and the practical conditions for self-application
  - paper: doi:10.1016/0304-3975(82)90111-6
    title: "Andrei P. Ershov, Mixed computation: potential applications and problems for study, Theoretical Computer Science 18(1), 1982, 41-67"
    locator: the generating extension of a program and compilation by mixed computation of an interpreter
---

The Futamura projections are three equations that follow from the definition of a [partial evaluator](/partial-evaluation/). A specializer $\mathit{mix}$ takes a program and the values of some of its inputs and makes a residual program for the other inputs. Apply it to an interpreter and a source program, and the result is the source program compiled. Apply it to itself and the interpreter, and the result is a compiler. Apply it to itself twice, and the result is a compiler generator. Futamura described the projections in 1971, and the proof is three lines of substitution. The common mistake is to think the theorem promises good compilers. It does not: the trivial specializer, which only stores its static input in the program, satisfies all three equations and gives a "compiler" that pairs the interpreter with the source program. Useful results need a specializer that removes the interpretive work, and self-application in practice needs an offline specializer with a [binding-time analysis](/binding-time-analysis/).

## Statement

**Setting.** Fix a programming language $L$ whose programs are data of $L$, so that an $L$-program can take $L$-programs as input. For a program $q$ write $[\![q]\!]$ for the partial function it computes. An equation $a = b$ between outcomes means that both are undefined or both are defined and equal. A program with two inputs gets them as a pair.

**Hypotheses.**

- *(mix)* $\mathit{mix}$ is an $L$-program that satisfies the *mix equation*: for every $L$-program $p$ of two inputs and all values $s$ and $d$, $[\![\mathit{mix}]\!](p, s)$ is defined and is an $L$-program, and $[\![\,[\![\mathit{mix}]\!](p, s)\,]\!](d) = [\![p]\!](s, d)$.
- *(int)* $\mathit{int}$ is an $L$-program that is an interpreter for a language $S$: for every $S$-program $\mathit{src}$ and every value $d$, $[\![\mathit{int}]\!](\mathit{src}, d) = [\![\mathit{src}]\!]_S(d)$.

**Theorem (the three projections).** Define $\mathit{target} = [\![\mathit{mix}]\!](\mathit{int}, \mathit{src})$, $\mathit{comp} = [\![\mathit{mix}]\!](\mathit{mix}, \mathit{int})$ and $\mathit{cogen} = [\![\mathit{mix}]\!](\mathit{mix}, \mathit{mix})$. Then:

1. $\mathit{target}$ is an $L$-program equivalent to $\mathit{src}$: $[\![\mathit{target}]\!](d) = [\![\mathit{src}]\!]_S(d)$ for all $d$.
2. $\mathit{comp}$ is a compiler from $S$ to $L$: $[\![\mathit{comp}]\!](\mathit{src}) = [\![\mathit{mix}]\!](\mathit{int}, \mathit{src})$, the program of item 1, for every $S$-program $\mathit{src}$.
3. $\mathit{cogen}$ is a compiler generator: $[\![\mathit{cogen}]\!](\mathit{int}) = \mathit{comp}$. More generally, for every $L$-program $p$ of two inputs, $g = [\![\mathit{cogen}]\!](p)$ is a *generating extension* of $p$: $[\![\,[\![g]\!](s)\,]\!](d) = [\![p]\!](s, d)$. And $[\![\mathit{cogen}]\!](\mathit{mix}) = \mathit{cogen}$.

The equalities in items 2 and 3 are equalities of program texts, not only of the functions that the texts compute: the compiler returns exactly the program that $\mathit{mix}$ would return.

**The partial case.** If $\mathit{mix}$ satisfies the mix equation only for the $(p, s)$ on which it stops, each item holds whenever every specialization named in its proof stops.

## In plain words

A specializer takes a program and part of its input, and writes a new program that waits for the rest.

Give it an interpreter and a user program. The new program waits only for the user's data, and it does what the interpreter would do with that user program. That is a translation of the user program: a compiled program.

Now give the specializer a copy of itself and the interpreter. The new program waits for a user program and writes the translation. That is a compiler, made from an interpreter without writing a compiler.

Give the specializer two copies of itself. The new program waits for an interpreter and writes its compiler. That is a compiler generator.

None of this says the results are fast. That depends on how well the specializer works.

## Proof

Each item applies the mix equation once or twice, with a different choice of $p$, $s$ and $d$.

*Item 1.* Take $p = \mathit{int}$ and $s = \mathit{src}$ in the mix equation, then use (int):

$$[\![\mathit{target}]\!](d) = [\![\,[\![\mathit{mix}]\!](\mathit{int}, \mathit{src})\,]\!](d) = [\![\mathit{int}]\!](\mathit{src}, d) = [\![\mathit{src}]\!]_S(d).$$

*Item 2.* Take $p = \mathit{mix}$, $s = \mathit{int}$ and $d = \mathit{src}$. This is allowed, since $\mathit{mix}$ is itself an $L$-program of two inputs:

$$[\![\mathit{comp}]\!](\mathit{src}) = [\![\,[\![\mathit{mix}]\!](\mathit{mix}, \mathit{int})\,]\!](\mathit{src}) = [\![\mathit{mix}]\!](\mathit{int}, \mathit{src}) = \mathit{target}.$$

By item 1, the output is an $L$-program equivalent to $\mathit{src}$, so $\mathit{comp}$ is a compiler.

*Item 3.* Take $p = \mathit{mix}$, $s = \mathit{mix}$ and $d = p$ for any $p$:

$$[\![\mathit{cogen}]\!](p) = [\![\,[\![\mathit{mix}]\!](\mathit{mix}, \mathit{mix})\,]\!](p) = [\![\mathit{mix}]\!](\mathit{mix}, p).$$

With $p = \mathit{int}$ the right side is $\mathit{comp}$ by definition. With $p = \mathit{mix}$ it is $\mathit{cogen}$. For a general $p$, let $g = [\![\mathit{mix}]\!](\mathit{mix}, p)$. The mix equation with $(\mathit{mix}, p, s)$ gives $[\![g]\!](s) = [\![\mathit{mix}]\!](p, s)$, and the mix equation with $(p, s, d)$ gives $[\![\,[\![\mathit{mix}]\!](p, s)\,]\!](d) = [\![p]\!](s, d)$. Together, $[\![\,[\![g]\!](s)\,]\!](d) = [\![p]\!](s, d)$.

*The partial case.* Each step above is one use of the mix equation at a named $(p, s)$, or a use of (int). If each of these specializations stops, each step holds, and so does the chain. $\square$

## Consequences

- **Interpreters as specifications of compilers.** A language implementer who writes an interpreter and has a good specializer gets compiled code (item 1) and a compiler (item 2). Item 2 also says the compiler is correct if the interpreter and the specializer are: there is nothing else to prove.
- **A worked first projection.** The [partial evaluation](/partial-evaluation/) page specializes an interpreter for a two-register machine to the program `0: jz 5, 1: dec, 2: inc, 3: inc, 4: jmp 0, 5: halt`. The residual program has three functions, one per machine address that a jump can reach, and the loop body `run_1` holds only the register work. A script counts $66a + 14$ calls, primitives and conditionals for the interpreter on input $a$, and $6a + 4$ for the residual program. The residual program is the target of item 1.
- **Generating extensions.** Item 3 says $\mathit{cogen}$ turns any two-input program $p$ into a program that, given $s$, writes $p$ specialized to $s$. Ershov called such a program a generating extension. A parser generator is a generating extension of a general parser, with the grammar as $s$.
- **Run-time compilation.** The [self-optimizing AST interpreter](/self-optimizing-ast-interpreter/) of Truffle is specialized to a hot user function at run time, which is item 1 applied inside a [just-in-time compiler](/just-in-time-compilation/). [Meta-tracing](/meta-tracing/) reaches item 1 by tracing the interpreter instead of specializing it, as a [tracing JIT](/tracing-jit-compilation/) does for user programs.
- **Existence.** The [s-m-n theorem](/s-m-n-theorem/) gives a specializer for any programming language that can compute all computable functions, so the projections hold in every such language. The specializer it gives is the trivial one, so this says nothing about speed.

## Tightness

- **The equations do not force speed.** Let $\mathit{mix}_0(p, s)$ return the text of the program `fun d -> p(s, d)`, with $p$ and $s$ written in as constants. It satisfies the mix equation, so all three items hold for it. Its target is the interpreter with the source program stored in it, and its compiler only stores the interpreter. The quality of the projections comes from the specializer, not from the theorem. A common measure is *Jones optimality*: for a self-interpreter $\mathit{sint}$ of $L$, the program $[\![\mathit{mix}]\!](\mathit{sint}, p)$ should be at least as fast as $p$ on every input. The trivial specializer fails this by the whole cost of interpretation.
- **Self-application needs $\mathit{mix}$ in $L$ and on $L$.** Items 2 and 3 apply $\mathit{mix}$ to itself. A specializer written in another language, or one that accepts only a subset of $L$ that does not contain its own text, gives item 1 and no more.
- **An online specializer self-applies badly.** In item 2, $\mathit{mix}$ is specialized with $p = \mathit{int}$ static and $s = \mathit{src}$ dynamic. An online specializer decides at each step whether a value is static by looking at it. When $\mathit{mix}$ itself runs on $(\mathit{int}, \mathit{src})$, those values come from $\mathit{src}$, which is dynamic. So the decisions cannot be made while $\mathit{comp}$ is generated, and they stay in $\mathit{comp}$ as run-time tests: the compiler is large and slow. Jones, Sestoft and Søndergaard found this in 1985. Their fix, now standard, is an *offline* specializer: a [binding-time analysis](/binding-time-analysis/) marks the program from the split of its inputs before specialization, and the specializer only follows the marks. The marks depend on $p$ and not on $s$, so in item 2 they are static, and the generated compiler contains no binding-time tests.
- **Termination.** The theorem is conditional when $\mathit{mix}$ can fail to stop. A specializer that stops on $(\mathit{int}, \mathit{src})$ for every $\mathit{src}$ may still loop when it is applied to itself, because $\mathit{mix}$ has its own static loops over the text of $p$.
- **Encoding.** The inputs and outputs of $\mathit{mix}$ are program texts. In a typed language, programs must be values of one data type, so a typed interpreter has to encode the values of $S$ in one universal type, and the target of item 1 keeps the tags of that encoding unless the specializer removes them.

## History

Futamura described the projections in 1971, and the paper was reprinted in 1999. Turchin and Ershov worked on the same ideas in the Soviet Union, and Ershov used the term generating extension. The first compiler and compiler generator made by self-application on a computer came from Jones, Sestoft and Søndergaard in 1985, with a specializer for first-order recursion equations whose annotations were computed before specialization. This was the start of binding-time analysis. The book of Jones, Gomard and Sestoft (1993) gives the projections for several languages. Truffle and Graal made the first projection the basis of production language runtimes.

## References
