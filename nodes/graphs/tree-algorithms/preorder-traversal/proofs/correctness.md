---
title: The stack-based preorder traversal lists the tree in preorder
proves: [correctness, termination]
status: full
---

Let $T$ be an ordered tree rooted at $r$, with child lists $C[v]$. Write $\mathrm{pre}(T_v)$ for the preorder of the subtree of $v$, and $\mathrm{pre}^-(T_v)$ for the same sequence without its first entry $v$. So $\mathrm{pre}^-(T_v) = \mathrm{pre}(T_{c_1}), \ldots, \mathrm{pre}(T_{c_k})$ for $C[v] = [c_1, \ldots, c_k]$. One *step* is one run of the body of the loop (lines L4 to L10).

**Claim.** Suppose that at some moment the stack is $S_0$ followed by the pair $(v, 0)$ on top, the last entry of out is $v$, and out is $X$ at this moment. Then after exactly $2|T_v| - 1$ more steps, the stack is $S_0$, out is $X, \mathrm{pre}^-(T_v)$, and during these steps no pair of $S_0$ is read or changed.

*Proof.* By strong induction on the height of $v$. Let $C[v] = [c_1, \ldots, c_k]$.

If $k = 0$, $v$ is a leaf, $T_v$ has one vertex, and $\mathrm{pre}^-(T_v)$ is empty. In the next step, line L4 reads $(v, 0)$, the test of line L5 fails, and line L10 pops $(v, 0)$. That is $1 = 2 \cdot 1 - 1$ step, and out is still $X$.

If $k \ge 1$, each child $c_j$ has a smaller height than $v$, so the claim holds for it. We show by induction on $j = 0, 1, \ldots, k$: after $\sum_{l \le j} 2|T_{c_l}|$ steps, the stack is $S_0, (v, j)$ and out is $X, \mathrm{pre}(T_{c_1}), \ldots, \mathrm{pre}(T_{c_j})$. For $j = 0$ this is the start. For $j < k$, the next step reads $(v, j)$, finds $j < k$ at line L5, sets the pair to $(v, j + 1)$, appends $c_{j+1}$ to out and pushes $(c_{j+1}, 0)$. Now the hypothesis of the claim holds for $c_{j+1}$, so after $2|T_{c_{j+1}}| - 1$ more steps the stack is $S_0, (v, j + 1)$ again and out has grown by $c_{j+1}, \mathrm{pre}^-(T_{c_{j+1}}) = \mathrm{pre}(T_{c_{j+1}})$. The steps used are $1 + 2|T_{c_{j+1}}| - 1 = 2|T_{c_{j+1}}|$, and the claim for $c_{j+1}$ says that the pairs below it, including $(v, j + 1)$ and $S_0$, are not touched.

At $j = k$, the stack is $S_0, (v, k)$ and out is $X, \mathrm{pre}^-(T_v)$. The next step finds $k = |C[v]|$ at line L5 and pops $(v, k)$. The total number of steps is $\sum_{l=1}^{k} 2|T_{c_l}| + 1 = 2(|T_v| - 1) + 1 = 2|T_v| - 1$, because the subtrees of the children partition $T_v$ minus $v$. Only the pair of $v$ and pairs above it were read or changed. $\square$

**Theorem.** PREORDER$(C, r)$ stops after $2n - 1$ steps and returns $\mathrm{pre}(T_r)$, where $n$ is the number of vertices.

*Proof.* After lines L1 and L2, the stack is the empty stack $S_0$ followed by $(r, 0)$, and out is $[r]$. The claim applies with $X = [r]$. After $2n - 1$ steps the stack is empty, so the test of line L3 fails, and out is $r, \mathrm{pre}^-(T_r) = \mathrm{pre}(T_r)$. Line L11 returns it. The count of steps is finite and exact, so the loop terminates. $\blacksquare$

**Stack size.** By the claim, while the walk is inside $T_v$, the pair of $v$ stays on the stack, and the pairs on the stack at any moment are the vertices of one path from $r$ down. So the stack never holds more than $h + 1$ pairs, where $h$ is the height of $T$.
