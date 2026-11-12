---
title: Fitch's algorithm returns a most parsimonious labeling
proves: [correctness]
status: full
---

Let $T$ be a rooted binary tree with leaf states $x$. For a node $w$, write $T_w$ for the subtree of $w$, and $[P]$ for 1 if $P$ holds and 0 if not. For a state $a$, let $c_w(a)$ be the least number of changes on the edges of $T_w$ over all labelings of $T_w$ that agree with $x$ at the leaves and give $w$ the state $a$. Put $c_w(a) = \infty$ if no such labeling exists, which happens only at a leaf with $a \ne x(w)$. Let $s_w = \min_a c_w(a)$, and let

$$g_w(a) = \min_b \bigl(c_w(b) + [a \ne b]\bigr),$$

the least number of changes on $T_w$ and on the edge above $w$, when the parent of $w$ has state $a$.

**Recurrence.** For an internal node $v$ with children $l$ and $r$, the edges of $T_v$ are the two edges to $l$ and $r$ and the edges of $T_l$ and $T_r$. Once $v$ has state $a$, the labelings of $T_l$ and $T_r$ can be chosen independently. So

$$c_v(a) = g_l(a) + g_r(a). \tag{1}$$

**Lemma 1.** After the first pass, for every node $w$: (a) $S_w = \{a : c_w(a) = s_w\}$; (b) $g_w(a) = s_w + [a \notin S_w]$ for every state $a$; (c) the number of executions of line L6 at nodes of $T_w$ is $s_w$.

*Proof.* By induction in the postorder of line L2.

*Leaf.* Here $c_w(x(w)) = 0$ and $c_w(a) = \infty$ for every other $a$, so $s_w = 0$ and line L3 gives $S_w = \{x(w)\}$, which is (a). For (b), $g_w(a) = [a \ne x(w)] = 0 + [a \notin S_w]$. For (c), a leaf runs line L6 zero times.

*Internal node.* Let $v$ have children $l$ and $r$, for which the lemma holds. By (1) and (b) for $l$ and $r$,

$$c_v(a) = s_l + s_r + [a \notin S_l] + [a \notin S_r]. \tag{2}$$

Case 1: $S_l \cap S_r \ne \emptyset$. A state in the intersection has $c_v(a) = s_l + s_r$, and every other state has $c_v(a) \ge s_l + s_r + 1$. So $s_v = s_l + s_r$ and $\{a : c_v(a) = s_v\} = S_l \cap S_r$, which is the set of line L5. This is (a). Line L6 does not run at $v$, so the count in $T_v$ is $s_l + s_r = s_v$, which is (c).

Case 2: $S_l \cap S_r = \emptyset$. Every state is outside at least one of the two sets, so $c_v(a) \ge s_l + s_r + 1$, with equality exactly for the states in $S_l \cup S_r$. So $s_v = s_l + s_r + 1$, and the set of line L6 is $\{a : c_v(a) = s_v\}$, which is (a). Line L6 runs once at $v$, so the count in $T_v$ is $s_l + s_r + 1 = s_v$, which is (c).

In both cases, (b) for $v$ follows from (a). If $a \in S_v$, then $c_v(a) = s_v$, so $g_v(a) \le c_v(a) + 0 = s_v$, and $g_v(a) \ge \min_b c_v(b) = s_v$. If $a \notin S_v$, then $c_v(a) \ge s_v + 1$ (in Case 1 by the bound above, in Case 2 because the states outside the union have $c_v(a) = s_l + s_r + 2$). So $c_v(a) + 0 \ge s_v + 1$, and $c_v(b) + 1 \ge s_v + 1$ for every $b \ne a$, with equality for any $b \in S_v$. So $g_v(a) = s_v + 1$. $\square$

**Lemma 2 (the score).** The value returned at line L11 is the parsimony score $s_{\text{root}}$.

*Proof.* By Lemma 1 (c) at the root. $\square$

**Lemma 3 (the labeling).** The second pass gives each node $w$ a state $\lambda(w) \in S_w$, gives each leaf its own state, and the labeling has exactly $s_{\text{root}}$ changes.

*Proof.* Line L7 picks $\lambda(\text{root}) \in S_{\text{root}}$. For a child $w$ of $v$, lines L9 and L10 pick a state of $S_w$. At a leaf $S_w = \{x(w)\}$, so $\lambda(w) = x(w)$. Hence $\lambda$ is a labeling of $T$.

Let $d_w$ be the number of changes of $\lambda$ on the edges of $T_w$. We show $d_w = s_w$ for every node, by induction from the leaves up. At a leaf, $d_w = 0 = s_w$. Let $v$ have children $l$ and $r$, and let $a = \lambda(v) \in S_v$. For a child $w \in \{l, r\}$, the edge $v \to w$ has a change if and only if $\lambda(w) \ne a$. Line L9 keeps $a$ when $a \in S_w$, and line L10 picks another state only when $a \notin S_w$. So the change count on that edge is $[a \notin S_w]$. With the induction hypothesis $d_w = s_w$, this gives

$$d_v = \sum_{w \in \{l, r\}} \bigl(s_w + [a \notin S_w]\bigr) = c_v(a)$$

by (2). Since $a \in S_v$, Lemma 1 (a) gives $c_v(a) = s_v$. So $d_v = s_v$, and at the root the labeling has $s_{\text{root}}$ changes. $\square$

**Theorem.** Fitch's algorithm returns the least number of changes over all labelings of $T$ that agree with $x$ at the leaves, and a labeling that reaches it. Moreover, $S_{\text{root}}$ is the set of states that the root has in at least one optimal labeling.

*Proof.* The least number of changes is $\min_a c_{\text{root}}(a) = s_{\text{root}}$. Lemma 2 shows that the score is this value, and Lemma 3 shows that $\lambda$ is a labeling with that many changes. The last claim is Lemma 1 (a) at the root. $\blacksquare$

**Remark.** Lemma 1 (a) speaks of the subtree only. A state $a \in S_w$ is optimal for $T_w$ alone, but it need not be in an optimal labeling of the whole tree, and a state outside $S_w$ can be. The example of the page has both cases. This is why the sets of the first pass are not the ancestral states, except at the root.
