---
title: The Hao-Orlin algorithm returns a minimum directed cut
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be directed with capacities $c \ge 0$, $n \ge 2$, and root $r$. For a set $Y$ write $c(Y) = c(Y, V \setminus Y)$. Arcs come in residual pairs, one per edge, and $r_f$ is the residual capacity. Write $e(v)$ for inflow minus outflow of $f$ at $v$. Order the parts as $S = D_0$, then the dormant sets $D_1, \dots, D_k$ in order of creation, then $W$, and call $W$ the last part.

**Invariants** (at every step of HAO-ORLIN-ROOTED):

- (I1) $0 \le f \le c$ and $e(v) \ge 0$ for every $v \notin S$.
- (I2) If $u \in D_i$ and $r_f(u, v) > 0$, then $v \in D_0 \cup \dots \cup D_i$. That is, no residual arc goes from $S$ or a dormant set to a later part.
- (I3) For every residual arc $(v, w)$ with $v, w \in W$, $d(v) \le d(w) + 1$.
- (I4) $t \in W$ and $d(t) \le d(v)$ for every $v \in W$; and the labels of $W$ form a set of consecutive integers.

**Initialization.** After lines L1 to L3, $f$ is full on arcs out of $r$ and 0 elsewhere, so (I1) holds and every arc from $r$ to $W$ is full, which is (I2); all labels in $W$ are 0, which gives (I3) and (I4).

**Push (line L6)** along $x = (v, w)$ with $w \in W$ moves at most $e(v)$, so $e(v)$ stays $\ge 0$ and (I1) holds. It may create the residual arc $(w, v)$ inside $W$, with $d(w) = d(v) - 1 \le d(v) + 1$, so (I3) holds. It creates no arc out of $S$ or a dormant set, so (I2) holds.

**Relabel (line L9).** Line L9 runs only if $v$ has no admissible arc, shares its label with another vertex of $W$, and has a residual arc into $W$. By (I3), each residual arc $(v, w)$ inside $W$ has $d(w) \ge d(v) - 1$, and not equal since no arc is admissible, so $d(w) \ge d(v)$. The new label $1 + \min d(w)$ is thus at least $d(v) + 1$; arcs out of $v$ satisfy (I3) by the choice, and arcs into $v$ only get looser. The new label is $d(w) + 1$ for a vertex $w \in W$, so by consecutiveness every value from $d(t)$ up to the new label is used, and the old label of $v$ is still used by another vertex; so (I4) holds. Since $v \ne t$ is never relabeled, $d(t)$ stays the least.

**Gap (line L7).** Let $R = \{w \in W : d(w) \ge d(v)\}$, where $v$ alone has the label $d(v)$. A residual arc from $x \in R$ to $y \in W \setminus R$ would have, by (I3), $d(x) \le d(y) + 1 \le d(v)$, so $d(x) = d(v)$ and $d(y) = d(v) - 1$; then $x = v$ and the arc is admissible, which is excluded. So $R$ has no residual arc to the new $W$, and as a new last dormant set it satisfies (I2). Since $d(t) \le d(v)$ and $t$ would share the label of $v$ if equal, $d(t) < d(v)$ and $t \notin R$. The remaining labels are those below $d(v)$, still consecutive. (I1) and (I3) are unaffected.

**Isolated vertex (line L8).** $v$ has no residual arc into $W$, so $\{v\}$ satisfies (I2) as a new last dormant set. It shares its label (else line L7 applied), so the label set of $W$ is unchanged, and $v \ne t$.

**Termination of a phase.** By (I4) the labels in $W$ lie in $[d(t), d(t) + n - 1]$, and $d(t)$ is fixed during a phase. Each relabel raises a label by at least 1, so a phase has at most $n^2$ relabels. Between relabels, each vertex scans its arcs with a current-arc pointer; a push saturates an arc or empties $v$. Saturated arcs $(v, w)$ become residual again only after a push along $(w, v)$, which needs $d(w) = d(v) + 1$, so $w$ must have been relabeled; hence there are finitely many saturating pushes. Each non-saturating push empties its vertex; with the potential $\sum_{v \text{ active}} d(v)$, which each such push lowers by at least 1 and each relabel or saturating push raises by at most $2n$, there are finitely many. Dormant moves shrink $W$. So the loop of line L5 stops, and then no vertex of $W \setminus \{t\}$ is active.

**The recorded cut is a minimum $S$-$t$ cut.** At line L10 let $X = V \setminus W$, the union of $S$ and the dormant sets, so $S \subseteq X$ and $t \notin X$. By (I2), no arc from $X$ to $W$ is residual: arcs from $X$ to $W$ are full, and arcs from $W$ to $X$ carry no flow, since flow on $(w, x)$ would make $(x, w)$ residual. So the net flow into $W$ is $c(X)$. Every vertex of $W$ other than $t$ has excess 0, so $e(t) = c(X)$. Now let $Y$ be any set with $S \subseteq Y$ and $t \notin Y$. The net flow into $V \setminus Y$ is at most $c(Y)$, and it equals $\sum_{v \notin Y} e(v)$, which by (I1) is at least $e(t)$, as $V \setminus Y$ contains no vertex of $S$. So $c(Y) \ge e(t) = c(X)$.

**Changing the sink (lines L11 to L14).** Moving $t$ into $S$ and pushing the full residual capacity of every arc from $t$ to a vertex outside $S$ keeps (I1) (the excess of $t$ may become negative, which is allowed in $S$, and the receivers gain excess) and makes every arc from $t$ to a later part full, so (I2) holds for $S$. Pushes from $S$ into a dormant set create residual arcs into $S$ only, which (I2) allows. Removing $t$, the least label, from $W$ keeps the labels consecutive. If $W$ becomes empty and a dormant set is left, the most recent one $D_k$ becomes $W$. Since its creation, no flow moved on arcs between two of its vertices, as only $W$ vertices push and line L12 pushes from $S$; so its labels still satisfy (I3), and they were consecutive when it was created, by the two cases above. By (I2) no older part has a residual arc into it, so (I2) still holds with $D_k$ as the last part. Line L14 then picks a least label, which gives (I4).

**Every vertex other than $r$ is a sink once.** Each phase moves one vertex from $W$ to $S$, and $W$ is nonempty at the start of each phase: at line L13 it is refilled while a dormant set remains, and when none remains every vertex is in $S$. After $n - 1$ phases $S = V$. So the sinks $t_1, \dots, t_{n-1}$ are exactly the vertices other than $r$.

**Rooted optimality.** Every recorded cut $X$ contains $r$ and not the current sink, so it is a nonempty proper set containing $r$. Let $X^*$ be a proper set containing $r$ of least $c(X^*)$. Since $X^* \ne V$, some sink lies outside it; let $t_i$ be the first. At phase $i$, $S = \{r, t_1, \dots, t_{i-1}\} \subseteq X^*$ and $t_i \notin X^*$, so the cut recorded in phase $i$ has capacity at most $c(X^*)$. Hence the least recorded cut is optimal among sets containing $r$.

**Global optimality (line L15).** Take $r = 0$. A nonempty proper set $X$ either contains 0, and is covered by the forward run, or does not, and then $V \setminus X$ contains 0 and $c(X) = c^{\mathrm{rev}}(V \setminus X)$, the capacity of the edges leaving $V \setminus X$ in the reversed graph, covered by the reverse run. Line L15 returns the better of the two, complementing the side found by the reverse run. So it returns a minimum directed cut. $\blacksquare$
