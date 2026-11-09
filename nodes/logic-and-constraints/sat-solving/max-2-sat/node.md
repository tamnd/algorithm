---
tag: CFW0ZM
kind: problem
slug: max-2-sat
name: MAX-2-SAT
aliases:
- maximum 2-satisfiability
area: logic-and-constraints/sat-solving
level: core
summary: Satisfy as many 2-literal clauses as possible. NP-hard, unlike 2-SAT. Semidefinite rounding gives 0.878 (Goemans and Williamson), later about 0.940; above 21/22 is NP-hard.
prereqs: [max-sat, 2-sat, np-hard]
see_also: [max-sat, 2-sat, maximum-cut, weighted-max-sat, semidefinite-programming, max-cut-ugc-hardness, unique-games-conjecture, core-guided-maxsat]
sources:
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: "Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1 (1976), 237 to 267"
    locator: the NP-completeness of MAX-2-SAT, by the ten-clause gadget
  - paper: doi:10.1145/227683.227684
    title: "Michel X. Goemans and David P. Williamson, Improved approximation algorithms for maximum cut and satisfiability problems using semidefinite programming, Journal of the ACM 42 (1995), 1115 to 1145"
    locator: the 0.878 approximation for MAX-2-SAT and MAX-CUT by random hyperplane rounding
  - paper: "Michael Lewin, Dror Livnat and Uri Zwick, Improved rounding techniques for the MAX 2-SAT and MAX DI-CUT problems, Integer Programming and Combinatorial Optimization (IPCO 2002), LNCS 2337, 67 to 82"
    locator: the ratio of about 0.940
  - paper: doi:10.1145/502090.502098
    title: "Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48 (2001), 798 to 859"
    locator: the NP-hardness of approximating MAX-2-SAT within 21/22 + epsilon
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348 (2005), 357 to 365"
    locator: the exact algorithm in O*(2^(omega n / 3)) time by matrix multiplication
  - paper: "Per Austrin, Balanced Max 2-Sat might not be the hardest, Proceedings of the 39th ACM Symposium on Theory of Computing (STOC 2007), 189 to 197"
    locator: the optimality of the Lewin-Livnat-Zwick ratio under the Unique Games Conjecture
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms (2011)
    locator: Chapter 6, Section 6.2 (MAX-2-SAT by semidefinite programming)
---

MAX-2-SAT is [maximum satisfiability](/max-sat/) restricted to clauses with at most two literals: given a 2-CNF formula, find an assignment that makes as many clauses true as possible. Deciding whether all clauses can be true is [2-SAT](/2-sat/), which takes linear time, but maximizing is [NP-hard](/np-hard/) (Garey, Johnson and Stockmeyer 1976). MAX-2-SAT is a classic problem of approximation: [semidefinite programming](/semidefinite-programming/) with random hyperplane rounding gives a ratio of about $0.878$ (Goemans and Williamson 1995), refined to about $0.940$ (Lewin, Livnat and Zwick 2002), while a ratio above $21/22 \approx 0.955$ is NP-hard (Håstad 2001). It contains [MAX-CUT](/maximum-cut/) as a special case.

## In plain words

You have yes-or-no choices and a list of wishes, and each wish names at most two choices: "Ann works on Monday, or Bob does not". If all wishes can be met together, a fast method finds out how. But usually some wishes clash, and then the question is how many can be met at most.

This question is hard, even though each wish is small. No fast method is known that always finds the best answer, and none is expected. Good approximate methods exist: one turns each choice into an arrow in space, finds arrows that please the wishes as much as possible, and cuts space with a random plane to turn the arrows back into yes and no. This meets at least 87.8 percent of the best possible number of wishes on average.

## Definition

The input is a CNF formula $F$ over $x_1, \ldots, x_n$ whose $m$ clauses each have one or two literals. The output is an assignment $x$ that maximizes the number $\mathrm{sat}(x)$ of true clauses. The decision version asks, for a number $t$, whether some $x$ has $\mathrm{sat}(x) \ge t$; it is NP-complete. The weighted version gives each clause a positive weight.

## Variants

- **MAX-E2-SAT.** Every clause has exactly two distinct variables.
- **Weighted MAX-2-SAT.** Maximize the total weight of true clauses; the approximation results below hold for weights.
- **Balanced MAX-2-SAT.** Each variable appears positively and negatively equally often in total weight; Austrin studied it as a candidate hardest case.
- **MIN-2-UNSAT, or Almost 2-SAT.** Delete as few clauses as possible to make the rest satisfiable. It has the same optimal solutions, but it is fixed-parameter tractable in the number of deleted clauses (Razgon and O'Sullivan 2009) and has different approximation behavior.
- **MAX-2-CSP.** Arbitrary constraints on two Boolean variables, which include MAX-CUT and MAX-DI-CUT.

## Examples

**A triangle as MAX-CUT.** Take the triangle on vertices 1, 2, 3, and for each edge $uv$ the two clauses $(x_u \vee x_v)$ and $(\neg x_u \vee \neg x_v)$:

$$(x_1 \vee x_2) (\neg x_1 \vee \neg x_2) (x_2 \vee x_3) (\neg x_2 \vee \neg x_3) (x_1 \vee x_3) (\neg x_1 \vee \neg x_3).$$

An edge whose ends get different values satisfies both of its clauses, and an edge with equal ends satisfies one. A triangle has a cut of at most 2 edges, so $\mathrm{OPT} = 3 + 2 = 5$, reached by $001$, $010$ and the other assignments that are not all equal. A brute-force check over the 8 assignments confirms this.

**Four clauses.** $(x_1 \vee x_2)(x_1 \vee \neg x_2)(\neg x_1 \vee x_2)(\neg x_1 \vee \neg x_2)$: every assignment satisfies exactly 3, so $\mathrm{OPT} = 3$ of 4. This formula is unsatisfiable, so 2-SAT answers "no", and MAX-2-SAT answers 3.

## Known algorithms

**Exact.** Brute force takes $O(2^n m)$ time. Williams (2005) gave an algorithm in $O^*(2^{\omega n/3})$ time, about $O(1.73^n)$ with the current [matrix multiplication exponent](/matrix-multiplication-exponent/) $\omega$: split the variables into three groups, build a graph whose vertices are the partial assignments of each group, and count weighted triangles by fast matrix multiplication. It is the only known algorithm for MAX-2-SAT that is exponentially faster than $2^n$ in the number of variables. Other exact algorithms are fast in terms of the number of clauses. In practice, MAX-2-SAT instances are solved with general [MaxSAT](/max-sat/) solvers, such as [core-guided](/core-guided-maxsat/) ones.

**The 3/4 algorithms.** The general MAX-SAT methods apply. A random assignment satisfies each 2-clause with probability $3/4$, and each unit clause with probability $1/2$; LP rounding and the best of two give $3/4$.

**Semidefinite programming, ratio 0.878.** Goemans and Williamson add a unit vector $v_0$ for "true" and a unit vector $v_i$ for each variable, with $x_i$ true when $v_i = v_0$. For literals, use $v_{\neg i} = -v_i$. A clause $(\ell_1 \vee \ell_2)$ is true unless both literals are false, so its value can be written as

$$\tfrac14\big[(1 + v_0 \cdot v_{\ell_1}) + (1 + v_0 \cdot v_{\ell_2}) + (1 - v_{\ell_1} \cdot v_{\ell_2})\big],$$

which is 1 or 0 when the vectors are $\pm v_0$. Maximize the sum over the clauses with arbitrary unit vectors in $\mathbb{R}^{n+1}$, which is a semidefinite program solvable to any precision in polynomial time, and its optimum is at least $\mathrm{OPT}$. Then pick a random hyperplane through the origin, and set $x_i$ true when $v_i$ is on the same side as $v_0$. Two unit vectors at angle $\theta$ are separated with probability $\theta/\pi$. Each term $(1 - v \cdot w)/4$ becomes $1/2$ with probability $\theta/\pi$, and each term $(1 + v \cdot w)/4$ becomes $1/2$ with probability $1 - \theta/\pi$. Since

$$\frac{\theta/\pi}{(1 - \cos\theta)/2} \ge \alpha_{GW} \quad\text{and}\quad \frac{1 - \theta/\pi}{(1 + \cos\theta)/2} \ge \alpha_{GW} \quad \text{for all } \theta \in (0, \pi),$$

with $\alpha_{GW} = \min_{0 < \theta \le \pi} \frac{2\theta}{\pi(1 - \cos\theta)} \approx 0.87856$, every term gets at least $\alpha_{GW}$ of its SDP value in expectation, and the rounded assignment satisfies at least $0.878\,\mathrm{OPT}$ clauses in expectation. The second inequality is the first with $\theta$ replaced by $\pi - \theta$.

**Better rounding.** Feige and Goemans (1995) improved the ratio to about $0.931$ by adding triangle inequalities and rotating the vectors before rounding, and Lewin, Livnat and Zwick (2002) reached about $0.9401$ with a skewed hyperplane distribution.

## Bounds

- **NP-hard.** By the ten-clause gadget of Garey, Johnson and Stockmeyer: for each clause of a 3-CNF formula, the gadget has 7 satisfiable clauses if the clause is satisfied and at most 6 otherwise. So deciding $\mathrm{OPT} \ge 7m$ is NP-complete. See [MAX-SAT](/max-sat/) for the gadget.
- **Hardness of approximation.** Approximating MAX-2-SAT within $21/22 + \varepsilon \approx 0.9545$ is NP-hard for every $\varepsilon > 0$ (Håstad 2001).
- **Under the [Unique Games Conjecture](/unique-games-conjecture/).** Approximating MAX-CUT within $\alpha_{GW} + \varepsilon$ is hard (Khot, Kindler, Mossel and O'Donnell; see [MAX-CUT UGC hardness](/max-cut-ugc-hardness/)), and Austrin (2007) showed that the ratio of about $0.9401$ of Lewin, Livnat and Zwick is optimal for MAX-2-SAT. These results are conditional.
- **Exact time.** No $O^*(c^n)$ algorithm with $c < 2^{\omega/3}$ is known.

## Reductions

- **From 3-SAT.** The ten-clause gadget above, which is the classic proof of NP-hardness.
- **From MAX-CUT.** Two clauses per edge, as in the triangle example. So MAX-2-SAT is at least as hard to approximate as MAX-CUT.
- **To 2-SAT.** $\mathrm{OPT} = m$ exactly when $F$ is satisfiable, which the [2-SAT algorithm](/two-sat-algorithm/) decides in linear time. So MAX-2-SAT is easy when the optimum is all clauses, and Almost 2-SAT is easy when the optimum is close to it.
- **To quadratic optimization.** With $s_i = \pm 1$, the number of true clauses is a quadratic polynomial in the $s_i$, so MAX-2-SAT is a problem of maximizing a quadratic function over $\{\pm 1\}^n$, the same family as MAX-CUT and Ising ground states.

## Applications

MAX-2-SAT appears directly when constraints are pairwise preferences, as in some scheduling, labeling and clustering problems, and as the core of maximizing a quadratic pseudo-Boolean function. In theory, it is a test case for semidefinite rounding, for the Unique Games Conjecture, and for exact exponential algorithms, where Williams's algorithm was the first to beat $2^n$.

## References
