---
tag: R3R54M
kind: concept
slug: near-far-problem
name: Near-far problem
aliases:
- near-far effect
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "In CDMA a nearby user arrives much stronger than a distant one, and its leakage through the code crosscorrelation drowns the weak user unless power is controlled or interference is cancelled."
prereqs: [code-division-multiple-access, matched-filter]
see_also: [foschini-miljanic-power-control, multiuser-detection, decorrelating-detector, successive-interference-cancellation, standard-interference-function, free-space-path-loss, processing-gain, log-normal-shadowing]
sources:
  - paper: doi:10.1109/18.42183
    title: "Ruxandra Lupas and Sergio Verdú, Linear multiuser detectors for synchronous code-division multiple-access channels, IEEE Transactions on Information Theory 35(1), 1989"
    locator: "the definitions of asymptotic efficiency and near-far resistance, and the near-far resistance of the conventional and decorrelating detectors"
  - paper: doi:10.1109/25.289411
    title: "Klein S. Gilhousen, Irwin M. Jacobs, Roberto Padovani, Andrew J. Viterbi, Lindsay A. Weaver and Charles E. Wheatley, On the capacity of a cellular CDMA system, IEEE Transactions on Vehicular Technology 40(2), 1991"
    locator: "the reverse link model with perfect power control and the capacity of a CDMA cell"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 4.3, CDMA (power control and the near-far problem)"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapter 5, Decorrelating detector (near-far resistance)"
---

The near-far problem is the main weakness of a [CDMA](/code-division-multiple-access/) uplink with conventional receivers. All users transmit in the same band at the same time, and the base station separates them only by their codes. The received power falls quickly with distance, so a user near the base station can arrive tens of decibels stronger than a user at the cell edge. A [matched filter](/matched-filter/) for the weak user still lets through a fraction of every other user, equal to the crosscorrelation of their codes. When that fraction of a strong user is larger than the weak user's own signal, the weak user is lost, even without noise. Two fixes exist. Power control makes all users arrive with about the same power, as in IS-95 and its successors. [Multiuser detection](/multiuser-detection/) uses the codes of all users to remove the interference, and the [decorrelating detector](/decorrelating-detector/) does so whatever the powers are. [Successive interference cancellation](/successive-interference-cancellation/) even turns the power differences into an advantage.

## In plain words

Two people talk to you at the same time. One stands next to you and the other is across a large hall. Even if they speak different languages, the near voice is so loud that you cannot follow the far one. In a CDMA system the base station is the listener and the phones are the speakers. Each phone has its own code, but the codes are not perfectly different, so a little of each voice leaks into the others. A little of a very loud voice can still be more than all of a quiet one. The system fixes this by telling the near phones to speak more quietly, or by a smarter receiver that removes the loud voice before it listens to the quiet one.

## The idea

With $K$ synchronous users, unit-norm signatures $s_k$, amplitudes $A_k$ and bits $b_k \in \{-1, +1\}$, the matched filter output of user $k$ is

$$z_k = A_k b_k + \sum_{j \ne k} R_{kj} A_j b_j + n_k, \qquad R_{kj} = s_k^\top s_j,$$

with $n_k \sim \mathcal{N}(0, \sigma^2)$. The middle term is the multiple access interference. Its size scales with the other users' amplitudes, not with $A_k$. If $\sum_{j \ne k} |R_{kj}| A_j > A_k$, some choice of the other bits makes the decision on $b_k$ wrong even with $\sigma = 0$.

Two figures, defined by Lupas and Verdú, measure how a detector suffers. The *asymptotic efficiency* $\eta_k$ is the fraction of user $k$'s energy that the detector keeps as the noise goes to 0: the error rate behaves like $Q(\sqrt{\eta_k}\, A_k / \sigma)$. For the matched filter,

$$\eta_k = \max\Big(0,\ 1 - \sum_{j \ne k} |R_{kj}| \frac{A_j}{A_k}\Big)^2.$$

The *near-far resistance* is the smallest $\eta_k$ over all amplitudes of the other users. For the matched filter it is 0 whenever some $R_{kj} \ne 0$: a strong enough interferer always wins. For the decorrelator it is $1/(R^{-1})_{kk} > 0$ when the signatures are linearly independent, and no detector does better.

Power control attacks the other factor. If all received amplitudes are equal, the interference on each user is the sum of $K - 1$ small crosscorrelations, which the [processing gain](/processing-gain/) keeps small, and the capacity of the cell is limited by the total interference, not by one strong user.

## Examples

- **The distance needed.** Two users have codes with crosscorrelation $\rho = 0.25$, typical of random codes with $N = 16$ chips, for which $E[\rho^2] = 1/16$. The matched filter of user 1 fails without noise when $A_2 > 4 A_1$, a power ratio of 16, or 12 dB. With a path loss exponent of 4, that is a user only twice as far away as the other.
- **Three users.** With the codes of length 8 used across this group, $R_{12} = 0.5$, $R_{13} = 0.25$, $R_{23} = -0.25$, and amplitudes $A = (1, 4, 2)$, user 1 receives $z_1 = 1 - 2 + 0.5 = -0.5$ for the bits $(+1, -1, +1)$ and is decided wrong without noise. At $\sigma = 0.5$ its matched filter error rate is 0.46, against 0.061 for the decorrelator and 0.023 if it were alone.
- **Shadowing.** Even users at the same distance can differ by 10 dB or more because of [log-normal shadowing](/log-normal-shadowing/) and fading, so equal distances do not remove the problem.
- **The downlink.** On the downlink, one base station sends all signals, which reach a given phone through the same channel and with powers the base station chooses. The near-far problem is mainly an uplink problem, and the downlink uses orthogonal codes such as [OVSF codes](/ovsf-codes/).

## Where it is used

- **Uplink power control.** IS-95 adjusts each phone's power with a fast closed loop of 800 commands per second, on top of an open loop that tracks the path loss. [Foschini-Miljanic power control](/foschini-miljanic-power-control/) and the [standard interference function](/standard-interference-function/) framework are the theory behind such loops.
- **Multiuser detection.** The near-far resistance of the [decorrelator](/decorrelating-detector/) and of the [optimum detector](/optimum-multiuser-detector/) was the first argument for multiuser receivers, which tolerate power differences instead of removing them.
- **Successive cancellation and NOMA.** [SIC](/successive-interference-cancellation/) decodes the strongest user first and removes it, so large power differences help it. Power domain [NOMA](/non-orthogonal-multiple-access/) assigns different powers on purpose for this reason.
- **Random access.** In [slotted ALOHA](/slotted-aloha/), a much stronger packet can survive a collision, the capture effect, which is the near-far effect seen from the strong user's side.

## References
