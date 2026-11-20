---
title: The Selfridge-Conway procedure is envy-free and uses at most five cuts
proves: [correctness]
status: full
---

**Setting.** The cake is $[0, 1]$. Agents 1, 2 and 3 have nonnegative, additive and nonatomic valuations $V_1, V_2, V_3$ with $V_i([0, 1]) = 1$. Single points have value 0, so two intervals that meet at one end point do not overlap in value. For $a \in [0, 1]$ and $0 \le t \le V_i([a, 1])$, the query $\mathrm{Cut}_i(a, t)$ returns the least $x \ge a$ with $V_i([a, x]) = t$; such an $x$ exists because $x \mapsto V_i([a, x])$ is continuous and nondecreasing. We refer to the lines L1 to L12 of the page. Let $A, B, C$ be the three pieces of line L1, let $P$ and $Q$ be the best and second best piece of agent 2 at line L2, and let $R$ be the third piece.

**Lemma 1 (the cuts exist).** Every cut query of the procedure has an answer.

*Proof.* Line L1 asks $\mathrm{Cut}_1(0, 1/3)$ and then $\mathrm{Cut}_1(c, 1/3)$, where $V_1([c, 1]) = 2/3 \ge 1/3$. Line L4 asks $\mathrm{Cut}_2(a, V_2(Q))$ with $P = [a, b]$, and $V_2(Q) < V_2(P) = V_2([a, b])$. Line L11 asks $\mathrm{Cut}_U(a', w)$ and then $\mathrm{Cut}_U(y, w)$ with $L = [a', b']$ and $w = V_U(L)/3$; here $V_U([a', b']) = 3w$ and $V_U([y, b']) = 2w$. $\square$

**Lemma 2 (stage one).** After line L8, the three pieces $P', Q, R$ (with $P' = P$ when there is no trim) form, together with the trimmings $L$, a partition of $[0, 1]$. The values satisfy:
1. $V_1(Q) = V_1(R) = 1/3 \ge V_1(P')$, and $V_1(P') + V_1(L) = 1/3$;
2. $V_2(P') = V_2(Q) \ge V_2(R)$;
3. agent 3 holds a piece that it values at least as much as each of the other two pieces of stage one;
4. agent 1 holds $Q$ or $R$, never the trimmed piece $P'$ when a trim happened.

*Proof.* Line L1 makes three pieces of value $1/3$ each to agent 1. Line L4 replaces $P = [a, b]$ by $P' = [a, x]$ and $L = [x, b]$, so $V_1(P') + V_1(L) = V_1(P) = 1/3$, and $Q$ and $R$ keep the value $1/3$. This gives item 1. Item 2: with a trim, $V_2(P') = V_2(Q)$ by line L4, and $V_2(Q) \ge V_2(R)$ by the choice of $Q$; without a trim, $V_2(P) = V_2(Q) \ge V_2(R)$ by line L3. Item 3 holds because agent 3 chooses first, in line L6, from all three pieces. For item 4: if agent 3 did not take $P'$, line L7 gives $P'$ to agent 2. If agent 3 took $P'$, then $P'$ is gone. In both cases $P'$ is not left for agent 1 in line L8. $\square$

**Lemma 3 (agent 2 in stage one).** Agent 2 holds a piece that it values at least as much as each of the other two pieces of stage one.

*Proof.* If agent 2 takes $P'$ in line L7, its value is $V_2(P') = V_2(Q) \ge V_2(R)$ by Lemma 2, so it is a best piece. If agent 3 took $P'$, agent 2 takes the better of $Q$ and $R$ by its own values, and that value is $V_2(Q) = V_2(P')$. $\square$

**Theorem 1 (envy-free).** The final division is envy-free: $V_i(X_i) \ge V_i(X_j)$ for all $i, j \in \{1, 2, 3\}$.

*Proof.* Without a trim, line L9 returns after stage one. Each $X_i$ is one of $A, B, C$. Agents 2 and 3 do not envy by Lemma 2 item 3 and Lemma 3, and agent 1 values all three pieces at $1/3$.

With a trim, let $T$ be the agent of $\{2, 3\}$ that holds $P'$ and $U$ the other one (line L10). Line L11 cuts $L$ into $L_1, L_2, L_3$ with $V_U(L_k) = V_U(L)/3$. In line L12, $T$ takes a part first, agent 1 takes a part second, and $U$ takes the last part. Write $S_i$ for the stage one piece and $Z_i$ for the part of $L$ of agent $i$, so $X_i = S_i \cup Z_i$ and $V_i(X_i) = V_i(S_i) + V_i(Z_i)$ by additivity.
- Agent $T$: $V_T(S_T) \ge V_T(S_j)$ for each $j$ by Lemma 2 item 3 or Lemma 3, and $V_T(Z_T) \ge V_T(Z_j)$ because $T$ chooses first among all three parts.
- Agent $U$: $V_U(S_U) \ge V_U(S_j)$ by the same lemmas, and $V_U(Z_j) = V_U(L)/3$ for every $j$ because $U$ made the parts.
- Agent 1: against $U$, $V_1(S_1) = 1/3 \ge V_1(S_U)$ by Lemma 2 items 1 and 4, and $V_1(Z_1) \ge V_1(Z_U)$ because agent 1 chooses before $U$. Against $T$, $V_1(X_T) = V_1(P') + V_1(Z_T) \le V_1(P') + V_1(L) = 1/3 = V_1(S_1) \le V_1(X_1)$, by Lemma 2 item 1 and monotonicity.

Adding the two inequalities for $T$ and for $U$ gives $V_i(X_i) \ge V_i(X_j)$ in each case. $\square$

**Theorem 2 (partition and pieces).** The pieces $X_1, X_2, X_3$ are disjoint up to end points and cover $[0, 1]$. Each $X_i$ is a union of at most two intervals.

*Proof.* Stage one splits $[0, 1]$ into $P', Q, R$ and $L$ (Lemma 2), and line L11 splits $L$ into three intervals. Each agent gets one interval in stage one and at most one interval in stage two. $\square$

**Theorem 3 (cost).** The procedure makes at most 5 cut queries and at most 12 eval queries.

*Proof.* Cuts: two in line L1, at most one in line L4 and at most two in line L11. Evals: three by agent 2 in line L2 and three by agent 3 in line L6; agent 2 needs no new query in line L7, because it knows its values from line L2 and $V_2(P') = V_2(Q)$. In stage two, $U$ makes one eval in line L11, $T$ makes three and agent 1 makes two in line L12. The total is at most $3 + 3 + 1 + 3 + 2 = 12$. $\square$
