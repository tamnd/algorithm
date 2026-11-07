---
title: GOERTZEL returns X_k with n + 1 multiplications and 2n + 1 additions, and its rounding error is at most (13u + η + μ)(n + 2) M ‖x‖_1 to first order
proves: [correctness, complexity]
status: full
---

**Statement.** Let $R$ be a commutative ring, $n \ge 1$, $\omega \in R$ with $\omega^n = 1$, $k$ an integer, $z = \omega^{-k}$ and $c = z + z^{-1}$. For every $x \in R^n$, GOERTZEL returns $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$, using exactly $n + 1$ multiplications and $2n + 1$ additions and subtractions in $R$, besides computing $z$ and $c$. Over $\mathbb{C}$ with $\omega = e^{-2\pi i/n}$, in floating-point arithmetic with unit roundoff $u$, if the constants are computed with $|\hat c - c| \le \eta$ and $|\hat z - z| \le \mu$, then to first order in $u$ (dropping terms of order $u^2$, $u\eta$ and $u\mu$)

$$|\hat X_k - X_k| \le (13u + \eta + \mu)(n + 2)\, M\, \lVert x \rVert_1, \qquad M = \min\left(n, \frac{1}{|\sin(2\pi k/n)|}\right),$$

with $M = n$ when $\sin(2\pi k/n) = 0$.

**The sequence.** Let $s_{-2} = s_{-1} = 0$ and $s_j = x_j + c\, s_{j-1} - s_{j-2}$ for $0 \le j < n$. By induction on the loop at line L4, after the iteration for $j$ the variables hold $s_1 = s_j$ and $s_2 = s_{j-1}$: before the loop they hold $s_{-1}$ and $s_{-2}$ (line L3), and lines L5 and L6 compute $s_j$ from them and shift. So line L7 returns $z s_{n-1} - s_{n-2}$.

**Lemma 1 (Horner).** For $j \ge 0$ let $y_j = \sum_{i=0}^{j} x_i z^{j-i}$. Then $y_j = s_j - z^{-1} s_{j-1}$. *Proof.* For $j = 0$: $y_0 = x_0 = s_0 - z^{-1} s_{-1}$. If it holds for $j$, then $y_{j+1} = z y_j + x_{j+1} = z s_j - s_{j-1} + x_{j+1}$, using $z z^{-1} = 1$, while $s_{j+1} - z^{-1} s_j = x_{j+1} + (c - z^{-1}) s_j - s_{j-1} = x_{j+1} + z s_j - s_{j-1}$, using $c - z^{-1} = z$. $\square$

**Correctness.** Since $\omega^n = 1$, $z^n = \omega^{-kn} = 1$, so $\omega^{jk} = z^{-j} = z^{n-j} = z \cdot z^{n-1-j}$. Hence $X_k = z \sum_j x_j z^{n-1-j} = z\, y_{n-1} = z s_{n-1} - s_{n-2}$ by Lemma 1, which is the value returned. Over $\mathbb{C}$, $z = e^{2\pi i k/n}$ and $c = 2\cos(2\pi k/n)$ is real.

**Operation count.** Each of the $n$ iterations of line L5 does one multiplication $c \cdot s_1$, one addition and one subtraction; line L6 only moves values. Line L7 does one multiplication and one subtraction. The total is $n + 1$ multiplications and $2n + 1$ additions and subtractions, for every input. The space is the three variables $s, s_1, s_2$ and the two constants, $\Theta(1)$.

**Lemma 2 (the propagation factors).** Let $U_{-1} = 0$, $U_0 = 1$ and $U_m = c U_{m-1} - U_{m-2}$ for $m \ge 1$. Then (a) $z U_m - U_{m-1} = z^{m+1}$ for $m \ge 0$; (b) $s_j = \sum_{i=0}^{j} U_{j-i} x_i$; (c) over $\mathbb{C}$ with $c = 2\cos\theta$, $|U_m| \le \min(m + 1, 1/|\sin\theta|)$. *Proof.* (a) For $m = 0$ it reads $z = z$. For $m \ge 1$, $z U_m - U_{m-1} = (z c - 1) U_{m-1} - z U_{m-2}$, and $z c - 1 = z^2$, so this is $z (z U_{m-1} - U_{m-2}) = z \cdot z^m$ by induction. (b) Both sides satisfy the recurrence $t_j = x_j + c t_{j-1} - t_{j-2}$ with $t_{-1} = t_{-2} = 0$, by linearity. (c) $U_m$ is the Chebyshev polynomial of the second kind at $\cos\theta$, and $U_m(\cos\theta) = \sin((m+1)\theta)/\sin\theta$ when $\sin\theta \ne 0$ (this satisfies the same recurrence, by $\sin((m+1)\theta) + \sin((m-1)\theta) = 2\cos\theta \sin(m\theta)$), which gives the bound $1/|\sin\theta|$. Also $U_m = \sum_{r=0}^{m} e^{i(m - 2r)\theta}$ (both sides are $1$ and $2\cos\theta$ for $m = 0, 1$ and satisfy the recurrence, since multiplying the sum for $m - 1$ by $e^{i\theta} + e^{-i\theta}$ gives the sums for $m$ and $m - 2$), so $|U_m| \le m + 1$. $\square$

By (b) and (c), with $\theta = 2\pi k/n$ and $j \le n - 1$, $|s_j| \le M \lVert x \rVert_1$.

**The rounding errors of the loop.** We use the standard model $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$, $|\delta| \le u$, for real operations. Since $\hat c$ is real, each operation of line L5 acts on the real and imaginary parts separately. For one real component, $\hat s = \mathrm{fl}(\mathrm{fl}(x + \mathrm{fl}(\hat c\, \hat s_1)) - \hat s_2)$ equals $x + \hat c \hat s_1 - \hat s_2 + e$ with $|e| \le 3u (|x| + |\hat c \hat s_1| + |\hat s_2|)$ to first order. Adding the bounds of the two components and using $|a_r| + |a_i| \le \sqrt 2 |a|$ gives, for the complex values,

$$\hat s_j = x_j + c\, \hat s_{j-1} - \hat s_{j-2} + f_j, \qquad |f_j| \le 3\sqrt2\, u (|x_j| + 2|s_{j-1}| + |s_{j-2}|) + \eta |s_{j-1}|,$$

to first order, where $f_j$ also absorbs $(\hat c - c)\hat s_{j-1}$ and we used $|\hat c| \le 2 + \eta$. The differences $d_j = \hat s_j - s_j$ satisfy $d_j = c d_{j-1} - d_{j-2} + f_j$ with $d_{-1} = d_{-2} = 0$, so by Lemma 2(b), $d_j = \sum_{i \le j} U_{j-i} f_i$. Then by Lemma 2(a),

$$z \hat s_{n-1} - \hat s_{n-2} - X_k = z d_{n-1} - d_{n-2} = \sum_{i=0}^{n-1} f_i (z U_{n-1-i} - U_{n-2-i}) = \sum_{i=0}^{n-1} f_i z^{n-i},$$

and since $|z| = 1$ its modulus is at most $\sum_i |f_i| \le 3\sqrt2\, u \lVert x \rVert_1 + (9\sqrt2\, u + \eta)\, n M \lVert x \rVert_1$, using $|s_j| \le M \lVert x \rVert_1$.

**The rounding errors of line L7.** For a complex product, $\mathrm{fl}(a b) = a b (1 + \delta)$ with $|\delta| \le \sqrt2 \gamma_2 = 2\sqrt2 u$ to first order (Higham, Lemma 3.5), and a complex subtraction has relative error at most $u$. So $\hat X_k = (\hat z \hat s_{n-1} (1 + \delta_1) - \hat s_{n-2})(1 + \delta_2)$, and $\hat X_k - (z \hat s_{n-1} - \hat s_{n-2})$ has modulus at most $\mu |s_{n-1}| + 2\sqrt2 u |s_{n-1}| + u |X_k|$ to first order, which is at most $(\mu + 2\sqrt2 u) M \lVert x \rVert_1 + u \lVert x \rVert_1$.

**The bound.** Adding the two parts,

$$|\hat X_k - X_k| \le \left[(9\sqrt2\, u + \eta)\, n M + (3\sqrt2 + 1) u + (2\sqrt2 u + \mu) M\right] \lVert x \rVert_1.$$

Now $9\sqrt 2 < 13$, and since $M \ge 1$, $(3\sqrt2 + 1) u + (2\sqrt2 u + \mu) M \le (8.1 u + \mu) M \le 2 (13 u + \mu) M$. So the right side is at most $(13 u + \eta + \mu)(n + 2) M \lVert x \rVert_1$. $\blacksquare$

**Remark.** The implementation computes $\hat z$ by `cmath.exp` and $\hat c = 2 \operatorname{Re} \hat z$, so $\eta \le 2\mu$; the tests assume $\mu \le 2u$ for the library exponential, hence $\eta + \mu \le 6u$, and use the constant $20 \ge 13 + 7$.
