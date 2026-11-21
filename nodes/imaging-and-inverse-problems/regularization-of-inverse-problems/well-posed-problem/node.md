---
tag: FM9HKC
kind: definition
slug: well-posed-problem
name: Well-posed problem
aliases:
- Hadamard well-posedness
- ill-posed problem
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: intro
summary: "A problem is well posed (Hadamard) if a solution exists, it is unique, and it depends continuously on the data. If one condition fails, the problem is ill posed."
model: real-ram
prereqs: [inverse-problem, forward-operator]
see_also: [condition-number, pseudoinverse, degree-of-ill-posedness, picard-condition, regularization-method, singular-value-expansion, bakushinskii-veto, heat-equation]
sources:
  - paper: "Jacques Hadamard, Sur les problemes aux derivees partielles et leur signification physique, Princeton University Bulletin 13, 1902, pages 49 to 52"
    locator: the requirement that a problem of mathematical physics has one solution that depends continuously on the data, with the Cauchy problem for the Laplace equation as the counterexample
  - book: "Jacques Hadamard, Lectures on Cauchy's Problem in Linear Partial Differential Equations, Yale University Press, 1923"
    locator: the longer later account of correctly set problems (general locator)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 2, Ill-Posed Linear Operator Equations (the generalized inverse and the closed range condition)
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, Numerical Aspects of Linear Inversion, SIAM, 1998
    locator: Chapter 1 (ill-posed and inverse problems, and the discrete notion)
---

A problem is well posed in the sense of Hadamard if, for every admissible data, a solution exists, the solution is unique, and the solution depends continuously on the data. The definition turns the vague question "can this [inverse problem](/inverse-problem/) be solved?" into three checks, and for each problem it pays to say which check fails. The definition is qualitative. The size of the instability is measured by the [condition number](/condition-number/) of a matrix, and for a compact operator by the [degree of ill-posedness](/degree-of-ill-posedness/).

## Definition

Let $A: X \to Y$ be a map between normed spaces (for the linear theory, a bounded linear [forward operator](/forward-operator/) between Hilbert spaces). The problem "given $y \in Y$, find $x \in X$ with $A x = y$" is **well posed** if:

1. **Existence.** For each $y \in Y$ there is an $x$ with $A x = y$. ($A$ is onto.)
2. **Uniqueness.** There is at most one such $x$. ($A$ is one to one.)
3. **Stability.** The solution depends continuously on $y$: if $y_j \to y$ then $x_j \to x$. ($A^{-1}$ is continuous.)

A problem that is not well posed, that is, a problem for which at least one of the three conditions fails, is called an ill-posed problem.

The conditions depend on the spaces and their norms. A problem can be well posed with one norm on $Y$ and fail condition 3 with another. So a statement of well-posedness must name the spaces.

**The linear case.** For a bounded linear $A$ between Hilbert spaces, conditions 1 and 2 imply condition 3, by the bounded inverse theorem. So in the strict sense, a linear problem fails stability only together with existence. The useful notion for linear inverse problems relaxes the first two conditions. Replace "a solution" by "the minimum norm least squares solution" $x^\dagger = A^\dagger y$ (see [pseudoinverse](/pseudoinverse/)). It exists exactly for $y$ in the domain $D(A^\dagger) = R(A) \oplus R(A)^\perp$ and it is always unique. Then the problem is well posed in this generalized sense exactly when $A^\dagger$ is bounded, and $A^\dagger$ is bounded exactly when the range $R(A)$ is closed (EHN chapter 2).

**The compact case.** If $A$ is compact and its range has infinite dimension, the range is not closed. Then $A^\dagger$ is unbounded and condition 3 fails, even in the generalized sense. Every integral operator with a square-integrable kernel is compact, so most continuous models of imaging fall here. The [Picard condition](/picard-condition/) says which $y$ are in the range; the [singular value expansion](/singular-value-expansion/) shows how fast the inverse amplifies each component.

**Matrices.** A linear system with an $m \times n$ matrix always has a closed range, so it is well posed in the generalized sense. But the stability constant is $\|A^\dagger\| = 1/\sigma_r$, with $\sigma_r$ the smallest positive singular value, and it can be huge. Hansen calls a matrix problem discrete ill posed when the matrix is ill conditioned and its singular values decay gradually to zero with no clear gap. Such a matrix comes from the discretization of a compact operator, and its condition number grows as the grid is refined.

## Examples and non-examples

**A nonsingular matrix (well posed).** $A x = y$ with a nonsingular square $A$. All three conditions hold, with $\|x - x'\| \le \|A^{-1}\| \|y - y'\|$. The rectangle-rule matrix of the integration operator ($h = 1/n$ on and below the diagonal) is nonsingular; its condition number is $10.65$ for $n = 8$ and $82.1$ for $n = 64$.

**The integration operator (existence and stability fail).** $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0,1)$. Uniqueness holds: if $\int_0^s x = 0$ for all $s$, then $x = 0$. Existence fails: the range is the set of $y \in H^1(0,1)$ with $y(0) = 0$, so the constant $y = 1$ has no solution, not even in the least squares sense, because the range is dense and $\inf_x \|A x - 1\| = 0$ is not attained. Stability fails: the data $e = \delta \sqrt2 \sin((k - \tfrac12)\pi s)$ have norm $\delta$, and they change the solution by a function of norm $\delta (k - \tfrac12)\pi$, without bound in $k$.

**The Cauchy problem for the Laplace equation (stability fails).** Hadamard's example. Find $u$ with $\Delta u = 0$ for $y > 0$, $u(x, 0) = 0$ and $\partial_y u(x, 0) = \sin(n x)/n$. The solution is $u(x, y) = \sin(n x) \sinh(n y)/n^2$. The data tend to zero uniformly as $n \to \infty$, but at $y = 1$ the amplitude $\sinh(n)/n^2$ is $1.18$ for $n = 1$, $110.1$ for $n = 10$ and $6.06 \times 10^5$ for $n = 20$.

**The heat equation (forward well posed, backward not).** For $u_t = u_{xx}$ on $(0,1)$ with zero boundary values, the map from $u(\cdot, 0)$ to $u(\cdot, T)$ multiplies the mode $\sqrt2 \sin(k\pi x)$ by $\exp(-k^2\pi^2 T)$. The forward problem is stable, with constant 1. The backward problem divides by these factors. With $T = 0.01$ the factor for $k = 10$ is $5.17 \times 10^{-5}$ (see [heat equation](/heat-equation/)).

**Rank-deficient least squares (uniqueness fails, then repaired).** If $A$ has a nontrivial null space, $A x = y$ has many least squares solutions. The minimum norm choice $A^\dagger y$ restores uniqueness, and since the range of a matrix is closed, the repaired problem is stable.

**A regularized problem (well posed).** For each fixed $\alpha > 0$, the Tikhonov problem $\min_x \|A x - y\|^2 + \alpha \|x\|^2$ has exactly one solution, $(A^* A + \alpha I)^{-1} A^* y$, and it depends on $y$ with Lipschitz constant at most $1/(2\sqrt{\alpha})$. Regularization replaces a problem that fails condition 3 by a family of well-posed ones.

## Related definitions

- [Condition number](/condition-number/): a quantitative form of condition 3 for matrices, $\kappa(A) = \sigma_1/\sigma_n$.
- [Degree of ill-posedness](/degree-of-ill-posedness/): the rate at which the singular values of a compact operator tend to zero, and so how badly condition 3 fails.
- [Picard condition](/picard-condition/): the test of condition 1 for a compact operator, in terms of its singular system.
- [Regularization method](/regularization-method/): a family of bounded approximations of $A^\dagger$ with a parameter rule; it gives approximations that converge as the noise goes to zero.
- [Bakushinskii veto](/bakushinskii-veto/): when condition 3 fails, a parameter rule that does not use the noise level cannot give a convergent method in the worst case.

## References
