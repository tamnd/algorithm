---
title: SCOUT returns the negamax value, and TEST decides the two inequalities
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page: SCOUT in lines L1 to L6 and TEST in lines L7 to L10. Let $N(n)$ be the [negamax](/negamax/) value of node $n$ for the side to move, with the search to a fixed depth, so a node at the depth limit counts as terminal. For an inner node, $N(n) = \max_c (-N(c))$ over the children $c$ of $n$. The tree is finite, so every recursion stops: each call is on a child, one level down.

**Lemma 1 (TEST).** For every node $n$ and every value $v$, TEST$(n, v, >)$ returns true iff $N(n) > v$, and TEST$(n, v, \ge)$ returns true iff $N(n) \ge v$.

*Proof.* By induction on the height of $n$. If $n$ is terminal, line L7 compares EVALUATE$(n) = N(n)$ with $v$ directly.

Let $n$ be an inner node and let the claim hold for its children. Take the relation $>$ first. Then
$$ N(n) > v \iff \exists c:\ -N(c) > v \iff \exists c:\ N(c) < -v \iff \exists c:\ \lnot\,(N(c) \ge -v). $$
Line L9 calls TEST$(c, -v, \ge)$ on the children in order, which by induction returns true iff $N(c) \ge -v$, and returns true at the first child for which this is false. If there is no such child, line L10 returns false. So the result is true iff some child has $\lnot(N(c) \ge -v)$, which is iff $N(n) > v$.

For the relation $\ge$ the same steps give
$$ N(n) \ge v \iff \exists c:\ -N(c) \ge v \iff \exists c:\ N(c) \le -v \iff \exists c:\ \lnot\,(N(c) > -v), $$
and line L9 calls TEST$(c, -v, >)$, the other relation. $\square$

**Theorem.** SCOUT$(n)$ returns $N(n)$.

*Proof.* By induction on the height of $n$. A terminal node returns EVALUATE$(n) = N(n)$ at line L1.

Let $n$ be an inner node with the children $c_1, \ldots, c_k$ in order, and let the claim hold for the children. Let $W_j = \max_{i \le j} (-N(c_i))$ be the best score of the first $j$ children. We show that after child $c_j$ is handled, $v = W_j$.

For $j = 1$, line L2 sets $v = -\text{SCOUT}(c_1) = -N(c_1) = W_1$ by induction.

For $j > 1$, let $v = W_{j-1}$ before line L4. By Lemma 1, TEST$(c_j, -v, \ge)$ is false iff $N(c_j) < -v$, that is iff $-N(c_j) > v$.
- If it is false, child $c_j$ is strictly better, so $W_j = -N(c_j)$. Line L5 sets $v = -\text{SCOUT}(c_j) = -N(c_j)$ by induction, which is $W_j$.
- If it is true, then $-N(c_j) \le v$, so $W_j = W_{j-1} = v$, and $v$ does not change.

After the last child, $v = W_k = \max_c(-N(c)) = N(n)$, and line L6 returns it. $\blacksquare$

**Remark on the choice of relations.** At line L4 the test is with $\ge$, so a child whose value ties the best so far is not searched again. A test with $>$ would also give the right value, but it would search such a child for its value for nothing. In Pearl's description in the MAX and MIN view, a MAX node tests a later child for $V(S_k) > v$, and a MIN node exempts a child when $V(S_k) \ge v$; this is the same rule.

**Remark on the cost of a node.** Lemma 1 also shows why TEST prunes more than alpha-beta with the same bound: a node that has to prove "$N(n) > v$" stops at the first child that proves it, even if a later child is better. The price is that a child that the test shows to be better is searched a second time, by SCOUT, for its value.
