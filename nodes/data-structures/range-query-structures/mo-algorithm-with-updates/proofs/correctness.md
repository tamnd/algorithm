---
title: Mo's algorithm with updates returns the answer of each query on the array of its time
proves: [correctness, termination]
status: full
---

Let $A_0$ be the original array and $A_j$ the array after the updates $1, \ldots, j$, where update $j$ sets position $p_j$ to $x_j$. A query $(l, r, t)$ asks for $f$ of the multiset $W(l, r, t) = \{A_t[k] : l \le k < r\}$. The state of the window is a function of the multiset of values passed to ADD and not yet passed to REMOVE.

**Invariant.** Between any two steps, (I1) the working array $A$ equals $A_T$; (I2) for each $j \le T$, $U[j] = (p_j, A_{j-1}[p_j])$, and for each $j > T$, $U[j] = (p_j, x_j)$; (I3) the state holds the multiset $\{A[k] : L \le k < R\}$.

At the start, $T = 0$, $A = A_0$, every $U[j] = (p_j, x_j)$, and the window is empty, so the invariant holds.

**Lemma 1 (forward step).** If the invariant holds with $T = j - 1$, then $T \leftarrow j$ followed by APPLY$(j)$ keeps it.

*Proof.* By (I2), $U[j] = (p_j, x_j)$. Line L12 sets $A[p_j] = x_j$, so $A = A_j$ by (I1), and stores the old value $A_{j-1}[p_j]$ in $U[j]$, which is (I2) for $T = j$. If $L \le p_j < R$, the multiset of the window loses $A_{j-1}[p_j]$ at line L11 and gains $A_j[p_j]$ at line L13, and no other position changes, so (I3) holds; otherwise the window multiset is unchanged, and so is the state. $\square$

**Lemma 2 (backward step).** If the invariant holds with $T = j$, then APPLY$(j)$ followed by $T \leftarrow j - 1$ keeps it.

*Proof.* By (I2), $U[j] = (p_j, A_{j-1}[p_j])$, and by (I1) $A = A_j$, which differs from $A_{j-1}$ only at $p_j$. Line L12 writes $A_{j-1}[p_j]$ into $A[p_j]$, so $A = A_{j-1}$, and stores $A_j[p_j] = x_j$ in $U[j]$, which is (I2) for $T = j - 1$. The window part is as in Lemma 1. $\square$

**Lemma 3 (window step).** Each single move of $L$ or $R$ in line L7, as in Mo's algorithm, keeps (I3), and lines L5 to L7 do not change $A$ except through APPLY.

*Proof.* A move adds or removes one position $k$ of the window and calls ADD$(A[k])$ or REMOVE$(A[k])$ with the current array value, which is the change of the multiset. Lines L4 to L7 of plain Mo's algorithm add before they remove, so $L \le R$ throughout and each removed position is in the window. $\square$

**Theorem.** For each query $(l, r, t)$, the recorded answer is $f(W(l, r, t))$, and the algorithm terminates.

*Proof.* Lines L5 and L6 change $T$ by one per step towards $t$, each by Lemma 1 or Lemma 2, so after them $T = t$ and $A = A_t$. Line L7 moves $L$ to $l$ and $R$ to $r$ by Lemma 3. Then (I3) says the state holds $W(l, r, t)$, and line L8 records $f$ of it. Every loop moves an integer pointer one step towards a fixed target, so each ends, and there are $q$ queries. $\square$
