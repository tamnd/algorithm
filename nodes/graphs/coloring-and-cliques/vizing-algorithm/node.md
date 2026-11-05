---
tag: 5TRSEH
kind: algorithm
slug: vizing-algorithm
name: Vizing's algorithm
aliases:
- Misra-Gries edge coloring
area: graphs/coloring-and-cliques
level: advanced
summary: Constructive proof that colors the edges of a simple graph with at most Delta plus one colors.
solves: [edge-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, Δ: the maximum degree}
  time: {worst: O(m (n + Δ^2))}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [vizing-theorem, edge-coloring, kempe-chain]
see_also: [chromatic-index, konig-theorem, line-graph, alternating-path, distributed-edge-coloring, bipartite-matching]
sources:
  - paper: doi:10.1016/0020-0190(92)90041-S
    title: Jayadev Misra and David Gries, A constructive proof of Vizing's theorem, Information Processing Letters 41(3), 131 to 133 (1992)
    locator: the whole paper (fans, rotation, the cd-path inversion and the O(|V| |E|) algorithm)
  - paper: "V. G. Vizing, On an estimate of the chromatic class of a p-graph (in Russian), Diskretnyi Analiz 3, 25 to 30 (1964)"
    locator: the theorem χ' ≤ Δ + 1 for simple graphs
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.3, Edge-colouring (proof of Vizing's theorem)
  - paper: doi:10.1137/0210055
    title: Ian Holyer, The NP-completeness of edge-coloring, SIAM Journal on Computing 10(4), 718 to 720 (1981)
    locator: the main theorem (deciding whether Δ colors suffice is NP-complete)
---

Vizing's algorithm colors the edges of a simple graph with at most $\Delta + 1$ colors, where $\Delta$ is the maximum degree, so that edges with a common end get different colors. It colors the edges one at a time, and when a new edge $uv$ does not fit, it builds a *fan* of edges at $u$, swaps two colors along a path (an edge [Kempe chain](/kempe-chain/)), and shifts the colors of the fan by one position. The version here is the short one of Misra and Gries (1992). Since any edge coloring needs $\Delta$ colors, the result is at most one color more than optimal, which is the best a polynomial-time algorithm can promise unless P = NP.

## In plain words

Color the edges one by one. Each vertex touches at most $\Delta$ edges, so with $\Delta + 1$ colors every vertex always has at least one unused color. The trouble is that the new edge needs a color that is unused at both of its ends.

So the algorithm makes room. It looks at the edges around one end, $u$, and finds a chain of them where each edge's color is unused at the previous neighbor. Shifting colors along this chain moves the problem to another edge. If that is not enough, it swaps two colors along a path that starts at $u$, which frees a color at $u$ without breaking anything. Then one color fits.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and a list of its $m$ edges. The output is a proper [edge coloring](/edge-coloring/) $c : E \to \{1, \ldots, \Delta + 1\}$. Finding a coloring with the least number of colors, the [chromatic index](/chromatic-index/), is NP-hard (Holyer 1981), so the algorithm aims for $\Delta + 1$, which [Vizing's theorem](/vizing-theorem/) shows is always possible.

## The algorithm

A color is *free* at a vertex when no colored edge at the vertex has it. A **fan** at $u$ is a sequence of distinct neighbors $F = (f_0, f_1, \ldots, f_t)$ of $u$ such that the edge $u f_0$ is uncolored and, for $i \ge 1$, the color of $u f_i$ is free at $f_{i-1}$. To **rotate** a fan $(f_0, \ldots, f_j)$ means to give each $u f_i$, $i < j$, the color of $u f_{i+1}$ and to uncolor $u f_j$. The **cd-path** at $u$ is the maximal path that starts at $u$ and uses edges colored $d$ and $c$ alternately, starting with $d$.

```pseudo id=main
MISRA-GRIES(G)
L1  for each edge uv of G do
L2      F ← a maximal fan (f0 = v, f1, ..., ft) at u
L3      c ← a color free at u, d ← a color free at ft
L4      swap the colors c and d on the cd-path at u
L5      w ← the first fj such that (f0, ..., fj) is a fan and d is free at fj
L6      rotate the fan (f0, ..., w)
L7      color uw with d
L8  return the coloring
```

Line L2 extends the fan while some neighbor $x$ of $u$, not yet in $F$, has $c(ux)$ free at the last vertex. Line L4 is the Kempe swap: since $c$ is free at $u$, the path starts at $u$ and is well defined, and after the swap $d$ is free at $u$. Line L5 always finds a vertex $w$, by the case analysis in the proof of [Vizing's theorem](/vizing-theorem/). After the rotation of line L6, the edge $uw$ is the uncolored one, and $d$ is free at both $u$ and $w$, so line L7 is proper. The implementation picks the smallest free color at line L3.

## Example

Take the graph with 4 vertices and the edges in the order $02, 23, 01, 03$: a triangle $0, 2, 3$ with a pendant edge $01$. Here $\Delta = 3$, so the colors are $1, \ldots, 4$.

| edge | fan at $u$ | $c$, $d$ | cd-path | $w$ | colors after the step |
|---|---|---|---|---|---|
| $02$ | $(2)$ | $1, 1$ | none | 2 | $02{:}1$ |
| $23$ | $(3, 0)$ | $2, 2$ | none | 3 | $02{:}1$, $23{:}2$ |
| $01$ | $(1, 2)$ | $2, 3$ | none | 1 | $02{:}1$, $23{:}2$, $01{:}3$ |
| $03$ | $(3, 2, 1)$ | $2, 1$ | $0\!-\!2\!-\!3$, colors $1, 2$ | 1 | $02{:}3$, $23{:}1$, $03{:}2$, $01{:}1$ |

The last step is the interesting one. At $u = 0$ the fan is $(3, 2, 1)$: the color 1 of $02$ is free at 3, and the color 3 of $01$ is free at 2. Color $c = 2$ is free at 0 and $d = 1$ is free at 1, but 1 is used at 0 by the edge $02$. The path $0 \xrightarrow{1} 2 \xrightarrow{2} 3$ is swapped, so $02$ gets 2 and $23$ gets 1. Now $d = 1$ is free at 0, but not at 3 or 2, and it is free at 1, with $(3, 2, 1)$ still a fan. Rotating gives $03$ the color 2 of $02$ and $02$ the color 3 of $01$, and $01$ takes 1. The final coloring uses 3 colors.

## Correctness

**Claim.** After each turn of line L1, the colored edges, now including $uv$, form a proper edge coloring with colors in $\{1, \ldots, \Delta + 1\}$.

Every vertex has at most $\Delta$ edges, so line L3 finds free colors. The swap of line L4 keeps the coloring proper, as for any two-color component, and makes $d$ free at $u$. Line L5 finds $w$: either $d$ was free at $u$ already and $w$ can be the last vertex of the fan, or the swap either leaves the prefix up to the neighbor whose edge had color $d$ intact, or it repairs the whole fan. A rotation keeps the coloring proper by the fan condition. The full proof is below.

## Complexity

**Time.** A fan has at most $\Delta$ vertices. Building it by scanning the neighbors of $u$ once for each new fan vertex takes $O(\Delta^2)$ time. Free colors take $O(\Delta)$ time with a map from colors to edges at each vertex. The cd-path is a simple path, so it has $O(n)$ edges, and swapping it costs $O(n)$. Line L5 and the rotation take $O(\Delta)$. So each edge costs $O(n + \Delta^2)$, and the total is $O(m(n + \Delta^2))$. Misra and Gries state $O(nm)$ for a more careful fan construction.

**Space.** The map from (vertex, color) to the other end of the edge, and the colors of the edges, use $O(n + m)$ space.

## Properties

- **At most $\Delta + 1$ colors**, so within one color of the optimum.
- **Greedy and incremental.** It handles the edges in any order, and an edge, once colored, stays colored, though its color may change.
- **Local changes.** Each step changes the colors of a fan at one vertex and of one path.
- **Not optimal.** On class 1 graphs it may still use $\Delta + 1$ colors; deciding whether $\Delta$ colors suffice is NP-complete.

## Variants and improvements

- **Faster algorithms.** Gabow, Nishizeki, Kariv, Leven and Terada gave $O(m \sqrt{n \log n})$ time in 1985, and Sinnamon $O(m \sqrt n)$ in 2019. In 2024, Assadi and coauthors announced near-linear time algorithms for $\Delta + 1$ colors.
- **Bipartite graphs.** König's theorem gives $\Delta$ colors, found by a similar swap along alternating paths, or by repeated [matchings](/bipartite-matching/) in regular bipartite graphs. Cole, Ost and Schirra do it in $O(m \log \Delta)$ time.
- **Multigraphs.** Vizing's bound $\Delta + \mu$ and Shannon's $\lfloor 3\Delta/2 \rfloor$ also have constructive proofs.
- **Distributed.** See [distributed edge coloring](/distributed-edge-coloring/) for algorithms that use few rounds of communication, usually with more colors.

## When to use it

Use it when an edge coloring with a guaranteed $\Delta + 1$ colors is needed: scheduling pairwise tasks such as matches of a tournament or transfers between nodes, conflict-free channel assignment on links, or as a subroutine in algorithms that split a graph into matchings. If $\Delta + 1$ is not needed and speed matters, a greedy edge coloring with up to $2\Delta - 1$ colors is simpler.

## Pitfalls

- **Rotating the whole fan.** After the swap of line L4, the fan may be broken after the vertex whose edge had color $d$. Rotate only the prefix up to $w$ chosen at line L5.
- **Path from the wrong end.** The cd-path must start at $u$ with the color $d$. Starting from the other end of the fan, or with color $c$, does not free $d$ at $u$.
- **Swapping part of a component.** The swap must cover the whole two-colored path; stopping early leaves two edges of the same color at a vertex.
- **Multigraphs.** The fan argument uses that $u$ has one edge to each neighbor. With parallel edges, $\Delta + 1$ colors may not suffice.

## Implementations

## History

Vadim Vizing proved the bound $\Delta + 1$ in 1964 with an argument that already used fans and alternating paths. Misra and Gries published the short constructive proof used here in 1992, which became the standard textbook algorithm. Faster algorithms followed, from Gabow and coauthors in 1985 to near-linear time results announced in 2024.

## References
