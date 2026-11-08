---
tag: 5VT41T
kind: theorem
slug: dahlquist-equivalence-theorem
name: Dahlquist equivalence theorem
aliases:
- Dahlquist convergence theorem
- Dahlquist's theorem on convergence of multistep methods
- consistency plus zero-stability implies convergence
area: numerical/differential-equations
level: advanced
summary: "A linear multistep method converges on every Lipschitz initial value problem if and only if it is consistent and zero-stable. With order p and starting errors O(h^p), the global error is O(h^p)."
prereqs: [linear-multistep-methods, zero-stability, consistency, global-error]
see_also: [dahlquist-barrier, lax-equivalence-theorem, adams-bashforth-methods, adams-moulton-methods, backward-differentiation-formulas, gronwall-inequality, local-truncation-error, order-of-accuracy]
sources:
  - paper: doi:10.7146/math.scand.a-10454
    title: Germund Dahlquist, Convergence and stability in the numerical integration of ordinary differential equations, Mathematica Scandinavica 4 (1956) 33-53
    locator: the root condition, the equivalence of convergence with consistency and stability, and the bound on the attainable order
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section III.2 (order of multistep methods), Section III.3 (stability and the first Dahlquist barrier), Section III.4 (convergence of multistep methods, the companion matrix formulation)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 2 (multistep methods; order, convergence, the root condition and the Dahlquist equivalence theorem)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 6 (zero-stability and convergence for initial value problems)
---

The Dahlquist equivalence theorem says that a [linear multistep method](/linear-multistep-methods/) for $y' = f(t, y)$ converges, for every initial value problem with $f$ Lipschitz in $y$ and every choice of starting values that tend to the exact ones, if and only if the method is [consistent](/consistency/) and [zero-stable](/zero-stability/). Consistency is two conditions on the polynomials $\rho$ and $\sigma$ at $\zeta = 1$, and zero-stability is the root condition on $\rho$, so convergence, a statement about all problems, is reduced to a finite check on the coefficients. Dahlquist proved it in 1956. It is the model for the [Lax equivalence theorem](/lax-equivalence-theorem/) for difference schemes for PDEs.

## Statement

**Setting.** A $k$-step method with real coefficients

$$\sum_{j=0}^{k}\alpha_j y_{n+j} = h\sum_{j=0}^{k}\beta_j f(t_{n+j}, y_{n+j}), \qquad \alpha_k = 1, \quad |\alpha_0| + |\beta_0| > 0,$$

on the grid $t_n = t_0 + nh$, with $\rho(\zeta) = \sum_j\alpha_j\zeta^j$ and $\sigma(\zeta) = \sum_j\beta_j\zeta^j$. The method is implicit when $\beta_k \ne 0$; for $h|\beta_k|L < 1$ the equation for $y_{n+k}$ has a unique solution by the contraction principle.

**Definitions.**

- *Consistent:* $\rho(1) = 0$ and $\rho'(1) = \sigma(1)$.
- *Zero-stable:* every root of $\rho$ has modulus at most 1, and every root of modulus 1 is simple (the root condition).
- *Convergent:* for every $d \ge 1$, every $T > t_0$, every $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ that is continuous and Lipschitz in $y$ with constant $L$, every $y_0$, and all starting values $y_0(h), \ldots, y_{k-1}(h)$ with $\eta(h) = \max_{i < k}\|y(t_i) - y_i(h)\| \to 0$ as $h \to 0$, the numbers satisfy

$$\max_{n : t_n \le T}\|y(t_n) - y_n\| \to 0 \quad \text{as } h = (T - t_0)/N \to 0.$$

**Theorem (Dahlquist 1956).** The method is convergent if and only if it is consistent and zero-stable.

**Quantitative form.** If the method is zero-stable, the [local truncation error](/local-truncation-error/) satisfies $\|\delta_{n+k}\| \le Ch^{p+1}$, and $\eta(h) \le C_0 h^p$, then $\max_{t_n \le T}\|y(t_n) - y_n\| \le K h^p$ for $h \le h_0$, with $K$ depending on $C$, $C_0$, $L$, $T - t_0$ and the coefficients. This is part of the proof below.

## In plain words

A multistep method computes the next value from several earlier values. For such a method to work, two separate things must hold. First, the formula must fit the equation: put the exact solution into it and the mismatch must vanish fast enough as the step shrinks. Second, the formula must not create its own runaway behaviour: on the trivial equation whose solution is constant, it must not let small disturbances in the starting values grow without limit. The theorem says that these two conditions are exactly what is needed. If both hold, the method gives the right answer as the step goes to zero, on every reasonable problem. If either fails, there is a problem on which it gives the wrong answer or blows up.

## Proof

Norms on $\mathbb{R}^d$ are any fixed norm $\|\cdot\|$; on $\mathbb{R}^{kd}$, written as $k$ blocks, we use $\|E\| = \max_i\|E_i\|$. For a $k \times k$ matrix $M$, the operator norm of $M \otimes I_d$ in this norm is at most $\|M\|_\infty = \max_i\sum_l|M_{il}|$, since block $i$ of $(M \otimes I_d)E$ is $\sum_l M_{il}E_l$.

**Lemma 1 (root condition and bounded powers).** Let $C$ be the companion matrix of $\rho$, the $k \times k$ matrix with first row $(-\alpha_{k-1}, \ldots, -\alpha_0)$, ones on the subdiagonal and zeros elsewhere. Then $\Gamma = \sup_{m \ge 0}\|C^m\|_\infty$ is finite if and only if $\rho$ satisfies the root condition.

*Proof.* The characteristic polynomial of $C$ is $\rho$, so its eigenvalues are the roots of $\rho$. A companion matrix is nonderogatory: for each eigenvalue $\zeta$, the matrix $C - \zeta I$ has rank $k - 1$ (deleting its first row and last column leaves a triangular matrix with ones on the diagonal), so $\zeta$ has exactly one Jordan block, whose size is the multiplicity of $\zeta$ as a root. The powers of a Jordan block $J$ of size $m$ for $\zeta$ have entries $\binom{n}{i}\zeta^{n-i}$ for $0 \le i < m$. They are bounded in $n$ iff $|\zeta| < 1$, or $|\zeta| = 1$ and $m = 1$. With $C = PJP^{-1}$, $\|C^n\| \le \|P\|\,\|P^{-1}\|\,\|J^n\|$ and $\|J^n\| \le \|P^{-1}\|\,\|P\|\,\|C^n\|$, so $C^n$ is bounded iff all Jordan blocks have bounded powers, which is the root condition. $\square$

**Lemma 2 (discrete Gronwall).** If $a_n \ge 0$ and $a_n \le M + Kh\sum_{m=0}^{n-1}a_m$ for $n = 0, 1, \ldots, N$, with $M, K \ge 0$, then $a_n \le M(1 + Kh)^n \le Me^{Knh}$.

*Proof.* Let $s_n = M + Kh\sum_{m<n}a_m$, so $a_n \le s_n$, $s_0 = M$, and $s_{n+1} = s_n + Kha_n \le (1 + Kh)s_n$. Induction gives $s_n \le M(1 + Kh)^n$, and $1 + x \le e^x$. $\square$

**Lemma 3 (consistency gives local error $o(h)$).** Let $y$ be the exact solution on $[t_0, T]$ and $\delta_{n+k} = \sum_j\alpha_j y(t_{n+j}) - h\sum_j\beta_j y'(t_{n+j})$ for $t_{n+k} \le T$. If the method is consistent, then $\|\delta_{n+k}\| \le A\,h\,\omega(kh)$ with $A = \sum_j j|\alpha_j| + \sum_j|\beta_j|$ and $\omega$ the modulus of continuity of $y'$ on $[t_0, T]$, so $\max_n\|\delta_{n+k}\|/h \to 0$. If $y \in C^{p+1}$ and the method has order $p$, then $\|\delta_{n+k}\| \le Ch^{p+1}$.

*Proof.* $y' = f(t, y(t))$ is continuous on the compact interval, hence uniformly continuous. Write $t = t_n$. By the mean value form of the integral, $y(t + jh) = y(t) + jh\,y'(t) + r_j$ with $r_j = \int_t^{t+jh}(y'(s) - y'(t))\,ds$, so $\|r_j\| \le jh\,\omega(jh)$, and $y'(t + jh) = y'(t) + s_j$ with $\|s_j\| \le \omega(jh)$. Then

$$\delta_{n+k} = \rho(1)\,y(t) + h(\rho'(1) - \sigma(1))\,y'(t) + \sum_j\alpha_j r_j - h\sum_j\beta_j s_j.$$

The first two terms vanish by consistency, and the rest is at most $h\,\omega(kh)A$. The order-$p$ statement is the definition of order, with $C$ from the Taylor remainder. $\square$

**Sufficiency.** Assume consistency and zero-stability. Let $e_n = y(t_n) - y_n$, and take $h \le h_0$ with $h_0\Gamma L B \le \tfrac12$, where $B = \sum_j|\beta_j|$ (this also gives $h|\beta_k|L < 1$, since $\Gamma \ge \|C^0\|_\infty = 1$). Subtracting the method from the identity that defines $\delta_{n+k}$:

$$\sum_{j=0}^{k}\alpha_j e_{n+j} = h g_n + \delta_{n+k}, \qquad g_n = \sum_j\beta_j\big(f(t_{n+j}, y(t_{n+j})) - f(t_{n+j}, y_{n+j})\big), \quad \|g_n\| \le LB\max_{0 \le j \le k}\|e_{n+j}\|.$$

Stack $E_n = (e_{n+k-1}, \ldots, e_n)$. The recurrence reads $E_{n+1} = (C \otimes I_d)E_n + u\otimes(hg_n + \delta_{n+k})$, with $u = (1, 0, \ldots, 0)^T$. Unrolling,

$$E_n = (C^n \otimes I_d)E_0 + \sum_{m=0}^{n-1}(C^{n-1-m}\otimes I_d)\big(u \otimes (hg_m + \delta_{m+k})\big).$$

By Lemma 1 every power has norm at most $\Gamma$. The values $e_{m}, \ldots, e_{m+k}$ are blocks of $E_m$ and $E_{m+1}$, so $\|g_m\| \le LB(\|E_m\| + \|E_{m+1}\|)$. Let $\Delta = \max_m\|\delta_{m+k}\|$, the maximum over the steps with $t_{m+k} \le T$. For $n$ with $t_{n+k-1} \le T$, using $nh \le T - t_0$,

$$\|E_n\| \le \Gamma\|E_0\| + \Gamma\frac{(T - t_0)}{h}\Delta + \Gamma hLB\Big(\|E_n\| + 2\sum_{m=0}^{n-1}\|E_m\|\Big).$$

Since $\Gamma hLB \le \tfrac12$, moving the $\|E_n\|$ term to the left and multiplying by 2 gives $\|E_n\| \le M + 4\Gamma LBh\sum_{m<n}\|E_m\|$ with $M = 2\Gamma\|E_0\| + 2\Gamma(T - t_0)\Delta/h$. Lemma 2 gives

$$\max_{t_n \le T}\|e_n\| \le \Big(2\Gamma\eta(h) + 2\Gamma(T - t_0)\frac{\Delta}{h}\Big)e^{4\Gamma LB(T - t_0)}.$$

By Lemma 3, $\Delta/h \to 0$, and $\eta(h) \to 0$ by assumption, so the method converges. If $\Delta \le Ch^{p+1}$ and $\eta(h) \le C_0h^p$, the right-hand side is at most $2\Gamma(C_0 + (T - t_0)C)e^{4\Gamma LB(T - t_0)}h^p$, which is the quantitative form.

**Necessity of zero-stability.** Assume the method is convergent. Apply it to $y' = 0$ in $\mathbb{R}^2$ with $y(t_0) = 0$, so $y \equiv 0$ and the method reduces to $\sum_j\alpha_jy_{n+j} = 0$. Identify $\mathbb{R}^2$ with $\mathbb{C}$. If $\rho(\zeta) = 0$ with $|\zeta| > 1$, then $y_n = h\zeta^n$ solves the recurrence, its starting values have $\eta(h) \le h|\zeta|^{k}\to 0$, and at $n = N = (T - t_0)/h$ it has $|y_N| = h|\zeta|^{N} \to \infty$. If $\zeta$ is a root of modulus 1 with multiplicity at least 2, then $\rho(\zeta) = \rho'(\zeta) = 0$ and $y_n = hn\zeta^n$ solves the recurrence, since $\sum_j\alpha_j(n + j)\zeta^{n+j} = \zeta^n(n\rho(\zeta) + \zeta\rho'(\zeta)) = 0$. Its starting values have $\eta(h) \le kh \to 0$, but $|y_N| = Nh = T - t_0$ does not tend to 0. Both contradict convergence, so the root condition holds.

**Necessity of consistency.** Assume convergence, so the root condition holds. (i) Apply the method to $y' = 0$, $y(t_0) = 1$, with exact starting values. Fix $T$ and let $n = N - k$. Convergence gives $y_{n+j} \to 1$ for each $j \le k$, and $\sum_j\alpha_jy_{n+j} = 0$ for every $h$, so $\rho(1) = \sum_j\alpha_j = 0$. (ii) Apply it to $y' = 1$, $y(t_0) = 0$, exact solution $y = t - t_0$, with exact starting values $y_i = ih$. The recurrence is $\sum_j\alpha_jy_{n+j} = h\sigma(1)$. Since 1 is a simple root of $\rho$, $\rho'(1) \ne 0$. Let $K = \sigma(1)/\rho'(1)$. The sequence $z_n = nhK$ solves the recurrence, because $\sum_j\alpha_j(n + j)hK = hK(n\rho(1) + \rho'(1)) = h\sigma(1)$. The difference $w_n = y_n - z_n$ solves the homogeneous recurrence with starting values $w_i = ih(1 - K)$, so by Lemma 1 $|w_n| \le \Gamma kh|1 - K| \to 0$. Hence $y_N \to K(T - t_0)$, and convergence forces $K = 1$, that is $\rho'(1) = \sigma(1)$. $\blacksquare$

## Consequences

- **One-step methods.** A one-step method has $\rho(\zeta) = \zeta - 1$, which always satisfies the root condition, so for Runge-Kutta methods consistency alone gives convergence (the analogous proof is on the page [Euler method](/euler-method/) and in HNW I, Section II.3).
- **Order of the global error.** With order $p$ and starting values accurate to $O(h^p)$, the [global error](/global-error/) is $O(h^p)$. A starting procedure of order $p - 1$ suffices, since its local errors $O(h^{p})$ occur only $k - 1$ times.
- **Order limits.** Zero-stability restricts the order: a zero-stable $k$-step method has order at most $k + 1$ for $k$ odd, $k + 2$ for $k$ even, and $k$ if it is explicit ([first Dahlquist barrier](/dahlquist-barrier/)).
- **Standard families.** All [Adams-Bashforth](/adams-bashforth-methods/) and [Adams-Moulton](/adams-moulton-methods/) methods have $\rho(\zeta) = \zeta^k - \zeta^{k-1}$ and converge. The [BDF methods](/backward-differentiation-formulas/) are zero-stable for $k \le 6$ and not for $k \ge 7$, so BDF7 does not converge.
- **The template for PDEs.** "Consistency plus stability is equivalent to convergence" is also the [Lax equivalence theorem](/lax-equivalence-theorem/) for linear difference schemes, published the same year.

## Tightness

Each hypothesis is needed, and the conclusion is no stronger than stated.

**Consistent but not zero-stable.** The explicit two-step method $y_{n+2} + 4y_{n+1} - 5y_n = h(4f_{n+1} + 2f_n)$ has order 3, the highest order of any explicit two-step method, but $\rho(\zeta) = (\zeta - 1)(\zeta + 5)$. On $y' = y$, $y(0) = 1$, with exact starting values $y_1 = e^h$, the error at $t = 1$ is $2.8$ for $h = 0.1$, $1.6 \cdot 10^{6}$ for $h = 0.05$, $9.3 \cdot 10^{18}$ for $h = 0.025$ and $5.2 \cdot 10^{45}$ for $h = 0.0125$: the local errors are $O(h^4)$, and the factor $5^n$ amplifies them.

**Zero-stable but not consistent.** The method $y_{n+1} - y_n = 2hf_n$ has $\rho(1) = 0$ and $\rho'(1) = 1 \ne 2 = \sigma(1)$. On $y' = 1$, $y(0) = 0$ it gives $y_n = 2t_n$ for every $h$, so $y(1) = 1$ is approximated by $2$. In general the argument in the necessity proof shows that a zero-stable method with $\rho(1) = 0$ converges to the solution of $y' = Kf$ with $K = \sigma(1)/\rho'(1)$.

**Convergent does not mean stable for long times.** The explicit midpoint rule $y_{n+2} - y_n = 2hf_{n+1}$ is consistent of order 2 and zero-stable (roots $\pm 1$, both simple), so it converges. On $y' = -y$ with $y_1 = e^{-h}$, at $t = 1$ it gives $0.36867$ ($h = 0.1$) and $0.36806$ ($h = 0.05$) against $0.36788$. At $t = 20$ it gives $3.5 \cdot 10^{4}$ and $4.8 \cdot 10^{3}$ against $2.1 \cdot 10^{-9}$: the root near $-1$ of $\rho - z\sigma$ has modulus about $1 + h$, which multiplies the starting error by about $e^{t}$. Convergence is a statement for $h \to 0$ at fixed $T$; behaviour at fixed $h$ over long times is the subject of [absolute stability](/absolute-stability/).

**The Lipschitz hypothesis.** The proof uses a global Lipschitz constant on $[t_0, T] \times \mathbb{R}^d$. For locally Lipschitz $f$ the same conclusion holds on a neighbourhood of the solution once $h$ is small enough that the numbers stay in it, by the usual localization argument.

## History

Germund Dahlquist proved the theorem in his 1956 paper in Mathematica Scandinavica, which also introduced the root condition and the order bound now called the first Dahlquist barrier. The proof via the companion matrix and a discrete Gronwall lemma is the form given by Henrici in his 1962 book and in HNW I, Section III.4. Lax and Richtmyer published the corresponding theorem for linear difference schemes for PDEs in 1956.

## References
