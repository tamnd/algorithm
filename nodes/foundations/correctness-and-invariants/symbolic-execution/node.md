---
tag: 9ERWJ0
kind: technique
slug: symbolic-execution
name: Symbolic execution
aliases:
- Symbolic evaluation
area: foundations/correctness-and-invariants
level: advanced
summary: Runs a program on symbolic inputs, collecting path conditions to explore all paths and find violations.
prereqs: [assertion, precondition, postcondition]
see_also: [floyd-inductive-assertions, weakest-precondition, program-verification, abstract-interpretation, sat, constraint-satisfaction-problem]
sources:
  - url: "https://en.wikipedia.org/wiki/Symbolic_execution"
    locator: article Symbolic execution, sections Example, Limitations (path explosion, environment interactions) and History
  - paper: doi:10.1145/2408776.2408795
    title: Cristian Cadar and Koushik Sen, Symbolic execution for software testing, three decades later, Communications of the ACM 56(2), 2013
    locator: pp. 82 to 90 (classical symbolic execution, concolic testing, the main challenges)
  - paper: doi:10.1145/3182657
    title: Roberto Baldoni, Emilio Coppa, Daniele Cono D'Elia, Camil Demetrescu and Irene Finocchi, A survey of symbolic execution techniques, ACM Computing Surveys 51(3), 2018
    locator: Article 50, pp. 1 to 39 (the sections on path selection, state merging, memory models and constraint solving)
  - paper: doi:10.1145/360248.360252
    title: James C. King, Symbolic execution and program testing, Communications of the ACM 19(7), 1976
    locator: pp. 385 to 394, the sections on the execution tree and on the path condition
  - paper: doi:10.1145/800027.808445
    title: Robert S. Boyer, Bernard Elspas and Karl N. Levitt, SELECT, a formal system for testing and debugging programs by symbolic execution, Proceedings of the International Conference on Reliable Software (1975)
    locator: pp. 234 to 245
  - paper: doi:10.1109/TSE.1976.233817
    title: Lori A. Clarke, A system to generate test data and symbolically execute programs, IEEE Transactions on Software Engineering SE-2(3), 1976
    locator: pp. 215 to 222
  - paper: doi:10.1145/1065010.1065036
    title: Patrice Godefroid, Nils Klarlund and Koushik Sen, DART, directed automated random testing, Proceedings of PLDI 2005
    locator: pp. 213 to 223, the sections on directed search and on constraints that the solver cannot decide
  - paper: doi:10.1145/1081706.1081750
    title: Koushik Sen, Darko Marinov and Gul Agha, CUTE, a concolic unit testing engine for C, Proceedings of ESEC/FSE 2005
    locator: pp. 263 to 272
  - url: "https://www.usenix.org/legacy/event/osdi08/tech/full_papers/cadar/cadar.pdf"
    title: Cristian Cadar, Daniel Dunbar and Dawson Engler, KLEE, unassisted and automatic generation of high-coverage tests for complex systems programs, Proceedings of OSDI 2008, USENIX
    locator: pp. 209 to 224, the sections on the architecture and on the search heuristics
  - paper: doi:10.1145/2093548.2093564
    title: Patrice Godefroid, Michael Y. Levin and David Molnar, SAGE, whitebox fuzzing for security testing, Communications of the ACM 55(3), 2012
    locator: pp. 40 to 44
---

Symbolic execution runs a program on symbols instead of concrete input values. Each program path gets a path condition, a formula that holds for exactly the inputs that follow that path. A solver for [satisfiability](/smt-problem/) finds an input for a path, or shows that the path cannot be taken. J. C. King (1976) described the method, at about the same time as Boyer, Elspas and Levitt (SELECT, 1975) and Clarke (1976). It is used today to generate tests and to find faults such as failed [assertions](/assertion/). A large program has too many paths, so the main limit of the method is path explosion.

## In plain words

A normal run uses a real input, such as the number 7, and follows one path. A symbolic run uses a name for the input, such as "the first argument", and keeps the name through all the steps. When the program reaches an "if", the symbolic run cannot say which side is taken. So it follows both sides. On each side it records the fact that must be true for the program to go there.

At the end of a path, the recorded facts say which inputs lead to that path. A solver can find one such input. If the path ends in an error, that input is a test that shows the error.

The method finds inputs that a random test would almost never find, for example an input that must be exactly twice another. It has trouble when the number of paths is very large.

## When it applies

- You want tests that cover many paths, or you want an input that reaches a given line or violates a given [assertion](/assertion/).
- The code is deterministic when the inputs are fixed, and the inputs can be named: arguments, the contents of a file, or messages.
- The conditions of the program belong to a theory that the solver decides: [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), [bit vectors](/bit-vector-satisfiability/), [arrays](/array-theory-satisfiability/). Fully general code with floating point, heap pointers and calls to the system is much harder.
- The program has a bounded number of paths, or you accept a bound on the depth and prove nothing about the part that you do not explore.

## The template

A *symbolic state* has three parts: the next statement, a *store* $\sigma$ that maps each variable to an expression over the input symbols, and a *path condition* $\pi$, which is a formula over the input symbols. The driver keeps a worklist of states.

```pseudo id=main
SYMEX(P)
L1  s0 ← (first statement of P, σ: each input x ↦ a fresh symbol α_x, π: true)
L2  W ← {s0}
L3  while W ≠ ∅ and the budget is not used up do
L4      s ← CHOOSE(W); remove s from W              ▷ hole: search strategy
L5      if depth(s) > BOUND then continue           ▷ hole: bound on the depth
L6      for each s′ in STEP(s) do
L7          if s′ is an error state then report MODEL(π(s′)) as a failing test
L8          else if s′ is final then emit MODEL(π(s′)) as a test
L9          else add s′ to W
```

The holes are CHOOSE, BOUND, the budget, and the solver behind SAT and MODEL, with the theory that it decides. SAT$(\varphi)$ answers whether the formula $\varphi$ has a model, and MODEL$(\varphi)$ returns one, as an input. STEP runs one statement of $s$ and returns the next states:

1. *Assignment* $v \leftarrow E$. Evaluate $E$ with the store: replace each variable of $E$ by its expression. Set $\sigma(v)$ to the result. The path condition does not change. One next state.
2. *Branch* on a test $B$. Let $b = \sigma(B)$. Make the state with $\pi \wedge b$ going to the true side, and the state with $\pi \wedge \neg b$ going to the false side. Keep each one whose condition passes SAT. A state whose condition is unsatisfiable is dropped, because the program cannot take that side.
3. *Assertion* $\mathbf{assert}\ A$. If SAT$(\pi \wedge \neg\sigma(A))$, return an error state with the path condition $\pi \wedge \neg\sigma(A)$: its model is an input that violates $A$. If SAT$(\pi \wedge \sigma(A))$, also return the state that goes on with $\pi \wedge \sigma(A)$, because the inputs that pass the assertion continue.
4. *End of a path.* The state is final. Its path condition $\pi$ describes the inputs of this path.

The states form a tree, the *execution tree*: its root is the start, each test with two feasible sides makes a node with two children, and each leaf is a final state or an error state.

**Properties.** Assume exact semantics for the operations, and a program that is deterministic given its input.

- An input $a$ follows the path of a node if and only if $a$ satisfies the path condition of the node. Proof by induction on the depth: the start has $\pi = \mathit{true}$; an assignment changes neither the path nor $\pi$; at a branch, an input that satisfies $\pi$ takes the true side exactly when it satisfies $b$, because $\sigma$ gives the values of the variables as functions of the input.
- The path conditions of two different leaves cannot both hold for one input, because the two paths differ at some test and the conditions have opposite signs for the test.
- If the execution tree is finite, the path conditions of its leaves cover all inputs, because each input follows some path to some leaf.

So if the tree is finite, the solver always answers (it never returns "unknown"), and each assertion is checked on each path that reaches it, then the checks cover all inputs. In this case the method proves that no assertion fails, for a program with no unbounded loop.

## Classic examples

Consider this program with the two integer inputs $x$ and $y$, with exact integer arithmetic.

1. $z \leftarrow 2y$
2. if $z = x$ then
3. $\quad$ if $x > y + 10$ then error
4. return

The symbolic run starts with $\sigma(x) = \alpha$, $\sigma(y) = \beta$, $\pi = \mathit{true}$. After line 1, $\sigma(z) = 2\beta$. The test on line 2 gives two states.

| path | path condition | end |
|---|---|---|
| 1 | $2\beta \ne \alpha$ | return |
| 2 | $2\beta = \alpha \wedge \alpha \le \beta + 10$ | return |
| 3 | $2\beta = \alpha \wedge \alpha > \beta + 10$ | error |

All three conditions are satisfiable, so the tree has three leaves. For path 3, substitute $\alpha = 2\beta$ into $\alpha > \beta + 10$. The result is $\beta > 10$. So the error is reached exactly for the inputs $x = 2y$ with $y \ge 11$, and one such input is $x = 22$ and $y = 11$. Take $x$ and $y$ uniform over the 32-bit values. With exact arithmetic, $2y$ is a 32-bit value for only half of the values of $y$, so a random test meets the first condition with a chance of about $2^{-33}$ (about $2^{-32}$ with wrapping arithmetic). A solver finds the input at once.

**Concolic testing.** The word *concolic* joins *concrete* and *symbolic*. The term comes from CUTE (Sen, Marinov and Agha, 2005). The program runs on a concrete input, and the run also builds the path condition of the path that it takes. To explore a new path, the tool negates one test of the condition, asks the solver for an input that satisfies the new condition, and runs again. DART (Godefroid, Klarlund and Sen, 2005) works in this way. For the program above, a start with $x = 1$ and $y = 0$ takes path 1 with the condition $2y \ne x$. The negation $2y = x$ has a solution, for example $x = 0$ and $y = 0$. This input takes path 2, with the condition $2y = x \wedge x \le y + 10$. The negation of the last test gives $2y = x \wedge x > y + 10$, and the solver returns an input such as $x = 22$ and $y = 11$, which reaches the error. When a condition is outside the theory of the solver, for example a call to a hash function, the tool replaces a symbolic value by the concrete value of the current run. Then each input that it finds still takes the path it aims for, and it gives up some paths.

The tools below are, from simple to large, the standard examples of the method.

- **King's EFFIGY (1976).** An interactive symbolic executor for a small language: the user follows the execution tree and asks for the path conditions. It shows the execution tree of the template.
- **DART and CUTE (2005).** Concolic testing of C functions: one concrete run per path, and the negation of one test of the path condition gives the next input.
- **KLEE (Cadar, Dunbar and Engler, 2008).** A symbolic executor for programs in the LLVM form. It keeps a set of states, forks a state at each test with two feasible sides, and checks the conditions with a constraint solver over bit vectors and arrays. It chooses the next state by search heuristics that aim to cover more code, and it writes a test input for each path that ends. On the GNU Coreutils programs its tests gave higher line coverage than the tests of the developers.
- **SAGE (Godefroid, Levin and Molnar).** Whitebox fuzzing at Microsoft: concolic runs of large programs that read files, with the negation of many tests of one long path condition per run. It is an application at the scale of whole products.
- **Comparison with [bounded model checking](/bounded-model-checking/).** A bounded model checker unrolls the loops to a fixed depth and puts all paths in one formula. Symbolic execution keeps one formula for each path. [Property-based testing](/property-based-testing/) and [differential testing](/differential-testing/) pick inputs at random, with no solver.

## Variations

- **Bounded loops.** For a loop whose test depends on a symbol, each number of iterations gives a different path, and the tree is infinite. Tools stop at a limit on the depth or on the number of iterations.
- **Search strategies.** Depth first, breadth first, random choice of path, and choice by the expected gain in coverage are all used. The strategy does not change which paths exist, only which ones are found within the budget.
- **Merging states.** Two states at the same point can be joined into one state, with a disjunction of the path conditions and with if-then-else expressions in the store. This gives fewer states and larger formulas for the solver.
- **Concretization.** A symbolic value is replaced by a concrete one, for example for a pointer or for a call to the environment. This keeps the solver fast and loses some paths.
- **Summaries.** The effect of a function is described once by pairs of a path condition and a result, and it is reused at each call.
- **Use for proofs.** A path condition together with an assertion is the same kind of formula as a verification condition of [Floyd's method](/floyd-inductive-assertions/). The two differ in how they treat loops: Floyd's method cuts the loop with an invariant, and symbolic execution unrolls the loop. Along one path, the pair $(\sigma, \pi)$ is the strongest postcondition of the path, and the check of an assertion is the check of a [weakest precondition](/weakest-precondition/) of the path.

## Pitfalls

- *Path explosion.* Each test with two feasible sides can double the number of paths. A program with $n$ tests on independent inputs, one after another, has $2^n$ paths. For $n = 40$ that is $2^{40} \approx 1.1 \times 10^{12}$ paths. Loops make the count unbounded. This is the main limit of the method.
- *Cost of the solver.* Deciding a path condition is a satisfiability problem. Already in the propositional case it is the NP-complete problem of [Boolean satisfiability](/sat/). Bit vectors of a fixed width keep the problem decidable and NP-complete. With multiplication of two unknown integers the problem is worse: satisfiability of polynomial equations over the integers is undecidable, by the solution of [Hilbert's tenth problem](/hilberts-tenth-problem/). So a solver can return "unknown" or never answer.
- *Unbounded integers against machine integers.* The path conditions above use exact integers. In 32-bit signed arithmetic, $2y$ can wrap. For $y = 2^{30}$ the product $2y$ is $2^{31}$, which wraps to $-2^{31}$, so $x = -2^{31}$ and $y = 2^{30}$ satisfy $2y = x$ in the machine arithmetic and do not satisfy it in exact arithmetic. The model must use the arithmetic of the real program, usually bit vectors. See [integer overflow](/integer-overflow/).
- *A timeout is not a proof.* When the solver does not answer in time, a tool that drops the path loses faults, and a tool that keeps the path may report a false fault.
- *Incomplete exploration.* A report of no fault is a proof only if the tree is finite, all the paths were explored to their end, the solver answered each query, and the model of the program is exact. A tool with a depth limit finds faults, and it does not prove their absence.
- *Environment.* Files, the network, threads and system calls are outside the program. A tool must model them or fix them, and a wrong model gives wrong paths.

## Exercises

1. Take the program: if $x > 3$ then $y \leftarrow 1$ else $y \leftarrow 2$, followed by: if $x < 0$ and $y = 1$ then error. How many paths does the execution tree have? *Answer:* 2. The first test gives two states. In the state with $x > 3$ the store has $y = 1$, and the second test needs $x < 0$, so the true side has the condition $x > 3 \wedge x < 0$, which is unsatisfiable. In the state with $x \le 3$ the store has $y = 2$, so the second test is false. Only the two false sides remain.
2. For the program in the examples, write the path conditions if line 1 reads $z \leftarrow 3y$. *Answer:* the test is $3\beta = \alpha$, and the error path has $3\beta = \alpha \wedge \alpha > \beta + 10$, which is $\beta > 5$. For $y = 6$ and $x = 18$, the error is reached.
3. Why can two path conditions of one deterministic program not share an input? *Answer:* two different paths diverge at some test. One condition has the test and the other has its negation, so no input satisfies both.
4. The program $i \leftarrow 0 ;\ \mathbf{while}\ i < n\ \mathbf{do}\ i \leftarrow i + 1$ has the symbolic input $n$. With a bound of $k$ iterations, how many paths end, and what are their path conditions? *Answer:* $k + 1$. The path with $j$ iterations, for $0 \le j \le k$, has the condition $n \le 0$ when $j = 0$, and $n = j$ when $j \ge 1$. One more state, with the condition $n > k$, is cut off by the bound.
5. Run the example program with 32-bit wrapping arithmetic for $2y$ and for $y + 10$. Find an input with $y < 0$ that reaches the error. *Answer:* $y = -2^{31}$ and $x = 0$. Then $2y = -2^{32}$ wraps to 0, which equals $x$, and $y + 10 = -2^{31} + 10$ does not wrap, so $x > y + 10$. Another input is $x = -2$ and $y = 2^{31} - 1$, where both $2y$ and $y + 10$ wrap.

## References
