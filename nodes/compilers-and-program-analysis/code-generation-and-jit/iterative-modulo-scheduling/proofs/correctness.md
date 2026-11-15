---
title: MII is a lower bound on the initiation interval, and iterative modulo scheduling returns a legal modulo schedule
proves: [correctness, termination]
status: full
---

We prove four things. Every legal modulo schedule has $II \ge \mathrm{MII}$ (Theorem 1). Line L1 computes $\mathrm{ResMII}$ and $\mathrm{RecMII}$ exactly (Lemmas 2 to 4). Each call of ITERATIVE-SCHEDULE stops, and when it succeeds its result is a legal modulo schedule (Theorem 5). A legal modulo schedule gives a legal overlapped run of any number of iterations (Theorem 6). The search over $II$ is a heuristic: we do not claim that the returned $II$ is the least one.

## Setup

The loop body has operations $0, \dots, n - 1$. Operation $v$ has a reservation table $\mathrm{res}(v)$, a list of pairs $(r, o)$ with $o \ge 0$: in iteration $i$, $v$ holds one unit of resource $r$ in cycle $\mathrm{start} + o$. Resource $r$ has $c_r \ge 1$ units. An edge $e = (u, v, \delta, d)$ has a delay $\delta \in \mathbb{Z}$ and a distance $d \ge 0$. The edges of distance 0 form no cycle.

For an integer $II \ge 1$, a *modulo schedule* is a map $t$ from operations to integers $t(v) \ge 0$. It is *legal* if

- (D) $t(v) + II \cdot d \ge t(u) + \delta$ for every edge $(u, v, \delta, d)$, and
- (R) for every resource $r$ and every slot $k \in \{0, \dots, II - 1\}$, the number of pairs $(v, (r, o))$ with $(r, o) \in \mathrm{res}(v)$ and $t(v) + o \equiv k \pmod{II}$ is at most $c_r$.

Let $u_r$ be the number of entries $(r, \cdot)$ in all tables. For a cycle $C$ of edges, let $\delta(C)$ and $d(C)$ be the sums of its delays and distances. Every cycle has $d(C) \ge 1$, since the edges of distance 0 form no cycle. Define
$$\mathrm{ResMII} = \max_r \lceil u_r / c_r \rceil, \qquad \mathrm{RecMII} = \max\Big(0, \max_C \lceil \delta(C) / d(C) \rceil\Big), \qquad \mathrm{MII} = \max(1, \mathrm{ResMII}, \mathrm{RecMII}),$$
with the maximum over all cycles $C$, simple or not, and $\max \emptyset = 0$.

## Part 1. The lower bound

**Theorem 1.** If $t$ is a legal modulo schedule for $II$, then $II \ge \mathrm{MII}$.

*Proof.* $II \ge 1$ by definition.

*Resources.* Fix $r$. By (R), each of the $II$ slots holds at most $c_r$ of the $u_r$ entries of $r$, and each entry falls in exactly one slot. So $u_r \le II \cdot c_r$, that is $II \ge u_r / c_r$. As $II$ is an integer, $II \ge \lceil u_r / c_r \rceil$. This holds for every $r$, so $II \ge \mathrm{ResMII}$.

*Recurrences.* Fix a cycle $C = (e_1, \dots, e_m)$ with $e_j = (x_{j-1}, x_j, \delta_j, d_j)$ and $x_m = x_0$. Adding (D) over the edges of $C$ gives
$$\sum_{j=1}^m \big(t(x_j) - t(x_{j-1})\big) + II \cdot d(C) \ge \delta(C).$$
The first sum telescopes to $t(x_m) - t(x_0) = 0$. So $II \cdot d(C) \ge \delta(C)$, and as $d(C) \ge 1$, $II \ge \delta(C) / d(C)$, hence $II \ge \lceil \delta(C) / d(C) \rceil$. With $II \ge 1 > 0$, this gives $II \ge \mathrm{RecMII}$. $\square$

So the least $II$ of any legal modulo schedule, the optimum, is at least MII, and the $II$ that the algorithm returns is at least the optimum, once Theorem 5 shows that it is legal.

## Part 2. Computing MII

`res_mii` counts the entries of each resource and returns the largest $\lceil u_r / c_r \rceil$, which is $\mathrm{ResMII}$ by definition. For RecMII, give each edge the weight $w_{II}(e) = \delta - II \cdot d$ and call a cycle *positive* if its weight $\delta(C) - II \cdot d(C)$ is $> 0$.

**Lemma 2.** For $II \ge 0$, there is no positive cycle at $II$ if and only if $II \ge \mathrm{RecMII}$. In particular, "no positive cycle" holds for all $II$ from $\mathrm{RecMII}$ on, and for no smaller $II \ge 0$.

*Proof.* There is no positive cycle iff $II \cdot d(C) \ge \delta(C)$ for every cycle, iff $II \ge \delta(C) / d(C)$ for every cycle (as $d(C) \ge 1$), iff $II \ge \lceil \delta(C)/d(C) \rceil$ for every cycle (as $II$ is an integer). With $II \ge 0$, this is $II \ge \mathrm{RecMII}$. $\square$

**Lemma 3.** `min_dist` returns a matrix with some diagonal entry $M[i][i] > 0$ if and only if there is a positive cycle.

*Proof.* Two invariants of the Floyd-Warshall loop, in the max-plus form of the code.

(a) Every finite entry $M[i][j]$ is the weight of some walk from $i$ to $j$ with at least one edge. True at the start, where $M[i][j]$ is the weight of the heaviest edge from $i$ to $j$. An update sets $M[i][j] = M[i][k] + M[k][j]$, the weight of the two walks joined at $k$.

(b) After the round for $k$, $M[i][j] \ge w(P)$ for every walk $P$ from $i$ to $j$ with at least one edge whose inner vertices are distinct, are different from $i$ and $j$, and are at most $k$. (A walk with $i = j$ is a cycle through $i$.) Before the first round, such a walk has no inner vertex and is one edge, and the claim holds. In the round for $k$, a walk $P$ that has $k$ as an inner vertex splits at $k$ into $P_1$ from $i$ to $k$ and $P_2$ from $k$ to $j$, whose inner vertices are distinct, are at most $k - 1$ and do not contain $k$. By the claim for round $k - 1$, $M[i][k] \ge w(P_1)$ and $M[k][j] \ge w(P_2)$ when the update for $(i, j)$ runs, since entries never decrease. So after the update $M[i][j] \ge w(P_1) + w(P_2) = w(P)$. A walk without $k$ as an inner vertex is covered by round $k - 1$.

If there is a positive cycle, there is a positive simple cycle: a closed walk splits into simple cycles whose weights add up to its weight, so one of them is positive. A simple cycle through its vertex $i$ satisfies the condition of (b), so after the last round $M[i][i] \ge$ its weight $> 0$. Conversely, if $M[i][i] > 0$, by (a) it is the weight of a closed walk, which splits into simple cycles, one of them positive. $\square$

**Lemma 4.** `rec_mii` returns $\mathrm{RecMII}$.

*Proof.* Let $h_0 = \sum_e \max(\delta_e, 0)$. At $II = h_0$, every cycle has $\delta(C) - h_0 d(C) \le h_0 - h_0 d(C) \le 0$, since $\delta(C) \le h_0$ and $d(C) \ge 1$. So $\mathrm{RecMII} \le h_0$ by Lemma 2. The binary search keeps the invariant $\mathrm{lo} \le \mathrm{RecMII} \le \mathrm{hi}$. It holds at the start with $\mathrm{lo} = 0$. If the test at $\mathrm{mid}$ finds a positive cycle (Lemma 3), then $\mathrm{mid} < \mathrm{RecMII}$ by Lemma 2 and $\mathrm{lo} = \mathrm{mid} + 1$ keeps it. Otherwise $\mathrm{mid} \ge \mathrm{RecMII}$ and $\mathrm{hi} = \mathrm{mid}$ keeps it. The interval shrinks in each step, and at the end $\mathrm{lo} = \mathrm{hi} = \mathrm{RecMII}$. $\square$

## Part 3. One attempt at a fixed II

Fix $II \ge \mathrm{MII}$ and a budget $b$. By Lemma 2, there is no positive cycle at $II$. In particular, every self-loop $(v, v, \delta, d)$ has $\delta - II \cdot d \le 0$, so (D) holds for it for every value of $t(v)$. The code leaves self-loops out of the lists `preds` and `succs`.

*Heights (line L4).* `height_r` runs Bellman-Ford rounds of $h(u) \leftarrow \max(h(u), h(v) + w_{II}(e))$ from $h = 0$. As there is no positive cycle, the values are bounded by the longest simple path weights, and $n$ rounds reach the fixed point. The heights only fix the order of line L6. The proof below does not use them, so any order gives a legal result.

*The check before line L4.* The attempt fails at once if some operation $v$ alone does not satisfy (R) at $t(v) = 0$, which is the same as at every start, since a shift of the start shifts all slots of $v$ by the same amount modulo $II$. Otherwise every operation fits into an empty table.

The state is the partial map $t$ on the scheduled set $S$, the map $\mathrm{prev}$, and the table $\mathrm{MRT}$, which maps each pair $(r, k)$ to a list of operations.

**Invariant.** Before each step of the loop of line L5:

- (I1) $\mathrm{MRT}[(r, k)]$ lists each $v \in S$ once for each entry $(r, o) \in \mathrm{res}(v)$ with $t(v) + o \equiv k$, and nothing else;
- (I2) every list $\mathrm{MRT}[(r, k)]$ has at most $c_r$ items;
- (I3) every edge $(u, v, \delta, d)$ with $u \ne v$ and $u, v \in S$ has $t(v) + II \cdot d \ge t(u) + \delta$;
- (I4) $t(v) \ge 0$ for every $v \in S$.

**Theorem 5.** Each call of ITERATIVE-SCHEDULE stops after at most $b$ steps. If it returns $t$, then $t$ is a legal modulo schedule for $II$.

*Proof.* *Initialization.* $S$ and $\mathrm{MRT}$ are empty, so (I1) to (I4) hold.

*Unscheduling keeps (I1) to (I4).* `unschedule(w)` removes $w$ from $S$ and removes exactly its entries from the table, so (I1) holds. Lists only get shorter, and constraints between members of $S$ only disappear.

*Maintenance.* Let $v \notin S$ be the operation of line L6 and $S_0$ the scheduled set at that moment. Line L7 sets $E = \max(0, \max \{ t(p) + \delta - II \cdot d : (p, v, \delta, d), p \ne v, p \in S_0 \})$, and every later choice $s$ satisfies $s \ge E$: line L8 takes $s \in [E, E + II - 1]$, and line L9 takes $E$ or $\mathrm{prev}(v) + 1$, the latter only when $E \le \mathrm{prev}(v)$. So $s \ge E \ge 0$.

*Resources.* If line L8 found $s$, then `_fits` says that every list $(r, k)$ that $v$ needs, with $c$ new entries, has at most $c_r - c$ items, so adding $v$ keeps (I2). If line L9 chose $s$, line L10 removes items from each such list while it has more than $c_r - c$ items. Each removal makes the list shorter, and $c \le c_r$ by the check before line L4, so the loop stops with at most $c_r - c$ items. Removing an operation never lengthens another list. So after line L10, adding the entries of $v$ keeps (I2), and line L12 adds exactly these entries, so (I1) holds.

*Dependences.* After lines L10 and L11 the scheduled set is $S_1 \subseteq S_0$. For an edge $(p, v, \delta, d)$ with $p \in S_1$, $p \ne v$: $p \in S_0$, so $s \ge E \ge t(p) + \delta - II \cdot d$. For an edge $(v, w, \delta, d)$ with $w \in S_1$, $w \ne v$: line L11 removed every $w$ with $t(w) < s + \delta - II \cdot d$, so $t(w) + II \cdot d \ge s + \delta$. Edges between two members of $S_1$ held before by (I3). So (I3) holds with $t(v) = s$, and (I4) holds as $s \ge 0$.

*Termination.* Each step decreases the budget by 1, and the loop stops when the budget is 0 or $S$ holds all operations. Line L10 stops as shown, and lines L6 to L8 and L11 are finite.

*Result.* The call returns $t$ only when $S$ holds all operations. Then (I1) and (I2) give (R), (I3) and the remark on self-loops give (D), and (I4) gives $t \ge 0$. $\square$

**Corollary.** If `modulo_schedule` returns $(II, t, \mathrm{MII})$, then $t$ is a legal modulo schedule for $II$, and $\mathrm{MII} \le II^* \le II$ for the least $II^*$ of any legal modulo schedule.

*Proof.* The loop of line L2 starts at MII, computed exactly by Lemma 4, so every attempt has $II \ge \mathrm{MII}$ and Theorem 5 applies to the one that returns. Theorem 1 gives $\mathrm{MII} \le II^*$, and $II^* \le II$ because $t$ is legal. The loop of line L2 is finite, since it stops at `max_ii`, so `modulo_schedule` stops: it returns or raises an error. $\square$

## Part 4. The overlapped run

**Theorem 6.** Let $t$ be a legal modulo schedule for $II$, and run iterations $i = 0, 1, \dots, N - 1$, with operation $v$ of iteration $i$ starting at cycle $\sigma(v, i) = i \cdot II + t(v)$. Then for every edge $(u, v, \delta, d)$ and every $i$ with $i + d < N$, $\sigma(v, i + d) \ge \sigma(u, i) + \delta$. And in every cycle $c$, at most $c_r$ units of each resource $r$ are in use.

*Proof.* $\sigma(v, i + d) - \sigma(u, i) = t(v) + II \cdot d - t(u) \ge \delta$ by (D). For resources, an entry $(r, o)$ of $v$ in iteration $i$ uses $r$ in cycle $i \cdot II + t(v) + o$, which is congruent to $t(v) + o$ modulo $II$. So all uses of $r$ in cycle $c$ come from entries in the slot $c \bmod II$. Two uses in cycle $c$ from the same entry $(v, (r, o))$ would have $i \cdot II + t(v) + o = i' \cdot II + t(v) + o$, so $i = i'$, the same use. So the uses of $r$ in cycle $c$ are at most the number of entries in slot $c \bmod II$, which is at most $c_r$ by (R). $\blacksquare$
