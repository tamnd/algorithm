---
title: Strand sort returns the items in sorted order, and it is stable
proves: [correctness]
status: full
---

We write $A_j$ for the list $A$ at the start of round $j$ of the loop of line L2, $S_j$ for the strand of round $j$, and $R_j$ for $R$ after round $j$, with $R_0$ empty and $A_1$ the input.

**Lemma 1 (one round).** $S_j$ is non-decreasing. Each item of $A_j$ goes to exactly one of $S_j$ and $U$, and each of the two lists keeps the order of $A_j$.

*Proof.* Line L3 puts $A_j[0]$ in $S_j$. The loop of line L4 visits each other item once, in order, and appends it to the end of $U$ (line L5) or of $S_j$ (line L6). An item goes to $S_j$ only when it is not less than the last item of $S_j$, so $S_j$ stays non-decreasing. $\square$

**Lemma 2 (MERGE).** For two sorted lists $X$ and $Y$, MERGE$(X, Y)$ returns a sorted list of the items of $X$ and $Y$. It keeps the order of the items of $X$, and of the items of $Y$, and on a tie it puts the item of $X$ first.

This is the merge of the [merging-sorted-lists](/merging-sorted-lists/) page, with the rule to take the front item of $X$ unless the front item of $Y$ is smaller.

**Theorem 1.** STRAND-SORT$(A)$ stops and returns the items of $A$ in sorted order.

*Proof.* Invariant: before round $j$, $R_{j-1}$ is sorted, and $R_{j-1}$ and $A_j$ together hold the items of the input. It holds for $j = 1$. If it holds before round $j$, then by Lemma 1, $S_j$ is sorted and $S_j$ and $A_{j+1} = U$ together hold the items of $A_j$; by Lemma 2, $R_j$ is sorted and holds the items of $R_{j-1}$ and $S_j$. So the invariant holds before round $j + 1$. Each round moves $A_j[0]$ into $S_j$, so $|A_{j+1}| < |A_j|$, and the loop stops after at most $n$ rounds, with $A$ empty. Then $R$ is sorted and holds all the items. $\blacksquare$

**Theorem 2 (stability).** If $y$ and $z$ have equal keys and $y$ comes before $z$ in the input, then $y$ comes before $z$ in the output.

*Proof.* Let $y$ be in strand $S_a$ and $z$ in strand $S_b$.

First, $a \le b$. Suppose $b < a$. In round $b$, both $y$ and $z$ are in $A_b$, and by Lemma 1 the earlier rounds kept the input order, so $y$ comes before $z$ in $A_b$. So $y$ is not $A_b[0]$, because $A_b[0]$ goes to $S_b$. The scan visits $y$ before $z$ and sends $y$ to $U$, so at that moment $y < \text{last}(S_b)$. The last item of $S_b$ never decreases during the scan, and $z$ has the key of $y$, so when $z$ is visited, $z < \text{last}(S_b)$ and $z$ goes to $U$ too. This contradicts $z \in S_b$.

If $a = b$, then $y$ is before $z$ in $S_a$ by Lemma 1, and the merges keep the order of the items of each input list (Lemma 2), so $y$ stays before $z$.

If $a < b$, then $y$ is in $R_{b-1}$ when $S_b$ is merged. By Lemma 2, on equal keys the item of $R_{b-1}$ comes first, and any item between them in $R_{b-1}$ is also kept in order. So $y$ comes before $z$ in $R_b$, and the later merges keep the order of the items of $R$. $\blacksquare$

**The number of strands.** Let $k$ be the number of rounds. Two items of a strictly decreasing subsequence of the input cannot be in the same strand: they keep their order in $A_j$, and a strand is non-decreasing. So $k$ is at least the length of each strictly decreasing subsequence. Conversely, for $j > 1$ each item $x$ of $S_j$ was in $A_{j-1}$ and went to $U$, so it was visited after an item $w$ of $S_{j-1}$ with $x < w$, and $w$ comes before $x$ in the input. Starting from an item of $S_k$ and following these items back to $S_1$ gives $k$ items, each earlier in the input and larger than the next. So the longest strictly decreasing subsequence has length exactly $k$.
