---
title: The stack-based postorder traversal lists the tree in postorder
proves: [correctness, termination]
status: full
---

Let $T$ be an ordered tree rooted at $r$, with child lists $C[v]$, and let $\mathrm{post}(T_v)$ be the postorder of the subtree of $v$: $\mathrm{post}(T_v) = \mathrm{post}(T_{c_1}), \ldots, \mathrm{post}(T_{c_k}), v$ for $C[v] = [c_1, \ldots, c_k]$. One *step* is one run of the body of the loop (lines L4 to L10).

**Claim.** Suppose that at some moment the stack is $S_0$ followed by $(v, 0)$ on top, and out is $X$. Then after exactly $2|T_v| - 1$ more steps, the stack is $S_0$ and out is $X, \mathrm{post}(T_v)$. During these steps no pair of $S_0$ is read or changed.

*Proof.* By strong induction on the height of $v$. Let $C[v] = [c_1, \ldots, c_k]$.

*Base, $k = 0$.* The next step reads $(v, 0)$ at line L4. The test $0 < 0$ of line L5 fails, so lines L9 and L10 pop the pair and append $v$. One step was used, $2 \cdot 1 - 1 = 1$, and out is $X, v = X, \mathrm{post}(T_v)$.

*Step, $k \ge 1$.* Each child has a smaller height, so the claim holds for it. By an inner induction on $j = 0, \ldots, k$: after $\sum_{l \le j} 2|T_{c_l}|$ steps, the stack is $S_0, (v, j)$ and out is $X, \mathrm{post}(T_{c_1}), \ldots, \mathrm{post}(T_{c_j})$. This holds for $j = 0$. For $j < k$, the next step reads $(v, j)$, finds $j < k$, changes the pair to $(v, j + 1)$ and pushes $(c_{j+1}, 0)$ at lines L6 and L7. It appends nothing. By the claim for $c_{j+1}$, after $2|T_{c_{j+1}}| - 1$ more steps the stack is $S_0, (v, j + 1)$ and out has grown by $\mathrm{post}(T_{c_{j+1}})$, and the pairs below $(c_{j+1}, 0)$ were not touched. That is $2|T_{c_{j+1}}|$ steps in all, which proves the inner step.

At $j = k$ the next step finds $k = |C[v]|$, pops $(v, k)$ and appends $v$. So out is $X, \mathrm{post}(T_{c_1}), \ldots, \mathrm{post}(T_{c_k}), v = X, \mathrm{post}(T_v)$, and the stack is $S_0$. The number of steps is $\sum_{l=1}^{k} 2|T_{c_l}| + 1 = 2(|T_v| - 1) + 1 = 2|T_v| - 1$, because the subtrees of the children partition the vertices of $T_v$ other than $v$. Only the pair of $v$ and the pairs above it were read or changed. $\square$

**Theorem.** POSTORDER$(C, r)$ stops after $2n - 1$ steps and returns $\mathrm{post}(T_r)$.

*Proof.* After lines L1 and L2, out is empty and the stack is the empty stack followed by $(r, 0)$. By the claim with $X$ empty, after $2n - 1$ steps the stack is empty and out is $\mathrm{post}(T_r)$. The test of line L3 then fails, and line L11 returns out. The number of steps is finite, so the procedure terminates. $\blacksquare$

**Stack size.** By the claim, the pairs on the stack are always the vertices of one path that starts at $r$ and goes down. So the stack holds at most $h + 1$ pairs, where $h$ is the height of $T$.
