---
tag: N0QEY1
kind: algorithm
slug: sreedhar-cssa-translation
name: Sreedhar out-of-SSA translation
aliases:
- conventional SSA translation
area: compilers-and-program-analysis/intermediate-representations
level: advanced
summary: Converts SSA into conventional SSA, where phi-related names do not interfere, by inserting copies, and then drops all phi-functions.
solves: [out-of-ssa-translation]
model: word-ram
complexity:
  vars: {N: the size of the program (each phi operand counts), V: the number of names, B: the number of blocks, F: the number of phi-functions}
  time: {worst: O(F B N V + N^2 V^2), average: O(F B N V + N^2 V^2), best: Θ(N)}
  space: {extra: O(N + V^2)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [out-of-ssa-translation, lost-copy-and-swap-problems, live-variable-analysis, interference-graph]
see_also: [static-single-assignment-form, phi-function, critical-edge-splitting, copy-propagation, register-coalescing-problem, ssa-based-register-allocation, disjoint-set-forest, chaitin-register-allocation]
sources:
  - paper: doi:10.1007/3-540-48294-6_13
    title: Vugranam C. Sreedhar, Roy Dz-Ching Ju, David M. Gillies and Vatsa Santhanam, Translating out of static single assignment form, Static Analysis Symposium (SAS 1999), LNCS 1694
    locator: conventional and transformed SSA form, phi congruence classes, Method I (copies for every resource), Method II (guided by the interference graph), Method III (guided by liveness and the interference graph, with four cases and deferred pairs), and copy coalescing on phi congruence classes
  - paper: "Preston Briggs, Keith D. Cooper, Timothy J. Harvey and L. Taylor Simpson, Practical improvements to the construction and destruction of static single assignment form, Software: Practice and Experience 28(8), 1998, pages 859-881"
    locator: the lost copy and swap problems, which the method solves without splitting edges
  - paper: doi:10.1109/CGO.2009.19
    title: Benoit Boissinot, Alain Darte, Fabrice Rastello, Benoît Dupont de Dinechin and Christophe Guillon, Revisiting out-of-SSA translation for correctness, code quality, and efficiency, International Symposium on Code Generation and Optimization (CGO 2009), pages 114-125
    locator: Method I with parallel copies as the starting point, followed by coalescing with value-based interference
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms), conventional SSA and its destruction with copies; Chapter 21 (SSA Destruction for Machine Code)
---

Sreedhar's out-of-SSA translation removes the [phi-functions](/phi-function/) of a program in [static single assignment form](/static-single-assignment-form/) without splitting edges. It works in two steps. First it adds copies until the program is in *conventional SSA form*: no two names joined by phi-functions are live at the same time. Then it gives all the names of each such group one variable and deletes the phi-functions. Sreedhar, Ju, Gillies and Santhanam published it in 1999 with three ways to choose the copies. Method I copies every resource of every phi-function. Method III uses liveness and interference to copy only where it is needed. It solves the [lost copy and swap problems](/lost-copy-and-swap-problems/), which break the older translation after copy folding.

## In plain words

A phi-function joins several names into one value. If none of these names is ever needed while another one holds a different value, they can all share one variable, and the phi-function becomes nothing. Optimizations break this. For example, a loop may still read the old value of a counter after the new value is made. The fix is to add a copy that gives one of the names a short private life: just before the jump in the block that feeds the phi-function, or just after the phi-functions at the top of the block. A careful choice of copies leaves only a few. When no group has a conflict left, rename the group to one variable and drop the phi-functions.

## The problem

The input is a strict SSA program. Phi-functions come first in each block and have one operand for each predecessor. An operand is a name or a constant. The output is an equivalent program with no phi-functions, as on the [out-of-SSA translation](/out-of-ssa-translation/) page. The method must not split edges or add blocks.

Most of the terms below come from Sreedhar et al. The *resources* of the phi-function $x_0 = \phi(x_1, \ldots, x_n)$ are its target $x_0$ and its operands $x_i$, where $x_i$ comes from the predecessor $L_i$ of the block $L_0$. The *phi congruence classes* are the classes of the smallest equivalence relation that relates each target to its operands. A name is *live* at a point if some path from there reads it before it is defined again. An operand $x_i$ is read at the end of $L_i$. Two names *interfere* if one is live just after the definition of the other. A program is *conventional* if no two names in one class interfere. Otherwise it is *transformed*. SSA form straight after construction is conventional. [Copy propagation](/copy-propagation/) and the removal of trivial phi-functions can make it transformed.

## The algorithm

For a resource $i$ of the current phi-function, $\mathrm{LIVE}(i)$ is the set of names that a new copy name for $i$ would interfere with. For an operand from $L_i$ it is $\mathrm{LiveOut}(L_i)$ plus the names read by the terminator of $L_i$, because the copy goes just before the terminator. For the target it is the set of names live just after the phi-functions of $L_0$, plus the other phi targets of $L_0$ and the targets of the copies already placed after them, without $x_0$ itself.

```pseudo id=main
SREEDHAR-METHOD-III(P)
L1  make each name its own phi congruence class
L2  for each phi-function x0 = phi(x1 from L1, ..., xn from Ln) of P do
L3      compute liveness and the interference graph of P
L4      chosen <- the resources that are constants
L5      for each pair i < j of named resources with xi != xj do
L6          if no name in class(xi) interferes with a name in class(xj) then go to the next pair
L7          needI <- class(xi) ∩ LIVE(j) != {}; needJ <- class(xj) ∩ LIVE(i) != {}
L8          if needI then add i to chosen
L9          if needJ then add j to chosen
L10         if not needI and not needJ then record i and j as deferred neighbours
L11     for each deferred resource i, the one with most deferred neighbours first do
L12         if i is not in chosen and some neighbour of i is not in chosen then add i to chosen
L13     while some i in chosen and j not in chosen have class(xj) ∩ LIVE(i) != {} do
L14         add j to chosen
L15     for each chosen resource, add a copy and use the new name in the phi-function
L16     merge the classes of x0, x1, ..., xn
L17 give each class one variable, delete the phi-functions and the copies v <- v
```

Line L15 puts the copy for an operand $x_i$ as `xi' = xi` at the end of $L_i$, before its terminator. A constant operand gets `xi' = k`. The copy for the target puts `x0 = x0'` just after the phi-functions of $L_0$, and $x_0'$ becomes the target. The new names are fresh, so the program stays in SSA form. Method I skips lines L3 to L14 and chooses every resource. Lines L5 to L12 are the four cases of the paper: copy $x_i$ if its class is live where $x_j$ is defined or read, copy $x_j$ in the opposite case, copy both if both hold, and defer the pair if neither holds. Lines L13 and L14 are a closing step added in this implementation; Pitfalls explains why it is needed.

Line L17 picks the parameter of the class as its variable if there is one, otherwise the smallest name. The implementation computes liveness and interference again for each phi-function. The paper updates them in place.

## Example

**The lost copy.** After copy propagation, the loop returns the old value of `x` from the last pass:

```
# params: n
B1:
  x.1 = 1
  jump B2
B2:
  x.2 = phi [B1: x.1, B2: x.3]
  x.3 = x.2 + 1
  t.1 = x.3 < n
  br t.1 B2 B3
B3:
  ret x.2
```

The one class is $\{x.2, x.1, x.3\}$. For $n = 3$ the program returns 2. If `x.1`, `x.2` and `x.3` simply become one variable, the add overwrites the value that B3 returns, and the result is 3.

1. The resources are the target `x.2`, `x.1` from B1, and `x.3` from B2. `x.2` and `x.3` interfere: `x.2` is live where `x.3` is defined, because B3 reads it. `x.1` interferes with neither.
2. For the pair (`x.2`, `x.3`): $\mathrm{LiveOut}(B2) = \{x.2, x.3, n\}$, so the class of `x.2` meets $\mathrm{LIVE}$ of the operand from B2, and the target needs a copy. Just after the phi-function only `n` is live, so `x.3` needs no copy.
3. The closing step finds nothing. One copy goes in. The new target is `x.2_1`, and the class becomes $\{x.2\_1, x.1, x.3\}$, while `x.2` is now in no class.

The conventional program and the result of renaming the class to `x.1`:

```
B2:                                    B2:
  x.2_1 = phi [B1: x.1, B2: x.3]         x.2 = x.1
  x.2 = x.2_1                            x.1 = x.2 + 1
  x.3 = x.2 + 1                          t.1 = x.1 < n
  t.1 = x.3 < n                          br t.1 B2 B3
  br t.1 B2 B3                         B3:
                                         ret x.2
```

Cytron's translation would put the copy `x.2 = x.3` at the end of B2, where it also runs when the loop exits. Here the copy sits at the top of B2, so the exit edge leaves `x.2` alone. No edge was split.

**The swap.** In this loop the two phi-functions exchange `a` and `b` on each pass:

```
# params: n
B1:
  a.1 = 1
  b.1 = 2
  i.1 = 1
  jump B2
B2:
  a.2 = phi [B1: a.1, B2: b.2]
  b.2 = phi [B1: b.1, B2: a.2]
  i.2 = phi [B1: i.1, B2: i.3]
  i.3 = i.2 + 1
  t.1 = i.2 < n
  br t.1 B2 B3
B3:
  r.1 = a.2 * 10
  r.2 = r.1 + b.2
  ret r.2
```

For $n = 1, 2, 3$ it returns 12, 21, 12. Naive renaming gives 22 for $n = 2$.

1. First phi-function: `a.2` and `b.2` are both phi targets of B2, and both are live in B3, so they interfere. `a.2` is live out of B2, and `b.2` is live just after the phi-functions. Both needs hold, so both the target `a.2` and the operand `b.2` from B2 are copied.
2. Second phi-function: the same holds for `b.2` and `a.2`. Two more copies.
3. Third phi-function: `i.2` interferes with `i.3`, because `t.1` reads `i.2` after `i.3` is defined. But `i.2` is not live out of B2, and `i.3` is not live just after the phi-functions. So the pair is deferred, and line L12 copies the target `i.2`.

Method III adds 5 copies. Method I adds 9: one for each of the 6 operands and one for each of the 3 targets. After renaming, B2 is:

```
B2:
  a.2 = a.1
  b.2 = a.2_4
  i.2 = i.1
  i.1 = i.2 + 1
  t.1 = i.2 < n
  a.1 = b.2
  a.2_4 = a.2
  br t.1 B2 B3
```

The class of `b.1` was named `a.2_4`, the smallest of its names, and B1 now sets `a.2_4 = 2`. The swap is correct because the top copies save the two values in `a.2` and `b.2` before the bottom copies overwrite the loop variables. No temporary is needed, and no edge is split.

## Correctness

The full proof is in the proof file. It has three parts.

- **Renaming a conventional program is correct.** By induction over a run, every live name has its value in the variable of its class. A write to the variable of a class cannot destroy the value of another live name of the same class, because that name would be live just after the definition, so the two would interfere. On an edge, each phi target already has the value of its operand in the shared variable.
- **Copies keep the meaning.** An operand copy reads the operand at the same point the phi-function did. A target copy passes the value on before any old instruction of the block. Copies never make two old names interfere, because they only move a use earlier or a definition later past other copies.
- **The merged class is free of interference.** A new name for an operand lives only from its copy to the end of $L_i$, and a new name for a target only from the phi-functions to its copy. So it interferes only with names in $\mathrm{LIVE}(i)$. Two old classes that interfered are split by lines L8 to L12. A new name against a class that was not copied is handled by lines L13 and L14. Two new names never overlap.

## Complexity

Let $N$ be the size of the program, counting each phi operand, $V$ the number of names, $B$ the number of blocks and $F$ the number of phi-functions.

- **Method I** adds one copy for each phi operand and one for each phi-function, in $\Theta(N)$ time, with no analysis.
- **Liveness.** The implementation runs the round-robin [live variable analysis](/live-variable-analysis/) once per phi-function. With sets of names, this is $O(BNV)$ per run in the worst case, so $O(FBNV)$ in total. The [interference graph](/interference-graph/) adds $O(NV)$ per run.
- **Choosing copies.** A phi-function with $k$ resources checks $O(k^2)$ pairs, and each check compares two classes in $O(V^2)$ time. Summed over all phi-functions, $\sum k^2 \le N^2$.
- **Space.** The interference graph takes $O(V^2)$.

The paper builds liveness and the interference graph once, and updates both as each copy is added. That makes the method practical for large procedures.

## Properties

- **No edge splitting.** All copies go into existing blocks, so it also works on edges that cannot be split.
- **Method III never adds more copies than Method I.** It copies a subset of the same resources.
- **No copies on conventional input.** If the program is conventional and has no constant operands, no pair passes line L6, and Method III adds nothing.
- **Order dependent.** The copies chosen depend on the order of the phi-functions and on the deferred choice at line L11.
- **Copies in sequence are enough.** The copies of one edge go into different places, at the end of $L_i$ or at the top of $L_0$, and each writes a fresh name. So there is no parallel copy to order, and no swap cycle that needs a temporary.

## Variants and improvements

- **Method I.** Copy every resource. It is simple and always correct, and it leaves the removal of copies to a later coalescing pass.
- **Method II.** The paper's second method uses the interference graph to choose the copies, without the liveness tests of Method III.
- **Coalescing on classes.** The paper also removes copies after the translation by merging phi congruence classes that do not interfere. See the [register coalescing problem](/register-coalescing-problem/).
- **Boissinot et al. (2009).** They start from Method I with parallel copies, then coalesce with an interference test that uses the values of names and the dominance order of definitions, in place of a full interference graph.
- **Register allocation on SSA.** An [SSA-based register allocator](/ssa-based-register-allocation/) assigns registers before leaving SSA form. The phi-functions then become parallel copies between registers.

## When to use it

Use it when the program is in transformed SSA form after copy propagation or value numbering, and edge splitting is costly or not possible. Method I with a strong coalescer is the simplest correct choice. Method III gives few copies from the start, at the cost of liveness and an interference graph. If edges can be split freely, [splitting critical edges](/critical-edge-splitting/) and ordering the copies of each edge as a parallel copy is the simpler way.

## Pitfalls

- **The four cases alone are not enough.** They look only at pairs whose classes already interfere. A copy gives a resource a new name, and that new name can interfere with the class of a resource that was not copied. For example, a constant operand always gets a copy, and its new name is live at the end of its block together with whatever is live there. Lines L13 and L14 add copies until no new name is live where a class that was not copied is.
- **The wrong live set for the target.** The new target is live from the phi-functions to its copy. Every other phi target of the block and every earlier copy at the top is defined there. A dead phi target still writes its variable, so it counts too.
- **Uses in the terminator.** An operand copy goes before the terminator, so the names that the terminator reads are live where the new name is born. $\mathrm{LiveOut}(L_i)$ alone misses them.
- **Stale liveness.** Each copy changes liveness. Either compute it again, as the implementation does, or update it, as the paper does.
- **Constant operands.** A constant has no variable. It must become a copy into a new name before the class can be renamed.
- **Choosing the class variable.** If a class has a parameter, the parameter must be its variable, because the entry block already holds the value there.

## Implementations

## History

Cytron, Ferrante, Rosen, Wegman and Zadeck (1991) translated out of SSA form with copies at the ends of the predecessors. Briggs, Cooper, Harvey and Simpson (1998) showed that this fails after copy folding, with the lost copy and swap problems, and fixed it with liveness and ordered copies. Sreedhar, Ju, Gillies and Santhanam (SAS 1999) gave the terms conventional and transformed SSA and phi congruence class. They showed that renaming is enough for conventional SSA, and gave three methods that reach it with copies alone. Boissinot, Darte, Rastello, Dupont de Dinechin and Guillon (CGO 2009) revisited the approach. They made Method I with parallel copies the starting point and moved the work to a fast coalescer. The SSA book edited by Rastello and Bouchez Tichadou (2022) presents both.

## References
