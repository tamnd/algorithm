---
title: The construction gives PH quintics with the given end data, there are exactly four when the radicands are nonzero, and there are no others
proves: [correctness]
status: full
---

We use the pseudocode of the page. Points and vectors of the plane are complex numbers. The data are $p_0, p_5 \in \mathbb{C}$ and $d_0, d_1 \in \mathbb{C} \setminus \{0\}$, and $\Delta = p_5 - p_0$. Write $B_k^n(t) = \binom{n}{k} (1 - t)^{n-k} t^k$. A *PH quintic* in the sense of this page is a polynomial curve $r(t)$ with $r'(t) = w(t)^2$ for a complex polynomial $w$ of degree at most $2$, written $w = w_0 B_0^2 + w_1 B_1^2 + w_2 B_2^2$.

**Lemma 1 (the square of $w$).** $w^2 = w_0^2 B_0^4 + w_0 w_1 B_1^4 + \tfrac{1}{3}(2 w_1^2 + w_0 w_2) B_2^4 + w_1 w_2 B_3^4 + w_2^2 B_4^4$.

*Proof.* $B_i^2 B_j^2 = \binom{2}{i}\binom{2}{j} \binom{4}{i+j}^{-1} B_{i+j}^4$, since both sides equal $\binom{2}{i}\binom{2}{j}(1 - t)^{4-i-j} t^{i+j}$. Collect the terms with $i + j = k$. For $k = 1$ the coefficient is $2 w_0 w_1 \cdot 2/4 = w_0 w_1$. For $k = 2$ it is $w_1^2 \cdot 4/6 + 2 w_0 w_2 \cdot 1/6 = (2 w_1^2 + w_0 w_2)/3$. The cases $k = 0, 3, 4$ are the same. $\square$

**Lemma 2 (control points).** Let $h_0, \dots, h_4$ be the coefficients of Lemma 1, and let $p_0' = p_0$ and $p_{k+1}' = p_k' + h_k/5$. Then the quintic Bézier curve $r$ with control points $p_0', \dots, p_5'$ satisfies $r(0) = p_0$ and $r' = w^2$. These are the points of line L8.

*Proof.* The derivative of a quintic Bézier curve is $r' = 5 \sum_{k=0}^4 (p_{k+1}' - p_k') B_k^4 = \sum_k h_k B_k^4 = w^2$, and $r(0) = p_0'$. Line L8 computes exactly $p_{k+1}' = p_k' + h_k/5$. $\square$

**Lemma 3 (the end conditions as equations).** A PH quintic $r$ with $r(0) = p_0$ satisfies $r(1) = p_5$, $r'(0) = d_0$ and $r'(1) = d_1$ if and only if

$$w_0^2 = d_0, \qquad w_2^2 = d_1, \qquad \left(4 w_1 + 3 (w_0 + w_2)\right)^2 = 120 \Delta - 15 (d_0 + d_1) + 10 w_0 w_2. \tag{1}$$

*Proof.* $r'(0) = w(0)^2 = w_0^2$ and $r'(1) = w_2^2$, which gives the first two equations. Since $\int_0^1 B_k^4\, dt = 1/5$, Lemma 1 gives $r(1) - r(0) = \frac{1}{5} \sum_k h_k$, so $r(1) = p_5$ if and only if

$$15 \Delta = 3 w_0^2 + 3 w_0 w_1 + 2 w_1^2 + w_0 w_2 + 3 w_1 w_2 + 3 w_2^2.$$

Multiply by $8$ and subtract $(4 w_1 + 3(w_0 + w_2))^2 = 16 w_1^2 + 24 w_0 w_1 + 24 w_1 w_2 + 9 w_0^2 + 18 w_0 w_2 + 9 w_2^2$. The terms in $w_1$ cancel and

$$120 \Delta - (4 w_1 + 3(w_0 + w_2))^2 = 15 w_0^2 + 15 w_2^2 - 10 w_0 w_2.$$

Given the first two equations, $15 w_0^2 + 15 w_2^2 = 15(d_0 + d_1)$, and the last equation of (1) follows. Each step can be reversed. $\square$

**Lemma 4 (square roots in $\mathbb{C}[t]$).** If $w, v \in \mathbb{C}[t]$ and $w^2 = v^2$, then $w = v$ or $w = -v$.

*Proof.* $(w - v)(w + v) = 0$, and $\mathbb{C}[t]$ has no zero divisors. $\square$

**Theorem.** Let $d_0, d_1 \ne 0$, and for $\varepsilon = \pm 1$ let $c_\varepsilon = 120 \Delta - 15 (d_0 + d_1) + 10 \sqrt{d_0}\, \varepsilon \sqrt{d_1}$, with the principal square roots.

1. Each of the curves returned in line L10 is a PH quintic with $r(0) = p_0$, $r(1) = p_5$, $r'(0) = d_0$, $r'(1) = d_1$.
2. Every PH quintic with these end data is one of them.
3. If $c_{+1} \ne 0$ and $c_{-1} \ne 0$, the four curves are pairwise different. If $c_\varepsilon = 0$, the two curves with this $\varepsilon$ coincide.

*Proof.* (1) Lines L2, L4 and L7 choose $w_0 = \sqrt{d_0}$, $w_2 = \varepsilon \sqrt{d_1}$ and $w_1 = (-3(w_0 + w_2) + \eta \sqrt{c_\varepsilon})/4$, and line L5 computes $c = c_\varepsilon$. So $w_0^2 = d_0$, $w_2^2 = d_1$, and $(4 w_1 + 3(w_0 + w_2))^2 = (\eta \sqrt{c_\varepsilon})^2 = c_\varepsilon$, which is (1). By Lemma 2 the curve of line L8 is a PH quintic with $r(0) = p_0$, and by Lemma 3 it has the end data.

(2) Let $r$ be a PH quintic with the end data, $r' = v^2$. By Lemma 3, $v(0)^2 = d_0$, so $v(0) = \pm \sqrt{d_0}$. Replacing $v$ by $-v$ does not change $r'$, so we may assume $v(0) = \sqrt{d_0} = w_0$. By Lemma 3 again, $v(1) = \pm \sqrt{d_1}$, which is $w_2$ for one $\varepsilon$, and $4 v_1 + 3(w_0 + w_2)$ is one of the two square roots $\pm \sqrt{c_\varepsilon}$ of $c_\varepsilon$, which fixes $v_1$ as the $w_1$ of one $\eta$. So $v$ has the coefficients of one of the four triples, and $r$ is its curve, since $r(0) = p_0$ and $r' = v^2$.

(3) Let two of the triples have quadratics $w$ and $v$ with $w^2 = v^2$. By Lemma 4, $w = \pm v$. Both have $w(0) = v(0) = \sqrt{d_0} \ne 0$, so $w = v$, and the triples are equal. Triples with different $\varepsilon$ differ in $w_2$, because $\sqrt{d_1} \ne -\sqrt{d_1}$. Triples with the same $\varepsilon$ and different $\eta$ differ in $w_1$ by $\sqrt{c_\varepsilon}/2$, which is nonzero exactly when $c_\varepsilon \ne 0$. Different triples give different $r'$, and so different curves, since all curves start at $p_0$. $\square$

**Lemma 5 (speed and arc length).** For a PH quintic, $|r'(t)| = \sigma(t) = |w(t)|^2$, a polynomial of degree at most $4$ with Bernstein coefficients

$$\sigma_0 = |w_0|^2, \quad \sigma_1 = \operatorname{Re}(w_0 \bar w_1), \quad \sigma_2 = \tfrac{1}{3}\left(2 |w_1|^2 + \operatorname{Re}(w_0 \bar w_2)\right), \quad \sigma_3 = \operatorname{Re}(w_1 \bar w_2), \quad \sigma_4 = |w_2|^2,$$

and the arc length is $S = \frac{1}{5}(\sigma_0 + \dots + \sigma_4)$.

*Proof.* $|r'| = |w^2| = |w|^2 = w \bar w$, where $\bar w = \bar w_0 B_0^2 + \bar w_1 B_1^2 + \bar w_2 B_2^2$ for real $t$. The product rule of Lemma 1 gives the coefficients $w_0 \bar w_0$, $\frac{1}{2}(w_0 \bar w_1 + w_1 \bar w_0)$, $\frac{1}{6}(4 w_1 \bar w_1 + w_0 \bar w_2 + w_2 \bar w_0)$, $\frac{1}{2}(w_1 \bar w_2 + w_2 \bar w_1)$ and $w_2 \bar w_2$, which are the real numbers above. The integral of each $B_k^4$ over $[0, 1]$ is $1/5$. $\square$
