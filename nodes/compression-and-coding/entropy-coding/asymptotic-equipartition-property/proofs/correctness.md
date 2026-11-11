---
title: The AEP for a memoryless source, and the properties of the typical set
proves: [statement]
status: full
---

This proof covers the memoryless case of the statement: parts (a) to (d). The ergodic form (part (e), the Shannon-McMillan-Breiman theorem) is not proved here; see Cover and Thomas, Section 16.8, or Breiman 1957.

We use the notation of the page. $X_1, X_2, \ldots$ are independent, and each has the law $p$ on the finite alphabet $\Sigma$. $H = H(X_1)$, logarithms are base 2, $X^n = (X_1, \ldots, X_n)$ and $p(x^n) = \prod_{i=1}^{n} p(x_i)$.

**Step 1: a sum of independent terms.** Let $S = \{x \in \Sigma : p(x) > 0\}$. With probability 1, every $X_i$ lies in $S$, so we can define

$$Y_i = \log_2 \frac{1}{p(X_i)}.$$

The $Y_i$ are functions of independent variables with the same law, so they are independent with the same law. Each $Y_i$ takes values in the finite set $\{\log_2 (1/p(x)) : x \in S\}$, so it is bounded. Its mean is $\mathbb{E}[Y_i] = \sum_{x \in S} p(x) \log_2 \frac{1}{p(x)} = H$, and its variance $V = \operatorname{Var}(Y_1)$ is finite. Because $p(X^n)$ is a product,

$$-\frac{1}{n} \log_2 p(X^n) = \frac{1}{n} \sum_{i=1}^{n} Y_i.$$

**Step 2: part (a), the AEP.** By [Chebyshev's inequality](/chebyshev-inequality/), for every $\varepsilon > 0$,

$$\Pr\left[\left| \frac{1}{n} \sum_{i=1}^{n} Y_i - H \right| > \varepsilon \right] \le \frac{\operatorname{Var}\left(\frac{1}{n} \sum Y_i\right)}{\varepsilon^2} = \frac{V}{n \varepsilon^2}.$$

The right side goes to 0 as $n \to \infty$. So $-\frac{1}{n} \log_2 p(X^n) \to H$ in probability. This is the [weak law of large numbers](/law-of-large-numbers/) for the $Y_i$. $\square$

**Step 3: part (b), the probability of the typical set.** By its definition, $x^n \in A_\varepsilon^{(n)}$ if and only if $H - \varepsilon \le -\frac{1}{n} \log_2 p(x^n) \le H + \varepsilon$. (We take only $x^n$ with $p(x^n) > 0$; the other strings have probability 0 and change no probability below.) So the event $X^n \in A_\varepsilon^{(n)}$ is the event $|\frac{1}{n} \sum Y_i - H| \le \varepsilon$, and Step 2 gives

$$\Pr\left[X^n \in A_\varepsilon^{(n)}\right] \ge 1 - \frac{V}{n \varepsilon^2}.$$

This is more than $1 - \varepsilon$ as soon as $n > V / \varepsilon^3$. $\square$

**Step 4: part (c), the upper bound on the size.** Each $x^n \in A_\varepsilon^{(n)}$ has $p(x^n) \ge 2^{-n(H + \varepsilon)}$. So

$$1 \ge \sum_{x^n \in A_\varepsilon^{(n)}} p(x^n) \ge \left|A_\varepsilon^{(n)}\right| 2^{-n(H + \varepsilon)},$$

and $|A_\varepsilon^{(n)}| \le 2^{n(H + \varepsilon)}$ for every $n$. $\square$

**Step 5: part (c), the lower bound on the size.** Each $x^n \in A_\varepsilon^{(n)}$ has $p(x^n) \le 2^{-n(H - \varepsilon)}$. For $n > V / \varepsilon^3$, Step 3 gives

$$1 - \varepsilon < \Pr\left[A_\varepsilon^{(n)}\right] = \sum_{x^n \in A_\varepsilon^{(n)}} p(x^n) \le \left|A_\varepsilon^{(n)}\right| 2^{-n(H - \varepsilon)},$$

so $|A_\varepsilon^{(n)}| > (1 - \varepsilon) 2^{n(H - \varepsilon)}$. $\square$

**Step 6: part (d), no much smaller set has high probability.** Let $0 < \delta < 1$ and let $B_n \subseteq \Sigma^n$ be any set with $\Pr[X^n \in B_n] \ge 1 - \delta$. Take $\varepsilon > 0$ with $\delta + \varepsilon < 1$. For $n > V / \varepsilon^3$, the union bound gives

$$\Pr\left[B_n \cap A_\varepsilon^{(n)}\right] \ge 1 - \Pr\left[\overline{B_n}\right] - \Pr\left[\overline{A_\varepsilon^{(n)}}\right] > 1 - \delta - \varepsilon.$$

Each string of $B_n \cap A_\varepsilon^{(n)}$ has probability at most $2^{-n(H - \varepsilon)}$, so

$$1 - \delta - \varepsilon < \left|B_n \cap A_\varepsilon^{(n)}\right| 2^{-n(H - \varepsilon)} \le |B_n| \, 2^{-n(H - \varepsilon)}.$$

Hence $\frac{1}{n} \log_2 |B_n| > H - \varepsilon + \frac{1}{n} \log_2 (1 - \delta - \varepsilon)$. The last term goes to 0, and $\varepsilon$ can be as small as we like, so $\liminf_{n} \frac{1}{n} \log_2 |B_n| \ge H$. With part (c), the typical set is, to first order in the exponent, the smallest set of probability at least $1 - \delta$. $\blacksquare$

**Remark on the constants.** The proof uses only the variance of $Y_1$, so its bound on $n$ is weak. For a coin with $p(1) = 0.1$, $V = 0.1 \cdot 0.9 \cdot (\log_2 9)^2 = 0.904$, and with $\varepsilon = 0.1$ Step 3 gives $\Pr[A_\varepsilon^{(n)}] \ge 1 - 90.4 / n$. At $n = 1000$ this is $0.9096$; the exact value is $0.99906$. A Chernoff bound gives a probability that goes to 1 exponentially fast in $n$.
