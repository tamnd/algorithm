---
tag: XKQ40D
kind: definition
slug: g-leakage
name: g-leakage
aliases:
- gain function leakage
area: security-and-privacy/access-control-and-information-flow
level: research
summary: Generalizes min-entropy leakage with a gain function that scores each guess, to model attackers who profit from partial or several guesses.
prereqs: [min-entropy-leakage]
see_also: [min-entropy-leakage-bound, quantitative-information-flow, channel-capacity, shannon-entropy, min-entropy, loss-function, metric-space, jensens-inequality]
sources:
  - paper: doi:10.1109/CSF.2012.26
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Catuscia Palamidessi and Geoffrey Smith, Measuring information leakage using generalized gain functions, Proceedings of CSF 2012
    locator: pp. 265 to 279; Definitions 3.1 to 3.6 and Proposition 3.1 (gain functions, g-vulnerability, g-leakage, identity, metric and binary gains), Examples 4 and 5, Theorems 4.1 and 4.2, Theorem 5.1 (the Miracle theorem), Corollary 5.2, Theorem 5.3 and Theorem 6.2
  - paper: doi:10.1109/CSF.2014.29
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Annabelle McIver, Carroll Morgan, Catuscia Palamidessi and Geoffrey Smith, Additive and multiplicative notions of leakage, and their capacities, Proceedings of CSF 2014
    locator: additive and multiplicative g-leakage and their capacities over priors and gain functions
  - book: isbn:9783319961293
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Annabelle McIver, Carroll Morgan, Catuscia Palamidessi and Geoffrey Smith, The Science of Quantitative Information Flow, Springer, 2020
    locator: Chapter 3 (gain functions and g-vulnerability), Chapter 5 (posterior g-vulnerability and g-leakage) and Chapter 7 (capacity)
---

g-leakage measures how much a channel helps an attacker whose payoff is not just "right or wrong in one guess". A gain function $g(w, x)$ says how much the attacker earns by guessing $w$ when the secret is $x$, so it can model an attacker who wins by guessing a value close to the secret, a property of the secret, or the secret within $k$ tries. The leakage is the base-2 log of the ratio of the best expected gain after and before seeing the output. Alvim, Chatzikokolakis, Palamidessi and Smith defined it in 2012. [Min-entropy leakage](/min-entropy-leakage/) is the special case where only an exact guess earns anything.

## Definition

**Secret, prior and channel.** As for [min-entropy leakage](/min-entropy-leakage/): a secret $X$ in a finite set $\mathcal X$ with prior $\pi$, and a channel matrix $C$ with $C[x, y] = P(Y = y \mid X = x)$ from $\mathcal X$ to a finite set $\mathcal Y$ of outputs.

**Gain function.** A finite nonempty set $\mathcal W$ of allowed guesses and a function $g : \mathcal W \times \mathcal X \to [0, 1]$. The guesses need not be secrets. Alvim et al. rule out gain functions for which some secret earns 0 under every guess, so that $V_g(\pi) > 0$ for every prior.

**Adversary.** The attacker knows $\pi$, $C$ and $g$, sees one output $y$, and picks one guess $w \in \mathcal W$ as any function of $y$. The payoff is $g(w, X)$, and the attacker maximizes its expectation. Nothing outside $Y$ is observed.

**g-vulnerability and g-leakage.**

$$ V_g(\pi) = \max_{w} \sum_{x} \pi(x)\, g(w, x), \qquad V_g(\pi, C) = \sum_{y} \max_{w} \sum_{x} \pi(x)\, C[x, y]\, g(w, x). $$

$$ H_g(\pi) = -\log_2 V_g(\pi), \qquad H_g(\pi, C) = -\log_2 V_g(\pi, C), \qquad \mathcal L_g(\pi, C) = H_g(\pi) - H_g(\pi, C) = \log_2 \frac{V_g(\pi, C)}{V_g(\pi)}. $$

The **g-capacity** is $\mathcal{ML}_g(C) = \sup_\pi \mathcal L_g(\pi, C)$. As on the other QIF pages, the logarithms are base 2 and the unit is the bit.

**Standard gain functions.**
- *Identity gain.* $\mathcal W = \mathcal X$ and $g_{\mathrm{id}}(w, x) = 1$ if $w = x$, else 0. Then $V_{g_{\mathrm{id}}} = V$ and the g-leakage is the min-entropy leakage (their Proposition 3.1).
- *Metric gain.* For a [metric](/metric-space/) $d$ on $\mathcal X$ normalized to $[0, 1]$, $g_d(w, x) = 1 - d(w, x)$. A guess close to the secret earns almost as much as the exact secret.
- *Binary gain.* Each guess is a set $W \subseteq \mathcal X$ and earns 1 when $x \in W$. With the blocks of a partition as guesses, the attacker wants to learn which block holds the secret. With all sets of at most $k$ secrets, $V_g(\pi)$ is the chance to find the secret within $k$ tries.

**Computation.** With $n$ secrets, $k$ outputs and $m$ guesses, the g-leakage costs $O(nkm)$ arithmetic operations:

```pseudo id=main
G-LEAKAGE(π, C, g)
L1  V0 ← max over w of Σ_x π[x] · g(w, x)
L2  V1 ← 0
L3  for each output y do
L4      V1 ← V1 + max over w of Σ_x π[x] · C[x, y] · g(w, x)
L5  return log2(V1 / V0)
```

The Python implementation uses `fractions.Fraction` and takes the logarithm only at the end. Its tests check the examples below, compare $V_g(\pi, C)$ with an enumeration of all maps from outputs to guesses on 600 random cases, and check the Miracle bound on a grid of priors. The $k$-tries gain is built from the sets of exactly $k$ secrets; for $k \le n$ this gives the same vulnerability as sets of at most $k$, because a larger set never earns less.

**Basic facts.** Each is a theorem from Alvim et al. (2012).
- *Best strategy.* $V_g(\pi, C)$ is the largest expected gain over all strategies $s : \mathcal Y \to \mathcal W$, by the same argument as for min-entropy leakage. A random strategy does no better, since the expected gain is linear in the strategy.
- *Never negative (Theorem 4.1).* $V_g(\pi, C) \ge V_g(\pi)$: the attacker can ignore $y$ and play the best prior guess. So $\mathcal L_g(\pi, C) \ge 0$.
- *Zero leakage (Theorem 4.2).* $\mathcal L_g(\pi, C) = 0$ if and only if one guess $w^\ast$ maximizes $\sum_x \pi(x) C[x, y] g(w, x)$ for every output $y$ at once.
- *Miracle theorem (Theorem 5.1).* For every channel $C$ and every gain function $g$, $\mathcal{ML}_g(C) \le \mathcal{ML}(C) = \log_2 \sum_y \max_x C[x, y]$. The proof replaces $C[x, y]$ by $\max_x C[x, y]$ inside the sum and pulls it out. So the [min-capacity](/min-entropy-leakage-bound/) bounds the leakage for every attacker of this form and every prior. As a corollary, allowing $k$ tries cannot raise the capacity above the one-try capacity (Corollary 5.2).
- *Composition (Theorem 6.2).* If $C_1 = C_2 C_3$ for some channel $C_3$, so that $C_1$ is $C_2$ followed by further processing, then $\mathcal L_g(\pi, C_1) \le \mathcal L_g(\pi, C_2)$ for every prior and every gain function.

## Examples and non-examples

**Example: a near pair of secrets.** This is Example 4 of Alvim et al. Take three secrets, the uniform prior and the channel

| | $y_1$ | $y_2$ |
| --- | --- | --- |
| $x_1$ | 1/2 | 1/2 |
| $x_2$ | 1 | 0 |
| $x_3$ | 0 | 1 |

with the metric gain where $x_2$ and $x_3$ are at distance $0.02$ and every other pair of distinct secrets is at distance 1: so $g(x_2, x_3) = g(x_3, x_2) = 0.98$, $g(w, w) = 1$, and the other gains are 0. The best prior guess is $x_2$ or $x_3$, with $V_g(\pi) = (0 + 1 + 0.98)/3 = 0.66$. After seeing the output, $V_g(\pi, C) = 2/3$, so $\mathcal L_g = \log_2 (2/3 / 0.66) = 0.0145$ bits. The min-entropy leakage of the same channel is 1 bit, about 70 times more. The output separates $x_2$ from $x_3$, which matters to a one-guess attacker but hardly to one who is paid for being close.

**Example: g-leakage above min-entropy leakage.** This is Example 5 of Alvim et al. Take the prior $\pi = (0.6, 0.2, 0.2)$ and the channel with rows $(0.6, 0.4)$, $(0, 1)$ and $(0, 1)$. The best single guess is $x_1$ for both outputs, so the min-entropy leakage is 0. With the gain of the previous example, $V_g(\pi) = 0.6$ and $V_g(\pi, C) = 0.36 + 0.396 = 0.756$, so $\mathcal L_g = \log_2 1.26 = 0.3334$ bits. With the partition gain for the blocks $\{x_1\}$ and $\{x_2, x_3\}$, $V_g(\pi, C) = 0.36 + 0.4 = 0.76$ and $\mathcal L_g = \log_2 (19/15) = 0.3410$ bits. So neither leakage bounds the other for a fixed prior; only the capacities are ordered.

**Example: two tries at the last two bits.** Let $h$ be uniform on $\{0, \ldots, 7\}$ and let the program output $h \bmod 4$. With the 2-tries gain, $V_g(\pi) = 2/8 = 1/4$. Each output leaves two secrets and the attacker tries both, so $V_g(\pi, C) = 1$ and $\mathcal L_g = 2$ bits, the same as the one-try min-entropy leakage. The attacker's success rises from $1/4$ to certainty.

**Non-example: the happy gain.** One guess that earns 1 for every secret gives $V_g(\pi) = V_g(\pi, C) = 1$, so every channel has g-leakage 0. The attacker already has all it wants, so the measure says nothing about the channel.

**Non-example: a gain that is 0 on the support.** If $g(w, x) = 0$ for every $w$ and every $x$ with $\pi(x) > 0$, then $V_g(\pi) = 0$ and the ratio is undefined. Alvim et al. exclude such gain functions; the implementation states $V_g(\pi) > 0$ as a precondition.

**Non-example: a change of scale.** A gain with values in $[0, a]$ instead of $[0, 1]$ is not a new measure: it multiplies both vulnerabilities by $a$, so the g-leakage does not change. Alvim et al. note this in a footnote to Definition 3.2.

## Related definitions

- **[Min-entropy leakage](/min-entropy-leakage/).** The identity gain. Every result on this page applies to it.
- **[Min-capacity bound](/min-entropy-leakage-bound/).** The theorem $\mathcal{ML}(C) = \log_2 \sum_y \max_x C[x, y]$, which the Miracle theorem uses as the bound for every gain function.
- **Shannon leakage and [channel capacity](/channel-capacity/).** The Shannon leakage is the mutual information $H(X) - H(X \mid Y)$, built from [Shannon entropy](/shannon-entropy/). Theorem 5.3 of Alvim et al. shows that the Shannon capacity is at most the min-capacity; its proof uses [Jensen's inequality](/jensens-inequality/).
- **Additive g-leakage.** $V_g(\pi, C) - V_g(\pi)$. Alvim et al. (2014) study its capacities next to those of the multiplicative form on this page.
- **[Loss functions](/loss-function/).** A gain function is a bounded payoff in the sense of decision theory, and the attacker picks the guess of the largest expected payoff. A loss function is the same idea with the sign turned around.
- **[Quantitative information flow](/quantitative-information-flow/).** The field that compares these measures.

## References
