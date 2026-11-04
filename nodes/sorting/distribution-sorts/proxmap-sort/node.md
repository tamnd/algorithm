---
tag: QTZM0Z
kind: algorithm
slug: proxmap-sort
name: Proxmap sort
aliases:
- Proxmap sorting
area: sorting/distribution-sorts
level: advanced
summary: Distribution sort that uses a proximity map from key values to array slots, with insertion to fix local order.
solves: [sorting-problem]
model: real-ram
complexity:
  vars: {n: the number of keys, m: the number of subarrays}
  time: {worst: Θ(n^2), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n + m)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history: {year: 1998, people: [Thomas A. Standish], note: described in his textbook Data Structures in Java together with proxmap search}
prereqs: [bucket-sort]
see_also: [bucket-sort, flashsort, counting-sort, insertion-sort, uniform-input-model, interpolation-search, bucket-sort-expected-linear, distribution-sort]
sources:
  - book: isbn:9780201305647
    title: Thomas A. Standish, Data Structures in Java
    locator: Section 10.6, pages 394 to 405 (proxmap sort, with the hit counts, the proxmap, the locations and the insertion into the subarrays, and proxmap search)
  - paper: doi:10.1145/1113847.1113874
    title: Thomas A. Standish and Norman Jacobson, Using O(n) Proxmap Sort and O(1) Proxmap Search to motivate CS2 students (Part I), ACM SIGCSE Bulletin 37(4), 2005
    locator: the description of the method and of its expected O(n) time for keys spread evenly
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.4, Bucket sort (the analysis by the sum of the squares of the bucket sizes, which applies to the subarrays of proxmap sort)
---

Proxmap sort is a [distribution sort](/distribution-sort/) that uses a map key from the key values to $m$ subarrays, counts how many keys go to each subarray, and from these counts builds a *proximity map* (proxmap) that gives the start of each subarray in the output. Then it inserts each key into its subarray, with [insertion sort](/insertion-sort/) inside the subarray. Standish described it in his textbook of 1998, together with proxmap search, which finds a key in the sorted array with the same map. Like [bucket sort](/bucket-sort/), it takes $\Theta(n)$ expected time when the map spreads the keys evenly, and $\Theta(n^2)$ time when most keys go to one subarray.

## In plain words

Think of a theatre where each guest gets a seat area by the first letter of the name. Before the doors open, you count how many guests have each first letter. Then you know exactly how many seats each area needs and where each area starts, so the areas sit side by side with no gaps.

When a guest comes in, you send the guest to the start of the right area. If the area already has guests, the new guest sits in order among them, and the guests after that move one seat along. Each area is small, so this takes little work. At the end, all guests sit in order.

## The problem

The input is an array $A[0 \ldots n-1]$ of keys and a map key $M$ from keys to $\{0, \ldots, m - 1\}$ that is non-decreasing: $x \le y$ implies $M(x) \le M(y)$. For numbers in $[0, 1)$ a usual choice is $M(x) = \lfloor m x \rfloor$; for other ranges, a linear map from the minimum to the maximum. The output is the keys in non-decreasing order.

## The algorithm

The array $B$ is the output area. $P[k]$ is the start of subarray $k$, and $F[k]$ is the number of keys already placed in it.

```pseudo id=main
PROXMAP-SORT(A, n, m, M)
L1  H[k] ← the number of i with M(A[i]) = k, for k = 0 .. m − 1     ▷ hit counts
L2  P[k] ← H[0] + ... + H[k − 1], for k = 0 .. m − 1                ▷ the proxmap
L3  F[k] ← 0 for k = 0 .. m − 1; B ← an array of n empty cells
L4  for i ← 0 to n − 1 do
L5      x ← A[i]; k ← M(x); j ← P[k] + F[k]; F[k] ← F[k] + 1          ▷ the location
L6      while j > P[k] and B[j − 1] > x do B[j] ← B[j − 1]; j ← j − 1
L7      B[j] ← x
L8  copy B to A
L9  return A
```

Lines L1 and L2 are the counting pass of a [counting sort](/counting-sort/) on $M(x)$. The proxmap reserves exactly $H[k]$ cells for subarray $k$, so subarray $k$ is $B[P[k] \ldots P[k] + H[k] - 1]$. Lines L5 to L7 insert $x$ into the filled part of its subarray, as one step of insertion sort: larger keys shift one cell right. The shift stays inside the subarray, because the subarray has a cell for each of its keys. Standish calls the value $P[M(x)]$ the location of $x$.

## Example

Sort $A = [3.4, 0.9, 5.2, 3.1, 7.7, 0.2, 5.9, 3.8, 2.5, 6.0]$ with $m = 8$ and $M(x) = \lfloor x \rfloor$.

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| hit count $H[k]$ | 2 | 0 | 1 | 3 | 0 | 2 | 1 | 1 |
| proxmap $P[k]$ | 0 | 2 | 2 | 3 | 6 | 6 | 8 | 9 |

Subarrays 1 and 4 are empty. The insertions go as follows.

| Key | $k$ | Cell | $B$ after the insert |
|---|---|---|---|
| 3.4 | 3 | 3 | · · · 3.4 · · · · · · |
| 0.9 | 0 | 0 | 0.9 · · 3.4 · · · · · · |
| 5.2 | 5 | 6 | 0.9 · · 3.4 · · 5.2 · · · |
| 3.1 | 3 | 3, after a shift of 3.4 | 0.9 · · 3.1 3.4 · 5.2 · · · |
| 7.7 | 7 | 9 | 0.9 · · 3.1 3.4 · 5.2 · · 7.7 |
| 0.2 | 0 | 0, after a shift of 0.9 | 0.2 0.9 · 3.1 3.4 · 5.2 · · 7.7 |
| 5.9 | 5 | 7 | 0.2 0.9 · 3.1 3.4 · 5.2 5.9 · 7.7 |
| 3.8 | 3 | 5 | 0.2 0.9 · 3.1 3.4 3.8 5.2 5.9 · 7.7 |
| 2.5 | 2 | 2 | 0.2 0.9 2.5 3.1 3.4 3.8 5.2 5.9 · 7.7 |
| 6.0 | 6 | 8 | 0.2 0.9 2.5 3.1 3.4 3.8 5.2 5.9 6.0 7.7 |

The sort makes 2 shifts in total.

## Correctness

Subarray $k$ gets exactly $H[k]$ cells, the subarrays are in the order of $k$, and every key with $M(x) = k$ goes to subarray $k$. Since $M$ is non-decreasing, every key of a lower subarray is at most every key of a higher subarray. Inside a subarray, lines L5 to L7 keep the filled part sorted, as insertion sort does, and never move a key out of its subarray. So at the end every subarray is sorted and full, and $B$ is sorted. The full proof is below.

## Complexity

- **Counting and proxmap.** Lines L1 to L3 take $\Theta(n + m)$ time.
- **Insertions.** Inserting into subarray $k$ costs $O(1)$ per key plus one step per shift. The shifts inside subarray $k$ are at most $\binom{H[k]}{2}$, so the time of lines L4 to L7 is $O(n + \sum_k H[k]^2)$.
- **Average.** For $n$ independent keys uniform on $[0, 1)$ and $M(x) = \lfloor m x \rfloor$ with $m = n$, $\mathbb{E}[H[k]^2] = 2 - 1/n$, as in the proof of [bucket sort expected linear time](/bucket-sort-expected-linear/). So the expected time is $\Theta(n)$.
- **Worst case.** If all keys map to one subarray and arrive in decreasing order, there are $\binom{n}{2}$ shifts, and the time is $\Theta(n^2)$.
- **Space.** $B$ takes $n$ cells, and $H$, $P$ and $F$ take $3m$ words, so the extra space is $\Theta(n + m)$.

## Properties

- **Stable.** Keys enter in input order, and line L6 moves a key only past larger keys, so equal keys keep their input order.
- **Not in place.** It writes into a second array $B$.
- **Not a comparison sort.** The map key does arithmetic on the keys. Comparisons occur only inside a subarray.
- **Proxmap search.** After the sort, $P$ and $H$ act as an index: to find $x$, search the subarray $B[P[M(x)] \ldots P[M(x)] + H[M(x)] - 1]$, which has $O(1)$ expected size for even keys.

## Variants and improvements

- **Other map keys.** Any non-decreasing map works. A map that follows the distribution of the keys, for example from a sample, makes the subarrays even when the keys are not uniform.
- **The number of subarrays.** $m = n$ is the usual choice. A smaller $m$ saves space but makes the subarrays larger.
- **Insertion order.** Inserting keys into $B$ from the back, with the subarray filled from its end, gives the same result.
- **[Flashsort](/flashsort/)** uses the same counting idea but moves the keys in place along cycles and sorts them at the end.
- **[Bucket sort](/bucket-sort/)** uses lists for the buckets; proxmap sort places the buckets in one array, with exact sizes from the counts.

## When to use it

Use proxmap sort when the keys are close to evenly spread over a known range and a second array is affordable, especially when the same map should later serve fast searches. For skewed keys, the subarrays become large, and a sort with an $O(n \log n)$ worst case is safer.

## Pitfalls

- **A map that is not monotone.** If $M(x) > M(y)$ for some $x < y$, the subarrays come out in the wrong order and the result is not sorted.
- **A map out of range.** The largest key can map to $m$ with $M(x) = \lfloor m(x - lo)/(hi - lo) \rfloor$. Clamp it to $m - 1$ or use $m - 1$ in place of $m$ in the formula.
- **Shifting past the subarray.** The loop of line L6 must stop at $P[k]$. Without that test, a key can move into the subarray before.
- **Skewed data.** One cluster of keys makes one large subarray, and the insertions become quadratic.

## Implementations

## History

Thomas A. Standish described proxmap sort and proxmap search in his textbook Data Structures in Java (1998). Standish and Norman Jacobson later wrote two papers in the ACM SIGCSE Bulletin (2005 and 2006) on how to use the method to teach algorithms with expected linear time. The idea of counting first and then placing keys in reserved areas goes back to [counting sort](/counting-sort/) and to the multiple list insertion of Knuth's Section 5.2.1.

## References
