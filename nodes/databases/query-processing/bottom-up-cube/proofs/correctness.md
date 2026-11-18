---
title: BUC outputs each cell of the iceberg cube exactly once
proves: [correctness]
status: full
---

Number the dimensions $1, \ldots, D$. For a cell $c$, let $\text{fix}(c)$ be the set of dimensions $i$ with $c_i \ne \text{ALL}$, and let $R_c$ be the multiset of rows of $R$ that agree with $c$ on $\text{fix}(c)$. The iceberg cube is the set $\mathcal{I}$ of cells $c$ with $|R_c| \ge \text{minsup}$, each with the aggregates of $R_c$. We write $\max S$ for the largest element of a set $S$ of dimensions, with $\max \emptyset = 0$.

**Lemma (monotone count).** If $c'$ agrees with $c$ on $\text{fix}(c)$ and $\text{fix}(c) \subseteq \text{fix}(c')$, then $R_{c'} \subseteq R_c$, so $|R_{c'}| \le |R_c|$.

*Proof.* A row of $R_{c'}$ agrees with $c'$ on $\text{fix}(c')$, hence on $\text{fix}(c)$, where $c'$ and $c$ agree. $\square$

**Lemma (blocks).** At line L8, the range $X[i .. j - 1]$ holds exactly the rows of $X[lo .. hi - 1]$ whose value on dimension $d$ is $X[i].A_d$.

*Proof.* Line L5 sorts the range on $d$, so equal values of $A_d$ are adjacent. A call of line L10 for an earlier block only permutes the rows inside that block, so the rows after it are not moved, and the earlier blocks keep their sets of rows. The scan of line L8 starts at the first row of a run of equal values and stops at its end. $\square$

**Lemma (one call).** Consider a call $\text{BUC-REC}(lo, hi, d_0)$ where the global cell is $c$, $\max \text{fix}(c) < d_0$, $X[lo .. hi - 1]$ holds exactly $R_c$, and $|R_c| \ge \text{minsup}$. The call outputs exactly the cells $c'$ such that

1. $c'$ agrees with $c$ on $\text{fix}(c)$,
2. $\text{fix}(c') = \text{fix}(c) \cup T$ for some $T \subseteq \{d_0, \ldots, D\}$, and
3. $|R_{c'}| \ge \text{minsup}$,

each exactly once, with the aggregates of $R_{c'}$. When the call returns, the global cell is $c$ again and $X[lo .. hi - 1]$ holds the same multiset of rows.

*Proof.* By induction on $D - d_0$. Call the set of cells that satisfy 1 to 3 the target set of the call.

Line L3 outputs $c$ with the aggregates of $X[lo .. hi - 1] = R_c$. This is the target cell with $T = \emptyset$, which is in the target set by the assumption $|R_c| \ge \text{minsup}$.

Every other target cell $c'$ has a non-empty $T$, with a smallest element $d \ge d_0$. In the loop of line L4 at this $d$, let $v = c'_d$. Every row of $R_{c'}$ has $A_d = v$ and lies in $R_c$ by the monotone count lemma. So there is a block for $v$ at line L8, and by the blocks lemma it holds exactly $R_{c''}$, where $c''$ is $c$ with $c''_d = v$. Since $\text{fix}(c'') \subseteq \text{fix}(c')$ and they agree there, $|R_{c''}| \ge |R_{c'}| \ge \text{minsup}$, so line L9 makes the call $\text{BUC-REC}(i, j, d + 1)$ with the global cell $c''$. This call satisfies the assumptions of the lemma: $\max \text{fix}(c'') = d < d + 1$, its range holds $R_{c''}$, and $|R_{c''}| \ge \text{minsup}$. The cell $c'$ is in its target set, with $T \setminus \{d\} \subseteq \{d + 1, \ldots, D\}$. By induction, $c'$ is output in that call.

Conversely, every cell output by the call is either $c$ at line L3 or a cell output by an inner call at line L10 for some $d$ and $v$. By induction, such a cell agrees with $c''$ on $\text{fix}(c'')$, has $\text{fix} = \text{fix}(c'') \cup T'$ with $T' \subseteq \{d+1, \ldots, D\}$, and has enough rows. It is in the target set of the call, with $T = \{d\} \cup T'$.

Uniqueness: a target cell $c'$ with $T$ empty is $c$ and is output only at line L3, since every inner call outputs cells that fix one more dimension. A target cell with $T$ not empty is output only in the inner call for $d = \min T$ and $v = c'_d$: an inner call for another $d$ fixes $d$, and an inner call for another $v$ has a different value at $d$. That inner call outputs it once, by induction.

The cell is restored by the last assignment of line L10, and the range keeps its multiset because sorting and the inner calls only permute it. $\square$

**Theorem.** BUC outputs every cell of $\mathcal{I}$ exactly once, with its aggregates, and no other cell.

*Proof.* If $n < \text{minsup}$, then by the monotone count lemma every cell has $|R_c| \le n < \text{minsup}$, so $\mathcal{I}$ is empty, and line L2 makes no call. Otherwise, line L2 calls $\text{BUC-REC}(0, n, 1)$ with $c = (\text{ALL}, \ldots, \text{ALL})$, $\text{fix}(c) = \emptyset$, and $X$ holding $R = R_c$. The lemma applies with $d_0 = 1$, and its target set is $\mathcal{I}$, since every set of dimensions is a subset of $\{1, \ldots, D\}$. $\square$

**Sorting work.** With $\text{minsup} = 1$, the lemma shows that BUC makes one call for each non-empty cell. The call for a cell $c$ with $\text{fix}(c) = S$ sorts its $|R_c|$ rows once for each $d$ with $\max S < d \le D$, which is $D - \max S$ times. Each row lies in exactly one cell for each $S$. So each row is sorted $\sum_{S} (D - \max S)$ times. The sets with $\max S = k \ge 1$ number $2^{k-1}$, so the sum is $D + \sum_{k=1}^{D} 2^{k-1} (D - k) = D + (2^D - D - 1) = 2^D - 1$. For a larger $\text{minsup}$, the calls are a subset of these.
