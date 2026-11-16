---
title: The Bayes tree encodes the linear system of its factors, solves it by back substitution, and stays valid and exact under updates
proves: [correctness]
status: full
---

**Setting.** A linear factor is $q_f(x) = \tfrac12 \|\sum_{k \in V_f} A_{f,k} x_k - b_f\|^2$ on the variables $V_f$. The system of a set of factors is $Q = \sum_f q_f$. A conditional on $v$ with the parents $P_v$ is the factor $c_v(x) = \tfrac12 \|R_v x_v + \sum_{s \in P_v} S_{vs} x_s - d_v\|^2$ with $R_v$ upper triangular and invertible. A Bayes tree encodes $Q$ if $Q = \sum_v c_v + \text{const}$ for all $x$, the sum over all conditionals in the tree. The tree is valid if:

- (T1) every variable is frontal in exactly one clique;
- (T2) the parents of each frontal variable lie in the later frontal variables of its clique and in its separator;
- (T3) the separator of each clique lies in the variables $F \cup S$ of its parent, and a root has an empty separator.

**Assumptions.**

- (A1) Exact arithmetic.
- (A2) Every information block $\Lambda_{vv}$ met during elimination is positive definite. If not, the code raises an error.

**Lemma 1 (one elimination step).** Let $g$ be a quadratic in $v$ and the variables $P$, with the information blocks $\Lambda$ and $\eta$. Let $R^\top R = \Lambda_{vv}$, $S_s = R^{-\top}\Lambda_{vs}$ and $d = R^{-\top}\eta_v$. Then $g = c + g'$ up to a constant, where $c$ is the conditional $(R, S, d)$ on $v$ with the parents $P$, and $g'$ is the quadratic on $P$ with the blocks $\Lambda_{ab} - S_a^\top S_b$ and $\eta_a - S_a^\top d$.

*Proof.* The $(v, v)$ block of $c$ is $R^\top R = \Lambda_{vv}$, its $(v, s)$ block is $R^\top S_s = \Lambda_{vs}$, its $(a, b)$ block on $P$ is $S_a^\top S_b$, and its linear part is $R^\top d = \eta_v$ in $v$ and $S_a^\top d$ in $a$. So $g - c$ has no term with $v$, and its blocks are those of $g'$. $\square$

**Claim 1 (elimination).** ELIMINATE returns one conditional per variable, the parents of each conditional come later in the order, and the sum of the conditionals is the sum of the input factors up to a constant.

*Proof.* Lines L2 and L3 take the factors whose first variable in the order is $v$ and apply Lemma 1 to their sum. The new factor of line L4 is on variables later than $v$. Every factor that contains $v$ has its first variable at or before $v$; one with its first variable before $v$ was already consumed, and its remainder is on later variables, so it is in the pool of $v$ or later. Hence the sum at line L3 holds all of the remaining factors that involve $v$, and after this step no factor involves $v$. By induction over the order, the sum of all conditionals plus the remaining factors stays equal to the input sum, and at the end no factor remains (a factor with no variables is a constant). $\square$

A fact used below: if a set $K$ of variables lies in one factor of the input, then when the first variable $u$ of $K$ is eliminated, every other variable of $K$ is a parent of $u$. Indeed, the factor that holds $K$ is either still in the input or has been summed into a remainder, and remainders keep all variables except the eliminated one, so at line L3 for $u$ the sum contains a factor on $K$.

**Claim 2 (grouping).** GROUP-INTO-CLIQUES on the output of ELIMINATE gives a valid tree.

*Proof.* The conditionals are visited in the reverse order, so all parents of $v$ already have cliques. Line L6 makes a root with an empty separator. Otherwise let $u$ be the first parent of $v$ in the order and $p$ its clique. The remainder that $v$ produced is on $P_v$ and enters the elimination of $u$, so $P_v \setminus \{u\} \subseteq P_u$. The clique $p$ holds $u$ and, by induction on (T2) and the merge rule, all of $P_u$, so $P_v \subseteq F_p \cup S_p$. At line L8, $P_v = F_p \cup S_p$, and $v$ becomes the first frontal variable of $p$; its parents are the old variables of $p$, which keeps (T2). At line L9 the new clique has the separator $P_v \subseteq F_p \cup S_p$, which is (T3), and (T2) holds for its single frontal variable. Each variable is placed once, which is (T1). $\square$

**Claim 3 (back substitution).** SOLVE returns the unique minimizer of $Q$.

*Proof.* Lines L10 and L11 visit a clique after its parent, and the frontal variables from the last eliminated to the first. By (T2) and (T3), the parents of a conditional are either later frontal variables of the same clique or separator variables, which are variables of the parent clique, and by induction they were solved earlier. So each $x_v = R_v^{-1}(d_v - \sum_s S_{vs} x_s)$ makes $c_v = 0$. All conditionals are zero, which is the minimum of $\sum_v c_v$, and so of $Q$ by Claim 1. The matrix of $\sum_v c_v$ is $R^\top R$ for the block upper triangular $R$ with invertible diagonal blocks $R_v$, so it is positive definite, and the minimizer is unique. $\square$

**Claim 4 (update).** If the tree is valid and encodes $Q$, then after UPDATE with the new factors $F'$ it is valid and encodes $Q + \sum_{f \in F'} q_f$.

*Proof.* Line L12 marks the clique of each old variable of $F'$ and all its ancestors. This top is closed under taking the parent, so the rest of the tree is a set of whole subtrees, rooted at the orphans of line L13. The conditionals in these subtrees are not touched.

*Encoding.* Line L14 reads each conditional of the top as a factor, which is the same quadratic. By Claim 1, the new conditionals of line L15 sum to the conditionals of the top plus $F'$. Adding the conditionals of the orphan subtrees gives all old conditionals plus $F'$, which is $Q + \sum_{F'} q_f$.

*Variables.* Each variable of a factor in line L14 is a frontal variable of a top clique, or a separator variable of one, which by (T3) is a variable of its parent and, going up, frontal in a top clique. Each variable of $F'$ is frontal in a top clique or is new. So line L15 eliminates exactly the frontal variables of the top and the new variables, and (T1) holds.

*Orphans.* Let $o$ be an orphan with the parent $p$ in the old tree, a top clique. By (T3), $\mathrm{sep}(o) \subseteq F_p \cup S_p$. The first frontal variable of $p$ has all other variables of $p$ as parents, by (T2) and the merge rule, so its conditional, read as a factor at line L14, holds all of $F_p \cup S_p$. By the fact after Claim 1, the first eliminated variable $u$ of $\mathrm{sep}(o)$ has the rest of $\mathrm{sep}(o)$ as parents, so $\mathrm{sep}(o) \subseteq \{u\} \cup P_u$, which lies in the new clique of $u$ by Claim 2. Line L16 attaches $o$ there, which keeps (T3). Inside the subtree of $o$ nothing changed. The new cliques satisfy (T2) and (T3) by Claim 2. $\square$

**What this does not show.** The size of the cliques, and so the cost, depends on the elimination order; nothing here bounds the fill-in. An update that touches a variable near the bottom of a deep tree removes the whole path to the root. The proof is for linear factors; for nonlinear factors the conditionals hold a linearization, and iSAM2 handles relinearization.
