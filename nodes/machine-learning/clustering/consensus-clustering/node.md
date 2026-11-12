---
tag: B4JZZB
kind: algorithm
slug: consensus-clustering
name: Consensus clustering
aliases:
- ensemble clustering
- clustering aggregation
- median partition
area: machine-learning/clustering
level: advanced
summary: "Combines m clusterings into one that is near all of them: a median partition under the Mirkin distance, found by a majority pivot rule or by graph and hypergraph partitioning."
solves: [clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of items, m: the number of input clusterings}
  time: {worst: "O(m n^2 + m^2 n)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2002
  people: [Alexander Strehl, Joydeep Ghosh, Nir Ailon, Moses Charikar, Alantha Newman]
  note: The median partition is older (Régnier 1965) and is NP-hard (Křivánek and Morávek 1986; Wakabayashi 1986). Strehl and Ghosh named cluster ensembles in 2002 with CSPA, HGPA and MCLA. Ailon, Charikar and Newman gave the pivot algorithm with expected ratio 11/7 in 2005.
prereqs: [correlation-clustering, set-partitions, clustering-problem]
see_also: [pivot-algorithm, rand-index, adjusted-rand-index, normalized-mutual-information, agglomerative-clustering, hypergraph, graph-partitioning-problem, ensemble-learning]
sources:
  - paper: "Alexander Strehl and Joydeep Ghosh, Cluster ensembles: a knowledge reuse framework for combining multiple partitions, Journal of Machine Learning Research 3, 2002, pages 583 to 617"
    locator: "the ANMI objective (average normalized mutual information), and the three consensus functions CSPA, HGPA and MCLA, with their costs"
  - paper: doi:10.1145/1411509.1411513
    title: "Nir Ailon, Moses Charikar and Alantha Newman, Aggregating inconsistent information: ranking and clustering, Journal of the ACM 55(5), 2008, article 23"
    locator: "consensus clustering as weighted correlation clustering with probability constraints and the triangle inequality; the pivot algorithm with expected ratio 2 on such weights, and ratio 11/7 for the better of the pivot output and the best input (Table 1)"
  - paper: doi:10.1145/1217299.1217303
    title: "Aristides Gionis, Heikki Mannila and Panayiotis Tsaparas, Clustering aggregation, ACM Transactions on Knowledge Discovery from Data 1(1), 2007, article 4"
    locator: "the aggregation problem as correlation clustering, the BALLS, AGGLOMERATIVE, FURTHEST and LOCALSEARCH algorithms, and the ratio 2(1 - 1/m) of the best input clustering"
  - paper: "Mirko Křivánek and Jaroslav Morávek, NP-hard problems in hierarchical-tree clustering, Acta Informatica 23, 1986, pages 311 to 323"
    locator: NP-hardness of approximating a relation by an equivalence relation, which gives the NP-hardness of the median partition
  - paper: "Yoshiko Wakabayashi, Aggregation of binary relations: algorithmic and polyhedral investigations, PhD thesis, University of Augsburg, 1986"
    locator: NP-hardness of the median of equivalence relations (the median partition) under the symmetric difference distance
---

Consensus clustering takes $m$ clusterings $P_1, \ldots, P_m$ of the same $n$ items and returns one clustering that agrees with them as much as possible. In the usual exact form, the answer is a *median partition*: a partition $P$ that minimizes $\sum_i d(P, P_i)$, where $d$ is the Mirkin distance, the number of item pairs that one clustering puts together and the other puts apart. This problem is NP-hard (Křivánek and Morávek 1986; Wakabayashi 1986). It is exactly weighted [correlation clustering](/correlation-clustering/) with the co-association weights $w^+_{uv}$ = the fraction of inputs that put $u$ and $v$ together. The algorithm on this page runs the [pivot algorithm](/pivot-algorithm/) on the majority vote of the inputs, compares the result with the best input clustering, and keeps the better one. Its expected cost is at most $11/7$ times the optimum (Ailon, Charikar and Newman). Strehl and Ghosh's graph and hypergraph methods CSPA, HGPA and MCLA are the other standard approach.

## In plain words

Several people sorted the same pile of photos into groups, and each of them did it a bit differently. You want one final grouping.

For each pair of photos, count how many people put the two together. If more than half did, the pair "votes" to be together. A good final grouping breaks as few of these votes as possible, counted with weights.

To build one, pick a random photo, make a group of it and every remaining photo that most people put with it, and repeat on the rest. As a safety net, also check which one of the original groupings is closest to all the others. Keep whichever of the two is better. On average, the votes it breaks weigh at most 11/7 times those of the best possible answer.

## The problem

Write a clustering of $V = \{1, \ldots, n\}$ as a partition, or as a label per item. A clustering *joins* the pair $\{u, v\}$ if $u$ and $v$ are in the same cluster and *splits* it otherwise.

- **The distance.** $d(P, Q)$ is the number of unordered pairs that one of $P, Q$ joins and the other splits. It is the Hamming distance between the sets of joined pairs, so it is a metric on partitions. Mirkin's original metric counts ordered pairs and equals $2 d(P, Q)$; the [Rand index](/rand-index/) is $1 - d(P, Q)/\binom{n}{2}$. All three give the same median.
- **The median partition.** Given $P_1, \ldots, P_m$, find a partition $P$ of $V$ that minimizes $D(P) = \sum_{i=1}^m d(P, P_i)$. Let $\mathrm{OPT}$ be the least value. The answer need not be one of the inputs, and the number of clusters is not given.
- **The reduction.** Let $w^+_{uv} = |\{i : P_i \text{ joins } uv\}|/m$ and $w^-_{uv} = 1 - w^+_{uv}$. For every partition $P$,

$$D(P) = m \Bigl( \sum_{uv \text{ split by } P} w^+_{uv} + \sum_{uv \text{ joined by } P} w^-_{uv} \Bigr),$$

because, for a pair that $P$ splits, the inputs that disagree on it are exactly the $m w^+_{uv}$ inputs that join it, and the other way around. So the median partition is the optimum of weighted correlation clustering with these weights. The weights meet the *probability constraints* $w^+ + w^- = 1$, and $w^-$ meets the triangle inequality $w^-_{uv} \le w^-_{uw} + w^-_{wv}$, because each input's "split" indicator does and an average keeps it.

## The algorithm

```pseudo id=main
CONSENSUS(P_1, ..., P_m)
L1  for each pair u < v
L2      w+(u, v) ← |{ i : P_i joins u and v }| / m       ▷ w-(u, v) = 1 - w+(u, v)
L3  R ← V; Q ← the empty list of clusters
L4  while R ≠ ∅
L5      pick a pivot p uniformly at random from R
L6      C ← {p} ∪ { v ∈ R : w+(p, v) > 1/2 }
L7      append C to Q; R ← R \ C
L8  B ← the input P_j with the least D(P_j) = Σ_i d(P_j, P_i)
L9  if D(Q) ≤ D(B) return Q, else return B
```

Lines L3 to L7 are the pivot algorithm on the *majority graph*, whose edges are the pairs that more than half of the inputs join. Line L8 is "pick the best input" (BESTCLUSTERING in Gionis, Mannila and Tsaparas). Line L9 keeps the better of the two. With an even $m$, a pair with $w^+ = 1/2$ costs $1/2$ whether it is joined or split, so the strict test in line L6 loses nothing.

**The distance in $O(n)$.** Build the contingency table $n_{ab}$ = the number of items with label $a$ in $P$ and $b$ in $Q$, with a hash map. Then

$$d(P, Q) = \sum_a \binom{|P_a|}{2} + \sum_b \binom{|Q_b|}{2} - 2 \sum_{a, b} \binom{n_{ab}}{2},$$

since the pairs joined by both are counted in each of the first two sums.

## Example

Six items, three clusterings:

| clustering | clusters |
|---|---|
| $P_1$ | $\{0, 1, 2\}$, $\{3, 4, 5\}$ |
| $P_2$ | $\{0, 1\}$, $\{2, 3\}$, $\{4, 5\}$ |
| $P_3$ | $\{0, 1, 2, 3\}$, $\{4, 5\}$ |

The co-association weights that are not zero are $w^+ = 1$ on $01$ and $45$; $w^+ = 2/3$ on $02$, $12$, $23$; and $w^+ = 1/3$ on $03$, $13$, $34$, $35$. The majority graph has the edges $01, 02, 12, 23, 45$.

The pairwise distances are $d(P_1, P_2) = 5$, $d(P_1, P_3) = 5$ and $d(P_2, P_3) = 4$, so $D(P_1) = 10$, $D(P_2) = 9$, $D(P_3) = 9$. A brute force over all $B_6 = 203$ partitions finds the unique median $M = \{0, 1, 2\}, \{3\}, \{4, 5\}$ with $D(M) = 8$. It is not one of the inputs. Check by the reduction: $M$ splits $03, 13, 23, 34, 35$ (weights $1/3 + 1/3 + 2/3 + 1/3 + 1/3 = 2$) and joins $01, 02, 12, 45$ ($w^-$ weights $0 + 1/3 + 1/3 + 0 = 2/3$), and $3 \cdot (2 + 2/3) = 8$.

The pivot part:

| first pivot | output $Q$ | $D(Q)$ |
|---|---|---|
| 0 or 1 | $\{0, 1, 2\}$, then $\{3\}$ and $\{4, 5\}$ in some order | 8 |
| 2 | $\{0, 1, 2, 3\}$, $\{4, 5\}$ (this is $P_3$) | 9 |
| 3 | $\{2, 3\}$, $\{0, 1\}$, $\{4, 5\}$ (this is $P_2$) | 9 |
| 4 or 5 | $\{4, 5\}$, then as above with the next pivot from $\{0, 1, 2, 3\}$ | 8 or 9 |

So $\Pr[D(Q) = 8] = 2/6 + (2/6)(2/4) = 1/2$, and $\mathbb{E}[D(Q)] = 17/2$, that is $1.0625 \cdot \mathrm{OPT}$. Over all $6! = 720$ pivot orders, 360 give 8 and 360 give 9. Line L8 picks $B = P_2$ with $D = 9$, so line L9 changes nothing here, and the combined expected cost is also $17/2$.

## Correctness

The output is a partition: lines L3 to L7 remove a non-empty set that contains the pivot in each round, and $B$ is an input.

- **The reduction is exact.** The identity in "The problem" holds pair by pair, so the median partition and the weighted correlation clustering optimum are the same partitions with $\mathrm{OPT} = m \cdot \mathrm{OPT}_{cc}$. The tests check the identity with fractions on random ensembles, and check that the brute-force minimizers of both coincide.
- **The best input is within $2(1 - 1/m)$.** Let $P^*$ be a median and $P_j$ the input nearest to it, so $m \, d(P_j, P^*) \le \sum_i d(P_i, P^*) = \mathrm{OPT}$. By the triangle inequality for $d$, and because the term $i = j$ is 0,

$$D(P_j) = \sum_{i \ne j} d(P_j, P_i) \le \sum_{i \ne j} \bigl( d(P_j, P^*) + d(P^*, P_i) \bigr) = (m - 2)\, d(P_j, P^*) + \mathrm{OPT} \le \Bigl(2 - \frac{2}{m}\Bigr) \mathrm{OPT}.$$

  Line L8 returns an input at least as good as $P_j$.
- **The pivot part and the combination.** On weights with the probability constraints and the triangle inequality, Ailon, Charikar and Newman prove that the majority pivot has expected cost at most $2 \cdot \mathrm{OPT}$, and that the better of the pivot output and the best input has expected cost at most $\frac{11}{7} \mathrm{OPT}$. We cite these two ratios and do not reprove them. The tests check both exactly, with fractions, over all $n!$ pivot orders on random small ensembles against a brute-force median.

The full proofs of the first two points are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **Time.** Lines L1 and L2 take $O(m n^2)$. Each pivot round scans $R$, and each item leaves $R$ once, so lines L3 to L7 take $O(n^2)$. Line L8 computes $\binom{m}{2}$ distances in $O(n)$ each by the contingency table, so $O(m^2 n)$. Line L9 takes $O(m n)$. In total $O(m n^2 + m^2 n)$.
- **Space.** $O(n^2)$ for the weights. Without storing them, line L6 can count the votes for each pair on the fly in $O(m)$, with $O(n + m)$ extra space and the same time.

## Properties

- **The number of clusters is not an input.** It comes from the votes.
- **Unanimity.** If all inputs are equal, the majority graph is a union of cliques, the pivot part returns that clustering, and so does line L9.
- **Label free.** Only the joined and split pairs matter, so the cluster labels in the inputs do not have to match.
- **Randomized.** The ratio $11/7$ is in expectation; repeating lines L3 to L7 and keeping the best output helps.

## Variants and improvements

- **Strehl and Ghosh (2002).** They choose the consensus with the most *average normalized mutual information* (ANMI) with the inputs, and give three heuristics for a given $k$. *CSPA* (cluster-based similarity partitioning) builds the co-association matrix of lines L1 and L2 and partitions that similarity graph into $k$ parts with METIS, in $O(n^2 k m)$. *HGPA* (hypergraph partitioning) makes each input cluster a hyperedge of a [hypergraph](/hypergraph/) on the items and cuts it into $k$ balanced parts with the fewest cut hyperedges, using HMETIS. *MCLA* (meta-clustering) partitions the graph whose vertices are the input clusters, weighted by their Jaccard similarity, into $k$ meta-clusters, and puts each item into the meta-cluster that it is most associated with. Their "supra-consensus" runs all three and keeps the one with the highest ANMI.
- **Gionis, Mannila and Tsaparas (2007).** BALLS, a deterministic ball-growing rule on the $w^-$ distances with ratio 3; AGGLOMERATIVE and FURTHEST heuristics; and LOCALSEARCH, which moves single items while $D$ drops.
- **Evidence accumulation.** Fred and Jain run single-linkage or other [agglomerative clustering](/agglomerative-clustering/) on the co-association matrix and cut the tree.
- **Resampling consensus.** Monti and others (2003) cluster many subsamples with one method and read the stability of each pair from the co-association matrix, to choose the number of clusters.
- **Exact solutions.** For small $n$, an integer program over the transitive constraints of correlation clustering (Grötschel and Wakabayashi) finds the median.

## When to use it

Use it when you have several clusterings of the same items, from different algorithms, different seeds, different feature sets or different subsamples, and you want one robust answer, or when the inputs come from separate sources that can share only labels, not features. The pivot form needs no $k$ and no features. Use CSPA or MCLA when you want exactly $k$ clusters. For $n$ in the tens of thousands, the $O(n^2)$ weights become the bottleneck; compute the votes on the fly or sample the pairs.

## Pitfalls

- **Matching labels.** Cluster 1 in one input has nothing to do with cluster 1 in another. Voting on labels per item is wrong; vote on pairs, as in lines L1 and L2.
- **Two meanings of "consensus clustering".** It names both the median partition of given clusterings and the resampling method of Monti and others for choosing $k$. Say which one you mean.
- **Ties at one half.** With an even $m$, some pairs have $w^+ = 1/2$. Treat them consistently; they cost $1/2$ either way.
- **Weak inputs.** The median of many poor clusterings is still poor. The guarantee is relative to the median, not to the truth.
- **Different item sets.** If some inputs cluster only part of the items, the distance and the weights must be defined on the pairs that each input covers.

## Implementations

## History

Régnier (1965) posed the median partition, and Mirkin defined the distance in the 1970s. Křivánek and Morávek (1986) and Wakabayashi (1986) proved that the median partition is NP-hard. Grötschel and Wakabayashi (1989) solved it with cutting planes. In machine learning, Strehl and Ghosh (2002) introduced cluster ensembles with CSPA, HGPA and MCLA, Fred and Jain (2005) used evidence accumulation, and Gionis, Mannila and Tsaparas (2005, 2007) studied clustering aggregation as correlation clustering. Ailon, Charikar and Newman (2005, 2008) gave the pivot algorithm with expected ratio $11/7$ for this case.

## References
