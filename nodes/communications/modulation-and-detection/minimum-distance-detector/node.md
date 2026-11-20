---
tag: NW9AYJ
kind: algorithm
slug: minimum-distance-detector
name: Minimum distance detector
aliases:
- minimum Euclidean distance detector
area: communications/modulation-and-detection
level: intro
summary: Choose the constellation point closest to the received sample. For PAM, square QAM and PSK a slicer finds it in O(1) time, and it is the ML decision for equal priors in white Gaussian noise.
solves: [symbol-detection]
model: real-ram
complexity:
  vars: {M: the number of constellation points, n: the number of real dimensions of a point}
  time: {worst: Θ(1)}
  time_general_constellation: {worst: Θ(M n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact_ml_in_awgn: true, separable_for_square_qam: true}
history:
  year: 1965
  people: [John M. Wozencraft, Irwin M. Jacobs]
  note: Wozencraft and Jacobs made the geometric view of the optimum receiver, with decision regions around the signal points, the standard textbook treatment in 1965. Kotelnikov had treated optimum detection in Gaussian noise in his 1947 thesis.
prereqs: [symbol-detection, signal-constellation, additive-white-gaussian-noise-channel]
see_also: [symbol-error-rate, gray-labeling, max-log-demapping, soft-demapping, closest-vector-problem, fincke-pohst-enumeration, mimo-detection, voronoi-diagram]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 4.2-1 (optimal detection for the vector AWGN channel, the minimum distance rule) and Sections 4.3-1 to 4.3-3 (the detectors and error probabilities for PAM, PSK and QAM)
  - book: isbn:9780792375487
    title: John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004
    locator: Chapter 5, Pulse-Amplitude Modulation (the section on the one-shot minimum-distance receiver), and Chapter 7, Probabilistic Detection
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Appendix A, Detection and estimation in additive Gaussian noise (detection in the scalar and vector Gaussian channel)
  - book: isbn:9780881335545
    title: John M. Wozencraft and Irwin M. Jacobs, Principles of Communication Engineering, Wiley, 1965 (reissued by Waveland Press, 1990)
    locator: Chapter 4, Optimum receiver principles (vector channels, decision regions and the probability of error)
---

The minimum distance detector takes a received sample and chooses the point of a known [signal constellation](/signal-constellation/) that is nearest to it in Euclidean distance. For equally likely symbols in [additive white Gaussian noise](/additive-white-gaussian-noise-channel/), this is the maximum likelihood decision, so it solves the [symbol detection](/symbol-detection/) problem exactly in that case. For [pulse amplitude modulation](/pulse-amplitude-modulation/), square [QAM](/quadrature-amplitude-modulation/) and [phase-shift keying](/phase-shift-keying/), a *slicer* finds the nearest point in a constant number of operations, without computing all $M$ distances. The problem page states the general MAP and ML rules; this page is the algorithm for the Gaussian case with equal priors. It differs from the binary threshold tests of [signal detection](/signal-detection/) and the [Neyman-Pearson lemma](/neyman-pearson-lemma/), which decide between two hypotheses with a chosen false alarm rate, not among $M$ symbols.

## In plain words

A transmitter sends one of a few agreed points, for example one of sixteen dots on a grid. Noise moves the point a little, so the receiver gets a dot that is near the sent one but usually not on it. The receiver picks the agreed dot that is nearest to what it got. When the noise is the usual random hiss and each dot is equally likely, no other rule makes fewer mistakes.

The receiver does not need to measure the distance to every dot. On a grid, it rounds the horizontal position and the vertical position to the nearest grid line, one at a time. On a circle of dots, it rounds the angle to the nearest dot angle. Each rounding is a few operations, however many dots there are.

## The problem

The receiver sees one complex sample after the [matched filter](/matched-filter/):

$$y = h x + w, \qquad x \in \mathcal{A} = \{a_0, \ldots, a_{M-1}\}, \qquad w \sim \mathcal{CN}(0, N_0).$$

The gain $h \ne 0$ is known; it includes the amplitude $\sqrt{E_s}$ and any channel phase. The points $a_i$ have unit average energy, and $a_i$ carries the bit label $i$ (the Gray labels of the [Gray labeling](/gray-labeling/) page). The symbols are equally likely. The output is the index

$$\hat\imath = \arg\min_{0 \le i < M} |y - h a_i|^2.$$

The SNR is $E_s/N_0 = |h|^2/N_0$ per complex symbol. The real and imaginary parts of $w$ are independent, each with variance $N_0/2$.

## The algorithm

Let $L$ be the number of levels on one axis: $L = M$ for $M$-PAM and $L = \sqrt{M}$ for square $M$-QAM. The raw amplitudes on an axis are $L - 1 - 2m$ for $m = 0, \ldots, L - 1$, and level $m$ has the Gray label $g(m) = m \oplus \lfloor m/2 \rfloor$. The unit-energy points are the raw points divided by $\sqrt{(M^2 - 1)/3}$ for PAM and by $\sqrt{2(M - 1)/3}$ for QAM. The $M$-PSK point with level $k$ is $e^{j(2\pi k/M + \phi_0)}$ and has the label $g(k)$.

```pseudo id=main
SLICE-AXIS(u, L)                     ▷ u is in raw units: the levels are L-1, L-3, ..., -(L-1)
L1  m ← ⌊(L - 1 - u)/2 + 1/2⌋         ▷ the nearest level index
L2  m ← min(max(m, 0), L - 1)          ▷ clamp to the outer levels
L3  return g(m)

DETECT-PAM(y, h, M)
L4  u ← Re(y / h) · sqrt((M² - 1)/3)
L5  return SLICE-AXIS(u, M)

DETECT-QAM(y, h, M)                  ▷ M = L², the label is the in-phase bits, then the quadrature bits
L6  z ← (y / h) · sqrt(2(M - 1)/3)
L7  return SLICE-AXIS(Re z, L) · L + SLICE-AXIS(Im z, L)

DETECT-PSK(y, h, M, φ0)
L8  θ ← arg(y / h) - φ0
L9  k ← ⌊M θ / (2π) + 1/2⌋ mod M        ▷ the nearest point on the circle
L10 return g(k)
```

Line L4 and line L6 remove the gain and undo the unit-energy scaling, so the levels of each axis are the odd integers. For PAM, the imaginary part of $y/h$ does not change the decision, because all points are real. For a constellation with no such structure, the detector computes all $M$ distances; the reference code of the area does this by brute force.

## Example

**16-QAM.** Take $h = 1$ and $y = 0.5 - 0.2j$. Line L6 gives $z = \sqrt{10}\,y = 1.5811 - 0.6325j$, with $L = 4$.

| step | in-phase | quadrature |
|---|---|---|
| $u$ | $1.5811$ | $-0.6325$ |
| $(L - 1 - u)/2$ | $0.7094$ | $1.8162$ |
| $m$ after L1 and L2 | $1$ | $2$ |
| raw level $L - 1 - 2m$ | $+1$ | $-1$ |
| label $g(m)$ | $1$ = 01 | $3$ = 11 |

Line L7 returns $1 \cdot 4 + 3 = 7$, the bits 0111, and the point $(1 - j)/\sqrt{10} = 0.3162 - 0.3162j$. Its squared distance to $y$ is $0.04728$. The next two points are index 3, $(3 - j)/\sqrt{10}$, at $0.21483$, and index 5, $(1 + j)/\sqrt{10}$, at $0.30026$. A search over all 16 points gives the same index 7.

**8-PSK with a channel.** Take $\phi_0 = 0$, $h = 0.6 + 0.8j$ and $y = -0.9 + 0.3j$. Then $y/h = -0.3 + 0.9j$, and line L8 gives $\theta = 1.8925$ rad (108.4 degrees). Line L9 gives $M\theta/(2\pi) = 2.4097$, so $k = 2$: the point at 90 degrees. Line L10 returns $g(2) = 3$, the bits 011.

## Correctness

The detector is exact: for every $y$ it returns an index that minimizes $|y - h a_i|^2$, and this index is a maximum likelihood decision. Three facts give this. First, the Gaussian density makes the likelihood a decreasing function of $|y - h a_i|^2$. Second, $|y - h a|^2 = |h|^2 |y/h - a|^2$, so the problem is the nearest point to $z = y/h$ in the unit-energy constellation. Third, for PAM and square QAM the squared distance is a sum of one term for each axis, and each term is smallest at the rounded level, clamped to the outer levels; for PSK the distance to a point on the unit circle depends only on the angle between them. Ties occur only on the boundaries of the decision regions, a set of probability zero, and there any of the tied points is a maximum likelihood decision. The full proof is below.

## Complexity

In the [real RAM](/real-ram/) with a floor operation, each of DETECT-PAM, DETECT-QAM and DETECT-PSK does a constant number of operations: one complex division, one or two scalings, at most two floors and clamps, and one or two Gray conversions $m \oplus \lfloor m/2 \rfloor$ on a small integer. The cost does not depend on $M$. The extra space is $\Theta(1)$, and no table of points is needed.

A general constellation of $M$ points in $n$ real dimensions costs $\Theta(M n)$ per symbol by exhaustive search. For a vector channel $y = Hx + w$ with $x \in \mathcal{A}^n$, maximum likelihood detection is a [closest vector problem](/closest-vector-problem/) over a finite part of a [lattice](/lattice/), and exhaustive search costs $M^n$ distance evaluations of $O(nm)$ each for $m$ receive dimensions. The per-axis slicer does not solve that problem; see [MIMO detection](/mimo-detection/).

## Properties

- **Exact for equal priors in white Gaussian noise.** It minimizes the symbol error probability among all detectors in that model.
- **Decision regions.** The region of each point is its Voronoi cell, the set of samples nearer to it than to any other point (see [Voronoi diagram](/voronoi-diagram/)). For square QAM the cells are rectangles, and the outer cells are unbounded. For PSK they are wedges of angle $2\pi/M$.
- **Invariant to the scale of $h$ for PSK.** DETECT-PSK uses only the angle of $y/h$, so an error in $|h|$ does not change its decisions. PAM and QAM need the exact $|h|$, because their decision boundaries scale with it.
- **Hard output.** The detector gives one point and its bits, not a reliability. A decoder that needs soft inputs uses [soft demapping](/soft-demapping/) or [max-log demapping](/max-log-demapping/) instead; the max-log form reuses the same slicer for each bit.

## Variants and improvements

- **MAP with unequal priors.** Minimize $|y - h a_i|^2 - N_0 \ln \pi_i$, where $\pi_i$ is the prior of point $i$. This needs $N_0$, which the minimum distance rule does not.
- **Colored noise.** With noise covariance $K$, whiten first: minimize $(y - Hx)^H K^{-1} (y - Hx)$.
- **Lattice decoding.** For a large constellation cut from a [lattice](/lattice/), round in the lattice coordinates and then check the boundary. Sphere decoders such as [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) solve the vector case exactly with less work than exhaustive search at high SNR.
- **APSK.** For points on several rings, deciding the ring by the radius and then the phase on that ring is fast but is not always the nearest point; an exact slicer must also check the neighbors on the adjacent rings. See [amplitude and phase-shift keying](/amplitude-and-phase-shift-keying/).

## When to use it

Use the slicer whenever the constellation is PAM, square QAM or PSK, the noise is white and Gaussian, and the symbols are equally likely; it is the standard hard decision device after an equalizer or a single-tap OFDM channel correction. Use the exhaustive form for an irregular constellation of a few dozen points. When the decision feeds a soft-input decoder, compute LLRs instead of hard decisions.

## Pitfalls

- **The wrong scale.** If the transmit points are $\sqrt{E_s}$ times the unit points, $h$ must include $\sqrt{E_s}$. A slicer for raw amplitudes $\pm 1, \pm 3$ applied to unit-energy samples decides wrongly for every outer point.
- **Rounding at a half.** Python's `round` rounds a half to the even integer; this is a tie, and either choice is correct, but code must not rely on one fixed answer at a boundary. The pseudocode uses $\lfloor t + 1/2 \rfloor$.
- **Forgetting the clamp.** A sample beyond the outer level gives an index outside $0, \ldots, L - 1$ without line L2.
- **Cross and other non-square QAM.** 32-QAM and 128-QAM have no corner points, so independent slicing of the two axes can return a point that does not exist.
- **Not ML outside the model.** With unequal priors, impulsive noise, phase noise or an imperfect estimate of $h$, the nearest point is not the most likely one.
- **Dividing by a small $h$.** The division in lines L4, L6 and L8 is safe for the decision, because a scale does not change the order of distances, but $y/h$ has the noise variance $N_0/|h|^2$. Use the scaled form when you also need the noise level, for example for LLRs.

## Implementations

## History

The rule that the best receiver for equally likely signals in white Gaussian noise picks the nearest signal follows from the likelihood ratio tests of statistical decision theory. Kotelnikov treated optimum reception of known signals in Gaussian noise in his 1947 doctoral thesis, published in English in 1959 as *The Theory of Optimum Noise Immunity*. Wozencraft and Jacobs, in *Principles of Communication Engineering* (1965), presented the receiver as a geometric decision in signal space, with a decision region around each signal point, and this became the textbook form.

## References
