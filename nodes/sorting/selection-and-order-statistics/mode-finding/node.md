---
tag: N0WY35
kind: problem
slug: mode-finding
name: Finding the mode
area: sorting/selection-and-order-statistics
level: intro
summary: Finds the element that occurs most often in a collection, typically by sorting or hashing and counting runs of equal values.
model: comparison-model
complexity:
  vars: {n: the number of items, m: the number of copies of the mode}
  time: {worst: Θ(n log(n/m))}
prereqs: [sorting-problem, hash-table]
see_also: [element-distinctness, frequency-counter, boyer-moore-majority, space-saving, presorting, counting-sort, element-distinctness-lower-bound, quickselect]
sources:
  - paper: doi:10.1016/0304-3975(80)90057-2
    title: David Dobkin and J. Ian Munro, Determining the mode, Theoretical Computer Science 12(3) (1980)
    locator: pages 255 to 263 (an algorithm with n lg(n/m) + o(n lg(n/m)) comparisons, and a lower bound that it matches up to a lower-order term)
  - paper: doi:10.1137/0205001
    title: J. Ian Munro and Philip M. Spira, Sorting and searching in multisets, SIAM Journal on Computing 5(1) (1976)
    locator: pages 1 to 8 (comparison bounds for sorting multisets and for the mode)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.1, Lower bounds for sorting, and Chapter 11, Hash tables
---

Finding the mode asks for the value that occurs most often among $n$ items, together with its number of copies. Two methods cover most uses: sort the items and scan for the longest run of equal values, in $O(n \log n)$ time, or count the values in a [hash table](/hash-table/), in $O(n)$ expected time. In the [comparison model](/comparison-model/) the problem needs $\Omega(n \log n)$ comparisons in general, because it answers [element distinctness](/element-distinctness/), but a mode with many copies can be found faster: Dobkin and Munro (1980) need about $n \lg(n/m)$ comparisons when the mode has $m$ copies.

## In plain words

You have a long list of votes and you want the name that got the most votes. One way is to put the votes in alphabetical order. Then all votes for one name sit together, and one pass finds the longest block.

Another way is to keep a tally sheet. For each vote you find the name on the sheet, or add it, and make a mark. At the end you look for the name with the most marks. With a good way to find names on the sheet, this takes one pass over the votes.

If you may only compare two votes at a time to see which name comes first, you cannot do much better than sorting, unless the winner has a large share of the votes.

## Definition

**Input.** A sequence $a_1, \ldots, a_n$ of $n \ge 1$ items. Two items are equal or not; in the comparison model they also have a [total order](/total-order/).

**Multiplicity.** For a value $v$, let $c(v) = |\{ i : a_i = v \}|$.

**Output.** A value $v$ of the input with $c(v) = m$, where $m = \max_i c(a_i)$ is the largest multiplicity, together with $m$. Such a $v$ is a **mode**. When several values share the largest multiplicity, any one of them is a correct answer, unless the variant asks for all of them or for a fixed one, such as the smallest.

## Variants

- **All modes.** Report each value with multiplicity $m$. The two methods below give this at no extra cost.
- **Majority.** Decide whether some value has more than $n/2$ copies, and find it. This is easier: the [Boyer-Moore majority vote](/boyer-moore-majority/) does it in $O(n)$ time with $O(1)$ extra space and only equality tests.
- **Streams and heavy hitters.** With small memory, the exact mode cannot be kept, but the values with more than $\varepsilon n$ copies can be found with $O(1/\varepsilon)$ counters, for example by [space saving](/space-saving/) or [lossy counting](/lossy-counting/).
- **Small integer keys.** If the items are integers in $\{0, \ldots, U - 1\}$, an array of $U$ counters, as in [counting sort](/counting-sort/), gives the mode in $O(n + U)$ time.
- **Continuous data.** For samples of a real distribution, almost all values differ, and the statistical mode is the peak of an estimated density, not a multiplicity. That problem is outside this page.

## Examples

**One mode.** For $A = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]$, the sorted order is $1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9$. The runs have lengths $2, 1, 2, 1, 3, 1, 1$, so the mode is $5$ with $m = 3$. The values $1$ and $3$ come next, with two copies each.

**Ties.** For $[2, 7, 2, 7, 4]$, both $2$ and $7$ have two copies, so $m = 2$ and each of them is a mode.

**All distinct.** For $[4, 8, 15, 16, 23, 42]$, each value has one copy, so $m = 1$ and each item is a mode. This case is the one that makes the problem hard in the comparison model.

**No majority.** In the first example $m = 3 \le 11/2$, so there is no majority value, and the majority vote returns a candidate that a second pass rejects.

## Known algorithms

**Sort and scan.** Sort the items, then walk the sorted array and keep the length of the current run of equal items and the longest run so far. The sort costs $O(n \log n)$ time and the scan $O(n)$. This is the standard example of [presorting](/presorting/).

**Hashing.** Insert each item into a hash table that maps a value to its count ([frequency counter](/frequency-counter/)), then take a value with the largest count. With [universal hashing](/universal-hashing/) the expected time is $O(n)$, and the extra space is $O(d)$ for $d$ distinct values. The items need only equality and a hash function, not an order.

**Multiset methods.** Dobkin and Munro (1980) find the mode with $n \lg (n/m) + o(n \lg (n/m))$ comparisons. When $m$ is a constant fraction of $n$, this is $O(n)$ comparisons; when $m = 1$, it is $n \lg n$, the same as sorting.

| method | time | needs |
|---|---|---|
| sort and scan | $O(n \log n)$ worst case | a total order |
| hash counting | $O(n)$ expected | equality and hashing |
| counter array | $O(n + U)$ worst case | integer keys below $U$ |
| Dobkin and Munro | $O(n \log (n/m))$ worst case | a total order |

## Bounds

**Lower bound $\Omega(n \log n)$.** The [element distinctness](/element-distinctness/) problem reduces to the mode: all $n$ items are distinct exactly when $m = 1$. Element distinctness needs $\Omega(n \log n)$ comparisons in the comparison model, and $\Omega(n \log n)$ operations even in the [algebraic decision tree](/algebraic-decision-tree/) model, by the [element distinctness lower bound](/element-distinctness-lower-bound/). So the same bounds hold for the mode, and sort and scan is optimal up to a constant factor in the worst case over all inputs.

**Bound in terms of $m$.** Munro and Spira (1976) studied comparison bounds for sorting multisets and for the mode, and Dobkin and Munro (1980) improved the lower bound and gave an algorithm that matches it up to a lower-order term. The bound is about $n \lg (n/m)$ comparisons.

**Hashing is outside the model.** The $O(n)$ expected time of hash counting does not contradict the lower bound: a hash function is not a comparison, and the bound is for the worst case of a deterministic or randomized comparison algorithm.

## Reductions

- **Element distinctness to the mode.** Compute $m$ and answer "distinct" exactly when $m = 1$. This is the reduction behind the lower bound.
- **Mode to sorting.** Sort, then scan, as above.
- **Mode to counting.** Given a [dictionary](/dictionary/) of counts, the mode is a maximum over the counts, found with one scan.

## Applications

- **Data summaries.** The most frequent value of a column in a database, or the most common word in a text.
- **Voting and classification.** Plurality voting, and the majority vote of the $k$ nearest neighbours in a classifier.
- **Compression.** Coding schemes give the shortest code to the most frequent symbol, and [run-length encoding](/run-length-encoding/) gains most on long runs of one value.

## References
