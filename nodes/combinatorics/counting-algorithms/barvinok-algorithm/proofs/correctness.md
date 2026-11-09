---
title: BARVINOK returns the number of lattice points (dimension 2)
proves: [correctness]
status: full
---

Notation: $d = 2$. For $x, y \in \mathbb{R}^2$, $\det(x, y) = x_1 y_2 - x_2 y_1$ and $\operatorname{rot}(x) = (-x_2, x_1)$, so $\operatorname{rot}(x) \cdot y = \det(x, y)$. For linearly independent $p, q$, $\operatorname{cone}(p, q) = \{\alpha p + \beta q : \alpha, \beta \ge 0\}$; its index is $|\det(p, q)|$. $[X]$ is the indicator function of a set $X$. A nonzero $x \in \mathbb{Z}^2$ is primitive if its coordinates have greatest common divisor 1. $P$ is a convex polygon with rational vertices $v_1, \ldots, v_k$ in counterclockwise order. At $v_i$, $a$ and $b$ are the primitive vectors in the directions of $v_{i+1} - v_i$ and $v_{i-1} - v_i$, so $\det(a, b) > 0$, and the tangent cone is $T_i = \operatorname{cone}(a, b)$.

We use three standard facts (Barvinok, Integer Points in Polyhedra, the chapters on the algebra of polyhedra and on polarity; Brion 1988).

- (F1) There is a linear map $\Phi$ from the vector space spanned by the indicator functions of rational polyhedra in $\mathbb{R}^2$ to rational functions in $z_1, z_2$ such that $\Phi([Q]) = \sum_{m \in Q \cap \mathbb{Z}^2} z^m$ whenever $Q$ contains no line (the series converges on an open set to a rational function), and $\Phi([Q]) = 0$ whenever $Q$ contains a line.
- (F2) Brion's theorem: $f(P; z) = \sum_{i} \Phi([v_i + T_i])$.
- (F3) Polarity: there is a linear map $\mathcal{D}$ on the space spanned by indicator functions of closed rational polyhedral cones with $\mathcal{D}([K]) = [K^*]$. If $K$ is lower-dimensional (a ray or $\{0\}$), then $K^*$ contains a line.

**Lemma 1 (dual cones).** If $\det(a, b) > 0$, then $\operatorname{cone}(a, b)^* = \operatorname{cone}(\operatorname{rot}(a), -\operatorname{rot}(b))$. If $\delta = \det(p, q) = \pm 1$, then $\operatorname{cone}(p, q)^* = \operatorname{cone}(r, s)$ with $r = \delta \operatorname{rot}(p)$, $s = -\delta \operatorname{rot}(q)$, and $|\det(r, s)| = 1$.

*Proof.* Let $\delta = \det(p, q) \ne 0$ and $y = \alpha \delta \operatorname{rot}(p) - \beta \delta \operatorname{rot}(q)$; every $y$ has this form, since $\operatorname{rot}(p), \operatorname{rot}(q)$ are independent. Then $y \cdot p = -\beta \delta \det(q, p) = \beta \delta^2$ and $y \cdot q = \alpha \delta \det(p, q) = \alpha \delta^2$. So $y \in \operatorname{cone}(p, q)^*$ if and only if $\alpha, \beta \ge 0$, and the dual is $\operatorname{cone}(\delta \operatorname{rot}(p), -\delta \operatorname{rot}(q))$. For $\delta = \pm 1$ this is the second claim, and $\det(r, s) = -\delta^2 \det(\operatorname{rot} p, \operatorname{rot} q) = -\delta$. For $\delta > 0$, scaling the generators by $1/\delta$ does not change the cone, which gives the first claim. $\square$

So line L3 sets the dual cone $C = \operatorname{cone}(p, q)$ with $p = \operatorname{rot}(a)$ and $q = -\operatorname{rot}(b)$, both primitive, with index $\det(a, b)$.

**Lemma 2 (one step of the decomposition).** Let $p, q$ be independent, $w = \lambda_1 p + \lambda_2 q$ with $\lambda_1, \lambda_2 \ne 0$, not both negative. Then

$$[\operatorname{cone}(p, q)] \equiv \operatorname{sgn}(\lambda_1) [\operatorname{cone}(w, q)] + \operatorname{sgn}(\lambda_2) [\operatorname{cone}(p, w)]$$

modulo the span of indicator functions of rays from 0.

*Proof.* Three cases. If $\lambda_1, \lambda_2 > 0$, $w$ is inside $\operatorname{cone}(p, q)$, which is the union of $\operatorname{cone}(p, w)$ and $\operatorname{cone}(w, q)$, and these meet in the ray of $w$. If $\lambda_1 > 0 > \lambda_2$, then $p = \frac{1}{\lambda_1} w + \frac{-\lambda_2}{\lambda_1} q$ is inside $\operatorname{cone}(w, q)$, which is the union of $\operatorname{cone}(w, p)$ and $\operatorname{cone}(p, q)$, meeting in the ray of $p$; so $[\operatorname{cone}(p, q)] \equiv [\operatorname{cone}(w, q)] - [\operatorname{cone}(p, w)]$. If $\lambda_1 < 0 < \lambda_2$, then by the same argument with the roles of $p$ and $q$ exchanged, $q$ is inside $\operatorname{cone}(p, w)$ and $[\operatorname{cone}(p, q)] \equiv [\operatorname{cone}(p, w)] - [\operatorname{cone}(w, q)]$. In each case the signs are $\operatorname{sgn}(\lambda_1)$ and $\operatorname{sgn}(\lambda_2)$. $\square$

**Lemma 3 (the short vector).** Let $p, q \in \mathbb{Z}^2$ be primitive with $D = \det(p, q)$, $|D| \ge 2$. Let $\mu$ be a shortest nonzero vector of the lattice $M$ spanned by $c_1 = (q_2, -p_2)$ and $c_2 = (-q_1, p_1)$, as returned by Lagrange-Gauss reduction, and $\lambda = \mu / D$. Then $w = \lambda_1 p + \lambda_2 q$ is a primitive vector of $\mathbb{Z}^2$, $\lambda_1, \lambda_2 \ne 0$, and $|\det(w, q)|, |\det(p, w)| \le (4/3)^{1/4} |D|^{1/2} < |D|$. The same holds after replacing $\lambda$ by $-\lambda$.

*Proof.* With $G$ the matrix with columns $p, q$, the columns $c_1, c_2$ are those of $D G^{-1}$, so $M = D G^{-1} \mathbb{Z}^2$ and $\lambda \in G^{-1} \mathbb{Z}^2$, that is, $w = G \lambda \in \mathbb{Z}^2$. The lattice $M$ has determinant $|\det(c_1, c_2)| = |D|$. By Hermite's bound in dimension 2, $|\mu|^2 \le \frac{2}{\sqrt{3}} |D|$, so $|\lambda|^2 \le \frac{2}{\sqrt 3} |D|^{-1}$ and $|\lambda_i| \le (4/3)^{1/4} |D|^{-1/2} < 1$. Now $\det(w, q) = \lambda_1 D$ and $\det(p, w) = \lambda_2 D$, which gives the bound; and $(4/3)^{1/4} |D|^{1/2} < |D|$ because $|D| \ge 2 > (4/3)^{1/2}$. If $\lambda_2 = 0$, then $w = \lambda_1 p$ is an integer vector and $p$ is primitive, so $\lambda_1$ is a nonzero integer, against $|\lambda_1| < 1$; the same for $\lambda_1$. If $w = k w'$ with $w' \in \mathbb{Z}^2$ and an integer $k \ge 2$, then $\lambda / k \in G^{-1} \mathbb{Z}^2$, so $\mu / k \in M$ is shorter than $\mu$, a contradiction; so $w$ is primitive. Negation keeps all of this. $\square$

**Lemma 4 (the loop of lines L4 to L6).** The loop stops, and when it stops, every cone in $Q$ is unimodular and $[C] \equiv \sum_{(\varepsilon, C') \in Q} \varepsilon [C']$ modulo the span of indicator functions of rays and of $\{0\}$.

*Proof.* At the start, $Q = \{(+1, C)\}$. Every cone in $Q$ is generated by two primitive vectors, by Lemma 3. A pass replaces $(\varepsilon, \operatorname{cone}(p, q))$ with index at least 2 by $(\varepsilon \operatorname{sgn} \lambda_1, \operatorname{cone}(w, q))$ and $(\varepsilon \operatorname{sgn} \lambda_2, \operatorname{cone}(p, w))$, with $\lambda$ not all negative after line L5. By Lemma 2 the invariant is kept. By Lemma 3 both new indices are positive integers smaller than the old one, so every branch of this replacement has finite depth and the loop stops. It stops only when every index is 1. $\square$

**Lemma 5 (unimodular cones).** Let $r, s$ be a basis of $\mathbb{Z}^2$, $v \in \mathbb{Q}^2$, $v = \alpha r + \beta s$, and $u = \lceil \alpha \rceil r + \lceil \beta \rceil s$. Then $\Phi([v + \operatorname{cone}(r, s)]) = z^u / ((1 - z^r)(1 - z^s))$.

*Proof.* A point $x = m r + n s$ with real $m, n$ is in $\mathbb{Z}^2$ if and only if $m, n \in \mathbb{Z}$, because $r, s$ is a basis. It is in $v + \operatorname{cone}(r, s)$ if and only if $m \ge \alpha$ and $n \ge \beta$. So the lattice points are $u + i r + j s$ with integers $i, j \ge 0$, and the series is $z^u \sum_{i} z^{ir} \sum_j z^{js}$, which converges where $|z^r|, |z^s| < 1$ to the stated function. $\square$

**Lemma 6 (evaluation).** For real $a$ and nonzero $\beta, \gamma$, the constant term of the Laurent series at $\tau = 0$ of $e^{a\tau} / ((1 - e^{\beta \tau})(1 - e^{\gamma \tau}))$ is

$$\frac{1}{\beta \gamma} \left( \frac{a^2}{2} - \frac{a(\beta + \gamma)}{2} + \frac{\beta^2 + \gamma^2}{12} + \frac{\beta \gamma}{4} \right).$$

*Proof.* $\frac{1}{1 - e^{x}} = -\frac{1}{x} \cdot \frac{x}{e^x - 1}$ and $\frac{x}{e^x - 1} = 1 - \frac{x}{2} + \frac{x^2}{12} + O(x^3)$. So the function is $\frac{1}{\beta \gamma \tau^2} e^{a \tau} \left(1 - \frac{\beta \tau}{2} + \frac{\beta^2 \tau^2}{12} + \cdots \right) \left(1 - \frac{\gamma \tau}{2} + \frac{\gamma^2 \tau^2}{12} + \cdots \right)$, and its constant term is $\frac{1}{\beta\gamma}$ times the coefficient of $\tau^2$ in the product. That coefficient is $\frac{a^2}{2} + a \left(-\frac{\beta}{2} - \frac{\gamma}{2}\right) + \frac{\beta^2}{12} + \frac{\gamma^2}{12} + \frac{\beta \gamma}{4}$. $\square$

**Theorem.** BARVINOK$(P)$ returns $|P \cap \mathbb{Z}^2|$.

*Proof.* Fix a vertex $v = v_i$ with tangent cone $T = T_i$ and dual cone $C = T^*$ from line L3. By Lemma 4, $[C] = \sum_{(\varepsilon, C') \in Q} \varepsilon [C'] + R$, where $R$ is a combination of indicator functions of rays and of $\{0\}$. Apply $\mathcal{D}$ from (F3): since $T^{**} = T$ for a closed convex cone, $[T] = \sum \varepsilon [C'^*] + \mathcal{D}(R)$, and $\mathcal{D}(R)$ is a combination of indicator functions of cones that contain lines. Translate by $v$; the identity of indicator functions is kept, and translates of sets that contain lines still contain lines. By Lemma 1, each $C'^*$ is $\operatorname{cone}(r, s)$ with $r, s$ from line L7, a basis of $\mathbb{Z}^2$. Apply $\Phi$ and use (F1) and Lemma 5:

$$\Phi([v + T]) = \sum_{(\varepsilon, C') \in Q} \varepsilon \frac{z^{u}}{(1 - z^{r})(1 - z^{s})},$$

with $u$ from line L8. Summing over the vertices and using (F2), the terms collected in $S$ satisfy $f(P; z) = \sum_{(\varepsilon, u, r, s) \in S} \varepsilon z^u / ((1 - z^r)(1 - z^s))$ as rational functions.

The left side is a Laurent polynomial. Put $z = (e^{\tau \lambda_1}, e^{\tau \lambda_2})$ with $\lambda$ from line L9, so $z^x = e^{\tau \lambda \cdot x}$. For small $\tau \ne 0$, every denominator $1 - e^{\tau \lambda \cdot r}$ is nonzero because $\lambda \cdot r \ne 0$, so the identity holds for these $\tau$:

$$\sum_{m \in P \cap \mathbb{Z}^2} e^{\tau \lambda \cdot m} = \sum_{(\varepsilon, u, r, s) \in S} \varepsilon \frac{e^{\tau \lambda \cdot u}}{(1 - e^{\tau \lambda \cdot r})(1 - e^{\tau \lambda \cdot s})}.$$

The left side is analytic at $\tau = 0$ with value $|P \cap \mathbb{Z}^2|$. The right side is a finite sum of functions with Laurent expansions at $\tau = 0$, and the Laurent expansion of the sum is the sum of the expansions. The two sides agree on a punctured neighborhood of 0, so their Laurent expansions agree, and the constant term of the right side equals the value of the left side at 0. By Lemma 6, line L10 computes exactly this constant term. $\blacksquare$
