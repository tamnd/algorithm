---
tag: VMGC16
kind: algorithm
slug: slp-vectorization
name: Superword-level parallelism vectorization
aliases:
- SLP vectorization
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Packs isomorphic independent statements of a basic block into SIMD instructions, starting from adjacent memory accesses.
model: word-ram
complexity:
  vars: {n: the number of statements in the basic block}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [basic-block, data-dependence, vectorization]
see_also: [loop-unrolling, allen-kennedy-algorithm, simd-within-a-register, straight-line-program, expression-dag, instruction-scheduling-problem, topological-sort]
sources:
  - paper: doi:10.1145/349299.349320
    title: Samuel Larsen and Saman Amarasinghe, Exploiting superword level parallelism with multimedia instruction sets, PLDI 2000, 145-156
    locator: Section 3 (the SLP algorithm, with alignment analysis, packset seeding from adjacent memory references, extension along use-def and def-use chains, combination of pairs and scheduling) and the definitions of isomorphic and independent statements
  - paper: doi:10.1145/3276480
    title: Charith Mendis and Saman Amarasinghe, goSLP, globally optimized superword level parallelism framework, Proceedings of the ACM on Programming Languages 2(OOPSLA), 2018, article 110
    locator: the statement packing problem solved pairwise optimally with integer linear programming, and the choice of vector permutations by dynamic programming
---

SLP vectorization finds SIMD work inside one [basic block](/basic-block/). It packs statements that do the same operation on different data, and that do not depend on each other, into one SIMD instruction. Larsen and Amarasinghe named this *superword level parallelism* in 2000. Loop [vectorization](/vectorization/) needs a loop whose iterations can run side by side. SLP needs only a straight block of code, for example the body of a loop after [loop unrolling](/loop-unrolling/), or hand-unrolled code for colours, coordinates or complex numbers. The algorithm starts from loads and stores to adjacent memory cells, follows the data flow from there, and schedules the packs in an order that keeps every dependence.

## In plain words

Look at a list of small steps that a program does one after the other. Often the same kind of step appears several times on neighbouring pieces of data: load the first number, load the second number, and so on, then multiply each of them. A processor can do four or eight such steps in one go, if they are of the same kind and none of them needs the result of another. The method first finds groups of loads or stores of neighbouring memory cells. It then follows where those values go and where the stored values came from, and groups the matching steps there too. In the end it writes the groups out in an order in which every value is ready before it is used.

## The problem

**Input.** A basic block $B = s_1, \dots, s_n$ of three-address statements, and a number of lanes $VL$. A statement is a load `x = A[c]`, a store `A[c] = y`, or an operation `x = y op z`, where `x`, `y`, `z` are scalar names (`y` and `z` may be constants) and `c` is a constant index or an address known up to a common base.

**Output.** A sequence of *items*. Each item is either one statement or a *group* of 2 to $VL$ statements in a lane order. A group runs as one SIMD instruction: it reads the operands of all lanes, then writes all results. The output must compute the same final values of all names and all memory cells as $B$, for every initial state.

**Definitions.** Two statements are *isomorphic* if they do the same operation: both loads from the same array, both stores to the same array, or both operations with the same operator. They are *independent* if there is no path of [dependences](/data-dependence/) from one to the other inside $B$. A group of loads or stores is *contiguous* if lane $k + 1$ accesses the cell right after the cell of lane $k$, so that one vector load or store does the work.

The goal is to cover many statements with few groups. The best packing is an optimization problem with very many choices. The algorithm below is a greedy heuristic, and it is always correct whatever it packs.

## The algorithm

```pseudo id=main
SLP(B, VL)
L1  P <- the pairs (s, t) of loads or stores with t on the next cell after s, for which CANPACK(P, s, t)
L2  W <- the pairs of P                                   ▷ a work list
L3  while W is not empty: take a pair (s, t) from W
L4      for each operand position j: let s', t' define operand j of s and t; if CANPACK(P, s', t') then add (s', t') to P and W
L5      for each pair of uses u of s and v of t at the same operand position: if CANPACK(P, u, v) then add (u, v) to P and W
L6  G <- the chains of P, joined by (s, t), (t, u) -> (s, t, u), cut where a member depends on an earlier one or the length passes VL
L7  while some statement of B is not emitted do
L8      x <- the first statement, in text order, whose item (its group, or x alone) has all its predecessors emitted
L9      if x exists then emit the item of x
L10     else split the group of the first statement not yet emitted into single statements

CANPACK(P, s, t): s and t are isomorphic and independent, t is on the next cell after s if they access memory,
                  s is the left element of no pair in P, and t is the right element of no pair in P
```

Lines L1 to L5 build a set $P$ of pairs. The seeds of line L1 are the cheapest packs, since a contiguous vector load or store replaces several scalar ones with no shuffle. Line L4 follows the use-def chains: if $s$ and $t$ are packed, the statements that computed their operands are good candidates, because their results then land in one vector register in the right lane order. Line L5 follows the def-use chains in the same way. The rule that each statement is the left element of at most one pair and the right element of at most one pair makes $P$ a set of disjoint chains. Line L6 joins the chains, and cuts them into groups of at most $VL$ statements that are pairwise independent. Lines L7 to L10 are a list scheduler: each group waits until every statement that one of its members depends on is done. When packs wait for each other in a cycle, line L10 breaks a group up.

## Example

Unroll `A[i] = B[i] * C[i] + D[i]` four times and write it in three-address form, with names `b0`, `c0`, `m0`, `d0`, `s0` for lane 0 and so on:

```
b0 = B[0]; c0 = C[0]; m0 = b0 * c0; d0 = D[0]; s0 = m0 + d0; A[0] = s0
b1 = B[1]; c1 = C[1]; m1 = b1 * c1; d1 = D[1]; s1 = m1 + d1; A[1] = s1
... the same for lanes 2 and 3
```

These are 24 statements. Line L1 finds the seed pairs of adjacent loads $(b_0, b_1), (b_1, b_2), (b_2, b_3)$, the same for $C$ and $D$, and the adjacent stores to $A[0 \ldots 3]$. Line L5 follows the uses of $b_0$ and $b_1$ (the first operand of the multiplications) and adds $(m_0, m_1)$, and so on; it then adds the additions $(s_0, s_1), \dots$ from the uses of the products. Line L4 would find the same pairs from the stores. Line L6 joins the pairs into six chains of four. All lanes are independent, so line L8 emits them in this order:

```
<b0, b1, b2, b3> = B[0:4]
<c0, c1, c2, c3> = C[0:4]
<m0, m1, m2, m3> = <b0, b1, b2, b3> * <c0, c1, c2, c3>
<d0, d1, d2, d3> = D[0:4]
<s0, s1, s2, s3> = <m0, m1, m2, m3> + <d0, d1, d2, d3>
A[0:4] = <s0, s1, s2, s3>
```

Six SIMD instructions replace 24 scalar ones, and every operand vector is the result of one earlier group in the same lane order, so no shuffle is needed. With $VL = 2$ the same pairs give twelve groups of two.

**A blocked case.** In `a = A[0]; b = a + 1; A[1] = b; c = A[1]; d = c + 1; A[2] = d`, the loads of `A[0]` and `A[1]` are adjacent, but the second load reads the value that the first lane stored, so a path of dependences joins them. CANPACK refuses the pair, and nothing is packed.

**A cycle between packs.** Suppose two groups are $\{s_1, s_4\}$ and $\{s_2, s_3\}$, with dependences $s_1 \to s_3$ and $s_2 \to s_4$. The first group needs $s_2$ done, and the second needs $s_1$ done. No item is ready, so line L10 splits the first group, and the scheduler emits $s_1$, then the group $\{s_2, s_3\}$, then $s_4$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The output computes the same final state as $B$, whatever pairs the heuristic picks.

- **Every group is a legal SIMD instruction.** Each pair passes CANPACK, so its members are isomorphic, independent and, for memory, contiguous in lane order. Isomorphism and contiguity carry along a chain. Line L6 checks independence against every earlier member of the group, not only the neighbour, because a chain $(s, t), (t, u)$ does not by itself make $s$ and $u$ independent.
- **The schedule keeps every dependence.** The first statement not yet emitted has all its predecessors emitted, because they come earlier in the text. So if it is alone, it is ready, and if nothing is ready it is in a group, which line L10 splits. Each split removes a group, so the loop ends. An item is emitted only after every predecessor of each member, and no predecessor is inside the item, by independence.
- **Same values.** If every dependence keeps its order, each read sees the same last writer as in $B$, by the reordering argument for straight-line code. Inside a group no lane reads or writes a location that another lane writes, so reading all lanes before writing them is the same as running them one by one.

## Complexity

Let $n$ be the number of statements. Computing the dependences of a block of constant-index accesses costs $O(n^2)$, and the reachability sets for the independence test cost $O(n (n + e)) = O(n^3)$ with $e \le n^2$ edges, and $O(n^2)$ space. The seeds take $O(n^2)$ tests. Each statement is the left element of at most one pair, so at most $n$ pairs enter the work list. A pair costs $O(n)$ for its definitions and $O(n^2)$ for pairs of uses, so the extension is $O(n^3)$. Line L6 is $O(n \cdot VL)$. Each emission of the scheduler scans $O(n + e)$ statements and edges, and there are at most $n$ emissions and $n$ splits, so it is $O(n^3)$ too. The total is $O(n^3)$ time. Production compilers limit the size of the block or the search, and use cost models; the cubic bound is for the plain algorithm.

## Properties

- **Always correct.** The heuristic choices (which seeds, which candidate when several fit) change only the speed of the result.
- **Not optimal.** A greedy choice can block a better packing. The best packing is an optimization problem; goSLP solves it pairwise optimally with integer linear programming.
- **Lane order matters for cost, not for correctness.** If an operand vector is not one earlier group in the same order, the compiler needs shuffles or inserts, which cost instructions. The use-def and def-use extension keeps the lanes aligned along the data flow.
- **Works without loops.** It finds parallelism in straight code, so it also helps loops that loop vectorization rejects, after unrolling.

## Variants and improvements

- **Cost-driven choice.** Larsen and Amarasinghe estimate the savings of each candidate pair, counting packing and unpacking costs, and pick the best one when several fit. The implementation here takes the first candidate that fits.
- **Bottom-up from stores.** Some compilers, LLVM among them, start mainly from groups of adjacent stores, build a tree of packs toward the loads, and keep the tree if a cost model says it pays.
- **Global packing.** goSLP (Mendis and Amarasinghe, 2018) chooses the packs of a whole function by integer linear programming over pairs, and picks the lane permutations by dynamic programming.
- **Loop-aware SLP.** Unroll a loop by $VL$ and run SLP on the body. This covers loops whose statements are isomorphic only after unrolling, and loops with a few lanes of different shape.
- **Reductions and alternating operations.** Extensions pack trees of additions that end in one sum, and pairs such as `+` and `-` in alternate lanes, when the machine has an add-subtract instruction.

## When to use it

Use SLP for code that is already unrolled, for structures of a few fields that are processed in the same way, and as a second pass after loop vectorization. Use loop vectorization when a loop has many iterations with the same body; it does not need unrolling and covers long trip counts with one vector loop. For a whole loop nest with carried dependences, the [Allen-Kennedy algorithm](/allen-kennedy-algorithm/) is the tool.

## Pitfalls

- **Checking independence only between neighbours.** Two pairs $(s, t)$ and $(t, u)$ can each be independent while $u$ depends on $s$ through a third statement. Packing $s$, $t$ and $u$ into one group then reads a value before it is written.
- **Direct dependence instead of a path.** Two statements with no direct dependence may still be joined by a path through others. Packing them makes the group wait for a statement that waits for the group.
- **Unknown addresses.** With pointers, two stores may hit the same cell. Without an alias analysis that proves otherwise, the compiler must add a dependence, which blocks the pack.
- **Packs that do not pay.** A group whose operands come from scattered scalars needs one insert per lane, and a group whose results are used one by one needs one extract per lane. The cost model must count these, or the vector code is slower.
- **Ignoring cycles between groups.** A scheduler that just emits groups in text order can run a group before a statement that one of its members needs.

## Implementations

## History

Samuel Larsen and Saman Amarasinghe introduced superword level parallelism at MIT and presented the algorithm at PLDI 2000, aiming at the short SIMD units of multimedia instruction sets. They showed that unrolled loop bodies and straight-line kernels have much SIMD work that loop vectorization does not see. GCC and LLVM later added SLP vectorizers, and research went on to optimal packing, as in goSLP in 2018.

## References
