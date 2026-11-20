---
tag: KRYPZ8
kind: algorithm
slug: chow-cioffi-bingham-algorithm
name: Chow-Cioffi-Bingham algorithm
aliases:
- Chow bit loading
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Fast DMT bit loading: compute real rates log2(1 + SNR/(Gamma margin)), round them, adjust the margin until the rounded total meets the target, then fix the last bits and scale the energies."
solves: [bit-loading]
model: real-ram
complexity:
  vars: {N: the number of subcarriers, K: the number of margin rounds (at most MaxCount), F: the number of bits moved by the fix-up}
  time: {worst: O(N (K + F))}
  space: {extra: O(N)}
properties: {deterministic: true, optimal: false, heuristic: true, needs_csit: true}
history:
  year: 1995
  people: [Peter S. Chow, John M. Cioffi, John A. C. Bingham]
  note: "Published in the IEEE Transactions on Communications in 1995 as a practical loading algorithm for discrete multitone transceivers on spectrally shaped channels such as telephone lines."
prereqs: [bit-loading, snr-gap-approximation]
see_also: [hughes-hartogs-algorithm, levin-campello-algorithm, water-filling-power-allocation, discrete-multitone, orthogonal-frequency-division-multiplexing, adaptive-modulation, bisection-method, link-adaptation]
sources:
  - paper: doi:10.1109/26.380108
    title: "Peter S. Chow, John M. Cioffi and John A. C. Bingham, A practical discrete multitone transceiver loading algorithm for data transmission over spectrally shaped channels, IEEE Transactions on Communications 43(2/3/4), 1995, pages 773 to 775"
    locator: "the loading algorithm: unit energy per carrier at the start, the rounded rates log2(1 + SNR/(Gamma + margin in dB)), the margin iteration and the final energy adjustment"
  - paper: doi:10.1109/35.54342
    title: "John A. C. Bingham, Multicarrier modulation for data transmission: an idea whose time has come, IEEE Communications Magazine 28(5), 1990, pages 5 to 14"
    locator: "multicarrier modems that load each subchannel according to its SNR, the setting of the algorithm"
  - paper: doi:10.1109/ICC.1999.765384
    title: "Jorge Campello, Practical bit loading for DMT, IEEE International Conference on Communications (ICC), 1999, pages 801 to 805"
    locator: "optimal discrete loading, against which heuristics such as this one are compared"
---

The Chow-Cioffi-Bingham algorithm is a fast heuristic for [bit loading](/bit-loading/) in [discrete multitone](/discrete-multitone/) modems. It starts with unit energy on every subcarrier and computes a real rate $b_i = \log_2(1 + \mathrm{SNR}_i/(\Gamma \gamma))$ for each, with the [SNR gap](/snr-gap-approximation/) $\Gamma$ and a margin $\gamma$ that starts at 0 dB. It rounds the rates, compares their sum with the target, and changes the margin by $10 \log_{10} 2^{(B_{\mathrm{total}} - B_{\mathrm{target}})/U}$ dB, where $U$ is the number of subcarriers in use; this is about 3 dB per missing or extra bit per subcarrier. After a few rounds it fixes the remaining difference one bit at a time, using the rounding errors, and finally gives each used subcarrier the energy its bits need and scales all energies to the budget. Each round costs $O(N)$. The result meets the target exactly and gives every used subcarrier the same margin, but unlike the [Hughes-Hartogs](/hughes-hartogs-algorithm/) and [Levin-Campello](/levin-campello-algorithm/) algorithms it is not optimal in general.

## In plain words

A modem must place a fixed number of bits on its tones. The slow, exact method places the bits one at a time.

This method is faster. It first asks: with equal power on every tone and a given safety margin, how many bits could each tone carry? It rounds each answer to a whole number and adds them up. If the sum is too large, it asks for a bigger margin; if too small, a smaller one, and it repeats a few times. Then it fixes the last few bits by hand, picking the tones that were rounded the most. Last, it sets the power of each tone so that all used tones have the same safety margin.

## The problem

This is the margin-adaptive form of [bit loading](/bit-loading/): carry exactly $B_{\mathrm{target}}$ bits with the total energy $P$ and the largest margin that is common to all used subcarriers. Subcarrier $i$ has $\mathrm{SNR}_i$ at unit energy. Under the gap model, $\hat b_i$ bits at the energy $e_i$ have the margin $e_i \mathrm{SNR}_i / (\Gamma(2^{\hat b_i} - 1))$. The largest common margin is $P/E^*(B)$, where $E^*(B)$ is the least energy for $B$ bits at margin 1, and the optimal algorithms reach it. This algorithm reaches a common margin that is usually close to it.

## The algorithm

$\Gamma$ and $\gamma$ are linear factors here; the paper writes the sum of the gap and the margin in dB.

```pseudo id=main
CHOW-CIOFFI-BINGHAM(SNR[1..N], Γ, B_target, P, MaxCount)   ▷ SNR_i at unit energy
L1  γ_dB ← 0, count ← 0
L2  repeat: b_i ← log2(1 + SNR_i / (Γ · 10^(γ_dB/10))), b̂_i ← round(b_i), diff_i ← b_i - b̂_i
L3      B_total ← Σ b̂_i, U ← the number of i with b̂_i > 0
L4      γ_dB ← γ_dB + 10 log10(2^((B_total - B_target)/U)), count ← count + 1
L5  until B_total = B_target or count = MaxCount
L6  while B_total ≠ B_target: if B_total > B_target, take a bit from the i with b̂_i > 0 and the smallest diff_i (diff_i ← diff_i + 1); else add a bit to the i with the largest diff_i (diff_i ← diff_i - 1)
L7  e_i ← Γ (2^(b̂_i) - 1) / SNR_i  for i = 1 .. N    ▷ the energy for b̂_i bits at margin 1
L8  scale every e_i by P / Σ_j e_j and return (b̂, e)
```

The test code uses $\mathrm{MaxCount} = 10$. A channel that loads no bit in the first round is reported as unusable. With a cap $b_{\max}$, line L2 clips $\hat b_i$ to it, and line L6 adds bits only below it.

## Example

Take $\mathrm{SNR} = (20, 9, 5, 1.5)$ at unit energy, $\Gamma = 1$, $B_{\mathrm{target}} = 8$, and the budget $P = 4$, one unit per subcarrier.

| round | margin before | real rates $b_i$ | rounded | $B_{\mathrm{total}}$ | margin step |
|---|---|---|---|---|---|
| 1 | 0 dB | 4.392, 3.322, 2.585, 1.322 | (4, 3, 3, 1) | 11 | $+2.258$ dB (3 extra bits over 4 carriers) |
| 2 | 2.258 dB | 3.688, 2.667, 1.990, 0.920 | (4, 3, 2, 1) | 10 | $+1.505$ dB |
| 3 | 3.763 dB | 3.234, 2.258, 1.633, 0.706 | (3, 2, 2, 1) | 8 | stop |

The loading $(3, 2, 2, 1)$ needs $0.35 + 0.333 + 0.6 + 0.667 = 1.95$ units at margin 1. Line L8 scales by $4/1.95$, so the energies are $(0.718, 0.684, 1.231, 1.368)$ and the common margin is $2.051$, or 3.12 dB. The optimal loading $(4, 2, 2, 0)$ needs $101/60 \approx 1.6833$, for a margin of 3.76 dB; the heuristic gives up 0.64 dB here.

With $\mathrm{MaxCount} = 1$, the fix-up starts from round 1: $(4, 3, 3, 1)$ with $\mathrm{diff} = (0.392, 0.322, -0.415, 0.322)$. It removes a bit from carrier 3, then from carrier 2 and carrier 4, whose rounding errors are equal, and reaches $(4, 2, 2, 0)$, which is optimal. More margin rounds are not always better.

## Correctness

**Claim.** If the first round loads at least one bit, the algorithm stops, the output carries exactly $B_{\mathrm{target}}$ bits, the energies add up to $P$, and every used subcarrier has the same margin $\gamma^* = P / \sum_j \Gamma(2^{\hat b_j} - 1)/\mathrm{SNR}_j$. This margin is at most the optimal margin $P/E^*(B_{\mathrm{target}})$, with equality when the rounded loading is optimal.

**Key steps.** The margin loop has at most $\mathrm{MaxCount}$ rounds. Each fix-up step moves $B_{\mathrm{total}}$ one bit toward the target, and a subcarrier to change always exists, so the fix-up takes exactly $|B_{\mathrm{total}} - B_{\mathrm{target}}|$ steps. Lines L7 and L8 make $e_i$ proportional to the energy that $\hat b_i$ bits need at margin 1, so all used subcarriers get the same factor $\gamma^*$. Raising the margin by $2^t$ lowers each real rate by at most $t$ bits, and by almost exactly $t$ on strong subcarriers, which is why the step of line L4 aims at the target. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/), each round of lines L2 to L4 costs $O(N)$, and there are $K \le \mathrm{MaxCount}$ rounds. Each fix-up step of line L6 scans the subcarriers in $O(N)$; with the rounding errors sorted once, the fix-up costs $O(N \log N + F)$ instead, because a subcarrier changed once has the largest or smallest error until all others have changed. Lines L7 and L8 cost $O(N)$. So the time is $O(N(K + F))$ as written, and the space is $O(N)$. The Hughes-Hartogs rule needs $O(N + B \log N)$, which is much more when each of thousands of tones carries many bits.

## Properties

- **Exact target, common margin.** The output always meets the bit target, and all used subcarriers have the same margin, so under the gap model they have the same error rate.
- **Not optimal.** The rounding to the nearest integer ignores the costs of the bits. The example loses 0.64 dB against the optimum.
- **Usually close.** On random channels with many subcarriers and a gap of 9.8 dB, the test code measures a mean loss of under 0.3 dB of margin; this is a measurement, not a bound.
- **Few rounds.** At high SNR one margin step nearly corrects the total, since each bit per subcarrier costs about 3.01 dB.
- **No sort and no heap in the main loop.** This made it attractive for the modem hardware of the 1990s.

## Variants and improvements

- **Rate-adaptive form.** Fix the margin, compute the rounded rates once, and scale the energies; the result is the rate that the channel supports at that margin.
- **Bisection on the margin.** Search the margin by [bisection](/bisection-method/) for the value where the rounded total crosses the target, then fix up; this replaces the step of line L4 when the loop does not settle.
- **A final optimal pass.** Run the swap phase of the [Levin-Campello algorithm](/levin-campello-algorithm/) on the output. Since the output is already close, few swaps are needed, and the result is optimal.
- **Fine gains.** DSL modems apply a fine gain per tone, a small energy adjustment that equalizes the margins; line L8 is a simple form of it.

## When to use it

Use it for a fast first loading of many tones, as in the training phase of a DSL modem, when an exact optimum is not needed or when a repair pass will follow. For an exact result use the [Hughes-Hartogs](/hughes-hartogs-algorithm/) or [Levin-Campello](/levin-campello-algorithm/) algorithm.

## Pitfalls

- **The margin in dB.** The paper writes the denominator as the gap plus the margin in dB, which is a product of linear factors. Adding linear values is a bug.
- **Division by zero.** If a round loads no bit, $U = 0$ and line L4 is undefined. Stop or report the channel as unusable.
- **Cycling.** The margin step can overshoot, for example when several subcarriers are near a rounding boundary. Keep $\mathrm{MaxCount}$ and the fix-up.
- **Rounding of halves.** Some languages round halves to even. Pick one rule and use it in both the loop and the fix-up.
- **Forgetting the scaling.** Without line L8 the total energy can exceed the budget or waste it, and the margins of the subcarriers differ.

## Implementations

## History

Peter Chow, John Cioffi and John Bingham published the algorithm in 1995 in the IEEE Transactions on Communications, in a short paper on a practical loading method for discrete multitone transceivers on spectrally shaped channels such as telephone lines. It came from the work on DMT for ADSL, and it was an alternative to the greedy method of Hughes-Hartogs, whose cost grows with the number of bits. Later work, such as Campello's 1999 paper, gave fast loading methods that are also optimal.

## References
