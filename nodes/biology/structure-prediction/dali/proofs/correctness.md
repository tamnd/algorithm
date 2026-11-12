---
title: DALI returns a sequential alignment, its true score, and a local optimum of the search moves
proves: [correctness]
status: full
---

DALI is a heuristic, so the claim is not that it finds the maximum of the elastic score. The claim is about what it returns. We use the notation of the page: $A = (a_1, \ldots, a_n)$ and $B = (b_1, \ldots, b_m)$, the fragment length $w$, the candidate list $C$ of line L2, and the elastic score $S(M) = \sum_{p \in M} \sum_{p' \in M} \phi(p, p')$.

An alignment is sequential if it is a set of pairs $(i, j)$ whose first parts are distinct, whose second parts are distinct, and in which $i < i'$ holds exactly when $j < j'$. Call two pairs $p = (i, j)$ and $q = (i', j')$ compatible if $i \ne i'$, $j \ne j'$, and $(i < i') = (j < j')$. A set of pairs is sequential exactly when each two of its pairs are compatible; sorted by $i$, such a set is strictly increasing in $j$ as well.

**Claim.** DALI$(A, B)$ returns a pair $(s, M)$ such that (1) $M$ is a sequential alignment; (2) $s = S(M)$; (3) if $C$ is not empty, $s \ge S(F)$ for each of the seed fragments $F$ of line L4, and no single move of the refinement, the addition of one candidate fragment of $C$ or the deletion of one segment of $M$, raises $S$ by more than the tolerance $\varepsilon = 10^{-12}$ from the final state of the trajectory that gave $M$; (4) the algorithm stops.

**Lemma 1 (the add move keeps the alignment sequential).** Let $M$ be sequential and $F = \{(i + k, j + k) : 0 \le k < w\}$ a fragment. Then $M' = \{p \in M : p \text{ is compatible with each } q \in F\} \cup F$ is sequential.

*Proof.* Two pairs of $F$ are compatible, since $(i + k, j + k)$ and $(i + k', j + k')$ differ in both parts and $k < k'$ holds in both. Two kept pairs of $M$ are compatible because $M$ is sequential. A kept pair and a pair of $F$ are compatible by the filter. So each two pairs of $M'$ are compatible. $\square$

**Lemma 2 (the delete move keeps the alignment sequential).** Each subset of a sequential alignment is sequential, because compatibility is a condition on two pairs at a time. $\square$

**Proof of (1).** Each state of the Monte Carlo run starts as a seed fragment, which is sequential, and changes only by the two moves of line L7, which keep it sequential by Lemmas 1 and 2. A rejected move leaves the state as it is. The refinement of line L11 uses the same two moves. The returned $M$ is either one of these states or the empty set, which is sequential. $\square$

**Proof of (2).** The value stored with each state is computed by the elastic score function from the state itself, at line L5 for the seed (as the score of the fragment in line L2), at line L8 for each accepted move, and in the refinement for each accepted move. Lines L9, L11 and L12 copy a state together with its value. The function computes $S$ exactly: it adds $\theta^E$ for each of the $|M|$ diagonal terms, and $2\phi(p, p')$ once for each unordered pair $\{p, p'\}$, which covers the two ordered terms $\phi(p, p')$ and $\phi(p', p)$, equal because $|a_i - a_{i'}| = |a_{i'} - a_i|$ and $|b_j - b_{j'}| = |b_{j'} - b_j|$. If $C$ is empty, the loop of line L4 does not run, and the result is $(0, \emptyset)$, with $S(\emptyset) = 0$. $\square$

**Proof of (3).** For a seed $F$, the trajectory best $s_F$ starts at $S(F)$ and line L9 only raises it. The refinement only accepts moves that raise the value, so its result is at least $s_F \ge S(F)$, and line L12 keeps the largest result over the seeds. The refinement stops only after a pass in which no candidate addition raised the value by more than $\varepsilon$ and no segment deletion did either. Its last state is the $M$ of that trajectory. $\square$

**Proof of (4).** The Monte Carlo loop has a fixed number of steps for each of at most a fixed number of seeds. In the refinement each accepted move raises $S$ by more than $\varepsilon > 0$. There are finitely many sequential alignments, so $S$ takes finitely many values, and it can rise only finitely many times. Each pass that accepts nothing ends the loop, and each pass is finite. $\blacksquare$

**Remark.** The search is a Metropolis chain with an acceptance probability $\min(1, e^{\beta \Delta S})$ and a rising $\beta$, as in simulated annealing. Nothing here bounds the gap between $s$ and the true maximum of $S$; the tests compare $s$ with an exhaustive search on small inputs, where it is never above the maximum and equal to it in most cases.
