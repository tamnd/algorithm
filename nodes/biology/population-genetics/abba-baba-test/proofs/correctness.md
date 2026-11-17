---
title: The counts, the leave-one-out values and the jackknife variance are computed exactly, and under the null model ABBA and BABA have the same expected count
proves: [correctness]
status: full
---

**Setting.** Sites $s = 1, \ldots, n$ carry frequencies $p_{1s}, \ldots, p_{4s} \in [0, 1]$ of allele B in samples of $P_1, P_2, P_3, O$. The blocks $J_1, \ldots, J_g$ partition the sites. $\text{ABBA}_s = (1 - p_{1s}) p_{2s} p_{3s} (1 - p_{4s})$ and $\text{BABA}_s = p_{1s} (1 - p_{2s}) p_{3s} (1 - p_{4s})$.

**Lemma 1 (single sequences).** If every $p_{is} \in \{0, 1\}$ and $p_{4s} = 0$, then $\text{ABBA}_s = 1$ exactly when the site has the pattern ABBA (with A the allele of $O$), and 0 otherwise; the same holds for BABA.

*Proof.* With $p_{4s} = 0$, the product $(1 - p_{1s}) p_{2s} p_{3s}$ is 1 exactly when $p_{1s} = 0$ and $p_{2s} = p_{3s} = 1$, that is, when $P_1$ has the allele of $O$ and $P_2$ and $P_3$ have the other allele. The BABA case is the same with $P_1$ and $P_2$ swapped. The function count_patterns tests the same conditions on the raw alleles, and polarize codes each allele as 1 when it differs from that of $O$. $\square$

**Lemma 2 (sampling).** Draw one sequence from each sample, independently, each carrying B with probability $p_{is}$. Then $P(\text{pattern ABBA at } s) = \text{ABBA}_s$ and $P(\text{BABA at } s) = \text{BABA}_s$.

*Proof.* The four draws are independent, and ABBA means A in $P_1$, B in $P_2$, B in $P_3$ and A in $O$. Multiply the four probabilities. $\square$

**Lemma 3 (the numerator).** $\text{ABBA}_s - \text{BABA}_s = (p_{2s} - p_{1s}) p_{3s} (1 - p_{4s})$. If $p_{4s} = 0$, this equals $(p_{2s} - p_{1s})(p_{3s} - p_{4s})$, the summand of $f_4(P_2, P_1; P_3, O)$.

*Proof.* $(1 - p_1) p_2 - p_1 (1 - p_2) = p_2 - p_1$. $\square$

**Lemma 4 (leave-one-out values).** Let $a_j = \sum_{s \in J_j} \text{ABBA}_s$, $b_j = \sum_{s \in J_j} \text{BABA}_s$, $A = \sum_j a_j$ and $B = \sum_j b_j$. The value of $D$ on the sites outside $J_j$ is $((A - a_j) - (B - b_j)) / ((A - a_j) + (B - b_j))$.

*Proof.* The sums over the sites outside $J_j$ are $A - a_j$ and $B - b_j$, because the blocks are disjoint and cover all sites. $\square$

Line L6 uses this form, and the code gets the same numbers by summing the remaining blocks. Line L7 is the delete-one jackknife variance $\frac{g - 1}{g} \sum_j (D_{(j)} - \bar D_{(\cdot)})^2$.

**Lemma 5 (scaling of the jackknife).** If the statistic is the mean of $g$ block values $x_1, \ldots, x_g$, the jackknife variance equals $s^2 / g$, where $s^2 = \frac{1}{g - 1} \sum_j (x_j - \bar x)^2$ is the sample variance.

*Proof.* The value without block $j$ is $\bar x_{(j)} = (g \bar x - x_j)/(g - 1)$, so $\bar x_{(j)} - \bar x_{(\cdot)} = -(x_j - \bar x)/(g - 1)$, where $\bar x_{(\cdot)} = \bar x$. Then $\frac{g - 1}{g} \sum_j (x_j - \bar x)^2 / (g - 1)^2 = \frac{1}{g (g - 1)} \sum_j (x_j - \bar x)^2 = s^2 / g$. $\square$

So the factor $(g - 1)/g$ makes the jackknife agree with the usual standard error in the linear case. For the ratio $D$, the jackknife variance is a consistent estimate when the blocks are independent and many, which is an asymptotic statement, not one proved here.

**The null model.** One gene copy is sampled from each of $P_1$, $P_2$, $P_3$ and $O$, with the copies of $P_1$ and $P_2$ sampled at the same time. The populations form the rooted tree $(((P_1, P_2), P_3), O)$ with no gene flow after any split. Each ancestral population mates at random, so the lineages in it coalesce by the Kingman coalescent, with all pairs equally likely to join next. Mutations fall on the branches of the gene tree as a Poisson process whose rate does not depend on the labels of the lineages, with at most one mutation per site (infinite sites). This is the multispecies coalescent with infinite sites.

**Theorem (equal expected counts).** Under the null model, at every site, $P(\text{ABBA}) = P(\text{BABA})$.

*Proof.* With one mutation at the site, the pattern is set by the branch $e$ of the gene tree that carries the mutation: the copies below $e$ carry B, the others A. An ABBA site needs a branch whose set of copies below it is $\{2, 3\}$ (or, for an unrooted reading with $O$ below the mutation, $\{1, O\}$; both split $\{2, 3\}$ from $\{1, O\}$). BABA needs a branch that splits $\{1, 3\}$ from $\{2, O\}$.

Let $C$ be the event that the lineages of $P_1$ and $P_2$ coalesce in the ancestral population of $P_1$ and $P_2$. On $C$, copies 1 and 2 form a clade in the gene tree, so no branch splits $\{2, 3\}$ from $\{1, O\}$, and no branch splits $\{1, 3\}$ from $\{2, O\}$. Both patterns have probability 0 on $C$.

On the complement of $C$, lineages 1 and 2 enter the ancestral population of $P_1$, $P_2$ and $P_3$ as two distinct lineages, and from then on they are in the same populations at all times. The law of the rest of the genealogy, of the branch lengths and of the mutations is invariant under the exchange of labels 1 and 2: each coalescence picks a pair uniformly at random, the times do not depend on the labels, and the mutation rate does not depend on the labels. The history of the two lineages before they entered that population is also exchangeable: each is a single lineage from its sampling time to the split of $P_1$ and $P_2$, and these times are equal, and under $C^c$ the two lineages then stay apart in the ancestor of $P_1$ and $P_2$ for the same length of time. So the map that swaps labels 1 and 2 preserves the law of the whole history on $C^c$, and it maps the event "the mutation splits $\{2, 3\}$ from $\{1, O\}$" onto the event "the mutation splits $\{1, 3\}$ from $\{2, O\}$". The two events have the same probability. $\square$

With frequency data, Lemma 2 writes $E[\text{ABBA}_s - \text{BABA}_s]$, taken over the sampling of sequences from populations that follow the null model, as the difference of the probabilities in the theorem, so the expected numerator of $D$ is 0. The theorem uses each assumption of the null model: gene flow into $P_2$ from $P_3$, structure in the ancestor of $P_1$ and $P_2$ that places $P_2$ closer to $P_3$, or a mutation rate that differs between the lineages of $P_1$ and $P_2$ all break the exchange of labels, and then $E[\text{ABBA}] \ne E[\text{BABA}]$ is possible.
