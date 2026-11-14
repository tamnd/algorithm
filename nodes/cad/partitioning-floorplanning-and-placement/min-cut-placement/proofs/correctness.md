---
title: Min-cut placement returns a legal placement, stops after at most 2S - 1 regions, and its HPWL is a sum of cut counts
proves: [correctness, termination, running time]
status: full
---

The sites are the integer points $(x, y)$ with $0 \le x < W$ and $0 \le y < H$, and $S = W H$. A region is a rectangle of sites $[x_0, x_1) \times [y_0, y_1)$. For a region $B$ with the cells $C$, line L5 cuts the longer side through the middle into $B_0$ and $B_1$, with $c_0$ and $c_1$ sites, and line L7 sets $t = \mathrm{round}(k c_0 / (c_0 + c_1))$ with $k = |C|$. The window of line L8 is $[lo, hi]$ with $lo = \max(k - c_1, t - 1, 0)$ and $hi = \min(c_0, t + 1, k)$.

**Lemma 1 (window).** If $k \le c_0 + c_1$, then $lo \le t \le hi$.

*Proof.* Let $q = k c_0 / (c_0 + c_1)$. Rounding gives $|t - q| \le \frac12$. Since $k \le c_0 + c_1$, we have $q \le c_0$, so $t \le c_0 + \frac12$, and $t \le c_0$ because $t$ is an integer. In the same way $k - q = k c_1 / (c_0 + c_1) \le c_1$, so $k - t \le k - q + \frac12 \le c_1 + \frac12$, and $k - t \le c_1$. Also $0 \le q \le k$ gives $0 \le t \le k$. The terms $t - 1$ and $t + 1$ hold trivially. So every term of the maximum is at most $t$, and every term of the minimum is at least $t$. $\square$

**Lemma 2 (FM keeps the window).** If the start has $|C_0| \in [lo, hi]$, the split returned by line L8 has $|C_0| \in [lo, hi]$.

*Proof.* A pass keeps the prefix of its tentative moves with the largest total gain among the prefixes that end with $|C_0| \in [lo, hi]$, and the empty prefix is one of them because the pass starts inside the window. So each pass ends inside the window, and the next pass starts there. The fixed terminals never move and are not counted in $|C_0|$. FM stops because a new pass starts only after a pass with positive total gain, and the integer cut falls by at least 1 each time. $\square$

The start of line L7 has exactly $t$ cells on side 0, which is in the window by Lemma 1. So with Lemma 2 every split satisfies $|C_0| \le c_0$ and $|C_1| = k - |C_0| \le c_1$.

**Theorem 1 (legality).** If $n \le S$, the output places every cell on a site of the rectangle, and no two cells on the same site.

*Proof.* Call a pair $(B, C)$ in the queue *good* if $|C|$ is at most the number of sites of $B$. The first pair is good because $n \le S$. If $(B, C)$ is good and is cut, Lemmas 1 and 2 show that both pairs $(B_s, C_s)$ are good. Consider the tree of all regions put in the queue, where the children of a cut region are $B_0$ and $B_1$. The two children are disjoint and their union is the parent, so two regions of the tree are either nested or disjoint. The cells of a cut region go to exactly one child, so at each time every cell is in exactly one region of the queue, or has a site. A cell leaves the queue only through line L4, and line L4 handles only regions of one site. A good pair with one site has at most one cell, so line L4 never puts two cells of one region on its site. Two different one-site regions are leaves of the tree, so they are disjoint and are different sites. By Theorem 2 the queue becomes empty, so every cell gets a site. $\blacksquare$

**Theorem 2 (termination).** The loop of lines L2 to L9 runs at most $2S - 1$ times, and every root to leaf path of the region tree has at most $\lceil \log_2 W \rceil + \lceil \log_2 H \rceil$ cuts.

*Proof.* A region that is cut is not one site, so its longer side has length $L \ge 2$, and the cut makes parts with sides $\lfloor L / 2 \rfloor \ge 1$ and $\lceil L / 2 \rceil < L$. So both children are nonempty rectangles with fewer sites. The region tree is a binary tree in which each inner node has exactly two children. Its leaves are pairwise disjoint nonempty sets of sites, so there are at most $S$ leaves, and at most $2S - 1$ nodes. Each node is removed from the queue once. On a path from the root, each vertical cut replaces a width $w \ge 2$ by at most $\lceil w / 2 \rceil$, so after $\lceil \log_2 W \rceil$ vertical cuts the width is 1 and no more vertical cut happens (line L5 cuts vertically only when the width is the longer side, and a region of width 1 and height 1 is not cut). The same holds for the height. $\square$

**Lemma 3 (HPWL as a sum of cut counts).** Let all pins have integer positions. For an integer $j$, let $X_j$ be the number of nets with pins on both sides of the line $x = j + \frac12$, and define $Y_j$ in the same way. Then the HPWL is $\sum_j X_j + \sum_j Y_j$.

*Proof.* Take one net with smallest and largest $x$ coordinates $a \le b$. It has pins on both sides of $x = j + \frac12$ exactly when $a < j + \frac12 < b$, that is $a \le j \le b - 1$. There are $b - a$ such $j$, which is the $x$ part of its bounding box. The same argument holds for $y$. Add over all nets and change the order of the sums. $\square$

Every cell of $C_s$ is later placed inside $B_s$ by Theorem 1, so it ends on side $s$ of the cut line. So the cut that line L8 makes small is a part of one term $X_j$ or $Y_j$: the nets of $C$ that will cross that line.

**Lemma 4 (terminal propagation).** Suppose that every pin outside $C$ is at a fixed position that is not on the cut line. For a split $(C_0, C_1)$, let $X$ be the number of nets with a pin in $C$ that have pins on both sides of the line when the cells of $C_s$ are on side $s$, and let $Z$ be the cut of the netlist built in line L6. Then $X = Z + D$, where $D$ is the number of nets left out because they have outside pins on both sides. $D$ does not depend on the split.

*Proof.* Take a net $e$ with a pin in $C$. If it has no outside pins, $e$ crosses the line exactly when its pins in $C$ are split, and the restricted net is cut exactly then (a net with one pin is never split and is left out). If all its outside pins are on side $s$, $e$ crosses the line exactly when some pin in $C$ is on side $1 - s$, and that is exactly when the restricted net with the terminal of side $s$ is cut. If it has outside pins on both sides, it crosses the line for every split, and it is left out of the netlist. Add over the nets. $\square$

So under the assumption of Lemma 4, the splits of least cut in line L8 are exactly the splits with the fewest crossing nets. In the algorithm the outside cells are at the centers of their regions, not at their final sites, so the assumption is false in general, and the lemma explains the method but gives no bound.

**Running time.** By Theorem 2 there are $O(\log S)$ levels. The regions of one level have disjoint cell sets. Line L6 visits each pin of each net with a pin in $C$, and adds at most one terminal per net. With a mark per net, a net is handled once per region it touches, and a net with $|e|$ pins touches at most $|e|$ regions of a level, so the netlists of a level have $O(n + m + P)$ pins in all. An FM pass with gain buckets costs time linear in the size of its netlist (see the [Fiduccia-Mattheyses](/fiduccia-mattheyses/) page), so a level costs $O(p (n + m + P))$ if each region uses at most $p$ passes, and the total is $O(p (n + m + P) \log S)$. The queue holds the regions of at most two levels, with disjoint cell sets, so the space is $O(n + m + P)$. The implementation picks each move by a scan of the free cells and rebuilds each restricted net from its full pin list, so a region with $k$ cells costs $O(k^2 + \sum_e |e|^2)$ per pass over the nets $e$ of the region.

**What is not proved.** Nothing above compares the HPWL of the output with the minimum. Each cut is only a local optimum of FM, and no approximation ratio of min-cut placement for HPWL is known.
