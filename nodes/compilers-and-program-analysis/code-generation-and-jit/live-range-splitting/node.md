---
tag: NYNRRJ
kind: technique
slug: live-range-splitting
name: Live range splitting
aliases:
- range splitting
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Splits the live range of a value into pieces with copies between them, so each piece can get its own register or be spilled.
prereqs: [interference-graph, spill-code-placement]
see_also: [register-coalescing-problem, ssa-based-register-allocation, static-single-assignment-form, register-allocation-np-completeness, critical-edge-splitting, linear-scan-register-allocation, out-of-ssa-translation, rematerialization]
sources:
  - paper: doi:10.1145/88616.88621
    title: Fred C. Chow and John L. Hennessy, The priority-based coloring approach to register allocation, ACM Transactions on Programming Languages and Systems 12(4), 1990, 501-536
    locator: splitting a live range that cannot be colored into smaller live ranges, each colored or spilled on its own
  - paper: doi:10.1007/978-3-540-72521-3_21
    title: "Florent Bouchez, Alain Darte, Christophe Guillon and Fabrice Rastello, Register allocation: what does the NP-completeness proof of Chaitin et al. really prove? Or revisiting register allocation: why and how, Languages and Compilers for Parallel Computing (LCPC 2006), LNCS 4382, Springer, 2007"
    locator: with split critical edges and moves and swaps, a strict program fits in MaxLive registers; without split critical edges the question stays NP-complete
  - paper: doi:10.1007/11688839_20
    title: Sebastian Hack, Daniel Grund and Gerhard Goos, Register allocation for programs in SSA-form, Compiler Construction (CC 2006), LNCS 3923, Springer, 2006, 247-262
    locator: SSA form splits live ranges at every definition and phi-function, which makes the interference graph chordal
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 13 (Register Allocation), live range splitting in global allocators
---

Live range splitting cuts the live range of a value into pieces and joins them with copies. Each piece is a new name with its own vertex in the [interference graph](/interference-graph/), and it interferes only with the values live during that piece. So the pieces can get different registers, and a piece that crosses a region of high register pressure can be spilled while the others stay in registers. Splitting is how an allocator avoids the all-or-nothing choice of keeping one value in one register for its whole life. It is also the reason why the NP-hardness of coloring the interference graph says little about register allocation: with splitting on split critical edges, every strict program fits in as many registers as the largest number of values live at one point.

## In plain words

A value may be needed for a long time, with busy stretches and quiet stretches. If it must keep one register all that time, it blocks that register even where it is not used, and it may clash with many other values. Splitting cuts its life into parts and adds a copy where one part ends and the next begins. Each part only clashes with the values around it. One part can sit in one register and the next part in another, and a part that crosses a busy stretch can wait in memory while the other parts stay in registers. The price is the copies, which the compiler later removes where they turn out not to be needed.

## When it applies

- A value has a long live range that crosses points of high pressure, such as a loop with many temporaries or a call that destroys registers, but is used mostly where pressure is low.
- The interference graph is hard to color even though few values are live at any point. The triangle program on the page [register-allocation-np-completeness](/register-allocation-np-completeness/) has at most two live values at any point, but its graph needs three colors.
- The allocator can remove copies later, by [coalescing](/register-coalescing-problem/) or because two pieces get the same register.

## The template

1. **Choose a value and split points.** Typical points are the boundaries of a loop, the points around a call, the edges into and out of a high-pressure region, or every definition and join point, as in [SSA form](/static-single-assignment-form/).
2. **Insert copies.** At each split point, add a copy `x2 = x1` from the old piece to the new one. A split point on a control flow edge needs a place on that edge; if the edge is critical, split it first ([critical edge splitting](/critical-edge-splitting/)).
3. **Rename.** Each use of the value reads the piece that reaches it. If several pieces reach a join, they must all have one name there, so the copies on the incoming edges write that name; this is what out-of-SSA copies do.
4. **Rebuild and allocate.** The pieces are separate vertices with fewer neighbors each. Color the new graph.
5. **Clean up.** A copy between two pieces with the same register becomes `r = r` and is deleted. A piece that is spilled turns its copies into a store and a load, which is [spill code placement](/spill-code-placement/) restricted to that piece.

Several copies on one edge must act at the same time, as a *parallel copy*. If they form a cycle, such as `r0 = r1` and `r1 = r0`, a sequence of plain copies cannot do it; it needs a free register or a swap instruction.

## Classic examples

**A triangle with two live values.** The program on the page [register-allocation-np-completeness](/register-allocation-np-completeness/) has the names $u$, $v$ and $w$, each two of which are live together on some path, so they form a triangle and need three registers if each keeps one register. But at most two of them are live at any point. Splitting the live range of $u$ on one critical edge, with a new block that holds the single copy `r1 = r0`, gives a correct program with two registers: $u$ is in `r1` on one path and in `r0` on the other.

**Spill only the middle.** In the one-block program of the page [spill code placement](/spill-code-placement/), with $k = 2$, the name $b$ is defined early, used by `c = a + b`, and used again by `e = b * d`. Between the two uses, $a$, $c$ and then $d$ need the registers. Split $b$ into the piece from its definition to its first use and the piece that covers its last use, and spill only the gap: one store after the definition and one load before `e = b * d`. Spill everywhere needs one store and two loads, and spilling $c$ does not help at all.

**SSA form.** Converting to SSA form gives each definition its own name and adds $\phi$-functions at joins, which is a split at every definition and join. Hack, Grund and Goos (2006) proved that the interference graph of a strict SSA program is chordal, so it can be colored with as many colors as the largest number of values live at one point, in polynomial time ([SSA chordal interference theorem](/ssa-chordal-interference-theorem/)). The copies come back when SSA form is left, and coalescing removes most of them.

**Around a call.** A call may destroy every caller-saved register. A value live across the call but used only before and after it can be split into three pieces: a piece in any register before the call, a piece in a callee-saved register or in memory across the call, and a piece after it.

## Variations

- **Priority-based coloring.** Chow and Hennessy (1990) color live ranges in order of priority and split a live range that finds no color into smaller pieces, which are colored or spilled on their own.
- **Split everywhere.** With split critical edges, moves and swaps, Bouchez, Darte, Guillon and Rastello (LCPC 2006) show that a strict program fits in MaxLive registers, the largest number of values live at one point. Then deciding if $k$ registers suffice is as easy as computing MaxLive. Without split critical edges, the question stays NP-complete even with splitting.
- **SSA-based allocation.** [SSA-based register allocation](/ssa-based-register-allocation/) uses the splits of SSA form, spills until MaxLive is at most $k$, colors the chordal graph, and then coalesces copies.
- **Interval splitting in linear scan.** [Linear scan](/linear-scan-register-allocation/) can split an interval at the point where no register is free, and continue the rest of the interval in another register or in memory.
- **Region-based splitting.** Split at the boundaries of loops or of other regions, so that the value can have a different register, or memory, in each region.

## Pitfalls

- **Coalescing can undo the split.** The copies between pieces are affinities whose ends do not interfere. Aggressive coalescing merges them all back into the original live range. Use [conservative coalescing](/conservative-coalescing/), which merges pieces only when this is safe.
- **Too many splits.** Each split adds a copy, and copies that are not removed cost time and code size. Split where pressure is high or the graph is hard to color, not everywhere.
- **Parallel copies.** The copies on one edge must not overwrite a value that another copy still reads. Order them, or use a swap or a free register for cycles.
- **Critical edges.** A copy at the end of a block with two successors runs on both paths, and it may overwrite a register that the other path needs. Split the edge.
- **All paths.** Every path into a piece must pass a copy into that piece. A missing copy on one path leaves a use that reads a stale register.

## Exercises

1. In the triangle program, why is one copy enough, when coloring needs three colors?

   *Answer.* The three names clash only along different paths, and at any point at most two are live. The copy lets $u$ change register on one edge, so on each path the two live names use two different registers, while no single choice of register per name works on all paths at once.

2. Why does aggressive coalescing undo a split, and why does conservative coalescing not always do so?

   *Answer.* The copy between two pieces has ends that do not interfere, since one piece ends where the next begins. Aggressive coalescing merges every such pair, which rebuilds the old live range and its old edges. Conservative coalescing merges only when the Briggs or George test passes, and those tests fail exactly when the merged vertex would have many neighbors of high degree, which is often why the split was made.

3. On one edge the allocator must perform `r0 = r1` and `r1 = r0` at the same time. Give a correct sequence with a free register `r2`, and say what to do with no free register.

   *Answer.* `r2 = r0; r0 = r1; r1 = r2`. With no free register, use a swap instruction if the machine has one, or three exclusive-or operations on `r0` and `r1`, or spill one of the values through memory.

4. A value is defined before a loop, not used in the loop, and used after it. The loop needs all registers. How should it be split?

   *Answer.* Into a piece before the loop and a piece after it, with the value in memory across the loop: a store before the loop and a load after it. Both run once, instead of once per iteration.

## References
