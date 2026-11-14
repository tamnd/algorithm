---
tag: RY3SVA
kind: algorithm
slug: parameter-correction
name: Parameter correction
aliases:
- Hoschek parameter correction
- intrinsic parameterization
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Hoschek's step of B-spline fitting that moves each data parameter to the foot point on the current curve or surface and refits, so the error is measured orthogonally.
solves: [curve-fitting]
model: real-ram
complexity:
  vars: {m: "the number of data points, minus one", n: the number of control points, p: the degree, d: the dimension of the points, S: the number of curve samples per iteration, k: the number of Newton steps per foot point, s: the number of iterations}
  time: {worst: "Θ(s (S p² + m (S d + k p²) + (m + n) p (p + d)))"}
  space: {extra: "Θ(m + n p + S d)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1988
  people: [Josef Hoschek]
  note: He called a parameterization intrinsic when every error vector from a data point to its curve point is normal to the curve, and reached it by correcting the parameters after each least-squares fit.
prereqs: [b-spline-fitting, point-projection-onto-a-surface, least-squares-problem]
see_also: [squared-distance-minimization, newton-point-inversion, iterative-closest-point, geometric-primitive-fitting, gauss-newton-algorithm, coordinate-descent, schoenberg-whitney-theorem, reverse-engineering-of-geometric-models]
sources:
  - paper: doi:10.1016/0167-8396(88)90017-9
    title: Josef Hoschek, Intrinsic parametrization for approximation, Computer Aided Geometric Design 5(1), 1988, 27 to 31
    locator: the condition that the error vectors be orthogonal to the approximating curve, and the iterative correction of the parameter values between least-squares fits
  - paper: doi:10.1145/1138450.1138453
    title: Wenping Wang, Helmut Pottmann and Yang Liu, Fitting B-spline curves to point clouds by curvature-based squared distance minimization, ACM Transactions on Graphics 25(2), 2006, 214 to 238
    locator: the analysis of point distance minimization (the alternation of foot point computation and least-squares fit) as an optimization method with linear convergence, compared with tangent and squared distance minimization
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 6, point inversion and projection by Newton iteration, and Chapter 9, least-squares curve and surface approximation with chord-length parameters
---

Parameter correction is an algorithm that fits a [B-spline](/b-spline/) curve or surface to measured points so that the error is the orthogonal distance from each point to the curve, not the distance to some arbitrary point of the curve. [B-spline fitting](/b-spline-fitting/) needs a parameter value $t_k$ for each data point $Q_k$; with the parameters fixed, the control points follow from one linear [least squares problem](/least-squares-problem/). But that problem measures $\lvert Q_k - C(t_k) \rvert$, the distance to the curve point at a guessed parameter, which is larger than the distance to the curve whenever the error vector is not normal to the curve. Parameter correction alternates two steps: move each $t_k$ to the foot point of $Q_k$ on the current curve, which is a [point projection](/point-projection-onto-a-surface/) problem, and refit the control points for the new parameters. Neither step can raise the total error, so the error decreases monotonically. Hoschek (1988) introduced the idea under the name *intrinsic parameterization*: parameters for which every error vector is normal to the curve. The method is simple and robust, but it converges only linearly, and slowly when the curve is far from the data; [squared distance minimization](/squared-distance-minimization/) was designed to remove that weakness.

## In plain words

To fit a smooth curve to many points, the usual method first gives each point a "time" along the curve, then finds the curve that passes close to each point at its own time. The trouble is that the times are a guess. A point may be matched to a place on the curve that is not the nearest one, and the fit then pulls the curve in the wrong direction.

Parameter correction repairs the guess. After a fit, it looks along the curve for the place nearest to each point and gives the point that new time. Then it fits again with the new times. It repeats this until the curve stops getting better. Each round can only make the total error smaller, but the rounds help less and less, so many rounds may be needed.

## The problem

**Input.** Data points $Q_0, \dots, Q_m \in \mathbb{R}^d$, a degree $p$ and a clamped knot vector $U$ that define $n$ B-spline basis functions $N_{1,p}, \dots, N_{n,p}$ on $[a, b]$, and optionally starting parameters.

**Output.** Control points $P_1, \dots, P_n$ of the curve $C_P(t) = \sum_i N_{i,p}(t) P_i$ that make the orthogonal error
$$ D(P) = \sum_{k=0}^{m} \operatorname{dist}(Q_k, C_P)^2 , \qquad \operatorname{dist}(Q, C_P) = \min_{t \in [a, b]} \lvert Q - C_P(t) \rvert , $$
small. $D$ is the geometric error of [curve fitting](/curve-fitting/); it is not a quadratic function of $P$. The algorithm works with the extended error
$$ E(P, t) = \sum_{k=0}^{m} \lvert Q_k - C_P(t_k) \rvert^2 , $$
which is quadratic in $P$ for fixed $t$, and satisfies $D(P) = \min_t E(P, t)$. So minimizing $D$ over $P$ is the same as minimizing $E$ over $P$ and $t$ together. The same holds for a tensor-product surface with parameter pairs $(u_k, v_k)$.

## The algorithm

```pseudo id=main
PARAMETER-CORRECTION(Q_0..Q_m, U, p, t)
L1  if no parameters are given then t ← chord-length parameters of Q, from a to b
L2  P ← least-squares control points for the parameters t
L3  repeat
L4      for each k (t_0 and t_m stay at a and b) do t_k ← foot point of Q_k on C_P, kept only if |Q_k − C_P(t_k)| does not grow
L5      P ← least-squares control points for the new parameters t
L6      E ← Σ_k |Q_k − C_P(t_k)|²
L7  until E falls by at most tol · E, or after the iteration limit
L8  return P and t
```

**Line L1.** Chord-length parameters put $t_k$ in proportion to the length of the polygon $Q_0 Q_1 \dots Q_k$. They are a good start for points spread evenly along a smooth curve. Uniform parameters are a poor start when the points are spaced unevenly, as the example shows.

**Lines L2 and L5.** For fixed $t$, $E$ is $\lVert \mathbf{Q} - N \mathbf{P} \rVert_F^2$ with the collocation matrix $N_{ki} = N_{i,p}(t_k)$, and the minimizer solves the [normal equations](/normal-equations/) $N^{\mathsf T} N \mathbf{P} = N^{\mathsf T} \mathbf{Q}$. It is unique when $N$ has full column rank, which by the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/) means that some $n$ of the parameters can be matched to the basis functions so that each basis function is nonzero at its parameter. The B-spline fitting page solves this banded system in linear time; the code here uses a dense solver.

**Line L4.** The foot point of $Q_k$ is a parameter $t$ that minimizes $\lvert Q_k - C(t) \rvert$. Inside $(a, b)$ it satisfies $g(t) = (C(t) - Q_k) \cdot C'(t) = 0$: the error vector is normal to the curve. The code samples the curve at $S + 1$ equal steps, starts from the best of the samples and the old $t_k$, and runs [Newton](/newton-point-inversion/) steps $t \leftarrow t - g(t)/g'(t)$ with $g' = \lvert C' \rvert^2 + (C - Q_k) \cdot C''$, clamped to $[a, b]$. The new $t_k$ is kept only if it is not farther than the old one, which is what makes the error monotone even when Newton fails. Hoschek's original step is cheaper: it moves $t_k$ by the tangential part of the error vector, scaled from length to parameter, which is one first-order step toward the foot point.

**The end parameters.** The code keeps $t_0 = a$ and $t_m = b$. If they move too, the curve can grow past the first and the last data point, where no data hold it, and the part beyond the data has no meaning. That growth was seen in tests; see the pitfalls.

## Example

**A quarter circle with unevenly spaced points.** The data are the $21$ points $(\cos \varphi_k, \sin \varphi_k)$ with $\varphi_k = \tfrac{\pi}{2} (k/20)^2$, which are dense near $(1, 0)$ and sparse near $(0, 1)$. The curve is a cubic B-spline with the knots $(0, 0, 0, 0, \tfrac12, 1, 1, 1, 1)$, so $5$ control points. $E$ is the error of line L6, $D$ the true orthogonal error, and "max" the largest distance from a data point to the curve.

| start | corrections | $E$ | $D$ | max |
| --- | --- | --- | --- | --- |
| uniform | 0 | $2.087 \times 10^{-4}$ | $5.231 \times 10^{-5}$ | $0.00304$ |
| uniform | 1 | $6.267 \times 10^{-5}$ | $4.074 \times 10^{-5}$ | $0.00242$ |
| uniform | 10 | $3.920 \times 10^{-5}$ | $3.498 \times 10^{-5}$ | $0.00199$ |
| uniform | 200 | $2.832 \times 10^{-5}$ | $2.786 \times 10^{-5}$ | $0.00194$ |
| chord length | 0 | $7.392 \times 10^{-7}$ | $6.634 \times 10^{-7}$ | $0.000309$ |
| chord length | 10 | $6.163 \times 10^{-7}$ | $6.105 \times 10^{-7}$ | $0.000322$ |
| chord length | 200 | $3.083 \times 10^{-7}$ | $3.064 \times 10^{-7}$ | $0.000245$ |

Three things show. With the uniform start, the fixed parameters overstate the error four times ($E$ against $D$), and the first correction removes most of the gap. After that, progress is slow: $199$ more corrections lower $E$ only by a factor of $2.2$. And the start matters more than the corrections: chord length with no correction is about $40$ times better than uniform with $200$ corrections, because the corrections only find a nearby local minimum.

**Noise-free data from a spline.** Thirty points sampled at random parameters on random cubic curves of the same spline space, eight curves, chord-length start. After $100$ corrections the error $E$ had dropped by factors from $2$ to $40$, and the largest distance from the true curve to the fitted curve had dropped from between $0.014$ and $0.047$ to between $0.004$ and $0.019$. The fit moves toward the true curve, but slowly. From the true parameters, the first fit is already the true curve and the corrections leave it there; that case is proved.

These numbers are measured with the code of this page.

## Correctness

The correctness file proves:

- **Monotone error.** Line L5 minimizes $E$ over $P$ for fixed $t$, and line L4 does not raise any term of $E$ for fixed $P$. So the values of $E$ after each fit never increase, and they converge.
- **The orthogonal error.** $D(P) \le E(P, t)$ for every $t$. If every parameter is moved to a global foot point, the orthogonal errors $D$ of the successive curves never increase either.
- **Fixed points are stationary.** At a fixed point whose parameters are interior foot points, the gradient of $E$ in $P$ and in $t$ vanishes, and every error vector $Q_k - C(t_k)$ is normal to the curve: the parameterization is intrinsic in Hoschek's sense. If the foot points are unique and nondegenerate, $P$ is then a stationary point of $D$.
- **Noise-free data.** If $Q_k = C^*(\tau_k)$ for a curve $C^*$ of the spline space and the collocation matrix at $\tau$ has full rank, the fit at $t = \tau$ returns $C^*$ exactly, and every later iteration keeps it.

Not proved: that the iteration reaches the global minimum of $D$, or even that the parameters converge, and how fast. Wang, Pottmann and Liu analyze the alternation as an optimization method, which they call point distance minimization, and find linear convergence, slow when the curve is far from the data; the example agrees with that.

## Complexity

One iteration samples the curve at $S + 1$ parameters in $\Theta(S p^2)$ (each point costs $\Theta(p^2)$ by the Cox-de Boor scheme, plus $\Theta(p d)$ to combine control points), compares each of the $m + 1$ data points with the samples in $\Theta(S d)$ and runs $k$ Newton steps in $\Theta(k p^2)$, then refits in $\Theta((m + n) p (p + d))$ with the banded solver of B-spline fitting. With $s$ iterations this is the bound in the front matter, on the [real RAM](/real-ram/). The sample search dominates; with a good start it can be replaced by Newton steps from the old parameter alone. The code of this page stores dense rows of length $n$ and solves the normal equations densely, which costs $\Theta(m (p n + S d + k p n) + n^3)$ per iteration; that is enough for small $n$.

## Properties

- **Monotone.** The error $E$ never increases, so the method cannot diverge.
- **Local.** It finds a local minimum near the start. The start, the knots and the degree decide most of the result.
- **Linear convergence.** The steps shrink as the curve settles, because moving the parameters and moving the control points are coupled and the alternation sees the coupling only one side at a time; this is the behavior of block [coordinate descent](/coordinate-descent/).
- **Orthogonal at the end.** At a fixed point the error vectors are normal to the curve, so $E$ equals the geometric error $D$.
- **General.** The same two steps work for surfaces, with foot points $(u_k, v_k)$, and for any family of curves that is linear in its coefficients.

## Variants and improvements

- **Hoschek's first-order correction.** Move $t_k$ by $\Delta t_k$ proportional to $(Q_k - C(t_k)) \cdot C'(t_k) / \lvert C'(t_k) \rvert$, without a full foot point search. Cheaper per step, and enough when the curve is already close.
- **Global foot points by sampling, as in the code.** Safer on curves that bend back, where a Newton step from the old parameter can lock onto the wrong branch.
- **Joint Gauss-Newton on $(P, t)$.** Treat the parameters as unknowns together with the control points and apply [Gauss-Newton](/gauss-newton-algorithm/) to $E$. The normal equations have a sparse structure, and convergence is faster than alternation.
- **Tangent and squared distance minimization.** Eliminate the parameters by using, at each foot point, a quadratic model of the squared distance: the distance to the tangent line, or the curvature-based model of squared distance minimization. These converge much faster near the solution.
- **Smoothing.** Add a fairness term, as in a [smoothing spline](/smoothing-spline/), so the curve does not wiggle when it has many control points.
- **Knot updates.** Insert knots where the error stays large, and correct the parameters again.

## When to use it

Use parameter correction after a B-spline fit with fixed parameters when the result is judged by the orthogonal distance, as in [reverse engineering](/reverse-engineering-of-geometric-models/) and inspection, and a few rounds are enough to remove most of the gap between $E$ and $D$. It is simple to add to any least-squares fit and never makes the fit worse. When high accuracy is needed or the start is poor, use squared distance minimization or a joint Gauss-Newton fit instead, and keep parameter correction as the cheap first step. When the parameters are known from the measuring process, for example time stamps of a tracked tool, correction is not needed.

## Pitfalls

- **Moving the end parameters.** If $t_0$ and $t_m$ are corrected too, the curve can extend past the data. In tests on noise-free spline data, correcting all parameters made $E$ fall while the largest distance from the true curve to the fitted curve rose from $0.018$ to $0.18$ in $100$ iterations. Keep the end parameters fixed, or trim the curve to the feet of the end points.
- **Rank loss.** Corrected parameters can crowd into a few knot spans and leave a basis function with no parameter in its support; the normal equations then become singular. Check the Schoenberg-Whitney condition, or add a small smoothing term.
- **Wrong foot points.** A Newton step from the old parameter finds a local foot point; on curves that bend back, it can be the wrong one. Sample, as the code does, or keep the step small.
- **Stopping too early.** The first corrections give large gains and later ones small gains, but small gains do not mean that the minimum is reached. Stop on a target error, not only on a small change.
- **Expecting the true curve.** On noisy data, or data not from the spline space, the result is a local minimum of the geometric error, not a recovery of a true curve.

## Implementations

## History

Least-squares fitting of splines with fixed parameters was standard by the 1970s, with uniform and chord-length parameters as the usual guesses. In 1988 Josef Hoschek observed that the error should be measured normal to the curve, called a parameterization with that property intrinsic, and reached it by correcting the parameters between fits. The same alternation appears in many fields, from principal curves in statistics to [iterative closest point](/iterative-closest-point/) registration, where the closest points play the role of the foot points. Wang, Pottmann and Liu (2006) analyzed it as point distance minimization and introduced squared distance minimization to speed it up.

## References
