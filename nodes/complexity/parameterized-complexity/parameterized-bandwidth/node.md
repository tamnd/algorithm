---
tag: FWH12V
kind: problem
slug: parameterized-bandwidth
name: Parameterized bandwidth
aliases:
- bandwidth
area: complexity/parameterized-complexity
level: research
summary: "Decide whether a graph has a vertex layout of bandwidth at most k, with parameter k. NP-complete on trees, in XP by an O(n^k) algorithm, and W[t]-hard for every t."
prereqs: [xp, w-hardness, path-decomposition]
see_also: [bandwidth-reduction, reverse-cuthill-mckee, w-hierarchy, treewidth, fpt-approximation, gaussian-elimination, strong-exponential-time-hypothesis, np-complete]
sources:
  - paper: doi:10.1137/0134037
    title: "Michael R. Garey, Ronald L. Graham, David S. Johnson and Donald E. Knuth, Complexity results for bandwidth minimization, SIAM Journal on Applied Mathematics 34(3), 477-495 (1978)"
    locator: NP-completeness of bandwidth on trees, and a linear-time test for bandwidth 2
  - paper: doi:10.1137/0601042
    title: "James B. Saxe, Dynamic-programming algorithms for recognizing small-bandwidth graphs in polynomial time, SIAM Journal on Algebraic and Discrete Methods 1(4), 363-369 (1980)"
    locator: the dynamic program, polynomial time for each fixed k with n^(k+1) in the bound
  - paper: doi:10.1016/0196-6774(84)90006-3
    title: "Eitan M. Gurari and Ivan Hal Sudborough, Improved dynamic programming algorithms for bandwidth minimization and the MinCut Linear Arrangement problem, Journal of Algorithms 5(4), 531-546 (1984)"
    locator: the O(n^k) algorithm for bandwidth at most k
  - paper: doi:10.1145/195058.195229
    title: "Hans L. Bodlaender, Michael R. Fellows and Michael T. Hallett, Beyond NP-completeness for problems of bounded width: hardness for the W hierarchy, STOC 1994, 449-458"
    locator: "bandwidth is W[t]-hard for every t, also on trees"
  - paper: arxiv:1404.7810
    title: "Markus Sortland Dregi and Daniel Lokshtanov, Parameterized complexity of bandwidth on trees, ICALP 2014, LNCS 8572, 405-416"
    locator: "no f(b) n^o(b) algorithm on trees of pathwidth at most 2 unless ETH fails, W[1]-hardness on these trees, and a polynomial-time algorithm on trees that returns a layout of bandwidth b^O(b) or proves bandwidth greater than b"
---

Bandwidth asks for an ordering of the vertices of a graph on a line such that the two ends of every edge are close. The parameter is the bound $k$ on the stretch of an edge. The problem is NP-complete even on trees, and for every fixed $k$ it is solvable in polynomial time, in time $O(n^k)$ by Gurari and Sudborough, so it is in XP. But it is W[t]-hard for every $t$, so it is not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$. This page is about the parameterized decision problem; [bandwidth reduction](/bandwidth-reduction/) is the numerical task of reordering a sparse matrix, mostly by heuristics.

## In plain words

Put the vertices of a graph in a row, one per slot. Each edge then has a length: how many slots apart its two ends are. The bandwidth is the smallest possible length of the longest edge, over all orders. The question is whether some order keeps every edge at most a given length. When that length is a fixed small number, a table-filling method that remembers the last few placed vertices solves the problem. But the number of states grows like the graph size raised to the power of that length. Strong evidence from parameterized complexity says that this power cannot be removed, even when the graph is a tree.

## Definition

A *layout* of a graph $G$ with $n$ vertices is a bijection $\pi : V(G) \to \{1, \dots, n\}$. Its bandwidth is $\max_{uv \in E(G)} |\pi(u) - \pi(v)|$, and the bandwidth $\mathrm{bw}(G)$ is the least bandwidth of a layout.

- Instance: a graph $G$ given as adjacency lists, and an integer $k$.
- Parameter: $k$.
- Question: Is $\mathrm{bw}(G) \le k$?

For a symmetric matrix $A$, the bandwidth of $A$ under a symmetric permutation of rows and columns is the bandwidth of the graph whose edges are the nonzero entries off the diagonal. So this problem and [bandwidth reduction](/bandwidth-reduction/) ask the same question. The difference is the point of view: here the question is the exact complexity in terms of $k$; there the goal is a good order for [Gaussian elimination](/gaussian-elimination/) on a banded matrix, found quickly by heuristics such as [reverse Cuthill-McKee](/reverse-cuthill-mckee/).

## Variants

- **Fixed $k$.** For each fixed $k$, "is $\mathrm{bw}(G) \le k$?" is a separate problem in P. Garey, Graham, Johnson and Knuth (1978) gave a linear-time test for $k = 2$.
- **Trees.** The problem stays NP-complete on trees (Garey, Graham, Johnson and Knuth 1978), and W[t]-hard for every $t$ on trees (Bodlaender, Fellows and Hallett 1994).
- **Approximation in FPT time.** On trees, Dregi and Lokshtanov (2014) give a polynomial-time algorithm that either proves $\mathrm{bw}(T) > b$ or returns a layout of bandwidth $b^{O(b)}$. This is an [FPT approximation](/fpt-approximation/) with a ratio that depends on $b$ only.

## Examples

The bandwidth values come from an exact backtracking search. The two lower bounds are proved under Bounds; $\Delta$ is the maximum degree and $\mathrm{diam}$ the diameter. The treewidth comes from an exact computation.

| graph | $n$ | $\mathrm{bw}$ | $\lceil \Delta / 2 \rceil$ | $\lceil (n-1)/\mathrm{diam} \rceil$ | treewidth |
|---|---|---|---|---|---|
| path $P_5$ | 5 | 1 | 1 | 1 | 1 |
| star $K_{1,6}$ | 7 | 3 | 3 | 3 | 1 |
| cycle $C_6$ | 6 | 2 | 1 | 2 | 2 |
| 3 by 3 grid | 9 | 3 | 2 | 2 | 3 |
| 3 by 4 grid | 12 | 3 | 2 | 3 | 3 |
| complete binary tree | 7 | 2 | 2 | 2 | 1 |
| complete binary tree | 15 | 3 | 2 | 3 | 1 |
| Petersen graph | 10 | 5 | 2 | 5 | 4 |

The star and the binary trees show that bandwidth can be much larger than treewidth. The 3 by 3 grid shows that neither simple lower bound is always tight. The row-major layout of the 3 by 3 grid has bandwidth 3, which is optimal.

## Known algorithms

- Saxe (1980) decides $\mathrm{bw}(G) \le k$ by dynamic programming in time polynomial for each fixed $k$, with $n^{k+1}$ in the bound, on a RAM.
- Gurari and Sudborough (1984) lower the time to $O(n^k)$ for each fixed $k$, on a RAM.
- For $k = 2$, Garey, Graham, Johnson and Knuth (1978) give a linear-time algorithm.
- On trees, Dregi and Lokshtanov (2014) give the polynomial-time approximation with ratio $b^{O(b)}$ described under Variants.

In practice, sparse matrix codes use heuristics such as [reverse Cuthill-McKee](/reverse-cuthill-mckee/) with no guarantee; see [bandwidth reduction](/bandwidth-reduction/).

## Bounds

- **NP-complete**, under polynomial-time many-one reductions, already on trees (Garey, Graham, Johnson and Knuth 1978). Membership in NP: the certificate is the layout.
- **In XP**, by the $O(n^k)$ algorithm. Since FPT is a proper subset of XP, membership in XP alone does not give FPT.
- **W[t]-hard for every $t$** (Bodlaender, Fellows and Hallett 1994), under parameterized reductions, also on trees. In particular it is [W[1]-hard](/w-hardness/), so it is not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$.
- **ETH lower bound.** Dregi and Lokshtanov (2014) proved that there is no algorithm in time $f(k) \cdot n^{o(k)}$ for any computable $f$, even on trees of pathwidth at most 2, unless ETH fails. So the $O(n^k)$ algorithm is optimal up to the constant in the exponent, under ETH. This bound is separate from the W-hardness; see [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) for ETH.
- **Lower bounds on the value.** For every graph, $\mathrm{bw}(G) \ge \lceil \Delta/2 \rceil$: a vertex of degree $\Delta$ has all neighbors within distance $\mathrm{bw}$ on each side, and there are at most $2\,\mathrm{bw}$ such slots. Also $\mathrm{bw}(G) \ge \lceil (n-1)/\mathrm{diam}(G) \rceil$ for connected $G$: the vertices in slots 1 and $n$ are joined by a path of at most $\mathrm{diam}$ edges, each edge covers at most $\mathrm{bw}$ slots, so $n - 1 \le \mathrm{bw} \cdot \mathrm{diam}$.
- **Bandwidth bounds pathwidth.** A layout of bandwidth $k$ gives a [path decomposition](/path-decomposition/) of width at most $k$: take the bags $\{\pi^{-1}(i), \dots, \pi^{-1}(i + k)\}$ for $i = 1, \dots, n - k$. Each edge $uv$ with $\pi(u) < \pi(v)$ lies in the bag that starts at $\min(\pi(u), n - k)$, and each vertex lies in consecutive bags. So $\mathrm{tw}(G) \le \mathrm{pw}(G) \le \mathrm{bw}(G)$, and every problem that is FPT in the [treewidth](/treewidth/) is FPT in the bandwidth.

## Reductions

- **From weighted circuit satisfiability.** Bodlaender, Fellows and Hallett reduce weighted satisfiability of circuits of weft $t$ to bandwidth by parameterized reductions, for every $t$. This gives the W[t]-hardness; see the [W-hierarchy](/w-hierarchy/).
- **To and from matrix bandwidth.** A graph and the symmetric 0/1 matrix of its adjacency (with a nonzero diagonal) have the same bandwidth. This is a linear-time equivalence in both directions, and it keeps $k$.
- **To treewidth problems.** Because $\mathrm{tw}(G) \le \mathrm{bw}(G)$, the layout itself is a path decomposition, so a problem with a dynamic program on path decompositions runs on a bandwidth-$k$ layout directly.

## Applications

- **Banded linear systems.** Gaussian elimination without pivoting and Cholesky factorization on a matrix of bandwidth $k$ produce no fill outside the band, so they take $O(n k^2)$ time and $O(n k)$ space. This is the main reason to reorder sparse matrices; see [bandwidth reduction](/bandwidth-reduction/).
- **Layout of circuits and graphs.** Placing components in a line with short wires leads to the same question.
- **A test case for the W-hierarchy.** Bandwidth was an early natural problem shown hard for every level of the W-hierarchy. It shows that a problem can be in P for each fixed $k$ and still not be FPT under standard assumptions.

## References
