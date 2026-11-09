---
tag: ST9MR9
kind: theorem
slug: pigeonhole-principle
name: Pigeonhole principle
aliases:
- Dirichlet's box principle
- drawer principle
- Schubfachprinzip
area: combinatorics/counting-algorithms
level: intro
summary: If more items than boxes are placed, some box holds at least two.
prereqs: [rule-of-sum]
see_also: [erdos-szekeres-theorem, counting-argument, hash-collision, birthday-paradox, floyd-cycle-detection, ramsey-theorem, double-counting]
sources:
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Chapter 3, The Pigeonhole Principle (Sections 3.1 and 3.2, the simple and the strong form)
  - book: isbn:9780073383095
    title: Kenneth H. Rosen, Discrete Mathematics and Its Applications, seventh edition
    locator: Section 6.2, The Pigeonhole Principle (the generalized form and the Erdős and Szekeres theorem)
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: Chapter Pigeon-hole and double counting
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter XI, Approximation of irrationals by rationals (Dirichlet's theorem and its proof by the box argument)
---

The pigeonhole principle says that a function from a finite set to a smaller finite set is not one to one: if more than $n$ items go into $n$ boxes, some box holds at least two items. Its strong form says that some box holds at least $\lceil m/n \rceil$ of $m$ items. It is an existence result: it proves that a collision exists without saying where. In computer science it is the reason why every [hash function](/hash-collision/) has collisions, why no lossless compressor shrinks every file, and why the iterates of a function on a finite set must cycle; it is also the base of the [counting argument](/counting-argument/) for lower bounds.

## Statement

Notation: $|S|$ is the size of a finite set $S$, and $f^{-1}(b) = \{a \in A : f(a) = b\}$ is the fiber of $b$.

**Theorem (pigeonhole principle).** Let $A$ and $B$ be finite sets and let $f : A \to B$ be a function.

1. **(Simple form.)** If $|A| > |B|$, then there are $a \ne a'$ in $A$ with $f(a) = f(a')$.
2. **(Strong form.)** Let $k \ge 0$ be an integer. If $|A| > k\,|B|$, then some $b \in B$ has $|f^{-1}(b)| \ge k + 1$. Equivalently, if $B \ne \emptyset$, some $b$ has $|f^{-1}(b)| \ge \lceil |A| / |B| \rceil$.
3. **(Averaging form.)** If $x_1, \ldots, x_n$ are real numbers with $n \ge 1$ and mean $\mu = (x_1 + \cdots + x_n)/n$, then some $x_i \ge \mu$ and some $x_j \le \mu$.

**Infinite form.** If $A$ is infinite, $B$ is finite and nonempty, then some fiber $f^{-1}(b)$ is infinite.

## In plain words

Ten pigeons fly into nine holes. However they choose, at least one hole gets two or more pigeons. You do not learn which hole, only that such a hole must exist.

The stronger version counts more carefully. If you deal 52 cards to 4 players, someone gets at least 13 cards, and if you put 53 letters into 4 piles, some pile has at least 14 letters. In general, divide the number of items by the number of boxes and round up: some box has at least that many. The reason is short. If every box had fewer, the boxes together would hold fewer items than you started with.

## Proof

The fibers $f^{-1}(b)$ for $b \in B$ are pairwise disjoint, because each $a \in A$ has exactly one image, and their union is $A$. By the [rule of sum](/rule-of-sum/),

$$|A| = \sum_{b \in B} |f^{-1}(b)|. \qquad (1)$$

*Strong form.* Assume, for a contradiction, that $|f^{-1}(b)| \le k$ for all $b \in B$. Then (1) gives $|A| \le k|B|$, which is false. So some fiber has at least $k + 1$ elements. For the second sentence, let $m = |A|$, $n = |B| \ge 1$ and $k = \lceil m/n \rceil - 1$. Then $k < m/n$, so $kn < m$, and the first sentence gives a fiber with at least $k + 1 = \lceil m/n \rceil$ elements. If $m = 0$, then $\lceil m/n \rceil = 0$ and the claim is trivial.

*Simple form.* Take $k = 1$ in the strong form. Some fiber has two elements $a \ne a'$, and $f(a) = f(a') = b$.

*Averaging form.* If every $x_i < \mu$, then $x_1 + \cdots + x_n < n\mu = x_1 + \cdots + x_n$, which is false. The same argument with the inequalities reversed gives some $x_j \le \mu$.

*Infinite form.* If every fiber were finite, $A$ would be a finite union of finite sets, so $A$ would be finite. $\square$

The proof is not constructive. To find a collision, an algorithm must still look for it, for example by sorting the images or by a hash table, in $O(|A| \log |A|)$ or expected $O(|A|)$ time.

## Consequences

**1. Monotone subsequences ([Erdős and Szekeres](/erdos-szekeres-theorem/)).** Each sequence of $n^2 + 1$ distinct real numbers has an increasing or a decreasing subsequence of length $n + 1$. *Proof.* Give each position $i$ the label $(u_i, d_i)$, the lengths of the longest increasing and the longest decreasing subsequence that end at $i$. For $i < j$, if $x_i < x_j$ then $u_j > u_i$, and if $x_i > x_j$ then $d_j > d_i$, so the labels are distinct. If all $u_i, d_i \le n$, only $n^2$ labels exist for $n^2 + 1$ positions, which is impossible. See also [longest increasing subsequence](/longest-increasing-subsequence/).

**2. A block sum divisible by the length.** Among any $n$ integers $x_1, \ldots, x_n$, some nonempty block $x_{i+1} + \cdots + x_j$ is divisible by $n$. *Proof.* The $n + 1$ [prefix sums](/prefix-sums/) $S_0 = 0, S_1, \ldots, S_n$ fall into $n$ residues modulo $n$, so $S_i \equiv S_j$ for some $i < j$. For $x = (4, 7, 1, 9, 5, 8)$ the prefix sums are $0, 4, 11, 12, 21, 26, 34$, with residues $0, 4, 5, 0, 3, 2, 4$ modulo 6, and the block $4 + 7 + 1 = 12$ is divisible by 6. One pass with an array of $n$ first positions finds such a block in $O(n)$ time. The same idea underlies [subarray sum equals k](/subarray-sum-equals-k/).

**3. Dirichlet's approximation theorem.** For each real $\alpha$ and integer $N \ge 1$, there are integers $p, q$ with $1 \le q \le N$ and $|q\alpha - p| < 1/N$. *Proof.* The $N + 1$ fractional parts of $0, \alpha, 2\alpha, \ldots, N\alpha$ lie in $[0, 1)$, which is the union of the $N$ intervals $[j/N, (j+1)/N)$. Two of them, for $q_1 < q_2$, lie in one interval, so $q = q_2 - q_1$ and the difference $p$ of their integer parts work. For $\alpha = \sqrt 2$ and $N = 10$: $|5\sqrt 2 - 7| \approx 0.0711$. See [continued fractions](/continued-fraction/) for the best such approximations.

**4. Hashing.** A hash function from a universe $U$ to $m$ slots with $|U| > km$ sends at least $k + 1$ keys to one slot. So for each fixed hash function, an adversary who knows it can make every key collide when $|U| \ge nm$, and a lookup then costs $\Theta(n)$. This is why hashing needs randomness or a known key distribution. See [hash collision](/hash-collision/) and the [birthday paradox](/birthday-paradox/), its random version.

**5. No compressor shrinks all inputs.** There are $2^n$ bit strings of length $n$ and only $2^n - 1$ strings of length less than $n$. So a one-to-one code maps some string of length $n$ to a string of length at least $n$. This is the base of the [incompressibility method](/incompressibility-method/).

**6. Cycles of a function.** For $f : B \to B$ with $|B| = n$ and any $x_0 \in B$, the $n + 1$ values $x_0, f(x_0), \ldots, f^n(x_0)$ contain a repeat, so the sequence $x_{t+1} = f(x_t)$ enters a cycle within $n$ steps. [Floyd's cycle detection](/floyd-cycle-detection/) and Pollard's rho method rely on this.

**7. Lower bounds.** A decision tree of height $h$ with two outcomes per node has at most $2^h$ leaves. If the problem has more than $2^h$ possible answers, two inputs with different answers reach the same leaf. This is the [counting argument](/counting-argument/) behind the $\lceil \lg n! \rceil$ bound for sorting by comparisons.

## Tightness

- **The simple form is sharp.** For $|A| = |B| = n$, the identity map is one to one, so $|A| > |B|$ cannot be weakened to $|A| \ge |B|$.
- **The strong form is sharp.** For $m$ items and $n$ boxes, put $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ items in each box, with $m \bmod n$ boxes of the larger size. The largest box has exactly $\lceil m/n \rceil$ items. With $m = kn$ every box has $k$ items, so $|A| > k|B|$ cannot be weakened to $|A| \ge k|B|$.
- **Erdős and Szekeres is sharp.** The sequence $3, 2, 1, 6, 5, 4, 9, 8, 7$ has $n^2 = 9$ terms for $n = 3$, and its longest increasing and longest decreasing subsequences both have length 3. The same block pattern works for every $n$.

## History

The principle is old and was used long before it had a name. It is often called Dirichlet's principle or the drawer principle (Schubfachprinzip in German, principe des tiroirs in French), because Dirichlet's approximation theorem is its classical application (Hardy and Wright, Chapter XI). The theorem of Erdős and Szekeres on monotone subsequences came from their work on convex polygons, and the labelling proof of consequence 1 is the one that Rosen (Section 6.2) gives. Ramsey theory, which starts with [Ramsey's theorem](/ramsey-theorem/), extends the principle from points to the edges of graphs: a large enough complete graph with two edge colors has a large clique of one color.

## References
