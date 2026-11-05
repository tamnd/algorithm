---
tag: 94HZFW
kind: problem
slug: order-preserving-matching
name: Order-preserving pattern matching
aliases:
- order-isomorphic matching
area: strings/exact-matching
level: advanced
summary: Find substrings order-isomorphic to the pattern, comparing relative order of characters.
model: comparison-model
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: O(n + m log m)}
prereqs: [string-matching, knuth-morris-pratt, prefix-function, total-order]
see_also: [permutation-pattern-matching, parameterized-pattern-matching, cartesian-tree, suffix-tree, aho-corasick, coordinate-compression, string-matching]
sources:
  - paper: doi:10.1016/j.ipl.2013.03.015
    title: M. Kubica, T. Kulczyński, J. Radoszewski, W. Rytter and T. Waleń, A linear time algorithm for consecutive permutation pattern matching, Information Processing Letters 113(12) (2013), 430-433
    locator: the main algorithm (a failure-function search that is linear when the pattern can be sorted in linear time)
  - paper: doi:10.1016/j.tcs.2013.10.006
    title: J. Kim, P. Eades, R. Fleischer, S.-H. Hong, C. S. Iliopoulos, K. Park, S. J. Puglisi and T. Tokuyama, Order-preserving matching, Theoretical Computer Science 525 (2014), 68-79
    locator: the prefix representation and the nearest neighbor representation, the O(n log m) and O(n + m log m) single-pattern algorithms, and the O(n log m) multiple-pattern algorithm
  - paper: doi:10.1016/j.tcs.2015.06.050
    title: M. Crochemore, C. S. Iliopoulos, T. Kociumaka, M. Kubica, A. Langiu, S. P. Pissis, J. Radoszewski, W. Rytter and T. Waleń, Order-preserving indexing, Theoretical Computer Science 638 (2016), 122-135
    locator: the introduction (summary of the linear-time matching results) and the order-preserving suffix tree
  - paper: doi:10.1007/978-3-319-07959-2_26
    title: T. Chhabra and J. Tarhio, Order-preserving matching with filtration, Experimental Algorithms (SEA 2014), Lecture Notes in Computer Science, 307-314
    locator: the filtration method (search a binary rise and fall encoding with an exact matcher, then verify)
---

Order-preserving pattern matching asks for every window of a numeric text $T$ of length $n$ whose characters are in the same relative order as those of a pattern $P$ of length $m$, so that the pattern describes a shape, such as "rise, fall a little, rise above the first peak", and not exact values. It was introduced in 2013 by Kubica, Kulczyński, Radoszewski, Rytter and Waleń, and independently by Kim et al., motivated by stock prices and melodies. A variant of [Knuth-Morris-Pratt](/knuth-morris-pratt/) that compares each new character against two earlier ones solves it in $O(n + m \log m)$ time over a general ordered alphabet, and in $O(n + m)$ time when the pattern can be sorted in linear time.

## In plain words

Suppose you want to find a price pattern in a stock chart: up, then down a little, then up to a new high. The actual prices do not matter, only which day was higher than which. So 10, 30, 20, 40 and 5, 9, 7, 12 have the same shape, even though no number is shared.

The task is to slide a window as long as the pattern across the text and report every window with the same shape. Two windows have the same shape when, for every two positions, the one that is smaller in the pattern is also smaller in the window, and equal stays equal.

Checking each window from scratch is slow. The fast method checks a new character only against two earlier ones: the closest smaller one and the closest larger one in the pattern. If it fits between those two, it fits everywhere.

## Definition

**Alphabet.** A general ordered alphabet: characters can only be compared with $<$, $=$ and $>$. The $O(n + m)$ bound needs an integer alphabet of size polynomial in $m$, so that the pattern can be sorted in linear time by [radix sort](/radix-sort/).

**Order isomorphism.** Two strings $u$ and $v$ of the same length $k$ are *order-isomorphic*, written $u \approx v$, when for all $0 \le i, j < k$, $u[i] < u[j]$ exactly when $v[i] < v[j]$. Applying this with $i$ and $j$ swapped shows that equality is preserved as well, so ties in the pattern must be ties in the window. Order isomorphism is an equivalence relation, and it is kept by taking factors at the same positions: if $u \approx v$ then $u[i \ldots j] \approx v[i \ldots j]$.

**Input.** A text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$. Indices are 0-based.

**Output.** The set $\{\, i : 0 \le i \le n - m,\ T[i \ldots i+m-1] \approx P \,\}$, in increasing order. Occurrences may overlap. As on the other pages of this area, if $m = 0$ every position $0, \ldots, n$ is reported, and if $m > n$ nothing is.

**Relation to exact matching.** Every exact occurrence is an order-preserving one, but not conversely. Over an alphabet of size 1, all strings of the same length are order-isomorphic, so every window matches.

## Variants

- **Distinct characters.** Kubica et al. state the problem for permutations: the pattern is a permutation of $\{1, \ldots, m\}$, and the windows of the text are compared by their relative order. This is *consecutive permutation pattern matching*, the case of [permutation pattern matching](/permutation-pattern-matching/) where the chosen text positions must be contiguous. Allowing ties, as on this page, changes the algorithm only in how equal neighbors are tested.
- **Multiple patterns.** Find the windows order-isomorphic to any pattern of a set, in the manner of [Aho-Corasick](/aho-corasick/). Kim et al. give an $O(n \log m)$ algorithm, with $m$ the total length of the patterns.
- **Indexing.** Preprocess the text so that queries take time proportional to the pattern; Crochemore et al. build an order-preserving [suffix tree](/suffix-tree/).
- **Approximate.** Allow up to $k$ mismatches, for example by asking that the window and $P$ become order-isomorphic after deleting the same $k$ positions from both.
- **Cartesian tree matching.** A weaker notion of shape: the window and the pattern must have the same [Cartesian tree](/cartesian-tree/). Every order-preserving occurrence is a Cartesian tree occurrence.
- **Parameterized matching.** A different relaxation of equality, in which symbols may be renamed by a bijection with no order condition; see [parameterized pattern matching](/parameterized-pattern-matching/).

## Examples

Take $P$ = (10, 30, 20, 40) and $T$ = (5, 9, 7, 12, 3, 8, 6, 9, 1, 4, 2, 5), with $n = 12$ and $m = 4$. The pattern's shape is: the second value is the largest so far, the third lies between the first two, the fourth is the largest of all.

| position $i$ | window | order-isomorphic to $P$ |
|---|---|---|
| 0 | 5, 9, 7, 12 | yes |
| 1 | 9, 7, 12, 3 | no (falls first) |
| 2 | 7, 12, 3, 8 | no (3 is below 7) |
| 4 | 3, 8, 6, 9 | yes |
| 8 | 1, 4, 2, 5 | yes |

The output is $\{0, 4, 8\}$, although no value of $P$ occurs in $T$.

More cases: $P$ = (1, 2) in $T$ = (1, 2, 3, 4, 5) gives 0, 1, 2, 3, overlapping; $P$ = (5, 5) in $T$ = (2, 2, 2, 1) gives 0 and 1, but not 2, because 2 and 1 are not equal; $P$ = (2, 1, 2) in $T$ = (3, 1, 2, 1, 3) gives nothing, because the ties of $P$ are never ties of a window.

## Known algorithms

| method | alphabet | time | extra space |
|---|---|---|---|
| check each window by sorting | general ordered | $O(nm \log m)$ | $O(m)$ |
| prefix representation (Kim et al.) | general ordered | $O(n \log m)$ | $O(m)$ |
| nearest neighbors and a failure function (Kubica et al., Kim et al.) | general ordered | $O(n + m \log m)$ | $O(m)$ |
| the same, sorting the pattern by radix sort | integer, polynomial in $m$ | $O(n + m)$ | $O(m)$ |
| filtration on a rise and fall encoding (Chhabra and Tarhio) | general ordered | fast in practice; $O(nm)$ worst case with linear-time verification | $O(m)$ |

**Nearest neighbors.** For each $q$ with $0 \le q < m$, let $a[q]$ be an index $j < q$ with the largest $P[j] \le P[q]$, and $b[q]$ an index $j < q$ with the smallest $P[j] \ge P[q]$, or none. Suppose a window $x$ of length $q + 1$ has $x[0 \ldots q-1] \approx P[0 \ldots q-1]$. Then $x \approx P[0 \ldots q]$ exactly when $x[a[q]]$ relates to $x[q]$ as $P[a[q]]$ relates to $P[q]$ (smaller or equal), and $x[b[q]]$ relates to $x[q]$ as $P[b[q]]$ relates to $P[q]$ (larger or equal). If $P[q]$ equals one of its neighbors, $x[q]$ must equal the matching character, which already has the right order against everything; otherwise nothing in the prefix lies strictly between the two neighbors, so fitting between them fixes every other comparison. This is two comparisons per step. When $P[q]$ has an equal earlier character, it is enough that one of the two neighbors is such a character. The arrays come from a balanced search tree over the prefix, or from sorting the pairs $(P[j], j)$ and deleting them from a doubly linked list in decreasing order of $j$.

**Failure function.** Because $u \approx v$ implies the same for factors at the same positions, the [prefix function](/prefix-function/) carries over: $f[q]$ is the length of the longest proper prefix of $P[0 \ldots q]$ that is order-isomorphic to its suffix of the same length. With the two-comparison extension test, the KMP loops compute $f$ in $O(m)$ steps and scan the text in $O(n)$ steps, by the same amortized argument as for KMP. For $P$ = (10, 30, 20, 40), the arrays are $a$ = (none, 0, 0, 1), $b$ = (none, none, 1, none) and $f$ = (0, 1, 1, 2); for example $f[3] = 2$ because (10, 30) and (20, 40) both rise. In the text above, after the window 5, 9, 7 the next value 12 is tested only against $T[0 + a[3]] = 9$, and $9 < 12$ as $30 < 40$, so the match extends to length 4.

**Filtration.** Chhabra and Tarhio encode each string by whether each step rises or not, search the encoded text for the encoded pattern with any fast exact matcher, and check each candidate window; equal encodings are necessary for order isomorphism but not sufficient.

## Bounds

**Upper bound.** $O(n + m \log m)$ comparisons over a general ordered alphabet, and $O(n + m)$ time when sorting the pattern takes linear time.

**Lower bound.** $\Omega(n + m)$, by an adversary as in the [string matching lower bound](/string-matching-lower-bound/). Take $P$ = (0, 1) and the text $0^n$, which has no occurrence. If an algorithm never reads $T[j]$ for some $j \ge 1$, setting $T[j] = 1$ creates the occurrence $j - 1$ without changing what the algorithm sees, so it must read at least $n - 1$ text characters; it must also read the pattern. Whether the $m \log m$ term is needed over a general ordered alphabet is not settled on this page.

**Output size.** Up to $n - m + 1$ positions, as for $P$ = (1, 2) on an increasing text.

## Reductions

- **To exact matching on an encoding, with verification.** Any map $e$ with $u \approx v \Rightarrow e(u) = e(v)$ for windows, such as the rise and fall encoding, turns order-preserving matching into a filter for exact matching.
- **Not to exact matching on a fixed encoding.** The natural encodings of a window, such as the rank of each character within it, change when the window slides, so the text cannot be encoded once. The nearest neighbor representation avoids this by encoding the pattern only and comparing text characters directly.
- **From exact matching.** Over the alphabet {0, 1}, a window is order-isomorphic to $0^{m-1}1$ exactly when it equals it, so this special case is exact matching.
- **From consecutive permutation matching.** The case of a permutation pattern and a text of distinct values.

## Applications

- Searching time series, such as stock prices, for a trend that matters by its shape, the motivation in Kim et al.
- Searching melodies by their contour, so that a tune transposed to another key still matches.
- Finding repeated shapes in time series with the order-preserving suffix tree, as in Crochemore et al.

## References
