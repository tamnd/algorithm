---
tag: 90HNZ3
kind: theorem
slug: polymorphic-recursion-undecidability
name: Undecidability of polymorphic recursion
aliases:
- Milner-Mycroft typability undecidability
area: compilers-and-program-analysis/type-systems-and-inference
level: research
summary: Type inference for ML with polymorphic recursion is undecidable, as it is equivalent to semi-unification.
prereqs: [hindley-milner-type-system, semi-unification-undecidability]
see_also: [semi-unification-problem, let-polymorphism, algorithm-w, ml-typability-dexptime-completeness, system-f-inference-undecidability, monomorphization, bidirectional-type-checking, undecidability]
sources:
  - paper: doi:10.1007/3-540-12925-1_41
    title: Alan Mycroft, Polymorphic type schemes and recursive definitions, International Symposium on Programming, Lecture Notes in Computer Science 167, 1984, pages 217 to 228
    locator: the typing rule that gives a recursive definition a type scheme inside its own body
  - paper: doi:10.1145/169701.169692
    title: Fritz Henglein, Type inference with polymorphic recursion, ACM Transactions on Programming Languages and Systems 15(2), 1993, pages 253 to 289
    locator: the log-space reductions from typability with polymorphic recursion to semi-unification and back
  - paper: "A. J. Kfoury, J. Tiuryn and P. Urzyczyn, Type reconstruction in the presence of polymorphic recursion, ACM Transactions on Programming Languages and Systems 15(2), 1993, pages 290 to 311"
    locator: the equivalence of typability with polymorphic recursion and semi-unification, and the resulting undecidability
  - paper: doi:10.1006/inco.1993.1003
    title: A. J. Kfoury, J. Tiuryn and P. Urzyczyn, The undecidability of the semi-unification problem, Information and Computation 102(1), 1993, pages 83 to 101
    locator: the main theorem, by reduction from the boundedness problem for Turing machines
---

Polymorphic recursion lets a recursive function call itself at a different instance of its own type. Mycroft (1984) proposed a typing rule for it as an extension of the [Hindley-Milner type system](/hindley-milner-type-system/), where a recursive function is monomorphic inside its own body. With the rule, more programs have types, but type inference becomes impossible: in 1993, Henglein and, independently, Kfoury, Tiuryn and Urzyczyn showed that typability with this rule is equivalent to the [semi-unification problem](/semi-unification-problem/), which is [undecidable](/semi-unification-undecidability/). Checking stays decidable when the programmer writes the type scheme of the recursive function. This is what Haskell and OCaml do.

## Statement

Extend the terms of the Hindley-Milner page with `fix f x -> e`. The ML rule T-Fix gives `f` a plain type in the body. Mycroft's rule, in syntax-directed form, gives it a scheme:

```text
Gamma, f : tau1 -> tau2, x : tau1 |- e : tau2               Gamma, f : Gen(Gamma, tau1 -> tau2), x : tau1 |- e : tau2
---------------------------------------------  T-Fix        ---------------------------------------------------------  T-FixPoly
Gamma |- fix f x -> e : tau1 -> tau2                        Gamma |- fix f x -> e : tau1 -> tau2
```

*Typability with polymorphic recursion* is the problem: given a closed term $e$, decide whether $\vdash e : \tau$ for some $\tau$, with T-FixPoly in place of T-Fix.

**Theorem (Henglein 1993; Kfoury, Tiuryn and Urzyczyn 1993).**

1. Typability with polymorphic recursion and semi-unification reduce to each other in logarithmic space.
2. So typability with polymorphic recursion is undecidable. It is semi-decidable: the set of typable terms is recursively enumerable, and its complement is not.

## In plain words

In ML, when a function calls itself, the inner call must use the function at the same type that is being worked out. A more generous rule lets the inner call use the function at any type that fits its final general form. Some useful programs, for example on nested data structures, need this freedom.

The catch is that the compiler must now guess the general form before it has finished reading the function, and each inner call may see a different copy of it. The theorem shows that this guessing problem is as hard as a known puzzle about patterns, semi-unification, and that no program solves that puzzle in all cases. So no compiler can find these types by itself every time. If the programmer writes the type of the function, the compiler only has to check it, and that is easy.

## Proof

The two reductions are in the [proof file](proofs/main.md). Here is their structure.

**From typability to semi-unification.** Give each node of the term a type variable. Applications, abstractions and constants give equations, as in the simply typed calculus. Each use $u$ of a `let`-bound or `fix`-bound name, bound at $b$, must have a type that is an instance of the type $\delta_b$ of the definition, where only the variables that are not free in the context may change. This is the inequality

$$\langle \delta_b, \gamma_b \rangle \le \langle \alpha_u, \gamma_b \rangle,$$

where $\gamma_b$ is the tuple of the types of the `fun`-bound variables in scope at $b$. A semi-unifier $\sigma$ with residual $\rho$ must satisfy $\sigma\gamma_b\,\rho = \sigma\gamma_b$, so $\rho$ cannot move the variables of the context. That is exactly the side condition of generalization. The term is typable if and only if the system has a semi-unifier, and the system has linear size.

**From semi-unification to typability.** Take inequalities $s_i \le t_i$ between types over the variables $v_1, \ldots, v_k$. Build one recursive function `fix f x1 -> fun x2 -> ... -> fun xk -> body`. With `eq = fun a -> fun b -> if true then a else b`, small terms built from the $x_j$ have exactly the types $s_i$ and $t_i$ with $v_j$ replaced by the type of $x_j$. The body forces the result type of `f` to be $s_1 \to \cdots \to s_n \to \mathsf{int}$ under this replacement $\sigma$. The $i$-th recursive call passes the term of type $t_i\sigma$ at place $i$ and `bot = (fix g y -> g y) 0`, which fits any type, everywhere else. T-FixPoly lets each call take its own instance $\rho_i$ of the type of `f`, so the call is typable exactly when $s_i\sigma\rho_i = t_i\sigma$. So the term is typable if and only if $\sigma$ can be chosen as a semi-unifier. The papers also code an arbitrary signature of function symbols into types.

**Undecidability.** Kfoury, Tiuryn and Urzyczyn (1993) proved semi-unification undecidable, by a reduction from the boundedness problem of [Turing machines](/turing-machine/). The second reduction carries this over to typability. The first reduction shows that typability is semi-decidable, since semi-unifiers can be listed and checked. $\square$

## Consequences

- **Inference must stop at recursive functions.** A compiler cannot infer polymorphically recursive types for all programs. Haskell accepts polymorphic recursion only for a function with a type signature. OCaml asks for an explicit polymorphic annotation, `let rec f : 'a. ...`.
- **Checking is decidable.** If each polymorphically recursive function has a written scheme, `f` has that scheme in its body, and the rest of the program is typed by unification as in [algorithm W](/algorithm-w/). The written scheme removes the guess. This is a simple case of [bidirectional type checking](/bidirectional-type-checking/).
- **An example that needs it.** In `fix f x -> if true then 0 else f true + f 1`, the two calls use `f` at $\mathsf{bool} \to \mathsf{int}$ and $\mathsf{int} \to \mathsf{int}$. T-Fix fails, since it needs one argument type. T-FixPoly gives $\forall \alpha.\, \alpha \to \mathsf{int}$. Functions on nested data types, such as `data Nested a = Flat a | Nest (Nested [a])` in Haskell, need the same freedom in real code.
- **No monomorphization.** A polymorphically recursive function can be used at infinitely many types in one run, such as $\alpha$, $[\alpha]$, $[[\alpha]]$ and so on. So a compiler cannot make one copy per type, and [monomorphization](/monomorphization/) fails. Implementations use a uniform representation or dictionaries instead.
- **Semi-algorithms exist.** Since the problem is semi-decidable, a type checker can search for a typing and succeed on every typable term. It cannot always stop on an untypable one.

## Tightness

- **Plain ML recursion.** With T-Fix, typability is decidable and complete for [DEXPTIME](/ml-typability-dexptime-completeness/). Kfoury, Tiuryn and Urzyczyn (1990) showed that it is equivalent to acyclic semi-unification, the decidable special case in which the inequalities have no cycles. Polymorphic recursion is what creates the cycles.
- **One inequality.** Semi-unification with one inequality is decidable. But a single recursive function with several recursive calls already gives several inequalities, and Reduction 2 needs only one such function.
- **Annotations.** With a written scheme for each polymorphically recursive function, the problem is no harder than ML typability.
- **System F.** Typability in [System F](/system-f/) is [undecidable](/system-f-inference-undecidability/) for a related reason: Wells (1999) reduced semi-unification to it.

## History

Mycroft (1984) proposed giving recursive definitions a type scheme in their own bodies. His motivation was that mutually recursive definitions in ML get less general types than the same definitions written apart. The decidability of typability stayed open. Kfoury, Tiuryn and Urzyczyn and, independently, Henglein reduced it to semi-unification and back. Kfoury, Tiuryn and Urzyczyn then proved semi-unification undecidable in 1990, with the journal versions of all three papers in 1993. Haskell accepts polymorphic recursion for functions with a type signature, and OCaml added explicit polymorphic annotations for it in version 3.12.

## References
