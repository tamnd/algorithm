---
tag: 8RWEGK
kind: concept
slug: massive-mimo
name: Massive MIMO
aliases:
- large-scale antenna systems
area: communications/mimo-communications
level: advanced
summary: A base station with many more antennas than users, where simple linear processing becomes near optimal.
prereqs: [mimo-channel-model, mimo-capacity, law-of-large-numbers]
see_also: [channel-hardening, favorable-propagation, pilot-contamination, cell-free-massive-mimo, zero-forcing-precoding, maximum-ratio-transmission, maximal-ratio-combining, hybrid-beamforming]
sources:
  - paper: doi:10.1109/TWC.2010.092810.091092
    title: "Thomas L. Marzetta, Noncooperative cellular wireless with unlimited numbers of base station antennas, IEEE Transactions on Wireless Communications 9(11), 3590-3600, 2010"
    locator: "the time-division duplex model with uplink pilots, the limit of an unlimited number of antennas with matched filtering, and pilot contamination as the remaining limit"
  - book: isbn:9781107175570
    title: "Thomas L. Marzetta, Erik G. Larsson, Hong Yang and Hien Quoc Ngo, Fundamentals of Massive MIMO, Cambridge University Press, 2016"
    locator: "the chapters on the single-cell and multi-cell systems, channel estimation from uplink pilots, and the capacity bounds for linear processing"
---

Massive MIMO is a cellular design in which a base station with a large number $M$ of antennas serves a smaller number $K$ of single-antenna users on the same time and frequency resources, with $M$ much larger than $K$, for example $M = 64$ and $K = 8$. When $M$ grows, the channel gain of each user hardens to its mean, which is [channel hardening](/channel-hardening/), and the channels of different users become nearly orthogonal, which is [favorable propagation](/favorable-propagation/). Then simple linear processing, such as [maximal ratio combining](/maximal-ratio-combining/) on the uplink and [maximum ratio transmission](/maximum-ratio-transmission/) or [zero-forcing precoding](/zero-forcing-precoding/) on the downlink, is close to the best possible. The base station learns the channels from uplink pilots, and the reuse of pilots between cells causes [pilot contamination](/pilot-contamination/), the main limit that remains as $M$ grows. [Cell-free massive MIMO](/cell-free-massive-mimo/) spreads the same antennas over many access points instead of one site.

## In plain words

A normal base station has a few antennas and serves one or a few users at a time on each frequency. A massive MIMO base station has dozens or hundreds of antennas and serves many users at once on the same frequency.

With so many antennas, two useful things happen. First, the signal of each user arrives with almost the same total strength every time, because the deep fades at some antennas are balanced by strong signals at others. Second, the signals of different users look almost unrelated to each other, so the base station can keep them apart with simple arithmetic. Each user gets a strong, steady link, and the base station needs little transmit power for each user.

## The idea

**The model.** On the uplink, the base station receives

$$y = \sqrt{p}\, G x + w, \qquad G = [g_1, \ldots, g_K] \in \mathbb{C}^{M \times K},$$

where user $k$ sends $x_k$ with $\mathbb{E}|x_k|^2 = 1$, $p$ is the SNR of each user, and $w$ has i.i.d. $\mathcal{CN}(0, 1)$ entries. In the i.i.d. Rayleigh model, $g_k = \sqrt{\beta_k}\, h_k$ with $h_k$ having i.i.d. $\mathcal{CN}(0, 1)$ entries and $\beta_k$ the large-scale fading of user $k$. This is the [MIMO channel model](/mimo-channel-model/) with the users as the transmit antennas.

**The law of large numbers (a theorem).** For i.i.d. Rayleigh channels, by the [law of large numbers](/law-of-large-numbers/),

$$\frac{1}{M} G^H G \to \mathrm{diag}(\beta_1, \ldots, \beta_K) \quad \text{almost surely as } M \to \infty.$$

The diagonal limit is channel hardening, and the zero limit off the diagonal is favorable propagation. So maximal ratio combining, $\frac{1}{M} G^H y$, tends to $\sqrt{p}\, \mathrm{diag}(\beta_k)\, x$: the interference between users and the noise both vanish, and each user sees a clean scalar channel.

**Linear processing is enough (an approximation).** With $\beta_k = 1$ and perfect channel knowledge, replace each random term in the SINR of maximal ratio combining by its mean: the signal power $p\, \|g_k\|^4 \approx p M^2$, the interference $p \sum_{i \ne k} |g_k^H g_i|^2 \approx (K - 1) p M$, and the noise $\|g_k\|^2 \approx M$. Then

$$\mathrm{SINR}_k \approx \frac{M p}{(K - 1) p + 1}.$$

The SINR grows linearly in $M$. With [zero forcing](/zero-forcing-precoding/), the SINR of each user in i.i.d. Rayleigh fading is $p$ times a Gamma variable with shape $M - K + 1$ (a theorem), with mean $(M - K + 1) p$, so the interference is removed at the cost of $K - 1$ degrees of freedom.

**Power scaling (a consequence of the approximation).** If the user power falls as $p = E/M$ for a fixed $E$, the approximate MRC SINR tends to $E$. So with perfect channel knowledge, each doubling of $M$ lets each user cut its power in half for the same rate. With estimated channels, the scaling is slower, because the estimate also degrades as $p$ falls.

**Pilots and time-division duplex.** The base station cannot learn $M K$ channel coefficients from downlink pilots with feedback when $M$ is large, because the pilot time grows with $M$. In time-division duplex, each user sends one uplink pilot, the base station estimates all $M$ coefficients of that user at once, and channel reciprocity gives the downlink channel. With a coherence block of $\tau_c$ samples and $\tau_p \ge K$ orthogonal pilots, the fraction $1 - \tau_p/\tau_c$ of the block carries data. The pilot cost depends on $K$ but not on $M$.

**The remaining limit.** Neighboring cells must reuse the same pilot sequences. The estimate of a user then contains the channels of the users in other cells with the same pilot, and the beam formed from it points partly at them. Marzetta showed that, with matched filtering, as $M \to \infty$ the noise and the uncorrelated interference vanish but this pilot contamination remains, so the SINR tends to a finite limit set by the ratios of the large-scale fading coefficients (a theorem in his model).

## Examples

- **A single cell (an approximation and a simulation).** With $M = 100$, $K = 10$ and $p = 1$ (0 dB per user), the approximate MRC SINR is $100/10 = 10$, or $\log_2 11 = 3.46$ bits per channel use for each user and 34.6 for the cell. A Monte Carlo average over 300 i.i.d. Rayleigh draws gives 3.50 bits per user. With $M = 400$, the approximation gives $\log_2 41 = 5.36$ bits, and the simulation gives 5.39. With zero forcing at $M = 100$, the mean SINR is $91$.
- **Interference-limited MRC.** At $p = 10$ (10 dB) with $M = 100$ and $K = 10$, the approximate SINR is $1000/91 = 10.99$, almost the same as at 0 dB: MRC is limited by the other users, not by noise, and zero forcing gains more at high SNR.
- **A deployment (industry practice).** Commercial 5G base stations in the 3.5 GHz band commonly use arrays of 64 transmit and 64 receive chains in time-division duplex and serve several users at once on the same resources.

## Where it is used

- **5G New Radio.** Massive MIMO in time-division duplex bands below 6 GHz is one of the main sources of the capacity gain of 5G over 4G.
- **Millimeter wave.** Large arrays at 28 GHz and above use [hybrid beamforming](/hybrid-beamforming/), with fewer radio chains than antennas, to keep the cost and power down.
- **Distributed systems.** [Cell-free massive MIMO](/cell-free-massive-mimo/) applies the same principles with antennas spread over the area.
- **Theory of linear precoding.** Channel hardening and favorable propagation are the reasons why the simple precoders [maximum ratio transmission](/maximum-ratio-transmission/) and [zero-forcing precoding](/zero-forcing-precoding/) are close to the multiuser capacity when $M \gg K$, and why the analysis can use deterministic equivalents in place of random SINRs.

## References
