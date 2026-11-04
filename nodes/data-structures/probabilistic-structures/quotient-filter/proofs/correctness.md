---
title: A quotient filter finds each stored fingerprint
proves: [correctness, invariant, termination]
status: full
---

All slot indices are modulo $m$, and "between", "before" and "after" are taken in the cyclic order that starts at the first slot of the cluster in question. Invariant (Q) of the page is assumed in the following precise form. The stored pairs (quotient, remainder) are the multiset $\Phi$ of the fingerprints of $S$. Each cluster, with first slot $c$ and slots $c, c+1, \ldots, e - 1$ before the empty slot $e$, is split into runs $[s_0, s_1), [s_1, s_2), \ldots, [s_{t-1}, s_t)$ with $s_0 = c$ and $s_t = e$. The occupied slots among $c, \ldots, e-1$ are $Q_0 = c < Q_1 < \cdots < Q_{t-1}$, run $k$ holds the remainders of quotient $Q_k$ in sorted order, and $Q_k \le s_k$. The first slot of a run has `continuation` = 0 and the others have 1, `shifted[p]` = 1 exactly when slot $p$ holds a remainder whose quotient is not $p$, and empty slots have all three bits 0.

**Lemma 1.** If `occupied[Q]` = 1, then slot $Q$ is non-empty and lies in the cluster that holds the run of $Q$.

*Proof.* `occupied[Q]` = 1 only for a slot $Q = Q_k$ of some cluster, by the form of the invariant. $\square$

**Lemma 2.** If slot $p$ is non-empty and `shifted[p]` = 0, then $p = Q_k = s_k$ for some run $k$ of its cluster.

*Proof.* Slot $p$ lies in some run $k$, so it holds a remainder of quotient $Q_k$, and `shifted[p]` = 0 gives $Q_k = p$. The run starts at $s_k \ge Q_k = p$ and contains $p$, so $s_k \le p$. $\square$

**Lemma 3 (line L2).** If `occupied[f_q]` = 1, the loop of line L2 ends at a slot $b$ of the cluster of $f_q$, at or before $f_q$, with $b = Q_j = s_j$ for some $j$.

*Proof.* By Lemma 1 the walk starts at a non-empty slot of the cluster. If `shifted[p]` = 1, then $p$ is not the first slot $c$ of the cluster, since $c = s_0 = Q_0$ holds a remainder of quotient $c$. So $p - 1$ is in the same cluster. The walk moves left inside the cluster and stops at the latest at $c$, which is unshifted. Lemma 2 gives the form of $b$. $\square$

**Lemma 4 (lines L4 to L6).** Let $f_q = Q_l$. The loop keeps $b = Q_i$ and $s = s_i$ for some $i \le l$, and ends with $i = l$.

*Proof.* By Lemma 3 this holds at the start with $i = j \le l$. Suppose $b = Q_i \ne f_q$, so $i < l$. Line L5 moves $s$ to the next slot with `continuation` = 0. The slots $s_i + 1, \ldots, s_{i+1} - 1$ are continuations of run $i$, and $s_{i+1}$ is the first slot of run $i + 1$, which exists since $i + 1 \le l < t$; so $s$ becomes $s_{i+1}$. Line L6 moves $b$ to the next occupied slot, which is $Q_{i+1}$, because no slot strictly between $Q_i$ and $Q_{i+1}$ is occupied. So the claim holds for $i + 1$. The index $i$ grows by 1 in each round and is at most $l$, so the loop ends, with $i = l$. $\square$

**Theorem 1 (query).** QUERY$(x)$ returns true exactly when the fingerprint $(f_q, f_r)$ of $x$ is in $\Phi$. So it returns true for each key of $S$, and each query ends.

*Proof.* If `occupied[f_q]` = 0, no stored pair has quotient $f_q$ and line L1 returns false. Otherwise, by Lemma 4, lines L7 to L10 start at $s_l$, the first slot of the run of $f_q$. They read slots $s_l, s_l + 1, \ldots$ and stop at the first later slot with `continuation` = 0, which is $s_{l+1}$, either the start of the next run or the empty slot $e$. So they compare $f_r$ with exactly the remainders of quotient $f_q$. $\square$

**Lemma 5 (decoding).** Let $b = Q_j = s_j$ in a cluster ending before the empty slot $e$. The slots $b, \ldots, e - 1$ hold exactly the runs $j, \ldots, t - 1$, and the occupied slots among them are $Q_j, \ldots, Q_{t-1}$, in the same order. No run of another quotient, and no other occupied bit, lies in these slots.

*Proof.* The runs are consecutive and $s_j = b$, $s_t = e$. The occupied slots of the cluster from $b$ on are $Q_j, \ldots, Q_{t-1}$, because $Q_j = b$ and the $Q_k$ increase. $\square$

So line L12 reads back the pairs of runs $j$ to $t - 1$: the $k$-th slot with `continuation` = 0 from $b$ starts the run of the $k$-th occupied slot from $b$.

**Theorem 2 (insert and delete keep the invariant).** Assume at most $m - 2$ stored fingerprints before an insert. After INSERT$(x)$ the stored multiset is $\Phi + \{F(x)\}$, and after DELETE$(x)$ for a present fingerprint it is $\Phi - \{F(x)\}$, and in both cases the invariant holds.

*Proof.* Let $b$ be the slot of line L11 or L15. If slot $f_q$ is empty, then $b = f_q$ and $E$ is empty. Otherwise slot $f_q$ is non-empty, and by the argument of Lemma 3 the walk ends at a slot $b = Q_j = s_j$ of the same cluster, at or before $f_q$; by Lemma 5 the list $E$ is the multiset of the pairs stored in slots $b$ to $e - 1$, and all their quotients are between $b$ and $e - 1$. In both cases $f_q$ is between $b$ and $e$.

Line L14 or L17 clears the old slots $b, \ldots, e - 1$ and writes the new list $E'$ greedily: the runs in increasing order of quotient, from $b$, each run at the later of its quotient and the slot after the previous run, with the bits set as in the invariant. The pairs outside $[b, e)$ are unchanged, so the stored multiset changes by exactly the added or removed pair.

*The new runs stay in place.* For a delete, removing a pair moves each greedy run start left or leaves it, so the new runs lie inside $[b, e)$. For an insert, adding one pair moves each greedy run start right by at most 1, so the new runs lie inside $[b, e]$. Slot $e$ was empty, and the slot after it either is empty or starts a cluster whose first run starts at its own quotient; neither changes, so no two runs overlap. There is still an empty slot, since at most $m - 1$ pairs are stored.

*The invariant holds.* Runs before $b$ end before $b$ and are unchanged. In the rewritten area, the greedy rule puts each run at or after its quotient and right after the previous run unless there is a gap; after a gap, the run starts at its own quotient, which makes it the first run of a new cluster with $s_0 = Q_0$. If the area now ends at $e$ and touches the next cluster, the two join; the runs of the next cluster start at or after their quotients and follow in increasing order, so the joined cluster satisfies the invariant. The occupied bits of the slots $b, \ldots, e$ are rewritten from $E'$, and by Lemma 5 no other quotient had its occupied bit there. $\blacksquare$
