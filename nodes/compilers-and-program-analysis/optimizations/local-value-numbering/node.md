---
tag: CJTBEP
kind: algorithm
slug: local-value-numbering
name: Local value numbering
aliases:
- LVN
area: compilers-and-program-analysis/optimizations
level: intro
summary: Gives each value in a basic block a number by hashing operator and operand numbers, so equal expressions get the same number.
model: word-ram
complexity:
  vars: {n: the number of instructions in the basic block}
  time: {expected: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [basic-block, three-address-code, hash-table, constant-folding]
see_also: [common-subexpression-elimination, global-value-numbering, alpern-wegman-zadeck-value-numbering, hash-consing, expression-dag, copy-propagation, dead-code-elimination, congruence-closure]
sources:
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Section 8.4.1 (Local Value Numbering, with the extensions for commutative operations, constant folding and algebraic identities, and the problem of a name that is redefined) and Section 8.5.1 (Superlocal Value Numbering)
  - paper: doi:10.1145/368892.368907
    title: Andrei P. Ershov, On programming of arithmetic operations, Communications of the ACM 1(8), 1958, 3-6
    locator: the numbering of the operations of a formula, so that an operation that is already programmed is found in a table and not programmed again
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 12 (Early Optimizations), the section on value numbering, and Section 13.1 (Common-Subexpression Elimination)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 6.1.2 (The Value-Number Method for Constructing DAGs) and Section 8.5 (Optimization of Basic Blocks, the DAG of a block and local common subexpressions)
---

Local value numbering (LVN) finds the operations in a [basic block](/basic-block/) that compute a value the block has already computed, and replaces them by a copy. It gives every value a number. Two operations get the same number when they apply the same operator to operands with the same numbers, and a [hash table](/hash-table/) keyed by (operator, number, number) finds this in expected constant time. With a few extra rules the same pass also does [constant folding](/constant-folding/) and safe algebraic identities. It is the local, one-block form of [common subexpression elimination](/common-subexpression-elimination/), and the base of [global value numbering](/global-value-numbering/).

## In plain words

Read the block from top to bottom and give each value a ticket number. A variable read for the first time gets a new ticket. When an instruction adds two values, look up "plus, with these two tickets" in a table. If the table already has an answer, the block computed this sum before, so the instruction can copy that earlier result instead of adding again. If not, the sum gets a new ticket and goes into the table. The ticket belongs to the value, not to the variable, so a copy or a different variable name does not hide a repeat. When a variable gets a new value, it gets a new ticket, and the old result can no longer be copied from it.

## The problem

The input is one basic block of the toy IR of [three-address code](/three-address-code/): a list of $n$ instructions with no jump into or out of the middle. The output is a block of the same length in which some `op` instructions are replaced by a constant or by a copy `x = y`, such that from every state on entry the new block traps exactly when the old one does and otherwise leaves the same state. The goal is to replace as many operations as possible whose value the block already holds in some name.

Two operations compute the same value if their operands hold the same values. This is undecidable in general (see [the full employment theorem](/full-employment-theorem/)), and LVN finds a decidable part of it: equal operators applied to operands that are equal by construction in the block, plus constant folding and a fixed list of identities. It does not know facts that come from other blocks or from algebra beyond that list.

## The algorithm

VN maps names to value numbers, CONST maps a number to its constant, KEY maps an expression key to a number, and HOLDERS maps a number to the names that were given it, oldest first.

```pseudo id=main
LVN(B)
L1  VN, CONST, KEY, HOLDERS <- empty maps
L2  for each instruction I of B, in order, do
L3      if I is a store then keep I and continue with the next instruction
L4      if I is x = k then v <- NUMBER(k)
L5      else if I is x = a then v <- NUMBER(a)
L6      else if I is x = a op b then
L7          va <- NUMBER(a); vb <- NUMBER(b)
L8          if CONST has va and vb and op does not trap on CONST[va], CONST[vb] then
L9              r <- CONST[va] op CONST[vb]; replace I by x = r; v <- NUMBER(r)
L10         else if a safe identity turns a op b into a constant or an operand c then
L11             replace I by x = c; v <- NUMBER(c)
L12         else key <- (op, va, vb), with va and vb sorted if op is commutative
L13             if key is in KEY then v <- KEY[key]
L14                 if some n in HOLDERS[v] has VN[n] = v then replace I by x = n
L15             else v <- a new number
L16                 KEY[key] <- v
L17     else v <- a new number          (phi, load, call, alloc, addr)
L18     VN[x] <- v; append x to HOLDERS[v]
L19 return B

NUMBER(a)
L20 if a is an integer k then
L21     if k has no number, give it a new number u and set CONST[u] <- k
L22     return the number of k
L23 if a is not in VN then VN[a] <- a new number; append a to HOLDERS[VN[a]]
L24 return VN[a]
```

Line L8 computes with the semantics of the target: in the toy IR `/` truncates toward zero, and `/`, `%` trap on a zero divisor and the shifts on a count outside 0 to 63. The identities of line L10 are $a + 0$, $a - 0$, $a \cdot 1$, $a / 1$, $a \ll 0$, $a \gg 0$, $a \mathbin{|} 0$, $a \oplus 0$ and $a \mathbin{\&} a$ (to $a$), $a \cdot 0$, $a \mathbin{\&} 0$, $a - a$, $a \oplus a$, $a \% 1$, $a \% (-1)$ (to 0), and $a = a$, $a \le a$ (to 1) and $a < a$, $a \ne a$ (to 0), where $a - a$ means two operands with the same number. None of them removes a trap: $a / a \to 1$ and $0 / a \to 0$ are not in the list, because they are wrong for $a = 0$. The commutative operators are $+$, $\cdot$, $\&$, $|$, $\oplus$, $=$ and $\ne$.

Line L14 is the subtle step. The table remembers that a value was computed, but the name that held it may have been overwritten since. HOLDERS keeps all names that were given the number, and the check $\mathrm{VN}[n] = v$ skips the ones that now hold something else. If no name holds the value any more, the instruction is kept, and its destination gets the old number, because it computes the same value. Line L17 gives a fresh number to every value that LVN cannot describe by a key: a phi (its operands come from other blocks), a load (memory may have changed), a call, `alloc` and `addr`. A store and a call keep their place and are never removed or merged.

The implementation keeps each holder list as a queue and drops stale names from its front, so that each name is passed over at most once.

## Example

The parameters are `x`, `y` and `d`. The table lists the numbers that the implementation gives, in order: `x` is 1, `y` is 2, and so on.

| instruction | numbers | result |
|---|---|---|
| `a = x + y` | key $(+, 1, 2)$ is new, gets 3 | kept, `a` is 3 |
| `b = y + x` | commutative, key $(+, 1, 2)$, number 3, holder `a` | `b = a` |
| `a = 17` | constant 17 is 4 | kept, `a` is now 4 |
| `c = x + y` | key $(+, 1, 2)$, number 3; holder `a` is stale, `b` holds 3 | `c = b` |
| `e = c * 1` | identity $a \cdot 1$ | `e = c` |
| `f = a * 2` | both constant: $17 \cdot 2 = 34$ | `f = 34` |
| `g = x / d` | `d` is 8, key $(/, 1, 8)$ is new, gets 9 | kept |
| `h = x / d` | key $(/, 1, 8)$, number 9, holder `g` | `h = g` |
| `k = d / d` | no identity for $a / a$; key $(/, 8, 8)$ is new | kept |
| `r = g - h` | both operands have number 9: $a - a$ | `r = 0` |
| `t = c + f`, `t = t + h`, `t = t + k` | three new keys | kept |
| `t = t + r` | `r` has the number of 0: $a + 0$ | `t = t` |

The block ends with `ret t`. Before LVN a run executes 13 operations; after it, 6: `a`, `g`, `k` and the three sums. For $x = 7$, $y = 2$, $d = 3$ both blocks return $9 + 34 + 2 + 1 + 0 = 46$. For $d = 0$ both trap at `g = x / d`: the replaced division `h = x / d` could not trap on its own, because `g = x / d` ran before it with the same values. The copy `t = t` and the unused names are left for [copy propagation](/copy-propagation/) and [dead code elimination](/dead-code-elimination/).

The classic block of Cooper and Torczon shows why the key holds numbers, not names:

```
a = b + c
b = a - d
c = b + c
d = a - d
```

`d = a - d` becomes `d = b`, because `a` and `d` still hold the values they had when `b = a - d` ran. But `c = b + c` is not the same as `a = b + c`: `b` got a new number in between, so the key differs.

## Correctness

The full proof is in the proof file. It gives each value number $v$ a value $\mathrm{val}(v)$ in the run that it describes: the entry value of a name, a constant, the result of the instruction that created a key, or the value written by a phi, load or call. Two invariants hold after each instruction: every name in VN holds $\mathrm{val}$ of its number, and every key in KEY was created by an instruction that ran without a trap. From them, each case of the algorithm writes the same value as the original instruction, and traps exactly when it does:

- a folded instruction does not trap and writes the value that the target computes from the same constants;
- an identity holds for all integers and never has a trap on one side only;
- a key that is already in KEY was computed by an earlier instruction from operands with the same values, without a trap. So the current instruction cannot trap either, and a current holder has its value.

So the two blocks move through the same states. This is the simulation argument used for every local rewrite: each changed name holds the same value at every use.

## Complexity

Each instruction does a constant number of hash map lookups and inserts and one holder search. Each name enters a holder list once per definition, and each stale entry is dropped at most once, so the holder searches cost $O(n)$ in total. With hashing the expected time is $\Theta(n)$ for a block of $n$ instructions, and the maps take $\Theta(n)$ space. A unit step here is one map operation on a key of three small integers.

## Properties

- **One pass, in order.** LVN reads the block once and decides each instruction from what came before it, so it can run while a front end emits the block.
- **Never more operations.** The result has the same instructions in the same places, and an operation is only ever replaced by a constant or a copy. So every run executes at most as many operations as before, with the same total number of instructions.
- **Deterministic.** The numbering depends only on the order of the instructions. Sorting the operands of commutative operators by number makes `x + y` and `y + x` meet.
- **Local.** The maps are empty at the top of every block, so the result for one block does not depend on the others.

## Variants and improvements

- **Superlocal value numbering.** Run LVN along each path of an extended basic block, a tree of blocks in which every block but the root has one predecessor, and keep the maps of a block for its successors in the tree. Cooper and Torczon use scoped hash tables to undo the maps when they move back up the tree.
- **Dominator-based value numbering.** On [static single assignment form](/static-single-assignment-form/), the maps of a block can be passed to every block it dominates. No name is redefined in SSA, so the holder problem of line L14 disappears.
- **Global value numbering.** [Global value numbering](/global-value-numbering/) proves equalities across blocks and through phi-functions, for example by the optimistic partitioning of [Alpern, Wegman and Zadeck](/alpern-wegman-zadeck-value-numbering/).
- **The DAG of a block.** The same table builds the [expression DAG](/expression-dag/) of a block, in which each node is a key; this is [hash consing](/hash-consing/) of the expressions.
- **Loads.** A load can get a key (load, number of the address) if every store, and every call, removes the load keys that may alias it. This needs [alias analysis](/alias-analysis/) for any store through a pointer.

## When to use it

Use LVN as an early, cheap cleanup inside each block, right after the front end and after inlining or unrolling, which create repeats. It is linear, needs no dataflow analysis, and does constant folding and simple identities in the same pass. It finds nothing across blocks, so a compiler that wants more runs it inside a superlocal or dominator-based scheme, or uses global value numbering and [partial redundancy elimination](/partial-redundancy-elimination/).

## Pitfalls

- **Copying from an overwritten name.** After `a = x + y; a = 17`, the value of `x + y` is no longer in `a`. An implementation that keeps one name per number and does not check it replaces a later `x + y` by `a`, which gives 17.
- **Identities that remove traps.** $a / a \to 1$ and $0 / a \to 0$ are false for $a = 0$; the toy IR traps there. Only identities with a constant divisor or shift count that cannot trap are safe.
- **Folding with the host arithmetic.** In Python `-7 // 2` is $-4$, while the target gives $-3$. The folder must use the target rules.
- **Treating loads and calls as pure.** Two loads from the same pointer can differ if a store or a call ran in between; two calls to the same function with the same arguments can return different values. LVN gives each of them a fresh number.
- **Longer live ranges.** Replacing `c = x + y` by `c = b` keeps `b` alive longer. On a machine with few registers this can cause a spill that costs more than the addition.
- **Floating point.** $a + b = b + a$ holds in IEEE arithmetic, but $(a + b) + c = a + (b + c)$ does not, and $a - a = 0$ fails for infinities and NaN. Use only the rules that hold in the target arithmetic.

## Implementations

## History

Ershov described in 1958 how the BESM programming program numbered the operations of a formula and kept them in a table, so that a repeated operation was programmed once. Cocke and Schwartz gave a fuller description of value numbering in their 1970 Courant Institute notes on programming languages and their compilers. The dragon book builds the DAG of a basic block by the same value-number method. Cooper and Torczon present LVN with the extensions for commutative operators, constants and identities, and use it as the first step towards superlocal and dominator-based value numbering.

## References
