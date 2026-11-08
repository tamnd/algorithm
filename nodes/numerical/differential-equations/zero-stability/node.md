---
tag: RDCQJ6
kind: definition
slug: zero-stability
name: Zero-stability
aliases:
- zero stability
- root condition
- D-stability
area: numerical/differential-equations
level: core
summary: "A multistep method is zero-stable if all roots of ρ lie in the closed unit disk, those on the circle simple. Perturbations then stay bounded as h -> 0; with consistency, it converges."
prereqs: [linear-multistep-methods, ode-initial-value-problem]
see_also: [consistency, dahlquist-equivalence-theorem, dahlquist-barrier, stability-region, backward-differentiation-formulas, global-error, lax-equivalence-theorem, absolute-stability]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section III.3 (stability and the root condition, the first Dahlquist barrier), Section III.4 (convergence of multistep methods)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Section 6.4 (zero-stability of linear multistep methods, the root condition, examples)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 2 (multistep methods, the root condition and the Dahlquist equivalence theorem)
  - paper: "Germund Dahlquist, Convergence and stability in the numerical integration of ordinary differential equations, Mathematica Scandinavica 4 (1956) 33-53"
    locator: the root condition and the equivalence of convergence with stability and consistency
---

Zero-stability is the property of a numerical method for $y' = f(t, y)$ that small perturbations in the starting values and in each step change the computed solution on a fixed interval $[t_0, T]$ by a bounded multiple of the perturbations, uniformly as $h \to 0$. For one-step methods it holds automatically. For [linear multistep methods](/linear-multistep-methods/) it reduces to a condition on the roots of the first characteristic polynomial $\rho$, and together with [consistency](/consistency/) it is exactly what is needed for convergence ([Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/)).

## Definition

A linear $k$-step method is
$$\sum_{j=0}^{k} \alpha_j y_{n+j} = h \sum_{j=0}^{k} \beta_j f(t_{n+j}, y_{n+j}), \qquad \alpha_k \ne 0,$$
with characteristic polynomials $\rho(\zeta) = \sum_j \alpha_j \zeta^j$ and $\sigma(\zeta) = \sum_j \beta_j \zeta^j$.

**Root condition.** The method satisfies the root condition, and is called **zero-stable**, if every root $\zeta$ of $\rho$ satisfies $|\zeta| \le 1$, and every root with $|\zeta| = 1$ is simple.

Equivalently, every solution of the difference equation $\sum_j \alpha_j y_{n+j} = 0$, which is the method applied to $y' = 0$, is bounded for all $n$. The name refers to this: it is the behaviour of the method on the test equation $y' = \lambda y$ at $z = h\lambda = 0$, the point $0$ of the [stability region](/stability-region/).

**Perturbation form.** More generally, a method on a grid with step $h$ is zero-stable if there are $h_0 > 0$ and $K$ such that for all $h \le h_0$, any two sequences produced from starting values $y_0, \ldots, y_{k-1}$ and $z_0, \ldots, z_{k-1}$, with the second one perturbed in step $n$ by $h\delta_n$, satisfy
$$\max_{t_n \le T} \|y_n - z_n\| \le K\Big(\max_{j < k}\|y_j - z_j\| + \max_n \|\delta_n\|\Big).$$
For linear multistep methods with $f$ Lipschitz, this holds if and only if the root condition holds (HNW I, Section III.4). For one-step methods with a Lipschitz increment function, it always holds, by the discrete [Gronwall](/gronwall-inequality/) argument; their $\rho$ is $\zeta - 1$.

**Strong and weak stability.** A zero-stable method is **strongly stable** if $\zeta = 1$ is the only root on the unit circle, and **weakly stable** otherwise.

## Examples and non-examples

- **Adams methods** have $\rho(\zeta) = \zeta^k - \zeta^{k-1}$, with roots 1 and 0 ($k - 1$ times): strongly stable for every $k$.
- **BDF methods.** The roots of $\rho$ other than 1 have largest moduli $0.3333$, $0.4264$, $0.5609$, $0.7087$ and $0.8634$ for $k = 2, \ldots, 6$ (computed). So the [BDF methods](/backward-differentiation-formulas/) of orders 1 to 6 are zero-stable. For $k = 7$ a pair of roots has modulus $1.0222$, so BDF7 and higher are not zero-stable and are never used.
- **Leapfrog (explicit midpoint two-step rule)** $y_{n+2} = y_n + 2hf_{n+1}$ has $\rho(\zeta) = \zeta^2 - 1$, roots $\pm 1$, simple: zero-stable but only weakly. It converges, but on $y' = -y$ the parasitic root near $-(1 + h)$ grows: with exact starting values, the error at $t = 10$ is $1.6$ for $h = 0.1$ and $1.8 \times 10^{-3}$ for $h = 0.01$, while $e^{-10} \approx 4.5 \times 10^{-5}$ (observed).
- **A consistent but unstable method.** The explicit two-step method of order 3
$$y_{n+2} + 4y_{n+1} - 5y_n = h(4f_{n+1} + 2f_n)$$
has $\rho(\zeta) = (\zeta - 1)(\zeta + 5)$, with the root $-5$. On $y' = y$, $y(0) = 1$ with exact starting values, the error at $t = 1$ is $2.8$, $1.6 \times 10^{6}$, $9.3 \times 10^{18}$ and $5.2 \times 10^{45}$ for $h = 0.1, 0.05, 0.025, 0.0125$ (observed): it grows as $h$ shrinks, because rounding and local errors are multiplied by about $5^{1/h}$. Adams-Bashforth 2 on the same problem gives $9.5 \times 10^{-3}$, $2.6 \times 10^{-3}$, $6.8 \times 10^{-4}$.
- **Double root on the circle.** $\rho(\zeta) = (\zeta - 1)^2$ admits the solution $y_n = n$ of the homogeneous recurrence, so perturbations grow like $n = (t_n - t_0)/h$, unbounded as $h \to 0$: not zero-stable.
- **One-step methods** (Euler, Runge-Kutta) are always zero-stable when their increment is Lipschitz.

## Related definitions

- **[Consistency](/consistency/):** $\rho(1) = 0$ and $\rho'(1) = \sigma(1)$, that is, local truncation error $o(1)$ per unit step. Zero-stability plus consistency is equivalent to convergence for linear multistep methods ([Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/)); the PDE analogue is the [Lax equivalence theorem](/lax-equivalence-theorem/).
- **First Dahlquist barrier:** a zero-stable $k$-step method has order at most $k + 1$ for odd $k$, $k + 2$ for even $k$, and $k$ if it is explicit (see [Dahlquist barrier](/dahlquist-barrier/)). The non-example above has order 3 with $k = 2$, beyond the explicit limit, which is why it must fail.
- **[Absolute stability](/absolute-stability/):** the root condition for $\rho - z\sigma$ at a fixed $z \ne 0$; zero-stability is the case $z = 0$, and it governs the limit $h \to 0$ rather than a fixed step.
- **[Global error](/global-error/):** zero-stability is what turns local errors $O(h^{p+1})$ into a global error $O(h^p)$.

## References
