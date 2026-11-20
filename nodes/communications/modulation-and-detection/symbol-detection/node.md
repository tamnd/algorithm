---
tag: FN7YTA
kind: problem
slug: symbol-detection
name: Symbol detection
aliases:
- MAP symbol detection
- ML symbol detection
area: communications/modulation-and-detection
level: intro
summary: Decide which point of a known constellation was sent, given a noisy received vector. MAP minimizes the error probability; with equal priors in AWGN it is the minimum distance rule.
model: real-ram
complexity:
  vars: {M: the number of constellation points, n: the number of complex dimensions of a point}
  time: {worst: Θ(M n)}
prereqs: [signal-space-representation, signal-constellation, additive-white-gaussian-noise-channel, bayes-theorem]
see_also: [minimum-distance-detector, symbol-error-rate, signal-detection, neyman-pearson-lemma, likelihood-ratio-test, sufficient-statistic, mimo-detection, union-bound]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 4.1-1 (optimal detection for a general vector channel, the MAP and ML rules), Section 4.2-1 (optimal detection for the vector AWGN channel) and Section 4.2-3 (a union bound on the probability of error of ML detection)
  - book: isbn:9780792375487
    title: John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004
    locator: Chapter 7, Probabilistic Detection (the MAP and ML detectors and their error probability)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Appendix A, Detection and estimation in additive Gaussian noise (scalar and vector detection, sufficient statistics)
  - book: isbn:9780881335545
    title: John M. Wozencraft and Irwin M. Jacobs, Principles of Communication Engineering, Wiley, 1965 (reissued by Waveland Press, 1990)
    locator: Chapter 4, Optimum receiver principles (decision regions, the optimum receiver for vector and waveform channels)
  - paper: doi:10.1007/BF01553893
    title: Sergio Verdú, Computational complexity of optimum multiuser detection, Algorithmica 4, 1989
    locator: pp. 303 to 312 (optimum multiuser detection in synchronous CDMA is NP-hard as the number of users grows)
---

Symbol detection is the problem of deciding which point of a known [signal constellation](/signal-constellation/) was sent, from a received vector that the channel has corrupted with noise. The rule that minimizes the probability of a wrong decision is the maximum a posteriori (MAP) rule. With equally likely symbols it is the maximum likelihood (ML) rule, and in [additive white Gaussian noise](/additive-white-gaussian-noise-channel/) the ML rule chooses the nearest point, which the [minimum distance detector](/minimum-distance-detector/) computes. It is an $M$-ary decision. The binary [signal detection](/signal-detection/) problem of signal processing, with its false alarm constraint and the [Neyman-Pearson lemma](/neyman-pearson-lemma/), is a different question: there the two kinds of error are treated differently, with a limit on one of them, and here all wrong decisions count the same.

## In plain words

A sender and a receiver agree on a small set of signals, and each signal stands for a group of bits. The sender sends one. The receiver gets it with noise added, and it must say which one was sent.

The best guess is the signal that is most probable after the receiver sees the data. To find it, the receiver weighs two things: how well each signal explains the data, and how often each signal is sent. If all signals are sent equally often, only the first thing counts. If the noise is the usual random hiss, the signal that explains the data best is simply the nearest one. So the receiver draws a region around each signal, the set of places nearer to it than to any other, and reports the region where the data fell.

## Definition

**Input.** A constellation $\mathcal{A} = \{a_0, \ldots, a_{M-1}\} \subset \mathbb{C}^n$ of distinct points, prior probabilities $\pi_0, \ldots, \pi_{M-1}$, a received vector $y$, and the conditional densities $p(y \mid a_i)$ of the channel.

**Output.** A decision rule $d$ that maps each $y$ to an index $d(y) \in \{0, \ldots, M - 1\}$.

**Goal.** Minimize the symbol error probability $P_e(d) = \sum_i \pi_i \Pr[d(y) \ne i \mid x = a_i]$, which the [symbol error rate](/symbol-error-rate/) page studies.

**Theorem (MAP is optimal).** The rule $d_{\mathrm{MAP}}(y) = \arg\max_i \pi_i\, p(y \mid a_i)$, with ties broken in any way, minimizes $P_e$ over all rules.

*Proof.* For any rule $d$, the probability of a correct decision is $1 - P_e(d) = \int \pi_{d(y)}\, p(y \mid a_{d(y)})\, dy$, because for each $y$ only the term of the chosen index counts. At each $y$ the integrand is at most $\max_i \pi_i\, p(y \mid a_i)$, and $d_{\mathrm{MAP}}$ reaches this maximum at every $y$. So $1 - P_e(d) \le 1 - P_e(d_{\mathrm{MAP}})$. $\blacksquare$

By [Bayes' theorem](/bayes-theorem/), $\pi_i\, p(y \mid a_i)$ is proportional to the posterior probability of $a_i$, which gives the rule its name. With equal priors, the MAP rule is the ML rule $\arg\max_i p(y \mid a_i)$.

**The Gaussian case.** For $y = a_i + w$ with $w \sim \mathcal{CN}(0, N_0 I_n)$, $\ln p(y \mid a_i) = -n \ln(\pi N_0) - \|y - a_i\|^2 / N_0$. So

$$d_{\mathrm{MAP}}(y) = \arg\min_i \big(\|y - a_i\|^2 - N_0 \ln \pi_i\big), \qquad d_{\mathrm{ML}}(y) = \arg\min_i \|y - a_i\|^2.$$

Expanding the square gives the *correlation form* $d_{\mathrm{ML}}(y) = \arg\max_i \big(\mathrm{Re}(a_i^H y) - \|a_i\|^2/2\big)$, which needs only $M$ inner products. The decision region $\{y : d(y) = i\}$ of the ML rule is the Voronoi cell of $a_i$: the set of points nearer to $a_i$ than to every other point. Each cell is an intersection of half-spaces, bounded by the perpendicular bisectors of $a_i$ and its neighbors.

**The waveform form.** In a waveform channel, the receiver first projects the received signal onto an orthonormal basis of the signal set, as the [signal space representation](/signal-space-representation/) page explains. The projection is a [sufficient statistic](/sufficient-statistic/) in white Gaussian noise, so detection on the vector $y$ loses nothing.

## Variants

- **Scalar detection after a matched filter.** $n = 1$ and $y = h x + w$ with a known gain $h$. This is the case of PAM, PSK and QAM on a flat channel.
- **Vector detection.** $y = H x + w$ with $x \in \mathcal{A}^n$, for several antennas or users. The ML rule minimizes $\|y - Hx\|^2$ over $M^n$ candidates; see [MIMO detection](/mimo-detection/).
- **Unknown phase.** If the carrier phase is unknown and uniform, the likelihood is averaged over the phase, and the rule becomes a comparison of envelopes; see [noncoherent detection](/noncoherent-detection/) and [differential phase-shift keying](/differential-phase-shift-keying/).
- **Sequence detection.** With intersymbol interference, the symbols are not independent given $y$, and the ML decision is over whole sequences; see [maximum likelihood sequence estimation](/maximum-likelihood-sequence-estimation/).
- **Soft output.** A decoder may need the posterior of each bit instead of a hard decision; see [soft demapping](/soft-demapping/).

## Examples

**Unequal priors.** BPSK with $a_0 = +1$, $a_1 = -1$, $\pi_0 = 0.9$, $\pi_1 = 0.1$ and $N_0 = 1$, so $E_s/N_0 = 0$ dB. The MAP rule decides $a_0$ when $|y - 1|^2 - N_0 \ln 0.9 < |y + 1|^2 - N_0 \ln 0.1$, that is, when $\mathrm{Re}\,y > (N_0/4)\ln(\pi_1/\pi_0) = -0.5493$. The real part of the noise has the standard deviation $\sigma = \sqrt{N_0/2} = 0.7071$. Then $P_e = 0.9\,Q(2.1910) + 0.1\,Q(0.6374) = 0.9 \cdot 0.014224 + 0.1 \cdot 0.26194 = 0.038996$. The ML rule uses the threshold 0 and has $P_e = Q(\sqrt{2}) = 0.078650$, about twice as large. Here [Q](/gaussian-q-function/) is the Gaussian tail function.

**QPSK.** The points $(\pm 1 \pm j)/\sqrt{2}$ have the four quadrants as Voronoi cells, so the ML rule decides the sign of the real part and the sign of the imaginary part. At $E_s/N_0 = 10$ dB its error probability is $2Q(\sqrt{10}) - Q(\sqrt{10})^2 = 1.5648 \times 10^{-3}$.

**A case where MAP and ML need different data.** The ML rule in Gaussian noise needs only the points and $y$. The MAP rule also needs $N_0$, because the prior term $N_0 \ln \pi_i$ scales with the noise. A receiver that does not know $N_0$ cannot apply the MAP rule exactly.

**Non-example: a threshold test.** Deciding whether a radar echo is present, with a fixed false alarm probability, is a binary hypothesis test of [signal detection](/signal-detection/). Its optimal rule is a [likelihood ratio test](/likelihood-ratio-test/) whose threshold comes from the false alarm constraint, not from priors.

## Known algorithms

- **[Minimum distance detector](/minimum-distance-detector/).** The ML rule in white Gaussian noise. A slicer does it in $\Theta(1)$ time per symbol for PAM, square QAM and PSK.
- **Exhaustive search.** Evaluate all $M$ metrics, $\Theta(Mn)$ time per decision in the [real RAM](/real-ram/). For a vector channel with $x \in \mathcal{A}^n$ and $y \in \mathbb{C}^m$, this is $M^n$ evaluations of $O(nm)$ each.
- **Sphere decoding.** Exact ML for the vector channel by a tree search inside a sphere around $y$: [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) and [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/). The worst case is exponential in $n$.
- **Linear and successive detectors.** Zero forcing, MMSE and V-BLAST detection solve the vector problem approximately in polynomial time; see [MIMO detection](/mimo-detection/).
- **Noncoherent and differential detectors** for an unknown phase, and the [Viterbi algorithm](/viterbi-algorithm/) for sequences with memory.

## Bounds

All bounds here are for the ML rule with equal priors in $\mathcal{CN}(0, N_0 I)$ noise. Write $d_{ik} = \|a_i - a_k\|$.

**Pairwise error.** If only $a_i$ and $a_k$ are possible, the error probability is $Q(d_{ik}/\sqrt{2N_0})$. The noise component along the line from $a_i$ to $a_k$ is real Gaussian with variance $N_0/2$, and an error occurs when it exceeds $d_{ik}/2$.

**Union bound.** The error event given $a_i$ is the union of the pairwise events, so by the [union bound](/union-bound/)

$$P_e \le \frac{1}{M}\sum_i \sum_{k \ne i} Q\!\left(\frac{d_{ik}}{\sqrt{2N_0}}\right).$$

For QPSK at $E_s/N_0 = 10$ dB this is $2Q(\sqrt{10}) + Q(\sqrt{20}) = 1.5693 \times 10^{-3}$, against the exact $1.5648 \times 10^{-3}$.

**Lower bound.** The decision region of $a_i$ lies inside the half-space on its side of the bisector to its nearest neighbor, so $\Pr[\text{error} \mid a_i] \ge Q(d_i/\sqrt{2N_0})$, where $d_i$ is the distance from $a_i$ to its nearest neighbor. For QPSK this gives $Q(\sqrt{10}) = 7.827 \times 10^{-4}$.

**Nearest neighbor approximation.** At high SNR, $P_e \approx \bar N_{\min}\, Q(d_{\min}/\sqrt{2N_0})$, where $d_{\min}$ is the minimum distance and $\bar N_{\min}$ the average number of neighbors at that distance. This is an approximation, not a bound. The [symbol error rate](/symbol-error-rate/) page gives the exact values for the common formats.

## Reductions

- **ML detection in Gaussian noise is a nearest point search.** For the vector channel $y = Hx + w$ with $\mathcal{A}$ a finite part of a lattice, the ML rule is the [closest vector problem](/closest-vector-problem/) restricted to a box. In general this is NP-hard; for the optimum multiuser detector of synchronous CDMA, which has this form with binary symbols, Verdú proved NP-hardness in the number of users (1989).
- **Binary detection is a likelihood ratio test.** For $M = 2$, the MAP rule compares the likelihood ratio $p(y \mid a_0)/p(y \mid a_1)$ with the threshold $\pi_1/\pi_0$.
- **From waveforms to vectors.** Projection onto a basis of the signal set reduces the waveform problem to the vector problem without loss in white Gaussian noise.

## Applications

Every digital receiver solves this problem, once per symbol: after the matched filter in a single-carrier link, after the one-tap correction on each OFDM subcarrier, and after an equalizer or a MIMO detector. The hard decisions feed decoders of hard-decision codes and decision-directed loops for carrier and timing recovery. The error probability of the optimal rule is the [symbol error rate](/symbol-error-rate/) of the link.

## References
