---
tag: GWVFXD
kind: theorem
slug: interpolation-search-expected-time
name: Interpolation search expected time
aliases:
- Perl-Itai-Avni bound
area: searching/sequential-and-binary-search
level: advanced
summary: For independent uniform keys, interpolation search uses O(log log n) expected probes.
prereqs: [interpolation-search, binomial-distribution, jensens-inequality, order-statistic]
see_also: [interpolation-search, binary-search, sorted-search-lower-bound, search-lower-bound, chebyshev-inequality, linearity-of-expectation, learned-index, uniform-distribution]
sources:
  - paper: doi:10.1145/359545.359557
    title: Yehoshua Perl, Alon Itai and Haim Avni, Interpolation search, a log log N search, Communications of the ACM 21(7) (1978)
    locator: pp. 550 to 553 (the expected number of accesses of plain interpolation search is log log N plus a constant)
  - paper: doi:10.1109/SFCS.1976.32
    title: Andrew C. Yao and F. Frances Yao, The complexity of searching an ordered random table, 17th Symposium on Foundations of Computer Science (1976)
    locator: pp. 173 to 177 (the upper bound and the matching lower bound for every search algorithm)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table (interpolation search and its analysis)
---

The expected time theorem of [interpolation search](/interpolation-search/) says that on $n$ keys drawn independently from the [uniform distribution](/uniform-distribution/), a search that places its probes by interpolation finds a key with $O(\log \log n)$ probes on average, against $\lg n$ for [binary search](/binary-search/). For the plain method, Yao and Yao (1976) and Perl, Itai and Avni (1978) proved the sharp form $\lg \lg n + O(1)$. This page proves the bound in full for a variant with jumps in the style of Perl and Reingold, where the proof is short: one interpolation probe, then jumps of $\sqrt{s}$ in a range of $s$ items, leave a range of fewer than $\sqrt{s}$ items after $O(1)$ expected probes. The bound needs the randomness of the keys: in the worst case the plain method takes $n$ probes.

## Statement

**The model.** The keys $U_1, \ldots, U_n$ are independent and uniform on $[0, 1]$. They are stored sorted, as $A[1] < A[2] < \cdots < A[n]$; with probability 1 they are distinct. Put $A[0] = 0$ and $A[n+1] = 1$. The search key $x$ is a fixed number in $[0, 1]$, or a random number independent of the keys. The task is to find the rank $r = |\{\, i : A[i] < x \,\}|$, which also answers whether $x$ is a key. A probe reads one item $A[i]$ and compares it with $x$; arithmetic on read values is free.

**The algorithm.** The search keeps two indices $lo < hi$ with $A[lo] < x \le A[hi]$ (at the start, $lo = 0$ and $hi = n + 1$), so that $lo \le r \le hi - 1$. Let $s = hi - lo - 1$ be the number of items strictly inside.

- If $s \le 2$, probe the inside items from the left until one is at least $x$.
- Otherwise let $d = \lfloor \sqrt{s} \rfloor$ and $q = (x - A[lo])/(A[hi] - A[lo])$. Probe $p = \min(\max(lo + \lceil s q \rceil, lo + 1), hi - 1)$. If $A[p] < x$, probe $p + d, p + 2d, \ldots$ until an item is at least $x$, or the next position is at least $hi$. If $A[p] \ge x$, probe $p - d, p - 2d, \ldots$ the same way to the left. The last two positions, or one of them and the old end, are the new $lo$ and $hi$.

**Theorem.** For $n \ge 3$, the expected number of probes is at most $3\lceil \lg \log_3 n \rceil + 2$. So the expected cost is $O(\log \log n)$.

For the plain method of the page [interpolation search](/interpolation-search/), with a new interpolation at each probe, the expected number of probes is $\lg \lg n + O(1)$ (Yao and Yao; Perl, Itai and Avni). That proof is longer and is not repeated here.

## In plain words

Draw a million random numbers and sort them. If you look for a number $x$, its place in the list is close to a million times $x$, because random numbers are spread evenly. The guess is not exact: it is off by about a thousand places, the square root of a million.

So you guess once, then step by a thousand places from the guess until you pass $x$. On average you take only one or two steps. Now $x$ is inside a stretch of a thousand items, and the same thing happens again: you guess, you are off by about thirty, and you step by thirty. Then you are inside about thirty items, then five. Each round takes the square root of the size, so a million goes to a thousand, to thirty, to five, in a few rounds.

## Proof

**Lemma 1 (the inside stays uniform).** Consider the search at the start of a round, with indices $lo < hi$. Given everything the search has read so far, the $s$ inside items $A[lo + 1], \ldots, A[hi - 1]$ have the law of $s$ independent uniform values on $(A[lo], A[hi])$, sorted.

*Proof.* The sorted keys $(A[1], \ldots, A[n])$ have the density $n!$ on the set $\{0 < a_1 < \cdots < a_n < 1\}$, which is constant. Each probe position is a function of the values read before it, so the event that the search has read the positions $i_1 < \cdots < i_m$ with given values depends only on those coordinates. Given this event, the density of the other coordinates is therefore constant on the set where the whole vector is increasing. That set is a product over the gaps between consecutive read positions: in the gap between the read positions $i < j$, the coordinates must increase from $A[i]$ to $A[j]$. A constant density on a product of such sets makes the gaps independent, and makes each gap the sorted sample of independent uniform values on its interval. The current $lo$ and $hi$ are read positions (or the ends $0$ and $n + 1$) with no read position between them, so the claim follows. $\square$

**Lemma 2 (one round).** In a round with $s \ge 3$ inside items, the expected number of probes, given the history, is at most 3, and the round ends with fewer than $\sqrt{s}$ inside items.

*Proof.* Let $K$ be the number of inside items less than $x$, so $r = lo + K$. By Lemma 1, each inside item is less than $x$ with probability $q$, independently, so $K$ has the [binomial distribution](/binomial-distribution/) with parameters $s$ and $q$, mean $sq$ and variance $sq(1 - q) \le s/4$.

First the size. The new range is bounded by two positions at distance at most $d$, or by one of them and the old end at a smaller distance. So it has at most $d - 1 < \sqrt{s}$ inside items.

Now the probes. There is the probe at $p$, and then the jumps. Suppose $A[p] < x$, so $p - lo \le K$. The $m$-th jump, at $p + md$, is made only if the item at $p + (m - 1)d$ was less than $x$, that is, $p + (m - 1)d \le lo + K$. So the number of jumps $J$ satisfies $J - 1 \le (K - (p - lo))/d$. Since $p - lo \ge sq$ (the ceiling and the lower clamp only make it larger, and the upper clamp is not active, because $\lceil sq \rceil \le s$), $J \le (K - sq)/d + 1$. Suppose $A[p] \ge x$, so $K \le p - lo - 1$. The $m$-th jump, at $p - md$, is made only if the item at $p - (m - 1)d$ was at least $x$, that is, $p - (m - 1)d \ge lo + K + 1$. So $J - 1 \le (p - lo - 1 - K)/d$. Here $p - lo - 1 \le sq$: without the clamp, $p - lo = \lceil sq \rceil < sq + 1$, and with the lower clamp, $p - lo = 1 \le sq + 1$. So $J \le (sq - K)/d + 1$. In both cases

$$ J \le \frac{|K - sq|}{d} + 1. $$

By [Jensen's inequality](/jensens-inequality/), $\mathbb{E}|K - sq| \le \sqrt{\mathbb{E}(K - sq)^2} = \sqrt{sq(1 - q)} \le \sqrt{s}/2$. So $\mathbb{E}[J] \le \sqrt{s}/(2d) + 1$. For $s \ge 4$, $d > \sqrt{s} - 1 \ge \sqrt{s}/2$, and for $s = 3$, $d = 1$ and $\sqrt{3} < 2$; in both cases $\sqrt{s}/d < 2$ and $\mathbb{E}[J] < 2$. With the probe at $p$, the expected number of probes of the round is less than 3. $\square$

**The number of rounds.** Let $s_0 = n$ and let $s_t$ be the number of inside items after $t$ rounds. By Lemma 2, $s_{t+1} < \sqrt{s_t}$ while $s_t \ge 3$, so $s_t < n^{1/2^t}$ for $t \ge 1$. This bound does not depend on the keys. If $2^t \ge \log_3 n$, then $n^{1/2^t} \le 3$ and $s_t \le 2$. So for $n \ge 3$ there are at most $R = \lceil \lg \log_3 n \rceil$ rounds with $s \ge 3$, and then at most 2 probes in the final scan.

**The total.** Let $P_t$ be the number of probes of round $t$, zero if there is no such round. By Lemma 2, $\mathbb{E}[P_t \mid \text{history}] \le 3$, so $\mathbb{E}[P_t] \le 3$. By [linearity of expectation](/linearity-of-expectation/), the expected total is at most $3R + 2 = 3\lceil \lg \log_3 n \rceil + 2$. When $x$ is random and independent of the keys, the bound holds for each value of $x$, and so also on average. $\blacksquare$

## Consequences

- **Interpolation beats comparison search on random data.** The lower bound $\lceil \lg(n+1) \rceil$ of the [sorted search lower bound](/sorted-search-lower-bound/) holds for comparisons only. Arithmetic on the key values, together with a random input, brings the expected cost down to $O(\log \log n)$.
- **The numbers are small.** For $n = 10^6$ the theorem gives at most $3 \cdot 4 + 2 = 14$ expected probes; a simulation of the variant gives about 7.7, and the plain method about 4.3. Binary search needs 20.
- **Guarded searches.** A search can mix interpolation rounds with binary search, and keep the $O(\log \log n)$ expected cost on uniform keys while the worst case is $O(\log n)$.
- **Other smooth distributions.** If the keys have a known continuous distribution function $F$, interpolating on $F(x)$ maps the problem to the uniform case, and the same proof applies. This is the idea behind a [learned index](/learned-index/), which fits $F$ to the data.

## Tightness

- **The $\log \log n$ order is best possible.** Yao and Yao proved that every search algorithm, with any probes and any arithmetic, needs $\lg \lg n - O(1)$ expected probes on independent uniform keys. So the plain interpolation search is optimal up to an additive constant.
- **The constant of this proof is not sharp.** The variant with jumps pays up to 3 probes per round, and the plain method, with its new interpolation at each probe, gets $\lg \lg n + O(1)$.
- **Randomness is needed.** For fixed inputs the plain method can take $n$ probes, as on $[0, 1, \ldots, n-2, 10^9]$. The variant with jumps can take about $\sqrt{n}$ jumps in its first round.
- **Uniformity is needed.** On keys with a heavy-tailed or clustered distribution the interpolation guesses can be far off in every round, and the expected cost can grow much faster than $\log \log n$.

## History

Peterson proposed interpolation search in 1957. Yao and Yao proved the $\lg \lg n + O(1)$ upper bound and the matching lower bound in 1976 with a hard combinatorial argument. Perl, Itai and Avni gave a simpler proof of the upper bound in 1978, and Perl and Reingold in 1977 gave the variant with $\sqrt{s}$ jumps and its short proof, which is the one above.

## References
