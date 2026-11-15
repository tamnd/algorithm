---
tag: H29A5E
kind: technique
slug: function-inlining
name: Function inlining
aliases:
- inline expansion
- procedure integration
area: compilers-and-program-analysis/optimizations
level: core
summary: Replaces a call by a copy of the body of the callee, which removes call overhead and exposes the body to optimization at the call site.
prereqs: [call-graph, activation-record]
see_also: [devirtualization, interprocedural-constant-propagation, tail-call-optimization, scalar-replacement-of-aggregates, partial-evaluation, profile-guided-optimization, knapsack-problem, deoptimization]
sources:
  - paper: doi:10.1145/359810.359830
    title: "Robert W. Scheifler, An analysis of inline substitution for a structured programming language, Communications of the ACM 20(9), 1977, 647-654"
    locator: the whole paper (inline substitution of procedure calls, its effect on run time and program size, and the choice of which calls to expand)
  - book: isbn:9780128154120
    title: "Keith D. Cooper and Linda Torczon, Engineering a Compiler, 3rd edition, Morgan Kaufmann, 2022"
    locator: Section 8.7.1 (Inline Substitution)
  - url: "https://llvm.org/docs/Passes.html"
    title: LLVM Project, LLVM's Analysis and Transform Passes, LLVM documentation
    locator: the entries for -inline and -always-inline (bottom-up inlining of functions into callers)
---

Function inlining replaces a call by a copy of the body of the called function. The arguments are bound to fresh copies of the parameters, the local names of the callee get fresh names, and each return becomes an assignment of the result and a jump back to the code after the call. The direct gain is that the call and return, the argument passing and the saving of registers go away. The larger gain is that the copy of the body now sits in the caller, where the compiler knows the actual arguments, so later passes can fold constants, remove dead branches and merge redundant work across what used to be a procedure boundary.

## In plain words

Calling a function costs a little: the program jumps away, sets up the callee's frame, and jumps back. For a tiny function this overhead can cost more than the work.

Inlining pastes the body of the function at the place of the call, with the argument values put in for the parameters. The program does the same work without the jump.

There is a second, bigger benefit. Once the body sits in the caller, the compiler can see that an argument is, say, the constant 0. It can then drop a test that is always false, and much of the pasted code may vanish.

The price is size. Each inlined call adds a copy of the body. Inlining a big function at many call sites makes the program large and can make it slower. A function that calls itself cannot be pasted in fully, because each copy contains another call.

## When it applies

Take a call `x = call f(a1, ..., ak)` in a procedure $g$. Inlining it needs:

- **(I1) A known callee.** The call names one function $f$. An indirect or virtual call must first be resolved by [devirtualization](/devirtualization/), possibly with a guard.
- **(I2) The body is available.** The code of $f$ is in the same compilation unit, or the compiler sees the whole program, for example at link time.
- **(I3) The body can be copied.** Constructs that depend on having their own frame need care: a dynamically sized stack allocation inside a loop of the caller grows the caller's frame on every iteration, and features like `setjmp`, stack inspection or variadic argument access depend on the frame of $f$ being separate.
- **(I4) A bound on the copies.** If $f$ can reach a call to itself in the [call graph](/call-graph/), each copy contains a new call that could be inlined again. The compiler must stop at a fixed depth or never inline along some edge of each cycle.

## The template

In the toy IR, a call `x = call f(a1, ..., ak)` sits in a block $B$ of $g$.

1. **Split the block.** Cut $B$ after the call. The part after the call becomes a new block $C$, the continuation.
2. **Rename.** Copy all blocks of $f$. Give every label and every variable of the copy a fresh name that does not occur in $g$. Let $p_1', \dots, p_k'$ be the new names of the parameters.
3. **Bind the arguments.** Replace the call by `p1' = a1`, ..., `pk' = ak` and `jump` to the copy of the entry block of $f$. The arguments are evaluated once, before the body runs, exactly as the call did.
4. **Rewrite the returns.** Each `ret v` in the copy becomes `x = v'` and `jump C`, where $v'$ is the renamed $v$. In SSA form, the values of the returns meet at a [φ-function](/phi-function/) at the top of $C$.
5. **Clean up.** Run copy propagation, [constant folding](/constant-folding/), dead code elimination and the other local passes on the merged body. If every call of $f$ has been inlined and $f$ is not exported, delete $f$.

**Why the behavior stays the same.** Consider the toy interpreter, which keeps one frame per activation. When the old program executes the call, it creates a frame for $f$ with the parameters bound to the argument values, runs the body of $f$ in that frame, and on `ret v` puts $v$ into $x$ and goes on after the call. The new program, at the same point, sets $p_i'$ to the argument values and runs the copy in the frame of $g$. Map each name $y$ of the frame of $f$ to its fresh name $y'$. By induction on the steps of the body, each instruction of the copy reads and writes the renamed names exactly as the original reads and writes the frame of $f$, takes the same branches and computes the same values or traps. The names of $g$ are not touched, since the fresh names are disjoint from them. A `ret v` of the old body and the matching `x = v'; jump C` of the copy give $x$ the same value, and both programs go on with $C$. A call inside $f$ stays a call in the copy and behaves the same. Only the number of steps changes: the call overhead is gone.

**Profit.** The gains are the removed call overhead, and the optimizations that the copy enables at the call site. The costs are code size, the instruction cache, compile time, and register pressure in the merged body. Compilers decide call by call with a cost model:

- always inline very small functions, whose body is smaller than the call sequence;
- inline a function with one call site, and delete it, since the program then shrinks;
- give a bonus for constant arguments that will fold branches, and for calls inside hot loops when [profile data](/profile-guided-optimization/) is present;
- stop when the caller grows past a size budget.

Picking the calls that give the most gain under a size budget resembles the [knapsack problem](/knapsack-problem/), but the items interact: inlining one call changes the size of the caller and the benefit of the calls inside the copied body. Compilers use greedy rules, usually working bottom-up over the call graph so that a callee is already optimized when it is copied.

## Classic examples

**An accessor.** `int get_x(struct P *p) { return p->x; }` called as `y = get_x(q)` becomes `y = q->x`. The call cost several instructions, and the body costs one load.

**A constant argument.**

```
int clamp(int v, int lo, int hi) {
  if (v < lo) return lo;
  if (v > hi) return hi;
  return v;
}
...
y = clamp(z, 0, 255);
```

After inlining, `lo` and `hi` are the constants 0 and 255, and the copy reads `if (z < 0) ... if (z > 255) ...`. On some targets this becomes a single saturating instruction. Without inlining the callee cannot know the bounds.

**A one-call helper.** A static function called from one place is inlined there and deleted. The program gets smaller and faster at once.

**A recursive function with a bound.** For `fib(n)` the compiler may inline the two recursive calls once, which unrolls one level of the recursion. The copies contain calls to `fib`, which stay calls. Doing this again would double the code each time, so the compiler stops after one level.

## Variations

- **Partial inlining.** Inline only the fast path of the callee, such as an early return, and keep a call to an outlined copy of the slow path.
- **Procedure cloning.** Make a specialized copy of $f$ for a set of call sites that pass the same constants, without merging it into each caller. This gets the constant folding with less growth. [Interprocedural constant propagation](/interprocedural-constant-propagation/) finds which constants to specialize on.
- **Speculative inlining in JIT compilers.** A JIT inlines the target that type feedback reports at a virtual call, behind a guard that checks the receiver's class. If the guard fails, the code calls the method normally or falls back to [deoptimization](/deoptimization/).
- **Functional languages.** Inlining a function value is beta reduction in the [lambda calculus](/lambda-calculus/). Compilers for lazy languages must not copy an argument expression that is used twice, or the work is duplicated, and they choose *loop breakers* in each recursive group, which are never inlined, so that inlining terminates.
- **Link-time inlining.** Link-time optimization keeps an IR of each unit, so calls across files can also be inlined.

## Pitfalls

- **Recursion needs a bound.** Inlining `f` into itself copies a body that again contains a call of `f`. Repeating the step never ends, and each round adds a full body. A compiler must bound this: inline along a call graph cycle at most $k$ times, or mark one function in each strongly connected component of the call graph as never inlined. With a bound of $k$ levels, a function with $c$ self-calls grows by a factor of about $c^k$, so $k$ must stay small.
- **Code growth.** Inlining a medium-sized function at hundreds of call sites can make the program much larger and slower, through instruction cache misses. Budgets per caller and per program are needed.
- **Frame-dependent code.** A stack allocation of variable size in the callee is freed when the callee returns. After inlining into a loop, it is freed only when the caller returns, so the stack can overflow. Compilers refuse to inline such callees into loops, or restore the stack pointer after the copy.
- **Debugging and stack traces.** The inlined function no longer has a frame, so a debugger or a crash report must use extra debug information to show it.
- **Separate compilation.** A caller that inlined a function from another unit must be recompiled when that function changes.
- **Argument evaluation.** The arguments must be evaluated once, in the original order, before the body. Pasting the argument expressions into the body in place of the parameters can repeat or reorder side effects.

## Exercises

1. Why must the copied body use fresh variable names? *Answer.* The callee and the caller may use the same name for different variables. Without renaming, an assignment in the copy would overwrite a variable of the caller that is still live after the call.
2. A function `f` has two `ret` instructions. What does the inlined copy look like in SSA form? *Answer.* Each return becomes a jump to the continuation block $C$, and $C$ starts with `x = φ(v1, v2)` that merges the two returned values.
3. `f` calls `g` and `g` calls `f`. A compiler inlines every call with a body under 50 instructions. Can it loop forever? *Answer.* Yes, if both are small: inlining `g` into `f` puts a call of `f` inside `f`, which can be inlined again, and so on. A size budget for the caller, or a rule that never inlines a call back into the same cycle, makes it stop.
4. Inlining makes a program larger. Give a case where it makes the program smaller. *Answer.* A static function with one call site: after inlining, the function is deleted, and the call sequence, the prologue and the epilogue are gone too.
5. Why do compilers usually inline bottom-up over the call graph? *Answer.* A callee is then already optimized, and its own small callees are already inlined, when it is copied. The cost model sees its real size, and the work done on the callee is reused in every copy.

## References
