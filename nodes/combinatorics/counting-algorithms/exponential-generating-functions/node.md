---
tag: 4SJ31D
kind: definition
slug: exponential-generating-functions
name: Exponential generating functions
aliases:
- EGF
- exponential generating function
area: combinatorics/counting-algorithms
level: core
summary: Series sum a_n x^n / n!, suited to labeled structures.
prereqs: [generating-functions, factorial, binomial-coefficient]
see_also: [generating-functions, symbolic-method, bell-numbers, stirling-numbers-second-kind, derangement, counting-connected-labeled-graphs, counting-labeled-graphs, stirling-numbers-first-kind]
sources:
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Labelled structures and exponential generating functions
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Chapter 5, Section 5.1, The exponential formula
  - book: isbn:9781568812793
    title: Herbert S. Wilf, generatingfunctionology, third edition, A K Peters, 2006
    locator: Chapter 3, Cards, decks, and hands, the exponential formula
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.6, Exponential Generating Functions
---

The exponential generating function (EGF) of a sequence $a_0, a_1, a_2, \ldots$ is the formal power series $\sum_{n \ge 0} a_n z^n / n!$. It is the right tool for labeled objects, such as permutations, set partitions and labeled graphs, because the product of two EGFs counts the ways to split a set of labels between two structures. With it, a count of connected objects gives the count of all objects through the exponential function, and back through the logarithm. It is the labeled partner of the ordinary [generating function](/generating-functions/).

## Definition

**Notation.** $n \ge 0$ is the number of labels, $[n] = \{1, \ldots, n\}$, and $\binom{n}{k}$ is the [binomial coefficient](/binomial-coefficient/).

Let $(a_n)_{n \ge 0}$ be a sequence of numbers. Its exponential generating function is the formal power series

$$\hat A(z) = \sum_{n \ge 0} a_n \frac{z^n}{n!}.$$

So $a_n = n!\,[z^n] \hat A(z)$. The series is formal: no value is put in for $z$, and the series need not converge. A *labeled class* is a set of objects in which each object of size $n$ carries the labels $[n]$, one label on each atom, and $a_n$ is the number of objects of size $n$.

**Product rule.** For sequences $(a_n)$ and $(b_n)$,

$$\hat A(z)\, \hat B(z) = \sum_{n \ge 0} c_n \frac{z^n}{n!}, \qquad c_n = \sum_{k=0}^{n} \binom{n}{k} a_k b_{n-k}.$$

*Proof.* The coefficient of $z^n$ in the product is $\sum_k \frac{a_k}{k!} \frac{b_{n-k}}{(n-k)!}$. Multiply by $n!$ and use $\frac{n!}{k!(n-k)!} = \binom{n}{k}$. $\square$

The rule has a counting meaning. Let $c_n$ count the pairs $(\alpha, \beta)$ where the labels $[n]$ are split into a set $S$ of size $k$ and its complement, $\alpha$ is an $A$-object on $S$ and $\beta$ is a $B$-object on $[n] \setminus S$, both relabeled in increasing order. There are $\binom{n}{k}$ choices of $S$, then $a_k$ choices of $\alpha$ and $b_{n-k}$ choices of $\beta$, so this $c_n$ is the one of the rule. This is the *labeled product*.

**Exponential formula.** Let $a_0 = 0$, and let $a_n$ count the connected objects on $[n]$ for $n \ge 1$. Let $b_n$ count the sets of connected objects whose label sets split $[n]$ into blocks, one object on each block, with $b_0 = 1$. Then

$$\hat B(z) = \exp\bigl(\hat A(z)\bigr) = \sum_{k \ge 0} \frac{\hat A(z)^k}{k!}.$$

*Proof.* Because $a_0 = 0$, the series $\hat A(z)^k$ has no term below $z^k$, so only $k \le n$ adds to the coefficient of $z^n$, and the sum is a well defined formal series. By the product rule applied $k - 1$ times, $n!\,[z^n] \hat A(z)^k$ counts the sequences $(\alpha_1, \ldots, \alpha_k)$ of connected objects on an ordered split of $[n]$ into $k$ blocks, each block nonempty since $a_0 = 0$. The blocks are disjoint and nonempty, so they are distinct, and each set of $k$ objects arises from exactly $k!$ such sequences, one for each order. So $n!\,[z^n] \hat A(z)^k / k!$ counts the sets of $k$ connected objects on $[n]$. Summing over $k$ gives $b_n$. $\square$

**A recurrence for the coefficients.** Split by the component that holds the label 1. If it has $k$ labels, there are $\binom{n-1}{k-1}$ ways to choose its other labels, $a_k$ ways to build it, and $b_{n-k}$ ways to build the rest. So, for $n \ge 1$,

$$b_n = \sum_{k=1}^{n} \binom{n-1}{k-1} a_k\, b_{n-k}.$$

This computes $b_0, \ldots, b_N$ in $O(N^2)$ operations on exact integers. Solved for $a_n$, the same rule computes the connected counts from the totals, which is the logarithm $\hat A = \log \hat B$.

## Examples and non-examples

**Example 1: sets and permutations.** The sequence $a_n = 1$ has the EGF $e^z$. The sequence $a_n = n!$, the number of permutations of $[n]$, has the EGF $\sum_n z^n = 1/(1 - z)$.

**Example 2: cycles give permutations.** There are $(n-1)!$ cyclic orders on $[n]$, so the connected objects "one cycle" have the EGF $\sum_{n \ge 1} (n-1)! z^n/n! = \sum_{n \ge 1} z^n/n = \log \frac{1}{1 - z}$. A permutation is a set of cycles, by the [cycle decomposition](/permutation-cycle-decomposition/). The exponential formula gives $\exp(\log \frac{1}{1-z}) = \frac{1}{1-z}$, which is example 1 again.

**Example 3: derangements.** A [derangement](/derangement/) is a permutation with no cycle of length 1. Remove the term $z$ from the cycle series: $\exp(\log \frac{1}{1-z} - z) = \frac{e^{-z}}{1 - z}$. The coefficients times $n!$ are $1, 0, 1, 2, 9, 44, 265, 1854, 14833$ for $n = 0$ to $8$ (OEIS A000166).

**Example 4: involutions.** An involution has only cycles of length 1 and 2. There is one such cycle on 1 label and one on 2 labels, so the EGF is $\exp(z + z^2/2)$, with the counts $1, 1, 2, 4, 10, 26, 76, 232, 764$ (OEIS A000085).

**Example 5: set partitions.** A block of a set partition is a nonempty set, with the EGF $e^z - 1$. So the [Bell numbers](/bell-numbers/) have the EGF $\exp(e^z - 1)$, and the values $1, 1, 2, 5, 15, 52, 203, 877, 4140$ (OEIS A000110). Partitions into exactly $k$ blocks have the EGF $(e^z - 1)^k / k!$, which gives the [Stirling numbers of the second kind](/stirling-numbers-second-kind/).

**Example 6: ordered set partitions.** A sequence of $k$ nonempty blocks has the EGF $(e^z - 1)^k$. Summed over $k$, this is $\frac{1}{2 - e^z}$, with the Fubini numbers $1, 1, 3, 13, 75, 541, 4683$ (OEIS A000670).

**Example 7: connected graphs.** There are $2^{\binom{n}{2}}$ [labeled graphs](/counting-labeled-graphs/) on $[n]$, and each is a set of connected components. The recurrence above, solved for $a_n$, gives the [connected labeled graphs](/counting-connected-labeled-graphs/) $1, 1, 4, 38, 728, 26704, 1866256$ for $n = 1$ to $7$ (OEIS A001187).

**Non-example 1: the plain convolution.** The EGF product is not the EGF of $\sum_k a_k b_{n-k}$. With $a_n = b_n = 1$, the plain convolution is $n + 1$, but $e^z \cdot e^z = e^{2z}$ gives $2^n$. The binomial factor counts the choice of which labels go to which side, so $2^n$ is the number of ways to split $[n]$ into an ordered pair of sets.

**Non-example 2: unlabeled objects.** Integer partitions are unlabeled: two parts of the same size cannot be told apart. Their counts $p(n)$ have an EGF as a formal series, but the product rule has no meaning for them, and $\exp$ of the EGF of "one part" ($e^z - 1$) gives the Bell numbers, not $p(n)$. For unlabeled multisets the right tool is the ordinary series $\prod_k (1 - z^k)^{-1}$, see [counting integer partitions](/integer-partition-counting/).

**Non-example 3: a nonzero constant term.** The exponential formula needs $a_0 = 0$. If $a_0 \ne 0$, $\exp(\hat A)$ has the factor $e^{a_0}$, and its coefficients are not integers in general. Objects of size 0 are not allowed as components.

## Related definitions

- [Generating functions](/generating-functions/) are the ordinary form $\sum a_n z^n$, used for unlabeled objects. The two forms agree up to the factor $n!$, and the same sequence often has a simple form in one and not in the other: $n!$ has the EGF $1/(1-z)$, but its ordinary series $\sum n!\, z^n$ converges only at $z = 0$.
- The [symbolic method](/symbolic-method/) turns the labeled constructions (labeled product, sequence, set, cycle) into the EGF operations (product, $1/(1 - \cdot)$, $\exp$, $\log \frac{1}{1 - \cdot}$).
- The [Stirling numbers of the first kind](/stirling-numbers-first-kind/) count permutations by cycles, with the bivariate EGF $(1 - z)^{-u}$.
- The [Bell numbers](/bell-numbers/) and [counting set partitions](/counting-set-partitions/) use the EGF $\exp(e^z - 1)$.
- [Cayley's formula](/cayley-formula/) for labeled trees comes from the EGF equation $T(z) = z\, e^{T(z)}$ of rooted labeled trees and Lagrange inversion.
- The [binomial coefficient](/binomial-coefficient/) appears in the product rule, and the identity $e^z e^w = e^{z + w}$ is the [binomial theorem](/binomial-theorem/) in EGF form.

## References
