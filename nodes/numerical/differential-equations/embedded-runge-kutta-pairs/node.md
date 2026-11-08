---
tag: QCT7V5
kind: concept
slug: embedded-runge-kutta-pairs
name: Embedded Runge-Kutta pairs
aliases:
- embedded pair
- embedded Runge-Kutta method
- Runge-Kutta pair
area: numerical/differential-equations
level: core
summary: "Two Runge-Kutta methods of orders p and p̂ that share all stages and differ only in the weights. The difference of their results estimates the local error at no extra cost in evaluations of f."
prereqs: [runge-kutta-methods, butcher-tableau, local-truncation-error]
see_also: [dormand-prince-method, runge-kutta-fehlberg-method, bogacki-shampine-method, cash-karp-method, adaptive-step-size-control, heuns-method, dense-output, richardson-extrapolation]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.4 (practical error estimation and step size selection; embedded Runge-Kutta formulas, Fehlberg's and Merson's methods, the step size formula), Section II.5 (higher order pairs, Dormand-Prince)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3 (Runge-Kutta methods; error estimation and embedded methods)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 4 (one-step methods; error estimation and control, embedded methods)
  - paper: doi:10.1016/0893-9659(89)90079-7
    title: P. Bogacki and L. F. Shampine, A 3(2) pair of Runge-Kutta formulas, Applied Mathematics Letters 2(4) (1989) 321-325
    locator: the coefficients of the 3(2) FSAL pair
  - paper: doi:10.1016/0771-050X(80)90013-3
    title: J. R. Dormand and P. J. Prince, A family of embedded Runge-Kutta formulae, Journal of Computational and Applied Mathematics 6(1) (1980) 19-26
    locator: the 5(4) pairs and the case for propagating the higher-order result
---

An embedded Runge-Kutta pair is a [Runge-Kutta method](/runge-kutta-methods/) with one set of stages and two weight vectors, $b$ and $\hat b$, that give two results of different orders $p$ and $\hat p$. The difference of the two results estimates the [local truncation error](/local-truncation-error/) of the lower-order one, and it costs no extra evaluation of $f$. This estimate is what lets a code choose the step size $h$ automatically ([adaptive step-size control](/adaptive-step-size-control/)). The pair is written $p(\hat p)$, for example 5(4) for the [Dormand-Prince method](/dormand-prince-method/).

## In plain words

To control an error you must first measure it, but the true answer is unknown. One way is to compute each step twice with different methods and compare. If one method is much more accurate than the other, the difference between the two answers is close to the error of the weaker one.

Doing this with two separate methods doubles the work. An embedded pair avoids this. Its two methods use the same intermediate slope evaluations and only add them up with different weights. So the second answer, and with it the error estimate, comes almost for free. A code then shortens the step when the estimate is too large and lengthens it when the estimate is small.

## The idea

**Definition.** An embedded pair is a [Butcher tableau](/butcher-tableau/) $(A, b, c)$ with $s$ stages together with a second weight vector $\hat b$. From $(t_n, y_n)$ and a step $h$ it computes the stages $k_i = f(t_n + c_i h, y_n + h\sum_j a_{ij}k_j)$, $i = 1, \ldots, s$, and the two results

$$y_{n+1} = y_n + h\sum_{i=1}^{s} b_i k_i, \qquad \hat y_{n+1} = y_n + h\sum_{i=1}^{s}\hat b_i k_i.$$

The method $(A, b, c)$ has order $p$, the method $(A, \hat b, c)$ has order $\hat p$, and $p \ne \hat p$ (usually $|p - \hat p| = 1$). The **error estimate** is

$$\mathrm{est} = y_{n+1} - \hat y_{n+1} = h\sum_{i=1}^{s}(b_i - \hat b_i)k_i.$$

**Why the estimate works (asymptotic).** Let $q = \min(p, \hat p)$, let $f$ be $C^{q+2}$, and start the step from an exact value $y_n = y(t_n)$. The local error of the order-$q$ result is $C(t_n)h^{q+1} + O(h^{q+2})$ with a principal error vector $C(t_n)$, and the local error of the other result is $O(h^{q+2})$. Subtracting, the estimate equals the local error of the lower-order result up to $O(h^{q+2})$. So $\mathrm{est}/h^{q+1} \to \pm C(t_n)$ as $h \to 0$. This is an asymptotic statement: for a finite $h$ it can fail, for example near a point where $C(t_n)$ vanishes, and it says nothing about the [global error](/global-error/).

**Local extrapolation.** If $p > \hat p$, the code may continue with the higher-order result $y_{n+1}$ while the estimate measures the error of $\hat y_{n+1}$. This is local extrapolation. The estimate is then pessimistic for the value kept. [Runge-Kutta-Fehlberg](/runge-kutta-fehlberg-method/) 4(5) continues with the order-4 value, [Dormand-Prince](/dormand-prince-method/) 5(4) with the order-5 value.

**Step size selection.** With a scaled norm $\mathrm{err} = \|\mathrm{est}\|_{\mathrm{sc}}$, where component $i$ is divided by $\mathrm{Atol} + \mathrm{Rtol}\max(|y_{n,i}|, |y_{n+1,i}|)$, the step is accepted when $\mathrm{err} \le 1$. Since $\mathrm{err} \approx K h^{q+1}$, the step that would give $\mathrm{err} = 1$ is $h\,\mathrm{err}^{-1/(q+1)}$, and codes use

$$h_{\text{new}} = h\cdot\min\left(\mathrm{fac}_{\max}, \max\left(\mathrm{fac}_{\min}, \mathrm{fac}\cdot\mathrm{err}^{-1/(q+1)}\right)\right)$$

with a safety factor $\mathrm{fac}$ near $0.9$ and limits such as $0.2$ and $5$ (HNW I, Section II.4).

**First same as last (FSAL).** If the last row of $A$ equals $b$ and $c_s = 1$, the last stage is $f(t_n + h, y_{n+1})$, which is the first stage of the next step. An accepted step then costs $s - 1$ evaluations.

**Design constraints.** Both weight vectors must satisfy the [order conditions](/butcher-order-conditions/) of their order for the same $A$ and $c$. A pair needs at least as many stages as the higher-order method alone, and often one more. An explicit 5(4) pair needs 6 stages, the same as the minimum for order 5 alone, and Dormand-Prince uses a seventh stage to gain FSAL and smaller error constants.

## Examples

**Heun-Euler 2(1).** Two stages, $c = (0, 1)$, $a_{21} = 1$, $b = (\tfrac12, \tfrac12)$ ([Heun's method](/heuns-method/), order 2) and $\hat b = (1, 0)$ ([Euler](/euler-method/), order 1). The estimate is $\mathrm{est} = \tfrac{h}{2}(k_2 - k_1)$. On $y' = -2ty^2$ with one step from the exact value $y(1) = \tfrac12$:

| $h$ | est | true local error of Euler | ratio | est$/h^2$ | local error of Heun |
|---|---|---|---|---|---|
| 0.2 | $1.1600 \cdot 10^{-2}$ | $9.8361 \cdot 10^{-3}$ | 1.1793 | 0.2900 | $-1.76 \cdot 10^{-3}$ |
| 0.1 | $2.7250 \cdot 10^{-3}$ | $2.4887 \cdot 10^{-3}$ | 1.0950 | 0.2725 | $-2.36 \cdot 10^{-4}$ |
| 0.05 | $6.5469 \cdot 10^{-4}$ | $6.2426 \cdot 10^{-4}$ | 1.0487 | 0.2619 | $-3.04 \cdot 10^{-5}$ |
| 0.025 | $1.6006 \cdot 10^{-4}$ | $1.5620 \cdot 10^{-4}$ | 1.0247 | 0.2561 | $-3.86 \cdot 10^{-6}$ |
| 0.0125 | $3.9545 \cdot 10^{-5}$ | $3.9059 \cdot 10^{-5}$ | 1.0124 | 0.2531 | $-4.85 \cdot 10^{-7}$ |

The ratio tends to 1 and $\mathrm{est}/h^2$ tends to $\tfrac12 y''(1) = 0.25$, where $y'' = (6t^2 - 2)/(1 + t^2)^3$. The Heun value itself has a local error of order $h^3$, about 6 to 80 times smaller than the estimate in this range.

**Bogacki-Shampine 3(2).** $c = (0, \tfrac12, \tfrac34, 1)$, $a_{21} = \tfrac12$, $a_{32} = \tfrac34$, last row $(\tfrac29, \tfrac13, \tfrac49)$, with $b = (\tfrac29, \tfrac13, \tfrac49, 0)$ and $\hat b = (\tfrac{7}{24}, \tfrac14, \tfrac13, \tfrac18)$. In exact arithmetic, $b$ gives $\sum b_i = 1$, $\sum b_i c_i = \tfrac12$, $\sum b_i c_i^2 = \tfrac13$, $\sum b_i a_{ij}c_j = \tfrac16$, so it has order 3. For $\hat b$ the first two hold, but the order-3 sums are $\tfrac38$ and $\tfrac{3}{16}$, so it has order 2. It is FSAL: 3 evaluations per step. MATLAB's `ode23` uses it.

**Dormand-Prince 5(4).** Seven stages, FSAL, 6 evaluations per step, order-5 value propagated. See [Dormand-Prince method](/dormand-prince-method/) for the tableau and a traced run.

**Non-example: step doubling.** Taking one step of $2h$ and two steps of $h$ with the same method of order $p$ and comparing gives an estimate by [Richardson extrapolation](/richardson-extrapolation/): the error of the two-step result is about $(y^{(h)} - y^{(2h)})/(2^p - 1)$. With the [classical RK4](/classical-runge-kutta-4/) this costs 11 evaluations per double step, against 6 for an embedded 5(4) pair over a similar distance per step. The idea is the same, but it is not an embedded pair, because the two results do not share stages.

## Where it is used

- Every adaptive explicit Runge-Kutta code: [Dormand-Prince](/dormand-prince-method/) (MATLAB `ode45`, SciPy `RK45`), [Bogacki-Shampine](/bogacki-shampine-method/) (`ode23`), [Runge-Kutta-Fehlberg](/runge-kutta-fehlberg-method/), [Cash-Karp](/cash-karp-method/).
- [Adaptive step-size control](/adaptive-step-size-control/): the estimate feeds the step size formula.
- [Dense output](/dense-output/): pairs are often designed together with a continuous extension that reuses the same stages.
- Implicit and Rosenbrock codes use the same idea with an embedded formula of lower order, for example in [Rosenbrock methods](/rosenbrock-methods/) and [Radau IIA](/radau-iia-methods/) codes.
- Stiffness detection: the ratio of successive estimates, or a comparison of two stage differences, signals that stability rather than accuracy limits $h$.

## References
