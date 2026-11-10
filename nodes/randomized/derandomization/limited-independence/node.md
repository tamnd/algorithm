---
tag: MDBYDY
kind: concept
slug: limited-independence
name: Limited independence
aliases:
- bounded independence
- tail bounds for k-wise independent variables
area: randomized/derandomization
level: core
summary: Using random variables with only bounded independence to get the concentration bounds of full independence at much lower randomness cost.
prereqs: [k-wise-independence, chebyshev-inequality, variance, markov-inequality]
see_also: [pairwise-independence, chernoff-bound, sample-space-reduction, k-independent-hashing, median-trick, randomness-amplification, ams-sketch, linear-probing]
sources:
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 3, Section 3.5 (pairwise independence, with the Chebyshev bound for pairwise independent samples)
  - paper: doi:10.1016/0885-064x(89)90015-0
    title: Benny Chor and Oded Goldreich, On the power of two-point based sampling, Journal of Complexity 5(1), 1989
    locator: pages 96 to 106 (error reduction with pairwise independent samples)
  - paper: doi:10.1109/sfcs.1994.365687
    title: Mihir Bellare and John Rompel, Randomness-efficient oblivious sampling, FOCS 1994
    locator: pages 276 to 287 (the tail inequality for sums of k-wise independent variables, Section 2)
  - paper: doi:10.1137/s089548019223872x
    title: Jeanette P. Schmidt, Alan Siegel and Aravind Srinivasan, Chernoff-Hoeffding bounds for applications with limited independence, SIAM Journal on Discrete Mathematics 8(2), 1995
    locator: pages 223 to 250 (Chernoff-Hoeffding type bounds from k-wise independence)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 16, Section 16.2 (d-wise independent random variables in small sample spaces)
---

Limited independence is the idea that many randomized algorithms do not need fully independent random choices: [k-wise independence](/k-wise-independence/) for a small $k$ already gives the tail bounds that their analysis uses. Pairwise independence gives the [Chebyshev bound](/chebyshev-inequality/), and $k$-wise independence gives a bound with the $k$-th moment, which decays like a polynomial of degree $k/2$ in the deviation. Since $k$-wise independent variables come from sample spaces with about $n^{k/2}$ points, an algorithm that needs only them uses $O(k \log n)$ random bits and can be derandomized by trying every point. The cost is a weaker tail: exponential bounds such as the [Chernoff bound](/chernoff-bound/) need independence of order the exponent.

## In plain words

Fully random choices are expensive: each coin flip is one more random bit, and checking all outcomes takes time that doubles with each flip. Most proofs, though, only ask questions about a few choices at a time. If any two choices look independent, the spread of their sum is the same as with full independence, and so is every bound that uses only that spread.

So a small set of possible outcomes, built so that every few choices look independent, can stand in for the full random choice. The price is in the rare cases: with few independent choices, large errors are less rare than with full independence. If an analysis needs very small error, it needs more independence, or more repetitions.

## The idea

Notation. $X_1, \ldots, X_n$ are random variables with values in $[0, 1]$, $S = \sum_i X_i$, $\mu = \mathrm{E}[S]$, and $a > 0$ is the deviation. $\Pr$, $\mathrm{E}$ and $\mathrm{Var}$ are probability, expectation and [variance](/variance/) over one random point of the sample space.

### Pairwise independence gives Chebyshev

**Claim.** If $X_1, \ldots, X_n$ are pairwise independent, then $\mathrm{Var}[S] = \sum_i \mathrm{Var}[X_i]$, so

$$\Pr\big[|S - \mu| \ge a\big] \le \frac{\sum_i \mathrm{Var}[X_i]}{a^2} \le \frac{\mu}{a^2}.$$

*Proof.* $\mathrm{Var}[S] = \sum_i \mathrm{Var}[X_i] + \sum_{i \ne j} \mathrm{Cov}[X_i, X_j]$. For $i \ne j$, $X_i$ and $X_j$ are independent, so $\mathrm{E}[X_i X_j] = \mathrm{E}[X_i]\,\mathrm{E}[X_j]$ and the covariance is 0. Chebyshev's inequality, which is [Markov's inequality](/markov-inequality/) applied to $(S - \mu)^2$, gives the first bound. For values in $[0, 1]$, $\mathrm{Var}[X_i] \le \mathrm{E}[X_i^2] \le \mathrm{E}[X_i]$, which gives the second. $\square$

The only thing the proof uses is that the second moment of $S$ is the same as under full independence. For an estimate of a mean $p$ by the average of $t$ pairwise independent samples, the error probability at deviation $\varepsilon$ is at most $p(1-p)/(t \varepsilon^2)$. This is the basis of two-point sampling (Chor and Goldreich 1989): $t$ pairwise independent samples from the polynomial construction over a field of size $2^m \ge t$ cost $2m$ random bits, in place of $t m$.

### Higher moments

If the $X_i$ are $k$-wise independent for an even $k$, then $\mathrm{E}[(S - \mu)^k]$ is the same as under full independence, because the expansion of $(S - \mu)^k$ is a sum of products of at most $k$ of the variables. Markov's inequality on $(S - \mu)^k$ gives

$$\Pr\big[|S - \mu| \ge a\big] \le \frac{\mathrm{E}[(S - \mu)^k]}{a^k}.$$

Bellare and Rompel (1994) bounded the moment and proved: for even $k \ge 4$ and $k$-wise independent $X_i \in [0, 1]$,

$$\Pr\big[|S - \mu| \ge a\big] \le 8 \left( \frac{k \mu + k^2}{a^2} \right)^{k/2}.$$

With $a = c\sqrt{k \mu}$ for $\mu \ge k$, the bound is at most $8(2/c^2)^{k/2}$, which falls exponentially in $k$. So $k$-wise independence gives tails that are exponentially small in $k$, but not in $a^2/\mu$ as the Chernoff bound gives. Schmidt, Siegel and Srinivasan (1995) proved Chernoff-Hoeffding type bounds under $k$-wise independence: roughly, the full independence bound holds as long as $k$ is at least of the order of the exponent in that bound. To get a tail $\delta$ in this way, $k$ must grow like $\log(1/\delta)$, and the sample space then has $n^{\Theta(\log(1/\delta))}$ points.

### Random bits

| independence | tail at deviation $a$ (order of magnitude) | random bits for $n$ variables |
|---|---|---|
| pairwise | $\mu / a^2$ | $2 \log_2 n$ (polynomial space), or $\log_2(n+1)$ for bits |
| $k$-wise, $k$ even | $(k\mu + k^2)^{k/2} / a^k$ | $k \log_2 n$, or about $\frac{k}{2} \log_2 n$ for bits |
| full | $e^{-\Omega(a^2/\mu)}$ for $a \le \mu$ | $n$ for bits |

The random bit counts are for the polynomial construction over a field of size at least $n$ and for the BCH spaces of [k-wise independence](/k-wise-independence/).

## Examples

### Pairwise independence is not enough for exponential tails

Let $X_a = \langle a, y \rangle \bmod 2$ for the $n = 2^m - 1$ nonzero $a \in \{0, 1\}^m$, with $y$ uniform. These bits are pairwise independent and uniform, $\mu = n/2$ and $\mathrm{Var}[S] = n/4$. Chebyshev with $a = n/2$ bounds $\Pr[S = 0] \le 1/n = 1/(2^m - 1)$. The exact value is $\Pr[y = 0] = 1/2^m = 1/(n+1)$, because $S = 0$ for $y = 0$ and $S = (n+1)/2$ for every other $y$. For $m = 3$ the bound is $1/7$ and the truth $1/8$; for $m = 4$, $1/15$ and $1/16$. With 7 fully independent bits, $\Pr[S = 0] = 1/128$. So the Chebyshev bound is almost exact for pairwise independent variables, and no better bound holds in general.

### A fourth moment

For uniform $\pm 1$ variables $\sigma_1, \ldots, \sigma_n$ that are 4-wise independent, let $T = \sum_i \sigma_i$. Expanding $T^4$, only the terms $\sigma_i^4$ and $\sigma_i^2 \sigma_j^2$ have nonzero expectation, so $\mathrm{E}[T^4] = n + 3n(n - 1) \le 3n^2$. Then $\Pr[|T| \ge a] \le 3n^2/a^4$, which for $a = c\sqrt{n}$ is $3/c^4$, better than the Chebyshev value $1/c^2$ when $c^2 > 3$. The AMS sketch for the second frequency moment uses this computation with 4-wise independent signs ([AMS sketch](/ams-sketch/)).

### Error reduction for one-sided error

Let a test accept a "yes" input on a fraction $p$ of its $m$-bit random strings. Run it on $t$ pairwise independent strings. The number of accepting runs has mean $pt$ and variance at most $pt$, so Chebyshev bounds the probability of no accepting run by $(1-p)/(pt)$. With $p \ge 1/2$, $t$ runs on $2m$ random bits give error at most $1/t$, in place of $2^{-t}$ for $tm$ bits. See [randomness amplification](/randomness-amplification/).

## Where it is used

- **Derandomization by enumeration.** An algorithm that needs only $k$-wise independent choices can try all $n^{O(k)}$ points of a small space, see [sample space reduction](/sample-space-reduction/). Luby's parallel [maximal independent set](/maximal-independent-set/) algorithm needs only pairwise independence, which put the problem in NC.
- **Hashing.** [Universal](/universal-hashing/) and [k-independent](/k-independent-hashing/) hash families give the expected bounds of chained hashing with pairwise independence. [Linear probing](/linear-probing/) needs 5-wise independence for constant expected time.
- **Streaming.** Sketches such as the [AMS sketch](/ams-sketch/) and the [count sketch](/count-sketch/) store a seed of $O(\log n)$ bits for a hash function with 2-wise or 4-wise independence in place of $n$ random values.
- **Sampling with few random bits.** Pairwise independent samples estimate a mean with $O(\log n)$ random bits, and the [median trick](/median-trick/) over independent groups turns the polynomial tail into an exponential one. [Expander walks](/expander-walk-sampler/) reach an exponential tail with even fewer bits.
- **Combinatorics.** Several results of the [probabilistic method](/probabilistic-method/), such as the max cut bound of $m/2$, hold over any pairwise independent space, which gives explicit constructions.

## References
