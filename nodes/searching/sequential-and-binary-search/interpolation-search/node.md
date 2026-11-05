---
tag: XVAMYG
kind: algorithm
slug: interpolation-search
name: Interpolation search
aliases:
- dictionary search
area: searching/sequential-and-binary-search
level: core
summary: Estimate the probe position by linear interpolation of the key between the endpoints; O(log log n) expected on uniform keys, O(n) worst case.
model: word-ram
complexity:
  vars: {n: the number of items in the array; the average is for keys drawn independently from a uniform distribution}
  time: {worst: Θ(n), average: Θ(log log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: false, recursive: false, in_place: true}
prereqs: [binary-search, uniform-distribution]
see_also: [interpolation-search-expected-time, binary-search, exponential-search, search-in-sorted-array, learned-index, regula-falsi, predecessor-problem, uniform-distribution]
sources:
  - paper: doi:10.1145/359545.359557
    title: Yehoshua Perl, Alon Itai and Haim Avni, Interpolation search, a log log N search, Communications of the ACM 21(7) (1978)
    locator: pp. 550 to 553 (the algorithm and the proof of log log N expected accesses on uniform keys)
  - paper: doi:10.1109/SFCS.1976.32
    title: Andrew C. Yao and F. Frances Yao, The complexity of searching an ordered random table, 17th Symposium on Foundations of Computer Science (1976)
    locator: pp. 173 to 177 (the log log n expected cost and the matching lower bound)
  - paper: doi:10.1147/rd.12.0130
    title: W. W. Peterson, Addressing for random-access storage, IBM Journal of Research and Development 1(2) (1957)
    locator: pp. 130 to 146
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table (interpolation search)
---

Interpolation search finds a numeric key $x$ in a sorted array by guessing where $x$ should be from its value, as a person opens a dictionary near the front for a word that starts with "b". If the range $A[lo \ldots hi]$ holds values from $A[lo]$ to $A[hi]$, the next probe is at the fraction $(x - A[lo])/(A[hi] - A[lo])$ of the way from $lo$ to $hi$. When the keys are drawn independently from a [uniform distribution](/uniform-distribution/), the expected number of probes is $\lg \lg n + O(1)$, which is far less than the $\lg n$ of [binary search](/binary-search/): about 4 probes for a million keys. But the method uses the values of the keys, not only their order, and on badly spread keys it can take $n$ probes. The method goes back to Peterson in 1957; the $\log \log n$ bound was proved by Yao and Yao and by Perl, Itai and Avni in 1976 to 1978.

## In plain words

To find "Miller" in a phone book, you do not open it in the middle and then halve. You know M is about half way through the alphabet, so you open near the middle. To find "Baker" you open near the front. Each time, you guess the page from how far the name is between the first and the last name of the part you still have.

When the names are spread evenly, each guess lands very close to the right page, and the part left to search shrinks very fast. When the names are spread unevenly, for example when half the book is "Smith", the guesses can be poor, and the search can take a long time.

## The problem

The input is an array $A[0 \ldots n-1]$, $n \ge 0$, of numbers sorted so that $A[0] \le \cdots \le A[n-1]$, and a number $x$. The output is an index $i$ with $A[i] = x$, or NIL when $x$ is not in $A$. When $x$ occurs more than once, any of its indices is a correct output; the variants below give the first one.

The algorithm computes with the key values: a difference, a product and a division. So it needs keys that are numbers, or that can be mapped to numbers in an order-preserving way, such as fixed-length strings read as integers. It is not a comparison algorithm, and the $\lceil \lg(n+1) \rceil$ lower bound of the [comparison model](/comparison-model/) does not apply to it. The cost model is the [word RAM](/word-ram/), in which these operations take constant time.

## The algorithm

```pseudo id=main
INTERPOLATION-SEARCH(A, x)
L1  lo ← 0, hi ← n − 1
L2  while lo ≤ hi and A[lo] ≤ x and x ≤ A[hi] do     ▷ x can only be in A[lo .. hi]
L3      if A[lo] = A[hi] then return lo               ▷ then A[lo] = x
L4      pos ← lo + ⌊(x − A[lo]) · (hi − lo) / (A[hi] − A[lo])⌋   ▷ lo ≤ pos ≤ hi
L5      if A[pos] < x then lo ← pos + 1
L6      else if A[pos] > x then hi ← pos − 1
L7      else return pos
L8  return NIL
```

Line L2 keeps the search only while $x$ is between the end values of the range. If $x < A[lo]$ or $x > A[hi]$, then $x$ is not in the range and the search stops. Line L3 handles a range of equal values, where line L4 would divide by zero. Line L4 is the interpolation: since $A[lo] \le x \le A[hi]$, the fraction is in $[0, 1]$ and $pos$ is in $[lo, hi]$. Lines L5 to L7 are the three-way test of [binary search](/binary-search/), with $pos$ in place of the middle.

## Example

The array has $n = 18$ items, spread fairly evenly between 10 and 94:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $A$ | 10 | 13 | 18 | 22 | 27 | 31 | 38 | 40 | 47 | 52 | 56 | 61 | 67 | 73 | 78 | 85 | 90 | 94 |

Search for $x = 61$:

| probe | $lo$ | $hi$ | $pos = lo + \lfloor (x - A[lo])(hi - lo)/(A[hi] - A[lo]) \rfloor$ | $A[pos]$ | result |
|---|---|---|---|---|---|
| 1 | 0 | 17 | $0 + \lfloor 51 \cdot 17 / 84 \rfloor = 10$ | 56 | $56 < 61$, so $lo = 11$ |
| 2 | 11 | 17 | $11 + \lfloor 0 \cdot 6 / 33 \rfloor = 11$ | 61 | return 11 |

Binary search would need 4 or 5 probes here. A search for $x = 50$ probes $pos = \lfloor 40 \cdot 17/84 \rfloor = 8$, finds $A[8] = 47 < 50$, sets $lo = 9$, and then line L2 sees $A[9] = 52 > 50$ and stops: one probe and the answer NIL.

**A bad input.** On $A = [0, 1, 2, \ldots, 998, 10^9]$, with $n = 1000$, a search for $x = 998$ computes $pos = lo$ in every step, because the last value is so large that the fraction is close to 0. The search moves one place per probe and takes 999 probes.

## Correctness

The loop keeps this invariant: if $x$ is in $A$, then it is in $A[lo \ldots hi]$. It holds at the start. Line L2 stops the loop correctly when $lo > hi$ or $x$ is outside $[A[lo], A[hi]]$, since the array is sorted. Line L3 returns $lo$ only when $A[lo] = A[hi]$, and then $A[lo] \le x \le A[hi]$ gives $A[lo] = x$. Line L4 gives $lo \le pos \le hi$. If $A[pos] < x$, every item at index at most $pos$ is less than $x$, so moving $lo$ to $pos + 1$ keeps the invariant; the case $A[pos] > x$ is the same on the other side. Each step either returns or makes $hi - lo$ smaller, so the loop stops after at most $n$ probes. The full proof is below.

## Complexity

Count the probes, the executions of line L4.

- **Worst case.** $\Theta(n)$. Each probe removes at least one index, so there are at most $n$ probes, and the bad input above needs $n - 1$.
- **Average case.** If the $n$ keys are drawn independently from the uniform distribution on an interval, and $x$ is drawn from the same distribution or is one of the keys, the expected number of probes is $\lg \lg n + O(1)$. The proof is on the page [expected time of interpolation search](/interpolation-search-expected-time/). The idea is that the error of the guess is about the square root of the size of the range, so the range shrinks from $s$ to about $\sqrt{s}$ in each probe, and $\sqrt{\cdot}$ applied $\lg \lg n$ times takes $n$ down to a constant.
- **Best case.** One probe.
- **Space.** $\Theta(1)$.

The table gives the mean and the largest number of probes in a simulation with 2000 searches for each $n$, on $n$ random integers drawn uniformly from $[0, 10^{12})$:

| $n$ | $10^3$ | $10^4$ | $10^5$ | $10^6$ |
|---|---|---|---|---|
| mean probes, key present | 3.49 | 3.92 | 4.00 | 4.28 |
| mean probes, random key, mostly absent | 3.04 | 3.45 | 3.56 | 3.95 |
| largest probes seen, key present | 7 | 10 | 9 | 11 |
| $\lg \lg n$ | 3.32 | 3.73 | 4.05 | 4.32 |
| binary search, $\lceil \lg(n+1) \rceil$ | 10 | 14 | 17 | 20 |

Each probe costs a multiplication and a division, which are more costly than the shift of binary search. In memory, interpolation search pays off only for large arrays, or when each probe is a slow access, such as a read from a disk.

## Properties

- **Uses the key values.** It needs arithmetic on keys, so it does not work for keys that can only be compared.
- **Fast on smooth data.** Its cost depends on how close the data is to a straight line from $(0, A[0])$ to $(n-1, A[n-1])$, not on $n$ alone.
- **Not robust.** Clusters, gaps and outliers make it slow, and the worst case is linear.
- **In place.** It does not change the array.

## Variants and improvements

- **First occurrence.** When line L7 finds $x$, every index before $lo$ holds an item less than $x$, so the first copy of $x$ is in $[lo, pos]$. A [lower bound search](/lower-and-upper-bound-search/) on that range finds it.
- **Interpolation-sequential search.** Make one interpolation probe, then scan from it to the key. The expected cost on uniform keys is $O(\sqrt{n})$.
- **Guard with binary search.** Alternate interpolation probes and binary search probes, or use a binary probe when an interpolation probe did not shrink the range by half. The worst case is then $O(\log n)$, and the expected cost on uniform keys stays $O(\log \log n)$.
- **Interpolation then jumps.** Perl and Reingold make one interpolation probe and then step by $\sqrt{s}$ from it until $x$ is bracketed, then recurse on a range of $\sqrt{s}$ items. The expected number of steps is $O(1)$ per level, so $O(\log \log n)$ in all, and the analysis is short.
- **Other distributions.** If the keys follow a known distribution with cumulative distribution function $F$, interpolate on $F(x)$ instead of $x$. A [learned index](/learned-index/) takes this further: it fits a model of $F$ to the data, predicts the position, and then searches a small range around it.
- **Root finding.** Interpolation on a sorted array is the discrete form of [regula falsi](/regula-falsi/) and the [secant method](/secant-method/).

## When to use it

Use interpolation search on large sorted arrays of numbers that are spread close to evenly, such as random identifiers, hashes, or timestamps at a steady rate, and when each probe is costly, as on a disk or over a network. For data with clusters or heavy tails, or for small arrays in memory, [binary search](/binary-search/) is safer and often faster. A guarded variant gives most of the speed with a logarithmic worst case.

## Pitfalls

- **Division by zero.** When $A[lo] = A[hi]$, line L4 divides by zero. Line L3 handles that case first.
- **A probe outside the range.** When $x$ is outside $[A[lo], A[hi]]$, the fraction is outside $[0, 1]$, and $pos$ can be outside the array. Line L2 tests both ends before line L4 runs. With floating-point keys, rounding can still move $pos$ by one, so clamp it to $[lo, hi]$.
- **Overflow.** The product $(x - A[lo])(hi - lo)$ can overflow a fixed-size integer. Use a wider type, or compute the fraction in floating point and then clamp.
- **Testing $lo \le hi$ last.** Line L2 must test $lo \le hi$ before it reads $A[lo]$ and $A[hi]$.
- **Trusting the average.** The $\log \log n$ bound holds only for keys close to uniform. Real data with clusters can make the plain method slower than binary search.

## Implementations

## History

Peterson described the idea in 1957, for the search of sorted files on random-access storage. Yao and Yao proved in 1976 that the expected number of probes on uniform keys is $\lg \lg n + O(1)$, and that no algorithm can do better on average in this setting. Perl, Itai and Avni gave a simpler proof in 1978, and Perl and Reingold one in 1977 for a variant with jumps. Later work, such as the dynamic interpolation search of Mehlhorn and Tsakalidis, extends the method to sets with insertions and deletions.

## References
