---
title: The stack-based inorder traversal lists each node once, in inorder
proves: [correctness, termination]
status: full
---

Let the binary tree have the nodes $0, \ldots, n-1$ and the root $r$, or be empty with $r = \mathrm{NIL}$. For a node $x$ let $T(x)$ be the set of nodes in the subtree of $x$, with $T(\mathrm{NIL}) = \emptyset$, and let $In(x)$ be the inorder list of $T(x)$: $In(\mathrm{NIL}) = (\,)$ and $In(x) = In(left[x]) \cdot (x) \cdot In(right[x])$. Because the subtrees $T(left[x])$ and $T(right[x])$ are disjoint and do not contain $x$, $In(x)$ lists each node of $T(x)$ exactly once.

Consider the state of INORDER at each test of line L2 and at each test of line L3. Write the stack as $s_1, \ldots, s_k$ from bottom to top, and define
$$pend = In(x) \cdot (s_k) \cdot In(right[s_k]) \cdot (s_{k-1}) \cdot In(right[s_{k-1}]) \cdots (s_1) \cdot In(right[s_1]).$$

**Lemma 1 (invariant).** At every test of lines L2 and L3, $out \cdot pend = In(r)$.

*Proof.* By induction on the number of executed lines. Before the first test of line L2, line L1 has set $out = (\,)$, $S$ empty and $x = r$, so $pend = In(r)$.

Line L4 runs when $x \ne \mathrm{NIL}$. Before it, $pend = In(x) \cdot R$ for the rest $R$. It pushes $x$ and sets $x \gets left[x]$, so afterwards $pend = In(left[x]) \cdot (x) \cdot In(right[x]) \cdot R$, which is $In(x) \cdot R$ by the definition of $In$. So $pend$ and $out$ do not change.

Lines L5 to L7 run when the test of line L3 fails, so $x = \mathrm{NIL}$ and $In(x) = (\,)$. The stack is not empty: the test of line L2 passed with $x = \mathrm{NIL}$ or, if it passed with $x \ne \mathrm{NIL}$, line L4 ran at least once. So $pend = (s_k) \cdot In(right[s_k]) \cdot R'$, where $R'$ is the part for $s_1, \ldots, s_{k-1}$. Line L5 pops $s_k$, line L6 appends it to $out$, and line L7 sets $x \gets right[s_k]$. Afterwards $out$ has gained $s_k$ at its end and $pend = In(right[s_k]) \cdot R'$, so $out \cdot pend$ is unchanged. $\square$

**Lemma 2 (each node is pushed at most once).** Every node of $pend$ appears in it exactly once, and a node is pushed only when it is the root $x$ of the first part $In(x)$ of $pend$.

*Proof.* $out \cdot pend = In(r)$ lists each node once, so each node is in exactly one of $out$ and $pend$. Line L4 pushes $x$, which is in $In(x) \subseteq pend$. After the push, $x$ is a stack entry and stays in $pend$ until line L5 pops it and line L6 moves it to $out$. After that, it is in $out$ for good: no line removes entries from $out$. A node in $out$ is not in $pend$, so it is never again the value of $x$ at line L4: the values of $x$ at line L4 are roots of subtrees whose nodes are all in $pend$. So each node is pushed at most once. $\square$

**Termination.** Each pass of the inner loop pushes a node, so by Lemma 2 there are at most $n$ passes in all. Each pass of the outer loop pops a node, and a node can be popped only after it was pushed, so there are at most $n$ passes of the outer loop. So INORDER terminates, after at most $n$ pushes and $n$ pops.

**Correctness.** When the outer loop stops, $x = \mathrm{NIL}$ and $S$ is empty, so $pend = In(\mathrm{NIL}) = (\,)$, and by Lemma 1, $out = In(r)$. Since $In(r)$ has exactly $n$ entries, there were exactly $n$ pushes and $n$ pops, and line L8 returns the inorder list of the tree.

**Search trees.** If the tree is a binary search tree with distinct keys, then for every node $x$ the keys of $T(left[x])$ are smaller than $key[x]$ and those of $T(right[x])$ are larger. By induction on the height, the keys of $In(x)$ are increasing: the keys of $In(left[x])$ are increasing and below $key[x]$, and those of $In(right[x])$ are increasing and above it. So the output lists the keys in sorted order. $\blacksquare$
