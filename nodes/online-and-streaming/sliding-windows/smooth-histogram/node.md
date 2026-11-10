---
tag: PBPEZG
kind: data-structure
slug: smooth-histogram
name: Smooth histogram
aliases:
- smooth histogram framework
- Braverman-Ostrovsky smooth histogram
area: online-and-streaming/sliding-windows
level: research
summary: Keeps insertion-only instances started at O((1/beta) log W) chosen times and gives a (1 - alpha) approximation of an (alpha, beta)-smooth function over the last W items.
model: word-ram
complexity:
  vars: {W: the window size, b: the smoothness parameter beta, F: the largest value of f on a window, g: the space of one instance, h: the time of one instance update}
  time: {amortized: O((h/b) log F), worst: O((h/b) log F)}
  space: {extra: O((g/b) log F)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2007
  people: [Vladimir Braverman, Rafail Ostrovsky]
  note: Braverman and Ostrovsky introduced smooth histograms at FOCS 2007, and published the full version in SIAM Journal on Computing in 2010.
prereqs: [smooth-function, sliding-window-model, count-based-window, relative-error]
see_also: [smooth-function, exponential-histogram, dgim-algorithm, sliding-window-distinct-count, sliding-hyperloglog, frequency-moment-problem, ams-sketch, hyperloglog]
sources:
  - paper: doi:10.1137/090749281
    title: Vladimir Braverman and Rafail Ostrovsky, Effective computations on sliding windows, SIAM Journal on Computing 39(6), 2010
    locator: Definition 2 (smooth histogram), Theorem 1 (exact instances), Theorem 2 (approximate instances), Theorem 3 (randomized instances) and Lemma 5 (frequency moments)
  - paper: doi:10.1109/FOCS.2007.55
    title: Vladimir Braverman and Rafail Ostrovsky, Smooth histograms for sliding windows, FOCS 2007
    locator: pp. 283 to 293, the first version of the smooth histogram
  - paper: arxiv:1805.00212
    title: Vladimir Braverman, Elena Grigorescu, Harry Lang, David P. Woodruff and Samson Zhou, Nearly optimal distinct elements and heavy hitters on sliding windows, APPROX/RANDOM 2018
    locator: Section 1 (smooth histograms as the base of sliding window algorithms for distinct elements)
---

A smooth histogram turns an insertion-only streaming algorithm for a [smooth function](/smooth-function/) $f$ into an algorithm for the last $W$ items of the stream. It keeps copies of the algorithm started at a few chosen times $x_1 < x_2 < \cdots < x_s$, deletes a copy when its neighbors already have almost the same value, and answers with the copy that starts just inside the window. For an $(\alpha, \beta)$-smooth $f$ with integer values at most $F$ on a window, it keeps $s = O(\frac{1}{\beta} \log F)$ copies and returns a value between $(1 - \alpha) f(\text{window})$ and $f(\text{window})$. Braverman and Ostrovsky introduced it in 2007, in the [sliding window model](/sliding-window-model/) with a [count-based window](/count-based-window/).

## In plain words

You want a total over the last thousand items, but your counter cannot forget items. So you start a new counter at each item. That is too many counters. But many of them say almost the same thing: a counter that started a little later sees almost the same total as its older neighbor. You keep the oldest of such a group and the newest, and delete the counters between them. For good functions, two counters that were close once stay close for ever. When the window moves, you answer with the oldest counter that started inside it. Its older neighbor started outside, and the two are close, so the answer is close to the true value.

## The abstract type

The structure keeps an approximation of $f$ over the last $w$ items. It is created with $W \ge 1$, a parameter $\beta \in (0, 1)$, and a way to create an **instance**: an object that reads items with `update(a)` and returns $f$ of the items it has read with `value()`.

- `update(a)`: append the item $a$ to the stream and advance the time $t$ by 1.
- `query(w)`, with $1 \le w \le W$: return $\hat f$ with $(1 - \alpha) f_w \le \hat f \le f_w$, where $f_w$ is $f$ of the last $\min(w, t)$ items.

The guarantee holds when $f$ is $(\alpha, \beta)$-smooth and the instances are exact. For the sum, the count, the maximum and the number of distinct items, $\alpha = \beta$.

## Representation

The structure keeps a list of start times $x_1 < \cdots < x_s = t$, and for each $x_i$ an instance $\Lambda(x_i)$ that has read the items $a_{x_i}, \ldots, a_t$. Write $f(x, t)$ for $f(a_x, \ldots, a_t)$, the value of $\Lambda(x)$ at time $t$. Since $a_{x_{i+1}}, \ldots, a_t$ is a suffix of $a_{x_i}, \ldots, a_t$, the values do not increase along the list.

After each update the list has three properties:

1. **Coverage.** If $t > W$, then $x_1 \le t - W < x_2$: the first instance started before the window and the second one inside it.
2. **Close neighbors.** For each $i < s$, either $x_{i+1} = x_i + 1$, or $(1 - \alpha) f(x_i, t) \le f(x_{i+1}, t)$.
3. **Decay.** For each $i \le s - 2$, $f(x_{i+2}, t) < (1 - \beta) f(x_i, t)$.

Property 2 gives the accuracy and property 3 gives the size.

## Operations

```pseudo id=main
SH-UPDATE(a)                    ▷ f(x) is the value of the instance Λ(x) that started at time x
L1  t ← t + 1
L2  append x_{s+1} = t to the list, with a new instance Λ(t)
L3  feed a to each instance Λ(x_1), …, Λ(x_s)
L4  i ← 1
L5  while i < s do
L6      j ← the largest index > i with f(x_j) ≥ (1 − β) f(x_i), or i + 1 if there is none
L7      delete x_{i+1}, …, x_{j−1} and their instances; i ← i + 1
L8  if some x_i ≤ t − W then delete all indices before the largest such i

SH-QUERY(w)                     ▷ 1 ≤ w ≤ W
L9  if x_1 > t − w then return f(x_1)
L10 i ← the largest index with x_i ≤ t − w
L11 return f(x_{i+1})
```

Line L7 renumbers the list, so after it $x_{i+1}$ is the old $x_j$. Since the values do not increase along the list, line L6 is a scan forward, and lines L4 to L7 read each value once. Line L9 applies only while $t \le W$: then $x_1 = 1$ and the window of size $w \ge t$ is the whole stream.

## Example

Take the sum, which is $(\beta, \beta)$-smooth, with $W = 4$ and $\beta = 1/2$, and the stream $3, 1, 2, 0, 3, 1, 1, 2$. The list is shown as pairs $(x_i, f(x_i, t))$ after the update.

| $t$ | $a_t$ | list after the update | answer | true sum |
|---|---|---|---|---|
| 1 | 3 | (1, 3) | 3 | 3 |
| 2 | 1 | (1, 4), (2, 1) | 4 | 4 |
| 3 | 2 | (1, 6), (2, 3), (3, 2) | 6 | 6 |
| 4 | 0 | (1, 6), (2, 3), (3, 2), (4, 0) | 6 | 6 |
| 5 | 3 | (1, 9), (3, 5), (5, 3) | 5 | 6 |
| 6 | 1 | (1, 10), (3, 6), (5, 4), (6, 1) | 6 | 6 |
| 7 | 1 | (3, 7), (5, 5), (6, 2), (7, 1) | 5 | 5 |
| 8 | 2 | (3, 9), (5, 7), (6, 4), (8, 2) | 7 | 7 |

At $t = 5$ the values before line L4 are $9, 6, 5, 3, 3$ at the start times $1, \ldots, 5$. For $x_1 = 1$ the threshold is $9/2$, and the largest start time with a value at least $9/2$ is 3, so line L7 deletes 2. For $x = 3$ the threshold is $5/2$, and line L7 deletes 4. The window is the items $2$ to $5$, with sum 6; $x_1 = 1$ is outside and the answer is $f(3, 5) = 5 \ge (1 - \frac{1}{2}) \cdot 6$. At $t = 7$ the start times 1 and 3 are both at most $t - W = 3$, so line L8 deletes 1 and keeps 3.

## Correctness

The full proof is on the [proof page](proofs/correctness.md). In short:

- **Close neighbors.** Two start times become neighbors in two ways. Line L2 appends $t$ next to $t - 1$. Line L7 makes $x_i$ and $x_j$ neighbors at some time $t'$ with $f(x_j, t') \ge (1 - \beta) f(x_i, t')$. In the second case, condition 4 of smoothness, with $A = a_{x_i} \ldots a_{t'}$, $B = a_{x_j} \ldots a_{t'}$ and $C = a_{t'+1} \ldots a_t$, gives $(1 - \alpha) f(x_i, t) \le f(x_j, t)$ at each later time $t$.
- **Accuracy.** For $t > w$, let $x_i \le t - w < x_{i+1}$. The window is a suffix of $a_{x_i} \ldots a_t$, and $a_{x_{i+1}} \ldots a_t$ is a suffix of the window. By monotonicity, $f(x_{i+1}, t) \le f_w \le f(x_i, t)$. If $x_{i+1} = x_i + 1$, then $x_{i+1} = t - w + 1$ and the answer is exact. Otherwise, by property 2, $f(x_{i+1}, t) \ge (1 - \alpha) f(x_i, t) \ge (1 - \alpha) f_w$.
- **Size.** By property 3, $f$ drops by a factor $1 - \beta$ every two indices. With integer values, $s \le 2 \lceil \ln(F + 1)/\beta \rceil + 3$.

## Complexity

The proofs are on the proof page.

- **Instances.** At most $2 \lceil \ln(F + 1)/\beta \rceil + 3 = O(\frac{1}{\beta} \log F)$, where $F$ is the largest value of $f$ on a stream of at most $W$ items. For the sum of integers in $\{0, \ldots, R\}$, $F = WR$; for the distinct count, $F \le W$. With $f$ bounded by a polynomial in $W$, as in the definition of smoothness, this is $O(\frac{1}{\beta} \log W)$.
- **Space.** $O(\frac{1}{\beta} \log F)$ instances of $g$ words each, and their start times. The start time $x_1$ can be far older than the window, but after time $W$ only the fact that it is outside the window is needed. The other start times are inside the window and take $O(\log W)$ bits each modulo $W$.
- **Update time.** $s$ instance updates in line L3 and $O(s)$ value reads in lines L4 to L8, so $O(\frac{h}{\beta} \log F)$ in the worst case, where $h$ is the time of one instance update and one value read.
- **Query time.** $O(\log s)$ by binary search over the start times, plus one value read.

For the sum with exact counters, the space is $O(\frac{1}{\varepsilon} \log^2 W)$ bits for $R \le W$, the same as the [exponential histogram](/exponential-histogram/). The gain of the method is for functions that buckets cannot handle, such as $F_2$.

## Variants

- **Approximate instances (cited).** Braverman and Ostrovsky (Theorem 2) allow instances that only approximate $f$, with a relative error small compared to $\beta$ (they use $\beta/4$), at the cost of a constant factor in the final error. The pruning of line L6 then uses the approximate values.
- **Randomized instances (cited).** For instances that are correct with probability $1 - \delta'$, a [union bound](/union-bound/) over the instances made in a window gives a guarantee of the [(ε, δ) kind](/epsilon-delta-guarantee/) at each query (their Theorem 3). With the [median trick](/median-trick/), $\delta'$ can be made small at a cost of a $\log$ factor.
- **Frequency moments.** $F_p$ with $p \ge 1$ is $(\alpha, (\alpha/p)^p)$-smooth. Instances of the [AMS sketch](/ams-sketch/) for $F_2$ give a window estimate with $O(\frac{1}{\varepsilon^2} \log W)$ sketches; see the [frequency moment problem](/frequency-moment-problem/).
- **Distinct count.** $F_0$ is $(\alpha, \alpha)$-smooth, so instances of [HyperLogLog](/hyperloglog/) or of the [KMV sketch](/kmv-sketch/) give a [sliding window distinct count](/sliding-window-distinct-count/). Braverman, Grigorescu, Lang, Woodruff and Zhou (2018) build a nearly optimal algorithm from this start.
- **Time-based windows.** Line L8 tests timestamps instead of positions, and the bound on $s$ uses the largest value of $f$ over items in one window of time.

## When to use it

Use it when $f$ is smooth, there is a good insertion-only algorithm for $f$, and buckets do not combine: for $F_2$, for the distinct count with a sketch that cannot delete, or for the length of the [longest increasing subsequence](/longest-increasing-subsequence/). For sums and counts, the [exponential histogram](/exponential-histogram/) gives the same space with a simpler structure and two-sided error. For exact answers on a small window, keep the window and use [sliding-window aggregation](/sliding-window-aggregation/).

## Pitfalls

- **Functions that are not smooth.** For the largest frequency $F_\infty$, take the stream $x^k y^k x^k$ with $W = 3k - 1$. At time $2k$ the start times $1$ to $k + 1$ all have the value $k$, so the pruning keeps none of the start times $2$ to $k$. At time $3k$ the answer is $k$ and the true value is $2k - 1$. The pruning is safe only with the guarantee of condition 4.
- **Monotone values.** The scan of line L6 assumes that the values do not increase along the list. With approximate instances this can fail; then compute the largest $j$ by its definition, or force the values to be monotone.
- **The output is low.** The error is one-sided: the answer never exceeds the true value with exact instances. To get a two-sided error of $\alpha/2$, multiply the answer by $1 + \alpha/2$ or so; this changes the constants only.
- **The cost per item.** Each item goes to all $s$ instances. With an instance update time of $h$, the time per item is $\Theta(\frac{h}{\beta} \log W)$, which is large for sketches with many counters.

## Implementations

## History

Braverman and Ostrovsky introduced smooth histograms at FOCS 2007 and gave the full version in SIAM Journal on Computing in 2010. They defined smooth functions, proved that the $L_p$ norms, the frequency moments and the length of the longest increasing subsequence are smooth, and got sliding window algorithms for them with a polylogarithmic overhead over the insertion-only algorithms. The method generalizes the [exponential histogram](/exponential-histogram/) of Datar, Gionis, Indyk and Motwani (2002), which needs weakly additive functions. Later work, for example on distinct elements and heavy hitters by Braverman, Grigorescu, Lang, Woodruff and Zhou (2018), starts from smooth histograms.

## References
