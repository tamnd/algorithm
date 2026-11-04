---
tag: 3RD7T8
kind: technique
slug: index-sort
name: Index sort
aliases:
- indirect sort
- argsort
- address table sorting
- pointer sorting
area: sorting/comparison-sorts
level: intro
summary: Sorts an array indirectly by producing an index permutation that lists the elements in order, leaving the original data unchanged.
prereqs: [permutation, comparison-sort, pointer]
see_also: [in-place-permutation, permutation-inverse, stable-sort, rank, suffix-array, cycle-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2, Internal sorting (the introduction, on address table sorting, list sorting and keysorting, and the exercises on rearranging records in place after an address table sort)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.5, Applications (pointer sorting, and sorting the same data by different keys)
---

Index sort sorts an array without moving its items. It makes an array of indices $P = [0, 1, \ldots, n-1]$ and sorts $P$ with any [comparison sort](/comparison-sort/), where index $i$ comes before index $j$ when $A[i] < A[j]$. The result is a [permutation](/permutation/) $P$ with $A[P[0]] \le A[P[1]] \le \cdots \le A[P[n-1]]$, and $A$ is unchanged. The technique is useful when the items are large, when the data must keep its order, when several orders of the same data are needed, and when a sort must become stable. Its cost is $n$ extra words and one indirection in each comparison.

## In plain words

A library does not put its books in a new order each time a reader wants them sorted by author, then by title, then by year. It keeps the books where they are and makes a card catalogue for each order. Each card names a shelf place. Sorting the cards is cheap, because cards are small, and the books never move.

Index sort does the same with an array. It sorts a list of positions instead of the items. To compare two positions, it looks at the items they point to. At the end, the list of positions tells you the items in order. If you need the items themselves in order, you can move each one once, at the end.

## When it applies

- The items are large, so a move of an item costs much more than a move of an index. A sort that moves items $\Theta(n \log n)$ times then moves only indices that many times.
- The original array must not change: other code holds positions into it, it is read-only, or it is shared.
- Several orders of the same data are needed at once, for example records by name and by date.
- The output that is needed is the order itself, or the [rank](/rank/) of each item, and not a sorted copy.
- A sort must be stable, but the only sort at hand is not.

Signs that it does not apply: the items are small numbers, so the indirection costs more than it saves; the indices do not fit the memory budget; or the order of the items is needed in memory for many later scans, where each indirect access is a cache miss.

## The template

```pseudo id=main
INDEX-SORT(A)
L1  P ← [0, 1, …, n − 1]
L2  SORT(P) with the order BEFORE                 ▷ hole: any comparison sort
L3  return P                                      ▷ A[P[0]] ≤ A[P[1]] ≤ … ≤ A[P[n − 1]]

BEFORE(i, j)                                      ▷ true when index i goes before index j
L4  if KEY(A[i]) < KEY(A[j]) then return true      ▷ hole: the key of an item
L5  if KEY(A[j]) < KEY(A[i]) then return false
L6  return i < j                                  ▷ ties by position: the result is stable

APPLY(A, P)                                       ▷ optional: put A itself in order, in place
L7  for s ← 0 to n − 1 do
L8      if P[s] ≠ s then
L9          t ← A[s], j ← s
L10         while P[j] ≠ s do
L11             k ← P[j], A[j] ← A[k], P[j] ← j, j ← k
L12         A[j] ← t, P[j] ← j
```

The holes are the sort of line L2 and the key of line L4. The rules that make the template correct are these.

1. **BEFORE is a strict total order on the indices.** Lines L4 to L6 compare the keys, and break ties by the index. Two different indices are never tied, so any comparison sort gives one well-defined permutation, the same for each sort. It lists equal keys in the order of their positions, so the result is stable even when the sort of line L2 is not.
2. **The sort moves only indices.** The items of $A$ are read in line L4 and never written by lines L1 to L6.
3. **APPLY follows the cycles of $P$.** The new value of $A[j]$ must be the old $A[P[j]]$. For each cycle $s \to P[s] \to P[P[s]] \to \cdots \to s$ of the permutation, line L9 saves $A[s]$, line L11 moves each item one step along the cycle, and line L12 writes the saved item at the end. Line L11 sets $P[j] \leftarrow j$, which marks the place as done, so the test of line L8 skips each cycle after its first visit. See [in-place permutation](/in-place-permutation/).

**The ranks.** The inverse permutation $R$, with $R[P[r]] = r$, gives the rank of each item: $R[i]$ is the number of items that go before $A[i]$. It takes one pass over $P$. See [permutation inverse](/permutation-inverse/).

**The cost.** Let the sort of line L2 make $C$ comparisons and $M$ moves. Index sort makes the same $C$ comparisons of keys, each through one indirection, and $M$ moves of one word each. APPLY makes $n - f + c$ moves of items, where $f$ is the number of fixed points of $P$ and $c$ is the number of cycles of length at least 2. This is at most $3n/2$. So with items of $w$ words, a direct sort that moves items $\Theta(n \log n)$ times moves $\Theta(w\, n \log n)$ words, and index sort with APPLY moves $\Theta(n \log n + w\, n)$ words. The extra memory is $n$ words for $P$, so the technique is not [in place](/in-place-algorithm/).

**An example.** Let $A = [\text{pear}, \text{fig}, \text{apple}, \text{fig}, \text{kiwi}]$. Index sort gives $P = [2, 1, 3, 4, 0]$: apple, fig at index 1, fig at index 3, kiwi, pear. The two figs keep their order. The ranks are $R = [4, 1, 0, 2, 3]$. The permutation has the cycle $0 \to 2 \to 3 \to 4 \to 0$ and the fixed point 1, so APPLY makes $5 - 1 + 1 = 5$ moves of items: $t \leftarrow$ pear, then apple to index 0, fig to index 2, kiwi to index 3, and pear to index 4.

## Classic examples

- **[Suffix array](/suffix-array/).** The suffix array of a string is the index sort of its suffixes: the indices $0, \ldots, n-1$ are sorted by the suffixes that start there. The suffixes are never copied.
- **Stable sorting with any sort.** [Quicksort](/quicksort/) and [heapsort](/heapsort/) are not [stable](/stable-sort/), but with the tie rule of line L6 they give a stable order.
- **Ranks and rank statistics.** The [rank](/rank/) of each item is the inverse of $P$. The [Kendall tau distance](/kendall-tau-distance/) of two orders of the same items counts the [inversions](/inversion/) of one rank array relative to the other.
- **Sorting large records.** Sedgewick and Wayne sort an array of references to objects, and so sort the objects by any of their fields without moving them. Knuth calls this address table sorting.
- **Indexes of a database.** A [B-tree](/b-tree/) index on a column lists the positions of the rows in the order of that column, and a table can have several such indexes. It is a dynamic form of the same idea.

## Variations

- **Key sorting.** Sort the pairs (key, index) instead of the indices. Each comparison then reads the key from the pair, not through the index, which gives better locality, at the cost of one copy of each key. This is the keysorting of Knuth.
- **Index sort with a distribution sort.** [Counting sort](/counting-sort/) and [radix sort](/radix-sort/) can sort the indices by the keys too. Counting sort over the indices is stable by its nature.
- **List sorting.** Instead of an array of indices, keep a link field in each record and sort by changing the links. The result is a linked list in sorted order.
- **Applying the permutation with extra memory.** With a second array $B$, set $B[r] \leftarrow A[P[r]]$ for each $r$. This makes $n$ moves and needs no work with cycles.
- **Applying the inverse.** If the ranks $R$ are known instead of $P$, move each item $A[i]$ to place $R[i]$ along the cycles of $R$. [Cycle sort](/cycle-sort/) computes each rank by counting, and then does this with the fewest writes.

## Pitfalls

- **Ties without the index.** Without line L6, an unstable sort can list equal keys in any order, and two runs of different sorts can give different $P$. Break ties by the index if the order of equal keys matters.
- **A comparison that is not an order.** BEFORE must compare the items, not the indices: "$i < j$" alone sorts nothing. And a key with a NaN, or a comparison that is not transitive, breaks the sort of the indices in the same way as a direct sort.
- **Applying $P$ the wrong way.** The new $A[j]$ is the old $A[P[j]]$. Moving $A[j]$ to place $P[j]$ instead applies the inverse permutation and gives a wrong order whenever $P$ is not its own inverse.
- **Losing $P$.** APPLY writes $P[j] \leftarrow j$, so after it $P$ is the identity. Copy $P$ first if the order is still needed.
- **Changing $A$ during the sort.** The order of $P$ is valid only for the values of $A$ at the time of the sort. An update of an item needs the index to be repaired, as a database does for its indexes.
- **Cache misses.** On a large array, each comparison reads two items at random places. For small items, sorting the items directly, or sorting (key, index) pairs, is faster.

## Exercises

1. Let $A = [30, 10, 20, 10]$. Give $P$ with the tie rule of line L6, and the ranks $R$. (Answer: $P = [1, 3, 2, 0]$ and $R = [3, 0, 2, 1]$.)
2. Prove that with the order BEFORE of lines L4 to L6, every correct comparison sort returns the same $P$, and that $P$ lists equal keys in the order of their positions.
3. How many moves of items does APPLY make for $P = [1, 2, 0, 4, 3]$? (Answer: the cycles are $0 \to 1 \to 2 \to 0$ and $3 \to 4 \to 3$, with no fixed point, so $5 - 0 + 2 = 7$.) Which permutations of $n$ items need the most moves, and how many?
4. A suffix array is built by index sort with [merge sort](/merge-sort/), and two suffixes are compared character by character. Show that on the string $a^n$ this takes $\Theta(n^2 \log n)$ time, even though the sort makes only $O(n \log n)$ comparisons.

## References
