---
title: Iterative policy evaluation converges in both forms, with an error bound at the stop
proves: [correctness, termination]
status: full
---

We use the notation of the page, with $0 \le \gamma < 1$, $\theta > 0$ and $\lVert U \rVert = \max_s |U(s)|$. Number the states $1, \ldots, n$ in the order of the sweep. For a state $s$ and a vector $U$ let

$$b_s(U) = \sum_a \pi(a \mid s)\Big[R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, U(s')\Big],$$

so $(T^\pi U)(s) = b_s(U)$, and $V^\pi$ is the unique vector with $b_s(V^\pi) = V^\pi(s)$ for each $s$ ([Bellman expectation equation](/bellman-expectation-equation/)).

**Lemma 1.** For all vectors $U$ and $W$ and each state $s$, $|b_s(U) - b_s(W)| \le \gamma \lVert U - W \rVert$.

*Proof.* $b_s(U) - b_s(W) = \gamma \sum_a \pi(a \mid s) \sum_{s'} P(s' \mid s, a)(U(s') - W(s'))$. The weights $\pi(a \mid s)P(s' \mid s, a)$ are nonnegative and sum to 1, so the absolute value is at most $\gamma \lVert U - W \rVert$. $\square$

**The two sweeps.** A two-array sweep maps $V$ to $T^\pi V$. An in-place sweep maps $V$ to the vector $G V$ defined in the order of the sweep: $(GV)(s) = b_s(U_s)$, where $U_s$ agrees with $GV$ on the states before $s$ and with $V$ on $s$ and the states after $s$. This is what lines L4 to L7 compute when line L7 writes into the array that line L5 reads.

**Lemma 2.** $T^\pi$ and $G$ are $\gamma$-contractions in the max norm, and $V^\pi$ is a fixed point of both.

*Proof.* For $T^\pi$ this is Lemma 1. For $G$, take vectors $V$ and $W$ and let $d = \lVert V - W \rVert$. We show by induction on $s$ that $|(GV)(s) - (GW)(s)| \le \gamma d$. The vectors $U_s$ for $V$ and for $W$ agree in their entries with the entries of $GV$ and $GW$ before $s$, which differ by at most $\gamma d \le d$ by induction, and with the entries of $V$ and $W$ from $s$ on, which differ by at most $d$. So the two vectors $U_s$ differ by at most $d$ in the max norm, and Lemma 1 gives the bound for state $s$. For the fixed point: if $V = V^\pi$, then at each state $U_s = V^\pi$ by induction, so $(GV^\pi)(s) = b_s(V^\pi) = V^\pi(s)$. $\square$

Let $F$ be $T^\pi$ for the two-array form and $G$ for the in-place form, let $V_0$ be the start and $V_k = F V_{k-1}$. Line L6 makes $\delta$ equal to $\delta_k = \lVert V_k - V_{k-1} \rVert$ at the end of sweep $k$.

**Lemma 3 (convergence).** $\lVert V_k - V^\pi \rVert \le \gamma^k \lVert V_0 - V^\pi \rVert$.

*Proof.* $\lVert V_k - V^\pi \rVert = \lVert FV_{k-1} - FV^\pi \rVert \le \gamma \lVert V_{k-1} - V^\pi \rVert$ by Lemma 2, and induction on $k$. $\square$

**Lemma 4 (termination).** The loop stops after at most $1 + \lceil \ln(\delta_1/\theta)/\ln(1/\gamma) \rceil$ sweeps if $\gamma > 0$, and after at most 2 sweeps if $\gamma = 0$.

*Proof.* $\delta_{k+1} = \lVert FV_k - FV_{k-1} \rVert \le \gamma\delta_k$, so $\delta_k \le \gamma^{k-1}\delta_1$. If $\delta_1 < \theta$ the loop stops after sweep 1. Otherwise $\gamma^{k-1}\delta_1 < \theta$ as soon as $k - 1 > \ln(\delta_1/\theta)/\ln(1/\gamma)$. If $\gamma = 0$, then $\delta_2 = 0 < \theta$. $\square$

**Theorem.** If $0 \le \gamma < 1$, the loop stops, and for both forms the returned vector satisfies $\lVert V - V^\pi \rVert \le \frac{\gamma}{1-\gamma}\theta$.

*Proof.* By Lemma 4 the loop stops at a sweep $k$ with $\delta_k < \theta$ and returns $V_k$. By Lemma 2, $\lVert V_k - V^\pi \rVert = \lVert FV_{k-1} - FV^\pi \rVert \le \gamma\lVert V_{k-1} - V^\pi \rVert \le \gamma(\delta_k + \lVert V_k - V^\pi \rVert)$. Move the last term to the left and divide by $1 - \gamma > 0$: $\lVert V_k - V^\pi \rVert \le \frac{\gamma}{1-\gamma}\delta_k < \frac{\gamma}{1-\gamma}\theta$. $\blacksquare$

**Remark on $\gamma = 1$.** For an episodic task with terminal states of value 0 that the policy reaches with probability 1, both forms still converge to $V^\pi$, because $T^\pi$ is then a contraction in a weighted max norm (stochastic shortest path theory, Bertsekas and Tsitsiklis). The bound of the theorem does not apply, as the gridworld on the page shows.
