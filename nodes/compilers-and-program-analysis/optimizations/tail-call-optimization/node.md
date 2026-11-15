---
tag: CVDNZN
kind: technique
slug: tail-call-optimization
name: Tail call optimization
aliases:
- tail call elimination
- proper tail calls
area: compilers-and-program-analysis/optimizations
level: core
summary: Compiles a call in tail position as a jump that reuses the caller's frame, so tail recursion runs in constant stack space.
prereqs: [activation-record, recursion]
see_also: [function-inlining, continuation-passing-style, cps-conversion, stack, loop-unrolling, lambda-calculus, defunctionalization, closure-conversion]
sources:
  - paper: doi:10.1145/800179.810196
    title: "Guy Lewis Steele Jr., Debunking the 'expensive procedure call' myth, or procedure call implementations considered harmful, or LAMBDA: the ultimate GOTO, Proceedings of the 1977 Annual Conference of the ACM (ACM '77), 153-162"
    locator: the whole paper (a procedure call in tail position compiled as a jump with argument passing, so that calls cost no more than GOTO)
  - paper: doi:10.1145/277650.277719
    title: "William D. Clinger, Proper tail recursion and space efficiency, Proceedings of the ACM SIGPLAN 1998 Conference on Programming Language Design and Implementation (PLDI 1998), 174-185"
    locator: the whole paper (a formal definition of proper tail recursion as a class of space consumption, compared with other implementation strategies)
  - book: isbn:9780128154120
    title: "Keith D. Cooper and Linda Torczon, Engineering a Compiler, 3rd edition, Morgan Kaufmann, 2022"
    locator: Section 10.4.1 (tail-call optimization)
  - url: "https://llvm.org/docs/Passes.html"
    title: LLVM Project, LLVM's Analysis and Transform Passes, LLVM documentation
    locator: the entry for -tailcallelim (self-recursive calls followed by a return become a branch to the entry of the function, which makes a loop)
---

A call is in *tail position* if the caller has nothing left to do after it except return the callee's result. Tail call optimization compiles such a call as a jump: the caller puts the arguments where the callee expects them, gives up its own frame, and jumps to the callee, which later returns straight to the caller's caller. When a function calls itself in tail position, the jump goes back to its own start, and the recursion becomes a loop. A language with *proper tail calls*, such as Scheme, guarantees this, so programs in it can write loops as recursion without running out of stack.

## In plain words

When a function calls another one, the computer keeps a note, called a frame, so that it knows where to come back and what the caller was doing. Each active call has its own frame, and the frames pile up on a stack.

Sometimes the last thing a function does is call another function and hand back its answer unchanged. Then the caller's note is useless: after the call there is nothing left to do but pass the answer on. So the compiler can throw the caller's frame away first and let the callee answer the caller's caller directly.

For a function that calls itself this way, the stack no longer grows with each call. A recursive loop with a million steps then uses one frame instead of a million.

## When it applies

Take a call `x = call f(a1, ..., ak)` in a function $g$. It is a *tail call* when:

- **(T1) Tail position.** The next thing $g$ does is `ret x`, with no other instruction on any path in between. In source code, `return f(a);` is a tail call, while `return f(a) + 1;`, `return -f(a);` and `f(a); return 0;` are not.
- **(T2) Nothing pending.** No cleanup is scheduled for after the call in $g$: no destructor of a local object, no `finally` block, no exception handler that covers the call.
- **(T3) No pointer into the frame of $g$.** The callee must not get the address of a local variable of $g$, directly or through memory, because that frame is about to be reused.
- **(T4) A compatible calling convention.** The machine-level setup must allow the jump: for example, the callee's stack arguments must fit in the space that $g$'s caller set up, and the stack must be popped by the right party. A self call always meets this condition.

## The template

**Self tail calls (tail recursion elimination).** Let $g$ have parameters $p_1, \dots, p_k$, and let `x = call g(b1, ..., bk); ret x` be a tail call of $g$ to itself.

1. If the entry block of $g$ has predecessors, or to keep it simple in any case, add a new entry block that only jumps to the old one, so the old entry can be the target of a back edge.
2. Replace the call and the return by `q1 = b1`, ..., `qk = bk`, then `p1 = q1`, ..., `pk = qk`, then `jump` to the old entry block. The fresh names $q_i$ make the assignment parallel: each $b_i$ is evaluated with the old values of the parameters.
3. In SSA form, the old entry now gets [φ-functions](/phi-function/) for the parameters.

**General tail calls.** At the machine level, evaluate the arguments, move them into the callee's argument registers or stack slots, restore the callee-saved registers, pop the frame of $g$, and jump to $f$. The return address on the stack is still the one of $g$'s caller, so $f$ returns there.

**Why the behavior stays the same.** In the self case, the old program, on the call, makes a new frame for $g$ with $p_i = b_i$, runs $g$ from its entry, and then returns its result through each waiting frame unchanged, by (T1) and (T2). The new program sets $p_i = b_i$ in the current frame and runs $g$ from its entry. The other locals of $g$ are dead at the entry: a toy program never reads a variable before it writes it on every path, so their old values cannot be seen. By (T3) no pointer refers to the old values. So the two runs do the same steps on the same values, and the final `ret` gives the same value that the chain of returns would give. In the general case the same argument applies to the frame of $f$ placed where the frame of $g$ was.

**Theorem (bounded stack).** Model a run with a stack of frames. A non-tail call pushes a frame, a return pops one, and an optimized tail call replaces the top frame by the frame of the callee. Then at every moment, the depth of the stack is $1 + N$, where $N$ is the number of non-tail calls that have started and not yet returned.

*Proof.* At the start the stack holds one frame and $N = 0$. A non-tail call adds one frame and one active non-tail call. A tail call replaces a frame, so the depth stays the same, and it does not start a non-tail call. A return pops the top frame. That frame was pushed by a non-tail call, possibly followed by tail calls that replaced it, and the return ends that non-tail call, so $N$ drops by one too. If the frame is the bottom one, the run ends. $\square$

**Corollary.** A tail-recursive loop runs in bounded stack space. If $g$ calls itself only in tail position, and the other calls in its body nest at most $d$ deep, then a run of $g$ with any number of iterations never has more than $d + 1$ frames. Each frame of the toy IR has a fixed set of variables, so the space is bounded by a constant that does not depend on the input. Without the optimization every self call is a non-tail call, and $n$ iterations need $n + 1$ frames.

## Classic examples

**Factorial with an accumulator.** The parameters are `n` and `acc`, and `fact(n, acc)` returns $n! \cdot acc$.

```
B0:
  c = n == 0
  br c B1 B2
B1:
  ret acc
B2:
  n1 = n - 1
  a1 = acc * n
  r = call fact(n1, a1)
  ret r
```

The call in `B2` is followed by `ret r`, so it is a tail call to itself. Tail recursion elimination gives:

```
start:
  jump B0
B0:
  c = n == 0
  br c B1 B2
B1:
  ret acc
B2:
  n1 = n - 1
  a1 = acc * n
  n = n1
  acc = a1
  jump B0
```

The new version is a loop, and `fact(100000, 1)` uses one frame. The plain definition `fact(n) = n * fact(n - 1)` is not tail recursive, because the multiplication waits for the call. The accumulator moves this pending work into an argument.

**Mutual recursion.** `even(n)` returns `odd(n - 1)` and `odd(n)` returns `even(n - 1)`, with base cases at 0. Each call is a tail call to the other function. Tail recursion elimination of self calls does not help here. General tail calls, as jumps between the two functions, run it in constant stack.

**State machines and continuations.** An interpreter or a lexer written as one function per state, where each state ends by calling the next state, runs in constant stack only with general tail calls. [Continuation-passing style](/continuation-passing-style/) makes every call a tail call, so compilers that use [CPS conversion](/cps-conversion/) rely on proper tail calls.

## Variations

- **Self recursion only.** Many compilers turn self tail calls into loops and handle other tail calls as normal calls. LLVM's `tailcallelim` pass does this.
- **Sibling calls.** C compilers do general tail calls when the calling conventions match, under names such as sibling call optimization. Clang also has a `musttail` attribute that makes a tail call a requirement, so the build fails if it cannot be done.
- **Accumulator introduction.** A call like `return n * f(n - 1)`, where the pending operation is associative, can be turned into a loop with an extra accumulator, as in the factorial example.
- **Tail recursion modulo cons.** A call whose result is put directly into a new data cell, as in `return cons(x, f(y))`, can become a loop that fills the cell later through a pointer.
- **Trampolines.** On a platform without tail calls, a function returns a description of the next call instead of making it, and a driver loop makes the calls one by one. The stack stays bounded at the cost of an extra return and call per step.

## Pitfalls

- **Stack traces change.** A tail call removes the frame of the caller. A debugger backtrace, an exception stack trace or a profiler then skips the functions that made tail calls, and a loop of self calls shows as one frame. Code that walks the stack to find its caller, for example for security checks or logging, sees a different caller. Compilers often turn the optimization off in debug builds for this reason.
- **Correct only in optimized builds.** In C and C++ the optimization is not required by the language. Deep tail recursion that works in an optimized build can overflow the stack in a debug build. Do not rely on it without a guarantee such as `musttail`.
- **Calls that look like tail calls.** `return f(x) + 1`, a conversion of the result, a destructor of a local object, or a `try` block around the call all leave work after the call.
- **The address of a local.** `return f(&x)` with a local `x` cannot reuse the frame, because `f` reads `x` through the pointer. The compiler must keep the frame or move `x` elsewhere.
- **Argument overlap.** When the arguments are computed from the parameters, as in `return g(b, a)` inside `g(a, b)`, the new values must be computed before any parameter is overwritten. Without the temporaries of step 2, the swap becomes `a = b; b = a`, which is wrong.

## Exercises

1. Is the call in `return f(x) || g(y);` a tail call? *Answer.* The call of `g` is: if it runs, its result is the result of the expression. The call of `f` is not, because its result must be tested first.
2. Why must the arguments of a self tail call be evaluated into fresh names first? *Answer.* An argument can read a parameter that an earlier assignment already changed. With `g(a, b)` calling `g(b, a)`, assigning in place gives `a = b` and then `b = a`, so both get the old `b`.
3. Use the theorem to bound the stack of `even(n)` and `odd(n)` with general tail calls. *Answer.* All calls between them are tail calls, so $N = 0$ during the run, and the depth stays 1 frame for any $n$.
4. A tail-recursive function `walk(t)` calls `visit(t)` in a non-tail position, and `visit` calls nothing. What is the most frames that a run of `walk` uses? *Answer.* Two: by the theorem the depth is $1 + N$, and $N \le 1$ because only the call of `visit` is a non-tail call and it returns before the next tail call.
5. Why is the transformation unsafe if the callee receives the address of a local of the caller? *Answer.* The frame of the caller is reused for the callee, so the local may be overwritten by the callee's own locals, and a read through the pointer would see a wrong value.

## References
