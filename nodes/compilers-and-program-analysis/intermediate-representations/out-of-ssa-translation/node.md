---
tag: P4GHD2
kind: problem
slug: out-of-ssa-translation
name: Out-of-SSA translation
aliases:
- SSA destruction
- SSA deconstruction
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Replace the phi-functions of an SSA program by copies on incoming edges so that the program runs on a machine without phi-functions.
prereqs: [static-single-assignment-form, phi-function, critical-edge-splitting]
see_also: [lost-copy-and-swap-problems, sreedhar-cssa-translation, ssa-construction-problem, copy-propagation, live-variable-analysis, interference-graph, ssa-based-register-allocation, chaitin-register-allocation]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the translation out of SSA form, with copies at the ends of predecessor blocks, followed by dead code elimination and allocation by coloring to remove most copies
  - paper: "Preston Briggs, Keith D. Cooper, Timothy J. Harvey and L. Taylor Simpson, Practical improvements to the construction and destruction of static single assignment form, Software: Practice and Experience 28(8), 1998, pages 859-881"
    locator: the lost copy and swap problems that appear after copy folding, and a translation that uses liveness and orders the copies, with temporaries for cycles
  - paper: doi:10.1007/3-540-48294-6_13
    title: Vugranam C. Sreedhar, Roy Dz-Ching Ju, David M. Gillies and Vatsa Santhanam, Translating out of static single assignment form, Static Analysis Symposium (SAS 1999), LNCS 1694
    locator: conventional and transformed SSA form, phi congruence classes, and three methods of copy insertion that need no edge splitting
  - paper: doi:10.1109/CGO.2009.19
    title: Benoit Boissinot, Alain Darte, Fabrice Rastello, Benoît Dupont de Dinechin and Christophe Guillon, Revisiting out-of-SSA translation for correctness, code quality, and efficiency, International Symposium on Code Generation and Optimization (CGO 2009), pages 114-125
    locator: phi-functions as parallel copies, their sequentialization with one extra variable, and interference tests that use values and dominance
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms); Chapter 21 (SSA Destruction for Machine Code)
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 19 (Static Single-Assignment Form), conversion out of SSA form
---

Out-of-SSA translation is the task of turning a program in [static single assignment form](/static-single-assignment-form/) back into ordinary code. Machines have no [phi-functions](/phi-function/), so each one must become copies: when control enters block $b$ from a predecessor $p$, each phi-function of $b$ copies its operand for $p$ into its target. Straight after SSA construction this is easy, because all names of one variable can take the old name back and the phi-functions disappear. After optimizations such as [copy propagation](/copy-propagation/), names joined by a phi-function can be live at the same time, and the simple translation gives wrong code. The two classic failures are the [lost copy and swap problems](/lost-copy-and-swap-problems/). So the task has two parts: produce correct code, and leave as few copies and new blocks as possible.

## In plain words

A phi-function says that the value at this point depends on where control came from. A real machine cannot do that, so the compiler puts copies on each incoming path instead. Two things can go wrong. A copy at the end of the previous block also runs when that block goes somewhere else. And the phi-functions at the top of one block all take their values at the same moment, while copies run one after another, so one copy can overwrite a value that a later copy still needs. A good translation avoids both mistakes. Then it removes as many copies as it can, because each copy costs time and code size.

## Definition

**Input.** A procedure in strict SSA form over a [control flow graph](/control-flow-graph/) $G = (N, E, r)$. A block $b$ can start with phi-functions $x = \phi(a_1, \ldots, a_k)$ that have one operand for each predecessor. An operand is a name or a constant.

**Meaning of the phi-functions.** When control moves along the edge $(p, b)$, all phi-functions of $b$ first read their operands for $p$, and then all of them write their targets. So on that edge, the phi-functions $x_1, \ldots, x_m$ of $b$ act as one *parallel copy*

$$(x_1, \ldots, x_m) \leftarrow (a_{1p}, \ldots, a_{mp}).$$

**Output.** A procedure with no phi-functions. It can have new blocks on edges and new copy instructions. On every input it must return the same value, trap in the same way, or run forever, as the SSA procedure does.

**Quality.** Fewer copies are better, and fewer new blocks and jumps are better. A copy on a frequent edge costs more than a copy on a rare one.

**Conventional SSA form.** Two names are *phi-related* if one is the target and the other an operand of the same phi-function. The *phi congruence classes* are the classes of the smallest equivalence relation that contains this relation. Two names *interfere* if one is live at the definition of the other. A program is in *conventional SSA form* (CSSA) if no two names in the same class interfere. Otherwise it is in *transformed SSA form* (TSSA). In CSSA form, a correct translation needs no copies: give all names of a class one variable, and delete the phi-functions. Sreedhar, Ju, Gillies and Santhanam (1999) introduced these terms and showed that SSA form straight after construction is conventional. Copy propagation and value numbering can make it transformed.

**A solution always exists.** Split each [critical edge](/critical-edge-splitting/) whose target has phi-functions. Then on each edge $(p, b)$, either $p$ has one successor or $b$ has one predecessor. Put the parallel copy of the edge at the end of $p$ in the first case, and at the top of $b$ in the second, and turn it into sequential copies as in the Bounds section. This is correct for every strict SSA program. The copy runs exactly when the edge is taken. It reads each operand when the phi-function would read it. It writes $x_i$ just before $b$ starts, and that clobbers nothing: by strictness, every use of $x_i$ comes after the phi-function in $b$. The rest of the problem is to do this with fewer copies and fewer new blocks.

## Variants

- **With or without edge splitting.** Splitting is simple, but it adds blocks and jumps, and some edges cannot be split. Sreedhar et al. (1999) and Boissinot et al. (2009) first make the program conventional with extra copies, and then rename. Neither splits edges.
- **Before or after register allocation.** Most compilers leave SSA form before register allocation. [SSA-based register allocation](/ssa-based-register-allocation/) assigns registers first, and then the parallel copies are moves between registers. Cycles then need a free register or a swap instruction.
- **Machine constraints.** Two-address instructions, fixed registers at calls, and edges that cannot be split add more copies. Chapter 21 of the SSA book by Rastello and Bouchez Tichadou covers these cases.
- **Fewest copies.** After a correct translation, a coalescing pass gives one variable to names that do not interfere, and deletes the copies between them. This is the coalescing step of [Chaitin's register allocator](/chaitin-register-allocation/) on the [interference graph](/interference-graph/). Boissinot et al. also let two names share a variable when they always hold the same value, even if both are live.

## Examples

### Conventional SSA: renaming is enough

```
# params: c
B1:
  br c B2 B3
B2:
  x.1 = 1
  jump B4
B3:
  x.2 = 2
  jump B4
B4:
  x.3 = phi [B2: x.1, B3: x.2]
  ret x.3
```

The only class is $\{x.1, x.2, x.3\}$, and its names are never live at the same time. Rename all three to `x` and delete the phi-function. The result is the program before SSA construction.

### The lost copy

```
# params: n
B1:
  x.1 = 1
  jump B2
B2:
  x.2 = phi [B1: x.1, B2: x.3]
  x.3 = x.2 + 1
  t.1 = x.3 < n
  br t.1 B2 B3
B3:
  ret x.2
```

This program returns $n - 1$ for $n \ge 2$. Copy propagation produced it from a program with `y.1 = x.2` in B2 and `ret y.1` in B3. Now $x.2$ is still live when $x.3$ is defined, so the program is not conventional. The copy `x.2 = x.3` at the end of B2 also runs on the exit to B3, and the program returns 3 for $n = 3$ instead of 2. Splitting the critical edge from B2 to B2 gives the copy its own block, and the result is correct again. The [lost copy and swap problems](/lost-copy-and-swap-problems/) page goes through both cases in detail.

### The swap

```
# params: n
B1:
  a.1 = 1
  b.1 = 2
  i.1 = 1
  jump B2
B2:
  a.2 = phi [B1: a.1, B2: b.2]
  b.2 = phi [B1: b.1, B2: a.2]
  i.2 = phi [B1: i.1, B2: i.3]
  i.3 = i.2 + 1
  t.1 = i.2 < n
  br t.1 B2 B3
B3:
  r.1 = a.2 * 10
  r.2 = r.1 + b.2
  ret r.2
```

Each trip around the loop swaps $a$ and $b$, so the program returns 12, 21, 12, ... for $n = 1, 2, 3, \ldots$. On the back edge, the parallel copy is $(a.2, b.2, i.2) \leftarrow (b.2, a.2, i.3)$. Split the back edge into a new block B4. If B4 does `a.2 = b.2` and then `b.2 = a.2`, both get the old value of $b.2$, and the program returns 22 for $n = 2$. A correct order needs one temporary:

```
B4:
  i.2 = i.3
  t = b.2
  b.2 = a.2
  a.2 = t
  jump B2
```

## Known algorithms

| method | idea | copies before coalescing |
|---|---|---|
| Cytron et al. (1991) | a copy for each phi operand at the end of the predecessor, then dead code elimination and coalescing by coloring | one per phi operand; wrong after copy folding |
| edge splitting with parallel copies | split critical edges, put one parallel copy on each edge, then sequentialize | one per phi operand, plus one per cycle |
| Briggs et al. (1998) | use liveness to find copies whose target is still needed, order the copies on each edge, and use temporaries for cycles | about one per phi operand |
| [Sreedhar et al.](/sreedhar-cssa-translation/) (1999) | add copies until the program is conventional, chosen with liveness and interference, then rename each class; no edge splitting | at most one per phi operand and one per phi-function |
| Boissinot et al. (2009) | add parallel copies for every phi-function, coalesce with interference tests that use values and dominance, then sequentialize; no edge splitting | as Sreedhar's first method, then coalesced |

Cytron et al. give the first method. It is correct while the program is conventional, which holds when no optimization ran in between. Briggs, Cooper, Harvey and Simpson (1998) showed how copy folding during renaming breaks it, with the lost copy and swap problems, and gave a repair. Sreedhar et al. (1999) define three methods. Method I copies every operand and every target. Method III uses liveness to copy only where two names in a class would interfere, and gives far fewer copies. Boissinot et al. (2009) start from Method I with parallel copies and leave the copy removal to a coalescer. Their interference test is fast because it uses the dominance order of definitions.

## Bounds

- **Copies.** Splitting with parallel copies uses at most one copy per phi operand, plus one per cycle in each parallel copy. Sreedhar's Method I uses exactly one copy per phi operand and one per phi-function. Neither needs liveness.
- **New blocks.** Edge splitting adds at most one block for each critical edge that enters a block with phi-functions. Sreedhar's and Boissinot's methods add none.
- **Time.** Splitting and Method I take time linear in the size of the program. Methods that use liveness or interference need that analysis first.
- **A parallel copy needs at most one extra temporary per cycle.** Let $P$ be a parallel copy $d_i \leftarrow s_i$ with different targets $d_i$, and drop the moves with $d_i = s_i$. Draw an edge $s_i \to d_i$ for each move. Each location has at most one incoming edge, so each part of the graph is a tree, or a single cycle with trees hanging from it. Let $c$ be the number of cycles. Then $P$ can be done with $|P| + c$ sequential copies and one extra location $t$, and the same $t$ serves every cycle.

  *Proof.* Repeat two rules. Rule 1: if a pending move $d \leftarrow s$ has a target $d$ that no pending move reads, emit it and remove it. This is safe, because no move still needs the old value of $d$. Rule 2: if rule 1 cannot apply but moves are pending, then every target is also a source. There are as many targets as moves and at most as many sources as moves, so the sources and targets are the same set, and each location is the source of exactly one pending move and the target of exactly one. So the pending moves form disjoint cycles. Pick a move $d \leftarrow s$, emit $t \leftarrow s$, and change the move to $d \leftarrow t$. Now no pending move reads $s$, so rule 1 applies to the move into $s$, then to the move into its source, and so on around the cycle. The last move emitted on it is $d \leftarrow t$, so $t$ is free before rule 2 runs again. Rule 1 never emits a move on an unbroken cycle, because each target on a cycle is read by the next move. So rule 2 runs once per cycle, and the total is $|P| + c$ copies. With a worklist of free targets this takes $O(|P|)$ time.

- **The extra copy cannot be avoided.** Take a parallel copy that is one cycle $d_2 \leftarrow d_1, d_3 \leftarrow d_2, \ldots, d_1 \leftarrow d_k$ with $k \ge 2$ and different values in the $d_i$. With only copies, it needs $k + 1$ of them. *Proof.* Each $d_i$ must end with a new value, so each is written at least once. With only $k$ copies, each $d_i$ is written exactly once and no other location is written. The first copy writes some $d_j$. At that moment the old value of $d_j$ is in no other location, so it is lost. But the final state needs it in $d_{j+1}$. A machine with a swap instruction can do the cycle with $k - 1$ swaps and no temporary.

## Reductions

- **From conventional SSA, the problem is renaming.** Union the names of each phi congruence class and delete the phi-functions. So every method is a way to make the program conventional, by copies or by edge splits.
- **Copy removal is coalescing.** After copies are in, deleting as many as possible is the coalescing problem of register allocation: merge names that do not interfere on the [interference graph](/interference-graph/). The same tools apply.
- **Sequentializing a parallel copy** is the decomposition of a functional graph into trees and cycles, as the proof above shows.
- **The inverse problem** is [SSA construction](/ssa-construction-problem/). Construction followed at once by destruction gives back the original program, up to names, because the result of construction is conventional.

## Applications

Every compiler that optimizes in SSA form must leave it before it emits code. GCC leaves SSA form when it expands its GIMPLE code into RTL, and it first coalesces SSA names into variables. LLVM keeps SSA form on its machine code and replaces phi-functions by copies in the predecessor blocks just before register allocation. Compilers with [SSA-based register allocation](/ssa-based-register-allocation/) or [SSA linear scan](/ssa-linear-scan/) allocate first and then turn each phi-function into register moves, where the cycle rule above decides when a free register or a swap is needed.

## References
