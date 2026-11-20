---
tag: QFFCWB
kind: concept
slug: favorable-propagation
name: Favorable propagation
aliases:
- asymptotic orthogonality of user channels
area: communications/mimo-communications
level: advanced
summary: With many antennas the channel vectors of different users become nearly orthogonal, which makes linear precoding near optimal.
prereqs: [massive-mimo, law-of-large-numbers]
see_also: [channel-hardening, pilot-contamination, cell-free-massive-mimo, zero-forcing-precoding, maximum-ratio-transmission, maximal-ratio-combining, mimo-capacity, beamforming]
sources:
  - paper: doi:10.5281/zenodo.43970
    title: "Hien Quoc Ngo, Erik G. Larsson and Thomas L. Marzetta, Aspects of favorable propagation in massive MIMO, 22nd European Signal Processing Conference (EUSIPCO), Lisbon, 76-80, 2014"
    locator: "the definition of favorable propagation, the sum capacity under favorable propagation, and the comparison of i.i.d. Rayleigh fading and line-of-sight propagation with uniform arrays"
  - paper: doi:10.1109/TWC.2010.092810.091092
    title: "Thomas L. Marzetta, Noncooperative cellular wireless with unlimited numbers of base station antennas, IEEE Transactions on Wireless Communications 9(11), 3590-3600, 2010"
    locator: the asymptotic orthogonality of the channel vectors of different users under i.i.d. fading as the number of antennas grows
  - book: isbn:9781107175570
    title: "Thomas L. Marzetta, Erik G. Larsson, Hong Yang and Hien Quoc Ngo, Fundamentals of Massive MIMO, Cambridge University Press, 2016"
    locator: the discussion of favorable propagation and its effect on linear processing
---

Favorable propagation is the condition that the channel vectors of different users, seen from a base station with many antennas, are nearly orthogonal. When it holds exactly, the users do not interfere after [maximal ratio combining](/maximal-ratio-combining/) or [maximum ratio transmission](/maximum-ratio-transmission/), and these simple linear methods reach the sum capacity. In [massive MIMO](/massive-mimo/), with $M$ antennas and i.i.d. Rayleigh fading, the normalized inner product $g_i^H g_j / M$ tends to 0 by the [law of large numbers](/law-of-large-numbers/), so favorable propagation holds in the limit. It is the companion of [channel hardening](/channel-hardening/): hardening is about the norm of one channel vector, and favorable propagation is about the angles between two. [Pilot contamination](/pilot-contamination/) undoes it for users that share a pilot, and in [cell-free massive MIMO](/cell-free-massive-mimo/) the different distances from users to access points also help to separate the users.

## In plain words

A base station listens to two phones at once on the same frequency. Each phone reaches the many antennas of the base station with its own pattern of strengths and delays, like a fingerprint.

If the two fingerprints are very different, the base station can listen to one phone and hardly hear the other, with no special effort. With a few antennas, the fingerprints often look alike, and the phones disturb each other. With hundreds of antennas, two fingerprints almost never look alike, unless the phones stand in the same direction or the surroundings are very simple. This is favorable propagation, and it is why a large array can serve many phones at once with simple processing.

## The idea

**The definition.** For the uplink $y = \sqrt{p}\, G x + w$ with $G = [g_1, \ldots, g_K] \in \mathbb{C}^{M \times K}$, propagation is **favorable** if

$$g_i^H g_j = 0 \quad \text{for all } i \ne j,$$

that is, if $G^H G$ is diagonal. It is **asymptotically favorable** if $g_i^H g_j / M \to 0$ for $i \ne j$ as $M \to \infty$, while $\|g_k\|^2/M$ stays bounded away from 0.

**Linear processing is optimal (a theorem).** With channel knowledge at the receiver, the sum capacity of the uplink is $\log_2 \det(I_K + p\, G^H G)$. By Hadamard's inequality for the [positive definite](/positive-definite-matrix/) matrix $I_K + p\, G^H G$,

$$\log_2 \det(I_K + p\, G^H G) \le \sum_{k=1}^{K} \log_2\left(1 + p\, \|g_k\|^2\right),$$

with equality if and only if $G^H G$ is diagonal. The right side is the sum of the rates of $K$ users who each have the channel to themselves. So favorable propagation is exactly the case in which the users do not hurt each other, and then maximal ratio combining, $g_k^H y$, gives each user the rate $\log_2(1 + p\|g_k\|^2)$ and reaches the sum capacity.

**I.i.d. Rayleigh fading (a closed form).** If $h_i$ and $h_j$ are independent with i.i.d. $\mathcal{CN}(0, 1)$ entries, then $\mathbb{E}|h_i^H h_j|^2 = M$, so $\mathbb{E}|h_i^H h_j / M|^2 = 1/M$, while $\|h_i\|^2/M \to 1$. The cosine of the angle between the two channel vectors has a typical size of $1/\sqrt{M}$: about 0.1 for $M = 100$.

**Line of sight (a closed form).** For a uniform linear array with half-wavelength spacing and users in the far field at angles $\phi_i$, $g_i = (1, e^{-j\pi \sin\phi_i}, \ldots, e^{-j\pi (M-1)\sin\phi_i})^T$, and

$$\frac{|g_i^H g_j|}{M} = \left|\frac{\sin(M \pi \delta / 2)}{M \sin(\pi \delta / 2)}\right|, \qquad \delta = \sin\phi_i - \sin\phi_j \ne 0.$$

This tends to 0 as $M$ grows for any two distinct directions, so line of sight is also asymptotically favorable. But users with close angles need a large $M$ before their channels separate.

## Examples

**Two users in line of sight (a closed form).** Take $p = 1$ and two users at $0°$ and $2°$. With $M = 10$, the normalized inner product is 0.951, the sum capacity is 4.93 bits per channel use, and the bound with favorable propagation is 6.92 bits. With $M = 100$, the inner product is 0.131, the sum capacity is 13.29 bits, and the bound is 13.32 bits. For users at $0°$ and $30°$, $\delta = 0.5$ and $M = 100$ give $\sin(25\pi) = 0$: the two channels are exactly orthogonal.

**Rayleigh fading (an approximation).** With $M = 100$, two users and $p = 1$, $\mathbb{E}|h_1^H h_2/M|^2 = 0.01$. Putting $|h_1^H h_2/M|^2 = 0.01$ and $\|h_k\|^2 = M$ into $\det(I_2 + p\, G^H G)$ gives a sum capacity only about 0.014 bits below the bound with favorable propagation. Maximal ratio combining does worse: its approximate SINR on the [massive MIMO](/massive-mimo/) page, $Mp/((K-1)p + 1) = 50$, is half of the 100 that a user alone would get, because the interference power $|h_1^H h_2|^2/\|h_1\|^2$ stays near 1 while the noise is 1. Zero forcing has the mean SINR $(M - K + 1)p = 99$. So asymptotic favorable propagation makes linear processing close to optimal, but at a fixed SNR, zero forcing is closer than maximal ratio combining.

**A non-example: a keyhole.** If $g_k = a\, z_k$ with a common vector $a$ and scalars $z_k$ for all users, then all channels are parallel and $|g_i^H g_j| = \|g_i\| \|g_j\|$ for every $M$. The users cannot be separated by any processing, and $G$ has rank one, so the channel carries only one stream.

## Where it is used

- **Linear precoding and detection.** [Maximum ratio transmission](/maximum-ratio-transmission/) and [zero-forcing precoding](/zero-forcing-precoding/) are close to the capacity of the multiuser downlink when propagation is close to favorable. Zero forcing removes the remaining interference at little cost when $G^H G$ is nearly diagonal.
- **User scheduling.** A scheduler can select users whose channels are nearly orthogonal, for example users in different directions in line of sight, to make propagation more favorable.
- **System analysis.** Together with [channel hardening](/channel-hardening/), it lets the SINR of linear schemes be written by deterministic approximations in [massive MIMO](/massive-mimo/).
- **Limits.** [Pilot contamination](/pilot-contamination/) makes the estimate of a user's channel contain the channels of other users with the same pilot, so the estimated channels are no longer orthogonal to them, even as $M$ grows.

## References
