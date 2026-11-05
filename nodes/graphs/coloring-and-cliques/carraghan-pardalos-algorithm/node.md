---
tag: F3SXV2
kind: algorithm
slug: carraghan-pardalos-algorithm
name: Carraghan-Pardalos algorithm
aliases:
- Carraghan-Pardalos maximum clique
- Carraghan-Pardalos maximum clique algorithm
area: graphs/coloring-and-cliques
level: advanced
summary: Branch-and-bound search for a maximum clique by extending partial cliques one vertex at a time.
solves: [maximum-clique]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n 2^n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true}
prereqs: [maximum-clique, generic-backtracking-algorithm, adjacency-list]
see_also: [maximum-clique, tomita-maximum-clique, bron-kerbosch, clique-decision, clique-number, greedy-coloring, degeneracy-ordering, maximum-independent-set]
sources:
  - paper: doi:10.1016/0167-6377(90)90057-C
    title: Randy Carraghan and Panos M. Pardalos, An exact algorithm for the maximum clique problem, Operations Research Letters 9(6), 375 to 382 (1990)
    locator: the whole paper (vertices in order of increasing degree, partial enumeration with the size bound, and the computational results)
  - paper: doi:10.1016/S0166-218X(01)00290-6
    title: Patric R. J. Östergård, A fast algorithm for the maximum clique problem, Discrete Applied Mathematics 120(1-3), 197 to 207 (2002)
    locator: the whole paper (the search in reverse order with the bound c(i) on the largest clique among the last vertices)
  - url: https://arxiv.org/abs/1207.4616
    title: Patrick Prosser, Exact algorithms for maximum clique, a computational study, Algorithms 5(4), 545 to 587 (2012)
    locator: Section 2.1, MC (the basic algorithm with the cut |C| + |P| <= best, Listing 1.1)
  - url: https://leria-info.univ-angers.fr/~jinkao.hao/papers/WuHaoEJOR2014.pdf
    title: Qinghua Wu and Jin-Kao Hao, A review on algorithms for maximum clique problems, European Journal of Operational Research 242(3), 693 to 709 (2015)
    locator: Section 3, exact algorithms (Algorithm 1, the Carraghan-Pardalos algorithm, and its successors)
---

The Carraghan-Pardalos algorithm finds a [maximum clique](/maximum-clique/) of an undirected graph by [backtracking](/generic-backtracking-algorithm/). It grows a clique $C$ one vertex at a time from a list $P$ of candidates adjacent to all of $C$, and it abandons a branch as soon as $|C| + |P|$ is no larger than the best clique found so far. The vertices are taken in order of increasing degree. The bound is the simplest possible, but it prunes well on sparse and random graphs, and the method is the base of later solvers such as Östergård's algorithm and the coloring-bound algorithms of [Tomita](/tomita-maximum-clique/).

## In plain words

You want the largest group of people who all know each other. Start with an empty group and a list of people who could join. Add the first person from the list. The new list keeps only those who know that person. Go on until the list is empty, and remember the group if it is the largest so far.

Then go back and try the next person instead. Before you try anything, count: the group you have plus everyone still on the list. If that count is not more than your best group, nothing down this road can win, so stop and go back.

Starting with the people who know the fewest others keeps the early lists short.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given as adjacency lists. The output is a clique $K$ of $G$ of the largest size $\omega(G)$, the [clique number](/clique-number/). For $n = 0$ the output is the empty set. The decision form of the problem is [NP-complete](/clique-decision/), so no polynomial algorithm is expected.

## The algorithm

```pseudo id=main
CARRAGHAN-PARDALOS(G)
L1  P0 ← the vertices of G in order of non-decreasing degree, ties by index
L2  best ← ∅
L3  EXPAND(∅, P0)
L4  return best

EXPAND(C, P)        ▷ C is a clique, every vertex of P is adjacent to all of C
L5  while P is not empty do
L6      if |C| + |P| ≤ |best| then return
L7      v ← the first vertex of P; remove v from P
L8      Q ← the vertices of P adjacent to v, in the same order
L9      if Q is empty then (if |C| + 1 > |best| then best ← C ∪ {v})
L10     else EXPAND(C ∪ {v}, Q)
```

Because $v$ is removed from $P$ at line L7 before the next pass, each clique is built only from the vertices that follow its smallest vertex in the order, so no clique is visited twice. The top call first finds the largest clique that contains $P_0[1]$, then the largest that contains $P_0[2]$ but not $P_0[1]$, and so on. The cut at line L6 is the bound: every clique of this branch lies in $C \cup P$.

## Example

The graph has the vertices $0, \ldots, 7$ and the 13 edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 06, 56, 14, 67$. The degrees of $0, \ldots, 7$ are $3, 4, 4, 4, 4, 3, 3, 1$, so line L1 gives $P_0 = (7, 0, 5, 6, 1, 2, 3, 4)$. The rows are the passes of line L5, in the order they run; the depth is the number of vertices in $C$.

| depth | $C$ | $P$ at line L6 | $\lvert$best$\rvert$ | action |
|---|---|---|---|---|
| 0 | {} | 7, 0, 5, 6, 1, 2, 3, 4 | 0 | $v = 7$, $Q = (6)$, recurse |
| 1 | {7} | 6 | 0 | $v = 6$, $Q$ empty, best $\leftarrow \{7, 6\}$ |
| 0 | {} | 0, 5, 6, 1, 2, 3, 4 | 2 | $v = 0$, $Q = (6, 1, 2)$, recurse |
| 1 | {0} | 6, 1, 2 | 2 | $v = 6$, $Q$ empty, no change |
| 1 | {0} | 1, 2 | 2 | $v = 1$, $Q = (2)$, recurse |
| 2 | {0, 1} | 2 | 2 | $v = 2$, $Q$ empty, best $\leftarrow \{0, 1, 2\}$ |
| 1 | {0} | 2 | 3 | $1 + 1 \le 3$, cut |
| 0 | {} | 5, 6, 1, 2, 3, 4 | 3 | $v = 5$, $Q = (6, 3, 4)$, recurse |
| 1 | {5} | 6, 3, 4 | 3 | $v = 6$, $Q$ empty, no change |
| 1 | {5} | 3, 4 | 3 | $1 + 2 \le 3$, cut |
| 0 | {} | 6, 1, 2, 3, 4 | 3 | $v = 6$, $Q$ empty, no change |
| 0 | {} | 1, 2, 3, 4 | 3 | $v = 1$, $Q = (2, 3, 4)$, recurse |
| 1 | {1} | 2, 3, 4 | 3 | $v = 2$, $Q = (3, 4)$, recurse |
| 2 | {1, 2} | 3, 4 | 3 | $v = 3$, $Q = (4)$, recurse |
| 3 | {1, 2, 3} | 4 | 3 | $v = 4$, $Q$ empty, best $\leftarrow \{1, 2, 3, 4\}$ |
| 2 | {1, 2} | 4 | 4 | $2 + 1 \le 4$, cut |
| 1 | {1} | 3, 4 | 4 | $1 + 2 \le 4$, cut |
| 0 | {} | 2, 3, 4 | 4 | $0 + 3 \le 4$, cut |

The output is $\{1, 2, 3, 4\}$, and $\omega = 4$. The search makes 8 calls of EXPAND. The last row shows the effect of the order: once $\{1, 2, 3, 4\}$ is found, the 3 vertices left at the top cannot beat it, and the search ends without looking at them.

## Correctness

**Theorem.** CARRAGHAN-PARDALOS$(G)$ terminates and returns a clique of size $\omega(G)$.

Two facts give the proof. First, best is always a clique: line L9 sets it to $C \cup \{v\}$, where $C$ is a clique and $v \in P$ is adjacent to all of $C$, and line L8 keeps this property for the child call. Second, the call EXPAND$(C, P)$ leaves $|{\rm best}|$ at least the size of every clique $K$ with $C \subseteq K \subseteq C \cup P$. Split these cliques by their first vertex $p_j$ in $P$. Those with first vertex $p_j$ lie in $C \cup \{p_j\} \cup Q$, and the child call covers them by induction on $|P|$. A cut at line L6 is safe, because every remaining clique lies in $C \cup P$ and has at most $|C| + |P| \le |{\rm best}|$ vertices. At the top call this gives $|{\rm best}| \ge \omega(G)$. The order of line L1 matters only for speed. The full proof is below.

## Complexity

The costs are in the [word RAM](/word-ram/) model, with the neighbor sets stored so that adjacency is tested in $O(1)$ time.

- **Worst case.** Each call of EXPAND, and each pass of its loop, corresponds to a different clique $C \cup \{v\}$ of $G$, because vertices are added in the order of $P_0$. A graph has at most $2^n$ cliques, and each pass costs $O(n)$ at line L8, so the time is $O(n\, 2^n)$. Algorithms with a proven bound below $2^n$, such as the $O(2^{n/3})$ algorithms for [maximum independent set](/maximum-independent-set/) run on the complement, use more involved branching rules; see [clique decision](/clique-decision/).
- **Cost of the order.** Line L1 takes $O(n + m)$ time with counting sort, or $O(n \log n + m)$ with a comparison sort.
- **Space.** The recursion depth is at most $\omega(G)$, and each level stores a list $Q$ of at most $n$ vertices, so $O(n\, \omega) \subseteq O(n^2)$ besides the graph.
- **In practice.** The cut at line L6 prunes most of the tree on sparse and on random graphs. On dense graphs with a small $\omega$, such as complete multipartite graphs, the bound $|C| + |P|$ is weak and the search explores many cliques.

## Properties

- **Exact.** The result is always a maximum clique; the order and the tie-breaks affect only which one and how fast.
- **Anytime.** best is a clique at every moment, and its size only grows, so stopping early still gives a clique and the lower bound $|{\rm best}| \le \omega(G)$.
- **No duplicate work.** Each clique is visited at most once, as a prefix in the order $P_0$.
- **Complement.** Run on the complement graph, the algorithm finds a maximum [independent set](/independent-set/).

## Variants and improvements

- **Östergård's algorithm (2002).** Process the vertices from the last to the first, and store $c(i)$, the size of the largest clique among the vertices from $i$ on. A branch that starts at vertex $i$ with clique $C$ is cut when $|C| + c(i) \le |{\rm best}|$, a much stronger bound, and a run at vertex $i$ stops as soon as it finds a clique of size $c(i+1) + 1$.
- **Coloring bounds.** A proper coloring of $G[P]$ with $k$ colors shows that $P$ holds no clique of more than $k$ vertices, so $|C| + k \le |{\rm best}|$ is a valid cut that is never weaker than $|C| + |P|$. The MCQ and MCS algorithms of Tomita and coauthors color $P$ greedily at each node; see [Tomita's algorithm](/tomita-maximum-clique/).
- **Bit-parallel sets.** With $P$ as a bit vector, line L8 is one AND of $n/w$ words on a machine with $w$-bit words. Prosser's study compares this encoding (BBMC) with list-based versions.
- **Degeneracy order.** For large sparse graphs, the vertices are processed in [degeneracy order](/degeneracy-ordering/), so that each top-level candidate list has at most $d$ vertices, the [degeneracy](/degeneracy/).

## When to use it

Use it as a short, exact baseline for maximum clique on small or sparse graphs, or as the skeleton on which to add better bounds. For hard instances, such as the DIMACS benchmark graphs, prefer an algorithm with coloring bounds and bit sets. If you need all maximal cliques, use [Bron-Kerbosch](/bron-kerbosch/). If $k$ is fixed and small, check $k$-subsets directly.

## Pitfalls

- **Cut with the wrong inequality.** The test must be $|C| + |P| \le |{\rm best}|$, which allows a branch only if it can find a strictly larger clique. Using $<$ is still correct but explores branches that can only tie.
- **Cut once per call only.** The test must be made before every pass of the loop, since $P$ shrinks and best grows during the loop. Testing only at the start of the call prunes far less.
- **Forgetting to remove $v$.** Line L7 removes $v$ before the next pass. Without it, line L8 of later passes would include $v$ again, and the search would visit each clique once for every order of its vertices.
- **The empty graph.** With $n = 0$, the loop does not run, and the result is the empty clique.

## Implementations

## History

Randy Carraghan and Panos Pardalos published the algorithm in 1990 in Operations Research Letters, with a Fortran code and tests on random graphs. The method uses only a partial enumeration of the cliques, cut by the size bound, not a list of all of them. Östergård reversed the search order in 2002 and added the bound $c(i)$. Later solvers, starting with those of Tomita and coauthors, replaced the bound $|C| + |P|$ by greedy coloring bounds and stored the sets as bit vectors; Prosser (2012) compares these algorithms in one framework.

## References
