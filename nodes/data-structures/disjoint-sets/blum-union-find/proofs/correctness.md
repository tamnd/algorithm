---
title: Blum's k-UF trees stay valid and answer finds correctly
proves: [correctness, termination]
status: full
---

The *leaves* of a tree are its nodes of height 0, which are elements. We prove that after each operation: (S) the leaves of the tree of each root are exactly the elements of its set, and the root stores the name of an element of the set; (K) each tree satisfies the three rules of the page; and (H) the height field of each node equals the length of every path from it down to a leaf. At the start each element is a tree of one leaf of height 0, so all three hold.

**FIND.** The parent pointers form a forest, so the walk of line L1 ends at the root of the tree of $x$, after at most the height of that tree. By (S), the name there is an element of the set of $x$, and two elements get the same name exactly when they are in the same tree. FIND changes nothing.

**UNION.** Line L3 finds the roots. If they are equal, nothing changes. Otherwise let $r$ and $s$ be the two roots after line L4, so $r.h \ge s.h$. In every case below, the leaves of the new tree are the leaves of the two old trees, because nodes are only moved or added, never removed except an emptied root, which is not a leaf; and the root of the new tree stores the name of $r$ or of the new root $t$, which is the name of $r$, an element of the union. So (S) holds. We check (K) and (H).

*Line L6, equal heights $h$, and $h = 0$ or both roots have at least $k$ children.* The new root $t$ has height $h + 1$ and the two children $r$ and $s$, both of height $h$, so (H) holds and the leaves are at depth $h + 1$, which is rule 1. Rule 2 holds for $t$. The nodes $r$ and $s$ are now inner non-root nodes if $h \ge 1$, and they have at least $k$ children, which is rule 3; if $h = 0$ they are leaves and rule 3 does not apply. Other nodes are unchanged.

*Line L8, equal heights $h \ge 1$, and not both roots have $k$ children.* After line L7, $s$ has the fewer children, so fewer than $k$. Its children have height $h - 1$ by (H) and become children of $r$, which has height $h$; so (H) holds and all leaves stay at depth $h$. The root $r$ had at least 2 children and keeps them, so rule 2 holds. The moved nodes keep their own children, so rule 3 holds. The node $s$ is dropped.

*Line L10, $r.h > s.h$, and $s$ is a leaf or has at least $k$ children.* The leftmost path of $r$ has a node of each height from $r.h$ down to 0, by (H), so the node $v$ of height $s.h + 1$ exists, and $v$ is an inner node. $s$ becomes a child of $v$; then (H) holds at $v$, and the leaves of $s$ have depth $(r.h - s.h - 1) + 1 + s.h = r.h$, which is rule 1. Now $s$ is a non-root; if it is inner, it has at least $k$ children, which is rule 3. $v$ only gains a child.

*Line L11, $r.h > s.h \ge 1$, and $s$ has fewer than $k$ children.* The node $v$ of height $s.h \ge 1$ on the leftmost path of $r$ exists, as above. The children of $s$, of height $s.h - 1$, become children of $v$, so (H) holds and their leaves have depth $r.h$. $v$ only gains children, and the moved nodes keep theirs, so rules 2 and 3 hold. The node $s$ is dropped.

So (S), (K) and (H) hold after every operation, and FIND and UNION are correct.

**Termination and the height bound.** By (K), a tree of height $h \ge 1$ has at least two subtrees of height $h - 1$ below the root, and every inner non-root node has at least $k$ children, so it has at least $2k^{h-1}$ leaves. With at most $n$ leaves, $h \le 1 + \log_k(n/2)$. Each walk up in FIND or ROOT and each walk down in lines L10 and L11 takes at most $h$ steps, and the moves of line L8 or L11 take fewer than $k$ steps. So every operation terminates, in $O(k + \log_k n)$ steps. $\blacksquare$
