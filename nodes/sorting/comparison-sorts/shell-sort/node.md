---
tag: ZSYXJJ
kind: algorithm
slug: shell-sort
name: Shell sort
aliases:
- Shellsort
- diminishing increment sort
area: sorting/comparison-sorts
level: core
summary: Insertion sort over gapped subsequences with decreasing gaps; its running time depends on the gap sequence.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: O(n^(3/2)), best: Θ(n log n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1959
  people: [Donald L. Shell]
  note: Shell published the method in the Communications of the ACM in 1959, with the gaps n/2, n/4, ..., 1.
prereqs: [insertion-sort, loop-invariant]
see_also: [shell-sort-gap-sequence, h-sorting, insertion-sort, comb-sort, inversion, heapsort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Sorting by insertion (Algorithm D, Theorem K on h-sorting a k-sorted file, Theorem H on the increments 2^k - 1, and the tables of increments)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1, Elementary sorts (Shellsort, Algorithm 2.3, with the increments 1, 4, 13, 40, ... and the O(N^{3/2}) bound)
  - paper: "D. L. Shell, A high-speed sorting procedure, Communications of the ACM 2(7), 1959"
    locator: pages 30 to 32, the whole paper
  - paper: "Robert Sedgewick, Analysis of Shellsort and related algorithms, Algorithms ESA '96, Lecture Notes in Computer Science 1136, Springer, 1996"
    locator: the survey of the known upper and lower bounds and the open problems
---

Shell sort is an [insertion sort](/insertion-sort/) that first moves items over long distances. For a decreasing sequence of gaps $h_t > \cdots > h_1 = 1$, it sorts the items that are $h$ apart, for each gap $h$ in turn. The last pass, with gap 1, is a plain insertion sort, but by then the array is almost sorted, so it is fast. It solves the [sorting problem](/sorting-problem/) in place, and its time depends on the [gap sequence](/shell-sort-gap-sequence/): $\Theta(n^2)$ in the worst case with Shell's gaps $n/2, n/4, \ldots$, and $O(n^{3/2})$ with the gaps $1, 4, 13, 40, \ldots$ of this page.

## In plain words

Insertion sort is slow on a big unsorted array because it moves each item only one place at a time. An item that belongs far away needs many small steps.

Shell sort first looks at the items that are, say, forty places apart. It sorts each such group with insertion sort. An item can now jump forty places in one step. Then it does the same with groups of items thirteen places apart, then four, and at the end one. The last round is a normal insertion sort.

Each round leaves the array more nearly in order, so the next round has little work. At the end, each item is close to its place, and the last insertion sort needs only short moves.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

An array is *$h$-sorted* when $A[i] \le A[i + h]$ for each $i$ with $0 \le i < n - h$. Then each of the $h$ chains $A[r], A[r + h], A[r + 2h], \ldots$ is sorted. A 1-sorted array is sorted. The page [h-sorting](/h-sorting/) covers this step.

## The algorithm

The gap sequence $H$ lists the gaps from the largest to the smallest, and the last gap must be 1. This page uses Knuth's gaps $h_{k+1} = 3h_k + 1$, which are $1, 4, 13, 40, 121, \ldots$. As in Sedgewick and Wayne, the largest gap is the first gap of this list that is at least $n/3$, so each other gap is less than $n/3$.

```pseudo id=main
SHELL-SORT(A, H)                           ▷ H is decreasing and ends with 1
L1  for each h in H do                     ▷ make A h-sorted
L2      for i ← h to n − 1 do
L3          key ← A[i]
L4          j ← i
L5          while j ≥ h and key < A[j − h] do
L6              A[j] ← A[j − h]
L7              j ← j − h
L8          A[j] ← key
```

Lines L2 to L8 are insertion sort with step $h$ instead of 1. The loop over $i$ does not sort one chain after another. It moves along the array and inserts each item into its own chain, so the $h$ chains are sorted in an interleaved way. After the pass for $h$, the array is $h$-sorted. The pass for the gap 1 is exactly [insertion sort](/insertion-sort/), so the output is sorted for any gap sequence that ends with 1. The earlier passes only make that last pass fast.

## Example

Sort $A = [62, 83, 18, 53, 7, 17, 95, 86, 47, 69, 25, 28]$, with $n = 12$. The first Knuth gap that is at least $12/3 = 4$ is 4, so the gaps are $4$ and $1$.

**The pass with $h = 4$.** The four chains are at the indices $\{0, 4, 8\}$, $\{1, 5, 9\}$, $\{2, 6, 10\}$ and $\{3, 7, 11\}$.

| chain | before | after |
|---|---|---|
| 0, 4, 8 | 62 7 47 | 7 47 62 |
| 1, 5, 9 | 83 17 69 | 17 69 83 |
| 2, 6, 10 | 18 95 25 | 18 25 95 |
| 3, 7, 11 | 53 86 28 | 28 53 86 |

The array is now $[7, 17, 18, 28, 47, 69, 25, 53, 62, 83, 95, 86]$. It is 4-sorted. The pass made 12 comparisons and 7 moves.

**The pass with $h = 1$.** Insertion sort now moves 25 left past 69, 47 and 28, moves 86 past 95, and needs no other move. The result is $[7, 17, 18, 25, 28, 47, 53, 62, 69, 83, 86, 95]$. This pass made 17 comparisons and 6 moves.

The total is 29 comparisons. Plain insertion sort on the same input makes 44.

## Correctness

The pass for a gap $h$ is an insertion sort on each chain $A[r], A[r+h], \ldots$, so after it the array is $h$-sorted and holds the same items. The last pass has $h = 1$, and it is a full insertion sort, so the output is sorted. The proof of insertion sort carries over to each chain, with the index step $h$ instead of 1; the full proof is below.

Shell sort also keeps the earlier work: **if an array is $k$-sorted and then $h$-sorted, it stays $k$-sorted** (Knuth, Section 5.2.1, Theorem K). The correctness does not need this fact, but the time bound does.

## Complexity

**The extra space** is $\Theta(1)$: the key, the indices and the gap. Knuth's gaps can be made on the fly, by $h \leftarrow 3h + 1$ up and $h \leftarrow \lfloor h/3 \rfloor$ down.

**The best case** is a sorted input. Then the loop of line L5 stops at once in each step, and the pass for $h$ makes $n - h$ comparisons. There are $\Theta(\log n)$ gaps, and each gap except the largest is less than $n/3$, so each of these passes makes more than $2n/3$ comparisons. So the time is $\Theta(n \log n)$. Here the number of passes, not the input, sets the cost.

**The worst case with Knuth's gaps is $O(n^{3/2})$.** The proof has three steps.

1. *A lemma on two gaps.* Let $g$ and $h$ be positive integers with $\gcd(g, h) = 1$. Each integer $d \ge (g-1)(h-1)$ is a sum $d = ag + bh$ with integers $a, b \ge 0$; this is the bound of Sylvester for the coin problem of two coins. So if an array is both $g$-sorted and $h$-sorted, then $A[i] \le A[i + d]$ for each such $d$: step from $i$ by $g$ a total of $a$ times and then by $h$ a total of $b$ times, and each step does not decrease the item.
2. *One pass.* Consider the pass for the gap $h_k$, with $h_{k+1} = 3h_k + 1$ and $h_{k+2} = 9h_k + 4$, and assume that both larger gaps were used before. The two numbers are coprime, because $h_{k+2} = 3h_{k+1} + 1$. By Theorem K, at the start of the pass the array is still $h_{k+1}$-sorted and $h_{k+2}$-sorted. So by the lemma, an item is at most each item that is $D = (h_{k+1}-1)(h_{k+2}-1) = 27h_k^2 + 9h_k$ or more places to its right. The pass is an insertion sort of each chain, and insertion sort does one move for each [inversion](/inversion/) of its chain at the start. An item has fewer than $D/h_k + 1 = 27h_k + 10$ larger items before it in its chain, so the pass does $O(n h_k)$ moves and comparisons.
3. *The sum.* A pass with gap $h$ is also an insertion sort of $h$ chains of at most $\lceil n/h \rceil$ items each, so it costs $O(h \cdot (n/h)^2) = O(n^2/h)$ with no assumption. Use the bound $O(n h_k)$ for the gaps $h_k \le \sqrt n$ and the bound $O(n^2/h_k)$ for the gaps $h_k > \sqrt n$. For $n \ge 900$, each gap $h_k \le \sqrt n$ has $h_{k+2} \le 9\sqrt n + 4 < n/3$, so both larger gaps are in the sequence and step 2 applies. The gaps grow by a factor of about 3, so both sums are geometric, and each is $O(n \sqrt n)$.

The same proof works for each sequence in which two consecutive gaps are coprime and the ratio of two consecutive gaps is bounded, such as Hibbard's gaps $2^k - 1$. For Hibbard's gaps, Papernov and Stasevich showed that $\Theta(n^{3/2})$ is tight in the worst case.

**Shell's own gaps are quadratic.** With $n = 2^m$ and the gaps $n/2, n/4, \ldots, 1$, each gap except the last is even. Put the $n/2$ largest items at the even indices and the $n/2$ smallest at the odd indices. No pass before the last one compares an even index with an odd index, so the last pass still has $\Theta(n^2)$ [inversions](/inversion/) to remove. For $n = 1024$ this input takes $140{,}544$ comparisons.

**Other gap sequences.** Pratt's gaps $2^p 3^q$ give $\Theta(n \log^2 n)$ in the worst case, but with many passes. Sedgewick's gaps $1, 8, 23, 77, 281, \ldots$ give $O(n^{4/3})$. No sequence gives $O(n \log n)$ in the worst case: Plaxton, Poonen and Suel proved a lower bound of $\Omega(n (\log n / \log \log n)^2)$ for each gap sequence. Whether some sequence gives $O(n \log n)$ on average is open. The page [Shellsort gap sequence](/shell-sort-gap-sequence/) gives the details and the sources.

**The average case** has no closed form for the sequences used in practice. In measurements on random input, the comparison count of the gaps of this page grows at about the rate $n^{1.25}$. For $n = 10^4$ and $n = 10^5$ random keys, the code below makes $242{,}290$ and $4{,}192{,}908$ comparisons, against $n^{3/2} = 10^6$ and $n^{3/2} \approx 3.2 \times 10^7$.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst, gaps $1, 4, 13, \ldots$ | $O(n^{3/2})$ |
| time | comparison model, best | $\Theta(n \log n)$ |
| time | comparison model, worst, Shell's gaps | $\Theta(n^2)$ |
| extra space | | $\Theta(1)$ |

## Properties

- **Not stable.** A pass with $h > 1$ moves an item past items of other chains, and these can be equal to it. On $(1, a), (1, b), (0, c)$ with the gaps 2 and 1, the 2-pass sorts the chain of the indices 0 and 2, so $(0, c)$ and $(1, a)$ change places. The output is $(0, c), (1, b), (1, a)$.
- **In place.** It uses $\Theta(1)$ extra space and no recursion.
- **Adaptive.** On a sorted or a nearly sorted input, each pass ends each step at once.
- **No stack and short code.** It needs no recursion and no buffer, which suits small embedded programs.

## Variants and improvements

- **Better gap sequences.** Ciura found by experiment the gaps $1, 4, 10, 23, 57, 132, 301, 701$, which are among the best known in practice for $n$ up to a few thousand. See [Shellsort gap sequence](/shell-sort-gap-sequence/).
- **[Comb sort](/comb-sort/).** The same idea with [bubble sort](/bubble-sort/) passes in place of insertion passes.

## When to use it

Use Shell sort for medium arrays, of a few hundred to a few thousand items, when the code must be short, in place and free of recursion. It is much faster than insertion sort on random input, and it has no bad worst case like plain quicksort. For large arrays, [heapsort](/heapsort/), [merge sort](/merge-sort/) or [quicksort](/quicksort/) are faster, because their $O(n \log n)$ bound grows more slowly.

## Pitfalls

- **The last gap is not 1.** A sequence that ends with a gap larger than 1 leaves the array only $h$-sorted, not sorted. The implementation below rejects it.
- **Gaps that share factors.** With the gaps $n/2, n/4, \ldots$ when $n$ is a power of two, the odd and the even indices never meet before the last pass, and the time is $\Theta(n^2)$. Use gaps with no common factor, such as Knuth's or Ciura's.
- **A gap at least $n$.** A pass with $h \ge n$ does nothing, but a sequence that starts too high wastes passes. For Knuth's gaps, stop at the first gap that is at least $n/3$.
- **Sorting each chain apart.** Sorting the chains one after the other also works, but it jumps around in memory. The loop of line L2 visits the array in order, which uses the cache better.

## Implementations

The Python version takes an optional list of gaps and uses Knuth's gaps by default.

## History

Donald L. Shell published the method in 1959 in the Communications of the ACM, with the gaps $\lfloor n/2 \rfloor, \lfloor n/4 \rfloor, \ldots, 1$. Hibbard proposed the gaps $2^k - 1$ in 1963, and Papernov and Stasevich proved the bound $O(n^{3/2})$ for them in 1965. Pratt gave the gaps $2^p 3^q$ and the bound $\Theta(n \log^2 n)$ in his thesis of 1971. Knuth's Section 5.2.1 gives the gaps $(3^k - 1)/2$, and Sedgewick found sequences with the bound $O(n^{4/3})$ in 1986. Plaxton, Poonen and Suel proved in 1992 that no gap sequence reaches $O(n \log n)$ in the worst case. Sedgewick's survey of 1996 lists what is known.

## References
