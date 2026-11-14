---
title: Algorithm W is sound and complete for the Hindley-Milner rules
proves: [correctness, termination]
status: full
---

This file proves in full that algorithm W is sound and complete for the syntax-directed rules of the [Hindley-Milner type system](/hindley-milner-type-system/): rules T-Var', T-Abs, T-App and T-Let'. The step from the syntax-directed rules to the declarative rules with T-Gen and T-Inst is cited. It is a separate induction on derivations, given in the thesis of Damas (1985), and outlined on the Hindley-Milner page. The proof follows the plan of Damas and Milner (1982). The forms `if`, the operators and `fix` add cases that are the same as the application case, so we leave them out.

## Setting

A *substitution* $S$ maps type variables to types and is the identity on all but finitely many. $S$ acts on a type by replacing each variable at once. On a scheme $\forall \vec\alpha.\, \tau$, we first rename $\vec\alpha$ to variables that $S$ does not touch and that do not occur in the range of $S$, and then apply $S$ to the body. $S S'$ is the composition: first $S'$, then $S$. Schemes are equal up to renaming of bound variables and removal of bound variables that do not occur in the body.

A scheme $\sigma'$ is *more general* than $\sigma$, written $\sigma' \sqsupseteq \sigma$, if each instance of $\sigma$ is an instance of $\sigma'$. Contexts are compared name by name.

W returns a pair $(S, \tau)$ or fails. It calls MGU, the most general unifier of [Robinson's algorithm](/robinson-unification/). We use two facts about MGU. If MGU$(\tau_1, \tau_2)$ returns $U$, then $U\tau_1 = U\tau_2$. If some $R$ has $R\tau_1 = R\tau_2$, then MGU$(\tau_1, \tau_2)$ succeeds and returns a $U$ with $R = R' U$ for some $R'$. The variables in $U$ all occur in $\tau_1$ or $\tau_2$ (see [most general unifier](/most-general-unifier/)).

*Fresh* variables. W takes each fresh variable from a global supply, so it is new to the whole run. A call $W(\Gamma, e)$ *creates* the fresh variables that it and its nested calls take. Each variable in the result $(S, \tau)$ is free in $\Gamma$ or created by the call. This follows from the cases of W below and from the fact about the variables of MGU.

## Two lemmas on derivations

**Lemma 1 (a more general context).** If $\Gamma, x : \sigma \vdash e : \tau$ and $\sigma' \sqsupseteq \sigma$, then $\Gamma, x : \sigma' \vdash e : \tau$.

*Proof.* First, $\mathrm{ftv}(\sigma') \subseteq \mathrm{ftv}(\sigma)$. Write $\sigma' = \forall \vec\alpha.\, \tau'$. Rename the bound variables of $\sigma$ to variables that do not occur in $\sigma'$, so that $\sigma = \forall \vec\beta.\, \tau$. The body $\tau$ is an instance of $\sigma$, so $\tau = R\tau'$ for an $R$ that changes only $\vec\alpha$. A free variable $\gamma$ of $\sigma'$ occurs in $\tau'$, and $R\gamma = \gamma$, so $\gamma$ occurs in $\tau$. It is not in $\vec\beta$, so $\gamma \in \mathrm{ftv}(\sigma)$.

Now use induction on the derivation, for all contexts in which some names have more general schemes. At T-Var', an instance of $\sigma$ is an instance of $\sigma'$. At T-Let', the generalization of the new context quantifies at least the variables that the old one quantifies, because the new context has no more free variables. So the scheme for the `let`-bound name is more general, and the induction hypothesis applies to the body. The other rules do not look at the context. $\square$

**Lemma 2 (type substitution).** If $\Gamma \vdash e : \tau$, then $S\Gamma \vdash e : S\tau$ for each substitution $S$, by a derivation of the same height.

*Proof.* Induction on the height of the derivation, for all $S$ at once. T-Abs and T-App follow from the induction hypothesis. At T-Var', $\Gamma(x) = \forall \vec\alpha.\, \tau_0$ and $\tau = [\vec\alpha := \vec\rho]\,\tau_0$. Rename $\vec\alpha$ so that $S$ does not touch these variables and they do not occur in the range of $S$. Then $S(\forall\vec\alpha.\, \tau_0) = \forall\vec\alpha.\, S\tau_0$, and $S\tau = [\vec\alpha := S\vec\rho]\,(S\tau_0)$ is an instance of it.

At T-Let', the premises are $\Gamma \vdash e_1 : \tau_1$ and $\Gamma, x : \forall\vec\alpha.\, \tau_1 \vdash e_2 : \tau$, where $\vec\alpha = \mathrm{ftv}(\tau_1) \setminus \mathrm{ftv}(\Gamma)$. Choose new variables $\vec\beta$ that do not occur in $\Gamma$, $\tau_1$ or $S$, and let $P = [\vec\alpha := \vec\beta]$. By the induction hypothesis with $SP$, $SP\Gamma \vdash e_1 : SP\tau_1$. Since $\vec\alpha$ is not free in $\Gamma$, $SP\Gamma = S\Gamma$. The variables $\vec\beta$ are not free in $S\Gamma$, so $\mathrm{Gen}(S\Gamma, SP\tau_1)$ quantifies all of $\vec\beta$ and is more general than $\forall \vec\beta.\, SP\tau_1$, which is $S(\forall \vec\alpha.\, \tau_1)$. By the induction hypothesis with $S$ on the second premise, $S\Gamma, x : S(\forall\vec\alpha.\, \tau_1) \vdash e_2 : S\tau$. By Lemma 1, the same holds with $x : \mathrm{Gen}(S\Gamma, SP\tau_1)$. T-Let' gives $S\Gamma \vdash \texttt{let } x = e_1 \texttt{ in } e_2 : S\tau$. Lemma 1 does not increase the height, so the heights stay the same. $\square$

The side condition of generalization is used in the step $SP\Gamma = S\Gamma$. If $\mathrm{Gen}$ also quantified variables that are free in $\Gamma$, this step and Lemma 2 would fail, and so would soundness.

## Soundness

**Theorem 1 (soundness).** If $W(\Gamma, e) = (S, \tau)$, then $S\Gamma \vdash e : \tau$.

*Proof.* Induction on $e$.

- *Variable* (lines L1 and L2). $\Gamma(x) = \forall\vec\alpha.\, \tau_0$, $S$ is the identity, and $\tau = [\vec\alpha := \vec\beta]\,\tau_0$ is an instance. T-Var' applies.
- *Abstraction* (lines L3 to L5). By induction, $S_1\Gamma, x : S_1\beta \vdash e_1 : \tau_1$. T-Abs gives $S_1\Gamma \vdash \texttt{fun } x \texttt{ -> } e_1 : S_1\beta \to \tau_1$.
- *Application* (lines L6 to L9). By induction, $S_1\Gamma \vdash e_1 : \tau_1$ and $S_2S_1\Gamma \vdash e_2 : \tau_2$. By Lemma 2 with $S_3S_2$ and with $S_3$, $S_3S_2S_1\Gamma \vdash e_1 : S_3S_2\tau_1$ and $S_3S_2S_1\Gamma \vdash e_2 : S_3\tau_2$. Line L8 gives $S_3S_2\tau_1 = S_3\tau_2 \to S_3\beta$. T-App gives the type $S_3\beta$.
- *Let* (lines L10 to L13). By induction, $S_1\Gamma \vdash e_1 : \tau_1$ and $S_2(S_1\Gamma, x : \sigma) \vdash e_2 : \tau_2$ with $\sigma = \mathrm{Gen}(S_1\Gamma, \tau_1)$. Exactly as in the `let` case of Lemma 2, with $S_2$ in place of $S$ and $S_1\Gamma$ in place of $\Gamma$, there is a type $\tau_1'$ with $S_2S_1\Gamma \vdash e_1 : \tau_1'$ and $\mathrm{Gen}(S_2S_1\Gamma, \tau_1') \sqsupseteq S_2\sigma$. Lemma 1 and T-Let' give $S_2S_1\Gamma \vdash \texttt{let } x = e_1 \texttt{ in } e_2 : \tau_2$. $\square$

## Completeness

**Theorem 2 (completeness).** Let $R$ be a substitution with $R\Gamma \vdash e : \tau'$. Then $W(\Gamma, e)$ succeeds with a result $(S, \tau)$, and there is a substitution $R'$ with $R'\tau = \tau'$ and $R'S\alpha = R\alpha$ for each variable $\alpha$ that the call did not create.

*Proof.* Induction on $e$, for all $\Gamma$, $R$ and $\tau'$. The variables created by the call are fresh, so they do not occur in $\Gamma$, and we may change $R$ on them freely.

*Variable.* Let $\Gamma(x) = \forall\vec\alpha.\, \tau_0$, with $\vec\alpha$ apart from $R$. The judgment $R\Gamma \vdash x : \tau'$ comes from T-Var', so $\tau' = [\vec\alpha := \vec\rho]\,R\tau_0$ for some types $\vec\rho$. W returns $(\mathrm{id}, [\vec\alpha := \vec\beta]\,\tau_0)$ with fresh $\vec\beta$. Let $R'$ be $R$ with $\vec\beta := \vec\rho$. Then $R'[\vec\alpha := \vec\beta]\,\tau_0 = [\vec\alpha := \vec\rho]\,R\tau_0 = \tau'$, and $R' = R$ on each old variable.

*Abstraction.* The judgment comes from T-Abs, so $\tau' = \tau_a \to \tau_b$ and $R\Gamma, x : \tau_a \vdash e_1 : \tau_b$. Let $R_0$ be $R$ with $\beta := \tau_a$, for the fresh $\beta$ of line L3. Then $R_0(\Gamma, x : \beta) = R\Gamma, x : \tau_a$. By induction, $W(\Gamma, x : \beta;\ e_1) = (S_1, \tau_1)$ with an $R_1$ such that $R_1\tau_1 = \tau_b$ and $R_1S_1 = R_0$ on the variables not created by that call. In particular $R_1S_1\beta = \tau_a$. So $R_1(S_1\beta \to \tau_1) = \tau'$. Take $R' = R_1$.

*Application.* The judgment comes from T-App, so $R\Gamma \vdash e_1 : \tau_a \to \tau'$ and $R\Gamma \vdash e_2 : \tau_a$.

1. By induction on $e_1$: $W(\Gamma, e_1) = (S_1, \tau_1)$ and $R_1\tau_1 = \tau_a \to \tau'$, with $R_1S_1 = R$ on old variables. So $R_1(S_1\Gamma) = R\Gamma$.
2. So $R_1(S_1\Gamma) \vdash e_2 : \tau_a$. By induction on $e_2$ with the context $S_1\Gamma$ and the substitution $R_1$: $W(S_1\Gamma, e_2) = (S_2, \tau_2)$ and $R_2\tau_2 = \tau_a$, with $R_2S_2 = R_1$ on each variable not created by the second call.
3. Each variable of $\tau_1$ is old for the second call. So $R_2S_2\tau_1 = R_1\tau_1 = \tau_a \to \tau'$. Let $R_3$ be $R_2$ with $\beta := \tau'$, for the fresh $\beta$ of line L8. The variable $\beta$ does not occur in $S_2\tau_1$ or $\tau_2$. So $R_3S_2\tau_1 = \tau_a \to \tau'$ and $R_3(\tau_2 \to \beta) = \tau_a \to \tau'$.
4. $R_3$ unifies $S_2\tau_1$ and $\tau_2 \to \beta$. So MGU succeeds at line L8 with $S_3$, and $R_3 = R_4S_3$ for some $R_4$.
5. Take $R' = R_4$. Then $R'S_3\beta = R_3\beta = \tau'$. On a variable that the whole call did not create, $R_4S_3S_2S_1 = R_3S_2S_1 = R_2S_2S_1 = R_1S_1 = R$. The second step holds because $\beta$ does not occur in $S_2S_1\alpha$ for an old $\alpha$. The third holds because $S_1\alpha$ only has variables that are old for the second call.

*Let.* The judgment comes from T-Let', so $R\Gamma \vdash e_1 : \tau_a$ and $R\Gamma, x : \mathrm{Gen}(R\Gamma, \tau_a) \vdash e_2 : \tau'$.

1. By induction on $e_1$: $W(\Gamma, e_1) = (S_1, \tau_1)$ with $R_1\tau_1 = \tau_a$ and $R_1S_1\Gamma = R\Gamma$.
2. **Claim.** $R_1(\mathrm{Gen}(S_1\Gamma, \tau_1)) \sqsupseteq \mathrm{Gen}(R\Gamma, \tau_a)$. Let $\vec\alpha = \mathrm{ftv}(\tau_1) \setminus \mathrm{ftv}(S_1\Gamma)$. Then $R_1(\forall\vec\alpha.\, \tau_1) = \forall\vec\beta.\, R_1P\tau_1$, where $P = [\vec\alpha := \vec\beta]$ and $\vec\beta$ is new. An instance of $\mathrm{Gen}(R\Gamma, \tau_a)$ has the form $Q R_1\tau_1$, where $Q$ changes only variables not free in $R\Gamma$. Let $Q' = [\vec\beta := Q R_1 \vec\alpha]$. For a variable $\delta$ of $\tau_1$: if $\delta \in \vec\alpha$, then $Q'R_1P\delta = QR_1\delta$. If not, then $\delta$ is free in $S_1\Gamma$, so the variables of $R_1\delta$ are free in $R_1S_1\Gamma = R\Gamma$, and $Q'R_1P\delta = R_1\delta = QR_1\delta$. So $QR_1\tau_1 = Q'(R_1P\tau_1)$ is an instance of $R_1(\forall\vec\alpha.\, \tau_1)$.
3. By the claim and Lemma 1, $R_1(S_1\Gamma, x : \mathrm{Gen}(S_1\Gamma, \tau_1)) \vdash e_2 : \tau'$. By induction on $e_2$: $W(S_1\Gamma, x : \mathrm{Gen}(S_1\Gamma, \tau_1);\ e_2) = (S_2, \tau_2)$ with $R_2\tau_2 = \tau'$ and $R_2S_2 = R_1$ on variables that the second call did not create.
4. Take $R' = R_2$. On old variables, $R_2S_2S_1 = R_1S_1 = R$, as in the application case. $\square$

## Principal types and termination

**Corollary (principal types).** Let $e$ be closed. If $e$ has a type, then $W(\emptyset, e) = (S, \tau)$, and each type of $e$ is an instance $R'\tau$ of $\tau$. If $e$ has no type, W fails.

*Proof.* If $\vdash e : \tau'$, Theorem 2 with any $R$ gives $\tau' = R'\tau$. By Theorem 1, $\vdash e : \tau$, and by Lemma 2 each instance of $\tau$ is a type of $e$. So the types of $e$ are exactly the instances of $\tau$, and $\forall \mathrm{ftv}(\tau).\, \tau$ is the principal scheme. If W succeeds, Theorem 1 gives a type, so W fails on untypable terms. $\square$

**Termination.** Each call of W recurses on proper subterms, and MGU always stops, so W stops on each input. The number of calls is the number of nodes of $e$. The time is not polynomial: see the complexity section of the page.

## References

- Luis Damas and Robin Milner, Principal type-schemes for functional programs, POPL 1982, pages 207 to 212. The statement of soundness and completeness of W.
- Luis Damas, Type assignment in programming languages, PhD thesis, University of Edinburgh, 1985. The full proofs, and the equivalence of the declarative and the syntax-directed rules.
- Oukseh Lee and Kwangkeun Yi, Proofs about a folklore let-polymorphic type inference algorithm, ACM TOPLAS 20(4), 1998, pages 707 to 723. Soundness and completeness proofs in the same style for W and for the top-down algorithm M.
