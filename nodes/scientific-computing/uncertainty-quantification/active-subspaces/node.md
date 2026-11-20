---
tag: 0TXSBW
kind: technique
slug: active-subspaces
name: Active subspaces
aliases:
- active subspace method
- gradient-based dimension reduction
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Finds the directions in input space along which the output changes most, from the eigenvectors of the average outer product of gradients.
prereqs: [symmetric-eigenproblem, monte-carlo-integration, principal-component-analysis]
see_also: [singular-value-decomposition, sobol-indices, morris-method, kriging, polynomial-chaos-expansion, response-surface-methodology, automatic-differentiation, adjoint-sensitivity-analysis]
sources:
  - paper: doi:10.1137/130916138
    title: Paul G. Constantine, Eric Dow and Qiqi Wang, Active subspace methods in theory and practice, applications to kriging surfaces, SIAM Journal on Scientific Computing 36(4), 2014, A1500-A1524
    locator: the matrix of averaged outer products of gradients, the bounds on the mean squared gradients along the active and inactive directions by sums of eigenvalues, the Poincare bound on the error of the conditional mean, and the Monte Carlo estimate of the matrix
  - book: isbn:9781611973853
    title: Paul G. Constantine, Active Subspaces, Emerging Ideas for Dimension Reduction in Parameter Studies, SIAM Spotlights 2, SIAM, 2015
    locator: the discovery of the active subspace from gradient samples, the choice of its dimension by the eigenvalue gap, and its use for response surfaces, integration and optimization
  - paper: doi:10.1016/j.ress.2017.01.013
    title: Paul G. Constantine and Paul Diaz, Global sensitivity metrics from active subspaces, Reliability Engineering and System Safety 162, 2017, 1-13
    locator: the activity scores built from the leading eigenpairs and their relation to derivative-based global sensitivity measures
---

Active subspaces find a few directions in the input space of a function $f : \mathbb{R}^m \to \mathbb{R}$ along which $f$ changes most on average. With $x$ random with density $\rho$, form the symmetric positive semidefinite matrix

$$C = \mathbb{E}\big[\nabla f(x)\, \nabla f(x)^{\mathsf T}\big] = W \Lambda W^{\mathsf T}, \qquad \lambda_1 \ge \cdots \ge \lambda_m \ge 0.$$

Each eigenvalue is the mean squared directional derivative along its eigenvector: $\lambda_i = \mathbb{E}[(w_i^{\mathsf T} \nabla f)^2]$. If there is a gap after $\lambda_n$, split $W = [W_1\ W_2]$ and set $y = W_1^{\mathsf T} x$, the active variables, and $z = W_2^{\mathsf T} x$, the inactive ones. Then $f$ changes little with $z$, and $f(x) \approx g(W_1^{\mathsf T} x)$ for a function $g$ of only $n$ variables, which can be fit, integrated or optimized cheaply. $C$ is estimated by Monte Carlo from $M$ gradient samples. The method is like [principal component analysis](/principal-component-analysis/), but of the gradients of $f$, not of the inputs. It finds rotated directions that no coordinate-wise sensitivity measure would see. Constantine, Dow and Wang gave the theory in 2014.

## In plain words

A model can have 50 inputs and still depend mainly on one weighted combination of them, such as a total load. Testing one input at a time hides this, because the combination spreads over many inputs. Instead, measure the slope of the model at many random points, and collect the slope vectors. If they all point roughly along one line, that line is the important direction. An eigenvalue decomposition of the average of the slope vectors times themselves finds these lines and ranks them. The large eigenvalues mark the directions that matter. You then study the model as a function of the few important combinations only.

## When it applies

- The gradient $\nabla f$ is available at sample points, by an [adjoint](/adjoint-sensitivity-analysis/) solve, [automatic differentiation](/automatic-differentiation/) or finite differences, and it is square integrable.
- The inputs are scaled to comparable ranges, usually standard normal or uniform on $[-1, 1]^m$. The eigenvectors change with the scaling.
- The function has low dimensional structure along linear combinations of inputs: it is close to a ridge function $g(W_1^{\mathsf T} x)$. The eigenvalues show whether this holds; a clear gap after $\lambda_n$ is the sign.
- For the error bound below, $\rho$ is the standard normal law. For other laws a Poincare constant of $\rho$ enters.

## The template

```pseudo id=main
ACTIVE-SUBSPACE(f, ∇f, ρ, M)
L1  draw x_1..x_M from ρ                                       ▷ hole: random or quasi-random points
L2  compute g_j ← ∇f(x_j) for each j                           ▷ hole: adjoint, AD, finite differences
L3  Ĉ ← (1/M) Σ_j g_j g_j^T                                    ▷ or the SVD of [g_1..g_M] / √M
L4  Ĉ = Ŵ Λ̂ Ŵ^T with eigenvalues in decreasing order
L5  choose n at a large gap λ̂_n / λ̂_(n+1)                     ▷ hole: gap, bootstrap of the subspace
L6  y ← Ŵ_1^T x;  fit g(y) ≈ f(x) from the runs                ▷ hole: polynomial, kriging, nothing
L7  return Ŵ_1, the eigenvalues and g
```

Line L3 builds the estimate; with $G = [g_1 \cdots g_M] / \sqrt{M}$, $\hat C = G G^{\mathsf T}$, so the [singular value decomposition](/singular-value-decomposition/) of $G$ gives $\hat W$ and $\hat\lambda_i = \sigma_i^2$ without forming $\hat C$. Line L5 fixes the dimension, and line L6 uses it: a response surface, a [polynomial chaos expansion](/polynomial-chaos-expansion/) or [kriging](/kriging/) in $n$ variables needs far fewer runs than in $m$.

**Gradients along the subspaces (proved).** $\mathbb{E}[\|\nabla_y f\|^2] = \lambda_1 + \cdots + \lambda_n$ and $\mathbb{E}[\|\nabla_z f\|^2] = \lambda_{n+1} + \cdots + \lambda_m$, where $\nabla_y f = W_1^{\mathsf T} \nabla f$ and $\nabla_z f = W_2^{\mathsf T} \nabla f$ are the gradients in the rotated coordinates.

*Proof.* $\mathbb{E}[\|W_1^{\mathsf T} \nabla f\|^2] = \mathbb{E}[\operatorname{tr}(W_1^{\mathsf T} \nabla f \nabla f^{\mathsf T} W_1)] = \operatorname{tr}(W_1^{\mathsf T} C W_1) = \operatorname{tr}(\Lambda_1)$, since the columns of $W_1$ are eigenvectors of $C$. The same holds for $W_2$. $\square$

**Error of the conditional mean (proved for Gaussian inputs).** Let $x \sim N(0, I)$ and $f$ be continuously differentiable with $\mathbb{E}\|\nabla f\|^2 < \infty$. Then $\mathbb{E}[(f - \mathbb{E}[f \mid y])^2] \le \lambda_{n+1} + \cdots + \lambda_m$.

*Proof.* $W$ is orthogonal, so $(y, z)$ is again standard normal, with $y$ and $z$ independent. For fixed $y$, the Gaussian Poincare inequality in $z$, $\operatorname{Var}_z[h(z)] \le \mathbb{E}_z[\|\nabla h(z)\|^2]$, applied to $h(z) = f(W_1 y + W_2 z)$, gives $\mathbb{E}[(f - \mathbb{E}[f \mid y])^2 \mid y] \le \mathbb{E}[\|\nabla_z f\|^2 \mid y]$. Take the expectation over $y$ and use the previous result. $\square$

So small trailing eigenvalues guarantee that the best function of $y$ alone is close to $f$ in mean square.

## Classic examples

**A ridge function.** Let $f(x) = \sin(x_1 + x_2)$ with $x \sim N(0, I_2)$. Then $\nabla f = \cos(x_1 + x_2)(1, 1)^{\mathsf T}$ and every gradient is parallel to $(1, 1)$. With $s = x_1 + x_2 \sim N(0, 2)$, $\mathbb{E}[\cos^2 s] = \frac{1}{2} + \frac{1}{2} e^{-4} = 0.5091578$, so $C = 0.5091578$ times the all-ones matrix, with eigenvalues $1.0183156$ and 0 and eigenvector $(1, 1)/\sqrt{2}$. The estimate $\hat C$ has rank one for every $M$, so $\hat\lambda_2 = 0$ and the direction is exact. With seed 1, $\hat\lambda_1$ is 1.435, 0.973, 0.998 and 1.021 for $M = 10, 100, 1000, 10000$. Every function of the form $h(a^{\mathsf T} x)$ has a rank one $C$ in the same way.

**A rotated quadratic.** Let $f(x) = \frac{1}{2} x^{\mathsf T} A x$ in three inputs, $x \sim N(0, I_3)$, with $A = Q \operatorname{diag}(1, 0.5, 0.1) Q^{\mathsf T}$ and $Q$ the Householder reflection of $(1, 1, 1)/\sqrt{3}$. Then $\nabla f = A x$ and $C = A^2$, with eigenvalues 1, 0.25 and 0.01, and leading eigenvector $w_1 = (1, -2, -2)/3$. The diagonal of $C$, the mean squared partial derivatives, is $(0.227, 0.477, 0.557)$: no single input stands out, yet one direction carries $1 / 1.26 = 79$ percent of the mean squared gradient. Monte Carlo estimates with seed 1:

| $M$ | $\hat\lambda_1$ | $\hat\lambda_2$ | $\hat\lambda_3$ | angle of $\hat w_1$ to $w_1$ |
|---|---|---|---|---|
| 10 | 0.759 | 0.068 | 0.0053 | 23.3 degrees |
| 100 | 0.807 | 0.245 | 0.0104 | 4.08 degrees |
| 1000 | 0.987 | 0.238 | 0.0102 | 0.094 degrees |
| 10000 | 1.007 | 0.244 | 0.0101 | 0.213 degrees |

The direction is accurate long before the eigenvalues are, because the gap between $\lambda_1$ and $\lambda_2$ is large. The error does not fall monotonically with $M$ for one seed.

**Contrast with principal component analysis.** [PCA](/principal-component-analysis/) of the inputs of both examples sees the identity covariance and finds no preferred direction. Active subspaces use the function, through its gradients, and find the direction that matters.

**Global sensitivity.** Constantine and Diaz define activity scores $\sum_{j \le n} \lambda_j w_{ij}^2$ for each input $i$. With $n = m$ the score is $C_{ii} = \mathbb{E}[(\partial f / \partial x_i)^2]$, the derivative-based measure, which bounds the total [Sobol index](/sobol-indices/) of input $i$ by a Poincare inequality. Screening by the [Morris method](/morris-method/) estimates a related average of derivatives without gradients.

## Variations

- **Finite difference and gradient-free estimates.** Use differences when no adjoint exists, or fit a global linear or quadratic model and take its gradients.
- **Bootstrap.** Resample the gradients to get intervals for the eigenvalues and for the distance between subspaces.
- **Different weights.** Use the outer products of the gradients of several outputs, or of a misfit function in a Bayesian inverse problem, where the active subspace is the data-informed one.
- **Ridge approximation.** Fit $g(W_1^{\mathsf T} x)$ by optimizing $W_1$ and $g$ together from function values only, without gradients.
- **Nonlinear analogues.** Active manifolds and kernel methods look for curved low dimensional structure.

## Pitfalls

- **Scaling of inputs.** The eigenvectors depend on the units. Normalize the inputs before computing gradients.
- **No linear structure.** For $f = \|x\|^2$ with $x \sim N(0, I)$, $\nabla f = 2 x$ and $C = 4 I$: all eigenvalues are equal and there is no active subspace, though $f$ depends on the single scalar $\|x\|$. The method sees only linear combinations.
- **Too few gradients.** With $M$ small, the eigenvalues are biased and the subspace is wrong when the gap is small, as the first row of the table shows. Use the bootstrap.
- **Noisy gradients.** Finite differences of a model with solver noise add a noise matrix to $\hat C$, which hides small eigenvalues.
- **Dependent or bounded inputs.** The rotated variables $y$ and $z$ are not independent when $x$ is not Gaussian, and the range of $y$ on a box is a zonotope, not a box. Account for this when fitting $g$ or integrating over $y$.

## Exercises

1. Show that $\lambda_i = \mathbb{E}[(w_i^{\mathsf T} \nabla f)^2]$ and that $\operatorname{tr} C = \mathbb{E}[\|\nabla f\|^2]$.
2. For $f(x) = h(a^{\mathsf T} x)$, show that $C = \mathbb{E}[h'(a^{\mathsf T} x)^2]\, a a^{\mathsf T}$ has rank at most one.
3. Compute $C$ for $f(x) = \sin(x_1 + x_2)$ with $x$ uniform on $[-1, 1]^2$ and compare it with the Gaussian case.
4. Prove that $\hat C$ has rank at most $\min(M, m)$, and explain why at least $n$ gradients are needed to find an $n$ dimensional subspace.
5. For $f = \frac{1}{2} x^{\mathsf T} A x$ with symmetric $A$ and $x \sim N(0, I)$, show that $C = A^2$.

## References
