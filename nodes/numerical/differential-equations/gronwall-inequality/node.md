---
tag: WMW4M1
kind: theorem
slug: gronwall-inequality
name: Gronwall's inequality
aliases:
- Gronwall lemma
- Gronwall-Bellman inequality
- discrete Gronwall inequality
area: numerical/differential-equations
level: advanced
summary: "If u(t) <= alpha(t) + integral of beta u with beta >= 0, then u is bounded by alpha plus a term with exp of the integral of beta. With alpha nondecreasing: u(t) <= alpha(t) exp(integral of beta)."
prereqs: [lipschitz-condition, ode-initial-value-problem]
see_also: [picard-lindelof-theorem, global-error, euler-method, dahlquist-equivalence-theorem, lax-equivalence-theorem, picard-iteration, local-truncation-error, stiff-ode-problem]
sources:
  - paper: doi:10.2307/1967124
    title: T. H. Gronwall, Note on the derivatives with respect to a parameter of the solutions of a system of differential equations, Annals of Mathematics (2) 20 (1919) 292-296
  - paper: doi:10.1215/S0012-7094-43-01059-2
    title: Richard Bellman, The stability of solutions of linear differential equations, Duke Mathematical Journal 10 (1943) 643-647
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section I.10 (differential inequalities, Gronwall's lemma) and Section II.3 (convergence of one-step methods by a discrete estimate)
  - book: isbn:9780898715101
    title: Philip Hartman, Ordinary Differential Equations, second edition, SIAM Classics in Applied Mathematics, 2002
    locator: Chapter III, Section 1 (Gronwall's inequality)
---

Gronwall's inequality turns an implicit bound of the form "$u$ is at most $\alpha$ plus an integral of $\beta u$" into an explicit bound by an exponential. It is the standard tool for proving uniqueness and continuous dependence for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$ when $f$ is [Lipschitz](/lipschitz-condition/) in $y$. Its discrete form is the step that turns local errors into a bound on the [global error](/global-error/) of a numerical method, with the factor $e^{L(T - t_0)}$ that appears in the convergence theorems of this sub-area.

## Statement

**Theorem (integral form).** Let $u$, $\alpha$, $\beta$ be continuous real functions on $[a, b]$ with $\beta(t) \ge 0$. If

$$u(t) \le \alpha(t) + \int_a^t \beta(s)\, u(s)\, ds \qquad (a \le t \le b),$$

then

$$u(t) \le \alpha(t) + \int_a^t \alpha(s)\,\beta(s)\, \exp\Bigl(\int_s^t \beta(r)\, dr\Bigr) ds \qquad (a \le t \le b).$$

If moreover $\alpha$ is nondecreasing, then $u(t) \le \alpha(t) \exp\bigl(\int_a^t \beta(s)\, ds\bigr)$. In particular, with constants $\alpha$ and $\beta = L \ge 0$: $u(t) \le \alpha\, e^{L (t - a)}$.

**Theorem (differential form).** Let $u$ be differentiable on $[a, b]$ and $\beta$ continuous, with no sign condition on $\beta$. If $u'(t) \le \beta(t)\, u(t)$ on $[a, b]$, then $u(t) \le u(a) \exp\bigl(\int_a^t \beta(s)\, ds\bigr)$.

**Theorem (discrete form).** Let $a_n$, $b_n$ be real numbers and $c_n \ge 0$, for $n \ge 0$. If

$$a_n \le b_n + \sum_{k=0}^{n-1} c_k\, a_k \qquad (n \ge 0),$$

then

$$a_n \le b_n + \sum_{k=0}^{n-1} c_k\, b_k \prod_{j=k+1}^{n-1} (1 + c_j) \qquad (n \ge 0).$$

In the form used for one-step methods: if $E_{n+1} \le (1 + h\Lambda) E_n + \delta$ with $h, \Lambda > 0$ and $\delta \ge 0$, then

$$E_n \le e^{n h \Lambda} E_0 + \delta\, \frac{e^{n h \Lambda} - 1}{h \Lambda}.$$

## In plain words

Suppose a quantity can grow, but at each moment its growth rate is at most a fixed multiple of its own size. Then it can grow at most as fast as an exponential with that rate. The inequality says this exactly, and it also allows a starting bound that changes with time.

For a differential equation the quantity is the distance between two solutions, or between the true solution and a computed one. The equation limits how fast this distance can grow, and the inequality turns that limit into a bound at the final time. The same argument, with sums in place of integrals, follows the error of a computer method step by step.

## Proof

**Integral form.** Let $v(t) = \int_a^t \beta(s) u(s)\, ds$. Then $v$ is $C^1$, $v(a) = 0$ and, by the hypothesis and $\beta \ge 0$,

$$v'(t) = \beta(t) u(t) \le \beta(t)\alpha(t) + \beta(t) v(t).$$

Let $B(t) = \int_a^t \beta(r)\, dr$. Then $\bigl(v(t) e^{-B(t)}\bigr)' = (v' - \beta v) e^{-B} \le \alpha\beta e^{-B}$. Integrating from $a$ to $t$ and using $v(a) = 0$ gives

$$v(t) e^{-B(t)} \le \int_a^t \alpha(s)\beta(s) e^{-B(s)}\, ds, \quad\text{so}\quad v(t) \le \int_a^t \alpha(s)\beta(s) e^{B(t) - B(s)}\, ds.$$

Since $u(t) \le \alpha(t) + v(t)$ and $B(t) - B(s) = \int_s^t \beta$, the first claim follows. The step $v' \le \beta\alpha + \beta v$ is where $\beta \ge 0$ is used: it multiplies the inequality $u \le \alpha + v$ by $\beta(t)$.

If $\alpha$ is nondecreasing, then $\alpha(s) \le \alpha(t)$ for $s \le t$, and

$$\int_a^t \alpha(s)\beta(s) e^{B(t) - B(s)}\, ds \le \alpha(t) \int_a^t \beta(s) e^{B(t) - B(s)}\, ds = \alpha(t)\bigl(e^{B(t)} - 1\bigr),$$

because $\frac{d}{ds}\bigl(-e^{B(t) - B(s)}\bigr) = \beta(s) e^{B(t) - B(s)}$. So $u(t) \le \alpha(t) + \alpha(t)(e^{B(t)} - 1) = \alpha(t) e^{B(t)}$. Here $\alpha(t) \ge 0$ is not needed. $\square$

**Differential form.** $\bigl(u(t) e^{-B(t)}\bigr)' = (u' - \beta u) e^{-B} \le 0$, so $u(t) e^{-B(t)} \le u(a)$. No sign of $\beta$ is used. $\square$

**Discrete form.** Let $S_n = \sum_{k=0}^{n-1} c_k a_k$, so $a_n \le b_n + S_n$ and $S_0 = 0$. Since $c_n \ge 0$,

$$S_{n+1} = S_n + c_n a_n \le S_n + c_n (b_n + S_n) = (1 + c_n) S_n + c_n b_n.$$

By induction on $n$, $S_n \le \sum_{k=0}^{n-1} c_k b_k \prod_{j=k+1}^{n-1}(1 + c_j)$: this is true for $n = 0$ (both sides 0), and the recurrence carries it from $n$ to $n + 1$, since multiplying the bound for $S_n$ by $1 + c_n$ adds the factor $j = n$ to each product and the new term is $c_n b_n$ with an empty product. Then $a_n \le b_n + S_n$ gives the claim. $\square$

**The one-step form.** From $E_{n+1} \le (1 + h\Lambda) E_n + \delta$, induction gives $E_n \le (1 + h\Lambda)^n E_0 + \delta \sum_{m=0}^{n-1} (1 + h\Lambda)^m = (1 + h\Lambda)^n E_0 + \delta \frac{(1 + h\Lambda)^n - 1}{h\Lambda}$. Since $1 + x \le e^x$, $(1 + h\Lambda)^n \le e^{n h\Lambda}$, and the right side increases with $(1 + h\Lambda)^n$. $\blacksquare$

## Consequences

- **Uniqueness and continuous dependence.** If $f$ is continuous and Lipschitz in $y$ with constant $L$, two solutions $y$, $z$ of $y' = f(t, y)$ satisfy $\|y(t) - z(t)\| \le \|y(t_0) - z(t_0)\| + \int_{t_0}^t L \|y(s) - z(s)\|\, ds$, so $\|y(t) - z(t)\| \le e^{L (t - t_0)} \|y(t_0) - z(t_0)\|$. With equal start values the two solutions agree. This is the uniqueness half of the [Picard-Lindelöf theorem](/picard-lindelof-theorem/).
- **Perturbed right-hand sides.** If $z' = f(t, z) + r(t)$ with $\|r\| \le \varepsilon$, then $\|y(t) - z(t)\| \le e^{L(t - t_0)}\|y(t_0) - z(t_0)\| + \frac{\varepsilon}{L}(e^{L(t - t_0)} - 1)$. This bounds the effect of modelling errors and is the continuous analogue of the error bound below.
- **Convergence of one-step methods.** With local errors $\|\delta_{n+1}\| \le C h^{p+1}$ and a step map with Lipschitz constant $1 + h\Lambda$, the one-step form gives $\|e_n\| \le C h^p (e^{\Lambda (t_n - t_0)} - 1)/\Lambda$. This is how the convergence of [Euler's method](/euler-method/), [Heun's method](/heuns-method/) and all Runge-Kutta methods is proved.
- **Multistep methods and PDE schemes.** The proofs of the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/) and of the [Lax equivalence theorem](/lax-equivalence-theorem/) use the discrete form with the bounds of the powers of a step matrix.
- **Convergence of Picard iteration.** The error bound $\|y - y^{(k)}\| \le \frac{(L (t - t_0))^k}{k!} \max \|y - y^{(0)}\|$ for [Picard iteration](/picard-iteration/) comes from the same estimate applied $k$ times.
- **Nonlinear versions.** Bihari's inequality replaces $\beta u$ by $\beta\, w(u)$ for a nondecreasing $w$, and gives bounds for problems that are not Lipschitz in the usual sense.

## Tightness

- **Equality.** For constant $\alpha \ge 0$ and $\beta = L$, the function $u(t) = \alpha e^{L(t - a)}$ satisfies the hypothesis with equality, because $\alpha + \int_a^t L \alpha e^{L(s - a)} ds = \alpha e^{L(t - a)}$. So the exponential cannot be improved in general. In the discrete form, $a_n = (1 + c)^n b$ with constant $b_n = b$ and $c_n = c$ gives equality.
- **The sign condition on $\beta$ is necessary in the integral form.** Take $\beta \equiv -1$, $\alpha \equiv 1$ on $[0, 1]$, and $u \equiv \frac12$. The hypothesis $\frac12 \le 1 - \frac{t}{2}$ holds for $0 \le t \le 1$, but the conclusion $u(t) \le e^{-t}$ fails at $t = 1$, where $e^{-1} = 0.3679 < 0.5$.
- **The short form needs a nondecreasing $\alpha$.** Take $\alpha(t) = 1 - t$, $\beta \equiv 1$ on $[0, 1]$ and $u \equiv 1$. The hypothesis holds with equality, $1 = (1 - t) + t$, but $\alpha(t) e^{t}$ is $0$ at $t = 1$, below $u(1) = 1$. The general bound of the theorem gives $u(1) \le 0 + \int_0^1 (1 - s) e^{1 - s} ds = 1$, which is exact.
- **The bound can be very pessimistic.** For $y' = -L y$ the difference of two solutions decays like $e^{-L t}$, while the Lipschitz argument gives the growth $e^{L t}$. For [stiff problems](/stiff-ode-problem/), where $L$ is large and the solutions contract, a one-sided Lipschitz constant in the differential form gives the realistic bound $e^{\nu t}$ with $\nu < 0$.

## History

Gronwall proved a differential inequality of this kind in 1919, in a paper on the dependence of solutions on a parameter. Bellman stated the integral form in 1943, in a paper on the stability of solutions of linear equations, and the result is often called the Gronwall-Bellman inequality.

## References
