---
title: MK-TEST puts each counted change in one cell, and its p-value is exact under the neutral model
proves: [correctness]
status: full
---

**Setting.** Species A has sequences $a_1, \ldots, a_{n_A}$ and species B has $b_1, \ldots, b_{n_B}$, with $n_A, n_B \ge 1$, all aligned and in frame, of $c$ codons over A, C, G and T, with no stop codon. At codon $t$, the column is the list of the $n_A + n_B$ codons there. A position $j \in \{1, 2, 3\}$ varies at codon $t$ when the column has two or more bases at $j$. Codon $t$ is counted when exactly one position $j$ varies. Then the change is synonymous when all codons of the column code the same amino acid, polymorphic when the codons of A, or those of B, have two or more bases at $j$, and fixed otherwise.

**Lemma 1 (one cell).** Each counted codon adds 1 to exactly one of $D_n$, $D_s$, $P_n$ and $P_s$, and no other codon changes them. After line L5, $D_n + D_s + P_n + P_s$ is the number of counted codons.

*Proof.* Line L1 sets the counters to 0. Line L2 visits each counted codon once and skips the others. For a counted codon, line L3 sets syn to true or false, and lines L4 and L5 are the two branches of one test, so the codon goes to the polymorphic row or to the fixed row and, inside the row, to one column by syn. $\square$

**Lemma 2 (fixed means a difference).** If a counted codon is fixed, then the bases of A at $j$ are all equal to some $x$, the bases of B are all equal to some $y$, and $x \ne y$.

*Proof.* A fixed codon is not polymorphic, so A has one base $x$ and B has one base $y$ at $j$. Position $j$ varies over the whole column, so $x \ne y$. $\square$

**Lemma 3 (Fisher's p-value).** Let $r_1 = D_n + D_s$, $r_2 = P_n + P_s$, $c_1 = D_n + P_n$ and $N = r_1 + r_2$. Suppose that, given $r_1$, $r_2$ and $c_1$, the law of $D_n$ is hypergeometric: $\Pr(D_n = k) = w(k) / \binom{N}{c_1}$ with $w(k) = \binom{r_1}{k}\binom{r_2}{c_1 - k}$ for $\max(0, c_1 - r_2) \le k \le \min(r_1, c_1)$. Then line L6 returns $p = \Pr(w(D_n) \le w(d))$ for the observed value $d$ of $D_n$, and $\Pr(p \le u) \le u$ for every $u \in [0, 1]$.

*Proof.* The loop of line L6 runs over exactly the values $k$ with $w(k) > 0$ and adds $w(k)$ when $w(k) \le w(d)$, so it returns $\sum_{k : w(k) \le w(d)} w(k) / \binom{N}{c_1}$, which is $\Pr(w(D_n) \le w(d))$. The sums are of integers, so the comparison is exact. Write $G(v) = \Pr(w(D_n) \le v)$, so that $p = G(w(D_n))$. For $u \in [0, 1]$, let $v^*$ be the largest value of $w$ with $G(v^*) \le u$. If there is none, $\Pr(p \le u) = 0$. Otherwise $p \le u$ holds exactly when $w(D_n) \le v^*$, because $G$ does not decrease, and so $\Pr(p \le u) = G(v^*) \le u$. $\square$

**Lemma 4 (the neutral model gives the hypergeometric law).** Suppose that, given the genealogy of the sample and the fixed or polymorphic status of every counted change, the kinds of the counted changes are independent, each nonsynonymous with the same probability $f \in (0, 1)$. Then, given $r_1$, $r_2$ and $c_1$, $D_n$ has the hypergeometric law of Lemma 3.

*Proof.* Given the statuses, $r_1$ and $r_2$ are fixed numbers, $D_n$ is the number of nonsynonymous changes among $r_1$ and $P_n$ among $r_2$. So $D_n$ and $P_n$ are independent with laws $\mathrm{Bin}(r_1, f)$ and $\mathrm{Bin}(r_2, f)$. For $D_n + P_n = c_1$,

$$\Pr(D_n = k \mid D_n + P_n = c_1) = \frac{\binom{r_1}{k} f^k (1-f)^{r_1 - k} \binom{r_2}{c_1 - k} f^{c_1 - k} (1-f)^{r_2 - c_1 + k}}{\sum_i \binom{r_1}{i} f^i (1-f)^{r_1 - i} \binom{r_2}{c_1 - i} f^{c_1 - i} (1-f)^{r_2 - c_1 + i}}.$$

Every term has the factor $f^{c_1} (1-f)^{N - c_1}$, which cancels, and $\sum_i \binom{r_1}{i}\binom{r_2}{c_1 - i} = \binom{N}{c_1}$ by Vandermonde's identity. So the law is $w(k)/\binom{N}{c_1}$, which does not depend on $f$ or on the statuses. $\square$

**When the hypothesis of Lemma 4 holds.** Take a region without recombination, so the sample has one genealogy, and infinite sites, so each change is one mutation on one branch. Mutations fall on the branches as a Poisson process, independent of their positions in the gene. A mutation on a branch whose descendants in the sample include all of A and none of B, or all of B and none of A, gives a fixed difference; any other branch gives a polymorphism. So the status of a mutation is a function of its branch only. If synonymous mutations are neutral and each nonsynonymous mutation is either neutral or never seen in the sample, then the kind of a seen mutation depends only on its position, and the positions are independent of the branches. So the kinds are independent of the statuses with one probability $f$, as Lemma 4 needs. Selection that favours amino acid changes breaks this: such changes go to fixation fast, so a fixed change is more often nonsynonymous than a polymorphic one.

**Theorem.** MK-TEST returns the four counts of the counting rule, with every counted codon in exactly one cell. Under the hypothesis of Lemma 4, its p-value satisfies $\Pr(p \le u) \le u$ for every $u$, so a test that rejects when $p \le u$ has level at most $u$. When $D_n$, $D_s$ and $P_s$ are positive, it returns $\mathrm{NI} = \frac{P_n D_s}{P_s D_n}$ and $\alpha = 1 - \mathrm{NI}$.

*Proof.* The counts follow from Lemma 1, and Lemma 2 shows that the fixed row counts real differences between the species. The level follows from Lemmas 4 and 3, applied given the margins; since the bound holds given every value of the margins, it also holds without the condition. Line L7 computes NI and $\alpha$ by their formulas, and returns no value when a denominator is 0. $\square$
