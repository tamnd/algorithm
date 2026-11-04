---
tag: X3NDEJ
kind: algorithm
slug: held-karp-algorithm
name: Held-Karp algorithm
aliases:
- Bellman-Held-Karp algorithm
- Held-Karp dynamic programming
- bitmask TSP DP
area: techniques/dynamic-programming
level: advanced
summary: Solve the exact travelling salesman problem in O(n^2 2^n) time by DP over subsets.
solves: [traveling-salesman-problem]
model: word-ram
complexity:
  vars: {n: the number of cities}
  time: {worst: Θ(n^2 2^n), average: Θ(n^2 2^n), best: Θ(n^2 2^n)}
  space: {extra: Θ(n 2^n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1962
  people: [Richard Bellman, Michael Held, Richard M. Karp]
  note: Bellman and, independently, Held and Karp published the subset dynamic program for the travelling salesman problem in 1962.
prereqs: [traveling-salesman-problem, bitmask-dp, optimal-substructure]
see_also: [bitmask-dp, hamiltonian-cycle, hamiltonian-path-problem, exact-exponential-algorithms, bitonic-tsp, traveling-salesman-decision, sum-over-subsets-dp]
sources:
  - paper: doi:10.1137/0110015
    title: Michael Held and Richard M. Karp, A dynamic programming approach to sequencing problems, Journal of the Society for Industrial and Applied Mathematics 10(1), 196-210, 1962
    locator: the travelling salesman recurrence over subsets and its operation count
  - paper: doi:10.1145/321105.321111
    title: Richard Bellman, Dynamic programming treatment of the travelling salesman problem, Journal of the ACM 9(1), 61-63, 1962
    locator: the whole note (the functional equation over subsets)
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Chapter 6, Section 6.6, The traveling salesman problem
---

The Held-Karp algorithm solves the [travelling salesman problem](/traveling-salesman-problem/) exactly. For each set $S$ of cities and each city $j \in S$, it computes the length of a shortest path that starts at a fixed city, visits exactly the cities of $S$, and ends at $j$. This is [bitmask dynamic programming](/bitmask-dp/): there are $\Theta(n 2^n)$ states and each takes $O(n)$ time, so the total is $\Theta(n^2 2^n)$ time and $\Theta(n 2^n)$ space. Trying all tours takes $(n-1)!$ steps, so the gain is large, but the time is still exponential, as expected for an [NP-hard](/np-hard/) problem.

## In plain words

A salesman starts at home, must visit every other city once, and must come back home. He wants the shortest trip.

Look at a trip in the middle. Two facts matter for the rest of the trip: which cities he has already seen, and where he is now. The order in which he saw them does not matter any more. So for each group of cities and each last city, we store the length of the shortest way to visit that group and stop at that city.

We fill these numbers for groups of one city, then for groups of two, and so on. A shortest way to a group that ends at a city comes from a shortest way to the same group without that city, plus one last road. At the end we add the road back home and take the best.

## The problem

The input is a number $n \ge 1$ of cities $0, 1, \ldots, n-1$ and a matrix of distances $d(i, j) \ge 0$ for $i \ne j$. The matrix need not be symmetric. A tour is a cyclic order $0 = v_0, v_1, \ldots, v_{n-1}$ of all the cities, and its length is

$$L(v) = \sum_{t=0}^{n-2} d(v_t, v_{t+1}) + d(v_{n-1}, v_0).$$

The output is a tour of least length. Each tour visits city 0, so we fix it as the start. For $n = 1$ the tour has no edges and its length is 0.

## The algorithm

Let $V = \{1, \ldots, n-1\}$. For a nonempty $S \subseteq V$ and $j \in S$, let $C(S, j)$ be the length of a shortest path that starts at 0, visits each city of $S$ exactly once, visits no other city, and ends at $j$. Then

$$C(\{j\}, j) = d(0, j), \qquad C(S, j) = \min_{i \in S \setminus \{j\}} \bigl( C(S \setminus \{j\}, i) + d(i, j) \bigr) \text{ for } |S| \ge 2,$$

and the length of a shortest tour is $\min_{j \in V} \bigl( C(V, j) + d(j, 0) \bigr)$. A set $S$ is stored as the integer mask with bit $j - 1$ set for each $j \in S$. The mask of $S \setminus \{j\}$ is smaller than the mask of $S$, so a scan of the masks in increasing order computes each entry after the entries it needs.

```pseudo id=main
HELD-KARP(d, n)                              ▷ cities 0 .. n − 1, start at 0
L1  if n = 1 then return (0, [0])
L2  for j ← 1 to n − 1 do C[{j}, j] ← d(0, j), P[{j}, j] ← 0
L3  for each S ⊆ V with |S| ≥ 2, in increasing order of mask do
L4      for each j ∈ S do
L5          C[S, j] ← min over i ∈ S − {j} of C[S − {j}, i] + d(i, j)
L6          P[S, j] ← an i that attains the minimum of line L5
L7  best ← min over j ∈ V of C[V, j] + d(j, 0), and last ← a j that attains it
L8  S ← V, j ← last, tour ← [ ]
L9  while j ≠ 0 do
L10     put j at the front of tour
L11     (S, j) ← (S − {j}, P[S, j])
L12 return (best, [0] + tour)
```

Lines L2 to L6 fill the table. Line L6 keeps the predecessor of $j$ on a best path, so lines L8 to L11 walk back from the last city to city 0 and rebuild the tour. The walk stops when the predecessor is 0, which is the case exactly for the one-city sets of line L2.

## Example

Take $n = 4$ with the asymmetric matrix below. Row $i$ holds $d(i, 0), \ldots, d(i, 3)$.

| | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | 0 | 2 | 9 | 10 |
| 1 | 1 | 0 | 6 | 4 |
| 2 | 15 | 7 | 0 | 8 |
| 3 | 6 | 3 | 12 | 0 |

The table, written as $C(S, j)$ with the predecessor $P(S, j)$ in brackets, is:

| $S$ | $j = 1$ | $j = 2$ | $j = 3$ |
|---|---|---|---|
| $\{1\}$ | 2 (0) | | |
| $\{2\}$ | | 9 (0) | |
| $\{3\}$ | | | 10 (0) |
| $\{1, 2\}$ | 16 (2) | 8 (1) | |
| $\{1, 3\}$ | 13 (3) | | 6 (1) |
| $\{2, 3\}$ | | 22 (3) | 17 (2) |
| $\{1, 2, 3\}$ | 20 (3) | 18 (3) | 16 (2) |

For example, $C(\{1, 2, 3\}, 1) = \min(C(\{2, 3\}, 2) + d(2, 1),\ C(\{2, 3\}, 3) + d(3, 1)) = \min(22 + 7, 17 + 3) = 20$. Line L7 compares $20 + 1 = 21$, $18 + 15 = 33$ and $16 + 6 = 22$, so the best length is 21 with last city 1. The walk back reads $P(\{1,2,3\}, 1) = 3$, $P(\{2, 3\}, 3) = 2$ and $P(\{2\}, 2) = 0$. The tour is $0, 2, 3, 1, 0$, with length $9 + 8 + 3 + 1 = 21$. A check of all $3! = 6$ tours gives the same minimum.

## Correctness

The key claim is that $C(S, j)$ equals the shortest length of a path from 0 through exactly the cities of $S$ to $j$. The proof is by induction on $|S|$. A path through $S$ that ends at $j$, with $|S| \ge 2$, is a path through $S \setminus \{j\}$ that ends at some $i$, followed by the edge $(i, j)$. Its prefix can be replaced by a shortest one without changing the set of visited cities, which is the [cut-and-paste argument](/cut-and-paste-argument/). A tour is such a path through $V$ plus the edge back to 0, so line L7 gives the optimum. The full proof, with the reconstruction of lines L8 to L11, is in the proof file below.

## Complexity

Count the work of line L5. For a set $S$ of size $s$, there are $s$ choices of $j$ and $s - 1$ choices of $i$. So the number of terms is

$$\sum_{s=2}^{n-1} \binom{n-1}{s} s (s-1) = (n-1)(n-2)\, 2^{n-3} \quad (n \ge 3).$$

The identity follows from $\binom{m}{s} s (s-1) = m(m-1)\binom{m-2}{s-2}$ with $m = n - 1$, and $\sum_{s} \binom{m-2}{s-2} = 2^{m-2}$. Each term takes $O(1)$ time on a [word RAM](/word-ram/) with the distances as words. So the time is $\Theta(n^2 2^n)$, and it is the same for each input: the algorithm has no early exit. The tables $C$ and $P$ have $(n-1) 2^{n-2}$ useful entries each, so the space is $\Theta(n 2^n)$. With arrays indexed by the full mask, the program uses $(n-1) 2^{n-1}$ cells, which is the same order. The rebuild of lines L8 to L11 takes $O(n)$ time.

For $n = 20$, the count is $19 \cdot 18 \cdot 2^{17} = 44{,}826{,}624$ terms, while $19!$ is about $1.2 \cdot 10^{17}$.

The space, not the time, is often the limit in practice. For $n = 30$, the table has about $1.6 \cdot 10^{10}$ entries.

## Properties

- **Exact.** It returns an optimal tour, not an approximation.
- **No assumption on the distances.** The matrix may be asymmetric and need not satisfy the triangle inequality. Negative distances also work, since each tour has exactly $n$ edges.
- **Not input-sensitive.** It does the same work on each input with $n$ cities.
- **Iterative.** It needs no recursion. The masks are the loop counter.

## Variants and improvements

- **Hamiltonian path or cycle.** With Boolean values instead of lengths, the same table decides whether a [Hamiltonian path](/hamiltonian-path-problem/) or a [Hamiltonian cycle](/hamiltonian-cycle/) exists, in $O(n^2 2^n)$ time. A bitset row per set cuts this to $O(n 2^n)$ word operations.
- **Paths with free ends.** Drop the edge back to 0 and start from every city to get a shortest Hamiltonian path.
- **Sequencing problems.** Held and Karp state the method for a family of sequencing problems in which the cost of the next job depends on the set of jobs done and on the last job. The travelling salesman problem is one member.
- **Polynomial space.** An inclusion-exclusion count over subsets decides Hamiltonicity in $O^*(2^n)$ time and polynomial space. See [exact exponential algorithms](/exact-exponential-algorithms/).
- **Pruning.** Practical exact solvers use branch and cut with linear programming bounds, which handle instances with thousands of cities.

## When to use it

Use it for exact answers with up to about 20 to 25 cities, or as a subroutine for small groups inside a larger heuristic. It is simple and has a guaranteed bound. For larger instances, use branch and cut for exact answers, or an approximation such as the [MST heuristic](/mst-tsp-heuristic/) for metric distances. When the points are on a line in the plane and the tour may only go right and then left, the [bitonic tour](/bitonic-tsp/) problem has an $O(n^2)$ algorithm.

## Pitfalls

- **Wrong fill order.** Line L3 must compute $C(S \setminus \{j\}, \cdot)$ before $C(S, \cdot)$. Increasing mask order or increasing size both work. An order by the last city $j$ does not.
- **City 0 inside the mask.** If the mask also holds city 0, the table doubles and the base case of line L2 becomes unclear. Keep 0 outside $V$.
- **Infinite values.** For a matrix with missing edges stored as infinity, use a large sentinel and keep it from overflowing when line L5 adds a distance to it.
- **The size $n = 1$ or $n = 2$.** For $n = 1$, line L1 returns 0. For $n = 2$, the tour is $0, 1, 0$ and its length is $d(0,1) + d(1,0)$, which lines L2 and L7 give with no pass of line L3.

## Implementations

## History

Richard Bellman published the subset recurrence for the travelling salesman problem in the Journal of the ACM in January 1962. Michael Held and Richard Karp published it in March 1962 in the Journal of SIAM, as one case of a dynamic programming approach to sequencing problems, with the operation count. The two works were independent, and the method is called the Bellman-Held-Karp algorithm for this reason. No algorithm for the general problem with arbitrary distances and $O(c^n)$ time for a constant $c < 2$ is known.

## References
