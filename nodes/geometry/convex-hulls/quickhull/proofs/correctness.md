---
title: Quickhull returns the hull vertices in counterclockwise order
proves: [correctness, termination]
status: full
---

**Claim.** Let $S$ be the set of distinct points after line L1. QUICKHULL returns the extreme points of $S$ (the vertices of $K = \operatorname{conv} S$), each once, in counterclockwise order, starting at the lexicographically smallest point $a$. If $S$ is collinear with $|S| \ge 2$, the output is its two end points.

**Notation.** $D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, so $\mathrm{orient}(p, q, r) = \operatorname{sign} D(p, q, r)$. "Right of $p \to q$" means $D(p, q, r) < 0$. For the directed line from $p$ to $q$, let $\nu = (q_y - p_y, -(q_x - p_x))$, its normal pointing to the right. Then $D(p, q, r) = -\langle \nu, r - p \rangle$, so the points farthest to the right of the line are the maximizers of $\langle \nu, \cdot \rangle$.

**Fact 1 (chords of a convex polygon).** Let $K$ be a convex polygon with vertices $w_0, \ldots, w_{h-1}$ in counterclockwise order, $h \ge 3$, no three collinear. For $p = w_0$ and $q = w_k$ with $1 \le k \le h - 1$, the vertices strictly right of $p \to q$ are exactly $w_1, \ldots, w_{k-1}$, the inner vertices of the counterclockwise boundary path from $p$ to $q$.

*Proof.* Each edge line of $K$ has all other vertices strictly on its left. A line meets the boundary of a convex polygon in at most two points or in one edge. The line through $p$ and $q$ meets the boundary at $p$ and $q$ (or along the edge $pq$ when $k = 1$ or $k = h - 1$), so each of the two boundary paths between $p$ and $q$ stays on one side of it, and no vertex other than $p, q$ lies on it. If $k \ge 2$, then $\mathrm{orient}(w_0, w_1, w_k) > 0$ because $w_k$ is strictly left of the edge $w_0 w_1$, so $D(p, q, w_1) < 0$ and the path $w_1, \ldots, w_{k-1}$ is on the right. The other path is on the left by the same argument applied to the edge $w_{h-1} w_0$. $\square$

**Fact 2 (no point behind a vertex).** Let $p$ be an extreme point of $S$, and $q, c \in S \setminus \{p\}$ with $c$ strictly right of $p \to q$. Every $r \in S$ strictly right of $p \to c$ is strictly right of $p \to q$.

*Proof.* Measure the directions of the vectors from $p$ counterclockwise from $q - p$. Then $c - p$ has angle $-\alpha$ with $0 < \alpha < \pi$. Suppose $r$ is strictly right of $p \to c$, so $r - p$ has angle in $(\pi - \alpha, 2\pi - \alpha)$ modulo $2\pi$, and not strictly right of $p \to q$, so its angle is in $[0, \pi]$. Then its angle $\theta$ is in $(\pi - \alpha, \pi]$. The three directions $0$, $\theta$ and $2\pi - \alpha$ leave gaps $\theta \le \pi$, $2\pi - \alpha - \theta < \pi$ and $\alpha < \pi$. So they lie in no open half-plane, and $p$ is in $\operatorname{conv}\{q, r, c\}$ (on the segment $rq$ if $\theta = \pi$). As $p \notin \{q, r, c\}$, $p$ is not extreme, a contradiction. $\square$

The same holds with the roles of the two ends exchanged: if $q$ is extreme and $c$ is strictly right of $p \to q$, every $r$ strictly right of $c \to q$ is strictly right of $p \to q$ (apply Fact 2 to the mirror image, or repeat the angle argument at $q$).

**Lemma (FIND-HULL).** Let $p \ne q$ be extreme points of $S$, and let $X = \{r \in S : D(p, q, r) < 0\}$. Then FIND-HULL$(p, q, X)$ returns the extreme points of $S$ that are strictly right of $p \to q$, in the order of the counterclockwise boundary path of $K$ from $p$ to $q$.

*Proof.* Induction on $|X|$.

*Base, $X = \emptyset$.* Every extreme point is in $S$, so none is strictly right of $p \to q$, and line L6 returns the empty list.

*Step, $X \ne \emptyset$.* Line L7 picks $c \in X$ with the largest $\langle \nu, c \rangle$, and among those the largest $\langle q - p, c \rangle$. Points of $S \setminus X$ have $\langle \nu, r - p \rangle \le 0 < \langle \nu, c - p \rangle$. So $c$ is the only maximizer over $S$ of $\langle \nu + \varepsilon (q - p), \cdot \rangle$ for a small enough $\varepsilon > 0$, and $c$ is an extreme point of $S$. It is strictly right of $p \to q$.

By Fact 2, $X_1$ of line L8 equals $\{r \in S : D(p, c, r) < 0\}$, and by its mirror form, $X_2$ of line L9 equals $\{r \in S : D(c, q, r) < 0\}$. Both are subsets of $X \setminus \{c\}$, so they are smaller than $X$, and the induction hypothesis applies to the calls of line L10 with the extreme pairs $(p, c)$ and $(c, q)$.

$S$ is not collinear, since $c$ is off the line $pq$, so $K$ is a convex polygon and Fact 1 applies. The extreme points strictly right of $p \to q$ are the inner vertices of the counterclockwise path from $p$ to $q$. The vertex $c$ is one of them, so this path is the path from $p$ to $c$ followed by the path from $c$ to $q$. By Fact 1 again, the inner vertices of these two paths are the extreme points strictly right of $p \to c$ and strictly right of $c \to q$, which the two calls return in path order. So line L10 returns the inner vertices of the path from $p$ to $q$ in order. $\square$

**Main procedure.** If $|S| \le 2$, line L2 returns the points of $S$ in order, which are its extreme points. Otherwise $a$ and $b$ of line L3 are distinct extreme points: the lexicographic minimum and maximum maximize $\langle u, \cdot \rangle$ uniquely for $u = (-1, -\varepsilon)$ and $u = (1, \varepsilon)$ with a small $\varepsilon > 0$. If $S$ is collinear, the sets of line L4 are empty and the output is $a, b$, the two end points. Otherwise, by the lemma, the two calls of line L5 return the inner vertices of the counterclockwise paths from $a$ to $b$ and from $b$ to $a$, so line L5 returns all vertices of $K$ in counterclockwise order from $a$, each once.

**Termination.** A call with $X \ne \emptyset$ makes two calls on sets with fewer elements, and a call with $X = \emptyset$ makes none. So the call tree is finite: by induction on $|X|$, a call on $X$ leads to at most $2|X| + 1$ calls in total. $\blacksquare$
