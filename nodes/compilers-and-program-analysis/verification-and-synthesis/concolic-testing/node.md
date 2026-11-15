---
tag: C4AWCW
kind: algorithm
slug: concolic-testing
name: Concolic testing
aliases:
- dynamic symbolic execution
- DART
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Runs the program on concrete input while recording the symbolic path condition, then negates a branch and solves for input to a new path.
model: word-ram
complexity:
  vars: {R: the number of feasible paths explored, m: the largest number of recorded conditions on one run, T: the largest number of steps of one run, C: the cost of one solver call}
  time: {worst: O(R (T + m C))}
  space: {extra: O(T)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2005
  people: [Patrice Godefroid, Nils Klarlund, Koushik Sen]
  note: DART (PLDI 2005) introduced directed automated random testing; CUTE (ESEC/FSE 2005) by Koushik Sen, Darko Marinov and Gul Agha named the method concolic testing.
prereqs: [path-condition, symbolic-execution]
see_also: [symbolic-execution-tree, generational-search, path-explosion-problem, coverage-guided-fuzzing, smt-problem, incremental-solving, depth-first-search, differential-testing]
sources:
  - paper: doi:10.1145/1065010.1065036
    title: Patrice Godefroid, Nils Klarlund and Koushik Sen, DART, directed automated random testing, Proceedings of PLDI 2005
    locator: pp. 213 to 223, the sections on the execution model, the stack of branch records and the search for a new input (solve_path_constraint)
  - paper: doi:10.1145/1081706.1081750
    title: Koushik Sen, Darko Marinov and Gul Agha, CUTE, a concolic unit testing engine for C, Proceedings of ESEC/FSE 2005
    locator: pp. 263 to 272, the sections on concolic execution, the approximation of pointer constraints and the depth-first search
  - paper: doi:10.1145/2408776.2408795
    title: Cristian Cadar and Koushik Sen, Symbolic execution for software testing, three decades later, Communications of the ACM 56(2), 2013
    locator: pp. 82 to 90, the section on concolic testing and the use of concrete values
  - paper: doi:10.1145/3182657
    title: Roberto Baldoni, Emilio Coppa, Daniele Cono D'Elia, Camil Demetrescu and Irene Finocchi, A survey of symbolic execution techniques, ACM Computing Surveys 51(3), 2018
    locator: Article 50, the section on concolic execution and concretization
---

Concolic testing runs the program on a concrete input and, at the same time, keeps a symbolic expression for each value, so that each run gives its own [path condition](/path-condition/). It then negates one condition of that path, asks a solver for an input that satisfies the new formula, and runs the program on that input. The name joins "concrete" and "symbolic". The concrete run decides the path, so the tool never forks states, and when an operation is too hard for the solver it can use the concrete value in its place. This page gives the depth-first search of DART, which explores the [symbolic execution tree](/symbolic-execution-tree/) one run at a time. The method that it implements is [symbolic execution](/symbolic-execution/); [generational search](/generational-search/) is a different order over the same runs.

## In plain words

Run the program once on any input, for example all zeros. While it runs, write down every test it passes and which way each test went, in terms of the inputs: "y times 2 was equal to x", "y plus 3 was not less than x". Now take the last test on that list and ask: is there an input that goes the same way at every earlier test but the other way at this one? A solver finds such an input, or says there is none. Run the program on the new input, write down its list, and repeat, always flipping the deepest test that has not been flipped yet. Each new input goes down a new way through the program. Inputs that random testing would almost never hit, such as "x is exactly twice y", come out of the solver at once.

## The problem

The input is a program $P$ of the toy IR with $k$ integer parameters, a set $D \subseteq \mathbb{Z}^k$ of allowed inputs, and a solver for the conditions of the program. The output is a list of tests, one input for each path of $P$ that some input of $D$ follows, where a path is the sequence of blocks together with the outcome (a return or a trap at a given instruction).

The goal "a test for every feasible path" cannot be met in general. The number of paths can be infinite (see [path explosion](/path-explosion-problem/)), and over unbounded integers with products of inputs, the feasibility of one path condition is undecidable by [Hilbert's tenth problem](/hilberts-tenth-problem/). The algorithm is complete relative to its solver: if the solver is exact over $D$, it finds every path that an input of $D$ follows, and it stops when $D$ is finite. On this page $D$ is the box $[-8, 8]^k$, and the solver tries every point of the box, in place of an SMT solver. A real tool uses an [SMT](/smt-problem/) solver for bit vectors, which is a decision procedure for machine integers.

## The algorithm

**The concolic run.** RUN executes $P$ on the input $v$ and keeps two stores: the concrete values and the symbolic expressions over the input symbols $\alpha_1, \dots, \alpha_k$. An operation on two constants is folded to a constant. Each run records a list of *conditions*. A condition is a pair $(e, s)$: the run went the way on which "$e \ne 0$" has the truth value $s$.

- At `br a L1 L2`, the run records $(\sigma(a), s)$, where $s$ tells whether it went to $L_1$.
- At a division or a remainder by $b$, the run records $(\sigma(b), s)$, where $s$ tells whether $b \ne 0$. At a shift by $b$, it records the condition $0 \le \sigma(b) \le 63$. If the check fails, the run stops with a trap. These are the implicit conditions of the [path condition](/path-condition/) page.
- A condition whose expression is a constant is not recorded: no input can change it.

The conditions $c_1, \dots, c_m$ of a run, joined by "and", are its path condition. Write $\neg(e, s)$ for $(e, \neg s)$.

**The search.** $S$ is a stack of pairs (condition, done). Entry $i$ of the stack is the $i$-th condition of the current path. The flag *done* says that the other side of that condition has been dealt with.

```pseudo id=main
CONCOLIC(P, SOLVE)
L1  v <- any input, for example all zeros
L2  S <- an empty stack of pairs (condition, done)
L3  loop
L4      (outcome, c_1 ... c_m) <- RUN(P, v)
L5      for i <- |S| + 1 to m do push (c_i, false) on S
L6      output the test (v, outcome)
L7      repeat
L8          if S is empty then return
L9          (c, done) <- the top of S; let d_1 ... d_(j-1) be the conditions below it
L10         if done then pop S and continue
L11         v' <- SOLVE(d_1 and ... and d_(j-1) and not c)
L12         if there is no v' then pop S and continue
L13         replace the top of S by (not c, true); v <- v'; leave the repeat
```

Line L5 keeps the entries that the stack already holds. The new input satisfies the conditions of the stack, so its run agrees with them, and only its later conditions are new. The implementation checks this agreement and reports a *divergence* if it fails; with exact symbolic tracking it never fails. Lines L8 to L13 find the deepest condition whose other side is still open, exactly as a [depth-first search](/depth-first-search/) backtracks. A flipped entry is marked done at once: the side that the earlier run took is finished, and the new run explores the other.

Each query on line L11 is the previous path condition with its last condition negated. A solver with [incremental solving](/incremental-solving/) keeps the shared prefix between calls.

## Example

The parameters are $x$ and $y$, with the symbols $\alpha$ and $\beta$. The return of 1 stands for a bug.

```
entry:
  z = y * 2
  t = z == x
  br t then miss
then:
  w = y + 3
  u = w < x
  br u bug near
miss:
  ret 0
bug:
  ret 1
near:
  ret 2
```

The solver tries the points of $[-8, 8]^2$ in lexicographic order of $(x, y)$.

| run | input | conditions recorded | outcome | stack after the search step |
|---|---|---|---|---|
| 1 | (0, 0) | $(2\beta = \alpha, \text{true})$, $(\beta + 3 < \alpha, \text{false})$ | ret 2 | $(2\beta = \alpha, \text{false})$, $(\beta + 3 < \alpha, \text{true})$ |
| 2 | (8, 4) | the same two, the second one true | ret 1 | $(2\beta = \alpha, \text{false})$, flipped and done |
| 3 | (-8, -8) | $(2\beta = \alpha, \text{false})$ | ret 0 | empty |

After run 1, the top entry is not done, so line L11 asks for $2\beta = \alpha \wedge \beta + 3 < \alpha$. This means $\beta > 3$ and $\alpha = 2\beta \le 8$, so the only model in the box is $(8, 4)$, and run 2 reaches the bug. After run 2, the top entry is done and is popped. The next entry asks for $2\beta \ne \alpha$, and the first point of the box, $(-8, -8)$, satisfies it. After run 3, the stack holds only done entries, and the search ends.

Three runs and two solver calls find all three paths. Of the 289 inputs of the box, 280 return 0, 8 return 2 and only one returns 1. Over pairs of 32-bit integers, a random input satisfies $x = 2y$ with probability about $2^{-32}$, so random testing almost never reaches `then`.

## Correctness

The full proof is in the proof file. The claim is: if SOLVE is exact over a finite set $D$ (it returns a model in $D$ whenever one exists) and the start input is in $D$, the search stops, and it outputs one test for each path that some input of $D$ follows, each path exactly once.

1. **The record is a function of the path so far.** By induction along a run, the symbolic store after a sequence of decisions does not depend on the input. So the next recorded condition, or the end of the run, is fixed by the earlier decisions. The sequences of senses of the runs on $D$ form the leaves of a binary tree $T_D$, the symbolic execution tree cut down to $D$.
2. **No divergence.** The input from line L11 satisfies all the conditions of the stack, so its run makes the same decisions, and line L5 keeps the stack.
3. **The invariant.** At line L8, the tests output so far are exactly the leaves below the other side of each done entry, together with all the leaves below the current stack. At line L3 (after line L13), they are exactly the leaves below the other side of each done entry. Popping a done entry, popping an entry whose other side is empty (the solver says so, and it is exact), and flipping an entry all keep this.
4. **The end.** When the stack is empty, the invariant says that every leaf of $T_D$ has been output. Each run outputs a leaf that is new, by the invariant, and $T_D$ has at most $|D|$ leaves, so the loop stops. The successful solver calls are one fewer than the runs.

With an exact solver over all of $\mathbb{Z}^k$ the same argument shows that no path is output twice. If the tree is infinite, the search may never stop, and a depth-first search may stay in one infinite branch.

## Complexity

Let $R$ be the number of paths explored, $m$ the largest number of conditions on one run, $T$ the largest number of steps of a run and $C$ the cost of one solver call. Each run costs $O(T)$, since each step adds at most one node to an expression. Each stack entry is pushed once and causes at most one solver call, so there are at most $R m$ calls, and exactly $R - 1$ of them succeed. The total is $O(R (T + m C))$. The stack and the expressions take $O(T)$ space, because shared subterms are stored once.

The cost $C$ dominates in practice. The brute-force solver of this page costs $|D|$ evaluations of a formula of size $O(T)$. An SMT solver for bit vectors solves an NP-complete problem in each call, see [bit-vector satisfiability](/bit-vector-satisfiability/). $R$ can be exponential in the number of branches.

## Properties

- **No false alarms.** Every test is a real run of the program, so every failure it reports is real. This holds even when the symbolic part is wrong or incomplete; a wrong symbolic part only makes the search miss paths or diverge.
- **Complete relative to the solver.** With an exact solver and exact tracking, every feasible path is found once and only once. With an incomplete solver or with concretization, some paths are missed, and the method gives no guarantee about them.
- **Concrete values help the solver.** When a condition contains an operation that the solver does not handle, such as a nonlinear product or a [hash function](/hash-function/), the tool can replace that subterm by its value in the current run. The query then stays solvable, at the price of completeness.
- **Depth-first and anytime.** Each run gives a test, so the tool can stop at any time and keep what it has. The stack has at most $m$ entries.

## Variants and improvements

- **CUTE.** Sen, Marinov and Agha extend the method to C programs with pointers and dynamic data. They keep a logical input map, approximate constraints on pointers by equalities and disequalities, and named the method concolic.
- **Concretization.** DART falls back to the concrete value when a condition leaves the theory of the solver, for example a product of two inputs with a linear solver. CUTE does the same. If the fall-back makes a run leave the predicted prefix, DART detects it and starts again from a random input.
- **Bounded depth.** A depth bound on the stack makes the search stop on programs with an infinite tree. The paths below the bound are lost.
- **Generational search.** [Generational search](/generational-search/) negates every condition of a run at once, and picks the next run by the new coverage it gives. It suits long runs with thousands of conditions, where depth-first search spends its budget in one corner of the tree.
- **Hybrid fuzzing.** A [coverage-guided fuzzer](/coverage-guided-fuzzing/) finds most easy paths quickly. A concolic engine is called on the inputs of the fuzzer when coverage stops growing, to solve the narrow conditions such as "x is twice y".
- **Pure symbolic execution with concrete help.** EXE and KLEE fork symbolic states at each feasible branch and keep many states in memory at once, instead of rerunning the program. They use concrete values for the operations that have no symbolic input.

## When to use it

Use concolic testing to generate tests for programs with narrow conditions that random inputs do not hit: parsers with magic numbers, checksums, arithmetic relations between inputs. It needs a way to observe the program as it runs, such as instrumentation of the code. Prefer pure [symbolic execution](/symbolic-execution/) when the program state is small and forking is cheap, and a fuzzer when the conditions are wide and runs are cheap. For proofs of absence of bugs, use a verifier: a concolic tool proves nothing about the paths that it does not reach.

## Pitfalls

- **Leaving out the implicit conditions.** If the run does not record $b \ne 0$ at a division, the search never generates the input that traps there, and a solver may give a model in which the division by zero has an arbitrary value. See the [path condition](/path-condition/) page.
- **A mismatch of semantics.** The solver must use the same arithmetic as the program. Unbounded integers in the solver and 32-bit words in the program give models that take a different path on the machine, because of [integer overflow](/integer-overflow/). Toy IR division truncates toward zero, so the solver must too.
- **Divergence.** Concretization, calls to code that is not instrumented, and nondeterminism such as time or threads make a run leave the predicted prefix. A tool that does not detect this explores the same path twice or marks a side as done that it never saw.
- **Recording constant conditions.** A branch on a value that does not depend on the input gives a condition with no symbols. Negating it always fails, so RUN does not record such conditions.
- **Expecting termination.** A loop whose trip count is an input gives an infinite tree, and the search follows it forever. On the box of this page, the counted loop `while i < n` gives one run for each $n$ from 0 to 8, and then the solver finds no $n > 8$ in the box.

## Implementations

## History

Godefroid, Klarlund and Sen presented DART at PLDI 2005. It combined random testing of the interface of a C program with a dynamic analysis that records the path condition of each run and directs the next run to a new path. In the same year Sen, Marinov and Agha presented CUTE at ESEC/FSE, which handles pointer inputs and named the method concolic testing. The idea of symbolic execution goes back to King in 1976. Concolic testing made it practical for large programs, because concrete values handle what the solver cannot. Later tools built on it: SAGE at Microsoft with [generational search](/generational-search/), and hybrid fuzzers that pair a concolic engine with a greybox fuzzer.

## References
