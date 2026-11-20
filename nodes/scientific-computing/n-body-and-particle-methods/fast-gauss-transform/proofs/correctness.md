---
title: The fast Gauss transform with p terms per coordinate and range n_r has error at most Q (2ε_p + ε_p² + e^{-n_r²/4})
proves: [correctness]
status: full
---

We use exact arithmetic and the scaled coordinates $x / \sqrt{\delta}$, in which the kernel is $e^{-|x - y|^2}$ and the boxes have side $\frac12$. So a point and the center of its box differ by at most $\frac14$ in each coordinate. Let $h_n(x) = (-1)^n \frac{d^n}{dx^n} e^{-x^2} = H_n(x) e^{-x^2}$, where $H_n$ is the Hermite polynomial, and let $Q = \sum_j |q_j|$.

**The double series.** Fix a source $y$ in box $B$ (center $c_B$) and a target $x$ in box $C$ (center $c_C$), and look at one coordinate. Write $a = y - c_B$, $u = x - c_C$ and $w = c_C - c_B$, so $x - y = w + u - a$ and $|a|, |u| \le \frac14$. Taylor's theorem for the entire function $f(z) = e^{-z^2}$ gives $f(z - a) = \sum_m \frac{(-a)^m}{m!} f^{(m)}(z) = \sum_m \frac{a^m}{m!} h_m(z)$, and since $h_m^{(n)} = (-1)^n h_{m+n}$, also $h_m(w + u) = \sum_n \frac{u^n}{n!} (-1)^n h_{m+n}(w)$. Hence

$$e^{-(w + u - a)^2} = \sum_{m \ge 0} \sum_{n \ge 0} T(m, n), \qquad T(m, n) = \frac{a^m}{m!} \frac{u^n}{n!} (-1)^n h_{m+n}(w),$$

with absolute convergence by Lemma 1 below.

**The four ways compute partial sums.** In one coordinate, line L2 (direct) computes the full sum. Line L4 (Hermite to targets) computes $\sum_{m < p} \frac{a^m}{m!} h_m(w + u) = \sum_{m < p} \sum_n T(m, n)$. Line L3 (sources to Taylor) computes $\sum_{n < p} \frac{u^n}{n!} h_n(a - w)$; since $h_n(-z) = (-1)^n h_n(z)$ and $\sum_m \frac{(-a)^m}{m!} h_n^{(m)}(w) = h_n(w - a)$, this is $\sum_{n < p} \sum_m T(m, n)$. Line L5 with line L6 (Hermite to Taylor) computes $\sum_{m < p} \sum_{n < p} T(m, n)$: the Taylor coefficient of order $n$ is $\frac{(-1)^n}{n!} \sum_{m < p} A_m h_{m+n}(w)$, with the Hermite coefficients $A_m = \sum q \frac{a^m}{m!}$. In 2D, the coefficients are products over the two coordinates, so for each source the algorithm computes the product $g_1 g_2$ of two such partial sums, while the true term is $f_1 f_2$ with $f_k = e^{-(x_k - y_k)^2}$. In every case the omitted terms of a coordinate have $m \ge p$ or $n \ge p$.

**Lemma 1 (tails).** Let $C_0 = \sum_{n \ge 0} 2^{-n} / \sqrt{n!}$ and $\sigma_p = \sum_{n \ge p} 2^{-n} / \sqrt{n!}$. Then $\sum_{m \ge p \text{ or } n \ge p} |T(m, n)| \le \varepsilon_p := 2 K C_0 \sigma_p$, where $K = 1.09$.

*Proof.* Cramér's inequality for Hermite polynomials, as stated in Section 2 of Greengard and Strain (1991), says $|H_k(z)| \le K 2^{k/2} \sqrt{k!} \, e^{z^2/2}$ for all real $z$, with $K < 1.09$, so $|h_k(w)| \le K 2^{k/2} \sqrt{k!}$. Since $\binom{m+n}{m} \le 2^{m+n}$, we have $(m + n)! \le 2^{m+n} m! \, n!$. With $|a|, |u| \le \frac14$,

$$|T(m, n)| \le \frac{4^{-m-n}}{m! \, n!} K \, 2^{(m+n)/2} \, 2^{(m+n)/2} \sqrt{m! \, n!} = K \frac{2^{-m}}{\sqrt{m!}} \frac{2^{-n}}{\sqrt{n!}}.$$

The sum over $m \ge p$ and all $n$ is at most $K \sigma_p C_0$, and so is the sum over $n \ge p$ and all $m$. $\square$

**Lemma 2 (range).** If $B$ is more than $n_r$ boxes from $C$ in some coordinate, then every source $y$ in $B$ and target $x$ in $C$ satisfy $e^{-|x - y|^2} \le e^{-n_r^2 / 4}$.

*Proof.* The index difference is at least $n_r + 1$, so at least $n_r$ whole boxes of side $\frac12$ lie between $B$ and $C$ in that coordinate, and $|x - y| \ge n_r / 2$. $\square$

**Theorem.** For every target $t_i$, the output $\tilde G(t_i)$ of the algorithm satisfies

$$|\tilde G(t_i) - G(t_i)| \le Q \, \big( 2 \varepsilon_p + \varepsilon_p^2 + e^{-n_r^2 / 4} \big).$$

*Proof.* Each source contributes through exactly one pair of boxes, the pair of its box and the box of $t_i$, so the error is a sum over sources. For a source in a skipped box, the error is $|q_j| e^{-|x - y|^2} \le |q_j| e^{-n_r^2/4}$ by Lemma 2. For any other source, by Lemma 1, $|f_k - g_k| \le \varepsilon_p$, and $|f_k| \le 1$, so $|g_1| \le 1 + \varepsilon_p$ and

$$|f_1 f_2 - g_1 g_2| \le |f_1 - g_1| \, |f_2| + |g_1| \, |f_2 - g_2| \le \varepsilon_p + (1 + \varepsilon_p) \varepsilon_p.$$

Multiply by $|q_j|$ and add. $\square$

For $p = 4, 6, 8, 10, 12$, the factor $2 \varepsilon_p + \varepsilon_p^2$ is about $1.3 \times 10^{-1}$, $5.4 \times 10^{-3}$, $1.8 \times 10^{-4}$, $4.7 \times 10^{-6}$ and $2.1 \times 10^{-7}$. The bound does not depend on $N$, $M$, the positions or $\delta$, and it decays faster than geometrically in $p$, since $\sigma_p$ is about $2^{-p} / \sqrt{p!}$.
