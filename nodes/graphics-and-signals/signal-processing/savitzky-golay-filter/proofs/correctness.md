---
title: The Savitzky-Golay weights give the least squares fit, reproduce polynomials, and have a noise gain equal to the center weight
proves: [correctness]
status: full
---

Fix $m \ge 0$ and $0 \le p \le 2m$. Let $I = \{-m, \ldots, m\}$ and $\langle f, g \rangle = \sum_{i \in I} f(i)\, g(i)$. Let $\Pi_p$ be the space of real polynomials of degree at most $p$. For a window $w = (w_{-m}, \ldots, w_m)$ we also write $w$ for the function $i \mapsto w_i$ on $I$.

**Lemma 1 (the basis).** After lines L1 and L2, the polynomials $P_0, \ldots, P_p$ satisfy $\langle P_j, P_k \rangle = 0$ for $j \ne k$, each $P_k$ is monic of degree $k$, and $\nu_k = \langle P_k, P_k \rangle > 0$. So they are an orthogonal basis of $\Pi_p$ restricted to $I$.

*Proof.* By induction on $k$. Line L1 starts from $x^k$. Line L2 subtracts multiples of $P_0, \ldots, P_{k-1}$, which have degree less than $k$, so $P_k$ stays monic of degree $k$. It is the [Gram-Schmidt process](/gram-schmidt-process/): after the step for $j$, $\langle P_k, P_j \rangle = 0$, and later steps subtract multiples of $P_{j'}$ with $\langle P_{j'}, P_j \rangle = 0$, so the zero is kept. A nonzero polynomial of degree $k \le 2m$ has at most $k < 2m + 1$ roots, so it is not zero on all of $I$, and $\nu_k > 0$. Then $P_0, \ldots, P_p$ are linearly independent on $I$ and span the $(p + 1)$-dimensional space $\Pi_p$. $\square$

**Theorem 2 (the weights).** Let $q$ be the polynomial in $\Pi_p$ that minimizes $\sum_{i \in I} (w_i - q(i))^2$. Then $q$ is unique, and the weights $c$ of lines L3 to L5 satisfy $\sum_{i \in I} c_i w_i = q^{(d)}(t)$ for every window $w$.

*Proof.* The minimizer on $I$ is the orthogonal projection of $w$ onto $\Pi_p$ in the inner product $\langle \cdot, \cdot \rangle$. With the orthogonal basis of Lemma 1, $q = \sum_{k=0}^{p} (\langle w, P_k \rangle / \nu_k)\, P_k$: for each $j$, $\langle w - q, P_j \rangle = \langle w, P_j \rangle - \langle w, P_j \rangle = 0$, so $w - q$ is orthogonal to $\Pi_p$, and for any $r \in \Pi_p$, $\sum (w_i - r(i))^2 = \sum (w_i - q(i))^2 + \sum (q(i) - r(i))^2$. The last sum is zero only if $r = q$ on $I$, and then $r = q$ because $p < 2m + 1$. Differentiate $d$ times and set $x = t$:

$$q^{(d)}(t) = \sum_{k=0}^{p} \frac{\langle w, P_k \rangle}{\nu_k} P_k^{(d)}(t) = \sum_{i \in I} w_i \sum_{k=0}^{p} \frac{P_k(i)\, P_k^{(d)}(t)}{\nu_k}.$$

The inner sum is the value $c_i$ that lines L3 to L5 accumulate. $\square$

**Corollary 3 (the filter).** For $m \le k \le n - 1 - m$, line L7 outputs $q_k^{(d)}(0)$, where $q_k$ is the fit of the window $x[k-m \ldots k+m]$. For $k < m$ it outputs the derivative at $k - m$ of the fit of the first window, and for $k > n - 1 - m$ the derivative at $k - (n - 1 - m)$ of the fit of the last window.

*Proof.* Apply Theorem 2 to the window $w_i = x[b + m + i]$ chosen at line L6, with its offset $t$. $\square$

**Theorem 4 (polynomials are kept).** If $d = 0$ and $r \in \Pi_p$, then $\sum_{i \in I} c_i\, r(i) = r(t)$. Equivalently, $\sum_i c_i = 1$ and $\sum_i c_i\, i^j = t^j$ for $1 \le j \le p$. For $d \ge 1$, $\sum_i c_i\, r(i) = r^{(d)}(t)$.

*Proof.* If $w = r$ on $I$, the sum of squares is zero at $q = r$, so the unique fit is $q = r$. Theorem 2 gives $\sum c_i r(i) = q^{(d)}(t) = r^{(d)}(t)$. Take $r = x^j$ for the moments. $\square$

**Theorem 5 (noise gain).** For the weights at $t$ with $d = 0$, $\sum_{i \in I} c_i^2 = c_t$, where $c_t$ is the weight at the index $i = t$. In particular the center weights satisfy $\sum_i c_i^2 = c_0$.

*Proof.* Write $c_i = \sum_k P_k(i) P_k(t)/\nu_k$. Then

$$\sum_i c_i^2 = \sum_{j, k} \frac{P_j(t) P_k(t)}{\nu_j \nu_k} \sum_i P_j(i) P_k(i) = \sum_k \frac{P_k(t)^2}{\nu_k},$$

by orthogonality, and this is $c_t$ from the same formula with $i = t$. $\square$

If the samples carry independent noise of variance $\sigma^2$, the output noise has variance $\sigma^2 \sum_i c_i^2 = c_t \sigma^2$. For $m = 2$ and $p = 2$ the center weights are $\frac{1}{35}(-3, 12, 17, 12, -3)$, and $\sum c_i^2 = (9 + 144 + 289 + 144 + 9)/1225 = 595/1225 = 17/35 = c_0$.

**Theorem 6 (parity).** $P_k(-x) = (-1)^k P_k(x)$. So for smoothing at the center ($d = 0$, $t = 0$), the degrees $2j$ and $2j + 1$ give the same weights, and for $d = 1$, $t = 0$, the degrees $2j - 1$ and $2j$ give the same weights.

*Proof.* The set $I$ is symmetric, so $\langle f, g \rangle = 0$ when $f g$ is odd. By induction, $P_k = x^k - \sum_{j < k} (\langle x^k, P_j \rangle / \nu_j) P_j$, because $\langle P_k, P_j \rangle$ in line L2 is computed after the earlier subtractions, but those subtractions do not change it, since $\langle P_{j'}, P_j \rangle = 0$. If $j$ and $k$ have different parity, $x^k P_j$ is odd, and the coefficient is zero. So $P_k$ is a combination of $x^k$ and of $P_j$ with the parity of $k$, and it has that parity. Going from degree $p$ to $p + 1$ adds the term $P_{p+1}(i)\, P_{p+1}^{(d)}(0)/\nu_{p+1}$ to $c_i$. If $p + 1 = 2j + 1$ and $d = 0$, $P_{p+1}$ is odd and $P_{p+1}(0) = 0$. If $p + 1 = 2j$ and $d = 1$, $P_{p+1}'$ is odd and $P_{p+1}'(0) = 0$. In both cases the term is zero. $\square$

**Theorem 7 (flat pass band).** Let $d = 0$, $t = 0$ and $p$ even. The center weights are symmetric, $c_{-i} = c_i$, and the frequency response $H(e^{i\omega}) = \sum_i c_i e^{-i\omega i}$ is real with $H(e^{i\omega}) = 1 + O(\omega^{p+2})$ as $\omega \to 0$.

*Proof.* By Theorem 6 each $P_k(i)P_k(0)$ is even in $i$, so $c_{-i} = c_i$, and $H(e^{i\omega}) = \sum_i c_i \cos(i\omega) = \sum_{l \ge 0} (-1)^l \frac{\omega^{2l}}{(2l)!} \sum_i c_i\, i^{2l}$. By Theorem 4 with $t = 0$, $\sum_i c_i = 1$ and $\sum_i c_i\, i^{2l} = 0$ for $1 \le 2l \le p$. So the first term after 1 has $2l \ge p + 2$. $\blacksquare$
