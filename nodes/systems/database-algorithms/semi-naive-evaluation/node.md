---
tag: EVCHB0
kind: algorithm
slug: semi-naive-evaluation
name: Semi-naive evaluation
aliases:
- semi-naive fixpoint
- seminaive evaluation of Datalog
- differential fixpoint evaluation
area: systems/database-algorithms
level: advanced
summary: "Bottom-up evaluation of a Datalog program that, in each round, uses only rule instances with at least one fact that is new from the last round. Same result as naive evaluation, less work."
solves: [datalog-evaluation]
model: word-ram
complexity:
  vars: {s: the number of rounds, r: the number of rules, k: the largest number of atoms in a rule body, v: the largest number of variables in a rule, n: the number of constants, F: the number of facts of the least model}
  time: {worst: O(s r k^2 n^v)}
  space: {extra: O(F)}
prereqs: [datalog, datalog-evaluation]
see_also: [magic-sets, dred-algorithm, transitive-closure, horn-sat-forward-chaining, incremental-view-maintenance, fixed-point]
sources:
  - paper: doi:10.1007/978-1-4612-4980-1_17
    title: François Bancilhon, Naive evaluation of recursively defined relations, in Michael L. Brodie and John Mylopoulos (eds.), On Knowledge Base Management Systems, Springer, 165 to 178 (1986)
    locator: the differential of a relational expression and its use to evaluate a least fixed point without repeated work
  - paper: doi:10.1016/0743-1066(87)90004-5
    title: Isaac Balbin and Kotagiri Ramamohanarao, A generalization of the differential approach to recursive query evaluation, Journal of Logic Programming 4(3), 259 to 262 (1987)
    locator: the semi-naive method for rules with several recursive atoms and for systems of rules
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 13 (evaluation of Datalog), the naive and semi-naive bottom-up methods
  - paper: doi:10.1109/69.43410
    title: Stefano Ceri, Georg Gottlob and Letizia Tanca, What you always wanted to know about Datalog (and never dared to ask), IEEE Transactions on Knowledge and Data Engineering 1(1), 146 to 166 (1989)
    locator: the section on bottom-up evaluation, naive and semi-naive
---

Semi-naive evaluation computes the least model of a [Datalog](/datalog/) program bottom up, like naive evaluation, but without most of its repeated work. Naive evaluation applies every rule to all known facts in each round, so it derives each fact again in every later round. Semi-naive evaluation keeps the set $\Delta$ of facts that are new in the last round, and in the next round it only uses rule instances that have at least one body fact from $\Delta$. Every other instance was already used in an earlier round. The result is the same least fixed point. Bancilhon described the method in 1986 as a differential of relational expressions, and Balbin and Ramamohanarao generalized it in 1987 to rules with several recursive atoms. It is the standard bottom-up method of Datalog engines.

## In plain words

Think of a list of facts that grows. Each rule says how to make a new fact from facts that are already on the list. The plain method reads the whole list in each round and tries every rule on it. Most of what it finds, it found before.

The better method marks the facts that came in the last round. In the next round, a rule is used only if at least one of the facts that it needs is a marked fact. A combination of only old facts was tried in an earlier round, so it cannot give anything new.

The method stops when a round adds nothing. It gives the same list as the plain method. With one more care, about which facts to use on each side of the marked one, it makes each derivation exactly once.

## The problem

The input is a Datalog program $P$ and a finite set $D$ of EDB facts. The output is the least model $M^*$ of $P$ on $D$, the least fixed point of the immediate consequence operator $T_P$. This is the [Datalog evaluation problem](/datalog-evaluation/). In a rule body, an atom with an IDB predicate, one that occurs in some head, is an *IDB atom*; the others are EDB atoms.

## The algorithm

```pseudo id=main
SEMI-NAIVE(P, D)
L1  Δ ← heads of the rules of P with no IDB atom, evaluated on D
L2  M ← D ∪ Δ
L3  while Δ ≠ ∅ do
L4      M_old ← M − Δ
L5      N ← ∅
L6      for each rule H ← B₁, …, Bₘ of P and each IDB position j of its body do
L7          N ← N ∪ heads of the rule with IDB atoms B_i (i < j) over M_old, B_j over Δ, and all other atoms over M
L8      Δ ← N − M
L9      M ← M ∪ Δ
L10 return M
```

Line L1 starts with the rules that need no IDB fact, such as the exit rule of a recursion. In a round, line L7 evaluates one *differential* of each rule for each IDB atom of its body: a join in which that atom ranges over the new facts $\Delta$ only. The IDB atoms before position $j$ range over the facts that were known before the last round, and the atoms after it range over all facts. This split makes each rule instance be found in exactly one round and for exactly one position. Line L8 keeps the facts that are really new, and they form the $\Delta$ of the next round.

**Naive evaluation**, for comparison, sets $M \leftarrow D$ and repeats $M \leftarrow M \cup T_P(M)$ until $M$ does not change, with every atom over all of $M$.

**The basic form.** Many texts give a simpler line L7: atom $B_j$ over $\Delta$ and every other atom over $M$. It has the same result. For a *linear* rule, with one IDB atom, it is the same as line L7. For a rule with two or more IDB atoms, an instance with new facts at two positions is found twice in the same round.

## Example

The right-linear [transitive closure](/transitive-closure/) program

$$\mathit{path}(x, y) \leftarrow \mathit{edge}(x, y), \qquad \mathit{path}(x, y) \leftarrow \mathit{edge}(x, z), \mathit{path}(z, y)$$

on the chain $\mathit{edge}(1, 2), \mathit{edge}(2, 3), \mathit{edge}(3, 4)$. Write $p_{ab}$ for $\mathit{path}(a, b)$.

| round | instances fired | $\Delta$ after the round |
|---|---|---|
| L1 | the exit rule on the 3 edges: 3 | $p_{12}, p_{23}, p_{34}$ |
| 1 | $\mathit{edge}(1,2), p_{23}$ and $\mathit{edge}(2,3), p_{34}$: 2 | $p_{13}, p_{24}$ |
| 2 | $\mathit{edge}(1,2), p_{24}$: 1 | $p_{14}$ |
| 3 | no edge ends at node 1: 0 | empty |

Semi-naive evaluation fires 6 rule instances, one for each fact of $\mathit{path}$. Naive evaluation fires $3 + 5 + 6 + 6 = 20$, because it fires the exit rule in each of its four rounds and repeats all earlier instances of the recursive rule. On a chain of 20 nodes the counts are 190 and 2660. For the nonlinear rule $\mathit{path}(x, y) \leftarrow \mathit{path}(x, z), \mathit{path}(z, y)$ on a chain of 10 nodes, this algorithm fires 129 instances, which is the number of true instances, the basic form fires 155, and naive evaluation fires 410. These counts come from the implementation of this page.

## Correctness

Each fact that the algorithm adds is the head of a rule instance whose body facts are already known, so all facts are in the least model $M^*$. For the converse, give each IDB fact its *stage*, the round in which it entered $\Delta$. Take any rule instance whose body is true in the final $M$, let $s$ be the largest stage of its IDB body facts, and let $j$ be the first IDB position with stage $s$. In round $s + 1$, the facts before $j$ have a smaller stage and are in $M_{\text{old}}$, the fact at $j$ is in $\Delta$, and the facts after $j$ are in $M$. So line L7 fires the instance in that round, and its head is in $M$. The final $M$ is therefore closed under the rules, so it contains $M^*$, and the two are equal. The same argument shows that an instance is fired only in round $s + 1$ and only for position $j$, so each true instance is fired exactly once. The loop stops because $M$ grows in each round and $M^*$ is finite. The full proof is in the proof file of this page.

## Complexity

Let $s$ be the number of rounds, $r$ the number of rules, $k$ the largest body size, $v$ the largest number of variables in a rule, $n$ the number of constants and $F$ the size of the least model.

- **Derivations.** The algorithm fires each true rule instance exactly once, so the number of derivations is the number of true instances, at most $r n^v$. Naive evaluation fires each one again in every round after it first becomes true, so on the chain of $n$ nodes it does $\Theta(n^3)$ derivations, against $\Theta(n^2)$ here.
- **Time.** With a hash index on each relation, the search for one differential of one rule explores at most $k n^v$ partial instances. There are $r$ rules with at most $k$ differentials each in each of the $s$ rounds, which gives $O(s r k^2 n^v)$ time. This is a coarse bound: in practice the joins with the small set $\Delta$ are cheap, and the total work is close to the number of derivations.
- **Rounds.** $s$ is at most the number of IDB facts, and for the path program it is the length of the longest shortest path: $\Delta$ after round $t$ holds the pairs at distance $t + 1$, and the last round finds nothing.
- **Space.** The sets $M$, $M_{\text{old}}$, $\Delta$ and $N$ hold at most $O(F)$ facts.

## Properties

- **Same result as naive evaluation.** Both compute the least fixed point of $T_P$.
- **No repeated derivation.** With the split of line L7, each true rule instance is used once. With the basic form, this holds for linear rules only.
- **Stage by stage.** After round $t$, $M$ holds exactly the facts that naive evaluation has after $t + 1$ rounds, so the number of rounds is the same.
- **Duplicate facts remain.** Two different instances can derive the same fact, so a fact can still be derived more than once. Line L8 removes these duplicates.
- **Bottom up.** It computes the whole least model, also the facts that a query does not need.

## Variants and improvements

- **Magic sets.** For a query with constants, such as $\mathit{path}(1, y)$, the [magic sets transformation](/magic-sets/) rewrites the program so that semi-naive evaluation only derives facts that are relevant to the query.
- **Stratified negation.** Evaluate the strata in order, each with semi-naive evaluation. Negated atoms refer to lower strata, which are complete, so they are read as fixed relations.
- **Incremental maintenance.** When facts are inserted into $D$, semi-naive evaluation can continue from the old model with the new facts as $\Delta$. Deletions need more care, as in the [DRed algorithm](/dred-algorithm/) and other methods of [incremental view maintenance](/incremental-view-maintenance/).
- **Differential dataflow and parallel engines.** Modern engines run the differentials of each round as parallel joins, and some keep the differences between rounds for later updates.

## When to use it

Use semi-naive evaluation whenever a Datalog program, a recursive SQL query or a fixed-point computation over relations must be computed bottom up. There is little reason to use naive evaluation except as a test oracle. When only a few answers are needed, combine it with magic sets or use top-down evaluation with tabling.

## Pitfalls

- **Using $\Delta$ for every IDB atom at once.** A join with all IDB atoms over $\Delta$ misses instances that combine a new fact with an old one, and the result is too small.
- **Forgetting the exit rules.** Rules with no IDB atom have no differential. They must be fired once, at the start, as in line L1.
- **Taking $\Delta$ as all of $N$.** Line L8 must remove the facts already known, or the loop never stops.
- **IDB facts in the input.** If $D$ already contains IDB facts, they must go into the first $\Delta$, or instances that use them are missed. The implementation of this page rejects such input.
- **Nonlinear rules with the basic form.** It is correct but does repeated work; use the split of line L7.

## Implementations

## History

The idea of evaluating only the change of a recursive expression appears in work on recursive query processing in the mid-1980s. Bancilhon's 1986 chapter, from a 1985 workshop, defined the differential of a relational expression and used it to compute a least fixed point. Balbin and Ramamohanarao gave a general form for rules with several recursive atoms and for mutually recursive rules in 1987. Bancilhon and Ramakrishnan compared the method with other strategies for recursive queries in 1986. The method became part of every bottom-up Datalog system.

## References
