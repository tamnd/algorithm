---
tag: JA6FDE
kind: technique
slug: deoptimization
name: Deoptimization
aliases:
- dynamic deoptimization
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Falls back from optimized code to the interpreter or less optimized code when a speculative assumption fails, rebuilding the frames.
prereqs: [just-in-time-compilation, activation-record, function-inlining]
see_also: [on-stack-replacement, type-feedback, adaptive-optimization, escape-analysis, class-hierarchy-analysis, simulation-relation, inline-caching, hidden-classes]
sources:
  - paper: doi:10.1145/143095.143114
    title: Urs Hölzle, Craig Chambers and David Ungar, Debugging optimized code with dynamic deoptimization, PLDI 1992, 32-43
    locator: the conversion of an optimized frame into unoptimized frames on demand, with scope descriptors and a mapping of program counters, at interrupt points, to show source-level state to the debugger
  - paper: "Urs Hölzle, Adaptive optimization for SELF: reconciling high performance with exploratory programming, PhD thesis, Stanford University, 1994 (report STAN-CS-TR-94-1520)"
    locator: Section 6.1.4 (uncommon traps and the recompilation after frequent traps), Section 10.2 (deoptimization, with 10.2.1 recovering the unoptimized state, 10.2.2 the transformation function in five steps, 10.2.3 lazy deoptimization and 10.2.4 interrupt points), Section 10.3 (dependencies and the invalidation of active methods) and Section 10.5.2 (no tail call elimination)
  - paper: doi:10.1145/3158137
    title: Olivier Flückiger, Gabriel Scherer, Ming-Ho Yee, Aviral Goel, Amal Ahmed and Jan Vitek, Correctness of speculative optimizations with dynamic deoptimization, Proceedings of the ACM on Programming Languages 2(POPL), 2018
    locator: the intermediate language with an assume instruction that carries the deoptimization metadata, and the proofs that speculative optimizations and inlining preserve its semantics
  - paper: doi:10.1145/3192366.3192396
    title: Daniele Cono D'Elia and Camil Demetrescu, On-stack replacement, distilled, PLDI 2018, 166-180
    locator: the treatment of deoptimization as a transition from optimized to base code at a program point, with a compensation function that rebuilds the state
---

Deoptimization moves a running computation out of optimized machine code and back into unoptimized code or an interpreter, in the middle of a method. It replaces each optimized frame on the stack with the frames that the unoptimized code would have at that moment, one for each method that the optimizer had inlined, with the right program counters and the values of all local variables and operand stack slots. A [JIT compiler](/just-in-time-compilation/) needs it for two reasons. Optimized code is often *speculative*: it assumes what the profile showed, such as one receiver class or small integers, and when a guard finds the assumption false the code must leave. And a debugger needs to show the state of the source program, which optimized code does not hold in that form. Hölzle, Chambers and Ungar introduced the technique in SELF in 1992 for debugging, and it became the safety net for speculation in Java and JavaScript engines. It is correct when the map from the optimized state to interpreter frames is exact. This page states that invariant.

## In plain words

A fast version of a function is made under some guesses, for example "this value is always a small number". Most of the time the guess is right and the fast code runs. When it is wrong, the program must not stop and must not give a wrong answer.

So at each place where a guess is checked, the compiler writes down a recipe: where each variable of the original function is kept at that moment, and at which line of the original function the work has arrived. If the check fails, the runtime follows the recipe. It builds the frames that the slow version would have, with the same values and at the same line, and lets the slow version go on. The fast code was a shortcut, and the recipe leads back to the normal road at the exact point reached.

## When it applies

- An optimizing compiler makes code under assumptions that can fail at run time: types from [type feedback](/type-feedback/), a single target from [class hierarchy analysis](/class-hierarchy-analysis/), the [hidden class](/hidden-classes/) of an object, a branch that was never taken.
- The system keeps an unoptimized form of each method, an interpreter or baseline code, that can run from any point that the optimized code can leave at.
- The optimized code inlines methods, keeps values in registers, removes allocations and reorders work, so its frame does not look like the unoptimized frames.
- A debugger, an exception handler or a profiler must see the state of the source program in a frame of optimized code.

## The template

### States and descriptors

An *interpreter state* $\sigma = (F, H)$ has a heap $H$ and a stack $F$ of frames. Each frame holds a method $u$, a program counter $\mathit{pc}$ in the bytecode of $u$, and the values of the local variables and of the operand stack. The interpreter takes deterministic steps $\sigma \to \sigma'$.

Optimized code $O$ for a method has *deoptimization points*: guards, calls, and points where the runtime may interrupt it (Hölzle chose method prologues and loop back edges, thesis Section 10.2.4). For each point $p$ the compiler records a descriptor $D_p$: the list of *virtual frames* that the optimized frame stands for at $p$, from the outer method to the innermost inlined one. Each virtual frame names a method $u_i$, a program counter $\mathit{pc}_i$, and for each local and operand slot a *location*: a register, a stack slot of the optimized frame, a constant, or a recipe to allocate an object whose allocation the optimizer removed.

Given the machine state $s$ of the optimized frame at $p$ and the heap $H$, $\mathrm{decode}_p(s, H)$ reads every location and gives the virtual frames and the heap with the removed objects allocated again.

### The exactness invariant

Let $\mathrm{enc}(\sigma)$ be the machine state in which $O$ is entered from an interpreter state $\sigma$ whose top frame is at the entry of the method of $O$. The compiler must guarantee:

> **Exactness.** For every such $\sigma = (F \cdot f, H)$ and every run of $O$ from $\mathrm{enc}(\sigma)$ that reaches the deoptimization point $p$ with machine state $s$ and heap $H'$, the interpreter run from $\sigma$ reaches the state $(F \cdot \mathrm{frames}, H'')$, where $(\mathrm{frames}, H'') = \mathrm{decode}_p(s, H')$.

In words: the frames rebuilt at $p$, together with the heap, form a state that the plain interpreter passes through on the same input. The same must hold for frames of $O$ that are suspended in a call, at the return point of the call, with the frames of the callee on top.

**Claim.** If exactness holds, then deoptimizing at $p$ and continuing in the interpreter gives the same outcome as interpreting from $\sigma$: the same returned value, the same final heap, the same output, the same error, or no end.

*Proof.* The interpreter is deterministic, so from $\sigma$ there is exactly one run. By exactness, that run passes through $\sigma_p = (F \cdot \mathrm{frames}, H'')$. The rest of a deterministic run from a state it passes through is the run from that state, so continuing from $\sigma_p$ gives the outcome of the run from $\sigma$. The output before $p$ is the same too, because exactness includes the heap, and the optimized code may only do the effects that the interpreter does before $\sigma_p$. $\square$

The claim reduces the correctness of deoptimization to one property of the compiler. Each optimization must keep the descriptors in step with the code it changes. If constant propagation finds that a slot is the constant 7, its location becomes the constant 7. If dead code elimination removes the last use of a value, the descriptor still uses it, so it is not dead. If code motion moves a store above a guard, the store happens even when the guard fails, and the heap no longer matches; so stores and other effects must not cross a deoptimization point. Flückiger and others prove such rules for a small intermediate language with an `assume` instruction that carries the descriptor.

### The transformation

Hölzle gives the transformation of one optimized frame in five steps (thesis, Section 10.2.2), which in the notation above are:

1. Save the contents of the optimized frame and remove it from the stack.
2. Find the descriptor $D_p$ for its program counter, which lists the virtual frames, their locals and their program counters.
3. Make an unoptimized version of each method that appears, and push one unoptimized frame for each virtual frame, outer first.
4. Set the program counter of each new frame to the machine address that matches $\mathit{pc}_i$ in its unoptimized code.
5. Copy the parameters, the locals and the operand stack values from their locations into the new frames.

In an interpreter, step 3 and step 4 are only "push an interpreter frame at $\mathit{pc}_i$".

### Eager and lazy deoptimization

A failed guard deoptimizes its own frame at once, which is *eager* deoptimization. When an assumption about the whole program becomes false, for example because a newly loaded class overrides a method that was inlined, the system must stop all code that depends on it. Frames that are running that code but are suspended in a call are deoptimized *lazily*: the runtime changes the return address of the callee so that the return goes to a routine that deoptimizes the caller (thesis, Section 10.2.3). This is correct because the code of the caller that has run so far ran while the assumption still held, and none of it runs again: on return the caller continues in the interpreter at the descriptor of the call site, with the returned value on its operand stack.

### A worked example

Let small integers be the range from $-2^{30}$ to $2^{30} - 1$, and take these two methods:

```
f(a):  pc 0: t = a * 2          g(x):  pc 0: return x + 3
       pc 1: u = g(t)
       pc 2: return u + a
```

The optimized code for `f` inlines `g` and assumes small integers:

```
f_opt(a):  guard a is a small integer               ▷ point p0, frames: f at pc 0
           r2 = a * 2;  guard no overflow           ▷ point p1, frames: f at pc 0
           r3 = r2 + 3; guard no overflow           ▷ point p2, frames: f at pc 1 {a = r1, t = r2}, g at pc 0 {x = r2}
           return r3 + a with a guard, as at p2
```

Run `f(536870911)`, so $a = 2^{29} - 1$. Then `r2` is $1073741822$, which fits. Then $1073741822 + 3 = 1073741825$, which is more than $2^{30} - 1 = 1073741823$, so the guard at $p_2$ fails. The descriptor of $p_2$ gives two frames: `f` at pc 1, waiting for the call, with $a = 536870911$ and $t = 1073741822$, and on top of it `g` at pc 0 with $x = 1073741822$. The interpreter runs `g` with general arithmetic and returns $1073741825$ to `f`, which sets $u = 1073741825$ and returns $u + a = 1610612736$. This is exactly what the interpreter computes for `f(536870911)` from the start, and the descriptor is exact because the interpreter from the start does pass through these two frames with these values.

If the descriptor of $p_2$ had only the frame of `f` at pc 1, `g` would never run, and $u$ would have no value. If it had `f` at pc 0, the multiplication would be done twice, which here is harmless but would print twice if pc 0 had output. Exactness rules out both.

## Classic examples

- **SELF, for debugging.** Hölzle, Chambers and Ungar deoptimized frames on demand when the programmer stopped in optimized code, so the debugger could show and change every source-level variable. Program changes invalidate the compiled methods that depend on the changed code, through dependency links, and active frames are deoptimized lazily (thesis, Section 10.3).
- **SELF-93 uncommon traps.** The optimizing compiler leaves out the code for cases that the profile shows to be rare, and puts an *uncommon trap* there. When a trap fires, the frame is deoptimized and the case runs in unoptimized code. If traps fire often, the method is recompiled without that assumption (thesis, Section 6.1.4).
- **Java virtual machines.** Optimized code inlines virtual calls that class hierarchy analysis shows to have one target, with a dependency on that fact. Loading a class that adds an override deoptimizes the dependent frames. Uncommon traps are used in the same way as in SELF.
- **JavaScript engines.** Type checks, hidden-class checks and overflow checks in optimized code are guards with descriptors. A failed guard is an eager deoptimization, and a change of a prototype or of a field type invalidates dependent code lazily.

## Variations

- **Deoptimize to an interpreter or to baseline code.** An interpreter frame needs only a method, a pc and values. Baseline machine code also needs the machine address for the pc and its own frame layout, which step 4 finds.
- **Materializing removed objects.** If [escape analysis](/escape-analysis/) and [scalar replacement](/scalar-replacement-of-aggregates/) removed an allocation, the descriptor holds the field values, and deoptimization allocates the object. Each removed object must be allocated once even if several frames refer to it, to keep its identity.
- **Deoptimization as the reverse of on-stack replacement.** Both move a running frame between two versions of code at a matching point. [On-stack replacement](/on-stack-replacement/) goes from slow to fast code, deoptimization from fast to slow, and D'Elia and Demetrescu treat both with one model.
- **Deoptimization without a guard.** A guard that only re-checks a fact that the system already watches can be removed, and the system relies on lazy deoptimization when the fact changes. This trades a test on every run for a dependency.

## Pitfalls

- **Missing inlined frames.** The descriptor must list every inlined method that is active at $p$, as the example shows. Leaving out a frame loses the rest of the inner method.
- **The wrong pc.** If the rebuilt pc is before an effect that the optimized code has already done, the interpreter does it again. If it is after an effect that the optimized code has not done, the effect is lost. Effects must not move across deoptimization points.
- **Values that the optimizer dropped.** A value can be dead for the optimized code but needed by a descriptor. Count the descriptors as uses in liveness, or keep a way to recompute the value.
- **Tail calls.** A tail call in optimized code removes a frame that the interpreter would have. SELF did not eliminate tail calls for this reason (thesis, Section 10.5.2).
- **Deoptimization loops.** If the system recompiles with the same assumption, the guard fails again. Count the deoptimizations per site and recompile without the assumption.
- **Freeing invalid code too early.** Code that was invalidated can still be on the stack in a suspended frame. Free it only after all such frames have been deoptimized.

## Exercises

1. In the worked example, write the descriptor of the guard at $p_1$ and the frames that deoptimization builds for `f(536870912)`. Check that the interpreter passes through them.
2. Prove that dead code elimination keeps exactness if the values named in descriptors count as uses.
3. An optimized loop keeps a running sum in a register and stores it to the field `o.total` only after the loop. Where can a guard inside the loop deoptimize to, and what must its descriptor say about `o.total`?
4. Escape analysis has removed the allocation of a point `q = Point(a, t)` that is passed to an inlined method. Write a descriptor that lets deoptimization rebuild `q`, and explain why two frames that both refer to `q` must get the same object.
5. Explain why lazy deoptimization at a return address is correct even though the caller's code was compiled under an assumption that is now false.

## References
