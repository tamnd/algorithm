---
title: A counting Bloom filter has no false negatives
proves: [correctness, invariant, termination]
status: full
---

Write $C_t$ for the counter array after the first $t$ operations and $S_t$ for the multiset of keys that are stored after them. The hash functions are fixed by line L2. For a key $x$ and a position $j$ let $a_j(x) = |\{i : h_i(x) = j\}|$, the number of times $x$ uses position $j$. Let $N_j(t) = \sum_{x} \mathrm{mult}_{S_t}(x)\, a_j(x)$. Assume that each DELETE$(x)$ is applied only when $x$ has a copy in $S_t$. Each loop has $k$ rounds and each round is a constant number of steps, so each operation ends.

**Lemma 1 (stuck counters stay stuck).** If $C_t[j] = c_{\max}$, then $C_{t'}[j] = c_{\max}$ for each $t' \ge t$.

*Proof.* Only lines L4 and L6 write a counter, and both write only when the counter is below $c_{\max}$. $\square$

**Lemma 2 (invariant (C)).** For each $t$ and $j$, either $C_t[j] = N_j(t)$ and $C_s[j] < c_{\max}$ for each $s \le t$, or $C_t[j] = c_{\max}$.

*Proof.* By induction on $t$. At $t = 0$, line L1 gives $C_0[j] = 0 = N_j(0)$, and $0 < c_{\max}$ since $c \ge 1$. Assume the claim at $t$ and look at operation $t + 1$ and a fixed position $j$.

A QUERY changes neither $C$ nor $S$. If $C_t[j] = c_{\max}$, then $C_{t+1}[j] = c_{\max}$ by Lemma 1. So assume that $C_t[j] = N_j(t) < c_{\max}$ and that the counter was never at $c_{\max}$.

*INSERT$(x)$.* Then $N_j(t+1) = N_j(t) + a_j(x)$. The loop of line L4 visits position $j$ exactly $a_j(x)$ times. Each visit adds 1 while the counter is below $c_{\max}$. If the counter stays below $c_{\max}$ through all the visits, then $C_{t+1}[j] = N_j(t) + a_j(x) = N_j(t+1)$, and it was never at $c_{\max}$. Otherwise it reaches $c_{\max}$ at some visit, and by Lemma 1 it ends at $c_{\max}$.

*DELETE$(x)$.* Then $N_j(t+1) = N_j(t) - a_j(x)$, and $N_j(t+1) \ge 0$ because $S_{t+1}$ is a multiset. The loop of line L6 visits position $j$ exactly $a_j(x)$ times, and each visit subtracts 1 since the counter is below $c_{\max}$. So $C_{t+1}[j] = N_j(t) - a_j(x) = N_j(t+1) \ge 0$, and it never reaches $c_{\max}$ on the way down. $\square$

**Theorem.** After any sequence of operations that respects the precondition of DELETE, QUERY$(x)$ returns true for each $x$ with a copy in $S_t$. QUERY$(x)$ returns true exactly when $C_t[h_i(x)] > 0$ for each $i$.

*Proof.* Lines L7 and L8 return false at the first $i$ with $C[h_i(x)] = 0$, and line L9 returns true if there is none. This gives the second claim. Let $x$ have a copy in $S_t$ and let $j = h_i(x)$. Then $a_j(x) \ge 1$, so $N_j(t) \ge 1$. By Lemma 2 either $C_t[j] = N_j(t) \ge 1$ or $C_t[j] = c_{\max} \ge 1$. So no counter of $x$ is 0, and the query returns true. $\square$

**Remark (the precondition).** If DELETE$(y)$ is applied to a $y$ with no copy in $S$, the step $N_j(t+1) \ge 0$ of Lemma 2 fails. For example, let $x$ and $y$ share position $j$ with $C[j] = 1$ from $x$ alone; then DELETE$(y)$ sets $C[j] = 0$ and QUERY$(x)$ returns false. So the precondition cannot be removed. $\blacksquare$
