---
title: Random mate list ranking returns the exact rank of each node
proves: [correctness]
status: full
---

**Claim.** For any input $next$ that is a set of disjoint simple paths, and for any outcome of the coins, each run of RANDOM-MATE-RANK that ends returns $rank[i] = \mathrm{rank}(i)$ for each node $i$. (The complexity proof shows that the run ends with probability 1.)

**Notation.** We use the lines of RANDOM-MATE-RANK on the page. $\mathrm{rank}(i)$ is the true rank of $i$ in the input, the number of links from $i$ to the tail of its list, and $\mathrm{rank}(\mathit{nil}) = 0$. A node is *live* while it is in $L$ and *removed* after line L8 takes it out of $L$. Round $r$ is the $r$-th turn of the loop of line L4, $D_r$ is the set of line L6 in that round, and $R$ is the number of rounds.

**Invariant.** At the start of each round, and when the loop ends:

- (P) The live nodes, with the pointers $next$ and $prev$ restricted to them, form the input lists with the removed nodes left out and with the order kept. So for live $i$, $next[i]$ is the first live node after $i$ in its input list, or $\mathit{nil}$, and $prev$ is the inverse of $next$ on the live nodes.
- (W) Each node $i$, live or removed, has $\mathrm{rank}(i) = w[i] + \mathrm{rank}(next[i])$.
- (F) A removed node $i$ keeps the values $next[i]$ and $w[i]$ that it had when it was removed.

**Lemma 1 (no two removed nodes are adjacent).** If $i \in D_r$ and $j = next[i] \ne \mathit{nil}$, then $j \notin D_r$. If $i \in D_r$ and $h = prev[i] \ne \mathit{nil}$, then $h \notin D_r$.

*Proof.* If $i \in D_r$ and $j = next[i] \ne \mathit{nil}$, the rule of line L6 needs the coin of $j$ to be tails, and each node of $D_r$ has heads. So $j \notin D_r$. For the second claim, $next[h] = i$ by (P). If $h$ were in $D_r$, the first claim would give $i \notin D_r$, which is false. $\blacksquare$

**Lemma 2 (the splices of line L7 do not interfere).** In line L7 two distinct nodes of $D_r$ write to distinct cells, and no node of $D_r$ reads a cell that another node of $D_r$ writes. So the parallel step has the same effect as the splices done one at a time, in any order.

*Proof.* Node $i$ reads $w[i]$, $prev[i]$ and $next[i]$. It writes $w[h]$ and $next[h]$ for $h = prev[i]$, and $prev[j]$ for $j = next[i]$. By (P), distinct live nodes have distinct predecessors and distinct successors, so the cells written by two nodes of $D_r$ differ. By Lemma 1, $h$ and $j$ are not in $D_r$, so no node of $D_r$ reads a cell of $h$ or of $j$. $\blacksquare$

**Lemma 3 (the invariant holds).** (P), (W) and (F) hold at the start of each round and when the loop ends.

*Proof.* *Initialization.* No node is removed yet, and line L2 makes $prev$ the inverse of $next$, so (P) and (F) hold. Line L1 sets $w[i] = 1$ when $next[i] \ne \mathit{nil}$, and then $\mathrm{rank}(i) = 1 + \mathrm{rank}(next[i])$. It sets $w[i] = 0$ at a tail, and then $\mathrm{rank}(i) = 0 = 0 + \mathrm{rank}(\mathit{nil})$. So (W) holds.

*Maintenance.* Assume the invariant at the start of round $r$. By Lemma 2 we can do the splices of line L7 one at a time. Take one $i \in D_r$, with $h = prev[i]$ and $j = next[i]$. By Lemma 1 both are live and not in $D_r$. The splice sets $next[h] = j$ and $prev[j] = h$. This takes $i$ out of its live list and keeps the order of the others, so (P) holds for the live set without $i$, which line L8 then makes the new $L$. By (W) before the splice, $\mathrm{rank}(h) = w[h] + \mathrm{rank}(i) = w[h] + w[i] + \mathrm{rank}(j)$. The splice makes $w[h]$ equal to the old $w[h] + w[i]$ and $next[h] = j$, so (W) holds for $h$. When $h = \mathit{nil}$ or $j = \mathit{nil}$ that part of the splice is skipped, and the same argument holds with $\mathrm{rank}(\mathit{nil}) = 0$. No other value of $w$ or $next$ changes, so (W) holds for each other node. For (F), each write of line L7 goes to $w[h]$, $next[h]$ or $prev[j]$ with $h$ and $j$ live, so the values of a removed node never change. $\blacksquare$

**Lemma 4 (the expansion is correct).** After line L10 has handled the rounds $R, R - 1, \ldots, r$, each node removed in a round $\ge r$ has $rank[i] = \mathrm{rank}(i)$.

*Proof.* By induction on $r$, from $R + 1$ down to 1. For $r = R + 1$ no round is handled and the claim is empty. For the step, assume the claim for $r + 1$ and let $i \in D_r$. When $i$ was removed, $next[i]$ was $\mathit{nil}$ or a node $j$ that was live and not in $D_r$ (Lemma 1), so $j$ was removed in a round after $r$. By (F), $next[i]$ and $w[i]$ still hold those values when line L10 runs. If $next[i] = \mathit{nil}$, line L10 sets $rank[i] = w[i] = \mathrm{rank}(i)$ by (W). Else $rank[j] = \mathrm{rank}(j)$ by the induction hypothesis, and line L10 sets $rank[i] = w[i] + \mathrm{rank}(j) = \mathrm{rank}(i)$ by (W). The nodes of $D_r$ read only $rank$ values of later rounds and write only their own, so the parallel loop of line L10 does the same as a sequential one. $\blacksquare$

**Theorem (correctness).** Each run that ends returns $\mathrm{rank}(i)$ for each node $i$.

*Proof.* The loop of line L4 ends only when $L$ is empty, so each node is in some $D_r$. Lemma 4 with $r = 1$ gives $rank[i] = \mathrm{rank}(i)$ for each node, and line L11 returns these values. $\blacksquare$
