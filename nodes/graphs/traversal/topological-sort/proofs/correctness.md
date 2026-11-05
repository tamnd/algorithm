---
title: DFS topological sort returns a topological ordering or finds a cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph with $n$ vertices. We say that VISIT$(u)$ is *active* from line L6 to line L11. A call that starts while another call is active ends before that call ends, as on any call stack.

**Lemma 1 (DFS structure).** Up to the moment the run stops, TOPOLOGICAL-SORT is the procedure DFS of the [depth-first search](/depth-first-search/) page without the clock and the parents, with line L6 as the discovery of $u$ and lines L10 and L11 as its finish. So each vertex is visited at most once, a vertex is white before its visit, gray while it is active and black after it, and the gray vertices at each moment form a path $g_1, \ldots, g_k$ in which $g_{i+1}$ was visited from the loop of $g_i$ through the edge $(g_i, g_{i+1})$.

*Proof.* Line L8 only reads colours and may stop the run, and line L11 only changes $L$. Removing both gives DFS without the clock and the parents. The facts are Lemmas 1 and 2 of the correctness proof of DFS, which hold for each prefix of the run. $\square$

**Lemma 2 (stop means cycle).** If line L8 stops the run while VISIT$(u)$ scans the edge $(u, v)$, then $G$ has a directed cycle.

*Proof.* The vertex $v$ is gray, so by Lemma 1 it is one of $g_1, \ldots, g_k$, and $u = g_k$ is the top of the gray path, because the call of $u$ is the one that runs. If $v = g_i$, then $g_i, g_{i+1}, \ldots, g_k$ are joined by edges, and $(g_k, g_i) = (u, v)$ is an edge. This is a directed cycle. If $i = k$, it is the self-loop $(u, u)$. $\square$

**Lemma 3 (cycle means stop).** If $G$ has a directed cycle, line L8 stops the run.

*Proof.* Assume that the run does not stop. Then by Lemma 1 it is a full DFS of $G$, so it visits each vertex. Let $C$ be a directed cycle and let $x$ be the vertex of $C$ whose visit starts first, and let $w$ be the vertex before $x$ on $C$, so $(w, x) \in E$. Just before VISIT$(x)$ starts, all the vertices of $C$ are white, so the path along $C$ from $x$ to $w$ is white. By the [white-path theorem](/white-path-theorem/), applied to this DFS, $w$ is a descendant of $x$. So the visit of $w$ is active while the visit of $x$ is active. The visit of $w$ scans the edge $(w, x)$ before it ends, and at that moment $x$ is gray. Then line L8 stops the run. This contradicts the assumption. (If $w = x$, the edge is a self-loop, and the scan of $x$ finds $x$ gray at once.) $\square$

**Lemma 4 (edges in $L$).** If the run does not stop, then for each edge $(u, v) \in E$, line L11 runs for $v$ before it runs for $u$.

*Proof.* Look at the moment when VISIT$(u)$ scans $(u, v)$ at line L7. The run does not stop, so $v$ is not gray at line L8. If $v$ is black, line L11 has already run for $v$, because line L11 directly follows line L10. Line L11 for $u$ comes later, after the loop of $u$ ends. If $v$ is white, line L9 calls VISIT$(v)$, and that call ends, with line L11 for $v$, before the loop of $u$ goes on. So again line L11 for $v$ runs first. $\square$

**Theorem.** TOPOLOGICAL-SORT terminates. If $G$ is acyclic, it returns a topological ordering of $G$. If $G$ has a directed cycle, it reports a cycle.

*Proof.* Termination: each vertex is visited at most once, each visit runs a finite loop, and the loop of line L3 is finite.

If $G$ has a directed cycle, Lemma 3 shows that the run stops at line L8 and reports a cycle.

If $G$ is acyclic, Lemma 2 shows that line L8 never stops the run. By Lemma 1 the run is a full DFS, so each vertex is visited exactly one time, and line L11 inserts it at the front of $L$ exactly one time. So $L$ holds each vertex once, and the vertex inserted last is first. For each edge $(u, v)$, Lemma 4 says that $v$ is inserted before $u$, so $u$ is in front of $v$ in the returned list. So $L$ is a topological ordering.

The two cases cover all graphs, and the report is correct in each, so the procedure is correct. In the acyclic case, line L11 runs in increasing order of the finish times of the DFS, so $L$ lists the vertices in decreasing order of $f$. $\blacksquare$
