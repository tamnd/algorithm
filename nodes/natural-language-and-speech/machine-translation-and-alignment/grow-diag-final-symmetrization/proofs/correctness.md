---
title: Grow-diag-final terminates, stays between the intersection and the union, and aligns every word that either direction aligns
proves: [correctness]
status: full
---

Let $A_1, A_2 \subseteq \{1, \ldots, m\} \times \{1, \ldots, l\}$ be the two link sets, with links $(j, i)$, and let $I = A_1 \cap A_2$ and $U = A_1 \cup A_2$. Let $A$ be the working set of GROW-DIAG-FINAL. A source word $j$ is *aligned* in $A$ if some $(j, i) \in A$, and a target word $i$ likewise. The procedure only adds links; it never removes one.

**Lemma 1 (bounds).** At every moment, $I \subseteq A \subseteq U$.

*Proof.* Line L1 sets $A = I \subseteq U$. Line L8 adds a link only if it is in $U$. Line L12 adds a link only if it is in $A_1$ or in $A_2$, so in $U$. Nothing is removed, so $I \subseteq A$ stays true. $\square$

**Lemma 2 (termination).** The loop of lines L2 to L9 runs at most $|U \setminus I| + 1$ times, and the whole procedure ends.

*Proof.* Every pass of the loop that does not stop sets *added*, so it adds at least one new link (line L8 tests $p \in U$ and that one of its words is unaligned, so $p \notin A$: if $p$ were in $A$, both of its words would be aligned). By Lemma 1, $A$ can grow at most $|U \setminus I|$ times. The final pass adds nothing and stops. Lines L10 to L12 are two finite loops. $\square$

If $A_1$ and $A_2$ come from two one-directional alignments (each source word has at most one link in $A_1$, and each target word at most one in $A_2$), then $|U| \le m + l$, so there are at most $m + l + 1$ passes.

**Lemma 3 (the grown set is closed).** When the loop of lines L2 to L9 stops, there is no link $(j, i) \in A$ and neighbour offset $(\Delta i, \Delta j)$ in the list of line L6 such that $p = (j + \Delta j, i + \Delta i) \in U$ and $p$ has an unaligned word in $A$.

*Proof.* The last pass adds nothing, so $A$ does not change during it. That pass visits every cell $(j, i)$ at lines L4 and L5, and for each $(j, i) \in A$ it tests every neighbour at line L8. If some neighbour $p$ were in $U$ with an unaligned word, line L8 would add it, a contradiction. $\square$

**Lemma 4 (coverage).** After line L12 has run for $B = A_1$, every word that has a link in $A_1$ is aligned in $A$. After it has run for $B = A_2$ too, every word that has a link in $U$ is aligned in $A$.

*Proof.* Let $(j, i) \in A_1$. When lines L11 and L12 reach $(j, i)$ in the pass for $A_1$, either $j$ or $i$ is unaligned, and line L12 adds $(j, i)$, so both are aligned; or both are aligned already. In both cases $j$ and $i$ are aligned after that step, and they stay aligned because links are never removed. The same holds for $A_2$ in the second pass, and the words aligned after the first pass stay aligned. $\square$

**Theorem.** GROW-DIAG-FINAL ends and returns $A$ with $I \subseteq A \subseteq U$, such that the set after line L9 is closed in the sense of Lemma 3, and every word with a link in $A_1 \cup A_2$ is aligned in $A$.

*Proof.* Lemmas 1 to 4. $\square$

**Remarks.**

1. *The result depends on the order.* Lemma 3 says the grown set is closed, but there can be several closed sets between $I$ and $U$, and the order in which lines L4 to L8 visit cells and neighbours picks one of them. For $m = 4$, $l = 3$, $A_1$ from $a = (3, 2, 1, 1)$ and $A_2$ from $b = (4, 4, 1)$, the target-outer order of line L4 adds $(4, 2)$, and the source-outer order does not. So the procedure is a function of the stated order, not of the two sets alone; this page follows the Moses pseudocode. The same holds for the final step: lines L10 to L12 use $A_1$ before $A_2$.
2. *The variant with "and".* If line L12 asks for both words to be unaligned (grow-diag-final-and), Lemma 1 still holds but Lemma 4 does not: a link whose source word is aligned and whose target word is not is never added in the final step, so its target word can stay unaligned. The result is also not always a subset of the grow-diag-final result, because a link added by the final step of grow-diag-final can block another one.
3. *No objective.* None of these statements says that the result is a good alignment. The procedure is a heuristic, and its value is measured.
4. *Cost.* Each pass of the loop costs $O(8 m l)$ with the alignment status of each word kept in arrays, and the final step costs $O(m l)$. With Lemma 2, the total time is $O(m l (|U \setminus I| + 1))$, which is $O(m l (m + l))$ for one-directional inputs.
