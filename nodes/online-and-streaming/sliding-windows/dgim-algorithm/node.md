---
tag: KD0VWY
kind: algorithm
slug: dgim-algorithm
name: DGIM algorithm
aliases:
- Datar-Gionis-Indyk-Motwani algorithm
- bucket algorithm for basic counting
- DGIM
area: online-and-streaming/sliding-windows
level: advanced
summary: Keeps buckets of 1s with power-of-2 sizes, about k/2 of each size, and answers basic counting over the last W bits with relative error below 1/k in O(k log^2 W) bits.
solves: [basic-counting]
model: word-ram
complexity:
  vars: {W: the window size, k: the accuracy parameter (relative error below 1/k)}
  time: {amortized: O(1), worst: O(log W)}
  space: {extra: O(k log^2 W)}
properties: {online: true, deterministic: true}
history:
  year: 2002
  people: [Mayur Datar, Aristides Gionis, Piotr Indyk, Rajeev Motwani]
  note: Datar, Gionis, Indyk and Motwani presented the algorithm at SODA 2002 and in SIAM Journal on Computing in 2002, with a matching lower bound.
prereqs: [basic-counting, sliding-window-model, count-based-window, relative-error]
see_also: [exponential-histogram, exponential-histogram-bound, smooth-histogram, time-based-window, sliding-window-distinct-count, aggregate-method, approximate-counting-problem, morris-counter]
sources:
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the exponential histogram for basic counting (the bucket invariants, the merge rule, the estimate and the space bound)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 4, Section 4.6, Counting Ones in a Window (the DGIM algorithm, with r or r minus 1 buckets of each size)
  - paper: doi:10.1145/564870.564880
    title: Phillip B. Gibbons and Srikanta Tirthapura, Distributed streams algorithms for sliding windows, SPAA 2002
    locator: pp. 63 to 72, the restatement of the bucket rule and the deterministic wave
---

The DGIM algorithm solves [basic counting](/basic-counting/): it keeps an estimate of the number of 1s among the last $W$ bits of a bit stream, with [relative error](/relative-error/) less than $1/k$, in $O(k \log^2 W)$ bits. It groups the 1s of the window into buckets whose sizes are powers of 2, keeps about $k/2$ buckets of each size, and stores for each bucket only its size and the time of its newest 1. Datar, Gionis, Indyk and Motwani (DGIM) gave it in 2002, together with a lower bound that shows that its space is optimal. It works in the [sliding window model](/sliding-window-model/) with a [count-based window](/count-based-window/); on this page $\sigma = b_1, b_2, \ldots$ is the bit stream, $t$ is the current time, $W$ is the window size, $k \ge 1$ is the accuracy parameter and $L = \lceil k/2 \rceil$. For a target error $\varepsilon$, take $k = \lceil 1/\varepsilon \rceil$.

## In plain words

Exact counting would need to remember every recent bit. Instead, the algorithm puts the ones into groups. The newest ones are in groups of one, older ones in groups of two, older still in groups of four, and so on. It keeps only a few groups of each size, and when there are too many small groups, it joins the two oldest of them into one group of twice the size. For each group it remembers only when its newest one arrived. A group leaves when that time is too old. To answer, it adds up all the groups. Only the oldest group can be partly outside the window, so it counts half of that group. Because the oldest group is small compared with all the groups after it, the answer is close.

## The problem

The input is the window size $W$, the parameter $k$ and a bit stream read one bit at a time. At any time $t$ a query gives $w \in \{1, \ldots, W\}$ and asks for $c = \sum_{i > t - w} b_i$, the number of 1s among the last $w$ bits. The answer $\hat c$ must satisfy $|\hat c - c| < c/k$ whenever $c \ge 1$, and $\hat c = 0$ when $c = 0$. The guarantee is deterministic and holds at every query.

## The algorithm

A **bucket** is a pair (timestamp, size). Its size is a power of 2, and it stands for that many 1s of the stream that are consecutive among the 1s. Its timestamp is the position of the newest of those 1s. The buckets partition the 1s that the structure still counts, and the older buckets hold older 1s. Level $j$ holds the buckets of size $2^j$.

**The bucket rule.** Let $r$ be the largest level present. Each level $j < r$ has $L$ or $L + 1$ buckets, and level $r$ has 1 to $L + 1$ buckets. The sizes do not decrease from the newest bucket to the oldest one.

```pseudo id=main
DGIM-UPDATE(b)                          ▷ L = ⌈k/2⌉; level j holds buckets of size 2^j
L1  t ← t + 1
L2  if the oldest bucket has timestamp ≤ t − W then remove it
L3  if b = 1 then
L4      add the bucket (t, 1) as the newest bucket of level 0
L5      j ← 0
L6      while level j has L + 2 buckets do
L7          remove the two oldest buckets of level j; add a bucket of size 2^(j+1) with the newer of their two timestamps, as the newest bucket of level j + 1
L8          j ← j + 1

DGIM-QUERY(w)                           ▷ 1 ≤ w ≤ W
L9  B ← the buckets with timestamp > t − w; if B is empty then return 0
L10 2^r ← the size of the oldest bucket of B; S ← the sum of the sizes of the other buckets of B
L11 return S + (2^r + 1)/2
```

Line L2 expires at most one bucket, because at most one timestamp is equal to $t - W$. Line L7 joins two buckets that are neighbours in time. The new bucket is older than every bucket left at level $j$ and newer than every bucket at level $j + 1$, so it becomes the newest bucket of level $j + 1$ and the order of sizes stays correct. The new bucket keeps the newer timestamp, because it must stay as long as any of its 1s is in the window. For the full window, $w = W$, line L10 needs only the total of all sizes and the size of the oldest bucket, both of which the structure keeps.

## Example

Take $W = 10$ and $k = 2$, so $L = 1$: each level below the largest has 1 or 2 buckets, and a level that reaches 3 buckets merges. The stream is $1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1$. The buckets are written as (timestamp, size), newest first.

| $t$ | buckets after the update | estimate | true count |
|---|---|---|---|
| 2 | (2, 1), (1, 1) | 2 | 2 |
| 4 | (4, 1), (2, 2) | 5/2 | 3 |
| 6 | (6, 1), (5, 2), (2, 2) | 9/2 | 5 |
| 9 | (9, 1), (8, 2), (5, 4) | 11/2 | 7 |
| 12 | (12, 1), (11, 2), (8, 2), (5, 4) | 15/2 | 7 |

At $t = 4$ level 0 holds (4, 1), (2, 1) and (1, 1), so line L7 joins (2, 1) and (1, 1) into (2, 2). At $t = 9$ the update cascades: level 0 holds (9, 1), (8, 1), (6, 1), and the two oldest become (8, 2); then level 1 holds (8, 2), (5, 2), (2, 2), and the two oldest become (5, 4). The bucket (5, 4) stands for the 1s at positions 1, 2, 4 and 5. At $t = 12$ the window is positions 3 to 12, the 1 at position 1 has left it, and the true count is 7. The estimate is $3 + 1 + 1 + (4+1)/2 = 15/2$, with relative error $1/14$. In 12 steps there were 5 merges, fewer than the 9 ones.

## Correctness

The proof is on the [proof page](proofs/correctness.md). The bucket rule holds after each update, by induction on the updates. For the query, let the oldest bucket of $B$ have size $2^r$ and let $S$ be the sum of the others. All buckets of $B$ except the oldest one lie inside the last $w$ positions, and the oldest one has at least its newest 1 inside. So $S + 1 \le c \le S + 2^r$, and the midpoint of line L11 is off by at most $(2^r - 1)/2$. If $r = 0$ the answer is exact. If $r \ge 1$, the bucket rule puts at least $L$ buckets of each size $2^0, \ldots, 2^{r-1}$ in $B$, so $S \ge L(2^r - 1)$ and
$$\frac{|\hat c - c|}{c} \le \frac{2^r - 1}{2\,(L(2^r - 1) + 1)} < \frac{1}{2L} \le \frac{1}{k}.$$

## Complexity

All bounds here are proved on the proof page. The model is the word RAM with words of $\Theta(\log W)$ bits.

- **Number of buckets.** At most $(L + 1)\left(\left\lfloor \log_2 \left(\frac{W - 1}{L} + 1\right) \right\rfloor + 1\right)$, since the oldest bucket of size $2^r$ needs $L(2^r - 1) + 1 \le W$. For $k = 2$ and $W = 10$ this is 8; for $k = 4$ and $W = 4096$ it is 36.
- **Space.** A timestamp is a position in the window, so it can be kept modulo $W$ in $\lceil \log_2 W \rceil$ bits; the size of a bucket is given by its level. With $t \bmod W$, the total and the counts of the levels, the space is $O(k \log^2 W)$ bits, $O(k \log W)$ words. There are no random bits.
- **Update time.** $O(1)$ amortized: each merge reduces the number of buckets by one, and each 1 creates one bucket, so after $m$ bits there have been fewer merges than 1s. The worst case is $O(\log W)$, a cascade over all the levels.
- **Query time.** $O(1)$ for $w = W$, from the total and the oldest bucket. For $w < W$, $O(k \log W)$ with a scan of the buckets.

## Properties

- **Deterministic.** The error bound holds at every query, for every stream, with no failure probability.
- **One structure for all window lengths.** The same buckets answer each $w \le W$ with the same error bound.
- **No error when the count is small.** When all 1s of the window are in buckets of size 1, the answer is exact.
- **Optimal space.** DGIM prove a lower bound of $\Omega(k \log^2(W/k))$ bits for each algorithm with relative error $1/k$, deterministic or randomized; see [the space theorem](/exponential-histogram-bound/).

## Variants and improvements

- **The general structure.** The [exponential histogram](/exponential-histogram/) uses the same buckets for sums of bounded integers and for other functions that combine like sums.
- **Worst-case $O(1)$ time.** The deterministic waves of Gibbons and Tirthapura (2002) reach the same space with $O(1)$ worst-case time per bit.
- **Time-based windows.** The same algorithm works on a [time-based window](/time-based-window/) if the bits of one time step are inserted one by one; line L2 must then remove all expired buckets, and the number of buckets grows with the logarithm of the largest number of 1s in a window.
- **Larger functions.** The [smooth histogram](/smooth-histogram/) extends the idea to each [smooth function](/smooth-function/), and the [sliding-window distinct count](/sliding-window-distinct-count/) uses related ideas.

## When to use it

Use DGIM when you need the count of events among the last $W$ events, $W$ is large, the memory per counter must be small, and a relative error is acceptable. If $W$ is small (a few thousand), a circular buffer of $W$ bits is simpler and exact. If the window is defined by time and the rate is variable, use the time-based variant. If an additive error $\varepsilon W$ is enough, counts of fixed blocks are simpler.

## Pitfalls

- **The half-bucket estimate.** A common form of the estimate is "all buckets but half the last one", $S + 2^r/2$ (or $S + 1$ when $r = 0$). With only $L = \lceil k/2 \rceil$ buckets per size, it can reach relative error $1/(L + 2)$, which is more than $1/k$ for $k \ge 6$. For example, with $k = 10$ and seven 1s the buckets are five of size 1 and one of size 2, the estimate is 6, the count is 7, and the error is $1/7$; the midpoint gives $13/2$ and the error $1/14$. Use the midpoint $S + (2^r + 1)/2$, or keep more buckets per size. The text of Leskovec, Rajaraman and Ullman keeps $r - 1$ or $r$ buckets of each size and states the weaker bound $1/(r - 1)$ for the half-bucket estimate, which this example does not contradict.
- **The wrong timestamp on a merge.** The merged bucket must keep the timestamp of its newest 1. With the older timestamp it expires while some of its 1s are still in the window, and the answer can drop far below the count.
- **Order of expiry and insertion.** Expire first, then insert, as in lines L2 and L4. Then the expiry test never sees the bucket of the current bit.
- **Unbounded timestamps.** Storing $t$ as an integer that grows forever costs $\log t$ bits per bucket, not $\log W$. Keep positions modulo $W$; the age of a kept bucket is less than $W$ before the expiry test, so the residue is enough.
- **Time-based windows.** With many 1s at one time step, more than one bucket can expire at once, and a single removal in line L2 is not enough.

## Implementations

## History

Datar, Gionis, Indyk and Motwani presented the algorithm at SODA 2002 and in SIAM Journal on Computing in 2002. They called the structure an exponential histogram, applied it to sums and other functions, and proved that its space is optimal for basic counting. In the same year Gibbons and Tirthapura gave waves, which reach the same space with worst-case constant time per bit and extend to distributed streams. The textbook of Leskovec, Rajaraman and Ullman made the algorithm a standard part of courses on data streams, under the name DGIM.

## References
