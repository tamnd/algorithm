---
title: The fast Walsh-Hadamard step is exact, HD flattens vectors, and the sparse or sampled projection keeps norms
proves: [correctness]
status: full
---

Let $d = 2^m$. Write $W_d$ for the unnormalized Sylvester-Hadamard matrix, $(W_d)_{ij} = (-1)^{\langle i, j \rangle}$ with indices $0, \ldots, d - 1$ and $\langle i, j \rangle$ the number of common 1 bits, so that $H = d^{-1/2} W_d$.

**Lemma 1 (the butterfly computes $W_d$).** Lines L5 to L8 turn the vector $a$ into $W_d a$.

*Proof.* For $i < 2h$ with $h$ a power of two, the top bit of $i$ is bit $\log_2 h$, so

$$W_{2h} = \begin{pmatrix} W_h & W_h \\ W_h & -W_h \end{pmatrix}.$$

Claim: when the loop of line L6 starts with the value $h$, every block of $h$ consecutive entries that starts at a multiple of $h$ holds $W_h$ times the matching block of the input. For $h = 1$ this holds because $W_1 = (1)$. Suppose it holds for $h$. Line L7 takes a block of length $2h$ whose halves hold $W_h a'$ and $W_h a''$, and puts $W_h a' + W_h a''$ in the first half and $W_h a' - W_h a''$ in the second half. By the block form this is $W_{2h}(a', a'')$, so the claim holds for $2h$ after line L8. When the loop stops, $h = d$ and the single block holds $W_d a$. $\square$

Each round does $d/2$ butterflies with one addition and one subtraction, so the transform uses $d \log_2 d$ additions and subtractions. The arithmetic is exact on integers.

**Lemma 2 (norms are kept).** $W_d W_d^{\mathsf T} = d I$, so $H$ is orthogonal; $D$ is orthogonal; hence $\|H D x\| = \|x\|$.

*Proof.* Row $i$ times row $i'$ of $W_d$ is $\sum_j (-1)^{\langle i, j \rangle + \langle i', j \rangle} = \sum_j (-1)^{\langle i \oplus i', j \rangle}$, where $\oplus$ is bitwise exclusive or. If $i = i'$ the sum is $d$. Otherwise $i \oplus i'$ has some bit $b$ set, and pairing each $j$ with $j \oplus 2^b$ flips the sign of the term, so the sum is 0. $D$ is diagonal with entries $\pm 1$. $\square$

**Lemma 3 (Hoeffding for random signs).** Let $\sigma_1, \ldots, \sigma_d$ be independent uniform signs and $a \in \mathbb{R}^d$. Then $\Pr\big[|\sum_j \sigma_j a_j| \ge t\big] \le 2 e^{-t^2 / (2\|a\|^2)}$.

*Proof.* For real $y$, $\cosh y = \sum_m y^{2m}/(2m)! \le \sum_m (y^2/2)^m / m! = e^{y^2/2}$, since $(2m)! \ge 2^m m!$. So $\mathbb{E} e^{\lambda \sum_j \sigma_j a_j} = \prod_j \cosh(\lambda a_j) \le e^{\lambda^2 \|a\|^2 / 2}$. By Markov's inequality, $\Pr[\sum_j \sigma_j a_j \ge t] \le e^{-\lambda t + \lambda^2\|a\|^2/2}$, and $\lambda = t / \|a\|^2$ gives $e^{-t^2/(2\|a\|^2)}$. The lower tail is the same by symmetry. $\square$

**Theorem 1 (flattening).** Let $x_1, \ldots, x_n \in \mathbb{R}^d$ and $s = \sqrt{2 \ln(40 n d) / d}$. With probability at least $19/20$ over $D$, $\|H D x_i\|_\infty \le s \|x_i\|$ for every $i$.

*Proof.* Coordinate $l$ of $HDx$ is $\sum_j \sigma_j a_j$ with $\sigma_j = D_{jj}$ and $a_j = d^{-1/2} (W_d)_{lj} x_j$, so $\|a\|^2 = \|x\|^2 / d$. By Lemma 3 with $t = s\|x\|$, $\Pr[|(HDx)_l| \ge s\|x\|] \le 2 e^{-s^2 d / 2} = 2/(40 n d)$. A union bound over the $n d$ pairs $(i, l)$ gives failure probability at most $1/20$. $\square$

When $\log d = O(\log n)$ this is the bound $\|HDx\|_\infty = O(\sqrt{\log n / d})\,\|x\|$ in the proof of Lemma 1 of Ailon and Chazelle.

**Theorem 2 (the sparse Gaussian projection).** Fix $u$ with $\|u\| = 1$ and let $P_r$ be one row of $P$. Then $\mathbb{E}(P_r u)^2 = 1$ and

$$\operatorname{Var}(P_r u)^2 = 2 + 3\,\frac{1 - q}{q} \sum_j u_j^4 .$$

So $\mathbb{E}\|\Phi x\|^2 = \|x\|^2$ for every $x$, and if $\|u\|_\infty^2 \le s^2$ then the variance of one row is at most $2 + 3 s^2 / q$.

*Proof.* Write $P_{rj} = b_j g_j / \sqrt{q}$ with independent $b_j \sim$ Bernoulli$(q)$ and $g_j \sim N(0, 1)$. Given $b$, $P_r u \sim N(0, V)$ with $V = \sum_j b_j u_j^2 / q$. So $\mathbb{E}[(P_r u)^2 \mid b] = V$ and $\mathbb{E}[(P_r u)^4 \mid b] = 3V^2$. Now $\mathbb{E} V = \sum_j u_j^2 = 1$ and $\operatorname{Var} V = \sum_j u_j^4\, q(1 - q)/q^2$. Hence $\mathbb{E}(P_r u)^2 = 1$ and $\operatorname{Var}(P_r u)^2 = 3(1 + \operatorname{Var} V) - 1$, which is the formula. With $u = HDx / \|x\|$ and Lemma 2, $\mathbb{E}\|\Phi x\|^2 = \frac{1}{k}\sum_r \mathbb{E}(P_r HDx)^2 = \|x\|^2$. Finally $\sum_j u_j^4 \le \|u\|_\infty^2 \sum_j u_j^2 \le s^2$. $\square$

With $s^2 = O(\log n / d)$ from Theorem 1 and $q = \Theta(\log^2 n / d)$, the variance of a row is $O(1)$, the same order as for a dense Gaussian row; without $HD$ the spike $u = e_1$ would give variance about $3/q$. The tail bound with $k = O(\varepsilon^{-2}\log n)$ is Lemma 1 of Ailon and Chazelle (SIAM Journal on Computing 39(1), 2009), which bounds the higher moments of $\sum_r (P_r u)^2$ given the flat event.

**Theorem 3 (the SRHT).** Let $x_1, \ldots, x_n \in \mathbb{R}^d$ be nonzero, $0 < \varepsilon < 1$, and

$$k \ge \frac{6}{\varepsilon^2}\, \ln(40 n d)\, \ln(40 n).$$

Let $c_1, \ldots, c_k$ be independent and uniform in $\{0, \ldots, d - 1\}$, independent of $D$, and $\Psi x = \sqrt{d/k}\,(HDx)_{c_1, \ldots, c_k}$. With probability at least $9/10$, $(1 - \varepsilon)\|x_i\|^2 \le \|\Psi x_i\|^2 \le (1 + \varepsilon)\|x_i\|^2$ for every $i$.

*Proof.* Condition on a $D$ for which the event of Theorem 1 holds; this fails with probability at most $1/20$. Fix $i$, let $u = HDx_i / \|x_i\|$, and let $Y_t = d\, u_{c_t}^2$. The $Y_t$ are independent, $\mathbb{E} Y_t = \sum_l u_l^2 = 1$, and $0 \le Y_t \le d s^2 = 2\ln(40nd) =: M$. Also $\|\Psi x_i\|^2 / \|x_i\|^2 = \frac{1}{k}\sum_t Y_t$. The Chernoff bound for independent variables in $[0, M]$ with total mean $\mu = k$ gives

$$\Pr\Big[\Big|\sum_t Y_t - k\Big| > \varepsilon k\Big] \le e^{-\varepsilon^2 k / (3M)} + e^{-\varepsilon^2 k / (2M)} \le 2 e^{-\varepsilon^2 k / (6 \ln(40nd))} \le 2 e^{-\ln(40 n)} = \frac{1}{20 n}.$$

A union bound over the $n$ vectors gives failure probability at most $1/20$ given $D$. In total the failure probability is at most $1/20 + 1/20 = 1/10$. $\square$

For distances among $N$ points, apply Theorem 3 to the $n = N(N - 1)/2$ differences.
