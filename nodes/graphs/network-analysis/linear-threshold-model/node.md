---
tag: 7YPBAT
kind: model
slug: linear-threshold-model
name: Linear threshold model
aliases:
- LT model
area: graphs/network-analysis
level: advanced
summary: A node activates when the weighted fraction of active neighbours exceeds a random threshold.
prereqs: [directed-graph, weighted-graph, probability-space]
see_also: [independent-cascade-model, influence-maximization, greedy-influence-maximization, submodular-function, homophily, epidemic-model, directed-acyclic-graph, vertex-cover]
sources:
  - paper: doi:10.1086/226707
    title: Mark Granovetter, Threshold models of collective behavior, American Journal of Sociology 83(6), 1420 to 1443 (1978)
    locator: the whole paper (each person joins once the fraction of others who joined reaches a personal threshold, and the distribution of thresholds decides the outcome)
  - paper: doi:10.1145/956750.956769
    title: David Kempe, Jon Kleinberg and Éva Tardos, Maximizing the spread of influence through a social network, Proceedings of the 9th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 137 to 146 (2003)
    locator: Section 2 (the linear threshold model with uniform random thresholds, its live-edge equivalence, the submodularity of the spread, and the NP-hardness of influence maximization by a reduction from vertex cover)
  - paper: doi:10.1109/ICDM.2010.118
    title: Wei Chen, Yifei Yuan and Li Zhang, Scalable influence maximization in social networks under the linear threshold model, Proceedings of the 10th IEEE International Conference on Data Mining, 88 to 97 (2010)
    locator: the #P-hardness of computing the spread under the linear threshold model, and the linear-time computation of the spread in a directed acyclic graph (the LDAG heuristic)
  - paper: doi:10.1073/pnas.082090499
    title: Duncan J. Watts, A simple model of global cascades on random networks, Proceedings of the National Academy of Sciences 99(9), 5766 to 5771 (2002)
    locator: the fractional threshold rule on random graphs and the cascade window in the mean degree
  - paper: doi:10.1111/1467-937X.00121
    title: Stephen Morris, Contagion, Review of Economic Studies 67(1), 57 to 78 (2000)
    locator: best-response dynamics of a coordination game on a network, the contagion threshold, and the cohesive sets that block contagion
  - paper: doi:10.1145/1250790.1250811
    title: Elchanan Mossel and Sebastien Roch, On the submodularity of influence in social networks, Proceedings of the 39th Annual ACM Symposium on Theory of Computing, 128 to 134 (2007)
    locator: the proof that the spread is submodular in the general threshold model whenever every local threshold function is monotone and submodular
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 19, Cascading behavior in networks (threshold adoption from a coordination game, cascades, and clusters that block them)
---

The linear threshold model is a random process on a [directed graph](/directed-graph/) with arc weights, in which a vertex becomes active once the total weight of its active in-neighbours reaches its own threshold. The weights into each vertex sum to at most 1, and each threshold is drawn uniformly at random from $[0, 1]$ once, at the start; after that the process is deterministic. It formalizes the threshold models of collective behaviour of Granovetter (1978), and Kempe, Kleinberg and Tardos made it, with the [independent cascade model](/independent-cascade-model/), one of the two standard models of [influence maximization](/influence-maximization/). Its expected spread $\sigma(S)$ is a monotone [submodular function](/submodular-function/), because the model is equivalent to reachability in a random graph where each vertex keeps at most one in-arc.

## The machine

**Parameters.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ arcs, a weight $b_{uv} \ge 0$ on each arc with $\sum_{u} b_{uv} \le 1$ for every vertex $v$, and a seed set $S \subseteq V$. A common choice is $b_{uv} = 1/d^{\mathrm{in}}(v)$, which makes the condition "a fraction $\theta_v$ of my in-neighbours is active". An undirected network is used with both arcs of each edge.

**One run.**

1. Draw a threshold $\theta_v$ uniformly from $[0, 1]$ for every vertex $v$, independently.
2. At step 0, the vertices of $S$ are active.
3. At step $t \ge 1$, every inactive vertex $v$ with $\sum_{u \text{ active}} b_{uv} \ge \theta_v$ becomes active, where the sum runs over the in-neighbours active after step $t - 1$.
4. The run stops at the first step that activates nobody.

Active vertices stay active, so the run stops after at most $n$ steps. A simulation keeps for each vertex the weight of its active in-neighbours, and adds $b_{uv}$ to it when $u$ becomes active, so one run takes $O(n + m)$ time.

**Ties in the same step.** All vertices of a step are tested against the same active set, and the test is a monotone function of that set, so the order in which they are tested does not matter. Activating them one at a time instead of in rounds gives the same final set, but possibly different step counts.

**The live-edge view.** Let every vertex $v$ independently keep at most one in-arc: the arc $(u, v)$ with probability $b_{uv}$, and no arc with probability $1 - \sum_u b_{uv}$. Then the final active set has the same distribution as the set of vertices reachable from $S$ along kept arcs. Kempe, Kleinberg and Tardos prove it by showing that both processes grow their active sets with the same probabilities: given that $v$ is still inactive after step $t$, it joins at step $t + 1$ with probability $\sum_{u \in A_t \setminus A_{t-1}} b_{uv} / (1 - \sum_{u \in A_{t-1}} b_{uv})$ in both, where $A_t$ is the active set after step $t$. The full argument is in the proof page of [greedy influence maximization](/greedy-influence-maximization/).

## What it counts

The main quantity is the **spread** $\sigma(S)$, the expected number of active vertices at the end, seeds included. By the live-edge view,

$$\sigma(S) = \sum_{v \in V} \Pr[v \text{ is reachable from } S \text{ by kept arcs}].$$

**Paths.** In the live-edge graph each vertex has at most one in-arc, so following kept arcs backwards from $v$ gives a single chain. Hence $v \notin S$ is active exactly when this chain reaches $S$, and the events for different paths are disjoint:

$$\Pr[v \text{ active}] = \sum_{P} \prod_{(x, y) \in P} b_{xy},$$

over the simple paths $P$ that start in $S$, end at $v$, and have no other vertex in $S$. In a [directed acyclic graph](/directed-acyclic-graph/), this gives the recurrence $\Pr[v \text{ active}] = \sum_u b_{uv} \Pr[u \text{ active}]$ for $v \notin S$, which is computed in [topological order](/topological-sort/) in $O(n + m)$ time.

**Example.** Take the vertices 0 to 5 and the arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$ and $5 \to 4$, each with weight $1/2$; the weights into 3 and into 4 sum to 1. This is the graph of the [independent cascade](/independent-cascade-model/) example, with the probabilities read as weights. The graph is acyclic, so the recurrence gives the activation probabilities from $S = \{0\}$:

| vertex | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| linear threshold | 1 | $\frac12$ | $\frac12$ | $\frac12 \cdot \frac12 + \frac12 \cdot \frac12 = \frac12$ | $\frac12 \cdot \frac12 = \frac14$ | 0 |
| independent cascade | 1 | $\frac12$ | $\frac12$ | $\frac{7}{16}$ | $\frac{7}{32}$ | 0 |

So $\sigma(\{0\}) = 11/4$ under the threshold model, against $85/32$ under the cascade. The difference is at vertex 3: with both 1 and 2 active, the weight $1/2 + 1/2 = 1$ always passes the threshold, while in the cascade the two tries can both fail. The other single seeds have the same spreads in both models: $7/4$ for 1 and 2, $3/2$ for 3 and 5, and 1 for 4. The best pair is $\{0, 5\}$ with $\sigma = 17/4$, and adding 3 to $\{0\}$ gains only $3/4$, half of $\sigma(\{3\}) = 3/2$.

**Fixed thresholds.** If the thresholds are fixed instead of random, the run is deterministic, and the output is the final active set itself. Granovetter's riot example has thresholds $0, 1, 2, \dots, 99$ in a crowd of 100 (in numbers of people): everyone joins one after another. Changing the threshold 1 into 2 stops the riot after one person.

## Relation to other models

- **[Independent cascade model](/independent-cascade-model/).** Both models have live-edge views and submodular spreads; both are cases of the *triggering model* of Kempe, Kleinberg and Tardos, where each vertex draws a random set of in-neighbours that can trigger it. In the cascade the set has each in-neighbour independently; in the threshold model it has at most one. On the example above, the threshold model spreads further through vertex 3, where two active in-neighbours add up.
- **General threshold model.** Each vertex has a monotone function $f_v$ of its set of active in-neighbours, with $f_v(\emptyset) = 0$, and activates when $f_v$ of that set reaches $\theta_v$. The linear model is $f_v(A) = \sum_{u \in A} b_{uv}$. Mossel and Roch proved the conjecture of Kempe, Kleinberg and Tardos that the spread is submodular whenever every $f_v$ is submodular.
- **Fixed and integer thresholds.** Granovetter's model, the fractional threshold model of Watts on random graphs, and *bootstrap percolation*, where a vertex activates with at least $r$ active neighbours, use fixed thresholds. Their spreads are not submodular: with threshold 2, two seeds next to a vertex activate it, while each alone does not.
- **Coordination games.** Morris and the book of Easley and Kleinberg derive a fractional threshold from a game: a vertex adopts a behaviour when at least a fraction $q$ of its neighbours have, where $q$ depends on the payoffs. Dense clusters with too few outside links block such cascades, which links the model to [homophily](/homophily/).
- **[Epidemic models](/epidemic-model/).** The threshold rule models complex contagion, where several contacts are needed, while the independent cascade and the SIR model are simple contagion, where one contact can suffice.

## Known results in the model

| question | result |
|---|---|
| spread as a set function | monotone and submodular, with $\sigma(\emptyset) = 0$ (Kempe, Kleinberg and Tardos, 2003) |
| computing $\sigma(S)$ exactly | #P-hard in general graphs (Chen, Yuan and Zhang, 2010) |
| computing $\sigma(S)$ in a directed acyclic graph | $O(n + m)$ by the recurrence above |
| [influence maximization](/influence-maximization/) | NP-hard, by a reduction from [vertex cover](/vertex-cover/) |
| approximation | [greedy](/greedy-influence-maximization/) gives $1 - 1/e - \varepsilon$ with Monte Carlo estimates |
| general threshold model with submodular $f_v$ | spread submodular (Mossel and Roch, 2007) |
| fractional fixed thresholds on random graphs | global cascades occur only in a window of mean degrees (Watts, 2002) |

**The vertex cover reduction.** Take an undirected graph $H$ with no isolated vertex, give it both arcs of each edge, and set $b_{uv} = 1/d(v)$. If $S$ is a vertex cover, every other vertex has all its neighbours in $S$, so its active weight is 1 at step 1 and it activates for sure; so $\sigma(S) = n$. If $S$ is not a cover, an edge $\{u, v\}$ has both ends outside $S$, and with positive probability $\theta_u > 1 - 1/d(u)$ and $\theta_v > 1 - 1/d(v)$. Then the other neighbours of $u$ give it weight at most $1 - 1/d(u) < \theta_u$, so $u$ can only join after $v$, and likewise $v$ only after $u$; neither joins, and the run ends with fewer than $n$ active vertices; so $\sigma(S) < n$. Hence $H$ has a vertex cover of size $k$ exactly when some $k$ seeds have spread $n$.

**A first run by hand.** In the example, start from $\{0\}$ and say the thresholds of 1 to 4 are $0.3, 0.8, 0.4, 0.6$. At step 1, vertex 1 has weight $1/2 \ge 0.3$ and joins; vertex 2 has $1/2 < 0.8$ and does not. At step 2, vertex 3 has weight $1/2 \ge 0.4$ and joins. At step 3, vertex 4 has weight $1/2 < 0.6$ and does not. The run stops with $\{0, 1, 3\}$.

## References
