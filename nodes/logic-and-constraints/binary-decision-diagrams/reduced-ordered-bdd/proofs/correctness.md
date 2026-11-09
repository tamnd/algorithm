---
title: The ROBDD operations are correct and equality is a pointer compare
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order. A terminal has the level $n + 1$, and an inner node $u$ that tests $x_i$ has the level $\mathrm{lev}(u) = i$. The function of a node is $f_0 = 0$, $f_1 = 1$ and $f_u = (\neg x_i \wedge f_{\mathrm{lo}(u)}) \vee (x_i \wedge f_{\mathrm{hi}(u)})$.

**Invariant (S).** For each inner node $u$ of the store: (a) $\mathrm{lo}(u) \ne \mathrm{hi}(u)$; (b) both children have a larger level than $u$; (c) no other node has the same triple; (d) the unique table $U$ maps the triple of $u$ to $u$, and holds no other key.

At the start the store holds only the terminals and $U$ is empty, so (S) holds. Only MK adds nodes.

**Lemma 1 (MK).** Let $l$ and $h$ be nodes with levels larger than $i$. Then MK$(i, l, h)$ keeps (S), and it returns a node $u$ with $\mathrm{lev}(u) \ge i$ and $f_u = (\neg x_i \wedge f_l) \vee (x_i \wedge f_h)$.

*Proof.* If $l = h$, line L1 returns $l$, with $f_l = (\neg x_i \wedge f_l) \vee (x_i \wedge f_l)$ and a level larger than $i$. Otherwise, if $U$ holds the key $(i, l, h)$, line L2 returns the node with this triple, which has the stated function by definition. Otherwise lines L3 and L4 add a node with the triple $(i, l, h)$. It satisfies (a) because $l \ne h$, (b) by the hypothesis, and (c) and (d) because the key was not in $U$ and (d) held before. $\square$

**Lemma 2 (BUILD).** Let $T$ be a truth table of $f \in B_n$, with entry $a$ equal to $f(x)$ for $a = \sum_j x_j 2^{j-1}$. Before the round of line L7 for $i$, and for $0 \le p < 2^i$, the entry $c[p]$ is a node of level larger than $i$ for the cofactor of $f$ by $x_1, \ldots, x_i$ set to the bits of $p$. So BUILD returns a node for $f$.

*Proof.* Before the first round, $i = n$ and $c[p]$ is the terminal $T[p]$, which is $f$ with all variables fixed (line L6). In the round for $i$, line L9 calls MK$(i, c[p], c[p + 2^{i-1}])$ for $p < 2^{i-1}$. The two entries are the cofactors by $x_1, \ldots, x_{i-1}$ set to the bits of $p$, and $x_i = 0$ or $x_i = 1$, and their levels are larger than $i$. By Lemma 1 and the [Shannon expansion](/shannon-expansion/), the new $c[p]$ is a node of level at least $i$ for the cofactor by $x_1, \ldots, x_{i-1}$ alone. This is the invariant for $i - 1$. After the round for $i = 1$, $c[0]$ is a node for $f$ (line L10). $\square$

**Lemma 3 (EVAL).** EVAL$(u, x)$ returns $f_u(x)$ in at most $n$ steps. Each step keeps $f_u(x)$ by the definition of $f_u$, and the level grows at each step.

**Lemma 4 (RESTRICT).** RESTRICT$(f, i, b)$ returns a node for $f|_{x_i=b}$ and calls MK at most once per node reachable from $f$.

*Proof.* We show that $\mathrm{go}(u)$ returns a node $r$ with $f_r = f_u|_{x_i=b}$ and $\mathrm{lev}(r) \ge \mathrm{lev}(u)$, by induction on the level of $u$, from the bottom up. If $\mathrm{lev}(u) > i$ (line L14), no node below $u$ tests $x_i$, so $f_u$ does not depend on $x_i$ and $f_u|_{x_i=b} = f_u$. If $u$ tests $x_i$ (line L15), the children do not depend on $x_i$, so by part 5 of the Shannon expansion, $\mathrm{lo}(u)$ and $\mathrm{hi}(u)$ are the cofactors by $x_i = 0$ and $x_i = 1$. Otherwise $u$ tests some $x_v$ with $v < i$. The cofactor commutes with the Shannon expansion on $x_v$:

$$f_u|_{x_i=b} = (\neg x_v \wedge f_{\mathrm{lo}(u)}|_{x_i=b}) \vee (x_v \wedge f_{\mathrm{hi}(u)}|_{x_i=b}).$$

By the induction hypothesis the two calls of line L17 return nodes for the two inner cofactors, with levels larger than $v$. Lemma 1 then gives a node for the right side, with level at least $v$. Lines L16 and L18 store the result of $u$, so a later call on $u$ returns it without a new MK. $\square$

**Theorem (EQUAL).** If (S) holds, then for any two nodes $u$ and $v$ of the store, $f_u = f_v$ implies $u = v$. So EQUAL$(f, g)$, which compares the ids at line L20, returns true exactly when the functions are equal.

*Proof.* By induction on $m = \min(\mathrm{lev}(u), \mathrm{lev}(v))$, from $m = n + 1$ down to $m = 1$. First we show a claim: an inner node $w$ that tests $x_k$ has a function that depends on $x_k$. Its children have levels larger than $k$, so they do not depend on $x_k$, and they are the cofactors of $f_w$ by $x_k$. They are different nodes by (a), and their levels are larger than $\mathrm{lev}(w)$. If the claim is used inside the induction step for $m = k$, the induction hypothesis applies to the pair of children, so $f_{\mathrm{lo}(w)} \ne f_{\mathrm{hi}(w)}$, and $f_w$ depends on $x_k$.

If $m = n + 1$, both nodes are terminals, and equal functions mean equal labels. Let $m \le n$, and let $u$ have the level $m$. By the claim, $f_u$ depends on $x_m$. If $\mathrm{lev}(v) > m$, then no node below $v$ tests $x_m$ and $f_v$ does not depend on $x_m$, which contradicts $f_u = f_v$. So $v$ also tests $x_m$. Its children are the cofactors of $f_v$, which equal the cofactors of $f_u$, so $f_{\mathrm{lo}(u)} = f_{\mathrm{lo}(v)}$ and $f_{\mathrm{hi}(u)} = f_{\mathrm{hi}(v)}$. These nodes have levels larger than $m$, so the induction hypothesis gives $\mathrm{lo}(u) = \mathrm{lo}(v)$ and $\mathrm{hi}(u) = \mathrm{hi}(v)$. Then $u$ and $v$ have the same triple, and by (c) $u = v$. $\blacksquare$

The page [BDD canonicity](/bdd-canonicity/) proves the same statement for any two reduced ordered BDDs, up to isomorphism, and adds that the reduced diagram is the smallest ordered diagram of its function.
