---
tag: 4AARD3
kind: definition
slug: t-closeness
name: t-closeness
aliases:
- t-close table
area: security-and-privacy/data-anonymization
level: core
summary: Requires the sensitive attribute distribution in each group to be within earth mover's distance t of its distribution in the whole table.
prereqs: [l-diversity, k-anonymity, total-variation-distance]
see_also: [l-diversity, k-anonymity, anatomy-bucketization, m-invariance, total-variation-distance, kullback-leibler-divergence, incognito, differential-privacy-definition]
sources:
  - paper: doi:10.1109/icde.2007.367856
    title: "Ninghui Li, Tiancheng Li and Suresh Venkatasubramanian, t-closeness: privacy beyond k-anonymity and l-diversity, 23rd International Conference on Data Engineering (ICDE 2007), pages 106-115"
    locator: Section 3 (the skewness and similarity attacks on l-diversity), Section 4 (Definition 2, the earth mover's distance, Facts 1 and 2, the generalization and subset properties) and Section 5 (the ordered, equal and hierarchical distances)
  - paper: doi:10.1023/A:1026543900054
    title: "Yossi Rubner, Carlo Tomasi and Leonidas J. Guibas, The earth mover's distance as a metric for image retrieval, International Journal of Computer Vision 40(2), 2000, pages 99-121"
    locator: the earth mover's distance as a transportation problem between two distributions over a space with a ground distance
  - paper: doi:10.1109/icde.2006.1
    title: "Ashwin Machanavajjhala, Johannes Gehrke, Daniel Kifer and Muthuramakrishnan Venkitasubramaniam, l-diversity: privacy beyond k-anonymity, ICDE 2006, page 24"
    locator: the l-diversity principle that t-closeness refines
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing: a survey of recent developments, ACM Computing Surveys 42(4), article 14, 2010"
    locator: the privacy models against attribute linkage, including t-closeness and its criticism
---

t-closeness is a condition on a released table that limits what the table tells about the sensitive value of one person beyond what it tells about the whole population. Li, Li and Venkatasubramanian (ICDE 2007) showed that [l-diversity](/l-diversity/) can fail in two ways: a block can be diverse but far more likely to hold a rare value than the table as a whole (the skewness attack), and a block can hold distinct values that all mean nearly the same thing (the similarity attack). t-closeness asks that, in each block, the distribution of the sensitive attribute be within distance $t$ of its distribution in the whole table. The distance is the earth mover's distance (also called the Wasserstein distance, a transportation cost), so values that are close in meaning count as close. The threshold $t$ is a policy choice. Like l-diversity, t-closeness is a property of one released table, not of the release mechanism.

## Definition

A table $T$ has quasi-identifier attributes $Q$ and a sensitive attribute $S$ with domain $\{v_1, \ldots, v_m\}$. A **block** (equivalence class) is a maximal set of rows with the same values on $Q$. Let $W = (w_1, \ldots, w_m)$ be the distribution of $S$ in the whole table, and $P = (p_1, \ldots, p_m)$ its distribution in a block $E$.

**Definition (Li, Li and Venkatasubramanian, Definition 2).** A block has **t-closeness** if $D[P, W] \le t$. A table has t-closeness if all its blocks have it. Here $D$ is the earth mover's distance for a ground distance $d_{ij}$ between values with $0 \le d_{ij} \le 1$:
$$D[P, W] = \min_{f} \sum_{i=1}^{m} \sum_{j=1}^{m} d_{ij} f_{ij} \quad \text{subject to} \quad f_{ij} \ge 0,\ \ \sum_j f_{ij} = p_i,\ \ \sum_i f_{ij} = w_j .$$
A flow $f$ moves mass $f_{ij}$ from value $i$ of $P$ to value $j$ of $W$, and $D$ is the least total work. With $0 \le d_{ij} \le 1$, $0 \le D \le 1$ (Fact 1 of the paper), so $t$ lies in $[0, 1]$.

The paper uses three ground distances, each with a closed formula (Section 5):

- **Ordered distance**, for a numeric or ordered attribute with $v_1 < \cdots < v_m$: $d_{ij} = |i - j| / (m - 1)$. Then, with $r_i = p_i - w_i$,
$$D[P, W] = \frac{1}{m - 1} \sum_{i=1}^{m-1} \Big| \sum_{j=1}^{i} r_j \Big| .$$
Each term is the mass that must cross the gap between $v_i$ and $v_{i+1}$.
- **Equal distance**, for a categorical attribute with no structure: $d_{ij} = 1$ for $i \ne j$. Then $D[P, W] = \frac12 \sum_i |p_i - w_i|$, which is the [total variation distance](/total-variation-distance/).
- **Hierarchical distance**, for a categorical attribute with a generalization tree of height $H$: the distance between two leaves is the height of their lowest common ancestor divided by $H$. The paper gives a formula that sums the excess mass of each internal node.

Facts, each a theorem:

- **Merging keeps t-closeness** (Fact 2 of the paper). If $P_1$ and $P_2$ are the distributions of two blocks $E_1$ and $E_2$, the distribution of the merged block is $P = \lambda P_1 + (1 - \lambda) P_2$ with $\lambda = |E_1| / (|E_1| + |E_2|)$, and $D[P, W] \le \lambda D[P_1, W] + (1 - \lambda) D[P_2, W] \le \max(D[P_1, W], D[P_2, W])$. The reason: mixing the two best flows with weights $\lambda$ and $1 - \lambda$ gives a flow for $P$. So a coarser generalization of a t-close table is t-close, and the lattice searches that need monotonicity, such as [Incognito](/incognito/), work.
- **The extreme cases.** $t = 0$ forces every block to have the distribution $W$, which is the same as publishing $W$ and no link between the quasi-identifiers and $S$. $t = 1$ allows every table. Putting all rows in one block always gives $D = 0$.
- **t-closeness does not imply l-diversity.** If one value has $w_1 = 0.99$, a block made only of $v_1$ has equal distance $\tfrac12 (0.01 + 0.01) = 0.01$ to $W$, so it is $0.01$-close and holds one value. Such a block tells an attacker little beyond the population, because nearly everyone has $v_1$; whether that is acceptable is again a policy choice.

proofs/correctness.md proves the ordered formula and the merging fact, and that the test below is exact. The test computes the running sum of $p_i - w_i$ in one pass per block.

```pseudo id=main
T-CLOSE(T, Q, S, t)                ▷ S takes the ordered values v_1 < ... < v_m, with m ≥ 2
L1  W ← the distribution of S in the whole table T
L2  for each block E of T under Q do
L3      P ← the distribution of S in E
L4      run ← 0, d ← 0
L5      for i ← 1 to m − 1 do
L6          run ← run + P[i] − W[i]
L7          d ← d + |run|
L8      if d / (m − 1) > t then return false
L9  return true
```

For $n$ rows and $g$ blocks, the test takes $O(n + g m)$ time in the word-RAM model with exact rational arithmetic, after the blocks are found by hashing. The code also has the equal distance, which replaces lines L4 to L8 by half the sum of $|P[i] - W[i]|$. A general ground distance needs a transportation solver, for example the [min-cost flow](/min-cost-flow-problem/) of the paper's Section 5.

## Examples and non-examples

The table is Table 4 of Li, Li and Venkatasubramanian: nine synthetic records in three blocks, with Salary as the sensitive attribute. The salaries are $3k, 4k, \ldots, 11k$, once each, so $W$ is uniform with $w_i = 1/9$ and $m = 9$. The values below were computed exactly with fractions.

| block | salaries | ordered $D[P, W]$ | equal $D[P, W]$ |
|---|---|---|---|
| $E_1$ | 3k, 4k, 5k | $3/8 = 0.375$ | $2/3$ |
| $E_2$ | 6k, 8k, 11k | $1/6 \approx 0.167$ | $2/3$ |
| $E_3$ | 7k, 9k, 10k | $17/72 \approx 0.236$ | $2/3$ |

- **The similarity attack, measured.** The table is distinct 3-diverse, but $E_1$ tells an attacker that its members have low salaries. The ordered distance sees this: $E_1$ is the farthest block from $W$. The running sums for $E_1$ are $\tfrac{2}{9}, \tfrac{4}{9}, \tfrac{6}{9}, \tfrac{5}{9}, \tfrac{4}{9}, \tfrac{3}{9}, \tfrac{2}{9}, \tfrac{1}{9}$, whose sum is $27/9 = 3$, and $3 / 8 = 0.375$. So the table is $0.375$-close and not $0.3$-close.
- **The equal distance is blind here.** Each block has three of the nine values with mass $1/3$ each, so the total variation to $W$ is $\tfrac12 (3 \cdot \tfrac29 + 6 \cdot \tfrac19) = \tfrac23$ for all three blocks. A distance that treats 3k and 11k as just two labels cannot tell $E_1$ from $E_2$. The paper also notes that the Kullback-Leibler divergence has the same problem.
- **The skewness attack, measured.** A test result has 99 percent negative records. A block with 50 percent positive records has equal distance $|0.5 - 0.01| = 0.49$ to $W$, so it is not $0.1$-close, although it is 2-diverse in all three senses of l-diversity.
- **Merging.** $E_1 \cup E_2$ has distance at most $\tfrac12 (0.375 + 0.167) \approx 0.271$ by the merging fact. All three blocks together give the distribution $W$ and distance 0.
- **Non-example: a numeric attribute with the equal distance.** Using the equal distance for salaries makes t-closeness blind to the similarity attack, as the table shows. Use the ordered distance, or a hierarchy, when the values have meaning.

## Related definitions

- [l-diversity](/l-diversity/): the condition t-closeness refines. l-diversity asks for many values in a block; t-closeness asks for a block that looks like the table.
- [k-anonymity](/k-anonymity/): t-closeness is used together with it, because t-closeness alone does not bound the size of a block from below.
- [Total variation distance](/total-variation-distance/): the earth mover's distance under the equal ground distance. The [Kullback-Leibler divergence](/kullback-leibler-divergence/) is another distance the paper considers and rejects, because it ignores the ground distance.
- [Anatomy](/anatomy-bucketization/) and [m-invariance](/m-invariance/): other models for the sensitive values, for one release without generalization and for a sequence of releases.
- [Differential privacy](/differential-privacy-definition/): a condition on the mechanism that holds against every background knowledge. t-closeness bounds only the gap between the block and the table, and it assumes that the attacker's knowledge about the population is the table distribution $W$.

## References
