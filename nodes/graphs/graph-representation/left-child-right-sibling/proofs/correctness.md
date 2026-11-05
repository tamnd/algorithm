---
title: The left-child right-sibling operations keep the chain invariant and traverse in preorder
proves: [correctness]
status: full
---

We use the pseudocode of the page. The invariant is:

> **(S1)** For each node $p$ with children $c_1, \ldots, c_k$ from left to right: if $k = 0$ then $p.child = $ NIL; if $k \ge 1$ then $p.child = c_1$, $c_i.sibling = c_{i+1}$ for $1 \le i < k$, and $c_k.sibling = $ NIL. **(S2)** $c_i.parent = p$ for each child $c_i$ of $p$, and the root has no parent and no sibling.

A tree with one node, the root, meets (S1) and (S2) with all links NIL.

**ADD-CHILD.** Let $p$ have the children $c_1, \ldots, c_k$, and let $x$ be a new node with no children, so $x.child = $ NIL. After the call, $p$ has the children $x, c_1, \ldots, c_k$. Line L3 sets $p.child = x$. Line L2 sets $x.sibling$ to the old $p.child$, which by (S1) is $c_1$ if $k \ge 1$ and NIL if $k = 0$. The links $c_i.sibling$ do not change. So (S1) holds for $p$. Line L1 sets $x.parent = p$, so (S2) holds for $x$. No other node changes, and $x$ has no children, so (S1) and (S2) hold for each node.

**CHILDREN.** By (S1), the sequence $p.child, p.child.sibling, \ldots$ is $c_1, c_2, \ldots, c_k$ and then NIL. Lines L4 to L7 report exactly this sequence and stop after $k$ steps of line L7.

**PREORDER.** Write $\text{pre}(x)$ for the preorder of the subtree of $x$: $x$, then $\text{pre}(c_1), \ldots, \text{pre}(c_k)$ for the children $c_1, \ldots, c_k$ of $x$. For a node $y$ with right siblings $y = y_1, y_2, \ldots, y_j$ (that is, $y_{i+1} = y_i.sibling$ and $y_j.sibling = $ NIL), write $\text{chain}(y) = \text{pre}(y_1) \cdots \text{pre}(y_j)$, the concatenation. By (S1), $\text{pre}(x) = x \cdot \text{chain}(x.child)$ when $x.child \ne$ NIL, and $\text{pre}(x) = x$ otherwise.

Define the *pending sequence* of a stack $S = [s_1, \ldots, s_t]$, with $s_t$ on top, as $\text{seq}(s_t) \cdots \text{seq}(s_1)$, where $\text{seq}(r) = \text{pre}(r)$ for the start node $r$ and $\text{seq}(y) = \text{chain}(y)$ for each other node. We claim that before each test of line L9,

> **(P)** the nodes reported so far, followed by the pending sequence of $S$, is $\text{pre}(r)$.

*Initialization.* Line L8 makes $S = [r]$ and nothing is reported. The pending sequence is $\text{pre}(r)$.

*Maintenance.* Let $x$ be the top of $S$. Line L10 pops it and line L11 reports it.

- If $x = r$, then $\text{seq}(x) = \text{pre}(r) = r \cdot \text{chain}(r.child)$, or just $r$ if $r$ has no child. Line L12 pushes nothing. Line L13 pushes $r.child$ if it exists, with $\text{seq}(r.child) = \text{chain}(r.child)$.
- If $x \ne r$, then $\text{seq}(x) = \text{chain}(x) = \text{pre}(x) \cdot \text{chain}(x.sibling)$, with the second factor empty if $x.sibling = $ NIL. And $\text{pre}(x) = x \cdot \text{chain}(x.child)$, with the second factor empty if $x.child = $ NIL. Line L12 pushes $x.sibling$ if it exists, and then line L13 pushes $x.child$ on top of it if it exists.

In each case, the reported $x$ followed by the pending sequence of the pushed nodes, top first, is $\text{seq}(x)$. The rest of the stack is unchanged. So (P) holds again.

*Termination.* Each iteration reports one node, and by (P) the reported nodes are a prefix of $\text{pre}(r)$, which has $s$ nodes, so there are at most $s$ iterations. The loop stops when $S$ is empty, and then the pending sequence is empty, so by (P) the reported sequence is $\text{pre}(r)$. $\square$

The same argument, with $\text{post}(x) = \text{post}(c_1) \cdots \text{post}(c_k) \cdot x$ and a mark on each node whose children were pushed, proves the postorder routine of the implementation.

**Binary-tree view.** Let $B$ be the binary tree on the same nodes with $\text{left}(x) = x.child$ and $\text{right}(x) = x.sibling$. Then $\text{chain}(y)$ is the preorder of the subtree of $y$ in $B$: by induction on the size of this subtree, its preorder is $y$, then the preorder of the subtree of $y.child$, then that of $y.sibling$, which is $\text{pre}(y) \cdot \text{chain}(y.sibling)$ by the equation above. For the root, which has no sibling, this gives that the preorder of the tree is the preorder of $B$.

**Cost.** Each line of ADD-CHILD is $O(1)$. CHILDREN does $O(1)$ work for each of the $k$ children, plus $O(1)$. PREORDER does $O(1)$ work in each of its at most $s$ iterations. $\square$
