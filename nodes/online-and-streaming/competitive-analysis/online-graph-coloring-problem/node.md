---
tag: XV2KWJ
kind: problem
slug: online-graph-coloring-problem
name: Online graph coloring problem
aliases:
- online coloring
- online graph coloring
- on-line graph coloring
- online vertex coloring
area: online-and-streaming/competitive-analysis
level: advanced
summary: Vertices arrive with their edges to earlier vertices and get a permanent color at once. First Fit can be forced to use log n colors on trees, and on interval graphs the best ratio is 3.
prereqs: [graph-coloring, online-algorithm, competitive-ratio]
see_also: [greedy-coloring, interval-coloring-depth-theorem, online-independent-set-problem, chromatic-number, graph-coloring-inapproximability, chordal-graph-coloring, degeneracy, yao-minimax-principle]
sources:
  - paper: doi:10.2307/2272247
    title: "Dwight R. Bean, Effective coloration, Journal of Symbolic Logic 41(2) (1976), 469-480"
    locator: the lower bound for coloring trees online, cited by Albers and Schraink (2017) as the Omega(log n) bound for every deterministic online algorithm
  - paper: doi:10.1002/jgt.3190120212
    title: "Andras Gyarfas and Jeno Lehel, On-line and first fit colorings of graphs, Journal of Graph Theory 12(2) (1988), 217-227"
    locator: First Fit on forests and trees (O(log n) colors, in the form log2 n + 1)
  - paper: doi:10.1016/0012-365X(89)90096-4
    title: "Laszlo Lovasz, Michael Saks and W. T. Trotter, An on-line graph coloring algorithm with sublinear performance ratio, Discrete Mathematics 75 (1989), 319-325"
    locator: the deterministic algorithm with ratio O(n / log* n), and the O(log n) colors for bipartite graphs
  - paper: "H. A. Kierstead and W. T. Trotter, An extremal problem in recursive combinatorics, Congressus Numerantium 33 (1981), 143-153"
    title: "H. A. Kierstead and W. T. Trotter, An extremal problem in recursive combinatorics, Congressus Numerantium 33 (1981), 143-153"
    locator: the online algorithm that colors interval graphs with 3 omega - 2 colors, and the adversary that forces 3 omega - 2 colors
  - paper: doi:10.1137/0401048
    title: "H. A. Kierstead, The linearity of first-fit coloring of interval graphs, SIAM Journal on Discrete Mathematics 1(4) (1988), 526-530"
    locator: First Fit uses at most 40 omega colors on interval graphs
  - paper: doi:10.1016/j.ejc.2015.05.015
    title: "H. A. Kierstead, David A. Smith and W. T. Trotter, First-fit coloring on interval graphs has performance ratio at least 5, European Journal of Combinatorics 51 (2016), 236-254"
    locator: the abstract and the introduction (the lower bound 5, and the history of the upper bounds 40, 25.72, 10 and 8)
  - paper: doi:10.1016/0304-3975(94)90157-0
    title: "Magnus M. Halldorsson and Mario Szegedy, Lower bounds for on-line graph coloring, Theoretical Computer Science 130(1) (1994), 163-174"
    locator: the lower bound Omega(n / log^2 n) for deterministic and randomized online algorithms
  - paper: doi:10.4230/LIPIcs.ESA.2017.7
    title: "Susanne Albers and Sebastian Schraink, Tight bounds for online coloring of basic graph classes, ESA 2017, LIPIcs 87, 7:1-7:14"
    locator: the introduction (a survey of the earlier bounds) and Section 4 (Omega(log n) expected colors on trees for randomized algorithms)
---

Online graph coloring is the problem of coloring the vertices of a graph that is revealed one vertex at a time. Each vertex arrives with its edges to the earlier vertices, and the algorithm must give it a color at once, different from the colors of its earlier neighbours. A color is never changed. The algorithm is measured by the number of colors it uses compared with the [chromatic number](/chromatic-number/) $\chi(G)$ of the whole graph. The problem is hard even on simple graphs. On trees, which need 2 colors, every deterministic algorithm can be forced to use $\log_2 n + 1$ colors, and First Fit never uses more. On bipartite graphs First Fit can be forced to use $n/2$ colors. On interval graphs the algorithm of Kierstead and Trotter uses at most $3\omega - 2$ colors, where $\omega$ is the largest clique, and no deterministic algorithm does better. On general graphs the best ratios are close to $n$.

## In plain words

Guests come to a dinner one at a time. When a guest arrives, the host learns which of the guests already seated this person does not get along with. The host must give the guest a table at once, and two guests who do not get along may not share a table. Nobody moves later. The host wants few tables.

The simplest rule puts each guest at the first table that has no enemy of the guest. This rule can be tricked. Even when the guests could be split into two friendly groups, a bad order of arrival can make the rule open many tables. No rule is safe from a bad order, but some rules lose much less than others on special kinds of guest lists, such as lists where the conflicts come from overlapping time intervals.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices, revealed as a sequence $v_1, v_2, \ldots, v_n$. When $v_t$ arrives, the algorithm learns the edges between $v_t$ and $v_1, \ldots, v_{t-1}$. The value of $n$ is not known in advance, and the algorithm does not see a geometric representation of the graph, such as the intervals of an interval graph.

**Decisions.** At the arrival of $v_t$, the algorithm gives it a color $c(v_t) \in \{1, 2, \ldots\}$ with $c(v_t) \ne c(v_s)$ for each earlier neighbour $v_s$. Colors are final.

**Measure.** $\mathrm{ALG}$ is the number of distinct colors used. For a class of graphs, an algorithm has performance ratio $\rho(n)$ if $\mathrm{ALG} \le \rho(n) \cdot \chi(G)$ on every graph of the class with $n$ vertices and every arrival order. For a randomized algorithm, $\mathbb{E}[\mathrm{ALG}]$ replaces $\mathrm{ALG}$, against an [oblivious adversary](/oblivious-adversary/). For interval graphs and other perfect graphs, $\chi(G) = \omega(G)$, the size of the largest clique, and bounds are written in terms of $\omega$.

**First Fit.** The basic algorithm gives $v_t$ the smallest color not used by its earlier neighbours. It is the online form of [greedy coloring](/greedy-coloring/), with the arrival order as the vertex order.

## Variants

- **Graph classes.** Forests and trees, bipartite graphs, interval graphs, chordal graphs, planar graphs, $d$-degenerate graphs and disk graphs each have their own bounds; the main ones are in the table below.
- **Randomized algorithms.** Randomization helps only a little. The Halldorsson and Szegedy lower bound for general graphs and the $\Omega(\log n)$ bound for trees (Albers and Schraink, 2017) both hold for randomized algorithms.
- **Lookahead and buffers.** The algorithm may see the next $l$ vertices, or keep up to $b$ vertices uncolored for a while. Albers and Schraink showed that for chordal graphs a lookahead of $O(n / \log n)$ or a buffer of size $n^{1 - \varepsilon}$ does not change the order of the bound.
- **Performance of First Fit.** For a class of graphs, the question is how many colors First Fit uses in the worst order, as a function of $\chi$ or $\omega$. For interval graphs this is a long open problem (Theorem 6).
- **Online chromatic number.** For a fixed graph class, the least number of colors that some online algorithm can always keep to, as a function of $n$ or $\omega$.
- **Advice.** The algorithm may read bits from an oracle that knows the graph; see the [advice model](/advice-model/).

## Examples

**First Fit on a tree.** The trees $T_k$ are built in arrival order. $T_1$ is one vertex. $T_k$ is a copy of $T_1$, then a copy of $T_2$, and so on up to $T_{k-1}$, all sent first, and then a new root joined to the root of each copy. $T_3$ arrives as $v_1$ (the copy of $T_1$), $v_2, v_3$ (the copy of $T_2$, with edge $v_2 v_3$), and the root $v_4$ with edges to $v_1$ and $v_3$.

| vertex | earlier neighbours | their colors | First Fit color |
|---|---|---|---|
| $v_1$ | none | none | 1 |
| $v_2$ | none | none | 1 |
| $v_3$ | $v_2$ | 1 | 2 |
| $v_4$ | $v_1, v_3$ | 1, 2 | 3 |

The tree is the path $v_2 v_3 v_4 v_1$, which needs 2 colors, but First Fit uses 3. In general First Fit gives the root of $T_k$ color $k$, and $T_k$ has $2^{k-1}$ vertices. A direct run of First Fit on $T_k$ for $k = 1, \ldots, 8$ gives exactly $k$ colors.

**First Fit on a crown.** Take vertices $a_1, b_1, \ldots, a_m, b_m$ with an edge $a_i b_j$ for each $i \ne j$. This is a bipartite graph. In the order $a_1, b_1, a_2, b_2, \ldots$, the vertices $a_i$ and $b_i$ have earlier neighbours of all colors $1, \ldots, i - 1$, and no earlier neighbour of color $i$. So First Fit gives both of them color $i$ and uses $m = n/2$ colors, while $\chi = 2$.

## Known algorithms

- **First Fit.** Simple and local. At most $\Delta + 1$ colors on a graph of maximum degree $\Delta$, as in the [$\Delta + 1$ bound](/delta-plus-one-bound/), at most $\lfloor \log_2 n \rfloor + 1$ on forests (Theorem 1), and $O(d \log n)$ on $d$-degenerate graphs (Irani, 1994). It is poor on bipartite graphs and has a constant ratio on interval graphs.
- **Lovasz, Saks and Trotter (1989).** A deterministic algorithm for general graphs with ratio $O(n / \log^* n)$, where $\log^*$ is the [iterated logarithm](/iterated-logarithm/). The same paper colors bipartite graphs online with $O(\log n)$ colors.
- **Randomized algorithms.** Vishwanathan (1992) gave ratio $O(n / \sqrt{\log n})$, and Halldorsson (1997) improved it to $O(n / \log n)$.
- **Kierstead and Trotter (1981).** An algorithm for interval graphs that uses at most $3\omega - 2$ colors. It puts each vertex in the first level $r$ such that the vertices of levels $1, \ldots, r$, together with the new vertex, contain no clique with more than $r$ vertices. Level 1 is an independent set and gets one color. Each other level induces a graph of maximum degree at most 2, and First Fit colors it with 3 colors of its own. This gives $1 + 3(\omega - 1) = 3\omega - 2$ colors.

## Bounds

**Theorem 1 (First Fit on forests).** First Fit uses at most $\lfloor \log_2 n \rfloor + 1$ colors on every forest with $n$ vertices, in every arrival order.

*Proof.* Let $N(k)$ be the least number of vertices of a forest, with an order, in which First Fit uses color $k$. Then $N(1) = 1$. Let $v$ get color $k \ge 2$. Then $v$ has earlier neighbours $u_1, \ldots, u_{k-1}$ with $c(u_i) = i$. Removing $v$ from the forest puts the $u_i$ in different components $C_1, \ldots, C_{k-1}$, because two of them in the same component would close a cycle through $v$. The color of $u_i$ depends only on the vertices of $C_i$ that arrive before $u_i$, since those vertices and their earlier neighbours all arrive before $v$ and lie in $C_i$. So First Fit run on $C_i$ alone, in the same order, also gives $u_i$ color $i$, and $\lvert C_i \rvert \ge N(i)$. The $C_i$ are disjoint and do not contain $v$, so $N(k) \ge 1 + \sum_{i < k} N(i)$, and by induction $N(k) \ge 2^{k-1}$. If First Fit uses $k$ colors on $n$ vertices, then $n \ge 2^{k-1}$, so $k \le \log_2 n + 1$. $\square$

**Theorem 2 (no deterministic algorithm beats First Fit on trees).** For each deterministic online algorithm and each $k \ge 1$, there is a tree with $2^{k-1}$ vertices on which the algorithm uses at least $k$ colors. So every deterministic algorithm uses at least $\log_2 n + 1$ colors on some tree with $n = 2^{k-1}$ vertices, and Theorem 1 shows that First Fit is optimal on forests. The lower bound for trees goes back to Bean (1976). The matching First Fit bound is due to Gyarfas and Lehel (1988).

*Proof.* By induction on $k$, the adversary builds a tree $S_k$ with $2^{k-1}$ vertices on which the algorithm uses at least $k$ colors. $S_1$ is one vertex. For $k \ge 2$, the adversary first sends disjoint trees $S_1, S_2, \ldots, S_{k-1}$, one after the other, each built by the induction against the algorithm as it behaves at that time. Then it picks one vertex $x_i$ in each $S_i$, for $i = 1, \ldots, k-1$ in turn, with a color different from $c(x_1), \ldots, c(x_{i-1})$. This is possible, because $S_i$ has at least $i$ colors. Then it sends a new vertex $r$ with edges to $x_1, \ldots, x_{k-1}$. The trees $S_i$ are disjoint and $r$ has one edge into each, so the result is a tree. Its size is $1 + \sum_{i < k} 2^{i-1} = 2^{k-1}$. The color of $r$ differs from the $k - 1$ distinct colors $c(x_i)$, so the tree has at least $k$ colors. $\square$

Against First Fit, this adversary builds exactly the tree $T_k$ of the examples. A run of the adversary against First Fit and four other deterministic rules, for $k = 1, \ldots, 8$, gives a tree with $2^{k-1}$ vertices and at least $k$ colors each time. For randomized algorithms, Albers and Schraink (2017) proved that the expected number of colors on trees is still $\Omega(\log n)$.

**Theorem 3 (First Fit on bipartite graphs).** For each $m \ge 1$ there is a bipartite graph with $n = 2m$ vertices and an order on which First Fit uses $n/2$ colors.

*Proof.* The crown of the examples. By induction on $i$: when $a_i$ arrives, its earlier neighbours are $b_1, \ldots, b_{i-1}$ with colors $1, \ldots, i-1$, so it gets color $i$, and the same holds for $b_i$, whose earlier neighbours are $a_1, \ldots, a_{i-1}$. $\square$

Other online algorithms do much better on bipartite graphs: Lovasz, Saks and Trotter color them with $O(\log n)$ colors, and Theorem 2 shows that $\Omega(\log n)$ is needed, since trees are bipartite.

**Theorem 4 (general graphs).** The following bounds are cited, not proved here.

- Lovasz, Saks and Trotter (1989): a deterministic online algorithm with ratio $O(n / \log^* n)$.
- Vishwanathan (1992): a randomized algorithm with ratio $O(n / \sqrt{\log n})$. Halldorsson (1997): $O(n / \log n)$.
- Halldorsson and Szegedy (1994): every online algorithm, deterministic or randomized, has ratio $\Omega(n / \log^2 n)$.

So the best ratio is between $n / \log^2 n$ and $n / \log n$ up to constant factors for randomized algorithms. Any algorithm uses at most $n$ colors, so these ratios are only a little better than trivial.

**Theorem 5 (interval graphs, Kierstead and Trotter 1981).** There is a deterministic online algorithm that colors each interval graph with largest clique $\omega$ using at most $3\omega - 2$ colors. For each $\omega$, every deterministic online algorithm can be forced to use $3\omega - 2$ colors on some interval graph with largest clique $\omega$. So the best deterministic ratio for interval graphs is 3, approached as $\omega$ grows. This is cited, not proved here. The offline problem needs only $\omega$ colors, by the [interval coloring depth theorem](/interval-coloring-depth-theorem/); the gap comes only from the online order.

**Theorem 6 (First Fit on interval graphs).** Let $R$ be the supremum of $\chi_{FF}(G) / \omega(G)$ over interval graphs $G$, where $\chi_{FF}$ is the largest number of colors that First Fit uses over all orders. Kierstead (1988) proved that $R$ is finite, with First Fit using at most $40\omega$ colors. The upper bound was lowered to $25.72\omega$ (Kierstead and Qin), to $10\omega$ (Pemmaraju, Raman and Varadarajan, 2004), and to $8\omega$ (Narayanaswamy and Subhash Babu, Order 25 (2008), 49-53; also Brightwell, Kierstead and Trotter, unpublished). The lower bound $R \ge 4$ is due to Witsenhausen (1976) and to Chrobak and Slusarek (1988), $R \ge 4.45$ to Slusarek (1993), and $R \ge 5$ to Kierstead, Smith and Trotter (2016). So $5 \le R \le 8$, and the exact value is open. This is cited, not proved here.

First Fit is thus worse than the Kierstead and Trotter algorithm on interval graphs, by a factor between about $5/3$ and $8/3$, but still within a constant of the optimum.

| graph class | $\chi$ | First Fit | best deterministic | lower bound |
|---|---|---|---|---|
| forests and trees | 2 | $\lfloor \log_2 n \rfloor + 1$ (Theorem 1) | $\lfloor \log_2 n \rfloor + 1$ | $\log_2 n + 1$ (Theorem 2); $\Omega(\log n)$ randomized |
| bipartite | 2 | $n/2$ in the worst case (Theorem 3) | $O(\log n)$ (Lovasz, Saks and Trotter) | $\Omega(\log n)$ |
| interval | $\omega$ | at most $8\omega$; ratio at least 5 in the worst case (Theorem 6) | $3\omega - 2$ (Kierstead and Trotter) | $3\omega - 2$ |
| general | $\chi$ | $n/2$ already for $\chi = 2$ | ratio $O(n / \log^* n)$ | ratio $\Omega(n / \log^2 n)$, also randomized |

## Reductions

- **To offline coloring.** A polynomial-time online algorithm is also an offline algorithm. So the [hardness of graph coloring](/graph-coloring-inapproximability/), no ratio $n^{1 - \varepsilon}$ in polynomial time unless P = NP, holds for polynomial-time online algorithms. The lower bounds above hold without any limit on time.
- **To online independent set.** The color classes of an online coloring are independent sets built online. With $\chi'$ colors, one class has at least $n / \chi'$ vertices, but it is not known in advance which one. So an online coloring gives an algorithm in the multi-solution model of [online independent set](/online-independent-set-problem/), with one set per color.
- **Interval graphs and storage.** Coloring intervals online is the same as giving each arriving interval of time a slot, such as a memory block or a channel, that is free during the whole interval. Interval graphs are chordal, and offline they are colored optimally as in [chordal graph coloring](/chordal-graph-coloring/).
- **Degenerate graphs.** On a [$d$-degenerate](/degeneracy/) graph, First Fit in a good order uses $d + 1$ colors, but in an adversarial order it uses $O(d \log n)$ colors, and this is the best order of growth for deterministic algorithms (Irani, 1994).

## Applications

- **Scheduling and storage allocation.** Jobs or memory requests with time intervals arrive one by one, and each must get a machine or a block that it keeps. The number of colors is the number of machines or blocks.
- **Frequency assignment.** Transmitters that interfere must get different frequencies, and new transmitters come into use over time. Disk graphs model the interference.
- **Register allocation in a single pass.** A compiler that assigns registers to live ranges as it reads the code, without going back, colors an interval graph online. When the ranges arrive in order of their start, First Fit uses only $\omega$ colors, as in the interval coloring depth theorem. The bounds above apply when the order is arbitrary.

## References
