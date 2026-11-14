---
tag: Y17GAM
kind: algorithm
slug: taubin-smoothing
name: Taubin smoothing
aliases:
- lambda-mu smoothing
area: cad/mesh-processing
level: core
summary: Alternates a shrinking Laplacian step with factor lambda and an expanding one with factor mu < -lambda, a low-pass filter that smooths without shrinking.
model: real-ram
complexity:
  vars: {n: the number of vertices, K: the number of passes}
  time: {worst: Θ(K n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1995
  people: [Gabriel Taubin]
  note: Taubin wrote one Laplacian step as a filter on the eigenvectors of the Laplacian and added a second step with a negative factor, so that the low frequencies keep their size.
prereqs: [laplacian-smoothing, laplacian-matrix, polygon-mesh]
see_also: [implicit-fairing, cotangent-laplacian, fir-filter, butterworth-filter, chebyshev-polynomials, spectral-partitioning, discrete-fourier-transform, isotropic-remeshing]
sources:
  - paper: doi:10.1145/218380.218473
    title: Gabriel Taubin, A signal processing approach to fair surface design, Proceedings of SIGGRAPH 95, 1995, 351 to 358
    locator: the lambda-mu algorithm, its transfer function (1 - lambda k)(1 - mu k), and the pass-band frequency 1/lambda + 1/mu
  - paper: doi:10.1109/ICCV.1995.466848
    title: Gabriel Taubin, Curve and surface smoothing without shrinkage, Proceedings of the Fifth International Conference on Computer Vision (ICCV), 1995, 852 to 857
    locator: the same two-step filter for curves and surfaces, with the analysis of the shrinkage of plain Laplacian smoothing
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 4, Smoothing (the spectral view of Laplacian smoothing and the lambda-mu filter)
---

Taubin smoothing repeats a pass of two [Laplacian smoothing](/laplacian-smoothing/) steps, $x \leftarrow x + f\,U(x)$, first with a positive factor $f = \lambda$, which shrinks, and then with a negative factor $f = \mu < -\lambda$, which inflates. $U(x)_i$ is the umbrella vector, the centroid of the neighbours of vertex $i$ minus $x_i$. On the eigenvectors of the uniform Laplacian, a pass multiplies the part of frequency $k$ by $(1 - \lambda k)(1 - \mu k)$. This factor is about 1 for low frequencies, the overall shape, and well below 1 for high frequencies, the noise. So the method is a low-pass filter, and a closed mesh keeps its size, where plain Laplacian smoothing shrinks it to a point. A pass costs $\Theta(n)$ time.

## In plain words

Plain smoothing moves each corner a bit toward the middle of its neighbours. That removes bumps, but it also pulls a round shape inward, a little at every step.

Taubin's idea is to follow each such step by a step the other way, slightly larger, which pushes each corner away from the middle of its neighbours. A large bump, such as the round shape itself, is pulled in by the first step and pushed back out by the second, and stays about the same. A small sharp bump is cut down a lot by the first step. The second step then pushes back only a little of it, so the bump stays small. After a few pairs of steps the noise is gone and the shape has kept its size.

## The problem

The input is a triangle mesh with vertex positions $x_1, \ldots, x_n \in \mathbb{R}^3$, two factors $\lambda > 0$ and $\mu < -\lambda$, a number of passes $K$, and a set $F$ of fixed vertices, by default the border vertices. The output is new positions with the same connectivity, with the high frequencies damped and the low frequencies kept. As for [Laplacian smoothing](/laplacian-smoothing/), there is no single target shape. The user picks $\lambda$, $\mu$ and $K$.

## The algorithm

Let $N(i)$ be the neighbours of vertex $i$, $d_i = |N(i)|$, and $c_i = \frac{1}{d_i}\sum_{j \in N(i)} x_j$.

```pseudo id=main
TAUBIN-SMOOTH(x[1 .. n], faces, λ, μ, K, F)
L1  require λ > 0 and μ < −λ; N ← the neighbour lists; F ← the border vertices if not given
L2  for k ← 1 to K do
L3      for each factor f in (λ, μ) do
L4          for each vertex i ∉ F do y_i ← x_i + f (c_i − x_i)     ▷ c_i from the old x
L5          y_i ← x_i for each i ∈ F
L6          x ← y
    return x
```

Write $G = I - D^{-1}A$ for the uniform Laplacian of the edge graph, with $A$ the adjacency matrix and $D = \operatorname{diag}(d_i)$, so that $U(x) = -Gx$. On a closed mesh, one pass is

$$x \leftarrow (I - \mu G)(I - \lambda G)\, x.$$

$G$ has real eigenvalues $0 = k_1 \le k_2 \le \cdots \le k_n \le 2$, the *frequencies*, and a basis of eigenvectors. A pass multiplies the part of $x$ along an eigenvector of frequency $k$ by the transfer function

$$f(k) = (1 - \lambda k)(1 - \mu k).$$

It has $f(0) = 1$, and $f(k) = 1$ again at the *pass-band frequency*

$$k_{PB} = \frac{1}{\lambda} + \frac{1}{\mu},$$

which is positive because $\mu < -\lambda$. Values of $k_{PB}$ from about $0.01$ to $0.1$ are the usual choice. With $\lambda = 0.33$ and $\mu = -0.34$, as in the code, $k_{PB} = \frac{50}{561} \approx 0.089$.

## Example

**The six modes of a hexagon.** Take a closed polygon with 6 vertices, the graph of a cycle, where each vertex has the two neighbours $i \pm 1$. The eigenvectors of $G$ are $x_i = \cos(\pi m i / 3)$ with frequencies $k = 1 - \cos(\pi m / 3)$, that is $k = 0, \frac{1}{2}, \frac{3}{2}, 2$ for $m = 0, 1, 2, 3$. Use one coordinate and $\lambda = \frac{33}{100}$, $\mu = -\frac{34}{100}$.

For $m = 1$, $x = (1, \frac{1}{2}, -\frac{1}{2}, -1, -\frac{1}{2}, \frac{1}{2})$. At vertex 0 the neighbours average to $\frac{1}{2}$, so the $\lambda$ step gives $1 + \frac{33}{100}(\frac{1}{2} - 1) = \frac{167}{200}$. All other vertices scale by the same factor $1 - \frac{\lambda}{2}$. The $\mu$ step then scales by $1 + \frac{34}{200}$, and $x_0$ ends at $\frac{167}{200} \cdot \frac{234}{200} = \frac{19539}{20000} = 0.97695$. For $m = 3$, $x = (1, -1, 1, -1, 1, -1)$, the noisiest shape. The $\lambda$ step gives $x_0 = 1 - 2\lambda = \frac{17}{50}$ and the $\mu$ step multiplies by $1 - 2\mu = \frac{168}{100}$, so $x_0 = \frac{357}{625} = 0.5712$.

| $k$ | $f(k)$, one Taubin pass | $(1 - \lambda k)^2$, two Laplacian steps |
|---|---|---|
| 0 | 1 | 1 |
| $1/2$ | $0.97695$ | $0.697225$ |
| $3/2$ | $0.76255$ | $0.255025$ |
| 2 | $0.5712$ | $0.1156$ |

Both damp the noise, but the two Laplacian steps also cut the low mode $k = \frac{1}{2}$ by 30 percent, and the Taubin pass cuts it by 2 percent. On a longer cycle the lowest modes have $k$ near 0 and are kept almost exactly.

**A sphere.** On the icosphere with 162 vertices on the unit sphere, 10 Taubin passes with $\lambda = 0.33$, $\mu = -0.34$ change the volume by the measured factor $1.0064$. Twenty Laplacian steps with $\lambda = 0.33$, the same work, give $0.409$. After 50 passes the factors are $1.032$ and $0.0116$.

## Correctness

These are proved in the correctness file:

- **A pass is the matrix product.** Lines L3 to L6 compute $(I - \mu G)(I - \lambda G)x$ on the free rows and keep the fixed rows. The tests compare the code with the product of the two step matrices exactly.
- **The transfer function.** On a closed mesh, an eigenvector of $G$ with frequency $k$ is multiplied by $f(k)$ in each pass. The tests check this exactly on the hexagon.
- **The shape of $f$.** For $\lambda > 0 > \mu$ and $\lambda + \mu < 0$, $f(0) = f(k_{PB}) = 1$, $f(k) > 1$ for $0 < k < k_{PB}$, and $f$ decreases on $[k_{PB}, 2]$. So every frequency above $k_{PB}$ is damped and the method is stable, exactly when $f(2) = (1 - 2\lambda)(1 - 2\mu) > -1$. The largest gain is $1 + \frac{(\lambda + \mu)^2}{-4\lambda\mu}$, which is $1.00022$ for the factors above.
- **Affine invariance and the weighted centroid.** Each step is an affine combination with weights summing to 1, and on a closed mesh each step keeps $\sum_i d_i x_i$, as for [Laplacian smoothing](/laplacian-smoothing/).

The gain above 1 means that Taubin smoothing does not converge as $K$ grows. The frequencies in $(0, k_{PB})$ grow slowly, which is why the measured volume of the sphere grows by 3 percent in 50 passes. The method is a filter used for a fixed small $K$, not an iteration to a limit. The volume figures above are measured, not proved.

## Complexity

The neighbour lists take $O(n)$ time to build. Each pass does two Laplacian steps, each with $\sum_i d_i \le 6n$ additions and one division per free vertex, so $K$ passes take $\Theta(Kn)$ time on the [real RAM](/real-ram/). The extra space is the array $y$ and the lists, $\Theta(n)$. The cost is twice that of $K$ Laplacian steps.

## Properties

- **A polynomial filter.** $K$ passes apply the polynomial $f(k)^K$ of degree $2K$ to the spectrum of $G$, without computing any eigenvector. This is a [finite impulse response filter](/fir-filter/) on the mesh graph.
- **No shrinkage in the low band.** Frequencies below $k_{PB}$ are kept or very slightly amplified. Plain Laplacian smoothing damps every nonzero frequency.
- **Linear.** The result is a linear function of the input positions, so noise added to a shape is filtered on its own. A test checks this exactly on a cycle.
- **Exact.** With rational input and rational factors, all values are exact.
- **Connectivity-dependent.** With the uniform weights, the frequencies depend on the graph, not on the geometry, and flat irregular regions drift inside the plane.

## Variants and improvements

- **Other weights.** Use the [cotangent weights](/cotangent-laplacian/), or Fujiwara's inverse edge-length weights, in place of the uniform average. The spectral analysis then holds for the generalized eigenproblem of the weighted Laplacian.
- **Other polynomials.** Taubin, Zhang and Golub (1996) designed polynomial low-pass filters of higher degree with a sharper cut-off than $(1 - \lambda k)(1 - \mu k)$, evaluated with the recurrence of the [Chebyshev polynomials](/chebyshev-polynomials/). The [Butterworth filter](/butterworth-filter/) is a 1-D analogue.
- **Implicit steps.** [Implicit fairing](/implicit-fairing/) solves a linear system per step and is stable for any step size, at a higher cost per step.
- **Curves.** The same two steps smooth a closed polygon, as in the hexagon example, and any graph with positions.

## When to use it

Use it to remove noise from a scanned or reconstructed mesh without changing its size, when a fast explicit method is wanted and the noise is at the scale of a few edges. It is the default non-shrinking smoother in many mesh libraries. Use [implicit fairing](/implicit-fairing/) when the mesh is irregular and the geometry should decide the smoothing, and [Laplacian smoothing](/laplacian-smoothing/) when shrinking does not matter or the border is fixed and close.

## Pitfalls

- **$\mu$ too close to $-\lambda$.** Then $k_{PB}$ is near 0 and almost everything is damped, as in plain smoothing. If $|\mu|$ is much larger than $\lambda$, $k_{PB}$ is large and the low band grows.
- **Too many passes.** The gain above 1 in $(0, k_{PB})$ makes the low frequencies grow. Hundreds of passes inflate the mesh slowly.
- **$\lambda$ too large.** If $\lambda \ge 1/\sqrt{2}$, then $-\mu > \lambda$ gives $f(2) = -(2\lambda - 1)(1 - 2\mu) < -(4\lambda^2 - 1) \le -1$, and the highest frequencies grow with alternating sign.
- **Wrong order of steps.** The two step matrices commute, so the order does not change the linear map. But doing all $\lambda$ steps first and then all $\mu$ steps can lose precision in floating point, because the intermediate shape is tiny.
- **A free border.** On an open mesh without fixed vertices, the border moves inward in the $\lambda$ step and outward in the $\mu$ step, and does not stay where it was.

## Implementations

## History

Taubin published the method in 1995, in a SIGGRAPH paper on fair surface design and in an ICCV paper on curve and surface smoothing without shrinkage, while he was at IBM. He viewed the vertex positions as a signal on the mesh graph, the eigenvectors of the Laplacian as its frequencies, and plain Laplacian smoothing as a filter with transfer function $1 - \lambda k$. The second step with a negative factor gave a low-pass filter. In 1996 Taubin, Zhang and Golub designed sharper polynomial filters, and in 1999 Desbrun, Meyer, Schröder and Barr replaced the explicit steps by [implicit fairing](/implicit-fairing/) with cotangent weights.

## References
