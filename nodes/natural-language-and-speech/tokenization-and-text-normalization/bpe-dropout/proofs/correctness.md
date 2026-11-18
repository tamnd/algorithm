---
title: BPE-dropout stops, returns a segmentation of the word, and has the law that the enumeration computes
proves: [correctness, termination]
status: full
---

Notation. The merge table is a list of pairs of strings; the rank of a pair is its position in the list, and a lower rank means a higher priority. A *segmentation* of a word $w$ is a list of nonempty strings whose concatenation is $w$. For a segmentation $u = u_1 \cdots u_r$, an *occurrence* is an index $i$ with $1 \le i < r$ such that $(u_i, u_{i+1})$ is in the table. JOIN($u$, $S$) joins $u_i$ and $u_{i+1}$ for the indices $i$ of a set $S$, taken from the left, and skips an index that is next to one already joined.

**Lemma 1 (one step).** If $u$ is a segmentation of $w$ and $S$ is a nonempty set of occurrences, then JOIN($u$, $S$) is a segmentation of $w$ with at least one unit less than $u$, and each of its units is a unit of $u$ or the join $a b$ of a pair $(a, b)$ of the table.

*Proof.* JOIN copies the units in order and writes two adjacent units as one string with the same characters, so the concatenation is still $w$. The smallest index of $S$ is always joined, so the length drops by at least one. A joined unit is $u_i u_{i+1}$ for an occurrence $i$, which is the join of a pair in the table. $\square$

**Theorem 1 (termination and output).** For every word $w$ of $n$ characters, every $p \in [0, 1]$ and every sequence of random draws, BPE-DROPOUT stops after at most $n - 1$ joins and returns a segmentation of $w$ whose units are characters of $w$ or joins of pairs in the table. With $p = 0$ it returns the segmentation that merges the pair of highest priority at all its occurrences until no pair is left, which is how Section 2.1 of Provilkov et al. describes the BPE segmentation. With $p = 1$ it returns the characters of $w$.

*Proof.* Line L1 starts with the characters of $w$, a segmentation with $n$ units. Each pass that does not stop at line L5 applies line L7 to a nonempty set, and by Lemma 1 it keeps a segmentation and removes at least one unit. A segmentation has at least one unit, so there are at most $n - 1$ such passes. With $p = 0$, line L4 keeps every occurrence, so line L6 takes the pair of highest priority among all occurrences and line L7 joins all its occurrences, which is the BPE rule. With $p = 1$, line L4 removes every occurrence, so the first pass stops at line L5 with the characters. $\square$

**Theorem 2 (the law).** Let $D(u)$ be the law of the output when the loop starts from the segmentation $u$, and let $O(u)$ be the set of occurrences of $u$. Then
$$D(u) = \sum_{S \subseteq O(u)} (1 - p)^{|S|} \, p^{|O(u)| - |S|} \cdot \begin{cases} \text{the point mass at } u & \text{if } S = \emptyset, \\ D(\mathrm{STEP}(u, S)) & \text{otherwise,} \end{cases}$$
where STEP($u$, $S$) is JOIN($u$, $S'$) for the set $S'$ of indices in $S$ that hold the pair of lowest rank among those in $S$. DISTRIBUTION computes this sum exactly.

*Proof.* In one pass, line L4 keeps each occurrence on its own with probability $1 - p$, as footnote 1 of Provilkov et al. asks, so the kept set equals $S$ with probability $(1 - p)^{|S|} p^{|O(u)| - |S|}$. These events cover all cases and do not overlap. If $S$ is empty, the output is $u$. Otherwise lines L6 and L7 give STEP($u$, $S$), and the later passes use fresh draws, so given $S$ the output has law $D(\mathrm{STEP}(u, S))$. The law of total probability gives the sum. The recursion ends, because STEP shortens $u$ (Lemma 1), and DISTRIBUTION evaluates the sum term by term in exact rational arithmetic, keeping a table of the laws it has found. $\blacksquare$

The law is not a product over the merges. A pass that keeps no occurrence ends the run, so a single drop at the first pass of a short word returns its characters, even when later merges could apply. The example on the page shows this for the word low.
