---
tag: 9RVWGF
kind: theorem
slug: yao-next-bit-unpredictability
name: Yao's next-bit unpredictability theorem
aliases:
- Yao's next-bit test
- next-bit test equivalence
area: randomized/derandomization
level: advanced
summary: A distribution on m-bit strings is pseudorandom exactly when no efficient predictor guesses a bit from the earlier bits much better than chance. Advantage ε gives a predictor with ε/m.
prereqs: [computational-indistinguishability, pseudorandom-generator, boolean-circuit]
see_also: [hybrid-argument, hill-prg-from-one-way-functions, blum-micali, cryptographically-secure-prng, nisan-wigderson-generator, hard-core-predicate, pseudorandom-generation]
sources:
  - paper: doi:10.1109/SFCS.1982.45
    title: Andrew C. Yao, Theory and applications of trapdoor functions, 23rd IEEE Symposium on Foundations of Computer Science (FOCS), 1982
    locator: the theorem that a generator that passes the next-bit test passes all polynomial-time statistical tests
  - paper: doi:10.1137/0213053
    title: Manuel Blum and Silvio Micali, How to generate cryptographically strong sequences of pseudo-random bits, SIAM Journal on Computing 13(4), 1984
    locator: the next-bit test as the definition of a cryptographically strong generator
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 3 (pseudorandomness and unpredictability, with the proof by hybrids)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 9 (Yao's theorem on unpredictability) and Chapter 20 (its use in the Nisan-Wigderson proof)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 7 (next-bit unpredictability and hybrid arguments)
---

Yao's theorem says that a distribution on $m$-bit strings is [pseudorandom](/pseudorandom-generator/) exactly when it is *next-bit unpredictable*: no efficient predictor, given the first $i - 1$ bits, guesses bit $i$ with probability much above $1/2$. One direction is direct. The other is a [hybrid argument](/computational-indistinguishability/): a test with advantage $\varepsilon$ gives a predictor for some position with advantage $\varepsilon/m$. The theorem lets one prove a generator secure by looking at one bit at a time, which is how the [Blum-Micali](/blum-micali/) generator and the [Nisan-Wigderson generator](/nisan-wigderson-generator/) are analyzed.

## Statement

Notation: $U_m$ is the uniform distribution on $\{0,1\}^m$. Let $Y = (Y_1, \ldots, Y_m)$ be any distribution on $\{0,1\}^m$, for example $Y = G(U_d)$ for a generator $G$. Write $Y_{<i}$ for $(Y_1, \ldots, Y_{i-1})$. Circuits are [Boolean circuits](/boolean-circuit/) with gates AND, OR and NOT.

**Theorem (concrete form).**

1. *From a test to a predictor.* If a circuit $D$ of size $t$ has $|\Pr[D(Y) = 1] - \Pr[D(U_m) = 1]| \ge \varepsilon$, then there are a position $i \in \{1, \ldots, m\}$ and a circuit $P$ of size at most $t + 2$ with
$$\Pr[P(Y_{<i}) = Y_i] \ge \frac12 + \frac{\varepsilon}{m}.$$
2. *From a predictor to a test.* If a circuit $P$ of size $t$ has $\Pr[P(Y_{<i}) = Y_i] \ge \frac12 + \delta$ for some $i$, then a circuit $D$ of size $t + O(1)$ has $\Pr[D(Y) = 1] - \Pr[D(U_m) = 1] \ge \delta$.

**Theorem (asymptotic form).** Let $G = \{G_n : \{0,1\}^n \to \{0,1\}^{\ell(n)}\}$ be computable in polynomial time. Then $G$ is a pseudorandom generator if and only if, for every probabilistic polynomial-time predictor $A$, with $i$ uniform in $\{1, \ldots, \ell(n)\}$ and $Y = G_n(U_n)$, the quantity $\Pr[A(1^n, i, Y_{<i}) = Y_i] - \frac12$ is negligible. The same holds with circuits in place of algorithms.

## In plain words

Suppose some program can tell the output of a generator from true random bits. Yao's theorem says that then some program can also guess one output bit from the bits before it, a little better than a coin flip.

The proof changes the random string into the generator's string one bit at a time. The first string is fully random, the last is the generator's output, and the ones in between are mixes. The tester behaves differently on the two ends, so it must behave differently on two neighbors in the chain. Two neighbors differ only in one bit, so the tester's behavior there can be turned into a guess for that bit. The total difference is shared among all the steps, so the guess is better than chance by at least the total difference divided by the number of bits.

## Proof

**Part 2.** Let $D(y) = 1$ when $P(y_{<i}) = y_i$; this adds one equality gate, of constant size. On $Y$, $\Pr[D(Y) = 1] = \Pr[P(Y_{<i}) = Y_i] \ge \frac12 + \delta$. On $U_m$, bit $i$ is uniform and independent of the bits before it, so $\Pr[D(U_m) = 1] = \frac12$ exactly. The difference is at least $\delta$.

**Part 1.** If $\Pr[D(Y) = 1] - \Pr[D(U_m) = 1] \le -\varepsilon$, replace $D$ by its negation, at the cost of one NOT gate. So assume $\Pr[D(Y) = 1] - \Pr[D(U_m) = 1] \ge \varepsilon$, with $D$ of size at most $t + 1$.

*Hybrids.* For $i = 0, \ldots, m$ let $H_i = (Y_1, \ldots, Y_i, R_{i+1}, \ldots, R_m)$, where $R_1, \ldots, R_m$ are uniform bits, independent of each other and of $Y$. Then $H_0 = U_m$ and $H_m = Y$. Let $p_i = \Pr[D(H_i) = 1]$. Since $p_m - p_0 = \sum_{i=1}^m (p_i - p_{i-1}) \ge \varepsilon$, some $i$ has $p_i - p_{i-1} \ge \varepsilon/m$. Fix this $i$.

*The predictor.* On input $y_{<i}$, the randomized predictor draws $R_i, \ldots, R_m$ and computes $b = D(y_{<i}, R_i, R_{i+1}, \ldots, R_m)$. It outputs $R_i$ if $b = 1$ and $1 - R_i$ if $b = 0$.

*Its success.* Let $E$ be the event $R_i = Y_i$. $R_i$ is independent of $(Y, R_{i+1}, \ldots, R_m)$, so $\Pr[E] = \frac12$, and given $E$ the input to $D$ has the distribution $H_i$. Given not $E$, the input is $(Y_{<i}, 1 - Y_i, R_{>i})$; let $q = \Pr[D(Y_{<i}, 1 - Y_i, R_{>i}) = 1]$. The input of $D$ in $H_{i-1}$ is the mixture of these two cases with weights $\frac12$ each, so

$$p_{i-1} = \tfrac12 p_i + \tfrac12 q, \qquad\text{that is,}\qquad q = 2p_{i-1} - p_i.$$

The predictor is right when $E$ holds and $b = 1$, or when $E$ fails and $b = 0$. Hence

$$\Pr[\text{right}] = \tfrac12 p_i + \tfrac12 (1 - q) = \tfrac12 p_i + \tfrac12 - p_{i-1} + \tfrac12 p_i = \frac12 + p_i - p_{i-1} \ge \frac12 + \frac{\varepsilon}{m}.$$

*Removing the randomness.* The success is an average over the values of $(R_i, \ldots, R_m)$, so some fixed value $(r_i, \ldots, r_m)$ does at least as well. With these values built in, the predictor is $D(y_{<i}, r_i, \ldots, r_m)$ when $r_i = 1$ and its negation when $r_i = 0$. Its size is at most $t + 2$. This proves part 1.

**Asymptotic form.** A predictor gives a test by part 2, run at a random $i$. For the other direction, run the construction of part 1 with $i$ drawn uniformly, as a uniform algorithm that also draws $R_i, \ldots, R_m$. By the computation above, its success at position $i$ is $\frac12 + p_i - p_{i-1}$, and the average over $i$ is $\frac12 + (p_m - p_0)/m$. If the test has an advantage that is not negligible, so has the predictor, because $m = \ell(n)$ is a polynomial. $\blacksquare$

**A check on numbers.** For $G(a, b) = (a \lor b, a \land b, a \oplus b)$ and $D = $ majority, the hybrid probabilities are $p = (1/2, 5/8, 1/2, 3/4)$. The predictor at $i = 3$ succeeds with probability exactly $1/2 + 3/4 - 1/2 = 3/4$, and the one at $i = 2$ with $1/2 + 1/2 - 5/8 = 3/8$, which is below $1/2$. A negative gap gives a predictor worse than chance, and its negation is better than chance.

## Consequences

- **Generators from hard-core bits.** If $f$ is a one-way permutation with [hard-core predicate](/hard-core-predicate/) $b$, then $(f(x), b(x))$ is pseudorandom: the first $n$ bits are exactly uniform, so no predictor gains there, and a predictor for the last bit predicts $b(x)$ from $f(x)$. This is the step that proves the [Blum-Micali](/blum-micali/) generator and the easy case of [HILL](/hill-prg-from-one-way-functions/).
- **The Nisan-Wigderson analysis.** The [Nisan-Wigderson generator](/nisan-wigderson-generator/) is proved pseudorandom by turning a test into a next-bit predictor and the predictor into a small circuit for the hard function.
- **Trevisan's extractor.** The same chain, applied to every string of a weak source, proves [Trevisan's extractor](/trevisan-extractor/).
- **Previous-bit unpredictability.** The proof works for the reversed order of the bits, so pseudorandom also means that no predictor guesses bit $i$ from the bits after it.
- **Practical generators.** The next-bit test is the definition used for [cryptographically secure PRNGs](/cryptographically-secure-prng/), because it is easier to check one bit at a time.

## Tightness

Part 2 loses nothing. Part 1 loses a factor $m$, and some loss is needed. Let $Y$ be $m$ independent bits, each equal to 1 with probability $\frac12 + \delta$. The bits are independent, so the best predictor for each position guesses 1 and succeeds with probability exactly $\frac12 + \delta$. The test "is the weight above $m/2$?" is a small circuit, and its advantage is the statistical distance $\Delta(Y, U_m)$:

| $m$ | $\delta$ | advantage of the test | advantage / $\delta$ |
|---|---|---|---|
| 25 | 0.02 | 0.0801 | 4.00 |
| 100 | 0.01 | 0.0799 | 7.99 |
| 400 | 0.005 | 0.0796 | 15.92 |

The ratio grows like $0.8\sqrt{m}$, close to $\sqrt{2/\pi}\,\sqrt{m}$. So a test with advantage $\varepsilon$ can come with predictors whose advantage is only about $\varepsilon/\sqrt m$. This example does not show that the full factor $m$ is needed.

## History

Blum and Micali, in a paper presented at FOCS 1982 and published in 1984, defined a cryptographically strong generator by the next-bit test and built one from the discrete logarithm. Yao, at the same conference, proved that a generator that passes the next-bit test passes every polynomial-time statistical test, so the next-bit test is universal. The proof by hybrids is the form given by Goldreich and by later textbooks.

## References
