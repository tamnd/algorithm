---
tag: 3N51WA
kind: algorithm
slug: copy-propagation
name: Copy propagation
aliases:
- copy folding
area: compilers-and-program-analysis/optimizations
level: intro
summary: Replaces uses of x after a copy x = y by y while neither changes, so that the copy can be removed as dead code.
model: word-ram
complexity:
  vars: {n: the number of instructions and terminators, b: the number of blocks, c: the number of copies, v: the number of names, R: the number of rounds}
  time: {worst: O(R b n c + c b n v)}
  space: {extra: O(b (c + v) + n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [three-address-code, control-flow-graph, dataflow-analysis, live-variable-analysis]
see_also: [dead-code-elimination, common-subexpression-elimination, local-value-numbering, reaching-definitions, sparse-conditional-constant-propagation, static-single-assignment-form, register-coalescing-problem, lost-copy-and-swap-problems]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.1.5 (Copy Propagation) and Section 9.2 (Introduction to Data-Flow Analysis)
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 12.5 (Copy Propagation), the local form and the global form with the sets of available copies
  - paper: doi:10.1145/512927.512945
    title: Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL), 1973, 194-206
    locator: the iterative algorithm for a dataflow problem with a meet operation, used here with intersection for the available copies
---

Copy propagation replaces a use of a name `x` by `y` when the copy `x = y` is the last write to `x` on every path to the use and `y` has not changed since. The fact that it needs is *available copies*, a forward dataflow problem with intersection as the meet, much like [available expressions](/available-expressions/). The pass does not make the program faster by itself. It removes the reasons to keep the copy, and the copy then dies and goes away, as in [dead code elimination](/dead-code-elimination/). Copies come from [common subexpression elimination](/common-subexpression-elimination/), [local value numbering](/local-value-numbering/), inlining and the translation out of [static single assignment form](/static-single-assignment-form/), so this pass runs often.

## In plain words

After `x = y`, the two names hold the same number. A later line that reads `x` can read `y` instead, as long as nothing wrote to `x` or to `y` in between. If every reader of `x` now reads `y`, nobody needs `x`, and the line `x = y` can be deleted. The hard part is "nothing wrote in between". The program can reach the reader along different roads, and the copy must be the latest news on every road. A write through a pointer can also change a name without naming it, so the pass must be careful with names whose address the program takes.

## The problem

The input is a program of the toy IR of [three-address code](/three-address-code/): a [control flow graph](/control-flow-graph/) of blocks with no phi-functions. The output is a program that has the same outcome on every input, the same return value, the same trap or no end, and that has fewer copies. A copy is an instruction `x = y` with `y` a name other than `x`. A copy of a constant, `x = 5`, is a constant, and spreading it is constant propagation, a different problem.

A pair $(x, y)$ is *available* at a point $q$ if on every path from the entry to $q$ there is a copy `x = y`, and after the last such copy on the path no instruction writes `x` or `y`. Then at $q$ the two names have the same value in every run, and a use of `x` at $q$ can read `y`.

## The algorithm

S is a set of pairs. A name is *address-taken* if the program has an instruction `p = &x` for it. A store or a call can change such a name through a pointer, so it removes the pairs that mention one.

```pseudo id=main
COPY-PROPAGATION(P)
L1  repeat
L2      IN <- AVAILABLE-COPIES(P)
L3      count <- 0
L4      for each block B of P do
L5          S <- IN[B]
L6          for each instruction I of B, in order, and then the terminator of B do
L7              for each operand u of I that is a name do
L8                  while S holds a copy (u, y) do u <- y
L9              if some operand changed then replace them in I; count <- count + 1
L10             S <- TRANSFER(I, S)
L11 until count = 0
L12 delete every copy x = y whose x is dead after it, and every x = x, until none is left
L13 return P

AVAILABLE-COPIES(P)
L14 C <- the set of copies (x, y) in P, with y a name other than x
L15 OUT[B] <- C for every block B
L16 repeat, visiting the reachable blocks in reverse postorder, until no OUT[B] changes
L17     IN[B] <- empty if B is the entry, else the intersection of OUT[p] over the predecessors p
L18     OUT[B] <- TRANSFER over the instructions of B, from IN[B]

TRANSFER(I, S)
L19 if I is a store or a call then remove the copies that mention an address-taken name
L20 if I defines x then remove every copy (x, .) and (., x)
L21 if I is x = y with y a name other than x then add (x, y)
L22 return S
```

Lines L14 to L18 solve the [dataflow analysis](/dataflow-analysis/) problem of available copies. It is a must problem, so OUT starts at the full set and only shrinks, and the meet at a join is intersection. The entry starts from the empty set: on entry no copy has run. A block that the entry does not reach keeps an empty IN, so that nothing is rewritten in code that never runs.

Line L8 follows chains. After `b = a; c = b`, a use of `c` becomes a use of `a`. The sets that the algorithm builds have at most one pair for each destination and no cycle, so the chain ends. Line L10 updates S with the rewritten instruction, so a copy `c = b` that became `c = a` adds the pair $(c, a)$.

Line L1 repeats the rounds, because one round does not find everything. In the example below, a copy is killed on one path in the first round, and only its rewritten form survives that path in the next round. Line L12 uses [live variable analysis](/live-variable-analysis/) and never deletes a copy to an address-taken name, since a load through a pointer can read it.

## Example

The parameters are `a` and `n`.

```
entry:
  b = a
  c = b
  br n left right
left:
  d = c + 1
  b = 7
  jump join
right:
  d = c * 2
  jump join
join:
  e = c + b
  e = e + d
  ret e
```

**Round 1.** The available sets on entry are $\{(b, a), (c, b)\}$ for `left` and `right`. In `entry`, `c = b` becomes `c = a`. In `left` and `right`, `c` follows the chain $c \to b \to a$, so `d = c + 1` becomes `d = a + 1` and `d = c * 2` becomes `d = a * 2`. At `join` the set is empty: `b = 7` in `left` removes both $(b, a)$ and $(c, b)$, because each mentions `b`.

**Round 2.** Now `entry` holds `c = a`. The write `b = 7` does not mention `c` or `a`, so $(c, a)$ is available at `join` on both paths, and `e = c + b` becomes `e = a + b`. The use of `b` at `join` stays, because on the path through `left` it is 7.

**Round 3** changes nothing. Then `c = a` is dead and line L12 deletes it. `b = a` stays, because `join` reads `b` on the path through `right`.

```
entry:
  b = a
  br n left right
left:
  d = a + 1
  b = 7
  jump join
right:
  d = a * 2
  jump join
join:
  e = a + b
  e = e + d
  ret e
```

For $a = 5$ both programs return 18 when $n \ne 0$ and 20 when $n = 0$, and the new one executes one instruction less on every run.

## Correctness

The full proof is in the proof file. It has four steps.

1. **TRANSFER is sound.** If every pair of S holds before an instruction, every pair of TRANSFER(I, S) holds after it. A write to a name removes every pair that mentions it. A store or a call can only change names that are address-taken, through a pointer that `p = &x` made, and line L19 removes those pairs.
2. **The analysis is sound.** The OUT sets only shrink, so the loop of line L16 stops, at a solution of the equations of lines L17 and L18. By induction on the steps of a run, every pair available at a point holds whenever the run is there: the entry starts from the empty set, and along an edge IN is a subset of the OUT of the predecessor that the run came from.
3. **A round keeps every state.** Each replaced operand follows pairs that hold, so it has the same value. So the rewritten instruction reads the same values, writes the same value, and traps on the same zero divisor. The old and the new program go through the same states, step by step.
4. **Line L12 keeps the outcome.** A deleted copy writes a name that no later instruction reads before it is written again, and that no pointer can reach. The two programs agree on every live name and on memory, and so they have the same outcome.

Each round is correct on its own, so the result is correct for any number of rounds. The implementation stops after at most $n + 1$ rounds.

## Complexity

One pass of the analysis applies TRANSFER to each of the $n$ instructions, at cost $O(c)$ with sets of the $c$ copies. In reverse postorder the must problem needs at most $b + 1$ passes, and on a reducible graph only the loop connectedness plus two, where the loop connectedness is the largest number of back edges on a path without repeats (see the [Kam and Ullman bound](/kam-ullman-iteration-bound/)). A round is then $O(b n c)$, and the rewrite adds $O(n c)$. Each pass of line L12 solves liveness in $O(b n v)$, and it deletes at least one copy, so there are at most $c + 1$ passes. With bit vectors of $w$ bits the set operations are $w$ times faster. The space is the IN and OUT sets of every block, $O(b(c + v))$, and the program. In practice $R$ is two or three.

## Properties

- **It never costs more.** A round replaces only operands, and line L12 only deletes copies, so every run executes at most as many instructions as before.
- **It needs a cleanup.** Without line L12, or a dead code pass after it, copy propagation saves nothing: it only moves uses from `x` to `y`.
- **It can lengthen live ranges.** After the rewrite, `y` is live up to the last former use of `x`, so `y` and other names can now interfere in [register allocation](/register-allocation-problem/).
- **It is conservative.** A path that cannot run in practice still kills a pair, and every store kills every pair with an address-taken name.

## Variants and improvements

- **Local copy propagation.** Inside one [basic block](/basic-block/), start from the empty set and apply lines L6 to L10. No dataflow analysis is needed.
- **On SSA form.** In [static single assignment form](/static-single-assignment-form/) each name has one definition and is never written again. So after `x = y`, every use of `x` can read `y`, and the copy is deleted, with no analysis at all. Copies in phi-functions need more care, see the pitfalls.
- **With def-use chains.** [Reaching definitions](/reaching-definitions/) and [def-use chains](/def-use-chains/) can drive the same rewrite: a use of `x` is rewritten if the copy `x = y` is the only definition of `x` that reaches it and no path from the copy to the use writes `y`. The second condition is the available-copies fact.
- **With constants and values.** [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) handles copies of constants, and [global value numbering](/global-value-numbering/) finds names that are equal by other means than a copy.
- **Coalescing.** A register allocator removes copies in a different way: it gives `x` and `y` the same register when they do not interfere, which is the [register coalescing problem](/register-coalescing-problem/).

## When to use it

Run copy propagation after any pass that leaves copies, such as common subexpression elimination, value numbering, inlining or out-of-SSA translation, and follow it by dead code elimination. On SSA form, use the trivial rule above. In a compiler with alias information, use it in TRANSFER in place of the address-taken test, so that a store kills only the pairs whose names it can reach.

## Pitfalls

- **A store through a pointer.** In `p = &x; y = x; *p = 5; z = y`, the store changes `x`. Rewriting `z = y` as `z = x` gives 5, not the old value. The pair $(y, x)$ must die at the store, which line L19 does because `x` is address-taken.
- **A kill on one path.** After `b = a`, the pair $(b, a)$ is not available at a join if one incoming path writes `b`. Using "some path has the copy" gives a wrong value on the other path.
- **Writes to the source.** After `y = a`, a later `a = a + 1` inside a loop kills $(y, a)$. Forgetting the kill of $(\cdot, x)$ on line L20 keeps a stale pair.
- **The wrong direction.** The rule replaces a use of `x` by `y`, the source. Replacing uses of `y` by `x` is wrong when `x` is written again.
- **Phi-functions after propagation on SSA.** Propagating copies into phi operands can make the live ranges of the phi results overlap. A naive translation out of SSA then loses a value, the [lost copy problem](/lost-copy-and-swap-problems/).
- **Deleting copies to address-taken names.** A load through a pointer is a use that liveness on names does not see. Such copies stay.

## Implementations

## History

Copy propagation is one of the classical global optimizations of the optimizing compilers of the 1960s and 1970s. Kildall gave in 1973 the iterative algorithm and lattice framework that solves problems such as available copies. The dragon book presents copy propagation with the sets of available copies and an intersection at joins, and Muchnick gives the local and global forms and the place of the pass among the early optimizations. In SSA-based compilers the pass is mostly a side effect of SSA construction and of value numbering.

## References
