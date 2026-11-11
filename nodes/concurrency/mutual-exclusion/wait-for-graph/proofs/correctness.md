---
title: The incremental cycle check is exact, cycles are deadlocks, and probes find exactly the cycles
proves: [correctness]
status: full
---

**Model.** $G = (V, E)$ is the wait-for graph. An edge $p \to q$ means that $p$ is blocked on a request that cannot be granted until $q$ releases something. Requests are AND requests: a blocked process proceeds only when all its outgoing edges are gone. A blocked process takes no step, and in particular it releases nothing. A process with no outgoing edge is not blocked.

**Theorem 1 (the check of ADD-WAIT).** Let $G$ have no cycle, and let $p \neq q$. Then $G' = G + (p \to q)$ has a cycle if and only if $G$ has a path from $q$ to $p$. If $q = v_0, v_1, \ldots, v_r = p$ is such a path, then $p, v_0, \ldots, v_{r-1}$ is a cycle of $G'$.

*Proof.* If $G$ has a path $v_0, \ldots, v_r$ from $q$ to $p$, then every edge $v_{s-1} \to v_s$ is in $G'$, and so is $p \to q = p \to v_0$; so $p, v_0, \ldots, v_{r-1}$ is a closed walk in $G'$. Its vertices are distinct, because a path found by search has distinct vertices and $p = v_r$ is not among $v_0, \ldots, v_{r-1}$. So it is a cycle. Conversely, let $C$ be a cycle of $G'$. Since $G$ has none, $C$ uses the edge $p \to q$, and the rest of $C$ is a path from $q$ to $p$ that uses only edges of $G$ (a cycle uses each edge once). $\square$

Line L3 finds a path from $q$ to $p$ by depth-first search if one exists, so lines L3 to L5 return a cycle exactly when $G'$ has one.

**Theorem 2 (a cycle means deadlock).** In every state reachable from the current one, every edge of every cycle is still present, as long as no process of the cycle is aborted. Hence every process that reaches a cycle is deadlocked.

*Proof.* Let $C = (c_0, \ldots, c_{r-1})$ be a cycle. Each $c_s$ has an outgoing edge, so it is blocked. An edge $c_s \to c_{s+1}$ can leave the graph only when $c_{s+1}$ releases something or $c_s$ withdraws its request, and both need a step of a process of $C$. Consider the first step, in any run, that removes an edge of $C$. Before that step every process of $C$ is blocked and takes no step, so that step cannot exist. Hence the edges of $C$ stay, and the processes of $C$ stay blocked forever.

Now let $p$ reach $C$ by a path $p = u_0 \to u_1 \to \cdots \to u_t = c_0$. By induction on $t - s$, the process $u_s$ stays blocked forever: $u_t$ does by the first part, and if $u_{s+1}$ stays blocked forever, it never takes a step, so the edge $u_s \to u_{s+1}$ is never removed, and $u_s$, which needs all its edges gone, stays blocked. $\square$

**Theorem 3 (deadlock means reaching a cycle).** Let every resource have one unit and let every request be for a single resource. Let a process be deadlocked when it is blocked in every reachable state. If $p$ reaches no cycle of $G$, then $p$ is not deadlocked.

*Proof.* Put the state in the form of the [deadlock detection](/deadlock-detection/) page: $\mathit{alloc}[i][r] = 1$ when $i$ holds $r$, and $\mathit{req}[i][r] = 1$ when $i$ waits for $r$. A blocked process waits for one held resource, and its edges go to the holders, which with one unit means the single holder. Theorem 2 of the proof file of that page states that the deadlocked processes are exactly those that no complete reduction removes, and its corollary on single units states that, in this case, a complete reduction removes exactly the vertices that reach no cycle of the wait-for graph. So $p$ is removed and is not deadlocked. $\square$

Theorems 2 and 3 together say: with single unit resources, the deadlocked processes are exactly the processes that reach a cycle. The peeling procedure of the page, which repeatedly deletes vertices with no outgoing edge, deletes exactly the vertices that reach no cycle: a vertex on a cycle always keeps the outgoing edge of the cycle, a vertex that reaches a cycle keeps the first edge of a path to it, and a vertex that reaches no cycle has only finite paths, so by induction on the length of its longest path, all its successors are deleted before it.

**Theorem 4 (the probe method on a fixed graph).** Let $G$ not change while the probes travel, and let the initiator $i$ be blocked. Messages are delivered in any order and none is lost. Then $i$ receives a probe $(i, j, i)$ if and only if $i$ is on a cycle of $G$. At most one probe is sent along each edge, so at most $e$ probes in all.

*Proof.* Say that a process *forwards* when it sends probes of initiator $i$ to all its successors. The initiator forwards once, at the start. Any other process $k$ forwards at most once, when it first gets a probe of $i$, and only if it is blocked. A probe is sent along an edge $k \to l$ only when $k$ forwards. Since each process forwards at most once, each edge carries at most one probe.

Claim: a process $k \neq i$ forwards if and only if $k$ is reachable from $i$ by a path of length at least one whose vertices other than $i$ are all different from $i$. Every probe travels along an edge from a forwarding process, and the initiator forwards, so by induction on the time of sending, every process that gets a probe is reachable from $i$ in this way. Conversely, let $i = u_0 \to u_1 \to \cdots \to u_t = k$ with $u_s \neq i$ for $s \ge 1$. By induction on $s$: $u_0$ forwards, so $u_1$ gets a probe. If $u_s$ with $1 \le s < t$ gets a probe, then it has the outgoing edge $u_s \to u_{s+1}$, so it is blocked; it forwards on this probe or on an earlier one, and $u_{s+1}$ gets a probe. Since no message is lost, $u_t = k$ gets a probe, and $k$ forwards if it is blocked. (A process with no outgoing edge gets the probe and discards it, which changes nothing in the claim about who receives.)

Now $i$ gets a probe $(i, j, i)$ if and only if some process $j$ that forwards, or $i$ itself, has the edge $j \to i$. By the claim this holds if and only if there is a path from $i$ back to $i$ of length at least one, that is, if and only if $i$ is on a cycle. $\square$

The fixed graph in Theorem 4 is not a strong assumption when the initiator is on a cycle: by Theorem 2, the edges of a cycle never leave while its processes are blocked, so the probes along the cycle travel on edges that are present all the time. Other edges may change, but the cycle alone already brings the probe back. The other direction, that a declared deadlock is real when edges come and go during the run, is proved by Chandy, Misra and Haas (1983) for their model; it is not proved here.

$\blacksquare$
