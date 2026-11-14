---
tag: ZKS818
kind: problem
slug: alias-analysis
name: Alias analysis
aliases:
- may-alias analysis
- must-alias analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: Decide whether two memory references in a program may, or must, refer to the same location.
prereqs: [three-address-code, control-flow-graph]
see_also: [points-to-analysis, type-based-alias-analysis, may-alias-undecidability, flow-insensitive-alias-np-hardness, mod-ref-analysis, andersen-analysis, steensgaard-analysis, shape-analysis]
sources:
  - paper: "William Landi, Undecidability of static analysis, ACM Letters on Programming Languages and Systems 1(4), 323 to 337 (1992)"
    locator: the main theorems (precise may-alias is not recursive and must-alias is not recursively enumerable)
  - paper: doi:10.1145/186025.186041
    title: G. Ramalingam, The undecidability of aliasing, ACM Transactions on Programming Languages and Systems 16(5), 1467 to 1471 (1994)
    locator: whole paper
  - paper: doi:10.1145/239912.239913
    title: Susan Horwitz, Precise flow-insensitive may-alias analysis is NP-hard, ACM Transactions on Programming Languages and Systems 19(1), 1 to 6 (1997)
    locator: whole paper
  - paper: doi:10.1145/1353445.1353447
    title: Noam Rinetzky, G. Ramalingam, Mooly Sagiv and Eran Yahav, On the complexity of partially-flow-sensitive alias analysis, ACM Transactions on Programming Languages and Systems 30(3), Article 13 (2008)
    locator: the summary of earlier results (flow-sensitive may-alias without dynamic allocation is PSPACE-complete)
  - paper: doi:10.1145/379605.379665
    title: Michael Hind, Pointer analysis, haven't we solved this problem yet?, Proceedings of the ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering (PASTE '01), 54 to 61, 2001
    locator: the relation of alias pairs and points-to sets, and the dimensions of precision
  - paper: doi:10.1145/277650.277670
    title: Amer Diwan, Kathryn S. McKinley and J. Eliot B. Moss, Type-based alias analysis, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 1998), 106 to 117
    locator: alias analysis from the type rules of a type-safe language
---

Alias analysis decides whether two memory references in a program can name the same location. A *may-alias* answer says that they can in some execution, and a *must-alias* answer says that they do in every execution that reaches the point. Compilers need both: a store through `*p` blocks the motion of a load from `*q` only if the two may alias, and a load can take the value of an earlier store only if the two must alias. The precise question is [undecidable](/may-alias-undecidability/) once the program can build data structures of any size, so analyses answer it approximately, and nearly all of them work from a [points-to analysis](/points-to-analysis/) or from the [type rules](/type-based-alias-analysis/) of the language.

## In plain words

Two names in a program can stand for the same box in memory. A pointer can point to a variable, or two pointers can point to the same object. If the compiler writes into one name and then reads from the other, the order matters. Alias analysis tells the compiler when two names might share a box, and when they surely share it. If they might, the compiler must keep the order of the read and the write. If they surely do not, it is free to move them. If they surely do, it can reuse the value it just wrote. A safe "might" answer can be too cautious, but it must never say "no" when the answer is "yes".

## Definition

**Input.** A program in the toy IR with the pointer instructions `p = &x`, `x = *p`, `*p = a` and `p = alloc`, a program point $x$, and two memory references $e_1$ and $e_2$. A memory reference is a variable `a` or a dereference `*p`. In a state $\sigma$, `a` names the location $a$, and `*p` names the location whose address $p$ holds; it names nothing if $p$ holds no address.

**The two questions.** $e_1$ and $e_2$ *alias* in $\sigma$ when both name the same location.

- *May-alias:* is there an executable path from the entry to $x$ that ends in a state where $e_1$ and $e_2$ alias?
- *Must-alias:* do $e_1$ and $e_2$ alias at the end of every executable path from the entry to $x$?

A sound may-alias analysis answers "no alias" only when the true answer is no. A sound must-alias analysis answers "must alias" only when the true answer is yes. Many compilers return one of three answers, no alias, may alias and must alias; LLVM adds partial alias for references that overlap in part.

**From points-to sets.** Let $G_x$ be the may points-to graph at $x$ ([points-to analysis](/points-to-analysis/)) and $M_x$ a must points-to graph, where $(p, a) \in M_x$ means that $p$ holds the address of the one concrete location $a$ on every path to $x$. Then

- `*p` and `*q` may alias if $G_x(p) \cap G_x(q) \ne \emptyset$, and `*p` and `a` may alias if $a \in G_x(p)$;
- `*p` and `*q` must alias if $M_x(p) = M_x(q) = \{a\}$ for some $a$, and `*p` and `a` must alias if $M_x(p) = \{a\}$.

A heap location $h_k$ stands for all cells made at one `alloc` site, so it never appears in $M_x$: two pointers into the same site may point to different cells.

**The lattices.** Both analyses below use the order of abstract interpretation in the direction of Cousot, where lower is more precise and the answer is the least fixed point. Turning the order upside down maps them onto the meet convention of Kildall, which some data-flow texts use.

| item | may-alias (from may points-to) | must-alias (from must points-to) |
|---|---|---|
| direction | forward | forward |
| may or must | may | must |
| domain | subsets of $Loc \times Loc$ | subsets of $V \times V$ in which each variable has at most one target, plus a bottom element |
| order | $\subseteq$ | $\supseteq$: more must facts is lower and more precise |
| join | union | intersection |
| bottom and top | $\emptyset$ and $Loc \times Loc$ | bottom is "not reached", top is $\emptyset$ (no must fact) |
| boundary value | $IN[entry] = \emptyset$ | $IN[entry] = \emptyset$ |
| initial value | $\emptyset$ | bottom |
| transfer | as in [points-to analysis](/points-to-analysis/); monotone, not distributive | below; monotone, not distributive |
| height | $N^2$ for $N$ locations | at most $|V| + 2$ |

**Must transfer functions.** "Kill $p$" removes the fact of $p$. The must analysis reads the may graph $G$ at the same point, which is computed first.

| instruction | output |
|---|---|
| `p = &a` | kill $p$, add $(p, a)$ |
| `p = alloc` | kill $p$ (a heap location is not one concrete location) |
| `p = q` | kill $p$, add $(p, a)$ if $(q, a)$ is a fact |
| `p = *q` | kill $p$, add $(p, b)$ if $(q, a)$ and $(a, b)$ are facts |
| `*p = q` with the fact $(p, a)$ | kill $a$, add $(a, b)$ if $(q, b)$ is a fact |
| `*p = q` otherwise | kill every $a \in G(p)$ |
| any other instruction that defines $x$ | kill $x$ |

**Equations.** $IN[B] = \bigsqcup_{P \in pred(B)} OUT[P]$ and $OUT[B] = f_B(IN[B])$, where $\bigsqcup$ is union for may and intersection for must.

**The ideal answer** is the join over all paths, $MOP(x) = \bigsqcup_\pi f_\pi(IN[entry])$ over the paths $\pi$ from the entry to $x$. **The computed answer** is the least fixed point in the order of the table, by a [worklist](/worklist-dataflow-algorithm/) that starts from the initial values. The functions are monotone, so $MOP(x) \sqsubseteq LFP(x)$: the may graph has at least the pairs of MOP, and the must graph has at most the facts of MOP.

**Soundness.** The concrete semantics is the set of states that reach each point along the executable paths. Every state that reaches $x$ along a path $\pi$ satisfies the facts of $f_\pi$: its address pairs are in the may graph, and every must fact holds in it. This follows by induction along $\pi$, one instruction at a time, as on the [points-to analysis](/points-to-analysis/) page. For the must store, the fact $(p, a)$ says that the store writes exactly $a$; otherwise it may write any $a \in G(p)$, and every such fact is killed. Every real path is a path of the control flow graph, so a "no alias" from the may graph and a "must alias" from the must graph are both correct.

**Precision.** In this program the two references `*p` and `*q` at block `join` may alias, along the path through `then`, but they do not must alias:

```
entry:
  p = alloc
  br c then else
then:
  q = p
  jump join
else:
  q = alloc
  jump join
join:
  *p = 1
  x = *q
  ret x
```

The may graph at `join` has $G(p) = \{h_1\}$ and $G(q) = \{h_1, h_2\}$, which meet, so the answer is "may alias". The must graph has no fact for `p` or `q`, because both point into the heap. Even if both branches did `q = p`, the must analysis above would not say "must alias", because $h_1$ is a heap location; an analysis that also tracks equalities of pointer values, such as `q = p`, recovers that answer. This is the usual price of reasoning through locations only.

**Cost.** The may graph costs what [points-to analysis](/points-to-analysis/) costs. The must graph has height at most $|V| + 2$ at each point, so the worklist applies $O((n + m)|V|)$ transfer functions for $n$ instructions and $m$ edges. A query then takes one set intersection.

## Variants

- **May and must.** Most analyses answer may-alias only; a must answer is a by-product of must points-to facts or of value numbering of pointers.
- **Flow and context.** A flow-insensitive analysis has one answer for the whole program ([flow sensitivity](/flow-sensitivity/)); a context-insensitive one merges the facts of all callers of a procedure ([context sensitivity](/context-sensitivity/)).
- **Representation.** Alias pairs list the pairs of access paths that may alias, often limited to paths of length $k$. Points-to graphs list targets. Equivalence classes, as in [Steensgaard's analysis](/steensgaard-analysis/), put references that may alias into one class. The points-to form is the most common, since it is compact and gives the other two.
- **Type-based.** In a type-safe language, two references of unrelated types cannot alias ([type-based alias analysis](/type-based-alias-analysis/)). C has the same rule for most types, and compilers use it unless a flag turns it off.
- **Programmer assertions.** C99 `restrict` and the rules on Fortran dummy arguments let the compiler assume that some references do not alias.
- **Fields and arrays.** References to different fields of one object never alias ([field sensitivity](/field-sensitivity/)); references to array elements need dependence tests on the index expressions.
- **Heap structure.** [Shape analysis](/shape-analysis/) and [separation logic](/separation-logic/) tell apart the cells of one allocation site when they form lists or trees.

## Examples

**Through one variable.** After `p = &a`, `*p` and `a` must alias, and after `q = &b` with $b \ne a$, `*p` and `*q` do not alias. A store `*q = 1` then does not change `a`, so a later load of `a` can reuse an earlier value.

**Two parameters.** In C, a function `f(int *x, int *y)` can be called with `f(&v, &v)`, so `*x` and `*y` may alias inside `f`. An intraprocedural analysis must assume this, and an interprocedural one looks at the call sites. With `int *restrict x`, the programmer promises that they do not.

**Types.** In Java, a reference of a class `A` and a reference of an unrelated class `B` never name the same object, whatever the flow; in C, an `int` lvalue and a `float` lvalue may be assumed apart under the strict aliasing rule.

## Known algorithms

- **From points-to sets:** [Andersen's analysis](/andersen-analysis/), [Steensgaard's analysis](/steensgaard-analysis/), [Das's one-level flow](/das-one-level-flow/), and their faster solvers; [demand-driven points-to analysis](/demand-driven-points-to/) for one query at a time.
- **From types:** [type-based alias analysis](/type-based-alias-analysis/), with one union-find pass over the assignments and then a table over pairs of types.
- **From local reasoning:** distinct local variables whose address is not taken never alias; a base pointer plus two different constant offsets never alias. Compilers chain such cheap tests before the costly ones. LLVM, for example, asks a list of alias analyses in turn and keeps the first definite answer.
- **From heap structure:** [shape analysis](/shape-analysis/) and [separation logic](/separation-logic/).

## Bounds

- **Undecidable.** With dynamic allocation and recursive data structures, precise may-alias is not decidable and precise must-alias is not recursively enumerable, even when every path is executable (Landi 1992, Ramalingam 1994; [undecidability of may-alias analysis](/may-alias-undecidability/)).
- **PSPACE-complete without allocation.** If the program cannot allocate, precise flow-sensitive may-alias is decidable and PSPACE-complete (as summarized by Rinetzky et al. 2008).
- **NP-hard without order.** Precise flow-insensitive may-alias is NP-hard, even with no dynamic memory (Horwitz 1997; [NP-hardness of precise flow-insensitive alias analysis](/flow-insensitive-alias-np-hardness/)).
- **Polynomial approximations.** Sound answers come in $O(n^3)$ time from Andersen's analysis, in almost linear time from Steensgaard's analysis, and from the types alone, in time polynomial in the number of types, by type-based analysis.

## Reductions

**Alias and points-to are the same question.** `*p` may alias `a` exactly when $p$ may point to $a$, and `*p` may alias `*q` exactly when $p$ and $q$ may point to a common location. So a points-to analysis gives an alias analysis, and an alias oracle for the pairs (`*p`, `a`) gives the points-to sets.

**PCP reduces to may-alias.** A program that grows a chain of cells and walks two pointers down it by the two halves of a Post correspondence instance makes the pointers alias exactly when the instance has a solution ([undecidability of may-alias analysis](/may-alias-undecidability/)).

**Hamiltonian path reduces to flow-insensitive may-alias.** One statement per edge and one long dereference chain make a pointer reach the end node exactly when a Hamiltonian path exists ([NP-hardness of precise flow-insensitive alias analysis](/flow-insensitive-alias-np-hardness/)).

## Applications

- **Reordering.** [Instruction scheduling](/instruction-scheduling-problem/) may swap a load and a store only if they do not alias.
- **Redundancy.** [Common subexpression elimination](/common-subexpression-elimination/) and [partial redundancy elimination](/partial-redundancy-elimination/) reuse a loaded value only if no store between may alias it; store-to-load forwarding needs a must answer.
- **Code motion.** [Loop-invariant code motion](/loop-invariant-code-motion/) hoists a load only if no store in the loop may alias it.
- **Dead stores.** [Dead code elimination](/dead-code-elimination/) removes a store that a later store must overwrite before any load that may alias reads it.
- **Registers and aggregates.** [Scalar replacement of aggregates](/scalar-replacement-of-aggregates/) keeps fields in registers when no other reference may alias them.
- **Side effects.** [Mod-ref analysis](/mod-ref-analysis/) finds the locations that a call may read or write, from the alias facts of its body.

## References
