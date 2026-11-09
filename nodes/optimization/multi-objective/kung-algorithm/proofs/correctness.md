---
title: Kung's algorithm returns the nondominated vectors within the stated time
proves: [correctness]
status: full
---

All objectives are minimized. The input $P$ is a set of $n$ distinct vectors of $\mathbb{R}^p$ with $p \ge 2$. We write $a \prec b$ when $a_j \le b_j$ for each $j$ and $a \ne b$. For $1 \le k \le p$ we write $a \sqsubseteq_k b$ when $a_j \le b_j$ for each $j = k, \ldots, p$. So $a \prec b$ is the same as $a \sqsubseteq_1 b$ and $a \ne b$.

**Specification of FILTER.** For finite sets $A$, $B$ and $1 \le k \le p$,

$$\mathrm{FILTER}(A, B, k) = \{\, b \in B : \text{no } a \in A \text{ has } a \sqsubseteq_k b \,\}.$$

The specification does not need any relation between $A$ and $B$ in the coordinates before $k$.

**Lemma 1 (the sweep).** Order $A \cup B$ by increasing $k$-th coordinate, with the vectors of $A$ before the vectors of $B$ when the $k$-th coordinates are equal, and any order inside a tie of the same set. For $a \in A$ and $b \in B$, $a$ comes before $b$ if and only if $a_k \le b_k$.

*Proof.* If $a_k < b_k$, the order puts $a$ first. If $a_k = b_k$, the tie rule puts $a$ first. If $a_k > b_k$, the order puts $b$ first. $\square$

**Lemma 2 (FILTER).** For all finite $A$, $B$ and $1 \le k \le p$, lines L6 to L14 return $\mathrm{FILTER}(A, B, k)$ as specified.

*Proof.* By induction on the pair $(p - k, |A| + |B|)$ in lexicographic order. Every call of lines L12 to L14 has a smaller pair, as shown below, so the induction is well founded and every call ends.

*Line L6.* If $A$ is empty, no $a$ exists and every $b$ is kept. If $B$ is empty, the answer is empty. Both cases return $B$.

*Line L7.* For $k = p$, $a \sqsubseteq_p b$ means $a_p \le b_p$. Some $a$ has it if and only if $\min_{a \in A} a_p \le b_p$. So $b$ is kept if and only if $b_p < \min_{a \in A} a_p$.

*Lines L8 to L10.* Here $k = p - 1$, so $a \sqsubseteq_k b$ means $a_k \le b_k$ and $a_{k+1} \le b_{k+1}$. By Lemma 1, the vectors of $A$ scanned before $b$ are exactly the $a \in A$ with $a_k \le b_k$. The value $m$ at the moment when $b$ is scanned is the least $(k+1)$-th coordinate among them, or $\infty$ if there are none. So some $a$ has $a \sqsubseteq_k b$ if and only if $m \le b_{k+1}$, and $b$ is kept if and only if $b_{k+1} < m$.

*Lines L11 to L14.* Here $k \le p - 2$, and both $A$ and $B$ are not empty, so $N = |A| + |B| \ge 2$. The lower half has $\lfloor N/2 \rfloor$ vectors and the upper half has $\lceil N/2 \rceil$, and both numbers are less than $N$. So the calls of lines L12 and L13 have a smaller second entry with the same $k$, and the call of line L14 has a smaller first entry $p - (k + 1)$. The induction hypothesis applies to all three.

Take $b \in B_{lo}$. Every $a \in A_{hi}$ comes after $b$ in the order of line L9, so by Lemma 1, $a_k > b_k$, and $a \not\sqsubseteq_k b$. So some $a \in A$ has $a \sqsubseteq_k b$ if and only if some $a \in A_{lo}$ has it. By the hypothesis, line L12 keeps exactly these $b$, and they are returned unchanged.

Take $b \in B_{hi}$. Some $a \in A$ has $a \sqsubseteq_k b$ if and only if some $a \in A_{hi}$ has it or some $a \in A_{lo}$ has it. By the hypothesis, line L13 keeps exactly the $b \in B_{hi}$ with no such $a \in A_{hi}$. Every $a \in A_{lo}$ comes before $b$, so by Lemma 1, $a_k \le b_k$, and then $a \sqsubseteq_k b$ if and only if $a \sqsubseteq_{k+1} b$. By the hypothesis, the call of line L14 keeps exactly the $b \in B_{hi}'$ with no $a \in A_{lo}$ such that $a \sqsubseteq_{k+1} b$. Together, the $b \in B_{hi}$ in the result are exactly those with no $a \in A$ such that $a \sqsubseteq_k b$.

The union of the two parts is $\mathrm{FILTER}(A, B, k)$. $\square$

**Lemma 3 (the lexicographic order).** If $a \prec b$, then $a$ comes before $b$ in the lexicographic order.

*Proof.* Since $a \ne b$, let $j$ be the first coordinate where they differ. Then $a_j \le b_j$ and $a_j \ne b_j$, so $a_j < b_j$, and the vectors agree before $j$. $\square$

**Lemma 4 (minimal dominators).** If some $a \in T$ dominates $b$, then some nondominated vector of $T$ dominates $b$.

*Proof.* The relation $\prec$ is irreflexive and transitive. The set $D = \{a \in T : a \prec b\}$ is finite and not empty, so it has an element $a^*$ that no element of $D$ dominates. If some $z \in T$ had $z \prec a^*$, then $z \prec b$ by transitivity, so $z \in D$, which is not possible. So $a^*$ is nondominated in $T$. $\square$

**Lemma 5 (FRONT).** If $S$ is not empty and sorted lexicographically, $\mathrm{FRONT}(S)$ returns $\min S$, the set of nondominated vectors of $S$.

*Proof.* By induction on $|S|$. For $|S| = 1$, line L2 returns $S = \min S$. Let $|S| \ge 2$. Then $T$ and $B$ are not empty and have fewer vectors than $S$, so by the hypothesis $R_T = \min T$ and $R_B = \min B$.

Take $t \in T$. Every $b \in B$ comes after $t$ in the lexicographic order, so by Lemma 3, $b \not\prec t$. So $t \in \min S$ if and only if $t \in \min T = R_T$.

Take $b \in B$. Then $b \in \min S$ if and only if no vector of $B$ dominates it and no vector of $T$ dominates it. The first part means $b \in R_B$. By Lemma 4, the second part means that no $a \in R_T$ dominates $b$. For $a \in R_T$ and $b \in R_B$, $a$ comes before $b$, so $a_1 \le b_1$, and the vectors are distinct. So $a \prec b$ if and only if $a_j \le b_j$ for all $j \ge 2$, that is, $a \sqsubseteq_2 b$. By Lemma 2, $\mathrm{FILTER}(R_T, R_B, 2)$ is exactly the set of $b \in R_B$ that no $a \in R_T$ dominates.

So line L5 returns $\min S$. $\blacksquare$

**Theorem (correctness).** For a nonempty set $P$ of distinct vectors of $\mathbb{R}^p$ with $p \ge 2$, $\mathrm{KUNG}(P)$ returns $\min P$.

*Proof.* Line L1 sorts $P$ and calls FRONT, which returns $\min P$ by Lemma 5. Copies are handled outside: if $P$ has copies, run the algorithm on one copy of each vector. A copy of $b$ is dominated by exactly the vectors that dominate $b$, so a copy is in the answer exactly when $b$ is. $\blacksquare$

## The time bound

Each set is kept as $p$ lists: one in lexicographic order and one sorted by each coordinate $j = 2, \ldots, p$. A call of FILTER at coordinate $k$ uses the lists of coordinates $k, \ldots, p$.

**Lemma 6 (linear steps).** With $N = |A| + |B|$ and $d = p - k + 1$, each of the following takes $O(d N)$ time: line L7; the merge of the lists of $A$ and $B$ sorted by coordinate $k$ into the order of line L9; the sweep of lines L9 and L10; the split of line L11 into sorted lists for the four parts; and the removal of the vectors that a call has found dominated from the lists of its caller. The split of line L3 into sorted lists for $T$ and $B$ takes $O(p |S|)$ time.

*Proof.* Two sorted lists merge in linear time, with $A$ first on ties. The sweep looks at each vector once. To split, mark the vectors of the lower half and then copy each sorted list into two lists by one pass, which keeps the order. The removal is one pass over each list with a mark for removed vectors. $\square$

**Theorem (time).** Let $T_d(N)$ be the worst time of FILTER with $d = p - k + 1$ coordinates left and $|A| + |B| = N$, and let $F(n)$ be the worst time of FRONT on $n$ vectors. Then $T_1(N) = O(N)$, $T_2(N) = O(N)$, $T_d(N) = O(N \log^{d-2} N)$ for $d \ge 3$ and $N \ge 2$, $F(n) = O(n \log n)$ for $p \in \{2, 3\}$, and $F(n) = O(n \log^{p-2} n)$ for $p \ge 4$. With the sort of line L1, the whole algorithm takes $O(p n \log n + F(n))$. The constants depend on $p$.

*Proof.* For $d = 1$ and $d = 2$, Lemma 6 gives linear time. For $d \ge 3$, lines L12 and L13 work on the two halves, line L14 works on at most $N$ vectors with $d - 1$ coordinates, and the rest is $O(d N)$ by Lemma 6. Since the worst time does not decrease with $N$,

$$T_d(N) \le T_d(\lceil N/2 \rceil) + T_d(\lfloor N/2 \rfloor) + T_{d-1}(N) + c\, d N.$$

Assume $T_{d-1}(N) \le C_{d-1} N \log^{d-3} N$ for $N \ge 2$, which holds for $d = 3$ by the linear bound. Unroll the recursion. At depth $i$ the sizes add up to $N$, each size is at most $N$, and there are at most $\lceil \log_2 N \rceil + 1$ levels. The cost at each level is at most $(C_{d-1} \log^{d-3} N + c d) N$. So $T_d(N) \le (\lceil \log_2 N \rceil + 1)(C_{d-1} \log^{d-3} N + c d) N = O(N \log^{d-2} N)$.

At the top, FRONT calls FILTER with $k = 2$, so with $d = p - 1$ coordinates, on at most $n$ vectors:

$$F(n) \le F(\lfloor n/2 \rfloor) + F(\lceil n/2 \rceil) + T_{p-1}(n) + c\, p\, n.$$

The same unrolling gives $F(n) = O(\log n \cdot (T_{p-1}(n) + p n))$, where $T_{p-1}(n)$ stands for the bound at size $n$. For $p = 2$ and $p = 3$, $T_{p-1}(n) = O(n)$, so $F(n) = O(n \log n)$. For $p \ge 4$, $T_{p-1}(n) = O(n \log^{p-3} n)$, so $F(n) = O(n \log^{p-2} n)$. The sort of line L1 makes $p$ sorted lists in $O(p n \log n)$ time. $\blacksquare$
