---
title: Dijkstra-Scholten announces termination if and only if the diffusing computation has terminated, with one signal per basic message
proves: [correctness, termination, complexity]
status: full
---

**Setting.** A diffusing computation runs on a network with reliable channels (not necessarily FIFO), no failures and arbitrary finite delays. At the start the root $r$ is active and every other node is passive. An active node may send basic messages and may become passive at any time; a passive node sends no basic message and becomes active only on receipt of a basic message. The computation has *terminated* when every node is passive and no basic message is in transit. This property is stable: once it holds, no node can become active again, since no basic message exists to activate it.

DIJKSTRA-SCHOLTEN runs lines L1 to L11 alongside. Write $\delta(v)$ for the deficit of $v$. Call a basic message sent by $v$ *open* while its SIGNAL has not yet arrived at $v$. The *children* of $v$ are the engaged nodes $w \ne r$ with $\mathit{parent}(w) = v$, and the *engaging message* of such a $w$ is the basic message whose receipt ran line L5 at $w$.

**Claim.** (1) Every basic message is answered by exactly one SIGNAL to its sender. (2) If $r$ announces at some time, the computation has terminated at that time. (3) If the computation terminates, $r$ announces after finitely many further steps. (4) The algorithm sends exactly as many SIGNAL messages as basic messages, and $r$ announces exactly one time.

## The invariant

At every moment, for every node $v$:

- **(a)** $\delta(v)$ is the number of open messages of $v$, and each open message of $v$ is in exactly one of three states: in transit; arrived and answered by a SIGNAL that is in transit to $v$; or the engaging message of a current child of $v$.
- **(b)** If $v$ is active or $\delta(v) > 0$, then $v$ is engaged.
- **(c)** The engaged nodes with their parent pointers form a tree rooted at $r$.

*Proof of (a).* Line L2 adds 1 to $\delta(v)$ when $v$ sends a basic message $x$ to $w$, and $x$ is open and in transit. On arrival, either $w$ is engaged and sends a SIGNAL at once (line L6), so $x$ is answered by a SIGNAL in transit; or $w$ is not engaged and $x$ engages it (line L5), so $w$ becomes a child of $v$ with $x$ as its engaging message. A child stops being a child only at line L11, where it sends to $v$ the SIGNAL for its engaging message. A SIGNAL subtracts 1 from $\delta(v)$ on arrival (line L7) and closes the message it answers. No other line changes $\delta$ or sends a SIGNAL. This also gives (1): each basic message is answered at line L6 or at line L11, never both and never twice, and every SIGNAL answers one basic message.

*Proof of (b).* At the start only $r$ is active, and $r$ is engaged. A node becomes active only at line L4, and after lines L5 or L6 it is engaged. $\delta(v)$ grows only at line L2, which only an active node runs. A node becomes disengaged only at line L11, which line L9 allows only when the node is passive and $\delta(v) = 0$.

*Proof of (c).* At the start the tree is $\{r\}$. A node $w$ joins at line L5 with the parent $u$ that sent the engaging message; $u$ was active when it sent, so it was engaged by (b), and from then on the engaging message is open, so $\delta(u) > 0$ and $u$ stays engaged while $w$ is its child. A node leaves only at line L11, with $\delta = 0$, so by (a) it has no children then: the tree loses only leaves. So every engaged node has a parent that is engaged and joined earlier, the parent pointers lead to $r$ without a cycle, and $r$ never leaves, since at $r$ line L10 replaces line L11.

## Safety

Suppose $r$ announces at time $t$. By line L9, at $t$ the root is passive and $\delta(r) = 0$, so by (a) $r$ has no children and no basic message of $r$ is in transit. By (c), every engaged node $w \ne r$ has a path of parent pointers to $r$ whose last node before $r$ is a child of $r$; there is none, so $r$ is the only engaged node. By (b), every other node is passive and has $\delta = 0$, so by (a) no basic message of any node is in transit. Hence at $t$ every node is passive and no basic message is in transit: the computation has terminated. This proves (2).

## Liveness

Suppose the computation has terminated at time $t_0$. After $t_0$ no basic message is sent or received and every node stays passive; the only messages are SIGNALs, which arrive after finite delays. By (a), the deficit of an engaged node is then the number of its children plus the number of SIGNALs in transit to it.

At a node $w$, the last event that changes its state is line L7 (a SIGNAL arrives) or line L8 (it becomes passive): line L4 makes $w$ active, so a line L8 follows it. Both lines run TRY-LEAVE in the state they leave behind.

We show by induction on the number of engaged nodes that eventually $r$ alone is engaged with $\delta(r) = 0$. Let $w \ne r$ be a leaf of the tree. It has no children, so $\delta(w)$ is the number of SIGNALs in transit to it. If that number is 0, then the last event at $w$ ran TRY-LEAVE with $w$ passive, engaged and $\delta(w) = 0$, so $w$ would have left; hence at least one SIGNAL is in transit, and on the arrival of the last one, line L7 brings $\delta(w)$ to 0 and TRY-LEAVE makes $w$ leave at line L11. So after finite time the tree has one node fewer. When $r$ alone is engaged, $\delta(r)$ is the number of SIGNALs in transit to $r$, and by the same argument the arrival of the last one, or line L8 if there is none, runs TRY-LEAVE with $\delta(r) = 0$ and $r$ passive, and $r$ announces at line L10. This proves (3).

## Counting

By (1), the SIGNALs and the basic messages are in one to one correspondence, so the run sends exactly $B$ SIGNALs for $B$ basic messages. At the announcement $\delta(v) = 0$ for every node $v$ (Safety), so by (a) no message of either kind is in transit, every node is passive, and no further event can happen; in particular $r$ announces only once. This proves (4). ∎
