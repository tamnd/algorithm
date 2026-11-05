---
title: BUILD makes a valid compressed sparse row array and the queries answer for the stored graph
proves: [correctness, termination]
status: full
---

Let $E$ be the input list of BUILD, of length $M$, with distinct pairs $(u, v)$, $0 \le u, v < n$; for an undirected graph it holds each edge in both orders and no loop. For a vertex $u$ let $d(u)$ be the number of pairs of $E$ with first end $u$. The structure stands for the graph with an edge $(u, v)$, or $\{u, v\}$, for each $v$ in the row $\mathit{adj}[\mathit{off}[u] \ldots \mathit{off}[u+1] - 1]$. The invariant (C) is (C1) on the offsets, (C2) strictly sorted rows and (C3) symmetry without loops for an undirected graph.

**Lemma 1 (offsets).** After line L3, $\mathit{off}[u] = \sum_{x < u} d(x)$ for $0 \le u \le n$. So (C1) holds and the row of $u$ has length $d(u)$.

*Proof.* After line L2, $\mathit{cnt}[x + 1] = d(x)$ for $0 \le x < n$, and $\mathit{cnt}[0] = 0$. Line L3 sets $\mathit{off}[0] = 0$ and $\mathit{off}[u] = \mathit{off}[u-1] + d(u-1)$, so by induction on $u$ the claim holds. Then $\mathit{off}[n] = \sum_x d(x) = M$, the offsets do not decrease, and $\mathit{off}[u+1] - \mathit{off}[u] = d(u)$. $\square$

**Lemma 2 (placement).** After lines L4 to L6, the row of each $u$ holds exactly the second ends of the pairs of $E$ with first end $u$, in the order in which these pairs occur in $E$.

*Proof.* We claim that before each step of the loop of line L5, for each $u$, $\mathit{pos}[u] = \mathit{off}[u] + k_u$, where $k_u$ is the number of pairs with first end $u$ processed so far, and the slots $\mathit{off}[u], \ldots, \mathit{pos}[u] - 1$ hold their second ends in order. This holds after line L4, with $k_u = 0$. A step on $(u, v)$ writes $v$ at slot $\mathit{pos}[u]$ and increases $\mathit{pos}[u]$ by 1, so the claim still holds. Since $k_u \le d(u)$ and the row of $u$ has $d(u)$ slots by Lemma 1, each write stays inside the row of $u$, so no write touches another row. At the end $k_u = d(u)$, so each row is full with its second ends in input order. The loop has $M$ steps, so it stops. $\square$

**Lemma 3 (sorting).** After line L7 each row is strictly increasing, so (C2) holds.

*Proof.* Line L7 is done by running lines L1 to L6 first with the second end as the key, which by Lemmas 1 and 2 lists the pairs in non-decreasing order of the second end, and then with the first end as the key on that list. By Lemma 2 the second pass places the pairs of each row in the order of the first list, which is non-decreasing in the second end. The pairs are distinct and have the same first end within a row, so their second ends are distinct, and the row is strictly increasing. $\square$

For an undirected graph the rows hold $v$ in the row of $u$ exactly when $(u, v) \in E$, which holds exactly when $(v, u) \in E$, and $E$ has no loop, so (C3) holds. So after BUILD, (C) holds and the stored graph is the graph given by $E$.

**Theorem.** With (C) holding, NEIGHBORS$(u)$ outputs the neighbours of $u$ in increasing order, DEGREE$(u)$ returns their number, and ADJACENT$(u, v)$ returns whether $v$ is a neighbour of $u$. Each of them stops.

*Proof.* NEIGHBORS reads exactly the row of $u$ in order, which by (C2) lists each neighbour once in increasing order. DEGREE returns the length of the row, which by (C2) is the number of distinct neighbours.

For ADJACENT, let $a = \mathit{off}[u]$ and $b = \mathit{off}[u+1]$, so the row is $\mathit{adj}[a \ldots b-1]$, sorted by (C2). We show that the loop of lines L11 to L13 keeps

> **(S)** $a \le \mathit{lo} \le \mathit{hi} \le b$, each entry at an index in $[a, \mathit{lo})$ is less than $v$, and each entry at an index in $[\mathit{hi}, b)$ is at least $v$.

Line L10 makes (S) true with both ranges empty. In a step, $\mathit{lo} \le \mathit{mid} < \mathit{hi}$. If $\mathit{adj}[\mathit{mid}] < v$, then since the row is sorted each entry at an index up to $\mathit{mid}$ is less than $v$, so setting $\mathit{lo} = \mathit{mid} + 1$ keeps (S). Otherwise $\mathit{adj}[\mathit{mid}] \ge v$, and each entry from $\mathit{mid}$ on is at least $v$, so setting $\mathit{hi} = \mathit{mid}$ keeps (S). Each step decreases $\mathit{hi} - \mathit{lo}$ by at least 1, so the loop stops, with $\mathit{lo} = \mathit{hi}$. Then by (S) the entries before $\mathit{lo}$ are less than $v$ and the entries from $\mathit{lo}$ on are at least $v$. If $v$ is in the row, its index is therefore $\mathit{lo}$, and line L14 returns true. If $v$ is not in the row, either $\mathit{lo} = b$ or $\mathit{adj}[\mathit{lo}] \ne v$, and line L14 returns false. $\blacksquare$
