---
title: The frequency counts, and the Cauchy-Schwarz lower bound behind Chao1
proves: [correctness]
status: full
---

**Setting.** A community has $S \ge 2$ species with abundances $p_1, \ldots, p_S$, all in $(0, 1)$, with $\sum_i p_i = 1$. A sample of $n \ge 2$ individuals is drawn by multinomial sampling: each individual is of species $i$ with probability $p_i$, independently of the others. Let $X_i$ be the number of individuals of species $i$, and $f_k = |\{i : X_i = k\}|$.

**Claim 1 (the counts).** Lines L1 to L3 return $n$, $S_{obs} = |\{i : X_i \ge 1\}|$, $f_1$ and $f_2$.

*Proof.* Line L1 adds 1 to the count of the label of each individual, once per individual. So after line L1, each label that occurs in the sample is a key, and its value is the number of individuals with that label, which is $X_i$ for species $i$. Labels that do not occur are not keys. Line L2 returns the length of the sample, $n$, and the number of keys, $S_{obs}$. Line L3 counts the keys with value 1 and with value 2, which are $f_1$ and $f_2$. $\square$

**Claim 2 (the expected frequency counts).** $\mathbb{E}[f_k] = \sum_{i=1}^{S} \binom{n}{k} p_i^k (1 - p_i)^{n - k}$ for $0 \le k \le n$, and $S = \mathbb{E}[S_{obs}] + \mathbb{E}[f_0]$.

*Proof.* $X_i$ has the binomial law with parameters $n$ and $p_i$, so $\Pr(X_i = k) = \binom{n}{k} p_i^k (1 - p_i)^{n - k}$. Write $f_k = \sum_i \mathbf{1}[X_i = k]$ and use linearity of expectation. Every species has either $X_i = 0$ or $X_i \ge 1$, so $S = f_0 + S_{obs}$ for every sample, and the second statement follows by taking expectations. $\square$

**Claim 3 (the lower bound).** $\mathbb{E}[f_2] > 0$, and

$$\mathbb{E}[f_0] \ge \frac{n - 1}{n} \cdot \frac{\mathbb{E}[f_1]^2}{2\, \mathbb{E}[f_2]},$$

with equality if and only if $p_1 = p_2 = \cdots = p_S$.

*Proof.* Step 1. Each term of $\mathbb{E}[f_2]$ in Claim 2 is positive, because $0 < p_i < 1$ and $n \ge 2$. So $\mathbb{E}[f_2] > 0$.

Step 2. Let $a_i = (1 - p_i)^{n/2}$ and $b_i = p_i (1 - p_i)^{n/2 - 1}$. Both are positive. Then $a_i^2 = (1 - p_i)^n$, $a_i b_i = p_i (1 - p_i)^{n - 1}$ and $b_i^2 = p_i^2 (1 - p_i)^{n - 2}$. By Claim 2,

$$\sum_i a_i^2 = \mathbb{E}[f_0], \qquad \sum_i a_i b_i = \frac{\mathbb{E}[f_1]}{n}, \qquad \sum_i b_i^2 = \frac{2\, \mathbb{E}[f_2]}{n (n - 1)}.$$

Step 3. The Cauchy-Schwarz inequality gives $\left(\sum_i a_i b_i\right)^2 \le \sum_i a_i^2 \sum_i b_i^2$, so

$$\frac{\mathbb{E}[f_1]^2}{n^2} \le \mathbb{E}[f_0] \cdot \frac{2\, \mathbb{E}[f_2]}{n (n - 1)}.$$

Multiply by $n (n - 1) / (2\, \mathbb{E}[f_2]) > 0$ to get the claim.

Step 4. Equality holds in Cauchy-Schwarz if and only if the vectors $(a_i)$ and $(b_i)$ are proportional. Since $a_i > 0$, this means that $b_i / a_i = p_i / (1 - p_i)$ is the same for all $i$. The map $p \mapsto p / (1 - p)$ is strictly increasing on $(0, 1)$, so this holds if and only if all $p_i$ are equal. $\square$

**Claim 4 (Poisson sampling).** If instead the $X_i$ are independent with Poisson laws of means $\lambda_i > 0$, then $\mathbb{E}[f_0] \ge \mathbb{E}[f_1]^2 / (2\, \mathbb{E}[f_2])$, with equality if and only if all $\lambda_i$ are equal.

*Proof.* Now $\mathbb{E}[f_k] = \sum_i e^{-\lambda_i} \lambda_i^k / k!$. Take $a_i = e^{-\lambda_i / 2}$ and $b_i = \lambda_i e^{-\lambda_i / 2}$. Then $\sum a_i^2 = \mathbb{E}[f_0]$, $\sum a_i b_i = \mathbb{E}[f_1]$ and $\sum b_i^2 = 2\, \mathbb{E}[f_2]$, and Cauchy-Schwarz gives the bound. Equality holds if and only if $b_i / a_i = \lambda_i$ is constant. $\square$

**Claim 5 (what lines L4 to L6 compute).** Line L6 returns $S_{obs} + f_1^2 / (2 f_2)$ when $f_2 \ge 1$, and Chao's variance formula $f_2 (q^4/4 + q^3 + q^2/2)$ with $q = f_1 / f_2$. Line L4 returns $S_{obs} + f_1 (f_1 - 1)/(2 (f_2 + 1))$ for every sample. Both are $\ge S_{obs}$. If $f_1 \ge 1$ and $f_2 \ge 1$, the value of line L4 is less than the value of line L6.

*Proof.* Line L6 computes $q f_1 / 2 = f_1^2 / (2 f_2)$, so the first statement holds, and the variance is the formula as written. Both corrections are products and quotients of numbers $\ge 0$, so both estimates are $\ge S_{obs}$. If $f_1 \ge 1$ and $f_2 \ge 1$, then $0 \le f_1 (f_1 - 1) < f_1^2$ and $2 (f_2 + 1) > 2 f_2 > 0$, so $f_1 (f_1 - 1) / (2 (f_2 + 1)) < f_1^2 / (2 f_2)$. $\square$

**Conclusion.** By Claims 2 and 3, $S = \mathbb{E}[S_{obs}] + \mathbb{E}[f_0] \ge \mathbb{E}[S_{obs}] + \frac{n - 1}{n} \mathbb{E}[f_1]^2 / (2\, \mathbb{E}[f_2])$ for every community. Line L6 evaluates the same expression with the observed $S_{obs}$, $f_1$ and $f_2$ in place of their expected values (and without the factor $(n - 1)/n$, which is the Poisson form of Claim 4). By Claim 1, the inputs of this expression are computed exactly. So the algorithm returns the plug-in estimate of a lower bound of $S$, and this lower bound is equal to $S$ exactly when all species are equally abundant. The step from expected to observed counts is an estimate, and no claim on its error is made here. $\blacksquare$
