---
tag: B53EJC
kind: algorithm
slug: tomita-maximum-clique
name: Tomita's maximum clique algorithm
aliases:
- MCQ
- MCS
- Tomita coloring bound
area: graphs/coloring-and-cliques
level: advanced
summary: Maximum clique branch-and-bound that prunes with a greedy coloring upper bound.
solves: [maximum-clique]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(2^n n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true}
prereqs: [maximum-clique, greedy-coloring, depth-first-branch-and-bound]
see_also: [bron-kerbosch, maximal-clique-enumeration, clique-number, maximum-independent-set, welsh-powell-algorithm, dsatur]
sources:
  - paper: doi:10.1007/3-540-45066-1_22
    title: Etsuji Tomita and Tomokazu Seki, An efficient branch-and-bound algorithm for finding a maximum clique, Discrete Mathematics and Theoretical Computer Science, DMTCS 2003, Lecture Notes in Computer Science 2731, 278 to 289 (2003)
    locator: the algorithm MCQ (NUMBER-SORT and EXPAND) and its experiments
  - paper: doi:10.1007/s10898-006-9039-7
    title: Etsuji Tomita and Toshikatsu Kameda, An efficient branch-and-bound algorithm for finding a maximum clique with computational experiments, Journal of Global Optimization 37(1), 95 to 111 (2007)
    locator: the algorithm MCR (the initial order and the initial coloring numbers)
  - paper: doi:10.1007/978-3-642-11440-3_18
    title: Etsuji Tomita, Yoichi Sutani, Takanori Higashi, Shinya Takahashi and Mitsuo Wakatsuki, A simple and faster branch-and-bound algorithm for finding a maximum clique, WALCOM 2010, Lecture Notes in Computer Science 5942, 191 to 203 (2010)
    locator: the algorithm MCS (Re-NUMBER recoloring)
  - paper: "R. Carraghan and P. M. Pardalos, An exact algorithm for the maximum clique problem, Operations Research Letters 9(6), 375 to 382 (1990)"
    locator: the earlier branch and bound with the bound |Q| + |R|
---

Tomita's algorithm finds a [maximum clique](/maximum-clique/) by depth-first [branch and bound](/depth-first-branch-and-bound/). It keeps a current clique $Q$ and a set $R$ of candidates adjacent to all of $Q$, and bounds the best clique that can still be found by $|Q|$ plus the number of colors in a [greedy coloring](/greedy-coloring/) of $R$, because a clique uses each color at most once. Ordering $R$ by these colors lets one coloring give a bound for every branch at once. The first version, MCQ (Tomita and Seki 2003), and its successors MCR and MCS are among the fastest exact methods in practice, although the worst case stays exponential, as expected for an NP-hard problem.

## In plain words

To find the largest group of vertices that are all linked to each other, grow a group one vertex at a time and back up when stuck, keeping the best group found so far.

Most branches are hopeless, and the trick is to see that early. Color the remaining candidates so that linked candidates get different colors. A group can contain at most one candidate of each color, so if the group so far plus the number of colors cannot beat the best group, stop this branch. Try the candidates with the largest colors first, so the bound shrinks as you go.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$. The output is a clique $C$ with $|C| = \omega(G)$, the [clique number](/clique-number/). The problem is NP-hard and hard to approximate.

## The algorithm

$Q$ is the current clique, $R$ the candidate list, and $Q_{\max}$ the best clique so far. NUMBER-SORT colors $R$ greedily in its current order (each vertex takes the first class with no neighbor of it) and lists $R$ class by class, so that $\mathrm{col}[p]$ is non-decreasing along the list.

```pseudo id=main
TOMITA-MAX-CLIQUE(G)
L1  Qmax ← ∅
L2  EXPAND(∅, the vertices sorted by non-increasing degree)
L3  return Qmax

EXPAND(Q, R)
L4  NUMBER-SORT(R), which gives col[p] for each p ∈ R, sorted by color
L5  while R ≠ ∅ do
L6      p ← the last vertex of R
L7      if |Q| + col[p] ≤ |Qmax| then return
L8      R' ← R ∩ N(p)
L9      if R' = ∅ then (if |Q| + 1 > |Qmax| then Qmax ← Q ∪ {p})
L10     else EXPAND(Q ∪ {p}, R')
L11     R ← R \ {p}
```

Line L7 is the bound. All vertices left in $R$ have colors at most $\mathrm{col}[p]$, so a clique inside $R$ has at most $\mathrm{col}[p]$ vertices, and every later branch at this level is cut too, which is why the line returns rather than skipping one vertex. Line L8 keeps $R'$ in the order of $R$, and line L4 of the child call recolors it. Line L11 removes $p$ after its branch, so cliques that contain $p$ are not searched again.

## Example

Take the graph with 7 vertices and edges $01, 02, 03, 12, 13, 14, 23, 25, 36, 45, 56$. The degrees give the order $1, 2, 3, 0, 5, 4, 6$, and NUMBER-SORT colors it as $1 \to 1$, $2 \to 2$, $3 \to 3$, $0 \to 4$, $5 \to 1$, $4 \to 2$, $6 \to 2$.

| call | $Q$ | $R$ with colors | $p$ | action |
|---|---|---|---|---|
| 1 | $\emptyset$ | $1^1, 5^1, 2^2, 4^2, 6^2, 3^3, 0^4$ | 0 | $0 + 4 > 0$; $R' = \{1, 2, 3\}$ |
| 2 | $\{0\}$ | $1^1, 2^2, 3^3$ | 3 | $1 + 3 > 0$; $R' = \{1, 2\}$ |
| 3 | $\{0, 3\}$ | $1^1, 2^2$ | 2 | $2 + 2 > 0$; $R' = \{1\}$ |
| 4 | $\{0, 3, 2\}$ | $1^1$ | 1 | $R' = \emptyset$; $Q_{\max} = \{0, 1, 2, 3\}$ |
| 3 | $\{0, 3\}$ | $1^1$ | 1 | $2 + 1 \le 4$: return |
| 2 | $\{0\}$ | $1^1, 2^2$ | 2 | $1 + 2 \le 4$: return |
| 1 | $\emptyset$ | $1^1, 5^1, 2^2, 4^2, 6^2, 3^3$ | 3 | $0 + 3 \le 4$: return |

Superscripts are colors. After the first leaf, three bound checks end the whole search: the coloring proves that no clique with more than 4 vertices exists.

## Correctness

**Claim.** TOMITA-MAX-CLIQUE returns a maximum clique of $G$.

Every set stored in $Q_{\max}$ is a clique, because each vertex added to $Q$ comes from a candidate list whose members are adjacent to all of $Q$. For optimality, the invariant of EXPAND$(Q, R)$ is that every clique not yet searched that extends $Q$ lies in $Q \cup R$. A branch on $p$ searches all cliques of $Q \cup R$ that contain $p$, and line L11 then drops $p$. The cut at line L7 is safe because the color classes are independent sets, so a clique of $G[R]$ has at most $\mathrm{col}[p]$ vertices. The full proof is below.

## Complexity

**Time.** Each call of EXPAND has a different clique $Q$: the cliques are generated in a canonical order, since a vertex removed at line L11 never returns to a candidate list at that level or below. So there are at most $2^n$ calls. Line L4 takes $O(|R|^2)$ time and the loop $O(|R|)$ per step, so a call costs $O(n^2)$, and the worst case is $O(2^n n^2)$. The bound of line L7 does not improve the worst case as a function of $n$ in this analysis, but on most inputs it removes almost all of the tree.

**Space.** The recursion depth is at most $\omega(G) + 1$, and each level stores lists of $O(n)$ vertices, which gives $O(n \omega) \subseteq O(n^2)$ besides the graph.

## Properties

- **Exact.** It returns a clique of size $\omega(G)$.
- **Anytime.** $Q_{\max}$ is always a valid clique, so stopping early gives a lower bound, and the coloring gives an upper bound.
- **Coloring is a bound, not a solution.** Any proper coloring of $G[R]$ bounds the cliques in $R$; greedy coloring is cheap and usually close enough.
- **Order matters.** Expanding the vertex of largest color first makes the remaining list have small colors, so the cut fires early.

## Variants and improvements

- **MCR (Tomita and Kameda 2007).** A better initial order, with the vertices sorted by degree in a degeneracy-like way, and initial color numbers taken from this order instead of a first coloring.
- **MCS (Tomita et al. 2010).** *Re-NUMBER*: when a vertex gets a color above the threshold that matters for the cut, try to move it to a lower class by swapping with a vertex of that class, which tightens the bound for little cost.
- **Bit-parallel versions.** San Segundo and others store $R$ and the color classes as bitsets, so NUMBER-SORT runs word by word.
- **MaxSAT bounds.** Li and Quan refine the coloring bound by finding sets of color classes that cannot all contribute, as in MaxSAT reasoning, which often removes one or more from the bound.
- **Maximum independent set.** Run on the [complement](/complement-graph/) to find a [maximum independent set](/maximum-independent-set/).

## When to use it

Use it when an exact maximum clique is needed in a graph of up to a few thousand vertices, or in sparse graphs much larger than that, after reducing by the degeneracy order. On the complement it finds maximum independent sets, which suits dense graphs whose complement is sparse. For listing all maximal cliques, use [Bron-Kerbosch](/bron-kerbosch/) instead.

## Pitfalls

- **Skipping instead of returning at line L7.** Because $R$ is sorted by color, the first failed check means that all the remaining vertices fail. Continuing the loop is correct but wastes time.
- **Recoloring in the wrong order.** NUMBER-SORT must list the vertices class by class with non-decreasing colors, and the loop must take vertices from the end. Taking them from the front breaks the argument that the cut covers all later branches.
- **Bound off by one.** The test is $|Q| + \mathrm{col}[p] \le |Q_{\max}|$; using $<$ explores branches that cannot improve the result.
- **Forgetting to drop $p$.** Without line L11, cliques through $p$ are searched again from later vertices.

## Implementations

## History

Carraghan and Pardalos published a simple branch and bound with the bound $|Q| + |R|$ in 1990. Tomita and Seki replaced $|R|$ by the number of colors in a greedy coloring and ordered the search by these colors in 2003, giving MCQ. Tomita and Kameda improved the initial order in MCR (2007), and Tomita, Sutani, Higashi, Takahashi and Wakatsuki added recoloring in MCS (2010). Bit-parallel and MaxSAT-based refinements followed in the 2010s.

## References
