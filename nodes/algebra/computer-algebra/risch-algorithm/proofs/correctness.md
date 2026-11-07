---
title: The Risch algorithm for one exponential monomial is correct and complete
proves: [correctness]
status: full
---

**Setting.** Let $\bar{\mathbb{Q}}$ be an algebraic closure of $\mathbb{Q}$, $k = \bar{\mathbb{Q}}(x)$ with $x' = 1$, $b \in \mathbb{Q}[x]$ of degree $m + 1 \ge 1$, and $t$ with $t' = b' t$. The integrand is $f = \sum_k f_k t^k$ with $f_k \in \mathbb{Q}(x)$ and finitely many $k \in \mathbb{Z}$. An *elementary integral* of $f$ is an element $F$ of an elementary extension of $k(t)$, with the same constants $\bar{\mathbb{Q}}$, such that $F' = f$.

**Theorem.** (a) If the algorithm returns $(y, R, A^*/D^*)$, then $f = \bigl(\sum_{k \ne 0} y_k t^k + R\bigr)' + A^*/D^*$ with $D^*$ squarefree, and so $f$ has the elementary integral $\sum_k y_k t^k + R + \sum_{c} c \log v_c$, where the last sum is the Rothstein-Trager logarithmic part of $\int A^*/D^*$. (b) If the algorithm returns FAIL, then $f$ has no elementary integral.

## Lemma 1 ($t$ is a monomial)

$t$ is transcendental over $k$, and $k(t)$ has the constants $\bar{\mathbb{Q}}$. Every monic irreducible $p \in k[t]$ other than $t$ satisfies $p \nmid p'$.

*Proof.* First, no nonzero $z \in k$ satisfies $z'/z = n b'$ with $n \in \mathbb{Z}$, $n \ne 0$. Indeed, for $z = c \prod_\alpha (x - \alpha)^{e_\alpha}$ we have $z'/z = \sum_\alpha e_\alpha / (x - \alpha)$, a proper rational function, while $n b'$ is a nonzero polynomial.

Transcendence. Suppose $t \ne 0$ is algebraic over $k$, with monic minimal polynomial $P = \sum_{i=0}^{d} p_i T^i$. Differentiating $P(t) = 0$ and subtracting $d b' P(t) = 0$ gives $\sum_{i<d} (p_i' - (d - i) b' p_i) t^i = 0$, a polynomial relation of degree less than $d$, so all its coefficients vanish. A nonzero $p_i$ with $i < d$ would satisfy $p_i'/p_i = (d - i) b'$, which is impossible. So $P = T^d$ and $t = 0$, a contradiction.

Normal factors. Let $p \ne t$ be monic irreducible of degree $d \ge 1$. Then $p' = \sum_i (p_i' + i b' p_i) t^i$ has degree at most $d$, with coefficient $d b'$ at $t^d$. If $p \mid p'$, then $p' = d b' p$, and the constant coefficients give $p_0' = d b' p_0$. Here $p_0 \ne 0$, since otherwise $t \mid p$ and $p = t$. This is impossible.

Constants. Let $F \in k(t)$ with $F' = 0$ and $F \ne 0$. If $F$ had a pole of order $e \ge 1$ at some $p \ne t$, then $F'$ would have a pole of order $e + 1$ there (the computation in Lemma 2 below), so it has none, and the same holds for $1/F$. So $F = c t^l$ with $c \in k^*$, and $0 = F' = (c' + l b' c) t^l$. If $l \ne 0$, then $c'/c = -l b'$, which is impossible. So $F = c$ with $c' = 0$, that is, $c \in \bar{\mathbb{Q}}$. $\square$

## Lemma 2 (the shape of an elementary integral)

If $f = \sum_k f_k t^k$ has an elementary integral, then for every $k \ne 0$ the equation $y' + k b' y = f_k$ has a solution $y \in \bar{\mathbb{Q}}(x)$.

*Proof.* By Liouville's theorem (see the page on it), there are $v \in k(t)$, constants $c_1, \ldots, c_r \in \bar{\mathbb{Q}}$ and $u_1, \ldots, u_r \in k(t)^*$ with
$$f = v' + \sum_{i=1}^{r} c_i \frac{u_i'}{u_i}. \tag{1}$$
Let $p \ne t$ be a monic irreducible in $k[t]$. By Lemma 1, $p \nmid p'$. If $v$ has a pole of order $e \ge 1$ at $p$, then $v'$ has a pole of order $e + 1 \ge 2$ there: with $v = A / (p^e B)$ and $p \nmid AB$, the numerator of $v'$ over $p^{e+1} B^2$ is $\equiv -e A p' B \not\equiv 0 \pmod p$. The sum $\sum_i c_i u_i'/u_i$ has at most a simple pole at $p$, and $f$ has none. So $v$ has no pole at $p$. Then the part of (1) with a pole at $p$ is $\bigl(\sum_i c_i \nu_p(u_i)\bigr) p'/p$, which must vanish, so $\sum_i c_i \nu_p(u_i) = 0$. Write $u_i = h_i t^{k_i} \prod_{p \ne t} p^{\nu_p(u_i)}$ with $h_i \in k^*$. Then
$$\sum_i c_i \frac{u_i'}{u_i} = \sum_i c_i \frac{h_i'}{h_i} + \Bigl(\sum_i c_i k_i\Bigr) b' + \sum_{p \ne t} \Bigl(\sum_i c_i \nu_p(u_i)\Bigr) \frac{p'}{p} \in k,$$
and $v \in k[t, t^{-1}]$, say $v = \sum_k v_k t^k$. Since $(v_k t^k)' = (v_k' + k b' v_k) t^k$, comparing the coefficients of $t^k$ for $k \ne 0$ in (1) gives $f_k = v_k' + k b' v_k$. $\square$

## Lemma 3 (the Risch differential equation, steps L4 and L5)

Let $k \ne 0$, $\phi = k b' \in \mathbb{Q}[x]$ of degree $m \ge 0$, and $g = a/d \in \mathbb{Q}(x)$ reduced and nonzero. The equation $y' + \phi y = g$ has at most one solution in $\bar{\mathbb{Q}}(x)$. It has one if and only if the code returns one, and then the code returns it.

*Proof.* Uniqueness: the difference $z$ of two solutions satisfies $z' = -\phi z$. If $z \ne 0$, then $z'/z = -\phi$ is a nonzero polynomial, but $z'/z$ for a rational function $z$ is a sum of terms $e/(x - \alpha)$ and tends to $0$ at infinity. So $z = 0$.

Denominator: let $y$ be a solution and $\alpha \in \bar{\mathbb{Q}}$. If $y$ has a pole of order $e \ge 1$ at $\alpha$, then $y'$ has a pole of order $e + 1$ and $\phi y$ of order at most $e$, so $g$ has a pole of order exactly $e + 1 \ge 2$ at $\alpha$. If $y$ has no pole at $\alpha$, neither does $g$. So $g$ has no simple poles, and $y$ has a pole of order $\nu - 1$ wherever $g$ has a pole of order $\nu$. With the squarefree factorization $d = \prod_i d_i^i$, this says $d_1$ is constant, which is the condition $d \mid a h^2$ for $h = \gcd(d, d') = \prod_i d_i^{i-1}$ (as $\gcd(a, d) = 1$), and that $y = q / h$ for a polynomial $q$. If the condition fails, there is no solution and the code returns None.

Polynomial equation: substituting $y = q/h$ and multiplying by $h^2$ gives
$$h q' + (\phi h - h') q = c, \qquad c = a h^2 / d \in \mathbb{Q}[x]. \tag{2}$$
Let $\ell = \phi h - h'$. Since $\deg(\phi h) = m + \deg h > \deg h'$, $\ell$ has degree $s = m + \deg h$ and leading coefficient $\mathrm{lc}(\phi)\,\mathrm{lc}(h)$, and $\deg(h (x^j)') \le \deg h + j - 1 < j + s$. So the operator $\mathcal{L}(q) = h q' + \ell q$ maps $x^j$ to a polynomial of degree exactly $j + s$ with leading coefficient $\mathrm{lc}(\ell)$. The loop of L5 is division by this triangular operator: if $c \ne 0$ and $\deg c < s$, no $q$ has $\mathcal{L}(q) = c$, since $\deg \mathcal{L}(q) = \deg q + s \ge s$ for $q \ne 0$. Otherwise the top term of $q$ is forced to be $\mathrm{lc}(c) / \mathrm{lc}(\ell)\, x^{\deg c - s}$, and the loop subtracts its image and continues with a polynomial of lower degree. It stops after at most $\deg c - s + 1$ rounds, with $c = 0$ and $\mathcal{L}(q) = $ the original $c$, or with None when no solution exists. A solution over $\bar{\mathbb{Q}}$ is also forced term by term in the same way, so it exists exactly when the loop succeeds, and it has rational coefficients. $\square$

## Lemma 4 (Hermite reduction, steps L6 and L7)

For $A, D \in \mathbb{Q}[x]$, $D \ne 0$, `hermite_reduce` returns $R$ and $A^*/D^*$ with $A/D = R' + A^*/D^*$ and $D^*$ squarefree.

*Proof.* The polynomial part $P$ of $A/D$ is integrated term by term. For the proper part, the loop is the linear version of Hermite reduction (Mack; Bronstein, Symbolic Integration I, Section 2.2): with $D^- = \gcd(D, D')$ and $D^* = D / D^-$, the invariant is $A/D = R' + A / (D^- D^*)$. In a round with $D^{-*} = D^- / \gcd(D^-, D^{-\prime})$, the polynomials $D^* D^{-\prime}/D^-$ and $D^{-*}$ are coprime, so the extended Euclidean step finds $B, C$ with $-B D^* D^{-\prime} / D^- + C D^{-*} = A$, and then
$$\frac{A}{D^- D^*} = \Bigl(\frac{B}{D^-}\Bigr)' + \frac{C - B' D^* / D^{-*}}{D^* \gcd(D^-, D^{-\prime})},$$
as a direct differentiation shows. Each round removes one from every multiplicity in $D^-$, so the loop ends with $D^- = 1$ and the remainder $A / D^*$, where $D^*$ is the squarefree part of $D$. $\square$

## Proof of the theorem

(a) For each $k \ne 0$, Lemma 3 gives $y_k' + k b' y_k = f_k$, so $(y_k t^k)' = f_k t^k$. Lemma 4 gives $f_0 = R' + A^*/D^*$ with $D^*$ squarefree. Summing gives the identity. The integral of $A^*/D^*$ with squarefree $D^*$ is a sum $\sum_c c \log v_c$ over the roots $c$ of the Rothstein-Trager resultant, which is elementary.

(b) The algorithm fails only in L3, when for some $k \ne 0$ the equation $y' + k b' y = f_k$ has no solution in $\mathbb{Q}(x)$. By Lemma 3 it then has no solution in $\bar{\mathbb{Q}}(x)$ either, and by Lemma 2 $f$ has no elementary integral. $\blacksquare$
