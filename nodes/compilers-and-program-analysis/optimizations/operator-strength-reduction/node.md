---
tag: VGSWKK
kind: algorithm
slug: operator-strength-reduction
name: Operator strength reduction on SSA
aliases:
- Cooper-Simpson-Vick strength reduction
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Finds induction variables as strongly connected components of the SSA graph and rewrites their multiplications into additions.
model: word-ram
complexity:
  vars: {n: the size of the input (instructions and operands), b: the number of blocks, m: the number of instructions that the pass creates}
  time: {worst: O(b^3 + (n + m)^2)}
  space: {extra: O(n + m + b)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [strength-reduction, static-single-assignment-form, induction-variable-analysis, tarjan-scc]
see_also: [chains-of-recurrences, phi-function, natural-loop, cooper-harvey-kennedy-dominance, dead-code-elimination, copy-propagation, loop-invariant-code-motion, global-value-numbering]
sources:
  - paper: doi:10.1145/504709.504710
    title: Keith D. Cooper, L. Taylor Simpson and Christopher A. Vick, Operator strength reduction, ACM Transactions on Programming Languages and Systems 23(5), 2001, 603-625
    locator: the algorithm OSR with the procedures ClassifyIV, Replace, Reduce and Apply, the header as the member first in reverse postorder, region constants, and linear function test replacement through the edges that Reduce records
  - book: isbn:9780137296811
    title: Frances E. Allen, John Cocke and Ken Kennedy, Reduction of operator strength, in Steven S. Muchnick and Neil D. Jones (eds.), Program Flow Analysis, Theory and Applications, Prentice-Hall, 1981
    locator: pp. 79-101, the earlier algorithm on strongly connected regions of the flow graph, with a table of temporaries and linear function test replacement
  - paper: doi:10.1145/359863.359888
    title: John Cocke and Ken Kennedy, An algorithm for reduction of operator strength, Communications of the ACM 20(11), 1977, 850-856
    locator: the table of temporaries indexed by the reduced expression, and the replacement of loop tests
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 1972, 146-160
    locator: the strongly connected components algorithm, which emits a component after every component it reaches
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 10 (Scalar Optimizations), the part on strength reduction with the algorithm OSR and linear function test replacement
---

Operator strength reduction on [static single assignment form](/static-single-assignment-form/) is the version of [strength reduction](/strength-reduction/) that Cooper, Simpson and Vick gave in 2001. It finds the induction variables of a procedure as strongly connected components of the SSA graph, the graph from each name to the names its definition reads. A product `iv * rc` of an induction variable and a value that the loop does not change then becomes a new induction variable, which the loop updates with adds. The algorithm needs no loop tree and no data-flow analysis: one pass of [Tarjan's algorithm](/tarjan-scc/) over the SSA graph does the work. It ends with linear function test replacement, which rewrites the loop test so that the old counter often becomes dead.

## In plain words

A loop that counts 0, 1, 2 and so on and multiplies the count by 4 each time does a multiply per trip. The products go up by 4 each time, so a second counter that starts at 0 and adds 4 gives the same numbers without the multiply. To find such counters, the method looks at which values feed which. A counter feeds itself around the loop through adds of fixed amounts, so it forms a closed cycle of values. The method finds each such cycle once, makes a new counter for each product, and points the product at it. When the loop test only compares the old counter with a limit, it compares the new counter with the limit times 4 instead. Then the old counter has no use left and goes away.

## The problem

The input is a program of the toy IR of [three-address code](/three-address-code/) in strict SSA form. Every name has one definition, [phi-functions](/phi-function/) stand at the tops of blocks, every use is dominated by its definition, no name is address-taken, every block is reachable, and the entry block has no predecessor. The output is a program in strict SSA form with the same outcome on every input, the same return value or the same trap, in which the products of induction variables and region constants are computed by adds.

The *SSA graph* has a node for each defined name and an edge from a name to each defined name that its definition reads. Let $N$ be a strongly connected component of it with more than one member, and let its *header* $h$ be the block of a member that comes first in reverse postorder. A *region constant* for $h$ is an integer, a parameter, or a name whose definition is in a block that strictly [dominates](/dominator-tree/) $h$. $N$ is an *induction variable* if $h$ dominates the blocks of all its members and every member is a phi-function, a copy, $iv + rc$, $rc + iv$ or $iv - rc$, with $iv$ in $N$ and $rc$ a region constant for $h$. A *candidate* is an instruction $x = iv \times rc$, $x = rc \times iv$, $x = iv + rc$, $x = rc + iv$ or $x = iv - rc$ with $iv$ an induction variable and $rc$ a region constant for its header.

## The algorithm

The table maps a key $(op, o_1, o_2)$ to the name that holds $o_1 \mathbin{op} o_2$. It is what makes two products of the same induction variable and constant share one new variable.

```pseudo id=main
OSR(P)
L1  compute the dominator tree and a reverse postorder of the blocks of P
L2  for each SCC N of the SSA graph, in the order Tarjan's algorithm finds them, do
L3      if N has more than one member then ClassifyIV(N)
L4      else if the member n of N is a candidate x = iv op rc then Replace(n, iv, rc)
L5      else mark n as not an induction variable
L6  replace the tests of induction variables (linear function test replacement)
L7  delete the instructions that no effect, branch or return needs
ClassifyIV(N)
L8  header <- the block of a member of N that comes first in reverse postorder
L9  if header dominates every member, and every member is a phi, a copy, iv + rc, rc + iv or iv - rc with iv in N and rc a region constant for header, then
L10     mark every member of N as an induction variable with this header
L11 else for each member n of N do
L12     if n is a candidate then Replace(n, iv, rc) else mark n as not an induction variable
Replace(n, iv, rc)
L13 result <- Reduce(op, iv, rc)
L14 replace n by x = result and mark x as an induction variable with the header of iv
Reduce(op, iv, rc)
L15 if (op, iv, rc) is in the table then return its entry
L16 result <- a new name; add (op, iv, rc) -> result to the table
L17 make a copy of the definition of iv that defines result
L18 for each operand o of the copy do
L19     if o is an induction variable with the header of iv then replace o by Reduce(op, o, rc)
L20     else if op is * or the copy is a phi then replace o by Apply(op, o, rc)
L21 insert the copy right after the definition of iv; mark result as an induction variable with the header of iv
L22 return result
Apply(op, o1, o2)
L23 if (op, o1, o2) is in the table then return its entry
L24 if o1 is an induction variable and o2 is a region constant for its header then return Reduce(op, o1, o2)
L25 if op is commutative, o2 is an induction variable and o1 is a region constant for its header then return Reduce(op, o2, o1)
L26 if o1 and o2 are constants then return o1 op o2
L27 result <- a new name; add (op, o1, o2) -> result to the table
L28 insert result = o1 op o2 at the end of the deeper of the blocks that define o1 and o2
L29 return result
```

Tarjan's algorithm emits a component only after every component that it reaches, so the operands of a definition are classified before the definition itself (line L2). A product of an induction variable is then seen after the variable is known, and the new name of line L14 is an induction variable that later candidates can use, so `(i * 4) + 5` becomes one new variable.

Line L19 follows the cycle: the copy of `i2 = i + 1` for the key `(*, i2, 4)` reads the copy of `i` for `(*, i, 4)`. Line L20 scales the other operands. For `*`, the step 1 becomes $1 \cdot 4$. For a phi-function, the start value 0 becomes $0 \mathbin{op} rc$. For `+` and `-` on the step of an add, the step stays the same. Line L28 puts the computations of new region constants where both operands are already known, which is outside the loop.

Line L6 looks at each comparison of an induction variable $iv$ with a region constant $b$. If $iv$ has a reduction $r = iv \mathbin{op} k$, the comparison becomes $r$ against $\mathrm{Apply}(op, b, k)$, and the step repeats with $r$. For `+` and `-` this is always valid. For `*` the pass uses only an integer $k \ne 0$, and for $k < 0$ it swaps the sides of `<` and `<=`. Line L7 marks the names that terminators, stores, calls, loads, `alloc` and operations that may trap read, then the names their definitions read, and deletes the other constants, copies, phi-functions and operations. This removes the old counter when nothing else reads it, even though it reads itself around the loop.

## Example

The parameters are `k` and `n`, and the program sums `i * 4 + 5` for `i` from 0 to `n - 1`.

```
entry:
  jump h
h:
  i = phi [entry: 0, body: i2]
  s = phi [entry: 0, body: s2]
  c = i < n
  br c body done
body:
  x = i * 4
  y = x + 5
  s2 = s + y
  i2 = i + 1
  jump h
done:
  ret s
```

Tarjan's algorithm finds the component $\{i, i2\}$ with header `h`. Its members are a phi and `i + 1`, so it is an induction variable. The component $\{s, s2\}$ is not one, because `s2 = s + y` adds `y`, which is defined in the loop. `x = i * 4` is a candidate. Reduce copies the phi of `i` into `osr1 = phi [entry: 0, body: osr2]` with $0 \cdot 4 = 0$, and the add into `osr2 = osr1 + 4` with $1 \cdot 4 = 4$, and `x` becomes `x = osr1`. Then `y = x + 5` is a candidate on the new variable `x`. Reduce makes `osr4 = phi [entry: 5, body: osr5]` and `osr5 = osr4 + 4`, and `y` becomes a copy of it through `osr3`.

Line L6 rewrites `c = i < n`. The reduction `(*, i, 4)` turns it into `osr1 < n * 4`, and the reduction `(+, osr1, 5)` into `osr4 < n * 4 + 5`. Apply puts `osr6 = n * 4` and `osr7 = osr6 + 5` at the end of `entry`. Now `i`, `i2`, `x`, `osr1` and `osr2` have no needed use, and line L7 deletes them.

```
entry:
  osr6 = n * 4
  osr7 = osr6 + 5
  jump h
h:
  osr4 = phi [entry: 5, body: osr5]
  s = phi [entry: 0, body: s2]
  c = osr4 < osr7
  br c body done
body:
  osr3 = osr4
  y = osr3
  s2 = s + y
  osr5 = osr4 + 4
  jump h
done:
  ret s
```

For $n = 3$ both programs return 27. The loop has no multiply left. The one multiply in `entry` runs once. The copies `osr3` and `y` stay. In the toy IR, where every instruction costs one step, the new program takes 35 steps against 33, because of the two instructions in `entry`. After [copy propagation](/copy-propagation/) and [dead code elimination](/dead-code-elimination/) remove the copies, the loop body has two instructions in place of four, and the run takes 29 steps. For $n = 10$ it takes 78 steps against 96.

With `x = i * -2` in place of `x = i * 4 + 5`, the test `i < n` becomes `osr3 < osr1` with `osr3 = n * -2`, because multiplying both sides by a negative number reverses the order. With `x = i * k`, the test stays, because the sign of `k` is not known.

## Correctness

The full proof is in the proof file. It assumes strict SSA form, unbounded integers, and that no pointer reaches an arithmetic operation.

1. **The new names are defined in time.** A copy of Reduce stands right after the definition of its induction variable. A name of Apply stands at the end of a block that defines one operand and is dominated by the other. A short argument on dominators shows that both come before every point that reads them. So the output is in strict SSA form.
2. **The new names hold what their keys say.** At every read of a name for the key $(op, o_1, o_2)$, its value equals $o_1 \mathbin{op} o_2$ for the current values. The proof is by induction on the time of the read. For a copy of Reduce it uses the identities $(a + b) k = ak + bk$, $(a - b) k = ak - bk$ and $(a + b) \pm k = (a \pm k) + b$. Two facts on dominance show that the operands have not changed since the last definition.
3. **The rewritten instructions compute the same values.** A replaced candidate reads a name that holds $iv \mathbin{op} rc$. A replaced test compares values that are both shifted by the same amount, or multiplied by the same nonzero integer, with the sides swapped if it is negative.
4. **The rest is the same.** The new instructions cannot trap and define only new names, so the old and the new program visit the same blocks and take the same branches. The deletion removes only instructions that cannot trap and whose names no kept instruction reads.

So the new program returns the same value or traps in the same visit, on every input.

## Complexity

The input has size $n$, counting instructions and operands, in $b$ blocks, and the pass creates $m$ instructions. Dominators by the iterative algorithm of [Cooper, Harvey and Kennedy](/cooper-harvey-kennedy-dominance/) take $O(b^3)$ time in the worst case and close to $O(b)$ on the graphs of real programs. Tarjan's algorithm takes $O(n)$. Each key enters the table once, so Reduce copies each definition at most once per key, and Apply does constant work besides the table. The implementation finds a definition by a scan of its block, which gives the $O((n + m)^2)$ term. With a map from names to positions, the work after the dominators is close to $O(n + m)$.

The number $m$ of new instructions is not bounded by a constant factor of $n$. Each distinct pair $(op, rc)$ used with an induction variable makes a copy of its whole component, so $m$ can grow as the number of candidates times the size of the components. The extra space is the table, the marks and the dominator tree.

## Properties

- **Sparse.** It works on the SSA graph only. It needs dominators but no loop nesting tree and no data-flow sets.
- **One pass in a good order.** Tarjan's order classifies operands before their users, so chains such as `(i * 4) + 5` reduce in one pass, and the results of Replace serve later candidates.
- **It shares work.** The table maps equal keys to one name, as in [global value numbering](/global-value-numbering/), so `i * 4` in two places gives one new variable.
- **It needs cleanup.** It leaves copies, and the old variables die only after test replacement. Copy propagation and dead code elimination finish the job.
- **Recursive.** Reduce calls itself around the cycle of a component and through Apply. The depth grows with the size of the component and the length of a chain of reductions.

## Variants and improvements

- **Allen, Cocke and Kennedy.** The earlier algorithm works on strongly connected regions of the control flow graph, the loops, and finds induction variables and region constants by data-flow analysis. It handles the same candidates. Cooper, Simpson and Vick report that their SSA version gives the same results and is simpler to implement.
- **Wider classes.** [Chains of recurrences](/chains-of-recurrences/) describe polynomial and geometric sequences, so a product of two induction variables can also become adds, with a second order recurrence.
- **Address computations.** In practice the candidates are mostly array addresses such as `base + i * 8`. A pass of [loop-invariant code motion](/loop-invariant-code-motion/) first moves invariant parts out of the loop, so they become region constants.
- **Test replacement with a computed limit.** When the multiplier is not a known integer, a compiler can still replace a test of equality if it knows that $k \ne 0$, or a test of order if it knows the sign of $k$.

## When to use it

Use it in a compiler that keeps the program in SSA form and wants the classic loop strength reduction without a loop tree or data-flow sets. It is most useful for array addresses and for loops whose counter is used only in products and in the loop test. Run it after loop-invariant code motion, so that more operands are region constants, and before copy propagation and dead code elimination. Do not use it when the new variables would not fit in registers: each reduction adds a variable that is live around the loop.

## Pitfalls

- **Wrapping integers.** The identities of the rewrite hold modulo $2^w$, but test replacement with `<` or `<=` does not: `osr4 < n * 4 + 5` can wrap when `i < n` cannot. A compiler for fixed-width integers must prove that the new values do not wrap, or keep the old test.
- **Region constants defined in the header.** A name defined in the header itself changes on each trip. The definition of a region constant must strictly dominate the header.
- **Sums of two members.** `i2 = i + i` is in the component but is not an induction variable of the linear kind. ClassifyIV must check that exactly one operand of each add is in the component.
- **The sign of the multiplier.** Test replacement through `x = i * k` with `k` not known must not change `<`. With $k = 0$ every product is 0, and for $k < 0$ the order reverses.
- **Traps.** A candidate never traps, but `a / i` does when `i` is 0. The pass must not touch it, and the cleanup must keep it, as an operation that may trap.
- **Placement of the new region constants.** A product of two region constants that is put in the loop runs on every trip. Line L28 puts it in the deeper of the defining blocks, which dominates the header.

## Implementations

## History

Strength reduction is one of the oldest loop optimizations of optimizing compilers. Cocke and Kennedy published an algorithm in 1977, and Allen, Cocke and Kennedy gave the full method with linear function test replacement in 1981. It works on the strongly connected regions of the flow graph. Cooper, Simpson and Vick moved it to SSA form in 2001: they found the induction variables as strongly connected components of the SSA graph with Tarjan's algorithm of 1972, and kept the table of temporaries of the earlier work. Their algorithm OSR is the one taught in the textbook of Cooper and Torczon.

## References
