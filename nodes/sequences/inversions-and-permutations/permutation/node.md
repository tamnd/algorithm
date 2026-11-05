---
tag: 13T8RN
kind: definition
slug: permutation
name: Permutation
aliases:
- arrangement
- arrangement of a set
- bijection of a finite set to itself
- bijection of {1..n}
area: sequences/inversions-and-permutations
level: intro
summary: A rearrangement of n distinct items, equivalently a bijection from a set to itself.
prereqs: [total-order]
see_also: [permutation-cycles, permutation-inverse, inversion, symmetric-group, lehmer-code, random-permutation, multiset-permutations, generating-all-permutations]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.5 (permutations and factorials) and Section 1.3.3 (applications to permutations, cycle notation, products and inverses)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1 (combinatorial properties of permutations)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.3 (cycles and inversions)
---

A permutation of a finite set $X$ is a bijection $\pi : X \to X$, that is, a rule that sends each item of $X$ to an item of $X$ so that no two items go to the same place. For $X = \{1, \ldots, n\}$ a permutation is the same thing as an ordering of the numbers $1$ to $n$, and there are $n!$ of them. Each array of $n$ distinct keys has a permutation inside it, the order of its ranks, and the [sorting problem](/sorting-problem/) asks for the permutation that puts the keys in order. The pages of this area study permutations as objects: their [cycles](/permutation-cycles/), [inversions](/inversion/), [inverses](/permutation-inverse/), codes and distances.

## Definition

Let $[n] = \{1, 2, \ldots, n\}$ for $n \ge 0$, with $[0] = \emptyset$. A **permutation of $[n]$** is a function $\pi : [n] \to [n]$ that is a bijection: for each $j \in [n]$ there is exactly one $i \in [n]$ with $\pi(i) = j$. For a finite set, injective, surjective and bijective are the same condition, because a map from a set of $n$ items to itself that misses a value must hit some other value twice.

**Notations.** The same permutation has three common written forms.

- *One-line notation* lists the images in order: $\pi = \pi(1)\,\pi(2) \cdots \pi(n)$. As an array, $\pi[i] = \pi(i)$. This is the form that programs use, usually with 0-based indices and values $0$ to $n - 1$.
- *Two-line notation* writes $1, \ldots, n$ on the top row and the images below them.
- *Cycle notation* writes the [cycles](/permutation-cycles/) of $\pi$: $(a_1\ a_2\ \ldots\ a_k)$ means $\pi(a_1) = a_2$, $\ldots$, $\pi(a_{k-1}) = a_k$ and $\pi(a_k) = a_1$.

**Product.** The product of two permutations is their composition, $(\sigma\tau)(i) = \sigma(\tau(i))$: apply $\tau$ first, then $\sigma$. Some books, Knuth among them, read products from left to right instead. The two conventions give mirror results, so a page that multiplies permutations must say which one it uses. All pages of this area apply the right factor first.

**Identity and inverse.** The identity is $\iota(i) = i$, written $12 \cdots n$. Each permutation has an [inverse](/permutation-inverse/) $\pi^{-1}$ with $\pi\pi^{-1} = \pi^{-1}\pi = \iota$. With the product, the $n!$ permutations of $[n]$ form the [symmetric group](/symmetric-group/) $S_n$.

**Count.** There are $n \cdot (n-1) \cdots 1 = n!$ permutations of $[n]$. *Proof.* The image $\pi(1)$ has $n$ choices. For each choice, $\pi(2)$ must avoid it and has $n - 1$ choices, and so on until $\pi(n)$, which has one choice. Each sequence of choices gives a different bijection, and each bijection comes from one sequence. $\square$ The [factorial](/factorial/) page gives the growth of $n!$.

**The permutation of an array.** Let $a = (a_1, \ldots, a_n)$ be a sequence of distinct items from a [total order](/total-order/). Its *standardization* $\operatorname{std}(a)$ is the permutation $\pi$ with $\pi(i) = $ the rank of $a_i$ among $a_1, \ldots, a_n$, where the smallest item has rank 1. Two sequences with the same standardization have the same relative order, so a comparison-based algorithm does the same steps on both. This is why results about permutations of $[n]$ apply to all arrays of distinct keys.

**Permutation matrix.** The matrix $P_\pi$ with $(P_\pi)_{i,j} = 1$ if $\pi(j) = i$ and $0$ otherwise has exactly one 1 in each row and in each column. With this convention $P_\sigma P_\tau = P_{\sigma\tau}$, and $P_\pi^{-1} = P_\pi^{\mathsf T}$. The [determinant](/determinant/) of $P_\pi$ is the [sign](/permutation-parity/) of $\pi$.

## Examples and non-examples

**One permutation in three notations.** Let $\pi = 3\,1\,4\,5\,2$, so $\pi(1) = 3$, $\pi(2) = 1$, $\pi(3) = 4$, $\pi(4) = 5$ and $\pi(5) = 2$.

$$\pi = \begin{pmatrix} 1 & 2 & 3 & 4 & 5 \\ 3 & 1 & 4 & 5 & 2 \end{pmatrix} = (1\ 3\ 4\ 5\ 2).$$

Starting at 1, the images are $1 \to 3 \to 4 \to 5 \to 2 \to 1$, so $\pi$ is one cycle of length 5. Its inverse is $\pi^{-1} = 2\,5\,1\,3\,4$, and it has 4 inversions.

**Products do not commute.** Let $\tau = (1\ 2) = 2\,1\,3\,4\,5$. Then $\pi\tau = 1\,3\,4\,5\,2$ and $\tau\pi = 3\,2\,4\,5\,1$. Applying $\tau$ first swaps the first two *positions* of the one-line notation of $\pi$. Applying $\tau$ last swaps the *values* 1 and 2.

**Small cases.** $S_0$ has one element, the empty permutation, because $0! = 1$. $S_1 = \{1\}$. $S_3$ has the $6$ elements $123, 132, 213, 231, 312, 321$, listed in [lexicographic order](/lexicographic-order/).

**Standardization.** The array $(40, 10, 70, 90, 20)$ has standardization $3\,1\,4\,5\,2$, the permutation above. The array $(7, 2, 9, 9.5, 3)$ has the same one.

**Non-examples.**

- $2\,2\,1$ is not a permutation of $[3]$: the value 2 appears twice and 3 does not appear. It is a word over $[3]$, and the arrangements of a multiset such as $\{1, 2, 2\}$ are [multiset permutations](/multiset-permutations/), counted by multinomial coefficients and not by $n!$.
- The map $i \mapsto 2i$ from $[3]$ to $[6]$ is injective but is not a permutation, because its domain and its codomain are different sets.
- The array $0\,2\,1$ is a permutation of $\{0, 1, 2\}$, not of $[3]$. Code that mixes the 0-based and 1-based conventions reads past the end of an array.
- On an infinite set, an injective map need not be a bijection: $i \mapsto i + 1$ on the natural numbers misses 0. The pigeonhole argument above needs a finite set.

## Related definitions

- **$k$-permutation.** An injective sequence of $k$ items from $[n]$, also called an arrangement or a partial permutation. There are $n!/(n-k)!$ of them, the falling factorial $n^{\underline{k}}$.
- **[Cycles](/permutation-cycles/).** The orbits of $i \mapsto \pi(i)$. A fixed point is a cycle of length 1, a [derangement](/derangement/) has none, and an involution has only cycles of length 1 and 2.
- **[Inversion](/inversion/).** A pair $i < j$ with $\pi(i) > \pi(j)$. The number of inversions measures how far $\pi$ is from the identity, and its parity is the [parity](/permutation-parity/) of $\pi$.
- **[Inverse permutation](/permutation-inverse/).** The permutation that undoes $\pi$. In an array it maps each value to its position.
- **[Symmetric group](/symmetric-group/).** The set $S_n$ with composition as the product.
- **Codes.** The [Lehmer code](/lehmer-code/) and the [inversion table](/inversion-table/) are bijections from $S_n$ to sequences $(c_1, \ldots, c_n)$ with $0 \le c_i \le n - i$. They give the [rank](/permutation-rank-unrank/) of a permutation in the [factorial number system](/factorial-number-system/).
- **Distances.** [Kendall tau](/kendall-tau-distance/), [Cayley](/cayley-distance/), [Ulam](/ulam-distance/) and [Spearman's footrule](/spearman-footrule/) compare two permutations.
- **Random permutation.** A [uniform random permutation](/random-permutation/) gives each of the $n!$ permutations probability $1/n!$. It is the input model of average-case analysis of sorting.

## References
