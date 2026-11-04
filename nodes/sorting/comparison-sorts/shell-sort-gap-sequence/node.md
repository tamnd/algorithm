---
tag: 90FWZ7
kind: concept
slug: shell-sort-gap-sequence
name: Shellsort increment sequence
aliases:
- Increment sequence
area: sorting/comparison-sorts
level: core
summary: The decreasing sequence of gaps used by Shellsort, whose choice strongly affects running time, with examples by Shell, Knuth and Sedgewick.
prereqs: [shell-sort]
see_also: [shell-sort, h-sorting, insertion-sort, coprime-integers, smooth-number, comb-sort, sorting-network]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Sorting by insertion (Theorem K, Theorem H on the increments 2^k - 1, Pratt's increments 2^p 3^q, and the table of the effect of increments)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1, Elementary sorts (Shellsort, the increments 1, 4, 13, 40, ..., and the remarks on other increment sequences)
  - paper: "Robert Sedgewick, Analysis of Shellsort and related algorithms, Algorithms ESA '96, Lecture Notes in Computer Science 1136, Springer, 1996"
    locator: the survey of the increment sequences, their upper and lower bounds, and the open problems
  - paper: "Marcin Ciura, Best increments for the average case of Shellsort, Fundamentals of Computation Theory (FCT 2001), Lecture Notes in Computer Science 2138, Springer, 2001"
    locator: the sequence 1, 4, 10, 23, 57, 132, 301, 701 found by search
  - paper: "C. Greg Plaxton, Bjorn Poonen and Torsten Suel, Improved lower bounds for Shellsort, 33rd IEEE Symposium on Foundations of Computer Science (FOCS), 1992"
    locator: the main theorem, a worst-case lower bound for each increment sequence
---

The increment sequence, or gap sequence, of [Shell sort](/shell-sort/) is the list of gaps $h_t > h_{t-1} > \cdots > h_1 = 1$ that the sort uses, one pass for each gap. Each pass [h-sorts](/h-sorting/) the array, and the last pass is a plain [insertion sort](/insertion-sort/). Any sequence that ends with 1 gives a correct sort, but the running time depends almost entirely on the sequence: from $\Theta(n^2)$ in the worst case for Shell's own gaps $n/2, n/4, \ldots, 1$, to $O(n^{3/2})$ for the gaps $2^k - 1$ or $(3^k - 1)/2$, to $O(n^{4/3})$ for Sedgewick's gaps and $\Theta(n \log^2 n)$ for Pratt's gaps $2^p 3^q$. No sequence is known to give $O(n \log n)$, and a lower bound of Plaxton, Poonen and Suel shows that none can in the worst case.

## In plain words

Shell sort sorts a row of cards in several rounds. In each round it picks a step size, and sorts the cards that are that many places apart, as if they were a separate short row. The step sizes get smaller, and the last round uses step size 1, which sorts the whole row.

The list of step sizes is the gap sequence. Any list that ends with 1 works, because the last round alone sorts the row. But the list decides how much work the last rounds have left. A good list makes each round leave the cards nearly sorted for the next one. A bad list, such as step sizes that are all even until the last round, never lets cards at even places meet cards at odd places, so the last round must do almost all the work.

## The idea

**Why the earlier passes help.** After a pass with gap $h$, the array is $h$-sorted: $A[i] \le A[i + h]$ for each $i$. Knuth's Theorem K (Section 5.2.1) says that a later pass with a smaller gap $k$ does not destroy this: if a $h$-sorted array is $k$-sorted, it stays $h$-sorted. So after the passes with gaps $g$ and $h$, the array is both $g$-sorted and $h$-sorted, and then $A[i] \le A[i + ag + bh]$ for all $a, b \ge 0$.

**Why the gaps should be [coprime](/coprime-integers/).** If $\gcd(g, h) = 1$, each integer at least $(g-1)(h-1)$ is of the form $ag + bh$ with $a, b \ge 0$. So after the passes with gaps $g$ and $h$, each item is at most each item that is $(g-1)(h-1)$ or more places to its right. In a later pass with gap $k$, an item can move only over items that are larger and fewer than $(g-1)(h-1)$ places to its left, so it moves at most $(g-1)(h-1)/k$ steps. This is the heart of the $O(n^{3/2})$ proofs. If all gaps share a factor $d > 1$, this argument gives nothing: the items in different classes modulo $d$ are never compared before the last pass.

**The trade-off.** A pass with gap $h$ on $n$ items costs at least about $n - h$ comparisons, so many gaps cost much even when each pass is cheap. Few gaps make each pass leave more work for the next. The good sequences grow roughly geometrically, with a ratio between about 2 and 4, so they have $\Theta(\log n)$ gaps. Pratt's sequence is the exception: it has $\Theta(\log^2 n)$ gaps, but each pass costs only $O(n)$.

**Pratt's sequence.** Take all numbers $2^p 3^q$ less than $n$, in decreasing order. When the pass for gap $h$ starts, the passes for $2h$ and $3h$ (if they are less than $n$) are already done, so by Theorem K the array is $2h$-sorted and $3h$-sorted. Each number at least $(2-1)(3-1) = 2$ is of the form $2a + 3b$, so in each chain of items $h$ apart, an item is at most each item two or more steps ahead. So in the $h$-pass each item moves at most one step, and the pass costs $O(n)$. There are $O(\log^2 n)$ numbers $2^p 3^q$ below $n$, so the total time is $O(n \log^2 n)$ in every case. These gaps are the [3-smooth numbers](/smooth-number/).

**Lower bounds.** Plaxton, Poonen and Suel (1992) proved that Shell sort with any sequence makes $\Omega(n (\log n / \log \log n)^2)$ comparisons in the worst case, so no sequence reaches $O(n \log n)$. Jiang, Li and Vitányi (2000) proved that with $p$ passes the average time is $\Omega(p\, n^{1 + 1/p})$. Whether some sequence gives $O(n \log n)$ on average is open.

## Examples

**The main sequences.** The bounds are for the worst case, as given by Knuth and by Sedgewick's survey.

| sequence | first gaps | rule | worst case |
|---|---|---|---|
| Shell, 1959 | $n/2, n/4, \ldots, 1$ | $\lfloor n / 2^k \rfloor$ | $\Theta(n^2)$ |
| Frank and Lazarus, 1960 | for $n = 100$: 51, 25, 13, 7, 3, 1 | $2 \lfloor n / 2^{k+1} \rfloor + 1$ | $\Theta(n^{3/2})$ |
| Hibbard, 1963 | 1, 3, 7, 15, 31, 63 | $2^k - 1$ | $\Theta(n^{3/2})$ |
| Papernov and Stasevich, 1965 | 1, 3, 5, 9, 17, 33 | $2^k + 1$, and 1 | $\Theta(n^{3/2})$ |
| Pratt, 1971 | 1, 2, 3, 4, 6, 8, 9, 12 | $2^p 3^q$ | $\Theta(n \log^2 n)$ |
| Knuth, 1973 | 1, 4, 13, 40, 121, 364 | $(3^k - 1)/2$, up to $n/3$ | $\Theta(n^{3/2})$ |
| Sedgewick, 1982 | 1, 8, 23, 77, 281, 1073 | $4^k + 3 \cdot 2^{k-1} + 1$, and 1 | $O(n^{4/3})$ |
| Sedgewick, 1986 | 1, 5, 19, 41, 109, 209, 505, 929 | $9 \cdot 4^k - 9 \cdot 2^k + 1$ and $4^k - 3 \cdot 2^k + 1$, merged | $O(n^{4/3})$ |
| Tokuda, 1992 | 1, 4, 9, 20, 46, 103, 233, 525 | $\lceil (9^k - 4^k) / (5 \cdot 4^{k-1}) \rceil$ | not known |
| Ciura, 2001 | 1, 4, 10, 23, 57, 132, 301, 701 | found by search; then times 2.25 | not known |

**The parity problem of Shell's gaps.** Let $n = 8$, with gaps 4, 2, 1, and the input $[1, 5, 2, 6, 3, 7, 4, 8]$: the small items 1 to 4 are at the even indices, and the large items 5 to 8 at the odd indices. The pass with gap 4 sorts the pairs at indices $(0, 4), (1, 5), (2, 6), (3, 7)$, which are already in order. The pass with gap 2 sorts the items at even indices and the items at odd indices, which are also in order. So the last pass gets the input unchanged, with 6 inversions. For $n = 2^k$ in general, this input has $(n/2)(n/2 - 1)/2$ inversions that only the last pass can remove, so the time is $\Theta(n^2)$. For $n = 1024$ the input has 130,816 inversions, and the sort makes 140,544 comparisons in total. The gaps $2 \lfloor n / 2^{k+1} \rfloor + 1$ of Frank and Lazarus are all odd, and this repairs the problem.

**Comparisons on random input.** The counts below are for one random permutation of each size, with the gaps less than $n$ (Knuth's gaps up to about $n/3$), measured with the implementation of Shell sort on this site.

| sequence | $n = 1000$ | $n = 100{,}000$ |
|---|---|---|
| Shell | 14,797 | 4,258,305 |
| Hibbard | 14,274 | 3,915,285 |
| Papernov and Stasevich | 14,993 | 4,101,089 |
| Knuth | 13,718 | 4,322,677 |
| Pratt | 34,380 | 9,373,141 |
| Sedgewick, 1986 | 13,539 | 2,611,067 |
| Tokuda | 13,028 | 2,562,955 |
| Ciura | 13,138 | 2,550,383 |

On random input Shell's gaps are not bad; their $\Theta(n^2)$ shows only on inputs such as the one above. Pratt's gaps have the best worst case of the table but the most passes, so they make the most comparisons on random input. The sequences of Sedgewick, Tokuda and Ciura make about 40 percent fewer comparisons than the others at $n = 100{,}000$, and $n \lg n$ is about 1,660,964 for this size.

**Why Knuth's gaps stop at $n/3$.** A gap close to $n$ sorts only a few pairs, and its pass costs about $n - h$ comparisons for little effect. Knuth starts with the largest gap $h_t$ such that $h_{t+2} \ge n$, which is about $n/9$; Sedgewick and Wayne start at the largest gap below $n/3$.

## Where it is used

- **[Shell sort](/shell-sort/).** Each implementation of Shell sort must choose a sequence. Sedgewick and Wayne use $1, 4, 13, 40, \ldots$ because it is easy to compute, and implementations that want speed often use Ciura's gaps or Sedgewick's 1986 gaps.
- **Sorting networks.** Pratt's sequence gives a [sorting network](/sorting-network/) of depth $O(\log^2 n)$, because each pass is a fixed set of compare-exchange steps between neighbours in the chains. Pratt's thesis studies Shell sort and sorting networks together.
- **[Comb sort](/comb-sort/).** Comb sort applies the idea of shrinking gaps to bubble sort, with a gap that shrinks by a factor of about 1.3 in each pass.
- **The analysis of algorithms.** The best gap sequence and the average time of Shell sort are among the oldest open problems in the analysis of sorting; Sedgewick's survey lists them.

## References
