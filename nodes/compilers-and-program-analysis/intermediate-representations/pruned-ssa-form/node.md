---
tag: TAVH19
kind: definition
slug: pruned-ssa-form
name: Pruned SSA form
aliases:
- pruned SSA
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: Minimal SSA form without the phi-functions whose variable is dead at the join, found with liveness.
prereqs: [static-single-assignment-form, live-variable-analysis, dominance-frontier]
see_also: [phi-function, ssa-construction-problem, cytron-ssa-construction, braun-ssa-construction, dead-code-elimination, def-use-chains, ssa-based-register-allocation, out-of-ssa-translation]
sources:
  - paper: doi:10.1145/99583.99594
    title: Jong-Deok Choi, Ron Cytron and Jeanne Ferrante, Automatic construction of sparse data flow evaluation graphs, POPL 1991, pages 55-66
    locator: the pruned form of SSA, which places a phi-function for a variable only where the variable is live
  - paper: "Preston Briggs, Keith D. Cooper, Timothy J. Harvey and L. Taylor Simpson, Practical improvements to the construction and destruction of static single assignment form, Software: Practice and Experience 28(8), 1998, pages 859-881"
    locator: minimal, semi-pruned and pruned SSA form compared, and the global names used for semi-pruned SSA
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: minimal SSA form and the placement of phi-functions at iterated dominance frontiers
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 2 (Properties and Flavours), minimal, pruned and conventional SSA; Chapter 3 (Standard Construction and Destruction Algorithms), pruning during construction
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), the section on static single-assignment form, minimal, semi-pruned and pruned SSA
---

Pruned SSA form is [static single assignment form](/static-single-assignment-form/) with a [phi-function](/phi-function/) for a variable at a join block only if the variable is live on entry to that block. Minimal SSA form places a phi-function wherever two definitions of a variable meet, even if no instruction ever reads the merged value. Those phi-functions are dead. Pruned SSA leaves them out. Choi, Cytron and Ferrante introduced it in 1991 for sparse data-flow evaluation graphs. The price is a [live variable analysis](/live-variable-analysis/) before construction. Semi-pruned SSA, below, gets most of the gain with a much cheaper test.

## Definition

Let $P$ be a procedure with control flow graph $G = (N, E, r)$, where the entry $r$ has no predecessors. For a variable $v$, let $S_v$ be the set of blocks that assign $v$, plus $r$. A variable $v$ is **live on entry** to a block $y$ if some path from the start of $y$ reaches a use of $v$ with no assignment to $v$ before the use. Write $\mathit{LiveIn}(y)$ for the set of these variables. Liveness is taken in $P$, before any phi-function is placed.

Minimal SSA form places a phi-function for $v$ at exactly the blocks of the iterated [dominance frontier](/dominance-frontier/) $DF^+(S_v)$. An SSA form of $P$ is **pruned** if it has a phi-function for $v$ at block $y$ exactly when

$$y \in DF^+(S_v) \quad\text{and}\quad v \in \mathit{LiveIn}(y),$$

and the uses are renamed as in minimal SSA. Hence the phi-functions of pruned SSA are a subset of those of minimal SSA.

There is an equivalent form that needs no liveness. In an SSA program, call a name **useful** if a non-phi instruction or a terminator reads it, or if it is an operand of a phi-function whose result is useful. Then pruned SSA is minimal SSA with every phi-function whose result is not useful removed.

*Why the two forms agree.* Take a phi-function for $v$ at $y$ in minimal SSA, with result $v_k$. If $v$ is live on entry to $y$, follow a path from $y$ to a use with no assignment to $v$. Along it, the name of $v$ in force changes only at phi-functions for $v$, and each new phi-function takes the old name as the operand for the edge just crossed. So the use reads a name that a chain of phi-functions links back to $v_k$, and $v_k$ is useful. Conversely, if $v_k$ is useful, there is a chain $v_k$, then phi-functions at $z_1, \dots, z_j$, then a real use. Each step is a path in $G$ with no original assignment to $v$: when a name $v_a$ defined at block $a$ is read at the end of block $p$, $a$ dominates $p$ and the definition of $v_a$ is the last definition of $v$ on every path to that point, as the renaming proof on the [Cytron construction](/cytron-ssa-construction/) page shows, so the part of such a path after its last visit to $a$ assigns no $v$. Joined, these paths go from $y$ to a use with no assignment to $v$, so $v$ is live on entry to $y$.

### Variants

**Semi-pruned SSA form.** Briggs, Cooper, Harvey and Simpson (1998) call a variable **global** if some block reads it before any assignment to it in the same block. Semi-pruned SSA places phi-functions as minimal SSA does, but only for global variables:

$$y \in DF^+(S_v) \quad\text{and}\quad v \in \mathit{Global}.$$

A variable that is never global lives inside single blocks, so no join ever needs its value. The global set takes one pass over the instructions and no iteration. If $v$ is live on entry to any block, the path to its use enters the block of the use at the top, so $v$ is global. Hence

$$\text{pruned} \subseteq \text{semi-pruned} \subseteq \text{minimal}$$

as sets of phi-functions. The gap between semi-pruned and pruned comes from variables that are global but dead at some joins.

## Examples and non-examples

**The odd-sum loop.** The program from the [Cytron construction](/cytron-ssa-construction/) page has the variables `i`, `s`, `t1` and `t2`:

```
# params: n
B1:
  i = 0
  s = 0
  jump B2
B2:
  t1 = i < n
  br t1 B3 B6
B3:
  t2 = i % 2
  br t2 B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
```

Minimal SSA has five phi-functions: `i`, `s`, `t1` and `t2` at B2, and `s` at B5. On entry to B2, `t1` is dead because B2 assigns it before it reads it, and `t2` is dead because every path to a use of `t2` passes its assignment in B3. So pruned SSA has three phi-functions: `i` and `s` at B2, and `s` at B5. Neither `t1` nor `t2` is global, so semi-pruned SSA also has these three. This is the common case: temporaries that live in one block make most of the dead phi-functions.

**Semi-pruned is not pruned.** Here `x` is global, because B5 reads it first:

```
# params: a
B1:
  br a B2 B3
B2:
  x = 1
  jump B4
B3:
  x = 2
  jump B4
B4:
  x = 5
  jump B5
B5:
  ret x
```

$DF^+(S_x) = \{B4\}$. Minimal and semi-pruned SSA both put `x = phi [B2: x.1, B3: x.2]` at B4. B4 assigns `x` before any read, so `x` is not live on entry to B4, and pruned SSA has no phi-function at all.

**Dead phi-functions that read each other.** Change the odd-sum loop so that B4 does `x = i` and B6 returns `i`. Then `x` is assigned but never read. Minimal SSA has

```
B2:
  x.2 = phi [B1: x.1, B5: x.4]
  ...
B5:
  x.4 = phi [B3: x.2, B4: x.3]
```

Each of the two phi-functions has a reader, the other one, so a pass that removes only phi-functions with no readers removes neither. Neither is useful, because no real instruction reads `x`, and `x` is not live on entry to B2 or B5. Pruned SSA has neither. The useful test, a mark that starts from the real uses, finds this case; a count of readers does not.

**Pruned is not dead-code free.** A phi-function in pruned SSA may feed an instruction whose own result is never used. Pruning works on liveness in the original program and does not remove dead instructions. [Dead code elimination](/dead-code-elimination/) after construction can then remove more phi-functions.
## Related definitions

- [Static single assignment form](/static-single-assignment-form/): the general form; minimal SSA is the case with phi-functions at $DF^+(S_v)$.
- [Phi-function](/phi-function/): the merge pruning removes when the variable is dead.
- [Live variable analysis](/live-variable-analysis/): the backward analysis that gives $\mathit{LiveIn}$.
- [SSA construction](/ssa-construction-problem/): the problem, with a table of the minimal, semi-pruned and pruned forms.
- [Cytron SSA construction](/cytron-ssa-construction/): gives minimal SSA; with a liveness test in its placement loop it gives pruned SSA.
- [Braun SSA construction](/braun-ssa-construction/): looks up a variable only where it is read, so the phi-functions it creates are useful, and on reducible graphs it gives pruned SSA.
- [Def-use chains](/def-use-chains/): the useful test above is a mark over these chains.
- [SSA-based register allocation](/ssa-based-register-allocation/): dead phi-functions add interference, so allocators work on pruned SSA.

## References
