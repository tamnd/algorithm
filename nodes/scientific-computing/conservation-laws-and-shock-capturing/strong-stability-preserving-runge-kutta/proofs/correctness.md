---
title: An SSP Runge-Kutta step keeps every convex bound of forward Euler for dt at most C dt_FE
proves: [correctness]
status: full
---

**Setting.** The semidiscrete system is $u' = L(u)$ in $\mathbb{R}^M$. Let $\|\cdot\|$ be a convex functional, for example a norm, the total variation seminorm $\mathrm{TV}(u) = \sum_j|u_j - u_{j-1}|$, or the maximum $\max_ju_j$. Assume that forward Euler is strongly stable for this functional up to a step $\Delta t_{FE}$:

$$\|u + \Delta t\,L(u)\| \le \|u\| \quad \text{for all } u \text{ and all } 0 \le \Delta t \le \Delta t_{FE}. \tag{FE}$$

An explicit method in Shu-Osher form with $s$ stages computes $y_0 = u$ (line L1), then for $i = 1, \dots, s$ (line L2)

$$y_i = \sum_{k=0}^{i-1}\big(\alpha_{ik}y_k + \Delta t\,\beta_{ik}L(y_k)\big) \quad \text{(line L3)},$$

and returns $u^{\text{new}} = y_s$ (line L4). The code computes each $L(y_k)$ once, before it is first used, and then forms the sums exactly as written. Consistency requires $\sum_k\alpha_{ik} = 1$ for each $i$, because a constant state with $L = 0$ must stay constant.

**The SSP coefficient (lines L5 and L6).** If some $\alpha_{ik} < 0$ or $\beta_{ik} < 0$, then $C = 0$. Otherwise $C = \min\{\alpha_{ik}/\beta_{ik} : \beta_{ik} > 0\}$, with $C = 0$ when some $\beta_{ik} > 0$ has $\alpha_{ik} = 0$.

**Theorem 1 (strong stability).** Assume $\alpha_{ik} \ge 0$, $\beta_{ik} \ge 0$, $\sum_k\alpha_{ik} = 1$, and $C > 0$. Then (FE) implies $\|u^{\text{new}}\| \le \|u\|$ for all $0 \le \Delta t \le C\,\Delta t_{FE}$.

*Proof.* We show $\|y_i\| \le \|u\|$ by induction on $i$; the case $i = 0$ is trivial. Let $P_i$ be the set of $k < i$ with $\alpha_{ik} > 0$. Since $C > 0$, $\beta_{ik} > 0$ implies $\alpha_{ik} > 0$, so the terms with $k \notin P_i$ are zero, and

$$y_i = \sum_{k \in P_i}\alpha_{ik}\Big(y_k + \frac{\beta_{ik}}{\alpha_{ik}}\Delta t\,L(y_k)\Big).$$

The weights $\alpha_{ik}$, $k \in P_i$, are positive and sum to 1, so this is a convex combination of forward Euler steps. Each step has size $(\beta_{ik}/\alpha_{ik})\Delta t \le \Delta t/C \le \Delta t_{FE}$. By convexity, then (FE), then the induction hypothesis,

$$\|y_i\| \le \sum_{k \in P_i}\alpha_{ik}\Big\|y_k + \frac{\beta_{ik}}{\alpha_{ik}}\Delta t\,L(y_k)\Big\| \le \sum_{k \in P_i}\alpha_{ik}\|y_k\| \le \|u\|. \qquad \square$$

The same argument keeps any convex set invariant: if forward Euler maps a convex set $S$ (for example the states with positive density and pressure) into itself for $\Delta t \le \Delta t_{FE}$, the SSP step does so for $\Delta t \le C\,\Delta t_{FE}$.

**Theorem 2 (coefficients and orders of the four methods).**

| method | $C$ | order |
|---|---|---|
| forward Euler | 1 | 1 |
| SSPRK(2,2) | 1 | 2 |
| SSPRK(3,3) | 1 | 3 |
| SSPRK(10,4) | 6 | 4 |

*Proof.* The values of $C$ follow from the tables by lines L5 and L6. In SSPRK(2,2) every ratio is 1. In SSPRK(3,3) the nonzero pairs are $(1, 1)$, $(\frac14, \frac14)$ and $(\frac23, \frac23)$. In SSPRK(10,4) every nonzero $\beta$ is $\frac16$ times its $\alpha$; the weights $\alpha_{5,0} = \frac35$ and $\alpha_{10,0} = \frac1{25}$ have $\beta = 0$.

For the order, eliminate the intermediate stages to get the Butcher form. SSPRK(2,2) gives nodes $c = (0, 1)$ and weights $b = (\frac12, \frac12)$, so $\sum b_i = 1$ and $\sum b_ic_i = \frac12$: order 2. For SSPRK(3,3), $y_1 = u + \Delta t L_0$, $y_2 = u + \frac{\Delta t}{4}(L_0 + L_1)$ and $y_3 = u + \Delta t(\frac16L_0 + \frac16L_1 + \frac23L_2)$, with $L_k = L(y_k)$. So $a_{21} = 1$, $a_{31} = a_{32} = \frac14$, $c = (0, 1, \frac12)$ and $b = (\frac16, \frac16, \frac23)$. The four conditions for order 3 hold:

$$\textstyle\sum b_i = 1, \quad \sum b_ic_i = \frac16 + \frac13 = \frac12, \quad \sum b_ic_i^2 = \frac16 + \frac16 = \frac13, \quad \sum b_ia_{ij}c_j = \frac23\cdot\frac14\cdot1 = \frac16.$$

For SSPRK(10,4) the order is cited from Ketcheson (2008); the tests on this page measure order 4 on a nonlinear ODE. $\square$

**Theorem 3 (upper bound $C \le s$).** For an explicit method with $s$ stages, order at least 1 and $C > 0$, $C \le s$.

*Proof.* Apply the method to $u' = \lambda u$ with $z = \lambda\Delta t$, and set $w = 1 + z/C$. Because $\beta_{ik}/\alpha_{ik} \le 1/C$,

$$1 + \frac{\beta_{ik}}{\alpha_{ik}}z = \Big(1 - \frac{\beta_{ik}C}{\alpha_{ik}}\Big) + \frac{\beta_{ik}C}{\alpha_{ik}}\,w$$

is a polynomial in $w$ with nonnegative coefficients. By induction, each stage $y_i/u$ is a polynomial in $w$ of degree at most $i$ with nonnegative coefficients, and its value at $w = 1$ is $\sum_k\alpha_{ik} = 1$. So the stability function is $R(z) = \sum_{j=0}^s\gamma_jw^j$ with $\gamma_j \ge 0$ and $\sum_j\gamma_j = 1$. Order at least 1 gives $R'(0) = 1$, and $R'(0) = \frac1C\sum_jj\gamma_j \le \frac{s}{C}$. So $C \le s$. $\square$

So the effective coefficient $C/s$ is at most 1. SSPRK(10,4) has $C/s = 0.6$, and SSPRK(3,3) has $C/s = \frac13$.

**Cited barriers, not proved here.** No explicit Runge-Kutta method with four stages and order four has $C > 0$ (Gottlieb and Shu 1998). No explicit Runge-Kutta method of order five or more has $C > 0$ (Ruuth and Spiteri 2002). The classical fourth-order method in Shu-Osher form has $\alpha_{4,0} = -\frac13$ and a pair with $\alpha_{2,1} = 0 < \beta_{2,1}$, so lines L5 and L6 return 0 for it.

**What the result does not say.** Theorem 1 transfers a property that forward Euler has; it does not create one. The time step bound $\Delta t \le C\,\Delta t_{FE}$ is sufficient, not necessary: for a particular $L$ a larger step can still keep the bound. And a method with $C = 0$ can still keep the bound for some problems; the counterexample in the tests shows a second-order method with a negative coefficient that does not. $\blacksquare$
