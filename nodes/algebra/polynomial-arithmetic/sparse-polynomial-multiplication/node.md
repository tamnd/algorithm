---
tag: YHNK2G
kind: algorithm
slug: sparse-polynomial-multiplication
name: Sparse polynomial multiplication
aliases:
- heap-based multiplication
- Johnson's algorithm for sparse multiplication
area: algebra/polynomial-arithmetic
level: advanced
summary: Multiplies sparse polynomials by merging rows of partial products with a heap, using s t coefficient products, O(s t log s) exponent comparisons and extra space linear in the smaller operand.
solves: [polynomial-multiplication]
model: blum-shub-smale-machine
complexity:
  vars: {s: the number of nonzero terms of the operand with fewer terms, t: the number of nonzero terms of the other operand}
  time: {worst: O(s t (1 + log s))}
  space: {extra: O(s)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [sparse-polynomial-representation, binary-heap]
see_also: [sparse-polynomial-representation, sparse-polynomial, k-way-merge, priority-queue, polynomial-multiplication, kronecker-substitution, monomial-ordering, sparse-polynomial-interpolation]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.4, Circular lists (Algorithm A, addition of polynomials, and Algorithm M, multiplication, on linked lists of terms)
  - paper: doi:10.1145/1086837.1086847
    title: Stephen C. Johnson, Sparse polynomial arithmetic, ACM SIGSAM Bulletin 8(3), 1974
    locator: pp. 63 to 71 (multiplication by a heap of partial products)
  - paper: doi:10.1016/j.jsc.2010.08.014
    title: Michael Monagan and Roman Pearce, Sparse polynomial division using a heap, Journal of Symbolic Computation 46(7), 2011
    locator: pp. 807 to 822 (heap multiplication and division, chaining, and the choice of the smaller operand for the heap)
  - paper: doi:10.1145/1576702.1576739
    title: Michael Monagan and Roman Pearce, Parallel sparse polynomial multiplication using heaps, ISSAC 2009
    locator: pp. 263 to 270
  - paper: doi:10.1006/jsco.1997.0176
    title: Thomas Yan, The geobucket data structure for polynomials, Journal of Symbolic Computation 25(3), 1998
    locator: pp. 285 to 293
  - paper: doi:10.1145/3373207.3404026
    title: Pascal Giorgi, Bruno Grenet and Armelle Perret du Cray, Essentially optimal sparse polynomial multiplication, ISSAC 2020
    locator: Abstract and main theorem (a probabilistic algorithm quasi-linear in the size of the input and the output)
  - paper: doi:10.1145/3208976.3209027
    title: Daniel S. Roche, What can (and can't) we do with sparse polynomials?, ISSAC 2018
    locator: pp. 25 to 30 (survey of sparse multiplication)
---

Heap-based multiplication computes the product of two polynomials in [sparse form](/sparse-polynomial-representation/) and writes its terms in increasing order of exponent. It sees the $s t$ products of a term of one operand by a term of the other as $s$ sorted rows and merges the rows with a [binary heap](/binary-heap/) of size $s$, the smaller number of terms. It uses $s t$ coefficient multiplications, $O(s t \log s)$ exponent comparisons and $O(s)$ extra space besides the output. Stephen Johnson described it in 1974, and Monagan and Pearce developed it into fast sparse multiplication and division.

## In plain words

Each term of the first polynomial times all terms of the second gives a row of terms, already in order of power. The product is the sum of all rows. So we merge the rows, like merging several sorted piles of cards into one pile.

We keep one card from each row in a heap, a structure that always gives back the card with the smallest power. We take the smallest card and add it to the result. If the result already ends with the same power, we add the two numbers instead. Then we put the next card of the same row into the heap. Equal powers come out one after the other, so they combine at once. At the end we drop the terms whose sum is zero.

The heap holds one card per row, so it stays small even when the product has many terms.

## The problem

Let $R$ be a commutative ring. Given $a = \sum_{i < s} a_i x^{e_i}$ and $b = \sum_{j < t} b_j x^{f_j}$ in $R[x]$ as lists of (exponent, coefficient) pairs that meet invariant (S) of the [sparse representation](/sparse-polynomial-representation/), that is $e_0 < e_1 < \cdots$, $f_0 < f_1 < \cdots$ and no zero coefficient, return the list that meets (S) for $a b$. The degrees can be much larger than $s$ and $t$, so the method must not use an array indexed by exponent. We take $s \le t$; the implementation swaps the operands when needed.

**Cost model.** We use the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $R$, as on the representation page: each ring operation and zero test costs 1, and each comparison or addition of two exponents costs 1. The last rule is right on a [word RAM](/word-ram/) when the exponents fit in a machine word.

## The algorithm

```pseudo id=main
HEAP-MULTIPLY(a, b)                            ▷ s = |a| ≤ t = |b|; both meet (S)
L1  if s = 0 then return [ ]
L2  H ← a min-heap of the keys (e[i] + f[0], i, 0) for i = 0, …, s − 1
L3  c ← [ ]
L4  while H is not empty do
L5      (k, i, j) ← POP-MIN(H)
L6      u ← a[i] · b[j]
L7      if c is not empty and the last exponent of c is k then add u to the last coefficient of c
L8      else append (k, u) to c
L9      if j + 1 < t then PUSH(H, (e[i] + f[j + 1], i, j + 1))
L10 return c without the terms whose coefficient is 0
```

The heap compares entries by the key $k$ first; ties can be broken in any way. Row $i$ is the list of the products $a_i b_j x^{e_i + f_j}$ for $j = 0, 1, \ldots, t - 1$, and its exponents increase because the $f_j$ do. The heap holds the next unused entry of each row that is not yet used up, so lines L2 to L9 are a [$k$-way merge](/k-way-merge/) of $s$ sorted rows. Line L7 combines the products with the same exponent. Over a ring with zero divisors, and over any ring when terms cancel, a combined coefficient can be zero, and line L10 removes it.

## Example

Over $\mathbb{Z}$, let $a = 1 + x^2$, so $a = [(0, 1), (2, 1)]$ and $s = 2$, and $b = 1 - x^2 + x^4$, so $b = [(0, 1), (2, -1), (4, 1)]$ and $t = 3$. Line L2 makes the heap $\{(0, 0, 0), (2, 1, 0)\}$. When two entries have the same key, the table pops the one with the smaller row first, as Python's `heapq` does with these tuples.

| Pop | $(k, i, j)$ | $u = a_i b_j$ | $c$ after L7 or L8 | Push |
|---|---|---|---|---|
| 1 | $(0, 0, 0)$ | $1$ | $(0, 1)$ | $(2, 0, 1)$ |
| 2 | $(2, 0, 1)$ | $-1$ | $(0, 1), (2, -1)$ | $(4, 0, 2)$ |
| 3 | $(2, 1, 0)$ | $1$ | $(0, 1), (2, 0)$ | $(4, 1, 1)$ |
| 4 | $(4, 0, 2)$ | $1$ | $(0, 1), (2, 0), (4, 1)$ | none, $j + 1 = t$ |
| 5 | $(4, 1, 1)$ | $-1$ | $(0, 1), (2, 0), (4, 0)$ | $(6, 1, 2)$ |
| 6 | $(6, 1, 2)$ | $1$ | $(0, 1), (2, 0), (4, 0), (6, 1)$ | none |

There are $s t = 6$ pops, and the heap never holds more than $s = 2$ entries. Line L10 removes the two zero terms and returns $[(0, 1), (6, 1)]$, that is $(1 + x^2)(1 - x^2 + x^4) = 1 + x^6$. As a second check, $(1 + 2x^5)(3 + x^2 + x^{10}) = 3 + x^2 + 6x^5 + 2x^7 + x^{10} + 2x^{15}$, with no combination at all. The tests run both examples.

## Correctness

The heap holds at most one pair $(i, j)$ from each row, namely the first pair of the row that is not yet popped. So every pair is popped exactly once. When a pair with key $k$ is popped, the pairs still in the heap have keys at least $k$, and every pair pushed later follows one of them in its row and so has a larger key. So the keys come out in nondecreasing order. The pairs with the same key then come out one after the other, and lines L7 and L8 add their products into one term. The list $c$ has strictly increasing exponents and sums to $a b$, and line L10 only removes zero terms. The full proof is below.

## Complexity

All bounds in this section are proved in the cost model above.

- **Ring operations.** Line L6 runs once per pair: $s t$ multiplications. Line L7 adds at most $s t - 1$ times. Line L10 makes at most $s t$ zero tests.
- **Heap operations.** Line L2 builds a heap of $s$ entries with $O(s)$ comparisons. There are $s t$ pops and $s (t - 1)$ pushes on a heap of at most $s$ entries, each with $O(1 + \log s)$ comparisons. Line L9 adds two exponents once per push. In total $O(s t (1 + \log s))$ exponent operations.
- **Space.** The heap has at most $s$ entries, so the extra space is $O(s)$. The output has at most $s t$ terms, and before line L10 the list $c$ has one term per distinct key.

Making the operand with fewer terms the heap rows gives the factor $\log \min(s, t)$ rather than $\log \max(s, t)$.

**A lower bound for this output.** Some products have $s t$ nonzero terms. Take $a = \sum_{i < s} x^i$ and $b = \sum_{j < t} x^{s j}$. The exponents $i + s j$ are all distinct, because $i$ is the remainder of $i + s j$ modulo $s$ and $j$ is the quotient, so $a b$ has $s t$ nonzero terms. Any method must write them, so $s t$ operations are needed in the worst case, and the heap method is within a factor $O(1 + \log s)$ of this.

**Observed in practice.** Monagan and Pearce argue, and show by timings, that the heap method is fast because the heap is small and stays in cache, and the products are made one at a time and are not stored. These are measurements in their papers, not proved bounds.

## Properties

- **Output in order.** The terms come out in increasing order of exponent, one at a time. A consumer can stop early, for example to get only the terms of degree less than some bound, or can feed the terms into a sparse division, as in Monagan and Pearce's heap division.
- **Small working memory.** Only $O(s)$ words are needed besides the output, and the $s t$ products are never stored together.
- **Generic in the coefficients.** Only ring addition, multiplication and the zero test are used, so the method works over any commutative ring in a normal form.
- **Multivariate use.** Exponents can be monomials compared in a [monomial ordering](/monomial-ordering/), because such an order is compatible with multiplication: if $u < v$ then $u w < v w$. The proof needs only this fact, so the method works unchanged. Monagan and Pearce pack the exponent vector of a monomial into one machine word, so that a comparison or an addition of monomials is one word operation.
- Deterministic, not recursive, and not in place.

## Variants and improvements

- **Heap on the larger operand.** With the $t$ terms of the larger operand as rows, the heap has $t$ entries and the cost is $O(s t \log t)$. Monagan and Pearce use the smaller operand for the rows.
- **Chaining.** Monagan and Pearce link the entries that have the same exponent into a chain at one heap node, so that each exponent is in the heap only once. This does fewer heap operations when many products share an exponent, as in nearly dense products.
- **Dictionary method.** Put each product into a [hash table](/hash-table/) indexed by exponent, then sort the distinct exponents. This is the method of the `mul` block on the [sparse representation](/sparse-polynomial-representation/) page. With hashing it does expected $O(s t)$ work plus a sort of the output, but it needs space for all distinct exponents at once.
- **Sort all products.** Form all $s t$ products, sort them by exponent, and combine. It costs $O(s t \log(s t))$ and $O(s t)$ space.
- **Geobuckets.** Yan's geobuckets add polynomials into buckets of sizes that grow geometrically and merge buckets when they become full. They are used for long sums of polynomials, as in the reductions of Gröbner basis computations.
- **Dense methods for dense products.** When $a$ and $b$ are nearly dense, use dense [polynomial multiplication](/polynomial-multiplication/) with Karatsuba or the [FFT](/fft-polynomial-multiplication/). For multivariate inputs, [Kronecker substitution](/kronecker-substitution/) changes the product into one univariate product.
- **Output-sensitive algorithms.** The heap method costs at least $s t$ even when the product has few terms, as for $a = \sum_{i < m} x^i$ and $b = \sum_{j < m} (x^{m j} - x^{m j + 1})$, with $m$ and $2m$ terms, whose product is $1 - x^{m^2}$. Indeed $(1 - x) a = 1 - x^m$ and $b = (1 - x) \sum_{j < m} x^{m j}$, so $a b = (1 - x^m) \sum_{j < m} x^{m j} = 1 - x^{m^2}$. Giorgi, Grenet and Perret du Cray (2020) give a probabilistic algorithm whose number of bit operations is quasi-linear in the size of the input and the output, over fields of characteristic zero or larger than the degree.
- **Parallel versions.** Monagan and Pearce (2009) give a parallel heap multiplication for multicore computers.

## When to use it

Use the heap method when the inputs are sparse, the degree is much larger than the number of terms, and the product is also expected to be sparse. It is a good default for multivariate polynomials in distributed form, and it is the right choice when the terms are needed in order or when memory is limited. When the inputs are nearly dense, a dense method is faster: the heap method costs $\Theta(n^2 \log n)$ for two dense inputs of degree $n$, which is worse than [schoolbook multiplication](/schoolbook-multiplication/) in dense form.

## Pitfalls

- **Forgetting the zero test.** Products with equal exponents can cancel, as in the example. Without line L10 the result breaks invariant (S), and later equality tests fail.
- **Zero divisors.** Over $\mathbb{Z}/6\mathbb{Z}$, $2 \cdot 3 = 0$, so even a single product can be zero. Line L10 also removes these.
- **Combining only adjacent output terms.** Line L7 compares with the last term of $c$ only. This is correct because the keys come out in nondecreasing order; a variant that pops in another order must search the output.
- **Exponent overflow.** In a language with fixed-size integers, $e_i + f_j$ can overflow. Check the degrees first, or use a wider type.
- **Heap ties.** If heap entries hold the coefficients themselves, a tie on the exponent can make the heap compare coefficients, which may not be ordered. Store row and column indices instead, as here.

## Implementations

## History

Johnson (1974) described the multiplication of sparse polynomials by merging the rows of partial products with a heap and compared it with the methods then used in the Altran system. Knuth's Volume 1, Section 2.2.4, had earlier given the addition and multiplication of polynomials stored as linked lists of terms. Yan (1998) introduced geobuckets for sums of many polynomials. Monagan and Pearce (2009, 2011) returned to Johnson's heap, added chaining, packed exponents and a parallel version, and extended it to division. Giorgi, Grenet and Perret du Cray (2020) gave a probabilistic output-sensitive algorithm. Roche's survey (2018) describes the state of sparse multiplication before that result.

## References
