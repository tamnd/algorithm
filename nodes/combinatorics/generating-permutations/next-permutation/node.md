---
tag: V6C3MR
kind: algorithm
slug: next-permutation
name: Next permutation
aliases:
- lexicographic next permutation
- next lexicographic permutation
- next_permutation
- Algorithm L
area: combinatorics/generating-permutations
level: intro
summary: Given a permutation, finds the next one in lexicographic order in O(n) time.
solves: [lexicographic-permutation-successor, generating-all-permutations, multiset-permutations]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n), best: Θ(1), amortized: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: true, recursive: false}
prereqs: [lexicographic-order, permutation, loop-invariant]
see_also: [lexicographic-permutation-successor, lexicographic-successor, generating-all-permutations, multiset-permutations, permutation-ranking, permutation-unranking, heaps-algorithm, steinhaus-johnson-trotter]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2, Algorithm L (lexicographic permutation generation, for distinct items and for multisets) and its history
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (permutations in lexicographic order, the successor algorithm)
  - paper: doi:10.1145/356689.356692
    title: Robert Sedgewick, Permutation generation methods, ACM Computing Surveys 9(2) (1977) 137-164
    locator: the discussion of lexicographic methods and their cost against exchange methods
---

Next permutation rearranges a sequence into the next larger arrangement of the same items in [lexicographic order](/lexicographic-order/), or reports that the sequence is the last one. It scans for the longest non-increasing suffix, exchanges the item just before it with the smallest larger item of the suffix, and reverses the suffix. One call takes $\Theta(n)$ time in the worst case and $\Theta(1)$ time amortized over a full listing of $n!$ distinct items. With repeated items it lists each distinct arrangement of a [multiset](/multiset-permutations/) once. It is Algorithm L of Knuth and the C++ library function `std::next_permutation`.

## In plain words

Think of a car odometer. To add one, you look at the digits at the right end that are already at their largest value. They cannot grow, so they go back to their smallest values, and the first digit to the left of them goes up by one step.

Next permutation does the same with an arrangement. At the right end, find the longest run that only goes down. That run is already at its largest order. The item just before the run must grow. Swap it with the smallest item in the run that is larger than it. The run still goes down after the swap. Turn the run around, so that it goes up. Now it is at its smallest order.

If the whole arrangement only goes down, it is the last one. The method then turns it around to get the first one again.

## The problem

The input is an array $A[0 \ldots n-1]$ of items from a [total order](/total-order/). Repeated items are allowed. Let $S(A)$ be the set of all distinct arrangements of the items of $A$, ordered lexicographically. The output is the least arrangement in $S(A)$ that is greater than $A$, written into $A$, together with the value true. If $A$ is the greatest arrangement, the output is the least arrangement, which is $A$ sorted in non-decreasing order, together with the value false. This is the [lexicographic successor problem](/lexicographic-permutation-successor/).

## The algorithm

The array is 0-based. The value false signals that the array was the last arrangement and is now the first one.

```pseudo id=main
NEXT-PERMUTATION(A, n)                      ▷ returns false when A was the last arrangement
L1  i ← n − 2
L2  while i ≥ 0 and A[i] ≥ A[i + 1] do i ← i − 1
L3  if i < 0 then
L4      reverse A[0 .. n − 1]               ▷ the last arrangement becomes the first
L5      return false
L6  j ← n − 1
L7  while A[j] ≤ A[i] do j ← j − 1
L8  exchange A[i] and A[j]
L9  reverse A[i + 1 .. n − 1]
L10 return true
```

Lines L1 and L2 find the *pivot* $i$: the largest index with $A[i] < A[i+1]$. After line L2, the suffix $A[i+1 \ldots n-1]$ is the longest non-increasing suffix. If no pivot exists, the whole array is non-increasing, so it is the greatest arrangement. Lines L4 and L5 then reverse it to the least arrangement and return false.

Line L7 scans the suffix from the right. The suffix is non-increasing, so the first item from the right that is greater than $A[i]$ is the smallest item of the suffix that is greater than $A[i]$, and it is its rightmost copy. The loop stops, because $A[i+1] > A[i]$. Line L8 puts that item at the pivot. After the exchange the suffix is still non-increasing, so line L9 turns it into a non-decreasing suffix, which is its least order.

The tests $\ge$ in line L2 and $\le$ in line L7 are non-strict. This makes the method correct for repeated items, and it then steps through the distinct arrangements only.

## Example

Apply NEXT-PERMUTATION to $A = [2, 6, 3, 9, 7, 5, 4, 1]$, with $n = 8$.

| step | lines | test or action | $A$ |
|---|---|---|---|
| 1 | L1 to L2 | $i = 6$: $4 \ge 1$, go left | 2 6 3 9 7 5 4 1 |
| 2 | L2 | $i = 5$: $5 \ge 4$; $i = 4$: $7 \ge 5$; $i = 3$: $9 \ge 7$, go left | 2 6 3 9 7 5 4 1 |
| 3 | L2 | $i = 2$: $3 \ge 9$ is false, so the pivot is $i = 2$ | 2 6 **3** 9 7 5 4 1 |
| 4 | L6 to L7 | $j = 7$: $1 \le 3$, go left; $j = 6$: $4 \le 3$ is false, so $j = 6$ | 2 6 **3** 9 7 5 **4** 1 |
| 5 | L8 | exchange $A[2]$ and $A[6]$ | 2 6 4 9 7 5 3 1 |
| 6 | L9 | reverse $A[3 \ldots 7]$ | 2 6 4 1 3 5 7 9 |

The longest non-increasing suffix is $9\,7\,5\,4\,1$, so the prefix $2\,6$ stays. The pivot item 3 is replaced by 4, the smallest larger item of the suffix. The call makes 5 comparisons in line L2, 2 in line L7, and 1 + 2 = 3 exchanges. The result is the successor: any arrangement between the two would have to start with $2\,6\,3$ and be greater than $2\,6\,3\,9\,7\,5\,4\,1$, which is the greatest arrangement with that start.

**A multiset.** Start from the sorted array $[1, 1, 2, 3]$ and call NEXT-PERMUTATION until it returns false. The calls visit the $4!/2! = 12$ distinct arrangements, each once:

$$1123,\ 1132,\ 1213,\ 1231,\ 1312,\ 1321,\ 2113,\ 2131,\ 2311,\ 3112,\ 3121,\ 3211.$$

The call on $3211$ finds no pivot, reverses the array back to $1123$ and returns false.

## Correctness

**Theorem.** Let $A$ hold a sequence of $n \ge 0$ items from a total order. If $A$ is not the greatest arrangement of its items, NEXT-PERMUTATION returns true and leaves in $A$ the least arrangement of the same multiset that is greater than the input. Otherwise it returns false and leaves $A$ sorted in non-decreasing order.

The key fact is about the suffix. Let $i$ be the pivot of line L2. Each arrangement that keeps $A[0 \ldots i]$ is at most the input, because the suffix $A[i+1 \ldots n-1]$ is non-increasing and so is already the greatest order of its items. So the successor must change position $i$ or an earlier one, and the smallest such change is at position $i$: put there the smallest larger item of the suffix, then write the rest in non-decreasing order. Lines L7 to L9 do exactly this. The full proof, with the multiset case, is in the proof file below.

**Corollary.** Start from $A$ sorted in non-decreasing order, and call NEXT-PERMUTATION until it returns false. The calls visit each distinct arrangement of the multiset exactly once, in increasing lexicographic order, and leave $A$ sorted again. For $n$ distinct items this is $n!$ arrangements. For a multiset with multiplicities $m_1, \ldots, m_k$ it is the [multinomial coefficient](/multinomial-coefficient/) $n!/(m_1! \cdots m_k!)$.

## Complexity

The cost model counts comparisons of items and exchanges of items. Each other step takes $O(1)$ time. Let $\ell = n - 1 - i$ be the length of the non-increasing suffix after line L2, with $\ell = n$ when there is no pivot.

- **Worst case, $\Theta(n)$.** Line L2 makes at most $n - 1$ comparisons, line L7 at most $\ell$, and lines L8 and L9 make $1 + \lfloor \ell/2 \rfloor$ exchanges. The input $1\,n\,(n-1) \cdots 2$ has $\ell = n - 1$ and its successor $2\,1\,3 \cdots n$ differs from it in all $n$ positions, so $\Omega(n)$ writes are needed for it.
- **Best case, $\Theta(1)$.** If $A[n-2] < A[n-1]$, line L2 makes one comparison, line L7 one, and line L9 reverses one item.
- **Extra space, $\Theta(1)$.** Two indices and the space of one exchange.

**Amortized cost for distinct items.** Run the corollary on $n \ge 2$ distinct items. The $n! - 1$ calls that return true see each permutation except the greatest one exactly once. For $1 \le k \le n$, exactly $n!/k!$ permutations end with $k$ items in decreasing order: choose the set of the last $k$ items in $\binom{n}{k}$ ways, place them in decreasing order, and order the rest in $(n-k)!$ ways. Such a permutation has $\ell \ge k$. Over the $n! - 1$ permutations that are not the greatest one, $\ell \le n - 1$, so

$$\sum \ell = \sum_{k=1}^{n-1} \left( \frac{n!}{k!} - 1 \right), \qquad \frac{\sum \ell}{n! - 1} \to \sum_{k \ge 1} \frac{1}{k!} = e - 1 \approx 1.718.$$

Line L2 makes exactly $\ell$ comparisons when a pivot exists. For a fixed $\ell$, the last $\ell + 1$ items have the pattern "pivot, then a decreasing run", with the pivot not the largest of them. Each of the $\ell$ possible ranks of the pivot among these items occurs equally often, so line L7 makes $1 + (\ell - 1)/2 = (\ell + 1)/2$ comparisons on average for that $\ell$. The averages per call, over the full listing, are then:

| $n$ | 3 | 5 | 7 | 9 | limit |
|---|---|---|---|---|---|
| comparisons in L2 | 1.400 | 1.689 | 1.717 | 1.718 | $e - 1 \approx 1.718$ |
| comparisons in L7 | 1.200 | 1.345 | 1.359 | 1.359 | $e/2 \approx 1.359$ |
| exchanges in L8 and L9 | 1.400 | 1.529 | 1.543 | 1.543 | $\cosh 1 \approx 1.543$ |

The exchange limit follows from $\mathbb{E}\lfloor \ell/2 \rfloor = \sum_{j \ge 1} \Pr[\ell \ge 2j] \to \sum_{j \ge 1} 1/(2j)! = \cosh 1 - 1$. So listing all $n!$ permutations takes $\Theta(n!)$ time, which is constant amortized time ([CAT](/constant-amortized-time-generation/)) per permutation, with about $3e/2 - 1 \approx 3.08$ comparisons per call. The delay between two outputs is still $\Theta(n)$ in the worst case, so the method is not [loopless](/loopless-generation/).

**Multisets are not always CAT.** For the multiset $0^{n-1}1$, the $n$ arrangements $0 \cdots 01, 0 \cdots 010, \ldots, 10 \cdots 0$ and the final call take $n^2 - 1$ comparisons in total, which is $\Theta(n)$ per arrangement.

**Lower bounds.** Each method that lists $N$ objects takes $\Omega(N)$ time. A method that visits the arrangement in place must change at least two positions between two distinct permutations, and the lexicographic order changes $\ell + 1$ positions, which is $e$ positions on average in the limit. Orders with a single exchange per step are given by [Heap's algorithm](/heaps-algorithm/) and the [Steinhaus-Johnson-Trotter algorithm](/steinhaus-johnson-trotter/).

## Properties

- **In place.** The method needs only two indices. It keeps no state between calls, so a call can start from any arrangement.
- **Comparison based.** It only compares and exchanges items, so it works for any total order, such as strings or tuples.
- **Multiset safe.** With the non-strict tests it never produces the same arrangement twice.
- **Cyclic.** The call on the last arrangement returns the first one, so repeated calls cycle through all arrangements.
- **Not a minimal-change order.** Two neighbors can differ in all $n$ positions.

## Variants and improvements

- **Previous permutation.** Reverse every comparison: find the longest non-decreasing suffix, exchange the item before it with the largest smaller item of the suffix, and reverse the suffix. This is `std::prev_permutation`.
- **Binary search in line L7.** The suffix is sorted, so the item of line L7 can be found with binary search in $O(\log \ell)$ comparisons. This helps only for long suffixes, which are rare.
- **Skip a block of permutations.** In a search, a prefix $A[0 \ldots k]$ can be rejected at once. Sort $A[k+1 \ldots n-1]$ in decreasing order, and the next call moves to the next prefix. This skips the remaining completions of the prefix.
- **Jump by $r$ steps.** [Rank](/permutation-ranking/) the permutation, add $r$, and [unrank](/permutation-unranking/). This costs $O(n \log n)$ time with a [Fenwick tree](/fenwick-tree/), instead of $r$ calls.
- **Successor of a $k$-subset or of a $k$-permutation.** The same suffix idea gives the [lexicographic order of combinations](/lexicographic-combinations/).

## When to use it

Use next permutation when the order matters: to list arrangements in sorted order, to produce the next larger number with the same digits, or to resume a listing from any arrangement without stored state. Use it for multisets, because it skips duplicates for free. If you need only all permutations in any order and want the fewest changes, [Heap's algorithm](/heaps-algorithm/) makes one exchange per step. If neighbors must differ by an adjacent exchange, use the [Steinhaus-Johnson-Trotter algorithm](/steinhaus-johnson-trotter/).

## Pitfalls

- **Strict tests with repeated items.** With the test $A[i] > A[i+1]$ in line L2 instead of $\ge$, two equal items become a pivot: on $[1, 2, 2]$ the pivot is $i = 1$, and the scan of line L7 runs off the left end of the array. With the test $A[j] < A[i]$ in line L7 instead of $\le$, the exchange can swap two equal items: from $1122$ the calls give $1212$, $1221$ and then $1122$ again, so the listing never ends. Keep $\ge$ in line L2 and $\le$ in line L7.
- **Sorting the suffix instead of reversing it.** The suffix is already in non-increasing order, so line L9 only needs a reversal in $O(\ell)$ time. A sort there costs $O(\ell \log \ell)$ and is a common slowdown.
- **Not starting from the sorted array.** The listing of all arrangements must start from the least arrangement. Starting from the given order lists only the arrangements that follow it, unless the loop also uses the wrap-around of line L4.
- **The index underflow.** In a language with unsigned indices, $i \ge 0$ in line L2 is always true. Use a signed index, or test $i > 0$ and look at $A[i-1]$.

## Implementations

## History

Knuth traces the method of Algorithm L to the Indian mathematician Nārāyaṇa Paṇḍita in the fourteenth century, and gives the version for multisets. It is the function `next_permutation` of the C++ standard library. In his 1977 survey, Sedgewick compared it with the methods that use one exchange per step, and found that those methods are faster for listing all permutations.

## References
