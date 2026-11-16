---
tag: 0KF8XW
kind: problem
slug: convolution-3sum
name: Convolution 3SUM
aliases:
- Convolution-3SUM
area: complexity/fine-grained-complexity
level: advanced
summary: "Given an array a, decide whether a[i] + a[j] = a[i+j] for some i and j. It is subquadratically equivalent to 3SUM and was the main route from 3SUM to dynamic lower bounds."
prereqs: [3sum, fine-grained-reduction, universal-hash-family]
see_also: [3sum, 3sum-conjecture, 3sum-hardness, min-plus-convolution, dynamic-lower-bounds, fine-grained-equivalence-class, convolution, triangle-listing-by-degree]
sources:
  - paper: doi:10.1145/1806689.1806772
    title: "Mihai Pătraşcu, Towards polynomial lower bounds for dynamic problems, STOC 2010, 603-610"
    locator: the definition of Convolution 3SUM, the randomized reduction from 3SUM by almost linear hashing, and its use for triangle listing and the multiphase problem
  - paper: doi:10.1137/1.9781611976014.1
    title: "Timothy M. Chan and Qizheng He, Reducing 3SUM to Convolution-3SUM, Symposium on Simplicity in Algorithms (SOSA 2020), 1-7"
    locator: the abstract and the main theorem (a deterministic reduction from 3SUM to Convolution 3SUM)
  - paper: doi:10.1145/3293465
    title: "Marek Cygan, Marcin Mucha, Karol Węgrzycki and Michał Włodarczyk, On problems equivalent to (min,+)-convolution, ACM Transactions on Algorithms 15(1), 2019, article 14 (conference version in ICALP 2017, LIPIcs 80, 22:1-22:15; arXiv:1702.07669)"
    locator: Section 2.1 (the three-array form 3SUMConv) and Appendix A, Theorem 25 (MaxConv UpperBound reduces to 3SUMConv); the locators are from the arXiv version
  - paper: doi:10.1137/1.9781611974331.ch89
    title: "Tsvi Kopelowitz, Seth Pettie and Ely Porat, Higher lower bounds from the 3SUM conjecture, SODA 2016, 1272-1287"
    locator: the lower bounds for set intersection, set disjointness and triangle listing that start from 3SUM
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract and the introduction (truly subquadratic 3SUM and Convolution 3SUM); not yet refereed
---

Convolution 3SUM asks whether an array $a_0, \ldots, a_{n-1}$ of integers has indices $i$ and $j$ with $a_i + a_j = a_{i+j}$. It is [3SUM](/3sum/) with a fixed link between the values and their positions: the index of the third term is the sum of the indices of the first two. Pătraşcu introduced it in 2010 and showed, with a randomized reduction, that it is as hard as 3SUM. The reduction in the other direction is simple and deterministic, so the two problems are subquadratically equivalent. Chan and He made the hard direction deterministic in 2020.

Convolution 3SUM was the main tool for turning the [3SUM conjecture](/3sum-conjecture/) into lower bounds for graphs and dynamic data structures, because the index structure is easy to embed into a matrix or a set system. In October 2026, Alman and Vassilevska Williams posted a truly subquadratic algorithm for 3SUM. Since Convolution 3SUM reduces to 3SUM in linear time, it is truly subquadratic too, if the preprint is correct.

## In plain words

You have a row of numbers in boxes, and each box has a position number. Look for two boxes whose numbers add up to the number in a third box, where the third box's position is the sum of the first two positions.

The easy way checks every pair of boxes, which takes work that grows with the square of the row length.

This puzzle is exactly as hard as the plain puzzle that asks whether three numbers from a bag add up to zero. Each one can be turned into the other. Its fixed positions make it easy to build into other problems, so it was used to show that those problems were hard. In 2026, both puzzles got a slightly faster method.

## Definition

**Convolution 3SUM**

- Instance: an array $a_0, \ldots, a_{n-1}$ of integers, each in binary.
- Question: are there indices $i, j \ge 0$ with $i + j \le n - 1$ and $a_i + a_j = a_{i+j}$?

**The model.** The [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits, and integers in $\{-n^{c}, \ldots, n^{c}\}$ for a constant $c$, as for 3SUM. Real forms exist but are rarely used.

**Three-array form.** Given arrays $a$, $b$ and $c$ of length $n$, are there $i$ and $j$ with $a_i + b_j = c_{i+j}$? Cygan, Mucha, Węgrzycki and Włodarczyk call this 3SUMConv. The one-array form is the case $a = b = c$. The name comes from the [convolution](/convolution/) pattern $i + j = k$ of the indices.

**Indices.** Some sources allow $i = j$ and some ask for $i \ne j$. The pairs with $i = j$ can be tested directly in $O(n)$ time. Say which form a result uses.

## Variants

- **Counting and listing.** Count or list all pairs $(i, j)$. There can be $\Theta(n^2)$ of them, for example when all entries are 0.
- **Target.** $a_i + a_j = a_{i+j} + t$ for a given $t$. Replace $a_i$ by $a_i - t$; then $(a_i - t) + (a_j - t) = (a_{i+j} - t)$ exactly when $a_i + a_j = a_{i+j} + t$.

## Examples

**A yes-instance.** Let $a = (2, 7, 1, 8, 3, 9)$, indexed from 0. The pairs $(i, j)$ with $a_i + a_j = a_{i+j}$ are $(1, 2)$ and $(2, 1)$, since $a_1 + a_2 = 7 + 1 = 8 = a_3$, and $(2, 3)$ and $(3, 2)$, since $a_2 + a_3 = 1 + 8 = 9 = a_5$. No other pair works: for example $a_0 + a_0 = 4 \ne a_0$, and $a_1 + a_1 = 14 \ne a_2$.

**The map to 3SUM.** Let $M = 2n = 12$ and $x_i = a_i M + i$. This gives

$$x = (24, 85, 14, 99, 40, 113).$$

The 3SUM instance asks for $x_i + x_j = x_k$. It has the solutions $85 + 14 = 99$ and $14 + 99 = 113$, which are $(i, j, k) = (1, 2, 3)$ and $(2, 3, 5)$, the solutions of the array, in both orders of $i$ and $j$. The map was also compared with a direct search on 3000 random arrays of length at most 7 and entries in $\{-6, \ldots, 6\}$, and it agreed on all of them.

## Known algorithms

- **Direct search.** Test all pairs $(i, j)$ with $i + j \le n - 1$. This takes $O(n^2)$ time, deterministic.
- **Through 3SUM.** The linear map below turns any 3SUM algorithm into a Convolution 3SUM algorithm with the same time bound, since the new numbers are still bounded by a polynomial in $n$. With the algorithm of Baran, Demaine and Pătraşcu this gives $O(n^2 (\log \log n)^2 / \log^2 n)$ expected time.
- **2026.** With the deterministic $O(n^{1.9992})$ algorithm for 3SUM of Alman and Vassilevska Williams (arXiv:2610.06783), the same map gives a deterministic $O(n^{1.9992})$ algorithm. Their paper also names Convolution 3SUM among the problems that it makes truly subquadratic. The randomized $O(n^{1.965})$ algorithm for 3SUM of Chan, Itakura, Ma and Yu (arXiv:2610.42012) gives a randomized $O(n^{1.965})$ algorithm. Both preprints are not yet refereed.

## Bounds

- **Unconditional.** $\Omega(n)$, to read the input. No better general lower bound is known.
- **Conditional, before 2026.** No $O(n^{2-\varepsilon})$ algorithm, conditional on the [3SUM conjecture](/3sum-conjecture/), by the reductions of Pătraşcu (randomized) and of Chan and He (deterministic).
- **After 2026.** The 3SUM conjecture is refuted in the preprints above, so this conditional bound has no base. The two problems stay equivalent: any further saving in the exponent of one gives a saving for the other.

## Reductions

- **From Convolution 3SUM to 3SUM.** Deterministic, one call of size $n$, linear time, $a(n) = b(n) = n^2$. Map $a_i$ to $x_i = a_i M + i$ with $M = 2n$, and ask for $x_i + x_j = x_k$. Then $x_i + x_j - x_k = (a_i + a_j - a_k) M + (i + j - k)$. The last term is between $-(n-1)$ and $2n - 2$, so its absolute value is less than $M$, and the sum is zero exactly when $a_i + a_j = a_k$ and $k = i + j$. For the three-array form, map $a$, $b$ and $c$ in the same way and use the three-set form of 3SUM.
- **From 3SUM to Convolution 3SUM** (Pătraşcu 2010). Randomized, $a(n) = b(n) = n^2$. A random hash function $h$ that is almost linear, so that $h(x) + h(y)$ is close to $h(x + y)$, sends the numbers into buckets, and the bucket numbers become array positions. A solution $a + b = c$ then sits at positions that almost add up, so a small number of shifted Convolution 3SUM instances cover it. Buckets with too many elements are rare and are handled directly, and the elements of the other buckets are spread over several instances so that each position holds one number. See [universal hash family](/universal-hash-family/).
- **From 3SUM to Convolution 3SUM, deterministic** (Chan and He, SOSA 2020). The same $a(n) = b(n) = n^2$, with no randomness.
- **From min-plus convolution to Convolution 3SUM** (Cygan, Mucha, Węgrzycki and Włodarczyk, Theorem 25 of the arXiv version, after Vassilevska Williams and Williams). Deterministic. The decision form "is $c_k \ge \max_{i+j=k}(a_i + b_j)$ for all $k$?" reduces to $O(\log W)$ instances of the three-array form, two for each length of binary prefix of the numbers, where $W$ bounds the absolute values. The instances test the conditions under which $x + y > z$ shows up in the prefixes of $x$, $y$ and $z$. With the equivalences of [min-plus convolution](/min-plus-convolution/), a truly subquadratic algorithm for Convolution 3SUM gives one for min-plus convolution.

Together, the first three items make 3SUM and Convolution 3SUM one [fine-grained equivalence class](/fine-grained-equivalence-class/).

## Applications

- **Triangle listing.** Pătraşcu reduced Convolution 3SUM to listing triangles and proved that listing $m$ triangles in a graph with $m$ edges has no $O(m^{4/3-\varepsilon})$ algorithm, conditional on the 3SUM conjecture. Kopelowitz, Pettie and Porat (SODA 2016) proved more bounds of this kind. See [triangle listing by degree](/triangle-listing-by-degree/) and [3SUM-hardness](/3sum-hardness/).
- **Dynamic problems.** Pătraşcu reduced it to the multiphase problem on set intersection, and from there to dynamic reachability, dynamic shortest paths and other problems. See [dynamic lower bounds](/dynamic-lower-bounds/).
- **Min-plus convolution.** The reduction above places [min-plus convolution](/min-plus-convolution/) below 3SUM in the order of hardness.

All these bounds are conditional on the 3SUM conjecture and lose their base if the 2026 preprints are correct, unless they also follow from another hypothesis such as the [OMv conjecture](/omv-conjecture/).

## References
