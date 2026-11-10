---
tag: QEGCXA
kind: problem
slug: weighted-sampling
name: Weighted sampling
aliases:
- weighted random choice
- sampling from a discrete distribution
- weighted random sampling
area: randomized/sampling
level: core
summary: Pick index i with probability proportional to its weight w_i, with or without replacement.
prereqs: [discrete-probability-distribution, prefix-sums, binary-search]
see_also: [alias-method, inverse-transform-sampling, gumbel-max-trick, weighted-reservoir-sampling, probability-proportional-to-size-sampling, random-variate-generation, fenwick-tree, rejection-sampling]
sources:
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter III, Sections 2 to 4 (inversion with guide tables, the alias method) and Chapter XV (the random bit model)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition, Addison-Wesley, 1997
    locator: Section 3.4.1 (general discrete distributions and the alias method)
  - paper: doi:10.1145/355744.355749
    title: Alastair J. Walker, An efficient method for generating discrete random variables with general distributions, ACM Transactions on Mathematical Software 3(3), 1977
    locator: pages 253 to 256
  - paper: doi:10.1016/j.ipl.2005.11.003
    title: Pavlos S. Efraimidis and Paul G. Spirakis, Weighted random sampling with a reservoir, Information Processing Letters 97(5), 2006
    locator: pages 181 to 185 (the key u^(1/w) and its equivalence to sampling without replacement)
  - paper: "Donald E. Knuth and Andrew C. Yao, The complexity of nonuniform random number generation, in J. F. Traub (editor), Algorithms and Complexity: New Directions and Recent Results, Academic Press, 1976"
    locator: pages 357 to 428 (the DDG tree and the entropy bounds)
  - paper: "Yossi Matias, Jeffrey Scott Vitter and Wen-Chun Ni, Dynamic generation of discrete random variates, Proceedings of the 4th ACM-SIAM Symposium on Discrete Algorithms, 1993"
    locator: pages 361 to 370
---

Weighted sampling is the problem of choosing an index $i \in \{1, \ldots, n\}$ with probability $w_i / W$, where $w_1, \ldots, w_n \ge 0$ are given weights and $W = \sum_j w_j > 0$. With replacement, the task is to produce many independent such indices, and the questions are the preprocessing time, the time per draw, the space and the cost of weight updates. The [alias method](/alias-method/) answers all draws in $O(1)$ after $O(n)$ preprocessing, and [inversion](/inverse-transform-sampling/) with [binary search](/binary-search/) takes $O(\log n)$ per draw. Without replacement, the task is to choose $k$ distinct indices, and the phrase has two different meanings: successive sampling, which draws one index at a time in proportion to the weights that remain, and designs with inclusion probabilities exactly proportional to the weights. They give different samples. This page states the problems and maps the methods; the methods have their own pages.

## In plain words

You have a list of items, and each item has a weight. You want to pick one item at random so that an item with twice the weight is twice as likely to be picked. A raffle is the picture: each person holds as many tickets as their weight, and one ticket is drawn.

If you draw many times and put each ticket back, the questions are how fast each draw is and how much setup you need. If weights change between draws, updates matter too.

If you want several different items, there is a choice to make. You can draw one ticket, remove all of that person's tickets, and draw again. Or you can ask that each person ends up in the sample with a probability proportional to their weight. These two rules sound alike, but they give different chances.

## Definition

**Input.** Weights $w_1, \ldots, w_n \ge 0$ with $W = \sum_j w_j > 0$, and a source of randomness: uniform reals in the [real RAM](/real-ram/) model, uniform integers in a range in the [word RAM](/word-ram/) model, or fair bits in the random bit model. Let $p_i = w_i / W$.

**With replacement.** Output a sequence $I_1, I_2, \ldots$ of independent indices with $\Pr[I_t = i] = p_i$. The number of draws $m$ may be unknown in advance. The costs are the preprocessing time and space, the time (or the number of random bits) per draw, and in the dynamic version the time to change one weight.

**Without replacement, successive sampling.** For $k \le |\{i : w_i > 0\}|$, output distinct $I_1, \ldots, I_k$ such that

$$\Pr[I_1 = i_1, \ldots, I_k = i_k] = \prod_{t=1}^{k}\frac{w_{i_t}}{W - w_{i_1} - \cdots - w_{i_{t-1}}}.$$

This is the Plackett-Luce law: draw one index by weight, remove it, and repeat.

**Without replacement, proportional inclusion.** Output a set $S$ of size $k$ with $\Pr[i \in S] = \pi_i$, where $\pi_i = k w_i / W$, after capping the indices with $k w_i > W$ at $\pi_i = 1$. This is [PPS sampling](/probability-proportional-to-size-sampling/), and many designs (joint laws of $S$) have the same $\pi_i$.

**Exactness.** With rational weights and uniform integers, the output law can be exactly the one asked for. With floating-point weights and uniform reals, every method has rounding error. The pages of the methods say which steps are exact.

## Variants

- **Static or dynamic.** In the dynamic version, weights change, are inserted or are deleted between draws.
- **Streaming.** The weights arrive one at a time, the sample must be kept in small memory, and $n$ is not known in advance. See [weighted reservoir sampling](/weighted-reservoir-sampling/) and [stream sampling](/stream-sampling/).
- **Log-domain weights.** The input is $\phi_i = \log w_i$, as in a softmax over scores. The [Gumbel-max trick](/gumbel-max-trick/) samples without computing $W$ or leaving the log domain.
- **Unknown total.** Only an upper bound $w_{\max}$ on each weight is known, or only a few weights can be read at a time. Then [rejection](/rejection-sampling/) from a uniform index is the natural method.
- **Random bit model.** The cost is the number of fair bits used. See [random variate generation](/random-variate-generation/).
- **Uniform weights.** All $w_i$ equal gives uniform sampling: a uniform index with replacement, and a [uniform random subset](/uniform-random-subset/) or [Floyd's sampling](/floyd-sampling/) without replacement.
- **Independent inclusion.** Include each index independently with probability $\pi_i$. The sample size is random. See [Bernoulli sampling](/bernoulli-sampling/).

## Examples

Take $w = (1, 2, 3, 4)$, so $W = 10$ and $p = (0.1, 0.2, 0.3, 0.4)$.

**Inversion.** The prefix sums are $(1, 3, 6, 10)$. A uniform integer $r \in \{0, \ldots, 9\}$ selects the first index whose prefix sum exceeds $r$: $r = 0$ gives index 1, $r \in \{1, 2\}$ gives 2, $r \in \{3, 4, 5\}$ gives 3, and $r \in \{6, \ldots, 9\}$ gives 4.

**Rejection from a uniform index.** Pick $i$ uniformly and accept with probability $w_i / w_{\max} = w_i / 4$. One try succeeds with probability $W / (n w_{\max}) = 10/16$, so the expected number of tries is $1.6$.

**Two without replacement.** Successive sampling of $k = 2$ gives the inclusion probabilities

| index | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| successive sampling | 0.2345 | 0.4413 | 0.6083 | 0.7159 |
| proportional inclusion $2 w_i / W$ | 0.2 | 0.4 | 0.6 | 0.8 |

from $\Pr[i \in S] = p_i + \sum_{j \ne i} p_j\,p_i/(1 - p_j)$. Both rows sum to 2. Successive sampling favors light items: once a heavy item is drawn, the light items share its weight. A Horvitz-Thompson estimate that uses the second row with a successive sample is biased.

**Random bits.** The entropy of $p$ is $H(p) \approx 1.846$ bits. The Knuth-Yao sampler uses about $3.0$ fair bits per draw on average, within the bound $H + 2$. Inversion with a uniform integer in $\{0, \ldots, 9\}$ made by rejection from 4 bits uses $4 \cdot 16/10 = 6.4$ bits per draw on average.

## Known algorithms

With replacement:

| method | preprocessing | per draw | update | notes |
|---|---|---|---|---|
| linear scan (sequential inversion) | none | $O(n)$ | $O(1)$ | sort weights in decreasing order to cut the mean scan |
| [inversion](/inverse-transform-sampling/) with [prefix sums](/prefix-sums/) and binary search | $O(n)$ | $O(\log n)$ | $O(n)$ | exact with integer weights |
| inversion with a guide table | $O(n)$ | $O(1)$ expected | $O(n)$ | Devroye III.2 |
| [alias method](/alias-method/) (Walker, Vose) | $O(n)$ | $O(1)$ | $O(n)$ | one uniform and one comparison per draw |
| [rejection](/rejection-sampling/) from a uniform index | none | $O(n w_{\max} / W)$ expected | $O(1)$ | good when weights are similar |
| [Fenwick tree](/fenwick-tree/) or [segment tree](/segment-tree/) descent | $O(n)$ | $O(\log n)$ | $O(\log n)$ | the simple dynamic method |
| [Gumbel-max](/gumbel-max-trick/) | none | $O(n)$ | $O(1)$ | log-domain weights, no normalization |

For $m$ draws at once, sort $m$ uniforms (or generate them in sorted order from exponential spacings) and merge them with the prefix sums in $O(n + m)$ time. Matias, Vitter and Ni (1993) gave a dynamic structure with fast expected draws and updates.

Without replacement:

- **Successive sampling.** $k$ draws with a Fenwick tree, setting each drawn weight to 0: $O(n + k \log n)$. Or the Efraimidis-Spirakis keys $u_i^{1/w_i}$, or equally the [Gumbel top-k](/gumbel-max-trick/) keys $\log w_i + G_i$, and the $k$ largest by [top-k selection](/top-k-selection/): $O(n)$ with selection, or $O(n \log k)$ in one pass with a heap. This works on a stream; see [weighted reservoir sampling](/weighted-reservoir-sampling/).
- **Proportional inclusion.** Systematic PPS in one pass of $O(n)$, Sampford's method, or conditional Poisson sampling. See [PPS sampling](/probability-proportional-to-size-sampling/).
- **Independent inclusion.** One Bernoulli trial per index, or geometric skips when all $\pi_i$ are equal. [Priority sampling](/priority-sampling/) gives a fixed-size sample with unbiased subset-sum estimates.

## Bounds

**Preprocessing must read the input.** Allow zero weights, and let $e_j$ be the input with weight 1 at position $j$ and 0 elsewhere; on $e_j$ the only correct output is $j$. Fix the random choices of an exact sampler and answer every read with 0. If this run stops after fewer than $n - 1$ reads, two positions $j \ne j'$ are unread, and the run is the same on $e_j$ and on $e_{j'}$, so it gives the same output on both, and one of them is wrong. So this run reads at least $n - 1$ positions. On $e_j$ the real run follows it until position $j$ is read, so for $j$ uniform the expected number of reads is at least about $(n-1)/2$. Hence any exact sampler for arbitrary weights reads $\Omega(n)$ weights in expectation on some input. The alias method and inversion meet this with $O(n)$ preprocessing. Rejection avoids it only because it assumes a known bound $w_{\max}$.

**Per draw.** In the real RAM or word RAM models, $O(1)$ per draw is reached by the alias method, so the per-draw cost is $\Theta(1)$.

**Random bits.** Knuth and Yao (1976) showed that every exact sampler from fair bits uses at least $H(p) = -\sum p_i \log_2 p_i$ bits per draw on average, and that the optimal sampler, a walk on the binary expansions of the $p_i$ (the DDG tree), uses fewer than $H(p) + 2$. The bound $H(p)$ cannot be beaten because the output itself carries $H(p)$ bits of information; see [Shannon entropy](/shannon-entropy/).

**Without replacement.** Any algorithm must read all $n$ weights for the same reason as above, and it outputs $k$ indices, so $\Omega(n)$ is a lower bound, met by the key methods with linear-time selection and by systematic PPS.

## Reductions

- **To and from [random variate generation](/random-variate-generation/).** Weighted sampling with replacement is the generation of a discrete random variable with finite support. Generating any discrete variable with finite support is weighted sampling.
- **To sorting by random keys.** Successive sampling of all $n$ indices is the same as sorting by the keys $u_i^{1/w_i}$, or by $\log w_i + G_i$ with Gumbel noise $G_i$, or by $E_i / w_i$ with exponential $E_i$ in increasing order. With equal weights this gives a uniform [random permutation](/random-permutation/).
- **To uniform sampling.** With integer weights, weighted sampling is uniform sampling of a ticket among $W$ tickets. This is the exact method used by inversion with a uniform integer.
- **From importance sampling.** [Resampling](/resampling/) in [particle filters](/particle-filter/) and sampling-importance-resampling is weighted sampling with the importance weights.

## Applications

- Resampling steps of [sequential Monte Carlo](/sequential-monte-carlo/) and [particle filters](/particle-filter/).
- Drawing the next token from the softmax output of a language model, and sampling actions from a stochastic policy.
- Random walks on weighted graphs, and the choice of the next reaction in stochastic chemical simulation.
- Survey sampling with unequal probabilities, and auditing with monetary unit sampling, through [PPS sampling](/probability-proportional-to-size-sampling/).
- Negative sampling and frequency-based sampling tables in machine learning, which often use the [alias method](/alias-method/).

## References
