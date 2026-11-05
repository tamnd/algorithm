---
tag: DGHXG8
kind: definition
slug: adamic-adar-index
name: Adamic-Adar index
aliases:
- Adamic-Adar measure
area: graphs/network-analysis
level: core
summary: Common-neighbour score weighting each shared neighbour by inverse log degree.
prereqs: [common-neighbors, degree]
see_also: [common-neighbors, link-prediction, node-similarity, triadic-closure, katz-centrality, simrank]
sources:
  - paper: doi:10.1016/S0378-8733(03)00009-1
    title: Lada A. Adamic and Eytan Adar, Friends and neighbors on the Web, Social Networks 25(3), 211 to 230 (2003)
    locator: the section on the similarity of home pages (the score as a sum over shared items of one over the log of their frequency)
  - paper: doi:10.1002/asi.20591
    title: David Liben-Nowell and Jon Kleinberg, The link-prediction problem for social networks, Journal of the American Society for Information Science and Technology 58(7), 1019 to 1031 (2007)
    locator: the section on methods based on node neighborhoods (Adamic/Adar as a weighted count of common neighbours), and the tables of results on the co-authorship networks
  - paper: doi:10.1140/epjb/e2009-00335-8
    title: Tao Zhou, Linyuan Lü and Yi-Cheng Zhang, Predicting missing links via local information, European Physical Journal B 71, 623 to 630 (2009)
    locator: the whole paper (the resource allocation index and the comparison with common neighbours and Adamic-Adar)
---

The Adamic-Adar index of two [vertices](/vertex/) $u$ and $v$ adds, over each common neighbour $w$, the weight $1/\log d(w)$, where $d(w)$ is the [degree](/degree/) of $w$. It refines the count of [common neighbors](/common-neighbors/): a shared friend who has few friends is strong evidence that $u$ and $v$ are close, and a shared hub that knows everyone is weak evidence. It is one of the standard scores for [link prediction](/link-prediction/), and in the study of Liben-Nowell and Kleinberg it was among the best simple predictors.

## Definition

Let $G = (V, E)$ be a simple undirected graph with [neighborhoods](/neighborhood/) $N(x)$ and degrees $d(x) = |N(x)|$. For two vertices $u \ne v$, the **Adamic-Adar index** is

$$\mathrm{AA}(u, v) = \sum_{w \in N(u) \cap N(v)} \frac{1}{\ln d(w)}.$$

Each common neighbour $w$ is adjacent to both $u$ and $v$, so $d(w) \ge 2$ and $\ln d(w) \ge \ln 2 > 0$. So each term is finite and positive, and

$$0 \le \mathrm{AA}(u, v) \le \frac{|N(u) \cap N(v)|}{\ln 2}.$$

The score is 0 exactly when $u$ and $v$ have no common neighbour.

**The base of the logarithm.** A change of base multiplies every term by the same constant, since $\log_b x = \ln x / \ln b$. So the base does not change the ranking of the pairs, only the values. Liben-Nowell and Kleinberg write $\log$; this page uses $\ln$.

**Why the inverse log.** Adamic and Adar defined the score for web pages that share items, such as links, words or mailing lists: an item that only two pages share says more than an item that thousands share. In a graph, the items are the neighbours, and the frequency of a neighbour $w$ is its degree. The log damps the weight slowly, so a hub still counts, but much less.

**The resource allocation index.** Zhou, Lü and Zhang use the weight $1/d(w)$ in place of $1/\ln d(w)$:

$$\mathrm{RA}(u, v) = \sum_{w \in N(u) \cap N(v)} \frac{1}{d(w)}.$$

It punishes hubs more strongly. It is the amount of a unit resource that $u$ sends to $v$ in one step when each common neighbour splits what it gets equally among its neighbours.

**Directed and weighted graphs.** The original definition is for an undirected graph without weights. For a directed graph one must choose which neighbours to intersect (out, in or both) and which degree to put in the logarithm. Weighted versions replace the count by a weighted sum. These are different scores, and a report must name the one it uses.

**Ties and disconnected graphs.** Pairs at distance more than 2, in particular in different components, all score 0 and tie. Among pairs with positive scores, ties are rarer than with the plain count, because the weights differ, but pairs whose common neighbours have the same degrees still tie. A ranked list needs a tie rule, for example the vertex numbers.

**Cost.** For one pair, the cost is that of the intersection, $O(\min(d(u), d(v)))$ expected time with hash sets, plus one logarithm per common neighbour, with the degrees stored. All pairs with a positive score come from listing, for each $w$, the pairs of its neighbours and adding $1/\ln d(w)$ to each pair. This takes time proportional to the number of paths of length 2, $\sum_w \binom{d(w)}{2}$.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. The degrees of the vertices 1, 2, 3 and 4 are all 3.

| pair, not adjacent | common neighbours | CN | AA |
|---|---|---|---|
| 0, 3 | 1, 2 | 2 | $2/\ln 3 \approx 1.8205$ |
| 1, 4 | 3 | 1 | $1/\ln 3 \approx 0.9102$ |
| 2, 4 | 3 | 1 | $1/\ln 3 \approx 0.9102$ |
| 3, 5 | 4 | 1 | $1/\ln 3 \approx 0.9102$ |
| 3, 6 | 4 | 1 | $1/\ln 3 \approx 0.9102$ |

All common neighbours here have degree 3, so AA is $1/\ln 3$ times the count and gives the same order.

**Where the two scores disagree.** Let $u$ and $v$ share two hubs $h_1$ and $h_2$, each of degree 20, and let $x$ and $y$ share one vertex $w$ of degree 2. The common-neighbour counts are 2 and 1, so the count ranks $\{u, v\}$ first. The Adamic-Adar scores are $2/\ln 20 \approx 0.6676$ and $1/\ln 2 \approx 1.4427$, so AA ranks $\{x, y\}$ first. The resource allocation scores are $2/20 = 0.1$ and $1/2 = 0.5$, with the same order as AA.

**Non-examples.**

- A sum of $1/\ln d(u) + 1/\ln d(v)$ over the two ends is not the Adamic-Adar index. The weights belong to the shared neighbours, not to $u$ and $v$.
- $\sum_w 1/d(w)$ is not the Adamic-Adar index. It is the resource allocation index, a different score that can rank pairs in a different order.
- The Adamic-Adar index is not a metric. It is a similarity, it is 0 for most pairs, and it does not satisfy a triangle inequality.

## Related definitions

- [Common neighbors](/common-neighbors/): the unweighted count that the index refines.
- [Link prediction](/link-prediction/) and [node similarity](/node-similarity/): the problems that use the index.
- [Katz centrality](/katz-centrality/): the related Katz score counts paths of all lengths with a decaying weight, not only paths of length 2.
- [SimRank](/simrank/): a recursive similarity of two vertices.
- [Triadic closure](/triadic-closure/): the tendency of shared neighbours to create new edges.

## References
