---
tag: T604D3
kind: data-structure
slug: fenwick-tree
name: Fenwick tree
aliases:
- binary indexed tree
- BIT
area: data-structures/range-query-structures
level: core
summary: Compact array structure for prefix aggregates with point updates in O(log n).
implements: [range-query-structure]
model: word-ram
complexity:
  vars: {n: the length of the array}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [prefix-sums, invertible-operation, bit-manipulation, loop-invariant]
see_also: [segment-tree, point-update-range-sum-query, range-sum-query, range-update-point-query, two-dimensional-fenwick-tree, dynamic-partial-sums-lower-bound, counting-inversions, offline-query-processing]
sources:
  - paper: doi:10.1002/spe.4380240306
    title: "Peter M. Fenwick, A new data structure for cumulative frequency tables, Software: Practice and Experience 24(3) (1994), 327-336"
    locator: the whole paper (the tree of partial sums indexed by the low bits of the index, update and prefix sum in O(log n), and the search for a cumulative frequency)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 9, Range queries, Section 9.2 Binary indexed tree, and Section 9.4 Additional techniques (range updates)
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1 (the Omega(lg n) bound for partial sums)
---

A Fenwick tree, or binary indexed tree, is an array $T[1 \ldots n]$ in which $T[i]$ holds the sum of the $\operatorname{lowbit}(i)$ items of $A$ that end at position $i$, where $\operatorname{lowbit}(i)$ is the value of the lowest set bit of $i$. With it, a [prefix sum](/prefix-sums/) and a point update each take $O(\log n)$ time, and the extra memory is one array of $n$ words. A range sum is the difference of two prefix sums, so the plain tree needs an [invertible operation](/invertible-operation/), such as addition in a group. Peter Fenwick published it in 1994 for the frequency tables of arithmetic coding, and it is the shortest code for the [point update range sum query](/point-update-range-sum-query/) problem.

## In plain words

You keep a list of numbers, and you want two things: change one number, and get the total of the first so many numbers. Keeping all running totals makes a change slow, because every later total moves. Keeping only the numbers makes a total slow.

A Fenwick tree keeps a middle path. Each slot of a helper list holds the total of a short run of numbers that ends at that slot. The length of the run comes from the binary form of the slot number: it is the value of its last one bit. Slot 12 is 1100 in binary, so it covers the 4 numbers from 9 to 12. A total of the first so many numbers then needs only a few slots, one for each one bit. A change touches only the few slots whose runs contain the changed position.

## The abstract type

A Fenwick tree implements the [range query structure](/range-query-structure/) for an array $A[1 \ldots n]$ over an abelian group $(G, +, 0)$, for example the integers with addition. It supports these operations.

- BUILD$(A)$ makes the tree of an array.
- ADD$(i, \delta)$ sets $A[i] \leftarrow A[i] + \delta$.
- PREFIX$(i)$ returns $A[1] + \cdots + A[i]$, and PREFIX$(0) = 0$.
- RANGE$(l, r)$ returns $A[l] + \cdots + A[r]$ for $1 \le l \le r \le n$.
- SEARCH$(s)$ returns the least $i$ with PREFIX$(i) \ge s$, when all items are non-negative.

ADD and PREFIX need only a commutative [monoid](/monoid/). RANGE needs the inverse, and SEARCH needs an order on $G$ that agrees with $+$.

## Representation

For $i \ge 1$ let $\operatorname{lowbit}(i) = 2^t$ where $2^t$ divides $i$ and $2^{t+1}$ does not. In two's complement, $\operatorname{lowbit}(i)$ is `i & -i`. The tree is an array $T[1 \ldots n]$, and its single invariant is

$$T[i] = \sum_{k \in R(i)} A[k], \qquad R(i) = (i - \operatorname{lowbit}(i),\ i\,] = \{\, i - \operatorname{lowbit}(i) + 1, \ldots, i \,\}.$$

So $T[i] = A[i]$ for odd $i$, $T[i]$ covers 2 items when $i \equiv 2 \pmod 4$, and $T[8]$ covers $A[1 \ldots 8]$. The ranges $R(i)$ are dyadic: $R(i) = (k 2^t, (k+1) 2^t]$ for an even $k$. Two dyadic ranges are either disjoint or one holds the other. If $j = i + \operatorname{lowbit}(i)$, then $R(j)$ is the smallest range that strictly holds $R(i)$, so $j$ is the *parent* of $i$, and the parents form a forest on $\{1, \ldots, n\}$ whose roots are the indices with a parent larger than $n$. No pointers are stored: the shape is in the binary digits of the indices.

## Operations

```pseudo id=main
ADD(T, n, i, δ)                            ▷ A[i] ← A[i] + δ, for 1 ≤ i ≤ n
L1  while i ≤ n do
L2      T[i] ← T[i] + δ
L3      i ← i + lowbit(i)                  ▷ go to the next range that holds i

PREFIX(T, i)                               ▷ A[1] + … + A[i], for 0 ≤ i ≤ n
L4  s ← 0
L5  while i > 0 do
L6      s ← s + T[i]
L7      i ← i − lowbit(i)                  ▷ drop the lowest set bit
L8  return s

RANGE(T, l, r)                             ▷ A[l] + … + A[r], for 1 ≤ l ≤ r ≤ n
L9  return PREFIX(T, r) − PREFIX(T, l − 1)
```

PREFIX walks from $i$ down to 0 and clears one bit at each step. The ranges $R(i)$, $R(i - \operatorname{lowbit}(i))$, and so on are adjacent and disjoint, and together they are $(0, i]$. So the sum of the visited cells is the prefix sum. The loop runs once for each set bit of $i$, at most $\lfloor \lg n \rfloor + 1$ times.

ADD walks up from $i$. The visited indices are exactly the $j \le n$ with $i \in R(j)$, so these are the cells that must change. Each step at least doubles $\operatorname{lowbit}(i)$, so the loop runs at most $\lfloor \lg n \rfloor + 1$ times.

```pseudo id=build
BUILD(A, n)                                ▷ linear-time construction
L10 T[1 .. n] ← A[1 .. n]
L11 for i ← 1 to n do
L12     j ← i + lowbit(i)
L13     if j ≤ n then T[j] ← T[j] + T[i]   ▷ T[i] is final when i is reached
```

BUILD pushes each finished cell into its parent. When the loop reaches $i$, all children of $i$ are smaller than $i$ and have already added their sums, so $T[i]$ is final. It does $n$ additions, against $\Theta(n \log n)$ for $n$ calls of ADD.

```pseudo id=search
SEARCH(T, n, s)                            ▷ least i with PREFIX(i) ≥ s; items ≥ 0
L14 pos ← 0, step ← the largest power of two ≤ n
L15 while step > 0 do
L16     if pos + step ≤ n and T[pos + step] < s then
L17         pos ← pos + step, s ← s − T[pos]
L18     step ← step / 2
L19 return pos + 1                         ▷ n + 1 if the total is less than s
```

SEARCH is a [binary search](/binary-search/) that uses the tree directly. It keeps $pos$ as the largest index found so far with PREFIX$(pos) < s_0$, where $s_0$ is the first $s$, and it keeps $s = s_0 - $ PREFIX$(pos)$. Because $pos$ is a multiple of $2 \cdot step$ at each test, $R(pos + step) = (pos, pos + step]$, so $T[pos + step]$ is exactly the sum of the next $step$ items. This takes $O(\log n)$ time, against $O(\log^2 n)$ for a binary search that calls PREFIX.

## Example

Take $n = 10$ and $A = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]$. BUILD gives:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| binary | 1 | 10 | 11 | 100 | 101 | 110 | 111 | 1000 | 1001 | 1010 |
| $R(i)$ | 1 | 1 to 2 | 3 | 1 to 4 | 5 | 5 to 6 | 7 | 1 to 8 | 9 | 9 to 10 |
| $T[i]$ | 3 | 4 | 4 | 9 | 5 | 14 | 2 | 31 | 5 | 8 |

- PREFIX$(7)$ visits $7 \to 6 \to 4 \to 0$ and returns $T[7] + T[6] + T[4] = 2 + 14 + 9 = 25$.
- PREFIX$(10)$ visits $10 \to 8 \to 0$ and returns $8 + 31 = 39$, the total.
- RANGE$(3, 7) = $ PREFIX$(7) - $ PREFIX$(2) = 25 - 4 = 21 = 4 + 1 + 5 + 9 + 2$.
- ADD$(3, 2)$ visits $3 \to 4 \to 8 \to 16$, so $T[3] = 6$, $T[4] = 11$ and $T[8] = 33$, and the loop stops at $16 > 10$. Now RANGE$(3, 7) = (2 + 14 + 11) - 4 = 23$.
- SEARCH$(20)$ on the first array: the prefix sums are $3, 4, 8, 9, 14, 23, \ldots$, so the answer is 6. The search tests $T[8] = 31$ (not less than 20), then takes $T[4] = 9$ ($pos = 4$, $s = 11$), rejects $T[6] = 14$, takes $T[5] = 5$ ($pos = 5$, $s = 6$), and returns $6$.

## Correctness

The invariant is the equation for $T[i]$ in the representation. BUILD makes it true, ADD keeps it true, and PREFIX, RANGE and SEARCH return the right values when it holds. The two key facts are that the PREFIX chain of $i$ cuts $(0, i]$ into the disjoint ranges of the visited cells, and that the ADD chain of $i$ visits exactly the cells whose range holds $i$. The [full proof](proofs/correctness.md) shows both from the binary form of the indices, and proves BUILD and SEARCH.

## Complexity

| operation | time, worst case | notes |
|---|---|---|
| BUILD | $\Theta(n)$ | $n$ additions; $n$ calls of ADD take $\Theta(n \log n)$ |
| ADD | $O(\log n)$ | at most $\lfloor \lg n \rfloor + 1$ cells |
| PREFIX | $O(\log n)$ | one step for each set bit of $i$ |
| RANGE | $O(\log n)$ | two calls of PREFIX |
| SEARCH | $O(\log n)$ | $\lfloor \lg n \rfloor + 1$ tests |
| space | $n$ words | no pointers, no child links |

The costs are counts of group operations and word operations in the [word RAM](/word-ram/), where `i & -i` takes one step. ADD at $i = 1$ and PREFIX at $i = 2^k - 1$ meet the bound $\Theta(\log n)$, so it is tight for single calls. For the problem itself, Patrascu and Demaine proved that every structure in the [cell-probe model](/cell-probe-model/) needs $\max(t_u, t_q) = \Omega(\log n)$ amortized time for updates and prefix sums of word-size values, see the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/). So the Fenwick tree is optimal up to a constant factor.

## Variants

- **Range update, point query.** Store the [difference array](/difference-array/) $D[i] = A[i] - A[i-1]$ in the tree. Adding $\delta$ to $A[l \ldots r]$ is ADD$(l, \delta)$ and ADD$(r + 1, -\delta)$, and $A[i] = $ PREFIX$(i)$. This solves [range update point query](/range-update-point-query/).
- **Range update, range query.** Keep two trees $B_1$ and $B_2$. A range add of $\delta$ on $[l, r]$ adds $\delta$ and $-\delta$ to $B_1$ at $l$ and $r + 1$, and $\delta(l - 1)$ and $-\delta r$ to $B_2$ at the same places. Then PREFIX$(i) = i \cdot B_1(i) - B_2(i)$, where $B_k(i)$ is the prefix sum of tree $k$.
- **Prefix minimum or maximum.** With $\min$ in place of $+$, PREFIX gives prefix minima, and ADD can only lower values. A general range minimum is not a difference of prefixes, because $\min$ has no inverse, see [idempotent operation](/idempotent-operation/) and the [segment tree](/segment-tree/).
- **More dimensions.** A [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) nests the loops and takes $O(\log^2 n)$ per operation on an $n \times n$ grid.
- **Order statistics.** On an array of counts over a value range, ADD inserts or deletes a value, and SEARCH$(k)$ returns the $k$-th smallest. This counts [inversions](/counting-inversions/) in $O(n \log n)$ time.
- **0-based form.** Some code uses $T[i]$ for the range $[(i \mathbin{\&} (i+1)), i]$ and the steps `i = (i & (i + 1)) - 1` and `i = i | (i + 1)`. It is the same tree shifted by one.

## When to use it

Use a Fenwick tree for prefix sums, range sums and counts under point updates, and for offline counting problems after [coordinate compression](/coordinate-compression/). It is shorter, faster in practice and smaller than a [segment tree](/segment-tree/), and it needs no recursion. Use a segment tree instead when the operation has no inverse (range minimum, range gcd), when you need range assignment, or when the combination is not commutative. Use plain [prefix sums](/prefix-sums/) when the array never changes.

## Pitfalls

- **Index 0.** With 1-based indices, ADD$(0, \delta)$ loops for ever, because $\operatorname{lowbit}(0) = 0$. Shift a 0-based index by one before line L1.
- **RANGE without an inverse.** Line L9 subtracts. With $\min$, $\max$ or $\gcd$ the subtraction does not exist, and PREFIX$(r)$ alone is not the answer for $[l, r]$.
- **SEARCH with negative items.** Line L16 assumes that the prefix sums do not decrease. With a negative item the result can be wrong.
- **The first step of SEARCH.** Line L14 must start with the largest power of two that is at most $n$. Starting at $n$ itself, when $n$ is not a power of two, tests cells whose range is not $(pos, pos + step]$.
- **Overflow.** Prefix sums can exceed the range of the items. Use a wider word for $T$ than for $A$.
- **Assignment.** To set $A[i] \leftarrow v$, call ADD$(i, v - A[i])$ and keep a copy of $A$. The tree alone does not store $A[i]$.

## Implementations

## History

Peter Fenwick described the structure in 1994 as a compact way to keep the cumulative frequencies of an adaptive arithmetic coder, with update, prefix sum and the search for a frequency in $O(\log n)$ time each. In competitive programming it is known as the binary indexed tree, and Laaksonen's handbook gives it as the first dynamic range query structure. The matching lower bound of $\Omega(\log n)$ in the cell-probe model is due to Patrascu and Demaine in 2004 and 2006.

## References
