---
tag: 92B1R4
kind: algorithm
slug: r-swoosh
name: "R-Swoosh"
aliases:
- Swoosh algorithms
- generic entity resolution
area: databases/data-integration-and-cleaning
level: advanced
summary: "Resolve entities with black-box match and merge functions: merge each record with the first resolved record it matches and put the result back. Under the ICAR properties the output is exact."
solves: [entity-resolution]
model: word-ram
complexity:
  vars: {n: the number of input records}
  time: {worst: "O(n^2)", average: "O(n^2)", best: "O(n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, external: false, online: false, in_place: false, recursive: false}
history:
  year: 2009
  people: [Omar Benjelloun, Hector Garcia-Molina, David Menestrina, Qi Su, Steven Euijong Whang, Jennifer Widom]
  note: "Published in The VLDB Journal as part of a generic model of entity resolution in which match and merge are black boxes, together with G-Swoosh and F-Swoosh."
prereqs: [entity-resolution]
see_also: [sorted-neighborhood-method, entity-resolution-blocking, collective-entity-resolution, fellegi-sunter-model, transitive-closure, weighted-union-find, queue]
sources:
  - paper: doi:10.1007/s00778-008-0098-x
    title: "Omar Benjelloun, Hector Garcia-Molina, David Menestrina, Qi Su, Steven Euijong Whang and Jennifer Widom, Swoosh: a generic approach to entity resolution, The VLDB Journal 18(1), 2009, pages 255 to 276"
    locator: the generic model with match and merge functions, the ICAR properties and the domination order, and the algorithms G-Swoosh, R-Swoosh and F-Swoosh with their experiments
---

R-Swoosh is an algorithm for [entity resolution](/entity-resolution/) in which the match rule and the merge rule are black boxes. It keeps a list of resolved records. It takes the input records one by one, compares each with the resolved records, and at the first match it merges the two and puts the merged record back into the input. The merged record is compared again, so information from one record can join two others that did not match on their own. If the functions have the four ICAR properties (idempotence, commutativity, associativity and representativity), the output is exactly the set of maximal records of the merge closure. Methods such as the [sorted neighborhood method](/sorted-neighborhood-method/) and [blocking](/entity-resolution-blocking/) decide which pairs to compare and do not merge records; [collective entity resolution](/collective-entity-resolution/) also uses links between records.

## In plain words

You have a pile of records about people, and you can ask two questions about any two records: "are these the same person?" and "what is the combined record?". You keep a second pile of finished records. You take a record from the first pile and check it against the finished pile. If it matches one, you join the two, take the old one out of the finished pile, and put the joined record back on the first pile, because it now knows more and can match records that neither part matched. If it matches none, it goes on the finished pile. When the first pile is empty, the finished pile is the answer.

## The problem

The input is a finite set $I$ of $n$ records, a match function $\mathit{match}(r, s)$ that returns true or false, and a merge function $\mathit{merge}(r, s)$ that returns a new record for two matching records. Write $r \approx s$ for a match and $\langle r, s \rangle$ for the merge. The *merge closure* $\bar I$ is the smallest set that holds $I$ and every merge of two matching records in it. A record $r$ is *dominated* by $s$ if $r \approx s$ and $\langle r, s \rangle = s$: $s$ already holds all that $r$ adds. The result $ER(I)$ is the set of records of $\bar I$ that no other record of $\bar I$ dominates.

The ICAR properties are:

- **Idempotence.** $r \approx r$ and $\langle r, r \rangle = r$.
- **Commutativity.** $r \approx s$ if and only if $s \approx r$, and then $\langle r, s \rangle = \langle s, r \rangle$.
- **Associativity.** $\langle r, \langle s, t \rangle \rangle = \langle \langle r, s \rangle, t \rangle$ when both are defined.
- **Representativity.** If $u = \langle r, s \rangle$ and $r \approx t$, then $u \approx t$: a merged record matches everything its parts match.

A typical example is a record as a set of attribute values, merge as the union, and a match rule that asks for shared values, such as "the same email, or the same name and the same phone".

## The algorithm

```pseudo id=main
R-Swoosh(I, match, merge)
L1  R ← I;  R' ← ∅                          ▷ R: records to do, R': resolved records
L2  while R ≠ ∅ do
L3      r ← remove a record from R
L4      buddy ← nil
L5      for each s in R' do
L6          if match(r, s) then buddy ← s; exit the loop
L7      if buddy = nil then add r to R'
L8      else remove buddy from R'; add merge(r, buddy) to R
L9  return R'
```

Line L6 stops at the first match, so each step makes at most $|R'|$ calls. Line L8 drops both $r$ and its buddy: under ICAR the merged record dominates both, so they can never be needed again. The implementation keeps $R$ as a [queue](/queue/), so a merged record waits behind the records that are still to do, and keeps $R'$ as a list.

## Example

The rule is "the same email, or the same name and the same phone", and merge is the union of the values.

| record | name | phone | email |
|---|---|---|---|
| r1 | ann | p1 | |
| r2 | ann | | e1 |
| r3 | | p1 | e1 |
| r4 | bob | p1 | |

Of the 6 pairs, only r2 and r3 match. The [transitive closure](/transitive-closure/) of the pairs gives the clusters {r1}, {r2, r3} and {r4}. R-Swoosh runs as follows.

| step | taken from R | compared with | result | R' after |
|---|---|---|---|---|
| 1 | r1 | none | no match | r1 |
| 2 | r2 | r1 | no match | r1, r2 |
| 3 | r3 | r1, r2 | match r2: m = (ann, p1, e1) goes to R | r1 |
| 4 | r4 | r1 | no match | r1, r4 |
| 5 | m | r1 | match r1 (same name and phone): m' = (ann, p1, e1) from r1, r2, r3 goes to R | r4 |
| 6 | m' | r4 | no match | r4, m' |

The output is {r1, r2, r3} and {r4}, after 6 calls. The merged record of r2 and r3 has both a name and a phone, so it matches r1, which neither part matched. Record r4 shares the phone but not the name, so it stays apart.

**A larger run.** On generated data with 40 people and 108 records (119 true duplicate pairs, Python seed 42), with copies that lose their email or phone, R-Swoosh made 3488 calls (all pairs are 5778) and returned 46 clusters with pairwise precision 0.926 and recall 0.840. Precision is below 1 because some people share a name and a phone number. On this data the clusters were the same as the closure of the pairwise matches. These numbers are measurements on that data only.

## Correctness

Each step either moves a record to $R'$ or merges it, so $R'$ never holds two records that match. The merge of two records dominates both of them, and domination is a partial order under ICAR. From these facts, every input record is dominated by an output record. The set of records dominated by an output record is also closed under merges, so it covers all of $\bar I$. Since no two output records match, each one is maximal. So under ICAR the output is exactly $ER(I)$, for any order of the input. Without the properties the output can be wrong, and the paper gives G-Swoosh for that case. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Calls.** There are exactly $n$ steps without a match and $n - j$ merge steps, where $j$ is the size of the output. The number of match calls is at most $(n - 1)^2 - (j - 1)(j - 2)/2$, so at most $(n - 1)^2$. With no matches it is exactly $n(n-1)/2$.
- **Best case.** If every record matches the first resolved record, each step makes at most one call, about $2n$ in total.
- **Time.** The calls times the cost of one call to $\mathit{match}$, plus $n - j$ calls to $\mathit{merge}$. In practice the match rule is the main cost.
- **Space.** At most $n$ records in $R$ and $R'$ together, but a merged record can be as large as all its parts.

## Properties

- **Exact under ICAR.** The output equals $ER(I)$ when the four properties hold. It is a heuristic when they do not.
- **Order independent result.** The output does not depend on the input order, but the number of calls does.
- **No transitive closure needed.** Merging replaces the closure step of pairwise methods, and it can join more records than the closure of the pairs.
- **Black box.** It needs nothing about the records except the two functions. It does not build an index, so it compares more pairs than blocking methods.

## Variants and improvements

- **G-Swoosh.** Makes no assumption on the functions. It compares all pairs of records, merged ones included, keeps the source records, and removes dominated records at the end. It can make many more calls.
- **F-Swoosh.** Assumes the match rule is a disjunction of feature comparisons. It records the feature values already compared, so a merged record does not repeat comparisons that failed before.
- **With blocking.** On large data, R-Swoosh runs inside each block of a [blocking](/entity-resolution-blocking/) or sorted neighborhood pass, which cuts the quadratic cost.

## When to use it

Use it when you have a reliable match rule and a merge that keeps all information, such as the union of attribute values, and want merged records instead of clusters of pairs. It suits small or blocked inputs, because its cost is quadratic. When the match rule gives a score instead of a yes or no, a probabilistic model such as [Fellegi-Sunter](/fellegi-sunter-model/) decides the pairs, and a closure with [union-find](/weighted-union-find/) groups them.

## Pitfalls

- **A merge that loses values.** If merge keeps only one of two values, for example the longer name, representativity can fail, and a record that matched a part no longer matches the merged record.
- **Rules with thresholds.** A rule such as "similarity at least 0.8" on a merged record is often not representative, because the merged value can be farther from a third record than one of its parts.
- **Idempotence of the rule.** A record must match itself. With the rule of the example, a record with no email and no phone does not, so the theory does not cover it.
- **Large merged records.** Each merge makes a larger record, and the cost of a match grows with it.

## Implementations

## History

Benjelloun, Garcia-Molina, Menestrina, Su, Whang and Widom of the Stanford InfoLab described the generic model of entity resolution and the Swoosh family of algorithms in The VLDB Journal in 2009. The model treats match and merge as black boxes given by a domain expert and asks which properties of these functions make the result well defined and the algorithms efficient. The paper defines the ICAR properties, the domination order and the result $ER(I)$, and gives G-Swoosh for arbitrary functions, R-Swoosh for ICAR functions and F-Swoosh for feature-level rules. It also compares the algorithms in experiments on real data.

## References
