---
title: Schroeppel-Shamir returns a subset with sum t exactly when one exists
proves: [correctness, termination]
status: full
---

**Notation.** Let $A, B, C, D$ be the four quarters of the positions, and let $L_A, L_B, L_C, L_D$ be the lists of line L1, with $L_B$ and $L_D$ sorted by sum after line L2. We write $L_X[i]$ also for the sum of the $i$-th entry. A *left entry* is a pair $(i, j)$ with value $\lambda(i, j) = L_A[i] + L_B[j]$. A *right entry* is a pair $(k, l)$ with value $\rho(k, l) = L_C[k] + L_D[l]$. Let $\mathcal{L}$ and $\mathcal{R}$ be the sets of all left and right entries. An entry is *used* when it has been popped from its heap, and *unused* otherwise. Let $U_1 \subseteq \mathcal{L}$ and $U_2 \subseteq \mathcal{R}$ be the unused entries.

**Lemma 1 (subsets and pairs).** The map $S \mapsto \bigl((S \cap A, S \cap B), (S \cap C, S \cap D)\bigr)$ is a bijection from the subsets of $\{0, \ldots, n-1\}$ to $\mathcal{L} \times \mathcal{R}$, and $\sum_{p \in S} a_p = \lambda + \rho$ for the image $(\lambda, \rho)$.

*Proof.* The quarters partition the positions, so $S$ is the disjoint union of its four parts, and four subsets, one of each quarter, have exactly one union. The sum over $S$ is the sum of the sums over the four parts. $\square$

**Lemma 2 (invariant H).** Before each test of line L5:

1. For each $i$, there is $c_i \in \{0, \ldots, |L_B|\}$ such that the used left entries of row $i$ are exactly $(i, 0), \ldots, (i, c_i - 1)$, and $H_1$ holds the entry $(i, c_i)$ with its value if $c_i < |L_B|$, and no entry of row $i$ otherwise.
2. If $U_1 \neq \emptyset$, then $H_1 \neq \emptyset$, and its top has the smallest value in $U_1$.

The mirror statements hold for $H_2$: the used right entries of row $k$ are $(k, |L_D| - 1), \ldots, (k, d_k + 1)$, $H_2$ holds $(k, d_k)$ if $d_k \ge 0$, and its top has the largest value in $U_2$.

*Proof.* Part 1, initialization: line L3 puts $(i, 0)$ in $H_1$ for each $i$, and nothing is used, so $c_i = 0$. Maintenance: $H_1$ changes only in line L8. It pops the top $(i, j)$, which by part 1 is $(i, c_i)$. This entry becomes used, so $c_i$ grows by 1, and line L8 pushes $(i, c_i)$ when $c_i < |L_B|$. Other rows do not change.

Part 2: by part 1, the unused entries of row $i$ are $(i, c_i), \ldots, (i, |L_B| - 1)$. Since $L_B$ is sorted, $\lambda(i, c_i) \le \lambda(i, j)$ for each $j \ge c_i$. So the smallest value in $U_1$ is the smallest $\lambda(i, c_i)$ over the rows with $c_i < |L_B|$, which is the smallest value in $H_1$, which is its top. If $U_1 \neq \emptyset$, some row has $c_i < |L_B|$, and $H_1$ holds its entry.

The proof for $H_2$ is the same, with $L_D$ sorted, the cursor moving down from $|L_D| - 1$ in line L9, and "largest" for "smallest". $\square$

**Lemma 3 (invariant S).** Before each test of line L5: for each $u \in \mathcal{L}$ and $v \in \mathcal{R}$ with $\lambda(u) + \rho(v) = t$, both $u \in U_1$ and $v \in U_2$.

*Proof.* Initialization: nothing is used. Maintenance: suppose the invariant holds before a pass that does not return. Then $H_1$ and $H_2$ are not empty, and by Lemma 2 $s_1 = \min_{U_1} \lambda$ and $s_2 = \max_{U_2} \rho$.

- Case $s_1 + s_2 < t$ (line L8). The pass uses only the top $u_0$ of $H_1$, with $\lambda(u_0) = s_1$. Suppose $\lambda(u_0) + \rho(v) = t$ for some $v \in \mathcal{R}$. By the invariant, $v \in U_2$, so $\rho(v) \le s_2$ and $\lambda(u_0) + \rho(v) \le s_1 + s_2 < t$, a contradiction. So $u_0$ is in no pair with total $t$, and the invariant still holds after $u_0$ is used.
- Case $s_1 + s_2 > t$ (line L9). The pass uses only the top $v_0$ of $H_2$, with $\rho(v_0) = s_2$. If $\lambda(u) + \rho(v_0) = t$, then $u \in U_1$ by the invariant, so $\lambda(u) \ge s_1$ and $\lambda(u) + \rho(v_0) \ge s_1 + s_2 > t$, a contradiction. The invariant still holds. $\square$

**Lemma 4 (termination).** The loop of line L5 runs at most $|\mathcal{L}| + |\mathcal{R}| = 2^{|A| + |B|} + 2^{|C| + |D|}$ times.

*Proof.* Each pass that does not return pops one entry from a heap. By Lemma 2, part 1, an entry is pushed only when it is the next unused entry of its row, so each entry is pushed at most once and popped at most once. Each pass therefore reduces $|U_1| + |U_2|$ by exactly 1, and this quantity starts at $|\mathcal{L}| + |\mathcal{R}|$ and is never negative. $\square$

**Theorem.** SCHROEPPEL-SHAMIR$(a, t)$ stops. It returns a set $S$ with $\sum_{p \in S} a_p = t$ if such a set exists, and NONE otherwise.

*Proof.* The loop stops by Lemma 4, and lines L1 to L4 and each pass take finite time.

*A returned set is correct.* Line L7 returns only when $s_1 + s_2 = t$, where $s_1 = \lambda(i, j)$ and $s_2 = \rho(k, l)$. The returned set is the union of the subsets of entries $L_A[i], L_B[j], L_C[k], L_D[l]$, and by Lemma 1 its sum is $s_1 + s_2 = t$.

*NONE is correct.* Line L10 runs only when $H_1$ or $H_2$ is empty. By Lemma 2, part 2, and its mirror, $U_1 = \emptyset$ or $U_2 = \emptyset$. By Lemma 3, every pair $(u, v)$ with total $t$ has $u \in U_1$ and $v \in U_2$, so no such pair exists. By Lemma 1, no subset has sum $t$.

*If a solution exists, the algorithm returns one.* The algorithm leaves the loop either by line L7, which returns a correct set, or by line L10. Line L10 is reached only when no pair has total $t$, as shown above. So when a solution exists, line L10 is not reached, and by termination line L7 returns. $\blacksquare$
