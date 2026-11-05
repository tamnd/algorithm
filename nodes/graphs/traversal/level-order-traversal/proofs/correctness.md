---
title: The queue-based traversal visits a binary tree in level order
proves: [correctness, termination]
status: full
---

Let $T$ be a binary tree with $n \ge 1$ nodes; for the empty tree, line L1 returns and the empty list is correct. Let $N_k$ be the list of the nodes of depth $k$ sorted by the relation "left of", for $k = 0, 1, \ldots, h$, where $h$ is the height. The level order is the concatenation $N_0 N_1 \cdots N_h$.

**Lemma 1 (left of, one level down).** Let $x \ne y$ be nodes of depth $k + 1$ with parents $p$ and $q$. If $p \ne q$, then $x$ is left of $y$ if and only if $p$ is left of $q$. If $p = q$, then $x$ is left of $y$ if and only if $x$ is the left child and $y$ is the right child.

*Proof.* If $p = q$, the deepest common ancestor of $x$ and $y$ is $p$, and the claim is the definition. If $p \ne q$, then $p$ and $q$ have the same depth $k$, and neither is an ancestor of the other. A common ancestor of $x$ and $y$ is not $x$ or $y$, so it is a common ancestor of $p$ and $q$, and conversely. So the deepest common ancestor $a$ is the same, and the paths from $a$ to $x$ and to $p$ start with the same child of $a$, and so do those to $y$ and to $q$. So the two relations agree. $\square$

**Lemma 2.** Write $C(x)$ for the list of the children of $x$, the left child first. If $N_k = (x_1, \ldots, x_r)$, then $N_{k+1} = C(x_1) C(x_2) \cdots C(x_r)$.

*Proof.* Each node of depth $k + 1$ has exactly one parent, of depth $k$, so the right side lists each node of depth $k + 1$ exactly once. Two nodes in the same block $C(x_i)$ are in the right order by the second part of Lemma 1, and two nodes in blocks $C(x_i)$ and $C(x_j)$ with $i < j$ are in the right order by the first part, because $x_i$ is left of $x_j$. $\square$

**FIFO order.** Let $E$ be the sequence of the nodes in the order in which they are enqueued. A FIFO queue dequeues in the order of enqueuing, so the nodes are visited in the order $E$, as far as the loop runs. By lines L2, L6 and L7, $E$ starts with the root, and for each visited node $y$, the block $C(y)$ is appended to $E$ at the visit of $y$. So $E = (\mathrm{root})\, C(e_1)\, C(e_2) \cdots$, where $e_1, e_2, \ldots$ are the entries of $E$ in order.

**Claim.** $E = N_0 N_1 \cdots N_h$.

*Proof.* We show by induction on $k$ that $E$ starts with $N_0 N_1 \cdots N_k$. For $k = 0$, $E$ starts with the root, and $N_0$ is the root. Assume that $E$ starts with $N_0 \cdots N_k$. The entries of $N_0 \cdots N_{k-1}$ contribute, by the FIFO order, the blocks of their children, which are $N_1 \cdots N_k$ by Lemma 2, and these come right after the root. So the children of the entries of $N_k$ are appended next, in the order of $N_k$, and by Lemma 2 they form $N_{k+1}$. So $E$ starts with $N_0 \cdots N_{k+1}$. Each node is in exactly one $N_k$ and is enqueued only by its parent or at line L2, so $E$ has no other entries. $\square$

**Termination.** Each node is enqueued at most once, by its unique parent or, for the root, at line L2, so there are $n$ enqueues, and the loop of line L3 runs $n$ times.

**Theorem.** LEVEL-ORDER$(T)$ visits each node of $T$ exactly once, in the level order $N_0 N_1 \cdots N_h$.

*Proof.* The loop ends after $n$ iterations, when every enqueued node is dequeued. The visits follow the order $E$, which is the level order by the claim. $\blacksquare$
