---
title: The LogLog registers have an exact Gumbel-type law and fit in log log n bits
proves: [correctness]
status: full
---

Let the stream have $d$ distinct items, let $h$ map items to $L$-bit integers, and let $m = 2^b$ with $b < L$. For an item, line L4 splits $y = h(x)$ into the first $b$ bits $j$ and the other $W = L - b$ bits $w$. Let $\rho(w)$ be the position of the leftmost 1 of $w$, counted from 1, with $\rho(0) = W + 1$.

**Lemma 1 (the state is a function of the set).** After lines L1 to L5, $M[j] = \max\{\rho(w_x) : x \text{ a distinct item with bucket } j\}$, or 0 if there is none. So the state does not depend on order or repeats, and the register by register maximum of the states of two streams with the same $h$ and $b$ is the state of their concatenation.

*Proof.* Line L5 replaces $M[j]$ by the maximum of $M[j]$ and the value of the current item, and this value is a function of the item. By induction, after a prefix, $M[j]$ is the maximum over the items of the prefix in bucket $j$, which depends only on the set of these items. The maximum over a union of two sets is the maximum of the two maxima. $\square$

From here on, the hash values of the distinct items are independent and uniform.

**Lemma 2 (one value).** For a uniform $W$-bit $w$ and $0 \le r \le W$, $\Pr[\rho(w) > r] = 2^{-r}$. The first $b$ bits $j$ are uniform and independent of $w$.

*Proof.* $\rho(w) > r$ exactly when the first $r$ bits of $w$ are 0, which has probability $2^{-r}$. The split of a uniform $L$-bit string into its first $b$ bits and its other $W$ bits is a bijection onto a product set, so the two parts are independent and uniform. $\square$

**Theorem 3 (register size).** For each $c \ge 0$, $\Pr\big[\max_j M[j] \ge \log_2 d + 1 + c\big] \le 2^{-c}$. So with probability at least $1 - 2^{-c}$, every register fits in $\lceil \log_2(\log_2 d + 2 + c) \rceil$ bits.

*Proof.* $\max_j M[j] \ge r$ only if some distinct item has $\rho \ge r$. By Lemma 2, each item has $\rho \ge r$ with probability $2^{-(r-1)}$ (or 0 if $r > W + 1$). The [union bound](/union-bound/) gives at most $d\,2^{-(r-1)}$, which is $2^{-c}$ for $r = \log_2 d + 1 + c$. A register below $\log_2 d + 1 + c$ is an integer from 0 to $\lfloor \log_2 d + 1 + c \rfloor$, so it fits in the stated number of bits. $\square$

**Theorem 4 (exact law in the Poisson model).** Suppose the number of distinct items is Poisson with mean $\lambda$. Then $M[0], \ldots, M[m-1]$ are independent, and with $\mu = \lambda/m$,
$$\Pr[M[j] \le r] = \exp(-\mu\,2^{-r}) \quad \text{for } 0 \le r \le W.$$

*Proof.* By Lemma 2, each item picks its bucket uniformly and independently of its $w$. By the splitting property of the [Poisson distribution](/poisson-distribution/), the items with bucket $j$ and $\rho > r$ form, for different $j$, independent Poisson counts. The count for bucket $j$ has mean $\lambda \cdot (1/m) \cdot 2^{-r} = \mu 2^{-r}$. The event $M[j] \le r$ is the event that this count is 0, which has probability $\exp(-\mu 2^{-r})$. The registers are functions of the disjoint groups of items in each bucket, and these groups are independent Poisson processes, so the registers are independent. $\square$

The splitting property used here is the same computation as Lemma 4 of the [PCSA](/pcsa/) proof: a Poisson number of items, each put into one of several classes independently, gives independent Poisson counts per class.

**Consequences of Theorem 4.** The mean of $M[j]$ is $\sum_{r \ge 0} \Pr[M[j] > r] = \sum_{r \ge 0}\big(1 - \exp(-\mu 2^{-r})\big)$, up to the cut at $r = W$. The registers are independent and have the same law, so the mean $\bar M$ of line L6 has variance $\mathrm{Var}(M[j])/m$.

**What is cited.** Durand and Flajolet (2003) show, with Mellin transforms, that $\mathbb{E}[M[j]] = \log_2 \mu + \gamma/\ln 2 + 1/2 + \epsilon(\mu)$, with a periodic term $\epsilon$ of tiny amplitude. Then $2^{\mathbb{E}\bar M} \approx \mu\, e^{\gamma}\sqrt 2$, and the factor $\alpha_\infty = e^{-\gamma}/\sqrt 2 \approx 0.39701$ makes $\alpha_\infty m 2^{\bar M}$ close to $\lambda$. They also give the exact $\alpha_m$ of line L6, which makes the estimate asymptotically unbiased for each fixed $m$, and the standard error $\beta_m/\sqrt m$ with $\beta_\infty = \sqrt{\pi^2/6 + (\ln 2)^2/12} \approx 1.29806$, and they show that the same results hold for a fixed $d$ in place of a Poisson number. These results assume a fully random hash and are not proved here. $\blacksquare$
