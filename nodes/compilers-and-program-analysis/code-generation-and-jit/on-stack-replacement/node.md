---
tag: 9PK11K
kind: technique
slug: on-stack-replacement
name: On-stack replacement
aliases:
- OSR
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Moves a running method from one compiled version to another in the middle of its execution, by mapping the live state of its frame.
prereqs: [deoptimization, adaptive-optimization]
see_also: [deoptimization, just-in-time-compilation, natural-loop, strength-reduction, loop-invariant, simulation-relation, activation-record, tracing-jit-compilation]
sources:
  - paper: doi:10.1109/CGO.2003.1191549
    title: Stephen J. Fink and Feng Qian, Design, implementation and evaluation of adaptive recompilation with on-stack replacement, CGO 2003, 241-252
    locator: on-stack replacement in the Jikes RVM, where the new version is compiled from the bytecode of the method with a prologue that sets the locals and the operand stack to the values from the frame and jumps to the current bytecode position
  - paper: doi:10.1145/3192366.3192396
    title: Daniele Cono D'Elia and Camil Demetrescu, On-stack replacement, distilled, PLDI 2018, 166-180
    locator: the formal model of OSR transitions between two versions of a program at matching points, with compensation code, and the conditions under which program transformations keep OSR mappings correct
  - paper: "Urs Hölzle, Adaptive optimization for SELF: reconciling high performance with exploratory programming, PhD thesis, Stanford University, 1994 (report STAN-CS-TR-94-1520)"
    locator: Section 5.4.1 (the recompilation process, which replaces the unoptimized frames on the stack by one optimized frame that continues at a restart point)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 14, Section 14.5.2 (on-stack replacement)
---

On-stack replacement (OSR) moves a method that is running from one compiled version to another, in the middle of its execution, without starting it again. At a point where the two versions match, typically the header of a loop, the runtime reads the live values of the old frame, maps them into the layout of the new version, replaces the frame on the stack, and continues in the new code. The main use is *OSR entry*: a method that is called once but spends a long time in a loop would never benefit from a better tier if the system waited for the next call, so [adaptive optimization](/adaptive-optimization/) switches the running frame into optimized code at a back edge. The reverse direction, from optimized code back to unoptimized code, is [deoptimization](/deoptimization/), and both are correct for the same reason: the mapped state is a state that the old version passes through, and the new version continues it faithfully.

## In plain words

Picture a program that starts a loop of a million steps, slowly, in an interpreter. After a thousand steps the system sees that the loop is busy and compiles a fast version. But the method is still in the middle of the loop, and it will not be called again. Waiting for the next call is useless.

So the system swaps the running copy. At the top of the loop it takes the current values, such as the counter and the running total, puts them where the fast code expects them, and jumps into the fast code at its own top of the loop. The fast code does the remaining steps. The answer is the same as if the slow copy had gone on, because the fast code starts from exactly the point the slow copy had reached.

## When it applies

- A method runs for a long time in one activation, usually in a loop, so recompiling it for the next call is too late.
- The system has two versions of the method and can find points in both that correspond, together with a map between their states at those points.
- The runtime can read and write frames: it knows where each live value of the old version is, and it can build a frame for the new version.
- For the other direction, the optimized code makes assumptions that can fail, and the system needs to leave it in the middle of a method, which is [deoptimization](/deoptimization/).

## The template

### The general form

Let $A$ and $B$ be two versions of the same method, and let $\ell_A$ in $A$ and $\ell_B$ in $B$ be *matching points*. An *OSR mapping* is a function $\mu$ from the states of $A$ at $\ell_A$ to the states of $B$ at $\ell_B$. Let $\mathrm{out}_A(s)$ be the outcome of running $A$ to the end of the method from state $s$, and the same for $B$. The transition at $\ell_A$ is correct when

$$\mathrm{out}_B(\mu(s)) = \mathrm{out}_A(s) \quad \text{for every state } s \text{ that } A \text{ can reach at } \ell_A.$$

The outcome includes the returned value, the effects on the heap and the output, a raised error, or no end. With the equation, an OSR transition at $\ell_A$ cannot change what the method does: the run of $A$ from the start reaches some $s$ at $\ell_A$, and its outcome from there is $\mathrm{out}_A(s)$, which the new frame then produces.

**Claim.** Let $R$ be a relation between states of $A$ at $\ell_A$ and states of $B$ at $\ell_B$ such that, whenever $R(s, t)$ holds, the runs of $A$ from $s$ and of $B$ from $t$ do the same effects and either both end with the same result, or both come back to their matching points in states $s'$ and $t'$ with $R(s', t')$, or both run forever. If $R(s, \mu(s))$ holds for every reachable $s$, then $\mu$ is a correct OSR mapping.

*Proof.* Take a reachable $s$, and let $t = \mu(s)$. Follow the two runs one round at a time, where a round goes from the matching point to the next visit of the matching point or to the end. By the condition on $R$, each round of $A$ and the matching round of $B$ do the same effects and end in related states, or both end with the same result, or both do not end. By induction on the number of rounds, the two runs do the same effects in the same order for as many rounds as they last, and if one ends, both end with the same result. So $\mathrm{out}_B(t) = \mathrm{out}_A(s)$. $\square$

$R$ is a [simulation relation](/simulation-relation/) between the two versions, checked one loop iteration at a time. In practice $R$ is the [loop invariant](/loop-invariant/) that the optimizer used: the facts about the variables of $B$ that hold at the loop header, such as "the pointer `p` equals the base of the array plus 8 times `i`". The OSR mapping must establish exactly these facts.

### OSR entry at a loop

1. **Count.** The baseline code has a counter at each loop back edge, as in [adaptive optimization](/adaptive-optimization/). When it passes a threshold, the system asks for an OSR version for this loop header.
2. **Compile with an extra entry.** The optimizing compiler compiles the method with a second entry at the loop header. The entry block takes the values of the variables that are live at the header in the baseline frame, applies the mapping to them, and jumps to the loop header of the optimized code.
3. **Transfer.** At the next back edge, the runtime reads the live values from the baseline frame, removes the frame, builds the optimized frame through the entry block, and continues there.
4. **Leave by deoptimization.** Guards inside the optimized loop deoptimize as usual, so the method can go back if an assumption fails.

Fink and Qian use a simple way to get step 2 without changing the compiler. They make a new bytecode method: a prologue that stores the actual values from the frame into the locals and the operand stack, followed by a jump to the current bytecode position, followed by the original bytecode. Any compiler for the bytecode can compile it. Because the prologue sets the exact state that the frame had, and the rest is the same bytecode, the new method continues the run exactly, and the values in the prologue are constants that the compiler may use. The price is that this version fits only one transition.

### A worked example

```
sum(a, n):  s = 0; i = 0
     L:     if i = n goto done        ▷ the loop header, the OSR point
            s = s + a[i]; i = i + 1; goto L
     done:  return s
```

The optimized version uses [strength reduction](/strength-reduction/): it keeps a pointer `p` to the current element and a pointer `e` past the last one, and drops `i`. Its loop invariant at `L` is $p = \mathit{base}(a) + 8i$ and $e = \mathit{base}(a) + 8n$, with $s$ the same in both versions. So the OSR entry mapping is

$$\mu(s, i, n, a) = \big(s,\; p = \mathit{base}(a) + 8i,\; e = \mathit{base}(a) + 8n\big),$$

and the deoptimization map back is $i = (p - \mathit{base}(a))/8$.

Take $n = 10^6$, $a[i] = i$ and $\mathit{base}(a) = 4096$. The baseline loop reaches its threshold after 1000 iterations, at `L` with $i = 1000$ and $s = 0 + 1 + \dots + 999 = 499500$. The mapping gives $p = 4096 + 8000 = 12096$, $e = 4096 + 8000000 = 8004096$ and $s = 499500$, which satisfies the invariant. The optimized loop adds the remaining 999000 elements and returns $s = 499999500000$, which is $\sum_{i < 10^6} i$, the result of the baseline loop alone.

A wrong mapping, such as $p = \mathit{base}(a)$, also gives a state from which the optimized code runs, but not a related one: the loop would add the first 1000 elements twice and return $499999999500$.

## Classic examples

- **SELF-93.** When the system recompiles a method, the unoptimized frames of that method and of the methods inlined into it can be on the stack. The recompilation replaces them by one frame of the new optimized code, which continues at a *restart point* (Hölzle 1994, Section 5.4.1). This is OSR of several frames into one, the reverse of deoptimization of one frame into several.
- **The Jikes RVM.** Fink and Qian added OSR entry from baseline code to optimized code at back edges, with the prologue technique above, and also used it to defer the compilation of code that has never run: such code is replaced by an OSR exit.
- **Java and JavaScript engines.** The interpreter or baseline tier counts loop back edges and enters optimized code at the loop header. The optimized code leaves by deoptimization. Cooper and Torczon describe the general mechanism.
- **Formal treatments.** D'Elia and Demetrescu give a model in which OSR between any two versions of a program at matching points is correct, and show how common optimizations can carry the mapping along.

## Variations

- **Entry only at loop headers or at any point.** Loop headers are enough for long loops and keep the number of entry blocks small. Deoptimization needs exit at any guard, which is why exits are more general than entries.
- **A general entry or a one-shot version.** A general entry block reads the values from the old frame at run time, and the version serves every later transition at that header. The prologue technique of Fink and Qian makes a version for one transition, which can use the values as constants.
- **Many frames.** With inlining, one optimized frame stands for several baseline frames, so an OSR entry may need to merge frames and a deoptimization to split them.
- **Tracing systems.** A [tracing JIT compiler](/tracing-jit-compilation/) enters a compiled trace at a loop header by construction, which is a form of OSR entry with a trivial mapping.

## Pitfalls

- **Facts from before the loop.** When the method is compiled with an entry at the loop header, the code before the loop does not run in the new version. The optimizer must not use facts that only that code establishes, such as "`i` starts at 0, so it is never negative", unless the entry checks them or the mapping establishes them.
- **Missing live values.** The mapping needs every value that is live at the header, including values on the operand stack and objects that hold locks. Leaving one out breaks the relation.
- **A mapping that breaks the loop invariant.** The optimized loop relies on its invariant at the header. The mapping must produce a state that satisfies it, as the wrong mapping of the example shows.
- **Waiting for the compiler.** The loop keeps running in the baseline tier while the compiler works. The transfer must happen at the next visit of the header after the code is ready, not at an arbitrary point.
- **Thrashing.** If the optimized loop deoptimizes soon after entry and the counter triggers again, the method goes back and forth. Count the transitions and stop entering when they fail.

## Exercises

1. In the worked example, the optimized loop deoptimizes when $p = 4096 + 8 \cdot 500000$. Write the baseline state that deoptimization must build, and check that the baseline loop from it returns the same sum.
2. Prove that the prologue technique gives a correct OSR mapping, using the claim with $R$ the identity on bytecode states.
3. An optimizer has moved the computation of `n * 2` out of the loop into a register `m` before the loop. What must the OSR entry mapping do with `m`?
4. Give a loop for which entry at the header is correct, but entry in the middle of the loop body needs values that are not live at any variable, such as a partly computed expression on the operand stack.
5. Explain why OSR entry is rarely needed in a method that is called often with short loops, and what the system can do instead.

## References
