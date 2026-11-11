---
tag: 5T9748
kind: theorem
slug: kmw-lower-bound
name: Kuhn-Moscibroda-Wattenhofer lower bound
aliases:
- KMW lower bound
- local approximation lower bound
area: distributed/distributed-graph-algorithms
level: research
summary: No k-round LOCAL algorithm approximates vertex cover within Delta^(1/(k+1))/k. So polylog ratios, MIS and maximal matching need Omega(log Delta/log log Delta) and Omega(sqrt(log n/log log n)) rounds.
prereqs: [local-model, vertex-cover, girth, lp-relaxation]
see_also: [distributed-minimum-vertex-cover, distributed-dominating-set, distributed-mis, distributed-maximal-matching, linial-coloring-lower-bound, sinkless-orientation, locally-checkable-labeling, line-graph]
sources:
  - paper: doi:10.1145/2742012
    title: Fabian Kuhn, Thomas Moscibroda and Roger Wattenhofer, Local computation, lower and upper bounds, Journal of the ACM 63(2), 2016
    locator: Article 17, pp. 1 to 44; Section 3 (the cluster tree, the high-girth graph, equal views, and the vertex cover bound, Theorems 13 and 14 in arXiv 1011.5470v2), Section 4 (reductions to dominating set, matching, maximal matching and MIS, Theorems 15 to 23), Section 5 (the upper bounds)
  - paper: doi:10.1145/1011767.1011811
    title: Fabian Kuhn, Thomas Moscibroda and Roger Wattenhofer, What cannot be computed locally!, PODC 2004
    locator: pp. 300 to 309 (the first version of the lower bound)
  - paper: doi:10.1145/1109557.1109666
    title: Fabian Kuhn, Thomas Moscibroda and Roger Wattenhofer, The price of being near-sighted, SODA 2006
    locator: pp. 980 to 989 (the improved bounds and the matching upper bounds for covering and packing LPs)
  - paper: doi:10.1137/1.9781611976496.21
    title: Corinna Coupette and Christoph Lenzen, A breezing proof of the KMW bound, SOSA 2021
    locator: pp. 184 to 195 (a shorter proof of the same bound)
  - paper: doi:10.1145/3060294
    title: Reuven Bar-Yehuda, Keren Censor-Hillel and Gregory Schwartzman, A distributed (2 + epsilon)-approximation for vertex cover in O(log Delta / epsilon log log Delta) rounds, Journal of the ACM 64(3), 2017
    locator: the round bound, which matches the Delta part of the lower bound for constant epsilon
  - paper: doi:10.1145/3461458
    title: Alkida Balliu, Sebastian Brandt, Juho Hirvonen, Dennis Olivetti, Mikaël Rabie and Jukka Suomela, Lower bounds for maximal matchings and maximal independent sets, Journal of the ACM 68(5), 2021
    locator: the bounds Omega(min(Delta, log n / log log n)) deterministic and Omega(min(Delta, log log n / log log log n)) randomized, which are stronger when Delta is small
---

The Kuhn-Moscibroda-Wattenhofer (KMW) lower bound says that in the [LOCAL model](/local-model/), an algorithm that runs for $k$ rounds cannot approximate [minimum vertex cover](/distributed-minimum-vertex-cover/) within a factor better than about $\Delta^{1/(k+1)} / k$ or $n^{1/(4k^2)} / k$, even with randomness and unbounded messages. So a constant or polylogarithmic approximation needs $\Omega(\log \Delta / \log \log \Delta)$ and $\Omega(\sqrt{\log n / \log \log n})$ rounds. By reductions, the same bounds hold for dominating set, fractional matching, covering and packing LPs, and for [MIS](/distributed-mis/) and [maximal matching](/distributed-maximal-matching/).

Notation on this page: $G$ has $n$ nodes and maximum degree $\Delta$. A $k$-round algorithm is one in which each node decides after $k$ rounds; in LOCAL its output is then a function of its view, the labelled ball of radius $k$ around it, and of its random bits. The approximation ratio of a randomized algorithm is measured in expectation.

## Statement

**Theorem (KMW, JACM 2016, Theorem 13 in the arXiv version).** For every integer $k > 0$ there are graphs $G$ such that every distributed algorithm for minimum vertex cover that runs for $k$ rounds in the LOCAL model, deterministic or randomized, has approximation ratio at least
$$\Omega\left(\frac{n^{(1 - o(1)) / (4k^2)}}{k}\right) \quad \text{and} \quad \Omega\left(\frac{\Delta^{1/(k+1)}}{k}\right).$$

**Corollary (Theorem 14).** To get a constant or polylogarithmic approximation of minimum vertex cover, even in LOCAL, every distributed algorithm needs $\Omega\left(\sqrt{\log n / \log \log n}\right)$ and $\Omega(\log \Delta / \log \log \Delta)$ rounds.

For a graph family where both parameters can be chosen, the corollary is often written as one bound, $\Omega\left(\min\left(\frac{\log \Delta}{\log \log \Delta}, \sqrt{\frac{\log n}{\log \log n}}\right)\right)$. The bounds hold even when the identifiers are $\{1, \dots, n\}$ and every node knows the whole topology, so they are not about missing information on $n$ or $\Delta$; they come from the fact that nodes cannot tell some neighbours apart.

**From the ratio to rounds.** If the ratio is at most $(\log \Delta)^c$, then $\Delta^{1/(k+1)} / k \le O((\log \Delta)^c)$. Taking logarithms gives $\frac{\log \Delta}{k + 1} \le c \log \log \Delta + \log k + O(1)$, so $k = \Omega(\log \Delta / \log \log \Delta)$. In the same way, $\frac{\log n}{4k^2} \le O(\log \log n)$ gives $k = \Omega(\sqrt{\log n / \log \log n})$.

## In plain words

Picture a large crowd of people, and a much smaller group of leaders. Each leader is linked to many people, and each person to one leader. To cover every link, it is enough to pick all the leaders, which is cheap because there are few of them.

Now hide the difference. Build the rest of the network so carefully that, looking a few steps around itself, a person sees exactly what a leader sees. Also make sure there are no short loops, so every local view is a tree.

A person and a leader who are linked must not both stay out of the cover. Since they see the same thing, they behave the same way, so each joins with probability at least one half. Then about half of the large crowd joins, while the best answer uses only the leaders. Looking further only helps if the network is small.

## Proof

This is a sketch of the proof in the paper; it gives the structure and the counting but not the full verification that the views are equal.

**Step 1: the cluster tree.** Fix $k$ and a number $\delta > 2(k + 1)$, and put $\delta_i = \delta^i$ for $i = 0, \dots, k + 1$. The graph $G_k$ is built from disjoint sets of nodes called clusters. Each cluster is an independent set, and two clusters are either not linked or linked by a biregular bipartite graph, in which each node of one cluster has $\delta_i$ neighbours in the other and each node of the other has $\delta_{i+1}$ neighbours in the first, for some $i$. The pattern of clusters and links is a tree, the cluster tree $CT_k$, defined by induction on $k$. Its root cluster $C_0$ has $n_0$ nodes and is linked to $C_1$ with degrees $(\delta_0, \delta_1) = (1, \delta)$, so $|C_1| = n_0 / \delta$. Moving one level down the tree divides cluster sizes by $\delta$, and each cluster has at most $k + 1$ child clusters, so (Lemma 12) $n \le n_0 \left(1 + \frac{k + 1}{\delta - (k + 1)}\right)$, and the maximum degree is $\Delta = \delta^{k+1}$.

**Step 2: high girth.** Some graph with the cluster tree structure exists. Taking a suitable lift (a covering graph) of it keeps the structure and raises the [girth](/girth/) to at least $2k + 1$, at the cost of more nodes, so that every view of radius $k$ is a tree (Lemma 6). With these sizes, $n = O(\delta^{4k^2 (1 + o(1))})$.

**Step 3: equal views (Theorem 10).** For adjacent nodes $v_0 \in C_0$ and $v_1 \in C_1$, the views of radius $k$ are isomorphic as rooted trees. The tree is designed for this: the degrees $\delta_i$ on the links make the number of neighbours of each kind agree at every depth up to $k$. The paper proves it with derivation rules for view trees. The fact that $k + 1$ degree classes are needed is what makes the graph grow so fast with $k$.

**Step 4: the counting (Lemma 11).** Assign the identifiers uniformly at random. A deterministic $k$-round algorithm then puts $v_0$ into the cover with some probability $p_0$ and $v_1$ with probability $p_1$. The views and the distributions of labels on them are the same, so $p_0 = p_1$. The edge $\{v_0, v_1\}$ must be covered, so $p_0 + p_1 \ge 1$, and $p_0 \ge \frac{1}{2}$. By linearity of expectation, at least $n_0 / 2$ nodes of $C_0$ are in the cover in expectation, so some labelling gives at least that many. For randomized algorithms, Yao's principle gives the same bound in expectation.

**Step 5: the ratio.** Every cluster is independent, so $V \setminus C_0$ is a vertex cover, and $\mathrm{OPT} \le n - n_0 \le n_0 \frac{k + 1}{\delta - (k + 1)}$. The ratio is therefore at least $\frac{n_0 / 2}{n_0 (k + 1) / (\delta - k - 1)} = \frac{\delta - k - 1}{2(k + 1)} = \Omega(\delta / k)$. With $\delta = \Delta^{1/(k+1)}$ and $\delta = n^{(1 - o(1)) / (4k^2)}$ this is the theorem. $\square$ (sketch)

The proof also works for the fractional vertex cover, the [LP relaxation](/lp-relaxation/), since the argument only uses the expected value of each node and the edge constraint.

## Consequences

- **Minimum dominating set (Theorem 15).** On the [line graph](/line-graph/) of $G_k$, a dominating set is a set of edges that touches every edge, and its endpoints form a vertex cover at most twice as large; in the other direction a vertex cover gives an edge dominating set of the same size. A $k$-round algorithm on the line graph runs in $k$ rounds on $G_k$. So [minimum dominating set](/distributed-dominating-set/) and its LP relaxation have the same bounds.
- **Fractional maximum matching (Theorem 20).** No simple reduction is known, but a modified cluster graph gives the same bounds. Since vertex cover and matching are the covering and packing LPs with constant integrality gap, general covering and packing LPs inherit the bounds.
- **Maximal matching (Theorem 22).** The endpoints of a maximal matching form a 2-approximate vertex cover. So a deterministic maximal matching algorithm needs $\Omega(\sqrt{\log n / \log \log n})$ and $\Omega(\log \Delta / \log \log \Delta)$ rounds. For a randomized algorithm with expected time $T$, the paper builds a vertex cover algorithm with fixed time $2T + 1$ and expected ratio 11, so the same bounds hold for the expected time.
- **MIS (Theorem 23).** An MIS of the line graph is a maximal matching of $G$, so MIS needs the same expected time on line graphs of the lower bound graphs.
- **Connected dominating set.** A simpler girth argument gives a ratio of at least $n^{c/k}$ for a constant $c > 0$, so a polylogarithmic ratio needs $\Omega(\log n / \log \log n)$ rounds.

## Tightness

- **In $\Delta$, for vertex cover.** KMW give a deterministic algorithm with ratio $O(\Delta^{1/k})$ in $O(k)$ rounds, which gives a polylogarithmic ratio in $O(\log \Delta / \log \log \Delta)$ rounds and a constant ratio in $O(\log \Delta)$ rounds. Bar-Yehuda, Censor-Hillel and Schwartzman (2017) get ratio $2 + \varepsilon$ in $O(\log \Delta / \log \log \Delta)$ rounds for constant $\varepsilon$, which matches the $\Delta$ part of the bound.
- **In $n$, a gap remains.** KMW solve covering and packing LPs within $1 + \varepsilon$ in $O(\log n / \varepsilon)$ rounds, and dominating set within $O(\log \Delta)$ after rounding; the lower bound in $n$ is only $\sqrt{\log n / \log \log n}$.
- **MIS and maximal matching.** Ghaffari's MIS algorithm takes $O(\log \Delta) + 2^{O(\sqrt{\log \log n})}$ rounds, close to the $\Delta$ part. For small $\Delta$, the bound $\log \Delta / \log \log \Delta$ is weak, and Balliu et al. (2019) proved $\Omega(\min(\Delta, \log n / \log \log n))$ deterministic and $\Omega(\min(\Delta, \log \log n / \log \log \log n))$ randomized bounds by [round elimination](/round-elimination/), with a quite different method.
- **What the bound does not cover.** It counts rounds only, not computation, and it holds for algorithms that know $n$, $\Delta$ and the topology. It does not apply to models with global communication, such as the [congested clique](/congested-clique-model/).

## History

Kuhn, Moscibroda and Wattenhofer proved the first version at PODC 2004 ("What cannot be computed locally!"), improved it and gave matching upper bounds for LPs at SODA 2006 ("The price of being near-sighted"), and published the full version with the reductions in the Journal of the ACM in 2016. Before it, the best lower bound for MIS and maximal matching on general graphs was Linial's $\Omega(\log^* n)$ from rings; see [Linial's colouring lower bound](/linial-coloring-lower-bound/). Coupette and Lenzen (2021) gave a shorter proof. Round elimination, which gave the later bounds for small $\Delta$, began with [sinkless orientation](/sinkless-orientation/).

## References
