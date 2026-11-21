---
tag: YFDA8G
kind: definition
slug: km-anonymity
name: km-anonymity
aliases:
- transaction k-anonymity
area: security-and-privacy/data-anonymization
level: advanced
summary: For set-valued data, requires that any m items an attacker knows of a transaction match at least k transactions.
prereqs: [k-anonymity, quasi-identifier]
see_also: [k-anonymity, quasi-identifier, sparse-dataset-deanonymization, generalization-and-suppression, incognito, l-diversity, linkage-attack, differential-privacy-definition]
sources:
  - paper: doi:10.14778/1453856.1453874
    title: "Manolis Terrovitis, Nikos Mamoulis and Panos Kalnis, Privacy-preserving anonymization of set-valued data, PVLDB 1(1), 2008, pages 115-125"
    locator: Section 1 (the shopping-bag example), Section 3 (Definition 1, the subset queries), Section 3.1 (the generalization hierarchy of Figure 1, Definition 2 and the example of Figure 2), Section 3.2 (cuts and global recoding), Section 3.3 (NCP), Section 3.4 (Property 1, monotonicity of cuts) and Section 4 (the count-tree and the OA, DA and AA algorithms)
  - paper: doi:10.1109/sp.2008.33
    title: "Arvind Narayanan and Vitaly Shmatikov, Robust de-anonymization of large sparse datasets, IEEE Symposium on Security and Privacy 2008, pages 111-125"
    locator: the re-identification of records in sparse data from a few known items, which motivates protection against partial knowledge
---

$k^m$-anonymity is a privacy condition for set-valued data, such as shopping baskets, search logs or lists of diagnoses, where each record is a set of items of any size. An attacker often knows a few items of a person's record, for example some of the things the person bought, and wants to find the whole record. Terrovitis, Mamoulis and Kalnis (PVLDB 2008) defined a database as $k^m$-anonymous if no attacker who knows up to $m$ items of a transaction can narrow the candidates down to fewer than $k$ transactions. Every item can be part of the attacker's knowledge, so there is no fixed set of [quasi-identifiers](/quasi-identifier/), and every item can also be the thing the attacker wants to learn. Both $k$ and $m$ are policy choices: $m$ models how much the attacker is assumed to know. The condition is a property of the published database, and it says nothing about attackers who know more than $m$ items.

## Definition

A **transaction** is a non-empty subset of a domain $\mathcal I$ of items, and a database $D$ is a multiset of transactions. The **support** of an itemset $I$ is the number of transactions $t \in D$ with $I \subseteq t$.

**Definition (Terrovitis, Mamoulis and Kalnis, Definition 1).** A database $D$ is **$k^m$-anonymous** if no attacker with background knowledge of up to $m$ items of a transaction $t \in D$ can use these items to identify fewer than $k$ transactions of $D$. Equivalently, every itemset $I$ with $|I| \le m$ has support 0 or at least $k$.

An itemset with support 0 is safe: knowing it matches no transaction. The knowledge is modelled as a subset query, the set of transactions that contain the known items.

To make a database $k^m$-anonymous, the paper uses a generalization hierarchy over $\mathcal I$ and **global recoding**: a cut of the hierarchy maps each item to one ancestor in all transactions, such as "skim milk" to "milk". Transactions keep set semantics, so two items that map to the same ancestor become one item (Definition 2 and Figure 2 of the paper). The cost of a cut is measured by the normalized certainty penalty (NCP), which charges each generalized item by the share of the domain it covers.

Facts, each a theorem:

- **Support is anti-monotone.** If $I \subseteq J$, the support of $I$ is at least that of $J$. So $k^m$-anonymity implies $k^{m'}$-anonymity for every $m' \le m$, and $k$-anonymity with a larger $k$ implies it with a smaller one.
- **Whole-transaction anonymity is stronger.** If every transaction occurs at least $k$ times in $D$, then $D$ is $k^m$-anonymous for every $m$, because an itemset $I \subseteq t$ is contained in all the copies of $t$. The converse is false, as the example below shows.
- **Coarser cuts stay anonymous** (Property 1 of the paper, monotonicity of cuts). If a cut gives a $k^m$-anonymous database, so does every more general cut. The reason: an itemset $I'$ of size at most $m$ over the coarser items that some transaction contains comes from an itemset $J$ of size at most $|I'|$ over the finer items in that transaction, picking one item below each element of $I'$, and every transaction that contains $J$ contains $I'$ after the coarser recoding. So the support of $I'$ is at least the support of $J$, which is 0 or at least $k$, and it is not 0.

The anti-monotone support gives a direct test: count every itemset of size at most $m$ that occurs in some transaction, and check the counts. proofs/correctness.md proves that the test is exact.

```pseudo id=main
KM-ANONYMOUS(D, k, m)
L1  C ← an empty map from itemsets to counts
L2  for each transaction t in D do
L3      for each subset I of t with 1 ≤ |I| ≤ m do
L4          C[I] ← C[I] + 1
L5  for each itemset I in C do
L6      if C[I] < k then return false
L7  return true
```

If each transaction has at most $\tau$ items, lines L2 to L4 do $\sum_{j=1}^{m} \binom{\tau}{j}$ map updates per transaction, which is $O(|D|\, \tau^m)$ in total for a fixed $m$, with hashing in the word-RAM model. The paper stores the same counts in a count-tree, a prefix tree like the FP-tree, and builds it in $O(|D| \binom{\tau}{m})$ steps (Section 4.1). The cost grows fast with $m$, which is one reason $m$ is small in practice.

Finding the cut with the least information loss is hard in general. The paper gives an optimal algorithm (OA) that searches the lattice of cuts bottom-up in the manner of [Incognito](/incognito/), and two heuristics: direct anonymization (DA), which fixes the itemsets of size $m$ that break the condition, and apriori anonymization (AA), which fixes itemsets of size $1, 2, \ldots, m$ in turn, so that each level has fewer combinations to check.

## Examples and non-examples

The database is the one of Figure 2 of the paper, with four synthetic transactions over $\mathcal I = \{a_1, a_2, b_1, b_2\}$ and the hierarchy $a_1, a_2 \to A$, $b_1, b_2 \to B$, $A, B \to ALL$. Take $k = 2$.

| id | original $D$ | cut $\{a_1, a_2\} \to A$ | cut $\{b_1, b_2\} \to B$ |
|---|---|---|---|
| $t_1$ | $\{a_1, b_1, b_2\}$ | $\{A, b_1, b_2\}$ | $\{a_1, B\}$ |
| $t_2$ | $\{a_2, b_1\}$ | $\{A, b_1\}$ | $\{a_2, B\}$ |
| $t_3$ | $\{a_2, b_1, b_2\}$ | $\{A, b_1, b_2\}$ | $\{a_2, B\}$ |
| $t_4$ | $\{a_1, a_2, b_2\}$ | $\{A, b_2\}$ | $\{a_1, a_2, B\}$ |

- **$D$ is $2^1$-anonymous but not $2^2$-anonymous.** Each single item has support at least 2: $a_1$ has 2, and $a_2$, $b_1$ and $b_2$ have 3. But the pair $\{a_1, b_1\}$ has support 1: an attacker who knows that a person bought $a_1$ and $b_1$ finds $t_1$ and learns that the person also bought $b_2$.
- **The cut $\{a_1, a_2\} \to A$ gives a $2^2$-anonymous database.** The supports are $\{A\}$: 4, $\{b_1\}$: 3, $\{b_2\}$: 3, $\{A, b_1\}$: 3, $\{A, b_2\}$: 3, $\{b_1, b_2\}$: 2. It is also $2^3$-anonymous, since $\{A, b_1, b_2\}$ has support 2.
- **$2^2$-anonymous but not 2-anonymous as whole transactions.** In the same recoded database, $\{A, b_1\}$ and $\{A, b_2\}$ each occur once as a whole transaction. An attacker who knew every item of $t_2$ and knew that the basket had no other items would find it. $k^m$-anonymity does not protect against that much knowledge, by design.
- **Non-example: the cut $\{b_1, b_2\} \to B$.** The supports of $\{a_1\}$, $\{a_2\}$ and $\{B\}$ are 2, 3 and 4, and $\{a_1, B\}$ has 2 and $\{a_2, B\}$ has 3, but $\{a_1, a_2\}$ has support 1, in $t_4$. Generalizing the wrong items does not help.
- **Coarser is safe.** The cut that maps all four items to $ALL$ gives four copies of $\{ALL\}$, which is $2^m$-anonymous for every $m$ and useless, as Property 1 predicts.

## Related definitions

- [k-anonymity](/k-anonymity/): the condition for tables with a fixed set of quasi-identifier attributes. $k^m$-anonymity bounds the attacker's knowledge by a number of items instead of a set of attributes.
- [Quasi-identifier](/quasi-identifier/): in set-valued data any combination of up to $m$ items can play this role.
- [Sparse dataset de-anonymization](/sparse-dataset-deanonymization/): Narayanan and Shmatikov showed that a few known items re-identify records in large sparse datasets, which is the threat that $k^m$-anonymity bounds when $m$ is at least the number of items the attacker knows.
- [l-diversity](/l-diversity/): protects sensitive values once a record is narrowed down to a group. Terrovitis et al. treat every item as both a possible quasi-identifier and possibly sensitive, so $k^m$-anonymity alone does not stop an attacker from learning an item that all matching transactions share.
- [Generalization and suppression](/generalization-and-suppression/): the operations used to reach $k^m$-anonymity; here generalization follows an item hierarchy and is global.
- [Differential privacy](/differential-privacy-definition/): a guarantee that does not depend on a bound $m$ on the attacker's knowledge.

## References
