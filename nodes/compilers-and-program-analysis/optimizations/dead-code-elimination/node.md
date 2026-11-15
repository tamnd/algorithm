---
tag: 4S85JP
kind: technique
slug: dead-code-elimination
name: Dead code elimination
aliases:
- DCE
- dead store elimination
area: compilers-and-program-analysis/optimizations
level: intro
summary: Removes instructions whose results are never used and that have no side effects.
prereqs: [three-address-code, control-flow-graph, live-variable-analysis]
see_also: [aggressive-dead-code-elimination, copy-propagation, common-subexpression-elimination, sparse-conditional-constant-propagation, def-use-chains, alias-analysis, escape-analysis, program-slicing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.1.6 (Dead-Code Elimination) and Section 9.2.5 (Live-Variable Analysis)
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, 451-490
    locator: Section 7.1 (Dead Code Elimination), the marking of useful statements from the statements that affect the output
  - paper: doi:10.1145/178243.178256
    title: Jens Knoop, Oliver Rüthing and Bernhard Steffen, Partial dead code elimination, Proceedings of the ACM SIGPLAN 1994 Conference on Programming Language Design and Implementation (PLDI), 1994, 147-158
    locator: the sinking of assignments that are dead on some paths, so that they become dead on all paths and can be removed
  - url: https://cwe.mitre.org/data/definitions/14.html
    title: MITRE, CWE-14, Compiler Removal of Code to Clear Buffers
    locator: the removal of a store that clears a secret before the memory is freed
---

Dead code elimination removes an instruction whose result no later instruction reads and that does nothing else. An instruction that "does nothing else" writes only its own destination: it is not a store, not a call that may have an effect, and it cannot trap. The fact that the rewrite needs is "the destination is not live after the instruction", which [live variable analysis](/live-variable-analysis/) computes. Other passes create most dead code: [copy propagation](/copy-propagation/) leaves copies that nobody reads, [common subexpression elimination](/common-subexpression-elimination/) leaves the old computations, and [sparse conditional constant propagation](/sparse-conditional-constant-propagation/) leaves the inputs of folded branches.

## In plain words

A line that computes a number nobody ever looks at is wasted work, and the compiler can delete it. But some lines do more than compute a number. A line that writes to memory, calls another function, or can crash the program, for example by a division by zero, has an effect that someone can see. Such lines stay, even if their number is never used. Deleting one line can make another line useless, because the deleted line was the only reader of its inputs. So the compiler repeats the deletion until no line is left to delete.

## When it applies

Fix an instruction $I$ at a point of the program. $I$ is *dead*, and may be removed, when both conditions hold:

- **No use.** If $I$ defines a name $x$, then $x$ is not live after $I$: on no path from $I$ is $x$ read before it is written again. If $x$ is address-taken, a load or a call can read it through a pointer, so $x$ counts as read by every load and every call, or the instruction stays.
- **No other effect.** $I$ writes nothing but $x$, and every run of $I$ ends normally. In the toy IR this holds for `x = k`, copies, `alloc`, `addr`, loads, and operations that cannot trap. It does not hold for a store, for a call to a function that is not known to be pure, to end, and to never trap, and for an operation that may trap: `/` and `%` by a divisor that may be zero, and shifts by a count that may be outside 0 to 63.

The second condition is about the target language. In the toy IR a trap is an outcome, so a division by zero must stay. On a real machine a load through an invalid pointer can fault, so a load is removable only if the pointer is known to be valid, and a Java compiler that removes a load must keep its null check.

## The template

**The rewrite.** Solve live variable analysis over the [control flow graph](/control-flow-graph/). Walk each block backward from the live set at its end. At each instruction $I$ that defines $x$: if $x$ is not in the live set, $x$ is not address-taken, and $I$ has no other effect, delete $I$. Otherwise keep $I$, remove $x$ from the live set and add the names that $I$ reads. Stores and calls add the names they read and remove nothing. A terminator adds the name it reads. Repeat the analysis and the walk until a walk deletes nothing.

**Legality.** The rewrite uses two facts at the instruction: the destination is not in $\mathrm{LIVE}_{out}$, a may property computed with union at joins and the empty set at exits, and the instruction is free of effects, in the sense above.

**Profit.** The cost model is the number of instructions executed on each run. Each run executes the same instructions as before, minus the deleted ones, so no run becomes slower. The code also gets smaller, live ranges get shorter, and [register allocation](/register-allocation-problem/) gets an easier problem. The cost is compile time: each repeat solves liveness again. A worklist driven by [def-use chains](/def-use-chains/) avoids the repeats, see the variations.

**Proof that behavior stays the same.** Let $Q$ be the program before a walk and $Q'$ after it. At each point $q$, let $L(q)$ be the live set that the walk has there, and $T$ the address-taken names. Inside a block, $L$ is computed backward over the kept instructions only, and since a deleted instruction defines a name outside $L$, $L(q)$ is a subset of the liveness of $Q$ at $q$. So on every edge from $b$ to $s$, $L$ at the start of $s$ is a subset of $L$ at the end of $b$. Run $Q$ and $Q'$ on the same input, matching their points, and keep this invariant: the memory and the call stack are the same, and the two environments agree on every name of $L(q) \cup T$. It holds at the start. A deleted instruction runs in $Q$ only. It cannot trap and it writes only a name that is outside $L$ and outside $T$, so the invariant still holds after it. A kept instruction reads names in $L$, which agree, so in both programs it traps in the same way, or it writes the same value to the same name or memory cell, and a called function, which does not change, sees the same arguments and the same memory. A terminator reads a name in $L$, so it takes the same branch or returns the same value. So the two runs trap together, return the same value, or both never end. The repeats are a sequence of such walks.

## Classic examples

**Dead code with a trap and a dead cycle.** The parameters are `a` and `b`.

```
entry:
  t = a * b
  u = t + 1
  q = a / b
  s = 0
  i = 0
  jump h
h:
  c = i < 3
  br c body done
body:
  s = s + i
  i = i + 1
  jump h
done:
  r = i + a
  ret r
```

The first walk deletes `u = t + 1`, because no one reads `u`. The second walk deletes `t = a * b`, whose only reader was `u = t + 1`. The division `q = a / b` is never read, but it stays: for $b = 0$ the program traps there, and without it the program would return $3 + a$. The sum `s` stays too. `s = s + i` reads `s`, and the back edge brings that read to the end of the loop body, so `s` is live after `s = s + i`. Liveness cannot see that `s` only feeds itself. For $a = 5$, $b = 2$ both programs return 8, in 25 and 23 steps.

**Dead cycles need a different view.** Turn the question around: start from the instructions that must stay, here the division, the branch and the return, mark the definitions that reach the names they read, and mark again, until nothing new is marked. `s = 0` and `s = s + i` are never marked and can go, and the run takes 19 steps. This is the marking method of Cytron and others. [Aggressive dead code elimination](/aggressive-dead-code-elimination/) pushes it further and also removes branches that no marked instruction depends on.

**A dead store.** In `p = alloc; *p = 1; *p = 2; v = *p`, no load reads the cell between the two stores, so the first store is dead. Liveness on names cannot see this; it needs facts about memory, see the variations.

## Variations

- **Marking from the useful instructions.** Mark as useful every store, every call with effects, every instruction that may trap, and every terminator. Then mark each definition that reaches an operand of a useful instruction, through [reaching definitions](/reaching-definitions/) or def-use chains, with a worklist. Delete what is not marked. This finds dead cycles in one pass. On [static single assignment form](/static-single-assignment-form/) each use has one definition, so the worklist is simple and linear.
- **Removing branches.** [Aggressive dead code elimination](/aggressive-dead-code-elimination/) does not mark a branch as useful at the start. It marks a branch only when a useful instruction is [control dependent](/control-dependence/) on it, and it replaces the other branches by a jump.
- **Removing dead stores.** A store `*p = v` is dead if on every path from it the same cell is written again before any load or call that may read it, or the function returns and the cell is a local that no pointer outside the function can reach. The first case needs must-alias facts from [alias analysis](/alias-analysis/). The second needs [escape analysis](/escape-analysis/). A backward pass over stores, much like liveness but on memory cells, finds them.
- **Partial dead code.** An assignment that is dead on some paths and live on others can be moved down, into the paths where it is used, and then it is dead on the paths it left. Knoop, Rüthing and Steffen give a version that never makes a path longer.
- **Unreachable code.** A block that the entry does not reach can be deleted with all its instructions. This is a graph search, not a liveness question, and is often done in the same pass.

## Pitfalls

- **Removing a trap.** `q = a / b` with `q` unused can still trap. Deleting it turns a crash into a normal return. Keep every operation that may trap unless the operands are known to be safe.
- **Removing a call.** A call can write memory, print, or not return. Delete it only if the function is known to be pure, to end, and to never trap. Some languages allow more: C++ lets a compiler assume that a loop without effects ends.
- **Removing a store that clears a secret.** `memset(key, 0, n); free(key)` stores zeros that nobody reads, so the store is dead, and compilers delete it. The secret stays in memory. This is CWE-14. Code that must clear memory uses a function the compiler may not remove, such as `explicit_bzero` or `memset_s`.
- **Pointers to names.** After `p = &x`, a load `*p` reads `x` without naming it. Liveness on names misses that use, so a definition of an address-taken name stays.
- **Volatile memory.** A load or a store to a device register has an effect even if the value is not used. Such accesses are never dead.
- **Stopping after one walk.** Deleting one instruction can make its operands dead. One walk misses them, and no number of walks removes a dead cycle.

## Exercises

1. In the first example, why does the second walk delete `t = a * b` but the first walk does not? *Answer.* In the first walk `t` is live after `t = a * b`, because `u = t + 1` reads it. The first walk deletes that reader, so in the second walk `t` is no longer live.
2. Change `q = a / b` into `q = a / 4`. May the instruction go now? *Answer.* Yes. The divisor is a nonzero constant, so the division cannot trap, and `q` is never read.
3. Give a program where liveness keeps two instructions that the marking method removes. *Answer.* `x = 0` before a loop and `x = x + 1` in the loop, with `x` read nowhere else. `x` is live around the loop, because the increment reads it, but no useful instruction depends on `x`.
4. In `p = alloc; *p = 1; w = call f(p); *p = 2; v = *p`, is the first store dead? *Answer.* Not without knowing `f`. The call gets `p` and may read the cell, so the store of 1 may be used.
5. Show that the rewrite never makes a run execute more instructions. *Answer.* It only deletes instructions and changes no branch, so every run follows the same path through the same blocks with fewer instructions.

## References
