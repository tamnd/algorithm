---
tag: 1Y9CA5
kind: algorithm
slug: water-filling-power-allocation
name: Water-filling power allocation
aliases:
- water-pouring algorithm
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Splits a power budget over parallel Gaussian channels as p_i = max(0, mu - nu_i), filling up to a common water level mu above each noise level. This maximizes the sum rate."
model: real-ram
complexity:
  vars: {N: the number of parallel channels}
  time: {worst: O(N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, optimal: true, needs_csit: true, continuous_rates: true}
history:
  year: 1949
  people: [Claude E. Shannon]
  note: "Shannon's 1949 paper gave the rule for a channel whose noise spectrum is not flat: the signal power plus the noise power is constant over the band that is used."
prereqs: [kkt-conditions, channel-capacity, additive-white-gaussian-noise-channel]
see_also: [snr-gap-approximation, bit-loading, hughes-hartogs-algorithm, svd-precoding, mimo-capacity, truncated-channel-inversion, adaptive-modulation, discrete-multitone]
sources:
  - book: isbn:9780471241959
    title: "Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006"
    locator: "Section 9.4 (parallel Gaussian channels, the water-filling solution) and Section 9.5 (channels with colored Gaussian noise)"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Chapter 5 (water-filling over the subcarriers of a frequency-selective channel, and over time for a fading channel with transmitter side information)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 4 (capacity of fading channels with side information at the transmitter and of frequency-selective channels)"
  - paper: doi:10.1109/JRPROC.1949.232969
    title: "Claude E. Shannon, Communication in the presence of noise, Proceedings of the IRE 37(1), 1949, pages 10 to 21"
    locator: "the capacity of a band with noise of arbitrary spectrum and the best distribution of the signal power"
---

Water-filling power allocation divides a total power $P$ over $N$ parallel Gaussian channels so that the sum of their rates is as large as possible. Channel $i$ has the noise level $\nu_i > 0$, its noise power divided by its power gain. The best power is $p_i = \max(0, \mu - \nu_i)$, where the water level $\mu$ is the one number that makes the powers add up to $P$. So the strong channels get more power, and channels whose noise level is above $\mu$ get none. The optimality is a direct consequence of the [KKT conditions](/kkt-conditions/). The same allocation gives the [capacity](/channel-capacity/) of an OFDM link with a known channel, of a MIMO channel over its singular values (see [SVD precoding](/svd-precoding/) and [MIMO capacity](/mimo-capacity/)), and of a fading channel over time. With integer bits per channel the problem is [bit loading](/bit-loading/), and the [SNR gap](/snr-gap-approximation/) turns the capacity formula into a rule for real constellations.

## In plain words

Picture a tank whose floor has steps of different heights, one step for each channel. The height of a step is the noise of that channel. Pour a fixed amount of water into the tank. The water settles at one flat level. Deep steps, the quiet channels, hold a lot of water. High steps, the noisy channels, hold a little. A step that sticks out above the water holds none.

The water is the power. Each channel gets the amount of water above its step. This split gives the largest total data rate, because the next small unit of power always does the most good where the water is lowest above the floor, and pouring makes all the used channels equal in that sense.

## The problem

The input is a list of noise levels $\nu_1, \ldots, \nu_N > 0$ and a total power $P > 0$. For a channel $y_i = h_i x_i + w_i$ with $w_i \sim \mathcal{CN}(0, N_{0,i})$, the noise level is $\nu_i = N_{0,i}/|h_i|^2$, the noise power referred to the input. With the power $p_i = E|x_i|^2$ and Gaussian inputs, channel $i$ carries $\log_2(1 + p_i/\nu_i)$ bits per complex channel use, since its SNR is $p_i |h_i|^2 / N_{0,i}$. The output is the power vector that solves

$$\max_{p \ge 0} \; \sum_{i=1}^{N} \log_2\!\left(1 + \frac{p_i}{\nu_i}\right) \quad \text{subject to} \quad \sum_{i=1}^{N} p_i \le P.$$

For OFDM, $i$ is the subcarrier and $h_i$ is the DFT of the channel taps at bin $i$. For a MIMO channel with transmitter knowledge, $\nu_i = N_0/\sigma_i^2$ for the singular values $\sigma_i$ of $H$.

## The algorithm

```pseudo id=main
WATER-FILL(ν[1..N], P)                       ▷ ν_i > 0, P > 0
L1  s ← the levels ν sorted so that s[1] ≤ s[2] ≤ .. ≤ s[N]
L2  S ← 0, k ← 0                               ▷ S = s[1] + .. + s[k]
L3  while k < N and k · s[k+1] < P + S do      ▷ is s[k+1] below the water?
L4      S ← S + s[k+1], k ← k + 1
L5  μ ← (P + S) / k                            ▷ the water level
L6  p_i ← max(0, μ - ν_i)  for i = 1 .. N
L7  return (p, μ)
```

If the first $k$ channels are used and the water stands at $s[k+1]$, they hold $k\, s[k+1] - S$ units of power. So the test of line L3 asks whether the power $P$ is enough to raise the water to the next step. When the answer is no, the active set is the first $k$ channels, and line L5 spreads $P$ over them so that each one reaches the same level. The first test, with $k = 0$, is $0 < P$, so at least one channel is active.

## Example

Take the noise levels $\nu = (1, 2, 4)$ and $P = 3$.

| $k$ | $s[k+1]$ | $k \cdot s[k+1]$ | $P + S$ | test of L3 |
|---|---|---|---|---|
| 0 | 1 | 0 | 3 | true, $S = 1$ |
| 1 | 2 | 2 | 4 | true, $S = 3$ |
| 2 | 4 | 8 | 6 | false |

So two channels are active and $\mu = (3 + 3)/2 = 3$. The powers are $p = (2, 1, 0)$: the water stands 2 above the first step and 1 above the second, and the third step, at 4, is dry. The sum rate is $\log_2 3 + \log_2 1.5 = 2.1699$ bits per channel use. Equal power, $p = (1, 1, 1)$, gives $\log_2 2 + \log_2 1.5 + \log_2 1.25 = 1.9069$ bits.

The level depends on $P$. With the same channels, $P = 0.5$ gives $\mu = 1.5$ and puts all the power on the best channel. $P = 10$ gives $\mu = 17/3$, all three channels active, and the powers $(4.667, 3.667, 1.667)$ for 4.5075 bits. As $P$ grows, the differences $\nu_i$ become small next to $\mu$, and water-filling approaches equal power.

A second case: $\nu = (0.5, 1, 1.5, 3)$ and $P = 2$. The loop stops at $k = 3$, because $3 \cdot 3 = 9$ is not less than $2 + 3 = 5$. Then $\mu = 5/3$, the powers are $(7/6, 2/3, 1/6, 0)$, and the sum rate is 2.6259 bits.

## Correctness

**Claim.** WATER-FILL returns the unique optimal power vector of the problem above, and $\mu$ is the unique solution of $\sum_i \max(0, \mu - \nu_i) = P$.

**Key steps.** The objective is a sum of strictly concave functions and the constraints are linear, so the KKT conditions are necessary and sufficient, and the optimum is unique. They say that the power constraint holds with equality, that $\nu_i + p_i = \mu$ on each channel with $p_i > 0$, and that $\nu_i \ge \mu$ on each channel with $p_i = 0$. That is $p_i = \max(0, \mu - \nu_i)$. The function $f(t) = \sum_i \max(0, t - \nu_i)$ is continuous and strictly increasing for $t \ge s[1]$, so exactly one $\mu$ gives $f(\mu) = P$. For sorted levels, $f(s[k+1]) = k\, s[k+1] - S$, so the test of line L3 is $f(s[k+1]) < P$, which holds exactly when $s[k+1] < \mu$. The loop therefore stops with $k$ equal to the number of levels below $\mu$, and line L5 solves $f(\mu) = P$ on that set. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/), line L1 sorts in $O(N \log N)$ time. The loop of lines L3 and L4 runs at most $N$ times with $O(1)$ work each, and line L6 takes $O(N)$. So the time is $O(N \log N)$ in the worst case, and the extra space is $O(N)$ for the sorted copy. If the levels arrive sorted, the time is $O(N)$. Without the sort, a search for the active count by repeated median selection, as in the linear-time algorithm for the fractional knapsack problem, also runs in $O(N)$ worst-case time. A bisection on $\mu$ costs $O(N)$ per step and needs about $\log_2(P/\epsilon)$ steps for the accuracy $\epsilon$; it is simple and is the usual choice when the constraint has extra terms.

## Properties

- **One water level.** All active channels end at the same total $\nu_i + p_i = \mu$. In the dual view, $\mu = 1/(\lambda \ln 2)$, where $\lambda$ is the [Lagrange multiplier](/lagrange-multiplier/) of the power constraint, the rate gained per unit of extra power.
- **Monotone in the channel.** A channel with a lower noise level never gets less power than a channel with a higher one.
- **Low and high power.** For $P \le s[2] - s[1]$, all the power goes to the best channel. As $P \to \infty$, every channel becomes active and $p_i - P/N \to \bar\nu - \nu_i$, where $\bar\nu$ is the mean noise level; the rate gain over equal power tends to 0.
- **Rate.** The sum rate is $\sum_{i \le k} \log_2(\mu / \nu_{(i)})$ over the active channels.
- **Gaussian inputs.** The rate formula and so the optimality assume Gaussian codebooks. With a fixed constellation such as QAM, the rate of each channel saturates at $\log_2 M$, and the best allocation is different (see Variants).

## Variants and improvements

- **Water-filling with a gap.** With a practical code, channel $i$ carries about $\log_2(1 + p_i/(\Gamma \nu_i))$ bits, where $\Gamma$ is the [SNR gap](/snr-gap-approximation/). This is water-filling on the levels $\Gamma \nu_i$.
- **Integer bits.** Rounding the water-filling rates gives a good start for [bit loading](/bit-loading/), and the [Hughes-Hartogs](/hughes-hartogs-algorithm/) and [Levin-Campello](/levin-campello-algorithm/) algorithms find the best integer loading.
- **Weighted sum rate.** Maximizing $\sum_i w_i \log_2(1 + p_i/\nu_i)$ gives $p_i = \max(0, w_i \mu - \nu_i)$, a water level that differs per channel.
- **Peak limits per channel.** With $p_i \le c_i$, as under a spectral mask, the answer is $p_i = \min(c_i, \max(0, \mu - \nu_i))$, and $\mu$ is found by the same search.
- **Water-filling over time.** For a fading channel with the gain known at both ends and an average power limit, the power at the SNR $\gamma$ is $\max(0, 1/\gamma_0 - 1/\gamma)$ times the average power (Goldsmith and Varaiya 1997). [Truncated channel inversion](/truncated-channel-inversion/) and [adaptive modulation](/adaptive-modulation/) are the practical forms.
- **Finite constellations.** Lozano, Tulino and Verdú (2006) gave the best allocation for arbitrary input distributions, called mercury/water-filling. It puts less power on strong channels whose constellation is already saturated.
- **Many users.** Iterative water-filling lets each user water-fill against the interference of the others; for the Gaussian vector multiple-access channel it converges to the sum capacity (Yu, Rhee, Boyd and Cioffi 2004).
- **Reverse water-filling.** The rate-distortion function of parallel Gaussian sources has the dual form, with a water level on the variances.

## When to use it

Use water-filling when the transmitter knows the gain of each parallel channel, as in DSL modems, OFDM with channel feedback, and MIMO with transmitter knowledge, and when the codes are good enough that the gap model holds. At high SNR the gain over equal power is small, and many systems use equal power on the active channels. When the rates must be integers, use water-filling for the start and a bit loading algorithm for the end.

## Pitfalls

- **Gains in place of noise levels.** The input is the noise-to-gain ratio $\nu_i = N_{0,i}/|h_i|^2$, not the gain. Passing $|h_i|^2$ gives the most power to the worst channel.
- **dB values.** The formula works on linear values. Convert $\nu_i$ and $P$ from dB first.
- **The wrong active set.** Spreading $P$ over all channels and then clipping negative powers to zero breaks the power constraint. The active set must be found first, as in line L3, or by a search on $\mu$.
- **Ties.** Equal noise levels are in or out together. The strict test $<$ in line L3 keeps a channel whose level equals $\mu$ out, which is correct, because its power would be 0.
- **Stale channel knowledge.** The allocation is only as good as the estimates of $\nu_i$. A channel that is weaker than the transmitter believes gets too much rate and causes errors; a margin, or the outer loop of [link adaptation](/outer-loop-link-adaptation/), protects against this.
- **Nats and bits.** Some texts use $\ln$. The allocation is the same, but the rate differs by the factor $\ln 2$.

## Implementations

## History

Shannon's 1949 paper found the best signal spectrum for a channel with noise that is not white: the signal power plus the noise power is constant over the band that is used, and no power goes where the noise is above that level. The parallel channel form, with the picture of water poured over an uneven floor, became standard in information theory texts, and Cover and Thomas give it for parallel Gaussian channels and for colored noise. In the late 1980s and 1990s it became an engineering tool for multicarrier modems, where the transmitter learns the SNR of each subcarrier and loads it, and later for MIMO with feedback.

## References
