---
tag: 9RJGHX
kind: technique
slug: pessimistic-estimators
name: Method of pessimistic estimators
aliases:
- pessimistic estimator method
- pessimistic estimator
- Raghavan's method of pessimistic estimators
area: randomized/derandomization
level: advanced
summary: Extends conditional expectations by replacing an intractable expectation with a computable upper bound that is preserved at each step.
prereqs: [method-of-conditional-expectations, chernoff-bound, moment-generating-function, union-bound]
see_also: [randomized-rounding, discrepancy, set-cover, sample-space-reduction, k-wise-independence, probabilistic-method]
sources:
  - paper: doi:10.1016/0022-0000(88)90003-7
    title: Prabhakar Raghavan, Probabilistic construction of deterministic algorithms, approximating packing integer programs, Journal of Computer and System Sciences 37(2), 1988
    locator: pages 130 to 143 (the definition of pessimistic estimators and their use for packing integer programs)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 16, Section 16.1 (the method of conditional probabilities)
  - book: isbn:9780898713251
    title: Joel Spencer, Ten Lectures on the Probabilistic Method, second edition, SIAM, 1994
    locator: Lecture 4, Large deviations and nonprobabilistic algorithms (pages 29 to 35)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4 (the Chernoff bound and its set balancing application)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 5 (the probabilistic method, with the method of conditional probabilities)
---

The method of pessimistic estimators, named by Raghavan (1988), derandomizes a probabilistic argument when the exact conditional probabilities of the [method of conditional expectations](/method-of-conditional-expectations/) cannot be computed. It replaces the conditional failure probability by an upper bound $U$ that can be computed, that starts below 1, and that some choice at each step does not increase. The bound usually comes from the proof itself: a [union bound](/union-bound/) over [Chernoff bounds](/chernoff-bound/), each written with its [moment generating function](/moment-generating-function/). The standard example is set balancing, where the method finds signs with every row sum below $\sqrt{2n \ln(2m)}$ in absolute value.

## In plain words

Sometimes the chance that a random choice fails is too hard to compute exactly, even though a proof shows that it is small. The proof gives a formula that is always at least the chance of failure and that is easy to compute. Use that formula as a guide.

Fix the random choices one at a time. Before each choice, the formula is an average of its values after the possible choices. So one choice keeps the formula as small as before. Take that choice. The formula started below 1, and it stays below 1. At the end nothing is random, and the formula is still at least the chance of failure, which is now 0 or 1. Since it is below 1, the chance is 0, and the fixed choices do not fail.

## When it applies

Notation. $X = (X_1, \ldots, X_n)$ are independent random choices, each from a small set of values. $\mathcal{B}$ is the bad event. A prefix $x_{\le i} = (x_1, \ldots, x_i)$ is a list of fixed values for the first $i$ choices.

A pessimistic estimator for $\mathcal{B}$ is a list of functions $U_0, U_1, \ldots, U_n$, with $U_i$ defined on prefixes of length $i$, such that:

1. **Upper bound.** $\Pr[\mathcal{B} \mid X_{\le i} = x_{\le i}] \le U_i(x_{\le i})$ for every prefix.
2. **Start.** $U_0 < 1$.
3. **Averaging.** For every prefix $x_{\le i-1}$, some value $v$ gives $U_i(x_{\le i-1}, v) \le U_{i-1}(x_{\le i-1})$. In most uses this holds because $U_{i-1}$ is at most the average of $U_i(x_{\le i-1}, v)$ over $v$ with the distribution of $X_i$.
4. **Efficiency.** Each $U_i$ can be computed in polynomial time.

Raghavan's definition asks for the same three properties: an upper bound on the conditional failure probability, a start below 1, and a value that does not increase under the right choice. Use the method when the analysis of a randomized algorithm ends with a union bound over many events, each bounded by Markov's inequality applied to some function of the choices, such as $e^{\lambda S}$. The bound of each event is then an expectation of a product of independent factors, so it can be computed for any prefix, and the averaging property holds with equality.

Use the plain [method of conditional expectations](/method-of-conditional-expectations/) instead when the exact conditional value is easy, as for max cut. Use [sample space reduction](/sample-space-reduction/) when the analysis needs only [k-wise independence](/k-wise-independence/) for small $k$.

## The template

```pseudo id=main
PESSIMISTIC-ESTIMATOR(U, n, S)          ▷ U = (U_0, …, U_n) a pessimistic estimator, U_0 < 1
L1  for i ← 1 to n do
L2      choose v in S with the least value U_i(x_1, …, x_{i−1}, v)
L3      x_i ← v
L4  return x = (x_1, …, x_n)            ▷ x is not in the bad event
```

**Claim.** The returned $x$ is not in $\mathcal{B}$.

*Proof.* By line L2 and the averaging property, $U_i(x_{\le i}) \le U_{i-1}(x_{\le i-1})$ for each $i$, so $U_n(x) \le U_0 < 1$. After step $n$ every choice is fixed, so $\Pr[\mathcal{B} \mid X = x]$ is 1 if $x \in \mathcal{B}$ and 0 otherwise. By the upper bound property this number is at most $U_n(x) < 1$, so it is 0. $\square$

The cost is $n |S|$ evaluations of $U$. If $U$ is a sum of $m$ terms and each step changes a term by a factor, an incremental update costs $O(m)$ per step.

## Classic examples

### Set balancing with Chernoff bounds

Let $A$ be an $m \times n$ matrix with entries 0 and 1. Choose signs $b \in \{-1, +1\}^n$ and let $s_i = \sum_j a_{ij} b_j$ be the $i$-th row sum. With uniform random signs, the Chernoff bound for sums of $\pm 1$ variables, $\Pr[|s_i| \ge t] \le 2 e^{-t^2/(2n)}$, and the union bound over the $m$ rows show that $t = \sqrt{2n \ln(2m)}$ gives $\Pr[\max_i |s_i| \ge t] < 1$. The exact conditional probability of "some row is large" is a sum over $2^{n-i}$ completions, so the plain method of conditional expectations does not apply. The Chernoff proof gives the estimator.

Fix $\lambda = t/n$. After the first $i$ signs are fixed, let $s_i'$ be the sum of $a_{ij} b_j$ over the fixed $j$, and let $r_i$ be the number of $j$ not yet fixed with $a_{ij} = 1$. Define

$$U = \sum_{i=1}^{m} e^{-\lambda t} \left( e^{\lambda s_i'} + e^{-\lambda s_i'} \right) (\cosh \lambda)^{r_i}.$$

- **Upper bound.** By Markov's inequality on $e^{\lambda s_i}$ and $e^{-\lambda s_i}$, $\Pr[|s_i| \ge t \mid \text{prefix}] \le e^{-\lambda t}\,\mathrm{E}[e^{\lambda s_i} + e^{-\lambda s_i} \mid \text{prefix}]$, and the conditional expectation of $e^{\lambda b_j}$ for a free sign is $\cosh \lambda$. So each term bounds the conditional probability of its row, and the union bound makes $U$ an upper bound on the conditional failure probability.
- **Averaging.** Fixing a free sign $b_j$ to $+1$ or $-1$ replaces a factor $\cosh \lambda$ by $e^{\pm\lambda}$ in each row with $a_{ij} = 1$. Since $\cosh \lambda$ is the average of $e^{\lambda}$ and $e^{-\lambda}$, $U$ is exactly the average of its two extensions, so the smaller one is at most $U$.
- **Start.** All $s_i' = 0$ and $r_i \le n$. With $\cosh \lambda < e^{\lambda^2/2}$ for $\lambda > 0$, $U_0 < 2m\, e^{-\lambda t + \lambda^2 n/2} = 2m\, e^{-t^2/(2n)} = 1$.
- **End.** All $r_i = 0$, so each term is at least $e^{\lambda(|s_i| - t)}$, which is at least 1 when $|s_i| \ge t$. Since the final $U$ is below 1, every $|s_i| < t$.

So the deterministic algorithm finds signs with $\max_i |s_i| < \sqrt{2n \ln(2m)}$ in $O(mn)$ arithmetic operations, by updating each row term when its sign is fixed. Equal values of $U$ need a tie rule; take $+1$.

Example with $m = n = 10$, $t = \sqrt{20 \ln 20} \approx 7.74$, and rows

`0011001100`, `1110001000`, `0101111110`, `1000101111`, `1110101010`, `0110011010`, `1001110001`, `1100100000`, `1110011101`, `1110110111`.

Fixing $b_1, \ldots, b_{10}$ in order with the rule of line L2 gives $U$ values (rounded) 0.2448 at the start, then 0.2448, 0.1897, 0.1814, 0.1811, 0.1806, 0.1540, 0.1373, 0.1132, 0.1035, 0.0962. The signs are $b = (+,-,+,-,+,-,-,+,-,-)$, and the row sums are $0, 0, -3, 0, 0, -3, -1, 1, -1, 0$, so the largest $|s_i|$ is 3. The guarantee is only $|s_i| \le 7$ here, and the best signing for this matrix has largest row sum 1. For large $m$ and $n$ the bound $\sqrt{2n \ln(2m)}$ is the useful part. When $m = n$, Spencer's "six standard deviations" theorem gives the better bound $O(\sqrt{n})$, by a different argument (see [discrepancy](/discrepancy/)).

### Packing integer programs (Raghavan 1988)

The problem is to choose 0 or 1 values for variables, subject to packing constraints $\sum_j a_{ij} x_j \le c_i$ with nonnegative $a_{ij}$. [Randomized rounding](/randomized-rounding/) solves the [LP relaxation](/lp-relaxation/) and sets $x_j = 1$ with probability equal to its fractional value, maybe scaled down. A Chernoff bound for each constraint and the union bound show that all constraints are nearly satisfied with positive probability. Raghavan showed that the Chernoff proof, written with moment generating functions as above, is a pessimistic estimator, which gives a deterministic algorithm with the same guarantee. He used it for packing problems and for routing with low congestion.

### Set cover and greedy algorithms

For [set cover](/set-cover/), rounding the LP solution with $\ln n$ times scaling, followed by a pessimistic estimator for "some element is not covered" and for the size of the cover, gives a deterministic $O(\log n)$ approximation. Young (SODA 1995) observed that some such estimators do not need the LP solution at all ("oblivious rounding"). The resulting algorithm is close to the classic greedy algorithm.

## Variations

- **Several estimators at once.** If the good event needs a small cost and few failures, add the estimator of the failure probability and a scaled estimator of the cost, so that the sum starts below 1. Each step keeps the sum from growing.
- **Non-binary choices.** The same template works with choices from any finite set, or with a non-uniform distribution: the averaging property must hold for the actual distribution of $X_i$.
- **Estimators from moments.** If the proof uses a $k$-th moment bound in place of an exponential one, the estimator is a polynomial in the partial sums, and its conditional expectation can be computed when $k$ is a constant.
- **Parallel versions.** If the estimator needs only [k-wise independence](/k-wise-independence/), the choices can be the seed of a small sample space; fixing the $O(\log n)$ seed bits one by one gives NC algorithms (see [sample space reduction](/sample-space-reduction/)).

## Pitfalls

- **An upper bound is not enough.** The function must also satisfy the averaging property. A loose bound such as $\min(1, \cdot)$ of a valid estimator can lose it, and then a step can raise the value above 1.
- **The start must be strictly below 1.** If the union bound gives exactly 1, the end value can be 1 and the argument proves nothing. Increase $t$ slightly.
- **Real arithmetic.** The terms $e^{\lambda s}$ are real numbers. Rounding errors can break the inequality $U_i \le U_{i-1}$ when the two choices are nearly equal. Any choice with a value below 1 at the end is safe, so a small margin at the start (such as $U_0 \le 1/2$) protects against rounding.
- **The guarantee is the bound of the proof.** The algorithm finds an object as good as the probabilistic bound, not an optimal one. In the example above the guarantee is 7 and the optimum is 1.

## Exercises

1. Prove $\cosh \lambda \le e^{\lambda^2/2}$ by comparing the power series term by term.
2. Write a pessimistic estimator for the event "some row of $A$ has $s_i \ge t$" (one side only), and find the value of $t$ it gives.
3. In set balancing, replace the estimator by the sum over rows of $\Pr[|s_i| \ge t \mid \text{prefix}]$, computed exactly. Show that it is also a pessimistic estimator, and say why it is slower to compute.
4. Use a pessimistic estimator to find, in polynomial time, a 2-colouring of the vertices of a hypergraph with $m$ edges of size $n$ in which every edge has at most $n/2 + \sqrt{n \ln(2m)/2}$ vertices of each colour.

## References
