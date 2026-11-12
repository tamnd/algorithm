---
title: YDS produces a feasible schedule of minimum energy
proves: [correctness, termination]
status: full
---

Jobs have windows $[r_j, d_j]$ and works $w_j > 0$. The power is $P(s) = s^\alpha$ with $\alpha > 1$, so $P$ is convex and increasing on $s \ge 0$, with derivative $P'(s) = \alpha s^{\alpha - 1} \ge 0$, which does not decrease in $s$. Let the rounds of YDS have speeds $g_1, g_2, \ldots, g_K$, job sets $A_1, \ldots, A_K$ and real time sets $T_1, \ldots, T_K$ (each a finite union of intervals). Let $U_k = T_1 \cup \cdots \cup T_k$, and let $W_k = \sum_{j \in A_k} w_j$. "Length" means total length, and sets that differ only in finitely many points are treated as equal.

**Termination.** Line L3 always finds an interval, since any job $j$ that is left gives the pair $z = r_j < d_j = z'$ with positive intensity. The chosen interval has positive intensity, so line L4 finds at least one job. So each round removes at least one job, and there are at most $n$ rounds.

**Lemma 1 (compressed time).** Let $c_k(t) = t - |U_k \cap (-\infty, t]|$ be the compressed time after $k$ rounds. Then the window of a job in the instance of round $k + 1$ is $[c_k(r_j), c_k(d_j)]$, and the real times outside $U_k$ whose compressed time lies in an interval $[a, b]$ have total length $b - a$.

*Proof.* The map of line L7 is exactly the change from $c_{k-1}$ to $c_k$ on compressed times, because $T_k$ is the real set whose compressed image is the removed interval. The function $c_k$ is continuous and does not decrease; it is constant on $U_k$ and has slope 1 outside it. So outside $U_k$ it maps length to equal length. $\square$

In particular $|T_k| = z'_k - z_k$, the length of the critical interval of round $k$, and $W_k = g_k |T_k|$.

**Lemma 2 (windows).** Every job of $A_1 \cup \cdots \cup A_k$ has its whole window inside $U_k$.

*Proof.* Let $j \in A_i$ with $i \le k$. In the instance of round $i$, its compressed window lies in $[z_i, z'_i]$. By Lemma 1, the real times of $[r_j, d_j]$ outside $U_{i-1}$ map into $[z_i, z'_i]$, so they lie in $T_i$. So $[r_j, d_j] \subseteq U_{i-1} \cup T_i = U_i \subseteq U_k$. $\square$

**Lemma 3 (speeds go down).** $g_{k+1} \le g_k$ for every $k$.

*Proof.* Take the critical interval $[a, b]$ of round $k + 1$, in the compressed time of that round, with work $W$ and intensity $g_{k+1} = W / (b - a)$. Undo the compression of round $k$. If $[a, b]$ does not contain the point $z_k$ to which the interval $[z_k, z'_k]$ was collapsed, then $[a, b]$ comes from an interval of the same length in round $k$ that contains the same jobs, so $g_{k+1} \le g_k$ by the choice of round $k$. Else it comes from an interval $I$ of length $(b - a) + (z'_k - z_k)$ that contains the jobs of $[a, b]$ and the jobs of $A_k$, with work at least $W + g_k (z'_k - z_k)$. Since $g(I) \le g_k$, we get $W + g_k (z'_k - z_k) \le g_k ((b - a) + (z'_k - z_k))$, so $W \le g_k (b - a)$. $\square$

**Lemma 4 (feasibility).** In each round, EDF at speed $g_k$ during $T_k$ finishes every job of $A_k$ within its window.

*Proof.* Work in the compressed time of round $k$, where the jobs of $A_k$ have windows in $I = [z_k, z'_k]$. By Lemma 1, running in the real set $T_k$ is the same as running in $I$, with the same order of times; EDF makes the same choices in both. For every subinterval $[a, b] \subseteq I$, the jobs of $A_k$ inside it have work at most $g_k (b - a)$, because $g_k$ is the maximum intensity of round $k$. This is the condition under which preemptive EDF on one processor of speed $g_k$ meets all deadlines: if a job missed its deadline $d$, let $a$ be the last time before $d$ at which the processor was idle or ran a job with deadline after $d$ (or $z_k$). Every job run in $[a, d]$ was released at or after $a$ and has deadline at most $d$, and the processor was busy throughout, so these jobs, plus the late one, have more work than $g_k (d - a)$, a contradiction. The total work $W_k = g_k |I|$, so the processor is busy at speed $g_k$ throughout $I$, as line L6 assumes. $\square$

So YDS is feasible, and its energy is $\sum_k |T_k| g_k^\alpha = \sum_k W_k g_k^{\alpha - 1} = \sum_j w_j g_j^{\alpha - 1}$.

**Theorem (optimality).** Every feasible schedule with speed function $s(t)$ has energy at least that of YDS.

*Proof.* Let $\gamma(t) = g_k$ for $t \in T_k$. Convexity gives $P(s) \ge P(\gamma) + P'(\gamma)(s - \gamma)$ for all $s, \gamma \ge 0$. Outside $U_K$, the energy is at least 0. So

$$\int s^\alpha\,dt \ \ge\ \sum_k \int_{T_k} \big( g_k^\alpha + P'(g_k)(s(t) - g_k) \big)\,dt \ =\ E_{\text{YDS}} + \sum_k c_k (a_k - W_k),$$

where $c_k = P'(g_k)$ and $a_k = \int_{T_k} s(t)\,dt$ is the work that the other schedule does during $T_k$. By Lemma 2, the other schedule does all the work of $A_1 \cup \cdots \cup A_k$ inside $U_k$, so $D_k = \sum_{i \le k} (a_i - W_i) \ge 0$ for every $k$. By Lemma 3, $c_1 \ge c_2 \ge \cdots \ge c_K \ge 0$; set $c_{K+1} = 0$. Summation by parts gives

$$\sum_k c_k (a_k - W_k) = \sum_{k=1}^{K} (c_k - c_{k+1}) D_k \ \ge\ 0,$$

since every factor is at least 0. So the energy is at least $E_{\text{YDS}}$. $\square$

The same proof works for every convex, increasing power function, which is why the YDS schedule does not depend on $\alpha$. With a strictly convex power, a schedule that runs a fixed amount of work in a fixed time at a speed that is not constant uses more energy than the constant speed, by Jensen's inequality; this is the case $K = 1$ with one job. $\blacksquare$
