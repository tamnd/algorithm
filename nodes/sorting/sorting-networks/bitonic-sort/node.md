---
tag: TD72MA
kind: algorithm
slug: bitonic-sort
name: Bitonic sort
aliases:
- Batcher's bitonic sorter
- bitonic sorting network
area: sorting/sorting-networks
level: core
summary: Batcher's network that sorts by recursively building and merging bitonic sequences, with O(log^2 n) depth.
solves: [sorting-problem]
model: sorting-network
complexity:
  vars: {n: "the number of items, a power of 2 in the exact counts"}
  time: {worst: Θ(n log² n), average: Θ(n log² n), best: Θ(n log² n)}
  space: {extra: Θ(log n)}
  depth: {worst: Θ(log² n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1968
  people: [Kenneth E. Batcher]
  note: Batcher gave the bitonic sorter and the odd-even merge sorter in one paper at the 1968 Spring Joint Computer Conference.
prereqs: [bitonic-merger, sorting-network]
see_also: [bitonic-sequence, bitonic-merger, odd-even-merge-sort, zero-one-principle, network-depth, network-size, merge-sort, bitonic-counting-network]
sources:
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32 (1968)
    locator: pp. 307 to 314
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (Batcher's bitonic sorter)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Sections 27.3 to 27.5 (the half-cleaner, the bitonic sorter, the merger and the sorter)
---

Bitonic sort is Batcher's [sorting network](/sorting-network/) that sorts $n = 2^k$ items with $\tfrac14 n \lg n (\lg n + 1)$ [comparators](/comparator/) in $\tfrac12 \lg n (\lg n + 1)$ layers. It sorts the two halves, puts them together as one [bitonic sequence](/bitonic-sequence/), and sorts that sequence with a [bitonic merger](/bitonic-merger/). Its [depth](/network-depth/) is $O(\log^2 n)$, and each layer compares the same pairs whatever the input is. So it runs well on parallel hardware such as SIMD units and GPUs, where the simple and regular pattern of its comparators matters more than its $\Theta(n \log^2 n)$ work.

## In plain words

A sequence that first goes up and then goes down is called bitonic. There is a fast way to sort a bitonic sequence: compare each item of the first half with the item at the same place in the second half, and put the smaller one in the first half. Now each item of the first half is at most each item of the second half, and each half is again bitonic. Do the same in each half, and so on, until the parts have one item.

Bitonic sort uses this to sort any list. It sorts the first half and the second half, with the same method. A sorted half followed by the other sorted half turned around is bitonic. So the method sorts the two halves, then sorts the bitonic result.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, where $n = 2^k$. The output is the same array in non-decreasing order. The method must be a fixed sequence of compare-exchange steps: which pairs it compares can depend on $n$, but not on the items. This is the [sorting problem](/sorting-problem/) in the [sorting network](/sorting-network/) model. Other values of $n$ are handled in [Variants and improvements](#variants-and-improvements).

## The algorithm

The call BITONIC-SORT$(A, 0, n)$ sorts the full array. The range $[lo, lo + m)$ holds $A[lo \ldots lo+m-1]$, and $m$ is always a power of 2.

```pseudo id=main
BITONIC-SORT(A, lo, m)                     ▷ sort A[lo .. lo + m − 1]
L1  if m ≤ 1 then return
L2  h ← m / 2
L3  BITONIC-SORT(A, lo, h)
L4  BITONIC-SORT(A, lo + h, h)
L5  for t ← 0 to h − 1 do COMPARE(A, lo + t, lo + m − 1 − t)    ▷ the flip
L6  HALF-CLEANERS(A, lo, h)
L7  HALF-CLEANERS(A, lo + h, h)

HALF-CLEANERS(A, lo, m)                    ▷ sort a bitonic A[lo .. lo + m − 1]
L8  if m ≤ 1 then return
L9  h ← m / 2
L10 for t ← 0 to h − 1 do COMPARE(A, lo + t, lo + t + h)
L11 HALF-CLEANERS(A, lo, h)
L12 HALF-CLEANERS(A, lo + h, h)

COMPARE(A, i, j)                           ▷ a comparator [i:j], with i < j
L13 if A[i] > A[j] then exchange A[i] and A[j]
```

Lines L5 to L7 are the merger of two sorted halves. Line L5 compares the first item with the last, the second with the second to last, and so on, so it acts as a half-cleaner on the first half followed by the second half in reverse order. The comparators of one line L5 or L10 have disjoint wires, so a parallel machine runs each of these lines as one step. All comparators put the minimum on the lower wire, so the network is in the standard form.

The comparators that one call makes depend only on $lo$ and $m$. So the same calls on any array of length $n$ give one fixed list of comparators. To get the network itself, record the pairs of line L13 instead of comparing.

## Example

Sort $A = [3, 7, 4, 8, 6, 2, 1, 5]$. The network has 6 layers. Each row shows the comparators of one layer and the array after them.

| layer | comparators | array after the layer |
|---|---|---|
| 1 | [0:1] [2:3] [4:5] [6:7] | 3 7 4 8 2 6 1 5 |
| 2 (flip) | [0:3] [1:2] [4:7] [5:6] | 3 4 7 8 2 1 6 5 |
| 3 | [0:1] [2:3] [4:5] [6:7] | 3 4 7 8 1 2 5 6 |
| 4 (flip) | [0:7] [1:6] [2:5] [3:4] | 3 4 2 1 8 7 5 6 |
| 5 | [0:2] [1:3] [4:6] [5:7] | 2 1 3 4 5 6 8 7 |
| 6 | [0:1] [2:3] [4:5] [6:7] | 1 2 3 4 5 6 7 8 |

After layer 3 both halves $[3, 4, 7, 8]$ and $[1, 2, 5, 6]$ are sorted. Layer 4 compares 3 with 6, 4 with 5, 7 with 2 and 8 with 1. Each item of the first half $[3, 4, 2, 1]$ is now at most each item of the second half $[8, 7, 5, 6]$, and both halves are bitonic. Layers 5 and 6 sort each half. The network has $3 \cdot 4 + 4 + 4 + 4 = 24$ comparators, which is $\tfrac14 \cdot 8 \cdot 3 \cdot 4$.

## Correctness

By the [zero-one principle](/zero-one-principle/) it is enough to show that the network sorts each input of zeros and ones. The proof uses one lemma. Call a 0-1 sequence bitonic when its ones fill one cyclic interval of positions. If $x$ has length $2h$ and is bitonic in this sense, then after the comparators $[t : t + h]$ for $t < h$, one half is all zeros or all ones, both halves are bitonic, and each item of the first half is at most each item of the second half. The reason is that a cyclic interval of at most $h$ ones can not hold both $t$ and $t + h$, and the same is true for zeros. By induction on $m$, HALF-CLEANERS then sorts each bitonic 0-1 sequence. Two sorted halves with the second in reverse order form a bitonic sequence, and line L5 is the half-cleaner of that sequence with the second half reversed. So lines L5 to L7 sort, and induction on $m$ completes the proof. The full proof is below.

## Complexity

Let $n = 2^k$. HALF-CLEANERS on $m$ wires has $\tfrac12 m \lg m$ comparators in $\lg m$ layers. The merger of lines L5 to L7 on $m$ wires has $m/2 + 2 \cdot \tfrac14 m \lg(m/2) = \tfrac12 m \lg m$ comparators in $\lg m$ layers. So the size $S$ and the depth $D$ satisfy

$$S(n) = 2 S(n/2) + \tfrac12 n \lg n, \qquad D(n) = D(n/2) + \lg n, \qquad S(1) = D(1) = 0,$$

which give

$$S(n) = \tfrac14 n k (k + 1), \qquad D(n) = \tfrac12 k (k + 1).$$

For $n = 2, 4, 8, 16, 32$ the size is $1, 6, 24, 80, 240$ and the depth is $1, 3, 6, 10, 15$.

- **Sequential time.** $\Theta(n \log^2 n)$ in each case, because the network makes the same $S(n)$ comparisons on each input.
- **Parallel time.** With $n/2$ processors, one layer per step, the time is $D(n) = \Theta(\log^2 n)$ and the work is $\Theta(n \log^2 n)$.
- **Extra space.** $\Theta(\log n)$ for the recursion. An iterative form with three nested loops needs $O(1)$ extra space.

[Odd-even merge sort](/odd-even-merge-sort/) has the same depth with fewer comparators: $\tfrac14 n k (k - 1) + n - 1$. Any comparison sort needs $\lg(n!) = n \lg n - \Theta(n)$ comparisons, and the [AKS network](/aks-sorting-network/) reaches size $O(n \log n)$ and depth $O(\log n)$, but with constants so large that it is never used.

## Properties

- **Data oblivious.** The sequence of comparisons does not depend on the items. This also makes it safe against timing attacks that read the branch pattern, if the compare-exchange is done without a branch.
- **In place.** It moves items only by exchanges.
- **Not stable.** The flip of line L5 compares items far apart and can move an item over an equal one.
- **Not adaptive.** A sorted input costs the same $S(n)$ comparisons.
- **Regular.** In the layers of line L10, wire $i$ is compared with wire $i \oplus h$ for a fixed $h$. In the common variant below, each layer of the whole network has this form, so the network maps onto a hypercube: each layer uses the links of one dimension.

## Variants and improvements

- **Directions instead of the flip.** Batcher's original form sorts the first half up and the second half down, so their concatenation is bitonic, and then applies half-cleaners only. Some comparators then put the minimum on the higher wire. Each layer compares $i$ with $i \oplus h$, which suits hardware. The size and the depth are the same.
- **Iterative form.** For $p = 2, 4, \ldots, n$ and for $q = p/2, p/4, \ldots, 1$, compare each pair $(i, i \oplus q)$ with $i \oplus q > i$, in the direction given by bit $p$ of $i$. This is the common form on GPUs.
- **Any $n$.** Build the network for the next power of 2 and drop each comparator that touches a wire $j \ge n$. This is correct for each network in the standard form: think of the missing wires as holding $+\infty$; such a wire keeps $+\infty$, and a comparator on it changes nothing. The Python code below does this. For $n = 5, \ldots, 15$ it gives $11, 15, 18, 24, 37, 42, 46, 54, 57, 64, 70$ comparators.
- **Bitonic merge alone.** Lines L8 to L12 sort each bitonic input. They merge two sorted lists when the second one is reversed. See [bitonic merger](/bitonic-merger/).
- **Counting networks.** The same wiring, with balancers instead of comparators, gives the [bitonic counting network](/bitonic-counting-network/).

## When to use it

Use bitonic sort on hardware that runs many equal operations at the same time: SIMD registers, GPUs and sorting circuits. Use it for small fixed sizes, for example to sort 8 or 16 numbers in registers without branches. Use it when the order of memory accesses must not depend on the data. On a single processor, [merge sort](/merge-sort/) or quicksort is faster for large $n$, because they do $O(n \log n)$ work.

## Pitfalls

- **A sequence that is not bitonic.** HALF-CLEANERS sorts only bitonic inputs. Two sorted halves in the same direction are not bitonic in general, so they need the flip of line L5 or a reversed half.
- **$n$ not a power of 2.** The recursion of lines L2 and L9 needs even lengths. Pad to a power of 2 with $+\infty$, or drop the comparators on the extra wires.
- **Counting the cost.** Bitonic sort makes $\Theta(n \log^2 n)$ comparisons, not $\Theta(n \log n)$. On one processor it is slower than a good sequential sort.
- **Branches.** On SIMD hardware use the minimum and the maximum instructions, not a test and an exchange.

## Implementations

## History

Kenneth Batcher described the bitonic sorter and the odd-even merge sorter in "Sorting networks and their applications" at the 1968 Spring Joint Computer Conference. Both networks have depth $\tfrac12 \lg n (\lg n + 1)$.

## References
