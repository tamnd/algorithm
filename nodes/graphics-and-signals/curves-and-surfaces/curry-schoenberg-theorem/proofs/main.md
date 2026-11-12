---
title: Proof of the Curry-Schoenberg theorem
proves: [statement]
status: full
---

We use the notation of the statement: $p \ge 0$, $n \ge p$, the knots $t_0 \le \cdots \le t_{n+p+1}$ with $t_p < t_{p+1}$ and $t_n < t_{n+1}$, the domain $[a, b] = [t_p, t_{n+1}]$, the distinct interior knots $\xi_1 < \cdots < \xi_l$ with multiplicities $m_j \le p + 1$, and the space $S$. The B-splines $N_i = N_{i,p}$ come from the Cox-de Boor recursion with half-open spans and the rule that a term with a zero denominator is $0$. At $x = b$ we use the closing rule: the value of $N_i$ at $b$ is its limit from the left. We put $(x - \xi)_+^k = (x - \xi)^k$ for $x \ge \xi$ and $0$ for $x < \xi$, also for $k = 0$. We use one fact from the B-spline page: $N_{i,q}(x) = 0$ for $x \notin [t_i, t_{i+q+1})$.

## Step 1. The truncated power basis and the dimension of S

Let $\mathcal{T}$ be the set of the functions $x^k$ for $0 \le k \le p$ and $(x - \xi_j)_+^k$ for $1 \le j \le l$ and $p - m_j + 1 \le k \le p$, restricted to $[a, b]$.

*They lie in $S$.* Each one is a polynomial of degree at most $p$ on each piece. The function $(x - \xi_j)_+^k$ is smooth at every $\xi_{j'} \ne \xi_j$. At $\xi_j$ its left piece is $0$ and its right piece is $(x - \xi_j)^k$, whose derivatives of the orders $0, \ldots, k - 1$ vanish at $\xi_j$. Since $k - 1 \ge p - m_j$, the two pieces have equal derivatives of the orders $0, \ldots, p - m_j$.

*They span $S$.* Put $\xi_0 = a$ and let $s \in S$ have the pieces $q_0, \ldots, q_l$, where $q_j$ is the polynomial of $s$ on $[\xi_j, \xi_{j+1})$. For $j \ge 1$ the polynomial $q_j - q_{j-1}$ has degree at most $p$, and its derivatives of the orders $0, \ldots, p - m_j$ vanish at $\xi_j$. Its Taylor expansion at $\xi_j$ is therefore $q_j - q_{j-1} = \sum_{k=p-m_j+1}^{p} \beta_{j,k} (x - \xi_j)^k$. Let
$$g = q_0 + \sum_{j=1}^{l} \sum_{k=p-m_j+1}^{p} \beta_{j,k} (x - \xi_j)_+^k .$$
On the piece $[\xi_J, \xi_{J+1})$ only the terms with $j \le J$ are nonzero, so $g = q_0 + \sum_{j=1}^{J} (q_j - q_{j-1}) = q_J = s$ there. So $s = g$ is a combination of $\mathcal{T}$.

*They are independent.* Suppose a combination $\sum_k \alpha_k x^k + \sum_{j,k} \beta_{j,k} (x - \xi_j)_+^k$ is $0$ on $[a, b]$. On $[a, \xi_1)$, a nonempty interval, all truncated powers are $0$, so a polynomial with the coefficients $\alpha_k$ vanishes on an interval and all $\alpha_k = 0$. If all coefficients with $j < J$ are $0$, then on $[\xi_J, \xi_{J+1})$ the combination is $\sum_k \beta_{J,k} (x - \xi_J)^k$, a polynomial that vanishes on an interval, so all $\beta_{J,k} = 0$. By induction on $J$ all coefficients are $0$.

*The count.* $\mathcal{T}$ has $(p + 1) + \sum_j m_j$ elements. The knots $t_0, \ldots, t_p$ are at most $t_p = a$, and the knots $t_{n+1}, \ldots, t_{n+p+1}$ are at least $b$. By the conditions $t_p < t_{p+1}$ and $t_n < t_{n+1}$, the knots $t_{p+1}, \ldots, t_n$ lie in $(a, b)$, and they are exactly the interior knots. So $\sum_j m_j = n - p$ and

$$\dim S = n + 1. \tag{1}$$

## Step 2. Marsden's identity

For $q \ge 0$ let $\psi_{i,q}(y) = \prod_{r=1}^{q} (y - t_{i+r})$, with $\psi_{i,0} = 1$, and write $\psi_i = \psi_{i,p}$.

**Claim.** Let $p \le \mu \le n$ with $t_\mu < t_{\mu+1}$. For $0 \le q \le p$, every $x \in [t_\mu, t_{\mu+1})$ and every real $y$,
$$\sum_{i=\mu-q}^{\mu} \psi_{i,q}(y) \, N_{i,q}(x) = (y - x)^q. \tag{2}$$

*Proof.* All indices $i$ in the sum satisfy $0 \le \mu - q \le i \le \mu \le n + p - q$, so the functions exist. For $q = 0$ the sum is $N_{\mu,0}(x) = 1$. Let $q \ge 1$ and write $\omega_i = (x - t_i)/(t_{i+q} - t_i)$. Insert the recursion $N_{i,q} = \omega_i N_{i,q-1} + (1 - \omega_{i+1}) N_{i+1,q-1}$ and collect the terms with the same $N_{k,q-1}$:
$$\sum_{i=\mu-q}^{\mu} \psi_{i,q}(y) N_{i,q}(x) = \sum_{k=\mu-q}^{\mu+1} N_{k,q-1}(x) \bigl( \omega_k \, \psi_{k,q}(y) + (1 - \omega_k) \, \psi_{k-1,q}(y) \bigr),$$
where the first part is absent for $k = \mu + 1$ and the second for $k = \mu - q$. Both of these end terms contain $N_{\mu-q,q-1}(x)$ or $N_{\mu+1,q-1}(x)$, which are $0$ on the span by the support fact. For $\mu - q + 1 \le k \le \mu$ we have $k \le \mu$ and $k + q \ge \mu + 1$, so $t_{k+q} - t_k \ge t_{\mu+1} - t_\mu > 0$ and $\omega_k (t_{k+q} - t_k) = x - t_k$. Also $\psi_{k,q}(y) = \psi_{k,q-1}(y) (y - t_{k+q})$ and $\psi_{k-1,q}(y) = (y - t_k) \psi_{k,q-1}(y)$. So the bracket is
$$\psi_{k,q-1}(y) \bigl( \omega_k (y - t_{k+q}) + (1 - \omega_k)(y - t_k) \bigr) = \psi_{k,q-1}(y) \bigl( y - t_k - \omega_k (t_{k+q} - t_k) \bigr) = \psi_{k,q-1}(y) \, (y - x).$$
The sum is therefore $(y - x) \sum_{k=\mu-q+1}^{\mu} \psi_{k,q-1}(y) N_{k,q-1}(x)$, which is $(y - x)(y - x)^{q-1}$ by the hypothesis for $q - 1$. $\square$

For $x \in [a, b)$ take the $\mu$ with $t_\mu \le x < t_{\mu+1}$; then $p \le \mu \le n$, and the terms with $i$ outside $\mu - p, \ldots, \mu$ are $0$. So (2) with $q = p$ gives

$$(y - x)^p = \sum_{i=0}^{n} \psi_i(y) \, N_i(x) \qquad (a \le x \le b). \tag{3}$$

At $x = b$, (3) holds by the closing rule: on the last nonempty span both sides are polynomials in $x$, and both sides at $b$ are the limits from the left.

## Step 3. The truncated powers are B-spline series

Fix $0 \le k \le p$ and a real $\xi$. Differentiate (3) $p - k$ times with respect to $y$; the left side becomes $\frac{p!}{k!} (y - x)^k$. Put $y = \xi$ and multiply by $(-1)^k k!/p!$:

$$(x - \xi)^k = (-1)^k \frac{k!}{p!} \sum_{i=0}^{n} \psi_i^{(p-k)}(\xi) \, N_i(x) \qquad (a \le x \le b). \tag{4}$$

With $\xi = 0$ this writes each $x^k$, $0 \le k \le p$, as a combination of the $N_i$.

Now let $\xi = \xi_j$ and $m = m_j$, and let $r$ be the smallest index with $t_r = \xi$. Then $t_r = \cdots = t_{r+m-1} = \xi$ and $p + 1 \le r \le r + m - 1 \le n$. Let $p - m + 1 \le k \le p$ and

$$g(x) = (-1)^k \frac{k!}{p!} \sum_{i=r}^{n} \psi_i^{(p-k)}(\xi) \, N_i(x).$$

For $a \le x < \xi$ and $i \ge r$ we have $x < \xi = t_r \le t_i$, so $N_i(x) = 0$ and $g(x) = 0$.

For $\xi \le x \le b$, by (4), $g(x) = (x - \xi)^k - (-1)^k \frac{k!}{p!} \sum_{i=0}^{r-1} \psi_i^{(p-k)}(\xi) N_i(x)$. Each term of the last sum is $0$. If $i + p + 1 \le r + m - 1$, then $t_{i+p+1} \le \xi \le x$, so $N_i(x) = 0$; at $x = b$ the limit from the left is $0$ as well, because $t_{i+p+1} \le \xi < b$. Otherwise $i + p \ge r + m - 1$, and together with $i + 1 \le r$ this shows that the indices $i + 1, \ldots, i + p$ include $r, \ldots, r + m - 1$. Then $\psi_i(y)$ has the factor $(y - \xi)^m$, so its derivatives of the orders $0, \ldots, m - 1$ vanish at $\xi$. The order $p - k$ is at most $m - 1$, so $\psi_i^{(p-k)}(\xi) = 0$.

So $g(x) = (x - \xi_j)_+^k$ on $[a, b]$, and every element of $\mathcal{T}$ is a combination of the $N_i$.

## Step 4. Conclusion

Let $V$ be the span of $N_0, \ldots, N_n$ on $[a, b]$. By Step 1 and Step 3, $S = \operatorname{span} \mathcal{T} \subseteq V$. So, by (1),
$$n + 1 = \dim S \le \dim V \le n + 1 .$$
Hence $\dim V = n + 1$, so the $n + 1$ functions $N_0, \ldots, N_n$ are linearly independent on $[a, b]$, and $S$ is a subspace of $V$ of the same finite dimension, so $S = V$. This proves (a) and (b). $\blacksquare$

The proof never used the smoothness of the $N_i$ at the knots. It follows: each $N_i$ lies in $V = S$, so it is $C^{p - m}$ at an interior knot of multiplicity $m$.
