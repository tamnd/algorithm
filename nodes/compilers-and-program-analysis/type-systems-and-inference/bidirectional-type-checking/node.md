---
tag: 25GB8S
kind: technique
slug: bidirectional-type-checking
name: Bidirectional type checking
aliases:
- bidirectional typing
- local type inference
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Splits the typing judgment into a checking mode and a synthesis mode, so annotations are needed only where the two modes meet.
prereqs: [type-checking-problem, simply-typed-lambda-calculus, type-inference-problem]
see_also: [system-f-inference-undecidability, type-checking-problem, subtyping, system-f, hindley-milner-type-system, dependent-types, curry-howard-correspondence]
sources:
  - paper: doi:10.1145/3450952
    title: Jana Dunfield and Neel Krishnaswami, Bidirectional typing, ACM Computing Surveys 54(5), 2021, Article 98
    locator: Section 2 (the bidirectional simply typed lambda calculus with Var, Anno, the arrow rules and the mode switch Sub), Section 4 (the Pfenning recipe, with the remark in Section 4.1 that annotations on redexes alone are not enough with binding eliminations), Section 5 (polymorphism), Section 7 and Figure 2 (a bidirectional system for beta-normal, eta-long terms), Section 9.1 (dependent, refinement and intersection types), Section 10 (history)
  - paper: "Jana Dunfield and Frank Pfenning, Tridirectional typechecking, ACM Symposium on Principles of Programming Languages (POPL 2004), pages 281 to 292"
    locator: the design recipe (introduction rules check, elimination rules synthesize) as restated in Section 4 of the survey above
  - paper: doi:10.1145/345099.345100
    title: Benjamin C. Pierce and David N. Turner, ACM Transactions on Programming Languages and Systems 22(1), 2000, pages 1 to 44
    locator: Section 1.1 (design goals for partial type inference), the bidirectional propagation of types, and the synthesis of type arguments at polymorphic applications by local constraint solving
  - paper: doi:10.1145/2500365.2500582
    title: Jana Dunfield and Neelakantan R. Krishnaswami, Complete and easy bidirectional typechecking for higher-rank polymorphism, ACM International Conference on Functional Programming (ICFP 2013), pages 429 to 442
    locator: the declarative system, the algorithmic system with ordered contexts and existential variables, and its soundness, completeness and decidability theorems
  - paper: "Simon Peyton Jones, Dimitrios Vytiniotis, Stephanie Weirich and Mark Shields, Practical type inference for arbitrary-rank types, Journal of Functional Programming 17(1), 2007"
    locator: the bidirectional system for arbitrary-rank types that GHC uses, with checking and inference modes
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 10 (a typechecker for the simply typed lambda calculus), Chapter 16 (algorithmic subtyping), Section 23.6 (erasure and type reconstruction in System F)
---

Bidirectional type checking splits the typing judgment in two. In *checking* mode, the type is an input: does $e$ have type $A$? In *synthesis* mode, the type is an output: what type does $e$ have? Each typing rule chooses a mode for its conclusion and for each premise, so the rules read as two mutually recursive functions. Type information flows down from annotations and function types into the term, and up from variables. A lambda needs no annotation when its type is known from outside. An annotation is needed only where a term that can only be checked sits in a place that must synthesize. The technique sits between full [type checking](/type-checking-problem/) of explicitly typed terms and full [type inference](/type-inference-problem/). It also scales to systems where inference is [undecidable](/system-f-inference-undecidability/), such as higher-rank polymorphism and dependent types.

## In plain words

A type checker can work in two ways. Sometimes it already knows the type that a piece of code must have, for example because the code is an argument to a function whose parameter type is known. Then it only has to check the code against that type. At other times it must work out the type from the code alone, for example for a variable whose type is in the context.

Bidirectional checking chooses one of the two ways for every kind of expression. Variables and function calls report their types. Function literals and branches are checked against a type given from outside. When a reporting expression appears where a check is needed, the checker compares the two types. When a checked-only expression appears where a report is needed, the programmer must write its type. That case is rare, so a few type signatures are usually enough.

## When it applies

- The language has a typing judgment, and the rules can be oriented so that every input of each premise is known when the premise is checked. This is the *mode correctness* of the rules.
- Full inference is undecidable, too expensive, or gives poor error messages, but the programmer will write some types. Typical cases are higher-rank polymorphism, [subtyping](/subtyping/) with polymorphism, dependent types and refinement types.
- The terms are mostly in normal form, as in ordinary programs. Each beta-redex in the source, such as a lambda applied in place, needs one annotation.

It does not apply when no annotations are allowed at all. For annotation-free ML programs, [Hindley-Milner](/hindley-milner-type-system/) inference with unification is the right tool.

## The template

Write $\Gamma \vdash e \Rightarrow A$ for "$e$ synthesizes $A$" and $\Gamma \vdash e \Leftarrow A$ for "$e$ checks against $A$". Add the annotated term $(e : A)$ to the syntax. For the simply typed lambda calculus with $\mathsf{Int}$, $\mathsf{Bool}$, $+$ and $\mathsf{if}$, the rules are as follows (Dunfield and Krishnaswami 2021, Section 2, extended with the base types).

- **Var⇒:** if $x : A$ is in $\Gamma$, then $\Gamma \vdash x \Rightarrow A$.
- **Lit⇒:** $\Gamma \vdash n \Rightarrow \mathsf{Int}$, and $\Gamma \vdash \mathsf{true} \Rightarrow \mathsf{Bool}$, $\Gamma \vdash \mathsf{false} \Rightarrow \mathsf{Bool}$.
- **Anno⇒:** if $\Gamma \vdash e \Leftarrow A$, then $\Gamma \vdash (e : A) \Rightarrow A$.
- **App⇒:** if $\Gamma \vdash e_1 \Rightarrow A \to B$ and $\Gamma \vdash e_2 \Leftarrow A$, then $\Gamma \vdash e_1\,e_2 \Rightarrow B$.
- **Add⇒:** if $\Gamma \vdash e_1 \Leftarrow \mathsf{Int}$ and $\Gamma \vdash e_2 \Leftarrow \mathsf{Int}$, then $\Gamma \vdash e_1 + e_2 \Rightarrow \mathsf{Int}$.
- **Abs⇐:** if $\Gamma, x : A \vdash e \Leftarrow B$, then $\Gamma \vdash \lambda x.\,e \Leftarrow A \to B$.
- **If⇐:** if $\Gamma \vdash e_1 \Leftarrow \mathsf{Bool}$, $\Gamma \vdash e_2 \Leftarrow A$ and $\Gamma \vdash e_3 \Leftarrow A$, then $\Gamma \vdash \mathsf{if}\ e_1\ \mathsf{then}\ e_2\ \mathsf{else}\ e_3 \Leftarrow A$.
- **Sub⇐ (mode switch):** if $\Gamma \vdash e \Rightarrow A$ and $A = B$, then $\Gamma \vdash e \Leftarrow B$.

The lambda carries no type. The mode switch goes one way only: a synthesizing term can be checked, but a checking-only term must be annotated to synthesize.

**How to orient rules: the Pfenning recipe.** Dunfield and Pfenning (2004) gave a recipe, which the survey restates in Section 4.

1. Find the *principal judgment* of each rule: the one that holds the connective that the rule introduces or eliminates. For an introduction rule it is usually the conclusion. For an elimination rule it is the first premise.
2. Make the principal judgment *checking* for introduction rules and *synthesizing* for elimination rules. So $\lambda$, the arrow introduction, checks, and application, the arrow elimination, synthesizes its function.
3. Orient the other premises so that known types are used: if a type is already known, check against it. In App⇒, the type $A$ is known once $e_1$ synthesizes, so $e_2$ is checked against $A$.
4. Variables synthesize, annotations synthesize and check their body, and one mode switch rule links the two modes.

**The algorithm.** Each rule has a distinct term form in its conclusion, except Sub⇐, which applies only to term forms that have no checking rule. So the rules are syntax-directed and read as code:

```text
synth(G, e):
  x          -> G(x)
  n          -> Int
  (e : A)    -> check(G, e, A); A
  e1 e2      -> A -> B := synth(G, e1) (else error "not a function"); check(G, e2, A); B
  e1 + e2    -> check(G, e1, Int); check(G, e2, Int); Int
  otherwise  -> error "annotation needed"

check(G, e, T):
  \x. e1               -> T must be A -> B; check(G + x:A, e1, B)
  if e1 then e2 else e3 -> check(G, e1, Bool); check(G, e2, T); check(G, e3, T)
  otherwise            -> A := synth(G, e); A must equal T
```

**Soundness.** If $\Gamma \vdash e \Rightarrow A$ or $\Gamma \vdash e \Leftarrow A$, then the term $|e|$ with annotations erased has type $A$ in the ordinary (Curry-style) STLC. *Proof:* induction on the derivation. Each bidirectional rule, with its arrows read as colons, is an STLC rule. Anno⇒ erases to its premise, and Sub⇐ with $A = B$ is the identity.

**Completeness for normal forms.** Define neutral terms $u$ and normal terms $m$ by
$$u ::= x \mid n \mid \mathsf{true} \mid \mathsf{false} \mid u\ m \mid m + m, \qquad m ::= u \mid \lambda x.\,m \mid \mathsf{if}\ m\ \mathsf{then}\ m\ \mathsf{else}\ m.$$
If $\Gamma \vdash u : A$ in the STLC, then $\Gamma \vdash u \Rightarrow A$. If $\Gamma \vdash m : A$, then $\Gamma \vdash m \Leftarrow A$. *Proof:* mutual induction on the term. A variable synthesizes its context type, and literals synthesize their types. For $u\ m$, the STLC derivation gives $u : B \to A$ and $m : B$. By induction, $u \Rightarrow B \to A$ and $m \Leftarrow B$, so App⇒ gives $u\ m \Rightarrow A$. For $m_1 + m_2$, the STLC gives $A = \mathsf{Int}$ and both operands of type $\mathsf{Int}$, and Add⇒ applies. For $\lambda x.m$, we have $A = B \to C$ and $\Gamma, x{:}B \vdash m : C$, and Abs⇐ applies. For $\mathsf{if}$, If⇐ applies by induction. For a neutral $m = u$, induction gives $u \Rightarrow A$, and Sub⇐ gives $u \Leftarrow A$. $\square$

So a normal term needs no annotation at all, as long as its expected type is given at the top. Every other typable term becomes checkable when each term in a synthesis place that is not neutral gets an annotation. In this language, these places are the heads of beta-redexes and the heads of applications whose function is an $\mathsf{if}$.

**Cost.** Each node of the term is visited once. The only other work is the type comparison in Sub⇐. With hash-consed types each comparison takes constant time, so the whole check is linear in the size of the annotated term, as for the [type checking problem](/type-checking-problem/).

## Classic examples

A script runs the checker above on each example and logs the rules it uses.

**Twice, with no annotation inside.** Check $\lambda f.\,\lambda x.\,f\,(f\,x) \Leftarrow (\mathsf{Int} \to \mathsf{Int}) \to \mathsf{Int} \to \mathsf{Int}$. Abs⇐ twice puts $f : \mathsf{Int} \to \mathsf{Int}$ and $x : \mathsf{Int}$ in the context, and leaves $f\,(f\,x) \Leftarrow \mathsf{Int}$. This is not a lambda or an if, so Sub⇐ synthesizes it. App⇒ synthesizes $f \Rightarrow \mathsf{Int} \to \mathsf{Int}$ and checks $f\,x \Leftarrow \mathsf{Int}$, which in turn goes through Sub⇐, App⇒, Var⇒ for $f$, and Sub⇐ and Var⇒ for $x$. The script logs 10 rule uses: 2 Abs⇐, 3 Sub⇐, 2 App⇒ and 3 Var⇒. Neither binder needed a type.

**A redex needs an annotation.** $(\lambda x.\,x + 1)\ 3$ fails in both modes. App⇒ must synthesize the type of its function, and no rule synthesizes a lambda. The script reports "cannot synthesize a type for a lam" after one rule in synthesis mode, and after two rules in checking mode, where Sub⇐ comes first. With one annotation, $((\lambda x.\,x + 1) : \mathsf{Int} \to \mathsf{Int})\ 3 \Rightarrow \mathsf{Int}$ succeeds, with 11 rule uses.

**An annotated function applied to arguments.** In the context $g : \mathsf{Int} \to \mathsf{Int}$, the term $(\mathit{twice} : (\mathsf{Int} \to \mathsf{Int}) \to \mathsf{Int} \to \mathsf{Int})\ g\ 3$ synthesizes $\mathsf{Int}$, with 17 rule uses. The arguments $g$ and $3$ are checked against the parameter types that the annotation provides.

**A conditional in function position.** With $b : \mathsf{Bool}$, the term $(\mathsf{if}\ b\ \mathsf{then}\ \lambda x.x\ \mathsf{else}\ \lambda x.\,x + 1)\ 3$ has no beta-redex, but it fails, because $\mathsf{if}$ only checks. Annotating the conditional with $\mathsf{Int} \to \mathsf{Int}$ fixes it: the script finds $\mathsf{Int}$ with 17 rule uses.

**Error location.** Checking $\lambda x.\,x + \mathsf{true} \Leftarrow \mathsf{Int} \to \mathsf{Int}$ fails with "expected Int, found Bool" at the subterm $\mathsf{true}$, because the expected type $\mathsf{Int}$ was pushed down to it. A unification-based checker would report a clash between two types and might name a different place.

**Partial application in checking mode.** With $f : \mathsf{Int} \to \mathsf{Int} \to \mathsf{Int}$ and $x : \mathsf{Int}$, the term $f\,x$ checks against $\mathsf{Int} \to \mathsf{Int}$ through Sub⇐, in 5 rule uses.

## Variations

- **Pierce and Turner (2000).** This paper made the idea widely known, and it is the earliest bidirectional paper that is often cited (survey, Section 10). It combines two parts for a language with subtyping and impredicative polymorphism. The first is the bidirectional propagation of types, as above. The second is the synthesis of missing type arguments at each polymorphic application, by solving the subtyping constraints of that one application alone. The design goal is to remove the annotations that are both common and boring, such as type arguments, and to keep the ones that serve as documentation (Section 1.1). Type arguments are inferred only for prenex polymorphic functions. Other instantiations must be written.
- **Subtyping.** Replace the equality in Sub⇐ by the [subtype](/subtyping/) check $A <: B$. This is the place where subsumption is used, and it keeps the system syntax-directed (Pierce, Chapter 16).
- **Higher-rank polymorphism.** Dunfield and Krishnaswami (2013) give a bidirectional system for predicative higher-rank polymorphism. It instantiates quantifiers with existential variables in an ordered context, and they prove it sound, complete and decidable. Peyton Jones, Vytiniotis, Weirich and Shields (2007) describe the arbitrary-rank system that GHC uses. Both escape [Wells' theorem](/system-f-inference-undecidability/) because the programmer writes the polymorphic types of arguments.
- **Normal forms only.** Remove Anno⇒ and allow Sub⇐ only at base types. Then the typable terms are exactly the beta-normal, eta-long terms (survey, Section 7 and Figure 2). Under the [Curry-Howard correspondence](/curry-howard-correspondence/), synthesis is elimination and checking is introduction, and this system is the normal natural deduction proofs.
- **Dependent types.** Type checkers for [dependent types](/dependent-types/) check a lambda against a known Pi type, and synthesize the types of variables and applications, in the same way. The survey (Section 9.1) lists many such systems.
- **Sum elimination.** A `case` can have a checking rule and a synthesizing rule. The original recipe had only the checking one (survey, Section 4, footnote 2).

## Pitfalls

- **It is not inference.** Bidirectional checking does not find the types of unannotated binders that occur in synthesis places. `let f = fun x -> x + 1 in f 3` fails, because the let rule synthesizes the bound term. The script reports this failure. One annotation, `let f = (fun x -> x + 1 : Int -> Int) in f 3`, fixes it. Checking and inference are different problems, and a bidirectional system only promises the first.
- **"Annotations only at redexes" is false in general.** Dunfield and Pfenning claimed that annotations are needed only at redexes. The survey (Section 4.1) shows that this holds for eliminations that do not bind variables. With binding eliminations such as `case`, some terms with no redex still need annotations. The conditional example above shows the same thing with `if`.
- **Mode correctness.** Each premise must have all its inputs known when it is checked. A rule such as App with a checking function premise would need the type of the function before it is known, so the algorithm would have to guess.
- **One mode switch, at the right place.** If a checking rule and Sub⇐ can both apply to the same term form, the system is no longer syntax-directed, and the algorithm must backtrack. Sub⇐ should apply only to forms that have no checking rule.
- **The equality in Sub⇐.** With polymorphism, types must be compared up to the renaming of bound variables. With type-level computation, as in dependent types, they must be compared up to conversion, which is decidable only when that computation terminates.
- **Annotation placement in the grammar.** If $(e : A)$ is parsed with low precedence, `fun x -> e : T` can mean an annotated lambda or a lambda with an annotated body. The two give different checks.

## Exercises

1. Extend the template with pairs $\langle e_1, e_2 \rangle$ and projections $\pi_1 e$, $\pi_2 e$. Use the Pfenning recipe to choose the modes, and check that the completeness proof for normal forms still goes through.
2. Give the bidirectional rule for `let x = e1 in e2` in checking mode, where $e_2$ is checked against the expected type. Which terms does it accept that the synthesizing let rule rejects?
3. Prove that if $\Gamma \vdash e \Rightarrow A$ and $\Gamma \vdash e \Rightarrow B$, then $A = B$.
4. Show that $\lambda f.\,f\,(\lambda x.\,x)$ checks against $((\mathsf{Int} \to \mathsf{Int}) \to \mathsf{Bool}) \to \mathsf{Bool}$ with no annotation, and count the rule uses.
5. Replace the equality in Sub⇐ by the subtyping relation of the [subtyping](/subtyping/) page with records. Show that the resulting system is sound for the declarative system with the subsumption rule.

## References
