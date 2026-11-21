---
tag: DTRZS8
kind: theorem
slug: min-entropy-leakage-bound
name: Min-capacity bound on leakage
aliases:
- min-capacity theorem
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: The min-entropy leakage of a deterministic program is at most the log of its number of distinct outputs, with equality for a uniform prior.
prereqs: [min-entropy-leakage]
see_also: [g-leakage, quantitative-information-flow, channel-capacity, binary-symmetric-channel, shannon-entropy, min-entropy, covert-channel, declassification]
sources:
  - paper: doi:10.1007/978-3-642-00596-1_21
    title: Geoffrey Smith, On the foundations of quantitative information flow, Proceedings of FoSSaCS 2009, LNCS 5504
    locator: pp. 288 to 302; Theorem 1 on p. 298 (a deterministic program under a uniform prior leaks log of its number of outputs) and Theorem 2 on p. 299 (this equals the Shannon capacity of the program)
  - paper: doi:10.1016/j.entcs.2009.07.085
    title: Christelle Braun, Konstantinos Chatzikokolakis and Catuscia Palamidessi, Quantitative notions of leakage for one-try attacks, Proceedings of MFPS 2009, Electronic Notes in Theoretical Computer Science 249
    locator: pp. 75 to 91, the min-capacity of a channel as the log of the sum of its column maxima, reached at the uniform prior
  - paper: doi:10.1109/CSF.2012.26
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Catuscia Palamidessi and Geoffrey Smith, Measuring information leakage using generalized gain functions, Proceedings of CSF 2012
    locator: pp. 265 to 279; Theorem 2.1 (the closed form of min-capacity), Theorem 5.1 (min-capacity bounds every g-capacity) and Theorem 5.3 (min-capacity is at least the Shannon capacity)
  - book: isbn:9783319961293
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Annabelle McIver, Carroll Morgan, Catuscia Palamidessi and Geoffrey Smith, The Science of Quantitative Information Flow, Springer, 2020
    locator: Chapter 7 (capacity)
---

The min-capacity theorem gives the worst-case [min-entropy leakage](/min-entropy-leakage/) of a channel in closed form. Over all priors, the leakage is at most the base-2 log of the sum of the column maxima of the channel matrix, and the uniform prior reaches this value. For a deterministic program, each output that can occur has column maximum 1, so the bound is the log of the number of distinct outputs. A program with $m$ possible outputs therefore leaks at most $\log_2 m$ bits to a one-try attacker, whatever the prior. Smith (2009) proved the deterministic case under a uniform prior, and Braun, Chatzikokolakis and Palamidessi (2009) gave the general form.

## Statement

**Theorem.** Let $C$ be a channel matrix from a finite set $\mathcal X$ of secrets to a finite set $\mathcal Y$ of outputs, with $C[x, y] = P(Y = y \mid X = x)$. For every prior $\pi$ on $\mathcal X$,

$$ \mathcal L(\pi, C) = \log_2 \frac{\sum_y \max_x \pi(x)\, C[x, y]}{\max_x \pi(x)} \;\le\; \log_2 \sum_{y \in \mathcal Y} \max_{x \in \mathcal X} C[x, y], $$

with equality when $\pi$ is uniform on $\mathcal X$. Hence the min-capacity is

$$ \mathcal{ML}(C) = \sup_\pi \mathcal L(\pi, C) = \log_2 \sum_{y} \max_{x} C[x, y]. $$

If $C$ is the channel of a deterministic program $y = f(x)$, then $\mathcal{ML}(C) = \log_2 |f(\mathcal X)|$, the log of the number of distinct outputs, and the uniform prior leaks exactly this amount.

## In plain words

Before seeing anything, the attacker's best guess wins with probability $V(\pi)$, the largest prior probability. After seeing an output, the attacker's best guess for that output can do no better than if every secret had that largest probability. Summing over the outputs, the output multiplies the chance of a correct guess by at most the sum of the column maxima of the matrix. Under a uniform prior no secret starts ahead, so nothing is lost in that step and the bound is exact. For a program without randomness, each possible output contributes exactly 1 to the sum. So the program cannot raise the attacker's chance by more than a factor equal to its number of outputs. A password check has two outputs and leaks at most 1 bit.

## Proof

Let $V(\pi) = \max_x \pi(x)$. For every $x$ and $y$, $\pi(x)\, C[x, y] \le V(\pi)\, C[x, y]$. Taking the maximum over $x$ and summing over $y$,

$$ V(\pi, C) = \sum_y \max_x \pi(x)\, C[x, y] \le V(\pi) \sum_y \max_x C[x, y]. $$

Divide by $V(\pi) > 0$ and take $\log_2$, which is increasing; this gives the inequality.

For the uniform prior, $\pi(x) = 1/|\mathcal X|$ for every $x$, so $V(\pi) = 1/|\mathcal X|$ and $V(\pi, C) = \frac{1}{|\mathcal X|} \sum_y \max_x C[x, y]$. The ratio is $\sum_y \max_x C[x, y]$, so equality holds. Since the bound holds for every prior and is reached at one, it is the supremum, which gives the formula for $\mathcal{ML}(C)$.

For a deterministic program, column $y$ of $C$ contains a 1 in row $x$ if $f(x) = y$ and zeros elsewhere. So $\max_x C[x, y] = 1$ if $y \in f(\mathcal X)$ and 0 otherwise, and $\sum_y \max_x C[x, y] = |f(\mathcal X)|$. ∎

## Consequences

Each item is a theorem unless marked otherwise.
- **A bound on the attacker's success.** For every prior, $V(\pi, C) \le V(\pi) \cdot 2^{\mathcal{ML}(C)}$. The adversary is the one of [min-entropy leakage](/min-entropy-leakage/): it knows $\pi$ and $C$, sees one output and makes one guess. A deterministic program with $m$ outputs raises the chance of a correct guess by a factor of at most $m$.
- **Capacity without optimization.** Computing $\mathcal{ML}(C)$ takes one pass over the matrix, $O(|\mathcal X|\,|\mathcal Y|)$ operations. The Shannon [channel capacity](/channel-capacity/) is a maximum over priors with no closed form in general.
- **Counting outputs bounds leakage.** An analysis that proves that a program has at most $m$ outputs, or that an observable such as a running time takes at most $m$ values, proves a leakage bound of $\log_2 m$ bits for that observable and that adversary. The bound says nothing about what an attacker gains from observables outside the model.
- **Repeated observations.** Let the attacker see the outputs of two channels $C_1$ and $C_2$ run on the same secret with independent randomness. The joint channel has entries $C_1[x, y_1]\, C_2[x, y_2]$, and $\max_x C_1[x, y_1] C_2[x, y_2] \le \max_x C_1[x, y_1] \cdot \max_x C_2[x, y_2]$. Summing gives $\mathcal{ML}(C_1 \| C_2) \le \mathcal{ML}(C_1) + \mathcal{ML}(C_2)$. So $n$ independent runs of a channel leak at most $n\, \mathcal{ML}(C)$ bits.
- **Every gain function.** The Miracle theorem of Alvim et al. (2012) uses this bound to show that the [g-leakage](/g-leakage/) of $C$, for every gain function and every prior, is at most $\mathcal{ML}(C)$. In particular, an attacker with $k$ tries does not see a larger capacity than a one-try attacker.
- **Shannon capacity.** Theorem 5.3 of Alvim et al. (2012) shows that the Shannon capacity of every channel is at most $\mathcal{ML}(C)$. So the min-capacity also bounds the mutual information $H(X) - H(X \mid Y)$ of [Shannon entropy](/shannon-entropy/) for every prior.

## Tightness

- **The bound is exact as a supremum.** The uniform prior reaches it for every channel, so no smaller function of $C$ bounds the leakage for all priors.
- **It can be far from the leakage at a given prior.** For the [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $0.1$, $\mathcal{ML}(C) = \log_2 1.8 = 0.847997$ bits, reached at the uniform prior. Under the prior $(0.9, 0.1)$, the best guess is 0 for both outputs and the leakage is 0. The bound is a worst case over priors, not an estimate for a known prior.
- **Equality at other priors.** For a deterministic program, the leakage under $\pi$ is $\log_2$ of $\sum_{y} \max_{x : f(x) = y} \pi(x) / \max_x \pi(x)$. It equals $\log_2 |f(\mathcal X)|$ exactly when every set $f^{-1}(y)$ holds a secret of the largest prior probability. So the uniform prior is sufficient for equality, not necessary.
- **Shannon capacity can be smaller.** For the same binary symmetric channel, the Shannon capacity is $1 - H(0.1) = 0.531004$ bits, below the min-capacity of 0.848 bits. For a deterministic program the two capacities agree, both being $\log_2 m$ (Theorem 2 of Smith 2009), but the Shannon capacity is reached at a prior that makes all outputs equally likely, which is typically not uniform on the secrets.
- **The multiplicative form matters.** The uniform prior does not maximize the additive leakage $V(\pi, C) - V(\pi)$. For the channel with rows $(1/5, 1/5, 3/5)$, $(4/7, 3/7, 0)$ and $(0, 1/5, 4/5)$, the uniform prior gives an additive leakage of $4/15$ and the prior $(0, 1/2, 1/2)$ gives $2/5$.
- **Repeated runs.** The bound $n\, \mathcal{ML}(C)$ for $n$ runs is not reached in general, because the min-entropy of the secret is finite: the leakage can never exceed $-\log_2 V(\pi)$, since $V(\pi, C) \le 1$.

## History

Smith (2009) argued that Shannon leakage misjudges the threat of a one-try attacker and proposed min-entropy leakage. His Theorem 1 states that a deterministic program under a uniform prior leaks $\log_2 |\mathcal Y|$ bits, where $\mathcal Y$ is its set of possible outputs, and his Theorem 2 notes that this equals the Shannon capacity of the program. In the same year, Braun, Chatzikokolakis and Palamidessi studied one-try attacks on probabilistic channels and showed that the multiplicative leakage is maximized by the uniform prior, which gives the closed form $\log_2 \sum_y \max_x C[x, y]$. Alvim, Chatzikokolakis, Palamidessi and Smith (2012) used the theorem as the base of the theory of [g-leakage](/g-leakage/), with the Miracle theorem and the comparison with Shannon capacity. The book of Alvim et al. (2020) treats capacity for gain functions and priors in general.

## References
