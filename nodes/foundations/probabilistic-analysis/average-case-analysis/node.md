---
tag: NMTCKZ
kind: concept
slug: average-case-analysis
name: Average-case analysis
aliases:
- expected-case analysis
area: foundations/probabilistic-analysis
level: intro
summary: Analyzes expected running time over a distribution of inputs, or over the algorithm's random choices.
prereqs: [worst-case-analysis, expected-value, random-variable, random-permutation]
see_also: [best-case-analysis, worst-case-analysis, smoothed-analysis, expected-running-time, randomized-algorithm, hiring-problem, quicksort-expected-running-time, amortized-vs-expected-cost]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (worst-case and average-case analysis), Chapter 5 (probabilistic analysis and randomized algorithms) and Section 7.4 (analysis of quicksort)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10 (analysis of an algorithm, with the mean and variance of the number of changes of the maximum)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversions of a random permutation) and Section 5.2.2 (quicksort)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 18, average-case complexity and Levin's theory
  - paper: "Leonid A. Levin, Average case complete problems, SIAM Journal on Computing 15(1), 1986"
    locator: pp. 285 to 286, the definition of polynomial on average and the first average-case complete problem
---

Average-case analysis measures the cost of an algorithm by its [expected value](/expected-value/) when the input is drawn from a stated probability distribution, usually the uniform one on inputs of size $n$. It answers the question "how much does the algorithm cost on a typical input", where [worst-case analysis](/worst-case-analysis/) answers "how much on the worst input". The answer is only as good as the distribution: a result for random permutations says nothing about sorted inputs. A related but different notion is the [expected running time](/expected-running-time/) of a [randomized algorithm](/randomized-algorithm/), where the randomness is in the algorithm and the input is the worst one.

## In plain words

Worst-case analysis asks how long a program can take on the hardest input. Often the hardest input is rare. Average-case analysis asks how long the program takes on a typical input instead. To say what typical means, you choose a way to pick the inputs at random, for example all orders of the items equally likely. Then you work out the mean cost over these inputs.

The answer can be much better than the worst case. A simple sort can take a long time on a list in reverse order, but on a shuffled list it takes about half as long, and some methods are much faster on average than in the worst case. The danger is that real inputs may not look like the random ones you chose.

## The idea

**Definition.** Let $T(x)$ be the cost of an algorithm on input $x$, and let $D_n$ be a probability distribution on the inputs of size $n$. The *average-case cost* is
$$ \bar T(n) = \mathbb{E}_{x \sim D_n}[T(x)] = \sum_{|x| = n} \Pr_{D_n}[x]\,T(x). $$
The worst-case cost is $\max_{|x| = n} T(x)$ and the [best-case](/best-case-analysis/) cost is $\min_{|x| = n} T(x)$, so $\min \le \bar T(n) \le \max$ for each distribution.

**Two kinds of randomness.** CLRS separates two ideas.

- *Probabilistic analysis* of a deterministic algorithm: the input is random with a known distribution. The result is the average-case cost.
- *Expected running time* of a randomized algorithm: the algorithm makes random choices, and the cost is $\max_x \mathbb{E}_{r}[T(x, r)]$, the worst input with the expectation over the random bits $r$. No assumption on the input is needed.

The two often give the same formula, because a randomized algorithm can make its input random. [Hire-assistant](/hire-assistant/) on a uniform random order and RANDOMIZED-HIRE-ASSISTANT, which shuffles first, both make $H_n$ hires in expectation; the first needs an assumption on the input and the second does not. The same holds for deterministic [quicksort](/quicksort/) on random permutations and [randomized quicksort](/randomized-quicksort/) on any input.

**The method.** Write the cost as a sum of [indicator random variables](/indicator-random-variable/), one for each event that costs a unit, and add their probabilities by [linearity of expectation](/linearity-of-expectation/). The indicators need not be independent. Other methods are recurrences in the expected cost, as for quicksort, and generating functions, which also give the variance and the full distribution.

**Mean and spread.** The mean alone can mislead. A result is stronger if the cost is also concentrated, for example with a small variance and the [Chebyshev inequality](/chebyshev-inequality/), or with a [high-probability bound](/high-probability-bounds/). For quicksort on a random permutation, the standard deviation is about $0.65n$ while the mean is about $2n\ln n$, so large deviations from the mean are rare for large $n$.

**Average-case complexity of problems.** For a problem with a distribution on its inputs, one asks if some algorithm is fast on average. The obvious definition, $\mathbb{E}[T] = n^{O(1)}$, has a defect. Let $T(x) = n$ for all strings of length $n$ but one, and $T(x) = 2^n$ on that one, with the uniform distribution on $\{0,1\}^n$. Then $\mathbb{E}[T] \le n + 1$, but $\mathbb{E}[T^2] \ge 2^{2n}\cdot 2^{-n} = 2^n$. So a machine that is polynomial on average can become exponential on average after a polynomial slowdown, such as a change of machine model. Levin's definition avoids this: $T$ is *polynomial on average* if $\mathbb{E}[T(x)^{\varepsilon}/n] = O(1)$ for some $\varepsilon > 0$. This class is closed under polynomial slowdowns, and Levin used it to define problems that are complete for average-case complexity.

## Examples

The table compares the worst case with the average over uniform random permutations of $n$ distinct items. The last two columns are for $n = 10$: the exact average and the mean of a simulation over 20000 random permutations (seed 3).

| algorithm and cost | worst case | average case | worst at $n = 10$ | average at $n = 10$ | simulated |
| --- | --- | --- | --- | --- | --- |
| [Linear search](/linear-search/), probes for a present key at a uniform position | $n$ | $(n+1)/2$ | 10 | 5.5 | 5.53 |
| [Insertion sort](/insertion-sort/), [inversions](/inversion/) (the number of shifts) | $n(n-1)/2$ | $n(n-1)/4$ | 45 | 22.5 | 22.45 |
| [Quicksort](/quicksort/) with the first item as pivot, comparisons | $n(n-1)/2$ | $2(n+1)H_n - 4n$ | 45 | 24.44 | 24.51 |
| [Hire-assistant](/hire-assistant/), hires | $n$ | $H_n$ | 10 | 2.93 | 2.93 |

- **Inversions.** For each pair $i < j$, the indicator of $a_i > a_j$ has probability $1/2$ in a random permutation, so the mean number of inversions is $\binom n2/2 = n(n-1)/4$. Insertion sort does one shift per inversion, so on average it does half the work of its worst case, still $\Theta(n^2)$.
- **Quicksort.** The average $2(n+1)H_n - 4n \approx 1.39\,n\lg n$ is $\Theta(n\log n)$, far below the worst case $\Theta(n^2)$. The proof is on the page [quicksort expected running time](/quicksort-expected-running-time/).
- **Hiring.** The candidate $i$ is the best so far with probability $1/i$, so the mean is $H_n \approx \ln n$, against $n$ in the worst case. See the [hiring problem](/hiring-problem/).
- **Hashing with chaining.** Under the [simple uniform hashing assumption](/uniform-hashing-assumption/), a successful search in a table with load factor $\alpha$ examines $1 + \alpha/2 - \alpha/(2n)$ items on average, against $n$ in the worst case. See [chaining analysis](/chaining-analysis/).
- **The simplex method.** It takes exponentially many steps on the [Klee-Minty cube](/klee-minty-cube/), but few on typical inputs. Average-case results for random linear programs explain part of this, and [smoothed analysis](/smoothed-analysis/) gives a stronger explanation.

## Where it is used

- **Choosing algorithms in practice.** Quicksort, hashing and the simplex method are used because their average cost is low, although their worst case is bad.
- **Randomized algorithms.** The same calculations, applied to an algorithm that shuffles or chooses at random, give guarantees for each input. Most analyses in CLRS Chapters 5, 7 and 11 work in both readings.
- **Data structures.** Random [binary search trees](/random-binary-search-tree/), skip lists and hash tables are analyzed by their expected depth or probe count.
- **Complexity theory.** Average-case hardness, from Levin's theory to the [worst-case to average-case reductions](/ajtai-worst-case-to-average-case-reduction/) for lattice problems, is the base of cryptography, which needs problems that are hard on random instances.
- **Pitfalls.** An average-case bound is a statement about a distribution. Real inputs are often partly sorted or adversarial, which breaks the uniform assumption; this is the reason to prefer a randomized algorithm, which makes the assumption true, or to also report the worst case. A mean can also hide a heavy tail, as the example of $T = 2^n$ on one input shows.

## References
