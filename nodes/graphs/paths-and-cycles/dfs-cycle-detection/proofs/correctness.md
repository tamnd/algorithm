---
title: DFS-CYCLE returns a cycle if and only if the graph has one
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ have $n$ vertices and $m$ edges, directed or undirected, with parallel edges and self-loops allowed. We use the facts proved for [depth-first search](/depth-first-search/): each vertex goes from white to gray to black, VISIT runs at most once for each vertex, and a call that starts while another call is active ends before it. The extra line L8 only stops the run early, so these facts hold until the run stops.

**Termination.** VISIT$(u)$ is called only when $u$ is white, and line L6 makes it gray, so there are at most $n$ calls, each with a finite loop. CYCLE stops by Lemma 1 below. So DFS-CYCLE stops.

**Lemma 1 (the gray path).** At each moment, let $g_1, \ldots, g_k$ be the gray vertices in the order in which they became gray. Then $g_1$ was called at line L4, and for $1 \le i < k$, $pe[g_{i+1}]$ is an edge from $g_i$ to $g_{i+1}$. The vertex whose loop runs now is $g_k$.

*Proof.* The gray vertices are the vertices with an active call, and the active calls form the call stack, with $g_1$ at the bottom and $g_k$ at the top. The bottom call comes from line L4. For $i < k$, the call of $g_{i+1}$ was made at line L9 in the loop of $g_i$, the call just below it, while scanning a pair $(e, g_{i+1}) \in \mathrm{Out}[g_i]$, and line L9 set $pe[g_{i+1}] = e$. So $e$ goes from $g_i$ to $g_{i+1}$. $\square$

**Lemma 2 (the output is a cycle).** If line L8 returns CYCLE$(e, u, v)$, the result is a cycle.

*Proof.* At that moment $u = g_k$ by Lemma 1, and $v = g_j$ for some $j \le k$, because $v$ is gray. Starting at $x = g_k$, each step of line L12 sets $x$ to the tail of $pe[x]$, which is $g_{i-1}$ when $x = g_i$. So the loop runs $k - j$ times, stops at $x = g_j = v$, and $C = (pe[g_{j+1}], \ldots, pe[g_k], e)$. This walk goes $g_j \to g_{j+1} \to \cdots \to g_k \to g_j$. Its vertices $g_j, \ldots, g_k$ are distinct. Its tree edges are distinct, because each one was the discovery edge of a different vertex.

It remains to see that $e$ is not one of the tree edges. If $j = k$, then $C = (e)$, and $e$ goes from $u$ to $u$, so it is a self-loop and the walk is a cycle of length 1. If $j < k$, then $e$ starts at $g_k$. In the directed case each tree edge $pe[g_{i+1}]$ starts at $g_i \ne g_k$, so $e$ is not a tree edge. In the undirected case, among the tree edges of the walk only $pe[g_k]$ has $g_k$ as an end, because $pe[g_{i+1}]$ joins $g_i$ and $g_{i+1}$. Line L7 skips $pe[g_k]$ in the loop of $g_k$, so $e \ne pe[g_k]$. If $j = k - 1$, the walk is $g_{k-1} \to g_k \to g_{k-1}$ along two different edges, which is a cycle of length 2. In all cases the edges of $C$ are distinct and the vertices $g_j, \ldots, g_k$ are distinct, so $C$ is a cycle. $\square$

**Lemma 3 (directed: a cycle is found).** If $G$ is directed and has a cycle, DFS-CYCLE does not return NIL.

*Proof.* Suppose it returns NIL. Then line L8 never fired, so every vertex was visited and every list was scanned in full. Let $Z$ be a cycle of $G$ and let $v$ be the vertex of $Z$ that became gray first. At that moment, all other vertices of $Z$ are white, so $Z$ minus its last edge is a path of white vertices from $v$ to the vertex $w$ whose edge $f$ goes to $v$. By the white-path theorem, $w$ becomes gray during the call of $v$ (if $w = v$, the edge $f$ is a self-loop). While the call of $w$ runs, the call of $v$ is still active, so $v$ is gray, and the loop of $w$ scans $f$ before the call of $w$ ends. At that scan, line L8 sees $v$ gray and returns. This contradicts the assumption. $\square$

**Lemma 4 (undirected: a cycle is found).** If $G$ is undirected and has a cycle, DFS-CYCLE does not return NIL.

*Proof.* Suppose it returns NIL, so every list was scanned in full. Take any edge $e$ that is not a tree edge, with ends $a$ and $b$, and say $a$ became gray no later than $b$. If $e$ is a self-loop at $a$, its scan from $a$ sees $a$ gray and returns, a contradiction. Otherwise, consider the scan of $e$ in the loop of $a$. If $b$ is white then, line L9 makes $e$ the tree edge $pe[b]$, a contradiction. If $b$ is gray then, line L8 returns, a contradiction. If $b$ is black then, $b$ became gray and black while $a$ was gray, so the loop of $b$ scanned $e$ while $a$ was gray. That scan was not skipped, since $e$ is not a tree edge, and line L8 returns, a contradiction. So every edge is a tree edge. Tree edges form a forest (Lemma 3 of the depth-first search proof), so $G$ is a forest and has no cycle. $\square$

**Theorem.** DFS-CYCLE stops. It returns a list of edges that forms a cycle if $G$ has a cycle, and it returns NIL if $G$ has none. It works on directed and undirected multigraphs with self-loops.

*Proof.* Termination is shown above. If the run returns a list, the list comes from line L8 and is a cycle by Lemma 2, so $G$ has a cycle. If it returns NIL, then $G$ has no cycle by Lemma 3 in the directed case and Lemma 4 in the undirected case. $\blacksquare$
