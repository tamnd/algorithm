---
tag: VFFWX5
kind: algorithm
slug: aggressive-dead-code-elimination
name: Aggressive dead code elimination
aliases:
- ADCE
- mark-sweep dead code elimination
area: compilers-and-program-analysis/optimizations
level: core
summary: Marks instructions with side effects as live, then marks what they depend on through data and control dependence, and deletes the rest.
model: word-ram
complexity:
  vars: {n: the number of statements (instructions and terminators), b: the number of blocks}
  time: {worst: O(b^2 n + n^2)}
  space: {extra: O(n^2 + b^2)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [dead-code-elimination, post-dominance, control-dependence, reaching-definitions]
see_also: [dominance-frontier, static-single-assignment-form, program-dependence-graph, program-slicing, def-use-chains, sparse-conditional-constant-propagation, copy-propagation, cytron-ssa-construction]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, 451-490
    locator: Section 7.1 (Dead Code Elimination), pp. 478-481 and Figure 17, the marking of live statements through definers and control dependence, and footnote 11 on the replacement of a dead branch
  - paper: doi:10.1145/24039.24041
    title: Jeanne Ferrante, Karl J. Ottenstein and Joe D. Warren, The program dependence graph and its use in optimization, ACM Transactions on Programming Languages and Systems 9(3), 1987, 319-349
    locator: the definition of control dependence by post-dominance, and its computation by a walk up the post-dominator tree
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 10 (Scalar Optimizations), the part on eliminating useless code, with the algorithms Mark and Sweep and the jump to the nearest marked post-dominator
---

Aggressive dead code elimination treats every statement as useless until it is shown to be useful. It starts from the statements whose effect someone can see, such as returns, stores, calls and operations that may trap. Then it marks the statements they depend on: the definitions that reach the names they read, and the branches that decide whether they run. Everything left unmarked is deleted, and an unmarked branch becomes a jump. Unlike [dead code elimination](/dead-code-elimination/) based on liveness, it removes values that only feed themselves around a loop, branches with no useful code behind them, and whole loops that compute nothing. The marking resembles the mark phase of a [mark-and-sweep](/mark-and-sweep/) garbage collector, but it is not garbage collection: it works on the statements of a program at compile time, not on objects in memory at run time.

## In plain words

Start from the lines of the program that matter on their own: a line that returns the answer, writes to memory, calls a function, or can crash. Mark them. Then ask, for each marked line, which earlier lines computed the numbers it reads, and which tests decide whether it runs. Mark those too, and ask the same about them. When nothing new gets marked, every line without a mark is useless, so delete it. A test that guards nothing marked is useless too. The program jumps straight to the next place where marked work happens. The method assumes that a loop which does nothing useful also ends, because it deletes such loops.

## The problem

The input is a program of the toy IR of [three-address code](/three-address-code/) without phi-functions, in which every block reaches a `ret`. The output is a program that has the same outcome on every input on which the input program ends: the same return value or the same trap. It should contain as few statements as possible. A *statement* is an instruction or a terminator.

Deciding which statements can really affect the outcome is undecidable (see the [full employment theorem](/full-employment-theorem/)). The algorithm gives a safe approximation through two kinds of dependence. A statement $S$ is *data dependent* on a definition $D$ if $D$ defines a name that $S$ reads and $D$ reaches $S$, in the sense of [reaching definitions](/reaching-definitions/). A block $Y$ is *[control dependent](/control-dependence/)* on a block $C$ if $Y$ [post-dominates](/post-dominance/) a successor of $C$ but does not strictly post-dominate $C$: one way out of $C$ forces $Y$ to run, and another can skip it. Post-dominance is computed with a virtual exit node after every `ret` block.

## The algorithm

A statement is *critical* if it is a `ret`, a store, a call, an `alloc`, an operation that may trap (`/` or `%` by a divisor that may be zero, a shift by a count that may be outside 0 to 63), or a definition of an address-taken name, which a load or a call can read through a pointer. A block is *useful* if it holds a marked statement.

```pseudo id=main
AggressiveDeadCode(P)
L1  compute the post-dominator tree with a virtual exit, the control dependences and the reaching definitions of P
L2  Marked <- empty; Work <- empty
L3  for each statement S of a reachable block do
L4      if S is critical then mark S and add S to Work
L5  while Work is not empty do
L6      take a statement S out of Work
L7      for each definition D that reaches S and defines a name that S reads do
L8          if D is not marked then mark D and add D to Work
L9      for each block C on which the block of S is control dependent do
L10         if the branch of C is not marked then mark it and add it to Work
L11 for each reachable block B do
L12     delete the unmarked instructions of B
L13     if the terminator of B is a branch that is not marked then
L14         N <- ipdom(B); while N is not useful do N <- ipdom(N)
L15         replace the branch by jump N
L16 delete the blocks that the entry no longer reaches
L17 return P
```

Lines L2 to L10 are the mark phase and lines L11 to L16 the sweep. A jump is never marked and never deleted. Line L9 uses the control dependences, which are the reverse [dominance frontier](/dominance-frontier/): the blocks in the dominance frontier of $Y$ in the reverse graph. The implementation finds them as Ferrante, Ottenstein and Warren do. For each branch block $C$ and each successor $s$, it walks up the post-dominator tree from $s$ to $\mathrm{ipdom}(C)$, and every block on the way, without $\mathrm{ipdom}(C)$, is control dependent on $C$.

Line L14 is the subtle step. A branch that is not marked decides nothing that matters, so the program may go straight to the first useful block that every path from $B$ reaches, the nearest useful post-dominator. Footnote 11 of Cytron and others says that a dead branch can become a jump "to any one of its prior targets". That is wrong for a branch that closes a useless loop: jumping back to the top of the loop never ends. Cooper and Torczon jump to the nearest marked post-dominator, as here.

## Example

The parameters are `a` and `b`.

```
entry:
  s = 0
  i = 0
  q = a / b
  jump h
h:
  t = i < 3
  br t body done
body:
  s = s + i
  k = s & 1
  br k odd even
odd:
  s = s + 1
  jump join
even:
  s = s - 1
  jump join
join:
  i = i + 1
  jump h
done:
  r = a + i
  ret r
```

The critical statements are `q = a / b`, which may trap, and `ret r`. The return reads `r`, so `r = a + i` is marked, then `i = 0` and `i = i + 1`, the definitions of `i` that reach it. `join` is now useful. It post-dominates `body`, a successor of `h`, but not `h` itself, because `h` can go to `done`. So `join` is control dependent on `h`, and the branch of `h` is marked, and with it `t = i < 3`. Nothing marks `s`, `k`, the branch of `body`, or the blocks `odd` and `even`.

The sweep deletes the unmarked instructions. The branch of `body` becomes a jump to `join`, its immediate post-dominator, which is useful. Then `odd` and `even` are unreachable and go away.

```
entry:
  i = 0
  q = a / b
  jump h
h:
  t = i < 3
  br t body done
body:
  jump join
join:
  i = i + 1
  jump h
done:
  r = a + i
  ret r
```

For $a = 5$, $b = 2$ both programs return 8. The first one executes 35 statements and the second 22. For $b = 0$ both trap at the division. Dead code elimination based on liveness removes nothing from `s` here: `s = s + i` reads `s` around the back edge, so `s` stays live, and the branch of `body` reads `k`.

## Correctness

The full proof is in the proof file. It assumes that no name is read before it is defined and that every block reaches a `ret`, and it compares runs of the input that end.

1. **The marks are closed.** At the end, every critical statement is marked. Every definition that reaches a name read by a marked statement is marked. And every branch on which a useful block is control dependent is marked.
2. **An unmarked branch leads to its nearest useful post-dominator.** Let $B$ end with an unmarked branch, and follow any path from $B$ to the first useful block $Y$ after it. If $Y$ did not strictly post-dominate $B$, then $Y$ would be control dependent on $B$ or on a block between them, and that block's branch would be marked, which makes it useful. So $Y$ strictly post-dominates $B$, and a short argument on the post-dominator tree shows that $Y$ is the nearest useful one, the target $N$ of line L14.
3. **The same marked statements run.** Follow the old and the new program from block to block. They agree at the start of each block that both visit. Inside it, the old program runs every instruction and the new one only the marked ones, and the unmarked ones cannot trap and write no memory. At an unmarked branch the old program wanders through blocks with no marked statement and arrives at $N$, where the new one jumps.
4. **They read the same values.** A marked statement reads a name whose last write in the old run was a definition that reaches it, and so is marked, or a store or call, which is critical. By induction that write ran in the new program too, with the same value, and nothing in between changed the name.

So on every input on which the old program ends, the new one ends in the same way and runs at most as many statements. On a run that loops forever inside a loop with no marked statement, the new program may end. This is the termination assumption of the algorithm.

## Complexity

With $n$ statements and $b$ blocks, the implementation computes reaching definitions by iteration over sets of up to $n$ definitions, in $O(b^2 n)$ time, and the definitions that reach each statement in $O(n^2)$. The post-dominator tree by the iterative algorithm of Cooper, Harvey and Kennedy and the control dependences by the tree walk take $O(b^2)$. Each statement enters the work list at most once and looks at its reaching definitions and its control dependences, which is $O(n^2 + n b)$ in all. The sweep is $O(n + b)$. On [static single assignment form](/static-single-assignment-form/) every use has one definition, so the data part of the marking is linear, and the whole algorithm runs in time linear in the program plus the size of the control dependences, as in Cytron and others.

## Properties

- **Optimistic.** Every statement is assumed dead until proven useful. This finds dead cycles, values that feed only themselves, which a pessimistic pass based on liveness cannot remove.
- **It removes control flow.** Branches with nothing useful behind them become jumps, and whole loops that compute nothing disappear.
- **It never costs more on a run that ends.** The new program runs a subset of the instructions of the old one, and no more terminators.
- **It needs post-dominators.** Every block must reach an exit. A block in an infinite loop with no exit has no post-dominator; a compiler adds a fake edge from such a loop to the exit before it runs the algorithm.

## Variants and improvements

- **On SSA form.** Cytron and others run the algorithm on [static single assignment form](/static-single-assignment-form/). Each use has one definition, and a phi-function is marked like any other statement. When a phi-function is marked, the branches that decide which of its operands arrives must stay too: they mark the last statement of each predecessor block of the phi.
- **Dependence graphs.** The marking is a backward walk on the [program dependence graph](/program-dependence-graph/). The same walk from a chosen statement, not from all critical ones, is backward [program slicing](/program-slicing/).
- **Keeping loops that may not end.** A language in which an infinite loop without effects is a valid program needs a stronger rule: mark the branch of every loop that is not known to end.
- **With constant propagation.** [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) proves that some branches always go one way, and aggressive dead code elimination then removes the dead side and the values that only fed it.

## When to use it

Use aggressive dead code elimination after transforms that leave behind computations and branches that no longer matter, such as constant propagation, inlining and [copy propagation](/copy-propagation/). It is more costly than a liveness pass because it needs post-dominators and control dependences, so compilers run the simple pass often and the aggressive one a few times. Do not use it where a loop that runs forever and does nothing is a valid behavior that must be kept, unless the loops it removes are known to end.

## Pitfalls

- **The wrong jump target.** Replacing an unmarked branch by a jump to one of its old targets can turn a loop that ends into one that does not. In `w: j = j + 1; k = j < 5; br k w out`, with `j` used nowhere else, jumping to `w` loops forever. The nearest useful post-dominator is `out`.
- **Loops that do not end.** In `h: i = i + 0; br a h done`, nothing in `h` is useful, so the branch becomes a jump to `done`. For $a \ne 0$ the old program never ends and the new one returns. This is the price of the termination assumption.
- **Effects that are not stores.** A trap is an outcome. An operation that may trap must be critical, or the pass deletes a division by zero. Volatile loads, input and output, and calls to functions that are not known to be pure are critical too.
- **Hidden reads through pointers.** A load through a pointer can read an address-taken name without naming it, so no reaching definition connects them. Treat the definitions of such names as critical, or connect them through [alias analysis](/alias-analysis/).
- **Blocks with no exit.** Without a virtual exit, or with a block that reaches no exit, post-dominance is not defined. Add the virtual exit, and add fake edges from infinite loops.

## Implementations

## History

Dead code elimination by marking useful statements goes back to the optimizing compilers of the 1970s, and the name "aggressive" refers to its optimistic start. Ferrante, Ottenstein and Warren defined control dependence through post-dominance in 1987 and used it for the program dependence graph. Cytron, Ferrante, Rosen, Wegman and Zadeck gave the algorithm on SSA form in 1991, with control dependence computed as the dominance frontier of the reverse graph. Its footnote on how to replace a dead branch was later corrected: Cooper and Torczon jump to the nearest marked post-dominator.

## References
