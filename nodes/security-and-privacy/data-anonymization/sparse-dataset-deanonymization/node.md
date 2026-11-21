---
tag: K7AE0V
kind: technique
slug: sparse-dataset-deanonymization
name: Sparse dataset de-anonymization
aliases:
- Narayanan-Shmatikov Netflix attack
area: security-and-privacy/data-anonymization
level: advanced
summary: Shows that records of a large sparse dataset with names removed, such as movie ratings, can be re-identified from a few facts about a person, so removing identifiers does not anonymize them.
prereqs: [linkage-attack, quasi-identifier]
see_also: [social-network-deanonymization, pseudonymization, k-anonymity, differential-privacy-definition, membership-inference-attack, dinur-nissim-reconstruction-attack, active-attack-on-social-graphs, data-swapping]
sources:
  - paper: doi:10.1109/SP.2008.33
    title: "Arvind Narayanan and Vitaly Shmatikov, Robust de-anonymization of large sparse datasets, IEEE Symposium on Security and Privacy (S&P 2008)"
    locator: "pp. 111 to 125, the abstract and introduction (the threat model, the robustness to errors in the outside knowledge, the measurement on the Netflix Prize data, and the lessons for data release); the preprint is arXiv cs/0610105"
  - paper: "Paul Ohm, Broken promises of privacy, responding to the surprising failure of anonymization, UCLA Law Review 57, 2010"
    locator: "pp. 1701 to 1777, the AOL and Netflix releases and the consequences for privacy law"
  - paper: doi:10.1145/1557019.1557090
    title: "Frank McSherry and Ilya Mironov, Differentially private recommender systems, building privacy into the Netflix Prize contenders, KDD 2009"
    locator: "pp. 627 to 636, differentially private versions of the leading Netflix Prize methods, with little loss of accuracy"
---

Narayanan and Shmatikov (IEEE S&P 2008) showed that a large sparse dataset, in which each record holds a few values out of a very large set of possible attributes, is easy to re-identify even when the names are removed. Their case was the Netflix Prize data of 2006: about 500,000 subscribers and their movie ratings with dates, released with the names replaced by numbers. Their measurement was that a few ratings with approximate dates, of the kind a person may also post on a public review site, single out almost every record, and that errors in this outside knowledge do not stop the match. The lesson for data release is that in sparse, high-dimensional data almost every record is unique, so there is no small set of [quasi-identifiers](/quasi-identifier/) to protect, and [pseudonymization](/pseudonymization/) gives no anonymity. This page describes the published result, the conditions it needs and the defenses. It gives no method that can be run on a real dataset.

## In plain words

A film service publishes the ratings of its customers for a contest. It removes the names, and it changes some ratings. Each customer has rated a few hundred films out of many thousands, and no two customers have the same mix.

Suppose someone knows a few films that a person watched and roughly when, for example from talk at work or from reviews that the person posted under her own name. In such data, very few customers match even these few facts, and often only one does. Then the whole record of that customer is known, with every film she rated. Some of them may say things about her that she never made public. The names were gone, but the data itself worked like a name.

## When it applies

The published result needs these conditions. Each is also a point where a defense can act.

- **A sparse, high-dimensional release.** Each record has values for a small part of a very large set of attributes: films, products, places, search terms or web pages. Two records seldom overlap much.
- **Records released at the level of a person.** The release has one record per person, with all of that person's values together. Aggregate statistics do not give a record to match.
- **Some outside knowledge about the target.** A few of the target's attribute values, possibly with errors and with approximate dates. It can come from a public source with names, from the person, or from people who know the person. The paper measures how little is needed.
- **No formal protection of the record.** The release was pseudonymized and lightly perturbed, with no guarantee that bounds what one record reveals.

The publisher cannot know all outside knowledge that exists now or later. A release that is safe only if nobody knows anything about a person is not safe.

## The template

The template is the abstract shape of the threat, with a named hole at each point where a defense can act. It names the stages at the level of the paper's abstract and is not a procedure.

```pseudo id=main
SPARSE-RELEASE-THREAT(release, outside knowledge)
L1  the publisher releases one record per person with names removed       ▷ hole RELEASE: records, or statistics only
L2  the attacker knows a few approximate values of one person               ▷ hole AUX: what is public about people
L3  the values are compared with every released record, allowing errors   ▷ hole SPARSITY: how many records agree
L4  the attacker accepts a match only if one record stands out clearly     ▷ hole DP: no record changes the output much
```

- **RELEASE (line L1).** Releasing only aggregate results, or giving analysts access to a query system instead of records, removes the per-person record that line L3 needs.
- **AUX (line L2).** The publisher does not control it. The paper's lesson is that even a small amount of approximate knowledge is enough in sparse data, and that the outside source can be one the publisher never thought of.
- **SPARSITY (line L3).** This is the property of the data that makes the threat work. In the model below, the number of other records that agree with $s$ known values falls exponentially in $s$. Removing a few values, or changing a few, does not change this much, which is why the paper found the threat robust to the perturbation used in the release.
- **DP (line L4).** A release with [differential privacy](/differential-privacy-definition/) bounds the change in the output distribution from adding or removing one person. Then no record stands out because of one person, whatever the outside knowledge. McSherry and Mironov (2009) showed that several leading methods of the Netflix Prize could be run with differential privacy with little loss of accuracy.

**An abstract model (a theorem in the model).** Take $n$ records over a set of $N$ attributes, where each record holds exactly $d$ attributes, chosen uniformly and independently of the other records. Fix one record $x$ and $s \le d$ of its attributes. The probability that another given record also holds all $s$ of them is

$$\frac{\binom{N - s}{d - s}}{\binom{N}{d}} = \frac{d (d - 1) \cdots (d - s + 1)}{N (N - 1) \cdots (N - s + 1)} \le \left(\frac{d}{N}\right)^{s},$$

so the expected number of other records that agree with $x$ on these $s$ attributes is at most $(n - 1) (d / N)^s$. With the made-up sizes $N = 1000$, $d = 10$ and $n = 10^6$, the exact expected counts are:

| $s$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| expected other records that agree | about 10,000 | about 90 | about 0.72 | about 0.005 | about 0.00003 |

So in this model, 4 known values leave $x$ alone with high probability, among a million records. Real data is not uniform. Popular attributes are shared by many records and say little, and rare attributes say much more, so a few rare values can be enough. The model is not a measurement on any dataset, and the numbers of the paper are measurements on its data.

## Classic examples

- **The Netflix Prize data (2006).** The case of Narayanan and Shmatikov. The paper reports that 8 ratings, of which 2 may be wrong, with dates known within 14 days, identify 99% of the records uniquely. They also matched a small sample of records against public reviews on IMDb to show that the outside knowledge exists. Netflix cancelled a planned second contest in March 2010, after a letter from the US Federal Trade Commission and a lawsuit by subscribers, which was settled.
- **The AOL search log (2006).** AOL released search queries with the user names replaced by numbers. Reporters identified a user from the content of her queries. Ohm (2010) treats the AOL and Netflix cases as the main examples of the failure of anonymization by the removal of identifiers.
- **Linkage on quasi-identifiers.** The older [linkage attack](/linkage-attack/) joins a release with a public list on a few fields such as postcode, birth date and sex. Sparse data differs because there is no fixed set of such fields: any few values of a record can act as its identifier.
- **Social graphs.** The same authors showed the same lesson for graphs with names removed, in [social network de-anonymization](/social-network-deanonymization/), and [active attacks on social graphs](/active-attack-on-social-graphs/) are an earlier result of this kind.
- **Statistics instead of records.** The [Dinur-Nissim theorem](/dinur-nissim-reconstruction-attack/) shows that even aggregate answers, if there are many and they are too accurate, let one reconstruct the data. So releasing statistics helps only together with noise.

## Variations

- **Other sparse data.** Location traces, purchase histories, browsing histories and medical codes have the same property. Few points per person, from a very large space, single a person out.
- **Membership instead of identity.** Even when no record is released, models trained on the data can reveal whether a person was in the data, which is [membership inference](/membership-inference-attack/).
- **Partial knowledge as the goal.** The attacker may only want to learn more values of a person already known, not to name a record. In sparse data this is the same threat, since one matched record gives all its values.

## Pitfalls

These are pitfalls for a publisher.

- **Treating the release as anonymous because names are gone.** Pseudonymization keeps the per-person record, and in sparse data the record itself identifies the person.
- **Light perturbation as protection.** Changing a few values or dates, or removing a few records, does not stop the threat, because the match allows errors at line L3. The paper's measurement supports this for its data.
- **Assuming the attacker knows a lot.** The point of the result is that a few approximate facts are enough. A risk assessment that assumes a full outside copy of the data overestimates the effort.
- **k-anonymity for sparse data.** Making every record agree with $k - 1$ others on all attributes needs very coarse generalization when there are thousands of attributes, and then little of the data is left. [k-anonymity](/k-anonymity/) and [data swapping](/data-swapping/) were designed for a few quasi-identifiers.
- **Calling the attributes not sensitive.** Ratings of films seem harmless, but Narayanan and Shmatikov point out that a full rating history can suggest political or religious views or sexual orientation.
- **Forgetting future data.** Outside knowledge grows after the release. A release cannot be recalled, so a check against the outside sources of today is not enough.

## Exercises

1. Prove the formula of the abstract model for the probability that a uniform random set of $d$ attributes out of $N$ contains $s$ given attributes, and the bound $(d / N)^s$.
2. In the abstract model with $N = 1000$, $d = 10$ and $n = 10^6$, find the least $s$ for which the expected number of other agreeing records is below $10^{-2}$. Then change the model so that one attribute is held by half of all records and the others are uniform. Explain why knowing that attribute helps much less than knowing a uniform one.
3. Explain why a release that is $\varepsilon$-differentially private bounds what any outside knowledge plus the release can say about whether one person is in the data, in terms of $e^{\varepsilon}$.
4. A publisher plans to release purchase histories with names removed and with 10% of the items deleted at random. Use the template to say which holes this choice addresses and which it does not.

## References
