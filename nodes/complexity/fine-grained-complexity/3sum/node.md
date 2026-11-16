---
tag: BM50B0
kind: problem
slug: 3sum
name: 3SUM
aliases:
- 3-SUM
- three sum problem
- three-sum
area: complexity/fine-grained-complexity
level: intro
summary: "Given n integers, decide whether three of them sum to zero. Sorting gives O(n^2) time; a 2026 preprint gives O(n^1.9992) on the word RAM."
prereqs: [word-ram, time-complexity]
see_also: [3sum-conjecture, 3sum-hardness, three-sum-two-pointer-scan, k-sum, convolution-3sum, collinear-points, real-ram, fine-grained-reduction]
sources:
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry: Theory and Applications 5(3), 1995, 165-185"
    locator: the definition of the problem, the quadratic algorithm and the reductions to geometric problems
  - paper: doi:10.1007/s00453-007-9036-3
    title: "Ilya Baran, Erik D. Demaine and Mihai Pătraşcu, Subquadratic algorithms for 3SUM, Algorithmica 50(4), 2008, 584-596 (conference version in WADS 2005, 409-421)"
    locator: the main theorem for integers on the word RAM, a Las Vegas algorithm with an n^2/max(w/lg^2 w, lg^2 n/(lg lg n)^2) bound
  - paper: doi:10.1145/3185378
    title: "Allan Grønlund and Seth Pettie, Threesomes, degenerates, and love triangles, Journal of the ACM 65(4), 2018, article 22 (conference version in FOCS 2014, 621-630)"
    locator: the abstract and the introduction (decision tree depth O(n^(3/2) sqrt(log n)) and the real RAM algorithms); the page relies on the journal version
  - paper: doi:10.1145/3363541
    title: "Timothy M. Chan, More logarithmic-factor speedups for 3SUM, (median,+)-convolution, and some geometric 3SUM-hard problems, ACM Transactions on Algorithms 16(1), 2020, article 7 (conference version in SODA 2018)"
    locator: the abstract (a deterministic real RAM algorithm in time (n^2/log^2 n)(log log n)^O(1))
  - paper: doi:10.1145/3285953
    title: "Daniel M. Kane, Shachar Lovett and Shay Moran, Near-optimal linear decision trees for k-SUM and related problems, Journal of the ACM 66(3), 2019, article 16 (conference version in STOC 2018)"
    locator: the abstract (linear decision trees with O(n log^2 n) queries, each query 2k-sparse with coefficients in {-1, 0, 1})
  - paper: "Jeff Erickson, Lower bounds for linear satisfiability problems, Chicago Journal of Theoretical Computer Science 1999, article 8 (conference version in SODA 1995, 388-395)"
    locator: the main lower bound, Omega(n^ceil(r/2)) in the r-linear decision tree model, which is Omega(n^2) for 3SUM
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract and the introduction (deterministic integer 3SUM in O(n^1.9992), Las Vegas real 3SUM in O(n^1.998)); not yet refereed
  - paper: arxiv:2610.42012
    title: "Timothy M. Chan, Reina Itakura, Zhiyuan Ma and Yuancheng Yu, 3SUM made simpler (without matrix multiplication), k-SUM hypothesis refuted for odd k, and real 3SUM/APSP derandomized, arXiv preprint, October 2026"
    locator: the abstract and the introduction (randomized integer 3SUM in O(n^1.965) without fast matrix multiplication, deterministic real 3SUM); not yet refereed
  - paper: arxiv:2610.10153
    title: "Nick Fischer, Adam Polak and Jonas Schmidt, 3SUM is really hard: a real-to-integer reduction, arXiv preprint, October 2026, to appear in FOCS 2026"
    locator: the abstract (a truly subquadratic algorithm for integer 3SUM gives one for real 3SUM)
---

3SUM asks whether a set of $n$ numbers contains three elements that sum to zero. Sorting and a two-pointer scan solve it in $O(n^2)$ time. For about thirty years after Gajentaan and Overmars named the problem in 1995, the best algorithms gained only logarithmic factors over this, and the [3SUM conjecture](/3sum-conjecture/) said that no algorithm runs in time $O(n^{2-\varepsilon})$. Many problems in computational geometry and in dynamic data structures were proved [3SUM-hard](/3sum-hardness/), which means that a fast algorithm for them would give a fast algorithm for 3SUM. In October 2026, Alman and Vassilevska Williams posted a preprint with a deterministic $O(n^{1.9992})$ algorithm for integers on the word RAM, and a randomized $O(n^{1.998})$ algorithm for reals. The preprints are not yet refereed.

This page is about the problem: its forms, its models, its algorithms and its reductions. The hypothesis about its running time, with its status, is on [3SUM conjecture](/3sum-conjecture/). The class of problems that 3SUM reduces to is on [3SUM-hardness](/3sum-hardness/). The quadratic algorithm, with pseudocode and a proof, is on [3SUM by sorting and two-pointer scan](/three-sum-two-pointer-scan/). The generalization to $k$ terms is [k-SUM](/k-sum/), and the form on an array with index sums is [Convolution 3SUM](/convolution-3sum/).

## In plain words

You have a bag of numbers, some positive and some negative. Can you pick three different numbers from the bag that cancel out to exactly zero?

The easy way is to try every group of three, but that is slow for a big bag. A better way puts the numbers in order. Then, for each number, it walks in from both ends of the ordered list to look for two partners. This takes work proportional to the square of the bag size.

For a long time, experts could only make this a little faster, and many believed that nothing much faster was possible. Many other problems, for example whether three points lie on one line, were shown to be at least as hard. In 2026 a new method beat the square by a tiny amount. It is a theoretical result and is not faster in practice.

## Definition

**3SUM**

- Instance: a set $S$ of $n$ integers, each in binary.
- Question: are there three distinct elements $a, b, c \in S$ with $a + b + c = 0$?

**The model.** The integer form is measured on the [word RAM](/word-ram/) with words of $w = \Theta(\log n)$ bits. The usual range is $|x| \le n^{c}$ for a constant $c$, so that each number fits in $O(1)$ words and an addition costs $O(1)$. The real form takes $n$ real numbers and is measured on the [real RAM](/real-ram/), with exact addition, subtraction and comparison at unit cost, or in the [linear decision tree](/linear-decision-tree/) model, which counts only the sign tests on linear combinations of the inputs. The two forms are different problems: an algorithm for one does not directly give an algorithm for the other (see Reductions).

**Equivalent forms.** The forms below are equivalent. Each reduction is deterministic, and makes at most $O(\log^2 n)$ calls on instances with at most $3n$ numbers:

- *Three sets.* Given sets $A$, $B$ and $C$ of $n$ integers each, are there $a \in A$, $b \in B$ and $c \in C$ with $a + b + c = 0$?
- *Sum form.* Are there $a \in A$, $b \in B$ and $c \in C$ with $a + b = c$? Negate every element of $C$ to get the three-set form.
- *Target.* Are there three elements with sum $t$? Replace each $x$ by $3x - t$.

From three sets to one set, map $a \mapsto 8a + 1$, $b \mapsto 8b + 2$ and $c \mapsto 8c - 3$. The residues modulo 8 are 1, 2 and 5. The only way to pick three of these residues, with repetition, that sum to 0 modulo 8 is $1 + 2 + 5$. So any zero-sum triple of the image takes one element from each set, and $(8a + 1) + (8b + 2) + (8c - 3) = 8(a + b + c)$.

From one set to three sets, number the elements $0, \ldots, n - 1$ and let $L = \lceil \log_2 n \rceil$. For each pair of bit positions $p, q < L$ and each bit $v$, color index $i$ with color 3 if bit $p$ of $i$ is $v$, and otherwise with color 1 or 2 by bit $q$ of $i$. Put the elements of color 1, 2 and 3 into $A$, $B$ and $C$. Three distinct indices differ in some bit $p$, where one index is alone; take $v$ to be its bit, and take $q$ to be a bit where the other two differ. That coloring gives the three indices three different colors. So $S$ is a yes-instance if and only if one of the $2L^2$ three-set instances is. For $n = 16$ there are 32 colorings, and every one of the 560 triples of indices gets three colors in at least one of them.

## Variants

- **Real 3SUM.** The input is $n$ real numbers, in the real RAM or the linear decision tree model. It was a separate problem until 2026, when Fischer, Polak and Schmidt gave a reduction from real 3SUM to integer 3SUM that keeps truly subquadratic time (arXiv:2610.10153, to appear in FOCS 2026).
- **Small range.** If all numbers are in $[-U, U]$, the fast Fourier transform computes the sumset $A + B$ in $O(n + U \log U)$ time, deterministic. This is fast only when $U$ is about $n$ or a little more.
- **Counting and listing.** Count or list all zero-sum triples. A set of $n$ integers can have $\Theta(n^2)$ such triples (take $\{-n, \ldots, n\}$), so listing needs $\Omega(n^2)$ time in the worst case.
- **3SUM-Indexing.** Preprocess $A$ and $B$, then answer queries "is $c \in A + B$?". This is a data structure problem with a space and query time trade-off.
- **[Convolution 3SUM](/convolution-3sum/).** An array $a_0, \ldots, a_{n-1}$; are there $i$ and $j$ with $a_i + a_j = a_{i+j}$?
- **[k-SUM](/k-sum/).** $k$ terms instead of 3.

## Examples

**A yes-instance with a trace.** Let $S = \{-25, -10, -7, -3, 2, 4, 8, 10\}$, already sorted. Fix the smallest element and scan the rest from both ends. With $-25$ fixed, the pairs $(-10, 10), (-7, 10), (-3, 10), (2, 10), (4, 10), (8, 10)$ give sums $-25, -22, -18, -13, -11, -7$; all are negative, so the left pointer moves each time and the scan ends without a hit. With $-10$ fixed, the sums are $-7$ for $(-7, 10)$, $-3$ for $(-3, 10)$, $2$ for $(2, 10)$, and then $0$ for $(2, 8)$. The triple $-10 + 2 + 8 = 0$ is found after 10 sum tests. If the scan continues to list all triples, it also finds $-7 + (-3) + 10 = 0$, and it ends after 19 sum tests. A test of all $\binom{8}{3} = 56$ triples finds the same two.

**A no-instance.** $S = \{-9, -4, 1, 6, 11, 15\}$. No triple sums to zero. The two negative elements sum to $-13$, and no element is 13. A triple with one negative element needs two positive elements that sum to 9 or 4; none do.

**Three sets to one set.** Let $A = \{3, -1, 4\}$, $B = \{1, -5, 9\}$ and $C = \{-2, 6, -7\}$. The only solution is $-1 + (-5) + 6 = 0$. The map gives the set $\{25, -7, 33, 10, -38, 74, -19, 45, -59\}$, and its only zero-sum triple is $-7 + (-38) + 45 = 0$, which is the image of $(-1, -5, 6)$.

## Known algorithms

- Sorting and a two-pointer scan, or a hash table of the elements, decide 3SUM in $O(n^2)$ time, deterministic for the scan and expected for hashing; this works on the word RAM and the real RAM. See [three-sum-two-pointer-scan](/three-sum-two-pointer-scan/).
- Baran, Demaine and Pătraşcu (WADS 2005, Algorithmica 2008) decide integer 3SUM on the word RAM in expected time $O(n^2 / \max\{w / \lg^2 w, \lg^2 n / (\lg \lg n)^2\})$, Las Vegas, by hashing and word packing; with $w = \Theta(\log n)$ this is $O(n^2 (\log \log n)^2 / \log^2 n)$.
- Grønlund and Pettie (FOCS 2014, JACM 2018) decide real 3SUM on the real RAM in deterministic time $O(n^2 / (\log n / \log \log n)^{2/3})$ and randomized time $O(n^2 (\log \log n)^2 / \log n)$.
- Chan (SODA 2018, TALG 2020) decides real 3SUM on the real RAM in deterministic time $(n^2 / \log^2 n)(\log \log n)^{O(1)}$.
- Alman and Vassilevska Williams (arXiv, October 2026) decide integer 3SUM with numbers bounded by a polynomial in $n$ on the word RAM in deterministic time $O(n^{1.9992})$, and real 3SUM in expected time $O(n^{1.998})$, Las Vegas, with only comparisons, additions and subtractions on the reals. The core is a fast product of thin matrices that is only asked for a chosen set of entries, a variant of Coppersmith's rectangular matrix multiplication.
- Chan, Itakura, Ma and Yu (arXiv, October 2026) decide integer 3SUM in time $O(n^{1.965})$, randomized (Monte Carlo), without fast matrix multiplication, and give a deterministic truly subquadratic algorithm for real 3SUM.

All the 2026 results are in preprints that are not yet refereed. The exponents are far from 2 only on paper: $n^{0.0008}$ is about $1.011$ for $n = 10^6$ and reaches 2 only at $n = 2^{1250}$.

## Bounds

- **Unconditional, word RAM.** $\Omega(n)$, to read the input. No better lower bound is known.
- **Unconditional, restricted linear decision trees.** Erickson (1995, 1999) proved $\Omega(n^2)$ depth for linear decision trees in which each query is the sign of an affine combination of at most 3 inputs.
- **Unconditional upper bounds on decision trees.** Grønlund and Pettie gave linear decision trees of depth $O(n^{3/2} \sqrt{\log n})$. Kane, Lovett and Moran gave linear decision trees with $O(n \log^2 n)$ queries, each with at most 6 nonzero coefficients in $\{-1, 0, 1\}$. So no quadratic lower bound can be proved in the general linear decision tree model, and Erickson's bound depends on the restriction to 3 inputs per query.
- **Conditional.** The [3SUM conjecture](/3sum-conjecture/) said that there is no $O(n^{2-\varepsilon})$ algorithm. The 2026 preprints above refute it for integers and for reals. 3SUM is not known to be hard under SETH, so SETH gives no bound to replace it.

## Reductions

- **From 3SUM to three collinear points** (Gajentaan and Overmars 1995). Deterministic, linear time: $a \mapsto (a, a^3)$. Distinct $a, b, c$ give collinear points exactly when $a + b + c = 0$. See [collinear points](/collinear-points/) for the proof and a worked example, and [3SUM-hardness](/3sum-hardness/) for the other geometric problems.
- **Between 3SUM and Convolution 3SUM.** From Convolution 3SUM to 3SUM: deterministic, linear time. From 3SUM to Convolution 3SUM: Pătraşcu (STOC 2010), randomized; Chan and He (SOSA 2020), deterministic. So the two problems are subquadratically equivalent. See [Convolution 3SUM](/convolution-3sum/).
- **From 3SUM to dynamic problems.** Pătraşcu (2010) reduced 3SUM, through Convolution 3SUM, to the multiphase problem and from there to many dynamic problems. Abboud and Vassilevska Williams (2014) and Kopelowitz, Pettie and Porat (2016) gave more. See [dynamic lower bounds](/dynamic-lower-bounds/).
- **From min-plus convolution to 3SUM.** A truly subquadratic algorithm for 3SUM gives one for the decision form of [min-plus convolution](/min-plus-convolution/) (Cygan, Mucha, Węgrzycki and Włodarczyk 2019, Figure 1 and Appendix A of the arXiv version).
- **Real and integer.** Fischer, Polak and Schmidt (2026) reduce real 3SUM to integer 3SUM in a way that keeps truly subquadratic time.
- **Not known.** No fine-grained reduction is known from CNF-SAT or [Orthogonal Vectors](/orthogonal-vectors/) to 3SUM, from 3SUM to them, or between 3SUM and all-pairs shortest paths. 3SUM is the case $k = 3$ of [k-SUM](/k-sum/).

## Applications

- **Hardness in geometry.** 3SUM was the first base problem of fine-grained complexity. Gajentaan and Overmars used it to explain why problems such as three collinear points, separating segments by a line and covering a triangle with triangles had no known subquadratic algorithms. See [3SUM-hardness](/3sum-hardness/).
- **Dynamic problems.** Through Convolution 3SUM, 3SUM gave polynomial lower bounds for dynamic data structures under the old conjecture. See [dynamic lower bounds](/dynamic-lower-bounds/).
- **Teaching.** The sort and two-pointer scan is a standard exercise for the two-pointer technique, and the problem is a short example of a problem in P whose exact exponent was open for a long time.

## References
