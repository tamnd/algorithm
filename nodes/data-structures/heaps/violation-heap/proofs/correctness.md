---
title: The violation heap operations keep heap order, the rank rule and the size bound
proves: [correctness]
status: full
---

We use the definitions of the page. A child is active if it is one of the last two children of its parent. A missing child has rank $-1$, and for a node $z$ with active children $z_1, z_2$, $\rho(z) = \lceil (r(z_1) + r(z_2))/2 \rceil + 1$. The invariants are (1) heap order: every key is at least the key of its parent; (2) the rank rule: $0 \le r(z) \le \rho(z)$ for every node $z$.

**Lemma 1 (the pointers).** If the sibling lists are as in the representation, then for an active node $x$ the procedure of lines L11 and L16 returns the parent of $x$, and for a node that is not active it returns NIL.

*Proof.* Let $y = x.right$. If $x$ is the last child of $p$, then $y = p$ and $p.last = x$. If $x$ is the second child from the end, $y$ is the last child, so $y.right = p$ and $p.last = y$. If $x$ is an older child, $y$ and $y.right$ are siblings of $x$, and neither is the last child of the other, since a last child is in the subtree of its parent and siblings are not. For a root, $y = $ NIL. $\square$

**Lemma 2 (heap order).** Every operation keeps (1), and $H.min$ holds a smallest key.

*Proof.* Insert and meld add roots. In JOIN3, line L1 puts the root of smallest key on top, and the two others become its children, so their keys are at least its key; nothing else changes. In delete-min, the children of $z$ become roots, which removes the parent relation and so cannot break (1). In decrease-key, the new key of a root has no parent to compare with. If line L11 returns, $x$ is active and its new key is at least the key of its parent, and the children of $x$ had keys at least the old key of $x$, which is at least the new key. Otherwise $x$ becomes a root, which keeps (1) for $x$ and its children. The node $z_1$, a child of $x$, has a key at least the old key of $x$, which was at least the key of the old parent of $x$; so $z_1$ in the place of $x$ keeps (1). By (1), the root of each tree holds the smallest key of the tree, and every operation sets $H.min$ to a smallest root, either by a comparison with the new root or by a scan of all roots. $\square$

**Lemma 3 (the rank rule).** Every operation keeps (2).

*Proof.* First, $\rho(z) \ge \lceil (-1 - 1)/2 \rceil + 1 = 0$ for every node, and every rank that the code sets is $0$, $\rho$ of a node, or one more than an old rank. So all ranks stay $\ge 0$.

$\rho(z)$ depends only on the active children of $z$ and their ranks. We list the events that change these, and for each we show that (2) holds for $z$ at the end.

- *A join on $z$ (line L3).* Before it, $r(z) = r(z_1) = r(z_2) = k$. After it, $z_1$ and $z_2$ are the active children of $z$, so $\rho(z) = \lceil 2k/2 \rceil + 1 = k + 1 = r(z)$. Line L2 changes the order of two children that are no longer active after line L3, so it does not matter for $\rho$.
- *The children of $z$ change at line L13.* There are two cases. If $z = x$, line L14 sets $r(x) = \rho(x)$ after the change. If $z$ is the parent of $x$ and $x$ was not active, the last two children of $z$ do not change: $x$ was older than both of them, and its place either gets $z_1$ or goes away. If $z$ is the parent of $x$ and $x$ was active, then $p = z$ at line L11, and the loop of line L15 first looks at $z$.
- *The rank of an active child $c$ of $z$ goes down.* Ranks go down only at line L16 (at line L14, the node is a root). Line L16 lowers $r(p)$ and, if $p$ is active, sets $p$ to its parent, which by Lemma 1 is $z$. So the loop looks at $z$ next.
- *The rank of $z$ goes up.* This happens only in a join, which is the first case, and at line L14, where it is set equal to $\rho(x)$.

When the loop of lines L15 and L16 looks at a node $p$, it either finds $\rho(p) \ge r(p)$, so (2) holds at $p$ and $r(p)$ did not change, so no parent sees a change; or it sets $r(p) = \rho(p) \ge 0$, so (2) holds at $p$, and the change of $r(p)$ is an event for the parent of $p$, which is looked at next if $p$ is active and does not matter if $p$ is not active. The loop goes up one level each time, so it ends. In delete-min and insert no non-root changes its active children, and a node that becomes a root keeps its children. So when an operation ends, every node obeys (2). $\square$

**Lemma 4 (the paper's Lemma 3).** Let $z$ obey (2), and let its active children have ranks $a \ge b$, with $-1$ for a missing child. Then $a \ge r(z)$, or $a = r(z) - 1$ and $b \ge r(z) - 2$.

*Proof.* Since $b \le a$, $r(z) \le \lceil (a + b)/2 \rceil + 1 \le a + 1$. If $a = r(z) - 1$, then $r(z) - 1 \le \lceil (r(z) - 1 + b)/2 \rceil$, which needs $(r(z) - 1 + b)/2 > r(z) - 2$, that is $b > r(z) - 3$. $\square$

**Theorem (size bound).** If every node obeys (2), the subtree of a node of rank $r$ has at least $F_{r+2}$ nodes, where $F_1 = F_2 = 1$ and $F_{i+2} = F_{i+1} + F_i$. So no rank is more than $\log_\varphi n$, with $\varphi = (1 + \sqrt 5)/2$.

*Proof.* By induction on the height of the subtree. Let $z$ have rank $r$ and active children of ranks $a \ge b$. If $r = 0$, the subtree has $1 = F_2$ node. Let $r \ge 1$. By Lemma 4, $a \ge r - 1 \ge 0$, so $z$ has an active child of rank $a$. If $a \ge r$, that child alone has at least $F_{a+2} \ge F_{r+2}$ nodes by induction, so $z$ has more. Otherwise $a = r - 1$ and $b \ge r - 2$. If $b \ge 0$, the two children give at least $1 + F_{r+1} + F_{r} > F_{r+2}$ nodes. If $b = -1$, then $r - 2 \le -1$, so $r = 1$ and $a = 0$, and $z$ with its child gives at least $2 = F_3$ nodes. In every case the bound holds. Since $F_{r+2} \ge \varphi^{r}$, a heap of $n$ nodes has no rank above $\log_\varphi n$. $\square$

**Theorem (the operations are correct).** Find-min returns a smallest key, delete-min removes and returns a smallest key, and the other operations keep the multiset of keys as the abstract type says.

*Proof.* By Lemma 2, $H.min$ is a root with a smallest key, which find-min returns. Delete-min removes exactly the node $z = H.min$ and keeps all other nodes, since its children become roots and the joins only move roots below roots. Insert adds one node, meld takes the union of the node sets, and decrease-key changes only the key of $x$ and moves subtrees, so no node is lost. By Lemmas 2 and 3 the invariants hold after each operation, so the next operation starts from a valid heap. $\blacksquare$
