---
tag: 8V5HQT
kind: problem
slug: balls-into-bins
name: Balls into bins
aliases:
- balanced allocation
- bins and balls
- occupancy problem
area: foundations/probabilistic-analysis
level: core
summary: Throwing m balls uniformly into n bins; analyzes loads, empty bins and the maximum load.
prereqs: [indicator-random-variable, linearity-of-expectation, union-bound, chebyshev-inequality, binomial-distribution]
see_also: [balls-into-bins-max-load, power-of-two-choices, coupon-collector-problem, birthday-paradox, chaining-analysis, bucket-sort-expected-linear, random-load-balancing, poisson-distribution]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.4 (Balls and bins)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Section 5.2 (Balls into bins, the maximum load bound 3 ln n / ln ln n) and Section 5.4 (The Poisson approximation, the lower bound ln n / ln ln n)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 3, Section 3.1 (Occupancy problems)
  - paper: "Martin Raab and Angelika Steger, Balls into bins: a simple and tight analysis, Randomization and Approximation Techniques in Computer Science (RANDOM 1998), Lecture Notes in Computer Science 1518, Springer"
    locator: pp. 159 to 170, the maximum load for each range of m
  - paper: doi:10.1137/S0097539795288490
    title: Yossi Azar, Andrei Z. Broder, Anna R. Karlin and Eli Upfal, Balanced allocations, SIAM Journal on Computing 29(1), 1999
    locator: pp. 180 to 200, the maximum load ln ln n / ln d + O(1) with d choices
---

Balls into bins is the random process in which $m$ balls are thrown, each independently into a bin chosen uniformly from $n$ bins, and the questions about the resulting loads: how many bins stay empty, how many balls share a bin, and how large the fullest bin is. For $m = n$ the expected load of each bin is 1, about $n/e$ bins stay empty, and the maximum load is $\Theta(\ln n / \ln\ln n)$ with high probability. The model describes [hashing with chaining](/chaining-analysis/), [random load balancing](/random-load-balancing/), [bucket sort](/bucket-sort-expected-linear/) and many other randomized algorithms; the [birthday paradox](/birthday-paradox/) and the [coupon collector's problem](/coupon-collector-problem/) are two of its questions.

## In plain words

You have a row of boxes and a pile of balls. You throw each ball into a box picked at random, every box equally likely. When the balls and the boxes are equally many, each box gets one ball on average. But the balls do not spread out evenly. About a third of the boxes stay empty. Some box gets several balls.

The fullest box gets more balls than you might expect, and its load grows with the number of boxes, but very slowly: a little less than the logarithm of the number of boxes. With a million boxes the fullest one usually has eight to ten balls. Asking two random boxes and taking the less full one makes the fullest box much smaller.

## Definition

**Model.** Integers $m \ge 0$ and $n \ge 1$. Balls $1, \ldots, m$ choose bins $B_1, \ldots, B_m$, independent and uniform on $\{1, \ldots, n\}$. The load of bin $j$ is $L_j = |\{i : B_i = j\}|$.

**Questions.**

- the distribution of one load: $L_j$ is [binomial](/binomial-distribution/) with parameters $m$ and $1/n$, so $\mathbb{E}[L_j] = m/n$ and $\Pr[L_j = k] = \binom mk n^{-k}(1 - 1/n)^{m-k}$;
- the number of empty bins, $N_0 = |\{j : L_j = 0\}|$;
- the number of collisions, the pairs of balls in the same bin;
- the maximum load $M = \max_j L_j$;
- the first $m$ at which some event happens, such as the first collision or the first time no bin is empty.

**The main theorem for $m = n$.** For each $n \ge 16$, $\Pr[M \ge 3\ln n / \ln\ln n] \le 1/n$. And $\Pr[M < \ln n / \ln\ln n] \to 0$ as $n \to \infty$. So $M = \Theta(\ln n / \ln\ln n)$ with probability $1 - o(1)$. The proofs are in the Bounds section.

## Variants

- **More balls, $m \ge n$.** Raab and Steger give the maximum load for each range of $m$. For $m = n\ln n$ it is $\Theta(\ln n)$, and for $m \ge n\ln n$ it is $\frac mn + \Theta\bigl(\sqrt{m\ln n / n}\bigr)$, so the gap to the average shrinks relative to the average.
- **Two choices.** Each ball looks at $d \ge 2$ random bins and goes to the least loaded one. With $m = n$, the maximum load drops to $\frac{\ln\ln n}{\ln d} + O(1)$ with high probability (Azar, Broder, Karlin and Upfal). See [the power of two choices](/power-of-two-choices/).
- **Weighted or non-uniform bins.** Bins with different probabilities, or balls with weights, model servers of different speed and jobs of different size.
- **Sequential questions.** The [birthday paradox](/birthday-paradox/) asks for the first collision, at about $\sqrt{\pi n/2}$ balls. The [coupon collector's problem](/coupon-collector-problem/) asks for the first time with no empty bin, at about $n\ln n$ balls.

## Examples

**Empty bins.** Bin $j$ is empty with probability $(1 - 1/n)^m$, so by [linearity of expectation](/linearity-of-expectation/) $\mathbb{E}[N_0] = n(1 - 1/n)^m \approx ne^{-m/n}$. For $m = n$ the fraction of empty bins tends to $1/e = 0.3679$. At $n = 1000$ the exact expected fraction is $(0.999)^{1000} = 0.3677$.

**Collisions.** Each of the $\binom m2$ pairs of balls shares a bin with probability $1/n$, so the expected number of colliding pairs is $\binom m2 / n$. For $m = n$ this is $(n-1)/2$.

**The maximum load for $m = n$.** The table compares $\ln n/\ln\ln n$, the upper threshold $3\ln n/\ln\ln n$, and a simulation with numpy (seed 11) that gives the mean of the maximum load and its observed range.

| $n$ | runs | $\ln n / \ln\ln n$ | $3\ln n / \ln\ln n$ | mean of $M$ | observed $M$ | empty fraction |
| --- | --- | --- | --- | --- | --- | --- |
| $10^3$ | 2000 | 3.57 | 10.72 | 5.50 | 4 to 9 | 0.3679 |
| $10^4$ | 1000 | 4.15 | 12.44 | 6.71 | 5 to 10 | 0.3680 |
| $10^5$ | 300 | 4.71 | 14.14 | 7.77 | 7 to 10 | 0.3679 |
| $10^6$ | 100 | 5.26 | 15.78 | 8.84 | 8 to 11 | 0.3679 |
| $10^7$ | 20 | 5.80 | 17.39 | 9.75 | 9 to 11 | 0.3679 |

The observed maximum lies between the two thresholds in every run, at about 1.7 times $\ln n/\ln\ln n$. The constant 3 of the upper bound is loose and the constant 1 of the lower bound is the true one only in the limit, since $\ln\ln n$ grows so slowly.

## Known algorithms

The process itself is the algorithm: drawing $m$ uniform bin indices and counting takes $O(m + n)$ time. The interest is in algorithms whose cost is a function of the loads.

- **Hashing with chaining.** Under the [uniform hashing assumption](/uniform-hashing-assumption/), a table of $n$ slots with $m$ keys is balls into bins. A search costs $O(1 + m/n)$ in expectation, see [chaining analysis](/chaining-analysis/), but the longest chain for $m = n$ is $\Theta(\ln n/\ln\ln n)$.
- **Bucket sort.** For $n$ keys uniform in $[0, 1)$ and $n$ buckets, the expected sum of the squares of the loads is $2 - 1/n$ for each bucket, so the insertion sorts of the buckets take $O(n)$ expected time in total, see [bucket sort](/bucket-sort-expected-linear/).
- **Random and two-choice load balancing.** Sending each job to a random server gives the loads above. [The power of two choices](/power-of-two-choices/) gives an exponentially smaller maximum.

## Bounds

All bounds below are for $m = n$ balls. Write $L = \ln n / \ln\ln n$.

**Upper bound: $\Pr[M \ge 3L] \le 1/n$ for each $n \ge 16$.** Let $k = \lceil 3L\rceil$. Bin 1 has at least $k$ balls only if some set of $k$ balls all choose bin 1. There are $\binom nk$ such sets, each with probability $n^{-k}$, so by the [union bound](/union-bound/)
$$ \Pr[L_1 \ge k] \le \binom nk \frac{1}{n^k} \le \frac{n^k}{k!}\cdot\frac{1}{n^k} = \frac{1}{k!} \le \left(\frac ek\right)^k, $$
where $k! \ge (k/e)^k$ follows from $e^k = \sum_j k^j/j! \ge k^k/k!$. Now we show $(e/k)^k \le n^{-2}$, that is $k(\ln k - 1) \ge 2\ln n$. The function $x(\ln x - 1)$ increases for $x \ge 1$, since its derivative is $\ln x$, so it suffices to check $x = 3L$. Let $y = \ln\ln n$; then $y \ge 1$ for $n \ge 16 > e^e$, and
$$ 3L(\ln(3L) - 1) = \frac{3\ln n}{y}\bigl(\ln 3 + y - \ln y - 1\bigr) = 3\ln n\left(1 - \frac{\ln y - \ln 3 + 1}{y}\right). $$
The function $\ln y - y/3$ has its maximum $\ln 3 - 1$ at $y = 3$, so $\ln y - \ln 3 + 1 \le y/3$, and the bracket is at least $2/3$. Hence $3L(\ln(3L) - 1) \ge 2\ln n$. A union bound over the $n$ bins gives $\Pr[M \ge k] \le n \cdot n^{-2} = 1/n$. Since loads are integers, $M \ge 3L$ is the same event as $M \ge k$.

**Lower bound: $\Pr[M < L] \to 0$.** Let $k = \lceil L\rceil$, and let $X$ be the number of bins with load exactly $k$. If $X \ge 1$ then $M \ge k \ge L$, so it suffices to show $\Pr[X = 0] \to 0$. We use the second moment method.

*One bin.* Let $p = \Pr[L_1 = k] = \binom nk n^{-k}(1 - 1/n)^{n-k}$. First, $\binom nk n^{-k} = \frac{1}{k!}\prod_{i<k}(1 - i/n) \ge \frac{1}{k!}\bigl(1 - \frac{k^2}{2n}\bigr)$, because $\prod(1 - a_i) \ge 1 - \sum a_i$ for $a_i \in [0, 1]$. Second, $(1 - 1/n)^{n-k} \ge (1 - 1/n)^{n-1} \ge 1/e$, because $(1 + \frac{1}{n-1})^{n-1} \le e$. So $p \ge \bigl(1 - \frac{k^2}{2n}\bigr)/(e\,k!)$.

*Two bins.* For $j \ne j'$, let $q = \Pr[L_j = L_{j'} = k] = \frac{n!}{k!\,k!\,(n-2k)!}n^{-2k}(1 - 2/n)^{n-2k}$. Divide by $p^2$. The ratio of the counting factors is $\prod_{i<k}\frac{n-k-i}{n-i} \le 1$. The ratio of the remaining factors is
$$ \frac{(1 - 2/n)^{n-2k}}{(1 - 1/n)^{2n-2k}} = \left(\frac{1 - 2/n}{(1 - 1/n)^2}\right)^{n-2k}\left(1 - \frac1n\right)^{-2k} \le \left(\frac{n}{n-1}\right)^{2k} \le e^{2k/(n-1)}, $$
since $1 - 2/n \le (1 - 1/n)^2$. So $q \le p^2 e^{2k/(n-1)}$.

*Chebyshev.* $\mathbb{E}[X] = np$ and $\operatorname{Var}[X] = np(1-p) + n(n-1)(q - p^2) \le np + n^2p^2(e^{2k/(n-1)} - 1)$. By [Chebyshev's inequality](/chebyshev-inequality/),
$$ \Pr[X = 0] \le \frac{\operatorname{Var}[X]}{(np)^2} \le \frac{1}{np} + e^{2k/(n-1)} - 1. $$
The second term tends to 0 because $k = O(\log n)$. For the first, $k \le L + 1$, and $\ln k! \le k\ln k \le (L+1)\ln(L+1) \le L\ln L + \ln(L + 1) + 1$, with
$$ L\ln L = \frac{\ln n}{\ln\ln n}(\ln\ln n - \ln\ln\ln n) = \ln n - \frac{\ln n\,\ln\ln\ln n}{\ln\ln n}. $$
So $\ln(n/k!) \ge \frac{\ln n\,\ln\ln\ln n}{\ln\ln n} - O(\ln\ln n) \to \infty$, and $np \ge \frac{n}{e\,k!}(1 - o(1)) \to \infty$. Hence $\Pr[M < L] \le \Pr[X = 0] \to 0$. At $n = 10^6$ the bound on $\Pr[X = 0]$ is $0.0020$, and at $n = 10^9$ it is $1.4 \times 10^{-5}$.

**The sharp form.** Both constants can be made exact: $M = (1 + o(1))\ln n / \ln\ln n$ with high probability. Mitzenmacher and Upfal prove the lower bound with probability $1 - 1/n$ for large $n$ by the Poisson approximation, and Raab and Steger give the precise second-order terms.

**Other ranges of $m$.** For $m = cn\ln n$ with a constant $c$, the maximum load is $\Theta(\ln n)$. For $m = o(\sqrt n)$ there is no collision with high probability, so $M = 1$, and for $m = \Theta(\sqrt n)$ the probability of $M \ge 2$ is a constant, by the [birthday paradox](/birthday-paradox/).

## Reductions

- **Coupon collector.** "No bin is empty after $m$ balls" is "all $n$ coupons are collected after $m$ draws". The [coupon collector's problem](/coupon-collector-problem/) is the question of the first such $m$.
- **Poisson approximation.** The loads $(L_1, \ldots, L_n)$ have the same distribution as independent Poisson variables with mean $m/n$, conditioned on their sum being $m$. If the probability of an event is monotone in the number of balls, then its probability in the exact model is at most twice its probability in the independent model. This is how Mitzenmacher and Upfal, Section 5.4, turn independent calculations into results for balls and bins. See the [Poisson distribution](/poisson-distribution/).
- **Random functions.** Throwing $m$ balls into $n$ bins is choosing a uniformly random function from $m$ items to $n$ values. Hash functions under the uniform hashing assumption are this model.

## Applications

- **Hash tables.** The worst chain of a table with chaining and load factor 1 has length $\Theta(\log n / \log\log n)$, which bounds the worst lookup time with high probability.
- **Load balancing.** The extra load of the busiest server when jobs go to random servers, and its reduction by two choices, as in [random load balancing](/random-load-balancing/).
- **Bucket sort and hashing-based partitioning**, where the cost is a sum of functions of the loads.
- **Distributed systems.** Consistent hashing, sharding and random placement of replicas are balls into bins with extra structure.

## References
