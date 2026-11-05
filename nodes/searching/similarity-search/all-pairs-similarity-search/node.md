---
tag: 7R0KDV
kind: problem
slug: all-pairs-similarity-search
name: All-pairs similarity search
aliases:
- similarity self-join
- all-pairs similarity
area: searching/similarity-search
level: advanced
summary: Find all pairs of objects in a collection whose similarity exceeds a threshold.
prereqs: [cosine-similarity, jaccard-similarity]
see_also: [allpairs, set-similarity-join, prefix-filtering, ppjoin, minhash, fixed-radius-near-neighbors, inverted-index, orthogonal-vectors]
sources:
  - paper: doi:10.1145/1242572.1242591
    title: Roberto J. Bayardo, Yiming Ma and Ramakrishnan Srikant, Scaling up all pairs similarity search, Proceedings of the 16th International World Wide Web Conference (WWW), 2007
    locator: pages 131 to 140 (the problem for cosine similarity on sparse unit vectors with a threshold t, its applications, and the All-Pairs algorithm)
  - paper: doi:10.1109/ICDE.2006.9
    title: Surajit Chaudhuri, Venkatesh Ganti and Raghav Kaushik, A primitive operator for similarity joins in data cleaning, Proceedings of the 22nd International Conference on Data Engineering (ICDE), 2006
    locator: the set-similarity join and the prefix filter
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005
    locator: pages 357 to 365 (a fast algorithm for orthogonal vectors would give a faster algorithm for CNF-SAT)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Sections 3.3 and 3.4 (finding similar pairs of documents with MinHash and banding) and Section 3.9 (methods for high degrees of similarity, with prefix and length filters)
---

All-pairs similarity search asks, for a collection of $n$ objects, a similarity function $s$ and a threshold $t$, for every pair of objects $\{x, y\}$ with $s(x, y) \ge t$. The usual similarities are [cosine similarity](/cosine-similarity/) on sparse vectors and [Jaccard similarity](/jaccard-similarity/) on sets. A scan of all $\binom{n}{2}$ pairs is the baseline; exact methods such as [All-Pairs](/allpairs/) and [prefix filtering](/prefix-filtering/) use an [inverted index](/inverted-index/) to skip pairs that cannot pass $t$, and [MinHash](/minhash/) banding finds most pairs with a probability. The problem is the threshold version of [fixed-radius near neighbors](/fixed-radius-near-neighbors/), and its join form between two collections is as hard as [orthogonal vectors](/orthogonal-vectors/).

## In plain words

You have many items, such as web pages, user profiles or product names, and a way to score how alike two items are. You want every pair of items whose score is at least some limit.

Testing every pair is slow when there are millions of items, since the number of pairs grows with the square. Most pairs share nothing, so the trick is to test only pairs that share at least one word or feature, and to cut even those pairs down with simple bounds on how high the score can get.

## Definition

Let $V = \{x_1, \dots, x_n\}$ be a collection of objects, $s : V \times V \to [0, 1]$ a symmetric similarity, and $t \in (0, 1]$ a threshold.

- **Self-join.** Report $\{\{x_i, x_j\} : i < j, \; s(x_i, x_j) \ge t\}$. Let $K$ be the number of reported pairs.
- **Cosine form (Bayardo, Ma and Srikant).** The objects are vectors in $\mathbb{R}_{\ge 0}^d$, usually sparse, normalized to unit length, and $s(x, y) = x \cdot y$.
- **Set form.** The objects are finite sets, and $s$ is the Jaccard similarity $|x \cap y| / |x \cup y|$, or the cosine $|x \cap y| / \sqrt{|x| |y|}$, or the Dice coefficient.

The cost is measured by the time and by the number of similarity evaluations, given an input of total size $N = \sum_i |x_i|$, where $|x_i|$ is the number of nonzero entries.

## Variants

- **R-S join.** Two collections $R$ and $S$; report all pairs $(x, y) \in R \times S$ with $s(x, y) \ge t$. This is the [set similarity join](/set-similarity-join/) of databases.
- **Top-k pairs.** Report the $k$ pairs of largest similarity, with no fixed threshold.
- **Approximate.** Report each pair with $s \ge t$ with probability at least $1 - f$, and possibly some pairs below $t$; [MinHash](/minhash/) and [random hyperplane](/random-hyperplane-lsh/) banding solve this.
- **Distance form.** For a metric $\delta$ and radius $r$, report the pairs with $\delta \le r$: the all-pairs form of [fixed-radius near neighbors](/fixed-radius-near-neighbors/).
- **Edit distance.** Pairs of strings within edit distance $k$, solved with $q$-gram filters.

## Examples

- **Sets.** Let $A = \{a, b, c, d\}$, $B = \{a, b, c\}$, $C = \{c, d, e\}$ and $D = \{a, b, e\}$, with Jaccard similarity and $t = 0.5$. The six similarities are $J(A,B) = 3/4$, $J(A,C) = 2/5$, $J(A,D) = 2/5$, $J(B,C) = 1/5$, $J(B,D) = 2/4$ and $J(C,D) = 1/5$. The answer is $\{A, B\}$ and $\{B, D\}$, so $K = 2$.
- **Cosine.** The unit vectors $x = (0.6, 0.8, 0)$, $y = (0.8, 0.6, 0)$ and $z = (0, 0, 1)$ with $t = 0.9$ give $x \cdot y = 0.96$, $x \cdot z = 0$ and $y \cdot z = 0$. The answer is $\{x, y\}$. The pair $(x, z)$ shares no nonzero dimension, so an inverted index never forms it.

## Known algorithms

- **Scan.** All $\binom{n}{2}$ pairs, with a sparse dot product each: $O(n^2)$ evaluations, $O(nN)$ time.
- **Inverted index join.** For each dimension, list the vectors that are nonzero in it. Score each $x$ against the vectors that share a dimension, using an accumulator. The time is $\sum_j |I_j|^2$ over the lists $I_j$, which is quadratic for frequent dimensions.
- **Prefix filtering.** For set similarity with threshold $t$, order the elements by a global order, usually by increasing frequency. Two sets with $s \ge t$ must share an element among the first few elements of each set, the prefix. Index only prefixes. See [prefix filtering](/prefix-filtering/), introduced for joins by Chaudhuri, Ganti and Kaushik.
- **All-Pairs.** Bayardo, Ma and Srikant extend prefix filtering to weighted cosine: index only the part of each vector beyond the point where the remaining weights could reach $t$. See [All-Pairs](/allpairs/).
- **PPJoin.** [PPJoin](/ppjoin/) adds a position filter on the prefix to prune more candidate pairs.
- **LSH banding.** Hash each object with $b$ bands of $r$ [MinHash](/minhash/) values each, and test only the pairs that share a band bucket. A pair of Jaccard similarity $J$ becomes a candidate with probability $1 - (1 - J^r)^b$; see [LSH amplification](/lsh-amplification/).

## Bounds

- **Output.** Any algorithm needs $\Omega(N + K)$ time.
- **Worst case of the filters.** If all objects share one frequent dimension with high weight, every pair passes the filters and the exact methods take $\Theta(n^2)$ evaluations, even when $K$ is small. The filters help on real data, where dimension frequencies are skewed, but they give no worst-case gain.
- **Hardness of the R-S join.** For each $\varepsilon > 0$ there is a constant $c$ such that the R-S cosine join on $n$ vectors of $\{0, 1\}^{c \log n}$ cannot be decided (is $K > 0$?) in $O(n^{2 - \varepsilon})$ time unless the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) fails. *Proof.* Take an orthogonal vectors instance $A, B \subseteq \{0,1\}^d$. Replace each $b$ by its complement $\bar b$, and split $A$ by $|a| = w_1$ and $B$ by $|\bar b| = w_2$. Then $a \cdot \bar b = w_1 - a \cdot b$, so $a \cdot b = 0$ if and only if $a \cdot \bar b = w_1$, which needs $w_1 \le w_2$. In the group $(w_1, w_2)$ with $1 \le w_1 \le w_2$, the cosine is $a \cdot \bar b / \sqrt{w_1 w_2}$, so $a \cdot b = 0$ if and only if the cosine is at least $t = \sqrt{w_1/w_2}$. Vectors with $|a| = 0$ are orthogonal to everything and are checked directly, and $|\bar b| = 0$ means $b$ is all ones, which is orthogonal to $a$ only if $a = 0$. So $(d+1)^2$ joins decide orthogonal vectors, and a subquadratic join would give a subquadratic algorithm for orthogonal vectors with $d = c \log n$, which Williams showed refutes the SETH. $\square$

## Reductions

- **Cosine to Euclidean distance.** For unit vectors, $\|x - y\|^2 = 2 - 2\, x \cdot y$, so $x \cdot y \ge t$ if and only if $\|x - y\| \le \sqrt{2 - 2t}$. The problem is the all-pairs [fixed-radius near neighbors](/fixed-radius-near-neighbors/) problem with $r = \sqrt{2 - 2t}$.
- **Jaccard to overlap.** For sets of sizes $a \le b$, $J \ge t$ implies $|x \cap y| \ge t \cdot b$ and $a \ge t \cdot b$; such size and overlap bounds turn a Jaccard threshold into an overlap threshold, which is what prefix filtering uses.
- **Self-join and R-S join.** An R-S join is a self-join on $R \cup S$ with the pairs inside $R$ or inside $S$ discarded; a self-join is an R-S join of $V$ with itself.
- **From orthogonal vectors.** The reduction in the bounds above.

## Applications

- **Near-duplicate detection** of web pages, with shingled sets and Jaccard similarity.
- **Collaborative filtering.** Pairs of users or items with similar rating vectors.
- **Query suggestion and spam detection**, with the cosine similarity of query or ad vectors, as in the experiments of Bayardo, Ma and Srikant.
- **Entity resolution and data cleaning.** Pairs of records with similar names or addresses, as in the similarity join of Chaudhuri, Ganti and Kaushik.
- **Graph building.** The $\varepsilon$-neighborhood graph used in clustering and in semi-supervised learning.

## References
