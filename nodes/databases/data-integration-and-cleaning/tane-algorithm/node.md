---
tag: HRXFKG
kind: algorithm
slug: tane-algorithm
name: TANE
aliases:
- TANE algorithm
area: databases/data-integration-and-cleaning
level: advanced
summary: "Find all minimal functional dependencies of a relation by a levelwise search over attribute sets. Stripped partitions test each candidate, and candidate sets and keys prune the search."
solves: [functional-dependency-discovery]
model: word-ram
complexity:
  vars: {n: the number of tuples, m: the number of attributes, s: the number of attribute sets in all levels, q: the number of superkeys met in the search}
  time: {worst: "O((n + m^2.5) 2^m)", average: "O(s (n + m^2) + q m^3)", best: "O(m n + m^3)"}
  space: {extra: "O((n + m) 2^m / sqrt(m))"}
properties: {deterministic: true, exact: true, external: false, online: false, in_place: false, recursive: false}
history:
  year: 1998
  people: [Yka Huhtala, Juha Kärkkäinen, Pasi Porkka, Hannu Toivonen]
  note: "Presented at ICDE 1998 and published in full in The Computer Journal in 1999. It replaced tests on tuple pairs by counts of partition classes and was much faster than the earlier methods on benchmark data."
prereqs: [functional-dependency, functional-dependency-discovery]
see_also: [candidate-key, attribute-closure-algorithm, armstrongs-axioms, normalization, conditional-functional-dependency, denial-constraint]
sources:
  - paper: "Yka Huhtala, Juha Kärkkäinen, Pasi Porkka and Hannu Toivonen, TANE: an efficient algorithm for discovering functional and approximate dependencies, The Computer Journal 42(2), 1999, pages 100 to 111"
    locator: "Section 2 (partitions, Lemmas 2.1 and 2.2), Section 3 (the sets C+, key pruning, stripped partitions and Lemma 3.5), Section 4 (the algorithm, Lemmas 4.1 and 4.2, the stripped product and the approximate version in Section 4.6), Section 5.1 (worst case analysis, Theorem 5.1)"
  - paper: "Yka Huhtala, Juha Kärkkäinen, Pasi Porkka and Hannu Toivonen, Efficient discovery of functional and approximate dependencies using partitions, Proceedings of the 14th International Conference on Data Engineering (ICDE), 1998, pages 392 to 401"
    locator: the first version of the algorithm
  - paper: "Thorsten Papenbrock, Jens Ehrlich, Jannik Marten, Tommy Neubert, Jan-Peer Rudolph, Martin Schönberg, Jakob Zwiener and Felix Naumann, Functional dependency discovery: an experimental evaluation of seven algorithms, PVLDB 8(10), 2015, pages 1082 to 1093"
    locator: the description of TANE and the measured run times and memory use of the seven algorithms
---

TANE finds all minimal [functional dependencies](/functional-dependency/) $X \to A$ that hold in one relation instance. It visits the attribute sets level by level, from small sets to large ones, as on the lattice of all subsets. For each set $X$ it keeps the *stripped partition* of the tuples by their values on $X$, and $X \setminus \{A\} \to A$ holds exactly when the partitions of $X \setminus \{A\}$ and $X$ have the same number of classes. Sets of *right-hand side candidates* $C^+(X)$ and *key pruning* cut the levels. The page [functional dependency discovery](/functional-dependency-discovery/) states the problem and compares TANE with the methods that work from pairs of rows. TANE is the levelwise method: its time is linear in the number of tuples and exponential in the number of attributes.

## In plain words

You have a table and you want every rule of the form "these columns decide that column". TANE starts with single columns, then pairs, then triples. For each group of columns it sorts the rows into piles, with one pile for each combination of values. If adding a column to a group does not split any pile, the group decides that column. It throws away piles with one row, because they can never break a rule. It also stops growing a group when nothing useful can come from it: when the group already decides every column, or when no column is left that could still give a new, shortest rule. Each rule it reports is as short as possible, and it reports each one once.

## The problem

The input is a relation $r$ with $n$ tuples over a set $R$ of $m$ attributes, under set semantics, with no nulls. The output is every non-trivial dependency $X \to A$ ($A \notin X$) that holds in $r$ and is *minimal*: no proper subset of $X$ determines $A$. The output can have size exponential in $m$, as shown on the [problem page](/functional-dependency-discovery/), so no method is polynomial in $m$ in the worst case.

**Partitions.** Two tuples are *equivalent on $X$* if they agree on every attribute of $X$. The classes of this relation form the partition $\pi_X$. The *stripped* partition $\hat\pi_X$ drops the classes of size 1. Write $\|\hat\pi_X\|$ for the number of tuples in its classes and $e(X) = \|\hat\pi_X\| - |\hat\pi_X|$. The paper divides $e(X)$ by $n$; the integer form used here also works for $n = 0$. The test is Lemma 3.5 of Huhtala et al.: $X \to A$ holds if and only if $e(X) = e(X \cup \{A\})$. $X$ is a *superkey* if and only if $e(X) = 0$.

**Candidates.** For a set $X$,
$$C^+(X) = \{ A \in R : X \setminus \{A, B\} \to B \text{ fails for every } B \in X \}.$$
If $X \setminus \{A\} \to A$ holds, it is minimal if and only if $A \in C^+(X \setminus \{B\})$ for every $B \in X$ (Lemma 3.1). $C^+$ can only shrink as $X$ grows.

## The algorithm

```pseudo id=main
TANE(r, R)
L1  L_0 ← {∅}; C+(∅) ← R; the partition of ∅ has one class with all tuples
L2  L_1 ← {{A} : A ∈ R}, with the stripped partition of each {A} read from r
L3  ℓ ← 1
L4  while L_ℓ ≠ ∅ do
L5      COMPUTE-DEPENDENCIES(L_ℓ)
L6      PRUNE(L_ℓ)
L7      L_(ℓ+1) ← GENERATE-NEXT-LEVEL(L_ℓ); ℓ ← ℓ + 1

COMPUTE-DEPENDENCIES(L_ℓ)
L8  for each X ∈ L_ℓ do C+(X) ← the intersection of C+(X \ {A}) over all A ∈ X
L9  for each X ∈ L_ℓ and each A ∈ X ∩ C+(X) do
L10     if e(X \ {A}) = e(X) then                       ▷ X \ {A} → A holds
L11         output X \ {A} → A
L12         remove A and every B ∈ R \ X from C+(X)

PRUNE(L_ℓ)
L13 for each X ∈ L_ℓ do
L14     if C+(X) = ∅ then delete X from L_ℓ
L15     else if e(X) = 0 then                           ▷ X is a superkey
L16         for each A ∈ C+(X) \ X with A ∈ C+(X ∪ {A} \ {B}) for all B ∈ X do output X → A
L17         delete X from L_ℓ

GENERATE-NEXT-LEVEL(L_ℓ)
L18 for each pair Y, Z ∈ L_ℓ that differ only in their last attribute do
L19     X ← Y ∪ Z; if X \ {A} ∈ L_ℓ for every A ∈ X then add X to L_(ℓ+1), with partition(Y) · partition(Z)
```

Line L8 starts $C^+(X)$ from its subsets. Line L10 tests one candidate with two numbers. Line L12 has two parts: $A$ leaves because $X \setminus \{A\} \to A$ is now known, and every attribute outside $X$ leaves because a larger left side that holds $X$ cannot be minimal for it (Lemma 3.2). Line L14 drops a set with no candidates, since no superset can give a new dependency. Lines L15 to L17 are *key pruning*: every superset of a superkey is a superkey and gives only non-minimal dependencies, so $X$ is deleted, and the dependencies $X \to A$ that the next level would have found are output at once. Line L19 is the *stripped product*: it builds $\hat\pi_X$ from the two parents in time linear in their size, with one table of $n$ entries. The test in line L16 reads $C^+(X \cup \{A\} \setminus \{B\})$; when that set was never made, the code tests $X \setminus \{B\} \to A$ directly, as explained under Pitfalls.

## Example

The relation has 5 tuples over $A, B, C, D$.

| tuple | A | B | C | D |
|---|---|---|---|---|
| t1 | 1 | a | x | 1 |
| t2 | 1 | a | y | 2 |
| t3 | 2 | b | x | 1 |
| t4 | 2 | b | y | 3 |
| t5 | 3 | b | x | 1 |

The stripped partitions of level 1 are $\hat\pi_A = \{\{1,2\},\{3,4\}\}$, $\hat\pi_B = \{\{1,2\},\{3,4,5\}\}$, $\hat\pi_C = \{\{1,3,5\},\{2,4\}\}$ and $\hat\pi_D = \{\{1,3,5\}\}$, so $e = 2, 3, 3, 2$, and $e(\emptyset) = 4$. No column is constant, so level 1 finds nothing, and no single attribute is a key.

| level | set | e | dependency at L10 | C+ after L12 | PRUNE |
|---|---|---|---|---|---|
| 2 | AB | 2 | $A \to B$, since $e(A) = 2$ | {A} | kept |
| 2 | AC | 0 | none | {A, B, C, D} | superkey: output $AC \to D$, delete |
| 2 | AD | 0 | none | {A, B, C, D} | superkey: no output, delete |
| 2 | BC | 1 | none | {A, B, C, D} | kept |
| 2 | BD | 1 | none | {A, B, C, D} | kept |
| 2 | CD | 2 | $D \to C$, since $e(D) = 2$ | {D} | kept |
| 3 | BCD | 1 | $BC \to D$, since $e(BC) = 1$ | {} | delete |

At the superkey $AC$, line L16 accepts $D$ because $D \in C^+(CD)$ and $D \in C^+(AD)$, and rejects $B$ because $B \notin C^+(AB)$: $A \to B$ already holds. At $AD$ it rejects $B$ for the same reason and $C$ because $C \notin C^+(CD)$. Level 3 is made from the kept sets $AB, BC, BD, CD$: only $BC$ and $BD$ share a prefix, and the three subsets of $BCD$ are all kept. $C^+(BCD) = \{D\}$, so only $BC \to D$ is tested. The output is $A \to B$, $D \to C$, $AC \to D$ and $BC \to D$, and the run handles 12 of the 16 attribute sets.

## Correctness

The main fact is that the stored $C^+(X)$ is exactly the set of the definition for every set that the run handles: line L8 gives the part that comes from the subsets, and lines L9 to L12 remove the rest. With this, an output at line L11 is minimal because no $X \setminus \{A, B\}$ determines $A$, and an output at line L16 is minimal because no $X \setminus \{B\}$ does. A minimal $Y \to A$ is found at line L11 on $Y \cup \{A\}$ unless some subset is a superkey; then $Y$ itself is a key, and line L16 finds it there. Lemmas 4.1 and 4.2 of the paper state these two parts. The full proof, for the version with the direct test in line L16, is in [the proof page](proofs/correctness.md).

## Complexity

The analysis is that of Section 5.1 of the paper, on a [word RAM](/word-ram/). Let $s$ be the number of sets in all levels and $q$ the number of superkeys met.

- **Partitions.** Each of the $s$ sets gets one stripped product, $O(n)$ each, so $O(s n)$.
- **Lattice work.** Lines L8, L16 and L19 look up $O(m)$ neighbours of each set, and each lookup costs $O(m)$. This gives $O(s m^2 + q m^3)$.
- **Total.** $O(s (n + m^2) + q m^3)$. The levels hold at most $2^m$ sets, and the largest level at most $O(2^m / \sqrt{m})$, which gives Theorem 5.1: time $O((n + m^{2.5}) 2^m)$ and space $O((n + m) 2^m / \sqrt{m})$. The space bound holds because only two levels and their partitions are kept at a time.
- **Best case.** If every attribute is a key, all of level 1 is deleted, and the run costs $O(m n + m^3)$.

For a fixed set of dependencies the time is linear in $n$. The exponential factor in $m$ cannot be removed in general, because the output itself can be that large.

## Properties

- **Exact and complete.** It returns all minimal dependencies and nothing else, each once.
- **Linear in the tuples.** Each validity test is a comparison of two integers, after the partitions are built.
- **Memory bound.** It keeps two levels of partitions. On wide relations the middle levels are the limit, not the time.
- **Approximate dependencies.** The same search finds dependencies with a small *g3 error*, the least fraction of tuples to delete so that the dependency holds (Kivinen and Mannila's measure).

## Variants and improvements

- **Approximate TANE.** Section 4.6 of the paper changes line L10 to $e(X \setminus \{A\} \to A) \le \varepsilon$, and runs the second part of line L12 only when the dependency holds exactly. The g3 error comes from $\hat\pi_{X \setminus \{A\}}$ and $\hat\pi_X$ in linear time: for each class of the first, keep its largest subclass in the second. The bounds $e(X) - e(X \cup \{A\}) \le e(X \to A) \le e(X)$ often decide the test without that pass. Key pruning must be off in this version (see Pitfalls).
- **Other lattice methods.** FUN and FD_Mine also walk the lattice level by level, with other pruning rules. DFD walks it depth first with random walks.
- **Row-based methods.** Dep-Miner and FastFDs compute the *agree sets* of all pairs of tuples and derive the dependencies from them, and FDEP induces them from the pairs that disagree. They are quadratic in $n$ but less sensitive to $m$. Papenbrock et al. (2015) measured all seven on the same data sets.
- **Related constraints.** [Conditional functional dependencies](/conditional-functional-dependency/) and [denial constraints](/denial-constraint/) are found by extensions of the same lattice and agree-set ideas.

## When to use it

Use it to profile a table with many rows and few columns, to find candidate [keys](/candidate-key/) and dependencies before [normalization](/normalization/) or data cleaning. For wide tables with few rows, a row-based method is usually faster. Each result is a fact about this one instance, not about the schema: a dependency can hold by chance, so a human or a domain rule has to confirm it before it becomes a constraint.

## Pitfalls

- **A missing neighbour in line L16.** The set $X \cup \{A\} \setminus \{B\}$ may never have been made, because one of its subsets was deleted as a superkey. Reading a missing set as an empty $C^+$ loses dependencies. For a superkey $X$ and $A \notin X$, $A \in C^+(X \cup \{A\} \setminus \{B\})$ if and only if $X \setminus \{B\} \to A$ fails, so the code tests that directly when the set is missing.
- **Key pruning with approximate dependencies.** Key pruning is safe only for exact dependencies. Take the tuples $(1, 0), (0, 0), (2, 2)$ over $A, B$ and $\varepsilon = 1/3$. $\{A\}$ is a key, so key pruning deletes it at level 1, the set $\{A, B\}$ is never made, and the minimal approximate dependency $B \to A$ (delete one tuple) is lost. The paper changes only lines L10 and L12 for this version; the implementation here also switches key pruning off.
- **Stale $C^+$.** Line L9 must use the value of line L8 for the whole loop on $X$, and line L12 must not remove attributes of $X$ other than $A$. Otherwise some candidates are never tested.
- **Dividing by $n$.** With the fraction $e(X)/n$ an empty relation divides by zero. The integer form avoids this, and with $n \le 1$ every attribute is constant, so every $\emptyset \to A$ holds.
- **Reading the output as constraints.** On a sample, many dependencies hold only by chance. The output describes the instance.

## Implementations

## History

Mannila and Räihä studied the inference of functional dependencies from relations in the 1980s and showed that the number of minimal dependencies can be exponential in the number of attributes. Huhtala, Kärkkäinen, Porkka and Toivonen presented TANE at ICDE in 1998 and the full version in The Computer Journal in 1999. Its small-to-large search follows the levelwise search that Mannila and Toivonen described for data mining tasks, and its tests with partitions gave speed-ups of several orders of magnitude over earlier published run times on benchmark data. The 2015 study of Papenbrock et al. reimplemented TANE with six other algorithms on common data sets and compared their run times and memory use.

## References
