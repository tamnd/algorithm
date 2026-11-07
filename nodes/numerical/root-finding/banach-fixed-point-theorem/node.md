---
tag: W014NF
kind: theorem
slug: banach-fixed-point-theorem
name: Banach fixed-point theorem
aliases:
- contraction mapping theorem
- contraction mapping principle
- Banach contraction principle
area: numerical/root-finding
level: core
summary: A contraction on a nonempty complete metric space has exactly one fixed point. Iteration from any start converges to it, with an error at most L^k/(1 - L) times the first step.
prereqs: [metric-space, fixed-point-iteration]
see_also: [fixed-point-iteration, picard-lindelof-theorem, picard-iteration, kantorovich-theorem, newton-method-for-systems, bellman-contraction, lipschitz-condition, jacobi-method]
sources:
  - paper: "Stefan Banach, Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales, Fundamenta Mathematicae 3, 133-181, 1922"
    locator: the theorem on operations that shrink distances (the contraction principle), in the part on applications to integral equations
  - book: isbn:9780898714616
    title: J. M. Ortega and W. C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000
    locator: Section 5.1, Contractions (the contraction mapping theorem and its error bounds) and Chapter 12, Contractions and Nonlinear Majorants
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 5.3, the Kantorovich and contractive mapping theorems
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1 (the contraction mapping theorem on a closed interval) and Chapter 4 (its form in R^n for simultaneous nonlinear equations)
  - book: isbn:9780898713527
    title: C. T. Kelley, Iterative Methods for Linear and Nonlinear Equations, SIAM Frontiers in Applied Mathematics 16, 1995
    locator: Chapter 4, the contraction mapping theorem and fixed point iteration
---

The Banach fixed-point theorem says that a contraction $T$ of a nonempty complete [metric space](/metric-space/) has exactly one fixed point, and that the iteration $x_{k+1} = T(x_k)$ converges to it from every start. It also gives computable error bounds: the error after $k$ steps is at most $L^k/(1 - L)$ times the first step, where $L < 1$ is the contraction constant. It is the convergence proof of [fixed-point iteration](/fixed-point-iteration/), and through it of the local theory of Newton's method, of [Picard iteration](/picard-iteration/) for differential equations, of the classical iterative methods for linear systems and of value iteration.

## Statement

Let $(X, d)$ be a nonempty complete metric space, and let $T : X \to X$ be a *contraction*: there is a constant $L$ with $0 \le L < 1$ such that

$$d(T(x), T(y)) \le L\, d(x, y) \qquad \text{for all } x, y \in X.$$

**Theorem (Banach, 1922).** Then:

1. $T$ has exactly one fixed point $x^* \in X$, that is, $T(x^*) = x^*$.
2. For every $x_0 \in X$, the sequence $x_{k+1} = T(x_k)$ converges to $x^*$.
3. For all $k \ge 0$: $d(x_k, x^*) \le L^k\, d(x_0, x^*)$.
4. For all $k \ge 1$: $d(x_k, x^*) \le \dfrac{L^k}{1 - L}\, d(x_1, x_0)$ (the a priori bound).
5. For all $k \ge 1$: $d(x_k, x^*) \le \dfrac{L}{1 - L}\, d(x_k, x_{k-1})$ (the a posteriori bound).

**Local form.** Let $(X, d)$ be complete, let $B = \{x : d(x, x_0) \le r\}$ be a closed ball, and let $T$ be a contraction with constant $L < 1$ on $B$, with values in $X$. If $d(T(x_0), x_0) \le (1 - L) r$, then $T(B) \subseteq B$, and items 1 to 5 hold with $B$ in place of $X$.

In $\mathbb{R}^n$ with a norm, a $C^1$ map $T$ on a closed convex set $D$ with $T(D) \subseteq D$ and $\sup_{x \in D}\|T'(x)\| \le L < 1$, in the induced matrix norm, is a contraction, by the mean value inequality. The theorem then holds on $D$.

## In plain words

Think of a map of a country, lying on the floor of a room in that country. Each place in the country has a point on the map. The map is smaller than the country, so it shrinks all distances. The theorem says that exactly one point of the map lies right above the place that it shows. To find it, take any place, look at its point on the map, then look at the point of that point, and go on. Since each step shrinks the distances by the same factor, the points crowd together and close in on the one fixed point. The factor also tells you how far you still are from it: when the steps get short, you are close. The country must have no holes, or the points could close in on a hole.

## Proof

Fix $x_0 \in X$ and let $x_{k+1} = T(x_k)$.

*The steps shrink.* For $k \ge 1$, $d(x_{k+1}, x_k) = d(T(x_k), T(x_{k-1})) \le L\, d(x_k, x_{k-1})$. By induction, $d(x_{k+1}, x_k) \le L^k d(x_1, x_0)$ for all $k \ge 0$.

*Cauchy sequence.* For $j > k \ge 0$, the triangle inequality and the sum of a geometric series give

$$d(x_j, x_k) \le \sum_{i=k}^{j-1} d(x_{i+1}, x_i) \le d(x_1, x_0) \sum_{i=k}^{j-1} L^i \le \frac{L^k}{1 - L}\, d(x_1, x_0).$$

The right side tends to 0 as $k \to \infty$, so $(x_k)$ is a Cauchy sequence. Since $X$ is complete, it has a limit $x^* \in X$.

*The limit is fixed.* A contraction is continuous: $d(T(x), T(y)) \le L\, d(x, y)$. So $T(x^*) = T(\lim x_k) = \lim T(x_k) = \lim x_{k+1} = x^*$. This proves existence in item 1, and item 2 for this $x_0$.

*Uniqueness.* If $T(y^*) = y^*$, then $d(x^*, y^*) = d(T(x^*), T(y^*)) \le L\, d(x^*, y^*)$. So $(1 - L)\, d(x^*, y^*) \le 0$, and since $1 - L > 0$, $d(x^*, y^*) = 0$. The fixed point does not depend on $x_0$, which completes items 1 and 2.

*Item 3.* $d(x_{k+1}, x^*) = d(T(x_k), T(x^*)) \le L\, d(x_k, x^*)$, and induction on $k$ gives the bound.

*Item 4.* In the Cauchy estimate, let $j \to \infty$. The distance is continuous, so $d(x^*, x_k) \le \frac{L^k}{1 - L} d(x_1, x_0)$.

*Item 5.* By the triangle inequality and item 3 for one step, $d(x_k, x^*) \le d(x_k, x_{k+1}) + d(x_{k+1}, x^*) \le L\, d(x_k, x_{k-1}) + L\, d(x_k, x^*)$. Solve for $d(x_k, x^*)$, using $1 - L > 0$.

*Local form.* A closed subset of a complete space is complete, so $B$ is complete. For $x \in B$, $d(T(x), x_0) \le d(T(x), T(x_0)) + d(T(x_0), x_0) \le L r + (1 - L) r = r$, so $T(B) \subseteq B$. Apply the theorem to $T : B \to B$.

*The form in $\mathbb{R}^n$.* For $x, y \in D$ the segment between them lies in $D$, since $D$ is convex. The mean value inequality gives $\|T(x) - T(y)\| \le \sup_{z \in D}\|T'(z)\|\, \|x - y\| \le L \|x - y\|$. A closed subset of $\mathbb{R}^n$ is complete. $\blacksquare$

## Consequences

- **[Fixed-point iteration](/fixed-point-iteration/).** On an interval $I$ that $g$ maps into itself with $|g'| \le L < 1$, the iteration converges from every start in $I$. For $g = \cos$ on $[0, 1]$, $L = \sin 1 = 0.8415$. From $x_0 = 1$, the a priori bound for $k = 10$ is $0.516$, the a posteriori bound is $0.0681$, and the true error is $0.00515$. The a posteriori bound is the one to use in a stop test.
- **Local convergence of Newton's method.** At a simple root of a $C^2$ function, the Newton map $N(x) = x - f(x)/f'(x)$ has $N'(x^*) = 0$. So $N$ is a contraction on a small closed interval around $x^*$, and the local form gives convergence. The [Kantorovich theorem](/kantorovich-theorem/) gives a ball of convergence that can be computed from the data at the start.
- **Systems.** The map $T(x, y) = (\tfrac12 \cos y, \tfrac12 \sin x)$ on $\mathbb{R}^2$ with the max norm has Jacobian entries of size at most $\tfrac12$ and one nonzero entry in each row, so $L = \tfrac12$. From $(0, 0)$ the iterates converge to $(0.4864051547, 0.2337255020)$, and the max-norm errors after 2, 4, 6 and 8 steps are $1.36 \times 10^{-2}$, $7.02 \times 10^{-4}$, $3.59 \times 10^{-5}$ and $1.84 \times 10^{-6}$. The a priori bound for $k = 8$ is $0.5^8 \cdot 0.5/0.5 = 3.91 \times 10^{-3}$.
- **Linear systems.** The [Jacobi method](/jacobi-method/) and other splittings iterate $x \mapsto Mx + c$. If $\|M\| < 1$ in some induced norm, the map is a contraction and the method converges. For [strictly diagonally dominant](/diagonally-dominant-matrix/) matrices, the Jacobi matrix has $\|M\|_\infty < 1$.
- **Differential equations.** The [Picard-Lindelöf theorem](/picard-lindelof-theorem/) applies the theorem to the integral operator of an initial value problem with a [Lipschitz](/lipschitz-condition/) right side, on a short time interval or with a weighted norm.
- **Dynamic programming.** The Bellman operator of a discounted problem is a contraction with constant equal to the discount factor in the max norm ([Bellman contraction](/bellman-contraction/)), so value iteration converges.
- **Inverse and implicit function theorems.** Ortega and Rheinboldt prove them in Section 5.2 by the contraction theorem.

## Tightness

Each hypothesis is needed, and the bounds cannot be improved in general.

- **Completeness.** On $X = (0, 1]$ with the usual distance, $T(x) = x/2$ is a contraction with $L = 1/2$, and it has no fixed point: the iterates converge to $0 \notin X$.
- **A constant $L < 1$.** On $X = [1, \infty)$, $T(x) = x + 1/x$ satisfies $|T(x) - T(y)| = |x - y|(1 - 1/(xy)) < |x - y|$ for $x \ne y$, so it shrinks every distance, but by no fixed factor. It has no fixed point, since $1/x \ne 0$. Edelstein's theorem shows that such a map does have a unique fixed point when $X$ is compact.
- **$L = 1$.** The shift $T(x) = x + 1$ on $\mathbb{R}$ keeps distances and has no fixed point. The map $T(x) = x$ has every point fixed.
- **The bounds.** For $T(x) = Lx$ on $\mathbb{R}$ with $x_0 > 0$, $x^* = 0$ and $d(x_k, x^*) = L^k x_0$, which is item 3 with equality. Also $d(x_1, x_0) = (1 - L)x_0$, so item 4 holds with equality, and $d(x_k, x_{k-1}) = L^{k-1}(1 - L)x_0$, so item 5 holds with equality too.
- **Local hypothesis.** $T(x) = x^2$ is a contraction with $L = 2r$ on $[-r, r]$ for $r < 1/2$, and it maps that interval into itself. On $[-2, 2]$ it is not a contraction, and from $x_0 = 2$ the iterates diverge. A contraction near a fixed point does not give convergence from far away.

## History

Banach stated and proved the principle for complete normed spaces in his 1922 thesis, published in Fundamenta Mathematicae, and applied it to integral equations. The form for complete metric spaces given above is the standard form today. Ortega and Rheinboldt (Section 5.1 and Chapter 12) give the theorem in the form used in numerical analysis, with the a priori and a posteriori bounds and many generalizations.

## References
