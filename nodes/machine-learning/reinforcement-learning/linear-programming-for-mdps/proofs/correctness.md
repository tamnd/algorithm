---
title: The MDP linear programs are correct, bases are policies, and the simplex method returns an optimal policy
proves: [correctness, termination]
status: full
---

We use the notation of the page: a finite MDP with $0 \le \gamma < 1$, weights $\alpha(s) > 0$, the programs (P) and (D), and the matrix $M$ whose column $(s, a)$ is $e_s - \gamma P(\cdot \mid s, a)$. For a deterministic policy $\pi$, $P_\pi(s, s') = P(s' \mid s, \pi(s))$, $r_\pi(s) = R(s, \pi(s))$ and $V^\pi = (I - \gamma P_\pi)^{-1}r_\pi$. The Bellman operators $T^\pi$ and $T$ are monotone, and $V^*$ is the unique fixed point of $T$ ([Bellman contraction](/bellman-contraction/)).

**Lemma 1 (primal).** $V^*$ is the unique optimal solution of (P).

*Proof.* The constraints of (P) say $V(s) \ge R(s, a) + \gamma\sum_{s'}P(s' \mid s, a)V(s')$ for every $a$, that is, $V \ge TV$. If $V$ is feasible, monotonicity gives $V \ge TV \ge T^2V \ge \cdots$, and $T^kV \to V^*$, so $V \ge V^*$. The vector $V^*$ is feasible because $V^* = TV^*$. So for every feasible $V$, $\sum_s \alpha(s)V(s) \ge \sum_s \alpha(s)V^*(s)$, with equality only if $V = V^*$, because $\alpha > 0$ and $V - V^* \ge 0$. $\square$

**Lemma 2 (weak duality).** If $V$ is feasible for (P) and $x$ is feasible for (D), then $\sum_{s,a}R(s, a)x(s, a) \le \sum_s \alpha(s)V(s)$.

*Proof.* Since $x \ge 0$ and $R(s, a) \le V(s) - \gamma\sum_{s'}P(s' \mid s, a)V(s')$,
$\sum_{s,a}R(s, a)x(s, a) \le \sum_{s,a}x(s, a)\big(V(s) - \gamma\sum_{s'}P(s' \mid s, a)V(s')\big) = \sum_{s'}V(s')\big(\sum_a x(s', a) - \gamma\sum_{s,a}P(s' \mid s, a)x(s, a)\big) = \sum_{s'}\alpha(s')V(s')$. $\square$

**Lemma 3 (the basis of a policy).** For a deterministic policy $\pi$, let $B_\pi$ be the matrix of the columns $(s, \pi(s))$, in the order of the states. Then $B_\pi = (I - \gamma P_\pi)^\top$, it is invertible, the basic solution $x_B = B_\pi^{-1}\alpha$ satisfies $x_B \ge \alpha > 0$, and the solution of $B_\pi^\top y = c_B$ is $y = V^\pi$.

*Proof.* Column $s$ of $B_\pi$ is $e_s - \gamma$ (row $s$ of $P_\pi$)$^\top$, so $B_\pi = (I - \gamma P_\pi)^\top$. The matrix $\gamma P_\pi^\top$ has nonnegative entries and column sums $\gamma < 1$, so the series $\sum_k \gamma^k (P_\pi^\top)^k$ converges to $(I - \gamma P_\pi^\top)^{-1}$, whose entries are nonnegative and whose diagonal entries are at least 1. So $x_B = \sum_k \gamma^k(P_\pi^\top)^k\alpha \ge \alpha$. Finally $B_\pi^\top y = c_B$ is $(I - \gamma P_\pi)y = r_\pi$, whose solution is $V^\pi$. $\square$

**Lemma 4 (every basic feasible solution is a policy).** Let $x$ be a basic feasible solution of (D) with basis $\mathcal{B}$. Then $\mathcal{B}$ contains exactly one column $(s, \pi(s))$ for each state $s$, and $x(s, \pi(s)) > 0$ for each $s$. So $\mathcal{B}$ is the basis of the policy $\pi$, and $x$ is nondegenerate.

*Proof.* Fix a state $s$. The constraint of $s$ gives $\sum_a x(s, a) = \alpha(s) + \gamma\sum_{s'',a}P(s \mid s'', a)x(s'', a) \ge \alpha(s) > 0$, so some $x(s, a)$ is positive. So $x$ has at least $|S|$ positive entries, one in each state. A basic solution has at most $|S|$ positive entries, all of them basic. So $x$ has exactly one positive entry in each state, these $|S|$ entries are the whole basis, and all basic entries are positive. $\square$

**Lemma 5 (reduced costs are advantages).** For the basis of $\pi$, with $y = V^\pi$, the reduced cost of the column $(s, a)$ is $\delta(s, a) = c(s, a) - y^\top M(s, a) = Q^\pi(s, a) - V^\pi(s)$.

*Proof.* $y^\top M(s, a) = V^\pi(s) - \gamma\sum_{s'}P(s' \mid s, a)V^\pi(s')$, so $\delta(s, a) = R(s, a) + \gamma\sum_{s'}P(s' \mid s, a)V^\pi(s') - V^\pi(s) = Q^\pi(s, a) - V^\pi(s)$. $\square$

**Lemma 6 (one pivot).** Suppose the basis is that of $\pi$ and line L7 picks $e = (s_e, a_e)$ with $\delta(e) > 0$. Then line L8 finds a row, the leaving column is $(s_e, \pi(s_e))$, the new basis is that of the policy $\pi'$ that agrees with $\pi$ except $\pi'(s_e) = a_e$, and the objective of (D) rises by a positive amount.

*Proof.* The basic solution of $\pi'$ is feasible by Lemma 3. The simplex step moves from $x_B$ along the edge where $x(e)$ grows from 0 and the basic entries change by $-x(e)u$. If no $u_r$ were positive, the objective would grow without bound along this edge, which contradicts Lemma 2 with the feasible $V^*$ of Lemma 1. So line L8 finds a row $r$, and the new solution is a basic feasible solution with basis $\mathcal{B}' = \mathcal{B} - \{\text{row } r\} + \{e\}$. By Lemma 4, $\mathcal{B}'$ has exactly one column in each state. It contains $e$, a column of $s_e$, so the column that left is the only other column of $s_e$ in $\mathcal{B}$, which is $(s_e, \pi(s_e))$. The new value of $x(e)$ is $\theta = (x_B)_r/u_r$, and $(x_B)_r > 0$ by Lemma 4, so $\theta > 0$. The objective changes by $\theta\,\delta(e) > 0$. $\square$

**Theorem.** LP-MDP-SIMPLEX stops after at most $|A|^{|S|} - 1$ pivots and returns $V = V^*$, an optimal solution $x$ of (D), and an optimal deterministic policy $\pi$.

*Proof.* The start is the basis of $\pi_0$, which is feasible by Lemma 3. By Lemma 6 every pivot leads to the basis of another deterministic policy and strictly raises the objective, so no basis repeats. There are at most $|A|^{|S|}$ deterministic policies, so the loop stops. It stops at line L6 with the basis of a policy $\pi$ and all reduced costs $\delta(s, a) \le 0$. By Lemma 5 this says $V^\pi(s) \ge Q^\pi(s, a)$ for each $(s, a)$, so $y = V^\pi$ is feasible for (P). The basic columns have reduced cost 0, so $c^\top x = \sum_{(s,a) \in \mathcal{B}}c(s, a)x(s, a) = \sum_{(s, a) \in \mathcal{B}}(y^\top M(s, a))x(s, a) = y^\top Mx = \sum_s\alpha(s)y(s)$. By Lemma 2 both $x$ and $y$ are optimal, and by Lemma 1, $y = V^*$. So $V^\pi = V^*$ and $\pi$ is optimal. The policy returned by line L6 is the action of the basic column of each state, which is the action with $x(s, a) > 0$. $\blacksquare$

**Any optimal dual solution gives an optimal policy.** Let $x$ be optimal for (D), not necessarily basic. Let $d(s) = \sum_a x(s, a)$, which is at least $\alpha(s) > 0$, and $\pi(a \mid s) = x(s, a)/d(s)$. The constraints of (D) read $d = \alpha + \gamma P_\pi^\top d$, so $d = (I - \gamma P_\pi^\top)^{-1}\alpha$. Then $c^\top x = \sum_s d(s)r_\pi(s) = \alpha^\top(I - \gamma P_\pi)^{-1}r_\pi = \alpha^\top V^\pi$. Optimality and Lemma 1 give $\alpha^\top V^\pi = \alpha^\top V^*$. Since $V^\pi \le V^*$ and $\alpha > 0$, $V^\pi = V^*$, so $\pi$ is optimal.
