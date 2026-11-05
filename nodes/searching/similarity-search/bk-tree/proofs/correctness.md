---
title: The BK-tree keeps its invariant and answers range and nearest queries exactly
proves: [correctness]
status: full
---

Let $(M, \delta)$ be a metric space with $\delta(x, y) \in \{0, 1, 2, \dots\}$. So $\delta(x, y) = 0$ if and only if $x = y$, $\delta$ is symmetric, and $\delta(x, z) \le \delta(x, y) + \delta(y, z)$.

**Invariant (B).** For each node $t$ and each key $i$ of $t.child$, every item $x$ in the subtree of $t.child[i]$ has $\delta(x, t.item) = i$.

**Lemma 1.** INSERT keeps (B) and stores no item twice.

*Proof.* Let $t_0, t_1, \dots, t_m$ be the nodes visited, with $t_0$ the root. For $j < m$, INSERT moves from $t_j$ to $t_{j+1} = t_j.child[k_j]$ with $k_j = \delta(x, t_j.item)$, and at $t_m$ it either returns at line L4 or adds $x$ as $t_m.child[k_m]$. In the second case, $x$ lies in the subtree of key $k_j$ of each $t_j$ and has distance $k_j$ to $t_j.item$, so (B) holds for $x$ at every ancestor. No other node gains or loses an item. If an equal item is stored, it lies on the path of $x$: by induction, if $y = x$ is in the subtree of $t_j$, then $\delta(y, t_j.item) = \delta(x, t_j.item) = k_j$, so $y$ is $t_j.item$ or lies in the subtree of $t_j.child[k_j] = t_{j+1}$. So INSERT reaches the node of $y$ and returns at line L4. $\square$

**Lemma 2.** If $x$ is in the subtree of $t.child[i]$, then $\delta(q, x) \ge |\delta(q, t.item) - i|$ for every $q$.

*Proof.* By (B), $\delta(x, t.item) = i$. The triangle inequality gives $\delta(q, t.item) \le \delta(q, x) + i$ and $i = \delta(x, t.item) \le \delta(x, q) + \delta(q, t.item)$. With symmetry, these two inequalities say $\delta(q, x) \ge |\delta(q, t.item) - i|$. $\square$

**Theorem 1.** RANGE$(t, q, r)$ reports exactly the items $x$ in the subtree of $t$ with $\delta(q, x) \le r$, each once.

*Proof.* By induction on the height of $t$. For $t = $ nil there is nothing to report. Otherwise, line L7 reports $t.item$ if and only if $k = \delta(q, t.item) \le r$. Every other item $x$ of the subtree lies in exactly one child subtree, say of key $i$. If $\delta(q, x) \le r$, Lemma 2 gives $|k - i| \le r$, so line L8 calls RANGE on that child, and by induction the call reports $x$ once. If the child is not called, no item in it is within $r$. Items of called children with $\delta(q, x) > r$ are not reported, by induction. $\square$

**Theorem 2.** NEAREST$(T, q)$ returns $\tau = \min_{x \in S} \delta(q, x)$ and an item $best$ with $\delta(q, best) = \tau$, if $S$ is not empty.

*Proof.* We show that the loop keeps the following invariant (N): for each stack entry $(b, u)$, every item of the subtree of $u$ is at distance at least $b$ from $q$; and every item of $S$ is in the subtree of a stack entry, or has been evaluated at line L11, or is at distance at least $\tau$ from $q$.

At the start, the stack holds $(0, root)$, and (N) holds. Pop $(b, t)$. If $b \ge \tau$, every item of the subtree of $t$ is at distance at least $b \ge \tau$, so dropping the entry keeps (N). Otherwise line L11 evaluates $t.item$, and lowers $\tau$ only to the distance of an evaluated item; items earlier covered by "at least $\tau$" remain at least the new, smaller $\tau$. Each child of key $i$ is pushed with bound $|i - k|$, which is a lower bound for its subtree by Lemma 2. A child with $|i - k| \ge \tau$ is not pushed, and all of its items are at distance at least $\tau$ by Lemma 2. So (N) holds after the step.

Each node is pushed at most once, since it is pushed only by its parent when the parent is evaluated, so the loop ends. Then the stack is empty, and by (N) every item is evaluated or at distance at least $\tau$. Since $\tau$ is the least distance among evaluated items and $best$ is an item with that distance, $\tau$ is the minimum over $S$. $\blacksquare$
