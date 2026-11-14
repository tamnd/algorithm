---
tag: 8V48ZJ
kind: model
slug: poisson-yield-model
name: Poisson yield model
aliases:
- Poisson defect model
area: eda/power-reliability-and-manufacturability
level: intro
summary: The yield model Y = e^(-A D), with A the critical area and D the defect density, which assumes defects fall independently and uniformly.
prereqs: [critical-area, poisson-distribution]
see_also: [murphy-yield-model, negative-binomial-yield-model, voronoi-critical-area-extraction, jensens-inequality, design-centering]
sources:
  - paper: doi:10.1109/PROC.1964.3442
    title: B. T. Murphy, Cost-size optima of monolithic integrated circuits, Proceedings of the IEEE 52(12), 1537 to 1545, December 1964
    locator: the yield of a chip of area A at a uniform defect density D as exp(-AD), and the observation that it underestimates the yield of large chips
  - paper: doi:10.1109/PROC.1983.12619
    title: C. H. Stapper, F. M. Armstrong and K. Saji, Integrated circuit yield statistics, Proceedings of the IEEE 71(4), 453 to 470, April 1983
    locator: the derivation of the Poisson yield formula from randomly placed faults, its product form over defect types, and its relation to the compound Poisson models
  - paper: doi:10.1147/rd.276.0549
    title: C. H. Stapper, Modeling of integrated circuit defect sensitivities, IBM Journal of Research and Development 27(6), 549 to 557, November 1983
    locator: the average critical area as the area that multiplies the defect density in the yield formula
---

The Poisson yield model says that the fraction of chips with no defect-caused fault is $Y = e^{-\bar A D}$, where $\bar A$ is the average [critical area](/critical-area/) of the chip and $D$ is the density of spot defects per unit area. It follows from one assumption: defects land on the wafer independently and uniformly, with the same density on every chip, so that the number of faults on a chip has a [Poisson distribution](/poisson-distribution/). The density $D$ is not derived; it is fitted to the yield or the defect monitors of a fab. Real defects cluster, and the [Murphy](/murphy-yield-model/) and [negative binomial](/negative-binomial-yield-model/) models correct for that by averaging this model over a random $D$.

## The machine

**Defects.** Spot defects of one type form a spatial Poisson process on the wafer with intensity $D$ per unit area: the number of defects in a region of area $a$ is Poisson with mean $D a$, and the counts in disjoint regions are independent. Each defect has an independent radius with density $f$ and its centre is uniform in its region.

**Chip.** A chip occupies a window $W$ and has the critical area function $A(r)$ of its layout, with average $\bar A = \int A(r) f(r)\, dr$. A defect is a *fault* if its centre lies in the critical region for its radius.

**Claim.** The number $K$ of faults on the chip is Poisson with mean $\lambda = D \bar A$, and the yield is $Y = P(K = 0) = e^{-D \bar A}$.

**Proof.** The number $N$ of defects in $W$ is Poisson with mean $\mu = D \operatorname{area}(W)$. Given $N = n$, the $n$ defects are independent, and each is a fault with probability $p = \int \frac{A(r)}{\operatorname{area}(W)} f(r)\, dr = \bar A / \operatorname{area}(W)$, because its centre is uniform on $W$ and its radius is independent of the centre. So, given $N = n$, $K$ is binomial with parameters $n$ and $p$, and

$$ P(K = k) = \sum_{n \ge k} e^{-\mu} \frac{\mu^n}{n!} \binom{n}{k} p^k (1-p)^{n-k} = e^{-\mu} \frac{(\mu p)^k}{k!} \sum_{j \ge 0} \frac{(\mu (1-p))^j}{j!} = e^{-\mu p} \frac{(\mu p)^k}{k!}. $$

This is the Poisson distribution with mean $\mu p = D \bar A$, and $k = 0$ gives $Y = e^{-D \bar A}$. This step is the *thinning* property of the Poisson process. $\square$

**Several defect types.** If defect types $i = 1, \dots, q$ (metal shorts, metal opens, via opens, particles on each layer) are independent Poisson processes with densities $D_i$ and average critical areas $\bar A_i$, the chip works only if each type causes no fault, so

$$ Y = \prod_{i=1}^{q} e^{-D_i \bar A_i} = \exp\Big( -\sum_{i=1}^{q} D_i \bar A_i \Big). $$

The model is closed under this product: the chip behaves as one Poisson model with $\lambda = \sum_i D_i \bar A_i$.

## What it counts

The model counts *random defect-limited yield*: the probability that no spot defect lands where it breaks or shorts a net. It does not count parametric yield loss, where every net is intact but timing or power is out of specification (the subject of [design centering](/design-centering/)), nor systematic loss from lithography or fill problems. Fits of real data often multiply it by a constant $Y_0 \le 1$ for such gross losses, so $Y = Y_0 e^{-D \bar A}$.

Its one free parameter is $D$. A fab estimates it from the yield of a product or a test chip with known critical area, as $D = -\ln(Y)/\bar A$, or from defect monitor structures. In early work, and in many quick estimates today, $\bar A$ is replaced by the chip area, which mixes the defect density with the fraction of the chip that is sensitive.

**Example.** With $\bar A = 1\ \mathrm{cm}^2$ and $D = 0.5\ \mathrm{cm}^{-2}$, $Y = e^{-0.5} = 0.6065$. Doubling the critical area to $2\ \mathrm{cm}^2$ gives $e^{-1} = 0.3679$, the square of the first yield. The model always says that a chip twice as large has the square of the yield, because the two halves fail independently.

## Relation to other models

- **Compound Poisson models.** If $D$ varies from chip to chip with a density $g$, and the Poisson model holds given $D$, then the yield is $Y = E[e^{-\bar A D}] = \int_0^\infty e^{-\bar A D} g(D)\, dD$. The [Murphy model](/murphy-yield-model/) takes a triangular $g$, Seeds takes an exponential $g$, and the [negative binomial model](/negative-binomial-yield-model/) takes a gamma $g$. The Poisson model is the case of a point mass at $D_0$.
- **Limit of the negative binomial model.** The negative binomial yield $(1 + \bar A D_0/\alpha)^{-\alpha}$ tends to $e^{-\bar A D_0}$ as the clustering parameter $\alpha \to \infty$; the proof is on that page.
- **Binomial form.** If a chip has $n$ independent sites, each failed with probability $\bar A D / n$, the yield is $(1 - \bar A D/n)^n$, which tends to $e^{-\bar A D}$ as $n \to \infty$. This is the classical limit of the binomial to the Poisson distribution.

## Known results in the model

**The Poisson model is the most pessimistic mixture.** For any density $g$ of $D$ on $[0, \infty)$ with mean $D_0$,

$$ E[e^{-\bar A D}] \;\ge\; e^{-\bar A D_0}. $$

*Proof.* The function $x \mapsto e^{-\bar A x}$ is convex, so [Jensen's inequality](/jensens-inequality/) gives $E[e^{-\bar A D}] \ge e^{-\bar A E[D]}$. Equality holds only when $D$ is constant with probability 1, since the function is strictly convex. $\square$

So, at the same mean defect density, any variation of $D$ between chips raises the predicted yield. Murphy noted in 1964 that $e^{-AD}$ predicted too low a yield for large chips, and the averaged models were his answer. For a fixed $\lambda = \bar A D_0 = 1$ the Poisson yield is $0.3679$, Murphy's triangular model gives $0.3996$, and the negative binomial model with $\alpha = 2$ gives $0.4444$.

**Area scaling.** Under the Poisson model $\ln Y$ is linear in $\bar A$ with slope $-D$. A plot of $\ln Y$ against chip critical area for several products of one process is a direct test of the model: curvature upward means the density varies between chips and a compound model fits better.

**Sensitivity.** $\partial Y / \partial \bar A = -D\, Y$, so each unit of critical area removed by a layout change raises the yield by $D\,Y$ per unit. This is the yield gain that [redundant via insertion](/redundant-via-insertion/) and wire spreading are scored by.

## References
