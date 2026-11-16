---
tag: SJX398
kind: concept
slug: fine-grained-equivalence-class
name: Fine-grained equivalence class
aliases:
- fine-grained equivalence
area: complexity/fine-grained-complexity
level: advanced
summary: "A set of problems with fine-grained reductions in both directions between any two, so that a polynomial speedup for one gives a polynomial speedup for all."
prereqs: [fine-grained-reduction, conditional-lower-bound]
see_also: [fine-grained-reduction, apsp-negative-triangle-equivalence, apsp-conjecture, 3sum, convolution-3sum, min-plus-convolution, online-matrix-vector-multiplication, 3sum-hardness]
sources:
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010, 645-654)"
    locator: the abstract and the definition of subcubic reductions (the class of problems equivalent to APSP); the page relies on the journal version
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the definition of fine-grained reductions and the overview of the classes around 3SUM, APSP and SETH
  - paper: doi:10.1145/3293465
    title: "Marek Cygan, Marcin Mucha, Karol Węgrzycki and Michał Włodarczyk, On problems equivalent to (min,+)-convolution, ACM Transactions on Algorithms 15(1), 2019, article 14 (conference version in ICALP 2017, LIPIcs 80, 22:1-22:15; arXiv:1702.07669)"
    locator: Theorem 2 and Figure 2 of the arXiv version (the class of min-plus convolution)
  - paper: arxiv:1511.06773
    title: "Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, STOC 2015, 21-30"
    locator: Theorem 2.7, Lemma 2.11 and Theorem 2.12 of the arXiv version (OMv, OuMv and their equivalent query problems)
  - paper: doi:10.1137/1.9781611976014.1
    title: "Timothy M. Chan and Qizheng He, Reducing 3SUM to Convolution-3SUM, Symposium on Simplicity in Algorithms (SOSA 2020), 1-7"
    locator: the deterministic reduction from 3SUM to Convolution 3SUM, which completes the deterministic equivalence
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract and the introduction (truly subquadratic 3SUM and truly subcubic APSP, which bring down the 3SUM, APSP and min-plus convolution classes); not yet refereed
---

A fine-grained equivalence class is a set of problems, each with a time bound, such that between any two of them there are [fine-grained reductions](/fine-grained-reduction/) in both directions. Then either every problem in the class has an algorithm that saves a polynomial factor over its bound, or none does. The first large class was found by Vassilevska Williams and Williams in 2010: all-pairs shortest paths, negative triangle detection and several other path and matrix problems are equivalent with respect to time $n^{3-\varepsilon}$.

Classes are the reason that a few hypotheses cover many problems. They also mean that one new algorithm can move a whole class at once. In October 2026, a preprint of Alman and Vassilevska Williams gave truly subquadratic 3SUM and truly subcubic APSP. If it is correct, every member of the 3SUM class and of the APSP class has a truly faster algorithm, and so does every member of the min-plus convolution class.

The single reduction is on [fine-grained reduction](/fine-grained-reduction/). This page is about what you get when the reductions go both ways, and which classes are known.

## In plain words

Suppose you have two puzzles. If a fast method for the first puzzle gives you a fast method for the second, and a fast method for the second gives you one for the first, then the two puzzles are equally hard, at least for this purpose. A group of puzzles that are all equally hard in this way is a class.

A class is useful in two ways. If you believe that one member is hard, you must believe that all of them are hard. And if someone finds a fast method for one member, everyone in the group gets a fast method.

A puzzle that is only known to be at least as hard as the members is not in the class. A fast method for the class does not help it.

## The idea

### Definition

Let $A$ have the time bound $a(n)$ and $B$ the time bound $b(n)$. The pair is fine-grained equivalent if $A$ is $(a, b)$-reducible to $B$ and $B$ is $(b, a)$-reducible to $A$. Then:

- If $B$ has an $O(b(n)^{1-\varepsilon})$ algorithm for some $\varepsilon > 0$, then $A$ has an $O(a(n)^{1-\delta})$ algorithm for some $\delta > 0$.
- If $A$ has an $O(a(n)^{1-\varepsilon})$ algorithm for some $\varepsilon > 0$, then $B$ has an $O(b(n)^{1-\delta})$ algorithm for some $\delta > 0$.

The relation is reflexive and symmetric. It is transitive because fine-grained reductions compose, so it splits problems into classes. Vassilevska Williams and Williams call the case $a(n) = b(n) = n^3$ subcubic equivalence, and the case $n^2$ is called subquadratic equivalence.

### What "equivalent" does not mean

- **Not the same exponent.** The $\delta$ may be smaller than the $\varepsilon$. An equivalence says that both problems are truly faster or neither is. It does not say that the best exponents are equal.
- **Not the same in every model.** Each reduction is stated in a model, often the word RAM, and may be randomized. If one direction is randomized, the class is a class for randomized algorithms. For example, 3SUM and Convolution 3SUM were equivalent only for randomized algorithms from 2010, when Pătraşcu gave a randomized reduction, until 2020, when Chan and He gave a deterministic one.
- **Not hardness.** Hard for a class means a reduction from the class to the problem, in one direction only. [3SUM-hardness](/3sum-hardness/) is the main example. An equivalence needs the reduction back.

### Known classes

| Class | Time bound | Members (examples) | Directions randomized | Status in 2026 |
|---|---|---|---|---|
| APSP | $n^3$ | APSP, min-plus matrix product, negative triangle, listing up to $n^{2.99}$ negative triangles, minimum weight cycle, replacement paths, second shortest simple path, metricity, verifying a min-plus product | none | truly subcubic in the AVW preprint |
| 3SUM | $n^2$ | 3SUM in one set and in three sets, the sum form $a + b = c$, Convolution 3SUM, GeomBase | none since 2020 | truly subquadratic in the AVW and CIMY preprints |
| min-plus convolution | $n^2$, or $(n+t)^2$ | min-plus and max-plus convolution, its upper bound test, superadditivity test, unbounded and 0/1 knapsack, maximum consecutive subsums, tree sparsity | one step (0/1 knapsack to max-plus convolution) | truly subquadratic through 3SUM, for numbers bounded by a polynomial |
| OMv | $n^3$ in total | OMv, OuMv, and the independent set, 2-CNF and edge query problems | none | open |

AVW is Alman and Vassilevska Williams (arXiv:2610.06783) and CIMY is Chan, Itakura, Ma and Yu (arXiv:2610.42012). Both are not yet refereed. The APSP list is from the abstract of Vassilevska Williams and Williams, plus the [min-plus matrix product](/min-plus-matrix-multiplication/), whose equivalence with APSP is classical. The min-plus convolution list is Theorem 2 and Figure 2 of Cygan, Mucha, Węgrzycki and Włodarczyk. The OMv list is from Henzinger, Krinninger, Nanongkai and Saranurak (STOC 2015), whose Theorem 2.12 shows that OuMv is equivalent to independent set queries, 2-CNF queries and edge queries.

### Links between the classes

The classes are joined by reductions in one direction only:

- Min-plus convolution reduces to APSP (Bremner et al.) and to 3SUM (Cygan et al., Appendix A). No reduction back is known, so it is a separate class.
- 3SUM and APSP both reduce to the exact (zero-weight) triangle problem. No reduction is known between 3SUM and APSP.
- No reduction is known between any of these classes and SETH or [Orthogonal Vectors](/orthogonal-vectors/).

So a fast algorithm for exact triangle would give fast algorithms for both 3SUM and APSP, and the 2026 preprint does just that: its core is an algorithm for triangles in sparse lopsided graphs.

### Pitfalls

- To claim an equivalence, give both reductions, each with its $a(n)$, $b(n)$ and whether it is randomized.
- Say which form of the problem is in the class. Integer and real 3SUM were not known to be equivalent until a 2026 preprint by Fischer, Polak and Schmidt (arXiv:2610.10153) reduced real 3SUM to integer 3SUM.
- A class falls as one. Once one member is truly faster, the hypothesis for the class is false, and every conditional bound based on it has no base.

## Examples

**One set and three sets.** One-set 3SUM and three-set 3SUM are equivalent, with $a(n) = b(n) = n^2$ and deterministic reductions both ways. From three sets to one set, map $a \mapsto 8a + 1$, $b \mapsto 8b + 2$ and $c \mapsto 8c - 3$; the residues 1, 2 and 5 modulo 8 force one element from each set. For $A = \{3, -1, 4\}$, $B = \{1, -5, 9\}$ and $C = \{-2, 6, -7\}$, the image is $\{25, -7, 33, 10, -38, 74, -19, 45, -59\}$, and its only zero-sum triple $-7 + (-38) + 45$ is the image of $-1 + (-5) + 6$. From one set to three sets, $2 \lceil \log_2 n \rceil^2$ colorings of the indices make sure that every triple gets three colors in one of them. For $n = 16$ there are 32 colorings, and each of the 560 triples of indices gets three colors in at least one. So an $O(n^{2-\varepsilon})$ algorithm for one form gives an $O(n^{2-\varepsilon} \log^2 n)$ algorithm for the other. See [3SUM](/3sum/).

**Convolution 3SUM.** The map $x_i = a_i \cdot 2n + i$ turns Convolution 3SUM into 3SUM in linear time. For $a = (2, 7, 1, 8, 3, 9)$ it gives $x = (24, 85, 14, 99, 40, 113)$, and the solutions $85 + 14 = 99$ and $14 + 99 = 113$ are the solutions $a_1 + a_2 = a_3$ and $a_2 + a_3 = a_5$ of the array. The reduction back, from 3SUM, is harder and needs hashing or the method of Chan and He. See [Convolution 3SUM](/convolution-3sum/).

**A non-example.** 3SUM reduces to deciding whether $n$ points in the plane contain three on a line, by $a \mapsto (a, a^3)$. No reduction back is known. So three [collinear points](/collinear-points/) is 3SUM-hard but not known to be in the 3SUM class, and the 2026 algorithms for 3SUM give nothing for it.

## Where it is used

- **Organizing hypotheses.** The survey of Vassilevska Williams (ICM 2018) arranges the field around a few classes and the reductions between them. Each class needs only one hypothesis.
- **Choosing a source problem.** To prove a bound under the APSP hypothesis, it is often easier to reduce from negative triangle than from APSP itself. The equivalence makes the two choices give the same result. See [APSP and negative triangle equivalence](/apsp-negative-triangle-equivalence/).
- **Algorithms.** A new algorithm for one member is an algorithm for all. The 2026 preprints on 3SUM and APSP moved three classes at once.
- **Dynamic problems.** The OMv class gives a single hypothesis for many dynamic problems; see [online matrix-vector multiplication](/online-matrix-vector-multiplication/) and [dynamic lower bounds](/dynamic-lower-bounds/).

## References
