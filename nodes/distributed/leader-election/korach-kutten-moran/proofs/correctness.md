---
title: The complete-network form elects exactly one leader with at most 4nH_n messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run KKM-COMPLETE on a complete network of $n \ge 2$ processes with distinct identifiers, in the asynchronous model with reliable channels, FIFO or not, under any schedule, where a nonempty set of processes start. Then (a) every run is finite; (b) exactly one process ends with status *leader*, the candidate with the largest final pair; (c) at most $n / (j + 1)$ candidates reach level $j$, for every $j \ge 0$; (d) the run sends at most $4 n H_n$ messages, where $H_n = \sum_{i=1}^{n} 1/i$; (e) if every message takes exactly one time unit, the run ends by a time no larger than the number of messages.

This proof covers the complete-network form on the page, not the general token scheme of the paper.

**Basic facts.** (F1) The pair of a process never decreases: $\mathit{lev}$ changes only in L1 (from $-1$ to $0$) and in L6 (by one). (F2) A candidate has at most one CAP in transit or in a queue, because it sends a new one only in L6, after the answer to the last one. (F3) Every CAP gets exactly one answer, ACC or REJ: it is handled in L2, or in L3 and then in L5 after the answer to its query, and a queued CAP is handled when the process stops being busy. (F4) A candidate $c$ sends its requests on distinct links, so it never sends a CAP to a process it has already captured, and $n - 1$ requests are enough to reach every other process. (F5) While a candidate $c$ is alive, $\mathrm{owner}(c) = c$. The owner of $c$'s own process changes only in L2 at $c$, and that line sets $\mathit{alive}_c \leftarrow \mathit{false}$ at the same moment.

**Lemma 1 (owners get stronger).** Let $o$ and $o'$ be two successive owners of a process $y$, where $o'$ takes over from $o$ at time $t$ with request pair $P'$. Then $P' > \mathrm{pair}(o)$ at time $t$. If $o$ is alive at time $t$, it dies at time $t$.

*Proof.* The owner changes in L2 or in L5. In L2, $o = y$ and the line compares $P'$ with $\mathrm{pair}(y)$ and sets $\mathit{alive}_y \leftarrow \mathit{false}$. In L5, the change follows a YES from $o$, sent in L4 after the comparison $P' > \mathrm{pair}(o)$, which also sets $\mathit{alive}_o \leftarrow \mathit{false}$. While $y$ is busy, no other CAP at $y$ is handled, so the owner of $y$ is still $o$ when the YES arrives. The pair of $o$ cannot change between the comparison and time $t$ in a way that matters: $o$ is dead after the comparison, and a dead candidate does not change its level in L6. $\square$

By Lemma 1 and F1, the request pairs of the successive owners of a process increase strictly, and each is larger than the pair of the process itself at its first capture.

**Lemma 2 (domains are disjoint).** For a candidate $c$ that reaches level $j$, let $S_c$ be its own process together with the $j$ processes whose ACC raised its level from $0, 1, \ldots, j - 1$. If $c \ne d$ both reach level $j$, then $S_c \cap S_d = \emptyset$.

*Proof.* Let $t_c$ be the time at which $c$ reaches level $j$. First, every capture of a process $y \in S_c$ by a new owner after $c$ happens after $t_c$ and has a request pair of level at least $j$. Take $y \in S_c$.

- If $y$ is $c$'s own process, $c$ owns it while alive (F5), and its first capture kills $c$ if $c$ is alive (Lemma 1). Since $c$ reaches level $j$, this capture comes after $t_c$, or after $c$ died by a REJ or a YES; in both cases $c$ had already reached level $j$, so $\mathrm{pair}(c) \ge (j, \cdot)$ at that moment.
- Otherwise $y$ was captured by $c$, and the ACC reached $c$ while $c$ was alive. The next owner after $c$ takes over by a query to $c$, which kills $c$ if alive (Lemma 1). If that happened before $t_c$, then $c$ would be dead at $t_c$ and could not raise its level in L6. So it happens after $t_c$, and $\mathrm{pair}(c) \ge (j, \cdot)$ then.

In both cases, the first capture of $y$ after $c$ has a request pair larger than a pair of level at least $j$, so its level is at least $j$. By Lemma 1 the later request pairs on $y$ are larger still, so they have level at least $j$ too.

Now suppose $y \in S_c \cap S_d$. If $y$ is the own process of both, then $c = d$. Otherwise one of them, say $d$, captured $y$ with a request of level at most $j - 1$, after the other one owned $y$ (either as its own process, which it owns from the start, or by a capture that raised its level earlier in time; captures of $y$ happen one after another, because $y$ handles one CAP at a time and L2 and L5 are the only places where the owner changes). By the first part of the proof, applied to $c$, this request has level at least $j$, a contradiction. $\square$

**Part (c).** By Lemma 2, the candidates that reach level $j$ have disjoint sets $S_c$ of $j + 1$ processes each, so there are at most $n / (j + 1)$ of them.

**Part (d).** A candidate that ends at level $L_c$ sends one CAP at each level $0, \ldots, L_c$ and none after it is elected, so at most $L_c + 1$ CAPs. Therefore the number of CAPs is at most $\sum_c (L_c + 1) = \sum_{j \ge 0} \#\{c : L_c \ge j\} \le \sum_{j=0}^{n-1} n / (j + 1) = n H_n$, using part (c) and $L_c \le n - 1$. Each CAP causes at most one Q, one answer to it and one ACC or REJ (F3), and no other messages are sent. So the run sends at most $4 n H_n$ messages.

**Part (a), termination.** By part (d) the number of messages is finite, and a process acts only when it starts or receives a message. So every run is finite.

**Part (b), at most one leader.** Suppose $c$ and $d$ are both elected, and $c$ is elected first, at time $t$. Both captured every other process. Consider the capture of $c$'s own process by $d$: it is a capture of $y = c$ by a request of $d$, with a level at most $n - 2$. If it happens before $t$, then by F5 and Lemma 1 it kills $c$ or finds $c$ already dead, and a dead candidate is not elected in L6. If it happens after $t$, the first capture of $c$'s process after $t$ must beat $\mathrm{pair}(c) = (n - 1, \cdot)$, which no request of level at most $n - 2$ does, and by Lemma 1 every later capture must beat that one. So $d$ cannot capture $c$'s process, a contradiction.

**Part (b), some leader.** Let $c^*$ be the candidate with the largest final pair; pairs are distinct because identifiers are. Suppose $c^*$ dies. It dies in L2 or L4, when a request pair beats $\mathrm{pair}(c^*)$, and the requester's final pair is at least that request pair (F1), larger than $c^*$'s final pair, a contradiction. Or it dies in L7, by a REJ: then its request $P$ lost against $\mathrm{pair}(y)$ in L2, or against the pair of an owner in L4, and that pair belongs to a candidate (a process that never was a candidate has level $-1 < 0$), whose final pair is larger than $P = $ the final pair of $c^*$, a contradiction. So $c^*$ stays alive. When the run ends, no message is in transit and no process is busy, since every query is answered in L4 at once and every answer ends a busy period. So every CAP of $c^*$ was answered with ACC, and $c^*$ sent a new one until its level reached $n - 1$ (F4). So $c^*$ is elected, and it is the only leader.

**Part (e).** With unit delays, a message sent at time $t$ arrives at time $t + 1$, and a process sends only at time 0 or when a message arrives. If no message arrives at some time $t \ge 1$, no message is sent at time $t$, so none is in transit after $t$ and the run has ended. So at least one message arrives at each time $1, 2, \ldots, T$, where $T$ is the end of the run, and $T$ is at most the number of messages. $\blacksquare$
