---
tag: T846M5
kind: algorithm
slug: braun-ssa-construction
name: Braun SSA construction algorithm
aliases:
- simple and efficient SSA construction
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: Builds SSA form directly from an AST or CFG by local value numbering and on-demand lookup in predecessors, with no dominance frontiers.
solves: [ssa-construction-problem]
model: word-ram
complexity:
  vars: {I: the number of instructions, V: the number of variables, B: the number of blocks, E: the number of edges}
  time: {worst: O(I + (B + E) V + B^2 V^2), average: O(I + (B + E) V + B^2 V^2), best: Θ(I + B + E)}
  space: {extra: O(I + (B + E) V)}
properties: {deterministic: true, recursive: true, online: true}
prereqs: [ssa-construction-problem, control-flow-graph]
see_also: [cytron-ssa-construction, pruned-ssa-form, static-single-assignment-form, local-value-numbering, reducible-flow-graph, tarjan-scc, ssa-cps-correspondence, abstract-syntax-tree]
sources:
  - paper: doi:10.1007/978-3-642-37051-9_6
    title: Matthias Braun, Sebastian Buchwald, Sebastian Hack, Roland Leißa, Christoph Mallon and Andreas Zwinkau, Simple and efficient construction of static single assignment form, Compiler Construction (CC 2013), LNCS 7791, pages 102-122
    locator: Section 2 (local value numbering, Algorithm 1; global value numbering and trivial phi-functions, Algorithms 2 and 3; incomplete CFGs and sealing, Algorithm 4), Section 3.2 (redundant SCCs of phi-functions, Lemma 1, Algorithm 5), Section 4 (pruned SSA, Theorem 1 on minimality for reducible graphs, Section 4.1 on time), Section 6 (evaluation in LLVM and libFirm)
  - paper: doi:10.1007/3-540-46423-9_8
    title: John Aycock and Nigel Horspool, Simple generation of static single-assignment form, Compiler Construction (CC 2000), LNCS 1781
    locator: phi-functions for every variable in every block, then removal of the redundant ones; minimal on reducible graphs
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the definition of minimal SSA form through converging paths, used by Braun et al. in Section 4
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 5 (SSA Reconstruction), on-demand lookup of reaching definitions after a transformation adds definitions
---

The Braun SSA construction builds [static single assignment form](/static-single-assignment-form/) while the compiler translates a program into its intermediate representation, with no dominator tree and no [dominance frontiers](/dominance-frontier/). Inside a block, it keeps the current value of each variable, as [local value numbering](/local-value-numbering/) does. When a block reads a variable that it has not assigned, the algorithm asks the predecessors, and puts a [phi-function](/phi-function/) at the block if there are several. A phi-function that merges only one value is removed at once. Braun, Buchwald, Hack, Leißa, Mallon and Zwinkau published it in 2013. They proved that the result is pruned, and minimal on reducible control flow graphs. A short extra pass makes it minimal on all graphs.

## In plain words

Translate the program block by block. In each block, remember the latest value of each variable. When the block reads a variable it did not set, look backward. With one predecessor, ask that block. With several, create a merge here first, so that a loop that leads back here stops at this merge, and then ask each predecessor. If all the answers are the same value, the merge is useless: delete it and use that value. A block whose incoming edges are not all known yet, such as a loop header before its loop body exists, gets a placeholder merge. Its inputs are filled in when the last edge arrives. The result has merges only where some later read needs one.

## The problem

The input is a procedure without phi-functions, given block by block in an order where each block comes after at least one of its predecessors, as a translator from an [abstract syntax tree](/abstract-syntax-tree/) produces it. A block is *filled* when all its instructions are translated. It is *sealed* when no more predecessors will be added. The output is a strict SSA form of the procedure with the same behaviour, as defined on the [SSA construction](/ssa-construction-problem/) page.

The implementation takes a whole [control flow graph](/control-flow-graph/) and replays this process: it fills the blocks in reverse postorder and seals each block as soon as all its predecessors are filled.

## The algorithm

```pseudo id=main
WRITE-VARIABLE(v, b, value)
L1  currentDef[v][b] <- value

READ-VARIABLE(v, b)
L2  if currentDef[v] has an entry for b then return currentDef[v][b]
L3  return READ-VARIABLE-RECURSIVE(v, b)

READ-VARIABLE-RECURSIVE(v, b)
L4  if b is not sealed then val <- new phi at b; incompletePhis[b][v] <- val
L5  else if b has one predecessor p then val <- READ-VARIABLE(v, p)
L6  else val <- new phi at b; WRITE-VARIABLE(v, b, val)
L7      val <- ADD-PHI-OPERANDS(v, val)
L8  WRITE-VARIABLE(v, b, val); return val

ADD-PHI-OPERANDS(v, phi)
L9  for each predecessor p of phi.block do append READ-VARIABLE(v, p) to phi
L10 return TRY-REMOVE-TRIVIAL-PHI(phi)

TRY-REMOVE-TRIVIAL-PHI(phi)
L11 same <- none; for each operand op of phi do
        if op = same or op = phi then continue
        if same != none then return phi        // two values: not trivial
        same <- op
L12 if same = none then same <- undefined     // start block, or unreachable
L13 replace every use of phi by same and delete phi
L14 for each phi-function u that used phi do TRY-REMOVE-TRIVIAL-PHI(u)
    return same

SEAL-BLOCK(b)
L15 for each (v, phi) in incompletePhis[b] do ADD-PHI-OPERANDS(v, phi)
    mark b sealed

BUILD(G)
L16 for each block b in reverse postorder do
        if all predecessors of b are filled then SEAL-BLOCK(b)
        fill b: for each read of v, use READ-VARIABLE(v, b);
                for each assignment to v, WRITE-VARIABLE(v, b, new name)
L17     for each successor s of b whose predecessors are all filled do SEAL-BLOCK(s)

REMOVE-REDUNDANT-PHIS(set of phi-functions)        // optional, Section 3.2
L18 for each SCC S of the graph "phi -> its phi operands", operands first do
        if |S| = 1 then continue
L19     outer <- operands of S that are not in S; inner <- members of S with no outer operand
L20     if |outer| = 1 then replace every member of S by the single outer value
L21     else if |outer| > 1 then REMOVE-REDUNDANT-PHIS(inner)
```

Lines L1 to L3 are local value numbering. If the block has no value for the variable, line L5 or L6 looks backward. Line L6 records the new phi-function as the block's value *before* line L7 reads the predecessors. A lookup that comes around a loop back to this block then finds the phi-function and stops. Without this step a loop would make the lookup recurse forever.

Lines L11 to L14 remove a *trivial* phi-function: one whose operands are only itself and one other value. Removing it can make the phi-functions that used it trivial, so line L14 checks them again. If a phi-function has no operand other than itself, it is in the start block or in unreachable code, and its value is undefined. The implementation gives such a variable the name `v.0` and defines `v.0 = 0` at the top of the entry, so that the result stays strict.

Line L4 handles a block whose predecessors are not all known. It creates an empty phi-function and waits. Line L15 completes it when the block is sealed. Sealing needs all predecessors to be filled, because a lookup there reads their final values. A loop header is sealed after the jump back from the loop body is added.

Lines L18 to L21 are the pass of Section 3.2 of the paper. Each phi-function in a set $S$ that takes values only from $S$ and from one outside value $w$ is equal to $w$. Irreducible control flow can leave such sets, and the trivial test alone does not see them.

## Example

Take the program from the [control flow graph](/control-flow-graph/) page that adds the odd numbers below $n$:

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

The reverse postorder is B1, B2, B6, B3, B4, B5.

1. B1 has no predecessors, so it is sealed. Filling it records `i.1` and `s.1`. B2 cannot be sealed: B5 is not filled.
2. B2 reads `i` and `n`. B2 is not sealed, so both get empty phi-functions, `i.2` and `n.1`. It defines `t1.1 = i.2 < n.1`. B3 and B6 have only B2 as predecessor, so they are sealed.
3. B6 reads `s`. It has one predecessor, so the lookup goes to B2, which has no value for `s` and is not sealed. B2 gets an empty phi-function `s.2`, and B6 returns `s.2`.
4. B3 reads `i`. The lookup goes to B2 and finds `i.2`. It defines `t2.1`.
5. B4 reads `s` and `i`, through B3, and finds `s.2` and `i.2`. It defines `s.3`. B5 now has both predecessors filled, so it is sealed.
6. B5 reads `i`. It is sealed and has two predecessors, so it gets the phi-function `i.3`, whose operands are `i.2` from B3 and `i.2` from B4. That is one value, so `i.3` is trivial and is replaced by `i.2`. B5 defines `i.4 = i.2 + 1`. B2 now has both predecessors filled, so it is sealed.
7. Sealing B2 completes its three empty phi-functions. `i.2` gets `i.1` from B1 and `i.4` from B5: it stays. `n.1` gets `n` from B1, and from B5 a new phi-function `n.2` in B5 whose operands are both `n.1`. So `n.2` is trivial and becomes `n.1`, and then `n.1` has the operands `n` and itself, so it is trivial too and becomes `n`. `s.2` gets `s.1` from B1, and from B5 a new phi-function `s.4` with the operands `s.2` from B3 and `s.3` from B4. Both stay.

The result is:

```
# params: n
B1:
  i.1 = 0
  s.1 = 0
  jump B2
B2:
  i.2 = phi [B1: i.1, B5: i.4]
  s.2 = phi [B1: s.1, B5: s.4]
  t1.1 = i.2 < n
  br t1.1 B3 B6
B3:
  t2.1 = i.2 % 2
  br t2.1 B4 B5
B4:
  s.3 = s.2 + i.2
  jump B5
B5:
  s.4 = phi [B3: s.2, B4: s.3]
  i.4 = i.2 + 1
  jump B2
B6:
  ret s.2
```

The gaps in the version numbers are the removed phi-functions. The three phi-functions that are left are exactly those of [pruned SSA form](/pruned-ssa-form/). The [Cytron construction](/cytron-ssa-construction/) also puts dead phi-functions for `t1` and `t2` at B2. Here, no block ever asks for `t1` or `t2` at B2, so those phi-functions are never created.

**Irreducible flow.** In this program, B2 and B3 form a loop with two entries from B1:

```
# params: c, d
B1:
  x = 1
  br c B3 B2
B2:
  br d B3 B4
B3:
  y = x + 1
  br y B2 B4
B4:
  ret x
```

Only B1 assigns `x`, so minimal SSA has no phi-function for it. The basic algorithm builds `x.3 = phi [B1: x.1, B3: x.2]` at B2 and `x.2 = phi [B1: x.1, B2: x.3]` at B3. Neither one is trivial, because each one has two operands other than itself: `x.1` and the other phi-function. Together they only pass `x.1` around. The SCC pass finds the set $\{x.2, x.3\}$ with the single outside value `x.1`, and replaces both by `x.1`. Then the phi-function for `x` at B4 becomes trivial, and the same happens for the parameter `d`.

## Correctness

The full proof is in the proof file. It has four parts.

- **Values.** The builder attaches a name of $v$ to the points where a lookup happens. At the top of a block, the name is either the block's phi-function or a name that every predecessor has at its end. A removed phi-function forwards to a value equal to all its operands. Induction over the steps of a run shows that every name holds the current value of its variable, so the output reads the same values and takes the same branches as the input.
- **Strictness.** Walk any path backward from a use. The name stays attached until the path reaches its definition, so the definition dominates the use.
- **No dead phi-function.** Every lookup is caused by a real read, through a chain of blocks without an assignment to the variable. So every phi-function sits at a block where its variable is live.
- **Minimal on reducible graphs.** This is Theorem 1 of Braun et al. Suppose a phi-function is not needed and not trivial. It must have an operand that is also a phi-function that is not needed, in a block that does not dominate it. Following these operands gives a cycle. On a reducible graph the loop entry dominates the rest of the cycle, which is a contradiction.

## Complexity

Let $I$ be the number of instructions, $V$ the number of variables, $B$ the number of blocks and $E$ the number of edges.

- **Lookups.** Each pair (variable, block) is looked up recursively at most once, because the answer is stored in `currentDef`. So there are $O(BV)$ phi-functions and $O(EV)$ operand reads. Braun et al. show that the basic algorithm runs in $\Theta(I + (B + E)V)$ in the worst case, and that this matches a lower bound: some programs need $\Theta(B)$ phi-functions with $\Theta(E)$ operands for each variable.
- **Trivial phi-functions.** Each removal rechecks the users. With a cache of two witness operands per phi-function, Braun et al. bound all checks by $O(B^2 V^2)$.
- **SCC pass.** $O(I + B(B + E)V^2)$, because each recursive step works on a strictly smaller set of phi-functions.

In practice, the paper's LLVM implementation of the marker variant was as fast as LLVM's tuned Cytron implementation: compiling SPEC CINT2000 executed 0.28% fewer instructions in total. The best case is a program where no variable is read outside the block that assigns it: then $\Theta(I + B + E)$.

## Properties

- **Pruned.** It never creates a phi-function that no read asks for, so no phi-function is dead.
- **Minimal on reducible graphs.** With all trivial phi-functions removed, the placement is the minimal one. On irreducible graphs it may keep extra cycles of phi-functions, unless the SCC pass runs.
- **No dominance information.** It needs only the predecessors of each block.
- **Incremental.** It works while the graph is still being built, block by block, as long as the translator says when a block is sealed.
- **Strict.** Every definition dominates its uses.
- **Recursive.** The lookup recurses along chains of predecessors, as deep as the longest such chain. Production code may need an explicit stack.

## Variants and improvements

- **On-the-fly optimizations.** Section 3.1 of the paper runs local optimizations during construction: constant folding, arithmetic simplification, common subexpression elimination with the value numbers, and copy propagation, which records `y`'s value as the value of `x` for `x = y`. These can remove phi-functions and even branches. With copy propagation, the output is no longer conventional SSA, and [out-of-SSA translation](/out-of-ssa-translation/) must handle the [lost copy and swap problems](/lost-copy-and-swap-problems/).
- **Fewer temporary phi-functions.** The marker variant only marks a block during the lookup and creates a phi-function there only if the lookup comes back to it or finds two different values. The SCC variant runs [Tarjan's algorithm](/tarjan-scc/) during the lookup and creates only needed phi-functions (Section 3.3).
- **Simpler recheck.** If the IR keeps no list of users, recheck the one remaining operand instead of the users. The paper notes that this gives minimal SSA in most cases, but not all.
- **SSA reconstruction.** After a transformation adds new definitions of a value, such as live range splitting, the same lookup finds the right definition for each use and places the missing phi-functions (Section 5.1).
- **Continuation-passing style.** Instead of phi-functions, the same lookup adds parameters to local functions and arguments to the calls that reach them; see [the SSA-CPS correspondence](/ssa-cps-correspondence/).
- **Earlier work.** Aycock and Horspool (2000) put a phi-function for every variable in every block and then removed the redundant ones, which is also minimal on reducible graphs. Braun et al. describe their SCC pass as a generalization of those local simplifications.

## When to use it

Use it in a front end or a JIT compiler that builds SSA form straight from the syntax tree or the bytecode, with no non-SSA form in between. It needs no dominator tree, no frontiers and no liveness, and it gives pruned SSA without a separate dead-code pass. The paper's authors used variants of it in the libFirm compiler library. When the compiler already has a complete graph, its dominator tree, and needs minimal SSA on irreducible code without an extra pass, the [Cytron construction](/cytron-ssa-construction/) is the standard choice.

## Pitfalls

- **Sealing too early.** A sealed block reads its predecessors at once. If one of them is not filled, the lookup misses its later assignments and gives a wrong value. Seal a block only when all its predecessors are filled.
- **Forgetting to seal.** An incomplete phi-function in a block that is never sealed has no operands. Seal every block at the end.
- **Recording the phi-function too late.** Line L6 must record the phi-function before line L7 reads the predecessors. Otherwise a loop makes the lookup recurse forever.
- **Checking a half-built phi-function.** The removal of one phi-function rechecks its users. If a user is still collecting its operands, the test sees only some of them and can remove it by mistake. Check a phi-function only after its last operand is in.
- **Stale references.** After a phi-function is replaced, every place that stored it, including `currentDef`, must see the new value. Use a list of users, or a forwarding map that is resolved on every read.
- **Expecting minimal SSA on irreducible graphs.** Without the SCC pass, cycles of phi-functions that carry one value can remain.

## Implementations

## History

Aycock and Horspool (2000) built SSA form by placing phi-functions everywhere and removing those that are not needed, and showed that this is minimal on reducible graphs. Braun, Buchwald, Hack, Leißa, Mallon and Zwinkau presented the on-demand construction at Compiler Construction 2013. Their compiler library libFirm had long used a variant of it. They proved that it gives pruned SSA, and minimal SSA on reducible graphs, gave the SCC pass for irreducible graphs, and compared an LLVM implementation with LLVM's Cytron-based construction. Section 5.1 of the paper applies the same lookup to SSA reconstruction, which Chapter 5 of the SSA book by Rastello and Bouchez Tichadou (2022) treats in full.

## References
