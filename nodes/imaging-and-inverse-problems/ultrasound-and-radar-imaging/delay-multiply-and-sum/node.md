---
tag: SF6EBZ
kind: algorithm
slug: delay-multiply-and-sum
name: Delay-multiply-and-sum beamforming
aliases:
- DMAS
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: research
summary: "A nonlinear beamformer that sums the signed square roots of the products of all pairs of delayed channel samples. It rewards channels that agree, and a square of sums makes it O(M) per pixel."
solves: [beamforming]
model: real-ram
complexity:
  vars: {M: the number of array elements, n: the number of pixels along one side of the image}
  time: {worst: O(M n^2)}
  space: {extra: O(M)}
properties: {deterministic: true, linear_in_data: false, recursive: false, exact: true}
history:
  year: 2015
  people: [Giulia Matrone, Alessandro Stuart Savoia, Giosue Caliano, Giovanni Magenes]
  note: "Lim, Nhung, Li and Thang (2008) introduced delay-multiply-and-sum for confocal microwave imaging of the breast. Matrone, Savoia, Caliano and Magenes (2015) applied it to B-mode ultrasound with a band-pass filter at the second harmonic."
prereqs: [delay-and-sum-beamforming, dynamic-receive-focusing]
see_also: [beamforming, coherence-factor, capon-beamformer, plane-wave-compounding, b-mode-image-formation, total-focusing-method, analytic-signal, speckle]
sources:
  - paper: doi:10.1109/TMI.2014.2371235
    title: "Giulia Matrone, Alessandro Stuart Savoia, Giosue Caliano and Giovanni Magenes, The delay multiply and sum beamforming algorithm in ultrasound B-mode medical imaging, IEEE Transactions on Medical Imaging 34(4), 2015, 940 to 949"
    locator: "the definition with signed square roots, the O(M) computation, the band-pass filtered version at 2 f0, and the comparison with delay-and-sum (general locator)"
  - paper: doi:10.1109/TBME.2008.919716
    title: "Hooi Been Lim, Nguyen Thi Tuyet Nhung, Er-Ping Li and Nguyen Duc Thang, Confocal microwave imaging for breast cancer detection: delay-multiply-and-sum image reconstruction algorithm, IEEE Transactions on Biomedical Engineering 55(6), 2008, 1697 to 1704"
    locator: "the original pairwise product algorithm for microwave imaging (general locator)"
---

Delay-multiply-and-sum (DMAS) is a nonlinear combiner for [beamforming](/beamforming/). It uses the same delayed channel samples $s_1, \ldots, s_M$ as [delay-and-sum](/delay-and-sum-beamforming/) (DAS), but in place of the sum $\sum_i s_i$ it adds the products of all pairs, each with a signed square root so that the output keeps the units of the input: $y = \sum_{i<j} \operatorname{sign}(s_i s_j) \sqrt{|s_i s_j|}$. A pair contributes a positive value when the two channels agree in sign and a negative value when they do not, so the output is large only where many channels agree. DAS is linear and treats a strong echo on a few channels the same as a weak echo on all of them; DMAS favors the second case. With the signed roots $r_i$, the pair sum is $((\sum r_i)^2 - \sum r_i^2)/2$, so DMAS costs $O(M)$ per pixel, not $O(M^2)$.

## In plain words

After the delays, each element of the array holds one number for the point you want to see. The usual method adds them up. DMAS instead takes every pair of elements and asks whether they agree. Two elements that agree add to the score, two that disagree take away from it. An echo that truly comes from the point is seen the same way by all elements, so all pairs agree and the score is high. Noise and echoes from other places are seen differently by different elements, so the pairs cancel. A square root on each product keeps the result at the same scale as a plain sum.

## The problem

The input of the combiner is a real vector $s = (s_1, \ldots, s_M)$: the RF samples of the $M$ channels after the focusing delays of one pixel, as in [dynamic receive focusing](/dynamic-receive-focusing/). The output is the real number $y(s)$ above. For an image, the combiner is applied at every pixel of an $n \times n$ grid; the RF image is then band-pass filtered, envelope detected and log compressed as in [B-mode image formation](/b-mode-image-formation/).

## The algorithm

```pseudo id=main
DMAS(s_1 … s_M)                         ▷ returns the pair sum y
L1  r_i ← sign(s_i) √|s_i| for i = 1 … M     ▷ signed square roots
L2  R ← Σ_i r_i
L3  E ← Σ_i |s_i|                        ▷ equals Σ_i r_i²
L4  return (R² - E) / 2
```

Line L4 is the square of the sum minus the diagonal, which leaves twice the sum over the pairs $i < j$. In an image, a pixel loop computes the delayed samples (by interpolation of the RF traces at the two-way time) and calls DMAS in place of the plain sum.

## Example

For $s = (4, 1, -1, 9)$, line L1 gives $r = (2, 1, -1, 3)$, line L2 gives $R = 5$, line L3 gives $E = 15$, and line L4 gives $(25 - 15)/2 = 5$. The six pairs give $2 - 2 + 6 - 1 + 3 - 3 = 5$, the same value. DAS gives $4 + 1 - 1 + 9 = 13$. The channel with the value $-1$ disagrees with the other three, and in DMAS it takes away from three pairs.

The tests simulate $M = 16$ elements with pitch 0.3 mm, a plane wave at normal incidence, one scatterer of amplitude 1 at $(0, 6)$ mm, $f_0 = 5$ MHz, $f_s = 40$ MHz and a Gaussian envelope with $\sigma_t = 0.1$ us. The lateral profile is the largest modulus of the RF output over depths from 5.9 to 6.1 mm, normalized to its peak:

| combiner | peak | value at x = 0.3 mm | largest side lobe at abs(x) at least 0.6 mm |
|---|---|---|---|
| DAS | 15.11 | 0.329 | 0.131 |
| DMAS | 113.33 | 0.095 | 0.029 |

At the scatterer the 16 delayed samples are almost equal, so DMAS is close to $\binom{16}{2} = 120$ times one sample, and $120 \cdot 15.11/16 = 113.3$. These are measurements on this simulation without noise and without the band-pass filter; they depend on the array, the pulse and the scene.

## Correctness

Line L4 equals the pair sum because each signed product is $r_i r_j$ and $r_i^2 = |s_i|$. With $E = \sum |s_i|$, the output lies between $-E/2$ and $\frac{M-1}{2} E$, and the upper bound holds only when all delayed samples are equal: by the Cauchy-Schwarz inequality, DMAS measures how well the channels agree. The output is homogeneous of degree one in the magnitude, $y(a s) = |a|\, y(s)$, so it loses the sign: for equal channels it is a rectified copy of the signal, with its spectrum at $0$ and $2 f_0$. This is a theorem, and it explains the band-pass filter at $2 f_0$ of filtered DMAS. The proofs are in proofs/correctness.md.

## Complexity

In the real-RAM model, lines L1 to L4 cost $O(M)$ per pixel, so an $n \times n$ image costs $O(M n^2)$, the same order as DAS, with $O(M)$ extra space for the delayed samples. The defining pair sum costs $O(M^2)$ per pixel. The square root in L1 is one more operation per channel; on hardware the products and the filter cost more than the sum of DAS.

## Properties

- Nonlinear: the output of a sum of two scenes is not the sum of the outputs, so cross terms between scatterers appear.
- Homogeneous of degree one in the magnitude, even in the sign: $y(-s) = y(s)$.
- Gain $M(M-1)/2$ for perfectly aligned channels, against $M$ for DAS, and a negative output where the channels cancel.
- The signed square root is a design choice that keeps the units; other exponents give other trade-offs between contrast and speckle. Treat it as tuned, not as derived.
- Matrone et al. (2015) explain the narrower main lobe by the pairwise products, which act like the autocorrelation of the receive aperture and so like a wider virtual aperture. This is a heuristic argument; the side-lobe and resolution gains are measurements.

## Variants and improvements

- **Filtered DMAS (F-DMAS).** A band-pass filter around $2 f_0$ on the RF image removes the DC part of the rectified output before envelope detection (Matrone et al. 2015).
- **Short-lag DMAS.** Only the pairs with $|i - j|$ up to a lag $L$ enter the sum, which trades resolution for less speckle variance.
- **Synthetic aperture and plane waves.** DMAS can combine the channels of [TFM](/total-focusing-method/) or [plane-wave compounding](/plane-wave-compounding/) data, over elements, angles or both.
- **Other adaptive weights.** The [coherence factor](/coherence-factor/) also rewards agreement, but as a weight on the DAS output; the [Capon beamformer](/capon-beamformer/) solves for data-dependent linear weights.

## When to use it

Use DMAS when contrast and lateral resolution matter more than a linear, well-understood speckle pattern, and the channel data are available after the delays. It is a research method: its nonlinearity changes the speckle statistics and the relation between echo strength and pixel value, so quantitative methods that assume a linear beamformer, such as Doppler and backscatter estimation, should use DAS.

## Pitfalls

- **Using the defining double loop.** It costs $O(M^2)$ per pixel; use the square of sums of L4.
- **No band-pass filter.** The raw output has a strong DC part; envelope detection at $f_0$ on it gives a wrong image. Filter around $2 f_0$ first.
- **Sampling.** The output has energy at $2 f_0$, so the RF sampling must keep that band, or it aliases.
- **IQ data.** The signed square root is defined for real samples. For complex baseband data the sign must be replaced, for example by the phase, and the result is a different method.
- **Linear expectations.** Two equal scatterers do not give twice the output of one, and weak targets near strong ones are suppressed more than with DAS.

## Implementations

## History

Lim, Nhung, Li and Thang (2008) introduced delay-multiply-and-sum to reconstruct images in confocal microwave imaging for the detection of breast cancer. Matrone, Savoia, Caliano and Magenes (2015) brought it to medical ultrasound B-mode imaging with the signed square root and a band-pass filter at the second harmonic, and reported better contrast and resolution than DAS on phantoms and simulations. Many later papers combine it with synthetic aperture and plane-wave imaging.

## References
