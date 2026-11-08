---
title: Correctness of Smolyak sparse grid interpolation
proves: [correctness, termination]
status: full
---

Notation: for each level $i \ge 1$, $X^i \subset [-1, 1]$ is a set of $m(i)$ distinct nodes, with $m$ nondecreasing, and $U^i$ maps a function of one variable to its interpolating polynomial of degree at most $m(i) - 1$ on $X^i$; $U^0 = 0$ and $\Delta^i = U^i - U^{i-1}$. Multi-indices $\mathbf{i} \in \mathbb{N}^d$ have entries $\ge 1$, $|\mathbf{i}| = \sum_j i_j$, and $\mathbf{i} \le \mathbf{k}$ is componentwise. For operators $V_1, \ldots, V_d$ on functions of one variable, $V_1 \otimes \cdots \otimes V_d$ applies $V_j$ in the $j$-th variable; on functions of the form $g_1 \otimes \cdots \otimes g_d$ (that is, $g_1(x_1) \cdots g_d(x_d)$) it gives $V_1 g_1 \otimes \cdots \otimes V_d g_d$, and for interpolation operators the tensor product is well defined on all functions because it is a finite linear combination of point evaluations. $q = d + L$ with $L \ge 0$. SMOLYAK computes
$$S = \sum_{\max(d, q-d+1) \le |\mathbf{k}| \le q} c_{\mathbf{k}}\, U^{k_1} \otimes \cdots \otimes U^{k_d}, \qquad c_{\mathbf{k}} = (-1)^{q - |\mathbf{k}|} \binom{d-1}{q - |\mathbf{k}|}.$$

**Lemma 1 (alternating binomial sums).** For integers $d \ge 1$ and $s \ge 0$, $\sum_{r=0}^{s} (-1)^r \binom{d}{r} = (-1)^s \binom{d-1}{s}$, which is $0$ for $s \ge d$.

*Proof.* Induction on $s$: the case $s = 0$ is $1 = 1$, and $(-1)^{s} \binom{d-1}{s} + (-1)^{s+1} \binom{d}{s+1} = (-1)^{s+1} \big(\binom{d}{s+1} - \binom{d-1}{s}\big) = (-1)^{s+1} \binom{d-1}{s+1}$ by Pascal's rule. $\square$

**Lemma 2 (combination formula).** $S = A(q, d) := \sum_{|\mathbf{i}| \le q} \Delta^{i_1} \otimes \cdots \otimes \Delta^{i_d}$.

*Proof.* Expanding, $\Delta^{i_1} \otimes \cdots \otimes \Delta^{i_d} = \sum_{\mathbf{e} \in \{0,1\}^d} (-1)^{|\mathbf{e}|}\, U^{i_1 - e_1} \otimes \cdots \otimes U^{i_d - e_d}$. Terms with some $i_j - e_j = 0$ vanish since $U^0 = 0$. So the coefficient of $U^{k_1} \otimes \cdots \otimes U^{k_d}$ with $\mathbf{k} \ge 1$ in $A(q, d)$ is the sum of $(-1)^{|\mathbf{e}|}$ over $\mathbf{e} \in \{0,1\}^d$ with $|\mathbf{k}| + |\mathbf{e}| \le q$; there are $\binom{d}{r}$ vectors with $|\mathbf{e}| = r$, so the coefficient is $\sum_{r=0}^{q - |\mathbf{k}|} (-1)^r \binom{d}{r}$ when $|\mathbf{k}| \le q$ and $0$ otherwise. By Lemma 1 this is $c_{\mathbf{k}}$ when $q - |\mathbf{k}| \le d - 1$ and $0$ when $q - |\mathbf{k}| \ge d$. Since $|\mathbf{k}| \ge d$ always, the surviving $\mathbf{k}$ are exactly those enumerated by SMOLYAK. $\square$

**Lemma 3 (one-dimensional differences).** (a) If $\deg g \le m(k) - 1$, then $U^i g = g$ for all $i \ge k$, so $\Delta^i g = 0$ for $i > k$ and $\sum_{i=1}^{k} \Delta^i g = U^k g = g$. (b) If the nodes are nested, $X^{i-1} \subset X^i$, then for every $g$ and every $x \in X^{k}$, $(\Delta^i g)(x) = 0$ for $i > k$, and $\sum_{i=1}^{k} (\Delta^i g)(x) = (U^k g)(x) = g(x)$.

*Proof.* (a) $m$ is nondecreasing, so $g$ lies in the polynomial space of $U^i$ for $i \ge k$, and interpolation reproduces that space. The sum telescopes to $U^k g - U^0 g$. (b) For $i > k \ge 1$, $x \in X^k \subset X^{i-1} \subset X^i$, so $U^i g$ and $U^{i-1} g$ both equal $g$ at $x$. The sum telescopes to $(U^k g)(x) = g(x)$ because $x \in X^k$. $\square$

**Theorem 1 (exactness).** Let $g = g_1 \otimes \cdots \otimes g_d$ with $\deg g_j \le m(k_j) - 1$ for some $\mathbf{k} \ge 1$ with $|\mathbf{k}| \le q$. Then $S g = g$. Consequently $S$ reproduces the span of such products; when $m(i) = 2^{i-1} + 1$ for $i \ge 2$, this span contains every polynomial of total degree at most $L$.

*Proof.* By Lemma 2, $S g = \sum_{|\mathbf{i}| \le q} \prod_j \Delta^{i_j} g_j$ (a product of functions of different variables). By Lemma 3(a) every term with some $i_j > k_j$ vanishes. Every $\mathbf{i} \le \mathbf{k}$ has $|\mathbf{i}| \le |\mathbf{k}| \le q$, so the sum is exactly $\sum_{\mathbf{i} \le \mathbf{k}} \prod_j \Delta^{i_j} g_j = \prod_j \sum_{i=1}^{k_j} \Delta^{i} g_j = \prod_j g_j$. For the total degree claim take a monomial $x^{\mathbf{a}}$ with $|\mathbf{a}| \le L$ and put $k_j = 1$ if $a_j = 0$ and $k_j = 1 + \max(1, \lceil \log_2 a_j \rceil)$ otherwise; then $m(k_j) - 1 \ge a_j$ (as $m(1) - 1 = 0$, and for $k_j \ge 2$, $m(k_j) - 1 = 2^{k_j - 1} \ge a_j$) and $k_j - 1 \le a_j$, so $|\mathbf{k}| \le d + |\mathbf{a}| \le q$. $S$ is linear, which extends exactness to sums. $\square$

**Theorem 2 (interpolation).** If the nodes are nested, then $(S f)(x) = f(x)$ for every function $f$ and every point $x$ of the sparse grid $H(q, d) = \bigcup_{|\mathbf{k}| = q} X^{k_1} \times \cdots \times X^{k_d}$.

*Proof.* Let $x = (x_1, \ldots, x_d)$ with $x_j \in X^{k_j}$ and $|\mathbf{k}| \le q$. Point evaluation at $x$ composed with $\Delta^{i_1} \otimes \cdots \otimes \Delta^{i_d}$ is the tensor product of the one-dimensional functionals $\lambda_{i_j} = \delta_{x_j} \circ \Delta^{i_j}$, each a finite combination of point evaluations, applied to $f$. By Lemma 3(b), $\lambda_{i_j} = 0$ when $i_j > k_j$, so those terms vanish, and the rest give $\sum_{\mathbf{i} \le \mathbf{k}} \lambda_{i_1} \otimes \cdots \otimes \lambda_{i_d} = \bigotimes_j \sum_{i=1}^{k_j} \lambda_i = \bigotimes_j \delta_{x_j} = \delta_x$. Hence $(A(q, d) f)(x) = f(x)$, and $S = A(q, d)$ by Lemma 2. $\square$

**Implementation remarks.** SMOLYAK samples $f$ on each component grid $X^{k_1} \times \cdots \times X^{k_d}$ and stores values by exact node position, so every value it uses is $f$ at that point; with nested nodes all component grids lie in $H(q, d)$. Line L4 evaluates $U^{k_1} \otimes \cdots \otimes U^{k_d} f$ at $t$ as $\sum_{y} f(y) \prod_j \ell_{j, y_j}(t_j)$ over the grid, with $\ell_{j, y_j}$ the Lagrange basis polynomials, which is the tensor product interpolant. So the returned value is $(S f)(t)$.

**Termination.** The set of multi-indices with $|\mathbf{k}| \le q$ and entries $\ge 1$ is finite ($\binom{q}{d}$ elements), each component grid is finite, and every step is a finite computation; the enumeration recurses only to depth $d$. $\square$
