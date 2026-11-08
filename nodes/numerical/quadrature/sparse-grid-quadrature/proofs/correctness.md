---
title: The combination formula computes the Smolyak rule, which is exact for total degree 2(q - s) + 1 and uses O(2^l l^(s-1)) points
proves: [correctness]
status: full
---

Let $U^1, U^2, \ldots$ be quadrature rules on $[0, 1]$, $U^i$ with $m_i$ nodes, and put $U^0 = 0$ and $\Delta^i = U^i - U^{i-1}$. For a multi-index $\mathbf i = (i_1, \ldots, i_s)$ with all $i_j \ge 1$ write $|\mathbf i| = i_1 + \cdots + i_s$ and $U^{\mathbf i} = U^{i_1} \otimes \cdots \otimes U^{i_s}$, the product rule that applies $U^{i_1}$ in the first variable, $U^{i_2}$ in the second, and so on (see [product quadrature](/product-quadrature/)). The Smolyak rule of level $q \ge s$ is

$$A(q, s) = \sum_{|\mathbf i| \le q} \Delta^{i_1} \otimes \cdots \otimes \Delta^{i_s}.$$

Lines refer to the pseudocode SMOLYAK.

**Lemma 1 (an alternating binomial sum).** For integers $s \ge 1$ and $r \ge 0$, $\sum_{t=0}^{r} (-1)^t \binom{s}{t} = (-1)^r \binom{s-1}{r}$, where $\binom{s-1}{r} = 0$ for $r \ge s$.

*Proof.* Induction on $r$. For $r = 0$ both sides are 1. If it holds for $r$, then adding $(-1)^{r+1}\binom{s}{r+1} = (-1)^{r+1}\big(\binom{s-1}{r+1} + \binom{s-1}{r}\big)$ to $(-1)^r\binom{s-1}{r}$ leaves $(-1)^{r+1}\binom{s-1}{r+1}$. $\square$

**Lemma 2 (the combination formula, proved).**

$$A(q, s) = \sum_{\max(s,\, q - s + 1) \le |\mathbf j| \le q} (-1)^{q - |\mathbf j|} \binom{s - 1}{q - |\mathbf j|}\, U^{\mathbf j}.$$

*Proof.* The tensor product is multilinear, so $\Delta^{i_1} \otimes \cdots \otimes \Delta^{i_s} = \sum_{\mathbf e \in \{0, 1\}^s} (-1)^{|\mathbf e|} U^{\mathbf i - \mathbf e}$, where any term with a zero index vanishes because $U^0 = 0$. Collect the coefficient of $U^{\mathbf j}$ for a fixed $\mathbf j \ge \mathbf 1$: it comes from $\mathbf i = \mathbf j + \mathbf e$ with $|\mathbf j| + |\mathbf e| \le q$, so it is $\sum_{t=0}^{q - |\mathbf j|} (-1)^t \binom{s}{t}$ when $|\mathbf j| \le q$ (there are $\binom{s}{t}$ vectors $\mathbf e$ with $|\mathbf e| = t$, and $t \le s$ automatically). By Lemma 1 it equals $(-1)^{q - |\mathbf j|}\binom{s-1}{q - |\mathbf j|}$, which is 0 when $q - |\mathbf j| \ge s$. Finally $|\mathbf j| \ge s$ always. $\square$

**Lemma 3 (what the lines compute).** SMOLYAK returns $A(q, s)f$ on $[0, 1]^s$, and the implementation returns $V \cdot A(q, s)\tilde f$ on the box $[a, b]$, where $\tilde f(u) = f(a + u \odot (b - a))$ and $V = \prod_j (b_j - a_j)$.

*Proof.* Line L2 runs over exactly the multi-indices of Lemma 2, line L3 sets the coefficient, and lines L4 and L5 add the coefficient times the product weights of $U^{\mathbf j}$ to the entry of each node. Equal nodes of different component grids are merged by their key; since $w f(x) + w' f(x) = (w + w') f(x)$, merging does not change the value. So line L6 returns $\sum_{\mathbf j} c_{\mathbf j} U^{\mathbf j} f = A(q, s) f$. On the box, the affine substitution $x = a + u \odot (b - a)$ has Jacobian $V$ (signed when some $b_j < a_j$, as an iterated integral is). $\square$

**Theorem 1 (exactness, proved).** If each $U^i$ is exact for all polynomials of degree at most $2i - 1$, then $A(q, s)$ is exact for all polynomials in $s$ variables of total degree at most $2(q - s) + 1$, on $[0, 1]^s$ and, via Lemma 3, on any box.

*Proof.* By linearity it suffices to take a monomial $x^{\mathbf k} = x_1^{k_1} \cdots x_s^{k_s}$ with $|\mathbf k| \le 2(q - s) + 1$. Let $\ell_j = \lceil (k_j + 1)/2 \rceil$, the least level $i$ with $2i - 1 \ge k_j$. For $i > \ell_j$ both $U^i$ and $U^{i-1}$ are exact for $x^{k_j}$, so $\Delta^i x^{k_j} = 0$. A product rule applied to a product of functions of separate variables is the product of the one-dimensional rules, so

$$A(q, s)\, x^{\mathbf k} = \sum_{|\mathbf i| \le q} \prod_{j=1}^{s} \Delta^{i_j} x_j^{k_j} = \sum_{|\mathbf i| \le q,\ i_j \le \ell_j} \prod_{j=1}^{s} \Delta^{i_j} x_j^{k_j}.$$

Now $\ell_j \le k_j/2 + 1$, so $\sum_j \ell_j \le |\mathbf k|/2 + s \le q + \tfrac12$, hence $\sum_j \ell_j \le q$ as it is an integer. So every $\mathbf i$ with $i_j \le \ell_j$ has $|\mathbf i| \le q$, and the sum runs over the whole box $1 \le i_j \le \ell_j$. It factorizes into $\prod_j \sum_{i=1}^{\ell_j} \Delta^i x_j^{k_j} = \prod_j U^{\ell_j} x_j^{k_j} = \prod_j \int_0^1 x_j^{k_j}\,dx_j = \int_{[0,1]^s} x^{\mathbf k}$, the sum telescoping and $U^{\ell_j}$ being exact for $x^{k_j}$. An affine map preserves total degree, which gives the statement on boxes. $\square$

**The one-dimensional rules satisfy the hypothesis (proved).** Both families of the implementation use $m_1 = 1$ and $m_i = 2^{i-1} + 1$ nodes, symmetric about $\tfrac12$, with interpolatory weights: the midpoint rule, and the Clenshaw-Curtis or equispaced closed Newton-Cotes rules. An interpolatory rule with $m$ nodes is exact for degree $m - 1$; if the nodes and weights are symmetric and $m$ is odd, it is also exact for $(x - \tfrac12)^m$, an odd function about $\tfrac12$ whose integral and rule value are both 0, hence for degree $m$. Since $m_i \ge 2i - 1$ for all $i \ge 1$, each $U^i$ is exact for degree $2i - 1$.

**Tightness of the example (proved).** For $s = 2$, $q = 3$ and $x_1^2 x_2^2$, of total degree $4 = 2(q - s) + 2$: here $\ell_1 = \ell_2 = 2$ and $\ell_1 + \ell_2 = 4 > q$, so the sum in the proof misses exactly $\mathbf i = (2, 2)$, and $A(3, 2)\,x_1^2 x_2^2 = \tfrac19 - (\Delta^2 x^2)^2$ with $\Delta^2 x^2 = \tfrac13 - \tfrac14 = \tfrac1{12}$, since $U^2$ is exact for $x^2$ and the midpoint rule gives $\tfrac14$. The test file checks this in exact arithmetic. For larger $q$ the Clenshaw-Curtis rules are exact for more than degree $2i - 1$, and $A(q, s)$ is then exact on a larger space than the total degree bound says.

**Theorem 2 (number of points, proved).** If the rules are nested, $\mathrm{nodes}(U^{i-1}) \subseteq \mathrm{nodes}(U^i)$, and $n_i = m_i - m_{i-1}$ ($m_0 = 0$) is the number of new nodes at level $i$, then $A(q, s)$ uses

$$N(q, s) = \sum_{|\mathbf i| \le q} \prod_{j=1}^{s} n_{i_j}$$

distinct points. For $m_i$ as above, $n_1 = 1$, $n_2 = 2$, $n_i = 2^{i-2}$ for $i \ge 3$, and with $\ell = q - s$,

$$N(q, s) \le 2^{\ell + 1} \binom{\ell + s - 1}{s - 1} = O\big(2^{\ell} \ell^{s-1}\big) \quad\text{for fixed } s.$$

*Proof.* The nodes of $U^{\mathbf j}$ for $|\mathbf j| \le q$ form the union, over $\mathbf i \le \mathbf j$ componentwise, of the sets $\prod_j \mathrm{new}(i_j)$, where $\mathrm{new}(i)$ are the nodes first appearing at level $i$; these sets are disjoint for different $\mathbf i$, and as $\mathbf j$ ranges over $|\mathbf j| \le q$, $\mathbf i$ ranges over $|\mathbf i| \le q$. Line L2 visits only $|\mathbf j| \ge q - s + 1$, but every $\mathbf j$ with smaller $|\mathbf j|$ lies below one of those componentwise (raise its first index), so by nesting the union is the same. So the set of points that lines L4 and L5 touch has the stated size. For the bound, $n_i \le 2^{i-1}$, so $\prod_j n_{i_j} \le 2^{|\mathbf i| - s}$, and there are $\binom{t + s - 1}{s - 1}$ multi-indices with $|\mathbf i| = s + t$. Hence $N \le \sum_{t=0}^{\ell} 2^t \binom{t + s - 1}{s - 1} \le \binom{\ell + s - 1}{s - 1}\sum_{t=0}^{\ell} 2^t < 2^{\ell+1}\binom{\ell + s - 1}{s - 1}$. $\square$

A product rule of the same one-dimensional level $\ell + 1$ has $(2^{\ell} + 1)^s$ points; the sparse grid replaces the exponent $s$ on $2^\ell$ by a logarithmic factor.

**Error for smooth functions (cited, asymptotic).** If $f$ has bounded mixed partial derivatives $\partial^{\boldsymbol\alpha} f$ for all $\alpha_j \le r$, the Clenshaw-Curtis sparse grid rule has error $O\big(N^{-r} (\log N)^{(s-1)(r+1)}\big)$ (Novak and Ritter 1996; Gerstner and Griebel 1998). This is the one-dimensional rate up to logarithms, but the hidden constants grow with $s$, and the class of mixed smoothness is much smaller than that of ordinary smoothness of order $r$.

**Floating point.** The weights can be negative (Lemma 2 has negative coefficients), and $\sum_x |W[x]|$ grows with $q$ and $s$: 1.00, 2.33, 6.56, 11.9, 20.7 and 35.3 for $s = 5$ and $\ell = 0, \ldots, 5$. If each value $f(x)$ carries an absolute error at most $\delta$, the result carries at most $\delta \sum_x |W[x]|$ from them, and the compensated sum of line L6 adds only a few rounding errors of the result. With exact rational weights and values (the Newton-Cotes family and Fraction arithmetic), the computation is exact.

**Termination and cost.** Line L2 enumerates finitely many multi-indices with an odometer, without recursion; lines L4 and L5 run $\sum_{\mathbf j} \prod_k m_{j_k}$ times, at most $(3/2)^s\, 2^{\ell + 1}\binom{\ell + s - 1}{s - 1}$ by the argument of Theorem 2 with $m_i \le \tfrac32 \cdot 2^{i-1}$, each with $O(s)$ work; and line L6 evaluates $f$ once per distinct point, $N(q, s)$ times. $\blacksquare$
