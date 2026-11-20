---
tag: F15D7D
kind: theorem
slug: bregman-distance-convergence-rates
name: Convergence rates in Bregman distance
aliases:
- Burger-Osher convergence rates
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: For convex variational regularization under a source condition, the Bregman distance of the reconstruction to the true solution is of the order of the noise level.
prereqs: [variational-regularization, bregman-divergence, source-condition, subdifferential]
see_also: [tikhonov-convergence-rates, bregman-iteration, total-variation-denoising, morozov-discrepancy-principle, fenchel-duality, regularization-method]
sources:
  - paper: doi:10.1088/0266-5611/20/5/005
    title: Martin Burger and Stanley Osher, Convergence rates of convex variational regularization, Inverse Problems 20(5), 2004
    locator: pages 1411 to 1421 (the source condition in subdifferential form and the rate in the generalized Bregman distance)
  - paper: doi:10.1088/0266-5611/21/4/007
    title: Elena Resmerita, Regularization of ill-posed problems in Banach spaces, convergence rates, Inverse Problems 21(4), 2005
    locator: pages 1303 to 1314 (rates in Bregman distance under higher order source conditions)
  - paper: doi:10.1088/0266-5611/23/3/009
    title: Bernd Hofmann, Barbara Kaltenbacher, Christiane Poschl and Otmar Scherzer, A convergence rates result for Tikhonov regularization in Banach spaces with non-smooth operators, Inverse Problems 23(3), 2007
    locator: pages 987 to 1010 (the variational inequality form of the source condition for nonlinear operators)
  - paper: doi:10.1088/0266-5611/24/5/055020
    title: Markus Grasmair, Markus Haltmeier and Otmar Scherzer, Sparse regularization with l^q penalty term, Inverse Problems 24(5), 2008
    locator: article 055020 (for the l1 penalty, from a Bregman rate to a linear rate in the norm)
  - paper: doi:10.1017/S0962492918000016
    title: Martin Benning and Martin Burger, Modern regularization methods for inverse problems, Acta Numerica 27, 2018
    locator: pages 1 to 111 (survey of error estimates in Bregman distances)
---

For convex variational regularization $x_\lambda \in \arg\min_x \tfrac12\|Ax - y^\delta\|^2 + \lambda R(x)$, Burger and Osher (2004) measure the error by the Bregman distance of $R$ and prove that it is $O(\delta)$ for $\lambda \sim \delta$, if the true solution satisfies the source condition $A^*w \in \partial R(x^\dagger)$. The result needs no smoothness of $R$, so it covers total variation and $\ell_1$, for which norm rates do not follow from the classical theory. For $R = \tfrac12\|x\|^2$ it is the classical rate $\|x_\lambda - x^\dagger\| = O(\sqrt\delta)$ of [Tikhonov regularization](/tikhonov-convergence-rates/).

## Statement

**Setting.** $X$ and $Y$ are Hilbert spaces, $A: X \to Y$ is bounded and linear, and $R: X \to (-\infty, \infty]$ is convex, proper and lower semicontinuous. The exact data are $y = Ax^\dagger$, the noisy data satisfy $\|y^\delta - y\| \le \delta$, and $x_\lambda$ is a minimizer of $T_\lambda(x) = \tfrac12\|Ax - y^\delta\|^2 + \lambda R(x)$ for $\lambda > 0$. For $\xi \in \partial R(u)$ the Bregman distance is

$$D_R^\xi(v, u) = R(v) - R(u) - \langle \xi, v - u\rangle \ge 0,$$

and for $\xi_v \in \partial R(v)$, $\xi_u \in \partial R(u)$ the symmetric Bregman distance is $D_R^{\mathrm{sym}}(v, u) = \langle \xi_v - \xi_u, v - u\rangle = D_R^{\xi_u}(v, u) + D_R^{\xi_v}(u, v)$.

**Source condition.** There is $w \in Y$ with $\xi^\dagger := A^*w \in \partial R(x^\dagger)$.

**Theorem** (Burger and Osher 2004). Under the source condition, let $\xi_\lambda = A^*(y^\delta - Ax_\lambda)/\lambda$. Then $\xi_\lambda \in \partial R(x_\lambda)$, and

$$D_R^{\mathrm{sym}}(x_\lambda, x^\dagger) = \langle \xi_\lambda - \xi^\dagger, x_\lambda - x^\dagger\rangle \le \frac{(\delta + \lambda\|w\|)^2}{4\lambda} \le \frac{\delta^2}{2\lambda} + \frac{\lambda\|w\|^2}{2},$$

$$\|Ax_\lambda - y\| \le \delta + \lambda\|w\|.$$

Each one-sided distance $D_R^{\xi^\dagger}(x_\lambda, x^\dagger)$ and $D_R^{\xi_\lambda}(x^\dagger, x_\lambda)$ satisfies the same bound. For the choice $\lambda = c\delta$ with $c > 0$,

$$D_R^{\mathrm{sym}}(x_\lambda, x^\dagger) \le \frac{(1 + c\|w\|)^2}{4c}\,\delta = O(\delta),$$

and $c = 1/\|w\|$ gives the bound $\|w\|\,\delta$.

## In plain words

To judge a reconstruction, we must measure how far it is from the truth. For smooth penalties the plain distance works well. For penalties with corners, such as total variation, the plain distance can stay large even for very good reconstructions, and no good bound on it exists in general. The Bregman distance measures the error in the way the penalty sees it. The theorem says: if the truth is the kind of object the penalty favors, in a precise sense that links it to the measurement operator, and the weight is chosen in proportion to the noise, then this error shrinks in proportion to the noise. The price is that the Bregman distance can be zero for objects that are not equal to the truth. It sees only the errors that the penalty can detect.

## Proof

*Optimality.* $x_\lambda$ minimizes the convex function $T_\lambda$, so $0 \in A^*(Ax_\lambda - y^\delta) + \lambda\partial R(x_\lambda)$, where the sum rule holds as the first term is continuous. This is $\xi_\lambda \in \partial R(x_\lambda)$.

*Main estimate.* Subtract $\lambda\xi^\dagger = \lambda A^*w$ from both sides of $A^*(Ax_\lambda - y^\delta) + \lambda\xi_\lambda = 0$:

$$A^*(Ax_\lambda - y^\delta) + \lambda(\xi_\lambda - \xi^\dagger) + \lambda A^*w = 0.$$

Take the inner product with $x_\lambda - x^\dagger$ and write $r = A(x_\lambda - x^\dagger) = Ax_\lambda - y$ and $e = y^\delta - y$. Then $Ax_\lambda - y^\delta = r - e$, and

$$\langle r - e, r\rangle + \lambda D_R^{\mathrm{sym}}(x_\lambda, x^\dagger) + \lambda\langle w, r\rangle = 0,$$

$$\lambda D_R^{\mathrm{sym}}(x_\lambda, x^\dagger) = \langle e - \lambda w, r\rangle - \|r\|^2.$$

*Bounds.* The right side is at most $\|e - \lambda w\|\,\|r\| - \|r\|^2 \le \tfrac14\|e - \lambda w\|^2$, the maximum of $s \mapsto as - s^2$. With $\|e - \lambda w\| \le \delta + \lambda\|w\|$ this gives the first bound, and $(a + b)^2 \le 2a^2 + 2b^2$ gives the second. As $D_R^{\mathrm{sym}} \ge 0$ by monotonicity of $\partial R$, also $\|r\|^2 \le \|e - \lambda w\|\,\|r\|$, so $\|Ax_\lambda - y\| = \|r\| \le \delta + \lambda\|w\|$. The two one-sided distances are nonnegative and sum to $D_R^{\mathrm{sym}}$, so each is bounded by it. Substituting $\lambda = c\delta$ gives the last bound, and $(1 + c\|w\|)^2/(4c)$ is smallest at $c = 1/\|w\|$, where it equals $\|w\|$. $\blacksquare$

The source condition also makes $x^\dagger$ an $R$-minimizing solution: for every $x$ with $Ax = y$, $R(x) \ge R(x^\dagger) + \langle A^*w, x - x^\dagger\rangle = R(x^\dagger) + \langle w, Ax - y\rangle = R(x^\dagger)$.

## Consequences

- **Quadratic penalty.** For $R = \tfrac12\|x\|^2$, $\partial R(x) = \{x\}$, the source condition is $x^\dagger = A^*w$, and $D_R^{\mathrm{sym}}(x_\lambda, x^\dagger) = \|x_\lambda - x^\dagger\|^2$. The theorem gives $\|x_\lambda - x^\dagger\| \le \sqrt{\|w\|\delta}$ for $\lambda = \delta/\|w\|$, the classical rate $O(\sqrt\delta)$ of Tikhonov regularization under the [source condition](/source-condition/) of order $\tfrac12$.
- **Strongly convex penalties.** If $R$ is $\mu$-strongly convex, $D_R^{\mathrm{sym}}(u, v) \ge \mu\|u - v\|^2$, so the theorem gives the norm rate $O(\sqrt\delta)$.
- **Total variation.** For $R = \mathrm{TV}$ the source condition asks for a dual certificate: a vector $w$ with $A^*w = -\operatorname{div} p$ for a field $p$ with $|p| \le 1$ that equals the unit normal on the edges of $x^\dagger$. The Bregman distance then measures how far the level lines of $x_\lambda$ are from being aligned with those of $x^\dagger$; it is blind to a change of contrast on a set where $x^\dagger$ is flat.
- **Sparsity.** For $R = \|x\|_1$ in $\ell^2$ the source condition holds if $x^\dagger$ is sparse and $A$ admits a certificate $A^*w$ with entries $\operatorname{sign}(x_i^\dagger)$ on the support and modulus at most 1 off it. With modulus strictly less than 1 off the support and an injectivity condition of $A$ on the support, Grasmair, Haltmeier and Scherzer (2008) turn the Bregman rate into the linear rate $\|x_\lambda - x^\dagger\| = O(\delta)$.
- **Parameter choice.** The a priori choice $\lambda \sim \delta$ needs only $\delta$, not $\|w\|$. The constant is best when $\lambda = \delta/\|w\|$, which is not known in practice.
- **Iterative methods.** Error estimates in Bregman distance of the same kind exist for [Bregman iteration](/bregman-iteration/), with the stop index chosen from the noise level.

**An example.** Let $A = \mathrm{diag}(1, 0.1)$ on $\mathbb{R}^2$, $R = \|x\|_1$, $x^\dagger = (1, 0)$, so $y = (1, 0)$. The source condition holds with $w = (1, 0)$: $A^\top w = (1, 0) \in \partial\|x^\dagger\|_1$, and $\|w\| = 1$. Take the noise $e = (0, \delta)$ and $\lambda = c\delta$ with $c < 1/\delta$. The problem separates, and $x_\lambda = (1 - \lambda,\ 100\delta(0.1 - c)_+)$. The Bregman distance is $D = 100\delta(0.1 - c)_+$, the second entry.

| $c$ | 0.01 | 0.05 | 0.08 | 0.1 |
|---|---|---|---|---|
| $D/\delta$ | 9 | 5 | 2 | 0 |
| bound $(1 + c)^2/(4c)$ | 25.5025 | 5.5125 | 3.645 | 3.025 |

For a small $c$ the noise in the weakly observed second entry is amplified by $1/0.1^2$ and passes the threshold. For $c \ge 0.1$ the threshold removes it. The error $\lambda$ in the first entry, a loss of contrast, does not enter the Bregman distance at all, because $R$ is linear near $x^\dagger$ in that direction.

## Tightness

**The order $\delta$ cannot be improved.** Take $R = \tfrac12\|x\|^2$, a bound $\|w\| \le \rho$, and suppose $A$ has a singular value $\sigma$ with $\sigma^2 = \delta/\rho$ and singular vectors $u$, $v$ ($Av = \sigma u$). The two elements $x_\pm = \pm\sigma\rho\,v = A^*(\pm\rho u)$ satisfy the source condition with $\|w\| = \rho$, and their exact data $\pm\sigma^2\rho\,u = \pm\delta u$ are both within $\delta$ of $y^\delta = 0$. Any method returns one point for $y^\delta = 0$, so its error for one of the two is at least $\|x_+ - x_-\|/2 = \sigma\rho = \sqrt{\delta\rho}$. The squared error, which is $D_R^{\mathrm{sym}}$, is then at least $\rho\delta$. For compact $A$ with singular values accumulating at 0 this happens for a sequence $\delta \to 0$. The bound $\|w\|\delta$ for $c = 1/\|w\|$ is thus sharp, constant included.

**The parameter rule matters.** For $\lambda = c\delta^\kappa$ the bound $\delta^2/(2\lambda) + \lambda\|w\|^2/2$ is of order $\delta^{\min(2 - \kappa, \kappa)}$, which is $\delta$ only for $\kappa = 1$. The example above shows that a small $c$ gives a large constant.

**The source condition is needed.** Without a source condition the theorem has no content, and no rate holds uniformly: for quadratic $R$, convergence can be arbitrarily slow for a suitable $x^\dagger$ (see [source condition](/source-condition/) and [Tikhonov convergence rates](/tikhonov-convergence-rates/)). Rates of other orders follow from weaker conditions in variational inequality form.

**The Bregman distance is weak.** $D_R(x_\lambda, x^\dagger) = 0$ does not imply $x_\lambda = x^\dagger$. In the example the error $\lambda$ in the first entry is invisible. For one-homogeneous $R$ such as TV and $\ell_1$, $D_R$ is 0 between any two points with a common subgradient, for example between $x^\dagger$ and $t x^\dagger$ for every $t > 0$.

## History

Burger and Osher (2004) introduced the Bregman distance as the error measure for convex variational regularization and proved the rate under the source condition $A^*w \in \partial R(x^\dagger)$, in the context of total variation methods. Resmerita (2005) proved higher rates in Bregman distance under a stronger source condition. Hofmann, Kaltenbacher, Poschl and Scherzer (2007) extended the theory to nonlinear operators in Banach spaces with a source condition in the form of a variational inequality, a form that later work uses to state rates of other orders. Grasmair, Haltmeier and Scherzer (2008) used it to derive norm rates for sparsity penalties. Benning and Burger (2018) survey the field.

## References
