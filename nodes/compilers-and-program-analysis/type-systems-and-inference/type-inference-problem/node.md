---
tag: 5X891X
kind: problem
slug: type-inference-problem
name: Type inference problem
aliases:
- type reconstruction
- typability problem
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Given a term without type annotations, find types for its variables and the term that make it well typed, or report that none exist; ideally return a principal type.
prereqs: [type-checking-problem, unification-problem]
see_also: [simply-typed-lambda-calculus, most-general-unifier, paterson-wegman-unification, hindley-milner-type-system, algorithm-w, constraint-based-type-inference, system-f-inference-undecidability, polymorphic-recursion-undecidability]
sources:
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 22 (Section 22.3 constraint-based typing with its soundness and completeness theorems, Section 22.4 unification, Section 22.5 principal types)
  - paper: doi:10.2307/1995158
    title: J. Roger Hindley, The principal type-scheme of an object in combinatory logic, Transactions of the American Mathematical Society 146, 1969, pages 29 to 60
    locator: the principal type-scheme theorem (each typable object has a principal type scheme, found by unification)
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 4 (algorithm W) and the soundness of W
  - paper: "Mitchell Wand, A simple algorithm and proof for type inference, Fundamenta Informaticae 10, 1987"
    locator: the separation of type inference into constraint generation and unification
  - paper: doi:10.1016/0022-0000(78)90043-0
    title: Michael S. Paterson and Mark N. Wegman, Linear unification, Journal of Computer and System Sciences 16(2), 1978, pages 158 to 167
    locator: the main theorem (unification in linear time on a DAG representation)
  - paper: doi:10.1145/96709.96748
    title: Harry G. Mairson, Deciding ML typability is complete for deterministic exponential time, POPL 1990, pages 382 to 401
    locator: the DEXPTIME-hardness proof by simulation of an exponential time Turing machine with nested let
  - paper: doi:10.1016/S0168-0072(98)00047-5
    title: Joe B. Wells, Typability and type checking in System F are equivalent and undecidable, Annals of Pure and Applied Logic 98(1-3), 1999, pages 111 to 156
    locator: Theorem 4.1 and Section 6 (undecidability of typability by reduction from semi-unification)
  - paper: doi:10.1145/182409.182456
    title: Assaf J. Kfoury and Joe B. Wells, A direct algorithm for type inference in the rank-2 fragment of the second-order lambda-calculus, LFP 1994, pages 196 to 207
    locator: the main results (rank-2 typability is decidable by reduction to acyclic semi-unification; rank k of 3 or more is undecidable)
---

The type inference problem takes a program with no type annotations and asks for types that make it well typed. For the [simply typed lambda calculus](/simply-typed-lambda-calculus/), Hindley (1969) showed that the answer, when it exists, has a *principal* form from which every other typing follows by substitution, and that [unification](/unification-problem/) finds it. The same method, with polymorphism at `let`, is the core of ML and Haskell. The problem is harder than [type checking](/type-checking-problem/), and for richer type systems it becomes undecidable.

## In plain words

In many languages you can write a function without saying what types its arguments have. The compiler then works the types out. It gives each unknown type a name, reads the program once, and writes down an equation for each use: if `f` is called on `x`, then the type of `f` must be a function from the type of `x` to something. Then it solves all the equations at once. If they have a solution, the program is accepted, and the most general solution is its type. If they have no solution, for example because a value must be both a number and a function, the program is rejected. For simple types this is fast. For more powerful type systems, no program can always find the answer.

## Definition

Fix a type system with a judgment $\Gamma \vdash e : \tau$ on untyped (Curry-style) terms.

- **Instance.** An untyped term $e$, and possibly a context $\Gamma_0$ that fixes the types of some free variables.
- **Output.** A pair $(\Gamma, \tau)$ with $\Gamma \vdash e : \tau$ and $\Gamma$ extending $\Gamma_0$, or the answer "untypable".

The decision version is **typability**: does such a pair exist? A *typing* $(\Gamma, \tau)$ is *principal* for $e$ if each typing of $e$ is $(S\Gamma, S\tau)$, possibly with more variables in the context, for some substitution $S$ of types for type variables. A type system has *principal typings* if each typable term has one. An inference algorithm is *sound* if each typing it returns is derivable, and *complete* if it returns a typing whenever one exists. A complete algorithm for a system with principal typings should return a principal one.

The input size $n$ is the number of nodes in the syntax tree of $e$. The cost model is a word RAM.

## Variants

- **Type checking** gives $\tau$ and asks only yes or no. It is a different problem, often much easier when the term carries annotations. See the [type checking problem](/type-checking-problem/).
- **Inference for simple types** (Curry-style STLC). Decidable in linear time.
- **Inference with let-polymorphism** ([Hindley-Milner](/hindley-milner-type-system/)). Decidable and DEXPTIME-complete. The algorithms are [W](/algorithm-w/), [J](/algorithm-j/) and [constraint-based inference](/constraint-based-type-inference/).
- **Inference with polymorphic recursion** (Milner-Mycroft typing). Undecidable ([polymorphic recursion undecidability](/polymorphic-recursion-undecidability/)), by equivalence with [semi-unification](/semi-unification-problem/).
- **Inference for System F.** Undecidable ([Wells' theorem](/system-f-inference-undecidability/)). For the rank-$k$ fragments, rank 2 is decidable and every rank of 3 or more is undecidable (Kfoury and Wells 1994).
- **Partial inference.** The programmer writes some annotations and the checker fills in the rest. [Bidirectional type checking](/bidirectional-type-checking/) is the common method in modern languages.
- **Inference with recursive types.** With equi-recursive types, drop the [occurs check](/occurs-check/) and unify regular infinite trees ([recursive types](/recursive-types/)). Then every pure lambda term is typable, so the question is interesting only with base types.

## Examples

**Twice.** Take $e = \lambda f.\lambda x.\ f\ (f\ x)$. Give $f$ the type variable $a$ and $x$ the type variable $b$. The inner application $f\ x$ gets a fresh $r_1$ and the equation $a = b \to r_1$. The outer application gets $r_2$ and the equation $a = r_1 \to r_2$. The term has type $a \to b \to r_2$. Unification of $b \to r_1$ with $r_1 \to r_2$ gives $b = r_1$ and $r_1 = r_2$. So the principal type is $(b \to b) \to b \to b$, or after renaming $(a \to a) \to a \to a$. A script that generates the two constraints and unifies them returns this type.

**Self-application.** For $\lambda x.\ x\ x$, give $x$ the type $a$. The application gives $a = a \to r$. The variable $a$ occurs inside $a \to r$, so the [occurs check](/occurs-check/) fails, no finite type solves the equation, and the term is untypable. A type checker that is given a candidate type would answer "no" for each candidate, but it could never say "no candidate works". Inference proves that.

**S and B.** The script gives $\lambda x.\lambda y.\lambda z.\ x\,z\,(y\,z) : (a \to b \to c) \to (a \to b) \to a \to c$ and $\lambda f.\lambda g.\lambda x.\ f\,(g\,x) : (a \to b) \to (c \to a) \to c \to b$. Each is principal: for example $(\mathsf{Int} \to \mathsf{Int}) \to (\mathsf{Bool} \to \mathsf{Int}) \to \mathsf{Bool} \to \mathsf{Int}$ is the instance $a, b, c := \mathsf{Int}, \mathsf{Int}, \mathsf{Bool}$ of the second.

**Exponential principal types.** Let $D = \lambda z.\lambda w.\ w\,z\,z$ and $e_k = \lambda x.\ D\,(D\,(\cdots(D\,x)\cdots))$ with $k$ copies of $D$. If the argument of $D$ has type $\sigma$, the result has type $(\sigma \to \sigma \to b) \to b$, which holds two copies of $\sigma$. The script gives these numbers.

| $k$ | term nodes | constraints | type tree nodes | type DAG nodes |
|---|---|---|---|---|
| 0 | 2 | 0 | 3 | 2 |
| 1 | 10 | 3 | 9 | 6 |
| 2 | 18 | 6 | 21 | 10 |
| 3 | 26 | 9 | 45 | 14 |
| 6 | 50 | 18 | 381 | 26 |

The term has $8k+2$ nodes, the principal type has $6 \cdot 2^k - 3$ tree nodes, and the DAG with shared subtypes has $4k+2$ nodes. For $k = 1$ the type is $a \to (a \to a \to b) \to b$. So an algorithm that prints the type as text needs exponential time, but one that returns a DAG does not.

## Known algorithms

**Constraint generation, then unification.** This is Wand's (1987) split of Hindley's method, and Chapter 22 of Pierce's book. For the Curry-style STLC with $\mathsf{Int}$ and $\mathsf{Bool}$, define $\mathrm{gen}(\Gamma, e) = (\tau, C)$ where $C$ is a set of equations:

- $\mathrm{gen}(\Gamma, x) = (\Gamma(x), \emptyset)$.
- $\mathrm{gen}(\Gamma, \lambda x.e_1) = (a \to \tau_1, C_1)$, where $a$ is fresh and $(\tau_1, C_1) = \mathrm{gen}((\Gamma, x{:}a), e_1)$.
- $\mathrm{gen}(\Gamma, e_1\,e_2) = (r, C_1 \cup C_2 \cup \{\tau_1 = \tau_2 \to r\})$, where $r$ is fresh.
- $\mathrm{gen}(\Gamma, \mathsf{if}\ e_1\ \mathsf{then}\ e_2\ \mathsf{else}\ e_3) = (\tau_2, C_1 \cup C_2 \cup C_3 \cup \{\tau_1 = \mathsf{Bool}, \tau_2 = \tau_3\})$, and constants give their base type.

For a closed term, start with $\Gamma = \emptyset$. Then compute a [most general unifier](/most-general-unifier/) $\sigma$ of $C$. If none exists, $e$ is untypable. Otherwise $\sigma\tau$ is the principal type.

*Theorem (soundness and completeness of constraint typing; Pierce, Section 22.3).* Let $\mathrm{gen}(\Gamma, e) = (\tau, C)$. (1) If a substitution $S$ solves $C$, then $S\Gamma \vdash e : S\tau$. (2) If $S'\Gamma \vdash e : T$ for some substitution $S'$, then there is a solution $S$ of $C$ that agrees with $S'$ on the variables of $\Gamma$ and has $S\tau = T$.

*Proof sketch.* Both parts go by induction on $e$. For (1), at an application, $S$ solves $C_1$ and $C_2$, so the induction gives $S\Gamma \vdash e_1 : S\tau_1$ and $S\Gamma \vdash e_2 : S\tau_2$. $S$ also solves $\tau_1 = \tau_2 \to r$, so $S\tau_1 = S\tau_2 \to Sr$, and T-App gives $S\Gamma \vdash e_1\,e_2 : Sr$. At an abstraction, the induction gives $S\Gamma, x{:}Sa \vdash e_1 : S\tau_1$, and T-Abs gives the arrow. For (2), inversion on the derivation of $T$ gives the types of the parts. At $\lambda x.e_1$, inversion gives $T = T_1 \to T_2$, so extend $S'$ with $a := T_1$, which is safe because $a$ is fresh, and use the induction. At an application, inversion gives a type $T_{11}$ for the argument. The induction gives solutions for $C_1$ and $C_2$, which agree on $\Gamma$ and touch disjoint sets of fresh variables, so their union is a function; add $r := T$. $\square$

*Corollary (principal types).* If $\sigma$ is a most general unifier of $C$, then $(\sigma\Gamma, \sigma\tau)$ is a principal typing: each solution $S$ factors as $S = S'' \circ \sigma$, so each typing is an instance of it.

**Choice of unification algorithm.** [Robinson's algorithm](/robinson-unification/) on trees can take exponential time, because the solved form can be exponentially large. [Martelli-Montanari](/martelli-montanari-unification/) with a [union-find](/disjoint-set-forest/) structure on a DAG runs in $O(n\,\alpha(n))$ time if the occurs check is done once at the end. [Paterson-Wegman](/paterson-wegman-unification/) runs in $O(n)$ time. The constraint set has $O(n)$ symbols, so Curry-style STLC inference takes $O(n)$ time with the type returned as a DAG.

**Inline solving.** [Algorithm W](/algorithm-w/) (Milner 1978) solves each equation as soon as it appears and returns a substitution. [Algorithm J](/algorithm-j/) keeps one global substitution in a union-find structure. Both add let-polymorphism: at `let x = e1 in e2` they solve the constraints of $e_1$, generalize its type over the variables that are not free in the context, and give $x$ that type scheme.

## Bounds

| system | typability | source |
|---|---|---|
| Curry-style STLC | $\Theta(n)$ time | Hindley 1969, Paterson and Wegman 1978 |
| Hindley-Milner (ML) | DEXPTIME-complete | Mairson 1990; Kfoury, Tiuryn and Urzyczyn 1990 |
| ML with polymorphic recursion | undecidable | Henglein 1993; Kfoury, Tiuryn and Urzyczyn 1993 |
| System F, rank 2 | decidable | Kfoury and Wells 1994 |
| System F, rank 3 or more, and full System F | undecidable | Kfoury and Wells 1994; Wells 1999 |

For ML, the exponent comes from nested `let`: each `let` can double the size of a type, as in the $D$ example with polymorphic copies. When the nesting depth of `let` is bounded by a constant, inference is polynomial. The table is about the decision problem. An algorithm that must print the principal type as a tree can need time exponential in $n$ even for the STLC, as the example shows.

## Reductions

- **STLC typability to unification.** The constraint generation above is a linear-time reduction from typability to first-order [unification](/unification-problem/), and it preserves most general solutions.
- **Typability to checking.** For ML and for System F, typability reduces to checking: $e$ is typable if and only if $\mathsf{let}\ u = e\ \mathsf{in}\ \mathsf{fun}\ v \to v$ has type $\mathsf{Int} \to \mathsf{Int}$ in ML, and Wells gives a similar term for System F. So checking is at least as hard as typability in these systems. See the [type checking problem](/type-checking-problem/).
- **Semi-unification.** Typability with polymorphic recursion and typability in System F both reduce from [semi-unification](/semi-unification-problem/), which is [undecidable](/semi-unification-undecidability/) (Kfoury, Tiuryn and Urzyczyn 1993).
- **Second-order unification.** Partial type reconstruction for System F, where the positions of type abstractions and applications are given but the types are not, reduces from second-order unification (Pfenning 1988), which is undecidable ([higher-order unification undecidability](/higher-order-unification-undecidability/)).

## Applications

- **ML, OCaml, F# and Haskell** infer the types of all functions without annotations, by Hindley-Milner inference with extensions. The error message for an ill-typed program is a unification failure, and its location is a known weak point.
- **Local inference in mainstream languages.** C++ `auto`, Java `var`, C# `var`, Go `:=`, Rust `let` and TypeScript infer the type of a variable from its initializer and use [bidirectional](/bidirectional-type-checking/) rules elsewhere. They require annotations on function signatures, which keeps inference decidable and local.
- **Program analysis.** Constraint generation followed by solving is also the shape of many static analyses, for example [Steensgaard's points-to analysis](/steensgaard-analysis/), which is unification on the points-to graph.
- **Proof search.** Principal types of combinators are the most general theorems they prove ([Curry-Howard correspondence](/curry-howard-correspondence/)).

## References
