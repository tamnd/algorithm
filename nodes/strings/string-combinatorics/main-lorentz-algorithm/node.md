---
tag: W9BQDM
kind: algorithm
slug: main-lorentz-algorithm
name: Main-Lorentz algorithm
area: strings/string-combinatorics
level: advanced
summary: A divide and conquer algorithm that finds all repetitions (squares) in a string in O(n log n) time using Z-function computations.
solves: [computing-runs]
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n·log n), best: Θ(n·log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [square, z-algorithm, divide-and-conquer-paradigm]
see_also: [computing-runs, maximal-repetition, square-free-word, counting-distinct-squares, lyndon-based-runs-computation, runs-theorem, longest-common-extension-query, master-theorem]
sources:
  - paper: doi:10.1016/0196-6774(84)90021-x
    title: Michael G. Main and Richard J. Lorentz, An O(n log n) algorithm for finding all repetitions in a string, Journal of Algorithms 5(3), 1984, 422-432
    locator: the divide and conquer scheme, the left and right repetitions across the split found with extension functions, the grouped output, and the lower bound for algorithms that only test letters for equality
  - paper: doi:10.1016/0020-0190(81)90024-7
    title: Maxime Crochemore, An optimal algorithm for computing the repetitions in a word, Information Processing Letters 12(5), 1981, 244-250
    locator: the earlier O(n log n) algorithm for all maximal repetitions by partition refinement
  - paper: doi:10.1109/sffcs.1999.814634
    title: Roman Kolpakov and Gregory Kucherov, Finding maximal repetitions in a word in linear time, 40th Annual Symposium on Foundations of Computer Science (FOCS 1999), 596-604
    locator: the use of Main-Lorentz extension functions inside the Lempel-Ziv factors, giving all runs in linear time over a constant alphabet
---

The Main-Lorentz algorithm finds every occurrence of a [square](/square/) $uu$ in a string of length $n$ in $O(n \log n)$ time. It splits the string in the middle, solves both halves, and finds the squares that cross the split with four runs of the [Z-algorithm](/z-algorithm/). There can be $\Theta(n^2)$ square occurrences, so the algorithm reports them in at most $O(n \log n)$ groups, each an interval of start positions with one half-length. Letters are only tested for equality, and for that model $O(n \log n)$ is optimal.

## In plain words

Cut the text in the middle. A square either lies entirely in the left part, entirely in the right part, or straddles the cut. The first two kinds are found by doing the same thing to each part. For the squares that straddle the cut, fix the length of the repeated piece. The cut position then has a twin, the same length away inside the square. A square of that length straddles the cut exactly when the text just before the twin matches the text just before the cut for long enough, and the text just after them matches too. Measuring how far the matches reach takes one pass of the Z-algorithm for all lengths at once. Each level of cutting costs linear time, and there are about log n levels.

## The problem

The input is a string $s = s[0..n-1]$ over an [alphabet](/alphabet/) with equality of letters only; indices are 0-based. A square occurrence is a pair $(i, m)$ with $m \ge 1$, $i + 2m \le n$ and $s[i..i+m-1] = s[i+m..i+2m-1]$. The output is a list of triples $(l, h, m)$ such that $s[i..i+2m-1]$ is a square for every $i$ with $l \le i \le h$, and every square occurrence lies in exactly one triple. In particular the output is empty if and only if $s$ is a [square-free word](/square-free-word/).

## The algorithm

For a word $t$, $Z(t)$ is its Z-array: $Z(t)[r]$ is the length of the longest common prefix of $t$ and $t[r..]$. Let $\#$ be a separator equal to no letter, and $\overline{x}$ the reversal of $x$. A segment $[lo, hi)$ with at least two letters is split at $mid = \lfloor (lo + hi)/2 \rfloor$ into $u = s[lo..mid-1]$ and $v = s[mid..hi-1]$. A square inside the segment crosses the split if it contains both $s[mid-1]$ and $s[mid]$. It is a left square if its center $i + m$ is at most $mid$, and a right square otherwise.

```pseudo id=main
MAIN-LORENTZ(s)                                  ▷ s[0 .. n − 1]
L1  R ← empty list, S ← stack holding the segment [0, n)
L2  while S is not empty do
L3      pop [lo, hi) from S; if hi − lo ≤ 1 then skip to the next iteration
L4      mid ← ⌊(lo + hi)/2⌋, u ← s[lo .. mid − 1], v ← s[mid .. hi − 1]; push [lo, mid) and [mid, hi)
L5      A ← Z(ū), B ← Z(v · # · u), C ← Z(ū · # · v̄), D ← Z(v)
L6      for m ← 1 to |u| do                         ▷ left squares, center ≤ mid
L7          k₁ ← A[m] (0 if m = |u|), k₂ ← B[|v| + 1 + |u| − m]
L8          a₁ ← max(0, m − k₂), a₂ ← min(m − 1, k₁); if a₁ ≤ a₂ then append (mid − m − a₂, mid − m − a₁, m) to R
L9      for m ← 1 to |v| do                         ▷ right squares, center > mid
L10         k₁ ← C[|u| + 1 + |v| − m], k₂ ← D[m] (0 if m = |v|)
L11         a₁ ← max(1, m − k₂), a₂ ← min(m − 1, k₁); if a₁ ≤ a₂ then append (mid − a₂, mid − a₁, m) to R
L12 return R
```

For a left square of half-length $m$, the index $mid$ in the second half has the twin $p = mid - m$ in the first half. The value $k_1$ of line L7 is the length of the longest common suffix of $s[lo..p-1]$ and $s[lo..mid-1]$, and $k_2$ is the length of the longest common prefix of $s[p..mid-1]$ and $s[mid..hi-1]$. A square that starts $a$ letters before the twin, at $i = p - a$, needs the $a$ letters before $p$ to match the $a$ letters before $mid$, so $a \le k_1$, and the $m - a$ letters from $p$ on to match those from $mid$ on, so $m - a \le k_2$. Line L8 reports the whole interval of such $a$ at once. Right squares are the mirror image: the index $mid$ in the first half has the twin $mid + m$, $k_1$ compares the text before $mid$ with $v[0..m-1]$, and $k_2$ compares the text from $mid$ with the text from $mid + m$.

## Example

Let $s = $ `abaabaa`, $n = 7$. The root segment $[0, 7)$ has $mid = 3$, $u = $ `aba`, $v = $ `abaa`.

| Side | $m$ | $k_1$ | $k_2$ | $[a_1, a_2]$ | Triple |
|---|---|---|---|---|---|
| left | 1 | 0 | 1 | $[0, 0]$ | $(2, 2, 1)$: `aa` at 2 |
| left | 2 | 1 | 0 | $[2, 1]$, empty | none |
| left | 3 | 0 | 3 | $[0, 0]$ | $(0, 0, 3)$: `abaaba` at 0 |
| right | 1 | 1 | 0 | $[1, 0]$, empty | none |
| right | 2 | 0 | 1 | $[1, 0]$, empty | none |
| right | 3 | 3 | 1 | $[2, 2]$ | $(1, 1, 3)$: `baabaa` at 1 |
| right | 4 | 1 | 0 | $[4, 1]$, empty | none |

For the left side with $m = 3$, the twin is $p = 0$, there is nothing before it, so $k_1 = 0$, and `aba` matches the first three letters of $v$, so $k_2 = 3$. For the right side with $m = 3$, $v[0..2] = $ `aba` equals $u$, so $k_1 = 3$, and $Z(v)[3] = 1$ since $v = $ `abaa`. Of the smaller segments, only $[5, 7)$ = `aa` reports a square, $(5, 5, 1)$. The output is the four triples $(2, 2, 1)$, $(0, 0, 3)$, $(1, 1, 3)$, $(5, 5, 1)$, which are the four square occurrences of `abaabaa`.

## Correctness

The segments form a binary tree: the root is $[0, n)$, and a segment with at least two letters has the two children pushed at line L4. Each segment of the tree is popped exactly once. A square occurrence $[i, i+2m)$ lies in the root; following the child that contains it, one reaches a unique segment where it contains both $s[mid-1]$ and $s[mid]$, since a single letter cannot contain a square. At that segment it is a left square if $i + m \le mid$ and a right square otherwise. The key lemma says that for a fixed $m$, the left squares of half-length $m$ inside the segment that cross the split are exactly those with $i = mid - m - a$ and $a_1 \le a \le a_2$, and similarly for right squares. So each square occurrence is reported once, at its segment, and nothing else is reported. The full proof, with the meaning of each Z-value, is in the proof file.

## Complexity

- **Time.** A segment of length $L$ costs $O(L)$: four Z-arrays of total length at most $4L$, each in linear time, and two loops of $O(L)$ steps. The segments at one depth of the tree are disjoint, so each depth costs $O(n)$, and there are $\lceil \log_2 n \rceil$ depths. So the time is $O(n \log n)$. Every segment of length at least 2 does this work in full, so the time is also $\Omega(n \log n)$ on every input, for example $\Theta(n \log n)$ on a square-free string.
- **Output size.** A segment of length $L$ appends at most $L$ triples, so the output has $O(n \log n)$ triples, even for $a^n$ with its $\Theta(n^2)$ square occurrences.
- **Space.** Besides the output, the arrays of one segment take $O(L) \le O(n)$ cells, and the stack holds $O(\log n)$ segments. So the extra space is $\Theta(n)$.
- **Comparisons.** The Z-algorithm makes $O(L)$ letter comparisons on a word of length $L$, so the total is $O(n \log n)$ equality tests. Main and Lorentz proved that algorithms that only test letters for equality need $\Omega(n \log n)$ tests in the worst case to decide whether a string over an unbounded alphabet is square-free, so the algorithm is optimal in that model.

## Properties

- **Equality only.** The algorithm never compares letters by order and never uses them as indices, so it works over any alphabet with an equality test.
- **Deterministic and not online.** The split of the root segment depends on $n$, so the whole string must be known in advance.
- **Grouped output.** For a fixed segment, side and half-length, the reported squares form one interval of start positions. They are consecutive squares of one periodic factor: $s[mid - m - k_1 .. mid + k_2 - 1]$ for the left side has the period $m$.
- **Iterative.** The pseudocode uses an explicit stack; a recursive version has recursion depth $\lceil \log_2 n \rceil$.

## Variants and improvements

- **Square-freeness.** Stop at the first triple. The time is still $O(n \log n)$ in the worst case. Over a constant alphabet, square-freeness can be tested in $O(n)$ time, for example with a suffix tree or the Lempel-Ziv factorization; Main and Lorentz gave such a linear test in 1985.
- **Runs.** The intervals of line L8 come from periodic factors with the period $m$, maximal inside the segment. Extending these factors to the whole string and keeping only smallest periods lists all [runs](/maximal-repetition/) in $O(n \log n)$ time; see [computing runs](/computing-runs/). Kolpakov and Kucherov applied the same extension functions inside the blocks of the Lempel-Ziv factorization to find all runs in $O(n)$ time over a constant alphabet.
- **Longest common extensions.** The Z-arrays answer exactly the [longest common extension queries](/longest-common-extension-query/) that the method needs.
- **Crochemore's algorithm.** A different $O(n \log n)$ method that refines partitions of positions by equal factors of growing length, from 1981.

## When to use it

Use it to list all square occurrences, or all repetitions with their periods, when $O(n \log n)$ time is acceptable and the alphabet has only an equality test, or when a short and robust implementation is wanted. Over integer alphabets, the [Lyndon-based runs computation](/lyndon-based-runs-computation/) gives all runs in $O(n)$ time, and the runs encode all squares. To count distinct squares, see [counting distinct squares](/counting-distinct-squares/).

## Pitfalls

- **Listing squares one by one.** Expanding the triples costs time proportional to the number of square occurrences, which is $\Theta(n^2)$ for $a^n$. Keep the triples when possible.
- **The separator.** In $v \cdot \# \cdot u$, the separator must differ from every letter; otherwise the common prefix of a suffix of $u$ with $v$ can run past the end of $u$ and report squares that end outside the segment.
- **Double counting at the center.** A square with center exactly at $mid$ is a left square, with $a = 0$. The right side must start at $a = 1$, or that square is reported twice.
- **Indices at the ends.** For $m = |u|$ the twin is at $lo$ and $k_1 = 0$; for $m = |v|$ on the right, $k_2 = 0$. Reading $Z$ at an index equal to its length is out of range.

## Implementations

## History

Main and Lorentz published the algorithm in 1984 in the Journal of Algorithms, with a proof that $\Omega(n \log n)$ equality tests are needed in the worst case. Crochemore had given another $O(n \log n)$ algorithm in 1981, and Apostolico and Preparata one based on suffix trees in 1983. Main and Lorentz gave a linear-time test for square-freeness over a fixed alphabet in 1985. The extension functions of their method became a building block of the linear-time algorithm of Kolpakov and Kucherov for runs.

## References
