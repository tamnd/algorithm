---
title: Pull gossip squares the uninformed fraction and informs all nodes in O(log n) rounds
proves: [correctness]
status: full
---

**Setting.** Nodes run lines L1 to L4 on the complete graph with $n \ge 4$ nodes in the random phone call model, with $T_{\max} = \infty$ and no failures. $S_t$ and $U_t$ are the informed and uninformed nodes after round $t$, $u_t = |U_t|$, $s_t = |S_t|$ and $\varepsilon_t = u_t / n$. "With high probability" means with probability $1 - O(n^{-1} \log^2 n)$ or better.

**Lemma 1 (monotone and safe).** $S_t \subseteq S_{t+1}$, and a node is informed only after receiving the rumor of the source.

*Proof.* Only line L4 changes the state of a node, from uninformed to informed, and only on a RUMOR, which line L3 sends only from a node informed at the start of the round. $\square$

**Lemma 2 (exact law of one round).** Given $U_t$, the indicators $[v \in U_{t+1}]$ for $v \in U_t$ are independent, and each is 1 with probability $(u_t - 1)/(n - 1)$. Hence $u_{t+1} \sim \mathrm{Bin}(u_t, (u_t - 1)/(n - 1))$ and $\mathbb{E}[\varepsilon_{t+1} \mid U_t] \le \varepsilon_t^2$.

*Proof.* A node $v \in U_t$ can receive RUMOR in round $t + 1$ only as an answer to its own CALL, since line L3 answers the caller. The callee answers if and only if it is in $S_t$. So $v \in U_{t+1}$ if and only if the call of $v$ goes to $U_t \setminus \{v\}$, which has probability $(u_t - 1)/(n - 1)$. The calls of distinct nodes are independent. Finally $(u_t - 1)/(n - 1) \le u_t/n$ because $u_t \le n$. $\square$

**Lemma 3 (growth while few are informed).** Given $S_t$ with $s_t \le n/2$, $s_{t+1} - s_t \sim \mathrm{Bin}(n - s_t, s_t/(n - 1))$, with mean at least $s_t/2$.

*Proof.* By the argument of Lemma 2, each $v \in U_t$ joins independently with probability $s_t/(n - 1)$. The mean is $(n - s_t) s_t/(n - 1) \ge (n/2) s_t/(n - 1) \ge s_t/2$. $\square$

**Theorem 1 (start phase).** With high probability, $s_t > n/2$ for some $t \le C \log n$, for a constant $C$.

*Proof.* Split into two parts.

*From 1 to $24 \ln n$ informed nodes.* Write $X_t = s_{t+1} - s_t$. While $1 \le s_t \le 24 \ln n$, $\Pr[X_t \ge 1] = 1 - (1 - s_t/(n - 1))^{n - s_t} \ge 1 - e^{-s_t (n - s_t)/(n - 1)} \ge 1 - e^{-1/2} > 1/3$ for $n$ large enough, independently of the past given $s_t$. Each success raises $s$ by at least 1, so $24 \ln n$ successes are enough. In $R = 144 \ln n$ rounds, the number of successes dominates $\mathrm{Bin}(R, 1/3)$ with mean $48 \ln n$, which is below $24 \ln n$ with probability at most $e^{-48 \ln n / 8} = n^{-6}$ by the Chernoff lower tail.

*From $24 \ln n$ to $n/2$.* While $24 \ln n \le s_t \le n/2$, Lemma 3 and the Chernoff lower tail $\Pr[X < \frac{1}{2}\mu] \le e^{-\mu/8}$ with $\mu \ge s_t/2 \ge 12 \ln n$ give $X_t \ge s_t/4$, so $s_{t+1} \ge \frac{5}{4} s_t$, with probability at least $1 - n^{-3/2}$. After $\log_{5/4} n$ such rounds $s_t > n/2$. A [union bound](/union-bound/) over these $O(\log n)$ rounds gives failure probability $O(n^{-3/2} \log n)$. $\square$

**Theorem 2 (end phase).** If $u_t \le n/2$, then with high probability $u_{t + r} = 0$ for $r = \log_2 \ln n + O(1)$.

*Proof.* We use the [Chernoff bound](/chernoff-bound/) for a binomial $X$ with mean at most $\mu$: $\Pr[X \ge (1 + \delta)\mu] \le e^{-\delta^2 \mu / 3}$ for $0 < \delta \le 1$.

*Squaring.* Suppose $u_t^2 / n \ge 36 \ln n$. By Lemma 2, $u_{t+1}$ has mean at most $\mu = u_t^2/n$, and with $\delta = 1/2$ we get $u_{t+1} \le \frac{3}{2} u_t^2 / n$ with probability at least $1 - n^{-3}$, that is $\varepsilon_{t+1} \le \frac{3}{2} \varepsilon_t^2$. Put $\eta_t = \frac{3}{2} \varepsilon_t$; then $\eta_{t+1} \le \eta_t^2$ and $\eta_t \le 3/4$ at the start. After $r_1$ such rounds, $\eta \le (3/4)^{2^{r_1}}$. For $r_1 = \lceil \log_2 \ln n - \log_2 (2 \ln (4/3)) \rceil$ this is at most $n^{-1/2}$, so $u < \sqrt{n}$ and $u^2 / n < 36 \ln n$. Hence the squaring rounds end within $r_1 = \log_2 \ln n + O(1)$ rounds.

*Two more rounds.* Once $u^2 / n < 36 \ln n$, the next round has mean below $36 \ln n$, and Chernoff with $\delta = 1$ gives $u \le 72 \ln n$ with probability at least $1 - n^{-12}$. In the round after, the mean is at most $(72 \ln n)^2 / n$, and by [Markov's inequality](/markov-inequality/) $\Pr[u \ge 1] \le 5184 \ln^2 n / n$.

The union bound over the $r_1 + 2$ rounds gives failure probability $O(\log^2 n / n)$. $\square$

**Corollary (time).** With high probability, $T = O(\log n)$: Theorem 1 reaches $s > n/2$, that is $u < n/2$, within $O(\log n)$ rounds, and Theorem 2 finishes in $\log_2 \ln n + O(1)$ more.

**Theorem 3 (transmissions per round).** Given $S_t$, the expected number of RUMOR messages in round $t + 1$ is exactly $s_t$.

*Proof.* By line L3, a node of $S_t$ sends one RUMOR for each call it receives. Each of the other $n - 1$ nodes calls it with probability $1/(n - 1)$, so it receives one call in expectation. Sum over the $s_t$ nodes of $S_t$ by [linearity of expectation](/linearity-of-expectation/). $\square$

So the transmissions up to round $T$ are $\sum_{t < T} s_t$ in expectation given the run. Up to the first round with $s_t > n/2$ the counts grow geometrically by Theorem 1, so their sum is $O(n)$ plus $O(\log^2 n)$ for the first part, and Theorem 2 adds $O(\log \log n)$ rounds of at most $n$ each.
