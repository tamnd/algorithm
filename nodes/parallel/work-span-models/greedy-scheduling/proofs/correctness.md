---
title: GREEDY-SCHEDULE returns a valid greedy schedule of length at most (T_1 - T_infinity)/p + T_infinity
proves: [correctness, complexity]
status: full
---

We use the pseudocode of the page. The input is a DAG $G$ with strands $V$, $|V| = n$, $m$ edges, and $p \ge 1$. Number the passes of the loop of line L4 as steps $1, 2, \ldots$, and let $X_t$ be the set chosen in line L6 at step $t$. Let $D_t = X_1 \cup \cdots \cup X_{t-1}$ be the strands that ran before step $t$.

**Invariant.** At line L4, before step $t$:

> **(G1)** for each strand $v \notin D_t$, $indeg[v]$ is the number of predecessors of $v$ that are not in $D_t$; **(G2)** $R$ is exactly the set of strands $v \notin D_t$ whose predecessors are all in $D_t$, that is, the ready strands; **(G3)** the sets $X_1, \ldots, X_{t-1}$ are disjoint.

*Initialization.* Before step 1, $D_1 = \emptyset$. Line L1 sets $indeg[v]$ to the number of predecessors of $v$, which is (G1). Line L2 puts in $R$ the strands with no predecessor, which is (G2). (G3) holds trivially.

*Maintenance.* Assume the invariant before step $t$. Line L6 picks $X_t \subseteq R$, so by (G2) the strands of $X_t$ are not in $D_t$, and (G3) holds before step $t + 1$. Line L7 removes $X_t$ from $R$. For each edge $u \to v$ with $u \in X_t$, line L9 lowers $indeg[v]$ by one, so afterwards $indeg[v]$ counts the predecessors of $v$ outside $D_{t+1} = D_t \cup X_t$, which is (G1). A strand $v$ goes into $N$ in line L10 exactly when this count becomes 0 at step $t$, that is, when its last predecessor outside $D_t$ is in $X_t$. Such a $v$ has a predecessor in $X_t$, so it was not ready before step $t$ and is not in $X_t$. After line L11, $R$ holds the strands that were ready before step $t$ and did not run, which are still ready, and the strands that became ready in step $t$. A strand outside $D_{t+1}$ whose predecessors are all in $D_{t+1}$ is in one of these two groups, according to whether it has a predecessor in $X_t$. So (G2) holds before step $t + 1$.

**Validity.** By (G2), each strand of $X_t$ is ready at step $t$, so each of its predecessors is in $D_t$ and ran at an earlier step. So for each edge $u \to v$, $u$ runs before $v$. By (G3), no strand runs twice. Line L5 gives $|X_t| = k \le p$, and $|X_t| \ge 1$ because $R$ is not empty at line L4.

**Greediness.** By (G2), $|R|$ at line L5 is the number $r$ of ready strands, and the step runs $k = \min(p, r)$ of them. If $k < p$, then $k = r$ and $X_t = R$: every ready strand runs.

**Termination and completeness.** Each step runs at least one new strand, by (G3), so there are at most $n$ steps. The loop stops when $R$ is empty. If some strand had not run at that point, the set $U = V \setminus D_t$ of strands that have not run is not empty, and the sub-DAG on $U$ has a source $v$, because $G$ is acyclic. All predecessors of $v$ are then in $D_t$, so $v$ is ready and $v \in R$ by (G2), which contradicts $R = \emptyset$. So every strand runs, and the returned list is a schedule of all of $G$. $\blacksquare$

**Length.** Let $C$ be the number of steps with $k = p$ (complete) and $I$ the number with $k < p$ (incomplete), and let $T_p = C + I$. Write $G_t$ for the sub-DAG of $G$ on $V \setminus D_t$ and $S(G_t)$ for the number of strands on its longest path.

At an incomplete step $t$, $X_t$ is the set of all ready strands, which by (G2) are the sources of $G_t$. Let $P$ be a path of $G_{t+1}$ with first strand $v$. Then $v$ is not a source of $G_t$, so it has a predecessor $u$ in $G_t$, and $u$ followed by $P$ is a path of $G_t$ with one more strand. So $S(G_{t+1}) \le S(G_t) - 1$. At a complete step, $G_{t+1}$ is a sub-DAG of $G_t$, so $S(G_{t+1}) \le S(G_t)$. Since $S(G_1) = T_\infty$ and $S(G_t) \ge 1$ before each step, there are at most $T_\infty$ incomplete steps: $I \le T_\infty$.

Each strand runs once, each complete step runs $p$ strands and each incomplete step at least one, so $pC + I \le T_1$. Then

$$T_p = C + I \le \frac{T_1 - I}{p} + I = \frac{T_1}{p} + \Big(1 - \frac1p\Big) I \le \frac{T_1 - T_\infty}{p} + T_\infty. \qquad \blacksquare$$

**Running time.** Line L1 takes $\Theta(n + m)$ time. With $R$ as a first-in first-out queue, lines L5 to L7 take $O(k)$ time at each step, and the sum of $k$ over all steps is $n$. Each edge is looked at once in line L8, when its tail runs, so lines L9 and L10 run $m$ times in total. Line L11 takes $O(|N|)$ time, and each strand enters $N$ at most once. The total is $\Theta(n + m)$ time, and the space is $\Theta(n + m)$. $\blacksquare$
