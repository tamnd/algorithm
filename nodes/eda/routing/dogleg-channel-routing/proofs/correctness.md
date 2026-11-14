---
title: The dogleg channel router returns a legal routing with doglegs at pin columns, reports exactly the cyclic cases, and never beats the density
proves: [correctness, termination, cycle detection, reduction to left-edge on two-pin nets, running time]
status: full
---

For a net $x$ with pin columns $c_0 < c_1 < \cdots < c_{k-1}$, the pieces are $p_i = [c_i, c_{i+1}]$ for $0 \le i \le k - 2$, each labeled with the net $x$. Let $G_p$ be the graph of line L2: an edge $p \to q$ when some column $c$ has net $a$ on top and net $b \ne a$ at the bottom, $p$ is a piece of $a$ with $c \in p$, and $q$ is a piece of $b$ with $c \in q$. Let $\prec$ be the order of line L1.

**Wires.** From tracks $t(p)$ with $T = \max_p t(p)$, build: a trunk of net $x$ on layer H on track $t(p)$ over the columns of $p$, for each piece $p$ of $x$; and for each pin of $x$ in column $c$, a branch of $x$ on layer V in column $c$ from the pin row (0 or $T + 1$) to the farthest track $t(p)$ among the pieces $p$ of $x$ that hold $c$, with a via at each such track.

**Lemma 1 (same track).** Two pieces placed on one track either have disjoint intervals, or belong to the same net and share one end column.

*Proof.* As in Lemma 1 of the left-edge proof, $\mathit{last}$ is the largest right end on the track, because line L6 only accepts $l_p \ge \mathit{last}$. If $l_p > \mathit{last}$, the interval of $p$ is disjoint from all intervals on the track. If $l_p = \mathit{last}$, line L6 requires that $p$ has the net of the piece that ends at $\mathit{last}$. Every other piece on the track ends before $\mathit{last}$, so $p$ is disjoint from those, and it shares only column $l_p$ with the last one. $\square$

**Lemma 2 (edges kept).** For every edge $p \to q$ of $G_p$ with both pieces placed, $t(p) < t(q)$.

*Proof.* Line L6 places $q$ on track $t$ only when its parent $p$ has a track less than $t$. $\square$

**Theorem 1 (legal routing).** If the algorithm returns tracks, the wires above form a legal routing in the reserved two-layer model.

*Proof.* *Layer H.* Two trunks of different nets on one track are disjoint by Lemma 1.

*Layer V.* The only branches in column $c$ are the branch of $a = \mathrm{top}(c)$, which holds rows 0 to $\max\{t(p) : p \text{ a piece of } a, c \in p\}$, and the branch of $b = \mathrm{bot}(c)$, which holds rows $\min\{t(q) : q \text{ a piece of } b, c \in q\}$ to $T + 1$. If $a = b$, both belong to one net. If $a \ne b$, every pair of such $p$ and $q$ is an edge $p \to q$ of $G_p$, so by Lemma 2 the maximum is less than the minimum, and the two branches are disjoint.

*Vias.* Each via of $x$ is at $(c, t(p))$ with $c \in p$, so the trunk of $p$ holds that point on layer H.

*Connectivity.* The pieces $p_{i-1}$ and $p_i$ of $x$ both hold the pin column $c_i$, and the branch of a pin of $x$ in column $c_i$ reaches both of their tracks, with vias. So consecutive pieces are joined, all pieces of $x$ form one connected wire, and every pin of $x$ lies on a branch that reaches a trunk of $x$. $\square$

**Theorem 2 (termination and cycles).** If $G_p$ is acyclic, the algorithm returns a track for every piece after at most $P$ passes. If $G_p$ has a cycle, it returns "cycle".

*Proof.* The argument is that of Lemmas 3 and 4 and Theorem 1 of the left-edge proof, with pieces for nets. If $G_p$ is acyclic, the first piece in the order $\prec$ among the unplaced pieces with all parents placed is accepted when it is scanned, unless an earlier piece of the pass was accepted. So every pass places a piece. A piece on a cycle is never placed, since its parent on the cycle is never on a higher track before it, so a cyclic $G_p$ leads to a pass that places nothing, and line L9 returns "cycle". $\square$

**Theorem 3 (two-pin nets).** If every net has pins in exactly two columns, the algorithm returns the same tracks as the left-edge algorithm, with each net in the place of its only piece.

*Proof.* Each net is one piece with the same interval, so the orders of line L1 agree. Two pieces of one net never meet, so the extra clause of line L6 never applies. A column with $a$ on top and $b \ne a$ at the bottom is in the only piece of each, so $G_p$ is the vertical constraint graph of the nets. The two scans are then the same step by step. $\square$

**Theorem 4 (density).** The algorithm never uses fewer than $d$ tracks.

*Proof.* By Theorem 1 the result is a legal routing in the reserved two-layer model, and the density bound holds for every such routing, with doglegs or without. $\square$

**Theorem 5 (running time).** The algorithm runs in $O(n + P \log P + T(P + n))$ time.

*Proof.* A column $c$ is held by at most two pieces of a net: the one or two pieces that end at $c$ if $c$ is a pin column of the net, and one piece otherwise. So each column gives at most $2 \cdot 2 = 4$ edges, and $G_p$ has at most $4n$ edges. A sweep over the columns that keeps, for each net, the pieces that hold the current column builds the pieces and $G_p$ in $O(n + P)$ time. Sorting takes $O(P \log P)$. Each pass looks at each unplaced piece and its parents once, in $O(P + n)$ time, and there are at most $T + 1$ passes. $\square$

**Tests.** The tests compare the implementation with two exhaustive searches over all maps from pieces to tracks: one that builds the wires and runs a geometric checker, and one that applies the rules of Lemma 1 and the edges of $G_p$ directly. On small channels both searches agree, the router is legal and never below their optimum, and it returns "cycle" exactly when no map works.
