---
title: The derivatives of Sammon's stress, its fixed points and the descent direction
proves: [correctness]
status: full
---

Write $E(Y) = \frac1c\sum_{i<j}(\delta_{ij} - d_{ij})^2/\delta_{ij}$ with $c = \sum_{i<j}\delta_{ij} > 0$, $\delta_{ij} > 0$ and $d_{ij} = \|y_i - y_j\|$. We assume $d_{pj} > 0$ for all pairs, so that $E$ is twice differentiable at $Y$.

**Lemma 1 (zero stress).** $E(Y) \ge 0$, and $E(Y) = 0$ if and only if $d_{ij} = \delta_{ij}$ for all $i < j$.

*Proof.* Each term $(\delta_{ij} - d_{ij})^2/\delta_{ij}$ is non-negative because $\delta_{ij} > 0$, and it is 0 exactly when $d_{ij} = \delta_{ij}$. The sum of non-negative terms is 0 exactly when each term is 0. $\square$

**Lemma 2 (first derivative).** For a point $p$ and a coordinate $q$,

$$\frac{\partial E}{\partial y_{pq}} = -\frac2c\sum_{j\ne p}\frac{\delta_{pj} - d_{pj}}{\delta_{pj}d_{pj}}u_j, \qquad u_j = y_{pq} - y_{jq}.$$

*Proof.* Only the terms with the pairs $\{p, j\}$ depend on $y_{pq}$. From $d_{pj}^2 = \sum_r (y_{pr} - y_{jr})^2$ we get $\partial d_{pj}/\partial y_{pq} = u_j/d_{pj}$. So the derivative of $(\delta_{pj} - d_{pj})^2/\delta_{pj}$ is $-2(\delta_{pj} - d_{pj})u_j/(\delta_{pj}d_{pj})$. Sum over $j$ and divide by $c$. $\square$

**Lemma 3 (second derivative).** With the same notation,

$$\frac{\partial^2 E}{\partial y_{pq}^2} = -\frac2c\sum_{j\ne p}\frac{1}{\delta_{pj}d_{pj}}\left[(\delta_{pj} - d_{pj}) - \frac{u_j^2}{d_{pj}}\left(1 + \frac{\delta_{pj} - d_{pj}}{d_{pj}}\right)\right].$$

*Proof.* Differentiate one term $f_j = (\delta_{pj} - d_{pj})u_j/(\delta_{pj}d_{pj}) = u_j/d_{pj} - u_j/\delta_{pj}$ of Lemma 2 with respect to $y_{pq}$. Since $\partial u_j/\partial y_{pq} = 1$ and $\partial d_{pj}/\partial y_{pq} = u_j/d_{pj}$,

$$\frac{\partial f_j}{\partial y_{pq}} = \frac{1}{d_{pj}} - \frac{u_j^2}{d_{pj}^3} - \frac{1}{\delta_{pj}}.$$

The bracket in the claim, divided by $\delta_{pj}d_{pj}$, is

$$\frac{\delta_{pj} - d_{pj}}{\delta_{pj}d_{pj}} - \frac{u_j^2}{\delta_{pj}d_{pj}^2}\cdot\frac{\delta_{pj}}{d_{pj}} = \frac{1}{d_{pj}} - \frac{1}{\delta_{pj}} - \frac{u_j^2}{d_{pj}^3},$$

because $1 + (\delta_{pj} - d_{pj})/d_{pj} = \delta_{pj}/d_{pj}$. The two expressions agree. Multiply by $-2/c$ and sum over $j$. $\square$

**Theorem 1 (exact fits are fixed points).** If $d_{ij} = \delta_{ij}$ for all pairs and each $h_{pq} \ne 0$, then line L6 returns $Y$ unchanged.

*Proof.* Each factor $\delta_{pj} - d_{pj}$ in Lemma 2 is 0, so each $g_{pq} = 0$, and the update of line L6 adds $-\mathrm{MF}\cdot 0/|h_{pq}| = 0$ to each coordinate. By Lemma 1 the stress is 0, its global minimum. $\square$

At an exact fit, Lemma 3 gives $h_{pq} = \frac2c\sum_{j\ne p}u_j^2/(\delta_{pj}d_{pj}^2) \ge 0$, and $h_{pq} > 0$ unless all other points share the coordinate $q$ with point $p$. The implementation replaces $|h_{pq}|$ by $\max(|h_{pq}|, 10^{-12})$, so the update is 0 in that case too.

**Theorem 2 (descent direction).** Let $g \ne 0$ be the gradient of $E$ at $Y$, and let $s$ have the entries $s_{pq} = -g_{pq}/|h_{pq}|$ with all $h_{pq} \ne 0$. Then $\langle g, s\rangle < 0$, and $E(Y + \mu s) < E(Y)$ for all small enough $\mu > 0$.

*Proof.* $\langle g, s\rangle = -\sum_{p,q} g_{pq}^2/|h_{pq}|$. Each term is non-negative and at least one is positive, so the sum is negative. Since $E$ is differentiable at $Y$, $E(Y + \mu s) = E(Y) + \mu\langle g, s\rangle + o(\mu)$, which is less than $E(Y)$ for small $\mu > 0$. $\square$

A plain Newton step for one coordinate, $-g_{pq}/h_{pq}$, goes uphill when $h_{pq} < 0$. The absolute value in line L6 is what makes Theorem 2 hold for every sign of $h_{pq}$.

**No monotone guarantee.** Theorem 2 needs a small enough step, and line L6 uses the fixed value $\mu = \mathrm{MF}$. No fixed value is small enough for all inputs, because $|h_{pq}|$ can be arbitrarily close to 0 while $g_{pq}$ is not. The example on the page is a concrete case: from the start $(0,0), (1,0), (0,1), (0.3, 0.3)$ with $\mathrm{MF} = 0.35$, the stress rises from 0.1289 to 0.7521 in one step. So the method is a heuristic, and the tests check a decrease over a run, not at each step.
