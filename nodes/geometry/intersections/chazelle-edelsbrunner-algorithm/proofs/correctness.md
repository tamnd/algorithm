---
title: STAIR-TREE reports exactly the intersecting pairs of closed segments, and terminates
proves: [correctness, termination]
status: full
---

**Notation.** $S$ is a finite list of closed segments with rational end points; a segment may have length zero (a *point*). For a non-vertical segment $s$, $s(x)$ is its height at $x$ and $\operatorname{rng}(s)$ its $x$-range. After line L1, $X_0 < \dots < X_m$ are the distinct $x$-coordinates of end points. A node $v$ of the slab tree covers the leaves $b, \dots, e - 1$ and has the closed strip $S_v = [X_b, X_e]$ and the half-open strip $H_v = [X_b, X_e)$. For a segment $s$ of positive length:

- $s \in \mathrm{Long}(v)$ if $S_v \subseteq \operatorname{rng}(s)$ but $S_u \not\subseteq \operatorname{rng}(s)$ for the parent $u$ of $v$ (the *canonical* nodes of a segment tree);
- $s \in \mathrm{Inner}(v)$ if $\operatorname{rng}(s) \cap S_v$ has positive length but $S_v \not\subseteq \operatorname{rng}(s)$.

A point $z$ is in $\mathrm{Inner}(v)$ if $z_x \in H_v$. The procedure `place` computes exactly these sets: it visits a node only if its strip meets $\operatorname{rng}(s)$ in positive length and no ancestor is contained in $\operatorname{rng}(s)$. $L_v$ is the list built at line L5, $Q_v$ and $\mathit{rest}_v$ are the stairs and the other segments of line L6. "Meets" always means shares a point.

**Lemma 1 (line L1).** The map $(x, y) \mapsto (x + \lambda y, y)$ is a linear bijection, so two segments meet if and only if their images meet. After it, distinct end points have distinct $x$-coordinates, so every segment of positive length is non-vertical, and for each $i$ there is exactly one end point $P_i$ with $x = X_i$.

*Proof.* If two distinct end points already have distinct $x$, then $\lambda = 0$. Otherwise $\lambda = \gamma / (2Y + 1)$, where $\gamma$ is the smallest gap between distinct $x$-coordinates and $Y$ the largest $|y|$. For end points with $x_1 \ne x_2$, $|x_1 - x_2| \ge \gamma > \lambda |y_1 - y_2|$, so their images differ in $x$; for $x_1 = x_2$ and $y_1 \ne y_2$, the images differ by $\lambda (y_1 - y_2) \ne 0$. $\square$

**Lemma 2 (SPLIT, line L6).** Let $L$ be sorted by height at $X_b$, all members spanning $S_v$. The stairs $q_0, q_1, \dots$ of $Q$ satisfy $q_0(x) < q_1(x) < \cdots$ for every $x \in S_v$. Each $s \in \mathit{rest}$ is recorded with a position $p$ such that $q_k(X_b) \le s(X_b)$ for $k < p$ and $q_k(X_b) \ge s(X_b)$ for $k \ge p$, and $s$ meets $q_{p - 1}$ inside $S_v$.

*Proof.* A segment $s$ becomes a stair only if it misses the last stair $q$ inside $S_v$. Since $s(X_b) \ge q(X_b)$ and the two linear functions do not meet on $S_v$, $s > q$ on all of $S_v$, and by induction $s$ is above every earlier stair. The position recorded for $s \in \mathit{rest}$ is the number of stairs so far, which come before $s$ in $L$; later stairs come after $s$. The sort gives the two inequalities, and $s$ went to $\mathit{rest}$ because it meets the last stair $q_{p - 1}$. $\square$

**Lemma 3 (WALK, lines L7 and L8).** Let the stairs be ordered as in Lemma 2, let $\tau \subseteq S_v$ be a segment or a point with left end $(c, y_c)$, and let $p$ satisfy $q_k(c) \le y_c$ for $k < p$ and $q_k(c) \ge y_c$ for $k \ge p$. Then WALK$(Q, p, \tau)$ reports exactly the stairs that meet $\tau$.

*Proof.* Let $\tau$ end at $(d, y_d)$ and put $f_k(x) = \tau(x) - q_k(x)$ on $[c, d]$, a linear function (for a point, $c = d$). A stair $q_k$ meets $\tau$ if and only if $f_k$ has a zero on $[c, d]$, that is, unless $f_k(c), f_k(d)$ are both positive or both negative. Since $q_k(x)$ increases with $k$, the indices with $f_k(c) > 0$ form a prefix, and so do those with $f_k(d) > 0$; their common part is a prefix $[0, \alpha)$. In the same way the indices where both values are negative form a suffix $[\beta, |Q|)$, and the stairs that meet $\tau$ are exactly those with index in $[\alpha, \beta)$. By the choice of $p$, $f_k(c) \ge 0$ for $k < p$ and $f_k(c) \le 0$ for $k \ge p$, so $\alpha \le p \le \beta$. WALK goes up from $p$ and down from $p - 1$, each time until the first stair that misses $\tau$. If $\alpha \le p - 1$, the downward walk covers $[\alpha, p - 1]$ and the upward walk $[p, \beta)$; if $\alpha = p$, the downward walk stops at once and the upward walk covers $[p, \beta)$. $\square$

At line L7, Lemma 2 gives the hypothesis with $c = X_b$ and $\tau$ the part of $s$ in $S_v$. At line L8, the binary search returns the first $p$ with $q_p(c) \ge y_c$, which is the hypothesis for the part of the inner segment in $S_v$. The same holds for each round of STRIP, since $\mathit{rest}$ is a subsequence of a sorted list.

**Lemma 4 (soundness).** Every reported pair meets.

*Proof.* Line L2 reports pairs with a common end point. Lines L7, L8 and L13 report a pair only after a successful exact test of two subsets of the two segments. Line L9 reports $t$ with a point $z$ only if $t(X_b) = z_y$, and $z_x = X_b$ there, since $z_x \in H_v$ is an end point coordinate and a leaf has no $X_i$ strictly inside. $\square$

**Lemma 5 (returned order).** If $P$ is sorted by the key (height at $X_b$, slope, index), then SEARCH$(v, P)$ returns the members of $P$ sorted by the same key at $X_e$, and STRIP$(L)$ returns $L$ sorted at $X_e$.

*Proof.* By induction on the height of $v$ and the number of rounds of STRIP. Each stair list is sorted at $X_e$, because the stairs are strictly ordered on all of $S_v$ by Lemma 2, so a merge of sorted lists is sorted and contains both. In STRIP, the result is the merge of all rounds, which is $L$. At an inner node, the left call gets $\mathit{rest}$ sorted at $X_b$ and returns it sorted at $X_{\mathrm{mid}}$, which is the precondition of the right call, and the right call returns $\mathit{rest}$ sorted at $X_e$. Merging with $Q$ gives $L_v = P \cup \mathrm{Long}(v)$, and these are disjoint, since a member of $P$ spans the parent and so is not canonical at $v$. Line L11 keeps $P$. $\square$

Call a pair $\{s, t\}$ with a common point $p$ *alive* at $v$ if $p \in S_v$, one of $s, t$ is in $L_v$, and the other is in $L_v \cup \mathrm{Inner}(v)$.

**Lemma 6 (a start).** If $s$ and $t$ meet at $p$ and have no common end point, they are alive at some node.

*Proof.* Two points meet only if they are equal, and then they share an end point; so at most one of them is a point. If $z = s$ is a point, then $z = p$ lies on $t$, and $z$ is not an end point of $t$, so $z_x$ lies strictly inside $\operatorname{rng}(t)$, because a non-vertical segment meets the line $x = X_i$ at an end of its range only in its end point. The canonical strips of $t$ split $\operatorname{rng}(t)$ into consecutive strips, so one of them, of node $v$, has $z_x \in H_v$; then $t \in \mathrm{Long}(v) \subseteq L_v$ and $z \in \mathrm{Inner}(v)$.

Now let both have positive length. Suppose first that a leaf $\ell$ with $p_x \in S_\ell$ lies in both ranges. The canonical nodes of $s$ and $t$ that contain $\ell$ lie on the path from the root to $\ell$, say $v_t$ is an ancestor of $v_s$ or equal to it. If they are equal, both are in $\mathrm{Long}(v_t)$. Otherwise $S_{v_t} \not\subseteq \operatorname{rng}(s)$, since the parent of $v_s$ is not contained in it, while $\operatorname{rng}(s) \supseteq S_{v_s}$ meets $S_{v_t}$ in positive length, so $s \in \mathrm{Inner}(v_t)$. In both cases the pair is alive at $v_t$.

If no such leaf exists, then $p_x$ is some $X_i$, because ranges are unions of leaves and a leaf that contains $p_x$ in its interior would lie in both. Each leaf next to $X_i$ is missed by one of the two ranges, and a range that contains $X_i$ but misses the leaf on one side ends at $X_i$. So each of $s, t$ has an end point with $x = X_i$, which by Lemma 1 is $P_i$. A non-vertical segment has only one point with $x = X_i$, so $p = P_i$ is a common end point, which was excluded. $\square$

**Lemma 7 (descent).** If a pair is alive at $v$, then SEARCH$(v)$ reports it, or $v$ is not a leaf and the pair is alive at a child of $v$.

*Proof.* Let $t \in L_v$ and let $s$ be the other segment. If one of them is a stair and the other is in $\mathit{rest}_v$ or in $\mathrm{Inner}(v)$, line L7 or line L8 reports the pair by Lemma 3, since the part of the other segment in $S_v$ contains $p$. Both cannot be stairs, because stairs do not meet in $S_v$. There remain two cases.

*Both in $\mathit{rest}_v$.* If $v$ is a leaf, the rounds of STRIP repeat the argument: in each round one of them becomes a stair and the pair is reported, or both go to the next round; the rounds stop with at most one segment, so the pair is reported. Otherwise both are passed to both children (Lemma 5), and the child with $p \in S_w$ makes the pair alive.

*$t \in \mathit{rest}_v$ and $s \in \mathrm{Inner}(v)$.* If $s$ is a point, then $p = s$. At a leaf, $s_x = X_b$, and line L9 finds $t$, whose height at $X_b$ is $s_y$, by binary search in $L_v$, which is sorted by height at $X_b$. At an inner node, $s$ is in $\mathrm{Inner}(w)$ for the one child $w$ with $s_x \in H_w$, and $t \in L_w$. If $s$ has positive length, $v$ is not a leaf, since a range that meets a leaf strip in positive length contains it. The interval $\operatorname{rng}(s) \cap S_v$ has positive length and contains $p_x$, so a child $w$ with $p \in S_w$ meets it in positive length: a child with $p_x$ in its interior, or, if $p_x$ is the split point, the child on the side where the interval goes on. Then $s \in \mathrm{Long}(w)$ or $s \in \mathrm{Inner}(w)$ by the definitions, since $S_v \not\subseteq \operatorname{rng}(s)$, and $t \in L_w$. $\square$

**Theorem.** STAIR-TREE terminates and returns exactly the pairs of segments of $S$ that meet.

*Proof.* Termination: SEARCH is called once for each node of a finite tree, each round of STRIP removes at least one stair, and the walks, splits, merges and binary searches are finite. By Lemma 1 the answer of the sheared input is the answer of the input. By Lemma 4 every reported pair meets. Conversely, a pair with a common end point is reported at line L2. Any other meeting pair is alive at some node by Lemma 6, and following Lemma 7 from that node down the tree, which SEARCH visits completely, the pair is reported at some node, at the latest at a leaf. The set `found` removes repeats. $\blacksquare$
