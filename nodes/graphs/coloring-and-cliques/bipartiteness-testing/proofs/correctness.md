---
title: Bipartiteness testing returns a 2-coloring or an odd cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be an undirected graph, with self-loops and parallel edges allowed. A self-loop at $v$ puts $v$ in its own adjacency list. For a search started at $s$ in line L3, let $\delta(s, v)$ be the number of edges of a shortest path from $s$ to $v$.

**Lemma 1 (layers).** Consider the search from $s$, lines L3 to L8, and suppose it runs to the end without a return. Then each vertex $v$ reachable from $s$ gets a color, $\mathrm{color}[v] = \delta(s, v) \bmod 2$, and for $v \ne s$, $\mathrm{parent}[v]$ is a neighbor of $v$ with $\delta(s, \mathrm{parent}[v]) = \delta(s, v) - 1$. The same holds, up to the moment of a return at line L8, for every vertex colored so far.

*Proof.* Lines L3 to L8 are the breadth-first search of the page on [breadth-first search](/breadth-first-search/), with $\mathrm{color}[v] \ne \mathrm{NIL}$ in the role of "discovered", and with an extra test at line L8 that only adds a return. That page proves that BFS discovers each reachable vertex, sets $\mathrm{dist}[w] = \mathrm{dist}[u] + 1$ when it discovers $w$ from $u$, and ends with $\mathrm{dist}[v] = \delta(s, v)$; the values set before any time are already final. Line L7 sets $\mathrm{color}[w] = 1 - \mathrm{color}[u]$ at the same moment, so by induction on the order of discovery, $\mathrm{color}[v] = \mathrm{dist}[v] \bmod 2 = \delta(s, v) \bmod 2$, and $\mathrm{parent}[w] = u$ is a neighbor with distance one less. $\square$

**Lemma 2 (edges).** For each edge $\{u, w\}$ with $u$ reachable from $s$, $|\delta(s, u) - \delta(s, w)| \le 1$.

*Proof.* A shortest path to $u$ followed by the edge is a walk to $w$, so $\delta(s, w) \le \delta(s, u) + 1$; by symmetry $\delta(s, u) \le \delta(s, w) + 1$. $\square$

**Theorem.** BIPARTITE-TEST stops. If it returns at line L9, $\mathrm{color}$ is a proper 2-coloring. If it returns at line L8 with the vertices $u$ and $w$, the output $C$ is a list of vertices of odd length in which each two consecutive vertices, and the last and the first, are adjacent; when $u \ne w$ the vertices of $C$ are distinct, so $C$ is a simple cycle of odd length. So line L9 is reached if and only if $G$ is bipartite.

*Proof.*

*Termination.* Each vertex is enqueued at most once, because line L7 enqueues only a vertex with color NIL and gives it a color at once, and line L3 starts a search only from a vertex with color NIL. So the loops of lines L4 and L6 make at most $n$ and $2m + (\text{number of loops})$ steps in total. The climb of line L10 stops by the argument below.

*Return at line L9.* Let $\{u, w\}$ be an edge. Both ends are in the same component, so they get colors in the same search. When the later of the two, say $u$, is dequeued at line L5, line L6 scans $w$, which already has a color (or gets one at line L7 from $u$, which is the opposite color). If $w$ had the color of $u$, line L8 would have returned. Colors never change after they are set. So at the end $\mathrm{color}[u] \ne \mathrm{color}[w]$ for each edge, and each vertex has a color because the loop of line L2 starts a search at each uncolored vertex. So $\mathrm{color}$ is a proper 2-coloring.

*Return at line L8.* The return happens while the search from some $s$ runs, with $u$ dequeued, $w$ a neighbor of $u$ with a color, and $\mathrm{color}[w] = \mathrm{color}[u]$. Both $u$ and $w$ were colored in this search, as $w$ is adjacent to $u$. By Lemma 1 their colors are the parities of $\delta(s, u)$ and $\delta(s, w)$, which are therefore equal mod 2. By Lemma 2 these distances differ by at most 1, so they are equal: $\delta(s, u) = \delta(s, w) = h$.

If $u = w$ (a self-loop), line L10 does not climb and $C = (u)$, of length 1, closed by the loop. Otherwise, by Lemma 1, each parent step lowers the distance by exactly 1. So after $j$ steps, $x$ and $y$ are both at distance $h - j$. When $j = h$, both are at distance 0, so both are $s$, and the loop of line L10 stops after at most $h$ steps. Let $j^* \le h$ be the first $j$ with $x = y$, and $z$ that vertex. The path $P$ from $u$ up to $z$ and the path $Q$ from $w$ up to $z$ have $j^*$ edges each, and their vertices have distinct distances along each path. They share only $z$: a common vertex $x_i = y_k$ has $h - i = h - k$, so $i = k$, and $i < j^*$ would contradict the choice of $j^*$. Line L11 lists $P$ from $u$ to $z$, then $Q$ from $z$ back to $w$, which is $2 j^* + 1$ distinct vertices, with consecutive vertices joined by tree edges, and $w$ joined to $u$ by the edge that triggered line L8. The length is odd. ($j^* \ge 1$ because $u \ne w$.)

*The final claim.* If line L9 is reached, $G$ has a proper 2-coloring, so it is bipartite. If line L8 is reached, $G$ has a closed walk of odd length. Along it a 2-coloring would have to switch color at each of an odd number of steps and return to the start color, which is impossible. So $G$ is not bipartite. $\blacksquare$
