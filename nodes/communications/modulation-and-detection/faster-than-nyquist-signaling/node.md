---
tag: VR513F
kind: technique
slug: faster-than-nyquist-signaling
name: Faster-than-Nyquist signaling
aliases:
- FTN signaling
- Mazo limit
area: communications/modulation-and-detection
level: research
summary: "Send the pulses of a Nyquist system closer together than T and accept the ISI. Mazo showed that with binary sinc pulses the minimum distance does not fall until the spacing is 0.802T."
prereqs: [nyquist-isi-criterion, maximum-likelihood-sequence-estimation]
see_also: [nyquist-isi-criterion, intersymbol-interference, partial-response-signaling, maximum-likelihood-sequence-estimation, bcjr-algorithm, turbo-equalization, ungerboeck-mlse-receiver, spectral-efficiency]
sources:
  - paper: doi:10.1002/j.1538-7305.1975.tb02043.x
    title: J. E. Mazo, Faster-than-Nyquist signaling, Bell System Technical Journal 54(8), 1975
    locator: pp. 1451 to 1462 (binary sinc pulses sent at the spacing tau T keep the minimum Euclidean distance of the orthogonal case down to tau = 0.802)
  - paper: "J. B. Anderson, F. Rusek and V. Öwall, Faster-than-Nyquist signaling, Proceedings of the IEEE 101(8), 2013"
    locator: pp. 1817 to 1830 (survey of the minimum distance, the information rates, the receivers and the multicarrier form)
  - paper: "A. D. Liveris and C. N. Georghiades, Exploiting faster-than-Nyquist signaling, IEEE Transactions on Communications 51(9), 2003"
    locator: pp. 1502 to 1511 (the minimum distance limit for raised-cosine pulses and reduced-complexity detection)
  - paper: "F. Rusek and J. B. Anderson, Constrained capacities for faster-than-Nyquist signaling, IEEE Transactions on Information Theory 55(2), 2009"
    locator: pp. 764 to 775 (the information rates of FTN signaling with a given pulse and input alphabet)
---

Faster-than-Nyquist (FTN) signaling keeps the pulse of an ordinary Nyquist system, one whose shifts by $T$ are orthogonal, but sends the symbols every $\tau T$ with $\tau < 1$. The bandwidth stays the same and the rate grows by $1/\tau$, at the price of [intersymbol interference](/intersymbol-interference/) that the receiver must handle with a sequence detector. Mazo found in 1975 that for binary symbols on sinc pulses the minimum Euclidean distance between two signals is the same as with no ISI for every $\tau \ge 0.802$. So an optimal detector has the same error rate at high SNR as the Nyquist system, with about $25\%$ more bits in the same band.

## In plain words

A normal link spaces its pulses so that each one is read at the moment all the others pass through zero. Faster-than-Nyquist signaling sends the same pulses closer together, so the band of the signal does not change but more symbols go through it each second. Now the pulses overlap at the reading moments, and a simple receiver gets confused. A receiver that looks at the whole sequence of symbols at once can still tell the possible messages apart, as long as no two messages make signals that are too close. A surprising result is that the closest pair of signals stays as far apart as before even when the pulses are about twenty percent closer. The cost moves to the receiver, which must do much more work.

## When it applies

- The band is the scarce resource and the SNR is high enough that more bits per hertz are worth more complex receivers.
- The receiver can run a sequence detector or an iterative detector: the [Viterbi algorithm](/viterbi-algorithm/) or the [BCJR algorithm](/bcjr-algorithm/) on a truncated model of the ISI, often inside [turbo equalization](/turbo-equalization/) with a channel code.
- The transmitter already uses a linear modulation with a Nyquist pulse, usually a [root-raised-cosine filter](/root-raised-cosine-filter/): FTN changes only the symbol clock.

## The template

The holes are the pulse $h$ (unit energy, with orthonormal shifts by $T$), the factor $\tau \in (0, 1]$, and the detector DETECT. The symbols $a_k$ are from a constellation such as 2-PAM.

```pseudo id=main
FTN-LINK(a_0, ..., a_{N-1})                ▷ holes: PULSE h, τ, DETECT
L1  s(t) ← Σ_k a_k · h(t - kτT)             ▷ one symbol every τT instead of every T
L2  r(t) ← s(t) + w(t)                      ▷ white Gaussian noise of density N_0/2
L3  for k = 0 to N - 1 do
L4      y_k ← ∫ r(t) h(t - kτT) dt          ▷ the matched filter, sampled every τT
L5  G[k][l] ← g((k - l)τT), with g = h * h(-·)   ▷ the ISI; the noise in y has covariance (N_0/2) G
L6  â ← DETECT(y, G)                         ▷ a sequence detector on a truncated G
L7  return â
```

**The model after line L4.** The samples are $y = G a + \eta$ with $\eta \sim \mathcal{N}(0, (N_0/2) G)$. For a Nyquist pulse and $\tau = 1$, $G$ is the identity and there is no ISI. For $\tau < 1$, $G$ has nonzero entries off the diagonal: the overlap $g(m\tau T)$ of two pulses $m$ positions apart. A detector in the form of the [Ungerboeck receiver](/ungerboeck-mlse-receiver/) works with these samples directly; one in the Forney form first whitens the noise.

**The minimum distance.** The squared distance between the signals of two binary sequences $a$ and $a'$ is $\|s - s'\|^2 = \sum_{i,j} \epsilon_i \epsilon_j\, g((i - j)\tau T)$ with $\epsilon = a - a'$. Write $\epsilon = 2e$, with $e_i \in \{-1, 0, 1\}$, and divide by the value $4$ of a single error. For sinc pulses, $h(t) = \mathrm{sinc}(t/T)/\sqrt{T}$ with $\mathrm{sinc}(x) = \sin(\pi x)/(\pi x)$, the overlap is $g(t) = \mathrm{sinc}(t/T)$, and the normalized squared distance is

$$d^2(e) = \sum_{i,j} e_i e_j\, \mathrm{sinc}\big((i - j)\tau\big).$$

A single error has $d^2 = 1$. If every other error sequence also has $d^2 \ge 1$, the error rate of the optimal detector at high SNR is the same as without ISI, about $Q(\sqrt{2 E_b/N_0})$ times a small factor, with $Q$ the [Gaussian Q function](/gaussian-q-function/).

**A hand check.** The error $e = (1, -1)$ has $d^2 = 2 - 2\,\mathrm{sinc}(\tau)$. At $\tau = 0.802$, $\mathrm{sinc}(0.802) = \sin(0.802\pi)/(0.802\pi) = 0.23127$, so $d^2 = 1.537$, well above $1$. Short events are not the danger; long alternating events are. The event $e = (1, -1, 1, -1, 1, -1, 1, -1)$ has $d^2 = 0.99718$ at $\tau = 0.802$ and crosses $1$ at $\tau = 0.8028$. A full search over all events of length up to $10$ finds no event below $1$ at $\tau = 0.803$ or $0.81$, and this event as the minimum at $\tau = 0.802$. Mazo reported $0.802$ as the limit.

**The gain.** The band of the signal is still $1/(2T)$ at baseband: with uncorrelated symbols the power spectrum is $(\sigma_a^2/(\tau T))|H(f)|^2$, the same shape at a higher level. The rate is $1/(\tau T)$ symbols per second. At $\tau = 0.802$ binary FTN carries $2/0.802 = 2.49$ bits/s/Hz at baseband instead of $2$, with the same asymptotic error rate.

**Why a linear equalizer does not work.** The samples $g(m \tau T)$ of the sinc overlap have a discrete-time spectrum equal to the fold of the rectangle $|H(f)|^2$ at the spacing $1/(\tau T)$. For $\tau < 1$ the fold leaves a gap between $1/(2T)$ and $1/(2\tau T)$ where it is zero. So $G$ is close to singular, a [zero-forcing equalizer](/zero-forcing-equalizer/) does not exist, and an [MMSE equalizer](/mmse-linear-equalizer/) loses much of the SNR. The gain of FTN needs a detector that works on sequences.

## Classic examples

- **Mazo's binary sinc case.** $\tau$ from $1$ down to $0.802$ keeps the minimum distance; below it the distance falls, first through long alternating error events.
- **Raised-cosine and RRC pulses.** Liveris and Georghiades computed the limit for raised-cosine pulses, where the excess band of the roll-off lets the spacing go lower than for the sinc, and gave reduced-complexity detectors.
- **Coded FTN with iterative detection.** A convolutional or LDPC code, an interleaver and a [BCJR](/bcjr-algorithm/) detector of the ISI exchange soft information in [turbo equalization](/turbo-equalization/), which makes FTN work at moderate SNR.
- **Multicarrier FTN.** The same idea packs subcarriers closer than $1/T$ in frequency as well as symbols closer in time, as in the survey of Anderson, Rusek and Öwall. See [multicarrier modulation](/multicarrier-modulation/).

## Variations

- **Sequence detectors of reduced size.** The ISI of FTN has no end, so the detector truncates $G$ to a few taps and uses [reduced-state sequence estimation](/reduced-state-sequence-estimation/), M-algorithm search, or a channel-shortening prefilter.
- **Information rates instead of distance.** Rusek and Anderson studied the rates that FTN reaches with a given pulse and input alphabet. With a pulse that has excess bandwidth, FTN can use the part of the band that the Nyquist spacing leaves underused.
- **Precoding at the transmitter.** Some designs move part of the work to the transmitter, as [partial-response signaling](/partial-response-signaling/) does with integer ISI.

## Pitfalls

- **The 0.802 limit is narrow.** It holds for binary symbols on sinc pulses and for the minimum distance. Larger constellations, other pulses and other measures give other limits.
- **Distance is not the whole error rate.** Near the limit there are many error events at the minimum distance, so the error rate at moderate SNR is worse than without ISI, even when $d_{\min}$ is the same.
- **Colored noise.** The noise after the matched filter has covariance $(N_0/2)G$, not white. Forgetting this gives a wrong metric in the detector.
- **Truncation.** Cutting $G$ to a few taps leaves residual ISI that acts as an error floor if it is not counted.
- **Synchronization.** Timing and carrier recovery must work with ISI that never goes away.

## Exercises

1. Show that the power spectral density of $\sum_k a_k h(t - k\tau T)$ with uncorrelated symbols of variance $\sigma_a^2$ is $(\sigma_a^2/(\tau T))|H(f)|^2$, so the band does not depend on $\tau$.
2. Compute $d^2$ of the error events $(1, -1)$ and $(1, -1, 1)$ for sinc pulses at $\tau = 0.802$. (About $1.537$ and $1.699$.)
3. For sinc pulses and $\tau < 1$, find the discrete-time spectrum of the sequence $g(m\tau T) = \mathrm{sinc}(m\tau)$ and show that it is zero on part of the band.
4. Compute numerically the $\tau$ at which the alternating error event of length $8$ reaches $d^2 = 1$. (About $0.8028$.)

## References
