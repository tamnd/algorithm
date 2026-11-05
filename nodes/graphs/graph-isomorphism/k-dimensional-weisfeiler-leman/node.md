---
tag: G42WBZ
kind: algorithm
slug: k-dimensional-weisfeiler-leman
name: k-dimensional Weisfeiler-Leman algorithm
aliases:
- k-WL
- Weisfeiler-Leman hierarchy
area: graphs/graph-isomorphism
level: advanced
summary: Refines colorings of k-tuples of vertices; higher k distinguishes more graphs but costs more time.
solves: [graph-isomorphism-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, k: the dimension}
  time: {worst: O(k n^(2k+1) log n), best: O(k n^(k+1) log n)}
  space: {extra: O(k n^(k+1))}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [weisfeiler-leman, partition-refinement, isomorphism-invariant]
see_also: [cai-furer-immerman-construction, weisfeiler-leman, individualization-refinement, babai-quasipolynomial-algorithm, planar-graph-isomorphism, equitable-partition, nauty]
sources:
  - paper: doi:10.1007/BF01305232
    title: Jin-Yi Cai, Martin Fürer and Neil Immerman, An optimal lower bound on the number of variables for graph identification, Combinatorica 12(4), 389 to 410 (1992)
    locator: Sections 4 to 6 (k-WL, its equivalence with counting logic and pebble games, and the CFI lower bound)
  - paper: "Neil Immerman and Eric Lander, Describing graphs: a first-order approach to graph canonization, in Complexity Theory Retrospective, Springer, 1990, 59 to 81"
    locator: the whole chapter (the counting logics C^k, the k-WL refinement, and its running time)
  - paper: "Boris Weisfeiler and Andrei Leman, The reduction of a graph to canonical form and the algebra which appears therein, Nauchno-Technicheskaya Informatsia, Series 2, 9, 12 to 16 (1968)"
    locator: the whole paper (the refinement of colorings of vertex pairs, the 2-dimensional case)
  - paper: doi:10.1145/2371656.2371662
    title: Martin Grohe, Fixed-point definability and polynomial time on graphs with excluded minors, Journal of the ACM 59(5), article 27 (2012)
    locator: the introduction (graph classes identified by k-WL for a fixed k)
---

The $k$-dimensional Weisfeiler-Leman algorithm ($k$-WL) colors all $k$-tuples of vertices of a graph and refines the colors until they are stable, in the same way as [color refinement](/weisfeiler-leman/) refines colors of single vertices. Two graphs whose stable color histograms differ are not isomorphic; the converse fails, but it holds for more and more graphs as $k$ grows, and $k = n - 1$ identifies every graph on $n$ vertices. The case $k = 2$ is the original 1968 algorithm of Weisfeiler and Leman. Each round costs about $n^{k+1}$ steps, so $k$-WL runs in polynomial time for each fixed $k$; Cai, Fürer and Immerman (1992) showed that no fixed $k$ suffices for all graphs.

## In plain words

Color refinement looks at single points and their neighbors. Some networks look the same from every single point, even when they differ. The idea of $k$-WL is to look at groups of $k$ points in order. Each group starts with a color that says which of its points are equal and which are linked. Then, again and again, a group gets a new color from its old color and from the colors of all groups made by swapping one of its points for another point. When no color splits any more, you compare how many groups of each color the two networks have. A larger $k$ sees more structure but needs far more work.

## The problem

The input is two simple undirected graphs $G$ and $H$ with $n$ vertices each, with optional vertex colors that isomorphisms must keep; directed and edge-colored graphs only change the atomic types. The output is "distinguished", which proves $G \not\cong H$, or "not distinguished", which does not prove isomorphism. The same refinement on one graph gives a stable coloring of $V^k$ that is an [isomorphism invariant](/isomorphism-invariant/).

This page uses the convention of Cai, Fürer and Immerman and of Grohe: for $k \ge 2$, $k$-WL has the same power as the counting logic $C^{k+1}$ with $k + 1$ variables, and 1-WL is color refinement. Papers in machine learning call this version folklore $k$-WL ($k$-FWL) and use "$k$-WL" for a weaker oblivious version; check the convention before comparing statements.

## The algorithm

For a tuple $t = (t_1, \ldots, t_k)$ and a vertex $w$, $t[i/w]$ is $t$ with $t_i$ replaced by $w$.

```pseudo id=main
KWL(G, k)
L1  for each t in V^k: χ(t) ← atomic type of t (colors of t_i; whether t_i = t_j; whether t_i t_j is an edge)
L2  repeat
L3      for each t in V^k: σ(t) ← (χ(t), multiset over w in V of (χ(t[1/w]), ..., χ(t[k/w])))
L4      χ' ← rank of σ(t) in the sorted list of all signatures
L5      if χ' has as many classes as χ then stop, else χ ← χ'
L6  return χ
```

To compare $G$ and $H$, both are refined in parallel with one shared sorted list of signatures, and they are distinguished as soon as the histograms of colors differ in some round.

## Example

2-WL on the cycle $C_6$ (vertices $0, \ldots, 5$). There are 36 pairs.

| round | classes of pairs $(u, v)$ | sizes |
|---|---|---|
| 0, atomic types | $u = v$; $uv$ an edge; $u \ne v$ not an edge | 6, 12, 18 |
| 1 | $u = v$; distance 1; distance 2; distance 3 | 6, 12, 12, 6 |
| 2 | no change, stop | |

In round 1 a non-adjacent pair $(u, v)$ sees, among the 6 choices of $w$, the number of $w$ with $(w, v)$ and $(u, w)$ both edges, which is the number of common neighbors: 1 at distance 2 and 0 at distance 3. On the disjoint union $2K_3$ the non-adjacent pairs have no common neighbors at all, so the histograms differ and 2-WL distinguishes $C_6$ from $2K_3$, which color refinement cannot do.

The $4 \times 4$ rook's graph and the Shrikhande graph are both strongly regular with parameters $(16, 6, 2, 2)$. 2-WL gives each of them 3 classes of pairs, of sizes 16, 96 and 144, already stable, so it does not distinguish them. 3-WL colors $16^3 = 4096$ triples: the rook's graph is stable at 15 classes after round 0, while the Shrikhande graph reaches 31 classes after 2 rounds, so 3-WL distinguishes them. (The rook's graph contains 8 copies of $K_4$ and the Shrikhande graph none, which 4-variable counting logic can express.)

## Correctness

The [full proof](proofs/correctness.md) has two parts.

- **Termination.** The new color includes the old one, so each round refines the partition of $V^k$. A round that does not increase the number of classes leaves the partition unchanged, and then all later rounds do too. So there are at most $n^k$ rounds.
- **Soundness.** An isomorphism $\gamma$ maps tuples to tuples, keeps atomic types, and maps the tuples $t[i/w]$ to $\gamma(t)[i/\gamma(w)]$. By induction on the rounds it keeps every color, so isomorphic graphs have equal histograms in every round, and a difference proves non-isomorphism.

## Complexity

| case | time | space |
|---|---|---|
| one round, this implementation | $O(k n^{k+1} \log n)$ | $O(k n^{k+1})$ for the signatures |
| all rounds, this implementation | $O(k n^{2k+1} \log n)$ for at most $n^k$ rounds | $O(k n^{k+1})$ |
| Immerman and Lander (1990) | $O(k^2 n^{k+1} \log n)$ | $O(n^k)$ |
| stable after 1 round | $O(k n^{k+1} \log n)$ | $O(k n^{k+1})$ |

The faster bound processes, as in [partition refinement](/partition-refinement/), only the classes that changed. For $k = 2$ the number of rounds can be large: Kiefer and McKay (2020) gave graphs on which color refinement needs $n - 1$ rounds, and lower bounds on the number of rounds are known for higher $k$ too.

## Properties

- **A hierarchy.** If $k$-WL distinguishes two graphs, so does $(k + 1)$-WL. The hierarchy is strict, and $(n - 1)$-WL distinguishes every pair of non-isomorphic graphs on $n$ vertices.
- **Logic and games.** $k$-WL distinguishes $G$ and $H$ exactly when some sentence of first-order logic with counting quantifiers and $k + 1$ variables is true in one and false in the other, and exactly when Spoiler wins the bijective $(k + 1)$-pebble game (Cai, Fürer and Immerman 1992; Hella 1996).
- **Not complete for fixed $k$.** The [CFI construction](/cai-furer-immerman-construction/) gives, for each $k$, non-isomorphic 3-regular graphs with $O(k)$ vertices that $k$-WL does not distinguish.
- **Complete on many classes.** For a fixed $k$, $k$-WL identifies all trees (already color refinement), all graphs of bounded treewidth, all planar graphs (3-WL suffices, by Kiefer, Ponomarenko and Schweitzer), and, by Grohe (2012), all graphs from any class that excludes a fixed minor.
- **Strongly regular graphs.** 2-WL never splits a strongly regular graph beyond its three atomic classes, so it cannot tell apart two such graphs with the same parameters.
- **Homomorphism counts.** $k$-WL distinguishes two graphs exactly when they differ in the number of homomorphisms from some graph of treewidth at most $k$ (Dvořák 2010; Dell, Grohe and Rattan 2018).

## Variants and improvements

- **Oblivious $k$-WL** (used in machine learning) refines with a separate multiset for each position $i$, of the colors $\chi(t[i/w])$, instead of one multiset of $k$-tuples of colors. For $k \ge 2$ it has the same power as the version on this page with $k - 1$.
- **Coherent configurations.** The stable 2-WL coloring is a coherent configuration, the combinatorial object at the heart of Babai's work; [Babai's algorithm](/babai-quasipolynomial-algorithm/) uses $k$-WL with $k$ of order $\log n$ as a subroutine.
- **Higher-order graph neural networks** (Morris et al. 2019) mimic $k$-WL to gain expressive power.
- **Individualization plus refinement.** Combining $k$-WL with individualization of a few vertices is the core of several theoretical algorithms; in practice, [nauty](/nauty/) and [bliss](/bliss/) individualize and use only color refinement.

## When to use it

Use 2-WL or 3-WL when color refinement is too weak and you need a polynomial-time invariant with stronger power, for example on regular graphs, in proofs about graph classes, or as a feature map. For deciding isomorphism of real graphs, individualization-refinement tools such as [nauty](/nauty/) are much faster, since $n^{k+1}$ grows quickly: 3-WL on 1000 vertices already handles $10^9$ triples.

## Pitfalls

- **Off-by-one conventions.** The "3-WL" of a machine learning paper is the 2-WL of this page. State the convention and the logic $C^{k+1}$ it matches.
- **Refining each graph alone.** Colors must be named by one shared table for both graphs; comparing the number of classes of separate runs can miss differences.
- **Reading "not distinguished" as "isomorphic".** CFI graphs and strongly regular graphs with equal parameters are standard counterexamples.
- **Memory.** The $n^k$ tuples, each with a signature of $n$ entries, exhaust memory long before time runs out; this implementation is meant for small $n$.

## Implementations

## History

Weisfeiler and Leman described the refinement of colorings of vertex pairs, today's 2-WL, in 1968, along with the algebra now called a cellular algebra or coherent configuration. Babai and Mathon generalized it to $k$-tuples in the late 1970s, and Immerman and Lander (1990) connected it with counting logics. Cai, Fürer and Immerman (1992) proved that no fixed dimension identifies all graphs, ending the hope that $k$-WL alone could solve graph isomorphism in polynomial time. Later work found graph classes on which a fixed dimension suffices and linked $k$-WL to homomorphism counts and to graph neural networks.

## References
