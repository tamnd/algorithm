---
title: Each row of the count sketch is unbiased with variance at most the squared L2 norm over w, and the median is within epsilon times the L2 norm with probability 1 - delta
proves: [correctness]
status: full
---

Let $f \in \mathbb{Z}^n$ be the frequency vector after a sequence of updates $(x, c)$ with integers $c$ of any sign. For each row $j = 1, \ldots, d$, the bucket hash $h_j$ is drawn from a universal family, so $\Pr[h_j(x) = h_j(y)] \le 1/w$ for $x \ne y$, and the sign hash $s_j$ is drawn from a pairwise independent family of fair signs: for $x \ne y$, $(s_j(x), s_j(y))$ is uniform on $\{-1, +1\}^2$. All $2d$ hash functions are independent. Probabilities are over the hash functions, with the stream and the query fixed in advance.

**Lemma 1 (the table is linear).** $C[j][b] = \sum_{y : h_j(y) = b} s_j(y) f_y$ for every row $j$ and column $b$.

*Proof.* By induction on the updates. An update $(x, c)$ adds $s_j(x) c$ to the right side exactly for $b = h_j(x)$, and lines L1 and L2 do the same. $\square$

So the table of line L5 for two sketches with the same hash functions is the table of $f + g$, and the difference of two tables is the table of $f - g$.

**Lemma 2 (one row).** Fix an item $x$ and a row $j$, and let $e_j = s_j(x) C[j][h_j(x)]$ be the value of line L3. Then $\mathbb{E}[e_j] = f_x$ and
$$ \mathrm{Var}[e_j] \le \frac{1}{w} \sum_{y \ne x} f_y^2 = \frac{\|f\|_2^2 - f_x^2}{w} . $$

*Proof.* Drop the index $j$. For $y \ne x$ let $Z_y = s(x) s(y) \cdot 1[h(y) = h(x)]$. By Lemma 1 and $s(x)^2 = 1$,
$$ e = f_x + \sum_{y \ne x} f_y Z_y . $$
The signs are independent of $h$. For $y \ne x$, $\mathbb{E}[s(x) s(y)] = 0$ by pairwise independence, so $\mathbb{E}[Z_y] = 0$ and $\mathbb{E}[e] = f_x$.

For the variance, $\mathrm{Var}[e] = \mathbb{E}[(\sum_{y \ne x} f_y Z_y)^2] = \sum_{y \ne x} \sum_{z \ne x} f_y f_z \mathbb{E}[Z_y Z_z]$. If $y = z$, then $Z_y^2 = 1[h(y) = h(x)]$, with mean at most $1/w$. If $y \ne z$, then $Z_y Z_z = s(y) s(z) \cdot 1[h(y) = h(x)] \, 1[h(z) = h(x)]$, since $s(x)^2 = 1$. Here $y \ne z$, so $\mathbb{E}[s(y) s(z)] = 0$ by pairwise independence, and by the independence of signs and buckets $\mathbb{E}[Z_y Z_z] = 0$. Only the square terms are left, and each is at most $f_y^2 / w$. $\square$

**Lemma 3 (the median).** Let $e_1, \ldots, e_d$ be independent, let $t \ge 0$, and suppose $\Pr[|e_j - f_x| > t] \le 1/3$ for each $j$. Let $M$ be the value at position $\lceil d/2 \rceil$ of $e_1, \ldots, e_d$ in sorted order (line L4). Then $\Pr[|M - f_x| > t] \le e^{-d/18}$.

*Proof.* Call row $j$ bad if $|e_j - f_x| > t$, and let $B$ be the number of bad rows. If $M > f_x + t$, then the values at positions $\lceil d/2 \rceil, \ldots, d$ are all above $f_x + t$, so at least $d - \lceil d/2 \rceil + 1 \ge d/2$ rows are bad. If $M < f_x - t$, then the values at positions $1, \ldots, \lceil d/2 \rceil$ are all below $f_x - t$, so at least $d/2$ rows are bad. So $|M - f_x| > t$ implies $B \ge d/2$.

The indicators of the bad rows are independent, with means $p_j \le 1/3$. The event $B \ge d/2$ implies $B - \sum_j p_j \ge d/2 - d/3 = d/6$. By the Hoeffding bound for $d$ independent variables in $[0, 1]$,
$$ \Pr[B \ge d/2] \le \exp\left(-\frac{2 (d/6)^2}{d}\right) = e^{-d/18} . \qquad \square $$

**Theorem 1.** If $w \ge 3/\varepsilon^2$ and $d \ge 18 \ln(1/\delta)$, then for every $f \in \mathbb{Z}^n$ and every item $x$,
$$ \Pr\left[|\hat f_x - f_x| > \varepsilon \|f\|_2\right] \le \delta . $$

*Proof.* If $\|f\|_2^2 - f_x^2 = 0$, every $Z_y$ term has $f_y = 0$, so each $e_j = f_x$ and $\hat f_x = f_x$. Otherwise $\|f\|_2 > 0$, and by Lemma 2 and Chebyshev's inequality, for each row
$$ \Pr[|e_j - f_x| > \varepsilon \|f\|_2] \le \frac{\|f\|_2^2}{w \, \varepsilon^2 \|f\|_2^2} \le \frac{1}{3} . $$
Each $e_j$ depends only on $h_j$ and $s_j$, so the rows are independent. By Lemma 3 with $t = \varepsilon \|f\|_2$, the failure probability is at most $e^{-d/18} \le \delta$. $\square$

**Theorem 2 (tail bound).** Let $K$ be a set of $k$ items with the largest values of $|f_y|$, and let $f_{\mathrm{res}(k)}$ be $f$ with the entries in $K$ set to 0. If $k \le w/6$, then for each row
$$ \Pr\left[|e_j - f_x| > \sqrt{6/w} \, \|f_{\mathrm{res}(k)}\|_2\right] \le \frac{1}{3} , $$
and with $d \ge 18 \ln(1/\delta)$ the median has this error bound with probability at least $1 - \delta$.

*Proof.* Split the error of row $j$ as $e_j - f_x = A + B$, with
$$ A = \sum_{y \in K, \, y \ne x} f_y Z_y , \qquad B = \sum_{y \notin K, \, y \ne x} f_y Z_y . $$
$A \ne 0$ only if some $y \in K \setminus \{x\}$ has $h_j(y) = h_j(x)$. By the union bound and universality, this has probability at most $k/w \le 1/6$.

The proof of Lemma 2, applied to the terms of $B$ only, gives $\mathbb{E}[B] = 0$ and $\mathrm{Var}[B] \le \frac{1}{w} \sum_{y \notin K} f_y^2 = \|f_{\mathrm{res}(k)}\|_2^2 / w$. Let $t = \sqrt{6/w} \, \|f_{\mathrm{res}(k)}\|_2$. If $t = 0$, all terms of $B$ have $f_y = 0$ and $B = 0$. Otherwise Chebyshev's inequality gives $\Pr[|B| > t] \le \mathrm{Var}[B]/t^2 \le 1/6$.

If $A = 0$ and $|B| \le t$, the error is at most $t$. So the row fails with probability at most $1/6 + 1/6 = 1/3$. Lemma 3 gives the bound for the median. $\blacksquare$

**Remark.** Theorem 1 is the case $k = 0$ of the same argument with a better constant: for $k = 0$ the term $A$ is empty, and Chebyshev alone gives the factor $\sqrt{3/w}$. Since $\|f_{\mathrm{res}(k)}\|_2 \le \|f\|_2$, Theorem 2 is stronger whenever the $k$ largest counts carry most of $\|f\|_2^2$.
