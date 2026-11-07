---
tag: 3AC783
kind: data-structure
slug: sparse-polynomial-representation
name: Sparse polynomial representation
aliases:
- linked-list polynomial
- sorted term list
area: algebra/polynomial-arithmetic
level: core
summary: Stores only nonzero terms as (degree, coefficient) pairs; efficient when most coefficients are zero.
implements: [polynomial]
model: blum-shub-smale-machine
complexity:
  vars: {s: the number of nonzero terms of the first operand, t: the number of nonzero terms of the second operand}
  time: {worst: Θ(s + t), best: Θ(s + t)}
  space: {extra: Θ(s + t)}
prereqs: [polynomial, dense-polynomial-representation]
see_also: [sparse-polynomial, sparse-polynomial-multiplication, dense-polynomial-representation, linked-list, k-way-merge, monomial-ordering, sparse-polynomial-interpolation, sparse-vector]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.4, Circular lists (Algorithm A, addition of polynomials stored as linked lists of terms, and Algorithm M, multiplication)
  - paper: doi:10.1145/1086837.1086847
    title: Stephen C. Johnson, Sparse polynomial arithmetic, ACM SIGSAM Bulletin 8(3), 1974
    locator: pp. 63 to 71
  - paper: doi:10.1016/j.jsc.2010.08.014
    title: Michael Monagan and Roman Pearce, Sparse polynomial division using a heap, Journal of Symbolic Computation 46(7), 2011
    locator: pp. 807 to 822 (sorted term arrays, packed exponents, and heap-based multiplication and division)
  - paper: doi:10.1145/3208976.3209027
    title: Daniel S. Roche, What can (and can't) we do with sparse polynomials?, ISSAC 2018
    locator: pp. 25 to 30 (survey of sparse algorithms and of the problems that are hard in the sparse model)
---

The sparse representation stores a [polynomial](/polynomial/) as the list of its nonzero terms, each a pair (exponent, coefficient), sorted by exponent. A polynomial with $t$ nonzero terms takes $O(t)$ space whatever its degree, so $x^{1000000} + 1$ needs two pairs where the [dense form](/dense-polynomial-representation/) needs a million entries. Addition is a merge of two sorted lists and takes $\Theta(s + t)$ operations; multiplication takes $st$ coefficient products; evaluation takes $O(t \log n)$ for degree $n$. The cost is that some operations, such as division and gcd, can produce dense results from sparse inputs.

## In plain words

Most of the numbers in front of the powers of x can be zero, as in x to the power one million plus one. The dense form would store a million zeros. The sparse form stores only the terms that are not zero: for each one, the power and the number in front of it. The terms are kept in order of the power, lowest first.

To add two polynomials, walk along both lists at the same time, like merging two sorted piles of cards. Take the term with the smaller power. When both lists have the same power, add the two numbers, and drop the term if the sum is zero. Because no zero term is ever stored and the order is fixed, each polynomial has only one list.

## The abstract type

The representation implements the [polynomial](/polynomial/) type over a commutative ring $R$: `add`, `sub`, `neg`, scalar multiplication, `mul`, `evaluate`, `degree`, the leading coefficient and the formal derivative. Costs are in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $R$: each ring operation and zero test costs 1. Unlike the dense form, the sparse form must also compare and add exponents. We count each comparison or addition of two exponents as 1 too, which is correct on a [word RAM](/word-ram/) when the exponents fit in a machine word. With exponents of arbitrary size, an exponent operation costs $O(\log n)$ word operations for degree $n$.

## Representation

A value is a list $a = [(e_0, c_0), (e_1, c_1), \ldots, (e_{t-1}, c_{t-1})]$ of $t \ge 0$ pairs with $e_i$ nonnegative integers and $c_i \in R$. It stands for

$$\operatorname{val}(a) = \sum_{i=0}^{t-1} c_i x^{e_i} \in R[x].$$

**Invariant (S).** $e_0 < e_1 < \cdots < e_{t-1}$ and every $c_i \ne 0$.

Each $f \in R[x]$ has exactly one list that meets (S): the list of its nonzero terms in increasing order of exponent. The zero polynomial is the empty list. So two values are equal exactly when the lists are equal, $\deg f = e_{t-1}$ (or $-\infty$ when $t = 0$), and the leading coefficient is $c_{t-1}$, both in $O(1)$ time. As for the dense form, the coefficients must be stored in a normal form for $R$, so that the test $c_i \ne 0$ is a real zero test.

The list can be an array of pairs, as in the implementation below and in most current libraries, or a [linked list](/linked-list/) of term nodes, as in Knuth's Section 2.2.4. An array is more compact and faster to scan; a linked list allows insertion of a term in $O(1)$ time once its place is known. Some systems store the terms in decreasing order of exponent, so that the leading term comes first; the algorithms are the same.

**Number of terms.** We write $\#f$ for the number of nonzero terms. Then $\#(f + g) \le \#f + \#g$ and $\#(f g) \le \#f \cdot \#g$, and $\#f \le \deg f + 1$.

## Operations

### Addition

```pseudo id=main
ADD(a, b)                                 ▷ both meet (S); s = |a|, t = |b|
L1  i ← 0; j ← 0; c ← [ ]
L2  while i < s and j < t do
L3      if a[i].e < b[j].e then append a[i] to c; i ← i + 1
L4      else if a[i].e > b[j].e then append b[j] to c; j ← j + 1
L5      else                                ▷ the same exponent
L6          u ← a[i].c + b[j].c
L7          if u ≠ 0 then append (a[i].e, u) to c
L8          i ← i + 1; j ← j + 1
L9  append a[i .. s − 1] and then b[j .. t − 1] to c
L10 return c
```

This is the merge step of [merge sort](/merge-sort/), with the extra rule of lines L5 to L8 for equal keys. Line L7 is the only place where a term can vanish, and it keeps (S): a sum of two coefficients that is zero is not stored. At most one of the two tails at line L9 is nonempty. Subtraction is ADD with the negated second operand.

### Multiplication

```pseudo id=mul
MUL(a, b)
M1  D ← an empty map from exponents to elements of R
M2  for each (e, u) in a do
M3      for each (d, v) in b do
M4          D[e + d] ← D[e + d] + u · v     ▷ D[k] is 0 if k is not yet a key
M5  return the pairs (k, D[k]) with D[k] ≠ 0, sorted by k
```

The map $D$ is a [hash table](/hash-table/) keyed by the exponent. Line M4 runs $st$ times. Line M5 removes the coefficients that cancel and restores (S). The [sparse multiplication](/sparse-polynomial-multiplication/) page gives Johnson's method, which merges the $s$ rows $u \cdot x^e \cdot b$ with a [binary heap](/binary-heap/) and needs no hash table and no final sort.

### Evaluation

```pseudo id=eval
EVALUATE(a, z)                            ▷ the value at z in R
E1  y ← 0; p ← 1; prev ← 0
E2  for each (e, u) in a, in increasing order of e do
E3      p ← p · z^(e − prev)                ▷ binary powering
E4      prev ← e
E5      y ← y + u · p
E6  return y
```

After line E3, $p = z^e$. [Binary powering](/binary-exponentiation/) computes $z^g$ with at most $2 \lfloor \log_2 g \rfloor$ multiplications for $g \ge 1$. [Horner's rule](/horner-rule/) on the dense form would take $n$ multiplications for degree $n$, one for each power, including the powers with a zero coefficient.

The **derivative** maps each term $(e, c)$ with $e \ge 1$ to $(e - 1, e \cdot c)$ and drops the terms with $e \cdot c = 0$; this happens in characteristic $p$ when $p \mid e$. **Scalar multiplication** by $u$ maps $(e, c)$ to $(e, u c)$ and drops the products that are zero, which can happen only when $u$ is a zero divisor. Neither operation changes the order of the exponents, so both keep (S). **Conversion** from the dense form keeps the entries that are not zero, and conversion to the dense form writes $\deg f + 1$ entries.

## Example

**A sum.** Over $\mathbb{Z}$, let $a = 3 + 2x^5 + x^{100}$ and $b = 4x^5 - x^{100} + x^{200}$, stored as $[(0, 3), (5, 2), (100, 1)]$ and $[(5, 4), (100, -1), (200, 1)]$.

| $i$ | $j$ | compared exponents | action | $c$ after the step |
|---|---|---|---|---|
| 0 | 0 | $0 < 5$ | line L3 | $[(0, 3)]$ |
| 1 | 0 | $5 = 5$ | $u = 2 + 4 = 6$, kept | $[(0, 3), (5, 6)]$ |
| 2 | 1 | $100 = 100$ | $u = 1 - 1 = 0$, dropped | $[(0, 3), (5, 6)]$ |
| 3 | 2 | loop ends | line L9 appends $b[2]$ | $[(0, 3), (5, 6), (200, 1)]$ |

So $a + b = 3 + 6x^5 + x^{200}$, after 4 exponent comparisons and 2 coefficient additions. The dense form would add 201 pairs of entries.

**A product with cancellation.** $(1 + x^{100})(-1 + x^{100})$: line M4 runs 4 times and gives $D[0] = -1$, $D[100] = 1 - 1 = 0$ and $D[200] = 1$. Line M5 drops $D[100]$, and the result is $[(0, -1), (200, 1)]$, that is $x^{200} - 1$.

**An evaluation over $\mathbb{F}_7$.** Evaluate $a = 3 + 2x^5 + x^{100}$ at $z = 3$. The first term gives $p = 1$ and $y = 3$. The second gives $p = 3^5 = 243 \equiv 5$ and $y = 3 + 2 \cdot 5 = 13 \equiv 6$. The third gives $p = 5 \cdot 3^{95} \equiv 5 \cdot 5 = 25 \equiv 4$, since $3^6 \equiv 1$ and $95 \equiv 5 \pmod 6$, and $y = 6 + 4 = 10 \equiv 3$. So $a(3) = 3$ in $\mathbb{F}_7$. The two powerings take $3$ and $11$ multiplications, and lines E3 and E5 add $5$ more, so the evaluation takes $19$ multiplications instead of the $100$ of Horner's rule.

**A dense product of sparse factors, and the other way round.** $(x - 1)(1 + x + \cdots + x^{n-1}) = x^n - 1$: a 2-term polynomial times an $n$-term one gives 2 terms. Read from right to left, the exact quotient $(x^n - 1) / (x - 1)$ of two sparse polynomials has $n$ terms. So the size of the output of division is not bounded by the size of the input.

## Correctness

ADD keeps the [loop invariant](/loop-invariant/) that $c$ meets (S), that $\operatorname{val}(c)$ is the sum of the terms $a[0 .. i-1]$ and $b[0 .. j-1]$, and that every exponent in $c$ is less than both $a[i].e$ and $b[j].e$ when they exist. At the end one list is used up, and the tail of the other has larger exponents than all of $c$. MUL is correct because $D[k]$ ends as $\sum_{e + d = k} u v$, the coefficient of $x^k$ in the product. EVALUATE keeps $p = z^{\text{prev}}$ and $y = \sum c_i z^{e_i}$ over the terms read so far. The full proof is in the proof file.

## Complexity

All costs are in the model of the abstract type: ring operations and zero tests in $R$, and comparisons and additions of exponents, each at unit cost. Let $s = \#a$, $t = \#b$ and $n = \max(\deg a, \deg b)$.

| operation | cost | notes |
|---|---|---|
| `add`, `sub` | at most $s + t - 1$ comparisons, at most $\min(s, t)$ ring additions and zero tests | $\Theta(s + t)$, since the output is written |
| `neg`, scalar multiple, derivative | $t$ ring operations | no comparisons |
| `mul` | $st$ multiplications, at most $st$ additions, $st$ exponent additions, and a sort of $k \le st$ keys | $O(st \log(st))$ in the worst case, with $O(1)$ expected time per hash table update |
| `evaluate` | at most $2t \log_2 n + 2t$ multiplications and $t$ additions | $O(t \log n)$ |
| `degree`, leading coefficient | 0 | by (S) |
| space | $s + t$ for a sum, at most $st$ for a product | |

ADD makes one comparison per pass of line L2, and each pass consumes at least one term, so at most $s + t - 1$ passes. The sort in line M5 dominates when the product has about $st$ terms; Johnson's heap method takes $O(st \log \min(s, t))$ comparisons and is deterministic. For EVALUATE, the gaps $g_i = e_i - e_{i-1}$ are each at most $n$, so the powers cost at most $2 \sum \log_2 g_i \le 2t \log_2 n$ multiplications. These bounds are proved. The faster speed of the sparse form when $t$ is much smaller than $n$ is observed in practice and follows from the counts.

The sizes $s$ and $t$ do not bound the cost of every operation. The quotient of $x^n - 1$ by $x - 1$ has $n$ terms, and the gcd of two sparse polynomials can have many more terms than both inputs. Roche (2018) surveys which problems have algorithms polynomial in the sparse size, $t \log n$, and which are hard. For example, deciding whether two sparse polynomials have a nontrivial gcd is NP-hard, a result of Plaisted that Roche cites.

## Variants

- **Decreasing order.** Store the leading term first. Long division then reads the leading term at once, and heap-based multiplication produces terms in this order.
- **Linked lists.** Knuth's Algorithm A in Section 2.2.4 adds polynomial $P$ into polynomial $Q$ in place, on circular linked lists with a sentinel node, and inserts or deletes terms of $Q$ as it goes. Algorithm M builds multiplication from it.
- **Hash map of terms.** Store the terms in a [hash table](/hash-table/) from exponents to coefficients. Lookup and update of one term take $O(1)$ expected time, but the leading term and ordered output need a sort.
- **Multivariate distributed form.** For polynomials in $x_1, \ldots, x_k$, store pairs (exponent vector, coefficient), sorted by a [monomial ordering](/monomial-ordering/). ADD is unchanged with the ordering in place of $<$. Monagan and Pearce pack each exponent vector into one machine word, so that the comparisons and the additions of exponents are single word operations. See [sparse polynomial](/sparse-polynomial/).
- **Recursive form.** A polynomial in $x_k$ whose coefficients are sparse polynomials in $x_1, \ldots, x_{k-1}$. This form suits algorithms that work one variable at a time, such as recursive gcd methods.
- **Sparse interpolation.** Recover the sparse form of a polynomial that is given only by a procedure to evaluate it: [sparse interpolation](/sparse-polynomial-interpolation/).

## When to use it

Use the sparse form when the number of terms $t$ is much smaller than the degree, as in $x^n - 1$, in polynomials with a few large exponents, and in most multivariate polynomials from applications, where the dense array over all exponent vectors would be enormous. Use the [dense form](/dense-polynomial-representation/) when a fixed fraction of the coefficients are nonzero, and for the fast algorithms based on the FFT, which need the coefficients at known positions. Many systems convert between the two forms. A product of a few dense factors, and a remainder modulo a dense polynomial, are dense, so a computation that starts sparse can become dense.

## Pitfalls

- **Storing zero terms.** If line L7 appends the term with $u = 0$, the list breaks (S): the degree and the equality test become wrong, and $x^{100} - x^{100}$ is stored as a term of degree 100.
- **Zero tests without a normal form.** Over $\mathbb{Z}/p\mathbb{Z}$ stored as plain integers, $7 \ne 0$ is true, and the cancellation of line L7 is missed for $p = 7$. Reduce the coefficients first, or use a coefficient type whose equality is that of $R$.
- **Unsorted input.** ADD is only correct when both lists meet (S). A list built by appending terms in arbitrary order must be sorted and its equal exponents combined first.
- **Exponent overflow.** In MUL, $e + d$ can exceed the word size when the exponents are packed or stored in fixed-size integers. Check the degrees before the product.
- **Dense outputs.** Do not assume that every operation stays sparse. Division, gcd and powers can return polynomials with far more terms than the inputs, and the run time follows the output size.
- **Scanning instead of merging.** Adding two term lists by looking up each term of $b$ in $a$ with a linear search costs $\Theta(st)$; the merge costs $\Theta(s + t)$.

## Implementations

## History

Knuth's Section 2.2.4 uses the addition and multiplication of polynomials stored as circular linked lists of terms as its main example of list processing. Johnson (1974), at Bell Laboratories, described heap-based multiplication and division of sparse polynomials and compared them with the methods then used in the Altran system. Monagan and Pearce (2011) combined heaps with packed exponent vectors in sorted arrays, and Roche (2018) surveys the theory of algorithms for sparse polynomials.

## References
