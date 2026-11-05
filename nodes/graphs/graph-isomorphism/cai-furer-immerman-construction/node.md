---
tag: BD1KRX
kind: concept
slug: cai-furer-immerman-construction
name: Cai-Fürer-Immerman construction
aliases:
- CFI graphs
- CFI construction
area: graphs/graph-isomorphism
level: advanced
summary: Builds pairs of non-isomorphic graphs that k-WL cannot distinguish, proving limits of the hierarchy.
prereqs: [k-dimensional-weisfeiler-leman, weisfeiler-leman, graph-isomorphism-definition]
see_also: [k-dimensional-weisfeiler-leman, individualization-refinement, nauty, babai-quasipolynomial-algorithm, gi-completeness, treewidth]
sources:
  - paper: doi:10.1007/BF01305232
    title: Jin-Yi Cai, Martin Fürer and Neil Immerman, An optimal lower bound on the number of variables for graph identification, Combinatorica 12(4), 389 to 410 (1992)
    locator: Section 6 (the gadgets, the twisted and untwisted graphs, and the lower bound through separators of the base graph)
  - paper: doi:10.1145/3188745.3188900
    title: Daniel Neuen and Pascal Schweitzer, An exponential lower bound for individualization-refinement algorithms for graph isomorphism, STOC 2018
    locator: the whole paper (CFI-type graphs over suitable base graphs force exponential search trees)
  - paper: "Neil Immerman and Eric Lander, Describing graphs: a first-order approach to graph canonization, in Complexity Theory Retrospective, Springer, 1990, 59 to 81"
    locator: the whole chapter (the equivalence of k-WL with counting logic, which the CFI bound is stated for)
---

The Cai-Fürer-Immerman (CFI) construction turns any connected base graph into a pair of graphs, the untwisted and the twisted one, that are not isomorphic but look alike locally. Cai, Fürer and Immerman (1992) proved that if the base graph has no small separators, then the [k-dimensional Weisfeiler-Leman algorithm](/k-dimensional-weisfeiler-leman/) cannot tell the pair apart unless $k$ is linear in the size of the base graph. Since the CFI graphs have bounded degree and are easy to tell apart by other means, this shows that $k$-WL for a fixed $k$, and counting logic with a fixed number of variables, do not capture graph isomorphism. CFI graphs are also the standard hard inputs for [individualization-refinement](/individualization-refinement/) tools.

## In plain words

Take any network, and replace each point by a small gadget and each link by a pair of wires. Each gadget is built so that it can "flip" an even number of its wire pairs without changing its shape. Now build two copies: in one, all wire pairs are connected straight; in the other, exactly one wire pair is crossed. A crossed pair can be pushed along the network by flipping gadgets, but flips come in pairs, so one crossing can never be removed: the two copies differ. Yet any test that only looks at a few points at a time sees the same thing in both, because the crossing can always be moved somewhere it is not looking.

## The idea

Graphs here are simple and undirected; the original construction also colors vertices by gadget to simplify the proof, and the examples below are uncolored.

**The gadget.** For a vertex $v$ of the base graph $H$ with incident edges $E(v)$, the gadget $X_v$ has:

- for each $e \in E(v)$, two **end vertices** $a_{v,e,0}$ and $a_{v,e,1}$;
- for each subset $S \subseteq E(v)$ of even size, a **middle vertex** $m_{v,S}$, adjacent to $a_{v,e,1}$ for $e \in S$ and to $a_{v,e,0}$ for $e \notin S$.

Swapping $a_{v,e,0}$ with $a_{v,e,1}$ for all $e$ in a set $F \subseteq E(v)$ maps $m_{v,S}$ to $m_{v,S \triangle F}$. This is an automorphism of $X_v$ exactly when $|F|$ is even, because only then does $S \triangle F$ keep even size.

**The pair.** For each base edge $e = uv$, join $a_{u,e,i}$ to $a_{v,e,i}$ for $i = 0, 1$: this gives the **untwisted** graph $X(H)$. Joining $a_{u,e,i}$ to $a_{v,e,1-i}$ instead, on one edge only, gives the **twisted** graph $\tilde X(H)$. More generally, twisting a set $T$ of edges gives a graph whose isomorphism type depends only on the parity of $|T|$, when $H$ is connected.

**Why they differ.** Flipping a gadget at $v$ along an even set $F$ moves twists across the edges of $F$, which changes $|T|$ by an even number. So twists can be moved and cancelled in pairs, but one twist cannot vanish. Making this precise shows that $X(H) \not\cong \tilde X(H)$ for connected $H$.

**Why $k$-WL fails.** The equivalence of $k$-WL with the bijective pebble game and counting logic with $k + 1$ variables reduces the question to a game. Spoiler places pebbles on gadgets; Duplicator answers with a bijection that "hides" the twist. As long as the pebbled gadgets do not separate the base graph into parts that trap the twist, Duplicator moves the twist into a part with no pebbles. If every separator of $H$ that splits it in a balanced way has more than $k + 1$ vertices, Duplicator wins, and $k$-WL does not distinguish the pair. Base graphs with large separators and $O(k)$ vertices of bounded degree, such as expanders, give pairs with $O(k)$ vertices.

## Examples

All values were computed with the implementations on the pages of [color refinement](/weisfeiler-leman/), [k-WL](/k-dimensional-weisfeiler-leman/) and [nauty](/nauty/).

| base graph $H$ | vertices, edges of each CFI graph | color refinement | 2-WL | 3-WL | isomorphic? |
|---|---|---|---|---|---|
| triangle $K_3$ | 18, 18 | not distinguished | distinguished | distinguished | no |
| $K_4$ | 40, 60 | not distinguished | not distinguished | distinguished | no |

- **Over $K_3$.** Each gadget has 2 middle vertices and 4 end vertices, and every vertex has degree 2. The untwisted graph is two 9-cycles, with $|\mathrm{Aut}| = 2 \cdot 18^2 = 648$, and the twisted one is an 18-cycle, with $|\mathrm{Aut}| = 36$. Both are 2-regular, so color refinement fails, but 2-WL sees the distances.
- **Over $K_4$.** Each gadget has $2^{3-1} = 4$ middle vertices of degree 3 and 6 end vertices of degree 2. Both graphs have 192 automorphisms. 2-WL does not separate them; 3-WL does, after refining $40^3 = 64000$ triples.
- **Size.** A gadget for a vertex of degree $d$ has $2^{d-1} + 2d$ vertices, so over a base graph of bounded degree the CFI graphs have $O(|V(H)|)$ vertices.

## Where it is used

- **Limits of the WL hierarchy and of counting logic.** CFI graphs show that no fixed $k$ makes $k$-WL a complete isomorphism test, and that fixed-point logic with counting does not capture polynomial time, since the CFI pairs can be told apart in polynomial time by solving a linear system over the two-element field.
- **Lower bounds for practical tools.** Miyazaki (1997) used Fürer's gadgets to make [nauty](/nauty/) take exponential time, and Neuen and Schweitzer (2018) built CFI-type graphs on which every [individualization-refinement](/individualization-refinement/) algorithm visits exponentially many nodes.
- **Benchmarks.** CFI graphs and related families appear in the benchmark sets of nauty, Traces and [bliss](/bliss/).
- **Group-theoretic algorithms.** Since CFI graphs have bounded degree, [Luks's algorithm](/luks-algorithm/) handles them in polynomial time, and they illustrate why [Babai's algorithm](/babai-quasipolynomial-algorithm/) needs group theory and not only combinatorial refinement.
- **Graph neural networks.** Message-passing networks are bounded by color refinement, and higher-order networks by $k$-WL, so CFI graphs mark the limits of their expressive power.

## References
