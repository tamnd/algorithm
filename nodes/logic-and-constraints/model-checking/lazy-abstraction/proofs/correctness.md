---
title: Lazy abstraction is sound, and terminates on finite data domains
proves: [correctness]
status: full
---

We use the notation of the page and of the implementation. The data domain $D$ is finite with $|D| = V$, and there are finitely many locations and edges. A node is *live* until line L8 deletes it. The predicate lists only grow. For a node $n$ with parent $p$ along the edge $\rho$, its region was set to $\alpha_{\mathrm{loc}(n)}(\mathrm{post}_\rho(\mathrm{region}(p)))$, and the root's region to $\alpha_{l_0}(\mathit{Init})$, with the predicates at the time of the computation. The only later change of a region is at line L8, for the pivot, which recomputes it in the same way.

**Lemma 0.** For every set $X$ and location $l$, $X \subseteq \alpha_l(X)$, and $\alpha_l(\emptyset) = \emptyset$. If $Q \in \Pi_l$ and $X \cap Q = \emptyset$, then $\alpha_l(X) \cap Q = \emptyset$.

*Proof.* Each $v \in X$ lies in its own cell. With no cells met, the union is empty. If $Q \in \Pi_l$, every cell lies inside $Q$ or outside it, and a cell that meets $X$ contains a point outside $Q$, so it lies outside $Q$. ∎

**Lemma 1.** A live node's parent is live, and the parent of a live non-root node is expanded and has not had its region changed since the child was created.

*Proof.* Line L8 deletes the whole subtree below the pivot, so it never deletes a node without its descendants. A region changes only for a pivot, and then the pivot's children are deleted and it is marked not expanded. ∎

## Soundness

**Theorem 1 (UNSAFE).** If line L6 returns UNSAFE, the trace is a concrete execution from an initial valuation at $l_0$ to $l_E$.

*Proof.* Line L6 computes $S_0 = \mathit{Init}$ and $S_{i+1} = \mathrm{post}_{\rho_{i+1}}(S_i)$ along the path. If $S_k \ne \emptyset$, the implementation picks a valuation in $S_k$ and, going back, a predecessor in each $S_i$. This is an execution along the path. ∎

We say that a live node $n$ is *closed* if its region is empty, or $\mathrm{loc}(n) \ne l_E$ and $n$ is expanded, or $\mathrm{loc}(n) \ne l_E$ and $n$ is covered by a live expanded node $m$ with $\mathrm{loc}(m) = \mathrm{loc}(n)$ and $\mathrm{region}(n) \subseteq \mathrm{region}(m)$.

**Lemma 2.** At each test of line L2, every live node that is not closed is in the work list $W$.

*Proof.* Nodes enter $W$ when they are created (line L1 or L10). A node leaves $W$ at line L3. If it is then skipped at line L4 because it is dead, expanded, covered, or empty, it is closed or dead. If it is at $l_E$ with a nonempty region, line L5 refines; the error node is then deleted, or it is the pivot and is put back in $W$. Otherwise line L9 covers it or line L10 expands it, and it is closed. A closed node stops being closed only when (i) it is the pivot of line L8, which puts it back in $W$; (ii) a node that covers it is deleted or becomes the pivot, and then line L8 uncovers it and puts it back in $W$. Its region does not change in any other way, and the region of a covering node changes only in case (ii). ∎

**Theorem 2 (SAFE).** If line L11 returns SAFE, then $\psi_l$, the union of the regions of the live nodes at $l$, is an inductive invariant with $\psi_{l_E} = \emptyset$. So $l_E$ is unreachable.

*Proof.* $W$ is empty, so every live node is closed by Lemma 2.

*Initiation.* The root is never deleted, and its region is $\alpha_{l_0}(\mathit{Init}) \supseteq \mathit{Init}$ by Lemma 0.

*Error.* A closed node at $l_E$ has an empty region, so $\psi_{l_E} = \emptyset$.

*Consecution.* Let $v \in \mathrm{region}(n)$ for a live node $n$ at $l \ne l_E$, and let $(l, \rho, l')$ be an edge with $w \in \mathrm{post}_\rho(\{v\})$. If $n$ is expanded, it has a child $c$ for this edge, which is live: children are deleted only together with their parent or when the parent is the pivot, and then the parent is no longer expanded. By Lemma 1 the region of $n$ has not changed since $c$ was created, so $w \in \mathrm{post}_\rho(\mathrm{region}(n)) \subseteq \mathrm{region}(c) \subseteq \psi_{l'}$ by Lemma 0. If $n$ is covered by a live expanded $m$, then $v \in \mathrm{region}(m)$, and the same argument applies to $m$.

By induction on the length of an execution, each reachable pair $(l, v)$ has $v \in \psi_l$. As $\psi_{l_E} = \emptyset$, $l_E$ is unreachable. ∎

## Progress of a refinement

Let the error node $n_k$ at the end of the path $n_0, \ldots, n_k$ have a nonempty region, and let the path be infeasible, $S_k = \emptyset$. Line L7 computes $B_k = D$ and $B_i = \mathrm{pre}_{\rho_{i+1}}(B_{i+1})$, the valuations from which the rest of the path can run to $l_E$; the interpolant is $\varphi_i = D \setminus B_i$. It adds $B_i$ to $\Pi_{\mathrm{loc}(n_i)}$ when $\emptyset \ne B_i \ne D$.

**Lemma 3.** $S_i \cap B_i = \emptyset$ for all $i$, and $\mathrm{post}_{\rho_{i+1}}(D \setminus B_i) \cap B_{i+1} = \emptyset$.

*Proof.* A valuation in $S_i \cap B_i$ would give an execution along the whole path, so $S_k \ne \emptyset$. If $w \in B_{i+1}$ is a successor of $v$ under $\rho_{i+1}$, then $v \in B_i$ by the definition of $B_i$. ∎

**Lemma 4.** The pivot exists. After line L8 its region is disjoint from $B_i$, where $i$ is its index on the path, while before it met $B_i$.

*Proof.* $\mathrm{region}(n_k) \cap B_k = \mathrm{region}(n_k) \ne \emptyset$, so a first index $i$ with $\mathrm{region}(n_i) \cap B_i \ne \emptyset$ exists. Let $X$ be the set that the new region abstracts: $X = \mathit{Init} = S_0$ if $i = 0$, and $X = \mathrm{post}_{\rho_i}(\mathrm{region}(n_{i-1}))$ otherwise. In the first case $X \cap B_0 = \emptyset$ by Lemma 3. In the second, $\mathrm{region}(n_{i-1}) \cap B_{i-1} = \emptyset$ by the choice of $i$, so $X \cap B_i = \emptyset$ by Lemma 3. If $B_i \in \Pi_{\mathrm{loc}(n_i)}$, Lemma 0 gives the claim. Otherwise $B_i = D$ (since $B_i \ne \emptyset$), so $X = \emptyset$ and the new region is empty. ∎

## Termination

**Lemma 5.** At all times, no two live expanded nodes have the same location and the same region.

*Proof.* When $n$ is expanded at line L10, line L9 found no live expanded node at $\mathrm{loc}(n)$ with a region that contains $\mathrm{region}(n)$. Later, regions of expanded nodes do not change (a pivot is first marked not expanded). ∎

**Lemma 6.** Between two refinements, the algorithm takes finitely many steps.

*Proof.* With no refinement, no node is deleted, so all expanded nodes stay live. By Lemma 5 there are at most $L \cdot 2^V$ of them, so at most that many expansions, each adding at most $E$ nodes to $W$. Every other pass of the loop removes a node from $W$ without adding one. ∎

**Theorem 3 (termination).** The algorithm stops after finitely many refinements, so it returns SAFE or UNSAFE, and the answer is correct by Theorems 1 and 2.

*Proof.* Each predicate list at a location holds distinct subsets of $D$, so predicates are added only finitely often. Let $t^*$ be a time after the last addition. Call a live node *old* if its region was last computed before $t^*$. Consider a refinement after $t^*$, with pivot $n_i$. Since nothing is added, either $B_i \in \Pi_{\mathrm{loc}(n_i)}$ already, or $B_i = D$. The set $X$ of Lemma 4 is disjoint from $B_i$, and by Lemma 1 it is the same set from which the current region of $n_i$ was computed. If that region had been computed after $t^*$, it would be disjoint from $B_i$ by the argument of Lemma 4, which contradicts the choice of the pivot. So the pivot is old, and after line L8 it is not. Nodes created or recomputed after $t^*$ are not old. So each refinement after $t^*$ reduces the finite number of old live nodes by at least one, and there are finitely many such refinements. With Lemma 6, the algorithm stops. ∎
