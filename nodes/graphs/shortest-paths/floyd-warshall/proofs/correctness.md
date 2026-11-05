---
title: Floyd-Warshall computes all distances or detects a negative cycle
proves: [correctness, termination]
status: full
---

**Claim.** Let $G$ be a directed graph on the vertices $1, \ldots, n$ with real weights. At the end of FLOYD-WARSHALL:

1. each finite $D[i][j]$ is the weight of a walk from $i$ to $j$ (the empty walk when $i = j$ and $D[i][i] = 0$);
2. $D[i][j] \le w(p)$ for each path $p$ from $i$ to $j$ with $i \ne j$, and $D[i][i] \le \min(0, w(C))$ for each cycle $C$ through $i$ with no repeated vertex.

Consequently, if $G$ has no negative cycle, then $D[i][j] = \delta(i, j)$ for all $i, j$; and if $G$ has a negative cycle, then $D[i][i] < 0$ for some $i$. Also, $D[i][i] < 0$ for some $i$ only if $G$ has a negative cycle.

**Termination.** The loops have the fixed bounds $m$, then $n \cdot n \cdot n$, so the algorithm ends.

**Notation.** A path *inside* $K \subseteq V$ is a path from $i$ to $j$ whose inner vertices (all but the first and the last) are in $K$. A cycle through $i$ inside $K$ is a cycle with no repeated vertex other than its start and end $i$, whose other vertices are in $K$. Let $[k] = \{1, \ldots, k\}$.

**Invariant.** At the end of pass $k$ of line L3 ($k = 0$ means after line L2):

- **(W)** each finite $D[i][j]$ is the weight of a walk from $i$ to $j$;
- **(P)** $D[i][j] \le w(p)$ for each path $p$ from $i \ne j$ to $j$ inside $[k]$, and $D[i][i] \le \min(0, w(C))$ for each cycle $C$ through $i$ inside $[k]$.

**Base, $k = 0$.** Line L1 sets $D[i][i] = 0$, the empty walk, and $\infty$ elsewhere. Line L2 lowers $D[u][v]$ to the least weight of an edge from $u$ to $v$, a walk of one edge. A path inside $\emptyset$ from $i \ne j$ is one edge, and a cycle through $i$ inside $\emptyset$ is a self-loop; line L2 covers both, and $D[i][i] \le 0$ from line L1. So (W) and (P) hold.

**Maintenance, from $k - 1$ to $k$.** Entries only decrease in pass $k$, so (P) for paths and cycles inside $[k-1]$ stays true. Line L7 sets $D[i][j] = D[i][k] + D[k][j]$ with both terms finite (else the test of line L6 fails, with $\infty + x = \infty$). By (W), these are the weights of walks $i \leadsto k$ and $k \leadsto j$; joined, they form a walk $i \leadsto j$ of that weight. So (W) holds at each step of the pass.

For (P), take a path $p$ from $i$ to $j \ne i$ inside $[k]$ that passes through $k$ as an inner vertex (the paths that do not are inside $[k-1]$). Since $p$ repeats no vertex, it splits at $k$ into a path $p_1$ from $i$ to $k$ and a path $p_2$ from $k$ to $j$, both inside $[k-1]$. By (P) for $k - 1$, $D[i][k] \le w(p_1)$ and $D[k][j] \le w(p_2)$ at the start of pass $k$, and these entries can only be smaller when line L6 tests the pair $(i, j)$. After that test, $D[i][j] \le D[i][k] + D[k][j] \le w(p_1) + w(p_2) = w(p)$, and it only decreases later. The same split works for a cycle $C$ through $i$ inside $[k]$ that contains $k \ne i$: it splits into a path from $i$ to $k$ and a path from $k$ to $i$, both inside $[k-1]$, so after the test of the pair $(i, i)$, $D[i][i] \le w(C)$. If $k = i$, a cycle through $i$ inside $[k]$ has its other vertices in $[k-1]$, so it is already inside $[k-1]$. Thus (P) holds after pass $k$.

**At the end ($k = n$).** Every path and every cycle is inside $[n]$, so parts 1 and 2 of the claim hold.

*No negative cycle.* Then every closed walk has weight at least 0, because it splits into cycles. A walk from $i$ to $j$ therefore weighs at least $\delta(i, j)$, so (W) gives $D[i][j] \ge \delta(i, j)$. A shortest walk can be taken to be a path, since removing a closed sub-walk does not increase the weight, so (P) gives $D[i][j] \le \delta(i, j)$ for $i \ne j$. For $i = j$, $\delta(i, i) = 0$, and $0 \le D[i][i] \le 0$. So $D = \delta$.

*A negative cycle.* A closed walk of negative weight contains a cycle with no repeated vertex and negative weight, because a closed walk splits into such cycles and their weights add up to its weight. Let $C$ be such a cycle and $i$ a vertex of $C$. By part 2, $D[i][i] \le w(C) < 0$.

*Conversely,* if $D[i][i] < 0$, then by part 1 it is the weight of a closed walk from $i$ (not the empty one, which weighs 0), so a negative cycle exists. $\blacksquare$

**The next-hop matrix.** This proof covers the matrix $D$. The matching statement for the predecessor matrix, that it encodes shortest paths when no negative cycle exists, is proved in CLRS, Section 23.2, and the next-hop matrix is its mirror image.
