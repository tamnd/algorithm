---
tag: CS857V
kind: problem
slug: range-gcd-query
name: Range GCD query
aliases:
- range gcd
area: data-structures/range-query-structures
level: intro
summary: Return the greatest common divisor of a subarray; gcd is idempotent, so sparse tables apply.
prereqs: [range-query-problem, gcd-of-two-integers, euclidean-algorithm]
see_also: [sparse-table, segment-tree, gcd-of-array, idempotent-operation, fenwick-tree, difference-array, range-minimum-query, range-update-range-query]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2 (Greatest common divisor), Euclid's algorithm and Lame's theorem on its running time
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2 (The greatest common divisor) and Section 4.5.3 (Analysis of Euclid's algorithm)
  - url: https://cp-algorithms.com/data_structures/sparse-table.html
    title: cp-algorithms, Sparse Table
    locator: section Range Minimum Queries (RMQ), the remark that the O(1) query works for every idempotent function such as gcd
---

The range GCD query asks for the greatest common divisor of the items $A[l], \ldots, A[r]$ of an integer array, for many ranges $[l, r]$. It is the [range query problem](/range-query-problem/) for $\gcd$, which is associative, commutative and [idempotent](/idempotent-operation/) on the non-negative integers, with $0$ as its identity. So a [sparse table](/sparse-table/) answers a static query with one gcd, and a [segment tree](/segment-tree/) handles point updates. One computation of $\gcd$ costs $O(\log M)$ division steps for numbers up to $M$, by the analysis of the [Euclidean algorithm](/euclidean-algorithm/), and this factor enters every bound.

## In plain words

You have a list of whole numbers. A question names a stretch of the list and asks for the largest number that divides every number of the stretch. For example, for 12, 18 and 24 the answer is 6.

Two facts make this easy. First, the common divisor of a stretch can be built from the common divisors of two parts of it, in any grouping. Second, using a number twice changes nothing: the largest common divisor of 12, 18, 18 and 24 is still 6. So the trick of the smallest-value questions works here too: cover the stretch by two pieces of the same length, which may overlap, and combine their two stored answers.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of non-negative integers, each at most $M$. Then queries $(l, r)$ with $0 \le l \le r \le n - 1$, and in the dynamic version updates.

**Output.** For each query,

$$G(l, r) = \gcd(A[l], A[l+1], \ldots, A[r]),$$

the largest integer $d \ge 0$ that divides each $A[i]$ with $l \le i \le r$, where $\gcd(0, 0, \ldots, 0) = 0$. Negative inputs are replaced by their absolute values, which have the same divisors.

**The algebra.** On the non-negative integers, $\gcd$ is associative and commutative, $\gcd(a, a) = a$, and $\gcd(0, a) = a$. So it is an idempotent commutative monoid, and $G(l, r) = \gcd(G(l, m), G(m', r))$ for any $l \le m' \le m + 1$ and $m \le r$, also when the two parts overlap. It has no inverse: $\gcd(6, x) = 6$ has many solutions $x$, so [prefix values](/prefix-sums/) cannot be subtracted.

## Variants

- **Static.** No updates; a sparse table answers each query with one gcd.
- **Point updates.** $A[i] \leftarrow x$; a segment tree gives $O(\log n)$ gcds per operation.
- **Range add.** $A[i] \leftarrow A[i] + c$ for $l \le i \le r$. Use the identity $\gcd(a_l, a_{l+1}, \ldots, a_r) = \gcd(a_l, a_{l+1} - a_l, \ldots, a_r - a_{r-1})$, which holds because $\gcd(x, y) = \gcd(x, y - x)$. On the [difference array](/difference-array/) $D[i] = A[i] - A[i-1]$, a range add changes only $D[l]$ and $D[r+1]$. Keep a segment tree of $\gcd$ over $|D|$ and a [Fenwick tree](/fenwick-tree/) of sums of $D$ to get $A[l]$; then $G(l, r) = \gcd(A[l], |D[l+1]|, \ldots, |D[r]|)$.
- **Counting.** Count the indices $i \in [l, r]$ with $A[i] = G(l, r)$, or count the subarrays with a given gcd.
- **Divisibility check.** Decide whether $G(l, r) = 1$, or whether a given $d$ divides all items of the range.

## Examples

Let $A = [12, 18, 24, 9, 36, 6, 15]$.

| query $(l, r)$ | the range | $G(l, r)$ |
|---|---|---|
| $(0, 2)$ | 12, 18, 24 | 6 |
| $(0, 3)$ | 12, 18, 24, 9 | 3 |
| $(4, 5)$ | 36, 6 | 6 |
| $(2, 2)$ | 24 | 24 |
| $(0, 6)$ | the full array | 3 |

With a sparse table, the query $(1, 4)$ has length 4 and reads one cell, $\gcd(18, 24, 9, 36) = 3$. The query $(0, 2)$ has length 3 and reads the two overlapping cells $\gcd(12, 18) = 6$ and $\gcd(18, 24) = 6$, so the answer is $\gcd(6, 6) = 6$; the item 18 is used twice, which idempotence allows.

After a range add of 3 to $A[1 \ldots 3]$, the array is $[12, 21, 27, 12, 36, 6, 15]$ and the difference array is $D = [12, 9, 6, -15, 24, -30, 9]$. Then $G(1, 3) = \gcd(21, |6|, |{-15}|) = 3$, which is $\gcd(21, 27, 12)$.

The distinct values of $G(l, r)$ for a fixed right end $r = 4$ and $l = 4, 3, \ldots, 0$ are $36, 9, 3$. Each value is a divisor of the one before it.

## Known algorithms

| method | preprocessing | query | update |
|---|---|---|---|
| scan with [gcd of an array](/gcd-of-array/) | none | $O(n + \log M)$ | $O(1)$ point |
| [sparse table](/sparse-table/) | $O(n \log n)$ gcds | 1 gcd, $O(\log M)$ | none |
| [segment tree](/segment-tree/) | $n - 1$ gcds | $O(\log n + \log M)$ | $O(\log n \cdot \log M)$ point |
| [square-root decomposition](/square-root-decomposition/) | $O(n + \sqrt n \log M)$ | $O(\sqrt n + \log M)$ | $O(\sqrt n + \log M)$ point |
| segment tree on the differences, with a Fenwick tree | $O(n \log M)$ | $O(\log n + \log M)$ | $O(\log n \cdot \log M)$ range add |

The query costs of the scan and of the segment tree follow from the folding bound below, when the query folds its parts into one running gcd from left to right.

## Bounds

**One gcd.** For $0 \le b \le a \le M$, Euclid's algorithm takes $O(\log b + 1)$ division steps; by Lame's theorem, if it takes $k \ge 1$ steps then $b \ge F_{k+1}$, a [Fibonacci number](/fibonacci-numbers/). For example, $\gcd(144, 89)$ takes 10 steps, the most for a second argument up to 89.

**Folding many items.** Computing $g_1 = A[l]$ and $g_{j+1} = \gcd(g_j, A[l + j])$ for $j = 1, \ldots, k - 1$ takes $O(k + \log M)$ division steps in total, not $O(k \log M)$. *Proof.* Let $d = g_{j+1}$. Euclid on $(g_j, a)$ does the same steps as on $(g_j / d, a / d)$, because each remainder is divided by $d$. Euclid on two numbers takes $O(1 + \log m)$ steps, where $m$ is the smaller one, and here $m \le g_j / d$, so the step costs $O(1 + \log(g_j / d))$. Summing over $j$, the terms $\log(g_j / g_{j+1})$ telescope to $\log(g_1 / g_k) \le \log M$, for $g_k \ge 1$; if some $g_j = 0$, all earlier items are 0 and those steps cost $O(1)$ each. $\square$

**Distinct values.** For a fixed $r$, the values $G(l, r)$ for $l = r, r - 1, \ldots, 0$ form a chain in which each value divides the one before. A proper divisor of a positive integer is at most half of it, so there are at most $\lfloor \lg M \rfloor + 2$ distinct values, counting a possible 0. This bounds the work of the classic $O(n \log M)$ scan that lists, for each $r$, the distinct gcds of the subarrays that end at $r$.

**Lower bounds.** Each query must look at the input or at stored values that depend on each item of the range, and the general bounds of the [range query problem](/range-query-problem/) apply. The reduction below shows that range gcd is at least as hard as range minimum on small values.

## Reductions

- **Range minimum on small values to range gcd.** Map each $x \in \{0, \ldots, w - 1\}$ to $2^x$. Then $\gcd(2^{x_l}, \ldots, 2^{x_r}) = 2^{\min(x_l, \ldots, x_r)}$, so a range gcd structure answers [range minimum queries](/range-minimum-query/), with numbers of $w$ bits.
- **Range add to point updates.** The difference identity of the variants turns each range add into two point updates.

## Applications

- Decide whether a segment of a sequence can be scaled down by a common factor, or whether a range of lattice steps has a common period.
- For positive items, count the indices of a range whose item divides all others: these are the indices with $A[i] = G(l, r)$, found with a count of the minimum, since such an item is also the minimum.
- Count the subarrays with gcd 1, or the number of distinct subarray gcds, with the chain bound above.
- Reduce fractions or periods of signals over windows of time.

## References
