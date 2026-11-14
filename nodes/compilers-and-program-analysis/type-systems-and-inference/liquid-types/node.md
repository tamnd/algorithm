---
tag: YG0HVJ
kind: technique
slug: liquid-types
name: Liquid types
aliases:
- logically qualified data types
area: compilers-and-program-analysis/type-systems-and-inference
level: research
summary: Infers refinement types by abstract interpretation over conjunctions of given qualifiers, with SMT queries to check each subtyping step.
prereqs: [hindley-milner-type-system, refinement-types, predicate-abstraction]
see_also: [houdini-algorithm, abstract-interpretation, smt-problem, knaster-tarski-theorem, loop-invariant-synthesis, cegar, constraint-based-type-inference, dependent-types]
sources:
  - paper: doi:10.1145/1375581.1375602
    title: Patrick M. Rondon, Ming Kawaguchi and Ranjit Jhala, Liquid types, ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2008), pages 159 to 169
    locator: logical qualifiers and liquid types, the liquid typing rules, constraint generation with liquid type variables, the iterative weakening algorithm, and the experiments on array bound checks in OCaml programs
  - paper: doi:10.1145/1706299.1706316
    title: Patrick M. Rondon, Ming Kawaguchi and Ranjit Jhala, Low-level liquid types, Thirty-Seventh ACM Symposium on Principles of Programming Languages (POPL 2010), pages 131 to 144
    locator: liquid type inference for a low-level imperative language with pointers and a heap
  - paper: doi:10.1007/3-540-45251-6_29
    title: Cormac Flanagan and K. Rustan M. Leino, Houdini, an annotation assistant for ESC/Java, FME 2001, Lecture Notes in Computer Science, pages 500 to 517
    locator: the algorithm that starts from all candidate annotations and removes those that the checker refutes until none is refuted
  - paper: doi:10.1145/2628136.2628161
    title: Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis and Simon Peyton Jones, Refinement types for Haskell, ACM SIGPLAN International Conference on Functional Programming (ICFP 2014), pages 269 to 282
    locator: Liquid Haskell, liquid type inference under lazy evaluation, and termination checking
  - paper: doi:10.1561/2500000032
    title: Ranjit Jhala and Niki Vazou, Refinement types, a tutorial, Foundations and Trends in Programming Languages 6(3-4), 2021, pages 159 to 317
    locator: the chapters on refinement inference with Horn constraints and their solution over qualifiers
---

Liquid types is a method to infer [refinement types](/refinement-types/) automatically. The user gives a finite set of *qualifiers*, small predicate patterns such as $0 \leq \nu$ or $\nu < \star$, where $\star$ stands for any program variable. Every unknown refinement in the program is then a conjunction of instances of these qualifiers, and the method finds the strongest such conjunctions that make the program type check, using an SMT solver for each implication. The name stands for "logically qualified data types" (Rondon, Kawaguchi and Jhala 2008). The refinement type system decides whether given types are correct; liquid types finds the types. The method is [predicate abstraction](/predicate-abstraction/) applied to types, and its fixed point loop is the same as the [Houdini algorithm](/houdini-algorithm/) for program annotations.

## In plain words

Writing refinement types by hand is a lot of work. Every helper function and every loop needs a fact such as "this index is between 0 and the length of the array". Liquid types guesses these facts from a short list of patterns that you give, such as "is at least 0" and "is less than some variable". For each unknown fact, it starts with every pattern that could apply, joined by "and". This is too strong to be true in most places. It then looks at each place where the fact must hold, asks the solver which patterns fail there, and drops them. It repeats until nothing more fails. Since the list of patterns is finite, the dropping must stop. What is left is the strongest fact that the patterns can say.

## When it applies

- The program is in a typed functional language, or can be put in A-normal form with types from [Hindley-Milner inference](/hindley-milner-type-system/). The liquid types are refinements of those types.
- The refinements needed for the property are conjunctions of a few qualifier patterns. Bounds of array indices, sizes of lists, sortedness of adjacent elements, and ordering between arguments and results are typical.
- The qualifiers are in a decidable logic, such as linear integer arithmetic with uninterpreted functions, so each implication is one decidable SMT query.
- The properties to prove are given as refinements on primitives and on some function signatures, for example a precondition on array access or division.

## The template

### Liquid templates and constraints

Let $Q$ be the set of qualifiers. For a refinement position whose scope contains the variables $X$, let $Q^\star_X$ be the set of instances of $Q$ where each $\star$ is replaced by a variable of $X$ of the right base type. It is finite because $Q$ and $X$ are finite. A *liquid type* is a refinement type whose refinements are conjunctions of such instances.

1. **Shapes.** Run HM inference. Give each base type position that has no user annotation a fresh *liquid variable* $\kappa$, so the refinement there is unknown.
2. **Constraints.** Walk the program with the rules of the [refinement type system](/refinement-types/), with $\kappa$ in place of each unknown. Each use of subtyping gives an implication $[\![\Gamma]\!] \wedge \varphi_1 \Rightarrow \varphi_2$, where the context, $\varphi_1$ and $\varphi_2$ may contain liquid variables under a pending substitution $\theta$ (from T-App and T-Var), written $\theta\,\kappa$. A constraint whose right side is some $\theta\,\kappa$ is a $\kappa$-constraint. A constraint whose right side has no liquid variable is a *check*.
3. **Solve.** Find an assignment $A$ of a subset of $Q^\star_\kappa$ to each $\kappa$ that makes all constraints valid, where a subset means its conjunction.

```pseudo
SOLVE(constraints C, qualifier instances Q*)
L1  for each liquid variable κ do A(κ) ← Q*(κ)          ▷ all candidates, the strongest guess
L2  repeat
L3      changed ← false
L4      for each κ-constraint  H ⇒ θ κ  in C do
L5          for each q in A(κ) do
L6              if not VALID(A(H) ⇒ θ q) then          ▷ one SMT query
L7                  A(κ) ← A(κ) minus {q} ; changed ← true
L8  until not changed
L9  for each check  H ⇒ φ  in C do
L10     if not VALID(A(H) ⇒ φ) then report an error at its source position
L11 return A
```

Here $A(H)$ replaces each liquid variable in $H$ by the conjunction that $A$ gives it. The liquid variables occur only as conjuncts on the left of an implication or alone on the right, so a larger set $A(\kappa)$ makes every left side stronger.

### Termination

**Theorem.** SOLVE ends after at most $|C| \cdot (1 + \sum_\kappa |Q^\star_\kappa|) \cdot \max_\kappa |Q^\star_\kappa|$ validity queries, plus one query for each check.

*Proof.* Each pass of L2 to L8 other than the last removes at least one qualifier from some $A(\kappa)$, and nothing is ever added. The sets start with $\sum_\kappa |Q^\star_\kappa|$ elements in all, so there are at most that many passes that change something, and then one pass that changes nothing. A pass makes at most $|C| \cdot \max_\kappa |Q^\star_\kappa|$ queries. Each query is an implication in a decidable logic, so each one ends. $\square$

The bound uses only the finiteness of $Q^\star$. With an infinite candidate set, such as all linear inequalities, the same loop could remove candidates forever, which is why invariant inference in general needs widening or interpolation ([CEGAR](/cegar/) and [loop invariant synthesis](/loop-invariant-synthesis/)).

### Correctness

**Soundness.** When SOLVE returns $A$, every $\kappa$-constraint is valid under $A$ (the last pass removed nothing), and every check is valid. So the refinement typing with $A$ put in for each $\kappa$ satisfies every premise of S-Base, and it is a valid refinement typing. By the soundness of refinement types, the program does not fail any refined precondition.

**Strongest solution.** Call an assignment $S$ a *solution* if it makes all $\kappa$-constraints valid. The invariant is: for every solution $S$ and every $\kappa$, $S(\kappa) \subseteq A(\kappa)$. It holds at L1, since $A(\kappa)$ is all of $Q^\star_\kappa$. Suppose L7 removes $q$ from $A(\kappa)$, because $A(H) \Rightarrow \theta q$ is not valid, and suppose $q \in S(\kappa)$. Since $S \subseteq A$ pointwise and liquid variables occur positively in $H$, $A(H) \Rightarrow S(H)$ is valid. Since $S$ is a solution, $S(H) \Rightarrow \theta S(\kappa)$ is valid, and $\theta S(\kappa) \Rightarrow \theta q$ because $q$ is a conjunct. So $A(H) \Rightarrow \theta q$ is valid, a contradiction. So the invariant is kept, and the final $A$ is the greatest solution: the strongest liquid types. This is the greatest fixed point of a monotone map on a finite lattice of subsets ([Knaster-Tarski](/knaster-tarski-theorem/)), reached from the top.

**Relative completeness.** If any liquid assignment $S$ over $Q$ makes all constraints valid, checks included, then SOLVE reports no error. Each check $H \Rightarrow \varphi$ holds under $S$, and $A(H) \Rightarrow S(H)$ by the invariant, so it holds under $A$. An error therefore means that no liquid typing over the given qualifiers exists. The program may still be safe, with an invariant that the qualifiers cannot express.

### Cost

$|Q^\star_\kappa|$ is at most $|Q| \cdot |X|^k$ for qualifiers with $k$ holes and $|X|$ variables in scope, so it grows with the number of variables. In practice qualifiers have one or two holes, and most candidates are removed in the first pass. The SMT queries dominate the time.

## Classic examples

**Maximum.** Let $Q = \{\nu \geq \star, \nu \leq \star\}$ with $\star$ ranging over the variables in scope and the constant 0, and infer the result of `let max x y = if x > y then x else y`, with unrefined arguments. The result has scope $\{x, y\}$, so $Q^\star_\kappa$ is $\{\nu \geq 0, \nu \geq x, \nu \geq y, \nu \leq 0, \nu \leq x, \nu \leq y\}$. The two branches give

$$C_1 : x > y \wedge \nu = x \Rightarrow \kappa \qquad C_2 : \neg(x > y) \wedge \nu = y \Rightarrow \kappa$$

| Step | Constraint | Removed | $A(\kappa)$ after |
| --- | --- | --- | --- |
| start | | | all six |
| 1 | $C_1$ | $\nu \geq 0$, $\nu \leq 0$, $\nu \leq y$ | $\nu \geq x$, $\nu \geq y$, $\nu \leq x$ |
| 2 | $C_2$ | $\nu \leq x$ | $\nu \geq x$, $\nu \geq y$ |
| 3 | $C_1$, $C_2$ | nothing | $\nu \geq x$, $\nu \geq y$ |

For example, $\nu \geq 0$ is removed at step 1 because $x = -1, y = -2, \nu = -1$ satisfies the left side of $C_1$ and not $\nu \geq 0$. The result is $\mathit{max} : x{:}\mathsf{int} \to y{:}\mathsf{int} \to \{\nu : \mathsf{int} \mid \nu \geq x \wedge \nu \geq y\}$.

**A loop invariant for array bounds.** Take, with $\mathsf{len} : \mathsf{arr} \to \{\nu : \mathsf{int} \mid \nu \geq 0\}$ and $\mathit{get}$ requiring $0 \leq i < \mathsf{len}\ a$,

```text
let rec sum a i acc = if i >= len a then acc else sum a (i + 1) (acc + get a i)
let total a = sum a 0 0
```

with $Q = \{0 \leq \nu, \nu < \mathsf{len}\ \star, \nu \leq \mathsf{len}\ \star\}$. The parameter `i` gets $\kappa_i$ with candidates $0 \leq \nu$, $\nu < \mathsf{len}\ a$ and $\nu \leq \mathsf{len}\ a$. The call in `total` gives $\mathsf{len}\ a \geq 0 \wedge \nu = 0 \Rightarrow \kappa_i$, which keeps $0 \leq \nu$ and $\nu \leq \mathsf{len}\ a$ and removes $\nu < \mathsf{len}\ a$ (the array may be empty). The recursive call gives $\kappa_i[i/\nu] \wedge \neg(i \geq \mathsf{len}\ a) \wedge \nu = i + 1 \Rightarrow \kappa_i$, which keeps both $0 \leq \nu$ and $\nu \leq \mathsf{len}\ a$. The check at $\mathit{get}$ is $0 \leq i \wedge i \leq \mathsf{len}\ a \wedge \neg(i \geq \mathsf{len}\ a) \wedge \nu = i \Rightarrow 0 \leq \nu \wedge \nu < \mathsf{len}\ a$, which is valid. The inferred invariant is $0 \leq i \leq \mathsf{len}\ a$, and the bound check in `get` can be removed with no annotation by the user. Rondon et al. (2008) report this kind of result on OCaml benchmarks.

**A missing qualifier.** With $Q = \{\nu < \mathsf{len}\ \star\}$ only, the call in `total` removes the one candidate, $\kappa_i$ becomes $\mathit{true}$, and the check at $\mathit{get}$ fails because $i$ could be negative. The program is safe, but no liquid type over this $Q$ shows it, and the error says only that the qualifiers are not enough.

## Variations

- **Horn clause solving.** The constraints are constrained Horn clauses with the $\kappa$ as unknown predicates. Liquid Haskell's solver, liquid-fixpoint, solves them over qualifiers as above. General Horn clause solvers use interpolation and need no qualifiers, but they may not terminate.
- **Liquid Haskell** (Vazou et al. 2014) adds *measures* (functions such as the length of a list that may be used in refinements), abstract refinements and termination checking, and mines qualifiers from the type signatures in the program.
- **Low-level liquid types** (Rondon et al. 2010) infers refinements for C-like code with pointers and a heap.
- **Houdini** (Flanagan and Leino 2001) runs the same "start with all candidates, remove the refuted ones" loop with a program verifier in place of the SMT queries, to infer annotations for ESC/Java.
- **Abstract interpretation view.** The domain is the finite lattice of conjunctions over $Q^\star$, ordered by inclusion, and the loop is a fixed point iteration in it. A richer domain, such as polyhedra, would need widening to end ([abstract interpretation](/abstract-interpretation/)).

## Pitfalls

- **The qualifiers decide what can be proved.** An error may mean a bug or a missing qualifier, and the tool cannot tell which. Good tools mine qualifiers from annotations and offer defaults.
- **Candidate sets grow fast.** Qualifiers with many holes, or many variables in scope, give large $Q^\star$ and many queries. Keep holes few and scopes small.
- **Monotonicity is needed.** The proof of the strongest solution uses that liquid variables occur only positively on the left of implications. A rule that puts a $\kappa$ under a negation breaks the argument.
- **Decidable logic only.** A nonlinear qualifier makes the SMT queries incomplete. A query that returns "unknown" must be treated as "not valid", which removes the qualifier and may cause a false error.
- **Precision at higher-order calls.** A function passed as an argument gets one liquid type for all its uses inside the callee. Liquid types give each use of a polymorphic function fresh templates for its type variables, which keeps facts about the elements. A monomorphic signature loses them.

## Exercises

1. In the maximum example, why is $\nu \leq x$ kept by $C_1$ but removed by $C_2$? *Answer.* In $C_1$ the result is $x$, so $\nu \leq x$ holds. In $C_2$ the result is $y$ with $x \leq y$, and $y \leq x$ fails when $y > x$, for example $x = 0, y = 1$.
2. Give the bound on the number of passes that change something, for one liquid variable with 6 candidates. *Answer.* At most 6, since each such pass removes at least one candidate, followed by one final pass that changes nothing.
3. Why does SOLVE start from the conjunction of all candidates and not from $\mathit{true}$? *Answer.* Loop invariants are inductive: a fact about `i` at the recursive call follows only if the same fact is assumed for the current `i`. In the sum example, $0 \leq i + 1$ follows from $0 \leq i$ and not from $\mathit{true}$. A loop that starts from $\mathit{true}$ and adds a candidate only when the current facts imply it never adds $0 \leq \nu$. Starting from all candidates assumes them all and then removes those that fail.
4. In the array example, add the qualifier $\nu = \star + 1$. Does the result change? *Answer.* No. In the scope of $\kappa_i$ the only other variable is `a`, which is an array, so $\nu = \star + 1$ has no well-sorted instance. $Q^\star$ for $\kappa_i$ is the same, and the result is still $0 \leq \nu \wedge \nu \leq \mathsf{len}\ a$.

## References
