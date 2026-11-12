---
tag: K2D6D5
kind: algorithm
slug: dred-algorithm
name: DRed algorithm
aliases:
- delete and rederive
- delete-rederive view maintenance
area: systems/database-algorithms
level: research
summary: "Maintains a recursive Datalog view after inserts and deletes of stored facts: overdelete every fact with a derivation through a deleted fact, rederive the ones that remain true, then insert."
solves: [view-maintenance]
model: word-ram
complexity:
  vars: {s: the number of rounds of the two loops, r: the number of rules, k: the largest number of atoms in a rule body, v: the largest number of variables in a rule, n: the number of constants, F: the number of facts of the old and the new model}
  time: {worst: O((s + 1) r k^2 n^v)}
  space: {extra: O(F)}
prereqs: [datalog, semi-naive-evaluation]
see_also: [incremental-view-maintenance, view-maintenance, materialized-view, datalog-evaluation, magic-sets, transitive-closure, horn-sat-forward-chaining]
sources:
  - paper: doi:10.1145/170035.170066
    title: Ashish Gupta, Inderpal Singh Mumick and V. S. Subrahmanian, Maintaining views incrementally, Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data, 157 to 166
    locator: the DRed algorithm for recursive views with its three steps, and the counting algorithm for nonrecursive views
  - url: http://sites.computer.org/debull/95JUN-CD.pdf
    title: Ashish Gupta and Inderpal Singh Mumick, Maintenance of materialized views, problems, techniques, and applications, IEEE Data Engineering Bulletin 18(2), 3 to 18 (1995)
    locator: the survey of view maintenance methods, with counting and DRed and the classes of views to which each applies
---

DRed, for *delete and rederive*, keeps the least model of a [Datalog](/datalog/) program up to date when stored facts are inserted or deleted. It is a method of [incremental view maintenance](/incremental-view-maintenance/) for recursive views, and it solves the [view maintenance](/view-maintenance/) problem without a new evaluation from the start. Insertions are easy: [semi-naive evaluation](/semi-naive-evaluation/) continues from the old model with the new facts as its first $\Delta$. Deletions are hard, because a derived fact can have several derivations, and with recursion a fact can seem to support itself through a cycle. DRed works in three phases. It first *overdeletes*: it removes every derived fact that has at least one derivation that uses a deleted fact. It then *rederives* the removed facts that still have a derivation from the facts that remain. Finally it *inserts*, semi-naively, the consequences of the rederived facts and of the inserted stored facts. Gupta, Mumick and Subrahmanian gave the algorithm in 1993, together with a counting algorithm for nonrecursive views.

## In plain words

You keep a list of facts that follow from some stored facts by rules. Now some stored facts are removed. Which derived facts must go?

A fact that was made with the help of a removed fact may still be true, because there can be another way to make it. DRed does not try to decide this at once. First it takes away, too eagerly, every fact that has any way of being made that uses a removed fact, and then every fact made from those, and so on.

Then it looks at each fact it took away and asks: can one rule still make it from the facts that are left? If yes, it puts the fact back. Last, it runs the rules forward from the facts it put back and from the new stored facts, so that every fact that is true again comes back.

## The problem

The input is a Datalog program $P$ with no negation, the old stored facts $E$, the old model $M = P(E)$, which is the least model of $P$ on $E$, a set $E^-$ of stored facts to delete and a set $E^+$ of stored facts to insert. The output is the new stored set $E' = (E \setminus E^-) \cup E^+$ and the new model $P(E')$. Only stored (EDB) facts change; derived (IDB) facts change as a result. A materialized view defined by recursive rules, such as the [transitive closure](/transitive-closure/) of a stored edge relation, is the usual case.

## The algorithm

A rule instance is *true* in a set of facts when all its body facts are in the set.

```pseudo id=main
DRED(P, E, M, E⁻, E⁺)
L1  E⁺ ← E⁺ − E;  E⁻ ← (E⁻ ∩ E) − E⁺           ▷ keep only real changes
L2  D ← E⁻;  Δ ← E⁻
L3  while Δ ≠ ∅ do                               ▷ phase 1: overdelete
L4      N ← heads of the rule instances that are true in M and have a body fact in Δ
L5      Δ ← N − D;  D ← D ∪ Δ
L6  M ← M − D;  E ← (E − E⁻) ∪ E⁺
L7  R ← {f ∈ D : some rule instance with head f is true in M}   ▷ phase 2: rederive
L8  Δ ← R ∪ E⁺;  M ← M ∪ Δ
L9  while Δ ≠ ∅ do                               ▷ phase 3: insert
L10     N ← heads of the rule instances that are true in M and have a body fact in Δ
L11     Δ ← N − M;  M ← M ∪ Δ
L12 return E, M
```

Lines L2 to L5 compute the overdeleted set $D$. They run semi-naive evaluation on the old model, but they propagate deletions instead of insertions: a head is marked when some instance that was true before the update uses a fact that is marked. The set $D$ holds the deleted stored facts and every derived fact with some derivation through them. Line L6 removes $D$. Line L7 checks each removed derived fact with one rule step over the facts that remain. Lines L8 to L11 are semi-naive evaluation with the rederived facts and the inserted stored facts as the first $\Delta$. The rederived facts in $R$ may be few, and the facts that they support come back in phase 3.

## Example

The right-linear program $\mathit{path}(x, y) \leftarrow \mathit{edge}(x, y)$, $\mathit{path}(x, y) \leftarrow \mathit{edge}(x, z), \mathit{path}(z, y)$ on the edges $1 \to 2$, $2 \to 3$, $3 \to 4$ and $1 \to 3$. Write $p_{ab}$ for $\mathit{path}(a, b)$. The model has the six facts $p_{12}, p_{13}, p_{14}, p_{23}, p_{24}, p_{34}$. Delete the edge $2 \to 3$.

| step | facts | why |
|---|---|---|
| overdelete, round 1 | $p_{23}$, $p_{24}$ | $\mathit{edge}(2, 3)$ is in the body of $p_{23} \leftarrow \mathit{edge}(2,3)$ and of $p_{24} \leftarrow \mathit{edge}(2,3), p_{34}$ |
| overdelete, round 2 | $p_{13}$, $p_{14}$ | $p_{23}$ and $p_{24}$ are used by $p_{13} \leftarrow \mathit{edge}(1,2), p_{23}$ and $p_{14} \leftarrow \mathit{edge}(1,2), p_{24}$ |
| overdelete, round 3 | none | no edge ends at node 1 |
| rederive | $p_{13}$, $p_{14}$ | $p_{13} \leftarrow \mathit{edge}(1,3)$ and $p_{14} \leftarrow \mathit{edge}(1,3), p_{34}$ use only facts that remain |
| insert | none | no instance uses $p_{13}$ or $p_{14}$ |

Four facts are overdeleted, two are rederived, and the new model has $p_{12}, p_{13}, p_{14}, p_{34}$. Inserting the edge $2 \to 3$ again overdeletes nothing, rederives nothing, and the insert phase derives $p_{23}$ and $p_{24}$.

On the cycle $1 \to 2 \to 3 \to 1$ all nine $\mathit{path}$ facts hold. Deleting the edge $3 \to 1$ overdeletes all nine. The rederive step puts back $p_{12}$ and $p_{23}$ from their edges, and the insert phase derives $p_{13}$ from them. This is the case that defeats simple counting: on a cycle, each fact has derivations through the others, so a count of derivations would not drop to zero for facts that are no longer true. These counts come from the implementation of this page.

## Correctness

Let $M$ be the old model and $M' = P(E')$ the new one. The overdeleted set $D$ is closed in this sense: if a rule instance is true in $M$ and has a body fact in $D$, its head is in $D$, because each fact of $D$ is in some $\Delta$, and the next round of line L4 uses it. Now take a fact $f$ of $M$ that is not in $D$, and use induction on the height of its shortest derivation in $M$. If $f$ is stored, it is not in $E^-$, so it is in $E'$. Otherwise it is the head of an instance whose body facts have shorter derivations. None of them is in $D$, since $f$ would then be in $D$. By induction they are in $M'$, so $f$ is in $M'$. So $M \setminus D \subseteq M'$. The facts of $R$ and of the insert phase are heads of instances over facts that are already known to be in $M'$, so the final $M$ is a subset of $M'$.

For the converse, the final $M$ is closed under the rules. Take an instance that is true in the final $M$. If all its body facts are in $M \setminus D$, its head was in $M$; if the head is in $D$, line L7 puts it in $R$. Otherwise the instance has a body fact in $R \cup E^+$ or in a later $\Delta$, and the insert phase fires it. A set that contains $E'$ and is closed under the rules contains the least model $M'$. Both loops stop because $D$ and $M$ grow in each round and are bounded by finite sets. The full proof is in the proof file of this page.

## Complexity

Let $s$ be the number of rounds of the two loops, $r$ the number of rules, $k$ the largest body size, $v$ the largest number of variables in a rule, $n$ the number of constants and $F$ the size of the old and the new model.

- **Time.** Each round of a loop evaluates, for each rule and each body position, one join with that position over $\Delta$. With a hash index on each relation, one such search explores at most $k n^v$ partial instances, which gives $O(s r k^2 n^v)$ for the two loops, as for semi-naive evaluation. The rederive step searches, for each rule and each fact of $D$ that matches its head, the maps of the other variables; together this is at most $O(r k^2 n^v)$. The total is $O((s + 1) r k^2 n^v)$.
- **In practice.** The work is proportional to the number of rule instances that touch the overdeleted facts, not to the size of the model. But the overdeleted set can be the whole model even when the net change is one fact, as on the cycle above, or when a deleted edge is on many paths.
- **Space.** The sets $D$, $R$, $\Delta$ and $N$ hold at most $O(F)$ facts.

## Properties

- **Exact.** The result is the least model of the new stored facts, for any program without negation and any mix of insertions and deletions.
- **Recursion and cycles.** Unlike counting, DRed is correct for recursive programs, also when facts support each other through a cycle.
- **Phases match semi-naive evaluation.** Overdeletion and insertion are both semi-naive loops, so an engine that evaluates rules semi-naively can run DRed with the same join code.
- **Set semantics.** It keeps no count of derivations, only the facts.
- **Overdeletion can be large.** It removes facts that are still true and must then derive them again; this is the main cost.

## Variants and improvements

- **Counting for nonrecursive views.** In the same paper, Gupta, Mumick and Subrahmanian maintain nonrecursive views by storing with each derived fact the number of its derivations. A delta rule for each body position computes the change of the count, with sign $+1$ for an inserted and $-1$ for a deleted body fact. A fact leaves the view when its count reaches zero. Counting needs no rederivation, but it does not work for recursive views: on a cycle the number of derivations can be infinite, and facts that support each other would keep their counts.
- **Stratified negation.** The paper also handles stratified negation and aggregation: a deletion in a lower stratum is an insertion for the negated atoms of the next stratum, and the strata are maintained in order.
- **Backward and forward.** Later methods such as the backward/forward algorithm of Motik and others check each candidate fact for an alternative derivation before it is deleted, so that fewer true facts are overdeleted.
- **Provenance and support counts.** Systems that keep, for each fact, its derivation tree or a count of supports from lower strata reduce overdeletion further, at the cost of space.
- **Differential dataflow.** Dataflow engines keep the changes of each round of the fixpoint, indexed by round and by update, and correct the model with these differences instead of overdeleting.

## When to use it

Use DRed to keep a recursive materialized view, such as reachability or a points-to relation, up to date under small changes of the stored facts, when a new evaluation from the start is too slow. Use counting instead for nonrecursive views, where it needs no rederivation. When deletions often hit facts with many derivations, a method that checks alternative derivations first, or a provenance-based method, removes fewer facts.

## Pitfalls

- **Deleting derived facts directly.** Only stored facts can be deleted; a derived fact goes only when its derivations go. The implementation of this page rejects a deletion or insertion of an IDB fact.
- **Overdeleting over the new model.** Line L4 must use the old model $M$. Instances that were true before the update are the ones that may lose a body fact.
- **Rederiving with the deleted facts still present.** Line L7 must run after line L6; otherwise each fact rederives itself.
- **Stopping after the rederive step.** One rule step is not enough: a fact may need other rederived facts, as $p_{13}$ on the cycle. The insert phase brings them back.
- **A fact in both $E^-$ and $E^+$.** The update keeps it, so line L1 removes it from $E^-$.
- **Counting on recursive views.** It keeps facts that are no longer true when they support each other.

## Implementations

## History

Incremental maintenance of materialized views was studied from the mid-1980s, first for relational expressions with counts of derivations and for nonrecursive views. Gupta, Mumick and Subrahmanian gave DRed for recursive views and the counting algorithm for nonrecursive views at SIGMOD 1993. Gupta and Mumick surveyed the field in 1995. DRed became the standard method for deletions in Datalog engines that materialize their results, and later work by Motik and others improved its overdeletion.

## References
