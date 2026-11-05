---
tag: XPC0T3
kind: problem
slug: parallel-merging-problem
name: Parallel merging problem
aliases:
- parallel merge
area: sorting/parallel-sorting
level: core
summary: Merge two sorted sequences using many processors at once.
prereqs: [merging-sorted-lists, binary-search, pram-model, work-span-model]
see_also: [merge-path, shiloach-vishkin-merge, valiant-parallel-merge, parallel-merge-sort, cole-merge-sort, merging-lower-bound, parallel-sorting-problem, merging-network]
sources:
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 4, Searching, merging and sorting (merging by ranking on the CREW PRAM)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.3, Parallel merge sort (the procedure P-MERGE, with work Theta(n) and span Theta(log^2 n))
  - paper: doi:10.1137/0204030
    title: Leslie G. Valiant, Parallelism in comparison problems, SIAM Journal on Computing 4(3), 1975
    locator: merging in O(log log n) rounds in the parallel comparison model
  - paper: "Allan Borodin and John E. Hopcroft, Routing, merging, and sorting on parallel models of computation, Journal of Computer and System Sciences 30(1), 1985"
    locator: the lower bound of Omega(log log n) rounds for merging with n processors in the parallel comparison model
  - paper: doi:10.1016/0196-6774(81)90010-9
    title: Yossi Shiloach and Uzi Vishkin, Finding the maximum, merging, and sorting in a parallel computation model, Journal of Algorithms 2(1), 1981
    locator: merging in depth O(n/p + log n) with p processors, and in depth O(k) with about m^(1/k) n processors
  - paper: "Clyde P. Kruskal, Searching, merging, and sorting in parallel computation, IEEE Transactions on Computers C-32(10), 1983"
    locator: merging on the CREW PRAM in O(log log n) time with n / log log n processors
---

The parallel merging problem asks to merge two sorted sequences $A$ and $B$ into one sorted sequence with many processors that work at the same time. It is the [merging problem](/merging-sorted-lists/) with parallel time as a second cost, and it is the inner step of [parallel merge sort](/parallel-merge-sort/). The key fact is that each item can find its own output position by a [binary search](/binary-search/) in the other sequence, so the items do not need to wait for each other.

## In plain words

Two sorted queues of people must become one sorted queue. One usher can do it alone by always letting the smaller of the two front people go first. That takes one step per person.

With many ushers, each person can find their own place. A person in the first queue counts how many people in the second queue are smaller, and adds their own place in the first queue. The sum is their place in the final queue. Everybody can do this at the same time, so the merge takes only as long as one search. The open questions are how few steps are possible, and how to share the work so that no usher does much more than the others.

## Definition

**Input.** Sorted sequences $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ of keys from a total order, $A[0] \le \cdots \le A[m-1]$ and $B[0] \le \cdots \le B[n-1]$, usually with $m \le n$.

**Output.** An array $C[0 \ldots m+n-1]$ that holds the items of $A$ and $B$ in non-decreasing order. In the *stable* version, each item of $A$ comes before each equal item of $B$, and the items of each input keep their order.

**Cross ranks.** For an item $a = A[i]$, let $\operatorname{rank}_B(a)$ be the number of items of $B$ that are less than $a$. For an item $b = B[j]$, let $\operatorname{rank}_A(b)$ be the number of items of $A$ that are at most $b$. The stable merge puts

$$A[i] \text{ at } C[i + \operatorname{rank}_B(A[i])], \qquad B[j] \text{ at } C[j + \operatorname{rank}_A(B[j])].$$

*Proof.* Order the $m + n$ items by key, and break each tie by putting the item of $A$ first and, within one input, the item with the smaller index first. This is a strict total order, and the stable merge lists the items in this order. The items before $A[i]$ in this order are $A[0], \ldots, A[i-1]$ and the items $B[j]$ with $B[j] < A[i]$, which are $\operatorname{rank}_B(A[i])$ items. The items before $B[j]$ are $B[0], \ldots, B[j-1]$ and the items $A[i]$ with $A[i] \le B[j]$, which are $\operatorname{rank}_A(B[j])$ items. An item with $q$ items before it is at position $q$. $\square$

**Costs.** As for the [parallel sorting problem](/parallel-sorting-problem/), each bound names a model: a [PRAM](/pram-model/) variant with $p$ processors (time and work), the [work-span model](/work-span-model/) (work $T_1$ and span $T_\infty$), or the parallel comparison model (rounds, where $p$ processors make one comparison each per round and all other work is free).

## Variants

- **Equal lengths or very unequal lengths.** The case $m = n$ is the inner step of merge sort. When $m$ is much smaller than $n$, the information bound $\lg \binom{m+n}{m}$ is much smaller than $m + n$, and merging by binary searches of the short list is better.
- **Partitioned merge.** Cut the output into $p$ pieces of nearly equal length so that each processor merges one piece with the sequential merge. [Merge path](/merge-path/) finds the cuts by binary search on the diagonals of the merge grid.
- **Multiway merge.** Merge $k$ sorted sequences at once, as in the last phase of [sample sort](/sample-sort/) and of [parallel sorting by regular sampling](/parallel-sorting-by-regular-sampling/).
- **Oblivious merge.** A [merging network](/merging-network/) makes the same comparisons on each input. For $m = n = 2^k$, Batcher's odd-even and bitonic mergers have depth $k + 1 = \lg(m+n)$ and size $\Theta(n \log n)$.

## Examples

**Cross ranks.** Let $A = [1, 4, 6, 9]$ and $B = [2, 3, 7, 8, 10]$.

| item | 1 | 4 | 6 | 9 | 2 | 3 | 7 | 8 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| from | $A[0]$ | $A[1]$ | $A[2]$ | $A[3]$ | $B[0]$ | $B[1]$ | $B[2]$ | $B[3]$ | $B[4]$ |
| rank in the other list | 0 | 2 | 2 | 4 | 1 | 1 | 3 | 3 | 4 |
| output position | 0 | 3 | 4 | 7 | 1 | 2 | 5 | 6 | 8 |

So $C = [1, 2, 3, 4, 6, 7, 8, 9, 10]$. With 9 processors, each item does one binary search in parallel, of $\lceil \lg 6 \rceil = 3$ steps for an item of $A$ (6 possible ranks) and $\lceil \lg 5 \rceil = 3$ steps for an item of $B$ (5 possible ranks), and one write.

**Ties.** Let $A = [2, 5]$ and $B = [2, 5]$. The ranks give $A[0] \to 0$, $A[1] \to 0 + 1 + 1 = 2$, $B[0] \to 0 + 1 = 1$ and $B[1] \to 1 + 2 = 3$. So $C$ lists the 2 of $A$, the 2 of $B$, the 5 of $A$ and the 5 of $B$, and the merge is stable. If both inputs used "less than" for the rank, both items 2 would go to position 0.

**Work and time.** For $m = n = 2^{20}$, the sequential merge makes at most $2^{21} - 1$ comparisons. The cross-rank method with $2^{21}$ processors makes about $2^{21} \cdot 21$ comparisons in about 21 steps. With $p = 2^{21} / 21 \approx 99864$ processors and the partitioned merge, each processor merges about 21 items, and both the time and the work are within a constant factor of the best.

## Known algorithms

| algorithm | model | time | work or processors |
| --- | --- | --- | --- |
| cross ranks by binary search | CREW PRAM, $m + n$ processors | $O(\log n)$ | $O((m+n)\log n)$ work |
| [Merge path](/merge-path/), [Shiloach-Vishkin](/shiloach-vishkin-merge/) | CREW PRAM, $p \le n$ processors | $O(n/p + \log n)$ | $O(n + p \log n)$ work |
| P-MERGE of CLRS | work-span | span $\Theta(\log^2 n)$ | work $\Theta(n)$ |
| partitioned merge with $p = n/\log n$ pieces | work-span | span $O(\log n)$ | work $O(n)$ |
| [Valiant's merge](/valiant-parallel-merge/) | parallel comparison model, $m + n$ processors | $O(\log \log n)$ rounds | $O((m+n)\log\log n)$ comparisons |
| Kruskal's merge | CREW PRAM, $n / \log \log n$ processors | $O(\log \log n)$ | $O(n)$ work |
| Shiloach-Vishkin with $\lceil m^{1/k} n \rceil$ processors | the comparison model of Shiloach and Vishkin | $O(k)$ | |
| Batcher's merger, $m = n = 2^k$ | comparator network | depth $k + 1$ | $\Theta(n \log n)$ comparators |

## Bounds

**Work.** In the [comparison model](/comparison-model/), merging needs at least $\lceil \lg \binom{m+n}{m} \rceil$ comparisons, and $m + n - 1$ when $|m - n| \le 1$. See the [merging lower bound](/merging-lower-bound/). So for $m = n$ the work of a parallel merge is $\Omega(n)$, and the methods with $O(n)$ work are work-efficient.

**Rounds in the comparison model.** With $n$ processors, Valiant's merge uses $O(\log \log n)$ rounds, and Borodin and Hopcroft proved that $\Omega(\log \log n)$ rounds are needed for $m = n$. So merging takes $\Theta(\log \log n)$ rounds in this model, while sorting takes $\Theta(\log n)$.

**PRAM time.** Kruskal's merge reaches $O(\log \log n)$ time on the CREW PRAM with linear work. Any merge with $p$ processors needs at least $(m + n)/p$ steps to write the output, and at least about $\lg \binom{m+n}{m} / p$ steps for the comparisons. On the EREW PRAM, the binary searches cannot share reads of one cell, and the known work-efficient merges take $O(\log n)$ time.

**Depth of a network.** Let $m = n$. On sorted inputs, the output $C[n-1]$ can be equal to any one of the $2n$ inputs, and then it changes when that input changes by a small amount. So $C[n-1]$ depends on all $2n$ inputs, and a network of gates of fan-in 2 needs depth at least $\lceil \lg 2n \rceil$. Batcher's mergers meet this bound for $n = 2^k$.

## Reductions

- **Merging to ranking.** By the cross-rank formula, a merge is the same as computing $\operatorname{rank}_B$ for each item of $A$ and $\operatorname{rank}_A$ for each item of $B$. Each rank is a [binary search](/binary-search/), and the searches are independent.
- **Ranking a sample.** It is enough to rank every $k$-th item of $A$ in $B$ and every $k$-th item of $B$ in $A$. These ranks cut both lists into pieces of at most $k$ items of each list, and the pieces merge independently. This is the base of the Shiloach-Vishkin merge, of merge path and of Valiant's merge.
- **Sorting to merging.** A merge sort with a parallel merge of span $S(n)$ has span $O(S(n) \log n)$. See [parallel merge sort](/parallel-merge-sort/). Cole's [pipelined merge sort](/cole-merge-sort/) avoids the factor $\log n$ by overlapping the merges of different levels.

## Applications

- **Parallel merge sort.** Each level of a parallel merge sort is a set of independent parallel merges.
- **GPU sorting.** GPU merge sorts use merge path to give each thread block the same number of output items.
- **Database operations.** The merge phase of a parallel sort-merge join and the merge of sorted runs in parallel external sorting are parallel merges.
- **Set operations.** Union and intersection of sorted sets use the same ranks, with a test for equal keys.

## References
