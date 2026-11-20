---
title: The Dubins-Spanier procedure is proportional and uses n(n+1)/2 - 1 cut queries
proves: [correctness]
status: full
---

**Setting.** The cake is $[0, 1]$, and agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. For $a \in [0, 1]$, the map $t \mapsto V_i([a, t])$ is continuous and nondecreasing on $[a, 1]$, since $V_i$ is nonatomic. So $\mathrm{Cut}_i(a, t)$ has an answer whenever $0 \le t \le V_i([a, 1])$, and the least answer $x$ has $V_i([a, x]) = t$. Single points have value 0. We refer to the lines L1 to L6 of the page.

**Lemma 1 (the stop point of the knife).** Let the knife start at $a$, and let each agent $i \in R$ call stop at the first point $y$ with $V_i([a, y]) \ge 1/n$. Then the knife stops at $\min_{i \in R} m_i$, where $m_i = \mathrm{Cut}_i(a, 1/n)$ is the least answer.

*Proof.* By continuity, the first point $y$ with $V_i([a, y]) \ge 1/n$ is the least $y$ with $V_i([a, y]) = 1/n$, which is $m_i$. The knife stops at the first call, so at $\min_i m_i$. $\square$

So lines L3 to L5 simulate the knife exactly, with the tie rule of line L4.

**Lemma 2 (invariant).** At the test of line L2, every agent $i \in R$ has $V_i([a, 1]) \ge |R|/n$.

*Proof.* By induction on the rounds. The first time, $a = 0$, $|R| = n$ and $V_i([0, 1]) = 1$. Suppose the invariant holds at the start of a round. Each cut query of line L3 asks for $1/n \le |R|/n \le V_i([a, 1])$, so it has an answer. Let $h$ be the agent of line L4. For each $j \in R \setminus \{h\}$, we have $m_h \le m_j$, so monotonicity gives $V_j([a, m_h]) \le V_j([a, m_j]) = 1/n$. Additivity then gives
$$V_j([m_h, 1]) = V_j([a, 1]) - V_j([a, m_h]) \ge \frac{|R|}{n} - \frac{1}{n} = \frac{|R| - 1}{n}.$$
Line L5 sets $a \leftarrow m_h$ and removes $h$, so the invariant holds for the new $R$. $\square$

**Theorem 1 (proportional).** The output is a partition of $[0, 1]$ into $n$ intervals, and $V_i(X_i) \ge 1/n$ for every agent $i$.

*Proof.* Each round removes one agent, so the loop runs $n - 1$ times. The successive left ends $a_0 = 0 \le a_1 \le \dots \le a_{n-1}$ satisfy $a_{k+1} = m_h \ge a_k$, because a cut from $a_k$ returns a point at least $a_k$. The pieces $[a_k, a_{k+1}]$ of line L5 and the piece $[a_{n-1}, 1]$ of line L6 cover $[0, 1]$ and meet only at end points. Each agent of line L5 gets $V_h([a, m_h]) = 1/n$. The last agent gets $V_i([a, 1]) \ge 1/n$ by Lemma 2 with $|R| = 1$. $\square$

**Theorem 2 (safe for an honest agent).** If agent $i$ answers by $V_i$, then $V_i(X_i) \ge 1/n$, whatever points the other agents give as marks.

*Proof.* The proof of Lemma 2 for the single agent $i$ uses only its own mark $m_i$ and the choice of the least mark in line L4: if agent $i$ is not chosen, some mark $m_h \le m_i$ was chosen, so $V_i([a, m_h]) \le 1/n$. This needs nothing about the marks of the other agents except that they lie in $[a, 1]$. So $V_i([a, 1]) \ge |R|/n$ while agent $i$ waits. If agent $i$ is chosen in line L5, its piece is worth exactly $1/n$ to it. If it is the last agent, its piece is worth at least $1/n$. $\square$

**Theorem 3 (query count).** The protocol makes exactly $n(n+1)/2 - 1$ cut queries and no eval queries.

*Proof.* The round with $|R| = r$ makes $r$ cut queries in line L3 and no other query. The rounds have $r = n, n - 1, \dots, 2$, and line L6 makes no query. So the count is $\sum_{r=2}^{n} r = n(n+1)/2 - 1$. $\blacksquare$
