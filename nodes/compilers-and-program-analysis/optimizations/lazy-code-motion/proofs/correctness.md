---
title: Lazy code motion is safe, computationally optimal and lifetime optimal
proves: [correctness]
status: full
---

**Setting.** The program has const, copy and op instructions only. After line L1 it has these properties. Every block is reachable from the entry block, and the entry block has no predecessor. No edge goes from a block with two successors to a block with two predecessors. We also assume that every block can reach a `ret`. The proof works on the node graph: one node for each instruction and one for each terminator, with an edge from each node to the next one in its block and from a terminator node to the first node of each successor block. Write $s$ for the first node of the entry block. A *path* is a finite sequence of nodes along edges, and a *complete path* goes from $s$ to a `ret` node. A path can visit a node more than once, so we count *positions* on a path.

Fix one expression $e = a \mathbin{op} b$. The bit vectors treat each expression on its own, so this is no loss. $\mathrm{Comp}(n)$ says that node $n$ computes $e$, and $\mathrm{Transp}(n)$ says that $n$ does not define $a$ or $b$. A node computes before it defines, so `a = a + b` computes $e$ and is not transparent.

The node graph has this property, which is the only place where split edges matter:

**(P)** If a node has two or more predecessors, each of them is a terminator node with one successor. A terminator node defines nothing and computes nothing.

A node inside a block has one predecessor. So a node with two predecessors is the first node of a block $B$, and its predecessors are the terminators of the blocks before $B$. A block before $B$ with two successors would give a critical edge.

## 1. What the equations mean

All six analyses are bit-vector problems with distributive transfer functions, so the round-robin iteration gives the meet over all paths, by the [MOP and MFP coincidence theorem](/mop-mfp-coincidence-theorem/). The analyses that meet with $\cap$ start at the full set and give the greatest solution. This is the meaning of each one, for $e$:

- $\mathrm{ANT}(n)$ (line L3, the value of ANT.in): every path from $n$ to a `ret` node has a position $m$ with $\mathrm{Comp}(m)$ and every node before it, from $n$ on, transparent. We say $n$ is *down-safe*.
- $\mathrm{AV.in}(n)$ (line L4): every path from $s$ to $n$ has a position $z$ before $n$ with $\mathrm{ANT}$ at $z$ and the nodes from $z$ to the predecessor of $n$ transparent. It is false at $s$.
- $\mathrm{EARLIEST}(n) = \mathrm{ANT}(n) \wedge \neg \mathrm{AV.in}(n)$ (line L5).
- $\mathrm{DELAY}(n) = \mathrm{EARLIEST}(n) \vee \mathrm{POST.in}(n)$ (line L6): every path from $s$ to $n$ has a position $z$ with $\mathrm{EARLIEST}$ at $z$ and no $\mathrm{Comp}$ node from $z$ to the predecessor of $n$.
- $\mathrm{LATEST}(n)$ (line L7): $\mathrm{DELAY}(n)$, and $\mathrm{Comp}(n)$ or some successor of $n$ is not $\mathrm{DELAY}$. At a `ret` node this is $\mathrm{DELAY}(n) \wedge \mathrm{Comp}(n)$.
- $\mathrm{USED.out}(n)$ (line L8, the least solution): some path from a successor of $n$ reaches a $\mathrm{Comp}$ node $m$, and no node on it, $m$ included, is $\mathrm{LATEST}$.
- $n$ is *up-safe* if every path from $s$ to $n$ has a position $c$ with $\mathrm{Comp}(c)$ and the nodes from $c$ to the predecessor of $n$, $c$ included, transparent. A node is *safe* if it is down-safe or up-safe.

## 2. Placements

A *placement* is a set $I$ of nodes. Its program computes `t = e` just before each node of $I$, into a new name $t$, and replaces each original `x = e` by `x = t`. A placement is *admissible* if every node of $I$ is safe, and if on every path from $s$ to a $\mathrm{Comp}$ node $m$ there is a position $w$ of a node of $I$ such that the nodes from $w$ to the predecessor of $m$ are transparent. We say that $t$ is *valid* at $m$.

The LCM program is the program of the placement
$$I_{\mathrm{LCM}} = \{\, n : \mathrm{LATEST}(n) \wedge (\mathrm{USED.out}(n) \vee \mathrm{Comp}(n)) \,\}.$$
Line L9 inserts at $\mathrm{LATEST} \wedge \mathrm{USED.out}$. At a node with $\mathrm{LATEST} \wedge \mathrm{Comp} \wedge \neg\mathrm{USED.out}$, line L11 keeps `x = e`, which is the same as `t = e; x = t` with a dead $t$. On every path both programs evaluate $e$ equally often and write the same values into the old names.

The placement of busy code motion (BCM) is $I_{\mathrm{BCM}} = \{\, n : \mathrm{EARLIEST}(n) \,\}$.

## 3. Admissible placements keep the outcome

**Theorem A.** Let $I$ be admissible. On each input, if the old program returns $v$, the new program returns $v$. If the old program traps, the new program traps.

*Proof.* Run both programs on the same input, and use fuel without limit. They take the same branches and hold the same values in the old names, as long as the new program does not trap at an inserted `t = e`. The induction step for an old instruction is clear, except at a replaced `x = e` at a node $m$. There $t$ is valid at $m$ along the path of the run. The last `t = e` before $m$ is at or after the position $w$ that validity gives. So it ran with the operand values that $e$ has at $m$, and $t$ holds the value of $e$. That `t = e` did not trap, so `x = e` would not trap either.

Now say an inserted `t = e` before node $n$ traps, and the old run has not stopped yet. If $n$ is up-safe, the path of the run has a position $c$ before $n$ with $\mathrm{Comp}(c)$ and transparent nodes from $c$ on. The old run computed $e$ at $c$ with the same operand values. That would have trapped, and the run would have stopped. So $n$ is down-safe. The old run goes on from $n$ in the same state. If it traps before it reaches a `ret`, both runs trap. Otherwise its path from $n$ reaches a `ret` node, so by down-safety it reaches a $\mathrm{Comp}$ node first, through transparent nodes, and $e$ traps there with the same operands. $\square$

The proof needs the old run to end. A run that never ends can pass a down-safe node and then loop forever away from the computation, and the new run then traps. The tests use programs that stop.

## 4. The two placements are admissible

**Lemma 1.** On a path $n_1 \ldots n_k$ from $s$ with $\mathrm{ANT}(n_k)$, there is a $j \le k$ with $\mathrm{EARLIEST}(n_j)$ and $n_j \ldots n_{k-1}$ transparent.

*Proof.* Take the least $j$ with $\mathrm{ANT}(n_j)$ and $n_j \ldots n_{k-1}$ transparent; $j = k$ is a candidate. If $\mathrm{AV.in}(n_j)$, then $j > 1$ and the path $n_1 \ldots n_j$ has a $z < j$ with $\mathrm{ANT}(n_z)$ and $n_z \ldots n_{j-1}$ transparent. Then $z$ is a smaller candidate. $\square$

**Lemma 2.** If $\mathrm{ANT}(n_j)$, $n_j \ldots n_{k-1}$ are transparent and none of them computes $e$, then $\mathrm{ANT}(n_l)$ for $j \le l \le k$.

*Proof.* Any path from $n_l$ to a `ret` node, with $n_j \ldots n_{l-1}$ in front, is a path from $n_j$. Its first $\mathrm{Comp}$ node is at or after $n_l$, and the nodes before it are transparent. $\square$

**Lemma 3.** If $\mathrm{DELAY}(n)$, then $\mathrm{ANT}(n)$.

*Proof.* Every node reaches a `ret`. Take a path from $s$ to $n$ and its position $z$ from the meaning of DELAY. Continue the path from $n$ to a `ret` node. Down-safety at $z$ and the absence of $\mathrm{Comp}$ from $z$ to the predecessor of $n$ give that $n_z \ldots$ up to the predecessor of $n$ are transparent. Lemma 2 gives $\mathrm{ANT}(n)$. $\square$

**Theorem B.** $I_{\mathrm{BCM}}$ and $I_{\mathrm{LCM}}$ are admissible.

*Proof.* Safety: $\mathrm{EARLIEST} \subseteq \mathrm{ANT}$, and $\mathrm{LATEST} \subseteq \mathrm{DELAY} \subseteq \mathrm{ANT}$ by Lemma 3.

Validity for BCM: if $\mathrm{Comp}(m)$ then $\mathrm{ANT}(m)$, and Lemma 1 gives the position.

Validity for LCM: take a path $n_1 \ldots n_k$ with $\mathrm{Comp}(n_k)$. Lemma 1 gives $j$ with $\mathrm{EARLIEST}(n_j)$ and $n_j \ldots n_{k-1}$ transparent. Walk from $l = j$. $\mathrm{DELAY}(n_l)$ holds at $l = j$. If $n_l$ is not $\mathrm{LATEST}$, it does not compute $e$ and all its successors are $\mathrm{DELAY}$, so $\mathrm{DELAY}(n_{l+1})$. At $l = k$, $\mathrm{Comp}(n_k)$ makes $n_k$ $\mathrm{LATEST}$. So $[j, k]$ has a $\mathrm{LATEST}$ position. Let $i$ be the largest. If $i = k$, then $n_k \in I_{\mathrm{LCM}}$. If $i < k$, no node $n_{i+1} \ldots n_k$ is $\mathrm{LATEST}$, so $\mathrm{USED.out}(n_i)$ by the path $n_{i+1} \ldots n_k$, and $n_i \in I_{\mathrm{LCM}}$. In both cases the nodes from $n_i$ to $n_{k-1}$ are transparent. $\square$

## 5. Computational optimality

Fix a complete path $P = n_1 \ldots n_r$. For each $\mathrm{EARLIEST}$ position $j$ on $P$, let $m(j)$ be the first position $\ge j$ with $\mathrm{Comp}$. It exists, since $\mathrm{ANT}(n_j)$ and $P$ ends at a `ret`, and $n_j \ldots n_{m(j)-1}$ are transparent. Call $[j, m(j)]$ the *segment* of $j$.

**Lemma 4.** No node at a position in $(j, m(j)]$ is $\mathrm{EARLIEST}$, so the segments on $P$ are disjoint.

*Proof.* Let $j < l \le m(j)$. By Lemma 2, every node from $n_j$ to $n_l$ is down-safe. We show $\mathrm{AV.in}(n_l)$. $\mathrm{AV.out}(n_{l-1})$ holds, because $n_{l-1}$ is down-safe and transparent. If $n_l$ has another predecessor $q$, then by (P) $q$ is a terminator with the one successor $n_l$. Since $n_l$ is down-safe and $q$ is transparent and computes nothing, $q$ is down-safe, so $\mathrm{AV.out}(q)$. So all predecessors give $\mathrm{AV.out}$, and $\mathrm{AV.in}(n_l)$. $\square$

**Lemma 5.** Every admissible placement $I$ has a node at some position of each segment.

*Proof.* Say no node of $I$ is at a position in $[j, m(j)]$. If $j = 1$, validity at $n_{m(j)}$ along $n_1 \ldots n_{m(j)}$ fails at once. Otherwise $\neg \mathrm{AV.in}(n_j)$ gives a path $q$ from $s$ to a predecessor of $n_j$ with no position $z$ that has $\mathrm{ANT}$ and transparent nodes from $z$ to the end of $q$. On the path $q\, n_j \ldots n_{m(j)}$, validity gives a position $w$ of a node of $I$ with transparent nodes from $w$ on. The node at $w$ is not one of $n_j \ldots n_{m(j)}$, so $w$ is on $q$. If the node at $w$ is down-safe, $w$ is a forbidden $z$. If it is up-safe, the part of $q$ before $w$ has a $\mathrm{Comp}$ position $c$ with transparent nodes from $c$ on, and $c$ is a forbidden $z$, since $\mathrm{Comp}$ implies $\mathrm{ANT}$. $\square$

**Lemma 6.** On $P$, every position of $I_{\mathrm{LCM}}$ lies in a segment, and each segment holds at most one of them.

*Proof.* Let $i$ be a position of $I_{\mathrm{LCM}}$. Then $\mathrm{DELAY}(n_i)$, so there is a position $j \le i$ with $\mathrm{EARLIEST}$ and no $\mathrm{Comp}$ from $n_j$ to $n_{i-1}$. Take the largest such $j$, and call it $j(i)$. As in the proof of Lemma 3, down-safety at $n_j$ makes the nodes from $n_j$ to $n_{i-1}$ transparent. None of them computes $e$, so $i \le m(j)$ and $i$ is in the segment of $j$.

Now let $i < i'$ be positions of $I_{\mathrm{LCM}}$ with $j(i') \le i$. Then no $\mathrm{Comp}$ is in $n_{j(i')} \ldots n_{i'-1}$, so $n_i$ does not compute $e$, and $n_i$ is $\mathrm{LATEST}$ because a successor is not $\mathrm{DELAY}$. If $n_i$ has two successors, (P) says that each has $n_i$ as its only predecessor, so each is $\mathrm{DELAY}$ through $\mathrm{POST.in}$. So $n_i$ has the one successor $n_{i+1}$. We show $\mathrm{DELAY}(n_l)$ for $i < l \le i'$. Take any path $q$ from $s$ to $n_l$, and add $n_{l+1} \ldots n_{i'}$. The meaning of $\mathrm{DELAY}(n_{i'})$ gives an $\mathrm{EARLIEST}$ position with no $\mathrm{Comp}$ up to $n_{i'-1}$. It is not in $n_{l+1} \ldots n_{i'}$, since such a position on $P$ would be larger than $j(i')$ and allowed. So it is on $q$, and it shows $\mathrm{DELAY}(n_l)$. With $l = i + 1$, $n_i$ is not $\mathrm{LATEST}$, which is false. So $j(i') > i$, and the map $i \mapsto j(i)$ is one to one. $\square$

**Theorem C.** For every admissible placement $I$ and every complete path $P$, BCM and LCM evaluate $e$ equally often on $P$, and no more often than $I$.

*Proof.* The program of a placement evaluates $e$ exactly at the positions of its nodes on $P$. BCM has one position for each segment. By Lemmas 4 and 5, $I$ has at least that many. By Lemma 6, LCM has at most that many, and by Lemma 5, applied to $I_{\mathrm{LCM}}$, at least that many. $\square$

The original program is the admissible placement that inserts just before each $\mathrm{Comp}$ node, so LCM never evaluates $e$ more often on a path than the original program does.

## 6. Lifetime optimality

The lifetime of a placement $I$ is the set of nodes $n$ after which $t$ is live: some path from a successor of $n$ reaches a $\mathrm{Comp}$ node $m$ with no node of $I$ on it, $m$ included. A placement is *computationally optimal* if it is admissible and evaluates $e$ as often as LCM on every complete path.

**Lemma 7.** Let $I$ be computationally optimal and $P$ a complete path. Then $I$ has exactly one position in each segment of $P$ and none outside the segments, and in each segment its position is at or before the position of $I_{\mathrm{LCM}}$.

*Proof.* The count on $P$ equals the number of segments, each segment holds at least one position (Lemma 5), and the segments are disjoint (Lemma 4). This gives the first claim, for $I$ and for $I_{\mathrm{LCM}}$. Let $x$ and $y$ be the positions of $I_{\mathrm{LCM}}$ and $I$ in the segment $[j, m(j)]$, and say $y > x$. Then $x < m(j)$, so $n_x$ does not compute $e$, and as in Lemma 6 its one successor $n_{x+1}$ is not $\mathrm{DELAY}$. So a path $q$ from $s$ to $n_{x+1}$ has no $\mathrm{EARLIEST}$ position with no $\mathrm{Comp}$ from it to the predecessor of $n_{x+1}$. Let $Q$ be $q$ followed by $n_{x+2} \ldots n_r$, a complete path. A segment of $Q$ that contains a position of $n_{x+1} \ldots n_{m(j)}$ starts at an $\mathrm{EARLIEST}$ position. By Lemma 4 on $P$, that position is not in $n_{x+1} \ldots n_{m(j)}$, so it is on $q$ before $n_{x+1}$, and the segment has no $\mathrm{Comp}$ from it to the end of $q$. The choice of $q$ forbids this. So no segment of $Q$ contains these positions, and by the first claim on $Q$ no node of $I$ is at them. But $n_y$ is one of them and is in $I$. $\square$

**Theorem D.** If $I$ is computationally optimal, the lifetime of $I_{\mathrm{LCM}}$ is a subset of the lifetime of $I$.

*Proof.* Let $n$ be in the lifetime of $I_{\mathrm{LCM}}$, by a path $\pi$ from a successor of $n$ to a $\mathrm{Comp}$ node $m$ with no node of $I_{\mathrm{LCM}}$. Put a path from $s$ to $n$ in front and a path from $m$ to a `ret` node behind, to get a complete path $P$. Say a node of $I$ is at a position $y$ of $\pi$. By Lemma 7, $y$ is in a segment $[j, m(j)]$, and the position $x$ of $I_{\mathrm{LCM}}$ in that segment is at or after $y$. It is not on $\pi$, so $x$ is after $m$. Then $m$ is a $\mathrm{Comp}$ position with $j \le y \le m < x \le m(j)$, which is before the first $\mathrm{Comp}$ position $m(j)$ of the segment. This is false. So $\pi$ has no node of $I$, and $n$ is in the lifetime of $I$. $\square$

## 7. Why the critical edges must be split

Property (P) is used in Lemmas 4, 6 and 7. Without it the optimum can be out of reach. In the program of the page's pitfall, with a branch `B2: br d B3 B4` and a partial redundancy at the join `B3`, the only node where a placement could evaluate `a / b` once on the path through `B1` and never on the path to `B4` is the edge `B2 -> B3` itself. The block `B2` is not down-safe, because the path to `B4` does not compute `a / b`, and the start of `B3` is too late. A new block on the edge gives the node that the proof needs.
