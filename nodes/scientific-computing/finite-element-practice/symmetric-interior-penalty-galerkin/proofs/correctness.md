---
title: SIPG assembles a symmetric consistent form that is positive definite above the penalty bound
proves: [correctness]
status: full
---

**Setting.** The problem is $-u'' = f$ on $(0, 1)$ with $u(0) = g_0$ and $u(1) = g_1$. The mesh has the nodes $x_e = eh$, $e = 0, \ldots, m$, $h = 1/m$, and the cells $K_j = (x_j, x_{j+1})$. The space $V_h$ holds the functions whose restriction to each cell is a polynomial of degree at most $k \ge 1$, with no continuity between cells. For $v \in V_h$ the jump and the average at a node are

$$[v]_e = v(x_e^-) - v(x_e^+), \quad \{v'\}_e = \tfrac12\bigl(v'(x_e^-) + v'(x_e^+)\bigr) \quad (0 < e < m),$$

$$[v]_m = v(1^-), \quad \{v'\}_m = v'(1^-), \qquad [v]_0 = -v(0^+), \quad \{v'\}_0 = v'(0^+).$$

Let $[g]_0 = -g_0$, $[g]_m = g_1$ and $[g]_e = 0$ for $0 < e < m$. For $\sigma > 0$ the SIPG forms are

$$a_h(w, v) = \sum_j (w', v')_{K_j} - \sum_{e=0}^m\bigl(\{w'\}_e[v]_e + \{v'\}_e[w]_e\bigr) + \sum_{e=0}^m\frac{\sigma}{h}[w]_e[v]_e,$$

$$l_h(v) = (f, v) - \sum_{e \in \{0, m\}}\{v'\}_e[g]_e + \sum_{e \in \{0, m\}}\frac{\sigma}{h}[g]_e[v]_e.$$

The basis of $V_h$ is $\phi_{j,r}(x) = \xi^r$ on $K_j$ with $\xi = (x - x_j)/h$ and $0$ elsewhere, for $0 \le r \le k$.

**Claim 1 (assembly).** The matrix and the vector built by lines L1 to L6 are $A[(j, r), (i, s)] = a_h(\phi_{i,s}, \phi_{j,r})$ and $b[(j, r)] = l_h(\phi_{j,r})$, when the quadrature of line L3 is exact for $f\phi_{j,r}$.

*Proof.* The volume part: $\phi_{i,s}'\phi_{j,r}'$ is zero unless $i = j$, and on $K_j$ it equals $\frac{rs}{h^2}\xi^{r+s-2}$, so its integral is $\frac{rs}{h(r+s-1)}$ for $r, s \ge 1$ and $0$ otherwise. Line L2 adds exactly these values. Line L3 adds $(f, \phi_{j,r})_{K_j}$, which is $(f, \phi_{j,r})$ since $\phi_{j,r}$ vanishes off $K_j$.

The node part: at node $e$ the code lists the sides of the node as tuples (cell, end, weight $w$, sign $s$). An interior node has the left cell at its right end with $(w, s) = (\tfrac12, +1)$ and the right cell at its left end with $(\tfrac12, -1)$; node $m$ has only the left cell with $(1, +1)$; node $0$ has only the right cell with $(1, -1)$. Comparing with the definitions, for every $v \in V_h$

$$\{v'\}_e = \sum_{\text{sides}} w\,v'_{\text{side}}(x_e), \qquad [v]_e = \sum_{\text{sides}} s\,v_{\text{side}}(x_e),$$

where $v_{\text{side}}$ is the polynomial of that cell. A basis function is nonzero on one cell only, so it contributes to these sums only through the side of its own cell. Line L5 loops over all pairs (trial side, test side) and adds $-w_u\phi'_s\,s_v\phi_r - w_v\phi'_r\,s_u\phi_s + \frac{\sigma}{h}s_u\phi_s\,s_v\phi_r$, with the values and derivatives from local_traces. Summing over the pairs gives the products $-\{\phi_{i,s}'\}_e[\phi_{j,r}]_e - \{\phi_{j,r}'\}_e[\phi_{i,s}]_e + \frac{\sigma}{h}[\phi_{i,s}]_e[\phi_{j,r}]_e$, because each product of two sums is the sum over all pairs. The values in local_traces are those of $\xi^r$: at the left end the value is $1$ for $r = 0$ and the derivative is $1/h$ for $r = 1$, all others $0$; at the right end the value is $1$ and the derivative is $r/h$. Line L6 adds $-\{\phi_{j,r}'\}_e[g]_e + \frac{\sigma}{h}[g]_e[\phi_{j,r}]_e$ at $e = 0$ and $e = m$, using the single side there. Summing over all nodes gives $a_h$ and $l_h$. $\square$

**Claim 2 (consistency).** If $u \in H^2(0, 1)$ is the exact solution, then $a_h(u, v) = l_h(v)$ for all $v \in V_h$.

*Proof.* In one dimension $u \in H^2$ means $u$ and $u'$ are continuous, so $[u]_e = 0$ and $\{u'\}_e = u'(x_e)$ at interior nodes, and $[u]_e = [g]_e$ at the two boundary nodes. Integration by parts on each cell gives $(u', v')_{K_j} = -(u'', v)_{K_j} + u'(x_{j+1})v(x_{j+1}^-) - u'(x_j)v(x_j^+)$. Summing over $j$ and collecting the terms at each node,

$$\sum_j (u', v')_{K_j} = (f, v) + \sum_{e=0}^m u'(x_e)[v]_e,$$

because at an interior node the two terms give $u'(x_e)(v(x_e^-) - v(x_e^+))$, at $x = 1$ the term is $u'(1)v(1^-)$ and at $x = 0$ it is $-u'(0)v(0^+)$. So the first two sums of $a_h(u, v)$ add up to $(f, v)$. The remaining terms only involve $[u]_e$, which is $0$ inside and $[g]_e$ at the boundary, so they equal $-\sum_{e \in \{0,m\}}\{v'\}_e[g]_e + \sum_{e \in \{0,m\}}\frac{\sigma}{h}[g]_e[v]_e$. Together this is $l_h(v)$. $\square$

**Claim 3 (symmetry).** $a_h(w, v) = a_h(v, w)$, so the matrix of Claim 1 is symmetric.

*Proof.* Each of the three sums is unchanged when $w$ and $v$ are exchanged: the first and the third are symmetric products, and the middle sum contains both $\{w'\}[v]$ and $\{v'\}[w]$. $\square$

**Lemma 4 (trace inverse inequality).** For a polynomial $p$ of degree at most $n$ on an interval $I$ of length $h$ and an end point $z$ of $I$, $p(z)^2 \le \frac{(n+1)^2}{h}\|p\|_{L^2(I)}^2$.

*Proof.* Map $I$ to $(-1, 1)$ by an affine map that sends $z$ to $1$; then $\|p\|_I^2 = \frac{h}{2}\|\hat p\|_{(-1,1)}^2$ and $p(z) = \hat p(1)$. The Legendre polynomials $P_i$ satisfy $P_i(1) = 1$ and $\int_{-1}^1 P_iP_l = \frac{2}{2i+1}\delta_{il}$, so $L_i = \sqrt{(2i+1)/2}\,P_i$ for $i = 0, \ldots, n$ form an orthonormal basis of the polynomials of degree at most $n$. Write $\hat p = \sum_i c_iL_i$. By the Cauchy-Schwarz inequality, $\hat p(1)^2 = \bigl(\sum_i c_i\sqrt{(2i+1)/2}\bigr)^2 \le \sum_i c_i^2\,\sum_{i=0}^n\frac{2i+1}{2} = \frac{(n+1)^2}{2}\|\hat p\|^2$. Then $p(z)^2 \le \frac{(n+1)^2}{2}\cdot\frac{2}{h}\|p\|_I^2$. $\square$

**Claim 5 (positive definiteness).** Let $c = 3/2$ if $m \ge 2$ and $c = 2$ if $m = 1$. If $\sigma > ck^2$, then for all $v \in V_h$

$$a_h(v, v) \ge \theta\Bigl(\sum_j\|v'\|_{K_j}^2 + \sum_e\frac{1}{h}[v]_e^2\Bigr), \qquad \theta = \min\Bigl(\frac{\sigma - ck^2}{\sigma + ck^2}, \frac{\sigma - ck^2}{2}\Bigr) > 0,$$

and $a_h(v, v) = 0$ only for $v = 0$. So the matrix is symmetric positive definite.

*Proof.* $a_h(v, v) = \sum_j\|v'\|_{K_j}^2 - 2\sum_e\{v'\}_e[v]_e + \frac{\sigma}{h}\sum_e[v]_e^2$. For $\delta > 0$, $2|\{v'\}_e[v]_e| \le \delta h\{v'\}_e^2 + \frac{1}{\delta h}[v]_e^2$. At an interior node $\{v'\}_e^2 \le \frac12\bigl(v'(x_e^-)^2 + v'(x_e^+)^2\bigr)$, and at a boundary node $\{v'\}_e^2$ is the square of the one-sided value. So $\sum_e h\{v'\}_e^2$ is at most a sum over the cell ends of $\omega\,h\,v'(\text{end})^2$, with $\omega = \frac12$ at an interior node and $\omega = 1$ at a boundary node. The two weights of one cell add up to at most $c$: to $1$ for a cell with two interior ends, to $\frac32$ for a cell with one boundary end, and to $2$ only when $m = 1$. By Lemma 4 with $n = k - 1$, $h\,v'(\text{end})^2 \le k^2\|v'\|_{K_j}^2$. Hence $\sum_e h\{v'\}_e^2 \le ck^2\sum_j\|v'\|_{K_j}^2$ and

$$a_h(v, v) \ge (1 - \delta ck^2)\sum_j\|v'\|_{K_j}^2 + \Bigl(\sigma - \frac1\delta\Bigr)\sum_e\frac1h[v]_e^2.$$

Take $\delta = 2/(\sigma + ck^2)$. Then $1 - \delta ck^2 = \frac{\sigma - ck^2}{\sigma + ck^2}$ and $\sigma - \frac1\delta = \frac{\sigma - ck^2}{2}$, both positive, which gives the bound. If $a_h(v, v) = 0$, then $v' = 0$ on every cell and every jump is $0$. So $v$ is one constant on $(0, 1)$, and $[v]_m = v(1^-) = 0$ makes it $0$. $\square$

**Conclusion.** By Claim 1 the code builds the matrix of $a_h$ and the vector of $l_h$ in the basis $\phi_{j,r}$. By Claims 3 and 5 the matrix is symmetric positive definite when $\sigma > ck^2$, in particular for the default $\sigma = 2k^2 + 1$ of the code, so it is nonsingular, Gaussian elimination in line L7 finds the unique solution, and line L8 returns its coefficients cell by cell. By Claim 2 the exact solution satisfies the same equations, so the error $e = u - u_h$ satisfies $a_h(e, v) = 0$ for all $v \in V_h$. In particular, if $u$ is a polynomial of degree at most $k$, then $u \in V_h$ solves the discrete problem, and by uniqueness $u_h = u$. $\blacksquare$
