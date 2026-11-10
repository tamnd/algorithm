---
title: The checker returns the least consistent cut on which every local predicate holds, or none if there is no such cut
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page. $Q_i$ starts as the list, in order, of the clocks $V(s)$ of the states $s$ of $p_i$ with $l_i(s)$ true. For a vector $v$ in $Q_i$ we write $a(v) = v[i]$, the index of its state. A *solution* is a tuple $(v_0, \dots, v_{n-1})$ with $v_i$ in the original $Q_i$ such that the cut $(a(v_0), \dots, a(v_{n-1}))$ is consistent. By the vector clock test of the page on [consistent cuts](/consistent-cut/), this holds if and only if $v_j[i] \le v_i[i]$ for all $i \ne j$.

**Lemma 1 (clocks grow along a process).** If $v$ comes before $w$ in $Q_j$, then $v \le w$ in every entry.

*Proof.* $v$ and $w$ are the clocks of two states of $p_j$, and the vector clock of a later event of a process is at least that of an earlier one in every entry. $\square$

**Lemma 2 (dropped heads are in no solution).** At every moment, every solution $(v_0, \dots, v_{n-1})$ has each $v_k$ in the current $Q_k$, at or after its head.

*Proof.* By induction on the steps of the checker. At the start the queues are full. Suppose the claim holds before line L3 drops $h_i = \mathrm{head}(Q_i)$, because $h_j = \mathrm{head}(Q_j)$ has $h_j[i] > h_i[i]$. Take any solution. By the induction hypothesis $v_j$ is at or after $h_j$, so by Lemma 1, $v_j[i] \ge h_j[i] > h_i[i]$. Since the solution is consistent, $v_j[i] \le v_i[i]$, so $v_i[i] > h_i[i]$ and $v_i \ne h_i$. As $v_i$ is at or after $h_i$, it is after $h_i$, so it is still in $Q_i$ after the drop. Line L5 is the same with $i$ and $j$ swapped. $\square$

**Corollary 1.** If line L4, or the same test after line L5, finds an empty queue, there is no solution.

*Proof.* By Lemma 2, a solution would have an entry in that queue. $\square$

**Lemma 3 (invariant of the work list).** Whenever control is at the top of the `while` loop, every two processes $i \ne j$ that are both outside `todo` have compatible heads: $\mathrm{head}(Q_j)[i] \le \mathrm{head}(Q_i)[i]$ and $\mathrm{head}(Q_i)[j] \le \mathrm{head}(Q_j)[j]$.

*Proof.* At the start every process is in `todo`. A head changes only at lines L3 and L5, and both put the changed process into `todo`, so a change never breaks the claim for a pair outside `todo`. A process leaves `todo` only when it is taken as $i$. If the loop over $j$ stops at line L3, $i$ goes back into `todo`. Otherwise the loop tests $i$ against every $j$. Line L2 did not fire, so $\mathrm{head}(Q_j)[i] \le \mathrm{head}(Q_i)[i]$. Either line L5 did not fire, so the other inequality holds too, or it dropped the head of $j$ and put $j$ in `todo`. During the loop the head of $i$ does not change, and the head of $j$ changes only in the test of $j$ itself. So at the end of the loop every $j$ outside `todo` has a head compatible with the head of $i$. $\square$

**Theorem 1 (correctness).** If the checker returns none, there is no solution. If it returns the cut $c$ at line L6, then $c$ is consistent, $l_i$ holds in the state $s_i^{c_i}$ for every $i$, and $c \le c'$ in every entry for the cut $c'$ of every solution.

*Proof.* The first claim is Corollary 1. At line L6, `todo` is empty, so by Lemma 3 all heads are pairwise compatible, which is the consistency test; and each head is a vector of $Q_i$, so $l_i$ holds in its state. By Lemma 2, every solution has $v_i$ at or after $\mathrm{head}(Q_i)$, so $c'_i = v_i[i] \ge \mathrm{head}(Q_i)[i] = c_i$ by Lemma 1. $\square$

**Theorem 2 (cost).** The checker makes at most $2n(n-1)m$ comparisons, where $m$ is the largest length of a queue.

*Proof.* Each time a process is taken from `todo`, the loop over $j$ makes at most two comparisons for each of the $n - 1$ other processes. Process $i$ is in `todo` once at the start, and it is put back only when its head is dropped and it is not already there. A drop that empties $Q_i$ ends the run, so $i$ is put back at most $|Q_i| - 1$ times, and it is taken at most $|Q_i| \le m$ times. Summing over the $n$ processes gives the bound. The run ends, since there are at most $nm$ takes. $\square$
