---
title: The tree-structured CSP algorithm is correct
proves: [correctness, termination]
status: full
---

Fix a binary CSP with variables $0, \ldots, n-1$, domains $D^0_v$, and one relation $R_{uv}$ for each edge of a forest $F$, with $R_{vu}$ its converse. A *solution* is an assignment $s$ with $s_v \in D^0_v$ for all $v$ and $(s_u, s_v) \in R_{uv}$ for each edge. Line L2 gives an order $v_1, \ldots, v_n$ and a parent function such that each tree of $F$ has one root, every other vertex has its parent among its neighbours, the parent comes earlier in the order, and every edge of $F$ joins a vertex and its parent. A breadth-first search from a root in each tree gives this. Let $D_v$ denote the current domains.

**Termination.** Every loop runs over a finite list, and the breadth-first search visits each vertex once. So TREE-CSP and TREE-COUNT stop.

**Lemma 1 (no solution value is lost).** At every point of the upward pass, $s_v \in D_v$ for every solution $s$ and every $v$.

*Proof.* At the start $D_v = D^0_v$. Suppose the claim holds before line L5 handles the edge $(p, v)$. For a solution $s$, $(s_p, s_v) \in R_{pv}$ and $s_v \in D_v$ by the hypothesis, so $s_p$ has a support in $D_v$ and line L5 keeps it. No other domain changes. $\square$

So if line L1 or line L6 returns NONE, some domain is empty, and by Lemma 1 there is no solution.

**Lemma 2 (when $D_v$ is final).** In the upward pass, $D_v$ changes only when line L5 handles an edge $(v, c)$ with $c$ a child of $v$. Each such edge is handled before the edge $(p, v)$ from $v$ to its parent.

*Proof.* Line L5 for the edge $(p, v)$ changes only $D_p$. A child $c$ of $v$ comes after $v$ in the order, so the reversed loop of line L3 reaches $c$, and handles $(v, c)$, before it reaches $v$ and handles $(p, v)$. $\square$

**Lemma 3 (directional arc consistency).** If the upward pass ends without NONE, then for every non-root $v$ with parent $p$, every $a \in D_p$ has some $b \in D_v$ with $(a, b) \in R_{pv}$, for the final domains.

*Proof.* Right after line L5 handles $(p, v)$, every $a \in D_p$ has a support $b$ in the current $D_v$. By Lemma 2, $D_v$ does not change after this point. Later steps can only delete values from $D_p$, which keeps the claim for the values that remain. $\square$

**Theorem 1.** TREE-CSP returns a solution if one exists, and NONE otherwise.

*Proof.* If it returns NONE, there is no solution by Lemma 1. Otherwise all final domains are non-empty, because line L1 checked the start and line L6 checked every change. We show by induction along the order that after the step for $v_i$, the values $x_{v_1}, \ldots, x_{v_i}$ lie in the final domains and satisfy every constraint between two of these variables.

For a root $v_i$, line L8 picks a value of the non-empty $D_{v_i}$. A root has no neighbour earlier in the order: each of its neighbours is its child. So no new constraint is involved. For a non-root $v_i$ with parent $p$, $p$ is earlier and $x_p \in D_p$, so by Lemma 3 line L9 finds some $b \in D_{v_i}$ with $(x_p, b) \in R_{p v_i}$. Any other neighbour of $v_i$ is a child of $v_i$, since every edge joins a vertex and its parent and $v_i$ has one parent; a child comes later. So the edge to $p$ is the only constraint between $v_i$ and earlier variables, and it holds.

After the last step, every edge has both ends assigned, so every constraint holds, and every value lies in $D_v \subseteq D^0_v$. $\square$

**Theorem 2.** TREE-COUNT returns the number of solutions.

*Proof.* For a vertex $v$ let $T_v$ be the set of vertices of its subtree, and let $N_v(a)$ be the number of assignments $t$ of $T_v$ with $t_u \in D^0_u$ for each $u$, $t_v = a$, and $(t_u, t_w) \in R_{uw}$ for each edge inside $T_v$. We prove $W_v(a) = N_v(a)$ for each $a \in D^0_v$, by induction in the order of line L11, which handles each child before its parent.

The edges inside $T_v$ are the edges $(v, c)$ to the children $c$ of $v$ and the edges inside each $T_c$. The sets $T_c$ for different children are disjoint. So an assignment counted by $N_v(a)$ is the same as a choice, for each child $c$, of a value $b \in D^0_c$ with $(a, b) \in R_{vc}$ and an assignment of $T_c$ counted by $N_c(b)$, and these choices are independent. So

$$N_v(a) = \prod_{c} \sum_{b \in D^0_c, (a, b) \in R_{vc}} N_c(b),$$

which is line L11 by the induction hypothesis. For a leaf the product is empty and $N_v(a) = 1$.

The trees of the forest have disjoint vertex sets and no edge between them, so a solution is an independent choice of an assignment for each tree, and the number of solutions is $\prod_r \sum_{a \in D^0_r} N_r(a)$ over the roots $r$, which is line L12. $\blacksquare$
