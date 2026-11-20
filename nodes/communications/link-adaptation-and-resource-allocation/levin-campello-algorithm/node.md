---
tag: XEKW7B
kind: algorithm
slug: levin-campello-algorithm
name: Levin-Campello algorithm
aliases:
- Campello bit loading
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Optimal integer bit loading from any start: move bits from the costliest loaded position to the cheapest free one until the loading is efficient, then add or remove bits to meet the target."
solves: [bit-loading]
model: word-ram
complexity:
  vars: {N: the number of subcarriers, M: the number of bit moves (swaps plus additions and removals)}
  time: {worst: O(N + M log(N + M))}
  space: {extra: O(N + M)}
properties: {deterministic: true, optimal: true, greedy: true, incremental: true, needs_csit: true}
history:
  year: 1999
  people: [Jorge Campello, Howard E. Levin]
  note: "Campello stated the efficiency and tightness conditions for discrete loading and an algorithm that reaches them (ISIT 1998, ICC 1999); Levin gave a complete and optimal allocation method for practical DMT systems in 2001."
prereqs: [bit-loading, hughes-hartogs-algorithm]
see_also: [hughes-hartogs-algorithm, chow-cioffi-bingham-algorithm, water-filling-power-allocation, snr-gap-approximation, discrete-multitone, binary-heap, exchange-argument, local-search]
sources:
  - paper: doi:10.1109/ICC.1999.765384
    title: "Jorge Campello, Practical bit loading for DMT, IEEE International Conference on Communications (ICC), 1999, pages 801 to 805"
    locator: "the efficiency (EF) condition, the E-tight and B-tight conditions, and the procedure that moves a start loading to an optimal one"
  - paper: doi:10.1109/GLOCOM.2001.965141
    title: "Howard E. Levin, A complete and optimal data allocation method for practical discrete multitone systems, IEEE Global Telecommunications Conference (GLOBECOM), 2001, pages 369 to 374"
    locator: "an optimal discrete allocation method for DMT that starts from any allocation"
  - paper: doi:10.1287/mnsc.13.3.210
    title: "Bennett Fox, Discrete optimization via marginal analysis, Management Science 13(3), 1966, pages 210 to 216"
    locator: "marginal allocation for separable convex costs, the optimality theory behind both greedy and exchange forms"
---

The Levin-Campello algorithm solves [bit loading](/bit-loading/) exactly, starting from any integer loading. A loading is *efficient* when no loaded bit costs more power than the cheapest bit that could still be added. The algorithm first makes the start efficient by moving bits: while the most expensive loaded bit costs more than the cheapest free bit, it moves that bit. Then it *tightens* the loading: in the margin-adaptive form it removes the most expensive bits or adds the cheapest ones until the total is the target $B$; in the rate-adaptive form it does the same until the power fits the budget $P$ and the next bit does not. With the costs of the [SNR gap](/snr-gap-approximation/) model, the result is optimal. It finds the same optimum as the [Hughes-Hartogs](/hughes-hartogs-algorithm/) greedy rule, but it moves only the bits that are wrong, so a good start, such as rounded [water-filling](/water-filling-power-allocation/) or the loading in use before a small change of the channel, makes it fast.

## In plain words

A modem has a table that says how many bits each tone carries. The table may be a rough guess, or it may be last minute's table and the line has changed a little.

To fix it, look for the most expensive bit now in the table and the cheapest bit that could be added. If moving that bit saves power, move it, and repeat. When no move saves power, the table is the best one for its number of bits. Then add the cheapest bits or remove the most expensive ones until the number of bits or the power matches what is needed. Only the bits that are in the wrong place get moved, so a good guess is fixed quickly.

## The problem

Subcarrier $i$ has the gain $g_i > 0$, and with the gap $\Gamma$ bit $k$ on it costs $d_i(k) = \Gamma 2^{k-1}/g_i$, so $b$ bits cost $e_i(b) = \Gamma(2^{b} - 1)/g_i$. Each subcarrier carries at most $b_{\max}$ bits. For a loading $b$, the *last cost* of subcarrier $i$ is $d_i(b_i)$ (if $b_i > 0$) and its *next cost* is $d_i(b_i + 1)$ (if $b_i < b_{\max}$). The margin-adaptive (MA) form asks for $\sum_i b_i = B$ at the least power; the rate-adaptive (RA) form asks for the most bits with power at most $P$. The input also contains a start loading.

Campello's names for the conditions: a loading is *efficient* (EF) if its largest last cost is at most its smallest next cost; it is *B-tight* if it has $B$ bits; it is *E-tight* if its power is at most $P$ and adding the cheapest next bit would exceed $P$.

## The algorithm

```pseudo id=main
LEVIN-CAMPELLO(g[1..N], Γ, b_max, b[1..N], B or P)  ▷ b is any start loading
L1  E ← Σ_i Γ(2^(b_i) - 1)/g_i; build a max-heap of last costs and a min-heap of next costs
L2  while the largest last cost (at m) > the smallest next cost (at n) do  ▷ make it efficient
L3      b_m ← b_m - 1, b_n ← b_n + 1, update E and both heaps
L4  while Σ_i b_i > B (MA) or E > P (RA) do              ▷ tighten from above
L5      remove the bit with the largest last cost, update E and both heaps
L6  while Σ_i b_i < B (MA) or E + the smallest next cost ≤ P (RA) do  ▷ tighten from below
L7      add the bit with the smallest next cost, update E and both heaps
L8  return (b, E)
```

The heaps break ties by the subcarrier index: the largest (cost, index) leaves and the smallest (cost, index) enters. The heaps use lazy deletion: each change pushes the new entries of one subcarrier, and old entries are dropped when they reach the top.

## Example

Take $g = (20, 9, 5, 1.5)$, $\Gamma = 1$, the MA target $B = 8$, and the flat start $b = (2, 2, 2, 2)$ with power $3.0833$.

| pass | last costs | next costs | move | bits after | power after |
|---|---|---|---|---|---|
| 1 | 0.1, 0.222, 0.4, 1.333 | 0.2, 0.444, 0.8, 2.667 | carrier 4 to carrier 1 | (3, 2, 2, 1) | 1.9500 |
| 2 | 0.2, 0.222, 0.4, 0.667 | 0.4, 0.444, 0.8, 1.333 | carrier 4 to carrier 1 | (4, 2, 2, 0) | 1.6833 |
| 3 | 0.4, 0.222, 0.4, none | 0.8, 0.444, 0.8, 0.667 | stop: 0.4 is at most 0.444 | (4, 2, 2, 0) | 1.6833 |

After two swaps the loading is efficient. It already has 8 bits, so it is B-tight, and the power $101/60 \approx 1.6833$ is the optimum that the greedy method also finds. The distance from the start to the optimum is $|2 - 4| + 0 + 0 + |2 - 0| = 4$, and each swap closed 2 of it.

For the RA form with $P = 2$, start from the rounded-down water-filling rates $(3, 2, 1, 0)$, with power $0.8833$. This start is already efficient (largest last cost $0.222$, smallest next cost $0.4$). Line L7 adds a bit to carrier 1 for $0.4$, then one to carrier 3 for $0.4$, reaching $1.6833$; the next bit would cost $0.444$ and exceed 2, so the result is again $(4, 2, 2, 0)$.

## Correctness

**Claim.** From any start, the MA form returns a loading with $B$ bits and the least power, and the RA form returns the most bits within $P$ at the least power for that number of bits, provided the next-bit costs on each subcarrier increase.

**Key steps.** Because each list of costs increases, the largest loaded cost is the largest last cost and the cheapest free cost is the smallest next cost. So an efficient loading has every loaded cost at most every free cost, and its loaded costs are the $t$ smallest of all, which is the least power $E^*(t)$ for $t$ bits. A swap keeps the bit count and lowers the power strictly, so the swap phase stops, and it stops exactly when the loading is efficient. Removing the most expensive bit or adding the cheapest one keeps a loading efficient, so the tightening phases walk along $E^*(t)$ to the target $B$ or to the largest $t$ with $E^*(t) \le P$. With the tie rule above, each swap removes one element that is not in the optimal set and adds one that is, so the number of swaps is at most half the distance $\sum_i |b_i - b_i^*|$ from the start to the optimum. The full proof is in the proofs folder.

## Complexity

Line L1 takes $O(N)$ time. Each move of one bit at lines L3, L5 or L7 takes a constant number of heap operations. With lazy deletion the heaps hold at most $N + 2M$ entries for $M$ moves, so each operation costs $O(\log(N + M))$, and the time is $O(N + M \log(N + M))$ with $O(N + M)$ extra space; indexed heaps with a decrease-key operation bring the space to $O(N)$ and each step to $O(\log N)$. The number of moves is at most half the distance to the optimum plus the change in the bit count. From the all-zero start, the algorithm is the Hughes-Hartogs rule and $M = B$. From rounded-down water-filling, the RA form adds fewer than $N$ bits, because the integer optimum is less than $N$ bits above the rounded rates.

## Properties

- **Optimal from any start.** The result does not depend on the start, apart from the choice among equal-power answers.
- **Incremental.** A small change of the channel changes the optimal loading a little, and the algorithm moves only the bits that change. This makes it fit for tracking a slowly changing DSL line.
- **Efficient is the same as optimal.** For increasing costs, a loading is MA-optimal for its own number of bits if and only if it is efficient. This gives a cheap test of any loading.
- **Monotone power.** The power never rises in the swap phase.
- **Integer arithmetic.** With the costs scaled by a common factor, all tests are comparisons of powers of two times fixed numbers per subcarrier, and the bit counts are small integers.

## Variants and improvements

- **Steps of $\beta$ bits.** Move $\beta$ bits at a time, with costs $e_i(b + \beta) - e_i(b)$, for constellations of even size only.
- **Margin-adaptive with a fixed power.** To maximize a common margin for a fixed $B$ and $P$, run the MA form and scale the power to $P$; the margin is $P/E^*(B)$.
- **Bit swapping in DSL.** DSL modems change the bits and gains of a few tones during operation, without a restart. The swap step of this algorithm is the natural rule for choosing the tones.
- **[Chow-Cioffi-Bingham](/chow-cioffi-bingham-algorithm/).** A faster method with real-valued rates and a margin; its result can serve as the start here.
- **Table costs.** Any cost table with increasing increments works. Without that condition, efficient loadings need not be optimal.

## When to use it

Use it when a good start is available: after a small change of the channel, after rounding water-filling, or after a fast heuristic such as Chow-Cioffi-Bingham. For a single loading from nothing, the [Hughes-Hartogs](/hughes-hartogs-algorithm/) rule is simpler and as fast. Both need costs whose increments increase.

## Pitfalls

- **Swapping within one subcarrier.** With increasing costs the largest last cost and the smallest next cost are never on the same subcarrier; an implementation that finds them on the same one has a bug in its heaps.
- **Stale heap entries.** With lazy deletion, an entry must be checked against the current bit count of its subcarrier before use.
- **Ties and stopping.** The swap test must be a strict inequality. With $\ge$, equal costs swap forever.
- **Order of the phases.** In the RA form, tightening before the swap phase can stop with too few bits, because the swaps lower the power afterwards and leave room for more. Swap first, then tighten.
- **Floating point.** Repeated additions and subtractions of the power drift; recompute it from the bits at the end if exact values matter.

## Implementations

## History

Jorge Campello studied optimal discrete loading for multicarrier systems in "Optimal discrete bit loading for multicarrier modulation systems" at ISIT 1998, and in "Practical bit loading for DMT" at ICC 1999. He defined efficient and tight loadings and gave an algorithm that starts from any loading and reaches one that is both, which is optimal. Howard Levin, in "A complete and optimal data allocation method for practical discrete multitone systems" at GLOBECOM 2001, gave an optimal allocation method for practical DMT systems. The joined name, Levin-Campello, is used in DSL texts for this family of algorithms. The optimality theory is the same as that of marginal allocation in Fox's 1966 paper.

## References
