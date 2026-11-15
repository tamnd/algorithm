---
tag: C6A8K4
kind: algorithm
slug: ssa-based-register-allocation
name: SSA-based register allocation
aliases:
- decoupled register allocation
area: compilers-and-program-analysis/code-generation-and-jit
level: research
summary: Spills until register pressure is at most k everywhere, then colors the chordal SSA interference graph with no further spills.
solves: [register-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of names, s: the number of nodes, b: the number of blocks, l: the time of one liveness analysis}
  time: {worst: O(l + s n^2 + b^2)}
  space: {extra: O(s n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2006
  people: [Sebastian Hack, Daniel Grund, Gerhard Goos]
  note: Brisk, Dabiri, Macbeth and Sarrafzadeh, and Bouchez, Darte, Guillon and Rastello, found the chordal property at about the same time, and Pereira and Palsberg had seen it in practice.
prereqs: [register-allocation-problem, static-single-assignment-form, ssa-chordal-interference-theorem, chordal-graph-coloring, out-of-ssa-translation]
see_also: [chaitin-register-allocation, linear-scan-register-allocation, ssa-linear-scan, register-allocation-np-completeness, register-coalescing-problem, spill-code-placement, live-range-splitting, belady-algorithm]
sources:
  - paper: doi:10.1007/11688839_20
    title: Sebastian Hack, Daniel Grund and Gerhard Goos, Register allocation for programs in SSA-form, Compiler Construction (CC 2006), LNCS 3923, 247-262
    locator: the split of allocation into a spill phase that lowers the register pressure to k and a coloring phase in a dominance order that needs no further spill, and the removal of the phis by permutations of registers
  - paper: doi:10.1016/j.ipl.2006.01.008
    title: Sebastian Hack and Gerhard Goos, Optimal register allocation for SSA-form programs in polynomial time, Information Processing Letters 98(4), 2006, 150-155
    locator: the proof that the interference graph of a strict SSA program is chordal, and that its chromatic number is the largest register pressure
  - paper: doi:10.1145/1254766.1254782
    title: Florent Bouchez, Alain Darte and Fabrice Rastello, On the complexity of spill everywhere under SSA form, LCTES 2007, 103-112
    locator: the proof that choosing the cheapest set of names to spill everywhere is NP-complete even for SSA programs, and the cases that are polynomial
  - paper: doi:10.1145/1375581.1375610
    title: Sebastian Hack and Gerhard Goos, Copy coalescing by graph recoloring, PLDI 2008, 227-237
    locator: copy coalescing after the coloring, by recoloring chunks of names connected by copies while the coloring stays valid
  - paper: doi:10.1007/978-3-642-00722-4_13
    title: Matthias Braun and Sebastian Hack, Register spilling and live-range splitting for SSA-form programs, Compiler Construction (CC 2009), LNCS 5501, 174-189
    locator: the spill phase based on the furthest next use rule of Belady, applied per block with loop-aware distances, which inserts reloads and splits live ranges
  - paper: doi:10.1007/978-3-030-80515-9_22
    title: Fabrice Rastello and Florent Bouchez Tichadou, Register allocation, chapter 22 of SSA-based Compiler Design, Springer, 2022, 303-328
    locator: the overview of the decoupled approach, the spill phase, the coloring along the dominance tree, and the coalescing and phi removal after coloring
---

SSA-based register allocation gives registers to the names of a program while it is still in [static single assignment form](/static-single-assignment-form/). It works in two separate phases. The spill phase keeps names in memory until, at every point, at most $k$ names that are not spilled hold a value. The coloring phase then walks the blocks in the order of the [dominator tree](/dominator-tree/) and gives each definition a free register, and it never fails, because the [SSA chordal interference theorem](/ssa-chordal-interference-theorem/) says that the register pressure is the number of colors needed. Only after that are the phis replaced by copies. This split is why it is also called decoupled register allocation. In [Chaitin's allocator](/chaitin-register-allocation/), spilling and coloring must loop, because a graph can need more colors than its pressure.

## In plain words

First decide which values will live in memory. Count, at every instruction, how many values must be held at once. Where the count is above the number of registers, pick a value that is cheap to keep in memory and move it out of the count. Repeat until every count fits. Then visit the code from the top, so that each value is seen where it is made before any place where it is used. Give each new value the lowest register that no live value holds. The first step promised that one is free. Last, where two paths join and a value takes different names on the two paths, add copies at the end of each path. If two values must swap registers, use a spare register.

## The problem

The input is a program $P$ in the toy IR in strict SSA form, with `const`, `copy`, `op` and `phi` instructions, and a number $k \ge 1$ of registers. Strict means that each name has one definition and that the definition dominates every use. A phi operand from the predecessor $Q$ counts as used at the end of $Q$. The output is a program with no phi that uses only the registers $r_0, \ldots, r_{k-1}$, two scratch registers $s_0$ and $s_1$ kept apart for spill code and copies, and memory slots `mem.x`, and that has the same outcome as $P$ on every input.

A *node* is the group of all phis of one block, one other instruction, or one terminator. For a node $v$, $D(v)$ is the set of names that $v$ defines and $O(v)$ is the set of names live just after $v$. The *register pressure* at $v$ is $|D(v) \cup O(v)|$, without the spilled names. MaxLive is the largest pressure when nothing is spilled.

## The algorithm

```pseudo id=main
SSA-ALLOCATE(P, k)
L1  P <- P with a start block that loads the parameters, and with each edge into a block with phis split when its source ends in br
L2  compute liveness; for each node v (a phi group, an instruction or a terminator) let D(v) be its definitions and O(v) its live-out set
L3  spilled <- empty
L4  while some node v has more than k names of D(v) ∪ O(v) not in spilled do
L5     x <- the name of D(v) ∪ O(v) not in spilled with the least cost
L6     spilled <- spilled + {x}
L7  for each block B in preorder of the dominator tree do
L8     for each node v of B in order do
L9        busy <- the colors of the names of O(v) \ D(v) not in spilled
L10       for each name y of D(v) not in spilled do
L11          color[y] <- the color of a copy or phi partner of y if it is not busy, else the lowest color not busy
L12          busy <- busy + {color[y]}
L13 for each edge (Q, B) with B having phis do
L14    put at the end of Q the parallel copy loc(y) <- loc(a) for each phi y = phi[..., Q: a, ...] of B
L15    sequentialize it, breaking cycles with s0 and moving memory to memory through s1
L16 return P without phis, names replaced by registers or slots, loads into s0/s1 before uses of spilled names and stores after their definitions
```

Here $\mathrm{loc}(x)$ is $r_c$ for a kept name of color $c$ and `mem.x` for a spilled name. The cost at line L5 is the number of definitions and uses of the name, phi operands included. Ties go to the name that is in the most nodes with too much pressure, then to the name order. A *partner* at line L11 is the source of a copy `y = a` or an operand of a phi `y`. Choosing a partner's color when it is free makes the copy or the phi move vanish, a cheap form of coalescing.

Line L1 needs a word. The parallel copy for an edge $(Q, B)$ goes at the end of $Q$. If $Q$ ends in `br`, the copy would also run on the other edge, so line L1 puts an empty block on such an edge, the usual [critical edge splitting](/critical-edge-splitting/). The start block gives each parameter a definition, which keeps the program strict.

The spill rule here is a simple heuristic, chosen so the code is short. Real compilers use the spiller of Braun and Hack, which applies the [furthest next use rule of Belady](/belady-algorithm/) along each block and splits live ranges instead of spilling whole names, and they replace the partner bias with the recoloring of Hack and Goos.

## Example

The program sums the squares $0^2 + 1^2 + \cdots + (n-1)^2$:

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

Line L1 adds `start: n = mem.n; jump entry`. No edge needs a split block: the two edges into `head` come from `entry` and `body`, which end in `jump`. The nodes, with their pressure, are:

| block | node | $D(v)$ | $O(v)$ | pressure |
|---|---|---|---|---|
| start | `n = mem.n` | $n$ | $n$ | 1 |
| entry | `i0 = 0` | $i_0$ | $i_0, n$ | 2 |
| entry | `a0 = 0` | $a_0$ | $a_0, i_0, n$ | 3 |
| head | phis | $i_1, a_1$ | $a_1, i_1, n$ | 3 |
| head | `t = i1 < n` | $t$ | $a_1, i_1, n, t$ | 4 |
| body | `u = i1 * i1` | $u$ | $a_1, i_1, n, u$ | 4 |
| body | `a2 = a1 + u` | $a_2$ | $a_2, i_1, n$ | 3 |
| body | `i2 = i1 + 1` | $i_2$ | $a_2, i_2, n$ | 3 |

The terminators define nothing and have at most 3 names live after them. So MaxLive is 4.

**With $k = 4$.** Nothing is spilled. The dominator tree has `start`, `entry` and `head` in a chain, with `body` and `done` below `head`. The coloring goes:

| node | busy | color |
|---|---|---|
| `n = mem.n` | none | $n \to 0$ |
| `i0 = 0` | 0 | $i_0 \to 1$ |
| `a0 = 0` | 0, 1 | $a_0 \to 2$ |
| phis of `head` | 0 | $i_1 \to 1$ (partner $i_0$), $a_1 \to 2$ (partner $a_0$) |
| `t = i1 < n` | 0, 1, 2 | $t \to 3$ |
| `u = i1 * i1` | 0, 1, 2 | $u \to 3$ |
| `a2 = a1 + u` | 0, 1 | $a_2 \to 2$ |
| `i2 = i1 + 1` | 0, 2 | $i_2 \to 1$ |

Four colors, exactly MaxLive. Each phi has the color of both of its operands: for $i_1$ and $a_1$ by the partner rule, for $a_2$ and $i_2$ because the lowest free color happens to match. So every parallel copy is empty and the output has no move at all except the load of the parameter:

```
start:
  r0 = mem.n
  jump entry
entry:
  r1 = 0
  r2 = 0
  jump head
head:
  r3 = r1 < r0
  br r3 body done
body:
  r3 = r1 * r1
  r2 = r2 + r3
  r1 = r1 + 1
  jump head
done:
  ret r2
```

**With $k = 3$.** The nodes of $t$ and $u$ have pressure 4. Line L5 looks at the first, $\{a_1, i_1, n, t\}$. The costs are $a_1$: 3, $i_1$: 5, $n$: 2 and $t$: 2, and $n$ wins the tie with $t$ because it is in both nodes with too much pressure. After that every pressure is at most 3, and `head` becomes `s0 = mem.n; r2 = r0 < s0; br r2 body done`. The loop reloads $n$ once per round, and the other names keep a register each, now $r_0$ to $r_2$.

**With $k = 2$.** The rule spills $n$, then $t$, then $u$. The output stores $t$ and $u$ and loads them back at once, which is the price of spilling whole names: a spiller that splits live ranges would keep $t$ and $u$ in a register for their one instruction. All three outputs return 0, 0, 1, 5, 14, 30 for $n = 0, \ldots, 5$, the same as the input.

## Correctness

The full proof is in the proof file. Its parts are:

- **Spilling.** Each round of lines L4 to L6 adds one name, so the loop stops after at most $n$ rounds, and then no node has more than $k$ kept names in $D(v) \cup O(v)$.
- **Coloring.** In a strict SSA program the definition of a live name dominates the point where it is live. So when line L9 runs at $v$, every kept name of $O(v) \setminus D(v)$ is already colored, because its definition is earlier in the block or in a dominating block. *busy* then has at most $k - 1$ colors, so line L11 finds a color below $k$. Two names that interfere meet at the definition of one of them, where the other is in *busy*, so they get different colors.
- **Optimal without spills.** If $k \ge$ MaxLive, nothing is spilled and the same bound gives at most MaxLive colors. The names of $D(v) \cup O(v)$ at a node of largest pressure all interfere, so no allocation uses fewer. This is the chordal theorem in action: the greedy order is the reverse of a perfect elimination ordering.
- **Parallel copies.** The destinations of one copy are distinct, since the phis of one block form one node. Moving a value whose destination no other move reads, and saving one destination in $s_0$ when only cycles are left, gives the effect of the parallel copy.
- **Same outcome.** Along a run, each live name holds its value in its register or slot. A definition writes a register that no other live name holds, and the parallel copy at the end of a predecessor writes only the locations of the phis.

The number of spills is not minimal when $k$ is below MaxLive. Bouchez, Darte and Rastello showed that the spill problem stays NP-complete in SSA form, so some heuristic is needed there.

## Complexity

With $n$ names, $s$ nodes, $b$ blocks and $l$ the time of liveness:

- **Liveness and nodes.** One fixed point of [live variable analysis](/live-variable-analysis/) on the blocks, then one backward walk per block gives $O(v)$ for each node in $O(s n)$ time and space.
- **Spill phase.** Each round scans all nodes in $O(s n)$, and there are at most $n$ rounds, so $O(s n^2)$ in the worst case. A real spiller works block by block in near-linear time.
- **Dominator tree.** The iterative method of Cooper, Harvey and Kennedy takes $O(b^2)$ in the worst case and is close to linear in practice.
- **Coloring.** One pass over the nodes with a set of busy colors, $O(s n)$.
- **Phi removal.** A parallel copy of $m$ moves takes $O(m^2)$ with the simple scan; the sum over all edges is at most the total size of the phis squared per block, small in practice.

The total is $O(l + s n^2 + b^2)$. No interference graph is built: the coloring needs only the live sets, which is what makes the method fast.

## Properties

- **Exact when the pressure fits.** With $k \ge$ MaxLive it uses exactly MaxLive registers and no spill, the best possible. In the Chaitin approach, deciding $k$-colorability of a general interference graph is NP-complete, so no such promise is possible there.
- **Spill and color are separate.** Once the pressure is at most $k$, coloring cannot fail. There is no loop back from coloring to spilling.
- **Strict SSA is required.** The dominance argument needs each use to be dominated by its definition. For a non-strict program, the interference graph need not be chordal.
- **Whole names in this version.** A spilled name is in memory everywhere, with a load before each use and a store after its definition, through $s_0$ and $s_1$.
- **Copies are left after coloring.** The phis turn into moves unless partners share a register. The partner bias removes many moves, but not all, and finding the fewest moves is NP-hard (see [register coalescing](/register-coalescing-problem/)).

## Variants and improvements

- **Belady-based spilling** (Braun and Hack, 2009) walks each block, keeps the $k$ values whose next use is nearest, and places reloads and splits, with loop-aware next-use distances. It lowers the pressure to $k$ with far fewer loads than spilling whole names.
- **Recoloring for coalescing** (Hack and Goos, 2008) changes the colors after the coloring phase so that names joined by copies share a register, while the coloring stays valid. Bouchez, Darte and Rastello studied other coalescing rules that keep the graph colorable.
- **Register constraints.** Calling conventions and two-address instructions fix some names to registers, which breaks chordality. Hack splits the live ranges just before such an instruction with a parallel copy, so that the constraint is met inside one node.
- **[SSA linear scan](/ssa-linear-scan/)** (Wimmer and Franz, 2010) keeps the interval model of [linear scan](/linear-scan-register-allocation/) but builds the intervals from SSA form. It is faster to write into a JIT, and it does not have the optimality of the coloring here.
- **Use in compilers.** The libFirm compiler uses this method as its main allocator, and the approach is taught in the SSA book of Rastello and Bouchez Tichadou.

## When to use it

Use it in an optimizing compiler that keeps SSA form until code generation, where code quality matters and the machine has a regular register file. It gives the best number of registers whenever no spill is needed, and its two phases can be built and tuned on their own. For a fast JIT tier, [linear scan](/linear-scan-register-allocation/) or [SSA linear scan](/ssa-linear-scan/) is simpler. For a program that has already left SSA form, use [graph coloring](/chaitin-register-allocation/), since the chordal property is gone.

## Pitfalls

- **Leaving SSA first.** If the phis are replaced by copies before allocation, a name gets several definitions and the interference graph may stop being chordal: the loop on the [interference graph](/interference-graph/) page has a chordless cycle of length 4 after [out-of-SSA translation](/out-of-ssa-translation/). Color first, then remove the phis.
- **Copies on a branch edge.** A copy for the edge $(Q, B)$ placed before a `br` of $Q$ also runs on the other edge and can overwrite a live value. Split such edges.
- **Swaps.** Two phis whose operands swap registers form a cycle in the parallel copy. Copying them one by one loses a value. Break each cycle with a scratch register, or use an exchange instruction.
- **Dead definitions.** A name that is defined and never used still needs a register at its definition. Count $D(v)$ in the pressure, not only the live names.
- **Pressure is not the whole story for spill code.** The output needs registers for the loads and stores of spilled names. Here $s_0$ and $s_1$ are kept apart for that. Without spare registers, the spill phase must lower the pressure further at instructions that read spilled names.
- **Non-strict input.** A name read on a path where it has no definition breaks the dominance argument. Give the parameters a definition in a start block and build strict SSA form.

## Implementations

## History

Pereira and Palsberg (2005) saw that most interference graphs from the Java programs they studied were chordal and colored them with a chordal coloring method. In 2005 three groups proved that strict SSA programs always give chordal interference graphs: Hack, Grund and Goos in a Karlsruhe report, published at CC 2006 and in a short proof with Goos in Information Processing Letters; Brisk, Dabiri, Macbeth and Sarrafzadeh at IWLS 2005; and Bouchez, Darte, Guillon and Rastello, whose paper appeared at LCPC 2006. Hack, Grund and Goos turned the result into the decoupled allocator. Bouchez, Darte and Rastello (2007) showed that spilling stays hard in SSA form, Hack and Goos (2008) added recoloring for coalescing, and Braun and Hack (2009) gave the spiller used in libFirm.

## References
