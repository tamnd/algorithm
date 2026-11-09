---
title: Reduced ordered decision diagrams are correct and canonical
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$, tested in this order, and $x_i$ takes values in $D_i = \{0, \ldots, d_i - 1\}$. A terminal $t$ has a value $\mathrm{val}(t) \in T$ and the level $n + 1$. An inner node $u$ on level $i$ has the children $c_0(u), \ldots, c_{d_i-1}(u)$. Its function $f_u : D_1 \times \cdots \times D_n \to T$ is defined from the bottom up:

$$f_u(x) = f_{c_{x_i}(u)}(x), \qquad f_t(x) = \mathrm{val}(t).$$

For $v \in D_i$, the cofactor $f|_{x_i=v}$ is $f$ with $x_i$ fixed to $v$. As in the Boolean [Shannon expansion](/shannon-expansion/), $f(x) = (f|_{x_i=v})(x)$ for each $x$ with $x_i = v$.

**Invariant (S).** (a) No inner node has all its children equal. (b) Each child has a larger level than its parent. (c) No two inner nodes have the same pair $(i, (c_0, \ldots, c_{d_i-1}))$, and no two terminals have the same value. (d) The unique table maps each such key to its node.

The store starts empty, and only TERMINAL and MK add nodes. TERMINAL adds a terminal only for a value that is not yet in the table.

**Lemma 1 (MK).** If each $c_v$ has a level larger than $i$, MK$(i, c)$ keeps (S) and returns a node $u$ with $f_u(x) = f_{c_{x_i}}(x)$ for each $x$, and with $\mathrm{lev}(u) \ge i$.

*Proof.* If all $c_v$ are equal (line L1), the node $c_0$ has this function, since $f_{c_{x_i}} = f_{c_0}$ for each $x$. Otherwise line L2 returns the node with the key, if there is one, and lines L3 and L4 add a new node with the key otherwise. The new node satisfies (a) by line L1, (b) by the hypothesis, and (c) and (d) because its key was not in the table. $\square$

**Lemma 2 (EVAL).** EVAL$(u, x)$ returns $f_u(x)$. Line L7 replaces $u$ by $c_{x_i}(u)$, which keeps $f_u(x)$ by the definition, and the level grows at each step. Line L8 returns the value of the terminal.

**Lemma 3 (APPLY).** For a function $\mathrm{op} : T \times T \to T$, APPLY$(\mathrm{op}, f, g)$ returns a node $r$ with $f_r(x) = \mathrm{op}(f_f(x), f_g(x))$ for each $x$, and with $\mathrm{lev}(r) \ge \min(\mathrm{lev}(f), \mathrm{lev}(g))$.

*Proof.* By induction on $\mathrm{lev}(f) + \mathrm{lev}(g)$, downward. If both are terminals (line L9), the result is the terminal with the value $\mathrm{op}(\mathrm{val}(f), \mathrm{val}(g))$. A cache entry (line L10) was stored by line L15 for the same key, so it is correct by the induction that holds at the time it was stored. Otherwise, line L11 takes the smaller level $i$. If $f$ is on level $i$, its cofactor by $x_i = v$ is its child $c_v(f)$, since no node below $f$ tests $x_i$. If $f$ is below level $i$, $f$ does not depend on $x_i$ and its cofactor is $f$ itself. The same holds for $g$. The two arguments of each call of line L13 have a larger sum of levels, so by the induction hypothesis the call returns a node for $\mathrm{op}(f_f|_{x_i=v}, f_g|_{x_i=v})$ with a level larger than $i$. A cofactor commutes with a pointwise operator, so this is $(\mathrm{op}(f_f, f_g))|_{x_i=v}$. Lemma 1 then gives a node for the function that agrees with this cofactor on each input with $x_i = v$, for each $v$, which is $\mathrm{op}(f_f, f_g)$. $\square$

**Theorem (canonicity).** If (S) holds, two nodes $u$ and $v$ with $f_u = f_v$ are the same node.

*Proof.* By induction on $m = \min(\mathrm{lev}(u), \mathrm{lev}(v))$, downward from $n + 1$. For $m = n + 1$ both are terminals with the same value, so they are the same node by (c). Let $m \le n$. First, every inner node $w$ on level $m$ has a function that depends on $x_m$. By (a) two of its children differ, they have larger levels, so by the induction hypothesis their functions differ, at some point $y$. These children are the cofactors of $f_w$ by two values $v \ne v'$ of $x_m$, since nothing below $w$ tests $x_m$. Then $f_w$ changes when $x_m$ changes from $v$ to $v'$ at $y$.

Let $\mathrm{lev}(u) = m$ and $f_u = f_v$. Then $f_v$ depends on $x_m$, so $v$ is on level $m$ too, since a node below level $m$ has no test of $x_m$ under it. For each value $a$, the children $c_a(u)$ and $c_a(v)$ are the cofactors of the same function by $x_m = a$, so they have the same function, and by the induction hypothesis they are the same node. So $u$ and $v$ have the same key, and by (c) they are the same node. $\blacksquare$

**Cost of APPLY.** By Lemma 3 and the cache, the body after line L10 runs at most once for each pair $(f', g')$ of a node below $f$ and a node below $g$. So APPLY makes at most $|f| \cdot |g|$ calls of MK, and with $d = \max_i d_i$, it does $O(d \cdot |f| \cdot |g|)$ work in expectation with hashing.
