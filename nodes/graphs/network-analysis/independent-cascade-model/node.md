---
tag: RHW0NJ
kind: model
slug: independent-cascade-model
name: Independent cascade model
aliases:
- IC model
area: graphs/network-analysis
level: advanced
summary: Each newly active node gets one independent chance to activate each neighbour.
prereqs: [directed-graph, probability-space, breadth-first-search]
see_also: [linear-threshold-model, influence-maximization, greedy-influence-maximization, sir-epidemic-model, percolation, epidemic-model, submodular-function, erdos-renyi-model]
sources:
  - paper: doi:10.1023/A:1011122126881
    title: Jacob Goldenberg, Barak Libai and Eitan Muller, Talk of the network, a complex systems look at the underlying process of word-of-mouth, Marketing Letters 12(3), 211 to 223 (2001)
    locator: the cellular-automaton model of word of mouth in which each informed person passes the news to each contact with a fixed probability, the origin of the independent cascade model
  - paper: doi:10.1145/956750.956769
    title: David Kempe, Jon Kleinberg and Éva Tardos, Maximizing the spread of influence through a social network, Proceedings of the 9th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 137 to 146 (2003)
    locator: Section 2 (the definition of the independent cascade model, the live-edge equivalence, the submodularity of the spread, and the NP-hardness of influence maximization by a reduction from set cover)
  - paper: doi:10.1007/11523468_91
    title: David Kempe, Jon Kleinberg and Éva Tardos, Influential nodes in a diffusion model for social networks, Proceedings of the 32nd International Colloquium on Automata, Languages and Programming, Lecture Notes in Computer Science 3580 (2005)
    locator: the general cascade model, the decreasing cascade model and the equivalence of the general cascade and general threshold models
  - paper: doi:10.1145/1835804.1835934
    title: Wei Chen, Chi Wang and Yajun Wang, Scalable influence maximization for prevalent viral marketing in large-scale social networks, Proceedings of the 16th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 1029 to 1038 (2010)
    locator: "the #P-hardness of computing the spread under the independent cascade model, by a reduction from s-t connectedness in a random graph"
  - paper: doi:10.1103/PhysRevE.66.016128
    title: M. E. J. Newman, Spread of epidemic disease on networks, Physical Review E 66(1), 016128 (2002)
    locator: the mapping of the SIR model with transmissibility T to bond percolation, and the outbreak threshold for random graphs with a given degree distribution
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 19, Cascading behavior in networks, and Chapter 21, Epidemics (the branching process and the SIR model on a network)
---

The independent cascade model is a random process on a [directed graph](/directed-graph/) in which activity spreads from a set of seed vertices. Each arc $(u, v)$ carries a probability $p_{uv}$, and when $u$ becomes active it gets exactly one chance to activate $v$, which succeeds with probability $p_{uv}$, independently of everything else. The process stops when a step activates nobody. Goldenberg, Libai and Muller used it in 2001 to model word of mouth, and Kempe, Kleinberg and Tardos made it, together with the [linear threshold model](/linear-threshold-model/), the standard model of [influence maximization](/influence-maximization/). Its central quantity is the expected number of active vertices, the spread $\sigma(S)$, which is a monotone [submodular function](/submodular-function/) of the seed set.

## The machine

**Parameters.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ arcs, a probability $p_{uv} \in [0, 1]$ on each arc, and a seed set $S \subseteq V$. An undirected network is used with both arcs of each edge, possibly with different probabilities. Common choices are a uniform $p_{uv} = p$; the *weighted cascade* $p_{uv} = 1/d^{\mathrm{in}}(v)$, where $d^{\mathrm{in}}(v)$ is the in-degree; and the *trivalency* model, where each $p_{uv}$ is drawn from $\{0.1, 0.01, 0.001\}$.

**One run.** Every vertex is inactive or active, and an active vertex stays active.

1. At step 0, the vertices of $S$ are active, and they form the set $A_0$ of newly active vertices.
2. At step $t \ge 1$, each vertex $u$ that became active at step $t - 1$ tries, for each out-neighbour $v$ that is still inactive, to activate $v$; the try succeeds with probability $p_{uv}$, independently of all other tries.
3. The vertices activated at step $t$ form $A_t$. The run stops at the first step with $A_t = \emptyset$.

Each arc is tried at most once, at the step after its tail becomes active, and only if its head is still inactive. So the run stops after at most $n$ steps, and one simulation by [breadth-first search](/breadth-first-search/) takes $O(n + m)$ time.

**Ties in the same step.** Several new vertices may try the same inactive $v$ in one step. The order of these tries does not matter: $v$ joins at that step with probability $1 - \prod_u (1 - p_{uv})$ over the tries, whatever the order, and later steps only use the fact that $v$ is active.

**The live-edge view.** Flip the coin of every arc in advance: keep $(u, v)$ as *live* with probability $p_{uv}$, independently. Then the final active set has the same distribution as the set of vertices reachable from $S$ along live arcs. The reason is that each coin of the run is flipped at most once and is independent of the others, so flipping it early does not change anything; a vertex is then active at the end exactly when a live path leads to it from $S$. This view turns the model into directed [bond percolation](/percolation/) and is the key to most results about it.

## What it counts

The main quantity is the **spread**

$$\sigma(S) = \mathbb{E}\bigl[\,|A_0 \cup A_1 \cup \cdots|\,\bigr] = \sum_{v \in V} \Pr[v \text{ is reachable from } S \text{ by live arcs}],$$

the expected number of active vertices at the end, seeds included. Other quantities are the activation probability of each vertex, the distribution of the final size, and the number of steps, which is the length of the longest shortest live path from $S$.

**Example.** Take the vertices 0 to 5 and the arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$ and $5 \to 4$, each with $p = 1/2$. This graph is the running example of [the greedy method](/greedy-influence-maximization/) and of the [linear threshold model](/linear-threshold-model/).

| vertex | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $\Pr[\text{active}]$ from $S = \{0\}$ | 1 | $\frac12$ | $\frac12$ | $\frac{7}{16}$ | $\frac{7}{32}$ | 0 |

Vertex 3 is reached when one of the two paths $0 \to 1 \to 3$ and $0 \to 2 \to 3$ is live; each is live with probability $1/4$, and they share no arc, so the probability is $1 - (3/4)^2 = 7/16$. Summing the row gives $\sigma(\{0\}) = 85/32 \approx 2.66$. The other single seeds have $\sigma(\{1\}) = \sigma(\{2\}) = 7/4$, $\sigma(\{3\}) = \sigma(\{5\}) = 3/2$ and $\sigma(\{4\}) = 1$, and the best pair is $\{0, 5\}$ with $\sigma = 259/64 \approx 4.05$.

**Monotone and submodular.** For a fixed set $L$ of live arcs, the number of vertices reachable from $S$ is a coverage function: it is the size of a union of one set per seed, so adding a seed to a larger set adds fewer new vertices. The spread is an average of such functions with non-negative weights, so it is monotone, $\sigma(S) \le \sigma(T)$ for $S \subseteq T$, and submodular, $\sigma(S \cup \{v\}) - \sigma(S) \ge \sigma(T \cup \{v\}) - \sigma(T)$. In the example, adding 3 to $\{0\}$ gains $27/32$, less than $\sigma(\{3\}) = 3/2$, since 0 often reaches 3 by itself.

**Estimating the spread.** Exact computation is #P-hard. The usual estimate runs $r$ independent simulations and averages the final sizes. Each size lies in $[|S|, n]$, so by the [Hoeffding inequality](/hoeffding-inequality/) $r = O(n^2 \varepsilon^{-2} \log(1/\eta))$ runs give an additive error of $\varepsilon$ with probability $1 - \eta$; far fewer runs suffice in practice.

## Relation to other models

- **[Percolation](/percolation/).** By the live-edge view, the cascade from a single seed is the cluster of that seed in directed bond percolation, where each arc stays with probability $p_{uv}$. With uniform $p$ on an undirected graph, the final active set from $v$ is the connected component of $v$ in the random subgraph.
- **[Erdős-Rényi model](/erdos-renyi-model/).** On the complete graph $K_n$ with uniform $p$, the live arcs in both directions of an edge are independent, so the cascade differs slightly from $G(n, p)$; if both arcs of an edge share one coin, the final set is exactly the component of the seed in $G(n, p)$, and a large cascade appears when $p > 1/n$, as the [giant component](/giant-component/) does.
- **[SIR epidemic model](/sir-epidemic-model/).** An SIR epidemic in discrete time, where an infected vertex infects each susceptible neighbour with probability $T$ during its one infectious step and then recovers, is exactly the independent cascade with $p_{uv} = T$. Newman showed that SIR with any fixed infectious period maps to bond percolation with transmissibility $T$, so its final size has the same distribution as an independent cascade.
- **[Linear threshold model](/linear-threshold-model/).** Both models have live-edge views and submodular spreads. In the cascade each arc is live independently; in the threshold model each vertex keeps at most one in-arc. Both are special cases of the *triggering model* of Kempe, Kleinberg and Tardos, where each vertex picks a random set of in-neighbours that can trigger it.
- **General and decreasing cascades.** In the general cascade model, the chance that $u$ activates $v$ may depend on the set of vertices that already tried $v$. Kempe, Kleinberg and Tardos showed that general cascades and general threshold models describe the same processes, and that the spread stays submodular when these chances decrease as more vertices try (the decreasing cascade model).
- **Branching processes.** On a tree-like graph, the number of new activations per active vertex behaves like a Galton-Watson process; a large cascade has positive probability exactly when the mean number of offspring is above 1.

## Known results in the model

| question | result |
|---|---|
| spread as a set function | monotone and submodular, with $\sigma(\emptyset) = 0$ (Kempe, Kleinberg and Tardos, 2003) |
| computing $\sigma(S)$ exactly | #P-hard (Chen, Wang and Wang, 2010), even for a single seed |
| estimating $\sigma(S)$ | Monte Carlo simulation in $O(r(n + m))$ time with $r$ runs |
| [influence maximization](/influence-maximization/) | NP-hard; contains maximum coverage when all $p_{uv} = 1$ on a bipartite graph |
| approximation | [greedy](/greedy-influence-maximization/) gives $1 - 1/e - \varepsilon$; no polynomial-time method beats $1 - 1/e$ unless P = NP |
| large cascades on random graphs with given degrees | a giant outbreak has positive probability when $T\, \frac{\mathbb{E}[d^2] - \mathbb{E}[d]}{\mathbb{E}[d]} > 1$ (Newman, 2002) |

**Why exact computation is hard.** With a single seed $s$ and a target $t$, $\Pr[t \text{ is active}]$ is the probability that $s$ reaches $t$ in a random subgraph, the network reliability problem, which is #P-hard. Chen, Wang and Wang reduce it to the computation of $\sigma$ by comparing the spreads of related graphs.

**Why influence maximization is hard.** Given a set cover instance with sets $S_1, \dots, S_q$ over a ground set, make a vertex for each set and each element, an arc of probability 1 from each set to each of its elements, and ask whether $k$ seeds give a spread of at least $k$ plus the size of the ground set. With probability 1 the spread is deterministic, and the answer is yes exactly when $k$ sets cover the ground set.

**A first run by hand.** In the example, start from $S = \{0\}$. At step 1, vertex 0 tries 1 and 2; say only the try on 1 succeeds. At step 2, vertex 1 tries 3, and it succeeds. At step 3, vertex 3 tries 4 and fails. The run stops with $\{0, 1, 3\}$; the arc $2 \to 3$ was never tried, since 2 stayed inactive, and $5 \to 4$ was never tried, since 5 is not active.

## References
