---
tag: GRCVMW
kind: technique
slug: partial-evaluation
name: Partial evaluation
aliases:
- program specialization
- mixed computation
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Specializes a program to the part of its input known in advance, giving a residual program that takes only the rest of the input.
prereqs: [constant-folding, function-inlining]
see_also: [binding-time-analysis, futamura-projections, supercompilation, deforestation, self-optimizing-ast-interpreter, meta-tracing, s-m-n-theorem, just-in-time-compilation]
sources:
  - book: isbn:9780130202499
    title: Neil D. Jones, Carsten K. Gomard and Peter Sestoft, Partial Evaluation and Automatic Program Generation, Prentice Hall, 1993
    locator: the mix equation, online and offline specialization, polyvariant specialization of program points, unfolding and termination, and the specialization of interpreters
  - paper: doi:10.1145/243439.243447
    title: Neil D. Jones, An introduction to partial evaluation, ACM Computing Surveys 28(3), 1996, 480-503
    locator: the definition of a specializer by the mix equation, the power and interpreter examples, and the problems of termination and code growth
  - paper: doi:10.1016/0304-3975(82)90111-6
    title: "Andrei P. Ershov, Mixed computation: potential applications and problems for study, Theoretical Computer Science 18(1), 1982, 41-67"
    locator: mixed computation, the program that does the known part of a computation and emits the rest
  - paper: doi:10.1023/A:1010095604496
    title: "Yoshihiko Futamura, Partial evaluation of computation process, an approach to a compiler-compiler, Higher-Order and Symbolic Computation 12(4), 1999, 381-391"
    locator: the reprint of the 1971 paper that specializes an interpreter to a program and names the projections
  - paper: doi:10.1007/3-540-15976-2_6
    title: "Neil D. Jones, Peter Sestoft and Harald Søndergaard, An experiment in partial evaluation: the generation of a compiler generator, Rewriting Techniques and Applications (RTA 1985), LNCS 202, 124-140"
    locator: the first self-applicable specializer, for first-order recursion equations, with memoization of specialized program points
  - paper: doi:10.1016/0020-0190(89)90113-0
    title: Charles Consel and Olivier Danvy, Partial evaluation of pattern matching in strings, Information Processing Letters 30(2), 1989, 79-86
    locator: a naive string matcher, rewritten so the matched prefix is static, specialized to a pattern into a matcher of Knuth-Morris-Pratt quality
  - paper: doi:10.1145/3062341.3062381
    title: Thomas Würthinger and others (9 authors), Practical partial evaluation for high-performance dynamic language runtimes, PLDI 2017, 662-676
    locator: partial evaluation of AST interpreters at run time in Truffle and Graal, with deoptimization when a speculation fails
---

Partial evaluation takes a program $p$ and the values $s$ of some of its inputs, the *static* inputs, and makes a new program $p_s$, the *residual program*, that takes only the other inputs, the *dynamic* inputs $d$, and gives the same result as $p$ on $(s, d)$. The program that does this is a *specializer*, often called $\mathit{mix}$. In the notation $[\![q]\!]$ for the function that a program $q$ computes, it must satisfy the *mix equation* $[\![\,[\![\mathit{mix}]\!](p, s)\,]\!](d) = [\![p]\!](s, d)$. The residual program does every computation that depends only on $s$ ahead of time and keeps only the work that needs $d$. Ershov called this mixed computation, Futamura used it in 1971 to turn interpreters into compilers, and Jones, Sestoft and Søndergaard built the first self-applicable specializer in 1985. The common mistake is to think a specializer always stops. It does not: unfolding a recursion whose stop test is dynamic, or making one version for each of infinitely many static values, runs forever.

## In plain words

Some inputs of a program are known long before the others. A program that draws a picture gets its settings once and its pixels millions of times. An interpreter gets the user's program once and its data many times.

A partial evaluator reads the program and the known inputs. It does all the work that needs only the known inputs, and writes down the rest as a new, smaller program. The new program asks only for the unknown inputs and gives the same answers as the old program.

If the known input is an exponent of 3, a general power function becomes "x times x times x". If the known input is a program for an interpreter, the interpreter becomes a translation of that program. The new program skips the tests and lookups that were decided ahead of time.

## When it applies

- The input splits into a part that is fixed for many runs and a part that changes between runs, and the program does real work that depends on the fixed part alone: decoding a format, walking a configuration, interpreting a program, testing a pattern.
- The program can be read as data, in a language for which a specializer exists. The cleanest case is a first-order or higher-order functional language without side effects, which this page uses. Specializers also exist for C, Scheme and Prolog, and run-time specializers such as Truffle work inside language virtual machines.
- The residual program runs often enough to pay for the time of specialization. A program that runs once on its static input gains nothing.

## The template

**Language.** A program is a list of first-order recursion equations $f(x_1, \ldots, x_n) = e$. An expression is a constant, a variable, a primitive $e_1 \mathbin{op} e_2$, a conditional $\mathtt{if}\ e_0\ \mathtt{then}\ e_1\ \mathtt{else}\ e_2$, a call $g(e_1, \ldots, e_n)$ or $\mathtt{let}\ x = e_1\ \mathtt{in}\ e_2$. Evaluation is call by value. The outcome of a run is a value, an error (such as division by 0), or no end. The higher-order case, with `fun x -> e`, needs a [binding-time analysis](/binding-time-analysis/) to be done well and is treated there.

**Specialization values.** During specialization each expression gets a *specialization value*: either $S(v)$, a value known now, or $D(r)$, a piece of residual code $r$ that computes the value later. A static environment $\rho$ maps each variable to a specialization value.

**Step 1: the program points.** A residual function is named by a pair $(f, \bar s)$: a function $f$ of the source and the values $\bar s$ of its static parameters. The residual program has one function $f_{\bar s}$ for each pair that is reached, and its parameters are the dynamic parameters of $f$. This is *polyvariant* specialization: one source function can have many residual versions.

**Step 2: the specializer of expressions.** $\mathrm{PE}(e, \rho, \mathit{ctx})$, where $\mathit{ctx}$ says whether $e$ is under a dynamic conditional:

- A constant $k$ gives $S(k)$. A variable $x$ gives $\rho(x)$.
- $e_1 \mathbin{op} e_2$: if both operands give $S(v_1)$ and $S(v_2)$, compute $S(v_1 \mathbin{op} v_2)$ now. Otherwise give $D(r_1 \mathbin{op} r_2)$, where a static operand $S(v)$ becomes the constant $v$ in the code.
- $\mathtt{if}\ e_0 \ldots$: if $e_0$ gives $S(v)$, specialize only the branch that $v$ selects. Otherwise specialize both branches with $\mathit{ctx}$ = dynamic and give $D(\mathtt{if}\ r_0\ \mathtt{then}\ r_1\ \mathtt{else}\ r_2)$.
- $g(e_1, \ldots, e_n)$ outside a dynamic conditional: *unfold* it. Specialize the body of $g$ with the parameters bound to the specialization values of the arguments. A dynamic argument that is not a variable is first bound by a residual $\mathtt{let}$ to a fresh variable (*let insertion*), so it is computed once and in the right order.
- $g(e_1, \ldots, e_n)$ under a dynamic conditional: *residualize* it. Let $\bar s$ be the values of the static arguments. Give $D(g_{\bar s}(r_{i_1}, \ldots, r_{i_m}))$ with the dynamic arguments, and add $(g, \bar s)$ to the pending list if it is new.

**Step 3: the main loop.** Start with the pending list $[(f_0, \bar s_0)]$ for the entry function and the static input. Take a pending pair $(f, \bar s)$ that has no residual function yet, and define $f_{\bar s}(\bar x_D) = r$, where $D(r)$ or $S(v)$ is $\mathrm{PE}$ of the body of $f$ with the static parameters bound to $S(\bar s)$ and the dynamic ones to $D$ of their own names. Repeat until no pair is pending. The memo table of pairs is what turns a loop of the source into a loop of the residual program.

The rule "unfold outside dynamic conditionals, memoize under them" is the classic one. A recursion that is controlled by static data, like the exponent of a power function, unfolds completely. A call under a dynamic test may be the back edge of a loop that runs a dynamic number of times, so it becomes a residual call.

**Legality.** The specializer may stop with a residual program, stop with an error (a static primitive failed), or not stop. *Correctness theorem: if it stops with a residual program, then for every dynamic input $d$, the residual program on $d$ and $p$ on $(s, d)$ have the same outcome: the same value, or both no value.*

*Proof.* (a) Each case of Step 2 replaces an expression by one that is equal in the call-by-value semantics, when each residual call $g_{\bar t}(\bar a)$ is read as the call $g(\bar t, \bar a)$. Computing a static primitive is the rule $v_1 \mathbin{op} v_2 = v$. A static test selects its branch by the rule for $\mathtt{if}$ on a value. Unfolding replaces a call by the body with the parameters replaced by the arguments. This is valid in call by value when the arguments are values; static values and variables are values, and let insertion makes every other argument a variable bound by a $\mathtt{let}$ that is evaluated first, as the call would do. So no dynamic computation is lost, copied or moved past another one. (b) Let $F_{f, \bar s}$ be the function $\bar d \mapsto [\![f]\!](\bar s, \bar d)$. By (a), the family of all $F_{f, \bar s}$ satisfies every equation $f_{\bar s}(\bar x) = r$ of the residual program. The meaning of a recursive program is the least solution of its equations, so whenever the residual function $f_{\bar s}$ returns a value on $\bar d$, $F_{f, \bar s}(\bar d)$ is that value. (c) Conversely, suppose $[\![f]\!](\bar s, \bar d)$ returns $v$ after $N$ calls. Run the body $r$ of $f_{\bar s}$ on $\bar d$. By (a), it does the dynamic steps of that run of $f$ in the same order, with the unfolded calls done inline. Each residual call $g_{\bar t}(\bar a)$ that it meets is a call $g(\bar t, \bar a)$ that the run of $f$ makes, with fewer than $N$ calls. By induction on $N$, that residual call returns the same value. So $r$ returns $v$. Parts (b) and (c) give the theorem. $\square$

**Profit.** The cost model is the number of operations that a run executes: calls, primitives and conditionals. A $\mathtt{let}$ from let insertion costs nothing, since it only names a value that a call would pass. Every operation on static values alone is done once, at specialization time, and leaves nothing in the residual program. Every dynamic operation of the source stays, at most once per execution of the source operation, because of let insertion. So the residual program never does more operations than the source on the same input, and it does fewer by the number of static operations of the run. It does not pay when the residual program is much larger than the source (a static loop of a million rounds unfolds into a million operations of code), or when it runs only a few times.

## Classic examples

**Power.** The source is `power(n, x) = if n == 0 then 1 else x * power(n - 1, x)`, with $n = 3$ static and $x$ dynamic. The test `n == 0` is static, so every call unfolds, and the residual program is

```
power_3(x) = x * (x * (x * 1))
```

On $x = 5$, the source makes 4 calls and runs 10 primitive operations and 4 conditionals. The residual program runs 3 multiplications. A constant folder that knows $x \cdot 1 = x$ would remove the last one; partial evaluation alone does not use algebra.

**An interpreter.** The source is an interpreter for a tiny machine with two registers $a$ and $b$. A machine program is a list of instructions: `jz t` jumps to $t$ if $a = 0$, `dec` sets $a = a - 1$, `inc` sets $b = b + 1$, `jmp t` jumps, and `halt` stops with the value of $b$.

```
run(prog, pc, a, b) =
  if op(prog, pc) == "halt" then b
  else if op(prog, pc) == "jz" then
    (if a == 0 then run(prog, arg(prog, pc), a, b) else run(prog, pc + 1, a, b))
  else if op(prog, pc) == "dec" then run(prog, pc + 1, a - 1, b)
  else if op(prog, pc) == "inc" then run(prog, pc + 1, a, b + 1)
  else run(prog, arg(prog, pc), a, b)
```

The machine program is `0: jz 5, 1: dec, 2: inc, 3: inc, 4: jmp 0, 5: halt`, which computes $b = 2a$. Specialize `run` with `prog` and `pc = 0` static and $a$, $b$ dynamic. The decoding tests `op(prog, pc) == ...` are all static. The only dynamic test is `a == 0`, so the calls in its branches are residualized, and the pending pairs are $pc = 0$, then $5$ and $1$. The residual program, as computed by a short script with the specializer of the template, is

```
run_0(a, b) = if a == 0 then run_5(a, b) else run_1(a, b)
run_5(a, b) = b
run_1(a, b) = let a0 = a - 1 in let b1 = b + 1 in let b2 = b1 + 1 in
              if a0 == 0 then run_5(a0, b2) else run_1(a0, b2)
```

Here `run_1` is the loop body of the machine program, compiled. The instruction decoding and the program counter are gone; only the work on the registers is left. The script counts the calls, primitives and conditionals of both programs on $a = 0, 1, 5, 20, 50$. The interpreter executes $66a + 14$ of them, and the residual program $6a + 4$, plus $3a$ lets that only name values. So it is faster by a factor that tends to 11. Both give $b = 2a$ on every input tried. This is the first of the [Futamura projections](/futamura-projections/): specializing an interpreter to a program compiles the program.

**String matching.** Consel and Danvy (1989) specialize a naive matcher, which compares a pattern with a text and restarts one place to the right after a mismatch, to a fixed pattern. After a rewriting of the matcher that keeps the matched prefix of the text static, the residual program never reads a text character twice. It is a matcher of the quality of [Knuth-Morris-Pratt](/knuth-morris-pratt/). Without the rewriting, the residual program is the naive matcher unrolled, which is the usual outcome: what the specializer can find depends on how the source keeps its static data apart.

**Run-time specialization of interpreters.** Truffle and Graal partially evaluate an AST interpreter for a hot user function at run time, with the AST as static input, and compile the residual program (Würthinger and others, 2017). The interpreter nodes rewrite themselves first, as in a [self-optimizing AST interpreter](/self-optimizing-ast-interpreter/), so the AST holds the speculations, and [deoptimization](/deoptimization/) goes back to the interpreter when one fails. This is [just-in-time compilation](/just-in-time-compilation/) by partial evaluation, the method-based counterpart of [meta-tracing](/meta-tracing/) and [tracing JIT compilation](/tracing-jit-compilation/).

## Variations

- **Online and offline.** The template is *online*: it looks at the specialization values as it goes. An *offline* specializer first runs a [binding-time analysis](/binding-time-analysis/) that marks every expression static or dynamic from the split of the inputs alone, and then follows the marks. Offline specializers are simpler and are the ones that can be applied to themselves well; online ones can find more static values.
- **Monovariant and polyvariant.** A monovariant specializer makes one residual version per source function. A polyvariant one makes one per tuple of static values, as in Step 1.
- **Generalization.** To stop the growth of versions, a specializer can forget a static value and treat it as dynamic. Offline specializers do this when the analysis finds a static value that grows under dynamic control.
- **Partially static data.** A pair whose first part is static and second part dynamic, or a list of known length with unknown elements, can be kept split. This needs a richer domain of specialization values.
- **Higher-order and imperative languages.** Specializers for the lambda calculus (Gomard and Jones), Scheme (Similix), C (C-Mix, Tempo) and Prolog (partial deduction) follow the same plan with more cases.
- **Stronger transformers.** [Supercompilation](/supercompilation/) also uses what a dynamic test tells: in the true branch of `if x == 3`, $x$ is 3. [Deforestation](/deforestation/) removes intermediate data structures. Both can do things that a partial evaluator cannot, such as the matcher of Consel and Danvy without the rewriting.
- **Computability.** The [s-m-n theorem](/s-m-n-theorem/) says that a specializer exists for any programming system that can compute all computable functions. It says nothing about speed: the trivial specializer that only wraps $p$ with $s$ as a constant satisfies the mix equation.

## Pitfalls

- **Infinite unfolding.** Unfolding a recursion whose stop test is dynamic does not end. The rule of the template residualizes calls under dynamic tests, but a recursion with no test between the calls, such as `f(x) = f(x + 1)`, still unfolds forever if `x` is static.
- **Infinitely many versions.** For `f(n, d) = if d == 0 then n else f(n + 1, d - 1)` with $n = 0$ static, every residualized call has a new static value, so the pending list never empties: the script stops at its limit of 50 versions, `f_0`, `f_1`, `f_2`, and so on. The fix is to generalize `n` to dynamic, which gives the single function `f(n, d)` back.
- **Errors at specialization time.** An online specializer computes static operations in both branches of a dynamic test. With `g(s, d) = if d == 0 then 0 else 10 / s` and $s = 0$, it fails on `10 / 0`, though the source never divides when $d = 0$. A specializer must either leave a static operation that can fail as residual code or accept that it may stop with an error.
- **Lost or copied dynamic work.** Unfolding by plain substitution can copy a dynamic argument into two places, so it is computed twice, or drop an argument that the body does not use, which removes an error or a loop of the source. Let insertion keeps call by value exact.
- **Code growth.** Each unfolding copies a body, and each new static tuple adds a version. A residual program can be exponentially larger than the source. Real specializers bound unfolding and the number of versions.
- **Hoping for algebra.** Partial evaluation computes with static values. It does not know that `x * 1` is `x` or that the else branch of `if a == 0` has $a \ne 0$. Constant folding after specialization, or a supercompiler, does that.

## Exercises

1. Specialize `power(n, x)` with $x$ static and $n$ dynamic. Which calls are residualized, and what is the residual program?
2. Add an instruction `add2` that sets $b = b + 2$ to the tiny machine, change the machine program to use it, and give the new residual program. How many operations does it execute on input $a$?
3. Show that the pending list in the interpreter example can never hold more pairs than the machine program has instructions. What does this say about termination for every machine program?
4. Give a source program of constant size and a family of static inputs for which the residual program of the template grows exponentially with the size of the static input.
5. Write a version of `f(n, d)` from the pitfalls where the static value grows but the number of versions stays finite. What property of the static values makes the difference?

## References
