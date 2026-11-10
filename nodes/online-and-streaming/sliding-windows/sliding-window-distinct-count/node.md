---
tag: 1JM0GW
kind: problem
slug: sliding-window-distinct-count
name: Sliding window distinct count
aliases:
- count distinct over a window
- sliding-window cardinality
- distinct elements over a sliding window
- F0 over a sliding window
area: online-and-streaming/sliding-windows
level: advanced
summary: Estimate the number of distinct items among the last W items or the last W time units; exact answers need Omega(W) bits, and a relative error eps needs polylogarithmic space.
prereqs: [distinct-elements-problem, sliding-window-model, epsilon-delta-guarantee]
see_also: [sliding-hyperloglog, smooth-histogram, smooth-function, distinct-elements-problem, hyperloglog, basic-counting, exponential-histogram-bound, kmv-sketch]
sources:
  - paper: doi:10.1145/564870.564880
    title: Phillip B. Gibbons and Srikanta Tirthapura, Distributed streams algorithms for sliding windows, SPAA 2002
    locator: Section 2 (related work on distinct values over windows) and Section 5, Theorem 5 (randomized waves for the number of distinct values)
  - paper: arxiv:1805.00212
    title: Vladimir Braverman, Elena Grigorescu, Harry Lang, David P. Woodruff and Samson Zhou, Nearly optimal distinct elements and heavy hitters on sliding windows, APPROX/RANDOM 2018
    locator: the abstract and the main theorems (the composable histogram, the upper bound and the lower bound for distinct elements)
  - paper: doi:10.1137/090749281
    title: Vladimir Braverman and Rafail Ostrovsky, Effective computations on sliding windows, SIAM Journal on Computing 39(6), 2010
    locator: Definition 1 and Theorems 1 to 3 (smooth functions and smooth histograms)
  - paper: doi:10.1109/ICDMW.2010.18
    title: Yousra Chabchoub and Georges Hébrail, Sliding HyperLogLog, estimating cardinality in a data stream over a sliding window, IEEE ICDM Workshops 2010
    locator: pp. 1297 to 1303
  - paper: doi:10.1137/1.9781611972979.9
    title: Éric Fusy and Frédéric Giroire, Estimating the number of active flows in a data stream over a sliding window, ANALCO 2007
    locator: pp. 223 to 231
---

The sliding window distinct count asks for the number of distinct items among the last $W$ items of a stream, or among the items of the last $W$ time units, at each time. It is the [distinct elements problem](/distinct-elements-problem/) in the [sliding window model](/sliding-window-model/). An exact answer needs memory linear in $W$, so the algorithms estimate the count with a relative error $\varepsilon$ and a failure probability $\delta$. The known algorithms keep hash-based samples with timestamps ([Sliding HyperLogLog](/sliding-hyperloglog/), randomized waves) or sketches started at chosen times ([smooth histograms](/smooth-histogram/)), and the best ones are optimal up to small factors.

## In plain words

You watch a stream of visitor names and want to know, at any moment, how many different visitors came in the last hour. Keeping every name of the hour is exact but large. A counter for the whole day cannot forget the morning. The tricks for the whole stream use a random hash of each name and remember only rare hash values. For a window, they also remember when each rare value was last seen, so that old ones can be ignored. Another way is to start a fresh small counter now and then and keep only the counters whose answers differ enough.

## Definition

The input is a stream $a_1, a_2, \ldots$ of items from a universe $U$, read one at a time. A window size $W \ge 1$ is fixed. At time $t$, the **window** is $S_t = \{a_i : \max(1, t - W + 1) \le i \le t\}$ for a [count-based window](/count-based-window/), and the answer is $n_t = |S_t|$, the number of distinct items in it.

- **Exact version.** Output $n_t$ at each time.
- **Approximate version.** For given $\varepsilon, \delta \in (0, 1)$, output at each query time an estimate $\hat n_t$ with $\Pr[|\hat n_t - n_t| \le \varepsilon n_t] \ge 1 - \delta$, an [(ε, δ) guarantee](/epsilon-delta-guarantee/).

The cost is the memory in bits, as a function of $W$, $\varepsilon$, $\delta$ and $|U|$, and the time per item and per query.

## Variants

- **Time-based windows.** Each item has a timestamp, and the window holds the items of the last $W$ time units; see [time-based window](/time-based-window/). The number of items in a window is then not bounded by $W$.
- **All window lengths.** A query gives any $w \le W$ and asks for the count over the last $w$ items or time units. Sliding HyperLogLog and randomized waves answer such queries; the basic smooth histogram is built for one $W$.
- **Distributed streams.** Several parties each see a stream, and the count is over the union of their windows. Gibbons and Tirthapura (2002) solve this case; their waves can be merged by a referee.
- **Predicates.** Count the distinct items in the window that satisfy a predicate given only at query time. Gibbons and Tirthapura answer such queries from a sample of the distinct values.
- **Basic counting.** Counting the 1s of a bit stream is a different problem: it counts positions, not values. Its algorithms do not apply directly, because one item can appear many times in a window. See [basic counting](/basic-counting/).

## Examples

Take $W = 5$ and the stream $a, b, a, c, b, b, d, a$.

| $t$ | window | distinct items | $n_t$ |
|---|---|---|---|
| 5 | $a, b, a, c, b$ | $a, b, c$ | 3 |
| 6 | $b, a, c, b, b$ | $a, b, c$ | 3 |
| 7 | $a, c, b, b, d$ | $a, b, c, d$ | 4 |
| 8 | $c, b, b, d, a$ | $a, b, c, d$ | 4 |

At $t = 6$ the item $a$ of time 1 leaves the window, but the count stays 3, because $a$ appears again at time 3. An exact algorithm must know this. It keeps, for each item, the time of its last occurrence: at $t = 8$ these are $a: 8$, $b: 6$, $c: 4$, $d: 7$, and the count is the number of last occurrences in $\{4, \ldots, 8\}$.

## Known algorithms

- **Exact, with a hash map.** Keep the window in a queue and a hash map from each item to the time of its last occurrence, with the count of items whose last occurrence is in the window. When $a_t$ arrives, the count grows by one if $a_t$ has no last occurrence in the window. When the item of time $t - W$ leaves, the count drops by one if that time is its last occurrence. This takes $O(1)$ expected time per item and $O(W)$ words.
- **Timestamped hash sketches.** [Sliding HyperLogLog](/sliding-hyperloglog/) (Chabchoub and Hébrail, 2010) keeps, for each [HyperLogLog](/hyperloglog/) register, a list of (time, rank) pairs, and reads the registers of any window of length $w \le W$ exactly, with a standard error of about $1.04/\sqrt{m}$ for $m$ registers. Sliding MinCount (Fusy and Giroire, 2007) does the same for the smallest hash values. Gibbons and Tirthapura report that the Flajolet and Martin estimate for a constant factor can be adapted to sliding windows, after Datar, Gionis, Indyk and Motwani.
- **Randomized waves.** Gibbons and Tirthapura (2002) hash each value to a level, where level $\ell$ is sampled with probability $2^{-\ell}$, and keep at each level the $O(1/\varepsilon^2)$ values with the most recent last occurrences. A query uses the lowest level whose sample covers the window. Their Theorem 5 gives an $(\varepsilon, \delta)$ scheme with $O(\frac{1}{\varepsilon^2} \log \frac{1}{\delta} \log W \log R)$ bits per party for values in $\{0, \ldots, R\}$, for distributed streams, with expected $O(\log \frac{1}{\delta})$ field operations per item.
- **Histograms of sketches (the DGIM-style approach).** The [exponential histogram](/exponential-histogram/) of DGIM splits the window into buckets and adds their counts, but distinct counts of buckets do not add up: an item can be in two buckets. The [smooth histogram](/smooth-histogram/) of Braverman and Ostrovsky keeps, instead, sketches of whole suffixes of the stream, started at $O(\frac{1}{\varepsilon} \log W)$ chosen times. The distinct count is an $(\varepsilon, \varepsilon)$-[smooth function](/smooth-function/), so instances of an insertion-only sketch such as [HyperLogLog](/hyperloglog/) or [KMV](/kmv-sketch/) give a $(1 \pm O(\varepsilon))$ estimate of the window.
- **Composable histograms.** Braverman, Grigorescu, Lang, Woodruff and Zhou (2018) refine the histogram approach and get a $(1 + \varepsilon)$ approximation in $O(\frac{1}{\varepsilon^2} \log W \log \frac{1}{\varepsilon} \log \log W + \frac{1}{\varepsilon} \log^2 W)$ bits, which is nearly optimal.

## Bounds

- **Exact answers need $\Omega(W)$ bits.** A stream of at most $W$ items is its own window, so each exact algorithm for the window also counts the distinct items of a whole stream of length $W$. The [distinct elements problem](/distinct-elements-problem/) page proves that a deterministic exact count over a universe of size $n$ needs at least $n - \log_2(n + 1)$ bits, with streams of $n/2$ items; with $n = 2W$ this is about $2W$ bits. Randomized exact algorithms also need $\Omega(W)$ bits, by the reduction from set disjointness on the same page.
- **Lower bound for approximation (cited).** Braverman, Grigorescu, Lang, Woodruff and Zhou prove that a $(1 + \varepsilon)$ approximation over a window of $W$ items needs $\Omega(\frac{1}{\varepsilon} \log^2 W + \frac{1}{\varepsilon^2} \log W)$ bits. The term $\frac{1}{\varepsilon} \log^2 W$ is the same as in the [space theorem for basic counting](/exponential-histogram-bound/); the term $\frac{1}{\varepsilon^2} \log W$ is larger than the $\Omega(\frac{1}{\varepsilon^2})$ bound for the whole stream.
- **Upper bound (cited).** Their algorithm uses $O(\frac{1}{\varepsilon^2} \log W \log \frac{1}{\varepsilon} \log \log W + \frac{1}{\varepsilon} \log^2 W)$ bits, so the gap to the lower bound is a factor $O(\log \frac{1}{\varepsilon} \log \log W)$ in the first term.
- **Whole stream against window.** For the whole stream, $O(\frac{1}{\varepsilon^2} + \log |U|)$ bits are enough (Kane, Nelson and Woodruff, on the [distinct elements problem](/distinct-elements-problem/) page). So the window multiplies the term $\frac{1}{\varepsilon^2}$ by a factor of at least about $\log W$.

## Reductions

- **From the distinct elements problem.** As in the first bound above, a stream of length at most $W$ is its own window. So every lower bound for the distinct elements problem on streams of length $W$ holds for the window problem.
- **To insertion-only sketches.** The distinct count is an $(\alpha, \alpha)$-smooth function, so the smooth histogram turns each insertion-only $(1 \pm \beta)$ sketch into a window algorithm with $O(\frac{1}{\beta} \log W)$ copies. The proof for exact instances is on the [smooth histogram](/smooth-histogram/) page; Braverman and Ostrovsky prove the case of approximate and randomized instances.
- **To a maximum over a window.** For one register of HyperLogLog, the window value is the [sliding window maximum](/sliding-window-maximum/) of the ranks sent to it. Sliding HyperLogLog is this reduction with one monotone list per register.

## Applications

- **Network monitoring.** The number of active flows in the last seconds or minutes, which is the problem of Fusy and Giroire and of Chabchoub and Hébrail. A sudden rise can show a worm or a denial of service attack.
- **Web and product analytics.** The number of distinct users in the last hour or day, updated as events arrive.
- **Databases and stream systems.** A `COUNT(DISTINCT x)` over a window clause, where an approximate answer is acceptable.

## References
