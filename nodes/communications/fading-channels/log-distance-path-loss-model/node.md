---
tag: 3DJP5Q
kind: model
slug: log-distance-path-loss-model
name: Log-distance path loss model
aliases:
- path loss exponent model
area: communications/fading-channels
level: intro
summary: "The mean path loss PL(d0) + 10 n log10(d/d0) in dB, a straight line in log distance whose slope n is fitted to measurements: 2 in free space, about 2.7 to 5 in cities."
prereqs: [free-space-path-loss]
see_also: [log-normal-shadowing, okumura-hata-model, free-space-path-loss, least-squares-problem, maximum-likelihood-estimation, multipath-fading]
sources:
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 4.9.1 (log-distance path loss model, the choice of the reference distance and the table of path loss exponents for different environments)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 2.6 (simplified path-loss model) and Section 2.5.4 (piecewise linear, or multislope, model)
  - paper: doi:10.1109/49.778178
    title: V. Erceg, L. J. Greenstein, S. Y. Tjandra, S. R. Parkoff, A. Gupta, B. Kulic, A. A. Julius and R. Bianchi, An empirically based path loss model for wireless channels in suburban environments, IEEE Journal on Selected Areas in Communications 17(7), 1999
    locator: pp. 1205 to 1211 (measurements in suburban macrocells, with the exponent fitted as a function of the base antenna height and the terrain category)
---

The log-distance path loss model says that the mean path loss in dB grows linearly with the logarithm of the distance: $\mathrm{PL}(d) = \mathrm{PL}(d_0) + 10 n \log_{10}(d / d_0)$. The slope $n$ is the path loss exponent. It is 2 in [free space](/free-space-path-loss/), and in real environments it is fitted to measurements. The model gives only the mean over an area; [log-normal shadowing](/log-normal-shadowing/) adds the random spread around it, and the [Okumura-Hata model](/okumura-hata-model/) is a more detailed fit of the same form for cellular systems.

## The machine

The model has three parameters, all fitted to measurements in one kind of environment:

- the reference distance $d_0$ (m), in the far field of the antennas and inside the range of the measurements;
- the loss $\mathrm{PL}(d_0)$ (dB) at $d_0$, which is measured or taken from the free-space formula at $d_0$;
- the path loss exponent $n$ (no unit).

For $d \ge d_0$ the mean path loss is

$$\overline{\mathrm{PL}}(d) = \mathrm{PL}(d_0) + 10 n \log_{10}\frac{d}{d_0} \quad \text{dB}.$$

In linear form, the mean received power is $\overline{P}_r(d) = P_t K (d_0 / d)^n$ with $K = 10^{-\mathrm{PL}(d_0)/10}$ for unit antenna gains. Goldsmith calls this the simplified path-loss model and writes $\gamma$ for $n$; for omnidirectional antennas and free space up to $d_0$, $K = (\lambda / (4 \pi d_0))^2$.

The "mean" is the local mean: the received power in dB, averaged over a few tens of wavelengths to remove the [multipath fading](/multipath-fading/), and then over many places at the same distance to remove the shadowing. Typical choices of $d_0$ are 1 m indoors, 100 m in microcells and 1 km in large cells (Rappaport, Section 4.9.1).

## What it counts

The model predicts the mean loss at each distance, and from it the mean received power $P_t + G_t + G_r - \overline{\mathrm{PL}}(d)$ in dBm. It also gives the distance at which the mean loss reaches a budget $\mathrm{PL}_{\max}$:

$$d_{\max} = d_0 \cdot 10^{(\mathrm{PL}_{\max} - \mathrm{PL}(d_0)) / (10 n)} .$$

**Measured exponents.** These values are measurements, not results of a theory. Rappaport (Section 4.9.1) lists 2 for free space, 2.7 to 3.5 for urban cellular radio, 3 to 5 for shadowed urban cellular radio, 1.6 to 1.8 for line of sight inside buildings, 4 to 6 for obstructed paths inside buildings and 2 to 3 for obstructed paths in factories. Erceg et al. 1999 fit the exponent in suburban macrocells as a function of the base antenna height and the terrain, and they find that it changes from one cell to the next.

**Example.** Indoors at 2.4 GHz, take $d_0 = 1$ m and the free-space value $\mathrm{PL}(d_0) = 40.05$ dB. With $n = 3$, the loss at 100 m is $40.05 + 30 \cdot 2 = 100.05$ dB, and with $n = 3.5$ it is 110.05 dB. Free space gives 80.05 dB at 100 m. A small change of the exponent changes the prediction by many dB at large distances.

## Relation to other models

- **Free space** is the case $n = 2$ with $\mathrm{PL}(d_0)$ from the Friis formula.
- **Two-ray ground reflection** gives $n = 2$ before the critical distance $4 h_t h_r / \lambda$ and $n = 4$ after it. A *dual-slope* or *multislope* model has a different exponent on each range of distance, joined at break points (Goldsmith, Section 2.5.4).
- **Okumura-Hata.** For fixed antenna heights, the Hata formula is a log-distance model. Its slope is $44.9 - 6.55 \log_{10} h_b$ dB per decade, so $n = 3.52$ for a base antenna of 30 m and $n = 3.18$ for 100 m.
- **Log-normal shadowing** adds a Gaussian term $X_\sigma$ in dB: $\mathrm{PL}(d) = \overline{\mathrm{PL}}(d) + X_\sigma$. The same fit gives $n$ and $\sigma$.
- **Multipath fading** ([Rayleigh](/rayleigh-fading-channel/), [Rician](/rician-fading-channel/)) is a third factor on top of the two.

## Known results in the model

1. **Differences do not depend on the intercept.** For $d_1, d_2 \ge d_0$, $\overline{\mathrm{PL}}(d_2) - \overline{\mathrm{PL}}(d_1) = 10 n \log_{10}(d_2 / d_1)$. So the loss grows by $10n$ dB per decade and by $10 n \log_{10} 2 = 3.01 n$ dB per doubling of the distance.
2. **Range and power.** If the power budget grows by $\Delta$ dB, the range is multiplied by $10^{\Delta / (10 n)}$, and the covered area by the square of that. With $\Delta = 6$ dB, the range grows by a factor of 2.0 for $n = 2$ and by a factor of 1.41 for $n = 4$.
3. **Interference and reuse.** With equal transmit powers and only path loss, a user at distance $R$ from its base station and $D$ from an interfering one has the signal to interference ratio $(D / R)^n$. For $D = 3R$ this is 9.54 dB with $n = 2$ and 19.08 dB with $n = 4$. A large exponent hurts the range but helps the reuse of frequencies.
4. **The least squares fit.** Let the measurements be $(d_i, \mathrm{PL}_i)$, $i = 1, \ldots, N$, with $\mathrm{PL}(d_0)$ fixed, and put $x_i = 10 \log_{10}(d_i / d_0)$ and $y_i = \mathrm{PL}_i - \mathrm{PL}(d_0)$. The [least squares](/least-squares-problem/) estimate minimizes $J(n) = \sum_i (y_i - n x_i)^2$. $J$ is a quadratic in $n$ with $J''(n) = 2 \sum_i x_i^2 > 0$, so its only minimum is where $J'(n) = -2 \sum_i x_i (y_i - n x_i) = 0$:
   $$\hat n = \frac{\sum_i x_i y_i}{\sum_i x_i^2}, \qquad \hat\sigma^2 = \frac1N \sum_i (y_i - \hat n x_i)^2 .$$
   If the residuals are independent and Gaussian in dB, as in the shadowing model, these are the [maximum likelihood estimates](/maximum-likelihood-estimation/) of $n$ and $\sigma^2$. Divide by $N - 1$ instead of $N$ to remove the bias of $\hat\sigma^2$.
5. **A worked fit.** Take $d_0 = 10$ m, $\mathrm{PL}(d_0) = 60$ dB, and five made-up measurements: 72 dB at 20 m, 85 dB at 50 m, 88 dB at 100 m, 101 dB at 200 m and 110 dB at 500 m. Then $x = (3.010, 6.990, 10, 13.010, 16.990)$, $\hat n = 3.04$, the residuals are $(2.84, 3.73, -2.43, 1.41, -1.69)$ dB, and $\hat\sigma = 2.56$ dB (2.86 dB with $N - 1$). The model predicts 120.85 dB at 1 km, a distance outside the data.

### Pitfalls

- **Extrapolation.** A fit is valid only over the distances, frequencies, antenna heights and environment of the measurements. Item 5 predicts 1 km from data that stop at 500 m; that number has no support.
- **Below $d_0$.** The formula is not defined for $d < d_0$. At $d \to 0$ it gives a negative loss.
- **The exponent depends on $d_0$.** Fixing the intercept at the free-space value and fitting only $n$ gives a different $n$ from a fit of both intercept and slope. Report $d_0$, $\mathrm{PL}(d_0)$, $n$ and $\sigma$ together.
- **Averages in dB.** The fit averages losses in dB. The mean of the received power in watts is larger than the power at the mean loss in dB; see [log-normal shadowing](/log-normal-shadowing/).

## References
