---
tag: 32F5AB
kind: model
slug: murphy-yield-model
name: Murphy yield model
aliases:
- Murphy's yield formula
area: eda/power-reliability-and-manufacturability
level: core
summary: Murphy's yield model ((1 - e^(-A D)) / (A D))^2 that averages the Poisson yield over a triangular distribution of defect density.
prereqs: [poisson-yield-model]
see_also: [negative-binomial-yield-model, critical-area, jensens-inequality, moment-generating-function, method-of-moments]
sources:
  - paper: doi:10.1109/PROC.1964.3442
    title: B. T. Murphy, Cost-size optima of monolithic integrated circuits, Proceedings of the IEEE 52(12), 1537 to 1545, December 1964
    locator: the yield as the Poisson yield averaged over a distribution of defect densities, with the delta, rectangular and triangular densities, and the triangular one chosen as a stand-in for a bell-shaped density
  - paper: "R. B. Seeds, Yield, economic, and logistic models for complex digital arrays, IEEE International Convention Record, part 6, 1967"
    locator: the exponential density of defect densities and the yield 1/(1 + AD) that it gives (page range not confirmed)
  - paper: doi:10.1147/rd.276.0545
    title: R. Meister, On Murphy's yield formula, IBM Journal of Research and Development 27(6), 545 to 548, November 1983
    locator: the comparison of Murphy's mixture yields with the Poisson yield at the same mean defect density
  - paper: doi:10.1109/PROC.1983.12619
    title: C. H. Stapper, F. M. Armstrong and K. Saji, Integrated circuit yield statistics, Proceedings of the IEEE 71(4), 453 to 470, April 1983
    locator: the survey of compound Poisson yield models, with Murphy's and Seeds' formulas as special mixing densities
---

Murphy's yield model gives the fraction of good chips as $Y = \big( (1 - e^{-A D_0}) / (A D_0) \big)^2$, where $A$ is the average [critical area](/critical-area/) of the chip and $D_0$ is the mean defect density. It is the [Poisson yield](/poisson-yield-model/) $e^{-AD}$ averaged over a defect density $D$ that varies from chip to chip with a triangular density on $[0, 2D_0]$. Murphy proposed it in 1964 because the Poisson model predicted too low a yield for large chips. The shape of the density is a modeling choice and $D_0$ is fitted to fab data; neither comes from the physics of defects.

## The machine

**Two levels of randomness.** Each chip has its own defect density $D \ge 0$, drawn from a density $g$ with mean $D_0$. Given $D$, defects fall on the chip as in the Poisson model, so the chip has no fault with probability $e^{-AD}$. Then the yield is the [expected value](/expected-value/) over $D$:

$$ Y \;=\; E\big[e^{-AD}\big] \;=\; \int_0^\infty e^{-AD} g(D)\, dD. $$

This is the [moment generating function](/moment-generating-function/) of $D$ evaluated at $-A$. Every model of this page and of the [negative binomial page](/negative-binomial-yield-model/) is this one integral with a different $g$.

**Murphy's triangular density.** Murphy took $g$ to be the triangle on $[0, 2D_0]$ with its peak at $D_0$:

$$ g(D) = \frac{D}{D_0^2} \text{ for } 0 \le D \le D_0, \qquad g(D) = \frac{2D_0 - D}{D_0^2} \text{ for } D_0 < D \le 2D_0, \qquad g(D) = 0 \text{ otherwise}. $$

**Claim.** With this $g$, $Y = \Big( \dfrac{1 - e^{-A D_0}}{A D_0} \Big)^2$.

**Proof.** Let $U_1$ and $U_2$ be independent and uniform on $[0, D_0]$. The density of $U_1 + U_2$ at $D$ is the length of $\{u \in [0, D_0] : D - u \in [0, D_0]\}$ divided by $D_0^2$, which is $D / D_0^2$ for $D \le D_0$ and $(2D_0 - D)/D_0^2$ for $D_0 < D \le 2D_0$. So $D$ has the law of $U_1 + U_2$. By independence,

$$ E\big[e^{-A(U_1 + U_2)}\big] = \Big( E\big[e^{-A U_1}\big] \Big)^2 = \Big( \frac{1}{D_0} \int_0^{D_0} e^{-Au}\, du \Big)^2 = \Big( \frac{1 - e^{-A D_0}}{A D_0} \Big)^2. \qquad \square $$

**Rectangular density.** Murphy also computed the uniform density on $[0, 2D_0]$, which gives, by the same one-variable integral,

$$ Y = \frac{1 - e^{-2 A D_0}}{2 A D_0}. $$

**Seeds' exponential density.** Seeds took $g(D) = e^{-D/D_0} / D_0$. Then

$$ Y = \frac{1}{D_0} \int_0^\infty e^{-AD} e^{-D/D_0}\, dD = \frac{1}{D_0} \cdot \frac{1}{A + 1/D_0} = \frac{1}{1 + A D_0}. $$

## What it counts

The same quantity as the Poisson model: the probability that a chip has no fault from random spot defects, now averaged over the spread of the defect density between wafers and between regions of a wafer. The input is $\lambda = A D_0$, the mean number of faults per chip. The parameters are fitted: $D_0$ from yields of products or test chips, and the choice between the triangular, rectangular and exponential shapes from how $\ln Y$ bends as the chip area grows. Murphy chose the triangle as a computable stand-in for a bell-shaped density of $D$, not because defect densities are triangular.

**Values.** With $\lambda = A D_0$:

| $\lambda$ | Poisson $e^{-\lambda}$ | Murphy triangular | rectangular | Seeds $1/(1+\lambda)$ |
|---|---|---|---|---|
| 0.5 | 0.6065 | 0.6193 | 0.6321 | 0.6667 |
| 1 | 0.3679 | 0.3996 | 0.4323 | 0.5000 |
| 2 | 0.1353 | 0.1869 | 0.2454 | 0.3333 |
| 4 | 0.0183 | 0.0602 | 0.1250 | 0.2000 |

At small $\lambda$ all four agree; the difference is in large chips.

## Relation to other models

- **Poisson.** A point mass at $D_0$ gives back $e^{-AD_0}$, and for any $g$ with mean $D_0$, $Y \ge e^{-AD_0}$ by [Jensen's inequality](/jensens-inequality/), as proved on the [Poisson page](/poisson-yield-model/). Meister studied this comparison for Murphy's formulas.
- **Negative binomial.** The gamma density with shape $\alpha$ and mean $D_0$ gives $(1 + A D_0/\alpha)^{-\alpha}$. Seeds' model is the case $\alpha = 1$, because the gamma density with shape 1 is the exponential density.
- **Ordering by spread.** The variances of $D$ are $0$ for Poisson, $D_0^2/6$ for the triangle, $D_0^2/3$ for the rectangle and $D_0^2$ for the exponential. The table above has the same order: a wider $g$ gives a higher yield at the same mean.

## Known results in the model

**Second-order agreement.** Expand $e^{-AD} = 1 - AD + \frac{1}{2}A^2 D^2 - R$, where $0 \le R \le \frac{1}{6} A^3 D^3$ for $D \ge 0$. Then $Y = 1 - A D_0 + \frac{1}{2} A^2 (D_0^2 + \sigma^2) - E[R]$ with $\sigma^2$ the variance of $D$, so two mixing densities with the same mean and variance give yields that differ by at most $\frac{1}{6} A^3 \max(E[D^3], E[D'^3])$. The triangle has $\sigma^2 = D_0^2/6$, the same as the gamma density with $\alpha = 6$, so Murphy's formula and the negative binomial formula with $\alpha = 6$ agree to second order in $A D_0$: at $\lambda = 0.5$ they give $0.6193$ and $0.6186$. They part at large $\lambda$, where Murphy's yield decays like $1/\lambda^2$ and the negative binomial yield like $\lambda^{-6}$.

**Large-chip behavior.** As $\lambda \to \infty$: the Poisson yield falls as $e^{-\lambda}$, the triangle as $\lambda^{-2}$, the rectangle as $1/(2\lambda)$ and Seeds as $1/\lambda$. The decay rate is set by the mass of $g$ near $D = 0$, since a density with $g(D) \approx c D^{k}$ near zero gives $Y \approx c\, k! / A^{k+1}$ (Watson's lemma). Large chips are good only when some wafers or regions are nearly clean, and the model's tail is only as good as its $g$ near zero.

**Fitting.** Given yields $Y_j$ of products with critical areas $A_j$ in one process, $D_0$ is chosen to fit the curve, for example by least squares on $\ln Y_j$ or by [maximum likelihood](/maximum-likelihood-estimation/) on counts of good and bad chips. Murphy's model has only $D_0$ to fit; the [negative binomial model](/negative-binomial-yield-model/) adds a shape parameter, so it can fit how fast $\ln Y$ bends with the area as well as its level.

## References
