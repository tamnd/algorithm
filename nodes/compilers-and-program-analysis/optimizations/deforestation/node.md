---
tag: 2RK0F8
kind: technique
slug: deforestation
name: Deforestation
aliases:
- Wadler deforestation
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Removes the intermediate trees and lists that one function builds and the next consumes, by fusing the two into one pass.
prereqs: [function-inlining, term]
see_also: [supercompilation, partial-evaluation, loop-fusion, kernel-fusion, term-rewriting-system, termination, beta-reduction]
sources:
  - paper: doi:10.1016/0304-3975(90)90147-A
    title: "Philip Wadler, Deforestation: transforming programs to eliminate trees, Theoretical Computer Science 73(2), 1990, 231-248"
    locator: treeless terms and their linearity condition, the transformation rules with case of case and folding, and the theorem that a composition of treeless functions becomes one treeless function
  - paper: doi:10.1145/227699.227716
    title: David Sands, Total correctness by local improvement in the transformation of functional programs, ACM Transactions on Programming Languages and Systems 18(2), 1996, 175-234
    locator: the improvement theorem, which makes folding in unfold and fold transformations totally correct, applied to deforestation
  - paper: doi:10.1145/165180.165214
    title: Andrew Gill, John Launchbury and Simon L. Peyton Jones, A short cut to deforestation, FPCA 1993, 223-232
    locator: the foldr and build rule, its proof by parametricity, and its use in the Glasgow Haskell compiler
  - paper: doi:10.1145/141471.141494
    title: Wei-Ngan Chin, Safe fusion of functional expressions, LISP and Functional Programming (LFP 1992), 11-20
    locator: the extension of deforestation to programs that are not treeless, by marking the arguments that are not safe to fuse
  - paper: doi:10.1145/1291151.1291199
    title: "Duncan Coutts, Roman Leshchinskiy and Don Stewart, Stream fusion: from lists to streams to nothing at all, ICFP 2007, 315-326"
    locator: list functions written as stream producers and consumers, so that fusion also covers left folds and zips
---

Deforestation is a program transformation of Wadler (1988, journal version 1990) that takes a composition of functions, where one function builds a data structure and the next one takes it apart, and makes one function that gives the same result without building the structure. For `len(app(xs, ys))`, the list that `app` builds is gone, and the new function counts the two lists in one pass. The transformation unfolds calls, moves a `case` that inspects the result of another `case` into its branches, picks a branch when the inspected value is a known constructor, and folds a term that is a renaming of an earlier term into a call of a new recursive function. Wadler's theorem says that if every function is *treeless*, which means that it passes and inspects only variables, then the transformation stops and the result is again treeless, so it builds no intermediate trees. The common mistake is to apply it to any functional program and expect it to stop: with an accumulating parameter, such as the second argument of a reverse with an accumulator, the terms grow without end and no fold is ever found.

## In plain words

Many programs are written as a pipeline: one function makes a list, the next one changes it, and the last one sums it. This is clear, but each stage makes a whole new list in memory that the next stage reads once and throws away.

Deforestation rewrites the pipeline into one function that does all the stages for each element in turn. It works by expanding each function call into its body. When a test looks at a value that the code just built, the answer is known, so the test and the building both go. When the expanded code comes back to a call it has seen before, the rewriter turns that point into a loop.

This always works when each function only passes plain variables to calls and only tests plain variables. Then the new function builds only its own result.

## When it applies

- The program is functional and first-order, with algebraic data types and `case` on flat patterns, as in the template. Higher-order programs need the variations at the end.
- The stages are compositions such as `f(g(x))`, where the result of `g` is used only by `f`.
- Every function is treeless, or close to it: no call argument and no `case` selector is a constructed term, and no variable is used twice in one branch. Most list and tree functions that walk their input once, such as `app`, `len`, `map` and a tree mirror, are treeless. Functions with accumulators are not.
- The language is lazy, or the functions are total. The rules are equations of call by name.

## The template

**Language.** A program is a list of equations $f(x_1, \ldots, x_n) = b$. A term $t$ is a variable $x$, a constructor term $c(t_1, \ldots, t_n)$, a call $f(t_1, \ldots, t_n)$, or $\mathtt{case}\ t_0\ \mathtt{of}\ p_1 \to u_1 \mid \cdots \mid p_k \to u_k$, where each pattern $p_i$ is $c_i(y_1, \ldots, y_m)$ with fresh variables. The meaning is call by name: a call is replaced by its body with the arguments put in for the parameters, and a `case` on $c(\bar t)$ takes the branch for $c$ with $\bar t$ put in for its pattern variables.

**Treeless terms.** A term is *treeless* if every argument of a call is a variable, every selector of a `case` is a variable, and it is *linear*: on every path that takes one branch of each `case`, no variable occurs twice. A function is treeless if its body is. For example, `app(xs, ys) = case xs of Nil -> ys | Cons(x, r) -> Cons(x, app(r, ys))` is treeless: `ys` occurs in both branches, but only once on each path.

**Case contexts.** A *case context* is $E = [\,]$ or $E = \mathtt{case}\ E'\ \mathtt{of}\ \mathit{alts}$. Every term can be written in one way as $E[r]$, where the *redex* $r$ is a variable, a constructor term or a call. The transformation $\mathcal{T}$ looks at the redex:

1. $\mathcal{T}[x] = x$.
2. $\mathcal{T}[c(t_1, \ldots, t_n)] = c(\mathcal{T}[t_1], \ldots, \mathcal{T}[t_n])$.
3. $\mathcal{T}[E[\mathtt{case}\ x\ \mathtt{of}\ p_i \to u_i]] = \mathtt{case}\ x\ \mathtt{of}\ p_i \to \mathcal{T}[E[u_i]]$, with the pattern variables renamed fresh. For $E$ not empty, this moves the outer `case` frames into the branches; it is Wadler's case of case rule for a variable selector.
4. $\mathcal{T}[E[\mathtt{case}\ c(\bar t)\ \mathtt{of}\ \ldots \mid c(\bar y) \to u \mid \ldots]] = \mathcal{T}[E[u[\bar t / \bar y]]]$.
5. $\mathcal{T}[E[f(\bar t)]]$, with $f(\bar x) = b$: let $\bar z$ be the free variables of the term $E[f(\bar t)]$. If this term is a renaming of a term met before, with name $h'$, give the call $h'$ on the renamed variables (a *fold*). Otherwise make a new function name $h$, define $h(\bar z) = \mathcal{T}[E[b[\bar t / \bar x]]]$ (an *unfold*), and give $h(\bar z)$.

The start term $t_0$ is built from variables, constructors and calls, such as `app(app(a, b), c)`. The result is $\mathcal{T}[t_0]$ and the new functions.

**Legality.** *Theorem. Let every function of the program be treeless and let $t_0$ have no `case`. Then (a) $\mathcal{T}$ stops; (b) every new function is a treeless term except for linearity: its call arguments and `case` selectors are variables; (c) for every input, $\mathcal{T}[t_0]$ and $t_0$ have the same value, or both have none.*

**Profit.** *(d) In a run of the new functions, every value that a `case` inspects is a subtree of an input, and every constructor that the run builds is a part of the final result.* So the only cells that the new program allocates are the new cells of its result. The source program allocates those and all the cells of its intermediate structures. The number of calls and `case` steps also goes down in the examples below; Wadler shows that, with linearity, the new program never does more steps than the source.

**Proof of (a).** Let $P$ be the finite set of all subterms of the function bodies that are not variables, together with the *generic* pieces $f(x_1, \ldots, x_n)$ for each function and $c(x_1, \ldots, x_n)$ for each constructor. A *piece tree* is a tree whose nodes hold a piece $s \in P$, with one child for each free variable of $s$; a leaf is a variable. It stands for the term $s[\bar z := \bar u]$, where $\bar u$ are the terms of the children. Its height is 0 for a leaf and 1 plus the largest height of a child otherwise. $t_0$ has a piece tree of generic pieces whose height $h_0$ is its depth.

*Claim: every term that $\mathcal{T}$ meets has a piece tree of height at most $h_0$.* We follow each rule on the piece tree. Because bodies are treeless, a `case` piece has a variable selector, so the `case` frames of $E$ form a chain of nodes, each one the selector child of the one above. The redex is the node at the end of the chain, and its piece has the redex's symbol at the top. Also, the branches of a frame are pieces whose own pattern variables have not been replaced.

- Rule 5, unfold: the redex node holds a call piece. A call piece is $f(\bar z)$ with variables $\bar z$, since bodies are treeless, so its children are $\bar t$. Replace the node by one that holds the body $b$, with the same children for $\bar x$. The height does not change.
- Rule 4: the redex node holds a piece $c(s_1, \ldots, s_n)$ with children $\bar w$, and its parent holds a `case` piece with children $\bar v$ for its other variables. Replace the parent by a node that holds the branch $u$, with children $\bar v$ for its outer variables and, for each $y_j$, the node $s_j$ with children taken from $\bar w$ (or the child of $\bar w$ itself if $s_j$ is a variable). Every child of the new node has height below that of the old parent, so the height does not grow.
- Rule 3: the selector child of the frame is a leaf $x$. Replace the frame node by a node that holds $u_i$, with fresh leaves for the pattern variables. The height does not grow.
- Rule 2: the new terms are the children of the root. Rule 1 makes no new term.

So the claim holds. There are finitely many piece trees of height at most $h_0$ with nodes in $P$, up to renaming of the leaves, so there is a finite number $N$ of terms, up to renaming, that $\mathcal{T}$ can meet, and their sizes are bounded by some $S$.

Now look at the tree of calls of $\mathcal{T}$. Each node has finitely many children. On a path, the nodes where rule 5 unfolds hold terms that are not renamings of each other, since a renaming of an earlier term is folded. So a path has at most $N$ unfolds. Define the size $D$ of a term as for a tree, but with the largest branch of each `case` in place of the sum of its branches. Rules 2, 3 and 4 make the term smaller in $D$: rule 4 removes a `case` and a constructor, and puts each $t_j$ in for $y_j$, which occurs at most once on each path of $u$ by linearity, so $D$ goes down by at least 2. So between two unfolds a path has at most $S$ steps. Every path has at most $(N + 1)(S + 1)$ nodes, and a tree with finite branching and bounded paths is finite. $\square$

**Proof of (b).** The rules give back only a variable (rule 1), a constructor of transformed terms (rule 2), a `case` on a variable $x$ (rule 3) and a call $h(\bar z)$ on variables (rule 5). By induction on the tree of calls, every new body is built from these. $\square$

**Proof of (c).** Each rule is an equation of call by name: rule 4 is the step for a `case` on a constructor, rule 5 without the fold is the step for a call, rule 3 holds because both sides take the same branch for each value of $x$, and rule 2 is trivial. Fix the term $\tau_h$ that rule 5 met when it made $h$, so $h(\bar z) = \mathcal{T}[\tau_h]$. *If $h$ gives a value, $\tau_h$ gives the same value*: the meanings $\bar z \mapsto [\![\tau_h]\!]$ satisfy every equation of the new program, by the rules, and a recursive program means the least solution of its equations. *If $\tau_h$ gives a value $v$, so does $h$*: let $n$ be the number of call steps that call by name uses to evaluate $\tau_h$ in full. Rules 2, 3 and 4 keep $n$, or split it among the parts for rule 2, and rule 5 lowers it by one. Every call of a function $h'$ in the body of $h$, from a fold or from an unfold further down, is made at a term $\tau'$ that is a renaming of $\tau_{h'}$ and is reached after the unfold of $\tau_h$, so evaluating $\tau'$ takes fewer than $n$ call steps. By induction on $n$, that call gives the value of $\tau'$, and so the body of $h$ gives $v$. Sands (1996) proves the same result in a general form for lazy languages with sharing, as total correctness of the improvement relation. $\square$

**Proof of (d).** In a run of a treeless program, every variable is bound either to an argument of a call, which is the value of a variable by (b), or to a field of a value that a `case` inspects. The root call gets the inputs. By induction on the run, every variable holds a subtree of an input, and so every `case`, whose selector is a variable, inspects one. A constructor term in a treeless term can only be the whole body, a branch, or a field of a larger constructor term, because call arguments and selectors are variables. So its value is part of the value of the body, and a call can also only be a body, a branch or a field, so this value is part of the value of the root call. $\square$

## Classic examples

The numbers below come from a short script that implements the rules above, with folding on any earlier term up to renaming and with function wrappers $h(\bar z) = g(\bar z)$ removed. Each new program was checked against the source on 200 random inputs: lists of length 0 to 6, and trees of depth at most 5 where each node is a leaf with probability 0.3, from a generator with seed 1. The counts are the constructor cells, the calls and the `case` steps of call by name on the stated inputs.

**Three appends.** The source is `app(app(a, b), c)`. The new program, with names chosen for reading, is

```
app3(a, b, c) = case a of
                  Nil -> (case b of
                            Nil -> c
                          | Cons(x, r) -> Cons(x, app2(r, c)))
                | Cons(x, r) -> Cons(x, app3(r, b, c))
app2(r, c)    = case r of Nil -> c | Cons(x, s) -> Cons(x, app2(s, c))
```

`app2` is `app` again, and the `case b` in the `Nil` branch is one step of it, unrolled by rule 4. The source copies `a` twice and `b` once. With lengths $n$, $m$ and $k$:

| lengths $n, m, k$ | cells, source | cells, new | calls, source | calls, new | case steps, source | case steps, new |
|---|---|---|---|---|---|---|
| 3, 4, 5 | 10 | 7 | 12 | 8 | 12 | 9 |
| 10, 10, 10 | 30 | 20 | 32 | 21 | 32 | 22 |
| 100, 0, 0 | 200 | 100 | 202 | 101 | 202 | 102 |

In general the source builds $2n + m$ cells and does $2n + m + 2$ calls, and the new program builds $n + m$ cells, the new cells of the result, and does $n + m + 1$ calls.

**Length of an append.** The source is `len(app(a, b))`, with `len(xs) = case xs of Nil -> Z | Cons(x, r) -> S(len(r))` on numbers in unary. The new program is `lenapp(a, b) = case a of Nil -> (case b of Nil -> Z | Cons(x, r) -> S(len2(r))) | Cons(x, r) -> S(lenapp(r, b))`, where `len2` is `len` again and the `Nil` branch holds one step of it. For $n = 3$ and $m = 4$, the source builds 11 cells, 3 list cells and the 8 cells of the number, and does 12 calls and 12 case steps. The new program builds only the 8 cells of the number, with 8 calls and 9 case steps. For $n = m = 10$ the counts are 31, 32, 32 against 21, 21, 22.

**Mirror twice.** With `flip(t) = case t of Leaf(n) -> Leaf(n) | Node(l, r) -> Node(flip(r), flip(l))`, the source `flip(flip(t))` becomes

```
ff(t) = case t of Leaf(n) -> Leaf(n) | Node(l, r) -> Node(ff(l), ff(r))
```

The two swaps cancel inside the transformation: the inner `flip` swaps the children, and the outer `case` on that `Node` takes them back in the other order. On a full tree of depth 3, with 15 nodes, the source builds 30 cells and the new program 15; on depth 5, with 63 nodes, 126 against 63. The calls and case steps drop by half in the same way. The result is a copy function, not the identity: deforestation does not know that a copy of $t$ is $t$.

## Variations

- **Short cut fusion.** Gill, Launchbury and Peyton Jones (1993) write list producers with `build g = g (fun x -> fun r -> Cons(x, r)) Nil` and consumers with `foldr`, and use the single rule `foldr k z (build g) = g k z`. The rule is correct by parametricity whenever `g` is polymorphic in the list type. It needs no folding and no termination check, and it is the form that the Glasgow Haskell compiler uses.
- **Stream fusion.** Coutts, Leshchinskiy and Stewart (2007) write list functions as producers and consumers of streams, with a non-recursive step function, so that fusion by inlining also covers left folds, `zip` and filters.
- **Programs that are not treeless.** Chin (1992) marks the arguments and selectors that are not safe, such as an accumulator, and fuses only the rest. Generalization, as in [supercompilation](/supercompilation/), is another way to stop.
- **Higher order.** Marlow and Wadler extended the rules to programs with `fun x -> e`, where a call of a variable function must be handled as well.
- **Positive information.** Rule 3 does not put the pattern $p_i$ in for $x$ in the branches. [Supercompilation](/supercompilation/) does, and with this and generalization it can do all that deforestation does and more, such as specializing a naive string matcher into a matcher in the style of Knuth, Morris and Pratt.
- **Imperative fusion.** [Loop fusion](/loop-fusion/) and [kernel fusion](/kernel-fusion/) join loops or GPU kernels so that an array that one writes and the next reads stays in registers or never exists. They are the same idea for arrays, with dependence tests in place of treeless terms.

## Pitfalls

- **Accumulating parameters.** `revacc(xs, acc) = case xs of Nil -> acc | Cons(x, r) -> revacc(r, Cons(x, acc))` is not treeless: a call argument is a constructor term. From `revacc(a, Nil)` the transformation meets `revacc(r1, Cons(x1, Nil))`, then `revacc(r2, Cons(x2, Cons(x1, Nil)))`, and so on. The script stopped at its depth limit of 40 after 14 call terms of sizes 3, 5, 7, 9 and up, with no fold. Generalize the accumulator, or leave such calls alone.
- **Lost sharing.** Linearity is part of the theorem. With `dup(x) = Pair(x, x)`, unfolding `dup(g(y))` gives `Pair(g(y), g(y))`, and a lazy program with sharing would compute `g(y)` once, the new program twice. Let insertion, or leaving the call alone, keeps the cost.
- **Strict languages.** The rules are equations of call by name. In a strict language, unfolding `first(x, y) = x` in `first(a, loop(b))` drops a call that does not stop, so the new program stops where the source did not. This is safe only when the dropped arguments are known to stop.
- **Code growth.** Rule 3 copies the outer frames into each branch, and rule 4 unrolls the first step of a function in a branch, as with `app2` and `len2`. Deep compositions with many branches grow the code.
- **No algebra.** The transformation does not prove laws. `flip(flip(t))` becomes a copy, not `t`, and `len(app(a, b))` does not become a sum of two lengths.
- **Folds only up to renaming.** A fold needs an earlier term that is the same up to the names of variables. A term that differs in a constant or in the order of two independent frames is not folded, and the process goes on to a later, possibly much larger, match.

## Exercises

1. Give the new program for `map(f1, map(f2, xs))` in a first-order form, where `map1` and `map2` are two first-order versions of `map` that apply fixed functions `g1` and `g2` to each element. How many cells do the source and the new program build on a list of length $n$?
2. Show that `sum(app(a, b))` is treeless as a composition, and give the new program and its counts of calls on lists of lengths $n$ and $m$.
3. Find the piece tree of height 2 for `app(app(a, b), c)`, and follow it through the first three steps of the transformation.
4. Show that the bound of the termination proof fails without linearity: give a term where rule 4 makes the size $D$ grow.
5. Change rule 5 so that each call argument that is a constructor term is first bound by a `let` to a fresh variable. Transform `revacc(a, Nil)` with this rule and show that a fold is found after one unfold. Does property (d) still hold for the new program?

## References
