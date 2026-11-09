---
tag: 9YHJCE
kind: definition
slug: self-concordant-function
name: Self-concordant function
aliases:
- self-concordance
- self-concordant barrier
area: optimization/convex-optimization
level: research
summary: A convex function whose third derivative is bounded by its second, giving Newton steps guarantees.
prereqs: [convex-function, newton-method-for-systems, positive-definite-matrix]
see_also: [barrier-method, interior-point-method, central-path, strong-convexity, smoothness, convex-optimization-problem, semidefinite-programming, second-order-cone-programming]
sources:
  - book: isbn:9780898713190
    title: Yurii Nesterov and Arkadii Nemirovskii, Interior-Point Polynomial Algorithms in Convex Programming, SIAM, 1994
    locator: Chapter 2 (self-concordant functions and barriers, the universal barrier), Chapter 3 (path-following methods)
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Chapter 5 (Section 5.1 self-concordant functions, the Dikin ellipsoid and the damped Newton method, Section 5.3 self-concordant barriers and the path-following scheme)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.6 (self-concordance, its calculus and the analysis of Newton's method), Section 11.5 (complexity of the barrier method)
  - book: isbn:9780898715026
    title: James Renegar, A Mathematical View of Interior-Point Methods in Convex Optimization, SIAM, 2001
    locator: Chapter 2 (basic interior-point method theory, self-concordant functions and barriers)
  - paper: doi:10.1287/moor.2020.1113
    title: Yin Tat Lee and Man-Chung Yue, Universal barrier is n-self-concordant, Mathematics of Operations Research 46(3), 2021
    locator: pages 1129 to 1148
---

A self-concordant function is a convex function whose third derivative is bounded by a power of its second derivative, along every line. The bound is the same in every coordinate system, so it says that the Hessian changes slowly when it is measured in its own norm. This is exactly what Newton's method needs. For a self-concordant function, the number of Newton steps to minimize it has a bound that depends only on the starting gap and the accuracy, not on condition numbers or Lipschitz constants. Nesterov and Nemirovski introduced the class in the late 1980s, and it is the base of the polynomial bounds of [interior-point methods](/interior-point-method/) for all convex programs.

## Definition

**One variable.** A convex function $f: \mathbb{R} \to \mathbb{R} \cup \{+\infty\}$ that is three times differentiable on its open domain is *self-concordant* if

$$|f'''(x)| \le 2 f''(x)^{3/2} \quad \text{for all } x \in \operatorname{dom} f.$$

**Several variables.** A convex $f: \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ with an open domain is self-concordant if, for each $x \in \operatorname{dom} f$ and each direction $h$, the function $g(s) = f(x + sh)$ is self-concordant. Equivalently, $|D^3 f(x)[h, h, h]| \le 2\,(h^\top\nabla^2 f(x) h)^{3/2}$. Some authors also ask that $f$ is closed, that is, $f(x) \to \infty$ at the boundary of its domain.

**The local norm and the Newton decrement.** Write $\|h\|_x = (h^\top\nabla^2 f(x) h)^{1/2}$, and $\lambda(x) = (\nabla f(x)^\top\nabla^2 f(x)^{-1}\nabla f(x))^{1/2}$ for the Newton decrement. Then the definition reads $|D^3 f(x)[h, h, h]| \le 2\|h\|_x^3$.

**Self-concordant barrier.** A self-concordant $f$ that is closed is a $\nu$-self-concordant barrier for the closure of its domain if also

$$|\nabla f(x)^\top h| \le \sqrt{\nu}\,\|h\|_x \quad\text{for all } x, h, \quad\text{that is,}\quad \lambda(x)^2 \le \nu.$$

The number $\nu$ is the barrier parameter. It controls the number of steps of a path-following method: $O(\sqrt{\nu}\log(\nu/\varepsilon))$ Newton steps.

**The constant 2.** Any constant works. If $|f'''| \le M f''^{3/2}$, then $(M^2/4)f$ satisfies the definition with the constant 2, which makes $-\log x$ satisfy it with equality.

## Examples and non-examples

**Examples.**

- *Linear and convex quadratic functions.* The third derivative is $0$.
- *The logarithm.* $f(x) = -\log x$ on $x > 0$ has $f''(x) = 1/x^2$ and $f'''(x) = -2/x^3$, so $|f'''| = 2f''^{3/2}$ with equality. Also $f'(x)^2/f''(x) = 1$, so it is a barrier with $\nu = 1$ for $[0, \infty)$.
- *Polyhedra.* $-\sum_{i=1}^m\log(b_i - a_i^\top x)$ is an $m$-self-concordant barrier for $\{Ax \le b\}$, because a sum of $\nu_i$-barriers is a $(\sum\nu_i)$-barrier and composition with an affine map keeps self-concordance.
- *The semidefinite cone.* $-\log\det X$ on $X \succ 0$, with $X$ of size $n \times n$, is an $n$-self-concordant barrier. On a line $X + sH$ it is $-\sum_j\log(1 + s\sigma_j) + \text{const}$, where $\sigma_j$ are the eigenvalues of $X^{-1/2}HX^{-1/2}$.
- *The second-order cone.* $-\log(t^2 - \|u\|^2)$ on $\{\|u\| < t\}$ is a $2$-self-concordant barrier, for every dimension of $u$.
- *A mixed example.* $f(x) = x\log x - \log x$ on $x > 0$ has $f'' = (x + 1)/x^2$ and $|f'''| = (x + 2)/x^3$. The condition is $x + 2 \le 2(x + 1)^{3/2}$, which holds because $(x + 1)^{3/2} \ge 1 + \tfrac32 x$.

**Non-examples.**

- *The exponential.* $f(x) = e^x$ has $|f'''|/f''^{3/2} = e^{-x/2}$, which is unbounded as $x \to -\infty$. So $e^x$ is not self-concordant on $\mathbb{R}$, though $\tfrac14 e^{-a}e^x$ is self-concordant on each half-line $x > a$.
- *The inverse.* $f(x) = 1/x$ on $x > 0$ has $|f'''|/f''^{3/2} = 6x^{-4}/(2x^{-3})^{3/2} = (3/\sqrt2)\sqrt{x}$, which is unbounded as $x \to \infty$.
- *Powers.* $f(x) = x^4$ has $|f'''|/f''^{3/2} = 24x/(12x^2)^{3/2}$, which is unbounded as $x \to 0$.
- *A quadratic is not a barrier.* $x^2$ is self-concordant, but $f'(x)^2/f''(x) = 2x^2$ is unbounded, so it is not a barrier with any finite $\nu$. This is consistent, since its domain is all of $\mathbb{R}$.

**What the definition gives.** Let $f$ be self-concordant with a positive definite Hessian. The following facts are in Nesterov (2018, Chapter 5) and in Boyd and Vandenberghe (Section 9.6).

- *Dikin ellipsoid.* The open ellipsoid $\{y : \|y - x\|_x < 1\}$ lies in $\operatorname{dom} f$.
- *Hessian stability.* If $r = \|y - x\|_x < 1$, then $(1 - r)^2\nabla^2 f(x) \preceq \nabla^2 f(y) \preceq (1 - r)^{-2}\nabla^2 f(x)$.
- *Damped Newton step.* The step $x^+ = x - \nabla^2 f(x)^{-1}\nabla f(x)/(1 + \lambda(x))$ stays in the domain and decreases $f$ by at least $\lambda - \log(1 + \lambda)$, where $\lambda = \lambda(x)$.
- *Quadratic convergence.* If $\lambda(x) < 1$, the full Newton step gives $\lambda(x^+) \le (\lambda(x)/(1 - \lambda(x)))^2$.
- *Newton's method with backtracking.* With line-search parameters $\alpha \in (0, \tfrac12)$ and $\beta \in (0, 1)$, the number of steps to reach accuracy $\varepsilon$ is at most $(f(x_0) - f^*)/\gamma + \log_2\log_2(1/\varepsilon)$, with $\gamma = \alpha\beta(1 - 2\alpha)^2/(20 - 8\alpha)$. The [barrier method](/barrier-method/) uses this bound for each centering.

**Every convex set has one.** Each open convex set in $\mathbb{R}^n$ that contains no line has an $O(n)$-self-concordant barrier, the universal barrier of Nesterov and Nemirovski. Lee and Yue (2021) showed that its parameter is at most $n$. The parameter cannot always be smaller: each barrier for the nonnegative orthant $\mathbb{R}^n_+$ has $\nu \ge n$. The universal barrier is not easy to compute, so practical methods use the explicit barriers above.

## Related definitions

- **[Strong convexity](/strong-convexity/) and [smoothness](/smoothness/).** They bound the Hessian between two fixed multiples of the identity. Self-concordance instead bounds how fast the Hessian changes relative to itself, which allows Hessians that go to infinity at the boundary.
- **Affine invariance.** If $f$ is self-concordant and $A$ is an invertible affine map, then $f \circ A$ is self-concordant with the same constant, and Newton's method makes the same steps in the new coordinates. Bounds based on condition numbers do not have this property.
- **[Central path](/central-path/).** The minimizers of $t\,c^\top x + f(x)$ for a $\nu$-self-concordant barrier $f$. The barrier parameter is the duality gap times $t$ on this path.
- **Logarithmically homogeneous barrier.** A barrier $F$ for a cone with $F(\tau x) = F(x) - \nu\log\tau$. The three barriers $-\sum\log x_i$, $-\log\det X$ and $-\log(t^2 - \|u\|^2)$ are of this kind, and primal-dual methods for [second-order cone](/second-order-cone-programming/) and [semidefinite programs](/semidefinite-programming/) use this property.
- **Generalized self-concordance.** Variants with other powers, $|f'''| \le M f''^{p/2}$, cover functions such as the logistic loss, which is not self-concordant in the standard sense.

## References
