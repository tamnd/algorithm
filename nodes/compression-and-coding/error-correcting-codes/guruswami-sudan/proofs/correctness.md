---
title: The Guruswami-Sudan decoder returns every polynomial with agreement at least t
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $F$ be a field, $a_1, \ldots, a_n \in F$ distinct, $y_1, \ldots, y_n \in F$, $2 \le k \le n$ and $r \ge 1$. Let $D$ and $t = \lfloor D/r \rfloor + 1$ be as in lines L1 and L2, so $t r > D$. A polynomial $f \in F[x]$ is *good* if $\deg f < k$ and $f(a_i) = y_i$ for at least $t$ indices $i$. We show that the algorithm returns exactly the good polynomials. We use that $F[x, y]$ is a unique factorization domain.

**Lemma 1 (interpolation).** Line L3 finds a nonzero $Q$.

*Proof.* Line L1 is well defined, since $N(D) \ge D + 1$ grows without bound. For a point $(a, b)$, the binomial theorem gives

$$Q(x + a, y + b) = \sum_{i, j} q_{ij} \sum_{u \le i} \sum_{v \le j} \binom{i}{u} \binom{j}{v} a^{i-u} b^{j-v} x^u y^v,$$

so the coefficient of $x^u y^v$ is $Q^{[u,v]}(a, b)$, a linear form in the $q_{ij}$. The conditions of line L3 are $n \cdot r(r+1)/2$ homogeneous linear equations, one for each point and each pair $(u, v)$ with $u + v < r$. The unknowns are the $N(D)$ coefficients $q_{ij}$ with $i + (k-1) j \le D$. By line L1, there are more unknowns than equations, so the system has a nonzero solution, and Gaussian elimination finds one. $\square$

**Lemma 2 (good polynomials are factors).** If $f$ is good, then $y - f(x)$ divides $Q(x, y)$.

*Proof.* Let $R(x) = Q(x, f(x))$. Each monomial $q_{ij} x^i f(x)^j$ has degree at most $i + (k-1) j \le D$, so $\deg R \le D$ or $R = 0$.

Let $a = a_i$ with $f(a) = y_i = b$. By the definition of line L3, $Q(x + a, y + b) = \sum_{u + v \ge r} c_{uv} x^u y^v$ for some $c_{uv} \in F$. The polynomial $f(x + a) - b = f(x + a) - f(a)$ is zero at $x = 0$, so it equals $x h(x)$ for some $h \in F[x]$. Then

$$R(x + a) = Q\bigl(x + a, (f(x + a) - b) + b\bigr) = \sum_{u + v \ge r} c_{uv} x^u x^v h(x)^v,$$

and each term is divisible by $x^{u+v}$, so by $x^r$. Hence $(x - a_i)^r$ divides $R(x)$.

The good $f$ agrees in at least $t$ places with distinct $a_i$, and the factors $(x - a_i)^r$ are pairwise coprime. So their product, of degree at least $t r > D$, divides $R$. Since $\deg R \le D$ when $R \ne 0$, we get $R = 0$. View $Q$ as a polynomial in $y$ over $F[x]$. Division by the monic polynomial $y - f(x)$ gives $Q = (y - f(x)) S(x, y) + Q(x, f(x)) = (y - f(x)) S(x, y)$. $\square$

**Lemma 3 (the recursion of line L4).** Let $P \in F[x, y]$ be nonzero, and let $s \ge 1$. Suppose $g = g_0 + g_1 x + \cdots + g_{s-1} x^{s-1}$ and $y - g(x)$ divides $P$. Then the recursion started on $P$ with $s$ levels left returns the coefficient list of $g$.

*Proof.* By induction on $s$. Let $x^m$ be the highest power of $x$ that divides $P$, and $P = x^m P_1$. The polynomial $y - g(x)$ has degree $1$ in $y$ and leading coefficient $1$, so it is irreducible and does not divide $x$. As $F[x, y]$ is a unique factorization domain, $y - g(x)$ divides $P_1$, say $P_1 = (y - g(x)) S$. Since $x$ does not divide $P_1$, the polynomial $P_1(0, y)$ is not zero. Also $P_1(0, y) = (y - g_0) S(0, y)$, so $g_0$ is a root of the nonzero polynomial $P_1(0, y)$. The search over all field elements finds it.

If $s = 1$, the recursion returns $(g_0)$. If $s > 1$, it goes on with $P'(x, y) = P_1(x, x y + g_0)$. This is not zero: if $P_1$ has degree $L$ in $y$ with leading coefficient $c_L(x) \ne 0$, then the coefficient of $y^L$ in $P'$ is $x^L c_L(x) \ne 0$. Let $g'(x) = g_1 + g_2 x + \cdots + g_{s-1} x^{s-2}$, so $g(x) = g_0 + x g'(x)$. Then

$$P'(x, y) = \bigl(x y + g_0 - g(x)\bigr) S(x, x y + g_0) = x \bigl(y - g'(x)\bigr) S(x, x y + g_0),$$

so $y - g'(x)$ divides $P'$. By induction, the recursion on $P'$ with $s - 1$ levels left returns $(g_1, \ldots, g_{s-1})$, and the prefix $g_0$ completes the list of $g$. $\square$

**Theorem.** The algorithm returns exactly the good polynomials.

*Proof.* By Lemma 1, $Q \ne 0$. Let $f$ be good. By Lemma 2, $y - f(x)$ divides $Q$. By Lemma 3 with $P = Q$ and $s = k$, line L4 puts $f$ (its $k$ coefficients, with zeros on top if $\deg f < k - 1$) in $C$. Line L5 keeps it, since it agrees in at least $t$ places. Conversely, line L5 keeps only polynomials of degree less than $k$ with at least $t$ agreements, and those are good. Repeated candidates are kept once, so the output is the set of good polynomials.

**Termination.** Lines L1 and L2 end, since $N(D)$ grows with $D$. Line L3 is one Gaussian elimination on a finite matrix. The recursion of line L4 has depth $k$, and each call tries the $|F|$ field elements, which is finite when $F$ is finite as in the implementation. Each call does finitely many polynomial operations. Line L5 checks finitely many candidates at $n$ points. $\blacksquare$
