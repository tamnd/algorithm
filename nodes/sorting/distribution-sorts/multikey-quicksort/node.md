---
tag: 36KMJW
kind: algorithm
slug: multikey-quicksort
name: Multikey quicksort
aliases:
- Three-way radix quicksort
- Ternary string quicksort
area: sorting/distribution-sorts
level: core
summary: Three-way quicksort on the current character of each string, recursing on the next character for equal keys.
solves: [string-sorting]
model: word-ram
complexity:
  vars: {n: the number of strings, D: the total length of the distinguishing prefixes, σ: the alphabet size}
  time: {worst: "O(min(n, σ) · (n + D))", average: O(n log n + D), best: Θ(n + D)}
  space: {extra: O(n)}
properties: {stable: false, in_place: true, adaptive: true, online: false, deterministic: false, comparison: false, recursive: true}
history: {year: 1997, people: [Jon L. Bentley, Robert Sedgewick], note: multikey quicksort and its link to ternary search trees}
prereqs: [quicksort, msd-radix-sort, string-sorting]
see_also: [three-way-radix-quicksort, three-way-quicksort, ternary-search-tree, msd-radix-sort, american-flag-sort, burstsort, dutch-national-flag-algorithm, string-sorting]
sources:
  - paper: Jon L. Bentley and Robert Sedgewick, Fast algorithms for sorting and searching strings, Proceedings of the Eighth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1997, pages 360 to 369
    locator: the description of multikey quicksort, its correspondence with ternary search trees, and the bound in terms of n log n plus the total length of the distinguishing prefixes
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.1, String Sorts, subsection Three-way string quicksort (Algorithm 5.3) and its performance analysis
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by Exchanging (quicksort and radix exchange sort, the two methods that multikey quicksort combines)
---

Multikey quicksort sorts strings by a three-way [quicksort](/quicksort/) partition on one character at a time: it picks a pivot character at position $d$, splits the strings into those whose character at $d$ is less, equal or greater, and sorts the equal part on position $d + 1$. Bentley and Sedgewick (1997) introduced it and showed that it makes $O(n \log n + D)$ character comparisons in expectation, where $D$ is the total length of the distinguishing prefixes, which matches the lower bound for [string sorting](/string-sorting/). It needs only comparisons of characters, works in place, and its recursion has the shape of a [ternary search tree](/ternary-search-tree/).

## In plain words

You must put a pile of words in dictionary order. Pick one word at random and look at its first letter, say m. Split the pile into three: the words that start with a letter before m, the words that start with m, and the words that start with a letter after m. Sort the first and the last pile the same way, still by the first letter. In the middle pile all words start with m, so you can forget the first letter there and sort by the second letter.

This mixes two familiar ideas. Like quicksort, it splits around a random choice. Like a sort by first letter, then second letter, it never looks again at a letter that it already knows is the same for the whole pile. So it reads few letters of words that are very long but start in the same way.

## The problem

The input is an array $A[0 \ldots n-1]$ of strings over an alphabet with a total order. The output is the strings in [lexicographic order](/lexicographic-order/), with a proper prefix before the longer string. For a string $s$ and an index $d$, let $c(s, d)$ be the character $s[d]$ if $d < |s|$, and a special value $-1$ that is less than every character if $d \ge |s|$. Two strings with the same first $d$ characters compare as their values $c(\cdot, d)$, unless both are $-1$, in which case they are equal.

## The algorithm

A task $(lo, hi, d)$ means that the strings of $A[lo \ldots hi-1]$ agree on their first $d$ characters and must be sorted by the rest. An explicit stack holds the tasks.

```pseudo id=main
MULTIKEY-QUICKSORT(A, n)
L1  S ← a stack that holds the task (0, n, 0)
L2  while S is not empty do
L3      (lo, hi, d) ← pop S
L4      if hi − lo ≤ 1 then continue
L5      v ← c(A[r], d) for an index r chosen uniformly at random in [lo, hi)
L6      partition A[lo .. hi − 1] by c(·, d) into three ranges:
            A[lo .. lt − 1] < v, A[lt .. gt − 1] = v, A[gt .. hi − 1] > v
L7      push (gt, hi, d) onto S
L8      if v ≠ −1 then push (lt, gt, d + 1) onto S
L9      push (lo, lt, d) onto S
L10 return A
```

Line L6 is a three-way partition, as in the [Dutch national flag algorithm](/dutch-national-flag-algorithm/): one scan with three pointers and swaps, which reads $c(A[i], d)$ once for each $i$ of the range. If $v = -1$, the middle range holds strings that all end at $d$; they are equal to each other, so line L8 does not push them. The less and the greater ranges keep the same depth $d$, because their strings still agree only on $d$ characters.

## Example

Sort $A = [\text{she}, \text{sells}, \text{sea}, \text{shells}, \text{by}, \text{the}, \text{sea}, \text{shore}]$. Here, for a trace that is easy to follow, the pivot is the string at index $\lfloor (lo + hi)/2 \rfloor$, not a random one. Each row is a task with at least two strings, in the order of the pops.

| $(lo, hi, d)$ | pivot $v$ | less | equal | greater |
|---|---|---|---|---|
| $(0, 8, 0)$ | b | none | by | sea shells sells the sea shore she |
| $(1, 8, 0)$ | t | sea shells sells sea shore she | the | none |
| $(1, 7, 0)$ | s | none | sea shells sells sea shore she | none |
| $(1, 7, 1)$ | e | none | sea sea sells | shore she shells |
| $(1, 4, 2)$ | a | none | sea sea | sells |
| $(1, 3, 3)$ | end | none | sea sea | none |
| $(4, 7, 1)$ | h | none | shore she shells | none |
| $(4, 7, 2)$ | e | none | shells she | shore |
| $(4, 6, 3)$ | end | none | she | shells |

The result is $[\text{by}, \text{sea}, \text{sea}, \text{sells}, \text{she}, \text{shells}, \text{shore}, \text{the}]$, after 40 reads of a character or an end mark. The poor first pivot b puts almost all strings in one part, as in quicksort, and costs one extra pass over the range. Row $(1, 7, 0)$ shows the other case: all strings have the pivot character, and the task moves one character deeper at once.

## Correctness

Each task is valid: its strings agree on their first $d$ characters. A partition step keeps this property for its three parts, and it puts the parts in the correct order, because strings that agree on $d$ characters compare by their character at $d$. The equal part agrees on $d + 1$ characters, unless it consists of strings that ended, which are all equal. So, at each moment, two strings that are not in the same task are in lexicographic order, and when the stack is empty the array is sorted. The loop ends because each step either shrinks the range of a task or increases its depth, and the depth is at most the length of the longest string. The full proof is below.

## Complexity

The cost of a task with $m$ strings is $\Theta(m)$ for line L6. Charge each read of $c(s, d)$ in line L6 to the string $s$.

- **Equal reads.** A read that puts $s$ in the equal part moves $s$ to depth $d + 1$. A task with at least two strings at depth $d$ has strings that agree on $d$ characters, so $d \le \ell(s)$, where $\ell(s)$ is the length of the distinguishing prefix of $s$. So $s$ has at most $\ell(s) + 1$ equal reads, and all strings together have at most $n + D$.
- **Less and greater reads.** At a fixed depth $d$, the reads that put $s$ in the less or the greater part form a run of partition steps, as in one quicksort run on the characters at position $d$. With a random pivot, the expected number of such steps for $s$ is $O(\log m)$, where $m$ is the size of the task at depth $d$. Bentley and Sedgewick show that, with random pivots, the total number of these reads over all strings and depths is $O(n \log n)$ in expectation.
- **Expected time.** $O(n \log n + D)$. For $n$ random strings, Sedgewick and Wayne give about $2 n \ln n$ character compares.
- **Worst case.** At one depth, the less and greater steps for $s$ are at most $\min(n, \sigma)$, because each step removes at least the pivot value from the range of the task. So the worst case is $O(\min(n, \sigma) \cdot (n + D))$. With a bad pivot each time, $n$ distinct one-character strings cost $\Theta(n^2)$, as in quicksort.
- **Best case.** If all strings are distinct one-character strings and every pivot is a median, the cost is $\Theta(n \log n)$; if all strings are equal, each depth takes one step and the cost is $\Theta(n + D)$.
- **Space.** The partition is in place. If tasks with fewer than two strings are never pushed, the tasks on the stack have disjoint ranges of at least two strings each, so the stack holds at most $n/2$ tasks.

## Properties

- **Not stable.** The swaps of line L6 can reorder strings. Equal strings are identical, so this matters only when the strings carry satellite data.
- **In place.** Only the stack is extra.
- **Character comparisons only.** It never uses a character as an array index, so it works for any ordered alphabet, also a large one such as Unicode.
- **Randomized.** The pivot is random, and the expected bound holds for every input.
- **Adaptive.** It reads each string only up to its distinguishing prefix, plus the less and greater steps.

## Variants and improvements

- **[Three-way radix quicksort](/three-way-radix-quicksort/).** The form in Sedgewick and Wayne: shuffle the input once, use the first string of the range as the pivot, recurse, and switch to [insertion sort](/insertion-sort/) on small ranges.
- **Median-of-three pivots.** A median of three or nine sampled characters gives more even splits, as in practical quicksort.
- **Split-end partition.** Bentley and Sedgewick use the partition of Bentley and McIlroy, which keeps the equal keys at the two ends during the scan and swaps them to the middle at the end. It makes fewer swaps when few keys are equal to the pivot.
- **Ternary search trees.** If each partition step stores its pivot in a node, with links to the less, equal and greater parts, the recursion builds a [ternary search tree](/ternary-search-tree/) of the strings. The same analysis gives the cost of search and insert in that tree.
- **Caching the character.** Reading $c(s, d)$ through a pointer to the string costs a cache miss for each read. Copying the current characters into a small array before the partition, as in later engineered versions, makes the scan faster.

## When to use it

Use multikey quicksort for strings with a large alphabet or with long common prefixes, when an in-place sort is wanted. It is a good default for general string keys, because it needs no count arrays and adapts to the data. For byte strings with many distinct first characters, [MSD radix sort](/msd-radix-sort/) or [American flag sort](/american-flag-sort/) can be faster; for very large sets, [burstsort](/burstsort/) uses the cache better.

## Pitfalls

- **Pushing the ended strings.** If line L8 pushes the equal part also when $v = -1$, the task never changes, since its strings have no character at $d + 1$, and the loop does not end.
- **Advancing the depth in the less or greater part.** These parts agree only on $d$ characters. Sorting them at depth $d + 1$ gives a wrong order.
- **A fixed pivot position.** Always taking the first string of the range as the pivot makes sorted input cost $\Theta(n^2)$ comparisons. Use a random pivot or shuffle the input first.
- **Deep recursion.** A recursive version goes one level deeper for each common character, so a set of long equal strings can overflow the call stack. An explicit stack, or a loop for the equal part, avoids this.

## Implementations

## History

Bentley and Sedgewick presented multikey quicksort at SODA 1997, together with ternary search trees, and showed that the two are the same recursion. They traced the idea of a three-way split on one character back to earlier work on radix sorting; Knuth (Section 5.2.2) describes quicksort and radix exchange sort, the two methods that it combines. Sedgewick and Wayne present it as three-way string quicksort.

## References
