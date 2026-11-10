---
tag: VVZHJZ
kind: technique
slug: filtering-technique
name: Filtering technique
aliases:
- Lin-Vitter filtering
- filtering and rounding
- LP filtering
area: approximation/lp-rounding
level: advanced
summary: Discard assignments with large fractional cost before rounding, so that each client is served near its LP cost; this yields bicriteria and constant-factor guarantees.
prereqs: [linear-programming-rounding, lp-relaxation, markov-inequality, facility-location-problem]
see_also: [shmoys-tardos-aardal-facility-location, k-median-problem, bicriteria-approximation, generalized-assignment-problem, unrelated-machine-scheduling-makespan, capacitated-facility-location, jain-vazirani-facility-location, threshold-rounding]
sources:
  - paper: "Jyh-Han Lin and Jeffrey Scott Vitter, ε-approximations with minimum packing constraint violation, Proceedings of the 24th Annual ACM Symposium on Theory of Computing (STOC), 1992"
    locator: pages 771 to 782
  - paper: "David B. Shmoys, Éva Tardos and Karen Aardal, Approximation algorithms for facility location problems, Proceedings of the 29th Annual ACM Symposium on Theory of Computing (STOC), 1997"
    locator: pages 265 to 274
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 4.5 (uncapacitated facility location by deterministic rounding and clustering)
---

Filtering is a step between solving an LP relaxation and rounding it. In a fractional solution, a client may be served in part by far facilities, even when its average cost is small. Filtering removes, for each client $j$, all assignments whose cost is more than $1 + \varepsilon$ times the fractional cost $C_j$ of $j$, and scales the rest up. By [Markov's inequality](/markov-inequality/), at least a fraction $\varepsilon / (1 + \varepsilon)$ of each client survives, so the scaling costs a factor $1 + 1/\varepsilon$ on the other part of the objective. After filtering, every client is served only from facilities within $(1 + \varepsilon) C_j$, which a later rounding step can use. Lin and Vitter introduced the method in 1992 for problems such as [k-median](/k-median-problem/), where it gives [bicriteria](/bicriteria-approximation/) results. Shmoys, Tardos and Aardal used it in 1997 for the first constant ratio for metric facility location.

## In plain words

Suppose each client of a fractional plan buys service from a mix of shops, some close and some far. The average distance is small, but a few far shops can spoil a rounding.

So for each client, drop the shops that are much farther than its average, and buy more from the close ones to make up. Not much can be far: if most of the mix were far, the average would be large too. So the close shops already carry a fair share, and the extra purchase is at most a fixed factor. Now each client uses only close shops, which makes it simple to pick one shop for it.

## When it applies

- **An assignment LP.** Each client $j$ is assigned fractionally, $\sum_i x_{ij} = 1$, to resources $i$ with costs $c_{ij} \ge 0$, and the assignment is bounded by an opening or capacity variable, $x_{ij} \le y_i$, that has its own cost.
- **Two parts of the objective.** One part is the assignment cost $\sum_{i,j} c_{ij} x_{ij}$, and the other is a cost or a constraint on the $y$ variables, such as an opening cost $\sum_i f_i y_i$ or a bound $\sum_i y_i \le k$. Filtering trades one part against the other.
- **A rounding that needs locality.** The next step, often clustering in a metric, needs each client to be served only from nearby resources.

## The template

```pseudo id=main
FILTER-AND-ROUND(I, ε)
L1  (x, y) ← an optimal solution of the LP relaxation of I
L2  for each client j: C_j ← Σ_i c_ij x_ij
L3  for each client j: N(j) ← {i : c_ij ≤ (1+ε) C_j}                 ▷ hole: FILTER rule
L4  for each client j and i ∈ N(j): x'_ij ← x_ij / Σ_{h ∈ N(j)} x_hj; x'_ij ← 0 for i ∉ N(j)
L5  for each resource i: y'_i ← min(1, (1 + 1/ε) y_i)
L6  return ROUND(x', y')                                               ▷ hole: clustering, matching, or GAP rounding
```

**Lemma (filtering).** For each client $j$, $\sum_{i \in N(j)} x_{ij} \ge \frac{\varepsilon}{1 + \varepsilon}$. Hence $(x', y')$ is feasible, $x'_{ij} > 0$ only when $c_{ij} \le (1 + \varepsilon) C_j$, and $\sum_i f_i y'_i \le (1 + \frac{1}{\varepsilon}) \sum_i f_i y_i$.

*Proof.* If $C_j = 0$, all of the assignment of $j$ is on resources with $c_{ij} = 0$, which are in $N(j)$. Otherwise, each $i \notin N(j)$ has $c_{ij} > (1 + \varepsilon) C_j$, so

$$C_j \ge \sum_{i \notin N(j)} c_{ij} x_{ij} > (1 + \varepsilon) C_j \sum_{i \notin N(j)} x_{ij},$$

which gives $\sum_{i \notin N(j)} x_{ij} < \frac{1}{1 + \varepsilon}$ and the first claim. Then $x'_{ij} \le \frac{1 + \varepsilon}{\varepsilon} x_{ij} \le (1 + \frac{1}{\varepsilon}) y_i$, and $x'_{ij} \le 1$, so $x'_{ij} \le y'_i$. The new assignment of $j$ sums to 1. The cost bound follows from $y'_i \le (1 + \frac{1}{\varepsilon}) y_i$. $\square$

The LP has polynomial size, so line L1 runs in polynomial time with an interior point or ellipsoid method and no separation oracle. Lines L2 to L5 take linear time in the size of the LP.

**The holes.**

- **FILTER.** The threshold $(1 + \varepsilon) C_j$ is the classic rule. A threshold at a random multiple of $C_j$, or at a quantile of the distribution of $c_{ij}$ under $x_{\cdot j}$, gives better constants.
- **ROUND.** The rounding of the filtered solution. For facility location it is a clustering step; for assignment problems it is the rounding of a bipartite assignment.

## Classic examples

- **Metric uncapacitated facility location, ratio 4.** Let $F = \sum_i f_i y_i$ and $C = \sum_j C_j$, so $\text{LP}^* = F + C \le \text{OPT}$. After filtering, take the clients in increasing order of $C_j$. For the next client $j$ not yet assigned, open the cheapest facility $i$ in $N(j)$, and assign to $i$ the client $j$ and each unassigned client $j'$ with $N(j') \cap N(j) \ne \emptyset$. Since $\sum_{h \in N(j)} y'_h \ge 1$, $f_i \le \sum_{h \in N(j)} f_h y'_h$, and the sets $N(j)$ of different centers are disjoint, so the opening cost is at most $(1 + \frac{1}{\varepsilon}) F$. By the triangle inequality through a facility $h \in N(j') \cap N(j)$, client $j'$ pays at most $(1 + \varepsilon)(C_{j'} + 2 C_j) \le 3 (1 + \varepsilon) C_{j'}$, because $C_j \le C_{j'}$. The total is at most $(1 + \frac{1}{\varepsilon}) F + 3(1 + \varepsilon) C$, and $\varepsilon = \frac13$ gives $4 F + 4 C \le 4 \cdot \text{OPT}$ in the worst case. Shmoys, Tardos and Aardal (1997) chose the threshold at random and got 3.16; see [Shmoys-Tardos-Aardal facility location](/shmoys-tardos-aardal-facility-location/). No ratio below 1.463 is possible unless NP has slightly superpolynomial algorithms (Guha and Khuller, 1999).
- **k-median, bicriteria.** For [k-median](/k-median-problem/), the constraint $\sum_i y_i \le k$ takes the place of the opening cost. Lin and Vitter (1992) used filtering and rounding to get a solution of cost at most $2(1 + \varepsilon)$ times the LP value that opens at most $(1 + 1/\varepsilon) k$ medians, which is a [bicriteria approximation](/bicriteria-approximation/).
- **Scheduling and assignment.** For [unrelated machine scheduling](/unrelated-machine-scheduling-makespan/) with a guessed makespan $T$, drop each assignment of job $j$ to machine $i$ with $p_{ij} > T$ before the LP is solved. This filter is what makes the rounded makespan at most $2T$. The same step appears in the [generalized assignment problem](/generalized-assignment-problem/) and [Shmoys-Tardos GAP rounding](/shmoys-tardos-gap/).
- **Capacitated facility location.** Filtering combined with a rounding that respects capacities gives constant ratios for some capacitated variants; see [capacitated facility location](/capacitated-facility-location/).

## Variations

- **Random threshold.** Pick the multiple $1 + \varepsilon$ from a distribution and average the two bounds; this gives 3.16 for facility location.
- **Filtering with the dual.** Use the dual value $v_j$ of client $j$ as the radius in place of $(1 + \varepsilon) C_j$. Complementary slackness puts every facility with $x_{ij} > 0$ within $v_j$, so no scaling is needed and the ratio is 4; see the dual-based rounding in Williamson and Shmoys, Section 4.5.
- **Primal-dual algorithms.** The [Jain-Vazirani algorithm](/jain-vazirani-facility-location/) builds a dual and a clustering without solving the LP, for ratio 3.
- **Randomized clustering.** Open one facility in each cluster at random, with probabilities from the LP, open the other facilities on their own with probability $y_i$, and assign each client to the nearest open facility. Chudak and Shmoys got the ratio $1 + 2/e$ in expectation in this way.

## Pitfalls

- **No metric.** The clustering step uses the triangle inequality. Without it, a client can be sent to a facility that is arbitrarily far, and the ratio fails. Non-metric facility location is as hard as [set cover](/set-cover/).
- **The wrong order.** The clustering must take clients in increasing order of $C_j$. In another order, the bound $C_j \le C_{j'}$ fails for a client $j'$ assigned to the center $j$.
- **Filtering on distance alone.** A fixed distance bound for all clients does not give the Markov argument, which needs the threshold to be a multiple of the cost of each client.
- **The trade-off of ε.** A small $\varepsilon$ keeps clients close but makes the factor $1 + 1/\varepsilon$ on the opening cost large. Balance the two bounds for the final ratio.

## Exercises

1. Show that $\max(1 + 1/\varepsilon, 3(1 + \varepsilon))$ is smallest at $\varepsilon = 1/3$, with value 4.
2. Prove the filtering lemma with the threshold $\alpha C_j$ for a general $\alpha > 1$, and find the fraction of each client that survives.
3. Show that in the facility location example the sets $N(j)$ of two cluster centers are disjoint, and that this gives the bound on the opening cost.
4. Give an instance of non-metric facility location where the clustering step pays far more than the LP value.

## References
