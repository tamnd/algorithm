---
tag: A73A6R
kind: concept
slug: eye-diagram
name: Eye diagram
aliases:
- eye pattern
area: communications/modulation-and-detection
level: intro
summary: "Many symbol periods of a received waveform drawn on top of each other. The open space in the middle, the eye, shows the noise margin and the timing margin left after intersymbol interference."
prereqs: [intersymbol-interference, raised-cosine-filter]
see_also: [intersymbol-interference, raised-cosine-filter, root-raised-cosine-filter, nyquist-isi-criterion, symbol-timing-recovery, channel-equalization, pulse-shaping, signal-constellation]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 9.2 (eye patterns of band-limited signals and the effect of intersymbol interference on the opening of the eye)
  - paper: "R. W. Lucky, Automatic equalization for digital communication, Bell System Technical Journal 44(4), 1965"
    locator: pp. 547 to 588 (the peak distortion of a sampled response as the measure of intersymbol interference)
---

An eye diagram is a picture of a received baseband waveform in which the trace is cut into pieces of one or two symbol periods and all pieces are drawn on top of each other, aligned to the symbol clock. For a binary signal the traces leave an open area in the middle that looks like an eye. The height of the eye at the sampling instant is the margin against noise, and its width is the margin against timing errors. Both shrink as [intersymbol interference](/intersymbol-interference/) grows, so the eye is the standard way to see ISI on an oscilloscope or in a simulation.

## In plain words

Take a long recording of the signal that arrives at the receiver, after its filter. Cut it into short pieces, each as long as one or two symbols, and draw all the pieces on the same screen, one over the other. If every symbol arrived clean, all the pieces would pass through the same few points at the moment the receiver reads the signal. Neighbors that leak into each other spread the traces out, and noise makes them fuzzy. What remains open between the upper and the lower traces is the eye. A tall eye means the receiver can tell the levels apart even with some noise. A wide eye means the receiver can read a little early or late and still be right. A closed eye means errors even without noise.

## The idea

**Construction.** Let $z(t)$ be the output of the receive filter, $z(t) = \sum_i a_i\, p(t - iT) + n(t)$, where $p$ is the overall pulse and $T$ the symbol period. The eye diagram draws the curves $t \mapsto z(kT + t)$ for $t$ in a window such as $[-T, T]$, for many $k$ on the same axes. A sampling oscilloscope does this by triggering on the symbol clock; a simulation does it by reshaping the sampled signal into rows of $2L_s$ samples, where $L_s$ is the number of samples per symbol.

**What the eye shows.**
- *Vertical opening.* At the sampling offset $\delta$, the noiseless trace of 2-PAM with $a_i = \pm 1$ in period $k$ has the value $a_k\, p(\delta) + \sum_{i \ne 0} a_{k - i}\, p(\delta + iT)$. The worst case over all data leaves the opening $p(\delta) - \sum_{i \ne 0} |p(\delta + iT)|$ above and below the threshold. At $\delta = 0$ this is $p(0)(1 - D)$, with $D$ the peak distortion of the [intersymbol interference](/intersymbol-interference/) page. The eye is open at $\delta$ when this is positive; noise then needs at least this amplitude to cause an error.
- *Horizontal opening.* The range of offsets $\delta$ at which the vertical opening is positive is the timing margin. It tells how much error [symbol timing recovery](/symbol-timing-recovery/) can make.
- *Slope of the sides.* Steep sides near the center mean that a small timing error costs much of the opening.
- *Crossings.* The spread of the zero crossings between the symbols shows the jitter that a timing loop based on zero crossings will see.
- *Several eyes.* $M$-PAM gives $M - 1$ eyes stacked on top of each other. QAM and PSK give one eye diagram for the in-phase part and one for the quadrature part.

**The eye and the Nyquist criterion.** A pulse that meets the [Nyquist ISI criterion](/nyquist-isi-criterion/) gives an eye whose traces pass through exactly the symbol values at $\delta = 0$: the eye is fully open there. How fast it closes away from $\delta = 0$ depends on how fast the tails of the pulse decay, which is where the roll-off of a [raised-cosine](/raised-cosine-filter/) pulse shows.

**A measure of quality.** With Gaussian noise, let the traces at the sampling instant have mean $\mu_1$ and spread $\sigma_1$ for one level and $\mu_0$ and $\sigma_0$ for the other. A threshold at $\mu_0 + \sigma_0 q$ with $q = (\mu_1 - \mu_0)/(\sigma_0 + \sigma_1)$ is $q$ standard deviations from both levels, so each level is read wrongly with probability $Q(q)$, where $Q$ is the [Gaussian Q function](/gaussian-q-function/). The number $q$, read from the eye, gives an estimate of the bit error rate.

## Examples

**Worst-case opening of a raised-cosine link.** For 2-PAM with a raised-cosine pulse of roll-off $\beta$, $p(0) = 1$, and the worst-case vertical opening at the offset $\delta$ is (summed over $2000$ symbols on each side):

| $\beta$ | $\delta = 0.1T$ | $\delta = 0.2T$ | $\delta = 0.3T$ |
|---|---|---|---|
| 0 (sinc) | $-0.63$ | $-2.14$ | $-3.41$ |
| 0.25 | 0.652 | 0.289 | $-0.069$ |
| 0.5 | 0.785 | 0.535 | 0.261 |
| 1 | 0.896 | 0.736 | 0.525 |

A negative value means that some data pattern closes the eye. The sinc pulse is fully open at $\delta = 0$ and closed at any offset, and its numbers get worse as the data grows longer, because its tails fall only like $1/|t|$. With $\beta = 0.25$ the eye closes between $0.2T$ and $0.3T$ from the center; with $\beta = 1$ it is still half open at $0.3T$.

**Full roll-off: thin crossings.** With $\beta = 1$ the raised-cosine pulse is zero at $\pm 3T/2, \pm 5T/2, \ldots$ and equal to $1/2$ at $\pm T/2$. So halfway between symbols $0$ and $1$ the signal is $(a_0 + a_1)/2$: every trace that goes from $+1$ to $-1$ or back passes through $0$ at exactly $t = T/2$. The crossings of the eye are a single point, with no jitter from the data.

**Two taps by hand.** The channel with $p(0) = 1$, $p(T) = 0.5$ and no other taps, sampled at the right time, gives the levels $\pm 1.5$ and $\pm 0.5$. The eye has four lines at the sampling instant, and its opening is $0.5$ above and below $0$, half of the opening without ISI. Adding a third tap $p(2T) = 0.5$ gives the level $1 - 0.5 - 0.5 = 0$ for one pattern: the eye is just closed. With $p(T) = 0.6$ instead, the level is $-0.1$ and the eye is closed.

**One RRC filter.** At the output of a transmit [root-raised-cosine filter](/root-raised-cosine-filter/) with $\beta = 0.5$, before the matched filter, the worst-case opening at $\delta = 0$ is $1 - 0.298 = 0.70$ of the peak, not $1$: the sum of the RRC samples at the other multiples of $T$ is $0.298$ of the peak. After the receive RRC filter, the eye opens fully.

## Where it is used

- Lab measurements of serial links, radio receivers and optical receivers, where an oscilloscope triggered by the clock draws the eye and a mask test checks that no trace enters a forbidden region.
- Choosing the sampling instant and checking the loop of [symbol timing recovery](/symbol-timing-recovery/).
- Tuning [channel equalization](/channel-equalization/): an equalizer is working when it opens the eye. A [zero-forcing equalizer](/zero-forcing-equalizer/) minimizes the peak distortion, which maximizes the worst-case opening at the sampling instant.
- Comparing pulse shapes: [pulse shaping](/pulse-shaping/) with a larger roll-off gives a wider eye in time.
- The sampled counterpart is the scatter plot of the samples on the [signal constellation](/signal-constellation/), which shows the same margins in two dimensions at a single instant.

## References
