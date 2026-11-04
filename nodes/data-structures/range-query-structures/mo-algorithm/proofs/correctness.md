---
title: Mo's algorithm returns the value of each query range
proves: [correctness, termination]
status: full
---

Let $A[0 \ldots n-1]$ be the array and $Q_0, \ldots, Q_{q-1}$ the queries, with $Q_j = (l_j, r_j)$ and $0 \le l_j \le r_j \le n$. Write $W(L, R)$ for the multiset $\{A[L], \ldots, A[R-1]\}$. The holes satisfy the contract: if $S$ is the state of $W(L, R)$, then ADD$(L - 1)$ makes it the state of $W(L - 1, R)$ for $L \ge 1$, ADD$(R)$ makes it the state of $W(L, R + 1)$ for $R < n$, REMOVE$(L)$ makes it the state of $W(L + 1, R)$ for $L < R$, REMOVE$(R - 1)$ makes it the state of $W(L, R - 1)$ for $L < R$, and ANSWER returns $f(W(L, R))$.

**Invariant (I).** Before each round of line L3 and after each step of lines L4 to L7, $0 \le L \le R \le n$ and $S$ is the state of $W(L, R)$.

**Lemma 1.** (I) holds before the first round.

*Proof.* Line L2 sets $L = R = 0$ and the state of the empty window, which is $W(0, 0)$. $\square$

**Lemma 2.** If (I) holds at the start of a round for the query $(l, r)$, then it holds after each step of lines L4 to L7, every call of ADD and REMOVE meets the contract, and at the end $L = l$ and $R = r$.

*Proof.* Let $(L_0, R_0)$ be the window at the start.

Line L4 runs while $L > l$. Each step has $L \ge 1$ because $L > l \ge 0$, sets $L \leftarrow L - 1$ and calls ADD on the new $L$, which is the item that enters on the left. $L$ stays at most $R$ because it decreases. The loop stops with $L = \min(L_0, l)$.

Line L5 runs while $R < r$. Each step has $R < r \le n$, calls ADD$(R)$, the item that enters on the right, and sets $R \leftarrow R + 1$. The loop stops with $R = \max(R_0, r)$.

Now $L \le l$ and $R \ge r$. Line L6 runs while $L < l$. During this loop $L < l \le r \le R$, so $L < R$ and REMOVE$(L)$ meets the contract; then $L \leftarrow L + 1 \le l \le R$. The loop stops with $L = l$.

Line L7 runs while $R > r$. During this loop $R > r \ge l = L$, so $L < R$, the step sets $R \leftarrow R - 1$ and REMOVE removes $A[R]$, the last item of the old window, and $R \ge r \ge L$ afterwards. The loop stops with $R = r$.

Each step keeps (I) by the contract of the hole it calls. $\square$

**Theorem 1 (correctness).** For each $j$, $\mathrm{ans}[j] = f(A[l_j \ldots r_j - 1])$.

*Proof.* Line L1 lists every index $j$ exactly once, because it sorts a permutation. By Lemma 1 and Lemma 2, by induction over the rounds, (I) holds at line L8 of the round of $j$ with $[L, R) = [l_j, r_j)$. So ANSWER returns $f(W(l_j, r_j))$, and line L8 stores it at index $j$. Later rounds write only other indices. $\square$

**Theorem 2 (termination).** The algorithm stops after a finite number of calls of ADD and REMOVE.

*Proof.* Each of the four loops of a round changes one end by one step towards a fixed target and stops when the target is reached, so a round makes at most $|L_0 - l| + |R_0 - r| + |l - L_0| + |r - R_0| \le 4n$ calls. There are $q$ rounds. $\square$

**Remark (the order of the loops).** The proof of Lemma 2 uses that lines L4 and L5 run before lines L6 and L7. If the left end shrinks first, for example from $[0, 2)$ to the query $[5, 8)$, then $L$ passes $R$, and REMOVE is called on items that are not in the window, which breaks the contract.
