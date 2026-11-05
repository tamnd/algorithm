---
title: BUILD-FROM-CSR makes a valid compressed sparse column array and the queries answer for the stored graph
proves: [correctness, termination]
status: full
---

Let $G$ be a directed graph on $\{0, \ldots, n-1\}$ with $m$ distinct edges, given by CSR arrays $\mathit{off}$ and $\mathit{adj}$: the row $\mathit{adj}[\mathit{off}[u] \ldots \mathit{off}[u+1] - 1]$ lists the heads of the edges out of $u$, each once, and $\mathit{off}[n] = m$. Write $d^-(v)$ for the number of edges into $v$. The CSC arrays stand for the graph with an edge $(u, v)$ for each $u$ in the column $\mathit{src}[\mathit{coff}[v] \ldots \mathit{coff}[v+1] - 1]$. The invariant (K) is (K1) on the offsets and (K2) strictly sorted columns.

**Lemma 1 (offsets).** After line L3, $\mathit{coff}[v] = \sum_{x < v} d^-(x)$ for $0 \le v \le n$. So (K1) holds and the column of $v$ has $d^-(v)$ slots.

*Proof.* Line L2 reads each of the $m$ entries of $\mathit{adj}$ once, and each entry is the head of one edge, so afterwards $\mathit{cnt}[x + 1] = d^-(x)$. Line L3 then computes the prefix sums, so the claim follows by induction on $v$, with $\mathit{coff}[n] = \sum_x d^-(x) = m$ and $\mathit{coff}[v+1] - \mathit{coff}[v] = d^-(v) \ge 0$. $\square$

**Lemma 2 (placement).** After lines L5 to L7, the column of each $v$ holds exactly the tails of the edges into $v$, in increasing order.

*Proof.* Lines L5 and L6 visit the CSR entries row by row, for $u = 0, 1, \ldots, n-1$, so they visit each edge $(u, v)$ once, in non-decreasing order of $u$. We claim that before each visit, for each $v$, $\mathit{pos}[v] = \mathit{coff}[v] + k_v$, where $k_v$ is the number of edges into $v$ visited so far, and the slots $\mathit{coff}[v], \ldots, \mathit{pos}[v] - 1$ hold their tails in the order of the visits. This holds after line L4 with $k_v = 0$, and line L7 keeps it by writing $u$ at slot $\mathit{pos}[v]$ and increasing $\mathit{pos}[v]$. Since $k_v \le d^-(v)$, each write stays within the column of $v$ by Lemma 1. At the end $k_v = d^-(v)$, so each column is full and holds exactly the tails of the edges into $v$, in the order of the visits, which is non-decreasing in $u$. The edges are distinct, so two edges into $v$ have different tails, and the column is strictly increasing. The loops run over $n$ rows and $m$ entries, so they stop. $\square$

So after BUILD-FROM-CSR, (K) holds and the stored graph is $G$.

**Theorem.** With (K) holding, IN-NEIGHBORS$(v)$ outputs the tails of the edges into $v$ in increasing order, IN-DEGREE$(v)$ returns $d^-(v)$, and ADJACENT$(u, v)$ returns whether $(u, v)$ is an edge. Each of them stops.

*Proof.* IN-NEIGHBORS reads exactly the column of $v$, which by Lemma 2 is the sorted list of the tails. IN-DEGREE returns the length of the column, which is $d^-(v)$ by Lemma 1.

For ADJACENT, let $a = \mathit{coff}[v]$ and $b = \mathit{coff}[v+1]$. The loop of lines L11 to L13 keeps the condition that $a \le \mathit{lo} \le \mathit{hi} \le b$, each entry of the column at an index in $[a, \mathit{lo})$ is less than $u$, and each entry at an index in $[\mathit{hi}, b)$ is at least $u$. Line L10 makes it true with empty ranges. In a step, $\mathit{lo} \le \mathit{mid} < \mathit{hi}$; if $\mathit{src}[\mathit{mid}] < u$ then, as the column is sorted, all entries up to $\mathit{mid}$ are less than $u$, and $\mathit{lo} \leftarrow \mathit{mid} + 1$ keeps the condition; otherwise all entries from $\mathit{mid}$ on are at least $u$, and $\mathit{hi} \leftarrow \mathit{mid}$ keeps it. Each step shrinks $\mathit{hi} - \mathit{lo}$, so the loop stops with $\mathit{lo} = \mathit{hi}$. Then $u$, if it is in the column, can only be at index $\mathit{lo}$, so line L14 returns true exactly when $u$ is in the column of $v$, that is, when $(u, v)$ is an edge. $\blacksquare$
