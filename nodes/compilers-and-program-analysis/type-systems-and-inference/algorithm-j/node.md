---
tag: M228A9
kind: algorithm
slug: algorithm-j
name: Algorithm J
aliases:
- Milner's algorithm J
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: An imperative form of Hindley-Milner inference that keeps one global substitution, updated in place by union-find unification.
solves: [type-inference-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes of the term}
  time: {worst: 2^O(n), best: Θ(n)}
  space: {extra: 2^O(n)}
properties: {deterministic: true, recursive: true}
prereqs: [algorithm-w, disjoint-set-forest, term-dag]
see_also: [algorithm-w, hindley-milner-type-system, principal-type-theorem, union-by-rank, path-compression, occurs-check, constraint-based-type-inference, martelli-montanari-unification]
sources:
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 4 (algorithm J with one global substitution changed by side effects, and the statement that it computes the same result as W)
  - paper: "Didier Remy, Extension of ML type system with a sorted equational theory on types, INRIA Research Report RR-1766, October 1992"
    locator: Section 2 (generalization by ranks, now called levels) and Section 3.3 (ranked unification)
  - paper: doi:10.1145/582153.582176
    title: Luis Damas and Robin Milner, Principal type-schemes for functional programs, Ninth ACM Symposium on Principles of Programming Languages (POPL 1982), pages 207 to 212
    locator: the soundness and completeness of W, which J inherits
  - book: isbn:9780262162289
    title: Benjamin C. Pierce (ed.), Advanced Topics in Types and Programming Languages, MIT Press, 2005
    locator: Chapter 10 by Francois Pottier and Didier Remy, The essence of ML type inference (Section 10.6, efficient constraint solving with a union-find structure, ranks for generalization, and the sharing of types)
  - paper: doi:10.1007/3-540-52590-4_50
    title: A. J. Kfoury, J. Tiuryn and P. Urzyczyn, ML typability is dexptime-complete, CAAP 1990, LNCS 431, Springer, pages 206 to 220
    locator: the exponential time upper bound for typability with types represented as DAGs
---

Algorithm J is the fast form of [algorithm W](/algorithm-w/) for [Hindley-Milner](/hindley-milner-type-system/) type inference. W returns a substitution from each call and composes them. J keeps one global substitution instead, stored in a [union-find structure](/disjoint-set-forest/), and changes it in place. Unification links classes of type variables, and a type variable that gets a value points to a shared type node. So types are DAGs, not trees, and a substitution is never applied to the whole context. Milner gave J in his 1978 paper, next to W, as the version to implement. With Rémy's levels for generalization, it is the core of the type checkers of OCaml and many other ML compilers. It returns exactly the principal types that W returns.

## In plain words

W keeps writing out new lists of facts, such as "placeholder a is a number", and copies them into every type it knows. J keeps one notice board instead. It pins each fact on the board once, and reads a type by following the pins. Two placeholders that must be equal join one group, so a later fact about one of them is a fact about both.

Because J follows pins instead of making copies, a big type that is used in many places is stored once. For some programs this is the difference between a few dozen boxes and many billions.

J also records how deep inside nested `let` definitions each placeholder was made. At the end of a definition, the placeholders made inside it that never joined anything outside are free to vary. J finds them from this number, without a search.

## The problem

The input and output are those of algorithm W: a context $\Gamma$ and a term $e$ in the language `x`, `fun x -> e`, `e1 e2`, `let x = e1 in e2`, with constants, `if`, integer operators and `fix f x -> e`. J returns a type $\tau$. The global substitution $E$ at the end gives the answer: $E\Gamma \vdash e : E\tau$, and for a closed term $E\tau$ is the principal type. If the term has no type, J fails. This is the [type inference problem](/type-inference-problem/) for ML.

## The algorithm

Type variables are nodes of a union-find structure. A root variable has no value. A non-root variable points to another variable or to a type node $a \to b$, $\mathsf{int}$ or $\mathsf{bool}$. FIND follows the pointers with [path compression](/path-compression/). Each root has a rank for [union by rank](/union-by-rank/) and a *level*, the `let` depth at which it was made. The global counter *depth* starts at 0.

```pseudo id=main
J(Γ, e)                                   ▷ E is the global substitution; returns τ with E(Γ) ⊢ e : E(τ)
L1  if e is a variable x then let ∀α1 ... αk. τ be Γ(x)      ▷ fail if x is not in Γ
L2      return a copy of τ with α1 ... αk replaced by fresh variables   ▷ copy each shared node once
L3  if e is fun x -> e1 then β ← fresh
L4      return β → J((Γ, x : β), e1)
L5  if e is e1 e2 then τ1 ← J(Γ, e1), τ2 ← J(Γ, e2), β ← fresh
L6      UNIFY(τ1, τ2 → β), return β
L7  if e is let x = e1 in e2 then depth ← depth + 1, τ1 ← J(Γ, e1), depth ← depth - 1
L8      σ ← GEN(τ1), return J((Γ, x : σ), e2)          ▷ GEN quantifies the variables of level > depth

UNIFY(τ1, τ2)
L9  τ1 ← FIND(τ1), τ2 ← FIND(τ2), if τ1 and τ2 are the same node then return
L10 if both are root variables then link them by rank, and give the root the smaller level
L11 else if one is a root variable v and the other a node t then OCCURS-ADJUST(v, t), point v to t
L12 else if τ1 = a1 → b1 and τ2 = a2 → b2 then UNIFY(a1, a2), UNIFY(b1, b2)
L13 else fail                                         ▷ int against bool, or a base type against an arrow
```

OCCURS-ADJUST$(v, t)$ walks the nodes of $t$ once, with FIND at each step. It fails if it reaches $v$, which is the [occurs check](/occurs-check/). Otherwise it lowers the level of each root variable of $t$ to at most the level of $v$. Both walks in L2 and L11, and the pairs in L12, use a table of the nodes already seen, so each walk is linear in the size of the DAG and not of the tree. `fix f x -> e1` makes fresh $\alpha, \beta$, types $e_1$ with $f : \alpha \to \beta$ and $x : \alpha$, and unifies $\beta$ with the result. `if` and the operators call UNIFY with $\mathsf{bool}$, $\mathsf{int}$ or the other branch.

The classic version of GEN, as in Milner's paper, quantifies the variables of the resolved $\tau_1$ that are not free in the resolved context. The version with levels gives the same set and costs only a walk over $\tau_1$.

## Example

Take `let id = fun x -> x in id id`, with levels.

| step | action | state |
|---|---|---|
| L7 | depth becomes 1, then L3 makes $\beta_0$ | $\beta_0$ has level 1, and $\tau_1 = \beta_0 \to \beta_0$ |
| L7 | depth becomes 0 again | |
| L8 | GEN: $\beta_0$ has level $1 > 0$ | $\sigma = \forall \beta_0.\, \beta_0 \to \beta_0$ |
| L2 | two copies of $\sigma$ | $\beta_1 \to \beta_1$ and $\beta_2 \to \beta_2$, both at level 0 |
| L5 | $\beta_3$ fresh | |
| L12 | UNIFY$(\beta_1 \to \beta_1,\ (\beta_2 \to \beta_2) \to \beta_3)$ | decompose into two pairs |
| L11 | UNIFY$(\beta_1,\ \beta_2 \to \beta_2)$ | $\beta_1$ points to the node $N = \beta_2 \to \beta_2$ |
| L11 | UNIFY$(\beta_1, \beta_3)$: FIND$(\beta_1) = N$ | $\beta_3$ points to the same node $N$ |

The result $\beta_3$ resolves to $N$, so the type is $a \to a$. The node $N$ is shared: $\beta_1$ and $\beta_3$ both point to it, and no copy of it was made. W, on the same term, builds the substitution $[\beta_1 := \beta_2 \to \beta_2,\ \beta_3 := \beta_2 \to \beta_2]$ with two copies of the type.

Sharing can save a lot. In the family $f_0 = $ `fun x -> fun z -> z x x`, $f_i = $ `fun y -> ` $f_{i-1}\ (f_{i-1}\ y)$, nested by `let`, the principal type of $f_k$ has $2^{k+2} + 2$ nodes in J's DAG, and $6 \cdot 2^{2^k} - 3$ nodes as a tree. For $k = 5$, that is 130 nodes against 25,769,803,773.

## Correctness

Each step of UNIFY is a step of the [Martelli-Montanari rules](/martelli-montanari-unification/). So if UNIFY starts with the substitution $E$, it ends with $UE$, where $U$ is a most general unifier of $E\tau_1$ and $E\tau_2$, or it fails when there is none. Path compression and union by rank change the representation but not the substitution. With this fact, the cases of J perform the same unifications as the cases of W, in the same order, on the context $E\Gamma$. The soundness and completeness proofs of W then carry over, and J returns the principal type. For levels, two invariants show that a variable of $\tau_1$ has a level above the current depth exactly when it is not free in the resolved context. The [proof file](proofs/correctness.md) gives the full proof.

## Complexity

Let $n$ be the number of nodes of the term.

- **Without `let`.** With an occurs check at each binding, as in L11, the time is $O(n^2)$ in the worst case. With one test for cycles at the end in place of the occurs checks, unification on the DAG takes $O(n\,\alpha(n))$ time.
- **With `let`.** Each copy at L2 costs time linear in the DAG size of the scheme. The DAG grows by at most its own size at each copy, so the time and the space are $2^{O(n)}$. This matches the upper bound of Kfoury, Tiuryn and Urzyczyn (1990).
- **Lower bound.** Typability is [complete for EXPTIME](/ml-typability-dexptime-completeness/), so no algorithm is polynomial. The sharing does not always help: in the family $y_0 = $ `fun x -> x`, $y_i = $ `fun z -> z` $y_{i-1}\ y_{i-1}$, each use of $y_{i-1}$ is a copy with new variables, and the DAG of $y_k$ has $6 \cdot 2^k - 4$ nodes.
- **Generalization.** With levels, GEN costs time linear in the DAG of $\tau_1$. The classic version also walks the whole context at each `let`, which costs $O(n)$ per `let` even for small types.

## Properties

- **Same results as W.** On each closed term, J and W both fail, or both return the principal type, up to renaming.
- **Imperative.** J changes a global structure. A type that J returned earlier can change its meaning when a later unification links one of its variables. So J must always read types through FIND.
- **Shared types.** Copies are made only at L2, and only of the quantified part. The result is a DAG.
- **Not backtracking.** A failed unification leaves the structure half changed. A compiler that reports an error and goes on must undo the changes or start again.

## Variants and improvements

- **Levels (Rémy 1992).** The version above. It replaces the scan of the context by a level check, and OCaml uses it.
- **Occurs check at the end.** Skip the check in L11, and look for cycles only before GEN and at the end. This gives the near-linear bound for terms without `let`. With [recursive types](/recursive-types/), cycles are allowed and the check goes away.
- **[Constraint-based inference](/constraint-based-type-inference/).** Pottier and Rémy's solver for HM(X) works on the same union-find structure with ranks, but it first builds a constraint and then solves it.
- **[Algorithm W](/algorithm-w/).** The functional version, easier to prove correct and slower to run.

## When to use it

Use J, with levels, whenever you implement Hindley-Milner inference for real programs. It is the standard design in compilers of ML-family languages. Use W instead when you want a short, pure program that follows the proofs, or when you need to keep the old states, for example in a type checker that tries several branches.

## Pitfalls

- **Reading a type without FIND.** A type node may contain a variable that now points elsewhere. Each walk must call FIND at each node, as in L9 and in OCCURS-ADJUST.
- **Copying shared nodes more than once.** A copy at L2, or a walk in OCCURS-ADJUST, that does not keep a table of seen nodes treats the DAG as a tree. Then it takes doubly exponential time on the $f_k$ family above.
- **Wrong levels.** If L10 keeps the larger level, or L11 does not lower the levels of $t$, GEN quantifies a variable that is still free in the context. Then `fun x -> let y = x in if y true then y 1 else 0` gets a type, and its application to `5` gets stuck.
- **Forgetting to restore the depth.** L7 must lower the depth after typing $e_1$, also when $e_1$ fails and the error is caught.
- **Equality of nodes.** L9 compares nodes, not the trees they stand for. A structural comparison of two big DAGs can take exponential time.

## Implementations

## History

Milner (1978) presented algorithm W for the proofs and algorithm J for the implementation of ML in the LCF system. He showed that J computes the same result as W, with one global substitution changed by side effects. Rémy's work on records, around 1989 to 1992, introduced ranks of type variables for fast generalization. These ranks, now called levels, are what the OCaml type checker uses. Pottier and Rémy (2005) described a constraint solver for ML type inference with the same data structures.

## References
