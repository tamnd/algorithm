---
tag: PHJYVS
kind: theorem
slug: curry-howard-correspondence
name: Curry-Howard correspondence
aliases:
- propositions as types
- proofs as programs
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Simple types are the formulas of intuitionistic implicational logic, typed lambda terms are its natural deduction proofs, and beta reduction is the removal of detours from proofs.
prereqs: [simply-typed-lambda-calculus]
see_also: [combinatory-logic, lambda-calculus, system-f, reducibility-method, type-soundness, dependent-types, linear-types, continuation-passing-style]
sources:
  - paper: "William A. Howard, The formulae-as-types notion of construction, in J. P. Seldin and J. R. Hindley (eds.), To H. B. Curry: Essays on Combinatory Logic, Lambda Calculus and Formalism, Academic Press, 1980, pages 479 to 490 (manuscript of 1969)"
    locator: Sections 1 and 2 (implicational formulas as types, terms as constructions, and the match of normalization of terms with normalization of proofs)
  - paper: doi:10.1145/2699407
    title: Philip Wadler, Propositions as types, Communications of the ACM 58(12), 2015, pages 75 to 84
    locator: the whole survey (history, the natural deduction and lambda calculus side by side, and the extensions to other logics)
  - book: isbn:9780521371810
    title: Jean-Yves Girard, Yves Lafont and Paul Taylor, Proofs and Types, Cambridge University Press, 1989
    locator: Chapter 2 (natural deduction), Chapter 3 (the Curry-Howard isomorphism), Chapter 4 (the normalization theorem), Chapter 6 (strong normalization), Chapter 11 (System F and second-order logic)
  - book: isbn:9780444520777
    title: Morten Heine Sorensen and Pawel Urzyczyn, Lectures on the Curry-Howard Isomorphism, Elsevier, 2006
    locator: Chapter 4 (the isomorphism for implicational logic), Chapter 5 (proofs as combinators, Hilbert systems), Chapter 6 (classical logic and control operators)
  - paper: "Haskell B. Curry and Robert Feys, Combinatory Logic, Volume I, North-Holland, 1958"
    locator: the chapter on functionality (the types of the basic combinators are the axioms of implicational logic)
  - paper: "Dag Prawitz, Natural Deduction: A Proof-Theoretical Study, Almqvist and Wiksell, 1965"
    locator: the normalization theorem for intuitionistic natural deduction and the reduction of detours
  - paper: doi:10.1016/0304-3975(79)90006-9
    title: Richard Statman, Intuitionistic propositional logic is polynomial-space complete, Theoretical Computer Science 9(1), 1979, pages 67 to 72
    locator: the main theorem (provability in intuitionistic implicational logic, and so inhabitation of simple types, is PSPACE-complete)
  - paper: "Timothy G. Griffin, A formulae-as-types notion of control, POPL 1990"
    locator: the typing of call/cc and the control operator C with classical tautologies such as double negation elimination
---

The Curry-Howard correspondence says that a type is a logical formula and a program of that type is a proof of the formula. In its first and most precise form, the types of the [simply typed lambda calculus](/simply-typed-lambda-calculus/) are the formulas of intuitionistic logic with implication only, the typed terms are exactly the natural deduction proofs, and one step of beta reduction is one step of the normalization of proofs. Curry saw the match for combinators in the 1930s and 1950s, and Howard stated it for natural deduction in 1969. It is the reason that a type checker can be a proof checker.

## Statement

Fix a set of atoms $p, q, \dots$. Formulas, which are also types, are $A ::= p \mid A \to A$. Natural deduction for intuitionistic implicational logic, NJ($\to$), proves judgments $\Gamma \vdash A$, where $\Gamma$ lists labelled hypotheses $x_1{:}A_1, \dots, x_k{:}A_k$. It has three rules: a hypothesis (Ax), implication introduction ($\to$I), which discharges a hypothesis, and implication elimination ($\to$E), which is modus ponens. A *detour* is a ($\to$I) whose conclusion is at once the major premise of a ($\to$E). Prawitz's reduction of a detour replaces each use of the discharged hypothesis by the proof of the minor premise. A derivation is *normal* if it has no detour. The terms are the Church-style terms $x$, $\lambda x{:}A.\,t$ and $t\,u$, typed by T-Var, T-Abs and T-App.

**Theorem (Curry-Howard).**

1. **Erasure.** If $\Gamma \vdash t : A$, then removing the terms from the typing derivation gives an NJ($\to$) derivation of $\Gamma \vdash A$.
2. **Bijection.** For each $\Gamma$ and $A$, erasure is a bijection between the terms $t$ with $\Gamma \vdash t : A$ (up to renaming of bound variables) and the NJ($\to$) derivations of $\Gamma \vdash A$ (up to renaming of discharged labels). T-Var, T-Abs and T-App match (Ax), ($\to$I) and ($\to$E).
3. **Reduction.** A beta-redex in $t$ is a detour in its derivation, and the beta step $(\lambda x{:}B.\,s)\,u \to [x := u]\,s$ is the reduction of that detour. So $t$ is beta-normal if and only if its derivation is normal.
4. **Normalization.** Every sequence of detour reductions of an NJ($\to$) derivation is finite, and it ends in a normal derivation of the same judgment.

**Corollary.** A formula $A$ is provable in NJ($\to$) if and only if the type $A$ has a closed term.

Natural deduction normalization is the natural deduction form of Gentzen's cut elimination: a detour is a cut, an introduction followed at once by an elimination of the same connective.

## In plain words

Read a type as a claim. The type "from A to B" is the claim "if A then B". A program of that type is a method that turns any evidence for A into evidence for B, and that is what a proof of "if A then B" is. Writing a function is proving an "if" claim; calling a function is using one. A program that builds a function only to call it at once is a proof with a pointless detour: it proves a general rule and then applies it once. Running that call is cutting out the detour. Because typed programs in this calculus always finish, every proof can be made direct. The match is with constructive logic, where a proof must give a method. Some classical laws, such as Peirce's law, have no program.

## Proof

The [proof file](proofs/main.md) has the full proof of parts 1 to 3, and of part 4 from strong normalization of the STLC, which it cites.

- **Erasure** is an induction on the typing derivation: each typing rule, with the terms removed, is a rule of NJ($\to$).
- **Bijection.** Church-style terms have unique typing derivations, so erasure is a function. Its inverse reads a term off a derivation: a hypothesis labelled $x$ gives the variable $x$, ($\to$I) discharging $x{:}A$ gives $\lambda x{:}A.\,\cdot$, and ($\to$E) gives application. Two inductions show the maps are inverse.
- **Reduction.** A redex $(\lambda x{:}B.\,s)\,u$ is typed by T-App above T-Abs, which erases to a detour. The substitution lemma builds the typing of $[x := u]\,s$ by putting a copy of the derivation of $u$ at each occurrence of $x$. That is exactly Prawitz's reduction.
- **Normalization.** By part 3, detour reductions of a derivation are beta steps of its term. The STLC is strongly normalizing (Tait 1967; the proof is on the [reducibility method](/reducibility-method/) page), so every such sequence is finite.

**Example: a detour.** The term $(\lambda f{:}p{\to}p.\ f)\ (\lambda x{:}p.\ x)$ has type $p \to p$. Its derivation first proves the general rule $(p \to p) \to (p \to p)$ by ($\to$I), then applies it to the proof $\lambda x.x$ of $p \to p$ by ($\to$E). One beta step gives $\lambda x{:}p.\ x$, the direct proof by one ($\to$I) over one hypothesis.

**Example: Peirce's law has no proof.** Let $p \neq q$. A closed normal term of type $((p \to q) \to p) \to p$ must be $\lambda f.\,N$ with $N : p$. An atom-typed normal term is a variable applied to arguments, and the only variable is $f$, so $N = f\,M$ with $M : p \to q$. A head form with head $f$ has type $(p \to q) \to p$ or $p$, so $M = \lambda x.\,P$ with $P : q$. Now the head of $P$ is $f$ or $x$, and neither can produce $q$. So there is no normal term, and by normalization no term at all. A depth-bounded search for long normal forms, run as a script, confirms this. The same search finds exactly one normal inhabitant of $p \to q \to p$, namely $\lambda x.\lambda y.\,x$ (the combinator $K$), and exactly one of $(p \to q \to r) \to (p \to q) \to p \to r$, namely $\lambda x.\lambda y.\lambda z.\ x\,z\,(y\,z)$ (the combinator $S$). Peirce's law holds in classical logic, so the correspondence is with intuitionistic logic.

## Consequences

The theorem extends connective by connective. Each extension has the same three parts: formulas as types, proofs as terms, normalization as evaluation.

- **Products, sums and the empty type.** Pairs $A \times B$ are conjunction, with pairing as $\wedge$I and projections as $\wedge$E. Tagged unions $A + B$ are disjunction, with `case` as $\vee$E. The empty type is falsity $\bot$, and $\neg A$ is $A \to \bot$.
- **Hilbert systems and combinators.** The types of $K : A \to B \to A$ and $S : (A \to B \to C) \to (A \to B) \to A \to C$ are the two axiom schemes of the Hilbert system for implication, and application is modus ponens. This was Curry's observation ([combinatory logic](/combinatory-logic/)). The translation of lambda terms to combinators is the deduction theorem.
- **Second-order logic.** [System F](/system-f/) is second-order intuitionistic propositional logic: $\forall\alpha.A$ is quantification over propositions. Normalization of System F implies the consistency of second-order arithmetic, so by Gödel's second incompleteness theorem Girard's normalization proof cannot be formalized inside second-order arithmetic.
- **Predicate logic.** [Dependent types](/dependent-types/) are predicate logic: a dependent function type $\Pi x{:}A.\,B(x)$ is $\forall x.\,B(x)$, and a dependent pair type is $\exists$. Automath (de Bruijn, 1968), Martin-Löf type theory, Coq, Agda and Lean rest on this.
- **Classical logic.** Griffin (1990) showed that `call/cc` can be given the type $((A \to B) \to A) \to A$, which is Peirce's law, and the control operator $C$ the type $\neg\neg A \to A$. Classical proofs are programs with control effects. The double-negation translations of classical logic into intuitionistic logic are [CPS translations](/continuation-passing-style/).
- **Linear logic.** Girard's linear logic corresponds to [linear types](/linear-types/), where each hypothesis is used exactly once.
- **Complexity.** Provability in intuitionistic implicational logic is the inhabitation problem for simple types, which is PSPACE-complete (Statman 1979). Type checking a proof term is proof checking, which takes linear time for this calculus.

## Tightness

- **Only intuitionistic logic.** Peirce's law, the excluded middle $A \vee \neg A$ and double negation elimination $\neg\neg A \to A$ are classical tautologies with no closed term in the pure typed lambda calculus. Adding them needs control operators, as above.
- **Termination is needed for consistency.** If the language has general recursion, for example $\mathsf{fix} : (A \to A) \to A$, then $\mathsf{fix}\ (\lambda x{:}A.\ x)$ has every type $A$, including $\bot$. The logic becomes inconsistent. This is why proof assistants require every function to terminate, and why ML or Haskell types are not sound as a logic.
- **The bijection needs Church style and labelled hypotheses.** In Curry style, one untyped term such as $\lambda x.\,x$ is the image of a derivation of $p \to p$ and of a derivation of $(q \to q) \to q \to q$. If hypotheses are not labelled, the two terms $\lambda x.\lambda y.\,x$ and $\lambda x.\lambda y.\,y$ of type $p \to p \to p$ give the same unlabelled proof tree, although they are different programs.
- **Proofs are finer than provability.** All the closed terms of type $(p \to p) \to p \to p$ prove the same formula, but they are the Church numerals $0, 1, 2, \dots$, an infinite set of different programs. The correspondence keeps the structure of proofs, not only provability.

## History

Curry noticed in 1934 that the types of the basic combinators are axioms of implicational logic, and Curry and Feys (1958) stated the match between combinator types and Hilbert-style proofs. Tait (1965) connected cut elimination with the normalization of typed terms. Prawitz (1965) proved normalization for natural deduction. Howard wrote "The formulae-as-types notion of construction" in 1969 and circulated it as a manuscript. It gave the match for natural deduction, extended it to first-order arithmetic with dependent types, and was published in 1980 in the Festschrift for Curry. De Bruijn's Automath (from 1968) used the same idea for computer-checked mathematics, and Martin-Löf (1971 onward) made it the base of a constructive type theory. Girard (1972) and Reynolds (1974) found System F, Girard from second-order logic. Lambek added the third side, cartesian closed categories. Wadler (2015) gives a survey.

## References
