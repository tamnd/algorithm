---
title: MUSCLE returns a valid alignment, and its refinement never lowers the SP score and always ends
proves: [correctness]
status: full
---

A *valid alignment* of sequences $(S_r)_{r \in R}$ is a set of rows of equal length over $\Sigma \cup \{-\}$ such that row $r$ with its gaps removed equals $S_r$, and no column consists of gaps only. A *block alignment* of two alignments $X$ and $Y$ is a sequence of columns, each being a column of $X$ over a column of $Y$, a column of $X$ over gaps, or gaps over a column of $Y$, in which the columns of $X$ appear once each in order, and so do the columns of $Y$. PROFILE-ALIGN returns a block alignment; this follows from its traceback, which emits one of the three kinds of column per step and walks from $(m, n)$ to $(0, 0)$.

**Lemma 1 (a block alignment of valid groups is valid).** If $X$ is a valid alignment of $(S_r)_{r \in R_X}$ and $Y$ of $(S_r)_{r \in R_Y}$, with $R_X \cap R_Y = \emptyset$, then every block alignment $N$ of $X$ and $Y$ is a valid alignment of $(S_r)_{r \in R_X \cup R_Y}$.

*Proof.* A row of $X$ appears in $N$ as its own symbols in order, with gaps added where $N$ has a column of the third kind; removing gaps leaves $S_r$. The same holds for rows of $Y$. All rows of $N$ have one symbol per column of $N$, so they have equal length. A column of the first two kinds contains a column of $X$, which has a letter; a column of the third kind contains a column of $Y$, which has a letter. $\square$

**Lemma 2 (removing empty columns keeps validity).** If $N$ is a valid alignment of $(S_r)_{r \in R}$ and $R' \subseteq R$ is nonempty, then the rows of $R'$ with every column of gaps only (within $R'$) removed are a valid alignment of $(S_r)_{r \in R'}$.

*Proof.* Removing a column where all rows of $R'$ have a gap removes no letter, keeps the rows of equal length, and leaves only columns with a letter. $\square$

**Claim 1 (stages 1 and 2 give valid alignments).** By induction over the postorder of a guide tree. A leaf gives the one-row alignment of its sequence, which is valid. An internal node either reuses an alignment of the same subtree computed in line L3, which is valid by the same induction in TREE1, or applies PROFILE-ALIGN to the valid alignments of its two children, whose leaf sets are disjoint; Lemma 1 gives validity. The root covers all $k$ sequences.

**Claim 2 (stage 3 keeps validity and never lowers the score).** Let $M_0$ be the alignment after line L6, and $M_t$ the alignment after the $t$-th accepted change in line L12. We show by induction that $M_t$ is valid and $\mathrm{SP}(M_t) > \mathrm{SP}(M_{t-1})$. Given a valid $M_{t-1}$, line L10 splits its rows by an edge of TREE2 into two nonempty disjoint sets and, by Lemma 2, gives two valid groups $X$ and $Y$. By Lemma 1, $A' = \text{PROFILE-ALIGN}(X, Y)$ is valid for all $k$ sequences. Line L12 sets $M_t = A'$ only if $\mathrm{SP}(A') > \mathrm{SP}(M_{t-1})$. If the test fails, the alignment does not change. So the score of the current alignment is nondecreasing during stage 3, and the output scores at least $\mathrm{SP}(M_0)$.

**Claim 3 (stage 3 ends).** Each pass of line L7 visits $2k - 3$ edges, a finite number, and there are at most maxPasses passes. Without the limit, the loop still ends: a pass that accepts no change triggers line L13, and every accepted change strictly increases $\mathrm{SP}$ among the finitely many valid alignments of the input (each has at most $\sum_r |S_r|$ columns), so only finitely many changes can be accepted.

**Claim 4 (two sequences).** For $k = 2$ both trees are the single pair, stage 1 runs one PROFILE-ALIGN on two one-row groups, and stage 3 can only realign the same two rows. For one-row columns $x = (a)$ and $y = (b)$ with letters $a, b$, we have $f_{xG} = f_{yG} = 0$, $f_{xa} = f_{yb} = 1$, and

$$\mathrm{LE}_{xy} = \log \frac{p_{ab}}{p_a\, p_b},$$

the pair score of the SP objective; a column against an inserted gap column scores the gap penalty, which is the SP score of a letter against a gap. So PROFILE-ALIGN maximizes the pairwise SP score over all block alignments, which for two one-row groups are all pairwise alignments, by the correctness of the global alignment recurrence. The result is optimal, and stage 3 cannot find a strictly better one. $\blacksquare$
