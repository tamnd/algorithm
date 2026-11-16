---
title: Correctness of QPBO
proves: [correctness]
status: full
---

Let $E(x) = \sum_p \theta_p(x_p) + \sum_{(p,q)} \theta_{pq}(x_p, x_q)$ for $x \in \{0,1\}^n$, with arbitrary real pair terms. Call a pair term submodular if $\theta_{pq}(0,0) + \theta_{pq}(1,1) \le \theta_{pq}(0,1) + \theta_{pq}(1,0)$. Lines L1 to L5 build the energy $\tilde E$ of $2n$ binary variables $y = (x, \bar x)$:

$$\tilde E(x, \bar x) = \tfrac12 \sum_p \big[\theta_p(x_p) + \theta_p(1 - \bar x_p)\big] + \tfrac12 \sum_{\text{subm.}} \big[\theta_{pq}(x_p, x_q) + \theta_{pq}(1 - \bar x_p, 1 - \bar x_q)\big] + \tfrac12 \sum_{\text{non-subm.}} \big[\theta_{pq}(x_p, 1 - \bar x_q) + \theta_{pq}(1 - \bar x_p, x_q)\big].$$

We prove: (1) $\tilde E$ is regular, so line L6 finds a minimizer $(x^*, \bar x^*)$ by one cut; (2) $\tilde E(x, 1 - x) = E(x)$, so $\min \tilde E \le \min E$; (3) persistency: if $z$ minimizes $E$, then the labeling $z'$ with $z'_p = x^*_p$ for every labeled $p$ (those with $\bar x^*_p = 1 - x^*_p$) and $z'_p = z_p$ otherwise also minimizes $E$.

## 1. $\tilde E$ is regular

Each term of $\tilde E$ depends on at most two variables. For a term $g(u, v)$ write $\Delta g = g(0,0) + g(1,1) - g(0,1) - g(1,0)$; the term is regular when $\Delta g \le 0$. Let $A, B, C, D$ be the values of $\theta_{pq}$ at $(0,0), (0,1), (1,0), (1,1)$, so $\Delta \theta_{pq} = A + D - B - C$.

- $\theta_{pq}(x_p, x_q)$ has $\Delta = A + D - B - C$.
- $\theta_{pq}(1 - \bar x_p, 1 - \bar x_q)$, as a function of $(\bar x_p, \bar x_q)$, takes the values $D, C, B, A$, so $\Delta = D + A - C - B$.
- $\theta_{pq}(x_p, 1 - \bar x_q)$, as a function of $(x_p, \bar x_q)$, takes the values $B, A, D, C$, so $\Delta = B + C - A - D$.
- $\theta_{pq}(1 - \bar x_p, x_q)$, as a function of $(\bar x_p, x_q)$, takes the values $C, D, A, B$, so $\Delta = C + B - A - D$.

Line L4 uses the first two when $A + D \le B + C$, and line L5 the last two when $A + D > B + C$. In both cases $\Delta \le 0$. So $\tilde E$ is in the class $\mathcal{F}^2$ and regular, and by the [Kolmogorov-Zabih theorem](/graph-representable-energies/) the graph of the code, with $2n + 2$ nodes, represents $2\tilde E$; a minimum cut gives a minimizer. The code doubles every value to stay in integers.

## 2. The diagonal and the lower bound

Put $\bar x = 1 - x$. Then $1 - \bar x_p = x_p$ for every $p$, and every bracket becomes twice the matching term of $E$. So $\tilde E(x, 1 - x) = E(x)$, and $\min \tilde E \le \min_x \tilde E(x, 1 - x) = \min E$. Line L8 returns $\tilde E(x^*, \bar x^*) = \min \tilde E$, which is therefore a lower bound on $\min E$.

## 3. Persistency

**Symmetry.** Let $\sigma(x, \bar x) = (1 - \bar x, 1 - x)$. Each bracket of $\tilde E$ is mapped onto itself by $\sigma$: the unary bracket becomes $\theta_p(1 - \bar x_p) + \theta_p(x_p)$; the submodular bracket becomes $\theta_{pq}(1 - \bar x_p, 1 - \bar x_q) + \theta_{pq}(x_p, x_q)$; the other bracket becomes $\theta_{pq}(1 - \bar x_p, x_q) + \theta_{pq}(x_p, 1 - \bar x_q)$. So $\tilde E(\sigma(y)) = \tilde E(y)$.

**Submodularity.** For $y, y' \in \{0,1\}^{2n}$ let $y \wedge y'$ and $y \vee y'$ be the componentwise minimum and maximum. A function of two binary variables with $\Delta \le 0$ satisfies $g(a \wedge a') + g(a \vee a') \le g(a) + g(a')$: if $a \le a'$ or $a' \le a$ both sides are equal, and otherwise $\{a, a'\} = \{(0,1), (1,0)\}$ and the inequality is $\Delta g \le 0$. Summing over the terms, $\tilde E(y \wedge y') + \tilde E(y \vee y') \le \tilde E(y) + \tilde E(y')$.

Let $a = (x^*, \bar x^*)$ be the minimizer of line L6, and let $m = \tilde E(a)$.

*Step 1.* Let $a' = a \vee \sigma(a)$. By submodularity and symmetry, $\tilde E(a') + \tilde E(a \wedge \sigma(a)) \le 2m$, and both terms are at least $m$, so $\tilde E(a') = m$. In coordinates, $a'$ has $x'_p = \max(x^*_p, 1 - \bar x^*_p)$ and $\bar x'_p = \max(\bar x^*_p, 1 - x^*_p)$. For a labeled $p$ this is $(x^*_p, 1 - x^*_p)$, unchanged. For an unlabeled $p$, $(x^*_p, \bar x^*_p)$ is $(0,0)$ or $(1,1)$, and both give $(1, 1)$.

*Step 2.* Let $z$ minimize $E$ and $b = (z, 1 - z)$, so $\tilde E(b) = E(z)$. Let $d = b \wedge a'$. Since $\tilde E(b \vee a') \ge m = \tilde E(a')$, submodularity gives $\tilde E(d) \le \tilde E(b)$.

*Step 3.* Let $c = d \vee \sigma(a')$. Since $\tilde E(d \wedge \sigma(a')) \ge m = \tilde E(\sigma(a'))$, submodularity gives $\tilde E(c) \le \tilde E(d) \le \tilde E(b)$.

*Coordinates of $c$.* $\sigma(a')$ is $(x^*_p, 1 - x^*_p)$ at a labeled $p$ and $(0, 0)$ at an unlabeled $p$. At a labeled $p$, $d$ is $(\min(z_p, x^*_p), \min(1 - z_p, 1 - x^*_p))$, and $c$ is $(\max(\min(z_p, x^*_p), x^*_p), \max(\min(1 - z_p, 1 - x^*_p), 1 - x^*_p)) = (x^*_p, 1 - x^*_p)$. At an unlabeled $p$, $d$ is $(z_p, 1 - z_p)$ because $a'$ is $(1,1)$ there, and $c$ is the same. So $c = (z', 1 - z')$.

Hence $E(z') = \tilde E(c) \le \tilde E(b) = E(z) = \min E$, and $z'$ is a minimizer of $E$. $\square$

## Consequences

- If every pair term is submodular, then $\tilde E(x, \bar x) = \tfrac12 [E(x) + E(1 - \bar x)]$. A minimizer has $x$ and $1 - \bar x$ both minimizing $E$. If the minimizer of $E$ is unique, then $\bar x^* = 1 - x^*$ and every variable is labeled with the optimum.
- If every variable is labeled, $x^*$ itself is a minimizer of $E$, by persistency with any $z$.
- The proof used only that $a$ is some minimizer of $\tilde E$. Different minimum cuts can label different sets; each set is persistent.
