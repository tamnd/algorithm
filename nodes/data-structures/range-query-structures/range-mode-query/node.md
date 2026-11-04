---
tag: E4EMFJ
kind: problem
slug: range-mode-query
name: Range mode query
aliases:
- range majority query
area: data-structures/range-query-structures
level: advanced
summary: Return the most frequent value in a subarray.
prereqs: [range-query-problem, square-root-decomposition]
see_also: [mo-algorithm, majority-problem, boolean-matrix-multiplication, matrix-multiplication-exponent, cell-probe-model, range-distinct-count-query, range-kth-smallest-query, word-ram]
sources:
  - paper: "Danny Krizanc, Pat Morin and Michiel Smid, Range mode and range median queries on lists and trees, Nordic Journal of Computing 12(1) (2005), 1-17"
    locator: the space-time trade-off for static range mode queries on arrays
  - paper: "Timothy M. Chan, Stephane Durocher, Kasper Green Larsen, Jason Morrison and Bryan T. Wilkinson, Linear-Space Data Structures for Range Mode Query in Arrays, Theory of Computing Systems 55(4) (2014)"
    locator: the O(sqrt n) linear-space structure with position lists, the O(sqrt(n/w)) structure, and the reduction from boolean matrix multiplication
  - paper: "Mark Greve, Allan Gronlund Jorgensen, Kasper Dalgaard Larsen and Jakob Truelsen, Cell probe lower bounds and approximations for range mode, ICALP 2010, Lecture Notes in Computer Science 6198"
    locator: the cell-probe lower bound for range mode and the approximate range mode structures
---

The range mode query asks for a most frequent value among $A[l], \ldots, A[r]$, for many ranges of one array. Unlike sums or minimums, the mode is not decomposable: the mode of a union can differ from the modes of both parts, so the tree methods of the [range query problem](/range-query-problem/) do not apply. The best known static structures with linear space take about $\sqrt n$ time per query, by [square-root decomposition](/square-root-decomposition/) with position lists, and a reduction from [boolean matrix multiplication](/boolean-matrix-multiplication/) suggests that much faster methods are hard to find. The range majority query, which asks for a value that fills more than half of the range, is much easier.

## In plain words

You have a long list of votes, songs played, or words of a text. A question names a stretch of the list and asks which item occurs most often in that stretch.

For the total or the smallest item of a stretch, you can split the stretch in two and combine two answers. That does not work here. The most common item of the left half and the most common item of the right half can both lose to a third item that is common in both halves. So the fast methods cut the list into blocks, store the most common item of every run of whole blocks, and then check only the few items of the loose ends, each one by a quick look in a list of the places where it occurs.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of values. Then queries $(l, r)$ with $0 \le l \le r \le n - 1$.

**Output.** For each query, a value $x$ that maximizes the frequency

$$f_x(l, r) = |\{ i \in [l, r] : A[i] = x \}|,$$

together with this frequency. Any value of maximum frequency is a correct answer.

**Not decomposable.** For $L = [1, 1, 1, 2, 2]$ and $R = [3, 3, 3, 2, 2]$, the modes are 1 and 3, each with the frequency 3. In the concatenation, the value 2 has the frequency 4 and the values 1 and 3 have 3. So the mode of a range is not a function of the modes of two parts, and no record of $O(1)$ values per part gives it.

**Value range.** After [coordinate compression](/coordinate-compression/) the values are $0, \ldots, \sigma - 1$ with $\sigma \le n$, and a table of counts replaces a hash map.

## Variants

- **Range majority.** Return the value with $f_x(l, r) > (r - l + 1)/2$, if one exists. The candidates of the [Boyer-Moore vote](/majority-problem/) merge as a monoid: a segment tree combines them in $O(\log n)$, and a binary search in the sorted list of the positions of the candidate checks it.
- **Range $\alpha$-majority.** Return all values with frequency more than $\alpha (r - l + 1)$, for a fixed $0 < \alpha < 1$; there are fewer than $1/\alpha$ of them.
- **Approximate mode.** Return a value whose frequency is at least $f^\ast / (1 + \varepsilon)$, where $f^\ast$ is the frequency of the mode. Greve and coauthors gave fast structures for this version.
- **Range minority or least frequent value.** Return a value that occurs in the range with the least frequency.
- **Dynamic.** Point updates between queries; the square-root methods adapt with a larger cost per update.
- **Offline.** All queries are known first. [Mo's algorithm](/mo-algorithm/) keeps counts and a count of counts, and answers each query after $O(n / \sqrt q)$ window moves on average, in $O(n \sqrt q)$ total time.

## Examples

Let $A = [3, 1, 3, 2, 1, 1, 2, 1, 3]$, with $n = 9$.

| query $(l, r)$ | the range | frequencies | mode |
|---|---|---|---|
| $(0, 3)$ | 3, 1, 3, 2 | 3: 2, 1: 1, 2: 1 | 3, twice |
| $(0, 8)$ | the whole array | 1: 4, 3: 3, 2: 2 | 1, four times |
| $(1, 7)$ | 1, 3, 2, 1, 1, 2, 1 | 1: 4, 2: 2, 3: 1 | 1, four times |
| $(2, 6)$ | 3, 2, 1, 1, 2 | 1: 2, 2: 2, 3: 1 | 1 or 2, twice |

**The block method on $(1, 7)$.** Take blocks of size $s = 3$: $[3, 1, 3]$, $[2, 1, 1]$ and $[2, 1, 3]$. The table of block spans says that the mode of block 1 alone is 1 with the frequency 2. The position lists are $P_1 = [1, 4, 5, 7]$, $P_2 = [3, 6]$ and $P_3 = [0, 2, 8]$, and each index $i$ stores its place $\mathrm{pos}[i]$ in the list of $A[i]$.

1. Start with the candidate 1 and $f = 2$.
2. Scan the left end, the indices 1 and 2. Index 1 holds the value 1 with $\mathrm{pos}[1] = 0$. The item $P_1[0 + f] = P_1[2] = 5$ is at most $r = 7$, so the value 1 occurs at least 3 times in $[1, 7]$: set $f = 3$. Then $P_1[3] = 7 \le 7$, so $f = 4$, and $P_1[4]$ does not exist. Index 2 holds 3 with $\mathrm{pos}[2] = 1$, and $P_3[1 + 4]$ does not exist.
3. Scan the right end, the indices 7 and 6, with the mirror test $P_x[\mathrm{pos}[i] - f] \ge l$. Index 7 has $\mathrm{pos}[7] = 3 < f$, and index 6 has $\mathrm{pos}[6] = 1 < f$, so neither can reach the frequency 5.
4. The answer is the value 1 with the frequency 4.

## Known algorithms

| method | preprocessing | query | space |
|---|---|---|---|
| scan with a table of counts | none | $O(r - l + 1)$ | $O(\sigma)$ |
| table of all answers | $O(n^2)$ | $O(1)$ | $\Theta(n^2)$ words |
| Krizanc, Morin and Smid | | $O(n^\varepsilon \log n)$ | $O(n^{2 - 2\varepsilon})$ words, $0 < \varepsilon \le 1/2$ |
| blocks and position lists (Chan and coauthors) | $O(n \sqrt n)$ | $O(\sqrt n)$ | $O(n)$ words |
| Chan and coauthors, with word operations | $O(n \sqrt n)$ | $O(\sqrt{n / w})$ | $O(n)$ words |
| [Mo's algorithm](/mo-algorithm/), offline | sort the queries | $O(n \sqrt q + q)$ in total | $O(n + q)$ |

Here $w = \Omega(\log n)$ is the word size of the [word RAM](/word-ram/).

**The block method.** With blocks of size $s$, store the mode and its frequency for each of the $(n/s)^2$ spans of whole blocks. A query takes the mode of its span of full blocks as the first candidate, with its frequency $f$. Every other candidate occurs in one of the two partial ends, which hold at most $2s$ items. Scan each item $A[i]$ of the left end: while $P_{A[i]}[\mathrm{pos}[i] + f]$ exists and is at most $r$, the value $A[i]$ occurs more than $f$ times in $[i, r] \subseteq [l, r]$, so it becomes the candidate and $f$ grows by one. The right end is the mirror image. The frequency $f$ never exceeds the true frequency of the mode, and it grows at most $2s$ times above the first value, because the true frequency of the mode is at most the span frequency plus $2s$. So a query costs $O(s)$, and $s = \sqrt n$ gives $O(\sqrt n)$ time with $O(n)$ space.

## Bounds

**Cell-probe lower bound.** Greve, Jorgensen, Larsen and Truelsen proved that a static structure that uses $S$ cells of $w$ bits needs $\Omega(\log n / \log(S w / n))$ probes per query in the [cell-probe model](/cell-probe-model/). With $S = n \log^{O(1)} n$ cells this is $\Omega(\log n / \log \log n)$. This bound is far below the known upper bounds near $\sqrt n$.

**Conditional lower bound.** Chan and coauthors reduced the product of two boolean $\sqrt n \times \sqrt n$ matrices to $n$ range mode queries on an array of length $O(n)$. So an offline algorithm for $n$ range mode queries in time $o(n^{\omega/2})$, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/), would multiply boolean matrices faster than the known methods. In particular, a combinatorial method with $O(n^{3/2 - \varepsilon})$ total time would give a combinatorial boolean matrix product in $O(m^{3 - 2\varepsilon})$ time for $m \times m$ matrices.

**Upper bound.** $O(\sqrt{n / w})$ query time with $O(n)$ space. Whether this gap to the cell-probe bound can be closed is open.

## Reductions

- **Boolean matrix multiplication to range mode.** By the reduction of Chan and coauthors above.
- **Element distinctness to range mode.** The mode of $A[0 \ldots n-1]$ has the frequency 1 exactly when all items are distinct; see [element distinctness](/element-distinctness/). So preprocessing and one query need $\Omega(n \log n)$ steps in the [algebraic decision tree](/algebraic-decision-tree/) model.
- **Range majority to range mode.** A majority, when it exists, is the unique mode. The reverse does not hold, and range majority is much easier.

## Applications

- The most common item of a window of a log, a sales record or a text, such as the most frequent word of a passage.
- Data mining and statistics on time series, where the mode summarizes categorical data.
- Majority and heavy-hitter queries on ranges of a database, through the majority and $\alpha$-majority variants.

## References
