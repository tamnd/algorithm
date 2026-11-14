---
tag: J9VE11
kind: algorithm
slug: cps-conversion
name: CPS conversion
aliases:
- CPS transformation
- Plotkin CPS translation
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Translates a direct-style program into continuation-passing style, in one pass without administrative redexes by the Danvy-Filinski method.
model: word-ram
complexity:
  vars: {n: the number of nodes of the source term}
  time: {worst: O(n), best: Θ(n)}
  space: {output: O(n), extra: O(n)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [lambda-calculus, beta-reduction, continuation-passing-style]
see_also: [a-normal-form, ssa-cps-correspondence, closure-conversion, lambda-lifting, defunctionalization, tail-call-optimization, partial-evaluation, static-single-assignment-form]
sources:
  - paper: doi:10.1016/0304-3975(75)90017-1
    title: Gordon D. Plotkin, Call-by-name, call-by-value and the λ-calculus, Theoretical Computer Science 1(2), 1975, pages 125-159
    locator: the call-by-value and call-by-name CPS translations, the colon translation, and the simulation and indifference theorems
  - paper: doi:10.1145/942580.807077
    title: Michael J. Fischer, Lambda calculus schemata, Proceedings of the ACM Conference on Proving Assertions about Programs, 1972, pages 104-109
    locator: the translation of lambda terms into a form where every function takes its continuation as an extra argument
  - paper: doi:10.1017/S0960129500001535
    title: Olivier Danvy and Andrzej Filinski, Representing control, a study of the CPS transformation, Mathematical Structures in Computer Science 2(4), 1992, pages 361-391
    locator: the one-pass call-by-value CPS transformation with static (translation-time) continuations, the treatment of tail calls without η-redexes, and the proof that its output has no administrative redexes
  - paper: doi:10.1145/91556.91622
    title: Olivier Danvy and Andrzej Filinski, Abstracting control, Proceedings of the 1990 ACM Conference on LISP and Functional Programming, pages 151-160
    locator: the first presentation of the one-pass CPS transformation, used there for the control operators shift and reset
  - paper: doi:10.1017/S0956796807006387
    title: Olivier Danvy, Kevin Millikin and Lasse R. Nielsen, On one-pass CPS transformations, Journal of Functional Programming 17(6), 2007, pages 793-812
    locator: the comparison of the compositional higher-order one-pass transformation with the non-compositional one of Sabry and Felleisen
  - book: isbn:0521416957
    title: Andrew W. Appel, Compiling with Continuations, Cambridge University Press, 1992
    locator: the chapter on CPS conversion of the ML compiler, which builds the output with continuations of the translator
  - paper: doi:10.1145/800194.805852
    title: John C. Reynolds, Definitional interpreters for higher-order programming languages, Proceedings of the ACM Annual Conference, 1972, pages 717-740
    locator: the use of continuations to make an interpreter independent of the evaluation order of the language it is written in
  - paper: doi:10.1007/BF01019462
    title: Amr Sabry and Matthias Felleisen, Reasoning about programs in continuation-passing style, LISP and Symbolic Computation 6(3-4), 1993, pages 289-360
    locator: the equational correspondence between a source calculus and its CPS image, and the one-pass transformation without administrative redexes
---

CPS conversion rewrites a program into [continuation-passing style](/continuation-passing-style/): every function gets one more argument, its continuation, and calls it with its result instead of returning. In the output every call is a [tail call](/tail-call-optimization/), the order of evaluation is written into the code, and every intermediate value has a name. Plotkin (1975) gave the translation rule by rule and proved it correct, but his rules leave many *administrative redexes*: calls of small functions that the translation itself made and that only pass values along. Danvy and Filinski (1990, 1992) moved those calls into the translator. Their one-pass translation keeps the continuation of the term it is translating as a function of the translator, so the output has no administrative redex and no extra η-redex at tail calls. It runs in linear time and its output has linear size.

## In plain words

A normal program says: compute this, then give the result back to whoever asked. In continuation-passing style no function gives a result back. Each function gets one more argument, the continuation, which says what to do with the result, and the function calls it at the end. CPS conversion rewrites a program into that form. The simple rewrite, rule by rule, makes many tiny helper functions that only pass a value along. The one-pass method keeps those helpers inside the translator. They run while the program is translated and never appear in the output, so the output is about as small as the input.

## The problem

The input is a closed term of a call-by-value [lambda calculus](/lambda-calculus/) with integer and boolean constants, `fun x -> e`, calls `e1 e2`, `let x = e1 in e2`, `if`, the operators `+ - * < ==` and recursive functions `fix f x -> e`, which evaluates from left to right. A term is *trivial* if it is a variable, a constant or a function. The output is a term of the same language with these properties:

1. It has the same outcome: the same integer or boolean result, a function if the source gives a function, a stuck term if the source gets stuck, and no result if the source loops.
2. Every call is a tail call whose operator and arguments are trivial: the call `f v k` is the last thing that its function body does.
3. A source function `fun x -> e` becomes `fun x -> fun k -> e'`, a function that takes its argument and then its continuation.

Plotkin's call-by-value translation $[\![e]\!]$ maps each term to a function of a continuation $k$:

$$[\![x]\!] = \mathtt{fun}\ k \to k\ x \qquad [\![\mathtt{fun}\ x \to e]\!] = \mathtt{fun}\ k \to k\ (\mathtt{fun}\ x \to [\![e]\!])$$

$$[\![e_1\ e_2]\!] = \mathtt{fun}\ k \to [\![e_1]\!]\ (\mathtt{fun}\ a \to [\![e_2]\!]\ (\mathtt{fun}\ b \to a\ b\ k))$$

The program is $[\![e]\!]\ (\mathtt{fun}\ a \to a)$. Constants follow the rule for variables, and `let`, `if` and the operators get rules of the same shape. The rules are correct, but each of them makes new redexes such as $(\mathtt{fun}\ k \to k\ x)\ (\mathtt{fun}\ a \to \dots)$. For the term `(f x) (g y)`, the result has 6 of these redexes and 46 nodes, and it reduces at run time to `f x (fun a -> g y (fun b -> a b k))`. The goal is to give that reduced term at once, in one pass.

## The algorithm

The translator has two kinds of functions. A word in `fun` is code of the output. A λ is a function of the translator, a *meta-continuation*, which runs now: it takes a trivial output term, the name or value of a result, and returns the output code that uses that result. TAIL translates a term whose continuation is an output variable $k$. META translates a term whose continuation is a meta-continuation $\kappa$.

```pseudo id=main
CPS(e)                                    ▷ e is closed; the result returns the value of e
L1  rename every bound variable of e to a new name
L2  k0, a ← new names
L3  return let k0 = (fun a -> a) in TAIL(e, k0)

VAL(v)                                    ▷ v is trivial: a variable, a constant or a function
L4  if v is a variable or a constant then return v
L5  if v is fun x -> b then return fun x -> fun k -> TAIL(b, k)              ▷ k new
L6  if v is fix f x -> b then return fix f x -> fun k -> TAIL(b, k)          ▷ k new

TAIL(e, k)                                ▷ k is an output variable that receives the value of e
L7  if e is trivial then return k VAL(e)
L8  if e is e1 e2 then return META(e1, λa. META(e2, λb. a b k))
L9  if e is let x = e1 in e2 then return META(e1, λa. let x = a in TAIL(e2, k))
L10 if e is if e1 then e2 else e3 then return META(e1, λa. if a then TAIL(e2, k) else TAIL(e3, k))
L11 if e is e1 op e2 then return META(e, λa. k a)

META(e, κ)                                ▷ κ maps a trivial output term to output code
L12 if e is trivial then return κ(VAL(e))
L13 if e is e1 e2 then return META(e1, λa. META(e2, λb. a b (fun t -> κ(t))))                  ▷ t new
L14 if e is let x = e1 in e2 then return META(e1, λa. let x = a in META(e2, κ))
L15 if e is if e1 then e2 else e3 then return META(e1, λa. let j = (fun t -> κ(t)) in if a then TAIL(e2, j) else TAIL(e3, j))   ▷ j, t new
L16 if e is e1 op e2 then return META(e1, λa. META(e2, λb. let t = a op b in κ(t)))            ▷ t new
```

Line L1 makes every binder unique. This matters because META puts the code of $\kappa$ under binders that come from the term it translates, for example under `let x = a` at line L14. Line L13 is the only place where a meta-continuation turns into output code: a call that is not in tail position needs a real continuation, so $\kappa$ is applied once to a new variable $t$ and wrapped in `fun t -> ...`. Line L8 gives the same call in tail position, and there the continuation is the variable $k$ itself, with no `fun t -> k t` around it. Line L15 binds the continuation of an `if` to a join point $j$ before the branch, so that $\kappa$ is used once and not copied into both branches.

## Example

Take `let f = fun x -> x + 1 in f (f 2)`, with 10 nodes. Line L1 renames `x` to `x1` and `f` to `f2`, and line L3 calls TAIL with `k3`. Line L9 gives `let f2 = VAL(fun x1 -> x1 + 1) in ...`, and line L5 translates the body `x1 + 1` with a new continuation `k5`. For the body `f2 (f2 2)` line L8 asks META for `f2`, which at line L12 hands `f2` to its λ at once. That λ asks META for `f2 2`, a call in a non-tail position, so line L13 makes `t7` and builds the call `f2 2 (fun t7 -> ...)`, whose body is the code for the outer call in tail position. The result has 23 nodes:

```
let k3 = fun a4 -> a4 in
let f2 = fun x1 -> fun k5 -> let t6 = x1 + 1 in k5 t6 in
f2 2 (fun t7 -> f2 t7 k3)
```

| step | term being run |
|---|---|
| 1 | `f2 2 (fun t7 -> f2 t7 k3)` after the two `let`s |
| 2 | `let t6 = 2 + 1 in (fun t7 -> f2 t7 k3) t6` |
| 3 | `(fun t7 -> f2 t7 k3) 3` |
| 4 | `f2 3 k3` |
| 5 | `let t6 = 3 + 1 in k3 t6`, then `k3 4`, then `4` |

Every call is the last thing done, so a machine that runs this needs no return stack. Plotkin's rules give 66 nodes for the same term, with 9 administrative redexes in the output and more that appear while they are reduced. Applied to a continuation variable `k` and with all of these redexes reduced, Plotkin's term for the source becomes `let f2 = (fun x1 -> fun k15 -> let t18 = x1 + 1 in k15 t18) in f2 2 (fun v7 -> f2 v7 k)`, which is TAIL(e, k) up to the names of bound variables.

## Correctness

Plotkin proved that his translation simulates call-by-value evaluation: for a closed term $e$, $[\![e]\!]\ (\mathtt{fun}\ a \to a)$ has the same outcome as $e$, where a function result maps to its image. His proof uses the *colon translation* $e : K$, which is $[\![e]\!]\ K$ with the administrative steps at the head already done. One source step from $e$ to $e'$ takes $e : K$ to $e' : K$ in one or more steps, and the image of a value $v$ is $K$ applied to the image of $v$. The one-pass translation computes the same term with every administrative redex reduced, also the ones under `fun`: by induction on $e$, the output of TAIL$(e, k)$ is the administrative normal form of $[\![e]\!]\ k$, and META$(e, \kappa)$ is the normal form of $[\![e]\!]\ (\mathtt{fun}\ t \to \kappa(t))$. The join point of line L15 is one more redex `let j = ...` whose right side is a value. Every redex that is removed in this way has a value as its argument, so it is a $\beta_v$ step, and Plotkin showed that $\beta_v$ steps keep the outcome of call-by-value programs. Every call in the output is a tail call, because each line places a call at a position where the code of its continuation would go, and the λ functions put only `let`, `if` and calls there. The [proof file](proofs/correctness.md) gives these arguments in detail.

## Complexity

The model is the word RAM. Names are small integers, so the renaming table of line L1 is an array, and the unit step is one table access or the creation of one node of the output. Each node of the source is handled by one call of TAIL or META, which does a constant amount of work besides its recursive calls. Each meta-continuation is called exactly once: at line L12, or inside the code it builds at lines L13, L15 and L16. So the time and the size of the output are $O(n)$. For the terms of the tests the output has at most $6n + 4$ nodes. The recursion is as deep as the term, and the meta-continuations that wait form a chain of the same length, so the extra space is $O(n)$. A two-pass method, Plotkin's rules followed by administrative reduction, first builds a term several times larger: 66 nodes against 23 in the example.

## Properties

- **No administrative redexes.** Every call in the output has a variable as its operator, or the image of a source function at a place where the source has the same call.
- **Properly tail recursive.** A call in tail position passes its own continuation $k$ on, so a loop written with tail calls runs in constant control space.
- **Linear size.** No meta-continuation is used twice, so no code is copied.
- **Compositional.** The output for a term is built from the outputs for its parts, which makes proofs by induction simple.
- **Deterministic.** The result depends only on the input, up to the choice of new names.

## Variants and improvements

- **Call by name.** Plotkin's call-by-name translation maps a variable to itself, since a variable then stands for a computation, and a call $e_1\ e_2$ to $\mathtt{fun}\ k \to [\![e_1]\!]\ (\mathtt{fun}\ f \to f\ [\![e_2]\!]\ k)$. Its output runs the same under both evaluation orders, which Plotkin called indifference.
- **Continuation first.** Fischer (1972) put the continuation as the first parameter of each function. The two orders give the same results.
- **First-class continuations.** Once a program is in CPS, `call/cc` is an ordinary function that passes its own continuation $k$, wrapped as `fun v -> fun k' -> k v`, to its argument. The `shift` and `reset` operators of Danvy and Filinski (1990) are defined in the same way.
- **Several continuations.** Passing one continuation for normal returns and one for exceptions gives exceptions without special support in the back end.
- **Non-compositional one-pass.** Sabry and Felleisen (1993) give a one-pass translation that is not compositional and is based on a syntactic theory of the source calculus. Danvy, Millikin and Nielsen (2007) relate the two methods.
- **[A-normal form](/a-normal-form/).** If the continuations are not passed but left implicit, the translation gives A-normal form instead, which names every intermediate value in the same way.

## When to use it

Use CPS conversion in a compiler for a functional language, especially one with first-class continuations, exceptions or coroutines, or one that must not grow the stack for tail calls. Steele's Rabbit compiler for Scheme and Appel's compiler for Standard ML of New Jersey both work on a CPS intermediate language. CPS also helps with [partial evaluation](/partial-evaluation/) and makes control flow explicit for analyses. Compilers that need no control operators often use A-normal form or [SSA form](/static-single-assignment-form/) instead, which have the same structure without the extra function arguments, see [the SSA and CPS correspondence](/ssa-cps-correspondence/). For a small interpreter, CPS conversion of the interpreter itself, and not of the program, removes the dependence on the host stack.

## Pitfalls

- **Call by value and call by name differ.** Plotkin gives two translations. The call-by-value one forces the argument before the call, so `(fun y -> 1) loop` loops after the translation, as it does in the source. Using the call-by-name translation for a strict language, or the other way around, changes which programs terminate.
- **Name capture.** META places code from outer parts of the term under binders of inner parts. Without line L1, a source `let x = ...` inside an argument can capture an outer `x` in that code.
- **Copying the continuation.** Applying $\kappa$ in both branches of an `if` copies its code, and nested `if`s then make the output exponential. The join point of line L15 avoids this.
- **η-redexes at tail calls.** A one-pass translation with only META wraps the continuation of a tail call as `fun t -> k t`. Each such call then wraps the continuation once more, so a loop of tail calls builds a chain of continuations and no longer runs in constant space. TAIL passes $k$ itself.
- **Evaluation order.** The order of the META calls fixes the order in which the arguments are evaluated. Line L8 evaluates the function before the argument. A different order changes the effects of the program.
- **New names.** The new names of the translation must not clash with the names of the source, or a continuation may capture a user variable.

## Implementations

## History

Continuations appeared in several places in the 1960s. Reynolds (1972) used them to write an interpreter whose meaning does not depend on the evaluation order of its host language, and Fischer (1972) used a translation of lambda terms into CPS in his study of lambda calculus schemata. Plotkin (1975) gave the call-by-value and call-by-name translations, proved them correct by simulation and introduced the colon translation for the proof. Steele built the first compiler that uses CPS as its intermediate language, Rabbit for Scheme, in 1978. Appel's book of 1992 describes the CPS compiler of Standard ML of New Jersey, whose conversion builds the output with continuations of the translator. Danvy and Filinski presented the one-pass translation in 1990 and studied it in full in 1992, with a proof that its output has no administrative redexes. Danvy, Millikin and Nielsen (2007) note that the compositional higher-order method was found independently by Appel, by Danvy and Filinski, and by Wand.

## References
