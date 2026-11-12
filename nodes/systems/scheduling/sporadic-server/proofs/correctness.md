---
title: A sporadic server at the top priority runs at most Cs units in any window of length Ts
proves: [correctness]
status: full
---

**Setting.** Time is cut into unit slots. One processor runs periodic tasks $\tau_j = (C_j, T_j, D_j)$ with $D_j \le T_j$ and distinct fixed priorities, and one sporadic server with capacity $C_s$ and period $T_s$, $1 \le C_s \le T_s$. The server starts with $c = C_s$. The proof below is for a server with the highest priority, which is the common case and the case in which the replenishment rules are simplest. For a server at any priority, Sprunt, Sha and Lehoczky state that the server acts on lower tasks like a periodic task $(C_s, T_s)$; the implementation tests that claim at random priorities, and the remark at the end gives the reason.

**Chunks.** With the top priority, the server is *active* (running priority at least $P_s$) exactly in the slots in which it runs. Line L6 arms the server at the first slot $t_A$ of a run, with $RT = t_A + T_s$ and $used = 0$. Line L7 counts each slot. The run ends when the server stops running (line L5) or when $c$ reaches 0 (line L8), and then the amount $u$ used since $t_A$ is added back at time $t_A + T_s$ (line L1). Call the slots between an arming and the next finalize a *chunk*. A chunk is a block of consecutive slots, it starts at its arming time $t_A$, and all of its units come back together at $t_A + T_s$.

**Tokens.** Think of the capacity as $C_s$ tokens. Line L7 takes one token from $c$ for each slot the server runs. A finalized chunk holds its tokens until its replenishment time, and line L1 puts them back into $c$. So at each time $t$, after line L1,

$$C_s = c(t) + P(t) + b(t), \qquad (1)$$

where $P(t)$ is the number of tokens of finalized chunks that come back after $t$, and $b(t)$ is the number of slots before $t$ of a chunk that is not yet finalized at $t$. Equation (1) holds at the start, and each line keeps it: line L7 moves one token from $c$ to $b$, a finalize moves $b$ to $P$, and line L1 moves tokens from $P$ to $c$.

**Lemma 1.** A chunk has at most $C_s$ slots, so it ends no later than $t_A + C_s \le t_A + T_s$.

*Proof.* The tokens used in a chunk come back only at $t_A + T_s$, after the chunk is finalized. So each slot of the chunk uses a token that it does not give back during the chunk, and by (1) there are at most $C_s$ of them. $\square$

**Lemma 2 (window bound).** For each $t \ge 0$, the server runs in at most $C_s$ slots of $W = [t, t + T_s)$.

*Proof.* A token that the server uses in $W$, in a chunk that starts at $t' \ge t$, comes back at $t' + T_s \ge t + T_s$, after $W$. So such a token is used at most once in $W$.

*Case 1: no chunk is in progress at $t$*, that is, $b(t) = 0$. Every slot of $W$ in which the server runs belongs to a chunk that starts in $W$, so it uses a distinct token. The tokens that can be used are those in $c(t)$ and those that come back during $W$, which are at most $P(t)$. By (1), the count is at most $c(t) + P(t) = C_s$.

*Case 2: a chunk $A$ started at $t_A < t$ and is still in progress at $t$*, so $b = b(t) = t - t_A \ge 1$. By Lemma 1, $b \le C_s \le T_s$, so the time $t_A + T_s$ at which the tokens of $A$ come back is in $(t, t + T_s]$. Cut $W$ into $W_1 = [t, t_A + T_s)$ and $W_2 = [t_A + T_s, t + T_s)$. The length of $W_2$ is $t - t_A = b$, so the server runs in at most $b$ slots of $W_2$. In $W_1$, the server runs in the rest of $A$ or in chunks that start at $t' \ge t$. Neither gets its tokens back inside $W_1$, so each slot uses a distinct token. These tokens are in $c(t)$ or come back from finalized chunks during $W_1$, and by (1) there are at most $c(t) + P(t) = C_s - b$ of them. So the total is at most $(C_s - b) + b = C_s$. $\square$

**Corollary.** In any window of length $w$, the server runs in at most $\lceil w / T_s \rceil C_s$ slots: cut the window into $\lceil w / T_s \rceil$ pieces of length at most $T_s$ and apply Lemma 2 to each.

**Theorem.** Let the server have the highest priority, and for each periodic task $\tau_i$ let $R_i$ be the least positive solution of

$$R = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R}{T_j} \right\rceil C_j + \left\lceil \frac{R}{T_s} \right\rceil C_s .$$

If $R_i \le D_i$, each job of $\tau_i$ ends within $R_i$ of its release.

*Proof.* By induction on the jobs of $\tau_i$ in order of release. Let job $J$ be released at $r$ and end at $f$, and assume that every earlier job of $\tau_i$ ended by $r$. Call a slot *high* if it runs the server or a job of a task in $hp(i)$. Let $t_0 \le r$ be the smallest time such that each slot of $[t_0, r)$ is high. If $t_0 > 0$, slot $t_0 - 1$ is idle or runs a job of priority at most that of $\tau_i$, so no job of $hp(i)$ was pending then. So each job of $hp(i)$ that runs in $[t_0, f)$ was released at or after $t_0$.

Assume that $f > t_0 + R_i$. Each of the $R_i$ slots of $[t_0, t_0 + R_i)$ runs $J$ or high work: before $r$ by the choice of $t_0$, and after $r$ because $J$ is pending and only higher work can run in its place. $J$ runs in fewer than $C_i$ of them. The jobs of $\tau_j$ released in the window number at most $\lceil R_i / T_j \rceil$. The server runs in at most $\lceil R_i / T_s \rceil C_s$ of them by the corollary. So the number of slots is less than $R_i$, which is false. Hence $f \le t_0 + R_i \le r + D_i$. $\blacksquare$

**Remark.** At a lower priority, the server is also active while a job of higher priority runs, and that time does not use its budget. Line L6 arms the server at the time $t_A$ when the level $P_s$ becomes busy, and the budget used before the level goes idle comes back at $t_A + T_s$. This is the same as a job of a periodic task $(C_s, T_s)$ that is released at $t_A$ and delayed by higher work, which the response-time test already allows. Sprunt, Sha and Lehoczky used this to show that, for lower tasks, the server is no worse than a periodic task. Later work found a defect in their first statement of the rules, and the POSIX rules had others, which Stanovich, Baker, Wang and González Harbour described and corrected in 2010. The rules in the implementation are the form in Buttazzo's book.
