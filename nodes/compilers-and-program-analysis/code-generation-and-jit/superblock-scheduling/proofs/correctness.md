---
title: Superblock formation and superblock scheduling keep the meaning of the program and stop
proves: [correctness, termination]
status: full
---

We prove three things about SUPERBLOCK-SCHEDULE. Tail duplication (lines L4 to L6) keeps the outcome of every run and gives each trace one entry. The formation loop (lines L2 to L7) stops. Scheduling one superblock (lines L9 to L14) keeps the outcome of every run, and adds no instruction. The rules of code motion of lines L11 and L12 are exactly what the scheduling proof needs.

## Setup

The program $P$ has an acyclic control flow graph and only `const`, `copy` and `op` instructions. Every value is an integer. A run ends with `ret v` or with a trap (a division or remainder by 0, or a shift by an amount outside 0 to 63). As the graph is acyclic, every run is finite. The *outcome* of a run is its returned value or the trap. $\mathrm{live}(L)$ is the set of names that some path from the start of block $L$ reads before it writes them, the least solution of the usual backward equations, which line L9 computes in one pass in reverse topological order.

An operation $u$ *may trap* if it is a division or remainder whose right operand is not a nonzero constant, or a shift whose amount is not a constant from 0 to 63. Every operation that traps on some run may trap.

## Part 1. Tail duplication

Line L3 gives a trace $T = b_1, \dots, b_k$, a path of blocks that are in no superblock yet. If some $b_i$ with $i \ge 2$ has a predecessor other than $b_{i-1}$ (a *side entrance*), let $j$ be the least such $i$ (line L4). Line L5 makes a new block $c_i$ for each $i \ge j$ with the instructions of $b_i$, and the terminator of $b_i$ in which every target $b_m$ with $m \ge j$ is replaced by $c_m$. Line L6 replaces, in the terminator of every predecessor $p \ne b_{i-1}$ of $b_i$ with $i \ge j$, the target $b_i$ by $c_i$. Call the result $P'$, and let $h$ map each $c_i$ to $b_i$ and every other label to itself.

**Lemma 1.** For every block $L$ of $P'$, the block $h(L)$ of $P$ has the same instructions, and its terminator is the terminator of $L$ with $h$ applied to each target. So $P$ and $P'$ have the same outcome on every input.

*Proof.* For a copy $c_i$ this is the construction of line L5. For any other block, line L6 only renames a target $b_i$ to $c_i$, and $h(c_i) = b_i$. Now run $P$ and $P'$ on the same input. By induction on the number of blocks run, after each block the runs are at labels $L'$ and $h(L')$ with the same state: the two blocks run the same instructions on the same state, so they trap together or reach the same state, and the terminators read the same name and take the targets in the same position, which $h$ maps one to the other. The entry is not a copy, so both runs start at the same label. $\square$

**Lemma 2.** In $P'$, for every $i \ge 2$, the only predecessor of $b_i$ is $b_{i-1}$.

*Proof.* For $i < j$, by the choice of $j$, $b_i$ had no other predecessor, and lines L5 and L6 add no edge into $b_i$: a copy only targets copies and blocks outside the tail. For $i \ge j$, line L6 moved every edge from a predecessor other than $b_{i-1}$ to $c_i$, and a copy never targets $b_i$. The edge from $b_{i-1}$ to $b_i$ is not renamed, since line L6 renames the target $b_i$ only in predecessors other than $b_{i-1}$, and renames a target $b_m \ne b_i$ of $b_{i-1}$ only to $c_m$. $\square$

**Lemma 3.** Once $T$ is a superblock, it stays one: in every later program of the loop, $b_i$ for $i \ge 2$ has the one predecessor $b_{i-1}$.

*Proof.* A later step of line L6 renames only targets that are blocks of the later trace, which are in no superblock yet, so it never removes or adds an edge into $b_i$. A later step of line L5 copies a block $t$ that is in no superblock. If $t$ had an edge to $b_i$ with $i \ge 2$, then $t = b_{i-1}$ by induction, but $b_{i-1}$ is in a superblock. So the copies add no edge into $b_i$. $\square$

**Lemma 4. The formation loop stops.** For a program $Q$ and the set $\mathrm{done}$ of blocks in superblocks, let $p(c) = 1$ if $c$ is done or has no successor, and otherwise $p(c) = \sum_s p(s)$ over the successors $s$ of $c$. Let $\Phi = \sum_{c \text{ not done}} p(c)$. Each step of the loop makes $\Phi$ smaller by at least 1, so the loop stops after at most $\Phi$ steps of the input.

*Proof.* Write $p$ before the step and $p'$ after it, when the blocks of $T$ are done. We show $p'(c) \le p(h(c))$ for every block $c$ of $P'$ that is not done after the step, by induction in reverse topological order of $P'$. If $c$ has no successor, both are 1. Otherwise $h(c)$ was not done before the step (copies are made only of blocks that were not done), and by Lemma 1 the successors of $c$ map one to one under $h$ to the successors of $h(c)$. A successor that is done after the step has $p' = 1 \le p$, and any other successor $s$ has $p'(s) \le p(h(s))$ by induction. So $p'(c) \le p(h(c))$.

The blocks not done after the step are the old blocks not done, minus $b_1, \dots, b_k$, plus the copies $c_j, \dots, c_k$. So
$$\Phi' \le \Big(\Phi - \sum_{i=1}^{k} p(b_i)\Big) + \sum_{i=j}^{k} p(b_i) = \Phi - \sum_{i < j} p(b_i) \le \Phi - p(b_1) \le \Phi - 1,$$
since $j \ge 2$ and $p \ge 1$. Without a side entrance there are no copies, and the bound is the same. $\square$

So formation stops, keeps the outcome of every run (Lemma 1), keeps the graph acyclic (a copy $c_i$ only has edges to copies of later trace blocks and to blocks after $b_i$, and an edge renamed by line L6 goes to a copy whose original came after its source), and gives superblocks that cover all blocks, each with a single entry at its head (Lemmas 2 and 3). The entry block is never $b_i$ with $i \ge 2$, because line L3 does not grow a trace into the entry or backward past it.

## Part 2. Scheduling one superblock

Fix a superblock $b_1, \dots, b_k$ of the current program $P$. Its *items* $I_0, \dots, I_{n-1}$ are, in *index order*: the instructions of each block, called *operations*; for $i < k$, a *branch* $B$ when $b_i$ ends with a `br` to two labels, one of them $b_{i+1}$ and the other its *exit target* $\mathrm{off}(B)$; and the *end* item, the terminator of $b_k$. A branch or the end item reads its condition or its returned name. Two items $u < v$ *conflict* if one of them writes a name that the other reads or writes.

By Lemmas 2 and 3, $\mathrm{off}(B)$ is not a block $b_m$ of the superblock: $m \le i$ would close a cycle, $m = i + 1$ is the trace target, and $m > i + 1$ would give $b_m$ a second predecessor.

Say that an operation $u$ *stays at* a branch $B$ if $u$ may trap or $u$ writes a name of $\mathrm{live}(\mathrm{off}(B))$. The DAG $D$ has these edges $u \to v$, all with $u < v$ and a delay $\delta \ge 0$:

- (E1) data: from the last writer of $x$ before $v$ to each reader $v$ of $x$, delay the latency of the writer; from the last writer of $x$ before $v$ to a writer $v$ of $x$, delay 1; from each reader of $x$ after the last writer of $x$ before $v$ to a writer $v$ of $x$, delay 0;
- (E2) from a branch $B$ to each later branch, to the end item, and to each later operation that stays at $B$ (line L11);
- (E3) from each operation that stays at $B$ to each later branch $B$ (line L12);
- (E4) from each item to the end item.

Line L13 gives each item a cycle $t_v$ with $t_v \ge t_u + \delta(u, v)$ for each edge. The order $\pi$ sorts the items by $(t_v, v)$, and $u \prec v$ means that $u$ is before $v$ in $\pi$. Line L14 cuts $\pi$ after each branch: the first piece takes the label $b_1$, the other pieces get new labels, a piece that ends at a branch $B$ ends with `br` on the same condition to the next piece and to $\mathrm{off}(B)$, in the positions of the old targets, and the last piece ends with the end item. The blocks $b_2, \dots, b_k$ are removed. All other blocks stay as they are. Call the result $P'$.

**Lemma 5. Order.** (a) Each edge $u \to v$ of $D$ has $u \prec v$. (b) If $u < v$ conflict, then $u \prec v$.

*Proof.* (a) $u < v$ and $t_v \ge t_u + \delta(u, v) \ge t_u$, so $(t_u, u) < (t_v, v)$. (b) By (a) it is enough to find a path from $u$ to $v$ in $D$. Let $x$ be the name of the conflict. The writers of $x$ form a path in index order by the output edges of (E1). If $u$ writes and $v$ reads, the last writer $w$ of $x$ before $v$ has $u \le w$, and the path is $u \to \dots \to w \to v$. If $u$ reads and $v$ writes, the first writer $w$ of $x$ after $u$ has $w \le v$, $u$ reads $x$ after the last writer before $w$, so (E1) has $u \to w$, and the path goes on along the writers to $v$. If both write, the writers path joins them. $\square$

**Lemma 6. Shape.** (a) The branches and the end item are in index order in $\pi$, and the end item is last. (b) If an operation $v$ and a branch $B$ are in a different order in $\pi$ than in index order, then $v$ does not stay at $B$: it cannot trap, and it writes no name of $\mathrm{live}(\mathrm{off}(B))$.

*Proof.* (a) is (E2) and (E4) with Lemma 5(a). (b) If $v > B$ and $v$ stayed at $B$, (E2) would give $B \prec v$. If $v < B$ and $v$ stayed at $B$, (E3) would give $v \prec B$. $\square$

So an operation moves above a branch only by speculation that is safe, and below a branch only when it is not needed on the exit and cannot trap. This is why no copy is needed.

**The two runs.** Run $P$ and $P'$ from the label $b_1$, with states $\sigma$ and $\sigma'$ that agree on $\mathrm{live}(b_1)$. $P$ runs the items in index order until a branch leaves or the end item. $P'$ runs the items in the order $\pi$ until a branch leaves or the end item. Call $X$ the items that $P'$ runs, a prefix of $\pi$.

For an item $u$ and a name $x$ that it reads, let $\mathrm{rw}(u, x)$ be the last writer of $x$ among $I_0, \dots, I_{u-1}$, or "none". The *ideal value* $\mathrm{val}(u)$ of an operation is its result when all operations run in index order as straight-line code from $\sigma$, with a special value $\bot$ for an operation that traps or reads $\bot$. $P$ computes exactly the ideal values for the items it runs.

**Lemma 7. The same values.** Every item of $X$ reads the ideal values of its operands, and every operation of $X$ that does not trap computes its ideal value.

*Proof.* By induction along $X$. Let $u \in X$ read $x$. If $w = \mathrm{rw}(u, x)$ exists, then $w \prec u$ by Lemma 5(b), so $w \in X$ before $u$, since $X$ is a prefix of $\pi$. Any other writer $w'$ of $x$ in $X$ has $w' < w$, and then $w' \prec w$, or $w' > u$, and then $u \prec w'$, by Lemma 5(b). So the last writer of $x$ before $u$ in $X$ is $w$, and $u$ reads $\mathrm{val}(w)$ by induction ($w$ did not trap, or the run would have stopped). If $\mathrm{rw}(u, x)$ is none, every writer of $x$ in $X$ comes after $u$, so $u$ reads $\sigma'(x)$. The trace path reads $x$ at $u$ with no write before it, so $x \in \mathrm{live}(b_1)$ and $\sigma'(x) = \sigma(x)$. $\square$

**Lemma 8. One superblock.** Exactly one of these holds.

1. Both runs trap.
2. Both leave at the same branch $B$ to $\mathrm{off}(B)$, with states that agree on $\mathrm{live}(\mathrm{off}(B))$.
3. Both reach the end item. If it is `ret a`, both return the same value. Otherwise both go to the same successor of $b_k$, with states that agree on its live set.

*Proof.* *$P$ leaves at a branch $B^*$ without a trap.* Before $B^*$ in $\pi$, $P'$ meets: branches below $B^*$, which are in index order (Lemma 6(a)) and read the same values as in $P$ (Lemma 7), so they stay on the superblock; operations below $B^*$ that are before $B^*$ in $\pi$, which ran in $P$ without a trap and get the same operands; and operations above $B^*$ that are before $B^*$ in $\pi$, which cannot trap by Lemma 6(b). So $P'$ reaches $B^*$, reads the same condition, and leaves to $\mathrm{off}(B^*)$. Take $x \in \mathrm{live}(\mathrm{off}(B^*))$. $P$ ran the writers of $x$ among the items below $B^*$. $P'$ ran the same writers: by Lemma 6(b), no operation that crossed $B^*$ writes $x$. Their order is the same by Lemma 5(b), so the last writer is the same, and it computed the same value by Lemma 7. If there is no such writer, both states keep the value at $b_1$, and $x \in \mathrm{live}(b_1)$ because the path through $B^*$ to $\mathrm{off}(B^*)$ reads $x$ first. This is case 2.

*$P$ reaches the end item without a trap.* The same argument with the end item for $B^*$. By Lemma 6(a), $X$ is all of $\pi$, so both runs ran all items, with the same last writer of each name. The end item reads the same value. If it is `ret`, both return it. Otherwise both take the same target with states that agree on every name, and in particular on its live set. This is case 3.

*$P$ traps at an operation $o$.* Then $o$ may trap. Suppose that $P'$ does not trap. Then it leaves at a branch $B$ or reaches the end item. The branches before $B$ in $\pi$ stayed on the superblock in $P'$ with the ideal values, so they stay in $P$ too, and $B$ leaves (or is the end) in $P$ too. As $P$ trapped first, $o < B$. Since $o$ may trap, it stays at $B$, so (E3), or (E4) for the end item, gives $o \prec B$, and $o \in X$. By Lemma 7, $o$ got its ideal operands in $P'$, the values with which it traps in $P$. So $P'$ traps, a contradiction. In the first two cases, $P'$ ran only operations that do not trap. So this is case 1, and in cases 2 and 3 $P'$ does not trap either. $\square$

**Theorem 9.** $P$ and $P'$ have the same outcome on every input, and $P'$ has exactly as many instructions as $P$.

*Proof.* The labels of $P'$ are the labels of $P$ other than $b_2, \dots, b_k$, plus the new pieces, which only pieces of the same superblock reach. By Lemma 2 and Lemma 3, the only edge into $b_i$, $i \ge 2$, is from $b_{i-1}$, so no other block of $P$ refers to a removed label. We show, for each label $L$ of $P$ other than $b_2, \dots, b_k$, that runs of $P$ and $P'$ from $L$ with states that agree on $\mathrm{live}(L)$ have the same outcome, by induction on $L$ in reverse topological order of $P$. If $L \ne b_1$, both have the same block at $L$: they trap together, return the same value, or go to the same successor with states that agree on its live set, and that successor is not $b_i$ with $i \ge 2$ (it would be $b_{i-1}$, which is not $L$) and comes later. If $L = b_1$, Lemma 8 applies; in case 2, $\mathrm{off}(B)$ is not in the superblock and comes after $b_1$, and in case 3 the successor of $b_k$ comes after $b_1$. The entry of $P$ is $b_1$ or not in the superblock, so it stays the entry. Line L14 puts every operation in exactly one piece, so no instruction is added or removed. $\square$

**Lemma 10. The rest of the loop.** $P'$ is acyclic, has only `const`, `copy` and `op` instructions, and every other superblock is still a path with a single entry in $P'$.

*Proof.* The pieces form a chain, and the edges out of the chain go to the exit targets and to the successors of $b_k$, which come after $b_k$ or after some $b_i$ in $P$; a cycle through the chain would give a cycle in $P$. The instructions are the old ones. Scheduling changes only the blocks of this superblock and keeps the exit targets, so the edges into the blocks of other superblocks are the same as before. $\square$

## Summary

Formation keeps the outcome (Lemma 1), stops (Lemma 4), and gives superblocks with one entry each (Lemmas 2 and 3). Each scheduling step keeps the outcome and the instruction count (Theorem 9) and keeps the other superblocks valid (Lemma 10). So SUPERBLOCK-SCHEDULE stops, its output has the same outcome as its input on every input, and all its new instructions come from tail duplication, none from scheduling. $\blacksquare$
