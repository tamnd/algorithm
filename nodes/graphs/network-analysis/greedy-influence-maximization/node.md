---
tag: DDTH3Z
kind: algorithm
slug: greedy-influence-maximization
name: Greedy influence maximization
aliases:
- Kempe-Kleinberg-Tardos greedy
area: graphs/network-analysis
level: advanced
summary: Greedy seed selection with a (1-1/e) approximation guarantee.
solves: [influence-maximization]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, k: the number of seeds, r: the number of Monte Carlo runs per estimate of the spread}
  time: {worst: Θ(k n r (n + m))}
  space: {extra: Θ(n + m)}
properties: {deterministic: false, recursive: false}
history:
  year: 2003
  people: [David Kempe, Jon Kleinberg, Éva Tardos]
  note: Presented at KDD 2003; the guarantee rests on the 1978 analysis of the greedy method for submodular functions by Nemhauser, Wolsey and Fisher. Domingos and Richardson had posed the problem at KDD 2001.
prereqs: [influence-maximization, independent-cascade-model, linear-threshold-model, submodular-function, greedy-algorithm]
see_also: [nemhauser-wolsey-fisher-theorem, greedy-max-coverage, max-coverage, monte-carlo-algorithm, sir-epidemic-model, percolation]
sources:
  - paper: doi:10.1145/956750.956769
    title: David Kempe, Jon Kleinberg and Éva Tardos, Maximizing the spread of influence through a social network, Proceedings of the 9th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 137 to 146 (2003)
    locator: Section 2 (the greedy bound for monotone submodular functions, the submodularity of the spread under the independent cascade and linear threshold models through live-edge graphs, and the remark on approximate evaluation of the spread)
  - paper: doi:10.1007/BF01588971
    title: George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions, I, Mathematical Programming 14, 265 to 294 (1978)
    locator: the bound 1 - (1 - 1/k)^k for the greedy method on a monotone submodular function under a cardinality constraint
  - paper: doi:10.1145/1281192.1281239
    title: Jure Leskovec, Andreas Krause, Carlos Guestrin, Christos Faloutsos, Jeanne VanBriesen and Natalie Glance, Cost-effective outbreak detection in networks, Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 420 to 429 (2007)
    locator: the CELF lazy-forward evaluation, which skips gains that cannot be the largest, and its speed-up of about 700 times
  - paper: doi:10.1137/1.9781611973402.70
    title: Christian Borgs, Michael Brautbar, Jennifer Chayes and Brendan Lucier, Maximizing social influence in nearly optimal time, Proceedings of the 25th Annual ACM-SIAM Symposium on Discrete Algorithms, 946 to 957 (2014)
    locator: reverse reachable sets, and the (1 - 1/e - ε)-approximation in O((m + n) ε^(-3) log n) time
  - paper: doi:10.1145/2723372.2723734
    title: Youze Tang, Yanchen Shi and Xiaokui Xiao, Influence maximization in near-linear time, a martingale approach, Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data, 1539 to 1554 (2015)
    locator: the IMM algorithm, which picks the number of reverse reachable sets by martingale bounds
  - paper: doi:10.1145/1835804.1835934
    title: Wei Chen, Chi Wang and Yajun Wang, Scalable influence maximization for prevalent viral marketing in large-scale social networks, Proceedings of the 16th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 1029 to 1038 (2010)
    locator: "the proof that computing the spread of a seed set under the independent cascade model is #P-hard"
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 634 to 652 (1998)
    locator: the hardness of approximating maximum coverage within 1 - 1/e + ε unless P = NP
---

Greedy influence maximization picks $k$ seed vertices of a network one at a time, each time adding the vertex that raises the expected spread $\sigma(S)$ the most. Kempe, Kleinberg and Tardos proved in 2003 that under the [independent cascade model](/independent-cascade-model/) and the [linear threshold model](/linear-threshold-model/) the spread is a monotone [submodular function](/submodular-function/), so by the theorem of Nemhauser, Wolsey and Fisher the greedy set reaches at least $1 - 1/e \approx 0.632$ of the best possible spread. Computing $\sigma$ exactly is #P-hard, so in practice each value is estimated by $r$ Monte Carlo simulations, and the guarantee becomes $1 - 1/e - \varepsilon$. The method makes $O(kn)$ calls to the estimate, which is slow on large graphs; lazy evaluation and reverse reachable sets make it fast.

## In plain words

A company can give a free product to $k$ people and hopes they tell their friends, who tell theirs. Whom should it pick?

The greedy method picks the single person who would start the largest wave of word of mouth. Then it picks the person who adds the most to the wave of the first one, and so on, $k$ times. It never goes back on a choice.

This works well because influence has diminishing returns: a second person who shares many friends with the first adds little, and the greedy method sees this when it measures what each candidate adds. A classic theorem says that for such diminishing returns, picking greedily gets at least 63% of the best possible result.

## The problem

The input is a [directed graph](/directed-graph/) $G = (V, E)$ with $n$ vertices and $m$ arcs, a diffusion model on it, and an integer $k \ge 0$. An undirected graph has both arcs of each edge. In the [independent cascade model](/independent-cascade-model/), each arc $(u, v)$ has a probability $p_{uv}$: when $u$ becomes active, it activates $v$ with probability $p_{uv}$, once. In the [linear threshold model](/linear-threshold-model/), each arc has a weight $b_{uv} \ge 0$ with $\sum_u b_{uv} \le 1$ for each $v$, and each vertex activates when the weight from its active in-neighbours reaches a random threshold drawn uniformly from $[0, 1]$.

For a seed set $S \subseteq V$, the *spread* $\sigma(S)$ is the expected number of active vertices when the process stops, counting the seeds. The [influence maximization](/influence-maximization/) problem asks for a set $S$ with $|S| = k$ (or $|S| \le k$) that maximizes $\sigma(S)$. It is [NP-hard](/np-hard/) in both models, and computing $\sigma(S)$ for a given $S$ is #P-hard.

**The two properties the method needs.** A set function $f$ is *monotone* when $f(S) \le f(T)$ for $S \subseteq T$, and *submodular* when $f(S \cup \{v\}) - f(S) \ge f(T \cup \{v\}) - f(T)$ for $S \subseteq T$ and $v \notin T$: a vertex adds less to a larger set. Under both models, $\sigma$ is monotone and submodular, with $\sigma(\emptyset) = 0$. The proof writes $\sigma$ as an average of reachability counts in random *live-edge* graphs, each of which is a [coverage function](/max-coverage/).

## The algorithm

```pseudo id=main
GREEDY-IM(V, k, σ)
L1  S ← ∅
L2  for i ← 1 to min(k, |V|) do
L3      for each vertex v ∉ S, in increasing order do
L4          Δ(v) ← σ(S ∪ {v}) − σ(S)
L5      u ← the vertex v ∉ S with the largest Δ(v); ties go to the smallest v
L6      S ← S ∪ {u}
L7  return S
```

The oracle $\sigma$ is the only access to the graph. For an exact analysis it returns the true spread. In practice it is an estimate: run the cascade $r$ times from $S \cup \{v\}$, each run by a [breadth-first search](/breadth-first-search/) that flips the coin of an arc when its tail becomes active, and average the number of active vertices.

**Ties and the order of the seeds.** The tie rule of line L5 makes the method deterministic for an exact oracle. The seeds come out in the order they were picked, and the first $j$ of them are the greedy answer for $k = j$, so one run gives the answers for all budgets up to $k$.

**Disconnected graphs and isolated vertices.** Nothing changes. An isolated vertex has gain exactly 1, so the method takes it only when no vertex adds more than 1, which happens once every vertex with out-arcs has small gain. A graph with no arcs gives $\sigma(S) = |S|$, every gain is 1, and the method returns the $k$ smallest vertices.

**Monte Carlo noise.** With estimates, two calls for the same set can return different values, and the computed gains need not be submodular. Using fresh random runs for each call is what Kempe and co-authors analyse. Drawing a fixed sample of live-edge graphs once and evaluating every set on the same sample (common random numbers) makes the estimate an exact average over that sample, which is again monotone and submodular, so the greedy bound holds for the sample.

## Example

Take the vertices 0 to 5 and the arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$ and $5 \to 4$, each with $p = 1/2$ under the independent cascade model, and $k = 2$. The spread of one seed is computed from the probability that each vertex is reached through live arcs. From 0, vertices 1 and 2 are reached with probability $1/2$ each, vertex 3 with probability $1 - (1 - 1/4)^2 = 7/16$, and vertex 4 with probability $7/32$.

| round | candidate | gain $\Delta$ | pick |
|---|---|---|---|
| 1 | 0 | $1 + \frac12 + \frac12 + \frac{7}{16} + \frac{7}{32} = \frac{85}{32} \approx 2.66$ | 0 |
| 1 | 1, 2 | $\frac74$ | |
| 1 | 3, 5 | $\frac32$ | |
| 1 | 4 | $1$ | |
| 2 | 5 | $1 + \frac12 \cdot \frac{25}{32} = \frac{89}{64} \approx 1.39$ | 5 |
| 2 | 3 | $\frac{9}{16} + \frac{9}{32} = \frac{27}{32} \approx 0.84$ | |
| 2 | 1, 2 | $\frac{25}{32} \approx 0.78$ | |
| 2 | 4 | $1 - \frac{7}{32} = \frac{25}{32}$ | |

In round 2, the gain of 3 counts 3 only when 0 does not reach it (probability $9/16$), and 4 only when the arc $3 \to 4$ is live and 3 was not reached from 0. Vertex 5 has nothing in common with 0 except vertex 4, so its gain loses only a little. The answer is $S = \{0, 5\}$ with $\sigma(S) = 259/64 \approx 4.05$, which is optimal here; a check of all 15 pairs confirms it. Under the linear threshold model with all weights $1/2$ on the same graph, $\sigma(\{0\}) = 11/4$, and the greedy answer is again $\{0, 5\}$, with spread $17/4$.

## Correctness

Let $S_i$ be the set after $i$ rounds and $S^\ast$ an optimal set of size $k$. Since $\sigma$ is monotone and submodular,

$$\sigma(S^\ast) \le \sigma(S_i \cup S^\ast) \le \sigma(S_i) + \sum_{v \in S^\ast} \bigl(\sigma(S_i \cup \{v\}) - \sigma(S_i)\bigr) \le \sigma(S_i) + k\bigl(\sigma(S_{i+1}) - \sigma(S_i)\bigr),$$

because line L5 picks the largest gain. So the gap $\sigma(S^\ast) - \sigma(S_i)$ shrinks by a factor $1 - 1/k$ each round, and after $k$ rounds $\sigma(S_k) \ge (1 - (1 - 1/k)^k)\, \sigma(S^\ast) \ge (1 - 1/e)\, \sigma(S^\ast)$. The submodularity of $\sigma$ in both models comes from the live-edge view: flip all the coins of the cascade in advance, and $\sigma(S)$ becomes the expected number of vertices reachable from $S$ in a random subgraph, an average of coverage functions. The full proof, with the live-edge equivalence for the linear threshold model, is in [the proof page](proofs/correctness.md).

**With estimates.** If every call of $\sigma$ is within a factor $1 \pm \delta$ of the truth, the same argument gives $1 - 1/e - \varepsilon$ with $\varepsilon$ that tends to 0 with $\delta$ for fixed $k$. By the [Hoeffding inequality](/hoeffding-inequality/), $r = O(\delta^{-2} n^2 \log(nk/\eta))$ runs per call suffice for all $O(nk)$ calls to be accurate with probability $1 - \eta$, since each run returns a number in $[1, n]$ and $\sigma \ge 1$ for a non-empty set. This worst-case $r$ is far larger than the $r = 10000$ used in the experiments of Kempe and co-authors.

## Complexity

- **Oracle calls.** Line L4 runs at most $n$ times per round, so the method makes at most $kn + 1$ calls, keeping $\sigma(S)$ from the last round.
- **One call.** One Monte Carlo run touches each vertex and each arc at most once, $O(n + m)$, so a call with $r$ runs costs $O(r(n + m))$, and the whole method $\Theta(k n r (n + m))$ in the worst case, reached when the cascades cover most of the graph. Each run also resets its $n$ active flags, so even a graph with no arcs costs $\Theta(k n^2 r)$ with this simple form.
- **Space.** The graph, the active flags and the frontier of the search, $\Theta(n + m)$ words.
- **Exact spread.** No polynomial-time exact oracle is known: Chen, Wang and Wang proved computing $\sigma$ #P-hard under the independent cascade model, and the same holds for the linear threshold model.

## Properties

- **Approximation ratio $1 - (1 - 1/k)^k \ge 1 - 1/e$** with an exact oracle, for every model whose spread is monotone and submodular.
- **Tight in general.** With all probabilities 1, influence maximization contains [maximum coverage](/max-coverage/), for which Feige showed that no polynomial-time method beats $1 - 1/e$ unless P = NP; so the factor cannot be improved for polynomial-time methods.
- **Prefix property.** The first $j$ seeds are the greedy answer for budget $j$.
- **Randomized in practice.** With Monte Carlo estimates the output is random, and the guarantee holds with high probability.
- **Not for every model.** In threshold models with fixed thresholds or other non-submodular rules, the greedy method has no guarantee, and Kempe and co-authors show such problems can be hard to approximate within $n^{1 - \varepsilon}$.

## Variants and improvements

- **CELF (lazy greedy).** Leskovec and co-authors keep the gains of the last round in a priority queue. By submodularity a gain can only fall, so a stale gain is an upper bound; recompute only the top entry, and stop when the top is fresh. The output is the same, and they report a speed-up of about 700 times. CELF++ by Goyal, Lu and Lakshmanan saves more calls.
- **Reverse reachable sets.** Borgs, Brautbar, Chayes and Lucier pick a random vertex, collect the set of vertices that would reach it in a random live-edge graph, and repeat. A seed set's spread is $n$ times the fraction of these sets it hits, so greedy maximum coverage over the sets gives $1 - 1/e - \varepsilon$ in $O((m + n)\varepsilon^{-3} \log n)$ time. TIM and IMM by Tang, Xiao and Shi tune the number of sets and run in $O((k + \ell)(n + m) \log n / \varepsilon^2)$ expected time for success probability $1 - n^{-\ell}$.
- **Heuristics.** Degree, [PageRank](/pagerank/) and degree discount pick seeds without simulation. PMIA of Chen, Wang and Wang restricts influence to maximum influence arborescences around each vertex. They are fast but carry no guarantee.
- **Other constraints.** With costs per vertex (a knapsack constraint) or a [matroid](/matroid/) of allowed seed sets, variants of the greedy method keep constant-factor guarantees.

## When to use it

Use the plain greedy method on small graphs, as a reference, or when the spread function is cheap or given by a fixed sample of live-edge graphs. On graphs with more than a few thousand vertices, use CELF, or better IMM or another reverse-reachable-set method, which keep the same guarantee and run in near-linear time. Use the degree or PageRank heuristics only when speed matters more than any guarantee.

## Pitfalls

- **Treating the estimates as exact.** With few runs, the noise in the gains can be larger than the differences between candidates, and the chosen vertex is then random. Use enough runs, or common random numbers for all candidates of a round.
- **Using it for a non-submodular model.** For a threshold rule like "activate when two neighbours are active", the spread is not submodular and greedy can be arbitrarily bad.
- **Forgetting to count the seeds.** The spread counts the seeds themselves; some code counts only the newly activated vertices, which changes the gains by a constant 1 and changes nothing in the choice, but changes reported spreads.
- **Weights above 1 in the linear threshold model.** If the weights into a vertex sum to more than 1, the live-edge view breaks, and so does submodularity. Normalize them, for example to $1/d^{\mathrm{in}}(v)$.

## Implementations

## History

Domingos and Richardson asked in 2001 which customers a company should market to so as to exploit the word-of-mouth effects in a network, and modelled it with Markov random fields. In 2003 David Kempe, Jon Kleinberg and Éva Tardos stated the problem for the independent cascade and linear threshold models, both from earlier work in sociology and marketing, proved it NP-hard, and showed that the spread is submodular, so that the greedy method of Nemhauser, Wolsey and Fisher from 1978 gives $1 - 1/e$. Leskovec and co-authors made it practical with lazy evaluation in 2007. Borgs, Brautbar, Chayes and Lucier introduced reverse reachable sets in 2014, which led to the near-linear TIM and IMM algorithms of Tang, Xiao and Shi.

## References
