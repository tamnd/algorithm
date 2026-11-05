---
tag: B805F1
kind: theorem
slug: expected-number-of-inversions
name: Expected number of inversions
area: sequences/inversions-and-permutations
level: intro
summary: A uniformly random permutation of n elements has n(n-1)/4 inversions in expectation.
prereqs: [inversion, random-permutation, indicator-random-variable, linearity-of-expectation]
see_also: [mahonian-numbers, lehmer-code, insertion-sort, bubble-sort, sorting-by-adjacent-swaps, variance, kendall-tau-distance, average-case-analysis]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (the generating function of the number of inversions, its mean n(n-1)/4 and its variance)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.2 and its exercises (indicator random variables and the expected number of inversions of a random permutation)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Chapter 7 (permutations, inversions and the analysis of insertion sort)
---

A uniform [random permutation](/random-permutation/) of $n$ items has $n(n-1)/4$ [inversions](/inversion/) on average, exactly half of the $\binom n2$ pairs. The proof uses one [indicator random variable](/indicator-random-variable/) for each pair and [linearity of expectation](/linearity-of-expectation/). The variance is $n(n-1)(2n+5)/72$, so the count is concentrated near its mean. The theorem is the reason why [insertion sort](/insertion-sort/), [bubble sort](/bubble-sort/) and every other sort that only exchanges adjacent items take quadratic time on average.

## Statement

Let $n \ge 0$ and let $\pi$ be chosen uniformly at random from the $n!$ [permutations](/permutation/) of $[n]$. Let $I = \operatorname{inv}(\pi)$. Then

$$\mathbb{E}[I] = \frac{n(n-1)}{4} = \frac12\binom n2, \qquad \operatorname{Var}[I] = \frac{n(n-1)(2n+5)}{72}.$$

The same holds for $I = \operatorname{inv}(X_1, \ldots, X_n)$ when $X_1, \ldots, X_n$ are independent with the same continuous distribution, because then the values are distinct with probability 1 and their relative order is a uniform permutation.

## In plain words

Shuffle a list of different numbers well, and pick any two positions. The bigger number is equally likely to be in the first position or in the second. So each pair is out of order half of the time. There are about half the square of the list length pairs, so on average about a quarter of the square of the length are out of order.

This is a lot. A list of a thousand shuffled numbers has about a quarter of a million out-of-order pairs. A sort that fixes only one such pair at each step, by swapping two neighbors, must take about that many steps. The count also does not spread far from this average, so most shuffled lists are close to it.

## Proof

**Mean.** For $1 \le i < j \le n$ let $X_{ij}$ be the indicator of the event $\pi(i) > \pi(j)$. Then $I = \sum_{i < j} X_{ij}$. Fix $i < j$ and let $\tau = (i\ j)$ be the transposition of the two positions. The map $\pi \mapsto \pi\tau$ exchanges the entries in positions $i$ and $j$. It is a bijection of $S_n$ onto itself (it is its own inverse), and it maps the permutations with $\pi(i) > \pi(j)$ onto those with $\pi(i) < \pi(j)$. Since $\pi(i) \ne \pi(j)$, these two sets split $S_n$ and have the same size $n!/2$. So $\Pr[X_{ij} = 1] = 1/2$ for $n \ge 2$, and by linearity of expectation

$$\mathbb{E}[I] = \sum_{i < j} \Pr[X_{ij} = 1] = \binom n2 \cdot \frac12 = \frac{n(n-1)}{4}.$$

For $n \le 1$ both sides are 0.

**Variance.** The indicators $X_{ij}$ are not independent, so we use another decomposition. For $1 \le i \le n$ let $c_i = |\{j > i : \pi(j) < \pi(i)\}|$, the [Lehmer code](/lehmer-code/) of $\pi$. Each inversion $(i, j)$ is counted in exactly one $c_i$, its left end, so $I = c_1 + \cdots + c_n$, and $0 \le c_i \le n - i$.

*Claim: the map $\pi \mapsto (c_1, \ldots, c_n)$ is a bijection from $S_n$ onto $C_n = \{0, \ldots, n-1\} \times \{0, \ldots, n-2\} \times \cdots \times \{0\}$.* The set $C_n$ has $n \cdot (n-1) \cdots 1 = n!$ elements, the same as $S_n$, so it is enough to show that the map is injective. Given the code, $\pi(1)$ is the item of $[n]$ with exactly $c_1$ smaller items after it, and all other items are after it, so $\pi(1)$ is the $(c_1 + 1)$-th smallest item of $[n]$. In the same way, $\pi(i)$ is the $(c_i + 1)$-th smallest item of $[n] \setminus \{\pi(1), \ldots, \pi(i-1)\}$, because the items after position $i$ are exactly the unused ones. So the code determines $\pi$. $\square$

A uniform $\pi$ therefore gives a uniform point of the product set $C_n$, and the coordinates of a uniform point of a product set are independent and uniform. So $c_i$ is uniform on $\{0, \ldots, k\}$ with $k = n - i$, and the $c_i$ are independent. A uniform variable on $\{0, \ldots, k\}$ has mean $k/2$ and variance

$$\frac{1}{k+1}\sum_{t=0}^{k} t^2 - \frac{k^2}{4} = \frac{k(2k+1)}{6} - \frac{k^2}{4} = \frac{k^2 + 2k}{12}.$$

By independence the variances add:

$$\operatorname{Var}[I] = \sum_{k=0}^{n-1} \frac{k^2 + 2k}{12} = \frac{1}{12}\left(\frac{(n-1)n(2n-1)}{6} + n(n-1)\right) = \frac{n(n-1)}{12} \cdot \frac{2n - 1 + 6}{6} = \frac{n(n-1)(2n+5)}{72}.$$

The same decomposition gives the mean again: $\sum_{k=0}^{n-1} k/2 = n(n-1)/4$.

**Continuous random values.** If $X_1, \ldots, X_n$ are independent with a common continuous distribution, then $\Pr[X_i = X_j] = 0$ for $i \ne j$, and the joint distribution does not change when the $X_i$ are permuted. So each of the $n!$ relative orders has the same probability $1/n!$, and $\operatorname{inv}(X_1, \ldots, X_n)$ has the distribution of $I$. $\blacksquare$

### Examples

For $n = 3$ the six permutations $123, 132, 213, 231, 312, 321$ have $0, 1, 1, 2, 2, 3$ inversions. The mean is $9/6 = 3/2 = 3 \cdot 2/4$, and the variance is $11/12 = 3 \cdot 2 \cdot 11/72$. Exact values for small $n$, and the scale for large $n$:

| $n$ | 2 | 3 | 4 | 5 | 6 | 10 | 100 | 1000 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\mathbb{E}[I]$ | 1/2 | 3/2 | 3 | 5 | 15/2 | 22.5 | 2475 | 249750 |
| $\operatorname{Var}[I]$ | 1/4 | 11/12 | 13/6 | 25/6 | 85/12 | 31.25 | 28187.5 | 27819375 |
| standard deviation | 0.50 | 0.96 | 1.47 | 2.04 | 2.66 | 5.59 | 167.9 | 5274.4 |

## Consequences

- **Average cost of insertion sort.** [Insertion sort](/insertion-sort/) shifts each item past exactly the larger items before it, so it makes $\operatorname{inv}$ shifts. On a uniform random permutation it makes $n(n-1)/4$ shifts on average, and its average time is $\Theta(n^2)$.
- **Average cost of bubble sort.** Each exchange of [bubble sort](/bubble-sort/) removes exactly one inversion, so it makes $n(n-1)/4$ exchanges on average.
- **A lower bound for adjacent exchanges.** An exchange of two adjacent items changes $\operatorname{inv}$ by exactly 1. So every algorithm that sorts only by exchanging adjacent items makes at least $\operatorname{inv}(\pi)$ exchanges on input $\pi$, which is $n(n-1)/4$ on average and $\Omega(n^2)$. To beat this, an algorithm must move items over long distances, as [Shell sort](/shell-sort/), [merge sort](/merge-sort/) and quicksort do. See [sorting by adjacent swaps](/sorting-by-adjacent-swaps/).
- **Concentration.** By the [Chebyshev inequality](/chebyshev-inequality/), $\Pr\big[|I - n(n-1)/4| \ge t\sqrt{\operatorname{Var}[I]}\big] \le 1/t^2$. The standard deviation is about $n^{3/2}/6$, which is small next to the mean $n^2/4$. So a random input is almost never much better than average for insertion sort.
- **Normal limit.** $I$ is a sum of the independent bounded variables $c_i$, and its variance grows like $n^3/36$ while each $c_i$ is at most $n$. By the Lyapunov form of the [central limit theorem](/central-limit-theorem/), $(I - \mathbb{E}[I])/\sqrt{\operatorname{Var}[I]}$ tends in distribution to the standard normal law.
- **Random rankings.** The [Kendall tau distance](/kendall-tau-distance/) between two independent uniform rankings has the same distribution as $I$, which gives the null distribution of Kendall's rank correlation test.
- **The full distribution.** The number of permutations with exactly $k$ inversions is the [Mahonian number](/mahonian-numbers/) $M(n, k)$, with generating function $\prod_{j=1}^{n} (1 + z + \cdots + z^{j-1})$. The mean and variance above also follow from it.

## Tightness

The statement is an exact equality, so there is nothing to tighten. Two remarks show what the hypotheses do.

- **Uniformity is needed.** For a fixed input order the count can be anything from $0$ to $\binom n2$. Only a random input, or a sort that first shuffles, gives the average.
- **Repeated values lower the mean.** If $X_1, \ldots, X_n$ are independent and uniform on $\{1, \ldots, k\}$, then $\Pr[X_i > X_j] = (k - 1)/(2k)$, because the two values are equal with probability $1/k$ and otherwise each order is equally likely. So $\mathbb{E}[I] = \binom n2 \frac{k-1}{2k}$, which is less than $n(n-1)/4$ and tends to it as $k$ grows. For $k = 2$ it is $\binom n2/4$.

## History

Knuth derives the generating function of the number of inversions, its mean and its variance in Section 5.1.1, as the base of the analysis of the sorting methods of his Chapter 5. CLRS uses the mean as an exercise on indicator random variables in Chapter 5, and Sedgewick and Flajolet treat inversions in their chapter on permutations, with the analysis of insertion sort.

## References
