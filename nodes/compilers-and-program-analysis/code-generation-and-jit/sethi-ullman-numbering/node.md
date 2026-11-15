---
tag: HKPTPW
kind: algorithm
slug: sethi-ullman-numbering
name: Sethi-Ullman algorithm
aliases:
- Ershov numbers
- Sethi-Ullman numbering
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Labels each node of an expression tree with the fewest registers that evaluate it, then emits code that evaluates the child with the larger label first and stores only when registers run out.
solves: [register-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree, k: the number of registers}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1970
  people: [Ravi Sethi, Jeffrey D. Ullman]
  note: Sethi and Ullman gave the labels, the code generator for N registers and a proof that the code is shortest when no algebraic law applies.
prereqs: [binary-tree, postorder-traversal, three-address-code]
see_also: [aho-johnson-code-generation, local-register-allocation, dag-code-generation-np-completeness, register-allocation-problem, instruction-selection-problem, abstract-syntax-tree, tree-dynamic-programming]
sources:
  - paper: doi:10.1145/321607.321620
    title: Ravi Sethi and J. D. Ullman, The generation of optimal code for arithmetic expressions, Journal of the ACM 17(4), 1970, 715-728
    locator: the labels of the nodes, the algorithm for a machine with N registers, and the proof that its programs are shortest when no algebraic law applies; the extension to commutative and associative operators
  - paper: doi:10.1145/368892.368907
    title: A. P. Ershov, On programming of arithmetic operations, Communications of the ACM 1(8), 1958, 3-6
    locator: the whole paper, an English translation of a 1958 note in Doklady AN SSSR
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 8 (Code Generation), Section 8.10, Ershov numbers and the evaluation of expressions with too few registers
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation), the part on register allocation for trees
---

The Sethi-Ullman algorithm generates code for an expression tree on a machine with $k$ registers. It gives each node a label: the fewest registers that evaluate the subtree of the node without a store to memory. Then it walks the tree and evaluates the child with the larger label first. For a tree, the label of the root is exactly the minimum register count, and the code is as short as possible. The method needs a tree: for code with shared subexpressions the problem is NP-complete (see [the DAG theorem](/dag-code-generation-np-completeness/)). It also has a fixed instruction set with unit costs. [Aho-Johnson code generation](/aho-johnson-code-generation/) handles any set of instructions with costs.

## In plain words

To compute a sum of two parts, you must keep the result of the first part in a register while you work on the second part. So the second part has one register less.

The algorithm first finds out how many registers each part needs. A single variable on the left needs one register. A variable on the right can stay in memory, because the machine can read it directly. When the two parts need different counts, the node needs the larger count: do the hungry part first, and the other part fits in what is left. When the two parts need the same count, the node needs one more register.

Then the algorithm writes the code in that order. When there are not enough registers, it computes the right part first, saves it in memory, and reads it back as the right operand at the end.

## The problem

The input is a binary [expression tree](/abstract-syntax-tree/) $T$ with $n$ nodes and a number $k \ge 1$. Each leaf is a variable in memory. Each inner node $v$ has an operator, a left child $a(v)$ and a right child $b(v)$. No algebraic law is used: the operators need not be commutative or associative, and two nodes are different even when their subtrees are equal.

The machine has registers $R_0, \ldots, R_{k-1}$ and four instructions, as in the model of Sethi and Ullman:

- load: $R_i \leftarrow x$, where $x$ is a variable or a temporary in memory,
- store: $t \leftarrow R_i$,
- operation with a register: $R_i \leftarrow R_j \mathbin{op} R_l$,
- operation with memory: $R_i \leftarrow R_j \mathbin{op} x$.

The left operand of an operation is always a register. The output is a program that leaves the value of the tree in $R_0$. The goal is the fewest registers when no store is allowed, and the fewest instructions when the registers are fixed. This is [register allocation](/register-allocation-problem/) and evaluation order together, for one tree.

## The algorithm

LABEL computes the labels bottom-up. GEN emits the code. In GEN, $r = k - i$ is the number of free registers $R_i, \ldots, R_{k-1}$, and $\ell(v)$ is the label of $v$.

```pseudo id=main
LABEL(v, left)                            ▷ left is true for the root and for each left child
L1  if v is a leaf and left then return 1
L2  if v is a leaf then return 0          ▷ a right leaf is a memory operand
L3  la ← LABEL(a(v), true), lb ← LABEL(b(v), false)
L4  if la = lb then return la + 1
L5  return max(la, lb)

GEN(v, i)                                 ▷ leave v in R_i, use only R_i .. R_(k-1)
L6  if v is a leaf then emit R_i ← v; return
L7  if b(v) is a leaf then GEN(a(v), i); emit R_i ← R_i op b(v); return
L8  if ℓ(a(v)) ≥ r and ℓ(b(v)) ≥ r then   ▷ both children are too big: spill
L9      GEN(b(v), i); t ← a new temporary; emit t ← R_i
L10     GEN(a(v), i); emit R_i ← R_i op t
L11 else if ℓ(a(v)) ≥ ℓ(b(v)) then GEN(a(v), i); GEN(b(v), i + 1); emit R_i ← R_i op R_(i+1)
L12 else GEN(b(v), i); GEN(a(v), i + 1); emit R_i ← R_(i+1) op R_i
```

The first child keeps its result in $R_i$ while the second child runs in $R_{i+1}, \ldots, R_{k-1}$. Line L12 evaluates the right child first, but the operation still puts the left child on the left, so a non-commutative operator gives the right value. Line L8 is the only place with a store. There, the right child goes to a temporary $t$, and line L10 reads $t$ directly as the right operand, so the algorithm never loads a temporary.

## Example

Take $(a - b) * (c + (d - e))$ with $a = 7$, $b = 2$, $c = 3$, $d = 10$ and $e = 4$. Its value is $5 \cdot 9 = 45$. The labels are:

| node | position | label | label without memory operands |
|---|---|---|---|
| $a$, $c$, $d$ | left leaf | 1 | 1 |
| $b$, $e$ | right leaf | 0 | 1 |
| $a - b$ | left child | 1 | 2 |
| $d - e$ | right child | 1 | 2 |
| $c + (d - e)$ | right child | 2 (equal labels 1 and 1) | 2 |
| root $*$ | root | 2 (labels 1 and 2) | 3 |

With $k = 2$, the right child has the larger label, so line L12 runs it first:

| step | instruction | value |
|---|---|---|
| 1 | $R_0 \leftarrow c$ | 3 |
| 2 | $R_1 \leftarrow d$ | 10 |
| 3 | $R_1 \leftarrow R_1 - e$ | 6 |
| 4 | $R_0 \leftarrow R_0 + R_1$ | 9 |
| 5 | $R_1 \leftarrow a$ | 7 |
| 6 | $R_1 \leftarrow R_1 - b$ | 5 |
| 7 | $R_0 \leftarrow R_1 * R_0$ | 45 |

The code uses two registers and seven instructions, and no program for this tree does better. If you evaluate the left child first instead, $a - b$ holds $R_0$ while $c + (d - e)$ needs two more registers, so the peak is three.

With $k = 1$, each inner node with an inner right child goes through line L8. The code is $R_0 \leftarrow d$, $R_0 \leftarrow R_0 - e$, $t_0 \leftarrow R_0$, $R_0 \leftarrow c$, $R_0 \leftarrow R_0 + t_0$, $t_1 \leftarrow R_0$, $R_0 \leftarrow a$, $R_0 \leftarrow R_0 - b$, $R_0 \leftarrow R_0 * t_1$. That is nine instructions with two stores, which is the minimum for one register.

## Correctness

A store-free program is a game on the tree: a register holds the value of one node, a node can enter a register when its operands are there, and any register can be overwritten. The lower bound looks at the last time that each subtree of a node $v$ was empty before $v$ is computed. When the two children have the same label $L$, the child whose subtree became non-empty last needs $L$ registers at some moment, and at that moment the other subtree still holds a register. So every program needs at least $\ell(v)$ registers, even if it interleaves the two subtrees. The upper bound is an induction on GEN: GEN$(v, i)$ with $\ell(v) \le k - i$ stays inside $R_i, \ldots, R_{i + \ell(v) - 1}$. With fewer registers, GEN stays inside $R_i, \ldots, R_{k-1}$ and still computes the right value. The full proof is in the proof file.

## Complexity

LABEL visits each node once and does constant work there, so it takes $\Theta(n)$ time. GEN also visits each node once. It emits one operation for each inner node, one load for each leaf that is the root or a left child, and at most one store for each inner node. So the code has $\Theta(n)$ instructions, and GEN takes $\Theta(n)$ time. A unit step is the work at one node. The extra space is $\Theta(n)$ for the labels and the recursion stack, whose depth is the height of the tree.

## Properties

- **Exact for trees.** The label of the root is the minimum register count over all store-free programs, in every evaluation order. The proof file proves this.
- **Few registers suffice.** A label $\ell$ in the variant without memory operands needs at least $2^{\ell - 1}$ leaves, because a label goes up only when two children have the same label. Each label with memory operands is at most the label without them. So the label is at most $1 + \lg(\text{number of leaves})$, and a complete tree of 32 leaves needs only 5 registers with memory operands.
- **A chain needs one register.** A left-deep tree such as $((a + b) + c) + d$ has label 1.
- **Shortest code.** On their machine and with no algebraic law, Sethi and Ullman prove that the program has the fewest instructions. The code also loads each variable once and never loads a temporary.

## Variants and improvements

- **Ershov numbers.** On a machine with no memory operand, each leaf needs a register, so each leaf gets the label 1. These labels are the Horton-Strahler numbers of the tree. A spill then needs a store and a later load. The example tree has label 3 in this variant.
- **Commutative and associative operators.** Sethi and Ullman also reorder the operands of commutative operators, and regroup associative ones, to find an equal expression with the shortest code.
- **Unary operators.** A unary node gets the label of its child.
- **Instruction costs.** [Aho-Johnson code generation](/aho-johnson-code-generation/) replaces the fixed instructions by any set of tree patterns with costs and computes a cost for each number of free registers. The Sethi-Ullman algorithm is the special case with one pattern per operator.

## When to use it

Use it to order the evaluation of expression trees in a simple compiler, or in the code generator of a [tree-walking](/postorder-traversal/) back end, when registers are few. Use the labels alone to decide which operand of a node to evaluate first. For straight-line code with named values, use [local register allocation](/local-register-allocation/). For a machine with complex addressing modes and costs, use tree tiling by dynamic programming or a [BURS](/burs/) generator.

## Pitfalls

- **Left to right.** A fixed left-to-right order can use more registers. The example needs three registers in that order and two in the labeled order.
- **Wrong operand order.** In line L12 the right child is in $R_i$, but it is still the right operand. Writing $R_i \leftarrow R_i \mathbin{op} R_{i+1}$ there computes $b - a$ for a subtraction.
- **The wrong variant.** Label 0 for a right leaf is right only when the machine can read that operand from memory. On a load-store machine it undercounts.
- **Shared subtrees.** On a DAG, a node with two parents keeps its register until both parents are done. The labels then give no bound, and the exact problem is NP-complete.
- **Algebraic laws.** The minimum is over programs that keep the tree as it is. With a commutative $+$, the tree $c + (d - e)$ can become $(d - e) + c$, which has label 1 instead of 2.
- **Calls inside the tree.** A call clobbers registers that the calling convention does not save, so a tree with calls needs more care than the labels show.

## Implementations

## History

Sethi and Ullman published the labels, the algorithm and the proofs in the Journal of the ACM in 1970. They prove that the code is shortest when no algebraic law applies, and they extend the method to commutative and associative operators. The dragon book calls the labels Ershov numbers, after a 1958 paper by A. P. Ershov on the programming of arithmetic operations.

## References
