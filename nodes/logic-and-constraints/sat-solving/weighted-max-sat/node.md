---
tag: A2N4D5
kind: problem
slug: weighted-max-sat
name: Weighted MaxSAT
aliases:
- weighted maximum satisfiability
area: logic-and-constraints/sat-solving
level: core
summary: MaxSAT in which each clause has a positive weight. Find an assignment of largest total weight of true clauses, or equivalently of least total weight of false clauses.
prereqs: [max-sat, sat, conjunctive-normal-form]
see_also: [max-sat, partial-max-sat, max-2-sat, core-guided-maxsat, hitting-set, binary-integer-programming, randomized-rounding, walksat]
sources:
  - paper: doi:10.1137/S0895480192243516
    title: "Michel X. Goemans and David P. Williamson, New 3/4-approximation algorithms for the maximum satisfiability problem, SIAM Journal on Discrete Mathematics 7 (1994), 656 to 666"
    locator: the 3/4 approximation, stated for weighted clauses
  - paper: doi:10.1016/j.artint.2013.01.002
    title: "Carlos Ansótegui, María Luisa Bonet and Jordi Levy, SAT-based MaxSAT algorithms, Artificial Intelligence 196 (2013), 77 to 105"
    locator: WPM1 and the clause-splitting rule for weights
  - paper: "Jessica Davies and Fahiem Bacchus, Solving MAXSAT by solving a sequence of simpler SAT instances, Principles and Practice of Constraint Programming (CP 2011), LNCS 6876, 225 to 239"
    locator: the implicit hitting set method
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms (2011)
    locator: Chapter 5, Sections 5.1 to 5.5, which treat weighted MAX-SAT
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapters on MaxSAT, weighted algorithms and stratification
  - url: "https://maxsat-evaluations.github.io/"
    locator: the MaxSAT Evaluations, with weighted tracks, benchmarks and solver descriptions
---

Weighted MaxSAT is the version of [maximum satisfiability](/max-sat/) in which each clause $C_j$ has a positive weight $w_j$. The goal is an assignment that maximizes the total weight of the true clauses, or, with the same optimal solutions, minimizes the total weight of the false clauses, called the *cost*. With all weights 1 it is plain MAX-SAT. With very large weights on some clauses it expresses [partial MaxSAT](/partial-max-sat/), where those clauses must hold. The approximation algorithms for MAX-SAT, such as the $3/4$ algorithm of Goemans and Williamson, work with weights unchanged. Exact solvers need extra ideas, such as splitting clauses by weight in core-guided search, or stratification by weight.

## In plain words

You have yes-or-no choices and a list of wishes, but now some wishes matter more than others. Each wish has a price, the amount you lose if it is not met. The task is to make the choices so that the total price of the unmet wishes is as small as possible.

Counting wishes is the special case where every price is 1. Prices let you say "this wish matters ten times more than that one", and a very high price says "this wish must be met". The problem is hard in general, but the same coin-flip and rounding tricks as for plain MaxSAT still give good answers, and solvers can find the best answer for many real problems.

## Definition

The input is a CNF formula $C_1 \wedge \cdots \wedge C_m$ over $x_1, \ldots, x_n$ and weights $w_1, \ldots, w_m > 0$, usually integers. For an assignment $x$,

$$W(x) = \sum_{j \,:\, x \text{ satisfies } C_j} w_j, \qquad \mathrm{cost}(x) = \sum_{j \,:\, x \text{ falsifies } C_j} w_j = \sum_j w_j - W(x).$$

The output is an $x$ that maximizes $W(x)$, which is an $x$ that minimizes $\mathrm{cost}(x)$. The decision version asks whether some $x$ has $\mathrm{cost}(x) \le t$.

## Variants

- **Unit weights.** This is [MAX-SAT](/max-sat/).
- **Weighted partial MaxSAT.** Some clauses are hard, with infinite weight; see [partial MaxSAT](/partial-max-sat/).
- **Weighted MAX-$k$-SAT.** Clauses of at most $k$ literals, such as weighted [MAX-2-SAT](/max-2-sat/).
- **Lexicographic and multi-objective MaxSAT.** Several weight functions ordered by priority, or a Pareto front.
- **Soft unit clauses only.** Every formula can be put in this form: add a fresh variable $b_j$ to each soft clause, make $C_j \vee b_j$ hard, and make $(\neg b_j)$ soft with weight $w_j$. Many solvers use this form internally.

## Examples

Take five clauses with weights:

| clause | $(x_1)$ | $(x_2)$ | $(\neg x_1 \vee \neg x_2)$ | $(\neg x_1 \vee x_3)$ | $(\neg x_3)$ |
|---|---|---|---|---|---|
| weight | 3 | 2 | 4 | 1 | 2 |

The total weight is 12. Setting both $x_1$ and $x_2$ true loses the clause of weight 4, so at most one of them is true. With $x = 100$, the true clauses are $(x_1)$, $(\neg x_1 \vee \neg x_2)$ and $(\neg x_3)$, weight $3 + 4 + 2 = 9$, and only $(x_2)$ and $(\neg x_1 \vee x_3)$ are false, cost 3. With $x = 010$, the true clauses are $(x_2)$, $(\neg x_1 \vee \neg x_2)$, $(\neg x_1 \vee x_3)$ and $(\neg x_3)$, weight $2 + 4 + 1 + 2 = 9$. A brute-force check over all 8 assignments confirms that 9 is the optimum and that $100$ and $010$ are the only optimal assignments. Unweighted, $010$ would be strictly better, with 4 true clauses against 3: the weights change the answer.

## Known algorithms

- **Approximation.** A random assignment gives each clause of size $k$ probability $1 - 2^{-k} \ge 1/2$ of being true, so the expected weight is at least half of the total. LP rounding and the best of the two give $3/4$ (Goemans and Williamson 1994); the proofs in [MAX-SAT](/max-sat/) work clause by clause, so the weights only multiply each term. Semidefinite methods give about $0.878$ and better for weighted [MAX-2-SAT](/max-2-sat/).
- **Reduction to unit weights.** With integer weights, replace each clause by $w_j$ copies. This is correct but only pseudo-polynomial, since the size grows with the weights.
- **Core-guided search with weights.** In WPM1 (Ansótegui, Bonet and Levy), each core $K$ found by the SAT solver has a least weight $w_{\min}$. Each clause of $K$ with a larger weight is split into a copy of weight $w_{\min}$ and a copy with the rest; the copies of weight $w_{\min}$ are relaxed as in the [Fu-Malik algorithm](/core-guided-maxsat/), and the lower bound grows by $w_{\min}$. OLL and its solver RC2 handle weights in a similar way.
- **Stratification.** Solve first with only the clauses of the largest weights, then add the next level. This finds good solutions early and avoids many small cores.
- **Implicit hitting sets.** Find cores with a SAT solver and a minimum-cost [hitting set](/hitting-set/) of all cores so far with an [integer programming](/binary-integer-programming/) solver; stop when the hitting set leaves a satisfiable formula (Davies and Bacchus 2011). This works well when there are many distinct weights.
- **Linear search.** Find any model, then add a pseudo-Boolean constraint "cost less than the current cost" and repeat until unsatisfiable.
- **Branch and bound.** Search over assignments with lower bounds from disjoint inconsistent subsets of clauses.
- **Local search.** Weighted versions of [WalkSAT](/walksat/) and newer solvers with dynamic clause weights give good solutions quickly on large instances, without a proof of optimality.

## Bounds

- **NP-hard**, since unit weights give MAX-SAT, and MAX-2-SAT is NP-hard.
- **Approximation.** $3/4$ in polynomial time; $7/8 + \varepsilon$ is NP-hard already for weighted, and even unweighted, MAX-E3-SAT (Håstad 2001).
- **Weights do not change the approximation ratios.** The approximation results for MAX-SAT are usually stated and proved for weights.
- **Exact time.** $O(2^n m k)$ by brute force; the exact exponential algorithms for MAX-SAT extend to weights.

## Reductions

- **Partial MaxSAT to weighted MaxSAT.** Give every hard clause the weight $1 + \sum_{\text{soft}} w_j$. Then an optimal assignment satisfies all hard clauses whenever some assignment does, since breaking a hard clause costs more than breaking all soft clauses.
- **Weighted MaxSAT to integer programming.** Variables $y_i, z_j \in \{0, 1\}$, constraint $\sum_{P_j} y_i + \sum_{N_j} (1 - y_i) \ge z_j$, maximize $\sum w_j z_j$.
- **Most probable explanation.** In a Markov network with positive factors, the logarithms of factor values become clause weights, and the most probable assignment is a weighted MaxSAT optimum. Markov logic networks use this.

## Applications

Weighted MaxSAT models problems with preferences of different strength: timetabling where some requests matter more, software upgrades that prefer some packages, cost-minimal debugging and diagnosis, set cover and other covering problems written as clauses, and probabilistic inference in Markov networks. The MaxSAT Evaluations have weighted tracks with instances from these areas.

## References
