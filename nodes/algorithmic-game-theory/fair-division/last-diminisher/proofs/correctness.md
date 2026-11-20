---
title: The last diminisher is proportional and uses at most n^2 - 1 queries
proves: [correctness]
status: full
---

**Setting.** The cake is $[0, 1]$, and agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. For $a \in [0, 1]$, the map $t \mapsto V_i([a, t])$ is continuous and nondecreasing on $[a, 1]$, since $V_i$ is nonatomic. So $\mathrm{Cut}_i(a, t)$ has an answer whenever $0 \le t \le V_i([a, 1])$, and any answer $x$ has $V_i([a, x]) = t$. Single points have value 0, so the end points shared by two pieces do not matter. We refer to the lines L1 to L8 of the page.

**Lemma 1 (the piece shrinks).** In one round, let $x_0$ be the mark of line L3 and $x_1, x_2, \dots$ the marks of the later executions of line L6, in order. Then $x_0 \ge x_1 \ge x_2 \ge \dots$, and the holder $h$ at the end of the round has $V_h([a, x]) = 1/n$ for the final mark $x$.

*Proof.* Line L6 runs for agent $j$ only when line L5 found $V_j([a, x]) > 1/n$ for the current mark $x$. The new mark $x'$ has $V_j([a, x']) = 1/n < V_j([a, x])$. Since $t \mapsto V_j([a, t])$ is nondecreasing, $x' < x$. The holder is always the agent whose cut gave the current mark, so $V_h([a, x]) = 1/n$ at the end. $\square$

**Lemma 2 (the others think the piece is not too large).** Let $x$ be the final mark of a round and $h$ the final holder. Every agent $j \ne h$ of $R$ has $V_j([a, x]) \le 1/n$.

*Proof.* Let $j \ne h$. If $j$ is the first agent of $R$, it made the mark $x_0$ with $V_j([a, x_0]) = 1/n$, and since $h \ne j$ some later trim happened, so $x \le x_0$ by Lemma 1. If $j$ comes later, it saw some mark $y$ in line L5. Either $V_j([a, y]) \le 1/n$ and it passed, or it trimmed to a mark $y'$ with $V_j([a, y']) = 1/n$ and was holder for a while. All later marks are at most $y$ (in the first case) or at most $y'$ (in the second case), by Lemma 1. So in all cases $[a, x]$ lies inside an interval $[a, z]$ with $V_j([a, z]) \le 1/n$, and $V_j([a, x]) \le V_j([a, z]) \le 1/n$. $\square$

**Lemma 3 (invariant).** At the test of line L2, every agent $i \in R$ has $V_i([a, 1]) \ge |R|/n$.

*Proof.* By induction on the rounds. The first time, $a = 0$ and $|R| = n$, and $V_i([0, 1]) = 1$. Suppose the invariant holds at the start of a round. All cut queries of the round have answers: each one asks for $1/n \le |R|/n \le V_i([a, 1])$. Let $x$ be the final mark and $h$ the holder. For every $j \in R \setminus \{h\}$, additivity and Lemma 2 give
$$V_j([x, 1]) = V_j([a, 1]) - V_j([a, x]) \ge \frac{|R|}{n} - \frac{1}{n} = \frac{|R| - 1}{n}.$$
Line L7 sets $a \leftarrow x$ and removes $h$, so the invariant holds for the new $R$ of size $|R| - 1$. $\square$

**Theorem 1 (proportional).** The output is a partition of $[0, 1]$ into $n$ intervals, and $V_i(X_i) \ge 1/n$ for every agent $i$.

*Proof.* Each round removes one agent from $R$, so the loop of line L2 runs $n - 1$ times. The pieces of line L7 are $[a_0, a_1], [a_1, a_2], \dots, [a_{n-2}, a_{n-1}]$ with $a_0 = 0$, and line L8 gives $[a_{n-1}, 1]$. Lemma 1 and the answer of a cut query from $a$ give $a_k \le a_{k+1}$. So the pieces are intervals that cover $[0, 1]$ and meet only at end points. Each agent in line L7 gets $V_h([a, x]) = 1/n$ by Lemma 1. The last agent gets $V_i([a, 1]) \ge 1/n$ by Lemma 3 with $|R| = 1$. $\square$

**Theorem 2 (safe for an honest agent).** Suppose agent $i$ answers by $V_i$, and every other agent $j$ answers by some nonnegative, additive and nonatomic valuation $W_j$ with $W_j([0, 1]) = 1$ of its own choice, not necessarily its true one. Then $V_i(X_i) \ge 1/n$.

*Proof.* Lemma 1 uses only that each agent answers both its queries by one valuation, so it holds for the valuations $W_j$ and $V_i$. In Lemma 2 and Lemma 3, take $j = i$ and $i$ alone: their proofs use Lemma 1 and the answers of agent $i$ only. They show that, as long as agent $i$ is in $R$, $V_i([a, 1]) \ge |R|/n$. If agent $i$ gets a piece in line L7, the piece is its own cut, worth $1/n$. If it is the last agent, it gets $[a, 1]$, worth at least $1/n$. $\square$

**Theorem 3 (query count).** The protocol makes exactly $n(n-1)/2$ eval queries, between $n - 1$ and $n(n+1)/2 - 1$ cut queries, and at most $n^2 - 1$ queries in total.

*Proof.* The round with $|R| = r$ makes one eval query for each of the $r - 1$ agents after the first (line L5), one cut query in line L3, and at most $r - 1$ cut queries in line L6. The rounds have $r = n, n - 1, \dots, 2$. So the evals number $\sum_{r=2}^{n} (r - 1) = n(n-1)/2$, and the cuts number at least $n - 1$ and at most $\sum_{r=2}^{n} r = n(n+1)/2 - 1$. The total is at most $n(n-1)/2 + n(n+1)/2 - 1 = n^2 - 1$. Line L8 makes no query. $\blacksquare$
