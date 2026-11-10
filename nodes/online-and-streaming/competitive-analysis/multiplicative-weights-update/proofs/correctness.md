---
title: Multiplicative weights has cost at most Σ m_i + η Σ |m_i| + (ln n)/η, and Hedge has regret at most (ln n)/η + ηT/8
proves: [ahk-bound, hedge-regret]
status: full
---

There are $n$ experts and $T$ rounds. In round $t$ the algorithm plays $p_t = w_t / \Phi_t$, where $\Phi_t = \sum_i w_{t,i}$ and $w_{1,i} = 1$, so $\Phi_1 = n$. The adversary may choose the costs of round $t$ after it sees $p_t$; the proofs below hold for every such choice, because they bound the cost $p_t \cdot m_t$ of each round directly.

## The linear update

Costs are $m_{t,i} \in [-1, 1]$, $0 < \eta \le 1/2$, and line L6 sets $w_{t+1,i} = w_{t,i}(1 - \eta m_{t,i})$. Every factor is at least $1 - \eta \ge 1/2 > 0$, so all weights stay positive.

**Lemma 1.** For $x \in [0, 1]$, $1 - \eta x \ge (1 - \eta)^x$. For $x \in [-1, 0]$, $1 - \eta x \ge (1 + \eta)^{-x}$.

*Proof.* On $[0, 1]$ the function $x \mapsto (1 - \eta)^x$ is convex, so it lies below its chord from $(0, 1)$ to $(1, 1 - \eta)$, which is $1 - \eta x$. On $[-1, 0]$ put $y = -x \in [0, 1]$; then $(1 + \eta)^y$ is convex in $y$ and lies below its chord $1 + \eta y = 1 - \eta x$. $\square$

**Lemma 2.** For $0 < \eta \le 1/2$, $\ln\frac{1}{1 - \eta} \le \eta + \eta^2$ and $\ln(1 + \eta) \ge \eta - \eta^2$.

*Proof.* $\ln\frac{1}{1-\eta} = \sum_{k \ge 1} \eta^k / k \le \eta + \frac{\eta^2}{2}\sum_{j \ge 0} \eta^j = \eta + \frac{\eta^2}{2(1 - \eta)} \le \eta + \eta^2$, since $1 - \eta \ge 1/2$. For the second, $g(\eta) = \ln(1 + \eta) - \eta + \eta^2$ has $g(0) = 0$ and $g'(\eta) = \frac{1}{1+\eta} - 1 + 2\eta = \frac{\eta(1 + 2\eta)}{1 + \eta} \ge 0$. $\square$

**Theorem 1 (Arora, Hazan and Kale).** For every expert $i$,

$$\sum_{t=1}^{T} p_t \cdot m_t \;\le\; \sum_{t=1}^{T} m_{t,i} + \eta \sum_{t=1}^{T} |m_{t,i}| + \frac{\ln n}{\eta}.$$

*Proof.*

1. *Upper bound on the potential.* $\Phi_{t+1} = \sum_i w_{t,i}(1 - \eta m_{t,i}) = \Phi_t (1 - \eta\, p_t \cdot m_t) \le \Phi_t\, e^{-\eta\, p_t \cdot m_t}$, by $1 - z \le e^{-z}$. So $\Phi_{T+1} \le n \exp(-\eta \sum_t p_t \cdot m_t)$.
2. *Lower bound.* Fix $i$. Let $P = \sum_{t : m_{t,i} \ge 0} m_{t,i}$ and $N = \sum_{t : m_{t,i} < 0} |m_{t,i}|$. By Lemma 1, $\Phi_{T+1} \ge w_{T+1,i} = \prod_t (1 - \eta m_{t,i}) \ge (1 - \eta)^{P} (1 + \eta)^{N}$.
3. *Combine.* Taking logarithms of $(1-\eta)^P (1+\eta)^N \le n \exp(-\eta \sum_t p_t \cdot m_t)$ gives
$$\eta \sum_t p_t \cdot m_t \le \ln n + P \ln\frac{1}{1-\eta} - N \ln(1 + \eta) \le \ln n + P(\eta + \eta^2) - N(\eta - \eta^2),$$
by Lemma 2. Divide by $\eta$: the right side is $\frac{\ln n}{\eta} + (P - N) + \eta(P + N)$, and $P - N = \sum_t m_{t,i}$, $P + N = \sum_t |m_{t,i}|$. $\square$

**Corollary 1.** For costs in $[0, 1]$, with $L_i = \sum_t m_{t,i}$, the cost is at most $(1 + \eta)L_i + \frac{\ln n}{\eta}$. With $\eta = \min(1/2, \sqrt{\ln n / T})$ and $T \ge 4 \ln n$, the regret against the best expert is at most $\eta T + \frac{\ln n}{\eta} = 2\sqrt{T \ln n}$.

## Hedge

Losses are $\ell_{t,i} \in [0, 1]$, $\eta > 0$, and the update is $w_{t+1,i} = w_{t,i}\, e^{-\eta \ell_{t,i}}$, so $w_{t,i} = e^{-\eta L_{t-1,i}}$ with $L_{t,i} = \sum_{s \le t} \ell_{s,i}$ and $L^* = \min_i L_{T,i}$.

**Lemma 3 (Hoeffding's lemma).** Let $X$ be a random variable with values in $[0, 1]$, and let $s$ be real. Then $\ln \mathbb{E}[e^{sX}] \le s\,\mathbb{E}[X] + s^2/8$.

*Proof.* Let $\psi(s) = \ln \mathbb{E}[e^{sX}]$; it is finite and smooth since $X$ is bounded. Then $\psi(0) = 0$ and $\psi'(0) = \mathbb{E}[X]$. Further, $\psi''(s)$ is the variance of $X$ under the probability measure with density $e^{sX}/\mathbb{E}[e^{sX}]$. Any random variable $Y$ with values in $[0, 1]$ has $\mathrm{Var}(Y) \le \mathbb{E}[(Y - \frac12)^2] \le \frac14$, so $\psi'' \le 1/4$ everywhere. By Taylor's theorem with the remainder, $\psi(s) = \psi(0) + s\psi'(0) + \frac{s^2}{2}\psi''(\xi) \le s\,\mathbb{E}[X] + \frac{s^2}{8}$. $\square$

**Theorem 2 (Freund and Schapire).** For every sequence of losses,

$$\sum_{t=1}^{T} p_t \cdot \ell_t - L^* \;\le\; \frac{\ln n}{\eta} + \frac{\eta T}{8}.$$

With $\eta = \sqrt{8 \ln n / T}$ the regret is at most $\sqrt{(T/2) \ln n}$.

*Proof.*

1. *One round.* $\frac{\Phi_{t+1}}{\Phi_t} = \sum_i p_{t,i}\, e^{-\eta \ell_{t,i}} = \mathbb{E}[e^{-\eta X}]$, where $X = \ell_{t,I}$ for $I$ drawn from $p_t$. By Lemma 3 with $s = -\eta$, $\ln \frac{\Phi_{t+1}}{\Phi_t} \le -\eta\, p_t \cdot \ell_t + \frac{\eta^2}{8}$.
2. *Sum.* Adding over $t$, $\ln \Phi_{T+1} - \ln n \le -\eta \sum_t p_t \cdot \ell_t + \frac{\eta^2 T}{8}$.
3. *Lower bound.* $\Phi_{T+1} \ge e^{-\eta L^*}$, the weight of a best expert, so $\ln \Phi_{T+1} \ge -\eta L^*$.
4. *Combine.* $-\eta L^* - \ln n \le -\eta \sum_t p_t \cdot \ell_t + \frac{\eta^2 T}{8}$. Divide by $\eta$ and rearrange.
5. *Tuning.* The right side $\frac{\ln n}{\eta} + \frac{\eta T}{8}$ is least at $\eta = \sqrt{8 \ln n / T}$, where both terms equal $\sqrt{T \ln n / 8}$, and their sum is $2\sqrt{T \ln n / 8} = \sqrt{T \ln n / 2}$. $\blacksquare$

**Remark.** The bound holds for an adversary that chooses $\ell_t$ after seeing $p_t$, since each step uses only the identity for $\Phi_{t+1}/\Phi_t$. If the algorithm draws one expert $I_t$ from $p_t$ and the adversary does not see $I_t$ before it fixes $\ell_t$, the expected loss of the drawn experts is the same sum, so the bound holds for the expected regret.
