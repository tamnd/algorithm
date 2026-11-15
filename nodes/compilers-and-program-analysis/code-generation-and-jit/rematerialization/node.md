---
tag: CGBGCK
kind: technique
slug: rematerialization
name: Register rematerialization
aliases:
- remat
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Recomputes a spilled value that is cheap to compute, such as a constant, instead of reloading it from memory.
prereqs: [spill-code-placement]
see_also: [live-range-splitting, chaitin-register-allocation, briggs-optimistic-coloring, conservative-coalescing, sparse-conditional-constant-propagation, static-single-assignment-form, loop-invariant-code-motion, common-subexpression-elimination]
sources:
  - paper: doi:10.1145/143095.143143
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Rematerialization, Proceedings of the ACM SIGPLAN 1992 Conference on Programming Language Design and Implementation (PLDI), SIGPLAN Notices 27(7), 1992, 311-321
    locator: the tags that mark values which can be recomputed, their propagation over SSA form, and the splitting of live ranges with mixed tags
  - paper: doi:10.1145/177492.177575
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Improvements to graph coloring register allocation, ACM Transactions on Programming Languages and Systems 16(3), 1994, 428-455
    locator: register rematerialization as one of the improvements to the Chaitin allocator, with its effect on spill costs
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: spill everywhere and the recomputation of values whose operands are always available
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), spill costs and rematerialization
---

Register rematerialization recomputes a spilled value instead of loading it back from memory. When an allocator spills a value whose definition is cheap and whose operands are available at every use, such as a constant, the address of a global variable, or an offset from the frame pointer, it can put a copy of the defining instruction before each use. Then the value needs no store, no load and no spill slot, and the original definition often becomes dead. Briggs, Cooper and Torczon (1992) gave a general method: they mark each value in [SSA form](/static-single-assignment-form/) with a tag that says if and how it can be recomputed, and they split the live ranges that mix values of different tags.

## In plain words

When there are too few registers, the compiler must put some value aside and get it back later. The usual way is to write it to memory and read it back. But some values are so easy to make that making them again is cheaper than reading them: a fixed number, or the address of a fixed place. For such a value the compiler does not save it at all. Just before each place that needs it, it makes the value again with one cheap instruction. This frees the register in between, as a spill does, but without any memory traffic.

## When it applies

- The allocator has decided to spill a value $x$ ([spill code placement](/spill-code-placement/)).
- Every definition of $x$ that reaches a use is the same instruction, for example `x = 100`, and that instruction can run at each use point with the same result: its operands are constants, or registers that are reserved and never change, such as the frame pointer.
- The instruction has no side effect and costs no more than a load. A load from memory that never changes, such as a table of constants, also qualifies.
- A value computed from other names, such as `x = p + 1`, does not qualify in general: at a later use, $p$ may be dead or may have changed, and keeping $p$ live would only move the register pressure to $p$.

## The template

1. **Tag the values.** On SSA form, give each name a tag from a small lattice: *top* (not yet known), *inst* (always defined by one cheap instruction with available operands, which the tag records), or *bottom* (not rematerializable). A constant or an address gets *inst*. Other computed values get *bottom*. A $\phi$-function gets the meet of the tags of its operands: two equal *inst* tags give *inst*, and different tags give *bottom*. Propagate to a fixed point, as in [sparse conditional constant propagation](/sparse-conditional-constant-propagation/).
2. **Split mixed live ranges.** A $\phi$-function whose operands have different tags joins a rematerializable value with one that is not. Put copies at that $\phi$-function, so that the parts with an *inst* tag become live ranges of their own ([live range splitting](/live-range-splitting/)).
3. **Lower the spill cost.** The spill cost of a rematerializable live range is the cost of the recomputations, with no store, instead of the cost of loads and stores. The allocator then prefers to spill these values.
4. **Rewrite on spill.** For a spilled rematerializable value, put a copy of its defining instruction before each use, into a new short temporary, and add no store. If the original definition then has no use, dead code elimination removes it.
5. **Remove extra copies.** Copies added in step 2 that turned out not to help are merged away by [conservative coalescing](/conservative-coalescing/).

## Classic examples

**A constant, with two registers.** In this program the constant $c$ is live from its definition to the last addition:

```
L0:
  c = 100
  a = p + 1
  b = a * p
  d = b + a
  e = d + c
  ret e
```

Just after `a = p + 1`, the names $a$, $c$ and $p$ are live, so the interference graph has a triangle, and with $k = 2$ one of them must be spilled; [optimistic coloring](/briggs-optimistic-coloring/) spills $c$. Spill everywhere adds a store `mem.c = c1` after `c1 = 100` and a load `c2 = mem.c` before the addition. Register rematerialization instead drops `c = 100` and writes `c2 = 100` just before `e = d + c2`. The result needs no store, no load and no slot. A script checked that both rewritten programs give the outcome of the original for $p$ from $-50$ to $49$, and that both interference graphs are 2-colorable.

**An address.** On a machine where `x = fp + 16` computes the address of a local array from the frame pointer `fp`, which never changes inside the function, $x$ can be rematerialized at each use. The same holds for the address of a global variable, which is a constant known at link time.

**A mixed live range.** After a join, `x = phi(0, y)`, where $y$ is computed by a multiplication. The tag of $x$ is *bottom*, because one input is a constant and the other is not. Splitting puts a copy on the edge from the constant, so that the constant part is a separate live range that can be rematerialized, and only the part that holds $y$ needs a real spill.

**Outside compilers.** The same trade of recomputation for storage appears in [gradient checkpointing](/gradient-checkpointing/), which recomputes the activations of a neural network during the backward pass instead of keeping them all in memory.

## Variations

- **Never-killed values.** The simplest form recomputes only values whose live range has a single defining instruction with constant operands. Chaitin's allocator already handled values of this kind ([Chaitin's allocator](/chaitin-register-allocation/)).
- **Tag propagation with splitting.** Briggs, Cooper and Torczon (1992) propagate tags over SSA form and split live ranges where tags differ, so that the rematerializable parts of a live range are recovered too.
- **Partial rematerialization.** If $x = y + 1$ and $y$ is live and in a register at a use of $x$ anyway, $x$ can be recomputed there from $y$. This saves the load, but the check must be done for each use.
- **In linear scan.** The rule does not depend on graph coloring. A [linear scan](/linear-scan-register-allocation/) allocator that spills an interval holding a constant or an address can recompute it before each use in the same way.

## Pitfalls

- **Operands must be available.** A recomputation reads its operands at the use point. If an operand is dead there, or has a different value, the result is wrong, or a new long live range appears. Only constants and reserved registers are safe in general.
- **Side effects.** An instruction that writes memory, can trap, or reads memory that can change must not be repeated.
- **Cost.** Rematerialization is a gain only if the recomputation costs no more than a load. A long expression is not cheap, and a recomputation in a loop runs once per iteration.
- **It undoes other passes.** [Loop invariant code motion](/loop-invariant-code-motion/) and [common subexpression elimination](/common-subexpression-elimination/) remove recomputations and make values live longer. Register rematerialization puts some of the recomputations back, where registers are short. This is intended, but the two passes must agree on which values are cheap.
- **Mixed tags.** Treating a live range as rematerializable when only some of its definitions are cheap gives wrong code on the other paths. Split first.

## Exercises

1. Why does a rematerialized value need no store?

   *Answer.* A store keeps the value so that a load can get it back. A rematerialized value is made again from its defining instruction at each use, so nothing reads the slot, and the slot and the store are not needed.

2. A value `x = p + 1` is spilled. Under what condition can it be recomputed at a use, and why is it not rematerializable in general?

   *Answer.* It can be recomputed at a use where $p$ is live, unchanged since the definition of $x$, and in a register. In general $p$ is dead or redefined at the use, and keeping $p$ live only moves the register pressure from $x$ to $p$.

3. In the constant example, why is spill everywhere worse than recomputation, although both make the graph 2-colorable?

   *Answer.* Spill everywhere adds one store and one load, two memory operations, and a slot in the frame. Recomputation adds one instruction `c2 = 100` and removes `c = 100`, so the instruction count does not change and no memory is used.

4. Give the tag of `x = phi(5, 5)` and of `x = phi(5, 6)`.

   *Answer.* `phi(5, 5)` gets the tag *inst* with the instruction `x = 5`, since both inputs are the same instruction. `phi(5, 6)` gets *bottom*: the two inputs are different instructions, so no single instruction recomputes $x$. Splitting at the $\phi$-function makes the two constants separate live ranges, and each one can be rematerialized.

## References
