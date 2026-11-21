---
tag: MG8T41
kind: definition
slug: source-condition
name: Source condition
aliases:
- range condition
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: "The assumption x = (A*A)^nu w with ||w|| <= rho on the true solution. It measures smoothness relative to A and turns convergence of a regularization method into a rate."
prereqs: [singular-value-expansion, regularization-method]
see_also: [qualification-of-regularization, tikhonov-convergence-rates, picard-condition, degree-of-ill-posedness, truncated-svd, landweber-iteration, iteratively-regularized-gauss-newton, fredholm-integral-equation-first-kind]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 3 (arbitrarily slow convergence without extra assumptions, the source sets, the interpolation inequality and the optimal error order) and Chapter 10 (the source condition for nonlinear Tikhonov regularization)
  - book: "C. W. Groetsch, The Theory of Tikhonov Regularization for Fredholm Equations of the First Kind, Pitman Research Notes in Mathematics 105, Pitman, Boston, 1984"
    locator: the chapter on convergence rates under range conditions (general locator)
  - paper: "T. Hohage, Regularization of exponentially ill-posed problems, Numerical Functional Analysis and Optimization 21, 2000, 439 to 464"
    locator: logarithmic source conditions (general locator)
  - paper: "B. Hofmann, B. Kaltenbacher, C. Poeschl and O. Scherzer, A convergence rates result for Tikhonov regularization in Banach spaces with non-smooth operators, Inverse Problems 23, 2007, 987 to 1010"
    locator: the variational form of the source condition (general locator)
---

A source condition is an assumption on the true solution $x^\dagger$ of an ill-posed equation $A x = y$. In its standard (Hoelder) form it says that $x^\dagger = (A^* A)^\nu w$ for some $\nu > 0$ and some $w$ with $\|w\| \le \rho$. In other words, $x^\dagger$ lies in the range of a power of $A^* A$, which is why the condition is also called a range condition. It measures smoothness relative to the forward operator: the larger $\nu$, the faster the coefficients of $x^\dagger$ in the singular basis fall compared to the singular values. Without some such condition, a regularization method converges as the noise level $\delta$ tends to 0 but can converge arbitrarily slowly. Under it, the best possible worst-case error is of the order $\rho^{1/(2\nu+1)} \delta^{2\nu/(2\nu+1)}$, and methods with enough [qualification](/qualification-of-regularization/) reach this order.

## Definition

**Setting.** $A: X \to Y$ is a bounded linear operator between Hilbert spaces with singular system $(\sigma_j; v_j, u_j)$, $A v_j = \sigma_j u_j$, $\sigma_j$ descending (see [singular value expansion](/singular-value-expansion/)). $x^\dagger = A^\dagger y$ is the minimum norm solution, and $y^\delta$ are data with $\|y^\delta - y\| \le \delta$. The power $(A^* A)^\nu$ is defined by the spectral theorem; on the singular basis it multiplies the coefficient of $v_j$ by $\sigma_j^{2\nu}$.

**Definition.** For $\nu > 0$ and $\rho > 0$, the source set is
$$M_{\nu, \rho} = \{ (A^* A)^\nu w : \|w\| \le \rho \}.$$
The element $x^\dagger$ satisfies the source condition of order $\nu$ with bound $\rho$ if $x^\dagger \in M_{\nu, \rho}$. The element $w$ is called the source element.

**The same condition in coefficients.** With $c_j = \langle v_j, x^\dagger \rangle$, and $x^\dagger$ orthogonal to the null space of $A$,
$$x^\dagger \in M_{\nu, \rho} \iff \sum_j \frac{|c_j|^2}{\sigma_j^{4\nu}} \le \rho^2 .$$
So the condition asks that the coefficients of $x^\dagger$ fall faster than $\sigma_j^{2\nu}$, in the square summable sense. Compare the [Picard condition](/picard-condition/), $\sum_j |\langle u_j, y\rangle|^2/\sigma_j^2 < \infty$, which only asks that a solution exists.

**Two special cases.** Since $R((A^* A)^{1/2}) = R(A^*)$, the case $\nu = 1/2$ reads $x^\dagger = A^* z$ with $\|z\| \le \rho$. The case $\nu = 1$ reads $x^\dagger = A^* A w$. These are the forms in which the condition first appeared in the analysis of Tikhonov regularization.

**Conventions.** Some authors write $x^\dagger = (A^* A)^{\mu/2} w$, so their $\mu$ is $2\nu$ and the rate reads $\delta^{\mu/(\mu+1)}$. The qualification numbers double in that convention. Other authors put the smoothness on $x^\dagger - x_0$ for a reference element $x_0$.

**Why it is needed (theorem).** If $R(A)$ is not closed, the singular values tend to 0. Fix $\delta > 0$ and $\rho > 0$, and take $j$ with $\sigma_j \rho \le \delta$. The two solutions $0$ and $\rho v_j$ have exact data $0$ and $\sigma_j \rho u_j$, both within $\delta$ of $y^\delta = 0$. A method sees the same data for both, so for one of them its error is at least $\rho/2$. So on the ball $\{\|x^\dagger\| \le \rho\}$ the worst-case error of every method is at least $\rho/2$ for every $\delta > 0$: no rate in $\delta$ is possible without a smaller set of solutions (EHN Chapter 3).

**What the condition buys (theorem).** For $x \in M_{\nu, \rho}$, the interpolation inequality
$$\|x\| \le \|A x\|^{2\nu/(2\nu+1)} \rho^{1/(2\nu+1)}$$
holds. Proof: with $x = (A^* A)^\nu w$ and $b_j = \langle v_j, w\rangle$, $\|x\|^2 = \sum_j \sigma_j^{4\nu} |b_j|^2$ and $\|A x\|^2 = \sum_j \sigma_j^{4\nu+2} |b_j|^2$. Put $\theta = 2\nu/(2\nu+1)$ and write $\sigma_j^{4\nu}|b_j|^2 = (\sigma_j^{4\nu+2}|b_j|^2)^\theta (|b_j|^2)^{1-\theta}$. Hoelder's inequality with exponents $1/\theta$ and $1/(1-\theta)$ gives $\|x\|^2 \le \|A x\|^{2\theta} \|w\|^{2(1-\theta)}$. Now if two elements of $M_{\nu,\rho}$ both fit the data within $\delta$, their difference $d$ is in $M_{\nu, 2\rho}$ with $\|A d\| \le 2\delta$, so $\|d\| \le (2\delta)^{\theta}(2\rho)^{1-\theta} = 2\delta^{\theta}\rho^{1-\theta}$. So the worst-case error of the best method on $M_{\nu,\rho}$ is at most of the order $\delta^{2\nu/(2\nu+1)}\rho^{1/(2\nu+1)}$, and EHN Chapter 3 shows that this order is attained for a sequence $\delta \to 0$, so it cannot be improved. A method that reaches it is called order optimal.

## Examples and non-examples

**The integration operator.** Let $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0,1)$. Its singular system is $c_j = (j - \frac12)\pi$, $\sigma_j = 1/c_j$, $v_j(t) = \sqrt2 \cos(c_j t)$ and $u_j(s) = \sqrt2 \sin(c_j s)$, and $(A^* z)(t) = \int_t^1 z(s)\,ds$. Integration by parts, with $\cos c_j = 0$ and $\sin c_j = (-1)^{j+1}$, gives the coefficients below. Then the coefficient test above decides the orders $\nu$.

| $x^\dagger(t)$ | $\langle v_j, x^\dagger\rangle$ | source condition holds for |
|---|---|---|
| $t$ | $\sqrt2\,((-1)^{j+1}/c_j - 1/c_j^2)$ | $\nu < 1/4$ |
| $1 - t$ | $\sqrt2 / c_j^2$ | $\nu < 3/4$ |
| $1 - t^2$ | $2\sqrt2\,(-1)^{j+1}/c_j^3$ | $\nu < 5/4$ |
| $\cos(\pi t/2)$ | $1/\sqrt2$ for $j = 1$, else $0$ | every $\nu$ |

For example, $\sum_j c_j^{-4} c_j^{4\nu}$ is finite exactly when $4\nu - 4 < -1$, which gives $\nu < 3/4$ for $1 - t$. The table shows what the condition means here. $\nu = 1/2$ means $x^\dagger = A^* z$, so $x^\dagger$ is in $H^1$ with $x^\dagger(1) = 0$; the function $1 - t$ has this with $z = 1$, and $t$ does not. $\nu = 1$ means $x^\dagger = A^* A w$, so in addition $x^{\dagger\prime}(0) = 0$ and $x^{\dagger\prime\prime} = -w \in L^2$; the function $1 - t^2$ has this with $w = 2$, and $1 - t$ does not. So the source condition is smoothness together with boundary conditions that come from $A$. A function that is smooth inside the interval can still have a low order.

**Rates seen in practice.** For $1 - t$ the order is just below $3/4$, so TSVD, Landweber and Tikhonov all have error of nearly the order $\delta^{0.6}$. The [qualification](/qualification-of-regularization/) page measures this rate in a diagonal model with coefficients $j^{-2}$.

**Non-example: a ball.** The set $\{\|x\| \le \rho\}$ is not a source set, and the theorem above shows that no method has a uniform rate on it.

**Non-example: exponentially ill-posed problems.** For the backward heat equation, $\sigma_j$ falls like $e^{-c j^2}$. Then $x^\dagger \in M_{\nu,\rho}$ asks for coefficients that fall like $e^{-2\nu c j^2}$, a kind of analytic smoothness that a physical solution rarely has. The natural assumption there is a logarithmic source condition $x^\dagger = (-\ln (A^* A))^{-p} w$ (with $\|A\|$ scaled below 1), which gives rates in powers of $1/\ln(1/\delta)$ (Hohage 2000). See [degree of ill-posedness](/degree-of-ill-posedness/).

## Related definitions

- [Qualification of a regularization method](/qualification-of-regularization/): the largest $\nu$ for which a method can use this condition.
- [Tikhonov convergence rates](/tikhonov-convergence-rates/): the rate $\delta^{2\nu/(2\nu+1)}$ for $\nu \le 1$ and its saturation.
- [Picard condition](/picard-condition/): the weaker condition that $y$ has a solution at all; the source condition is a weighted Picard condition, $\sum_j |\langle u_j, y\rangle|^2/\sigma_j^{2+4\nu} < \infty$.
- General source conditions: $x^\dagger = \varphi(A^* A) w$ for an increasing index function $\varphi$ with $\varphi(0) = 0$; the Hoelder form is $\varphi(\lambda) = \lambda^\nu$ and the logarithmic form is another case.
- Nonlinear problems $F(x) = y$: the condition is put on $x^\dagger - x_0$ with the linearization $F'(x^\dagger)$ in place of $A$, often together with a condition on how nonlinear $F$ is. The [iteratively regularized Gauss-Newton method](/iteratively-regularized-gauss-newton/) uses it in this form.
- Variational source conditions: an inequality in place of the range condition, used in Banach spaces and for non-smooth operators (Hofmann, Kaltenbacher, Poeschl and Scherzer 2007).

## References
