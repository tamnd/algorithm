---
title: Progress and preservation for the simply typed lambda calculus with Booleans and integers
proves: [statement]
status: full
---

This file proves the statement on the page for the system defined on the [simply typed lambda calculus](/simply-typed-lambda-calculus/) page: types $\mathsf{Bool}$, $\mathsf{Int}$ and $T_1 \to T_2$; terms $x$, $\lambda x{:}T.\,t$, $t_1\,t_2$, $\mathsf{true}$, $\mathsf{false}$, $\mathsf{if}\ t_1\ \mathsf{then}\ t_2\ \mathsf{else}\ t_3$, integer literals $n$ and $t_1 + t_2$; the typing rules T-Var, T-Abs, T-App, T-True, T-False, T-If, T-Int and T-Add; and the call-by-value rules E-App1, E-App2, E-AppAbs, E-IfTrue, E-IfFalse, E-If, E-Add1, E-Add2 and E-AddInt. The values are $\lambda x{:}T.\,t$, $\mathsf{true}$, $\mathsf{false}$ and the literals $n$.

Terms are taken up to the renaming of bound variables. We use the variable convention: in any term, context or rule instance under discussion, the bound variables are chosen different from each other and from the free variables and the variables of the context. Substitution $[x := s]t$ is capture avoiding. A context is a list of distinct variables with types, and we write $x{:}S \in \Gamma$ for membership.

The proof follows the order of Pierce, Types and Programming Languages, Section 9.3.

## Lemma 1 (inversion)

1. If $\Gamma \vdash x : R$, then $x{:}R \in \Gamma$.
2. If $\Gamma \vdash \lambda x{:}T_1.\,t_2 : R$, then $R = T_1 \to R_2$ for some $R_2$ with $\Gamma, x{:}T_1 \vdash t_2 : R_2$.
3. If $\Gamma \vdash t_1\,t_2 : R$, then there is a $T_{11}$ with $\Gamma \vdash t_1 : T_{11} \to R$ and $\Gamma \vdash t_2 : T_{11}$.
4. If $\Gamma \vdash \mathsf{true} : R$ or $\Gamma \vdash \mathsf{false} : R$, then $R = \mathsf{Bool}$.
5. If $\Gamma \vdash \mathsf{if}\ t_1\ \mathsf{then}\ t_2\ \mathsf{else}\ t_3 : R$, then $\Gamma \vdash t_1 : \mathsf{Bool}$, $\Gamma \vdash t_2 : R$ and $\Gamma \vdash t_3 : R$.
6. If $\Gamma \vdash n : R$, then $R = \mathsf{Int}$.
7. If $\Gamma \vdash t_1 + t_2 : R$, then $R = \mathsf{Int}$, $\Gamma \vdash t_1 : \mathsf{Int}$ and $\Gamma \vdash t_2 : \mathsf{Int}$.

*Proof.* The typing relation is the smallest relation closed under the rules, so each derivation ends in some rule whose conclusion matches the term. For each form of term exactly one rule has a conclusion of that form: T-Var for variables, T-Abs for abstractions, T-App for applications, T-True and T-False for the two constants, T-If for conditionals, T-Int for literals and T-Add for sums. Each claim is the premise list of that rule, read off with the conclusion matched to $R$. $\square$

## Lemma 2 (canonical forms)

Let $v$ be a value.

1. If $\vdash v : \mathsf{Bool}$, then $v$ is $\mathsf{true}$ or $\mathsf{false}$.
2. If $\vdash v : \mathsf{Int}$, then $v$ is a literal $n$.
3. If $\vdash v : T_1 \to T_2$, then $v = \lambda x{:}T_1.\,t$ for some $x$ and $t$.

*Proof.* A value has one of four forms. By Lemma 1, an abstraction has an arrow type, $\mathsf{true}$ and $\mathsf{false}$ have type $\mathsf{Bool}$, and a literal has type $\mathsf{Int}$. The three types $\mathsf{Bool}$, $\mathsf{Int}$ and $T_1 \to T_2$ are pairwise different, so in case 1 only the Boolean constants are possible, in case 2 only literals, and in case 3 only abstractions. In case 3, Lemma 1.2 also gives that the annotation is $T_1$. $\square$

## Theorem 1 (progress)

If $\vdash t : T$ (in the empty context), then $t$ is a value or there is a $t'$ with $t \to t'$.

*Proof.* By induction on the derivation of $\vdash t : T$. Consider the last rule.

- **T-Var.** Impossible: the context is empty, so no premise $x{:}T \in \emptyset$ holds.
- **T-Abs, T-True, T-False, T-Int.** The term is a value.
- **T-App.** Here $t = t_1\,t_2$ with $\vdash t_1 : T_{11} \to T$ and $\vdash t_2 : T_{11}$. By the induction hypothesis on $t_1$, either $t_1 \to t_1'$, and then E-App1 gives $t_1\,t_2 \to t_1'\,t_2$; or $t_1$ is a value. In the second case apply the induction hypothesis to $t_2$: either $t_2 \to t_2'$, and E-App2 gives $t_1\,t_2 \to t_1\,t_2'$; or $t_2$ is a value too. In that last case, Lemma 2.3 gives $t_1 = \lambda x{:}T_{11}.\,t_{12}$, and E-AppAbs gives $t_1\,t_2 \to [x := t_2]\,t_{12}$.
- **T-If.** Here $t = \mathsf{if}\ t_1\ \mathsf{then}\ t_2\ \mathsf{else}\ t_3$ with $\vdash t_1 : \mathsf{Bool}$. By induction, either $t_1 \to t_1'$ and E-If applies, or $t_1$ is a value. Then Lemma 2.1 gives $t_1 = \mathsf{true}$ or $t_1 = \mathsf{false}$, and E-IfTrue or E-IfFalse applies.
- **T-Add.** Here $t = t_1 + t_2$ with both parts of type $\mathsf{Int}$. If $t_1$ steps, E-Add1 applies. Otherwise $t_1$ is a value. If $t_2$ steps, E-Add2 applies. Otherwise both are values, Lemma 2.2 makes them literals $n_1$ and $n_2$, and E-AddInt gives $t \to n$ with $n = n_1 + n_2$.

Every case gives a value or a step. $\square$

## Lemma 3 (permutation and weakening)

1. If $\Gamma \vdash t : T$ and $\Delta$ is a permutation of $\Gamma$, then $\Delta \vdash t : T$.
2. If $\Gamma \vdash t : T$ and $x$ is not in the domain of $\Gamma$, then $\Gamma, x{:}S \vdash t : T$ for every $S$.

*Proof.* Both go by induction on the derivation. The only rule that reads the context is T-Var, and its premise $y{:}T \in \Gamma$ holds in any context with the same bindings, or with more bindings. T-Abs extends the context with its bound variable. By the variable convention, that variable differs from $x$ and from every variable of $\Gamma$, so the extended context is still a list of distinct variables, and the induction hypothesis applies to the premise. Every other rule passes the context unchanged to its premises. $\square$

## Lemma 4 (substitution)

If $\Gamma, x{:}S \vdash t : T$ and $\Gamma \vdash s : S$, then $\Gamma \vdash [x := s]\,t : T$.

*Proof.* By induction on the term $t$, for all $\Gamma$ and $T$ at once. Induction on the term, and not on the derivation, lets us use Lemma 3 on a premise and still apply the induction hypothesis, because the permuted derivation is a derivation for the same subterm. By Lemma 1, the last rule of the derivation is fixed by the form of $t$.

- **T-Var**, $t = z$ with $z{:}T \in (\Gamma, x{:}S)$. If $z = x$, then $T = S$ because the context binds $x$ once, and $[x := s]\,x = s$, which has type $S$ under $\Gamma$ by assumption. If $z \neq x$, then $[x := s]\,z = z$ and $z{:}T \in \Gamma$, so T-Var gives $\Gamma \vdash z : T$.
- **T-Abs**, $t = \lambda y{:}T_2.\,t_1$ with $T = T_2 \to T_1$ and $\Gamma, x{:}S, y{:}T_2 \vdash t_1 : T_1$. By the variable convention, $y \neq x$ and $y$ is not free in $s$, so $[x := s]\,t = \lambda y{:}T_2.\,[x := s]\,t_1$. By Lemma 3.1, $\Gamma, y{:}T_2, x{:}S \vdash t_1 : T_1$. By Lemma 3.2, $\Gamma, y{:}T_2 \vdash s : S$. The induction hypothesis gives $\Gamma, y{:}T_2 \vdash [x := s]\,t_1 : T_1$, and T-Abs gives $\Gamma \vdash [x := s]\,t : T_2 \to T_1$.
- **T-App**, $t = t_1\,t_2$. The premises are $\Gamma, x{:}S \vdash t_1 : T_{11} \to T$ and $\Gamma, x{:}S \vdash t_2 : T_{11}$. The induction hypothesis gives the same judgments for $[x := s]\,t_1$ and $[x := s]\,t_2$ under $\Gamma$, and T-App gives $\Gamma \vdash ([x := s]\,t_1)\,([x := s]\,t_2) : T$, which is $[x := s]\,t$.
- **T-If** and **T-Add** are the same as T-App: substitute into each premise by induction and apply the rule again.
- **T-True, T-False, T-Int.** The term has no variables, so $[x := s]\,t = t$, and the same rule types it under $\Gamma$. $\square$

## Theorem 2 (preservation)

If $\Gamma \vdash t : T$ and $t \to t'$, then $\Gamma \vdash t' : T$.

*Proof.* By induction on the derivation of $\Gamma \vdash t : T$. Consider the last rule.

- **T-Var, T-Abs, T-True, T-False, T-Int.** The term is a variable or a value. No evaluation rule has a variable or a value on its left side, so $t \to t'$ is impossible, and the claim holds vacuously.
- **T-App**, $t = t_1\,t_2$ with $\Gamma \vdash t_1 : T_{11} \to T$ and $\Gamma \vdash t_2 : T_{11}$. Three rules can give $t \to t'$.
  - E-App1: $t' = t_1'\,t_2$ with $t_1 \to t_1'$. The induction hypothesis gives $\Gamma \vdash t_1' : T_{11} \to T$, and T-App gives $\Gamma \vdash t' : T$.
  - E-App2: $t' = t_1\,t_2'$ with $t_2 \to t_2'$. The same argument on $t_2$.
  - E-AppAbs: $t_1 = \lambda x{:}T_{11}'.\,t_{12}$, $t_2$ is a value, and $t' = [x := t_2]\,t_{12}$. Lemma 1.2 applied to $\Gamma \vdash t_1 : T_{11} \to T$ gives $T_{11}' = T_{11}$ and $\Gamma, x{:}T_{11} \vdash t_{12} : T$. Lemma 4 with $s = t_2$ gives $\Gamma \vdash t' : T$.
- **T-If**, $t = \mathsf{if}\ t_1\ \mathsf{then}\ t_2\ \mathsf{else}\ t_3$ with $\Gamma \vdash t_1 : \mathsf{Bool}$, $\Gamma \vdash t_2 : T$ and $\Gamma \vdash t_3 : T$. For E-IfTrue, $t' = t_2$, and for E-IfFalse, $t' = t_3$; both have type $T$ by the premises. For E-If, $t' = \mathsf{if}\ t_1'\ \mathsf{then}\ t_2\ \mathsf{else}\ t_3$ with $t_1 \to t_1'$; the induction hypothesis gives $\Gamma \vdash t_1' : \mathsf{Bool}$, and T-If gives $\Gamma \vdash t' : T$.
- **T-Add**, $t = t_1 + t_2$ with $T = \mathsf{Int}$. For E-Add1 and E-Add2, use the induction hypothesis on the part that steps and apply T-Add again. For E-AddInt, $t'$ is a literal, and T-Int gives $\Gamma \vdash t' : \mathsf{Int}$. $\square$

## Corollary (safety)

If $\vdash t : T$ and $t \to^* t'$, then $t'$ is not stuck: $t'$ is a value of type $T$, or $t' \to t''$ for some $t''$.

*Proof.* By induction on the number $k$ of steps in $t \to^* t'$, Theorem 2 gives $\vdash t' : T$: for $k = 0$ this is the assumption, and for $k + 1$ apply Theorem 2 to the last step. Then Theorem 1 says $t'$ is a value or steps. If it is a value, it has type $T$. $\square$

## Remarks on the proof

- Progress needs the empty context. The open term $x$ has type $\mathsf{Int}$ under $x{:}\mathsf{Int}$, but it is not a value and does not step. Preservation holds in any context.
- Progress uses canonical forms, and canonical forms use the fact that the types of the different kinds of values are different. If a rule gave $\mathsf{true}$ the type $\mathsf{Int}$, Lemma 2.2 would fail, and the term $\mathsf{true} + 1$ would be well typed and stuck.
- Preservation uses substitution only in the case E-AppAbs. That is the step where computation happens. In systems with type variables, a second substitution lemma, for types, is needed in the case of type application.
- The proofs do not use the order of evaluation. With a call-by-name rule $(\lambda x{:}T.\,t)\,t_2 \to [x := t_2]\,t$ for every $t_2$, the same Lemma 4 gives preservation, and progress holds with the matching changes.
