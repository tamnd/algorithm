---
tag: MV580F
kind: theorem
slug: principal-type-theorem
name: Principal type theorem
aliases:
- principal type property
- Damas-Milner completeness theorem
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Every typable ML term has a principal type scheme of which all its other types are instances, and algorithm W computes it.
prereqs: [hindley-milner-type-system, algorithm-w, most-general-unifier]
see_also: [algorithm-j, let-polymorphism, type-inference-problem, simply-typed-lambda-calculus, system-f-inference-undecidability, constraint-based-type-inference, value-restriction, robinson-unification]
sources:
  - paper: doi:10.1145/582153.582176
    title: Luis Damas and Robin Milner, Principal type-schemes for functional programs, Ninth ACM Symposium on Principles of Programming Languages (POPL 1982), pages 207 to 212
    locator: the definitions of generic instance and principal type scheme, Theorem 1 (soundness of W), Theorem 2 (completeness of W) and the corollary that each typable expression has a principal type scheme
  - paper: doi:10.2307/1995158
    title: J. Roger Hindley, The principal type-scheme of an object in combinatory logic, Transactions of the American Mathematical Society 146, 1969, pages 29 to 60
    locator: the principal type-scheme theorem for combinatory logic, with the scheme found by Robinson unification
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 4 (algorithm W and its soundness theorem)
  - paper: "Luis Damas, Type assignment in programming languages, PhD thesis, University of Edinburgh, 1985"
    locator: the full proofs of soundness and completeness of W, and of the equivalence of the declarative and syntax-directed rules
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Section 22.5 (principal types for the simply typed calculus by constraint typing and unification) and Section 22.7 (let-polymorphism)
  - paper: doi:10.1145/291891.291892
    title: Oukseh Lee and Kwangkeun Yi, Proofs about a folklore let-polymorphic type inference algorithm, ACM Transactions on Programming Languages and Systems 20(4), 1998, pages 707 to 723
    locator: complete proofs of soundness and completeness of W and of the top-down algorithm M
---

The principal type theorem says that a typable term of the [Hindley-Milner type system](/hindley-milner-type-system/) has one most general type scheme, and that every other type of the term is an instance of it. [Algorithm W](/algorithm-w/) computes this scheme and fails on untypable terms. So an ML compiler can find the types of a whole program without one annotation, and the type it finds never rules out a correct use. Hindley proved the first form in 1969, for combinatory logic. Damas and Milner proved the form with `let`-polymorphism in 1982. It is the reason that ML-style languages can make type annotations optional.

## Statement

Use the syntax, types, schemes and rules of the [Hindley-Milner page](/hindley-milner-type-system/). A substitution $S$ maps type variables to types. For schemes, $\sigma \sqsubseteq \sigma'$ means that $\sigma'$ is a generic instance of $\sigma$: each type that is an instance of $\sigma'$ is an instance of $\sigma$.

**Definition.** A *principal type scheme* of a term $e$ in a context $\Gamma$ is a scheme $\sigma_p$ with $\Gamma \vdash e : \sigma_p$ such that $\sigma_p \sqsubseteq \sigma$ for each $\sigma$ with $\Gamma \vdash e : \sigma$.

**Theorem (Damas and Milner 1982).**

1. *Closed terms.* If a closed term $e$ has a type, then it has a principal type scheme $\sigma_p = \forall \vec\alpha.\, \tau_p$. W computes $\tau_p$, and $\vec\alpha$ lists all the variables of $\tau_p$. The types of $e$ are exactly the instances of $\tau_p$.
2. *Open terms.* For each context $\Gamma$ and term $e$: if $R\Gamma \vdash e : \sigma$ for some substitution $R$ and scheme $\sigma$, then $W(\Gamma, e)$ returns $(S, \tau)$, and there is a substitution $R'$ with $R'S\Gamma = R\Gamma$ and $R'(\mathrm{Gen}(S\Gamma, \tau)) \sqsubseteq \sigma$. If there are no such $R$ and $\sigma$, W fails.
3. *Soundness.* If $W(\Gamma, e) = (S, \tau)$, then $S\Gamma \vdash e : \tau$, and so $S\Gamma \vdash e : \mathrm{Gen}(S\Gamma, \tau)$.

The principal scheme is unique up to renaming of its bound variables. The term "principal type property" names part 1.

## In plain words

Many types fit a function like "take two functions and compose them". You could say that it works on numbers, or on text, or on lists of truth values. The theorem says that among all these fitting types there is always one best type. It uses placeholders where the program does not care what goes in. Every other fitting type comes out of the best one by filling in the placeholders.

So the compiler never has to guess. If it finds the best type, it has lost nothing, because any use that some correct type allows is also allowed by the best type. If no type fits, the compiler can say so for certain.

The theorem also says how to find the best type: the step-by-step method called algorithm W always finds it.

## Proof

The theorem follows from two theorems about W. The [proof file of algorithm W](/algorithm-w/) proves both in full, by induction on the term, for the syntax-directed rules T-Var', T-Abs, T-App and T-Let'. The syntax-directed rules derive the same types as the declarative rules with T-Gen and T-Inst. That equivalence is proved by moving each T-Inst up to a variable and each T-Gen down to a `let` (Damas 1985). Here is the structure of the proof.

**Two lemmas on derivations.**

- *Type substitution.* If $\Gamma \vdash e : \tau$, then $S\Gamma \vdash e : S\tau$ for each substitution $S$. At T-Let', rename the generalized variables of $e_1$ apart from $S$ first. This step is correct only because generalization skips the variables that are free in $\Gamma$.
- *A more general context.* If $\Gamma, x : \sigma \vdash e : \tau$ and $\sigma' \sqsupseteq \sigma$ (each instance of $\sigma$ is an instance of $\sigma'$), then $\Gamma, x : \sigma' \vdash e : \tau$.

**Soundness of W** (part 3). If $W(\Gamma, e) = (S, \tau)$, then $S\Gamma \vdash e : \tau$. The proof is an induction on $e$. At an application, the two premises are moved to the final context by type substitution, and the unifier of line L8 makes the function type match. At a `let`, the scheme that W stores is at least as general as the scheme that T-Let' builds in the final context, and the lemma on a more general context finishes the case.

**Completeness of W** (part 2). If $R\Gamma \vdash e : \tau'$, then W succeeds with $(S, \tau)$, and some $R'$ has $R'\tau = \tau'$ and $R'S = R$ on the variables that W did not create. The proof is an induction on $e$.

- At a variable, $R'$ maps the fresh copies of the bound variables to the instance that the derivation chose.
- At an application, the substitution built from the two induction hypotheses, extended by the result type, unifies the two types of line L8. So MGU succeeds, and by the most general unifier property this substitution factors through the unifier. This gives $R'$.
- At a `let`, the key claim is $R_1(\mathrm{Gen}(S_1\Gamma, \tau_1)) \sqsupseteq \mathrm{Gen}(R\Gamma, R_1\tau_1)$: applying $R_1$ to the scheme that W computes gives a scheme at least as general as the one in the derivation. The proof checks the claim one variable at a time. A variable of $\tau_1$ that W quantified can be sent to anything. A variable that W did not quantify is free in $S_1\Gamma$, so its image under $R_1$ only has variables that are free in $R\Gamma$, which the derivation could not quantify either.

**From the two theorems to principal types.** Take a typable closed term $e$ and let $W(\emptyset, e) = (S, \tau_p)$. By soundness, $\vdash e : \tau_p$, and by type substitution each instance of $\tau_p$ is a type of $e$. By completeness with $\Gamma = \emptyset$, each type $\tau'$ of $e$ is $R'\tau_p$ for some $R'$. So the types of $e$ are exactly the instances of $\tau_p$, and $\forall \mathrm{ftv}(\tau_p).\, \tau_p$ is principal. If $e$ has no type, W cannot succeed, by soundness. For an open term, the same argument with the substitution $R$ gives part 2. Two principal schemes are generic instances of each other, so they are equal up to renaming. $\square$

## Consequences

- **No annotations are needed.** An ML program can be checked with no type written in it. The compiler can still print the principal type of each definition, which is often the best documentation of the definition.
- **Definitions are typed once.** Because the scheme of a `let`-bound definition is principal, a compiler can type each definition once and store the scheme. The uses do not change it. This allows the separate typing of the definitions of a module.
- **Signatures become matching.** A written signature $\tau_s$ for a definition is correct exactly when $\tau_s$ is an instance of the principal type. This test is one-sided unification, called matching, and takes linear time.
- **Typability is decidable.** A term is typable exactly when W succeeds. The cost is not small: the principal type can be exponentially large, and the problem is [complete for EXPTIME](/ml-typability-dexptime-completeness/).
- **Errors are certain.** If W fails, no type exists. The place where W fails is not always the place of the mistake, but the failure itself is never a false alarm.

## Tightness

- **First-class polymorphism.** The theorem fails if function arguments may have polymorphic types. In [System F](/system-f/), `fun f -> (fun u -> f 1) (f true)` has the type $(\forall \alpha.\, \alpha \to \alpha) \to \mathsf{int}$ and the type $(\forall \alpha.\, \alpha \to \mathsf{bool}) \to \mathsf{bool}$. No type has both as substitution instances: to get them, a free type variable would have to become $\alpha$ under the binder $\forall \alpha$, and substitution never captures a bound variable. Type inference for System F is even [undecidable](/system-f-inference-undecidability/). HM has no such term, because a `fun`-bound variable has one plain type.
- **Polymorphic recursion.** If recursive functions get schemes in their own bodies, typability is equivalent to [semi-unification](/semi-unification-problem/) and becomes [undecidable](/polymorphic-recursion-undecidability/). Then W can no longer find the type, even where one exists.
- **Principal typings.** The theorem is about the best type for a given context. A stronger property asks for the best pair of a context and a type, for terms with free variables. Wells (2002) showed that the HM system does not have this property, while the simply typed calculus does.
- **Subtyping and overloading.** With [subtyping](/subtyping/) or overloading, a term may have several incomparable types. The theorem comes back if the types carry constraints, as in [type classes](/type-classes/) and [HM(X)](/constraint-based-type-inference/).
- **References.** With mutable references, the rules must not generalize every `let`, or soundness fails. The [value restriction](/value-restriction/) keeps both soundness and principal types, since it only changes which variables T-Let' generalizes.
- **Size.** Principal does not mean small. The principal type of the nested term $y_k$ of the [let-polymorphism page](/let-polymorphism/) has $8 \cdot 2^k - 5$ nodes for a term with $7k + 4$ nodes.

## History

Curry and Feys (1958) set up type assignment for combinatory logic. Hindley (1969) proved that each typable object of combinatory logic has a principal type scheme, found by [Robinson's unification](/robinson-unification/) of 1965. Milner, who did not know Hindley's paper, found the same idea for the ML language of the LCF prover, added polymorphic `let`, and proved W sound in 1978. Completeness of W, and so the principal type theorem for the system with `let`, was proved by Damas and Milner in 1982, with the details in Damas's thesis of 1985. The name "Hindley-Milner" comes from these two independent discoveries. Lee and Yi (1998) published complete proofs for W and for the top-down algorithm M.

## References
