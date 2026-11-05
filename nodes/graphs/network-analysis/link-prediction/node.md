---
tag: DVNNVJ
kind: problem
slug: link-prediction
name: Link prediction
aliases:
- edge prediction
area: graphs/network-analysis
level: core
summary: Predict which currently absent edges are likely to appear.
prereqs: [graph, neighborhood, node-similarity]
see_also: [common-neighbors, adamic-adar-index, katz-centrality, simrank, personalized-pagerank, node-embedding, triadic-closure, homophily]
sources:
  - paper: doi:10.1002/asi.20591
    title: David Liben-Nowell and Jon Kleinberg, The link-prediction problem for social networks, Journal of the American Society for Information Science and Technology 58(7), 1019 to 1031 (2007)
    locator: the definition of the problem on co-authorship networks split by time, the list of scores, and the comparison with a random predictor
  - paper: doi:10.1016/j.physa.2010.11.027
    title: Linyuan Lü and Tao Zhou, Link prediction in complex networks, a survey, Physica A 390(6), 1150 to 1170 (2011)
    locator: the evaluation by AUC and precision, and the local, global and quasi-local similarity indices
  - paper: doi:10.1016/S0378-8733(03)00009-1
    title: Lada A. Adamic and Eytan Adar, Friends and neighbors on the Web, Social Networks 25(3), 211 to 230 (2003)
    locator: the similarity score that weights shared features by the inverse logarithm of their frequency
---

Link prediction is the problem of ranking the pairs of [vertices](/vertex/) that are not joined by an edge by how likely an edge between them is: either an edge that will form later, or one that exists but is missing from the data. Most methods give each pair a similarity score computed from the graph, such as the number of [common neighbours](/common-neighbors/), the [Adamic-Adar index](/adamic-adar-index/) or the [Katz](/katz-centrality/) count of walks, and output the pairs with the largest scores. The answer is judged on held-out edges, by measures such as the AUC and the precision of the top of the list.

## In plain words

A social network suggests "people you may know". It cannot read minds, so it guesses from the friendships it already sees. Two people with many friends in common have probably met, or will meet soon. A shared friend who has few friends is a stronger hint than a shared friend who knows everyone.

Link prediction turns such hints into a score for each pair of people who are not yet linked. The pairs with the highest scores are the guesses. To check a method, hide some of the links you know, run the method on the rest, and see whether the hidden links come out near the top of the list.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices and $m$ edges. In the time version of Liben-Nowell and Kleinberg, $G$ is the graph of the edges seen up to a time $t_0$, and the edges $E_{\mathrm{new}}$ that appear between $t_0$ and a later time $t_1$ are hidden. In the missing-link version, $E_{\mathrm{new}}$ is a random sample of the edges removed from the data. The basic problem is undirected and unweighted.

**Output.** A score $s(u, v) \in \mathbb{R}$ for each pair $\{u, v\} \notin E$ with $u \ne v$, or a list of the top $k$ pairs. The pairs are ranked by score.

**Quality.** Let $U$ be the set of non-adjacent pairs of $G$, so $E_{\mathrm{new}} \subseteq U$.

- The **AUC** is the probability that a uniform pair of $E_{\mathrm{new}}$ gets a higher score than a uniform pair of $U \setminus E_{\mathrm{new}}$, with a tie counted as $\tfrac12$. A random score has AUC $\tfrac12$.
- The **precision at $k$** is the fraction of the $k$ top-ranked pairs that are in $E_{\mathrm{new}}$. Liben-Nowell and Kleinberg report the *factor of improvement* over a random predictor, which is this precision divided by $|E_{\mathrm{new}}|/|U|$.

**Ties.** Local scores take few distinct values, so many pairs tie, and the order inside a tie changes precision at $k$. A method must say how it breaks ties, for example at random with a fixed seed.

**Disconnected graphs.** Scores built on short paths give 0 to every pair in different [components](/connected-components/), so they cannot rank those pairs; global scores such as preferential attachment can. Vertices that are new at $t_1$ have no edges in $G$ and cannot be scored by structure alone; Liben-Nowell and Kleinberg keep only vertices with enough edges in both periods.

**Directed and weighted graphs.** For a [directed graph](/directed-graph/), the pair is ordered and the scores use out-neighbours of $u$ and in-neighbours of $v$, or both. For a weighted graph, the scores can sum weights instead of counting neighbours, or the task can be to predict the weight.

## Variants

- **Temporal link prediction.** Predict the edges of a future snapshot, as above.
- **Missing links.** Recover edges absent from incomplete data, such as untested protein interactions.
- **Spurious links.** Rank the present edges by how likely each one is an error.
- **Link prediction with attributes.** Use vertex features as well as structure; [homophily](/homophily/) makes a shared attribute a good feature.
- **Signed and typed links.** Predict the sign of an edge, or which kind of relation it is, as in knowledge graphs.
- **Supervised prediction.** Train a classifier on features of pairs, such as several scores below and [node embeddings](/node-embedding/).

## Examples

**Local scores.** Take the graph with the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. Let $\Gamma(v)$ be the set of neighbours of $v$. The scores are: common neighbours $|\Gamma(u) \cap \Gamma(v)|$; Jaccard $|\Gamma(u) \cap \Gamma(v)| / |\Gamma(u) \cup \Gamma(v)|$; Adamic-Adar $\sum_{w \in \Gamma(u) \cap \Gamma(v)} 1/\ln |\Gamma(w)|$; resource allocation $\sum_{w} 1/|\Gamma(w)|$ over the same $w$; preferential attachment $|\Gamma(u)| \cdot |\Gamma(v)|$.

| pair | common | Jaccard | Adamic-Adar | resource allocation | pref. attachment |
|---|---|---|---|---|---|
| $\{0, 3\}$ | 2 | 2/3 | 1.820 | 2/3 | 6 |
| $\{1, 4\}$, $\{2, 4\}$ | 1 | 1/5 | 0.910 | 1/3 | 9 |
| $\{3, 5\}$, $\{3, 6\}$ | 1 | 1/4 | 0.910 | 1/3 | 6 |
| the other 7 pairs | 0 | 0 | 0 | 0 | 4 or 6 |

All neighbourhood scores put $\{0, 3\}$ first, the pair that closes two triangles. Preferential attachment prefers $\{1, 4\}$, the pair of two vertices of degree 3, even though they share only vertex 3.

**Evaluation.** Hide the edge $\{1, 3\}$ and score the 13 non-adjacent pairs of what is left. The hidden pair has 1 common neighbour (vertex 2). Of the 12 other pairs, 4 also have 1 common neighbour and 8 have none, so the AUC of common neighbours is $(8 + \tfrac12 \cdot 4)/12 = \tfrac56 \approx 0.833$. Preferential attachment gives the hidden pair $2 \cdot 2 = 4$, which beats no other pair and ties 7 of them, so its AUC is $\tfrac{7}{24} \approx 0.292$, worse than random on this graph.

## Known algorithms

| method | idea | cost for all candidate pairs |
|---|---|---|
| [Common neighbours](/common-neighbors/), Jaccard | shared neighbours | $O(\sum_w \deg(w)^2)$ by listing the pairs of neighbours of each $w$ |
| [Adamic-Adar index](/adamic-adar-index/), resource allocation | shared neighbours, weighted by their rarity | the same |
| Preferential attachment | product of degrees, after the [preferential attachment](/preferential-attachment/) model | $O(1)$ per pair |
| [Katz centrality](/katz-centrality/) index | all walks between the pair, damped by length | $O(n^3)$ by matrix inversion, less with truncated sums |
| Rooted PageRank, [personalized PageRank](/personalized-pagerank/) | the walk from $u$ that restarts at $u$ | one PageRank per source |
| [SimRank](/simrank/) | pairs whose neighbours are similar | $O(k n^2 \bar{d}^{\,2})$ for $k$ iterations in the plain method |
| [Node embeddings](/node-embedding/) such as [node2vec](/node2vec/) | the inner product of learned vectors | training cost, then $O(\text{dimension})$ per pair |
| [Stochastic block model](/stochastic-block-model/) | the edge probability of the fitted model | the cost of fitting |

## Bounds

- **No universal winner.** Liben-Nowell and Kleinberg found, on five co-authorship networks, that the good methods beat a random predictor by large factors, and that no score is best on all five; the Katz index and Adamic-Adar were among the strongest. Lü and Zhou report similar results on other data, with resource allocation strong among local scores.
- **Cost of the output.** There are $\binom{n}{2} - m$ candidate pairs, so a method that scores all of them needs $\Omega(n^2)$ time for a sparse graph. Local scores are 0 for all pairs at distance more than 2, so only the $O(\sum_w \deg(w)^2)$ pairs at distance 2 need work.
- **Statistical limits.** An edge that forms for reasons the graph does not show, such as one between two otherwise unrelated vertices, gets a low score from every structural method. So the best possible AUC on real data is below 1, and how far below is not known in general.

## Reductions

- **From vertex similarity.** Any [node similarity](/node-similarity/) measure defines a predictor: rank the pairs by similarity.
- **To binary classification.** With features of pairs and labels from held-out edges, the problem is supervised classification with very unbalanced classes, since $|E_{\mathrm{new}}|$ is tiny compared with $|U|$.
- **To matrix completion.** The adjacency matrix with the missing entries is a low-rank matrix to complete, which is what embedding methods do.

## Applications

- Friend and follower suggestions in social networks.
- Recommendation of products, as links in a graph of users and items.
- Biology: choosing which protein interactions to test next.
- Citation and co-authorship: suggesting related work and collaborators.
- Knowledge graphs: completing missing facts.

## References
