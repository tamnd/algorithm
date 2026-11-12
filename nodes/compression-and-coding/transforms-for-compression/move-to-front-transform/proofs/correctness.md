---
title: The decoder inverts the encoder, the output is the recency rank, and the coded length is bounded by the order-0 entropy
proves: [correctness, length]
status: full
---

We use the notation of the page. $X = X[0 \ldots n-1]$ is over $\Sigma$ with $|\Sigma| = \sigma$, and both sides start with the list $A$. For a list $P$ and an index $r$, $\mathrm{move}(P, r)$ is the list with the entry at index $r$ taken out and put at index 0. Let $P_i$ be the encoder's list before step $i$, and $Q_i$ the decoder's list before step $i$.

**Theorem 1 (the decoder inverts the encoder).** For each $i$, $Q_i = P_i$ and $\mathrm{MTF\text{-}DECODE}$ outputs $X[i]$ at step $i$.

*Proof.* By induction on $i$. For $i = 0$, $P_0 = Q_0 = A$. Suppose $P_i = Q_i$. The encoder sets $Y[i] = r$ with $P_i[r] = X[i]$ (line L2), so the decoder reads $Q_i[r] = P_i[r] = X[i]$ (line D2). Both sides then set the list to $\mathrm{move}(P_i, r)$ (lines L4 and D3), so $P_{i+1} = Q_{i+1}$. $\blacksquare$

**Theorem 2 (the output is the recency rank).** Put a virtual history before $X$: the symbols $A[\sigma-1], A[\sigma-2], \ldots, A[0]$ at the times $-\sigma, \ldots, -1$, so $A[0]$ is used last. For $x \in \Sigma$ and $i \ge 0$, let $\ell_i(x)$ be the last time before $i$ at which $x$ is used. Then $P_i$ lists $\Sigma$ in decreasing order of $\ell_i$, and $Y[i]$ equals the number of distinct symbols used at the times $\ell_i(X[i]) + 1, \ldots, i - 1$.

*Proof.* At $i = 0$, $\ell_0(A[k]) = -1 - k$, which decreases with $k$, so $P_0 = A$ is in decreasing order of $\ell_0$. Step $i$ moves $X[i]$ to the front and keeps the order of the others; at the same time $\ell_{i+1}(X[i]) = i$, the largest value, and $\ell_{i+1}(y) = \ell_i(y)$ for $y \ne X[i]$. So $P_{i+1}$ is in decreasing order of $\ell_{i+1}$. The index of $x = X[i]$ in $P_i$ is the number of symbols $y$ with $\ell_i(y) > \ell_i(x)$, that is the number of distinct symbols used after the last use of $x$ and before $i$. $\blacksquare$

**Corollary (rank and gap).** If $x = X[i]$ and $\ell_i(x) \ge 0$, then $Y[i] + 1 \le i - \ell_i(x)$, since at most $i - \ell_i(x) - 1$ symbols are used strictly between the two times. Always $Y[i] + 1 \le \sigma$.

**Lemma 3 (the function $f$).** Let $f(x) = 1 + \log_2 x + 2 \log_2(1 + \log_2 x)$ for $x \ge 1$. Then (a) the Elias delta code of an integer $k \ge 1$ has at most $f(k)$ bits; (b) $f$ is increasing and concave on $[1, \infty)$; (c) $f(a b) \le f(a) + f(b)$ for $a, b \ge 1$.

*Proof.* (a) With $N = \lfloor \log_2 k \rfloor$, the code has $N + 2 \lfloor \log_2(N + 1) \rfloor + 1$ bits; $N \le \log_2 k$ and $\log_2(N + 1) \le \log_2(1 + \log_2 k)$. (b) $\log_2 x$ is increasing and concave, and $\log_2(1 + t)$ is increasing and concave in $t \ge 0$, so the composition $\log_2(1 + \log_2 x)$ is increasing and concave, and a sum of such functions is too. (c) With $\alpha = \log_2 a \ge 0$ and $\beta = \log_2 b \ge 0$, $1 + \alpha + \beta \le (1 + \alpha)(1 + \beta)$, so $2 \log_2(1 + \alpha + \beta) \le 2 \log_2(1 + \alpha) + 2 \log_2(1 + \beta)$. Adding $1 + \alpha + \beta \le 2 + \alpha + \beta$ gives $f(ab) \le f(a) + f(b)$. $\square$

**Theorem 4 (length bound).** Let $n_x$ be the number of uses of $x$ in $X$, $\Sigma_X$ the set of symbols with $n_x > 0$, and $H_0 = \sum_{x \in \Sigma_X} \frac{n_x}{n} \log_2 \frac{n}{n_x}$. If each $Y[i]$ is written as the Elias delta code of $Y[i] + 1$, the total length is at most

$$n\,\bigl(1 + H_0 + 2 \log_2(1 + H_0)\bigr) + |\Sigma_X|\, f(\sigma) \le n\,\bigl(1 + H_0 + 2 \log_2(1 + H_0)\bigr) + \sigma f(\sigma).$$

*Proof.* Fix $x \in \Sigma_X$ with uses at $t_1 < t_2 < \cdots < t_{n_x}$. Put $g_1 = t_1 + 1$ and $g_j = t_j - t_{j-1}$ for $j \ge 2$. Each $g_j \ge 1$, and $\sum_j g_j = t_{n_x} + 1 \le n$.

For $j \ge 2$, the corollary gives $Y[t_j] + 1 \le g_j$, so by Lemma 3 (a) and (b) the code has at most $f(g_j)$ bits. For $j = 1$, $Y[t_1] + 1 \le \sigma \le \sigma g_1$, so the code has at most $f(\sigma g_1) \le f(\sigma) + f(g_1)$ bits by Lemma 3 (c).

So the uses of $x$ cost at most $f(\sigma) + \sum_{j=1}^{n_x} f(g_j)$. By Jensen's inequality for the concave $f$, and since $f$ is increasing, $\sum_j f(g_j) \le n_x f\bigl(\frac{1}{n_x} \sum_j g_j\bigr) \le n_x f(n / n_x)$.

Add over $x$, and write $p_x = n_x / n$:

$$\sum_{x} n_x f\Bigl(\frac{n}{n_x}\Bigr) = n \sum_x p_x \Bigl(1 + \log_2 \frac{1}{p_x} + 2 \log_2\bigl(1 + \log_2 \tfrac{1}{p_x}\bigr)\Bigr) = n\Bigl(1 + H_0 + 2 \sum_x p_x \log_2\bigl(1 + \log_2 \tfrac{1}{p_x}\bigr)\Bigr).$$

By Jensen's inequality for the concave $\log_2$, $\sum_x p_x \log_2(1 + \log_2 \frac{1}{p_x}) \le \log_2(1 + H_0)$. With the term $f(\sigma)$ for each $x \in \Sigma_X$, this gives the bound. $\blacksquare$
