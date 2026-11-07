---
tag: 1HPPT6
kind: data-structure
slug: subproduct-tree
name: Subproduct tree
aliases:
- product tree
- tree of subproducts
area: algebra/polynomial-arithmetic
level: advanced
summary: Binary tree whose nodes hold products of linear factors; the backbone of fast multipoint evaluation and interpolation.
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of points, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {build: O(M(n) log n), evaluate: O(M(n) log n), combine: O(M(n) log n)}
  space: {extra: O(n log n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [polynomial-multiplication, polynomial-remainder-theorem, binary-tree]
see_also: [fast-multipoint-evaluation, fast-interpolation, multipoint-evaluation, fast-polynomial-division, chinese-remainder-theorem, lagrange-interpolation, segment-tree, fft-polynomial-multiplication]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 10.1, Fast multipoint evaluation (building up and going down the subproduct tree); Section 10.2, Fast interpolation; Section 10.3, Fast Chinese remaindering; Section 8.3 (the properties of M used in the bounds)
  - paper: doi:10.1109/SWAT.1972.5
    title: Robert T. Moenck and Allan Borodin, Fast modular transforms via division, 13th Annual Symposium on Switching and Automata Theory, 1972
    locator: pp. 90 to 96
  - paper: doi:10.1016/S0022-0000(74)80029-2
    title: Allan Borodin and Robert T. Moenck, Fast modular transforms, Journal of Computer and System Sciences 8(3), 1974
    locator: pp. 366 to 386
  - paper: doi:10.1145/800152.804900
    title: Charles M. Fiduccia, Polynomial evaluation via the division algorithm, the fast Fourier transform revisited, STOC 1972
    locator: pp. 88 to 93
  - paper: doi:10.1007/BF01436566
    title: Volker Strassen, Die Berechnungskomplexität von elementarsymmetrischen Funktionen und von Interpolationskoeffizienten, Numerische Mathematik 20(3), 1973
    locator: pp. 238 to 251 (lower bound of order n log n for the elementary symmetric functions)
  - paper: doi:10.1145/860854.860870
    title: Alin Bostan, Grégoire Lecerf and Éric Schost, Tellegen's principle into practice, ISSAC 2003
    locator: pp. 37 to 44 (transposed algorithms with smaller constants for evaluation and interpolation)
---

The subproduct tree of points $u_0, \ldots, u_{n-1}$ in a commutative ring $R$ is a [binary tree](/binary-tree/) whose leaves are the linear polynomials $x - u_j$ and whose every inner node is the product of its two children. The root is $m = \prod_j (x - u_j)$, and each node is the product of $x - u_j$ over a range of consecutive indices. With fast [polynomial multiplication](/polynomial-multiplication/), the tree is built in $O(M(n) \log n)$ ring operations. Going down the tree with remainders evaluates a polynomial at all $n$ points, and going up with cross products computes the sums $\sum_j c_j\, m / (x - u_j)$ that fast interpolation and Chinese remaindering need.

## In plain words

We have many points and want to work with all of them at once. For each point we make the simple polynomial x minus that point. We pair them up and multiply each pair. Then we pair up the products and multiply again, and so on, until one product is left. The result looks like a family tree upside down: the single products are at the bottom, and the product of everything is at the top.

To find the values of a polynomial at all points, we start at the top and divide: the remainder at each child is the remainder of its parent divided by the child. At the bottom, each remainder is a number, the value at that point. Every step works on smaller polynomials, so the total work is close to the cost of a few multiplications.

## The abstract type

A subproduct tree stores a sequence of points $u_0, \ldots, u_{n-1} \in R$, $n \ge 1$, and supports three operations.

- `build(u)`: make the tree. Its root is $m = \prod_j (x - u_j)$.
- `evaluate(f)`: return $f(u_0), \ldots, f(u_{n-1})$ for $f \in R[x]$. This solves [multipoint evaluation](/multipoint-evaluation/).
- `combine(c)`: return $\sum_j c_j\, m / (x - u_j)$ for $c_0, \ldots, c_{n-1} \in R$.

Together they give `interpolate(u, v)`: when $R$ is a field and the $u_j$ are distinct, return the unique $f$ of degree less than $n$ with $f(u_j) = v_j$. The points may repeat for the first three operations.

**Cost model.** We count ring operations at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $R$. $M(n)$ is the number of ring operations to multiply two polynomials of degree less than $n$. As in von zur Gathen and Gerhard, Section 8.3, we assume that $M(n)/n$ is nondecreasing and $M(2n) \le 4 M(n)$; schoolbook, Karatsuba and FFT multiplication all satisfy this.

## Representation

The tree is stored by levels. Level $0$ is the list of the $n$ leaves $x - u_j$. Level $h + 1$ is made from level $h$ by multiplying the nodes $2i$ and $2i + 1$ for each pair; if level $h$ has an odd number of nodes, its last node is copied up unchanged. So level $h$ has $\lceil n / 2^h \rceil$ nodes, the top level is $k = \lceil \log_2 n \rceil$, and

$$T[h][i] = \prod_{i 2^h \le j < \min((i+1) 2^h,\, n)} (x - u_j),$$

a monic polynomial of degree at most $2^h$. Each polynomial is a dense coefficient list, as in the [dense representation](/dense-polynomial-representation/). The degrees on a level add up to $n$, so each level stores at most $n + \lceil n / 2^h \rceil$ coefficients and the whole tree $n (k + 1) + O(n)$, that is $O(n \log n)$. The leading coefficients are all $1$ and could be omitted.

The children of node $(h + 1, i)$ are $(h, 2i)$ and $(h, 2i + 1)$, as in an array [heap](/binary-heap/) or a bottom-up [segment tree](/segment-tree/), so no pointers are needed.

## Operations

```pseudo id=main
BUILD(u[0 .. n − 1])                            ▷ n ≥ 1; R a commutative ring
L1  T[0] ← [x − u[0], x − u[1], …, x − u[n − 1]]
L2  h ← 0
L3  while T[h] has more than one node do
L4      T[h + 1] ← [ ]
L5      for i ← 0, 2, 4, … while i + 1 < |T[h]| do
L6          append T[h][i] · T[h][i + 1] to T[h + 1]
L7      if |T[h]| is odd then append the last node of T[h] to T[h + 1]
L8      h ← h + 1
L9  return T                                    ▷ T[h] = [m], m = ∏ (x − u[j])
```

```pseudo id=eval
EVALUATE(T, f)                                  ▷ T from BUILD, top level k
E1  r[0] ← f rem T[k][0]
E2  for h ← k − 1 down to 0 do
E3      for each i < |T[h]| do r'[i] ← r[⌊i / 2⌋] rem T[h][i]
E4      r ← r'
E5  return r[0], …, r[n − 1]                    ▷ r[j] = f(u[j])
```

```pseudo id=comb
COMBINE(T, c[0 .. n − 1])                       ▷ returns Σ c[j] · m / (x − u[j])
C1  s ← [c[0], …, c[n − 1]]
C2  for h ← 0 to k − 1 do
C3      s' ← [ ]
C4      for i ← 0, 2, 4, … while i + 1 < |T[h]| do append s[i] · T[h][i + 1] + s[i + 1] · T[h][i] to s'
C5      if |T[h]| is odd then append the last entry of s to s'
C6      s ← s'
C7  return s[0]
```

```pseudo id=interp
INTERPOLATE(u[0 .. n − 1], v[0 .. n − 1])       ▷ R a field, the u[j] distinct
I1  T ← BUILD(u); m ← the root of T
I2  w ← EVALUATE(T, m')                          ▷ w[j] = m'(u[j]) = ∏_{i ≠ j} (u[j] − u[i])
I3  return COMBINE(T, [v[0] / w[0], …, v[n − 1] / w[n − 1]])
```

All nodes are monic, so the remainders in EVALUATE need no division in $R$, and BUILD, EVALUATE and COMBINE work over any commutative ring. Only line I3 divides. In line E3, when $\deg r[\lfloor i/2 \rfloor]$ is already less than $\deg T[h][i]$, the remainder is $r[\lfloor i/2 \rfloor]$ itself; this happens for the copied nodes.

## Example

Over $\mathbb{Z}$ with the points $0, 1, 2, 3$:

| Level | Nodes |
|---|---|
| 2 (root) | $x^4 - 6x^3 + 11x^2 - 6x$ |
| 1 | $x^2 - x$, $x^2 - 5x + 6$ |
| 0 | $x$, $x - 1$, $x - 2$, $x - 3$ |

To evaluate $f = x^3 + 2$, line E1 gives $f \operatorname{rem} m = f$, because $\deg f < 4$. At level $1$, $x^3 + 2 = (x + 1)(x^2 - x) + (x + 2)$ and $x^3 + 2 = (x + 5)(x^2 - 5x + 6) + (19x - 28)$. At level $0$, $x + 2$ gives $2$ and $3$ at $x = 0, 1$, and $19x - 28$ gives $10$ and $29$ at $x = 2, 3$. These are $f(0), f(1), f(2), f(3)$.

COMBINE with $c = (1, 1, 1, 1)$ gives $\sum_j m / (x - u_j) = m' = 4x^3 - 18x^2 + 22x - 6$. INTERPOLATE with the values $2, 3, 10, 29$ gives back $x^3 + 2$.

With five points $0, \ldots, 4$ the levels have $5, 3, 2, 1$ nodes: the leaf $x - 4$ is copied up twice and joins the rest at the root, $x^5 - 10x^4 + 35x^3 - 50x^2 + 24x$. The tests check all these values.

## Correctness

By induction on the level, node $i$ of level $h$ is the product of $x - u_j$ over the range $i 2^h \le j < \min((i+1) 2^h, n)$: a pair of adjacent ranges joins into the range of the parent, and a copied last node keeps its range. For EVALUATE, each node divides its parent, so $(f \operatorname{rem} \text{parent}) \operatorname{rem} \text{child} = f \operatorname{rem} \text{child}$, and at a leaf $f \operatorname{rem} (x - u_j) = f(u_j)$ by the [polynomial remainder theorem](/polynomial-remainder-theorem/). For COMBINE, if a node has the ranges $A$ and $B$ below it, then for $j \in A$ the cofactor $m_{A \cup B} / (x - u_j)$ is $(m_A / (x - u_j)) \cdot m_B$, which is what line C4 forms. INTERPOLATE then computes the Lagrange form. The full proof is below.

## Complexity

All bounds here are proved in the cost model above, with the assumptions on $M$.

- **Build.** Level $h + 1$ is formed by products of two monic polynomials of degree at most $d = 2^h$, whose larger degrees add up to at most $n$. A product of two polynomials of degree at most $d$ costs at most $M(2d) \le (d / n) M(2n) \le 4 (d / n) M(n)$ by the two assumptions on $M$. So a level costs at most $4 M(n)$, and the $\lceil \log_2 n \rceil$ levels cost $O(M(n) \log n)$. When $n$ is a power of $2$, all products at level $h + 1$ are of two monic polynomials of degree $d = 2^h$. Writing them as $(x^d + a)(x^d + b) = x^{2d} + (a + b) x^d + a b$ with $\deg a, \deg b < d$ costs $M(d) + O(d)$, and $M(d) \le (d / n) M(n)$. The $n / (2d)$ products then cost $M(n)/2 + O(n)$, and the build costs at most $\frac{1}{2} M(n) \log_2 n + O(n \log n)$.
- **Evaluate.** If $\deg f < n$, each level divides polynomials of degree less than $2 d$ by monic polynomials of degree $d$, with degrees adding up to $O(n)$. With [fast division](/fast-polynomial-division/), a division costs $O(M(d))$, so a level costs $O(M(n))$ and the descent $O(M(n) \log n)$. A larger $f$ costs one more division by $m$ at the start.
- **Combine.** Each level makes two products and one addition per pair, of degrees at most $2^h$, so the same argument as for the build gives $O(M(n) \log n)$.
- **Interpolate.** One build, one derivative ($O(n)$), one evaluation, $n$ divisions in $R$ and one combine: $O(M(n) \log n)$ field operations.
- **Space.** The tree has $O(n \log n)$ coefficients. One level of remainders or partial sums has $O(n)$.

With FFT multiplication, $M(n) = O(n \log n \log \log n)$, so the operations cost $O(n \log^2 n \log \log n)$. The implementation below uses schoolbook products and divisions, so for it $M(n) = O(n^2)$ and each operation costs $O(n^2)$.

**Lower bound.** The root alone holds, up to sign, the $n$ elementary symmetric functions of $u_0, \ldots, u_{n-1}$. Strassen (1973) proved that computing them needs a number of nonscalar multiplications of order $n \log n$; in that model, multiplications by fixed constants and additions are free. Over an infinite field, a product of two polynomials of degree less than $d$ needs only $2d - 1$ nonscalar multiplications: evaluate both at $2d - 1$ fixed points, multiply the values, and interpolate, where the evaluation and interpolation are linear maps with fixed coefficients. So the build uses $O(n \log n)$ nonscalar multiplications, and Strassen's bound is tight in that model. In the algebraic model counted here, the best known bound is $O(M(n) \log n)$.

**Observed in practice.** The constants matter. Bostan, Lecerf and Schost (2003) use the transposition principle to reduce the constant factors of evaluation and interpolation, and they report the effect with timings.

## Variants

- **General moduli.** The leaves can be any monic polynomials $m_1, \ldots, m_r$ instead of linear ones. Then the descent computes $f \operatorname{rem} m_i$ for all $i$, and the combination step gives fast Chinese remaindering. Von zur Gathen and Gerhard, Section 10.3, treat this case.
- **Integer product trees.** The same tree for integers $m_1, \ldots, m_n$ gives fast multi-modular reduction and the [Chinese remainder theorem](/chinese-remainder-theorem/) for many moduli.
- **Transposed algorithms.** Bostan, Lecerf and Schost (2003) derive faster evaluation and interpolation from the transposes of these linear maps, by the transposition principle.
- **Monic products.** As in the complexity proof, the product of two monic nodes of equal degree needs only one multiplication of size $d$; implementations also drop the stored leading $1$.
- **Storing only a few levels.** To save memory, keep only the top levels and recompute the lower ones when the descent reaches them.

## When to use it

Use the subproduct tree when many operations involve the same set of points: evaluating many polynomials, interpolating many value vectors, or Chinese remaindering many residue vectors, so that the tree is built once. It pays only with fast multiplication and fast division. With schoolbook arithmetic, [Horner's rule](/horner-rule/) at each point costs $O(n^2)$ too and is simpler, and Newton or Lagrange interpolation costs $O(n^2)$. When the points are roots of unity in a ring that has them, the [FFT](/fast-fourier-transform/) evaluates in $O(n \log n)$ without a tree.

## Pitfalls

- **Unbalanced splits.** A tree that peels off one factor at a time is a path of depth $n$; it costs $\Theta(n M(n))$, not $O(M(n) \log n)$. Keep the tree balanced.
- **Odd levels.** With $n$ not a power of $2$, a level can have an odd number of nodes. Copy the last node up and copy its remainder down; do not pair it with a missing node.
- **Repeated points in interpolation.** If $u_i = u_j$ for some $i \ne j$, then $m'(u_i) = 0$ and line I3 divides by zero. Over a ring that is not a field, $m'(u_j)$ must be a unit.
- **Large inputs to EVALUATE.** The bounds assume $\deg f < n$. For larger $f$, reduce modulo $m$ first, or split $f$ into blocks of $n$ coefficients.
- **Recursion depth.** A recursive build on the halves has depth $\lceil \log_2 n \rceil$, which is safe; the level-by-level loop here avoids recursion altogether.

## Implementations

## History

Fiduccia (1972) and Moenck and Borodin (1972) showed that evaluation at $n$ points and interpolation can be done with $O(M(n) \log n)$ operations by repeated division with remainder along a balanced product tree; Borodin and Moenck gave the journal version in 1974. Strassen (1973) proved the matching lower bound of order $n \log n$ for the elementary symmetric functions and for the coefficients of the interpolating polynomial. Von zur Gathen and Gerhard present the subproduct tree in Chapter 10 of Modern Computer Algebra, and Bostan, Lecerf and Schost (2003) lowered the constants with transposed algorithms.

## References
