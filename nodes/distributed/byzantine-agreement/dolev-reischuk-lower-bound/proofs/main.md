---
title: Deterministic Byzantine broadcast needs Omega(n + t^2) messages
proves: [statement]
status: full
---

This proof covers parts 1 and 2 of the statement. Part 3, on signatures and on messages without authentication, is cited from Dolev and Reischuk (1985). The proof of part 1 follows the warmup proof of Abraham et al. (2019), with one change: the isolated process is chosen with both runs $E_0$ and $E_1$ before the input is fixed.

**Statement.** Let $A$ be a deterministic algorithm for Byzantine broadcast in the synchronous model with $n$ processes, a sender $s$ with a binary input, and at most $t$ faulty processes, where $2 \le t < n$. Signatures may be used. Let $k = \lfloor t/2 \rfloor$. Then:

1. some run of $A$ with at most $t$ faulty processes, which only omit messages, has at least $k^2/2$ messages sent by correct processes;
2. some failure-free run of $A$ has at least $(n - 1)/2$ messages.

**Setup.**

1. In each round, each process sends messages and then receives the messages sent to it in that round. A correct process follows $A$. Its messages and its output are functions of its *view*: its identity, its keys, its input if it is the sender, and the messages it has received, with sender and round.
2. Order the messages that a process receives by round, and inside a round by the identity of the sender. "The first $k$ messages" refers to this order.
3. A faulty process in this proof only *omits*: in each round it sends a subset of the messages that $A$ would send from its current view, and it may treat some received messages as not received. Such a process never forges anything, so signatures do not stop it.
4. Broadcast requires, in each run with at most $t$ faulty processes: every correct process outputs a value (termination); all correct processes output the same value (agreement); if the sender is correct, the value is its input (validity).

**Part 1.**

1. Assume that in every run of $A$ with at most $t$ omission faults, the correct processes send fewer than $k^2/2$ messages. Note $k \ge 1$ since $t \ge 2$.
2. *The set $V$.* Fix a set $V$ of $k$ processes that does not contain $s$. This is possible because $k \le t/2 < n - 1$ for $t \ge 2$ and $t < n$. Let $U$ be the set of the other $n - k$ processes. It contains $s$.
3. *Runs $E_0$ and $E_1$.* In $E_b$, the sender has input $b$. The processes of $U$ are correct. Each process of $V$ is faulty and does the following: it follows $A$, but it does not send any message to a process of $V$, and it treats the first $k$ messages it receives as not received. This is $k \le t$ omission faults.
4. In $E_b$ the sender is correct with input $b$, so by validity and termination every process of $U$ outputs $b$.
5. *A process that hears little.* Processes of $V$ send nothing to $V$, so every message that a process of $V$ receives in $E_b$ comes from $U$ and is counted. By step 1, fewer than $k^2/2$ messages are sent in each of $E_0$ and $E_1$, so fewer than $k^2$ messages are received by processes of $V$ in the two runs together.
6. Assume that each $q \in V$ receives more than $k$ messages in $E_0$ or more than $k$ messages in $E_1$. Then the two runs together deliver at least $k(k + 1) > k^2$ messages to $V$, which contradicts step 5. So there is a $p \in V$ that receives at most $k$ messages in $E_0$ and at most $k$ messages in $E_1$.
7. By step 3, $p$ treats all messages it receives in $E_0$ and in $E_1$ as not received. So in both runs $p$ acts as a correct process whose view has no messages. Call this the *empty view* of $p$. It is the same in both runs, since $p$ is not the sender.
8. *Runs $E'_0$ and $E'_1$.* Let $S_b \subseteq U$ be the set of processes that send at least one message to $p$ in $E_b$. Then $|S_b| \le k$. In $E'_b$, the sender has input $b$. The process $p$ is correct. Each process of $V \setminus \{p\}$ is faulty and acts as in $E_b$: it follows $A$, sends nothing to $V$, treats the messages from $p$ as not received, and treats the first $k$ other messages it receives as not received. Each process of $S_b$ is faulty: it follows $A$, except that it sends nothing to $p$. The processes of $U \setminus S_b$ are correct.
9. The faulty processes of $E'_b$ are $(V \setminus \{p\}) \cup S_b$. There are at most $(k - 1) + k \le t - 1$ of them, and they only omit messages. So $E'_b$ is a run of the model, and $A$ satisfies agreement and termination in it.
10. *Claim: after each round $r$, (a) $p$ has received no message in $E'_b$, and (b) every process $q \ne p$ has the same view in $E'_b$ as in $E_b$, counting only the messages that $q$ treats as received.* By induction on $r$. Both hold before round 1. Assume both after round $r - 1$. In round $r$:
    - The processes of $U \setminus S_b$ are correct in both runs and have the same views, so they send the same messages. In $E_b$ they send nothing to $p$, by the choice of $S_b$, so they send nothing to $p$ in $E'_b$ either.
    - The processes of $S_b$ have the same views, so they compute the same messages. In $E'_b$ they send all of them except those to $p$.
    - The processes of $V \setminus \{p\}$ have the same views and act by the same rule, so they send the same messages, and none to $p$.
    - The process $p$ has the empty view in $E'_b$ by (a), and acts on the empty view in $E_b$ by step 7. So it sends the same messages to $U$ in both runs. In $E'_b$ it also sends to $V \setminus \{p\}$, which treat these messages as not received, as they treat nothing from $p$ in $E_b$ either, where $p$ sends nothing to $V$.
    - So $p$ receives nothing in round $r$ of $E'_b$, which gives (a). Every $q \ne p$ receives the same messages from every process in round $r$ in both runs, except for messages from $p$ to $V \setminus \{p\}$, which $q$ treats as not received. So (b) holds after round $r$.
11. By step 10, each process of $U \setminus S_b$ has the same view in $E'_b$ as in $E_b$, so it outputs $b$ by step 4. This set has at least $n - k - k \ge n - t \ge 1$ processes, and they are correct in $E'_b$.
12. By step 10, $p$ has the empty view in $E'_0$ and in $E'_1$. $A$ is deterministic, so $p$ outputs one value $c$ in both. It outputs some value, by termination in $E'_0$.
13. Let $b = 1 - c$. In $E'_b$, the correct process $p$ outputs $c$, and the correct processes of $U \setminus S_b$ output $b \ne c$. This breaks agreement, and the assumption of step 1 is false. $\square$

**Part 2.**

1. Let $F_b$ be the failure-free run with input $b$. By validity, every process outputs $b$ in $F_b$.
2. Let $q \ne s$ be a process that receives no message in $F_0$ and none in $F_1$. Its view is the empty view in both runs, so it outputs the same value in both. But it outputs 0 in $F_0$ and 1 in $F_1$. So there is no such $q$.
3. So each of the $n - 1$ non-senders receives at least one message in $F_0$ or in $F_1$. The two runs together have at least $n - 1$ messages, and one of them has at least $(n - 1)/2$. $\square$

**Conclusion.** Some run has at least $\max(k^2/2, (n - 1)/2) \ge (k^2/2 + (n - 1)/2)/2$ messages from correct processes. With $k = \lfloor t/2 \rfloor$, this is $\Omega(n + t^2)$. $\blacksquare$
