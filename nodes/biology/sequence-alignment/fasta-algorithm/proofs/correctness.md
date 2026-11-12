---
title: The steps of FASTA are exact, and init1 ≤ opt ≤ SW
proves: [correctness]
status: full
---

FASTA is a heuristic, so we prove what each step computes and how the three scores relate. Line numbers refer to the pseudocode on the page. $\mathrm{SW}(q, y)$ is the best local alignment score of $q$ and $y$ under the same substitution scores and gap cost.

**Lemma 1 (line L1).** The lookup returns exactly the pairs $(i, j)$ with $q[i \ldots i+k-1] = y[j \ldots j+k-1]$.

*Proof.* The table maps each word $u$ of length $k$ to the list of all $i$ with $q[i \ldots i+k-1] = u$. For each $j$ the scan looks up $u = y[j \ldots j+k-1]$ and outputs $(i, j)$ for each $i$ in the list. So a pair is output if and only if the two words are equal. $\square$

**Lemma 2 (line L3).** For a region $(i_0, j_0, L, \cdot)$, rescoring returns a stretch $(i_0 + u, j_0 + u, v - u, \beta)$ with $0 \le u \le v \le L$ and $\beta = \max\left(0, \max_{0 \le u' < v' \le L} \sum_{t=u'}^{v'-1} s(q[i_0+t], y[j_0+t])\right)$.

*Proof.* This is Kadane's scan on the sequence $x_t = s(q[i_0+t], y[j_0+t])$. The invariant after step $t$ is: *run* is the largest sum of a stretch that ends at $t$, or 0 if all are at most 0, and *best* is the largest sum of a stretch inside $x_0, \ldots, x_t$, or 0. A stretch that ends at $t + 1$ either is $x_{t+1}$ alone or extends the best stretch that ends at $t$, so $\max(0, \text{run} + x_{t+1})$ keeps the first part of the invariant, and comparing it with *best* keeps the second. The recorded ends give a stretch with this sum. $\square$

**Lemma 3 (line L5).** Let the kept regions be sorted by start in $q$ and then in $y$. A *chain* is a sequence of regions $R_1, \ldots, R_t$ in which each $R_{u+1}$ starts after $R_u$ ends, in both $q$ and $y$. Its value is $\sum_u \text{score}(R_u) - (t - 1) \cdot \text{penalty}$. The join DP returns the largest value of a chain, or 0 if there are no regions.

*Proof.* In a chain, each region starts strictly later in $q$ than the one before, so the regions of a chain appear in the sorted order. Let $V(b)$ be the largest value of a chain that ends with region $b$. A chain ending with $b$ is $b$ alone, or a chain ending with some compatible $a$ before $b$ in the order, followed by $b$. So $V(b) = \max\left(\text{score}(b), \max_{a \to b} V(a) + \text{score}(b) - \text{penalty}\right)$, which is the update of the DP. By induction on the position of $b$ in the order, the DP computes $V(b)$ for each $b$, and the answer is $\max_b V(b)$. $\square$

**Lemma 4 (line L6).** Let $B$ be the set of cells $(i, j)$ with $|(j - i) - c| \le \text{width}/2$. The banded DP returns the largest score of a local alignment all of whose aligned and gap cells lie in $B$, or 0.

*Proof.* The DP is the Smith-Waterman recurrence $H(i, j) = \max(0, H(i-1, j-1) + s(q_i, y_j), H(i-1, j) - d, H(i, j-1) - d)$ for a linear gap cost $d$ per letter, with $H = -\infty$ outside $B$ and $H = 0$ on row 0 and column 0. By induction on $i + j$, $H(i, j)$ for a cell in $B$ is the best score of a local alignment that ends at $(i, j)$ and whose cells all lie in $B$: each such alignment either starts at $(i, j)$, which the diagonal term covers because $(i-1, j-1)$ is on the same diagonal and so is in $B$ or on row or column 0, where $H \ge 0$; or its last step comes from one of the three neighbors, and a neighbor outside $B$ contributes $-\infty$, which is the same as forbidding it. The answer is the maximum over all cells. $\square$

**Theorem.** For every pair $q, y$ with at least one ktup match:

1. $\text{init1} \le \text{initn}$.
2. $\text{init1} \le \text{opt} \le \mathrm{SW}(q, y)$.
3. If $B$ holds every cell of the table, $\text{opt} = \mathrm{SW}(q, y)$.

If there is no ktup match, all three scores are 0.

*Proof.* (1) The region with score init1 is a chain of one region, so by Lemma 3 initn is at least its score.

(2) The region that gives init1 is an ungapped stretch on diagonal $c$, the center of the band. Its cells all lie in $B$, so it is one of the local alignments of Lemma 4, and opt is at least its score $\text{init1}$. The banded DP maximizes over a subset of the local alignments that the full recurrence maximizes over, so $\text{opt} \le \mathrm{SW}(q, y)$.

(3) With every cell in $B$, the banded recurrence is the full Smith-Waterman recurrence.

With no match, line L2 has no region, and the program returns 0 for all three. $\blacksquare$

**What is not claimed.** There is no relation between initn and opt in general: initn uses a fixed penalty per join and opt uses the real gap cost, so either can be larger. And $\mathrm{SW}(q, y)$ can be positive when there is no ktup match, so the scores of FASTA can be 0 for a pair with a real local alignment.

**Termination.** Each step loops over finite sets: the words of $q$, the positions of $y$, at most ten regions, and the cells of the band.
