---
title: 0-1 BFS returns the distances and a shortest-path tree
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ have weights $w : E \to \{0, 1\}$ and source $s$. A *copy* in the deque $D$ is a pair $(v, k)$, where $k$ is the value of $d[v]$ when line L2, L10 or L11 pushed it. Line L4 pops a copy, and line L5 skips it when $v$ is already finished.

**Fact 1 (labels are path weights).** At every moment, if $d[v] < \infty$ then $d[v] = w(p)$ for some walk $p$ from $s$ to $v$, so $d[v] \ge \delta(s, v)$. Also, for $v \ne s$ with $d[v] < \infty$, $d[v] = d[\pi[v]] + w(\pi[v], v)$ held at the moment of the last change of $d[v]$, and $d[\pi[v]]$ has not changed since.

*Proof.* Line L2 sets $d[s] = 0$, the weight of the empty walk. Line L9 sets $d[v] = d[u] + w(u, v)$, which is the weight of a walk to $u$ extended by the arc $(u, v)$. The second claim holds because line L9 runs only while $u$ is scanned, after line L6 finished $u$, and the label of a finished vertex never changes: by Fact 3 below, after $u$ is finished no relaxation can lower $d[u]$. $\square$

**Fact 2 (invariant D).** Before each test of line L3, if the keys of the copies in $D$, front to back, are $k_1, \ldots, k_r$ with $r \ge 1$, then $k_1 \le k_2 \le \cdots \le k_r \le k_1 + 1$. Moreover, while a vertex $u$ is scanned after the pop of a copy with key $k$, every key in $D$ lies in $[k, k + 1]$ and the keys stay sorted.

*Proof.* At the start $D$ holds one copy, so (D) holds. Suppose (D) holds and line L4 pops the copy with key $k = k_1$. The rest of $D$ is sorted with keys in $[k, k + 1]$. If line L5 skips the copy, (D) holds again for the rest. Otherwise $u$ is scanned. We show below that the key of the popped copy equals $d[u]$, so each relaxation sets $d[v] = k + w(u, v)$. A push to the front of key $k$ (when $w = 0$) puts a key no larger than every key in $D$ at the front, and it is still at least $k$, so $D$ stays sorted in $[k, k + 1]$. A push to the back of key $k + 1$ (when $w = 1$) puts a key at least every key in $D$ at the back, and it is $k + 1$, so $D$ stays sorted in $[k, k + 1]$. When the scan ends, the front key $k_1'$ is at least $k$ and every key is at most $k + 1 \le k_1' + 1$, so (D) holds.

It remains to see that the popped copy $(u, k)$ that is not skipped has $k = d[u]$. Each push of $u$ follows a strict drop of $d[u]$, so the copies of $u$ ever pushed have strictly decreasing keys, and the last one has key $d[u]$. None of them was popped and scanned before, because $u$ is not finished. All of them are therefore still in $D$, since a copy leaves $D$ only through line L4. The popped copy has the least key in $D$, so $k \le d[u]$; and every copy of $u$ has key at least $d[u]$, so $k \ge d[u]$. $\square$

**Fact 3 (scans in key order).** Let $u_1, u_2, \ldots$ be the vertices in the order line L6 finishes them, with labels $d[u_1], d[u_2], \ldots$ at those moments. Then $d[u_1] \le d[u_2] \le \cdots$, and after $u_i$ is finished, no relaxation lowers $d[u_i]$.

*Proof.* By Fact 2, the popped keys never decrease: each pop takes the least key, and the scan of a vertex with key $k$ only pushes keys at least $k$. The finished labels are popped keys, so they are nondecreasing. After $u_i$ is finished with label $d[u_i]$, each later relaxation sets a label to (a later finished label) $+ w \ge d[u_i]$, which is not less than $d[u_i]$, so the strict test of line L8 fails for $v = u_i$. $\square$

**Lemma (finished labels are distances).** When line L6 finishes $u$, $d[u] = \delta(s, u)$.

*Proof.* Suppose not, and let $u$ be the first vertex finished with $d[u] \ne \delta(s, u)$. By Fact 1, $d[u] > \delta(s, u)$, so $\delta(s, u) < \infty$ and there is a shortest path $p$ from $s$ to $u$. Since $u \ne s$ ($s$ is finished first, with $d[s] = 0 = \delta(s, s)$ as all weights are nonnegative), the path $p$ leaves the set $F$ of vertices finished before $u$. Let $(x, y)$ be the first arc of $p$ with $x \in F$ and $y \notin F$. By the choice of $u$, $d[x] = \delta(s, x)$, and when $x$ was scanned line L8 made $d[y] \le d[x] + w(x, y) = \delta(s, y)$, where the last equality is optimal substructure along $p$. So $d[y] = \delta(s, y)$ by Fact 1, and a copy of $y$ with key $\delta(s, y)$ was pushed (or $y$ already had that label and a copy with that key). That copy is still in $D$ or has been popped; it was not popped, since $y \notin F$ and a pop of a copy with key $d[y]$ would have finished $y$. Weights are nonnegative, so $\delta(s, y) \le \delta(s, u) < d[u]$. But $u$ was popped with the least key in $D$, which is at most $\delta(s, y)$, so $d[u] \le \delta(s, y)$, a contradiction. $\square$

**Termination.** Each pop removes one copy, and each push follows a successful relaxation of line L8. A vertex is scanned at most once, by lines L5 and L6, so line L8 runs at most $m$ times, and at most $m + 1$ copies are ever pushed. So the loop of line L3 runs at most $m + 1$ times and stops.

**Theorem.** When ZERO-ONE-BFS returns, $d[v] = \delta(s, v)$ for every $v \in V$, and for every $v \ne s$ with $d[v] < \infty$, the parent $\pi[v]$ satisfies $d[\pi[v]] + w(\pi[v], v) = d[v]$, and following parents from $v$ reaches $s$.

*Proof.* If $v$ is reachable, every vertex on a shortest path to $v$ is finished: by induction along the path, when a vertex is finished its successor gets a finite label and a copy, and that copy is popped before $D$ is empty. So $v$ is finished, and the lemma gives $d[v] = \delta(s, v)$. If $v$ is not reachable, Fact 1 shows $d[v]$ stays $\infty$, which is $\delta(s, v)$. For the parents, Fact 1 gives $d[v] = d[\pi[v]] + w(\pi[v], v)$ at the last change of $d[v]$, and $\pi[v]$ was finished before that change, with its final label. So $\pi[v]$ was finished strictly before $v$, and following parents walks back through vertices finished earlier and earlier. It cannot repeat a vertex, and the only finished vertex without a parent is $s$, so it reaches $s$. $\blacksquare$
