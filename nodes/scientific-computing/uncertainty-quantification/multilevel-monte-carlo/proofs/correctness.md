---
title: The multilevel estimator is unbiased for the finest level and meets its variance target at the least cost
proves: [correctness, termination]
status: full
---

We assume exact arithmetic and exact random numbers. The approximations $P_0, P_1, \ldots$ of the output $P$ are square integrable random variables on one probability space $(\Omega, \mathcal{F}, \mathbb{P})$. For $l \ge 0$ let $Y_l = P_l - P_{l-1}$ with $P_{-1} = 0$, $V_l = \mathrm{Var}(Y_l)$ and $C_l$ the mean cost of one sample of $Y_l$. The estimator with finest level $L$ and sample counts $N_0, \ldots, N_L$ is

$$\widehat{Y} = \sum_{l=0}^{L} \widehat{Y}_l, \qquad \widehat{Y}_l = \frac{1}{N_l} \sum_{n=1}^{N_l} Y_l^{(n, l)},$$

where the samples $Y_l^{(n, l)}$ are independent for all $n$ and $l$, and each has the law of $Y_l$. Inside one sample, $P_l$ and $P_{l-1}$ use the same random input; this changes $V_l$ but none of the statements below.

**Lemma 1 (the telescoping sum).** $\mathbb{E}[\widehat{Y}] = \mathbb{E}[P_L]$.

*Proof.* By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\widehat{Y}_l] = \mathbb{E}[Y_l] = \mathbb{E}[P_l] - \mathbb{E}[P_{l-1}]$. The sum over $l = 0, \ldots, L$ telescopes to $\mathbb{E}[P_L] - \mathbb{E}[P_{-1}] = \mathbb{E}[P_L]$. $\square$

**Lemma 2 (the variance).** $\mathrm{Var}(\widehat{Y}) = \sum_{l=0}^{L} V_l / N_l$.

*Proof.* The $N_0 + \cdots + N_L$ samples are independent, so the variance of the sum is the sum of the variances: $\mathrm{Var}(\widehat{Y}) = \sum_l N_l^{-2} \sum_n \mathrm{Var}(Y_l^{(n, l)}) = \sum_l V_l / N_l$. $\square$

**Lemma 3 (the error split).** $\mathbb{E}[(\widehat{Y} - \mathbb{E}[P])^2] = \sum_l V_l / N_l + (\mathbb{E}[P_L] - \mathbb{E}[P])^2$.

*Proof.* Write $\widehat{Y} - \mathbb{E}[P] = (\widehat{Y} - \mathbb{E}[P_L]) + (\mathbb{E}[P_L] - \mathbb{E}[P])$. The first term has mean zero by Lemma 1 and the second is a constant, so the cross term has mean zero. The mean square of the first term is the variance of Lemma 2. $\square$

So the [mean squared error](/mean-squared-error/) is at most $\varepsilon^2$ if the variance is at most $\varepsilon^2/2$ and the bias $|\mathbb{E}[P_L] - \mathbb{E}[P]|$ is at most $\varepsilon/\sqrt{2}$. The algorithm aims at these two targets separately.

**Lemma 4 (the least cost for the variance target).** For fixed $L$ and real $N_l > 0$, every choice with $\sum_l V_l / N_l \le \varepsilon^2/2$ has cost $\sum_l N_l C_l \ge 2 \varepsilon^{-2} \big(\sum_l \sqrt{V_l C_l}\big)^2$. Equality holds for

$$N_l = 2 \varepsilon^{-2} \sqrt{V_l / C_l}\, \sum_{k=0}^{L} \sqrt{V_k C_k}.$$

*Proof.* By the Cauchy-Schwarz inequality for the vectors with entries $\sqrt{V_l / N_l}$ and $\sqrt{N_l C_l}$,

$$\Big(\sum_l \sqrt{V_l C_l}\Big)^2 = \Big(\sum_l \sqrt{V_l / N_l}\, \sqrt{N_l C_l}\Big)^2 \le \Big(\sum_l \frac{V_l}{N_l}\Big) \Big(\sum_l N_l C_l\Big) \le \frac{\varepsilon^2}{2} \sum_l N_l C_l.$$

Equality in the first step holds if and only if $N_l C_l$ is a fixed multiple of $V_l / N_l$, that is $N_l = \mu \sqrt{V_l / C_l}$. Equality in the second step needs $\sum_l V_l / N_l = \varepsilon^2/2$, which gives $\mu = 2 \varepsilon^{-2} \sum_k \sqrt{V_k C_k}$. The same counts come from a [Lagrange multiplier](/lagrange-multiplier/) for the cost with the variance constraint. $\square$

Line L5 rounds these counts up. The variance target still holds: with $S = \sum_k \sqrt{V_k C_k}$ and $N_l \ge 2 \varepsilon^{-2} \sqrt{V_l / C_l}\, S$,

$$\sum_l \frac{V_l}{N_l} \le \sum_l \frac{\varepsilon^2 V_l}{2 S \sqrt{V_l / C_l}} = \frac{\varepsilon^2}{2 S} \sum_l \sqrt{V_l C_l} = \frac{\varepsilon^2}{2}.$$

The rounding adds at most one sample on each level, so at most $\sum_l C_l$ to the cost.

**Lemma 5 (the bias test).** Assume that $\mathbb{E}[Y_l] = c\, 2^{-\alpha l}$ for all $l \ge L$, with $\alpha > 0$ and a constant $c$. Then $|\mathbb{E}[P] - \mathbb{E}[P_L]| = |\mathbb{E}[Y_L]| / (2^\alpha - 1)$.

*Proof.* If $\mathbb{E}[P_l] \to \mathbb{E}[P]$, then $\mathbb{E}[P] - \mathbb{E}[P_L] = \sum_{l > L} \mathbb{E}[Y_l] = \mathbb{E}[Y_L] \sum_{k \ge 1} 2^{-\alpha k} = \mathbb{E}[Y_L] / (2^\alpha - 1)$, a geometric series. $\square$

Line L7 puts the sample means $\widehat{Y}_L$ and $\widehat{Y}_{L-1} / 2^\alpha$ into this formula and takes the larger value. Under the assumption of Lemma 5 from level $L - 1$ on, both are estimates of $|\mathbb{E}[Y_L]|$; the second one guards against a sample mean $\widehat{Y}_L$ that is small by chance. Line L8 adds a level while the estimate is above $\varepsilon/\sqrt{2}$.

**Theorem (correctness).** When the loop ends, the estimate of line L9 has mean $\mathbb{E}[P_L]$. If the sample variances and means of lines L4 and L7 are equal to the true $V_l$ and $\mathbb{E}[Y_l]$, and $\mathbb{E}[Y_l] = c\, 2^{-\alpha l}$ for $l \ge L - 1$, then its mean squared error is at most $\varepsilon^2$, and no choice of real sample counts for this $L$ reaches the variance target at a lower cost.

*Proof.* The first claim is Lemma 1. The loop ends only when all $dN_l = 0$, so the counts are at least those of Lemma 4 and the variance is at most $\varepsilon^2/2$; the bias test passed, so by Lemma 5 the bias is at most $\varepsilon/\sqrt{2}$. Lemma 3 adds the two parts. The cost claim is Lemma 4. $\blacksquare$

**Termination.** Each pass of lines L2 to L8 with some $dN_l > 0$ adds at least one sample, and the counts never go down. On a fixed level set, the sample variances converge almost surely as the counts grow (the [law of large numbers](/law-of-large-numbers/)), so the optimal counts of line L5 stay bounded and the counts pass them after finitely many passes. The number of levels is at most `max_level`, after which the code stops with an error. So the loop ends with probability 1.

**The geometric Brownian motion example.** The Euler-Maruyama step for $dS = rS\, dt + \sigma S\, dW$ is $S_{k+1} = S_k (1 + r h + \sigma \Delta W_k)$. The factors are independent with mean $1 + r h$, so after $2^l$ steps of size $h_l = T/2^l$, $\mathbb{E}[P_l] = S_0 (1 + r T/2^l)^{2^l}$. This is the exact level mean that the tests compare with. Since $\ln(1 + x) = x - x^2/2 + O(x^3)$, $\mathbb{E}[P_l] = S_0 e^{rT} (1 - r^2 T h_l / 2 + O(h_l^2))$, so the weak rate is $\alpha = 1$. The coarse path of a sample sums pairs of the fine increments, so it has the law of a coarse Euler path, and $\mathbb{E}[Y_l]$ is the difference of two consecutive level means, as Lemma 1 needs.

**What is not proved.** The theorem is conditional on exact moments. In a real run, $V_l$ and $\mathbb{E}[Y_l]$ are estimated from the same samples, the rate $\alpha$ is an assumption, and the bias test can pass too early when $\mathbb{E}[Y_l]$ does not yet follow its rate. Then the mean squared error can be larger than $\varepsilon^2$. The cost bound as a function of $\varepsilon$ is the [MLMC complexity theorem](/mlmc-complexity-theorem/), and it needs the rate hypotheses of that theorem.
