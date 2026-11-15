---
title: Trace scheduling with compensation code keeps the meaning of the program and stops
proves: [correctness, termination]
status: full
---

We prove that one step of TRACE-SCHEDULE (lines L2 to L14: pick a trace, schedule it, add compensation code, cut it into blocks) gives a program with the same outcome as the input on every input. Then we prove that the loop of line L1 stops on an acyclic control flow graph. The rules of code motion in lines L4 to L6 are exactly what the proof needs: each rule appears in one lemma.

## Setup

The program $P$ has an acyclic control flow graph and only `const`, `copy` and `op` instructions. Every value is an integer. A run of $P$ ends with `ret v` or with a trap (a division or remainder by 0, or a shift by an amount outside 0 to 63). As the graph is acyclic, every run is finite. $\mathrm{live}(L)$ is the set of names that some path from the start of block $L$ reads before it writes them. It is the least solution of the usual backward equations, which line L3 computes.

**The trace and its items.** The trace is a path $b_1, \dots, b_k$ of the graph. The entry block of $P$ is never $b_j$ for $j \ge 2$, because line L2 never grows a trace backward from the entry. Its *items* $I_0, \dots, I_{n-1}$ are, in this *index order*:

- for each $b_j$ with $j \ge 2$ that has a predecessor other than $b_{j-1}$: an *entrance* $J_j$;
- the instructions of $b_j$, which we call *operations*;
- for $j < k$, if $b_j$ ends with a `br` to two labels: a *branch* $B$. One target is $b_{j+1}$, and the other is its *off-trace target* $\mathrm{off}(B)$;
- for $j = k$: the *end* item, the terminator of $b_k$.

A branch or the end item reads its condition or its returned name. We say that two items $u < v$ *conflict* if one of them writes a name that the other reads or writes.

**The DAG.** $D$ has these edges $u \to v$ with $u < v$ and a delay $\delta(u, v) \ge 0$:

- (E1) data: from the last writer of $x$ before $v$ to each reader $v$ of $x$, delay the latency of the writer; from the last writer of $x$ before $v$ to a writer $v$ of $x$, delay 1; from each reader of $x$ after the last writer of $x$ before $v$ to a writer $v$ of $x$, delay 0;
- (E2) from a branch $B$ to each later branch and to the end item; and from $B$ to each later operation that can trap or whose result is in $\mathrm{live}(\mathrm{off}(B))$ (line L5);
- (E3) from each item before an entrance $J$ to $J$, and from $J$ to each later branch and to the end item (line L6);
- (E4) from each item to the end item.

**The schedule.** Line L7 gives each item a cycle $t_v$ with $t_v \ge t_u + \delta(u, v)$ for each edge. The order $\pi$ sorts the items by $(t_v, v)$. We write $u \prec v$ when $u$ comes before $v$ in $\pi$.

**The output $P'$.** Walk $\pi$ and cut it after each branch, at each entrance and after the end item. The pieces become blocks. The first piece keeps the label $b_1$. A piece that ends with a branch $B$ ends with `br` to the next piece and to the exit target of $B$: that is $\mathrm{off}(B)$ if $M_B$ is empty, and otherwise a new *exit block* with copies of the operations of

$$M_B = \{u \text{ operation} : u < B,\ B \prec u\}$$

in the order $\pi$, and then `jump off(B)` (lines L8 to L10). A piece that ends at an entrance $J_j$ jumps to the next piece. The label $b_j$ goes to a new *entrance block* with copies of the operations of

$$C_j = \{u \text{ operation} : u > J_j,\ u \prec J_j\}$$

in the order $\pi$, and then a jump to the piece after $J_j$. If $C_j$ is empty, the piece after $J_j$ takes the label $b_j$ itself (lines L11 to L13). The last piece ends with the terminator of $b_k$. All other blocks of $P$ stay as they are.

## Lemma 1. Order

(a) Each edge $u \to v$ of $D$ has $u \prec v$. (b) If $u < v$ conflict, then $u \prec v$.

*Proof.* (a) $u < v$ and $t_v \ge t_u + \delta(u, v) \ge t_u$, so $(t_u, u) < (t_v, v)$.

(b) By (a) it is enough to find a path from $u$ to $v$ in $D$. Let $x$ be the name of the conflict and let $w_1 < w_2 < \dots$ be the writers of $x$. Consecutive writers are joined by output edges of (E1), so the writers form a path in index order. If $u$ writes and $v$ reads, the last writer $w$ before $v$ has $u \le w$, and the path goes $u \to \dots \to w \to v$. If $u$ reads and $v$ writes, the first writer $w$ after $u$ has $w \le v$, $u$ is a reader after the last writer before $w$, so (E1) has $u \to w$, and the path goes on along the writers to $v$. If both write, the writers path joins them. $\square$

## Lemma 2. Shape of the order

(a) The branches and the end item are in index order in $\pi$.

(b) For an entrance $J$: every item $u < J$ has $u \prec J$, and every branch or end item $v > J$ has $J \prec v$. So the items $v \succ J$ all have $v > J$.

(c) For a branch $B$ and an entrance $J < B$: every $u \in M_B$ has $u > J$.

(d) For a branch $B$: every operation $v > B$ with $v \prec B$ cannot trap, and its result is not in $\mathrm{live}(\mathrm{off}(B))$.

*Proof.* (a) is (E2) with Lemma 1. (b) is (E3) with Lemma 1; for the last sentence, an operation $v < J$ would have $v \prec J$. (c) If $u < J$, then $u \prec J \prec B$ by (b), but $u \in M_B$ means $B \prec u$. (d) If $v$ could trap or wrote a name of $\mathrm{live}(\mathrm{off}(B))$, (E2) would give the edge $B \to v$ and so $B \prec v$. $\square$

## The run through one region

Fix an *entrance point* $e$: either $e = -1$ for the head $b_1$, or $e$ is the index of an entrance $J_j$. Its label $L_e$ is $b_1$ or $b_j$. Both labels exist in $P'$. Let $\pi_e$ be $\pi$ restricted to the items with index above $e$.

**What $P$ does from $L_e$.** It runs the items $e+1, e+2, \dots$ in index order. An entrance does nothing. A branch either goes on along the trace or leaves to $\mathrm{off}(B)$.

**What $P'$ does from $L_e$.** For $e = -1$ it runs the pieces from the first one, that is $\pi$ in order. For an entrance it first runs the copies of $C_j$ in the order $\pi$, then the pieces after $J_j$. By Lemma 2(b), the items after $J_j$ in $\pi$ are the items above $e$ that are not in $C_j$. So in both cases $P'$ runs $\pi_e$ in order, until a branch $B$ leaves the trace. Then it runs the copies of $M_B$ in the order $\pi$ and jumps to $\mathrm{off}(B)$. By Lemma 2(c), $M_B$ has only items above $e$. If no branch leaves, it ends with the end item. Call the items that $P'$ runs in this region, in the order it runs them, the sequence $X$.

**Ideal values.** For an item $u > e$ and a name $x$ that $u$ reads, let $\mathrm{rw}(u, x)$ be the last writer of $x$ among the items $e+1, \dots, u-1$, or "the entrance" if there is none. Run the operations above $e$ in index order as straight-line code from a state $\sigma$, with a trapping operation giving the special value $\bot$, and with $\bot$ for any operation that reads $\bot$. This gives each operation $u$ its *ideal value* $\mathrm{val}_\sigma(u)$. The run of $P$ from $L_e$ computes exactly these values for the items it runs, because it runs them in index order.

## Lemma 3. The same writers

If $u$ is in $X$ and reads $x$, then the last item before $u$ in $X$ that writes $x$ is $\mathrm{rw}(u, x)$, or there is none if $\mathrm{rw}(u, x)$ is the entrance.

*Proof.* First, for two items $u < w$ in $X$ that conflict, $u$ is before $w$ in $X$. If both are in $\pi_e$ or both in $M_B$, this is Lemma 1(b), as both parts follow $\pi$. If $u \in M_B$ and $w$ is in the part of $\pi_e$ that runs, then $w \preceq B \prec u$, which is against Lemma 1(b). If $u$ runs in $\pi_e$ and $w \in M_B$, then $u$ is before $w$ in $X$ anyway.

Next, $w = \mathrm{rw}(u, x)$ is in $X$ before $u$. If $u$ runs in the part of $\pi_e$, then $w \prec u$ by Lemma 1(b), and $w > e$, so $w$ runs before $u$. If $u \in M_B$, then $w < u < B$. Either $w \prec B$ and $w$ ran in $\pi_e$, or $w \in M_B$ and $w \prec u$.

Last, take any other writer $w'$ of $x$ in $X$. If $w' < w$, it is before $w$ by the first step. No writer lies strictly between $w$ and $u$ in index order. If $w' > u$, it conflicts with $u$ and so is after $u$. So $w$ is the last writer before $u$. If $\mathrm{rw}(u, x)$ is the entrance, every writer of $x$ in $X$ is above $u$, so after $u$. $\square$

## Lemma 4. The same values

Let $\sigma$ and $\sigma'$ agree on $\mathrm{live}(L_e)$. Run $P$ from $L_e$ with $\sigma$, and $P'$ from $L_e$ with $\sigma'$. Then every item in $X$ reads the same values as in the ideal run from $\sigma$, and every operation in $X$ that does not trap computes $\mathrm{val}_\sigma(u)$.

*Proof.* By induction along $X$. Take $u$ and a name $x$ that it reads. If $\mathrm{rw}(u, x) = w$, then by Lemma 3, $u$ reads the value that $w$ computed in $X$, which is $\mathrm{val}_\sigma(w)$ by induction. ($w$ did not trap, or the run would have stopped.) If $\mathrm{rw}(u, x)$ is the entrance, $u$ reads $\sigma'(x)$. The trace path from $L_e$ to the block of $u$ reads $x$ at $u$ with no write before, so $x \in \mathrm{live}(L_e)$ and $\sigma'(x) = \sigma(x)$. In both cases $u$ reads the ideal value. $\square$

## Lemma 5. One region

Under the hypothesis of Lemma 4, exactly one of these holds.

1. Both runs trap in the region.
2. Both leave at the same branch $B$ to $\mathrm{off}(B)$, with states that agree on $\mathrm{live}(\mathrm{off}(B))$.
3. Both reach the end item. If it is `ret a`, both return the same value. Otherwise both go to the same successor of $b_k$, with states that agree on its live set.

*Proof.* There are three cases for the run of $P$.

*$P$ leaves at a branch $B^*$ without a trap.* The items of $\pi_e$ that $P'$ meets before $B^*$ are of three kinds. Branches: by Lemma 2(a) they are the branches below $B^*$ in index order. They read the ideal values by Lemma 4, the same as in $P$, so they stay on the trace. Operations below $B^*$: $P$ ran them without a trap, and they compute the same values. Operations above $B^*$ that are before $B^*$ in $\pi$: they cannot trap, by Lemma 2(d). So $P'$ reaches $B^*$, leaves the trace, and runs $M_{B^*}$, whose operations are below $B^*$ and do not trap. The items that $P'$ ran are all the items $e+1, \dots, B^*$ and the set $S = \{v > B^* : v \prec B^*\}$ of operations. Take $x \in \mathrm{live}(\mathrm{off}(B^*))$. By Lemma 2(d), no item of $S$ writes $x$. The writers of $x$ in $e+1, \dots, B^*$ run in index order (Lemma 3, first step), so the last one is the same as in $P$, and it computed the same value. If none of them writes $x$, then $x \in \mathrm{live}(L_e)$ and both states keep the entry value. This is case 2.

*$P$ reaches the end item without a trap.* The same argument with $B^*$ the end item. By (E4), $S$ is empty. The end item reads the same value. This is case 3.

*$P$ traps at an operation $o$, and every branch below $o$ stays on the trace.* Suppose that $P'$ does not trap in the region. Then it leaves at a branch $B$ or reaches the end item, and as above it ran every item from $e+1$ to $B$ (or to the end). The branches below $B$ stayed on the trace in $P'$ with the ideal values, so they also do so in $P$. $B$ left in $P'$, so it would leave in $P$ too. As $P$ trapped first, $o < B$. So $P'$ ran $o$, with the ideal values of its operands by Lemma 4, and these are the values with which $o$ traps in $P$. So $P'$ traps, which is a contradiction. This is case 1. $\square$

## Theorem 6. One step keeps the meaning

On every input, $P$ and $P'$ have the same outcome.

*Proof.* Call a label of $P$ *kept* if it is not on the trace, or it is $b_1$, or it is a $b_j$ with an entrance. Every kept label is a label of $P'$. We show, for every kept label $L$, that runs of $P$ and $P'$ from $L$ with states that agree on $\mathrm{live}(L)$ have the same outcome. We use induction on $L$ in reverse topological order of $P$.

If $L$ is not on the trace, $P'$ has the same block at $L$. Both runs compute the same values on the live names, trap together, and go to the same successor $L'$ with states that agree on $\mathrm{live}(L')$. $L'$ is kept: if $L' = b_j$ with $j \ge 2$, then $L$ is a predecessor other than $b_{j-1}$, so $b_j$ has an entrance. $L'$ comes after $L$ in the topological order, so the induction applies.

If $L$ is $b_1$ or an entrance label $b_j$, Lemma 5 applies. In case 1 both trap, and in case 3 with `ret` both return the same value. In case 2, $\mathrm{off}(B)$ for a branch of $b_i$ with $i \ge j$ is either off the trace, or it is some $b_m$. In the second case $m > i + 1$, because $m \le i$ would close a cycle and $m = i + 1$ is the trace target. Then $b_i$ is a predecessor of $b_m$ other than $b_{m-1}$, so $b_m$ has an entrance and is kept. $\mathrm{off}(B)$ comes after $b_i$, so after $L$, and the induction applies. Case 3 with a jump or a branch is the same.

The entry of $P$ is kept, because it is $b_1$ or off the trace, and it stays the entry of $P'$. Both runs start there with the same arguments. $\square$

## Lemma 7. The new program can go through the loop again

$P'$ has only `const`, `copy` and `op` instructions, and its graph is acyclic.

*Proof.* The copies are copies of operations. For the graph, give each block of $P'$ a key, and compare the keys first by the topological rank of a block of $P$, then by a number. Let $c_0, c_1, \dots$ be the cut items in $\pi$ (branches, entrances and the end item). By Lemma 2(a) and 2(b) they are in index order. Let $\beta(c)$ be the block of $P$ that holds $c$, where $\beta(J_j) = b_j$. The keys are:

- a block not on the trace: (its rank, 0);
- the piece that ends at $c_r$: $(\beta(c_r), r)$;
- the exit block of a branch of $b_i$: $(b_i, n + 1)$;
- the entrance block of $b_j$: $(b_j, -1)$.

Every edge of $P'$ goes to a larger key. From a piece to the next piece: the block does not go down, and the number goes up. From the piece of a branch of $b_i$ to its exit block: $r \le n$. From an exit block of $b_i$, or from the piece of a branch of $b_i$, to $\mathrm{off}(B)$: $\mathrm{off}(B)$ comes after $b_i$ in $P$, and its key has that block or a later one. From an entrance block $(b_j, -1)$ to the piece after $J_j$: that piece has a block at least $b_j$ and a number at least 0. From a block off the trace to $b_1$ or $b_j$: it comes before $b_j$ in $P$. From the last piece to a successor of $b_k$: the successor comes after $b_k$. So there is no cycle. $\square$

## Theorem 8. The loop stops

For a program $Q$ with a set $\mathrm{done}$ of scheduled blocks, let $p(c) = 1$ if $c$ is done or has no successor, and otherwise $p(c) = \sum_{s} p(s)$ over the successors $s$ of $c$. So $p(c)$ counts the paths from $c$ that stop at the first done block or at a `ret`. Let

$$\Phi = \sum_{c \text{ not done}} p(c).$$

$\Phi$ is a positive integer while some block is not done, and each step makes it smaller by at least 1. So the loop of line L1 stops after at most $\Phi$ steps of the input.

*Proof.* Write $p$ before the step and $p'$ after. The step removes $b_1, \dots, b_k$ from the blocks that are not done, marks the pieces done, and adds exit blocks and entrance blocks.

*Old blocks do not grow.* For a block $c$ off the trace, the edges into the trace now go to $b_1$ (a done piece, $p' = 1$) or to the label $b_j$ (a done piece, $p' = 1$, or an entrance block whose only successor is done, so $p' = 1$). Each of these has $p' = 1 \le p(b_j)$. By induction in reverse topological order, $p'(c) \le p(c)$.

*The exit blocks.* An exit block of $B$ has the one successor $\mathrm{off}(B)$, so its $p'$ is $p'(\mathrm{off}(B)) \le p(\mathrm{off}(B))$. Each path from $b_1$ leaves the trace at a first place: at a branch $B$ to $\mathrm{off}(B)$, or at the end of $b_k$. So $p(b_1) = \sum_B p(\mathrm{off}(B)) + E$, where $E \ge 1$ counts the paths that leave at the end ($E = 1$ if $b_k$ returns). So the exit blocks add at most $p(b_1) - 1$.

*The entrance blocks.* There are at most $k - 1$, and each has $p' = 1$.

*The removed blocks.* They had $\sum_i p(b_i) \ge p(b_1) + (k - 1)$.

So $\Phi' \le \Phi - p(b_1) - (k - 1) + (p(b_1) - 1) + (k - 1) = \Phi - 1$. $\square$

## Summary

Each step keeps the outcome (Theorem 6), keeps the input form (Lemma 7), and lowers $\Phi$ (Theorem 8). So TRACE-SCHEDULE stops, and its output has the same outcome as its input on every input. The bound $\Phi$ counts paths, so it can be exponential in the number of blocks. This proof does not bound the code growth any better.
