---
tag: Y4WDK2
kind: algorithm
slug: anatomy-bucketization
name: Anatomy
aliases:
- bucketization
area: security-and-privacy/data-anonymization
level: advanced
summary: Releases quasi-identifiers and sensitive values in two tables linked only by group id, with l-diverse groups and no generalization.
model: word-ram
complexity:
  vars: {n: the number of tuples, l: the diversity parameter, m: the number of distinct sensitive values}
  time: {worst: O(n log m)}
  space: {extra: O(n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2006
  people: [Xiaokui Xiao, Yufei Tao]
  note: Xiao and Tao proposed anatomy at VLDB 2006 as an alternative to generalization that keeps the exact quasi-identifier values and still bounds the breach probability by 1/l.
prereqs: [l-diversity, quasi-identifier, k-anonymity]
see_also: [l-diversity, t-closeness, m-invariance, generalization-and-suppression, mondrian-anonymization, linkage-attack, k-anonymity, differential-privacy-definition]
sources:
  - url: "https://www.cse.cuhk.edu.hk/~taoyf/paper/vldb06.pdf"
    title: "Xiaokui Xiao and Yufei Tao, Anatomy: simple and effective privacy preservation, 32nd International Conference on Very Large Data Bases (VLDB 2006), pages 139-150"
    locator: Section 3 (Definitions 2 and 3, Lemma 1, Corollary 1 and Theorem 1 on the breach probability 1/l, and the assumptions A1 and A2), Section 4 (the reconstruction error), Section 5.1 (Theorem 2), Section 5.2 (Figure 3 and Properties 1 to 3) and Section 5.3 (Theorems 3 and 4)
  - paper: doi:10.1145/1559845.1559861
    title: "Daniel Kifer, Attacks on privacy and deFinetti's theorem, ACM SIGMOD 2009, pages 127-138"
    locator: the attack that learns the correlation between quasi-identifiers and sensitive values from an anatomized release and uses it against single records
  - paper: doi:10.1109/icde.2006.1
    title: "Ashwin Machanavajjhala, Johannes Gehrke, Daniel Kifer and Muthuramakrishnan Venkitasubramaniam, l-diversity: privacy beyond k-anonymity, ICDE 2006, page 24"
    locator: the l-diversity principle that anatomy enforces on each group
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing: a survey of recent developments, ACM Computing Surveys 42(4), article 14, 2010"
    locator: the anonymization operations, where anatomy is compared with generalization, suppression and perturbation
---

Anatomy publishes a table with a sensitive attribute as two tables. The quasi-identifier table (QIT) holds the exact quasi-identifier values of each tuple and a group id. The sensitive table (ST) holds, for each group, the sensitive values and their counts. Nothing joins a tuple to its own sensitive value except the group id, and each group holds at least $l$ tuples with distinct sensitive values. Xiao and Tao (VLDB 2006) proved that an attacker who knows a person's quasi-identifier values and knows that the person is in the table then guesses the person's sensitive value with probability at most $1/l$, the same as for an [l-diverse](/l-diversity/) generalized table. But no value is coarsened, so aggregate queries that mix quasi-identifiers and the sensitive attribute are much more accurate. Their algorithm Anatomize builds the groups in $O(n \log m)$ time in the word-RAM model, and its reconstruction error is within a factor $1 + 1/n$ of the lowest possible. The value of $l$ is a policy choice.

## In plain words

A hospital wants to publish patient ages and ZIP codes, and also the diseases, without letting anyone link a patient to a disease. Generalization would blur the ages into ranges. Anatomy keeps them exact.

It puts the patients into small groups, and each group must have different diseases. It then publishes two lists. The first list gives each patient's age and ZIP code and the number of the group. The second list gives, for each group number, the diseases in the group, but not who has which one.

If a group has three patients with three different diseases, a neighbour who finds a patient in the first list only learns that the patient has one of three diseases. The groups are formed by taking one patient from each of the most common diseases at a time, so that no disease is left over at the end.

## The problem

The input is a table $T$ of $n$ tuples with quasi-identifier attributes $A_1, \ldots, A_d$ and one categorical sensitive attribute $A^s$, and an integer $l \ge 1$. A partition of $T$ into groups $G_1, \ldots, G_g$ is **l-diverse** if in each group $G_j$, the most frequent sensitive value $v$ has $c_j(v) / |G_j| \le 1/l$ (Definition 2 of the paper). The output is the QIT, with one row $(t[A_1], \ldots, t[A_d], j)$ for each tuple $t$ in group $j$, and the ST, with one row $(j, v, c_j(v))$ for each group $j$ and each value $v$ in it (Definition 3).

An l-diverse partition exists if and only if at most $n/l$ tuples share a sensitive value; the paper calls this the eligibility condition. It is necessary because each group can hold at most $|G_j|/l$ tuples of a value, and these numbers add up to at most $n/l$. The algorithm below shows that it is also sufficient.

The quality measure of the paper is the reconstruction error. For a tuple $t$ with value $v_h$ in group $G$, $Err_t = (1 - c(v_h)/|G|)^2 + \sum_{h' \ne h} c(v_{h'})^2 / |G|^2$, the squared distance between the true point of $t$ and the distribution that the release gives for it, and $RCE = \sum_t Err_t$. Theorem 2 of the paper proves $RCE \ge n (1 - 1/l)$ for every l-diverse partition.

## The algorithm

```pseudo id=main
ANATOMIZE(T, l)                  ▷ at most n/l tuples of T share a sensitive value
L1  QIT ← ∅, ST ← ∅, g ← 0
L2  hash the tuples of T into buckets by their sensitive value
L3  while at least l buckets are non-empty do
L4      g ← g + 1, G_g ← ∅
L5      S ← the l buckets that hold the most tuples
L6      for each bucket B in S do
L7          remove one tuple from B and add it to G_g
L8  for each non-empty bucket B do          ▷ B holds exactly one tuple
L9      t ← the tuple of B
L10     S' ← the groups that hold no tuple with the sensitive value of t
L11     add t to one group of S'
L12 for j ← 1 to g do
L13     for each tuple t of G_j, insert (t[A_1], ..., t[A_d], j) into QIT
L14     for each distinct value v in G_j, insert (j, v, c_j(v)) into ST
L15 return QIT, ST
```

Lines L3 to L7 are the group creation phase. Each iteration takes one tuple from each of the $l$ largest buckets, so each new group has exactly $l$ tuples with $l$ distinct values. The phase stops when fewer than $l$ buckets are non-empty. Lines L8 to L11 are the residue phase. The eligibility condition guarantees two facts that the paper proves as Properties 1 and 2: at the end of the first phase each non-empty bucket holds exactly one tuple, and each such residue tuple has a group without its value. Lines L12 to L14 write the two tables.

The paper removes "an arbitrary tuple" at line L7 and picks "a random group" at line L11; both choices are free. The code takes the oldest tuple of each bucket, breaks ties between buckets of the same size by the first appearance of their value, and puts a residue tuple into the first group of $S'$. Within each group, it writes the QIT rows and the ST rows in sorted order, so that the order of the rows says nothing about which tuple has which value (see Pitfalls).

## Example

Take seven synthetic tuples with $l = 2$. Age and ZIP code are the quasi-identifiers and the disease is sensitive. Flu occurs 3 times, and $3 \le 7/2$, so the table is eligible.

| tuple | Age | ZIP | disease |
|---|---|---|---|
| $t_1$ | 23 | 11001 | flu |
| $t_2$ | 27 | 11002 | gastritis |
| $t_3$ | 35 | 11005 | flu |
| $t_4$ | 59 | 12001 | dyspepsia |
| $t_5$ | 61 | 12003 | flu |
| $t_6$ | 65 | 12004 | gastritis |
| $t_7$ | 70 | 12007 | pneumonia |

Line L2 makes four buckets. Ties of size go to the value that appears first in the table.

| step | buckets before the step (flu, gastritis, dyspepsia, pneumonia) | the $l$ largest | new group |
|---|---|---|---|
| iteration 1 | $\{t_1, t_3, t_5\}$, $\{t_2, t_6\}$, $\{t_4\}$, $\{t_7\}$ | flu, gastritis | $G_1 = \{t_1, t_2\}$ |
| iteration 2 | $\{t_3, t_5\}$, $\{t_6\}$, $\{t_4\}$, $\{t_7\}$ | flu, gastritis | $G_2 = \{t_3, t_6\}$ |
| iteration 3 | $\{t_5\}$, $\emptyset$, $\{t_4\}$, $\{t_7\}$ | flu, dyspepsia | $G_3 = \{t_5, t_4\}$ |
| residue | $\emptyset$, $\emptyset$, $\emptyset$, $\{t_7\}$ | one bucket left, $1 < l$ | $t_7$ goes to $G_1$, which has no pneumonia |

The release is the two tables below.

| Age | ZIP | group |
|---|---|---|
| 23 | 11001 | 1 |
| 27 | 11002 | 1 |
| 70 | 12007 | 1 |
| 35 | 11005 | 2 |
| 65 | 12004 | 2 |
| 59 | 12001 | 3 |
| 61 | 12003 | 3 |

| group | disease | count |
|---|---|---|
| 1 | flu | 1 |
| 1 | gastritis | 1 |
| 1 | pneumonia | 1 |
| 2 | flu | 1 |
| 2 | gastritis | 1 |
| 3 | dyspepsia | 1 |
| 3 | flu | 1 |

An attacker who knows that a person aged 23 in ZIP 11001 is in the table finds group 1, and learns only that the person has flu, gastritis or pneumonia, each with probability $1/3 \le 1/2$. A researcher still sees the exact ages. Each tuple is alone with its value in its group, so $Err_t = 1 - 1/|G|$, and $RCE = 3 \cdot \tfrac23 + 4 \cdot \tfrac12 = 4$. The lower bound is $7 (1 - \tfrac12) = 3.5$, and $4 / 3.5 = 8/7 = 1 + 1/n$, the worst case of Theorem 4.

## Correctness

Let $R$ be the number of tuples left in the buckets, $c_1$ the size of the largest bucket and $j$ the number of buckets of that size. The group creation phase keeps the invariant: either $c_1 \le 1$, or $R - j \ge l (c_1 - 1)$. At the start, it follows from the eligibility condition $l c_1 \le n$. When the phase stops, $N < l$ buckets are non-empty, and $R \le j c_1 + (N - j)(c_1 - 1)$ gives $R - j \le N (c_1 - 1)$. With $c_1 \ge 2$ this is less than $l (c_1 - 1)$, against the invariant. So each bucket holds at most one tuple (Property 1). The first phase makes $g = \lfloor n/l \rfloor$ groups. A residue value $v$ occurs at most $\lfloor n/l \rfloor$ times in $T$, and one of these occurrences is the residue tuple, so at most $g - 1$ groups hold $v$ and $S'$ is not empty (Property 2). Each group then has at least $l$ tuples, all with distinct values (Property 3), so $c_j(v)/|G_j| \le 1/|G_j| \le 1/l$. The full proof is in proofs/correctness.md.

The privacy claim is a theorem of the paper (Lemma 1, Corollary 1 and Theorem 1): if the attacker knows the quasi-identifier values of a person and that the person is in $T$, and treats each assignment of the values of a group to its tuples as equally likely, then the probability that the person has value $v$ is $c_j(v) / |G_j| \le 1/l$.

## Complexity

The model is the word-RAM, with the sensitive values hashed in $O(1)$ expected time.

- Line L2 takes $O(n)$ expected time.
- The code keeps the non-empty buckets in a binary heap keyed by size. Each of the $\lfloor n/l \rfloor$ iterations pops $l$ buckets and pushes back at most $l$, at $O(\log m)$ each, so the first phase takes $O(n \log m)$ time.
- At most $l - 1$ residue tuples exist, and each scans at most $g = \lfloor n/l \rfloor$ groups with a set of values per group, so the residue phase takes $O(n)$ time.
- Lines L12 to L14 take $O(n)$ time, or $O(n \log n)$ with the sorting of rows inside each group.
- The extra space is $O(n)$ for the groups.

In external memory, Theorem 3 of the paper shows $O(n/b)$ I/Os and $O(m)$ memory for a page size $b$: the bucket sizes fit in memory, and the groups are written out in the order they are made. Theorem 4 bounds the quality: if $l$ divides $n$, then $RCE = n(1 - 1/l)$, the lower bound; otherwise $RCE$ is at most $1 + 1/n$ times the lower bound. With all counts 1, $RCE = \sum_j (|G_j| - 1) = n - \lfloor n/l \rfloor$, whatever group each residue tuple joins.

## Properties

- **No generalization.** The quasi-identifier values are published exactly. The privacy comes from cutting the link between the QIT row and the ST row.
- **Groups of size $l$ or slightly more.** Each group has $l$ tuples, and at most $l - 1$ groups receive one or more residue tuples.
- **Deterministic as coded.** The paper allows any choice at lines L7 and L11; the guarantee holds for every choice.
- **Membership is not hidden.** The QIT shows the exact quasi-identifier values of everyone in the table, so an attacker learns who is in it. A generalized table can hide this when the attacker does not know who is in the table, which the paper discusses as its assumption A2.

## Variants and improvements

- **Other diversity rules per group.** Lines L3 to L7 make each group distinct $l$-diverse with one tuple per value, which also meets the entropy and recursive forms of [l-diversity](/l-diversity/). A group rule based on [t-closeness](/t-closeness/) needs a different grouping step.
- **Republication.** When the table changes and is released again, each release can be l-diverse and the sequence can still leak. [m-invariance](/m-invariance/) is the fix of Xiao and Tao for that case; it uses the same group and signature idea.
- **More than two tables.** Later work cuts the attributes into more than two column groups, each released with a group id, so that correlated quasi-identifiers stay together.
- **The same format with a generalized QIT.** Some systems combine a coarse generalization of the quasi-identifiers with a separate sensitive table, to hide membership as well.

## When to use it

Use anatomy when analysts need the exact quasi-identifier values, for example to run range queries or to fit a model on age and ZIP code together with the sensitive attribute, and when publishing who is in the table is acceptable. If membership itself is sensitive, use a [generalization](/generalization-and-suppression/) such as [Mondrian](/mondrian-anonymization/), or a [differentially private](/differential-privacy-definition/) release. If the attacker may learn the correlation between quasi-identifiers and the sensitive value from the release itself, the $1/l$ bound does not hold, as the next section explains.

## Pitfalls

- **Taking any $l$ buckets at line L5.** If line L5 takes $l$ non-empty buckets that are not the largest, values can be stranded. With the values $a, a, b, c$ and $l = 2$ (eligible, since $2 \le 4/2$), the group $\{b, c\}$ leaves the bucket $\{a, a\}$, and the second $a$ has no group without $a$. Line L5 must take the $l$ largest buckets.
- **Placing a residue tuple anywhere at line L11.** A residue tuple put into a group that already has its value makes that value occur twice in a group of $l + 1$ tuples, and $2/(l + 1) > 1/l$ for $l > 1$. Line L10 must restrict the choice to groups without the value.
- **Leaking through row order at lines L13 and L14.** If the QIT rows of a group are written in the same order as the ST rows, for example both in the order in which line L7 picked the tuples, then the $i$-th row of one table matches the $i$-th row of the other, and the release links every person to a value. Write each group's rows in an order that does not depend on the link, such as sorted by value.
- **Skipping the eligibility test.** If more than $n/l$ tuples share a value, no l-diverse partition exists. Without the test, the loop of line L3 ends with a bucket of two or more tuples, and line L11 fails. Test first, and suppress tuples of the frequent value or lower $l$.
- **Trusting $1/l$ against a learning attacker.** The bound assumes that each assignment inside a group is equally likely. Kifer (SIGMOD 2009) showed that an attacker can learn from the whole anatomized release how quasi-identifiers and sensitive values correlate, and then guess single values with probability well above $1/l$. Anatomy limits what one row reveals, not what the release reveals about the population.

## Implementations

## History

Xiao and Tao presented anatomy at VLDB 2006, with the l-diverse partition, the two-table release, the lower bound on the reconstruction error and the linear I/O algorithm. Their running example compared anatomy with a generalized table of the same data and showed much smaller errors on aggregate queries. The same release format, a table of group ids next to a table of sensitive values, is often called bucketization in later work. Kifer's 2009 deFinetti attack showed the limits of the $1/l$ bound when the attacker learns from the release, and the same authors' [m-invariance](/m-invariance/) of 2007 extended the group and signature idea to tables that change over time.

## References
