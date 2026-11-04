---
title: Correctness of the LOUDS navigation formulas
proves: [correctness]
status: full
---

Let $v_0, \ldots, v_{n-1}$ be the nodes in level order, $d_k$ the degree of $v_k$, and $L = 10\, 1^{d_0} 0 \cdots 1^{d_{n-1}} 0$. Call $10$ the code of the super-root $v_{-1}$ and $1^{d_k} 0$ the code of $v_k$.

**Fact A.** The code of $v_k$ starts at position $\text{select}_0(k+1) + 1$ and ends at $\text{select}_0(k+2)$. Each code ends with exactly one 0, and the codes of $v_{-1}, v_0, \ldots, v_{k-1}$ come first, so the $(k+1)$-th 0 ends the code of $v_{k-1}$ and the $(k+2)$-th 0 ends the code of $v_k$.

**Fact B.** The $(j+1)$-th 1 of $L$ stands for $v_j$, meaning that it lies in the code of the parent of $v_j$ (with $v_{-1}$ as the parent of $v_0$), and the 1s of one code stand for the children of that node in order. A breadth-first traversal appends the children of $v_k$ to its queue when it removes $v_k$, in order; the queue therefore receives $v_0$ (the child of $v_{-1}$), then the children of $v_0$, then those of $v_1$, and so on. Its output order, which is the level order, is the order of insertion. The 1s of $L$ are written in the same order: one for $v_0$ in the super-root's code, then one for each child of $v_0$, then of $v_1$, and so on. So the $(j+1)$-th 1 written corresponds to the $(j+1)$-th node inserted, which is $v_j$.

**DEGREE.** By Fact A, the code of $v_k$ occupies positions $\text{select}_0(k+1) + 1$ to $\text{select}_0(k+2)$, and all of them but the last are 1s, so $d_k = \text{select}_0(k+2) - \text{select}_0(k+1) - 1$.

**CHILD.** Let $s = \text{select}_0(k+1)$. The bits before $s + 1$ contain $\text{rank}_1(s + 1) = \text{rank}_1(s)$ ones, since $L[s] = 0$. The $i$-th bit of the code of $v_k$, for $1 \le i \le d_k$, is therefore the $(\text{rank}_1(s) + i)$-th 1 of $L$, and by Fact B it stands for $v_{\text{rank}_1(s) + i - 1}$, the $i$-th child of $v_k$. Line L2 rejects $i > d_k$.

**PARENT.** For $k \ge 1$, let $p = \text{select}_1(k+1)$. By Fact B, $p$ lies in the code of the parent $v_j$ of $v_k$, and $j \ge 0$ because only $v_0$ has its 1 in the super-root's code. The 0s before $p$ are the final 0s of the codes that end before $p$, which are those of $v_{-1}, v_0, \ldots, v_{j-1}$; the code of $v_j$ contains $p$ and ends after it. So $\text{rank}_0(p) = j + 1$ and line L7 returns $j$.

**NEXT-SIBLING.** The siblings of $v_k$ are the nodes whose 1s lie in the same code. If $L[p+1] = 1$, that 1 is in the same code (a code has no 0 before its end), it is the $(k+2)$-th 1, and by Fact B it stands for $v_{k+1}$, the next child of the same parent. If $L[p+1] = 0$, the code ends at $p + 1$ and $v_k$ is the last child. The same argument with $L[p-1]$ gives PREV-SIBLING for $k \ge 1$; for $k = 0$, $p = 0$ and the root has no siblings.

**CHILD-RANK.** With $p$ as above and $r = \text{rank}_0(p)$, the code containing $p$ starts at $\text{select}_0(r) + 1$, since the $r$-th 0 is the last 0 before $p$. The bits from there to $p$ are all 1s, and there are $p - \text{select}_0(r)$ of them, which is the index of $v_k$ among its siblings.

**Space.** $L$ has $2$ bits for the super-root and $d_k + 1$ bits for each $v_k$, in total $2 + (n - 1) + n = 2n + 1$, since the degrees sum to the $n - 1$ edges. $\blacksquare$
