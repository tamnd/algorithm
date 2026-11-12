---
title: Warnock's algorithm gives each pixel its nearest covering triangle
proves: [correctness]
status: full
---

We use the pseudocode and the definitions of the page. For a pixel $p$ with center $c_p$, let $\mathrm{ans}(p)$ be the covering triangle with the least pair (depth at $c_p$, index), or the background. A window $w = [x, x + s] \times [y, y + s]$ *contains* the pixel $p$ when $p = (i, j)$ with $x \le i < x + s$ and $y \le j < y + s$. Then $c_p$ is in the open window, because $x < i + \tfrac12 < x + s$ and the same holds for $y$.

**Lemma 1 (the list).** When a window $w$ is popped with list $L$, every triangle that is not in $L$ is disjoint from $w$.

*Proof.* By induction on the depth of $w$ in the subdivision. The first window has $L = T$. A child $w'$ of $w$ gets the list $R$ of $w$ (line L9). A triangle not in $R$ is either not in $L$, and then disjoint from $w$ by induction, or in $L$ and disjoint from $w$ by line L3. The open window $w'$ is a subset of the open window $w$, so in both cases the triangle is disjoint from $w'$. $\square$

**Lemma 2 (the tests of line L3).** The test for *disjoint* returns true exactly when the triangle meets no point of the open window, and the test for *surrounding* returns true exactly when the triangle contains the closed window.

*Proof.* A triangle and a square are convex. By the separating axis theorem for two convex polygons in the plane, the closed triangle and the open square are disjoint if and only if some line parallel to an edge of one of them separates them, with the open square strictly on one side and the closed triangle on the other side or on the line. The edges of the square give the $x$ and $y$ axes, which is the bounding box test. The edges of the triangle give the three edge lines: the square is outside the edge line when each corner has an edge function value at most 0, because the open square is the interior of the convex hull of its corners. For *surrounding*: a convex set contains the closed square if and only if it contains its four corners, since the square is their convex hull. $\square$

**Lemma 3 (each case is right).** Let $w$ be a window popped with list $L$, and let $R$ and $U$ be the lists of line L3. Every triangle that covers the center of a pixel of $w$ is in $R$, by Lemmas 1 and 2. Then:

1. In case L4, no triangle covers any center of $w$, so $\mathrm{ans}(p)$ is the background for each pixel $p$ of $w$.
2. In case L5, only $t$ can cover a center of $w$. So $\mathrm{ans}(p)$ is $t$ if $t$ covers $c_p$, and the background if not, which is what line L5 draws.
3. In case L7, let $t \in U$ and let $u \ne t$ be in $R$. The depth $z_t$ is affine, so on the closed window its greatest value is at a corner, and $z_t(c) \le \max_{\text{corners}} z_t$ for each point $c$ of the window. In the same way $z_u(c) \ge \min_{\text{corners}} z_u$, where $z_u$ is the depth of the plane of $u$. The test of line L6 gives $z_t(c) < z_u(c)$ at each point of the window. The triangle $t$ surrounds the window, so it covers each center (each center is an interior point of $t$, so the fill rule does not matter). Hence $t$ is the unique nearest covering triangle at each center, and $\mathrm{ans}(p) = t$.
4. In case L8, $w$ is one pixel, and line L8 computes $\mathrm{ans}(p)$ over $R$, which holds every triangle that covers $c_p$.

So each window that ends in lines L4 to L8 writes $\mathrm{ans}(p)$ at each of its pixels on the screen. $\square$

**Lemma 4 (termination and cover).** The loop ends, and each pixel of the screen is contained in exactly one window that ends in lines L4 to L8.

*Proof.* Each window that is split has side $s \ge 2$ (a window of side 1 ends in line L8 at the latest), and its children have side $s/2$. So the side of a window at depth $d$ is $s_0 / 2^d$, and there is no window at depth more than $\log_2 s_0$. Each window has at most four children, so the number of windows is finite, and each iteration pops one. The four children of a window split its pixels into four disjoint sets. By induction on the depth, the windows that are not split, together with the skipped windows outside the screen, split the pixels of the first window, which contains the screen. A skipped window contains no pixel of the screen. $\square$

**Theorem.** WARNOCK writes $\mathrm{ans}(p)$ at each pixel $p$ of the screen.

*Proof.* By Lemma 4, each pixel is in exactly one window that ends in lines L4 to L8, and no other window writes to it, since a split window writes nothing. By Lemma 3 that window writes $\mathrm{ans}(p)$. $\blacksquare$
