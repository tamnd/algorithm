---
title: The Morris counter is unbiased, with variance a n(n-1)/2
proves: [correctness]
status: full
---

We prove the claims for Morris(a) with $a \in (0, 1]$. The base 2 counter of lines L1 to L5 is the case $a = 1$. Write $c = 1 + a$ and let $X_n$ be the register after $n$ events, with $X_0 = 0$ by line L1. At each event, line L4 raises $X$ by 1 with probability $c^{-X}$, with fresh randomness, and otherwise leaves it. The estimate is $Y_n = (c^{X_n} - 1)/a$. For $a = 1$ the raise of line L4 happens when $X$ fresh fair bits are all 0, which has probability $2^{-X}$, and $Y_n = 2^{X_n} - 1$ is the value of line L5.

**Lemma 1 (one step).** For each value $x$ of $X_k$,
$$\mathbb{E}[c^{X_{k+1}} \mid X_k = x] = c^x + a, \qquad \mathbb{E}[c^{2X_{k+1}} \mid X_k = x] = c^{2x} + (c^2 - 1)\,c^x.$$

*Proof.* With probability $c^{-x}$ the next value is $x + 1$, and otherwise it is $x$. So
$$\mathbb{E}[c^{X_{k+1}} \mid X_k = x] = c^x + c^{-x}(c^{x+1} - c^x) = c^x + (c - 1) = c^x + a,$$
$$\mathbb{E}[c^{2X_{k+1}} \mid X_k = x] = c^{2x} + c^{-x}(c^{2x+2} - c^{2x}) = c^{2x} + (c^2 - 1)\,c^x. \qquad \square$$

**Theorem 1 (unbiased).** $\mathbb{E}[Y_n] = n$ for each $n \ge 0$.

*Proof.* Take the expectation of the first identity of Lemma 1 over $X_k$: $\mathbb{E}[c^{X_{k+1}}] = \mathbb{E}[c^{X_k}] + a$. With $\mathbb{E}[c^{X_0}] = 1$, induction gives $\mathbb{E}[c^{X_n}] = 1 + an$. So $\mathbb{E}[Y_n] = (1 + an - 1)/a = n$. $\square$

**Theorem 2 (variance).** $\mathrm{Var}(Y_n) = a\,n(n-1)/2$. For the base 2 counter, $\mathrm{Var}(2^{X_n} - 1) = n(n-1)/2$.

*Proof.* Take the expectation of the second identity of Lemma 1 and use Theorem 1:
$$\mathbb{E}[c^{2X_{k+1}}] = \mathbb{E}[c^{2X_k}] + (c^2 - 1)(1 + ak).$$
With $\mathbb{E}[c^{2X_0}] = 1$, the sum over $k = 0, \ldots, n-1$ gives
$$\mathbb{E}[c^{2X_n}] = 1 + (c^2 - 1)\left(n + \frac{a\,n(n-1)}{2}\right).$$
Here $c^2 - 1 = 2a + a^2$. So
$$\mathrm{Var}(c^{X_n}) = 1 + (2a + a^2)\left(n + \frac{a\,n(n-1)}{2}\right) - (1 + an)^2.$$
Expand: $(2a + a^2)\,n = 2an + a^2 n$ and $(2a + a^2)\,a\,n(n-1)/2 = a^2 n(n-1) + a^3 n(n-1)/2$. Also $(1 + an)^2 = 1 + 2an + a^2 n^2$. The terms $1$ and $2an$ cancel, and $a^2 n + a^2 n(n-1) - a^2 n^2 = 0$. What is left is $\mathrm{Var}(c^{X_n}) = a^3 n(n-1)/2$. Since $Y_n = (c^{X_n} - 1)/a$, $\mathrm{Var}(Y_n) = \mathrm{Var}(c^{X_n})/a^2 = a\,n(n-1)/2$. For $a = 1$ this is $n(n-1)/2$. $\square$

For $a = 1$ the two moments are $\mathbb{E}[2^{X_n}] = n + 1$ and $\mathbb{E}[4^{X_n}] = 1 + 3n(n+1)/2$, which are the forms in the main text.

**Theorem 3 (one counter).** For each $\varepsilon > 0$, $\Pr[|Y_n - n| \ge \varepsilon n] \le a(n-1)/(2\varepsilon^2 n) < a/(2\varepsilon^2)$. So with $a = 2\varepsilon^2\delta$, the failure probability is below $\delta$.

*Proof.* [Chebyshev's inequality](/chebyshev-inequality/) with Theorems 1 and 2: $\Pr[|Y_n - n| \ge \varepsilon n] \le \mathrm{Var}(Y_n)/(\varepsilon n)^2 = a(n-1)/(2\varepsilon^2 n)$. $\square$

**Theorem 4 (Morris+).** Let $\bar Y$ be the mean of $s$ independent base 2 counters. Then $\Pr[|\bar Y - n| \ge \varepsilon n] < 1/(2s\varepsilon^2)$. With $s = \lceil 3/(2\varepsilon^2) \rceil$ this is at most $1/3$.

*Proof.* The copies are independent, so $\mathbb{E}[\bar Y] = n$ and $\mathrm{Var}(\bar Y) = n(n-1)/(2s) < n^2/(2s)$. Chebyshev gives the first bound. With $s \ge 3/(2\varepsilon^2)$, $1/(2s\varepsilon^2) \le 1/3$. $\square$

**Theorem 5 (Morris++).** Let $Z$ be the median of $t$ independent copies of Morris+, with $t$ odd and $t \ge 2\ln(1/\delta)/\ln(9/8)$. Then $\Pr[|Z - n| \ge \varepsilon n] \le \delta$.

*Proof.* Call a copy bad if its value is not in $(n - \varepsilon n, n + \varepsilon n)$. By Theorem 4 each copy is bad with probability at most $p = 1/3$, independently. If at most $(t-1)/2$ copies are bad, more than half of the values are in the interval, so the median is in it too. The [median trick](/median-trick/) page proves, with a Chernoff bound, that $\Pr[\text{at least } t/2 \text{ copies are bad}] \le (4p(1-p))^{t/2} = (8/9)^{t/2}$, and this is at most $\delta$ for the stated $t$. $\square$

**Theorem 6 (register size).** For each $\delta' \in (0, 1]$, $\Pr[c^{X_n} \ge (1 + an)/\delta'] \le \delta'$. So with probability at least $1 - \delta'$,
$$X_n < \log_c\frac{1 + an}{\delta'} \le \frac{2}{a}\ln\frac{1 + an}{\delta'},$$
and the register fits in $\log_2 X_n + 1 = O(\log(1/a) + \log\log(n/\delta'))$ bits.

*Proof.* $c^{X_n}$ is positive with mean $1 + an$ by Theorem 1, so [Markov's inequality](/markov-inequality/) gives the first claim. The second follows by taking $\log_c$, and from $\ln(1 + a) \ge a/2$ for $0 < a \le 1$. Then $\log_2 X_n \le 1 + \log_2(1/a) + \log_2 \ln((1 + an)/\delta')$, and $(1+an)/\delta' \le 2n/\delta'$ for $n \ge 1$. $\square$

For $a = 1$ the first claim reads $\Pr[X_n \ge \log_2(n+1) + c'] \le 2^{-c'}$, with $\delta' = 2^{-c'}$. With $a = 2\varepsilon^2\delta$ and $\delta' = \delta$, Theorems 3 and 6 and the [union bound](/union-bound/) show that one counter is within $\varepsilon n$ of $n$ and fits in $O(\log\log n + \log(1/\varepsilon) + \log(1/\delta))$ bits, with probability at least $1 - 2\delta$. For Morris++ there are $st$ base 2 registers. By Theorem 6 with $\delta' = \delta/(st)$ and the union bound, all of them are below $\log_2(n+1) + \log_2(st/\delta)$ with probability $1 - \delta$, so the total space is $O(st \log\log(n st/\delta)) = O(\varepsilon^{-2}\log(1/\delta)\log\log(n/(\varepsilon\delta)))$ bits.

The optimal bound of Nelson and Yu (2022) is not proved here. $\blacksquare$
