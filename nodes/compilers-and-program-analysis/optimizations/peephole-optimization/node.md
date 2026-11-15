---
tag: 7DT1HA
kind: technique
slug: peephole-optimization
name: Peephole optimization
aliases:
- peephole optimizer
area: compilers-and-program-analysis/optimizations
level: intro
summary: Scans a short window of adjacent instructions and replaces patterns by shorter or faster equivalent sequences, until no rule applies.
prereqs: [three-address-code, basic-block]
see_also: [constant-folding, strength-reduction, superoptimization, live-variable-analysis, instruction-selection-problem, tree-pattern-matching, verified-compilation, dead-code-elimination]
sources:
  - paper: doi:10.1145/364995.365000
    title: William M. McKeeman, Peephole optimization, Communications of the ACM 8(7), 1965, 443-444
    locator: the whole note (the window over the generated code, with redundant store and load pairs and other local patterns)
  - paper: doi:10.1145/357094.357098
    title: Jack W. Davidson and Christopher W. Fraser, The design and application of a retargetable peephole optimizer, ACM Transactions on Programming Languages and Systems 2(2), 1980, 191-202
    locator: the optimizer PO, which simulates pairs of adjacent instructions as register transfers and replaces a pair by one cheaper instruction with the same effect, from a machine description
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 8.7 (Peephole Optimization, with redundant loads and stores, unreachable code, flow-of-control optimizations, algebraic simplification and reduction in strength, and machine idioms)
  - paper: "Nuno P. Lopes, David Menendez, Santosh Nagarakatte and John Regehr, Provably correct peephole optimizations with Alive, Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2015)"
    locator: the Alive language for peephole rewrites of LLVM, their proof with an SMT solver for all bit widths in a range, and the bugs found in the LLVM instruction combiner
---

Peephole optimization looks at a short window of adjacent instructions, usually two or three, and replaces a pattern in the window by a shorter or faster sequence with the same effect. It slides the window over the code and repeats until no rule applies. McKeeman named the method in 1965 for the output of a code generator, and Davidson and Fraser made it machine independent in 1980 by simulating the effect of instruction pairs. A peephole rule is local, so it is cheap and easy to check, but it sees only what is in the window and in a few facts such as liveness.

## In plain words

A code generator often writes code that is correct but clumsy: it stores a value and loads it straight back, jumps to a jump, or multiplies by one. A peephole optimizer reads the code through a small hole that shows only a few lines at a time. When the lines in the hole match a known clumsy pattern, it writes a better version in their place. Then it moves on, and it comes back to look again, because one fix often makes another fix possible. It stops when nothing in any window matches. Each rule is small, so it is easy to see that the rule is right, but the optimizer never sees the whole program.

## When it applies

Peephole optimization runs on a straight list of instructions: the final machine code, assembly, or the instructions of each [basic block](/basic-block/) of an IR. A rule applies when:

- the window matches the pattern of the rule, with any side conditions on constants (for example "the constant is a power of two");
- the replacement has the same effect on every value that is read after the window. If the rule drops a name that the old code wrote, that name must be dead after the window, which needs [live variable analysis](/live-variable-analysis/) or a flag from the code generator;
- the replacement traps exactly when the old code traps;
- no label inside the window is a jump target, unless the rule keeps it, because another path could enter the window in the middle.

## The template

**The algorithm.** Keep a list of rules $\ell \to r$, each with a side condition. Put the window at the start of the code. If some rule matches the instructions under the window, replace them by $r$ and move the window back by the length of the longest rule, so that the new code can combine with the instructions before it. Otherwise move the window one instruction forward. Stop at the end of the code. With $n$ instructions, a window of $k$ instructions and constant-time matching by a [hash table](/hash-table/) or a decision tree, one forward pass takes $O(nk)$ time. Each rewrite strictly lowers the cost (or keeps the cost and lowers the size), so the number of rewrites is at most the cost of the input, and the method ends.

**Classic rules in the toy IR.** The toy IR is described on [three-address code](/three-address-code/). Here words are $w$-bit two's complement integers, as on a real target, and every rule below is correct for each $w \ge 4$.

| window | replacement | side condition |
|---|---|---|
| `v = u`, `u = v` | `v = u` | none: the second copy writes the value that `u` already holds |
| `x = y + 0` | `x = y` | none |
| `x = y * 1` | `x = y` | none |
| `x = y * 8` | `x = y << 3` | multiplier is a power of two, $2^j$ with $j < w$ |
| `jump L`, and `L:` starts with `jump M` | `jump M` | none (jump chaining) |
| `br k L1 L2` with a constant `k` | `jump L1` if $k \ne 0$, else `jump L2` | none |
| `t = b << 2`, `x = a + t` | one `lea x, [a + b*4]` on x86 | `t` is dead after the window |

**Legality.** A rule $\ell \to r$ is legal if, for every state before the window, $\ell$ and $r$ both trap or both end in states that agree on every name that is live after the window, on memory, and on the next instruction. For a rule without memory, this is an identity on $w$-bit words that can be checked for all values; for $w$ up to 64 an SMT solver over bit-vectors does this, as Alive does for LLVM.

**Profit.** The cost model is the cycles or the bytes of the instructions in the window, from the machine description. A rule fires only if the replacement is cheaper. A rule can stop paying when the machine changes: on many current processors a multiply by 8 is about as fast as a shift, so `x * 8 → x << 3` only saves energy or code size there.

**Proof that behavior stays the same.** The proof is local. Assume the program before the rewrite and after it reach the window in the same state. By legality, they leave it in states that agree on every live name and on memory, or both trap. A name that differs is dead, so it is written before it is read on every path, and no later instruction can see the difference. From there both programs run the same instructions. So the outcome of the whole run is the same. Each rule is proved once, for all states, and the optimizer is correct because each step it takes is one of these rules.

## Classic examples

**A pass over one block.** The parameter is `x`.

```
entry:
  t = x * 8
  u = t + 0
  v = u
  u = v
  q = x / 8
  jump next
next:
  jump done
done:
  r = q + u
  ret r
```

The rules give `t = x << 3`, then `u = t`, then they drop `u = v`, because `v = u` just made the two equal. The jump to `next`, which only jumps to `done`, becomes `jump done`, and `next` is no longer reachable. The division `q = x / 8` is not a shift: `/` truncates toward zero, while `>>` rounds toward minus infinity. For $x = -1$ the division gives $0$ and `x >> 3` gives $-1$; for $x = -9$ they give $-1$ and $-2$. A correct rule adds 7 to negative values first:

```
s = x < 0
s = s * 7
s = x + s
q = s >> 3
```

This is four instructions in place of one, and it pays because a division takes tens of cycles on most processors. The original and the rewritten program return the same value for every $x$ from $-3000$ to $2999$, for example $-73$ for $x = -9$ and $105$ for $x = 13$.

**McKeeman's redundant load.** A stack machine compiler writes `STORE A` at the end of one statement and `LOAD A` at the start of the next. If no label is between them, the load is redundant, because the accumulator already holds `A`. This is the toy rule `v = u`, `u = v` in machine form.

**Davidson and Fraser's combination.** The optimizer PO writes each instruction as a list of register transfers, such as `r1 := r2 << 2` and `r3 := r4 + r1`. For two adjacent instructions it composes the transfers into `r3 := r4 + (r2 << 2)`, drops the transfer to `r1` if `r1` is dead, and asks the machine description whether one instruction has exactly this effect. On x86 the answer is `lea`. When PO is done, no instruction and no adjacent pair can be replaced by one cheaper instruction with the same effect.

## Variations

- **Rule generation.** [Superoptimization](/superoptimization/) searches for the cheapest sequence equal to a short one, and the results can be stored as peephole rules. Davidson and Fraser also learned rules from the combinations that PO found on training programs.
- **Pattern matching on trees or DAGs.** Instead of adjacent instructions, a rule can match a tree of operations linked by data flow, as in [tree pattern matching](/tree-pattern-matching/) for instruction selection. The LLVM instruction combiner works this way on SSA values, so its "window" follows def-use edges, not text order.
- **Rewriting to a fixed point with an e-graph.** [Equality saturation](/equality-saturation/) applies all rules at once and picks the best result later, so the order of the rules does not matter.
- **Verified rules.** Alive proves each LLVM peephole rule with an SMT solver; [verified compilation](/verified-compilation/) proves a whole optimizer correct once.

## Pitfalls

- **Division by a power of two is not a shift.** For signed values, truncation and arithmetic shift differ on negative numbers. The fix above, or an unsigned type, is needed.
- **A label in the window.** If another jump enters between the `STORE` and the `LOAD`, the accumulator may hold another value there. The rule must not fire.
- **Dropping a live name.** Combining two instructions into one drops the write of the middle value. If that value is used later, the program breaks. Liveness must be known at the window.
- **Changing the flags.** On machines with condition codes, `x = y * 1 → x = y` can change the flags that a later branch reads. The flags must be dead too.
- **Order of rules.** A greedy order can miss a better result, because one rewrite can block another. Running to a fixed point does not remove this; it only ensures that no single rule still applies.

## Exercises

1. Show that `x * 8 → x << 3` is correct on $w$-bit two's complement words for $w \ge 4$. *Answer.* Both sides equal $8x \bmod 2^w$, read as a signed value: a left shift by 3 multiplies by $2^3$ and drops the bits above $w$, which is multiplication modulo $2^w$.
2. For which negative $x$ do `x / 4` and `x >> 2` agree in the toy IR? *Answer.* Exactly for the multiples of 4. For $x = 4m$ both give $m$. For other negative $x$ the division rounds up toward zero and the shift rounds down, so the shift is smaller by 1; for example $x = -1$ gives $0$ and $-1$.
3. Why must the window move back after a rewrite? *Answer.* The new code may form a pattern with the instruction just before it. Take `v = u`, `u = v + 0` with a window of two. The pair matches no rule, so the window moves on, and then `u = v + 0` becomes `u = v`. Now the pair `v = u`, `u = v` matches the copy rule, but only if the window moves back to see it.
4. Give a rule that is legal only if a name is dead after the window. *Answer.* `t = b << 2`, `x = a + t` to one `lea`: the combined instruction does not write `t`.

## References
