---
title: Edge chasing declares only processes on a wait cycle, and finds every cycle
proves: [correctness, messages]
status: full
---

We use the line numbers of the pseudocode on the page, the rule of line L7 with the extension (declare when $P_i \in \mathrm{LD}^*(P_k)$), and numbered computations. The model is the resource model of the page, as in the code.

**The model.** Each site has a controller. A transaction $t$ has a home process $(t, h)$ and at most one agent $(t, m)$ at each other site $m$. The home process asks for one resource at a time. Channels are first in, first out, and messages are not lost. No transaction aborts while a probe computation runs; this is the assumption of Section 3 of Chandy, Misra and Haas (1983), and the page discusses what happens without it. The *true wait-for graph* $W$ at a moment has a node for each idle process and these edges between idle processes:

- $(u, s) \to (v, s)$ if $(u, s)$ waits at $s$ for a resource that $v$ holds at $s$ (a local edge);
- $(t, h) \to (t, m)$ if the home process has a request to $m$ that is not yet answered (a remote edge);
- $(t, m) \to (t, h)$ if the agent holds resources at $m$, waits for none, and no request from the home to $m$ is in transit or waiting (a remote edge).

A process is idle when it has an out-edge in this sense: a waiting agent, a home process with an open request, or an agent that holds resources and has nothing to do. $P_i$ *depends on* $P_k$ if $W$ has a path from $P_i$ to $P_k$. $\mathrm{LD}^*(P_k)$ is the set of processes that $P_k$ reaches by local edges, with $P_k$. The controller of $P_k$ computes it from its own lock table.

**Lemma 1 (stability).** If $p \to q$ is an edge of $W$, the edge stays in $W$ while $q$ stays idle. So a path $p_0 \to \dots \to p_r$ of $W$ stays in $W$ while $p_r$ stays idle, and a cycle of $W$ stays forever.

*Proof.* Look at what removes each kind of edge. A local edge $(u, s) \to (v, s)$ goes away only when $v$ releases the resource at $s$, which happens when the home of $v$ commits or when the agent $(v, s)$ gets the release from its home; in both cases $(v, s)$ stops being idle in that step. An edge $(t, h) \to (t, m)$ goes away when the reply of the agent arrives, and the agent sent it when it got the resource, so it stopped waiting before. An edge $(t, m) \to (t, h)$ goes away when the home sends a release, a new request or an abort to $m$, and the home is executing when it does this. So the target of an edge always leaves the idle state first. The path claim follows by induction from the end of the path: $p_{r-1} \to p_r$ stays while $p_r$ is idle, so $p_{r-1}$ stays idle, and so on. On a cycle every node is the target of an edge, so no node can be the first to leave. $\square$

**Lemma 2 (a probe carries a true dependency).** Let the controller of $a$ send probe$(i, m, a, b)$ at time $\tau$, at a moment when $P_i$ depends on $a$ or equals $a$, and $a$ is idle. If the controller of $b$ accepts it at time $\tau'$ (line L5), then at $\tau'$ the edge $a \to b$ is in $W$, $a$ has been idle since $\tau$, and $P_i$ depends on $b$.

*Proof.* There are two cases for the edge that the controller of $a$ saw.

*From a home to an agent.* At $\tau$ the home $a$ has an open request to the site of $b$. The probe goes on the same channel as the request and after it. Line L5 accepts only if $b$ waits at its controller. That wait is for this request: a later request needs a reply first, the reply needs the grant, and a later request would be behind the probe on the channel. So the request was open during the whole interval $[\tau, \tau']$, $a$ was idle, and at $\tau'$ the edge $a \to b$ is in $W$.

*From an agent to its home.* At $\tau$ the agent $a$ holds resources and waits for none. Line L5 accepts only if the home $b$ is idle and has no open request to the site of $a$. Suppose the home sent a request to that site at some time before $\tau'$ and after the last reply of $a$. If the request is still open at $\tau'$, the probe is dropped. If it was answered, the answer came after the request reached $a$; if the request reached $a$ after $\tau$, the answer is behind the probe on the channel and cannot have arrived; if it reached $a$ before $\tau$, then $a$ was not free at $\tau$, a contradiction. So no request went from $b$ to $a$ in $[\tau, \tau']$, $b$ did not commit or abort (it is idle), and $a$ held its resources and waited for $b$ during the whole interval. At $\tau'$ the edge $a \to b$ is in $W$.

In both cases $a$ stayed idle from $\tau$ to $\tau'$. By Lemma 1, the path from $P_i$ to $a$ that existed at $\tau$ is still in $W$ at $\tau'$. With the edge $a \to b$, $P_i$ depends on $b$. $\square$

**Lemma 3 (the flags).** At all times, if the controller of $P_k$ holds dependent$_k(i) = m$, then $P_k$ is idle and $P_i$ depends on $P_k$.

*Proof.* The flag is set only at line L6, where $P_k$ is idle and, by Lemma 2, $P_i$ depends on $P_k$. While $P_k$ stays idle the path stays, by Lemma 1. When $P_k$ leaves the idle state, line L10 clears all its flags. For the probes that $P_k$ forwards at line L9: they start at some $a \in \mathrm{LD}^*(P_k)$, so $P_i$ depends on $a$, and $a$ is idle; this is the premise of Lemma 2 for the next step. The probes of line L4 satisfy it because $a \in \mathrm{LD}^*(P_i)$. $\square$

**Theorem 1 (no false deadlocks).** If a process $P_i$ is declared deadlocked, then at that moment $P_i$ is on a cycle of $W$. With no aborts, it then stays deadlocked forever.

*Proof.* At line L1 the controller sees a cycle of local edges through $P_i$. At line L7, the flag dependent$_k(i)$ was just set, so $P_i$ depends on $P_k$ by Lemma 3, and $P_i \in \mathrm{LD}^*(P_k)$ gives a path back from $P_k$ to $P_i$. The literal rule $k = i$ is the special case $P_k = P_i$. The cycle stays by Lemma 1. $\blacksquare$

**Theorem 2 (every cycle is found).** If a computation for $P_i$ starts (line L2) while $P_i$ is on a cycle of $W$, then $P_i$ is declared deadlocked, by this computation or by a later computation for $P_i$.

*Proof.* If the cycle has no remote edge, line L1 declares $P_i$. Otherwise write the cycle as $P_i \leadsto a_1 \to b_1 \leadsto a_2 \to b_2 \leadsto \dots \leadsto a_r \to b_r \leadsto P_i$, where each $a_j \to b_j$ is a remote edge and each $\leadsto$ is a path of local edges. The cycle stays forever by Lemma 1, so each $a_j$ is in $\mathrm{LD}^*(b_{j-1})$ (with $b_0 = P_i$) at all later times, and each controller sees the edge $a_j \to b_j$.

We show by induction on $j$ that the flag dependent$_{b_j}(i)$ is set to $m$ or to a larger number at some time, and that at the moment it is set to some number $m' \geq m$, the controller of $b_j$ checks line L7 and, if it does not declare, sends probe$(i, m', a_{j+1}, b_{j+1})$. For $j = 0$ this is line L3. For the step, the probe$(i, m', a_j, b_j)$ arrives at $b_j$. The process $b_j$ is idle forever, and the remote edge stays, so the condition on replies in line L5 holds. If the flag of $b_j$ is less than $m'$, the probe is accepted. If it is already at least $m'$, it was set by a probe of a computation numbered at least $m'$, and the claim holds for that number. Flags of $b_j$ are never cleared, because $b_j$ never leaves the idle state.

For $j = r$: when the flag of $b_r$ is set, $P_i \in \mathrm{LD}^*(b_r)$, so line L7 declares $P_i$. $\blacksquare$

With the literal rule $k = i$, the last step needs $b_r = P_i$, that is, the edge of the cycle that enters $P_i$ must be a remote edge. If it is a local edge, the probes go round the cycle and are dropped at $b_1$, whose flag is already set; the test file has such a case with two sites. A computation for $b_j$, the end of any remote edge on the cycle, still finds the cycle with the literal rule. So if the system starts a computation for every idle process, as the code does when no message is in transit, both rules find every cycle.

**Without numbers.** If the flag is a Boolean, as in the paper, Theorem 2 needs the flag of $b_j$ to be false when the computation starts. A computation for $P_i$ that ran before the cycle closed can leave a flag at a process that stays idle, and this flag stops every later probe for $P_i$ at that process. The test file has such a case with three sites. The numbers of line L2 remove the problem, and they do not change Lemma 3.

**Theorem 3 (messages).** Suppose that the wait-for graph does not change while a computation runs, and let $e$ be the number of remote edges that start at idle processes. Then the computation sends at most $e(e + 1)$ probes, and each probe has four fields.

*Proof.* A probe is accepted at its target, the end of a remote edge, and a target accepts a computation at most once, because its flag keeps the number and is not cleared. So at most $e$ processes accept, and each of them, and the initiator, sends at most one probe for each remote edge that starts in its set $\mathrm{LD}^*$, at most $e$ probes. $\blacksquare$
