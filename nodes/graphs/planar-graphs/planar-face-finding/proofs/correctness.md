---
title: Face tracing outputs each cycle of the face permutation exactly once
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph with a rotation system $\rho$, and let $D = \{(u, v), (v, u) : uv \in E\}$ be its set of $2m$ darts. For a vertex $b$ of degree $k \ge 1$ write $\rho_b = (\rho_b[0], \ldots, \rho_b[k-1])$, read cyclically, and let pos$[(b, a)]$ be the index of $a$ in $\rho_b$. Define

$$\varphi(a, b) = \big(b, \rho_b[(\text{pos}[(b, a)] - 1) \bmod k]\big),$$

which is exactly the dart computed by lines L8 and L9.

**Lemma 1 ($\varphi$ is a permutation of $D$).** Define $\psi(b, w) = (a, b)$ with $a = \rho_b[(\text{pos}[(b, w)] + 1) \bmod k]$. Both maps send darts to darts: $\varphi(a, b)$ is a dart because $\rho_b[j]$ is a neighbour of $b$ for each $j$. For each dart $(a, b)$, $\psi(\varphi(a, b)) = (a, b)$, because the index of $\varphi(a,b)$'s head in $\rho_b$ is pos$[(b, a)] - 1$, and adding 1 gives back $a$. Likewise $\varphi(\psi(b, w)) = (b, w)$. So $\varphi$ is a bijection of the finite set $D$. $\square$

Hence $D$ is the disjoint union of the cycles of $\varphi$: for each $d \in D$ there is a least $k \ge 1$ with $\varphi^k(d) = d$, and the cycle of $d$ is $C(d) = \{d, \varphi(d), \ldots, \varphi^{k-1}(d)\}$, with $k$ distinct elements.

**Lemma 2 (one walk is one whole cycle).** Suppose that at line L5 the start dart $d_0$ is not visited, and that every visited dart lies in a cycle that is disjoint from $C(d_0)$. Then the loop of lines L6 to L9 visits exactly the darts $d_0, \varphi(d_0), \ldots, \varphi^{k-1}(d_0)$ in this order, appends their tails to $W$, and stops.

*Proof.* Invariant at the test of line L6, after $j$ iterations with $0 \le j \le k$: $d = \varphi^{j}(d_0)$, the darts $\varphi^0(d_0), \ldots, \varphi^{j-1}(d_0)$ are visited and are the last $j$ darts marked, and $W$ holds their tails in order. It holds for $j = 0$. If $j < k$, then $\varphi^{j}(d_0)$ is in $C(d_0)$ and differs from the $j$ darts of the cycle visited so far, and it was not visited before the walk by the hypothesis. So the test succeeds, line L7 marks it and appends its tail, and line L9 sets $d = \varphi^{j+1}(d_0)$. If $j = k$, then $d = \varphi^k(d_0) = d_0$, which line L7 marked in the first iteration, so the loop stops. $\square$

**Theorem (correctness and termination).** FACES$(\rho)$ stops after exactly $2m$ iterations of line L7, and the list $F$ it returns contains each cycle of $\varphi$ exactly once, as the sequence of tails of its darts in the order of $\varphi$.

*Proof.* We show by induction over the iterations of the loop of line L3 that, at the start of each iteration, the visited set is the union of the cycles already appended to $F$, and that these cycles are distinct.

At the start, both are empty. Consider the iteration for the dart $(u, v)$. If $(u, v)$ is visited, line L4 skips it and nothing changes. If not, then by the induction hypothesis the visited darts form whole cycles that do not contain $(u, v)$; since cycles are disjoint, none of them meets $C((u, v))$. Lemma 2 applies: the walk appends exactly $C((u, v))$, a cycle not yet in $F$, and the visited set becomes the union of the old cycles and this one. So the statement holds after the iteration.

Each dart of $D$ is taken once by line L3. At the end, every dart was either visited before its turn or started a walk, so every dart is visited, and the visited set, which is the union of the cycles in $F$, is all of $D$. Since the cycles in $F$ are distinct and cover $D$, $F$ contains each cycle exactly once. Line L7 marks each dart once, so it runs exactly $2m$ times, and line L3 runs $2m$ times; the algorithm stops. $\square$

**Faces of a drawing.** Suppose now that $\rho$ is read from a straight-line planar drawing, with $\rho_v$ in counterclockwise order. Fix a vertex $b$ and a disc $B$ around $p_b$ so small that it meets only the segments at $b$ and no other vertex. The segments at $b$ cut $B$ into $\deg b$ open sectors, one between each pair of rays that are consecutive in $\rho_b$, and each sector lies in one face. Let a walk arrive at $b$ along the dart $(a, b)$. Put $p_b$ at the origin with the ray to $a$ pointing in the direction of angle 0. Walking from $p_a$ toward $p_b$ moves in the direction of angle $\pi$, and its left side is the side of angles just below $0$, which is the sector between the ray to $a$ and the next ray clockwise. That next ray goes to the neighbour $w$ just before $a$ in the counterclockwise order $\rho_b$, so the sector is the one between the rays to $w$ and to $a$. Leaving along $(b, w)$, the left side is the side just counterclockwise of the ray to $w$, which is the same sector. So the face on the left of $(a, b)$ near $p_b$ is also on the left of $\varphi(a, b)$. By induction along a cycle, all darts of one cycle of $\varphi$ have the same face on their left. Conversely, each face of a connected plane graph has a boundary that is one closed walk (Mohar and Thomassen, Chapters 3 and 4), so it is the face on the left of exactly one cycle of $\varphi$. Therefore, for a connected drawing, the walks in $F$ are the face boundaries, one for each face. $\blacksquare$
