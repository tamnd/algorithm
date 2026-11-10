---
tag: W53DKC
kind: theorem
slug: dominating-set-inapproximability
name: Dominating set inapproximability
aliases:
- Raz-Safra dominating set hardness
- ln n hardness of dominating set
- dominating set and set cover equivalence
area: approximation/hardness-of-approximation
level: advanced
summary: Dominating set and set cover reduce to each other with the same optimum, so for each ε > 0 a ratio of (1 - ε) ln n for dominating set is NP-hard, and greedy is within one of this.
prereqs: [dominating-set, set-cover, set-cover-inapproximability, l-reduction]
see_also: [greedy-set-cover, set-cover-inapproximability, max-coverage-inapproximability, k-center-inapproximability, parameterized-dominating-set, parameterized-inapproximability, hitting-set, apx-class]
sources:
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: Theorem 4.4 and Section 4 (the reduction from label cover with partition systems)
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, STOC 2014
    locator: the corollary on set cover, (1 - ε) ln n unless P = NP
  - paper: doi:10.1145/258533.258641
    title: Ran Raz and Shmuel Safra, A sub-constant error-probability low-degree test, and a sub-constant error-probability PCP characterization of NP, STOC 1997
    locator: the corollary on set cover and dominating set, ratio c ln n unless P = NP
  - book: isbn:9783540654315
    title: G. Ausiello, P. Crescenzi, G. Gambosi, V. Kann, A. Marchetti-Spaccamela and M. Protasi, Complexity and Approximation
    locator: Appendix B, compendium entry GT2 (minimum dominating set)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A1.1, problem GT2 (dominating set)
  - paper: doi:10.1016/0022-0000(91)90023-X
    title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: the APX-hardness of dominating set in graphs of bounded degree
  - paper: "M. Chlebík and J. Chlebíková, Approximation hardness of dominating set problems in bounded degree graphs, Information and Computation 206(11), 2008"
    locator: the bound ln Δ - C ln ln Δ for graphs of largest degree Δ
  - paper: "P. Slavík, A tight analysis of the greedy algorithm for set cover, Journal of Algorithms 25(2), 1997"
    locator: the bound ln N - ln ln N + O(1) for greedy
---

Dominating set is as hard to approximate as [set cover](/set-cover/). Two simple reductions, one in each direction, keep the optimum exactly and map solutions back without loss. So the threshold of $\ln n$ for set cover, proved by Feige (1998) under a quasi-polynomial assumption and by Dinur and Steurer (2014) under P $\ne$ NP, also holds for [dominating set](/dominating-set/) on graphs with $n$ vertices. The greedy algorithm reaches $\ln n + 1$, so the threshold is tight up to lower-order terms.

## Statement

A graph $G = (V, E)$ has $n$ vertices and $m$ edges. $N[v]$ is the closed neighbourhood of $v$, and $\gamma(G)$ is the least size of a dominating set. A set cover instance has a universe $U$ of $N$ elements and sets $S_1, \ldots, S_M$, each element in some set. Both problems are minimization problems, and a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance.

**Theorem.**

1. *(Equivalence.)* There are polynomial maps in both directions between dominating set and set cover that keep the optimum value and map each feasible solution of the image back to a feasible solution of the source with no larger cost. So each is an [L-reduction](/l-reduction/) with $\alpha = \beta = 1$, and a ratio $\rho$ for one problem gives the same ratio for the other, measured in the size parameter of the instance that the algorithm sees.
2. *(Threshold.)* For each $\varepsilon > 0$, if a polynomial algorithm has ratio $(1 - \varepsilon) \ln n$ for dominating set on graphs with $n$ vertices, then P = NP.
3. *(Upper bound.)* The greedy set cover algorithm on the sets $N[v]$ has ratio $H_{\Delta + 1} \le \ln(\Delta + 1) + 1 \le \ln n + 1$, where $\Delta$ is the largest degree.

Part 2 uses the set cover theorem in this form: for each $\delta > 0$, a ratio of $(1 - \delta) \ln N$ for set cover is NP-hard on instances with $M \le N$. See the remark after the proof.

## In plain words

Picking few vertices so that every vertex is picked or next to a picked one is the same job as picking few groups that together hold every item. Each vertex with its neighbours is a group. In the other direction, any family of groups becomes a graph: one point per group, one point per item, all group points joined to each other, and each item joined to the groups that hold it. The best answer does not change in either direction.

So the two problems are equally hard to approximate. The covering problem is known to be hard to approximate better than the natural logarithm of its size. Hence the graph problem is too, and the simple greedy rule is almost the best possible.

## Proof

*Dominating set to set cover.* Map $G$ to the universe $V$ with the $n$ sets $N[v]$ for $v \in V$. A set $D \subseteq V$ is dominating exactly when $\bigcup_{v \in D} N[v] = V$, so the dominating sets of $G$ are the covers, with the same size. The instance has $N = M = n$ and total size $\sum_v |N[v]| = n + 2m$.

*Set cover to dominating set.* Build the graph $G'$ with a set vertex $s_j$ for each set $S_j$ and an element vertex $u_e$ for each $e \in U$. Join every two set vertices, and join $u_e$ to $s_j$ when $e \in S_j$. Then $G'$ has $N + M$ vertices and $\binom{M}{2} + \sum_j |S_j|$ edges.

- *A cover gives a dominating set.* Let $\{S_j : j \in J\}$ cover $U$ with $J \neq \emptyset$. Each set vertex is in $\{s_j : j \in J\}$ or adjacent to it, because the set vertices form a clique. Each $u_e$ is adjacent to $s_j$ for a $j \in J$ with $e \in S_j$. So $\{s_j : j \in J\}$ dominates $G'$, and $\gamma(G') \le \mathrm{OPT}_{\mathrm{SC}}$.
- *A dominating set gives a cover.* Let $D$ dominate $G'$. Replace each element vertex $u_e \in D$ by a set vertex $s_j$ with $e \in S_j$. The new set $D'$ has $|D'| \le |D|$ and contains only set vertices. Take an element $e$. It is dominated by $D$: either $u_e \in D$, and then $D'$ contains an $s_j$ with $e \in S_j$, or a neighbour $s_j$ of $u_e$ is in $D$, and then $e \in S_j$ and $s_j \in D'$. So $\{S_j : s_j \in D'\}$ covers $U$, and $\mathrm{OPT}_{\mathrm{SC}} \le \gamma(G')$.

Both maps keep the optimum and map solutions back with no larger cost, which proves part 1.

*Part 2.* Fix $\varepsilon > 0$ and suppose an algorithm $A$ has ratio $(1 - \varepsilon) \ln n$ on graphs with $n$ vertices. Take a set cover instance with $N$ elements and $M \le N$ sets, build $G'$ with $n = N + M \le 2N$ vertices, run $A$, and map its output back as above. The result is a cover with at most

$$(1 - \varepsilon) \ln(2N) \cdot \gamma(G') = (1 - \varepsilon)(\ln N + \ln 2) \cdot \mathrm{OPT}_{\mathrm{SC}}$$

sets. If $\ln N \ge 2 \ln 2 / \varepsilon$, then $(1 - \varepsilon) \ln 2 \le \frac{\varepsilon}{2} \ln N$, so the factor is at most $(1 - \frac{\varepsilon}{2}) \ln N$. Instances with smaller $N$ have a size bounded by a constant that depends only on $\varepsilon$, and are solved exactly by trying all subsets. This gives a polynomial set cover algorithm with ratio $(1 - \frac{\varepsilon}{2}) \ln N$ on instances with $M \le N$, so P = NP by the set cover theorem with $\delta = \varepsilon / 2$.

*Part 3.* The sets $N[v]$ have size $\deg(v) + 1 \le \Delta + 1$, and the greedy set cover bound $H_d$ for largest set size $d$ is proved on the [greedy set cover](/greedy-set-cover/) page. $\blacksquare$

*Remark on the form of the set cover theorem.* The hardness of [set cover](/set-cover-inapproximability/) is proved by a reduction from label cover in which the universe is the set of pairs (edge, point of a partition system) and the sets are indexed by pairs (vertex, label). The ground set of the partition system can be taken polynomially larger than the label cover instance without loss in the ratio, so the hard instances can be taken with $M \le N$. Without this form, the proof above gives the same threshold measured as $(1 - \varepsilon) \ln N$ in the number of element vertices, and the ratio $(1 - \varepsilon) \ln n$ in all vertices for instances with $M \le N^{o(1) + 1}$. This point is a sketch: it depends on the structure of the cited reductions and not only on their statements.

### Example

Take $U = \{0, \ldots, 5\}$ and the sets $\{0, 1, 2\}$, $\{2, 3\}$, $\{3, 4, 5\}$, $\{0, 3\}$, $\{1, 4\}$, $\{5\}$. No single set covers $U$, and $\{0, 1, 2\}$ with $\{3, 4, 5\}$ does, so $\mathrm{OPT}_{\mathrm{SC}} = 2$. The graph $G'$ has $6 + 6 = 12$ vertices and $\binom{6}{2} + 13 = 28$ edges, and $\gamma(G') = 2$. The dominating set $\{s_0, s_2, u_5\}$ is not minimal. If $u_5$ is replaced by the first set vertex that holds 5, which is $s_2$, it maps back to the cover $\{S_0, S_2\}$ with 2 sets. In the other direction, the Petersen graph gives 10 sets of size 4 on 10 elements, and the least cover has 3 sets, because $\gamma = 3$.

## Consequences

- **The same threshold for both problems.** Any ratio $\rho(n)$ for one problem gives the ratio $\rho$ for the other, with $n$ replaced by $N + M$ or by $n$. So an improvement over $\ln n$ for dominating set would improve set cover, and the reverse.
- **Feige's form.** With Feige's theorem in place of Dinur and Steurer's, the ratio $(1 - \varepsilon) \ln n$ is ruled out unless NP $\subseteq$ DTIME$(n^{O(\log \log n)})$. This was the best known form from 1998 to 2014.
- **Weighted versions.** The reductions keep weights: give $s_j$ the weight of $S_j$ and give each $u_e$ the weight of the cheapest set holding $e$. So weighted dominating set and weighted set cover are also equivalent.
- **Bounded degree.** For each fixed $\Delta \ge 3$, dominating set on graphs of largest degree $\Delta$ is APX-hard (Papadimitriou and Yannakakis 1991), so it has no [PTAS](/ptas/) unless P = NP. For large $\Delta$, Chlebík and Chlebíková (2008) show that the ratio $\ln \Delta - C \ln \ln \Delta$ is NP-hard for a constant $C$, which nearly matches the greedy bound $\ln(\Delta + 1) + 1$.
- **Other problems.** The graph $G'$ has a clique on the set vertices, so a [$k$-center](/k-center-inapproximability/) reduction or a [parameterized](/parameterized-inapproximability/) one that starts from dominating set can start from set cover. Under Gap-ETH, $k$-dominating set has no FPT algorithm with ratio $f(k)$ for any function $f$.

## Tightness

The threshold $\ln n$ is tight up to an additive constant in the ratio: greedy gives $\ln(\Delta + 1) + 1 \le \ln n + 1$, and part 2 rules out $(1 - \varepsilon) \ln n$. For set cover, Slavík (1997) showed that greedy has ratio $\ln N - \ln \ln N + O(1)$, so the exact lower-order term of the threshold is not known for either problem.

The size relation matters. The map from dominating set to set cover keeps $N = M = n$, so it gives no loss. The map from set cover to dominating set adds $M$ vertices. If $M$ were much larger than $N$, for example $M = N^c$, then $\ln n \approx c \ln N$ and the transfer would lose the factor $c$. This is why the proof needs the form of the set cover theorem with $M \le N$.

## History

The two reductions are standard; the compendium of Ausiello et al. lists dominating set as equivalent to set cover under L-reductions (entry GT2). Johnson (1974) proved the greedy bound for set cover. Lund and Yannakakis (1994) gave the first logarithmic hardness of set cover, under a quasi-polynomial assumption, and Raz and Safra (1997) obtained a ratio $c \ln n$ for some constant $c > 0$ unless P = NP, by a PCP with sub-constant error. Feige (1998) proved the sharp threshold $(1 - \varepsilon) \ln n$ under NP $\not\subseteq$ DTIME$(n^{O(\log \log n)})$, and Dinur and Steurer (2014) proved it unless P = NP. Each of these results transfers to dominating set by the reduction above.

## References
