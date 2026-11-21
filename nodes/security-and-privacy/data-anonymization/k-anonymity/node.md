---
tag: TCBPNZ
kind: definition
slug: k-anonymity
name: k-anonymity
aliases:
- k-anonymous table
area: security-and-privacy/data-anonymization
level: intro
summary: A released table is k-anonymous if every record shares its quasi-identifier values with at least k-1 other records.
prereqs: [quasi-identifier, linkage-attack]
see_also: [generalization-and-suppression, l-diversity, t-closeness, km-anonymity, m-invariance, microaggregation, k-anonymity-np-hardness, differential-privacy-definition]
sources:
  - paper: doi:10.1142/S0218488502001648
    title: "Latanya Sweeney, k-anonymity, a model for protecting privacy, International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems 10(5), 2002"
    locator: "pp. 557 to 570, the definition of k-anonymity, and the attacks on k-anonymous releases by unsorted matching, complementary release and temporal inference"
  - paper: doi:10.1109/69.971193
    title: "Pierangela Samarati, Protecting respondents' identities in microdata release, IEEE Transactions on Knowledge and Data Engineering 13(6), 2001"
    locator: "pp. 1010 to 1027, the k-anonymity requirement for released microdata, met by generalization and suppression"
  - url: "https://spdp.di.unimi.it/papers/k-Anonymity.pdf"
    title: "Valentina Ciriani, Sabrina De Capitani di Vimercati, Sara Foresti and Pierangela Samarati, k-Anonymity, in Secure Data Management in Decentralized Systems, Springer, Advances in Information Security, 2007"
    locator: Sections 2 and 3, the definition, the k-anonymity requirement and the taxonomy of generalization and suppression
  - paper: doi:10.1145/1217299.1217302
    title: "Ashwin Machanavajjhala, Daniel Kifer, Johannes Gehrke and Muthuramakrishnan Venkitasubramaniam, l-diversity, privacy beyond k-anonymity, ACM Transactions on Knowledge Discovery from Data 1(1), 2007"
    locator: the homogeneity attack and the background knowledge attack on k-anonymous tables
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing, a survey of recent developments, ACM Computing Surveys 42(4), 2010"
    locator: the sections on record linkage and on k-anonymity and its refinements
---

k-anonymity is a condition on a released table: each combination of [quasi-identifier](/quasi-identifier/) values that occurs in the table occurs in at least $k$ rows. Then a join of the release with an outside table on the quasi-identifier, the [linkage attack](/linkage-attack/), never ties a person to fewer than $k$ rows. Sweeney and Samarati proposed the model around 1998, and the main papers appeared in 2001 and 2002. A table is made k-anonymous by [generalization and suppression](/generalization-and-suppression/) or by [microaggregation](/microaggregation/). The value of $k$ is a policy choice of the data holder.

## Definition

Let $T$ be a table with $n$ rows and let $Q = \{A_1, \ldots, A_d\}$ be its quasi-identifier. For a row $t$, write $t[Q]$ for the tuple of its values on $Q$. The *equivalence class* of $t$ is the set of rows $t'$ with $t'[Q] = t[Q]$.

**Definition (Sweeney 2002).** Let $k \ge 1$ be an integer. The table $T$ is **k-anonymous** with respect to $Q$ if each tuple of values that occurs in $T[Q]$ occurs in at least $k$ rows of $T$. In other words, each equivalence class on $Q$ has at least $k$ rows.

Three facts follow at once from the definition.
- **Monotone in k.** A k-anonymous table is $k'$-anonymous for each $k' \le k$. Each table is 1-anonymous.
- **Monotone in the attributes.** If $T$ is k-anonymous on $Q$, it is k-anonymous on each subset of $Q$, because each class on the subset is a union of classes on $Q$.
- **Easy to check.** Count the rows of each tuple $t[Q]$ with a hash table, and compare the smallest count with $k$. This takes $O(n d)$ expected time on the [word RAM](/word-ram/).

What it protects against, and only that: let $E$ be any outside table with identities and the attributes $Q$, written at the same level of detail as the release. For each person $p$ of $E$, the set of rows of the release that agree with $p$ on $Q$ is empty or has at least $k$ rows. This is a theorem about the join on $Q$. The common reading "the adversary finds the row of $p$ with probability at most $1/k$" is a heuristic. It assumes that the adversary has no information outside $Q$ and picks one row of the class at random.

Making a table k-anonymous with the fewest suppressed cells is NP-hard for $k \ge 3$ ([NP-hardness of optimal k-anonymity](/k-anonymity-np-hardness/)), and the [O(k) approximation](/k-anonymity-approximation/) gives a bound on the cost.

## Examples and non-examples

The tables are made up. The quasi-identifier is $Q = \{$ZIP, age$\}$.

| row | ZIP | age | diagnosis |
|---|---|---|---|
| 1 | 1305\* | 20 to 29 | flu |
| 2 | 1305\* | 20 to 29 | asthma |
| 3 | 1306\* | 30 to 39 | diabetes |
| 4 | 1306\* | 30 to 39 | flu |
| 5 | 1306\* | 30 to 39 | cold |

- **2-anonymous, not 3-anonymous.** The classes are $\{1, 2\}$ and $\{3, 4, 5\}$. The smallest class has 2 rows.
- **k-anonymous but not private: homogeneity.** Change the diagnosis of rows 3, 4 and 5 to flu. The table is still 3-anonymous, but each person who matches the class $\{3, 4, 5\}$ has flu. The join gives no row, but it gives the value. Machanavajjhala et al. (2007) call this the homogeneity attack, and [l-diversity](/l-diversity/) and [t-closeness](/t-closeness/) answer it.
- **k-anonymous but not private: background knowledge.** If the adversary knows that a person of class $\{1, 2\}$ does not have asthma, the class shows that the person has flu. k-anonymity says nothing about knowledge outside $Q$.
- **Not k-anonymous after two releases: complementary release.** Take four rows with (ZIP, age, diagnosis) equal to (13053, 28, flu), (13053, 29, cold), (13068, 28, asthma) and (13068, 29, diabetes). Release A shows the ZIP and hides the age: each class has 2 rows. Release B hides the ZIP and shows the age: each class has 2 rows. Both are 2-anonymous. But a person with ZIP 13053 and age 28 has a diagnosis in $\{$flu, cold$\}$ by A and in $\{$flu, asthma$\}$ by B, so the diagnosis is flu. Sweeney (2002) names this the complementary release attack. Each new release must be k-anonymous together with the earlier ones, which [m-invariance](/m-invariance/) studies for data that changes.
- **Row order.** If two releases of the same rows keep the same row order, a reader can match the rows by position. Sweeney (2002) calls this unsorted matching. Shuffle the rows of each release.
- **The quasi-identifier is too small.** A table that is k-anonymous on $\{$ZIP, age$\}$ may have unique rows on $\{$ZIP, age, sex$\}$. If an outside table has the sex, the protection is gone. The choice of $Q$ is a policy decision, and so is $k$.

## Related definitions

- [Quasi-identifier](/quasi-identifier/): the attributes that the condition is about.
- [Generalization and suppression](/generalization-and-suppression/): the usual way to reach k-anonymity, with the algorithms [Samarati's algorithm](/samarati-algorithm/), [Datafly](/datafly/), [Incognito](/incognito/) and [Mondrian](/mondrian-anonymization/).
- [Microaggregation](/microaggregation/) reaches k-anonymity on numeric data by replacing each group of at least $k$ rows by its mean.
- [l-diversity](/l-diversity/) and [t-closeness](/t-closeness/) add conditions on the sensitive values of each class.
- [km-anonymity](/km-anonymity/) asks k-anonymity only for each set of at most $m$ items of a set-valued record.
- [Differential privacy](/differential-privacy-definition/) is a condition on the release mechanism, not on the output table, and it holds whatever the adversary knows.

## References
