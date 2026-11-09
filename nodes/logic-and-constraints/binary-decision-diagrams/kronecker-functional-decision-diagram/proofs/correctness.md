---
title: For a fixed order and DTL, reduced KFDDs are canonical, and FROM-TABLE, EVALUATE and XOR are correct
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order, and $d = (d_1, \ldots, d_n)$ is the DTL. All sums are over GF(2), written $\oplus$. The basis functions are $b_{\mathrm{S},0} = \bar{x}$, $b_{\mathrm{S},1} = x$, $b_{\mathrm{pD},0} = 1$, $b_{\mathrm{pD},1} = x$, $b_{\mathrm{nD},0} = 1$, $b_{\mathrm{nD},1} = \bar{x}$. The sinks 0 and 1 have the level $n + 1$. An inner node $u = (v, lo, hi)$ has the level $v$, both children have larger levels, and $f_u = b_{d_v, 0}(x_v) f_{lo} \oplus b_{d_v, 1}(x_v) f_{hi}$. By induction from the sinks, $f_u$ depends only on $x_v, \ldots, x_n$. The store is *reduced* if no S node has $lo = hi$, no Davio node has $hi = 0$, and no two inner nodes have the same triple. MK keeps it reduced by lines L1 to L3.

**Lemma 1 (the expansion of one type).** Let $f$ not depend on $x_1, \ldots, x_{v-1}$, let $t$ be a type, let $f_0, f_1$ be the cofactors by $x_v$, and $f_2 = f_0 \oplus f_1$. Then (a) there is exactly one pair $(lo, hi)$ of functions that do not depend on $x_1, \ldots, x_v$ with $f = b_{t,0}(x_v) \, lo \oplus b_{t,1}(x_v) \, hi$, namely $(f_0, f_1)$ for S, $(f_0, f_2)$ for pD and $(f_1, f_2)$ for nD; (b) $f$ depends on $x_v$ if and only if $lo \ne hi$ for S, and if and only if $hi \ne 0$ for pD and nD.

*Proof.* Both sides of the expansion are functions; compare them at $x_v = 0$ and at $x_v = 1$, where $lo$ and $hi$ do not change.

- S: at $x_v = 0$ the right side is $lo$, and at $x_v = 1$ it is $hi$. So the expansion holds if and only if $lo = f_0$ and $hi = f_1$.
- pD: at $x_v = 0$ the right side is $lo$, and at $x_v = 1$ it is $lo \oplus hi$. So $lo = f_0$ and $hi = f_0 \oplus f_1 = f_2$.
- nD: at $x_v = 1$ the right side is $lo$, and at $x_v = 0$ it is $lo \oplus hi$. So $lo = f_1$ and $hi = f_0 \oplus f_1 = f_2$.

In each case the pair is forced, and the given pair satisfies the two equations, so it exists. For (b), $f$ depends on $x_v$ if and only if $f_0 \ne f_1$, which is $f_2 \ne 0$. For S this is $lo \ne hi$, and for pD and nD it is $hi \ne 0$. $\square$

**Lemma 2 (MK).** MK$(v, lo, hi)$, with $lo$ and $hi$ on levels larger than $v$, returns a node of the function $b_{d_v,0}(x_v) f_{lo} \oplus b_{d_v,1}(x_v) f_{hi}$.

*Proof.* In line L1, $lo = hi$ and $\bar{x} f_{lo} \oplus x f_{lo} = f_{lo}$. In line L2, $hi = 0$, so the function is $1 \cdot f_{lo} \oplus 0 = f_{lo}$. In lines L3 and L4, the node has the triple $(v, lo, hi)$ and so the function by definition. $\square$

**Theorem 3 (canonicity).** For a fixed order and DTL, in a reduced store, (a) every inner node depends on the variable of its level, and (b) two distinct nodes compute distinct functions.

*Proof.* By induction on $k$ from $n + 1$ down to 1, for the nodes on the levels $k$ and above. For $k = n + 1$ there are two sinks with distinct functions.

Let $u = (k, lo, hi)$. By Lemma 1(a), $(f_{lo}, f_{hi})$ is the pair of the type $d_k$ for $f_u$. If $d_k = \mathrm{S}$, then $lo \ne hi$, so $f_{lo} \ne f_{hi}$ by (b) for the higher levels. If $d_k$ is a Davio type, then $hi$ is not the sink 0, so $f_{hi} \ne 0$ by (b). In both cases $f_u$ depends on $x_k$ by Lemma 1(b). This is (a).

For (b), let $u \ne w$ with $f_u = f_w$. If both are above level $k$, (b) for those levels gives a contradiction. If $u$ is on level $k$ and $w$ is above it, $f_u$ depends on $x_k$ and $f_w$ does not. If both are on level $k$, they have the same type $d_k$, so Lemma 1(a) gives $f_{lo} = f_{lo'}$ and $f_{hi} = f_{hi'}$. By (b) for the higher levels the children are equal, and the merging rule gives $u = w$. $\square$

So, for a fixed order and DTL, every function has exactly one reduced KFDD, and EQUAL by ids is correct.

**Theorem 4 (FROM-TABLE).** FROM-TABLE$(T)$ returns the node of the function $f$ with $f(x) = T[a]$, where bit $v - 1$ of $a$ is $x_v$.

*Proof.* For an index $a$ write $a_v$ for bit $v - 1$ of $a$. For $t = 0, \ldots, n$, let $T_t$ be the array after line L5 has handled $x_1, \ldots, x_t$. Claim:

$$f(x) = \bigoplus_{a} T_t[a] \prod_{v \le t} b_{d_v, a_v}(x_v) \prod_{v > t} [x_v = a_v].$$

For $t = 0$, the sum has one non-zero product, for $a = x$, which gives $T[x] = f(x)$. For the step from $t - 1$ to $t$, group the indices in pairs $a$, $a' = a + 2^{t-1}$ with $a_t = 0$. The pair contributes $P \cdot (\bar{x}_t T_{t-1}[a] \oplus x_t T_{t-1}[a'])$, where $P$ is the common product over the other variables, since $[x_t = 0] = \bar{x}_t$ and $[x_t = 1] = x_t$. By Lemma 1(a) applied to the function of one variable $\bar{x}_t T_{t-1}[a] \oplus x_t T_{t-1}[a']$, with the cofactors $T_{t-1}[a]$ and $T_{t-1}[a']$, it equals $b_{d_t,0}(x_t) \, lo \oplus b_{d_t,1}(x_t) \, hi$, where $(lo, hi)$ is the pair of the type $d_t$. Line L5 stores exactly $(lo, hi)$ in $(T[a], T[a'])$, so the claim holds for $t$. The pass for $x_t$ reads only the pair it writes, so the passes do not interfere.

For $t = n$, $f = \bigoplus_a T_n[a] \prod_v b_{d_v, a_v}(x_v)$. Now the loop of lines L6 and L7. Claim: after the round for $v$, entry $a < 2^{v-1}$ of the layer is the node of

$$g_{v, a} = \bigoplus_{c} T_n[a + c] \prod_{w \ge v} b_{d_w, (a + c)_w}(x_w),$$

where $c$ runs over the multiples of $2^{v-1}$ below $2^n$. Before the first round ($v = n + 1$) the entry $a$ is the sink $T_n[a]$, which is the claim. In the round for $v$, the new entry $a$ is MK$(v, \text{old } a, \text{old } a + 2^{v-1})$, so by Lemma 2 its function is $b_{d_v,0}(x_v) \, g_{v+1, a} \oplus b_{d_v,1}(x_v) \, g_{v+1, a + 2^{v-1}}$. The two terms are the parts of $g_{v, a}$ with bit $v - 1$ of $a + c$ equal to 0 and to 1. The children are functions of $x_{v+1}, \ldots, x_n$, so by Theorem 3 they are on later levels, as Lemma 2 needs. After the round for $v = 1$, entry 0 is the node of $f$. $\square$

**Theorem 5 (EVALUATE).** Line L8 computes $\mathrm{val}[w] = f_w(x)$ for every node $w$ reachable from $u$, in $O(\lvert u \rvert)$ time.

*Proof.* The nodes are taken children first, and the sinks have their values. For an inner node $w = (v, lo, hi)$, the three cases of line L8 are $b_{d_v,0}(x_v) \mathrm{val}[lo] \oplus b_{d_v,1}(x_v) \mathrm{val}[hi]$ for the three types: for S this is $\mathrm{val}[lo]$ if $x_v = 0$ and $\mathrm{val}[hi]$ if $x_v = 1$. By induction this is $f_w(x)$. Each node is handled once. $\square$

**Theorem 6 (XOR).** XOR$(f, g)$ returns the node of $f_f \oplus f_g$, with at most $\lvert f \rvert \cdot \lvert g \rvert$ calls that reach the recursive case.

*Proof.* Let $\mathrm{parts}(u, v)$ be the children of $u$ if $u$ is on level $v$, and $(u, u)$ for $d_v = \mathrm{S}$ or $(u, 0)$ for a Davio type if $u$ is on a later level. In every case $f_u = b_{d_v,0} f_{lo} \oplus b_{d_v,1} f_{hi}$ for $(lo, hi) = \mathrm{parts}(u, v)$, and both parts are on later levels: for S, $\bar{x} f_u \oplus x f_u = f_u$, and for Davio types $f_u \oplus b \cdot 0 = f_u$. The base cases are correct: two sinks give their XOR, $0 \oplus g = g$, and $f \oplus f = 0$. In the recursive case, with $v$ the smaller level,

$$f_f \oplus f_g = b_{d_v,0} (f_{f_{lo}} \oplus f_{g_{lo}}) \oplus b_{d_v,1} (f_{f_{hi}} \oplus f_{g_{hi}}),$$

by the distributive law over GF(2). The two recursive calls return the nodes of the two sums by induction on the sum of the levels of the arguments, these are on levels larger than $v$, and Lemma 2 gives the node of $f_f \oplus f_g$. The arguments of every call are a node reachable from $f$ or the sink 0, and a node reachable from $g$ or the sink 0; the cases with the sink 0 end at once, and the cache, keyed by the unordered pair, lets each pair of reachable nodes reach the recursive case at most once. $\blacksquare$
