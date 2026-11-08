---
tag: ZZSXKF
kind: technique
slug: linear-multistep-methods
name: Linear multistep methods
aliases:
- multistep methods
- LMM
- k-step methods
area: numerical/differential-equations
level: core
summary: "Advance y' = f(t, y) by a linear relation sum alpha_j y_(n+j) = h sum beta_j f_(n+j) over k past values. One new evaluation of f per step. Converges iff consistent and zero-stable."
prereqs: [ode-initial-value-problem, euler-method, local-truncation-error]
see_also: [adams-bashforth-methods, adams-moulton-methods, backward-differentiation-formulas, dahlquist-equivalence-theorem, zero-stability, dahlquist-barrier, adams-bashforth-moulton-method, absolute-stability]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Chapter III, Sections III.1 to III.4 (classical linear multistep formulas, local error and order conditions, stability and the first Dahlquist barrier, convergence)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 2 (multistep methods, the Adams method, order and convergence, backward differentiation formulae)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 4 (linear multistep methods)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (linear multistep methods), Chapter 6 (zero-stability and convergence) and Chapter 7 (absolute stability)
  - paper: doi:10.7146/math.scand.a-10454
    title: Germund Dahlquist, Convergence and stability in the numerical integration of ordinary differential equations, Mathematica Scandinavica 4 (1956) 33-53
---

A linear multistep method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$ by a linear relation between the last $k$ values $y_{n}, \dots, y_{n+k-1}$, the new value $y_{n+k}$ and the slopes $f_{n+j} = f(t_{n+j}, y_{n+j})$: $\sum_{j=0}^{k} \alpha_j y_{n+j} = h \sum_{j=0}^{k} \beta_j f_{n+j}$. Because it reuses old slopes, it needs only one new evaluation of $f$ per step at any order. The family contains [Euler's method](/euler-method/), the [Adams-Bashforth](/adams-bashforth-methods/) and [Adams-Moulton methods](/adams-moulton-methods/) and the [backward differentiation formulas](/backward-differentiation-formulas/). A method converges if and only if it is consistent and [zero-stable](/zero-stability/) ([Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/)).

## In plain words

A one-step method forgets the past: at each step it asks the equation for new directions, often several times. A multistep method keeps a short memory of the last few points and directions. It fits a smooth curve through what it remembers and uses that curve to guess the next point. So it needs to ask the equation only once per step.

The memory brings two problems. At the start there is no past, so the first few points must come from another method. And a bad choice of weights can make an old error echo and grow from step to step, even when each single step looks accurate. A test on the weights tells which methods are safe.

## When it applies

- The problem is $y' = f(t, y)$ with $f$ continuous and Lipschitz in $y$, and the solution is smooth enough for the order wanted ($y \in C^{p+1}$ for order $p$).
- An evaluation of $f$ is expensive, so one evaluation per step is worth the bookkeeping. Large nonstiff systems from celestial mechanics and the [method of lines](/method-of-lines/) are typical.
- The step size is constant, or changes slowly. Each change of $h$ needs new coefficients or an interpolation of the past values.
- For stiff problems the implicit members, above all the [BDF](/backward-differentiation-formulas/), apply with Newton's method for the implicit equation.
- It does not apply well to problems with frequent discontinuities in $f$ or in its derivatives, since each one forces a restart from a one-step method.

## The template

**Notation.** Step size $h$, grid $t_n = t_0 + nh$, values $y_n \approx y(t_n)$, slopes $f_n = f(t_n, y_n)$. A $k$-step method is given by real numbers $\alpha_0, \dots, \alpha_k$ and $\beta_0, \dots, \beta_k$ with $\alpha_k = 1$ and $|\alpha_0| + |\beta_0| > 0$, or equivalently by the characteristic polynomials

$$\rho(\zeta) = \sum_{j=0}^{k} \alpha_j \zeta^j, \qquad \sigma(\zeta) = \sum_{j=0}^{k} \beta_j \zeta^j.$$

The method is explicit when $\beta_k = 0$ and implicit otherwise.

```pseudo id=main
LMM(f, t0, y0, T, h, α, β, START)
L1  N ← number of steps from t0 to T          ▷ the grid must be uniform
L2  y_1, …, y_{k−1} ← START(f, t0, y0, h)     ▷ hole: starting values of order p, e.g. a Runge-Kutta method
L3  f_j ← f(t_j, y_j) for j = 0, …, k − 1
L4  for n ← 0 to N − k do
L5      r ← h Σ_{j<k} β_j f_{n+j} − Σ_{j<k} α_j y_{n+j}      ▷ the known part
L6      if β_k = 0 then y_{n+k} ← r                           ▷ explicit
L7      else solve y_{n+k} − h β_k f(t_{n+k}, y_{n+k}) = r     ▷ hole: fixed-point or Newton iteration
L8      f_{n+k} ← f(t_{n+k}, y_{n+k})
L9      drop y_n and f_n                                        ▷ keep only the last k values
L10 return y_N
```

**Order.** The [local truncation error](/local-truncation-error/) is $\delta_{n+k} = \sum_j \alpha_j y(t_{n+j}) - h\sum_j \beta_j y'(t_{n+j})$. The method has order $p$ if and only if $\rho(e^h) - h\sigma(e^h) = O(h^{p+1})$ as $h \to 0$, or equivalently

$$\sum_{j} \alpha_j = 0, \qquad \sum_j j^q \alpha_j = q \sum_j j^{q-1} \beta_j \quad (q = 1, \dots, p).$$

**Consistency** is order at least 1: $\rho(1) = 0$ and $\rho'(1) = \sigma(1)$.

**Zero-stability (the root condition).** All roots of $\rho$ satisfy $|\zeta| \le 1$, and the roots with $|\zeta| = 1$ are simple. This is the stability of the method on $y' = 0$, where it reduces to the linear recurrence $\sum_j \alpha_j y_{n+j} = 0$ with solutions $\zeta^n$ (and $n\zeta^n$ for double roots).

**Convergence.** If $f$ is continuous and Lipschitz in $y$, the method is consistent and zero-stable, and the starting errors tend to 0, then $\max_{t_n \le T} \|y(t_n) - y_n\| \to 0$ as $h \to 0$. With order $p$, a $C^{p+1}$ solution and starting errors $O(h^p)$, the global error is $O(h^p)$. Conversely, a convergent method is consistent and zero-stable. This is Dahlquist's theorem of 1956, proved on the page of the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/).

**Absolute stability.** On $y' = \lambda y$ with $z = h\lambda$ the method becomes $\sum_j (\alpha_j - z\beta_j) y_{n+j} = 0$, with the stability polynomial $\pi(\zeta; z) = \rho(\zeta) - z\sigma(\zeta)$. The [stability region](/stability-region/) is the set of $z$ for which all roots of $\pi(\cdot; z)$ satisfy $|\zeta| \le 1$, with simple roots on the unit circle. Its boundary lies on the curve $z(\theta) = \rho(e^{i\theta}) / \sigma(e^{i\theta})$, $0 \le \theta \le 2\pi$ (the boundary locus method).

**Cost.** An explicit method costs one evaluation of $f$ per step. An implicit method costs one evaluation per fixed-point iteration, which converges when $h |\beta_k| L < 1$; on stiff problems a Newton iteration is used instead, with Jacobian evaluations and linear solves with $I - h\beta_k J$. A predictor-corrector pair in PECE mode costs two evaluations per step. The storage is $k$ past values and slopes, $O(k d)$.

**Barriers.** A zero-stable $k$-step method has order at most $k + 1$ when $k$ is odd and $k + 2$ when $k$ is even, and at most $k$ when it is explicit (first Dahlquist barrier, HNW I, Section III.3). An A-stable method has order at most 2 (second [Dahlquist barrier](/dahlquist-barrier/)).

## Classic examples

**The main families.** For each, $\rho$ and $\sigma$ are:

| family | $\rho(\zeta)$ | $\sigma(\zeta)$ | order with $k$ steps | built by |
|---|---|---|---|---|
| [Adams-Bashforth](/adams-bashforth-methods/) | $\zeta^k - \zeta^{k-1}$ | degree $k - 1$ | $k$ | integrating the interpolant of $f_n, \dots, f_{n+k-1}$ |
| [Adams-Moulton](/adams-moulton-methods/) | $\zeta^k - \zeta^{k-1}$ | degree $k$ | $k + 1$ | integrating the interpolant of $f_n, \dots, f_{n+k}$ |
| [BDF](/backward-differentiation-formulas/) | degree $k$ | $\beta_k \zeta^k$ | $k$ | differentiating the interpolant of $y_n, \dots, y_{n+k}$ |
| Nyström, Milne-Simpson | $\zeta^k - \zeta^{k-2}$ | degree $k - 1$ or $k$ | $k$, and $k + 1$ for Milne-Simpson ($4$ for $k = 2$) | integrating over two steps |

Euler's method is $k = 1$, $\rho = \zeta - 1$, $\sigma = 1$. The trapezoidal rule is $\rho = \zeta - 1$, $\sigma = (\zeta + 1)/2$. Adams methods have $\rho$ with the single root 1 and the root 0 of multiplicity $k - 1$, so they are always zero-stable. The BDF are zero-stable for $k \le 6$ only.

**AB2 in action.** The two-step Adams-Bashforth method $y_{n+2} = y_{n+1} + h(\frac32 f_{n+1} - \frac12 f_n)$, started with one step of [Heun's method](/heuns-method/), on $y' = -2ty^2$, $y(0) = 1$, gives at $T = 1$ the errors $4.106 \cdot 10^{-3}$, $9.962 \cdot 10^{-4}$, $2.446 \cdot 10^{-4}$, $6.055 \cdot 10^{-5}$, $1.506 \cdot 10^{-5}$ for $N = 10, 20, 40, 80, 160$. The observed orders are $2.043$, $2.026$, $2.014$, $2.007$, at one new evaluation per step against two for Heun's method. Its stability interval on the real axis is $[-1, 0]$: at $\theta = \pi$ the boundary locus gives $z = \rho(-1)/\sigma(-1) = 2/(-2) = -1$.

**Consistent but not zero-stable.** The explicit two-step method $y_{n+2} + 4y_{n+1} - 5y_n = h(4f_{n+1} + 2f_n)$ has order 3, the largest for $k = 2$ with $\beta_2 = 0$. But $\rho(\zeta) = (\zeta - 1)(\zeta + 5)$ has the root $-5$. On $y' = -y$, $y(0) = 1$, with the exact starting value $y_1 = e^{-h}$, the errors at $T = 1$ are $3.07 \cdot 10^{-2}$, $7.05$, $4.65 \cdot 10^{6}$, $2.88 \cdot 10^{19}$, $1.67 \cdot 10^{46}$ for $N = 5, 10, 20, 40, 80$. Rounding errors and the local errors excite the parasitic solution $(-5)^n$, so the smaller $h$, the worse the result.

**Weak instability.** The leapfrog method $y_{n+2} = y_n + 2hf_{n+1}$ has $\rho(\zeta) = \zeta^2 - 1$ with the roots $\pm 1$. It is zero-stable and convergent of order 2. But on $y' = -y$ the parasitic root of $\pi(\zeta; z)$ is about $-(1 + h)$, so it grows like $e^{t}$ while the solution decays like $e^{-t}$. At $T = 10$, where $y = 4.54 \cdot 10^{-5}$, the errors for $N = 100, 200, 400$ are $1.62$, $0.217$ and $0.0279$: convergent, with ratios near 8, yet useless for this problem.

## Variations

- **Predictor-corrector methods.** Predict with an explicit method, evaluate, correct with an implicit one, evaluate again (PECE). The [Adams-Bashforth-Moulton method](/adams-bashforth-moulton-method/) is the standard pair. The difference of predictor and corrector estimates the local error (Milne's device).
- **Variable step size and order.** Adams codes use divided differences or the Nordsieck vector $(y_n, h y_n', h^2 y_n''/2, \dots)$ to change $h$ and $k$ cheaply. Codes such as DIFSUB, LSODE and the BDF solvers of MATLAB and SUNDIALS work this way.
- **Methods for second order equations.** For $y'' = g(t, y)$, Störmer's method $y_{n+2} - 2y_{n+1} + y_n = h^2 g_{n+1}$ and its higher-order relatives use $y$ directly; Störmer's method is the position form of [Verlet integration](/verlet-integration/).
- **General linear methods.** Methods with several stages and several steps, which contain both Runge-Kutta and multistep methods as special cases (Butcher, Chapter 5).

## Pitfalls

- **Forgetting zero-stability.** Maximizing the order for a given $k$ gives unstable methods for $k \ge 3$ (for $k \ge 2$ among explicit ones), as the example above shows. Always check the root condition of $\rho$, which can be done in exact arithmetic.
- **Starting values of lower order.** If the starting values have errors $O(h^q)$, the global error is only $O(h^{\min(p, q)})$. Starting AB4 with single Euler steps gives starting errors $O(h^2)$, and so a global error $O(h^2)$.
- **Changing $h$ by just changing the number.** The coefficients are derived for equal spacing. After a change of $h$, the old values must be interpolated to the new grid, or variable-step coefficients must be used.
- **Fixed-point iteration on stiff problems.** The condition $h|\beta_k| L < 1$ forces tiny steps when $L$ is large, which removes the point of an implicit method. Use Newton's method.
- **Weak instability.** Zero-stable methods with several roots of $\rho$ on the unit circle, such as leapfrog and Milne-Simpson, are unstable on $y' = \lambda y$ with $\lambda < 0$ for each $h > 0$.
- **Restarts at discontinuities.** A jump in $f$ invalidates the stored slopes. The method must restart with a one-step method at the jump.

## Exercises

1. Show that $\rho(e^h) - h\sigma(e^h) = O(h^{p+1})$ is equivalent to the conditions $\sum_j j^q \alpha_j = q\sum_j j^{q-1}\beta_j$ for $q \le p$.
2. Derive the two-step Adams-Bashforth method by integrating the linear interpolant of $f_n$ and $f_{n+1}$ over $[t_{n+1}, t_{n+2}]$, and find its error constant $C_3 = 5/12$.
3. Find the explicit two-step method of order 3 and show that it is not zero-stable.
4. Use the boundary locus to show that the stability interval of AB2 on the negative real axis is $[-1, 0]$, and that the BDF2 method is A-stable.
5. Show that the leapfrog method applied to $y' = \lambda y$ with real $\lambda < 0$ has a root of modulus greater than 1 for each $h > 0$.

## References
