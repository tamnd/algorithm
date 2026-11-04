---
tag: YVKHNF
kind: concept
slug: stable-sort
name: Stable sort
aliases:
- stability
area: sorting/comparison-sorts
level: core
summary: A sort that keeps the relative order of elements with equal keys.
prereqs: [sorting-problem]
see_also: [merge-sort, insertion-sort, multi-key-sorting, radix-sort, counting-sort, timsort, block-sort, quicksort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 5, Sorting (the introduction defines a stable sort)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.2, Counting sort (the definition of stability and why radix sort needs it), and Section 8.3, Radix sort
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.5, Applications (Stability, and the table of the properties of the sorts)
---

A sort is stable when items with equal keys keep the order that they had in the input. Stability matters when the items carry more data than the key, for example records that are sorted by one field. It is what makes a sort by several keys in turn work, and [LSD radix sort](/radix-sort/) depends on it. [Merge sort](/merge-sort/), [insertion sort](/insertion-sort/), [counting sort](/counting-sort/) and [Timsort](/timsort/) are stable; [quicksort](/quicksort/), [heapsort](/heapsort/) and [selection sort](/selection-sort/) are not.

## In plain words

A teacher has a list of students in the order that they handed in their tests. She sorts the list by grade. Several students have the same grade. A stable sort keeps these students in the order that they handed in: the first one to hand in is still first among them. An unstable sort can mix them up.

When only the grade matters, both sorts are equally good. But when the order of hand-in also matters, only the stable sort keeps it. It also lets you sort in two passes: sort by name first, then sort by grade with a stable sort. Within each grade, the names are then still in order.

## The idea

**The definition.** Let the input be $a_1, \ldots, a_n$, and let a sort output $a_{\pi(1)}, \ldots, a_{\pi(n)}$ for a [permutation](/permutation/) $\pi$. The sort is *stable* on this input when for all $i < j$ with $\mathrm{key}(a_{\pi(i)}) = \mathrm{key}(a_{\pi(j)})$, we have $\pi(i) < \pi(j)$. A sorting algorithm is stable when it is stable on each input. For a given input and key, the stable output is unique: it is the input order, sorted by key, with ties broken by the input position.

**An equivalent form.** Sorting stably by $\mathrm{key}$ is the same as sorting by the pair $(\mathrm{key}(a_i), i)$ in [lexicographic order](/lexicographic-order/). The pairs are all different, so this sort has only one correct output, and it is the stable output.

**When it matters.** Stability is a property of the output only when equal keys can belong to items that are different. If the items are plain numbers and the key is the number, each correct output is the same, and stability does not show.

**Why sorts lose it.** A sort is unstable when it can move an item past an equal item. Long-distance swaps do this. In [selection sort](/selection-sort/), the swap of the least item with the first unsorted item can jump that item over an equal item. In [quicksort](/quicksort/), the partition swaps items across the range. In [heapsort](/heapsort/), the heap mixes the order of equal items. A sort that only moves an item past items that are strictly larger or strictly smaller, as insertion sort does, keeps it.

**How sorts keep it.** In a merge, the rule "on a tie, take the item from the left run" keeps equal items in order. With "take the right item", the merge sort is still correct but not stable. In counting sort, the last pass reads the input from right to left and fills each bucket from its end, which keeps the order in each bucket.

**Making any sort stable.** Replace each item $a_i$ by the pair $(a_i, i)$, and compare the pairs by key first and by index on a tie. Then any correct sort gives the stable output. The cost is $\Theta(n)$ extra space for the indices, or $\lceil \lg n \rceil$ extra bits per item.

**The cost of stability.** A stable sort in $O(n \log n)$ time with $\Theta(n)$ extra space is easy: merge sort. A stable sort that is [in place](/in-place-algorithm/) and $O(n \log n)$ in the worst case also exists, for example [block sort](/block-sort/), but it is much more complex. So most libraries pay with memory: their stable sort is a merge sort that uses a buffer.

## Examples

Students in the order of hand-in, with their grades: (Dan, B), (Ann, A), (Eve, B), (Bob, A), (Cid, B). Sort by grade.

| sort | output |
|---|---|
| a stable sort (merge sort) | (Ann, A) (Bob, A) (Dan, B) (Eve, B) (Cid, B) |
| selection sort | (Ann, A) (Bob, A) (Eve, B) (Dan, B) (Cid, B) |
| quicksort with the Lomuto partition | (Ann, A) (Bob, A) (Eve, B) (Dan, B) (Cid, B) |

Both unstable sorts give a correct sorted output, but Eve now comes before Dan, although Dan handed in first. In selection sort, the first swap exchanges (Dan, B) and (Ann, A), so Dan jumps over Eve.

**Two passes.** Sort the same list by name: (Ann, A) (Bob, A) (Cid, B) (Dan, B) (Eve, B). Then sort this list by grade with a stable sort. The result is (Ann, A) (Bob, A) (Cid, B) (Dan, B) (Eve, B): by grade, and by name within a grade. This is the method of [multi-key sorting](/multi-key-sorting/): sort by the least important key first.

**The pair form.** The pairs (grade, position) of the input are (B, 0), (A, 1), (B, 2), (A, 3), (B, 4). Each correct sort of these pairs gives (A, 1), (A, 3), (B, 0), (B, 2), (B, 4), which is the stable output above.

**Non-example.** A sort that always outputs equal items in reverse input order is not stable, even though its output is fully determined. A sort that keeps the order on some inputs but not on all is also not stable: selection sort keeps the order on (1, a), (2, b), (2, c), but not on (2, a), (2, b), (1, c).

**The common sorts.**

| stable | not stable |
|---|---|
| [insertion sort](/insertion-sort/), [bubble sort](/bubble-sort/) | [selection sort](/selection-sort/) |
| [merge sort](/merge-sort/), [natural merge sort](/natural-merge-sort/), [Timsort](/timsort/) | [quicksort](/quicksort/), [introsort](/introsort/) |
| [counting sort](/counting-sort/), LSD [radix sort](/radix-sort/) | [heapsort](/heapsort/), [smoothsort](/smoothsort/) |
| [tree sort](/tree-sort/), when equal keys go right | [shell sort](/shell-sort/) |

## Where it is used

- **Multi-key sorting.** Sort by the secondary key, then by the primary key with a stable sort. Spreadsheets and tables that sort by a clicked column depend on this, so that an earlier sort survives in each group.
- **LSD radix sort.** Each pass sorts by one digit, from the least significant, with a stable counting sort. Without stability, a later pass destroys the order of the earlier ones.
- **Library sorts.** Python's `list.sort` and `sorted` are stable (they use Timsort), and so is Java's `Arrays.sort` for objects. C's `qsort` and C++'s `std::sort` are not guaranteed stable. C++ has `std::stable_sort` for this.
- **Databases and reports.** A report sorted by date and then grouped by customer keeps the dates in order in each group if the second sort is stable.
- **Deterministic output.** A stable sort gives the same output on the same input under any implementation, which makes tests and diffs stable.

## References
