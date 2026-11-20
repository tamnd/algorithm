---
tag: BGW13T
kind: definition
slug: coherence-factor
name: Coherence factor
aliases:
- coherence factor weighting
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "The energy of the coherent sum of the delayed channel samples at a pixel, over M times their total energy. It lies in [0, 1] and is used as a pixel weight to suppress clutter and side lobes."
prereqs: [delay-and-sum-beamforming]
see_also: [beamforming, van-cittert-zernike-theorem, speckle, delay-multiply-and-sum, capon-beamformer, plane-wave-compounding, total-focusing-method, saft]
sources:
  - paper: doi:10.1121/1.410562
    title: "Raoul Mallart and Mathias Fink, Adaptive focusing in scattering media through sound-speed inhomogeneities: The van Cittert Zernike approach and focusing criterion, Journal of the Acoustical Society of America 96(6), 1994, 3721 to 3732"
    locator: "the focusing criterion, a ratio of coherent to incoherent energy across the aperture, and its relation to the van Cittert-Zernike theorem (general locator)"
  - paper: doi:10.1109/ULTSYM.1999.849225
    title: "K. W. Hollman, K. W. Rigby and M. O'Donnell, Coherence factor of speckle from a multi-row probe, Proceedings of the 1999 IEEE Ultrasonics Symposium, vol. 2, 1257 to 1260"
    locator: "the coherence factor of speckle and its use as an image weight (general locator)"
---

The coherence factor (CF) of a pixel measures how well the channels of an array agree after the focusing delays. It is the energy of the coherent sum of the delayed samples, the value that [delay-and-sum](/delay-and-sum-beamforming/) (DAS) forms, divided by $M$ times the total energy of the $M$ samples. It is $1$ when all channels hold the same value, as for an echo from a point at the focus, about $1/M$ for independent noise, and lower for clutter and side lobes, where the channels disagree. CF is not a beamformer by itself: in CF weighting, the DAS output of each pixel is multiplied by its CF, or by a power of it, which keeps coherent targets and darkens incoherent parts of the image. Unlike the fixed weights of DAS and other linear [beamforming](/beamforming/), the weight comes from the data of the pixel, so CF weighting is a nonlinear, adaptive method, and it costs only $O(M)$ per pixel.

## Definition

Let $s = (s_1, \ldots, s_M)$ be the delayed channel samples of one pixel: complex (IQ or analytic) values, or real RF values. The **coherence factor** is

$$\operatorname{CF}(s) = \frac{\left|\sum_{i=1}^M s_i\right|^2}{M \sum_{i=1}^M |s_i|^2}$$

for $s \ne 0$, and $\operatorname{CF}(0) = 0$ by convention. With the mean $\bar s$ and the spread $v = \frac1M \sum_i |s_i - \bar s|^2$ of the samples, $\operatorname{CF}(s) = |\bar s|^2 / (|\bar s|^2 + v)$: the fraction of the channel energy that lies in the mean.

**CF weighting** with an exponent $p \ge 0$ replaces the DAS value $\sum_i s_i$ by $\operatorname{CF}(s)^p \sum_i s_i$. The exponent is a design choice that trades the suppression of clutter against the darkening of speckle; $p = 1$ is common, and other values must be tuned for the task.

The definition has these consequences, each proved in proofs/correctness.md.

1. **Range.** $0 \le \operatorname{CF} \le 1$, by the Cauchy-Schwarz inequality. It is $1$ if and only if all samples are equal, and $0$ if and only if they sum to $0$. This is a theorem.
2. **Scale invariance.** $\operatorname{CF}(a s) = \operatorname{CF}(s)$ for every $a \ne 0$, so CF does not depend on the echo strength. The weighted output is homogeneous of degree one.
3. **Noise.** For independent circular complex Gaussian samples of equal variance, $\mathbb{E}[\operatorname{CF}] = 1/M$. This is a theorem for that model.
4. **Speckle.** For the triangular channel correlation $1 - |i - j|/M$, which the van Cittert-Zernike theorem predicts for fully developed speckle at the focus with equal transmit and receive apertures, the ratio of the expected coherent energy to $M$ times the expected total energy is $(2M^2 + 1)/(3M^2)$, near $2/3$. The formula is a theorem for the model; that real speckle follows the model is a heuristic.

### Computing it

```pseudo id=main
CF(s_1 … s_M, p)                          ▷ returns CF and the weighted value
L1  C ← |Σ_i s_i|²                         ▷ coherent energy
L2  E ← M Σ_i |s_i|²                       ▷ M times the incoherent energy
L3  if E = 0 then CF ← 0
L4  else CF ← C / E
L5  y ← CF^p · Σ_i s_i                     ▷ CF weighting of the DAS value
```

All lines run in $O(M)$ time per pixel, the same order as DAS itself. For an image, the delayed samples come from any delay-based method: focused lines, [synthetic transmit aperture](/synthetic-transmit-aperture/), [TFM](/total-focusing-method/), [SAFT](/saft/) or [plane-wave compounding](/plane-wave-compounding/).

## Examples and non-examples

**Perfect agreement.** $s = (1, 1, 1, 1)$ gives $|4|^2 / (4 \cdot 4) = 1$. Any constant nonzero vector gives $1$, whatever its phase.

**One channel.** $s = (1, 0, 0, 0)$ gives $1/(4 \cdot 1) = 1/4 = 1/M$: a signal on one channel only is as incoherent as independent noise on average.

**Cancellation.** $s = (1, -1, 1, -1)$ gives $0$. The DAS value is $0$ too, but CF also says that the zero comes from disagreement, not from silence.

**Partial agreement.** $s = (3, 1, 1, 1)$ gives $36 / (4 \cdot 12) = 0.75$. The DAS value $6$ becomes $4.5$ with $p = 1$ and $3.375$ with $p = 2$.

**Noise.** For $M = 8$ independent complex Gaussian samples, the mean CF over 3000 trials in the test is within $0.01$ of $1/8$.

**Speckle.** The triangular coherence gives $0.671875$ for $M = 8$ and $0.66675$ for $M = 64$. A simulation with this correlation matches $M = 8$ within $0.03$.

**A non-example: a strong point off the focus.** A bright scatterer that is not at the pixel gives samples with a phase ramp across the array. CF is low, though the DAS value can be large in a side lobe. This is what CF weighting suppresses, and it shows that CF is not a measure of echo strength.

**A non-example: a focusing error.** With a wrong speed of sound, a true point target gives a curved phase across the channels and a CF below $1$, so CF weighting darkens a real target. Mallart and Fink (1994) used a ratio of this kind as a criterion of focusing quality for this reason.

## Related definitions

- [Delay-and-sum beamforming](/delay-and-sum-beamforming/): its output is the coherent sum in the numerator of CF.
- [Van Cittert-Zernike theorem](/van-cittert-zernike-theorem/): it gives the spatial coherence of the echoes from a random medium across the aperture, and so the expected CF of [speckle](/speckle/).
- [Delay-multiply-and-sum](/delay-multiply-and-sum/): another nonlinear combiner that rewards agreement, through pairwise products in place of a ratio of energies.
- [Capon beamformer](/capon-beamformer/): an adaptive beamformer that changes the weights of each channel, not the gain of the pixel.
- Generalized coherence factor: the fraction of the energy of the aperture spectrum (the DFT across the channels) in a few low spatial frequencies, not only at the zero frequency. CF is the case of one frequency.
- Short-lag spatial coherence: an image formed from the normalized correlation of channels at small lags, in place of a weight on DAS.

## References
