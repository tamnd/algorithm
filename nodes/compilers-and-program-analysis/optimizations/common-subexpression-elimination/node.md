---
tag: 5PZ5JW
kind: technique
slug: common-subexpression-elimination
name: Common subexpression elimination
aliases:
- CSE
area: compilers-and-program-analysis/optimizations
level: intro
summary: Computes an expression once and reuses the value where the same expression is computed again with the same operands.
prereqs: [available-expressions, local-value-numbering, control-flow-graph]
see_also: [partial-redundancy-elimination, global-value-numbering, lazy-code-motion, copy-propagation, dead-code-elimination, loop-invariant-code-motion, alias-analysis, register-allocation-problem]
sources:
  - paper: doi:10.1145/390013.808480
    title: John Cocke, Global common subexpression elimination, ACM SIGPLAN Notices 5(7), 1970, 20-24 (Proceedings of a Symposium on Compiler Optimization)
    locator: the global form of the transform over the flow graph, using the expressions available on entry to each block
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.1.4 (Global Common Subexpressions), Section 9.2.6 (Available Expressions) and Section 9.5 (Partial-Redundancy Elimination)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Section 8.4.1 (Local Value Numbering) and Section 10.5 (Redundancy Elimination)
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 13.1 (Common-Subexpression Elimination, local and global forms)
---

Common subexpression elimination (CSE) finds an operation `y = a op b` whose value the program has already computed on every path that reaches it, with the same operands and no change to them since, and replaces it by a copy of the earlier result. Inside one [basic block](/basic-block/) this is [local value numbering](/local-value-numbering/). Across blocks it needs the fact that the expression is *available*, which [available expressions](/available-expressions/) computes as a forward dataflow problem. CSE saves the cost of the operation; it pays with a longer live range for the saved value.

## In plain words

If a program works out `a * b` and later works out `a * b` again, and neither `a` nor `b` changed in between, the second time is wasted. The compiler can keep the first answer in a spare variable and use it the second time. This is only safe if the first answer exists on every road the program can take to reach the second place. If one road skips the first computation, or changes `a` on the way, the spare variable may hold nothing or the wrong number there. The price is that the spare variable must be kept until its last use, which takes a register for longer.

## When it applies

Fix an expression $e = a \mathbin{op} b$ with names or constants as operands. An occurrence `y = a op b` at a point $p$ is *redundant*, and CSE may replace it, when:

- $e$ is **available** at $p$: on every path from the entry to $p$, some instruction evaluates $e$, and after the last such evaluation on that path no instruction redefines $a$ or $b$. This is a must property, the meet is intersection, and the boundary is "nothing is available at the entry". Paths that cannot run in practice still count, so the analysis is safe and not exact.
- $e$ is **pure**: its value depends only on $a$ and $b$. An operation of the toy IR is pure. A load is pure only if no store or call between the two loads can write the same memory, which needs [alias analysis](/alias-analysis/). A call is pure only if the function has no side effect and reads no memory that can change.

An occurrence that may trap needs no extra condition. If `y = a / b` is redundant, an earlier `a / b` ran with the same values without a trap, so the occurrence cannot trap either.

## The template

**The rewrite.** Solve available expressions over the [control flow graph](/control-flow-graph/). Choose a fresh name $t_e$ for each expression $e$ that has a redundant occurrence. Then:

1. at every evaluation `x = a op b` of $e$ in the program, write `t_e = a op b` followed by `x = t_e`;
2. at every redundant occurrence `y = a op b`, write `y = t_e` and drop the evaluation.

An occurrence can be both: it reads $t_e$ if it is redundant, and otherwise it writes $t_e$. Afterwards [copy propagation](/copy-propagation/) and [dead code elimination](/dead-code-elimination/) clean up the copies. The textbook variant searches backward from each redundant occurrence for the evaluations that reach it and changes only those; the version above changes all evaluations, which is simpler and gives the same result after cleanup.

**Legality.** The fact used is $e \in \mathrm{AVAIL}_{in}$ at the occurrence, in the sense above, and that $e$ is pure.

**Profit.** The cost model is the number of operations executed on each path. Every run that reaches a redundant occurrence saves one evaluation of $e$; no run does more operations, because step 1 only adds a copy, which a register allocator usually removes by coalescing. The cost is register pressure: $t_e$ is live from each evaluation to the last redundant use. If $e$ is cheap, such as an addition, and the extra live range forces a spill, the store and the reload cost more than the addition saved. Compilers then undo the choice by rematerialization, which recomputes a cheap value instead of keeping it.

**Proof that behavior stays the same.** We show one invariant: in every run of the new program, at every point $q$ with $e \in \mathrm{AVAIL}_{in}(q)$, the name $t_e$ is defined and holds the value of $a \mathbin{op} b$ in the current state. Take a run that reaches $q$, and the path it took. Since $e$ is available at $q$, the path contains an evaluation of $e$, and after the last one, at a point $q'$, no instruction redefines $a$ or $b$. In the new program that evaluation writes $t_e = a \mathbin{op} b$. Only evaluations of $e$ write $t_e$, and there is none after $q'$ on the path, so $t_e$ still holds that value at $q$, and the operands still have the same values, so it is the current value of $a \mathbin{op} b$. Now the two programs move in lock step: step 1 writes the same value to $x$ and only adds a fresh name, and step 2 writes to $y$ the value that the dropped evaluation would write. That evaluation would not trap, because the evaluation at $q'$ ran on the same values. So both programs trap at the same instructions, leave the same values in the original names, and have the same outcome.

## Classic examples

**A diamond with a kill.** The parameters are `a`, `b` and `c`.

```
entry:
  x = a * b
  br c left right
left:
  y = a * b
  jump join
right:
  a = a + 1
  w = a * b
  jump join
join:
  z = a * b
  r = z + x
  ret r
```

`a * b` is available in `left`, because `entry` computed it and nothing changed `a` or `b`. It is not available at `w` in `right`, because `a = a + 1` killed it. At `join` it is available on both incoming paths: through `left` from the evaluation in `entry`, and through `right` from `w`. The two paths reach `join` with different values of `a * b`, but on each path $t$ holds the right one:

```
entry:
  t = a * b
  x = t
  br c left right
left:
  y = t
  jump join
right:
  a = a + 1
  t = a * b
  w = t
  jump join
join:
  z = t
  r = z + x
  ret r
```

For $a = 2$, $b = 3$ both programs return 12 when $c \ne 0$ and 15 when $c = 0$. The original program does three multiplications on every run; the new one does one on the left path and two on the right path.

**A partial redundancy.** If `entry` did not compute `a * b`, then at `join` the expression would be available only through `right`. CSE leaves it alone. Inserting `a * b` at the end of `left` would make it fully redundant; that is [partial redundancy elimination](/partial-redundancy-elimination/), which needs its own safety rule, so that no path computes more than before.

**Local CSE.** Inside a block, local value numbering finds the same redundancies and more, because it compares value numbers: after `c = a`, it knows that `c * b` and `a * b` are equal, while available expressions compares the text of the expressions and does not.

## Variations

- **Local only.** [Local value numbering](/local-value-numbering/) in each block, with no dataflow analysis.
- **Value-based CSE.** [Global value numbering](/global-value-numbering/) proves that two different expressions have the same value, for example through copies and phi-functions, and then removes the later one if a value with that number dominates it.
- **Partial redundancy elimination.** [Partial redundancy elimination](/partial-redundancy-elimination/) and [lazy code motion](/lazy-code-motion/) also insert evaluations to make partly redundant ones fully redundant. They subsume global CSE and most [loop-invariant code motion](/loop-invariant-code-motion/).
- **Loads and calls.** Redundant load elimination treats `*p` as an expression that a store through any pointer that may alias `p` kills. Pure functions can be handled the same way.

## Pitfalls

- **A kill on one path.** An expression that is computed on every path but whose operand changes on one of them after the computation is not available. A transform that only checks "computed on every path" uses a stale value.
- **Loads across stores.** `u = *p; *q = 1; v = *p` is redundant only if `p` and `q` never point to the same cell. Without alias facts, every store kills every load.
- **Calls with side effects.** Two calls `f(x)` may return different values, or the second may be needed for its effect. CSE treats a call as an expression only if it is known to be pure.
- **One temporary per expression.** Using one shared temporary for two different expressions, or reusing an existing name of the program for $t_e$, breaks the invariant of the proof.
- **Register pressure.** CSE on cheap expressions can make code slower by forcing spills. Many compilers limit CSE of constants and address arithmetic for this reason.
- **Text and value.** `a + b` and `b + a` are different texts. Normalize commutative operators first, or use value numbering.

## Exercises

1. In the diamond above, swap the order of `a = a + 1` and `w = a * b` in `right`. Is `a * b` available at `join`? *Answer.* No. On the path through `right` the last evaluation is followed by `a = a + 1`, so `a * b` is killed there; availability needs every path.
2. Why may a redundant `y = a / b` be replaced even though the division can trap? *Answer.* On every path to it an earlier `a / b` ran with the same values of `a` and `b`. Had that one trapped, the run would not reach the occurrence. So the occurrence never traps, and dropping it changes no outcome.
3. Give a block where local value numbering removes an operation that CSE based on available expressions does not. *Answer.* `c = a`, `x = a * b`, `y = c * b`. The texts `a * b` and `c * b` differ, but `c` and `a` have the same value number.
4. Show that CSE never increases the number of operations executed on any run. *Answer.* Step 1 keeps each evaluation and adds a copy; step 2 replaces an operation by a copy. So each run executes the same operations as before, minus those at redundant occurrences.

## References
