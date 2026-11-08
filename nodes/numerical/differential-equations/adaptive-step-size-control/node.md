---
tag: GB26DW
kind: technique
slug: adaptive-step-size-control
name: Adaptive step-size control
aliases:
- adaptive time stepping
- step size control
- error control
area: numerical/differential-equations
level: core
summary: Choosing each step size from a local error estimate so that the estimate stays below a tolerance. A rejected step is retried with a smaller step.
prereqs: [ode-initial-value-problem, local-truncation-error]
see_also: [embedded-runge-kutta-pairs, bogacki-shampine-method, dormand-prince-method, richardson-extrapolation, adams-bashforth-moulton-method, stiff-ode-problem, dense-output, order-of-accuracy]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.4 (error estimation by extrapolation and by embedded formulas, the automatic step size control, the starting step size) and Section III.7 (variable step size for multistep methods)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.2 (stability of the step size control and the PI controller)
  - paper: "K. Gustafsson, M. Lundh and G. Söderlind, A PI stepsize control for the numerical solution of ordinary differential equations, BIT 28 (1988) 270-287"
    locator: the PI controller and its analysis as a feedback loop
  - paper: "G. Söderlind, Digital filters in adaptive time-stepping, ACM Transactions on Mathematical Software 29 (2003) 1-26"
    locator: the general family of controllers as digital filters
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 4 (error estimation and step size selection for one-step methods) and Chapter 5 (variable step multistep methods)
---

Adaptive step-size control chooses the step size $h_n$ of an integrator for $y' = f(t, y)$ while it runs. After each step, a cheap estimate of the local error is compared with a tolerance given by the user. If the estimate is too large, the step is rejected and repeated with a smaller $h$. In both cases the next $h$ comes from the asymptotic law $\text{error} \approx Ch^q$. The result is small steps where the solution changes fast, large steps where it is smooth, and no need for the user to guess $h$. The estimate can come from an [embedded Runge-Kutta pair](/embedded-runge-kutta-pairs/), from [Richardson extrapolation](/richardson-extrapolation/) (step doubling), or from a predictor-corrector difference such as Milne's device in the [Adams-Bashforth-Moulton method](/adams-bashforth-moulton-method/).

## In plain words

You do not know in advance how large a step the problem allows. So you take a step, estimate how wrong it is, and compare the estimate with how wrong you are willing to be. If the step was too wrong, you throw it away and try again with a shorter one. If it was fine, you keep it. Either way, the estimate tells you roughly how the error depends on the step size, so you can pick the next step to land just inside the tolerance, with a small safety margin. Over a whole run the steps grow where the solution is calm and shrink where it changes quickly.

## When it applies

- The integrator has an error estimate $\mathrm{est}_n$ that behaves like $\Psi(t_n, y_n)h^q + O(h^{q+1})$ for some known $q \ge 1$, with $\Psi$ varying smoothly along the solution. For an embedded pair of orders $p$ and $\hat p = p - 1$, $q = p$. For step doubling of a method of order $p$, $q = p + 1$.
- The solution is smooth enough for this asymptotic form to be meaningful at the step sizes used. Across discontinuities of $f$ or its derivatives the method still works, but only through rejections.
- Accepting a step and repeating a step both cost a known number of evaluations of $f$. The controller pays for one wasted attempt per rejection.
- What is controlled is the local error per step (or per unit step), not the global error $e_n = y(t_n) - y_n$. No general theorem bounds $e_n$ by the tolerance.

## The template

Let $\mathrm{tol}$ stand for the pair $(\mathrm{atol}, \mathrm{rtol})$. Measure the estimate in the scaled norm
$$\mathrm{err}_n = \Big\| \Big(\frac{\mathrm{est}_{n,i}}{\mathrm{atol} + \mathrm{rtol}\cdot\max(|y_{n,i}|, |y_{n+1,i}|)}\Big)_{i=1}^d \Big\|,$$
with the max norm or the root mean square norm. If $\mathrm{err} \approx Ch^q$ and we want $\mathrm{err} = 1$ on the next step, then $h_{\mathrm{new}} = h\,\mathrm{err}^{-1/q}$.

```pseudo id=template
ADAPTIVE(step, t0, y0, T, tol, q)
L1  t ← t0, y ← y0, h ← starting step
L2  while t < T do
L3      h ← min(h, T − t)
L4      (y′, est) ← step(t, y, h)                       ▷ new value and error estimate
L5      err ← scaled norm of est
L6      fac ← min(facmax, max(facmin, 0.9·err^(−1/q)))
L7      if err ≤ 1 then t ← t + h, y ← y′, facmax ← 5      ▷ accept
L8      else facmax ← 1                                   ▷ reject, retry from (t, y)
L9      h ← h·fac
L10 return the accepted points
```

The safety factor $0.9$ (values from 0.8 to 0.95 are common) makes the next attempt aim a little below the tolerance, which reduces rejections. The bounds $\mathrm{facmin} \approx 0.2$ and $\mathrm{facmax} \approx 5$ stop the step from changing too abruptly when the asymptotic law is poor. After a rejection the step is not allowed to grow. The starting step can be guessed from $\|y_0\|$ and $\|f(t_0, y_0)\|$ in the scaled norm, as in Hairer, Nørsett and Wanner, Section II.4. A poor guess costs only a few rejections.

**Why the exponent is $1/q$.** If $\mathrm{err}(h) = Ch^q$ with the same $C$ on two nearby steps, then $\mathrm{err}(h_{\mathrm{new}}) = (h_{\mathrm{new}}/h)^q\,\mathrm{err}(h) = 1$ exactly for $h_{\mathrm{new}} = h\,\mathrm{err}^{-1/q}$. This is a heuristic, because $C$ changes along the solution. That is the reason for the safety factor and for the rejection test.

## Classic examples

- **Embedded pairs.** The [Bogacki-Shampine pair](/bogacki-shampine-method/) uses $q = 3$ and FSAL, so every attempt costs 3 evaluations. On $y' = -2ty^2$, $y(0) = 1$ over $[0, 2]$ with $\mathrm{rtol} = \mathrm{atol} = 10^{-3}$ and $h_0 = 0.5$, the first attempt has $\mathrm{err} = 3.84$. It is rejected, the next $h$ is $0.5 \cdot 0.9 \cdot 3.84^{-1/3} = 0.2875$, and that step is accepted. [Dormand-Prince 5(4)](/dormand-prince-method/) uses $q = 5$ and is the usual default.
- **Step doubling.** Take one step of size $2h$ and two of size $h$ with a method of order $p$. The difference divided by $2^p - 1$ estimates the error of the two small steps, with $q = p + 1$. For [RK4](/classical-runge-kutta-4/) this costs 11 evaluations per pair of steps instead of 8. Adding the estimate to the result gives a value of order $p + 1$. That is [Richardson extrapolation](/richardson-extrapolation/).
- **Predictor-corrector.** In an Adams PECE code the difference between predictor and corrector, multiplied by Milne's factor ($-19/270$ for the fourth-order pair), estimates the local error of the corrector. Changing $h$ in a multistep method also needs new past values, by interpolation or by variable-coefficient formulas (HNW I, Section III.7).
- **Stiff codes.** BDF and Radau codes use the same template. There a rejection or a step change may also force a new Jacobian and a new LU factorization, so the controller avoids small changes of $h$. Many codes keep $h$ fixed unless the proposed factor is outside about $[1, 1.2]$.

## Variations

- **Error per step and error per unit step.** Control $\|\mathrm{est}\| \le \mathrm{tol}$ or $\|\mathrm{est}\|/h \le \mathrm{tol}$. The second changes $q$ to $q - 1$ and is used in some codes so that the global error is roughly proportional to the tolerance.
- **Local extrapolation.** Most modern pairs continue with the higher-order solution. The estimate is then the error of the lower-order one, so it is pessimistic for the value kept.
- **PI controller.** Use $h_{n+1} = h_n\cdot 0.9\cdot\mathrm{err}_n^{-\alpha}\,\mathrm{err}_{n-1}^{\beta}$, with for example $\alpha = 0.7/q$ and $\beta = 0.4/q$. Gustafsson, Lundh and Söderlind (1988) derived it from control theory. It smooths the step sequence and removes the oscillation of the elementary controller near the boundary of the stability region.
- **Digital filters.** Söderlind (2003) treats such controllers as a family of filters on the sequence $\log\mathrm{err}_n$ and chooses their coefficients for smoothness and stability.
- **Order selection.** Variable-order codes (Adams, BDF, extrapolation) estimate the error for several orders and pick the order that allows the largest step per unit of work.

## Pitfalls

- **The tolerance is not the global error.** In the Bogacki-Shampine runs on the example above, the maximum global error is about 6 times the tolerance. This is an observation on one problem, not a guarantee. To check the accuracy, solve again with a smaller tolerance and compare.
- **Stiffness.** For an explicit method on a stiff problem, accuracy would allow large steps but stability does not. The controller then keeps $h$ near the stability boundary, with many rejections and a step count that does not fall when the tolerance is loosened. Bogacki-Shampine needs about 400 steps on $y' = -1000(y - \cos t) - \sin t$ over $[0, 1]$, for $\mathrm{rtol} = 10^{-3}$ and for $\mathrm{rtol} = 10^{-6}$. Switch to an implicit method.
- **Zero scale.** With $\mathrm{atol} = 0$, a component that passes through 0 has scale 0, and the test can never pass. Keep $\mathrm{atol} > 0$.
- **Tolerances near rounding.** With $\mathrm{rtol}$ near $10^{-15}$, the estimate is dominated by rounding errors and the step size collapses. Codes usually raise $\mathrm{rtol}$ to a small multiple of the machine epsilon.
- **Discontinuities.** A jump in $f$ makes the asymptotic law false on the step that contains it. The controller then shrinks $h$ through many rejections until the jump falls inside a tiny step. If the jump time is known, stop the integration there and restart.
- **Wrong exponent.** Using $1/(p + 1)$ for an embedded pair whose estimate is $O(h^p)$ makes the controller react too weakly. It still works, with more rejections.
- **Forcing output points.** Shortening steps to hit many output times wastes work. Use [dense output](/dense-output/) instead.

## Exercises

1. A method has an estimate $\mathrm{err} \approx Ch^4$. A step with $h = 0.1$ gives $\mathrm{err} = 16$. What step does the elementary controller with safety factor 0.9 propose, and is it within $[0.2h, 5h]$?
2. Show that step doubling for a method of order $p$ gives the estimate $(y_{h,h} - y_{2h})/(2^p - 1)$ for the local error of the two half steps, up to $O(h^{p+2})$.
3. Explain why the number of evaluations of an FSAL pair with $s$ stages is $1 + (s - 1)(N + R)$ for $N$ accepted and $R$ rejected steps.
4. For explicit Euler on $y' = \lambda y$ with $\lambda < 0$, estimate the local error with Heun's method. Show that when the tolerance is loose, the accepted step sizes settle near $h = -2/\lambda$, and explain why.
5. Take the PI controller with $\alpha = 0.7/q$ and $\beta = 0.4/q$, and assume $\mathrm{err}_n = Ch_n^q$ exactly with constant $C$. Write the recurrence for $\log h_n$, show that its characteristic roots are $0.8$ and $-0.5$, and conclude that the step sizes converge, with a damped oscillation, to the value where $\mathrm{err} = 0.9^{1/(\alpha - \beta)}$.

## References
