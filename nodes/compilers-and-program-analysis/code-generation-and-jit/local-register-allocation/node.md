---
tag: A84DF7
kind: algorithm
slug: local-register-allocation
name: Local register allocation
aliases:
- bottom-up local allocation
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Allocates registers in one basic block in order, and when none is free spills the value whose next use is farthest away.
solves: [register-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of instructions of the block, k: the number of registers}
  time: {worst: O(n k)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1966
  people: [Laszlo A. Belady]
  note: "Belady gave the furthest-next-use rule for paging in 1966. Compilers use the same rule for the registers of a basic block; Farach-Colton and Liberatore showed in 2000 that the problem with dirty values is NP-hard."
prereqs: [basic-block, three-address-code, belady-algorithm]
see_also: [belady-optimality, register-allocation-problem, spill-code-placement, linear-scan-register-allocation, chaitin-register-allocation, rematerialization, live-variable-analysis, sethi-ullman-numbering]
sources:
  - paper: doi:10.1147/sj.52.0078
    title: L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2), 1966, 78-101
    locator: the replacement rule that evicts the page whose next reference is furthest in the future
  - paper: doi:10.1006/jagm.2000.1095
    title: Martin Farach-Colton and Vincenzo Liberatore, On local register allocation, Journal of Algorithms 37(1), 2000, 37-65
    locator: the model with clean and dirty values, the NP-hardness of the problem with store costs, and the approximation algorithm
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), local register allocation, the top-down and the bottom-up local allocators, and the remark on clean and dirty values
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 8 (Code Generation), the simple code generator for a basic block and its function getReg
---

Local register allocation assigns machine registers to the values of one [basic block](/basic-block/). The bottom-up allocator walks the block from the first instruction to the last. It gives each operand and each result a register, and when no register is free, it frees the register whose value is needed again furthest in the future. This is Belady's rule for [paging](/belady-algorithm/), applied to registers. When every value has a copy in memory, the rule gives the least number of loads, by [the optimality of Belady's rule](/belady-optimality/). When some values are *dirty*, so that freeing them costs a store, the rule can lose, and the exact problem is NP-hard.

## In plain words

A block of code uses more values than the machine has registers. The allocator walks through the block in order. Before an instruction runs, its operands must be in registers. If an operand is not there, the allocator loads it from memory. The result of the instruction also needs a register.

When all registers are full, one value must go. The allocator looks ahead in the block and chooses the value that will be needed again last. That value would stay unused for the longest time, so a register spent on it is the most wasted.

If the value that goes has no copy in memory yet, the allocator must save it first. This extra store is the weak spot of the rule. A value with a copy in memory is cheaper to throw out, and the rule does not look at that.

## The problem

The input is one block of the [toy IR](/three-address-code/) and a number $k \ge 2$ of registers $r_0, \ldots, r_{k-1}$. The block has `const`, `copy` and `op` instructions and ends with `ret`. Each name $x$ has a memory slot `mem.x`. The parameters start in memory. An `op` instruction reads its operands from registers and writes its result to a register.

A value in a register is *clean* if memory holds the same value, and *dirty* if not. A parameter that was loaded is clean. A value that an instruction computes is dirty until it is stored. A load costs 1, and a store costs 1. In the *clean model*, a store costs 0, which is the same as saying that every value is clean.

The output is a block that uses only the registers and the memory slots, computes the same result, and has the least number of loads and stores. The allocation is on demand: it loads a value only when an instruction needs it, and frees a register only when it needs one.

## The algorithm

The block is first read backwards to find, for each value and each point, the next use of the value. A value with no later use is *dead*.

```pseudo id=main
ALLOCATE(block, k)
L1  for each instruction x ← a op b of the block, in order do
L2      for each operand u that is not in a register do
L3          r ← GETREG(pinned = the operands of this instruction that are already in registers); emit r ← mem.u; u is clean
L4      for each operand u that is dead after this instruction do free the register of u
L5      r ← GETREG(pinned = none); emit r ← the operation, with the registers of the operands
L6      put x in r; x is dirty; if x is dead, free r

GETREG(pinned)
L7  if some register is free then return it
L8  v ← the value in a register, not pinned, whose next use is furthest away
L9  if v is dirty then emit mem.v ← the register of v      ▷ a store
L10 free the register of v and return it
```

The ret is an instruction with one operand and no result. Line L5 may reuse the register of an operand, even of a live one, because the instruction reads its operands before it writes its result. A pinned operand is never freed at line L3, so both operands of an instruction are in registers at the same time.

## Example

Take this block and $k = 2$:

```
# params: a, b, c, d
entry:
  t = a + b
  u = c + d
  v = t * u
  w = v - a
  ret w
```

The allocator emits:

```
# params: mem.a, mem.b, mem.c, mem.d
entry:
  r0 = mem.a
  r1 = mem.b
  r1 = r0 + r1
  r0 = mem.c
  mem.t = r1
  r1 = mem.d
  r0 = r0 + r1
  r1 = mem.t
  r0 = r1 * r0
  r1 = mem.a
  r0 = r0 - r1
  ret r0
```

After the first instruction, $b$ is dead, so $t$ takes its register, and $r_0$ still holds $a$. To load $c$, the allocator compares $a$, needed at the fourth instruction, with $t$, needed at the third, and frees $a$. It is clean, so this costs nothing now. To load $d$, the only register that is not pinned holds $t$, which is dirty, so it is stored first. The cost is six loads and one store, 7 in total. A brute force search over all choices also finds 7. With $k = 3$, the allocator frees the clean $a$ to load $d$, and the cost is 5 loads.

For $a = 1$, $b = 2$, $c = 3$ and $d = 4$, both blocks return 20.

## Correctness

The output computes the same values as the block. Each instruction reads its operands from the registers that hold them, a pinned operand is never freed before its instruction runs, and a value is loaded only from a memory slot that holds it, because a dirty value is stored before its register is freed.

The clean model is a case of [demand paging](/demand-paging/). The values are pages, the registers are the cache, and each use of a value is a request. A pinned operand gets one more request just after the request for the other operand, so the furthest-next-request rule never evicts it, and each definition is a request for a new page, which every schedule must load. Under this map the allocator is exactly LFD, and its cost is the cost of LFD minus the number of definitions, the same constant for every allocation. So [the optimality of Belady's rule](/belady-optimality/) gives the least number of loads.

With dirty values, the rule can lose. With $k = 3$ and the block `t = b + 1`, `u = b + t`, `u = u * a`, `t = b * t`, `v = t * u`, `ret v`, the allocator must free a register for $a$ while $u$ is pinned. The next uses of $b$ and $t$ are the two operands of the fourth instruction, and $t$ comes second, so the rule frees the dirty $t$: a store and a load later, for a total of 4. Freeing the clean $b$ costs one load, for a total of 3. The proof file gives both proofs.

## Complexity

Reading the block backwards gives, for each use, the position of the next use of the same value, in $O(n)$ time. Then each step of ALLOCATE tests at most $k$ registers at lines L7 and L8, so the time is $O(n k)$ in the worst case. A priority queue of the registers by next use brings this to $O(n \log k)$, but $k$ is small, so a scan is the usual choice. The next-use table takes $\Theta(n)$ space. The reference code keeps a copy of the table for each step, for clarity.

## Properties

- **Optimal for clean values.** In the clean model, with equal load costs, no allocation of the block has fewer loads.
- **Not optimal with stores.** With dirty values the exact problem is NP-hard (Farach-Colton and Liberatore), and the rule is only a heuristic.
- **Offline.** The rule looks at future uses, which is fine in a compiler, because the whole block is known.
- **Local.** It knows nothing about other blocks. At the end of a block, the values that are live out must go back to memory or to agreed registers.

## Variants and improvements

- **Clean first.** Among the values whose next use is far away, prefer a clean one. This fixes the counterexample, but it can lose in other blocks. Farach-Colton and Liberatore give an algorithm whose cost is within a constant factor of the optimum.
- **Top-down allocation.** Count the uses of each value in the block, give registers to the most used values for the whole block, and keep a few registers free for the rest. It is simpler and often worse.
- **Rematerialization.** A constant or a value that is cheap to compute again is always clean: instead of a reload, the allocator can [recompute it](/rematerialization/).
- **Global allocators.** [Linear scan](/linear-scan-register-allocation/) uses a similar furthest-end rule over a whole function, and [graph coloring](/chaitin-register-allocation/) works on the interference of live ranges.
- **Expression trees.** For a single tree without shared values, the [Sethi-Ullman numbering](/sethi-ullman-numbering/) chooses an evaluation order that needs the fewest registers.

## When to use it

Use it in a fast compiler or a JIT, where a global allocator is too slow, and in the back end of a simple code generator for straight-line code. It is also the inner step of some global allocators, which first fix the values that live across blocks and then allocate each block on its own. For code with many dirty values and expensive stores, add the clean-first rule or a cost-aware search.

## Pitfalls

- **Freeing a pinned operand.** If the load of the second operand frees the register of the first, the instruction cannot run. Pin the operands of the current instruction.
- **Forgetting the store.** A dirty value must be stored before its register is reused, or a later reload reads an old value.
- **Reusing a slot too early.** If two values of the same name share one memory slot, the slot of the old value must not be needed after the new one is stored. In the toy IR this holds, because the new definition comes after the last use of the old value.
- **Dead values.** A value with no later use should free its register at once. Belady's rule evicts it first anyway, but code that keeps dead values can store them for nothing.
- **"Optimal" for the wrong model.** The optimality theorem counts loads with clean values. With stores, or with loads of different costs, it no longer holds.

## Implementations

## History

Belady studied replacement algorithms for virtual memory in 1966 and gave the rule that evicts the page whose next use is furthest in the future. Compiler textbooks use the same rule for the bottom-up local allocator. Its optimality for paging was proved later; the [optimality page](/belady-optimality/) gives the history. Farach-Colton and Liberatore studied local register allocation with clean and dirty values in 2000. They proved that the problem with store costs is NP-hard and gave an approximation algorithm.

## References
