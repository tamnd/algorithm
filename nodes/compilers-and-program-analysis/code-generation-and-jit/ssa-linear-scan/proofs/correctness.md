---
title: SSA linear scan builds exact intervals without a fixed point and gives a correct program
proves: [correctness, optimality]
status: full
---

We prove six facts about SSA-LINEAR-SCAN. Lemma 1 is about the block order. Lemmas 2 and 3 show that the one backward pass of lines L3 to L11 gives, for each name, exactly the positions where it is live, with no fixed point. Lemma 4 shows that the scan never gives one register to two intervals that intersect. Lemma 5 shows that with $k \ge$ MaxLive nothing is spilled and exactly MaxLive registers are used. Lemma 6 shows that the output has the same outcome as the input.

## Setup

The input $P$ is in strict SSA form: each name has one definition, and the definition dominates each use, where a phi operand from $Q$ counts as a use at the end of $Q$. The control flow graph is reducible. Line L1 adds a start block that copies each parameter from its slot, and puts an empty block on each edge from a `br` to a block with phis. Both keep strict SSA form, reducibility and the outcome.

An edge $u \to h$ is a *back edge* if $h$ dominates $u$. The *loop* of a header $h$ is the union, over the back edges $u \to h$, of $h$ and the blocks that reach $u$ without passing through $h$. In a reducible graph, the graph $F$ without back edges is acyclic, and two loops with different headers are disjoint or one holds the other: if $h \in \mathrm{loop}(h')$ and $h' \in \mathrm{loop}(h)$ with $h \ne h'$, each would dominate the other.

A *node* is the group of phis of a block, an instruction or a terminator, as on the [SSA chordal interference theorem](/ssa-chordal-interference-theorem/) page. For a node $v$, $D(v)$ is the set of names it defines and $O(v)$ the names live just after it, where a phi operand stays live until the end of its predecessor. Names $x \ne y$ *interfere* when some node $v$ has $x \in D(v)$ and $y \in D(v) \cup O(v)$, and MaxLive is the largest $|D(v) \cup O(v)|$.

Positions follow the order of line L2. A block $b$ has the even position $b.\mathit{start}$, where its phis write; its items get the next even positions; and $b.\mathit{end}$, two after its last item, is the start of the next block. A name is *live at* position $q$ of an item when it is live just after that item and was live before it or is written by it; it is live at $q + 1$ when it is live just after the item. It is live at $b.\mathit{start}$ when it is a phi of $b$ or live into $b$, and at $b.\mathit{start} + 1$ when it is live after the phis. A phi operand that $b$ sends is live up to $b.\mathit{end}$. A name that is written and never read gets the single position of its write.

## The block order

**Lemma 1.** Line L2 lists every reachable block once. Each block comes after its strict dominators, the blocks of each loop are contiguous with the header first, and every edge $u \to w$ with $w$ before $u$ is a back edge.

*Proof.* Look at one call of the region routine, on a loop body $R$ with header $h$, or on all blocks with the entry as $h$. Every block $v$ of $R$ is mapped to $\mathrm{top}(v)$, the header of the largest loop inside $R$, other than the loop of $h$, that holds $v$, or $v$ itself. The edges of the shrunken graph are the edges $u \to w$ of $R$ with $w \ne h$ and $\mathrm{top}(u) \ne \mathrm{top}(w)$.

No such edge is a back edge. A back edge $u \to w$ with $w \ne h$ inside $R$ has $u \in \mathrm{loop}(w)$; the loops of $R$ that hold $w$ form a chain and all hold $\mathrm{loop}(w)$, so $u$ and $w$ have the same top. So all edges of the shrunken graph come from edges of $F$. It has no cycle: entries into a loop go to its header, and inside a loop the header reaches every block by edges of $F$, so a cycle of shrunken nodes would give a cycle in $F$. Every block of $R$ is reachable from $h$ inside $R$, so the depth-first search from $h$ reaches every shrunken node, and its reverse postorder is a topological order of them, with $h$ first.

Each loop node is then replaced by the order of its own loop, built the same way. By induction on the depth of the loops, each loop is contiguous with its header first, and each edge of $F$ goes forward in the order. Every edge that goes backward is therefore a back edge.

For dominance, let $d$ strictly dominate $v$. If $d$ is outside the region of $v$, then $d$ dominates the header of that region and comes before it by induction. Otherwise, a path in the shrunken graph from $h$ to $\mathrm{top}(v)$ that misses $\mathrm{top}(d)$ would lift to a path in $R$ from $h$ to $v$ that misses $d$; with a path from the entry to $h$, this contradicts dominance (if $\mathrm{top}(d) = \mathrm{top}(v)$, use induction inside the loop). So $\mathrm{top}(d)$ is on every path to $\mathrm{top}(v)$ in an acyclic graph, and it comes first in any topological order. $\square$

## The intervals are exact

Let $\mathrm{PL}(b)$ be the set of names live into $b$ in the graph $F$, that is, along paths with no back edge, not counting the phis of $b$.

**Lemma 2.** When line L3 has finished with $b$, the set $\mathit{liveIn}(b)$ is $\mathrm{PL}(b)$. Every range added is made of positions where its name is live.

*Proof.* By Lemma 1, every edge $b \to s$ of $F$ goes forward, so $s$ is done before $b$ in the backward pass, and line L4 unions $\mathrm{PL}(s)$ over those successors and adds the phi operands sent by $b$. For a back edge $b \to h$, $h$ is not done yet, and line L4 adds only the phi operands of $h$ from $b$, which are live until the end of $b$. This set is the live-out set of $b$ in $F$. Lines L5 to L9 then do the standard backward walk through one block: a name live at the end gets the whole block, a definition cuts the range of its name to start at the definition, and a use adds the range from the block start to the use. So $\mathit{liveIn}(b)$ is the live-in set of $b$ in $F$ without the phis of $b$, which is $\mathrm{PL}(b)$.

Every position put in a range at lines L5 to L9 is live in $F$, hence live in the program. The first range of a name $y$ at line L7 is the one from this block, since all ranges added before come from later blocks, so the cut is right. For line L11, take $x \in \mathrm{PL}(h)$ for a header $h$. The definition of $x$ dominates $h$, by strictness, and is not a phi of $h$. It is not in $\mathrm{loop}(h)$ either, since no block of the loop other than $h$ dominates $h$, and a definition inside $h$ after its start could not reach a use before itself without passing through itself. Every block of the loop reaches $h$ inside the loop with no definition of $x$, and from $h$ the name $x$ reaches a use. So $x$ is live at every position of the loop, which by Lemma 1 is exactly the range from $h.\mathit{start}$ to the end of the last block of the loop. $\square$

**Lemma 3.** A name $x$ is live at a position if and only if its interval covers that position.

*Proof.* One direction is Lemma 2. For the other, let $x$ be live at a position in block $b$. If a use of $x$ later in $b$ explains it, or $x$ is defined at that position, lines L6 to L9 cover it. Otherwise $x$ is live into $b$ or live at its end, and it is enough to show $x \in \mathrm{PL}(b)$, or $x \in \mathrm{PL}(h)$ for a header $h$ whose loop holds $b$: in the first case lines L4 to L9 of the blocks on the path cover the position, and in the second line L11 does.

Take a shortest path $\pi$ from the start of $b$ to a use of $x$ with no definition of $x$; it repeats no block. We use induction on the number of back edges on $\pi$. With none, $x \in \mathrm{PL}(b)$. Otherwise, let $u \to h$ be the first back edge. The part from $b$ to $u$ is in $F$, and it does not pass through $h$, because $h$ comes later on $\pi$ and $\pi$ repeats no block; also $b \ne h$ for the same reason. So $b$ reaches $u$ without passing $h$, and $b \in \mathrm{loop}(h)$. The rest of $\pi$, from $h$, has fewer back edges, so by induction $x \in \mathrm{PL}(h)$, or $x \in \mathrm{PL}(h')$ for a header $h'$ whose loop holds $h$. In the second case the loop of $h'$ shares $h$ with the loop of $h$, so one holds the other, and it is the loop of $h'$ that holds the loop of $h$ (otherwise $h'$ would be in the loop of $h$ and the two headers would dominate each other). So $b \in \mathrm{loop}(h')$ as well. $\square$

So the backward pass computes liveness exactly in one pass. Two intervals then intersect if and only if their names interfere: a shared position is either the write of one name while the other is live after it or written at the same node, or a point where both are live, and by Lemma 3 of the theorem page two names live at one point interfere. Conversely, if $x \in D(v)$ and $y \in D(v) \cup O(v)$, both intervals cover the position of $v$.

## The scan

**Lemma 4.** Every kept interval gets one register below $k$, and two kept intervals that intersect get different registers.

*Proof.* We keep this invariant at line L14 for the interval $\mathit{cur}$ with start $p$: every kept interval handled before is in *active* if it covers $p$, in *inactive* if it does not cover $p$ but ends after $p$, and dropped if it ends at or before $p$. Lines L14 and L15 restore it from the previous step, since they look again at every interval of both sets.

A dropped interval cannot intersect $\mathit{cur}$, which lies at or after $p$. An active interval covers $p$, which $\mathit{cur}$ also covers. So the registers held by earlier kept intervals that intersect $\mathit{cur}$ are exactly those in *busy* at line L16. Line L17 picks a register not in *busy*. At line L18, two active intervals both cover $p$ and so intersect, and by induction they have different registers, so $s$ is the only active interval with its register. No inactive interval that intersects $\mathit{cur}$ holds that register, by the choice of $s$. So after $s$ is spilled, no earlier kept interval that intersects $\mathit{cur}$ shares its register. Later intervals are checked against $\mathit{cur}$ in their own step. $\square$

**Lemma 5.** If $k \ge$ MaxLive $= m$, nothing is spilled and exactly $m$ registers are used.

*Proof.* Order the names by the start of their interval, which is the position of their definition. By Lemma 1, a strict dominator comes before in this order, which is all that Lemma 4 of the theorem page needs. So the names that start no later than $\mathit{cur}$ and intersect it, that is, interfere with it, are all in $D(v) \cup O(v)$ for the node $v$ that defines $\mathit{cur}$. There are at most $m - 1$ of them, so *busy* has at most $m - 1$ registers and line L17 picks a register below $m \le k$. No spill happens, and at most $m$ registers are used. A node with $|D(v) \cup O(v)| = m$ gives $m$ names that pairwise interfere (Lemma 3 of the theorem page), so their intervals pairwise intersect and need $m$ different registers. $\square$

The same argument shows that an inactive interval never intersects $\mathit{cur}$, for any $k$. If $x$ started before $p$ and does not cover $p$, but meets $\mathit{cur}$, the two names interfere, so one is live at the definition of the other. The name $x$ is not live at $p$, and $\mathit{cur}$ is not live before $p$. So the registers from inactive intervals at line L16 add nothing, and the choice at line L18 is among all active intervals. Wimmer and Franz use this to skip intersection tests.

When $k < m$ the scan spills, and the choice at lines L18 to L20 is a heuristic. Without lifetime holes the furthest end rule would give the fewest spilled intervals, as on the [linear scan](/linear-scan-register-allocation/) page. With holes the intervals no longer form an interval graph, and that optimality is lost.

## The same outcome

**Lemma 6.** On every input, the output has the same outcome as $P$.

*Proof.* Let $\mathrm{loc}(x)$ be $r_c$ for a kept name with register $c$ and `mem.x` for a spilled one. We show that along a run, at each position, every name whose interval covers the position holds its value in $\mathrm{loc}(x)$.

An instruction at position $q$ that writes $y$ reads its operands from their locations, which hold their values by the invariant, through $s_0$ and $s_1$ for slots. It then writes $\mathrm{loc}(y)$ only. Any other name $z$ live after the item was live before it too, so its interval covers $q$, as does the interval of $y$. They intersect, so $z$ has a different register by Lemma 4, or one of them has a slot, which is named after its name.

At the end of a block $Q$ whose successor $B$ has phis, $Q$ ends in `jump` because of line L1. The parallel copy reads the phi operands, which are live up to $Q.\mathit{end}$ and so hold their values. Its destinations are the locations of the phis of $B$; they are different, since the phis of one block all start at $B.\mathit{start}$ and pairwise intersect. A name $z$ live into $B$ that is not a phi also covers $B.\mathit{start}$, so it does not share a location with a phi of $B$. The sequential form from line L22 writes the destinations with the values the parallel copy would give and changes nothing else but $s_0$ and $s_1$, by the same argument as for the [SSA-based allocator](/ssa-based-register-allocation/): a move is emitted only when no pending move reads its destination, and when only cycles are left one destination is saved in $s_0$, which no pending move reads at that time. So after the copy, every name live into $B$ and every phi of $B$ holds its value.

Branches and returns read their operands from their locations. So the output takes the same branches and returns the same value as $P$, and it traps in the same place. $\square$
