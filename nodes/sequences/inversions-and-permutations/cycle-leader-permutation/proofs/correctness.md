---
title: APPLY and APPLY-READONLY move every item to its target and restore P
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $P$ be a permutation of $[n]$, let $A_0$ be the array on entry, and let the goal be the array $A'$ with $A'[P[i]] = A_0[i]$ for every $i$, equivalently $A'[m] = A_0[P^{-1}(m)]$. For an index $i$ write $C(i) = \{i, P(i), P^2(i), \ldots\}$ for its cycle and $\ell(i) = |C(i)|$, so $P^{\ell(i)}(i) = i$ and the indices $i, P(i), \ldots, P^{\ell(i)-1}(i)$ are distinct. Write $|P[j]|$ for the value of the entry of $P$ at $j$ ignoring its sign.

**Lemma 1 (one cycle).** Suppose the cycle walk of lines L3 to L7 starts at $i$ when $A[m] = A_0[m]$ for every $m \in C(i)$ and when $|P[j]| = P(j)$ for every $j$. Then it ends after $\ell(i) - 1$ rounds of the loop at line L4, with $A[m] = A'[m]$ for every $m \in C(i)$, with $A$ unchanged outside $C(i)$, and with the entries of $P$ on $C(i)$ negated and all other entries unchanged.

*Proof.* We claim that before round $t$ of the loop, for $1 \le t \le \ell(i)$, we have $j = P^t(i)$, $x = A_0[P^{t-1}(i)]$, $A[P^s(i)] = A'[P^s(i)]$ and $P[P^s(i)] < 0$ for $1 \le s < t$, and every other entry of $A$ and $P$ on $C(i)$ is as on entry. For $t = 1$, line L3 sets $x = A_0[i]$ and $j = P(i)$, and nothing else has changed. Suppose the claim holds before round $t$ and $j = P^t(i) \ne i$, so $t < \ell(i)$ and $j$ has not been written yet. Line L5 stores $x = A_0[P^{t-1}(i)]$ at $j = P(P^{t-1}(i))$, which is $A'[j]$ by the definition of $A'$, and sets $x$ to the old content $A_0[j] = A_0[P^t(i)]$. Line L6 reads $k = P[j] = P^{t+1}(i)$, still positive since $j$ was not marked, negates $P[j]$ and sets $j = P^{t+1}(i)$. So the claim holds before round $t + 1$. The loop stops at the first $t$ with $P^t(i) = i$, which is $t = \ell(i)$. Then $x = A_0[P^{\ell(i)-1}(i)] = A_0[P^{-1}(i)]$, which line L7 writes to $A[i]$, so $A[i] = A'[i]$, and line L7 negates $P[i]$. Every index of $C(i)$ has now been written once and negated once, and nothing outside $C(i)$ was read for writing or changed. $\square$

**Lemma 2 (APPLY).** Before iteration $i$ of line L1, the cycles that contain an index smaller than $i$ are exactly the cycles whose entries of $P$ are all negative, they hold their final items, and every other cycle holds its original items and has all its entries of $P$ positive.

*Proof.* By induction on $i$. Before $i = 1$ nothing is marked and nothing has moved. At iteration $i$, if $C(i)$ contains an index smaller than $i$ then by the hypothesis its entries, including $P[i]$, are negative, line L2 skips it, and the statement holds for $i + 1$. Otherwise $i$ is the smallest index of $C(i)$, the hypothesis says that $C(i)$ holds its original items with positive entries, and the absolute values of all entries equal $P$. Lemma 1 then finishes $C(i)$ and marks it, without touching the other cycles. In both cases the cycles with an index smaller than $i + 1$ are exactly the finished, negated ones. $\square$

**Theorem 1.** APPLY returns $A'$ and leaves $P$ unchanged.

*Proof.* After the last iteration of line L1, Lemma 2 with $i = n + 1$ says every cycle is finished, so $A = A'$, and every entry of $P$ is negative with absolute value $P(j)$. Line L8 negates every entry once, which restores $P$. $\square$

**Lemma 3 (leader test).** At iteration $i$ of line L10, line L11 ends with $j = i$ exactly when $i = \min C(i)$.

*Proof.* The walk visits $P(i), P^2(i), \ldots$ and stops at the first visited index that is at most $i$. Such an index exists, since $P^{\ell(i)}(i) = i$, so the walk stops after at most $\ell(i)$ steps. If $i = \min C(i)$, every index visited before returning to $i$ is larger than $i$, so the walk stops at $i$. If some index of $C(i)$ is smaller than $i$, the walk meets one of them before it can come back to $i$, since it passes through every element of $C(i)$ before $P^{\ell(i)}(i) = i$, and stops there with $j < i$. $\square$

**Theorem 2.** APPLY-READONLY returns $A'$ and does not write $P$.

*Proof.* Line L14 is the walk of Lemma 1 without the marks. The argument of Lemma 1 does not use the signs except to keep $P[j]$ readable, so a walk started at $i$ when $C(i)$ holds its original items finishes $C(i)$ and changes nothing else. By Lemma 3, each cycle is walked exactly once, at its smallest index, and at that moment no index of it has been written, because the only walks so far started at the leaders of other cycles. So at the end every cycle is finished and $A = A'$. No line writes $P$. $\square$

**Termination.** Each walk of line L4 or line L14 stops after $\ell(i) - 1$ rounds by Lemma 1, each walk of line L11 after at most $\ell(i)$ steps by Lemma 3, and the loops at lines L1, L8 and L10 run $n$ times. So both procedures halt, APPLY after $O(n)$ steps in total, since the rounds of line L4 over all cycles add up to $\sum_C (|C| - 1) = n - c$, where $c$ is the number of cycles. $\blacksquare$
