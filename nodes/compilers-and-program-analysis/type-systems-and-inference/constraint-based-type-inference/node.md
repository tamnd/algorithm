---
tag: 39X2F2
kind: technique
slug: constraint-based-type-inference
name: Constraint-based type inference
aliases:
- HM(X)
- constraint generation and solving
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Splits inference into a pass that emits type constraints and a solver for them, so one inference engine serves many constraint domains.
prereqs: [hindley-milner-type-system, most-general-unifier]
see_also: [algorithm-w, algorithm-j, let-polymorphism, type-classes, subtyping, row-polymorphism, equational-unification, value-restriction]
sources:
  - paper: "Mitchell Wand, A simple algorithm and proof for type inference, Fundamenta Informaticae 10(2), 1987"
    locator: whole paper (a term of the simply typed calculus is turned into a set of type equations, and the term is typable exactly when the equations have a unifier)
  - paper: doi:10.1002/(SICI)1096-9942(199901/03)5:1<35::AID-TAPO4>3.0.CO;2-4
    title: Martin Odersky, Martin Sulzmann and Martin Wehr, Type inference with constrained types, Theory and Practice of Object Systems 5(1), 1999, pages 35 to 55
    locator: the HM(X) framework, with constrained type schemes and an inference algorithm for any constraint system X that meets the conditions of the paper
  - book: isbn:9780262162289
    title: François Pottier and Didier Rémy, The essence of ML type inference, Chapter 10 of Benjamin C. Pierce (editor), Advanced Topics in Types and Programming Languages, MIT Press, 2005
    locator: Chapter 10, pages 389 to 489 (the constraint language with let, constraint generation, its correctness, and the constraint solver)
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 22 (constraint typing rules, unification and principal types)
---

Constraint-based type inference splits the inference of types into two passes. The first pass, *constraint generation*, walks the program once and emits a formula in a small logic of types: equations between types, existential variables, and a `let` form for polymorphic definitions. The second pass, *constraint solving*, rewrites the formula into a solved form, which gives the principal type, or finds that it has no solution, which is a type error. Wand (1987) used this split for simple types. Odersky, Sulzmann and Wehr (1999) made the logic a parameter in their framework *HM(X)*: with X the equality of types, it is the [Hindley-Milner type system](/hindley-milner-type-system/), and other choices of X give [type classes](/type-classes/), [subtyping](/subtyping/) or [record rows](/row-polymorphism/). Pottier and Rémy (2005) gave the standard presentation, with a generator that is linear in the program and a solver that works like [algorithm J](/algorithm-j/) with levels.

## In plain words

A type checker that finds types by itself does two jobs at once: it reads the program, and it solves the puzzle of which types fit together. This technique separates the two jobs.

The first job reads the program once and writes down every rule that the types must obey, such as "this function takes what that value is". It does not try to solve anything. The second job takes the list of rules and solves it, like a person solving a set of equations.

The split helps in three ways. The reading part stays small and simple. The solver can be changed to support new kinds of rules, such as "this type must support equality", without touching the reading part. And when the rules cannot all hold, the solver can point at the few rules that clash, which helps to write good error messages.

## When it applies

- The language infers types in the style of ML, with polymorphic `let`, and the type system has more than plain equality of types: class predicates, subtyping, record fields, units of measure, or effects.
- The same front end must serve several type system features, or several languages, with a common solver.
- Good error messages matter, so the checker should know which program points produced the constraints that clash.
- The types of the program are first order. Constraints over types with higher rank quantifiers need annotations, as in [bidirectional type checking](/bidirectional-type-checking/), since inference for [System F](/system-f-inference-undecidability/) is undecidable.

## The template

**Constraints.** Types $\tau$ are type variables, base types and arrows. Constraints $C$ are:

```text
C ::= true | false | tau1 = tau2 | C1 /\ C2 | exists a. C | x <= tau | let x : forall a[C1].tau1 in C2
```

The constraint `x <= tau` says that $\tau$ is an instance of the scheme of $x$. For the scheme `forall a[C1].tau1`, it stands for `exists a. (C1 /\ tau1 = tau)`. The constraint `let x : forall a[C1].tau1 in C2` stands for `(exists a. C1) /\ C2'`, where $C_2'$ is $C_2$ with each `x <= tau` replaced in this way. The conjunct `exists a. C1` makes sure the definition is checked even when $x$ is never used. A monomorphic binding `let x : a1 in C` is the case with no quantified variables and `C1 = true`.

**Generation.** The function $[\![ e : \tau ]\!]$ gives a constraint that holds exactly when $e$ has the type $\tau$. Each rule takes fresh variables:

```text
[[ x : tau ]]                = x <= tau                                                       CT-Var
[[ n : tau ]]                = tau = int                                                      CT-Int
[[ fun x -> e : tau ]]       = exists a1 a2. (let x : a1 in [[ e : a2 ]]) /\ a1 -> a2 = tau     CT-Abs
[[ e1 e2 : tau ]]            = exists a. [[ e1 : a -> tau ]] /\ [[ e2 : a ]]                     CT-App
[[ let x = e1 in e2 : tau ]] = let x : forall a[ [[ e1 : a ]] ].a in [[ e2 : tau ]]            CT-Let
```

Each rule adds a fixed number of nodes, so the constraint has size $O(|e|)$ and is built in time $O(|e|)$. Pottier and Rémy prove that a closed term $e$ is typable in HM exactly when `exists a. [[ e : a ]]` is satisfiable, and that the most general solution for $a$ is the principal type of $e$. The rule CT-Let is where polymorphism lives: the constraint of $e_1$ goes into the scheme of $x$, and each use of $x$ gets its own copy.

**Solving.** The solver keeps a union-find structure of types, as in algorithm J, and gives each variable a level, the number of `let` constraints around the place where it was made.

```pseudo id=main
SOLVE(C, depth)                                   ▷ env maps names to schemes; UNIFY is the union-find unification of J
L1  if C is true then return
L2  if C is false then fail
L3  if C is τ1 = τ2 then UNIFY(τ1, τ2)              ▷ the root of a merged class keeps the smaller level
L4  if C is C1 ∧ C2 then SOLVE(C1, depth), SOLVE(C2, depth)
L5  if C is ∃α. C1 then make α a fresh variable of level depth, SOLVE(C1, depth)
L6  if C is let x : ∀α[C1].τ in C2 then
L7      make α a fresh variable of level depth + 1, SOLVE(C1, depth + 1)
L8      env(x) ← τ with the variables of level > depth quantified      ▷ never a variable joined to an outer one
L9      SOLVE(C2, depth), remove x from env
L10 if C is x ≤ τ then UNIFY(a fresh copy of env(x), τ)                ▷ copy only the quantified variables
L11 return
```

The holes of the template are the constraint domain and the solver for it. For HM the domain is equations and L3 is unification. For another domain X, L3 gets the atomic constraints of X, and L8 must also decide which atomic constraints stay in the scheme of $x$, which become a type error, and which can be dropped.

**Cost.** Generation is linear. Solving is exponential in the worst case, because L10 copies a type at each use and nested `let` doubles the copies. This cannot be avoided: [ML typability is DEXPTIME-complete](/ml-typability-dexptime-completeness/). With the union-find and levels, the solver runs in time $2^{O(n)}$, and on real programs it is close to linear.

## Classic examples

**Simple types (Wand 1987).** Without `let`, the constraint is a set of equations under existential quantifiers, and the solver is plain unification. For `fun x -> x x`, CT-Abs gives $x$ the type $a_1$, and the two uses give $a_1 = a \to a_2$ and $a_1 = a$. So $a = a \to a_2$, and the [occurs check](/occurs-check/) fails: the term has no type.

**Polymorphic let.** For `let id = fun x -> x in id id` and a result variable $t$, the generator gives

```text
let id : forall b[ exists a1 a2. (let x : a1 in x <= a2) /\ a1 -> a2 = b ].b
in exists a. (id <= a -> t /\ id <= a)
```

The solver works at level 1 inside the scheme. There `x <= a2` gives $a_2 = a_1$, and then $b = a_1 \to a_1$. The variable $a_1$ has level 1, so L8 gives `id` the scheme $\forall a_1.\, a_1 \to a_1$. The first use copies it to $a_3 \to a_3 = a \to t$, so $t = a$. The second copies it to $a_4 \to a_4 = a$. So $t = a_4 \to a_4$, and the principal type is $\forall a_4.\, a_4 \to a_4$.

**Type classes.** Extend X with class predicates such as `Eq a`, and give `==` the scheme `forall a[Eq a].a -> a -> bool`. For `fun x -> fun y -> x == y`, the solver unifies the types of `x` and `y` with $a$, and the predicate `Eq a` stays unsolved. At L8 a predicate on a quantified variable moves into the scheme, which becomes `forall a[Eq a].a -> a -> bool`. Haskell prints it as `Eq a => a -> a -> Bool`. A later use at `int` turns the predicate into `Eq int`, which an instance discharges. A predicate such as `Eq (int -> int)`, with no instance, is a type error. The [dictionary-passing translation](/dictionary-passing-translation/) then turns each predicate in a scheme into an extra argument.

## Variations

- **HM(X).** Odersky, Sulzmann and Wehr state the type system itself with constraints: judgments $C, \Gamma \vdash e : \sigma$ with constrained schemes $\forall \vec\alpha[D].\, \tau$. They give one inference algorithm for every X, and prove that it finds principal types when X meets the conditions of the paper.
- **Subtyping.** With X a set of subtyping constraints $\tau_1 \le \tau_2$, solving is no longer unification, and solved forms can grow large. Practical solvers simplify the constraints of each scheme before they store it.
- **Rows.** Record and variant types with [row variables](/row-polymorphism/) fit as a domain of equations with a richer theory. Pottier and Rémy treat them in the same chapter.
- **Equational theories.** Units of measure, as in F#, use unification modulo the laws of an abelian group, a case of [equational unification](/equational-unification/).
- **Local assumptions.** GHC's checker, OutsideIn(X) by Vytiniotis, Peyton Jones, Schrijvers and Sulzmann (2011), adds implication constraints for GADTs and type families. When these features are on, it does not generalize local `let` definitions, which keeps inference simple and predictable.
- **Error localization.** When the constraint has no solution, a solver can search for a small set of constraints that already has none, and report the program points that made them. This is the idea behind type error slicing.

## Pitfalls

- **Generalizing a variable joined to the context.** In `fun x -> let y = x in if y true then y 1 else 0`, the scheme of `y` is `forall b[ x <= b ].b`. Since `x` has the type $a_1$, this gives $b = a_1$, and $a_1$ belongs to the outer level. A solver that quantifies $b$ anyway gives `y` the scheme $\forall b.\, b$, so both uses of `y` type check, and the function gets a type $a_1 \to \mathsf{int}$. Then applying it to `5` runs `5 true`. The correct solver lowers the level of $b$ at L3, and the term is rejected, since $a_1$ cannot be both $\mathsf{bool} \to \mathsf{bool}$ and $\mathsf{int} \to \mathsf{int}$. Generalizing over variables free in the context is unsound.
- **Unused definitions.** `let x = 1 + true in 0` is not typable, though `x` is never used. A generator that only copies the constraint of $e_1$ to the uses of $x$ misses the error. The conjunct `exists a. C1` in the meaning of `let` keeps it.
- **Copying constraints instead of solved schemes.** Replacing each `x <= tau` by the full constraint of the definition is correct, but the constraint then grows exponentially with the nesting of `let`, even when the types stay small. Solve $C_1$ once, simplify it, and copy only the result.
- **Order of solving.** The solution does not depend on the order, but the first failure does. A solver that always blames the last equation can point far away from the real error.
- **Effects.** With mutable references, CT-Let must follow the [value restriction](/value-restriction/) and quantify only when $e_1$ is a value. Otherwise the solver accepts unsound programs.
- **No occurs check.** Unification without the occurs check solves the equations over infinite regular trees. That is a different type system, with recursive types, as in OCaml's `-rectypes` mode.

## Exercises

1. Generate the constraint for `fun f -> fun x -> f (f x)` and solve it. Check that the principal type is $(\alpha \to \alpha) \to \alpha \to \alpha$.
2. Write generation rules for `if e1 then e2 else e3` and for `fix f x -> e`. Check that your rules for `fix` give `f` a monomorphic type in the body.
3. Show that `let x = 1 + true in 0` is rejected, and name the constraint that fails.
4. For the family $f_0 = $ `fun x -> fun z -> z x x`, $f_i = $ `fun y -> f(i-1) (f(i-1) y)`, nested by `let`, count the size of the constraint when each `x <= tau` is replaced by the constraint of the definition, and compare it with the size of the generated constraint.
5. Extend the solver with class predicates, and give the scheme of `fun x -> fun y -> if x == y then 1 else 0`.

## References
