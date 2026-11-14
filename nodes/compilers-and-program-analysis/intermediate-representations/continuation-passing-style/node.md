---
tag: 6QSA2M
kind: definition
slug: continuation-passing-style
name: Continuation-passing style
aliases:
- CPS
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: A form where no function returns, and each call passes a continuation that receives the result, so control flow is explicit.
prereqs: [lambda-calculus, beta-reduction]
see_also: [cps-conversion, a-normal-form, ssa-cps-correspondence, tail-call-optimization, closure-conversion, defunctionalization, activation-record, static-single-assignment-form]
sources:
  - paper: doi:10.1016/0304-3975(75)90017-1
    title: Gordon D. Plotkin, Call-by-name, call-by-value and the λ-calculus, Theoretical Computer Science 1(2), 1975, pages 125-159
    locator: the CPS translations, and the indifference and simulation theorems for terms in continuation-passing style
  - paper: doi:10.1145/800194.805852
    title: John C. Reynolds, Definitional interpreters for higher-order programming languages, Proceedings of the ACM Annual Conference, 1972, pages 717-740
    locator: an interpreter in continuation-passing style, whose meaning does not depend on the evaluation order of the language it is written in, and the defunctionalized form of its continuations
  - paper: doi:10.1007/BF01019459
    title: John C. Reynolds, The discoveries of continuations, LISP and Symbolic Computation 6(3-4), 1993, pages 233-247
    locator: the account of the independent discoveries of continuations
  - url: "https://dspace.mit.edu/handle/1721.1/6913"
    title: Guy L. Steele Jr., RABBIT, a compiler for SCHEME, MIT Artificial Intelligence Laboratory Technical Report AITR-474, 1978
    locator: the compiler whose intermediate language is a subset of Scheme in continuation-passing style, with procedure calls compiled as jumps
  - book: isbn:0521416957
    title: Andrew W. Appel, Compiling with Continuations, Cambridge University Press, 1992
    locator: the CPS intermediate language of the Standard ML of New Jersey compiler and the optimizations done on it
  - paper: doi:10.1017/S0960129500001535
    title: Olivier Danvy and Andrzej Filinski, Representing control, a study of the CPS transformation, Mathematical Structures in Computer Science 2(4), 1992, pages 361-391
    locator: the grammar of CPS terms that are images of direct-style terms, and the stack discipline of their continuations
---

A term is in continuation-passing style (CPS) when no function returns a result to its caller. Each function takes one more argument, its *continuation*, a function that stands for the rest of the computation, and the function ends by calling the continuation with its result. So every call is a [tail call](/tail-call-optimization/), every intermediate result has a name, and the order of evaluation is written into the term. Reynolds (1972) used this style to make an interpreter independent of the evaluation order of the language it is written in. Plotkin (1975) proved that a CPS term gives the same result under call-by-name and call-by-value evaluation. Steele (1978) made CPS the intermediate language of the Rabbit compiler for Scheme, and Appel (1992) did the same for Standard ML of New Jersey. [CPS conversion](/cps-conversion/) translates a direct-style program into this form.

## Definition

Take a [lambda calculus](/lambda-calculus/) with constants and primitive operators. Variables come in two kinds: value variables $x, y, \dots$ and continuation variables $k, \dots$. A term in **continuation-passing style** is a *serious term* $S$ of the following grammar:

$$
\begin{aligned}
W &::= c \mid x \mid \lambda x.\lambda k.\,S && \text{(trivial terms: values)}\\
K &::= k \mid \lambda x.\,S && \text{(continuations)}\\
S &::= W_1\,W_2\,K \mid K\,W \mid \mathtt{let}\ x = W_1 \oplus W_2\ \mathtt{in}\ S \mid \mathtt{if}\ W\ \mathtt{then}\ S_1\ \mathtt{else}\ S_2 && \text{(serious terms)}
\end{aligned}
$$

A **CPS program** is $\lambda k.\,S$, and it is run by applying it to a top-level continuation, for example $\lambda x.\,x$ with a rule that stops there.

The grammar gives the three marks of the style:

1. **Every call is a tail call.** A call $W_1\,W_2\,K$ or $K\,W$ appears only as a whole serious term, never as an argument or as the right side of a `let`. So once a call starts, the caller has nothing left to do.
2. **Every operand is trivial.** Operators, arguments and conditions are constants, variables or functions. No operand needs evaluation before the call.
3. **Control is a value.** What happens after a call is the term $K$, passed as an argument. A function returns by calling $k$, and it can also ignore $k$, keep it, or call it twice.

Two facts follow. First, a serious term has its redex at the root: the next step is always the whole term, a call, a `let` of an operator on two trivial terms, or an `if` on a trivial term. A machine that runs a CPS term needs no control stack. Each call is a jump with arguments, and what a direct-style compiler keeps in [stack frames](/activation-record/) lives in the continuation closures. Second, every argument is a value, so a $\beta$-redex is also a $\beta_v$-redex. This is Plotkin's *indifference* theorem: call-by-name and call-by-value evaluation of a CPS program give the same result.

The terms that CPS conversion makes from direct-style terms form a smaller class. In them each function has one continuation parameter, and continuation variables obey a stack discipline: a continuation is used once on each path, and $\lambda x.\,S$ continuations are built only to extend the current one. Danvy and Filinski (1992) give a grammar for this class. A term outside it can express jumps that direct style cannot, such as an exception that skips several callers, or `call/cc`.

## Examples and non-examples

**Factorial.** In direct style, `fact n = if n < 1 then 1 else n * fact (n - 1)`. In CPS,

```
fact n k = if n < 1 then k 1
           else let m = n - 1 in fact m (fun r -> let t = n * r in k t)
```

The recursive call is now a tail call. The work left after it, multiply by `n` and pass on, moved into a new continuation. A call `fact 3 k0` builds three nested continuations before it reaches `k 1`, one for each frame that the direct-style program keeps on its stack.

**A tail call keeps its continuation.** `f x = g (x + 1)` becomes `f x k = let t = x + 1 in g t k`. The call of `g` receives `k` itself, so no new continuation is built and no stack grows. That is why tail calls run in constant space in a CPS compiler.

**Order of evaluation.** `h (f a) (g b)` becomes `f a (fun u -> g b (fun v -> h u v k))`. The term says that `f a` runs before `g b`. The other order is a different CPS term.

**First-class control.** `call/cc` is an ordinary function in CPS: `callcc f k = f (fun v k2 -> k v) k`. The function `fun v k2 -> k v` ignores its own continuation `k2` and jumps to `k`.

**Non-examples.**

- `fun x -> x + 1` is in direct style: it returns its result.
- `k (f x k)` is not in CPS: the call `f x k` is an argument, so it is not a tail call.
- `f (g x) k` is not in CPS: the argument `g x` is serious.
- `let y = f x k in k y` is not in CPS: a call is the right side of a `let`, which makes it a call that returns. That term is in [A-normal form](/a-normal-form/) with an extra argument.
- A JavaScript program that passes callbacks to some functions and returns values from others is partly in CPS. The definition asks that every call be a tail call.

## Related definitions

- **[CPS conversion](/cps-conversion/)** translates a direct-style term into CPS. Plotkin's rules leave administrative redexes; the one-pass method of Danvy and Filinski does not.
- **[A-normal form](/a-normal-form/)** keeps the naming of intermediate results and the fixed order of CPS, but in direct style. Flanagan, Sabry, Duba and Felleisen (1993) showed that it is what CPS conversion followed by simplification and the inverse translation gives.
- **[Static single assignment form](/static-single-assignment-form/)** is CPS restricted to local continuations that never escape: basic blocks are continuations and jumps are calls. The [correspondence of SSA and functional programs](/ssa-cps-correspondence/) states this.
- **[Closure conversion](/closure-conversion/)** after CPS turns continuations into heap records, which take the place of stack frames.
- **[Defunctionalization](/defunctionalization/)** of the continuations of a CPS program gives one data constructor per kind of continuation. For an interpreter, the result is the control stack of an abstract machine.
- **[Tail-call optimization](/tail-call-optimization/)** is what makes CPS run in bounded stack space: every call in a CPS program is a tail call.

## References
