---
title: Correctness of KwikSort and its ratio for feedback arc set in tournaments
proves: [correctness]
status: full
---

Let $T$ be a tournament on a finite set $V$: for each pair $u \ne v$, exactly one of $u \to v$ and $v \to u$ holds. For a ranking $r$ of $V$, an arc $u \to v$ is backward when $r$ puts $v$ above $u$, and $\mathrm{fas}(r)$ is the number of backward arcs. Let $\mathrm{OPT}_T$ be the least $\mathrm{fas}(r)$. A triangle is a set $\{u, v, w\}$ whose three arcs form a directed cycle. A run of KWIKSORT is a tree of calls, and each call on a list with at least 2 members picks one pivot.

**Claim 1 (output).** KWIKSORT$(V, T)$ returns each member of $V$ exactly once. If the arcs of $T$ form a linear order, it returns that order.

*Proof.* By induction on $|V|$. Lines L3 and L4 put each $u \ne p$ in exactly one of $L$ and $R$, because exactly one of $u \to p$ and $p \to u$ holds, and $|L|, |R| < |V|$. If $T$ is a linear order, the members of $L$ are above $p$ and those of $R$ below it, and by induction each side is returned in order.

**Claim 2 (separation).** For $u \ne v$, there is exactly one call in which $u$ and $v$ are both in the list and either one of them is the pivot or they go to different sides. Their final order is decided in that call, and only there.

*Proof.* Both are in the first call. A call that keeps them together passes them to the same side, and the list gets shorter, so such calls end. The first call that does not keep them together decides the order: the pivot goes between the two sides, and the sides keep their order in the output.

**Claim 3 (backward arcs and triangles).** An arc $u \to v$ is backward in the output exactly when, in the call of Claim 2 for $u$ and $v$, the pivot $w$ is neither of them and $v \to w \to u$. So $\mathrm{fas}$ of the output equals the number of triangles $t$ for which some call has all of $t$ in its list and a member of $t$ as its pivot. Call such a triangle hit.

*Proof.* If the pivot is $u$, then $v$ goes right since $u \to v$, and the arc is forward. If the pivot is $v$, $u$ goes left, and the arc is forward. If the pivot $w$ is neither and the two go to different sides, then $v$ goes left and $u$ goes right exactly when $v \to w$ and $w \to u$, and then $u \to v \to w \to u$ is a triangle. In that call all of $\{u, v, w\}$ are in the list and $w$ is the pivot. Conversely, if a triangle $\{u, v, w\}$ with $u \to v \to w \to u$ is in a list whose pivot is $w$, then $v$ goes left and $u$ goes right, so $u \to v$ is backward. Before that call, no member of the triangle was a pivot and no pair of it was separated, so this is the separating call of Claim 2 for $u$ and $v$, and each hit triangle gives one backward arc. Different hit triangles give different arcs, because the arc determines the separating call and so its pivot.

**Claim 4 (ratio 3).** $\mathbb{E}[\mathrm{fas}(\mathrm{KWIKSORT}(V, T))] \le 3 \cdot \mathrm{OPT}_T$.

*Proof.* For a triangle $t$, let $q_t$ be the probability that $t$ is hit. Consider the first call whose pivot lies in $t$, if any. Before it, $t$ has stayed in one list or has been split. If it is still in one list, the pivot of that call is uniform over the list, so given that it lies in $t$, each of the three members of $t$ is the pivot with probability $1/3$. So for each member $w$ of $t$, the probability that $t$ is hit with pivot $w$ is $q_t / 3$. Fix an arc $e = (u, v)$. By Claim 3, the event that $t \ni e$ is hit with the pivot opposite $e$ is the event that $e$ is made backward by that pivot in its separating call. There is only one separating call for $e$, so these events are disjoint for the triangles that contain $e$, and $\sum_{t \ni e} q_t / 3 \le 1$.

Let $F$ be the set of backward arcs of an optimal ranking. Every triangle has at least one arc in $F$, since a ranking cannot follow all three arcs of a cycle. So

$$\sum_t \frac{q_t}{3} \le \sum_t \frac{q_t}{3} \, |t \cap F| = \sum_{e \in F} \sum_{t \ni e} \frac{q_t}{3} \le |F| = \mathrm{OPT}_T.$$

By Claim 3, $\mathbb{E}[\mathrm{fas}] = \sum_t q_t \le 3 \cdot \mathrm{OPT}_T$.

**Claim 5 (Smith set on top).** Let $S$ be a nonempty set with $x \to y$ for every $x \in S$ and $y \notin S$. Then KWIKSORT ranks every member of $S$ above every other candidate. For the majority tournament of a profile, this holds for the Smith set, and a Condorcet winner is ranked first.

*Proof.* Take $x \in S$ and $y \notin S$ and their call from Claim 2. If the pivot is $x$, $y$ goes right; if it is $y$, $x$ goes left. If the pivot $w$ is neither, $y$ left and $x$ right would need $y \to w$ and $w \to x$. If $w \in S$, then $w \to y$; if $w \notin S$, then $x \to w$. Both contradict this. So $x$ ends above $y$. The members of the Smith set have positive margins over the outsiders, so the tie rule of line L6 does not affect these arcs.

**Claim 6 (the best ballot).** The ballot $r_2$ of line L8 has $K(r_2) \le 2 \cdot \mathrm{OPT}$, so the output of line L9 does too.

*Proof.* Let $d$ be the Kendall tau distance, which is a metric, let $\pi^*$ be optimal, and let $v_1, \ldots, v_n$ be the ballots. Then $K(v_j) = \sum_i d(v_j, v_i) \le \sum_i (d(v_j, \pi^*) + d(\pi^*, v_i)) = n \, d(v_j, \pi^*) + \mathrm{OPT}$. The average of $d(v_j, \pi^*)$ over $j$ is $\mathrm{OPT}/n$, so the average of $K(v_j)$ is at most $2 \cdot \mathrm{OPT}$, and the least $K(v_j)$ is not larger.

**Claim 7 (time).** AGGREGATE runs in $O(n m^2)$ time and $O(m^2)$ space in the worst case.

*Proof.* The counts and the tournament take $O(n m^2)$ time and $O(m^2)$ space. A call of KWIKSORT on a list of $k \ge 2$ members compares the pivot with the $k - 1$ others in lines L3 and L4. A pair is compared only when one of its members is the pivot, and then the two are separated for good, so each pair is compared at most once and there are at most $m(m - 1)/2$ comparisons. There are at most $m$ calls with a pivot, and the lists of one level of the call tree are disjoint, so the other work is $O(m^2)$ too. Line L8 computes $n$ costs in $O(m^2)$ each, and line L9 two more. $\blacksquare$
