---
tag: D7W565
kind: algorithm
slug: interprocedural-constant-propagation
name: Interprocedural constant propagation
aliases:
- jump function constant propagation
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Finds parameters that are constant on every call by propagating jump functions over the call graph.
solves: [constant-propagation-problem]
model: word-ram
complexity:
  vars: {n: the total size of all procedures (instructions and terminators and call arguments), b: the total number of blocks, v: the largest number of names in one procedure, k: the largest number of formals of one procedure}
  time: {worst: O((v + 1)(n + b v) + (k + 1) n)}
  space: {extra: O(n + b v)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [constant-propagation-problem, call-graph, interprocedural-dataflow-analysis]
see_also: [sparse-conditional-constant-propagation, function-inlining, functional-approach-interprocedural, ide-framework, context-sensitivity, call-graph-construction, constant-folding, partial-evaluation]
sources:
  - paper: doi:10.1145/12276.13327
    title: "David Callahan, Keith D. Cooper, Ken Kennedy and Linda Torczon, Interprocedural constant propagation, Proceedings of the 1986 SIGPLAN Symposium on Compiler Construction (SIGPLAN Notices 21(7)), 152-161"
    locator: the whole paper (jump functions for the arguments of each call site, return jump functions, and propagation of constants over the call graph)
  - paper: doi:10.1145/155090.155099
    title: "Dan Grove and Linda Torczon, Interprocedural constant propagation: a study of jump function implementation, Proceedings of the ACM SIGPLAN 1993 Conference on Programming Language Design and Implementation (PLDI 1993), 90-99"
    locator: the whole paper (literal constant, intraprocedural constant, pass-through and polynomial jump functions, compared on real programs)
  - book: isbn:9780128154120
    title: "Keith D. Cooper and Linda Torczon, Engineering a Compiler, 3rd edition, Morgan Kaufmann, 2022"
    locator: Section 9.4.2 (Interprocedural Constant Propagation)
  - url: "https://llvm.org/docs/Passes.html"
    title: LLVM Project, LLVM's Analysis and Transform Passes, LLVM documentation
    locator: the entry for -ipsccp (interprocedural sparse conditional constant propagation)
---

Interprocedural constant propagation finds the formal parameters of each procedure that receive the same constant on every call, in every run of the program. It looks at each procedure once and describes each argument of each call site by a *jump function*: the argument is a known constant, or it passes on the value of one of the caller's own formals unchanged, or it is unknown. Then it propagates values over the [call graph](/call-graph/) with a worklist, the way an intraprocedural [constant propagation](/constant-propagation-problem/) moves values over a flow graph. A formal that is the constant $c$ on every call gets `p = c` at the entry of its procedure, and local passes fold the rest. The method is due to Callahan, Cooper, Kennedy and Torczon.

## In plain words

A function often gets the same value for a parameter at every place where it is called, such as a buffer size of 4096. Inside the function, the compiler cannot know this, because it sees only the parameter.

This algorithm looks at every call in the program. For each argument it notes one of three things: it is a fixed number, it just passes on a parameter of the caller, or it is unknown. Then it starts at the main function and follows the calls. If all calls of a function pass 4096 for a parameter, that parameter is 4096. If a function passes its own parameter on to another function, the value travels along.

When two calls disagree, the parameter is unknown. At the end, every parameter that is still a single number is fixed in the code, so tests on it can be folded away.

## The problem

The input is a whole program: a set of procedures in the toy IR, with one procedure $\mathit{main}$ where every run starts. A procedure has formals and uses `const`, `copy`, `op` and `call` instructions, so a callee cannot change the variables of its caller. The inputs of $\mathit{main}$ are unknown.

The output is a value $\mathrm{VAL}[f, p]$ for each formal $p$ of each procedure $f$, in the lattice $\top$ (no call seen), $\mathrm{Const}(c)$, and $\bot$ (not known to be constant), and a transformed program. The result must be *sound*: if $\mathrm{VAL}[f, p] = \mathrm{Const}(c)$, then every activation of $f$ in every run starts with $p = c$. Recursion is allowed.

## The algorithm

Line L1 runs a forward [constant analysis](/constant-propagation-problem/) inside each procedure $f$. Each formal $q$ starts as the symbol $q$, meaning "the value of $q$ when $f$ was entered", and every other name starts as $\bot$. An operation on two constants is folded, and any other operation, as well as the result of a call, gives $\bot$. The local value of the $i$-th argument at a call site $s$ is its jump function $J(s, i)$: a constant $k$, a symbol $q$, or $\bot$. A jump function is evaluated in the values of the caller: $k$ gives $\mathrm{Const}(k)$, $q$ gives $\mathrm{VAL}[f, q]$, and $\bot$ gives $\bot$. The meet $\sqcap$ keeps two equal values, turns two different ones into $\bot$, and has $\top$ as its identity.

```pseudo id=main
IPCP(procedures, main)
L1  for each procedure f: analyze f locally and record the jump function J(s, i) of each argument i of each call site s in a block it reaches
L2  for each procedure f and each formal p of f: VAL[f, p] <- ⊤
L3  for each formal p of main: VAL[main, p] <- ⊥
L4  REACHED <- {main}; W <- [main]
L5  while W is not empty
L6      f <- take the first procedure out of W
L7      for each recorded call site s in f, with callee g
L8          if g is not in REACHED then add g to REACHED and to W
L9          for each argument position i, with p the i-th formal of g
L10             v <- J(s, i) evaluated in VAL[f, ·]
L11             if VAL[g, p] ⊓ v ≠ VAL[g, p] then VAL[g, p] <- VAL[g, p] ⊓ v and add g to W if it is not there
L12 for each procedure f and each formal p with VAL[f, p] = Const(c): insert p = c in a new entry block of f
L13 return VAL and the new procedures
```

The jump functions do not depend on VAL, so line L1 runs once per procedure. The worklist then touches only the call sites. A procedure goes back into $W$ only when one of its own values drops, because only then can the values it sends to its callees change.

## Example

The program has four procedures, written one after another. The formals of `main` are `n`, of `scale` are `x, k`, of `mul` are `u, v`, and of `count` are `i, lim`.

```
main:                         scale:
B0:                           B0:
  w = 4                         t = call mul(x, k)
  a = call scale(n, w)          ret t
  b = call scale(a, 4)
  c = call count(0, 5)        mul:
  d = b + c                   B0:
  ret d                         t = u * v
                                ret t
count:
B0:
  c = i < lim
  br c B1 B2
B1:
  j = i + 1
  r = call count(j, lim)
  ret r
B2:
  ret i
```

Line L1 gives these jump functions.

| call site | first argument | second argument |
|---|---|---|
| `scale(n, w)` in `main` | `n` | 4 |
| `scale(a, 4)` in `main` | ⊥ | 4 |
| `count(0, 5)` in `main` | 0 | 5 |
| `mul(x, k)` in `scale` | `x` | `k` |
| `count(j, lim)` in `count` | ⊥ | `lim` |

The second argument of the first call is the constant 4 because the local analysis knows `w = 4`. `a` is the result of a call, so it is ⊥. `j = i + 1` is not a plain pass-through, so it is ⊥ too.

The worklist starts with `main`, where `n` is ⊥. Processing `main` reaches `scale` with $x = \bot$ and $k = 4$, and `count` with $i = 0$ and $\mathit{lim} = 5$. Processing `scale` reaches `mul` with $u = \mathrm{VAL}[\mathit{scale}, x] = \bot$ and $v = \mathrm{VAL}[\mathit{scale}, k] = 4$. Processing `count` meets $i = 0$ with ⊥ from the recursive call, so $i$ drops to ⊥ and `count` goes back into the worklist, while $\mathit{lim}$ meets 5 with $\mathrm{VAL}[\mathit{count}, \mathit{lim}] = 5$ and stays 5. One more pass over `count` and one over `mul` change nothing.

| procedure | formals |
|---|---|
| `main` | $n = \bot$ |
| `scale` | $x = \bot$, $k = 4$ |
| `mul` | $u = \bot$, $v = 4$ |
| `count` | $i = \bot$, $\mathit{lim} = 5$ |

Line L12 gives `scale`, `mul` and `count` a new entry block. For `count` it is:

```
ipcp.entry:
  lim = 5
  jump B0
```

Constant propagation inside `mul` then turns `t = u * v` into `t = u * 4`, which strength reduction can make a shift. The value 4 reached `mul` only through `scale`, which passes `k` on unchanged. On $n = 3$ both versions return 53.

## Correctness

The proof file has the full proof. It has three parts.

- **Local soundness.** In an activation of $f$ that started with formals $\sigma$, at every point that the run reaches, a name with local value $k$ holds $k$, and a name with local value $q$ holds $\sigma(q)$. This is the usual induction for a forward analysis at its fixed point. A call cannot change the caller's variables, so only its result becomes ⊥. So an argument with jump function $k$ is $k$, and one with jump function $q$ is $\sigma(q)$.
- **Global fixed point.** When $W$ is empty, every call site $s$ from $f$ to $g$ has $\mathrm{VAL}[g, p_i] \sqsubseteq J(s, i)$ evaluated in $\mathrm{VAL}[f, \cdot]$. The reason is that $f$ was processed after its values last changed, and values only go down.
- **Soundness.** By induction on the order in which activations start, every activation of $f$ starts with each formal $p$ in the set that $\mathrm{VAL}[f, p]$ describes. The first activation of `main` has ⊥ formals. For an activation made by a call site, the two facts above give the step. Recursion needs no special care, because the induction is over activations, not over the call graph.

The new entry block writes into each constant formal the value that it already holds, so the transformed program runs the same steps and has the same outcome.

## Complexity

The local analysis of a procedure with $n_f$ size, $b_f$ blocks and $v_f$ names lowers each name in the start state of a block at most once below its first value. So each block is processed at most $v_f + 2$ times, at a cost of $O(\text{its length} + v_f)$. Summed over all procedures, line L1 costs $O((v + 1)(n + b v))$. In the worklist, a value goes down at most twice, from $\top$ to a constant and then to $\bot$. So a procedure with $k_f$ formals is processed at most $1 + 2 k_f$ times, and each time costs the size of its call sites. This gives $O((k + 1) n)$ for lines L5 to L11. Line L12 is linear. The jump functions take $O(n)$ space, the values one entry per formal, and the local analysis of one procedure $O(b v)$ at a time.

## Properties

- **Sound.** A claimed constant holds on every call in every run, for any inputs of `main`, with or without recursion.
- **Flow-insensitive between procedures.** A formal gets one value for all calls. Two callers that pass 1 and 2 make it ⊥, even if each call alone could be specialized.
- **Monotone and terminating.** Values only go down in a lattice of height 2.
- **Precision depends on the jump functions.** A pass-through jump function moves constants along chains of calls. Without it, the constant 4 in the example never reaches `mul`.
- **Deterministic.** The order of the worklist can change the number of steps, not the result, since the result is the greatest fixed point of the equations.

## Variants and improvements

- **Kinds of jump functions.** Grove and Torczon compared literal constant jump functions, which only see constants written at the call, intraprocedural constant ones as on this page, pass-through ones, and polynomial ones, which allow expressions such as `q + 1` over the caller's formals. In their study, pass-through functions came close to the more expensive kinds at a much lower cost.
- **Return jump functions.** Callahan and colleagues also describe the result of a procedure as a function of its formals, so that `a = call scale(n, 4)` can become a constant when `scale` returns a constant.
- **Conditional propagation.** LLVM's `ipsccp` pass runs [sparse conditional constant propagation](/sparse-conditional-constant-propagation/) over the whole module. It skips branches that cannot run and call sites in them, so it finds more constants, and it also tracks constant return values.
- **Cloning.** When the callers disagree, a compiler can make a copy of the callee for the calls that pass a constant. This is procedure cloning, a middle ground between this algorithm and [inlining](/function-inlining/).
- **Context-sensitive analysis.** [IDE](/ide-framework/) and the [functional approach](/functional-approach-interprocedural/) give a result for each calling context instead of one value per formal.

## When to use it

Use it in a compiler that sees the whole program or a whole module, such as at link time, before inlining decisions and cloning. It is cheap, because each procedure is analyzed once and the propagation touches only call sites. It pays most in programs with configuration parameters, flags and sizes passed down through several layers of calls. Inside one procedure after inlining, plain constant propagation is enough.

## Pitfalls

- **Unknown callers.** A procedure that can be called from outside the analyzed code, for example an exported function, a function whose address is taken, or a callback, must have all its formals at ⊥. Otherwise a call from outside can break the claim.
- **Indirect calls.** A call through a function pointer or a virtual call must be resolved to its possible targets by [call graph construction](/call-graph-construction/), and each target must get the meet of the arguments. A missed target makes the result unsound.
- **Memory.** If a callee can write the caller's variables through pointers, a value that the local analysis keeps after a call may be wrong. The local analysis must treat names whose address is taken as ⊥ after calls, or use a mod-ref summary of the callee.
- **Starting at ⊥ by mistake.** If every formal starts at ⊥, nothing is ever found. Only the entry points start at ⊥. The others start at ⊤ and drop as calls are seen.
- **Dead callers.** A call site in code that never runs still lowers the values of its callee. A conditional variant avoids this.

## Implementations

## History

Callahan, Cooper, Kennedy and Torczon presented interprocedural constant propagation with jump functions at the SIGPLAN Symposium on Compiler Construction in 1986. They separated the cost of building jump functions from the cheap propagation over the call graph, and they described return jump functions. Grove and Torczon measured the kinds of jump functions on real programs at PLDI 1993. Later compilers, such as LLVM with its `ipsccp` pass, combine the interprocedural step with sparse conditional constant propagation.

## References
