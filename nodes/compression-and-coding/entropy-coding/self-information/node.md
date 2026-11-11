---
tag: 10AS4N
kind: definition
slug: self-information
name: Self-information
aliases:
- information content
- surprisal
area: compression-and-coding/entropy-coding
level: intro
summary: The information of one outcome, I(x) = -log2 p(x) bits. It adds over independent events, its mean is the entropy, and it is the ideal code length of x.
prereqs: [discrete-probability-distribution]
see_also: [shannon-entropy, arithmetic-coding, kraft-inequality, source-coding-theorem, cross-entropy-loss, min-entropy]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Section 6 (Choice, uncertainty and entropy) and the introduction, on the logarithmic measure of information
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 2.1 (entropy as the expected value of log 1/p(X)) and Section 5.4 (ideal code lengths log 1/p(x))
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Section 2.4 (the Shannon information content of an outcome) and Chapter 4
---

The self-information of an outcome $x$ of probability $p(x)$ is $I(x) = -\log_2 p(x)$ bits. A rare outcome carries much information and a sure outcome carries none. Self-information is a property of one outcome; [Shannon entropy](/shannon-entropy/) is its mean over all outcomes. In compression, $I(x)$ is the ideal length of the codeword for $x$, and [arithmetic coding](/arithmetic-coding/) reaches it to within 2 bits for a whole message.

## Definition

Notation. $\Sigma$ is a finite alphabet of size $\sigma$, $X$ is a random variable on $\Sigma$, and $p(x) = \Pr[X = x]$. Logarithms are base 2, so the unit is the bit; with the natural logarithm the unit is the nat. The model is a known probability law; for a message it is a memoryless source with law $p$, or any model that gives each symbol a probability given the symbols before it.

**Definition.** For an outcome $x$ with $p(x) > 0$,

$$I(x) = \log_2 \frac{1}{p(x)} = -\log_2 p(x).$$

$I(x) \ge 0$, with equality only when $p(x) = 1$, and $I(x) \to \infty$ as $p(x) \to 0$.

**Additivity.** If $x$ and $y$ are outcomes of independent variables, $I(x, y) = -\log_2 (p(x) p(y)) = I(x) + I(y)$. For a message $x_1 \cdots x_n$ from any model, the chain rule of probability gives

$$I(x_1 \cdots x_n) = \sum_{i=1}^{n} -\log_2 p(x_i \mid x_1 \cdots x_{i-1}),$$

so the information of a message is the sum of the information of its symbols, each one given the symbols before it. A logarithm is the only continuous function of $p$ that turns products of independent probabilities into sums, up to the base.

**Entropy as the expected value.** $H(X) = \mathbb{E}[I(X)] = \sum_x p(x) I(x)$. Entropy is a number for a source; self-information is a random variable, a value for each outcome.

**Ideal code length.** A code that gives $x$ a codeword of length $\ell(x) = \lceil I(x) \rceil$ exists as a [prefix code](/prefix-code/), because $\sum_x 2^{-\lceil I(x) \rceil} \le \sum_x p(x) = 1$ and the [Kraft inequality](/kraft-inequality/) then gives the code. Its mean length is less than $H(X) + 1$. On a whole message, arithmetic coding gives the message an interval of width $p(x_1 \cdots x_n) = 2^{-I}$. A dyadic interval of width $2^{-\ell}$ fits inside it when $\ell \ge \lceil I \rceil + 1$, so the message needs at most $\lceil I \rceil + 1$ bits, which is less than $I + 2$. No lossless code does better on average than the mean of $I$, which is the [source coding theorem](/source-coding-theorem/).

## Examples and non-examples

**Single outcomes.**

| event | $p$ | $I$ in bits |
|---|---|---|
| a fair coin lands heads | $1/2$ | 1 |
| one card from a deck of 52 | $1/52$ | 5.70 |
| ten fair coins all land heads | $2^{-10}$ | 10 |
| a sure event | 1 | 0 |
| one outcome of probability 0.999 | 0.999 | 0.00144 |

**A message and its arithmetic code.** Take the model $p(a) = 1/2$, $p(b) = 1/4$, $p(c) = 1/4$ and the message $abac$. By additivity, $I = 1 + 2 + 1 + 2 = 6$ bits. Arithmetic coding with the symbols in the order $a, b, c$ narrows $[0, 1)$ to $[0, 1/2)$, then $[1/4, 3/8)$, then $[1/4, 5/16)$, then $[19/64, 20/64)$. The width is $1/64 = 2^{-6}$, the same as $2^{-I}$. Here the interval is itself dyadic, so the 6 bits $010011$ (the binary digits of $19/64$) name it, and the code length equals the ideal length. In general the length is between $I$ and $\lceil I \rceil + 1$; the code on this page checks this bound on random messages.

**Non-examples.**

- Self-information is not a property of the value. The outcome "rain" has 1 bit of information under a model that gives it probability $1/2$ and 6.6 bits under a model that gives it $1/100$. Change the model and $I$ changes.
- A long string is not more informative than a short one by length alone. Under a model with $p(0) = 0.99$, the string of 100 zeros has $I = 1.45$ bits, less than the single symbol 1, which has $I = 6.64$ bits.
- $I(x) = -\log_2 p(x)$ for an event of probability 0 is not defined; such an event does not occur and gets no codeword.
- The mean of $I$ under a different law $q$, $-\sum_x q(x) \log_2 p(x)$, is the cross entropy, not the entropy of either law.

## Related definitions

- [Shannon entropy](/shannon-entropy/) is the expected self-information.
- [Min-entropy](/min-entropy/) is the smallest self-information of any outcome, $\min_x I(x) = -\log_2 \max_x p(x)$.
- [Cross-entropy loss](/cross-entropy-loss/) is the mean self-information of the data under a model; training a model to lower it is the same as asking for shorter ideal code lengths.
- Pointwise mutual information, $\log_2 \frac{p(x, y)}{p(x) p(y)} = I(x) - I(x \mid y)$, is the drop in self-information of $x$ when $y$ is known; its mean is the mutual information of [conditional entropy](/conditional-entropy/).
- The [Kraft inequality](/kraft-inequality/) turns the lengths $\lceil I(x) \rceil$ into a code (the Shannon code).

## References
