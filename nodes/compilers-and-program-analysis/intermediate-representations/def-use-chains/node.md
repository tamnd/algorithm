---
tag: XZ8C52
kind: data-structure
slug: def-use-chains
name: Def-use chains
aliases:
- use-def chains
- du-chains
- ud-chains
area: compilers-and-program-analysis/intermediate-representations
level: intro
summary: Links each definition of a variable to the uses it can reach and each use to the definitions that can reach it.
prereqs: [three-address-code, basic-block, control-flow-graph]
see_also: [reaching-definitions, static-single-assignment-form, live-variable-analysis, dead-code-elimination, copy-propagation, sparse-conditional-constant-propagation, program-dependence-graph, chaitin-register-allocation]
sources:
  - paper: doi:10.1016/0096-0551(78)90009-7
    title: Ken Kennedy, Use-definition chains with applications, Computer Languages 3(3), 1978, pages 163-179
    locator: use-definition chains, how to compute them from reaching definitions, and their use in program optimization
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.2.4 (reaching definitions, with gen and kill sets per block and the iterative solution)
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 8 (Data-Flow Analysis), the section on du-chains, ud-chains and webs
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), iterative data-flow analysis and static single-assignment form
---

Def-use chains record, for a program in [three-address code](/three-address-code/), which definitions of a variable can supply the value that each use reads. A *du-chain* links a definition to all the uses it can reach; a *ud-chain*, or use-def chain, links a use to all the definitions that can reach it. Both are the same set of pairs, read in two directions. A definition $d$ of $x$ reaches a use of $x$ if some path in the [control flow graph](/control-flow-graph/) leads from $d$ to the use without another definition of $x$. The chains are built from the answer of [reaching definitions](/reaching-definitions/), and optimizations then follow them instead of scanning the whole program: [copy propagation](/copy-propagation/), [dead code elimination](/dead-code-elimination/), constant propagation, induction variable analysis and the webs of register allocation. They can be large: $k$ definitions that meet at one join and reach $k$ uses give $k^2$ links, which is one reason for [static single assignment form](/static-single-assignment-form/).

## In plain words

A program sets variables in some places and reads them in others. When a line reads a variable, the compiler wants to know which earlier lines could have set the value it gets. It looks at every way the program can run to that line and keeps the lines that set the variable last before it. A ud-chain is that list for one reading line. A du-chain goes the other way: for one line that sets a variable, the list of lines that can read the value it wrote. With these lists, a compiler can see that a value is never read, so its line can go, or that only one line can set a value, so that value is known. It follows the lists instead of reading the whole program again.

## The abstract type

The structure stores a relation between two kinds of sites. A *definition site* $(b, i, x)$ is instruction $i$ of block $b$ when it writes the name $x$; a parameter $x$ is the site $(\mathit{entry}, -1, x)$, written on the way into the program. A *use site* $(b, i, x)$ is instruction $i$ of block $b$ when it reads $x$, and $i = n_b$, the number of instructions of $b$, means the terminator. The operations are:

- `chains(P)`: build the structure for program $P$.
- `du(d)`: the uses that definition $d$ reaches.
- `ud(u)`: the definitions that reach use $u$.

The law: $u \in du(d)$ if and only if $d \in ud(u)$ if and only if $d$ reaches $u$. Here $d$ of $x$ *reaches* $u$ if some path from the point just after $d$ to $u$ passes no other definition of $x$; the instruction at $u$ may itself define $x$, since it reads first. A phi operand that comes from the predecessor $p$ counts as a use at the end of $p$. The relation is about paths, not about runs: a path that no input can take still counts, so the chains may contain pairs that never happen, but they miss no pair that does happen in a run that writes variables only by name.

## Representation

Two maps hold the relation: `du` from each definition site to the sorted list of its uses, and `ud` from each use site to the sorted list of its definitions. Every definition site is a key of `du`, even with no uses, and every use site is a key of `ud`, even with no definitions. A compiler keeps the lists on the instructions themselves, as pointers, so that it can go from an instruction to its uses in constant time per link.

To build the maps, the code first solves reaching definitions per block. $GEN[b]$ holds the last definition in $b$ of each name, and $KILL[b]$ holds the names that $b$ defines. $IN[b]$ and $OUT[b]$ are the definitions that reach the start and the end of $b$. Compilers store these sets as bit vectors with one bit per definition site; the Python code uses sets of site tuples.

## Operations

```pseudo id=main
BUILD-CHAINS(P)
L1  for each block b: GEN[b] <- the last definition in b of each name; KILL[b] <- the names b defines
L2  OUT[b] <- GEN[b] for every block b
L3  repeat
L4      for each block b in reverse postorder do
L5          IN[b] <- the union of OUT[p] over the predecessors p of b, plus the parameters if b is the entry
L6          OUT[b] <- GEN[b] ∪ {d in IN[b] : the name of d is not in KILL[b]}
L7  until no OUT set changed in the pass
L8  for each block b do
L9      live[x] <- the definitions of x in IN[b], for every name x
L10     for each instruction s of b in order, then the terminator do
L11         link every d in live[x] with the use (s, x), for each name x that s reads
L12         if s defines x then live[x] <- {s}
L13 return du and ud
```

Lines L1 to L7 are the round-robin solution of reaching definitions. Lines L8 to L12 walk each block once: $live[x]$ is always the set of definitions of $x$ that reach the current instruction, so a read of $x$ is linked to exactly those. Line L11 reads before line L12 writes, so `i = i + 1` links its read of `i` to the earlier definitions, not to itself. A phi is the exception to line L11: its operand from predecessor $p$ is linked to the definitions of that name in $OUT[p]$, because the value is chosen on the edge from $p$.

`du(d)` and `ud(u)` are lookups in the two maps. The function `reaching` returns $IN$, $OUT$ and the number of passes.

## Example

The odd-sum program of the [control flow graph](/control-flow-graph/) page, with the parameter `n`:

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

Reaching definitions in reverse postorder B1, B2, B6, B3, B4, B5 settle in 2 passes, and a third pass changes nothing. Since $OUT$ starts at $GEN$, `i = i + 1` reaches the loop header B2 along $B5 \to B2$ already in the first pass. `s = s + i` in B4 gets there only in the second pass, after the first pass has carried it into $OUT[B5]$. The chains, as du-chains:

| definition | uses it reaches |
|---|---|
| `n` (parameter) | `t1 = i < n` in B2 |
| `i = 0` in B1 | the reads of `i` in B2, B3, B4 and B5 |
| `i = i + 1` in B5 | the reads of `i` in B2, B3, B4 and B5 |
| `s = 0` in B1 | `s = s + i` in B4, `ret s` in B6 |
| `s = s + i` in B4 | `s = s + i` in B4, `ret s` in B6 |
| `t1` in B2 | `br t1` in B2 |
| `t2` in B3 | `br t2` in B3 |

There are 15 links. Read as ud-chains, the use of `s` in `ret s` has two definitions, `s = 0` and `s = s + i`, so `s` is not a constant there. The definition `s = s + i` reaches its own read through the loop. Each `ti` has one definition and one use, so a compiler could fold the comparison into the branch. The program returns 9 for $n = 6$.

## Correctness

The proof file shows three things. First, the sets "definitions that reach the start of $b$" and "definitions that reach the end of $b$" are the least solution of the equations of lines L5 and L6: they solve them, by cutting a path at its last entry into $b$, and every solution contains them, by induction on the length of the path. Second, the iteration starts below this least solution, stays below it and only grows, so it stops, and when a pass changes nothing it has reached the least solution; at most $B D + 1$ passes are needed, for $B$ blocks and $D$ definition sites. Third, during the scan of a block, $live[x]$ is always the set of definitions of $x$ that reach the current instruction, because the only way into instruction $i + 1$ is through instruction $i$. So each use is linked to exactly the definitions that reach it. The proof covers names only. A store through a pointer writes a variable without naming it, and the chains do not see it.

## Complexity

Let $B$ be the number of blocks, $E$ the number of edges, $I$ the number of instructions, $D$ the number of definition sites, $U$ the number of use sites and $C$ the number of links.

| part | time | space |
|---|---|---|
| GEN and KILL (line L1) | $O(I)$ | $O(B D / w)$ words as bit vectors |
| one pass of lines L4 to L6 | $O((B + E)\, D / w)$ word operations | |
| the scan (lines L8 to L12) | $O(I + C)$ set operations plus reading the IN sets | |
| the chains | | $\Theta(C)$, with $C \le D \cdot U$ |

**Proved.** At most $B D + 1$ passes, in the proof file. The number of links can be quadratic: $k$ blocks that each set `x` and jump to one join block, followed by $k$ reads of `x` and `ret x`, give $k (k + 1)$ links, because each of the $k + 1$ uses is reached by all $k$ definitions. In SSA form the join gets one phi with $k$ operands and the count is $2k$.

**Cited, not proved.** For bit-vector problems such as reaching definitions, round-robin iteration in reverse postorder needs at most the loop connectedness plus 2 passes ([Kam-Ullman bound](/kam-ullman-iteration-bound/)). Structured programs have small loop connectedness, so a few passes are usual.

**Measured, not proved.** Over 3,000 seeded random toy programs with loops and up to 9 blocks, the iteration took 1 pass on 46 programs, 2 on 2,571, 3 on 363 and 4 on 20. On one random program with 400 blocks it took 13 passes and built 19,451 links; on one with 1,600 blocks, 12 passes and 348,930 links, which shows how fast the chains grow on large functions.

## Variants

- **Static single assignment form.** Rename each definition so that every name has one, and put phi-functions at joins. Then the ud-chain of each use has exactly one element, the du-chain of a name is its list of uses, and the size is linear in the program. Most modern compilers keep this form instead of chains.
- **Webs.** A web is a maximal set of du-chains of one name that share uses. Each web becomes one live range in [Chaitin-style register allocation](/chaitin-register-allocation/), and different webs of the same name can get different registers.
- **Data dependence edges.** In a [program dependence graph](/program-dependence-graph/), the data edges are the def-use chains, next to the control dependence edges.
- **Only one direction.** Some passes need only ud-chains, for example constant propagation, which asks "what can this use see". Others need only du-chains, for example dead code elimination, which asks "is this value read".
- **Pointers and calls.** With pointer analysis, a store `*p = a` becomes a possible definition of each variable that `p` may point to. Such a definition does not kill the earlier ones, because the store may write somewhere else.
- **Sparse analyses.** Constant propagation and similar analyses can run over the chains instead of over the blocks, so that they only visit places where a value can flow. [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) does this on SSA form.

## When to use it

Use def-use chains when an analysis or optimization asks again and again which definitions a use can see, or which uses a definition feeds, and the program is not in SSA form: in a simple compiler, in a debugger or program analysis tool that works on the original variables, or in a register allocator that builds webs. For a full optimizing compiler, SSA form gives the same information in linear size and is easier to keep up to date when the code changes.

## Pitfalls

- **Phi operands.** A phi operand from predecessor $p$ is a use at the end of $p$, not at the top of the join block. Treating it as a use at the join links it to definitions that come in on other edges.
- **Pointers.** If a variable's address is taken, a store through a pointer can change it, and chains built from names alone miss that definition. Either treat such stores as possible definitions or leave address-taken variables out.
- **Uninitialized variables.** A ud-chain lists the definitions that reach a use, but it does not say whether some path reaches the use with no definition at all. Add a dummy definition of every name at the entry to find such paths.
- **Unreachable code.** A definition in a block that the entry does not reach still has paths to later uses, and the iteration counts it. Delete unreachable blocks first if this matters.
- **Size.** The number of links can grow with the square of the number of definitions of a name. Large generated functions can make the chains much bigger than the code.
- **Stale chains.** A transformation that moves, copies or deletes an instruction changes the chains. Rebuild them or update them, or the next pass works on wrong facts.

## Implementations

## History

Reaching definitions was among the first global data-flow problems that optimizing compilers solved, in the work of Allen and Cocke at IBM in the late 1960s and 1970s, and the chains were the usual way to keep its answer per use. Kennedy's paper of 1978 described use-definition chains and many optimizations built on them. Textbooks of the 1980s and 1990s, among them the dragon book and Muchnick, presented du-chains, ud-chains and webs as the standard tools of global optimization. Static single assignment form, from Cytron, Ferrante, Rosen, Wegman and Zadeck (1991), made each ud-chain a single definition and replaced explicit chains in most compilers.

## References
