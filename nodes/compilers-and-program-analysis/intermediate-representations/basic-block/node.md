---
tag: SEYHTF
kind: definition
slug: basic-block
name: Basic block
aliases:
- straight-line code block
area: compilers-and-program-analysis/intermediate-representations
level: intro
summary: A maximal sequence of instructions entered only at the first one and left only at the last, so it runs all or nothing.
prereqs: [three-address-code]
see_also: [control-flow-graph, intermediate-representation, local-value-numbering, expression-dag, live-variable-analysis, superblock-scheduling, trace-scheduling, critical-edge-splitting]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 8.4 (Basic Blocks and Flow Graphs), with 8.4.1 (the partition into basic blocks by leaders) and 8.4.3 (flow graphs); Section 8.5 (optimization of basic blocks with the DAG)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 4 (Intermediate Representations), the part on control flow graphs and basic blocks; Chapter 8 (local optimization within one block)
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 7 (Control-Flow Analysis), the construction of basic blocks and of extended basic blocks
---

A basic block is a maximal run of consecutive instructions of a [three-address code](/three-address-code/) program with one entry and one exit: control can enter it only at its first instruction and can leave it only after its last instruction. So if the first instruction runs, all of them run, in order, unless an instruction traps. Basic blocks are the nodes of the [control flow graph](/control-flow-graph/). They are the unit of local optimization, such as [local value numbering](/local-value-numbering/), and the unit at which global analyses store their facts.

## Definition

Let $P = i_1, i_2, \ldots, i_n$ be a three-address program, a list of instructions in which some instructions have labels and some are jumps or conditional branches to labels. A *basic block* is a range $i_a, \ldots, i_b$ of consecutive instructions with these properties:

1. **One entry.** No jump or branch in $P$ targets an instruction $i_k$ with $a < k \le b$, and $i_{a-1}$ is not a fall-through into the middle of the range. Control enters only at $i_a$.
2. **One exit.** No instruction $i_k$ with $a \le k < b$ is a jump, a branch or a return. Control leaves only after $i_b$.
3. **Maximal.** The range cannot be extended by $i_{a-1}$ or by $i_{b+1}$ and still have properties 1 and 2.

### Leaders

The dragon book (Section 8.4.1) finds the blocks with *leaders*, the instructions that start a block:

1. The first instruction $i_1$ is a leader.
2. Every instruction that is the target of a jump or a branch is a leader.
3. Every instruction that comes right after a jump, a branch or a return is a leader.

Each block runs from one leader up to the instruction before the next leader, or to the end of $P$. One pass marks the leaders and a second pass cuts the list, so the partition takes $O(n)$ time for $n$ instructions.

**Claim.** The ranges cut at the leaders are exactly the basic blocks, and they partition $P$.

*Proof.* The ranges partition $P$ by construction. Take one range $i_a, \ldots, i_b$. No $i_k$ with $a < k \le b$ is a jump target, by rule 2, and no $i_k$ with $a \le k < b$ is a jump, a branch or a return, because then $i_{k+1}$ would be a leader by rule 3. So properties 1 and 2 hold. For property 3: $i_{b+1}$, if it exists, is a leader, so it is a jump target or it follows a jump, a branch or a return at $i_b$, and adding it breaks property 1 or property 2. In the same way $i_a$ is a leader, so $i_a = i_1$, or $i_a$ is a jump target, or $i_{a-1}$ is a jump, a branch or a return; in each case adding $i_{a-1}$ breaks a property. Conversely, every basic block lies inside one range, because a range boundary inside it would mean a leader inside it, which breaks property 1 or 2; by maximality it equals that range. $\square$

### In the toy IR

The toy IR of this site is already written as blocks: a label, instructions, and one terminator `jump L`, `br a L1 L2` or `ret a`. There is no fall-through. Each toy IR block satisfies properties 1 and 2. It need not be maximal: a block that ends in `jump C`, where `C` has no other predecessor, could be merged with `C`. Most passes do not need maximality, and some passes, such as [critical edge splitting](/critical-edge-splitting/), add blocks that are not maximal on purpose.

### Traps and calls

"All or nothing" is true only if no instruction leaves the block in the middle. In the toy IR, `/` and `%` trap on a zero divisor and the shifts trap on a count outside 0 to 63, so a run can stop inside a block. Optimizations that move such an instruction within its block, or out of it, must keep the trap. Most compilers do not end a block at a call, because the call returns to the next instruction; a call that can throw an exception is either treated as an exit edge (as in Java and C++ compilers with exception edges) or ends its block.

## Examples and non-examples

### Partitioning a flat program

This flat three-address program adds the odd numbers below $n$:

```
 1      i = 0
 2      s = 0
 3  L1: t1 = i < n
 4      ifFalse t1 goto L2
 5      t2 = i % 2
 6      ifFalse t2 goto L3
 7      s = s + i
 8  L3: i = i + 1
 9      goto L1
10  L2: ret s
```

The leaders are instruction 1 (the first), instructions 3, 8 and 10 (targets of `goto L1`, `goto L3` and `goto L2`), and instructions 5, 7 and 10 (right after a branch or a jump). The blocks are

| block | instructions | ends with |
|---|---|---|
| B1 | 1, 2 | falls through to B2 |
| B2 | 3, 4 | branch to B6 or B3 |
| B3 | 5, 6 | branch to B5 or B4 |
| B4 | 7 | falls through to B5 |
| B5 | 8, 9 | jump to B2 |
| B6 | 10 | return |

In the toy IR, with the fall-throughs written as jumps:

```
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

The edges are B1 → B2, B2 → B3, B2 → B6, B3 → B4, B3 → B5, B4 → B5 and B5 → B2. The runs on $n = 6$ and $n = 7$ return $1 + 3 + 5 = 9$, and the runs on $n = 0$, $n = 1$ and $n = -2$ return 0.

### Local facts

Inside B5, `i = i + 1` reads the old `i` and writes the new one. Inside one block such facts are easy: a forward scan computes which names are defined, which names are read before any definition in the block (here `i`), and which expressions are computed. Global analyses summarize each block by these sets, the *gen* and *kill* sets of [reaching definitions](/reaching-definitions/) or the *use* and *def* sets of [live variable analysis](/live-variable-analysis/), and then work only with blocks and edges.

### Non-examples

- **Instructions 3 to 5.** Instruction 4 is a branch, so control can leave after it, and instruction 5 is not reached on every run that reaches instruction 3.
- **Instructions 7 and 8.** Instruction 8 is the target of `goto L3`, so control can enter the range in the middle.
- **Instructions 1 to 2 of B1, written as two blocks.** Each part has one entry and one exit, but the pair is not maximal; together they are one block.
- **A block of the toy IR with a `/` by a variable.** It is a basic block, but it is not true that a run that starts it always reaches its terminator; the division may trap.

### Pitfalls

- **Forgetting rule 3 for returns.** An instruction right after a `ret` is a leader; if it is not a jump target, its block is unreachable and can be deleted.
- **Missing jump targets.** Computed jumps, such as a `switch` jump table, make every table entry a leader. If the table is not known, every labeled instruction must be a leader.
- **Assuming a block runs to the end.** A trap, an exception or an exit call can stop it. An optimization that moves a trapping instruction above an observable side effect changes the outcome of the program.

## Related definitions

- [Control flow graph](/control-flow-graph/): the graph whose nodes are the basic blocks and whose edges are the possible transfers of control.
- [Three-address code](/three-address-code/): the instructions that the blocks hold.
- [Expression DAG](/expression-dag/) and [local value numbering](/local-value-numbering/): the graph form of one block, and the pass that builds it to find redundant computations.
- *Extended basic block*: a tree of blocks in which every block except the root has exactly one predecessor. Local methods extend to it because each path through it is straight-line code.
- *Superblock* and *trace*: a sequence of blocks on a likely path, with one entry and several exits, the unit of [trace scheduling](/trace-scheduling/) and [superblock scheduling](/superblock-scheduling/).
- [Straight-line program](/straight-line-program/): a program with no branches at all; one basic block without its terminator is one.

## References
