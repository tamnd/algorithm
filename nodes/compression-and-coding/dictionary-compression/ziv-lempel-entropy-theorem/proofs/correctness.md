---
title: Proof that the LZ78 code length per symbol tends to the entropy rate
proves: [statement]
status: full
---

The proof follows the plan of Cover and Thomas (second edition, Section 13.5): a bound on the number of phrases, Ziv's inequality, and the ergodic theorem. We do the binary case; logarithms are to base 2. For a larger alphabet, replace 2 by the alphabet size $k$ and use $\log_k$; nothing else changes.

**Setting.** $X = (X_i)_{i \in \mathbb{Z}}$ is a stationary ergodic process over $\{0, 1\}$ with entropy rate $H$. A *distinct parsing* of $x_1^n$ is a cut $x_1^n = y_1 y_2 \cdots y_c$ into $c$ nonempty phrases that are pairwise different. The LZ78 parse is a distinct parsing, except that its last phrase may repeat an earlier one; deleting that phrase changes $c$ by 1 and $n$ by at most the length of the longest phrase, so we can ignore it in the limits (see Step 5).

## Step 1. Few phrases

**Lemma 1.** For $n \ge 4$, every distinct parsing of a binary string of length $n$ has
$$c \le \frac{n}{(1 - \varepsilon_n) \log n}, \qquad \varepsilon_n = \min\Big\{1, \frac{\log \log n + 4}{\log n}\Big\},$$
where the right side is $+\infty$ when $\varepsilon_n = 1$.

*Proof.* We may assume $\varepsilon_n < 1$. Let $n_k = \sum_{j=1}^{k} j\, 2^j = (k-1) 2^{k+1} + 2$, the total length of all binary strings of length 1 to $k$. Pick $k$ with $n_k \le n < n_{k+1}$; then $k \ge 2$, as $\varepsilon_n < 1$ forces $n > n_2 = 10$. The $c$ phrases are distinct, so their total length $n$ is at least the total length of the $c$ shortest distinct strings. If $c > 2^{k+1} - 2$ (the number of strings of length at most $k$), the extra phrases have length at least $k + 1$, so
$$c \le 2^{k+1} - 2 + \frac{n - n_k}{k + 1} \le \frac{n_k}{k - 1} + \frac{n - n_k}{k - 1} = \frac{n}{k - 1},$$
because $n_k / (k - 1) = 2^{k+1} + 2/(k-1)$. The same bound holds if $c \le 2^{k+1} - 2$.

Now bound $k$. From $n \ge n_k \ge 2^k$ we get $k \le \log n$. From $n < n_{k+1} = k\, 2^{k+2} + 2 \le (k + 2) 2^{k+2} \le (\log n + 2) 2^{k+2}$ we get
$$k + 2 > \log n - \log(\log n + 2) \ge \log n - \log \log n - 1,$$
since $\log n \ge 2$ gives $\log n + 2 \le 2 \log n$. So $k - 1 > \log n - \log \log n - 4 = (1 - \varepsilon_n) \log n$, and $c \le n/(k-1) < n / ((1 - \varepsilon_n) \log n)$. $\square$

As $\varepsilon_n \to 0$, Lemma 1 gives $c/n \to 0$ uniformly over all strings, at the rate $O(1/\log n)$.

## Step 2. A bound on entropy

**Lemma 2.** If $U$ is a random variable with values in $\{1, 2, \ldots\}$ and mean $\mu$, then $H(U) \le (\mu + 1) \log(\mu + 1) - \mu \log \mu \le \log(\mu + 1) + \log e$.

*Proof.* Among the laws on $\{0, 1, 2, \ldots\}$ with mean $m$, the geometric law has the largest entropy, $g(m) = (m + 1) \log(m + 1) - m \log m$, and $g$ increases in $m$. The variable $U - 1$ has such a law with mean $\mu - 1$, so $H(U) = H(U - 1) \le g(\mu - 1) \le g(\mu)$. For the second bound, $(\mu+1)\log(\mu+1) - \mu \log \mu = \log(\mu + 1) + \mu \log(1 + 1/\mu) \le \log(\mu+1) + \log e$. $\square$

## Step 3. Ziv's inequality

Fix $k \ge 0$ and a $k$-th order Markov law $Q_k$: a probability $Q_k(a \mid s)$ for each symbol $a$ and each state $s \in \{0,1\}^k$, and $Q_k(x_1^n \mid s_0) = \prod_{i=1}^n Q_k(x_i \mid x_{i-k}^{i-1})$ with the initial state $s_0 = x_{-k+1}^0$. For a distinct parsing $y_1 \cdots y_c$ of $x_1^n$, let $s_j$ be the $k$ symbols before $y_j$, and let $c_{\ell s}$ be the number of phrases with length $\ell$ and state $s$.

**Lemma 3 (Ziv's inequality).** $\displaystyle \log Q_k(x_1^n \mid s_0) \le -\sum_{\ell, s} c_{\ell s} \log c_{\ell s}.$

*Proof.* By the Markov property, $Q_k(x_1^n \mid s_0) = \prod_j Q_k(y_j \mid s_j)$. Group the phrases by $(\ell, s)$ and use Jensen's inequality for the concave $\log$:
$$\log Q_k(x_1^n \mid s_0) = \sum_{\ell, s} c_{\ell s} \sum_{j : |y_j| = \ell,\, s_j = s} \frac{1}{c_{\ell s}} \log Q_k(y_j \mid s) \le \sum_{\ell, s} c_{\ell s} \log \Big( \frac{1}{c_{\ell s}} \sum_{j : |y_j| = \ell,\, s_j = s} Q_k(y_j \mid s) \Big).$$
The phrases in one group are distinct strings of length $\ell$, so the inner sum is at most the total probability of all strings of length $\ell$ from state $s$, which is 1. $\square$

## Step 4. From Ziv's inequality to the phrase count

Let $\pi_{\ell s} = c_{\ell s}/c$, and let $(U, V)$ have the law $\pi$. Then
$$\sum_{\ell, s} c_{\ell s} \log c_{\ell s} = c \log c - c\, H(U, V),$$
and Lemma 3 gives
$$\frac{c \log c}{n} \le -\frac{1}{n} \log Q_k(x_1^n \mid s_0) + \frac{c}{n} H(U, V).$$
Now $H(U, V) \le H(U) + H(V) \le H(U) + k$, and $U$ has mean $\sum_{\ell, s} \ell\, c_{\ell s} / c = n / c$. By Lemma 2,
$$\frac{c}{n} H(U, V) \le \frac{c}{n} k + \frac{c}{n} \log\Big(\frac{n}{c} + 1\Big) + \frac{c}{n} \log e.$$
The function $t \mapsto t \log(1/t + 1)$ tends to 0 as $t \to 0$ and increases for small $t$. With $t = c/n \le 1/((1 - \varepsilon_n) \log n)$ from Lemma 1, the right side is at most some $\delta_k(n)$ that does not depend on $x$ and tends to 0. So, for every $x$ and every initial state,
$$\frac{c(n) \log c(n)}{n} \le -\frac{1}{n} \log Q_k(x_1^n \mid s_0) + \delta_k(n). \tag{1}$$

## Step 5. The upper bound on the code length

Take for $Q_k$ the true conditional law of the process, $Q_k(a \mid s) = P(X_0 = a \mid X_{-k}^{-1} = s)$, and $s_0 = X_{-k+1}^0$. Then
$$-\frac{1}{n} \log Q_k(X_1^n \mid s_0) = \frac{1}{n} \sum_{i=1}^n -\log P(X_i \mid X_{i-k}^{i-1}).$$
The summands are a stationary ergodic sequence with mean $H(X_0 \mid X_{-k}^{-1}) =: H_k \le 1$, so by the [ergodic theorem](/ergodic-theorem/) the average tends to $H_k$ with probability 1. With (1),
$$\limsup_{n \to \infty} \frac{c(n) \log c(n)}{n} \le H_k \quad \text{almost surely, for each } k.$$
For a stationary process $H_k$ decreases to $H$ as $k \to \infty$, so the limsup is at most $H$ almost surely.

The LZ78 code writes for phrase $j$ a pointer of $\lceil \log j \rceil$ bits and one symbol bit, so its length is $l_n \le c(\log c + 2)$. The possible repeated last phrase adds at most $\log c + 1$ bits and changes $c$ by one. As $c/n \to 0$,
$$\limsup_{n \to \infty} \frac{l_n(X_1^n)}{n} \le \limsup_{n \to \infty} \frac{c \log c}{n} \le H \quad \text{almost surely.}$$

## Step 6. No code does better, so the limit exists

For a fixed $n$ the LZ78 codewords form a prefix-free set: the decoder knows $n$, reads bits from the left and stops after $n$ symbols, so if the codeword of $x$ were a proper prefix of the codeword of $x' \ne x$, decoding the codeword of $x'$ would stop after reading the codeword of $x$ and output $x$. For any prefix-free code with lengths $l_n$, the [Kraft inequality](/kraft-inequality/) gives
$$P\big(l_n(X_1^n) < -\log P(X_1^n) - 2 \log n\big) = \sum_{x:\, P(x) < 2^{-l_n(x)} n^{-2}} P(x) < n^{-2} \sum_x 2^{-l_n(x)} \le n^{-2}.$$
The sum of $n^{-2}$ is finite, so by the Borel-Cantelli lemma, with probability 1, $l_n(X_1^n) \ge -\log P(X_1^n) - 2\log n$ for all large $n$. By the Shannon-McMillan-Breiman theorem (the [asymptotic equipartition property](/asymptotic-equipartition-property/) for stationary ergodic processes), $-\frac{1}{n} \log P(X_1^n) \to H$ almost surely. So $\liminf l_n / n \ge H$ almost surely. With Step 5,
$$\lim_{n \to \infty} \frac{l_n(X_1^n)}{n} = H \quad \text{almost surely.}$$
The same two steps give $c(n) \log c(n) / n \to H$ almost surely, because $l_n$ and $c \log c$ differ by $O(c) = o(n)$. $\square$
