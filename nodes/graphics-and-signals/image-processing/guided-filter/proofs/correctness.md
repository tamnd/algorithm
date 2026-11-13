---
title: Line L3 of GUIDED-FILTER gives the unique minimizer of each window's regularized least squares fit, and line L5 averages the fits of all windows that hold a pixel
proves: [correctness]
status: full
---

Let $D$ be the set of pixels of an image with $W \ge 1$ columns and $H \ge 1$ rows. For $k \in D$, let $w_k = \{i \in D : |i_x - k_x| \le r,\ |i_y - k_y| \le r\}$ be the cut window and $n_k = |w_k| \ge 1$, since $k \in w_k$. For an image $X$, $\mathrm{mean}(X)[k] = \frac{1}{n_k} \sum_{i \in w_k} X_i$; the [integral image](/integral-image/) page proves that its BOX-MEAN returns this value. Fix $\varepsilon > 0$.

**Lemma 1 (window statistics).** After lines L1 and L2, for every $k \in D$,

$$\mathrm{var}_k = \frac{1}{n_k} \sum_{i \in w_k} (I_i - \mu_k)^2 \ge 0, \qquad \mathrm{cov}_k = \frac{1}{n_k} \sum_{i \in w_k} (I_i - \mu_k)(p_i - \bar p_k).$$

*Proof.* Expand the right sides. $\frac{1}{n_k}\sum (I_i - \mu_k)^2 = \frac{1}{n_k}\sum I_i^2 - 2\mu_k \frac{1}{n_k}\sum I_i + \mu_k^2 = c_{II}[k] - \mu_k^2$, because $\frac{1}{n_k} \sum_{i \in w_k} I_i = \mu_k$. In the same way, $\frac{1}{n_k}\sum (I_i - \mu_k)(p_i - \bar p_k) = c_{Ip}[k] - \mu_k \bar p_k - \bar p_k \mu_k + \mu_k \bar p_k = c_{Ip}[k] - \mu_k \bar p_k$. The variance is a mean of squares, so it is nonnegative. $\square$

**Lemma 2 (the fit).** For every $k$, the function $E_k(a, b) = \sum_{i \in w_k} ((a I_i + b - p_i)^2 + \varepsilon a^2)$ has exactly one minimizer, and it is the pair $(a_k, b_k)$ of line L3.

*Proof.* $E_k$ is a quadratic polynomial in $(a, b)$. Its Hessian is twice the matrix

$$M = \begin{pmatrix} \sum_i I_i^2 + n_k \varepsilon & \sum_i I_i \\ \sum_i I_i & n_k \end{pmatrix},$$

with sums over $w_k$. Here $n_k > 0$ and $\det M = n_k \sum_i I_i^2 + n_k^2 \varepsilon - (\sum_i I_i)^2 = n_k^2 (\mathrm{var}_k + \varepsilon) > 0$ by Lemma 1, so $M$ is positive definite, $E_k$ is strictly convex, and its unique minimizer is the unique zero of its gradient. Setting $\partial E_k / \partial b = 2 \sum_i (a I_i + b - p_i) = 0$ and dividing by $2 n_k$ gives $a \mu_k + b = \bar p_k$, so $b = \bar p_k - a \mu_k$. Setting $\partial E_k / \partial a = 2 \sum_i (I_i (a I_i + b - p_i) + \varepsilon a) = 0$ and dividing by $2 n_k$ gives $a\, c_{II}[k] + b \mu_k - c_{Ip}[k] + \varepsilon a = 0$. Substituting $b$:

$$a\,(c_{II}[k] - \mu_k^2 + \varepsilon) = c_{Ip}[k] - \mu_k \bar p_k, \quad\text{that is}\quad a\,(\mathrm{var}_k + \varepsilon) = \mathrm{cov}_k.$$

Since $\mathrm{var}_k + \varepsilon > 0$, $a = \mathrm{cov}_k / (\mathrm{var}_k + \varepsilon)$, which with the value of $b$ is line L3. $\square$

**Lemma 3 (the windows that hold a pixel).** For $i, k \in D$, $i \in w_k$ if and only if $k \in w_i$. Hence $\{k \in D : i \in w_k\} = w_i$.

*Proof.* Both conditions say $|i_x - k_x| \le r$ and $|i_y - k_y| \le r$, which is symmetric in $i$ and $k$. $\square$

**Theorem.** GUIDED-FILTER returns, for every $i \in D$,

$$q_i = \frac{1}{n_i} \sum_{k \,:\, i \in w_k} (a_k I_i + b_k),$$

where $(a_k, b_k)$ is the unique minimizer of $E_k$, that is, the mean over all windows that hold $i$ of the value their best fit gives at $i$.

*Proof.* By Lemma 2, line L3 stores the minimizer of $E_k$ for every $k$. Line L4 gives $\bar a_i = \frac{1}{n_i} \sum_{k \in w_i} a_k$ and $\bar b_i = \frac{1}{n_i} \sum_{k \in w_i} b_k$, and line L5 returns $\bar a_i I_i + \bar b_i = \frac{1}{n_i} \sum_{k \in w_i} (a_k I_i + b_k)$. By Lemma 3, the index set $w_i$ is the set of $k$ with $i \in w_k$. $\blacksquare$

**Corollary (constants).** If $p \equiv c$, then $\bar p_k = c$ and $\mathrm{cov}_k = 0$ for every $k$, so $a_k = 0$, $b_k = c$, and $q \equiv c$ for every guide $I$.
