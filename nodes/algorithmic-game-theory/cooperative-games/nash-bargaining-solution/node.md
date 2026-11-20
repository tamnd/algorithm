---
tag: 9AB1DG
kind: definition
slug: nash-bargaining-solution
name: Nash bargaining solution
aliases:
- Nash bargaining
area: algorithmic-game-theory/cooperative-games
level: core
summary: The agreement that maximizes the product of the players' gains over the disagreement point. Four axioms characterize it.
prereqs: [pareto-optimality]
see_also: [rubinstein-bargaining-model, eisenberg-gale-program, proportional-fairness, fisher-market, nash-equilibrium, shapley-value, core-of-a-cooperative-game, subgame-perfect-equilibrium]
sources:
  - paper: "John F. Nash, The bargaining problem, Econometrica 18(2) (1950), 155-162"
    title: The bargaining problem
    locator: the two-person bargaining problem, the four axioms, and the theorem that the product of the gains is maximized by the only solution that satisfies them
  - paper: "Ehud Kalai and Meir Smorodinsky, Other solutions to Nash's bargaining problem, Econometrica 43(3) (1975), 513-518"
    title: "Other solutions to Nash's bargaining problem"
    locator: the solution that replaces independence of irrelevant alternatives by monotonicity, and the example where the Nash solution is not monotone
  - paper: doi:10.2307/2555382
    title: "Ken Binmore, Ariel Rubinstein and Asher Wolinsky, The Nash bargaining solution in economic modelling, RAND Journal of Economics 17(2) (1986), 176-188"
    locator: the Nash solution as the limit of the subgame perfect equilibria of alternating offers bargaining as the time between offers goes to 0, and the choice of the disagreement point
  - book: "Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994"
    title: A Course in Game Theory
    locator: the chapter on the axiomatic approach to bargaining, with the Nash solution and its characterization
---

The Nash bargaining solution answers a question about two parties who can agree on one of many outcomes, or fail to agree and get a fixed fallback. Nash (1950) did not model the haggling. He listed four properties that a fair and sensible agreement should have, and proved that exactly one rule has all four: choose the agreement that maximizes the product of the two players' gains over the fallback.

## Definition

A **bargaining problem** is a pair $(F, d)$, where $F \subseteq \mathbb{R}^2$ is a compact convex set of feasible utility pairs and $d \in F$ is the disagreement point, the utilities if there is no agreement. It is assumed that some $x \in F$ has $x_1 > d_1$ and $x_2 > d_2$. A **bargaining solution** $f$ assigns to each bargaining problem a point $f(F, d) \in F$.

The **Nash bargaining solution** is

$$N(F, d) = \arg\max \{ (x_1 - d_1)(x_2 - d_2) : x \in F,\ x \ge d \}.$$

The four axioms are:

1. **Pareto efficiency (PAR).** If $y \in F$ and $y \ge f(F, d)$, then $y = f(F, d)$. See [Pareto optimality](/pareto-optimality/).
2. **Symmetry (SYM).** If $d_1 = d_2$ and $(x_1, x_2) \in F$ implies $(x_2, x_1) \in F$, then $f_1(F, d) = f_2(F, d)$.
3. **Independence of irrelevant alternatives (IIA).** If $G \subseteq F$ and $f(F, d) \in G$, then $f(G, d) = f(F, d)$.
4. **Invariance to affine changes of utility (INV).** If $L(x) = (a_1 x_1 + b_1, a_2 x_2 + b_2)$ with $a_1, a_2 > 0$, then $f(L(F), L(d)) = L(f(F, d))$.

**Theorem (Nash 1950).** $N$ is well defined, and it is the only bargaining solution that satisfies PAR, SYM, IIA and INV.

*Proof.* *Well defined.* The set $\{x \in F : x \ge d\}$ is compact and the product is continuous, so a maximizer exists, and its product is positive because some point of $F$ is above $d$ in both coordinates. On the points with $x > d$, the function $\log(x_1 - d_1) + \log(x_2 - d_2)$ is strictly concave, and $F$ is convex. So the maximizer $z$ is unique, and $z > d$.

*$N$ satisfies the axioms.* If $y \ge z$, $y \ne z$ and $y \in F$, the product at $y$ is larger than at $z$, which is impossible; so PAR holds. If the problem is symmetric, the mirror image of $z$ is also a maximizer, so by uniqueness $z_1 = z_2$; so SYM holds. If $z \in G \subseteq F$, then $z$ maximizes the product over the smaller set too; so IIA holds. An affine map $L$ multiplies the product by $a_1 a_2 > 0$, so it maps the maximizer to the maximizer; so INV holds.

*Only $N$ satisfies them.* Let $f$ satisfy the four axioms, and let $z = N(F, d)$. Let $L(x) = \big( (x_1 - d_1)/(z_1 - d_1),\ (x_2 - d_2)/(z_2 - d_2) \big)$, and let $F' = L(F)$. Then $L(d) = (0, 0)$ and, by INV for $N$, $N(F', 0) = L(z) = (1, 1)$.

First, every $y \in F'$ has $y_1 + y_2 \le 2$. If not, take $y \in F'$ with $y_1 + y_2 > 2$, and for $0 < t < 1$ let $w = (1 - t)(1, 1) + t y$, which is in $F'$ by convexity. Then

$$w_1 w_2 = 1 + t (y_1 + y_2 - 2) + t^2 (y_1 - 1)(y_2 - 1),$$

which is greater than 1 for small $t > 0$, and $w > 0$ for small $t$. This contradicts the fact that $(1, 1)$ maximizes $x_1 x_2$ over $F'$ with $x \ge 0$.

Since $F'$ is bounded, there is $M > 0$ such that $F'$ lies in the triangle $G = \{x : x_1 + x_2 \le 2,\ x_1 \ge -M,\ x_2 \ge -M\}$. The set $G$ is compact, convex and symmetric, and contains $0$. By SYM, $f(G, 0)$ has equal coordinates, and by PAR it is on the line $x_1 + x_2 = 2$. So $f(G, 0) = (1, 1)$. Since $(1, 1) \in F' \subseteq G$, IIA gives $f(F', 0) = (1, 1)$. By INV for $f$, $f(F, d) = L^{-1}(1, 1) = z$. $\square$

With $n$ players the same rule maximizes $\prod_i (x_i - d_i)$, and the same axioms characterize it. The **asymmetric Nash solution** with weights $\alpha_1, \alpha_2 > 0$ maximizes $(x_1 - d_1)^{\alpha_1} (x_2 - d_2)^{\alpha_2}$ and drops symmetry.

## Examples and non-examples

- **Splitting a dollar.** With $F = \{x \ge 0 : x_1 + x_2 \le 1\}$ and $d = (0, 0)$, the product $x (1 - x)$ is largest at $x = 1/2$. Each player gets half.
- **Risk aversion.** Player 1 values money linearly and player 2 has utility $\sqrt{y}$ for $y$ dollars. If player 1 gets $x$, the product is $x \sqrt{1 - x}$. Setting the derivative to 0 gives $2 (1 - x) = x$, so $x = 2/3$. The more risk-averse player gets less money.
- **A better outside option.** With linear utilities and $d = (0.3, 0)$, the product $(x - 0.3)(1 - x)$ is largest at $x = 0.65$. Player 1 gets its fallback 0.3 plus half of the remaining 0.7.
- **Not Nash: Kalai-Smorodinsky.** The Kalai-Smorodinsky solution picks the Pareto point on the line from $d$ to the ideal point, whose coordinates are the best payoff of each player in $F$. Let $F = \{x \ge 0 : x_1 + x_2 \le 1,\ x_2 \le 1/2\}$ and $d = (0, 0)$. The ideal point is $(1, 1/2)$, so Kalai-Smorodinsky gives $(2/3, 1/3)$, while Nash gives $(1/2, 1/2)$. On the larger set $F' = \{x \ge 0 : x_1 + x_2 \le 1\}$ both give $(1/2, 1/2)$, which is also in $F$. So Kalai-Smorodinsky violates IIA. In return it satisfies a monotonicity axiom that the Nash solution fails (Kalai and Smorodinsky 1975).
- **Not Nash: the sum of utilities.** Maximizing $x_1 + x_2$ is not invariant to rescaling one player's utility. If player 2's utility is doubled, the chosen agreement can change, so the rule violates INV.
- **Not Nash: equal gains.** The egalitarian solution picks the point of $F$ with equal gains, $x_1 - d_1 = x_2 - d_2$, at which these gains are largest. It satisfies symmetry and IIA but compares utility units across players, so it violates INV.

## Related definitions

- **[Rubinstein bargaining model](/rubinstein-bargaining-model/).** A noncooperative model of alternating offers. Binmore, Rubinstein and Wolinsky (1986) showed that its [subgame perfect equilibrium](/subgame-perfect-equilibrium/) agreement converges to the Nash solution as the time between offers goes to 0, and to the asymmetric Nash solution if the players discount at different rates. This gives the axioms a strategic foundation.
- **[Eisenberg-Gale program](/eisenberg-gale-program/) and [proportional fairness](/proportional-fairness/).** Maximizing $\sum_i \log(x_i - d_i)$ is the same as maximizing the Nash product. The Eisenberg-Gale convex program for [Fisher markets](/fisher-market/) and the proportional fairness rule for network rates both maximize a weighted sum of logarithms, so their solutions are Nash bargaining solutions of a suitable problem.
- **Nash equilibrium.** A different concept by the same author, for noncooperative games. The bargaining solution is an axiomatic rule for agreements, not an equilibrium.
- **Disagreement point.** The choice of $d$ matters: in applications it can be the payoff during a strike, the value of an outside option, or the payoff if the talks break down for good, and these give different answers (Binmore, Rubinstein and Wolinsky 1986).

## References
