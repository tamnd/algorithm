---
tag: FC22KF
kind: technique
slug: inverse-transform-sampling
name: Inverse transform sampling
aliases:
- inversion method
- inverse CDF method
- quantile transform
area: randomized/sampling
level: core
summary: Sample X by applying the inverse CDF to a uniform random number.
prereqs: [uniform-distribution, probability-distribution, binary-search]
see_also: [rejection-sampling, random-variate-generation, alias-method, weighted-sampling, box-muller-transform, bernoulli-sampling, quasi-monte-carlo-integration, quantile]
sources:
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter II, Section 2 (the inversion method), and Chapter III, Section 2 (discrete inversion, with guide tables)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.1 (numerical distributions)
  - url: https://artowen.su.domains/mc/
    title: Art B. Owen, Monte Carlo theory, methods and examples, 2013
    locator: Chapter 4 (non-uniform random variables), the section on inversion
---

Inverse transform sampling turns a uniform random number $U$ on $(0, 1)$ into a variate with any given distribution function $F$: return $X = F^{-1}(U)$, where $F^{-1}(u) = \inf\{x : F(x) \ge u\}$ is the generalized inverse. The key fact is $F^{-1}(u) \le x \iff u \le F(x)$, so $\Pr[X \le x] = \Pr[U \le F(x)] = F(x)$. It works for every distribution on the real line, continuous, discrete or mixed. For a discrete law it becomes a search: find the first index whose prefix sum passes $U$. It uses exactly one uniform per variate and the output is a monotone function of $U$, which makes it the base case of [random variate generation](/random-variate-generation/) and the natural partner of [quasi-Monte Carlo](/quasi-monte-carlo-integration/) methods.

## In plain words

Line up all possible outcomes from smallest to largest. Give each one a piece of the stick from 0 to 1, as long as its probability. Then drop a random point on the stick, and return the outcome whose piece it hits.

That is all. Outcomes with big pieces are hit more often, in exact proportion to their length. For a continuous law, like a waiting time, the pieces are infinitely thin, and the rule becomes a formula: find the value at which the chance of being at most that value equals the random point.

The method needs a way to go from a point on the stick back to the outcome. For some laws this is one formula. For others it is a search in a table.

## When it applies

- The inverse $F^{-1}$ has a closed form: the exponential, Weibull, Cauchy, logistic, Pareto, Gumbel and geometric laws, and many others.
- The law is discrete with a finite or easily listed support. Then $F^{-1}$ is a search in the prefix sums.
- A good numerical approximation of $F^{-1}$ exists, as for the normal law.
- The application needs a monotone map from uniforms to variates: common random numbers, antithetic variates, stratified or Latin hypercube designs, quasi-Monte Carlo, or a truncated law $F$ restricted to an interval $[F(a), F(b)]$ of $u$.

It does not apply well when $F^{-1}$ is costly and has no good approximation, as for many densities known only up to a constant. Then [rejection sampling](/rejection-sampling/) or the [ratio-of-uniforms](/ratio-of-uniforms/) method fits better.

## The template

Notation: $F$ is a distribution function on $\mathbb{R}$: non-decreasing, right-continuous, with limits 0 at $-\infty$ and 1 at $+\infty$. The hole to fill is $F^{-1}$, or for a discrete law the weights. For the discrete form, $w_1, \ldots, w_n \ge 0$ are integer weights with total $W > 0$, and $P_i = w_1 + \dots + w_i$.

```pseudo id=main
INVERSION(F)
L1  U ← a uniform real in (0, 1)
L2  return F⁻¹(U) = inf{x : F(x) ≥ U}

DISCRETE-INVERSION(P[1..n])                 ▷ P = prefix sums of integer weights, W = P[n]
L3  t ← a uniform integer in {0, …, W − 1}
L4  return the least i with P[i] > t        ▷ binary search
```

The discrete form is the continuous one with $U = (t + 1)/W$ in disguise: $P_i > t \iff (t+1)/W \le P_i/W = F(i)$. It uses an integer draw, so it is exact with integer arithmetic. A uniform integer in $\{0, \ldots, W - 1\}$ from random bits needs rejection when $W$ is not a power of 2.

### Example

**Discrete.** Weights $(1, 0, 2, 3, 2)$, so $W = 8$ and the prefix sums are $(1, 1, 3, 6, 8)$. The eight values of $t$ give:

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| index | 1 | 3 | 3 | 4 | 4 | 4 | 5 | 5 |

Index 1 appears once, index 2 never, index 3 twice, index 4 three times and index 5 twice: exactly the weights. Index 2 has weight 0, and the strict test $P_i > t$ skips it.

**Exponential.** $F(x) = 1 - e^{-\lambda x}$ for $x \ge 0$, so $F^{-1}(u) = -\ln(1 - u)/\lambda$. With $\lambda = 2$ and $U = 0.5$, $X = \ln 2 / 2 \approx 0.3466$, the median. Since $1 - U$ is also uniform, $-\ln(U)/\lambda$ works as well.

**Cauchy.** $F(x) = \frac{1}{2} + \frac{1}{\pi}\arctan x$, so $F^{-1}(u) = \tan\bigl(\pi(u - \frac{1}{2})\bigr)$.

### Why it is correct

**Lemma.** For $0 < u < 1$ and real $x$: $F^{-1}(u) \le x \iff u \le F(x)$.

*Proof.* Let $S_u = \{y : F(y) \ge u\}$. It is not empty, because $F(y) \to 1 > u$, and it is bounded below, because $F(y) \to 0 < u$. So $F^{-1}(u) = \inf S_u$ is a real number. Since $F$ is non-decreasing, $S_u$ is an interval that goes to $+\infty$. Since $F$ is right-continuous, the infimum is in $S_u$: $F(F^{-1}(u)) \ge u$.

If $u \le F(x)$, then $x \in S_u$, so $F^{-1}(u) \le x$. If $F^{-1}(u) \le x$, then $F(x) \ge F(F^{-1}(u)) \ge u$. $\square$

**Theorem.** If $U$ is uniform on $(0, 1)$, then $X = F^{-1}(U)$ has distribution function $F$.

*Proof.* By the lemma, $\Pr[X \le x] = \Pr[U \le F(x)] = F(x)$ for every $x$, since $0 \le F(x) \le 1$. $\blacksquare$

The theorem needs no density and no continuity: jumps of $F$ become atoms of $X$, and flat parts of $F$ become values that $X$ never takes. For the discrete form, the lemma with $u = (t + 1)/W$ shows that $i$ is returned for exactly $w_i$ of the $W$ values of $t$, so $\Pr[\text{index} = i] = w_i/W$ exactly.

The converse, the probability integral transform, holds when $F$ is continuous: then $F(X)$ is uniform on $(0, 1)$.

### Cost

- One uniform per variate, and one evaluation of $F^{-1}$.
- Discrete law with $n$ values: $O(n)$ setup for the prefix sums, then $O(\log n)$ per variate by [binary search](/binary-search/). A sequential search from the most likely value costs $1 + \mathbb{E}[\text{position}]$ comparisons.
- With a guide table of $n$ entries that maps $\lfloor nU \rfloor$ to a starting index, the expected search cost is $O(1)$ after $O(n)$ setup (Devroye, Section III.2).

## Classic examples

- **Exponential and geometric variates.** $-\ln(U)/\lambda$, and $\lfloor \ln U / \ln(1 - p) \rfloor$ for the [geometric distribution](/geometric-distribution/). [Bernoulli sampling](/bernoulli-sampling/) uses the geometric form to skip over items.
- **The radius in the [Box-Muller transform](/box-muller-transform/).** $R^2 = -2\ln U_1$ is inversion for the exponential law of $R^2$.
- **[Weighted sampling](/weighted-sampling/) with replacement.** Prefix sums and binary search. The [alias method](/alias-method/) is the $O(1)$ alternative, and a [Fenwick tree](/fenwick-tree/) of the weights allows updates in $O(\log n)$.
- **Normal variates by inversion.** $\Phi^{-1}(U)$ with an accurate rational approximation of the normal quantile function, used where the monotone map matters.
- **Truncated laws.** For $X$ conditioned on $a < X \le b$, draw $U$ uniform on $(F(a), F(b))$ and return $F^{-1}(U)$. No sample is wasted.

## Variations

- **Numerical inversion.** Solve $F(x) = U$ by [bisection](/bisection-method/) or Newton's method when $F$ is known but $F^{-1}$ is not. The cost per variate is then a root search.
- **Inversion of the survival function.** Use $\bar F(x) = 1 - F(x)$ and $X = \bar F^{-1}(U)$ when $F$ is close to 1 in the region of interest. This keeps the precision in the upper tail.
- **Discrete inversion with random bits.** Generate $U$ one bit at a time and stop as soon as the interval of possible $U$ values lies inside one piece. This is the entropy-optimal idea of Knuth and Yao: the expected number of bits is less than the entropy plus 2.
- **[Rejection sampling](/rejection-sampling/)** replaces inversion when $F^{-1}$ is hard, at the cost of a random number of uniforms.

## Pitfalls

- **$U = 0$ or $U = 1$.** Many generators return values in $[0, 1)$, and $F^{-1}(0) = -\infty$ for unbounded laws. Use $1 - U$ or reject 0, depending on the formula.
- **Strict and weak tests.** In the discrete search, use $P_i > t$ for an integer $t \in \{0, \ldots, W-1\}$, or $P_i \ge u$ for a real $u \in (0, 1]$. Mixing the two forms is off by one: $P_i \ge t$ gives index 1 one extra value of $t$ and the last index one value less.
- **Floating point.** With 53-bit uniforms, $U$ takes only multiples of $2^{-53}$, so the tails are cut: $-\ln(1 - U)$ never exceeds $53 \ln 2 \approx 36.7$. With float prefix sums, each probability is wrong by up to a few units in the last place, and the last prefix sum may not be exactly 1, so the search must handle $U \ge P_n$. The method is exact only in exact arithmetic, or with integer weights and integer draws as above.
- **Loss of precision near 1.** Computing $F^{-1}(1 - \varepsilon)$ as written loses digits when $F$ is near 1. Use the survival function.
- **Slow $F^{-1}$.** A numerical root search for each variate is often slower than a rejection method. Measure.

## Exercises

1. Show that if $F$ is continuous, $F(X)$ is uniform on $(0, 1)$, and give a discrete $F$ for which it is not.
2. Derive the inversion formulas for the Weibull law $F(x) = 1 - e^{-(x/\lambda)^k}$ and the Pareto law $F(x) = 1 - (x_m/x)^\alpha$ for $x \ge x_m$.
3. Prove that sequential search from the most likely value down uses the least expected number of comparisons among all orders.
4. For weights with total $W = 10$, how many random bits does the integer draw in line L3 use in expectation with the simple rejection method that draws 4 bits and retries when the value is at least 10?

## References
