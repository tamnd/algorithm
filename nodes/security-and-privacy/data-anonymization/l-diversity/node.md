---
tag: HGM0PD
kind: definition
slug: l-diversity
name: l-diversity
aliases:
- l-diverse table
area: security-and-privacy/data-anonymization
level: core
summary: Requires each group of records with the same quasi-identifiers to hold at least l well-represented values of the sensitive attribute.
prereqs: [k-anonymity, quasi-identifier, shannon-entropy]
see_also: [t-closeness, anatomy-bucketization, m-invariance, k-anonymity, linkage-attack, generalization-and-suppression, incognito, mondrian-anonymization]
sources:
  - paper: doi:10.1109/icde.2006.1
    title: "Ashwin Machanavajjhala, Johannes Gehrke, Daniel Kifer and Muthuramakrishnan Venkitasubramaniam, l-diversity: privacy beyond k-anonymity, 22nd International Conference on Data Engineering (ICDE 2006), page 24"
    locator: the homogeneity and background knowledge attacks on k-anonymity, the l-diversity principle, and its entropy and recursive (c, l) instances
  - paper: doi:10.1145/1217299.1217302
    title: "Ashwin Machanavajjhala, Daniel Kifer, Johannes Gehrke and Muthuramakrishnan Venkitasubramaniam, l-diversity: privacy beyond k-anonymity, ACM Transactions on Knowledge Discovery from Data 1(1), article 3, 2007"
    locator: the journal version, with Bayes-optimal privacy as the motivation, the monotonicity of the instances, and the use of l-diversity inside Incognito
  - paper: doi:10.1109/icde.2007.367856
    title: "Ninghui Li, Tiancheng Li and Suresh Venkatasubramanian, t-closeness: privacy beyond k-anonymity and l-diversity, ICDE 2007, pages 106-115"
    locator: Section 3 (the limits of l-diversity, with the skewness attack and the similarity attack, and Example 2 on a skewed test result)
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing: a survey of recent developments, ACM Computing Surveys 42(4), article 14, 2010"
    locator: the privacy models against attribute linkage, which compare l-diversity with its variants and with t-closeness
---

l-diversity is a condition on a released table that protects the sensitive values, not only the identities. [k-anonymity](/k-anonymity/) makes each record look like at least $k - 1$ others on the [quasi-identifier](/quasi-identifier/), so a [linkage attack](/linkage-attack/) can only find a group of records. But if all records of that group have the same diagnosis, the attacker learns the diagnosis anyway. Machanavajjhala, Gehrke, Kifer and Venkitasubramaniam (ICDE 2006) named this the homogeneity attack, and they asked that each group hold at least $l$ "well-represented" sensitive values. They gave three exact meanings of "well-represented": distinct, entropy and recursive $(c, l)$. The value of $l$, and of $c$, is a policy choice of the publisher, not a result. l-diversity is a syntactic condition on one release; it gives no bound of the kind that [differential privacy](/differential-privacy-definition/) gives, and [t-closeness](/t-closeness/) shows two attacks that it does not stop.

## Definition

A table $T$ has a set $Q$ of quasi-identifier attributes and one sensitive attribute $S$. The rows of $T$ that have the same values on $Q$ form a **block** (the paper says a $q^\star$-block; other papers say an equivalence class). For a block $E$ and a sensitive value $s$, let $n(E, s)$ be the number of rows of $E$ with value $s$, and let $p(E, s) = n(E, s) / |E|$. Sort the counts of the values that occur in $E$ as $r_1 \ge r_2 \ge \cdots \ge r_m > 0$, so $m$ is the number of distinct sensitive values in $E$ and $r_1 + \cdots + r_m = |E|$.

**The principle.** A block is $l$-diverse if it holds at least $l$ well-represented values of $S$. A table is $l$-diverse if every block is $l$-diverse. The three instances below make "well-represented" exact. Each one is a property of single blocks, so a table has it if and only if every block has it.

1. **Distinct $l$-diversity.** $m \ge l$: the block holds at least $l$ distinct sensitive values.
2. **Entropy $l$-diversity.** The [Shannon entropy](/shannon-entropy/) of the block is at least $\log l$:
$$H(E) = -\sum_{s} p(E, s) \log p(E, s) \ \ge\ \log l.$$
The base of the logarithm does not matter, as long as both sides use the same base. Multiply by $|E|$ and take exponentials: the condition is the same as the integer test $|E|^{|E|} \ge l^{|E|} \, r_1^{r_1} r_2^{r_2} \cdots r_m^{r_m}$, which needs no floating point.
3. **Recursive $(c, l)$-diversity.** For a constant $c > 0$,
$$r_1 < c \, (r_l + r_{l+1} + \cdots + r_m).$$
The most frequent value must not be too frequent compared with the tail that remains after the $l - 1$ most frequent values. If $m < l$ the tail is empty, the right side is 0, and the block fails.

Some facts follow at once, and each is a theorem:

- **Entropy and recursive imply distinct.** $H(E) \le \log m$, with equality for the uniform distribution, so $H(E) \ge \log l$ forces $m \ge l$. A recursive $(c, l)$-diverse block has a non-empty tail, so $m \ge l$.
- **A bound on the whole table.** The distribution of $S$ in $T$ is the mixture of the block distributions, with weights $|E| / |T|$. Entropy is concave, so $H(T) \ge \sum_E \frac{|E|}{|T|} H(E)$. If each block has $H(E) \ge \log l$, then $H(T) \ge \log l$. A table whose sensitive column has low entropy can be entropy $l$-diverse only for a small $l$, whatever the anonymization does.
- **Monotonicity.** If two blocks are $l$-diverse in one of the three senses, then the block made by merging them is $l$-diverse in the same sense. For entropy this is the concavity again. For the recursive form it holds because $r_1$ and the sum of the $l - 1$ largest counts are both subadditive under merging. So a coarser generalization of an $l$-diverse table is $l$-diverse, and the lattice searches that prune by monotonicity, such as [Incognito](/incognito/), work for l-diversity as they do for k-anonymity.
- **Background knowledge in the recursive form.** Suppose a block is recursive $(c, l)$-diverse and the attacker can rule out one sensitive value for the target, for example because the target is male and the value is a pregnancy. Remove that value from the block. The rest is recursive $(c, l - 1)$-diverse. If the removed value had rank 1, the new largest count is $r_2 \le r_1$ and the new tail is the old tail. If it had rank $j \ge 2$, the largest count is still $r_1$, and the new tail is the old tail, or the old tail with $r_j$ replaced by $r_{l-1} \ge r_j$. So an attacker who can rule out $l - 2$ values still faces a $(c, 2)$-diverse block, in which the most frequent value has fewer than $c$ times the rows of all the others.

proofs/correctness.md proves the monotonicity and the test below. The test reads each row once, groups the rows by their quasi-identifier values, and checks each block.

```pseudo id=main
L-DIVERSE(T, Q, S, l, variant, c)
L1  B ← the blocks of T: the groups of rows with equal values on Q
L2  for each block E in B do
L3      r_1 ≥ r_2 ≥ ... ≥ r_m ← the counts of the distinct values of S in E
L4      if variant = distinct and m < l then return false
L5      if variant = entropy and |E|^|E| < l^|E| · r_1^r_1 ⋯ r_m^r_m then return false    ▷ the same as H(E) < log l
L6      if variant = recursive and r_1 ≥ c · (r_l + ... + r_m) then return false
L7  return true
```

With a hash table for the blocks, line L1 takes $O(n)$ expected time for $n$ rows with a fixed number of quasi-identifiers, in the word-RAM model. Line L3 sorts the counts, $O(m \log m)$ per block and $O(n \log n)$ in total. Line L5 multiplies integers with up to $O(|E| \log |E|)$ bits, which is cheap for the small blocks that releases use; a floating point version with a tolerance is the usual choice for large blocks.

## Examples and non-examples

The table below is synthetic. It is already generalized: Age and ZIP code are the quasi-identifiers, and the disease is sensitive. It has three blocks of 4 rows, so it is 4-anonymous.

| block | Age | ZIP | diseases | counts $r_1, r_2, \ldots$ |
|---|---|---|---|---|
| $E_1$ | < 30 | 130** | heart, heart, heart, heart | 4 |
| $E_2$ | ≥ 40 | 1485* | flu, heart, cancer, flu | 2, 1, 1 |
| $E_3$ | 3* | 130** | flu, cancer, viral, heart | 1, 1, 1, 1 |

- **$E_1$ is the homogeneity attack.** An attacker who knows that a neighbour is under 30, lives in 130**, and is in the table, learns that the neighbour has heart disease, although the table is 4-anonymous. $E_1$ has $m = 1$, so the table is not even distinct 2-diverse.
- **$E_2$.** Distinct: $m = 3$. Entropy: $H(E_2) = -(\tfrac12 \log_2 \tfrac12 + 2 \cdot \tfrac14 \log_2 \tfrac14) = 1.5$ bits, and $2^{1.5} \approx 2.83$, so $E_2$ is entropy $l$-diverse for $l = 2$ but not for $l = 3$. The integer test for $l = 2$ reads $4^4 = 256 \ge 2^4 \cdot 2^2 \cdot 1 \cdot 1 = 64$. Recursive: for $l = 2$ the condition is $2 < c \cdot (1 + 1)$, true for every $c > 1$; for $l = 3$ it is $2 < c \cdot 1$, so $E_2$ is $(3, 3)$-diverse but not $(2, 3)$-diverse.
- **$E_3$.** All four values differ, $H(E_3) = 2$ bits, and $E_3$ is $l$-diverse in every sense for each $l \le 4$ (recursive with any $c > 1$).
- **A repair by merging.** Generalize Age in $E_1$ and $E_2$ to "any" and ZIP to 1****. The merged block has counts 5 (heart), 2 (flu), 1 (cancer). Its entropy is $1.299$ bits, and $2^{1.299} \approx 2.46$, so it is entropy 2-diverse. Monotonicity does not predict this, because $E_1$ was not 2-diverse; the merge works because $E_2$ brings enough other values. The merged block is recursive $(c, 2)$-diverse for $c > 5/3$ (the test is $5 < 3c$) and recursive $(c, 3)$-diverse only for $c > 5$.
- **l = 1.** Every non-empty block is 1-diverse in all three senses, so 1-diversity adds nothing to k-anonymity.
- **The skewness attack (a non-example of protection).** Li, Li and Venkatasubramanian take a test result with 99 percent negative and 1 percent positive records. A block with 50 percent positive records is distinct, entropy and recursive 2-diverse, yet it raises the chance that a member is positive from 1 percent to 50 percent. A block with 49 positive and 1 negative records is distinct 2-diverse and has the same entropy as one with 1 positive and 49 negative. Their Example 2 also notes that a distinct 2-diverse version of a table of 10000 such records can have at most $10000 \times 1\% = 100$ blocks, because each block needs a positive record, so the information loss is large.
- **The similarity attack (a non-example of protection).** A block with the diseases gastric ulcer, gastritis and stomach cancer is distinct 3-diverse, but each value is a stomach disease, so the attacker learns that. The salaries 3k, 4k and 5k in one block are distinct, but all low. l-diversity treats the values as labels with no distance between them.

## Related definitions

- [k-anonymity](/k-anonymity/): the condition that l-diversity extends. Distinct $l$-diversity of a block with $m$ values implies that the block has at least $l$ rows, so a distinct $l$-diverse table is $l$-anonymous.
- [Quasi-identifier](/quasi-identifier/) and [linkage attack](/linkage-attack/): the attributes that define the blocks, and the attack that k-anonymity stops and l-diversity extends to sensitive values.
- [t-closeness](/t-closeness/): asks that the distribution of $S$ in each block be close to its distribution in the whole table, under the earth mover's distance. It answers the skewness and similarity attacks above.
- [Anatomy](/anatomy-bucketization/): releases the quasi-identifiers and the sensitive values in two tables joined by a group id, with $l$-diverse groups, and gives a breach probability of at most $1/l$ without generalization.
- [m-invariance](/m-invariance/): l-diversity for a table that is released again after insertions and deletions; each single release can be $l$-diverse and the sequence can still leak.
- [Generalization and suppression](/generalization-and-suppression/), [Incognito](/incognito/) and [Mondrian](/mondrian-anonymization/): the methods that produce the blocks; each can test l-diversity in place of k-anonymity.
- [Differential privacy](/differential-privacy-definition/): a condition on the release mechanism, not on the released table, that holds against every background knowledge.

## References
