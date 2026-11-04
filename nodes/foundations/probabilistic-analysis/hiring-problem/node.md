---
tag: VGQMN0
kind: problem
slug: hiring-problem
name: Hiring problem
area: foundations/probabilistic-analysis
level: intro
summary: Interview candidates in random order and hire the best so far; analyzes the expected number of hires.
prereqs: [indicator-random-variable, linearity-of-expectation, random-permutation, harmonic-series]
see_also: [hire-assistant, secretary-problem, find-maximum, coupon-collector-problem, streaks, average-case-analysis, randomized-algorithm, online-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Sections 5.1 to 5.3 (the hiring problem, its expected cost and the randomized version), and Section 5.4 (the online hiring problem)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, analysis of Algorithm M (the number of changes of the maximum, its mean and variance, and the Stirling numbers of the first kind)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 2 (indicator random variables and linearity of expectation)
---

The hiring problem asks how many times a manager hires when $n$ candidates arrive one at a time and the manager hires each candidate who is better than all who came before. In the worst case the answer is $n$, but when the candidates arrive in a uniformly random order the expected number of hires is the [harmonic number](/harmonic-series/) $H_n = \ln n + O(1)$. It is the opening example of probabilistic analysis in CLRS Chapter 5. This page is about the question and its answers; the procedure that the manager runs is the [Hire-assistant](/hire-assistant/) algorithm.

## In plain words

You need an office assistant, and an agency sends you one candidate each day. After each interview you can keep your current assistant or fire them and hire the new person. You always want the best person you have seen. Each interview costs a little, and each hire costs a lot.

The question is how many people you hire. If the candidates come from worst to best, you hire every one of them. If the best comes first, you hire only one. If the order is random, you hire only a few: a person is a new best only when they beat everyone before them, and that gets less likely as the days pass. For a thousand candidates you hire about seven or eight people.

## Definition

**Input.** $n$ candidates with distinct qualities, which arrive in an order $\pi$. A candidate can be compared with another, but the qualities are not known in advance. An interview costs $c_i$ and a hire costs $c_h$, with $c_h \gg c_i$ in the usual story.

**The rule.** Hire candidate $i$ if and only if candidate $i$ is better than candidates $1, \ldots, i-1$. Candidate 1 is always hired. This rule is the [Hire-assistant](/hire-assistant/) algorithm.

**The quantity.** Let $m = m(\pi)$ be the number of hires. The total cost is $c_i n + c_h m$. The interview cost is fixed, so the question is about $m$. In the language of permutations, $m$ is the number of *left-to-right maxima* or *records* of $\pi$.

**The question.** Find $m$ in the worst case, in the best case, and in expectation and distribution when $\pi$ is a uniform [random permutation](/random-permutation/).

## Variants

- **Probabilistic analysis.** Assume the input order is uniformly random and compute $\mathbb{E}[m]$. The answer depends on that assumption about the input.
- **Randomized hiring.** The manager gets the whole list in advance and first shuffles it, for example with the [Fisher-Yates shuffle](/fisher-yates-shuffle/). Then $\mathbb{E}[m] = H_n$ for *each* input, and no input is bad. This turns an [average-case analysis](/average-case-analysis/) into the expected cost of a [randomized algorithm](/randomized-algorithm/).
- **Online hiring.** The manager may hire only once and must decide right after each interview. The goal is to maximize the probability of hiring the best candidate. This is the [secretary problem](/secretary-problem/). CLRS Section 5.4 analyzes the rule "reject the first $k$ candidates, then hire the first one who beats all of them".
- **Ties.** With equal qualities, the rule must say whether an equal candidate is hired. With "strictly better", equal candidates lower the number of hires.

## Examples

**One input.** For the arrival order $[5, 2, 8, 6, 9, 1, 10, 3, 7, 4]$ of qualities, the hires are at positions 1, 3, 5 and 7, with qualities 5, 8, 9 and 10. So $m = 4$, and $H_{10} = 7381/2520 \approx 2.929$.

**All orders for $n = 4$.** Of the $24$ orders, $6$ give one hire, $11$ give two, $6$ give three and $1$ gives four. The mean is $(6 + 22 + 18 + 4)/24 = 50/24 = 25/12 = H_4$.

**The distribution for $n = 10$.** $\Pr[m = k] = {10 \brack k}/10!$, where ${n \brack k}$ is an unsigned [Stirling number](/stirling-numbers/) of the first kind:

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | $\ge 8$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\Pr[m = k]$ | 0.1000 | 0.2829 | 0.3232 | 0.1994 | 0.0742 | 0.0174 | 0.0026 | 0.0002 |

**Means and spread.** Exact mean $H_n$, exact variance $H_n - H_n^{(2)}$ with $H_n^{(2)} = \sum_{i \le n} 1/i^2$, and the mean of a simulation with uniform random orders (seed 9; 100000, 20000 and 2000 runs):

| $n$ | $\ln n$ | $\mathbb{E}[m] = H_n$ | $\operatorname{Var}[m]$ | standard deviation | simulated mean |
| --- | --- | --- | --- | --- | --- |
| 10 | 2.303 | 2.929 | 1.379 | 1.174 | 2.929 |
| 100 | 4.605 | 5.187 | 3.552 | 1.885 | 5.177 |
| 1000 | 6.908 | 7.486 | 5.842 | 2.417 | 7.422 |
| $10^6$ | 13.816 | 14.393 | 12.748 | 3.570 | |

So with a million candidates in random order, the manager hires about 14 times, not a million times.

## Known algorithms

- **[Hire-assistant](/hire-assistant/).** The rule itself: one pass that keeps the best candidate so far. It does $n$ interviews and $m$ hires, so it costs $c_i n + c_h m$.
- **Randomized hire-assistant.** Shuffle the list first, then run Hire-assistant. The expected number of hires is $H_n$ for each input order.
- **Threshold rule for online hiring.** Reject the first $k$ candidates and then hire the first who beats all of them. It hires the best candidate with probability $\frac{k}{n}\sum_{i=k+1}^{n}\frac{1}{i-1} = \frac{k}{n}(H_{n-1} - H_{k-1})$. The best $k$ is $3$ for $n = 10$ (probability $0.3987$) and $37$ for $n = 100$ (probability $0.3710$). With $k \approx n/e$ the probability tends to $1/e \approx 0.368$.

## Bounds

**Worst and best case.** If the candidates arrive in increasing order of quality, each one is a new best, so $m = n$. If the best arrives first, $m = 1$. Both bounds are reached.

**Expected number of hires.** Let $\pi$ be uniform and let $X_i$ be the [indicator](/indicator-random-variable/) that candidate $i$ is hired, so $m = \sum_{i=1}^n X_i$. Candidate $i$ is hired if and only if candidate $i$ is the best of candidates $1, \ldots, i$. In a uniform random order, each of these $i$ candidates is equally likely to be the best among them, so $\Pr[X_i = 1] = 1/i$. By [linearity of expectation](/linearity-of-expectation/),
$$ \mathbb{E}[m] = \sum_{i=1}^n \frac{1}{i} = H_n. $$
Since $1/x$ is decreasing, $\ln(n+1) = \int_1^{n+1} dx/x \le H_n \le 1 + \int_1^n dx/x = 1 + \ln n$. So $\mathbb{E}[m] = \ln n + O(1)$, and the expected hiring cost is $O(c_h \ln n)$, against $O(c_h n)$ in the worst case.

**The indicators are independent.** The relative order of the first $i$ candidates is a uniform permutation of $i$ items. It is determined by two independent parts: the rank of candidate $i$ among the first $i$, which is uniform on $\{1, \ldots, i\}$, and the relative order of the first $i - 1$, which is uniform on the $(i-1)!$ orders. The count $i \cdot (i-1)! = i!$ shows that each pair of values occurs exactly once. $X_i$ depends only on the first part, and $X_1, \ldots, X_{i-1}$ depend only on the second. By induction on $i$, $X_1, \ldots, X_n$ are independent.

**Variance and concentration.** From independence, $\operatorname{Var}[m] = \sum_{i=1}^n \frac1i\left(1 - \frac1i\right) = H_n - H_n^{(2)}$, which is less than $H_n$. By the [Chebyshev inequality](/chebyshev-inequality/), $\Pr[|m - H_n| \ge t\sqrt{H_n}] \le 1/t^2$. Since $m$ is a sum of independent indicators, the [Chernoff bound](/chernoff-bound/) also applies: for example, $\Pr[m \ge 2e H_n] \le 2^{-2eH_n} \le n^{-2e\ln 2} < n^{-3}$, from the bound $\Pr[X \ge R] \le 2^{-R}$ for $R \ge 2e\,\mathbb{E}[X]$ and $H_n \ge \ln n$.

**The exact distribution.** The generating function of $m$ is the product of the independent factors $\frac{i-1+z}{i}$:
$$ \mathbb{E}[z^m] = \prod_{i=1}^{n}\frac{z + i - 1}{i} = \frac{1}{n!}\sum_{k}{n \brack k}z^k, $$
since $z(z+1)\cdots(z+n-1) = \sum_k {n \brack k}z^k$. So $\Pr[m = k] = {n \brack k}/n!$. Knuth derives the same distribution for the number of changes of the maximum in Algorithm M of Section 1.2.10, which is $m - 1$.

## Reductions

- **[Finding the maximum](/find-maximum/).** A scan that keeps the largest item so far updates it $m - 1$ times. So the hiring problem is the cost analysis of the maximum scan when an update is expensive.
- **Cycles of a permutation.** The number of records of a uniform permutation has the same distribution as the number of [cycles](/permutation-cycles/) of a uniform permutation. Both have the generating function above.
- **Random binary search trees.** If the items are inserted into a [binary search tree](/binary-search-tree/) in the order $\pi$, the records are the nodes on the path from the root to the maximum. So the expected length of this path in a [random binary search tree](/random-binary-search-tree/) is $H_n$.

## Applications

- **Teaching probabilistic analysis.** CLRS uses the problem to introduce indicator random variables, the gap between worst-case and expected cost, and the idea that an algorithm can enforce a random input by shuffling it.
- **Cost of updates.** Any process that does an expensive action at each new maximum, such as rewriting a best-so-far result to disk or broadcasting a new best bound in a search, does $H_n$ actions in expectation on a random order.
- **Online decisions.** The online version is the secretary problem, which is the base of a large family of online selection problems.

## References
