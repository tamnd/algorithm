---
tag: YMENDP
kind: algorithm
slug: hughes-hartogs-algorithm
name: Hughes-Hartogs algorithm
aliases:
- greedy bit loading
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Adds bits one at a time to the subcarrier where the next bit costs the least power. This gives the optimal integer loading when the incremental costs increase on each subcarrier."
solves: [bit-loading]
model: word-ram
complexity:
  vars: {N: the number of subcarriers, B: the number of bits loaded}
  time: {worst: O(N + B log N)}
  space: {extra: O(N)}
properties: {deterministic: true, optimal: true, greedy: true, needs_csit: true}
history:
  year: 1987
  people: [Dirk Hughes-Hartogs]
  note: "The US patent 4,679,227, filed in 1985 and issued in 1987 to Telebit, describes a modem that allocates bits and power to its carriers one unit at a time, each to the carrier that needs the least additional power."
prereqs: [bit-loading, greedy-algorithm, binary-heap]
see_also: [levin-campello-algorithm, chow-cioffi-bingham-algorithm, water-filling-power-allocation, snr-gap-approximation, discrete-multitone, priority-queue, exchange-argument, matroid-greedy-algorithm]
sources:
  - url: https://patents.google.com/patent/US4679227A/en
    title: "Dirk Hughes-Hartogs, Ensemble modem structure for imperfect transmission media, US Patent 4,679,227, filed May 20, 1985, issued July 7, 1987"
    locator: "the allocation of data bits and power to the carriers, one increment at a time, to the carrier that needs the least additional power"
  - paper: doi:10.1287/mnsc.13.3.210
    title: "Bennett Fox, Discrete optimization via marginal analysis, Management Science 13(3), 1966, pages 210 to 216"
    locator: "marginal allocation and its optimality for separable problems with convex costs"
  - paper: doi:10.1109/ICC.1999.765384
    title: "Jorge Campello, Practical bit loading for DMT, IEEE International Conference on Communications (ICC), 1999, pages 801 to 805"
    locator: "the greedy loading as a baseline, and the efficiency condition that it satisfies"
---

The Hughes-Hartogs algorithm solves [bit loading](/bit-loading/) by adding bits one at a time. At each step it finds the subcarrier where one more bit costs the least extra power and gives the bit to it. In the margin-adaptive form it stops at the target number of bits $B$; in the rate-adaptive form it stops when the next bit would exceed the power budget $P$. With the cost $e_i(b) = \Gamma(2^b - 1)/g_i$ of the [SNR gap](/snr-gap-approximation/) model, the next bit on a subcarrier always costs twice the last one, the incremental costs increase, and under that condition the greedy result is optimal. It is marginal allocation, which Fox analysed in 1966, applied to a modem. A [binary heap](/binary-heap/) of the next costs makes it run in $O(N + B \log N)$ time.

## In plain words

A modem has many tones and must put a whole number of bits on each. Each extra bit on a tone costs more power than the one before, and weak tones cost more than strong ones.

The method is simple. Look at every tone and ask what one more bit there would cost. Give the bit to the cheapest tone. Repeat until all the bits are placed or the power runs out. Because each tone gets more expensive as it fills, a cheap bit never hides behind an expensive one, so this simple rule finds the best answer.

## The problem

Subcarrier $i$ has the gain $g_i > 0$, its SNR per unit of power. With the gap $\Gamma$, it needs the power $e_i(b) = \Gamma(2^b - 1)/g_i$ for $b$ bits, so bit $b + 1$ costs $\Delta_i(b) = \Gamma 2^{b}/g_i$. Each subcarrier carries at most $b_{\max}$ bits. The margin-adaptive (MA) form finds integers $b_i$ with $\sum_i b_i = B$ that minimize $\sum_i e_i(b_i)$. The rate-adaptive (RA) form maximizes $\sum_i b_i$ subject to $\sum_i e_i(b_i) \le P$. See [bit loading](/bit-loading/) for the full definition.

## The algorithm

For the MA form set $P = \infty$; for the RA form set $B = \infty$.

```pseudo id=main
HUGHES-HARTOGS(g[1..N], Γ, b_max, B, P)
L1  b_i ← 0 for i = 1 .. N, E ← 0, k ← 0       ▷ bits, power, bit count
L2  H ← min-heap of (Γ / g_i, i) for i = 1 .. N  ▷ the cost of each first bit
L3  while H is not empty do
L4      (c, i) ← the minimum of H
L5      if k = B or E + c > P then break         ▷ target reached, or budget full
L6      remove (c, i) from H, b_i ← b_i + 1, E ← E + c, k ← k + 1
L7      if b_i < b_max then insert (Γ · 2^(b_i) / g_i, i) into H
L8  return (b, E)
```

The heap orders its entries by cost and then by index, so ties go to the lowest index. Without a cap, line L7 always inserts. A direct form scans all carriers at each step, which takes $O(N)$ per bit; the heap gives the same choices faster.

## Example

Take $g = (20, 9, 5, 1.5)$, $\Gamma = 1$, no cap, and the MA target $B = 10$. The cost of each step is the heap minimum at line L4.

| step | carrier | cost of the bit | bits after the step | total power |
|---|---|---|---|---|
| 1 | 1 | 1/20 = 0.05 | (1, 0, 0, 0) | 0.0500 |
| 2 | 1 | 1/10 = 0.1 | (2, 0, 0, 0) | 0.1500 |
| 3 | 2 | 1/9 = 0.111 | (2, 1, 0, 0) | 0.2611 |
| 4 | 1 | 1/5 = 0.2 (a tie with carrier 3) | (3, 1, 0, 0) | 0.4611 |
| 5 | 3 | 1/5 = 0.2 | (3, 1, 1, 0) | 0.6611 |
| 6 | 2 | 2/9 = 0.222 | (3, 2, 1, 0) | 0.8833 |
| 7 | 1 | 2/5 = 0.4 (a tie with carrier 3) | (4, 2, 1, 0) | 1.2833 |
| 8 | 3 | 2/5 = 0.4 | (4, 2, 2, 0) | 1.6833 |
| 9 | 2 | 4/9 = 0.444 | (4, 3, 2, 0) | 2.1278 |
| 10 | 4 | 2/3 = 0.667 | (4, 3, 2, 1) | 2.7944 |

At steps 4 and 7, carriers 1 and 3 have the same next cost; the lowest-index rule gives the bit to carrier 1 first, and carrier 3 gets its bit in the next step. The other order gives the same powers. The prefix of 8 steps is the MA answer for $B = 8$, $b = (4, 2, 2, 0)$ with power $101/60$, and a search over every split of 8 bits confirms it. With the RA budget $P = 2$, step 9 would bring the power to 2.1278, so line L5 stops after 8 bits with the same loading.

## Correctness

**Claim.** If the next-bit costs on each subcarrier are positive and nondecreasing, the MA result has the least power among all loadings with $B$ bits, and the RA result has the most bits among all loadings within $P$, with the least power for that number of bits.

**Key steps.** A loading is the same as a choice of a prefix of each list of next-bit costs, and its power is the sum of the chosen costs. Because each list is nondecreasing, the head of each list is its smallest unchosen element, and the heap holds exactly the heads, so each step takes the smallest unchosen cost of all. After $t$ steps the chosen set is the $t$ smallest costs, and no set of $t$ costs has a smaller sum. For the RA form, the least power $E^*(t)$ for $t$ bits is strictly increasing in $t$, so once $E^*(k + 1) > P$ no larger $t$ fits. The full proof is in the proofs folder.

**The condition matters.** For next-bit costs $(4, 1)$ on one subcarrier and $(3, 3)$ on the other and $B = 2$, the rule takes 3 and 3 for a power of 6, while both bits on the first subcarrier cost 5. Tables of measured SNR thresholds can have this shape, for example when a step from one constellation to the next costs less than the step before it.

## Complexity

Line L2 builds the heap in $O(N)$ time. Each pass of the loop does at most two heap operations of $O(\log N)$ each, and there are at most $B + 1$ passes, where $B$ is the number of bits returned. So the time is $O(N + B \log N)$ in the worst case and the extra space is $O(N)$. A direct form that scans all $N$ carriers per bit takes $O(NB)$ time. In the word RAM the bit counts are integers; the costs are real numbers, or exact rationals as in the test code.

## Properties

- **Optimal under increasing increments.** This is the condition of the theorem, and the gap model always satisfies it.
- **Every prefix is optimal.** The first $t$ steps give the MA optimum for $t$ bits, for every $t$. One run therefore gives the whole curve $E^*(t)$ of least power against bits.
- **The gap does not change the MA answer.** Multiplying all costs by $\Gamma$ keeps their order.
- **Water level.** At the end, every loaded bit costs at most the cheapest unloaded bit; the last cost taken plays the part of the water level of [water-filling](/water-filling-power-allocation/).
- **Order free.** The result does not depend on the order of the subcarriers, apart from the choice among ties, and every choice among ties has the same power.

## Variants and improvements

- **[Levin-Campello](/levin-campello-algorithm/).** Starts from any loading, for example rounded water-filling, and moves bits between subcarriers until no move saves power. It reaches the same optimum, often with far fewer steps than $B$.
- **[Chow-Cioffi-Bingham](/chow-cioffi-bingham-algorithm/).** Computes real-valued rates from the SNR and a margin, rounds them, and adjusts the margin; it is faster for large $N$ and $B$ but not exactly optimal.
- **Steps of $\beta$ bits.** For loading in steps of two bits, to keep square QAM, each step adds $\beta$ bits with the cost $e_i(b + \beta) - e_i(b)$; these costs also increase.
- **Removing bits.** To lower the rate, run the rule in reverse and remove the bit that saves the most power.
- **Tables from simulation.** The rule works for any cost tables, but it is optimal only for tables with nondecreasing increments; check this before using it.

## When to use it

Use it when $B$ is small or moderate, when the loading is computed once in a training phase, or as the reference that faster methods are tested against. When the loading must be updated often for a slowly changing channel, a [Levin-Campello](/levin-campello-algorithm/) update from the current loading costs less. For thousands of tones with many bits each, as in VDSL, start from rounded water-filling and repair.

## Pitfalls

- **Costs without increasing increments.** With cost tables from measurements, the greedy rule can be wrong, as the example in Correctness shows.
- **Forgetting the cap.** Real modems cap $b_i$, for example at 15 bits in ADSL. Without the cap the rule can load a very strong tone beyond the largest constellation.
- **Linear and dB values.** The gains and the gap must be linear. A gap of 9.8 dB is $\Gamma \approx 9.55$.
- **Using the sum of all bits in the loop.** Computing $\sum_i b_i$ in every pass instead of keeping a counter turns the time into $O(NB)$.
- **Floating ties.** With floating point costs, two equal costs can compare unequal. This changes the loading but not its optimality, since the powers differ only by rounding.

## Implementations

## History

Dirk Hughes-Hartogs filed the patent "Ensemble modem structure for imperfect transmission media" in May 1985, and it was issued in July 1987 and assigned to Telebit, a maker of high-speed dial-up modems that sent data on many carriers at once. Its loading procedure adds one unit of data at a time to the carrier that needs the least additional power. The same rule had appeared in operations research as marginal allocation, which Fox analysed in 1966 for separable problems with convex costs. In the 1990s the rule became the standard reference for DMT loading in DSL, and its cost for large $B$ motivated the faster methods of Chow, Cioffi and Bingham (1995) and the efficiency and tightness conditions of Campello and Levin.

## References
