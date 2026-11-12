---
title: The training error of AdaBoost is at most the product of the normalizers
proves: [correctness]
status: full
---

We use the pseudocode of the page. The training set is $S = ((x_1, y_1), \ldots, (x_n, y_n))$ with $y_i \in \{-1, +1\}$, and each weak hypothesis $h_t$ maps into $\{-1, +1\}$. Write $F_t(x) = \sum_{s=1}^{t} \alpha_s h_s(x)$, with $F_0 = 0$, and $H_t(x) = \operatorname{sign}(F_t(x))$, where we count $F_t(x) = 0$ as an error. Let $\varepsilon_t = \sum_i D_t(i) [h_t(x_i) \ne y_i]$ and $\gamma_t = \frac12 - \varepsilon_t$. Assume that the algorithm runs $T$ rounds with $0 < \varepsilon_t < \frac12$ in each round, so that line L5 and line L6 never stop it.

**Theorem.** For each $T \ge 1$,

$$\frac1n \left|\{i : H_T(x_i) \ne y_i\}\right| \le \prod_{t=1}^{T} Z_t = \prod_{t=1}^{T} 2\sqrt{\varepsilon_t (1 - \varepsilon_t)} = \prod_{t=1}^{T} \sqrt{1 - 4\gamma_t^2} \le \exp\left(-2 \sum_{t=1}^{T} \gamma_t^2\right).$$

### Step 1: the weights after $T$ rounds

**Claim 1.** For each $t$ with $0 \le t \le T$ and each $i$, $D_{t+1}(i) = \dfrac{\exp(-y_i F_t(x_i))}{n \prod_{s=1}^{t} Z_s}$, with the empty product equal to 1.

*Proof.* By induction on $t$. For $t = 0$, line L1 gives $D_1(i) = 1/n = \exp(0)/n$. Assume the claim for $t - 1$. Lines L8 and L9 give $D_{t+1}(i) = D_t(i) \exp(-\alpha_t y_i h_t(x_i)) / Z_t$. Put in the claim for $D_t(i)$:

$$D_{t+1}(i) = \frac{\exp(-y_i F_{t-1}(x_i)) \exp(-\alpha_t y_i h_t(x_i))}{n \prod_{s=1}^{t-1} Z_s \cdot Z_t} = \frac{\exp(-y_i F_t(x_i))}{n \prod_{s=1}^{t} Z_s},$$

because $F_t = F_{t-1} + \alpha_t h_t$. $\square$

### Step 2: the training error is at most the mean exponential loss

If $H_T(x_i) \ne y_i$, then $y_i F_T(x_i) \le 0$, so $\exp(-y_i F_T(x_i)) \ge 1$. If $H_T(x_i) = y_i$, then $\exp(-y_i F_T(x_i)) > 0$. So for each $i$, $[H_T(x_i) \ne y_i] \le \exp(-y_i F_T(x_i))$. Sum over $i$ and divide by $n$. Line L9 makes $D_{T+1}$ sum to 1, so Claim 1 gives

$$\frac1n \sum_{i=1}^{n} [H_T(x_i) \ne y_i] \le \frac1n \sum_{i=1}^{n} \exp(-y_i F_T(x_i)) = \prod_{t=1}^{T} Z_t \sum_{i=1}^{n} D_{T+1}(i) = \prod_{t=1}^{T} Z_t.$$

### Step 3: the value of each normalizer

Before the division of line L9, $\sum_i D_t(i) \exp(-\alpha y_i h_t(x_i))$ is a function of $\alpha$. The examples with $h_t(x_i) = y_i$ have $y_i h_t(x_i) = 1$ and total weight $1 - \varepsilon_t$. The others have $y_i h_t(x_i) = -1$ and total weight $\varepsilon_t$. So

$$Z(\alpha) = (1 - \varepsilon_t) e^{-\alpha} + \varepsilon_t e^{\alpha}.$$

$Z$ is strictly convex in $\alpha$, since $Z''(\alpha) = Z(\alpha) > 0$. Its derivative $-(1 - \varepsilon_t) e^{-\alpha} + \varepsilon_t e^{\alpha}$ is zero exactly when $e^{2\alpha} = (1 - \varepsilon_t)/\varepsilon_t$, that is, at $\alpha_t = \frac12 \ln \frac{1 - \varepsilon_t}{\varepsilon_t}$ of line L7. So $\alpha_t$ is the unique minimizer of $Z$. At this point $e^{\alpha_t} = \sqrt{(1 - \varepsilon_t)/\varepsilon_t}$, and

$$Z_t = (1 - \varepsilon_t)\sqrt{\frac{\varepsilon_t}{1 - \varepsilon_t}} + \varepsilon_t \sqrt{\frac{1 - \varepsilon_t}{\varepsilon_t}} = 2\sqrt{\varepsilon_t (1 - \varepsilon_t)}.$$

With $\varepsilon_t = \frac12 - \gamma_t$, $4\varepsilon_t(1 - \varepsilon_t) = 4(\frac12 - \gamma_t)(\frac12 + \gamma_t) = 1 - 4\gamma_t^2$, so $Z_t = \sqrt{1 - 4\gamma_t^2}$.

### Step 4: the exponential form

For each real $u$, $1 + u \le e^{u}$, because $e^{u} - 1 - u$ has derivative $e^{u} - 1$, which is negative for $u < 0$ and positive for $u > 0$, so its minimum is 0 at $u = 0$. With $u = -4\gamma_t^2$, we get $1 - 4\gamma_t^2 \le e^{-4\gamma_t^2}$. Both sides are nonnegative, so the square roots keep the order: $\sqrt{1 - 4\gamma_t^2} \le e^{-2\gamma_t^2}$. Multiply over $t = 1, \ldots, T$. This proves the theorem. $\square$

**Corollary.** If $\gamma_t \ge \gamma > 0$ in each round, the training error is at most $e^{-2T\gamma^2}$. The training error is a multiple of $1/n$, so it is 0 once $e^{-2T\gamma^2} < 1/n$, that is, for each $T > \ln(n) / (2\gamma^2)$.

### Step 5: the stopping rules

Line L5 stops when $\varepsilon_t \ge \frac12$. Then $\alpha_t \le 0$, and the round would not reduce the bound, since $Z_t = 2\sqrt{\varepsilon_t(1 - \varepsilon_t)} \le 1$ with equality only at $\varepsilon_t = \frac12$; with $\varepsilon_t > \frac12$ the negated hypothesis $-h_t$ has error $1 - \varepsilon_t < \frac12$, so a weak learner that may return $-h_t$ never needs this case. Line L6 stops when $\varepsilon_t = 0$. Then $h_t$ is correct on all of $S$, and returning it gives training error 0. The loop of line L2 runs at most $T$ times, so the algorithm stops.

### Step 6: the weak hypothesis of round $t$ has error exactly $\frac12$ under $D_{t+1}$

By Step 3, before the division the correct examples carry total weight $(1 - \varepsilon_t) e^{-\alpha_t} = \sqrt{\varepsilon_t(1 - \varepsilon_t)}$ and the wrong ones carry $\varepsilon_t e^{\alpha_t} = \sqrt{\varepsilon_t(1 - \varepsilon_t)}$. The two parts are equal, so after the division by $Z_t$ each part is $\frac12$. So $h_t$ has weighted error $\frac12$ under $D_{t+1}$, and the next round cannot pick $h_t$ again with an edge. $\square$

### Step 7: AdaBoost is forward stagewise additive modeling with the exponential loss

Let $L(F) = \sum_{i=1}^{n} \exp(-y_i F(x_i))$. Fix $F_{t-1}$, and consider one new term $\alpha h$ with $\alpha > 0$ and $h$ from the weak class. Write $w_i = \exp(-y_i F_{t-1}(x_i))$ and $W = \sum_i w_i$. By Claim 1, $w_i / W = D_t(i)$. Let $\varepsilon(h) = \sum_i D_t(i) [h(x_i) \ne y_i]$. As in Step 3,

$$L(F_{t-1} + \alpha h) = W\left((1 - \varepsilon(h)) e^{-\alpha} + \varepsilon(h) e^{\alpha}\right) = W\left(e^{-\alpha} + (e^{\alpha} - e^{-\alpha})\varepsilon(h)\right).$$

For each fixed $\alpha > 0$, the factor $e^{\alpha} - e^{-\alpha}$ is positive, so the best $h$ is a hypothesis of least weighted error under $D_t$, the choice of line L3 when the weak learner minimizes weighted error. For this $h$, Step 3 shows that the best $\alpha$ is $\alpha_t$ of line L7. So each round of AdaBoost takes the term $\alpha h$ that most reduces the exponential loss of the training set, and the remaining loss is $W Z_t$. $\square$

**The population minimizer.** For a fixed $x$ with $p = \Pr[Y = 1 \mid x] \in (0, 1)$, the expected loss of the value $f$ is $g(f) = p e^{-f} + (1 - p) e^{f}$. It is strictly convex, and $g'(f) = 0$ gives $e^{2f} = p/(1 - p)$, so $f^* = \frac12 \ln \frac{p}{1 - p}$. The sign of $f^*$ is the Bayes decision, and $p = 1/(1 + e^{-2 f^*})$. Friedman, Hastie and Tibshirani (2000) use this fact to read the AdaBoost score as an estimate of half the log-odds. $\square$
