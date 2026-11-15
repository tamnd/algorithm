---
tag: XH30CH
kind: technique
slug: equality-saturation
name: Equality saturation
aliases:
- e-graph rewriting
area: compilers-and-program-analysis/optimizations
level: research
summary: Applies all rewrite rules to an e-graph without choosing, until no rule adds anything, and then extracts the cheapest equivalent program.
prereqs: [e-graph, e-matching, term-rewriting-system]
see_also: [superoptimization, congruence-closure, set-cover, peephole-optimization, strength-reduction, translation-validation, binary-integer-programming, word-problem]
sources:
  - paper: doi:10.1145/1480881.1480915
    title: "Ross Tate, Michael Stepp, Zachary Tatlock and Sorin Lerner, Equality saturation: a new approach to optimization, Proceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 2009), 264-276"
    locator: the phase ordering problem, the saturation of an e-graph by axioms, program expression graphs for loops, and the extraction of the best program by a pseudo-Boolean solver
  - paper: "doi:10.2168/lmcs-7(1:10)2011"
    title: "Ross Tate, Michael Stepp, Zachary Tatlock and Sorin Lerner, Equality saturation: a new approach to optimization, Logical Methods in Computer Science 7(1), 2011"
    locator: the journal version, with the full translation of programs to and from program expression graphs and the evaluation in the Peggy optimizer
  - paper: doi:10.1145/3434304
    title: "Max Willsey, Chandrakana Nandi, Yisu Remy Wang, Oliver Flatt, Zachary Tatlock and Pavel Panchekha, egg: fast and extensible equality saturation, Proceedings of the ACM on Programming Languages 5(POPL), 2021"
    locator: Section 2, the equality saturation loop with search, apply and rebuild, the limits on iterations, e-nodes and time, the example of (a * 2) / 2, and e-class analyses
  - paper: doi:10.1145/322186.322198
    title: Greg Nelson and Derek C. Oppen, Fast decision procedures based on congruence closure, Journal of the ACM 27(2), 1980, 356-364
    locator: the graph of terms with merged classes and the congruence closure that the e-graph keeps
  - paper: doi:10.1145/512529.512566
    title: "Rajeev Joshi, Greg Nelson and Keith Randall, Denali: a goal-directed superoptimizer, Proceedings of the ACM SIGPLAN 2002 Conference on Programming Language Design and Implementation (PLDI 2002), 304-314"
    locator: the use of an e-graph saturated by axioms as the space of programs for a superoptimizer
  - paper: doi:10.1145/2737924.2737959
    title: Pavel Panchekha, Alex Sanchez-Stern, James R. Wilcox and Zachary Tatlock, Automatically improving accuracy for floating point expressions, Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2015), 1-11
    locator: the Herbie tool, which rewrites real-number expressions in an e-graph and extracts the most accurate floating point program
  - paper: doi:10.1007/978-3-642-22110-1_59
    title: Michael Stepp, Ross Tate and Sorin Lerner, Equality-based translation validator for LLVM, Computer Aided Verification (CAV 2011), LNCS 6806, 737-742
    locator: the use of equality saturation to show that a program and its optimized version are equal
---

Equality saturation is a way to optimize a program with rewrite rules without choosing which rule to apply first. A normal rewriter replaces a term by another, so each step loses the old term, and the order of the steps decides the result. This is the phase ordering problem. Equality saturation keeps every version. It puts the program in an [e-graph](/e-graph/), finds every match of every rule by [E-matching](/e-matching/), and adds each right-hand side to the class of the term it matched, so the class now holds both. It repeats this until no rule adds anything, which is *saturation*, and then *extracts* the cheapest term of the root class under a cost model. Tate, Stepp, Tatlock and Lerner introduced it in 2009, and the egg library of Willsey and others made it fast and common. When it stops, the e-graph holds every program that the rules can reach, so the result does not depend on rule order. The common mistake is to think that it always stops. Many natural rules make the e-graph grow without end, and real tools stop at a limit on iterations, e-nodes or time.

## In plain words

Think of a rewriter that may only keep one version of a formula. Each change throws away the old version, and an early change can block a better one later. Equality saturation keeps a shared record of all versions that are known to be equal. Each rule only adds a new version beside the old one. It never removes anything.

We apply every rule everywhere, again and again. If a round adds nothing new, the record holds every version the rules can reach, and we pick the cheapest one. Because nothing was thrown away, the order of the rules does not matter.

The record is compact: a part that two versions share is stored once. Still, some rule sets make it grow forever, so in practice we also stop after a fixed number of rounds or a size limit, and pick the cheapest version found so far.

## When it applies

- The program, or a part of it, is a term or a DAG of pure operations. A block of [three-address code](/three-address-code/) without side effects becomes a DAG by naming each value once. Loops and effects need an extended form, such as the program expression graphs of Tate and others.
- The optimizations are equations: rules $l \to r$ where $l\theta$ and $r\theta$ have the same value for every substitution $\theta$, possibly under a side condition.
- The order of the rules matters for a normal rewriter, or the rules include ones that make a term worse before it gets better, such as reassociation.
- A cost model gives a cost to each operation, and the best program is the one of least cost.

## The template

**Rules.** A rule $l \to r$ is a pair of patterns, terms with variables, where every variable of $r$ occurs in $l$. A *step* $s \to_R s'$ replaces one subterm $l\theta$ of $s$ by $r\theta$. Let $=_R$ be the least congruence that contains every pair $(l\theta, r\theta)$; equivalently, $s =_R s'$ when a chain of steps, each one forward or backward, leads from $s$ to $s'$. A rule is *sound* if $l\theta$ and $r\theta$ have the same value for every $\theta$. If every rule is sound, $s =_R s'$ implies that $s$ and $s'$ have the same value, since equality of values is a congruence.

**Represented terms.** A class represents a term as on the [e-graph](/e-graph/) page: $f(t_1, \ldots, t_k)$ is represented by $x$ if $x$ has an e-node $f(c_1, \ldots, c_k)$ and each $t_i$ is represented by $c_i$. In a clean state, a term is represented by at most one class, by the congruence invariant.

**The loop.**

```
G ← an e-graph with the input term t; root ← the class of t
repeat
    M ← every (l → r, x, σ) such that class x matches l with σ    ▷ on a clean G
    for each (l → r, x, σ) in M: y ← ADD(r σ); MERGE(x, y)
    REBUILD
until no step in this round added an e-node or merged two classes,
      or a limit on rounds, e-nodes or time is reached
return EXTRACT(root)
```

Here $\sigma$ maps each variable of $l$ to a class, and $r\sigma$ is added bottom up. All matches of a round are found before any is applied, so the round does not depend on the order of the rules. EXTRACT is the least tree cost fixpoint of the e-graph page.

**Legality.** *Theorem 1. At every point of the loop, two terms represented by the same class are equal under $=_R$. So if the rules are sound, every term that the root class represents, and in particular the extracted one, has the value of the input.* Proof. In a clean state, the relation "represented by the same class" is contained in the congruence closure of the pairs that were merged, by the invariants on the e-graph page. Before any merge, each class represents one term. So it is enough that each merged pair is made of $=_R$-equal terms, by induction on the merges, since $=_R$ is a congruence and contains the closure of equal pairs. ADD merges nothing. A merge of the loop joins $x$ and $y$, where $x$ matches $l$ with $\sigma$ and $y$ is the class of $r\sigma$. Choose for each variable $v$ a term $\theta(v)$ that $\sigma(v)$ represents; every class represents at least one term, since its first e-node was built from existing classes. Then $x$ represents $l\theta$, $y$ represents $r\theta$, and $l\theta =_R r\theta$. By induction, every term of $x$ is $=_R$-equal to $l\theta$, and every term of $y$ to $r\theta$, so all are $=_R$-equal. $\square$

**Profit.** The input term stays represented by the root class, since the loop never removes an e-node. So the extracted term has a tree cost at most that of the input. With an exact extractor it has the least cost of all the terms the e-graph represents.

**Saturation.** *Theorem 2. Suppose a round adds no e-node and merges no classes. If a class $x$ represents $s$ and $s \to_R s'$, then $x$ represents $s'$. So the root class represents every term that forward steps reach from the input. If $R$ has each rule in both directions, the root class represents exactly the terms $s'$ with $s' =_R t$.*

Proof. *(a) Matching finds the step.* If $x$ represents $l\theta$, then $x$ matches $l$ with some $\sigma$ such that $\sigma(v)$ represents $\theta(v)$ for each variable $v$. By induction on $l$: a variable binds to $x$; for $l = f(l_1, \ldots, l_k)$, the class $x$ has an e-node $f(c_1, \ldots, c_k)$ with $c_i$ representing $l_i\theta$, and E-matching tries this e-node. A variable that occurs twice gets the same class both times, because a term is represented by only one class. *(b) Instances.* If $\sigma(v)$ represents $\theta(v)$ for each $v$ and the e-graph has every e-node of $r\sigma$, then the class of $r\sigma$ represents $r\theta$, by induction on $r$. *(c) One step at the root.* Let $s = l\theta$. By (a), the round found $(l \to r, x, \sigma)$. It added nothing, so the e-graph had every e-node of $r\sigma$, and MERGE$(x, y)$ joined nothing, so $y = x$. By (b), $x$ represents $r\theta = s'$. *(d) A step below the root.* Let $s = f(s_1, \ldots, s_k)$ with the step in $s_i$. The class $x$ has an e-node $f(c_1, \ldots, c_k)$ with $c_j$ representing $s_j$. By induction on the depth of the step, $c_i$ represents $s'_i$, so $x$ represents $s'$. *(e)* By induction on the number of steps, $x$ represents every term that forward steps reach. With both directions of each rule, any chain of steps is a chain of forward steps, so the root class contains the whole $=_R$-class of $t$; Theorem 1 gives the other inclusion. $\square$

So "saturated" means that the e-graph is closed under the rules, and the choice of the result is left to extraction. The result is the cheapest term reachable by the rules, up to the congruence that the e-graph keeps, and it does not depend on any order of rule application. Saturation can fail to happen; Example 3 below gives a rule set that never saturates.

**Extraction with sharing.** The tree cost counts a shared subterm once for each use. The *DAG cost* counts each chosen e-node once. An *extraction* chooses one e-node for each class that it needs, starting at the root and going through the children of the chosen e-nodes, with no cycle. Its DAG cost is the sum of the costs of the chosen e-nodes.

*Theorem 3. To decide whether an e-graph has an extraction of DAG cost at most $K$ is NP-complete.* Proof. It is in NP: an extraction is a certificate, and its cost and the absence of a cycle are checked in polynomial time. For hardness, reduce [set cover](/set-cover/): a universe $u_1, \ldots, u_n$, sets $S_1, \ldots, S_m$ and a bound $k$. Build an e-graph with:

- a class $X_j$ for each set, with one leaf e-node $s_j$ of cost 1;
- a class $E_i$ for each element, with one e-node $g_i(X_j)$ of cost 0 for each $j$ such that $u_i \in S_j$;
- a root class with one e-node $\mathit{root}(E_1, \ldots, E_n)$ of cost 0.

The symbols $g_i$ differ for different $i$, so no two e-nodes are congruent, and the e-graph is clean. It has $O(nm)$ e-nodes. An extraction chooses for each $E_i$ one $g_i(X_j)$ with $u_i \in S_j$, and then it must choose $s_j$ in each class $X_j$ that it reaches. Its DAG cost is the number of distinct $j$ chosen, and those sets cover every $u_i$. Conversely, a cover by $S_{j_1}, \ldots, S_{j_c}$ gives an extraction of cost $c$: for each $u_i$, choose $g_i(X_j)$ for some $j$ in the cover with $u_i \in S_j$. So an extraction of DAG cost at most $k$ exists if and only if a cover of size at most $k$ exists. Set cover is [NP-complete](/np-complete/). $\square$

So exact DAG extraction is done by [0-1 integer programming](/binary-integer-programming/) or a pseudo-Boolean solver, as in Tate and others, or by a heuristic. The tree cost fixpoint is exact for tree cost and runs in polynomial time.

## Classic examples

The numbers come from a short Python script with an e-graph, E-matching by search over all classes, and the loop above. Each count is the number of classes and of e-nodes after the round.

**Division by a power of two.** The input is $(a \cdot 2) / 2$, read as exact arithmetic on rationals, with the rules

| name | rule |
|---|---|
| shl | $x \cdot 2 \to x \ll 1$ |
| reassoc | $(x \cdot y) / z \to x \cdot (y / z)$ |
| div-self | $x / x \to 1$ |
| mul-one | $x \cdot 1 \to x$ |

A rewriter that applies `shl` first, as a [strength reduction](/strength-reduction/) pass would, gets $(a \ll 1) / 2$, where no rule applies any more. Equality saturation gives:

| round | matches | classes | e-nodes | what happened |
|---|---|---|---|---|
| start | | 4 | 4 | $a$, $2$, $a \cdot 2$, $(a \cdot 2) / 2$ |
| 1 | 2 | 6 | 8 | `shl` adds $a \ll 1$; `reassoc` adds $2 / 2$ and $a \cdot (2 / 2)$ |
| 2 | 3 | 5 | 8 | `div-self` merges $2 / 2$ with $1$ |
| 3 | 4 | 4 | 8 | `mul-one` matches $a \cdot (2 / 2)$ and merges the root with $a$ |
| 4 | 4 | 4 | 8 | nothing new: saturated |

At the end the four classes are $\{a, (a \cdot 2)/2, a \cdot 1\}$, $\{2\}$, $\{1, 2/2\}$ and $\{a \cdot 2, a \ll 1\}$. The root class has e-nodes that point back to it, so it represents infinitely many terms, such as $a \cdot 1 \cdot 1$. With costs 8 for $/$, 4 for $\cdot$, 1 for $\ll$ and 1 for a leaf, the input costs 15, and extraction returns $a$ with cost 1. The rule `div-self` needs $x \ne 0$ to be sound; here it matches only $2 / 2$. The rule `reassoc` is sound for rationals but not for integer division: $(3 \cdot 2) / 4 = 1$ but $3 \cdot (2 / 4) = 0$.

**Associativity and commutativity.** The rules $x + y \to y + x$, $x + (y + z) \to (x + y) + z$ and $(x + y) + z \to x + (y + z)$, from $a_1 + (a_2 + (\cdots + a_n))$:

| $n$ | rounds | classes | e-nodes |
|---|---|---|---|
| 2 | 2 | 3 | 4 |
| 3 | 4 | 7 | 15 |
| 4 | 5 | 15 | 54 |
| 5 | 6 | 31 | 185 |
| 6 | 6 | 63 | 608 |

The rounds count the last round, which adds nothing. Each class is the sum of a nonempty subset of the $a_i$, so there are $2^n - 1$ classes. A class of a subset $S$ with $|S| \ge 2$ has one e-node $X + Y$ for each ordered split of $S$ into two nonempty parts, $2^{|S|} - 2$ of them, and the sum over all subsets, with the $n$ leaves, is $3^n - 2^{n+1} + 1 + n$. The e-graph saturates, but its size is exponential in $n$. It is still much smaller than the set of terms it represents, which holds every bracketing and every order of the $n$ operands.

**A rule set that never saturates.** The rule $x / y \to (x \cdot 2) / (y \cdot 2)$ from $a / b$: after round $k$ there are $4 + 2k$ classes and $4 + 3k$ e-nodes, for $k = 1$ to 6, the limit in the script. Each round adds the class of $b \cdot 2^{k}$. These classes never merge: a term without $/$ has no subterm that the rule matches, so it is $=_R$-equal only to itself, and by Theorem 1 two different such terms are in different classes. The loop runs until a limit stops it. In contrast, $x \to x + 0$ from $a$ saturates after 3 rounds with 2 classes and 4 e-nodes: $a + 0$ goes into the class of $a$, and the next match of $x$ to that class adds the same e-node again.

**Sharing in extraction.** The set cover instance with $U = \{1, 2, 3, 4\}$, $S_1 = \{1, 2\}$, $S_2 = \{3, 4\}$, $S_3 = \{1, 3\}$, $S_4 = \{2, 4\}$, $S_5 = \{1\}$, built as in Theorem 3, has $3 \cdot 2 \cdot 2 \cdot 2 = 24$ extractions. Every one has tree cost 4, so the tree cost fixpoint cannot tell them apart. The least DAG cost is 2, with $S_1$ and $S_2$, which is the least cover.

## Variations

- **E-class analysis.** egg attaches a value from a semilattice to each class, such as a known constant, and joins the values at each merge. A class with a known constant gets the constant as an e-node, which does [constant folding](/constant-folding/) inside the e-graph.
- **Program expression graphs.** Tate and others turn a whole function, with loops, into a graph of pure operators with special nodes for loop values, saturate it, and turn the extracted graph back into a program. Their Peggy optimizer works this way on Java bytecode.
- **Schedules and limits.** egg stops on a limit of rounds, e-nodes or time, and can apply a rule less often when it matches too much, so that rules such as associativity do not fill the e-graph alone.
- **Extraction.** Exact DAG extraction by integer programming or a pseudo-Boolean solver, as in Tate and others; the tree cost fixpoint of the e-graph page; or a greedy heuristic.
- **Superoptimization.** Denali saturates an e-graph with axioms and asks a SAT solver for the fastest machine program that the e-graph holds, a goal-directed form of [superoptimization](/superoptimization/).
- **Accuracy and validation.** Herbie rewrites real-number expressions in an e-graph and extracts the most accurate floating point program. The same saturation can show that two programs are equal, which is [translation validation](/translation-validation/) by equality.

## Pitfalls

- **It may not stop.** As in the example above, a rule can make new classes in every round. Run with a limit on rounds, e-nodes and time, and accept that a stop by limit gives the best term found, not the best term the rules can reach.
- **Exponential growth.** Associativity and commutativity saturate, but with $2^n - 1$ classes and about $3^n$ e-nodes for $n$ operands. Apply such rules with a schedule, or handle them with a special form of the e-graph.
- **Unsound rules.** Theorem 1 only says that the result is $=_R$-equal to the input. A rule that is false, such as `reassoc` for integer division, or `div-self` without $x \ne 0$, makes the optimizer return a wrong program. Each rule needs its side condition and a proof, or an e-class analysis that checks it.
- **Tree cost and shared terms.** The fixpoint counts a shared term once for each use. For $(a + b) \cdot (a + b)$ it pays for $a + b$ twice. If the code generator shares the value, the costs differ, and the exact DAG problem is NP-hard by Theorem 3.
- **A dirty e-graph.** Matching between MERGE and REBUILD can miss matches. Find all matches of a round on a clean e-graph, as in the loop above.
- **The cost model.** Extraction is as good as its costs. Costs per e-node cannot see the latency of a chain or the pressure on registers.

## Exercises

1. Run the loop by hand on $(a \cdot 2) / 2$ with only `shl`, `div-self` and `mul-one`. Does it saturate, and what does it extract?
2. Prove that the tree cost of the extracted term never increases from one round to the next, if extraction is run after every round.
3. With the rules $x + y \to y + x$ only, how many classes and e-nodes does $a_1 + (a_2 + a_3)$ have at saturation?
4. Give a sound rule that adds a new class in every round, other than the one above, and prove that the classes never merge.
5. In the reduction of Theorem 3, show that the e-graph has no cycle, and that the tree cost of every extraction is $n$.

## References
