---
tag: SBG2CF
kind: algorithm
slug: ssa-linear-scan
name: Linear scan register allocation on SSA form
aliases:
- Wimmer-Franz linear scan
area: compilers-and-program-analysis/code-generation-and-jit
level: research
summary: Runs linear scan directly on SSA form with lifetime intervals and resolves phi-functions after allocation, without leaving SSA first.
solves: [register-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of names, s: the number of instructions and terminators, b: the number of blocks}
  time: {worst: O(s + b^2 + n^2 b)}
  space: {extra: O(s + n b)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2010
  people: [Christian Wimmer, Michael Franz]
  note: Built on the linear scan allocator of the Java HotSpot client compiler by Wimmer and Mössenböck, which took lifetime holes from Traub, Holloway and Smith and SSA-based intervals from Mössenböck and Pfeiffer.
prereqs: [static-single-assignment-form, dominator-tree, natural-loop, reducible-flow-graph, live-variable-analysis, linear-scan-register-allocation]
see_also: [ssa-based-register-allocation, ssa-chordal-interference-theorem, live-range-splitting, chaitin-register-allocation, just-in-time-compilation, critical-edge-splitting, out-of-ssa-translation, loop-nesting-forest]
sources:
  - paper: doi:10.1145/1772954.1772979
    title: Christian Wimmer and Michael Franz, Linear scan register allocation on SSA form, CGO 2010, 170-179
    locator: the block order with dominators first and contiguous loops, the construction of the lifetime intervals in one backward pass over the blocks with a range over the whole loop for names live at a loop header, the intersection tests that SSA form makes unneeded, and the removal of the phis in the resolution phase after allocation
  - paper: doi:10.1145/1064979.1064998
    title: Christian Wimmer and Hanspeter Mössenböck, Optimized interval splitting in a linear scan register allocator, VEE 2005, 132-141
    locator: the lifetime intervals with holes, the active and inactive sets of the scan, interval splitting and register hints, and the resolution of moves on the edges in the HotSpot client compiler
  - paper: doi:10.1007/3-540-45937-5_17
    title: Hanspeter Mössenböck and Michael Pfeiffer, Linear scan register allocation in the context of SSA form and register constraints, Compiler Construction (CC 2002), LNCS, 229-246
    locator: linear scan on lifetime intervals of a program in SSA form, with register constraints of the machine and the phis turned into moves after allocation
  - paper: doi:10.1145/277650.277714
    title: Omri Traub, Glenn Holloway and Michael D. Smith, Quality and speed in linear-scan register allocation, PLDI 1998, 142-151
    locator: lifetimes with holes in second-chance binpacking, where a value in a hole does not hold its register
  - paper: doi:10.1145/330249.330250
    title: Massimiliano Poletto and Vivek Sarkar, Linear scan register allocation, ACM TOPLAS 21(5), 1999, 895-913
    locator: the original scan over live intervals sorted by start, with the spill of the interval that ends last
---

Linear scan on SSA form gives registers to the names of a program while it is still in [static single assignment form](/static-single-assignment-form/), with the scan of [linear scan](/linear-scan-register-allocation/). It differs from classic linear scan in three ways. Each name gets a lifetime interval with holes, a list of ranges, not one interval from the first to the last point where it is live. The intervals come from one backward pass over the blocks, with no fixed point of liveness, because each name has one definition and the blocks are put in an order where dominators come first and loops are contiguous. The phis stay until after the scan, and then turn into moves at the ends of the predecessors. It differs from [SSA-based register allocation](/ssa-based-register-allocation/) in that it does not spill first and color second: it decides spills during the scan, like any linear scan, so it is fast and simple but gives no promise on the number of spills.

## In plain words

Put the blocks of the program in a line, so that every block comes after the blocks that must run before it, and every loop sits together. Number every instruction along that line. For each value, write down the stretches of the line where the value must be kept, going from the bottom to the top once. A value can have gaps where it is not needed. Then walk down the line. When a value starts, give it a register that no value holds at any point where the new value is kept. If no register is free, send the value that lasts longest to memory. Last, where paths join and a value has different names on different paths, add copies at the end of each path.

## The problem

The input is a program $P$ in the toy IR in strict SSA form, with `const`, `copy`, `op` and `phi` instructions, a reducible control flow graph, and a number $k \ge 1$ of registers. Strict means that each name has one definition and that the definition dominates every use, where a phi operand from the predecessor $Q$ counts as used at the end of $Q$. Reducible means that every cycle enters through a block that dominates the cycle, see [reducible flow graph](/reducible-flow-graph/). The output is a program with no phi that uses only the registers $r_0, \ldots, r_{k-1}$, two scratch registers $s_0$ and $s_1$ for spill code and copies, and memory slots `mem.x`, and that has the same outcome as $P$ on every input.

A *node* is the group of all phis of one block, one other instruction, or one terminator. For a node $v$, $D(v)$ is the set of names that $v$ defines and $O(v)$ is the set of names live just after $v$. MaxLive is the largest $|D(v) \cup O(v)|$. Names $x$ and $y$ interfere when one of them is in $D(v)$ and the other in $D(v) \cup O(v)$ for some node $v$.

## The algorithm

```pseudo id=main
SSA-LINEAR-SCAN(P, k)
L1  P <- P with a start block that loads the parameters, and each edge from a br into a block with phis split
L2  order the blocks so that each block follows its dominators and each loop is contiguous; number the positions
L3  for each block b in reverse order do
L4     live <- union of liveIn(s) over the successors s of b, plus the phi operands that b sends to s
L5     for each x in live do add the range [b.start, b.end) to x
L6     for each item i of b from last to first (terminator, then instructions) do
L7        for its result y: if y in live, cut the first range of y to start at pos(i) and remove y from live; else add [pos(i), pos(i)+1)
L8        for each operand x: add [b.start, pos(i)) to x; add x to live
L9     for each phi y of b: remove y from live (add [b.start, b.start+1) if it is dead); liveIn(b) <- live
L10    if b is a loop header then
L11       for each x in live do add [b.start, end of the last block of the loop) to x
L12 sort the intervals by start
L13 for each interval cur in that order do
L14    move intervals of active that ended out, and those in a hole at start(cur) to inactive
L15    move intervals of inactive that ended out, and those that cover start(cur) to active
L16    busy <- registers of active, and of inactive intervals that intersect cur
L17    if some register is not busy then give cur the lowest one; add cur to active
L18    else s <- the interval in active, whose register no intersecting inactive interval holds, with the largest end
L19       if end(s) > end(cur) then give cur the register of s; spill s
L20       else spill cur
L21 for each edge (Q, B) with B having phis do the parallel copy loc(y) <- loc(a) at the end of Q
L22 sequentialize it with s0 for cycles and s1 for memory to memory moves
L23 return the program with registers and slots, loads into s0/s1 before uses of spilled names and stores after definitions
```

Here $\mathrm{loc}(x)$ is $r_c$ for a kept name with register $c$ and `mem.x` for a spilled name. A range $[a, e)$ is half open.

**Positions.** Line L2 gives each block $b$ an even position $b.\mathit{start}$, where its phis write. Its instructions and its terminator get the next even positions, and $b.\mathit{end}$, two after the last item, is the start of the next block. An item at position $q$ reads its operands at the end of ranges that stop at $q$, and writes its result at the start of a range that begins at $q$. So a name read at $q$ and a name written at $q$ do not meet there, and the result can take the register of an operand that dies.

**The block order.** The [natural loops](/natural-loop/) are found from the back edges, and each loop is first shrunk to its header. Without back edges the graph is acyclic, so its reverse postorder puts every block after its dominators. Each header is then replaced by the order of its own loop, built the same way. Every edge that goes backward in this order is a back edge. Irreducible graphs are rejected: they have a cycle with two entries and no single header.

**Why one pass suffices.** In the backward pass, every successor along a forward edge is done before its predecessor, so lines L4 to L9 compute liveness along paths with no back edge. A value can be live around a loop only if it is live at the header, and such a value is defined before the loop and needed in all of it. Line L11 covers the whole loop for it, which is one range because the loop is contiguous. That fills in the rest, and the result is exact liveness without a fixed point.

**The scan.** An interval is *active* when it covers the current position and *inactive* when it is in a hole there but has later ranges. An inactive interval does not hold its register, so another interval that fits in the hole can use it. Line L16 still checks inactive intervals for a later overlap. In strict SSA with this order that check never finds one: an earlier interval in a hole at $\mathrm{start}(\mathit{cur})$ is not live at the definition of $\mathit{cur}$, so the two names do not interfere. Wimmer and Franz use this to skip those tests.

Line L1 is the usual [critical edge splitting](/critical-edge-splitting/): the copies for an edge $(Q, B)$ go at the end of $Q$, and if $Q$ ended in `br` they would also run on its other edge. The start block gives each parameter a definition, which keeps the program strict.

This version never splits an interval: a name lives in one register for its whole life or in its slot. The allocator of Wimmer and Franz splits intervals and uses register hints, see the variants below.

## Example

**Holes.** The program has the parameter `p` and a join with a phi:

```
entry:
  a = p + 1
  br p L R
L:
  d = a - p
  jump J
R:
  b = p * 2
  c = b + p
  jump J
J:
  e = phi [L: d, R: c]
  ret e
```

Line L1 adds `start: p = mem.p; jump entry`. No edge needs a split block, because `L` and `R` end in `jump`. Line L2 gives the order `start`, `entry`, `R`, `L`, `J`. The positions are:

| block | start | items | end |
|---|---|---|---|
| start | 0 | `p = mem.p` 2, `jump` 4 | 6 |
| entry | 6 | `a = p + 1` 8, `br` 10 | 12 |
| R | 12 | `b = p * 2` 14, `c = b + p` 16, `jump` 18 | 20 |
| L | 20 | `d = a - p` 22, `jump` 24 | 26 |
| J | 26 | `ret e` 28 | 30 |

The backward pass gives these intervals:

| name | ranges | why |
|---|---|---|
| $p$ | $[2, 16)$, $[20, 22)$ | dead in `R` after `c = b + p` at 16, live into `L` |
| $a$ | $[8, 12)$, $[20, 22)$ | dead in `R`, used in `L` |
| $b$ | $[14, 16)$ | |
| $c$ | $[16, 20)$ | phi operand, live to the end of `R` |
| $d$ | $[22, 26)$ | phi operand, live to the end of `L` |
| $e$ | $[26, 28)$ | |

The scan with $k = 2$ goes:

| cur | start | active | inactive | busy | action |
|---|---|---|---|---|---|
| $p$ | 2 | none | none | none | $p \to r_0$ |
| $a$ | 8 | $p$ | none | 0 | $a \to r_1$ |
| $b$ | 14 | $p$ | $a$ (hole) | 0 | $a$ does not meet $b$: $b \to r_1$ |
| $c$ | 16 | none | $p$, $a$ (holes) | none | $b$ ended, $p$ is in a hole: $c \to r_0$ |
| $d$ | 22 | none | none | none | $p$, $a$, $c$ ended: $d \to r_0$ |
| $e$ | 26 | none | none | none | $e \to r_0$ |

Nothing is spilled. The phi needs no move, since $c$, $d$ and $e$ all have $r_0$. The output is:

```
start:
  r0 = mem.p
  jump entry
entry:
  r1 = r0 + 1
  br r0 L R
R:
  r1 = r0 * 2
  r0 = r1 + r0
  jump J
L:
  r0 = r1 - r0
  jump J
J:
  ret r0
```

Without holes, the interval of $a$ would be $[8, 22)$ and that of $p$ would be $[2, 22)$. At position 14 these two and $b$ would overlap, so classic linear scan with two registers would spill. The same happens on the [linear scan](/linear-scan-register-allocation/) page, where the program has no join. With $k = 1$ the scan spills $p$ and $a$, and the output loads them through $s_0$ and $s_1$. Both outputs return the same values as the input, for example 1 for $p = 1$ and 0 for $p = 0$.

**Loops.** The program sums the squares $0^2 + 1^2 + \cdots + (n-1)^2$:

```
entry:
  i0 = 0
  a0 = 0
  jump head
head:
  i1 = phi [entry: i0, body: i2]
  a1 = phi [entry: a0, body: a2]
  t = i1 < n
  br t body done
body:
  u = i1 * i1
  a2 = a1 + u
  i2 = i1 + 1
  jump head
done:
  ret a1
```

The order is `start`, `entry`, `head`, `body`, `done`, with starts 0, 6, 14, 20 and 30. The loop is `head` and `body`, which ends at 30. The intervals are:

| name | ranges | why |
|---|---|---|
| $n$ | $[2, 30)$ | live into `head`, so line L11 covers the whole loop |
| $i_0$ | $[8, 14)$ | phi operand |
| $a_0$ | $[10, 14)$ | phi operand |
| $a_1$ | $[14, 24)$, $[30, 32)$ | phi of `head`, last use in `body` at 24, used in `done` |
| $i_1$ | $[14, 26)$ | |
| $t$ | $[16, 18)$ | |
| $u$ | $[22, 24)$ | |
| $a_2$ | $[24, 30)$ | phi operand on the back edge |
| $i_2$ | $[26, 30)$ | phi operand on the back edge |

When `body` is done in the backward pass, `head` is not done yet, so `body` sees only the phi operands $a_2$ and $i_2$ it sends, not $n$. Line L11 at `head` adds $[14, 30)$ to $n$, which joins $[2, 14)$ into $[2, 30)$. MaxLive is 4, at `t = i1 < n`, where $n$, $a_1$, $i_1$ and $t$ meet.

With $k = 4$ nothing is spilled and four registers are used: $n \to r_0$, $i_0 \to r_1$, $a_0 \to r_2$, $a_1 \to r_1$, $i_1 \to r_2$, $t \to r_3$, $u \to r_3$, $a_2 \to r_1$ and $i_2 \to r_2$. The loop body has no move, but on the edge from `entry` the parallel copy $r_2 \leftarrow r_1$, $r_1 \leftarrow r_2$ is a swap, and line L22 breaks it with $s_0$:

```
entry:
  r1 = 0
  r2 = 0
  s0 = r2
  r2 = r1
  r1 = s0
  jump head
```

The scan took the lowest free register for $a_1$ and $i_1$, in name order, without looking at their phi operands. Register hints would give $i_1$ the register of $i_0$ and remove the swap.

With $k = 3$, at $t$ (start 16) the active intervals are $n$ (end 30), $a_1$ (end 32) and $i_1$ (end 26). The one with the largest end is $a_1$, and $32 > 18$, so $a_1$ is spilled and $t$ takes its register $r_1$. Then $u \to r_1$, $a_2 \to r_1$ and $i_2 \to r_2$. The edge copies become `mem.a1 = r2; r2 = r1` from `entry` and `mem.a1 = r1` from `body`. With $k = 2$ the scan spills $a_1$ and $n$. All outputs return 0, 0, 1, 5, 14, 30 for $n = 0, \ldots, 5$, the same as the input.

## Correctness

The full proof is in the proof file. Its parts are:

- **Order.** In each region the graph with loops shrunk to their headers has only forward edges and is acyclic, so its reverse postorder puts dominators first. By induction on the nesting of loops, each loop is contiguous and every backward edge is a back edge.
- **Exact intervals.** The backward pass computes liveness along paths with no back edge. A shortest path from a block to a use, cut at its first back edge $u \to h$, shows that a name live into a block is either found by the pass or live into a header $h$ whose loop holds the block. Such a name is defined before the loop and live in all of it, which is what line L11 adds. So an interval covers a position exactly when its name is live there, and two intervals meet exactly when their names interfere.
- **Scan.** At each step, active holds the earlier kept intervals that cover the current start, and inactive those in a hole that end later. So *busy* is exactly the set of registers of earlier kept intervals that meet $\mathit{cur}$, and two kept intervals that meet never share a register.
- **Optimal when the pressure fits.** The start of an interval is the definition of its name, and dominators come first. So the earlier intervals that meet $\mathit{cur}$ are names live at the definition of $\mathit{cur}$, at most MaxLive $- 1$ of them. With $k \ge$ MaxLive, nothing is spilled and exactly MaxLive registers are used, by the [SSA chordal interference theorem](/ssa-chordal-interference-theorem/).
- **Same outcome.** Along a run, every name whose interval covers the position holds its value in its location. A definition writes only its own location, and the parallel copy on an edge writes only the locations of the phis, which no other live name shares.

When $k$ is below MaxLive the spill choice is a heuristic. With holes the intervals no longer form an interval graph, so the optimality of the furthest end rule for intervals does not carry over.

## Complexity

With $n$ names, $s$ instructions and terminators, and $b$ blocks:

- **Block order.** Dominators by the iterative method, natural loops from the back edges, and one reverse postorder per loop region take $O(b^2)$ in the worst case and close to $O(b)$ in practice.
- **Intervals.** One backward pass. Each block adds a range for each name live through it, so there are $O(s + n b)$ range additions. In the backward pass a new range is always at or before the first range of its name, so with ranges kept in a list from the front each addition is $O(1)$, as in the paper. The Python code merges into a sorted list, which is simpler and slower.
- **Scan.** Each interval looks at the active and inactive sets, $O(n)$ intervals, and an intersection test walks two lists of at most $O(b)$ ranges. That is $O(n^2 b)$ in the worst case. Since the inactive test can be skipped in SSA form, and the active set is at most $k$ long, the scan is close to linear in practice.
- **Phi removal.** One parallel copy per edge into a block with phis, quadratic in the number of phis of that block with the simple scan.

The total is $O(s + b^2 + n^2 b)$ time and $O(s + n b)$ space. No interference graph is built and no liveness fixed point is run.

## Properties

- **One liveness pass.** For a reducible graph in SSA form, the intervals are exact after one backward pass. Classic linear scan needs a fixed point of [live variable analysis](/live-variable-analysis/) first.
- **Holes.** A name does not hold its register where it is dead, so another name can use it there. This often saves a register, as in the diamond above.
- **Exact when the pressure fits.** With $k \ge$ MaxLive it uses exactly MaxLive registers and no spill. Classic linear scan has no such promise, because its intervals depend on the block order and can overlap where the names do not interfere.
- **No interference graph.** The scan needs only the intervals, so it fits a [just-in-time compiler](/just-in-time-compilation/), where compile time counts.
- **Whole names in this version.** A spilled name is in memory everywhere. There is no splitting, so one hot use cannot save a name that lives long.
- **Reducible graphs only.** The loop rule of line L11 needs one header per loop. Structured source languages rarely give irreducible graphs, and node splitting can make any graph reducible.

## Variants and improvements

- **Interval splitting** (Wimmer and Mössenböck, 2005). When no register is free for the whole of $\mathit{cur}$, the allocator gives it a register up to the point where that register is next needed, splits the interval there, and puts the rest back in the list. Spilled parts are split around their uses so that each use has a register. A resolution pass then adds moves on edges where the two sides of a split are in different locations. Wimmer and Franz keep this and put the phi moves into the same pass. See [live range splitting](/live-range-splitting/).
- **Register hints.** An interval defined by a move or a phi gets a hint to use the register of its source, which removes the swap of the loop example in most cases.
- **Fixed intervals.** Registers that an instruction must use, such as the operands of a call, are given as intervals that are already assigned, and other intervals must avoid them.
- **Use positions.** Real allocators keep for each interval the positions of its uses, and spill the interval whose next use is furthest away instead of the one that ends last.
- **[SSA-based register allocation](/ssa-based-register-allocation/).** Spill first until the pressure is at most $k$, then color in dominance order with no spill. It gives better spill decisions when $k$ is small, at the cost of a separate spill phase.

## When to use it

Use it in a JIT compiler or a fast compiler tier that keeps SSA form until code generation, where allocation time matters more than the last bit of code quality. It removes the liveness fixed point and the step that leaves SSA form, and it gives the best number of registers when no spill is needed. For an optimizing compiler where spill code matters most, use [SSA-based register allocation](/ssa-based-register-allocation/) or [graph coloring](/chaitin-register-allocation/). For a program that has already left SSA form, use [classic linear scan](/linear-scan-register-allocation/).

## Pitfalls

- **A bad block order.** The loop rule covers a loop with one range from the header to the end of the last loop block. If a block from outside the loop sits in between, a name gets a range where it is not live, and if a loop block sits outside, a range is missing. Keep each loop contiguous.
- **Back edges in the backward pass.** The pass cannot see the live-in set of a header from the end of its loop, since the header is done last. Do not try to read it there. Add only the phi operands the latch sends, and let line L11 cover the rest.
- **Irreducible graphs.** A cycle with two entries has no header, so the one-pass intervals miss liveness around it. Reject such graphs, make them reducible first, or fall back to a liveness fixed point.
- **Phi operands.** An operand of a phi of $B$ is live to the end of the predecessor $Q$, not to the start of $B$. Count it in the live-out set of $Q$ only, not in the live-in set of $B$.
- **Copies on a branch edge.** A copy for the edge $(Q, B)$ placed before a `br` of $Q$ also runs on the other edge. Split such edges first.
- **Swaps.** Two phi moves that exchange registers form a cycle. Copying them one by one loses a value. Use a scratch register or an exchange instruction.
- **Leaving SSA first.** If the phis are replaced by copies before the scan, a name has several definitions, the one-pass rule fails, and the MaxLive promise is lost. Allocate first, then remove the phis.

## Implementations

## History

Poletto and Sarkar (1999) introduced linear scan for fast code generation, with one interval per name. Traub, Holloway and Smith (1998) used lifetimes with holes in their second-chance binpacking allocator. Mössenböck and Pfeiffer (2002) built a linear scan on lifetime intervals of an SSA-based intermediate form with register constraints, and Wimmer and Mössenböck (2005) added interval splitting and register hints in the allocator of the Java HotSpot client compiler. These allocators still left SSA form before the scan. Wimmer and Franz (2010) changed the HotSpot client allocator to work on SSA form. They built the intervals without iterative liveness, skipped the intersection tests that SSA form makes unneeded, and removed the phis in the resolution phase. They reported code that was as good or slightly better, and a faster allocator.

## References
