---
tag: 3NZ9N7
kind: concept
slug: exact-exponential-algorithms
name: Exact exponential-time algorithms
aliases:
- exact algorithms
- exponential-time algorithms
area: combinatorics/exhaustive-search
level: advanced
summary: Algorithms that solve NP-hard problems optimally in running time exponential in the input size, with a better base than brute force.
prereqs: [np-hard, brute-force-search, combinatorial-explosion]
see_also: [measure-and-conquer, held-karp-algorithm, bjorklund-chromatic-number, horowitz-sahni-algorithm, schoning-algorithm, branch-and-reduce, strong-exponential-time-hypothesis, brute-force-search]
sources:
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 1 (the O* notation and the branching analysis of maximum independent set), Chapter 2 (branching), Chapter 3 (dynamic programming), Chapter 4 (inclusion-exclusion) and Chapter 6 (measure and conquer)
  - paper: doi:10.1007/3-540-36478-1_17
    title: Gerhard J. Woeginger, Exact algorithms for NP-hard problems, a survey, in Combinatorial Optimization, Eureka, You Shrink!, Lecture Notes in Computer Science 2570, Springer, 2003, 185 to 207
    locator: the techniques of dynamic programming across subsets, pruning the search tree, preprocessing, and local search, with open problems
  - paper: "Michael Held and Richard M. Karp, A dynamic programming approach to sequencing problems, Journal of the Society for Industrial and Applied Mathematics 10(1), 1962, 196 to 210"
    locator: the dynamic program over subsets for the traveling salesman problem in O(n^2 2^n) time
  - paper: "Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 2009, 546 to 563"
    locator: the chromatic number of an n-vertex graph in time 2^n times a polynomial
  - paper: "Fedor V. Fomin, Fabrizio Grandoni and Dieter Kratsch, A measure and conquer approach for the analysis of exact algorithms, Journal of the ACM 56(5), 2009"
    locator: maximum independent set in O(1.2201^n) time and polynomial space by measure and conquer
---

An *exact exponential-time algorithm* solves an [NP-hard](/np-hard/) problem exactly, with no approximation, in time $O^*(c^n)$ for a constant $c$ that is smaller than the base of [brute-force search](/brute-force-search/). The notation $O^*$ hides factors polynomial in the input size, and $n$ is a natural measure of the instance, such as the number of vertices or variables. Since no polynomial algorithm is expected, the aim is to lower the base: the difference between $2^n$ and $1.2^n$ is the difference between $n = 40$ and $n = 150$ in the same time. The main tools are branching, dynamic programming over subsets, inclusion-exclusion, meet in the middle and randomized local search.

## In plain words

Some problems seem to have no fast method at all. For them, the best that anyone knows is a search through a very large number of cases. Exact exponential algorithms still search, but they search much less than the plain method of trying everything.

They do this with tricks that are proven to work. A search can skip choices that cannot help. It can remember answers for parts of the problem and reuse them. It can split the problem into two halves and match the halves. It can count answers with a formula instead of listing them.

The answer is always correct and optimal. Only the time grows fast. But when the growth is slower, the same computer can solve much bigger problems.

## The idea

**The trivial bound.** Most problems in [NP](/np/) have a natural search space: for a graph with $n$ vertices, the $2^n$ subsets of vertices; for a formula with $n$ variables, the $2^n$ assignments; for a tour through $n$ cities, the $(n-1)!/2$ tours. Checking every candidate gives the trivial bound. An exact exponential algorithm beats it by an exponential factor.

**The $O^*$ notation.** $f(n) = O^*(g(n))$ means $f(n) = O(g(n) \cdot p(n))$ for a polynomial $p$. Since $c^n p(n) = O((c + \varepsilon)^n)$ for every $\varepsilon > 0$, bases are often rounded up, as in $O(1.3803^n)$.

**Branching.** A [branch-and-reduce](/branch-and-reduce/) algorithm applies reduction rules, then splits the instance into smaller instances. If a branch removes $t_1, \ldots, t_k$ units of the measure in its $k$ subproblems, the running time satisfies $T(n) \le T(n - t_1) + \cdots + T(n - t_k)$, and $T(n) = O^*(\lambda^n)$, where $\lambda$ is the unique positive root of $1 = \sum_i x^{-t_i}$. The worst branch decides the bound. [Measure and conquer](/measure-and-conquer/) improves the analysis with a cleverer measure than $n$.

**Dynamic programming over subsets.** Store a value for every subset of a set of size $n$ instead of every ordering. The [Held-Karp algorithm](/held-karp-algorithm/) solves the [traveling salesman problem](/traveling-salesman-problem/) in $O(n^2 2^n)$ time, against $(n-1)!/2$ tours. The price is exponential space. See [bitmask DP](/bitmask-dp/).

**Inclusion-exclusion.** Count the objects with a formula over all subsets, which needs only polynomial space. With it, [Björklund, Husfeldt and Koivisto](/bjorklund-chromatic-number/) compute the chromatic number in $O^*(2^n)$ time, and [Ryser's formula](/ryser-formula/) computes the permanent in $O^*(2^n)$ time instead of $n!$.

**Meet in the middle.** Split the $n$ variables into two halves, list the $2^{n/2}$ partial solutions of each half, and combine them by sorting or hashing. The [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/) solves [subset sum](/subset-sum-problem/) in $O^*(2^{n/2})$ time, and the [Schroeppel-Shamir algorithm](/schroeppel-shamir-algorithm/) lowers its space to $O^*(2^{n/4})$.

**Randomized local search.** [Schöning's algorithm](/schoning-algorithm/) for [3-SAT](/3-sat/) starts from a random assignment and makes $3n$ random repair steps, and repeats. It finds a satisfying assignment, if there is one, in expected time $O^*((4/3)^n)$. The [PPSZ algorithm](/ppsz-algorithm/) improves the base further.

**Lower bounds.** No exact exponential algorithm is known to be optimal unconditionally. The exponential time hypothesis states that 3-SAT has no algorithm in time $2^{o(n)}$, and the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) states that for every $\varepsilon > 0$ there is a $k$ such that $k$-SAT has no algorithm in time $O((2 - \varepsilon)^n)$. Under these hypotheses, many bounds of the form $O^*(2^n)$ cannot be improved to $O^*((2 - \varepsilon)^n)$, and many bounds of the form $2^{O(n)}$ cannot be improved to $2^{o(n)}$.

## Examples

**Maximum independent set by branching.** An [independent set](/independent-set/) of a graph has no two adjacent vertices. Brute force tries all $2^n$ subsets. A simple branching algorithm does better:

1. If some vertex $v$ has degree 0 or 1, some maximum independent set contains $v$. Take $v$, delete $v$ and its neighbor, and continue. No branch is needed.
2. If every vertex has degree 2, the graph is a union of cycles, and the answer is $\sum \lfloor \ell / 2 \rfloor$ over the cycle lengths $\ell$.
3. Otherwise pick a vertex $v$ of degree at least 3, and branch. Either $v$ is not in the set: delete $v$, which leaves $n - 1$ vertices. Or $v$ is in the set: delete $v$ and its at least 3 neighbors, which leaves at most $n - 4$ vertices.

The recurrence is $T(n) \le T(n - 1) + T(n - 4)$, and the root of $x^4 = x^3 + 1$ is $\lambda \approx 1.3803$. So the algorithm runs in $O(1.3803^n)$ time and polynomial space. For $n = 50$, $1.3803^{50} \approx 10^7$, while $2^{50} \approx 1.1 \times 10^{15}$. More careful rules and the measure-and-conquer analysis of Fomin, Grandoni and Kratsch give $O(1.2201^n)$.

**Traveling salesman.** For $n = 20$ cities, there are $19!/2 \approx 6.1 \times 10^{16}$ tours, but Held-Karp needs about $20^2 \cdot 2^{20} \approx 4.2 \times 10^8$ steps. No algorithm in time $O^*((2 - \varepsilon)^n)$ for the general problem is known.

**Satisfiability.** For 3-SAT with $n$ variables, brute force checks $2^n$ assignments. Schöning's algorithm needs $O^*((4/3)^n)$ expected time. At $n = 100$, $2^{100} \approx 1.3 \times 10^{30}$, while $(4/3)^{100} \approx 3.1 \times 10^{12}$.

**A non-example.** For general [CNF-SAT](/sat/) with $n$ variables and clauses of any length, no algorithm in time $O^*((2 - \varepsilon)^n)$ is known for any fixed $\varepsilon > 0$, and the strong exponential time hypothesis states that none exists. Here brute force may be the best possible base.

## Where it is used

- **Exact solutions of small hard instances.** Scheduling, routing, coloring and other problems where an optimal answer for a few dozen elements is worth the cost.
- **Kernels and parameters.** An exact algorithm runs on the small kernel that a [fixed-parameter](/fixed-parameter-tractable/) reduction produces, and branching analysis is shared with [bounded search trees](/bounded-search-tree/).
- **Subroutines.** Exact algorithms on small pieces appear inside approximation schemes and inside decompositions such as tree decompositions.
- **Fine-grained complexity.** The question of which bases are possible, under hypotheses such as the strong exponential time hypothesis, organizes many problems into classes.
- **Benchmarks for solvers.** Exact algorithms give the reference answers against which heuristics are tested.

## References
