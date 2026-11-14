---
title: The left-edge algorithm returns a legal routing without doglegs, reports every cycle, and uses d tracks when there are no vertical constraints
proves: [correctness, termination, cycle detection, optimality without vertical constraints, running time]
status: full
---

Let the nets be $x$ with closed intervals $I_x = [l_x, r_x]$, let $G_v$ be the vertical constraint graph, and let $\prec$ be the order of line L1: by left end, then by label. Call pass $t$ the run of lines L4 to L9 with the value $t$. Let $N$ be the number of nets.

**Lemma 1 (disjoint intervals on a track).** The nets placed on one track have pairwise disjoint intervals, and after each placement, $\mathit{last}$ is the largest right end on the track.

*Proof.* Within pass $t$ the nets are scanned in the order $\prec$. Let $y_1, y_2, \ldots$ be the nets placed on track $t$, in the order of placement. When $y_{j+1}$ is placed, line L6 gives $l_{y_{j+1}} > r_{y_j}$, and $r_{y_j}$ is the largest right end so far by induction. So $I_{y_{j+1}}$ starts after every interval already on the track, and its right end $r_{y_{j+1}} \ge l_{y_{j+1}} > r_{y_j}$ is the new largest. $\square$

**Lemma 2 (vertical constraints).** For every edge $a \to b$ of $G_v$ with both nets placed, $t(a) < t(b)$.

*Proof.* When $b$ is placed on track $t$, line L6 requires its parent $a$ to have a track less than $t$. A net keeps its track for ever, so $t(a) < t(b)$. $\square$

**Lemma 3 (progress).** If $G_v$ restricted to the unplaced nets $U$ at the start of pass $t$ has a node with no parent in $U$, then pass $t$ places at least one net.

*Proof.* Let $x$ be the first net in the order $\prec$ among the nets of $U$ whose parents are all outside $U$. All its parents were placed in earlier passes, so they have tracks less than $t$. If some net is placed before $x$ is scanned, the claim holds. Otherwise $\mathit{last}$ is still none when $x$ is scanned, and line L6 accepts $x$. $\square$

**Lemma 4 (nets on a cycle are never placed).** If $x_1 \to x_2 \to \cdots \to x_k \to x_1$ is a cycle of $G_v$, no net of the cycle is ever placed.

*Proof.* Suppose some net of the cycle is placed, and let $x_i$ be the first one placed, in a pass $t$. Its parent $x_{i-1}$ on the cycle (with $x_0 = x_k$) is not placed before $x_i$. If it is still unplaced, line L6 rejects $x_i$. If it is placed earlier in the same pass, it is on track $t$, and line L6 rejects $x_i$ too. Both contradict the choice of $x_i$. $\square$

**Theorem 1 (termination and cycle detection).** If $G_v$ is acyclic, the algorithm returns a track for every net after at most $N$ passes, and line L9 never fires. If $G_v$ has a cycle, the algorithm returns "cycle" after at most $N + 1$ passes.

*Proof.* If $G_v$ is acyclic, so is its restriction to $U$, and an acyclic graph with a node has a node with no parent. By Lemma 3, every pass places a net, so $U$ is empty after at most $N$ passes. If $G_v$ has a cycle, by Lemma 4 its nets stay in $U$ for ever. The nets not on any cycle are placed at most once each, so at most $N$ passes place a net. A pass that places nothing makes line L9 return "cycle". $\square$

**Theorem 2 (legal routing).** If the algorithm returns tracks $t(x)$ with $T = \max_x t(x)$, then the routing with a trunk of $x$ on track $t(x)$ over the columns of $I_x$ on layer H, and a branch on layer V from each pin of $x$ straight to track $t(x)$, is legal in the reserved two-layer model.

*Proof.* On layer H, two nets share a point only if they are on the same track and their intervals share a column. By Lemma 1 this does not happen. On layer V, the branches in column $c$ are the segment of $\mathrm{top}(c)$ from row 0 to its track and the segment of $\mathrm{bot}(c)$ from its track to row $T + 1$. If the two pins belong to the same net, the two segments belong to one net. If they belong to nets $a \ne b$, then $a \to b$ is an edge of $G_v$, and by Lemma 2 $t(a) < t(b)$, so the two segments are disjoint. Each via is at a point $(c, t(x))$ with $c$ a pin column of $x$, so $c \in I_x$ and the trunk of $x$ holds that point on layer H. Each net is connected, because each branch reaches the trunk. $\square$

**Theorem 3 (optimal without vertical constraints).** If $G_v$ has no edges, the algorithm uses exactly $d$ tracks, where $d$ is the channel density, and no routing uses fewer.

*Proof.* Let $x$ be a net placed on track $k$. For each $j < k$, net $x$ was scanned in pass $j$ and rejected. With no parents, the only reason is $l_x \le \mathit{last}$, and $\mathit{last} = r_y$ for a net $y$ already placed on track $j$ with $y \prec x$, so $l_y \le l_x$. So $l_y \le l_x \le r_y$, and $y$ crosses column $l_x$. The nets $y$ for different $j$ lie on different tracks and are different, and none of them is $x$. So at least $k$ nets cross column $l_x$, and $k \le d(l_x) \le d$. Hence $T \le d$. The density bound on the page on channel density, or the interval coloring depth theorem, gives $T \ge d$ for every routing. $\square$

**Theorem 4 (running time).** The algorithm runs in $O(n + N \log N + T(N + n))$ time and $\Theta(N + n)$ space.

*Proof.* One pass over the columns gives the intervals and the at most $n$ edges of $G_v$. Line L1 sorts $N$ nets. Each pass scans the nets of $U$ once, checks each parent of each scanned net once, and filters $U$ once, in $O(N + n)$ time. There are $T$ passes, plus one more when a cycle is reported, and $T \le N$. $\square$

**Tests.** The tests compare the implementation with two exhaustive searches over all maps from nets to tracks: one that builds the wires of each map and runs a geometric checker, and one that applies the rules of disjoint intervals and vertical constraints by backtracking, on channels with up to 6 nets. The track count of left-edge is never below the optimum, and it is above it on some cases. On channels with one pin per column, it always equals the density.
