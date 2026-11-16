---
title: Under diminishing marginal gain the sequential greedy assignment that CBBA reaches is at least half of the optimum, and agreement needs at least as many rounds as the distance to the winner
proves: [correctness]
status: partial
---

There are $r$ agents and $t$ tasks, with scores $a_{ij} > 0$. Agent $i$ can hold at most $L$ tasks. The score of a bundle is the one of the code on the [CBBA](/consensus-based-bundle-algorithm/) page: if agent $i$ already holds $n$ tasks, a new task $j$ is worth $a_{ij} \gamma^n$, with $0 < \gamma \le 1$. The communication graph is fixed, undirected and connected, with diameter $D$, and time is synchronous. Lines L1 to L15 refer to the pseudocode on the page.

The proof has three parts. Theorem 1 is a full proof that the sequential greedy assignment (SGA) is at least half of the optimum under this score. Theorem 2, that CBBA reaches the SGA assignment without conflicts within $N_{min} D$ rounds, is the theorem of Choi, Brunet and How (2009); here it is stated with its hypotheses and a proof sketch, and the tests check it on random instances. Theorem 3 is a full proof that $D$ rounds can be needed.

## The team score

For a set $S$ of tasks given to agent $i$, let $f_i(S) = \sum_{n=0}^{\min(|S|, L) - 1} \gamma^n x_{(n)}$, where $x_{(0)} \ge x_{(1)} \ge \dots$ are the values $a_{ij}$, $j \in S$, in decreasing order. This is the best score of the bundle when the agent does its best tasks first and ignores tasks beyond $L$. The team score of an assignment, which gives each task to at most one agent, is $F = \sum_i f_i(S_i)$. The test helper `assignment_value` computes $F$, and the brute force optimum maximizes it.

**Lemma 1 (diminishing marginal gain).** Each $f_i$ is monotone and submodular: for $S \subseteq T$ and a task $j \notin T$, $f_i(S \cup \{j\}) - f_i(S) \ge f_i(T \cup \{j\}) - f_i(T) \ge 0$.

*Proof.* Let $\mathrm{top}_k(S)$ be the sum of the $k$ largest values in $S$, or of all of them if $|S| < k$. It is the weighted rank function of the uniform matroid of rank $k$, which is monotone and submodular. The weights $w_n = \gamma^n$ for $n < L$ and $w_n = 0$ for $n \ge L$ do not increase in $n$, so by summation by parts $f_i = \sum_{k \ge 1} (w_{k-1} - w_k) \mathrm{top}_k$, a combination of these functions with coefficients $\ge 0$. Such a combination is monotone and submodular. $\square$

$F$ is then a monotone submodular function of the set of agent-task pairs, and the rule "each task goes to at most one agent" is a partition matroid on these pairs.

**Lemma 2 (SGA is the greedy algorithm for $F$).** SGA repeatedly takes the agent-task pair $(i, j)$ with the largest value $a_{ij} \gamma^{|S_i|}$ among free tasks and agents with $|S_i| < L$. Each such value is the true marginal gain $F(G + (i, j)) - F(G)$, and every pair that SGA does not consider has marginal gain $0$.

*Proof.* When SGA gives task $j'$ to agent $i$ with value $a_{ij'} \gamma^{n}$, the value of every free task $j$ for the same agent was at most this, so $a_{ij} \le a_{ij'}$. So the tasks of each agent arrive in decreasing order of $a_{ij}$, and every free task has a value at most the smallest value in $S_i$. Adding such a task to $S_i$ puts it at position $|S_i|$ in the sorted order, so the gain is $a_{ij} \gamma^{|S_i|}$ if $|S_i| < L$ and $0$ if $|S_i| = L$. $\square$

**Theorem 1 (half of the optimum).** Let $G$ be the SGA assignment and $O$ an optimal one. Then $F(G) \ge \frac12 F(O)$.

*Proof.* Let $g_1, \dots, g_k$ be the pairs that SGA picks, in order, with gains $\delta_1, \dots, \delta_k$, so $F(G) = \sum_\tau \delta_\tau$, and let $G_\tau = \{ g_1, \dots, g_\tau \}$. By monotonicity and submodularity, $F(O) \le F(O \cup G) \le F(G) + \sum_{e \in O \setminus G} \Delta(e \mid G)$, where $\Delta(e \mid X) = F(X + e) - F(X)$. Take $e = (i, j) \in O \setminus G$. If SGA gave task $j$ to some agent at step $\tau$, then $e$ was a feasible pair before step $\tau$, because task $j$ was free, so $\Delta(e \mid G_{\tau - 1}) \le \delta_\tau$ by Lemma 2 and the greedy choice, and $\Delta(e \mid G) \le \Delta(e \mid G_{\tau - 1})$ by submodularity. Each step $\tau$ takes one task, and $O$ gives each task to one agent, so each $\delta_\tau$ is used at most once. If SGA never gave task $j$ away, then when SGA stopped, agent $i$ was full, since otherwise the pair $(i, j)$ was still available; so $\Delta(e \mid G) = 0$ by Lemma 2. Summing, $F(O) \le F(G) + \sum_\tau \delta_\tau = 2 F(G)$. $\square$

This is the argument of Fisher, Nemhauser and Wolsey (1978) for greedy maximization of a monotone submodular function over a matroid, applied to this score. The test `test_half_of_optimum_under_dmg` checks $2 F \ge F(O)$ against brute force and finds instances with $F < F(O)$, so the bound is not an equality. On the three-agent example of the page, SGA gives $16$ and the optimum is $17$.

## Convergence to the SGA assignment

**Theorem 2 (Choi, Brunet and How 2009).** Suppose the score has diminishing marginal gain, the network is fixed and connected with diameter $D$, the rounds are synchronous, and the consensus phase uses the decision table of the paper. Then after at most $N_{min} D$ rounds, where $N_{min} = \min(t, L r)$, all agents hold the same winners and winning bids, no task has two winners, and the assignment is the SGA assignment.

*Proof sketch.* Induction on the SGA steps. Suppose all agents agree on the first $k$ SGA pairs. The pair $(i^*, j^*)$ of step $k + 1$ has the largest value among the rest. Under diminishing marginal gain no agent can bid more than this value on $j^*$ once its bundle holds its first SGA tasks, so agent $i^*$ adds $j^*$ in its bundle phase, and no other bid on $j^*$ beats it. The table makes a receiver update to a bid that the sender wins with a better bid, and the timestamps make newer information win over older information about a third agent. So the claim of $i^*$ on $j^*$ spreads one hop per round, is never reset, and reaches every agent within $D$ rounds. Each SGA step adds one pair, and there are at most $N_{min}$ steps. The full proof, with the cases of the table, is in the paper. $\square$

**What the code changes, and how it is checked.** The release rule of line L13 in the paper resets every task after the first task the agent has lost. The code removes these tasks from the bundle, but it keeps a record that another agent wins such a task, and it resets only the entries where the agent itself was the winner. With the paper's rule, the code ran into a cycle of period one on about one random instance in three thousand, because the reset erased the information about the true winner of a later task in every round. The test `test_agreement_and_equal_to_sequential_greedy` checks on 300 random instances, with up to 6 agents and 7 tasks on random connected graphs, that all agents agree, that no task has two winners, that the result equals SGA, and that the number of rounds is at most $N_{min} D$. These are measurements, not a proof for the changed rule.

## A lower bound on the rounds

**Theorem 3 ($D$ rounds can be needed).** On a path of $r$ agents with one task, $L = 1$, and $a_{i0} = i + 1$, every agent must end with winner $r - 1$, and agent $0$ cannot know it before round $r - 1 = D$.

*Proof.* The best agent is $r - 1$, so by Theorem 2 and Lemma 2 all agents end with winner $r - 1$. In round 1, agent 0 claims the task for itself, since it knows no other bid. In a synchronous round an agent receives only the values its neighbors held at the end of the round before, so information that starts at agent $r - 1$ reaches agent $r - 1 - k$ at the earliest in round $k$. So agent 0 learns of agent $r - 1$'s bid at the earliest in round $r - 1$, and before that its winner is wrong. $\square$

The test `test_line_needs_diameter_rounds` measures exactly $r - 1$ rounds for $r = 2, \dots, 7$, so the bound of Theorem 2 is reached for $N_{min} = 1$.
