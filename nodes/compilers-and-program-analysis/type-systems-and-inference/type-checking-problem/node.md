---
tag: 0WZYBC
kind: problem
slug: type-checking-problem
name: Type checking problem
aliases:
- typechecking
area: compilers-and-program-analysis/type-systems-and-inference
level: intro
summary: Given a typing context, a term and a type, decide whether the term has that type under the rules of a type system.
prereqs: [type-system]
see_also: [type-inference-problem, simply-typed-lambda-calculus, bidirectional-type-checking, paterson-wegman-unification, hash-consing, ml-typability-dexptime-completeness, system-f-inference-undecidability, subtyping]
sources:
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 9, Section 9.3 (uniqueness of types and the inversion lemma for the simply typed lambda calculus), Chapter 10 (the typechecker as one recursive function), Section 23.6 (erasure and typability in System F), Chapter 28 (undecidability of bounded quantification)
  - paper: doi:10.1016/0022-0000(78)90043-0
    title: Michael S. Paterson and Mark N. Wegman, Linear unification, Journal of Computer and System Sciences 16(2), 1978, pages 158 to 167
    locator: the main theorem (unifiability of a set of term equations in time linear in the size of the input; STOC 1976 version)
  - paper: doi:10.1145/96709.96748
    title: Harry G. Mairson, Deciding ML typability is complete for deterministic exponential time, POPL 1990, pages 382 to 401
    locator: the DEXPTIME-hardness of ML typability
  - paper: doi:10.1007/3-540-52590-4_50
    title: Assaf J. Kfoury, Jerzy Tiuryn and Pawel Urzyczyn, ML typability is DEXPTIME-complete, CAAP 1990, LNCS 431, pages 206 to 220
    locator: the upper and lower bounds for ML typability
  - paper: doi:10.1016/S0168-0072(98)00047-5
    title: Joe B. Wells, Typability and type checking in System F are equivalent and undecidable, Annals of Pure and Applied Logic 98(1-3), 1999, pages 111 to 156
    locator: Theorem 4.1 (type checking reduces from semi-unification) and Section 6 (typability and type checking are equivalent); LICS 1994 version, pages 176 to 185
  - paper: doi:10.1145/182409.182456
    title: Assaf J. Kfoury and Joe B. Wells, A direct algorithm for type inference in the rank-2 fragment of the second-order lambda-calculus, LFP 1994, pages 196 to 207
    locator: the abstract and main results (typability is decidable at rank 2 and undecidable at every rank k of 3 or more)
  - paper: doi:10.1006/inco.1994.1055
    title: Benjamin C. Pierce, Bounded quantification is undecidable, Information and Computation 112(1), 1994, pages 131 to 165
    locator: the reduction from two-counter machines to the subtype relation of full F-sub (POPL 1992 version)
---

The type checking problem asks whether a given term has a given type in a given context: decide $\Gamma \vdash e : \tau$. It is the question a compiler front end answers for every program it accepts. Its difficulty depends on how much type information the term carries. For the explicitly typed [simply typed lambda calculus](/simply-typed-lambda-calculus/) it takes linear time, for ML with `let` it is DEXPTIME-complete, and for the implicitly typed [System F](/system-f/) it is undecidable. It is a different problem from [type inference](/type-inference-problem/), which must find the types.

## In plain words

A type checker gets three things: a program fragment, the types of the names it may use, and a claimed type. It answers yes or no: does the fragment have that type under the rules? The checker does not invent anything when the programmer has written the type of every variable. It walks over the program once, works out the type of each piece from its parts, and compares at each function call that the argument has the type the function wants. That is fast. The problem gets harder when the program leaves types out, because then the checker must guess them, and for some type systems no program can always make that guess.

## Definition

Fix a [type system](/type-system/) $S$, that is, a grammar of types $\tau$, a grammar of terms $e$, and inference rules for the judgment $\Gamma \vdash_S e : \tau$.

- **Instance.** A context $\Gamma = x_1 : \tau_1, \dots, x_k : \tau_k$, a term $e$ whose free variables are among $x_1, \dots, x_k$, and a type $\tau$.
- **Question.** Is there a derivation of $\Gamma \vdash_S e : \tau$?

The input size $n$ is the total number of symbols in $\Gamma$, $e$ and $\tau$, type annotations included.

The answer depends on the term syntax. In a *Church-style* (explicitly typed) system, each binder carries its type, as in $\lambda x{:}\mathsf{Int}.\ x$, and type abstractions and applications are written in the term. In a *Curry-style* (implicitly typed) system, terms are untyped, as in $\lambda x.\ x$, and the derivation must choose the types of the binders. The same rules in the two styles give two different checking problems.

## Variants

- **Type computation.** Given $\Gamma$ and $e$, compute a type $\tau$ with $\Gamma \vdash e : \tau$. In a Church-style system where each term has at most one type (Pierce, Theorem 9.3.3, uniqueness of types), checking is type computation followed by one type comparison.
- **Curry-style checking.** Given $\Gamma$, an untyped $e$ and $\tau$, decide $\Gamma \vdash e : \tau$. The type variables in $\tau$ are fixed: they are not to be instantiated.
- **Typability.** Given an untyped $e$, decide whether some $\Gamma$ and $\tau$ exist. This is the decision form of the [type inference problem](/type-inference-problem/). For System F, Wells (1999) showed that typability and Curry-style checking are equivalent under many-one reductions, and both are undecidable.
- **Partial annotations.** Some but not all types are written. [Bidirectional type checking](/bidirectional-type-checking/) handles systems where annotations are needed only at a few places.
- **Checking with subtyping.** The comparison of types becomes a subtype test. For [subtyping](/subtyping/) of simple types, records and recursive types, the test is decidable. For full bounded quantification ($F_{<:}$), the subtype relation is undecidable (Pierce 1994), so checking explicitly typed $F_{<:}$ terms is undecidable.
- **Checking with definitional equality.** In [dependent type](/dependent-types/) theories, two types are equal if their terms compute to the same normal form. Checking then needs a normalization procedure. It is decidable for theories where every term normalizes, and it can be undecidable when types may contain non-terminating computations.

## Examples

**Church-style STLC, a yes instance.** Let $e = \lambda f{:}\mathsf{Int}{\to}\mathsf{Int}.\ \lambda x{:}\mathsf{Int}.\ f\ (f\ x)$, $\Gamma$ empty, and $\tau = (\mathsf{Int} \to \mathsf{Int}) \to \mathsf{Int} \to \mathsf{Int}$. The bottom-up pass gives $x : \mathsf{Int}$, then $f\ x : \mathsf{Int}$ after one comparison of the domain $\mathsf{Int}$ of $f$ with the type $\mathsf{Int}$ of $x$, then $f\ (f\ x) : \mathsf{Int}$ after a second comparison, then the two arrows from T-Abs. The computed type equals $\tau$, so the answer is yes. The script check computes the same type with two application comparisons.

**The same term, a no instance.** With $\tau = (\mathsf{Int} \to \mathsf{Int}) \to \mathsf{Bool} \to \mathsf{Int}$ the answer is no. The term has the unique type $(\mathsf{Int} \to \mathsf{Int}) \to \mathsf{Int} \to \mathsf{Int}$, and it differs from $\tau$ in the second argument.

**Curry-style, a no instance.** For the untyped $\lambda x.\ x$ and $\tau = \mathsf{Int} \to \mathsf{Bool}$, the answer is no: T-Abs needs $x : \mathsf{Int} \vdash x : \mathsf{Bool}$, and T-Var gives only $\mathsf{Int}$. For $\tau = \mathsf{Int} \to \mathsf{Int}$ the answer is yes, and so is the answer for $\tau = \alpha \to \alpha$ with a fixed type variable $\alpha$.

**Why naive comparison is quadratic.** Let $T_m = \mathsf{Int} \to \mathsf{Int} \to \dots \to \mathsf{Int}$ with $m$ arrows, a type tree with $2m+1$ nodes, and take

$$
e_{k,m} = \lambda f{:}T_m{\to}T_m.\ \lambda a{:}T_m.\ \underbrace{f\ (f\ (\cdots (f}_{k}\ a)\cdots)).
$$

The term has $6m + 2k + 7$ nodes. A checker that compares types as trees does $k$ comparisons of two copies of $T_m$, so $k(2m+1)$ node visits. For $k = m = 50$ the term has 407 nodes and the checker makes 5050 node visits. With $k = m = n/8$ the cost grows as $n^2/32$.

## Known algorithms

**Church-style STLC: one bottom-up pass.** Compute the type of each subterm from the types of its children (Pierce, Chapter 10). T-Var looks up the context, T-Abs builds an arrow, and T-App and T-If compare two types. Each node does constant work besides the comparisons.

**Linear time with shared types.** Two ways remove the quadratic cost.

1. *Hash-consing.* Store each type once, in a table keyed by its constructor and the numbers of its children ([hash-consing](/hash-consing/)). Then equal types are the same node, and a comparison is one test of two numbers. Each annotation node and each arrow built by T-Abs costs one table lookup, so the pass takes expected $O(n)$ time with a hash table, or $O(n \log n)$ worst case with a balanced search tree on pairs of numbers.
2. *Reduction to unification.* Give each subterm $e'$ an unknown $X_{e'}$ and write one equation per node: $X_{x} = A$ for a variable bound with annotation $A$ or given $A$ by $\Gamma$, $X_{\lambda x{:}A.b} = A \to X_b$, $X_{e_1} = X_{e_2} \to X_{e_1 e_2}$, $X_{c} = \mathsf{Bool}$ and $X_{t} = X_{f} = X_{\mathsf{if}\ c\ t\ f}$ for a conditional, and $X_e = \tau$ at the root. The rules are syntax directed, so a solution of the equations is exactly an assignment of a type to each node that satisfies every rule, and $\Gamma \vdash e : \tau$ holds if and only if the equations are unifiable. The system has $O(n)$ symbols, and the [Paterson-Wegman algorithm](/paterson-wegman-unification/) decides it in worst-case $O(n)$ time.

**Curry-style STLC.** Use the same equations with a fresh unknown for each binder instead of its annotation, and treat the type variables of $\tau$ and $\Gamma$ as constants. Unifiability is again equivalent to $\Gamma \vdash e : \tau$, so this problem is also linear with Paterson-Wegman. The [type inference problem](/type-inference-problem/) page gives the details of constraint generation.

**ML (Hindley-Milner).** Compute the principal type of $e$ with [algorithm W](/algorithm-w/) or [algorithm J](/algorithm-j/), then test whether $\tau$ is an instance of it by one-way matching. The principal type can be exponentially large as a DAG, so this is exponential time in the worst case.

**Church-style System F.** One bottom-up pass, as for STLC, with two more rules: a type abstraction $\Lambda\alpha.e$ gets $\forall\alpha.\tau$, and a type application $e\,[T]$ substitutes $T$ for the bound variable. Types are compared up to the renaming of bound type variables (for example with de Bruijn indices). This decides checking for every term.

## Bounds

- Church-style and Curry-style STLC: $\Theta(n)$. The upper bound is the Paterson-Wegman reduction above, and the lower bound holds because the checker must read the whole input.
- ML with `let` (Curry style, Hindley-Milner): DEXPTIME-complete. The upper bound is algorithm W followed by matching. Hardness comes from typability (Mairson 1990; Kfoury, Tiuryn and Urzyczyn 1990; see [ML typability is DEXPTIME-complete](/ml-typability-dexptime-completeness/)) by the reduction in the next section. With a fixed bound on the nesting depth of `let`, the cost is polynomial.
- Church-style System F: decidable. Curry-style System F: undecidable ([Wells' theorem](/system-f-inference-undecidability/)). Typability in the rank-2 fragment of System F is decidable, and typability at every finite rank of 3 or more is undecidable (Kfoury and Wells 1994).
- Explicitly typed $F_{<:}$ with the full contravariant rule for bounded quantifiers: undecidable (Pierce 1994, by a reduction from two-counter machines). The kernel variant, which requires equal bounds, is decidable.

## Reductions

- **Typability reduces to checking, for ML.** Let $e$ be closed, and let $e' = \mathsf{let}\ u = e\ \mathsf{in}\ \mathsf{fun}\ v \to v$. If $e$ has a type, T-Let types $e'$ with the type of the body, and $\vdash e' : \mathsf{Int} \to \mathsf{Int}$. If $e$ has no type, then T-Let has no premise for $e$, and $e'$ has no type at all. So $e$ is typable if and only if $\vdash e' : \mathsf{Int} \to \mathsf{Int}$, and the map from $e$ to $e'$ takes linear time. This transfers DEXPTIME-hardness from typability to checking.
- **Typability reduces to checking, for System F.** Wells uses the same idea with the term $K\,I\,(\lambda x_1 \dots x_k.\,M)$ and the type $\forall\alpha.\alpha \to \alpha$, where $K = \lambda u.\lambda v.u$ and $I = \lambda w.w$. The details are on the [Wells' theorem](/system-f-inference-undecidability/) page.
- **Checking reduces to unification**, for simple types, as shown above. This is the bridge from type systems to [first-order unification](/unification-problem/) and the [most general unifier](/most-general-unifier/).
- **Semi-unification reduces to Curry-style System F checking** (Wells 1999, Theorem 4.1). [Semi-unification](/semi-unification-problem/) is [undecidable](/semi-unification-undecidability/), so checking is undecidable too.

## Applications

- **Compilers.** Every statically typed compiler solves this problem on each function. Java, C# and Go use mostly Church-style syntax for declarations, so their checkers are close to the linear bottom-up pass, with extra work for overloading and generics.
- **Proof assistants.** The kernel of Coq, Lean or Agda is a type checker for an explicitly typed dependent type theory. By the [Curry-Howard correspondence](/curry-howard-correspondence/), checking the proof term is checking the proof.
- **Bytecode verification.** The JVM verifies class files by a type-checking pass over the bytecode before it runs them.
- **Typed intermediate languages.** GHC can check its typed core language (System FC, a Church-style extension of System F) after each optimization pass. The check is turned on by a flag (`-dcore-lint`), and it catches bugs in the optimizer.

## References
