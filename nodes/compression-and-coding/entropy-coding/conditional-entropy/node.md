---
tag: 70YZ8M
kind: definition
slug: conditional-entropy
name: Conditional entropy
aliases:
- equivocation
area: compression-and-coding/entropy-coding
level: intro
summary: H(X|Y), the entropy of X that is left when Y is known. With the chain rule and mutual information it measures how much one variable tells about another.
prereqs: [shannon-entropy, conditional-probability]
see_also: [slepian-wolf-theorem, entropy-rate, self-information, channel-capacity, channel-coding-theorem, jensens-inequality, markov-chain]
sources:
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 2.2 (joint and conditional entropy, the chain rule), Section 2.4 (mutual information), Section 2.6 (conditioning reduces entropy, Example 2.6.1) and Section 2.8 (data processing inequality)
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Section 6 (the conditional entropy H_x(y) and the inequality H(x, y) <= H(x) + H(y)) and Section 12 (equivocation)
---

The conditional entropy $H(X \mid Y)$ is the uncertainty about $X$ that is left after $Y$ is known: the [entropy](/shannon-entropy/) of $X$ under the law of $X$ given $Y = y$, averaged over $y$. The chain rule $H(X, Y) = H(Y) + H(X \mid Y)$ splits a joint entropy into steps, and the drop $H(X) - H(X \mid Y)$ is the mutual information. In compression, $H(X \mid Y)$ is the number of bits per symbol for $X$ when the decoder already has $Y$; the [Slepian-Wolf theorem](/slepian-wolf-theorem/) says this is enough even when the encoder does not have $Y$.

## Definition

Notation. $X$ takes values in a finite alphabet $\Sigma_X$ and $Y$ in $\Sigma_Y$. The model is one joint law $p(x, y)$, with marginals $p(x) = \sum_y p(x, y)$ and $p(y) = \sum_x p(x, y)$, and $p(x \mid y) = p(x, y) / p(y)$ when $p(y) > 0$. Logarithms are base 2 and $0 \log 0 = 0$.

**Definition.**

$$H(X \mid Y = y) = -\sum_x p(x \mid y) \log_2 p(x \mid y),$$

$$H(X \mid Y) = \sum_y p(y) \, H(X \mid Y = y) = -\sum_{x, y} p(x, y) \log_2 p(x \mid y) = \mathbb{E}\left[\log_2 \frac{1}{p(X \mid Y)}\right].$$

The joint entropy is $H(X, Y) = -\sum_{x, y} p(x, y) \log_2 p(x, y)$, the entropy of the pair as one variable.

**Chain rule.** $H(X, Y) = H(Y) + H(X \mid Y) = H(X) + H(Y \mid X)$. More generally, $H(X_1, \ldots, X_n) = \sum_{i=1}^{n} H(X_i \mid X_1, \ldots, X_{i-1})$.

*Proof.* $\log_2 p(x, y) = \log_2 p(y) + \log_2 p(x \mid y)$ for every pair with $p(x, y) > 0$. Multiply by $-p(x, y)$ and sum over $x, y$; the first term sums to $H(Y)$ because $\sum_x p(x, y) = p(y)$. The general form follows by induction on $n$. $\square$

**Mutual information.**

$$I(X; Y) = H(X) - H(X \mid Y) = H(Y) - H(Y \mid X) = H(X) + H(Y) - H(X, Y) = \sum_{x, y} p(x, y) \log_2 \frac{p(x, y)}{p(x) p(y)}.$$

The three forms agree by the chain rule. $I(X; Y)$ is symmetric, and $I(X; X) = H(X)$.

**Conditioning reduces entropy, on average.** $I(X; Y) \ge 0$, so $H(X \mid Y) \le H(X)$, with equality if and only if $X$ and $Y$ are independent.

*Proof.* Over the pairs with $p(x, y) > 0$, $-I(X; Y) = \sum p(x, y) \log_2 \frac{p(x) p(y)}{p(x, y)} \le \log_2 \sum p(x, y) \frac{p(x) p(y)}{p(x, y)} \le \log_2 1 = 0$, by [Jensen's inequality](/jensens-inequality/) for the concave $\log$. Equality in Jensen needs $p(x) p(y) / p(x, y)$ to be constant on the pairs with $p(x, y) > 0$, and equality in the last step needs those pairs to carry all of the mass of $p(x) p(y)$. Together these say $p(x, y) = p(x) p(y)$ everywhere. $\square$

The inequality is about the average over $y$. For one value $y$, $H(X \mid Y = y)$ can be larger than $H(X)$; the example below shows this.

**Data processing inequality.** If $X \to Y \to Z$ is a Markov chain, that is, $Z$ depends on $X$ only through $Y$, then $I(X; Z) \le I(X; Y)$. The chain rule for mutual information gives $I(X; Y, Z) = I(X; Z) + I(X; Y \mid Z) = I(X; Y) + I(X; Z \mid Y)$, and $I(X; Z \mid Y) = 0$ by the Markov property, while $I(X; Y \mid Z) \ge 0$. So no processing of $Y$, deterministic or random, gives more information about $X$ than $Y$ has. In particular $H(X \mid g(Y)) \ge H(X \mid Y)$ for every function $g$.

## Examples and non-examples

**Conditioning on one value can raise the entropy.** This is Example 2.6.1 of Cover and Thomas. Let $X, Y \in \{1, 2\}$ with

| | $Y = 1$ | $Y = 2$ |
|---|---|---|
| $X = 1$ | 0 | 1/8 |
| $X = 2$ | 3/4 | 1/8 |

Then $p(X = 1) = 1/8$, so $H(X) = h(1/8) = 0.5436$ bits, with $h$ the [binary entropy function](/binary-entropy-function/). If $Y = 1$ (probability $3/4$), $X = 2$ for sure, so $H(X \mid Y = 1) = 0$. If $Y = 2$ (probability $1/4$), $X$ is uniform, so $H(X \mid Y = 2) = 1 > H(X)$. On average, $H(X \mid Y) = \frac{3}{4} \cdot 0 + \frac{1}{4} \cdot 1 = 0.25 \le 0.5436$. The other quantities are $H(Y) = h(1/4) = 0.8113$, $H(X, Y) = 1.0613 = H(Y) + H(X \mid Y)$, and $I(X; Y) = 0.5436 - 0.25 = 0.2936$ bits. The code on this page computes all of these from the table and checks the chain rule.

**Two extremes.** If $X = f(Y)$ for a function $f$, then $H(X \mid Y) = 0$. If $X$ and $Y$ are independent, $H(X \mid Y) = H(X)$.

**A channel.** Send a uniform bit $X$ over a [binary symmetric channel](/binary-symmetric-channel/) that flips it with probability $p$, and call the output $Y$. Then $H(X \mid Y) = h(p)$ (Shannon called this the equivocation) and $I(X; Y) = 1 - h(p)$, which is the [channel capacity](/channel-capacity/).

**Non-examples.**

- $H(X \mid Y)$ is not the entropy of $X$ given one fixed value of $Y$. That is $H(X \mid Y = y)$, a different number for each $y$.
- $H(X \mid Y) \ne H(Y \mid X)$ in general. In the table above, $H(Y \mid X) = H(X, Y) - H(X) = 0.5177$, not 0.25.
- Conditional entropy is not the entropy of a "conditional variable" $X - Y$ or $X / Y$. It is defined from the joint law, not from any operation on the values.
- Pairwise independence of $X$ from $Y$ and from $Z$ does not give $H(X \mid Y, Z) = H(X)$. For $X = Y \oplus Z$ with $Y, Z$ independent fair bits, $X$ is independent of $Y$ and of $Z$, but $H(X \mid Y, Z) = 0$.

## Related definitions

- [Shannon entropy](/shannon-entropy/) is the case where $Y$ is a constant.
- The [entropy rate](/entropy-rate/) of a stationary source is the limit of $H(X_n \mid X_1, \ldots, X_{n-1})$, the conditional entropy of the next symbol given the past.
- The [Slepian-Wolf theorem](/slepian-wolf-theorem/) gives $H(X \mid Y)$ its meaning as a compression rate with side information at the decoder.
- The [channel coding theorem](/channel-coding-theorem/) uses the maximum of $I(X; Y)$ over input laws, which is the channel capacity.
- The conditional form of [self-information](/self-information/), $-\log_2 p(x \mid y)$, has $H(X \mid Y)$ as its mean.
- The relative entropy $D(p \| q) = \sum_x p(x) \log_2 \frac{p(x)}{q(x)}$ is the general form; $I(X; Y)$ is the relative entropy of $p(x, y)$ from $p(x) p(y)$.

## References
