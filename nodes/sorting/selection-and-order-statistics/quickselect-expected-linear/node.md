---
tag: STSDV8
kind: theorem
slug: quickselect-expected-linear
name: Expected linear time of randomized selection
aliases:
- expected linear time of quickselect
area: sorting/selection-and-order-statistics
level: core
summary: Randomized quickselect finds any order statistic in expected O(n) time.
prereqs: [quickselect, indicator-random-variable, linearity-of-expectation, harmonic-series]
see_also: [randomized-quickselect, selection-problem, median-of-medians, floyd-rivest-select, deterministic-linear-selection, randomized-quicksort, expected-running-time, las-vegas-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.2, Selection in expected linear time, and the end-of-chapter problem "Alternative analysis of randomized selection" (the indicator-variable proof of a bound below 4n)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging, the exercises on Hoare's FIND (the exact average number of comparisons)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 13.5, Randomized divide and conquer, median-finding and quicksort (the analysis by phases)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 2, Section 2.4, Medians (the good-split argument, T(n) ≤ T(3n/4) + O(n))
  - paper: doi:10.1145/366622.366647
    title: C. A. R. Hoare, Algorithm 65, Find, Communications of the ACM 4(7) (1961)
    locator: pages 321 to 322
---

[Quickselect](/quickselect/) with a pivot chosen uniformly at random from the current range finds the item of each rank $k$ among $n$ distinct items with fewer than $4n$ comparisons in expectation, on every input. The exact expectation is $2\bigl((n+1)H_n - (n+3-k)H_{n+1-k} - (k+2)H_k + n + 3\bigr)$, which is about $2n$ for the extreme ranks and $2(1 + \ln 2)n \approx 3.386n$ for the median. So randomized selection runs in expected $\Theta(n)$ time, although its worst case is $\Theta(n^2)$.

## Statement

Let $A$ be an array of $n \ge 1$ distinct items, and let $1 \le k \le n$. Run QUICKSELECT$(A, k)$, as on the [quickselect](/quickselect/) page: in each pass on a range of $m \ge 2$ items, the pivot is uniform at random among the $m$ items of the range, independent of earlier choices, the partition compares each other item of the range with the pivot once, and the loop stops when the pivot has rank $k$ or the range has one item. Let $C_{n,k}$ be the number of comparisons between items. Then

$$ \mathbb{E}[C_{n,k}] = 2\Bigl((n+1)H_n - (n+3-k)H_{n+1-k} - (k+2)H_k + n + 3\Bigr) < 4n, $$

where $H_m = \sum_{i=1}^{m} 1/i$ is the $m$-th [harmonic number](/harmonic-series/). The running time is $O(C_{n,k} + 1)$, so the [expected running time](/expected-running-time/) is $O(n)$, for each input and each $k$.

**Asymptotic form.** For $k = \alpha n$ with a fixed $0 < \alpha < 1$,

$$ \mathbb{E}[C_{n,k}] = 2n\bigl(1 + h(\alpha)\bigr) + O(\log n), \qquad h(\alpha) = -\alpha \ln \alpha - (1 - \alpha) \ln (1 - \alpha). $$

The largest value is at $\alpha = 1/2$: $2(1 + \ln 2)n \approx 3.386n$.

## In plain words

Each pass of quickselect compares every item of the range with the pivot and then throws a part of the range away. A random pivot is often near the middle, so the range shrinks fast, and the total work is a sum that looks like $n + 3n/4 + 9n/16 + \cdots$, a few times $n$.

The proof makes this exact by asking, for each pair of items, how likely it is that the two are ever compared. Two items are compared only if one of them is the first pivot taken from the stretch of sorted order that holds both of them and the target. Long stretches make this unlikely. Adding up these chances over all pairs gives the exact expected number of comparisons.

## Proof

Let $z_1 < z_2 < \cdots < z_n$ be the items in sorted order, so the answer is $z_k$. For $i < j$, let $X_{ij}$ be the [indicator](/indicator-random-variable/) of the event that $z_i$ and $z_j$ are compared at some time in the run. Write $Z_{ij} = \{ z_l : \min(i, k) \le l \le \max(j, k) \}$, the stretch of sorted order from the smallest to the largest of $z_i$, $z_j$, $z_k$. It has $d_{ij} = \max(j, k) - \min(i, k) + 1$ items.

### Lemma 1 (each pair at most once)

Each comparison is between the pivot of a pass and another item of its range. After the pass, the pivot is not in the next range. So two items are compared at most once, and $C_{n,k} = \sum_{i<j} X_{ij}$.

### Lemma 2 (the range is a stretch of sorted order)

At each pass the range holds the items $z_l$ for $l$ in an interval $[a, b]$ with $a \le k \le b$. At the start this is $[1, n]$. If the pivot is $z_p$ with $p \ne k$, the next range is $[a, p - 1]$ when $k < p$ and $[p + 1, b]$ when $k > p$; both are intervals that hold $k$. This is the invariant (Q) of the proof of quickselect, written with ranks.

### Lemma 3 (the probability of a comparison)

For $i < j$,

$$ \Pr[X_{ij} = 1] = \frac{2}{d_{ij}}. $$

*Proof.* As long as no pivot has been taken from $Z_{ij}$, each pivot $z_p$ satisfies $p < \min(i, k)$ or $p > \max(j, k)$, so by Lemma 2 the next range still holds all of $Z_{ij}$: the part thrown away is all on one side of $Z_{ij}$, since $Z_{ij}$ holds $z_k$. The run cannot stop before a pivot comes from $Z_{ij}$, because it stops only at the pivot $z_k \in Z_{ij}$ or at a range of one item, and the range holds $Z_{ij}$, which has at least two items. So some pass takes the first pivot from $Z_{ij}$, and in that pass the range holds all of $Z_{ij}$. Given the history up to this pass and given that the pivot lies in $Z_{ij}$, the pivot is uniform on $Z_{ij}$, since it is uniform on the range.

- If the pivot is $z_i$ or $z_j$, the partition compares it with the other one, which is in the range. Probability $2/d_{ij}$.
- If the pivot is $z_p$ with $i < p < j$, then $z_i$ and $z_j$ go to different sides, and at most one of them stays in the range, so they are never compared.
- If the pivot is $z_p$ with $p$ in $Z_{ij}$ but outside $[i, j]$, then $p$ is between $k$ and the nearer of $i$ and $j$, or $p = k$. If $p = k$ the run stops. Else $z_k$ is on one side of $z_p$ and both $z_i$ and $z_j$ are on the other side, so both are thrown away. Neither was the pivot of an earlier pass, so they are never compared.

So $X_{ij} = 1$ exactly in the first case. $\square$

### Lemma 4 (the three sums)

By Lemma 1, [linearity of expectation](/linearity-of-expectation/) and Lemma 3, $\mathbb{E}[C_{n,k}] = \sum_{i<j} 2/d_{ij}$. Split the pairs $i < j$ into three disjoint classes, which cover all pairs:

1. $i < j \le k$. Then $d_{ij} = k - i + 1$. For fixed $i$ there are $k - i$ values of $j$. With $m = k - i$,
$$ S_1 = \sum_{i=1}^{k-1} \frac{2(k-i)}{k-i+1} = 2\sum_{m=1}^{k-1} \Bigl(1 - \frac{1}{m+1}\Bigr) = 2(k - H_k). $$
2. $k \le i < j$. Then $d_{ij} = j - k + 1$. For fixed $j$ there are $j - k$ values of $i$. With $m = j - k$,
$$ S_2 = \sum_{m=1}^{n-k} \frac{2m}{m+1} = 2(n - k + 1 - H_{n-k+1}). $$
3. $i < k < j$. Then $d_{ij} = j - i + 1$, and
$$ S_3 = 2\sum_{i=1}^{k-1} \sum_{j=k+1}^{n} \frac{1}{j - i + 1} = 2\sum_{i=1}^{k-1} \bigl(H_{n-i+1} - H_{k-i+1}\bigr). $$

### The exact value

Use $\sum_{m=1}^{N} H_m = (N+1)H_N - N$, which follows by exchanging the sums: $\sum_{m=1}^{N} \sum_{l=1}^{m} 1/l = \sum_{l=1}^{N} (N - l + 1)/l = (N+1)H_N - N$. Then $\sum_{m=a}^{b} H_m = (b+1)H_b - b - aH_{a-1} + (a - 1)$ for $1 \le a \le b + 1$. With $m = n - i + 1$ and $m = k - i + 1$,

$$ \sum_{i=1}^{k-1} H_{n-i+1} = \sum_{m=n-k+2}^{n} H_m = (n+1)H_n - (n-k+2)H_{n-k+1} - k + 1, $$

$$ \sum_{i=1}^{k-1} H_{k-i+1} = \sum_{m=2}^{k} H_m = (k+1)H_k - k - 1. $$

So $S_3 = 2\bigl((n+1)H_n - (n-k+2)H_{n-k+1} - (k+1)H_k + 2\bigr)$, and

$$ S_1 + S_2 + S_3 = 2\Bigl((n+1)H_n - (n+3-k)H_{n+1-k} - (k+2)H_k + n + 3\Bigr). $$

For $n = 9$ and $k = 5$ this is $10487/630 \approx 16.65$.

### The bound $4n$

Each term $2(k-i)/(k-i+1)$ of $S_1$ is less than $2$, so $S_1 < 2(k - 1)$ when $k \ge 2$, and $S_1 = 0$ when $k = 1$. In the same way $S_2 \le 2(n - k)$. In $S_3$, group the pairs by $d = j - i + 1$, which runs from $3$ to $n$. A pair with $i < k < j$ and $j - i + 1 = d$ is fixed by $i$, and $i$ runs over $k - d + 2 \le i \le k - 1$ at most, so there are at most $d - 2$ such pairs. So
$$ S_3 \le \sum_{d=3}^{n} \frac{2(d-2)}{d} < 2(n - 2). $$
In total $\mathbb{E}[C_{n,k}] < 2(k - 1) + 2(n - k) + 2(n - 2) < 4n$. This is the bound of the CLRS problem "Alternative analysis of randomized selection".

### Time

A pass on a range of $m \ge 2$ items makes $m - 1 \ge 1$ comparisons and $O(m)$ other work. So the number of passes is at most $C_{n,k}$, and the time is $O(C_{n,k} + 1)$. Its expectation is $O(n)$.

### The asymptotic form

With $H_m = \ln m + \gamma + O(1/m)$ and $k = \alpha n$, the terms in $\ln n$ cancel: $(n+1)\ln n - (n - k)\ln n - k \ln n = O(\ln n)$. What is left is
$$ 2\bigl(-(1-\alpha)n \ln(1-\alpha) - \alpha n \ln \alpha + n\bigr) + O(\log n) = 2n(1 + h(\alpha)) + O(\log n), $$
and $h$ has its maximum $\ln 2$ at $\alpha = 1/2$. $\blacksquare$

## Consequences

- **Selection in expected linear time.** The [selection problem](/selection-problem/) is solved in expected $O(n)$ time by a simple in-place method, which is why [quickselect](/quickselect/) and its relatives are the library routines.
- **The extreme ranks.** For $k = 1$ the formula gives $2n - 2H_n$, about $2n$ comparisons: $1985.0$ for $n = 1000$. A plain scan uses $n - 1$, so quickselect is a poor way to find the minimum.
- **The median.** For $n = 1000$ and $k = 500$ the formula gives $3336.3$ comparisons, $3.34n$; the limit $3.386n$ is reached slowly because of the $O(\log n)$ term.
- **Top-k at no extra cost.** At the end, the $k$ smallest items are in $A[0 \ldots k-1]$, so [top-k selection](/top-k-selection/) in any order also takes expected $O(n)$ time.
- **Las Vegas.** The answer is always correct; only the time is random. So the algorithm is a [Las Vegas algorithm](/las-vegas-algorithm/), and by [Markov's inequality](/markov-inequality/) it makes more than $4cn$ comparisons with probability less than $1/c$.

## Tightness

- **The constant.** The formula is exact, so for this algorithm the constant $2(1 + \ln 2)$ for the median cannot be improved. Better pivots improve it: the median of three random items gives about $2.75n$ for the median, and the samples of [Floyd-Rivest selection](/floyd-rivest-select/) give $n + \min(k, n - k) + o(n)$, which matches the average-case lower bound of Cunto and Munro.
- **The worst case.** The bound is on the expectation only. With probability at least $1/n!$, each pivot is the largest item of its range, and for $k = 1$ the run makes $n(n-1)/2$ comparisons. A guaranteed $O(n)$ needs a deterministic pivot rule such as [median of medians](/median-of-medians/); see the [deterministic linear selection](/deterministic-linear-selection/) theorem.
- **Distinct items.** The theorem assumes distinct items. With the test $A[j] \le x$ of the Lomuto partition, an array of $n$ equal items makes each pivot land at the right end of the range, and quickselect makes $\Theta(n^2)$ comparisons with any random choices. A three-way partition restores the bound.
- **A fixed pivot rule.** If the pivot is the last item of the range instead of a random one, the same expectation holds over a uniformly random order of the input, but not for each input: a sorted input takes $\Theta(n^2)$ time.

## History

C. A. R. Hoare published FIND in 1961. Knuth worked out the exact average number of comparisons of the random-pivot version, the formula of the statement. The textbook proofs of an $O(n)$ bound differ: CLRS bounds the recurrence $\mathbb{E}[T(n)] \le \frac{2}{n} \sum_{q = \lfloor n/2 \rfloor}^{n-1} \mathbb{E}[T(q)] + O(n)$ by substitution in its third edition, and counts helpful partitions in its fourth edition; Kleinberg and Tardos and Dasgupta, Papadimitriou and Vazirani count the passes until the range shrinks by a factor $3/4$. The indicator proof above follows the CLRS problem on an alternative analysis.

## References
