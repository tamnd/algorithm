---
title: With proper nesting and refluxing, the Berger-Colella step is well defined, conservative and reduces to the uniform scheme
proves: [correctness, termination]
status: full
---

**Setting.** The domain is periodic. Level $l$ has $n_l = n_0r^l$ cells of width $\Delta x_l$ and time step $\Delta t_l = \Delta t_0/r^l$. Level 0 is one patch that covers the domain. A patch $Q$ of level $l + 1$ covers the level-$l$ cells $c_{lo}, \dots, c_{hi} - 1$, so its two end faces are the level-$l$ faces $c_{lo}$ and $c_{hi}$. Patches of one level are disjoint, and two patches of one level are separated by at least one level-$l$ cell that they do not cover (they are maximal runs). The scheme on each patch is conservative: $u_i \leftarrow u_i - \frac{\Delta t}{\Delta x}(F_{i+1/2} - F_{i-1/2})$. For a patch $P$ of level $l$ write $S(P) = \sum_{i \in P}\Delta x_l\,u_i$.

**Invariant (A), averages.** Every covered level-$l$ cell holds the mean of its $r$ cells on level $l + 1$.

**Invariant (N), proper nesting.** For each patch of level $l + 1 \ge 2$ and each level-$l$ cell $c$ under it, the cells $c - 1$, $c$, $c + 1$ are on level $l$.

**Lemma 1 (well defined).** If (N) holds, every value used by L1 and L6 exists.

*Proof.* On level 0 the single patch covers the domain, so every ghost value is in it. Let $l \ge 1$ and let $Q$ be a patch of level $l$ that does not cover the whole domain. Its ghost cells lie in the level-$(l-1)$ cells $c_{lo} - 1$ and $c_{hi}$. For $l = 1$ these are on level 0. For $l \ge 2$ they are on level $l - 1$ by (N), applied to the end cells $c_{lo}$ and $c_{hi} - 1$ of $Q$. That level has been advanced in the current step before $Q$, so both its old and its new values exist, and L1 can interpolate between them. The cells corrected by L6 are the same two cells, so they exist too. They are not covered by level $l$, because $Q$ is a maximal run. $\square$

**Lemma 2 (one patch).** Let (A) and (N) hold before the call $\text{ADVANCE}(l, \theta)$. For every patch $P$ of level $l$, the call changes $S(P)$ by exactly $-(\Delta t_lF_{hi} - \Delta t_lF_{lo})$, where $F_{lo}$ and $F_{hi}$ are the fluxes that L2 computes at the two end faces of $P$. After the call, (A) holds on level $l$ and below the cells of level $l$.

*Proof.* By induction on $L - l$. L2 changes $S(P)$ by $-\sum_i\Delta t_l(F_{i+1/2} - F_{i-1/2})$, which telescopes to $-(\Delta t_lF_{hi} - \Delta t_lF_{lo})$. If $l = L$, nothing else changes $P$.

Let $l < L$. Fix a patch $Q$ of level $l + 1$ inside $P$, with end faces $c_{lo}$ and $c_{hi}$ on level $l$. Let $C_{lo}$ and $C_{hi}$ be $\Delta t_l$ times the level-$l$ fluxes at those faces (L4), and $R_{lo}$ and $R_{hi}$ the sums of $\Delta t_{l+1}$ times the level-$(l+1)$ end fluxes over the $r$ subcycles (L3). By the induction hypothesis applied $r$ times, $S(Q)$ changes by $-(R_{hi} - R_{lo})$, and (A) holds below $Q$ after the subcycles. Now count the changes of $S(P)$ caused by $Q$ after L2.

- L6 changes the cell to the left of face $c_{lo}$ by $-(R_{lo} - C_{lo})/\Delta x_l$ and the cell to the right of face $c_{hi}$ by $+(R_{hi} - C_{hi})/\Delta x_l$. These cells are in $P$ by (N) (or because $P$ is level 0). The change of $S(P)$ is $-(R_{lo} - C_{lo}) + (R_{hi} - C_{hi})$.
- L7 replaces the values of the covered cells. Before the step, by (A), their sum times $\Delta x_l$ was $S(Q)$ before the step. L2 changed that sum by $-(C_{hi} - C_{lo})$, by telescoping over the covered cells. After L7 the sum is $S(Q)$ after the subcycles, which is $S(Q)$ before the step minus $(R_{hi} - R_{lo})$. So L7 changes $S(P)$ by $-(R_{hi} - R_{lo}) + (C_{hi} - C_{lo})$.

The two changes add up to zero. Different patches $Q$ touch different cells of $P$, because they are separated by uncovered cells and each L6 cell is uncovered. So the total change of $S(P)$ is the one from L2. L7 restores (A) on level $l$. $\square$

**Theorem 1 (conservation).** With refluxing, one coarse step keeps the composite mass $M = \sum \Delta x\,u$ over the finest cells that cover each point. In rational arithmetic the equality is exact.

*Proof.* By (A) and induction from the finest level down, $M = S(P_0)$, where $P_0$ is the level-0 patch. The level-0 patch has no end faces on the periodic domain: its two end fluxes are the same face flux, so Lemma 2 gives $S(P_0)$ unchanged. After the step (A) holds, so $M = S(P_0)$ again. $\square$

**Lemma 3 (regridding).** L8 and L9 keep (A), (N) and $M$.

*Proof.* L8 keeps on level $l \ge 1$ only cells $c$ with $c - 1, c, c + 1$ on level $l$, so the new patches of level $l + 1$ satisfy (N). Patches cover whole parent cells. The $r$ children of a parent cell are either all copied from an old fine patch, whose mean equals the parent by (A), or all set to the parent value. In both cases the mean of the children equals the parent, so (A) holds and the final average down changes nothing. The values of level 0 are not changed, so $M = S(P_0)$ is kept. $\square$

**Theorem 2 (reductions).** If $L = 0$, a coarse step is one step of the single-grid scheme. If level 1 covers the whole domain and $L = 1$, the values of level 1 after one coarse step are those of $r$ steps of the uniform scheme with $\Delta x_1$ and $\Delta t_1$.

*Proof.* With $L = 0$ only L1 and L2 run on one periodic patch. If the level-1 patch covers the domain, L1 takes every ghost value from the patch itself, so level 1 does $r$ periodic uniform steps. There are no end faces, so L6 does nothing, and L7 only changes level 0. $\square$

**Termination.** A coarse step makes $r^l$ calls on level $l$ for $l = 0, \dots, L$, each with finitely many cells, and the regrid makes one pass over each level. So each step ends after finitely many operations.

**Remark (order).** The proof gives conservation, not accuracy. The accuracy table on the main page is a measurement. The ghost values are first order in space and linear in time, which matches the first-order upwind scheme of the reference code.

$\blacksquare$
