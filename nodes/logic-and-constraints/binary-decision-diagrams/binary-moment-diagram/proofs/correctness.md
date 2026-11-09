---
title: Reduced BMDs are canonical, the operations are correct, and the BMD of X times Y has w^2 + 3w nodes
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order. A sink $(n + 1, k)$ has the level $n + 1$ and the function $f \equiv k$. An inner node $u = (v, c, l)$ has the level $v$, both children have larger levels, and $f_u = f_c + x_v \cdot f_l$. By induction from the sinks, $f_u$ depends only on $x_v, \ldots, x_n$, where $v$ is the level of $u$. The store is *reduced* if no inner node has $l$ equal to the sink 0, no two sinks hold the same integer, and no two inner nodes have the same triple. MK keeps it reduced by lines L1 and L2, and CONST by its own lookup.

**Lemma 1 (moments).** Let $f$ not depend on $x_1, \ldots, x_{v-1}$. Put $f_0 = f|_{x_v = 0}$ and $m = f|_{x_v = 1} - f|_{x_v = 0}$. Then (a) $f_0$ and $m$ do not depend on $x_1, \ldots, x_v$, and $f = f_0 + x_v m$; (b) if $f = c + x_v l$ with $c$ and $l$ not depending on $x_1, \ldots, x_v$, then $c = f_0$ and $l = m$; (c) $f$ depends on $x_v$ if and only if $m \ne 0$.

*Proof.* (a) A restriction to $x_v = b$ does not depend on $x_v$, and the others are not present in $f$. For $x_v = 0$ the right side is $f_0 = f|_{x_v = 0}$, and for $x_v = 1$ it is $f|_{x_v = 1}$. (b) Set $x_v = 0$ to get $c = f_0$, and $x_v = 1$ to get $c + l = f|_{x_v = 1}$. (c) $f$ depends on $x_v$ if and only if the two restrictions differ, which is $m \ne 0$. $\square$

**Theorem 2 (canonicity).** In a reduced store, (a) every inner node $u$ depends on the variable of its level, and (b) two distinct nodes compute distinct functions.

*Proof.* By induction on $k$ from $n + 1$ down to 1, for the nodes on levels $k$ and above. For $k = n + 1$ the nodes are sinks with distinct integers, so (b) holds and (a) is empty.

Let $u = (k, c, l)$ with $k \le n$. By Lemma 1(b), $f_l$ is the linear moment of $f_u$ by $x_k$. The node $l$ is on a level above $k$ and is not the sink 0, so by (b) for those levels $f_l$ is not the constant 0. By Lemma 1(c), $f_u$ depends on $x_k$. This is (a).

For (b), let $u \ne w$ be nodes on levels $k$ and above with $f_u = f_w$. If both are above level $k$, (b) for those levels gives a contradiction. If $u$ is on level $k$ and $w$ above it, then $f_u$ depends on $x_k$ by (a) and $f_w$ does not, a contradiction. If $u = (k, c, l)$ and $w = (k, c', l')$, then Lemma 1(b) gives $f_c = f_{c'}$ and $f_l = f_{l'}$, so $c = c'$ and $l = l'$ by (b) for the higher levels, and the merging rule gives $u = w$. $\square$

So EQUAL by ids is correct. Also, the node MK$(v, c, l)$ has the function $f_c + x_v f_l$ in both cases of line L1: if $l$ is the sink 0, this function is $f_c$.

**Lemma 3 (mom).** If $v$ is at most the level of $u$ and $\mathrm{mom}(u, v) = (c, l)$, then $f_u = f_c + x_v f_l$ and both $c$ and $l$ are on levels larger than $v$.

*Proof.* If $u$ is on level $v$, this is the definition. Otherwise $u$ is on a later level, $\mathrm{mom}$ returns $(u, 0)$, and $f_u = f_u + x_v \cdot 0$. $\square$

**Theorem 4 (ADD).** ADD$(f, g)$ returns the node of $f_f + f_g$, and at most $\lvert f \rvert \cdot \lvert g \rvert$ calls reach line L8.

*Proof.* By induction on the sum of the levels of the arguments, which grows in each recursive call, by Lemma 3. Line L7 is correct for two sinks, and the cache returns only results of earlier calls with the same arguments, in either order, which is correct since addition commutes. At line L8, Lemma 3 gives $f_f + f_g = (f_a + f_c) + x_v (f_b + f_d)$. The recursive calls return the nodes of $f_a + f_c$ and $f_b + f_d$ by induction. These sums do not depend on $x_1, \ldots, x_v$, since their terms do not, so by canonicity the returned nodes are on levels larger than $v$. Then MK returns the node of the sum. Every pair of arguments is a pair of nodes reachable from $f$ and from $g$, since mom returns the node or its children, and the cache lets each pair reach line L8 at most once. $\square$

**Theorem 5 (MUL).** MUL$(f, g)$ returns the node of $f_f \cdot f_g$.

*Proof.* By the same induction. For two sinks, line L9 is correct. Otherwise, by Lemma 3, $f_f = a + x_v b$ and $f_g = c + x_v d$, writing the functions of the nodes by their names. Since $x_v \in \{0, 1\}$, $x_v^2 = x_v$, so

$$f_f f_g = ac + x_v (ad + bc + bd).$$

The calls of lines L10 and L11 compute $ad$, $bc$, $bd$ and $ac$ by induction, and ADD sums them by Theorem 4. The functions $ac$ and $ad + bc + bd$ do not depend on $x_1, \ldots, x_v$, so their nodes are on later levels, and MK of line L11 returns the node of the product. $\square$

**Theorem 6 (FROM-TABLE).** FROM-TABLE$(T)$ returns the node of the function $f$ with $f(x) = T[a]$, where bit $i - 1$ of $a$ is $x_i$.

*Proof.* Write $a \subseteq b$ if the set bits of $a$ are among those of $b$. First the transform. Claim: after the passes for the bits $0, \ldots, t - 1$, the array holds $C_t[a] = \sum (-1)^{\lvert a \setminus b \rvert} T[b]$ over the $b \subseteq a$ that agree with $a$ on the bits $t, \ldots, n - 1$. For $t = 0$ the only such $b$ is $a$. The pass for bit $t$ sets $C_{t+1}[a] = C_t[a] - C_t[a \oplus 2^t]$ if bit $t$ of $a$ is 1, and leaves $C_t[a]$ otherwise; it reads $C_t[a \oplus 2^t]$ before that entry changes, since that entry has bit $t$ equal to 0. In the first case the $b$ for $C_{t+1}[a]$ split by bit $t$: those with bit $t$ set give $C_t[a]$, and those without it give $C_t[a \oplus 2^t]$ with one more element in $a \setminus b$, so with the sign changed. In the second case nothing changes. After all $n$ passes, $C[a] = \sum_{b \subseteq a} (-1)^{\lvert a \setminus b \rvert} T[b]$, which is the coefficient $C_f(S)$ of the multilinear form, for $S$ the set of $a$. The form is correct by the inverse formula $f(\mathbf{1}_T) = \sum_{S \subseteq T} C_f(S)$, which is the standard inversion of sums over subsets.

Next the loop of lines L4 and L5. For a set $S$ write $\beta(S) = \sum_{i \in S} 2^{i-1}$ and $x^S = \prod_{i \in S} x_i$. Claim: after the round for $v$, the layer has $2^{v-1}$ entries, and entry $a$ is the node of

$$g_{v, a} = \sum_{S \subseteq \{v, \ldots, n\}} C[a + \beta(S)] \, x^S.$$

Before the first round ($v = n + 1$), entry $a$ is the sink $C[a]$, and the sum has only $S = \emptyset$. In the round for $v$, the new entry $a < 2^{v-1}$ is MK$(v, \text{old } a, \text{old } a + 2^{v-1})$, whose function is $g_{v+1, a} + x_v \, g_{v+1, a + 2^{v-1}}$. The first term is the part of $g_{v, a}$ with $v \notin S$, and the second is the part with $v \in S$, since $a + 2^{v-1} + \beta(S') = a + \beta(S' \cup \{v\})$. Both are functions of $x_{v+1}, \ldots, x_n$, so their nodes are on later levels, as MK needs. After the round for $v = 1$, entry 0 is the node of $\sum_S C_f(S) x^S = f$. $\square$

**Lemma 7 (EVALUATE).** Line L6 computes $\mathrm{val}[w] = f_w(x)$ for each node $w$ reachable from $u$.

*Proof.* The nodes are taken children first. For a sink this is its integer. For $w = (v, c, l)$, $f_w(x) = f_c(x) + x_v f_l(x) = \mathrm{val}[c] + x_v \mathrm{val}[l]$ by induction. Each node is visited once, so the time is $O(\lvert u \rvert)$. $\square$

**Theorem 8 (sizes of words and products).** Let $X = \sum_{i=1}^w 2^{i-1} x_i$ and $Y = \sum_{j=1}^w 2^{j-1} y_j$, where $y_j = x_{w+j}$ and $n = 2w$. Then the BMD of $X$ has $2w + 1$ nodes, and the BMD of $X \cdot Y$ has $w^2 + 3w$ nodes.

*Proof.* By Theorem 2 it is enough to give a reduced set of nodes, all reachable from a root with the right function: the BMD is then this set.

For $X$: let $V_{w+1}$ be the sink 0 and $V_i = (x_i, V_{i+1}, 2^{i-1})$ for $i = w$ down to 1. Then $f_{V_i} = \sum_{i' \ge i} 2^{i'-1} x_{i'}$ by induction, and $V_1$ is $X$. The linear moments are the sinks $2^{i-1} \ne 0$, and the nodes are on distinct levels, so the set is reduced. It has $w$ inner nodes and the $w + 1$ sinks $0, 1, 2, \ldots, 2^{w-1}$, so $2w + 1$ nodes.

For $X \cdot Y$: for $1 \le i, j \le w$ let $W(i, w + 1)$ be the sink 0 and $W(i, j) = (y_j, W(i, j + 1), 2^{i + j - 2})$. By induction, $f_{W(i, j)} = 2^{i-1} \sum_{j' \ge j} 2^{j' - 1} y_{j'}$, so $W(i, 1)$ is the node of $2^{i-1} Y$. Let $R_{w+1}$ be the sink 0 and $R_i = (x_i, R_{i+1}, W(i, 1))$. By induction, $f_{R_i} = \sum_{i' \ge i} 2^{i'-1} x_{i'} \, Y$, so $R_1$ is the node of $X \cdot Y$.

The set is reduced. The linear moments are the sinks $2^{i+j-2} \ne 0$ and the nodes $W(i, 1)$, whose functions $2^{i-1} Y$ are not 0. The $R_i$ are on distinct levels. For a fixed $j$, the nodes $W(1, j), \ldots, W(w, j)$ are on the same level and have the distinct linear moments $2^{j-1}, \ldots, 2^{w + j - 2}$. Nodes on different levels are distinct. All nodes are reachable from $R_1$.

Count: $w$ nodes $R_i$, $w^2$ nodes $W(i, j)$, the sinks $2^k$ for $k = i + j - 2 \in \{0, \ldots, 2w - 2\}$, which are $2w - 1$ sinks, and the sink 0. The total is $w + w^2 + 2w - 1 + 1 = w^2 + 3w$. $\blacksquare$
