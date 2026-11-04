---
tag: ERAPMK
kind: theorem
slug: union-bound
name: Union bound
aliases:
- Boole's inequality
area: foundations/probabilistic-analysis
level: intro
summary: For finitely or countably many events, P(A_1 or A_2 or ...) <= P(A_1) + P(A_2) + ..., with no assumption on how the events depend on each other.
prereqs: [probability-space, independence-of-events, indicator-random-variable]
see_also: [markov-inequality, chernoff-bound, high-probability-bounds, balls-into-bins, coupon-collector-problem, probabilistic-method, lovasz-local-lemma, power-of-two-choices]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Section 1.2, Axioms of Probability (the union bound); Section 5.2.1, The Balls-and-Bins Model (maximum load at most 3 ln n/ln ln n with probability at least 1 - 1/n); Section 5.4, The Poisson Approximation (the matching lower bound), and Section 5.4.1, Coupon Collector's Problem, Revisited
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Section 3.1, Occupancy Problems (the union bound and Theorem 3.1, maximum load at most e ln n/ln ln n); Appendix C, Proposition C.2 (the Boole-Bonferroni inequalities)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 1, The Basic Method, Section 1.1, The Probabilistic Method (Proposition 1.1.1, the lower bound for Ramsey numbers)
  - paper: doi:10.1007/3-540-49543-6_13
    title: Martin Raab and Angelika Steger, Balls into bins, a simple and tight analysis, RANDOM 1998, Lecture Notes in Computer Science 1518, pages 159 to 170
    locator: Theorem 1 (the maximum load is (1 + o(1)) ln n/ln ln n for m = n), and Section 1.1 (the earlier result of Gonnet, 1981)
  - url: "https://en.wikipedia.org/wiki/Boole%27s_inequality"
    locator: lead (the name), and section Bonferroni inequalities (Bonferroni 1936)
---

The union bound, also called Boole's inequality, says that the probability that at least one of a finite or countable family of events happens is at most the sum of their probabilities. It needs no [independence](/independence-of-events/) and no other knowledge of how the events interact. In the analysis of algorithms it is the standard way to pass from "each bad event is rare" to "no bad event happens": bound each event alone, often with a [Chernoff bound](/chernoff-bound/), then add. It gives the $O(\log n/\log\log n)$ bound on the largest bin in [balls into bins](/balls-into-bins/), and it is behind most bounds that hold [with high probability](/high-probability-bounds/).

## Statement

Let $(\Omega, \mathcal{F}, \Pr)$ be a [probability space](/probability-space/).

**Theorem (union bound).** For each finite or countably infinite sequence of events $A_1, A_2, \ldots$,
$$ \Pr\Big(\bigcup_i A_i\Big) \le \sum_i \Pr(A_i). $$
The events may depend on each other in any way. Equality holds if and only if $\sum_i \Pr(A_i) \le 1$ and $\Pr(A_i \cap A_j) = 0$ for all $i \ne j$, that is, the events are disjoint up to sets of probability 0.

**Theorem (Bonferroni lower bound).** For finitely many events $A_1, \ldots, A_m$,
$$ \Pr\Big(\bigcup_{i=1}^m A_i\Big) \ge \sum_{i=1}^m \Pr(A_i) - \sum_{1 \le i < j \le m} \Pr(A_i \cap A_j). $$

The two bounds are the first two truncations of the inclusion-exclusion formula. In general the truncations alternate: stopping after a sum over sets of odd size gives an upper bound, and after a sum over sets of even size a lower bound (Motwani and Raghavan, Appendix C, Proposition C.2). Only the first two are proved and used here.

## In plain words

Suppose a program can fail in several ways: a hash bucket overflows, a sample is unlucky, a pivot is bad. You can often bound the chance of each kind of failure on its own, but the failures may be linked in ways that are hard to work out. The union bound says that you do not need to work them out. The chance that anything at all goes wrong is at most the total of the separate chances.

The bound is exact when two failures never happen together. When failures overlap, the total counts the shared outcomes more than once, so it is too large. It becomes useless when the total passes one. So it works best for many failures that are each very rare, which is the usual case in the analysis of randomized algorithms.

## Proof

**Union bound.** Define $B_1 = A_1$ and $B_i = A_i \setminus (A_1 \cup \cdots \cup A_{i-1})$ for $i \ge 2$.

1. *The $B_i$ are disjoint.* For $j < i$, $B_i$ excludes $A_j$, and $B_j \subseteq A_j$.
2. *They have the same union.* Each $B_i \subseteq A_i$, so $\bigcup B_i \subseteq \bigcup A_i$. If $\omega \in \bigcup A_i$, let $i$ be the least index with $\omega \in A_i$; then $\omega \in B_i$.
3. *Add.* By countable additivity of $\Pr$ on the disjoint sets $B_i$, and by monotonicity ($B_i \subseteq A_i$ gives $\Pr(B_i) \le \Pr(A_i)$),
$$ \Pr\Big(\bigcup_i A_i\Big) = \Pr\Big(\bigcup_i B_i\Big) = \sum_i \Pr(B_i) \le \sum_i \Pr(A_i). \qquad \square $$

**When equality holds.** Equality in step 3 means $\sum_i (\Pr(A_i) - \Pr(B_i)) = 0$, a sum of nonnegative terms. The left side of the bound is at most 1, so equality forces $\sum_i \Pr(A_i) \le 1$; then the sum of differences is finite, and it is 0 exactly when $\Pr(A_i \setminus B_i) = 0$ for each $i$.

- If $\Pr(A_i \cap A_j) = 0$ for all $i \ne j$: $A_i \setminus B_i = \bigcup_{j < i} (A_i \cap A_j)$, so $\Pr(A_i \setminus B_i) \le \sum_{j<i} \Pr(A_i \cap A_j) = 0$ by the union bound itself. So equality holds.
- If equality holds: for $j < i$, $A_i \cap A_j \subseteq A_i \setminus B_i$, so $\Pr(A_i \cap A_j) = 0$. $\square$

**Bonferroni.** Let $I_i$ be the [indicator](/indicator-random-variable/) of $A_i$, and let $N = \sum_i I_i$ be the number of events that happen.

1. *A pointwise inequality.* We show $1[N \ge 1] \ge N - \binom{N}{2}$ for each outcome. The right side is $N(3 - N)/2$. If $N = 0$ both sides are 0. If $N \ge 1$, the inequality $N(3 - N)/2 \le 1$ is $(N - 1)(N - 2) \ge 0$, which holds for each integer $N$.
2. *Identify the terms.* $\binom{N}{2} = \sum_{i<j} I_i I_j$, because it counts the pairs of events that both happen, and $I_i I_j$ is the indicator of $A_i \cap A_j$. Also $1[N \ge 1]$ is the indicator of the union.
3. *Take expectations.* By [linearity of expectation](/linearity-of-expectation/), $\Pr(\bigcup A_i) \ge \sum_i \Pr(A_i) - \sum_{i<j} \Pr(A_i \cap A_j)$. $\square$

The same argument with $1[N \ge 1] \le N$ gives the finite union bound a second proof.

## Consequences

### The largest bin when n balls go into n bins

Throw $n$ balls into $n$ bins, each ball into a bin chosen uniformly at random, independently of the others. This is the model of [balls into bins](/balls-into-bins/), and of a [hash table with chaining](/separate-chaining/) with a random hash function and load factor 1. Let $L_j$ be the number of balls in bin $j$ and $M = \max_j L_j$.

**Claim.** For each integer $n \ge 3$, with $k = \lceil 3\ln n/\ln\ln n \rceil$,
$$ \Pr(M \ge k) \le \frac{n}{k!} \le \frac1n. $$

*Proof.* The union bound is used twice: once inside a bin, once over the bins.

1. *One bin.* Fix a bin $j$ and an integer $k \ge 1$. If $k > n$, then $L_j \ge k$ is impossible. Otherwise, $L_j \ge k$ holds exactly when some set $S$ of $k$ balls all land in bin $j$. For a fixed $S$ this has probability $n^{-k}$, by independence of the balls. There are $\binom{n}{k}$ sets $S$, so by the union bound
$$ \Pr(L_j \ge k) \le \binom{n}{k}\frac{1}{n^k} = \frac{n(n-1)\cdots(n-k+1)}{k!\,n^k} \le \frac{1}{k!}. $$
2. *All bins.* $\{M \ge k\} = \bigcup_{j=1}^n \{L_j \ge k\}$, so the union bound gives $\Pr(M \ge k) \le n/k!$.
3. *A bound on $k!$.* The series $e^k = \sum_{i \ge 0} k^i/i!$ has positive terms, so $e^k \ge k^k/k!$, that is $k! \ge (k/e)^k$. Hence $n/k! \le n\,e^{-h(k)}$ with $h(k) = k\ln(k/e)$.
4. *The choice of $k$.* Let $y = \ln\ln n$, which is positive for $n \ge 3$, and $k_0 = 3\ln n/y$. For $x = \ln n > 1$, $x/\ln x \ge e$, so $k_0 \ge 3e > 1$. The function $h$ is increasing on $[1, \infty)$, because $h'(k) = \ln k \ge 0$. So $h(k) \ge h(k_0)$, and
$$ h(k_0) = \frac{3\ln n}{y}\big(\ln 3 + \ln\ln n - \ln y - 1\big) = \frac{3\ln n}{y}\big(y - (\ln y + 1 - \ln 3)\big). $$
5. *An inequality in one variable.* For each $y > 0$, $\ln y + 1 - \ln 3 \le y/3$. Indeed $g(y) = y/3 - \ln y - 1 + \ln 3$ has $g'(y) = 1/3 - 1/y$, so $g$ is smallest at $y = 3$, where $g(3) = 0$.
6. *Conclude.* By steps 4 and 5, $h(k) \ge \frac{3\ln n}{y}\cdot\frac{2y}{3} = 2\ln n$. So $\Pr(M \ge k) \le n\,e^{-2\ln n} = 1/n$. $\square$

The table gives the numbers. "Least $k$ for $n/k!$" is the least $k$ with $n/k! \le 1/n$. The exact distribution of $M$ comes from the formula $\Pr(M \le m) = \frac{n!}{n^n}[x^n]\big(\sum_{j=0}^m x^j/j!\big)^n$, which counts the assignments with all loads at most $m$.

| $n$ | $\frac{\ln n}{\ln\ln n}$ | $\frac{3\ln n}{\ln\ln n}$ | $k$ | $n/k!$ | least $k$ for $n/k!$ | least $k$ with exact $\Pr(M \ge k) \le 1/n$ | most likely $M$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $10^3$ | 3.57 | 10.72 | 11 | $2.51 \times 10^{-5}$ | 10 | 10 | 5 (probability 0.530) |
| $10^6$ | 5.26 | 15.78 | 16 | $4.78 \times 10^{-8}$ | 15 | 15 | 9 (probability 0.570) |

The union bound loses almost nothing in the far tail. For $n = 10^3$ the next table compares $n/k!$, the union bound over bins with the exact tail of one bin, $n\Pr(L_1 \ge k)$, the Bonferroni lower bound $n\Pr(L_1 \ge k) - \binom n2\Pr(L_1 \ge k, L_2 \ge k)$, and the exact $\Pr(M \ge k)$.

| $k$ | $n/k!$ | $n\Pr(L_1 \ge k)$ | Bonferroni | exact $\Pr(M \ge k)$ |
| --- | --- | --- | --- | --- |
| 6 | 1.389 | 0.588 | 0.420 | 0.447 |
| 7 | 0.198 | 0.0820 | 0.0787 | 0.0788 |
| 8 | 0.0248 | 0.01003 | 0.009984 | 0.009984 |
| 9 | 0.00276 | 0.001094 | 0.001093 | 0.001093 |
| 10 | 0.000276 | 0.0001074 | 0.0001074 | 0.0001074 |
| 12 | $2.09 \times 10^{-6}$ | $7.87 \times 10^{-7}$ | $7.87 \times 10^{-7}$ | $7.87 \times 10^{-7}$ |

When the events $\{L_j \ge k\}$ are rare, they rarely happen together, and the union bound and the Bonferroni bound squeeze the exact value. The factor of about $2.5$ between $n/k!$ and $n\Pr(L_1 \ge k)$ comes from step 1, which drops the probability, about $e^{-1}$, that the other balls miss the bin. The real slack of the claim is elsewhere: the threshold $3\ln n/\ln\ln n$ is 2.1 times the most likely value of $M$ at $n = 10^3$ and 1.75 times at $n = 10^6$. The constant 3 is a convenience of the proof. Raab and Steger (1998), Theorem 1, show that $M = (1 + o(1))\ln n/\ln\ln n$ with probability $1 - o(1)$, and Mitzenmacher and Upfal, Section 5.4, prove $M \ge \ln n/\ln\ln n$ with probability at least $1 - 1/n$ for $n$ large enough. The lower-order terms are large: at $n = 10^6$ the most likely value 9 is 1.7 times $\ln n/\ln\ln n$. With two random choices per ball the maximum drops to $\ln\ln n/\ln 2 + O(1)$, see the [power of two choices](/power-of-two-choices/).

### The coupon collector

Draw coupons uniformly at random, with replacement, from $n$ types, and let $T$ be the number of draws until each type is seen (the [coupon collector problem](/coupon-collector-problem/)). After $r$ draws, type $i$ is missing with probability $(1 - 1/n)^r \le e^{-r/n}$. With $r = \lceil n\ln n + cn \rceil$ for a constant $c$, the union bound over the $n$ types gives
$$ \Pr(T > r) \le n\Big(1 - \frac1n\Big)^r \le n\,e^{-\ln n - c} = e^{-c}. $$
For $n = 100$, where $\mathbb{E}[T] = nH_n = 518.7$, and the exact value from inclusion-exclusion, $\Pr(T > r) = \sum_{j=1}^{n} (-1)^{j+1}\binom{n}{j}(1 - j/n)^r$:

| $c$ | $r$ | $n(1 - 1/n)^r$ | $e^{-c}$ | exact $\Pr(T > r)$ |
| --- | --- | --- | --- | --- |
| 0 | 461 | 0.972 | 1 | 0.632 |
| 1 | 561 | 0.356 | 0.368 | 0.302 |
| 2 | 661 | 0.130 | 0.135 | 0.123 |
| 3 | 761 | 0.0477 | 0.0498 | 0.0467 |
| 5 | 961 | 0.00639 | 0.00674 | 0.00637 |

The bound is close for $c \ge 2$ and loose near $c = 0$, where several types are often missing at the same time. As $n \to \infty$, $\Pr(T > n\ln n + cn) \to 1 - e^{-e^{-c}}$ (Mitzenmacher and Upfal, Section 5.4.1), and $1 - e^{-e^{-c}} \le e^{-c}$, with ratio tending to 1 as $c$ grows. With $r = (1 + a)\,n\ln n$ the same computation gives $\Pr(T > r) \le n^{-a}$.

### Existence proofs

The union bound is the simplest form of the [probabilistic method](/probabilistic-method/): if a random object has bad events whose probabilities sum to less than 1, then with positive probability none of them happens, so a good object exists. Color each edge of the complete graph on $n$ vertices red or blue at random. A fixed set of $k$ vertices spans a single-colored complete graph with probability $2^{1 - \binom k2}$. If $\binom nk 2^{1 - \binom k2} < 1$, the union bound over the $\binom nk$ sets shows that some coloring has no single-colored $K_k$, so the [Ramsey number](/ramsey-theorem/) $R(k, k)$ exceeds $n$. For $k \ge 3$ the condition holds at $n = \lfloor 2^{k/2} \rfloor$ (Alon and Spencer, Proposition 1.1.1). For $k = 10$ the largest $n$ that satisfies it is 100, so $R(10, 10) > 100$, against $2^{5} = 32$ from the closed form. When the bad events are rare and each depends on few others, the [Lovász local lemma](/lovasz-local-lemma/) gives existence where the union bound fails.

## Tightness

The bound is exact for events that are disjoint up to probability 0, as proved above, and no bound that uses only the numbers $\Pr(A_i)$ can be smaller: for any numbers $p_1, \ldots, p_m \ge 0$ with $\sum p_i \le 1$, disjoint events with these probabilities exist in the unit interval. The bound is loose when events overlap. For $m$ [independent](/independence-of-events/) events of probability $p$ each, the union has probability $1 - (1 - p)^m$:

| $m$ | $p$ | union bound $mp$ | exact $1 - (1 - p)^m$ | Bonferroni $mp - \binom m2 p^2$ |
| --- | --- | --- | --- | --- |
| 10 | 0.01 | 0.1 | 0.0956 | 0.0955 |
| 1000 | $10^{-4}$ | 0.1 | 0.0952 | 0.0950 |
| 1000 | $10^{-3}$ | 1 | 0.632 | 0.500 |
| 100 | 0.05 | 5 | 0.994 | $-7.4$ |

When $mp$ is small the union bound is within a factor $1 + O(mp)$ of the truth. When $mp \ge 1$ it says nothing, and the Bonferroni bound can even be negative. For $m$ copies of one event, the union has probability $p$ and the bound is $mp$, which is wrong by the factor $m$.

### Pitfalls

- **Countable, not uncountable.** For a uniform point $U$ in $[0, 1]$, each event $\{U = x\}$ has probability 0, but the union over all $x$ is the whole space. The bound holds only for finitely or countably many events.
- **Too many events.** The bound is useful only if the sum is small. A union over the $2^n$ subsets of the input, or over all $n!$ orders, needs each event to have probability far below $2^{-n}$ or $1/n!$. A union over polynomially many events with probability $n^{-c}$ each keeps a polynomially small failure probability, which is why [high-probability bounds](/high-probability-bounds/) compose well.
- **Paying for the union.** A union over $n$ events costs a factor $n$, so each event must be bounded by about $1/n^2$ to end with $1/n$. In the max load proof this is the factor 2 in $2\ln n$, and it is the reason for the $\log n$ terms in many bounds.
- **Heavy overlap.** Events that tend to happen together are counted many times. With 1000 balls in 1000 bins, each bin is empty with probability $(1 - 1/1000)^{1000} = 0.368$, so the union bound for "some bin is empty" is 368, a useless number. Here the right tools are the expected count of empty bins, which is 368, and [Chebyshev's inequality](/chebyshev-inequality/) or a [concentration bound](/concentration-of-measure/), which show that the number of empty bins is close to 368 with high probability.
- **The bound is an upper bound only.** To show that some event does happen with high probability you need a lower bound, such as Bonferroni or the second moment method.

## History

The inequality is named after George Boole. The lower bounds from truncating inclusion-exclusion are named after Carlo Emilio Bonferroni, who studied them in 1936. The bound on the maximum load is classical in the analysis of hashing: Raab and Steger, Section 1.1, credit Gonnet (1981) with the expected maximum load for $m = n$, and they give a short proof by the first and second moment methods. The union bound proof with the constant $e$ in place of 3 is Theorem 3.1 of Motwani and Raghavan, and the form with 3 is in Mitzenmacher and Upfal, Section 5.2.1.

## References
