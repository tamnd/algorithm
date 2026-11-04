---
title: The hollow heap operations keep the heap order and find the minimum
proves: [correctness, termination]
status: full
---

We use the notation of the page. The *child list* of a node $x$ starts at $\mathit{child}(x)$, follows the sibling pointers, and ends at nil or right after the first node $u$ with $\mathit{ep}(u) = x$. An edge goes from $x$ to each node of its child list. A heap with root $h$ satisfies the following invariants.

- **(G)** The nodes and edges form a finite acyclic graph in which every node is a descendant of $h$.
- **(P)** Each node other than $h$ has one or two parents. A node $u$ with two parents is hollow, $\mathit{ep}(u)$ is one of them, $u$ is the last node of the child list of $\mathit{ep}(u)$, and its sibling pointer continues the child list of the other parent. A node with one parent, or none, has $\mathit{ep} = \mathrm{nil}$.
- **(O)** For each edge from $x$ to $y$, $\mathrm{key}(x) \le \mathrm{key}(y)$.
- **(R)** The heap is empty, or $h$ is full.
- **(I)** For each item $e$ in the heap, $\mathrm{node}(e)$ is a full node whose item is $e$; each full node holds an item of the heap.

**Lemma 1.** If (G), (O), (R) and (I) hold, the item of $h$ has the minimum key.

*Proof.* Each item is in a full node by (I), which is a descendant of $h$ by (G). The keys do not decrease along each path from $h$, by (O). $\square$

**Lemma 2.** LINK$(v, w)$ of two roots of disjoint heaps returns a root whose descendants are those of $v$ and $w$, and keeps (O), (P) and (G).

*Proof.* The loser $\ell$ becomes the first child of the winner $m$: its sibling pointer is set to the old first child of $m$, so the child list of $m$ gains $\ell$ at its front and keeps its old end. The only new edge goes from $m$ to $\ell$, with $\mathrm{key}(m) \le \mathrm{key}(\ell)$ by the test of line L1. $\ell$ was a root, so it now has one parent, and its $\mathit{ep}$ is nil by (P). No cycle is made, since $m$ is not a descendant of $\ell$ in disjoint heaps. $\square$

## Insert, meld and decrease-key

INSERT makes a full node of rank 0 with no children and links it with $h$; MELD links two roots. By Lemma 2 the invariants hold, and the new root is full, since both roots were full.

DECREASE-KEY$(e, k)$ with $k \le \mathrm{key}(\mathrm{node}(e))$. If $u = \mathrm{node}(e)$ is the root, setting its key keeps (O), since the key went down and the root has no parents. Else $u$ is full and is not the root, so by (P) it has one parent and $\mathit{ep}(u) = \mathrm{nil}$. Lines L8 to L11 make $v$ with the item $e$ and the key $k$, make $u$ hollow, and make $u$ the only node of the child list of $v$, with $\mathit{ep}(u) = v$; the sibling pointer of $u$ still continues the list of its first parent. So $u$ has two parents and meets (P). The new edge from $v$ to $u$ has $k \le \mathrm{key}(u)$, and the key of $u$ is unchanged, so (O) holds. Now $e$ is in the full node $v$ only, which gives (I). $v$ is a root, and line L12 links it with $h$, so by Lemma 2 (G) holds again. The new root is $h$ or $v$, both full.

## Delete

Line L13 makes $\mathrm{node}(e)$ hollow and removes $e$, which keeps (I), (G), (O) and (P). If $h$ is still full, (R) holds and we are done. Else the loop runs. Call a node *destroyed* if it enters $H$. The loop keeps the following.

**(L1)** Each node in $H$, or destroyed, is hollow and has no parent that is not destroyed. **(L2)** Each node $y$ that is not destroyed has a parent that is not destroyed, or is a full root in a tree of a root in $A$, and each node of a tree of $A$ that is not a root of $A$ has one parent. **(L3)** For a node $u$ that is not destroyed, $\mathit{ep}(u)$ is nil or a node that is not destroyed, and (P) holds for $u$ with respect to its parents that are not destroyed, except that $u$ may still be in the list of the node $x$ under scan.

*The cases of a child $u$ of $x$.* The node $x$ is hollow and all its parents are destroyed, by (L1).

- $u$ is full. By (P), $u$ has the one parent $x$. It becomes a root. Each ranked link in line L22 links two roots of trees in $A$, which are disjoint, so by Lemma 2 the result is a tree with a full root that is again in $A$ and (O) holds on the new edge. So (L2) holds for $u$.
- $u$ is hollow and $\mathit{ep}(u) = \mathrm{nil}$. By (P) and (L3), $x$ was its only parent that is not destroyed, so it has none now, and line L19 puts it into $H$, which keeps (L1).
- $u$ is hollow and $\mathit{ep}(u) \ne \mathrm{nil}$. Then $u$ has two parents, $x$ and $y$. If $\mathit{ep}(u) = x$, then $u$ is the last node of the list of $x$, so the scan stops; its sibling pointer continues the list of $y$, and with $\mathit{ep}(u) = \mathrm{nil}$ it now has the one parent $y$, as (P) asks. If $\mathit{ep}(u) = y$, then $x$ is the first parent; setting the sibling pointer of $u$ to nil ends the list of $y$ at $u$, as before, and with $\mathit{ep}(u) = \mathrm{nil}$ it has the one parent $y$. The scan of $x$ goes on with the sibling read before the change.

So the scan of $x$ visits every node of its child list. After it, $x$ is destroyed and no node that is not destroyed points to it as a parent: every child of $x$ was handled above.

*After the loop.* $H$ is empty. Let $y$ be a node that is not destroyed. Walk from $y$ to a parent that is not destroyed, while there is one. The walk ends, by (G), at a node $z$ with no parent that is not destroyed. If $z$ were hollow, then when the scan of its last destroyed parent reached it, its $\mathit{ep}$ was nil, and it entered $H$, so it was destroyed; this is false. So $z$ is full, and it is a root of a tree in $A$ or below one, by (L2). Hence every node that is not destroyed is in a tree of a root of $A$, and in particular so is every full node, since destroyed nodes are hollow by (L1). The links of lines L25 and L26 join the roots of $A$ into one tree, by Lemma 2, whose root is full, being a root of $A$. If $A$ is empty, no full node is left and the heap is empty. So (G), (O), (P) and (R) hold, and (I) holds, since no full node was changed.

DELETE-MIN reads the item of $h$, which is a minimum by Lemma 1, and deletes it.

## Termination

INSERT, MELD and DECREASE-KEY do a constant number of steps. In DELETE, a node enters $H$ only when the scan of its last remaining parent reaches it, and a scanned node is destroyed, so each node enters $H$ at most once and the outer loop runs at most once per node of the finite graph. Each child list is finite and is scanned once. Each iteration of the inner loop of line L21 removes one root from $A$, so it runs at most $|A|$ times. The final loop runs once per root in $A$. So every operation ends.

Together with Lemma 1, the invariants show that FIND-MIN and DELETE-MIN return an item of minimum key, and that each operation leaves a valid hollow heap that holds exactly the items inserted and not yet deleted, with their current keys. $\blacksquare$
