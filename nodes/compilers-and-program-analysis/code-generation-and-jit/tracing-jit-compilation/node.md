---
tag: G3F0E4
kind: technique
slug: tracing-jit-compilation
name: Tracing JIT compilation
aliases:
- trace-based compilation
- tracing JIT
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Records the operations of a hot loop path as a linear trace, optimizes it with guards for exits, and compiles it to machine code.
prereqs: [just-in-time-compilation, basic-block]
see_also: [meta-tracing, deoptimization, trace-scheduling, superblock-scheduling, on-stack-replacement, ball-larus-path-profiling, natural-loop, adaptive-optimization]
sources:
  - paper: doi:10.1145/349299.349303
    title: "Vasanth Bala, Evelyn Duesterwald and Sanjeev Banerjia, Dynamo: a transparent dynamic optimization system, PLDI 2000, 1-12"
    locator: the interpretation of native code, the selection of hot traces that start at targets of backward branches, the optimization of traces as straight-line fragments with exits, and the fragment cache with linked fragments
  - paper: doi:10.1145/1542476.1542528
    title: Andreas Gal, Brendan Eich, Mike Shaver, David Anderson, David Mandelin, Mohammad R. Haghighat, Blake Kaplan, Graydon Hoare, Boris Zbarsky, Jason Orendorff, Jesse Ruderman, Edwin W. Smith, Rick Reitmaier, Michael Bebenita, Mason Chang and Michael Franz, Trace-based just-in-time type specialization for dynamic languages, PLDI 2009, 465-478
    locator: TraceMonkey, the recording of loop traces in a JavaScript interpreter with type guards, side exits that restore the interpreter state, trace trees and nested trace trees
  - paper: doi:10.1145/1565824.1565827
    title: "Carl Friedrich Bolz, Antonio Cuni, Maciej Fijałkowski and Armin Rigo, Tracing the meta-level: PyPy's tracing JIT compiler, ICOOOLPS 2009, 18-25"
    locator: the summary of tracing JIT compilers at the start of the paper, before it applies tracing to an interpreter
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 14, Section 14.3 (hot-trace optimization)
  - book: isbn:9781558609105
    title: "James E. Smith and Ravi Nair, Virtual Machines: Versatile Platforms for Systems and Processes, Morgan Kaufmann, 2005"
    locator: the chapter on dynamic binary optimization, on traces, superblocks and their formation from profiles
---

A tracing JIT compiler compiles paths, not methods. It runs the program in an interpreter, counts how often the targets of backward branches are reached, and when a loop header becomes hot it *records* one iteration: it lets the interpreter run on and logs each operation that it executes, following calls into their bodies, until control comes back to the header. The log, called a *trace*, is a straight line of code. Each branch on the recorded path becomes a *guard* that checks that the same direction is taken again, and each guard has a *side exit* that hands the state back to the interpreter. The trace is easy to optimize, because it has no merges, and it is compiled to a loop of machine code. Dynamo did this for machine code in 2000, and TraceMonkey for JavaScript in 2009. A trace with exact side exits is equivalent to the interpreter on the paths it covers, and the interpreter handles all other paths.

## In plain words

In most programs the time goes into loops, and inside a loop the same few branches go the same way almost every time. A tracing compiler watches the program in an interpreter. When a loop has run a few times, it records what the next round of the loop actually does, step by step, as one long list without any branches.

Each point where the program chose a direction becomes a check: "the same way as last time?". The list is then turned into fast machine code that repeats the round. If a check fails, the fast code stops and gives the current values back to the interpreter, which goes on along the other branch. So the fast code is right on the path it recorded, and the interpreter does the rest.

## When it applies

- The program runs in an interpreter first, which can switch to a recording mode, or it is machine code that a system can interpret, as in Dynamo.
- The time goes into loops whose body takes the same path most of the time, so one or a few traces cover most of the work.
- The language is dynamic, so knowing the types of values on one path pays off: the trace records the types it saw and specializes each operation to them, behind type guards.
- The system can rebuild interpreter frames at a side exit, which is the same mechanism as [deoptimization](/deoptimization/).

## The template

### Finding and recording a trace

1. **Count.** The interpreter keeps a counter at each target of a backward branch, which is a loop header of a [natural loop](/natural-loop/) in structured code. When a counter reaches a threshold and no trace exists for the header, the interpreter starts recording.
2. **Record.** While it runs one iteration as usual, the interpreter appends each executed operation to the trace, in a simple intermediate form like [three-address code](/three-address-code/). When it executes a conditional branch and goes to $L_1$, it appends a guard that the condition has the same value, with a side exit to the other target. When an operation depends on a type, it appends a type guard. A call is not recorded as a call: the trace goes on in the body of the callee.
3. **Close or abort.** When control comes back to the header, the trace ends with a jump to its own start. If the recording runs too long, leaves the loop, or meets an operation that the recorder cannot handle, it aborts and the interpreter goes on.
4. **Optimize and compile.** The trace is one [basic block](/basic-block/) with exits, so forward passes such as constant folding, common subexpression elimination, type specialization and the removal of redundant guards are simple and fast. Invariant operations can be moved out by copying one iteration in front of the loop.
5. **Run.** The next time the interpreter reaches the header, it jumps into the compiled trace, which is an entry with a trivial state mapping. At a side exit, the trace writes the live values back into the interpreter frames listed in the exit's snapshot and the interpreter continues at the recorded program counter.

### Why a trace is equivalent on its paths

Let $\pi = (o_1, o_2, \dots, o_r)$ be the operations that the interpreter executed in the recorded iteration, from the header $h$ back to $h$, with each branch among them replaced by a guard. Write $\sigma \xrightarrow{o} \sigma'$ for one interpreter step on operation $o$. For each guard $g_j$ the recorder stores a snapshot: the program counter of the branch target that was not taken, and where each live interpreter value is held in the trace.

**Claim.** Let $\sigma$ be an interpreter state at $h$, and run the trace from the matching trace state. Then exactly one of these happens: (a) the interpreter from $\sigma$ follows $\pi$ for one whole iteration, and the trace reaches its loop back edge in the state that matches the interpreter's state at $h$ after that iteration; or (b) the interpreter leaves $\pi$ first at the branch of some guard $g_j$, and the trace takes the side exit of $g_j$, whose snapshot gives exactly the interpreter's state after that branch.

*Proof.* By induction on the position $t$ in the trace, keep the hypothesis $H_t$: if the interpreter from $\sigma$ has executed $o_1, \dots, o_t$, then after the trace has executed its first $t$ entries without exiting, the trace state matches the interpreter state. $H_0$ holds by the entry mapping. Assume $H_{t-1}$ and look at $o_t$. If it is not a branch and not a type-dependent operation, the trace entry performs the same operation on the same values, because it was recorded from that operation, so $H_t$ holds. If it is a branch whose recorded direction was $L_1$, the guard evaluates the same condition on the same values. If the condition has the recorded value, the interpreter also goes to $L_1$, which is the next operation $o_{t+1}$ of $\pi$, and the trace goes on: $H_t$ holds. Otherwise the interpreter goes to the other target, so it leaves $\pi$ here, and the trace exits at this guard; the snapshot names that target and the location of each live value, and by $H_{t-1}$ those values are the interpreter's values, so the interpreter state is rebuilt exactly. A type guard works the same way, with the type test in place of the condition. If no guard exits, then after $o_r$ the interpreter is back at $h$ and $H_r$ gives case (a). $\square$

By induction on the number of iterations, a run of the compiled loop is a run of the interpreter, cut into iterations along $\pi$, and ending in a side exit to the right state, so by the determinism of the interpreter the program has the same outcome as in the interpreter alone. Optimizations of the trace must keep the snapshots exact, which is the exactness invariant of [deoptimization](/deoptimization/): an optimization may change how a value is computed, but each snapshot must still give the value that the interpreter has at that guard.

### A worked example

In the notation of three-address code:

```
entry:  i = 0; s = 0; jump h
h:      c = i < n; br c body done
body:   t = i % 10; z = t == 0; br z rare common
rare:   s = s + 100; jump latch
common: s = s + i; jump latch
latch:  i = i + 1; jump h
done:   ret s
```

With $n = 100$ and a threshold of 2, the interpreter runs the iterations $i = 0$ and $i = 1$, then records the iteration $i = 2$, which takes the path through `common`. The trace is

```
loop:  c = i < n;   guard c ≠ 0, else exit to done with (i, s)
       t = i % 10;  z = t == 0;  guard z = 0, else exit to rare with (i, s)
       s = s + i;   i = i + 1;   jump loop
```

From $i = 3$ on, the trace runs. It completes 88 iterations, takes the side exit to `rare` 9 times, at $i = 10, 20, \dots, 90$, each time followed by one interpreted iteration and a new entry into the trace at `h`, and takes the exit to `done` once, at $i = 100$. That is $3 + 88 + 9 = 100$ iterations in all, and the result is $s = 5500$: the sum of the 90 values of $i$ that are not multiples of 10, which is $4950 - 450 = 4500$, plus $10 \times 100$. The interpreter alone gives the same 5500.

## Classic examples

- **Dynamo.** Dynamo interprets PA-RISC machine code, counts the targets of backward branches and the exits of existing fragments, and records the next path that runs from a hot target. It optimizes the path as a straight-line fragment, puts it in a fragment cache, and links fragments that exit into each other directly, so that control stays in the cache.
- **TraceMonkey.** The JavaScript engine of Firefox from 2009 recorded traces in its bytecode interpreter, with type guards on every value, and specialized the trace to the types it saw. A side exit that becomes hot starts a new trace from the exit, which grows a *trace tree* rooted at the loop header. An inner loop gets its own tree, and the outer trace calls it, which forms nested trace trees. Mozilla later moved to method-based compilers.
- **LuaJIT and PyPy.** LuaJIT 2 is a tracing JIT compiler for Lua. PyPy applies tracing to its interpreter for Python instead of to the Python program, which is [meta-tracing](/meta-tracing/).

## Variations

- **Trace trees and bridges.** When a side exit becomes hot, record a trace from it and link it to the exit, so that the second path is also compiled. The traces of one loop then form a tree rooted at the header.
- **Where traces start.** At targets of backward branches, at exits of existing traces, or at the entry of hot functions. Dynamo also starts at fragment exits.
- **Loop peeling on traces.** Copy the trace once and use the first copy as a preamble, so that invariant work and guards that hold for all iterations run only in the preamble.
- **Superblocks ahead of time.** A static compiler can form traces from a profile, as in [trace scheduling](/trace-scheduling/) and [superblock scheduling](/superblock-scheduling/), which are the ancestors of the idea. A path profile such as that of [Ball and Larus](/ball-larus-path-profiling/) can select them.

## Pitfalls

- **Exits that are not exact.** A side exit must rebuild every interpreter frame that is active at its guard, including the frames of inlined calls, with the right program counters. This is the same rule as for deoptimization.
- **Branchy loops.** If a loop body has many paths with similar frequency, a single trace exits often, and trace trees grow large. Method compilers handle such code better.
- **Trace explosion.** Every path through nested branches and calls is a separate trace, and code after a branch is copied into each of them. Limit the number and length of traces.
- **Recursion and long calls.** A trace follows calls into their bodies. Deep recursion or a very long callee makes the recording too long, so it must abort or stop at the call.
- **Assumptions from one iteration.** Everything that held in the recorded iteration, such as a type or a branch direction, is only a guess for the next one and needs a guard. A missing guard turns a guess into a wrong answer.
- **Speed claims.** Reports such as those for TraceMonkey and Dynamo are measurements on given programs and machines. Tracing helps loop-heavy code with stable paths and can be slower on other code.

## Exercises

1. In the worked example, the threshold is changed to 15. On which iteration is the trace recorded, which path does it take, and how many side exits happen?
2. Extend the claim to a trace that records a call to a function `f` and its body. What must the snapshot of a guard inside the body of `f` hold?
3. Show that removing the second of two identical guards in a trace keeps the snapshots exact, and give a case where removing a guard that is implied by an earlier one is wrong because the snapshot differs.
4. Design a trace tree for the worked example, with a bridge for the exit to `rare`. How many iterations then run in compiled code?
5. Why does a tracing compiler find loop-invariant code easily by peeling one iteration of the trace, and what kind of invariant code does it miss?

## References
