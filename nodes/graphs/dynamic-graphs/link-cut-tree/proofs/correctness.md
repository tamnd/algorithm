---
title: The operations of a link-cut tree keep the preferred path invariant
proves: [correctness]
status: full
---

We use invariant (L) of the page. Each real tree is rooted. For a splay tree $S$, write $\mathrm{seq}(S)$ for its symmetric order with all pending reversal bits applied: a bit on a vertex reverses the sequence of its whole subtree. (L1) says that $\mathrm{seq}(S)$ is a vertical path $x_1, \ldots, x_k$ of the real tree, with $x_{i+1}$ a child of $x_i$. (L2) says that the parent pointer of the splay root of $S$ is the real parent of $x_1$, or nothing if $x_1$ is the root of its real tree. (L3) says that each stored sum and maximum is that of the values in the splay subtree. Each vertex lies in exactly one splay tree.

**Lemma 1 (splaying).** Pushing a reversal bit and rotating inside a splay tree change neither $\mathrm{seq}(S)$ nor the set of its vertices, and they keep (L3). After SPLAY$(x)$, $x$ is the splay root and its parent pointer is the old path-parent of $S$.

*Proof.* Pushing the bit of $y$ swaps the children of $y$ and toggles the bits of both children. The sequence of the subtree of $y$ was the reverse of $\mathrm{seq}(\text{left})\,y\,\mathrm{seq}(\text{right})$, with the children's sequences read with their own bits; after the push it is $\mathrm{rev}(\mathrm{seq}(\text{right}))\,y\,\mathrm{rev}(\mathrm{seq}(\text{left}))$, which is the same sequence. SPLAY pushes the bits on the path from the splay root to $x$ before any rotation, so every rotation acts on vertices without pending bits, where it keeps the symmetric order as in any binary search tree. Each rotation recomputes the aggregates of the two rotated vertices from their new children, which keeps (L3). In a rotation at the splay root $p$, the new splay root $x$ takes the parent pointer of $p$, so the path-parent is kept. $\square$

**Lemma 2 (access).** After ACCESS$(v)$, (L) holds, the splay tree of $v$ holds exactly the path from the root of the real tree to $v$, and $v$ is its splay root with no right child.

*Proof.* Let the loop visit $x_0 = v, x_1, x_2, \ldots, x_t$, where $x_{i+1}$ is the parent pointer of $x_i$ after the splay of $x_i$. We show by induction on $i$ that after the step at $x_i$ (lines L3 to L5), (L) holds, and the splay tree of $x_i$ holds the path from the top of the old path of $x_i$ down to $v$, ordered by depth.

For $i = 0$, after line L3 $v$ is the splay root of its path $P$ by Lemma 1. Its right subtree holds the vertices of $P$ below $v$. Line L4 makes that subtree a separate splay tree. Its sequence is the part of $P$ below $v$, a vertical path whose top is a child of $v$, and its root keeps the parent pointer $v$, so (L2) holds for it. The tree of $v$ now holds the part of $P$ from its top to $v$. The aggregates of $v$ are recomputed, so (L3) holds.

For $i > 0$, the splay root $x_{i-1}$ of the tree $S$ built so far has parent pointer $x_i$, which by (L2) is the real parent of the top of $\mathrm{seq}(S)$. So the path in $S$ starts at a child of $x_i$. After line L3, $x_i$ is the root of its splay tree, whose sequence is a path $Q$ through $x_i$. Line L4 makes the part of $Q$ below $x_i$ a separate splay tree with path-parent $x_i$, as in the base case, and makes $S$ the right subtree of $x_i$. The sequence of the tree of $x_i$ is now the part of $Q$ from its top to $x_i$, then $\mathrm{seq}(S)$, which is a vertical path ordered by depth because the top of $\mathrm{seq}(S)$ is a child of $x_i$. Line L4 also sets the parent of $x_{i-1}$ to $x_i$, now as a splay edge, and the aggregates of $x_i$ are recomputed.

The loop ends when the parent pointer is nothing, so by (L2) the top of the last path is the root of the real tree. Then the splay tree of $v$ holds the path from the root to $v$. The last splay, line L6, moves $v$ to the splay root; since $v$ is the deepest vertex of the sequence, it has no right child. $\square$

**Lemma 3 (make root).** After MAKE-ROOT$(v)$, (L) holds for the same tree rooted at $v$.

*Proof.* Let $r = y_1, y_2, \ldots, y_k = v$ be the path from the old root to $v$. Rooting at $v$ instead of $r$ changes the parent of $y_i$ from $y_{i-1}$ to $y_{i+1}$ for $i < k$, makes $v$ parentless, and keeps every other parent. By Lemma 2 the splay tree of $v$ holds exactly $y_1, \ldots, y_k$, and line L8 reverses its sequence to $y_k, \ldots, y_1$, which is a vertical path of the new rooted tree, top first. Its top $v$ has no parent, and the parent pointer of $v$ is nothing, as (L2) needs. Every other splay tree has a top $x$ that is not on the path (each $y_i$ is in the tree of $v$), so the parent of $x$ is unchanged, and its sequence is a path that avoids $y_1, \ldots, y_k$ except possibly at its parent, so its parent relations are unchanged. A reversal bit does not change any aggregate of a sum or a maximum. $\square$

**Theorem.** After each operation, (L) holds for the current forest, and each query returns the value of its definition.

*Proof.* At the start every vertex is a splay tree of its own with no parent pointer, which satisfies (L). Lemmas 1 to 3 cover splay, access and make root.

*Find root* (lines L9 and L10). After the access, the splay tree of $v$ holds the path from the real root to $v$, and its leftmost vertex in the symmetric order with bits applied is the first vertex of the sequence, the real root. The walk pushes bits on its way down, so it reads the right children. The final splay keeps (L) by Lemma 1.

*Connected.* Two vertices are in the same tree if and only if they have the same real root.

*Link$(u, v)$* (lines L11 and L12) with $u$ and $v$ in different trees. After MAKE-ROOT$(u)$, by Lemmas 2 and 3, $u$ is the real root of its tree and the splay root of a tree whose sequence starts at $u$. The access of $v$ keeps (L) and does not touch the tree of $u$. In the new forest, $v$ is the parent of $u$ and all other parents are kept. Setting the parent pointer of $u$ to $v$ makes (L2) hold for the splay tree of $u$, whose top is $u$; the other splay trees keep their tops and parents.

*Cut$(u, v)$* (lines L13 and L14) with $\{u, v\}$ a forest edge. After MAKE-ROOT$(u)$ and ACCESS$(v)$, by Lemma 2 the splay tree of $v$ holds the path from the root $u$ to $v$, which is $u, v$, with $v$ as splay root without a right child. So the tree has exactly two vertices and $u$ is the left child of $v$. Line L14 makes $u$ a splay tree of its own with no parent pointer: $u$ is the real root of its new tree, as (L2) needs. The splay tree of $v$ is now $\{v\}$, with no parent pointer, and $v$ is the root of its new tree. Every other splay tree keeps its top, and the real parent of each top is unchanged, since only the edge between $u$ and $v$ was removed. The aggregates of $v$ are recomputed.

*Path sum and path maximum* (lines L15 and L16). After MAKE-ROOT$(u)$ and ACCESS$(v)$, by Lemma 2 the splay tree with root $v$ holds exactly the path from $u$ to $v$, and by (L3) the aggregates at $v$ are those of this path.

*Set value* accesses $v$, so $v$ is a splay root, and recomputes only the aggregates of $v$, which are the only ones that contain its value.

*Lowest common ancestor.* After MAKE-ROOT$(r)$ and ACCESS$(u)$, the splay tree $R$ that holds the root $r$ has the sequence of the path from $r$ to $u$. Run the loop of an access of $v$. Every step before the last one splays a vertex whose splay tree does not contain $r$, so these steps do not change $R$; the last step visits a vertex $x$ of $R$, since the loop ends at the splay tree that contains the real root. By the induction in Lemma 2, $x$ is an ancestor of $v$ (or $v$ itself), and $x$ lies on the path from $r$ to $u$, so $x$ is a common ancestor. The vertex below $x$ on the path from $x$ to $v$, if any, is the top of a different preferred path, so it is not on the path from $r$ to $u$. Hence no deeper common ancestor exists, and $x$ is the lowest common ancestor. $\blacksquare$
