---
title: The maximum load of n balls in n bins is (1 + o(1)) ln n / ln ln n, and the heavily loaded gap is O(sqrt(m ln n / n))
proves: [correctness]
status: full
---

**Setup.** Throw $m$ balls into $n \ge 2$ bins. Ball $t$ picks bin $B_t$, and $B_1, \ldots, B_m$ are independent and uniform on $\{1, \ldots, n\}$. The load of bin $j$ is $X_j = |\{t : B_t = j\}|$, and $M = \max_j X_j$. Write $L = \ln n / \ln\ln n$. For $n \ge 16$ we have $\ln\ln n \ge 1.01$ and $\ln\ln\ln n \ge 0$, so $L$, $\ln L$ and the quantities below are defined.

**Theorem.** Fix $\varepsilon \in (0, 1)$.

1. (Upper tail, $m = n$.) Let $r_n = (\ln\ln\ln n + 1)/\ln\ln n$. For each $n \ge 16$ with $r_n \le \varepsilon / (2(1 + \varepsilon))$, $\Pr[M \ge (1 + \varepsilon)L] \le n^{-\varepsilon/2}$.
2. (Lower tail, $m = n$.) For each $n \ge 16$ with $L \ge 1/(1-\varepsilon)$ and $\varepsilon \ln n \ge 2\ln\ln n + 4$, $\Pr[M \le (1 - \varepsilon)L] \le e\sqrt{n}\,\exp(-n^{\varepsilon/2}/e)$.
3. (Heavy case.) If $m \ge 6n\ln n$, then $\Pr[M \ge m/n + \sqrt{6(m/n)\ln n}] \le 1/n$.

## Two lemmas

**Lemma A.** For each integer $k \ge 1$, $(k/e)^k \le k! \le e\sqrt{k}\,(k/e)^k$.

*Proof.* The lower bound: $e^k = \sum_{j \ge 0} k^j/j! \ge k^k/k!$. The upper bound: $\ln$ is concave, so on each interval $[i, i+1]$ the chord lies below the curve, and $\frac12(\ln i + \ln(i+1)) \le \int_i^{i+1} \ln x\,dx$. Sum over $i = 1, \ldots, k-1$: $\ln k! - \frac12 \ln k \le \int_1^k \ln x\,dx = k\ln k - k + 1$. Exponentiate. $\square$

**Lemma B (Poisson comparison).** Let $Y_1, \ldots, Y_n$ be independent Poisson variables with mean $m/n$, and $m \ge 1$. For each set $A$ of vectors in $\mathbb{Z}_{\ge 0}^n$, $\Pr[(X_1, \ldots, X_n) \in A] \le e\sqrt{m}\,\Pr[(Y_1, \ldots, Y_n) \in A]$.

*Proof.* Let $k = (k_1, \ldots, k_n)$ with $\sum_j k_j = m$. The multinomial law gives $\Pr[X = k] = \frac{m!}{k_1! \cdots k_n!} n^{-m}$. Independence gives $\Pr[Y = k] = \prod_j e^{-m/n}(m/n)^{k_j}/k_j! = e^{-m} m^m n^{-m} / (k_1! \cdots k_n!)$. So $\Pr[X = k] = \frac{m!\,e^m}{m^m} \Pr[Y = k] \le e\sqrt m\,\Pr[Y = k]$ by Lemma A. A vector whose sum is not $m$ has probability 0 under $X$. Sum over $k \in A$. $\square$

## Proof of part 1

1. *One bin.* Fix bin 1 and an integer $k \ge 1$. If $X_1 \ge k$, then some set of $k$ balls all chose bin 1. There are $\binom nk$ sets of $k$ balls, and a fixed set all chooses bin 1 with probability $n^{-k}$. By the [union bound](/union-bound/), $\Pr[X_1 \ge k] \le \binom nk n^{-k} \le \frac{n^k}{k!} n^{-k} = \frac1{k!}$.
2. *All bins.* By the union bound over the $n$ bins, $\Pr[M \ge k] \le n/k!$.
3. *The choice of $k$.* Let $x = (1+\varepsilon)L$ and $k = \lceil x \rceil$. Loads are integers, so $M \ge x$ is the event $M \ge k$.
4. *A lower bound on $\ln k!$.* By Lemma A, $\ln k! \ge k\ln k - k$. The function $g(y) = y\ln y - y$ has $g'(y) = \ln y \ge 0$ for $y \ge 1$, and $x \ge L \ge 1$ for $n \ge 16$, so $\ln k! \ge g(x)$.
5. *Evaluate $g(x)$.* Here $\ln x = \ln(1+\varepsilon) + \ln\ln n - \ln\ln\ln n$. So
$$ g(x) = (1+\varepsilon)\frac{\ln n}{\ln\ln n}\bigl(\ln\ln n - \ln\ln\ln n + \ln(1+\varepsilon) - 1\bigr) \ge (1+\varepsilon)\ln n\,(1 - r_n). $$
6. *Use the hypothesis.* If $r_n \le \varepsilon/(2(1+\varepsilon))$, then $(1+\varepsilon)(1 - r_n) \ge 1 + \varepsilon - \varepsilon/2 = 1 + \varepsilon/2$, so $\ln k! \ge (1 + \varepsilon/2)\ln n$.
7. *Conclude.* $\Pr[M \ge (1+\varepsilon)L] \le n / k! \le n \cdot n^{-1-\varepsilon/2} = n^{-\varepsilon/2}$.

The condition on $r_n$ holds for all large $n$: with $y = \ln\ln n$, $r_n = (\ln y + 1)/y$, whose derivative in $y$ is $-\ln y / y^2 < 0$ for $y > 1$, and $r_n \to 0$.

## Proof of part 2

1. *The event.* Let $k = \lfloor (1-\varepsilon)L \rfloor + 1$. The event $M \le (1-\varepsilon)L$ is the event that every load is less than $k$. Call it $A$.
2. *The Poisson model.* Take $Y_j$ independent Poisson with mean $m/n = 1$. A Poisson(1) variable equals $k$ with probability $1/(e\,k!)$, so $\Pr[Y_j < k] \le 1 - 1/(e\,k!)$. By independence and $1 - u \le e^{-u}$,
$$ \Pr[Y \in A] \le \Bigl(1 - \frac{1}{e\,k!}\Bigr)^n \le \exp\Bigl(-\frac{n}{e\,k!}\Bigr). $$
3. *An upper bound on $\ln k!$.* Let $a = (1-\varepsilon)L$, so $k \le a + 1$, and $\ln k! \le k\ln k \le (a+1)\ln(a+1)$. Now $\ln(a+1) = \ln a + \ln(1 + 1/a) \le \ln L + 1/a$, because $\ln a \le \ln L$ and $\ln(1+u) \le u$. Hence
$$ \ln k! \le (a+1)\Bigl(\ln L + \frac1a\Bigr) = (1-\varepsilon)L\ln L + \ln L + 1 + \frac1a. $$
4. *Bound each term.* $L\ln L = \ln n\,(1 - \ln\ln\ln n/\ln\ln n) \le \ln n$, because $\ln\ln\ln n \ge 0$. Also $\ln L \le \ln\ln n$, and $1/a \le 1$ because $L \ge 1/(1-\varepsilon)$. So $\ln k! \le (1-\varepsilon)\ln n + \ln\ln n + 2$.
5. *Use the hypothesis.* $\ln(n/k!) \ge \varepsilon\ln n - \ln\ln n - 2 \ge \frac{\varepsilon}{2}\ln n$, because $\varepsilon \ln n \ge 2\ln\ln n + 4$. So $n/(e\,k!) \ge n^{\varepsilon/2}/e$, and step 2 gives $\Pr[Y \in A] \le \exp(-n^{\varepsilon/2}/e)$.
6. *Back to balls and bins.* By Lemma B with $m = n$, $\Pr[M \le (1-\varepsilon)L] = \Pr[X \in A] \le e\sqrt n\,\exp(-n^{\varepsilon/2}/e)$.

## Proof of part 3

Let $\mu = m/n$. Each load $X_j$ is a sum of $m$ independent indicator variables with mean $1/n$, so $\mathbb{E}[X_j] = \mu$. The [Chernoff bound](/chernoff-bound/) gives $\Pr[X_j \ge (1+\delta)\mu] \le e^{-\mu\delta^2/3}$ for $0 < \delta \le 1$. Take $\delta = \sqrt{6\ln n/\mu}$. The hypothesis $m \ge 6n\ln n$ is $\mu \ge 6\ln n$, so $\delta \le 1$. Then $\mu\delta^2/3 = 2\ln n$ and $\Pr[X_j \ge \mu + \sqrt{6\mu\ln n}] \le n^{-2}$. The union bound over the $n$ bins gives the probability $1/n$. $\blacksquare$

## Consequence

Parts 1 and 2 give, for each fixed $\varepsilon > 0$, $\Pr[(1-\varepsilon)L < M < (1+\varepsilon)L] \to 1$ as $n \to \infty$, with failure probability at most $n^{-\varepsilon/2} + e\sqrt n\exp(-n^{\varepsilon/2}/e)$ for large $n$. That is, $M = (1 + o(1))\ln n/\ln\ln n$ with high probability.
