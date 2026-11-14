---
tag: M0C7VW
kind: theorem
slug: ssa-cps-correspondence
name: Correspondence of SSA and functional programs
aliases:
- SSA is functional programming
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: SSA blocks correspond to local functions and phi operands to arguments of jumps, so SSA is a restricted form of CPS or ANF.
prereqs: [static-single-assignment-form, continuation-passing-style, dominator-tree]
see_also: [a-normal-form, cps-conversion, phi-function, lambda-lifting, static-single-information-form, out-of-ssa-translation, lost-copy-and-swap-problems, tail-call-optimization]
sources:
  - paper: doi:10.1145/202530.202532
    title: Richard A. Kelsey, A correspondence between continuation passing style and static single assignment form, ACM SIGPLAN Workshop on Intermediate Representations (IR 1995), ACM SIGPLAN Notices 30(3), 1995, pages 13-22
    locator: the translations from SSA to CPS and from CPS with non-escaping local continuations to SSA
  - paper: doi:10.1145/278283.278285
    title: Andrew W. Appel, SSA is functional programming, ACM SIGPLAN Notices 33(4), 1998, pages 17-20
    locator: the reading of SSA blocks as nested functions, of phi-functions as parameters, and of dominance as lexical scope
  - paper: doi:10.1016/S1571-0661(05)82596-4
    title: Manuel M. T. Chakravarty, Gabriele Keller and Patryk Zadarnowski, A functional perspective on SSA optimisation algorithms, Compiler Optimization Meets Compiler Verification (COCV 2003), Electronic Notes in Theoretical Computer Science 82(2), pages 347-361
    locator: the formal translation of SSA programs into A-normal form, and sparse conditional constant propagation done on the translated programs
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the definition of SSA form, with phi-functions and the property that each definition dominates its uses
  - book: isbn:0521582741
    title: Andrew W. Appel, Modern Compiler Implementation in ML, Cambridge University Press, 1998
    locator: the chapter on static single-assignment form, the section on functional intermediate forms
  - paper: doi:10.1145/1291151.1291179
    title: Andrew Kennedy, Compiling with continuations, continued, Proceedings of the 12th ACM SIGPLAN International Conference on Functional Programming (ICFP 2007), pages 177-190
    locator: a CPS intermediate language with local continuations that are bound by a letcont form and compiled as jumps
---

A procedure in [static single assignment form](/static-single-assignment-form/) is a functional program in disguise. Each basic block is a local function, the [phi-functions](/phi-function/) at the start of a block are its parameters, and a jump to the block is a call that passes the phi operands of that edge as arguments. Nest each block function inside the block that immediately dominates it, and every variable is in lexical scope wherever SSA allows a use: dominance becomes scope. Every call of a block function is a tail call, and no block function escapes, so the result is a program in [continuation-passing style](/continuation-passing-style/) whose local continuations are only called, or a program in [A-normal form](/a-normal-form/). Kelsey (1995) gave the translations in both directions, and Appel (1998) stated the correspondence in the paper "SSA is functional programming".

## Statement

Let $P$ be a procedure with parameters $\vec p$ in strict SSA form: every name has one definition, and the definition of each name dominates each of its uses, where a phi operand for the edge $B \to C$ counts as a use at the end of $B$. Let $T$ be the [dominator tree](/dominator-tree/) of its control flow graph. Define, for each block $B$ with phi-functions $x_1 \leftarrow \phi(\dots), \dots, x_k \leftarrow \phi(\dots)$, instructions $I_1, \dots, I_m$ and children $C_1, \dots, C_r$ in $T$:

$$\mathrm{BLOCK}(B) = B(x_1, \dots, x_k) = I_1; \dots; I_m;\ \mathtt{letrec}\ \mathrm{BLOCK}(C_1)\ \mathtt{and} \dots \mathtt{and}\ \mathrm{BLOCK}(C_r)\ \mathtt{in}\ \mathrm{TERM}(B),$$

where each instruction $y \leftarrow e$ becomes $\mathtt{let}\ y = e\ \mathtt{in}$, and $\mathrm{TERM}(B)$ is $C(\vec a_{B \to C})$ for a jump to $C$, $\mathtt{if}\ v\ \mathtt{then}\ C(\vec a_{B \to C})\ \mathtt{else}\ C'(\vec a_{B \to C'})$ for a branch, and $k\ v$ for `return v`. Here $\vec a_{B \to C}$ lists the operands of the phi-functions of $C$ for the edge $B \to C$. The translation of $P$ is

$$\mathrm{FUN}(P) = \lambda \vec p.\,\lambda k.\ \mathtt{letrec}\ \mathrm{BLOCK}(\mathit{entry})\ \mathtt{in}\ \mathit{entry}().$$

**Theorem.** For every procedure $P$ in strict SSA form:

1. **Dominance is scope.** Every variable of $\mathrm{FUN}(P)$ other than $\vec p$ and $k$ is bound around each of its uses. A name defined in block $D$ is in scope in the body of $B$ exactly when $D$ dominates $B$; each block name $C$ is in scope at every jump to $C$.
2. **Blocks are local functions.** Every call of a block function is a tail call, and block functions occur only as the operator of such calls. So $\mathrm{FUN}(P)$ is a CPS term in which the continuation $k$ is the only continuation that is passed, and the block functions are local continuations. Replacing $k\ v$ by $v$ gives a term in A-normal form.
3. **Phi operands are call arguments.** On every input, $P$ and $\mathrm{FUN}(P)$ applied to the same arguments and to the continuation $\lambda v.\,v$ give the same result, or both run forever. The parallel assignment of the phi-functions of $C$ on the edge $B \to C$ is the binding of the arguments $\vec a_{B \to C}$ to the parameters of $C$.

The translation has size linear in the size of $P$ plus the number of phi operands.

**Example.** A loop that sums $0 + 1 + \dots + (n - 1)$, in SSA form and translated. The dominator tree has `entry` above `loop`, and `loop` above `body` and `exit`.

```
entry:  i0 = 0; s0 = 0; goto loop                  fun n k ->
loop:   i1 = φ(i0, i2); s1 = φ(s0, s2)               letrec entry () =
        c = i1 < n; if c goto body else exit           let i0 = 0 in let s0 = 0 in
body:   s2 = s1 + i1; i2 = i1 + 1; goto loop           letrec loop (i1, s1) =
exit:   return s1                                        let c = i1 < n in
                                                         letrec body () = let s2 = s1 + i1 in
                                                                          let i2 = i1 + 1 in loop (i2, s2)
                                                            and exit () = k s1
                                                         in if c then body () else exit ()
                                                       in loop (i0, s0)
                                                     in entry ()
```

The phi-functions of `loop` are its parameters. The jump from `entry` passes `(i0, s0)`, and the back edge from `body` passes `(i2, s2)`. The body of `body` reads `i1` and `s1` from the enclosing function `loop`, because `loop` dominates `body`.

## In plain words

Each block of the program becomes a small local function. Its phi-functions become its parameters. A jump to a block becomes a call of that function, and the values that the phi-functions would pick for that jump become the arguments. Each block function is written inside the function of the block that comes before it on every path, so it can read every name that SSA lets it read. No block function ever returns to the place that called it, so all of these calls are jumps. The result is an ordinary functional program that does the same thing.

## Proof

**Part 1, scope.** The variables bound around a point in the body of $B$ are: the parameters $\vec p$; the phi targets and instruction targets of every proper ancestor of $B$ in $T$, because $\mathrm{BLOCK}(B)$ is nested in the bodies of these blocks after their instructions; the phi targets of $B$; and the instruction targets of $B$ before the point. These are exactly the names whose definitions dominate the point, since a block $D$ dominates $B$ if and only if $D$ is an ancestor of $B$ in $T$. Strict SSA says that each use is dominated by its definition, so each use is in scope. For a phi operand $a$ on the edge $B \to C$, the use is at the end of $B$, where $\mathrm{TERM}(B)$ is, and the same argument applies. For a jump from $B$ to $C$: every dominator of $C$ other than $C$ dominates $B$, because a path to $B$ followed by the edge is a path to $C$. So $\mathrm{idom}(C)$ is $B$ or an ancestor of $B$, and the `letrec` of the children of $\mathrm{idom}(C)$, which binds $C$, encloses $\mathrm{TERM}(B)$. If $C$ dominates $B$ (a back edge), $C$ is bound by the `letrec` that encloses its own body, which also encloses $B$. In both cases the name $C$ is in scope at the jump.

**Part 2, tail calls.** A block function appears only in $\mathrm{TERM}(B)$, as the operator of a call that is the whole term or a whole branch of the final `if`. Both are tail positions, and nothing else uses the name. The term $k\ v$ is the only use of $k$, also in tail position. So the term meets the grammar of CPS terms with the block functions as continuations that are bound and called but never passed.

**Part 3, same results.** Use the operational semantics of SSA: a state is the current block $B$ and a map $\rho$ from names to values. Entering $C$ from $B$ first evaluates all operands $\vec a_{B \to C}$ in $\rho$ and then assigns them to the phi targets of $C$ at once; then the instructions run in order and update $\rho$; then the terminator picks the next block or returns. For the functional program use call-by-value evaluation with environments and closures. Each run of the body of a block $D$ creates new closures for the children of $D$ in $T$.

*Invariant.* When the SSA program enters block $B$, the functional program calls $B$, and the call uses a closure of $B$ whose chain of enclosing activations contains, for each proper ancestor $D$ of $B$ in $T$, the most recent run of the body of $D$.

The invariant holds at the start, where $\mathit{entry}$ is called with no enclosing block. Suppose it holds when the program enters $B$, and the program then goes to $C$. In the functional program, the body of $B$ runs and calls $C$. The name $C$ refers to the closure made by the most recent run of $\mathrm{idom}(C)$ that encloses the current activation, because $\mathrm{idom}(C)$ is $B$ or an ancestor of $B$ (Part 1). By the invariant for $B$, plus the run of $B$ that has just happened, that run is the most recent run of $\mathrm{idom}(C)$, and its chain gives the most recent runs of the ancestors of $\mathrm{idom}(C)$. So the invariant holds for $C$.

*Values agree.* Let $x$ be a name used in $B$ and defined in $D$, a dominator of $B$. In SSA, $\rho(x)$ is the value from the most recent run of $D$, since $x$ has no other definition. In the functional program, the use of $x$ refers to the binding in the activation of $D$ on the closure chain, which is the most recent run of $D$ by the invariant, or to the current run if $D = B$. So the two values are equal. This needs that no other block assigns $x$ in between, which single assignment gives, and that a run of $D$ after the closure was made would have created a new closure: if control leaves the blocks dominated by $D$ and comes back to $B$, it must pass $D$ again, since otherwise a path from the entry to $B$ would avoid $D$.

*Phi-functions.* A call $C(\vec a_{B \to C})$ evaluates all arguments in the environment of $B$, where they have the values $\rho(\vec a_{B \to C})$, and only then binds them to the parameters. That is the parallel assignment of the phi-functions. Instructions are `let`s in the same order and compute the same values, a branch tests the same value, and `return v` calls $k = \lambda v.\,v$ with $\rho(v)$. So the sequences of blocks visited are the same, both programs return the same value, and if one runs forever so does the other.

The size bound holds because each block, instruction and phi operand gives one binding, one `let` or one argument. $\square$

## Consequences

- **Optimizations transfer.** An SSA optimization is a transformation of the functional program, and the other way round. Chakravarty, Keller and Zadarnowski (2003) do sparse conditional constant propagation on the A-normal form translation. Copy propagation in SSA is substitution of a variable for a variable, which is always safe because names are not reassigned.
- **Compiling CPS to machine code.** Block functions are known, never escape and are only called in tail position. A compiler can give them no closures, keep their free variables in registers, and compile each call as a move of arguments followed by a jump. That is what CPS compilers do with local continuations, as Kennedy (2007) describes.
- **The converse.** Kelsey (1995) also translates CPS programs to SSA: if the local continuations of a CPS program are only bound and called, never passed as arguments, each of them becomes a block, and its parameters become phi-functions.
- **Out of SSA as argument passing.** A call binds its arguments to its parameters at once, so the [lost-copy and swap problems](/lost-copy-and-swap-problems/) of [out-of-SSA translation](/out-of-ssa-translation/) do not arise in the functional reading. They come back when the parallel binding is turned into a sequence of moves.
- **Lambda lifting gives the flat form.** Applying [lambda lifting](/lambda-lifting/) to $\mathrm{FUN}(P)$ moves every block to the top level and passes its free variables as extra parameters. The result is a program in which every live variable is passed at every jump, a form with many more phi-functions than minimal SSA.

## Tightness

- **Strictness is needed.** If a use is not dominated by its definition, as in non-strict SSA where a variable may be undefined on some path, the use lies outside the scope of its binding in $\mathrm{FUN}(P)$. The functional program then has a free variable.
- **Nesting by dominance is needed.** With all block functions in one flat `letrec` at the top, blocks could not read the names of other blocks. Then every name used outside its block must be passed explicitly, which is what lambda lifting does.
- **CPS is strictly more general.** A CPS program can pass a continuation as an argument, store it, or call it from a deeper procedure, as with exceptions or `call/cc`. Such a program has no SSA form within one procedure: the correspondence covers exactly the CPS programs whose local continuations do not escape.
- **Phi-functions only at block entry.** The translation uses the fact that phi-functions sit at the start of blocks and read their operands at the end of predecessors. Forms that also split at branches, such as [SSI form](/static-single-information-form/), translate the same way, with the split names as parameters of the successor blocks.

## History

Kelsey (1995) presented the correspondence at the ACM SIGPLAN workshop on intermediate representations, with translations in both directions between SSA and CPS with local continuations. Appel (1998) made the same point for a wider audience in "SSA is functional programming", with blocks as nested functions and dominance as scope, and described functional intermediate forms in his compiler textbook of the same year. Chakravarty, Keller and Zadarnowski (2003) formalized the translation into A-normal form and carried an SSA optimization over to it. Kennedy (2007) argued for a CPS intermediate language with local continuations that are compiled as jumps.

## References
