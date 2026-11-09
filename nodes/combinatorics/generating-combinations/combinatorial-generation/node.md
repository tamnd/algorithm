---
tag: M971AZ
kind: concept
slug: combinatorial-generation
name: Combinatorial generation
aliases:
- Generating combinatorial objects
- Listing combinatorial objects
- generation of combinatorial objects
- listing combinatorial objects
- exhaustive generation
area: combinatorics/generating-combinations
level: intro
summary: The task of listing every object of a combinatorial class exactly once, usually in a defined order.
prereqs: [asymptotic-notation, binomial-coefficient]
see_also: [power-set-enumeration, k-subset-enumeration, generating-all-permutations, constant-amortized-time-generation, loopless-generation, combinatorial-ranking-and-unranking, gray-code, brute-force-search]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1, Generating basic combinatorial patterns (7.2.1.1 n-tuples, 7.2.1.2 permutations, 7.2.1.3 combinations)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Generating elementary combinatorial objects (successor, rank and unrank for subsets, k-subsets and permutations)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapters 1 to 7 (next subset, next k-subset, next composition, next partition, next permutation)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 1997, 605-629
    locator: Sections 1 and 2 (minimal change listings and the cost measures of generation)
---

Combinatorial generation is the task of listing each object of a finite combinatorial class exactly once, usually in a fixed order. The classes are, for example, the [subsets](/power-set-enumeration/) of a set, the [k-subsets](/k-subset-enumeration/), the [permutations](/generating-all-permutations/), the partitions and the trees of a given size. A list of $N$ objects needs $\Omega(N)$ time, so the best methods spend $O(1)$ time for each object, either on average ([CAT](/constant-amortized-time-generation/)) or in the worst case ([loopless](/loopless-generation/)).

## In plain words

Sometimes a program must look at every possible choice: every group of players for a team, every order of cities for a tour, every way to split a bill. A generation algorithm makes these choices one after the other. It must not skip one and it must not give one twice.

Most generators keep one current object in memory. They change it a little to get the next object, and they stop after the last one. Good generators make the change cheap, so that the work for each object does not grow with the size of the object.

The number of objects grows very fast with the size. A list of all of them is useful only for small sizes, or when the program can stop early.

## The idea

**Classes and listings.** A combinatorial class is a family of finite sets $\mathcal{A}_n$, one for each size $n \ge 0$. Let $N = |\mathcal{A}_n|$. A *listing* of $\mathcal{A}_n$ is a sequence $x_0, x_1, \ldots, x_{N-1}$ that contains each element of $\mathcal{A}_n$ exactly once. A generation algorithm takes $n$ and produces a listing: it calls a procedure *visit* on $x_0$, then on $x_1$, and so on, and then stops.

| class | $N$ | page |
| --- | --- | --- |
| subsets of $[n] = \{1, \ldots, n\}$ | $2^n$ | [power set enumeration](/power-set-enumeration/) |
| $k$-subsets of $[n]$ | $C(n, k)$ | [k-subset enumeration](/k-subset-enumeration/) |
| multisets of size $k$ from $[n]$ | $C(n+k-1, k)$ | [combinations with repetition](/combinations-with-repetition/) |
| $n$-bit strings with $k$ ones | $C(n, k)$ | [fixed-weight binary strings](/fixed-weight-binary-strings/) |
| permutations of $[n]$ | $n!$ | [generating all permutations](/generating-all-permutations/) |

**The output model.** The usual model, used by Knuth in Section 7.2.1, keeps the current object in an array that the generator changes in place. The visit procedure reads the array, and its cost is not counted. If the visit copies the object, each object costs $\Theta(n)$ more time. A bound such as "constant amortized time" counts only the changes that the generator makes, not the copies.

**Orders.** A listing has an order, and the order decides how cheap the next step is.

- *Lexicographic order* compares two objects at their first difference, as words in a dictionary. See [lexicographic order](/lexicographic-order/) and [lexicographic combinations](/lexicographic-combinations/).
- *Colexicographic order* compares two objects at their last difference. See [colexicographic order](/colexicographic-order/).
- A *Gray code* is a listing where two neighbors differ by a small change of a fixed kind: one bit flip, one swap of two elements, one move of one element. See [Gray code](/gray-code/) and [minimal change ordering](/minimal-change-ordering/).
- A listing is in *genlex* order when all objects with a common prefix are consecutive. Lexicographic order is genlex, and so are many Gray codes. The name is due to T. Walsh, as Knuth reports in Section 7.2.1.3.

**Cost measures.** Let $T(n)$ be the total time to list $\mathcal{A}_n$, and let the *delay* be the largest time between two consecutive visits, or before the first visit, or after the last one.

- The amortized time for each object is $T(n)/N$.
- The generator has *polynomial delay* when the delay is bounded by a polynomial in $n$.
- The generator is *CAT* (constant amortized time) when $T(n) = O(N)$. See [constant amortized time generation](/constant-amortized-time-generation/).
- The generator is *loopless* when the delay is $O(1)$ after an initialization of polynomial time. See [loopless generation](/loopless-generation/).

**A lower bound.** Each object needs at least one visit, so $T(n) = \Omega(N)$. If the objects are written out in full, each of size $n$, the output alone has size $nN$. A loopless generator in the in-place model needs a listing where neighbors differ in $O(1)$ entries of the array, because each changed entry costs one write.

**Three methods.**

1. *A successor function.* Compute $x_{i+1}$ from $x_i$ alone. The lexicographic successor of a $k$-subset is an example.
2. *Recursion on a decomposition.* Build $\mathcal{A}_n$ from smaller classes, for example "the subsets that do not contain $n$, then the subsets that contain $n$". The recursion tree has the objects at its leaves. See [power set by recursion](/power-set-by-recursion/) and [recursive combination generation](/recursive-combination-generation/).
3. *Ranking and unranking.* Use a bijection $\mathrm{rank}: \mathcal{A}_n \to \{0, \ldots, N-1\}$ and its inverse. Then $x_i = \mathrm{unrank}(i)$. This is slower than a successor function, but it gives random access, uniform random objects and an easy split of the work between processors. See [ranking and unranking combinations](/combinatorial-ranking-and-unranking/).

## Examples

**Subsets of $\{1, 2, 3\}$ in three orders.** Each column lists the $8$ subsets.

| step | binary counting | Gray code | lexicographic |
| --- | --- | --- | --- |
| 0 | $\emptyset$ | $\emptyset$ | $\emptyset$ |
| 1 | $\{1\}$ | $\{1\}$ | $\{1\}$ |
| 2 | $\{2\}$ | $\{1, 2\}$ | $\{1, 2\}$ |
| 3 | $\{1, 2\}$ | $\{2\}$ | $\{1, 2, 3\}$ |
| 4 | $\{3\}$ | $\{2, 3\}$ | $\{1, 3\}$ |
| 5 | $\{1, 3\}$ | $\{1, 2, 3\}$ | $\{2\}$ |
| 6 | $\{2, 3\}$ | $\{1, 3\}$ | $\{2, 3\}$ |
| 7 | $\{1, 2, 3\}$ | $\{3\}$ | $\{3\}$ |

The binary counting column reads the integer $i$ in binary, with bit $j$ for the element $j + 1$. The Gray code column is the [binary reflected Gray code](/binary-reflected-gray-code/): each step adds or removes exactly one element. The lexicographic column compares the subsets as increasing sequences.

**2-subsets of $\{1, 2, 3, 4\}$ in three orders.**

- Lexicographic: $12, 13, 14, 23, 24, 34$.
- Colexicographic: $12, 13, 23, 14, 24, 34$.
- Revolving door: $12, 23, 13, 34, 24, 14$. Each step removes one element and adds one element.

**The cost of the change.** For $n = 10$, the binary counter changes $2036$ bits in total to go from $0$ to $1023$, and the Gray code changes $1023$ bits, one at each step. Both are CAT, but only the Gray code has a constant number of changes at each step.

**How fast the counts grow.** For $n = 10$: there are $1024$ subsets, $C(10, 5) = 252$ subsets of size $5$, $115975$ set partitions (the [Bell number](/bell-numbers/)), $16796$ binary trees with $10$ nodes (the [Catalan number](/catalan-numbers/)) and $10! = 3628800$ permutations. For $n = 20$ there are already $1048576$ subsets. This growth is the [combinatorial explosion](/combinatorial-explosion/).

## Where it is used

- **Exhaustive search.** [Brute-force search](/brute-force-search/) and [generate and test](/generate-and-test/) list the candidates and check each one. [Backtracking](/generic-backtracking-algorithm/) is generation with early cuts of the [search space](/search-space/).
- **Gray codes in hardware and in search.** A [Gray code](/gray-code/) changes one bit at a time, so an incremental test (for example the sum of a subset) costs $O(1)$ for each step. See [subset sum](/subset-sum-problem/).
- **Indexing and random objects.** [Ranking and unranking](/combinatorial-ranking-and-unranking/) store a $k$-subset as one integer and draw a [uniform random subset](/uniform-random-subset/). The [combinatorial number system](/combinatorial-number-system/) is the standard bijection.
- **Enumeration with output-sensitive bounds.** In graph problems the number of objects is not known in advance, and the cost is measured by the delay. See [output-sensitive enumeration](/output-sensitive-enumeration/) and the [enumeration problem](/enumeration-problem/).
- **Exact counting by listing.** For small sizes, a generator checks a counting formula, for example the values of the [binomial coefficient](/binomial-coefficient/).

## References
