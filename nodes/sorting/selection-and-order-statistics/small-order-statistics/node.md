---
tag: E3GDGT
kind: problem
slug: small-order-statistics
name: Small order statistics
area: sorting/selection-and-order-statistics
level: advanced
summary: Finding the i-th smallest element for small i using fewer comparisons than general selection, via tournament style methods.
model: comparison-model
complexity:
  vars: {n: the number of items, i: "the rank sought, a constant or small compared with n"}
  time: {worst: Θ(n)}
prereqs: [selection-problem, tournament-method]
see_also: [tournament-method, tournament-minimum, second-largest-lower-bound, selection-lower-bound, heap-select, top-k-selection, minimum-and-maximum-finding, floyd-rivest-select]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the numbers V_t(n), the Hadian-Sobel upper bound and the lower bounds for small t)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9 problems, Small order statistics (the pairing recursion U_i(n) = n + O(S(2i) lg(n/i)))
  - paper: "Abdollah Hadian and Milton Sobel, Selecting the t-th largest using binary errorless comparisons, Combinatorial Theory and Its Applications, Colloquia Mathematica Societatis János Bolyai 4 (1969)"
    locator: pages 585 to 599 (the bound n - t + (t - 1) ceil(lg(n + 2 - t)))
  - paper: "Frank Fussenegger and Harold N. Gabow, A counting approach to lower bounds for selection problems, Journal of the ACM 26(2) (1979)"
    locator: pages 227 to 238 (the bound n - t + ceil(lg C(n, t - 1)))
  - paper: "S. S. Kislitsyn, On the selection of the k-th element of an ordered set by pairwise comparisons, Sibirskii Matematicheskii Zhurnal 5 (1964)"
    locator: pages 557 to 564 (the exact value for the second largest)
---

Small order statistics is the [selection problem](/selection-problem/) when the rank $i$ is small compared with $n$, such as the second or the tenth smallest of a million items. Then the cost can be pushed close to the $n - 1$ comparisons needed for the minimum: for each fixed $i$, the least worst-case number of comparisons is $n + (i - 1) \lg n + O(1)$. The methods that reach it are built on knockout [tournaments](/tournament-minimum/), in which each comparison knocks out one item and the winner has met only $\lceil \lg n \rceil$ others.

## In plain words

To find the smallest of a million numbers, you must look at each of them, and a single pass that keeps the smallest so far does it. To find the second smallest, two passes would cost twice as much. But almost all of the second pass is wasted, because most numbers were already shown to be bigger than something other than the winner.

A knockout tournament keeps track of who beat whom. The second smallest must have lost only to the winner, and the winner met only about twenty others in a million-item tournament. So the second smallest costs only about twenty more comparisons. The same idea, repeated, gives the third, the fourth, and so on, each for a small extra cost.

## Definition

**Input.** A list of $n$ items with a [total order](/total-order/), and a rank $i$ with $1 \le i \le n$, thought of as small: a constant, or $i = o(n)$.

**Output.** The item of rank $i$, the $i$-th smallest.

**Cost.** The number of comparisons in the worst case. Write $V_i(n)$ for the least worst-case number of comparisons with which any algorithm finds rank $i$ of $n$ distinct items. By symmetry $V_i(n) = V_{n+1-i}(n)$, so small ranks and ranks near $n$ are the same problem.

## Variants

- **Rank $i$ alone, or the $i$ smallest.** The methods below find the $i$ smallest along the way; reporting them as a set costs nothing more, and sorting them costs $O(i \log i)$ more ([top-k selection](/top-k-selection/), [the largest $i$ numbers in sorted order](/largest-i-numbers-in-sorted-order/)).
- **The second smallest.** The case $i = 2$, solved exactly by the [tournament method](/tournament-method/).
- **The minimum and the maximum.** A different small question, with exact answer $\lceil 3n/2 \rceil - 2$ ([minimum and maximum finding](/minimum-and-maximum-finding/)).
- **Average cost.** With random choices, rank $i$ costs $n + i + o(n)$ comparisons in expectation by [Floyd-Rivest selection](/floyd-rivest-select/), less than the worst-case bound when $i$ is a constant.

## Examples

**The second smallest.** For $A = [7, 2, 9, 4, 1, 8, 3, 6]$, a knockout for the minimum makes $7$ comparisons and gives $1$, which beat $8$, $3$ and $2$. Two more comparisons give the second smallest, $2$: $9$ comparisons in total, against $13$ for two scans.

**Pairing.** The same $A$ with $i = 2$, by the pairing method below. Compare in pairs: $2 < 7$, $4 < 9$, $1 < 8$, $3 < 6$, which is $4$ comparisons. The two smallest of the winners $2, 4, 1, 3$ are $1$ and $2$. Each of the two smallest of all items is one of these or a partner of one, so the answer is the second smallest of $\{1, 2, 8, 7\}$, which is $2$.

**Exact values.** $V_1(n) = n - 1$ and $V_2(n) = n + \lceil \lg n \rceil - 2$; so $V_2(8) = 9$ and $V_2(1000) = 1008$. For the median of five, $V_3(5) = 6$.

## Known algorithms

**Repeated scans.** Find the minimum, remove it, and repeat $i$ times: $\sum_{j=0}^{i-1} (n - 1 - j)$, about $i n$ comparisons. Good only for $i = 1$.

**Tournament with replays.** Play a knockout for the minimum and keep the tree. To get the next smallest, remove the winner's leaf and replay only the matches on its path to the root, which costs at most $\lceil \lg n \rceil$ comparisons. Rank $i$ costs $n - 1 + (i - 1)\lceil \lg n \rceil$. This is the first part of [tournament sort](/tournament-sort/), and it also gives the $i$ smallest in sorted order.

**Hadian and Sobel (1969).** Use a smaller tree. Play a knockout on $n - i + 2$ of the items. Its winner is smaller than $n - i + 1$ items, so its rank is at most $i - 1$: it is too small to be the answer, and can be thrown away. Put one of the $i - 2$ items not yet played in its leaf and replay the path. After $i - 2$ such steps, all items are in the tree, the $i - 2$ items thrown away are among the $i - 1$ smallest, and the answer is the second smallest of the tree, found from the winner's beaten list as in the tournament method. The count is

$$ (n - i + 1) + (i - 2) \lceil \lg(n - i + 2) \rceil + \lceil \lg(n - i + 2) \rceil - 1 = n - i + (i - 1) \lceil \lg(n + 2 - i) \rceil. $$

For $i = 2$ this is $n + \lceil \lg n \rceil - 2$, which is optimal.

**Pairing recursion.** For $i < n/2$, compare the items in $\lfloor n/2 \rfloor$ pairs, and keep the smaller item of each pair (and the odd item out). The $i$ smallest items of the input are among the $i$ smallest of the kept items and their partners: if an item is among the $i$ smallest, so is the smaller item of its pair. So find recursively the $i$ smallest of the $\lceil n/2 \rceil$ kept items, and then select rank $i$ among those $i$ items and their at most $i$ partners. With $S(2i)$ the cost of selection on $2i$ items, the cost $U_i(n)$ satisfies

$$ U_i(n) = \lfloor n/2 \rfloor + U_i(\lceil n/2 \rceil) + S(2i), $$

which solves to $n + O(S(2i) \log(n/i))$. With a linear-time selection inside, this is $n + O(i \log(n/i))$. This is the CLRS problem on small order statistics.

**One pass with a heap.** [Heap-based selection](/heap-select/) keeps the $i$ smallest so far in a max-heap of size $i$: $O(n \log i)$ comparisons in the worst case, but about $n + O(i \log i \log(n/i))$ on random input, and it reads the items as a stream.

## Bounds

- **Upper bound.** $V_i(n) \le n - i + (i - 1)\lceil \lg(n + 2 - i) \rceil$, by Hadian and Sobel.
- **Lower bound.** $V_i(n) \ge n - i + \lceil \lg \binom{n}{i-1} \rceil$, by Fussenegger and Gabow (1979). The simpler [selection lower bound](/selection-lower-bound/) $n - 1 + \min(i - 1, n - i)$ is weaker for small $i$.
- **Fixed $i$.** Since $\lg \binom{n}{i-1} = (i - 1) \lg n - \lg((i - 1)!) - o(1)$ for fixed $i$, the two bounds differ by an amount that depends only on $i$, so $V_i(n) = n + (i - 1)\lg n + O(1)$ for each fixed $i$.
- **Exact cases.** $V_1(n) = n - 1$ ([max-finding lower bound](/max-finding-lower-bound/)) and $V_2(n) = n + \lceil \lg n \rceil - 2$, proved by Kislitsyn in 1964 ([second largest lower bound](/second-largest-lower-bound/)). For $i \ge 3$ exact values are known only for small $n$ and some ranges; Knuth's Section 5.3.3 tables them.

## Reductions

- **To general selection.** Each selection algorithm solves this problem, but the linear-time worst-case methods make several times $n$ comparisons, far more than $n + O(\log n)$.
- **Rank $n + 1 - i$.** Reverse the order: the $i$-th largest has the same cost as the $i$-th smallest.
- **From the $i$ smallest.** Once the $i$ smallest are known, rank $i$ is their maximum, with $i - 1$ more comparisons, and rank $i + 1$ is a small selection among the items that lost directly to them.

## Applications

- **Contests and rankings.** The second and third prize of a knockout tournament, the problem that started the subject.
- **Top results.** A search for the best few matches among many, where comparisons are expensive, as in [top-k selection](/top-k-selection/) with a costly score.
- **Robust extremes.** The second or third largest value of a sample is a common guard against a single outlier, and it costs little more than the maximum.

## References
