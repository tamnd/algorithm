---
title: The Flajolet-Martin bitmap and the AMS estimate are within a constant factor of d
proves: [correctness]
status: full
---

Let the stream have $d \ge 1$ distinct items $x_1, \ldots, x_d$, and let $h$ map items to $L$-bit integers. Write $\rho(y)$ for the number of trailing zeros of $y$, with $\rho(0) = L$. For $0 \le r \le L$ and a uniform $L$-bit $y$, $\Pr[\rho(y) \ge r] = 2^{-r}$, because the $r$ lowest bits must all be 0, and $\Pr[\rho(y) = r] = 2^{-(r+1)}$ for $r < L$.

**Lemma 1 (the state is a function of the set).** After lines L1 to L4, bit $r$ of $B$ is 1 exactly when $\rho(h(x_i)) = r$ for some $i$. So $B$ does not depend on the order of the stream or on repeats, and if $B_1$ and $B_2$ are the bitmaps of two streams with the same $h$, then $B_1 \lor B_2$ is the bitmap of their concatenation. The same holds for $Z = \max_i \rho(h(x_i))$ with the maximum in place of the OR.

*Proof.* Line L4 only sets bits, and it sets bit $\rho(h(x))$ for each item $x$ in the stream. By induction over the stream, after any prefix, bit $r$ is set exactly when some item of the prefix has $\rho(h(x)) = r$. This is a property of the set of items in the prefix. The set of the concatenation is the union of the two sets, and "some item of the union has $\rho = r$" is the OR of the two conditions. $\square$

## The bitmap with a fully random hash

In this section $h(x_1), \ldots, h(x_d)$ are independent and uniform.

**Theorem 1 (tails of R).** Let $R$ be the value of line L5. For each integer $r$ with $0 \le r < L$,
$$\Pr[R > r] \le \frac{d}{2^{r+1}}, \qquad \Pr[R \le r] \le \sum_{j=0}^{r} e^{-d/2^{j+1}}.$$

*Proof.* If $R > r$, then bit $r$ is set, so some $x_i$ has $\rho(h(x_i)) = r$. By the [union bound](/union-bound/), this has probability at most $d \cdot 2^{-(r+1)}$. If $R \le r$, then some bit $j \le r$ is 0. Bit $j$ is 0 when no item has $\rho = j$, which by independence has probability $(1 - 2^{-(j+1)})^d \le e^{-d/2^{j+1}}$, from $1 - x \le e^{-x}$. The union bound over $j = 0, \ldots, r$ gives the second claim. $\square$

**Corollary 2 (constant factor).** Let $c \ge 1$. Then $\Pr[2^R \ge 2cd] \le 1/(2c)$ when $2cd$ is a power of 2 at most $2^L$, and $\Pr[2^{R+1} \le d/c] \le e^{-c}/(1 - e^{-c})$ when $L > \log_2 d$.

*Proof.* For the first claim, let $2^{r+1} = 2cd$. Then $2^R \ge 2cd$ means $R \ge r + 1$, that is $R > r$, and Theorem 1 gives at most $d/2^{r+1} = 1/(2c)$. For the second, if $d/c < 2$ the event is empty, because $2^{R+1} \ge 2$. Otherwise let $r \ge 0$ be the largest integer with $2^{r+1} \le d/c$, so that $2^{R+1} \le d/c$ means $R \le r$, and $r < L$. For $j \le r$, $d/2^{j+1} = (d/2^{r+1})\,2^{r-j} \ge c \cdot 2^{r-j}$. With $k = r - j$, Theorem 1 gives $\Pr[R \le r] \le \sum_{k \ge 0} e^{-c 2^k} \le \sum_{k \ge 0} e^{-c(k+1)} = e^{-c}/(1 - e^{-c})$, because $2^k \ge k + 1$. $\square$

The finer facts, $\mathbb{E}[R] = \log_2(\varphi d) + o(1)$ up to a tiny periodic term, with $\varphi \approx 0.77351$, and a standard deviation of $R$ near 1.12, are due to Flajolet and Martin (1985) and are not proved here.

## The AMS estimate with pairwise independent hashing

**Lemma 3 (the hash family).** Let $h(x) = Ax \oplus b$, where $x$ is an $L$-bit vector, $A$ is a uniform $L \times L$ matrix over $\mathrm{GF}(2)$, $b$ is a uniform $L$-bit vector, and the product is over $\mathrm{GF}(2)$. Then for $x \ne y$ the pair $(h(x), h(y))$ is uniform over all pairs of $L$-bit vectors.

*Proof.* Let $z = x \oplus y \ne 0$, and let $j$ be a position with $z_j = 1$. Then $Az$ is the XOR of the columns of $A$ at the positions where $z$ is 1. Column $j$ is uniform and independent of the other columns, so $Az$ is uniform. Since $b$ is uniform and independent of $A$, $h(x) = Ax \oplus b$ is uniform for each fixed value of $A$, so $h(x)$ is uniform and independent of $Az$. Then $(h(x), h(y)) = (h(x), h(x) \oplus Az)$ is the image of the uniform pair $(h(x), Az)$ under a bijection, so it is uniform. $\square$

The same holds for $h(x) = ax + b$ over the field $\mathrm{GF}(2^L)$ with uniform $a, b$, with a seed of $2L$ bits. The proof below uses only the pairwise property.

Let $Z = \max_i \rho(h(x_i))$ and let the estimate be $\hat d = 2^{Z + 1/2}$. For $0 \le r \le L$ let
$$Y_r = |\{i : \rho(h(x_i)) \ge r\}|.$$

**Lemma 4.** $Z \ge r$ exactly when $Y_r \ge 1$. Also $\mathbb{E}[Y_r] = d/2^r$ and $\mathrm{Var}(Y_r) \le d/2^r$.

*Proof.* The first claim is the definition of the maximum. $Y_r$ is the sum of the [indicators](/indicator-random-variable/) $I_i$ of $\rho(h(x_i)) \ge r$. By Lemma 3 each $h(x_i)$ is uniform, so $\Pr[I_i = 1] = 2^{-r}$ and $\mathbb{E}[Y_r] = d 2^{-r}$. By Lemma 3 the $I_i$ are pairwise independent, so the covariances are 0 and $\mathrm{Var}(Y_r) = \sum_i \mathrm{Var}(I_i) = d 2^{-r}(1 - 2^{-r}) \le d 2^{-r}$. $\square$

**Theorem 5 (AMS).** $\Pr[\hat d \ge 3d] \le \sqrt 2/3$ and $\Pr[\hat d \le d/3] \le \sqrt 2/3$.

*Proof.* Upper side. Let $a$ be the smallest integer with $2^{a + 1/2} \ge 3d$. Then $\hat d \ge 3d$ exactly when $Z \ge a$. If $a > L$, this is impossible since $Z \le L$. Otherwise, by Lemma 4 and [Markov's inequality](/markov-inequality/),
$$\Pr[Z \ge a] = \Pr[Y_a \ge 1] \le \mathbb{E}[Y_a] = \frac{d}{2^a} \le \frac{d\sqrt 2}{3d} = \frac{\sqrt 2}{3},$$
because $2^a \ge 3d/\sqrt 2$.

Lower side. If $d/3 < 2^{1/2}$, then $\hat d \ge 2^{1/2} > d/3$ always, since $Z \ge 0$. Otherwise let $b \ge 0$ be the largest integer with $2^{b + 1/2} \le d/3$. Then $\hat d \le d/3$ exactly when $Z \le b$, that is, when $Y_{b+1} = 0$. We may assume $b + 1 \le L$, because $2^{b+1/2} \le d/3 < 2^L$. By [Chebyshev's inequality](/chebyshev-inequality/) and Lemma 4,
$$\Pr[Y_{b+1} = 0] \le \Pr\big[|Y_{b+1} - \mathbb{E}Y_{b+1}| \ge \mathbb{E}Y_{b+1}\big] \le \frac{\mathrm{Var}(Y_{b+1})}{(\mathbb{E}Y_{b+1})^2} \le \frac{2^{b+1}}{d} = \frac{\sqrt 2 \cdot 2^{b + 1/2}}{d} \le \frac{\sqrt 2}{3}. \qquad \square$$

**Corollary 6 (the median of copies).** Let $\hat d_1, \ldots, \hat d_t$ come from independent seeds, with $t$ odd, and let $M$ be their median. Then $\Pr[M \notin (d/3, 3d)] \le 2(4q(1-q))^{t/2}$ with $q = \sqrt 2/3$.

*Proof.* $M \ge 3d$ only if at least $(t+1)/2$ copies are $3d$ or more. Each copy is, independently, with probability at most $q < 1/2$ by Theorem 5. The Chernoff argument of the [median trick](/median-trick/) bounds this by $(4q(1-q))^{t/2}$. The side $M \le d/3$ is the same, and the union bound adds the two. $\square$

Since $4q(1-q) \approx 0.99673$, $t \ge 2\ln(2/\delta)/\ln(1/0.99673) \approx 611\ln(2/\delta)$ copies give failure probability at most $\delta$. Each copy stores $Z$ in $O(\log L)$ bits and a seed of $2L$ bits with the field hash, or $L^2 + L$ bits with the matrix hash. $\blacksquare$
