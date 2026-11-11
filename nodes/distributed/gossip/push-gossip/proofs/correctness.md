---
title: Push gossip is safe, informs every node with probability 1, and sends one message per informed node per round
proves: [correctness]
status: full
---

**Setting.** Nodes run lines L1 to L4 in the random phone call model on a connected graph $G$ with $n$ nodes, with no failures and $T_{\max} = \infty$. On the complete graph, a partner is uniform over the other $n - 1$ nodes; on $G$, it is uniform over the neighbors of the caller. $S_t$ is the set of informed nodes after round $t$, with $S_0 = \{s\}$.

**Lemma 1 (safety and monotonicity).** For every $t$, $S_t \subseteq S_{t+1}$, and every node in $S_t$ has received the rumor of $s$ or is $s$.

*Proof.* A node changes state only at line L4, from uninformed to informed, and only on receiving RUMOR. RUMOR is sent only at line L3 by an informed node. By induction on $t$, every RUMOR carries the rumor of $s$. No line makes a node uninformed. $\square$

**Lemma 2 (one round).** Let $u \notin S_t$. Given $S_t$, the events "$u \in S_{t+1}$" for different $u$ are determined by the independent choices of the nodes of $S_t$, and
$$\Pr[u \notin S_{t+1} \mid S_t] = \prod_{v \in S_t,\ v \sim u} \left(1 - \frac{1}{\deg(v)}\right),$$
where $v \sim u$ means that $v$ is a neighbor of $u$. On the complete graph this is $(1 - 1/(n - 1))^{|S_t|}$.

*Proof.* By line L4 and the rule that a node informed in round $t + 1$ pushes only from round $t + 2$ on, $u$ joins $S_{t+1}$ exactly when some $v \in S_t$ calls $u$ at line L2 of round $t + 1$. Each $v$ calls $u$ with probability $1/\deg(v)$ if $u$ is a neighbor and 0 otherwise, independently of the other nodes. $\square$

**Theorem 1 (eventual delivery).** With probability 1 there is a finite $T$ with $S_T = V$.

*Proof.* Let $u \notin S_t$ have a neighbor $v \in S_t$. By Lemma 1, $v \in S_{t'}$ for all $t' \ge t$, and by Lemma 2, in each later round $u$ stays uninformed with probability at most $1 - 1/\deg(v) \le 1 - 1/\Delta$, independently of the earlier rounds. So $u$ stays uninformed for $r$ more rounds with probability at most $(1 - 1/\Delta)^r \to 0$, and $u$ is informed after a finite time with probability 1. Order the nodes by their distance from $s$ in $G$; every node at distance $d \ge 1$ has a neighbor at distance $d - 1$, so by induction on $d$ every node is informed after a finite time with probability 1. There are finitely many nodes, so the maximum of these times is finite with probability 1. $\square$

**Theorem 2 (message count).** The number of messages sent until round $T$ is exactly $M = \sum_{t=0}^{T-1} |S_t|$, and on the complete graph $\mathbb{E}[|U_{t+1}| \mid S_t] = |U_t| (1 - 1/(n - 1))^{|S_t|}$.

*Proof.* In round $t + 1$, line L3 runs once for each node of $S_t$ and never for other nodes, which gives the sum. The second claim is Lemma 2 summed over $u \in U_t$ by [linearity of expectation](/linearity-of-expectation/). $\square$

**Consequence (the late phase).** On the complete graph, while $|S_t| \ge n/2$, Theorem 2 gives $\mathbb{E}[|U_{t+1}|] \le |U_t| e^{-1/2}$, and when $|S_t| = n - o(n)$ the factor is $e^{-1 + o(1)}$. Every round in the late phase sends at least $n/2$ messages, and the late phase lasts $(1 - o(1)) \ln n$ rounds by Pittel's theorem, so $M = \Omega(n \log n)$.

The bound $T = O(\log n)$ with high probability on the complete graph, and the exact form $\log_2 n + \ln n + O(1)$, are proved on [the push rumor spreading time page](/push-rumor-spreading-time/). With an age bound $T_{\max} = \log_2 n + c \ln n$ for a constant $c > 1$, the run is the same as the unbounded run up to round $T_{\max}$, so it informs every node whenever $T \le T_{\max}$, which by that proof holds with high probability; Theorem 1 does not apply, since with a finite $T_{\max}$ there is a small probability of failure.
