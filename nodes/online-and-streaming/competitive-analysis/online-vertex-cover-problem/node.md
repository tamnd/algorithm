---
tag: 6GN3JT
kind: problem
slug: online-vertex-cover-problem
name: Online vertex cover problem
aliases:
- online vertex cover
- online vertex cover with edge arrivals
- online vertex cover with vertex arrivals
area: online-and-streaming/competitive-analysis
level: advanced
summary: The edges of a graph are revealed online and a vertex cover must be kept, adding vertices but never removing them. Taking both endpoints of each uncovered edge is 2-competitive.
prereqs: [vertex-cover, online-algorithm, competitive-ratio]
see_also: [online-set-cover-problem, online-independent-set-problem, vertex-cover-2-approximation, bar-yehuda-even-vertex-cover, online-bipartite-matching, maximal-matching, vertex-cover-inapproximability, yao-minimax-principle]
sources:
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: "Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2) (1981), 198-203"
    locator: the local-ratio algorithm that raises the price of each uncovered edge until an endpoint is paid for, which works edge by edge and so online
  - paper: doi:10.1007/978-3-662-47672-7_87
    title: "Yajun Wang and Sam Chiu-wai Wong, Two-sided online bipartite matching and vertex cover: beating the greedy algorithm, ICALP 2015, LNCS 9134, 1070-1081"
    locator: the vertex arrival model, the fractional algorithm with ratio about 1.901, and the lower bound 1 + sqrt((1 + e^-2)/2)
  - url: https://arxiv.org/abs/2608.04994
    title: "Zhihao Gavin Tang and Yuhao Zhang, A tight bound on online vertex cover under edge arrivals, arXiv preprint 2608.04994 (2026)"
    locator: the abstract (no randomized integral or fractional algorithm beats 2 under edge arrivals, even on bipartite graphs)
  - url: https://arxiv.org/abs/2608.09210
    title: "Tianhang Lu, A new lower bound for online vertex cover under vertex arrivals, arXiv preprint 2608.09210 (2026)"
    locator: the abstract and the introduction (the lower bound 1 + sqrt(e)/2 under vertex arrivals, and the earlier bounds)
---

Online vertex cover is the problem of keeping a [vertex cover](/vertex-cover/) of a graph that is revealed piece by piece. The cover may grow, but a vertex that was put in it stays there, and after each step every revealed edge must have an endpoint in the cover. The goal is a cover of small size or weight compared with the best cover of the whole graph. The model matters. When edges arrive and the algorithm may add any vertex, taking both endpoints of each uncovered edge is 2-competitive, and no deterministic algorithm does better. The same bound holds for weighted vertices by an online form of the algorithm of Bar-Yehuda and Even. When each vertex must be put in or left out for good at its arrival, no algorithm has a bounded ratio. Online vertex cover is the case $d = 2$ of [online set cover](/online-set-cover-problem/).

## In plain words

A guard service watches roads between towns. Roads are announced one at a time, and each new road must be watched at once by a guard in one of its two end towns. A guard, once placed, stays. The service wants few guards, compared with the fewest guards that would watch all the roads.

A simple rule works well: when a new road has no guard at either end, put a guard at both ends. The roads that trigger this rule share no town, and the best plan needs a separate guard for each of them. So the rule uses at most twice as many guards as the best plan. If a town must be given its guard, or refused one forever, at the moment it is announced, no rule can stay within any fixed factor of the best plan.

## Definition

**Graph and cost.** A graph $G = (V, E)$ with a weight $w_v > 0$ for each vertex, or $w_v = 1$ in the unweighted case. A cover $C$ costs $w(C) = \sum_{v \in C} w_v$. $\mathrm{OPT}$ is the least cost of a vertex cover of the revealed graph. An algorithm is $\rho$-competitive if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on each input, with no additive term; a randomized algorithm needs $\mathbb{E}[\mathrm{ALG}] \le \rho \cdot \mathrm{OPT}$ against an [oblivious adversary](/oblivious-adversary/).

**Edge arrival model.** The edges $e_1, e_2, \ldots$ arrive one at a time. A vertex is known, with its weight, when the first edge that touches it arrives. After the arrival of $e_t$, the algorithm may add any revealed vertices to $C$, and then $C$ must cover $e_1, \ldots, e_t$. Vertices are never removed.

**Vertex arrival model.** The vertices $v_1, v_2, \ldots$ arrive one at a time, and $v_t$ arrives with its edges to $v_1, \ldots, v_{t-1}$. After the arrival, the algorithm may add $v_t$ or any earlier vertex to $C$, and then $C$ must cover all revealed edges. An algorithm for the edge arrival model also works here, if it treats the edges of $v_t$ one by one, so each upper bound of the edge model holds in this model. A lower bound in this model also holds for edge arrivals. So this model is at least as easy for the algorithm. It is the model of Wang and Wong (2015).

**Decide-on-arrival model.** As in the vertex arrival model, but the decision about $v_t$ is made only at its arrival: $v_t$ joins $C$ now or never. If an edge $(v_s, v_t)$ arrives with $v_s \notin C$, the algorithm must take $v_t$. The vertices left out form an independent set, so this model is the complement of [online independent set](/online-independent-set-problem/) in the same arrival order.

**Fractional version.** The algorithm keeps values $x_v \in [0, 1]$, which may only increase, with $x_u + x_v \ge 1$ for each revealed edge, at cost $\sum_v w_v x_v$. It is the dual of fractional online matching in the same model.

## Variants

- **Unweighted or weighted.** In the edge arrival model the best deterministic ratio is 2 in both cases.
- **Bipartite graphs.** The lower bounds below hold even for bipartite graphs. In the one-sided model, where one side is known in advance and the other side arrives, the fractional cover problem is the dual of online fractional matching; see the reductions below.
- **Fractional.** The fractional version under vertex arrivals is where the bound 2 can be beaten; see Theorem 5.
- **Recourse and dynamic graphs.** If the algorithm may also remove vertices, or edges may be deleted, the problem becomes [dynamic vertex cover](/dynamic-vertex-cover/), where the measure is update time and not the competitive ratio.

## Examples

**The rule "both endpoints".** Edges arrive in the order $ab$, $bc$, $cd$, $de$ on the path $a b c d e$.

| edge | covered before? | added | $C$ after |
|---|---|---|---|
| $ab$ | no | $a, b$ | $a, b$ |
| $bc$ | yes, by $b$ | none | $a, b$ |
| $cd$ | no | $c, d$ | $a, b, c, d$ |
| $de$ | yes, by $d$ | none | $a, b, c, d$ |

The rule picks the matching $\{ab, cd\}$ and pays 4. The optimum $\{b, d\}$ pays 2, so the ratio 2 is reached on this input.

**The adversary for one endpoint.** The first edge is $ab$. A deterministic algorithm that takes only $a$ then sees the edge $b \ell$. It must take $b$ or $\ell$, so it pays 2, while $\{b\}$ covers both edges and $\mathrm{OPT} = 1$. Taking both $a$ and $b$ at the first edge costs 2 as well.

## Known algorithms

- **Both endpoints of each uncovered edge** (unweighted, edge or vertex arrival). The added edges form a [maximal matching](/maximal-matching/) of the revealed graph. Ratio 2. This is the online form of the offline [2-approximation](/vertex-cover-2-approximation/).
- **Online primal-dual of Bar-Yehuda and Even** (weighted). For each uncovered edge $uv$, raise its price $y_{uv}$ by the smaller remaining slack of $u$ and $v$, and add the endpoints whose slack reaches 0. Ratio 2 (Theorem 2). With unit weights it takes both endpoints, as the first rule.
- **Wang and Wong's fractional algorithm** (fractional, vertex arrival). A water-filling rule for the fractional matching, whose dual is a fractional cover with ratio $1/\Gamma^* \approx 1.901$.

## Bounds

**Theorem 1 (ratio 2, unweighted).** In the edge arrival model, and so in the vertex arrival model, the rule "both endpoints of each uncovered edge" keeps a vertex cover with $\lvert C \rvert \le 2 \cdot \mathrm{OPT}$.

*Proof.* After an edge $uv$ arrives, either it is covered or the rule adds $u$ and $v$, so $C$ is a cover at each step. Let $M$ be the set of edges for which the rule added both endpoints. When $uv$ is added to $M$, neither $u$ nor $v$ is in $C$, so $uv$ shares no vertex with an earlier edge of $M$. So $M$ is a matching, and $\lvert C \rvert = 2 \lvert M \rvert$. Each cover, in particular an optimal one, has a distinct vertex on each edge of $M$, so $\mathrm{OPT} \ge \lvert M \rvert$. $\square$

**Theorem 2 (ratio 2, weighted).** In the edge arrival model, the online primal-dual rule keeps a vertex cover with $w(C) \le 2 \cdot \mathrm{OPT}$.

*Proof.* This is Theorem 2 of [online set cover](/online-set-cover-problem/) with each vertex as the set of its edges, so each element lies in $d = 2$ sets. In brief: the slack of a vertex is $w_v - \sum_{e \ni v} y_e$, and it never becomes negative, so $y$ is a feasible fractional matching of the dual and $\sum_e y_e \le \mathrm{OPT}$. Each vertex in $C$ has slack 0, so $w(C) = \sum_{v \in C} \sum_{e \ni v} y_e \le 2 \sum_e y_e$. The rule is online, because each step reads only the slacks of the two endpoints of the new edge. $\square$

**Theorem 3 (no deterministic algorithm beats 2).** For each deterministic algorithm in the edge arrival model, unweighted, and each $k \ge 1$, there is an input with $\mathrm{OPT} = k$ on which the algorithm pays at least $2k$.

*Proof.* Use $k$ disjoint copies of the adversary of the examples. In copy $i$, the first edge is $a_i b_i$. If the algorithm takes both, the copy ends. If it takes only one endpoint, say $a_i$, the adversary sends one edge $b_i \ell_i$ with a new vertex $\ell_i$, and the algorithm must take $b_i$ or $\ell_i$. In each case the copy costs the algorithm at least 2, and one vertex ($b_i$, or $a_i$ in the symmetric case, or either one if the copy ended) covers it, so its optimum is 1. The copies share no vertex, so $\mathrm{OPT} = k$ and $\mathrm{ALG} \ge 2k$. $\square$

**Theorem 4 (randomized algorithms, edge arrival).** Each randomized algorithm in the edge arrival model has ratio at least $3/2$ against an oblivious adversary. A 2026 preprint of Tang and Zhang states the tight bound: no randomized algorithm, integral or fractional, has ratio below 2, even on bipartite graphs.

*Proof of 3/2.* By [Yao's principle](/yao-minimax-principle/) it is enough to give a distribution over inputs on which each deterministic algorithm pays at least $3/2$ in expectation, with $\mathrm{OPT} = 1$ on each input; repeating $k$ independent disjoint copies removes any additive constant. The input is the edge $ab$ followed by one edge $a\ell$ or $b\ell$, each with probability $1/2$, where $\ell$ is a new vertex. After the first edge, the algorithm holds $a$, $b$ or both. If it holds both, it pays 2. If it holds $a$, it pays 1 when the second edge is $a\ell$, and 2 when it is $b\ell$, as in Theorem 3. The same holds for $b$. So the expected cost is at least $\frac{1}{2} \cdot 1 + \frac{1}{2} \cdot 2 = 3/2$, and the optimum is 1 on both inputs. $\square$

The preprint closes the gap between $3/2$ and 2 by a reduction from a lower bound construction for online matching under edge arrivals. It is not yet refereed.

**Theorem 5 (vertex arrival).** In the vertex arrival model, Theorem 1 and Theorem 2 still give ratio 2. For the fractional version, Wang and Wong (2015) gave an algorithm with ratio $1/\Gamma^* \approx 1.901$, and showed that no algorithm, even randomized and even on bipartite graphs, has ratio below $1 + \sqrt{(1 + e^{-2})/2} \approx 1.7534$. A 2026 preprint of Lu raises the lower bound to $1 + \sqrt{e}/2 \approx 1.8244$. These are cited results, not proved here. Whether an integral randomized algorithm beats 2 in this model is not settled on this page.

**Theorem 6 (decide-on-arrival: no bounded ratio).** In the decide-on-arrival model, unweighted, no deterministic algorithm and no randomized algorithm against an oblivious adversary has a bounded competitive ratio.

*Proof for deterministic algorithms.* Fix $N$. The adversary sends isolated vertices $c_1, c_2, \ldots$. If the algorithm takes each of $c_1, \ldots, c_N$, the adversary ends with one edge between two new vertices: $\mathrm{OPT} = 1$ and $\mathrm{ALG} \ge N + 1$. If the algorithm leaves out some $c_i$ with $i \le N$, the adversary sends $N$ new vertices, each with one edge to $c_i$. The algorithm cannot take $c_i$ any more, so it must take all $N$ leaves, while $\{c_i\}$ covers every edge: $\mathrm{OPT} = 1$ and $\mathrm{ALG} \ge N$. $\square$

*Proof for randomized algorithms.* Fix $N \ge 4$ and let $q_i$ be the probability that the algorithm takes $c_i$ when it has seen the isolated vertices $c_1, \ldots, c_i$. These numbers are fixed by the algorithm alone. Input $B$ is $c_1, \ldots, c_N$ and then one edge between two new vertices, so $\mathrm{OPT} = 1$ and $\mathbb{E}[\mathrm{ALG}] \ge \sum_{i \le N} q_i$. Input $A_i$ is $c_1, \ldots, c_i$ and then $N$ leaves on $c_i$, so $\mathrm{OPT} = 1$ and $\mathbb{E}[\mathrm{ALG}] \ge (1 - q_i) N$, because the leaves are forced when $c_i$ is left out. If $\sum_i q_i \ge \sqrt{N}$, input $B$ gives ratio at least $\sqrt{N}$. Otherwise some $q_i < 1/\sqrt{N}$, and $A_i$ gives ratio more than $N - \sqrt{N} \ge \sqrt{N}$. Each input is fixed in advance, so the adversary is oblivious. As $N$ is arbitrary, the ratio is unbounded. $\square$

**Offline hardness applies.** A polynomial-time online algorithm is also an offline approximation algorithm. So the [hardness of vertex cover](/vertex-cover-inapproximability/), a ratio $2 - \varepsilon$ under the Unique Games Conjecture, holds for polynomial-time online algorithms. Theorems 3 and 4 need no such assumption.

| model | upper bound | lower bound |
|---|---|---|
| edge arrival, deterministic | 2 (Theorems 1 and 2) | 2 (Theorem 3) |
| edge arrival, randomized | 2 | $3/2$ (Theorem 4); 2 in a 2026 preprint |
| vertex arrival, fractional | about 1.901 (Wang and Wong) | about 1.7534 (Wang and Wong); 1.8244 in a 2026 preprint |
| decide on arrival | unbounded | unbounded (Theorem 6) |

## Reductions

- **To online set cover.** Each vertex is the set of its edges, with $d = 2$. The online primal-dual rule of [online set cover](/online-set-cover-problem/) with ratio $d$ becomes Theorem 2.
- **Matching duality.** The LP dual of fractional vertex cover is fractional matching. In the one-sided model of [online bipartite matching](/online-bipartite-matching/), the dual of the water-filling algorithm (the fractional form of [Balance](/balance-algorithm/)) gives each offline vertex a value that only grows and each online vertex a value fixed at its arrival, and these values cover each edge. So they form an online fractional cover whose cost is at most $e/(e - 1)$ times the fractional matching, and so at most $e/(e-1)$ times the fractional optimum of the cover.
- **Complement of independent set.** In the decide-on-arrival model, the vertices that are left out form an independent set, and each online independent set algorithm gives a cover by taking the rest. The ratios do not carry over, because a cover of size $n - \alpha$ can be near optimal while an independent set of size $\alpha/2$ is poor, and the other way round.

## Applications

- **Monitoring links.** Placing monitors at the ends of network links as new links come up, so that each link is watched.
- **Conflict resolution.** Each new conflict between two requests must be removed by dropping one of them, and dropped requests stay dropped; the dropped set is a vertex cover of the conflict graph.
- **A test case for online covering.** It is the smallest case of online set cover, and the results above show how the model of arrival changes the answer.

## References
