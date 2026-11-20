---
title: Divide and choose is proportional and envy-free
proves: [correctness]
status: full
---

**Setting.** The cake is $[0, 1]$. Agents 1 and 2 have valuations $V_1$ and $V_2$, each a nonnegative, additive and nonatomic measure with $V_i([0, 1]) = 1$. Agent 1 cuts and agent 2 chooses, as in lines L1 to L4.

**Lemma 1 (the cut exists).** There is a point $x \in [0, 1]$ with $V_1([0, x]) = 1/2$.

*Proof.* Let $f(t) = V_1([0, t])$. Then $f(0) = V_1(\{0\}) = 0$ because $V_1$ is nonatomic, and $f(1) = 1$. For $s < t$, additivity gives $f(t) - f(s) = V_1((s, t])$, and this tends to 0 as $t - s \to 0$, because a nonatomic measure of a shrinking interval goes to the measure of a point, which is 0. So $f$ is continuous and nondecreasing, and the intermediate value theorem gives $x$ with $f(x) = 1/2$. The least such $x$ exists because the set $f^{-1}(1/2)$ is closed and nonempty. $\square$

So line L1 always has an answer. Fix this $x$. Because $V_i$ is nonatomic, $V_i(\{x\}) = 0$, so for each agent $V_i([0, x]) + V_i([x, 1]) = 1$.

**Lemma 2 (two goals are one for two agents).** Let $X_1, X_2$ be a partition of $[0, 1]$, up to a finite set of points. Then $V_i(X_i) \ge V_i(X_j)$ holds if and only if $V_i(X_i) \ge 1/2$.

*Proof.* Additivity and the nonatomic property give $V_i(X_i) + V_i(X_j) = 1$. So $V_i(X_i) \ge V_i(X_j) = 1 - V_i(X_i)$ holds exactly when $2 V_i(X_i) \ge 1$. $\square$

**Theorem.** The output of lines L1 to L4 has $V_1(X_1) = 1/2$ and $V_2(X_2) \ge 1/2$. Hence it is proportional and envy-free.

*Proof.* Agent 1. In line L3, $X_1 = [x, 1]$ and $V_1(X_1) = 1 - V_1([0, x]) = 1/2$. In line L4, $X_1 = [0, x]$ and $V_1(X_1) = 1/2$ by line L1. So $V_1(X_1) = 1/2$ in both branches.

Agent 2. Let $e = V_2([0, x])$, the answer of line L2. If $e \ge 1/2$, line L3 gives $X_2 = [0, x]$ and $V_2(X_2) = e \ge 1/2$. If $e < 1/2$, line L4 gives $X_2 = [x, 1]$ and $V_2(X_2) = 1 - e > 1/2$.

Both agents get at least $1/2$, which is proportionality for $n = 2$. Lemma 2 turns this into envy-freeness. $\square$

**Each guarantee needs only the agent's own behavior.** The argument for agent 1 uses only line L1, the cut by agent 1. It holds for any rule the chooser uses, because both pieces are worth $1/2$ to agent 1. The argument for agent 2 uses only line L2, the choice by agent 2. It holds for any point $x$, because $\max(e, 1 - e) \ge 1/2$ for every $e$. So an agent that follows the protocol gets at least $1/2$ even if the other agent does not follow it.

**Query count.** Line L1 makes one cut query and line L2 makes one eval query. No other line makes a query. So the protocol makes exactly two queries in the Robertson-Webb model. $\blacksquare$
