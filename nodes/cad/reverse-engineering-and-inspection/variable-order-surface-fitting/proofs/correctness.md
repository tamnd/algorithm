---
title: A 5 by 5 seed determines every fit, the segmentation stops, and the growth from a seed recovers a noise-free polynomial patch with its true order
proves: [correctness, termination]
status: full
---

**Setup.** Pixels $p = (i, j)$ sit at $(x, y) = (j h, i h)$ with height $z(p)$. $P_d$ is the space of real polynomials in $x, y$ of total degree at most $d$. For a set $R$ of pixels and $d \le 4$, a least-squares polynomial of order $d$ on $R$ is an $f \in P_d$ that minimizes $\sum_{p \in R} (z(p) - f(p))^2$, and $e_d(R)$ is the RMS error of such an $f$. A seed is a $5 \times 5$ block of pixels. Lines L3 to L7 of the algorithm are the growth from one seed $S$; the set $U$ of used pixels does not change during it. All statements are in exact arithmetic.

**Lemma 1 (unisolvence on a grid).** Let $X$ and $Y$ be sets of $k + 1$ distinct numbers each. A polynomial $q$ of degree at most $k$ in $x$ and at most $k$ in $y$ that vanishes on $X \times Y$ is zero.

*Proof.* Write $q(x, y) = \sum_{a=0}^{k} c_a(y) x^a$ with polynomials $c_a$ of degree at most $k$. For each $y_0 \in Y$, $q(\cdot, y_0)$ has degree at most $k$ and $k + 1$ distinct roots $X$, so all its coefficients $c_a(y_0)$ vanish. So each $c_a$ has the $k + 1$ distinct roots $Y$, and $c_a = 0$. $\square$

**Corollary 1 (the fits exist and are unique).** If $R$ contains a seed, then for every $d \le 4$ the least-squares polynomial of order $d$ on $R$ is unique.

*Proof.* The pixels of a seed have $5$ distinct values of $x$ and $5$ distinct values of $y$. A polynomial of total degree at most $4$ has degree at most $4$ in each variable, so by Lemma 1 the only $f \in P_d$ that vanishes on the seed, and hence on $R$, is $0$. So the map from the coefficients to the values on $R$ is injective, the design matrix has full column rank, and the least-squares solution is unique. $\square$

Lemma 1 is sharp for the seed size: on a $4 \times 4$ grid with $x$ values $x_0, \dots, x_3$, the quartic $(x - x_0)(x - x_1)(x - x_2)(x - x_3)$ vanishes, so the quartic fit is not unique.

**Theorem 1 (termination).** The growth from a seed stops after at most $|R_{\text{final}}| - 25 + 4$ passes of lines L4 to L7, and the whole algorithm stops after at most $N / 25$ seeds, where $N$ is the number of pixels.

*Proof.* Every region during the growth contains its seed, so by Corollary 1 line L4 is always defined. Each pass does one of four things: line L5 raises $d$, which happens at most $3$ times since $d \le 4$; line L5 rejects; line L7 accepts; or line L7 replaces $R$ by $R' \supseteq R$ with $R' \ne R$, so $R$ gains at least one pixel. A region has at most $N$ pixels, so the number of growth passes is bounded, and the growth ends with a rejection or an acceptance. Line L2 picks a seed of $25$ pixels that are not blocked and then blocks them, so the blocked set grows by $25$ pixels per seed, and there are at most $N / 25$ seeds. $\square$

**Lemma 2 (lower orders leave an error).** Let $g$ have total degree exactly $d^\ast \le 4$, and let $z = g$ on a seed $S$. Then $e_d(S) > 0$ for every $d < d^\ast$.

*Proof.* Suppose $e_d(S) = 0$ for some $d < d^\ast$. Then some $f \in P_d$ agrees with $g$ on $S$, so $g - f$ vanishes on the $5 \times 5$ grid $S$. It has degree at most $4$ in each variable, so $g - f = 0$ by Lemma 1. But $g - f$ contains the nonzero terms of degree $d^\ast > d$ of $g$, a contradiction. $\square$

**Theorem 2 (exact recovery of a polynomial patch).** Let $A$ be a 4-connected set of pixels with $A \cap U = \emptyset$, let $g$ be a polynomial of total degree exactly $d^\ast \in \{1, 2, 3, 4\}$ with $z = g$ on $A$, and let the seed $S$ lie in $A$. Assume

1. $0 \le \tau < e_d(S)$ for every $d < d^\ast$ (these numbers are positive by Lemma 2), and $\beta \ge 0$;
2. every pixel $q \notin A \cup U$ that is a 4-neighbor of a pixel of $A$ has $\lvert z(q) - g(q) \rvert > \beta$.

Then the growth from $S$ accepts the region $A$ with the polynomial $g$ and the order $d^\ast$.

*Proof.* Line L3 sets $R = S$ and $d = 1$. For $d < d^\ast$, line L4 gives the error $e_d(S) > \tau$ by assumption 1, and since $d < d^\ast \le 4$ line L5 raises the order. So the order reaches $d^\ast$ with $R = S$.

Now take any $R$ with $S \subseteq R \subseteq A$ and $d = d^\ast$. Since $g \in P_{d^\ast}$ fits $R$ with zero error, it is a least-squares polynomial, and by Corollary 1 it is the only one; so line L4 gives $f = g$ and $e = 0 \le \tau$, and line L5 passes to line L6. The search of line L6 starts from $R$ and moves through unused pixels $q$ with $\lvert z(q) - g(q) \rvert \le \beta$.

It reaches every pixel of $A$: these are unused, have residual $0 \le \beta$, and $A$ is 4-connected and contains $R$.

It reaches no pixel outside $A$: suppose it does, and let $q$ be the first such pixel reached. The pixel from which $q$ was reached is in $R$ or was reached earlier, so it is in $A$, and $q$ is a 4-neighbor of $A$, unused and outside $A$. Assumption 2 gives $\lvert z(q) - g(q) \rvert > \beta$, so the search does not enter $q$, a contradiction.

So $R' = A$. If $R = A$, line L7 accepts $(A, g, d^\ast)$. Otherwise line L7 sets $R = A$, and the next pass, by the same argument with $R = A$, gives $f = g$, $e = 0$ and $R' = A = R$, and accepts $(A, g, d^\ast)$. $\square$

**What is not proved.** Theorem 2 starts from a seed inside the patch. Whether line L2 finds such a seed depends on the sign map, which is computed from a local quadratic fit and is exact only where the surface is quadratic on the whole window; this is not proved here. Nothing is proved for noisy data: then the errors of all orders are positive, and the result depends on $\tau$, $\beta$ and the curvature thresholds. With floating point the fits have rounding errors of about $10^{-15}$ times the size of the data, so the code uses a small positive $\tau$ in place of $0$. $\blacksquare$
