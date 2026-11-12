---
tag: 5P8JQX
kind: problem
slug: correlation-clustering
name: Correlation clustering
aliases:
- correlation clustering problem
- clustering with qualitative information
area: machine-learning/clustering
level: advanced
summary: "Given a + or - label on each pair of items, partition the items to minimize disagreements (+ pairs split, - pairs joined). The number of clusters is free. NP-hard."
prereqs: [clustering-problem, set-partitions, np-hard]
see_also: [pivot-algorithm, consensus-clustering, multicut-problem, lp-relaxation, apx, bell-numbers, modularity, subspace-clustering-problem]
sources:
  - paper: doi:10.1023/B:MACH.0000033116.57574.95
    title: "Nikhil Bansal, Avrim Blum and Shuchi Chawla, Correlation clustering, Machine Learning 56(1-3), 2004, pages 89 to 113"
    locator: "the definition of MinDisagree and MaxAgree on complete graphs, the NP-completeness proof, the constant factor approximation for MinDisagree and the PTAS for MaxAgree"
  - paper: doi:10.1016/j.jcss.2004.10.012
    title: "Moses Charikar, Venkatesan Guruswami and Anthony Wirth, Clustering with qualitative information, Journal of Computer and System Sciences 71(3), 2005, pages 360 to 383"
    locator: "the 4-approximation by LP rounding for complete graphs, the APX-hardness of MinDisagree on complete graphs, the O(log n) approximation for general weighted graphs, and the SDP algorithm for MaxAgree on general graphs"
  - paper: doi:10.1145/1411509.1411513
    title: "Nir Ailon, Moses Charikar and Alantha Newman, Aggregating inconsistent information: ranking and clustering, Journal of the ACM 55(5), 2008, article 23"
    locator: "KwikCluster (expected ratio 3), the LP-based pivot (expected ratio 2.5), and the weighted cases with probability constraints and triangle inequalities (Table 1)"
  - paper: doi:10.1145/2746539.2746604
    title: "Shuchi Chawla, Konstantin Makarychev, Tselil Schramm and Grigory Yaroslavtsev, Near optimal LP rounding algorithm for correlation clustering on complete and complete k-partite graphs, STOC 2015, pages 219 to 228"
    locator: the 2.06-approximation by LP rounding for complete graphs
  - paper: "Erik D. Demaine, Dotan Emanuel, Amos Fiat and Nicole Immorlica, Correlation clustering in general weighted graphs, Theoretical Computer Science 361(2-3), 2006, pages 172 to 187"
    locator: the equivalence with minimum multicut and the O(log n) approximation for general weighted graphs
  - paper: "Martin Grötschel and Yoshiko Wakabayashi, A cutting plane algorithm for a clustering problem, Mathematical Programming 45, 1989, pages 59 to 96"
    locator: the clique partitioning problem, its integer program with triangle inequalities, and exact solution by cutting planes
---

Correlation clustering asks for a partition of $n$ items when the only data is a judgment on each pair: $+$ ("these two are similar") or $-$ ("these two are different"). A partition disagrees with a $+$ pair that it splits and with a $-$ pair that it puts in one cluster. The goal is to minimize the number of disagreements (MinDisagree) or, equivalently for exact solutions, to maximize the number of agreements (MaxAgree). The number of clusters is not given; it comes out of the data. Bansal, Blum and Chawla (2004) defined the problem and proved it NP-hard. On complete graphs MinDisagree is APX-hard (Charikar, Guruswami and Wirth 2005), and the simple [pivot algorithm](/pivot-algorithm/) has expected ratio 3.

## In plain words

You have a pile of documents and a helper who looked at each pair and said "same author" or "different authors". The helper makes mistakes, so the answers do not fit together: A and B are the same, B and C are the same, but A and C are different. No grouping can agree with all three answers.

Correlation clustering asks for the grouping that disagrees with the fewest answers. You do not say how many groups you want. If most answers say "same", you get a few big groups. If most say "different", you get many small ones.

The problem is hard to solve exactly, because the number of possible groupings grows faster than exponentially. Fast methods exist that are at most a few times worse than the best grouping.

## Definition

**Input.** A complete graph on the vertex set $V = \{1, \ldots, n\}$, each edge labeled $+$ or $-$. Write $E^+$ and $E^-$ for the two sets of edges.

**Feasible solutions.** All partitions $\mathcal{C}$ of $V$ into non-empty clusters, with any number of clusters from 1 to $n$. There are $B_n$ of them, the [Bell number](/bell-numbers/).

**Objective.** For a partition $\mathcal{C}$ write $u \sim v$ if $u$ and $v$ are in the same cluster.

$$\mathrm{disagree}(\mathcal{C}) = \bigl|\{uv \in E^+ : u \not\sim v\}\bigr| + \bigl|\{uv \in E^- : u \sim v\}\bigr|, \qquad \mathrm{agree}(\mathcal{C}) = \binom{n}{2} - \mathrm{disagree}(\mathcal{C}).$$

MinDisagree asks for a partition with the least disagreements, and MaxAgree for one with the most agreements. They have the same optimal partitions, but not the same approximation behavior: a partition with half of the pairs in agreement is a $1/2$-approximation for MaxAgree, but it can be very bad for MinDisagree.

**The weighted form.** Each pair has weights $w^+_{uv}, w^-_{uv} \ge 0$, and a partition pays $w^+_{uv}$ when it splits $u, v$ and $w^-_{uv}$ when it joins them. The unweighted problem has $(w^+, w^-) \in \{(1, 0), (0, 1)\}$.

**Bad triangles.** A triple $\{u, v, w\}$ with two $+$ edges and one $-$ edge is a *bad triangle*. Each partition disagrees with at least one edge of each bad triangle: if it joins the two $+$ edges, it joins the $-$ edge too. Conversely, if there is no bad triangle, the relation "$+$ or equal" is transitive, so $E^+$ is a disjoint union of cliques, and that union has no disagreement. So the optimum is 0 if and only if there is no bad triangle.

## Variants

- **General graphs.** Some pairs have no label (weight 0 on both sides). MinDisagree on general weighted graphs is equivalent to minimum [multicut](/multicut-problem/) under approximation-preserving reductions (Demaine, Emanuel, Fiat and Immorlica 2006; Charikar, Guruswami and Wirth 2005).
- **Probability constraints.** $w^+_{uv} + w^-_{uv} = 1$ for each pair, for example when $w^+$ is the fraction of votes for "same". With the triangle inequality $w^-_{uw} \le w^-_{uv} + w^-_{vw}$ as well, better ratios are possible (Ailon, Charikar and Newman 2008).
- **Consensus clustering.** Given $m$ clusterings, let $w^+_{uv}$ be the fraction of them that join $u$ and $v$. The weighted problem is then the median partition problem; see [consensus clustering](/consensus-clustering/).
- **Clique partitioning.** With $c_{uv} = w^+_{uv} - w^-_{uv}$, minimizing disagreements is the same as maximizing $\sum_{u \sim v} c_{uv}$, the clique partitioning problem of Grötschel and Wakabayashi (1989).
- **A fixed number of clusters.** Some versions add the constraint "at most $k$ clusters".

**Not the same name.** In data mining, "correlation clustering" also names the search for clusters in arbitrarily oriented subspaces (Kriegel, Kröger and Zimek 2009); that is a form of the [subspace clustering problem](/subspace-clustering-problem/), not this problem.

## Examples

**A small instance.** Take $n = 5$ with $E^+ = \{01, 02, 12, 23, 34\}$ and the other five pairs in $E^-$. The bad triangles are $\{0, 2, 3\}$, $\{1, 2, 3\}$ and $\{2, 3, 4\}$, and all three contain the $+$ edge $23$. Splitting that edge fixes all three: the partition $\{0, 1, 2\}, \{3, 4\}$ has exactly one disagreement. A brute force over all $B_5 = 52$ partitions shows that it is the unique optimum. One cluster has 5 disagreements (the five $-$ pairs), and five singletons also have 5 (the five $+$ pairs).

**A star.** Take $E^+ = \{01, 02, 03\}$ on four vertices. Each of the three $-$ pairs between leaves forms a bad triangle with the center. The optimum is 2. The center with one leaf splits two $+$ pairs. The center with two leaves joins one $-$ pair and splits one $+$ pair. The center with all three leaves joins three $-$ pairs, and the center alone splits three $+$ pairs. So six partitions attain 2. Any two bad triangles here share an edge, so a set of edge-disjoint bad triangles gives only the lower bound 1. Giving each bad triangle the weight $1/2$ is a fractional packing (each edge is in at most two of them) and gives the better bound $3/2$.

**Inconsistent judgments.** $+$ on $ab$ and $bc$, $-$ on $ac$: the single bad triangle forces one disagreement, and three partitions attain it ($\{a, b, c\}$, $\{a, b\}\{c\}$ and $\{a\}\{b, c\}$).

## Known algorithms

- **Exact.** Brute force over the $B_n$ partitions. An integer program with a variable $x_{uv} \in \{0, 1\}$ for "split" and the triangle inequalities $x_{uw} \le x_{uv} + x_{vw}$ is exact; Grötschel and Wakabayashi (1989) solved it by cutting planes for instances with about 100 items.
- **Pivot (KwikCluster).** Pick a random vertex, make a cluster of it and its $+$ neighbors, remove them, and repeat. Expected ratio 3 for MinDisagree on complete graphs (Ailon, Charikar and Newman 2008); see the [pivot algorithm](/pivot-algorithm/).
- **LP rounding.** Solve the [LP relaxation](/lp-relaxation/) of the integer program. Charikar, Guruswami and Wirth rounded it with ratio 4. Ailon, Charikar and Newman used the LP values as probabilities in the pivot step for expected ratio 2.5. Chawla, Makarychev, Schramm and Yaroslavtsev (2015) gave a rounding with ratio 2.06.
- **General weighted graphs.** Region growing on the LP, as for multicut, gives $O(\log n)$ (Charikar, Guruswami and Wirth; Demaine et al.).
- **MaxAgree.** On complete graphs there is a PTAS (Bansal, Blum and Chawla). On general weighted graphs, semidefinite programming gives a constant ratio of about 0.766 (Charikar, Guruswami and Wirth).
- **Heuristics.** Local search that moves one vertex at a time, and greedy merging, are common in practice and have no guarantee.

## Bounds

- **Hardness.** MinDisagree and MaxAgree on complete graphs are NP-hard (Bansal, Blum and Chawla 2004). MinDisagree on complete graphs is [APX-hard](/apx/) (Charikar, Guruswami and Wirth 2005), so there is no PTAS unless P = NP. On general weighted graphs, MinDisagree is as hard to approximate as minimum multicut.
- **Trivial upper bound.** One cluster costs $|E^-|$ and all singletons cost $|E^+|$, so $\mathrm{OPT} \le \min(|E^+|, |E^-|)$.
- **Lower bound.** For any weights $\beta_T \ge 0$ on the bad triangles with $\sum_{T \ni e} \beta_T \le 1$ for each pair $e$, $\mathrm{OPT} \ge \sum_T \beta_T$, because each partition pays at least one edge of each bad triangle. This bound drives the analysis of the pivot algorithm.
- **LP integrality gap.** The triangle-inequality LP has an integrality gap of at least 2 on complete graphs (Charikar, Guruswami and Wirth), so ratio 2.06 is close to the limit of rounding this LP.
- **Size of the search space.** $B_n$ grows faster than $c^n$ for each constant $c$: $B_{10} = 115975$ and $B_{20} \approx 5.2 \times 10^{13}$.

## Reductions

- **To and from multicut.** On general weighted graphs, MinDisagree and minimum multicut reduce to each other with only a constant factor loss (Demaine et al. 2006; Charikar, Guruswami and Wirth 2005).
- **Consensus clustering.** The median partition problem is weighted correlation clustering with $w^+_{uv}$ equal to the fraction of the input clusterings that join $u$ and $v$; see [consensus clustering](/consensus-clustering/).
- **Clique partitioning.** Maximizing $\sum_{u \sim v} c_{uv}$ over partitions is the same problem with $c_{uv} = w^+_{uv} - w^-_{uv}$, up to an additive constant.
- **Modularity.** Maximizing [modularity](/modularity/) is also a clique partitioning problem, with $c_{uv} = A_{uv} - d_u d_v/(2m)$.

## Applications

- **Entity resolution and deduplication.** A classifier labels pairs of records as "same entity" or not, and correlation clustering turns the noisy pairwise answers into consistent groups.
- **Document and co-reference clustering**, the motivating example of Bansal, Blum and Chawla.
- **Combining clusterings** ([consensus clustering](/consensus-clustering/)) and ranking aggregation (Ailon, Charikar and Newman).
- **Community detection on signed networks**, where edges mean friendship or hostility.

## References
