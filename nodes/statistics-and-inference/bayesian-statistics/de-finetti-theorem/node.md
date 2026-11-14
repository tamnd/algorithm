---
tag: FHK5T8
kind: theorem
slug: de-finetti-theorem
name: De Finetti's theorem
aliases:
- de Finetti representation theorem
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: An infinite exchangeable sequence of random variables is a mixture of i.i.d. sequences. This gives a reason to model data with a prior over a parameter.
prereqs: [bayesian-inference, law-of-large-numbers, binomial-distribution, total-variation-distance]
see_also: [posterior-predictive-distribution, conjugate-prior, dirichlet-process, permutation-test, conformal-prediction, martingale, credible-interval]
sources:
  - paper: "Bruno de Finetti, La prévision: ses lois logiques, ses sources subjectives, Annales de l'Institut Henri Poincaré 7(1), 1937"
    locator: pages 1 to 68 (exchangeable events and the representation of their law as a mixture of Bernoulli laws)
  - paper: doi:10.1090/S0002-9947-1955-0076206-8
    title: "Edwin Hewitt and Leonard J. Savage, Symmetric measures on Cartesian products, Transactions of the American Mathematical Society 80(2), 1955"
    locator: pages 470 to 501 (the representation for exchangeable sequences with values in general spaces, and the zero-one law)
  - paper: "Persi Diaconis and David Freedman, Finite exchangeable sequences, Annals of Probability 8(4), 1980"
    locator: pages 745 to 764 (a finite exchangeable sequence that extends to a longer one is close to a mixture of iid laws, with error of order the ratio of the two lengths)
  - book: isbn:9780471494645
    title: "José M. Bernardo and Adrian F. M. Smith, Bayesian Theory, Wiley, 1994"
    locator: Chapter 4 (exchangeability and the representation theorems)
---

De Finetti's theorem says that an infinite sequence of 0-1 random variables whose joint law does not change when finitely many terms are permuted is a mixture of sequences of independent coin tosses. There is one probability law $\mu$ on $[0, 1]$, the law of the long-run frequency of ones, such that the sequence behaves as if a coin bias $\theta$ were first drawn from $\mu$ and then the tosses were iid Bernoulli$(\theta)$. For Bayesian statistics this is the reason to model data as iid given a parameter with a prior: if the order of the observations is judged not to matter, the parameter and its prior follow. The result fails for finite sequences, which are only close to such mixtures.

## Statement

A sequence of random variables $X_1, X_2, \ldots$ is **exchangeable** if for every $n$ and every permutation $\sigma$ of $\{1, \ldots, n\}$ the vector $(X_{\sigma(1)}, \ldots, X_{\sigma(n)})$ has the same law as $(X_1, \ldots, X_n)$.

**Theorem (de Finetti).** Assume:

1. $X_1, X_2, \ldots$ is an infinite sequence of random variables with values in $\{0, 1\}$;
2. the sequence is exchangeable.

Then:

- (a) $S_n/n$, where $S_n = X_1 + \cdots + X_n$, converges almost surely and in mean square to a random variable $\Theta$ with values in $[0, 1]$;
- (b) with $\mu$ the law of $\Theta$, for every $n$ and every $x_1, \ldots, x_n \in \{0, 1\}$ with $s = x_1 + \cdots + x_n$,
$$P(X_1 = x_1, \ldots, X_n = x_n) = \int_0^1 \theta^s (1 - \theta)^{n - s}\, \mu(d\theta);$$
- (c) given $\Theta$, the $X_i$ are iid Bernoulli$(\Theta)$: $P(X_1 = x_1, \ldots, X_n = x_n \mid \Theta) = \Theta^s(1 - \Theta)^{n-s}$ almost surely;
- (d) $\mu$ is the only probability measure on $[0, 1]$ for which (b) holds.

Conversely, every mixture of this form is an exchangeable sequence. Hewitt and Savage (1955) proved the same representation for exchangeable sequences with values in more general spaces, including the real line, with a random probability law in place of $\Theta$.

## In plain words

Suppose you watch a long run of yes-or-no results, and you believe that only the number of yes answers matters, not the order in which they come. Then you must think about the data in one way. There is an unknown long-run rate of yes answers. Your uncertainty about that rate is a probability distribution. Given the rate, the results act like independent tosses of a coin with that bias. So the usual Bayesian set-up, a parameter with a prior and independent data given the parameter, is not an extra assumption: it follows from the belief that order does not matter, for a sequence that can go on forever. The prior is your belief about a quantity you could, in principle, observe: the long-run frequency.

## Proof

The proof uses only exchangeability, counting and Chebyshev's inequality. Write $(a)_j = a(a - 1)\cdots(a - j + 1)$ for a falling factorial, with $(a)_0 = 1$.

**Step 1: the moments of pairs.** By exchangeability $E[X_i] = m$ for all $i$ and $E[X_i X_j] = c$ for all $i \ne j$, with $c \le m$ because $X_iX_j \le X_i$. Since $X_i^2 = X_i$, for $j \le n$

$$E[S_n^2] = nm + n(n - 1)c, \qquad E[S_j S_n] = jm + j(n - 1)c.$$

**Step 2: $S_n/n$ converges.** For $j < n$, expanding the square with Step 1 gives

$$E\Big[\Big(\frac{S_n}{n} - \frac{S_j}{j}\Big)^2\Big] = (m - c)\Big(\frac1j - \frac1n\Big).$$

So $S_n/n$ is a Cauchy sequence in mean square and converges in mean square to some $\Theta \in [0, 1]$. For almost sure convergence take $n = k^2$: then $E[(S_{k^2}/k^2 - \Theta)^2] = (m - c)/k^2$ (let $n \to \infty$ above), so by Chebyshev's inequality and the Borel-Cantelli lemma $S_{k^2}/k^2 \to \Theta$ almost surely. For $k^2 \le n < (k + 1)^2$ the terms are in $[0, 1]$, so $|S_n/n - S_{k^2}/k^2| \le 2(n - k^2)/n \le 2(2k + 1)/k^2$, which tends to 0. This proves (a).

**Step 3: the urn.** Fix $n < N$, a pattern $x = (x_1, \ldots, x_n)$ with $s$ ones, and $0 \le k \le N$ with $P(S_N = k) > 0$. Every arrangement of $k$ ones among the first $N$ places has the same probability, because a permutation carries one to another and does not change the law. So, given $S_N = k$, $(X_1, \ldots, X_N)$ is a uniformly random arrangement, and $(X_1, \ldots, X_n)$ is a sample of $n$ balls drawn without replacement from an urn of $k$ ones and $N - k$ zeros:

$$P(X_1 = x_1, \ldots, X_n = x_n \mid S_N = k) = \frac{(k)_s\, (N - k)_{n - s}}{(N)_n} =: h_N(k).$$

**Step 4: without replacement is close to with replacement.** Draw $n$ ball positions from the urn uniformly with replacement. If they are all different, they are a uniform sample without replacement. The probability that two of them agree is at most $\binom n2 /N$. So for every event about the colours, in particular the pattern $x$,

$$\Big| h_N(k) - \Big(\frac kN\Big)^s\Big(1 - \frac kN\Big)^{n - s} \Big| \le \frac{n(n - 1)}{2N} \quad \text{for every } k.$$

**Step 5: the representation (b) and (c).** Let $g$ be a continuous function on $[0, 1]$. By Step 3,

$$E\big[1\{X_1 = x_1, \ldots, X_n = x_n\}\, g(S_N/N)\big] = E\big[h_N(S_N)\, g(S_N/N)\big].$$

As $N \to \infty$, $S_N/N \to \Theta$ almost surely, so by bounded convergence the left side tends to $E[1\{X_1 = x_1, \ldots, X_n = x_n\}\, g(\Theta)]$. By Step 4 the right side differs from $E[(S_N/N)^s (1 - S_N/N)^{n-s} g(S_N/N)]$ by at most $\max|g| \cdot n(n - 1)/(2N)$, and that expectation tends to $E[\Theta^s(1 - \Theta)^{n-s} g(\Theta)]$. So

$$E\big[1\{X_1 = x_1, \ldots, X_n = x_n\}\, g(\Theta)\big] = E\big[\Theta^s(1 - \Theta)^{n - s} g(\Theta)\big]$$

for every continuous $g$, hence for every bounded measurable $g$. This is (c). Taking $g = 1$ gives (b).

**Step 6: uniqueness (d).** If (b) holds for $\mu$, then $\int \theta^n \mu(d\theta) = P(X_1 = \cdots = X_n = 1)$ for every $n$, so the law of the $X_i$ fixes all moments of $\mu$. Polynomials are dense in the continuous functions on $[0, 1]$ (Weierstrass), so the moments fix $\int g\, d\mu$ for every continuous $g$, and so fix $\mu$.

**The converse.** If $\Theta \sim \mu$ and the $X_i$ are iid Bernoulli$(\Theta)$ given $\Theta$, the probability of a pattern depends only on its number of ones, so every permutation leaves it unchanged. $\square$

## Consequences

**Priors and posteriors.** The law of an exchangeable 0-1 sequence is a prior $\mu$ on a parameter $\theta$ and an iid Bernoulli model given $\theta$. The predictive probability of a one at the next step is
$$P(X_{n+1} = 1 \mid x_1, \ldots, x_n) = \frac{\int \theta^{s+1}(1 - \theta)^{n - s}\,\mu(d\theta)}{\int \theta^s(1 - \theta)^{n-s}\,\mu(d\theta)} = E[\Theta \mid x_1, \ldots, x_n],$$
the posterior mean, which is the [posterior predictive](/posterior-predictive-distribution/) probability. The parameter has a meaning in terms of observables: it is the limit of the frequency of ones, by (a).

**The Pólya urn.** Start an urn with $a$ balls marked 1 and $b$ marked 0; draw a ball, return it with one more of the same mark, and repeat. The probability of a sequence with $s$ ones in $n$ draws is $B(a + s, b + n - s)/B(a, b)$, which depends only on $s$, so the draws are exchangeable, and by (b) and (d) the mixing law is the Beta$(a, b)$ [conjugate prior](/conjugate-prior/). For $a = 2$, $b = 3$ the product of the urn's step probabilities agrees with the beta formula for all 64 sequences of length 6, checked exactly with rational numbers. For $a = b = 1$, a sequence of 3 draws with 0, 1, 2 or 3 ones has probability $1/4$, $1/12$, $1/12$ or $1/4$; the mixing law is uniform. The urn predicts a one next with probability $(a + s)/(a + b + n)$.

**Positive correlation.** By (b), $\mathrm{Cov}(X_1, X_2) = E[\Theta^2] - E[\Theta]^2 = \mathrm{Var}(\Theta) \ge 0$. Infinite exchangeable 0-1 sequences are never negatively correlated, and they are independent only when $\mu$ is a point mass.

**General spaces.** The Hewitt and Savage form says that an exchangeable sequence of real random variables is iid given its limiting empirical distribution, which is random. A prior on that random law is a nonparametric prior; the [Dirichlet process](/dirichlet-process/) is the case whose predictive rule is a generalized Pólya urn.

**Methods that need only exchangeability.** [Permutation tests](/permutation-test/) and [conformal prediction](/conformal-prediction/) are valid when the data are exchangeable, a weaker assumption than iid; de Finetti's theorem says that, for an infinite sequence, exchangeable means conditionally iid.

## Tightness

**A finite exchangeable sequence need not be a mixture.** Let $(X_1, X_2)$ take the values $(1, 0)$ and $(0, 1)$ with probability $1/2$ each. It is exchangeable. If it were a mixture, then $E[\Theta] = P(X_1 = 1) = 1/2$ and $P(X_1 = X_2 = 1) = E[\Theta^2] \ge E[\Theta]^2 = 1/4$, but this probability is 0. The pair has negative correlation, which by the consequence above no infinite exchangeable sequence has; so it cannot be extended to one.

**Finite sequences are close to mixtures.** Steps 3 and 4 hold for any exchangeable $(X_1, \ldots, X_N)$, infinite or not. They show that the law of the first $n$ values is within [total variation distance](/total-variation-distance/) $n(n - 1)/(2N)$ of the mixture of iid Bernoulli laws with mixing law that of $S_N/N$. The exact distance between the urn without replacement and with replacement, computed with rational numbers and maximized over $k$, is 0.0395 for $N = 20$, $n = 3$ (bound 0.15) and 0.0277 for $N = 50$, $n = 5$ (bound 0.2); in these cases it is near $n/(4N)$. Diaconis and Freedman (1980) study this approximation in general; for 0-1 values the error is of order $n/N$, as these numbers suggest, so a short exchangeable sequence that extends to a much longer one is nearly a mixture.

**The infinite length is needed, not only exchangeability.** The two-point example is exchangeable for every permutation of its two terms. What fails is extendibility to longer exchangeable sequences.

## History

Bruno de Finetti proved the 0-1 case in 1931 and gave it a central place in his 1937 lectures at the Institut Henri Poincaré, published as "La prévision". For him it showed that a subjective probability over observable events, with the symmetry of exchangeability, produces the parameter and the prior of the statistical model, which need not be taken as real. Hewitt and Savage (1955) gave the general form with a zero-one law for symmetric events. Diaconis and Freedman (1980) gave the finite version and its rate.

## References
