---
title: The operations of an ordered BDD are correct
proves: [correctness]
status: full
---

Let $\pi = (\pi_1, \ldots, \pi_n)$ be the variable order, from the top level to the bottom level, and let $\mathrm{lev}(u)$ be the position of $\mathrm{var}(u)$ in $\pi$, with $\mathrm{lev}(u) = n + 1$ for a terminal. The function of a node is $f_0 = 0$, $f_1 = 1$ and $f_u = (\neg x_i \wedge f_{\mathrm{lo}(u)}) \vee (x_i \wedge f_{\mathrm{hi}(u)})$ for $i = \mathrm{var}(u)$. The diagram reachable from $r$ is **ordered** when $\mathrm{lev}(c) > \mathrm{lev}(u)$ for each edge from $u$ to $c$.

**Lemma 1 (EVAL).** EVAL$(u, x)$ returns $f_u(x)$. If the diagram is ordered, it makes at most $n$ steps.

*Proof.* Each step of line L2 keeps the value $f_u(x)$, by the definition of $f_u$, and line L3 returns the label of a terminal $t$, which is $f_t(x)$. If the diagram is ordered, the level increases strictly at each step, from at least 1 to at most $n + 1$, so there are at most $n$ steps. $\square$

**Lemma 2 (IS-ORDERED).** IS-ORDERED$(r)$ returns true if and only if the diagram reachable from $r$ is ordered.

*Proof.* Lines L4 and L5 visit each edge out of each reachable inner node. Line L6 returns false exactly when one of these edges does not go to a larger level. A terminal has no edges. $\square$

**Lemma 3 (TREE).** Let $T$ be a truth table of $f \in B_n$. For $0 \le k \le n$ and an assignment $a$ that fixes $\pi_1, \ldots, \pi_k$ and has 0 in the other positions, $\mathrm{go}(k, a)$ returns an ordered node $u$ with $\mathrm{lev}(u) \ge k + 1$ and

$$f_u = f|_{x_{\pi_1} = a_{\pi_1}, \ldots, x_{\pi_k} = a_{\pi_k}}.$$

It makes $2^{n-k} - 1$ new inner nodes.

*Proof.* By downward induction on $k$. For $k = n$, $a$ fixes all variables, and line L8 returns the terminal with the label $T[a] = f(a)$, a constant equal to the full cofactor. It makes no node. For $k < n$, let $i = \pi_{k+1}$ (line L9). By the induction hypothesis, the two calls of line L10 return ordered nodes with level at least $k + 2$, for the cofactors $g_b$ of $f$ by the assignment $a$ extended with $x_i = b$. The new node has level $k + 1$, so its edges go down and it is ordered. Its function is $(\neg x_i \wedge g_0) \vee (x_i \wedge g_1)$, which is the cofactor of $f$ by $a$, by the [Shannon expansion](/shannon-expansion/) of that cofactor on $x_i$. The node count is $1 + 2(2^{n-k-1} - 1) = 2^{n-k} - 1$. With $k = 0$, TREE returns an ordered diagram of $f$ with $2^n - 1$ inner nodes. $\square$

**Lemma 4 (REDUCE).** Let the diagram reachable from $r$ be ordered. For each node $u$ visited by line L11, the node $R[u]$ satisfies:

1. $f_{R[u]} = f_u$;
2. $\mathrm{lev}(R[u]) \ge \mathrm{lev}(u)$, and the diagram reachable from $R[u]$ is ordered;
3. each node reachable from $R[u]$ was made by line L16, or is a terminal. So no such node has two equal children, and no two of them have the same triple.

*Proof.* Line L11 visits the children of $u$ before $u$, so we can use induction on that order. A terminal maps to itself (line L12). For an inner node $u$ with $i = \mathrm{var}(u)$, line L13 sets $l = R[\mathrm{lo}(u)]$ and $h = R[\mathrm{hi}(u)]$. By the induction hypothesis, $f_l = f_{\mathrm{lo}(u)}$ and $f_h = f_{\mathrm{hi}(u)}$, and both have level at least the levels of the old children, so more than $\mathrm{lev}(u)$.

- If $l = h$ (line L14), $R[u] = l$. Then $f_u = (\neg x_i \wedge f_l) \vee (x_i \wedge f_l) = f_l$, and $\mathrm{lev}(l) > \mathrm{lev}(u)$.
- Otherwise $R[u]$ is the node with the triple $(i, l, h)$, found in the table (line L15) or made (line L16). Its function is $(\neg x_i \wedge f_l) \vee (x_i \wedge f_h) = f_u$, its level is $\mathrm{lev}(u)$, and its edges go to $l$ and $h$, which have larger levels. Its children were made by line L16, and the node itself was made by line L16 with $l \ne h$.

The table maps each triple to one node, and line L16 makes a node only for a triple that is not yet in the table, so two nodes made by line L16 have different triples. $\blacksquare$

**Consequence.** REDUCE returns a reduced ordered diagram for $f_r$ in the sense of the [reduction rules](/bdd-reduction-rules/). By the [canonicity theorem](/bdd-canonicity/), this diagram is unique for $f_r$ and $\pi$. All calls of REDUCE share one table. If two calls return isomorphic diagrams, then by induction from the terminals upward, matched nodes have the same triple and therefore the same id in the table. So two calls on ordered diagrams of the same function return the same node id.
