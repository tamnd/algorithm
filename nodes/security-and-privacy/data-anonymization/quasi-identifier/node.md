---
tag: NFXPZ8
kind: definition
slug: quasi-identifier
name: Quasi-identifier
aliases:
- QID
- key attributes
area: security-and-privacy/data-anonymization
level: intro
summary: "A set of attributes such as zip code, birth date and sex that is not an identifier alone but can single out people when joined with other data."
prereqs: []
see_also: [k-anonymity, linkage-attack, l-diversity, km-anonymity, sparse-dataset-deanonymization, pseudonymization, entity-resolution, differential-privacy-definition]
sources:
  - paper: doi:10.1142/S0218488502001648
    title: "Latanya Sweeney, k-anonymity, a model for protecting privacy, International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems 10(5), 2002"
    locator: "pp. 557 to 570, the definition of a quasi-identifier through the link between a released table and outside data"
  - paper: doi:10.1109/69.971193
    title: "Pierangela Samarati, Protecting respondents' identities in microdata release, IEEE Transactions on Knowledge and Data Engineering 13(6), 2001"
    locator: "pp. 1010 to 1027, the quasi-identifier as the attributes of the released table that can be linked to outside data"
  - paper: "Latanya Sweeney, Simple demographics often identify people uniquely, Carnegie Mellon University, Data Privacy Working Paper 3, 2000"
    locator: the summary of the uniqueness rates measured on the 1990 United States census summary data
  - paper: doi:10.1145/1179601.1179615
    title: Philippe Golle, Revisiting the uniqueness of simple demographics in the US population, Proceedings of the 5th ACM Workshop on Privacy in the Electronic Society (WPES 2006)
    locator: "pp. 77 to 80, the uniqueness rates for the 1990 and 2000 census data"
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing, a survey of recent developments, ACM Computing Surveys 42(4), 2010"
    locator: the sections on the attack models and on record linkage
---

A quasi-identifier of a released table is a set of attributes that does not name a person, but whose combined values are rare enough to single out a person when someone matches them with an outside table that has names. ZIP code, date of birth and sex are the standard example. The data holder chooses the quasi-identifier from what an adversary can plausibly know, so it is a policy choice and not a property of the table alone. Models such as [k-anonymity](/k-anonymity/) protect a release by making each combination of quasi-identifier values common.

## Definition

A *person-specific table* $T$ has one row per person of some population $U$. Its attributes fall into three groups:
- **Explicit identifiers**, such as a name or a social security number. They are removed before release.
- **Quasi-identifiers**, the attributes that an adversary can also find in outside data that holds identities.
- **Sensitive attributes**, such as a diagnosis, which the release must not tie to a person.

Let $E$ be the outside data: a table that holds an identity and some attributes for people of $U$, such as a voter list. A set $Q$ of attributes of $T$ is a **quasi-identifier** for $E$ when $Q$ is also a set of attributes of $E$, and the values of $Q$ in some row of $T$ match exactly one row of $E$, so that the row of $T$ is tied to one identity. This follows Sweeney (2002) and Samarati (2001), who define the quasi-identifier through the link between the released table and outside data.

For a row $t$ of $T$, the *equivalence class* of $t$ on $Q$ is the set of rows of $T$ with the same values as $t$ on each attribute of $Q$. The row is *sample unique* on $Q$ if its class has one row. It is *population unique* if no other person of $U$ has its values on $Q$. Sample uniqueness is what the data holder can see in $T$. Population uniqueness is what makes a link to $E$ correct, and a sample unique row need not be population unique.

## Examples and non-examples

- **ZIP code, date of birth and sex.** Sweeney (2000) used the 1990 United States census summary data and estimated that about 87 percent of the population (216 million of 248 million) was likely unique on the 5-digit ZIP code, sex and full date of birth. With the place instead of the ZIP code the estimate was 53 percent, and with the county it was 18 percent. Golle (2006) did the measurement again and found about 61 percent for the 1990 census and 63 percent for the 2000 census. These numbers are measurements on one population at one time, with their own models of how birth dates spread. They are not properties of the attributes, but both show that three ordinary attributes can act as an identifier for most people.
- **A synthetic table.** The rows below are made up. On $Q = \{$ZIP, age, sex$\}$, rows 1 and 2 form a class of two rows, and rows 3 and 4 are each sample unique, so each of them can be tied to one person by a table that has the same three attributes and names.

| row | ZIP | age | sex | diagnosis |
|---|---|---|---|---|
| 1 | 10001 | 34 | F | flu |
| 2 | 10001 | 34 | F | asthma |
| 3 | 10002 | 51 | M | flu |
| 4 | 10003 | 29 | F | diabetes |

- **Not a quasi-identifier: an explicit identifier.** A name or a record number identifies a person by itself. It is removed or replaced (see [pseudonymization](/pseudonymization/)), and it is not part of the quasi-identifier.
- **Not a quasi-identifier: an attribute no adversary can know.** An attribute that appears in no outside source does not link a row to an identity, even if its values are unique. The choice is a judgment of the data holder, and a wrong judgment leaves a link open.
- **A sensitive attribute can be both.** A diagnosis is the value to protect, but an adversary who knows that a neighbor was in hospital for a rare condition can use it as a quasi-identifier. Many models assume that the sensitive attributes are not known to the adversary; this assumption must be stated.
- **Sparse data.** In a table of movie ratings or of purchases, a few items of one person are often unique among millions. There every small set of attributes can act as a quasi-identifier, and the split into quasi-identifiers and other attributes breaks down (see [sparse dataset de-anonymization](/sparse-dataset-deanonymization/)).

## Related definitions

- [k-anonymity](/k-anonymity/) asks that each equivalence class on the quasi-identifier has at least $k$ rows.
- A [linkage attack](/linkage-attack/) is the join of a release with outside data on the quasi-identifier.
- [l-diversity](/l-diversity/) and [t-closeness](/t-closeness/) add conditions on the sensitive values inside each class.
- [km-anonymity](/km-anonymity/) treats any $m$ items of a set-valued record as a possible quasi-identifier.
- [Entity resolution](/entity-resolution/) matches records of the same entity across sources; it is the benign form of the same join.
- [Differential privacy](/differential-privacy-definition/) does not need a choice of quasi-identifier, because it bounds what the output reveals about any one record, whatever the adversary knows.

## References
