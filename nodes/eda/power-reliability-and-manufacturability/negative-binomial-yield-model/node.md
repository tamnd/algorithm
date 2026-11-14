---
tag: MBXP8F
kind: model
slug: negative-binomial-yield-model
name: Negative binomial yield model
aliases:
- Stapper yield model
- clustered defect yield model
area: eda/power-reliability-and-manufacturability
level: core
summary: Stapper's yield model Y = (1 + A D / alpha)^(-alpha) that adds a clustering parameter alpha to the Poisson model, matching real wafers where defects cluster.
prereqs: [poisson-yield-model]
see_also: [murphy-yield-model, critical-area, redundant-via-insertion, moment-generating-function, method-of-moments, variance]
sources:
  - paper: "C. H. Stapper, Defect density distribution for LSI yield calculations, IEEE Transactions on Electron Devices ED-20(7), 655 to 657, July 1973"
    locator: the gamma distribution of the defect density between chips and the yield (1 + AD/alpha)^(-alpha) that it gives
  - paper: doi:10.1109/PROC.1983.12619
    title: C. H. Stapper, F. M. Armstrong and K. Saji, Integrated circuit yield statistics, Proceedings of the IEEE 71(4), 453 to 470, April 1983
    locator: the negative binomial distribution of the number of faults per chip, its mean and variance, the cluster parameter alpha, the limit to the Poisson model, and the fit to wafer data
  - paper: doi:10.1109/PROC.1964.3442
    title: B. T. Murphy, Cost-size optima of monolithic integrated circuits, Proceedings of the IEEE 52(12), 1537 to 1545, December 1964
    locator: the idea of averaging the Poisson yield over a distribution of defect densities, which this model applies with a gamma density
---

The negative binomial yield model gives the fraction of good chips as $Y = (1 + \lambda/\alpha)^{-\alpha}$, where $\lambda = A D_0$ is the mean number of faults per chip, $A$ the average [critical area](/critical-area/) and $D_0$ the mean defect density. It is the [Poisson yield](/poisson-yield-model/) $e^{-AD}$ averaged over a defect density $D$ that has a gamma distribution between chips, and the number of faults per chip then has a negative binomial distribution. The *cluster parameter* $\alpha > 0$ measures how much the density varies: small $\alpha$ means strong clustering, and $\alpha \to \infty$ gives back the Poisson model. Stapper introduced it in 1973, and both $D_0$ and $\alpha$ are fitted to fab data.

## The machine

**Gamma mixing.** Each chip has a defect density $D$ drawn from the gamma density with shape $\alpha > 0$ and scale $\theta = D_0/\alpha$:

$$ g(D) = \frac{D^{\alpha - 1} e^{-D/\theta}}{\Gamma(\alpha)\, \theta^{\alpha}}, \qquad D > 0, $$

where $\Gamma(\alpha) = \int_0^\infty t^{\alpha-1} e^{-t}\, dt$. The substitution $t = D/\theta$ shows $\int g = 1$, and the same substitution gives $E[D^j] = \theta^j \Gamma(\alpha + j)/\Gamma(\alpha)$, so $E[D] = \alpha\theta = D_0$ and $\operatorname{Var}(D) = \alpha(\alpha+1)\theta^2 - \alpha^2\theta^2 = D_0^2/\alpha$. Given $D$, the chip has a Poisson number $K$ of faults with mean $AD$, as in the Poisson model. The gamma and negative binomial families have no page here, so the facts this page uses about them are derived on it.

**Claim 1 (yield).** $Y = E[e^{-AD}] = (1 + A D_0/\alpha)^{-\alpha}$.

**Proof.** Substitute $t = D(A + 1/\theta)$:

$$ \int_0^\infty e^{-AD} \frac{D^{\alpha - 1} e^{-D/\theta}}{\Gamma(\alpha)\theta^{\alpha}}\, dD = \frac{1}{\Gamma(\alpha)\theta^{\alpha}} \cdot \frac{\Gamma(\alpha)}{(A + 1/\theta)^{\alpha}} = (1 + A\theta)^{-\alpha} = \Big(1 + \frac{A D_0}{\alpha}\Big)^{-\alpha}. \qquad \square $$

**Claim 2 (fault count).** With $\lambda = A D_0$, for $k = 0, 1, 2, \dots$

$$ P(K = k) = \frac{\Gamma(\alpha + k)}{k!\, \Gamma(\alpha)} \cdot \frac{(\lambda/\alpha)^k}{(1 + \lambda/\alpha)^{\alpha + k}}, \qquad E[K] = \lambda, \qquad \operatorname{Var}(K) = \lambda\Big(1 + \frac{\lambda}{\alpha}\Big). $$

**Proof.** $P(K = k) = \int_0^\infty e^{-AD} \frac{(AD)^k}{k!} g(D)\, dD = \frac{A^k}{k!\, \Gamma(\alpha)\theta^{\alpha}} \int_0^\infty D^{\alpha + k - 1} e^{-D(A + 1/\theta)}\, dD = \frac{A^k\, \Gamma(\alpha + k)}{k!\, \Gamma(\alpha)\theta^{\alpha} (A + 1/\theta)^{\alpha + k}}$, and $A\theta = \lambda/\alpha$ turns this into the formula. For the moments, $E[K \mid D] = \operatorname{Var}(K \mid D) = AD$, so $E[K] = A D_0$ and, by the law of total [variance](/variance/), $\operatorname{Var}(K) = E[AD] + \operatorname{Var}(AD) = \lambda + A^2 D_0^2/\alpha$. $\square$

The count has more variance than a Poisson count with the same mean. That excess, $\lambda^2/\alpha$, is what "clustering" means in the model.

## What it counts

The probability that a chip has no fault from random spot defects, when the defect density is constant over one chip but varies between chips, wafers and lots. The two inputs are fitted to fab data: $D_0$ sets the level of the yield and $\alpha$ sets how fast $\ln Y$ bends as the critical area grows. Neither is predicted from the physics. Fits of real data often add a gross yield factor $Y_0 \le 1$, giving $Y = Y_0 (1 + \lambda/\alpha)^{-\alpha}$.

**Estimating $\alpha$.** If defect counts are taken in windows of one fixed area (chips of a test wafer, or windows of a defect inspection map) with sample mean $m$ and sample variance $v > m$, Claim 2 gives the [method of moments](/method-of-moments/) estimate $\hat\alpha = m^2 / (v - m)$. For $m = 0.8$ and $v = 1.12$ this is $\hat\alpha = 0.64/0.32 = 2$, and a chip with $\lambda = 0.8$ then has yield $1.4^{-2} = 0.5102$, against $e^{-0.8} = 0.4493$ for the Poisson model. If $v \le m$ the data show no clustering and the Poisson model is the fit. Maximum likelihood on the counts with the formula of Claim 2 is the usual better estimate.

**Example.** For $\lambda = 1$ and $\alpha = 2$ the fault count has $P(K = 0, 1, 2, 3) = 0.4444, 0.2963, 0.1481, 0.0658$; the Poisson count with the same mean has $0.3679, 0.3679, 0.1839, 0.0613$. Clustering puts more chips at zero faults and more at many faults, and fewer at one or two.

## Relation to other models

**Poisson as the limit.** For fixed $\lambda \ge 0$, $(1 + \lambda/\alpha)^{-\alpha} \to e^{-\lambda}$ as $\alpha \to \infty$, and more precisely

$$ e^{-\lambda} \;\le\; \Big(1 + \frac{\lambda}{\alpha}\Big)^{-\alpha} \;\le\; e^{-\lambda + \lambda^2/(2\alpha)}. $$

*Proof.* For $x \ge 0$, $x - x^2/2 \le \ln(1 + x) \le x$: both sides are 0 at $x = 0$, and the derivatives satisfy $1 - x \le \frac{1}{1+x} \le 1$, because $(1-x)(1+x) = 1 - x^2 \le 1$. Put $x = \lambda/\alpha$ and multiply by $\alpha$: $\lambda - \frac{\lambda^2}{2\alpha} \le \alpha \ln(1 + \lambda/\alpha) \le \lambda$. Negate and exponentiate; the upper bound tends to $e^{-\lambda}$ as $\alpha \to \infty$. $\square$

For $\lambda = 1$: $\alpha = 1$ gives $0.5$, $\alpha = 10$ gives $0.3855$, $\alpha = 100$ gives $0.3697$, and $e^{-1} = 0.3679$. The same limit holds for the whole distribution of $K$: each probability of Claim 2 tends to $e^{-\lambda}\lambda^k/k!$, because $\Gamma(\alpha + k)/(\Gamma(\alpha)\alpha^k) \to 1$ and $(1 + \lambda/\alpha)^{-k} \to 1$.

**Seeds and Murphy.** $\alpha = 1$ makes $g$ exponential and gives Seeds' $1/(1 + \lambda)$. Murphy's triangular density has the same mean and variance as the gamma density with $\alpha = 6$, so the two models agree to second order in $\lambda$; see the [Murphy model](/murphy-yield-model/).

**Ordering.** The yield falls as $\alpha$ grows at fixed $\lambda$, since $\alpha \ln(1 + \lambda/\alpha)$ is increasing in $\alpha$ (its derivative is $\ln(1+x) - \frac{x}{1+x} \ge 0$ with $x = \lambda/\alpha$). So, for the same mean density, more clustering always predicts a higher yield of fault-free chips, down to the Poisson bound.

## Known results in the model

**Product over defect types.** If defect types $i$ have independent gamma densities with their own $\alpha_i$, the yield is $\prod_i (1 + \lambda_i/\alpha_i)^{-\alpha_i}$. If one density $D$ is shared and only the critical areas differ, the model is the single formula with $\lambda = D_0 \sum_i A_i$. The two assumptions give different yields, and the data decide which one to use.

**Defect-tolerant chips.** A chip with spare rows that can repair up to $k$ faults has yield $P(K \le k)$ from Claim 2. For $\lambda = 1$ and $\alpha = 2$, $P(K \le 2) = 0.8889$, against $0.9197$ for the Poisson count: clustering raises the fault-free yield but lowers the repairable yield, because the faults it adds come in groups.

**Scope of $\alpha$.** The derivation assumes that the density is constant over a chip. If clusters are smaller than a chip, part of the clustering acts inside the chip and a fitted $\alpha$ changes with the chip area, so an $\alpha$ fitted on one die size is not automatically valid for another.

**Fitting the yield curve.** For products with critical areas $A_j$ in one process, $\ln Y_j = -\alpha \ln(1 + A_j D_0/\alpha)$. Two products already fix both parameters; more products test the model. The fitted pair is specific to the process, the period and the defect types included.

## References
