---
tag: 42DC3Z
kind: concept
slug: harmonic-series
name: Harmonic series
aliases:
- harmonic numbers
- H_n
area: foundations/asymptotic-analysis
level: intro
summary: The sum 1 + 1/2 + ... + 1/n, which is Theta(log n) and recurs in randomized and average-case analyses.
prereqs: [asymptotic-notation, logarithms, integral-bounds-for-sums]
see_also: [arithmetic-series, geometric-series, randomized-quicksort, hiring-problem, expected-value, linearity-of-expectation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix A, Summations; Section 5.1 for the hiring problem; Chapter 7 for quicksort
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.7, Harmonic numbers
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 6, Special numbers (harmonic numbers)
  - book: isbn:9781107154889
    title: Mitzenmacher and Upfal, Probability and Computing, second edition
    locator: Chapter 2 (coupon collector)
---

The harmonic number $H_n$ is the sum $1 + \tfrac12 + \tfrac13 + \dots + \tfrac1n$. It grows like the natural logarithm: $\ln(n+1) \le H_n \le \ln n + 1$, so $H_n = \Theta(\log n)$, and $H_n = \ln n + \gamma + O(1/n)$ with $\gamma \approx 0.5772$. The series $\sum_{k \ge 1} 1/k$ diverges, but very slowly. Harmonic numbers appear in the exact average-case cost of [randomized quicksort](/randomized-quicksort/), in the [coupon collector problem](/coupon-collector-problem/) and in the [hiring problem](/hiring-problem/).

## In plain words

Add the fractions 1, 1/2, 1/3, and so on. Each fraction is smaller than the one before, yet the sum has no limit. It passes 2, then 3, then 10, then any number you choose. It is very slow: the sum of the first million terms is only about 14.39.

The sum grows like the logarithm of the number of terms. To see why, group the terms after the first into blocks that double in length: 1/2, then 1/3 and 1/4, then 1/5 to 1/8, and so on. Each block adds at least a half. A million terms make about twenty blocks, so the sum is at least ten.

When a random process has a step with chance 1/k at stage k, the expected number of such steps is a harmonic number. This is why the sum appears in the analysis of randomized algorithms.

## The idea

**Definition.** For each integer $n \ge 0$, $H_n = \sum_{k=1}^{n} 1/k$, with $H_0 = 0$.

**Bounds.** For each integer $n \ge 1$,
$$ \ln(n+1) \le H_n \le 1 + \ln n. $$

*Proof.* The function $1/x$ is decreasing on $(0, \infty)$. For each $k \ge 1$ and each $x \in [k, k+1]$, $1/x \le 1/k$. So $\int_k^{k+1} dx/x \le 1/k$. Summing over $k = 1, \dots, n$ gives $\ln(n+1) = \int_1^{n+1} dx/x \le H_n$. For each $k \ge 2$ and each $x \in [k-1, k]$, $1/x \ge 1/k$. So $1/k \le \int_{k-1}^{k} dx/x$. Summing over $k = 2, \dots, n$ gives $H_n - 1 \le \int_1^n dx/x = \ln n$. $\square$

So $H_n = \Theta(\log n)$. This is a case of the [integral bounds for sums](/integral-bounds-for-sums/) for the decreasing function $1/x$. For $n = 10$: $H_{10} = 2.92897\dots$, and the bounds are $\ln 11 = 2.3979\dots$ and $1 + \ln 10 = 3.3026\dots$.

**Divergence.** Since $\ln(n+1) \to \infty$, the lower bound shows $H_n \to \infty$. So $\sum_{k \ge 1} 1/k$ diverges. It needs about $e^{m - \gamma}$ terms to pass $m$: the sum passes 10 only at $n = 12367$.

**Asymptotic form.** Let $d_n = H_n - \ln n$. Then there is a constant $\gamma$ with $0 \le d_n - \gamma \le 1/n$ for each $n \ge 1$. So
$$ H_n = \ln n + \gamma + O(1/n). $$

*Proof.* We have $d_n - d_{n+1} = \ln(1 + 1/n) - 1/(n+1)$. From $\ln(1 + 1/n) = \int_n^{n+1} dx/x$ we get $1/(n+1) \le \ln(1+1/n) \le 1/n$. So $0 \le d_n - d_{n+1} \le 1/n - 1/(n+1)$. The sequence $d_n$ is non-increasing. It is bounded below by 0, because $d_n \ge \ln(n+1) - \ln n > 0$ by the lower bound above. So it converges to a limit $\gamma \ge 0$. Then $d_n - \gamma = \sum_{m \ge n} (d_m - d_{m+1}) \le \sum_{m \ge n} (1/m - 1/(m+1)) = 1/n$, since the last sum telescopes. $\square$

The constant $\gamma = 0.5772156649\dots$ is the Euler-Mascheroni constant, often called Euler's constant. A finer expansion is $H_n = \ln n + \gamma + \frac{1}{2n} - \frac{1}{12n^2} + O(n^{-4})$ (Knuth, Section 1.2.7). So the error of $\ln n + \gamma$ is about $1/(2n)$. For $n = 100$, $H_{100} = 5.18738\dots$ and $\ln 100 + \gamma = 5.18239\dots$.

**Sum of harmonic numbers.** $\sum_{k=1}^{n} H_k = (n+1)H_n - n$. *Proof.* The term $1/j$ appears in $H_k$ for each $k \ge j$, so it appears $n - j + 1$ times. So the sum is $\sum_{j=1}^{n} (n+1-j)/j = (n+1)H_n - n$. $\square$

## Examples

- Exact values: $H_1 = 1$, $H_2 = 3/2$, $H_6 = 49/20 = 2.45$, $H_{10} = 7381/2520 \approx 2.9290$.
- $H_{100} \approx 5.1874$ and $\ln 100 + 1 \approx 5.6052$, so the upper bound is not tight, and $\ln 100 + \gamma \approx 5.1824$ is much closer.
- The harmonic sum over a subset: $\sum_{k=1}^{n} 1/(2k-1) = H_{2n} - \tfrac12 H_n = \Theta(\log n)$ as well.
- Non-example: $\sum_{k \ge 1} 1/k^2$ converges (to $\pi^2/6$). The exponent 1 is the border: $\sum 1/k^s$ converges for $s > 1$ and diverges for $s \le 1$. Another non-example is $\sum_{k=1}^n k$, an [arithmetic series](/arithmetic-series/), which is $\Theta(n^2)$.

## Where it is used

**Quicksort.** Let $C_n$ be the expected number of comparisons of [randomized quicksort](/randomized-quicksort/) on $n$ distinct keys, when the pivot is uniform and the partition of $m$ keys makes $m - 1$ comparisons. Then $C_0 = C_1 = 0$ and $C_n = n - 1 + \frac{2}{n}\sum_{k=0}^{n-1} C_k$, and
$$ C_n = 2(n+1)H_n - 4n \approx 2n \ln n. $$
*Proof.* Multiply by $n$ and subtract the same equation for $n - 1$ (for $n \ge 2$): $nC_n - (n-1)C_{n-1} = n(n-1) - (n-1)(n-2) + 2C_{n-1}$. So $nC_n = (n+1)C_{n-1} + 2(n-1)$. Divide by $n(n+1)$: $\frac{C_n}{n+1} = \frac{C_{n-1}}{n} + \frac{2(n-1)}{n(n+1)}$, and $\frac{2(n-1)}{n(n+1)} = \frac{4}{n+1} - \frac{2}{n}$. Sum from $2$ to $n$, with $C_1 = 0$: $\frac{C_n}{n+1} = 4\left(H_{n+1} - \tfrac32\right) - 2(H_n - 1) = 2H_n + \frac{4}{n+1} - 4$. Multiply by $n+1$: $C_n = 2(n+1)H_n - 4n$. $\square$

For $n = 10$ the value is $2 \cdot 11 \cdot H_{10} - 40 = 24.437\dots$ expected comparisons, and the exact recurrence gives the same number. With $H_n = \ln n + O(1)$ the cost is $2n \ln n + O(n) \approx 1.386\, n \lg n$. The base matters here: $H_n \approx \ln n = (\ln 2) \lg n \approx 0.693 \lg n$. Inside $\Theta$ the base has no effect, but it changes the leading constant, and this constant is the one that you compare with the $n \lg n$ of merge sort.

**Coupon collector.** See the [coupon collector problem](/coupon-collector-problem/). A set has $n$ types, and each draw picks a type uniformly and independently. While $i - 1$ types are collected, a draw gives a new type with probability $(n - i + 1)/n$, so the wait for the $i$-th new type has expectation $n/(n - i + 1)$. By [linearity of expectation](/linearity-of-expectation/) the expected number of draws to collect all types is $\sum_{i=1}^{n} \frac{n}{n-i+1} = nH_n$. For a fair die, $n = 6$, this is $6 \cdot 2.45 = 14.7$ throws.

**The hiring problem.** Candidates come in a uniformly random order and you hire a candidate who is better than all earlier ones. Candidate $i$ is the best of the first $i$ with probability $1/i$, when the ranks are distinct. By linearity of expectation the expected number of hires is $H_n = \ln n + O(1)$. The [hiring problem](/hiring-problem/) page gives the full analysis.

**Other uses.** The sum $\sum_{k=1}^{n} \lfloor n/k \rfloor$ is at most $nH_n$, which bounds loops that run over the multiples of each $k$. In a [random binary search tree](/random-binary-search-tree/) or a [treap](/treap/) with $n$ keys, the expected number of nodes on the path from the root to the key of rank $i$ is $H_i + H_{n-i+1} - 1$, so the expected search cost is $O(\log n)$. The analysis of [quickselect](/quickselect/) with a random pivot sums terms of the form $1/(j - i + 1)$, and it gives a linear bound on the expected number of comparisons.

## References
