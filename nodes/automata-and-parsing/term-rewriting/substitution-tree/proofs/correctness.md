---
title: Substitution tree operations keep the invariant and retrieval is exact
proves: [correctness]
status: full
---

We use the pseudocode and the invariant (S1) to (S4) of the page, and the notation of the term rewriting pages: terms $T(\Sigma, V)$ and substitutions applied on the right. For a node $x$ with path $x_1, \ldots, x_k$ below the top, $term(x) = *0\, \sigma_{x_1} \cdots \sigma_{x_k}$, and $open(x)$ is the set of indicator variables in $term(x)$; for the top, $term = *0$ and $open = \{*0\}$. For a stored term $l$, $\hat l$ is its normal form, whose variables are $\#1, \#2, \ldots$.

**Lemma 0 (open variables).** If $c$ is a child of $x$, then $open(c) = (open(x) \setminus dom\, \sigma_c) \cup I_c$, where $I_c$ is the set of indicator variables in the range of $\sigma_c$, and $I_c$ is disjoint from $open(x)$ and from the domains on the path to $x$.

*Proof.* $term(c) = term(x)\sigma_c$, and $dom\, \sigma_c \subseteq open(x)$ by (S2). Each variable of $dom\, \sigma_c$ occurs in $term(x)$ and is replaced; by (S3) each variable of $I_c$ occurs only once in all ranges, so it is not in the range of an ancestor, and it is not $*0$ or in $term(x)$, whose indicator variables come from those ranges. It is not in an ancestor's domain either, since by (S2) such domains are open at that ancestor, hence come from earlier ranges or are $*0$. $\square$

## Insertion

**Loop invariant.** At line L2, $\tau$ has domain $open(x)$, its values have no indicator variables, and $term(x)\tau = \hat l$.

Initially $x$ is the top, $\tau = \{*0 \mapsto \hat l\}$, and $term = *0$. At line L3, $\rho$ binds exactly the variables of $I_c$: matching walks every position of $\sigma_c(y)$ against $\tau(y)$, and each variable of $I_c$ occurs once, so it gets one binding, to a subterm of a value of $\tau$, which has no indicator variables. Line L4 sets $\tau' = (\tau \setminus dom\, \sigma_c) \cup \rho$, whose domain is $open(c)$ by Lemma 0. For $y \in dom\, \sigma_c$, $y\sigma_c\tau' = \sigma_c(y)\rho = \tau(y)$, because $\sigma_c(y)$ contains only variables of $I_c$ besides stored variables; for other $y \in open(x)$, $y\sigma_c\tau' = \tau(y)$. Hence $term(c)\tau' = term(x)\sigma_c\tau' = term(x)\tau = \hat l$.

**Line L5.** If $\tau$ is empty, $open(x)$ is empty. Then $x$ is not the top, and by (S1) and (S2) it is a leaf, since an inner node has open variables. So $term(x) = \hat l$, and adding the entry there keeps (S1). The other parts of the invariant do not change.

**Line L8.** Here $\tau$ is not empty and no child matches. For $y \in dom\, \sigma_c$, GENERALIZE walks $\sigma_c(y)$ and $\tau(y)$ in parallel. At equal function symbols it descends; at an equal stored variable it keeps it; at an indicator variable $w$ of $\sigma_c$ it keeps $w$ and sets $\beta(w)$ to the subterm of $\tau(y)$; elsewhere it puts a fresh $z$ with $\alpha(z)$ and $\beta(z)$ the two subterms. By induction on the walk, $\mu(y)\alpha = \sigma_c(y)$ and $\mu(y)\beta = \tau(y)$, where $\alpha$ leaves the kept variables $w$ alone. Let $M$ be the new node, $c'$ the old child with substitution $\alpha$, and $L$ the new leaf with $\rho_L = (\tau \setminus dom\, \mu) \cup \beta$.

- *Terms below $c'$.* $term(c') = term(x)\mu\alpha$, and $\mu\alpha$ agrees with $\sigma_c$ on $dom\, \sigma_c$ and is the identity elsewhere on $open(x)$, so $term(c') = term(c)$. All nodes below $c$ keep their terms, and (S1) holds for them.
- *The new leaf.* $term(L) = term(x)\mu\rho_L$. For $y \in dom\, \mu$, $\mu(y)\rho_L = \mu(y)\beta = \tau(y)$, because the variables of $\mu(y)$ are fresh variables, kept variables and stored variables, and $\beta$ binds the first two. For other $y \in open(x)$, $y\rho_L = \tau(y)$. So $term(L) = term(x)\tau = \hat l$, which has no indicator variables, and $L$ is a leaf with one entry.
- *(S2) and (S3).* $dom\, \mu = dom\, \sigma_c$, which is open at $x$. The range of $\mu$ has the fresh variables, each once, and the kept variables of $I_c$, which leave the range of $\sigma_c$: the range of $\alpha$ consists of subterms of $\sigma_c$ at the positions of fresh variables, which do not contain the kept variables. So every indicator variable still occurs once in all ranges. $dom\, \alpha$ is the set of fresh variables and $dom\, \rho_L$ is $(open(x) \setminus dom\, \mu)$ plus the fresh and kept variables, all open at $M$ by Lemma 0. Both are nonempty: $\alpha$ is checked at line L7, and $\rho_L \supseteq \beta$, which is nonempty because a $\mu$ with no fresh or kept variable would equal $\tau$ on the domain, and then $c$ would have matched at line L3.
- *(S4).* $M$ has two children, and the number of children of $x$ does not change.

**Line L9.** The new leaf has domain $open(x)$, nonempty, and $term = term(x)\tau = \hat l$; its range has no indicator variables. $x$ is the top or an inner node, since a leaf has no open variables, so (S4) still holds. $\blacksquare$

## Retrieval

Let $q'$ be the renamed query, with variables $?x$ disjoint from all stored and indicator variables. Let $R$ be the set of rigid variables of the mode: the query variables for generalizations, the stored variables for instances, none for unifiable terms. For a node $x$ with path $x_1, \ldots, x_k$, let $E(x)$ be the set of equations $*0 = q'$ and $y = \sigma_{x_i}(y)$ for $i \le k$ and $y \in dom\, \sigma_{x_i}$. A solution of $E(x)$ is a substitution $\theta$ that binds no variable of $R$ and makes both sides of each equation equal.

**Lemma 1.** For a leaf $x$, $E(x)$ has a solution iff there is a $\theta$ that binds no variable of $R$ with $term(x)\theta = q'\theta$.

*Proof.* Let $\theta$ solve $E(x)$. By induction on $i$, $*0\theta = *0\, \sigma_{x_1} \cdots \sigma_{x_i}\theta$: the step replaces each variable $y$ of $dom\, \sigma_{x_{i+1}}$ by $\sigma_{x_{i+1}}(y)$, and $y\theta = \sigma_{x_{i+1}}(y)\theta$. So $term(x)\theta = *0\theta = q'\theta$. Conversely, let $term(x)\theta = q'\theta$. Change $\theta$ on the indicator variables, which occur in neither $term(x)$ nor $q'$: for each $y$ bound on the path at $x_i$, set $y\theta' = y\,\sigma_{x_{i+1}} \cdots \sigma_{x_k}\theta$, and $*0\theta' = term(x)\theta$. Then $*0\theta' = q'\theta = q'\theta'$, and $y\theta' = \sigma_{x_i}(y)\sigma_{x_{i+1}} \cdots \sigma_{x_k}\theta = \sigma_{x_i}(y)\theta'$ by the same definition applied to the variables of $\sigma_{x_i}(y)$, which are bound later on the path or are not indicator variables. $\square$

**Lemma 2.** When line L13 processes a node $x$, it succeeds iff $E(x)$ has a solution, and then $\theta$ is a most general such solution.

*Proof.* Induction on the depth of $x$. Before $x$, $\theta$ is a most general solution of $E(parent)$, by induction, or $\{*0 \mapsto q'\}$ for a child of the top, the bindings of other branches having been removed at lines L12 and L16. Robinson's algorithm with rigid variables treated as constants, started from a most general solution $\theta_0$ of a set $E_0$ and given new equations $E_1$, succeeds iff $E_0 \cup E_1$ has a solution, and returns a most general one: every solution of $E_0 \cup E_1$ is an instance of $\theta_0$, so it solves $E_1\theta_0$, and the algorithm is complete for that problem. $\square$

**Theorem.** SUBST-RETRIEVE outputs each entry $(l, v)$ exactly once if it satisfies the query, and no other entry.

*Proof.* The stack visits each node at most once, and visits the children of a node iff its equations succeed, so by Lemma 2 it reaches a leaf $x$ and line L15 outputs its entries iff $E(x)$ has a solution, since $E$ grows along the path. By Lemma 1 and (S1), this holds iff $\hat l\theta = q'\theta$ for some $\theta$ with no rigid binding. For generalizations the query variables are rigid, so $q'\theta = q'$ and $\theta$ restricted to the stored variables is a matcher of $\hat l$ onto $q'$, and so of $l$ onto $q$ after renaming. For instances the stored variables are rigid, so $\hat l = q'\theta$. For unifiable terms, $\hat l$ and $q'$ have disjoint variables, and $\theta$ is a unifier of the renamed terms. Each entry is at exactly one leaf by (S1). $\blacksquare$

## Deletion

Line L17 follows from the top every child that matches, with the same loop invariant as insertion, and a leaf $x$ is reached with $\tau$ empty iff $term(x) = \hat l$: if $term(x) = \hat l$, then at every node on its path $\sigma_c(y)\rho = \tau(y)$ holds with $\rho$ the bindings that the rest of the path gives, so the path is followed; the converse is the loop invariant. By (S1) the entry, if present, is at such a leaf, and line L18 removes one copy. A leaf left without entries is removed at line L19, which keeps (S1) to (S3) for the other nodes.

Line L21 merges a node $p$, other than the top, with its only child $c$. Let $I_p$ be the indicator variables in the range of $\sigma_p$. The merged substitution $\nu$ maps $y \in dom\, \sigma_p$ to $\sigma_p(y)\sigma_c$ and $y \in dom\, \sigma_c \setminus I_p$ to $\sigma_c(y)$. For a variable $y$ of $open(parent)$, $y\sigma_p\sigma_c = y\nu$: if $y \in dom\, \sigma_p$ this is the definition, and otherwise $y\sigma_p = y$ and $y\sigma_c = y\nu$. So $term$ of the merged node equals $term(c)$, and every node below keeps its term. The domain of $\nu$ is $dom\, \sigma_p$ and the part of $dom\, \sigma_c$ open at the parent of $p$, so (S2) holds. Each indicator variable of the range of $\nu$ comes from the range of $\sigma_p$ or $\sigma_c$, and a variable of $I_p$ bound by $\sigma_c$ disappears, so (S3) holds. The merged node has the children and entries of $c$, so (S4) holds again, and the parent of $p$ keeps its number of children. $\blacksquare$
