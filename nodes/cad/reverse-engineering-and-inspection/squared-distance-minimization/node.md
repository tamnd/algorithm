---
tag: YVZM72
kind: algorithm
slug: squared-distance-minimization
name: Squared distance minimization
aliases:
- SDM fitting
- curvature-based squared distance minimization
area: cad/reverse-engineering-and-inspection
level: research
summary: Wang, Pottmann and Liu's B-spline fitting that minimises a local quadratic model of the squared distance, which converges faster than point distance methods.
solves: [curve-fitting]
model: real-ram
complexity:
  vars: {m: the number of data points, n: the number of control points, p: the degree, S: the number of curve samples for the foot points, k: the number of Newton steps per foot point, b: the number of energy evaluations per iteration, s: the number of iterations}
  time: {worst: "Θ(s (b + 1) (S p² + m (S + k p²)) + s (m p² + n p²))"}
  space: {extra: "Θ(m + n p + S)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2006
  people: [Wenping Wang, Helmut Pottmann, Yang Liu]
  note: They fitted B-spline curves to point clouds by minimizing, at each step, the second-order approximation of the squared distance function that Pottmann and Hofer had derived from the curvature, and showed that this behaves like a quasi-Newton method.
prereqs: [parameter-correction, b-spline-fitting, surface-curvature]
see_also: [point-to-plane-icp, iterative-closest-point, newton-point-inversion, gauss-newton-algorithm, levenberg-marquardt, geometric-primitive-fitting, frenet-frame, reverse-engineering-of-geometric-models]
sources:
  - paper: doi:10.1145/1138450.1138453
    title: Wenping Wang, Helmut Pottmann and Yang Liu, Fitting B-spline curves to point clouds by curvature-based squared distance minimization, ACM Transactions on Graphics 25(2), 2006, 214 to 238
    locator: the error terms of point distance, tangent distance and squared distance minimization, the curvature-based term with the case 0 <= d < rho, the regularization, and the analysis of the three methods as optimization methods
  - paper: doi:10.1007/978-3-662-05105-4_12
    title: Helmut Pottmann and Michael Hofer, Geometry of the squared distance function to curves and surfaces, in Visualization and Mathematics III, Springer, 2003, 221 to 242
    locator: the second-order Taylor approximation of the squared distance function to a planar curve, a space curve and a surface, in the Frenet frame or the principal frame at the foot point
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 3, line search methods with backtracking, and Chapter 10, Gauss-Newton and Levenberg-Marquardt methods for nonlinear least squares
---

Squared distance minimization (SDM) is an algorithm that fits a [B-spline](/b-spline/) curve to a cloud of points by minimizing, at each step, a quadratic model of the squared distance from each point to the curve that takes the curvature of the curve into account. [Parameter correction](/parameter-correction/), which Wang, Pottmann and Liu call point distance minimization (PDM), models the squared distance from a data point $X_k$ to the moving curve by the squared distance to its current foot point $K_k$, a model that is correct only far from the curve. Tangent distance minimization (TDM) uses the squared distance to the tangent line at $K_k$, which is correct only for points on a straight curve. SDM uses the second-order approximation of the squared distance function derived by Pottmann and Hofer: in the frame of the tangent $T$ and the normal $N$ at the foot point, with signed distance $d$ and radius of curvature $\rho$,
$$ F(y) \approx \frac{d}{d - \rho} \bigl( (y - K) \cdot T \bigr)^2 + \bigl( (y - K) \cdot N \bigr)^2 . $$
Both PDM and TDM are limits of this model. Since the model is quadratic in the control points, each SDM step is one linear least-squares problem, like a PDM step, but it converges in a few steps where PDM needs hundreds. Wang, Pottmann and Liu (2006) introduced the method and analyzed it as a quasi-Newton method; with a step-length control, as in the code here, the true error never increases.

## In plain words

To fit a smooth curve to many points, we start from a rough curve and improve it step by step. At each step, every point pulls on the curve. The question is how hard each point should pull, and in which direction.

If a point pulls the curve straight toward itself, as in parameter correction, the curve also slides along itself, which does nothing useful and slows the fit down. If a point only pulls in the direction across the curve, the curve can slide freely, and the fit may jump. SDM uses the bend of the curve to decide. A point on the outside of a bend, or far away, also pulls a little along the curve; a point close to the curve on the inside of a bend pulls only across. With this rule the curve settles in a handful of steps.

## The problem

**Input.** Points $X_1, \dots, X_m$ in the plane, a degree $p \ge 2$, a clamped knot vector $U$ with $n$ basis functions on $[a, b]$, a starting control polygon $P$, and a smoothing weight $\mu \ge 0$.

**Output.** Control points $P$ of the curve $C_P(t) = \sum_i N_{i,p}(t) P_i$ that make
$$ f(P) = \sum_{k=1}^{m} \operatorname{dist}(X_k, C_P)^2 + \mu R(P) $$
small, where $\operatorname{dist}$ is the orthogonal distance to the curve and $R(P) = \sum_i \lvert P_{i+1} - 2 P_i + P_{i-1} \rvert^2$ is a roughness term. This is [curve fitting](/curve-fitting/) with the geometric error, the same objective as parameter correction. It is nonlinear, and in general it has many local minima.

## The algorithm

At a foot point $K = C(t)$ with $C'(t) \ne 0$, let $T$ be the unit tangent, $N$ the unit normal ($T$ turned left by $90$ degrees), $\kappa$ the signed curvature, so that the center of curvature is $K + N/\kappa$ and $\rho = 1/\kappa$, and $d = (X - K) \cdot N$ the signed distance. The SDM weight is
$$ w = \frac{d}{d - \rho} = \frac{\kappa d}{\kappa d - 1} , $$
set to $0$ when $0 \le \kappa d < 1$, and to $1$ when the foot point is an end of the curve.

```pseudo id=main
SDM(X_1..X_m, U, p, P, μ)
L1  P ← the starting control points
L2  repeat
L3      for each k: t_k ← foot point of X_k on C_P; K_k, T_k, N_k, κ_k, d_k at t_k
L4      w_k ← κ_k d_k / (κ_k d_k − 1), or 0 if 0 ≤ κ_k d_k < 1, or 1 at an end of the curve
L5      Q ← argmin over Q of Σ_k [ w_k ((C_Q(t_k) − X_k)·T_k)² + ((C_Q(t_k) − X_k)·N_k)² ] + μ R(Q)
L6      α ← 1; while f(P + α(Q − P)) > f(P) do α ← α / 2
L7      P ← P + α (Q − P)
L8  until the decrease of f is below a tolerance
L9  return P
```

**Line L3.** The foot point is a [point projection](/point-projection-onto-a-surface/) problem: the code samples the curve, takes the nearest sample, and refines it with [Newton steps](/newton-point-inversion/) on $(C(t) - X_k) \cdot C'(t) = 0$. $T$, $N$ and $\kappa = (C' \times C'') / \lvert C' \rvert^3$ come from the first two derivatives of the B-spline, as in the [Frenet frame](/frenet-frame/).

**Line L4, the weight.** At a true foot point $\kappa d \le 1$, because the second derivative of $\lvert X - C(t) \rvert^2$ there is $2 \lvert C' \rvert^2 (1 - \kappa d) \ge 0$. For a point on the outer side of the bend, $\kappa d < 0$ and $w$ lies in $(0, 1)$. For a point on the inner side, between the curve and its center of curvature, $0 < \kappa d < 1$ and the formula gives a negative $w$: the true squared distance is not convex there. SDM then uses $w = 0$, which is the tangent distance term; Wang, Pottmann and Liu treat this case the same way. When the foot point is an end of the curve, the distance is to that end point, and $w = 1$ makes the term the squared distance to the end point.

**Line L5.** The term of point $k$ is a quadratic function of the new control points $Q$, because $C_Q(t_k)$ is linear in $Q$. So the minimum solves a linear system with $2n$ unknowns. Unlike in PDM, the two coordinates are coupled through $T_k$ and $N_k$. Points with $w_k = 0$ do not constrain a slide along the curve; when all weights are $0$, as on straight data, the system is singular, and the code adds a tiny damping term $\nu \lvert Q - P \rvert^2$, as in [Levenberg-Marquardt](/levenberg-marquardt/).

**Lines L6 and L7.** The model is accurate only near the current curve, so a full step can be too long. The code halves the step until the true energy $f$ does not increase; Wang, Pottmann and Liu discuss step control and regularization too. This makes the energy history monotone by construction.

## Example

**A quarter circle.** The $21$ points $(\cos \varphi_k, \sin \varphi_k)$ with $\varphi_k = \tfrac{\pi}{2} (k/20)^2$ are fitted by a cubic B-spline with the knots $(0, 0, 0, 0, \tfrac12, 1, 1, 1, 1)$ and $\mu = 0$, starting from the least-squares fit with chord-length parameters. The table gives the true squared distance error after each iteration; the parameter correction column uses the same start with all parameters corrected.

| iteration | SDM | parameter correction |
| --- | --- | --- |
| 0 | $6.634 \times 10^{-7}$ | $6.634 \times 10^{-7}$ |
| 1 | $4.077 \times 10^{-9}$ | $6.489 \times 10^{-7}$ |
| 2 | $1.587 \times 10^{-9}$ | $6.403 \times 10^{-7}$ |
| 3 | $1.552 \times 10^{-9}$ | $6.326 \times 10^{-7}$ |
| 10 | $1.545 \times 10^{-9}$ | $5.920 \times 10^{-7}$ |
| 200 | | $1.492 \times 10^{-7}$ |

SDM took full steps every time and reached in one step an error $36$ times smaller than parameter correction reached in $200$. The largest distance from a data point to the final SDM curve is $1.6 \times 10^{-5}$.

**A poor start.** From the fit with uniform parameters, whose error is $5.231 \times 10^{-5}$, SDM needed step halving in some iterations and stopped at $1.12 \times 10^{-6}$, a local minimum: the curve starts beyond the first data point, and parameter correction from there makes no progress either. Parameter correction from the same uniform start was still at $1.604 \times 10^{-5}$ after $200$ iterations.

**Noisy data.** Forty points with noise $\sigma = 0.005$ on three quarters of a wavy loop, $r = 1 + 0.3 \cos 2\varphi$ for $0 \le \varphi \le \tfrac{3\pi}{2}$, cubic with $8$ control points, $\mu = 10^{-6}$, five noise samples: in $15$ iterations each, $60$ of the $75$ steps were full steps, and the energy fell from between $0.022$ and $0.025$ to between $0.0009$ and $0.0019$.

All numbers are measured with the code of this page.

## Correctness

The correctness file proves:

- **The second-order model.** If $X = K + d N$ has the unique foot point $K$ on a $C^2$ curve, with $\kappa d < 1$, then the squared distance function $F$ satisfies $F(X + v) = \frac{d}{d - \rho} (v \cdot T)^2 + (d + v \cdot N)^2 + o(\lvert v \rvert^2)$, the formula of the lead.
- **The limits.** As $d \to 0$ or $\kappa \to 0$, the weight tends to $0$ and the model to the squared distance to the tangent line (TDM). As $\lvert d \rvert \to \infty$ on the outer side, the weight tends to $1$ and the model to the squared distance to the foot point (PDM). With the clamp, $0 \le w < 1$ at every interior foot point.
- **The step.** The model of line L5 is a sum of squares of linear functions of $Q$, so its minimizers solve a linear system; with damping $\nu > 0$ the solution is unique.
- **Monotone energy.** With the step control of line L6, $f$ never increases, and the loop stops.
- **Fixed point on exact data.** If every data point lies on the current curve, the current control points minimize the model, so a nonsingular SDM step returns them unchanged.

Not proved here: that SDM converges, how fast, or to which minimum. Wang, Pottmann and Liu interpret SDM as a quasi-Newton method, TDM as the Gauss-Newton method and PDM as an alternating method with linear convergence, and report fast convergence of SDM in their experiments; the examples above agree, but they are measurements.

## Complexity

Each iteration computes $m$ foot points: one sampling of the curve costs $\Theta(S p^2)$, comparing each point with the samples $\Theta(S)$ and $k$ Newton steps $\Theta(k p^2)$. Each term of line L5 touches $2(p + 1)$ unknowns, so the system has band width $\Theta(p)$ in a suitable order, costs $\Theta(m p^2)$ to build and $\Theta(n p^2)$ to solve. Each energy evaluation of line L6 costs another foot point pass. With $b$ energy evaluations per iteration and $s$ iterations this gives the bound in the front matter on the [real RAM](/real-ram/). The code of this page uses a dense solver, $\Theta(n^3)$ per iteration, which is fine for small $n$.

## Properties

- **Fast in practice.** Near a solution SDM takes full steps and converges in a few iterations, where parameter correction needs hundreds.
- **Geometric.** It minimizes the orthogonal distance, invariant under rigid motions of the data and the curve together.
- **Local.** It finds a local minimum near the start; the start curve, the knots and the degree matter.
- **No explicit parameters.** The data parameters are recomputed as foot points in every step, so they never enter the unknowns; the curve can slide along itself freely when this lowers the error.
- **Curvature dependent.** It needs the second derivative of the curve, so the degree must be at least $2$, and the weights jump at the boundary of the clamped region $0 \le \kappa d < 1$.

## Variants and improvements

- **Tangent distance minimization.** $w = 0$ for every point: the Gauss-Newton method for the orthogonal distance, used in [point-to-plane ICP](/point-to-plane-icp/) for registration. Fast near the solution, unstable far from it without step control.
- **Point distance minimization.** $w = 1$ with both terms, which is parameter correction.
- **Space curves.** For a curve in space, the model has a third term along the binormal; Wang, Pottmann and Liu give the space curve form.
- **Surfaces.** For a surface, the model in the frame of the principal directions is $\frac{d}{d - \rho_1} x_1^2 + \frac{d}{d - \rho_2} x_2^2 + x_3^2$, with the principal radii of curvature $\rho_1$, $\rho_2$ and the normal coordinate $x_3$; Pottmann and Hofer derive it, and it is used for B-spline surface fitting and for registration with curvature information.
- **Active curves and knot insertion.** The fit can start from a simple curve around the data and add control points where the error stays large; Wang, Pottmann and Liu also add knots during the fit.
- **Regularization.** A fairness term such as $\mu R$ or the bending energy keeps the curve smooth and the system well posed.

## When to use it

Use SDM to fit a B-spline curve or surface to an unordered point cloud with a geometric error, when the data have no natural parameters, or when parameter correction is too slow. It needs a start that is roughly right, such as a fit with chord-length parameters for ordered points, or a simple curve placed around the data for unordered points. In [reverse engineering](/reverse-engineering-of-geometric-models/) it is a method for free-form regions, after the regions of simple surfaces have gone to [geometric primitive fitting](/geometric-primitive-fitting/).

## Pitfalls

- **Bad start.** Far from the data the model is poor, steps are cut short, and the fit can stop in a wrong local minimum, as in the uniform-start example.
- **Curve grows past the data.** Nothing holds the ends of the curve to the first and the last data point; the curve can extend beyond them while the error falls. Trim, or add end conditions.
- **Points near the center of curvature.** When $\kappa d$ is close to $1$, the foot point is close to not being unique, and a small move of the curve moves it far. Such points often belong to another part of the curve.
- **Singular systems.** With many points in the tangent distance case the system can be singular along the curve; use damping or regularization.
- **Noise and many control points.** With many control points, the curve fits the noise; use the smoothing term or fewer control points.

## Implementations

## History

In 2003 Pottmann and Hofer worked out the second-order approximation of the squared distance function to curves and surfaces from the curvature at the foot point. Pottmann, Leopoldseder and Hofer used such approximations for active curves and surfaces and for registration around the same time. In 2006 Wang, Pottmann and Liu turned the planar and space curve forms into the SDM fitting method, compared it with point distance and tangent distance minimization as optimization methods, and showed by experiments that it converges much faster than the older point distance method of Hoschek.

## References
