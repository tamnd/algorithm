---
title: An LWW-Register returns the write with the largest stamp in its causal history and is a CRDT
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas with distinct ids from a totally ordered set, and $\bot$ is below every id. Replica $i$ runs the main block with state $(\mathit{stamp}_i, \mathit{value}_i)$. In one step a replica runs WRITE (lines L3 and L4), sends a copy of its state, or runs MERGE (lines L5 and L6) on a copy that some replica sent earlier. Copies may be lost, merged more than once and merged in any order. Stamps are compared in lexicographic order.

**Histories.** The causal history $C_i$ is a set of write events. A write at $i$ adds an event $w$ with stamp $s(w)$ and value $v(w)$, the values set on line L4. A MERGE at $i$ of a copy sent when the sender had history $H$ sets $C_i \leftarrow C_i \cup H$.

**Claim 1 (invariant).** At every time and for every $i$: if $C_i$ is empty, the state is $((0, \bot), v_0)$; otherwise $\mathit{stamp}_i = \max\{s(w) : w \in C_i\}$ and $\mathit{value}_i = v(w)$ for the write $w$ with that stamp. A copy in transit satisfies the same with its history.

*Proof.* By induction on the steps, with Claim 2 below used for uniqueness. At the start $C_i$ is empty. A copy is the state and history of its sender at one time. For WRITE at $i$, line L3 sets $c$ to the counter of $\mathit{stamp}_i$ plus 1, so the new stamp $(c, i)$ is larger than $\mathit{stamp}_i$, which by the hypothesis is the largest stamp in $C_i$ (or $(0, \bot)$). The new event therefore has the largest stamp in the new history, and line L4 stores its stamp and value. For MERGE of a copy $(s', v', H)$, by the hypothesis $s'$ is the largest stamp in $H$ (or $(0, \bot)$ if $H$ is empty), and the largest stamp in $C_i \cup H$ is the larger of the two maxima. Lines L5 and L6 keep the state with the larger stamp. If the stamps are equal, both states describe the same write, by Claim 2, or both are initial, so keeping the current state is right. $\square$

**Claim 2 (unique stamps).** Two different write events have different stamps.

*Proof.* Two writes at different replicas have different ids in their stamps. Two writes at the same replica $i$: by Claim 1 for the earlier time, the later write reads a stamp at least as large as the stamp of the earlier one, which is in $C_i$, so its counter is larger. $\square$

**Theorem 1 (safety).** READ at $i$ returns the value of the write with the largest stamp in $C_i$, or $v_0$ if there is none. If a write $w$ is in the causal history of the replica that makes a write $w'$ at the time of $w'$, then $s(w) < s(w')$, so stamps are consistent with causality.

*Proof.* Line L2 returns $\mathit{value}_i$, and Claim 1 gives the first part. For the second, $w'$ gets a stamp larger than $\mathit{stamp}_i$, which is at least $s(w)$ by Claim 1. $\square$

**Theorem 2 (semilattice).** Let the states be the pairs $(s, v)$ that occur in runs, ordered by stamp. This order is total, and each stamp occurs with only one value, by Claim 2. So it is a chain, and a chain is a join-semilattice whose join is the larger element. MERGE computes the join, and WRITE is inflationary.

*Proof.* A total order is a join-semilattice: the least upper bound of two elements is the larger one. Hence the join is commutative, associative and idempotent. Lines L5 and L6 keep the state with the larger stamp, and with equal stamps the two states are equal. Line L4 sets a stamp larger than the current one. $\square$

**Theorem 3 (convergence).** If writes stop and every replica sends its state to every other replica infinitely often over fair-lossy channels, then there is a time after which every replica holds the write with the largest stamp of the whole run.

*Proof.* After the last write, each replica in the end merges a copy from every other replica sent after the last write, and then its history contains theirs. After finitely many merges every history holds all writes, and Claim 1 gives the result. $\square$

**Termination.** Every operation is a constant number of steps and stamp comparisons. $\blacksquare$
