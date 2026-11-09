---
title: Hill climbing on n-bit strings can need 2^(n/2+1) - 2 moves
proves: [time.worst]
status: full
---

The bound of the page is $O(k N T)$ time for $k$ moves, where $N$ is the size of the largest neighborhood and $T$ the time to evaluate $f$ once. A pass of line L2 evaluates $f$ at most $|N(x)| \le N$ times, and there are $k + 1$ passes, so this part is direct. The real question is how large $k$ can be. On a set of $n$-bit strings with the flip neighborhood there are $2^n$ solutions, so $k \le 2^n - 1$. We show that $k$ can be exponential in $n$ for every pivoting rule, with a construction that is self-contained.

**Definitions.** The cube $Q_n$ has the vertex set $\{0,1\}^n$, and two strings are adjacent if they differ in one position. This is the flip neighborhood. A path $p_0, p_1, \ldots, p_\ell$ of distinct vertices with $p_{i}$ adjacent to $p_{i+1}$ is *induced* if no two of its vertices are adjacent except $p_i$ and $p_{i+1}$.

**Lemma (snake).** For each $j \ge 0$, the cube $Q_{2j}$ has an induced path with $2^{j+1} - 1$ vertices.

*Proof.* By induction on $j$. For $j = 0$, the single vertex of $Q_0$ (the empty string) is an induced path with $1 = 2^1 - 1$ vertex. Let $P = (p_0, \ldots, p_\ell)$ be an induced path in $Q_{2j}$ with $\ell + 1 = 2^{j+1} - 1$ vertices, and let $b = p_\ell$. In $Q_{2j+2}$ write a vertex as $(x, u, v)$ with $x \in \{0,1\}^{2j}$ and two more bits $u, v$. Define the path

$$P' = (p_0,0,0), \ldots, (p_\ell,0,0), \; (b,0,1), \; (p_\ell,1,1), (p_{\ell-1},1,1), \ldots, (p_0,1,1).$$

Consecutive vertices differ in one position: inside each copy because $P$ is a path, and at the joins $(b,0,0) \to (b,0,1) \to (b,1,1)$ in the bit $v$ and then the bit $u$. The vertices are distinct, since the two copies differ in $(u, v)$ and the middle vertex is the only one with $(u,v) = (0,1)$. It has $2(\ell + 1) + 1 = 2^{j+2} - 1$ vertices.

It is induced. Two vertices of the copy with $(u,v) = (0,0)$ are adjacent only if their first parts are adjacent in $Q_{2j}$, so only if they are consecutive on $P$, which makes them consecutive on $P'$. The same holds in the copy with $(1,1)$. A vertex $(x,0,0)$ and a vertex $(y,1,1)$ differ in both $u$ and $v$, so they are not adjacent. The middle vertex $(b,0,1)$ is adjacent to $(x,0,0)$ only if $x = b$, and to $(y,1,1)$ only if $y = b$. Both of these are its neighbors on $P'$. $\square$

**Theorem.** For each even $n = 2j$ there is an objective $f$ on $\{0,1\}^n$ and a start $x_0$ such that hill climbing with the flip neighborhood makes exactly $2^{j+1} - 2 = 2^{n/2+1} - 2$ moves, with every pivoting rule that moves only to a strictly better neighbor.

*Proof.* Take the induced path $p_0, \ldots, p_\ell$ of the lemma, with $\ell = 2^{j+1} - 2$. Set $f(p_i) = -i$, and $f(x) = 1$ for each $x$ not on the path. Start at $x_0 = p_0$. Let the current solution be $p_i$ with $i < \ell$. Its neighbors on the path are $p_{i-1}$ (if $i \ge 1$) and $p_{i+1}$, because the path is induced. All its other neighbors are off the path and have $f = 1 > -i$. So its only strictly better neighbor is $p_{i+1}$, with $f = -(i+1)$. Each rule moves there. At $p_\ell$ the neighbors are $p_{\ell-1}$, with a larger value, and points off the path, so $p_\ell$ is a local minimum and the search stops. The moves are $p_0 \to p_1 \to \cdots \to p_\ell$, which is $\ell$ moves. $\blacksquare$

**For natural problems.** The function above is artificial. For a problem whose objective is given by an instance of polynomial size, the same kind of result holds: Schäffer and Yannakakis (1991) built weighted graphs and start cuts for Max-Cut with the flip neighborhood from which every sequence of improving flips is exponentially long in the number of vertices. For the 2-opt neighborhood of the traveling salesman problem, Englert, Röglin and Vöcking (2014) built Euclidean instances in the plane on which 2-opt can make exponentially many moves. These results are proved in the cited papers and are not reproved here.
