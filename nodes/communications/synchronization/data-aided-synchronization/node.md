---
tag: V4VVZK
kind: concept
slug: data-aided-synchronization
name: Data-aided synchronization
aliases:
- data-aided estimation
- non-data-aided synchronization
area: communications/synchronization
level: core
summary: The split of synchronizers into those that use known or decided symbols and those that only use signal statistics.
prereqs: [carrier-recovery, symbol-timing-recovery, maximum-likelihood-estimation]
see_also: [modified-cramer-rao-bound, pilot-symbol-assisted-modulation, decision-directed-carrier-recovery, costas-loop, viterbi-viterbi-phase-estimation, preamble-correlation-detection, frequency-offset-estimation, cycle-slip]
sources:
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 2 (basic principles: data-aided, decision-directed and non-data-aided maximum likelihood estimation) and Chapter 5 (carrier phase recovery with linear modulations)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 5 (synthesis of synchronization algorithms, the decision-directed approach) and Chapter 6 (performance analysis of synchronizers)"
  - paper: doi:10.1109/TCOMM.1994.580247
    title: "A. N. D'Andrea, U. Mengali and R. Reggiannini, The modified Cramer-Rao bound and its application to synchronization problems, IEEE Transactions on Communications 42(2/3/4), 1994, pages 1391 to 1399"
    locator: "the modified Cramer-Rao bound, which is the true bound for data-aided estimation and a looser bound otherwise"
---

Data-aided synchronization is the use of known symbols, such as pilots or a preamble, to estimate the carrier phase, the frequency offset or the symbol timing. It is one of three classes into which synchronizers are split by what they know about the data. Decision-directed synchronizers use the receiver's own decisions as if they were known symbols. Non-data-aided synchronizers, also called blind, use only the statistics of the signal, by averaging the likelihood over all possible data or by a nonlinearity that removes the modulation. The class sets the cost, the accuracy and the failure modes of a synchronizer: data-aided methods pay for the pilots and have no ambiguity, while non-data-aided methods are free but resolve the phase only up to the symmetry of the constellation and lose accuracy at low SNR. The [modified Cramer-Rao bound](/modified-cramer-rao-bound/) is tied to this split: it is the true bound for data-aided estimation and only a lower bound for the other two classes.

## In plain words

To find the phase or the timing of a signal, the receiver must compare it with something. If the transmitter sends some symbols that the receiver knows in advance, the receiver compares with those. This is accurate and simple, but the known symbols carry no new data. The receiver can instead use the symbols it has just read, and treat them as known. This is free and works well while few of them are wrong. Or the receiver can use only the general shape of the signal, such as how its points are spread around a circle. This is also free, but it is less accurate when noise is strong, and it cannot tell some positions apart.

## The idea

**Three likelihoods.** Let $r$ be the received samples, $\lambda$ the parameter (phase, frequency or timing) and $a$ the data symbols. The density $p(r \mid a, \lambda)$ is known in form.

- **Data-aided (DA).** The $a$ are known, and the estimate maximizes $p(r \mid a, \lambda)$ in $\lambda$. For the phase in white Gaussian noise this gives $\hat\theta = \arg\sum_k a_k^\ast r_k$.
- **Decision-directed (DD).** The $a$ are replaced by decisions $\hat a$, made with the current estimate, and the estimate maximizes $p(r \mid \hat a, \lambda)$. This is the method of [decision-directed carrier recovery](/decision-directed-carrier-recovery/).
- **Non-data-aided (NDA).** The data are averaged out, and the estimate maximizes $p(r \mid \lambda) = E_a\, p(r \mid a, \lambda)$, or an approximation of it.

**The NDA likelihood for BPSK (theorem).** With $a_k = \pm1$ equally likely, $E_s = 1$ and white noise of density $N_0$, averaging gives
$$p(r \mid \theta) \propto \prod_k \cosh\Bigl(\tfrac{2}{N_0}\operatorname{Re}\bigl(r_k e^{-j\theta}\bigr)\Bigr).$$
At low SNR, $\ln\cosh x \approx x^2/2$, and maximizing $\sum_k \operatorname{Re}(r_k e^{-j\theta})^2$ gives $\hat\theta = \frac12\arg\sum_k r_k^2$, the squaring estimator behind the [squaring loop](/squaring-loop/) and the [Costas loop](/costas-loop/). At high SNR, $\ln\cosh x \approx |x|$, which is the decision-directed metric $\sum_k \hat a_k \operatorname{Re}(r_k e^{-j\theta})$. So the three classes are the exact NDA estimator and its two limits. The same steps for M-PSK lead to the M-th power estimators, such as [Viterbi and Viterbi phase estimation](/viterbi-viterbi-phase-estimation/).

**What each class costs.**

| | Data-aided | Decision-directed | Non-data-aided |
|---|---|---|---|
| Overhead | pilots or preamble | none | none |
| Phase ambiguity | none | $2\pi/M$, fixed at start | $2\pi/M$ |
| Accuracy | at the MCRB | near the MCRB at high SNR | squaring loss at low SNR |
| Main failure | too few pilots for fast changes | wrong decisions, false lock | cycle slips, ambiguity |
| Typical use | acquisition, bursts, fading | tracking after acquisition | continuous links, blind receivers |

**The bound and the split (theorem).** With known data, the modified Cramer-Rao bound equals the true Cramer-Rao bound, so DA estimators can be judged exactly against it. Without known data, the true bound is larger, and the MCRB is only a lower bound. Decision-directed estimators come close to it at high SNR, where decisions are almost always right, and both the true CRB and the MCRB then agree.

**Mixed schemes.** Real receivers combine the classes: a DA estimate from a preamble starts the loop and fixes the ambiguity, DD or NDA tracking follows during the data, and pilots inserted at intervals, as in [pilot-symbol-assisted modulation](/pilot-symbol-assisted-modulation/), check for slips and support tracking in fading. A second distinction, used for carrier recovery, is whether the timing is already known (clock-aided) or not.

## Examples

**The price of not knowing the data (computation).** For BPSK, the ratio of the true NDA phase bound to the MCRB is $1/E[\tanh^2(2x/N_0)]$ with $x \sim \mathcal{N}(1, N_0/2)$, the per-symbol information loss of averaging. A numerical integration gives $2.42$ at $E_s/N_0 = -5$ dB, $1.30$ at 0 dB, $1.019$ at 5 dB and $1.00001$ at 10 dB. To reach a phase error of $2^\circ$ in standard deviation, a variance of $1.22 \times 10^{-3}$ rad$^2$, a DA estimator needs these numbers of symbols, from $N = 1/(2\,\mathrm{var}\,E_s/N_0)$, and an NDA estimator at least these, from the true bound:

| $E_s/N_0$ | DA pilots | NDA data symbols, at least |
|---|---|---|
| 5 dB | 130 | 133 |
| 0 dB | 411 | 534 |
| $-5$ dB | 1298 | 3144 |

At moderate SNR, blind estimation needs almost no more symbols than pilots, and the symbols carry data. At low SNR, it needs more than twice as many, and practical NDA estimators lose more than the bound: on the Viterbi and Viterbi page, the measured mean square error of a QPSK block of 32 symbols at 0 dB is more than 7 times the MCRB.

**A phase estimate with and without known data (measurement).** On the [carrier recovery](/carrier-recovery/) page, eight QPSK symbols at 10 dB with $\theta = 0.7$ give $0.655$ with known data and $0.626$ with the fourth-power NDA estimator; the second is only defined modulo $\pi/2$.

**Pilots in a standard.** DVB-S2 can insert blocks of 36 known pilot symbols at regular intervals in the frame, so that the receiver can use DA estimation for the carrier at very low SNR, where NDA loops would slip.

## Where it is used

- **Carrier recovery.** All classes are used; see [carrier recovery](/carrier-recovery/) and [cycle slips](/cycle-slip/) for the failures of the non-data-aided ones.
- **Frequency offset estimation.** Most fast [frequency offset estimators](/frequency-offset-estimation/) are DA; OFDM uses DA training symbols (Moose, Schmidl-Cox) or the NDA cyclic prefix (van de Beek).
- **Timing recovery.** The Gardner detector and the Oerder and Meyr estimator are NDA; the Mueller and Muller detector is DD.
- **Frame synchronization.** [Preamble correlation detection](/preamble-correlation-detection/) finds a known sequence, after which DA estimation can start.
- **Channel estimation.** Pilot-based channel estimation in fading is the same idea applied to the channel gain, of which the carrier phase is the angle.

## References
