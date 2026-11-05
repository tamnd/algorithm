---
tag: ZW59T3
kind: problem
slug: maximum-subarray-problem
name: Maximum subarray problem
aliases:
- maximum contiguous subarray problem
- maximum subarray sum
area: sequences/subarray-problems
level: intro
summary: Find the contiguous subarray with the largest sum in an array that may contain negative numbers.
prereqs: [subarray, prefix-sums]
see_also: [kadane-algorithm, maximum-subarray-divide-and-conquer, maximum-sum-submatrix, maximum-circular-subarray-sum, k-maximum-subarray-problem, maximum-density-segment, high-scoring-segment-pair, maximum-product-subarray]
sources:
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the whole column (the problem, its origin, and the cubic, quadratic, n log n and linear algorithms)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm Design Techniques, Sections 8.1 to 8.4
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 4.1, The maximum-subarray problem, and Exercise 4.1-5
  - paper: doi:10.3390/a16110519
    title: "Joseph B. Kadane, Two Kadane Algorithms for the Maximum Sum Subarray Problem, Algorithms 16(11) (2023), 519"
    locator: the history of the problem and the two linear algorithms
  - paper: doi:10.1016/s1571-0661(04)00313-5
    title: "Tadao Takaoka, Efficient Algorithms for the Maximum Subarray Problem by Distance Matrix Multiplication, Electronic Notes in Theoretical Computer Science 61 (2002), 191-200"
    locator: the reduction of the two-dimensional problem to distance matrix multiplication
  - paper: "Walter L. Ruzzo and Martin Tompa, A linear time algorithm for finding all maximal scoring subsequences, Proceedings of the 7th International Conference on Intelligent Systems for Molecular Biology (ISMB 1999), 234-241"
    locator: the linear-time algorithm for all maximal segments
  - url: https://arxiv.org/abs/1602.05837
    title: "Arturs Backurs, Nishanth Dikkala and Christos Tzamos, Tight Hardness Results for Maximum Weight Rectangles, ICALP 2016"
    locator: the conditional cubic lower bound for the two-dimensional problem
---

The maximum subarray problem asks, for an array of numbers that may be negative, for the [subarray](/subarray/) of consecutive items whose sum is largest. It is easy to state, it has algorithms at every level of the usual hierarchy, cubic, quadratic, $n \log n$ and linear, and for this reason Jon Bentley used it in 1984 as the model example of algorithm design. The linear answer is [Kadane's algorithm](/kadane-algorithm/), and the problem is solved in $\Theta(n)$ time, which is optimal. Its two-dimensional form, the [maximum sum submatrix](/maximum-sum-submatrix/), is much harder.

## In plain words

You have a list of daily gains and losses. You want to pick one stretch of days in a row, so that the total over the stretch is as large as possible. If all the numbers were positive, the answer would be the whole list. The losses make it hard: a stretch may be worth taking even with some losses inside, if the gains on both sides make up for them.

There are many stretches, about half the square of the number of days, so trying them all is slow. The good methods use the fact that a best stretch never starts with a part whose total is negative. Cutting such a part off would only make the total larger.

## Definition

**Input.** An array $A[1..n]$ of real numbers, with $n \ge 1$.

**Output.** Indices $1 \le i \le j \le n$ that maximize

$$S(i, j) = A[i] + A[i+1] + \dots + A[j],$$

and the value $S^* = \max_{i \le j} S(i, j)$.

**The empty subarray.** Two conventions are in use. If the empty subarray, with sum $0$, is allowed, then $S^* \ge 0$, and an array of negative numbers has answer $0$. This is the convention of Bentley. If the subarray must be non-empty, then for an array of negative numbers the answer is its largest item. This is the convention of most textbooks and judges, such as CLRS. The two answers are equal whenever some item is non-negative.

**With prefix sums.** Let $P_0 = 0$ and $P_k = A[1] + \dots + A[k]$, the [prefix sums](/prefix-sums/). Then $S(i, j) = P_j - P_{i-1}$, so

$$S^* = \max_{0 \le a < b \le n} (P_b - P_a).$$

The problem is to find the largest rise, from an earlier point to a later point, in the sequence $P$. This is the same problem as the best single buy and sell of a stock, with $P$ as the price.

## Variants

- **Circular.** The array is a ring and a subarray may wrap around the end, see [maximum circular subarray sum](/maximum-circular-subarray-sum/).
- **Fixed or bounded length.** The subarray has length exactly $k$, see [maximum sum subarray of fixed length](/maximum-sum-subarray-of-fixed-length/), or length between $L$ and $U$, solved in $O(n)$ with a [monotonic deque](/monotonic-deque/) over the prefix sums.
- **$k$ subarrays.** The $k$ largest sums, or $k$ disjoint subarrays of largest total, see the [k-maximum subarray problem](/k-maximum-subarray-problem/).
- **All maximal segments.** List every maximal-scoring segment, as in the analysis of biological sequences: Ruzzo and Tompa (1999) do this in linear time.
- **Two dimensions.** A rectangle of a matrix, see the [maximum sum submatrix](/maximum-sum-submatrix/).
- **Other aggregates.** Largest product, see the [maximum product subarray](/maximum-product-subarray/); largest average with a length bound, see the [maximum density segment](/maximum-density-segment/); largest XOR, see the [maximum XOR subarray](/maximum-xor-subarray/).
- **Online and streaming.** The items arrive one at a time and the best sum so far is reported after each. Kadane's algorithm does this with $O(1)$ words of memory.

## Examples

**Bentley's example.** For $A = [31, -41, 59, 26, -53, 58, 97, -93, -23, 84]$ the maximum subarray is $A[3..7] = [59, 26, -53, 58, 97]$ with sum $187$. It contains the negative item $-53$, because the items on both sides make up for it.

**CLRS's example.** For the daily price changes $A = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]$ the maximum subarray is $A[8..11] = [18, 20, -7, 12]$ with sum $43$. Buying before day 8 and selling after day 11 gives the largest profit.

**All negative.** For $A = [-3, -1, -2]$ the answer is $-1$, the subarray $A[2..2]$, under the non-empty convention, and $0$, the empty subarray, under Bentley's.

**All non-negative.** If no item is negative, the whole array is a maximum subarray.

## Known algorithms

| method | time | extra space | idea |
|---|---|---|---|
| try all pairs, sum each | $\Theta(n^3)$ | $O(1)$ | three nested loops |
| try all pairs with running sums or prefix sums | $\Theta(n^2)$ | $O(1)$ or $O(n)$ | $S(i, j) = S(i, j-1) + A[j]$ |
| [divide and conquer](/maximum-subarray-divide-and-conquer/) | $\Theta(n \log n)$ | $O(\log n)$ | best of left half, right half and crossing |
| [Kadane's algorithm](/kadane-algorithm/) | $\Theta(n)$ | $O(1)$ | best sum ending at each position |
| minimum prefix scan | $\Theta(n)$ | $O(1)$ | $\max_b (P_b - \min_{a < b} P_a)$ |
| parallel, with [all prefix sums](/all-prefix-sums/) | $O(\log n)$ with $O(n / \log n)$ processors | $O(n)$ | prefix sums, prefix minima, one maximum |

The divide-and-conquer method can also run in $\Theta(n)$ if each recursive call returns the total, the best prefix and the best suffix of its part along with the best subarray. Then the crossing case costs $O(1)$, and the recurrence is $T(n) = 2T(n/2) + O(1)$. This form gives the [segment tree for maximum subsegment sum](/segment-tree-maximum-subsegment-sum/), which answers the problem on any range of a changing array in $O(\log n)$ time.

## Bounds

**Linear time is optimal.** Every algorithm must read every item. If an algorithm does not read $A[k]$, an adversary sets $A[k]$ to a number larger than the sum of the absolute values of all other items. Then the answer must contain $A[k]$, and the algorithm cannot know this. So $\Omega(n)$ time is needed, and Kadane's algorithm reaches it with $O(1)$ extra space. This is an [adversary argument](/adversary-argument/).

**Two dimensions.** On an $n \times n$ matrix the column sweep with Kadane takes $O(n^3)$ time. Tamaki and Tokuyama (1998) and Takaoka (2002) reduce the problem to [min-plus matrix multiplication](/min-plus-matrix-multiplication/) and get slightly subcubic time. Backurs, Dikkala and Tzamos (2016) showed that an $O(n^{3 - \varepsilon})$ algorithm for the two-dimensional problem would refute the [APSP conjecture](/apsp-conjecture/), so the cubic time is essentially the best possible unless that conjecture fails.

## Reductions

- **To the largest rise in prefix sums.** By the identity $S(i, j) = P_j - P_{i-1}$, the problem is the largest $P_b - P_a$ with $a < b$, which one scan with a running minimum solves.
- **Stock trading.** Given prices $p_0, \dots, p_n$, the best profit of one purchase and one later sale is $\max_{a < b}(p_b - p_a)$, which is the maximum subarray of the daily changes $A[k] = p_k - p_{k-1}$.
- **Two dimensions to one.** For each pair of rows, sum the columns between them into one array and solve the one-dimensional problem; see the [Bentley column sweep](/bentley-column-sweep/).
- **Circular to linear.** A wrapping subarray is the complement of a non-wrapping one, so the circular answer is the larger of the plain maximum and the total minus the plain minimum; see the [circular Kadane algorithm](/circular-kadane-algorithm/).
- **Local alignment.** With a scoring scheme that gives each position a score, the best ungapped [local alignment](/local-alignment/) of two fixed diagonals is a maximum subarray of the scores.

## Applications

- **Pattern recognition.** Ulf Grenander posed the two-dimensional form as a maximum likelihood estimate of the brightest rectangular region in a digitized picture. The one-dimensional form was the simplification that he and Bentley studied first.
- **Biological sequences.** With scores per residue, such as hydrophobicity or GC content, maximal-scoring segments locate transmembrane regions, DNA binding domains and regions of high GC content. Karlin and Altschul (1990) gave the statistics of the [high-scoring segment pairs](/high-scoring-segment-pair/) behind BLAST.
- **Finance.** The best single trade in a price series, and the period of largest gain or largest loss.

## References
