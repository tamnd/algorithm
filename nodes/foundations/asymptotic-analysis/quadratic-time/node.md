---
tag: F3NSM5
kind: concept
slug: quadratic-time
name: Quadratic time
area: foundations/asymptotic-analysis
level: intro
summary: Running time proportional to the square of the input size, typical of algorithms that examine all pairs or use nested loops.
prereqs: [asymptotic-notation, time-complexity, arithmetic-series]
see_also: [cubic-time, linear-time, linearithmic-time, polynomial-time, common-growth-rates, doubling-hypothesis, insertion-sort, selection-sort]
sources:
  - url: "https://en.wikipedia.org/wiki/Time_complexity"
    locator: section Polynomial time
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 2.4
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2 (insertion sort) and Appendix A (summations)
  - paper: "Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), STOC 2015"
    locator: the main theorem on edit distance
  - paper: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, FOCS 2015"
    locator: the main theorem on the longest common subsequence
---

An algorithm runs in quadratic time when its worst-case [time](/time-complexity/) is $\Theta(n^2)$ in the input size $n$, in a stated model such as the [word RAM](/word-ram/). The usual cause is a pair of nested loops that range over the input, or a loop of $n$ rounds that does a linear amount of work in each round. The elementary sorts, the brute-force search over all pairs, and many dynamic programs over two sequences belong to this class. In the usual list of [common growth rates](/common-growth-rates/), it comes right after the [linearithmic](/linearithmic-time/) class and before [cubic time](/cubic-time/). It is a class of [polynomial time](/polynomial-time/).

## In plain words

Think of a room with a number of people, where each person shakes hands with each other person. Ten people make 45 handshakes. Twenty people make 190. When the number of people doubles, the number of handshakes becomes about four times larger. This is the growth of quadratic time.

A program has this cost when it compares each item with each other item, or when it goes over the whole input once for each item. A program that is fast on a few thousand items can be too slow on a few million. With a thousand times more items, the work is a million times larger.

## The idea

**Definition.** Fix a model and a case. Let $T(n)$ be the number of steps on inputs of size $n$ in that case (worst, average or best). The algorithm runs in *quadratic time* when $T(n) = \Theta(n^2)$. It runs in *at most quadratic time* when $T(n) = O(n^2)$. The second statement includes the algorithms that are faster, so a linear algorithm is also $O(n^2)$. Use $\Theta$ for the class and $O$ for a bound. For a precise statement about doubling, use [tilde notation](/tilde-notation/): if $T(n) \sim a n^2$ with $a > 0$, then $T(2n)/T(n) \to 4$. The weaker statement $T(n) = \Theta(n^2)$ gives only that the ratio stays between two positive constants.

**Loop shapes and their exact counts.** Let the body of the inner loop cost one step. The counts below are exact for the loops as written.

- Two independent loops, `for i in 1..n` and `for j in 1..n`: the body runs $n^2$ times. For $n = 8$ it runs 64 times.
- The inner loop starts after the outer index, `for j in i+1..n`: the body runs $\sum_{i=1}^{n} (n - i) = n(n-1)/2 = \binom{n}{2}$ times. This is the number of pairs $i < j$. For $n = 8$ it is 28.
- The inner loop stops at the outer index, `for j in 1..i`: the body runs $\sum_{i=1}^{n} i = n(n+1)/2$ times. For $n = 8$ it is 36.
- One loop of $n$ rounds in which round $i$ costs $\Theta(i)$ or $\Theta(n)$, such as a scan or a shift of an array: the total is $\Theta(n^2)$ in both cases. The case $\Theta(i)$ is an [arithmetic series](/arithmetic-series/).

The page on [arithmetic series](/arithmetic-series/) proves that $\sum_{i=1}^{n} i = n(n+1)/2$. The sum $\sum_{i=1}^{n} (n-i)$ has the same terms in reverse order, with the last term 0, so it equals $\sum_{i=1}^{n-1} i = n(n-1)/2$. Since $n(n+1)/2 \ge n^2/2$ and $n(n+1)/2 \le n^2$ for $n \ge 1$, the count $n(n+1)/2$ is $\Theta(n^2)$. For $n \ge 2$ we have $n - 1 \ge n/2$, so $n^2/4 \le n(n-1)/2 \le n^2/2$, and the count $n(n-1)/2$ is $\Theta(n^2)$ too. The count $n^2$ is $\Theta(n^2)$ by definition.

**Nested loops that are not quadratic.** Two nested loops do not always make quadratic time. The count depends on how the inner bound changes.

- The inner index doubles, `j = 1; while j <= n: j = 2j`. The inner loop runs $\lfloor \lg n \rfloor + 1$ times, so the whole code runs $n(\lfloor \lg n \rfloor + 1)$ times. For $n = 8$ this is 32. The class is [linearithmic](/linearithmic-time/).
- The outer index doubles and the inner loop runs to it, `i = 1; while i <= n: (for j in 1..i); i = 2i`. The body runs $1 + 2 + 4 + \dots + 2^{\lfloor \lg n \rfloor} = 2^{\lfloor \lg n \rfloor + 1} - 1 < 2n$ times. For $n = 8$ this is 15. The class is [linear](/linear-time/). The sum is a [geometric series](/geometric-series/).
- One loop of $n$ rounds with constant work per round, `for i in 1..n`, is linear, even when the code is long.

The other direction also holds: a single loop can be quadratic. A loop of $n$ rounds in which each round calls a function that costs $\Theta(n)$, for example a search in an unsorted list, is quadratic.

**Cost in practice.** If a step costs one nanosecond, $n = 10^5$ means $10^{10}$ steps and about 10 seconds. With $n = 10^6$ the same code needs about $10^{12}$ steps, which is about 1000 seconds. Each doubling of $n$ multiplies the time by about 4, and the [doubling hypothesis](/doubling-hypothesis/) uses this ratio to find the class from measured times.

## Examples

- [Insertion sort](/insertion-sort/) makes $n(n-1)/2$ key comparisons on a reverse-sorted array of $n$ items, which is its worst case. For $n = 8$ this is 28. Its best case, on a sorted array, is $n - 1$ comparisons. A reverse-sorted array has $n(n-1)/2$ [inversions](/inversion/), and a swap of two adjacent items changes the number of inversions by exactly one, so it removes at most one. So insertion sort, bubble sort and every other sort that only swaps adjacent items need at least $n(n-1)/2$ swaps, and $\Omega(n^2)$ time, in the worst case.
- [Selection sort](/selection-sort/) makes $n(n-1)/2$ comparisons on each input, because the search for the minimum in the unsorted part does not depend on the values. Its time is $\Theta(n^2)$ in the best, average and worst case.
- [Bubble sort](/bubble-sort/) in its plain form, without a test for an early stop, compares adjacent items in $(n-1) + (n-2) + \dots + 1 = n(n-1)/2$ places, on each input.
- The brute-force search over all pairs computes $\binom{n}{2}$ distances to find the closest pair of $n$ points. The [closest pair of points](/closest-pair-of-points/) has a faster algorithm that takes $O(n \log n)$ time.
- The school method for the product of two numbers with $n$ digits multiplies each digit of one number by each digit of the other, so it makes $n^2$ digit products. [Karatsuba multiplication](/karatsuba-multiplication/) is faster, with $O(n^{\lg 3})$ digit operations, and $\lg 3 \approx 1.585$.
- [Edit distance](/edit-distance/) and the [longest common subsequence](/longest-common-subsequence/) of two sequences of lengths $m$ and $n$ fill a table with $(m+1)(n+1)$ cells, with constant work in each cell. For $m = n$ the time is $\Theta(n^2)$. For two lengths the right bound is $\Theta(mn)$, see [multivariate asymptotic notation](/multivariate-asymptotic-notation/).
- The standard algorithm for [3SUM](/3sum/) sorts the numbers and then runs two pointers for each choice of the first number, in $O(n^2)$ time. The 3SUM conjecture says that no algorithm with time $O(n^{2-\varepsilon})$ exists for a constant $\varepsilon > 0$ on the word RAM. This is a conjecture, not a theorem.
- Non-example: [merge sort](/merge-sort/) has $\Theta(n \log n)$ time. It is $O(n^2)$ but it is not quadratic, because $n \lg n / n^2 \to 0$.
- Non-example: a nested loop in which the inner loop runs a constant number of times, such as 3, makes $3n$ steps and is linear.

## Where it is used

Quadratic algorithms are the first choice when the input is small or when the code must be simple. Some library sorts switch to [insertion sort](/insertion-sort/) for short ranges, because its constant factor is small. For large inputs the class is often too slow, and the standard step is to replace the loop over all pairs by a sort or a balanced tree, which gives a [linearithmic](/linearithmic-time/) bound, or by a hash table, which gives expected [linear](/linear-time/) time. Tables of dynamic programming over pairs of positions take quadratic time. For edit distance and the longest common subsequence, the space can be cut to linear, see [Hirschberg's algorithm](/hirschberg-algorithm/). Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), neither problem has an algorithm with time $O(n^{2-\varepsilon})$ for a constant $\varepsilon > 0$, so quadratic time is believed to be close to the best possible for them. See also [cubic time](/cubic-time/) for the next class and [common growth rates](/common-growth-rates/) for the whole list.

## References
