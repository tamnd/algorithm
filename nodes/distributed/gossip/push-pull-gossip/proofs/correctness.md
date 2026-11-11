---
title: Push-pull gossip is safe, and its late phase finishes in log2 ln n + O(1) rounds
proves: [correctness]
status: full
---

**Setting.** Nodes run lines L1 to L4 with the age rule on the complete graph with $n \ge 4$ nodes in the random phone call model, with no failures. $S_t$ and $U_t$ are the informed and uninformed nodes after round $t$, $s_t = |S_t|$, $u_t = |U_t|$ and $\varepsilon_t = u_t/n$. A node is active in round $t + 1$ if it is in $S_t$ and the age is at most $T_{\max}$.

**Lemma 1 (safety and monotonicity).** $S_t \subseteq S_{t+1}$, and every informed node other than the source received the rumor.

*Proof.* A node becomes informed only at line L4, after receiving RUMOR, which lines L2 and L3 send only from active nodes, and active nodes are informed. No line makes a node uninformed. $\square$

**Lemma 2 (domination by pull).** Given $U_t$ and an age at most $T_{\max}$, let $Y$ be the number of $v \in U_t$ whose call in round $t + 1$ goes to a node of $U_t \setminus \{v\}$. Then $u_{t+1} \le Y$ and $Y \sim \mathrm{Bin}(u_t, (u_t - 1)/(n - 1))$.

*Proof.* Let $v \in U_t$. If its call at line L1 goes to some $q \in S_t$, then $q$ is active and sends RUMOR to $v$ at line L3, so $v \in S_{t+1}$ by line L4. So $v \in U_{t+1}$ implies that the call of $v$ goes to $U_t \setminus \{v\}$, which gives $u_{t+1} \le Y$. Each call is uniform over the other $n - 1$ nodes and independent of the others, which gives the law of $Y$. $\square$

**Lemma 3 (Chernoff).** For a binomial $X$ with $\mathbb{E}[X] \le \mu$ and $0 < \delta \le 1$, $\Pr[X \ge (1 + \delta)\mu] \le e^{-\delta^2 \mu/3}$.

This is the standard [Chernoff bound](/chernoff-bound/); raising the mean to $\mu$ only increases the probability, since a binomial is stochastically increasing in its success probability.

**Theorem 1 (late phase).** If $u_t \le n/2$ and the age stays at most $T_{\max}$ for the next $r = \log_2 \ln n + 3$ rounds, then $u_{t+r} = 0$ with probability $1 - O(\log^2 n / n)$.

*Proof.* By Lemma 2, $\mathbb{E}[u_{t+1} \mid U_t] \le u_t (u_t - 1)/(n - 1) \le u_t^2/n$, and $u_{t+1}$ is at most a binomial with mean at most $u_t^2/n$.

*Squaring rounds.* While $u^2/n \ge 36 \ln n$, Lemma 3 with $\delta = 1/2$ gives $u_{t+1} \le \frac{3}{2} u_t^2/n$, that is $\varepsilon_{t+1} \le \frac{3}{2}\varepsilon_t^2$, with probability at least $1 - n^{-3}$. With $\eta_t = \frac{3}{2}\varepsilon_t$ we get $\eta_{t+1} \le \eta_t^2$ and $\eta_t \le \frac{3}{4}$ at the start, so after $j$ such rounds $\eta \le (3/4)^{2^j}$. For $j \ge \log_2 \ln n - \log_2(2 \ln \frac{4}{3})$, which is at most $\log_2 \ln n + 1$, this is at most $n^{-1/2}$, so $u < \sqrt{n}$ and the squaring rounds have ended.

*Two last rounds.* When $u^2/n < 36 \ln n$, the next round has mean below $36 \ln n$, and Lemma 3 with $\delta = 1$ gives $u \le 72 \ln n$ with probability at least $1 - n^{-12}$. In the next round $\mathbb{E}[u] \le (72 \ln n)^2/n$, so $\Pr[u \ge 1] \le 5184 \ln^2 n / n$ by [Markov's inequality](/markov-inequality/). Since $u$ never grows (Lemma 1), $u$ stays 0.

A [union bound](/union-bound/) over at most $\log_2 \ln n + 3$ rounds gives the claim. $\square$

**Theorem 2 (transmissions per round).** Given $S_t$, the expected number of RUMOR messages in round $t + 1$ is exactly $2 s_t$ when all nodes of $S_t$ are active.

*Proof.* Each active node sends one push at line L2 and one RUMOR at line L3 for each call it receives. Each of the other $n - 1$ nodes calls it with probability $1/(n - 1)$, so it receives one call in expectation. Summing over $S_t$ gives $s_t + s_t$. $\square$

**What is cited.** The early phases, from 1 to $n/2$ informed nodes in $\log_3 n + O(\log \log n)$ rounds w.h.p., and the sum $O(n/\ln n)$ of $s_t$ over the rounds with $s_t \le n/\ln n$, are from the proof of Theorem 2.1 of Karp et al. (2000). With them, Theorem 1 gives the time $\log_3 n + O(\log \log n)$, and Theorem 2 with at most $O(\log \log n)$ rounds of cost at most $2n$ gives $O(n \log \log n)$ transmissions in expectation. The median counter bound, Theorem 3.1 of Karp et al., is cited without proof.
