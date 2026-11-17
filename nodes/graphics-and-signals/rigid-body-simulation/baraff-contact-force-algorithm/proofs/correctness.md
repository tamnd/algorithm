---
title: Baraff's pivoting algorithm returns a solution of the contact LCP, and it terminates for a positive definite matrix
proves: [correctness, termination]
status: full
---

The input is a symmetric positive semidefinite $n \times n$ matrix $A$ and a vector $b$. The goal is $f$ with $f \ge 0$, $a = A f + b \ge 0$ and $f_i a_i = 0$ for all $i$. The algorithm keeps $f$, $a$ and two disjoint index sets $C$ (clamped) and $NC$ (not clamped). Call $P = C \cup NC$ the processed indices. Line numbers refer to the pseudocode of the page.

**Invariants.** At line L3 and at the start of every pass of the loop in DRIVE-TO-ZERO($d$):

- (I0) $a = A f + b$.
- (I1) $f \ge 0$.
- (I2) $a_i = 0$ for $i \in C$.
- (I3) $f_i = 0$ and $a_i \ge 0$ for $i \in NC$.
- (I4) $f_i = 0$ for $i \notin P$, except $f_d \ge 0$ inside DRIVE-TO-ZERO($d$).
- (I5) inside DRIVE-TO-ZERO($d$): $d \notin P$ and $a_d < 0$.

At line L1, $f = 0$, $a = b$ and $P = \emptyset$, so (I0) to (I4) hold. The outer loop picks $d$ with $a_d < 0$; by (I2) and (I3), $d \notin P$, so (I5) holds at the first pass.

**Lemma 1 (the direction).** Let $\Delta f$ be the result of FDIRECTION($d$) and $\Delta a = A \Delta f$. Then $\Delta f_d = 1$, $\Delta f_i = 0$ for $i \notin C \cup \{d\}$, $\Delta a_i = 0$ for $i \in C$, and $\Delta a_d = \Delta f^T A \Delta f \ge 0$. If $A$ is positive definite, $\Delta a_d > 0$.

*Proof.* The first two facts are lines L12 to L14. For $i \in C$, $\Delta a_i = \sum_{j \in C} A_{ij} x_j + A_{id} = (A_{CC} x + A_{Cd})_i = 0$ by line L13. Since $\Delta f$ is supported on $C \cup \{d\}$, $\Delta f^T A \Delta f = \sum_{i \in C} \Delta f_i \Delta a_i + \Delta f_d \Delta a_d = \Delta a_d$. It is $\ge 0$ because $A$ is positive semidefinite, and $> 0$ for positive definite $A$ because $\Delta f \ne 0$. $\square$

So $\Delta a_d$ is the Schur complement $A_{dd} - A_{dC} A_{CC}^{-1} A_{Cd}$; this is Theorem 2 of Baraff's Appendix A.

**Lemma 2 (the step keeps the invariants).** Let $(s, j)$ be the result of MAXSTEP. Then $s \ge 0$, and after line L8 and the set update of lines L9 to L11, the invariants hold again, with $f_d$ increased by $s$.

*Proof.* Each candidate step is nonnegative: $-a_d / \Delta a_d > 0$ by (I5), $-f_i / \Delta f_i \ge 0$ for $i \in C$ by (I1), and $-a_i / \Delta a_i \ge 0$ for $i \in NC$ by (I3). (I0) holds because $a$ and $f$ change by $s \Delta a = A (s \Delta f)$. By Lemma 1, $a_C$ does not change, $f$ does not change outside $C \cup \{d\}$, and $f_d$ grows by $s$. The step is the smallest of the candidates, so no $f_i$ with $i \in C$ becomes negative, no $a_i$ with $i \in NC$ becomes negative, and $a_d$ does not pass zero. The index $j$ that limits the step is tight: if $j \in C$, then $f_j = 0$, and moving $j$ to $NC$ keeps (I3) because $a_j = 0$; if $j \in NC$, then $a_j = 0$, and moving $j$ to $C$ keeps (I2) and (I1); if $j = d$, then $a_d = 0$, and adding $d$ to $C$ keeps (I2) and ends the call. $\square$

**Theorem 1 (the output solves the LCP).** If COMPUTE-FORCES returns, then $f \ge 0$, $a = A f + b \ge 0$ and $f_i a_i = 0$ for all $i$.

*Proof.* It returns only when no $a_i$ is negative. By (I1), $f \ge 0$. For $i \in C$, $a_i = 0$; for $i \in NC$ and for $i \notin P$, $f_i = 0$ by (I3) and (I4). $\square$

**Lemma 3 (each call adds one processed index).** Every call DRIVE-TO-ZERO($d$) that returns adds $d$ to $P$ and does not remove any index from $P$. So there are at most $n$ calls.

*Proof.* Lines L9 and L10 move indices between $C$ and $NC$; line L11 adds $d$, which is not in $P$ by (I5). The outer loop only calls DRIVE-TO-ZERO on an index $d \notin P$, so each call is on a new index. $\square$

**Lemma 4 (uniqueness for positive definite matrices).** If $M$ is positive definite, the LCP $g \ge 0$, $w = M g + q \ge 0$, $g \cdot w = 0$ has at most one solution.

*Proof.* Let $(g, w)$ and $(h, z)$ be solutions. Then $(g - h)^T M (g - h) = (g - h) \cdot (w - z) = g \cdot w - g \cdot z - h \cdot w + h \cdot z = -g \cdot z - h \cdot w \le 0$. Positive definiteness forces $g = h$. $\square$

**Theorem 2 (termination for positive definite $A$).** Let $A$ be positive definite, and assume that no step of MAXSTEP has $s = 0$ (nondegeneracy). Then every call DRIVE-TO-ZERO($d$) ends after at most $2^{|P|}$ passes, and COMPUTE-FORCES ends after at most $n$ calls. The result is the unique solution of the LCP.

*Proof.* Fix one call, with the processed set $P$ at its start; $P$ does not change during the call until the last pass. For $\tau \ge 0$, let $L(\tau)$ be the LCP on the indices $P$ with the matrix $A_{PP}$ and the vector $b_P + A_{Pd} \tau$. By the invariants, at the start of each pass $f_P$ solves $L(f_d)$. $A_{PP}$ is positive definite, so by Lemma 4 this solution is the only one.

For a split $(C, NC)$ of $P$, let $T(C)$ be the set of $\tau$ for which $f_C = -A_{CC}^{-1}(b_C + A_{Cd} \tau)$, $f_{NC} = 0$ solves $L(\tau)$. The conditions are $f_C \ge 0$ and $a_{NC} \ge 0$, which are finitely many linear inequalities in $\tau$, so $T(C)$ is a closed interval. A pass with the set $C$ starts at some $\tau_0 \in T(C)$, moves the state along exactly this affine family (Lemma 1: $f_C$ changes by $s x$, $a_{NC}$ by $s \Delta a_{NC}$), and MAXSTEP stops at the right end of $T(C)$, unless $a_d$ reaches zero first. With $s > 0$ for every step, $f_d$ strictly increases from pass to pass. So if the set $C$ were used again in a later pass, at a value $\tau_1$ larger than the right end of $T(C)$, then $\tau_1 \in T(C)$, which is a contradiction. The passes therefore use distinct subsets $C$ of $P$, so there are at most $2^{|P|}$ of them, and since $\Delta a_d > 0$ (Lemma 1) every pass has a finite step, so the call ends at $j = d$. By Lemma 3 there are at most $n$ calls. The result solves the LCP by Theorem 1, and it is the unique solution by Lemma 4. $\square$

Baraff's Theorem 3 states the same fact, that no set $C$ repeats in one call, and his Theorems 4 and 5 rule out zero steps. This proof assumes nondegeneracy instead.

**Lemma 5 (the index that just moved does not block the next step).** Let $A$ be positive definite. If $j$ moved from $C$ to $NC$, the next direction has $\Delta a_j > 0$. If $j$ moved from $NC$ to $C$, the next direction has $\Delta f_j > 0$.

*Proof.* Let $\Delta f$ be the old direction and $\Delta f'$ the new one, and $\delta = \Delta f' - \Delta f$. Then $\delta_d = 0$. In the first case, $\delta$ is supported on $C$ (the old set), $(A \delta)_i = 0$ for $i \in C \setminus \{j\}$, and $\delta_j = -\Delta f_j > 0$, since $j$ left $C$ because $\Delta f_j < 0$. So $0 < \delta^T A \delta = \delta_j (A\delta)_j = -\Delta f_j\, \Delta a'_j$, where $(A \delta)_j = \Delta a'_j - 0$. Hence $\Delta a'_j > 0$. In the second case, $\delta$ is supported on $C \cup \{j\}$, $(A\delta)_i = 0$ for $i \in C$, $(A \delta)_j = 0 - \Delta a_j > 0$, and $\delta_j = \Delta f'_j$. So $0 < \delta^T A \delta = \Delta f'_j (-\Delta a_j)$, and $\Delta f'_j > 0$. $\square$

So a zero step can only come from a second index that becomes tight at the same value of $f_d$, which is the degenerate case.

**Theorem 3 (positive semidefinite $A$: the accelerations are unique).** Let $A$ be symmetric positive semidefinite and $b = A z$ for some $z$. Then the LCP has a solution, and all solutions have the same $a = A f + b$.

*Proof.* The solutions of the LCP are exactly the points that satisfy the KKT conditions of the convex program: minimize $q(f) = \tfrac12 f^T A f + b^T f$ subject to $f \ge 0$ (the multiplier of $f \ge 0$ is $a$). For a convex program the KKT conditions are necessary and sufficient, so the solutions are the minimizers. A minimizer exists: $q(f) = \tfrac12 (f + z)^T A (f + z) - \tfrac12 z^T A z$ is bounded below, and a quadratic function that is bounded below on a polyhedron attains its minimum there (the Frank-Wolfe theorem). If $f$ and $g$ are minimizers with value $q^*$, then $q(\tfrac12 (f + g)) = \tfrac12 q(f) + \tfrac12 q(g) - \tfrac18 (f - g)^T A (f - g) \ge q^*$, so $(f - g)^T A (f - g) \le 0$, hence $= 0$, and $A (f - g) = 0$ for a positive semidefinite $A$. $\square$

In contact terms, $b = J w$ for the matrix $J$ of the contact normals and the unconstrained accelerations $w$, and $A = J M^{-1} J^T$ has the same column space as $J$, so the condition holds. The forces of a box on three collinear contacts are not unique, but the accelerations are.

**What is not proved.** Termination for a singular $A$ and for degenerate steps is not proved here; Baraff proves it in his Appendix A for $b$ in the column space of $A$, and the sets $A_{CC}$ are then nonsingular (his footnote 2). The bound of $2^{|P|}$ passes per call is not a bound that is reached in practice; Baraff reports about three times the work of one Gaussian elimination of size $n$ in his simulations, which is a measurement. Friction is not covered: Baraff's extension to static friction is not proved to terminate, and the frictional problem is NP-hard in general (Baraff 1991).
