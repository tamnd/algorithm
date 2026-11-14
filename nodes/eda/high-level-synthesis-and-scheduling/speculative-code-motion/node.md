---
tag: 49T964
kind: technique
slug: speculative-code-motion
name: Speculative code motion in high-level synthesis
aliases:
- SPARK code motion
- trailblazing
area: eda/high-level-synthesis-and-scheduling
level: research
summary: Moves operations across branches and executes them before the condition is known, as in the SPARK synthesizer, to shorten the schedule of control-heavy code.
prereqs: [control-data-flow-graph, basic-block]
see_also: [trace-scheduling, path-based-scheduling, operation-chaining, loop-invariant-code-motion, partial-redundancy-elimination, dominator-tree, phi-function, resource-binding]
sources:
  - paper: "Sumit Gupta, Nikil Dutt, Rajesh Gupta and Alexandru Nicolau, SPARK: a high-level synthesis framework for applying parallelizing compiler transformations, Proceedings of the International Conference on VLSI Design, 461 to 466, 2003"
    locator: the SPARK framework, its hierarchical task graph and the code motions applied during scheduling
  - paper: doi:10.1109/TCAD.2003.822099
    title: Sumit Gupta, Nicolae Savoiu, Nikil Dutt, Rajesh Gupta and Alexandru Nicolau, Using global code motions to improve the quality of results for high-level synthesis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 23(2), 302 to 311, 2004
    locator: speculation, reverse speculation, early condition execution and conditional speculation, and their effect on cycles, controller size and area
---

Speculative code motion moves an operation out of a branch of an if/else and above the condition, so that the hardware computes it before it knows whether the result is needed. In [high-level synthesis](/high-level-synthesis/), units that sit idle in early control steps can then do useful work, and the path through the branch gets shorter. If the other branch is taken, the result is simply not used. The price is an extra register for the result, a multiplexer that selects between the speculated values, and the energy of the operations whose results are thrown away. The SPARK synthesizer of Gupta, Dutt, Gupta and Nicolau (2003) applies a family of such moves during scheduling: speculation above a condition, reverse speculation into the branches below it, early condition execution, and conditional speculation into the arms of an earlier branch. To move operations over large regions of code quickly, SPARK uses the hierarchical code motion of Nicolau and Novack (1993) on its hierarchical task graph. That is one method among several; [trace scheduling](/trace-scheduling/) and percolation scheduling in compilers move code across branches in other ways.

## In plain words

Suppose a circuit must first check a condition and then do one of two adds, and the check takes a while. The adder is free while the check runs. So do both adds early, keep both results, and when the check is done, just pick the right one. You spend an extra add and an extra place to keep a value, and in return you save the time of the add after the check. The method is safe only when the early work cannot cause harm: it must not write to memory, and it must not overwrite a value that the other path still needs.

## When it applies

It applies to control-heavy code, such as decoders, parsers and image filters with many tests on the data, where the critical path runs through conditions and the units are idle in the steps that compute them. It pays when the time saved on the branch is worth more than the extra registers, multiplexers and energy. It is a transformation of the [control and data flow graph](/control-data-flow-graph/), so any scheduler can follow it, but it works best when the scheduler applies it as it goes and knows which units are free in each step.

An operation $v$ can move from a branch arm above the condition $c$ only when

- it has no side effect: no store, no output, no call with effects, and no operation that can trap, such as a load from a possibly invalid address or a divide by a value that can be zero;
- its operands are ready above $c$, which may require moving or copying the operations that produce them;
- its result does not overwrite a value that is live on the other path. If it does, give the result a new name and copy it back on the original path, which is what SPARK does with renaming.

## The template

1. **Build the region.** Take a region of the CDFG with its branches, in SPARK a hierarchical task graph whose nodes are basic blocks, if/else nodes and loop nodes.
2. **Schedule step by step.** Run a list scheduler over the steps of the region. In each step, collect the operations that are ready, including operations from inside later branches whose operands are available.
3. **Choose moves.** For a free unit in the current step, pick an operation by priority, usually its distance to the end of the region on the longest path. If it lies below a condition, apply the move that brings it here: speculation if it is in an arm of a later branch, and conditional speculation if the current step lies inside an arm and the operation sits after the join, in which case copy it into each arm.
4. **Rename.** Give a speculated result a new register, and add a copy, or a multiplexer selected by the condition, where the original operation was.
5. **Clean up.** Remove copies that became dead, and merge the arms of a branch whose operations all moved out. Reverse speculation moves operations down into the arms of a branch when only one arm uses them, which frees units in the steps above.
6. **Early condition execution.** Move the computation of a condition as early as its operands allow, so that the branch is decided early and less speculation is needed.

## Classic examples

**Two adds after a compare.** Take the code

```
t = p + q
c = t > 0
if (c) x = a + b; else x = a - b
y = x + e
```

with two ALUs, one step per operation and no chaining. Without code motion, $t$, $c$, $x$ and $y$ form a chain, and the schedule takes 4 steps on each path, with one ALU idle in each step. With speculation, $x_1 = a + b$ runs in step 1 beside $t$, and $x_2 = a - b$ in step 2 beside $c$. In step 3 a multiplexer in front of the ALU selects $x_1$ or $x_2$ by $c$ and $y$ is computed, so the schedule takes 3 steps, if the multiplexer delay fits in the step with the add. The cost is one more ALU operation per run, one more register, since $x_1$ and $x_2$ are both live in step 2, and the multiplexer. A third ALU does not help here: $t$, $c$ and $y$ still form a chain of 3 steps.

**Conditional speculation.** An operation after the join, such as $y = x + e$ above, cannot move above the branch, since $x$ is not known there. It can be copied into both arms, $y = (a + b) + e$ in one and $(a - b) + e$ in the other, where each copy can use a unit that is free in its arm. The code grows, but each path can get shorter.

**Reverse speculation.** An operation before an if/else whose result only one arm uses can move down into that arm. It then runs only on that path, and it frees a unit in the step before the branch for an operation on the critical path.

## Variations

- **Trace scheduling and percolation scheduling.** In compilers, [trace scheduling](/trace-scheduling/) schedules the most likely path as one block and adds repair code on the other paths. Percolation scheduling moves operations one step at a time by a small set of local rules. SPARK takes its moves from this line of work.
- **Path-based scheduling.** [Path-based scheduling](/path-based-scheduling/) keeps the order of operations on each path fixed and chooses where to cut it into states. Code motion before it relaxes the fixed order.
- **Code motion without speculation.** [Loop invariant code motion](/loop-invariant-code-motion/) and [partial redundancy elimination](/partial-redundancy-elimination/) move code only where it runs on every path that reaches the original place, so they never compute a value that is not needed. Speculation drops that rule on purpose.
- **Predication.** Instead of moving operations, compute both arms and select by the condition everywhere. This is speculation of all operations of both arms at once.
- **Dynamic renaming.** Rename results only when a move needs it, to keep the number of registers low.

## Pitfalls

- **Side effects.** Never speculate a store, an output or a load that may be out of range. In hardware, a speculated load from a memory can also take a port that a non-speculated load needs.
- **Register and multiplexer cost.** Each speculated value needs a register until the condition is known and a multiplexer input. Gupta and coauthors report the effect of each move on the area and the controller as well as on the cycles. Measure the area, not only the steps.
- **Energy.** Operations whose results are discarded still switch. For designs under a power limit, weigh the steps saved against the energy of the wasted operations.
- **Longer clock.** The multiplexers on the moved values add delay, which may break [chained](/operation-chaining/) paths that fit before.
- **Code growth.** Conditional speculation copies operations into each arm. Applied without a limit, it can grow the code and the controller faster than it shortens the schedule.
- **Live values on the other path.** Moving an operation that writes a variable that the other path reads, without renaming, silently changes the result of that path.

## Exercises

1. In the example with two ALUs, write the schedule with speculation of $x_1$ and $x_2$ and list the registers live at the end of each step.
2. The first arm is taken with probability $\pi$. Only its add is speculated, and this saves one step on the first path only. Give the expected number of steps saved and the expected number of wasted adds per run.
3. Show an example where speculating an operation makes the schedule longer, because it takes a unit that an operation on the critical path needs.
4. Explain why a divide cannot be speculated above the test `if (d != 0)` without a change, and give the change that makes it safe.

## References
