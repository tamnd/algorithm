---
tag: EFB787
kind: algorithm
slug: steensgaard-analysis
name: Steensgaard's analysis
aliases:
- unification-based points-to analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: Flow-insensitive points-to analysis that unifies the targets of both sides of each assignment, with union-find, in almost linear time.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of pointer statements, α: the inverse Ackermann function}
  time: {worst: O((n + m) α(n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, online: true, flow_sensitive: false, context_sensitive: false}
history:
  year: 1996
  people: [Bjarne Steensgaard]
  note: Steensgaard presented the analysis at POPL 1996 as type inference with a non-standard type system, solved by union-find.
prereqs: [points-to-analysis, disjoint-set-forest, andersen-analysis]
see_also: [das-one-level-flow, andersen-analysis, union-find-amortized-bound, inverse-ackermann-function, unification-problem, hindley-milner-type-system, alias-analysis, field-sensitivity]
sources:
  - paper: doi:10.1145/237721.237727
    title: Bjarne Steensgaard, Points-to analysis in almost linear time, Proceedings of the 23rd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '96), 32 to 41, 1996
    locator: the non-standard type system for C, the equivalence class representatives with fast union-find, the conditional join with pending sets, the O(N α(N, N)) bound and the timings on C programs
  - paper: doi:10.1145/349299.349309
    title: Manuvir Das, Unification-based pointer analysis with directional assignments, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2000), 35 to 46
    locator: the comparison of the precision of Steensgaard's analysis, one-level flow and Andersen's analysis on C programs
  - paper: doi:10.1145/379605.379665
    title: Michael Hind, Pointer analysis, haven't we solved this problem yet?, Proceedings of the ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering (PASTE '01), 54 to 61, 2001
    locator: the place of unification-based analyses among the flow-insensitive analyses
  - paper: doi:10.1561/2500000014
    title: Yannis Smaragdakis and George Balatsouras, Pointer Analysis, Foundations and Trends in Programming Languages 2(1), 1 to 69, 2015
    locator: the comparison of unification-based and inclusion-based analyses
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19 (data structures for disjoint sets, union by rank with path compression)
---

Steensgaard's analysis solves the [points-to analysis](/points-to-analysis/) problem by unification. Where [Andersen's analysis](/andersen-analysis/) reads `p = q` as "the set of `p` contains the set of `q`", Steensgaard's analysis reads it as "`p` and `q` point into the same class of locations". The locations are kept in classes with union-find, each class points to at most one class, and every statement merges a few classes. One pass over the statements is enough, and the total time is almost linear in the size of the program. The sets are larger than Andersen's, and the proof file shows that they always contain them.

## In plain words

Think of the memory cells of a program as grouped into boxes, where every box has at most one arrow to another box. A pointer in a box can point to any cell in the box at the end of the arrow. When the program copies one pointer into another, the analysis makes them use the same target box: if the two boxes they point to are different, it pours one into the other. Pouring two boxes together also pours together the boxes that they point to. Each statement is read once, and each pour is quick with the union-find structure. The answer is safe, because every cell a real run can use ends up in the right box. It is coarse, because cells that were only copied in one direction still share a box.

## The problem

The input is a set of statements over $n$ variables in the forms `p = &a`, `p = q`, `p = *q` and `*p = q`; `p = alloc` at site $k$ is treated as `p = &h_k`. The output is a set $S(v)$ for each variable $v$ that meets the subset constraints of Andersen's analysis. Steensgaard's analysis computes more: a partition of the locations into classes and, for each class, at most one target class, such that:

- for `p = &a`, the class of $a$ is the target of the class of $p$;
- for `p = q`, if the class of $q$ has a target, the class of $p$ has the same target;
- for `p = *q` and `*p = q`, the same rule applies between $p$ and the target class of $q$, or between the target class of $p$ and $q$.

Then $S(v)$ is the set of variables in the target class of the class of $v$. Steensgaard wrote these rules as a type system: the type of a location is a reference to the class of its targets, and the analysis is type inference. The analysis in the terms of a data-flow framework:

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | partitions of the locations, with at most one target class per class |
| order | the partition is coarser and the target map follows it (bottom is precise) |
| join | merging classes (union-find) |
| bottom and top | all classes single, with no targets; one class that points to itself |
| boundary value | none |
| initial value | each location in its own class, with no target |
| transfer | monotone, not distributive |

## The algorithm

Each root of the union-find forest has a target $pt$, or none, and a list $pending$. A copy `p = q` when $q$ has no target yet must not invent one: that would merge the classes of $p$ and $q$ for nothing. So ASSIGN puts $p$ on the pending list of $q$, and the join happens only if $q$ gets a target later. Steensgaard calls this a conditional join. JOIN merges two classes and then their targets.

```pseudo id=main
STEENSGAARD(S)
L1  make a class for each variable, with no target and an empty pending list
L2  for each statement of S, in any order do
L3      p = &a: if class(p) has no target then SET-TARGET(class(p), class(a))
L4              else queue JOIN(pt(class(p)), class(a))
L5      p = q:  ASSIGN(class(p), class(q))
L6      p = *q: ASSIGN(class(p), DEREF(class(q)))
L7      *p = q: ASSIGN(DEREF(class(p)), class(q))
L8      run the queued operations until the queue is empty
L9  return S(v) = the variables in the class pt(class(v)), for each v

DEREF(c)
L10 if c has no target then SET-TARGET(c, a new class)
L11 return pt(c)

ASSIGN(x, y)                          the targets of x must include those of y
    if x = y then return
L12 if y has no target then add x to pending(y)
L13 else if x has no target then SET-TARGET(x, pt(y))
L14 else queue JOIN(pt(x), pt(y))

JOIN(c1, c2)
    if c1 = c2 then return
L15 c <- UNION(c1, c2)
L16 if neither had a target then pending(c) <- pending(c1) + pending(c2)
L17 else if one had no target then pt(c) <- the other target; queue ASSIGN(d, c) for each d pending on the one with no target
L18 else pt(c) <- pt(c1); queue JOIN(pt(c1), pt(c2))

SET-TARGET(c, t)
L19 pt(c) <- t
L20 queue ASSIGN(d, c) for each d in pending(c); pending(c) <- empty
```

The paper writes JOIN and the conditional join as recursive procedures. The implementation uses one queue of operations instead, so long chains of joins do not use the call stack. The union-find forest uses union by rank and path compression, as in a [disjoint-set forest](/disjoint-set-forest/).

## Example

The same program as on the [Andersen page](/andersen-analysis/):

```
entry:
  p = &a
  q = &b
  r = &p
  s = q
  *r = s
  t = *r
  ret 0
```

| statement | what happens | classes and targets after it |
|---|---|---|
| `p = &a` | $p$ had no target | $p \to \{a\}$ |
| `q = &b` | $q$ had no target | $q \to \{b\}$ |
| `r = &p` | $r$ had no target | $r \to \{p\}$ |
| `s = q` | ASSIGN: $q$ has a target, $s$ has none, so $s$ gets it | $s \to \{b\}$ |
| `*r = s` | DEREF$(r)$ is $\{p\}$; ASSIGN: both $\{p\}$ and $\{s\}$ have targets, so JOIN$(\{a\}, \{b\})$ | $\{a, b\}$ is one class; $p, q, s \to \{a, b\}$ |
| `t = *r` | DEREF$(r)$ is $\{p\}$; ASSIGN gives $t$ the target of $\{p\}$ | $t \to \{a, b\}$ |

The result is $S(p) = S(q) = S(s) = S(t) = \{a, b\}$ and $S(r) = \{p\}$. Andersen's analysis gives $\{b\}$ for $q$ and $s$: here the store `*r = s` merged $a$ and $b$, and since $q$ and $s$ already shared the class $\{b\}$, the merge reached them too.

The pending lists matter for statements in the other order. In `p = q` followed by `q = &b`, the first statement finds that $q$ has no target and puts $p$ on its pending list; the second gives $q$ the target $\{b\}$, and SET-TARGET then runs ASSIGN for $p$, so $S(p) = \{b\}$. A version without pending lists would make a placeholder target for $q$ at the first statement, which gives the same sets here, but in larger programs it merges classes that never needed to meet.

## Correctness

The full proof is in the proof file. Its steps:

1. **A target, once set, stays.** A class with a target keeps one when it merges, and the old and the new targets end up in one class, because the JOIN of line L18 runs before the end.
2. **A pending copy is not lost.** If ASSIGN$(x, y)$ runs and the class of $y$ has a target at the end, then the classes of $x$ and $y$ have the same target at the end. The pending entry moves with the class until the class gets a target, and then it becomes an ASSIGN again.
3. **The result is a solution.** With steps 1 and 2, each of the four statement forms meets its subset constraint. For a load `p = *q`, every $a$ in $S(q)$ is in the target class of $q$, which is the class that DEREF returned, and its target is the target of $p$.
4. **It contains Andersen's result.** Andersen's sets are the least solution, so they are inside every solution, and in particular inside $S$.

The sets have one more property: two sets are equal or disjoint, because each is a whole class.

## Complexity

**Proved.** There are at most $n + m$ classes, one per variable and one fresh class per load or store at most. Each statement queues $O(1)$ operations; each pending entry is added once and fired once; each JOIN that merges removes a class and queues at most one more JOIN. So there are $O(n + m)$ operations, each with $O(1)$ finds and unions. With union by rank and path compression the total time is $O((n + m)\,\alpha(n + m))$, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/), and the space is $O(n + m)$. This assumes pending lists that join in $O(1)$, such as linked lists; the implementation appends the shorter list to the longer, which costs $O(m \log m)$ for that part. Writing out all the sets $S(v)$ costs their total size, up to $\Theta(n^2)$, so a client should query the classes instead.

**Stated in the paper, not proved here.** Steensgaard states the bound $O(N \alpha(N, N))$ in the size $N$ of the program, for full C with structures and function pointers, and reports that the analysis of a C program of about 75,000 lines took about 27 seconds on an SGI Indigo2 workstation of the time.

**Measured, not proved.** In the seeded tests of the implementation, on 400 random programs of up to 30 statements, the sets of every variable contained Andersen's sets, and on 200 programs, three random orders of the statements each gave the same result.

## Properties

- **Online.** Each statement is read once, in any order, and the classes after a prefix of the statements are already correct for that prefix. The analysis can run while a compiler reads the program.
- **Sets are equal or disjoint.** Two pointers that may point to one common location have the same set. This is what makes the result so small to store: one target per class.
- **Bidirectional loss.** A copy `p = q` makes the targets of $q$ visible to $p$ and also the targets of $p$ visible to $q$.
- **Not recursive in the code.** The queue replaces the recursion of JOIN.
- **Result independent of the order.** The tests found no case where the order of the statements changed the result.

## Variants and improvements

- **One-level flow.** [Das's one-level flow](/das-one-level-flow/) keeps the subset direction for top-level copies, which are most of the copies in C, and unifies below that. Its precision is close to Andersen's at a cost close to Steensgaard's.
- **Fields.** Steensgaard's paper treats a structure as one location. Later work gives each field its own class; see [field sensitivity](/field-sensitivity/).
- **Context sensitivity.** Unification works well with [context sensitivity](/context-sensitivity/) by cloning: the classes of a function are copied at each call, as the type of a polymorphic function is copied at each use.
- **Andersen's analysis.** [Andersen's analysis](/andersen-analysis/) keeps the subset direction everywhere, for more precision and up to cubic time.
- **Type inference.** The same union-find method solves the [unification problem](/unification-problem/) for first-order terms and the type equations of the [Hindley-Milner type system](/hindley-milner-type-system/).

## When to use it

Use it when the program is very large or the analysis must run in a compile pass, and coarse sets are acceptable. It is a good first pass that tells which pointers can never alias, and it can split a program into parts that a more precise analysis then studies apart. When the clients need precise sets, such as call graphs through function pointers or alias queries for an optimizer, use Andersen's analysis or one-level flow.

## Pitfalls

- **Joining on copies from pointers with no target.** If `p = q` merges the targets of $p$ and $q$ even when $q$ has none yet, a placeholder target is made and later joined with real targets; the result is still sound but coarser. The pending lists avoid this.
- **Forgetting to join targets.** When two classes merge, their targets must merge too. Without line L18 the classes no longer have one target each, and the result misses facts.
- **Reading sets as precise.** Equal sets do not mean the two pointers were copied into each other. Unification merges along the whole chain of statements, as in the example, where $q$ gets $a$.
- **Recursion depth.** A program with a long chain of pointers to pointers gives a long chain of JOINs. A recursive JOIN can overflow the stack on such input.

## Implementations

## History

Bjarne Steensgaard presented the analysis at POPL 1996, as an answer to the cubic cost of Andersen's analysis. He described it as type inference with a non-standard type system for C and solved it with union-find, the method of type inference for ML-like languages. The conditional join with pending sets was his device to avoid merging classes for copies of pointers that never point anywhere. Das (2000) showed that keeping the direction at the top level gives most of Andersen's precision at almost the same cost. Unification remains the basis of fast analyses in compilers and of context-sensitive analyses by cloning.

## References
