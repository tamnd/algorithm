---
title: Sparse random projection is unbiased, has the stated variance, and keeps distances for s = 1 and s = 3
proves: [correctness]
status: full
---

Lines L4 to L6 make each entry $R_{ij}$ of the $d \times k$ matrix independent, with $R_{ij} = +\sqrt{s}$ with probability $1/(2s)$, $R_{ij} = -\sqrt{s}$ with probability $1/(2s)$, and $R_{ij} = 0$ otherwise. Line L9 outputs $y = f(x) = x R / \sqrt{k}$. Let $r$ be one column of $R$ and $Q = \langle x, r \rangle^2$. Then $\|f(x)\|^2 = \frac{1}{k} \sum_{j=1}^k Q_j$, where $Q_1, \ldots, Q_k$ are independent copies of $Q$, one for each column.

**Lemma 1 (moments of one entry).** The entry distribution is symmetric, so every odd moment is 0. For $m \ge 1$, $\mathbb{E} R_{ij}^{2m} = \frac{1}{s} \cdot s^m = s^{m-1}$. In particular $\mathbb{E} R_{ij}^2 = 1$ and $\mathbb{E} R_{ij}^4 = s$; for $s = 3$ these are 1 and 3, the values of $N(0, 1)$.

**Theorem 1 (mean and variance).** For every $s \ge 1$ and $x \in \mathbb{R}^d$,

$$\mathbb{E}\|f(x)\|^2 = \|x\|^2, \qquad \operatorname{Var}\|f(x)\|^2 = \frac{1}{k}\Big(2\|x\|^4 + (s - 3)\sum_{i} x_i^4\Big).$$

*Proof.* Write $Q = \sum_{a, b} x_a x_b r_a r_b$. By independence and Lemma 1, $\mathbb{E} r_a r_b$ is 1 if $a = b$ and 0 otherwise, so $\mathbb{E} Q = \sum_a x_a^2 = \|x\|^2$. Next, $Q^2 = \sum_{a, b, c, e} x_a x_b x_c x_e\, r_a r_b r_c r_e$. The expected value of $r_a r_b r_c r_e$ is 0 unless every index value appears an even number of times. Two cases remain. If $a = b = c = e$ the term is $x_a^4\, \mathbb{E} r_a^4 = s\, x_a^4$. If the four positions split into two pairs with different values, there are 3 ways to pair the positions, and each gives $\sum_{a \ne b} x_a^2 x_b^2 = \|x\|^4 - \sum_a x_a^4$. So

$$\mathbb{E} Q^2 = s \sum_a x_a^4 + 3\Big(\|x\|^4 - \sum_a x_a^4\Big), \qquad \operatorname{Var} Q = \mathbb{E} Q^2 - \|x\|^4 = 2\|x\|^4 + (s - 3)\sum_a x_a^4 .$$

The mean of $\frac{1}{k}\sum_j Q_j$ is $\|x\|^2$, and since the $Q_j$ are independent its variance is $\operatorname{Var} Q / k$. $\square$

**Lemma 2 (moment comparison for $s \in \{1, 3\}$).** Let $g_1, \ldots, g_d$ be independent $N(0, 1)$ and $Z \sim N(0, 1)$. For $s \in \{1, 3\}$, every unit vector $x$ and every $m \ge 0$, $\mathbb{E} \langle x, r \rangle^{2m} \le \mathbb{E} Z^{2m}$.

*Proof.* First, $\mathbb{E} R_{ij}^{2j'} = s^{j'-1} \le (2j' - 1)!! = \mathbb{E} g^{2j'}$ for every $j' \ge 1$. For $s = 1$ the left side is 1. For $s = 3$ it is $3^{j'-1} = \prod_{i=2}^{j'} 3 \le \prod_{i=2}^{j'} (2i - 1)$. Now expand $\langle x, r \rangle^{2m} = \sum_{a_1, \ldots, a_{2m}} \prod_t x_{a_t} r_{a_t}$ and group the terms by the multiplicities $m_1, \ldots, m_d$ of the index values. A group has expected value $c \prod_i x_i^{m_i} \prod_i \mathbb{E} r_i^{m_i}$ with a positive integer $c$. If some $m_i$ is odd, the expected value is 0. Otherwise every $x_i^{m_i} \ge 0$ and every $\mathbb{E} r_i^{m_i} \le \mathbb{E} g_i^{m_i}$, so the group is at most the same group with $g$ in place of $r$. Summing, $\mathbb{E}\langle x, r \rangle^{2m} \le \mathbb{E}\langle x, g \rangle^{2m}$. Finally $\langle x, g \rangle \sim N(0, \|x\|^2) = N(0, 1)$, so the right side is $\mathbb{E} Z^{2m}$. $\square$

**Theorem 2 (the Johnson-Lindenstrauss guarantee for $s \in \{1, 3\}$).** Let $0 < \varepsilon < 1$, $c_\varepsilon = \varepsilon^2/2 - \varepsilon^3/3$, and $x \ne 0$. Then

$$\Pr\big[\|f(x)\|^2 \ge (1 + \varepsilon)\|x\|^2\big] \le e^{-k c_\varepsilon / 2}, \qquad \Pr\big[\|f(x)\|^2 \le (1 - \varepsilon)\|x\|^2\big] \le e^{-k \varepsilon^2 / 6}.$$

So for $n \ge 2$ points and $k \ge \max(4 / c_\varepsilon,\ 12 / \varepsilon^2) \ln n$, all pairwise squared distances are within a factor $1 \pm \varepsilon$ with probability at least $1/n$.

*Proof.* By linearity we may take $\|x\| = 1$. Let $S = \sum_{j=1}^k Q_j = k \|f(x)\|^2$.

Upper tail. For $0 \le t < 1/2$, every term of $e^{tQ} = \sum_{m \ge 0} t^m Q^m / m!$ is non-negative, so by Lemma 2 and monotone convergence $\mathbb{E} e^{tQ} \le \mathbb{E} e^{t Z^2} = (1 - 2t)^{-1/2}$. From here the argument is Step 5 of the Gaussian proof on the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) page, word for word: Markov's inequality on $e^{tS}$ with $t = \varepsilon / (2(1 + \varepsilon))$ gives $\Pr[S \ge (1 + \varepsilon) k] \le \exp(\frac{k}{2}(\ln(1 + \varepsilon) - \varepsilon)) \le e^{-k c_\varepsilon / 2}$.

Lower tail. For $y \ge 0$, $e^{-y} \le 1 - y + y^2/2$ (the difference $1 - y + y^2/2 - e^{-y}$ is 0 at $y = 0$ and has derivative $-1 + y + e^{-y} \ge 0$). By Theorem 1 with $\|x\| = 1$ and $s \le 3$, $\mathbb{E} Q = 1$ and $\mathbb{E} Q^2 = 3 + (s - 3)\sum_i x_i^4 \le 3$. So for $t > 0$,

$$\mathbb{E} e^{-tQ} \le 1 - t + \tfrac{3}{2} t^2 \le \exp\big(-t + \tfrac{3}{2} t^2\big).$$

By Markov's inequality on $e^{-tS}$ and independence,

$$\Pr[S \le (1 - \varepsilon) k] \le e^{t (1 - \varepsilon) k} \big(\mathbb{E} e^{-tQ}\big)^k \le \exp\big(k(\tfrac{3}{2} t^2 - t\varepsilon)\big).$$

With $t = \varepsilon / 3$ the exponent is $k(\varepsilon^2/6 - \varepsilon^2/3) = -k\varepsilon^2/6$.

All pairs. Apply both tails to $x = u - v$ for each of the $n(n-1)/2$ pairs. When $k \ge (4 / c_\varepsilon) \ln n$ the upper tail is at most $n^{-2}$, and when $k \ge (12 / \varepsilon^2) \ln n$ the lower tail is at most $n^{-2}$. By the union bound some pair fails with probability at most $\frac{n(n-1)}{2} \cdot \frac{2}{n^2} = 1 - \frac{1}{n}$. $\square$

Achlioptas proves a sharper lower tail, $e^{-k c_\varepsilon / 2}$, by a finer choice of $t$ and a closer estimate of $1 - t + \frac{3}{2}t^2$; with it the bound on $k$ becomes $4 c_\varepsilon^{-1} \ln n$, the same as for a Gaussian matrix. For $s > 3$, Lemma 2 fails at $m = 2$, and Theorem 1 shows that the variance for $x = e_1$ is $(s - 1)/k$ instead of $2/k$.

**Theorem 3 (the block construction).** Let $k = bs$. For each block $\beta = 1, \ldots, s$ let $h_\beta : \{1, \ldots, d\} \to \{1, \ldots, b\}$ be uniform and $\sigma_\beta : \{1, \ldots, d\} \to \{-1, +1\}$ be uniform signs, all independent. Let $S$ have entry $\sigma_\beta(i) / \sqrt{s}$ in row $(\beta, h_\beta(i))$ and column $i$, and 0 elsewhere. Then every column of $S$ has exactly $s$ nonzeros and norm 1, and for every $x$

$$\mathbb{E}\|Sx\|^2 = \|x\|^2, \qquad \operatorname{Var}\|Sx\|^2 = \frac{2}{bs}\Big(\|x\|^4 - \sum_i x_i^4\Big) \le \frac{2\|x\|^4}{k}.$$

*Proof.* Column $i$ has one entry $\pm 1/\sqrt{s}$ in each of the $s$ blocks, so it has $s$ nonzeros and squared norm $s \cdot (1/s) = 1$. Fix a block $\beta$ and write $\eta_{il} = 1$ if $h_\beta(i) = h_\beta(l)$ and 0 otherwise. The rows of block $\beta$ contribute

$$\frac{1}{s} \sum_{\rho = 1}^b \Big(\sum_{i : h_\beta(i) = \rho} \sigma_\beta(i) x_i\Big)^2 = \frac{1}{s}\Big(\|x\|^2 + W_\beta\Big), \qquad W_\beta = 2 \sum_{i < l} \eta_{il}\, \sigma_\beta(i) \sigma_\beta(l)\, x_i x_l .$$

So $\|Sx\|^2 = \|x\|^2 + \frac{1}{s}\sum_\beta W_\beta$. Each term of $W_\beta$ has mean 0 because of the sign $\sigma_\beta(i)\sigma_\beta(l)$ with $i \ne l$, so $\mathbb{E}\|Sx\|^2 = \|x\|^2$. In $\mathbb{E} W_\beta^2$, a product of the terms for pairs $\{i, l\}$ and $\{i', l'\}$ has mean 0 unless the pairs are equal, because otherwise some sign appears exactly once. For equal pairs the mean is $4\, \mathbb{E}\eta_{il}\, x_i^2 x_l^2 = \frac{4}{b} x_i^2 x_l^2$. Hence $\operatorname{Var} W_\beta = \frac{4}{b}\sum_{i < l} x_i^2 x_l^2 = \frac{2}{b}\big(\|x\|^4 - \sum_i x_i^4\big)$. The blocks are independent, so $\operatorname{Var}\|Sx\|^2 = \frac{1}{s^2} \cdot s \cdot \frac{2}{b}\big(\|x\|^4 - \sum_i x_i^4\big)$. $\square$

The tail bound for the block construction, with $s = O(\varepsilon^{-1}\log(1/\delta))$, needs higher moments of $\sum_\beta W_\beta$ and is proved by Kane and Nelson (Journal of the ACM 61(1), 2014).
