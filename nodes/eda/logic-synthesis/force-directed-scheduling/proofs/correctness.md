---
title: Force-directed scheduling stops with a schedule that meets the latency bound
proves: [correctness]
status: full
---

This proof covers what FDS guarantees: it stops, and its output is a valid schedule for the latency bound $L$. It does not claim that the schedule needs the fewest units, which is false in general (see the Pitfalls on the page).

We use the notation of the page. A schedule for $L$ is a map $t$ with $t(v) \ge 1$, $t(v) \ge t(u) + \delta(u)$ for each edge $(u, v)$, and $t(v) + \delta(v) - 1 \le L$. For a partial map $\phi$ of fixed starts, a schedule meets $\phi$ when $t(v) = \phi(v)$ for every $v$ in its domain. TIME-FRAMES computes, in topological order, $a(v) = \max(1, \max_{(u,v)} a(u) + \delta(u))$, replaced by $\phi(v)$ when $v$ is fixed and reported as a clash when $\phi(v) < a(v)$. It computes $b(v) = \min(L + 1, \min_{(v,w)} b(w)) - \delta(v)$ in reverse order in the same way, with a clash when $\phi(v) > b(v)$. It reports "infeasible" on a clash or when some $a(v) > b(v)$.

**Lemma 1 (frames bound every schedule).** Every schedule $t$ for $L$ that meets $\phi$ has $a(v) \le t(v) \le b(v)$ for all $v$. So if TIME-FRAMES reports "infeasible", no such schedule exists.

*Proof.* By induction in topological order: $t(v) \ge 1$ and $t(v) \ge t(u) + \delta(u) \ge a(u) + \delta(u)$ for each edge, so $t(v)$ is at least the unfixed value of $a(v)$. If $v$ is fixed, $t(v) = \phi(v)$, which is then at least that value, so no clash happens and $t(v) = a(v)$. The upper bound is the same argument in reverse order. If a schedule exists, it lies in every frame, so no clash happens and $a(v) \le t(v) \le b(v)$. $\square$

**Lemma 2 (the frame bounds are schedules).** If TIME-FRAMES does not report "infeasible", then $a$ and $b$ are schedules for $L$ that meet $\phi$.

*Proof.* For $a$: $a(v) \ge 1$, and for each edge, $a(v) \ge a(u) + \delta(u)$ by construction when $v$ is free, and because $\phi(v) \ge$ that value when $v$ is fixed. For the latency, $b(v) + \delta(v) - 1 \le L$ by construction, and $a(v) \le b(v)$. So $a$ is a schedule, and it meets $\phi$ since $a(v) = \phi(v)$ for fixed $v$. For $b$: $b(v) \le b(w) - \delta(v)$ for each edge, in the same way, $b(v) + \delta(v) - 1 \le L$, and $b(v) \ge a(v) \ge 1$. $\square$

**Lemma 3 (frames are exact).** If TIME-FRAMES does not report "infeasible", then for every $v$ and every $s$ with $a(v) \le s \le b(v)$, some schedule for $L$ that meets $\phi$ has $t(v) = s$.

*Proof.* Let $g(x)$ be the largest $\delta(p) - \delta(x)$ over the paths $p$ from $v$ to $x$, with $\delta(p)$ the sum of the delays of the vertices of $p$, or $-\infty$ if there is no path. Put $t(x) = \max(a(x), s + g(x))$. Then $t(v) = \max(a(v), s) = s$.

Precedence. For an edge $(x, y)$, $a(y) \ge a(x) + \delta(x)$ by Lemma 2, and $g(y) \ge g(x) + \delta(x)$ when $g(x) > -\infty$. So $t(y) \ge t(x) + \delta(x)$.

Upper bounds. For every edge $(x, y)$, $b(x) \le b(y) - \delta(x)$, so along a path $p$ from $v$ to $x$, $b(x) \ge b(v) + \delta(p) - \delta(x)$. Hence $s + g(x) \le b(v) + g(x) \le b(x)$ when $g(x) > -\infty$. Also $a(x) \le b(x)$. So $t(x) \le b(x)$, and $t(x) + \delta(x) - 1 \le L$. Also $t(x) \ge a(x) \ge 1$.

Fixed starts. Let $x$ be fixed with $\phi(x) = c$. Then $a(x) = b(x) = c$, since $a(x)$ is set to $c$, $b(x)$ is set to $c$, and the bounds do not clash. So $c = a(x) \le t(x) \le b(x) = c$. $\square$

**Lemma 4 (the loop invariant).** At the start of each round of line L3, TIME-FRAMES on the current $\phi$ did not report "infeasible", and every schedule that meets the current $\phi$ is a schedule for $L$. In each round, every trial of line L8 succeeds, and the round adds at least one operation to $\phi$.

*Proof.* At the first round, line L2 returned unless the frames exist. Line L4 fixes $v$ at $s$ where its frame is $[s, s]$. By Lemma 1, every schedule that meets $\phi$ has $t(v) = s$, so the set of schedules that meet $\phi$ does not change, and by Lemma 3 it is not empty, so the frames with the new fixings exist and are the same. If line L5 does not return, some $v$ is free, and its frame has at least one step. For each such $v$ and each $s$ in its frame, Lemma 3 gives a schedule that meets $\phi$ and has $t(v) = s$, so by Lemma 1 TIME-FRAMES on $\phi \cup \{v \mapsto s\}$ does not report "infeasible". So every trial on line L8 succeeds, line L10 has at least one candidate, and line L11 adds a new operation to $\phi$, with frames that exist. $\square$

**Theorem.** If $L$ is less than the critical path length, FDS returns "infeasible" on line L2, and no schedule exists. Otherwise it stops after at most $|V|$ rounds and returns a schedule for $L$. The output depends only on the input.

*Proof.* With $\phi$ empty, the frames are the ASAP and ALAP schedules. By the [ASAP and ALAP](/asap-alap-scheduling/) correctness proof, they exist exactly when $L$ is at least the critical path length, and otherwise no schedule exists. By Lemma 4, each round fixes a new operation, so after at most $|V|$ rounds all operations are fixed, and line L5 returns $\phi$. At that point, the frames exist, so by Lemma 3 some schedule meets $\phi$. Since $\phi$ fixes every operation, that schedule is $\phi$ itself, and it is a schedule for $L$. The forces are computed in exact arithmetic, and line L10 breaks ties by a fixed order, so every step is a function of the input. $\blacksquare$
