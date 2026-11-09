---
title: MEASURE returns the volume of the union of the boxes inside the cell, and terminates
proves: [correctness, termination]
status: full
---

**Notation.** $C = \prod_j [\ell_j, h_j]$ is a cell with positive volume, $S$ a finite set of boxes, and $U(S) = \bigcup_{B \in S} B$. The claim is that $\text{MEASURE}(C, S) = \operatorname{vol}(U(S) \cap C)$. For a box $B$ with $B \cap C$ of positive volume, $F(B) = \{j : B \text{ does not cover } [\ell_j, h_j] \text{ in coordinate } j\}$; $B$ covers $C$ when $F(B) = \emptyset$, and it is a $j$-pile when $F(B) = \{j\}$. $\Phi(C, S)$ is the number of pairs $(j, v)$ such that $v$ is a boundary value in coordinate $j$ of some box of $S$ and $\ell_j < v < h_j$.

**Lemma 1 (line L1).** Replacing $S$ by $S' = \{B \cap C : \operatorname{vol}(B \cap C) > 0\}$ does not change $\operatorname{vol}(U \cap C)$.

*Proof.* $U(S) \cap C = \bigcup_B (B \cap C)$. The dropped sets have volume $0$, and a finite union of null sets is null, so the volume does not change. $\square$

**Lemma 2 (line L5).** If every box of $S$ is a pile of $C$, then $\operatorname{vol}(U(S) \cap C) = \operatorname{vol}(C) - \prod_j (|C_j| - U_j)$.

*Proof.* Let $I_j$ be the union of the $j$-intervals of the $j$-piles, intersected with $[\ell_j, h_j]$, so that $|I_j| = U_j$. A $j$-pile $B$ contains a point $x \in C$ if and only if $x_j \in B_j$, since $B$ covers $C$ in every other coordinate. So $x \in C$ is in no box if and only if $x_j \notin I_j$ for every $j$, and the uncovered part of $C$ is $\prod_j ([\ell_j, h_j] \setminus I_j)$, of volume $\prod_j (|C_j| - U_j)$. Each box has exactly one pile coordinate, so each is counted in one $I_j$. $\square$

**Lemma 3 (line L6).** If no box of $S$ covers $C$ and some box is not a pile, then that box has an inner value, so line L6 can choose $j$ and $m$.

*Proof.* After line L1 every box is clipped, $B = \prod_j [a_j, b_j] \subseteq C$ with $a_j < b_j$. The box $B$ has $|F(B)| \ge 2$; take $j \in F(B)$. Not covering in coordinate $j$ means $a_j > \ell_j$ or $b_j < h_j$. In the first case $\ell_j < a_j < b_j \le h_j$, so $a_j$ is inner; in the second case $\ell_j \le a_j < b_j < h_j$, so $b_j$ is inner. $\square$

**Lemma 4 (lines L7 and L8).** If $C^-$ and $C^+$ are the two halves of $C$ cut at $x_j = m$, then $\operatorname{vol}(U \cap C) = \operatorname{vol}(U \cap C^-) + \operatorname{vol}(U \cap C^+)$, and $\Phi(C^\pm, S) < \Phi(C, S)$.

*Proof.* $C = C^- \cup C^+$, and $C^- \cap C^+$ lies in the hyperplane $x_j = m$, of volume $0$, so the volume is additive. Every pair $(k, v)$ inner for $C^\pm$ is inner for $C$, since the intervals of $C^\pm$ are contained in those of $C$. The pair $(j, m)$ is inner for $C$ but not for $C^-$ or $C^+$, where $m$ is an end point. $\square$

**Theorem.** For every cell $C$ of positive volume and finite set $S$ of boxes, $\text{MEASURE}(C, S)$ terminates and returns $\operatorname{vol}(U(S) \cap C)$. The recursion depth is at most $\Phi(C, S) \le 2 d |S|$.

*Proof.* By induction on $\Phi(C, S)$. By Lemma 1, line L1 keeps the answer and gives boxes that all meet $C$ with positive volume; this step does not increase $\Phi$, since it only removes boxes and moves boundary values onto the boundary of $C$. If a box covers $C$, then $U \cap C = C$ and line L2 is right. If all boxes are piles, line L5 is right by Lemma 2. Otherwise Lemma 3 gives a valid cut, and by Lemma 4 both children have a smaller $\Phi$; by induction both calls terminate with the right volumes, and their sum is the right volume by Lemma 4. When $\Phi = 0$, no box has an inner value, so by Lemma 3 line L2 or line L3 applies, which is the base case. Each box has $2$ boundary values in each of $d$ coordinates, so $\Phi \le 2 d |S|$, and the depth bound follows from the strict decrease. $\blacksquare$
