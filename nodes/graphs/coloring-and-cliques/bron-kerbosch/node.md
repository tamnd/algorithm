---
tag: SFJ221
kind: algorithm
slug: bron-kerbosch
name: Bron-Kerbosch algorithm
aliases:
- Bron-Kerbosch with pivoting
area: graphs/coloring-and-cliques
level: core
summary: Backtracking enumeration of maximal cliques, with pivoting to prune the search.
solves: [maximal-clique-enumeration]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, d: the degeneracy}
  time: {worst: Θ(3^(n/3)), sparse: O(d n 3^(d/3))}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true}
prereqs: [clique, generic-backtracking-algorithm, adjacency-list]
see_also: [maximal-clique-enumeration, clique, maximum-clique, tomita-maximum-clique, carraghan-pardalos-algorithm, degeneracy-ordering, clique-number, maximal-clique]
sources:
  - paper: doi:10.1145/362342.362367
    title: Coen Bron and Joep Kerbosch, Algorithm 457, Finding all cliques of an undirected graph, Communications of the ACM 16(9), 575 to 577 (1973)
    locator: the whole paper (the sets compsub, candidates and not, the basic version and the version with a fixed point)
  - paper: doi:10.1016/j.tcs.2006.06.015
    title: Etsuji Tomita, Akira Tanaka and Haruhisa Takahashi, The worst-case time complexity for generating all maximal cliques and computational experiments, Theoretical Computer Science 363(1), 28 to 42 (2006)
    locator: the whole paper (the pivot with the most neighbors in P, and the O(3^(n/3)) bound)
  - paper: doi:10.1007/978-3-642-17517-6_36
    title: David Eppstein, Maarten Löffler and Darren Strash, Listing all maximal cliques in sparse graphs in near-optimal time, ISAAC 2010, LNCS 6506, 403 to 414
    locator: the whole paper (the outer loop in degeneracy order and the O(d n 3^(d/3)) bound)
  - paper: doi:10.1007/BF02760024
    title: J. W. Moon and L. Moser, On cliques in graphs, Israel Journal of Mathematics 3(1), 23 to 28 (1965)
    locator: the whole paper (at most 3^(n/3) maximal cliques, reached by K_(3,3,...,3))
---

The Bron-Kerbosch algorithm lists all maximal [cliques](/clique/) of an undirected graph by backtracking. It keeps three sets: the clique $R$ built so far, the candidates $P$ that can still extend $R$, and the excluded vertices $X$ that could extend $R$ but whose cliques were already listed. $R$ is reported when $P$ and $X$ are both empty. With the pivot rule of Tomita, Tanaka and Takahashi it runs in $O(3^{n/3})$ time, which matches the largest possible number of maximal cliques by the Moon-Moser theorem, and with an outer loop in [degeneracy](/degeneracy/) order it runs in $O(d\, n\, 3^{d/3})$ time.

## In plain words

You want every group of people in a network who all know each other and cannot be made larger. Build a group one person at a time. Keep a list of people who know everyone in the group so far: those are the candidates. When no candidate is left, the group may be complete, but only if nobody you set aside earlier could still join; otherwise you already listed a larger group that contains it.

The pivot is a shortcut. Pick a person who knows many of the candidates. Any complete group must contain this person or someone who does not know them, so you only need to start new branches from the candidates who do not know the pivot.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, as adjacency lists; $N(v)$ is the set of neighbors of $v$. The output is the list of all maximal cliques of $G$, each exactly once. A clique $K$ is maximal when no vertex outside $K$ is adjacent to all of $K$. The empty graph has one maximal clique, $\emptyset$. This is [maximal clique enumeration](/maximal-clique-enumeration/).

## The algorithm

```pseudo id=main
BRON-KERBOSCH(G)
L1  out ← an empty list
L2  EXPAND(∅, V, ∅)
L3  return out

EXPAND(R, P, X)        ▷ R is a clique, P ∪ X = the vertices adjacent to all of R
L4  if P = ∅ and X = ∅ then append R to out; return
L5  u ← a vertex of P ∪ X with the most neighbors in P
L6  for each v ∈ P \ N(u) do
L7      EXPAND(R ∪ {v}, P ∩ N(v), X ∩ N(v))
L8      P ← P \ {v}, X ← X ∪ {v}
```

Each call keeps the invariant that $R$ is a clique and that $P \cup X$ is exactly the set of vertices outside $R$ that are adjacent to every vertex of $R$. The vertices of $X$ were tried before, and every maximal clique that contains $R$ and a vertex of $X$ was listed already. If $P$ is empty but $X$ is not, $R$ is not maximal and has been covered, and the loop at L6 runs zero times. The original 1973 version branches on all of $P$; the pivot $u$ cuts the branches to $P \setminus N(u)$, because every maximal clique containing $R$ contains $u$ or a non-neighbor of $u$.

## Example

The graph has the vertices $0, \ldots, 6$ and the edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 06, 56$. The pivot is the vertex of $P \cup X$ with the most neighbors in $P$, ties to the smallest index, and branches go in increasing order. The rows are the calls in the order they start.

| call | $R$ | $P$ | $X$ | pivot $u$ | branches $P \setminus N(u)$ | result |
|---|---|---|---|---|---|---|
| 1 | {} | {0, 1, 2, 3, 4, 5, 6} | {} | 2 | 2, 5, 6 | |
| 2 | {2} | {0, 1, 3, 4} | {} | 1 | 1, 4 | |
| 3 | {1, 2} | {0, 3} | {} | 0 | 0, 3 | |
| 4 | {0, 1, 2} | {} | {} | | | report |
| 5 | {1, 2, 3} | {} | {} | | | report |
| 6 | {2, 4} | {3} | {} | 3 | 3 | |
| 7 | {2, 3, 4} | {} | {} | | | report |
| 8 | {5} | {3, 4, 6} | {} | 3 | 3, 6 | |
| 9 | {3, 5} | {4} | {} | 4 | 4 | |
| 10 | {3, 4, 5} | {} | {} | | | report |
| 11 | {5, 6} | {} | {} | | | report |
| 12 | {6} | {0} | {5} | 0 | 0 | |
| 13 | {0, 6} | {} | {} | | | report |

The output is $\{0,1,2\}, \{1,2,3\}, \{2,3,4\}, \{3,4,5\}, \{5,6\}, \{0,6\}$, the 6 maximal cliques. In call 6, vertex 1 is no longer a candidate: it moved to $X$ after call 3, and $X \cap N(4) = \emptyset$. In call 12, $X = \{5\}$ records that the cliques with 5 are done, so $\{6\}$ alone, or with 5, is not reported again. Without the pivot, the top call alone would branch on all 7 vertices.

## Correctness

**Theorem.** BRON-KERBOSCH$(G)$ terminates and appends to out each maximal clique of $G$ exactly once, and nothing else.

The proof is by the invariant of EXPAND$(R, P, X)$: $R$ is a clique, $P$ and $X$ are disjoint, and $P \cup X = \{ w \notin R : R \subseteq N(w) \}$. Then (i) every reported $R$ is maximal, because no vertex extends it when $P \cup X = \emptyset$; (ii) the call EXPAND$(R, P, X)$ reports exactly the maximal cliques $K$ with $R \subseteq K \subseteq R \cup P$, which do not meet $X$; and (iii) the branches at line L6 split these cliques into disjoint groups by the first branch vertex they contain, so each is reported once. The pivot is safe: a maximal clique $K \supseteq R$ with $K \subseteq R \cup P$ that contains no vertex of $P \setminus N(u)$ lies in $R \cup (P \cap N(u))$, so $u$ is adjacent to all of $K$ while $u \notin K$, which contradicts the maximality of $K$. The recursion terminates because $|P|$ strictly drops in each child. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model. The analysis of Tomita, Tanaka and Takahashi uses an adjacency matrix and counts set operations of $O(n)$ time each.

- **Worst case.** With the pivot of line L5, the total time is $O(3^{n/3})$ (Tomita, Tanaka and Takahashi 2006).
- **Lower bound.** By the Moon-Moser theorem, a graph on $n$ vertices has up to $3^{n/3}$ maximal cliques (the complete multipartite graph $K_{3, 3, \ldots, 3}$), so every algorithm that lists them needs $\Omega(3^{n/3})$ time in the worst case. The bound is optimal.
- **Sparse graphs.** Order the vertices by the [smallest-last ordering](/degeneracy-ordering/) $v_1, \ldots, v_n$. For each $v_i$, call EXPAND$(\{v_i\}, N(v_i) \cap \{v_{i+1}, \ldots, v_n\}, N(v_i) \cap \{v_1, \ldots, v_{i-1}\})$ with the Tomita pivot. Each $P$ has at most $d$ vertices, and the total time is $O(d\, n\, 3^{d/3})$ (Eppstein, Löffler and Strash 2010). This is optimal: some graphs of degeneracy $d$ have $(n - d)\, 3^{d/3}$ maximal cliques.
- **Space.** The recursion depth is at most $\omega(G) + 1$, and each level stores $P$ and $X$ with at most $n$ vertices, so $O(n^2)$ besides the output, or $O(n\, \omega)$.

There is no polynomial bound in terms of the output size for this method. Algorithms with polynomial delay between outputs exist; see [maximal clique enumeration](/maximal-clique-enumeration/).

## Properties

- **Each clique once.** The set $X$ prevents duplicates and non-maximal reports; this is the main idea of the 1973 paper.
- **Maximum clique as a by-product.** The largest reported clique is a maximum clique, but listing all maximal cliques to find it is wasteful; [branch and bound](/carraghan-pardalos-algorithm/) methods prune by size.
- **Complement.** Run on the complement, the algorithm lists all maximal [independent sets](/independent-set/).

## Variants and improvements

- **No pivot.** The basic version of Bron and Kerbosch branches on every vertex of $P$. It is correct, but it makes one call for each clique of $G$, not only for each maximal one: on $K_n$ it makes $2^n$ calls to report a single clique.
- **Pivot choices.** Bron and Kerbosch already chose a fixed point with many neighbors in $P$. Tomita, Tanaka and Takahashi take the maximum over $P \cup X$, which gives the worst-case bound. Cheaper pivot rules, such as a random vertex or the vertex of largest degree, keep correctness, but the worst-case bound is proved only for the rule of line L5.
- **Degeneracy order.** The outer loop of Eppstein, Löffler and Strash, above, is the method of choice for large sparse graphs.
- **Maximum clique.** Adding a bound $|R| + |P| \le$ best size so far, with coloring bounds, gives the [Tomita maximum clique](/tomita-maximum-clique/) algorithms and [Carraghan-Pardalos](/carraghan-pardalos-algorithm/).
- **Bit-parallel sets.** Storing $P$ and $X$ as bit vectors makes each set operation $O(n / w)$ on a machine with words of $w$ bits.

## When to use it

Use it when you need all maximal cliques, for example in community detection, in bioinformatics for clusters of interacting proteins, or as a step of algorithms on [chordal graphs](/chordal-graph/) and clique graphs. Use the degeneracy version for sparse graphs. Use a maximum clique algorithm instead when you only need one largest clique, and an algorithm for $k$-cliques when you only need cliques of a fixed size.

## Pitfalls

- **Forgetting $X$.** Without $X$, the algorithm reports non-maximal cliques, or the same maximal clique many times, once for each order of its vertices.
- **Not moving $v$ to $X$.** Line L8 must remove $v$ from $P$ and add it to $X$ after its branch. If only the removal from $P$ is done, later branches report cliques that are not maximal.
- **Pivot from $P$ only.** Taking the pivot from $P$ alone is correct, but the $3^{n/3}$ bound of Tomita, Tanaka and Takahashi is for the pivot from $P \cup X$.
- **Iterating over a set while changing it.** Line L6 loops over $P \setminus N(u)$, computed before the loop, while line L8 changes $P$. Iterate over a copy.
- **The empty graph.** With $n = 0$, the first call has $P = X = \emptyset$ and reports $\emptyset$. Code that expects at least one vertex in each clique must special-case this.

## Implementations

## History

Coen Bron and Joep Kerbosch published the algorithm in 1973 as Algorithm 457 of Communications of the ACM, with the basic version and a version with a fixed point that is an early form of the pivot. Tomita, Tanaka and Takahashi proved in 2006 that the pivot with the most neighbors in $P$ gives the optimal worst-case bound $O(3^{n/3})$. Eppstein, Löffler and Strash added the degeneracy order in 2010, and in 2011 Eppstein and Strash showed in experiments that it is fast on large real networks.

## References
