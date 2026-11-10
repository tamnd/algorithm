---
tag: NNHQ8F
kind: technique
slug: dual-fitting
name: Dual fitting
aliases:
- Dual fitting analysis
- dual fitting
- dual fitting analysis
- fitting the dual
area: approximation/lp-rounding
level: advanced
summary: Analyse a greedy algorithm by scaling the charges it pays into a feasible dual solution; weak duality then bounds its cost by the scale factor times the optimum.
prereqs: [lp-duality, weak-duality, dual-linear-program, greedy-algorithm]
see_also: [greedy-set-cover, primal-dual-schema, set-cover-primal-dual, jain-vazirani-facility-location, facility-location-problem, linear-programming-rounding, harmonic-series, maximum-weight-matching]
sources:
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 13 (set cover via dual fitting, and constrained set multicover)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 1.6 (a greedy algorithm for set cover analyzed by dual fitting) and Section 9.4 (a greedy algorithm for uncapacitated facility location)
  - paper: doi:10.1016/0012-365X(75)90058-8
    title: László Lovász, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13(4), 1975
    locator: pages 383 to 390
  - paper: doi:10.1287/moor.4.3.233
    title: Vašek Chvátal, A greedy heuristic for the set-covering problem, Mathematics of Operations Research 4(3), 1979
    locator: pages 233 to 235
  - paper: doi:10.1145/950620.950621
    title: Kamal Jain, Mohammad Mahdian, Evangelos Markakis, Amin Saberi and Vijay V. Vazirani, Greedy facility location algorithms analyzed using dual fitting with factor-revealing LP, Journal of the ACM 50(6), 2003
    locator: pages 795 to 824
---

Dual fitting is a way to prove an approximation ratio for a combinatorial algorithm, most often a greedy one, with an LP that the algorithm never solves. As the algorithm runs, it charges its cost to the elements or clients it serves, so that the charges sum to the cost. These charges are usually not a feasible solution of the [dual LP](/dual-linear-program/), but divided by a factor $\gamma$ they are. [Weak duality](/weak-duality/) then gives $\text{ALG} = \gamma \sum_j y_j \le \gamma \cdot \text{LP}^* \le \gamma \cdot \text{OPT}$ for a minimization problem. The classic case is greedy set cover, where the charges are the prices per element and $\gamma = H_d$, the harmonic number of the largest set size.

## In plain words

Some simple algorithms work well, but it is not clear how to compare them with the best answer, which is unknown. Dual fitting compares them with a lower bound instead.

Each time the algorithm pays, it splits the bill among the items it serves. The split amounts look like a certificate that the best answer costs at least their sum, but they are a little too large to be a valid certificate. Shrink them all by the same factor until they become valid. Then the best answer costs at least the shrunken sum, and the algorithm paid that factor times the shrunken sum.

## When it applies

- **An LP relaxation with a known dual.** The problem has a relaxation $\min \{ c \cdot x : A x \ge b, x \ge 0 \}$ whose dual $\max \{ b \cdot y : A^{\top} y \le c, y \ge 0 \}$ has a clear meaning, such as a payment for each element or client.
- **An algorithm that pays as it goes.** Each step of the algorithm has a cost that can be split among the dual variables, so that $\text{ALG} \le \sum_j b_j \alpha_j$ for the charges $\alpha$.
- **Bounded overpayment.** Each dual constraint is violated by the charges by at most a factor $\gamma$: $\sum_j a_{ij} \alpha_j \le \gamma \, c_i$ for each $i$. This is the part of the proof that uses the structure of the algorithm.

## The template

```pseudo id=main
DUAL-FIT(I)
L1  run the algorithm on I and record a charge α_j ≥ 0 for each dual variable   ▷ hole: CHARGE
L2  check that the charges pay for the output: ALG ≤ Σ_j b_j α_j
L3  y ← α / γ                                                                  ▷ hole: FACTOR γ
L4  prove that y is dual feasible: Σ_j a_ij y_j ≤ c_i for each i                ▷ hole: FIT
L5  conclude ALG ≤ γ · b·y ≤ γ · LP* ≤ γ · OPT                                  ▷ weak duality
```

The template is a proof, not a computation: no LP is solved, and the algorithm keeps its own running time.

**Claim.** If $\text{ALG} \le \sum_j b_j \alpha_j$ and $y = \alpha / \gamma$ is feasible for the dual, then $\text{ALG} \le \gamma \cdot \text{OPT}$ in the worst case, and the integrality gap of the relaxation is at most $\gamma$.

*Proof.* By weak duality, $b \cdot y \le c \cdot x$ for each feasible primal $x$, so $b \cdot y \le \text{LP}^* \le \text{OPT}$. Then $\text{ALG} \le b \cdot \alpha = \gamma \, b \cdot y \le \gamma \cdot \text{LP}^*$. The algorithm returns an integral solution of cost at most $\gamma \cdot \text{LP}^*$, so the integral optimum is at most $\gamma \cdot \text{LP}^*$ on each instance. $\square$

**The holes.**

- **CHARGE.** How the cost of each step is split. For greedy set cover, the cost of a chosen set is split evenly among the elements it newly covers.
- **FACTOR.** The smallest $\gamma$ for which the fit works. It can be a closed form, such as $H_d$, or the optimum of a *factor-revealing LP* that finds the worst case of the inequalities that the charges satisfy.
- **FIT.** The per-constraint proof. It uses the order in which the algorithm made its choices.

## Classic examples

- **Greedy set cover.** The set cover LP is $\min \sum_S c_S x_S$ subject to $\sum_{S \ni e} x_S \ge 1$, with dual $\max \sum_e y_e$ subject to $\sum_{e \in S} y_e \le c_S$. When greedy picks a set of least cost per new element, each newly covered element gets that ratio as its price, so the prices sum to the cost. Fix a set $S$ of size $s$ and list its elements in the order in which they are covered, $e_1, \ldots, e_s$. Just before $e_i$ is covered, the elements $e_i, \ldots, e_s$ are uncovered, so $S$ offers a ratio of at most $c_S / (s - i + 1)$, and the price of $e_i$ is at most that. Summing, $\sum_{e \in S} \text{price}(e) \le c_S H_s \le c_S H_d$. So $y = \text{price} / H_d$ is dual feasible, and $\text{ALG} \le H_d \cdot \text{OPT}$. See [greedy set cover](/greedy-set-cover/).
- **A tight fit.** Take elements $e_1, \ldots, e_n$, singletons $\{e_i\}$ of cost $1/i$, and one set $U$ of all elements with cost $1 + \varepsilon$. Greedy buys $\{e_n\}, \ldots, \{e_1\}$ in this order, and $e_i$ has price $1/i$. On $U$ the prices sum to $H_n > 1 + \varepsilon$, so they do not fit. Divided by $H_n$ they fit: the sum on $U$ is $1$, and each singleton gets $y_{e_i} = 1/(i H_n) \le 1/i$. So the dual value is 1, ALG $= H_n$, and the factor $\gamma = H_n$ cannot be lowered here.
- **Greedy maximum weight matching.** For maximization the roles turn around. Greedy takes edges in order of decreasing weight when both ends are free. For each chosen edge $uv$ of weight $w$, set $y_u = y_v = w$. A rejected edge $ab$ met an earlier chosen edge of weight at least $w_{ab}$ at $a$ or $b$, so $y_a + y_b \ge w_{ab}$. This $y$ is feasible for the dual $\min \sum_v y_v$ subject to $y_u + y_v \ge w_{uv}$, and $\sum_v y_v = 2 \cdot \text{ALG}$, so $\text{OPT} \le \text{LP}^* \le 2 \cdot \text{ALG}$. See [maximum weight matching](/maximum-weight-matching/).
- **Greedy facility location.** For uncapacitated metric [facility location](/facility-location-problem/), the dual has a payment $\alpha_j$ for each client $j$ with $\sum_j \max(0, \alpha_j - c_{ij}) \le f_i$ for each facility $i$. Jain, Mahdian, Markakis, Saberi and Vazirani (2003) raise the payments of all unconnected clients at the same rate and open a facility when the payments that reach it cover its cost. The payments are not feasible, but divided by 1.861 they are, which a factor-revealing LP shows. A variant that lets clients switch facilities gives 1.61. Compare the primal-dual method of [Jain and Vazirani](/jain-vazirani-facility-location/), where the payments are feasible by construction. No ratio below 1.463 is possible for metric facility location unless NP has slightly superpolynomial algorithms (Guha and Khuller, 1999).
- **Constrained set multicover.** Each element $e$ must be covered $r_e$ times, by different sets. The greedy algorithm that picks the set of least cost per element that still needs coverage is an $H_n$-approximation, where $n$ is the number of elements, by a dual fit with one extra dual variable for each set (Vazirani, Chapter 13).

## Variations

- **Factor-revealing LP.** When the worst case of the fit is not clear, write the inequalities that the charges satisfy as an LP in the charges, and maximize the ratio. Its optimum, over all sizes, is the factor $\gamma$.
- **Primal-dual schema.** The [primal-dual schema](/primal-dual-schema/) raises a dual that stays feasible at all times, so $\gamma$ comes from the relaxed complementary slackness and not from scaling; see [primal-dual for set cover](/set-cover-primal-dual/).
- **Online and scheduling problems.** Dual fitting gives competitive ratios of online algorithms and bounds for scheduling with speed augmentation, where the algorithm is compared with an optimum on slower machines; see [online algorithms](/online-algorithm/).
- **Fitting a stronger LP.** A fit against a stronger relaxation, such as one with extra valid inequalities, can give a smaller $\gamma$, because the dual has more variables to absorb the charges.

## Pitfalls

- **Charges that do not pay for the output.** If $\sum_j b_j \alpha_j < \text{ALG}$, the chain of inequalities breaks at the first step. Check line L2 on its own.
- **Fitting only the tight constraints.** The fit must hold for every dual constraint, including sets or facilities that the algorithm never chose. In greedy set cover the per-set bound is proved for each set $S$, not only for the chosen ones.
- **A factor from one instance.** A ratio seen on examples is a lower bound on $\gamma$, not a proof. The fit must hold for all instances, which needs a proof or a factor-revealing LP over all sizes.
- **Reading $\gamma$ as tight for the problem.** The fit bounds the algorithm against $\text{LP}^*$. The algorithm may be better than $\gamma$ against OPT, and the problem may allow a smaller ratio by another method.

## Exercises

1. Write the dual of the set cover LP, and check that $y_e = \text{price}(e)/H_d$ satisfies every dual constraint for the tight fit example above with $n = 3$.
2. Prove the greedy maximum weight matching bound above, and give a graph where greedy reaches exactly half of the optimum in the limit.
3. For the tight fit example with $n \ge 2$ and $0 < \varepsilon < H_n - 1$, show that $\text{LP}^* = \text{OPT} = 1 + \varepsilon$. Conclude that the loss of the factor $H_n$ comes from the algorithm and not from the relaxation.

## References
