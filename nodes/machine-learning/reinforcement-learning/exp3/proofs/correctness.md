---
title: The regret bound of EXP3 (Auer, Cesa-Bianchi, Freund and Schapire 2002, Theorem 3.1 and Corollary 3.2)
proves: [correctness]
status: full
---

**Setting.** A reward table $x_t(i) \in [0,1]$, for $t \le n$ and $i \le K$ with $K \ge 2$, is fixed before the run. EXP3 runs with $\gamma \in (0,1]$ as in the pseudocode. Write $w_i(t)$ for the weight of arm $i$ at the start of round $t$, $W_t = \sum_i w_i(t)$, $p_i(t)$ for the probabilities of line L3, and

$$\hat x_t(i) = \frac{x_t(i)}{p_i(t)}\,\mathbb{1}\{A_t = i\},$$

so that line L7 is $w_i(t+1) = w_i(t)\exp(\gamma\hat x_t(i)/K)$ for every $i$ (arms with $\hat x_t(i) = 0$ keep their weight). Let $G_i = \sum_t x_t(i)$, $G_{\max} = \max_i G_i$ and $G = \sum_t x_t(A_t)$. Let $\mathbb{E}_t$ be the expectation given the choices before round $t$.

**Theorem.** $G_{\max} - \mathbb{E}[G] \le (e-1)\gamma G_{\max} + \dfrac{K\ln K}{\gamma}$.

**Corollary.** If $g \ge G_{\max}$ and $\gamma = \min\{1, \sqrt{K\ln K/((e-1)g)}\}$, then $G_{\max} - \mathbb{E}[G] \le 2\sqrt{e-1}\sqrt{gK\ln K}$.

**Three facts about the estimates.** Fix a round $t$ and the past.

1. $\mathbb{E}_t[\hat x_t(i)] = p_i(t)\cdot x_t(i)/p_i(t) = x_t(i)$, since the table is fixed and $p_i(t) > 0$.
2. $\sum_i p_i(t)\hat x_t(i) = x_t(A_t)$, since only the term $i = A_t$ is not 0.
3. $\sum_i p_i(t)\hat x_t(i)^2 = x_t(A_t)\,\hat x_t(A_t) \le \hat x_t(A_t) = \sum_i \hat x_t(i)$, since $x_t(A_t) \le 1$.

Also $p_i(t) \ge \gamma/K$, so $0 \le \gamma\hat x_t(i)/K \le \gamma \cdot \frac{1}{p_i(t)} \cdot \frac{1}{K} \le 1$.

**An inequality.** For $0 \le z \le 1$, $e^z \le 1 + z + (e-2)z^2$. *Proof.* $e^z = 1 + z + z^2\sum_{k\ge2} z^{k-2}/k!$, and for $0 \le z \le 1$ the sum is at most $\sum_{k \ge 2} 1/k! = e - 2$.

*Proof of the theorem.* If $\gamma = 1$ the right side is at least $(e-1)G_{\max} \ge G_{\max}$, and $\mathbb{E}[G] \ge 0$, so the claim holds. Let $\gamma < 1$.

*Upper bound on the growth of $W$.* By line L3, $w_i(t)/W_t = (p_i(t) - \gamma/K)/(1-\gamma)$, which is at most $p_i(t)/(1-\gamma)$. With $z = \gamma\hat x_t(i)/K \in [0,1]$,

$$\frac{W_{t+1}}{W_t} = \sum_i \frac{w_i(t)}{W_t}e^{z} \le \sum_i \frac{w_i(t)}{W_t}\Big(1 + \frac{\gamma}{K}\hat x_t(i) + (e-2)\frac{\gamma^2}{K^2}\hat x_t(i)^2\Big)$$

$$\le 1 + \frac{\gamma/K}{1-\gamma}\sum_i p_i(t)\hat x_t(i) + \frac{(e-2)(\gamma/K)^2}{1-\gamma}\sum_i p_i(t)\hat x_t(i)^2 \le 1 + \frac{\gamma/K}{1-\gamma}x_t(A_t) + \frac{(e-2)(\gamma/K)^2}{1-\gamma}\sum_i\hat x_t(i),$$

using $\sum_i w_i(t)/W_t = 1$ and facts 2 and 3. Take logarithms, use $\ln(1+y) \le y$, and sum over $t = 1, \ldots, n$:

$$\ln\frac{W_{n+1}}{W_1} \le \frac{\gamma/K}{1-\gamma}\,G + \frac{(e-2)(\gamma/K)^2}{1-\gamma}\sum_{t=1}^{n}\sum_{i=1}^{K}\hat x_t(i).$$

*Lower bound.* For each arm $j$, $W_{n+1} \ge w_j(n+1) = \exp\big(\frac{\gamma}{K}\sum_t \hat x_t(j)\big)$ and $W_1 = K$, so

$$\ln\frac{W_{n+1}}{W_1} \ge \frac{\gamma}{K}\sum_{t=1}^{n}\hat x_t(j) - \ln K.$$

*Combine.* Put the two bounds together and multiply by $K(1-\gamma)/\gamma > 0$:

$$(1-\gamma)\sum_t \hat x_t(j) - \frac{(1-\gamma)K\ln K}{\gamma} \le G + (e-2)\frac{\gamma}{K}\sum_t\sum_i \hat x_t(i).$$

*Take expectations.* By fact 1 and the tower rule, $\mathbb{E}[\sum_t\hat x_t(i)] = G_i$ for each $i$. So

$$(1-\gamma)G_j - \frac{(1-\gamma)K\ln K}{\gamma} \le \mathbb{E}[G] + (e-2)\frac{\gamma}{K}\sum_{i=1}^{K}G_i \le \mathbb{E}[G] + (e-2)\gamma G_{\max}.$$

Choose $j$ with $G_j = G_{\max}$ and rearrange:

$$G_{\max} - \mathbb{E}[G] \le \gamma G_{\max} + (e-2)\gamma G_{\max} + \frac{(1-\gamma)K\ln K}{\gamma} \le (e-1)\gamma G_{\max} + \frac{K\ln K}{\gamma}. \qquad\blacksquare$$

*Proof of the corollary.* If $\gamma < 1$, then $(e-1)\gamma G_{\max} \le (e-1)\gamma g$, and with $\gamma = \sqrt{K\ln K/((e-1)g)}$ the two terms $(e-1)\gamma g$ and $K\ln K/\gamma$ are both equal to $\sqrt{(e-1)gK\ln K}$; their sum is the bound. If $\gamma = 1$, then $K\ln K \ge (e-1)g$, so $2\sqrt{e-1}\sqrt{gK\ln K} \ge 2(e-1)g \ge g \ge G_{\max} \ge G_{\max} - \mathbb{E}[G]$, since rewards are not negative. $\blacksquare$

**Remarks.**

- The proof uses the fixed table in fact 1: $x_t(i)$ does not depend on the choices of the player. This is the [oblivious adversary](/oblivious-adversary/) model.
- With $g = n$ the bound is $2\sqrt{e-1}\sqrt{nK\ln K} \approx 2.63\sqrt{nK\ln K}$.
- The lower bound of order $\sqrt{nK}$ (Theorem 5.1 of the paper) uses a random table in which one random arm has mean $\frac12 + \varepsilon$ and the others have mean $\frac12$, with $\varepsilon$ of order $\sqrt{K/n}$. A player then cannot tell the good arm from the others without about $K/\varepsilon^2$ pulls.
