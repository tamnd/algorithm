---
title: SPFA returns the distances or reports a reachable negative cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ have $n$ vertices, real weights $w$ and source $s$. Line numbers refer to the pseudocode of SPFA on the main page. A *label change* is one execution of line L7.

**Walks behind the labels.** Attach to each vertex $v$ with $d(v) < \infty$ a walk $W(v)$ from $s$ to $v$: at the start $W(s) = \langle s \rangle$, and at each label change of $v$ through the arc $(u, v)$, set $W(v)$ to the current $W(u)$ followed by $(u, v)$. These walks are only for the proof.

**Fact 1.** At all times, for every $v$ with $d(v) < \infty$, $d(v) = w(W(v))$ and $k(v)$ is the number of arcs of $W(v)$.

*Proof.* True at the start, since $d(s) = 0 = w(\langle s \rangle)$ and $k(s) = 0$. A label change of $v$ sets $d(v) = d(u) + w(u, v)$ and $k(v) = k(u) + 1$, which by induction are the weight and the arc count of $W(u)$ followed by $(u, v)$. Other labels do not change. $\square$

**Fact 2.** Labels only decrease, and each label change of $v$ makes $d(v)$ strictly smaller.

*Proof.* Line L7 runs only when the test of line L6 holds. $\square$

**Lemma 1 (repeated vertices).** If at some time $W(v) = \langle v_0, \ldots, v_k \rangle$ has $v_i = v_j$ with $i < j$, then the closed walk $\langle v_i, \ldots, v_j \rangle$ has negative weight, and it is reachable from $s$.

*Proof.* By construction, the prefix $P_\ell = \langle v_0, \ldots, v_\ell \rangle$ of $W(v)$ was the walk $W(v_\ell)$ at some time $t_\ell$, and $w(P_\ell)$ was the label $d(v_\ell)$ at that time, by Fact 1. Here $t_\ell$ is the time of the label change that created $W(v_\ell)$, or the start for $\ell = 0$, and $t_0 < t_1 < \cdots < t_k$, because $W(v_{\ell+1})$ was built from the walk $W(v_\ell)$ that existed at that moment. The vertex $x = v_i = v_j$ has a label change at time $t_j > t_i$ (if $j \ge 1$, then $t_j$ is a label change). By Fact 2, the label of $x$ after time $t_j$ is strictly smaller than its label just before $t_j$, which is at most its label at time $t_i$. So $w(P_j) < w(P_i)$. Since $P_j$ is $P_i$ followed by the closed walk $C = \langle v_i, \ldots, v_j \rangle$, $w(C) = w(P_j) - w(P_i) < 0$. $C$ starts at $v_i$, which $P_i$ reaches from $s$. $\square$

A negative closed walk contains a negative cycle (see [negative cycle](/negative-cycle/)), so we get:

**Corollary 1.** If line L8 returns "negative cycle", then a negative cycle is reachable from $s$.

*Proof.* At that moment $k(v) \ge n$, so $W(v)$ has at least $n + 1$ vertices by Fact 1 and repeats one. Apply Lemma 1. $\square$

**Lemma 2 (queue invariant).** At the test of line L3, every arc $(u, v)$ with $d(u) < \infty$ and $d(u) + w(u, v) < d(v)$ has $u$ in $Q$.

*Proof.* At the start only $d(s)$ is finite, and $s$ is in $Q$. Consider one iteration that dequeues $u$. Line L5 scans every arc out of $u$, and after its relaxation each such arc $(u, v)$ satisfies $d(v) \le d(u) + w(u, v)$; later relaxations in the same scan only lower other labels $d(v')$ with $v' \ne u$, or lower $d(u)$ itself through a self-loop. In the last case line L9 puts $u$ back in $Q$. Every vertex $v$ whose label goes down is in $Q$ after line L9, which covers the arcs out of $v$ that may now be violated. Lowering $d(v)$ cannot violate an arc into $v$. So the invariant holds again at the next test. $\square$

**Lemma 3 (termination).** SPFA terminates.

*Proof.* While line L8 has not returned, every $k(v) \le n - 1$, so by Fact 1 every finite label is the weight of a walk from $s$ with at most $n - 1$ arcs. There are finitely many such walks, so the labels take values in a finite set. By Fact 2 each vertex has finitely many label changes, and so line L9 adds finitely many vertices to $Q$. Each iteration of line L3 removes one vertex from $Q$, so the loop ends. $\square$

**Theorem.** If a negative cycle is reachable from $s$, SPFA returns "negative cycle". Otherwise it returns $d(v) = \delta(s, v)$ for every $v$, with $d(v) = \infty$ exactly when $v$ is not reachable from $s$, and $\pi$ is a shortest-path tree.

*Proof.* By Lemma 3, SPFA either returns at line L8 or reaches line L10 with $Q$ empty. Suppose it reaches line L10. By Fact 1 only reachable vertices have finite labels, and every reachable vertex has one: along a path from $s$, an arc $(u, v)$ with $d(u) < \infty = d(v)$ would be violated, against Lemma 2. So, by Lemma 2, $d(v) \le d(u) + w(u, v)$ holds on every arc whose tail is reachable.

*No negative cycle is reachable.* Let $C = \langle c_0, \ldots, c_\ell = c_0 \rangle$ be a cycle through a reachable vertex. All its vertices are reachable, so their labels are real, and summing $d(c_i) \le d(c_{i-1}) + w(c_{i-1}, c_i)$ over $i = 1, \ldots, \ell$ gives $0 \le w(C)$.

*The labels are the distances.* The label $d(s)$ never changed: a change would make $d(s) < 0$ the weight of a closed walk from $s$ by Fact 1, a negative closed walk reachable from $s$, which contains a negative cycle reachable from $s$. So $d(s) = 0$, each finite label is the weight of a walk from $s$, and the triangle inequality holds on every arc with a reachable tail. Theorem B of the [optimality conditions](/shortest-path-optimality-conditions/) gives $d = \delta(s, \cdot)$.

So if a negative cycle is reachable from $s$, SPFA cannot reach line L10, and it returns "negative cycle". If no negative cycle is reachable, Corollary 1 shows that line L8 never returns, and the run ends at line L10 with the distances. For the tree: each parent arc $(\pi(v), v)$ was tight when it was set, $d(\pi(v))$ can only have gone down since then, and by the optimality conditions it cannot go below $d(v) - w(\pi(v), v)$; so every parent arc is tight at the end, and with the distances final, the parents form a [shortest-path tree](/shortest-path-tree/) by its predecessor-subgraph property. $\square$

**Running time.** Define passes: pass 0 is the dequeue of $s$, and pass $j + 1$ dequeues the vertices in $Q$ at the end of pass $j$. *Claim:* a label set during pass $j$ has $k(v) \ge j + 1$. For $j = 0$, $k(s) = 0$, so $k(v) = 1$. For pass $j \ge 1$, the dequeued vertex $u$ entered $Q$ during pass $j - 1$, so its current label was set during pass $j - 1$ or later, and $k(u) \ge j$ by induction on time; hence $k(v) = k(u) + 1 \ge j + 1$. So a label set during pass $n - 1$ has $k(v) \ge n$ and line L8 returns. There are at most $n$ passes. Each vertex is in $Q$ at most once at a time, so it is dequeued at most once per pass, and a pass scans each arc at most once. The total time is $O(n(n' + m))$, where $n' \le \min(n, m + 1)$ is the number of vertices reachable from $s$, which is $O(nm)$. $\blacksquare$
