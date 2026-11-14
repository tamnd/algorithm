---
title: ASAP and ALAP are the pointwise earliest and latest schedules, and the frames are exact
proves: [correctness]
status: full
---

We use the notation of the page. $G = (V, E)$ has no cycle, every $\delta(v) \ge 1$, and a schedule for $L$ is a map $t : V \to \mathbb{Z}$ with $t(v) \ge 1$, $t(v) \ge t(u) + \delta(u)$ for every edge $(u, v)$, and $t(v) + \delta(v) - 1 \le L$ for every $v$.

For a path $p = x_0 x_1 \cdots x_k$, let $\delta(p) = \sum_{i=0}^{k} \delta(x_i)$. Let $\mathrm{in}(v)$ be the largest $\delta(p) - \delta(v)$ over paths $p$ that end at $v$, and let $\mathrm{out}(v)$ be the largest $\delta(p)$ over paths that start at $v$. The one-vertex path gives $\mathrm{in}(v) \ge 0$ and $\mathrm{out}(v) \ge \delta(v)$. The critical path length is $\mathrm{cp} = \max_v (\mathrm{in}(v) + \delta(v))$, which is also $\max_v \mathrm{out}(v)$.

**Lemma 1 (closed forms).** Lines L1 to L4 give $t_S(v) = 1 + \mathrm{in}(v)$. Lines L5 and L6 give $t_L(v) = L + 1 - \mathrm{out}(v)$.

*Proof.* Line L1 succeeds because $G$ has no cycle. In topological order, all predecessors of $v$ are done before $v$. By induction, line L3 gives $t_S(v) = \max(1, \max_{(u,v)} (1 + \mathrm{in}(u) + \delta(u)))$. A longest path ending at $v$ is either $v$ alone, with $\mathrm{in} = 0$, or a longest path ending at a predecessor $u$ followed by the edge $(u, v)$, with $\mathrm{in}(u) + \delta(u)$. So the right side is $1 + \mathrm{in}(v)$. The ALAP case is the same argument on the reverse graph: line L6 gives $\min(L + 1, \min_{(v,w)} (L + 1 - \mathrm{out}(w))) - \delta(v) = L + 1 - \delta(v) - \max(0, \max_{(v,w)} \mathrm{out}(w)) = L + 1 - \mathrm{out}(v)$. $\square$

**Lemma 2 (bounds).** Every schedule $t$ for $L$ has $t_S(v) \le t(v) \le t_L(v)$ for every $v$.

*Proof.* Let $p = x_0 \cdots x_k$ end at $x_k = v$. The edges give $t(x_{i}) \ge t(x_{i-1}) + \delta(x_{i-1})$, so $t(v) \ge t(x_0) + \delta(p) - \delta(v) \ge 1 + \delta(p) - \delta(v)$. Taking the largest such path gives $t(v) \ge 1 + \mathrm{in}(v) = t_S(v)$. Now let $p$ start at $x_0 = v$. In the same way $t(x_k) \ge t(v) + \delta(p) - \delta(x_k)$, and $t(x_k) + \delta(x_k) - 1 \le L$, so $t(v) \le L + 1 - \delta(p)$. Taking the largest path gives $t(v) \le L + 1 - \mathrm{out}(v) = t_L(v)$. $\square$

**Lemma 3 (both are schedules).** $t_S$ is a schedule for every $L \ge \mathrm{cp}$, with latency exactly $\mathrm{cp}$. $t_L$ is a schedule for $L$ exactly when $L \ge \mathrm{cp}$, and line L7 fails exactly when $L < \mathrm{cp}$.

*Proof.* Line L3 gives $t_S(v) \ge 1$ and $t_S(v) \ge t_S(u) + \delta(u)$ for every edge. The last step used is $\max_v (t_S(v) + \delta(v) - 1) = \max_v (\mathrm{in}(v) + \delta(v)) = \mathrm{cp}$ by Lemma 1. Line L6 gives $t_L(v) \le t_L(w) - \delta(v)$ for every edge $(v, w)$, and $t_L(v) + \delta(v) - 1 \le L$. So $t_L$ meets all conditions except possibly $t_L(v) \ge 1$. By Lemma 1, $\min_v t_L(v) = L + 1 - \max_v \mathrm{out}(v) = L + 1 - \mathrm{cp}$, which is at least 1 exactly when $L \ge \mathrm{cp}$. If $L < \mathrm{cp}$, no schedule exists at all, since a schedule has latency at least that of $t_S$ by Lemma 2. $\square$

**Theorem 1.** If $L \ge \mathrm{cp}$, $t_S$ and $t_L$ are schedules for $L$, and for every $v$, $t_S(v)$ is the least and $t_L(v)$ is the largest value of $t(v)$ over all schedules $t$ for $L$. If $L < \mathrm{cp}$, ALAP returns "infeasible" and no schedule exists. Line L9 returns $\mu(v) = t_L(v) - t_S(v) \ge 0$.

*Proof.* Lemmas 2 and 3. The mobility is nonnegative because $t_L$ is a schedule and Lemma 2 applies to it. $\square$

**Theorem 2 (the frames are exact).** Let $L \ge \mathrm{cp}$, let $v$ be an operation and let $t_S(v) \le s \le t_L(v)$. Then some schedule for $L$ has $t(v) = s$.

*Proof.* For each $x$, let $g(x)$ be the largest $\delta(p) - \delta(x)$ over paths $p$ from $v$ to $x$, or $-\infty$ if there is none. So $g(v) = 0$. Put $t(x) = \max(t_S(x), s + g(x))$. Then $t(v) = \max(t_S(v), s) = s$.

Precedence. Let $(x, y)$ be an edge. Then $t_S(y) \ge t_S(x) + \delta(x)$ by line L3. If $g(x) > -\infty$, the path to $x$ followed by the edge gives $g(y) \ge g(x) + \delta(x)$. So both terms of $t(y)$ are at least the matching term of $t(x)$ plus $\delta(x)$, and $t(y) \ge t(x) + \delta(x)$.

Range. $t(x) \ge t_S(x) \ge 1$. For the latency, $t_S(x) \le t_L(x)$ by Theorem 1. If $g(x) > -\infty$, take a path $p$ from $v$ to $x$ with $\delta(p) - \delta(x) = g(x)$. Then $\mathrm{out}(v) \ge g(x) + \mathrm{out}(x)$, because $p$ followed by a longest path from $x$ is a path from $v$. So $s + g(x) \le t_L(v) + g(x) = L + 1 - \mathrm{out}(v) + g(x) \le L + 1 - \mathrm{out}(x) = t_L(x)$. In both cases $t(x) \le t_L(x)$, so $t(x) + \delta(x) - 1 \le t_L(x) + \delta(x) - 1 \le L$. $\blacksquare$

**Fixed starts.** The variant on the page with fixed starts is the same pair of passes with extra lower and upper bounds on some operations. The correctness proof of [force-directed scheduling](/force-directed-scheduling/) shows that its frames are exact too.

**Termination.** Each line runs over a finite list, and no line repeats.
