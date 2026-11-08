---
tag: Q9558D
kind: concept
slug: global-error
name: Global error
aliases:
- global discretization error
- global truncation error
- accumulated error
area: numerical/differential-equations
level: core
summary: "The gap e_n = y(t_n) - y_n between exact and numerical solution at a grid point. It collects all local errors, each carried forward by the problem. Order p means e_n = O(h^p) on bounded intervals."
prereqs: [ode-initial-value-problem, local-truncation-error, lipschitz-condition]
see_also: [order-of-accuracy, gronwall-inequality, dahlquist-equivalence-theorem, zero-stability, richardson-extrapolation, adaptive-step-size-control, euler-method, stiff-ode-problem]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.3 (convergence of Runge-Kutta methods, the error propagation picture called Lady Windermere's fan, the global error bound), Section II.8 (asymptotic expansion of the global error)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1 (Euler's method and its convergence)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (the initial value problem, local truncation error and convergence of one-step methods), Chapter 6 (zero-stability and convergence of multistep methods)
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Chapter X (perturbation theory of integrable systems; linear error growth of symplectic methods)
---

The global error of a numerical method for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, at the grid point $t_n$ is $e_n = y(t_n) - y_n$, the difference between the exact solution and the computed value. It is what a user wants to be small, but a code cannot measure it directly. It is made of all the [local truncation errors](/local-truncation-error/) committed at earlier steps, each one carried forward to $t_n$ by the differential equation itself. A method has [order](/order-of-accuracy/) $p$ when $\max_n\|e_n\| = O(h^p)$ on every bounded interval for smooth problems.

## In plain words

At each step, a numerical method makes a small mistake, because it only approximates the true curve over that step. The next step starts from a slightly wrong point, so it follows a slightly different true curve, and it makes its own mistake on top. The global error is the total gap between the computed answer and the true answer after many steps. Whether the gap stays small depends on the problem. If nearby solutions move apart, old mistakes grow as they travel. If nearby solutions come together, old mistakes shrink. Codes usually control only the mistake of each single step, so the total gap can be larger, or much smaller, than the tolerance the user asked for.

## The idea

**Notation.** Grid $t_n = t_0 + nh$ (or variable steps $h_n$), values $y_n$, local error $\ell_{n+1} = y(t_{n+1}) - \Phi_h(t_n, y(t_n))$, where $\Phi_h$ is one step of a one-step method started from the exact value. The norm $\|\cdot\|$ is any norm on $\mathbb{R}^d$. $L$ is a Lipschitz constant of $f$ in $y$.

**Error propagation.** Write the global error as a telescoping sum. Let $y^{(k)}(t)$ be the exact solution through $(t_k, y_k)$. Then $y(t_n) - y_n = \sum_{k=0}^{n-1}\left(y^{(k)}(t_n) - y^{(k+1)}(t_n)\right)$, with $y^{(0)} = y$ and $y^{(n)}(t_n) = y_n$. Each term is the local error made at step $k+1$, transported from $t_{k+1}$ to $t_n$ by the flow of the equation. HNW I (Section II.3) draws this as a fan of exact solutions. The transport factor is at most $e^{L(t_n - t_{k+1})}$ by the [Gronwall inequality](/gronwall-inequality/).

**The basic bound (proved).** Let a one-step method satisfy $\|\ell_{n+1}\| \le C h_n^{p+1}$ for all steps, and let its increment be Lipschitz in $y$ with constant $\Lambda$, so that two steps from $u$ and $v$ differ by at most $(1 + h\Lambda)\|u - v\|$. Then, with $h = \max_n h_n$,

$$\|e_n\| \le \frac{C h^{p}}{\Lambda}\left(e^{\Lambda(t_n - t_0)} - 1\right).$$

For Euler's method $\Lambda = L$ and $C = \tfrac12\max\|y''\|$ (proof on the page [Euler method](/euler-method/)); for a Runge-Kutta method $\Lambda$ depends on $L$, $h$ and the tableau (HNW I, Section II.3). For [linear multistep methods](/linear-multistep-methods/) the analogous statement needs [zero-stability](/zero-stability/) as well as consistency, which is the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/).

**The bound is often pessimistic.** The factor $e^{\Lambda(t - t_0)}$ assumes that every perturbation grows at the worst rate. When solutions contract, a one-sided Lipschitz constant $\mu$ (with $\langle f(t,u) - f(t,v), u - v\rangle \le \mu\|u - v\|^2$ in the Euclidean norm) can be negative and gives far smaller bounds, as long as $h$ is in the stable range.

**Asymptotic expansion (asymptotic).** If $f$ is smooth enough and the local error is $\ell_{n+1} = d_{p+1}(t_n)h^{p+1} + O(h^{p+2})$ with a smooth principal error function $d_{p+1}$, then for constant steps

$$e_n = h^{p}\, E_p(t_n) + O(h^{p+1}), \qquad E_p'(t) = f_y(t, y(t))\,E_p(t) + d_{p+1}(t), \quad E_p(t_0) = 0$$

(HNW I, Section II.8, sign adapted to $e_n = y(t_n) - y_n$). The leading global error solves the linearized equation forced by the principal local error. This is what makes [Richardson extrapolation](/richardson-extrapolation/) of whole solutions work: with results $y^{(h)}$ and $y^{(h/2)}$ at the same time, $(y^{(h/2)} - y^{(h)})/(2^p - 1)$ estimates the error of $y^{(h/2)}$.

**Local control is not global control.** An adaptive code ([adaptive step-size control](/adaptive-step-size-control/)) keeps each local error estimate below a tolerance. The global error then depends on the propagation factors. The most one can hope for is tolerance proportionality: the global error is roughly proportional to the tolerance, which holds asymptotically for well-designed step size rules but with an unknown constant.

## Examples

**Euler on growth and on decay.** Euler's method on $y' = \lambda y$, $y(0) = 1$, has $y_n = (1 + h\lambda)^n$. Here $d_2(t) = \tfrac12 y''(t) = \tfrac12\lambda^2 e^{\lambda t}$, and the expansion gives $E_1(t) = \tfrac12\lambda^2 t\, e^{\lambda t}$.

| $\lambda$ | $T$ | $e_N$ at $h = 0.1$ | $e_N$ at $h = 0.05$ | $e_N$ at $h = 0.025$ | $e_N/h$ at $h = 0.025$ | $E_1(T)$ |
|---|---|---|---|---|---|---|
| 1 | 1 | $1.2454 \cdot 10^{-1}$ | $6.4984 \cdot 10^{-2}$ | $3.3218 \cdot 10^{-2}$ | 1.3287 | 1.3591 |
| 1 | 10 | $8.2459 \cdot 10^{3}$ | $4.7339 \cdot 10^{3}$ | $2.5484 \cdot 10^{3}$ | $1.0194 \cdot 10^{5}$ | $1.1013 \cdot 10^{5}$ |
| $-1$ | 1 | $1.9201 \cdot 10^{-2}$ | $9.3935 \cdot 10^{-3}$ | $4.6470 \cdot 10^{-3}$ | 0.1859 | 0.1839 |
| $-1$ | 10 | $1.8839 \cdot 10^{-5}$ | $1.0347 \cdot 10^{-5}$ | $5.4196 \cdot 10^{-6}$ | $2.168 \cdot 10^{-4}$ | $2.270 \cdot 10^{-4}$ |

In each row the error halves with $h$ (order 1) and $e_N/h$ approaches $E_1(T)$. On the growing problem the error at $T = 10$ is about $10^5 h$; on the decaying problem it is about $2 \cdot 10^{-4}h$. The Lipschitz bound with $L = 1$ cannot tell the two apart: for $\lambda = -1$, $T = 10$, $h = 0.1$ it gives $\tfrac{h}{2}(e^{10} - 1) \approx 1101$, against an actual error of $1.9 \cdot 10^{-5}$.

**Richardson estimate.** For $\lambda = 1$, $T = 1$, $p = 1$: with $h = 0.1$ and $0.05$, $y^{(0.05)} - y^{(0.1)} = 0.059555$, against the true error $0.064984$ of $y^{(0.05)}$. With $h = 0.05$ and $0.025$, the estimate is $0.031766$ against $0.033218$. The estimate improves as $h$ shrinks, as the expansion predicts.

**Stability decides before accuracy.** Euler on $y' = -50y$, $y(0) = 1$, to $T = 1$: the exact value is $1.9 \cdot 10^{-22}$. With $h = 1/26$ ($h\lambda \approx -1.92$, inside the stability interval $[-2, 0]$) the computed value is $0.125$; with $h = 1/24$ ($h\lambda \approx -2.08$) it is $6.83$; with $h = 0.05$ ($h\lambda = -2.5$) it is $3325$. The three step sizes differ by less than a factor 2 in accuracy. What changes is stability: outside the interval $|1 + h\lambda| > 1$, and every error is multiplied by $|1 + h\lambda|$ at every later step. See [stiff problems](/stiff-ode-problem/).

**Long-time behaviour on Hamiltonian problems.** For integrable Hamiltonian systems, a symplectic method of order $p$ has a global error that grows roughly linearly in $t$, about $C t h^p$, over long intervals, while a general method of the same order has errors growing like $t^2 h^p$ (HLW GNI, Chapter X). See [symplectic integrators](/symplectic-integrators/).

**Non-example: the sum of local errors.** Adding the local errors $\sum_k\|\ell_k\|$ is not the global error. It overestimates it on contracting problems, as in the $\lambda = -1$ rows, and underestimates it on expanding ones, as in the $\lambda = 1$ rows.

## Where it is used

- Convergence proofs: the definition of order and of convergence in the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/) and the [Lax equivalence theorem](/lax-equivalence-theorem/).
- Measuring the observed order of a code by halving $h$ on a problem with known solution, as in the tests of every method page here.
- Global error estimation by [Richardson extrapolation](/richardson-extrapolation/), by solving the variational equation for $E_p$, or by running two codes of different order.
- Choosing a tolerance: since codes control local errors, users judge the global error by rerunning with a tighter tolerance and comparing.

## References
