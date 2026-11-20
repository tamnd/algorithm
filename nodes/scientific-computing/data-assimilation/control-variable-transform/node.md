---
tag: APMFJW
kind: technique
slug: control-variable-transform
name: Control variable transform
aliases: []
area: scientific-computing/data-assimilation
level: advanced
summary: "Writes the increment as x - x^b = U v with B = U U^T, so the background term of the variational cost becomes v^T v / 2, which removes B^-1 and preconditions the minimization."
prereqs: [three-dimensional-variational-assimilation, cholesky-decomposition]
see_also: [background-error-covariance, preconditioning, conjugate-gradient-method, incremental-4d-var, four-dimensional-variational-assimilation, hybrid-ensemble-variational, four-dimensional-ensemble-variational, condition-number]
sources:
  - paper: doi:10.1002/qj.340
    title: R. N. Bannister, A review of forecast error covariance statistics in atmospheric variational data assimilation. II, Modelling the forecast error covariance statistics, Quarterly Journal of the Royal Meteorological Society 134(637) (2008) 1971-1996
    locator: the control variable transform and its balance, vertical and horizontal parts
  - paper: doi:10.1175/1520-0493(1992)120<1747:TNMCSS>2.0.CO;2
    title: D. F. Parrish and J. C. Derber, The National Meteorological Center's spectral statistical-interpolation analysis system, Monthly Weather Review 120(8) (1992) 1747-1763
    locator: the analysis variables and the background error covariance in spectral space
  - paper: doi:10.1034/j.1600-0870.1999.t01-2-00003.x
    title: J. Derber and F. Bouttier, A reformulation of the background error covariance in the ECMWF global data assimilation system, Tellus A 51(2) (1999) 195-221
    locator: the change of variables through balance operators in the ECMWF system
---

A control variable transform is a change of variables in a variational analysis. The analysis increment is written as $x - x^b = U v$, where $U$ is a factor of the [background error covariance](/background-error-covariance/), $B = U U^\top$, and the minimization runs over the new variable $v$. The background term $\tfrac12 (x - x^b)^\top B^{-1} (x - x^b)$ of the cost then becomes $\tfrac12 v^\top v$. This has two effects. The method never needs $B^{-1}$, and in practice not even $B$, only products with $U$ and $U^\top$. And the Hessian of the cost becomes the identity plus a term of rank at most $p$, the number of observations, so its eigenvalues are at least 1 and conjugate gradients converge in far fewer steps. Every operational [3D-Var](/three-dimensional-variational-assimilation/) and [4D-Var](/four-dimensional-variational-assimilation/) system works in such variables, and $U$ is where the model of $B$ is coded.

## In plain words

The background errors at nearby points and in related quantities move together, so the numbers that describe the state are strongly linked. A minimizer that works with these linked numbers makes slow progress, because a step in one number is undone by the links to the others. The transform replaces them by new numbers that are independent and all of the same size. Each new number stands for one independent pattern of error. In these numbers the background term is a plain sum of squares, the minimizer converges quickly, and at the end the transform turns the result back into a correction of the state.

## When it applies

- The analysis minimizes a cost with a background term weighted by $B^{-1}$, as in [3D-Var](/three-dimensional-variational-assimilation/), [4D-Var](/four-dimensional-variational-assimilation/) and [incremental 4D-Var](/incremental-4d-var/).
- $B$ is too large to form or to invert, but it can be written as a product $UU^\top$ of operators that are cheap to apply, together with their transposes.
- The minimizer is iterative, such as [conjugate gradients](/conjugate-gradient-method/), so its speed depends on the [condition number](/condition-number/) of the Hessian.
- $U$ may be square or rectangular, and it does not have to be invertible: $B$ may even be singular, as an ensemble covariance is.

## The template

For a linear (or linearized) observation operator $H$ and the innovation $d = y^o - H(x^b)$, the cost in the control variable is

$$J(v) = \tfrac12 v^\top v + \tfrac12 (d - H U v)^\top R^{-1} (d - H U v), \qquad \nabla J(v) = v - U^\top H^\top R^{-1} (d - HUv).$$

Its minimizer solves a linear system with the Hessian $A = I + U^\top H^\top R^{-1} H U$:

```pseudo id=main
CVT-ANALYSIS(x^b, U, H, R, y^o)
L1  d <- y^o - H(x^b)
L2  b <- U^T H^T R^-1 d
L3  solve (I + U^T H^T R^-1 H U) v = b by conjugate gradients, with products only
L4  return x^a <- x^b + U v
```

The holes are the factor $U$ and its transpose (lines L2 to L4) and the observation operator with its adjoint. In an operational system $U$ is a product of simple steps, applied from right to left (Bannister 2008, Part II; Derber and Bouttier 1999): a horizontal transform, often spectral, in which the horizontal correlations are diagonal; a vertical transform onto the modes of a vertical covariance; a scaling by the standard deviations; and a balance operator that builds the full wind and mass increments from uncorrelated variables, such as a balanced part of the stream function and the unbalanced residuals.

**Why the analysis is unchanged (a theorem).** For any $U$ with $UU^\top = B$, put $C = HU$. The minimizer of $J(v)$ is $v^* = (I + C^\top R^{-1} C)^{-1} C^\top R^{-1} d = C^\top (R + CC^\top)^{-1} d$, by the push-through identity. So

$$x^a = x^b + U v^* = x^b + B H^\top (H B H^\top + R)^{-1} d,$$

which is the analysis of [optimal interpolation](/optimal-interpolation/) and of 3D-Var in the original variables. If $U$ is square and invertible, the two costs are equal point by point, $J(v) = J(x^b + Uv)$, since $(Uv)^\top B^{-1} (Uv) = v^\top v$.

**Why it preconditions (a theorem).** $C^\top R^{-1} C$ is positive semidefinite with rank at most $p$, and its nonzero eigenvalues $\mu_i$ are those of $R^{-1/2} H B H^\top R^{-1/2}$. So the eigenvalues of $A$ are 1, at least $n - p$ times, and $1 + \mu_i$. Hence:

- the condition number of $A$ is $1 + \mu_{\max}$, whatever the condition number of $B$;
- $A$ has at most $p + 1$ distinct eigenvalues, so conjugate gradients reach the exact minimizer in at most $p + 1$ steps in exact arithmetic.

In the original variables the Hessian is $B^{-1} + H^\top R^{-1} H$, and its condition number grows with that of $B$, which is large for long correlation lengths.

**Worked example.** Take $B = \begin{pmatrix} 1 & 0.9 \\ 0.9 & 1 \end{pmatrix}$, with eigenvalues 1.9 and 0.1, one observation of the first value with $R = 1$, and $d = 1$.

- In the original variables the Hessian is $B^{-1} + e_1 e_1^\top = \frac{1}{0.19}\begin{pmatrix} 1.19 & -0.9 \\ -0.9 & 1 \end{pmatrix}$, with eigenvalues 1 and $200/19 \approx 10.53$.
- The Cholesky factor is $U = \begin{pmatrix} 1 & 0 \\ 0.9 & \sqrt{0.19} \end{pmatrix}$, so $HU = (1, 0)$ and the Hessian in $v$ is $\begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$, with the condition number $2 = 1 + HBH^\top/R$.
- The minimizer is $v = (1/2, 0)$, and $x^a - x^b = Uv = (0.5, 0.45)$. This is $BH^\top d/(HBH^\top + R) = (1, 0.9)/2$, as the theorem says.

**Measurement.** On a line of $n = 100$ points take $B_{ij} = \rho^{|i - j|}$ with $\rho = e^{-1/L}$, observe every fifth point with $R = 0.25\,I$ ($p = 20$), and stop conjugate gradients at a relative residual of $10^{-8}$.

| $L$ (grid steps) | cond $B$ | cond, original | CG steps, original | cond, in $v$ | CG steps, in $v$ |
|---|---|---|---|---|---|
| 5 | 98.6 | 24.4 | 39 | 9.5 | 14 |
| 10 | 374.7 | 38.7 | 52 | 16.3 | 15 |

With every tenth point observed ($p = 10$, $L = 10$) the condition number falls from 92.1 to 9.2, and the steps fall from 76 to 10, within the bound $p + 1 = 11$. Both forms gave the same analysis to the tolerance of the solver. The matrices were dense, and the eigenvalues were computed by the Jacobi method.

## Classic examples

- **[3D-Var](/three-dimensional-variational-assimilation/).** The first operational 3D-Var minimized over spectral coefficients in which the horizontal covariance is diagonal (Parrish and Derber 1992).
- **[Incremental 4D-Var](/incremental-4d-var/) and [4D-Var](/four-dimensional-variational-assimilation/).** The inner loop minimizes over $v$, and the tangent linear and [adjoint models](/adjoint-model/) are applied to $Uv$ and to $U^\top$ of the adjoint result.
- **Multivariate balance.** The balance operator in $U$ lets an observation of the wind correct the pressure and the opposite, without any explicit cross covariance (Derber and Bouttier 1999).
- **[Hybrid ensemble-variational](/hybrid-ensemble-variational/) methods and [4D-EnVar](/four-dimensional-ensemble-variational/).** $U$ is extended with the ensemble perturbations, and the control vector gets one set of weights per member. Here $U$ is rectangular and the ensemble part of $B$ is singular, which the transform handles without change.

## Variations

- **Symmetric square root.** $U = B^{1/2}$ is one choice, the Cholesky factor is another. Any $U$ with $UU^\top = B$ gives the same analysis, and the choice is made for cost of application, not for accuracy.
- **Rectangular factors.** $U$ may be $n \times m$ with $m > n$ (several sources of covariance, as in hybrid methods) or $m < n$ (a reduced rank $B$). The increments then lie in the range of $U$.
- **Preconditioning with $B$.** A related method keeps the state variables and uses $B$ itself as the preconditioner of conjugate gradients. It needs products with $B$ but not a factor of it.
- **Second level preconditioning.** If the observations are dense and accurate, $\mu_{\max}$ is large and the transformed problem is still badly conditioned. Eigenvectors of the Hessian from an earlier minimization, computed by the [Lanczos algorithm](/lanczos-algorithm/), are then used as a further [preconditioner](/preconditioning/).

## Pitfalls

- **$U^\top$ not the exact transpose of $U$.** The gradient uses $U^\top$, so an error in it gives a wrong but plausible gradient. Check it with the dot product test $\langle Uv, w \rangle = \langle v, U^\top w \rangle$, as for an [adjoint model](/adjoint-model/).
- **Outer loops.** With a nonlinear $H$, each outer loop linearizes about a new guess, but the background term must stay relative to $x^b$. Keep $v$ as the total increment from $x^b$, and do not restart it from zero in each outer loop.
- **Balance relations where they do not hold.** Geostrophic balance, the usual link between wind and mass, is weak near the equator, so a balance operator built on it must be relaxed there (a rule of thumb).
- **Expecting the transform to fix a bad $B$.** The transform makes the minimization faster and does not change the analysis. If the model of $B$ is wrong, the analysis is wrong in the same way.

## Exercises

1. Prove the push-through identity $(I + C^\top R^{-1} C)^{-1} C^\top R^{-1} = C^\top (R + CC^\top)^{-1}$ by multiplying both sides by $(I + C^\top R^{-1} C)$ on the left and by $(R + CC^\top)$ on the right.
2. For one observation, show that the Hessian in $v$ has the eigenvalue $1 + HBH^\top/R$ once and the eigenvalue 1 for all other directions, and that conjugate gradients stop after 2 steps at most.
3. In the worked example, take $U = B^{1/2}$ instead of the Cholesky factor, and check that $Uv^*$ gives the same increment $(0.5, 0.45)$.

## References
