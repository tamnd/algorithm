---
tag: WE1B25
kind: algorithm
slug: binding-time-analysis
name: Binding-time analysis
aliases:
- BTA
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Marks each expression static or dynamic by whether it depends only on known input, which guides offline partial evaluation.
model: word-ram
complexity:
  vars: {N: the number of nodes of the program term, T: the total size of the simple types of all nodes and binders written as trees}
  time: {worst: O(N T)}
  space: {extra: Θ(T)}
properties: {deterministic: true, recursive: true, online: false, exact: true}
prereqs: [partial-evaluation, simply-typed-lambda-calculus, robinson-unification, horn-sat-forward-chaining]
see_also: [futamura-projections, supercompilation, constraint-based-type-inference, abstract-interpretation, sparse-conditional-constant-propagation, self-optimizing-ast-interpreter, meta-tracing, k-cfa]
sources:
  - book: isbn:9780130202499
    title: Neil D. Jones, Carsten K. Gomard and Peter Sestoft, Partial Evaluation and Automatic Program Generation, Prentice Hall, 1993
    locator: the chapters on offline partial evaluation, binding-time analysis, congruence and the partial evaluation of the lambda calculus
  - paper: doi:10.1017/S0956796800000058
    title: Carsten K. Gomard and Neil D. Jones, A partial evaluator for the untyped lambda-calculus, Journal of Functional Programming 1(1), 1991, 21-69
    locator: the two-level lambda calculus, the binding-time rules with lift, and the correctness of the specializer for well-annotated terms
  - paper: doi:10.1007/3540543961_22
    title: Fritz Henglein, Efficient type inference for higher-order binding-time analysis, Functional Programming Languages and Computer Architecture (FPCA 1991), LNCS 523, 448-472
    locator: binding-time analysis as constraint solving over annotated types, in almost linear time
  - paper: doi:10.1145/243439.243447
    title: Neil D. Jones, An introduction to partial evaluation, ACM Computing Surveys 28(3), 1996, 480-503
    locator: offline and online specialization, and the role of the binding-time analysis
  - paper: doi:10.1016/0304-3975(75)90017-1
    title: Gordon D. Plotkin, Call-by-name, call-by-value and the λ-calculus, Theoretical Computer Science 1(2), 1975, 125-159
    locator: the soundness of the call-by-value calculus for operational equivalence, used in the correctness proof
---

Binding-time analysis (BTA) is the first phase of offline [partial evaluation](/partial-evaluation/). The input is a program and a split of its inputs into *static* inputs, known at specialization time, and *dynamic* inputs, known only later. BTA marks every expression static ($S$) when the specializer can compute its value from the static inputs alone, and dynamic ($D$) when it must emit code for it. The result is a two-level program. The specializer then follows the marks without any more decisions: it runs the $S$ parts and rebuilds the $D$ parts. The marks must obey a *congruence* condition, which guarantees that the specializer never meets a dynamic value where it needs a static one. This page gives a BTA for a higher-order language with recursion as the least solution of Horn implications over annotated types.

## In plain words

Some of a program's inputs are known early, and some only later. Before we specialize the program, we go through it once and label every part. A part gets the label "known now" if it only uses inputs that are known early. Everything else gets the label "known later", and the specializer must write code for it. The labels spread: a part that uses a "later" value is itself "later". A function that takes a "later" argument gives a "later" result. The analysis finds the labels that keep as much as possible "known now" while every rule still holds. The specializer then reads the labels and does the work without guessing. The labels do not promise that specialization stops: a loop that is "known now" can run forever.

## The problem

**The language.** Terms of the toy lambda language with call by value: variables, constants, `fun x -> e`, application `e1 e2`, `let x = e1 in e2`, `if e0 then e1 else e2`, binary operators `+ - * < ==` on integers, and recursive functions `fix f x -> e`, where `f` names the function itself. The free variables of the program are its inputs, all of base type (int or bool). The program has a simple type; `let` is monomorphic.

**Annotated types.** A binding time is $S$ or $D$, with $S \sqsubseteq D$. An annotated type puts a binding time on every type constructor:

$$\tau ::= \mathrm{base}^{\beta} \mid (\tau_1 \to^{\beta} \tau_2), \qquad \beta \in \{S, D\}.$$

$\mathrm{top}(\tau)$ is the binding time of the outer constructor. A static function $(\tau_1 \to^S \tau_2)$ is a closure that the specializer can call, which unfolds its body. A dynamic function $(\tau_1 \to^D \tau_2)$ is code. Code can only take code and give code, so a type is *well formed* when $\mathrm{top}(\tau) = D$ implies that its parts have $D$ on top, at every level.

**Flow.** When a value of type $\tau$ goes to a place of type $\tau'$, we write $\mathrm{flow}(\tau, \tau')$. At base type it means $\mathrm{top}(\tau) = D \Rightarrow \mathrm{top}(\tau') = D$: a static constant can be *lifted* into code, so an $S$ value may go to a $D$ place. At function type it means $\tau = \tau'$ on every constructor, because a closure cannot be turned into code in this setting.

**Congruence.** An annotation gives an annotated type with the same shape as the simple type to every node and every binder. It is *congruent* when all types are well formed, every dynamic input has $D$ on top, a function-typed program has $D$ on top, and every node obeys its rule:

| node, with type $\tau$ | rule |
|---|---|
| variable `x`, binder type $\tau_x$ | $\mathrm{flow}(\tau_x, \tau)$ |
| constant | none |
| `fun x -> e1`, $\tau = (\tau_x \to^{\beta} \tau_r)$ | $\mathrm{flow}(\tau_1, \tau_r)$; $\mathrm{top}(\tau_x) = D \Rightarrow \mathrm{top}(\tau_r) = D$ |
| `e1 e2`, $\tau_1 = (\tau_a \to^{\beta} \tau_r)$ | $\mathrm{flow}(\tau_2, \tau_a)$; $\mathrm{flow}(\tau_r, \tau)$ |
| `let x = e1 in e2` | $\mathrm{flow}(\tau_1, \tau_x)$; $\mathrm{flow}(\tau_2, \tau)$; $\mathrm{top}(\tau_x) = D \Rightarrow \mathrm{top}(\tau) = D$ |
| `if e0 then e1 else e2` | $\mathrm{flow}(\tau_1, \tau)$; $\mathrm{flow}(\tau_2, \tau)$; $\mathrm{top}(\tau_0) = D \Rightarrow \mathrm{top}(\tau) = D$ |
| `e1 op e2` | $\mathrm{top}(\tau_i) = D \Rightarrow \mathrm{top}(\tau) = D$ for $i = 1, 2$ |
| `fix f x -> e1`, $\tau = \tau_f = (\tau_x \to^{\beta} \tau_r)$ | as for `fun`, and $\mathrm{top}(\tau_x) = D \Rightarrow \beta = D$ |

Here $\tau_i$ is the type of the subterm $e_i$. Three rules need a reason. A static function with a dynamic parameter is unfolded with a residual `let` for the argument (let insertion), so its body result is code: that is the rule $\mathrm{top}(\tau_x) = D \Rightarrow \mathrm{top}(\tau_r) = D$. The same holds for a `let` whose variable is dynamic. A recursive function with a dynamic parameter is made dynamic, because unfolding it would not stop: nothing static decides when the recursion ends.

**Goal.** Among the congruent annotations, find the least one, the one with the fewest $D$ marks. There is a least one, because the rules are Horn implications and the set of solutions is closed under intersection.

**The specializer.** Given a congruent annotation and values for the static inputs, the specializer works on the term. On an $S$ node it computes a value: a constant or a closure. On a $D$ node it builds code with fresh variable names. Where an $S$ constant meets a $D$ place, it lifts the constant into code. A static call with a dynamic argument binds the argument with a residual `let`, unless the argument is a variable or a constant. The *residual program* is the code for the root, or the lifted constant when the root is $S$.

## The algorithm

```pseudo id=main
BTA(e, static, dynamic)
L1  infer the simple types of all nodes and binders of e by unification; fail if there are none
L2  copy each simple type into an annotated type, with a fresh variable on every constructor
L3  for each dynamic input x add the fact top(x) = D
L4  walk e and add the implications of the rule of each node; flow at function type adds both directions
L5  for each annotated function type (t1 ->b t2) add b = D => top(t1) = D and b = D => top(t2) = D
L6  if e has a function type then add the fact top(e) = D
L7  Dset <- the variables reachable from a fact along the implications
L8  if the variable of a static input is in Dset then fail
L9  return the annotation: a variable is D if it is in Dset, and S otherwise
```

L1 resolves a type variable that is left over to int; any base type would do. L2 gives a binder its own annotated type, and a `fun` or `fix` node shares its parameter part with the binder. L7 is the forward chaining of [Horn satisfiability](/horn-sat-forward-chaining/): every constraint is an implication between two variables or a fact, so the least model is the set of variables reachable from the facts. L8 cannot fire when all inputs have base type, because no implication ends at the variable of an input. It guards extensions with structured inputs.

## Example

**Power.** The program, with static `s` and dynamic `d`:

```
(fix p n -> fun x -> if n == 0 then 1 else x * p (n - 1) x) s d
```

It has 20 nodes. L2 makes 36 binding-time variables, L4 and L5 add 67 implications, and the one fact is $\mathrm{top}(d) = D$. L7 marks 18 variables $D$. The annotated program, with a leading `_` on dynamic operators, `@` for a dynamic call and `lift` for a lifted constant:

```
(((fix p n -> (fun x -> (if (n == 0) then lift(1) else (x _* ((p (n - 1)) x))))) s) d)
```

The binders get $n : \mathrm{int}^S$, $x : \mathrm{int}^D$ and $p : (\mathrm{int}^S \to^S (\mathrm{int}^D \to^S \mathrm{int}^D))$. So `p` is a static function that the specializer unfolds, the test on `n` is done at specialization time, and only the multiplications on `x` stay. The residual programs:

| s | residual program | nodes | value at d = 2 |
|---|---|---|---|
| 0 | `1` | 1 | 1 |
| 1 | `(d * 1)` | 3 | 2 |
| 2 | `(d * (d * 1))` | 5 | 4 |
| 3 | `(d * (d * (d * 1)))` | 7 | 8 |

With the roles swapped (`s` dynamic, `d` static), `n` is dynamic, the `fix` rule makes `p` dynamic, and 31 of the 36 variables are $D$. Only the binder of `d`, its use and the three constants stay static:

```
(((_fix p n -> (_fun x -> (_if (n _== lift(0)) then lift(1) else (x _* ((p @ (n _- lift(1))) @ x))))) @ s) @ lift(d))
```

The residual program for `d = 2` is the original program with fresh names and `2` in place of `d`. Nothing is gained, and nothing loops.

**Let insertion.** With static `s` and dynamic `d`:

```
let t = fun f -> fun z -> f (f z) in t (fun y -> y + s) d
```

The analysis gives $t : ((\mathrm{int}^D \to^S \mathrm{int}^D) \to^S (\mathrm{int}^D \to^S \mathrm{int}^D))$: both `t` and the function passed to it are static, with dynamic arguments. For `s = 5` the residual program is `(let y1 = (d + 5) in (y1 + 5))`, which gives 11 at `d = 1`. The inner call `f z` gets the variable `d` and needs no `let`. The outer call gets the code `(d + 5)`, so the specializer binds it to a fresh `y1`. This keeps call by value: the argument is computed once, before the body, even if the body used `y` twice or not at all.

**A function result.** For `fun x -> x + s` with static `s`, the result is a function, so L6 makes the root $D$: `(_fun x -> (x _+ lift(s)))`. For `s = 2` the residual program is `(fun x1 -> (x1 + 2))`.

**A loop that does not stop.** With static `s` and dynamic `d`:

```
(fix f n -> if d < n then n else f (n + 1)) s
```

The annotation is `((fix f n -> (_if (d _< lift(n)) then lift(n) else (f (n + 1)))) s)`. The parameter `n` is static, so `f` is static and the specializer unfolds it. The test is dynamic, so the specializer builds both branches, and the else branch calls `f` again with `n + 1`. With `s = 0` the original program stops for every `d` (it gives 4 at `d = 3`), but the specializer unfolds forever. The implementation stops it after a budget of unfoldings (50 in the test).

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts.

1. **The result is the least congruent annotation.** Every congruence rule is an implication between two variables or a fact, and L3 to L6 add exactly these. The set reachable from the facts in L7 satisfies every implication, and any set that satisfies all of them and holds the facts contains it.
2. **No binding-time error.** For a congruent annotation, by induction on the run of the specializer: a node marked $S$ gives a value, a constant at base type and a closure at function type; a node marked $D$ gives code; and every variable is bound to a static value or to a variable or constant of code. So the specializer never needs the value of code, and never needs to turn a closure into code.
3. **The residual program is equivalent to the original.** Each step of the specializer replaces a part of the program by a part that is equal in Plotkin's call-by-value calculus: a static call becomes a `let`, a `let` of a value becomes a substitution, a static `if` on a constant takes its branch, and a static operator on constants gives a constant. These equalities are sound for operational equivalence, so when the specializer stops, the residual program gives the same result as the original on every dynamic input.

The tests check the three parts on 250 random typed programs (the analysis is congruent, and changing any single $D$ variable to $S$ breaks a rule), and they compare the residual program with the original on random inputs of 400 random programs.

## Complexity

The model is the word RAM. $N$ is the number of nodes of the term, and $T$ is the total size of the simple types of all nodes and binders, written as trees, so $T \ge N$. L1 makes $O(N)$ unification steps, and each occurs check walks a type of size at most $T$, so L1 takes $O(N T)$ time. L2 makes $T$ variables. L4 and L5 add $O(T)$ implications, because a flow at function type adds two per constructor and every other rule adds at most three. L7 visits each variable and each implication once, in $O(T)$ time. The total time is $O(N T)$ and the space is $\Theta(T)$.

$T$ is usually $O(N)$, but simple types written as trees can be exponential in $N$. A version that keeps types as shared graphs and unifies binding times with them, as Henglein did, runs in almost linear time in $N$.

## Properties

- **Monovariant.** Each function in the program gets one annotated type. If one call of a function passes a dynamic argument, every call of that function treats the argument as dynamic.
- **Least.** The result is the most static congruent annotation for this set of rules.
- **Offline.** The marks depend on which inputs are static, not on their values. One analysis serves every value of the static inputs.
- **Termination is not part of congruence.** A congruent annotation can still make the specializer run forever, as in the loop example.

## Variants and improvements

- **Polyvariant BTA.** Each function gets one annotated type for each pattern of binding times it is called with, and the specializer keeps one copy of the function per pattern. This avoids the loss shown in the Pitfalls.
- **Constraint-based BTA in almost linear time.** Henglein solves the binding-time constraints together with the types, with union-find on the type graph.
- **Online partial evaluation.** No BTA at all: the specializer looks at each value as it goes and decides then. It is more precise but slower, and it is hard to make it specialize itself (see [Futamura projections](/futamura-projections/)).
- **Termination analysis.** Static variables that can grow without bound under dynamic control, like `n` in the loop example, are made dynamic before specialization. This makes the specializer stop on more programs at the cost of less static work.
- **Partially static structures.** Pairs and lists whose shape is static but whose elements are dynamic get a richer annotated type than the plain $S$ or $D$ used here.

## When to use it

Use a BTA when the same program is specialized many times, or when the specializer itself must be specialized, as in the second and third Futamura projections: there the marks must be known before the static values are. Use it also when you want to see, before running anything, which parts of the program the specializer will remove. For one-off specialization with complex static data, an online specializer is often simpler and more precise.

## Pitfalls

- **Monovariance loses static work.** In `let g = fun y -> y * 2 in g s + g d` with static `s`, the call `g d` makes the parameter of `g` dynamic everywhere. For `s = 5` the residual program is `((5 * 2) + (d * 2))`. With two copies of the function, one per call, it is `(10 + (d * 2))`. A *binding-time improvement*, a rewrite of the source by hand, or a polyvariant BTA fixes this.
- **Specialization need not stop.** Congruence makes specialization safe, not finite. A static recursion under a dynamic test unfolds forever. Use a budget, or a termination analysis that makes such a variable dynamic.
- **Dropping the let insertion.** If a static call with a code argument puts the code in place of the parameter, the residual program can compute the argument many times or never. Under call by value, a program whose argument does not stop would then stop. Bind the argument with a residual `let`.
- **Lifting a function.** A static closure cannot be turned into code in this setting. That is why flow at function type is equality and why a function-typed result must be $D$.
- **Untypable programs.** This BTA needs simple types. An untyped program needs a different analysis, for example the one of Gomard and Jones for the untyped lambda calculus, where a value that cannot get a consistent annotated type is made dynamic.

## Implementations

## History

Binding-time analysis came with the first self-applicable partial evaluator, the mix project of Jones, Sestoft and Søndergaard in 1985. Its purpose was to take the decisions out of the specializer, so that specializing the specializer gave good compilers. Gomard and Jones extended it to the untyped lambda calculus in 1991 with a two-level language and a type-based analysis. In the same year Henglein gave an almost linear algorithm for higher-order BTA by constraint solving. The book of Jones, Gomard and Sestoft (1993) made BTA and congruence the standard way to present offline partial evaluation.

## References
