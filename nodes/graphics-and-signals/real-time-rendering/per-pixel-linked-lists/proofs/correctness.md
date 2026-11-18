---
title: The lists hold every kept fragment once, and the resolve is exact
proves: [correctness]
status: full
---

**Setting.** A frame has $f$ transparent fragments, each with a pixel $q$, and a pool of $n$ nodes. The atomic operations are linearizable: every ATOMIC-ADD on the counter and every ATOMIC-EXCHANGE on a head pointer takes effect at one point in time, and all of them form one total order consistent with each thread. Other writes of a thread (lines L4 and the write of the next field in line L5) touch only the node that the thread owns. At the start, the counter is 0 and every head is NULL (line L1). The resolve pass starts after every thread of the build pass has finished; on a GPU this is the barrier between the two passes.

**Lemma 1 (distinct nodes).** The ATOMIC-ADD calls return the values $0, 1, \dots, f - 1$, each to exactly one thread. A fragment is kept if and only if its value is below $n$, so exactly $\min(f, n)$ fragments are kept, each in its own node.

*Proof.* The calls are totally ordered. The $t$-th call in this order reads $t - 1$ and writes $t$, by induction on $t$, because no other operation writes the counter. Line L3 drops a fragment exactly when its value is at least $n$. $\square$

**Lemma 2 (shape of one list).** Fix a pixel $q$. Let $e_1, \dots, e_m$ be the exchanges on $\mathrm{head}[q]$ in their total order, with the node values $i_1, \dots, i_m$. Then $e_t$ returns $i_{t-1}$, with $i_0 = \mathrm{NULL}$. After the build pass, $\mathrm{head}[q] = i_m$ (or NULL if $m = 0$), and $\mathrm{next}[i_t] = i_{t-1}$ for every $t$.

*Proof.* Only exchanges at $q$ write $\mathrm{head}[q]$, and it starts as NULL. By induction, just before $e_t$ the head holds $i_{t-1}$, and $e_t$ returns this value and writes $i_t$. The thread that owns node $i_t$ writes the returned value into $\mathrm{next}[i_t]$, and no other thread writes that field, because the nodes are distinct by Lemma 1. When all threads have finished, every one of these writes has happened. $\square$

**Theorem 1 (the lists are complete).** After the build pass, the walk from $\mathrm{head}[q]$ visits $i_m, i_{m-1}, \dots, i_1$ and stops. So it visits exactly the kept fragments of pixel $q$, each once, in the reverse order of their exchanges.

*Proof.* By Lemma 2 the walk starts at $i_m$ and follows $\mathrm{next}[i_t] = i_{t-1}$ down to $i_0 = \mathrm{NULL}$, where line L7 stops. The values $i_t$ are distinct, so no node is visited twice. Every kept fragment of $q$ does one exchange at $q$, and dropped fragments do none. $\square$

The order of a list depends on the interleaving. The set of its nodes does not, when nothing is dropped.

**Theorem 2 (the resolve is exact).** If the pool is large enough ($f \le n$) and the depths of the fragments of each pixel are distinct, the resolve of pixel $q$ returns the composite in depth order $\sum_i c_i \prod_{j < i} (1 - \alpha_j) + C_0 \prod_i (1 - \alpha_i)$ of all fragments of $q$, for every interleaving of the build.

*Proof.* By Lemma 1 and Theorem 1, the walk collects all fragments of $q$. Insertion sort (line L8) puts them in increasing depth, which is unique because the depths are distinct. Line L9 folds $C \leftarrow c_j + (1 - \alpha_j) C$ from the farthest to the nearest, starting at $C_0$, which unrolls to the sum above. $\square$

With equal depths, the stable insertion sort keeps the list order, which depends on the timing, so the result for ties can change from frame to frame.

**Theorem 3 (overflow).** If $f > n$, the resolve returns, for each pixel, the exact composite of the kept fragments of that pixel. The kept fragments are those that won the first $n$ values of the counter, which depends on the interleaving.

*Proof.* Theorem 1 and the proof of Theorem 2 apply to the kept fragments. Lemma 1 says which they are. $\square$

**Theorem 4 (cost).** The build does $O(f)$ work and at most $2 f$ atomic operations. The resolve of a pixel with $k$ fragments does $O(k^2)$ comparisons in the worst case and $O(k)$ blends. The memory is $p$ head pointers, one counter and $n$ nodes.

*Proof.* Each thread does a constant number of steps. Insertion sort on $k$ items does at most $k (k - 1) / 2$ comparisons and moves. $\square$
