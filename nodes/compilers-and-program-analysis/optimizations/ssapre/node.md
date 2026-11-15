---
tag: H6X0KK
kind: algorithm
slug: ssapre
name: SSAPRE
aliases:
- SSA-based partial redundancy elimination
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Performs PRE on SSA form one expression at a time by building a sparse SSA graph of the expression's occurrences.
solves: [partial-redundancy-elimination]
model: word-ram
complexity:
  vars: {n: the number of instructions and blocks, d: the total size of the dominance frontiers, m: the number of distinct expressions, v: the number of variables}
  time: {worst: O((m + v)(n + d))}
  space: {extra: O(n v + d)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [partial-redundancy-elimination, static-single-assignment-form, dominance-frontier, dominator-tree]
see_also: [lazy-code-motion, global-value-numbering, phi-function, cytron-ssa-construction, out-of-ssa-translation, critical-edge-splitting, very-busy-expressions, strength-reduction]
sources:
  - paper: doi:10.1145/258915.258940
    title: "Fred Chow, Sun Chan, Robert Kennedy, Shin-Ming Liu, Raymond Lo and Peng Tu, A new algorithm for partial redundancy elimination based on SSA form, Proceedings of the ACM SIGPLAN 1997 Conference on Programming Language Design and Implementation (PLDI 1997), 273-286"
    locator: the whole paper (the six steps Φ-Insertion, Rename, DownSafety, WillBeAvail, Finalize and CodeMotion)
  - paper: doi:10.1145/319301.319348
    title: "Robert Kennedy, Sun Chan, Shin-Ming Liu, Raymond Lo, Peng Tu and Fred Chow, Partial redundancy elimination in SSA form, ACM Transactions on Programming Languages and Systems 21(3), 1999, 627-676"
    locator: the whole paper (the full algorithm, the proofs of correctness and optimality, and the extensions to loads, stores and strength reduction)
  - paper: doi:10.1145/183432.183443
    title: "Jens Knoop, Oliver Rüthing and Bernhard Steffen, Optimal code motion: theory and practice, ACM Transactions on Programming Languages and Systems 16(4), 1994, 1117-1155"
    locator: the definitions of down-safety, computational optimality and lifetime optimality that SSAPRE reaches
---

SSAPRE is an algorithm for [partial redundancy elimination](/partial-redundancy-elimination/) on [static single assignment form](/static-single-assignment-form/), by Chow, Chan, Kennedy, Liu, Lo and Tu. It handles one expression at a time. For each expression it builds a small graph of the places that compute the expression and of the joins where different values of it meet, and it decides where to compute it on this graph alone. It needs no bit vectors and no dataflow over the whole flow graph, and it gets the same placement as [lazy code motion](/lazy-code-motion/).

## In plain words

Take one expression, such as `a + b`. Mark every place that computes it. At each join where two paths can bring different values of it, put a marker that says "the value here comes from one of the paths".

Now walk the program from the top, branch by branch, and give each value of `a + b` a number. Two places get the same number when `a` and `b` did not change between them. The second of them is then redundant.

At each join marker, check two things. Will every path from here compute the expression again before `a` or `b` changes? And can the value be made ready on every path into the join? If both hold and the value is needed, compute it on the paths that lack it, just before the join, and let the later places read a temporary.

## The problem

The input is a procedure of the toy IR with const, copy and op instructions and any control flow. An expression is the text `a op b` of an op instruction. The output is a program that gives the same result or trap on every input that ends, and in which no path from the entry to a `ret` evaluates an expression more often than before. Inserted computations must be at *down-safe* points: every path from there computes the expression again before an operand changes. Among such programs, SSAPRE wants the fewest evaluations on every path.

The paper works on a program that is already in SSA form. The toy IR lets a variable be assigned more than once, so this implementation computes the SSA versions of the variables on the side and does not rename the program.

## The algorithm

A *real occurrence* of $e$ is an instruction `x = e`. A *Φ* for $e$ sits at the top of a join block. It is like a [φ-function](/phi-function/) for a temporary $h$ that would hold the value of $e$. Each Φ has one *operand* for each predecessor. An operand is ⊥ if no value of $e$ with the right operand versions reaches the end of that predecessor. It *has a real use* if the value comes from a real occurrence and not from another Φ.

```pseudo id=main
SSAPRE(P)
L1  remove unreachable blocks, give the entry no predecessor, and split every critical edge
L2  build the dominator tree and the dominance frontiers, and give each variable its SSA versions
L3  for each expression e = a op b, one at a time
L4      Φ-Insertion: put a Φ for e at DF+(blocks that compute e) and at each block with a φ for a or b
L5      Rename: walk the dominator tree with a stack of occurrences; an occurrence whose operand versions match the top takes its version, else it gets a new one; a Φ whose version is killed or reaches a ret before a real use is not down-safe
L6      DownSafety: if a Φ f is not down-safe, each Φ g that gives f an operand with no real use is not down-safe
L7      can_be_avail: reset each Φ that is not down-safe and has a ⊥ operand, and pass the reset to Φs that are not down-safe and use it with no real use
L8      later: start from can_be_avail; reset each Φ with an operand that has a real use, and pass the reset to every Φ that uses it
L9      will_be_avail(Φ) <- can_be_avail(Φ) and not later(Φ)
L10     Finalize: a real occurrence reloads t if its version comes from an earlier real occurrence, which then saves t, or from a will_be_avail Φ; mark each operand of a will_be_avail Φ that is ⊥, or has no real use and comes from a Φ that is not will_be_avail
L11     CodeMotion: insert t = e at the end of the predecessor of each marked operand, turn each save into t = e; x = t, and each reload into x = t
L12 return P
```

- **Φ-Insertion (line L4).** A join needs a Φ where values from different occurrences can meet, which is the iterated [dominance frontier](/dominance-frontier/) of the occurrences, as in [SSA construction](/cytron-ssa-construction/). A φ for an operand also changes the value of $e$, so its block gets a Φ too.
- **Rename (line L5).** The walk keeps a stack of occurrences, like the renaming step of SSA construction. Two occurrences get the same version exactly when the versions of `a` and `b` agree. The walk also notes each Φ whose value dies or reaches a `ret` before a real occurrence uses it.
- **DownSafety (line L6).** A Φ that only feeds another Φ, with no real occurrence in between, is down-safe only if that Φ is. This is the [very busy expressions](/very-busy-expressions/) analysis on the sparse graph.
- **WillBeAvail (lines L7 to L9).** can_be_avail says the value can be made ready at the Φ with safe insertions. later says that every insertion for the Φ could also go further down, because no operand has a real value yet. A Φ that is will_be_avail is a place where the value will be ready after the insertions.
- **Finalize and CodeMotion (lines L10 and L11).** The paper gives the temporary SSA versions and keeps the Φs that are will_be_avail as real φs. Here the temporary is one plain name `pre.k`, which is what [out-of-SSA translation](/out-of-ssa-translation/) would give.

## Example

The parameters are `a`, `b`, `c` and `n`.

```
B0:
  i = 0
  br c B1 B2
B1:
  x = a + b
  jump B3
B2:
  x = 0
  jump B3
B3:
  y = a + b
  i = i + 1
  d = i < n
  br d B3 B4
B4:
  ret y
```

The edge from `B3` to itself is critical, so line L1 adds a block `B3_B3` that only jumps to `B3`. Each expression gets one Φ, at `B3`. For `a + b`, `B3` is the dominance frontier of `B1` and of `B3`. For `i + 1` and `i < n`, `B3` has a φ for `i`. In the notation of the paper, the factored graph of `a + b` is `h1 = a + b` in `B1`, then `h2 = Φ(h1, ⊥, h2)` at the top of `B3` for the predecessors `B1`, `B2` and `B3_B3`, then the occurrence in `B3` with version `h2`.

| Φ at `B3` for | operands from `B1`, `B2`, `B3_B3` | down-safe | can_be_avail | later | will_be_avail |
|---|---|---|---|---|---|
| `a + b` | real use, ⊥, real use | yes | yes | no | yes |
| `i + 1` | ⊥, ⊥, ⊥ | yes | yes | yes | no |
| `i < n` | ⊥, ⊥, real use | no | no | no | no |

For `a + b`, the Φ is down-safe, because `B3` computes it first thing. Its operand from `B2` is ⊥, so line L10 marks it, and the occurrence in `B1` saves the temporary. For `i + 1`, the Φ is down-safe too, but no operand has a value yet, so it stays later: moving the addition would only make a temporary. For `i < n`, `i` changes before the comparison, so the Φ is not down-safe. The result is:

```
B1:
  pre.0 = a + b
  x = pre.0
  jump B3
B2:
  x = 0
  pre.0 = a + b
  jump B3
B3:
  y = pre.0
  i = i + 1
  d = i < n
  br d B3_B3 B4
B3_B3:
  jump B3
B4:
  ret y
```

With $c = 1$ and $n = 3$ the loop runs three times, and `a + b` runs once instead of four times. With $c = 0$ it runs once instead of three times.

## Correctness

The proof file has the full proof. It fixes one expression and uses one property of SSA form: the version of a variable at a point names the definition that is last on every path to the point.

- **Rename finds equal values.** If an occurrence gets the version of an earlier one, the earlier one dominates it, and no path between them changes `a` or `b`.
- **Down-safety.** A Φ that is still down-safe after line L6 is down-safe in the program. Every Φ with a marked operand is down-safe. The proof follows a chain of Φs that are not down-safe, can_be_avail and later back toward the entry, and shows that such a chain cannot exist.
- **Same outcome.** At each reload and at each will_be_avail Φ, the temporary was computed after the last change of `a` and `b`. An inserted computation is down-safe, so if it traps, the old program would trap on the same values a little later.
- **Never more evaluations.** Each insertion is matched with the first real occurrence after it on the path. That occurrence becomes a reload, and no two insertions share it.

Kennedy and colleagues also prove computational optimality: no safe placement does better on any path. The tests check it against busy code motion on every path of random acyclic programs.

## Complexity

In this implementation, line L2 costs $O(n + d)$ for the dominance frontiers and $O(v (n + d))$ for the φs and the versions of the variables. For each expression, line L4 costs $O(n + d)$ and the walk of line L5 costs $O(n)$. Lines L6 to L10 visit each Φ and each operand a fixed number of times, so they are linear in the size of the sparse graph, which is $O(n)$. The total is $O((m + v)(n + d))$.

Production versions find the occurrences of all expressions in one pass over the program and do the rest on the sparse graphs. Then the cost of the later steps for an expression depends on its own occurrences and Φs, not on the size of the procedure. Lazy code motion, in contrast, iterates bit vectors over every node of the flow graph.

## Properties

- **Safe.** Insertions are only at down-safe points.
- **Never more evaluations.** No path evaluates an expression more often than before.
- **Computationally optimal.** Proved by Kennedy and colleagues, and checked by the tests against busy code motion.
- **Sparse.** Each expression is handled on a graph of its own occurrences and Φs.
- **Lexical.** It works on the text `a op b` with the original variable names. Two different names with equal values are not seen as equal.
- **One expression at a time.** Expressions do not interact, so a compiler can also restrict the work to the expressions it cares about.

## Variants and improvements

- **Loads and stores.** The same steps treat a load as an expression whose operand is a memory location, with stores and calls as kills. The dual problem sinks stores. Together they give register promotion of memory values.
- **Strength reduction.** If an update such as `i = i + 1` does not count as a kill of `i * c` but as a change that can be repaired, the same framework does [strength reduction](/strength-reduction/).
- **Value-based PRE.** Working on the classes of [global value numbering](/global-value-numbering/) instead of on lexical expressions finds redundancy between different names.
- **Speculative PRE.** With profile data, the down-safety rule can be relaxed on cold paths for expressions that cannot trap.

## When to use it

Use SSAPRE in a compiler that keeps SSA form through its global optimizations. It needs no translation back to lexical expressions and no bit vectors, and the work for one expression stays near its occurrences. It also fits passes that only want PRE for a few expressions, such as loads in hot loops. In a compiler without SSA form, [lazy code motion](/lazy-code-motion/) is the simpler choice. Use value-based PRE if much of the redundancy is hidden by copies.

## Pitfalls

- **Critical edges.** Insertions go at the end of the predecessor of a Φ block. That place is safe only if the predecessor has one successor, so the critical edges must be split first.
- **Kills before a real use.** Rename must mark a Φ as not down-safe when the operands change before the next real occurrence, as for `i < n` in the example, and not only when the value reaches a `ret`. Missing this mark puts computations on paths that never needed them.
- **Loops that may not run.** In a `while` loop whose test comes first, the Φ at the loop header is not down-safe for an expression in the body, so SSAPRE leaves it in the loop, like every safe PRE.
- **Runs that never end.** Down-safety looks at paths that reach a `ret`. A run that passes an insertion and then loops forever can trap in the new program and not in the old one.
- **The temporary in SSA form.** The paper's temporary has SSA versions and new φs at the will_be_avail Φs. These φs must go through out-of-SSA translation like any other, and the copies `x = t` need [copy propagation](/copy-propagation/) afterwards.

## Implementations

## History

Chow, Chan, Kennedy, Liu, Lo and Tu presented SSAPRE at PLDI 1997. Earlier PRE methods, from Morel and Renvoise in 1979 to the lazy code motion of Knoop, Rüthing and Steffen in 1992, worked with bit vectors over the whole flow graph. SSAPRE showed that the same safe and optimal placement can be computed on SSA form, one expression at a time, by steps that look like SSA construction. Kennedy and the same coauthors gave the full algorithm, the proofs and the extensions to memory operations and strength reduction in TOPLAS in 1999.

## References
