---
title: Active replication answers each command as one copy of the state machine would
proves: [correctness]
status: full
---

**Statement.** Assume a total-order broadcast with these properties: (validity) a command broadcast by a correct client is delivered by every correct replica; (agreement) a command delivered by one correct replica is delivered by every correct replica; (integrity) each command is delivered at most once, and only if a client broadcast it; (total order) all replicas see the delivered commands with the same numbers $1, 2, 3, \ldots$, each number used once. Assume a deterministic state machine $(s_0, \delta, \omega)$. Let $c_k$ be the command with number $k$, let $s_k = \delta^*(s_0, c_1 \cdots c_k)$ and $o_k = \omega(s_{k-1}, c_k)$. Then:

- (a) A replica that has run line L4 exactly $k$ times is in state $s_k$, and for each $j \le k$ the output it sent at line L5 for number $j$ is $o_j$ (the Byzantine replicas excepted).
- (b) With crash faults only and at least one correct replica, each command $c_k$ of a correct client gets the reply $o_k$, and every reply it gets is $o_k$.
- (c) With at most $f$ Byzantine replicas among $n \ge 2f + 1$, each command $c_k$ of a correct client gets $f + 1$ equal replies $o_k$, and no other value gets $f + 1$ replies.

**Setup.** Fix a replica that follows the algorithm. Let $E_k$ be the $k$-th run of line L4 at this replica.

**Lemma 1 (in-order execution).** $E_k$ applies the command $c_k$, for every $k$ for which $E_k$ happens.

*Proof.* We show by induction on $k$ that before $E_k$ the counter $next$ equals $k$ and that $E_k$ removes the entry with number $k$. At the start, $next = 1$ and no line L4 has run. Line L4 runs only inside the loop of line L2, whose test is that the buffer holds the number $next$, and line L3 removes exactly that entry. So $E_k$ applies the entry with number $next$. Line L6 adds 1 to $next$ after each run of line L4, and no other line changes $next$. So before $E_1$, $next = 1$; and if $next = k$ before $E_k$, then $next = k + 1$ before $E_{k+1}$. By total order the entry with number $k$ holds $c_k$, and by integrity no other entry has the number $k$. $\square$

**Proof of (a).** By induction on $k$. Before $E_1$ the state is $s_0$. Assume the state is $s_{k-1}$ before $E_k$. By Lemma 1, $E_k$ applies $c_k$, so line L4 sets the state to $\delta(s_{k-1}, c_k) = s_k$ and the output to $\omega(s_{k-1}, c_k) = o_k$. The machine is deterministic, so these values depend only on $s_{k-1}$ and $c_k$, not on the replica, the time or the order in which messages arrived. Line L5 sends the output $o_k$ with the number $k$. $\square$

**Proof of (b).** Let $c$ be a command of a correct client, broadcast at line L7. By validity, every correct replica delivers $c$, say with number $k$. Before line L4 can run for $c_k$, the replica must hold $c_1, \ldots, c_{k-1}$ (Lemma 1). Each $c_j$ with $j < k$ was delivered at some correct replica, since its number is in the total order, so by agreement each correct replica delivers it. So each correct replica runs $E_1, \ldots, E_k$ and, by (a), sends $o_k$ to the client. Links between correct processes are reliable, so the reply arrives. With crash faults, a replica that crashes sends nothing after its crash, and before its crash it follows the algorithm, so by (a) any reply it sent is also $o_k$. So the first reply the client gets for number $k$ is $o_k$, and line L9 returns $o_k$. $\square$

**Proof of (c).** At least $n - f \ge f + 1$ replicas are correct. As in (b), each of them sends $o_k$, so $o_k$ gets at least $f + 1$ votes. A value $o \ne o_k$ can come only from Byzantine replicas, because correct replicas send $o_k$ by (a). The client counts at most one vote from each replica for each number (the simulator sends one reply from each replica; a real client keys the votes by the sender), so $o$ gets at most $f$ votes. Line L9 therefore returns $o_k$, and never another value. $\square$

**Why the counts are tight for the vote.** With crash faults and $n = f$, all replicas can crash and no reply comes, so $f + 1$ is needed. With Byzantine faults and $n = 2f$, let $f$ replicas be correct and $f$ lie with one common wrong value $o$. Both $o_k$ and $o$ get $f$ votes, and the client cannot tell them apart, since the run is the same with the roles of the two groups swapped. So $2f + 1$ is needed for the vote. $\blacksquare$
