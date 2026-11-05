---
tag: C5A0JP
kind: theorem
slug: vizing-theorem
name: Vizing's theorem
aliases:
- Vizing's edge coloring theorem
area: graphs/coloring-and-cliques
level: advanced
summary: Every simple graph has chromatic index Delta or Delta plus one.
prereqs: [edge-coloring, chromatic-index, kempe-chain]
see_also: [vizing-algorithm, konig-theorem, line-graph, brooks-theorem, list-coloring, alternating-path, distributed-edge-coloring]
sources:
  - paper: "V. G. Vizing, On an estimate of the chromatic class of a p-graph (in Russian), Diskretnyi Analiz 3, 25 to 30 (1964)"
    locator: the main theorem (Δ ≤ χ' ≤ Δ + μ for multigraphs of multiplicity μ)
  - paper: doi:10.1016/0020-0190(92)90041-S
    title: Jayadev Misra and David Gries, A constructive proof of Vizing's theorem, Information Processing Letters 41(3), 131 to 133 (1992)
    locator: the fan and path argument used in the proof below
  - paper: "C. E. Shannon, A theorem on coloring the lines of a network, Journal of Mathematics and Physics 28, 148 to 151 (1949)"
    locator: the bound 3Δ/2 for multigraphs and the examples that reach it
  - paper: doi:10.1137/0210055
    title: Ian Holyer, The NP-completeness of edge-coloring, SIAM Journal on Computing 10(4), 718 to 720 (1981)
    locator: the main theorem (deciding χ' = 3 for cubic graphs is NP-complete)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.3, Edge-colouring (Vizing's theorem and König's theorem)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 7.1, Line graphs and edge-coloring
---

Vizing's theorem says that the edges of every simple graph with maximum degree $\Delta$ can be properly colored with $\Delta + 1$ colors. Since the $\Delta$ edges at a vertex of largest degree need distinct colors, the [chromatic index](/chromatic-index/) $\chi'(G)$ is either $\Delta$ or $\Delta + 1$. The proof is constructive and gives a polynomial-time algorithm for $\Delta + 1$ colors, the [Misra-Gries algorithm](/vizing-algorithm/), while deciding which of the two values is correct is NP-complete.

## Statement

A proper [edge coloring](/edge-coloring/) of a graph gives different colors to any two edges that share an end. The chromatic index $\chi'(G)$ is the least number of colors of a proper edge coloring; it is the chromatic number of the [line graph](/line-graph/) $L(G)$.

**Theorem (Vizing 1964).** Every finite simple graph $G$ with maximum degree $\Delta$ satisfies

$$\Delta \le \chi'(G) \le \Delta + 1.$$

**Multigraph form.** If $G$ is a multigraph (loopless) in which each pair of vertices is joined by at most $\mu$ parallel edges, then $\chi'(G) \le \Delta + \mu$.

Graphs with $\chi' = \Delta$ are called **class 1**, and those with $\chi' = \Delta + 1$ are **class 2**.

## In plain words

At a meeting, each pair of people who must talk gets a private conversation, and each person can hold only one conversation per hour. How many hours are needed?

A person with the most partners needs one hour for each partner, so that number of hours is a lower bound. Vizing's theorem says that one extra hour is always enough. The proof builds the schedule one conversation at a time. When a new conversation does not fit, a chain of two hours is swapped along a path of people, which frees a common hour for the new pair.

## Proof

The lower bound holds because the $\Delta$ edges at a vertex of degree $\Delta$ need $\Delta$ different colors. For the upper bound, let $k = \Delta + 1$, and color the edges with colors $\{1, \ldots, k\}$ one at a time. We show: if all edges except one edge $uv$ are properly colored, the coloring can be changed so that $uv$ is colored too. Induction on the number of colored edges then proves the theorem.

A color is **free** at a vertex $x$ when no edge at $x$ has it. Every vertex has degree at most $\Delta < k$, so every vertex has a free color, even counting the uncolored edge $uv$ at $u$ and $v$.

**Fans.** A fan at $u$ is a sequence of distinct neighbors $f_0 = v, f_1, \ldots, f_t$ of $u$ such that, for each $i \ge 1$, the edge $u f_i$ is colored and its color is free at $f_{i-1}$. To **rotate** the fan up to $f_j$ means: for $i = 0, \ldots, j - 1$, give $u f_i$ the color that $u f_{i+1}$ had, and uncolor $u f_j$. The result is proper. At $u$ the set of colors does not change. At $f_i$ the new color of $u f_i$ was free at $f_i$, by the fan condition, and the old color of $u f_i$ is gone.

**Two-colored paths.** For two colors $a$ and $b$, the edges colored $a$ or $b$ form paths and cycles, since each vertex meets at most one edge of each color. Swapping $a$ and $b$ on one such component keeps the coloring proper; this is the edge form of a [Kempe chain](/kempe-chain/) interchange. If $a$ is free at $x$ and $b$ is not, then $x$ is the end of a path in this subgraph.

**The step.** Take a fan $F = (f_0, \ldots, f_t)$ at $u$ that cannot be extended. Let $c$ be a color free at $u$ and $d$ a color free at $f_t$.

*Case 1: $d$ is free at $u$.* Rotate the whole fan and color $u f_t$ with $d$, which is free at both $u$ and $f_t$ after the rotation, since the rotation does not change the colors at $u$ or add $d$ at $f_t$.

*Case 2: $d$ is not free at $u$.* Let $ux$ be the edge at $u$ with color $d$. Since $d$ is free at $f_t$, the vertex $x$ could extend $F$ if it were not in it. So $x = f_{j+1}$ for some $j$ with $0 \le j < t$, and by the fan condition $d$ is free at $f_j$. Let $P$ be the path of colors $c$ and $d$ that starts at $u$; its first edge is $u f_{j+1}$, because $c$ is free at $u$. No other fan edge has color $c$ or $d$: $c$ is free at $u$ and $d$ is used at $u$ only by $u f_{j+1}$. So swapping $c$ and $d$ on $P$ changes no fan edge other than $u f_{j+1}$, and it changes free colors only among $c$ and $d$.

- *Case 2a: $P$ does not end at $f_j$.* Then $f_j$ is not on $P$ at all, because $d$ is free at $f_j$, so $f_j$ could only be an end of $P$. Swap $c$ and $d$ on $P$. Now $d$ is free at $u$ and still free at $f_j$, and $(f_0, \ldots, f_j)$ is still a fan, since its edges kept their colors and the free colors that matter are not $c$ or $d$. Rotate this fan up to $f_j$ and color $u f_j$ with $d$.
- *Case 2b: $P$ ends at $f_j$.* Then $f_t$ is not on $P$: $d$ is free at $f_t$, so $f_t$ could only be an end, and the ends are $u$ and $f_j \ne f_t$. Swap $c$ and $d$ on $P$. The edge $u f_{j+1}$ now has color $c$, and $c$ is now free at $f_j$, because the last edge of $P$ at $f_j$ had color $c$ (as $d$ was free there) and now has color $d$. So $F$ is still a fan, $d$ is still free at $f_t$, and $d$ is now free at $u$. This is Case 1: rotate the whole fan and color $u f_t$ with $d$.

In every case $uv$ is colored and the coloring stays proper with $k = \Delta + 1$ colors. $\blacksquare$

Each step builds a fan in $O(\Delta)$ steps and walks one path of length $O(n)$, so coloring all $m$ edges takes $O(m n)$ time; see the [Misra-Gries algorithm](/vizing-algorithm/).

## Consequences

- **Two classes.** Every simple graph is class 1 or class 2. Deciding which is NP-complete, even for cubic graphs (Holyer 1981), so finding $\chi'$ exactly is NP-hard, although it is known up to one.
- **Bipartite graphs are class 1.** König's edge coloring theorem says $\chi' = \Delta$ for bipartite multigraphs. The same path swap works, because in a bipartite graph the path $P$ cannot return to the other end of the uncolored edge.
- **Odd regular graphs.** A $\Delta$-regular graph with an odd number of vertices is class 2: each color class is a matching, which covers at most $n - 1$ vertices, so it has at most $(n-1)/2$ edges, and $\Delta$ classes hold at most $\Delta (n-1)/2 < \Delta n / 2 = m$ edges.
- **Approximation.** The constructive proof gives a polynomial-time edge coloring with at most one color more than optimal, a rare case of an NP-hard problem with an additive error of 1.
- **Scheduling.** Rounds of pairwise meetings, data transfers between nodes, and the switching in a crossbar are edge colorings, so $\Delta + 1$ rounds always suffice.

## Tightness

Both values occur.

| graph | $\Delta$ | $\chi'$ | class |
|---|---|---|---|
| $C_6$ | 2 | 2 | 1 |
| $C_5$ | 2 | 3 | 2 |
| $K_4$ | 3 | 3 | 1 |
| $K_5$ | 4 | 5 | 2 |
| $K_6$ | 5 | 5 | 1 |
| $K_{3,3}$ | 3 | 3 | 1 |
| Petersen graph | 3 | 4 | 2 |

The values in the table agree with an exhaustive search. In general $K_n$ is class 1 for even $n$ and class 2 for odd $n$, by the remark on odd regular graphs.

For multigraphs, $\Delta + \mu$ can be much larger than $\Delta + 1$, and the right bound is then often Shannon's $\lfloor 3\Delta/2 \rfloor$. The **Shannon multigraph**, a triangle whose three edges each have multiplicity $\Delta/2$ (for even $\Delta$), has $3\Delta/2$ edges that pairwise share an end, so it needs $3\Delta/2$ colors; here $\mu = \Delta/2$ and Vizing's bound $\Delta + \mu$ is exact.

## History

Shannon proved the bound $3\Delta/2$ for multigraphs in 1949, motivated by wiring problems. Vadim Vizing proved $\chi' \le \Delta + \mu$ in 1964, and Gupta found it independently around 1966. Holyer proved in 1981 that deciding $\chi' = \Delta$ is NP-complete. Misra and Gries gave the short constructive proof used above in 1992. Vizing also conjectured that every planar graph with $\Delta \ge 6$ is class 1; the case $\Delta \ge 8$ is his, $\Delta = 7$ was settled by Sanders and Zhao in 2001, and $\Delta = 6$ is open.

## References
