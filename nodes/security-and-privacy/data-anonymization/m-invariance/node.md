---
tag: DJ2GGT
kind: definition
slug: m-invariance
name: m-invariance
aliases:
- m-invariant republication
area: security-and-privacy/data-anonymization
level: advanced
summary: A rule for republishing a changing table, which keeps the set of sensitive values of each record's group fixed across releases.
prereqs: [l-diversity, k-anonymity]
see_also: [l-diversity, k-anonymity, anatomy-bucketization, t-closeness, quasi-identifier, generalization-and-suppression, linkage-attack, differential-privacy-definition]
sources:
  - paper: doi:10.1145/1247480.1247556
    title: "Xiaokui Xiao and Yufei Tao, m-Invariance: towards privacy preserving re-publication of dynamic datasets, ACM SIGMOD International Conference on Management of Data (SIGMOD 2007), pages 689-700"
    locator: Section 1 (Tables 1 to 3, the attack that combines two releases, critical absence and counterfeits), Section 2 (Definitions 2 and 3, counterfeited generalization and the auxiliary relation R(j)), Section 3 (Definitions 13 to 17 and Lemmas 1 to 4) and Section 4.1 (m-eligibility and the four phases of the publishing algorithm)
  - paper: doi:10.1109/icde.2006.1
    title: "Ashwin Machanavajjhala, Johannes Gehrke, Daniel Kifer and Muthuramakrishnan Venkitasubramaniam, l-diversity: privacy beyond k-anonymity, 22nd International Conference on Data Engineering (ICDE 2006), page 24"
    locator: the l-diversity principle, which protects one release but not a sequence of releases
---

m-invariance is a privacy condition for a table that changes over time and is published again after each change, such as a hospital table that gains new patients and loses old ones every quarter. Each release can be [k-anonymous](/k-anonymity/) and [l-diverse](/l-diversity/) on its own and still disclose a sensitive value: an attacker who knows that a person is in two releases intersects the sets of sensitive values of the person's two groups, and the intersection can have one element. Xiao and Tao (SIGMOD 2007) showed this and defined $m$-invariance: every group has at least $m$ tuples with different sensitive values, and all groups that hold the same record over its lifetime have the same set of sensitive values. To make this possible when a value leaves the table, the publisher may add counterfeit tuples and must publish how many each group has. The number $m$ is a policy choice. The condition is a property of the sequence of published tables, under the attacker model of the paper.

## Definition

The publisher keeps a table $T$ with a [quasi-identifier](/quasi-identifier/) and one categorical sensitive attribute. At time $j$ the table is $T(j)$, and the publisher releases a generalized table $T^*(j)$ in which the tuples are split into QI groups, each with one generalized range on every quasi-identifier attribute. A record $t$ is in $T(x), \ldots, T(y)$ for a range $[x, y]$ called its **lifespan**.

**Counterfeited generalization** (Definitions 2 and 3 of the paper). A group of $T^*(j)$ may contain **counterfeit** tuples, which have a sensitive value but match no real record. Together with $T^*(j)$ the publisher releases an auxiliary table $R(j)$ that lists, for each group with counterfeits, the group ID and the number of counterfeits. The counts let an analyst correct aggregate results.

**Signature** (Definition 16). The signature of a QI group is the set of distinct sensitive values in it.

**Definition (Xiao and Tao, Definition 17).** A release $T^*(j)$ is **$m$-unique** if each QI group has at least $m$ tuples, counterfeits included, and all tuples in a group have different sensitive values. A sequence $T^*(1), \ldots, T^*(n)$ is **$m$-invariant** if

1. every $T^*(j)$ is $m$-unique, and
2. for every record $t$ with lifespan $[x, y]$, the groups that hold $t$ in $T^*(x), T^*(x+1), \ldots, T^*(y)$ all have the same signature.

$m$-uniqueness implies distinct $m$-diversity of each release, but not the other way round.

Results of the paper, each a theorem:

- **Lemma 1 (the attack).** For any generalization principle, if the intersection of the candidate sensitive sets of $t$ over its lifespan has one element, the attacker learns the value of $t$ with certainty. The candidate set of $t$ at time $j$ is the union of the signatures of all groups whose ranges cover the QI values of $t$.
- **Lemma 3 (the guarantee).** If the sequence is $m$-invariant, the disclosure risk of every record is at most $1/m$. The risk is the share of the reconstructions of the original tables, among those consistent with the releases and the attacker's knowledge, that give the true value; this is the paper's random-world model.
- **Lemma 4 (incremental).** If $T^*(1), \ldots, T^*(n-1)$ is $m$-invariant, adding $T^*(n)$ keeps it $m$-invariant if and only if $T^*(n)$ is $m$-unique and every record in both $T(n-1)$ and $T(n)$ has groups with the same signature in $T^*(n-1)$ and $T^*(n)$. The publisher needs only the last release.

The attacker model is strong on purpose (Definition 6). The attacker knows the identity, the exact QI values and the lifespan of every record, and the counterfeit counts. So the attacker knows which releases contain a person.

Condition 2 can be checked in one pass over the releases, with a map from each record to the signature of its first group. proofs/correctness.md proves that the check is exact, and proves Lemma 4 for this check.

```pseudo id=main
M-INVARIANT(T*(1), ..., T*(n), m)
L1  S ← an empty map from records to signatures
L2  for j ← 1 to n do
L3      for each QI group G of T*(j) do
L4          if |G| < m or two tuples of G share a sensitive value then return false
L5          σ ← the set of sensitive values in G
L6          for each record t in G that is not a counterfeit do
L7              if t is a key of S and S[t] ≠ σ then return false
L8              S[t] ← σ
L9  return true
```

With hashing, the check takes $O(N s)$ expected time, where $N$ is the number of tuples over all releases and $s$ is the largest group size.

**Publishing.** The paper's algorithm builds $T^*(n)$ from $T(n-1)$, $T(n)$ and $T^*(n-1)$ in four phases. Division puts each record that stays into a bucket by the signature of its old group. Balancing makes every value of a bucket's signature appear the same number of times, with new records where possible and counterfeits otherwise. Assignment places the new records into buckets, and split cuts each bucket into groups, one tuple per value of the signature. Publication is allowed only if the new records are $m$-eligible: at most $1/m$ of them share one sensitive value. The algorithm tries to use few counterfeits and small QI ranges; this is a heuristic aim, measured in the paper's experiments.

## Examples and non-examples

The example is small and made up, in the style of Tables 1 to 3 of the paper. Take $m = 2$, and suppose the QI ranges of different groups do not overlap, so the candidate set of each person is the signature of the person's own group. The first release is:

| group | records and sensitive values | signature |
|---|---|---|
| 1 | Bob: dyspepsia, Carol: bronchitis | {dyspepsia, bronchitis} |
| 2 | Dan: flu, Eve: gastritis | {flu, gastritis} |

Before the second release, Carol is deleted, and Frank (pneumonia) and Gina (flu) are inserted. The two new records have different values, so they are 2-eligible.

- **Non-example: a fresh 2-diverse release.** The publisher ignores the first release and forms groups $\{$Bob: dyspepsia, Eve: gastritis, Gina: flu$\}$ and $\{$Dan: flu, Frank: pneumonia$\}$. This release is 2-anonymous and 2-unique. But for Bob, $\{$dyspepsia, bronchitis$\} \cap \{$dyspepsia, gastritis, flu$\} = \{$dyspepsia$\}$, and for Dan, $\{$flu, gastritis$\} \cap \{$flu, pneumonia$\} = \{$flu$\}$. Both values are disclosed, as Lemma 1 says. The pair of releases is not 2-invariant.
- **Critical absence.** Bob's first group had the signature $\{$dyspepsia, bronchitis$\}$, and after Carol leaves no real record has bronchitis. So no release made only of real records can give Bob a group with that signature. The paper calls this critical absence.
- **Example: a 2-invariant second release.** The publisher adds one counterfeit $c_1$ with bronchitis:

| group | records and sensitive values | signature |
|---|---|---|
| 1 | Bob: dyspepsia, $c_1$: bronchitis | {dyspepsia, bronchitis} |
| 2 | Dan: flu, Eve: gastritis | {flu, gastritis} |
| 3 | Frank: pneumonia, Gina: flu | {pneumonia, flu} |

  and $R(2) = \{(1, 1)\}$: group 1 has one counterfeit. Every group has 2 tuples with different values, and Bob, Dan and Eve keep their signatures, so the pair is 2-invariant. The attacker who knows that Bob is in both releases still has two candidate values, and $R(2)$ says only that one tuple of group 1 is a counterfeit, not which one.
- **Not 3-invariant.** The same pair is not 3-invariant, since each group has only 2 tuples.
- **Non-example: keeping deleted records.** Keeping Carol's tuple in all later releases as if she had not left also keeps the signatures, but the published data then holds a record that is no longer in the table, and the paper notes that the guarantees of insertion-only methods become unclear when the attacker knows the deletion times.

## Related definitions

- [l-diversity](/l-diversity/) and [k-anonymity](/k-anonymity/): conditions on one release. Lemma 1 explains why they fail under republication: each constrains one candidate set, not the intersection of several.
- [t-closeness](/t-closeness/): another refinement of l-diversity for one release.
- [Anatomy](/anatomy-bucketization/): by the same authors, publishes groups without generalizing the quasi-identifiers. A group with one tuple per value of its signature is the same shape that m-invariance asks for.
- [Generalization and suppression](/generalization-and-suppression/): the operations that make the QI ranges. m-invariance adds a third operation, counterfeit tuples, with published counts.
- [Linkage attack](/linkage-attack/): here the attacker links a person to groups in several releases of the same table, not to a second dataset.
- [Differential privacy](/differential-privacy-definition/): a guarantee that does not depend on a model of the attacker's knowledge, at the cost of noise.

## References
