---
title: After each iSAM2 update, the Bayes tree encodes the full linearized system, and the back substitution with alpha = 0 solves it exactly
proves: [correctness]
status: full
---

**Setting.** The nonlinear factors are $f_1, \dots, f_K$, each on a set $V_f$ of variables. The linearization point is $\theta$. The linear factor of $f$ at $\theta$ is the quadratic $q_f(\delta) = \tfrac12 \delta^\top \Lambda_f \delta - \eta_f^\top \delta$ (up to a constant), in the variables $V_f$. The full linear system at $\theta$ is $Q(\delta) = \sum_f q_f(\delta)$. A conditional on $v$ with the parents $P$ is $c(\delta) = \tfrac12 \|R\delta_v + \sum_{s \in P} S_s \delta_s - d\|^2$ with $R$ upper triangular and invertible. The tree encodes $Q$ if $Q(\delta) = \sum_{\text{all conditionals}} c(\delta) + \text{const}$ for all $\delta$.

The home of a factor in a tree is the clique in which the first eliminated variable of the factor is frontal. For a clique $C$, let $T(C)$ be the subtree below and including $C$, and let $\mathcal{F}(C)$ be the factors whose home is in $T(C)$.

**Assumptions.**

- (A1) Exact arithmetic.
- (A2) Every information block $\Lambda_{vv}$ met during elimination is positive definite. (A prior on the first pose and a connected graph give this.)

**Lemma 1 (one elimination step).** Let $g$ be a quadratic in $v$ and the variables $P$, with the blocks $\Lambda$ and $\eta$. With $R^\top R = \Lambda_{vv}$, $S_s = R^{-\top}\Lambda_{vs}$ and $d = R^{-\top}\eta_v$, we have $g = c + g'$ up to a constant, where $c$ is the conditional $(R, S, d)$ and $g'$ is the quadratic on $P$ with the blocks $\Lambda_{ab} - S_a^\top S_b$ and $\eta_a - S_a^\top d$.

*Proof.* Expand $c = \tfrac12 \|R\delta_v + \sum_s S_s \delta_s - d\|^2$. Its $(v, v)$ block is $R^\top R = \Lambda_{vv}$, its $(v, s)$ block is $R^\top S_s = \Lambda_{vs}$, its $(a, b)$ block on $P$ is $S_a^\top S_b$, and its linear part is $R^\top d = \eta_v$ in $v$ and $S_a^\top d$ in $a$. Subtracting $c$ from $g$ removes every term with $v$ and leaves $g'$. $\square$

By induction over the variables, ELIMINATE turns a set of quadratics into one conditional per variable, and the sum of the conditionals equals the sum of the input quadratics up to a constant.

**Lemma 2 (subtrees).** In a tree built by ELIMINATE and BUILD-CLIQUES, for every clique $C$, $\sum_{f \in \mathcal{F}(C)} q_f = \sum_{\text{conditionals in } T(C)} c + \mathit{cached}(C)$ up to a constant, where $\mathit{cached}(C)$ is the factor on the separator of $C$ produced by the elimination of its last frontal variable.

*Proof.* Elimination puts each factor in the bucket of its first variable in the order, and the factor produced by $v$ lives on the parents $P_v$. Let $v$ be frontal in a clique $D$. The frontal variables of $D$ are eliminated before its separator variables, which are frontal in ancestors. BUILD-CLIQUES merges $v$ into $D$ only if $P_v$ is all of the other variables of $D$ at that moment, so if $v$ is not the last frontal variable of $D$, the first variable of $P_v$ is the next frontal variable of $D$. If $v$ is the last one, $P_v = \mathrm{sep}(D)$, and its first variable is frontal in the parent of $D$. Hence every factor produced in $T(C)$ lands in a bucket of $T(C)$, except the one produced by the last frontal variable of $C$, which is $\mathit{cached}(C)$. Conversely, no factor from outside $T(C)$ lands in a bucket of $T(C)$: an input factor with its home outside $T(C)$ has its first variable outside $T(C)$, and a factor produced in a clique $E$ outside $T(C)$ lands in $E$ or in the parent of $E$, which is outside $T(C)$ as well. So the inputs of the eliminations in $T(C)$ are $\mathcal{F}(C)$ and the factors produced in $T(C)$ other than $\mathit{cached}(C)$. Summing Lemma 1 over these eliminations, the produced factors appear on both sides and cancel, which leaves the claim. $\square$

**Claim 1 (the update keeps the encoding).** If before an update the tree encodes $Q$ at $\theta$, then after the update the tree encodes $Q'$, the full system of the old and new factors at the new linearization point $\theta'$.

*Proof.* Let $J$ be the relinearized variables, so $\theta'$ differs from $\theta$ only on $J$. Line L3 marks every clique that has a variable of $J$ in its frontal or separator variables, every clique with a frontal variable of a new factor, and all their ancestors. The top is the set of marked cliques. It is closed under taking the parent, so the rest of the tree is a set of whole subtrees, rooted at the orphans.

Take a factor $f$ whose home $H$ is in an orphan subtree $T(o)$. All of $V_f$ lies in the frontal and separator variables of $H$. If $V_f$ met $J$, $H$ would be marked, so $V_f \cap J = \emptyset$, and $q_f$ at $\theta'$ equals $q_f$ at $\theta$. By Lemma 2, the conditionals of $T(o)$ plus $\mathit{cached}(o)$ still represent these factors at $\theta'$.

Take a factor $f$ whose home is in the top, or a new factor. Each variable of $V_f$ is a frontal variable of the home or of an ancestor of it, so all of $V_f$ lies in the top variables; for a new factor, its variables are frontal in marked cliques or are new. Conversely a factor with all variables in the top has its home in the top. So line L6 selects exactly these factors, and it relinearizes those that touch $J$ or are new; the others keep their linear factor, which is the same at $\theta'$.

Line L9 eliminates the selected factors and the cached factors of the orphans. By Lemma 1, the new conditionals sum to these quadratics. Together with the conditionals of the orphan subtrees, and by Lemma 2 for each orphan, the sum of all conditionals is $\sum_f q_f$ at $\theta'$ over all factors, which is $Q'$. $\square$

**Claim 2 (the tree is valid).** After an update, every variable is frontal in exactly one clique, and the separator of every clique lies in the frontal and separator variables of its parent.

*Proof.* The variables of the top are eliminated once each at line L9 and placed in one new clique each by BUILD-CLIQUES; the orphan subtrees keep their frontal variables, which are disjoint from the top. Inside the new part, a new clique for $v$ is a child of the clique $p$ of the first eliminated variable $u$ of its parents $P_v$. Variable elimination makes the variables of $P_v \setminus \{u\}$ parents of $u$ (they are all in the factor that $v$ passed up, which lands in the bucket of $u$), so $P_v \subseteq \{u\} \cup P_u \subseteq$ the frontal and separator variables of $p$. A merged variable joins $p$ only if $P_v$ equals all of the variables of $p$, which keeps the property for $p$. For an orphan $o$, $\mathit{cached}(o)$ is a factor on $\mathrm{sep}(o)$ in the input of line L9, so the first eliminated variable $u$ of $\mathrm{sep}(o)$ receives it, and $\mathrm{sep}(o) \subseteq \{u\} \cup P_u$, which lies in the clique of $u$, the new parent from line L11. $\square$

**Claim 3 (the solution).** With $\alpha = 0$, after line L12 the vector $\delta$ satisfies every conditional with zero residual, so it is the unique minimizer of $Q'$.

*Proof.* The back substitution visits cliques from the roots down, and inside a clique it solves the frontal variables from the last eliminated to the first, so the parents of each conditional are solved before it. A visited conditional gets zero residual by line L14. A clique that is skipped at line L13 is not new, so its conditionals did not change, and none of its separator variables changed, so its frontal variables, which were solved for the same conditionals and the same parent values, still have zero residual. Its descendants are not visited. They are not new, because the top is closed under the parent. A separator variable $u$ of a descendant lies in the variables of its parent, by Claim 2, and so, going up, either $u$ is frontal in the skipped part, where nothing changed, or $u$ is in the separator of the skipped clique, where nothing changed. So the inputs of every descendant are unchanged, and its old values still give zero residuals. With all conditionals at zero, the sum of the conditionals is at its minimum, and by Claim 1 this sum is $Q'$ up to a constant. $Q'$ is strictly convex because each $R$ is invertible, so the minimizer is unique. $\square$

**Corollary (no relinearization).** With $\beta = \infty$, $\theta$ never changes after a variable is added, and by Claims 1 and 3, $\delta$ after each update equals the solution of the full linear system at the initial values. The test checks this against a dense solve to $10^{-9}$.

**What this does not show.** With $0 < \beta < \infty$, a variable whose step stays below $\beta$ keeps an old linearization point, so the estimate $\theta + \delta$ is the minimizer of a mix of linearizations, not a stationary point of the nonlinear cost. This is an approximation, and its error depends on $\beta$ and on the problem. With $\alpha > 0$, a clique whose inputs changed by at most $\alpha$ is not updated, so $\delta$ only approximately solves the system. Nothing here bounds the number of cliques that an update touches.
