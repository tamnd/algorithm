---
tag: ME8VP4
kind: theorem
slug: quicksort-expected-running-time
name: Expected running time of randomized quicksort
area: foundations/probabilistic-analysis
level: core
summary: Randomized quicksort uses O(n log n) comparisons in expectation, proved by summing indicators of compared pairs.
prereqs: [quicksort, indicator-random-variable, linearity-of-expectation, harmonic-series]
see_also: [randomized-quicksort, lomuto-partition, average-case-analysis, hiring-problem, random-bst-expected-depth, comparison-sort-lower-bound, quickselect, variance]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 7, Section 7.3 (A randomized version of quicksort) and Section 7.4 (Analysis of quicksort, expected running time)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 2, Section 2.5 (Application, the expected run-time of quicksort)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (the algorithm RandQS and its analysis)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (analysis of quicksort, mean and variance of the comparison count)
  - paper: doi:10.1093/comjnl/5.1.10
    title: C. A. R. Hoare, Quicksort, The Computer Journal 5(1), 1962
    locator: pp. 10 to 16, the whole paper (the average number of comparisons)
---

[Randomized quicksort](/randomized-quicksort/) on $n$ distinct keys makes exactly $2(n+1)H_n - 4n$ key comparisons in expectation, where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). This is $2n\ln n - (4 - 2\gamma)n + O(\log n) \approx 1.386\,n\lg n$, so the expected running time is $\Theta(n \log n)$ for every input. The short proof uses one [indicator random variable](/indicator-random-variable/) for each pair of keys and [linearity of expectation](/linearity-of-expectation/). The same number is the average comparison count of deterministic [quicksort](/quicksort/) on a uniformly random permutation.

## Statement

Let RANDOMIZED-QUICKSORT be the algorithm of CLRS, Section 7.3: on a subarray of $m \ge 2$ items it picks a pivot uniformly at random from the subarray, partitions with the [Lomuto partition](/lomuto-partition/), which compares each of the other $m - 1$ items with the pivot once, and then recurses on the two sides. A subarray of at most one item causes no comparison.

**Theorem.** Let the input be $n \ge 1$ distinct keys, in any order, and let $C_n$ be the number of key comparisons that RANDOMIZED-QUICKSORT makes. Then
$$ \mathbb{E}[C_n] = 2(n+1)H_n - 4n, \qquad H_n = \sum_{k=1}^{n} \frac1k. $$
The expectation is over the random pivot choices only. It does not depend on the input order.

**Corollary.** $\mathbb{E}[C_n] = 2n\ln n - (4 - 2\gamma)n + 2\ln n + 2\gamma + 1 + O(1/n)$, where $\gamma = 0.5772\ldots$ is Euler's constant. So $\mathbb{E}[C_n] \sim 2n\ln n = (2\ln 2)\,n\lg n \approx 1.3863\,n\lg n$, and the expected running time is $\Theta(n\log n)$ in the RAM model.

## In plain words

Quicksort picks one item, the pivot, and compares every other item of its part with it. Smaller items go left and larger items go right. Two items are compared only if one of them is a pivot while both are still in the same part. After that they are never compared again.

Take two items and look at all the items whose values lie between them, including the two. As long as no pivot comes from this group, the whole group stays together. The first pivot from the group is equally likely to be any of its members. The two items are compared only if this first pivot is one of them. So close items are compared often, and items far apart rarely. Adding these chances over all pairs gives about twice the number of items times the natural logarithm of that number.

## Proof

Write $z_1 < z_2 < \cdots < z_n$ for the keys in sorted order, and $Z_{ij} = \{z_i, z_{i+1}, \ldots, z_j\}$ for $i < j$. Let $X_{ij}$ be the indicator that $z_i$ and $z_j$ are compared at some time.

**Step 1: each pair is compared at most once.** A comparison always has the pivot of the current partition as one side. After the partition, the pivot is in its final place and is not in either subarray of the recursion, so it is never compared again. Hence $z_i$ and $z_j$ meet at most once, and
$$ C_n = \sum_{i=1}^{n-1}\sum_{j=i+1}^{n} X_{ij}. $$

**Step 2: $\Pr[X_{ij} = 1] = 2/(j - i + 1)$.** Consider the run of the algorithm up to the first time that a pivot is chosen from $Z_{ij}$.

- *The group stays together until then.* At the start, all of $Z_{ij}$ is in one subarray. A partition with a pivot $x \notin Z_{ij}$ has $x < z_i$ or $x > z_j$, so all of $Z_{ij}$ goes to the same side. By induction on the number of partitions, all of $Z_{ij}$ is in one subarray until a pivot from $Z_{ij}$ is chosen.
- *Such a pivot is chosen.* The subarray that holds $Z_{ij}$ has at least $j - i + 1 \ge 2$ items, so it is partitioned, and each partition makes the subarray that holds the group strictly smaller. A subarray cannot shrink forever, so at some time the pivot comes from $Z_{ij}$.
- *It is uniform over $Z_{ij}$.* At that partition the subarray $S$ contains $Z_{ij}$, and the pivot is uniform over $S$. Conditioned on the event that the pivot lies in $Z_{ij}$, it is uniform over $Z_{ij}$, and this holds for each history that leads to $S$. So the first pivot chosen from $Z_{ij}$ is uniform over the $j - i + 1$ keys of $Z_{ij}$.
- *When the comparison happens.* If this first pivot is $z_i$ or $z_j$, then the other one is in the same subarray and is compared with it. If the first pivot is some $z_k$ with $i < k < j$, then $z_i$ goes to the left side and $z_j$ to the right side, and they are never in one subarray again. Before this partition neither of them was a pivot, so by Step 1 they are never compared.

So $\Pr[X_{ij} = 1] = 2/(j - i + 1)$.

**Step 3: the sum.** By linearity of expectation, and with $d = j - i + 1$, so that $d$ runs from 2 to $n$ and each value of $d$ occurs for $n - d + 1$ pairs,
$$ \mathbb{E}[C_n] = \sum_{i<j}\frac{2}{j-i+1} = \sum_{d=2}^{n}\frac{2(n+1-d)}{d} = 2(n+1)\sum_{d=2}^{n}\frac1d - 2(n-1) = 2(n+1)(H_n - 1) - 2(n - 1). $$
The right side is $2(n+1)H_n - 2n - 2 - 2n + 2 = 2(n+1)H_n - 4n$. $\square$

**The corollary.** The harmonic numbers satisfy $H_n = \ln n + \gamma + \frac{1}{2n} + O(1/n^2)$, see [harmonic series](/harmonic-series/). Put this in $2(n+1)H_n - 4n$:
$$ 2(n+1)\left(\ln n + \gamma + \tfrac{1}{2n}\right) - 4n + O(1/n) = 2n\ln n + 2\ln n + 2\gamma n + 2\gamma + 1 - 4n + O(1/n). $$
The bound $\ln n < H_n \le \ln n + 1$ alone already gives $2(n+1)\ln n - 4n < \mathbb{E}[C_n] \le 2(n+1)\ln n - 2n + 2$, which is $\Theta(n \log n)$. The running time is $O(n + C_n)$ by CLRS, Section 7.4: the work outside the comparisons is $O(1)$ for each of the at most $n$ calls of PARTITION, plus $O(1)$ for each comparison. It is also $\Omega(n)$. So the expected time is $\Theta(n \log n)$.

**A second proof by the recurrence.** The pivot has rank $k$ with probability $1/n$ for each $k$, and the two sides are then random problems of sizes $k - 1$ and $n - k$, so
$$ \mathbb{E}[C_n] = n - 1 + \frac1n\sum_{k=1}^{n}\bigl(\mathbb{E}[C_{k-1}] + \mathbb{E}[C_{n-k}]\bigr) = n - 1 + \frac2n\sum_{k=0}^{n-1}\mathbb{E}[C_k], \qquad \mathbb{E}[C_0] = 0. $$
Write $c_n = \mathbb{E}[C_n]$. Multiply by $n$, and subtract the same equation for $n - 1$: $n c_n - (n-1)c_{n-1} = 2(n-1) + 2c_{n-1}$, so $n c_n = (n+1)c_{n-1} + 2(n-1)$. Divide by $n(n+1)$:
$$ \frac{c_n}{n+1} = \frac{c_{n-1}}{n} + \frac{2(n-1)}{n(n+1)} = \frac{c_{n-1}}{n} + \frac{4}{n+1} - \frac{2}{n}. $$
Sum from 1 to $n$, with $c_0 = 0$: $\frac{c_n}{n+1} = 4(H_{n+1} - 1) - 2H_n = 2H_n + \frac{4}{n+1} - 4$. So $c_n = 2(n+1)H_n - 4n$, the same value.

## Consequences

**Exact values.** The table gives the exact mean $2(n+1)H_n - 4n$, its leading term $2n\ln n$, the worst case $\binom n2$ and the standard deviation $\sigma_n$ from the variance formula under Tightness. The last column is the mean comparison count of a simulation of CLRS RANDOMIZED-QUICKSORT with the Lomuto partition (seed 1; 100000, 20000, 2000 and 200 runs for the four sizes).

| $n$ | $\mathbb{E}[C_n]$ | $2n\ln n$ | worst case $\binom n2$ | $\sigma_n$ | $\sigma_n / n$ | simulated mean |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 24.44 | 46.05 | 45 | 3.93 | 0.393 | 24.44 |
| 100 | 647.85 | 921.03 | 4950 | 59.48 | 0.595 | 648.58 |
| 1000 | 10985.91 | 13815.51 | 499500 | 639.62 | 0.640 | 10962.42 |
| 10000 | 155771.70 | 184206.81 | 49995000 | 6470.63 | 0.647 | 155104.09 |
| $10^6$ | 24785482.23 | 27631021.12 | $\approx 5.0 \times 10^{11}$ | 648258.27 | 0.648 | |

The simulated means are within 1.7 standard errors of the exact values. The term $-(4 - 2\gamma)n = -2.8456\,n$ is large: at $n = 1000$ the leading term $2n\ln n$ overstates the mean by 26 percent. For small $n$ the exact distribution is short: $C_3$ is 2 with probability $1/3$ and 3 with probability $2/3$, with mean $8/3 = 2\cdot 4\cdot H_3 - 12$.

**Every input has the same expectation.** The proof never used the input order. A sorted input, which drives quicksort with a fixed pivot rule to $\binom n2$ comparisons, has the same expected cost as any other. This is the difference between an [expected running time](/expected-running-time/) of a [randomized algorithm](/randomized-algorithm/) and an [average-case analysis](/average-case-analysis/) of a deterministic one.

**Deterministic quicksort on random input.** If the pivot is always the last item and the input is a uniformly random permutation of distinct keys, then each subarray is again a uniformly random permutation of its keys, and the pivot of each call is uniform over its subarray. The recurrence above holds as written, so the average comparison count is again $2(n+1)H_n - 4n$.

**Other results with the same proof.** The pair argument also gives the expected cost of [Quickselect](/quickselect/), and the expected depth of a node in a [random binary search tree](/random-bst-expected-depth/): $z_j$ is an ancestor of $z_i$ in the tree that the pivots form exactly when $z_j$ is the first pivot chosen from the keys between them.

**Optimality up to a constant.** Each comparison sort needs at least $\lg n! = n\lg n - n\lg e + O(\log n)$ comparisons on average over random inputs, see [the comparison sorting lower bound](/comparison-sort-lower-bound/). Randomized quicksort is within the factor $2\ln 2 \approx 1.386$ of this bound.

## Tightness

The value $2(n+1)H_n - 4n$ is exact, so the result cannot be improved for this algorithm and this way of counting. The interesting questions are how far $C_n$ strays from its mean, and what other pivot rules give.

**Variance.** The exact variance is
$$ \operatorname{Var}[C_n] = 7n^2 - 4(n+1)^2 H_n^{(2)} - 2(n+1)H_n + 13n, \qquad H_n^{(2)} = \sum_{k=1}^{n}\frac{1}{k^2}, $$
as given by Knuth, Volume 3, Section 5.2.2. For example, $\operatorname{Var}[C_3] = 2/9$ and $\operatorname{Var}[C_4] = 29/36$. Since $H_n^{(2)} \to \pi^2/6$, the variance is $\sim (7 - \tfrac{2\pi^2}{3})n^2$, and the standard deviation is $\sim 0.6483\,n$. The standard deviation is $\Theta(n)$ while the mean is $\Theta(n\log n)$, so $C_n / \mathbb{E}[C_n] \to 1$ in probability, by [Chebyshev's inequality](/chebyshev-inequality/).

**Simple tail bounds.** [Markov's inequality](/markov-inequality/) gives $\Pr[C_n \ge 2\,\mathbb{E}[C_n]] \le 1/2$ with no further work. Chebyshev's inequality with the variance gives $\Pr[|C_n - \mathbb{E}[C_n]| \ge t\,n] \le 0.43/t^2$ for large $n$.

**The worst case remains.** If every pivot is the smallest key of its subarray, the run makes $\binom n2$ comparisons. For each input this sequence of choices has probability $\prod_{m=2}^{n} \frac1m = 1/n!$. Randomization moves the bad case from the input to the coin flips; it does not remove it.

**Better pivots.** Choosing the median of three random items lowers the leading term to $\frac{12}{7}n\ln n \approx 1.188\,n\lg n$, a result in Knuth, Volume 3, Section 5.2.2. No pivot rule beats the information-theoretic bound $n\lg n - O(n)$ in the comparison model.

### Pitfalls

- **Equal keys.** The proof assumes distinct keys. With the Lomuto partition and all $n$ keys equal, each pivot puts every other key on one side, and the run makes exactly $\binom n2$ comparisons whatever the random choices are. Use a three-way partition, or break ties by position, to restore $O(n\log n)$.
- **Counting convention.** Other partition schemes compare the pivot with some items twice, or count sentinel comparisons. Then the linear term changes, while the leading term $2n\ln n$ stays. Compare a formula only with the count that it was proved for.
- **$\ln$ and $\lg$.** The leading term is $2n\ln n$, not $2n\lg n$. In base 2 it is $1.386\,n\lg n$.
- **Expected is not average.** For randomized quicksort the bound holds for each input. For quicksort with a fixed pivot rule the same number holds only on average over random inputs, and real inputs such as sorted or nearly sorted files are not random.
- **The leading term alone.** $2n\ln n$ is a poor estimate for practical sizes, because the next term $-2.85\,n$ is large. Use the exact value or the expansion with the linear term.

## History

Hoare published quicksort in 1961 and analysed it in his 1962 paper in The Computer Journal, where he showed that the expected number of comparisons on random input is about $2n\ln n$. Knuth gives the exact mean and variance in Volume 3, Section 5.2.2. The proof by indicators of compared pairs is the one in CLRS, Section 7.4, in Mitzenmacher and Upfal, Section 2.5, and in Motwani and Raghavan, Chapter 1.

## References
