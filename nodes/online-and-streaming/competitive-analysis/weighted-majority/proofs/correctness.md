---
title: Weighted majority makes at most (ln n + m* ln(1/β)) / ln(2/(1+β)) mistakes, and its randomized version has expected loss at most (ln n + L* ln(1/β)) / (1 − β)
proves: [mistake-bound, expected-loss-bound]
status: full
---

There are $n$ experts and $T$ rounds, and $0 \le \beta < 1$ (with $0 < \beta < 1$ for the randomized version). Let $w_{t,i}$ be the weight of expert $i$ at the start of round $t$, with $w_{1,i} = 1$, and let $W_t = \sum_i w_{t,i}$, so $W_1 = n$. Let $m_i$ be the number of mistakes of expert $i$ and $m^* = \min_i m_i$.

**Lemma 1 (weights).** In the deterministic algorithm, $w_{T+1,i} = \beta^{m_i}$ for every $i$.

*Proof.* Line L7 multiplies $w_i$ by $\beta$ exactly in the rounds where expert $i$ is wrong, and nothing else changes $w_i$. $\square$

**Lemma 2 (the potential falls at each mistake).** If the algorithm errs in round $t$, then $W_{t+1} \le \frac{1+\beta}{2} W_t$. In every round, $W_{t+1} \le W_t$.

*Proof.* Let $W^{\text{wrong}}$ be the total weight of the experts that predict $1 - y_t$ in round $t$. Line L7 gives $W_{t+1} = W_t - (1 - \beta) W^{\text{wrong}} \le W_t$. If the algorithm errs, it predicted $1 - y_t$, so by line L5 the side $1 - y_t$ had at least as much weight as the side $y_t$ (for $\hat y_t = 1$ this is $W^1 \ge W^0$; for $\hat y_t = 0$ it is $W^0 > W^1$). So $W^{\text{wrong}} \ge W_t / 2$, and $W_{t+1} \le W_t (1 - \frac{1 - \beta}{2}) = \frac{1+\beta}{2} W_t$. $\square$

**Theorem 1 (mistake bound).** If the algorithm makes $m$ mistakes, then $\beta^{m^*} \le n \left(\frac{1+\beta}{2}\right)^m$. For $0 < \beta < 1$ this is

$$m \le \frac{\ln n + m^* \ln(1/\beta)}{\ln\frac{2}{1+\beta}},$$

and for $\beta = 1/2$ it gives $m \le 2.41\,(m^* + \log_2 n)$.

*Proof.* By Lemma 1, $W_{T+1} \ge w_{T+1,i^*} = \beta^{m^*}$ for an expert $i^*$ with $m_{i^*} = m^*$. By Lemma 2, applied to each round, $W_{T+1} \le W_1 \left(\frac{1+\beta}{2}\right)^m = n\left(\frac{1+\beta}{2}\right)^m$. Combine the two and take logarithms; $\ln \frac{2}{1+\beta} > 0$ because $\beta < 1$. For $\beta = 1/2$: $\ln 2 / \ln \frac43 = 2.4094\ldots$ and $\ln n / \ln \frac43 = \log_2 n \cdot \ln 2 / \ln\frac43$, so both terms have the factor $2.4094\ldots < 2.41$. $\square$

**Corollary (halving).** If $\beta = 0$ and some expert is never wrong, then $m \le \lfloor \log_2 n \rfloor$.

*Proof.* Here $m^* = 0$ and $\beta^{0} = 1$, so $1 \le n \cdot 2^{-m}$, and $m \le \log_2 n$. Since $m$ is an integer, $m \le \lfloor \log_2 n \rfloor$. $\square$

**Randomized weighted majority.** Losses are $\ell_{t,i} \in [0, 1]$, and $L_i = \sum_t \ell_{t,i}$, $L^* = \min_i L_i$. In round $t$ the algorithm picks expert $i$ with probability $p_{t,i} = w_{t,i}/W_t$, so its expected loss is $E_t = \sum_i p_{t,i} \ell_{t,i}$, and then sets $w_{t+1,i} = w_{t,i}\bigl(1 - (1-\beta)\ell_{t,i}\bigr)$. For losses in $\{0, 1\}$ this is the update of line L7.

**Lemma 3.** For $x \in [0, 1]$ and $0 < \beta < 1$, $\beta^x \le 1 - (1 - \beta)x$.

*Proof.* The function $x \mapsto \beta^x$ is convex, so on $[0, 1]$ it lies below the chord from $(0, 1)$ to $(1, \beta)$, which is $1 - (1-\beta)x$. $\square$

**Theorem 2 (expected loss).** For every sequence of losses, also when $\ell_t$ is chosen after seeing $p_t$,

$$\sum_{t=1}^{T} E_t \le \frac{\ln n + L^* \ln(1/\beta)}{1 - \beta}.$$

With $\beta = 1 - \varepsilon$ and $0 < \varepsilon \le 1/2$, this is at most $(1 + \varepsilon)L^* + \frac{\ln n}{\varepsilon}$.

*Proof.* Upper bound: $W_{t+1} = \sum_i w_{t,i}(1 - (1-\beta)\ell_{t,i}) = W_t (1 - (1-\beta)E_t) \le W_t\, e^{-(1-\beta)E_t}$, using $1 - z \le e^{-z}$. So $W_{T+1} \le n\,e^{-(1-\beta)\sum_t E_t}$. Lower bound: by Lemma 3, $w_{T+1,i} \ge \prod_t \beta^{\ell_{t,i}} = \beta^{L_i}$, so $W_{T+1} \ge \beta^{L^*}$. Combine and take logarithms: $L^* \ln \beta \le \ln n - (1 - \beta)\sum_t E_t$, which is the claim. For the second form, $\ln\frac{1}{1-\varepsilon} = \varepsilon + \frac{\varepsilon^2}{2} + \frac{\varepsilon^3}{3} + \cdots \le \varepsilon + \frac{\varepsilon^2}{2(1 - \varepsilon)} \le \varepsilon + \varepsilon^2$ for $\varepsilon \le 1/2$. Divide by $1 - \beta = \varepsilon$. The proof uses only the identity for $W_{t+1}$, which holds for whatever $\ell_t$ is, so it also holds for an adversary that sees $p_t$. $\blacksquare$

**Corollary (regret).** If $T$ is known and $\varepsilon = \sqrt{\ln n / T} \le 1/2$, then $\sum_t E_t - L^* \le \varepsilon L^* + \frac{\ln n}{\varepsilon} \le \varepsilon T + \frac{\ln n}{\varepsilon} = 2\sqrt{T \ln n}$.
