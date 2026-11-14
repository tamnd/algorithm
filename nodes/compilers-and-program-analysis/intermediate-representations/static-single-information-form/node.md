---
tag: BHYZ1N
kind: definition
slug: static-single-information-form
name: Static single information form
aliases:
- SSI form
area: compilers-and-program-analysis/intermediate-representations
level: research
summary: An extension of SSA that also splits variables at branches with sigma-functions, so that facts learned from conditions get their own names.
prereqs: [static-single-assignment-form, phi-function, post-dominance]
see_also: [control-dependence, dominance-frontier, cytron-ssa-construction, sparse-conditional-constant-propagation, live-variable-analysis, interval-domain, ssa-cps-correspondence, program-dependence-graph]
sources:
  - url: "https://dspace.mit.edu/entities/publication/90fce509-5200-494b-9292-d34ffade899f"
    title: C. Scott Ananian, The static single information form, Master's thesis, MIT, Laboratory for Computer Science Technical Report MIT-LCS-TR-801, 1999
    locator: the definition of SSI form with sigma-functions, its construction, and its use for predicated and backward analyses in the FLEX Java compiler
  - paper: doi:10.48456/tr-660
    title: Jeremy Singer, Static program analysis based on virtual register renaming, University of Cambridge Computer Laboratory Technical Report UCAM-CL-TR-660, 2006
    locator: SSI as one member of a family of virtual register renaming schemes, its construction by alternating the placement of phi- and sigma-functions, and sparse liveness and type analyses on it
  - paper: doi:10.1145/2180887.2180898
    title: Benoit Boissinot, Philip Brisk, Alain Darte and Fabrice Rastello, SSI properties revisited, ACM Transactions on Embedded Computing Systems 11(S1), 2012, article 21
    locator: the comparison of the definitions of Ananian and Singer, the corrections to earlier claims, and the order of program points in which live ranges are intervals
  - paper: doi:10.1007/978-3-642-54807-9_2
    title: André L. C. Tavares, Benoit Boissinot, Fernando M. Q. Pereira and Fabrice Rastello, Parameterized construction of program representations for sparse dataflow analyses, Compiler Construction (CC 2014), LNCS, pages 18-39
    locator: the single information property for a given analysis, splits at iterated dominance and post-dominance frontiers, and the measured growth of programs
  - paper: doi:10.1145/349299.349342
    title: Rastislav Bodík, Rajiv Gupta and Vivek Sarkar, ABCD, eliminating array bounds checks on demand, Proceedings of the ACM SIGPLAN 2000 Conference on Programming Language Design and Implementation (PLDI 2000), pages 321-333
    locator: the extended SSA form with pi-assignments after conditional branches, on which the bounds-check analysis works
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the placement of phi-functions at iterated dominance frontiers, which SSI applies to definitions and, on the reverse graph, to uses
---

Static single information (SSI) form extends [static single assignment form](/static-single-assignment-form/). SSA gives a variable a new name where control flow joins, with a [phi-function](/phi-function/). SSI also gives it new names where control flow splits, with a *sigma-function* at the end of a branch block. After `if x > 0`, the then-branch reads `x1` and the else-branch reads `x2`. So the fact `x1 > 0` belongs to the name `x1` and holds wherever `x1` is used. Ananian (1999) introduced the form so that analyses that learn from branch conditions, and analyses that run backward, can be sparse: they keep one fact per name instead of one fact per variable at each program point. Singer (2006) gave a second definition and other constructions, and Boissinot, Brisk, Darte and Rastello (2012) showed that the two definitions differ.

## Definition

Let $G$ be a [control flow graph](/control-flow-graph/) with entry and exit nodes. A **sigma-function** at the end of a block $B$ with successors $S_1, \dots, S_k$ is written

$$(v_1, \dots, v_k) \leftarrow \sigma(v).$$

When control leaves $B$ for $S_i$, it copies $v$ into $v_i$. A sigma-function is the mirror image of a phi-function: a phi-function chooses one of several inputs by the incoming edge, and a sigma-function chooses one of several outputs by the outgoing edge.

A program with phi- and sigma-functions is in **SSI form** if, for every variable $v$ of the original program:

1. **Single assignment.** Each name of $v$ has exactly one definition, by an instruction, a phi-function or a sigma-function, and the definition [dominates](/dominator-tree/) every use of the name.
2. **Joins.** If two paths that start at two different definitions of $v$ first meet at a node $Z$, and $v$ is live at $Z$, then $Z$ has a phi-function for $v$.
3. **Splits.** If two paths that start at a node $B$ and end at two different uses of $v$ leave $B$ by different edges, and $v$ is live on both edges, then $B$ ends with a sigma-function for $v$.

Condition 3 is condition 2 on the reverse graph, with uses in place of definitions. Cytron et al. place phi-functions at the iterated [dominance frontier](/dominance-frontier/) of the definitions. By the same argument on the reverse graph, sigma-functions belong at the iterated dominance frontier of the uses in the reverse graph, that is, at the blocks on which a use is [control dependent](/control-dependence/), with [post-dominance](/post-dominance/) in place of dominance. A sigma-function is a new definition and a phi-function is a new use, so a construction places both kinds until no more are needed. Ananian's and Singer's definitions differ in details of conditions 2 and 3; this page states the common core.

**The single information property.** The point of the form is the following. Take a dataflow analysis that attaches a fact to each variable at each program point. SSI form has this property for the analysis if, for each name, the fact is the same at every point of the name's live range. Facts change only at definitions, at joins (where SSA already puts a new name) and at branches (where SSI puts a new name), so in SSI form one fact per name is enough. Tavares, Boissinot, Pereira and Rastello (2014) define the property for a given analysis and split only at the points that the analysis needs.

## Examples and non-examples

**A condition becomes a fact about a name.**

```
x0 = read()
if x0 > 0:              (x1, x2) = σ(x0) at the end of this block
    y1 = 100 / x1
else:
    y2 = 0 - x2
y3 = φ(y1, y2)
```

A range analysis sets $x_1 \in [1, \infty)$ and $x_2 \in (-\infty, 0]$. Each fact holds wherever its name is used, so the division by `x1` is safe without a test at the division. In SSA form both branches read `x0`, and the analysis would have to keep a different range for `x0` in each branch.

**Backward analysis.** A backward analysis such as [liveness](/live-variable-analysis/) combines facts at branches, where SSI form puts new names, as a forward analysis combines them at joins. Singer computes liveness and other backward analyses sparsely on the form.

**Intervals.** Boissinot et al. (2012) show that the program points of a program in SSI form can be ordered so that the live range of every name is an interval of that order. This holds for both definitions of SSI.

**Non-examples.**

- The SSA form of the program above, without the sigma-function, is not in SSI form: two uses of `x0` lie on different edges out of the branch block, and condition 3 fails.
- A program with `(x1, x2) = σ(x0)` but where the else-branch still reads `x0` is not in SSI form: the sigma-function is there, but the use is not renamed, and `x0` is now read where `x2` should be.
- The extended SSA form (e-SSA) of Bodík, Gupta and Sarkar (2000), with pi-assignments only after branches that test a variable, is not full SSI form. It splits a variable only at the branches that teach something about it, which is what their bounds-check analysis needs. It is a partial form in the sense of Tavares et al.

## Related definitions

- **[Static single assignment form](/static-single-assignment-form/).** SSI form is SSA form with sigma-functions added. Dropping the sigma-functions and renaming each $v_i$ back to $v$ gives SSA form again.
- **[Control dependence](/control-dependence/).** The blocks that need a sigma-function for $v$ are the branches on which the uses of $v$ are control dependent, iterated with the new definitions. The [program dependence graph](/program-dependence-graph/) records the same relation as edges.
- **Extended SSA and pi-nodes.** Bodík, Gupta and Sarkar insert $v' \leftarrow \pi(v)$ on each outgoing edge of a branch that tests $v$, which is a sigma-function restricted to those branches.
- **[Sparse conditional constant propagation](/sparse-conditional-constant-propagation/)** and range analysis over the [interval domain](/interval-domain/) are forward analyses that gain from the extra names. Constant propagation gains when a branch tests a variable for equality.
- **[Correspondence of SSA and functional programs](/ssa-cps-correspondence/).** In the functional view, where each block is a local function, a sigma-function makes $v$ a parameter of each successor block, so that each block gets its own name for it.

## References
