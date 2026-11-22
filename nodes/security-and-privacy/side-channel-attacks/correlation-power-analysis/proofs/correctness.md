---
title: CPA returns the first top-scoring guess, and it finds the key in the Hamming weight model
proves: [correctness]
status: full
---

We write $s(g)$ for the score that line L6 gives to the guess $g$.

**Lemma 1 (the loop of line L2).** After the iteration for guess $g$, top is $\max_{h \le g} s(h)$ and best is the smallest $h \le g$ with $s(h) =$ top.

*Proof.* By induction on $g$, as for [DPA](/differential-power-analysis/). Line L1 starts with top $= -\infty$. Every score is a finite number in $[0, 1]$, so the first guess always passes line L7. Later, line L7 replaces best only when the new score is strictly larger, so among guesses with equal top scores the first one stays. $\square$

So line L9 returns the first argmax of the scores.

**Lemma 2 (scale and offset).** For $a \ne 0$ and any $c$, replacing every $\ell_i[j]$ by $a \ell_i[j] + c$ does not change $|r_j|$.

*Proof.* The offset $c$ cancels in $\ell_i[j] - \bar\ell[j]$. The factor $a$ multiplies the numerator of $r_j$ by $a$ and the square root in the denominator by $|a|$. So $r_j$ is multiplied by the sign of $a$, and $|r_j|$ does not change. $\square$

**The model.** Let $k$ be the key. The inputs are independent and uniform on $\{0, \ldots, 15\}$. At the sample $j^\ast$, $\ell_i[j^\ast] = \varepsilon \, \mathrm{HW}(S(p_i \oplus k)) + N_{ij^\ast}$ with $\varepsilon > 0$, and $\ell_i[j] = N_{ij}$ elsewhere. The noise values are independent of each other and of the inputs, with mean 0 and variance $\sigma^2$. For $X$ uniform on $\{0, \ldots, 15\}$ define

$$c(\delta) = \operatorname{corr}\big(\mathrm{HW}(S(X)),\ \mathrm{HW}(S(X \oplus \delta))\big).$$

**Lemma 3 (the population correlation).** Fix a guess $g$, put $\delta = g \oplus k$, and let $h = \mathrm{HW}(S(p \oplus g))$ for a uniform input $p$. Then

$$\operatorname{corr}(h, \ell[j^\ast]) = c(\delta) \, \rho, \qquad \rho = \frac{\varepsilon}{\sqrt{\varepsilon^2 + \sigma^2}},$$

and $\operatorname{corr}(h, \ell[j]) = 0$ for $j \ne j^\ast$.

*Proof.* Put $X = p \oplus k$, which is uniform, so $h = \mathrm{HW}(S(X \oplus \delta))$. Since $S$ is a bijection, $S(X)$ and $S(X \oplus \delta)$ are both uniform on 4 bits. The Hamming weight of a uniform 4-bit value is a sum of 4 independent fair bits, so its variance is $4 \cdot \tfrac14 = 1$. So $\operatorname{Var}(h) = 1$, and the covariance of $h$ with $\mathrm{HW}(S(X))$ equals their correlation $c(\delta)$. The noise is independent of $p$, so

$$\operatorname{Cov}(h, \ell[j^\ast]) = \varepsilon \, c(\delta), \qquad \operatorname{Var}(\ell[j^\ast]) = \varepsilon^2 \cdot 1 + \sigma^2 .$$

Dividing the covariance by $\sqrt{1 \cdot (\varepsilon^2 + \sigma^2)}$ gives the first claim. For $j \ne j^\ast$, $\ell[j]$ is independent of $h$, so the covariance is 0. $\square$

**Lemma 4 (the table of $c$).** For the PRESENT S-box $S = (\texttt{C}, 5, 6, \texttt{B}, 9, 0, \texttt{A}, \texttt{D}, 3, \texttt{E}, \texttt{F}, 8, 4, 7, 1, 2)$, the values $c(\delta)$ for $\delta = 0, 1, \ldots, 15$ are

$$1,\ -0.25,\ -0.375,\ 0.25,\ 0.125,\ -0.25,\ -0.75,\ 0.25,\ -0.5,\ 0.375,\ 0.5,\ 0.125,\ -0.5,\ 0.125,\ 0.5,\ -0.625 .$$

So $|c(\delta)| \le 0.75$ for every $\delta \ne 0$, with equality only at $\delta = 6$.

*Proof.* Both Hamming weights have mean 2 and variance 1, so $c(\delta) = \tfrac{1}{16}\sum_{x} (\mathrm{HW}(S(x)) - 2)(\mathrm{HW}(S(x \oplus \delta)) - 2)$, a finite sum of 16 terms. For example, for $\delta = 6$ the products are, for $x = 0, \ldots, 15$, $0, 0, 0, -2, 0, -2, 0, 0, 0, -1, -2, -1, -2, -1, 0, -1$, and the sum is $-12$, so $c(6) = -12/16 = -0.75$. The test file computes all 16 values with `statistics.correlation` and checks that the noiseless scores of the code equal them, for every key. $\square$

**Theorem (consistency).** In the model, with the PRESENT S-box, the probability that line L9 returns best $= k$ tends to 1 as $m \to \infty$.

*Proof.* For a fixed guess and sample, $r_j$ is a continuous function of the five sample moments $\bar h$, $\bar\ell[j]$, $\overline{h^2}$, $\overline{\ell[j]^2}$ and $\overline{h \ell[j]}$, wherever the two sample variances are positive. All the variables have finite second moments, so by the strong [law of large numbers](/law-of-large-numbers/) each sample moment converges with probability 1 to its population value, and both population variances are positive ($\operatorname{Var}(h) = 1$ and $\operatorname{Var}(\ell[j]) \ge \sigma^2$, or $\varepsilon^2$ at $j^\ast$). So $r_j$ converges with probability 1 to the population correlation of Lemma 3. Line L6 takes a maximum of finitely many absolute values, which is continuous, so

$$s(g) \to |c(g \oplus k)| \, \rho .$$

The limit is $\rho$ for $g = k$ and at most $0.75\rho$ for $g \ne k$, by Lemma 4. There are 16 guesses, so with probability 1 there is an $M$ such that $s(k) > 0.875\rho > s(g)$ for all $g \ne k$ and all $m \ge M$. Then $k$ is the only guess with the top score, and by Lemma 1 line L9 returns it. Convergence with probability 1 implies convergence in probability. $\blacksquare$

**Remark.** Without the S-box (the pitfall of line L3), the hypothesis of $g = k \oplus \texttt{F}$ is $4 - \mathrm{HW}(p \oplus k)$, whose correlation with $\mathrm{HW}(p \oplus k)$ is $-1$. Its absolute value ties with the right key for every $m$, so no number of traces separates the two guesses.
