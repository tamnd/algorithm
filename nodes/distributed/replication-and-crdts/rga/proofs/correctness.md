---
title: The RGA list is the pre-order of its insertion tree, so replicas converge and local inserts land in place
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas. Each runs the main block. A local insert at visible index $i$ takes as reference the visible element $i - 1$ (or the head), makes a timestamp, applies the operation, and broadcasts it. Operations are delivered by causal broadcast: exactly once at each replica, after every operation in their causal past. Write $u \prec v$ when operation $u$ was delivered at the source of $v$ before $v$ was made, closed under transitivity.

**Timestamps.** Each insert $v$ made at replica $s$ gets $t(v) = (\mathit{ssn}, \mathit{sum}, s)$, where $\mathit{sum}$ is the number of inserts delivered at $s$ so far, $v$ included. All sessions have the same $\mathit{ssn}$ here. Timestamps are compared in lexicographic order.

**Claim 1 (timestamps are unique and grow along causality).** If $u \ne v$ are inserts then $t(u) \ne t(v)$, and if $u \prec v$ then $t(u) < t(v)$.

*Proof.* Let $H(v)$ be the set of inserts delivered at the source of $v$ when $v$ is made, $v$ included, so $\mathit{sum}(v) = |H(v)|$. If $u \prec v$, then every insert in $H(u)$ is in the causal past of $v$ and is delivered at the source of $v$ before $v$ by causal delivery, so $H(u) \subseteq H(v)$; and $v \in H(v) \setminus H(u)$. Hence $\mathit{sum}(u) < \mathit{sum}(v)$. Two inserts of the same replica are ordered by $\prec$, so they differ in $\mathit{sum}$; inserts of different replicas differ in the id. $\square$

**The tree.** For a set $D$ of inserts closed under taking references, let $T(D)$ be the tree with root the head, nodes $D$, and the parent of each insert its reference. Order the children of each node by decreasing timestamp. Let $\pi(D)$ be the pre-order of $T(D)$: a node, then the subtrees of its children in that order.

**Claim 2 (subtrees have larger timestamps).** Every descendant $d$ of a node $c$ in $T(D)$ has $t(d) > t(c)$.

*Proof.* The reference of an insert was delivered at its source before it was made, so a parent is causally before its child, and by transitivity $c \prec d$. Claim 1 gives $t(c) < t(d)$. $\square$

**Claim 3 (invariant).** At every time, replica $i$ has delivered a set $D_i$ of inserts that is closed under taking references, and its node list, tombstones included, is $\pi(D_i)$, with a node marked as a tombstone exactly when a delete of it has been delivered.

*Proof.* By induction on deliveries. At the start the list is the head alone. A delete (line L8) changes only a flag; its target was delivered before it, by causal delivery. Consider the delivery of an insert $v$ with reference $r$ and timestamp $t$. The reference is in $D_i$ by causal delivery, and $v$ is new. No node of $D_i$ has $v$ as its reference, because such an insert is causally after $v$. So in $T(D_i \cup \{v\})$, $v$ is a leaf child of $r$, and $\pi(D_i \cup \{v\})$ is $\pi(D_i)$ with $v$ put right after the subtrees of the children $c$ of $r$ with $t(c) > t$, and before the subtree of the first child with $t(c) < t$ if there is one; otherwise right after the whole subtree of $r$.

Line L2 starts right after $r$. In $\pi(D_i)$ the next nodes are the subtrees of the children of $r$ in decreasing timestamp order. While the children have timestamps above $t$, every node in their subtrees has a timestamp above $t$ too, by Claim 2, so lines L3 and L4 skip them all. Then one of three things holds. (a) The next node is a child $c$ of $r$ with $t(c) < t$; the loop stops there, which is the right place. (b) The subtree of $r$ ends and the list ends; the loop stops at the end, which is right. (c) The subtree of $r$ ends and the next node $q$ is a child of some ancestor $A$ of $r$ (where $A$ may be $r$'s parent or higher), coming after the child of $A$ that is $r$ or an ancestor of $r$; call that child $B$. Then $t(q) < t(B)$ by the order of children, $t(B) \le t(r)$ by Claim 2, and $t(r) < t$ because $r \prec v$. So $t(q) < t$ and the loop stops at $q$, which is the right place. Timestamps are unique by Claim 1, so no comparison is an equality. Lines L5 to L7 insert $v$ there. $\square$

**Theorem 1 (convergence).** Two replicas that have delivered the same set of operations have the same list and the same tombstones, so READ returns the same sequence.

*Proof.* By Claim 3, both lists are $\pi(D)$ for the same $D$, with the same flags. $\square$

**Theorem 2 (local intent).** A local INSERT$(i, x)$ makes $x$ the $i$-th visible element at its source, and a local DELETE$(i)$ hides exactly the $i$-th visible element.

*Proof.* The new timestamp is larger than every timestamp delivered at the source, by Claim 1, since each of those inserts is causally before the new one. So the loop of line L3 stops at once and $x$ goes right after its reference, which was visible element $i - 1$ or the head. The delete case is immediate. $\square$

**Theorem 3 (one order for all replicas).** Let $D$ be the set of all inserts of a run. At every time, the list of every replica is the restriction of $\pi(D)$ to its delivered set.

*Proof.* For two nodes $x$ and $y$ of a tree, whether $x$ comes before $y$ in pre-order depends only on their paths from the root: $x$ is first if it is an ancestor of $y$, or if at the first node where the paths split, the child towards $x$ has the larger timestamp. These paths are the same in $T(D_i)$ and in $T(D)$, since $D_i$ is closed under taking references. So $\pi(D_i)$ is $\pi(D)$ restricted to $D_i$. $\square$

Theorem 3, with Theorem 2 and the tombstone rule, is the strong list specification of Attiya et al. in the form used here.

**Termination.** The loop of line L3 moves forward through a finite list. $\blacksquare$
