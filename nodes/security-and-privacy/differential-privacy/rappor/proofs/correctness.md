---
title: RAPPOR meets its two privacy bounds and its decoded counts are unbiased
proves: [correctness]
status: full
---

Fix the parameters: $k$ bits, $h$ hash functions, $m$ cohorts, $0 < f < 1$ and $0 \le p < q \le 1$, all rational. For a value $v$ and a cohort, let $B(v) \in \{0,1\}^k$ be the Bloom filter of line L2. It has at most $h$ ones, because each of the $h$ hash functions sets one bit. Write

$$q^* = \tfrac{f}{2}(p + q) + (1 - f)q, \qquad p^* = \tfrac{f}{2}(p + q) + (1 - f)p.$$

**Lemma 1 (the coins).** Line L3 sets each bit $B'_i$ to 1 with probability $f/2$, to 0 with probability $f/2$, and to $B_i$ with probability $1 - f$, independently over $i$. Line L6 sets $S_i = 1$ with probability $q$ if $B'_i = 1$ and $p$ if $B'_i = 0$, independently over $i$ and given $B'$.

*Proof.* Let $f = a/b$ in lowest terms. Line L3 draws $u$ uniform on $\{0, \ldots, 2b - 1\}$. The events $u < a$ and $a \le u < 2a$ have probability $a/(2b) = f/2$ each, and the rest has probability $1 - f$. Line L6 draws one uniform integer below the denominator of $q$ or $p$ and compares it with the numerator, which gives probability $q$ or $p$ exactly. Each bit uses its own draw. $\square$

**Lemma 2 (one report).** If no memo exists for $v$, the bits of the report $S$ are independent, and $\Pr[S_i = 1] = q^*$ if $B_i = 1$ and $p^*$ if $B_i = 0$.

*Proof.* By Lemma 1, if $B_i = 1$ then $\Pr[B'_i = 1] = 1 - f/2$, so $\Pr[S_i = 1] = (1 - f/2)q + (f/2)p = q^*$. If $B_i = 0$ then $\Pr[B'_i = 1] = f/2$, so $\Pr[S_i = 1] = (f/2)q + (1 - f/2)p = p^*$. The pairs $(B'_i, S_i)$ are independent over $i$. $\square$

Note that $q^* - p^* = (1 - f)(q - p) > 0$.

**Theorem 1 (longitudinal bound).** Let $\varepsilon_\infty = 2h \ln\big((1 - f/2)/(f/2)\big)$. For two values $v_1, v_2$ of the same cohort and every output $b'$, $\Pr[B' = b' \mid v_1] \le e^{\varepsilon_\infty} \Pr[B' = b' \mid v_2]$. So the sequence of all reports that a client sends for one value is $\varepsilon_\infty$-LDP, for any number of reports. The bound is attained when $B(v_1)$ and $B(v_2)$ have $h$ ones each and no common one.

*Proof.* By Lemma 1, $\Pr[B' = b' \mid B] = \prod_i \pi(B_i, b'_i)$ with $\pi(x, x) = 1 - f/2$ and $\pi(x, 1 - x) = f/2$. Let $D$ be the set of positions where $B(v_1)$ and $B(v_2)$ differ. The factors outside $D$ cancel. Inside $D$, each factor of the ratio is $(1 - f/2)/(f/2)$ or its inverse, and $(1 - f/2)/(f/2) > 1$ because $f < 1$. So the ratio is at most $((1 - f/2)/(f/2))^{|D|}$. Each filter has at most $h$ ones, so $|D| \le 2h$, which gives $e^{\varepsilon_\infty}$. Equality holds for $b' = B(v_1)$ when $|D| = 2h$.

Lines L1 and L4 store $B'$ the first time the value is seen, and line L5 reads it back each later time. So every report of $v$ is $S = $ L6 applied to the same $B'$, with fresh coins that do not depend on $v$. The sequence of reports is a randomized function of $B'$ alone, and the post-processing theorem gives the same bound for it. $\square$

**Theorem 2 (bound for one report).** Let $\varepsilon_1 = h \ln\big(q^*(1 - p^*)/(p^*(1 - q^*))\big)$. One report of a value with no memo is $\varepsilon_1$-LDP among the values of one cohort, and the bound is attained for two disjoint filters with $h$ ones each.

*Proof.* By Lemma 2, the ratio $\Pr[S = s \mid v_1]/\Pr[S = s \mid v_2]$ is the product over $i \in D$ of a factor that depends on $s_i$. Let $D_{10}$ be the positions with $B_i(v_1) = 1$ and $B_i(v_2) = 0$, and $D_{01}$ the others in $D$. On $D_{10}$, the factor is $q^*/p^*$ if $s_i = 1$ and $(1 - q^*)/(1 - p^*)$ if $s_i = 0$. The first is above 1 and the second below 1, because $q^* > p^*$. On $D_{01}$ the factors are $p^*/q^*$ and $(1 - p^*)/(1 - q^*)$, and the second is the one above 1. So

$$\frac{\Pr[S = s \mid v_1]}{\Pr[S = s \mid v_2]} \le \left(\frac{q^*}{p^*}\right)^{|D_{10}|}\left(\frac{1 - p^*}{1 - q^*}\right)^{|D_{01}|} \le \left(\frac{q^*(1 - p^*)}{p^*(1 - q^*)}\right)^{h},$$

since $|D_{10}| \le h$ (the ones of $v_1$) and $|D_{01}| \le h$ (the ones of $v_2$), and both bases are at least 1. Equality holds when $|D_{10}| = |D_{01}| = h$ and $s = B(v_1)$. $\square$

**Theorem 3 (unbiased bit counts).** Let cohort $j$ have $N_j$ clients that each send one report, and let $T_{ji}$ be the number of them whose filter has bit $i$ set. Then the value $t_{ji}$ of line L9 has $\mathbb E[t_{ji}] = T_{ji}$ and

$$\mathrm{Var}[t_{ji}] = \frac{T_{ji}\,q^*(1 - q^*) + (N_j - T_{ji})\,p^*(1 - p^*)}{(1 - f)^2(q - p)^2}.$$

*Proof.* Line L8 counts $c_{ji}$, a sum of $N_j$ independent indicators: $T_{ji}$ of them have mean $q^*$ and the others have mean $p^*$, by Lemma 2. So $\mathbb E[c_{ji}] = T_{ji} q^* + (N_j - T_{ji}) p^* = T_{ji}(q^* - p^*) + N_j p^*$. Line L9 computes $t_{ji} = (c_{ji} - p^* N_j)/((1 - f)(q - p))$, and $(1 - f)(q - p) = q^* - p^*$, so $\mathbb E[t_{ji}] = T_{ji}$. The variance of a sum of independent indicators is the sum of their variances, and the affine map divides it by $(q^* - p^*)^2$. $\square$

**Theorem 4 (the fit).** Let $X$ be the $km \times M$ matrix of line L10 and suppose its columns are independent. Suppose that every client holds one of the $M$ candidate values and that cohort $j$ has $a_{vj}$ clients with value $v$. If each candidate has the same count $a_v$ in every cohort, then line L11 returns an unbiased estimate of $(a_v)_v$, and line L12 returns an unbiased estimate of the totals $(m a_v)_v$.

*Proof.* Since $X$ has independent columns, $X^{\mathsf T} X$ is invertible, and line L11 returns $\hat a = (X^{\mathsf T}X)^{-1} X^{\mathsf T} t$, the unique solution of the normal equations. By the definition of $X$, $T_{ji} = \sum_v a_{vj} X_{(j,i),v} = \sum_v a_v X_{(j,i),v}$, so $T = X a$ as vectors. By Theorem 3 and linearity, $\mathbb E[\hat a] = (X^{\mathsf T}X)^{-1}X^{\mathsf T} X a = a$. Line L12 multiplies by $m$. $\square$

Theorems 1 and 2 give the privacy of the client for many reports and for one report. Theorems 3 and 4 give the correctness of the collector when the candidate list is complete and the cohorts are balanced. If some clients hold a value outside the list, Theorem 4 does not apply, and the fit can be biased. $\blacksquare$
