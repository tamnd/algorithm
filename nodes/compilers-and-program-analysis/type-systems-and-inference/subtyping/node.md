---
tag: GDSKYF
kind: concept
slug: subtyping
name: Subtyping
aliases:
- subtype polymorphism
- inclusion polymorphism
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: "A relation S <: T saying a value of type S can be used wherever a T is expected; functions are contravariant in the argument, and records allow width and depth subtyping."
prereqs: [simply-typed-lambda-calculus]
see_also: [type-system, type-soundness, recursive-types, system-f, bidirectional-type-checking, row-polymorphism, gradual-typing, type-checking-problem]
sources:
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 15 (the rules S-Refl, S-Trans, S-Top, S-Arrow, S-RcdWidth, S-RcdDepth, S-RcdPerm and T-Sub, the inversion lemmas for subtyping and soundness), Chapter 16 (algorithmic subtyping and typing, joins and meets), Chapter 26 and Section 28.5 (bounded quantification and its undecidability)
  - paper: doi:10.1007/3-540-13346-1_2
    title: Luca Cardelli, A semantics of multiple inheritance, in Semantics of Data Types, LNCS 173, Springer, 1984, pages 51 to 66
    locator: the record and function subtyping rules and the soundness of the typing with subsumption
  - paper: doi:10.1016/0890-5401(88)90007-7
    title: Luca Cardelli, A semantics of multiple inheritance, Information and Computation 76(2-3), 1988, pages 138 to 164
    locator: the journal version of the 1984 paper
  - paper: "Luca Cardelli and Peter Wegner, On understanding types, data abstraction, and polymorphism, ACM Computing Surveys 17(4), 1985"
    locator: the classification of polymorphism into parametric, inclusion, overloading and coercion, and bounded quantification
  - paper: doi:10.1006/inco.1994.1055
    title: Benjamin C. Pierce, Bounded quantification is undecidable, Information and Computation 112(1), 1994, pages 131 to 165
    locator: the main theorem (subtyping in full F-sub is undecidable), by reduction from the halting problem for two-counter machines; POPL 1992 version
  - paper: doi:10.1017/S0960129500000657
    title: Dexter Kozen, Jens Palsberg and Michael I. Schwartzbach, Efficient recursive subtyping, Mathematical Structures in Computer Science 5(1), 1995, pages 113 to 125
    locator: the O(n^2) algorithm for subtyping of recursive types (POPL 1993 version)
---

Subtyping is a relation $S <: T$ between types that says a value of type $S$ is safe to use wherever a value of type $T$ is expected. A type system with subtyping adds one typing rule, *subsumption*: if a term has type $S$ and $S <: T$, then it also has type $T$. So one term has many types, and one function accepts arguments of many types. This is the form of polymorphism behind classes and interfaces in object-oriented languages. Cardelli (1984) gave the first formal rules for records and functions, and the rule for functions surprises many people: it reverses the order on the argument.

## In plain words

Suppose a function wants a point with an `x` field. You can give it a point that also has a `y` field, because the function never looks at `y`. So "point with x and y" is a subtype of "point with x". That is subtyping: a more detailed thing can stand in for a less detailed thing. The surprise is with functions. Where a function that accepts any point with `x` is expected, you can use a function that accepts more, but not one that accepts less. A function that needs `y` cannot be used where callers may pass a point without `y`. So for the input of a function the order flips. For the output it does not. Getting these directions wrong lets a program read a field that is not there, and real languages have made this mistake.

## The idea

### The rules

Add to the [simply typed lambda calculus](/simply-typed-lambda-calculus/) a type $\mathsf{Top}$ and record types $\{l_1{:}T_1, \dots, l_k{:}T_k\}$ with distinct labels, record values $\{l_1 = t_1, \dots, l_k = t_k\}$ and projection $t.l$. The subtype relation is the smallest relation closed under these rules (Pierce, Chapter 15).

```text
                     S <: U    U <: T
------  S-Refl       ----------------  S-Trans       --------  S-Top
S <: S               S <: T                          S <: Top

T1 <: S1    S2 <: T2
--------------------  S-Arrow
S1 -> S2 <: T1 -> T2

-------------------------------------------------------  S-RcdWidth
{l1:T1, ..., ln:Tn, ..., ln+k:Tn+k} <: {l1:T1, ..., ln:Tn}

for each i:  Si <: Ti                       {k1:S1, ..., kn:Sn} is a permutation of {l1:T1, ..., ln:Tn}
-------------------------------------  S-RcdDepth      ----------------------------------------------  S-RcdPerm
{l1:S1, ..., ln:Sn} <: {l1:T1, ..., ln:Tn}             {k1:S1, ..., kn:Sn} <: {l1:T1, ..., ln:Tn}

Gamma |- t : S    S <: T
------------------------  T-Sub
Gamma |- t : T
```

S-Arrow is *contravariant* in the argument (the order flips from $T_1 <: S_1$ to the arrow) and *covariant* in the result. Records are covariant in each field (depth), and a record with more fields is a subtype of one with fewer (width).

### Why the arrow rule is right

A function $f : S_1 \to S_2$ is used at type $T_1 \to T_2$ by a caller that passes a $T_1$ and expects a $T_2$. The call is safe if $f$ can accept any $T_1$, which needs $T_1 <: S_1$, and if what $f$ returns can serve as a $T_2$, which needs $S_2 <: T_2$. Two contravariant positions cancel: in $(A \to \mathsf{Int}) \to \mathsf{Int}$, the type $A$ is in a covariant position.

### Soundness

[Progress and preservation](/type-soundness/) still hold, with two changes in the proof (Pierce, Section 15.3). Canonical forms needs *inversion lemmas for subtyping*: if $S <: T_1 \to T_2$, then $S = S_1 \to S_2$ with $T_1 <: S_1$ and $S_2 <: T_2$; if $S$ is a subtype of a record type, then $S$ is a record type with at least the same labels, and the fields are subtypes. Preservation must allow a step to make the type smaller: after E-AppAbs, the substituted value may have a subtype of the parameter type, and T-Sub covers it.

### Algorithmic subtyping

The rules above are not syntax directed. S-Trans has a middle type $U$ that does not appear in the conclusion, and T-Sub can be applied at any node. A checker uses equivalent *algorithmic* rules (Pierce, Chapter 16):

- Drop S-Refl and S-Trans, which are admissible: they can be derived from the others.
- Merge the three record rules into one: $\{k_j{:}S_j\} <: \{l_i{:}T_i\}$ if each $l_i$ is some $k_j$ with $S_j <: T_i$.
- Drop T-Sub and check subtyping only where types meet: in T-App, require that the argument type is a subtype of the domain, instead of equal to it.

The algorithmic system computes the *minimal type* of each term, and it accepts a term exactly when the declarative system does. A conditional needs the *join* (least upper bound) of the types of its branches. For this language with $\mathsf{Top}$, joins always exist; for records, the join keeps the common labels.

### Bounded quantification

[System F](/system-f/) with subtyping, $F_{<:}$, has types $\forall \alpha <: T.\,S$: a polymorphic function that works for every subtype $\alpha$ of $T$. Cardelli and Wegner (1985) proposed it to type functions on records that return their argument with its full type. The full subtype rule for these types compares the bounds contravariantly. Pierce (1994) proved that this makes subtyping in full $F_{<:}$ undecidable, by a reduction from the halting problem for two-counter machines. The *kernel* $F_{<:}$, which requires the two bounds to be equal, is decidable. Java generics with wildcards and Scala have related undecidability results.

### Other choices

- **Inclusion or coercion.** In the *inclusion* view, a value of type $S$ simply is a value of type $T$. In the *coercion* view, $S <: T$ comes with a conversion function, as for $\mathsf{Int} <: \mathsf{Float}$. Then each subtyping derivation inserts conversions, and the design must be *coherent*: two derivations of the same judgment must give the same program.
- **Structural or nominal.** Structural subtyping, as above, follows the shape of types (OCaml objects, TypeScript, Go interfaces). Nominal subtyping holds only between declared names (Java and C# classes), and the checker verifies that each declaration is consistent with the structural rules.
- **Recursive types.** With [recursive types](/recursive-types/), subtyping is decided on infinite regular trees, by Amadio and Cardelli's rules. Kozen, Palsberg and Schwartzbach (1995) gave an $O(n^2)$ algorithm.
- **Rows.** [Row polymorphism](/row-polymorphism/) gets much of the effect of width subtyping with type variables instead, and it works with ML-style inference.

## Examples

A script with the algorithmic rules checks each subtype claim below. Let $P_1 = \{x{:}\mathsf{Int}\}$ and $P_2 = \{x{:}\mathsf{Int}, y{:}\mathsf{Int}\}$.

| claim | holds | reason |
|---|---|---|
| $P_2 <: P_1$ | yes | width |
| $P_1 <: P_2$ | no | $P_1$ has no field $y$ |
| $P_1 \to \mathsf{Int} <: P_2 \to \mathsf{Int}$ | yes | contravariant argument |
| $P_2 \to \mathsf{Int} <: P_1 \to \mathsf{Int}$ | no | contravariant argument |
| $\mathsf{Int} \to P_2 <: \mathsf{Int} \to P_1$ | yes | covariant result |
| $\{a{:}P_2, b{:}\mathsf{Int}\} <: \{a{:}\mathsf{Top}\}$ | yes | width, then depth with S-Top |
| $(P_2 \to \mathsf{Int}) \to \mathsf{Int} <: (P_1 \to \mathsf{Int}) \to \mathsf{Int}$ | yes | two flips cancel |
| $(P_1 \to \mathsf{Int}) \to \mathsf{Int} <: (P_2 \to \mathsf{Int}) \to \mathsf{Int}$ | no | two flips cancel |

**Subsumption at a call.** Let $\mathit{getx} = \lambda p{:}P_1.\ p.x$. The application $\mathit{getx}\ \{x = 1, y = 2\}$ is well typed: the argument has type $P_2$, T-Sub with $P_2 <: P_1$ gives it type $P_1$, and T-App gives $\mathsf{Int}$. It steps to $\{x = 1, y = 2\}.x$ and then to $1$.

**Why a covariant argument would be unsound.** Let $\mathit{gety} = \lambda p{:}P_2.\ p.y$, of type $P_2 \to \mathsf{Int}$. If the rules allowed $P_2 \to \mathsf{Int} <: P_1 \to \mathsf{Int}$, then $\mathit{gety}\ \{x = 1\}$ would be typed $\mathsf{Int}$. It steps to $\{x = 1\}.y$, which is stuck: the record has no field $y$. The table shows that the algorithm rejects this subtype claim.

**Mutable cells must be invariant.** Suppose $\mathsf{Ref}\ P_2 <: \mathsf{Ref}\ P_1$. A function of type $\mathsf{Ref}\ P_1 \to \mathsf{Unit}$ may write $\{x = 1\}$ into the cell, and the owner of the $\mathsf{Ref}\ P_2$ then reads field $y$ of it: stuck. Suppose instead $\mathsf{Ref}\ P_1 <: \mathsf{Ref}\ P_2$. Then a reader reads $y$ from a cell that holds only $\{x = 1\}$: stuck again. So $\mathsf{Ref}\ S <: \mathsf{Ref}\ T$ needs both $S <: T$ and $T <: S$. Pierce (Section 15.5) splits a reference into a covariant source and a contravariant sink to recover some flexibility.

**Java arrays.** Java makes arrays covariant: `String[]` is a subtype of `Object[]`. By the argument above, this is unsound for writes. The program `Object[] a = new String[1]; a[0] = Integer.valueOf(1);` passes the compiler. The JVM keeps the element type with each array and checks every store, so the second statement throws `ArrayStoreException`. The language is safe only because of this run-time check. Java generics, which came later, are invariant: `List<String>` is not a subtype of `List<Object>`.

## Where it is used

- **Object-oriented languages.** A subclass is a subtype of its superclass, so a method that takes a `Shape` accepts a `Circle`. Method overriding must follow S-Arrow: Java and C# allow a covariant return type in an override, but not a contravariant parameter type, which they treat as overloading instead.
- **Variance annotations.** Scala (`+A`, `-A`), Kotlin (`out`, `in`) and C# (`out T`, `in T`) let the programmer declare the variance of a type parameter, and the checker verifies that the parameter appears only in positions of that variance. Java uses wildcards (`? extends T`, `? super T`) at use sites instead.
- **Structural typing.** TypeScript checks object types by width and depth, and Go checks that a type has the methods of an interface. TypeScript deliberately accepts unsound method parameter bivariance in some places, for convenience.
- **Numeric types.** Many languages treat $\mathsf{Int} <: \mathsf{Float}$ as a coercion.
- **Type checking with subtyping** is mostly done with [bidirectional rules](/bidirectional-type-checking/), because full inference with subtyping gives large sets of subtype constraints that are hard to solve and present.

## References
