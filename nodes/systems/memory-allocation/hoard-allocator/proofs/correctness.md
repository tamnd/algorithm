---
title: Hoard hands out each block once, keeps its invariant after every free, and bounds memory
proves: [correctness]
status: full
---

We prove the claims for MALLOC (lines L1 to L8) and FREE (lines L9 to L14) of the page, with the loop at L13. Heaps $1, \ldots, P$ belong to processors and heap 0 is the global heap. All superblocks have $S$ bytes, and a block of class $c$ has $c$ bytes, with $c$ dividing $S$.

**Lemma 1 (each block in one place).** At every moment each block of each superblock is either on the free list of its superblock or handed out to exactly one caller, and $s.u$ equals $c$ times the number of handed-out blocks of $s$.

*Proof.* A new superblock has all its blocks on its free list and $s.u = 0$. Line L7 removes one block from the list, hands it out, and adds $c$ to $s.u$. Line L11 takes back a block that is handed out (a valid free) and puts it on the list, and subtracts $c$. A move at L5 or L14 changes only the owner. An empty superblock that is reused for a new class at L5 has no handed-out block, so its list can be rebuilt. No other line touches lists. $\square$

**Lemma 2 (counters).** For every heap $i$, $u_i = \sum s.u$ and $a_i = S \cdot |\{s\}|$ over the superblocks $s$ owned by $i$.

*Proof.* Each line that changes $s.u$ or the owner of $s$ changes $u$ and $a$ of the owner heaps by the same amounts: L7 and L11 change $s.u$ and $u_i$ by $c$; L5, L6 and L14 move or add a superblock and change $u$ and $a$ of both heaps by $s.u$ and $S$. $\square$

**Lemma 3 (the loop).** The loop at L13 and L14 stops, each move takes a superblock that is at least $f$ empty, and when it stops heap $i$ satisfies the invariant $u_i \ge a_i - KS$ or $u_i \ge (1-f)a_i$.

*Proof.* While the condition at L13 holds, $u_i < (1-f) a_i$ and $u_i \ge 0$, so $a_i > 0$ and heap $i$ owns $a_i / S \ge 1$ superblocks. By Lemma 2 their average $s.u$ is $u_i S / a_i < (1-f)S$, so the emptiest one has $s.u < (1-f)S$: it is more than $f$ empty. Each move lowers $a_i$ by $S$; the loop runs at most $a_i/S$ times, because at $a_i = 0$ the condition $u_i < (1-f)a_i = 0$ is false. When the loop stops, its condition is false, which is the invariant. $\square$

**Theorem 1 (safety).** No block is handed out to two callers at once, and a block handed out to a thread $t$ lies in a superblock owned, at that moment, by the heap of $t$.

*Proof.* The first part is Lemma 1. For the second, L7 takes the block from $s$, and $s$ was chosen at L3 among the superblocks of heap $i$, or moved to heap $i$ at L5, or created for heap $i$ at L6. $\square$

**Theorem 2 (memory with one size class).** Assume all blocks have one class. Then at every moment, for every processor heap,

$$a_i \le \frac{u_i}{1-f} + (K+1) S, \tag{W}$$

and the memory taken from the system for superblocks is at most $U/(1-f) + P(K+1)S$, where $U$ is the largest value of $u_0 + u_1 + \cdots + u_P$ so far.

*Proof.* We show (W) by induction over the calls; it holds at the start, with $a_i = u_i = 0$.

- A FREE on heap $i \ge 1$ ends, by Lemma 3, with $u_i \ge a_i - KS$ or $u_i \ge (1-f)a_i$. In both cases $a_i \le \max(u_i + KS,\ u_i/(1-f)) \le u_i/(1-f) + KS$, which implies (W). A FREE on another heap does not change heap $i$.
- A MALLOC that uses a superblock at L3 raises $u_i$ and keeps $a_i$, so (W) stays true.
- A MALLOC that reaches L5 or L6 found no free block in heap $i$, and with one class this means every superblock of heap $i$ is full: $u_i = a_i$ before the call. After it, $a_i$ grew by $S$ and $u_i$ by at least $c > 0$, so $a_i \le u_i + S$, which implies (W).

For the second claim, the system memory grows only at L6. With one class, a superblock in heap 0 always has a free block: it entered heap 0 at L14 while more than $f$ empty, and heap 0 never allocates from it. So L6 runs only when heap 0 holds no superblock, and then the system memory equals $a_1 + \cdots + a_P$ after the call. By (W) this is at most $\sum_i u_i/(1-f) + P(K+1)S \le U/(1-f) + P(K+1)S$. Between two runs of L6 the system memory does not change and $U$ does not decrease. $\square$

With several size classes, a superblock of one class in heap 0 cannot serve a request of another class unless it is empty, and a malloc at L5 or L6 can happen while heap $i$ has free blocks of other classes, so (W) can fail. The paper states Theorem 1, $A(t) = O(U(t) + P)$, for a constant number of classes; this note proves only the case of one class. The test of the model checks (W), the system bound, Lemmas 1 and 2 and Theorem 1 after every call on random traces. $\blacksquare$
