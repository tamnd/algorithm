---
title: A Bloom filter has no false negatives
proves: [correctness, invariant, termination]
status: full
---

Write $B_t$ for the bit array after the first $t$ operations, and $S_t$ for the set of keys inserted by them. The hash functions $h_1, \ldots, h_k$ are fixed by line L2 and do not change. Let $P(x) = \{h_1(x), \ldots, h_k(x)\}$ be the set of positions of a key $x$.

**Lemma 1 (bits only rise).** For each $t$ and each position $j$, if $B_t[j] = 1$ then $B_{t+1}[j] = 1$.

*Proof.* A QUERY writes nothing. An INSERT writes only in line L4, and it writes the value 1. So no operation changes a 1 to a 0. $\square$

**Lemma 2 (invariant (B)).** For each $t$, each $x \in S_t$ and each $j \in P(x)$, $B_t[j] = 1$.

*Proof.* By induction on $t$. For $t = 0$, line L1 makes all bits 0, and $S_0 = \emptyset$, so the claim holds with nothing to check. Assume the claim for $t$. If operation $t + 1$ is a QUERY, then $S_{t+1} = S_t$ and $B_{t+1} = B_t$, so the claim holds. If it is INSERT$(y)$, then $S_{t+1} = S_t \cup \{y\}$. For $x \in S_t$ and $j \in P(x)$ we have $B_t[j] = 1$ by the hypothesis, so $B_{t+1}[j] = 1$ by Lemma 1. For $x = y$, the loop of lines L3 and L4 runs for $i = 1, \ldots, k$ and sets $B[h_i(y)] = 1$ for each $i$, so each $j \in P(y)$ is 1 after the loop. A later round of the same loop writes only the value 1, so it does not undo an earlier round. $\square$

**Theorem.** After any sequence of operations, QUERY$(x)$ returns true for each inserted key $x$. If QUERY$(x)$ returns false, then $x$ was never inserted. QUERY$(x)$ returns true exactly when $B[j] = 1$ for each $j \in P(x)$.

*Proof.* The loop of lines L5 and L6 reads $B[h_i(x)]$ for $i = 1, 2, \ldots$ and returns false at the first $i$ with $B[h_i(x)] = 0$. If there is no such $i$, it ends after $k$ rounds and line L7 returns true. So QUERY returns true exactly when each position of $P(x)$ holds a 1. If $x \in S_t$, Lemma 2 says that each position of $P(x)$ holds a 1, so the query returns true. The second claim is the contrapositive of the first. $\square$

**Union.** Let $B$ and $B'$ be the arrays for the sets $S$ and $S'$, built with the same $m$ and the same hash functions from an all-zero array. By Lemma 1 and line L4, position $j$ is 1 in $B$ exactly when $j \in \bigcup_{x \in S} P(x)$, because no other position is ever written. So $B[j] \lor B'[j] = 1$ exactly when $j \in \bigcup_{x \in S \cup S'} P(x)$, which is the array that inserting $S \cup S'$ gives.

**Termination.** Each loop of lines L3 and L5 has at most $k$ rounds, and each round does one hash evaluation and one access to the array. $\blacksquare$
