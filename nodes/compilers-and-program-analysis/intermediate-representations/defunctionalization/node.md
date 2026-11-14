---
tag: F1V3C8
kind: technique
slug: defunctionalization
name: Defunctionalization
aliases:
- Reynolds defunctionalization
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: Replaces first-class functions by data constructors, one per lambda, and an apply function that dispatches on the constructor.
prereqs: [closure-conversion, lambda-calculus]
see_also: [closure-conversion, lambda-lifting, continuation-passing-style, cps-conversion, zero-cfa, monomorphization, recursive-types, function-inlining]
sources:
  - paper: doi:10.1145/800194.805852
    title: John C. Reynolds, Definitional interpreters for higher-order programming languages, Proceedings of the ACM Annual Conference, 1972, pages 717-740
    locator: the first-order interpreter obtained by replacing the functional values and continuations of a higher-order interpreter with records and an apply function
  - paper: doi:10.1023/A:1010027404223
    title: John C. Reynolds, Definitional interpreters for higher-order programming languages, Higher-Order and Symbolic Computation 11(4), 1998, pages 363-397
    locator: the reprint of the 1972 paper
  - paper: doi:10.1145/773184.773202
    title: Olivier Danvy and Lasse R. Nielsen, Defunctionalization at work, Proceedings of the 3rd ACM SIGPLAN International Conference on Principles and Practice of Declarative Programming (PPDP 2001), pages 162-174
    locator: the transformation stated for whole programs, its examples, and defunctionalized continuations as first-order data structures such as stacks
  - paper: doi:10.1145/258949.258953
    title: Jeffrey M. Bell, Françoise Bellegarde and James Hook, Type-driven defunctionalization, Proceedings of the 1997 ACM SIGPLAN International Conference on Functional Programming (ICFP 1997), pages 25-37
    locator: defunctionalization that keeps programs typed, with data types and apply functions chosen by the types of the functions
  - paper: doi:10.1007/3-540-46425-5_4
    title: Henry Cejtin, Suresh Jagannathan and Stephen Weeks, Flow-directed closure conversion for typed languages, Programming Languages and Systems (ESOP 2000), LNCS 1782, pages 56-71
    locator: the closure conversion of the MLton whole-program compiler, which represents closures as values of sum types and dispatches at each call on the functions that flow analysis says can reach it
  - paper: doi:10.1145/964001.964009
    title: François Pottier and Nadji Gauthier, Polymorphic typed defunctionalization, Proceedings of the 31st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 2004), pages 89-98
    locator: defunctionalization as a type-preserving translation of System F with guarded algebraic data types into itself
---

Defunctionalization turns a higher-order program into a first-order one. Each function abstraction `fun x -> b` in the program gets a data constructor whose fields are the free variables of the abstraction. Where the program made a function value, it now builds that constructor. Where it called a function that it does not know, it now calls one global function `apply`, which matches on the constructor and runs the body of the abstraction that the constructor names, with the fields as its free variables. [Closure conversion](/closure-conversion/) also makes a record of the free variables, but it stores a code pointer in it and calls through that pointer; defunctionalization stores a tag and branches on it. Reynolds (1972) introduced the method to make a higher-order definitional interpreter first-order. Danvy and Nielsen (2001) stated it for whole programs and showed its uses. In particular, the continuations of a program in [continuation-passing style](/continuation-passing-style/) become a data structure, often a stack, and an interpreter in that style becomes an abstract machine. The method needs the whole program, because `apply` must have a branch for every abstraction that can reach a call.

## In plain words

A program that passes functions around is hard to run where only data and jumps exist. Defunctionalization replaces each function value by a small record. The record has a tag that says which function of the program it stands for, and it holds the values that the function took from its surroundings. One dispatcher, apply, takes a record and an argument, looks at the tag, and runs the matching piece of code. So passing a function becomes passing a record, and calling a function becomes calling the dispatcher. When the functions are the "what to do next" of a computation, the records chain together and form a stack of pending jobs. The price is that the dispatcher must know every function in the program before it is built.

## When it applies

- The target is first-order: C, a first-order intermediate language, a hardware description, or a tool that has no function values. Data can also be stored or sent over a network, and a function value cannot.
- The whole program is known at compile time, so that every abstraction is visible. Whole-program compilers such as MLton use this representation for closures (Cejtin, Jagannathan and Weeks 2000).
- A higher-order program hides a data structure that we want to see. Defunctionalized continuations are stacks, and a defunctionalized interpreter in continuation-passing style is an abstract machine.
- Calls through unknown functions are costly or hard to analyse. After the transformation every call goes to a known function, `apply`, and a [flow analysis](/zero-cfa/) can cut the branches of each call down to the few that can occur.

## The template

Take a closed program in a call-by-value [lambda calculus](/lambda-calculus/) with constants, operators, `let`, `if`, abstractions `fun x -> b`, and recursive functions `fix f. fun x -> b`. The output has the same forms without abstractions, plus constructors, a `case` on constructors, and one global recursive function `apply`.

```pseudo id=main
DEFUNCTIONALIZE(P)
L1  rename the binders of P apart, and give each abstraction a distinct label ℓ
L2  for each label ℓ of an abstraction fun x_ℓ -> b_ℓ (or fix f_ℓ. fun x_ℓ -> b_ℓ):
L3      let y_1, ..., y_k be its free variables, in a fixed order
L4      declare a constructor C_ℓ with k fields
L5  in all of P, replace each abstraction with label ℓ by C_ℓ(y_1, ..., y_k)
L6  in all of P, replace each call e_1 e_2 by apply(e_1, e_2)
L7  let b'_ℓ be b_ℓ after L5 and L6, for each label ℓ
L8  define apply(g, a) = case g of
L9      C_ℓ(y_1, ..., y_k) → let x_ℓ = a in b'_ℓ        for each label ℓ
L10 return apply and the new main term
```

For a recursive function, the branch of L9 also binds $f_\ell$ to $g$ itself, so that the body can call itself through `apply`. The constructors of L4 form one data type, which is recursive whenever a field holds a function, as in the [recursive types](/recursive-types/) of the source. The holes are the order of the fields in L3, the set of branches in L9 (all labels, or those that a flow analysis allows at each call), and the number of data types and `apply` functions (one in total, or one per function type).

**Why the program keeps its meaning.** Relate source values and target values by $c \sim c$ for each constant, and by $v \sim C_\ell(w_1, \dots, w_k)$ when $v$ is the abstraction with label $\ell$ after a substitution $\sigma$ of values for its free variables $y_1, \dots, y_k$, and $\sigma(y_i) \sim w_i$ for each $i$. This is a definition by induction on the size of $v$, since each $\sigma(y_i)$ is a part of $v$. Now take a subterm $e$, a source substitution $\sigma$ and a target substitution $\gamma$ with $\sigma(y) \sim \gamma(y)$ for each free variable $y$ of $e$, and write $e'$ for $e$ after L5 and L6. Then the run of $e[\sigma]$ ends with $v$ exactly when the run of $e'[\gamma]$ ends with some $w \sim v$, and the two runs are stuck together. The proof goes by induction on the run, one case per form.

- An abstraction with label $\ell$ is a value, and L5 gives the value $C_\ell(\gamma(y_1), \dots, \gamma(y_k))$. Its free variables are free in $e$, so the fields are related to $\sigma(y_i)$, and the two values are related.
- A call $e_1\,e_2$ becomes $\mathrm{apply}(e_1', e_2')$. By induction the parts give related values $v_1 \sim w_1$ and $v_2 \sim w_2$, or are stuck in both. If $v_1$ is a constant, $w_1$ is the same constant, the source call is stuck, and `apply` has no branch for it. Otherwise $v_1$ is the abstraction with label $\ell$ under some $\sigma_1$, and $w_1 = C_\ell(w_1', \dots, w_k')$ with $\sigma_1(y_i) \sim w_i'$. The source continues with $b_\ell$ under $\sigma_1$ and $x_\ell \mapsto v_2$. The target enters the branch for $\ell$ and continues with $b'_\ell$ under $y_i \mapsto w_i'$ and $x_\ell \mapsto w_2$. These substitutions are related on every free variable of $b_\ell$ (for a recursive function also $f_\ell \mapsto v_1$ and $f_\ell \mapsto w_1$), so the induction hypothesis applies to the body.
- `let`, `if`, constants and operators keep their form. Related booleans are equal, so both runs take the same branch, and related integers are equal, so operators give equal results.

The only step that uses the whole program is the call case: the branch for $\ell$ exists because L9 lists every abstraction of the program. Applied to the closed main term with empty substitutions, the claim says that the source and the target give the same constant, both give a function value, both get stuck, or both run forever.

## Classic examples

**Two abstractions and a recursive data type.**

```
add n   = fun x -> x + n             (* label Add, free variable n *)
twice f = fun x -> f (f x)           (* label Twice, free variable f *)
main    = (twice (add 3)) 10         (* 16 *)
```

The functions `add` and `twice` are known, so their calls stay direct. The two inner abstractions become constructors:

```
type fn = Add of int | Twice of fn
apply (Add n)   x = x + n
apply (Twice f) x = apply f (apply f x)
add n   = Add n
twice f = Twice f
main    = apply (twice (add 3)) 10
```

The run is `apply (Twice (Add 3)) 10`, then `apply (Add 3) (apply (Add 3) 10)`, then `apply (Add 3) 13`, which is 16. The field of `Twice` holds a function, so the type `fn` is recursive.

**Continuations become a stack.** Factorial in continuation-passing style, as [CPS conversion](/cps-conversion/) makes it, has two kinds of continuation: the first one, with no free variables, and the one built at each recursive call, with free variables `n` and `k`.

```
fact n k = if n = 0 then k 1 else fact (n - 1) (fun r -> k (n * r))
main     = fact 5 (fun r -> r)
```

Defunctionalization gives:

```
type cont = Id | Mul of int * cont
fact n k = if n = 0 then apply k 1 else fact (n - 1) (Mul (n, k))
apply Id r           = r
apply (Mul (n, k)) r = apply k (n * r)
main = fact 5 Id
```

The type `cont` is a list of integers, that is, a stack. `fact` pushes `5, 4, 3, 2, 1` and `apply` pops them and multiplies, giving 120. Every call is a tail call and every value is first-order, so the program is a loop with an explicit stack, which is what the direct-style factorial keeps in its [stack frames](/activation-record/). Danvy and Nielsen (2001) study this pattern: a defunctionalized continuation is a first-order data structure, and its `apply` is the code that consumes it.

**Reynolds' interpreter.** Reynolds (1972) wrote an interpreter for a higher-order language in a higher-order language, then removed the dependence on the higher-order features of the host. He represented the function values of the interpreted language and the continuations of the interpreter by records, one kind of record per abstraction in the interpreter, each with an apply function. The result is a first-order interpreter in which the records of the continuations form the control stack of a machine.

## Variations

- **Typed output.** A single type `fn` mixes functions of different types, so the output does not type check in a simply-typed language. Bell, Bellegarde and Hook (1997) use the types of the functions to give separate data types and `apply` functions, so the output is typed. With polymorphism such a scheme needs [monomorphization](/monomorphization/) first.
- **Polymorphic typed defunctionalization.** Pottier and Gauthier (2004) keep polymorphism. They translate System F with guarded algebraic data types into itself: one data type indexed by the type of the function, and one polymorphic `apply` whose result type is fixed by the constructor in each branch.
- **Flow-directed dispatch.** A control-flow analysis such as [0-CFA](/zero-cfa/) finds the set of abstractions that can reach each call. Each call then gets its own `case` with only those branches, and a call with one possible abstraction becomes a direct call that [inlining](/function-inlining/) can remove. MLton compiles closures this way (Cejtin, Jagannathan and Weeks 2000).
- **Partial defunctionalization.** Only some function values are replaced, for example only the continuations, as in the factorial example, while other functions stay higher-order or are closure converted.
- **Before or after lambda lifting.** [Lambda lifting](/lambda-lifting/) removes free variables by adding parameters, and defunctionalization removes function values. A first-order target with no nested scopes needs both, or closure conversion.

## Pitfalls

- **It needs the whole program.** `apply` must have a branch for every abstraction whose value can reach a call. A function from a separately compiled module, a library loaded at run time, or a callback from foreign code has no branch, and the call fails. Adding one abstraction anywhere changes `apply`, so every module must be compiled again. A compiler that links separate modules can keep ordinary closures for the functions that cross a module boundary.
- **The cost of dispatch.** Without flow analysis, each unknown call is a `case` over all abstractions of the program, and `apply` grows with the program. Most compilers restrict the branches by type or by flow analysis.
- **Types.** One `apply` for all functions does not type check in a typed target. Split it by function type, monomorphize, or use guarded algebraic data types.
- **Recursion.** A recursive function refers to itself. Taking its own name as a field gives an infinite value; the branch must instead bind the name to the scrutinee, as said after the template.
- **Name capture.** The fields of $C_\ell$ are bound again in the branch of `apply`. Without renaming apart at L1, a field can hide a variable that the body needs.
- **Space.** Each constructor keeps all free variables of its abstraction, as a flat closure does. A value that the body uses only on some paths stays alive as long as the constructor does.

## Exercises

1. Defunctionalize `compose f g = fun x -> f (g x)` with `main = (compose (add 1) (add 2)) 5`, using `add` from the first example, and run the result.
2. Write a function that sums a list in continuation-passing style, defunctionalize its continuations, and show that the continuation type is a list of integers.
3. Rewrite the defunctionalized factorial with an array and a loop in place of the type `cont`, and show that each step of the loop matches one call of `fact` or `apply`.
4. Give a program of two modules for which defunctionalizing one module alone gives a call with no matching branch.
5. Show that one `apply` for the functions `fun x -> x + 1` and `fun b -> not b` does not type check in a simply-typed target, and split it by function type.

## References
