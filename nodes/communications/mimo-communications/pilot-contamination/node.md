---
tag: 77RVN3
kind: concept
slug: pilot-contamination
name: Pilot contamination
aliases:
- pilot interference
area: communications/mimo-communications
level: advanced
summary: Reuse of pilots in nearby cells corrupts the channel estimates. With matched filtering in an uncorrelated fading model it caps the SINR as the number of antennas grows.
prereqs: [massive-mimo, channel-estimation, least-squares-channel-estimation]
see_also: [channel-hardening, favorable-propagation, lmmse-channel-estimation, maximal-ratio-combining, cell-free-massive-mimo, max-min-sinr-power-control, zadoff-chu-sequence, law-of-large-numbers]
sources:
  - paper: doi:10.1109/TWC.2010.092810.091092
    title: "Thomas L. Marzetta, Noncooperative cellular wireless with unlimited numbers of base station antennas, IEEE Transactions on Wireless Communications 9(11), 3590-3600, 2010"
    locator: "the multicell TDD model with pilots reused in every cell, matched filter processing, and the limit of the SINR as the number of base station antennas grows without bound"
  - paper: doi:10.1109/TWC.2011.060711.101155
    title: "Jubin Jose, Alexei Ashikhmin, Thomas L. Marzetta and Sriram Vishwanath, Pilot contamination and precoding in multi-cell TDD systems, IEEE Transactions on Wireless Communications 10(8), 2640-2651, 2011"
    locator: "the name pilot contamination, the effect of nonorthogonal training on downlink precoding, and a multicell MMSE-based linear precoder that reduces it"
  - paper: doi:10.1109/TWC.2017.2768423
    title: "Emil Björnson, Jakob Hoydis and Luca Sanguinetti, Massive MIMO has unlimited capacity, IEEE Transactions on Wireless Communications 17(1), 574-590, 2018"
    locator: "the result that with multicell MMSE processing and asymptotically linearly independent channel covariance matrices the capacity grows without bound as the number of antennas grows, even with pilot contamination"
---

Pilot contamination is the error in the channel estimates of a multicell [massive MIMO](/massive-mimo/) system that comes from pilot reuse. In time division duplex (TDD), each base station learns the channels of its users from uplink pilots and uses the same estimates for the uplink combiner and, by reciprocity, for the downlink precoder. A coherence block has room for only a small number $\tau$ of orthogonal pilot sequences, so cells reuse them. When user $k$ in cell $j$ and user $k$ in cell $l$ send the same pilot, base station $j$ cannot tell their channels apart: its estimate is a mix of both. The combiner or precoder built from that estimate then points partly at the user in the other cell. This interference grows with the number of antennas $M$ at the same rate as the wanted signal, so it does not average out. Marzetta (2010) showed that, in his model, it is the only impairment that remains as $M$ grows without bound.

## In plain words

A base station with many antennas learns where each of its users is by listening to a short known signal, the pilot, from each user. There are only a few different pilots, so a user in the next cell sends the same pilot at the same time. The base station hears both and takes the mix as the channel of its own user. When it aims a beam at its own user, part of the beam goes to the other user, and when it listens to its own user, it also hears the other user.

More antennas make the beam sharper, but the beam is sharp in the wrong mixed direction. The wanted signal and this one kind of interference grow together, so their ratio stops at a fixed value. Noise and all other interference fade away as the array grows; this does not.

## The idea

**Model.** There are $L$ cells, each with a base station of $M$ antennas and $K$ single-antenna users. The channel from user $k$ in cell $l$ to base station $j$ is $g_{jlk} = \sqrt{\beta_{jlk}}\, h_{jlk}$, where $\beta_{jlk} > 0$ is the large-scale fading and $h_{jlk} \sim \mathcal{CN}(0, I_M)$ are independent for all $(j, l, k)$ (uncorrelated Rayleigh fading). Every cell uses the same $K$ orthogonal pilots of length $\tau \ge K$, and user $k$ of every cell sends pilot $k$. All users send with power $p$, and the noise has unit power, so $p$ is the SNR per antenna before fading. After it correlates the received pilot signal with pilot $k$, base station $j$ forms the least squares estimate

$$\hat g_{jk} = \sum_{l=1}^{L} g_{jlk} + \frac{1}{\sqrt{\tau p}}\, n_{jk}, \qquad n_{jk} \sim \mathcal{CN}(0, I_M).$$

The estimate has the channels of all $L$ users with pilot $k$ in it. A different estimator does not remove the mix: the [LMMSE estimate](/lmmse-channel-estimation/) in this model is $\hat g_{jk}$ times the scalar $\beta_{jjk} / (\sum_l \beta_{jlk} + 1/(\tau p))$, which points in the same direction.

In the uplink, base station $j$ receives $y_j = \sqrt{p} \sum_{l} \sum_{k'} g_{jlk'}\, x_{lk'} + n_j$ with unit-power data $x_{lk'}$, and decodes user $k$ from $r_{jk} = \hat g_{jk}^H y_j / M$, which is [maximal-ratio combining](/maximal-ratio-combining/) with the estimate.

**Theorem (Marzetta 2010, in this model).** As $M \to \infty$ with $L$, $K$, $\tau$, $p$ and all $\beta$ fixed,

$$r_{jk} \to \sqrt{p} \left( \beta_{jjk}\, x_{jk} + \sum_{l \ne j} \beta_{jlk}\, x_{lk} \right) \quad \text{almost surely},$$

so the SINR of user $k$ in cell $j$ tends to

$$\mathrm{SINR}_{jk}^{\infty} = \frac{\beta_{jjk}^2}{\sum_{l \ne j} \beta_{jlk}^2}.$$

*Proof.* Every term of $r_{jk}$ has the form $\frac{1}{M} u^H v$, where $u$ and $v$ are among the independent Gaussian vectors $h_{jlk'}$, $n_{jk}$ and $n_j$, scaled by constants. For independent $u, v \sim \mathcal{CN}(0, I_M)$ the strong [law of large numbers](/law-of-large-numbers/) gives $\frac{1}{M} u^H u \to 1$ and $\frac{1}{M} u^H v \to 0$ almost surely, because these are means of $M$ independent terms with mean 1 and mean 0 and finite variance. Expand $r_{jk} = \frac{1}{M} \hat g_{jk}^H \big(\sqrt{p} \sum_{l, k'} g_{jlk'} x_{lk'} + n_j\big)$. The term with $\hat g_{jk}^H g_{jlk}$ for pilot $k$ contains $\frac{1}{M} g_{jlk}^H g_{jlk} \to \beta_{jlk}$ and only cross terms otherwise, so it tends to $\sqrt{p}\, \beta_{jlk}\, x_{lk}$. For $k' \ne k$, $\hat g_{jk}$ and $g_{jlk'}$ are independent, so the term tends to 0. The noise term $\frac{1}{M} \hat g_{jk}^H n_j$ tends to 0. Summing the finitely many limits gives the first display. The data symbols are independent with unit power, so the ratio of the power of the wanted term to the power of the rest is the second display. $\square$

Thermal noise, the noise in the estimate, small-scale fading and the interference from users with other pilots all vanish in the limit. Only the users that share pilot $k$ remain. The same argument applied to the downlink, where base station $l$ uses $\hat g_{lk}$ for maximum ratio transmission, gives the limit $\beta_{jjk}^2 / \sum_{l \ne j} \beta_{ljk}^2$ for user $k$ in cell $j$ (theorem, same proof).

**Finite $M$ (closed form).** In the same model, the ratio of the power of the mean wanted signal $\sqrt{p}\, \mathbb{E}[\hat g_{jk}^H g_{jjk}]\, x_{jk}$ to the power of everything else in $\hat g_{jk}^H y_j$ is

$$\mathrm{SINR}_{jk}(M) = \frac{M \beta_{jjk}^2}{S_{jk} \left( \sum_{l, k'} \beta_{jlk'} + \frac{1}{p} \right) + M \sum_{l \ne j} \beta_{jlk}^2}, \qquad S_{jk} = \sum_l \beta_{jlk} + \frac{1}{\tau p}.$$

It follows from $\mathbb{E}\|g\|^4 = (M^2 + M)\beta^2$ for $g \sim \mathcal{CN}(0, \beta I_M)$ and from the independence of all other pairs. The rate $\log_2(1 + \mathrm{SINR}_{jk}(M))$ is the standard lower bound on the achievable rate used in the massive MIMO literature, which treats the part of the signal that the receiver does not know as uncorrelated noise. As $M \to \infty$ it tends to the limit of the theorem, and the $M$ in the denominator is the contamination term.

**Is the limit fundamental?** No, not in general. The cap comes from two choices in the model: uncorrelated fading, under which all users with pilot $k$ look the same to the array apart from their $\beta$, and processing that ignores the other cells. Björnson, Hoydis and Sanguinetti (2018) proved that with multicell MMSE processing the capacity grows without bound in $M$, even with pilot contamination, when the channel covariance matrices of the users that share a pilot are asymptotically linearly independent (theorem, in their model). Contamination is still a large loss at practical $M$, which is why the mitigation methods below are used.

## Examples

**Two cells, one pilot.** Take $L = 2$ cells, one user per cell, the same pilot of length $\tau = 2$ in both cells, $p = 10$ (10 dB), $\beta_{jjk} = 1$ for the own cell and $\beta_{jlk} = 0.1$ for the other cell. The limit is $\mathrm{SINR}^\infty = 1 / 0.01 = 100$, or $\log_2 101 = 6.658$ bits per channel use. With orthogonal pilots in the two cells (no contamination), the denominator has no $M$ term and the SINR grows linearly in $M$. The closed form gives (rates in bits per channel use):

| $M$ | SINR, shared pilot | rate, shared pilot | SINR, orthogonal pilots | rate, orthogonal pilots |
|---|---|---|---|---|
| 10 | 6.76 | 2.955 | 7.94 | 3.160 |
| 100 | 42.02 | 5.427 | 79.37 | 6.328 |
| 1000 | 87.87 | 6.474 | 793.65 | 9.634 |
| 10000 | 98.64 | 6.639 | 7936.5 | 12.954 |

With a shared pilot, ten times more antennas add less and less, and the rate stays below 6.658. With orthogonal pilots, each factor of ten adds about $\log_2 10 = 3.3$ bits.

**A measurement.** In the same setup, a simulation of the instantaneous SINR with the channel realizations known (4000 trials per point, 500 at $M = 10000$, fixed seed) gives mean rates of 5.11, 6.48, 6.64 and 6.65 bits per channel use with a shared pilot at $M = 10, 100, 1000, 10000$, and 5.67, 9.05, 12.33 and 15.66 with orthogonal pilots. These rates are higher than the closed form, which is a lower bound, but they show the same cap at 6.658 (measurement).

## Where it is used

- **Pilot assignment and reuse.** Giving neighboring cells different pilots, with a reuse factor of 3 or 7 as for frequencies, removes the strongest contaminating users at the cost of a longer $\tau$ and so fewer data symbols per block. Pilot assignment algorithms give the same pilot to users that are far apart, so that their $\beta_{jlk}$ is small. [Zadoff-Chu sequences](/zadoff-chu-sequence/) are a common choice of pilot sequence in the 4G and 5G uplink.
- **Multicell precoding and combining.** Jose et al. (2011), who named the effect, proposed a multicell MMSE-based precoder that uses the $\beta$ of the other cells. Multicell MMSE processing with spatially correlated channels removes the cap in the sense of Björnson et al. (2018).
- **Power control.** The limit depends only on the $\beta$ values, so [max-min SINR power control](/max-min-sinr-power-control/) of the pilot and data powers changes the limit directly.
- **Cell-free systems.** In [cell-free massive MIMO](/cell-free-massive-mimo/) there are no cells, but users that share a pilot still contaminate each other's estimates at every access point, so pilot assignment is part of the design.
- **System dimensioning.** The theorem tells how much a larger array can help at a given pilot reuse, which is a design input next to [channel hardening](/channel-hardening/) and [favorable propagation](/favorable-propagation/).

## References
