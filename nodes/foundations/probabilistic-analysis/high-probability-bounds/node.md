---
tag: 4DR1QV
kind: concept
slug: high-probability-bounds
name: With high probability
aliases:
- High probability
area: foundations/probabilistic-analysis
level: core
summary: An event holds with high probability when it fails with probability at most n^-c for input size n; such bounds survive union bounds over polynomially many events.
prereqs: [randomized-algorithm, union-bound, chernoff-bound, markov-inequality]
see_also: [randomized-quicksort, quicksort-expected-running-time, error-amplification, monte-carlo-algorithm, balls-into-bins, skip-list, karger-min-cut, concentration-of-measure]
sources:
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms, Cambridge University Press, 2009
    locator: Chapter 2, Applications of the Chernoff-Hoeffding Bounds, Section 2.1, Probabilistic Amplification, Section 2.3, Skip Lists, and Section 2.4, Quicksort
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Section 1.5, Application, A Randomized Min-Cut Algorithm; Section 2.5, Application, The Expected Run-Time of Quicksort; Section 4.2, Deriving and Applying Chernoff Bounds
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Section 1.2, Las Vegas and Monte Carlo; Chapter 4, Tail Inequalities (Section 4.1, The Chernoff Bound); Section 8.3, Skip Lists
  - url: "https://en.wikipedia.org/wiki/With_high_probability"
    locator: lead (the convention that the probability tends to 1 as n grows)
---

An event about a [randomized algorithm](/randomized-algorithm/) on inputs of size $n$ holds *with high probability* (w.h.p.) when it fails with probability at most $n^{-c}$ for a constant $c > 0$, usually $c \ge 1$. A bound of this form says more than a bound on the [expected value](/expected-value/): it says that a bad run is so rare that a [union bound](/union-bound/) over polynomially many such events still leaves a rare failure. Most such bounds come from a [Chernoff bound](/chernoff-bound/) for one item, followed by a union bound over all items. The standard example is that [randomized quicksort](/randomized-quicksort/) makes $O(n \log n)$ comparisons with probability at least $1 - n^{-2}$.

## In plain words

An average running time does not tell you how often a randomized program is slow. Two programs with the same average can behave very differently: one is always close to its average, the other is usually fast and once in a while extremely slow.

A high-probability bound closes this gap. It says that the program is slow only with a chance that shrinks quickly as the input grows, for example one in a million for an input of a thousand items, and one in a trillion for an input of a million items. At that rate you can ask the same question about every item, every step or every machine at once, add up the small chances, and still be almost sure that nothing goes wrong. You can usually make the chance even smaller by accepting a larger constant in the bound.

## The idea

### The definition

Let $n$ be the input size, and let $E_n$ be an event, for example "the algorithm finishes within $\alpha\, n \log n$ steps". Three conventions are in use, and a page or a paper must say which one it means.

1. **Fixed exponent.** $E_n$ holds with high probability if $\Pr(\overline{E_n}) \le n^{-c}$ for all large $n$, for a stated constant $c > 0$. Many texts take $c = 1$, or allow $O(n^{-c})$.
2. **Every exponent, with the constant in the bound.** A random quantity $T$ is $O(f(n))$ with high probability if for each $c > 0$ there is a constant $\alpha_c$ with $\Pr(T > \alpha_c f(n)) \le n^{-c}$ for all large $n$. This is the strong form. The quicksort bound below has it.
3. **Probability tending to 1.** In the theory of random graphs, "with high probability" often means only $\Pr(E_n) \to 1$, also called *asymptotically almost surely*. This is much weaker: a failure probability of $1/\ln n$ qualifies.

None of these means *almost surely*, which says that the probability is exactly 1. A randomized quicksort run of more than $n^2$ comparisons is impossible, but a run of more than $24\, n \ln n$ comparisons has a positive probability, so the bound below holds with high probability and not almost surely.

### Why the polynomial rate matters

**Union bounds compose.** If $E_1, \ldots, E_m$ are events with $\Pr(\overline{E_i}) \le n^{-c}$ each and $m \le n^d$, then by the [union bound](/union-bound/)
$$ \Pr\Big(\bigcap_i E_i\Big) \ge 1 - \sum_i \Pr(\overline{E_i}) \ge 1 - n^{d - c}. $$
So "each of the $n$ elements has depth $O(\log n)$" becomes "all elements have depth $O(\log n)$" at the cost of one in the exponent. No independence between the events is needed. A failure probability that is only constant, or $1/\log n$, does not survive this step.

**The exponent can be bought with the constant.** For the sums of independent indicators that most algorithms produce, the failure probability falls exponentially in the threshold, so raising the threshold by a constant factor raises the exponent $c$ by a constant factor. The quicksort example shows this with explicit numbers.

**Repetition.** A [Monte Carlo algorithm](/monte-carlo-algorithm/) with one-sided error at most $\frac12$ errs in all of $k$ independent runs with probability at most $2^{-k}$. With $k = \lceil c\lg n \rceil$ runs this is at most $n^{-c}$, at a cost of a factor $O(\log n)$ in time. For two-sided error, a majority vote over $O(c\log n)$ runs gives the same with a Chernoff bound. This is [error amplification](/error-amplification/).

### High probability and expectation

**From a high-probability bound to an expected bound.** Suppose that $0 \le T \le T_{\max}(n)$ always, and $\Pr(T > \alpha f(n)) \le n^{-c}$. Split the expectation on the event $\{T \le \alpha f(n)\}$:
$$ \mathbb{E}[T] \le \alpha f(n) + T_{\max}(n)\, n^{-c}. $$
So if $T_{\max}(n) \le n^c f(n)$, then $\mathbb{E}[T] = O(f(n))$. For quicksort, $T_{\max} = n(n-1)/2$ comparisons, and $c = 2$ suffices. Without a worst-case bound this fails: let $T = n$ with probability $1 - 2^{-n}$ and $T = 2^{2n}$ otherwise. Then $\Pr(T > n) = 2^{-n} \le n^{-c}$ for each $c$ and all large $n$, so $T = O(n)$ with high probability in the strong sense, but $\mathbb{E}[T] \ge 2^{n}$.

**From an expected bound to a high-probability bound.** In general, only [Markov's inequality](/markov-inequality/) is available: $\Pr(T \ge t\,\mathbb{E}[T]) \le 1/t$. For a failure probability of $n^{-c}$ this needs the threshold $n^c\,\mathbb{E}[T]$, which is not $O(\mathbb{E}[T])$. A concrete gap: let $T = n^2$ with probability $1/n$ and $T = n$ otherwise. Then $\mathbb{E}[T] = 2n - 1$, and $\Pr(T > \alpha n) = 1/n$ for each $\alpha$ with $1 \le \alpha < n$. So $T = O(n)$ holds with probability $1 - 1/n$ (the fixed exponent $c = 1$), but not with probability $1 - n^{-2}$ for any constant $\alpha$, so $T$ is not $O(n)$ in the strong sense. For a [Las Vegas algorithm](/las-vegas-algorithm/) that restarts after a time limit, Markov's inequality plus independent restarts does give an exponential tail, see [Markov's inequality](/markov-inequality/).

### Pitfalls

- **Name the convention.** "With high probability" means $1 - 1/n$ in one text, $1 - n^{-c}$ for every $c$ in another, and only "tends to 1" in a third. A bound proved for $c = 1$ cannot be used in a union bound over $n^2$ events.
- **The $n$ is the input size.** In a recursive algorithm, a subproblem of size $m$ does not fail with probability $m^{-c}$ in a useful sense, because $m$ may be a constant. Bound each event in terms of the original $n$, as the quicksort proof below does for every element at every depth.
- **The constant depends on $c$.** "$T = O(f(n))$ w.h.p." in the strong sense hides a constant $\alpha_c$ that grows with $c$. Quoting the constant for one $c$ and the probability for another is an error.
- **Union bounds over too many events.** The bound $1 - n^{d - c}$ is useless when the number of events grows faster than $n^c$, for example over all $2^n$ subsets of the input.
- **Independence is needed for the per-item bound.** The Chernoff step needs independence, or the domination argument used below. The union step needs nothing.

## Examples

### Randomized quicksort makes O(n log n) comparisons with high probability

[Randomized quicksort](/randomized-quicksort/) on $n$ distinct keys works as follows. A call on a subarray of size at most 1 returns. A call on a subarray of size $m \ge 2$ picks a pivot uniformly at random from the $m$ keys, independently of all earlier choices, compares each other key with the pivot once, and recurses on the keys smaller and larger than the pivot. Its expected number of comparisons is $2(n+1)H_n - 4n$, see [quicksort expected running time](/quicksort-expected-running-time/).

**Claim.** For each $n \ge 3$, with probability at least $1 - n^{-2}$, every key takes part in fewer than $24\ln n$ comparisons as a non-pivot. Hence the total number of comparisons $C$ is less than $24\, n\ln n$, and the depth of the recursion is less than $24\ln n + 1$.

*Proof.*

1. *Counting by keys.* For a key $x$, its *chain* is the sequence of calls of size at least 2 whose subarray contains $x$, in the order of the recursion. Let $D_x$ be the number of calls on the chain where $x$ is not the pivot. In each such call $x$ is compared with the pivot once, and every comparison has this form. So $C = \sum_x D_x$.
2. *Good calls.* A call of size $m \ge 2$ is *good* if both parts it creates have size at most $3m/4$. With the pivot of rank $r$, this is $r - 1 \le 3m/4$ and $m - r \le 3m/4$. The integers $r$ in $[m/4,\, 3m/4 + 1] \cap [1, m]$ qualify, and there are at least $m/2$ of them for each $m \ge 2$. The pivot is uniform among the $m$ keys, independently of everything that happened before the call, so the call is good with probability at least $\frac12$ given the past.
3. *Shrinking.* In a call of size $m$ on the chain where $x$ is not the pivot, the next subarray that contains $x$ has size at most $m - 1$, and at most $3m/4$ if the call is good.
4. *Few good calls before the end.* Let $L = \lceil 24\ln n \rceil$ and suppose $D_x \ge L$. Then the first $L$ calls on the chain all exist and do not have $x$ as pivot. If $G$ of them are good, then by step 3 the subarray that contains $x$ after them has size at most $n(3/4)^G$, and this size is at least 1. So $G \le t$ with $t = \ln n/\ln(4/3) = 3.476\ln n$.
5. *Domination by a binomial.* For $j = 1, \ldots, L$, let $G_j = 1$ if the $j$-th call on the chain is good or does not exist, and $G_j = 0$ otherwise. By step 2, $\Pr(G_j = 1 \mid G_1, \ldots, G_{j-1}) \ge \frac12$. By step 4, $\{D_x \ge L\} \subseteq \{G_1 + \cdots + G_L \le t\}$. The lemma below gives $\Pr(G_1 + \cdots + G_L \le t) \le \Pr(\mathrm{Bin}(L, \frac12) \le t)$.
6. *Chernoff lower tail.* For $X \sim \mathrm{Bin}(L, \frac12)$ with mean $\mu = L/2 \ge 12\ln n$, the [Chernoff bound](/chernoff-bound/) gives $\Pr(X \le (1 - \delta)\mu) \le e^{-\delta^2\mu/2}$ for $0 < \delta < 1$. Take $\delta = 1 - t/\mu$, which lies in $(0, 1)$. Then $\delta^2\mu/2 = (\mu - t)^2/(2\mu)$, which increases with $\mu$ for $\mu > t$, so it is at least $(12 - 3.476)^2\ln n/24 = 3.027\ln n$. Hence $\Pr(D_x \ge L) \le n^{-3.027} \le n^{-3}$.
7. *Union over keys.* By the union bound over the $n$ keys, $\Pr(\text{some } D_x \ge L) \le n \cdot n^{-3} = n^{-2}$. Otherwise each $D_x \le L - 1 < 24\ln n$, so $C < 24\, n\ln n$, and each chain, so each path of the recursion, has fewer than $24\ln n + 1$ calls. $\square$

*Lemma (domination).* Let $G_1, \ldots, G_L$ take values in $\{0, 1\}$, with $\Pr(G_j = 1 \mid G_1, \ldots, G_{j-1}) \ge p$ for each $j$ and each history of positive probability. Then for each real $t$, $\Pr(G_1 + \cdots + G_L \le t) \le h_L(t)$, where $h_L(t) = \Pr(\mathrm{Bin}(L, p) \le t)$.

*Proof.* Induction on $L$. For $L = 0$ both sides equal $1[0 \le t]$. For $L \ge 1$, condition on $G_1 = g$. Under this condition, $G_2, \ldots, G_L$ satisfy the hypothesis with $L - 1$ variables, so $\Pr(\sum_j G_j \le t \mid G_1 = g) \le h_{L-1}(t - g)$. Let $\pi = \Pr(G_1 = 1) \ge p$. Then
$$ \Pr\Big(\sum_j G_j \le t\Big) \le \pi\,h_{L-1}(t-1) + (1 - \pi)\,h_{L-1}(t) \le p\,h_{L-1}(t-1) + (1 - p)\,h_{L-1}(t) = h_L(t). $$
The second step holds because $h_{L-1}(t-1) \le h_{L-1}(t)$ and $\pi \ge p$. The last equality conditions on the first trial of $\mathrm{Bin}(L, p)$. $\square$

The constant 24 gives the exponent 3. A larger constant $\alpha$ in place of 24 gives the exponent $(\alpha/2 - 3.476)^2/\alpha$, which grows without bound, so for each $c$ some $\alpha_c$ gives $\Pr(C \ge \alpha_c n\ln n) \le n^{-c}$. This is the strong form of "$C = O(n\log n)$ with high probability".

*The numbers.* The table follows the proof for three input sizes. The column "binomial tail" is the exact value of $\Pr(\mathrm{Bin}(L, \frac12) \le t)$, the quantity that step 6 bounds.

| $n$ | $t = \log_{4/3} n$ | $L = \lceil 24\ln n \rceil$ | Chernoff bound, step 6 | binomial tail | $n^{-3}$ |
| --- | --- | --- | --- | --- | --- |
| $10^3$ | 24.0 | 166 | $7.9 \times 10^{-10}$ | $6.9 \times 10^{-22}$ | $10^{-9}$ |
| $10^6$ | 48.0 | 332 | $6.2 \times 10^{-19}$ | $3.2 \times 10^{-42}$ | $10^{-18}$ |
| $10^9$ | 72.0 | 498 | $4.9 \times 10^{-28}$ | $1.7 \times 10^{-62}$ | $10^{-27}$ |

The Chernoff step is loose. With the exact binomial tail in step 6, the least $L$ with $\Pr(\mathrm{Bin}(L, \frac12) \le t) \le n^{-2}$ is 95, 193 and 292 for the three sizes, about $14\ln n$, so the same proof gives, for these three sizes, $C < 14.1\, n\ln n$ with probability at least $1 - 1/n$.

The bound is still far above the typical run. For $n = 10^6$:

| quantity | value |
| --- | --- |
| expected comparisons $2(n+1)H_n - 4n$ | $2.479 \times 10^7$ |
| comparisons in 10 simulated runs | $2.395 \times 10^7$ to $2.532 \times 10^7$ |
| high-probability bound $24\, n\ln n$, failure at most $10^{-12}$ | $3.316 \times 10^8$ |
| largest $D_x$ in the 10 runs (the height of the recursion tree minus 1) | 46 to 53 |
| bound on each $D_x$ from the proof | 331 |
| Markov's bound on $\Pr(C \ge 24\, n\ln n)$ from the mean | 0.0748 |

The last row shows what the expected value alone gives for the same threshold: a failure bound of 7.5 percent instead of $10^{-12}$. The high-probability bound is a statement about the tail, and the expected value cannot replace it.

### The largest bin and the coupon collector

When $n$ balls go into $n$ random bins, each bin has at least $k = \lceil 3\ln n/\ln\ln n \rceil$ balls with probability at most $1/k! \le n^{-2}$, and a union bound over the bins shows that the largest bin has fewer than $k$ balls with probability at least $1 - 1/n$. The proof and the exact numbers are on the page of the [union bound](/union-bound/). For the [coupon collector](/coupon-collector-problem/) with $n$ types, the same two steps show that $(1 + c)\,n\ln n$ draws see every type with probability at least $1 - n^{-c}$: each type is missed with probability at most $e^{-(1+c)\ln n} = n^{-1-c}$, and there are $n$ types. The exponent $c$ is bought with the constant $1 + c$, as in the quicksort bound.

### Skip lists

In a [skip list](/skip-list/) with $n$ keys, each key is promoted to each next level with probability $\frac12$, independently. A key reaches level $k$ with probability $2^{-k}$, so by the union bound the list has a level $k$ or higher with probability at most $n\,2^{-k}$. With $k = (c + 1)\lg n$ this is $n^{-c}$. So the height is at most $(c+1)\lg n$ with probability at least $1 - n^{-c}$. The search time is also $O(\log n)$ with high probability (Motwani and Raghavan, Section 8.3; Dubhashi and Panconesi, Section 2.3).

### Repeated Karger contractions

One run of [Karger's min cut algorithm](/karger-min-cut/) on a graph with $n$ vertices finds a given minimum cut with probability at least $2/(n(n-1)) = 1/\binom n2$ (Mitzenmacher and Upfal, Section 1.5). With $N = \lceil \binom n2 \ln n \rceil$ independent runs, all miss with probability at most $(1 - 1/\binom n2)^N \le e^{-\ln n} = 1/n$. With $c\binom n2\ln n$ runs the failure probability is at most $n^{-c}$.

## Where it is used

- **Randomized sorting and selection.** [Randomized quicksort](/randomized-quicksort/) runs in $O(n\log n)$ time with high probability, as shown above. The same good-pivot argument bounds the recursion depth, so the stack depth is $O(\log n)$ with high probability.
- **Randomized data structures.** The height of a [skip list](/skip-list/) and the depth of a [treap](/treap/) are $O(\log n)$ with high probability. The longest chain of a [hash table](/hash-table/) with a random hash function and load factor 1 is $O(\log n/\log\log n)$ with high probability, see [balls into bins](/balls-into-bins/), and $O(\log\log n)$ with the [power of two choices](/power-of-two-choices/).
- **Monte Carlo algorithms.** [Error amplification](/error-amplification/) turns a constant error into $n^{-c}$ with $O(c\log n)$ repetitions. [Karger's min cut algorithm](/karger-min-cut/) is the standard example.
- **Parallel and distributed algorithms.** When $n$ processors each run a random process, the algorithm finishes when the slowest one finishes. A bound for one processor with failure $n^{-c}$ plus a union bound gives a bound for all of them.
- **Proof structure.** The pattern "a [Chernoff bound](/chernoff-bound/) for one item, then a union bound over polynomially many items" appears in load balancing, routing, sampling and sketching, and in the [concentration of measure](/concentration-of-measure/) results that replace Chernoff when the variables are dependent.

## References
