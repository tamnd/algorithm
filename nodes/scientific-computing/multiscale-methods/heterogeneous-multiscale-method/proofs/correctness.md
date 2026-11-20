---
title: The 1D heterogeneous multiscale method has an error controlled by the error of its estimated coefficients
proves: [correctness]
status: full
---

We prove three facts about the 1D method of the page, in exact arithmetic. The problem is $-(a_\varepsilon u')' = f$ on $(0, 1)$, $u(0) = u(1) = 0$, with $0 < \alpha \le a_\varepsilon \le \beta$. For the periodic case, $a_\varepsilon(x) = a(x/\varepsilon)$ with $a$ 1-periodic, and the homogenized coefficient is the harmonic mean $a^* = (\int_0^1 dy / a(y))^{-1}$, so $\alpha \le a^* \le \beta$.

**Lemma 1 (the micro estimate is a harmonic mean).** Let the micro cell $I = [x_K - \delta/2, x_K + \delta/2]$ have $c$ cells of length $\eta = \delta / c$ with values $a_1, \ldots, a_c$. Lines L2 and L3 return

$$a_K = \Big( \frac1c \sum_{j=1}^{c} \frac{1}{a_j} \Big)^{-1}.$$

*Proof.* The P1 equation of line L2 at an interior micro node $j$ reads $a_j (v_j - v_{j-1})/\eta = a_{j+1} (v_{j+1} - v_j)/\eta$, so the flux $q = a_j (v_j - v_{j-1})/\eta$ is the same on every cell. Then $v_j - v_{j-1} = q \eta / a_j$, and the boundary values give $\delta = v_c - v_0 = q \eta \sum_j 1/a_j$. Line L3 returns $\delta^{-1} \sum_j a_j (v_j - v_{j-1}) = \delta^{-1} c\, q \eta = q$, and $q = c / \sum_j (1/a_j)$. The tridiagonal system has one solution, because it is the stiffness matrix of a positive coefficient with Dirichlet conditions. $\square$

The same argument for the exact micro problem $-(a_\varepsilon v')' = 0$ on $I$, $v = x - x_K$ at the ends, gives $a_K = (\delta^{-1} \int_I dx / a_\varepsilon)^{-1}$. The micro mesh of line L2 computes this value with the midpoint rule.

**Lemma 2 (the error of the estimate).** For the exact micro problem and periodic $a_\varepsilon$,

$$\Big| \frac{1}{a_K} - \frac{1}{a^*} \Big| \le \frac{\varepsilon}{\delta} \max_y \Big| \frac{1}{a(y)} - \frac{1}{a^*} \Big|, \qquad |a_K - a^*| \le \beta^2 \frac{\varepsilon}{\delta} \max_y \Big| \frac{1}{a(y)} - \frac{1}{a^*} \Big|.$$

If $\delta$ is a whole multiple of $\varepsilon$, then $a_K = a^*$.

*Proof.* Write $\delta = p \varepsilon + r$ with an integer $p \ge 0$ and $0 \le r < \varepsilon$, and split $I$ into $p$ intervals of length $\varepsilon$ and a rest $R$ of length $r$. The integral of $1/a_\varepsilon$ over an interval of length $\varepsilon$ is $\varepsilon / a^*$ by periodicity. So

$$\frac{1}{a_K} - \frac{1}{a^*} = \frac{1}{\delta} \int_I \Big( \frac{1}{a_\varepsilon} - \frac{1}{a^*} \Big) dx = \frac{1}{\delta} \int_R \Big( \frac{1}{a_\varepsilon} - \frac{1}{a^*} \Big) dx,$$

whose absolute value is at most $(r / \delta) \max |1/a - 1/a^*| \le (\varepsilon / \delta) \max |1/a - 1/a^*|$. For $r = 0$ the right side is zero. The second bound follows from $|a_K - a^*| = a_K a^* |1/a_K - 1/a^*|$ and $a_K, a^* \le \beta$, since a harmonic mean of values in $[\alpha, \beta]$ lies in $[\alpha, \beta]$. $\square$

**Theorem (the macro error).** Let $U$ be the result of lines L4 to L6, and let $u_H$ be the P1 solution of the homogenized problem $-(a^* u')' = f$ on the same mesh with the same load. With $e = \max_K |a_K - a^*|$,

$$\| (u_H - U)' \|_{L^2} \le \frac{e}{a^*} \| U' \|_{L^2}.$$

*Proof.* Lines L4 and L5 compute the Galerkin solution $U \in V_H$ of $A(U, v) = F(v)$ for all $v \in V_H$, with $A(w, v) = \sum_K a_K \int_K w' v'$ and the load $F$ of line L4. The homogenized solution satisfies $A^*(u_H, v) = F(v)$ with $A^*(w, v) = a^* \int_0^1 w' v'$. Put $v = u_H - U \in V_H$. Then

$$a^* \| v' \|^2 = A^*(u_H, v) - A^*(U, v) = A(U, v) - A^*(U, v) = \sum_K (a_K - a^*) \int_K U' v' \le e\, \| U' \|\, \| v' \|$$

by the Cauchy-Schwarz inequality on each element and then for the sum. Divide by $a^* \| v' \|$. $\square$

**Consequences.** In 1D with a constant coefficient, the P1 solution is exact at the nodes when the load is exact, and Simpson's rule in line L4 is exact for $f$ of degree at most 2 times a linear hat function. So for such $f$, $u_H$ equals the homogenized solution $u_0$ at the nodes, and the HMM error at the nodes comes only from $e$. By Lemma 2, $e = 0$ when the micro cell holds whole periods, and $e$ is of order $\varepsilon / \delta$ otherwise. By Lemma 1 the micro mesh adds the error of the midpoint rule for $\int_I dx / a_\varepsilon$, which for a smooth periodic $a$ over whole periods decreases faster than any power of $\eta / \varepsilon$. This is the structure of the general HMM analysis: the total error is the error of the macro solver for the homogenized problem plus a term controlled by the error $e$ of the estimated data.

The proof does not show that $u_\varepsilon$ is close to $u_0$; that is the homogenization theorem, and the HMM approximates $u_0$, not the fine oscillations of $u_\varepsilon$.
