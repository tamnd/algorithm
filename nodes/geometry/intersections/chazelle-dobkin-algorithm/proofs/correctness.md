---
title: CONVEX-MEET decides whether two convex polygons meet, with O(log p + log q) steps
proves: [correctness, termination]
status: full
---

**Notation.** A convex polygon $P$, possibly a point or a segment, has the $x$-range $[x_P^-, x_P^+]$. Its upper chain is the vertex list $U_P$ with strictly increasing $x$, and the same letter denotes the piecewise linear function on $[x_P^-, x_P^+]$ whose graph it is; likewise for the lower chain $L_P$. By the construction of the [monotone chain hull](/andrew-monotone-chain/), $U_P$ is concave, $L_P$ is convex, and $P = \{(x, y) : x_P^- \le x \le x_P^+,\ L_P(x) \le y \le U_P(x)\}$. For a function $f$ and a point $x$, $f'(x^+)$ and $f'(x^-)$ are the right and left derivatives. For a chain $c$, $s_c(k)$ is the slope of its edge from $c[k]$ to $c[k + 1]$. For a concave chain the slopes are nonincreasing in $k$, for a convex chain nondecreasing.

**Lemma 1 (line L2).** Let $I$ be the common $x$-range of $P$ and $Q$. Then $P \cap Q \ne \emptyset$ if and only if $I \ne \emptyset$, some $x \in I$ has $U_P(x) \ge L_Q(x)$, and some $x' \in I$ has $U_Q(x') \ge L_P(x')$.

*Proof.* A point $(x, y)$ lies in both polygons exactly when $x \in I$ and $\max(L_P(x), L_Q(x)) \le y \le \min(U_P(x), U_Q(x))$. Such a $y$ exists exactly when $f_1(x) = U_P(x) - L_Q(x) \ge 0$ and $f_2(x) = U_Q(x) - L_P(x) \ge 0$, since $L_P \le U_P$ and $L_Q \le U_Q$ hold anyway. So "only if" is clear. For "if", $f_1$ and $f_2$ are concave, so $A_1 = \{x \in I : f_1(x) \ge 0\}$ and $A_2 = \{x \in I : f_2(x) \ge 0\}$ are closed intervals, nonempty by assumption. Suppose they were disjoint, say every point of $A_1$ is left of every point of $A_2$. Then there is an $x$ strictly between them with $f_1(x) < 0$ and $f_2(x) < 0$. But $f_1 + f_2 = (U_P - L_P) + (U_Q - L_Q) \ge 0$ on $I$, a contradiction. So $A_1 \cap A_2$ contains a point $x$, and $P \cap Q \ne \emptyset$. $\square$

So it remains to show that GAP$(u, l)$, for a concave chain $u$ and a convex chain $l$, decides whether $g = u - l$ is nonnegative somewhere on the common range $[lo, hi]$. The function $g$ is concave and piecewise linear, and it can bend only at the $x$-coordinates of vertices of $u$ or $l$.

**Lemma 2 (concave pruning).** Let $a$ and $b$ be points of $[lo, hi)$. If $g'(a^+) > 0$, then $g(x) < g(a)$ for all $x < a$. If $g'(b^+) \le 0$, then $g(x) \le g(b)$ for all $x > b$. If both hold, then $a < b$.

*Proof.* For concave $g$, the right derivative is a supergradient: $g(x) \le g(c) + g'(c^+)(x - c)$ for all $x$ and $c$. With $c = a$ and $x < a$ this gives $g(x) < g(a)$, and with $c = b$ and $x > b$ it gives $g(x) \le g(b)$. The right derivative of a concave function is nonincreasing, so $a \ge b$ would give $g'(a^+) \le g'(b^+) \le 0$. $\square$

Since $g'(b^-) \ge g'(b^+)$ for concave $g$, a left derivative $g'(b^-) \le 0$ also gives $g'(b^+) \le 0$.

**Invariant.** After line L5 and after every pass of lines L6, L7 and L8:

1. $lo \le wl \le wr \le hi$;
2. $wl = lo$ or $g'(wl^+) > 0$, and $wr = hi$ or $g'(wr^+) \le 0$;
3. every vertex of $u$ with $x$-coordinate in the open interval $(wl, wr)$ has an index in $[ia, ib]$, and every vertex of $l$ with $x$-coordinate in $(wl, wr)$ has an index in $[ja, jb]$;
4. every index in $[ia, ib]$ or $[ja, jb]$ is a vertex whose $x$-coordinate lies strictly inside $(lo, hi)$.

By part 2 and Lemma 2, $\max_{[lo, hi]} g = \max_{[wl, wr]} g$. Part 4 makes every slope that the passes read well defined: a vertex strictly inside $(lo, hi)$ is not an end of its chain, so the edges on both sides of it exist.

**Lemma 3 (lines L3 to L5).** If $lo > hi$ the ranges are disjoint and the answer false is right; otherwise the invariant holds after line L5.

*Proof.* Line L4 selects exactly the vertices with $x$-coordinate strictly inside $(lo, hi)$, which gives parts 3 and 4 for the window $[lo, hi]$, and parts 1 and 2 hold with $wl = lo$, $wr = hi$. $\square$

**Lemma 4 (line L6).** One pass of line L6 keeps the invariant and removes at least half of the indices of $[ia, ib]$ or of $[ja, jb]$.

*Proof.* Let $u[i]$ and $l[j]$ be the medians, at $x$-coordinates $a$ and $b$.

*Case $a < b$.* The edge of $u$ right of $a$ is edge $i$, so $u'(a^+) = s_u(i)$. The edge of $l$ right of $a$ ends at or before $l[j]$, so its index is at most $j - 1$, and since $l$ is convex, $l'(a^+) \le s_l(j - 1)$. If $s_u(i) - s_l(j - 1) > 0$, then $g'(a^+) > 0$, and the pass sets $wl$ to $\max(wl, a)$, which satisfies part 2 either way. The removed vertices $u[ia..i]$ have $x \le a \le wl$, so part 3 is kept. Otherwise $s_u(i) \le s_l(j - 1)$. The edge of $u$ left of $b$ has index at least $i$, so $u'(b^-) \le s_u(i)$, and the edge of $l$ left of $b$ is edge $j - 1$; hence $g'(b^-) \le s_u(i) - s_l(j - 1) \le 0$, so $g'(b^+) \le 0$, the pass sets $wr$ to $\min(wr, b)$, and the removed vertices $l[j..jb]$ have $x \ge b \ge wr$.

*Case $a > b$.* Symmetric: $g'(a^-) \le s_u(i - 1) - s_l(j)$, so if this is $\le 0$ then $g'(a^+) \le 0$ and the pass sets $wr$ to $\min(wr, a)$ and removes $u[i..ib]$; otherwise $g'(b^+) \ge s_u(i - 1) - s_l(j) > 0$ and the pass sets $wl$ to $\max(wl, b)$ and removes $l[ja..j]$.

*Case $a = b$.* Here $g'(a^+) = s_u(i) - s_l(j)$ exactly. If it is positive, $wl$ becomes $\max(wl, a)$ and the vertices of both chains up to index $i$ and $j$ go. If not, $g'(a^+) \le 0$, so $wr$ becomes $\min(wr, a)$ and the vertices from index $i$ and $j$ on go.

In each case part 1 follows from part 2 and the last claim of Lemma 2, part 4 is kept because only indices are removed, and the removed block contains the median and everything on one side of it. $\square$

**Lemma 5 (lines L7 and L8).** When line L7 starts with $[ja, jb]$ empty and $wl < wr$, the chain $l$ has no vertex in $(wl, wr)$ by part 3, so it is linear on $[wl, wr]$ with the slope $s_l$ of its edge at $wl$. The binary search of line L7 keeps the invariant, and when it ends, $u$ has no vertex in $(wl, wr)$ either. Line L8 is the same with the roles of $u$ and $l$ exchanged.

*Proof.* For a vertex $u[i]$ with $x$-coordinate $c \in (wl, wr)$, $g'(c^+) = s_u(i) - s_l$, so the two branches are the cases of Lemma 2 with the same reasoning as in Lemma 4. A vertex with $c \le wl$ or $c \ge wr$ lies outside the open window, and since the indices are sorted by $x$, removing it with everything on its outer side keeps part 3. The search ends when $[ia, ib]$ is empty, and then part 3 says that no vertex of $u$ is left in $(wl, wr)$. $\square$

**Theorem.** GAP$(u, l)$ returns true if and only if $u(x) \ge l(x)$ for some $x$ in the common range, and CONVEX-MEET$(P, Q)$ returns true if and only if $P \cap Q \ne \emptyset$. Both use $O(\log p + \log q)$ steps, where $p$ and $q$ are the numbers of vertices.

*Proof.* The loop of line L6 ends when one of the index ranges is empty, and then at most one of lines L7 and L8 has work to do. If $wl = wr$ the window is a point. Otherwise, by Lemma 5, after lines L7 and L8 neither chain has a vertex in $(wl, wr)$, so $g$ is linear on $[wl, wr]$ and its maximum there is $\max(g(wl), g(wr))$. By the invariant this is the maximum of $g$ on $[lo, hi]$, so line L9 answers correctly. Lemma 1 turns the two answers of line L2 into the answer for $P$ and $Q$.

For termination and the bound, every pass of lines L6, L7 and L8 removes at least half of a nonempty index range, so there are at most $\lceil \log_2 (p + 1) \rceil + \lceil \log_2 (q + 1) \rceil$ passes in each of the two calls, each with $O(1)$ slope evaluations. Lines L4, L7, L8 and L9 also do a constant number of binary searches for an $x$-coordinate in a chain, each with $O(\log p + \log q)$ steps. $\blacksquare$
