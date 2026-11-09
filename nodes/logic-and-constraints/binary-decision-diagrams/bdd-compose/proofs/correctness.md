---
title: COMPOSE returns the reduced ordered BDD of f with g in place of x_i
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order. The store is a [reduced ordered BDD](/reduced-ordered-bdd/) store, $f_u$ is the function of node $u$, and the level of a terminal is $n + 1$. MK$(j, l, h)$ returns the node of $(\neg x_j \wedge f_l) \vee (x_j \wedge f_h)$ when $l$ and $h$ are below level $j$, and ITE$(g, h_1, h_0)$ returns the node of $(f_g \wedge f_{h_1}) \vee (\neg f_g \wedge f_{h_0})$; see the [ITE operator](/ite-operator/). For a function $f$, the composition is $f[x_i := g](a) = f(a[x_i := g(a)])$, where $a[x_i := c]$ is $a$ with $x_i$ set to $c$.

**Lemma 1 (composition).** $f[x_i := g] = (g \wedge f|_{x_i=1}) \vee (\neg g \wedge f|_{x_i=0})$.

*Proof.* Fix an input $a$ and let $c = g(a)$. Then $f[x_i := g](a) = f(a[x_i := c]) = f|_{x_i=c}(a)$, and the right side at $a$ picks $f|_{x_i=1}(a)$ if $c = 1$ and $f|_{x_i=0}(a)$ if $c = 0$. $\square$

**Lemma 2 (RESTRICT).** RESTRICT$(u, i, b)$ returns the node of $f_u|_{x_i=b}$, whose level is at least the level of $u$, and it reaches each node below $u$ at most once past line L5.

*Proof.* By induction on the number of nodes below $u$. At line L4, the level of $u$ is larger than $i$, so $f_u$ does not depend on $x_i$ and the cofactor is $f_u$. A memo hit at line L5 returns a value that line L8 stored for the same $u$ in this call. At line L6, $u = (i, l, h)$ and $f_u = (\neg x_i \wedge f_l) \vee (x_i \wedge f_h)$, where $f_l$ and $f_h$ do not depend on $x_i$, so the cofactor by $x_i = b$ is $f_h$ if $b = 1$ and $f_l$ if $b = 0$. At line L7, $u = (j, l, h)$ with $j < i$. A cofactor by $x_i$ commutes with the Shannon expansion by $x_j$, so $f_u|_{x_i=b} = (\neg x_j \wedge f_l|_{x_i=b}) \vee (x_j \wedge f_h|_{x_i=b})$. By induction the two calls return nodes of these cofactors at levels larger than $j$, and MK returns the node of $f_u|_{x_i=b}$ at level $j$ or larger. Each node is stored in the memo the first time it passes line L5, so it passes line L5 at most once. $\square$

**Theorem.** COMPOSE$(f, i, g)$ returns the node of $f_f[x_i := f_g]$, and the store stays reduced.

*Proof.* By Lemma 2, lines L1 and L2 give the nodes of $f|_{x_i=0}$ and $f|_{x_i=1}$. Line L3 returns the node of $\mathrm{ite}(g, f|_{x_i=1}, f|_{x_i=0})$, which is $f[x_i := g]$ by Lemma 1. All new nodes come from MK, which keeps the store reduced. By the [canonicity theorem](/bdd-canonicity/), the node is the only node of this function in the store. $\blacksquare$

**Cost.** Each RESTRICT call does $O(1)$ work for each node of $f$ that passes line L5, so it takes $O(|f|)$ expected time. Every node of its result is a node of $f$ below level $i$ or a node made by MK for one node of $f$ above level $i$, so $|f|_{x_i=b}| \leq |f|$. ITE on arguments of sizes $|g|$, $|f_1|$ and $|f_0|$ takes $O(|g| \cdot |f_1| \cdot |f_0|)$ expected time and makes at most that many nodes. So COMPOSE takes $O(|f|^2 \cdot |g|)$ expected time, and $|f[x_i := g]| \leq |f|^2 \cdot |g|$.
