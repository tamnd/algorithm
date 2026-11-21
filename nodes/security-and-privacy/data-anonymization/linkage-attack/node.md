---
tag: 5N17KX
kind: concept
slug: linkage-attack
name: Linkage attack
aliases:
- re-identification attack
area: security-and-privacy/data-anonymization
level: intro
summary: Re-identifies records in a released table by joining it with a public table on shared quasi-identifiers.
history:
  year: 2002
  people: [Latanya Sweeney]
  note: "Sweeney published in 2002 how a release of medical data without names was linked to a voter list on ZIP code, birth date and sex, and proposed k-anonymity as the answer."
prereqs: [quasi-identifier]
see_also: [k-anonymity, quasi-identifier, entity-resolution, fellegi-sunter-model, sparse-dataset-deanonymization, social-network-deanonymization, l-diversity, differential-privacy-definition]
sources:
  - paper: doi:10.1142/S0218488502001648
    title: "Latanya Sweeney, k-anonymity, a model for protecting privacy, International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems 10(5), 2002"
    locator: "pp. 557 to 570, the introduction, with the linkage of medical data and a voter list on ZIP code, birth date and sex"
  - paper: "Latanya Sweeney, Simple demographics often identify people uniquely, Carnegie Mellon University, Data Privacy Working Paper 3, 2000"
    locator: the uniqueness rates measured on the 1990 United States census summary data
  - paper: doi:10.1145/1179601.1179615
    title: Philippe Golle, Revisiting the uniqueness of simple demographics in the US population, Proceedings of the 5th ACM Workshop on Privacy in the Electronic Society (WPES 2006)
    locator: "pp. 77 to 80, the uniqueness rates for the 1990 and 2000 census data"
  - paper: doi:10.1109/69.971193
    title: "Pierangela Samarati, Protecting respondents' identities in microdata release, IEEE Transactions on Knowledge and Data Engineering 13(6), 2001"
    locator: "pp. 1010 to 1027, the linking of released microdata to outside sources as the threat that generalization answers"
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing, a survey of recent developments, ACM Computing Surveys 42(4), 2010"
    locator: the sections on the attack models, record linkage, attribute linkage and table linkage
---

A linkage attack joins a released table that has no names with an outside table that has names, on the attributes that both tables share. A row of the release that matches exactly one person of the outside table is tied to that person, together with its sensitive values. The attack needs no access to the data holder and no special skill: it is a join of two tables. Its main lesson is that removing names and record numbers does not make a table anonymous. This lesson is the starting point of [k-anonymity](/k-anonymity/) and of the later models of data release.

## In plain words

A hospital gives out its records for research. It deletes the names, but each record still has the ZIP code, the date of birth and the sex of the patient. A town publishes its voter list, with the name, the address, the date of birth and the sex of each voter. Put the two lists side by side and look for records that agree on ZIP code, birth date and sex. Where only one voter fits a hospital record, you know whose record it is, and you know the diagnosis too.

The defense is to make each combination of these shared details common in the release, or to stop releasing exact records at all.

## The idea

Let $T$ be the released table. It has a set $Q$ of [quasi-identifier](/quasi-identifier/) attributes and some sensitive attributes, but no names. Let $E$ be an outside table with an identity column and the attributes of $Q$. The attack is the join of $T$ and $E$ on equal values of $Q$. For a person $p$ in $E$, let $M(p)$ be the set of rows of $T$ that agree with $p$ on $Q$.

- If $|M(p)| = 1$, the release ties one row to $p$. The tie is correct when $p$ is in $T$ and no other person outside $E$ has the same values. Population uniqueness on $Q$ is what makes such ties correct.
- If $|M(p)| \ge k$, the join alone does not say which of the $k$ or more rows is the row of $p$. This is the protection that k-anonymity gives against this join.
- If all rows of $M(p)$ have the same sensitive value, the adversary learns this value for $p$ without knowing the row. This is the homogeneity problem that [l-diversity](/l-diversity/) answers.

In practice the values do not always agree exactly, because of typing errors and different formats. Probabilistic record linkage, such as the [Fellegi-Sunter model](/fellegi-sunter-model/), scores the pairs and accepts the likely matches. The same methods that link records of one person for good reasons, as in [entity resolution](/entity-resolution/), also link a release to outside data. So a data holder must assume that approximate matches are found too.

The size of the risk depends on outside data that the data holder does not control. A quasi-identifier is a guess about what an adversary can know, and new public sources can make the guess wrong after the release.

**Published results.** Sweeney (2002) describes how a state release of medical data for state employees, without names, was joined with a voter list on ZIP code, birth date and sex. Her measurement on the 1990 census estimated that about 87 percent of the United States population was likely unique on 5-digit ZIP code, sex and date of birth (Sweeney 2000). Golle (2006) measured about 61 percent for the 1990 census and 63 percent for the 2000 census. These rates are measurements on one population at one time, not properties of the attributes. Later work showed the same effect in sparse data, such as ratings and purchases, where a few items of one person are unique among millions ([sparse dataset de-anonymization](/sparse-dataset-deanonymization/)), and in released graphs ([social network de-anonymization](/social-network-deanonymization/)).

**Lessons for release.**
- Removing explicit identifiers is not anonymization. The other attributes can act as an identifier.
- The protection must be judged against each plausible outside table, now and in the future.
- A syntactic model such as k-anonymity protects only the attributes that the data holder named as the quasi-identifier, and only against the join on them.
- [Differential privacy](/differential-privacy-definition/) bounds what the output reveals about each record whatever the adversary knows, so it needs no choice of quasi-identifier. It answers aggregate queries or makes synthetic data, not exact records.
- Contracts that forbid linking, and controlled access to the data, reduce the risk but do not remove it.

## Examples

All names and values below are made up. The released table has no names:

| row | ZIP | birth year | sex | diagnosis |
|---|---|---|---|---|
| r1 | 13053 | 1980 | F | flu |
| r2 | 13053 | 1980 | F | asthma |
| r3 | 13068 | 1975 | M | diabetes |
| r4 | 13068 | 1991 | M | flu |

An outside list has names and the same three attributes:

| name | ZIP | birth year | sex |
|---|---|---|---|
| Person A | 13053 | 1980 | F |
| Person B | 13053 | 1980 | F |
| Person C | 13068 | 1975 | M |
| Person D | 13068 | 1991 | M |
| Person E | 13068 | 1975 | F |

The join on ZIP, birth year and sex gives $M(\text{C}) = \{r3\}$ and $M(\text{D}) = \{r4\}$, so the release ties diabetes to Person C and flu to Person D. Persons A and B each match $\{r1, r2\}$, so the join does not tell which of the two rows is theirs. Person E matches no row.

Now release ZIP as 1306\* or 1305\* and the birth year as \*. Then $r3$ and $r4$ both read (1306\*, \*, M), and Persons C and D each match two rows with different diagnoses. Each class of the release has two rows, so the table is 2-anonymous on these attributes. If $r3$ and $r4$ had both been flu, the release would still tell that Persons C and D have flu, which is the homogeneity problem.

## Where it is used

- **Threat model of k-anonymity.** [k-anonymity](/k-anonymity/), [generalization and suppression](/generalization-and-suppression/) and [microaggregation](/microaggregation/) are defined against this join.
- **Disclosure control.** Statistical agencies assess the risk of a release by counting the rows that are unique, or rare, on the attributes an adversary can know, before they publish microdata.
- **Privacy-preserving record linkage.** [Privacy-preserving record linkage](/privacy-preserving-record-linkage/) does the benign form of the join between two data holders without showing the identifiers in the clear.
- **Motivation for formal privacy.** The failures of release without names, measured again and again, are a main reason for the move to [differential privacy](/differential-privacy-definition/) in official statistics.

## References
