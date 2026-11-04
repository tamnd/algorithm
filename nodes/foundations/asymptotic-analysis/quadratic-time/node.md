---
tag: F3NSM5
kind: concept
slug: quadratic-time
name: Quadratic time
area: foundations/asymptotic-analysis
level: intro
summary: Running time proportional to the square of the input size, typical of algorithms that examine all pairs or use nested loops.
prereqs: [asymptotic-notation, time-complexity, arithmetic-series]
see_also: [cubic-time, linear-time, linearithmic-time, polynomial-time, common-growth-rates, doubling-hypothesis, insertion-sort, edit-distance]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (analysis of insertion sort), the problems of Chapter 2 (inversions) and Appendix A (summations)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversions) and Section 5.2.1 (sorting by insertion)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.4, A Survey of Common Running Times (quadratic time)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (the doubling ratio)
  - paper: doi:10.1145/2746539.2746612
    title: Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), Proceedings of the 47th ACM Symposium on Theory of Computing (STOC 2015), 51 to 58
    locator: the main theorem on edit distance
  - paper: doi:10.1109/FOCS.2015.14
    title: Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 59 to 78
    locator: the main theorem on the longest common subsequence
---

An algorithm runs in quadratic time when its cost is $\Theta(n^2)$ in the [input size](/input-size/) $n$, in a stated model such as the [word RAM](/word-ram/) and a stated case. The usual cause is a pair of nested loops over the input, or a loop of $n$ rounds that does linear work in each round. The elementary sorts, the brute-force search over all pairs, and the dynamic programs over two sequences such as [edit distance](/edit-distance/) belong to this class. It comes after [linearithmic time](/linearithmic-time/) and before [cubic time](/cubic-time/) in the [common growth rates](/common-growth-rates/), and it is a class of [polynomial time](/polynomial-time/).

## In plain words

Think of a room where each person shakes hands with each other person. Ten people make 45 handshakes. Twenty people make 190. When the number of people doubles, the number of handshakes becomes about four times larger. This is the growth of quadratic time.

A program has this cost when it compares each item with each other item, or when it goes over the whole input once for each item. A program that is fast on a few thousand items can be too slow on a few million. With a thousand times more items, the work is a million times larger.

## The idea

### Definition

Fix a model and a case. Let $T(n)$ be the cost on inputs of size $n$ in that case. The algorithm runs in *quadratic time* when $T(n) = \Theta(n^2)$, and in *at most quadratic time* when $T(n) = O(n^2)$. The second statement also holds for faster algorithms: a linear algorithm is $O(n^2)$. For a statement about doubling, use [tilde notation](/tilde-notation/): if $T(n) \sim a n^2$ with $a > 0$, then $T(2n)/T(n) \to 4$. From $T(n) = \Theta(n^2)$ alone, the ratio only stays between two positive constants.

### Loop shapes and their exact counts

Let the body of the inner loop cost one step. The counts are exact for the loops as written.

- Two independent loops, `for i in 1..n` and `for j in 1..n`: $n^2$ runs of the body. For $n = 8$, 64.
- `for j in i+1..n`: $\sum_{i=1}^{n} (n - i) = n(n-1)/2 = \binom{n}{2}$, the number of pairs $i < j$. For $n = 8$, 28.
- `for j in 1..i`: $\sum_{i=1}^{n} i = n(n+1)/2$. For $n = 8$, 36.

The [arithmetic series](/arithmetic-series/) page proves $\sum_{i=1}^{n} i = n(n+1)/2$. The sum $\sum_{i=1}^{n} (n-i)$ has the terms $n - 1, n - 2, \ldots, 0$, so it equals $\sum_{i=1}^{n-1} i = n(n-1)/2$. For $n \ge 1$, $n^2/2 \le n(n+1)/2 \le n^2$. For $n \ge 2$, $n - 1 \ge n/2$, so $n^2/4 \le n(n-1)/2 \le n^2/2$. So each count is $\Theta(n^2)$. The ratio of the count $n(n-1)/2$ at $2n$ and at $n$ is $2(2n-1)/(n-1)$, which is $4.002$ for $n = 1000$ and tends to 4.

**Nested loops that are not quadratic.** The nesting does not decide the class. The count does.

- The inner index doubles, `j = 1; while j <= n: j = 2j`: the inner loop runs $\lfloor \lg n \rfloor + 1$ times, so the body runs $n(\lfloor \lg n \rfloor + 1)$ times, 32 for $n = 8$. This is [linearithmic](/linearithmic-time/).
- The outer index doubles and the inner loop runs to it, `i = 1; while i <= n: (for j in 1..i); i = 2i`: the body runs $1 + 2 + 4 + \cdots + 2^{\lfloor \lg n \rfloor} = 2^{\lfloor \lg n \rfloor + 1} - 1 < 2n$ times, 15 for $n = 8$. This is [linear](/linear-time/), by a [geometric series](/geometric-series/).
- Conversely, a single loop of $n$ rounds whose body calls a function of cost $\Theta(n)$, such as a search in an unsorted list, is quadratic.

### Worked example: insertion sort and inversions

An *inversion* of an array $A$ is a pair of positions $i < j$ with $A[i] > A[j]$. [Insertion sort](/insertion-sort/) moves each item left past the larger items before it, one position at a time, so it makes exactly one shift for each inversion. The number of key comparisons is the number of shifts plus at most one comparison for each of the $n - 1$ insertions, the one that stops the inner loop.

*Claim.* Each algorithm that sorts by swaps of adjacent items makes at least $n(n-1)/2$ swaps on the reversed array, so it takes $\Omega(n^2)$ time in the worst case.

*Proof.* A swap of two adjacent items $A[k]$ and $A[k+1]$ changes the relative order of that one pair and of no other pair, so it changes the number of inversions by exactly 1. A sorted array has 0 inversions. The reversed array $n, n-1, \ldots, 1$ has each of its $\binom{n}{2}$ pairs inverted. So at least $\binom{n}{2}$ swaps are needed. $\square$

On the reversed array of 8 items, insertion sort makes 28 shifts and 28 comparisons. On the reversed array of 1000 items it makes 499500 of each. On a sorted array of 8 items it makes 7 comparisons and no shift. A random permutation of $n$ distinct items has $n(n-1)/4$ inversions in expectation, because each pair is inverted with probability $1/2$, so the average case is also $\Theta(n^2)$ (Knuth, Section 5.1.1).

### Cost in practice

At $10^9$ simple steps per second, $n = 10^5$ means $10^{10}$ steps, about 10 seconds, and $n = 10^6$ means $10^{12}$ steps, about 17 minutes. The largest $n$ with $n^2 \le 10^9$ is 31622. Each doubling of $n$ multiplies the time by about 4, and the [doubling hypothesis](/doubling-hypothesis/) uses this ratio to find the class from measured times.

### Pitfalls

- **The measure of input size.** A quadratic time in the number of vertices $V$ of a graph given as a $V \times V$ adjacency matrix is linear in the size of the input, which is $V^2$ entries. In the other direction, an algorithm that is $\Theta(V^2)$ on a sparse graph with $E = O(V)$ edges in adjacency lists is quadratic in its input size. Always say what $n$ counts.
- **Two sizes.** Edit distance of strings of lengths $m$ and $n$ takes $\Theta(mn)$ time. It is quadratic only when $m = \Theta(n)$. For $m = 10$ and $n = 10^6$ it is linear in $n$. See [multivariate asymptotic notation](/multivariate-asymptotic-notation/).
- **Pseudo-polynomial is not quadratic.** A dynamic program with a table of $n \times W$ cells, such as the one for the [knapsack problem](/knapsack-problem/), is not "quadratic" when $W$ is a number in the input. Its time is polynomial in the value $W$ and exponential in the $\lg W$ bits that encode it. See [pseudo-polynomial time](/pseudo-polynomial-time/).
- **The model of computation.** The school method for the product of two numbers of $n$ digits makes $n^2$ digit products, so it is quadratic in the bit model. In the word RAM with unit-cost multiplication of one-word numbers, the same product of two numbers that fit in a word is one step. The class depends on what one step is. See [unit-cost model](/unit-cost-model/).
- **Hidden linear steps.** String concatenation in a loop, insertion at the front of an array, and a membership test in a list each cost $\Theta(n)$. In a loop of $n$ rounds they make the loop quadratic, with no visible nested loop.
- **Name the case.** Insertion sort is $\Theta(n)$ in the best case and $\Theta(n^2)$ in the worst and the average case. [Quicksort](/quicksort/) is $\Theta(n^2)$ only in the worst case.

## Examples

- [Selection sort](/selection-sort/) makes $n(n-1)/2$ comparisons on each input, because the search for the minimum of the unsorted part does not depend on the values. Its time is $\Theta(n^2)$ in each case.
- Plain [bubble sort](/bubble-sort/), without a test for an early stop, compares adjacent items $(n-1) + (n-2) + \cdots + 1 = n(n-1)/2$ times on each input.
- The brute-force search for the [closest pair of points](/closest-pair-of-points/) computes $\binom{n}{2}$ distances. Divide and conquer solves the problem in $O(n \log n)$ time.
- The [school method of multiplication](/schoolbook-multiplication/) for two numbers of $n$ digits makes $n^2$ digit products. [Karatsuba multiplication](/karatsuba-multiplication/) makes $O(n^{\lg 3})$ digit operations, with $\lg 3 \approx 1.585$.
- [Edit distance](/edit-distance/) and the [longest common subsequence](/longest-common-subsequence/) of sequences of lengths $m$ and $n$ fill a table of $(m+1)(n+1)$ cells with constant work in each, so $\Theta(mn)$ time. Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), edit distance has no algorithm with time $O(n^{2-\varepsilon})$ for a constant $\varepsilon > 0$ (Backurs and Indyk, 2015), and neither has the longest common subsequence over a constant-size alphabet (Abboud, Backurs and Vassilevska Williams, 2015). These are conditional results, not proofs of a lower bound.
- The standard algorithm for [3SUM](/3sum/) sorts the numbers and runs two pointers for each choice of the first number, in $O(n^2)$ time. The 3SUM conjecture says that no algorithm with time $O(n^{2-\varepsilon})$ exists on the word RAM for integer inputs. It is a conjecture, not a theorem.
- Non-example: [merge sort](/merge-sort/) takes $\Theta(n \log n)$ time. It is $O(n^2)$, but not quadratic, because $n \lg n / n^2 \to 0$.
- Non-example: a nested loop whose inner loop runs 3 times makes $3n$ steps and is linear.

## Where it is used

Quadratic algorithms are a good first choice when the input is small or the code must be simple, and library sorts switch to insertion sort for short ranges because its constant factor is small. For large inputs the standard step is to replace the loop over all pairs by a sort or a balanced tree, which gives a [linearithmic](/linearithmic-time/) bound, or by a hash table, which gives expected [linear](/linear-time/) time. Dynamic programs over pairs of positions take quadratic time, and for edit distance and the longest common subsequence the space can be cut to linear by [Hirschberg's algorithm](/hirschberg-algorithm/). The conditional lower bounds above explain why no strongly subquadratic algorithm for these problems has been found.

## References
