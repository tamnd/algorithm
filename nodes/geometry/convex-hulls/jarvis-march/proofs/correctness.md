---
title: The Jarvis march returns the hull vertices in counterclockwise order
proves: [correctness, termination]
status: full
---

**Claim.** Let $S$ be the set of distinct points after line L1, with $|S| \ge 2$, and let $h$ be the number of extreme points of $S$. JARVIS-MARCH stops after exactly $h$ iterations of the loop of line L5 and returns the extreme points of $S$, each once, in counterclockwise order, starting at the lexicographically smallest point. (If $S$ is collinear, $h = 2$ and the output is the two end points.)

**Notation.** $\mathrm{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, with $u \times w = u_x w_y - u_y w_x$. For a directed pair $(p, q)$ of distinct points of $S$, call $(p, q)$ a **hull edge** if every $r \in S$ has $\mathrm{orient}(p, q, r) \ge 0$, and every $r$ with $\mathrm{orient}(p, q, r) = 0$ lies on the closed segment $pq$.

**Lemma 1 (successor).** Let $p$ be an extreme point of $S$. Then there is exactly one $q \in S$ such that $(p, q)$ is a hull edge, $q$ is an extreme point, and walking from each extreme point to its successor visits the $h$ extreme points in counterclockwise order around $\operatorname{conv} S$ and returns to the start after $h$ steps.

*Proof.* If $S$ is collinear, its extreme points are its two end points $a$ and $b$. From $a$, only $q = b$ has all points on the segment $aq$; from $b$, only $q = a$. So the walk is $a, b, a$ with $h = 2$. Otherwise $\operatorname{conv} S$ is a convex polygon with vertices $w_0, \ldots, w_{h-1}$ in counterclockwise order, $h \ge 3$, and its edges are the segments $w_i w_{i+1}$ (indices modulo $h$). For $p = w_i$ the pair $(w_i, w_{i+1})$ is a hull edge: the line through it supports the polygon with the polygon on its left, and the points of $S$ on the line lie in the polygon's boundary segment $w_i w_{i+1}$. No other $q$ works: if $(w_i, q)$ is a hull edge, then the line from $w_i$ through $q$ supports the polygon, so it contains one of the two polygon edges at $w_i$, and with the polygon on its left it is the line of $w_i w_{i+1}$. Then $q$ lies on that line on the segment, and since $w_{i+1}$ lies on the closed segment $w_i q$ by the definition, $q = w_{i+1}$. $\square$

**Lemma 2 (the scan of line L8).** Let $p$ be an extreme point of $S$. After the loop of lines L8 and L9, $q$ is the successor of $p$ from Lemma 1.

*Proof.* Since $p$ is extreme, there is a direction $u$ such that $p$ is the only maximizer of $\langle u, \cdot \rangle$ on $S$. Every $r \in S \setminus \{p\}$ then satisfies $\langle u, r - p \rangle < 0$, so all the vectors $r - p$ lie in an open half-plane, and their angles, measured from the direction $u$ turned by a right angle, lie in an open interval of length $\pi$. For $r, r'$ with angles $\phi(r), \phi(r')$ in this interval, $(r - p) \times (r' - p) = |r - p|\,|r' - p| \sin(\phi(r') - \phi(r))$ with $\phi(r') - \phi(r) \in (-\pi, \pi)$. So $\mathrm{orient}(p, q, r) < 0$ holds exactly when $\phi(r) < \phi(q)$, and $\mathrm{orient}(p, q, r) = 0$ exactly when $\phi(r) = \phi(q)$, that is, when $r$ is on the ray from $p$ through $q$.

Define $r \prec r'$ when $\phi(r) < \phi(r')$, or $\phi(r) = \phi(r')$ and $|r - p| > |r' - p|$. This is a strict total order on $S \setminus \{p\}$ (two distinct points with the same angle have different distances). Line L9 replaces $q$ by $r$ exactly when $r \prec q$. Invariant of the loop of line L8: $q$ is the $\prec$-smallest of the initial $q$ and the points scanned so far. It holds at the start and is kept by each step, because $\prec$ is transitive. So at the end $q$ is the $\prec$-minimum $q^*$ of $S \setminus \{p\}$: the point with the smallest angle, and the farthest one on that ray.

$(p, q^*)$ is a hull edge. For $r \ne p$, $\phi(r) \ge \phi(q^*)$, so $\mathrm{orient}(p, q^*, r) \ge 0$. If it is $0$, then $r$ is on the ray from $p$ through $q^*$ and $|r - p| \le |q^* - p|$, so $r$ lies on the segment $p q^*$. Also $r = p$ gives $0$ and lies on the segment. By the uniqueness in Lemma 1, $q^*$ is the successor. $\square$

**Correctness.** Line L3 sets $start$ to the lexicographically smallest point, which is extreme: it is the only maximizer of $\langle u, \cdot \rangle$ for $u = (-1, -\varepsilon)$ with a small enough $\varepsilon > 0$. By induction on the iterations, the point $p$ at line L6 of iteration $k$ is the $k$-th extreme point in counterclockwise order from $start$: true for $k = 1$, and if true for $k$, then by Lemma 2 line L10 sets $p$ to the successor, which is the $(k+1)$-th. By Lemma 1, the successor walk returns to $start$ for the first time after $h$ steps. So line L11 stops the loop after exactly $h$ iterations, and $hull$ holds the $h$ extreme points in counterclockwise order, each once.

**Termination.** The loop of line L8 is a finite scan, and the loop of line L5 stops after $h \le |S|$ iterations by the argument above. With $|S| \le 1$, line L2 returns at once. $\blacksquare$
