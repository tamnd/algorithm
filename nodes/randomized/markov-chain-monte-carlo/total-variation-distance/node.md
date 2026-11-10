---
tag: DSP0ES
kind: definition
slug: total-variation-distance
name: Total variation distance
aliases:
- statistical distance
area: randomized/markov-chain-monte-carlo
level: core
summary: The total variation distance of μ and ν is the largest gap |μ(A) − ν(A)| over events A. It equals half the L1 distance and the least chance that two coupled draws differ.
prereqs: [probability-distribution, random-variable, markov-chain]
see_also: [mixing-time, coupling-inequality, coupling-method, stationary-distribution, ergodicity, spectral-gap, strong-uniform-time, matrix-norms]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 4.1, Total Variation Distance (Proposition 4.2, Remark 4.3, Proposition 4.5); Section 4.2, Coupling and Total Variation Distance (Proposition 4.7); Section 4.4, Standardizing Distance from Stationarity (Lemma 4.10)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 12, Coupling of Markov Chains (variation distance and the coupling lemma)
---

The total variation distance between two probability distributions $\mu$ and $\nu$ on the same finite set is the largest difference $|\mu(A) - \nu(A)|$ over all events $A$. It equals half the $\ell_1$ distance between the two probability vectors, and it equals the smallest probability that $X \ne Y$ when $X \sim \mu$ and $Y \sim \nu$ are drawn together on one probability space. It is the standard way to measure how far the law of a [Markov chain](/markov-chain/) is from its [stationary distribution](/stationary-distribution/), and the [mixing time](/mixing-time/) is defined through it. In cryptography and complexity theory the same quantity is called the *statistical distance*.

## Definition

Let $\mu$ and $\nu$ be probability distributions on a finite set $\mathcal X$. Their **total variation distance** is
$$
\|\mu - \nu\|_{TV} = \max_{A \subseteq \mathcal X}|\mu(A) - \nu(A)|.
$$
It is a metric on the distributions on $\mathcal X$, with values in $[0, 1]$. It is 0 exactly when $\mu = \nu$, and 1 exactly when $\mu$ and $\nu$ have disjoint supports.

The notation shared by the pages on mixing: for a chain with [transition matrix](/transition-matrix/) $P$ and stationary distribution $\pi$,
$$
d(t) = \max_{x}\|P^t(x, \cdot) - \pi\|_{TV}, \qquad \bar d(t) = \max_{x, y}\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV},
$$
$t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$. Some books define the distance as $\sum_x|\mu(x) - \nu(x)|$, without the factor $\tfrac12$; their values are twice the values here.

### The identities

**Proposition 1 (LPW Proposition 4.2).** Let $B = \{x : \mu(x) \ge \nu(x)\}$. Then
$$
\|\mu - \nu\|_{TV} = \mu(B) - \nu(B) = \sum_{x}(\mu(x) - \nu(x))^+ = \frac12\sum_x|\mu(x) - \nu(x)|.
$$
*Proof.* For any event $A$, the points of $A \setminus B$ add negative terms to $\mu(A) - \nu(A)$, and the points of $B \setminus A$ are positive terms that $A$ leaves out. So $\mu(A) - \nu(A) \le \mu(A \cap B) - \nu(A \cap B) \le \mu(B) - \nu(B)$. In the same way $\nu(A) - \mu(A) \le \nu(B^c) - \mu(B^c)$. The two upper bounds are equal, because $\mu(B) + \mu(B^c) = 1 = \nu(B) + \nu(B^c)$. So the maximum of $|\mu(A) - \nu(A)|$ is $\mu(B) - \nu(B)$, attained at $A = B$. This number is $\sum_x(\mu(x) - \nu(x))^+$. Since $\sum_x(\mu(x) - \nu(x)) = 0$, the sum of the positive parts equals the sum of the negative parts, and each is half of $\sum_x|\mu(x) - \nu(x)|$. $\square$

**Proposition 2 (test functions; LPW Proposition 4.5).** For functions $f : \mathcal X \to \mathbb R$,
$$
\|\mu - \nu\|_{TV} = \frac12\max_{|f| \le 1}\Big|\sum_x f(x)\mu(x) - \sum_x f(x)\nu(x)\Big| = \max_{0 \le f \le 1}\Big(\sum_x f(x)\mu(x) - \sum_x f(x)\nu(x)\Big).
$$
*Proof.* For $|f| \le 1$, $|\sum_x f(x)(\mu(x) - \nu(x))| \le \sum_x|\mu(x) - \nu(x)|$, with equality for $f = 1_B - 1_{B^c}$. For $0 \le f \le 1$, $\sum_x f(x)(\mu(x) - \nu(x)) \le \sum_x(\mu(x) - \nu(x))^+$, with equality for $f = 1_B$. $\square$

So a test that answers 1 with probability $f(x)$ on input $x$, even a randomized one, has acceptance probabilities under $\mu$ and $\nu$ that differ by at most $\|\mu - \nu\|_{TV}$. This is the meaning of "statistical distance" as the best advantage of a distinguisher.

**Proposition 3 (couplings; LPW Proposition 4.7).** A *coupling* of $\mu$ and $\nu$ is a pair of random variables $(X, Y)$ on one probability space with $X \sim \mu$ and $Y \sim \nu$. Then
$$
\|\mu - \nu\|_{TV} = \min\{\Pr[X \ne Y] : (X, Y) \text{ a coupling of } \mu \text{ and } \nu\},
$$
and the minimum is attained.

*Proof.* For any coupling and any event $A$, $\mu(A) - \nu(A) = \Pr[X \in A] - \Pr[Y \in A] \le \Pr[X \in A, Y \notin A] \le \Pr[X \ne Y]$. Take $A = B$. This is the [coupling inequality](/coupling-inequality/). For the other direction, build a *maximal coupling*. Let $p = \sum_x\min(\mu(x), \nu(x)) = 1 - \|\mu - \nu\|_{TV}$. With probability $p$, draw $Z$ from the distribution $\min(\mu, \nu)/p$ and set $X = Y = Z$. With probability $1 - p$, draw $X$ from $(\mu - \nu)^+/(1 - p)$ and $Y$ from $(\nu - \mu)^+/(1 - p)$. The second pair of distributions have disjoint supports. Then $\Pr[X = x] = \min(\mu(x), \nu(x)) + (\mu(x) - \nu(x))^+ = \mu(x)$, in the same way $Y \sim \nu$, and $\Pr[X \ne Y] = 1 - p$. If $p$ is 0 or 1, one of the two branches is empty. $\square$

Proposition 3 is the reason that the [coupling method](/coupling-method/) bounds distances to stationarity: any coupling gives an upper bound, and some coupling gives the exact value.

### Other properties

- **Contraction.** For any transition matrix $P$, $\|\mu P - \nu P\|_{TV} \le \|\mu - \nu\|_{TV}$. *Proof.* $\frac12\sum_y|\sum_x(\mu(x) - \nu(x))P(x, y)| \le \frac12\sum_x|\mu(x) - \nu(x)|\sum_y P(x, y)$. With $\nu = \pi$ this shows that $\|\mu P^t - \pi\|_{TV}$ does not increase in $t$, so $d(t)$ is non-increasing; see [mixing time](/mixing-time/).
- **Convexity.** $\|\sum_i a_i\mu_i - \nu\|_{TV} \le \sum_i a_i\|\mu_i - \nu\|_{TV}$ for weights $a_i \ge 0$ with sum 1, by the triangle inequality on the $\ell_1$ form. So the worst start for $d(t)$ is always a single state: $\max_\mu\|\mu P^t - \pi\|_{TV} = d(t)$.
- **Comparison with $\bar d$ (LPW Lemma 4.10).** $d(t) \le \bar d(t) \le 2d(t)$. The right inequality is the triangle inequality through $\pi$. For the left one, $\pi = \sum_y\pi(y)P^t(y, \cdot)$, so by convexity $\|P^t(x, \cdot) - \pi\|_{TV} \le \sum_y\pi(y)\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV} \le \bar d(t)$.
- **The $\ell^2$ bound.** If $\pi(x) > 0$ for all $x$, the Cauchy-Schwarz inequality gives
$$
\|\mu - \pi\|_{TV} = \frac12\sum_x\pi(x)\Big|\frac{\mu(x)}{\pi(x)} - 1\Big| \le \frac12\Big(\sum_x\pi(x)\Big(\frac{\mu(x)}{\pi(x)} - 1\Big)^2\Big)^{1/2}.
$$
The right side is half the chi-square distance. The [spectral gap](/spectral-gap/) controls it, and that is how the spectral bounds on $t_{mix}$ are proved.
- **Pinsker's inequality.** $\|\mu - \nu\|_{TV} \le \sqrt{D(\mu \| \nu)/2}$, where $D$ is the Kullback-Leibler divergence in nats.

## Examples and non-examples

**One step of the Land of Oz chain.** The chain on (rain, nice, snow) has stationary distribution $\pi = (2/5, 1/5, 2/5)$. One day after rain the law is $\mu = (1/2, 1/4, 1/4)$. The differences are $(1/10, 1/20, -3/20)$, so
$$
\|\mu - \pi\|_{TV} = \tfrac1{10} + \tfrac1{20} = \tfrac3{20},
$$
attained at $A = \{R, N\}$. The maximal coupling agrees with probability $\sum_x\min(\mu(x), \pi(x)) = \tfrac25 + \tfrac15 + \tfrac14 = \tfrac{17}{20}$. After $t$ days from rain the distance is $\tfrac35\cdot4^{-t}$.

**Two coins.** The distributions Bernoulli($p$) and Bernoulli($q$) are at distance $|p - q|$.

**Uniform distributions on nested sets.** If $\nu$ is uniform on a set $S$ and $\mu$ is uniform on a superset $T$, then $\|\mu - \nu\|_{TV} = 1 - |S|/|T|$, attained at $A = S$. For example, let $\mu$ be uniform on all sequences in $\{1, \ldots, n\}^k$, and $\nu$ uniform on the sequences with no repeated entry. Then $\|\mu - \nu\|_{TV} = 1 - n(n-1)\cdots(n-k+1)/n^k$, the birthday collision probability. For $n = 3$, $k = 2$ it is $1/3$.

**A periodic chain.** The walk on a cycle with 4 vertices, started at vertex 0, is at an even vertex at each even time. Its law at time $t \ge 1$ puts mass 0 on half of the states, so it is at distance exactly $1/2$ from the uniform $\pi$ for all $t \ge 1$.

**Non-example: TV does not see geometry.** Two point masses $\delta_x$ and $\delta_y$ with $x \ne y$ are at distance 1, however close $x$ and $y$ are in any metric on $\mathcal X$. Distances that see the metric, such as the transportation (Wasserstein) distance $\min_{\text{couplings}}\mathbb E\rho(X, Y)$, are a different tool; [path coupling](/path-coupling/) contracts that distance and then converts it to a TV bound.

**Non-example: the separation distance.** The quantity $s(t) = \max_{x, y}(1 - P^t(x, y)/\pi(y))$ is not a TV distance. It is at least $d(t)$, and the [strong uniform time](/strong-uniform-time/) method bounds it.

**Non-example: a run is not a distribution.** The TV distance compares laws, not samples. Let $\pi$ be uniform on a set of size $N$. The empirical histogram of $m$ draws from $\pi$ is supported on at most $m$ points, so it is at TV distance at least $1 - m/N$ from $\pi$, which is close to 1 when $N \gg m$. So the distance of a chain's law from $\pi$ cannot be read off from its output, and a convergence diagnostic cannot prove that a chain has mixed.

## Related definitions

- [Mixing time](/mixing-time/): $t_{mix}(\varepsilon)$ is the first time that $d(t) \le \varepsilon$.
- [Coupling inequality](/coupling-inequality/): the easy half of Proposition 3, used for upper bounds.
- [Coupling method](/coupling-method/): couplings of two copies of a chain, which bound $\bar d(t)$.
- [Ergodicity](/ergodicity/): the convergence theorem $d(t) \to 0$.
- [Spectral gap](/spectral-gap/): bounds the $\ell^2$ distance above, hence the TV distance.
- [Strong uniform time](/strong-uniform-time/): bounds the separation distance, hence the TV distance.
- [Matrix norms](/matrix-norms/): $2d(t)$ is the $\ell_\infty \to \ell_\infty$ norm of $P^t - \Pi$, where each row of $\Pi$ is $\pi$, which is the largest $\ell_1$ norm of a row.

## References
