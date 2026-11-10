---
title: Delta-stepping computes the shortest distances, with at most l + 1 phases per bucket
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, A)$ is a directed graph with $n$ vertices, $m$ arcs and weights $w(a) \ge 0$; $s$ is the source and $\Delta > 0$. $d(v)$ is the true distance from $s$, and $dist(v)$ is the tentative distance kept by the algorithm. An arc is light if $w \le \Delta$ and heavy otherwise. Bucket $B[i]$ holds the vertices $v$ with $dist(v) \in [i\Delta, (i + 1)\Delta)$ that wait to be handled. To handle a set in a phase (lines L6 to L8) means to take it out of the bucket and relax its light arcs from the current $dist$ values. For each reachable $v$, fix a shortest path $P_v$ from $s$ to $v$ with the fewest arcs. $l$ is the largest number of arcs on a sub-path of some $P_v$ whose weight is less than $\Delta$. $k$ is the number of buckets that line L3 selects.

**Lemma 1 (safety).** At all times, $dist(v) \ge d(v)$ for every $v$, and a finite $dist(v)$ is the weight of a walk from $s$ to $v$.

*Proof.* It holds after line L1. A relaxation sets $dist(v)$ to $dist(u) + w(u, v)$, the weight of a walk to $u$ followed by the arc $(u, v)$. $\square$

**Lemma 2 (no bucket below the current one).** Let bucket $i$ be selected in line L3, and suppose that every vertex $u$ with $d(u) < i\Delta$ has $dist(u) = d(u)$ and has had all its arcs relaxed with this value. Then while bucket $i$ is current, every vertex that is in $B[i]$ has $d(v) \in [i\Delta, (i + 1)\Delta)$, no relaxation puts a vertex in a bucket below $i$, and the heavy relaxations of line L10 put vertices only in buckets above $i$.

*Proof.* Let $v \in B[i]$. If $d(v) < i\Delta$, then $dist(v) = d(v) < i\Delta$ by the hypothesis, so $v$ is not in $B[i]$. So $d(v) \ge i\Delta$, and $d(v) \le dist(v) < (i + 1)\Delta$ by Lemma 1. A relaxation changes $dist(v)$ only to a value at least $d(v)$, by Lemma 1. If $d(v) < i\Delta$, then $dist(v) = d(v)$ already, so nothing changes; otherwise the new value is at least $i\Delta$. A heavy arc $(u, v)$ relaxed in line L10 has $u$ handled in bucket $i$, so $dist(u) \ge i\Delta$ and $dist(u) + w(u, v) > i\Delta + \Delta$. $\square$

**Lemma 3 (one bucket).** Under the hypothesis of Lemma 2, bucket $i$ stays empty after at most $l + 1$ phases. Every vertex $v$ with $d(v) \in [i\Delta, (i + 1)\Delta)$ is handled in bucket $i$ with $dist(v) = d(v)$, it is handled at most $l + 1$ times in all, and no vertex outside this range is handled in bucket $i$.

*Proof.* The last claim is Lemma 2. Let $d(v) \in [i\Delta, (i + 1)\Delta)$, and let $x_0, x_1, \ldots, x_h = v$ be the part of $P_v$ from its first vertex $x_0$ with $d(x_0) \ge i\Delta$. This part has weight $d(v) - d(x_0) < \Delta$, so its arcs are light and $h \le l$. The vertices $x_j$ all have $d(x_j) \in [i\Delta, d(v)]$, since $d$ does not decrease along a shortest path.

First, $dist(x_0) = d(x_0)$ when bucket $i$ is selected: either $x_0 = s$ and $dist(s) = 0$ from line L1, or the vertex $p$ before $x_0$ on $P_v$ has $d(p) < i\Delta$, and the arc $(p, x_0)$ was relaxed with $dist(p) = d(p)$. Then $x_0 \in B[i]$, as no vertex was handled in bucket $i$ yet.

Claim: at the start of phase $j + 1$, $dist(x_j) = d(x_j)$, and if $x_j$ is not in $B[i]$ then it was handled in an earlier phase with $dist(x_j) = d(x_j)$. For $j = 0$ this was just shown. A vertex takes the value $d(x_j)$ in a relaxation, which puts it in $B[i]$; after that, its distance does not change, so it leaves $B[i]$ only when it is handled with this value. Now let the claim hold for $j - 1$. Then $x_{j-1}$ is handled with its final value in some phase at most $j$, which relaxes the light arc $(x_{j-1}, x_j)$ to $d(x_{j-1}) + w = d(x_j)$. So at the start of phase $j + 1$, $dist(x_j) = d(x_j)$, and the rest of the claim follows as above.

So $v = x_h$ has its final value at the start of phase $h + 1$, and it is handled with this value in a phase at most $h + 1$; after that, it never comes back to $B[i]$. Each earlier time that $v$ was handled was in a different phase at most $h$, so $v$ is handled at most $h + 1 \le l + 1$ times. At the start of phase $l + 2$, every vertex that can be in $B[i]$ was already handled with its final value, so $B[i]$ is empty. $\square$

**Theorem 1 (correctness and termination).** DELTA-STEPPING stops after selecting $k \le n$ buckets, and then $dist(v) = d(v)$ for every $v$, with $dist(v) = \infty$ exactly for the vertices that $s$ does not reach.

*Proof.* Invariant: when line L3 selects bucket $i$, every vertex $u$ with $d(u) < i\Delta$ has $dist(u) = d(u)$ and has had all its arcs relaxed with this value. It holds for the first bucket, $i = 0$, since no distance is negative.

Let it hold for bucket $i$. By Lemma 3, after the phases of bucket $i$, every $v$ with $d(v)$ in its range has $dist(v) = d(v)$, it was handled with this value, which relaxed its light arcs, and it is in the set $R$, so line L10 relaxes its heavy arcs with this value. By Lemma 2, no later relaxation fills a bucket at or below $i$. Let $i'$ be the next bucket that line L3 selects, and suppose some $v$ has $(i + 1)\Delta \le d(v) < i'\Delta$. Let $x$ be the first vertex on $P_v$ with $d(x) \ge (i + 1)\Delta$. The vertex before $x$ has its final value and its arcs relaxed, so $dist(x) = d(x)$, and $x$ is in the bucket $\lfloor d(x)/\Delta \rfloor < i'$, which is above $i$ and not empty. That contradicts the choice of $i'$. So the invariant holds for $i'$.

Each selected bucket holds a vertex whose true distance is in its range (Lemma 2), and these ranges are disjoint, so $k \le n$, and each bucket has at most $l + 1$ phases by Lemma 3. When no bucket is left, suppose that some reachable $v$ has $dist(v) > d(v)$, and take such a $v$ with the fewest arcs on $P_v$. Its predecessor on $P_v$ has its final value and was handled in the bucket of its distance, so the arc to $v$ was relaxed with this value, and $dist(v) \le d(v)$. That is a contradiction. With Lemma 1, $dist = d$, and an unreachable vertex is never relaxed, so it keeps $\infty$. $\blacksquare$

**Theorem 2 (cost).** In the work-span model with a minimum concurrent write, or a sort of the requests, in $O(\log n)$ span per phase, the work is $W = O((n + m)(l + 1) + k \log n)$, and the span is $S = O(k (l + 1) \log n)$.

*Proof.* By Lemma 3, a vertex is handled at most $l + 1$ times, all in the bucket of its distance, and each time costs $O(1)$ plus its number of light out-arcs. It is in one set $R$, so its heavy arcs are read once. The moves of vertices between buckets are at most one per relaxation. Finding the smallest nonempty bucket costs $O(\log n)$ per selected bucket, with a heap of bucket indices. A phase, and the heavy step of a bucket, take $O(\log n)$ span for the minimum writes and the pack of the next bucket, and there are at most $k(l + 1)$ phases and $k$ heavy steps. $\blacksquare$
