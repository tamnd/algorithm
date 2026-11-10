---
tag: G6SM48
kind: problem
slug: moving-average
name: Moving average
aliases:
- rolling average
- running average over a window
- simple moving average
- SMA
area: online-and-streaming/sliding-windows
level: intro
summary: Report the average of the last W items after each item; a running sum gives O(1) time per step, and compensated addition or periodic recomputation stops the floating-point drift.
prereqs: [sliding-window-model, circular-buffer, floating-point-arithmetic]
see_also: [exponential-moving-average, sliding-window-aggregation, kahan-summation, pairwise-summation, count-based-window, exponential-decay, basic-counting]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 4, Summation, Section 4.2 (the error bound of recursive summation) and Section 4.3 (compensated summation and its error bound)
  - paper: doi:10.1145/363707.363723
    title: William Kahan, Further remarks on reducing truncation errors, Communications of the ACM 8(1), 1965
    locator: page 40, compensated summation
  - paper: "Arnold Neumaier, Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen, Zeitschrift für Angewandte Mathematik und Mechanik 54(1), 1974"
    locator: pages 39 to 51, the compensated sum that also handles terms larger than the running sum
  - url: https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc421.htm
    title: NIST/SEMATECH e-Handbook of Statistical Methods
    locator: Section 6.4.2.1, single moving average
---

The moving average problem asks for the mean of the last $W$ items of a stream after each new item. Keeping the window in a [ring buffer](/circular-buffer/) and a running sum that adds the new item and subtracts the leaving one gives $O(1)$ time per step and $O(W)$ memory. In floating-point arithmetic the running sum collects rounding errors from every item ever seen, so long streams need compensated addition or a periodic exact recomputation. For integers the running sum is exact.

## In plain words

To smooth a noisy series, replace each value by the mean of the last few values. Adding up the whole window at every step is wasteful, because consecutive windows share all but two items. So keep a running total: add the new value and subtract the value that just left, then divide by the window size. With whole numbers this is exact. With decimal computer numbers, each addition rounds a little, and the rounding errors never leave the total even when their items do. A large value that passes through the window can wipe out small values for good. Correcting each addition, or rebuilding the total from the stored window now and then, fixes this.

## Definition

The input is a stream $x_1, x_2, \ldots$ of real numbers and a window size $W \ge 1$. After item $t$, with $n = \min(t, W)$, output

$$A_t = \frac{1}{n} \sum_{i = t - n + 1}^{t} x_i.$$

The first $W - 1$ outputs average partial windows. Some uses start the output only at $t = W$; the update below is the same.

The running sum $S_t = \sum_{i = t - n + 1}^{t} x_i$ satisfies

$$S_t = S_{t-1} + x_t - x_{t - W} \quad (t > W), \qquad S_t = S_{t-1} + x_t \quad (t \le W),$$

so $A_t$ costs one addition, one subtraction and one division per step.

## Variants

- **Time-based window.** The mean of the items with timestamps in $(t - T, t]$. The buffer becomes a queue of (timestamp, value) pairs, the running sum and count are updated on each insert and each expiry, and one step can expire many items; the cost stays $O(1)$ amortized per item.
- **Cumulative average.** The mean of all items so far, $A_t = A_{t-1} + (x_t - A_{t-1})/t$, with $O(1)$ memory.
- **Weighted moving average.** The linear weights $W, W - 1, \ldots, 1$, newest first. The numerator $N_t = \sum_{j=0}^{n-1} (W - j)\, x_{t-j}$ has the update $N_t = N_{t-1} + W x_t - S_{t-1}$, because every older item loses one unit of weight, so it also costs $O(1)$ per step.
- **Centered moving average.** For an offline series, average $x_{t-h}, \ldots, x_{t+h}$. A trailing average of a linear trend lags it by $(W - 1)/2$ steps, and the centered form removes this lag at the price of needing future items.
- **Moving variance.** The window variance from the running sums of $x$ and $x^2$ cancels badly in floating point; the triple (count, mean, sum of squared deviations) with its merge formula is safer and is a [sliding-window aggregation](/sliding-window-aggregation/) with an inverse.
- **Exponential weights.** The [exponential moving average](/exponential-moving-average/) keeps $O(1)$ memory and no buffer, and gives a smooth fade instead of a cut at $W$.

## Examples

$W = 3$ and the stream $4, 8, 6, 2, 10, 7$:

| $t$ | $x_t$ | leaving item | $S_t$ | $A_t$ |
|---|---|---|---|---|
| 1 | 4 | | 4 | 4 |
| 2 | 8 | | 12 | 6 |
| 3 | 6 | | 18 | 6 |
| 4 | 2 | 4 | 16 | 16/3 |
| 5 | 10 | 8 | 18 | 6 |
| 6 | 7 | 6 | 19 | 19/3 |

**Drift.** In binary64 arithmetic, take $W = 2$ and the stream $10^{16}, 1, 1, 1, \ldots$. At $t = 2$ the exact sum $10^{16} + 1$ is not representable, because the spacing of doubles near $10^{16}$ is 2, and it rounds to $10^{16}$. At $t = 3$ the update adds 1 to the stored $10^{16}$, which rounds to $10^{16}$ again, and then subtracts the leaving $10^{16}$, which gives 0, while the true window sum is 2. From then on every step adds 1 and subtracts 1, so the plain running sum reports the average 0 forever, while the true average is 1. Neumaier's compensated addition, below, keeps the lost unit in a separate term and reports 1 at every step.

## Known algorithms

The pseudocode keeps the window in a buffer $B$, the running sum $s$, a compensation term $c$, and a recomputation period $R$, such as $R = W$; with $R = \infty$ there is no recomputation.

```pseudo id=main
STEP(x)
L1  t ← t + 1; append x to B
L2  ADD(x)
L3  if t > W then remove the oldest item y from B; ADD(−y)
L4  if R divides t then s ← the correctly rounded sum of B; c ← 0
L5  return (s + c) / size(B)
ADD(y)
L6  u ← s + y
L7  if |s| ≥ |y| then c ← c + ((s − u) + y) else c ← c + ((y − u) + s)
L8  s ← u
```

Lines L6 to L8 are Neumaier's form of compensated summation: $(s - u) + y$ is exactly the rounding error of $u = s + y$ when $|s| \ge |y|$, and the other branch handles a new term larger than the sum, where Kahan's original form can lose part of the error. Line L4 bounds the history: after a recomputation, the error depends only on the items since then.

**Cost.** Lines L1 to L3 and L5 to L8 take $O(1)$ time. Line L4 takes $O(W)$ time once every $R$ steps, so $O(1)$ amortized time per step when $R \ge W$, and $O(W)$ in the worst case for one step. Memory is the $W$ items of the buffer and two numbers.

**Error.** The plain running sum is a recursive summation of the $m = 2t - W$ terms $x_1, \ldots, x_t, -x_1, \ldots, -x_{t-W}$, so by the standard bound (Higham, Section 4.2) its error is at most about $(m - 1)\, u \sum |x_i|$ over all those terms, where $u = 2^{-53}$ for binary64. This grows with $t$, not with $W$, and does not shrink when large items leave. Compensated summation reduces the bound to about $2u \sum |x_i| + O(m u^2) \sum |x_i|$ (Higham, Section 4.3), so the $m$ in front of $u$ disappears, but the sum still runs over the whole history. Recomputation with period $R$ limits the history to the last $R + W$ items. A method that never subtracts, such as the [two-stacks queue](/two-stacks-queue/) with $\otimes = +$, answers each query from sums of at most $W$ window items, so its error depends only on the window, at the cost of about two additions per item.

**Other methods.**

| method | time per item | memory | exact for |
|---|---|---|---|
| recompute each window | $O(W)$ | $W$ | as exact as the summation used |
| running sum, above | $O(1)$ | $W + 2$ | integers, fixed point |
| running sum with wrapping integers | $O(1)$ | $W + 1$ | integers whose window sums fit in a word |
| prefix sums $P_t - P_{t-W}$, offline | $O(1)$ after $O(n)$ setup | $n$ | integers |
| two-stacks queue with $+$ | $O(1)$ amortized | $2W$ | error bounded by the window |

With integers in fixed-width registers, overflow in the middle of the update does no harm: addition modulo $2^{64}$ is a group, so the running sum is exact modulo $2^{64}$, and it equals the true sum whenever the true window sum fits in the signed range. Decimal values such as prices are best stored as integers in the smallest unit for this reason.

## Bounds

**Time.** Every item must be read, so $\Omega(1)$ per item, which the running sum meets.

**Space, proved here.** An exact moving average of integers from $\{0, \ldots, U - 1\}$ needs at least $W \log_2 U$ bits of memory. After any window $x_{t-W+1}, \ldots, x_t$, feed $W$ zeros. The sum drops at step $j$ by exactly the item that leaves, so $W (A_{t+j-1} - A_{t+j}) = x_{t-W+j}$, and the outputs spell out the whole window. So different windows need different memory states, and there are $U^W$ windows. An approximate answer can use much less: the [basic counting](/basic-counting/) problem, the moving sum of bits, needs only $O(\frac{1}{\varepsilon} \log^2 W)$ bits for a relative error $\varepsilon$.

## Reductions

- **To sliding-window aggregation.** The pair (sum, count) under componentwise addition is a group, so the moving average is the invertible case of [sliding-window aggregation](/sliding-window-aggregation/), solved by subtract on evict; the division is the lower step.
- **To prefix sums.** For an offline array, $S_t = P_t - P_{t - W}$ with $P_t = x_1 + \cdots + x_t$.
- **As a filter.** The moving average is the convolution of the series with a box of $W$ weights $1/W$, a finite impulse response low-pass filter. The [exponential moving average](/exponential-moving-average/) is the matching infinite impulse response filter, and [exponential decay](/exponential-decay/) is its version over real time.

## Applications

Smoothing noisy measurements in monitoring dashboards and sensors; the simple moving average of prices in technical analysis, often of 50 or 200 days; frame time and throughput displays in software; trend estimation in time series, where centered moving averages remove seasonal cycles of a known length; and rate limits that count events in the last minute.

## References
