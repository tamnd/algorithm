---
title: Balance is a valid online b-matching rule and is (1 - (1 + 1/b)^(-b))-competitive
proves: [correctness]
status: full
---

We use the pseudocode of the page. $G = (U \cup V, E)$ is bipartite, each offline vertex has capacity $b \ge 1$, and the online vertices $v_1, \ldots, v_n$ arrive in order. A $b$-matching is a set of edges that covers each online vertex at most once and each offline vertex at most $b$ times. $M$ is the output and $\mathrm{OPT}$ is the size of a maximum $b$-matching. The proof is a primal-dual argument in the style of Buchbinder, Jain and Naor; Kalyanasundaram and Pruhs (2000) proved the same bound by a different counting argument.

**Claim 1 (validity).** $M$ is a $b$-matching, $\mathrm{load}(u)$ is the number of edges of $M$ at $u$, and each decision uses only the past.

*Proof.* Line L4 keeps only neighbours with load below $b$, and line L6 raises the load of the chosen vertex by one as line L7 adds its edge. Each online vertex is handled once. Nothing is undone. $\square$

**The LP and its dual.** The fractional $b$-matching LP and its dual are

$$\max \sum_{(u,v) \in E} x_{uv} \ \text{ s.t. } \sum_{v} x_{uv} \le b \ (u \in U), \ \sum_{u} x_{uv} \le 1 \ (v \in V), \ x \ge 0;$$

$$\min \ b \sum_{u \in U} \alpha_u + \sum_{v \in V} \beta_v \ \text{ s.t. } \ \alpha_u + \beta_v \ge 1 \ ((u,v) \in E), \ \alpha, \beta \ge 0.$$

By [weak duality](/weak-duality/), every feasible dual has value at least the LP optimum, which is at least $\mathrm{OPT}$.

**The dual built by the algorithm.** Let $r = 1 + 1/b$ and

$$A(\ell) = \frac{r^\ell - 1}{r^b - 1}, \qquad \ell = 0, 1, \ldots, b.$$

So $A(0) = 0$, $A(b) = 1$, and $A$ is increasing. Set $\alpha_u = A(\mathrm{load}(u))$ at all times. When $v_t$ is assigned to $u$ whose load was $\ell$ just before, set $\beta_{v_t} = 1 - A(\ell)$. If $v_t$ is not assigned, $\beta_{v_t} = 0$.

**Claim 2 (dual value).** Let $c = 1 - r^{-b}$. At the end, $b \sum_u \alpha_u + \sum_v \beta_v = \lvert M \rvert / c$.

*Proof.* Both sides start at 0, and an unassigned arrival changes neither. When $v_t$ is assigned to $u$ at load $\ell$, the dual grows by

$$b\big(A(\ell+1) - A(\ell)\big) + 1 - A(\ell) = \frac{b \, r^\ell (r - 1)}{r^b - 1} + \frac{r^b - r^\ell}{r^b - 1} = \frac{r^\ell + r^b - r^\ell}{r^b - 1} = \frac{1}{1 - r^{-b}},$$

since $b(r - 1) = 1$. The size of $M$ grows by 1. $\square$

**Claim 3 (dual feasibility).** At the end, $\alpha_u + \beta_v \ge 1$ for each edge $(u, v)$.

*Proof.* Loads never decrease, so $\alpha_u$ never decreases. Look at the arrival of $v$, and let $\ell_u$ be the load of $u$ then.

- If $\ell_u = b$, then $u$ is full at the end too, and $\alpha_u = A(b) = 1$.
- If $\ell_u < b$, then $u \in C$ at line L4, so $C \ne \emptyset$ and $v$ is assigned to a vertex $u'$ whose load $\ell^*$ is the smallest in $C$. So $\ell^* \le \ell_u$, and since $A$ is increasing, at the end $\alpha_u \ge A(\ell_u) \ge A(\ell^*) = 1 - \beta_v$. $\square$

**Theorem.** For every input, $\lvert M \rvert \ge \big(1 - (1 + 1/b)^{-b}\big) \cdot \mathrm{OPT}$.

*Proof.* By Claim 3 the final $(\alpha, \beta)$ is dual feasible, so by weak duality $\mathrm{OPT} \le b \sum_u \alpha_u + \sum_v \beta_v$. By Claim 2 this is $\lvert M \rvert / c$. So $\lvert M \rvert \ge c \cdot \mathrm{OPT}$ with $c = 1 - (1 + 1/b)^{-b}$. $\blacksquare$

**Remarks.**

- For $b = 1$, $c = 1/2$, the bound of any greedy rule. For $b = 2$, $c = 5/9$; for $b = 3$, $c = 37/64$. Since $(1 + 1/b)^b$ increases to $e$, $c$ increases to $1 - 1/e$.
- The proof also bounds Balance against the fractional optimum, not only the integral one.
- The proof uses only that the chosen vertex has the smallest load among the neighbours with room. Ties may be broken in any way.
