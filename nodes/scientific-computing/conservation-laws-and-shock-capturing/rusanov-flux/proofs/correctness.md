---
title: The Rusanov scheme is conservative and consistent, and for a convex scalar law it is TVD and keeps a discrete maximum principle
proves: [correctness]
status: full
---

**Setting.** The scheme stores cell averages $U_j^n$ on a uniform grid with width $\Delta x$ and steps $U_j^{n+1} = U_j^n - \lambda(F_{j+1/2} - F_{j-1/2})$ with $\lambda = \Delta t/\Delta x$ (line L5). The face flux is the Rusanov flux of lines L1 and L2,

$$F_{j+1/2} = \tfrac12\big(f(U_j) + f(U_{j+1})\big) - \tfrac12 s_{j+1/2}(U_{j+1} - U_j),$$

where $s_{j+1/2}$ is the largest wave speed of the two states: $\max(|f'(U_j)|, |f'(U_{j+1})|)$ for a scalar law, and $\max(|u| + c)$ over the two states for the Euler equations. The grid is periodic, or it has one outflow ghost cell on each side, filled by copy, as in line L3.

**Lemma 1 (consistency).** $F(U, U) = f(U)$ for every state $U$.

*Proof.* With $U_L = U_R = U$ the dissipation term $\frac12 s(U_R - U_L)$ is zero, and the average of the two fluxes is $f(U)$. $\square$

**Lemma 2 (conservation).** On a periodic grid, $\sum_j U_j^{n+1} = \sum_j U_j^n$ for each conserved component.

*Proof.* Each face flux $F_{j+1/2}$ enters the update of cell $j$ with the factor $-\lambda$ and the update of cell $j+1$ with the factor $+\lambda$. The sum over all cells telescopes to zero. In floating point arithmetic the sum is kept up to rounding. With rational data and `Fraction` arithmetic it is kept exactly, and the test checks this for Burgers' equation. $\square$

**Lemma 3 (Harten's incremental form).** Let a scheme be written as $U_j^{n+1} = U_j + C_{j+1/2}\Delta_{j+1/2} - D_{j-1/2}\Delta_{j-1/2}$ with $\Delta_{j+1/2} = U_{j+1} - U_j$, where the coefficients may depend on the data. If $C_{j+1/2} \ge 0$, $D_{j+1/2} \ge 0$ and $C_{j+1/2} + D_{j+1/2} \le 1$ for all $j$, then $TV(U^{n+1}) \le TV(U^n)$ on a periodic grid.

*Proof.* Subtract the formula for cell $j$ from the formula for cell $j+1$:

$$\Delta_{j+1/2}^{n+1} = (1 - C_{j+1/2} - D_{j+1/2})\Delta_{j+1/2} + C_{j+3/2}\Delta_{j+3/2} + D_{j-1/2}\Delta_{j-1/2}.$$

The three coefficients are nonnegative. Take absolute values, use the triangle inequality, and sum over $j$. After a shift of the index in the second and the third sum, the right side is $\sum_j (1 - C_{j+1/2} - D_{j+1/2} + C_{j+1/2} + D_{j+1/2})|\Delta_{j+1/2}| = TV(U^n)$. $\square$

This is the lemma of Harten (1983); LeVeque (2002, Section 12.12) uses it in the same way.

**Theorem 1 (TVD and maximum principle for a convex scalar law).** Let $f$ be convex and $C^1$.

1. If $\lambda \max_j s_{j+1/2} \le 1$, the Rusanov scheme is TVD.
2. If $\lambda \max_j s_{j+1/2} \le 1/2$, then $\min(U_{j-1}, U_j, U_{j+1}) \le U_j^{n+1} \le \max(U_{j-1}, U_j, U_{j+1})$ for every $j$.

*Proof.* Let $a_{j+1/2} = (f(U_{j+1}) - f(U_j))/\Delta_{j+1/2}$ when $\Delta_{j+1/2} \ne 0$, and $a_{j+1/2} = f'(U_j)$ otherwise. By the mean value theorem $a_{j+1/2} = f'(\xi)$ for some $\xi$ between $U_j$ and $U_{j+1}$. Because $f$ is convex, $f'$ is nondecreasing, so $f'(\xi)$ lies between $f'(U_j)$ and $f'(U_{j+1})$, and $|a_{j+1/2}| \le s_{j+1/2}$. Two ways to write the flux follow from $f(U_{j+1}) = f(U_j) + a_{j+1/2}\Delta_{j+1/2}$:

$$F_{j+1/2} = f(U_j) + \tfrac12(a_{j+1/2} - s_{j+1/2})\Delta_{j+1/2} = f(U_{j+1}) - \tfrac12(a_{j+1/2} + s_{j+1/2})\Delta_{j+1/2}.$$

Use the first form at the face $j+1/2$ and the second form at the face $j-1/2$ in line L5. The terms $f(U_j)$ cancel, and

$$U_j^{n+1} = U_j + C_{j+1/2}\Delta_{j+1/2} - D_{j-1/2}\Delta_{j-1/2}, \qquad C_{j+1/2} = \tfrac{\lambda}{2}(s - a)_{j+1/2}, \quad D_{j+1/2} = \tfrac{\lambda}{2}(s + a)_{j+1/2}.$$

Both coefficients are nonnegative because $|a| \le s$, and $C_{j+1/2} + D_{j+1/2} = \lambda s_{j+1/2} \le 1$. Lemma 3 gives part 1.

For part 2, write the same update as a weighted sum of three values:

$$U_j^{n+1} = (1 - C_{j+1/2} - D_{j-1/2})U_j + C_{j+1/2}U_{j+1} + D_{j-1/2}U_{j-1}.$$

The weights sum to 1, and the last two are nonnegative. Since $|a| \le s$, $C_{j+1/2} \le \lambda s_{j+1/2}$ and $D_{j-1/2} \le \lambda s_{j-1/2}$, so $C_{j+1/2} + D_{j-1/2} \le 2\lambda \max s \le 1$. All weights are nonnegative, and $U_j^{n+1}$ is a convex combination of $U_{j-1}$, $U_j$ and $U_{j+1}$. $\square$

The test checks the global bounds on a Burgers step at the Courant number 0.9, above the bound 1/2 of part 2. That check is a measurement for this problem, not a proof for that Courant number.

**Theorem 2 (positivity for the Euler equations, under a hypothesis).** Suppose that at every face, $s_{j+1/2}$ is at least the largest absolute wave speed of the exact Riemann solution between $U_j$ and $U_{j+1}$, and that $\lambda \max s \le 1/2$. If all $U_j^n$ have positive density and pressure, then so do all $U_j^{n+1}$.

*Proof.* The Rusanov flux is the HLL flux with the speeds $S_L = -s$ and $S_R = s$. With these speeds, the HLL intermediate state $U^*_{j+1/2} = \frac12(U_j + U_{j+1}) - \frac{1}{2s}(f(U_{j+1}) - f(U_j))$ equals the average of the exact Riemann solution over $[-s\Delta t, s\Delta t]$ at time $\Delta t$. This follows from the integral form of the conservation law over that rectangle, because no wave leaves the interval. The set of states with positive density and pressure is convex, so an average of such states is again such a state. When $\lambda s \le 1/2$, the fans of neighboring faces do not meet, and $U_j^{n+1}$ is the average over cell $j$ of a function whose values are $U_j$ and the two intermediate states. So it is a convex combination of admissible states. This is the argument of Einfeldt, Munz, Roe and Sjögreen (1991) for HLL type solvers. $\square$

The estimate $s = \max(|u_L| + c_L, |u_R| + c_R)$ of line L1 bounds the wave speeds in many cases, but not in all cases: in a strong collision a shock can be faster than both. So Theorem 2 is a conditional result for the code on this page, and the test on the 123 problem is a measurement.

**Order.** For smooth $f$ and smooth data, the flux differs from $f(U_j) + \frac12 a\Delta_{j+1/2}$ by $\frac12 s\Delta_{j+1/2} = O(\Delta x)$, so the local truncation error is $O(\Delta x)$ and the scheme is first order accurate (LeVeque 2002, Section 8.2). The dissipation coefficient $s$ does not vanish where the solution is smooth, so the order is exactly 1 in general, as the refinement study on the page measures.
