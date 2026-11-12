---
tag: R1T161
kind: data-structure
slug: histogram
name: Histogram (database statistics)
aliases:
- equi-depth histogram
- equi-width histogram
- V-optimal histogram
- end-biased histogram
- equi-height histogram
area: systems/database-algorithms
level: core
summary: "A few buckets that summarize the value distribution of a column. The optimizer reads them to estimate the selectivity of equality and range predicates."
model: word-ram
complexity:
  vars: {N: the number of tuples, n: the number of distinct values, B: the number of buckets}
  time: {worst: "O(n^2 B)"}
  space: {extra: "O(n B)"}
prereqs: [selectivity]
see_also: [cardinality-estimation, selectivity, query-optimization, exponential-histogram, count-min-sketch, matrix-chain-multiplication]
sources:
  - paper: "Gregory Piatetsky-Shapiro and Charles Connell, Accurate estimation of the number of tuples satisfying a condition, Proceedings of ACM SIGMOD 1984, 256 to 276"
    title: Accurate estimation of the number of tuples satisfying a condition
    locator: the equi-depth (equal height) histogram and its error compared with the equal-width histogram
  - paper: doi:10.1145/223784.223841
    title: Yannis E. Ioannidis and Viswanath Poosala, Balancing histogram optimality and practicality for query result size estimation, Proceedings of ACM SIGMOD 1995, 233 to 244
    locator: the definitions of V-optimal and end-biased histograms and the comparison of their errors
  - url: https://www.vldb.org/conf/1998/p275.pdf
    title: H. V. Jagadish, Nick Koudas, S. Muthukrishnan, Viswanath Poosala, Ken Sevcik and Torsten Suel, Optimal histograms with quality guarantees, Proceedings of VLDB 1998, 275 to 286
    locator: the dynamic program for the V-optimal histogram with contiguous buckets in O(n^2 B) time
  - paper: doi:10.1145/233269.233342
    title: Viswanath Poosala, Yannis E. Ioannidis, Peter J. Haas and Eugene J. Shekita, Improved histograms for selectivity estimation of range predicates, Proceedings of ACM SIGMOD 1996, 294 to 305
    locator: the taxonomy of histograms (partition rule, sort parameter, source parameter) and the MaxDiff and compressed histograms
  - url: https://www.vldb.org/conf/2003/papers/S02P01.pdf
    title: Yannis Ioannidis, The history of histograms (abridged), Proceedings of VLDB 2003, 19 to 30
    locator: the history of histograms in databases, from the first use in query optimization to the optimal histograms
---

A histogram in a database is a small summary of the values of one column: the value range is cut into $B$ buckets, and each bucket stores how many tuples fall in it and how many distinct values it has. The [query optimizer](/query-optimization/) reads it to estimate the [selectivity](/selectivity/) of predicates such as `A = 7` or `A BETWEEN 10 AND 20`, assuming that the values inside a bucket are spread evenly. The main kinds differ in where they put the bucket boundaries: equal widths (equi-width), equal numbers of tuples (equi-depth), the least squared error of the frequencies (V-optimal, built by dynamic programming in $O(n^2 B)$ time), or separate buckets for the most extreme frequencies (end-biased).

## In plain words

A table can have millions of rows, and the optimizer has no time to read them while it plans a query. So the database keeps a small picture of each important column. It splits the values into a few groups, for example the values 1 to 100, 101 to 200, and so on. For each group it writes down only how many rows have a value in that group.

To guess how many rows have a value between 150 and 250, the optimizer takes half of the second group and half of the third group. The guess is good when the values inside each group are spread evenly. So a good histogram puts its group boundaries where the data changes, and gives a frequent value a group of its own.

## The abstract type

A histogram answers estimates about one column $A$ of a relation $R$. Let $N = |R|$, let $v_1 < v_2 < \cdots < v_n$ be the distinct values of $A$, and let $f_i$ be the number of tuples with $A = v_i$ (the *frequency* of $v_i$).

- `build(R.A, B)`: make a histogram with at most $B$ buckets.
- `estimate_eq(c)`: an estimate of $|\sigma_{A = c}(R)|$.
- `estimate_range(a, b)`: an estimate of $|\sigma_{a \le A \le b}(R)|$.

The estimates are not exact; a histogram trades space for error. Divide an estimate by $N$ to get a selectivity.

## Representation

A list of buckets $(lo_k, hi_k, c_k, d_k)$ for $k = 1, \ldots, B$: the bucket covers the values from $lo_k$ to $hi_k$, holds $c_k$ tuples, and has $d_k$ distinct values. The invariant:

- $lo_k \le hi_k$ and $hi_k \le lo_{k+1}$ (sorted; neighbors may share an end value only in an equi-depth histogram, where a very frequent value can be split between two buckets);
- each tuple belongs to exactly one bucket whose range contains its value, so $\sum_k c_k = N$.

The estimates use two assumptions inside a bucket. *Uniform frequency*: each of the $d_k$ distinct values has $c_k/d_k$ tuples. *Uniform spread* (for ranges over integers): the $c_k$ tuples are spread evenly over the $hi_k - lo_k + 1$ integers of the range.

$$\text{estimate\_eq}(c) = \sum_{k :\, lo_k \le c \le hi_k} \frac{c_k}{d_k}, \qquad \text{estimate\_range}(a, b) = \sum_k c_k \cdot \frac{|[a, b] \cap [lo_k, hi_k]|}{hi_k - lo_k + 1},$$

where $|[x, y]|$ counts the integers from $x$ to $y$. The kinds of histogram:

- **Equi-width.** The domain $[v_1, v_n]$ is cut into $B$ ranges of equal width $\lceil (v_n - v_1 + 1)/B \rceil$.
- **Equi-depth** (equal height). Sort the $N$ values and cut the sorted list into groups of $d = \lceil N/B \rceil$ consecutive tuples. Each bucket holds $d$ tuples (the last one at most $d$).
- **V-optimal.** The buckets are contiguous runs of distinct values, chosen to minimize the total squared error of the frequencies, $\sum_k \sum_{i \in \text{bucket } k} (f_i - \bar f_k)^2$, where $\bar f_k$ is the mean frequency of bucket $k$. This is the error of `estimate_eq` summed over squares.
- **End-biased.** The $h$ highest and the $l$ lowest frequencies, with $h + l = B - 1$, are stored exactly in singleton buckets, and all other values share one bucket with their mean frequency. The split $(h, l)$ is the one with the least squared error in the shared bucket.

## Operations

**V-optimal build.** Input: the frequencies $f_1, \ldots, f_n$ in value order, and $B \le n$. $E[j][b]$ is the least error of a split of $f_1, \ldots, f_j$ into $b$ buckets, and $\mathrm{SSE}(i, j)$ is the squared error of one bucket that holds $f_{i+1}, \ldots, f_j$.

```pseudo id=main
V-OPTIMAL(f[1..n], B)
L1  P[j] ← f[1] + … + f[j];  Q[j] ← f[1]² + … + f[j]²     ▷ prefix sums, P[0] = Q[0] = 0
    ▷ SSE(i, j) = Q[j] − Q[i] − (P[j] − P[i])² / (j − i)
L2  E[0][0] ← 0;  E[j][0] ← ∞ for j ≥ 1
L3  for b ← 1 to B do
L4      for j ← b to n do
L5          for i ← b − 1 to j − 1 do                    ▷ the last bucket is f[i+1 .. j]
L6              c ← E[i][b − 1] + SSE(i, j)
L7              if c < E[j][b] then remember c and i
L8          E[j][b] ← the least c;  T[j][b] ← its i
L9  j ← n;  for b ← B down to 1 do: the bucket f[T[j][b]+1 .. j];  j ← T[j][b]
L10 return E[n][B] and the B buckets
```

Line L1 makes each SSE an $O(1)$ computation: the squared error of a group is $\sum f_i^2 - (\sum f_i)^2 / m$ for a group of $m$ values. The loops of L3 to L5 fill a table of $n \times B$ cells, each in $O(n)$ time. Line L9 follows the stored choices back from the full problem. The cost is $O(n^2 B)$ time and $O(n B)$ space. Allowing *at most* $B$ buckets gives the same optimum, because splitting a bucket never raises the error.

**Equi-depth build.** Sort the values in $O(N \log N)$ time and cut every $d = \lceil N/B \rceil$ positions. One pass over a sorted index or a sample gives the same in $O(N)$.

```pseudo id=estimate
ESTIMATE-RANGE(H, a, b)
E1  s ← 0
E2  for each bucket (lo, hi, c, d) of H do
E3      x ← max(a, lo);  y ← min(b, hi)
E4      if x ≤ y then s ← s + c · (y − x + 1) / (hi − lo + 1)
E5  return s
```

The scan costs $O(B)$; a binary search on the boundaries finds the two partial buckets in $O(\log B)$ time if the prefix sums of the counts are stored.

## Example

The column has the values 1 to 8 with frequencies $f = (5, 6, 4, 20, 3, 4, 5, 6)$, so $N = 53$ and $n = 8$. Take $B = 3$.

| kind | buckets $[lo, hi]$: count | estimate for $A = 4$ (true 20) | estimate for $4 \le A \le 5$ (true 23) | squared error of the frequencies |
|---|---|---|---|---|
| equi-width | [1, 3]: 15, [4, 6]: 27, [7, 8]: 11 | 9 | 18 | 369/2 |
| equi-depth, $d = 18$ | [1, 4]: 18, [4, 5]: 18, [5, 8]: 17 | 18/4 + 18/2 = 13.5 | 26.75 | |
| V-optimal | [1, 3]: 15, [4, 4]: 20, [5, 8]: 18 | 20 | 24.5 | 7 |

The V-optimal histogram gives the frequent value 4 a bucket of its own. The equi-depth histogram splits the 20 tuples of value 4 between two buckets (3 in the first, 17 in the second), so value 4 sits at a shared end. The end-biased histogram with $B = 3$ keeps $f(4) = 20$ and $f(5) = 3$ exactly and gives the other six values the mean frequency $30/6 = 5$, with squared error 4.

The DP table $E[j][b]$ of the V-optimal build:

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $b = 1$ | 0 | 1/2 | 2 | 683/4 | 986/5 | 208 | 1480/7 | 1695/8 |
| $b = 2$ | | 0 | 1/2 | 2 | 293/2 | 685/4 | 691/4 | 703/4 |
| $b = 3$ | | | 0 | 1/2 | 2 | 5/2 | 4 | 7 |

The answer is $E[8][3] = 7$ with $T[8][3] = 4$: the last bucket holds the values 5 to 8. Then $T[4][2] = 3$ gives the bucket of value 4 alone, and the first bucket is values 1 to 3. The errors are 2, 0 and 5, with the sum 7.

## Correctness

The V-optimal build is correct by optimal substructure: in an optimal split of $f_1 \ldots f_j$ into $b$ buckets, the last bucket is $f_{i+1} \ldots f_j$ for some $i$, the error is a sum over buckets, and the first $b - 1$ buckets must be an optimal split of $f_1 \ldots f_i$. So $E[j][b] = \min_{b-1 \le i < j} (E[i][b-1] + \mathrm{SSE}(i, j))$, which is line L6, by induction on $b$.

For the equi-depth histogram, the error of a range estimate is at most $2 \lceil N/B \rceil$ tuples, for every range: a bucket inside the range or outside it contributes its exact count, and at most two buckets meet the range only in part, each with an error of at most its count. The proofs are in the proof file.

## Complexity

| operation | time | space |
|---|---|---|
| equi-width build | $O(N + B)$ | $O(B)$ |
| equi-depth build | $O(N \log N)$ (sort), $O(N)$ from sorted input | $O(B)$ |
| V-optimal build | $O(n^2 B)$ after counting the frequencies | $O(n B)$ |
| end-biased build | $O(n \log n)$ (sort the frequencies; try the $B$ splits with prefix sums) | $O(n)$ |
| estimate_eq, estimate_range | $O(B)$, or $O(\log B)$ with binary search | $O(1)$ |

The stored histogram has $O(B)$ words, independent of $N$. In practice $B$ is a few hundred buckets per column, and the statistics are rebuilt from a sample, not after each update, so they can be stale.

## Variants

- **MaxDiff and compressed histograms.** Poosala, Ioannidis, Haas and Shekita (1996) classified histograms by the partition rule and by what is sorted and summed. MaxDiff puts boundaries at the $B - 1$ largest differences between neighboring values of the source parameter; compressed histograms keep the most frequent values in singleton buckets and use equi-depth buckets for the rest. They found MaxDiff and compressed histograms good for range predicates in their experiments.
- **Serial histograms.** Ioannidis and Poosala (1995) studied V-optimal histograms in which each bucket groups values by frequency (any set of values whose frequencies are adjacent in sorted order), not by contiguous value ranges. End-biased histograms are the special case with at most one bucket of more than one value. The contiguous V-optimal histogram above suits range predicates, because a range is a contiguous set of values.
- **Most common values.** Many systems keep a list of the most frequent values with their exact frequencies, plus an equi-depth histogram of the rest. This is close to an end-biased or compressed histogram.
- **Approximate V-optimal.** The $O(n^2 B)$ DP is slow for large $n$. Jagadish et al. (1998) also give faster approximations with guarantees on the error.
- **Multidimensional histograms** cut the space of two or more columns into boxes and capture correlation, which a set of one-column histograms cannot (see the [selectivity](/selectivity/) page for the independence assumption).
- **A different histogram.** The [exponential histogram](/exponential-histogram/) of streaming algorithms is not a summary of a value distribution: it counts the 1s in a sliding window of a stream with buckets whose sizes are powers of 2. It shares only the name.

## When to use it

Use an equi-depth histogram as the default for range predicates: its error bound depends only on $N/B$, not on the skew of the data, and it is cheap to build from a sorted sample. Add a list of the most common values, or use an end-biased histogram, when equality predicates on skewed columns matter, because a frequent value then gets its exact count. Use a V-optimal histogram when the number of distinct values is moderate and you can afford the DP at build time; it gives the least squared error of frequency estimates among histograms with contiguous buckets. Equi-width is simple and supports cheap updates, but one dense bucket can hold most of the data. For join sizes and for counts of distinct values, sketches such as the [count-min sketch](/count-min-sketch/) or samples are often better than histograms; see [cardinality estimation](/cardinality-estimation/).

## Pitfalls

- **Off-by-one in the range fraction.** For integer values, the fraction of a bucket $[lo, hi]$ inside $[a, b]$ is $(y - x + 1)/(hi - lo + 1)$, as in line E4, not $(y - x)/(hi - lo)$, which gives 0 for a point range and divides by 0 for a one-value bucket.
- **A frequent value split between buckets.** In an equi-depth histogram, a value with more than $N/B$ tuples spans two or more buckets, so `estimate_eq` must add the parts from all buckets whose range contains the value. Taking only one bucket gives 4.5 instead of 13.5 for value 4 in the example.
- **Wrong error in the DP.** The squared error of a bucket is $\sum f_i^2 - (\sum f_i)^2/m$. Using the variance (divided by $m$) instead of the sum of squares in line L6 weights small buckets wrongly and gives a different, non-optimal split.
- **Stale statistics.** A histogram built before a bulk load says nothing about the new values. Estimates for values beyond the last bucket are 0, and a plan built for a tiny result can be disastrous. Refresh after large changes.
- **Independence between columns.** One histogram per column says nothing about the correlation between columns; multiplying their selectivities is the independence assumption.

## Implementations

## History

Ioannidis (2003) traces the use of histograms for selectivity estimation in databases to the PhD thesis of Kooi (1980). Piatetsky-Shapiro and Connell (1984) proposed equal-height buckets and compared their error with equal-width buckets. Ioannidis and Poosala (1995) defined V-optimal and end-biased histograms and showed that end-biased histograms are a practical compromise between optimality and the cost of building them. Poosala, Ioannidis, Haas and Shekita (1996) gave the taxonomy and the MaxDiff and compressed histograms. Jagadish, Koudas, Muthukrishnan, Poosala, Sevcik and Suel (1998) gave the $O(n^2 B)$ dynamic program for V-optimal histograms with contiguous buckets.

## References
