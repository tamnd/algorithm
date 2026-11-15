---
tag: 7Z715T
kind: concept
slug: just-in-time-compilation
name: Just-in-time compilation
aliases:
- JIT compilation
- dynamic compilation
area: compilers-and-program-analysis/code-generation-and-jit
level: intro
summary: Compiles code while the program runs, so the compiler can use the actual types, values and profile seen so far.
prereqs: [three-address-code, activation-record]
see_also: [adaptive-optimization, tracing-jit-compilation, copy-and-patch-compilation, inline-caching, deoptimization, threaded-code, profile-guided-optimization, ski-rental-problem]
sources:
  - paper: doi:10.1145/857076.857077
    title: John Aycock, A brief history of just-in-time, ACM Computing Surveys 35(2), 2003, 97-113
    locator: the definition of JIT compilation as any translation done after the program starts, the survey of systems from 1960 to 2000, and the classification of JIT systems
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 14 (Runtime Optimization), Section 14.2 on the execution model, compilation triggers and granularity, and Section 14.5 on levels, on-stack replacement and code cache management
  - paper: doi:10.1145/800017.800542
    title: L. Peter Deutsch and Allan M. Schiffman, Efficient implementation of the Smalltalk-80 system, POPL 1984, 297-302
    locator: dynamic translation of bytecode methods to native code on first use, the bounded code cache, and the inline cache
  - paper: doi:10.1109/JPROC.2004.840305
    title: Matthew Arnold, Stephen J. Fink, David Grove, Michael Hind and Peter F. Sweeney, A survey of adaptive optimization in virtual machines, Proceedings of the IEEE 93(2), 2005, 449-466
    locator: the survey of selective optimization, profiling and feedback-directed optimization in virtual machines
  - paper: "Urs Hölzle, Adaptive optimization for SELF: reconciling high performance with exploratory programming, PhD thesis, Stanford University, 1994 (report STAN-CS-TR-94-1520)"
    locator: Section 5.2 (adaptive recompilation) and Section 5.3 (invocation counters with exponential decay)
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Regular expression search algorithm, Communications of the ACM 11(6), 1968, 419-422
    locator: the compilation of a regular expression to IBM 7094 machine code at search time
---

Just-in-time (JIT) compilation is the translation of program code into machine code while the program runs, after it has started. A JIT system usually starts the program in an interpreter, finds the parts that run often, and compiles only those parts, at the moment they are needed. Because it compiles late, the compiler can use facts that a compiler before the run does not have: the types and values that actually occur, the paths that are actually taken, and the exact processor. This page gives the general idea. [Adaptive optimization](/adaptive-optimization/) decides when to compile and at which level, [tracing JIT compilation](/tracing-jit-compilation/) and [meta-tracing](/meta-tracing/) compile hot paths instead of whole methods, a [self-optimizing AST interpreter](/self-optimizing-ast-interpreter/) gets its compiler from the interpreter by partial evaluation, and [copy-and-patch compilation](/copy-and-patch-compilation/) is a fast way to emit the machine code.

## In plain words

A program can run in two ways. An interpreter reads the program one step at a time and does what each step says. It starts at once, but each step costs extra work for the reading. A compiler first translates the whole program to machine code. That takes time before the start, but then each step is fast.

A just-in-time compiler mixes the two. The program starts in the interpreter, and the system counts how often each part runs. When a part has run many times, the system translates that part to machine code and uses the fast code from then on. Parts that run only once are never compiled, so no time is lost on them. Because the program is already running, the compiler can also see what the program really does, and make code that is fast for that case.

## The idea

### The parts of a JIT system

An *interpreter* is a program that runs another program from a data representation of it, such as an [abstract syntax tree](/abstract-syntax-tree/) or *bytecode*, a compact list of virtual instructions (see [threaded code](/threaded-code/) for the ways to dispatch them). The interpreter keeps the state of the running program in its own data: one frame for each active call, as in an [activation record](/activation-record/), with the local variables and a virtual program counter that names the next instruction. A JIT system adds these parts to the interpreter:

- a *profiler*: counters at method entries and at loop back edges, samples of the program counter, and the receiver types that [inline caches](/inline-caching/) record;
- one or more compilers, from a fast baseline compiler to a slow optimizing one;
- a *code cache*: a map from each compiled unit to its machine code and its entry points;
- the glue between the two worlds: entry from the interpreter into compiled code, exit from compiled code back to the interpreter ([deoptimization](/deoptimization/)), and the switch of a loop that is already running to new code ([on-stack replacement](/on-stack-replacement/)).

The *unit* of compilation can be a method, a loop, a straight path through the code called a *trace*, or a region of basic blocks. The rest of this section uses methods, but the same ideas hold for the other units.

### The life of a unit

Each unit is in one state at a time. The system moves it between the states on these events:

| state | event | next state |
|---|---|---|
| interpreted | its counter reaches the threshold | queued for compilation |
| queued | the compiler finishes | compiled at level $i$ |
| compiled at level $i$ | its counter at this level reaches the next threshold | queued for level $i + 1$ |
| compiled | an assumption of the code fails | interpreted (the code is invalid) |
| compiled | the code cache is full and the unit is evicted | interpreted |

A call then goes through a small dispatch step:

```
CALL(u, args)
L1  if the code cache has code for u then return RUN(code[u], args)
L2  count[u] ← count[u] + 1
L3  if count[u] ≥ threshold then put u on the compile queue
L4  return INTERPRET(u, args)
```

Line L3 only queues the unit. Many systems compile on a background thread and keep interpreting until the code is ready, so the program does not stop for the compiler. The next call after the code is installed takes line L1.

### What the compiled code must do

Write $I(u, \sigma)$ for the outcome of interpreting unit $u$ from the interpreter state $\sigma$: a returned value with the final heap, an error, or no end. Compiled code $K$ for $u$ is correct when, for each state $\sigma$ from which $u$ can be entered, running $K$ from the machine state that encodes $\sigma$ has the outcome $I(u, \sigma)$. Two features make this harder than in a compiler that runs before the program.

- **Speculation.** Optimized code often holds *guards*: tests of an assumption, such as "this value is a small integer" or "the receiver has the shape seen before". The code needs to be correct only on the states that pass its guards. A failing guard is an *exit point*, and at each exit point $p$ the compiler records a map $\delta_p$ from the machine state to interpreter frames. The invariant is: if the run of $K$ from the encoding of $\sigma$ reaches $p$ in machine state $s$, then interpreting $u$ from $\sigma$ reaches the program point of $p$ in the state $\delta_p(s)$. Then the interpreter can go on from $\delta_p(s)$ and give the outcome $I(u, \sigma)$. This is the contract of [deoptimization](/deoptimization/), and [on-stack replacement](/on-stack-replacement/) needs the same map in the other direction.
- **Facts about the whole program that can change.** A JIT compiler can use a fact such as "class C has no subclass yet" from [class hierarchy analysis](/class-hierarchy-analysis/) to [devirtualize](/devirtualization/) a call. When a new class is loaded, the fact becomes false, and the system must invalidate each piece of code that depends on it before that code runs again. So the system keeps a list of dependencies from facts to code.

### What a JIT compiler knows

A compiler that runs before the program must make code that is correct and reasonably fast for each possible input. A JIT compiler sees one run. It can use:

- the *types* that occur, from inline caches and [type feedback](/type-feedback/);
- *values* that do not change in this run, such as a configuration flag, a regular expression, or the loaded class hierarchy;
- the *paths* that are taken, for block layout and for [function inlining](/function-inlining/) decisions. [Profile-guided optimization](/profile-guided-optimization/) uses the same kind of profile, but from a separate training run;
- the exact *processor*, so it can use its vector instructions.

The price is that compile time is now part of the run time. A JIT compiler must be fast, it uses memory for the code cache, and the program is slow while it warms up. It also needs memory that it can write and then execute. Many systems keep each page either writable or executable, never both at the same time, and switch a page when they install code.

### When to compile, as a rent-or-buy problem

Take one unit that will run $n$ times, where $n$ is not known in advance. One run costs $a$ in the interpreter and $b < a$ in compiled code, and the compilation costs $C$ once. If $n$ were known, the best cost would be

$$\mathrm{OPT}(n) = \min(n a,\; C + n b).$$

The *break-even rule* interprets the first $k = \lceil C/(a - b) \rceil$ runs and compiles before run $k + 1$. Its cost is $\mathrm{ALG}(n) = na$ for $n \le k$, and $ka + C + (n - k) b$ for $n > k$.

**Claim.** For each $n \ge 0$, $\mathrm{ALG}(n) < 2\,\mathrm{OPT}(n) + (a - b)$.

*Proof.* Let $d = a - b > 0$. By the choice of $k$, $C \le kd < C + d$. Case $n \le k$: if $\mathrm{OPT}(n) = na$, then $\mathrm{ALG}(n) = \mathrm{OPT}(n)$. Otherwise $\mathrm{OPT}(n) = C + nb$, and $\mathrm{ALG}(n) = nb + nd \le nb + kd < nb + C + d = \mathrm{OPT}(n) + d$. Case $n > k$: then $nd > kd \ge C$, so $\mathrm{OPT}(n) = C + nb$. And $\mathrm{ALG}(n) = C + nb + kd < 2C + nb + d \le 2\,\mathrm{OPT}(n) + d$. $\square$

This is the [ski rental problem](/ski-rental-problem/), with the saving $a - b$ per run in place of the rent and $C$ in place of the price. No rule that does not know $n$ can do better than a ratio of about 2 in the worst case, by the lower bound for ski rental. Real systems do not know $a$, $b$ and $C$ exactly, so their thresholds are tuned by hand. The SELF system also let its counters decay over time, so that a high rate of calls, not a high total, triggers a compilation (Hölzle 1994, Section 5.3). The model is a guide to the shape of the rule. It says nothing about the speed of a real system.

## Examples

### Break-even numbers

Take $a = 10$, $b = 1$ and $C = 500$. Then $k = \lceil 500/9 \rceil = 56$.

| runs $n$ | cost of the break-even rule | best cost | ratio |
|---|---|---|---|
| 10 | 100 | 100 | 1.000 |
| 56 | 560 | 556 | 1.007 |
| 57 | 1061 | 557 | 1.905 |
| 100 | 1104 | 600 | 1.840 |
| 1000 | 2004 | 1500 | 1.336 |

The worst case is $n = k + 1$: the rule pays for 56 interpreted runs and for the compilation, and then the unit runs only once more. The bound of the claim is $2 \cdot 557 + 9 = 1123$ there. For large $n$ the ratio goes to 1, because the cost of the compilation and of the first runs is spread over many runs.

### Specializing on the types seen at run time

In a dynamic language, the function `add(x, y) = x + y` must work for integers, floating-point numbers and strings. The interpreter tests the types of both operands on every call. Suppose that the first 1000 calls all have small integers. A JIT compiler can emit this code:

```
add_compiled(x, y):
  guard x is a small integer    else exit to the interpreter at add, pc 0, with x and y
  guard y is a small integer    else exit to the interpreter at add, pc 0, with x and y
  r = x + y
  guard r did not overflow      else exit to the interpreter at add, pc 0, with x and y
  return r
```

Call 1001 is `add("ab", "c")`. The first guard fails. The exit builds an interpreter frame for `add` at the start, with `x = "ab"` and `y = "c"`, and the interpreter returns `"abc"`. The program cannot tell that compiled code was ever involved. That is the invariant of the section above, at an exit point where no work was done yet.

### Thompson's regular expression compiler

In 1968, Thompson's search program compiled a regular expression into IBM 7094 machine code at the time of the search, and then ran that code on the text. The code simulates the nondeterministic automaton of the expression, which is the [Thompson construction](/thompson-construction/). Aycock lists it among the early JIT systems. The input to the compiler, the [regular expression](/regular-expression/), is known only when the program runs, so compilation must happen at run time.

### Smalltalk-80 by Deutsch and Schiffman

Deutsch and Schiffman's Smalltalk-80 system of 1984 translated the bytecode of a method into native code the first time it ran, and kept the native code in a cache of fixed size. When the cache was full, it dropped code, and translated a method again when it was needed. So the native code was a cache of the bytecode, not a replacement for it. The same system introduced [inline caching](/inline-caching/) for message sends.

## Where it is used

- **Java virtual machines.** They start with an interpreter or a baseline compiler and recompile hot methods with optimizing compilers, which is [adaptive optimization](/adaptive-optimization/). Arnold and others survey these systems.
- **JavaScript engines.** They have several tiers, from an interpreter to an optimizing compiler, and depend on [inline caches](/inline-caching/), [hidden classes](/hidden-classes/), [type feedback](/type-feedback/) and [deoptimization](/deoptimization/).
- **Dynamic language runtimes.** PyPy gets a tracing JIT compiler from an interpreter by [meta-tracing](/meta-tracing/). The Truffle framework uses a [self-optimizing AST interpreter](/self-optimizing-ast-interpreter/) and partial evaluation. CPython 3.13 added an experimental JIT compiler that uses [copy-and-patch compilation](/copy-and-patch-compilation/).
- **Binary translation and dynamic optimization.** A system such as Dynamo reads machine code, finds hot paths, and writes optimized copies of them into a code cache, which is [tracing JIT compilation](/tracing-jit-compilation/) without a source language.
- **Small languages inside large programs.** Regular expression engines, database query engines, packet filters in operating system kernels and graphics shaders are often compiled at run time, because the program text arrives at run time.

## References
