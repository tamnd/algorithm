---
title: PCSA is a set of independent Flajolet-Martin bitmaps, and averaging divides the variance by m
proves: [correctness]
status: full
---

Let the stream have $d$ distinct items $x_1, \ldots, x_d$. Let $m = 2^b$, and let $h$ map items to $L$-bit integers with $L > b$. Line L4 writes $y = h(x)$ as $j = y \bmod m$, the low $b$ bits, and $w = \lfloor y/m \rfloor$, the other $L - b$ bits. Let $R_j$ be the position of the lowest zero bit of $B[j]$, so $S = \sum_j R_j$.

**Lemma 1 (the state is a function of the set).** Bit $r$ of $B[j]$ is 1 exactly when some $x_i$ has bucket $j$ and $\rho(w_i) = r$. So the state does not depend on the order or the repeats of the stream, and the bucket by bucket OR of the states of two streams with the same $h$ and $m$ is the state of their concatenation.

*Proof.* Line L5 only sets bits, and for each item it sets bit $\rho(w)$ of $B[j]$, where $(j, w)$ is a function of the item. Induction over the stream gives the first claim, which is a condition on the set of items. The set of the concatenation is the union of the two sets, and the condition for the union is the OR of the two conditions. $\square$

From here on, $h(x_1), \ldots, h(x_d)$ are independent and uniform on $\{0, \ldots, 2^L - 1\}$.

**Lemma 2 (bucket and rest are independent).** For each item, $j$ and $w$ are independent, $j$ is uniform on $\{0, \ldots, m-1\}$, and $w$ is uniform on $\{0, \ldots, 2^{L-b} - 1\}$.

*Proof.* The map $y \mapsto (y \bmod 2^b, \lfloor y/2^b \rfloor)$ is a bijection from $\{0, \ldots, 2^L - 1\}$ to the product of the two ranges. The image of the uniform distribution under a bijection onto a product set is the uniform distribution on the product, which is the product of the two uniform distributions. $\square$

**Lemma 3 (conditional independence).** Given the buckets $j_1, \ldots, j_d$ of all items, let $D_k = |\{i : j_i = k\}|$. Then $B[0], \ldots, B[m-1]$ are independent, and $B[k]$ has the distribution of a Flajolet-Martin bitmap of $D_k$ items with an ideal random hash of $L - b$ bits.

*Proof.* By Lemma 2 and the independence of the items, the values $w_1, \ldots, w_d$ are independent and uniform, also given $j_1, \ldots, j_d$. $B[k]$ is a function of the $w_i$ with $j_i = k$ only, and these groups are disjoint, so the bitmaps are independent. Each $B[k]$ is the bitmap of lines L1 to L4 of the Flajolet-Martin counter, fed $D_k$ independent uniform values. $\square$

**Lemma 4 (Poisson buckets).** Suppose the number of distinct items is a random $N$ with the [Poisson distribution](/poisson-distribution/) of mean $\lambda$, and each item picks its bucket independently and uniformly. Then $D_0, \ldots, D_{m-1}$ are independent, each Poisson with mean $\lambda/m$.

*Proof.* For counts $k_0, \ldots, k_{m-1}$ with sum $K$,
$$\Pr[D_0 = k_0, \ldots, D_{m-1} = k_{m-1}] = e^{-\lambda}\frac{\lambda^K}{K!} \cdot \frac{K!}{k_0! \cdots k_{m-1}!}\, m^{-K} = \prod_{j=0}^{m-1} e^{-\lambda/m}\frac{(\lambda/m)^{k_j}}{k_j!}.$$
The joint distribution is the product of Poisson distributions with mean $\lambda/m$. $\square$

**Theorem 5 (averaging).** In the model of Lemma 4, let $R^{(\mu)}$ be the lowest zero position of one Flajolet-Martin bitmap fed a Poisson number of items with mean $\mu$. Then $R_0, \ldots, R_{m-1}$ are independent copies of $R^{(\lambda/m)}$, and
$$\mathbb{E}[S/m] = \mathbb{E}[R^{(\lambda/m)}], \qquad \mathrm{Var}(S/m) = \frac{\mathrm{Var}(R^{(\lambda/m)})}{m}.$$

*Proof.* By Lemma 4 the bucket sizes are independent Poisson variables with mean $\lambda/m$. By Lemma 3, given the sizes, the bitmaps are independent and each is a bitmap of its own size. So the pairs $(D_k, B[k])$ are independent over $k$, with the same distribution, and the $R_k$, which are functions of $B[k]$, are independent copies of $R^{(\lambda/m)}$. The mean and the variance of an average of $m$ independent copies are the mean and the variance divided by $m$. $\square$

**Remark (a sketch, not a proof).** Flajolet and Martin show that $\mathbb{E}[R^{(\mu)}] \approx \log_2(\varphi\mu)$ and that its standard deviation tends to about 1.12 as $\mu$ grows. With $\bar R = S/m$, the estimate is $(m/\varphi)\,2^{\bar R}$, and a first order expansion of $2^{\bar R}$ around its mean gives a relative standard deviation of about $\ln 2 \cdot 1.12/\sqrt m \approx 0.78/\sqrt m$, by Theorem 5. Their full analysis, which also gives the bias factor $1 + 0.31/m$ and handles a fixed $d$ in place of a Poisson number, is cited and not proved here. $\blacksquare$
