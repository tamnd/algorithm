---
tag: R32A7X
kind: algorithm
slug: kung-algorithm
name: Kung's algorithm
aliases:
- Kung-Luccio-Preparata algorithm
- maxima-finding divide and conquer
- KLP maxima algorithm
area: optimization/multi-objective
level: advanced
summary: Divide-and-conquer computation of the maxima of a vector set, running in O(n log n) for d up to 3 and O(n log^(d-2) n) for higher d.
solves: [pareto-front-computation]
model: comparison-model
complexity:
  vars: {n: the number of vectors, p: the number of objectives (the dimension d)}
  time: {worst: "O(n log^(max(1, p-2)) n)"}
  space: {extra: O(p^2 n)}
properties: {deterministic: true, comparison: true, recursive: true, output-sensitive: false}
history:
  year: 1975
  people: [H. T. Kung, F. Luccio, F. P. Preparata]
  note: Kung, Luccio and Preparata gave the divide and conquer maxima algorithm and the lower bound of log2 n! comparisons in the Journal of the ACM in 1975. Bentley put the method into his framework of multidimensional divide and conquer in 1980.
prereqs: [pareto-dominance, divide-and-conquer-paradigm, lexicographic-order]
see_also: [non-dominated-sorting, bnl-skyline, sort-filter-skyline, dominance-counting, range-tree, pareto-front, convex-hull]
sources:
  - paper: doi:10.1145/321906.321910
    title: H. T. Kung, F. Luccio and F. P. Preparata, On finding the maxima of a set of vectors, Journal of the ACM 22(4), 1975
    locator: pages 469 to 476 (the divide and conquer algorithm, the bounds O(n log n) for d = 2, 3 and O(n log^(d-2) n) for d ≥ 4, and the lower bound of log2 n! comparisons)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Section 4.1.3 (the maxima of a point set)
  - paper: doi:10.1145/358841.358850
    title: Jon Louis Bentley, Multidimensional divide-and-conquer, Communications of the ACM 23(4), 1980
    locator: pages 214 to 229 (the maxima problem as an example of multidimensional divide and conquer)
  - paper: doi:10.1145/322092.322095
    title: J. L. Bentley, H. T. Kung, M. Schkolnick and C. D. Thompson, On the average number of maxima in a set of vectors and applications, Journal of the ACM 25(4), 1978
    locator: pages 536 to 543 (the expected number of maxima and algorithms with linear expected time)
  - paper: doi:10.1145/323233.323246
    title: David G. Kirkpatrick and Raimund Seidel, Output-size sensitive algorithms for finding maximal vectors, Proceedings of the First Annual Symposium on Computational Geometry, 1985
    locator: pages 89 to 96 (bounds in terms of the number of maxima)
  - paper: doi:10.1109/TEVC.2003.817234
    title: Mikkel T. Jensen, Reducing the run-time complexity of multiobjective EAs, the NSGA-II and other algorithms, IEEE Transactions on Evolutionary Computation 7(5), 2003
    locator: pages 503 to 515 (the extension of the method to non-dominated sorting)
---

Kung's algorithm finds the nondominated vectors of a finite set of $n$ vectors in $\mathbb{R}^p$, the [Pareto front](/pareto-front/) of a finite set. Kung, Luccio and Preparata gave it in 1975 as an algorithm for the *maxima* of a set of vectors; with all objectives minimized, the maxima become the minima, and nothing else changes. It sorts the vectors once, splits them into two halves, solves each half, and then removes the vectors of the second half that the first half dominates. This last step is itself a divide and conquer on one fewer coordinate. The time is $O(n \log n)$ for $p = 2$ and $p = 3$ and $O(n \log^{p-2} n)$ for $p \ge 4$, and no algorithm that compares coordinates can do better than $\lceil \log_2 n! \rceil$ comparisons for $p \ge 2$.

## In plain words

You have a list of options, each with several costs, and you want the options that no other option beats. One option beats another if it is no worse in any cost and better in at least one.

Sort the list by the first cost. An option late in the list can never beat an option early in the list. So split the list in the middle and solve each half alone. All the winners of the first half stay. A winner of the second half stays only if no winner of the first half beats it.

That last test is the hard part. It looks like the first problem, with one cost fewer, because the first cost is already settled by the sort. So it is solved in the same way, by splitting again. With two or three costs the test is one pass over a sorted list.

## The problem

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, and each input vector $y$ is the image $y = f(x)$ of some solution $x$. A vector $a$ dominates $b$, written $a \prec b$, when $a_j \le b_j$ for each $j$ and $a \ne b$. This is [Pareto dominance](/pareto-dominance/).

The input is a set $P$ of $n$ distinct vectors of $\mathbb{R}^p$. Only comparisons of two coordinates are used, so any totally ordered values work. The output is the set of nondominated vectors

$$\min P = \{\, b \in P : \text{no } a \in P \text{ has } a \prec b \,\}.$$

This is the finite case of [Pareto front computation](/pareto-front-computation/), also called the maxima problem in computational geometry and the skyline query in databases. Copies of a vector do not dominate each other; they are removed first and given back at the end.

## The algorithm

The core is a subroutine $\mathrm{FILTER}(A, B, k)$. It returns the vectors $b \in B$ such that no $a \in A$ satisfies $a_j \le b_j$ for all $j = k, \ldots, p$. When every $a \in A$ already satisfies $a_j \le b_j$ for $j < k$, this is exactly the set of $b \in B$ that $A$ does not dominate.

```pseudo id=main
KUNG(P)                                          ▷ P: n distinct vectors of ℝ^p, p ≥ 2
L1  sort P lexicographically; return FRONT(P)
FRONT(S)                                         ▷ S is sorted lexicographically
L2  if |S| = 1 then return S
L3  T ← the first ⌊|S|/2⌋ vectors of S;  B ← the other vectors of S
L4  R_T ← FRONT(T);  R_B ← FRONT(B)
L5  return R_T ∪ FILTER(R_T, R_B, 2)
FILTER(A, B, k)        ▷ the b ∈ B with no a ∈ A such that a_j ≤ b_j for j = k, ..., p
L6  if A = ∅ or B = ∅ then return B
L7  if k = p then return { b ∈ B : b_p < min over a ∈ A of a_p }
L8  if k = p − 1 then
L9      scan A ∪ B by increasing x_k, A before B on ties; m ← the least x_{k+1} of the A vectors scanned so far
L10     return the b ∈ B with b_{k+1} < m at the moment when b is scanned
L11 split A ∪ B, in the order of line L9, into a lower half and an upper half; A_lo, B_lo, A_hi, B_hi are the parts of A and B
L12 B_lo′ ← FILTER(A_lo, B_lo, k)
L13 B_hi′ ← FILTER(A_hi, B_hi, k)
L14 return B_lo′ ∪ FILTER(A_lo, B_hi′, k + 1)
```

Line L5 can call FILTER on coordinates $2, \ldots, p$ only, because every vector of $T$ comes before every vector of $B$ in the sort, so its first coordinate is not larger. Line L11 uses the same idea one level down: a vector of $A_{lo}$ has $x_k$ not larger than any vector of $B_{hi}$, so line L14 can drop coordinate $k$. A vector of $A_{hi}$ has $x_k$ strictly larger than any vector of $B_{lo}$, because ties put $A$ first, so $A_{hi}$ cannot beat $B_{lo}$, and no fourth call is needed.

For $p = 2$, line L5 calls line L7 at once, and the algorithm is a sort followed by a merge. For $p = 3$, line L5 calls the sweep of lines L9 and L10. Lines L11 to L14 run only for $p \ge 4$.

The sort of line L1 is done once. Each set in the recursion is kept as $p$ lists, one sorted lexicographically and one sorted by each coordinate $j \ge 2$. Lines L3 and L11 split each list by one pass with a mark on the lower part, so no call sorts again.

## Example

Take the seven vectors $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, with $p = 2$. They are already sorted. Each FILTER call is line L7: a vector of the second set stays if its second coordinate is below the least second coordinate of the first set.

| call | $R_T$ | $R_B$ | least $y_2$ in $R_T$ | kept from $R_B$ | result |
|---|---|---|---|---|---|
| FRONT($b, c$) | $b$ | $c$ | 6 | none ($7 \ge 6$) | $b$ |
| FRONT($a, b, c$) | $a$ | $b$ | 9 | $b$ | $a, b$ |
| FRONT($d, e$) | $d$ | $e$ | 4 | $e$ | $d, e$ |
| FRONT($f, g$) | $f$ | $g$ | 5 | $g$ | $f, g$ |
| FRONT($d, e, f, g$) | $d, e$ | $f, g$ | 3 | $g$ ($f$ has $5 \ge 3$) | $d, e, g$ |
| FRONT($a, \ldots, g$) | $a, b$ | $d, e, g$ | 6 | $d, e, g$ | $a, b, d, e, g$ |

The answer $\{a, b, d, e, g\}$ is the Pareto front. The dominated vectors $c$ and $f$ are removed in the calls where their dominators $b$ and $d$ first meet them.

With $p = 3$, take $q_1 = (0, 5, 5)$, $q_2 = (1, 1, 9)$, $q_3 = (1, 1, 10)$, $q_4 = (5, 0, 5)$, $q_5 = (5, 5, 0)$ and $q_6 = (6, 6, 6)$, sorted. The halves give $R_T = \{q_1, q_2\}$ ($q_2$ removes $q_3$) and $R_B = \{q_4, q_5\}$ ($q_5$ removes $q_6$). The last call FILTER$(R_T, R_B, 2)$ runs the sweep of line L9 by the second coordinate.

| scanned | set | $x_2$ | $x_3$ | $m$ before | action | $m$ after |
|---|---|---|---|---|---|---|
| $q_4$ | $B$ | 0 | 5 | $\infty$ | keep, $5 < \infty$ | $\infty$ |
| $q_2$ | $A$ | 1 | 9 | $\infty$ | | 9 |
| $q_1$ | $A$ | 5 | 5 | 9 | | 5 |
| $q_5$ | $B$ | 5 | 0 | 5 | keep, $0 < 5$ | 5 |

The tie $x_2 = 5$ puts $q_1$ before $q_5$. The answer is $\{q_1, q_2, q_4, q_5\}$.

## Correctness

Two facts carry the proof. First, a vector cannot be dominated by a vector that comes later in the lexicographic order, so the winners of $T$ are winners of $S$, and a vector of $B$ that some vector of $T$ dominates is also dominated by some winner of $T$. Second, FILTER meets its specification, by induction on the number of coordinates left and on $|A| + |B|$: line L7 is one coordinate, the sweep of lines L9 and L10 sees exactly the vectors of $A$ with $a_k \le b_k$ before $b$, and the split of line L11 sends each pair to a call that decides it. For distinct vectors, $a_j \le b_j$ for all $j$ means $a \prec b$, so FILTER at the top removes exactly the dominated vectors. The full proof is below.

## Complexity

Let $T_d(n)$ be the time of FILTER with $d = p - k + 1$ coordinates left and $|A| + |B| = n$. With the sorted lists, line L7 and the sweep take linear time, so $T_1(n) = O(n)$ and $T_2(n) = O(n)$. For $d \ge 3$, the two calls of lines L12 and L13 have half the size, the call of line L14 has at most $n$ vectors and one coordinate fewer, and the split costs $O(d n)$:

$$T_d(n) \le 2\, T_d(n/2) + T_{d-1}(n) + O(d n), \qquad \text{so} \qquad T_d(n) = O(n \log^{d-2} n).$$

The top level calls FILTER with $d = p - 1$ coordinates, so the time $F(n)$ of FRONT satisfies

$$F(n) \le 2\, F(n/2) + T_{p-1}(n) + O(p n).$$

For $p = 2$ and $p = 3$, $T_{p-1}(n) = O(n)$ and $F(n) = O(n \log n)$. For $p \ge 4$, $T_{p-1}(n) = O(n \log^{p-3} n)$ and $F(n) = O(n \log^{p-2} n)$. The sort of line L1 adds $O(p n \log n)$. The constants grow with $p$.

**Lower bound.** Kung, Luccio and Preparata show that every algorithm that compares two coordinates at a time needs at least $\lceil \log_2 n! \rceil = \Omega(n \log n)$ comparisons in the worst case for $p \ge 2$. So the algorithm is optimal for $p = 2$ and $p = 3$. For $p \ge 4$ the gap between $n \log n$ and $n \log^{p-2} n$ is not closed by this argument.

**Space.** A call keeps its lists while its children run. Along a chain of calls, each step either halves the size or drops a coordinate, so the lists on the stack hold $O(p^2 n)$ entries. The depth of the recursion is $O(p \log n)$.

**The size of the answer.** The front can have all $n$ vectors, for example $n$ vectors on the line $y_1 + y_2 = 1$. For vectors with independent coordinates drawn from continuous distributions, the expected number of nondominated vectors $A(n, p)$ satisfies $A(n, 1) = 1$ and $A(n, p) = \sum_{k=1}^{n} A(k, p-1)/k$, so $A(n, 2) = H_n$, the harmonic number, and $A(n, p) = O(\log^{p-1} n)$ (Bentley, Kung, Schkolnick and Thompson, 1978).

## Properties

- **Deterministic and comparison based.** It uses only comparisons of two values of the same coordinate, so it works for any totally ordered values, such as integers, fractions or strings.
- **Not output sensitive.** It takes $\Theta(n \log n)$ time for $p = 2$ even when the front has one vector.
- **Exact.** It returns the full front of a finite set, with no tolerance.
- **Depth.** The recursion depth is $O(p \log n)$, so stack depth is not a problem.

## Variants and improvements

- **Two objectives.** Sort lexicographically and scan, keeping the least second coordinate seen so far. A vector is kept when its second coordinate is below that value. This is the same algorithm with the recursion unrolled.
- **Three objectives.** Sort by the first coordinate and sweep, keeping the front of the vectors seen so far in the other two coordinates as a staircase in a balanced search tree. This gives $O(n \log n)$ with one sort.
- **Output-sensitive algorithms.** Kirkpatrick and Seidel (1985) give algorithms whose time depends on the number $h$ of nondominated vectors, such as $O(n \log h)$ for $p = 2$ and $p = 3$.
- **Average case.** Bentley, Kung, Schkolnick and Thompson (1978) give algorithms with $O(n)$ expected time for vectors with independent coordinates, because the expected front is small.
- **All fronts.** Jensen (2003) uses the same divide and conquer to compute every front of [non-dominated sorting](/non-dominated-sorting/) in $O(n \log^{p-1} n)$ time.
- **Database skylines.** [Block nested loops](/bnl-skyline/) and [sort-filter-skyline](/sort-filter-skyline/) are not as good in the worst case, but they work with data on disk and are fast when the front is small.
- **Counting instead of filtering.** The same recursion with counters computes, for every vector, the number of vectors that dominate it. See [dominance counting](/dominance-counting/) and [range trees](/range-tree/).

## When to use it

Use it when the front may be large, when $p$ is small, and when a worst-case bound matters, for example in a library routine that must handle every input. For $p = 2$ the sort and scan is simpler and has the same bound. For random data with few nondominated vectors, a simple filter such as sort-filter-skyline is often faster. For $p$ much larger than $\log n$, the $\log^{p-2} n$ factor is larger than $n$, and the $O(p n^2)$ comparison of all pairs is faster.

## Pitfalls

- **Copies.** The algorithm assumes distinct vectors. With copies, a test $a_j \le b_j$ for all $j$ removes a copy of a nondominated vector, because the copy is not strictly worse. Remove copies first and give them back at the end, as the implementation does.
- **The order of ties in the sweep.** Line L9 must scan $A$ before $B$ when $x_k$ is equal. With $B$ first, a vector $b$ with $a_k = b_k$ and $a_{k+1} \le b_{k+1}$ is not removed, and the split of line L11 can send a pair that ties to the wrong call.
- **Sorting in every call.** A sort in each call adds a factor $\log n$ to every level. Keep the presorted lists and split them in linear time.
- **Maxima or minima.** The paper finds maxima. For minimized objectives, reverse all comparisons or negate the values, but do it for every coordinate.
- **A quadratic merge.** Some textbooks on evolutionary methods describe the method with a merge that compares each vector of $R_B$ with each vector of $R_T$. That version is correct, but its merge costs $O(p\, |R_T|\, |R_B|)$, and the bound of the paper is lost when the front is large.

## Implementations

## History

Kung, Luccio and Preparata posed the maxima problem in a model where the cost is the number of comparisons of two coordinates. Their paper of 1975 gave the divide and conquer algorithm, the bounds $O(n \log n)$ for $d = 2, 3$ and $O(n \log^{d-2} n)$ for $d \ge 4$, and the lower bound of $\lceil \log_2 n! \rceil$ comparisons for $d \ge 2$. Bentley, Kung, Schkolnick and Thompson studied the expected number of maxima in 1978. Bentley (1980) used the maxima problem as a main example of multidimensional divide and conquer, and Kirkpatrick and Seidel (1985) gave output-sensitive bounds. The algorithm entered evolutionary multi-objective optimization through textbooks such as Deb (2001), where it is called Kung's method, and Jensen (2003) extended it to non-dominated sorting.

## References
