---
tag: 9J94S8
kind: problem
slug: influence-maximization
name: Influence maximization
aliases:
- viral marketing problem
area: graphs/network-analysis
level: advanced
summary: Choose k seed nodes that maximise expected spread under a diffusion model.
prereqs: [directed-graph, independent-cascade-model, linear-threshold-model, submodular-function]
see_also: [greedy-influence-maximization, max-coverage, nemhauser-wolsey-fisher-theorem, set-cover, vertex-cover, centrality, pagerank, sir-epidemic-model]
sources:
  - paper: doi:10.1145/502512.502525
    title: Pedro Domingos and Matt Richardson, Mining the network value of customers, Proceedings of the 7th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 57 to 66 (2001)
    locator: the whole paper (the network value of a customer and the choice of customers to market to, in a Markov random field model)
  - paper: doi:10.1145/956750.956769
    title: David Kempe, Jon Kleinberg and Éva Tardos, Maximizing the spread of influence through a social network, Proceedings of the 9th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 137 to 146 (2003)
    locator: Section 2 (the problem under the independent cascade and linear threshold models, its NP-hardness, the submodularity of the spread and the greedy (1 - 1/e)-approximation), and the hardness within n^(1-ε) for general threshold functions
  - paper: doi:10.1145/1835804.1835934
    title: Wei Chen, Chi Wang and Yajun Wang, Scalable influence maximization for prevalent viral marketing in large-scale social networks, Proceedings of the 16th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 1029 to 1038 (2010)
    locator: the #P-hardness of computing the spread under the independent cascade model, and the PMIA heuristic
  - paper: doi:10.1109/ICDM.2010.118
    title: Wei Chen, Yifei Yuan and Li Zhang, Scalable influence maximization in social networks under the linear threshold model, Proceedings of the 10th IEEE International Conference on Data Mining, 88 to 97 (2010)
    locator: the #P-hardness of computing the spread under the linear threshold model
  - paper: doi:10.1137/1.9781611973402.70
    title: Christian Borgs, Michael Brautbar, Jennifer Chayes and Brendan Lucier, Maximizing social influence in nearly optimal time, Proceedings of the 25th Annual ACM-SIAM Symposium on Discrete Algorithms, 946 to 957 (2014)
    locator: reverse reachable sets, the (1 - 1/e - ε)-approximation in O((m + n) ε^(-3) log n) time, and its optimality up to a logarithmic factor
  - paper: doi:10.1145/2588555.2593670
    title: Youze Tang, Xiaokui Xiao and Yanchen Shi, Influence maximization, near-optimal time complexity meets practical efficiency, Proceedings of the 2014 ACM SIGMOD International Conference on Management of Data, 75 to 86 (2014)
    locator: the TIM algorithm and its expected time O((k + ℓ)(n + m) log n / ε^2)
  - paper: doi:10.1145/2723372.2723734
    title: Youze Tang, Yanchen Shi and Xiaokui Xiao, Influence maximization in near-linear time, a martingale approach, Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data, 1539 to 1554 (2015)
    locator: the IMM algorithm, with the same guarantee and bound as TIM and fewer samples in practice
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 634 to 652 (1998)
    locator: the hardness of approximating maximum coverage within 1 - 1/e + ε unless P = NP
  - paper: doi:10.1145/1281192.1281239
    title: Jure Leskovec, Andreas Krause, Carlos Guestrin, Christos Faloutsos, Jeanne VanBriesen and Natalie Glance, Cost-effective outbreak detection in networks, Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 420 to 429 (2007)
    locator: the outbreak detection problem, its submodularity, and the CELF lazy evaluation
---

Influence maximization asks for $k$ seed vertices of a network that make the expected spread $\sigma(S)$ of a diffusion process as large as possible. The spread is defined by a random model of how activity passes along the arcs, most often the [independent cascade model](/independent-cascade-model/) or the [linear threshold model](/linear-threshold-model/). Kempe, Kleinberg and Tardos stated it in this form in 2003, after Domingos and Richardson had asked which customers a company should target to exploit word of mouth. The problem is NP-hard, and even evaluating $\sigma(S)$ is #P-hard, but $\sigma$ is monotone and submodular in both models, so the [greedy method](/greedy-influence-maximization/) reaches $1 - 1/e$ of the optimum, and no polynomial-time method can do better unless P = NP.

## In plain words

A company has free samples for a few people and wants the news to spread as far as possible through friends of friends. Each friend passes it on only with some chance. Whom should the samples go to?

The obvious answer, the people with the most friends, is often poor, because the most popular people tend to share friends, and two samples in the same circle reach the same people twice. A good choice spreads the samples over different parts of the network. Influence maximization makes this precise: it fixes a model of how news passes from person to person, and asks for the $k$ people whose combined expected reach is largest.

## Definition

**Input.** A [directed graph](/directed-graph/) $G = (V, E)$ with $n$ vertices and $m$ arcs, the parameters of a diffusion model on it, and an integer $k \ge 0$. In the independent cascade model these are a probability $p_{uv}$ on each arc; in the linear threshold model, a weight $b_{uv} \ge 0$ on each arc with $\sum_u b_{uv} \le 1$ for each $v$. An undirected network has both arcs of each edge.

**The objective.** For $S \subseteq V$, run the model from the seeds $S$ until it stops, and let $\sigma(S)$ be the expected number of active vertices at the end, counting the seeds. In both models, $\sigma(S) = \mathbb{E}[|R_L(S)|]$, where $L$ is a random set of live arcs and $R_L(S)$ the set of vertices reachable from $S$ along $L$: each arc is live independently with probability $p_{uv}$ in the cascade, and each vertex keeps one in-arc $(u, v)$ with probability $b_{uv}$ in the threshold model.

**Output.** A set $S \subseteq V$ with $|S| \le k$ that maximizes $\sigma(S)$. Since $\sigma$ is monotone, some optimal set has exactly $\min(k, n)$ vertices. Since $\sigma$ cannot be computed exactly in polynomial time unless P = #P, an algorithm is usually asked for a set whose spread is within a factor of the optimum with high probability, not for the spread itself.

**Monotone and submodular.** In both models, $\sigma(S) \le \sigma(T)$ for $S \subseteq T$, and $\sigma(S \cup \{v\}) - \sigma(S) \ge \sigma(T \cup \{v\}) - \sigma(T)$ for $S \subseteq T$, $v \notin T$. Each $|R_L(\cdot)|$ is a coverage function, the size of a union of one reachable set per seed, and $\sigma$ is an average of them.

## Variants

- **The model.** Besides the two standard models: the *triggering model*, which contains both; the *general threshold* and *general cascade* models, where submodularity holds only under extra conditions; and continuous-time models where each arc has a random delay.
- **Budgeted.** Each vertex has a cost and the seeds must fit a budget, a knapsack constraint instead of a cardinality one.
- **Time-critical.** Only the vertices activated within $T$ steps count. The spread stays submodular in both models.
- **Seed minimization.** Find the fewest seeds whose spread reaches a target $\eta$, the covering form of the problem.
- **Adaptive.** Seeds are chosen one at a time after observing the cascade of the previous seeds.
- **Competitive.** Several companies seed competing products, and each vertex adopts at most one.
- **Weighted and profit forms.** Each vertex has a value, and the goal is the expected value of the active set, possibly minus the cost of the seeds.

## Examples

**A small graph.** Take the vertices 0 to 5 and the arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$ and $5 \to 4$, each with probability or weight $1/2$.

| $k$ | best seeds | $\sigma$, independent cascade | $\sigma$, linear threshold |
|---|---|---|---|
| 1 | $\{0\}$ | $85/32 \approx 2.66$ | $11/4 = 2.75$ |
| 2 | $\{0, 5\}$ | $259/64 \approx 4.05$ | $17/4 = 4.25$ |
| 3 | $\{0, 1, 5\}$ or $\{0, 2, 5\}$ | $153/32 \approx 4.78$ | $41/8 \approx 5.13$ |
| 6 | all | 6 | 6 |

For $k = 2$, the best single seeds after 0 are 1 and 2, with spread $7/4$ each, but they reach mostly what 0 already reaches; vertex 5 reaches 4 from the side, and the pair $\{0, 5\}$ wins in both models. The [greedy method](/greedy-influence-maximization/) finds these sets here.

**Standard cases.**

- **All probabilities 1.** The spread is the number of vertices reachable from $S$, and the problem is [maximum coverage](/max-coverage/) with one set per vertex, the set of vertices it reaches.
- **All probabilities 0, or no arcs.** $\sigma(S) = |S|$, and every set of size $k$ is optimal.
- **A star with centre $c$ and $q$ leaves, arcs from the centre, probability $p$.** $\sigma(\{c\}) = 1 + qp$ and $\sigma(\{\text{leaf}\}) = 1$; for $k = 1$ the centre is best when $p > 0$.
- **Two disjoint communities.** With one large and one small dense community and $k = 2$, the best pair usually takes one seed in each, while the two highest-degree vertices both lie in the large one.

## Known algorithms

| algorithm | guarantee | time | notes |
|---|---|---|---|
| test every set of size $k$ | exact, with an exact oracle | $\binom{n}{k}$ evaluations of $\sigma$ | each exact evaluation is itself exponential in general |
| [greedy](/greedy-influence-maximization/), Kempe, Kleinberg and Tardos | $1 - 1/e - \varepsilon$ w.h.p. | $\Theta(knr(n + m))$ with $r$ simulations per estimate | the reference method |
| CELF, CELF++ | same as greedy | far fewer simulations in practice | lazy evaluation of the gains |
| reverse reachable sets, Borgs and co-authors | $1 - 1/e - \varepsilon$ w.h.p. | $O((m + n)\varepsilon^{-3} \log n)$ | greedy coverage of random reverse reachable sets |
| TIM, IMM, Tang, Xiao and Shi | $1 - 1/e - \varepsilon$ with probability $1 - n^{-\ell}$ | $O((k + \ell)(n + m) \log n / \varepsilon^2)$ expected | the usual choice for large graphs |
| highest degree, degree discount, [PageRank](/pagerank/) | none | $O(n \log n + m)$ or one PageRank run | fast heuristics |
| PMIA (cascade), LDAG (threshold) | none | near linear in practice | restrict influence to local trees or acyclic graphs |

## Bounds

- **NP-hard.** In both models, with all probabilities 1 in the cascade or a reduction from [vertex cover](/vertex-cover/) in the threshold model (Kempe, Kleinberg and Tardos).
- **No better than $1 - 1/e$.** Maximum coverage is a special case, and Feige proved that approximating it within $1 - 1/e + \varepsilon$ is NP-hard; so the greedy factor is the best possible for polynomial-time methods unless P = NP.
- **Evaluating the objective is #P-hard,** in the cascade model (Chen, Wang and Wang) and in the threshold model (Chen, Yuan and Zhang), so algorithms work with estimates, and their guarantees hold with high probability.
- **General threshold functions.** Without submodularity, Kempe, Kleinberg and Tardos show that the problem cannot be approximated within $n^{1 - \varepsilon}$ unless P = NP.
- **Time.** Borgs and co-authors show that their running time is optimal up to a logarithmic factor for an algorithm with a constant-factor guarantee.

## Reductions

- **From [maximum coverage](/max-coverage/) and [set cover](/set-cover/).** Make a vertex for each set and each element, an arc of probability 1 from each set to each of its elements; then $\sigma(S) = |S| + $ the number of elements covered, for seeds among the set vertices. This gives the NP-hardness in the cascade model and the $1 - 1/e$ barrier.
- **From [vertex cover](/vertex-cover/).** With both arcs of each edge and weights $1/d(v)$ in the threshold model, $\sigma(S) = n$ exactly when $S$ is a vertex cover.
- **To submodular maximization.** Any monotone submodular objective under a cardinality constraint is handled by the [Nemhauser-Wolsey-Fisher](/nemhauser-wolsey-fisher-theorem/) greedy bound, which is how the problem is solved.
- **To maximum coverage over samples.** A reverse reachable set is the set of vertices that reach a random vertex in a random live-edge graph. The spread of $S$ equals $n$ times the probability that $S$ meets such a set, so maximizing coverage of many sampled sets with [greedy max coverage](/greedy-max-coverage/) approximates the problem.

## Applications

- **Viral marketing.** Choosing whom to give free samples or discounts, the original motivation.
- **Information campaigns.** Choosing who should start a public health or safety message in a community network.
- **Outbreak detection.** The dual problem of placing sensors to detect cascades early has the same submodular structure, and Leskovec and co-authors solve both with CELF.
- **Rumour control.** Choosing vertices that spread a correction, or arcs and vertices to block, so that a harmful cascade reaches few people.
- **Ranking influential users.** The marginal gains of the greedy method give an influence-based [centrality](/centrality/), unlike degree, which ignores overlaps.

## References
