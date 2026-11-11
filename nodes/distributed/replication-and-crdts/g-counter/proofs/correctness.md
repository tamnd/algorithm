---
title: A g-counter returns the number of increments in its causal history and converges
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas with ids $1, \ldots, n$. Replica $i$ runs the main block with its state $P_i$. A *run* is a sequence of steps. In one step a replica either runs INCREMENT (line L3), or sends a copy of its current state, or runs MERGE (lines L5 and L6) on a copy that some replica sent earlier. Copies may be lost, merged more than once, and merged in any order. Crashes with recovery of the durable state do not change $P_i$, so they need no separate case.

**Causal histories.** Name the $k$-th increment at replica $j$ as the pair $(j, k)$. Define the causal history $C_i$ of replica $i$ along the run: at the start $C_i = \varnothing$; an INCREMENT at $i$ that is the $k$-th one at $i$ adds $(i, k)$; a MERGE at $i$ of a copy sent by $j$ when $j$ had history $H$ sets $C_i \leftarrow C_i \cup H$. A copy carries the history of its sender at the time of sending. For a set $H$ of increments and a replica $j$, write $H_j = \{k : (j, k) \in H\}$.

**Claim 1 (prefix property).** At every time, for every pair of replicas $i, j$, the set $(C_i)_j$ is $\{1, 2, \ldots, m\}$ for some $m \ge 0$. Moreover $(C_i)_i$ is the set of all increments made at $i$ so far.

*Proof.* By induction on the steps. At the start all sets are empty. A step at a replica other than $i$ does not change $C_i$. An INCREMENT at $i$ that is the $k$-th one at $i$ adds $(i, k)$. By induction $(C_i)_i = \{1, \ldots, k - 1\}$, so it becomes $\{1, \ldots, k\}$, which is again a prefix and is again the set of all increments at $i$. It adds nothing for $j \ne i$. A MERGE at $i$ of a copy with history $H$ replaces $(C_i)_j$ by $(C_i)_j \cup H_j$. $H$ was the history of some replica at an earlier time, so $H_j$ is a prefix by induction. The union of two prefixes $\{1, \ldots, a\}$ and $\{1, \ldots, b\}$ is the prefix $\{1, \ldots, \max(a, b)\}$. For $j = i$, $H_i$ contains only increments of $i$ made before the copy was sent, so $H_i \subseteq (C_i)_i$, and $(C_i)_i$ does not change. $\square$

**Claim 2 (main invariant).** At every time, for every $i$ and $j$, $P_i[j] = |(C_i)_j|$. A copy of a state carries a vector $Q$ and a history $H$ with $Q[j] = |H_j|$ for every $j$.

*Proof.* By induction on the steps. At the start both sides are 0. A copy is the state and history of its sender at the time of sending, so the second part follows from the first part at that time. INCREMENT at $i$: line L3 adds 1 to $P_i[i]$, and the history gains exactly one element, $(i, k)$, in the set for $i$; no other entry or set changes. MERGE at $i$ of a copy $(Q, H)$: line L6 sets $P_i[j]$ to $\max(P_i[j], Q[j])$. By induction and Claim 1, $P_i[j] = a$ and $Q[j] = b$ where $(C_i)_j = \{1, \ldots, a\}$ and $H_j = \{1, \ldots, b\}$, and the new set is $\{1, \ldots, \max(a, b)\}$, of size $\max(a, b)$. So the invariant holds for each $j$ after the loop of line L5. $\square$

**Theorem (safety).** At every time, VALUE at replica $i$ returns $|C_i|$, the number of increments in its causal history. Hence it returns at most the number of increments made so far in the whole system, the value at a replica never decreases, and two replicas with the same causal history have the same state.

*Proof.* Line L4 returns $\sum_j P_i[j] = \sum_j |(C_i)_j| = |C_i|$ by Claim 2, since the sets $(C_i)_j$ for different $j$ partition $C_i$. Every element of $C_i$ is an increment that was made, so $|C_i|$ is at most the total. $C_i$ only grows: INCREMENT adds an element and MERGE takes a union. Finally, $P_i$ is determined by $C_i$ through Claim 2, so equal histories give equal states. $\square$

**Theorem (convergence).** Suppose that after some time no replica increments, and that for every pair $i, j$, replica $i$ sends its state to $j$ infinitely often over a fair-lossy channel. Then there is a time after which every replica has $P_i[j] = $ the number of increments at $j$ for all $j$, and VALUE returns the total number of increments at every replica.

*Proof.* Let $I$ be the finite set of all increments of the run, and let $T$ be a time after the last increment. Fix $i$ and $j$. Replica $j$ sends its state to $i$ infinitely often after $T$, so by fairness one of these copies is merged at $i$, and from then on $(C_i)_j \supseteq (C_j)_j$, which by Claim 1 is the set of all increments at $j$. Histories never shrink. Taking the latest of these finitely many times over all pairs, every $C_i$ contains all increments of every replica, so $C_i = I$. By Claim 2, $P_i[j] = |I_j|$, the same vector at every replica, and VALUE returns $|I|$. $\square$

**Termination.** INCREMENT runs one step, and VALUE, MERGE and COMPARE run a loop of $n$ rounds with a constant number of steps each, so each operation ends.

**Where each assumption is used.** Claim 1 needs that only replica $i$ creates increments named $(i, k)$, which is the rule that a replica writes only its own entry, and that $(C_i)_i$ is never forgotten, which is the durable state. If a replica restarts from the zero vector under its old id, its next increment is named $(i, 1)$ again, Claim 1 fails, and the max in line L6 hides the new increments. The convergence theorem needs only that each pair exchanges states infinitely often; it does not need delivery in order, at most once, or exactly once. $\blacksquare$
