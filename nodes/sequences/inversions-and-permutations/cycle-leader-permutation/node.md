---
tag: J8DYW4
kind: algorithm
slug: cycle-leader-permutation
name: Cycle-leader in-place permutation
aliases:
- in-place permutation by cycles
area: sequences/inversions-and-permutations
level: core
summary: Apply a permutation in O(n) time and O(1) extra space by following its cycles.
solves: [in-place-permutation]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
prereqs: [permutation-cycles, in-place-permutation]
see_also: [permutation-inverse, cycle-sort, index-sort, in-place-algorithm, scatter-and-gather, faro-shuffle, permutation-power, fisher-yates-shuffle]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2 (rearranging the records in place after an address table sort, by following the cycles of the permutation)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.3.3 (applications to permutations, including computing the inverse of a permutation in place by following its cycles)
  - paper: "Faith E. Fich, J. Ian Munro and Patricio V. Poblete, Permuting in place, SIAM Journal on Computing 24(2) (1995) 266-278"
    locator: rearranging an array by a read-only permutation with little extra space, and the cost of finding cycle leaders
---

The cycle-leader method rearranges an array $A$ in place so that the item at position $i$ moves to position $P[i]$, for a given [permutation](/permutation/) $P$. It walks each [cycle](/permutation-cycles/) of $P$ once, carrying one item in a temporary and dropping it into its target, which evicts the next item to carry. If the entries of $P$ can be marked, for example by negating them, the whole job takes $\Theta(n)$ time, exactly one write per position, and $O(1)$ extra words, and the marks are removed at the end. If $P$ is read-only, the method moves a cycle only from its smallest index, its leader, and finding the leaders costs $\Theta(n^2)$ time in the worst case and $(n+1)H_n - n$ steps on average.

## In plain words

Each item has a ticket that names its new seat. With a spare table you would just copy every item to its seat. Without one, pick up the first item and walk it to its seat. Someone is sitting there, so pick that one up and walk it to its own seat, and so on. After a few steps you come back to the empty first seat and the loop is closed. Every item on that loop is now in place.

Then look for an item that has not moved yet and do the same. To know which items have already moved, mark their tickets as you go, and clear the marks at the end. If the tickets may not be marked, start a loop only from its smallest seat number, which you can check by walking around the loop first. That check is slow for long loops.

## The problem

Given an array $A[1..n]$ and a permutation $P$ of $[n]$, rearrange $A$ so that afterwards $A'[P[i]] = A[i]$ for every $i$, using $O(1)$ extra words of memory. This is the scatter form of the [in-place permutation](/in-place-permutation/) problem. The gather form, $A'[i] = A[P[i]]$, is the scatter by the [inverse](/permutation-inverse/) $P^{-1}$, and the [variants](#variants-and-improvements) below treat it.

## The algorithm

**Following one cycle.** Start at an index $i$ and hold $x = A[i]$. Its target is $j = P[i]$. Exchange $x$ with $A[j]$: now $A[j]$ holds its final item, and $x$ holds the item that was at $j$, whose target is $P[j]$. Repeat until the target is $i$ again, and drop $x$ into $A[i]$. Every index on the cycle of $i$ is written once.

**Marking.** The values of $P$ are $1$ to $n$, so a negative entry is free to mean "this index is done". APPLY negates $P[j]$ when it fills $A[j]$, skips indices whose entry is negative, and negates every entry back at the end, so $P$ is unchanged afterwards.

**Leaders.** If $P$ may not be written, APPLY-READONLY starts a cycle only from its smallest index. Line L10 walks the cycle from $i$ until it reaches an index that is not larger than $i$. It stops at $i$ itself exactly when $i$ is the smallest index on its cycle.

```pseudo id=main
APPLY(A[1 .. n], P[1 .. n])                       ▷ move A[i] to position P[i], marking P
L1  for i ← 1 to n do
L2      if P[i] > 0 then                          ▷ the cycle of i is not done yet
L3          x ← A[i], j ← P[i]
L4          while j ≠ i do
L5              exchange x ↔ A[j]                 ▷ A[j] gets its final item
L6              k ← P[j], P[j] ← −P[j], j ← k     ▷ mark j, go to the target of x
L7          A[i] ← x, P[i] ← −P[i]
L8  for i ← 1 to n do P[i] ← −P[i]                ▷ restore P
L9  return A

APPLY-READONLY(A[1 .. n], P[1 .. n])              ▷ the same result, P is not written
L10 for i ← 1 to n do
L11     j ← P[i]; while j > i do j ← P[j]         ▷ walk until an index ≤ i
L12     if j = i then                             ▷ i is the leader of its cycle
L13         x ← A[i], j ← P[i]
L14         while j ≠ i do exchange x ↔ A[j], j ← P[j]
L15         A[i] ← x
L16 return A
```

## Example

Let $A = (\mathrm{A}, \mathrm{B}, \mathrm{C}, \mathrm{D}, \mathrm{E}, \mathrm{F})$ and $P = 3\,6\,4\,1\,5\,2$, whose cycles are $(1\,3\,4)$, $(2\,6)$ and $(5)$. The result must have $A'[P[i]] = A[i]$: $A'[3] = \mathrm{A}$, $A'[6] = \mathrm{B}$, $A'[4] = \mathrm{C}$, $A'[1] = \mathrm{D}$, $A'[5] = \mathrm{E}$, $A'[2] = \mathrm{F}$, so $A' = (\mathrm{D}, \mathrm{F}, \mathrm{A}, \mathrm{C}, \mathrm{E}, \mathrm{B})$.

| step | $j$ | $x$ after the step | $A$ after the step | $P$ after the step |
| --- | --- | --- | --- | --- |
| L3, $i = 1$ | 3 | A | A B C D E F | 3 6 4 1 5 2 |
| L5, L6 | 3, then 4 | C | A B **A** D E F | 3 6 −4 1 5 2 |
| L5, L6 | 4, then 1 | D | A B A **C** E F | 3 6 −4 −1 5 2 |
| L7 | 1 | | **D** B A C E F | −3 6 −4 −1 5 2 |
| L3, $i = 2$ | 6 | B | D B A C E F | −3 6 −4 −1 5 2 |
| L5, L6 | 6, then 2 | F | D B A C E **B** | −3 6 −4 −1 5 −2 |
| L7 | 2 | | D **F** A C E B | −3 −6 −4 −1 5 −2 |
| L7, $i = 5$ | 5 | | D F A C **E** B | −3 −6 −4 −1 −5 −2 |

Indices 3, 4 and 6 are skipped at line L2, and line L8 restores $P = 3\,6\,4\,1\,5\,2$. Each of the six positions was written once.

**The read-only version on the same input.** At $i = 1$ the walk of line L11 goes $3, 4, 1$ and stops at 1, so 1 is a leader. At $i = 2$ it goes $6, 2$, a leader. At $i = 3$ it goes $4, 1$ and stops at $1 \ne 3$, so 3 is not a leader, and the same happens for 4 and 6. At $i = 5$ the walk stops at once. In total line L11 reads $P$ 10 times.

## Correctness

APPLY keeps this invariant at line L4: the indices already filled on the current cycle hold their final items, $x$ holds the item that originally stood at the last index visited before $j$, and the target of that item is $j$. Line L5 puts $x$ at its target and picks up the original item of $j$, whose target is $P[j]$, so the invariant holds again after line L6. Since the cycle of $i$ is finite and returns to $i$, the loop ends with $x$ holding the original item of $P^{-1}(i)$, which line L7 drops at $i$. A negative entry marks exactly the indices of finished cycles, so no cycle is started twice and every cycle is started at its first index. For APPLY-READONLY, every cycle has exactly one smallest index and line L11 recognizes exactly that index, so every cycle is moved once. The [full proof](proofs/correctness.md) gives the details.

## Complexity

**APPLY.** Each index is visited once inside a cycle walk and once at line L2 and line L8, so the time is $\Theta(n)$. There are exactly $n$ writes into $A$, $n - c$ of them at line L5 and $c$ at line L7, where $c$ is the number of cycles, so the item moves are the fewest possible for moving each item directly to its place. The extra space is the three words $x$, $j$ and $k$, plus one bit per entry of $P$ borrowed from its sign.

**APPLY-READONLY.** The moves cost $\Theta(n)$ as before. Line L11 dominates: from index $i$ it walks until it meets an index not larger than $i$. For the single cycle $P = 2\,3 \cdots n\,1$ the walk from $i$ takes $n - i + 1$ steps, so the worst case is $n(n+1)/2 = \Theta(n^2)$ reads of $P$. Over a uniform random permutation the expected number of reads is $(n+1)H_n - n = \Theta(n \log n)$, where $H_n$ is the $n$-th harmonic number. The extra space is $O(1)$ words.

## Properties

- **In place.** $O(1)$ extra words, with or without the borrowed sign bits.
- **Minimal writes.** Each item is written once, into its final position. This matters when the items are large records or when writes are expensive.
- **Not stable in any useful sense.** The items are not compared, so stability does not apply; equal items simply go where $P$ says.
- **Touches memory in cycle order.** The accesses jump around the array, so for large arrays most of them are cache misses.
- **Restores $P$.** APPLY leaves $P$ as it found it, and APPLY-READONLY never writes it.

## Variants and improvements

- **Gather instead of scatter.** To get $A'[i] = A[P[i]]$, walk each cycle backwards: save $t = A[i]$, then repeatedly copy $A[j] \leftarrow A[P[j]]$ and move $j \leftarrow P[j]$ until $P[j] = i$, and finish with $A[j] \leftarrow t$. This uses copies instead of exchanges.
- **Inverting $P$ itself.** A cycle walk that writes $i$ into position $P[i]$, while reading the next index before overwriting it, turns $P$ into its [inverse](/permutation-inverse/) in place. Knuth gives such algorithms in the section on permutations.
- **Sign bits are not available.** If the items carry no free bit, a bit vector of $n$ bits does the marking. With fewer bits, the leader test of APPLY-READONLY can be sped up by walking both directions or by storing a few marked indices, and Fich, Munro and Poblete gave $O(n \log n)$ worst-case time with a polylogarithmic number of extra bits.
- **Structured permutations.** For a rotation of an array by $k$ places, the cycles are the $\gcd(n, k)$ residue classes and their leaders are the indices $1$ to $\gcd(n, k)$. For a [perfect shuffle](/faro-shuffle/), number theory gives the leaders of suitable blocks. In such cases no marks are needed.
- **Sorting by a key array.** After an [index sort](/index-sort/) produces the sorted order as a permutation, the cycle method moves the records into place with one write each. [Cycle sort](/cycle-sort/) does the same but computes each target by counting smaller items.

## When to use it

Use APPLY when memory is tight and the permutation array can be borrowed for a moment, for example to reorder large records after sorting their keys, to apply a precomputed relabeling in a graph or a mesh, or to permute rows of a matrix in place. Use APPLY-READONLY only when $P$ cannot be marked and $n$ is small or the cycles are known to be short. If a second array of size $n$ is affordable, a plain copy $B[P[i]] \leftarrow A[i]$ is simpler and touches memory in a better order.

## Pitfalls

- **Scatter or gather.** Applying $P$ when $P^{-1}$ was meant produces a different array whenever $P$ has a cycle longer than 2. Test with a 3-cycle.
- **Zero-based indices.** With values $0$ to $n-1$, the index 0 cannot be marked by negation. Use the complement $\sim P[j] = -P[j] - 1$ instead, which maps $0$ to $-1$.
- **Forgetting to restore.** Leaving $P$ negated breaks the caller's copy of the permutation. Line L8 restores it.
- **Invalid input.** If $P$ is not a permutation, for example with a repeated value, the walk of line L4 can loop forever. Validate $P$ when it comes from outside.
- **Read-only cost.** APPLY-READONLY looks linear but is quadratic on a single long cycle with the leader at the end of the walk.

## Implementations

## History

Rearranging records in place by following the cycles of a permutation is folklore of early sorting programs, where the keys were sorted through an address table and the records were then moved once each. Knuth describes it in the treatment of address table sorting and of computing the inverse of a permutation in place. Fich, Munro and Poblete studied in 1995 how much extra space is needed when the permutation is read-only.

## References
