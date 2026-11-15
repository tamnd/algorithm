---
tag: N2VDR9
kind: algorithm
slug: slg-resolution
name: SLG resolution
aliases:
- tabled resolution
- tabling
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Goal-directed evaluation that keeps a table of answers for each call and delays negative literals it cannot decide yet. It terminates on finite ground programs and computes the well-founded semantics.
model: word-ram
complexity:
  vars: {s: "the size of the part of the program that the query reaches, the number of rules plus the number of body literals"}
  time: {worst: O(s³)}
  space: {extra: O(s)}
properties: {deterministic: true}
history:
  year: 1996
  people: [Weidong Chen, David S. Warren]
  note: Chen and Warren gave the full definition of SLG resolution, with delaying, simplification and completion, and proved it sound and complete for the well-founded semantics. It became the basis of the XSB system.
prereqs: [well-founded-semantics, sldnf-resolution, negation-as-failure, memoization]
see_also: [alternating-fixpoint, sld-resolution, tarjan-scc, datalog-evaluation, magic-sets, warren-abstract-machine, backward-chaining, stable-model-semantics]
sources:
  - paper: doi:10.1145/227595.227597
    title: Weidong Chen and David S. Warren, Tabled evaluation with delaying for general logic programs, Journal of the ACM 43(1), 20 to 74 (1996)
    locator: the SLG transformations (resolution, answer return, negative return, delaying, simplification, completion) and the proofs of soundness, completeness and termination for the well-founded semantics
  - paper: doi:10.1007/3-540-16492-8_66
    title: Hisao Tamaki and Taisuke Sato, OLD resolution with tabulation, Third International Conference on Logic Programming, Lecture Notes in Computer Science 225, Springer, 84 to 98 (1986)
    locator: tables of calls and answers for definite programs
  - paper: doi:10.1145/116825.116838
    title: Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)
    locator: unfounded sets and the well-founded partial model that SLG computes
  - paper: doi:10.1017/S1471068411000500
    title: Terrance Swift and David S. Warren, XSB, extending Prolog with tabled logic programming, Theory and Practice of Logic Programming 12(1-2), 157 to 187 (2012)
    locator: the history of tabling in XSB, the SLG-WAM, scheduling and the treatment of the well-founded semantics
  - paper: "Terrance Swift, Alexandre Miguel Pinto and Luís Moniz Pereira, Incremental answer completion in the SLG-WAM, Proceedings of the 25th International Conference on Logic Programming (ICLP 2009), Springer (2009)"
    locator: the answer completion operation and its implementation in the SLG-WAM
---

SLG resolution answers queries top-down, like [SLDNF resolution](/sldnf-resolution/), but it keeps a *table* for each atom it calls. A repeated call does not start a new search: it waits for the answers in the table. A negative literal whose atom is still under evaluation in a cycle is *delayed*: the answer carries it as a condition, and the condition is resolved later. When a group of mutually dependent calls can give no new answers, the group is *completed*. Chen and Warren (1996) proved that this gives the [well-founded semantics](/well-founded-semantics/), and that the evaluation terminates on programs with a finite ground instance, where SLDNF resolution can loop. This page describes SLG for finite ground normal programs. Unlike the [alternating fixpoint](/alternating-fixpoint/), which computes the whole well-founded model bottom-up, SLG evaluates only the atoms that the query reaches.

## In plain words

Prolog answers a question by working backward through the rules. With recursion and negation this can run forever: to decide p it asks about q, and q asks about p again. SLG resolution keeps a table for each question it has asked. When a question comes back, it waits for the answers in the table instead of starting again. When a question depends on its own negation, the method cannot decide it yet, so it puts that condition aside and attaches it to the answer. When a group of questions can produce no new answers, the method closes their tables: a question with no answers is false, and the conditions put aside are checked again. What stays open at the end is unknown. The result agrees with the well-founded model, and only the part of the program that the question reaches is used.

## The problem

The input is a finite ground normal program $P$, a set of rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$, and a query atom $q$. The output is the value of $q$ in the well-founded model of $P$: true, false or undefined. The evaluation also gives the values of all the atoms it calls. Programs with variables are handled by the real engines through calls with substitutions; the page leaves them out.

## The algorithm

A *node* $(h \leftarrow G \mid D)$ stands for a rule of $h$ with the goals $G$ still to solve and the set $D$ of delayed literals. A table holds the answers of its atom: an answer $(h \mid D)$ with $D = \emptyset$ makes the atom *true*, and the other answers are *conditional*. A table is *false* when it is complete and has no answers, and *undefined* when it is complete and has only conditional answers. A literal $b$ is true when $b$ is true and false when $b$ is false; $\mathit{not}\ b$ is the opposite. The *call graph* has an edge $h \to b$ when a node of $h$ selects a literal on $b$.

```pseudo id=main
SLG(P, q)                   ▷ P: a finite ground normal program, q: the query atom
L1  CALL(q) from no caller
L2  loop
L3      while the work list W is not empty do
L4          take a node (h ← G | D) from W, and skip it if h is true
L5          if G is empty then ANSWER(h, D), and continue with the next node
L6          L ← the first literal of G, R ← the rest of G, b ← the atom of L; CALL(b) from h
L7          if L = b then
L8              if b is true then push (h ← R | D)
L9              else if b has answers then push (h ← R | D ∪ {b})                 ▷ delay b
L10             else if b is not complete then add (h ← R | D) to the consumers of b    ▷ else b is false: drop the node
L11         else                                                                ▷ L = not b
L12             if b is true then drop the node
L13             else if b is complete and has no answers then push (h ← R | D)
L14             else if b is complete then push (h ← R | D ∪ {not b})           ▷ b is undefined
L15             else add (h ← R | D) to the negative waiters of b
L16     SIMPLIFY
L17     if every table is complete then return the status of each table
L18     C ← a strongly connected component of the call graph on the incomplete tables, with no edge to another one
L19     if a node of a table of C waits on not b for a table b of C then
L20         move each such node (h ← R | D) to W as (h ← R | D ∪ {not b})       ▷ delaying
L21     else
L22         mark the tables of C complete                                      ▷ completion
L23         repeat
L24             SIMPLIFY
L25             S ← the least set of atoms of C such that a ∈ S if a has an answer whose delayed positive atoms in C are all in S
L26             delete the answers of the atoms of C that are not in S          ▷ answer completion
L27         until line L26 deletes nothing
L28         move each negative waiter on a table of C to W, handled as at lines L12 to L14

CALL(b) from h
L29 if there is a caller h then add the edge h → b to the call graph
L30 if b has no table then create an incomplete table for b, and push (b ← body | ∅) for each rule of b

ANSWER(h, D)
L31 remove the true literals from D; return if D has a false literal, if h is true, or if h has the answer D
L32 if D is empty then make h true: delete its answers, mark it complete, drop its negative waiters
L33 else add the answer (h | D)
L34 if this is the first answer of h then move its consumers to W, handled as at lines L8 and L9

SIMPLIFY
L35 until nothing changes: in each answer remove the true literals; delete the answer if a literal is false; make the head true as at line L32 if the delay becomes empty
```

A component chosen at line L18 has edges only to complete tables, so a node of $C$ can only wait on tables of $C$. If one of these waits is negative, nothing else can move, and line L20 delays the literal. If none is, no table of $C$ can get a new answer, and line L22 completes $C$: a table with no answers becomes false, and its positive consumers are dropped. Line L26 removes answers that are kept only by a positive loop through delayed literals, since such atoms are unfounded.

## Example

Take the program below and the query $p$. Its well-founded model makes $r$ false and leaves $p$ and $q$ undefined.

```text
p ← not q.   q ← not p.   q ← r.   r ← r.
```

The work list is a stack, and the rules of an atom are pushed in order, so the last rule runs first.

| step | node or event | action |
|---|---|---|
| 1 | CALL($p$) | create the table $p$; push $p \leftarrow \mathit{not}\ q$ |
| 2 | $p \leftarrow \mathit{not}\ q$ | CALL($q$): create the table $q$; push $q \leftarrow \mathit{not}\ p$ and $q \leftarrow r$. The table $q$ is incomplete, so the node waits on $\mathit{not}\ q$ |
| 3 | $q \leftarrow r$ | CALL($r$): create the table $r$; push $r \leftarrow r$. The table $r$ has no answers, so the node becomes a consumer of $r$ |
| 4 | $r \leftarrow r$ | $r$ has no answers: the node becomes a consumer of $r$ |
| 5 | $q \leftarrow \mathit{not}\ p$ | $p$ is incomplete: the node waits on $\mathit{not}\ p$ |
| 6 | $W$ is empty | the call graph is $p \to q$, $q \to p$, $q \to r$, $r \to r$; the component $\{r\}$ has no edge out and no negative wait, so it is completed. It has no answers: $r$ is false, and its consumers are dropped |
| 7 | $W$ is empty | the component $\{p, q\}$ has the waits of $p$ on $\mathit{not}\ q$ and of $q$ on $\mathit{not}\ p$; delaying pushes $p \leftarrow\ \mid \{\mathit{not}\ q\}$ and $q \leftarrow\ \mid \{\mathit{not}\ p\}$ |
| 8 | $q \leftarrow\ \mid \{\mathit{not}\ p\}$ | the answer $q \mid \{\mathit{not}\ p\}$ |
| 9 | $p \leftarrow\ \mid \{\mathit{not}\ q\}$ | the answer $p \mid \{\mathit{not}\ q\}$ |
| 10 | $W$ is empty | complete $\{p, q\}$: no literal can be simplified, $S = \{p, q\}$, and nothing is deleted |

The result is $p$ and $q$ undefined, $r$ false. The conditional answers $p \mid \{\mathit{not}\ q\}$ and $q \mid \{\mathit{not}\ p\}$ are the *residual program*: they record why $p$ and $q$ are undefined. SLDNF resolution loops on this query, because the subsidiary tree for $q$ calls $p$ again.

## Correctness

The [correctness proof](proofs/correctness.md) has the details for this ground version. Termination: each rule of a tabled atom starts one chain of nodes, each node has at most one successor, and each wait ends at most once, so there are at most $s$ nodes. Soundness: every node $(h \leftarrow G \mid D)$ comes from a rule of $P$ whose other body literals were true when they were removed, so a true table is true in the well-founded model; and the tables that become false at a completion form an unfounded set, because each of their rules stopped at a false literal or at a positive literal of the same set. Completeness: the final statuses, extended by the well-founded values of the atoms without a table, are a pre-fixpoint of the operator of Van Gelder, Ross and Schlipf, so they are at least as defined as its least fixpoint. Answer completion is needed for the false atoms of positive loops through delayed literals. Chen and Warren (1996) prove soundness and completeness for programs with variables and a finite ground instance.

## Complexity

Let $s$ be the number of rules plus the number of body literals in the part of the program that the query reaches. There are at most $s$ nodes, and each step on a node takes time proportional to the size of its delay. Each pass of the main loop delays at least one waiting node or completes at least one table, so there are at most $2s$ passes. This simple version recomputes the components and repeats the SIMPLIFY passes, which gives $O(s^3)$ time in the worst case. The space is $O(s)$: each chain holds one live node, each table its answers, and the call graph one edge per selected literal. Engines such as XSB keep the components incrementally on a completion stack and simplify through links from each atom to the answers that mention it. For Datalog programs with a fixed set of rules, tabled evaluation under the well-founded semantics takes time polynomial in the size of the data, while SLDNF resolution may not terminate at all.

## Properties

- **Goal-directed.** Only the atoms that the query reaches get tables. The tests check this on random programs.
- **Terminates on finite ground programs.** Loops through positive or negative literals end in a table, never in an infinite branch.
- **Sound and complete for the well-founded semantics.** Each tabled atom gets its value in the well-founded model, with three values.
- **Answers carry their conditions.** The conditional answers form a residual program that explains the undefined atoms.
- **Independent of the rule order.** The order of rules and literals changes the path of the evaluation, but not the result.

## Variants and improvements

- **OLDT resolution.** Tamaki and Sato (1986) introduced tables for definite programs. SLG adds negation, delaying and simplification.
- **The SLG-WAM.** XSB compiles SLG resolution into an extension of the [Warren abstract machine](/warren-abstract-machine/), with scheduling strategies (local and batched) that change the order of answer return and the time of completion.
- **Answer completion.** The operation at line L26 was described by Chen and Warren, and Swift, Pinto and Pereira (2009) gave an incremental way to do it in the SLG-WAM, which had not implemented it before.
- **Call subsumption.** Instead of a table per call variant, a call can use the answers of a more general call that is already tabled.
- **Stratified programs.** If the program is [stratified](/stratified-logic-program/), the well-founded model is total, so every table ends true or false and no conditional answer is left at the end.
- **Bottom-up alternatives.** [Magic sets](/magic-sets/) rewrite a program so that bottom-up [Datalog evaluation](/datalog-evaluation/) also uses only the relevant facts.

## When to use it

Use SLG resolution, through a tabling engine, to answer queries on recursive rules with negation when the program is large and the query needs only a small part of it, or when the program is not stratified and a three-valued answer is acceptable. To get the whole well-founded model of a ground program, the alternating fixpoint is simpler. To get [stable models](/stable-model-semantics/), use an answer set solver; atoms that SLG finds undefined may still be true in every stable model.

## Pitfalls

- **Tables are not free.** Tabling an atom stores all its answers. For programs with variables, a call with many different arguments creates many tables, and the memory grows with them.
- **Delayed literals are not answers.** An answer with a nonempty delay is conditional. Reporting it as true before completion gives wrong results, as in the example, where $p$ and $q$ have answers but are undefined.
- **Answer completion.** Without line L26, a positive loop through delayed literals can keep a false atom undefined. For $a \leftarrow \mathit{not}\ b$, $b \leftarrow c, b$, $c \leftarrow \mathit{not}\ a$, $c \leftarrow c, \mathit{not}\ c$ and the query $a$, the answer $c \mid \{c, \mathit{not}\ c\}$ survives simplification, but $c$ is false.
- **Early decisions on negation.** A negative literal on an incomplete table may only be resolved when the table is true (fail) or complete (succeed or delay). Treating an incomplete table with no answers as false is a common error, and it gives wrong results on loops.

## Implementations

## History

Tamaki and Sato (1986) introduced OLDT resolution, tabling for definite programs. Van Gelder, Ross and Schlipf (1991) defined the well-founded semantics, and Przymusinski and others studied global SLS resolution, a top-down procedure for it that is not effective in general. Chen and Warren developed SLG resolution in the early 1990s and published the full account, with delaying, simplification and the proofs, in the Journal of the ACM in 1996. XSB implemented it in the SLG-WAM, and later Prolog systems added tabling with the well-founded semantics. Swift, Pinto and Pereira (2009) added incremental answer completion to XSB.

## References
