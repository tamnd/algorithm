---
title: The median of the absolute sketch values, divided by the median of |X|, is within a factor 1 plus or minus epsilon of the p-norm with probability 1 - delta
proves: [correctness]
status: full
---

Let $0 < p \le 2$, and let $X$ have the standard symmetric [p-stable law](/p-stable-distribution/), with characteristic function $e^{-|t|^p}$. Let $G(x) = \Pr[|X| \le x]$ for $x \ge 0$, and let $\mu_p$ be the median of $|X|$, so $G(\mu_p) = 1/2$. The sketch uses a $k \times n$ matrix of independent copies $X_{j,i}$ of $X$. Let $f \in \mathbb{R}^n$ be the frequency vector after a sequence of updates $(x, c)$ with any real $c$, and write $\|f\|_p = (\sum_i |f_i|^p)^{1/p}$. The analysis assumes that the matrix entries are fully independent; the remarks at the end say what changes with a pseudorandom matrix. The median is the lower median: for $k$ values, the $\lceil k/2 \rceil$-th smallest.

**Lemma 1 (the sketch is linear).** After the updates, $y_j = \sum_i X_{j,i} f_i$ for every $j$.

*Proof.* By induction on the updates. At the start, $y = 0$ and $f = 0$. An update $(x, c)$ adds $c$ to $f_x$, so the right side grows by $c X_{j,x}$, and lines L1 and L2 add the same amount to $y_j$. $\square$

So line L5 gives the sketch of $f + g$ from the sketches of $f$ and $g$ under the same matrix, and an update followed by the same update with $-c$ leaves $y$ unchanged.

**Lemma 2 (each counter is a scaled stable variable).** The values $y_1, \ldots, y_k$ are independent, and each has the law of $\|f\|_p X$. So $\Pr[|y_j| \le \|f\|_p x] = G(x)$ for every $x \ge 0$ when $f \ne 0$.

*Proof.* The rows of the matrix are independent, and $y_j$ depends only on row $j$, so the $y_j$ are independent. By the definition of $p$-stability, $\sum_i f_i X_{j,i}$ has the law of $\|f\|_p X$; the proof on the [p-stable distribution](/p-stable-distribution/) page computes the characteristic function $\prod_i e^{-|f_i t|^p} = e^{-\|f\|_p^p |t|^p}$. $\square$

**Lemma 3 (the median of independent samples).** Let $Z_1, \ldots, Z_k$ be independent with the law of $|X|$, let $0 < \varepsilon \le 1$, and let
$$ \eta = \min\big(\tfrac12 - G((1 - \varepsilon)\mu_p),\; G((1 + \varepsilon)\mu_p) - \tfrac12\big) . $$
If $\eta > 0$, then the lower median $M$ of the $Z_j$ satisfies
$$ \Pr\big[M < (1 - \varepsilon)\mu_p\big] \le e^{-2\eta^2 k} \quad\text{and}\quad \Pr\big[M > (1 + \varepsilon)\mu_p\big] \le e^{-2\eta^2 k} . $$

*Proof.* Let $L = (1 - \varepsilon)\mu_p$ and $A$ the number of $j$ with $Z_j < L$. If $M < L$, then at least $\lceil k/2 \rceil \ge k/2$ values are below $L$, so $A \ge k/2$. Each indicator $1[Z_j < L]$ has mean at most $G(L) \le 1/2 - \eta$, so $A \ge k/2$ means that $A$ exceeds its mean by at least $\eta k$. The indicators are independent, and Hoeffding's inequality gives probability at most $e^{-2\eta^2 k}$.

Let $U = (1 + \varepsilon)\mu_p$ and $B$ the number of $j$ with $Z_j > U$. If $M > U$, then fewer than $\lceil k/2 \rceil$ values are at most $U$, so $B \ge k - \lceil k/2 \rceil + 1 = \lfloor k/2 \rfloor + 1 > k/2$. Each indicator has mean $1 - G(U) \le 1/2 - \eta$, and the same bound follows. $\square$

**Lemma 4 ($\eta$ for the Cauchy case).** For $p = 1$, $\mu_1 = 1$ and $\eta \ge \frac{2\varepsilon}{5\pi}$ for $0 < \varepsilon \le 1$.

*Proof.* For $p = 1$, $X$ is standard Cauchy and $G(x) = \frac{2}{\pi}\arctan x$, so $G(1) = \frac{2}{\pi} \cdot \frac{\pi}{4} = \frac12$ and $\mu_1 = 1$. The derivative of $\arctan$ is $\frac{1}{1 + x^2}$. On $[1 - \varepsilon, 1]$ it is at least $\frac12$, so
$$ \tfrac12 - G(1 - \varepsilon) = \tfrac{2}{\pi}\big(\arctan 1 - \arctan(1 - \varepsilon)\big) \ge \tfrac{2}{\pi} \cdot \tfrac{\varepsilon}{2} = \tfrac{\varepsilon}{\pi} . $$
On $[1, 1 + \varepsilon] \subseteq [1, 2]$ it is at least $\frac15$, so $G(1 + \varepsilon) - \frac12 \ge \frac{2}{\pi} \cdot \frac{\varepsilon}{5} = \frac{2\varepsilon}{5\pi}$. The smaller of the two is at least $\frac{2\varepsilon}{5\pi}$. $\square$

**Theorem 1 (the norm estimate).** Let $0 < \varepsilon \le 1$, $0 < \delta < 1$, and suppose $\eta > 0$ as in Lemma 3. If
$$ k \ge \frac{\ln(2/\delta)}{2\eta^2}, $$
then the value $N$ of line L3 satisfies $(1 - \varepsilon)\|f\|_p \le N \le (1 + \varepsilon)\|f\|_p$ with probability at least $1 - \delta$. For $p = 1$, the choice $k = \lceil \ln(2/\delta) \cdot \frac{25\pi^2}{8\varepsilon^2} \rceil$ is enough.

*Proof.* If $f = 0$, every $y_j$ is 0 by Lemma 1, and $N = 0 = \|f\|_p$. Otherwise, by Lemma 2 the values $Z_j = |y_j| / \|f\|_p$ are independent with the law of $|X|$. The median of the $|y_j|$ is $\|f\|_p$ times the median $M$ of the $Z_j$, so $N = \|f\|_p M / \mu_p$. The event $N < (1 - \varepsilon)\|f\|_p$ is $M < (1 - \varepsilon)\mu_p$, and the event $N > (1 + \varepsilon)\|f\|_p$ is $M > (1 + \varepsilon)\mu_p$. By Lemma 3 and the union bound, the failure probability is at most $2e^{-2\eta^2 k} \le \delta$. For $p = 1$, Lemma 4 gives $\frac{1}{2\eta^2} \le \frac{25\pi^2}{8\varepsilon^2}$. $\square$

**Theorem 2 ($\eta$ is of order $\varepsilon$ for every $p$).** For each $p \in (0, 2]$ there is $c_p > 0$ with $\eta \ge c_p \varepsilon$ for all $0 < \varepsilon \le 1$. So $k = O(\varepsilon^{-2}\log(1/\delta))$ for every fixed $p$.

*Proof.* The law of $X$ has a density that is continuous and positive on all of $\mathbb{R}$ (Zolotarev 1986, Chapter 2; for $p = 1$ and $p = 2$ the closed forms show it). So $|X|$ has the density $g(x) = 2 \cdot \mathrm{density}(x)$ on $(0, \infty)$, which is continuous and positive, and its minimum $m_p$ over the compact interval $[0, 2\mu_p]$ is positive. Then $\frac12 - G((1-\varepsilon)\mu_p) = \int_{(1-\varepsilon)\mu_p}^{\mu_p} g \ge m_p \mu_p \varepsilon$, and the same holds on the right side. Take $c_p = m_p \mu_p$. $\square$

**Corollary (the moment estimate).** Under Theorem 1 with $\varepsilon/3$ in place of $\varepsilon$, line L4 returns $\hat F$ with $(1 - \varepsilon) F_p \le \hat F \le (1 + \varepsilon) F_p$, where $F_p = \|f\|_p^p$.

*Proof.* $\hat F = N^p$ with $N \in [(1 - \varepsilon/3), (1 + \varepsilon/3)] \cdot \|f\|_p$. For $0 < p \le 2$, $(1 + \varepsilon/3)^p \le (1 + \varepsilon/3)^2 = 1 + \frac{2\varepsilon}{3} + \frac{\varepsilon^2}{9} \le 1 + \varepsilon$. For the lower side, $(1 - \varepsilon/3)^p \ge (1 - \varepsilon/3)^2 \ge 1 - \frac{2\varepsilon}{3} \ge 1 - \varepsilon$. $\square$

**Remarks on the random matrix.** The proof uses $nk$ fully independent entries, which is too many to store. Indyk (2006) generated them with Nisan's pseudorandom generator for space-bounded computation: the estimator is a small-space test of the matrix, so the generator fools it, and the seed is polylogarithmic in $n$. Kane, Nelson and Woodruff (2010) showed that entries with limited independence are enough for a different estimator, which gives optimal space. The implementation on this page makes each column again from a seeded generator; that is a practical choice, and the guarantee above holds for it only in the model where the generator is ideal. The entries are also real numbers. If each entry is rounded to a multiple of $2^{-b}$, each $y_j$ changes by at most $2^{-b}\|f\|_1$, so the median changes by at most the same amount. For a nonzero integer vector with entries at most $M$ in absolute value, $\|f\|_p \ge 1$ and $\|f\|_1 \le nM$, so $b = O(\log(nM/\varepsilon))$ bits make this change a small fraction of $\varepsilon\|f\|_p$. $\blacksquare$
