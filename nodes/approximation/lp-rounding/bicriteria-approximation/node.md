---
tag: 8TWMEK
kind: definition
slug: bicriteria-approximation
name: Bicriteria approximation
aliases:
- bicriteria guarantee
- (alpha, beta)-approximation
- bicriteria approximation algorithm
area: approximation/lp-rounding
level: advanced
summary: An (alpha, beta) guarantee returns a solution of cost at most alpha times the optimum that meets the budget B, while it may use up to beta times B; it is used when meeting B exactly is NP-hard.
prereqs: [approximation-ratio, lp-relaxation, np-hard]
see_also: [shmoys-tardos-gap, generalized-assignment-problem, iterative-relaxation, dual-approximation, filtering-technique, approximation-ratio, capacitated-facility-location, lagrangian-relaxation]
sources:
  - title: Madhav V. Marathe, R. Ravi, Ravi Sundaram, S. S. Ravi, Daniel J. Rosenkrantz and Harry B. Hunt III, Bicriteria network design problems, Journal of Algorithms 28(1), 1998
    locator: the definition of an (alpha, beta) approximation and the results for diameter and degree bounded Steiner trees
  - paper: doi:10.1007/BF01585178
    title: David B. Shmoys and Éva Tardos, An approximation algorithm for the generalized assignment problem, Mathematical Programming 62(3), 1993
    locator: the cost C and load 2T guarantee
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.1 (the generalized assignment problem) and Section 11.2 (bounded-degree spanning trees)
  - title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of web sources, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science, 2000
    locator: the approximate Pareto curve
---

A bicriteria approximation is a guarantee for a problem with an objective and a budget constraint, in which the algorithm may break the budget by a bounded factor. It compares its cost with the best solution that keeps the budget exactly. The notion is needed when even finding a solution that meets the budget is NP-hard, as for the [generalized assignment problem](/generalized-assignment-problem/), where no ratio on cost alone is possible. The standard example is the $(1, 2)$ result of [Shmoys and Tardos](/shmoys-tardos-gap/): cost at most the optimum and machine loads at most twice the limit. Steiner and spanning tree problems with degree or diameter bounds give other classic examples.

## Definition

**Setting.** A minimization problem has instances $I$ with a budget $B > 0$, a cost $c(S) \ge 0$ and a usage $u(S) \ge 0$ for each solution $S$. The solutions that *meet the budget* are those with $u(S) \le B$. Let $\text{OPT}(I, B)$ be the least cost among them.

**$(\alpha, \beta)$ approximation.** For $\alpha, \beta \ge 1$, an algorithm is an $(\alpha, \beta)$ *bicriteria approximation* if, for each instance with at least one solution that meets the budget, it returns a solution $S$ with

$$c(S) \le \alpha \cdot \text{OPT}(I, B) \qquad \text{and} \qquad u(S) \le \beta \cdot B.$$

On instances with no solution that meets the budget, it may return anything or report failure.

**Additive form.** The usage bound may be $u(S) \le B + k$ instead of $\beta B$, or a mix such as $u(S) \le 2B + 3$. With several budgets, such as one degree bound $B_v$ per vertex, the bound must hold for each of them.

**Two objectives.** If both $c$ and $u$ are objectives, a solution $S$ is an $(\alpha, \beta)$ approximation of a target point $(C, B)$ when $c(S) \le \alpha C$ and $u(S) \le \beta B$, whenever some solution has $c \le C$ and $u \le B$. The roles of the two criteria are then symmetric.

The first factor is always for the objective being minimized, and the second for the relaxed constraint. A $(1, \beta)$ guarantee is often called a *$\beta$-relaxed* solution of optimal cost.

## Examples and non-examples

**Example (GAP).** In the generalized assignment problem, job $j$ costs $c_{ij}$ and takes $p_{ij}$ on machine $i$, and the budget is a load limit $T$ on each machine. The [Shmoys-Tardos rounding](/shmoys-tardos-gap/) returns, for each instance that has an assignment with loads at most $T$, an assignment of cost at most $\text{OPT}(I, T)$ with loads at most $2T$. So it is a $(1, 2)$ bicriteria approximation. No $(\alpha, \beta)$ guarantee with $\beta < 3/2$ and finite $\alpha$ is possible unless P = NP, by the hardness of [unrelated machine scheduling](/unrelated-machine-scheduling-makespan/), and none with $\beta = 1$, since deciding feasibility is NP-hard.

**Example (bounded degree spanning trees).** Given costs and a degree bound $B_v$ for each vertex, the [iterative relaxation](/iterative-relaxation/) algorithm of Singh and Lau returns a spanning tree of cost at most the optimum among trees with all degrees at most $B_v$, with each degree at most $B_v + 1$. This is a $(1, B_v + 1)$ guarantee in the additive form.

**Example (Steiner trees and networks with degree bounds).** For [survivable network design](/survivable-network-design/), with the Steiner tree and the [Steiner forest](/steiner-forest/) as special cases, Lau, Naor, Salavatipour and Singh (2007) gave cost at most $2 \cdot \text{OPT}$ with each degree at most $2 B_v + 3$. The cost factor 2 matches the best ratio without degree bounds.

**Example (Steiner trees with a diameter bound).** Marathe et al. (1998) studied Steiner trees of least cost whose diameter, or depth from a root, is at most $D$. They gave guarantees with logarithmic factors on both criteria: cost $O(\log k)$ times the optimum among trees of diameter at most $D$, with $k$ terminals, and diameter $O(\log k) \cdot D$.

**Example ($k$-median).** With $k$ as the budget on the number of open facilities, the [filtering](/filtering-technique/) method of Lin and Vitter (1992) rounds the LP to a solution of cost within a constant factor of the LP that opens at most a constant times $k$ facilities.

**Example (balanced cuts).** Leighton and Rao find a $1/3$-balanced cut of capacity $O(\log n)$ times the least capacity of a $1/2$-balanced cut. Here the relaxed constraint is the balance: the smaller side may hold only a third of the vertices, not a half.

**Non-example (unbounded violation).** An algorithm for GAP that returns cost at most OPT but may give a machine any load is not a bicriteria approximation: the cheapest machine for each job already achieves this, with no bound on the load.

**Non-example (comparison with the relaxed optimum).** An algorithm that returns $u(S) \le \beta B$ and $c(S) \le \alpha \cdot \text{OPT}(I, \beta B)$ satisfies a weaker guarantee. Since $\text{OPT}(I, \beta B) \le \text{OPT}(I, B)$, an $(\alpha, \beta)$ approximation as defined above also satisfies it, but not the other way around.

**Non-example (one combined objective).** A bound $c(S) + \lambda u(S) \le \alpha \min_{S'} (c(S') + \lambda u(S'))$ for a fixed $\lambda$ is a single-criterion ratio for a [Lagrangian](/lagrangian-relaxation/) objective. It bounds neither the cost nor the usage on its own, so it is not a bicriteria guarantee, although such bounds are often a step toward one.

## Related definitions

- **[Approximation ratio](/approximation-ratio/).** An $(\alpha, 1)$ bicriteria approximation is an $\alpha$-approximation in the usual sense, with the budget as a hard constraint.
- **[Dual approximation](/dual-approximation/).** Hochbaum and Shmoys call an algorithm a $\rho$-relaxed decision procedure if, for a target $T$, it either finds a schedule of makespan at most $\rho T$ or shows that none of makespan $T$ exists. It is the $(1, \rho)$ bicriteria idea for a problem with no cost.
- **Approximate Pareto curve.** Papadimitriou and Yannakakis (2000) define a set of solutions that contains, for each solution $S'$, some $S$ with $c(S) \le (1 + \varepsilon) c(S')$ and $u(S) \le (1 + \varepsilon) u(S')$. It is a family of bicriteria approximations for all budgets at once.
- **Resource augmentation.** In online and scheduling problems, the algorithm gets faster machines or more machines than the optimum it is compared with. This is a bicriteria guarantee where the second criterion is the resource.
- **Lagrangian multiplier preserving.** A guarantee of the form $c(S) + \alpha \cdot \text{penalty}(S) \le \alpha \cdot \text{OPT}$, used for [prize-collecting](/prize-collecting-steiner-tree/) and $k$-median problems. It turns into bicriteria results by a search on the multiplier.

## References
