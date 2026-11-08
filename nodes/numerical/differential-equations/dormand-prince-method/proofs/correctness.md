---
title: The Dormand-Prince pair has orders 5 and 4, and the controlled loop ends at T
proves: [correctness, termination, order]
status: full
---

**Notation.** The pair has $s = 7$ stages with the coefficients $(A, b, c)$ of the main block, and the second weight vector $\hat b$. For a rooted tree $\tau$ let $|\tau|$ be its number of vertices, $\gamma(\tau)$ its density, and $\Phi(\tau) = \sum_i b_i \Phi_i(\tau)$ its elementary weight, where $\Phi_i(\bullet) = 1$ and $\Phi_i([\tau_1, \ldots, \tau_m]) = \prod_{k=1}^{m}\sum_j a_{ij}\Phi_j(\tau_k)$.

**Butcher's theorem** (Butcher 1963; HNW I, Section II.2). Let $f$ be $C^p$. A Runge-Kutta method with $\sum_j a_{ij} = c_i$ has order $p$, that is, its local error on every such problem is $O(h^{p+1})$, if and only if $\Phi(\tau) = 1/\gamma(\tau)$ for every rooted tree with $|\tau| \le p$.

**Lemma 1 (orders).** The weights $b$ satisfy the conditions for all 17 trees with at most 5 vertices, and fail at least one of the 20 conditions with 6 vertices. The weights $\hat b$ satisfy the conditions for all 8 trees with at most 4 vertices, and fail at least one with 5 vertices. Each row of $A$ sums to $c_i$.

*Proof.* Each condition is an identity between rational numbers built from the coefficients by sums and products. The trees of order 1 to 5 are $\bullet$; $[\bullet]$; $[\bullet, \bullet]$, $[[\bullet]]$; and the 4 trees of order 4 and 9 of order 5. For example the conditions of order at most 3 read $\sum b_i = 1$, $\sum b_i c_i = \tfrac12$, $\sum b_i c_i^2 = \tfrac13$, $\sum_{i,j} b_i a_{ij} c_j = \tfrac16$. For $b = (\tfrac{35}{384}, 0, \tfrac{500}{1113}, \tfrac{125}{192}, -\tfrac{2187}{6784}, \tfrac{11}{84}, 0)$ the first one is $\tfrac{35}{384} + \tfrac{500}{1113} + \tfrac{125}{192} - \tfrac{2187}{6784} + \tfrac{11}{84} = 1$. The test file of the implementation enumerates the trees by order and evaluates every condition in exact rational arithmetic (Python `fractions.Fraction`), so each claim of the lemma is checked as an exact identity, not in floating point. $\square$

By Butcher's theorem, the method with weights $b$ has order exactly 5 and the method with $\hat b$ has order exactly 4, for $f \in C^5$.

**Lemma 2 (FSAL).** The last row of $A$ equals $(b_1, \ldots, b_6)$, $b_7 = 0$ and $c_7 = 1$. Hence the seventh stage is $k_7 = f(t_n + h, y_{n+1})$, the first stage of the next step.

*Proof.* Compare the rows of the table; the seventh stage value is $y_n + h\sum_{j \le 6} a_{7j}k_j = y_n + h\sum_j b_j k_j = y_{n+1}$. $\square$

**Lemma 3 (the error estimate).** Let $f \in C^6$. For a step from an exact value $y_n = y(t_n)$, the difference $\mathrm{est} = h\sum_i (b_i - \hat b_i)k_i = y_{n+1} - \hat y_{n+1}$ satisfies $\mathrm{est} = \big(y(t_n + h) - \hat y_{n+1}\big) + O(h^6)$. So it equals the local error of the order-4 method up to a term of higher order.

*Proof.* By Lemma 1 and Butcher's theorem, $y(t_n + h) - y_{n+1} = O(h^6)$ and $y(t_n + h) - \hat y_{n+1} = O(h^5)$. Subtract. $\square$

**Lemma 4 (termination).** Assume that $f$ is $C^6$ near the solution, so that there are $h_0 > 0$ and $K$ (depending on the tolerances) with $\mathrm{err} \le K h^5$ whenever $h \le h_0$. Let $h^* = \min(h_0, K^{-1/5})$, let $h_1$ be the first trial step and $m = 0.2\min(h_1, h^*)$. Then every trial step except a cut last step has $h \ge m$, at most $\lceil \log(h/h^*)/\log(1/0.9) \rceil$ rejections happen in a row, and the loop ends with $t = T$ after at most $(T - t_0)/m + 1$ accepted steps.

*Proof.* If $h \le h^*$, then $\mathrm{err} \le K h^5 \le 1$ and the step is accepted. So a rejection needs $h > h^*$, and then the factor $\min(1, \max(0.2, 0.9\,\mathrm{err}^{-1/5}))$ is at most $0.9$, which gives the bound on rejections in a row. For the lower bound, use induction over the passes. If $h > h^*$, the factor is at least $0.2$, so the next $h$ is at least $0.2 h^* \ge m$. If $h \le h^*$, then $0.9\,\mathrm{err}^{-1/5} \ge 0.9 K^{-1/5}/h$, and since the upper limit of the factor is at least $1$, the next $h$ is at least $\min(h, 0.9K^{-1/5}) \ge \min(h, 0.9h^*) \ge m$ by the induction hypothesis. (If $\mathrm{err} = 0$ the factor is the upper limit, at least $1$.) Each accepted step that is not the last advances $t$ by at least $m$. Line L3 sets $h = T - t$ when the step would reach $T$, and the accepted last step sets $t = T$ exactly, so the loop of line L2 stops. $\blacksquare$

**What is not proved.** The controller makes the local error estimate of each accepted step at most 1 in the scaled norm. It does not bound the global error by the tolerance. That the global error at $T$ is roughly proportional to the tolerance is an asymptotic result for smooth problems under extra hypotheses on the controller, and otherwise an observation (HNW I, Section II.4).
