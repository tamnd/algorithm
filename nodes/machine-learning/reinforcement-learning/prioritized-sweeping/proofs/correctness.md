---
title: Prioritized sweeping terminates with every Bellman error at most theta
proves: [correctness, termination]
status: full
---

We use the notation of the page: a finite MDP, $0 \le \gamma < 1$, $\theta > 0$, $(TV)(s) = \max_a Q_V(s, a)$ with $Q_V(s, a) = R(s, a) + \gamma\sum_{s'}P(s' \mid s, a)V(s')$, the Bellman error $\mathrm{err}_V(s) = |(TV)(s) - V(s)|$, and $\lVert U \rVert = \max_s |U(s)|$. The successors of $s$ are the states $s'$ with $P(s' \mid s, a) > 0$ for some $a$; so $p \in \mathrm{pred}(s)$ exactly when $s$ is a successor of $p$.

**Fact.** $(TV)(s)$ depends only on the values of the successors of $s$. So if $V$ and $V'$ differ only at the state $s$, then $\mathrm{err}_{V'}(p) = \mathrm{err}_V(p)$ for every state $p$ with $p \ne s$ and $p \notin \mathrm{pred}(s)$.

**Lemma 1 (invariant).** Before each test of line L3, the set of states in the queue is $\{s : \mathrm{err}_V(s) > \theta\}$, and the priority of each such state is $\mathrm{err}_V(s)$.

*Proof.* Lines L1 and L2 establish it. Assume it holds before an iteration that backs up $s$. Line L4 removes $s$, and line L5 sets $V(s) = (TV)(s)$, computed with the old values. If $s \notin \mathrm{pred}(s)$, then $(TV)(s)$ does not depend on $V(s)$, so after line L5 the error of $s$ is 0, and $s$ is correctly absent. Lines L6 to L8 recompute the error of every $p \in \mathrm{pred}(s)$, including $s$ itself if it has a self-loop, and put $p$ in the queue with that priority exactly when it exceeds $\theta$. By the fact, no other error changed. So the invariant holds again. With lazy deletion, the heap has, for each state in the queue, an entry with its current priority, and line L4 skips any entry whose priority is not the current one, so the first entry it accepts is a state of largest error. $\square$

**Lemma 2 (termination).** The loop of lines L3 to L8 stops.

*Proof.* Suppose it does not. Let $S_\infty$ be the set of states that are backed up infinitely often. It is not empty, and after some step $t_0$ only states of $S_\infty$ are backed up, so the values of the states outside $S_\infty$ stay fixed after $t_0$. Fix these values, and let $F$ be the map on vectors indexed by $S_\infty$ given by $F(W)(s) = (T\tilde W)(s)$, where $\tilde W$ agrees with $W$ on $S_\infty$ and with the fixed values elsewhere. $F$ is a $\gamma$-contraction in the max norm, by the same argument as for $T$, so it has a unique fixed point $W^\circ$.

Let $D_t = \max_{s \in S_\infty}|V_t(s) - W^\circ(s)|$ after step $t \ge t_0$. A backup at $s \in S_\infty$ sets $V(s) = F(V)(s)$, and $|F(V)(s) - W^\circ(s)| = |F(V)(s) - F(W^\circ)(s)| \le \gamma D_t$. So $D_t$ never increases. Take any $t \ge t_0$, and let $t' > t$ be a step by which every state of $S_\infty$ has been backed up at least once after $t$. Each such state was last set to a value within $\gamma D_t$ of $W^\circ$, and it was not changed after that, so $D_{t'} \le \gamma D_t$. Repeating this, $D_t \to 0$.

For $s \in S_\infty$, $\mathrm{err}_V(s) = |F(V)(s) - V(s)| \le |F(V)(s) - W^\circ(s)| + |W^\circ(s) - V(s)| \le (1 + \gamma)D_t$, which tends to 0. So after some step every state of $S_\infty$ has error at most $\theta$, and by Lemma 1 none of them is in the queue. Then no state of $S_\infty$ is backed up again, which contradicts the definition of $S_\infty$. $\square$

**Theorem.** PRIORITIZED-SWEEPING stops and returns $V$ with $\lVert TV - V \rVert \le \theta$ and $\lVert V - V^* \rVert \le \theta/(1-\gamma)$.

*Proof.* By Lemma 2 the loop stops, with an empty queue. By Lemma 1, $\mathrm{err}_V(s) \le \theta$ for every state, that is $\lVert TV - V \rVert \le \theta$. Since $V^* = TV^*$ and $T$ is a $\gamma$-contraction ([Bellman contraction](/bellman-contraction/)), $\lVert V - V^* \rVert \le \lVert V - TV \rVert + \lVert TV - TV^* \rVert \le \theta + \gamma\lVert V - V^* \rVert$, and so $\lVert V - V^* \rVert \le \theta/(1 - \gamma)$. $\blacksquare$

**The chain.** On the chain of the page, with $V = 0$ at the start, line L2 queues only state $n - 2$. Backing up state $s$ sets $V(s) = 0.9^{\,n-2-s}$, which is final, and makes the error of $s - 1$ equal to $0.9^{\,n-1-s} > \theta$ for small $\theta$, while the error of $s + 1$ stays 0. By induction the method backs up $n - 2, n - 3, \ldots, 0$ once each, which is $n - 1$ backups.
