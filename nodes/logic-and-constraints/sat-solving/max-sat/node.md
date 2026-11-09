---
tag: W2TT9G
kind: problem
slug: max-sat
name: Maximum satisfiability
aliases:
- MAX-SAT
- MaxSAT
area: logic-and-constraints/sat-solving
level: core
summary: Find an assignment that satisfies as many clauses of a CNF formula as possible. NP-hard even for 2-clauses; a random assignment gives 1/2, and LP rounding with it gives 3/4.
prereqs: [sat, conjunctive-normal-form, np-hard, lp-relaxation]
see_also: [max-2-sat, weighted-max-sat, partial-max-sat, core-guided-maxsat, max-3sat-inapproximability, randomized-rounding, method-of-conditional-expectations, walksat]
sources:
  - paper: doi:10.1016/S0022-0000(74)80044-9
    title: "David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9 (1974), 256 to 278"
    locator: the section on maximum satisfiability, the greedy 1/2 approximation
  - paper: doi:10.1137/S0895480192243516
    title: "Michel X. Goemans and David P. Williamson, New 3/4-approximation algorithms for the maximum satisfiability problem, SIAM Journal on Discrete Mathematics 7 (1994), 656 to 666"
    locator: the LP relaxation, randomized rounding with 1 - 1/e, and the best of two algorithms
  - paper: doi:10.1006/jagm.1994.1045
    title: "Mihalis Yannakakis, On the approximation of maximum satisfiability, Journal of Algorithms 17 (1994), 475 to 502"
    locator: the first 3/4 approximation
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: "Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1 (1976), 237 to 267"
    locator: the NP-completeness of MAX-2-SAT
  - paper: doi:10.1145/502090.502098
    title: "Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48 (2001), 798 to 859"
    locator: the 7/8 bound for MAX-E3-SAT
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms (2011)
    locator: Chapter 5, Sections 5.1 to 5.5 (random assignment, derandomization, LP rounding, the best of two)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapters on MaxSAT
---

Maximum satisfiability (MAX-SAT) asks for an assignment of a [CNF](/conjunctive-normal-form/) formula that makes as many clauses true as possible. It generalizes [SAT](/sat/), which asks whether all clauses can be true at once. MAX-SAT is [NP-hard](/np-hard/), even when every clause has at most two literals ([MAX-2-SAT](/max-2-sat/)), although [2-SAT](/2-sat/) itself is easy. It is a basic problem of approximation: a random assignment satisfies at least half of the clauses in expectation, and the better of random assignment and LP rounding gives $3/4$. The practical versions with weights and hard clauses, [weighted MaxSAT](/weighted-max-sat/) and [partial MaxSAT](/partial-max-sat/), are solved exactly by [core-guided](/core-guided-maxsat/) and other SAT-based methods.

## In plain words

You have a list of yes-or-no choices and a list of wishes. Each wish names a few choices and is met if at least one of them goes its way. Often not all wishes can be met. The task is to make the choices so that as many wishes as possible are met.

Even flipping a coin for each choice meets at least half of the wishes on average, since each wish has at least one chance to be met. A smarter method looks at a relaxed version of the problem with fractional choices, and uses it to bias the coins. The better of the two meets at least three quarters of the best possible number. Finding the true best is hard in general.

## Definition

The input is a CNF formula $F = C_1 \wedge \cdots \wedge C_m$ over $x_1, \ldots, x_n$. For an assignment $x$, let $\mathrm{sat}(x)$ be the number of clauses that $x$ makes true. The output is an assignment $x$ that maximizes $\mathrm{sat}(x)$. The value $\mathrm{OPT}(F) = \max_x \mathrm{sat}(x)$. Equivalently, minimize the number of false clauses, $m - \mathrm{sat}(x)$; the two forms have the same optimal solutions but behave differently under approximation.

The decision version asks, for $F$ and $t$, whether some $x$ has $\mathrm{sat}(x) \ge t$. It is in NP, and it is NP-complete by the reductions below. An algorithm is an $\alpha$-approximation if it returns $x$ with $\mathrm{sat}(x) \ge \alpha \cdot \mathrm{OPT}(F)$, in expectation for a randomized algorithm.

## Variants

- **MAX-$k$-SAT and MAX-E$k$-SAT.** Clauses have at most $k$ literals, or exactly $k$ distinct variables. See [MAX-2-SAT](/max-2-sat/).
- **[Weighted MaxSAT](/weighted-max-sat/).** Each clause has a positive weight; maximize the total weight of true clauses.
- **[Partial MaxSAT](/partial-max-sat/).** Some clauses are hard and must be true; maximize the number or weight of true soft clauses.
- **MIN-SAT and MIN-UNSAT.** Minimize the number of true clauses, or the number of false clauses; the second has the same optima as MAX-SAT.
- **MAX-CSP.** Constraints of other types, as in [MAX-CUT](/maximum-cut/) or [MAX-XOR-SAT](/xor-sat/).

## Examples

**Four clauses on two variables.** $F = (x_1 \vee x_2) \wedge (x_1 \vee \neg x_2) \wedge (\neg x_1 \vee x_2) \wedge (\neg x_1 \vee \neg x_2)$. Each assignment makes exactly one clause false, the one whose two literals are both false, so $\mathrm{OPT} = 3$ and every assignment is optimal. The LP relaxation below has value 4, at $y_1 = y_2 = 1/2$ and all $z_j = 1$, so the [integrality gap](/integrality-gap/) of this LP is at least $4/3$, and an analysis that compares with the LP value cannot prove a ratio better than $3/4$.

**A gadget.** For a clause $(a \vee b \vee c)$ and a new variable $d$, the ten clauses $(a), (b), (c), (d), (\neg a \vee \neg b), (\neg a \vee \neg c), (\neg b \vee \neg c), (a \vee \neg d), (b \vee \neg d), (c \vee \neg d)$ have the property that, for each assignment of $a, b, c$, the best choice of $d$ satisfies 7 of them if $a \vee b \vee c$ is true, and 6 if it is false. This is the reduction of Garey, Johnson and Stockmeyer from [3-SAT](/3-sat/) to MAX-2-SAT; all eight cases were checked by a script.

## Known algorithms

**Random assignment, ratio 1/2.** Set each variable true with probability 1/2. A clause with $k \ge 1$ distinct literals is false only if all $k$ literals are false, with probability $2^{-k}$, so it is true with probability $1 - 2^{-k} \ge 1/2$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\mathrm{sat}(x)] \ge m/2 \ge \mathrm{OPT}/2$. A deterministic version: for any $x$, each non-empty clause is true under $x$ or under its complement $\bar{x}$, because a clause false under $x$ has all literals false under $x$, hence all true under $\bar{x}$. So $\mathrm{sat}(x) + \mathrm{sat}(\bar{x}) \ge m$, and the better of the two satisfies at least $m/2$. The [method of conditional expectations](/method-of-conditional-expectations/) also derandomizes the coin flips; this gives Johnson's 1974 algorithm. For MAX-E3-SAT the same argument gives $7/8$.

**LP rounding, ratio $1 - 1/e$.** Let $P_j$ and $N_j$ be the variables that appear positive and negative in $C_j$. The [LP relaxation](/lp-relaxation/) is

$$\max \sum_j z_j \quad \text{subject to} \quad \sum_{i \in P_j} y_i + \sum_{i \in N_j} (1 - y_i) \ge z_j, \quad 0 \le y_i \le 1, \quad 0 \le z_j \le 1.$$

Every assignment gives a feasible point with $z_j = 1$ for true clauses, so the LP value $Z^* \ge \mathrm{OPT}$. Solve it, and set $x_i$ true with probability $y_i^*$ ([randomized rounding](/randomized-rounding/)). For a clause with $k$ literals, the probability that all are false is $\prod_{i \in P_j} (1 - y_i^*) \prod_{i \in N_j} y_i^*$. By the inequality of arithmetic and geometric means, this is at most $\big(1 - \tfrac{1}{k}(\sum_{P_j} y_i^* + \sum_{N_j} (1 - y_i^*))\big)^k \le (1 - z_j^*/k)^k$. The function $g(z) = 1 - (1 - z/k)^k$ is concave on $[0, 1]$ with $g(0) = 0$, so $g(z) \ge g(1) z$ there, and

$$\Pr[C_j \text{ true}] \ge \Big(1 - \big(1 - \tfrac{1}{k}\big)^k\Big) z_j^* \ge \big(1 - \tfrac{1}{e}\big) z_j^*.$$

Summing, the expected value is at least $(1 - 1/e) Z^* \ge 0.632\,\mathrm{OPT}$.

**The best of two, ratio 3/4 (Goemans and Williamson 1994).** Run both and keep the better. Its value is at least the average of the two expectations. For a clause of size $k$, with $z_j^* \le 1$, the average is at least

$$\tfrac{1}{2}(1 - 2^{-k}) z_j^* + \tfrac{1}{2}\Big(1 - \big(1 - \tfrac{1}{k}\big)^k\Big) z_j^*.$$

For $k = 1$ the bracket is $\tfrac12 \cdot \tfrac12 + \tfrac12 \cdot 1 = \tfrac34$; for $k = 2$ it is $\tfrac12 \cdot \tfrac34 + \tfrac12 \cdot \tfrac34 = \tfrac34$; for $k \ge 3$ it is at least $\tfrac12 \cdot \tfrac78 + \tfrac12 (1 - \tfrac1e) > 0.753$. So every clause gets at least $\tfrac34 z_j^*$, and the expected value is at least $\tfrac34 Z^* \ge \tfrac34 \mathrm{OPT}$. Both parts can be derandomized. Yannakakis (1994) found the first $3/4$ algorithm, by a different method based on network flows. Goemans and Williamson also gave a single rounding with a non-linear function that reaches $3/4$ directly.

**Better ratios.** [Semidefinite programming](/semidefinite-programming/) gives $0.878$ for MAX-2-SAT (Goemans and Williamson 1995, see [MAX-2-SAT](/max-2-sat/)), $7/8$ for MAX-3-SAT (Karloff and Zwick 1997, with the analysis completed later by computer), and ratios near $0.8$ for general MAX-SAT.

**Exact algorithms.** Brute force takes $O(2^n m k)$ time. Branch and bound with lower bounds from unit propagation and inconsistent subsets was the first practical exact approach. Today, SAT-based methods dominate on structured formulas: [core-guided](/core-guided-maxsat/) algorithms, linear search that lowers an upper bound with [cardinality encodings](/totalizer-encoding/), and implicit [hitting set](/hitting-set/) methods. For large random or hard formulas where an optimal answer is not needed, local search such as [WalkSAT](/walksat/) with weights finds good assignments.

## Bounds

- **NP-hardness.** MAX-2-SAT is NP-complete (Garey, Johnson and Stockmeyer 1976), so MAX-SAT is too.
- **APX-completeness.** MAX-SAT and MAX-3-SAT are complete for [APX](/apx/) under approximation-preserving reductions; this follows from the [PCP theorem](/pcp-theorem/).
- **7/8 is tight for MAX-E3-SAT.** For every $\varepsilon > 0$, approximating MAX-E3-SAT within $7/8 + \varepsilon$ is NP-hard (Håstad 2001); see [MAX-3SAT inapproximability](/max-3sat-inapproximability/). So the random assignment is optimal for this case.
- **Integrality gap.** The LP above has gap $4/3$, by the four-clause example, so the best-of-two analysis is tight against the LP.
- **Lower bound on OPT.** $\mathrm{OPT} \ge m/2$ for every formula without empty clauses, by the complement argument. Asking whether $\mathrm{OPT} \ge m/2 + t$ is fixed-parameter tractable in $t$ (Mahajan and Raman 1999).

## Reductions

- **From 3-SAT to MAX-2-SAT.** Use the ten-clause gadget for each clause. A 3-CNF formula with $m$ clauses is satisfiable if and only if the 2-CNF formula of $10m$ clauses has an assignment satisfying $7m$ clauses.
- **From [MAX-CUT](/maximum-cut/) to MAX-2-SAT.** For each edge $uv$, add $(x_u \vee x_v)$ and $(\neg x_u \vee \neg x_v)$. A cut edge satisfies both, an uncut edge one, so $\mathrm{sat}(x) = |E| + \mathrm{cut}(x)$.
- **To weighted and partial versions.** MAX-SAT is the case of [weighted MaxSAT](/weighted-max-sat/) with all weights 1, and of [partial MaxSAT](/partial-max-sat/) with no hard clauses.
- **To integer programming.** The LP above with $y_i, z_j \in \{0, 1\}$ is an exact [binary integer program](/binary-integer-programming/).

## Applications

MaxSAT solvers are used for scheduling and timetabling with soft preferences, for software package upgrades that should change as little as possible, for fault localization and design debugging (find the fewest components whose failure explains the observations), for haplotype inference and other problems in bioinformatics, and for finding the most probable explanation in probabilistic models. MAX-SAT and MAX-2-SAT are also central in the theory of approximation and of hardness of approximation.

## References
