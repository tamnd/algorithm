---
tag: PC1TJR
kind: algorithm
slug: three-way-radix-quicksort
name: Three-way radix quicksort
aliases:
- Sorting equal keys
area: sorting/distribution-sorts
level: core
summary: String sort that partitions on the leading character into three parts and recurses, combining quicksort and most-significant-digit radix sort.
solves: [string-sorting]
model: word-ram
complexity:
  vars: {n: the number of strings, D: the total length of the distinguishing prefixes, σ: the alphabet size}
  time: {worst: "O(min(n, σ) · (n + D))", average: O(n log n + D), best: Θ(n + D)}
  space: {extra: O(n)}
properties: {stable: false, in_place: true, adaptive: true, online: false, deterministic: false, comparison: false, recursive: true}
history: {year: 1997, people: [Jon L. Bentley, Robert Sedgewick], note: three-way partitioning on one character with recursion on the next}
prereqs: [three-way-quicksort, msd-radix-sort, string-sorting]
see_also: [multikey-quicksort, msd-radix-sort, three-way-quicksort, insertion-sort, ternary-search-tree, dutch-national-flag-algorithm, american-flag-sort, string-sorting]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.1, String Sorts, subsection Three-way string quicksort (Algorithm 5.3, the cutoff to insertion sort, randomization, and the proposition of about 2 n ln n character compares for random strings)
  - paper: Jon L. Bentley and Robert Sedgewick, Fast algorithms for sorting and searching strings, Proceedings of the Eighth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1997, pages 360 to 369
    locator: the description of multikey quicksort (the same method), and the bound in terms of n log n plus the total length of the distinguishing prefixes
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by Exchanging (quicksort and the treatment of keys equal to the pivot)
---

Three-way radix quicksort is a string sort that partitions a range of strings into three parts by the character at the current index $d$, less than, equal to and greater than the character of a pivot string, then sorts the two outer parts at index $d$ and the middle part at index $d + 1$. It is the same method as [multikey quicksort](/multikey-quicksort/), written as in Sedgewick and Wayne: one shuffle at the start, the first string of a range as pivot, recursion on the outer parts, a loop on the middle part, and a cut-off to [insertion sort](/insertion-sort/) for small ranges. It combines [three-way quicksort](/three-way-quicksort/), which handles many equal keys, with [MSD radix sort](/msd-radix-sort/), which never looks again at a character that all strings of a range share. On $n$ random strings it makes about $2 n \ln n$ character compares in expectation.

## In plain words

Think of quicksort, but for words, and one letter at a time. Take the first word of the pile and look at its first letter. Make three piles: words whose first letter comes earlier, words with the same first letter, and words whose first letter comes later. Sort the first and the last pile the same way. In the middle pile all words share the first letter, so sort that pile by the second letter.

Very small piles are faster to sort by hand, one word at a time, so the method stops splitting when a pile is small. To avoid a bad pile order, such as words that are already sorted, it mixes the words at random once before it starts.

## The problem

The input is an array $A[0 \ldots n-1]$ of strings over an ordered alphabet. The output is the strings in [lexicographic order](/lexicographic-order/), with a proper prefix before the longer string. This is the [string sorting](/string-sorting/) problem. Let $c(s, d) = s[d]$ if $d < |s|$, and $c(s, d) = -1$ if $d \ge |s|$, where $-1$ is less than every character.

## The algorithm

The first call is THREE-WAY-RADIX-QUICKSORT$(A, 0, n, 0)$ after a random shuffle of $A$. $M \ge 1$ is the cut-off size.

```pseudo id=main
THREE-WAY-RADIX-QUICKSORT(A, lo, hi, d)     ▷ sorts A[lo .. hi − 1]; all agree on d characters
L1  while hi − lo > M do
L2      v ← c(A[lo], d)
L3      lt ← lo; gt ← hi − 1; i ← lo + 1
L4      while i ≤ gt do
L5          t ← c(A[i], d)
L6          if t < v then swap A[lt] and A[i]; lt ← lt + 1; i ← i + 1
L7          else if t > v then swap A[i] and A[gt]; gt ← gt − 1
L8          else i ← i + 1
L9      THREE-WAY-RADIX-QUICKSORT(A, lo, lt, d)
L10     THREE-WAY-RADIX-QUICKSORT(A, gt + 1, hi, d)
L11     if v = −1 then return
L12     (lo, hi, d) ← (lt, gt + 1, d + 1)
L13 INSERTION-SORT(A, lo, hi, d)        ▷ compares the strings from index d on
```

Lines L3 to L8 are Dijkstra's three-way partition, as in the [Dutch national flag algorithm](/dutch-national-flag-algorithm/). They keep $c(\cdot, d) < v$ in $A[lo \ldots lt-1]$, $= v$ in $A[lt \ldots i-1]$, and $> v$ in $A[gt+1 \ldots hi-1]$. The pivot string $A[lo]$ starts in the equal part. After the scan, line L12 replaces the call on the middle part by one more turn of the loop, so the call stack does not grow with the length of common prefixes. If $v = -1$, the middle part holds strings that end at $d$, which are all equal, and line L11 stops.

## Example

Sort $A = [\text{cab}, \text{add}, \text{dad}, \text{bad}, \text{cad}, \text{ace}, \text{ad}]$ with $M = 1$ and, for the trace, no shuffle. Each row is one partition, in the order in which the calls make them.

| $(lo, hi, d)$ | pivot $v$ | less | equal | greater |
|---|---|---|---|---|
| $(0, 7, 0)$ | c | add ad bad ace | cad cab | dad |
| $(0, 4, 0)$ | a | none | add ad ace | bad |
| $(0, 3, 1)$ | d | ace | ad add | none |
| $(1, 3, 2)$ | end | none | ad | add |
| $(4, 6, 1)$ | a | none | cad cab | none |
| $(4, 6, 2)$ | d | cab | cad | none |

The result is $[\text{ace}, \text{ad}, \text{add}, \text{bad}, \text{cab}, \text{cad}, \text{dad}]$. Row $(1, 3, 2)$ shows a short string: ad has ended at $d = 2$, so its value $-1$ is the pivot, ad is final, and add goes to the greater part. Row $(4, 6, 1)$ is a step in which all strings share the character, so the range moves to $d = 2$ without a split.

## Correctness

Each range that a call or a turn of the loop handles holds strings that agree on their first $d$ characters. A partition on $c(\cdot, d)$ then puts the three parts in the right order, because two such strings compare as their characters at $d$, with $-1$ first. The two outer parts still agree on $d$ characters, and the middle part agrees on $d + 1$ characters, unless all of its strings ended, in which case they are equal. Insertion sort from index $d$ sorts a small range correctly, because the first $d$ characters are equal. Each turn of the loop either shrinks the range or increases $d$, and $d$ is at most the length of the longest string, so the method ends. The full proof is below.

## Complexity

- **Random strings.** For $n$ random strings, Sedgewick and Wayne show about $2 n \ln n \approx 1.39\, n \lg n$ character compares in expectation, the same count as the key compares of quicksort with distinct keys. The strings differ early, so most of the work is at small $d$.
- **General input.** After a random shuffle, the expected number of character reads is $O(n \log n + D)$, where $D$ is the total length of the distinguishing prefixes; the argument is the one of [multikey quicksort](/multikey-quicksort/). This matches the $\Omega(D + n \log n)$ lower bound of [string sorting](/string-sorting/) over a comparison alphabet.
- **Long common prefixes.** A set of strings that share a prefix of length $L$ costs $O(nL)$ for the prefix, one scan per character, and no extra $\log n$ factor. A comparison sort would read the prefix in each of its $\Theta(n \log n)$ compares.
- **Worst case.** With bad pivots, a run at one index costs as much as quicksort, so the worst case is $O(\min(n, \sigma) \cdot (n + D))$, for example $\Theta(n^2)$ for $n$ distinct characters in sorted order without the shuffle.
- **Space.** The partition is in place. The calls of lines L9 and L10 use the call stack. Sedgewick and Wayne list the extra space as about $\log n + W$, where $W$ is the length of the longest string; the loop of line L12 removes the calls for the middle parts. In the worst case the depth is $O(n)$.

## Properties

- **Not stable.** The swaps of the partition reorder strings with satellite data.
- **In place.** Apart from the call stack.
- **Character comparisons only.** Characters are never array indices, so a large alphabet costs nothing extra, unlike in MSD radix sort, where each range pays for $\sigma$ counters.
- **Randomized.** The shuffle protects against bad orders such as sorted input. Without it the method is deterministic but slow on such inputs.
- **Good for equal keys.** Many equal strings move to the middle part at each step. In the extreme case of $n$ copies of one string of length $L$, the cost is $\Theta(nL)$.

## Variants and improvements

- **Cut-off.** Sedgewick and Wayne use insertion sort for ranges of at most about 15 strings. The best value depends on the machine.
- **Pivot choice.** A random pivot index in place of the shuffle, or the median of three sampled characters, gives the same guarantees and often better splits.
- **[Multikey quicksort](/multikey-quicksort/).** The form of Bentley and Sedgewick, with a random pivot and an explicit stack, and the link to [ternary search trees](/ternary-search-tree/).
- **Caching characters.** Storing $c(A[i], d)$ in a small array for the range before the partition reduces cache misses when the strings are far apart in memory.
- **Integers.** For integer keys, the same scheme with 8-bit or 16-bit digits gives a radix quicksort; with 1-bit digits and two parts it becomes [radix exchange sort](/radix-exchange-sort/).

## When to use it

Use it as a general string sort when the alphabet is large, when many strings share long prefixes, or when many strings are equal, such as keys from log files, URLs or file paths. It is in place and needs no tuning of a radix. For byte strings that differ in the first few characters, [MSD radix sort](/msd-radix-sort/) can be faster, and for huge sets [burstsort](/burstsort/) uses the cache better. If stability is needed, use MSD radix sort.

## Pitfalls

- **Recursing on the ended strings.** The middle part for $v = -1$ holds strings that ended. Sorting it at $d + 1$ never changes the range, so the loop must stop there, as in line L11.
- **Advancing $d$ in the outer parts.** The less and greater parts agree only on $d$ characters. They must be sorted at the same $d$, as lines L9 and L10 do.
- **Insertion sort from index 0.** The cut-off sort can start at index $d$, because the first $d$ characters are equal. Starting from 0 is correct but reads the common prefix again for each compare.
- **No shuffle.** With the first string as pivot, sorted or reverse sorted input gives quadratic time and a call depth of $n$.

## Implementations

## History

Three-way partitioning comes from Dijkstra's Dutch national flag problem and from work on quicksort with equal keys; Sedgewick analysed quicksort with equal keys in the 1970s. Bentley and Sedgewick (1997) combined it with sorting by one character at a time and called the result multikey quicksort. Sedgewick and Wayne present the same method as three-way string quicksort, with the cut-off and the shuffle shown here.

## References
