---
title: Reduced ADDs are canonical, APPLY computes the pointwise operation with O(|f| |g|) calls, and SUM-OUT sums the two cofactors
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order. A sink $(n + 1, c)$ has the level $n + 1$ and the function $f \equiv c$. An inner node $u = (v, l, h)$ has the level $v$, both children have larger levels, and $f_u(x) = f_l(x)$ if $x_v = 0$ and $f_h(x)$ if $x_v = 1$. By induction from the sinks, $f_u$ depends only on the variables $x_{v}, \ldots, x_n$, where $v$ is the level of $u$. The store is *reduced* if no inner node has $l = h$, no two sinks have the same value, and no two inner nodes have the same triple; CONST and MK keep it reduced, since they return a stored node when the key exists (lines L1 to L3).

**Theorem 1 (canonicity).** In a reduced store, (a) every inner node $u$ depends on the variable of its level, and (b) two distinct nodes compute distinct functions.

*Proof.* By induction on $k$ from $n + 1$ down to 1, for the nodes on the levels $k$ and above (numbers larger than or equal to $k$). For $k = n + 1$ the nodes are sinks, and distinct sinks have distinct values, so (b) holds and (a) is empty.

Let $k \le n$ and let $u = (k, l, h)$. The children are on levels larger than $k$ and $l \ne h$, so by (b) for those levels $f_l \ne f_h$. Neither depends on $x_k$, so $f_u|_{x_k = 0} = f_l \ne f_h = f_u|_{x_k = 1}$, and $f_u$ depends on $x_k$. This is (a).

For (b), let $u \ne w$ be nodes on levels $k$ and above with $f_u = f_w$. If both are on levels above $k$, (b) for those levels gives a contradiction. If $u$ is on level $k$ and $w$ on a level above $k$, then $f_u$ depends on $x_k$ by (a) and $f_w$ does not, which is a contradiction. If both are on level $k$, say $u = (k, l, h)$ and $w = (k, l', h')$, then $f_l = f_u|_{x_k = 0} = f_w|_{x_k = 0} = f_{l'}$ and in the same way $f_h = f_{h'}$, so $l = l'$ and $h = h'$ by (b) for the higher levels, and the merging rule gives $u = w$. $\square$

So EQUAL by ids is correct: two nodes are equal if and only if their functions are equal.

**Lemma 2 (cof).** If $v$ is at most the level of $u$, and $\mathrm{cof}(u, v) = (u_0, u_1)$, then $f_{u_b} = f_u|_{x_v = b}$ for $b \in \{0, 1\}$, and both $u_0$ and $u_1$ are on levels larger than $v$.

*Proof.* If $u$ is on level $v$, the children are the cofactors by definition. Otherwise $u$ is on a level larger than $v$, so $f_u$ does not depend on $x_v$, and $f_u|_{x_v = b} = f_u$. $\square$

**Theorem 2 (APPLY).** APPLY$(\mathrm{op}, f, g)$ returns the node of $x \mapsto \mathrm{op}(f_f(x), f_g(x))$. It makes at most $\lvert f \rvert \cdot \lvert g \rvert$ calls that reach line L6, and the result has at most $\lvert f \rvert \cdot \lvert g \rvert$ nodes, where $\lvert f \rvert$ is the number of nodes reachable from $f$.

*Proof.* Correctness is by induction on the sum of the levels of the two arguments, which grows in every recursive call, by Lemma 2. Line L4 is correct for two constants. The cache of line L5 only returns results of earlier calls with the same arguments. At line L6, $v$ is at most both levels, so Lemma 2 applies. For $b \in \{0, 1\}$, the result at $x_v = b$ must be $\mathrm{op}(f_f|_{x_v = b}, f_g|_{x_v = b}) = \mathrm{op}(f_{f_b}, f_{g_b})$, which the recursive call of line L7 computes by induction. Neither result depends on $x_v$, since both arguments are on levels larger than $v$ and the result of a call is on a level at least the smaller level of its arguments (by induction, since MK returns a node of level $v$ or one of its arguments). So MK$(v, \cdot, \cdot)$ has the right function.

For the cost, every argument pair of a call is $(f', g')$ where $f'$ is reachable from $f$ and $g'$ from $g$, since cof returns the node or its children. With the cache, each pair reaches line L6 at most once, so there are at most $\lvert f \rvert \cdot \lvert g \rvert$ such calls, each with $O(1)$ expected work besides the recursion. Each node of the result is returned by one of these calls or by line L4, and the sinks of the result correspond to pairs of sinks. So the result has at most $\lvert f \rvert \cdot \lvert g \rvert$ nodes. $\square$

**Theorem 3 (SUM-OUT).** For $D$ a set of numbers, SUM-OUT$(f, v)$ returns the node of $s(x) = f_f|_{x_v = 0}(x) + f_f|_{x_v = 1}(x)$.

*Proof.* By induction on the level of $f$, from the bottom. If $f$ is a sink or on a level larger than $v$, then $f_f$ does not depend on $x_v$, so $s = f_f + f_f$, which is APPLY$(+, f, f)$. If $f = (v, l, h)$, then $s = f_l + f_h$, which is APPLY$(+, l, h)$ by Theorem 2. If $f = (w, l, h)$ with $w < v$, then for $x_w = 0$ the two restrictions of $f_f$ to $x_v = b$ are the restrictions of $f_l$, so $s|_{x_w = 0}$ is SUM-OUT$(l, v)$, and in the same way $s|_{x_w = 1}$ is SUM-OUT$(h, v)$. These results do not depend on $x_w$, since they are built from nodes on levels larger than $w$, so MK$(w, \cdot, \cdot)$ has the function $s$. $\square$

**Corollary (matrix product).** Let $A(r, k)$ and $B(k, c)$ be ADDs over disjoint groups of variables $r$, $k$, $c$. Then summing out all variables of $k$ from APPLY$(\times, A, B)$ gives the function $\sum_k A(r, k) B(k, c)$, by Theorem 2 and $\lvert k \rvert$ uses of Theorem 3, since each SUM-OUT replaces the sum over one bit of $k$ by its two terms. $\blacksquare$
