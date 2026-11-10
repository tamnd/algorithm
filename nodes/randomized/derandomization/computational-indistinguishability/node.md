---
tag: SBVWAV
kind: definition
slug: computational-indistinguishability
name: Computational indistinguishability
aliases:
- pseudorandomness against bounded tests
area: randomized/derandomization
level: advanced
summary: Two distributions are computationally indistinguishable if every efficient test has negligible advantage in telling them apart. Hybrid arguments prove most facts about it.
prereqs: [total-variation-distance, boolean-circuit, probabilistic-turing-machine]
see_also: [pseudorandom-generator, pseudorandom-generation, yao-next-bit-unpredictability, hybrid-argument, semantic-security, goldwasser-micali-cryptosystem, randomness-extractor, one-way-function]
sources:
  - paper: doi:10.1016/0022-0000(84)90070-9
    title: Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), 1984
    locator: the definition of polynomial-time indistinguishability of the encryptions of two messages, and the hybrid proof for many bits
  - paper: doi:10.1109/SFCS.1982.45
    title: Andrew C. Yao, Theory and applications of trapdoor functions, 23rd IEEE Symposium on Foundations of Computer Science (FOCS), 1982
    locator: indistinguishability of distributions by polynomial-time statistical tests
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 3, Section 3.2 (computational indistinguishability, the hybrid technique, indistinguishability by repeated samples)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 7 (computational indistinguishability and hybrid arguments)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 9, Cryptography (computational security and the hybrid argument)
---

Two distributions are *computationally indistinguishable* when every efficient test accepts them with almost the same probability: the difference, the advantage, is negligible. Goldwasser and Micali defined it in 1984 to say what secure encryption means, and Yao used it in 1982 for [pseudorandom generators](/pseudorandom-generator/). The main tool for proofs about it is the *hybrid argument*: a chain of distributions between the two ends, where a test that tells the ends apart must tell some neighbors apart. This page gives the definition and proves the hybrid argument; [Yao's theorem](/yao-next-bit-unpredictability/) and the stretch extension on [pseudorandom generator](/pseudorandom-generator/) are its main uses.

## Definition

Notation: $U_m$ is the uniform distribution on $\{0,1\}^m$; $\Pr$ and $E$ are probability and expectation. For distributions $X, Y$ on $\{0,1\}^m$ and a test $D : \{0,1\}^m \to \{0,1\}$, the *advantage* of $D$ is

$$\operatorname{adv}_D(X, Y) = \big| \Pr[D(X) = 1] - \Pr[D(Y) = 1] \big|.$$

**Statistical distance.** $\Delta(X, Y) = \max_{T \subseteq \{0,1\}^m} |\Pr[X \in T] - \Pr[Y \in T]| = \frac12 \sum_z |\Pr[X = z] - \Pr[Y = z]|$. This is the [total variation distance](/total-variation-distance/). It is the advantage of the best test with no bound on its cost.

**Concrete form.** $X$ and $Y$ are *$(t, \varepsilon)$-indistinguishable* if $\operatorname{adv}_D(X, Y) \le \varepsilon$ for every [Boolean circuit](/boolean-circuit/) $D$ of size at most $t$.

**Asymptotic form.** Let $X = \{X_n\}$ and $Y = \{Y_n\}$ be ensembles, where $X_n$ and $Y_n$ are distributions on $\{0,1\}^{\ell(n)}$ and $\ell$ is a polynomial. A function $\nu(n)$ is *negligible* if $\nu(n) < 1/p(n)$ for each polynomial $p$ and all large enough $n$. Then:

- $X$ and $Y$ are *computationally indistinguishable*, written $X \approx_c Y$, if for every [probabilistic](/probabilistic-turing-machine/) polynomial-time algorithm $D$, the advantage $|\Pr[D(1^n, X_n) = 1] - \Pr[D(1^n, Y_n) = 1]|$ is negligible. The *non-uniform* version asks the same for every family of circuits of polynomial size.
- They are *statistically indistinguishable* if $\Delta(X_n, Y_n)$ is negligible.
- $X$ is *pseudorandom* if $X \approx_c \{U_{\ell(n)}\}$.

### Basic facts

**Fact 1 (statistical bounds computational).** For every test $D$, $\operatorname{adv}_D(X, Y) \le \Delta(X, Y)$, with equality for $D = $ the indicator of $T^* = \{z : \Pr[X = z] > \Pr[Y = z]\}$. *Proof.* With $T = D^{-1}(1)$, the advantage is $|\Pr[X \in T] - \Pr[Y \in T]|$, which is at most the maximum over all $T$. The sum $\Pr[X \in T] - \Pr[Y \in T] = \sum_{z \in T} (\Pr[X = z] - \Pr[Y = z])$ is largest when $T$ holds exactly the $z$ with a positive term, which is $T^*$. Since both distributions sum to 1, the positive terms sum to half of $\sum_z |\Pr[X=z] - \Pr[Y=z]|$. $\square$

**Fact 2 (efficient maps).** If $X \approx_c Y$ and $f$ is computable in polynomial time, then $f(X) \approx_c f(Y)$, because $D \circ f$ is a test for $X$ and $Y$ with the same advantage.

**Fact 3 (triangle inequality).** For each $D$, $\operatorname{adv}_D(X, Z) \le \operatorname{adv}_D(X, Y) + \operatorname{adv}_D(Y, Z)$. So a chain of a constant or polynomial number of indistinguishable steps is indistinguishable. A chain of exponential length is not covered.

### The hybrid argument

**Lemma (hybrids).** Let $H_0, H_1, \ldots, H_k$ be distributions and $D$ a test, and let $p_i = \Pr[D(H_i) = 1]$. Then

$$p_k - p_0 = \sum_{i=1}^{k} (p_i - p_{i-1}),$$

so some $i$ has $|p_i - p_{i-1}| \ge |p_k - p_0| / k$, and the average of $p_i - p_{i-1}$ over a uniform $i \in \{1, \ldots, k\}$ is exactly $(p_k - p_0)/k$.

*Proof.* The sum telescopes: each $p_i$ with $0 < i < k$ appears once with a plus sign and once with a minus sign. If each term had absolute value less than $|p_k - p_0|/k$, the triangle inequality would give $|p_k - p_0| < k \cdot |p_k - p_0|/k$, which is false. The average is the sum divided by $k$. $\square$

**Theorem (many samples).** Let $X = \{X_n\}$ and $Y = \{Y_n\}$ be computationally indistinguishable, and assume that both can be sampled in polynomial time. Then for each polynomial $k = k(n)$, the $k$ independent samples $X_n^{k} = (X^{(1)}, \ldots, X^{(k)})$ and $Y_n^{k} = (Y^{(1)}, \ldots, Y^{(k)})$ are computationally indistinguishable.

*Proof.* Let $D$ be a polynomial-time test with advantage $\delta(n)$ on $X_n^k$ and $Y_n^k$. Let $H_i$ be $i$ independent samples of $X_n$ followed by $k - i$ independent samples of $Y_n$. Then $H_k = X_n^k$ and $H_0 = Y_n^k$. Build a test $D'$ for one sample: on input $z$, pick $i$ uniform in $\{1, \ldots, k\}$, draw $x_1, \ldots, x_{i-1}$ from $X_n$ and $y_{i+1}, \ldots, y_k$ from $Y_n$, and output $D(x_1, \ldots, x_{i-1}, z, y_{i+1}, \ldots, y_k)$. If $z$ comes from $X_n$, the input to $D$ has the distribution $H_i$; if $z$ comes from $Y_n$, it has the distribution $H_{i-1}$. So

$$\Pr[D'(X_n) = 1] - \Pr[D'(Y_n) = 1] = \frac1k \sum_{i=1}^k (p_i - p_{i-1}) = \frac{p_k - p_0}{k},$$

whose absolute value is $\delta(n)/k(n)$. $D'$ runs in polynomial time because sampling is efficient. If $\delta$ were not negligible, $\delta/k$ would not be negligible, which contradicts $X \approx_c Y$. $\blacksquare$

In the non-uniform version the samples are not needed at run time: fix the $i$ and the samples that give the largest advantage, and build them into the circuit. Then the assumption that $X$ and $Y$ can be sampled can be dropped.

## Examples and non-examples

**A hybrid chain computed exactly.** Let $G(a, b) = (a \lor b,\ a \land b,\ a \oplus b)$ map 2 bits to 3 bits, and let $D$ be the majority of the 3 bits. Let $H_i$ be the first $i$ bits of $G(U_2)$ followed by $3 - i$ uniform bits, so $H_0 = U_3$ and $H_3 = G(U_2)$.

| $i$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $p_i = \Pr[D(H_i) = 1]$ | 1/2 | 5/8 | 1/2 | 3/4 |
| $p_i - p_{i-1}$ |  | 1/8 | −1/8 | 1/4 |

The gaps sum to $1/4 = p_3 - p_0$, the advantage of $D$. One gap is negative, so gaps can cancel; the largest gap, $1/4$, is at least the average $1/12$. Yao's predictor built from step $i = 3$ guesses the third bit from the first two with success $1/2 + p_3 - p_2 = 3/4$. The statistical distance is larger than this advantage: $G(U_2)$ gives $000$ weight $1/4$, $101$ weight $1/2$ and $110$ weight $1/4$, so $\Delta(G(U_2), U_3) = 5/8$, reached by the test "is $z$ one of $000, 101, 110$?".

**Encryption.** Goldwasser and Micali call an encryption scheme secure when, for each pair of messages, the encryptions of the two are computationally indistinguishable ([semantic security](/semantic-security/)). The hybrid argument then gives security for messages of many bits from security for one bit. The [Goldwasser-Micali cryptosystem](/goldwasser-micali-cryptosystem/) encrypts bit by bit in this way.

**Pseudorandom but statistically far.** If $G : \{0,1\}^n \to \{0,1\}^{n+1}$ is a pseudorandom generator, then $G(U_n) \approx_c U_{n+1}$, but $\Delta(G(U_n), U_{n+1}) \ge 1/2$, because the image of $G$ has at most $2^n$ of the $2^{n+1}$ strings. So computational indistinguishability is strictly weaker than statistical indistinguishability, if generators exist.

**Non-examples.**

- An advantage of $1/n^{10}$ is not negligible. Two ensembles with this advantage are distinguishable, even though the gap is tiny for every practical $n$. The asymptotic definition asks for a bound below every inverse polynomial.
- $(s, s)$ for uniform $s$ and $U_{2n}$: the test "are the halves equal?" has advantage $1 - 2^{-n}$.
- The hybrid argument with $k = 2^n$ steps proves nothing: the advantage per step may be $2^{-n}$ times the total, which is negligible even when the total advantage is large.

**Common errors.**

- **Fixing $i$ in a uniform reduction.** The index with a large gap may depend on $n$ in a way that no algorithm can compute. A uniform reduction picks $i$ at random and loses the factor $k$; only a non-uniform reduction can fix the best $i$.
- **Forgetting samplability.** The many-samples theorem needs efficient sampling of $X$ and $Y$ in the uniform setting. Without it the reduction cannot fill in the other positions.
- **Mixing the sign.** The hybrid gaps are signed. Take absolute values only at the end, as in the lemma.

## Related definitions

- [Pseudorandom generator](/pseudorandom-generator/): a function whose output on a uniform seed is pseudorandom.
- [Yao's next-bit theorem](/yao-next-bit-unpredictability/): the hybrid argument applied to the bits of one string, which shows that pseudorandom is the same as next-bit unpredictable.
- [Pseudorandom generation](/pseudorandom-generation/): the kinds of tests (efficient algorithms, circuits, small space, linear tests) for which one asks for indistinguishability.
- [Hybrid argument](/hybrid-argument/): the proof technique in general, also used in communication complexity and quantum query lower bounds.
- [Randomness extractor](/randomness-extractor/): the statistical counterpart, where the output must be close to uniform in statistical distance.
- [Semantic security](/semantic-security/) and the [one-way function](/one-way-function/): the cryptographic definitions built on this notion.

## References
