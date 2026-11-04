---
tag: 302WGD
kind: algorithm
slug: dutch-national-flag-algorithm
name: Dijkstra's three-way partition
aliases:
- Dijkstra three-way partition
area: techniques/two-pointers-and-windows
level: intro
summary: Maintain low, mid and high pointers so the array is split into less-than, equal and greater-than regions in one pass.
solves: [dutch-national-flag]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [dutch-national-flag, two-pointers, loop-invariant]
see_also: [dutch-national-flag, three-way-quicksort, bentley-mcilroy-partitioning, hoare-partition, lomuto-partition, partition-around-pivot, counting-sort, guarded-commands]
sources:
  - book: isbn:9780132158718
    title: Edsger W. Dijkstra, A Discipline of Programming, Prentice-Hall, 1976
    locator: Chapter 14, The problem of the Dutch national flag
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (3-way partitioning)
  - paper: doi:10.1002/spe.4380231105
    title: Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software Practice and Experience 23(11), 1993
    locator: the split-end three-way partition and its comparison with the Dutch national flag partition
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 11, Sorting (partition loops and their invariants)
---

Dijkstra's three-way partition rearranges an array in place around a pivot value $p$, so that all items less than $p$ come first, then all items equal to $p$, then all items greater than $p$. It keeps three indices $lo$, $mid$ and $hi$ that split the array into four regions, and it looks at each item exactly once. It solves the [Dutch national flag problem](/dutch-national-flag/) in exactly $n$ iterations and $O(1)$ extra space. Its loop invariant is the model for in-place partition loops, and it is the partition step of [three-way quicksort](/three-way-quicksort/).

## In plain words

Think of a row of red, white and blue balls. You want red on the left, white in the middle and blue on the right, and you may only look at a ball or swap two balls.

Keep three markers. Everything left of the first marker is red. Everything between the first and the second marker is white. Everything right of the third marker is blue. The balls between the second and the third marker are not looked at yet. Look at the ball at the second marker. If it is white, it is already in the right place: move the second marker on. If it is red, swap it with the first white ball and move the first two markers on. If it is blue, swap it with the last unknown ball and move the third marker back. Each step shrinks the unknown part by one ball.

## The problem

**Input.** An array $A[0 \ldots n-1]$ of items with a total order, and a pivot value $p$. The value $p$ need not occur in $A$.

**Output.** A permutation of $A$, in place, and two indices $lt \le gt$ such that $A[0 \ldots lt-1] < p$, $A[lt \ldots gt-1] = p$ and $A[gt \ldots n-1] > p$.

For the flag with colors 0, 1 and 2, take $p = 1$. Then the three output regions are the 0s, the 1s and the 2s, and the array is sorted.

## The algorithm

```pseudo id=main
THREE-WAY-PARTITION(A[0 .. n − 1], p)
L1  lo ← 0, mid ← 0, hi ← n − 1
L2  while mid ≤ hi do
L3      if A[mid] < p then
L4          swap A[lo] and A[mid]; lo ← lo + 1; mid ← mid + 1
L5      else if A[mid] > p then
L6          swap A[mid] and A[hi]; hi ← hi − 1
L7      else mid ← mid + 1
L8  return (lo, hi + 1)
```

The four regions, at each test of line L2:

| $A[0 \ldots lo-1]$ | $A[lo \ldots mid-1]$ | $A[mid \ldots hi]$ | $A[hi+1 \ldots n-1]$ |
| --- | --- | --- | --- |
| less than $p$ | equal to $p$ | not inspected | greater than $p$ |

Line L4 moves the item less than $p$ to the end of the first region. The item that was at $lo$ is the first item of the equal region, and it moves to the end of that region; if the equal region is empty, $lo = mid$ and the swap does nothing. Line L6 moves the item greater than $p$ to the front of the last region, and brings an item that was not inspected to position $mid$. So line L6 does not advance $mid$: the next iteration inspects the item that came from $hi$.

## Example

$A = [1, 2, 0, 1, 2, 0, 1]$ with $p = 1$, so $n = 7$. The table shows the state after each iteration.

| iter | $A[mid]$ before | line | $lo$ | $mid$ | $hi$ | $A$ after |
| --- | --- | --- | --- | --- | --- | --- |
| start | | | 0 | 0 | 6 | $[1, 2, 0, 1, 2, 0, 1]$ |
| 1 | 1 | L7 | 0 | 1 | 6 | $[1, 2, 0, 1, 2, 0, 1]$ |
| 2 | 2 | L6 | 0 | 1 | 5 | $[1, 1, 0, 1, 2, 0, 2]$ |
| 3 | 1 | L7 | 0 | 2 | 5 | $[1, 1, 0, 1, 2, 0, 2]$ |
| 4 | 0 | L4 | 1 | 3 | 5 | $[0, 1, 1, 1, 2, 0, 2]$ |
| 5 | 1 | L7 | 1 | 4 | 5 | $[0, 1, 1, 1, 2, 0, 2]$ |
| 6 | 2 | L6 | 1 | 4 | 4 | $[0, 1, 1, 1, 0, 2, 2]$ |
| 7 | 0 | L4 | 2 | 5 | 4 | $[0, 0, 1, 1, 1, 2, 2]$ |

The loop stops with $mid = 5 > hi = 4$ and returns $(lt, gt) = (2, 5)$. It ran $7 = n$ iterations and did 4 swaps, one for each item different from $p$. In iteration 4 the swap of line L4 moved the 0 to position 0 and the equal item from position 0 to position 2, the end of the equal region.

## Correctness

The loop keeps this invariant, at each test of line L2:

> **(F)** $0 \le lo \le mid \le hi + 1 \le n$; $A$ is a permutation of the input; $A[0 \ldots lo-1] < p$; $A[lo \ldots mid-1] = p$; $A[hi+1 \ldots n-1] > p$.

*Initialization.* Line L1 makes the first three regions empty and the unknown region the whole array.

*Maintenance.* Let $x = A[mid]$, with $mid \le hi$.

- *Line L4, $x < p$.* If $lo < mid$, then $A[lo] = p$ by (F). After the swap, $A[lo] = x < p$ and $A[mid] = p$. So with $lo + 1$ and $mid + 1$ the first region grows by one item less than $p$, and the equal region keeps its length and moves one step right. If $lo = mid$, the swap does nothing and both regions shift in the same way.
- *Line L6, $x > p$.* After the swap $A[hi] = x > p$, so with $hi - 1$ the last region grows by one item greater than $p$. The item now at $mid$ came from the unknown region, and $mid \le hi$ before the step means $mid \le (hi - 1) + 1$ after it, so it stays in the unknown region.
- *Line L7, $x = p$.* The equal region grows by one.

Swaps keep $A$ a permutation, and the bounds of (F) hold in each case.

*Why no item ends in the wrong region.* The only items that change regions are the item at $mid$, which is placed by its own value, and, in line L4, an equal item that moves from the front to the back of the equal region. No item leaves the unknown region without a test. In particular, line L6 does not advance $mid$, so the item brought from $hi$ is tested in the next iteration.

*Termination.* Let $u = hi - mid + 1$, the size of the unknown region. It starts at $n$, and each line L4, L6 and L7 decreases it by exactly 1. So the loop runs exactly $n$ times and stops with $u = 0$, that is $mid = hi + 1$. Then (F) says that $A[0 \ldots lo-1] < p$, $A[lo \ldots hi] = p$ and $A[hi+1 \ldots n-1] > p$, which is the output with $lt = lo$ and $gt = hi + 1$. The [proof page](proofs/correctness.md) gives the details.

## Complexity

- **Iterations.** Exactly $n$, by the variant $u$. Each item is inspected once, when it is at $mid$.
- **Comparisons.** At most 2 per iteration, so at most $2n$. An item less than $p$ uses 1; an item equal to or greater than $p$ uses 2. With a three-way compare it is 1 per iteration.
- **Swaps.** Exactly one swap for each item less than $p$ and one for each item greater than $p$, so $n_< + n_>$ swaps, at most $n$. Some of the swaps of line L4 are of an item with itself; a test $lo \ne mid$ skips them.
- **Space.** Three indices.

| measure | worst | best |
| --- | --- | --- |
| iterations | $n$ | $n$ |
| comparisons, two-way | $2n$ | $n$ (all items less than $p$) |
| swaps | $n$ | $0$ (all items equal to $p$) |

## Properties

- **In place.** $O(1)$ extra space.
- **Not stable.** Line L6 can move a greater item past equal items, and line L4 moves equal items. On $[2_a, 2_b, 1]$ with $p = 1$, the output is $[1, 2_b, 2_a]$.
- **Not adaptive.** An array that is already partitioned still takes $n$ iterations, and still has swaps: on $[0, 1, 2, 2]$ with $p = 1$ line L6 swaps the two 2s.
- **One pass, one inspection per item.** No item is compared with $p$ more than once.

## Variants and improvements

- **Bentley and McIlroy partition.** Keep the items equal to $p$ at both ends during the scan, and swap them to the middle at the end. When few items equal $p$, this does fewer swaps than the Dutch flag loop, which is why it is used in library sorts. See [Bentley-McIlroy partitioning](/bentley-mcilroy-partitioning/).
- **Mirror form.** Scan from the right with $mid$ moving down, so that the unknown region is between the less-than region and the equal region.
- **Two values.** With only two classes the loop is the ordinary [partition around a pivot](/partition-around-pivot/), as in [Lomuto](/lomuto-partition/) or [Hoare](/hoare-partition/) partition.
- **More than three values.** For $k$ colors, use $k - 1$ boundaries; or count the items of each color and rewrite the array, as in [counting sort](/counting-sort/), which takes two passes. For $k = 4$ the same four-pointer scheme with two unknown boundaries works but needs more care.
- **Three-way quicksort.** Partition around a pivot, then recurse on the less-than and greater-than regions only. The equal region is done, which makes the sort fast on inputs with many equal keys. See [three-way quicksort](/three-way-quicksort/).

## When to use it

Use it to sort an array of three values, to partition around a pivot when many items may equal the pivot, or to separate items into three classes by a test, in place and in one pass. When stability matters, use a counting pass and a second array instead.

## Pitfalls

- **Advancing $mid$ after line L6.** The item that comes from $hi$ is not inspected yet. If $mid$ moves on, this item stays in the equal region without a test. On $[1, 2, 0]$ with $p = 1$, the wrong loop passes the 1, swaps the 2 with the 0, moves $mid$ past the 0 and stops with $[1, 0, 2]$.
- **Loop test $mid < hi$.** The item at $mid = hi$ is still unknown and must be tested. With $mid < hi$, the input $[1, 0]$ ends after one iteration, before the 0 is inspected, and returns $[1, 0]$.
- **Unsigned $hi$.** With $n = 0$, $hi = -1$; in an unsigned type this wraps around. Use signed indices, or keep $hi$ one past the unknown region.
- **Pivot from the array by position.** If the pivot is read as $A[k]$ during the loop, the swaps can move it. Copy the pivot value first.

## Implementations

## History

Edsger Dijkstra posed the problem and gave this solution in Chapter 14 of *A Discipline of Programming* (1976), where he used it to show how a program follows from its invariant. Bentley and McIlroy (1993) studied three-way partitions for library sort functions and proposed their split-end scheme, which makes fewer swaps. Sedgewick's teaching of quicksort with three-way partitioning uses Dijkstra's loop.

## References
