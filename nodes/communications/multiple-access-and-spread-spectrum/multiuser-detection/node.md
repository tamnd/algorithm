---
tag: 52R9T9
kind: problem
slug: multiuser-detection
name: Multiuser detection
aliases:
- MUD
- joint detection
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "Decide the symbols of all users at once from a received signal in which their spread waveforms overlap, using what the receiver knows about every user and not only the wanted one."
model: real-ram
complexity:
  vars: {K: the number of users, N: the number of chips per symbol}
  time: {worst: O(K N + K^2 2^K)}
prereqs: [code-division-multiple-access, near-far-problem, symbol-detection]
see_also: [optimum-multiuser-detector, decorrelating-detector, mmse-multiuser-detector, successive-interference-cancellation, parallel-interference-cancellation, multiuser-detection-np-hardness, mimo-detection, matched-filter]
sources:
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapters 4 to 7 (optimum, decorrelating, non-decorrelating linear, and decision-driven multiuser detectors)"
  - paper: doi:10.1109/TIT.1986.1057121
    title: "Sergio Verdú, Minimum probability of error for asynchronous Gaussian multiple-access channels, IEEE Transactions on Information Theory 32(1), 1986"
    locator: "the asynchronous model and the jointly optimum detector"
  - paper: doi:10.1109/18.42183
    title: "Ruxandra Lupas and Sergio Verdú, Linear multiuser detectors for synchronous code-division multiple-access channels, IEEE Transactions on Information Theory 35(1), 1989"
    locator: "the definitions of asymptotic efficiency and near-far resistance"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Discussion 8.1, Connections with CDMA multiuser detection and ISI equalization"
---

Multiuser detection is the problem of deciding the data of several users that share a channel, from a received signal in which their waveforms overlap. In [CDMA](/code-division-multiple-access/) every user transmits at the same time in the same band, separated only by its signature. A conventional receiver runs one [matched filter](/matched-filter/) per user and treats the other users as noise. That fails when the signatures are not orthogonal and one user is much stronger than another, the [near-far problem](/near-far-problem/). A multiuser detector uses the signatures, and possibly the amplitudes, of all users to decide all the bits jointly. The exact solution, the [optimum multiuser detector](/optimum-multiuser-detector/), is [NP-hard](/multiuser-detection-np-hardness/) in the number of users, so most practical detectors are linear filters or cancellation methods that are polynomial in $K$. The same mathematics describes [MIMO detection](/mimo-detection/), with transmit antennas in the place of users.

## In plain words

Several people talk at the same time in the same room, each with a slightly different voice. A simple listener tries to follow one person and treats all the others as background noise. That works when the voices are very different and equally loud. It fails when a loud speaker stands next to the listener and a quiet one stands far away. A multiuser detector listens to everyone at once. Because it knows what each voice sounds like, it can work out what each person said even when the voices overlap and one is much louder than the others.

## Definition

There are $K$ users. In one symbol interval, user $k$ sends a bit $b_k \in \{-1, +1\}$ with received amplitude $A_k > 0$ and a signature $s_k \in \mathbb{R}^N$ with $\|s_k\| = 1$, where $N$ is the number of chips. In the synchronous model the receiver sees

$$y = \sum_{k=1}^K A_k b_k s_k + w = S A b + w, \qquad w \sim \mathcal{N}(0, \sigma^2 I_N),$$

with $S = [s_1, \ldots, s_K]$ and $A = \mathrm{diag}(A_k)$. The matched filter outputs $z = S^\top y = R A b + n$, with $R = S^\top S$ and $n \sim \mathcal{N}(0, \sigma^2 R)$, are a sufficient statistic for $b$.

**Input:** $y$ (or $z$), the signatures, and whatever else the receiver knows of $A$ and $\sigma$.

**Output:** decisions $\hat b_1, \ldots, \hat b_K$.

**Goal:** a small error probability $P(\hat b_k \ne b_k)$ for each user. Two exact versions are common. The *jointly optimum* detector maximizes $P(b \mid y)$, which for equally likely bits is $\max_b \Omega(b)$ with $\Omega(b) = 2\, b^\top A z - b^\top A R A b$. The *individually optimum* detector minimizes each $P(\hat b_k \ne b_k)$ separately, by summing the likelihood over the other bits. The two differ only slightly at high SNR.

Two figures of merit compare detectors. The *asymptotic efficiency* $\eta_k$ of a detector is the fraction of user $k$'s energy that it keeps as $\sigma \to 0$: its error rate behaves like $Q(\sqrt{\eta_k}\, A_k / \sigma)$. The *near-far resistance* is the infimum of $\eta_k$ over all amplitudes of the other users.

## Variants

- **Asynchronous users.** The symbol intervals of the users are offset, so each bit overlaps two bits of every other user. The matched filter outputs of a frame of $M$ symbols form a block banded system of size $K M$.
- **Multipath and fading.** Each signature becomes the convolution of the code with the user's channel, which the receiver must estimate. A [rake receiver](/rake-receiver/) is the single-user matched filter in this case.
- **Unknown interferers.** Only the wanted user's signature is known. Blind and adaptive detectors learn the filter from the data.
- **Coded data.** The detector exchanges soft information with the channel decoders of all users, which leads to iterative multiuser detection.
- **More users than chips.** With $K > N$, $R$ is singular. The optimum and MMSE detectors still work, the decorrelator does not.
- **Other alphabets.** QAM or higher order symbols replace the bits, and the same structure holds with complex signals.

## Examples

Three users with $N = 8$ chips use $s_1 = (1,1,1,1,1,1,1,1)/\sqrt 8$, $s_2 = (1,1,1,1,1,1,-1,-1)/\sqrt 8$ and $s_3 = (1,-1,1,-1,1,-1,1,1)/\sqrt 8$, so

$$R = \begin{pmatrix} 1 & 0.5 & 0.25 \\ 0.5 & 1 & -0.25 \\ 0.25 & -0.25 & 1 \end{pmatrix}.$$

The amplitudes are $A = (1, 4, 2)$, the bits $b = (+1, -1, +1)$. Without noise, $z = R A b = (-0.5, -4, 3.25)$: user 1 receives $+1$ from itself, $-2$ from user 2 and $+0.5$ from user 3, so its matched filter decides $-1$, wrong, even with no noise at all. At $\sigma = 0.5$ the exact error rates for user 1 are:

| detector | error rate of user 1 |
|---|---|
| matched filter | 0.460 |
| [decorrelator](/decorrelating-detector/) | 0.0607 |
| [MMSE detector](/mmse-multiuser-detector/) | 0.0584 |
| single-user bound $Q(A_1/\sigma) = Q(2)$ | 0.0228 |

For one noisy draw, $z = (-0.47, -4.21, 2.18)$, the matched filter errs on user 1, and the decorrelator, the MMSE detector, successive and parallel cancellation, and the optimum detector all return $b$.

## Known algorithms

| algorithm | idea | cost for $K$ users | needs |
|---|---|---|---|
| [matched filter](/matched-filter/) | treat the others as noise | $O(K N)$ | signatures |
| [optimum detector](/optimum-multiuser-detector/) | maximize $\Omega(b)$ | $O(K^2 2^K)$ per bit | signatures, amplitudes |
| [decorrelator](/decorrelating-detector/) | apply $R^{-1}$ to $z$ | $O(K^2 N + K^3)$ | signatures |
| [MMSE detector](/mmse-multiuser-detector/) | apply $(R + \sigma^2 A^{-2})^{-1}$ | $O(K^2 N + K^3)$ | signatures, amplitudes, $\sigma$ |
| [successive cancellation](/successive-interference-cancellation/) | decide the strongest, subtract, repeat | $O(K N)$ on the chips | signatures, amplitudes or estimates |
| [parallel cancellation](/parallel-interference-cancellation/) | cancel all others in stages | $O(K^2 N + J K^2)$ | signatures, amplitudes |

[Semidefinite relaxation](/semidefinite-relaxation-detection/) and sphere decoding by [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) are used for the jointly optimum problem, mostly in the MIMO setting.

## Bounds

- **Single-user bound.** No detector beats the error rate that user $k$ would have alone, $Q(A_k / \sigma)$, because a genie that tells the receiver the other bits can only help.
- **Hardness.** The jointly optimum problem is NP-hard in $K$ ([NP-hardness of optimum multiuser detection](/multiuser-detection-np-hardness/)), so no exact algorithm polynomial in $K$ is known.
- **Near-far resistance.** The matched filter has near-far resistance 0 when any $R_{kj} \ne 0$. The decorrelator has $1/(R^{-1})_{kk}$, the squared distance from $s_k$ to the span of the other signatures, and no detector has more (Lupas and Verdú).
- **Linear detectors.** The MMSE detector has the largest SINR among all linear detectors for every user.

## Reductions

- **From maximum cut.** Every weighted [maximum cut](/maximum-cut/) instance is a jointly optimum detection instance with a suitable $R$ and $z = 0$, which proves the hardness.
- **To minimum cut.** When all crosscorrelations are nonpositive, the jointly optimum problem becomes a minimum cut problem, solvable in polynomial time.
- **To least squares.** Dropping the constraint $b \in \{-1, +1\}^K$ turns $\max_b \Omega(b)$ into a [least squares problem](/least-squares-problem/), whose solution is the decorrelator output.
- **Same as MIMO detection and equalization.** Replacing $S A$ by a channel matrix gives [MIMO detection](/mimo-detection/); replacing it by a convolution matrix gives equalization of intersymbol interference. Each detector here has a counterpart there.

## Applications

- **CDMA uplinks.** Base stations of CDMA systems receive many users with different powers and codes, which is the setting in which multiuser detection was developed.
- **NOMA.** Non-orthogonal multiple access sends several users in the same resource on purpose and separates them with successive cancellation.
- **MIMO receivers.** V-BLAST and other spatial multiplexing receivers solve the same problem with antennas in the place of users.
- **Random access and satellite links.** Colliding packets can be separated by cancellation instead of retransmitted.

## References
