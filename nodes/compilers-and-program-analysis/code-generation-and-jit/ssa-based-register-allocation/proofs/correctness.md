---
title: SSA-based allocation gives a correct program and uses exactly MaxLive registers when nothing is spilled
proves: [correctness, optimality]
status: full
---

We prove five facts about SSA-ALLOCATE. Lemma 1 is about the spill phase: it stops, and after it each node has at most $k$ names that are not spilled. Lemma 2 shows that the coloring phase gives two interfering names different colors, all below $k$. Lemma 3 shows that, with no spill, the number of colors is exactly MaxLive, the least possible. Lemma 4 shows that the sequential form of a parallel copy does what the parallel copy does. Lemma 5 shows that the output has the same outcome as the input.

## Setup

The input $P$ is a program in strict SSA form: each name has one definition, and each use of a name is dominated by its definition. A phi operand from the predecessor $Q$ counts as a use at the end of $Q$. Line L1 makes the program $W$. It adds a block `start`, the new entry, that copies each parameter $p$ live at the old entry from its slot `mem.p`, and it puts a new empty block on each edge from a block that ends in `br` to a block with phis. Both changes keep the outcome and keep strict SSA form: the copies of the parameters are the only definitions of those names and they dominate every block, and an empty block on an edge only moves the end of the predecessor.

A *node* is the group of all phis of one block, one other instruction, or one terminator. The nodes of a block come in the order phi group, instructions, terminator. For a node $v$, $D(v)$ is the set of names it defines and $O(v)$ is the set of names live just after it. Liveness counts a phi operand as read by the terminator of its predecessor, so $O(t)$ for the terminator $t$ of a block $Q$ is the live-out set of $Q$, phi operands included. Two names $x \ne y$ *interfere* when some node $v$ has $x \in D(v)$ and $y \in D(v) \cup O(v)$. For a set $S$ of spilled names, the *pressure* of $v$ is $|(D(v) \cup O(v)) \setminus S|$, and MaxLive is the largest pressure with $S$ empty.

We use one fact from the [SSA chordal interference theorem](/ssa-chordal-interference-theorem/): in a strict SSA program, the definition of a name $z$ dominates every point where $z$ is live. So if $z \in O(v) \setminus D(v)$, then the node that defines $z$ comes before $v$ in its block, or lies in a block that strictly dominates the block of $v$.

## The spill phase

**Lemma 1.** Lines L3 to L6 stop after at most $n$ rounds, where $n$ is the number of names. When they stop, each node has pressure at most $k$ for the set *spilled*.

*Proof.* Each round runs only if some node $v$ has pressure above $k$. Then $(D(v) \cup O(v)) \setminus \mathit{spilled}$ has more than $k \ge 1$ names, so line L5 can pick one, and line L6 adds a name that was not in *spilled*. So *spilled* grows by one name in each round, and there are at most $n$ rounds. The loop stops only when the test of line L4 fails, that is, when no node has pressure above $k$. $\square$

The choice at line L5 does not matter for correctness. It only changes how many loads and stores the output has.

## The coloring phase

Line L7 visits the blocks in a preorder of the dominator tree, so a block comes after every block that strictly dominates it. Line L8 visits the nodes of a block in order. Call a name *kept* if it is not spilled.

**Lemma 2.** When line L9 runs at a node $v$, every kept name of $O(v) \setminus D(v)$ has a color. Each kept name gets one color, every color is below $k$, and two kept names that interfere get different colors.

*Proof.* Take a kept $z \in O(v) \setminus D(v)$. By the fact from the setup, the node that defines $z$ is earlier in the same block or in a block that strictly dominates the block of $v$. In both cases lines L7 and L8 visit it before $v$, and lines L10 and L11 gave $z$ its color there. Each name has one definition, so each kept name is colored once.

Now the bound. At line L11 for a name $y \in D(v)$, *busy* holds the colors of the kept names of $O(v) \setminus D(v)$ and the colors given so far to the kept names of $D(v)$ before $y$. All of these names are in $(D(v) \cup O(v)) \setminus \mathit{spilled}$ and are not $y$, so by Lemma 1, $|\mathit{busy}| \le k - 1$. The lowest color not in *busy* is at most $|\mathit{busy}|$, so it is below $k$. A partner color is the color of a name colored before, so by induction on the order of the coloring it is below $k$ too.

Last, take kept names $x \ne y$ that interfere at the node $v$ with $x \in D(v)$. If $y \in D(v)$ too, the one of them colored second sees the color of the first in *busy*, because line L12 adds each new color. If $y \in O(v) \setminus D(v)$, its color is in *busy* from line L9 when $x$ is colored. In both cases line L11 picks a color not in *busy*, and a partner color is used only when it is not in *busy*. So $x$ and $y$ get different colors. $\square$

**Lemma 3.** Let $m$ be MaxLive. If $k \ge m$, nothing is spilled and the coloring uses exactly $m$ colors. No valid assignment of registers to the names of $W$ uses fewer.

*Proof.* With $k \ge m$, no node has pressure above $k$ with *spilled* empty, so the loop of line L4 stops at once. Repeat the bound of Lemma 2 with $m$ in place of $k$: at each node $|\mathit{busy}| \le m - 1$, so a lowest free color is below $m$, and by induction every partner color is below $m$ too. So at most $m$ colors are used.

For the lower bound, take a node $v$ with $|D(v) \cup O(v)| = m$. Every $x \in D(v)$ interferes with every other name of $D(v) \cup O(v)$ by the definition. Two names $y, z \in O(v) \setminus D(v)$ are both live just after $v$, and neither is defined at $v$, so both were live just before $v$ too; the theorem shows that two names live at one point interfere (one of their definitions dominates the other, and the other name is live just after the later definition). So $D(v) \cup O(v)$ is a clique of $m$ names, and any valid assignment uses at least $m$ registers. $\square$

This is where chordality shows: the [interference graph](/interference-graph/) of $W$ has chromatic number equal to its largest clique, and a greedy pass in dominance order finds such a coloring without building the graph.

## Leaving SSA form

Let $\mathrm{loc}(x)$ be the register $r_c$ for a kept name of color $c$, and the slot `mem.x` for a spilled name. Lines L13 and L14 put at the end of each predecessor $Q$ of a block $B$ with phis the parallel copy $\{\mathrm{loc}(y) \leftarrow \mathrm{loc}(a)\}$ over the phis $y = \phi[\ldots, Q{:}\ a, \ldots]$ of $B$. Its destinations are distinct: the phis of $B$ form one node, so two kept phis of $B$ get different colors by Lemma 2, and two spilled phis have different slots. The source $Q$ ends in `jump`, since line L1 split every edge from a `br` into a block with phis, so the copy can go just before the jump.

**Lemma 4.** Let $M$ be a list of moves $(d, s)$ with distinct destinations, where each $d$ is a register or a slot and each $s$ is a register, a slot or a constant, and none of them is $s_0$ or $s_1$. The instructions that SEQUENTIALIZE returns leave each $d$ with the old value of its $s$, leave every other register and slot unchanged, and may change only $s_0$ and $s_1$ besides.

*Proof.* Moves with $d = s$ are dropped; they change nothing. Call a move *pending* if it is not yet emitted. We keep this invariant: each pending move reads, from its source, the value that its original source had at the start, and every location that is not $s_0$ and not the destination of an emitted move still has its value from the start.

A move is emitted only when its destination is not the source of any pending move. Emitting it writes $d$, which no pending move still has to read, and it reads its source, which still has the right value by the invariant. A move from a slot to a slot goes through $s_1$, which no pending move reads. So the invariant holds after the emit.

If no move can be emitted, every pending destination is the source of some pending move. There are as many pending moves as pending destinations, and each move has one source, so the sources of the pending moves are exactly the pending destinations. In particular, no pending move reads $s_0$. Line L15 copies the destination $d$ of the first pending move into $s_0$ and makes every pending move that reads $d$ read $s_0$ instead. The invariant holds, and now $d$ is no longer read, so the next round emits a move. Each round either emits a move or is followed by an emit, so the loop stops after at most $2|M|$ rounds with all moves emitted. Then, by the invariant, each destination holds the start value of its source. $\square$

## The same outcome

**Lemma 5.** On every input, the output of SSA-ALLOCATE has the same outcome as $P$.

*Proof.* $W$ has the same outcome as $P$, as shown in the setup. Line L16 turns each node of $W$ into a short list of instructions: a phi group into nothing (its work is done by the parallel copies at the ends of the predecessors), an instruction into the same operation on locations, with loads into $s_0$ and $s_1$ before a read of a slot and a store from $s_0$ after a write of a slot, and a terminator into the same terminator after the parallel copy of its block, if any. So a run of the output follows a run of $W$ node by node. We show by induction along the run this invariant:

(I) Just after each node of $W$, every name $z \in O(v)$ that has a value holds that value in $\mathrm{loc}(z)$.

Just before the entry, nothing is live except the slots of the parameters, which hold the arguments. Now take a node $v$ and assume (I) for the node before it in the run.

- An instruction $y = f(a, b)$. The names $a$ and $b$ are live before $v$, so they are in the live-out set of the previous node, and by (I) they are in $\mathrm{loc}(a)$ and $\mathrm{loc}(b)$. The loads into $s_0$ and $s_1$ change no location of a name. The result goes to $\mathrm{loc}(y)$. Every other $z \in O(v)$ is in $O(v) \setminus D(v)$, so it was live before $v$ and held its value. If $y$ is kept, $z$ kept, then $y$ and $z$ interfere and Lemma 2 gives them different registers. If either is spilled, their locations differ because slots are named after names and registers are not slots. So only $\mathrm{loc}(y)$ changed, and (I) holds after $v$.
- A terminator. It writes no location, and a `br` or `ret` reads its operand from its location, through $s_0$ if it is a slot. If the block ends in `jump` to a block $B$ with phis, the parallel copy runs first. Its sources are phi operands, which are in $O$ of the terminator, so by (I) they hold the right values. By Lemma 4 the copy writes exactly the locations of the phis of $B$ and changes nothing else but $s_0$ and $s_1$.
- The phi group of $B$, reached from $Q$. After the copy at the end of $Q$, $\mathrm{loc}(y)$ holds the value that the phi $y$ takes. The other names live after the phi group are in $O \setminus D$ of the phi group, so they were live at the end of $Q$, and by Lemma 2 none of them shares a location with a phi of $B$. So they kept their values, and (I) holds after the phi group.

Each read of the output therefore sees the value that $W$ reads, and so each branch goes the same way and `ret` returns the same value. A run of $W$ that traps or runs out of fuel does the same in the output after at most a constant factor more steps; the tests use enough fuel for both. $\square$

Together, Lemmas 1 to 5 show that SSA-ALLOCATE gives a program with the same outcome that uses only $r_0, \ldots, r_{k-1}$, $s_0$, $s_1$ and slots, and that when $k \ge$ MaxLive it spills nothing and uses exactly MaxLive registers, which no allocation can beat. The number of spills when $k <$ MaxLive is not minimal: choosing the fewest names to spill is NP-hard even in SSA form.
