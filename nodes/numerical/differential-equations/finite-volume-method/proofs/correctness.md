---
title: The finite volume update conserves the total exactly, and is total variation diminishing and bounded under the CFL condition
proves: [correctness, termination]
status: full
---

**Setting.** Cells $i = 1, \ldots, m$ of width $\Delta x > 0$ carry values $u_i$. One step of FINITE-VOLUME with step $k > 0$ (equal to $\Delta t$, or shorter for the last step) and $\lambda = k/\Delta x$ computes ghost values $u_0, u_{m+1}$, face fluxes $F_{i+1/2} = F(u_i, u_{i+1})$ for $i = 0, \ldots, m$, and

$$u_i^{\text{new}} = u_i - \lambda\big(F_{i+1/2} - F_{i-1/2}\big), \qquad i = 1, \ldots, m. \tag{1}$$

Periodic boundaries use $u_0 = u_m$, $u_{m+1} = u_1$; transmissive ones use $u_0 = u_1$, $u_{m+1} = u_m$. We write $\Delta_{i+1/2} = u_{i+1} - u_i$ and $TV(u) = \sum_{i=1}^m|u_{i+1} - u_i|$ with $u_{m+1} = u_1$ (periodic total variation).

**Termination.** The loop runs $\lceil T/\Delta t\rceil$ times (computed with a relative slack of $10^{-9}$ against rounding), each step evaluates $m + 1$ fluxes and does $O(m)$ arithmetic, and the last step has length $T - t > 0$ so the run ends exactly at $T$.

**Theorem 1 (discrete conservation).** For any numerical flux, one step changes the total amount $\Delta x\sum_iu_i$ by

$$\Delta x\sum_{i=1}^m u_i^{\text{new}} - \Delta x\sum_{i=1}^m u_i = k\big(F_{1/2} - F_{m+1/2}\big),$$

which is zero for periodic boundaries. Over the run, the total changes by the accumulated boundary balance, which the implementation returns as `mass_change`.

*Proof.* Multiply (1) by $\Delta x$ and sum over $i$. The inner fluxes cancel in pairs, $\sum_{i=1}^m(F_{i+1/2} - F_{i-1/2}) = F_{m+1/2} - F_{1/2}$, and $\lambda\Delta x = k$. For periodic boundaries $F_{m+1/2} = F(u_m, u_{m+1}) = F(u_0, u_1) = F_{1/2}$, because $u_{m+1} = u_1$ and $u_0 = u_m$. Every operation is a field operation on the data and the flux values, so the identity holds exactly in rational arithmetic, as the tests check with fractions. $\square$

**Lemma 2 (Harten).** Suppose that for periodic data one step can be written as

$$u_i^{\text{new}} = u_i + D_{i+1/2}\Delta_{i+1/2} - C_{i-1/2}\Delta_{i-1/2} \tag{2}$$

with indices taken modulo $m$ and coefficients satisfying $C_{i+1/2} \ge 0$, $D_{i+1/2} \ge 0$ and $C_{i+1/2} + D_{i+1/2} \le 1$ for every $i$. Then $TV(u^{\text{new}}) \le TV(u)$.

*Proof.* Subtracting (2) at $i$ from (2) at $i + 1$,

$$\Delta^{\text{new}}_{i+1/2} = \big(1 - C_{i+1/2} - D_{i+1/2}\big)\Delta_{i+1/2} + D_{i+3/2}\Delta_{i+3/2} + C_{i-1/2}\Delta_{i-1/2}.$$

All three coefficients are nonnegative. Taking absolute values, summing over $i$ modulo $m$, and shifting the index in the last two sums,

$$TV(u^{\text{new}}) \le \sum_i\big(1 - C_{i+1/2} - D_{i+1/2}\big)|\Delta_{i+1/2}| + \sum_iD_{i+1/2}|\Delta_{i+1/2}| + \sum_iC_{i+1/2}|\Delta_{i+1/2}| = TV(u). \ \square$$

**Theorem 3 (TVD under the CFL condition).** With periodic boundaries:

1. For the upwind flux of $f(u) = au$ and $\lambda|a| \le 1$, $TV(u^{\text{new}}) \le TV(u)$ and $\min(u_{i-1}, u_i, u_{i+1}) \le u_i^{\text{new}} \le \max(u_{i-1}, u_i, u_{i+1})$.
2. For the Rusanov flux with $f \in C^1$ and $f'$ monotone ($f$ convex or concave), and $\lambda s_{i+1/2} \le 1$ for every face, where $s_{i+1/2} = \max(|f'(u_i)|, |f'(u_{i+1})|)$, $TV(u^{\text{new}}) \le TV(u)$. If $\lambda s_{i+1/2} \le \tfrac12$ for every face, then also $\min(u_{i-1}, u_i, u_{i+1}) \le u_i^{\text{new}} \le \max(u_{i-1}, u_i, u_{i+1})$.

*Proof.* (1) For $a \ge 0$, (1) reads $u_i^{\text{new}} = u_i - \lambda a\Delta_{i-1/2}$, which is (2) with $C = \lambda a$, $D = 0$; for $a < 0$ it is $u_i^{\text{new}} = u_i - \lambda|a|\cdot(-\Delta_{i+1/2})$, which is (2) with $C = 0$, $D = \lambda|a|$. In both cases $C + D = \lambda|a| \le 1$, so Lemma 2 applies. Also $u_i^{\text{new}} = (1 - \lambda|a|)u_i + \lambda|a|u_{i\mp1}$ is a convex combination, which gives the bounds.

(2) Let $a_{i+1/2} = (f(u_{i+1}) - f(u_i))/\Delta_{i+1/2}$ if $\Delta_{i+1/2} \ne 0$ and $f'(u_i)$ otherwise. By the mean value theorem $a_{i+1/2} = f'(\xi)$ for some $\xi$ between $u_i$ and $u_{i+1}$, and since $f'$ is monotone, $|f'(\xi)| \le \max(|f'(u_i)|, |f'(u_{i+1})|)$, so $|a_{i+1/2}| \le s_{i+1/2}$. From the definition of the Rusanov flux,

$$F_{i+1/2} - f(u_i) = \tfrac12(a_{i+1/2} - s_{i+1/2})\Delta_{i+1/2}, \qquad f(u_i) - F_{i-1/2} = \tfrac12(a_{i-1/2} + s_{i-1/2})\Delta_{i-1/2}.$$

Adding these and inserting into (1) gives (2) with $D_{i+1/2} = \tfrac{\lambda}{2}(s - a)_{i+1/2} \ge 0$ and $C_{i+1/2} = \tfrac{\lambda}{2}(s + a)_{i+1/2} \ge 0$, and $C_{i+1/2} + D_{i+1/2} = \lambda s_{i+1/2} \le 1$. Lemma 2 gives the TVD property. For the bounds, write

$$u_i^{\text{new}} = \tfrac12\Big(u_i + 2D_{i+1/2}(u_{i+1} - u_i)\Big) + \tfrac12\Big(u_i + 2C_{i-1/2}(u_{i-1} - u_i)\Big).$$

If $\lambda s \le \tfrac12$ at every face, then $2D_{i+1/2} \le 2\lambda s_{i+1/2} \le 1$ and $2C_{i-1/2} \le 1$, so each bracket is a convex combination of two of the three values and so is their average. $\blacksquare$

**Remarks.** (i) The tests check the bounds for the Rusanov flux with $f(u) = u^2/2$ up to $\lambda\max|u| = 1$, where they are observed but not covered by part 2. (ii) For transmissive boundaries, the ghost differences $\Delta_{1/2}$ and $\Delta_{m+1/2}$ vanish and the same computation gives $\sum_{i=1}^{m-1}|\Delta^{\text{new}}_{i+1/2}| \le \sum_{i=1}^{m-1}|\Delta_{i+1/2}|$. (iii) Convergence is cited, not proved: the Lax-Wendroff theorem (Lax and Wendroff 1960; LeVeque 2002, Chapter 12) states that if the numerical solutions of a conservative scheme with consistent Lipschitz flux converge boundedly almost everywhere as $\Delta x, \Delta t \to 0$, the limit is a weak solution. Monotone schemes, a class that includes the upwind scheme under the CFL condition, converge to the entropy solution, with $L^1$ error $O(\Delta x^{1/2})$ for initial data of bounded variation (Kuznetsov).
