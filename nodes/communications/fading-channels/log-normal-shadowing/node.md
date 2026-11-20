---
tag: XAPK6T
kind: model
slug: log-normal-shadowing
name: Log-normal shadowing
aliases:
- shadow fading
- large-scale fading
area: communications/fading-channels
level: core
summary: "Models the slow random change of the local mean power around the path loss, caused by obstacles, as Gaussian in dB with a measured sigma of about 4 to 13 dB."
prereqs: [log-distance-path-loss-model, gaussian-q-function]
see_also: [log-distance-path-loss-model, okumura-hata-model, outage-probability, rayleigh-fading-channel, multipath-fading, central-limit-theorem, autoregressive-model]
sources:
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 2.7 (shadow fading), Section 2.8 (combined path loss and shadowing), Section 2.9 (outage probability under path loss and shadowing) and Section 2.10 (cell coverage area)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 4.9.2 (log-normal shadowing) and Section 4.9.3 (determination of percentage of coverage area)
  - paper: doi:10.1049/el:19911328
    title: M. Gudmundson, Correlation model for shadow fading in mobile radio systems, Electronics Letters 27(23), 1991
    locator: pp. 2145 to 2146 (the exponential autocorrelation of the shadowing in dB along the path of a mobile, fitted to measurements)
---

Log-normal shadowing is the model of the slow random change of the received power around the mean [path loss](/log-distance-path-loss-model/). Buildings, hills and trees block the path by different amounts at different places, so two receivers at the same distance from the transmitter get different local mean powers. The model says that this loss in dB is a Gaussian random variable with mean zero and a standard deviation $\sigma$ that is fitted to measurements. It acts over tens of meters, unlike [multipath fading](/multipath-fading/), which acts over a fraction of a wavelength.

## The machine

The loss at distance $d$ is the mean path loss plus a random term in dB:

$$\mathrm{PL}(d) = \overline{\mathrm{PL}}(d) + X_\sigma, \qquad X_\sigma \sim \mathcal{N}(0, \sigma^2) \ \text{(in dB)},$$

so the local mean received power is $P_r(d) = P_t + G_t + G_r - \overline{\mathrm{PL}}(d) - X_\sigma$ in dBm. The mean $\overline{\mathrm{PL}}(d)$ comes from a path loss model, usually the [log-distance model](/log-distance-path-loss-model/) or the [Okumura-Hata model](/okumura-hata-model/). The linear power gain $\psi = 10^{-X_\sigma/10}$ is log-normal: with $\xi = 10 / \ln 10$, its density is

$$p(\psi) = \frac{\xi}{\sqrt{2 \pi}\, \sigma \psi} \exp\left(-\frac{(10 \log_{10} \psi)^2}{2 \sigma^2}\right), \qquad \psi > 0 .$$

The parameters and the standing assumptions are:

- **$\sigma$ in dB, a measurement.** Goldsmith (Section 2.7) reports that most outdoor studies give $\sigma$ from 4 dB to 13 dB. The same fit gives the exponent of the path loss model and $\sigma$ (see item 4 of the log-distance page).
- **Constant statistics.** $\sigma$ does not depend on the distance, and $X_\sigma$ has mean 0, so $\overline{\mathrm{PL}}$ is the median loss as well as the mean loss in dB.
- **Spatial correlation.** Values at nearby points are correlated. Gudmundson 1991 fitted the autocorrelation $\mathbb{E}[X(u) X(u + \delta)] = \sigma^2 e^{-|\delta| / X_c}$ along the path of a mobile, where $X_c$ is a decorrelation distance fitted to the measurements.
- **Local mean.** $P_r$ is averaged over the multipath fading. The fast fading is a separate factor; see "Relation to other models".

**Why Gaussian in dB.** This is a heuristic, not a theorem. The wave passes through or around several obstacles, and each one multiplies the power by a random factor. In dB the factors add, and by the [central limit theorem](/central-limit-theorem/) a sum of many independent terms is close to Gaussian. Measurements support the fit (Goldsmith, Section 2.7; Rappaport, Section 4.9.2).

## What it counts

The model predicts the probability that the local mean power is below a level. For a receiver that needs at least $P_{\min}$ dBm, the outage probability at distance $d$ is

$$P_{\mathrm{out}}(d) = \Pr[P_r(d) < P_{\min}] = Q\left(\frac{\overline{P}_r(d) - P_{\min}}{\sigma}\right),$$

where $\overline{P}_r(d)$ is the mean received power in dBm and $Q$ is the [Gaussian Q function](/gaussian-q-function/). The proof is one line: $P_r(d) < P_{\min}$ means $X_\sigma > \overline{P}_r(d) - P_{\min}$, and $X_\sigma / \sigma$ is a standard normal variable.

**Example.** A cell edge has the mean power $-100$ dBm, the receiver needs $-110$ dBm, and $\sigma = 8$ dB. Then $P_{\mathrm{out}} = Q(10/8) = Q(1.25) = 0.1056$. About one place in ten at the edge is in outage.

**Fade margin.** To keep the outage at $p$, the mean power must be $M = \sigma Q^{-1}(p)$ dB above $P_{\min}$. With $\sigma = 8$ dB: $M = 1.2816 \cdot 8 = 10.25$ dB for 90 percent coverage at the edge, 13.16 dB for 95 percent and 18.61 dB for 99 percent.

## Relation to other models

- **Path loss.** The [log-distance](/log-distance-path-loss-model/) and [Okumura-Hata](/okumura-hata-model/) models give the mean; shadowing gives the spread around it. Without shadowing, every receiver at one distance has the same power.
- **Multipath fading.** The composite model multiplies three factors: the path loss, the shadowing $\psi$ and a fast fading factor $|h|^2$ with $\mathbb{E}|h|^2 = 1$, for example [Rayleigh](/rayleigh-fading-channel/) or [Rician](/rician-fading-channel/). Shadowing changes over tens of meters, and $h$ changes over half a wavelength. Rayleigh fading with a log-normal mean power is often called the Suzuki model.
- **Correlated samples.** Sampled every $\Delta$ meters along a path, the exponential correlation gives the first-order [autoregressive model](/autoregressive-model/) $X_{k+1} = \rho X_k + \sqrt{1 - \rho^2}\, \sigma g_k$ with $\rho = e^{-\Delta / X_c}$ and $g_k$ independent standard normal. This is how system simulators generate shadowing along a route.
## Known results in the model

1. **Mean and median in watts.** $X_\sigma$ is Gaussian, so $\mathbb{E}[e^{t X_\sigma}] = e^{t^2 \sigma^2 / 2}$. With $t = \ln 10 / 10$, the mean of the linear factor $10^{X_\sigma/10}$ is $e^{(\sigma \ln 10 / 10)^2 / 2}$, and in dB this is $\sigma^2 \ln 10 / 20$. For $\sigma = 8$ dB the mean in watts is 7.37 dB above the median, and for $\sigma = 4$ dB it is 1.84 dB above. The median of the linear factor is 1 (0 dB).
2. **Outage and margin** are the closed forms of "What it counts". They hold in the model: Gaussian $X_\sigma$ in dB with known $\overline{\mathrm{PL}}(d)$ and $\sigma$.
3. **Cell coverage area.** Take a cell of radius $R$, the log-distance mean with exponent $n$, and the power $\overline{P}_r(R)$ at the edge. The fraction of the area of the disk where $P_r > P_{\min}$ is $U = \frac{2}{R^2} \int_0^R r \Pr[P_r(r) > P_{\min}]\, dr$, and in closed form
   $$U = \tfrac12 \left[ \operatorname{erfc}(a) + e^{(1 - 2ab)/b^2} \operatorname{erfc}\left(\frac{1 - ab}{b}\right) \right], \quad a = \frac{P_{\min} - \overline{P}_r(R)}{\sigma \sqrt 2}, \quad b = \frac{10 n \log_{10} e}{\sigma \sqrt 2}$$
   (Goldsmith, Section 2.10; Rappaport, Section 4.9.3). With $\sigma = 8$ dB and $n = 4$, so $b = 1.5355$: an edge mean equal to $P_{\min}$ ($a = 0$, so 50 percent at the edge) covers $U = 0.773$ of the area; a 5 dB margin at the edge gives 0.900, and a 10 dB margin gives 0.967. Inside the cell the mean power is higher, so the area coverage is always larger than the coverage at the edge.
4. **Estimating $\sigma$.** The residuals of the path loss fit in dB estimate $X_\sigma$; their root mean square is the maximum likelihood estimate of $\sigma$ when they are independent.

### Pitfalls

- **dB or watts.** Averaging powers in watts and in dB gives different answers (item 1). A path loss fit in dB predicts the median power, not the mean power.
- **Independent samples.** Samples taken a few meters apart are correlated. A fit that treats them as independent overstates the amount of data, and a simulator with independent shadowing at each step has no slow fades.
- **Links to two base stations.** The shadowing on two links from one mobile is often correlated, because the obstacles near the mobile are the same. Independent shadowing overstates the gain of macrodiversity and handover.
- **Mixing time scales.** The outage on this page is for the local mean. The instantaneous power also has the multipath fade on top; an [outage probability](/outage-probability/) that ignores one of the two factors is optimistic.

## References
