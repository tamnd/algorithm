---
title: The DG operator is the Galerkin projection with numerical fluxes, it is conservative, and it is L2 stable for upwind advection
proves: [correctness, termination]
status: full
---

**Setting.** The grid is periodic with $M$ cells $C_j$ of width $\Delta x$, the degree is $k \ge 0$, and $V_h$ is the space of functions whose restriction to each cell is a polynomial of degree at most $k$. On $C_j$, $\xi = 2(x - x_j)/\Delta x$ and $u_h = \sum_l U_{j,l} P_l(\xi)$. The numerical flux $\hat F$ is consistent, $\hat F(u, u) = f(u)$. The DG method is: find $u_h(t) \in V_h$ such that for every cell $C_j$ and every polynomial $v$ of degree at most $k$ on $C_j$,

$$\int_{C_j} \partial_t u_h\, v\,dx - \int_{C_j} f(u_h)\, v_x\,dx + \hat F_{j+1/2}\, v(x_{j+1/2}^-) - \hat F_{j-1/2}\, v(x_{j-1/2}^+) = 0. \tag{W}$$

This is the equation $u_t + f(u)_x = 0$ multiplied by $v$ and integrated by parts over one cell, with the two unknown face values of $f(u)$ replaced by $\hat F$. The exact solution satisfies (W) when it is smooth, because then $\hat F$ at each face equals $f(u)$ by consistency.

**Lemma 1 (the cell equations).** (W) is equivalent to lines L2 to L6 of the main page, provided the integral in L5 is exact.

*Proof.* Take $v = P_l(\xi)$, $l = 0, \dots, k$. These polynomials span the test space, so (W) for all $v$ is equivalent to (W) for these $k + 1$ functions. Since $dx = \frac{\Delta x}{2}d\xi$ and $\int_{-1}^1 P_l P_m\,d\xi = \frac{2}{2l+1}\delta_{lm}$, the first term is $\frac{\Delta x}{2l+1}\frac{dU_{j,l}}{dt}$. Since $v_x = \frac{2}{\Delta x}P_l'(\xi)$, the second term is $-\int_{-1}^1 f(u_h)P_l'(\xi)\,d\xi = -V$. The face values of $v$ are $P_l(1) = 1$ and $P_l(-1) = (-1)^l$. So (W) reads $\frac{\Delta x}{2l+1}\frac{dU_{j,l}}{dt} = V - \hat F_{j+1/2} + (-1)^l\hat F_{j-1/2}$, which is L6. The traces in L2 are $u_h$ at $\xi = 1$ in $C_j$ and at $\xi = -1$ in $C_{j+1}$, which are $\sum_l U_{j,l}$ and $\sum_l (-1)^l U_{j+1,l}$. The Gauss rule with $k + 1$ points in L5 is exact for polynomials of degree $2k + 1$. When $f$ is linear, $f(u_h)P_l'$ has degree at most $2k - 1$, so L5 is exact. $\square$

**Lemma 2 (conservation).** $\frac{d}{dt}\sum_j \Delta x\,U_{j,0} = 0$ on a periodic grid. On a nonperiodic grid the total changes only by the two boundary fluxes.

*Proof.* For $l = 0$, $P_0' = 0$, so $V = 0$ and L6 gives $\Delta x\,\frac{dU_{j,0}}{dt} = -(\hat F_{j+1/2} - \hat F_{j-1/2})$. Each face flux appears once with each sign in the sum over $j$, so the sum telescopes to zero on a periodic grid and to $\hat F_{1/2} - \hat F_{M+1/2}$ otherwise. $\square$

Each stage of an explicit Runge-Kutta method is a linear combination of $U$ and of values of the operator, whose $l = 0$ rows sum to zero, so the fully discrete method also keeps $\sum_j U_{j,0}$ fixed (up to rounding). Since $\int_{C_j} u_h\,dx = \Delta x\,U_{j,0}$, this is the integral of $u_h$.

**Lemma 3 (energy identity).** Let $f(u) = au$ with $a > 0$ and the upwind flux $\hat F(u^-, u^+) = a u^-$. Then

$$\frac{d}{dt}\,\frac12\|u_h\|_{L^2}^2 = -\frac{a}{2}\sum_{j=1}^{M}\big(u^-_{j+1/2} - u^+_{j+1/2}\big)^2 \le 0.$$

For $a < 0$ the same holds with $|a|$, by the reflection $x \mapsto -x$.

*Proof.* Take $v = u_h$ in (W) on each cell and add over $j$. The first terms add to $\frac{d}{dt}\frac12\|u_h\|^2$. In the second term, $\int_{C_j} a\,u_h\,\partial_x u_h\,dx = \frac{a}{2}\big((u^-_{j+1/2})^2 - (u^+_{j-1/2})^2\big)$. Collect the terms at one face $j + 1/2$: cell $C_j$ gives $-\frac{a}{2}(u^-)^2 + a u^- u^-$ and cell $C_{j+1}$ gives $+\frac{a}{2}(u^+)^2 - a u^- u^+$, with $u^\pm = u^\pm_{j+1/2}$. Their sum is $\frac{a}{2}\big((u^-)^2 - 2u^-u^+ + (u^+)^2\big) = \frac{a}{2}(u^- - u^+)^2$. So $\frac{d}{dt}\frac12\|u_h\|^2 + \frac{a}{2}\sum (u^- - u^+)^2 = 0$. $\square$

In coefficients, $\|u_h\|^2 = \sum_j\sum_l \frac{\Delta x}{2l+1}U_{j,l}^2$, so the identity says $\sum_{j,l}\frac{\Delta x}{2l+1}U_{j,l}R_{j,l} = -\frac{a}{2}\sum(u^- - u^+)^2$. By Lemma 1 the code computes $R$ exactly in this case, so the identity holds up to rounding; the tests check it on random data.

**Corollary ($k = 0$).** With $k = 0$ and the upwind flux, $R_{j,0} = -\frac{a}{\Delta x}(U_{j,0} - U_{j-1,0})$, the upwind scheme. This follows from L6 with $V = 0$ and $\hat F_{j+1/2} = aU_{j,0}$.

**Stability and convergence.** Lemma 3 gives $\|u_h(t)\| \le \|u_h(0)\| \le \|u_0\|$ for the semi-discrete method, since the $L^2$ projection does not increase the norm. Combined with the consistency of (W), this is the start of the error analysis. The estimates themselves are cited, not proved here: order $k$ on general meshes (Lesaint and Raviart 1974), $\|u - u_h\|_{L^2} \le C\,\Delta x^{k+1/2}\,|u_0|_{H^{k+1}}$ in general (Johnson and Pitkäranta 1986), sharp on some meshes (Peterson 1991). The order $k + 1$ observed on uniform meshes is a measurement on the main page.

**Termination.** The time loop runs $\lceil T/\Delta t\rceil$ steps, the last one shortened so the run ends at $T$. Each step makes three operator evaluations, and each evaluation is a fixed number of loops over the $M$ faces and the $M(k+1)$ coefficients. The Newton iteration for the Gauss nodes runs at most 100 times per node. So the method stops after finitely many operations. $\blacksquare$
