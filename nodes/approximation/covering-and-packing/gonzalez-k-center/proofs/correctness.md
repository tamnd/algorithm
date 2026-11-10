---
title: Farthest-first traversal returns at most k centers of radius at most 2 OPT
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a finite set $V$ of $n$ points with a metric $d$ and an integer $k \ge 1$. For a set $C$ of points and a point $v$ we write $d(v, C) = \min_{c \in C} d(v, c)$, and $r(C) = \max_{v \in V} d(v, C)$ is the radius of $C$. $\mathrm{OPT}$ is the least radius of a set of at most $k$ points. The proof uses the lower bound on $\mathrm{OPT}$ that comes from $k + 1$ points that are pairwise far apart.

**Lemma 1 (the array).** At the start of each pass of line L3, and when line L8 runs, the set $C$ of chosen centers satisfies $D[v] = d(v, C)$ for each $v \in V$.

*Proof.* After lines L1 and L2, $C = \{c_1\}$ and $D[v] = d(v, c_1) = d(v, C)$. When line L6 adds $c$ to $C$, line L7 replaces $D[v]$ by $\min(D[v], d(v, c))$, and $\min(d(v, C), d(v, c)) = d(v, C \cup \{c\})$. A pass that stops at line L5 does not change $C$ or $D$. $\square$

So line L8 returns $C$ together with its true radius $r = r(C)$. The centers are distinct: a point $c$ that is already in $C$ has $D[c] = 0$, and line L6 adds a point only if line L5 found its value positive. So $|C| \le k$.

**Lemma 2 (far apart).** Let $C = \{c_1, \ldots, c_t\}$ be the output, in the order of choice, with radius $r$. Then $d(c_i, c_j) \ge r$ for all $i < j$.

*Proof.* Let $D_j$ be the array at the moment line L4 chooses $c_j$; it holds the distances to $\{c_1, \ldots, c_{j-1}\}$ by Lemma 1, and $c_j$ has the largest value. So $d(c_i, c_j) \ge D_j[c_j] = \max_v D_j[v]$. The values of the array never grow, so $\max_v D_j[v] \ge \max_v D[v] = r$ for the final array $D$. $\square$

**Theorem.** The output $C$ has at most $k$ points and $r(C) \le 2\,\mathrm{OPT}$.

*Proof.* If $r = 0$, then $r \le 2\,\mathrm{OPT}$. Let $r > 0$. Then no pass stopped at line L5, because a pass stops only when the largest value is 0, and the values never grow. So $C = \{c_1, \ldots, c_k\}$ has $k$ points. Let $f$ be a point with $d(f, C) = r$. Then $d(f, c_i) \ge r$ for each $i$, and with Lemma 2 the $k + 1$ points $c_1, \ldots, c_k, f$ have pairwise distances at least $r > 0$; in particular they are distinct.

Take an optimal set $C^*$ with $|C^*| \le k$ and $r(C^*) = \mathrm{OPT}$. Assign each of the $k + 1$ points to a nearest point of $C^*$. By the pigeonhole principle, two of them, $u$ and $v$, go to the same $c^* \in C^*$. By the triangle inequality,

$$r \le d(u, v) \le d(u, c^*) + d(c^*, v) \le 2\,\mathrm{OPT}. \qquad \blacksquare$$

The proof does not use the choice of the first center or the way ties are broken, so the bound holds for each such choice.

**Prefixes.** For each $i \le t$, the first $i$ centers have radius at most $2\,\mathrm{OPT}_i$, where $\mathrm{OPT}_i$ is the optimum with $i$ centers. *Proof.* The algorithm with input $i$ in place of $k$ makes the same choices in the same order, so it returns exactly $c_1, \ldots, c_i$, and the theorem applies to it. $\square$

**Tightness.** Take $V = \{-1, 0, 1\}$ on a line and $k = 1$. The center $0$ gives $\mathrm{OPT} = 1$. If line L1 picks $c_1 = -1$, the radius is $d(-1, 1) = 2 = 2\,\mathrm{OPT}$. For a general $k$, add the points $100, 200, \ldots, 100(k-1)$. Then $\mathrm{OPT} = 1$, with the center $0$ and each new point as its own center. From $c_1 = -1$, each new point has distance at least 100 to the centers until it is chosen, so the passes of line L3 choose the $k - 1$ new points, and the point 1 is left at distance 2. So the factor 2 cannot be improved for this algorithm, and by the theorem of Hsu and Nemhauser it cannot be improved by any polynomial-time algorithm unless P = NP.
