---
tag: T991RF
kind: technique
slug: loop-invariant-code-motion
name: Loop-invariant code motion
aliases:
- LICM
- hoisting
area: compilers-and-program-analysis/optimizations
level: intro
summary: Moves computations whose operands do not change inside a loop to a preheader before the loop, when this is safe.
prereqs: [control-flow-graph, natural-loop, reaching-definitions, live-variable-analysis]
see_also: [partial-redundancy-elimination, lazy-code-motion, very-busy-expressions, strength-reduction, induction-variable-analysis, loop-nesting-forest, alias-analysis, mod-ref-analysis]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.1.7 (Code Motion), Section 9.5 (Partial-Redundancy Elimination) and Section 9.6 (Loops in Flow Graphs)
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 13.2 (Loop-Invariant Code Motion), the marking of invariant instructions and the conditions for moving them to the preheader
  - paper: doi:10.1145/359060.359069
    title: Etienne Morel and Claude Renvoise, Global optimization by suppression of partial redundancies, Communications of the ACM 22(2), 1979, 96-103
    locator: the treatment of loop-invariant computations as partial redundancies, moved to the entrance of the outermost loop in which they are invariant
  - paper: doi:10.1145/390013.808479
    title: Frances E. Allen, Control flow analysis, ACM SIGPLAN Notices 5(7), 1970, 1-19
    locator: loops as strongly connected regions found with dominators, and the use of this structure to place code outside loops
---

Loop-invariant code motion takes an instruction inside a loop whose operands have the same values on every iteration, and computes it once before the loop. The new home is the *preheader*: a block that runs once each time the loop is entered, just before the loop header. The rewrite needs four facts. The operands are not written inside the loop. The destination is written only by this instruction in the loop. The destination is not read in the loop, or after it, before this instruction writes it. And the instruction cannot trap, or it runs on every path where the moved copy runs. The last fact is the one that is easy to forget: moving a division out of a loop that may run zero times adds a trap.

## In plain words

If a loop computes the same thing on every turn, the compiler can compute it once before the loop starts and keep the answer. This saves work each time around the loop. But the move must not change what the program does. The computed value must really be the same on every turn, and nobody may need the old value of the variable it goes into. Also, the loop might not run at all, or the line might sit behind a test inside the loop. Then the program did not compute it before, and computing it now can crash the program, for example by dividing by zero.

## When it applies

Take a [natural loop](/natural-loop/) $L$ with header $h$. Its blocks are $h$ and the blocks that reach a back edge into $h$ without passing $h$.

**The preheader.** A *preheader* of $L$ is a block $p$ outside $L$ whose only successor is $h$, and which is the only predecessor of $h$ outside $L$. Every entry into the loop passes through $p$, and $p$ runs exactly once per entry. If $h$ has no such block, create one: a new block `p: jump h`, and redirect every edge into $h$ from outside $L$ to $p$. This changes only the number of jumps executed.

Fix an instruction $I$: `x = e` in a block $B$ of $L$, where $e$ is a constant, a copy, or an operation `a op b`. Loads, calls, `alloc` and stores are not candidates here; see the variations for loads. $I$ is *loop invariant* if each operand is a constant or a name with no definition in $L$, or, by the same test applied again, a name whose only reaching definition is an invariant instruction of $L$ that is moved first. $I$ may be moved to the end of $p$ when these conditions hold in the current program:

- **(C1) Invariant operands.** Each operand of $I$ is a constant, or a name that no instruction of $L$ defines and that is not address-taken. An address-taken name can change through a store or a call without being named.
- **(C2) One definition.** $I$ is the only instruction of $L$ that defines $x$, and $x$ is not address-taken.
- **(C3) No earlier read.** $x$ is not live at the start of $h$, in the sense of [live variable analysis](/live-variable-analysis/): no path from $h$ reads $x$ before it writes $x$. This rules out a read of $x$ in the loop that sees the value from before the loop or from the previous iteration, and a read after the loop on a path that skipped $I$.
- **(C4) No new trap.** $I$ cannot trap: it is not `/` or `%` by a divisor that may be zero, and not a shift by a count that may be outside 0 to 63.

(C1) is what the [reaching definitions](/reaching-definitions/) test of the textbooks checks: all definitions of the operand that reach $I$ are outside $L$. The textbook form of (C3) is two conditions: every use of $x$ in $L$ is reached only by $I$, and $B$ dominates every exit of $L$ after which $x$ is live. Together these say that $x$ is not live at $h$.

## The template

**The rewrite.** Find the loops, from the innermost out, and give each a preheader. For one loop, mark the invariant instructions until no new one is found, in the order they are found. Then, in that order, move each marked instruction that meets (C1) to (C4) from its block to the end of the preheader, before its jump. An instruction moved out of an inner loop lands in the inner preheader, which is a block of the outer loop, so it is a candidate again when the outer loop is processed.

**Legality.** (C1) to (C4) are checked on the program as it is after the earlier moves. (C1) uses reaching definitions or a scan of the loop for definitions, (C3) uses liveness, a may property with union at joins, and (C4) is a fact about the operation and its operands.

**Profit.** The cost model is the number of instructions executed. A moved instruction runs once per entry of the loop instead of once per execution of $B$. This pays when $B$ runs at least once per entry, the usual case. It costs one extra instruction per entry when the loop runs zero times or when $B$ is skipped, for example behind a test in the loop. A second cost is register pressure: the moved value stays live through the whole loop. In a loop that already uses all registers, this can cause spills that cost more than the instruction saved.

**Proof that behavior stays the same.** Let $Q$ be the program with the preheader $p$, and let $Q'$ be $Q$ with $I$ moved from $B$ to the end of $p$. Fix an input. The two programs have the same blocks, with the same instructions except $I$, and the same terminators. Run them side by side, block by block, and keep this invariant at each matched point $q$: the memory is the same, every name other than $x$ has the same value, and either $x$ has the same value or $x$ is not live at $q$ in $Q$.

1. *Outside the loop and $p$*, both programs run the same instructions. An instruction that reads $x$ needs $x$ live before it, so $x$ agrees there. All other operands agree. So the instruction writes the same value or traps in both, a call gets the same arguments and memory and returns the same result, and a definition of $x$ makes $x$ agree. A terminator reads a live name, so both take the same branch or return the same value.
2. *At $p$*, $Q'$ also sets $x$ to $v$, the value of $e$ at that moment, and $I$ does not trap by (C4). Afterward all names other than $x$ still agree, and $x$ is not live at $h$ by (C3). So the invariant holds at $h$.
3. *Inside one visit of the loop*, from $h$ until the run leaves $L$: no instruction of $L$ writes an operand of $I$, by (C1), so every execution of $I$ in $Q$ computes $v$ again. In $Q'$ no instruction of $L$ writes $x$, by (C2), and no store or call can write it, since it is not address-taken, so $x$ stays $v$ all through the visit. Now take a point $q$ in the visit. If $Q$ has run $I$ in this visit, $x$ is $v$ in both. If not, the run of $Q$ went from $h$ to $q$ with no write to $x$, and if $x$ were live at $q$, that path followed by a path to a read would show that $x$ is live at $h$, against (C3). So the invariant holds at every point in the visit. Every instruction other than $I$ behaves the same in both programs by the argument of case 1, and $I$ in $Q$ cannot trap and leaves $x$ equal to $v$ in both.
4. *When the run leaves $L$*, the invariant holds at that point, and case 1 takes over. Each new entry of the loop passes through $p$ again.

So the two runs take the same branches, trap at the same instruction, return the same value, or both run forever. The only difference is the instruction count: $Q'$ runs $I$ once per arrival at $p$, and $Q$ once per execution of $B$. When several instructions move, apply the argument once per move, in the order of the rewrite. Each move is checked against the program left by the moves before it.

## Classic examples

**An invariant product.** The parameters are `a`, `b` and `n`. The block `entry` is the only way into the loop and ends with `jump h`, so it is already a preheader.

```
entry:
  i = 0
  s = 0
  jump h
h:
  c = i < n
  br c body done
body:
  t = a * b
  u = t + i
  s = s + u
  i = i + 1
  jump h
done:
  ret s
```

`a` and `b` are parameters with no definition in the loop, `t` has one definition in the loop, `t` is read only after it, and a product cannot trap. So `t = a * b` moves to `entry`, before `jump h`. `u = t + i` reads `i`, which the loop changes, so it stays. For $a = 2$, $b = 3$, $n = 3$ both programs return 21, in 27 steps before and 25 after. For $n = 0$ the loop body never runs, and the new program takes 7 steps instead of 6.

**A division that adds a trap.** Replace the body by `q = a / b; s = s + q; i = i + 1; jump h`. The division is invariant, but it may trap. For $b = 0$ and $n = 0$ the old program returns 0: the body never runs. With `q = a / b` in the preheader, the new program traps. For $b = 0$ and $n = 2$ both trap. (C4) forbids the move. The usual fix is to rotate the loop first, see the variations: under a test that $n > 0$, the body runs at least once, and the division can move there.

**A read before the write.** In `body: s = s + x; x = a * b; ...`, the operands of `x = a * b` are invariant, but the first iteration reads `x` before the loop writes it, and sees the value from before the loop. So `x` is live at `h`, and (C3) forbids the move. If it moved, the first iteration would read $a \cdot b$ instead.

**Two definitions.** If the loop holds `x = a * b` in one branch and `x = a + b` in the other, both are invariant in their operands, but neither may move: after the move, the loop would see one value of `x` where it saw two. (C2) catches this.

## Variations

- **On SSA form.** In [static single assignment form](/static-single-assignment-form/), every name has one definition, which dominates all its uses. Then (C2) and (C3) always hold, and an instruction is invariant when each operand is defined outside the loop or by an invariant instruction. Only (C1) and (C4) are left to check.
- **Loop rotation.** A loop `while c do body` becomes `if c then (do body while c)`. The new guarded block before the loop is a preheader that runs only if the body runs at least once. An instruction at the start of the body, before any store, call or other trap, can then move to this preheader even if it may trap: it would have run right after the preheader anyway, with the same operands.
- **Invariant loads.** A load `x = *r` is invariant if `r` is invariant and no store or call in the loop may write the cell that `r` points to. Proving this needs [alias analysis](/alias-analysis/) and [mod-ref analysis](/mod-ref-analysis/) of the calls. A load may also fault on a real machine, so the same care as for (C4) applies.
- **Scalar promotion.** If a loop reads and writes one memory cell through an invariant pointer and nothing else touches it, the compiler loads the cell into a name in the preheader, uses the name in the loop, and stores it back at each exit.
- **Partial redundancy elimination.** [Partial redundancy elimination](/partial-redundancy-elimination/) treats an invariant expression as redundant on the back edge and inserts it at the preheader. [Lazy code motion](/lazy-code-motion/) does this only where the expression is [very busy](/very-busy-expressions/), that is, computed on every path from that point, so it never adds a computation, and never a trap, to a path that lacked one. This subsumes most loop-invariant code motion, but it does not move a computation out of a loop that may run zero times unless the loop is rotated first.
- **Sinking.** The opposite move takes an instruction whose result is used only after the loop and puts it at the loop exits, so it runs once instead of on each iteration.

## Pitfalls

- **Adding a trap.** A division, a remainder, a shift, or a load in a loop that may run zero times, or behind a test in the loop, did not run on every path. Moving it to the preheader can trap where the old program did not.
- **Loops that run zero times.** Even without traps, a moved instruction runs once on entry to a loop whose body never runs. This is one wasted instruction, not a wrong result, but it can matter in an outer loop that runs many times.
- **Register pressure.** Each moved value stays live through the whole loop. Many moved values can force spills inside the loop, which costs more than the work saved.
- **Memory changed by the loop.** A load is not invariant just because its pointer is: a store in the loop through another pointer, or a call, may change the cell. A load from memory that another thread writes, such as `while (!flag)`, must not move out of the loop, or the loop waits forever. Such accesses must be atomic or volatile, which the compiler never moves.
- **Calls.** A call with invariant arguments is not invariant unless the function is known to be pure, to end, and to never trap.
- **Values live into the loop.** A name defined in the loop but read at the top of the loop before that definition holds the previous value on each iteration. Moving its definition changes the first read.

## Exercises

1. In the first example, why may `u = t + i` not move, even after `t = a * b` has moved? *Answer.* It reads `i`, which `i = i + 1` defines in the loop, so (C1) fails.
2. A loop body holds `t = a * b` and then `w = t * 2`. After `t = a * b` moves, may `w = t * 2` move too? *Answer.* Yes. `t` no longer has a definition in the loop, `w` has one definition, a product cannot trap, and if `w` is read only after it is written, (C3) holds. It moves to the preheader after `t = a * b`.
3. Give a loop in which `q = a / 4` may move but `q = a / b` may not. *Answer.* Any loop that may run zero times, with `a` and `b` not defined in it. Division by the constant 4 cannot trap, so (C4) holds for it. Division by `b` can trap when `b = 0`, so the move would add a trap on the run where the loop body never runs.
4. Why is it not enough, for (C3), that $B$ dominates every loop exit? *Answer.* A read of $x$ in the loop before $B$, on the first iteration, still sees the value from before the loop. (C3) rules out this read and the reads after exits that skip $B$ in one condition.
5. On SSA form, why do (C2) and (C3) hold? *Answer.* Each name has one definition, so (C2) holds. That definition dominates every use. A path from $h$ to a use that misses the definition, preceded by a path from the entry to $h$ that does not enter $L$ before $h$, would be a path from the entry to the use that misses it, against dominance.

## References
