---
title: Each Fedorov exchange multiplies the determinant by 1 + Delta, so the algorithm increases it strictly, stops, and returns a design that no single exchange improves
proves: [correctness, termination]
status: full
---

The arithmetic is exact. The candidates are vectors $f(c_1), \dots, f(c_n) \in \mathbb R^p$, a design is a list $D$ of $N$ candidate indices, $M_D = \sum_{i=1}^Nf(x_i)f(x_i)^\top$ with $x_i = c_{D[i]}$, and the start has $\det M_D > 0$. For an invertible $M$, write $A = M^{-1}$, $d(u, v) = f(u)^\top Af(v)$ and $d(u) = d(u, u)$.

**Lemma 1 (matrix determinant lemma).** For an invertible symmetric $M$ and a vector $v$, $\det(M + svv^\top) = \det M\,(1 + s\,v^\top M^{-1}v)$ for $s = \pm1$. If $1 + s\,v^\top M^{-1}v \ne 0$, then

$$(M + svv^\top)^{-1} = M^{-1} - \frac{s\,M^{-1}vv^\top M^{-1}}{1 + s\,v^\top M^{-1}v}.$$

*Proof.* $M + svv^\top = M(I + sM^{-1}vv^\top)$, and $I + suw^\top$ has the eigenvalue $1 + sw^\top u$ on $u$ and 1 on the $(p - 1)$-dimensional space orthogonal to $w$, so its determinant is $1 + sw^\top u$. With $u = M^{-1}v$ and $w = v$ this gives the first claim. The second is the [Sherman-Morrison formula](/sherman-morrison-formula/): multiply the right side by $M + svv^\top$ and expand. $\square$

**Lemma 2 (the exchange ratio).** Let $M$ be positive definite and let $M' = M - f(x_i)f(x_i)^\top + f(x)f(x)^\top$. Then

$$\det M' = \det M\,\bigl(1 + \Delta(x_i, x)\bigr), \qquad \Delta(x_i, x) = d(x) - d(x_i) - \bigl(d(x)d(x_i) - d(x, x_i)^2\bigr).$$

*Proof.* Let $g = f(x_i)$ and $h = f(x)$, and let $K = M + hh^\top$. By Lemma 1 with $s = 1$, $\det K = \det M\,(1 + d(x))$, and $1 + d(x) \ge 1$ since $A$ is positive definite, so

$$K^{-1} = A - \frac{Ahh^\top A}{1 + d(x)}, \qquad g^\top K^{-1}g = d(x_i) - \frac{d(x, x_i)^2}{1 + d(x)}.$$

$K$ is invertible, so Lemma 1 with $s = -1$ applied to $M' = K - gg^\top$ gives

$$\det M' = \det K\,(1 - g^\top K^{-1}g) = \det M\,\Bigl[(1 + d(x))(1 - d(x_i)) + d(x, x_i)^2\Bigr].$$

Expanding the bracket gives $1 + d(x) - d(x_i) - d(x)d(x_i) + d(x, x_i)^2 = 1 + \Delta(x_i, x)$. The formula holds also when $1 - g^\top K^{-1}g = 0$; then $M'$ is singular. $\square$

Line L4 computes $\Delta$ for every pair from $A = M^{-1}$ (line L3), and line L7 forms exactly the matrix $M'$ of Lemma 2 for the chosen pair, so after line L7, $M = M_D$ for the new list $D$.

**Lemma 3 (invariant).** At the start of every pass, $M = M_D$ and $\det M_D \ge \det M_{\text{start}} > 0$. Every exchange multiplies $\det M_D$ by a factor larger than $1 + \varepsilon \ge 1$.

*Proof.* By induction on the passes. The claim holds before the first pass. In a pass, $M$ is invertible by the hypothesis, so line L3 is defined. The algorithm exchanges only if $\Delta(i^*, j^*) > \varepsilon$, and then by Lemma 2 the new determinant is $(1 + \Delta(i^*, j^*))\det M_D > (1 + \varepsilon)\det M_D \ge \det M_D > 0$. $\square$

**Theorem (termination).** The algorithm stops after at most $\binom{n + N - 1}N - 1$ exchanges. If $\varepsilon > 0$, it stops after at most $\log(D_{\max}/D_0)/\log(1 + \varepsilon)$ exchanges, with $D_0$ the starting determinant and $D_{\max}$ the largest determinant of a design.

*Proof.* $\det M_D$ depends only on the multiset of indices in $D$. By Lemma 3 it strictly increases at each exchange, so no multiset appears twice. There are $\binom{n + N - 1}N$ multisets of size $N$ from $n$ candidates, which bounds the number of designs visited. If $\varepsilon > 0$, after $T$ exchanges $D_{\max} \ge \det M_D > (1 + \varepsilon)^TD_0$, which gives the second bound. $\square$

**Theorem (correctness).** The returned design $D$ has $\det M_D \ge \det M_{\text{start}} > 0$, and for every position $i$ and candidate $j$, the design $D'$ obtained by replacing $D[i]$ by $j$ has $\det M_{D'} \le (1 + \varepsilon)\det M_D$. With $\varepsilon = 0$, no single exchange increases the determinant.

*Proof.* The first claim is Lemma 3. The algorithm returns at line L6 only when the largest $\Delta$ over all pairs is at most $\varepsilon$, and by Lemma 2, $\det M_{D'} = (1 + \Delta(i, j))\det M_D \le (1 + \varepsilon)\det M_D$ for every pair. $\square$

**What is not claimed.** The returned design is a local optimum for one exchange, not a global one. The page gives a design with $\det X^\top X = 64$ for the second-order model in two factors with 6 runs on $\{-1, 0, 1\}^2$, where the global optimum is 256 and the algorithm stops at 64. Global optimality of an exact design follows only from an outside certificate, for example $\max_xN\,d(x) = p$, which by the [Kiefer-Wolfowitz theorem](/kiefer-wolfowitz-equivalence-theorem/) makes the design optimal even among approximate designs.
