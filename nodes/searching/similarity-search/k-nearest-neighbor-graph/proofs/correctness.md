---
title: Correctness of the k-nearest neighbor graph build and of its beam search
proves: [correctness]
status: full
---

Let $P = \{p_0, \dots, p_{n-1}\}$ with a distance $\delta$. Order pairs $(d, j)$ lexicographically, so that ties in distance go to the smaller index.

**Lemma 1 (build).** After line L4, $N(i)$ is the sequence of the $\min(k, n-1)$ least pairs $(\delta(p_i, p_j), j)$ over $j \ne i$, in increasing order.

*Proof.* We show by induction on the offers at line L3 that $H_i$ holds the $\min(k, t)$ least pairs among the first $t$ pairs offered. For $t = 0$ it is empty. Suppose it holds after $t$ offers and pair $a$ is offered next. If $|H_i| < k$, $a$ is added, and $H_i$ holds all $t + 1$ pairs. Otherwise $H_i$ holds the $k$ least of the first $t$, and its root $m$ is the largest of them. If $a < m$, the $k$ least of the first $t + 1$ pairs are $H_i \setminus \{m\} \cup \{a\}$, which is what the replacement gives. If $a > m$, the $k$ least are unchanged and $a$ is not added. All pairs are distinct since the indices are, so there is no third case. After all $n - 1$ offers, $H_i$ holds the $\min(k, n-1)$ least pairs, and line L4 lists them in increasing order. $\square$

For the search, write $f(x) = (\delta(q, p_x), x)$, and let "nearer" compare $f$. The heaps $C$ and $W$ order by $f$.

**Lemma 2 (termination and the set $W$).** SEARCH ends after at most $n$ passes of line L7. At every moment, $W$ holds the $\min(ef, |V|)$ nearest points of $V$, and every point of $W$ has entered $C$.

*Proof.* A point enters $V$ once, at line L5 or line L8, and enters $C$ only then, so $C$ receives at most $n$ points, and each pass of line L7 removes one. At line L5, $W$ is the $\min(ef, |S|)$ nearest points of $V = S$, and all of $S$ is in $C$. At line L8, a new point $e$ joins $V$. If $|W| < ef$ then $|V| \le ef$ before the step, $W = V$, and $e$ is added to $W$ and to $C$. Otherwise $W$ holds the $ef$ nearest points of the old $V$; if $e$ is nearer than the farthest of $W$, it replaces that point and enters $C$, and if not, $W$ is still the $ef$ nearest of the new $V$. So the invariant holds after each step. $\square$

**Lemma 3 (local minimum).** Let $w$ be the nearest point of $W$ when SEARCH stops. Then $w$ was extracted at line L7 and expanded at line L8. Hence every out-neighbor $e$ of $w$ is in $V$ and satisfies $f(e) > f(w)$; in particular $\delta(q, p_e) \ge \delta(q, p_w)$.

*Proof.* By Lemma 2, $w$ is the nearest point of $V$, and $w$ entered $C$. Suppose $w$ was never extracted. Then $w$ is still in $C$ when the loop stops. The loop cannot stop because $C$ is empty, so it stops at line L7 with an extracted $c$ such that $\delta(q, p_c) > \delta(q, \text{farthest of } W) \ge \delta(q, p_w)$. But $C$ is a min-heap that contains $w$, so the extracted $c$ satisfies $f(c) \le f(w)$, a contradiction. So $w$ was extracted, and since $w$ is the nearest point of $V$ and $W \ne \emptyset$, the test of line L7 did not stop the loop at $w$: $\delta(q, p_w) \le \delta(q, \text{farthest of } W)$ at that time, as $W$ then held points of $V$ and $w$ was already among them or nearer. So $w$ was expanded, all its out-neighbors entered $V$, and since $w$ is the nearest point of $V$, each of them is farther in the order $f$. $\square$

**Lemma 4 (reach).** If $ef \ge n$, then when SEARCH stops, $V$ is the set $R$ of points reachable from $S$ along directed edges.

*Proof.* $V \subseteq R$, since points enter $V$ only from $S$ or along an edge out of a point of $V$. With $ef \ge n \ge |V|$, the removal at line L8 never happens, the test $|W| < ef$ holds for every new point unless $|W| = n$, in which case all points are already in $V$; so every point of $V$ is in $W$ and in $C$. Every point $c$ extracted from $C$ is in $W$, so $\delta(q, p_c) \le \delta(q, \text{farthest of } W)$, and line L7 never stops the loop. So the loop runs until $C$ is empty, and every point of $V$ is expanded. Then $V$ contains $S$ and is closed under out-edges, so $R \subseteq V$. $\square$

**Theorem.** If $ef \ge n$, SEARCH$(q, k', ef, S)$ returns the $\min(k', |R|)$ nearest points to $q$ in $R$, in the order $f$.

*Proof.* By Lemma 4, $V = R$ at the end. By Lemma 2, $W$ holds the $\min(ef, |R|) = |R|$ nearest points of $R$, that is, all of $R$. Line L9 returns the first $k'$ of them in the order $f$. $\blacksquare$
