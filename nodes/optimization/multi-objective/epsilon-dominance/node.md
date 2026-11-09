---
tag: 0FA8Z2
kind: definition
slug: epsilon-dominance
name: Epsilon-dominance
aliases:
- epsilon-Pareto dominance
- additive epsilon dominance
- multiplicative epsilon dominance
- epsilon-domination
area: optimization/multi-objective
level: advanced
summary: A relaxed dominance in which a point may be worse than another by at most epsilon in each objective, by an additive amount or by a factor 1 + epsilon. It defines epsilon-Pareto sets.
prereqs: [pareto-dominance, pareto-optimality]
see_also: [approximate-pareto-set, epsilon-indicator, pareto-front, multi-objective-evolutionary-algorithm, epsilon-constraint-method]
sources:
  - paper: doi:10.1162/106365602760234108
    title: Marco Laumanns, Lothar Thiele, Kalyanmoy Deb and Eckart Zitzler, Combining convergence and diversity in evolutionary multiobjective optimization, Evolutionary Computation 10(3), 2002, 263-282
    locator: the definitions of epsilon-dominance and of epsilon-approximate Pareto sets, and the box-based archives
  - paper: doi:10.1109/SFCS.2000.892068
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of Web sources, Proceedings of the 41st IEEE FOCS, 2000, 86-92
    locator: the definition of the epsilon-approximate Pareto curve with a factor 1 + epsilon
  - paper: doi:10.1109/TEVC.2003.810758
    title: Eckart Zitzler, Lothar Thiele, Marco Laumanns, Carlos M. Fonseca and Viviane Grunert da Fonseca, Performance assessment of multiobjective optimizers, an analysis and review, IEEE Transactions on Evolutionary Computation 7(2), 2003, 117-132
    locator: the additive and multiplicative epsilon-dominance and the binary epsilon indicator
  - paper: "Kalyanmoy Deb, Manikanth Mohan and Shikhar Mishra, Evaluating the epsilon-domination based multi-objective evolutionary algorithm for a quick computation of Pareto-optimal solutions, Evolutionary Computation 13(4), 2005, 501-525"
    locator: the epsilon-MOEA, a steady-state algorithm with a box archive
---

Epsilon-dominance relaxes [Pareto dominance](/pareto-dominance/): a point $a$ epsilon-dominates a point $b$ when $a$ is worse than $b$ by at most $\varepsilon$ in each objective, either by an additive amount or by a factor $1 + \varepsilon$. A set that epsilon-dominates every feasible point is an [approximate Pareto set](/approximate-pareto-set/), and such sets can be small even when the [Pareto front](/pareto-front/) is huge. The relation drives the box archives of Laumanns, Thiele, Deb and Zitzler, and it is the base of the [epsilon indicator](/epsilon-indicator/).

## Definition

**Convention.** All objectives are minimized, $p$ is the number of objectives, and $y = f(x) \in \mathbb{R}^p$ is the image of a solution $x$. For vectors, $a \le b$ means $a_i \le b_i$ for each $i$.

Let $a, b \in \mathbb{R}^p$ and $\varepsilon \ge 0$.

- **Additive.** $a$ additively $\varepsilon$-dominates $b$, written $a \preceq_{\varepsilon+} b$, when
$$a_i - \varepsilon \le b_i \quad \text{for each } i = 1, \ldots, p.$$
- **Multiplicative.** For $a, b \in \mathbb{R}^p_{>0}$, $a$ multiplicatively $\varepsilon$-dominates $b$, written $a \preceq_{\varepsilon} b$, when
$$a_i \le (1 + \varepsilon)\, b_i \quad \text{for each } i = 1, \ldots, p.$$

A vector $\varepsilon = (\varepsilon_1, \ldots, \varepsilon_p)$ of different values per objective is also common; replace $\varepsilon$ by $\varepsilon_i$ in objective $i$. For maximization, the inequalities turn around: $a_i + \varepsilon \ge b_i$, or $(1 + \varepsilon) a_i \ge b_i$, which is the form of Laumanns et al. A solution $x$ $\varepsilon$-dominates $x'$ when $f(x)$ $\varepsilon$-dominates $f(x')$.

**Epsilon-Pareto set.** Given a set $Y \subseteq \mathbb{R}^p$, a set $A \subseteq Y$ is an $\varepsilon$-Pareto set (an $\varepsilon$-approximate Pareto set) of $Y$ when each $y \in Y$ is $\varepsilon$-dominated by some $a \in A$. Some authors also ask that $A$ hold only Pareto-optimal points of $Y$.

**Basic facts.** Let $\varepsilon, \delta \ge 0$.

1. With $\varepsilon = 0$, both relations are weak Pareto dominance: $a \le b$. The relation is reflexive for each $\varepsilon \ge 0$.
2. *Monotone in $\varepsilon$.* If $a \preceq_{\varepsilon+} b$ and $\varepsilon \le \delta$, then $a \preceq_{\delta+} b$.
3. *Chaining.* If $a \preceq_{\varepsilon+} b$ and $b \preceq_{\delta+} c$, then $a \preceq_{(\varepsilon + \delta)+} c$, because $a_i - \varepsilon - \delta \le b_i - \delta \le c_i$. In the multiplicative form, $a \preceq_{\varepsilon} b$ and $b \preceq_{\delta} c$ give $a_i \le (1 + \varepsilon)(1 + \delta) c_i$, so the factor is $(1 + \varepsilon)(1 + \delta)$. So for $\varepsilon > 0$ the relation is not transitive, but the error grows only by addition (or by multiplication of the factors).
4. *Mixed chaining.* If $a \le b$ and $b \preceq_{\varepsilon+} c$, then $a \preceq_{\varepsilon+} c$. The same holds with $a \preceq_{\varepsilon+} b$ and $b \le c$. So a point that weakly dominates an approximating point is also approximating.
5. *Logarithms.* For positive vectors, $a \preceq_{\varepsilon} b$ holds exactly when $\log a \preceq_{\log(1+\varepsilon)+} \log b$, with the logarithm taken in each coordinate. So results for one form carry over to the other.
6. *Not antisymmetric.* Two different points can $\varepsilon$-dominate each other, as the first example below shows. So $\varepsilon$-dominance is not a partial order for $\varepsilon > 0$.

## Examples and non-examples

- **Additive, both ways.** Let $a = (3, 5)$, $b = (4, 4)$ and $\varepsilon = 1$. Then $a_1 - 1 = 2 \le 4$ and $a_2 - 1 = 4 \le 4$, so $a \preceq_{1+} b$. Also $b_1 - 1 = 3 \le 3$ and $b_2 - 1 = 3 \le 5$, so $b \preceq_{1+} a$. Neither point Pareto-dominates the other.
- **Not transitive.** Let $a = (0, 2)$, $b = (1, 1)$, $c = (2, 0)$ and $\varepsilon = 1$. Then $a \preceq_{1+} b$ and $b \preceq_{1+} c$, but $a_2 - 1 = 1 > 0 = c_2$, so $a$ does not $1$-dominate $c$. It does $2$-dominate $c$, as fact 3 gives.
- **Multiplicative.** Let $a = (10, 20)$, $b = (12, 19)$ and $\varepsilon = 0.1$. Then $10 \le 1.1 \cdot 12 = 13.2$ and $20 \le 1.1 \cdot 19 = 20.9$, so $a \preceq_{0.1} b$. With $\varepsilon = 0.05$, $1.05 \cdot 19 = 19.95 < 20$, so the relation fails.
- **An $\varepsilon$-Pareto set.** The eleven points $(t, 10 - t)$, $t = 0, \ldots, 10$, all lie on the Pareto front of the set. With $\varepsilon = 2$, a point $a$ of this line covers $y$ exactly when $\lvert a_1 - y_1 \rvert \le 2$, so it covers at most five points. The three points $(2, 8)$, $(7, 3)$, $(10, 0)$ form a $2$-Pareto set, and no two points do.
- **Non-example: values that are not positive.** The multiplicative form needs $b > 0$. With $b = (0, 5)$, the test $a_1 \le (1 + \varepsilon) \cdot 0$ needs $a_1 \le 0$ for every $\varepsilon$, so no relaxation happens in that objective. With $b_1 < 0$, a larger $\varepsilon$ makes the test harder. Shift the objectives to a positive range first, and say which shift you use, because the result depends on it.
- **Non-example: Pareto dominance is not implied.** $a \preceq_{\varepsilon+} b$ says nothing about which point is better. In the first example, $a$ and $b$ cover each other, and each has a better value in one objective.

## Related definitions

- **[Pareto dominance](/pareto-dominance/)** and **[Pareto optimality](/pareto-optimality/).** The case $\varepsilon = 0$ gives weak dominance; strict dominance asks for one strict inequality.
- **[Approximate Pareto set](/approximate-pareto-set/).** The problem of finding a small $\varepsilon$-Pareto set. Papadimitriou and Yannakakis (2000) showed that one of polynomial size exists for many combinatorial problems.
- **Box dominance.** Laumanns et al. map each point to a box with index $b(y)_i = \lfloor (y_i - \ell_i) / \varepsilon \rfloor$ (additive) or $\lfloor \log(y_i / \ell_i) / \log(1 + \varepsilon) \rfloor$ (multiplicative) and compare the boxes by Pareto dominance. A point whose box weakly dominates the box of $y$ $\varepsilon$-dominates $y$ in the strict sense $a_i < y_i + \varepsilon$. The archive built on this rule is on the [approximate Pareto set](/approximate-pareto-set/) page; the epsilon-MOEA of Deb, Mohan and Mishra (2005) uses it.
- **[Epsilon indicator](/epsilon-indicator/).** The smallest $\varepsilon$ such that a set $\varepsilon$-dominates another set, used to compare the outputs of two optimizers.
- **[Epsilon-constraint method](/epsilon-constraint-method/).** A different idea with a similar name: it bounds all but one objective by constants $\varepsilon_i$ and minimizes the last one.

## References
