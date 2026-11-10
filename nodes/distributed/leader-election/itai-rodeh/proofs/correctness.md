---
title: Itai-Rodeh is always correct, ends with probability 1, and has O(n log n) expected messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run ITAI-RODEH on an anonymous unidirectional ring of $n \ge 1$ processes with reliable FIFO channels, every process knowing $n$, under any schedule. Then (a) in every run at most one process becomes the leader; (b) with probability 1 exactly one process becomes the leader and all messages are consumed; (c) the expected number of rounds is at most $(1 - 1/n)^{-n}$; (d) the expected number of messages is at most $(1 - 1/n)^{-n} \, n (H_n + 1)$. For $n = 1$ the only process gets its own message back clean with $h = 1$ and is the leader.

Write $\pi = (r, v)$ for the *tag* of an active process and of the message it sends in line L2. Tags compare round first. The message with tag $\pi$ sent by $p$ is called $p$'s round-$r$ message.

**Lemma 1 (hops).** A message with hop count $h$ is at the process $h$ links after its sender. In particular a message with $h = n$ is at its sender.

*Proof.* Line L2 sends with $h = 1$ to the next process, and each forward (lines L3, L4, L6) adds 1 and moves one link. $\square$

**Lemma 2 (who returns).** If $p$'s round-$r$ message comes back to $p$ while $p$ is still active with tag $\pi$, then on its way it met no active process with a larger tag, and it is dirty exactly when it met an active process with the same tag $\pi$.

*Proof.* By lines L4 to L6 an active process with a larger tag drops the message, one with a smaller tag forwards it unchanged and becomes passive, one with the same tag sets the bit, and passive processes forward it unchanged. When it reaches $p$ with $h = n$ (Lemma 1) and $p$ has tag $\pi$, line L7 or L8 runs. $\square$

**Lemma 3 (tags only grow, passive is final).** The tag of a process only grows, and a passive process never becomes active.

*Proof.* Line L2 raises the round; no line lowers it or sets $\mathit{active}$ to true after line L1. $\square$

**Part (a), at most one leader.** Let $p$ be the first process that becomes the leader, at time $t_1$, with tag $\pi = (r, v)$. By Lemma 2 its message came back clean, so on its way it met no active process other than $p$ with a tag $\ge \pi$. So each $q \ne p$, at the moment the message passed it, was passive, or was active with a smaller tag and became passive by line L4. By Lemma 3 every $q \ne p$ is passive from then on, and a passive process never runs line L7. No $q$ became the leader before $t_1$, since $p$ is the first. Hence there is at most one leader.

**Lemma 4 (each round has a survivor).** Suppose some process starts round $r$. Let $v^*$ be the largest value drawn in round $r$. Then some process with tag $(r, v^*)$ gets its round-$r$ message back while active with that tag, unless a process has entered round $r + 1$ or become the leader in round $r$.

*Proof.* Take the processes with tag $(r, v^*)$; their messages can only be dropped by an active process with a larger tag, that is, one in a round $> r$. If no process reaches a later round, the messages are never dropped and each one comes back. Such a process stays active, since only a larger tag makes it passive. $\square$

**Lemma 5 (a unique maximum ends the election).** If in round $r$ the largest value $v^*$ is drawn by exactly one process $p$, then $p$ becomes the leader in round $r$.

*Proof.* No process enters round $r + 1$: that needs a dirty own message of round $r$ that returns, and a returning round-$r$ message met no larger tag, so its value is $v^*$ (it passed $p$, or reached $p$'s position while $p$ was in round $r$; if $p$ were still in round $r - 1$ at that moment, $p$ became passive and would not have drawn in round $r$). Only $p$ has $v^*$, and its message is clean because no other active process has tag $(r, v^*)$. By Lemma 4 the message comes back, and line L7 makes $p$ the leader. $\square$

**Part (b) and (c).** Let $k_r \ge 1$ be the number of processes that draw in round $r$. Their values are independent and uniform on $\{1, \ldots, n\}$, and independent of everything before. If $k_r = 1$ the maximum is unique. If $k_r = k \ge 2$, the probability that it is unique is
$$P_k = \sum_{m=1}^{n} k \cdot \tfrac{1}{n} \left(\tfrac{m-1}{n}\right)^{k-1} = \tfrac{k}{n} \sum_{j=1}^{n-1} f(j/n), \qquad f(x) = x^{k-1}.$$
Since $f$ is increasing, $f(j/n) \ge n \int_{(j-1)/n}^{j/n} f$, so $\sum_{j=1}^{n-1} f(j/n) \ge n \int_0^{(n-1)/n} f = \frac{n}{k} (1 - \tfrac1n)^k$, and $P_k \ge (1 - 1/n)^k \ge (1 - 1/n)^n =: q$. By Lemma 4 every round either ends the election or leads to a next round, and by Lemma 5 each round ends it with probability at least $q$, given the past. So $\Pr[R > t] \le (1 - q)^t$, the number of rounds $R$ is finite with probability 1, and $\mathbb{E}[R] \le 1/q = (1 - 1/n)^{-n} \le e \cdot n/(n-1)$. When the leader $p$ is elected with tag $\pi$, all other processes are passive and stay so (part (a)). No message has a tag larger than $\pi$: its sender would have dropped $p$'s message, or, if it drew after the message passed, it was already passive and could not draw. Messages with the tag $\pi$ come only from $p$. So every message still in transit is forwarded by passive processes until it reaches $p$, which drops it by line L5, within $n$ hops.

**Part (d).** Fix a round $r$ with $k$ drawing processes $c_1, \ldots, c_k$ in ring order; their positions are fixed by the past and their values are fresh. The round-$r$ message of $c_s$ crosses a link that lies after $c_{s+j}$ and before $c_{s+j+1}$, for $0 \le j \le k - 1$, only if $v_{c_s} \ge v_{c_{s+1}}, \ldots, v_{c_{s+j}}$, because the first active process with a larger round-$r$ value drops it; being dropped earlier by a process in a later round only lowers the count. For independent uniform values,
$$\Pr[v_0 \ge \max(v_1, \ldots, v_j)] = \sum_{m=1}^{n} \tfrac1n \left(\tfrac mn\right)^j \le \int_0^1 x^j \, dx + \tfrac1n = \tfrac{1}{j+1} + \tfrac1n,$$
using $\frac1n (m/n)^j \le \int_{m/n}^{(m+1)/n} x^j dx$ for $m \le n - 1$ and $\frac1n$ for $m = n$. Each link lies after exactly one $c_{s+j}$ for each $j$ when counted from the $k$ senders, so the expected number of round-$r$ messages on a link is at most $\sum_{j=0}^{k-1} \left(\frac{1}{j+1} + \frac1n\right) \le H_k + 1 \le H_n + 1$, and over the $n$ links at most $n(H_n + 1)$. The event $R \ge r$ depends only on rounds before $r$, so
$$\mathbb{E}[M] = \sum_{r \ge 1} \mathbb{E}[M_r \mathbf{1}_{R \ge r}] \le n (H_n + 1) \sum_{r \ge 1} \Pr[R \ge r] = n(H_n + 1)\, \mathbb{E}[R] \le \left(1 - \tfrac1n\right)^{-n} n (H_n + 1).$$
This is $O(n \log n)$. $\blacksquare$
