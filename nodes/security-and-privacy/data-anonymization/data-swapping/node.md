---
tag: 13GPVZ
kind: technique
slug: data-swapping
name: Data swapping
aliases:
- record swapping
- rank swapping
area: security-and-privacy/data-anonymization
level: core
summary: Exchanges values of an attribute between pairs of records, chosen to keep marginal totals, to confuse a linkage attack.
prereqs: [linkage-attack, quasi-identifier]
see_also: [post-randomization-method, microaggregation, randomized-response, k-anonymity, differential-privacy-definition, dinur-nissim-reconstruction-attack, generalization-and-suppression, cell-suppression-problem]
sources:
  - paper: doi:10.1016/0378-3758(82)90058-1
    title: "Tore Dalenius and Steven P. Reiss, Data-swapping, a technique for disclosure control, Journal of Statistical Planning and Inference 6(1), 1982"
    locator: "pp. 73 to 85, swaps of values between records that keep the frequency counts of low order"
  - paper: "Stephen E. Fienberg and Julie McIntyre, Data swapping, variations on a theme by Dalenius and Reiss, Privacy in Statistical Databases (PSD 2004), LNCS 3050, Springer, 2004"
    locator: "the survey of the original method, rank swapping and the swapping at the US Census Bureau"
  - paper: "Richard A. Moore, Controlled data-swapping techniques for masking public use microdata sets, Statistical Research Division Report Series RR 96-04, US Census Bureau, 1996"
    locator: "the rank swapping method with a window of p percent of the records, credited to Greenberg (1987), and its controls on the change of statistics"
  - book: isbn:9781119978152
    title: "Anco Hundepool, Josep Domingo-Ferrer, Luisa Franconi, Sarah Giessing, Eric Schulte Nordholt, Keith Spicer and Peter-Paul de Wolf, Statistical Disclosure Control, Wiley, 2012"
    locator: "Chapter 3, Microdata, the section on data swapping and rank swapping among the perturbative masking methods"
  - url: "https://www2.census.gov/library/publications/decennial/2020/2020-census-disclosure-avoidance-handbook.pdf"
    title: "US Census Bureau, Disclosure Avoidance for the 2020 Census, An Introduction, November 2021"
    locator: "the history of disclosure avoidance at the Census Bureau, the household swapping of the 1990, 2000 and 2010 censuses, and the change to differential privacy for 2020"
---

Data swapping masks a microdata file by exchanging the values of some attributes between pairs of records. Dalenius and Reiss (1982) proposed it so that a released file keeps the low-order frequency counts of the original, but no single record can be trusted to be a true record. A person who links a released record to a known person by its [quasi-identifier](/quasi-identifier/) values cannot be sure that the sensitive values belong to that person, because the record may have been swapped. The common forms are swapping between records that agree on a matching key, as in the household swapping of the US censuses of 1990 to 2010, and rank swapping of a numerical attribute, where the partner has a close rank. Swapping keeps the counts that the key controls and blurs the others. It gives no formal guarantee, and in 2020 the Census Bureau replaced it with [differential privacy](/differential-privacy-definition/).

## In plain words

A town office publishes one line for each house, with the street, the number of people and some answers. Before it publishes, it picks a few houses at random. Each picked house trades its street with another house that has the same number of people, in another part of town. The number of houses of each size on each street is still right. The number of people in the town is still right.

Now a neighbor who finds a line that looks like a house he knows cannot be sure. That line can be a house from another street that was moved here. The price is that some details are wrong, such as which answers go with which street.

## When it applies

- The file is microdata, with categorical attributes such as area, household size or tenure, or numerical attributes such as income.
- The analysts need some counts exactly: the counts by area, or by area and household size. The matching key of the swap can keep exactly those counts.
- The office accepts that other joint counts move a little, and it can choose the swap rate and the records to swap.
- A formal privacy bound is not required. Swapping has a policy parameter (the swap rate) but no bound on what one record changes. For a bound, use a [differentially private](/differential-privacy-definition/) method.

## The template

Let $T$ be a table of $n$ records, $A$ the attributes to swap, $M$ the matching key (attributes that the partners must share), and $\rho$ the swap rate, a policy choice.

```pseudo id=main
SWAP(T, A, M, ρ)
L1  S ← SELECT(T, ρ)                         ▷ hole: about ρ n records, at random or the records at most risk
L2  for each record x of S that is not yet swapped do
L3      y ← PARTNER(T, x, M)                 ▷ hole: a record not yet swapped with the same values of M
L4      if y exists then
L5          exchange the values of A between x and y
L6          mark x and y as swapped
L7  return T in a random order
```

The holes are SELECT, PARTNER and the choice of $A$ and $M$:

- **Random swapping.** SELECT draws records at random. Every record has the same chance to be swapped.
- **Targeted swapping.** SELECT prefers the records at most risk, for example households that are unique on their area and a few other attributes. The swap rate is then spent where it protects most.
- **Rank swapping** of one numerical attribute (Moore 1996, who credits Greenberg 1987). Sort the records by the attribute. For each record in rank order that is not yet swapped, PARTNER picks at random a record not yet swapped whose rank is higher by at most $p$ percent of $n$. A small $p$ moves each value only a little.

What a swap keeps is a fact of counting, not a heuristic. A swap of $A$ between two records with the same $M$ keeps:

- the count of each combination of values of $A$ and $M$, because one record leaves the cell and one comes in;
- the count of each combination of values of the attributes outside $A$, because those values do not move;
- every total of a numerical attribute in $A$.

It can change the count of a combination of $A$ with an attribute $B$ outside $A$ and $M$.

**Example.** Six households, with $A = \{\text{area}\}$ and $M = \{\text{size}\}$:

| household | area | size | tenure |
|---|---|---|---|
| 1 | north | 2 | own |
| 2 | north | 3 | rent |
| 3 | north | 2 | rent |
| 4 | south | 2 | rent |
| 5 | south | 4 | own |
| 6 | south | 2 | own |

Swap the area of household 1 with that of household 4. Both have size 2. After the swap, household 1 is in the south and household 4 in the north.

| count | before | after |
|---|---|---|
| north, size 2 | 2 (1, 3) | 2 (3, 4) |
| south, size 2 | 2 (4, 6) | 2 (1, 6) |
| owners | 3 | 3 |
| north, own | 1 | 0 |
| north, rent | 2 | 3 |

The counts by area and size and the counts by tenure stay the same. The counts by area and tenure change, because tenure was not in $M$. A swap of household 1 with household 6, which has the same size and the same tenure, would keep all the counts above. That is why offices often add more attributes to $M$: each one keeps more counts but leaves fewer partners.

## Classic examples

- **Dalenius and Reiss (1982).** The original method swaps values of categorical attributes so that the counts of all combinations of up to $t$ attributes stay the same. It is hard to find such swaps for large files, which led to the simpler forms below.
- **Household swapping in the US census.** The Census Bureau swapped the geography of a part of the households between areas, with households matched on some attributes, in the censuses of 1990, 2000 and 2010. The swap rate was not published. For 2020 the Bureau changed to a [differentially private](/differential-privacy-definition/) method, and its handbook gives the risk of reconstruction from many published tables as a reason. See the [Dinur-Nissim reconstruction theorem](/dinur-nissim-reconstruction-attack/) for why many accurate tables allow reconstruction.
- **Rank swapping** of numerical microdata, as above. It is one of the masking methods in the mu-Argus software and in the textbook of Hundepool et al. (2012), together with [microaggregation](/microaggregation/).
- **The post-randomization method.** [PRAM](/post-randomization-method/) replaces a categorical value by a random value from a published matrix. It is the probabilistic relative of swapping. Because the matrix is public, an analyst can correct the counts, which is not possible with a secret swap rate.
- **[Randomized response](/randomized-response/).** The same idea of a planned random change, but done by the respondent before the data is collected.

## Variations

- **Swap more than one attribute.** Swap all the attributes of $A$ together, so that their joint counts stay the same.
- **Swap within a stratum.** Restrict partners to the same larger area, so that counts at the larger level stay exact and only the small areas change.
- **Rank swapping of several attributes.** Swap each numerical attribute on its own ranks. The marginal distribution of each attribute is exactly kept, but the correlations go down as $p$ grows.
- **Data shuffling.** Replace the values of a sensitive numerical attribute by a permutation of the original values chosen through a model of the other attributes. This is a later relative of rank swapping, outside the scope of this page.

## Pitfalls

- **A low swap rate leaves most records true.** With a swap rate of a few percent, most records are exactly right, and a person who links a record is right most of the time. Targeted swapping helps for the risky records only.
- **A secret swap rate blocks corrections.** If the rate and the key are secret, an analyst cannot correct the counts that the swap changed, and the size of the bias is unknown. If they are public, the analyst knows how much to trust each count, but an attacker knows it too.
- **Rank swapping with a small window.** With $p$ small, the released value is close to the true one. An attacker who links a record learns the value up to the window. This is a disclosure of an interval, not of an exact value, but it can still be harmful.
- **Joint counts outside the key move.** Tables of an area by an attribute outside $M$ are biased. Small areas suffer most, because a few swaps are a large part of their records.
- **Swapping is not differential privacy.** The swap depends on the records, and the swapped values are real values of other people. No bound limits what an attacker with many published tables learns.

## Exercises

1. Prove the three statements of the template on what a swap with key $M$ keeps.
2. In the example table, list all pairs of households that can swap their area with $M = \{\text{size}\}$, and the pairs that also keep the counts by area and tenure.
3. Rank swapping with $p$ percent swaps each value with one of rank at most $p n / 100$ above it. Show that the mean and the sorted list of values do not change. Give the largest possible change of one value in terms of the gaps between sorted values.
4. Explain why the counts of the original method of Dalenius and Reiss, for all combinations of up to $t$ attributes, are harder to keep than the counts of a fixed key $M$.

## References
