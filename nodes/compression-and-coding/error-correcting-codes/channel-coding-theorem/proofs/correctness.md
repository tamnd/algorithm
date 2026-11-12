---
title: Proof of the noisy-channel coding theorem (random coding with joint typicality, and the converse from Fano's inequality)
proves: [statement]
status: full
---

**Setting.** A discrete memoryless channel has finite alphabets $\mathcal{X}$, $\mathcal{Y}$ and transition probabilities $W(y \mid x)$; over $n$ uses, $W^n(y^n \mid x^n) = \prod_{i=1}^n W(y_i \mid x_i)$, and there is no feedback. An $(M, n)$ code has an encoder $x^n : \{1, \ldots, M\} \to \mathcal{X}^n$ and a decoder $g : \mathcal{Y}^n \to \{1, \ldots, M\}$. The error probability of message $m$ is $\lambda_m = \Pr[g(Y^n) \ne m \mid x^n(m) \text{ sent}]$, the maximal error is $\lambda^{(n)} = \max_m \lambda_m$, and the average error is $P_e^{(n)} = \frac1M \sum_m \lambda_m$. The rate is $R = (\log_2 M)/n$. A rate $R$ is *achievable* if there are $(M_n, n)$ codes with $M_n \ge 2^{nR}$ and $\lambda^{(n)} \to 0$. The capacity is $C = \max_r I(X; Y)$, where $X \sim r$ and $Y$ is the output. All logarithms are to base 2.

**Statement.** (a) Every rate $R < C$ is achievable. (b) Every sequence of $(M_n, n)$ codes with $M_n \ge 2^{nR}$ has $P_e^{(n)} \ge 1 - \frac{C}{R} - \frac{1}{nR}$. So if $R > C$, the average (and so the maximal) error probability does not tend to 0, and $R$ is not achievable.

## Joint typicality

Fix an input law $r$, let $p(x, y) = r(x) W(y \mid x)$ with marginals $r$ and $q$, and remove from $\mathcal{X}$ and $\mathcal{Y}$ the symbols of probability 0. For $\varepsilon > 0$, the **jointly typical set** $A_\varepsilon^{(n)}$ is the set of pairs $(x^n, y^n)$ with

$$\Bigl| -\tfrac1n \log r(x^n) - H(X) \Bigr| < \varepsilon, \quad \Bigl| -\tfrac1n \log q(y^n) - H(Y) \Bigr| < \varepsilon, \quad \Bigl| -\tfrac1n \log p(x^n, y^n) - H(X, Y) \Bigr| < \varepsilon,$$

where $r(x^n) = \prod_i r(x_i)$, and likewise for $q$ and $p$.

**Lemma 1 (joint AEP).**

1. If $(X^n, Y^n)$ has i.i.d. pairs with law $p$, then $\Pr[(X^n, Y^n) \in A_\varepsilon^{(n)}] \to 1$ as $n \to \infty$.
2. $|A_\varepsilon^{(n)}| \le 2^{n(H(X, Y) + \varepsilon)}$.
3. If $\tilde X^n$ has law $r^n$, $\tilde Y^n$ has law $q^n$, and they are independent, then $\Pr[(\tilde X^n, \tilde Y^n) \in A_\varepsilon^{(n)}] \le 2^{-n(I(X; Y) - 3\varepsilon)}$.

*Proof.* (1) $-\frac1n \log r(X^n) = \frac1n \sum_i (-\log r(X_i))$ is an average of $n$ i.i.d. bounded random variables with mean $H(X)$, so by the weak [law of large numbers](/law-of-large-numbers/) it is within $\varepsilon$ of $H(X)$ with probability tending to 1. The same holds for the other two averages, and by a [union bound](/union-bound/) over the three, all three hold with probability tending to 1. (2) Every pair in the set has $p(x^n, y^n) > 2^{-n(H(X, Y) + \varepsilon)}$, and the probabilities sum to at most 1. (3) Every pair in the set has $r(x^n) < 2^{-n(H(X) - \varepsilon)}$ and $q(y^n) < 2^{-n(H(Y) - \varepsilon)}$, so with part 2,
$$\sum_{(x^n, y^n) \in A_\varepsilon^{(n)}} r(x^n) q(y^n) \le 2^{n(H(X, Y) + \varepsilon)} \, 2^{-n(H(X) - \varepsilon)} \, 2^{-n(H(Y) - \varepsilon)} = 2^{-n(I(X; Y) - 3\varepsilon)},$$
using $I(X; Y) = H(X) + H(Y) - H(X, Y)$. $\square$

## Part (a): achievability

Let $R < C$. Choose $r$ with $I(X; Y) = C$, and choose $\varepsilon > 0$ with $R + 3\varepsilon < C$ and so small that $4\varepsilon$ is below a target $\delta$. Let $M = 2 \lceil 2^{nR} \rceil$.

*Random codebook.* Choose the $M$ codewords $X^n(1), \ldots, X^n(M)$ independently, each with i.i.d. symbols of law $r$.

*Decoder.* Given $y^n$, output the unique $m$ with $(X^n(m), y^n) \in A_\varepsilon^{(n)}$. If there is no such $m$, or more than one, output a failure mark, which counts as an error for every message.

*Error averaged over codebooks.* Let $\bar P$ be the average over the random codebook of $P_e^{(n)}$. By the symmetry of the construction, $\bar P$ equals the probability of error when message 1 is sent. Let $E_m$ be the event that $(X^n(m), Y^n) \in A_\varepsilon^{(n)}$. An error needs $E_1$ to fail or some $E_m$ with $m \ne 1$ to hold, so

$$\bar P \le \Pr[E_1^c] + \sum_{m=2}^{M} \Pr[E_m].$$

The pair $(X^n(1), Y^n)$ is i.i.d. with law $p$, so $\Pr[E_1^c] \le \varepsilon$ for all large $n$ by Lemma 1(1). For $m \ne 1$, the codeword $X^n(m)$ is independent of $X^n(1)$ and therefore of $Y^n$, which depends on $X^n(1)$ and the noise alone; $X^n(m)$ has law $r^n$ and $Y^n$ has law $q^n$. By Lemma 1(3), $\Pr[E_m] \le 2^{-n(C - 3\varepsilon)}$. Since $M \le 2^{nR + 2}$,

$$\bar P \le \varepsilon + 2^{nR + 2} \, 2^{-n(C - 3\varepsilon)} = \varepsilon + 4 \cdot 2^{-n(C - R - 3\varepsilon)},$$

which is at most $2\varepsilon$ for all large $n$, because $C - R - 3\varepsilon > 0$.

*One good code.* An average over codebooks is at most $2\varepsilon$, so at least one codebook $\mathcal{C}^*$ has $P_e^{(n)}(\mathcal{C}^*) \le 2\varepsilon$.

*From average to maximal error.* In $\mathcal{C}^*$, at most half of the $M$ messages can have $\lambda_m > 4\varepsilon$, since otherwise the average would exceed $2\varepsilon$. Keep the best half, $M/2 = \lceil 2^{nR} \rceil \ge 2^{nR}$ codewords, and keep the same decoder; when it outputs a removed message, count that as an error. For a kept message $m$ the decoder errs on exactly the same received words as before, so $\lambda_m$ does not change, and each kept message has $\lambda_m \le 4\varepsilon < \delta$.

So for every $\delta > 0$ and all large $n$ there is a code with at least $2^{nR}$ codewords and maximal error below $\delta$, and $R$ is achievable. $\square$

## Part (b): the converse

Fix an $(M, n)$ code with $M \ge 2^{nR}$, and let the message $U$ be uniform on $\{1, \ldots, M\}$. Then $U \to X^n \to Y^n \to \hat U = g(Y^n)$ is a Markov chain: $X^n$ is a function of $U$, $Y^n$ depends on $U$ only through $X^n$, and $\hat U$ is a function of $Y^n$. Here $\Pr[\hat U \ne U] = P_e^{(n)}$.

**Lemma 2 (Fano's inequality).** $H(U \mid \hat U) \le 1 + P_e^{(n)} \log M$.

*Proof.* Let $E = 1$ if $\hat U \ne U$ and $E = 0$ otherwise. Expand $H(E, U \mid \hat U)$ by the chain rule in two ways. First, $H(U \mid \hat U) + H(E \mid U, \hat U) = H(U \mid \hat U)$, because $E$ is a function of $U$ and $\hat U$. Second, $H(E \mid \hat U) + H(U \mid E, \hat U) \le 1 + \Pr[E = 0] \cdot 0 + \Pr[E = 1] \log(M - 1)$: a binary variable has entropy at most 1, given $E = 0$ the message is $\hat U$, and given $E = 1$ it is one of $M - 1$ other values. So $H(U \mid \hat U) \le 1 + P_e^{(n)} \log M$. $\square$

**Lemma 3 (no gain from blocks).** $I(X^n; Y^n) \le nC$.

*Proof.* Given $X^n = x^n$, the outputs are independent with laws $W(\cdot \mid x_i)$, so $H(Y^n \mid X^n) = \sum_i H(Y_i \mid X_i)$. Also $H(Y^n) \le \sum_i H(Y_i)$, since [conditional entropy](/conditional-entropy/) is at most entropy, applied with the chain rule. So $I(X^n; Y^n) = H(Y^n) - H(Y^n \mid X^n) \le \sum_i \bigl(H(Y_i) - H(Y_i \mid X_i)\bigr) = \sum_i I(X_i; Y_i) \le nC$, because each $X_i$ has some law and $C$ is the maximum over all laws. $\square$

*Proof of (b).* Since $U$ is uniform,
$$\log M = H(U) = H(U \mid \hat U) + I(U; \hat U) \le 1 + P_e^{(n)} \log M + I(X^n; Y^n) \le 1 + P_e^{(n)} \log M + nC.$$
The middle step uses Lemma 2 and the data processing inequality $I(U; \hat U) \le I(X^n; Y^n)$ for the Markov chain $U \to X^n \to Y^n \to \hat U$; the last step is Lemma 3. Divide by $\log M \ge nR$:
$$P_e^{(n)} \ge 1 - \frac{nC + 1}{\log M} \ge 1 - \frac{C}{R} - \frac{1}{nR}.$$
If $R > C$, the right side tends to $1 - C/R > 0$, so neither the average nor the maximal error tends to 0. $\blacksquare$
