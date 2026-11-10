---
title: FloodSet solves consensus with at most f crashes in f + 1 rounds
proves: [correctness, termination, time.worst]
status: full
---

**Claim.** In the synchronous model with $n$ processes, reliable links and at most $f$ crash failures, $0 \le f < n$, each run of FLOODSET has these properties. (Agreement) No two processes decide different values. (Validity) If all inputs equal $v$, each decision is $v$; with the rule $\min W$, each decision is an input. (Termination) Each process that does not crash decides at the end of round $f + 1$.

**Setup.** Fix a run. A process is *alive after round $r$* if it does not crash in rounds $1, \ldots, r$; let $A_r$ be this set, with $A_0$ the set of all processes. For $i \in A_r$, let $W_i(r)$ be the value of $W$ at $p_i$ after round $r$, with $W_i(0) = \{v_i\}$ from line L1. Round $r$ is *clean* if no process crashes in round $r$, that is, $A_r = A_{r-1}$. Let $I = \{v_1, \ldots, v_n\}$ be the set of inputs.

A process $p_k \in A_{r-1}$ sends $W_k(r-1)$ in round $r$ (line L3). If $p_k \in A_r$, the message reaches each other process. If $p_k$ crashes in round $r$, it reaches a subset of the others. A process $p_i \in A_r$ receives these messages and sets $W_i(r)$ to the union of $W_i(r-1)$ and the received sets (lines L4 and L5). So for each $i \in A_r$:

$$W_i(r) = W_i(r-1) \cup \bigcup_{k \in S_i(r)} W_k(r-1), \qquad A_r \setminus \{i\} \subseteq S_i(r) \subseteq A_{r-1} \setminus \{i\}, \tag{1}$$

where $S_i(r)$ is the set of senders whose round $r$ message reaches $p_i$. The left inclusion holds because a process that stays alive sends to all.

**Lemma 1 (only inputs).** For each $r$ and each $i \in A_r$, $W_i(r) \subseteq I$.

*Proof.* By induction on $r$. $W_i(0) = \{v_i\} \subseteq I$. By (1), $W_i(r)$ is a union of sets $W_k(r-1)$ with $k \in A_{r-1}$, and each is a subset of $I$ by the induction hypothesis. $\square$

**Lemma 2 (clean round).** If round $r$ is clean, then $W_i(r) = W_j(r)$ for all $i, j \in A_r$.

*Proof.* Round $r$ is clean, so $A_r = A_{r-1}$, and (1) gives $S_i(r) = A_{r-1} \setminus \{i\}$. Then $W_i(r) = \bigcup_{k \in A_{r-1}} W_k(r-1)$. The right side does not depend on $i$. $\square$

**Lemma 3 (equal sets stay equal).** If there is a set $X$ with $W_i(r) = X$ for all $i \in A_r$, then $W_i(r') = X$ for all $r' \ge r$ and all $i \in A_{r'}$.

*Proof.* By induction on $r'$. The case $r' = r$ is the hypothesis. Let $r' > r$ and $i \in A_{r'}$. Then $i \in A_{r'-1}$ and each $k \in S_i(r')$ is in $A_{r'-1}$, so by the induction hypothesis each set in (1) equals $X$. The union of one or more copies of $X$ is $X$. $\square$

**Lemma 4 (a clean round exists).** Among rounds $1, \ldots, f + 1$, at least one is clean.

*Proof.* A round that is not clean has at least one process that crashes in it, and each process crashes in at most one round. At most $f$ processes crash, so at most $f$ of the $f + 1$ rounds are not clean. $\square$

**Agreement.** Let $c \le f + 1$ be a clean round, by Lemma 4. By Lemma 2, all processes in $A_c$ have the same set $X$ after round $c$. By Lemma 3, all processes in $A_{f+1}$ have $W = X$ after round $f + 1$. A process decides only in lines L6 and L7, after round $f + 1$, so only the processes in $A_{f+1}$ decide. The decision is a function of $W$ alone, so all of them decide the same value. This also covers a process that would crash after it decides, so the agreement is uniform.

**Validity.** Assume all inputs equal $v$. Then $I = \{v\}$. Each $W_i(r)$ holds $v_i = v$ for all $r$, because (1) only adds values, and $W_i(r) \subseteq \{v\}$ by Lemma 1. So $W = \{v\}$ at each deciding process, and line L6 decides $v$. With the rule $\min W$, the decision is in $W \subseteq I$ by Lemma 1, so it is an input.

**Termination and rounds.** The loop of line L2 runs exactly $f + 1$ times, and each round ends, because the synchronous model delivers all messages of a round within the round. A process in $A_{f+1}$ then runs line L6 or line L7 and decides. So each process that does not crash decides at the end of round $f + 1$, in every run. $\blacksquare$
