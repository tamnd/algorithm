---
tag: NW4VDT
kind: concept
slug: computational-tractability
name: Computational tractability
aliases:
- Cobham-Edmonds thesis
- Cobham's thesis
area: complexity/complexity-classes
level: intro
summary: "The Cobham-Edmonds thesis: a problem is tractable when a polynomial-time algorithm solves it. Why theory adopts this convention, and where it fails."
prereqs: [polynomial-time, time-complexity]
see_also: [p, polynomial-time, p-versus-np-problem, np-complete, fixed-parameter-tractable, conditional-lower-bound, bqp, exptime]
sources:
  - paper: "Alan Cobham, The intrinsic computational difficulty of functions, in Y. Bar-Hillel (editor), Logic, Methodology and Philosophy of Science, Proceedings of the 1964 International Congress, North-Holland (1965), 24 to 30"
    locator: the class of functions computable in time polynomial in the length of the input
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17 (1965), 449 to 467
    locator: Section 2, the digression on good algorithms
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Chapter 1 (polynomial and exponential time, the growth tables)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 1 (the philosophical importance of P and the criticisms of P)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.1 (computational tractability)
---

Computational tractability is the convention that a problem is *tractable*, or feasible, when some algorithm solves it in [polynomial time](/polynomial-time/), and *intractable* when no such algorithm exists. This convention is called the Cobham-Edmonds thesis, after Alan Cobham and Jack Edmonds, who proposed it independently in 1965. It is the reason why the class [P](/p/) stands for "the problems that computers can solve", and why an [NP-complete](/np-complete/) problem counts as hard. The thesis is a definition that has proved useful, not a theorem, and it has known limits.

## In plain words

When the input grows, a good algorithm should slow down at a steady rate. If the input doubles, a program whose time grows like a fixed power of the input size becomes slower by a fixed factor, such as 4 or 8. A program that tries every subset of the items becomes slower by a factor that itself grows without limit: doubling the input squares its running time.

The thesis draws the line between these two kinds of growth. Programs of the first kind count as efficient, programs of the second kind do not. The line is useful because it does not depend on the computer or on the programming language. It can also be wrong for a single program, because a power of 50 is efficient by the rule and useless in practice.

## The idea

### The thesis

Let $T(n)$ be the worst-case number of steps of an algorithm on inputs of length $n$, where $n$ is the length of a reasonable encoding of the input in bits. The Cobham-Edmonds thesis says:

> A problem can be solved efficiently in practice if and only if it can be solved by an algorithm with $T(n) = O(n^k)$ for some constant $k$.

In terms of classes, the tractable decision problems are the problems in [P](/p/) and the tractable function problems are those in [FP](/fp/). The thesis is not a mathematical statement. It identifies an informal notion (efficient) with a formal one (polynomial), as the [Church-Turing thesis](/church-turing-thesis/) identifies "computable by a procedure" with "computable by a Turing machine".

### Why polynomial time

There are four arguments for the thesis.

1. **Growth.** An exponential function overtakes every polynomial. A faster computer helps a polynomial algorithm by a constant factor in the input size, and helps an exponential algorithm only by an additive constant. The table under Examples shows this.
2. **Robustness.** Polynomial time is the same for one-tape and multitape [Turing machines](/turing-machine/), for the [random-access machine](/random-access-machine/) with the logarithmic cost, and for every other deterministic model that is used in practice ([RAM and Turing machine equivalence](/ram-turing-equivalence/)). So "tractable" does not depend on the computer. A fixed exponent such as $n^2$ does depend on it.
3. **Closure.** Polynomials are closed under sum, product and composition. A program that calls a polynomial-time subroutine a polynomial number of times, on arguments of polynomial length, runs in polynomial time. Theory can build algorithms from parts without leaving the class.
4. **Natural problems.** Experience suggests that once a natural problem is known to be in P, algorithms with a small exponent follow. The first polynomial-time algorithm is often slow, and later work lowers the exponent.

### Where the thesis is weak

- **Large exponents and constants.** A running time of $n^{100}$ is polynomial and useless. The test for a fixed minor that comes with the [graph minor theorem](/graph-minor-theorem/) runs in cubic time in the version of Robertson and Seymour, with constants too large for any computer.
- **Fast exponential algorithms.** An exponential worst case can be harmless on the inputs that occur. The [simplex method](/simplex-method/) has exponential worst cases for its classical pivot rules, but it is fast in practice. Modern [SAT](/sat/) solvers decide many large industrial formulas, although SAT is NP-complete.
- **Worst case only.** The thesis looks at the worst input. Average-case analysis and the [smoothed analysis of the simplex method](/smoothed-simplex-analysis/) give other answers for some problems.
- **The model of physics.** The *strong* (or extended) Church-Turing thesis says that every reasonable physical model of computation is simulated by a probabilistic Turing machine with a polynomial slowdown. Shor's algorithm puts [factoring in BQP](/factoring-in-bqp/), while no polynomial-time classical algorithm for factoring is known. If large quantum computers are built, the strong thesis may fail, even though the Cobham-Edmonds thesis stays a good definition for each fixed model.
- **Randomness.** Some problems have fast randomized algorithms and no known deterministic ones. [Polynomial identity testing](/polynomial-identity-testing/) is the standard example. Many authors count the class [BPP](/bpp/), not P, as the tractable problems. Whether $\mathsf{BPP} = \mathsf{P}$ is open.

### Refinements

Several parts of complexity theory refine the line between tractable and intractable. Parameterized complexity calls a problem [fixed-parameter tractable](/fixed-parameter-tractable/) when it has an algorithm of time $f(k) \cdot n^{c}$ for a parameter $k$, so that an exponential part depends only on $k$. Fine-grained complexity studies the exact exponent inside P, with [conditional lower bounds](/conditional-lower-bound/) such as "no $O(n^{2 - \varepsilon})$ algorithm for edit distance unless SETH fails". Approximation algorithms ask how close to the optimum a polynomial-time algorithm can get when the exact problem is NP-hard.

## Examples

**Growth at $10^9$ steps per second.** The table gives the time of an algorithm that takes exactly $T(n)$ steps.

| $n$ | $n^2$ | $n^3$ | $n^5$ | $2^n$ | $n!$ |
|---|---|---|---|---|---|
| 10 | 0.1 µs | 1 µs | 100 µs | 1.02 µs | 3.63 ms |
| 20 | 0.4 µs | 8 µs | 3.2 ms | 1.05 ms | 77.1 years |
| 30 | 0.9 µs | 27 µs | 24.3 ms | 1.07 s | $8.41 \times 10^{15}$ years |
| 40 | 1.6 µs | 64 µs | 102 ms | 18.3 minutes | $2.59 \times 10^{31}$ years |
| 50 | 2.5 µs | 125 µs | 312 ms | 13 days | $9.64 \times 10^{47}$ years |
| 60 | 3.6 µs | 216 µs | 778 ms | 36.5 years | $2.64 \times 10^{65}$ years |
| 100 | 10 µs | 1 ms | 10 s | $4.02 \times 10^{13}$ years | $2.96 \times 10^{141}$ years |

For small inputs the exponential algorithm can be faster: at $n = 10$, $2^n$ steps take less time than $n^5$ steps.

**A faster computer.** In one hour, a computer that does $10^9$ steps per second solves inputs up to these sizes: $n = 1{,}897{,}366$ for $n^2$ steps, $n = 15{,}326$ for $n^3$ steps and $n = 41$ for $2^n$ steps. A computer that is 1000 times faster reaches $n = 60{,}000{,}000$, $n = 153{,}261$ and $n = 51$. The polynomial algorithms gain a factor ($1000^{1/2} \approx 31.6$ and $1000^{1/3} = 10$), and the exponential one gains about $\lg 1000 \approx 10$ items.

**Tractable problems.** Shortest paths with non-negative weights ([Dijkstra's algorithm](/dijkstra/)), [maximum matching](/maximum-matching/) in general graphs, [linear programming](/lp-in-p/) and [primality testing](/aks-primality-test/) are in P. Edmonds's paper on matching introduced the word "good" for a polynomial-time algorithm.

**Problems believed intractable.** No polynomial-time algorithm is known for [SAT](/sat/), the [traveling salesman problem](/traveling-salesman-problem/) or the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/). Each is NP-complete, so a polynomial-time algorithm for one of them would give one for every problem in NP. Some problems are provably intractable: by the [time hierarchy theorem](/time-hierarchy-theorem/), every problem that is complete for [EXP](/exptime/) is outside P.

## Where it is used

The thesis is the reason for the shape of the theory of [NP-completeness](/np-complete/): a proof of NP-completeness is read as evidence of intractability, because it shows that a polynomial-time algorithm would answer the [P versus NP problem](/p-versus-np-problem/). Garey and Johnson built their guide on this reading. Algorithm textbooks, for example Kleinberg and Tardos (Section 2.1), use polynomial time as the working definition of efficiency.

Cobham (1965) described the class of functions computable in time polynomial in the length of the input, showed that it does not depend on the choice of a reasonable machine, and gave it a machine-free definition by recursion. In the same year Edmonds called an algorithm good when its running time is bounded by a polynomial in the size of the input, and gave a good algorithm for maximum matching. The two papers are the origin of the name of the thesis.

## References
