---
tag: GEP1AZ
kind: algorithm
slug: flashsort
name: Flashsort
aliases:
- Flash sort
area: sorting/distribution-sorts
level: advanced
summary: In-place distribution sort that classifies keys into about n/10 classes by a linear map, then permutes and insertion-sorts.
solves: [sorting-problem]
model: real-ram
complexity:
  vars: {n: the number of keys, m: the number of classes}
  time: {worst: Θ(n^2), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(m)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history: {year: 1998, people: [Karl-Dietrich Neubert], note: published in Dr. Dobb's Journal as Flashsort1}
prereqs: [bucket-sort, insertion-sort]
see_also: [bucket-sort, counting-sort, proxmap-sort, uniform-input-model, cycle-leader-permutation, in-place-permutation, american-flag-sort, insertion-sort]
sources:
  - paper: Karl-Dietrich Neubert, The Flashsort1 algorithm, Dr. Dobb's Journal, February 1998
    locator: the three steps of the algorithm (classification by a linear map from the minimum and the maximum, the in-place permutation along cycles, and the final straight insertion), and the measurements for the number of classes
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.4, Bucket sort (the expected linear time on uniform keys, by the sum of the squares of the bucket sizes)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 5.2.2, Application, Bucket Sort (the balls and bins analysis of the expected cost)
---

Flashsort is a distribution sort that puts each key into one of $m$ classes by a linear map from the smallest to the largest key, moves the keys into their class areas in place along permutation cycles, and then finishes with one [insertion sort](/insertion-sort/) over the whole array. Neubert published it in 1998. On keys that are close to the [uniform input model](/uniform-input-model/) and with $m = \Theta(n)$ classes, its expected time is $\Theta(n)$, and it needs only $\Theta(m)$ counters, not a second array for the keys. On skewed keys many fall into one class, and the final insertion sort can take $\Theta(n^2)$ time.

## In plain words

Look at the smallest and the largest key. If the keys are spread out evenly between them, then the value of a key tells you about where it goes: a key a quarter of the way from the smallest to the largest goes about a quarter of the way along the array. Flashsort cuts the range into many equal slices, counts how many keys fall in each slice, and so knows exactly which part of the array each slice gets.

Then it moves the keys to their parts. It picks up one key, puts it in the free place of its slice, picks up the key that was there, and so on, until it comes back to where it started. No second array is needed. At the end, each key is in the right slice, and a quick final pass with insertion sort fixes the small disorder inside each slice.

## The problem

The input is an array $A[0 \ldots n-1]$ of numbers. The output is the same keys in non-decreasing order, in $A$. The method needs a key map: an order-preserving way to turn a key into a position in the range from the minimum to the maximum. For real numbers this is $x \mapsto (x - lo)/(hi - lo)$; other keys need a map of the same kind, as for [bucket sort](/bucket-sort/).

## The algorithm

$m \ge 2$ is the number of classes. Class $k$ will occupy the positions $[start[k], top_0[k])$, where $top_0$ is the value of $top$ after line L5 and $start[k] = top_0[k] - C[k]$. During the permutation, positions $[top[k], top_0[k])$ hold keys of class $k$ that are already in place.

```pseudo id=main
FLASHSORT(A, n, m)
L1  if n ≤ 1 then return A
L2  lo ← min A; hi ← max A; if lo = hi then return A
L3  K(x) ← ⌊(m − 1)(x − lo) / (hi − lo)⌋          ▷ the class of x, in 0 .. m − 1
L4  C[k] ← the number of i with K(A[i]) = k, for k = 0 .. m − 1
L5  top[k] ← C[0] + ... + C[k], for k = 0 .. m − 1  ▷ one past the last free place of class k
L6  i ← 0
L7  while i < n do
L8      if i ≥ top[K(A[i])] then i ← i + 1; continue     ▷ A[i] is already in place
L9      x ← A[i]                                       ▷ the leader of a new cycle
L10     repeat k ← K(x); top[k] ← top[k] − 1; swap x and A[top[k]] until top[k] = i
L11 INSERTION-SORT(A)
L12 return A
```

Lines L3 to L5 are the counting pass of a [counting sort](/counting-sort/) on the class. Lines L7 to L10 are an in-place permutation by cycles, as in [cycle leader permutation](/cycle-leader-permutation/): each step of line L10 puts the key in hand at the top free place of its class and picks up the key that was there. The cycle that starts at position $i$ ends when a key is put at $i$ itself. Each key is put in place exactly once, so lines L7 to L10 make $n$ moves in total. After them, the classes are in order, and only the keys inside one class can be out of order, which line L11 fixes.

## Example

Sort $A = [42, 7, 93, 18, 65, 30, 7, 88, 51, 24]$ with $m = 4$. Then $lo = 7$, $hi = 93$ and $K(x) = \lfloor 3(x - 7)/86 \rfloor$. The classes of the keys are $1, 0, 3, 0, 2, 0, 0, 2, 1, 0$, so $C = [5, 2, 2, 1]$ and $top = [5, 7, 9, 10]$.

The first cycle starts at $i = 0$ with the leader 42.

| Step | Key in hand | Class | Put at | Key picked up |
|---|---|---|---|---|
| 1 | 42 | 1 | 6 | 7 |
| 2 | 7 | 0 | 4 | 65 |
| 3 | 65 | 2 | 8 | 51 |
| 4 | 51 | 1 | 5 | 30 |
| 5 | 30 | 0 | 3 | 18 |
| 6 | 18 | 0 | 2 | 93 |
| 7 | 93 | 3 | 9 | 24 |
| 8 | 24 | 0 | 1 | 7 |
| 9 | 7 | 0 | 0 | the old leader, which is dropped |

Now $A = [7, 24, 18, 30, 7, 51, 42, 88, 65, 93]$. Positions 1 to 6 pass the test of line L8. At $i = 7$ the key 88 is of class 2 with $top[2] = 8 > 7$, so it is the leader of a cycle of one step and goes back to position 7. The array has the classes $\{7, 24, 18, 30, 7\}$, $\{51, 42\}$, $\{88, 65\}$ and $\{93\}$ in order, with 6 inversions, all inside classes. Line L11 removes them with 6 shifts and gives $[7, 7, 18, 24, 30, 42, 51, 65, 88, 93]$.

## Correctness

The class map is non-decreasing, so a key of a lower class is never larger than a key of a higher class. Lines L4 and L5 give each class a block of positions of the right size, in the order of the classes. During the permutation, the number of keys of class $k$ that are not yet in place equals $top[k] - start[k]$, and every position before $i$ is in place. So the place where line L10 puts a key is free, and the cycle closes at $i$. After the loop the array is sorted by class, and insertion sort makes it fully sorted. The full proof is below.

## Complexity

- **Classification and permutation.** Lines L2 to L10 take $\Theta(n + m)$ time: two passes for the minimum, the maximum and the counts, $m$ prefix sums, and $n$ moves plus $n$ tests in line L8.
- **Insertion sort.** Its cost is $\Theta(n + I)$, where $I$ is the number of inversions. All inversions are inside classes, so $I \le \sum_k \binom{C[k]}{2}$.
- **Average.** For $n$ independent keys, uniform between their minimum and maximum, each key other than the minimum and the maximum falls into each class with probability about $1/m$, as balls into $m$ bins. Then $\mathbb{E}[C[k]^2] \approx n/m + n^2/m^2$, so $\mathbb{E}[I] \le \frac{1}{2} \sum_k \mathbb{E}[C[k]^2] = O(n + n^2/m)$, the same computation as for [bucket sort](/bucket-sort-expected-linear/). This is $O(n)$ for $m = \Theta(n)$, and the expected time is $\Theta(n)$.
- **Worst case.** If all keys but the largest fall into class 0, for example the keys $10^9, n - 1, n - 2, \ldots, 1$ with $m n < 10^9$, then $I = \Theta(n^2)$, and the time is $\Theta(n^2)$.
- **Best case.** Sorted keys spread evenly have $I = 0$, and the time is $\Theta(n + m)$.
- **Space.** The arrays $C$ and $top$ take $\Theta(m)$ words. For $m$ a fixed fraction of $n$, this is $\Theta(n)$ words, but much less than a second array of keys with their records.

## Properties

- **Not stable.** The cycles move keys past keys of the same class.
- **No second key array.** The permutation is in place, and only the $m$ counters are extra. With $m = \Theta(n)$ this is not in place in the strict sense.
- **Not a comparison sort.** The class map does arithmetic on the keys. Only the final insertion sort compares.
- **Deterministic.** Its expected bound holds for random inputs, not for every input.

## Variants and improvements

- **Number of classes.** The ratio $m/n$ trades the cost of the counters against the cost of the insertion sort. Published versions use a fixed fraction, with about $n/10$ classes as a common choice; the best value depends on the machine.
- **Recursive flashsort.** Sort large classes with flashsort again, on the minimum and the maximum of the class, and small classes with insertion sort. This limits the damage of skewed keys.
- **Sort each class.** Use a sort with a good worst case, such as [heapsort](/heapsort/) or [merge sort](/merge-sort/), for large classes, so the worst case becomes $O(n \log n)$.
- **Other key types.** Any order-preserving map to numbers works in line L3. For strings, a code of the characters after the common prefix of the minimum and the maximum is such a map.
- **[Proxmap sort](/proxmap-sort/)** is a close relative that uses a map to subarrays and inserts each key into its subarray.

## When to use it

Use flashsort for large arrays of numbers that are close to uniform on their range, when memory for a second array is short. Measurements, starting with those of Neubert, show it faster than quicksort on such data. Avoid it for data with clusters, heavy tails or many large gaps, where the classes are uneven; a hybrid with a sort that has a good worst case is safer.

## Pitfalls

- **All keys equal.** Then $hi = lo$ and line L3 divides by zero. Line L2 handles this case first.
- **Rounding.** In floating point, the class of $hi$ must be $m - 1$ and no class may exceed it. Clamp $K(x)$ to $[0, m - 1]$, and compute it in a way that keeps it non-decreasing in $x$.
- **Overflow.** For 64-bit integers, $(m - 1)(x - lo)$ can overflow. Use wider arithmetic or floating point with a clamp.
- **The test of line L8.** The test uses the class of the key at $i$, not the class of the position. This is correct only because every position before $i$ is already in place, so the loop must not skip ahead.
- **Skewed data.** One outlier can put almost all keys in one class, and the insertion sort then takes quadratic time.

## Implementations

## History

Karl-Dietrich Neubert published flashsort, as Flashsort1, in Dr. Dobb's Journal in 1998, with code in Fortran and C and measurements against quicksort. It combines ideas that were known before: the classification of [bucket sort](/bucket-sort/) by a linear map, the counting pass of counting sort, the in-place permutation by cycles, and a final insertion sort.

## References
