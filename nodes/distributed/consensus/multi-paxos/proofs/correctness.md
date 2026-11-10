---
title: Multi-Paxos chooses at most one value per slot
proves: [correctness]
status: full
---

The model is asynchronous, with crash failures and messages that can be lost, duplicated and reordered. A value $v$ is *chosen in slot $s$ in ballot $b$* when a majority of acceptors have run line L12 with ballot $b$, slot $s$ and value $v$. We reduce each slot to single-decree [Paxos](/paxos/) and reuse its proof.

**Lemma 1 (one value per ballot and slot).** For each ballot $b$ and slot $s$, at most one value appears in a message ACCEPT($b$, $s$, $v$).

*Proof.* Only the leader named in $b$ sends ACCEPT messages with ballot $b$, and it uses $b$ in one attempt only, because line L1 makes a fresh ballot each time. In that attempt, line L5 runs once, when *active* is false, and sends one value for each slot $s <$ top. Line L6 sets *next* to top and *active* to true, so lines L3 to L6 do not run again for $b$. Line L7 gives each command the current *next* and then increases it, so lines L7 and L8 use each slot $s \ge$ top at most once. So the slots of line L5 and of line L8 are disjoint, and each is used once. $\square$

**Lemma 2 (promises cover all slots).** If acceptor $a$ sends PROMISE($b$, accepted$_a$), then after that time $a$ never votes (line L12) in any slot with a ballot smaller than $b$. The map accepted$_a$ gives, for each slot $s$, the vote of $a$ in slot $s$ with the largest ballot so far, and that ballot is smaller than $b$.

*Proof.* *promised* is one value for all slots. Lines L10 and L12 never lower it, and line L11 lets a vote through only if its ballot is at least *promised*. So after line L10 sets it to $b$, no vote with a smaller ballot happens in any slot. Line L12 writes accepted$[s]$ only with the ballot of the vote, and the ballots of votes of $a$ never decrease, by the same argument, so accepted$[s]$ is the vote with the largest ballot in slot $s$. Line L9 requires $b >$ promised, and promised is at least each ballot in accepted, so each reported ballot is smaller than $b$. $\square$

**Lemma 3 (P2c per slot).** If ACCEPT($b$, $s$, $v$) is sent, then there is a majority $Q$ such that either (a) no acceptor of $Q$ ever votes in slot $s$ with a ballot smaller than $b$, or (b) $v$ is the value of the vote with the largest ballot smaller than $b$ in slot $s$ among the acceptors of $Q$.

*Proof.* Let $Q$ be the majority whose promises the leader used in line L3. By Lemma 2, the votes of an acceptor of $Q$ in slot $s$ with ballots below $b$ are exactly its votes in slot $s$ before its promise, and the promise reports the largest of them.

If ACCEPT($b$, $s$, $v$) was sent by line L5 and slot $s$ has a report, line L4 takes the value with the largest reported ballot in slot $s$. By Lemma 1 all votes in that ballot and slot have the same value. This is case (b). If slot $s$ has no report, no acceptor of $Q$ ever votes in slot $s$ below $b$, which is case (a), and the no-op of line L5 is allowed.

If it was sent by line L8, then $s \ge$ top, and top is larger than every slot that $Q$ reported. So slot $s$ has no report from $Q$, which is case (a). $\square$

**Theorem (agreement per slot).** If $v$ is chosen in slot $s$ in ballot $b_0$, and $w$ is chosen in slot $s$ in ballot $b_1$, then $v = w$.

*Proof.* Fix the slot $s$. Lemmas 1 and 3 are the two facts that the agreement proof of single-decree Paxos uses: one value per ballot, and the invariant P2c. That proof is a strong induction on the ballot. It shows that each ACCEPT($b$, $s$, $w$) with $b > b_0$ has $w = v$, because the majority $Q$ of Lemma 3 shares an acceptor with the majority that chose $v$ in $b_0$. The same steps apply here word for word, with all votes and messages restricted to slot $s$. Then $v = w$ follows as in Paxos. $\square$

**Theorem (validity).** Each chosen value is a submitted command or no-op.

*Proof.* Line L8 sends a submitted command, and line L5 sends no-op or a reported value. A reported value is the value of an earlier vote, so of an earlier ACCEPT message. Strong induction on the ballot gives the claim. $\square$

**Theorem (the logs agree).** If learner $i$ has applied the sequence $x_0, \ldots, x_{k-1}$ and learner $j$ has applied $y_0, \ldots, y_{m-1}$ with $k \le m$, then $x_t = y_t$ for each $t < k$.

*Proof.* Line L13 sets learned$[s] \leftarrow v$ only when a majority of acceptors sent ACCEPTED($b$, $s$, $v$) for one ballot $b$, which they do only when they vote for $v$ in slot $s$ in $b$. So $v$ is chosen in slot $s$. Line L14 applies learned$[t]$ as the $t$-th command, for $t = 0, 1, \ldots$ in order. So $x_t$ and $y_t$ are both chosen in slot $t$, and by the agreement theorem they are equal. $\blacksquare$
