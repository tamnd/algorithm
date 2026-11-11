---
tag: 02QMVF
kind: theorem
slug: asymptotic-equipartition-property
name: Asymptotic equipartition property
aliases:
- AEP
- typical set theorem
- Shannon-McMillan-Breiman theorem
area: compression-and-coding/entropy-coding
level: advanced
summary: For a long output X_1..X_n of a memoryless or ergodic source, -(1/n) log2 p(X_1..X_n) is close to the entropy, so about 2^(nH) typical strings carry almost all of the probability.
prereqs: [shannon-entropy, law-of-large-numbers]
see_also: [source-coding-theorem, entropy-rate, binary-entropy-function, chebyshev-inequality, ergodic-theorem, channel-coding-theorem, slepian-wolf-theorem]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Section 7, Theorem 3 (for an ergodic Markoff source, the sequences of length N split into a high-probability set where log(1/p)/N is close to H and a set of small total probability)
  - paper: doi:10.1214/aoms/1177729028
    title: Brockway McMillan, The basic theorems of information theory, Annals of Mathematical Statistics 24(2), 1953
    locator: The asymptotic equipartition property for stationary ergodic sources, with convergence in mean
  - paper: doi:10.1214/aoms/1177706899
    title: Leo Breiman, The individual ergodic theorem of information theory, Annals of Mathematical Statistics 28(3), 1957
    locator: The main theorem (convergence with probability 1 for a stationary ergodic source on a finite alphabet)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 3 (Theorem 3.1.1, the AEP; Theorem 3.1.2, the typical set; Section 3.2, data compression; Section 3.3, the smallest high-probability set) and Section 16.8 (the Shannon-McMillan-Breiman theorem)
---

The asymptotic equipartition property (AEP) says that a long output of a memoryless source almost surely has a probability close to $2^{-nH}$, where $H$ is the [entropy](/shannon-entropy/) of one symbol. So the $\sigma^n$ possible strings fall into two groups: about $2^{nH}$ *typical* strings, each with probability about $2^{-nH}$ and with total probability close to 1, and the rest, which almost never occur. It is the [law of large numbers](/law-of-large-numbers/) applied to $-\log_2 p(X_i)$. The Shannon-McMillan-Breiman theorem extends it to stationary ergodic sources, with the [entropy rate](/entropy-rate/) in place of $H$. The AEP is the main tool in the proof of the fixed-length [source coding theorem](/source-coding-theorem/).

## Statement

Notation. $\Sigma$ is a finite alphabet of size $\sigma$. $X_1, X_2, \ldots$ is a source with values in $\Sigma$, and $X^n = (X_1, \ldots, X_n)$. Logarithms are base 2. In parts (a) to (d), the model is memoryless: the $X_i$ are independent and each has the law $p$, with entropy $H = H(X_1)$, and $p(x^n) = \prod_i p(x_i)$. In part (e), the model is a stationary ergodic process with entropy rate $H(\mathcal{X})$.

For $\varepsilon > 0$, the **typical set** $A_\varepsilon^{(n)}$ is the set of strings $x^n \in \Sigma^n$ with

$$2^{-n(H + \varepsilon)} \le p(x^n) \le 2^{-n(H - \varepsilon)}.$$

**Theorem.**

- **(a) AEP.** $-\frac{1}{n} \log_2 p(X_1, \ldots, X_n) \to H$ in probability.
- **(b)** $\Pr[X^n \in A_\varepsilon^{(n)}] > 1 - \varepsilon$ for all $n$ large enough.
- **(c)** $|A_\varepsilon^{(n)}| \le 2^{n(H + \varepsilon)}$ for all $n$, and $|A_\varepsilon^{(n)}| \ge (1 - \varepsilon) 2^{n(H - \varepsilon)}$ for all $n$ large enough.
- **(d)** If $0 < \delta < 1$ and $B_n \subseteq \Sigma^n$ has $\Pr[X^n \in B_n] \ge 1 - \delta$ for each $n$, then $\liminf_n \frac{1}{n} \log_2 |B_n| \ge H$.
- **(e) Shannon-McMillan-Breiman.** If $X_1, X_2, \ldots$ is stationary and ergodic, then $-\frac{1}{n} \log_2 p(X_1, \ldots, X_n) \to H(\mathcal{X})$ with probability 1.

## In plain words

Toss a coin that shows heads one time in ten, many times. Almost every long run you see has about one head in ten. Each such run has about the same, very small, chance. The number of such runs is far smaller than the number of all runs, and together they hold almost all of the chance. So, to store a run, it is enough to number the usual runs and to give a short name to each. The other runs almost never happen, and we can treat them in any way. The number of usual runs grows with the length at a rate that the entropy of the coin fixes. The same is true for sources with memory, if they are stable over time and do not mix two kinds of behaviour.

## Proof

The full proof of parts (a) to (d) is in [the proof](proofs/correctness.md). The idea is short. Let $Y_i = -\log_2 p(X_i)$, the [self-information](/self-information/) of the $i$-th symbol. The $Y_i$ are independent, bounded and have mean $H$. Since $p(X^n)$ is a product, $-\frac{1}{n} \log_2 p(X^n)$ is the mean $\frac{1}{n} \sum Y_i$, and the weak law of large numbers (via [Chebyshev's inequality](/chebyshev-inequality/)) gives (a). The typical set is the event that this mean is within $\varepsilon$ of $H$, so (b) is (a) again. For (c), each typical string has probability between $2^{-n(H+\varepsilon)}$ and $2^{-n(H-\varepsilon)}$, and the total probability of the set is between $1 - \varepsilon$ and 1; divide. For (d), a set of probability $1 - \delta$ must meet the typical set in probability at least $1 - \delta - \varepsilon$, and each typical string carries at most $2^{-n(H - \varepsilon)}$.

Part (e) needs more than a law of large numbers, because $-\log_2 p(X_n \mid X^{n-1})$ depends on the whole past. The proof in Cover and Thomas, Section 16.8, is the sandwich argument of Algoet and Cover: it puts $-\frac{1}{n} \log_2 p(X^n)$ between the same quantity for Markov approximations of growing order $k$, which converge by the [ergodic theorem](/ergodic-theorem/), and a limit for the infinite past, and it lets $k \to \infty$. It is not repeated here.

## Consequences

- **Fixed-length coding at rate $H$.** Number the typical strings with $\lceil n(H + \varepsilon) \rceil$ bits and give up on the rest, or send the rest with a flag and $n \lceil \log_2 \sigma \rceil$ bits. The error probability, or the mean extra length, goes to 0. This is the achievability part of the [source coding theorem](/source-coding-theorem/), and part (d) is its converse.
- **Typical strings of a coin.** For a coin with $p(1) = p$, a string with $k$ ones has $-\frac{1}{n} \log_2 p(x^n) = \frac{k}{n} \log_2 \frac{1}{p} + \left(1 - \frac{k}{n}\right) \log_2 \frac{1}{1 - p}$, which depends only on $k$. So the typical set is a union of whole classes of strings with a fixed number of ones, with $k/n$ close to $p$, and its size is a sum of binomial coefficients, close to $2^{n h(p)}$ by the estimate on the [binary entropy function](/binary-entropy-function/) page.
- **Joint typicality.** The same argument applied to pairs $(X_i, Y_i)$ gives jointly typical sets, with about $2^{n H(X, Y)}$ pairs. They are the basis of the random coding proofs of the [channel coding theorem](/channel-coding-theorem/) and of the [Slepian-Wolf theorem](/slepian-wolf-theorem/).
- **Universal coding.** Part (e) is why a code that does not know the law, such as a Lempel-Ziv code, can reach the entropy rate of any stationary ergodic source.

## Tightness

**The typical set for $p(1) = 0.1$ and $\varepsilon = 0.1$.** Here $H = h(0.1) = 0.4690$, so a typical string has $-\frac{1}{n} \log_2 p(x^n)$ in $[0.369, 0.569]$. The code on this page computes the set exactly as a range of numbers of ones, with exact rational arithmetic:

| $n$ | ones in a typical string | $\Pr[A_\varepsilon^{(n)}]$ | $\frac{1}{n} \log_2 \lvert A_\varepsilon^{(n)} \rvert$ |
|---|---|---|---|
| 10 | 1 | 0.3874 | 0.332 |
| 25 | 2 to 3 | 0.4924 | 0.454 |
| 50 | 4 to 6 | 0.5199 | 0.482 |
| 100 | 7 to 13 | 0.7590 | 0.529 |
| 200 | 14 to 26 | 0.8762 | 0.541 |
| 500 | 35 to 65 | 0.97939 | 0.549 |
| 1000 | 69 to 131 | 0.999060 | 0.556 |
| 2000 | 137 to 263 | 0.99999695 | 0.559 |

The table shows three limits of the theorem. First, $n$ must be large: at $n = 50$ the typical set holds only about half of the probability, so part (b) with $\varepsilon = 0.1$ needs $n$ in the hundreds. Second, the size of the set grows at a rate near $H + \varepsilon$, not $H$: the bound $2^{n(H + \varepsilon)}$ of part (c) is close to the truth for a fixed $\varepsilon$, and a rate of exactly $H$ needs $\varepsilon \to 0$. Third, the convergence in (b) is fast once it starts; the Chebyshev bound of the proof is weak, and a Chernoff bound shows that $1 - \Pr[A_\varepsilon^{(n)}]$ decreases exponentially in $n$.

**The typical set is not the set of the most likely strings.** The single most likely string is all zeros, with probability $0.9^n = 2^{-0.152 n}$, which is far above $2^{-n(H - \varepsilon)}$. It is not typical, and neither is any string with too few ones. Each such string is likely, but there are few of them, so together they have small probability. Part (d) says this does not matter for the size: the smallest set of probability $1 - \delta$ also has about $2^{nH}$ strings.

**The source must be ergodic.** Choose once, at random, a coin with $p(1) = 0.1$ or a fair coin, and toss it forever. This source is stationary but not ergodic. On the runs of the first coin, $-\frac{1}{n} \log_2 p(X^n)$ tends to $0.469$; on the runs of the fair coin it tends to 1. The limit is a random variable, not a constant, and no single rate describes the source.

**The alphabet.** The explicit bound in the proof uses a finite variance of $\log_2 p(X_1)$, which a finite alphabet gives. For a countable alphabet with finite $H$, the $Y_i$ still have the finite mean $H$, and Khinchin's weak law of large numbers still gives (a), (b) and (c); only the rate of convergence is lost.

## History

Shannon stated the property for ergodic Markov sources as Theorem 3 of his 1948 paper, in Section 7, and used it for his coding theorems. McMillan (1953) proved it for every stationary ergodic source on a finite alphabet, with convergence in mean, which gives convergence in probability, and gave it the name *asymptotic equipartition property*: in the limit, the probability is spread equally over the typical strings. Breiman (1957) proved convergence with probability 1, which is part (e). The theorem is now called the Shannon-McMillan-Breiman theorem. Algoet and Cover (1988) gave the short sandwich proof used in Cover and Thomas.

## References
