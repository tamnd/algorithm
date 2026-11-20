---
tag: 4P6AFK
kind: definition
slug: gaspari-cohn-function
name: Gaspari-Cohn function
aliases:
- Gaspari-Cohn correlation function
area: scientific-computing/data-assimilation
level: advanced
summary: A fifth order piecewise rational function with compact support that is a valid correlation function in up to three dimensions, the standard taper for localization.
prereqs: [positive-definite-matrix, covariance-matrix]
see_also: [covariance-localization, local-ensemble-transform-kalman-filter, ensemble-square-root-filter, ensemble-kalman-filter, kriging, gaussian-process, random-field, lorenz-96-model]
sources:
  - paper: doi:10.1002/qj.49712555417
    title: "G. Gaspari and S. E. Cohn, Construction of correlation functions in two and three dimensions, Quarterly Journal of the Royal Meteorological Society 125(554) (1999) 723-757"
    locator: "eq. (4.10), the compactly supported fifth order function and its positive definiteness in three dimensions"
  - paper: doi:10.1175/1520-0493(2001)129<0123:ASEKFF>2.0.CO;2
    title: "P. L. Houtekamer and H. L. Mitchell, A sequential ensemble Kalman filter for atmospheric data assimilation, Monthly Weather Review 129(1) (2001) 123-137"
    locator: the use of a compactly supported correlation function to localize the ensemble covariance
  - paper: doi:10.1175/1520-0493(2001)129<2776:DDFOBE>2.0.CO;2
    title: "T. M. Hamill, J. S. Whitaker and C. Snyder, Distance-dependent filtering of background error covariance estimates in an ensemble Kalman filter, Monthly Weather Review 129(11) (2001) 2776-2790"
    locator: the Schur product of the ensemble covariance with a compactly supported correlation function
---

The Gaspari-Cohn function is a correlation function of the distance $r$ that equals $1$ at $r = 0$, falls smoothly like a Gaussian and is exactly zero for $r \ge 2c$, where $c$ is the half-width. Gaspari and Cohn (1999) gave it as eq. (4.10): a fifth order piecewise rational function of $r/c$, positive definite in $\mathbb R^3$. Because it has compact support, a matrix of its values is sparse. Because it is positive definite, the Schur product of such a matrix with a sample covariance is again a covariance. This makes it the usual taper of [covariance localization](/covariance-localization/) in ensemble filters, since Houtekamer and Mitchell (2001) and Hamill, Whitaker and Snyder (2001).

## Definition

Let $c > 0$ be the half-width and $z = |r|/c$. The Gaspari-Cohn function is

$$\mathrm{GC}(r; c) = \begin{cases} -\tfrac14 z^5 + \tfrac12 z^4 + \tfrac58 z^3 - \tfrac53 z^2 + 1, & 0 \le z \le 1,\\[2pt] \tfrac1{12} z^5 - \tfrac12 z^4 + \tfrac58 z^3 + \tfrac53 z^2 - 5z + 4 - \tfrac{2}{3z}, & 1 < z < 2,\\[2pt] 0, & z \ge 2. \end{cases}$$

For points $x$ and $x'$ of $\mathbb R^d$ with $d \le 3$, $\rho(x, x') = \mathrm{GC}(|x - x'|; c)$ is a correlation function: for any points $x_1, \ldots, x_m$ the matrix $[\rho(x_i, x_j)]$ is symmetric positive semidefinite with unit diagonal (Gaspari and Cohn 1999). Since $\mathbb R^1$ and $\mathbb R^2$ lie in $\mathbb R^3$, the same holds in one and two dimensions. The code evaluates it in four lines:

```pseudo id=main
GC(r, c)
L1  z <- |r| / c
L2  if z <= 1 then return -z^5/4 + z^4/2 + 5 z^3/8 - 5 z^2/3 + 1
L3  if z < 2 then return z^5/12 - z^4/2 + 5 z^3/8 + 5 z^2/3 - 5 z + 4 - 2/(3 z)
L4  return 0
```

**Properties.** These follow from the formula by direct computation, and the test file checks them.

- At $z = 1$ both pieces have the value $5/24$, and their first four derivatives agree. At $z = 2$ the outer piece and its first three derivatives are zero. As a function of $x \in \mathbb R^3$ it is twice continuously differentiable; the term $\tfrac58|x/c|^3$ has no third derivative at the origin.
- It decreases strictly from $1$ to $0$ on $0 \le z \le 2$.
- Near zero, $\mathrm{GC} = 1 - \tfrac53 z^2 + O(z^3)$. A Gaussian $\exp(-r^2/(2L^2))$ has the same second derivative at zero when $L = c\sqrt{3/10} \approx 0.548c$. This is the usual way to match $c$ to a Gaussian length scale.
- A matrix of its values on a grid has no nonzero entry for points more than $2c$ apart.

## Examples and non-examples

**Values.** With $c = 2$: $\mathrm{GC}(0) = 1$, $\mathrm{GC}(1) = 263/384 \approx 0.685$, $\mathrm{GC}(2) = 5/24 \approx 0.208$, $\mathrm{GC}(3) = 19/1152 \approx 0.0165$ and $\mathrm{GC}(r) = 0$ for $r \ge 4$. For example at $z = 3/2$: $\tfrac{243}{384} - \tfrac{81}{32} + \tfrac{135}{64} + \tfrac{15}{4} - \tfrac{15}{2} + 4 - \tfrac49 = \tfrac{19}{1152}$. The [LETKF](/local-ensemble-transform-kalman-filter/) and [covariance localization](/covariance-localization/) pages use this value in their worked examples.

**A ring of points.** On the ring of 40 points of the [Lorenz-96 model](/lorenz-96-model/), the taper matrix is circulant, and its eigenvalues are the discrete Fourier transform of its first row. With the chordal distance $(40/\pi)\sin(\pi k/40)$, which is the distance in the plane for a circle of circumference $40$, the smallest eigenvalue was positive for every $c$ tested ($2$ to $40$). With the distance along the ring, $\min(k, 40 - k)$, it was positive for $c \le 10.5$ and negative for each tested $c \ge 11$ ($11$, $12$, $15$, $20$, $25$ and $40$): about $-0.00016$ for $c = 11$, $-0.0023$ for $c = 12$ and $-0.066$ for $c = 15$. For $2c \le 20$ the support is at most half the ring, so the matrix is the periodic sum of the matrix on the integers and is positive semidefinite. For a larger $c$ the distance along the ring is not a distance in $\mathbb R^3$, and the matrix is not a correlation matrix. The [EnSRF](/ensemble-square-root-filter/) measurement with $c = 15$ used the distance along the ring, so its taper matrix had a negative eigenvalue; the serial filter does not form the full matrix, and the run still worked.

**Non-examples.**

- The Gaussian $\exp(-r^2/(2L^2))$ is a correlation function in every dimension, but it has no compact support, so the matrix is dense.
- The triangle $\max(0, 1 - z/2)$ is a correlation function on the line but not in two or three dimensions, so on a two-dimensional grid it can give a matrix with negative eigenvalues.
- A Gaussian set to zero beyond a cutoff, or a step that is $1$ up to a distance and $0$ after it, is not positive definite in general.
- The Gaspari-Cohn function of the great circle distance on a sphere is not guaranteed to be positive definite. With the chordal distance it is, because the sphere lies in $\mathbb R^3$.

## Related definitions

- [Positive definite matrix](/positive-definite-matrix/) and [covariance matrix](/covariance-matrix/): what "valid correlation" means for the matrix of weights.
- [Covariance localization](/covariance-localization/): the Schur product of the ensemble covariance with the taper, and the proof that it stays a covariance.
- [Random field](/random-field/), [Gaussian process](/gaussian-process/) and [kriging](/kriging/): other uses of correlation functions of distance. A compactly supported one gives sparse matrices there as well.
- [Local ensemble transform Kalman filter](/local-ensemble-transform-kalman-filter/): the same function used to weight observations instead of covariances.

### History

Gaspari and Cohn built compactly supported correlation functions in two and three dimensions in 1999, for the modelling of error covariances in data assimilation. Their function of eq. (4.10) has the shape of a Gaussian and support $2c$. Two years later Houtekamer and Mitchell and Hamill, Whitaker and Snyder used such functions to localize the covariances of the ensemble Kalman filter.

## References
