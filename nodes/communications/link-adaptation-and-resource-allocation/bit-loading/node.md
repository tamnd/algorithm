---
tag: XSKM4M
kind: problem
slug: bit-loading
name: Bit loading
aliases:
- bit and power loading
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Give each subcarrier of a multicarrier link an integer number of bits and a power, either to reach a bit target with the least power or to carry the most bits under a power budget."
model: word-ram
complexity:
  vars: {N: the number of subcarriers, B: the number of bits loaded}
  time: {worst: O(N + B log N)}
prereqs: [water-filling-power-allocation, snr-gap-approximation]
see_also: [hughes-hartogs-algorithm, levin-campello-algorithm, chow-cioffi-bingham-algorithm, discrete-multitone, orthogonal-frequency-division-multiplexing, greedy-algorithm, adaptive-modulation, link-adaptation]
sources:
  - url: https://patents.google.com/patent/US4679227A/en
    title: "Dirk Hughes-Hartogs, Ensemble modem structure for imperfect transmission media, US Patent 4,679,227, filed May 20, 1985, issued July 7, 1987"
    locator: "the allocation of bits one at a time to the carrier that needs the least additional power"
  - paper: doi:10.1109/ICC.1999.765384
    title: "Jorge Campello, Practical bit loading for DMT, IEEE International Conference on Communications (ICC), 1999, pages 801 to 805"
    locator: "the efficiency and tightness conditions for an optimal discrete loading and the algorithm that reaches them"
  - paper: doi:10.1287/mnsc.13.3.210
    title: "Bennett Fox, Discrete optimization via marginal analysis, Management Science 13(3), 1966, pages 210 to 216"
    locator: "marginal allocation for separable objectives with convex costs, the general form of greedy bit loading"
  - paper: doi:10.1109/26.380108
    title: "Peter S. Chow, John M. Cioffi and John A. C. Bingham, A practical discrete multitone transceiver loading algorithm for data transmission over spectrally shaped channels, IEEE Transactions on Communications 43(2/3/4), 1995, pages 773 to 775"
    locator: "the rate-adaptive and margin-adaptive forms of the loading problem and a fast loading algorithm for DMT"
---

Bit loading is the problem of giving each subcarrier of a multicarrier link, such as a [DMT](/discrete-multitone/) or [OFDM](/orthogonal-frequency-division-multiplexing/) system, an integer number of bits $b_i$ and a power $p_i$. Subcarrier $i$ has the SNR $g_i$ per unit of power, and with the [SNR gap](/snr-gap-approximation/) $\Gamma$ it needs the power $e_i(b) = \Gamma(2^{b} - 1)/g_i$ to carry $b$ bits at the target error rate. The margin-adaptive form asks for $B$ bits in total with the least power; the rate-adaptive form asks for the most bits within a power budget $P$. It is the integer form of [water-filling](/water-filling-power-allocation/). Because the cost of each extra bit doubles, the greedy rule of adding the cheapest next bit is optimal, and the [Hughes-Hartogs](/hughes-hartogs-algorithm/) and [Levin-Campello](/levin-campello-algorithm/) algorithms solve it exactly.

## In plain words

A multicarrier modem sends data on many narrow tones at once. Some tones arrive strong and some weak. Each tone carries a whole number of bits per symbol, and more bits on a tone need much more power on it, because each extra bit doubles the power that the tone needs.

The modem must decide how many bits to put on each tone. It may have a fixed number of bits to send and want to use the least power. Or it may have a fixed power and want to send as many bits as it can. Weak tones get few bits or none. Strong tones get many.

## Definition

**Input.** The gains $g_1, \ldots, g_N > 0$ (the SNR of each subcarrier per unit of power, which already includes the noise), the gap $\Gamma \ge 1$, and a bit cap $b_{\max}$ per subcarrier. The power to carry $b$ bits on subcarrier $i$ is

$$e_i(b) = \frac{\Gamma\,(2^{b} - 1)}{g_i}, \qquad b = 0, 1, \ldots, b_{\max},$$

and the cost of the next bit is $\Delta e_i(b) = e_i(b+1) - e_i(b) = \Gamma\, 2^{b}/g_i$.

**Margin-adaptive (MA) form.** Given the target $B$, find integers $b_i \in [0, b_{\max}]$ with $\sum_i b_i = B$ that minimize the total power $\sum_i e_i(b_i)$.

**Rate-adaptive (RA) form.** Given the budget $P$, find integers $b_i \in [0, b_{\max}]$ that maximize $\sum_i b_i$ subject to $\sum_i e_i(b_i) \le P$. Among the best answers, one with the least power is preferred.

**Output.** The bits $b_i$ and the powers $p_i = e_i(b_i)$.

The two forms are linked: the least MA power $E^*(B)$ grows with $B$, so the RA answer is the largest $B$ with $E^*(B) \le P$. The gap $\Gamma$ scales every cost by the same factor, so it does not change the MA allocation, only its power; in the RA form it acts as a smaller budget $P/\Gamma$.

## Variants

- **Margin maximization.** Fix $B$ and $P$ and maximize a margin $\gamma_m$ common to all subcarriers. The MA answer for $B$ gives the margin $P/E^*(B)$, so this is the MA form again.
- **Granularity.** Some systems load bits in steps of $\beta$, for example $\beta = 2$ to keep to square QAM. The costs keep their increasing increments, and the same algorithms apply with the step $\beta$.
- **Per-subcarrier power limits.** A spectral mask adds $p_i \le c_i$, which caps $b_i$ at the largest $b$ with $e_i(b) \le c_i$. This is a different $b_{\max}$ per subcarrier.
- **General cost tables.** Any cost $e_i(b)$ taken from a table of measured thresholds per constellation. The greedy methods stay optimal only while each table has increasing increments.
- **Multiuser loading.** In OFDMA several users share the subcarriers and each subcarrier goes to one user. In DSL bundles the users interfere with each other through crosstalk. These problems are harder and are usually solved with Lagrangian or iterative methods.

## Examples

**A four-carrier channel.** Let $g = (20, 9, 5, 1.5)$ and $\Gamma = 1$. The costs of the next bit are $2^{b}/g_i$: $0.05, 0.1, 0.2, 0.4, \ldots$ on carrier 1, $1/9, 2/9, 4/9, \ldots$ on carrier 2, $0.2, 0.4, 0.8, \ldots$ on carrier 3, and $2/3, 4/3, \ldots$ on carrier 4.

- **MA with $B = 8$.** The eight cheapest bits are $0.05, 0.1, 1/9, 0.2, 0.2, 2/9, 0.4, 0.4$, which gives $b = (4, 2, 2, 0)$ with total power $101/60 \approx 1.6833$. A search over every split of 8 bits confirms this is the least. Equal loading $(2, 2, 2, 2)$ needs $3.0833$.
- **RA with $P = 2$.** The ninth bit would cost $4/9$ and bring the total to $2.1278 > 2$, so the answer is again 8 bits, with $b = (4, 2, 2, 0)$.
- **The continuous relaxation.** Water-filling the same budget $P = 2$ over the noise levels $1/g_i$ gives the rates $(3.920, 2.768, 1.920, 0.183)$, a total of $8.792$ bits. Rounding each rate down gives $(3, 2, 1, 0)$, only 6 bits; the integer optimum of 8 bits is much better than rounding. For $B = 8$, the continuous least power is $1.6119$, against $1.6833$ for integers.

**When the greedy rule fails.** If a cost table does not have increasing increments, the cheapest next bit can be a trap. Take two subcarriers with next-bit costs $(4, 1)$ on the first and $(3, 3)$ on the second, and $B = 2$. The greedy rule takes 3 and then 3, a total of 6; two bits on the first cost $4 + 1 = 5$. Costs of the form $\Gamma(2^b - 1)/g_i$ never do this.

## Known algorithms

| algorithm | form | result | time |
|---|---|---|---|
| [Hughes-Hartogs](/hughes-hartogs-algorithm/) (1987) | MA and RA | optimal for increasing increments | $O(N + B \log N)$ with a heap |
| [Levin-Campello](/levin-campello-algorithm/) (1998 to 2001) | MA and RA | optimal for increasing increments | $O(N \log N)$ plus one heap step per bit moved from a given start |
| [Chow-Cioffi-Bingham](/chow-cioffi-bingham-algorithm/) (1995) | MA and RA | near optimal, not optimal in general | $O(N)$ per margin iteration, with a fixed cap on iterations |
| water-filling then rounding | RA | a heuristic | $O(N \log N)$ |

Marginal allocation, as Fox (1966) analysed it for separable resource problems with convex costs, is the general form of the Hughes-Hartogs rule. Levin-Campello starts from any loading, for example rounded water-filling, and moves bits only where they are wrong, so it is faster when the start is close. Chow-Cioffi-Bingham works with real-valued rates and a margin, and rounds; it is the fast method of DSL practice.

## Bounds

- **Time.** Every algorithm must read all $N$ gains, so $\Omega(N)$ time is needed. The heap greedy adds $O(B \log N)$ for $B$ bits.
- **Against the continuous rate.** Let $C$ be the water-filling rate $\sum_i \log_2(1 + p_i g_i/\Gamma)$ at budget $P$. Then the RA optimum $B^*$ satisfies $C - N < B^* \le C$. The upper bound holds because the integer problem is a restriction of the continuous one. For the lower bound, rounding each water-filling rate down lowers each power, so the result fits in $P$, and it loses less than one bit per subcarrier. In the example, $8.792 - 4 < 8 \le 8.792$.
- **Gap.** The integer loss is at most $N$ bits per multicarrier symbol, while the gap $\Gamma$ costs about $\log_2 \Gamma$ bits on every active subcarrier at high SNR. For uncoded QAM at $10^{-7}$ that is about 3.2 bits per subcarrier, much more than the integer loss.

## Reductions

- **To marginal allocation.** Both forms are separable integer resource problems with a convex cost per variable. The MA form takes the $B$ smallest elements of the multiset of all increments $\Delta e_i(b)$, which is correct exactly when each list of increments is increasing; the proof is an exchange argument.
- **RA to MA.** Since $E^*(B)$ is increasing, the RA problem is a search for the largest feasible $B$. The greedy order computes $E^*(1), E^*(2), \ldots$ in one pass and stops at the first $B$ that does not fit.
- **From water-filling.** With the integer constraint removed, the RA form becomes water-filling on the levels $\Gamma/g_i$, and its answer is a starting point for Levin-Campello.

## Applications

- ADSL and VDSL modems, where the receiver measures the SNR of each tone in training and sends the bit and gain table back to the transmitter.
- Power line modems and some wired OFDM systems with slowly changing channels.
- Wireless OFDM with channel feedback, though most cellular systems use one modulation and code for a block of subcarriers and adapt it by [link adaptation](/link-adaptation/), since per-subcarrier tables cost too much feedback.
- Optical OFDM and discrete multitone links over fibre, where the channel is static enough for loading.

## References
