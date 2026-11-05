---
title: Greedy coloring returns a proper coloring with at most Δ + 1 colors
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph and $\sigma = (v_1, \ldots, v_n)$ an order of $V$. For a vertex $v = v_i$, let $N^-(v) = \{ w : \{v, w\} \in E,\ w = v_j \text{ with } j < i \}$ be the set of its earlier neighbors, and $d^-(v) = |N^-(v)|$. The array $\mathrm{used}$ has the indices $1$ to $n + 1$ and starts with a value that is not a vertex.

**Claim.** GREEDY-COLORING$(G, \sigma)$ stops. The returned $c$ satisfies $1 \le c(v) \le d^-(v) + 1$ for each $v$, and $c(u) \ne c(v)$ for each edge $\{u, v\}$.

**Invariant.** At the start of iteration $i$ of the loop of line L2:

> **(G)** $c(v_j) \ge 1$ for each $j < i$, $c(v_j) = 0$ for each $j \ge i$, and no edge joins two vertices $v_j, v_l$ with $j, l < i$ and $c(v_j) = c(v_l)$.

*Initialization.* For $i = 1$, line L1 set all colors to 0, and there is no pair with $j, l < 1$.

*Maintenance.* Fix iteration $i$ and $v = v_i$. By (G), the neighbors $w$ of $v$ with $c(w) > 0$ are exactly the vertices of $N^-(v)$. Line L4 writes the stamp $v$ at the index $c(w)$ for each of them. No other entry holds the stamp $v$: an entry gets a stamp only in line L4, and the iterations before $i$ wrote other vertices as stamps, because each vertex appears once in $\sigma$. So after line L4,

$$\{ k : \mathrm{used}[k] = v \} = C(v) := \{ c(w) : w \in N^-(v) \}.$$

The set $C(v)$ has at most $d^-(v)$ elements. So among the $d^-(v) + 1$ values $1, \ldots, d^-(v) + 1$, at least one is not in $C(v)$. As $d^-(v) + 1 \le n$, these values are valid indices. The loop of line L6 starts at $k = 1$, adds 1 in each step, and stops at the first $k \notin C(v)$. So it stops after at most $d^-(v) + 1$ tests, with $1 \le k \le d^-(v) + 1$ and $k \notin C(v)$. Line L7 sets $c(v) = k$.

Now $v$ has a color of at least 1, and the vertices $v_{i+1}, \ldots, v_n$ are still at 0. A new edge between two colored vertices is an edge $\{v, w\}$ with $w \in N^-(v)$, and $c(w) \in C(v)$ while $c(v) \notin C(v)$, so $c(v) \ne c(w)$. Edges between earlier vertices keep their colors, which differ by (G). So (G) holds at the start of iteration $i + 1$.

*Termination.* The loop of line L2 runs $n$ times, and each loop of line L6 runs at most $d^-(v) + 1$ times, as shown. When the loop of line L2 ends, (G) with $i = n + 1$ says that each vertex has a color of at least 1 and that each edge joins two vertices of different colors. The bound $c(v) \le d^-(v) + 1$ was shown in the maintenance step, and $d^-(v) \le \deg(v) \le \Delta$. $\blacksquare$
