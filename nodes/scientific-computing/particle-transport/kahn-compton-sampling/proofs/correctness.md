---
title: "Kahn's method samples the Klein-Nishina law exactly"
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform numbers $\xi_1, \xi_2, \xi_3$ on $[0, 1)$ in each try, independent between tries. Fix $\alpha > 0$, write $I = [1, 1 + 2\alpha]$, $\mu(q) = 1 - (q - 1)/\alpha$, and

$$f(q) = \frac{1}{q^2}\Big(q + \frac{1}{q} - 1 + \mu(q)^2\Big), \qquad q \in I,$$

the Klein-Nishina density in $q$ up to a constant. As $q$ runs over $I$, $\mu$ runs over $[-1, 1]$.

**Lemma 1 (the target).** The Klein-Nishina law for $\mu$ is the law of $\mu(q)$ when $q$ has density proportional to $f$ on $I$.

*Proof.* The Klein-Nishina density in $\mu$ is proportional to $P^2(P + 1/P - 1 + \mu^2)$ with $P = \alpha'/\alpha = 1/q$ and $q = 1 + \alpha(1 - \mu)$. The map $\mu \mapsto q$ is affine with $|dq/d\mu| = \alpha$, a constant, so the density in $q$ is the same expression divided by $\alpha$, which is $f(q)/\alpha$. $\square$

**Lemma 2 (the acceptance factors are probabilities).** For $q \in I$, $0 \le 4(1/q - 1/q^2) \le 1$ and $0 \le (\mu^2 + 1/q)/2 \le 1$.

*Proof.* $4(1/q - 1/q^2) = 1 - (1 - 2/q)^2 \in [0, 1]$ for $q \ge 1$. And $\mu^2 \le 1$, $0 < 1/q \le 1$. $\square$

**Lemma 3 (the proposals).** In branch 1, line L4 gives $q$ with density $1/(2\alpha)$ on $I$. In branch 2, line L7 gives $q$ with density $(1 + 2\alpha)/(2\alpha q^2)$ on $I$.

*Proof.* The first is clear. For the second, $q = (1 + 2\alpha)/(1 + 2\alpha \xi_2)$ is a decreasing function of $\xi_2$ from $1 + 2\alpha$ (at $\xi_2 = 0$) to $1$ (at $\xi_2 = 1$). Its inverse is $\xi_2 = ((1 + 2\alpha)/q - 1)/(2\alpha)$ with $|d\xi_2/dq| = (1 + 2\alpha)/(2\alpha q^2)$, which is the density of $q$ because $\xi_2$ is uniform. As a check, $\int_I (1 + 2\alpha)/(2\alpha q^2)\, dq = \frac{1 + 2\alpha}{2\alpha}(1 - \frac{1}{1 + 2\alpha}) = 1$. $\square$

**Lemma 4 (one try).** For every measurable $A \subseteq I$, the probability that one try accepts a value $q \in A$ is $C \int_A f(q)\, dq$ with

$$C = \frac{4(1 + 2\alpha)}{2\alpha(9 + 2\alpha)}.$$

*Proof.* Branch 1 is taken with probability $w_1 = (1 + 2\alpha)/(9 + 2\alpha)$ and branch 2 with $w_2 = 8/(9 + 2\alpha)$, by $\xi_1$. Given the branch and $q$, the try accepts with the factor of Lemma 2, because $\xi_3$ is uniform and independent. So the density of an accepted $q$ is, by Lemma 3,

$$w_1 \frac{1}{2\alpha} \cdot 4\Big(\frac{1}{q} - \frac{1}{q^2}\Big) + w_2 \frac{1 + 2\alpha}{2\alpha q^2} \cdot \frac{1}{2}\Big(\mu^2 + \frac{1}{q}\Big).$$

The first term is $\frac{4(1 + 2\alpha)}{2\alpha(9 + 2\alpha)} \cdot \frac{q - 1}{q^2}$ and the second is $\frac{4(1 + 2\alpha)}{2\alpha(9 + 2\alpha)} \cdot \frac{\mu^2 + 1/q}{q^2}$. Their sum is $C (q - 1 + \mu^2 + 1/q)/q^2 = C f(q)$. $\square$

**Theorem (exactness).** KAHN($\alpha$) ends with probability 1, the number of tries has the geometric law with success probability $p = C \int_I f$, and the returned $q$ has the density $f/\int_I f$ on $I$. So the returned $\mu$ has the Klein-Nishina law and $\alpha' = \alpha/q$ is the Compton energy.

*Proof.* By Lemma 4 with $A = I$, each try accepts with probability $p > 0$ ($f > 0$ on $I$), independently of the other tries. So the number of tries is geometric and finite with probability 1. The returned value is the value of the first accepted try. Because tries are independent and identical, its law is the law of $q$ in one try given acceptance: $P(q \in A) = C \int_A f / (C \int_I f)$. Lemma 1 turns this into the Klein-Nishina law of $\mu$. $\blacksquare$

**The efficiency.** $p(\alpha) = C \int_1^{1 + 2\alpha} f(q)\, dq$. As $\alpha \to 0$, put $q = 1 + \alpha(1 - \mu)$; then $f \to 1 + \mu^2$, $dq = \alpha\, d\mu$, and $\int_I f \approx \alpha \int_{-1}^1 (1 + \mu^2)\, d\mu = 8\alpha/3$, while $C \approx 4/(18\alpha)$. So $p \to 32/54 = 16/27 \approx 0.593$. The same limit shows that the accepted law tends to the Thomson law $\frac{3}{8}(1 + \mu^2)$, which has $E[\mu^2] = 2/5$.
