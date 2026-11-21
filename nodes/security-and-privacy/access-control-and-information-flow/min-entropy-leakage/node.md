---
tag: 7HY8Q8
kind: definition
slug: min-entropy-leakage
name: Min-entropy leakage
aliases:
- vulnerability-based leakage
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: The leakage of a channel as the log of the ratio of an attacker's chance to guess the secret in one try after and before seeing the output.
prereqs: [min-entropy, bayes-theorem, quantitative-information-flow]
see_also: [min-entropy-leakage-bound, g-leakage, shannon-entropy, conditional-entropy, channel-capacity, binary-symmetric-channel, noninterference, covert-channel]
sources:
  - paper: doi:10.1007/978-3-642-00596-1_21
    title: Geoffrey Smith, On the foundations of quantitative information flow, Proceedings of FoSSaCS 2009, LNCS 5504
    locator: pp. 288 to 302; Section 4 (the examples where Shannon entropy misjudges the one-guess threat) and Section 5 (Definitions 1 to 4 of vulnerability, min-entropy, conditional vulnerability and conditional min-entropy, and Theorem 1)
  - paper: doi:10.1016/j.entcs.2009.07.085
    title: Christelle Braun, Konstantinos Chatzikokolakis and Catuscia Palamidessi, Quantitative notions of leakage for one-try attacks, Proceedings of MFPS 2009, Electronic Notes in Theoretical Computer Science 249
    locator: pp. 75 to 91, multiplicative and additive leakage for one-try attacks and the min-capacity
  - paper: doi:10.1109/CSF.2012.26
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Catuscia Palamidessi and Geoffrey Smith, Measuring information leakage using generalized gain functions, Proceedings of CSF 2012
    locator: pp. 265 to 279, Section 2 (min-entropy leakage and min-capacity as the starting point of g-leakage)
  - book: isbn:9783319961293
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Annabelle McIver, Carroll Morgan, Catuscia Palamidessi and Geoffrey Smith, The Science of Quantitative Information Flow, Springer, 2020
    locator: Chapter 2 (Bayes vulnerability of a prior), Chapter 4 (channels), Chapter 5 (posterior vulnerability and leakage) and Chapter 7 (capacity)
---

Min-entropy leakage measures how much a channel helps an attacker who wants to guess a secret in one try. It compares the attacker's best chance of a correct guess before seeing the output, the prior vulnerability, with the best chance after seeing it, the posterior vulnerability, and reports the base-2 log of the ratio. A leakage of $L$ bits means that the output multiplies the attacker's success probability by $2^L$. Geoffrey Smith proposed it in 2009 because the Shannon measures of [quantitative information flow](/quantitative-information-flow/) can rate a program as safe when it lets the attacker guess the secret often.

## Definition

**Secret, prior and channel.** The secret $X$ takes values in a finite set $\mathcal X$ with a prior distribution $\pi$. A system is modeled as a channel from $\mathcal X$ to a finite set $\mathcal Y$ of observable outputs, given by a matrix $C$ with $C[x, y] = P(Y = y \mid X = x)$; each row sums to 1. A deterministic program $y = f(x)$ has $C[x, f(x)] = 1$ and zeros elsewhere. The joint distribution is $p(x, y) = \pi(x)\, C[x, y]$.

**Adversary.** The attacker knows $\pi$ and $C$, sees one output $y$, and makes one guess of the secret. The guess wins when it equals $X$ exactly. The attacker may choose the guess as any function of $y$. Nothing else is observed: timing, repeated runs and other side information are outside the model unless they are part of $Y$.

**Vulnerabilities.**

$$ V(\pi) = \max_{x} \pi(x), \qquad V(\pi, C) = \sum_{y} p(y) \max_x p(x \mid y) = \sum_{y} \max_{x} \pi(x)\, C[x, y]. $$

The second form of $V(\pi, C)$ follows from [Bayes' theorem](/bayes-theorem/), $p(y)\,p(x \mid y) = \pi(x)\,C[x, y]$, and needs no division. $V(\pi)$ is the probability that the best blind guess is right. $V(\pi, C)$ is the probability that the best guess after seeing $y$ is right, averaged over $y$.

**Min-entropy and leakage.** The [min-entropy](/min-entropy/) of the prior and the conditional min-entropy are

$$ H_\infty(\pi) = -\log_2 V(\pi), \qquad H_\infty(\pi, C) = -\log_2 V(\pi, C). $$

The min-entropy page defines the same quantity; the QIF pages measure it in bits, with $\log_2$. The **min-entropy leakage** of $C$ under $\pi$ is

$$ \mathcal L(\pi, C) = H_\infty(\pi) - H_\infty(\pi, C) = \log_2 \frac{V(\pi, C)}{V(\pi)}. $$

The **min-capacity** is the worst case over priors, $\mathcal{ML}(C) = \sup_\pi \mathcal L(\pi, C)$. The [min-capacity bound](/min-entropy-leakage-bound/) proves that $\mathcal{ML}(C) = \log_2 \sum_y \max_x C[x, y]$, reached by the uniform prior.

**Computation.** With $|\mathcal X| = n$ secrets and $|\mathcal Y| = k$ outputs, the leakage costs $O(nk)$ arithmetic operations:

```pseudo id=main
MIN-ENTROPY-LEAKAGE(π, C)
L1  V0 ← max over x of π[x]
L2  V1 ← 0
L3  for each output y do
L4      V1 ← V1 + max over x of π[x] · C[x, y]
L5  return log2(V1 / V0)
```

The Python implementation does all of this with `fractions.Fraction` and takes the logarithm only at the end. Its tests check every example on this page, compare $V(\pi, C)$ with an enumeration of all guessing strategies on 600 random channels, and compare the min-capacity formula with a search over all priors on a grid of step 1/12.

**Basic facts.** Each is a theorem with a short proof.
- *$V(\pi, C)$ is the success of the best strategy.* A strategy is a map $s$ from outputs to guesses, and it wins with probability $\sum_y \pi(s(y))\, C[s(y), y] \le \sum_y \max_x \pi(x) C[x, y]$, with equality for $s(y) = \arg\max_x \pi(x) C[x, y]$.
- *Leakage is never negative.* Let $x^*$ maximize $\pi$. Then $V(\pi, C) \ge \sum_y \pi(x^*)\, C[x^*, y] = \pi(x^*) = V(\pi)$, so $\mathcal L(\pi, C) \ge 0$.
- *Zero leakage.* $\mathcal L(\pi, C) = 0$ if and only if one guess $x$ maximizes $\pi(x) C[x, y]$ for every output $y$ at once, by the equality case of the previous line. So zero leakage does not mean that the output is independent of the secret; see the skewed channel below.
- *Post-processing cannot increase it.* If $D$ is a second channel applied to the output of $C$, then $\sum_z \max_x \sum_y \pi(x) C[x, y] D[y, z] \le \sum_z \sum_y D[y, z] \max_x \pi(x) C[x, y] = V(\pi, C)$, because the rows of $D$ sum to 1. So $\mathcal L(\pi, CD) \le \mathcal L(\pi, C)$.
- *A security guarantee.* $V(\pi, C) = 2^{-H_\infty(\pi, C)}$ exactly, so a bound on the leakage is a bound on the attacker's one-try success: $V(\pi, C) \le 2^{\mathcal L(\pi, C)}\, V(\pi)$. With $m$ tries the success is at most $m\, V(\pi, C)$.

## Examples and non-examples

**Example: the last two bits.** Let $h$ be uniform on $\{0, \ldots, 7\}$ and let the program output $h \bmod 4$. Then $V(\pi) = 1/8$. Each of the 4 outputs has two secrets of probability $1/8$, so $V(\pi, C) = 4 \cdot 1/8 = 1/2$ and $\mathcal L = \log_2 4 = 2$ bits. The attacker's chance goes from $1/8$ to $1/2$.

**Example: a password check.** Let $h$ be uniform on 8 values and let the output be whether $h$ equals a fixed value. The output "yes" has one secret of probability $1/8$ and the output "no" has seven, so $V(\pi, C) = 1/8 + 1/8 = 1/4$ and $\mathcal L = 1$ bit. For a uniform secret on $n$ values the leakage of one check is always 1 bit, while the attacker's chance grows only from $1/n$ to $2/n$.

**Example: a noisy bit.** The [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $0.1$ copies a secret bit and flips it with probability $0.1$. Under the uniform prior, $V(\pi) = 1/2$ and $V(\pi, C) = 0.45 + 0.45 = 0.9$, so $\mathcal L = \log_2 1.8 = 0.847997$ bits. This is also its min-capacity. Its Shannon capacity is $1 - H(0.1) = 0.531004$ bits, which is smaller; the [min-capacity bound](/min-entropy-leakage-bound/) page proves that the min-capacity is never below the Shannon capacity.

**Non-example: zero leakage with a dependent output.** Use the same channel with the prior $\pi = (0.9, 0.1)$. Then $V(\pi) = 0.9$, and $V(\pi, C) = \max(0.81, 0.01) + \max(0.09, 0.09) = 0.9$, so $\mathcal L = 0$. The best guess is 0 whatever the output, so the output does not help a one-try attacker. The Shannon mutual information is $H(Y) - H(Y \mid X) = H(0.82) - H(0.1) = 0.211$ bits, so the output does carry information in the Shannon sense. Zero min-entropy leakage is not [noninterference](/noninterference/): noninterference asks that the output distribution be the same for every secret, which fails here.

**Non-example: Shannon leakage as a proxy.** Let $h$ be uniform on $\{0, \ldots, 255\}$, an 8-bit secret, and compare two programs, after the examples of Smith (2009):
- program A outputs $h$ when $h$ is a multiple of 8 and outputs 1 otherwise;
- program B outputs the last three bits of $h$.

| program | outputs | Shannon leakage $H(Y)$ | $V(\pi, C)$ | min-entropy leakage |
| --- | --- | --- | --- | --- |
| A | 33 | 1.169 bits | 33/256 = 0.129 | $\log_2 33 = 5.044$ bits |
| B | 8 | 3 bits | 8/256 = 0.031 | 3 bits |

For a deterministic program the Shannon leakage is the entropy of the output. By that measure A leaks less than B. But A reveals the whole secret one time in eight, and its attacker guesses right with probability 0.129, four times the 0.031 of B. Min-entropy leakage ranks them the right way for a one-try attacker. The numbers were computed exactly with the implementation of this page.

**Non-example: a different attacker.** If the attacker has three tries, or wins by guessing a value close to the secret, min-entropy leakage is the wrong measure. [g-leakage](/g-leakage/) handles those attackers with a gain function.

## Related definitions

- **[Min-entropy](/min-entropy/).** The same quantity $-\log_2 \max_x \pi(x)$, used in randomness extraction. Here it measures the uncertainty that matters for one guess.
- **[Shannon entropy](/shannon-entropy/) and [conditional entropy](/conditional-entropy/).** The Shannon leakage is $H(X) - H(X \mid Y)$, the mutual information. It measures the expected number of bits needed to describe the secret, not the chance of guessing it. For a deterministic program under a uniform prior, the two agree exactly when all outputs are equally likely, which is the case for program B in the table and not for program A.
- **Additive leakage.** $V(\pi, C) - V(\pi)$, studied by Braun, Chatzikokolakis and Palamidessi (2009) next to the multiplicative form above. It is not maximized by the uniform prior in general: for the channel with rows $(1/5, 1/5, 3/5)$, $(4/7, 3/7, 0)$ and $(0, 1/5, 4/5)$, the uniform prior gives $4/15$ and the prior $(0, 1/2, 1/2)$ gives $2/5$.
- **[g-leakage](/g-leakage/).** Replaces "one exact guess" by a gain function $g(w, x)$; min-entropy leakage is the case of the identity gain.
- **[Min-capacity bound](/min-entropy-leakage-bound/).** The theorem that gives $\mathcal{ML}(C)$ in closed form and, for a deterministic program, $\log_2$ of the number of distinct outputs.
- **[Channel capacity](/channel-capacity/).** The Shannon analogue: the maximum mutual information over priors.
- **[Covert channel](/covert-channel/).** Min-capacity per use is one way to state the bandwidth of a covert channel against a one-try receiver.

## References
