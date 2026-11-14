---
title: The Curry-Howard correspondence between the simply typed lambda calculus and implicational natural deduction
proves: [statement]
status: full
---

This file proves parts 1 to 3 of the statement in full. Part 4 uses strong normalization of the simply typed lambda calculus, which is proved on the [reducibility method](/reducibility-method/) page and in Girard, Lafont and Taylor, Proofs and Types, Chapter 6. Given that theorem, part 4 is proved here in full.

## Setting

**Formulas and types.** Fix a set of atoms $p, q, \dots$. Formulas, which are also the types, are $A ::= p \mid A \to A$.

**Natural deduction NJ($\to$).** A derivation has open hypotheses, each with a label. We write $\Gamma \vdash A$ where $\Gamma = x_1{:}A_1, \dots, x_k{:}A_k$ lists the labels of the open hypotheses with their formulas; the labels are distinct, and two labels may carry the same formula. The rules are:

- (Ax) If $x{:}A \in \Gamma$, then $\Gamma \vdash A$ by the hypothesis $x$.
- ($\to$I) From a derivation of $\Gamma, x{:}A \vdash B$, infer $\Gamma \vdash A \to B$ and discharge the hypotheses labelled $x$.
- ($\to$E) From derivations of $\Gamma \vdash A \to B$ and $\Gamma \vdash A$, infer $\Gamma \vdash B$.

Two derivations are the same if they differ only in the names of discharged labels.

**Terms.** The Church-style terms are $t ::= x \mid \lambda x{:}A.\,t \mid t\,t$, up to renaming of bound variables, with the typing rules T-Var, T-Abs and T-App of the [simply typed lambda calculus](/simply-typed-lambda-calculus/).

**Detours.** A *detour* in a derivation is an application of ($\to$I) whose conclusion $A \to B$ is at once the major premise of ($\to$E). Its *reduction* (Prawitz) takes the subderivation $D$ of $\Gamma, x{:}A \vdash B$ and the subderivation $E$ of $\Gamma \vdash A$, and replaces each use of the hypothesis $x$ in $D$ by a copy of $E$. The result is a derivation of $\Gamma \vdash B$. A derivation is *normal* if it has no detour.

## Part 1: erasure

*Claim.* If $\Gamma \vdash t : A$, then the derivation of the typing judgment, with each term removed, is an NJ($\to$) derivation of $\Gamma \vdash A$.

*Proof.* By induction on the typing derivation. T-Var with $x{:}A \in \Gamma$ becomes (Ax) with hypothesis $x$. T-Abs, from $\Gamma, x{:}A \vdash t : B$ to $\Gamma \vdash \lambda x{:}A.\,t : A \to B$, becomes ($\to$I) on the erased premise, discharging $x$. T-App becomes ($\to$E) on the two erased premises. Each rule has the same premises and conclusion once terms are removed, so the result is a derivation. $\square$

Write $\lvert \mathcal{D} \rvert$ for this erasure of a typing derivation $\mathcal{D}$.

## Part 2: the bijection

*Claim.* For each $\Gamma$ and $A$, the map $t \mapsto \lvert \mathcal{D}_t \rvert$, where $\mathcal{D}_t$ is the typing derivation of $\Gamma \vdash t : A$, is a bijection from the terms $t$ with $\Gamma \vdash t : A$ to the NJ($\to$) derivations of $\Gamma \vdash A$.

*Proof.* First, the map is well defined: by the inversion lemma for T-Var, T-Abs and T-App (one rule per form of term, and in T-App the type of the argument is fixed by uniqueness of types), each typable Church term has exactly one typing derivation $\mathcal{D}_t$.

Define the inverse $\mathrm{tm}$ on derivations by induction:

- $\mathrm{tm}$ of the hypothesis $x$ is the variable $x$.
- $\mathrm{tm}$ of ($\to$I) discharging $x{:}A$ above a derivation $D$ is $\lambda x{:}A.\,\mathrm{tm}(D)$.
- $\mathrm{tm}$ of ($\to$E) with premises $D_1$ and $D_2$ is $\mathrm{tm}(D_1)\,\mathrm{tm}(D_2)$.

By induction on $D$, $\Gamma \vdash \mathrm{tm}(D) : A$, because each clause is the matching typing rule. By induction on $D$, $\lvert \mathcal{D}_{\mathrm{tm}(D)} \rvert = D$: each clause makes a term whose last typing rule erases to the last rule of $D$, and the subterms come from the subderivations. By induction on $t$, $\mathrm{tm}(\lvert \mathcal{D}_t \rvert) = t$, for the same reason. Renaming a discharged label on one side is renaming a bound variable on the other, so the two notions of sameness match. $\square$

## Part 3: beta reduction is detour reduction

*Claim.* Let $\Gamma \vdash t : A$. Then $t$ has a beta-redex if and only if $\lvert \mathcal{D}_t \rvert$ has a detour. Contracting a redex $(\lambda x{:}B.\,s)\,u$ in $t$ gives the term whose derivation is the reduction of the matching detour. So $t$ is beta-normal if and only if its derivation is normal.

*Proof.* A subterm $(\lambda x{:}B.\,s)\,u$ is typed by T-App whose first premise is T-Abs, and this erases to ($\to$E) whose major premise is ($\to$I): a detour. Conversely, by Part 2, a detour is the image of a T-App whose function premise ends in T-Abs, and a term typed that way is a redex. So redexes and detours are in one-to-one correspondence, by position.

Let $\mathcal{S}$ be the derivation of $\Gamma, x{:}B \vdash s : C$ and $\mathcal{U}$ that of $\Gamma \vdash u : B$. The substitution lemma (proved in full for this calculus on the [type soundness](/type-soundness/) page) builds the derivation of $\Gamma \vdash [x := u]\,s : C$ by induction on $s$: at each occurrence of the variable $x$ it puts a copy of $\mathcal{U}$, weakened by the bound variables of $s$ above that occurrence, and it keeps every other rule. After erasure this is exactly Prawitz's reduction: each use of the hypothesis $x$ in $\lvert \mathcal{S} \rvert$ is replaced by a copy of $\lvert \mathcal{U} \rvert$. The context of the whole term is unchanged, because a redex inside $t$ sits under the same rules before and after the step. $\square$

## Part 4: normalization

*Claim.* Every NJ($\to$) derivation reduces, by any sequence of detour reductions, in finitely many steps, to a normal derivation of the same sequent.

*Proof.* Let $D$ be a derivation of $\Gamma \vdash A$, and $t = \mathrm{tm}(D)$. By Part 3, a sequence of detour reductions from $D$ is the image of a sequence of beta steps from $t$, of the same length. By strong normalization of the simply typed lambda calculus (Tait 1967), every such sequence from $t$ is finite. When no step is possible, the term is beta-normal, and by Part 3 the derivation is normal. Each step keeps the sequent, by Part 3 and preservation. $\square$

## Corollary: Peirce's law has no proof

*Claim.* For distinct atoms $p$ and $q$, there is no closed term of type $((p \to q) \to p) \to p$, so the formula has no NJ($\to$) proof.

*Proof.* By Parts 2 and 4 it is enough to show that there is no closed beta-normal term $t$ of this type. A beta-normal term has the form $\lambda x_1 \dots x_k.\ y\,N_1 \cdots N_m$ with $k, m \geq 0$, a variable $y$ at the head and beta-normal $N_i$, because a term that is not an abstraction is a variable applied to arguments (otherwise its leftmost head would be an abstraction applied to an argument, a redex).

- $t$ is closed, so it is not of the form $y\,N_1 \cdots N_m$ with $y$ free. So $t = \lambda f{:}(p \to q) \to p.\ N$ with $f{:}(p \to q) \to p \vdash N : p$.
- $N$ has the atom type $p$, so it is not an abstraction, and $N = y\,N_1 \cdots N_m$ with $y = f$, the only variable. The type $(p \to q) \to p$ ends in $p$ after one argument, so $N = f\,M$ with $f \vdash M : p \to q$.
- $M$ is an abstraction or a head form. A head form has head $f$, and its type is $(p \to q) \to p$ with no argument or $p$ with one argument. Neither is $p \to q$. So $M = \lambda x{:}p.\ P$ with $f, x{:}p \vdash P : q$.
- $P$ has the atom type $q$, so it is a head form with head $f$ or $x$. A head form with head $f$ has type $(p \to q) \to p$ or $p$, and a head form with head $x$ has type $p$. None is $q$, because $p \neq q$.

So no normal term exists, and no term exists. $\square$

The same argument with $p = q$ finds the term $\lambda f.\ f\,(\lambda x.\ x)$, so the atoms must be distinct. A depth-bounded search over long normal forms, run as a script, finds no inhabitant of Peirce's law, one of $p \to q \to p$, and one of the type of $S$.
