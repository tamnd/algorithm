---
tag: AKP7YG
kind: technique
slug: spill-code-placement
name: Spill code placement
aliases:
- spill code insertion
- register spilling
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Keeps a value in memory and inserts stores after its definitions and loads before its uses when it cannot have a register.
prereqs: [register-allocation-problem, chaitin-register-allocation]
see_also: [live-range-splitting, rematerialization, briggs-optimistic-coloring, iterated-register-coalescing, linear-scan-register-allocation, belady-algorithm, critical-edge-splitting, profile-guided-optimization]
sources:
  - paper: doi:10.1145/800230.806984
    title: Gregory J. Chaitin, Register allocation and spilling via graph coloring, Proceedings of the SIGPLAN '82 Symposium on Compiler Construction, SIGPLAN Notices 17(6), 1982, 98-105
    locator: spill everywhere, the spill cost estimate, and the rebuild of the graph after spill code is added
  - paper: doi:10.1145/177492.177575
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Improvements to graph coloring register allocation, ACM Transactions on Programming Languages and Systems 16(3), 1994, 428-455
    locator: spill decisions in the optimistic allocator and the cheaper spill code given by rematerialization
  - paper: doi:10.1145/1254766.1254782
    title: Florent Bouchez, Alain Darte and Fabrice Rastello, On the complexity of spill everywhere under SSA form, Proceedings of LCTES 2007, ACM, 2007
    locator: the complexity of choosing which values to spill everywhere, which stays NP-complete under SSA form in general
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), spill costs, spill code and the placement of loads and stores
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation), the rewrite of the program for actual spills
---

Spill code placement decides where the loads and stores of a spilled value go. When an allocator cannot give a value a register for its whole life, it keeps the value in a memory slot, the *spill slot*, and adds a store that copies it from a register to the slot and a load that copies it back before it is used. The simplest rule, *spill everywhere* from Chaitin's allocator, puts a store after every definition and a load before every use. It is always correct, but it can add far more memory traffic than needed, and a load right after a store may not even lower the register pressure. Better placement keeps the value in a register where registers are free, puts it in memory only across the part of the program where too many values are live, and puts the loads and stores at the points that run least often.

## In plain words

When there are not enough registers, some value has to wait in memory. The compiler then writes it to memory and reads it back later. The easy way is to write it each time it is made and read it each time it is needed. That works, but it wastes time: if the value is needed twice in a row with plenty of free registers between, one read is enough, and if the shortage is only in one small part of the program, the value only needs to be in memory there. Reads and writes inside a loop run many times, so it pays to move them before or after the loop. Spill code placement is the work of putting these reads and writes in the cheapest places that still keep the program correct.

## When it applies

- An allocator has decided to spill a value $x$: [Chaitin's allocator](/chaitin-register-allocation/), [optimistic coloring](/briggs-optimistic-coloring/), [linear scan](/linear-scan-register-allocation/) or a local allocator.
- The machine computes only on registers, as in the toy IR, so each use of $x$ needs $x$ in some register at that point, and each definition writes $x$ to a register first.
- Memory and registers can be moved between with a store `mem.x = t` and a load `t = mem.x`. A load costs more than an instruction on registers, and its cost is multiplied by how often the point runs.

## The template

Fix a spilled name $x$ with the slot `mem.x`. A *high-pressure point* is a point where more than $k$ values would be live if $x$ were kept in a register.

1. **Spill everywhere.** After each definition of $x$, store it; before each instruction that reads $x$, load it into a new short temporary. This is correct, by the spill lemma in the proof file of [Chaitin's allocator](/chaitin-register-allocation/): at each read, the slot holds the value of $x$ that the original program would read.
2. **Keep the register where it is free.** If a use of $x$ follows its definition, or an earlier load, in the same block with no high-pressure point between, use the register directly and drop the load. In the same way, several uses close together can share one load.
3. **Store only when needed.** A store is needed only if the slot does not already hold the current value. A value that was just loaded from its slot, or a parameter that arrives in its slot, needs no store. A value that is never redefined needs one store after its only definition.
4. **Move the code to cold points.** The value must be in memory across each high-pressure region it is live in. Put the store on the edges into the region and the load on the edges out of it, and choose, among the correct points, those with the lowest execution frequency. Loop nests or [profile data](/profile-guided-optimization/) give the frequencies.
5. **Split critical edges.** A load or store that belongs on an edge from a block with several successors to a block with several predecessors needs a new block on that edge ([critical edge splitting](/critical-edge-splitting/)).
6. **Rebuild.** In a graph-coloring allocator, the spill code changes liveness, so the interference graph is built again.

Steps 2 to 4 keep $x$ in a register over longer stretches, so they must keep each stretch free of high-pressure points. Otherwise the allocator will have to spill again.

## Classic examples

**One block, two registers.** The program from the page [register allocation problem](/register-allocation-problem/) is:

```
L0:
  a = p + 1
  b = p + 2
  c = a + b
  d = a * c
  e = b * d
  ret e
```

Just after `c = a + b`, the names $a$, $b$ and $c$ are all live, so with $k = 2$ one of them goes to memory. Spilling $b$ everywhere gives one store and two loads:

```
  a = p + 1
  b1 = p + 2
  mem.b = b1
  b2 = mem.b
  c = a + b2
  d = a * c
  b3 = mem.b
  e = b3 * d
```

Step 2 drops the load of `b2`: between the definition of $b$ and its first use, only $a$ and $b$ are live. The result has one store and one load, which is the least possible:

```
  a = p + 1
  b = p + 2
  mem.b = b
  c = a + b
  d = a * c
  b2 = mem.b
  e = b2 * d
```

A script checked that both programs give the outcome of the original for $p$ from $-50$ to $49$, and that both interference graphs are 2-colorable. Spilling $c$ everywhere does not help at all: `c1 = a + b; mem.c = c1; c2 = mem.c; d = a * c2` still has $a$, $b$ and `c2` live together. Chaitin's allocator, which uses spill everywhere, ends with 3 stores and 5 loads on this program.

**A value used in a loop.** Let $x$ be defined before a loop, read in every iteration, and not redefined. If the high pressure is only after the loop, spill everywhere loads $x$ in every iteration, and the cost grows with the number of iterations. Keeping $x$ in its register through the loop and storing it once on the exit edge costs one store, run once. This is a case where placement and [live range splitting](/live-range-splitting/) meet: $x$ gets a register in the loop and a slot after it.

**A parameter.** In the toy IR, a parameter $p$ arrives in its slot `mem.p`, and the entry block loads it. If $p$ is spilled everywhere, the load is followed by a store of the same value to the same slot, which can be deleted.

**A constant.** If $x$ is set by `x = 7` and never changed, no store and no slot are needed: each load can be replaced by `x = 7` itself ([rematerialization](/rematerialization/)).

## Variations

- **Spill everywhere.** Chaitin (1982). It makes each spilled value a set of tiny live ranges, which helps the coloring, at the cost of many memory operations. Bouchez, Darte and Rastello (2007) proved that choosing which values to spill everywhere at least cost is NP-complete in general, even under SSA form.
- **Local cleanup.** After spill everywhere, a pass over each block removes loads whose value is still in a register and stores whose slot is already up to date.
- **Interval splitting in linear scan.** [Linear scan](/linear-scan-register-allocation/) can split an interval at the point where it runs out of registers and place a store there and a load before the next use.
- **Farthest next use.** Inside one block, when a register must be freed, evicting the value whose next use is farthest is the rule of [Belady's algorithm](/belady-algorithm/) for caches. It minimizes the number of loads in a block, but stores and the cost of different values make the register problem harder than paging.
- **Spill slot sharing.** Two spilled values that are never live at the same time can share one slot, by a coloring of the slots that works like register allocation.
- **Recomputation.** [Rematerialization](/rematerialization/) replaces the loads of a cheap value by its computation.

## Pitfalls

- **A load right after a store gains nothing.** If the store and the load are next to each other, the value is still live across the same points, under another name. Choose the value to spill by where it can stay in memory, not only by its cost.
- **Do not move a load above a redefinition.** A load must read the slot after the last store that matches the definition it stands for.
- **Every path needs the value.** When loads move to edges, every path from a store to a use must pass a load, and every path from a definition to a load must pass a store.
- **Critical edges.** A load placed at the end of a block with two successors runs on both paths. Split the edge to put it on one path only.
- **Spill temporaries.** The short temporaries of spill code must never be spilled again; give them an infinite spill cost.
- **Frequency counts.** A load in a loop counts once per iteration. Ignoring this can make a placement with fewer instructions run slower.

## Exercises

1. In the one-block example, spill $a$ everywhere instead of $b$. How many stores and loads does it need, and is the interference graph 2-colorable?

   *Answer.* $a$ is read by `c = a + b` and `d = a * c`, so spill everywhere needs one store and two loads, into `a2` before `c = a2 + b` and into `a3` before `d = a3 * c`. Just after the load of `a3`, the names `a3`, $b$ and $c$ are live, since $b$ is read later by `e = b * d`. So three names are live together and the graph has a triangle. Spilling $a$ does not solve the problem; $b$ is the right choice.

2. A value $x$ is defined once and read in five places in one block, with no high-pressure point between the definition and the last read. How much spill code does $x$ need?

   *Answer.* None. With no high-pressure point in its live range, $x$ can stay in a register, and spilling it only adds cost.

3. Why can the store be dropped for a spilled parameter of the toy IR?

   *Answer.* The parameter arrives in `mem.p` and is never redefined before the entry load. After the load, the register and the slot hold the same value, so storing it again writes the value the slot already has.

4. A value is defined in block $A$ and read in block $D$. The path goes $A \to B \to D$ and $A \to C \to D$, and only $B$ has high pressure. Where should the store and the load go?

   *Answer.* The value must be in memory across $B$ only. Store it on the edge $A \to B$ and load it on the edge $B \to D$. Along $A \to C \to D$ it can stay in its register. If the edges are critical, split them first. If the register differs on the two paths into $D$, a copy on one of the edges makes them equal.

## References
