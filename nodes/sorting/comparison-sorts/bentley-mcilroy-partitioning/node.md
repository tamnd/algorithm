---
tag: 39BDBS
kind: technique
slug: bentley-mcilroy-partitioning
name: Bentley-McIlroy three-way partitioning
aliases:
- fast three-way partitioning
- split-end partitioning
area: sorting/comparison-sorts
level: core
summary: A quicksort partitioning scheme that moves keys equal to the pivot to the ends and then swaps them to the middle.
prereqs: [hoare-partition, partition-around-pivot, quicksort]
see_also: [three-way-quicksort, dutch-national-flag, lomuto-partition, multikey-quicksort, dual-pivot-quicksort, java-system-sort, shannon-entropy]
sources:
  - paper: doi:10.1002/spe.4380231105
    title: Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software Practice and Experience 23(11) (1993)
    locator: pp. 1249 to 1265 (the split-end partition, with the keys equal to the pivot kept at the two ends and swapped to the middle)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (three-way partitioning, and the exercise on fast three-way partitioning by Bentley and McIlroy)
---

Bentley-McIlroy partitioning splits a range of an array into three parts, the keys less than a pivot $v$, the keys equal to $v$, and the keys greater than $v$, with the two scans of the [Hoare partition](/hoare-partition/). While the scans run, each key equal to $v$ that a scan meets is moved to the near end of the range. When the scans cross, the two blocks of equal keys are exchanged into the middle. On distinct keys it makes the same exchanges as Hoare's scheme, and on keys with many duplicates it makes [three-way quicksort](/three-way-quicksort/) linear on equal keys. Bentley and McIlroy used it in their sort function of 1993, which became the model of several library sorts.

## In plain words

Plain quicksort splits a range into small and large items. When many items equal the pivot, they end up on both sides, and the sort works on them again and again. A better split has three parts: small, equal and large. Then the equal items are done at once.

Bentley and McIlroy found a cheap way to make three parts. Scan from both ends, as in Hoare's method. Each time you meet an item equal to the pivot, move it out of the way, to the far left or the far right end. When the scans meet, the range looks like this: equal, small, large, equal. Then move the two blocks of equal items to the middle. If there are few equal items, this costs almost nothing extra.

## When it applies

- A [quicksort](/quicksort/) or [quickselect](/quickselect/) on keys that may have many duplicates, where the two parts of a two-way partition would both hold copies of the pivot.
- The keys are compared with a three-way comparison (less, equal or greater), so the test for equality costs no more than the test for less.
- The cost of exchanges matters: on distinct keys, the scheme makes no more exchanges than Hoare's partition, while [Dijkstra's three-way partition](/dutch-national-flag/) makes many more.

Signs that it does not apply: the keys are known to be distinct, so a two-way partition is simpler; or a three-way comparison is expensive, so each extra test for equality costs a full comparison.

## The template

The range is $A[lo \ldots hi]$ with $lo < hi$, and the pivot is $v = A[lo]$. The code is the form of Sedgewick and Wayne's exercise.

```pseudo id=main
BM-PARTITION(A, lo, hi)                     ▷ lo < hi, pivot v = A[lo]
L1  v ← A[lo]                               ▷ hole: the choice of the pivot, moved to A[lo]
L2  i ← lo, j ← hi + 1, p ← lo, q ← hi + 1
L3  loop
L4      repeat i ← i + 1 until A[i] ≥ v or i = hi
L5      repeat j ← j − 1 until A[j] ≤ v or j = lo
L6      if i = j and A[i] = v then p ← p + 1, exchange A[p] and A[i]
L7      if i ≥ j then leave the loop
L8      exchange A[i] and A[j]
L9      if A[i] = v then p ← p + 1, exchange A[p] and A[i]
L10     if A[j] = v then q ← q − 1, exchange A[q] and A[j]
L11 i ← j + 1
L12 for k ← lo to p do exchange A[k] and A[j], j ← j − 1
L13 for k ← hi downto q do exchange A[k] and A[i], i ← i + 1
L14 return (j, i)       ▷ A[lo..j] < v, A[j+1..i−1] = v, A[i..hi] > v
```

The holes are the choice of the pivot, and the comparison. Quicksort then calls itself on $A[lo \ldots j]$ and $A[i \ldots hi]$, and does not touch the middle part. The rules that make the template correct are these.

1. **The invariant of the scans.** At the test of line L4,
   $$A[lo \ldots p] = v, \quad A[p+1 \ldots i] < v, \quad A[j \ldots q-1] > v, \quad A[q \ldots hi] = v,$$
   with the convention that the first round has $i = p = lo$ and $j = q = hi + 1$. Lines L4 and L5 extend the middle two parts. After the exchange of line L8, $A[i] \le v$ and $A[j] \ge v$, and lines L9 and L10 move an equal key from $i$ to the left end block and from $j$ to the right end block, which keeps the invariant.
2. **The crossing.** When the scans cross ($i \ge j$), the range is: equal keys $A[lo \ldots p]$, smaller keys up to $j$, larger keys from $j + 1$, and equal keys $A[q \ldots hi]$. Line L6 handles the case where both scans stop at the same key equal to $v$, which belongs to neither the small nor the large part.
3. **The swap to the middle.** Line L12 exchanges the left block of equal keys with the last keys of the small part, and line L13 exchanges the right block with the first keys of the large part. Each block is exchanged as a whole, so the order of the keys inside each part does not matter.
4. **No run off the end.** The key $A[lo] = v$ does not move during the scans, so the scan of $j$ stops at $lo$ at the latest, and the test $j = lo$ is only a guard. The scan of $i$ has no such stop, so it needs the test $i = hi$.

**The cost.** On a range of $m$ keys, the scans make $m + O(1)$ comparisons of the form $A[i] < v$, and as many tests for equality. The exchanges are those of the Hoare scheme, plus at most one for each key equal to $v$ in lines L6, L9 and L10, plus one for each equal key in lines L12 and L13. So with $e$ keys equal to the pivot, there are at most $m/2 + 2e + O(1)$ exchanges. On distinct keys $e = 1$, and the extra work is the tests for equality.

**An example.** Partition $A = [3, 5, 3, 1, 3, 8, 2, 3, 7]$ with $v = 3$.

| step | what happens | the array |
|---|---|---|
| round 1 | $i = 1$ (5), $j = 7$ (3): exchange, then $A[1] = 3$ goes to the left block, $p = 1$ | 3 3 3 1 3 8 2 5 7 |
| round 2 | $i = 2$ (3), $j = 6$ (2): exchange, then $A[6] = 3$ goes to the right block, $q = 8$ | 3 3 2 1 3 8 7 5 3 |
| round 3 | $i = j = 4$ and $A[4] = 3$: it goes to the left block, $p = 2$; the scans have crossed | 3 3 3 1 2 8 7 5 3 |
| line L12 | the left block $A[0 \ldots 2]$ moves to $A[2 \ldots 4]$ | 2 1 3 3 3 8 7 5 3 |
| line L13 | the right block $A[8]$ moves to $A[5]$ | 2 1 3 3 3 3 7 5 8 |

The result is $(j, i) = (1, 6)$: the keys $A[0 \ldots 1] = [2, 1]$ are less than 3, $A[2 \ldots 5]$ are the four 3s, and $A[6 \ldots 8] = [7, 5, 8]$ are greater.

## Classic examples

- **[Three-way quicksort](/three-way-quicksort/).** Quicksort with this partition sorts an array of $n$ equal keys with one partition, in $\Theta(n)$ time. In a measurement with $n = 1000$, it made a mean of 10,852 comparisons with $A[i] < v$ on distinct keys, 3,428 on keys with 10 distinct values, and 1,000 on all-equal keys. Sedgewick and Wayne show that quicksort with a three-way partition makes a number of comparisons within a constant factor of $n H$, where $H$ is the [Shannon entropy](/shannon-entropy/) of the frequencies of the keys.
- **The sort of Bentley and McIlroy.** Their `qsort` for C of 1993 combines this partition with a pseudomedian of nine as the pivot and insertion sort for small ranges. The `qsort` of several C libraries comes from it.
- **[Java system sort](/java-system-sort/).** The sort of arrays of primitive types in Java up to version 6 was a tuned quicksort adapted from the paper of Bentley and McIlroy, with this partition.
- **[Multikey quicksort](/multikey-quicksort/).** Bentley and Sedgewick's sort for strings makes a three-way partition on one character at a time, and the equal part goes on to the next character. A three-way partition is essential there, because many strings share their first characters.

## Variations

- **[Dijkstra's three-way partition](/dutch-national-flag/).** One scan from the left with three indices $lt$, $i$ and $gt$ keeps the parts less, equal and greater in their final places at each step. It is simpler, but on distinct keys it makes about $m$ exchanges, against about $m/6$ for the Hoare scans on random input.
- **[Dual-pivot quicksort](/dual-pivot-quicksort/).** Partition around two pivots into three parts by value. With $p < q$, the middle part holds the keys between them, not the keys equal to a pivot. Yaroslavskiy's version in Java 7 also groups the keys equal to the pivots.
- **A block swap with fewer exchanges.** Lines L12 and L13 can exchange only $\min(p - lo + 1, j - p)$ pairs on the left, as in the original code of Bentley and McIlroy, which uses a vector swap of the shorter length.
- **[Lomuto](/lomuto-partition/) with a fat pivot.** A Lomuto scan can also keep a block of equal keys, but it inherits the many exchanges of the Lomuto scheme.

## Pitfalls

- **A range of one key.** Line L4 reads $A[lo + 1]$ before it tests $i = hi$, so the code needs $lo < hi$. Quicksort must not call it on a range of one key.
- **Forgetting line L6.** If both scans stop at the same key equal to $v$, that key must go to an end block. Without line L6 it stays at $A[j]$, which then is the last key of the small part, and the small part holds a key equal to $v$. The sort is still correct, but the claim of three parts is false.
- **Recursing on the wrong ranges.** After lines L12 and L13, the parts are $A[lo \ldots j]$ and $A[i \ldots hi]$ with the new $j$ and $i$, not the values at the crossing.
- **Tests for equality with a costly comparison.** With a comparison function that returns only "less", each test $A[i] = v$ needs a second call. Bentley and McIlroy assume a three-way comparison, as in C's `qsort`.

## Exercises

1. Partition $[2, 2, 2, 2]$ with the template. How many rounds are there, and what are $p$, $q$ and the result $(j, i)$? (Answer: round 1 has $i = 1$, $j = 3$, an exchange of two 2s, then $p = 1$ and $q = 3$. Round 2 has $i = j = 2$, so line L6 sets $p = 2$, and the loop ends with $j = 2$. Line L12 gives $j = -1$, and line L13 gives $i = 4$. The result is $(-1, 4)$: both outer parts are empty.)
2. Prove that on a range of distinct keys, the template makes exactly the exchanges of the Hoare partition with the pivot excluded from the scans, plus the one exchange that puts the pivot in the middle.
3. Show that three-way quicksort on an array with only $k$ distinct values has a recursion depth of at most $k$ for any choice of the pivots, and so runs in $O(nk)$ time. (Hint: each call removes the value of its pivot from both of its parts.)
4. Write the version of lines L12 and L13 that exchanges only $\min(s, t)$ pairs for two adjacent blocks of lengths $s$ and $t$, and prove that it gives the same three parts.

## References
