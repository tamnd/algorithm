---
title: Reduced ordered TEDs are canonical, and ADD, MUL and EVALUATE are correct
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order, and all polynomials have rational coefficients. Write $R_v = \mathbb{Q}[x_v, \ldots, x_n]$, so $R_{n+1} = \mathbb{Q}$. A sink $(n + 1, q)$ has the level $n + 1$ and the polynomial $f \equiv q$. An inner node $u = (v, c_0, \ldots, c_d)$ has the level $v$, its children have larger levels, and $f_u = \sum_{k=0}^{d} x_v^k f_{c_k}$. By induction from the sinks, $f_u \in R_v$. The store is *reduced* if every inner node has $d \ge 1$ and $c_d$ not the sink 0, no two sinks hold the same number, and no two inner nodes have the same key $(v, c_0, \ldots, c_d)$. Lines L1 to L4 of MK keep it reduced, and CONST keeps the sinks distinct.

**Lemma 1 (Taylor coefficients).** Let $f \in R_v$. (a) There are unique $d \ge 0$ and $f_0, \ldots, f_d \in R_{v+1}$ with $f_d \ne 0$ or $d = 0$, such that $f = \sum_{k=0}^{d} x_v^k f_k$. (b) $f_k = \frac{1}{k!} \frac{\partial^k f}{\partial x_v^k}\big|_{x_v = 0}$. (c) $f \in R_{v+1}$ if and only if $d = 0$.

*Proof.* (a) $R_v$ is the ring $R_{v+1}[x_v]$ of polynomials in $x_v$ with coefficients in $R_{v+1}$: group the monomials of $f$ by their power of $x_v$. A polynomial in $x_v$ has unique coefficients, so the $f_k$ are unique, and $d$ is the degree, or 0 for $f = 0$. (b) For $j \ge k$, $\partial^k x_v^j / \partial x_v^k = \frac{j!}{(j-k)!} x_v^{j-k}$, and for $j < k$ it is 0. At $x_v = 0$ only $j = k$ is left, which gives $k! \, f_k$. The field $\mathbb{Q}$ has characteristic 0, so we may divide by $k!$. (c) By uniqueness in (a). $\square$

So a node is exactly the Taylor expansion of its polynomial at $x_v = 0$, cut after the last nonzero term. Equality here is equality of polynomials. Over the infinite field $\mathbb{Q}$ a polynomial that is 0 at every point is the zero polynomial, so it is also equality of functions on $\mathbb{Q}^n$.

**Theorem 2 (canonicity).** In a reduced store, (a) the polynomial of every inner node on level $v$ is not in $R_{v+1}$, and (b) two distinct nodes have distinct polynomials.

*Proof.* By induction on $k$ from $n + 1$ down to 1, for the nodes on levels $k$ and above. For $k = n + 1$ the nodes are sinks with distinct numbers, so (b) holds, and (a) has no cases.

Let $u = (k, c_0, \ldots, c_d)$. Its children are on levels above $k$. The child $c_d$ is not the sink 0, and the sink 0 has the polynomial 0, so by (b) for those levels $f_{c_d} \ne 0$. With $d \ge 1$, Lemma 1(a) says that $d$ is the degree of $f_u$ in $x_k$, and Lemma 1(c) gives $f_u \notin R_{k+1}$. This is (a).

For (b), let $u \ne w$ be nodes on levels $k$ and above with $f_u = f_w$. If both are above level $k$, (b) for those levels gives a contradiction. If $u$ is on level $k$ and $w$ above it, then $f_w \in R_{k+1}$ and $f_u \notin R_{k+1}$ by (a), a contradiction. If $u = (k, c_0, \ldots, c_d)$ and $w = (k, c'_0, \ldots, c'_{d'})$, then Lemma 1(a) gives $d = d'$ and $f_{c_i} = f_{c'_i}$ for all $i$. By (b) for the higher levels $c_i = c'_i$, so $u$ and $w$ have the same key, and the merging of lines L3 and L4 gives $u = w$. $\square$

**Corollary.** A node whose polynomial lies in $R_{v+1}$ is on a level larger than $v$: an inner node on level $w \le v$ has a polynomial outside $R_{w+1} \supseteq R_{v+1}$. And EQUAL by node ids is correct.

**Lemma 3 (MK and coef).** (a) MK$(v, c_0, \ldots, c_d)$, with all $c_k$ on levels larger than $v$, returns a node with the polynomial $\sum_k x_v^k f_{c_k}$. (b) If $v$ is at most the level of $u$ and $\mathrm{coef}(u, v) = (c_0, \ldots, c_d)$, then $f_u = \sum_k x_v^k f_{c_k}$ and every $c_k$ is on a level larger than $v$.

*Proof.* (a) Line L1 drops children that are the sink 0, which add $x_v^k \cdot 0$. If one child is left, line L2 returns it, and its polynomial is the sum. Otherwise lines L3 and L4 return the node with that key. (b) If $u$ is on level $v$, this is the definition of $f_u$. If not, $\mathrm{coef}$ returns $(u)$, and $f_u = x_v^0 f_u$. $\square$

**Theorem 4 (ADD).** ADD$(f, g)$ returns the node of $f_f + f_g$, and at most $\lvert f \rvert \cdot \lvert g \rvert$ calls reach line L6.

*Proof.* By induction on the sum of the levels of the arguments. The shortcuts for the sink 0 and line L5 are correct. The cache returns only results of earlier calls with the same pair, in either order, which is correct because addition commutes. At line L6, Lemma 3(b) gives $f_f + f_g = \sum_k x_v^k (f_{a_k} + f_{b_k})$, with the shorter list padded by the sink 0. Each recursive call has both arguments on levels larger than $v$, so the level sum grows, and by induction it returns the node of $f_{a_k} + f_{b_k} \in R_{v+1}$. By the corollary that node is on a level larger than $v$, so Lemma 3(a) applies and MK returns the node of the sum. The arguments of every call are nodes reachable from $f$ and from $g$, or the sink 0, which the shortcut handles, and the cache lets each pair reach line L6 once. $\square$

**Theorem 5 (MUL).** MUL$(f, g)$ returns the node of $f_f \cdot f_g$.

*Proof.* By induction on the sum of the levels, as for ADD. The shortcuts for 0 and 1 and line L7 are correct, and so is the cache, since multiplication commutes. At line L8, with $f_f = \sum_i x_v^i f_{a_i}$ and $f_g = \sum_j x_v^j f_{b_j}$ from Lemma 3(b), the coefficients lie in $R_{v+1}$ and commute with $x_v$, so

$$f_f \cdot f_g = \sum_{k} x_v^k \sum_{i + j = k} f_{a_i} f_{b_j}.$$

Each MUL$(a_i, b_j)$ has both arguments on levels larger than $v$, so by induction it returns the node of $f_{a_i} f_{b_j} \in R_{v+1}$, and ADD (Theorem 4) sums them in $c_k$, the node of the inner sum. By the corollary every $c_k$ is on a level larger than $v$, and Lemma 3(a) gives the result at line L9. $\square$

**EVALUATE and BUILD.** Line L10 computes, children first, $\mathit{val}(u) = \sum_k \mathit{val}(c_k) \, x_v^k$ by Horner's rule, so by induction $\mathit{val}(u) = f_u$ at the point. BUILD at line L11 is correct by induction on the expression: a variable $x$ is MK$(x, 0, 1)$, the polynomial $0 + x \cdot 1$, a number is a sink, and $+$, $-$ and $\times$ are ADD, ADD with MUL by $-1$, and MUL. A power is repeated MUL. So two expressions of the same polynomial give the same node, by Theorem 2. $\blacksquare$
