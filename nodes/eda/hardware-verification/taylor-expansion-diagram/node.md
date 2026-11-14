---
tag: B790DF
kind: data-structure
slug: taylor-expansion-diagram
name: Taylor expansion diagram
aliases:
- TED
area: eda/hardware-verification
level: advanced
summary: Ciesielski, Kalla and Askar's canonical graph of a polynomial over word-level variables built by Taylor expansion, used to verify arithmetic datapaths.
model: word-ram
complexity:
  vars: {f: the number of nodes of the first argument, g: the number of nodes of the second argument, D: the largest degree of one variable}
  time: {mk: O(D) expected, add: O(f g D) expected, evaluate: O(f D)}
  space: {nodes: O(f D)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 2001
  people: [Maciej Ciesielski, Priyank Kalla]
  note: Ciesielski, Kalla and coauthors introduced TEDs in 2001 and 2002 to verify register-transfer and data flow designs at the word level, and gave the journal treatment with Askar in 2006.
prereqs: [binary-moment-diagram, polynomial-ring, reduced-ordered-bdd]
see_also: [binary-moment-diagram, bdd-canonicity, algebraic-decision-diagram, kronecker-functional-decision-diagram, algebraic-arithmetic-circuit-verification, polynomial-identity-testing, horner-rule, polynomial-ring]
sources:
  - paper: doi:10.1109/TC.2006.153
    title: M. Ciesielski, P. Kalla and S. Askar, Taylor expansion diagrams, a canonical representation for verification of data flow designs, IEEE Transactions on Computers 55(9), 1188 to 1201, 2006
    locator: the decomposition of a polynomial by the Taylor series in one variable at a time, the reduction and normalization rules, canonicity for a fixed variable order, the operations, and the use for equivalence of data flow designs
  - paper: doi:10.1109/DATE.2002.998286
    title: M. J. Ciesielski, P. Kalla, Z. Zeng and B. Rouzeyre, Taylor expansion diagrams, a compact, canonical representation with applications to symbolic verification, Design, Automation and Test in Europe (DATE 2002), 285 to 289, 2002
    locator: TEDs as a compact canonical form of polynomials and their use in symbolic verification
  - paper: doi:10.1109/HLDVT.2001.972810
    title: M. Ciesielski, P. Kalla, Z. Zeng and B. Rouzeyre, Taylor expansion diagrams, a new representation for RTL verification, IEEE International High-Level Design Validation and Test Workshop (HLDVT 2001), 70 to 75, 2001
    locator: the first presentation of TEDs for register-transfer level verification
---

A Taylor expansion diagram (TED) is a canonical graph of a multivariate polynomial. Ciesielski, Kalla and their coauthors introduced it in 2001 to compare arithmetic datapaths at the word level. Each variable stands for a whole data word and takes integer or real values, not bits. For the top variable $x$ in a fixed order, a node expands its polynomial $f$ in the Taylor series at $x = 0$:

$$f = f(0) + x \, f'(0) + \tfrac{1}{2} x^2 f''(0) + \cdots + \tfrac{1}{d!} x^d f^{(d)}(0),$$

where the derivatives are by $x$ and the coefficients are polynomials in the later variables. A polynomial has a finite series, so the node has one child per power $x^0, \ldots, x^d$. With the rules "drop a node that does not depend on its variable" and "merge equal nodes", the diagram is canonical: two expressions, such as $A \cdot B + A \cdot C$ and $A \cdot (B + C)$, give the same node exactly when they are the same polynomial. A TED of a 0-1 variable needs only the powers 0 and 1, since $x^2 = x$, and then the node is the moment node of a [binary moment diagram](/binary-moment-diagram/). The TED carries that idea to word variables.

## In plain words

Write a polynomial in a fixed order of its variables. Take the first variable, say $a$, and group the terms by the power of $a$: the terms without $a$, the terms with $a$, those with $a^2$, and so on. Each group, with its power of $a$ taken out, is a smaller polynomial in the other variables. Do the same for each of them with the next variable, and so on until only numbers are left.

Draw this as a graph. A node for $a$ has an arrow to each group. Equal groups are stored only once, and a variable that does not occur is skipped. Then every polynomial has exactly one graph. To test whether two circuits compute the same polynomial, build both graphs and compare the two top nodes.

## The abstract type

The variables are $x_1, \ldots, x_n$ in this order, and the coefficients are rational numbers. A node $u$ stands for a polynomial $f_u \in \mathbb{Q}[x_1, \ldots, x_n]$.

| operation | result |
|---|---|
| CONST$(q)$ | the constant polynomial $q$ |
| MK$(v, c_0, \ldots, c_d)$ | the polynomial $\sum_{k=0}^{d} x_v^k f_{c_k}$ |
| ADD$(f, g)$ | $f + g$ |
| MUL$(f, g)$ | $f \cdot g$ |
| EVALUATE$(f, p)$ | the value of $f$ at the point $p$ |
| BUILD$(e)$ | the node of an expression $e$ made of variables, numbers, $+$, $-$, $\times$ and powers |
| EQUAL$(f, g)$ | whether $f = g$, by comparing ids |

For a polynomial $f$ in $x_v, \ldots, x_n$ there are unique polynomials $f_0, \ldots, f_d$ in $x_{v+1}, \ldots, x_n$, with $f_d \ne 0$ unless $d = 0$, such that $f = \sum_k x_v^k f_k$. They are the Taylor coefficients: $f_k = \frac{1}{k!} \partial^k f / \partial x_v^k$ at $x_v = 0$. Division by $k!$ needs a field of characteristic 0, such as $\mathbb{Q}$ or $\mathbb{R}$.

## Representation

A sink $(n + 1, q)$ stores one rational number $q$. An inner node $(v, c_0, \ldots, c_d)$ stores the level $v$ and $d + 1$ children on later levels, where $c_k$ is the node of the $k$-th Taylor coefficient. A unique table maps each key to its node, and MK keeps three rules:

- **Trailing zeros.** A last child that is the sink 0 is dropped, since $x_v^d \cdot 0$ adds nothing.
- **No dependence.** If only $c_0$ is left, MK returns $c_0$, since $f = f_0$ does not depend on $x_v$.
- **Merging.** If the key is stored, MK returns the stored node.

So every inner node has at least two children and a nonzero last child. Unfolded, a TED lists the monomials of $f$: the path that takes child $k_v$ at each tested variable ends at the coefficient of $\prod_v x_v^{k_v}$, and a skipped variable has power 0.

## Operations

For a node $u$ and a level $v$ at most the level of $u$, let $\mathrm{coef}(u, v)$ be $(c_0, \ldots, c_d)$ if $u = (v, c_0, \ldots, c_d)$, and $(u)$ if $u$ is on a later level.

```pseudo id=main
MK(v, c_0, ..., c_d)
L1  while d ≥ 1 and c_d is the sink 0 do d ← d − 1           ▷ trailing zeros
L2  if d = 0 then return c_0                                  ▷ no dependence on x_v
L3  if U holds (v, c_0, ..., c_d) then return it              ▷ merging
L4  otherwise make a new node u, store U[v, c_0, ..., c_d] ← u, and return u

ADD(f, g)            ▷ ADD(0, g) = g, ADD(f, 0) = f; results are cached under {f, g}
L5  if f and g are sinks then return CONST(q_f + q_g)
L6  v ← min(level(f), level(g)); a ← coef(f, v); b ← coef(g, v); pad the shorter with 0; return MK(v, ADD(a_k, b_k) for each k)

MUL(f, g)            ▷ 0 and 1 are shortcuts; results are cached under {f, g}
L7  if f and g are sinks then return CONST(q_f · q_g)
L8  v, a, b as in ADD; for k ← 0 to d_a + d_b do c_k ← the ADD of MUL(a_i, b_j) over all i + j = k
L9  return MK(v, c_0, ..., c_{d_a + d_b})

EVALUATE(u, p)       ▷ one pass over the nodes reachable from u, children first
L10 val[w] ← q for a sink (n + 1, q); val[w] ← Σ_k val[c_k] · p_v^k by Horner's rule for w = (v, c_0, ..., c_d); return val[u]

BUILD(e)
L11 a variable x gives MK(x, 0, 1), a number q gives CONST(q); +, −, × and powers recurse with ADD, ADD and MUL by −1, and MUL
```

ADD uses that the Taylor coefficients of a sum are the sums of the coefficients. MUL multiplies two polynomials in $x_v$ whose coefficients are polynomials in the later variables:

$$\Bigl(\sum_i x_v^i a_i\Bigr)\Bigl(\sum_j x_v^j b_j\Bigr) = \sum_k x_v^k \sum_{i + j = k} a_i b_j.$$

## Example

**The square of a sum.** Take the order $a, b$ and $f = (a + b)^2$. BUILD gives the node of $a + b$, namely $(a, (b, 0, 1), 1)$, and MUL of it with itself. Line L8 takes $v = a$, $\mathrm{coef} = ((b, 0, 1), 1)$ for both, and computes

| $k$ | $\sum_{i + j = k} a_i b_j$ | Taylor coefficient of $f$ by $a$ | node |
|---|---|---|---|
| 0 | $b \cdot b$ | $f(0, b) = b^2$ | $(b, 0, 0, 1)$ |
| 1 | $b \cdot 1 + 1 \cdot b$ | $\partial f / \partial a$ at $a = 0$: $2b$ | $(b, 0, 2)$ |
| 2 | $1 \cdot 1$ | $\frac{1}{2} \partial^2 f / \partial a^2 = 1$ | the sink 1 |

The root is $(a, (b, 0, 0, 1), (b, 0, 2), 1)$: 3 inner nodes and the sinks 0, 1 and 2, so 6 nodes. BUILD of the other form $a \cdot a + 2 \cdot a \cdot b + b \cdot b$ goes through other calls and returns the same root id.

**Rational coefficients.** With one variable, $(x + \frac{1}{2})(x - \frac{1}{3})$ and $x^2 + \frac{1}{6} x - \frac{1}{6}$ both give the node $(x, -\frac{1}{6}, \frac{1}{6}, 1)$. The children are $f(0) = -\frac{1}{6}$, $f'(0) = \frac{1}{6}$ and $\frac{1}{2} f''(0) = 1$.

**A datapath rewrite.** With the order $A, B, C$, the designs $A \cdot B + A \cdot C$ and $A \cdot (B + C)$ give the same node $(A, 0, (B, C, 1))$, where $(B, C, 1)$ is $B + C$. A bit-level check of the two would compare circuits with different multipliers.

**Measured sizes**, with the code of this page:

| polynomial | inner nodes | all nodes | monomials |
|---|---|---|---|
| $(a + b)^k$, $k = 1, \ldots, 6$ | $k + 1$ | 4, 6, 7, 9, 10, 12 | $k + 1$ |
| $(x_1 + \cdots + x_n)^2$, $n = 2, \ldots, 6$ | $2n - 1$ | $2n + 2$ | $n(n + 1)/2$ |

The square of a sum of $n$ words has a linear number of nodes, while it has a quadratic number of monomials.

## Correctness

**Canonicity.** The Taylor coefficients of a polynomial by $x_v$ are unique, because $\mathbb{Q}[x_v, \ldots, x_n]$ is the ring of polynomials in $x_v$ over $\mathbb{Q}[x_{v+1}, \ldots, x_n]$. And $f$ does not depend on $x_v$ exactly when all coefficients after the 0-th are zero. With these two facts, the induction of [BDD canonicity](/bdd-canonicity/) goes through. Every inner node depends on its variable, by the trailing-zeros rule. Two nodes with the same polynomial on the same level have the same coefficients, hence by induction the same children, and the merging rule makes them one node. So over $\mathbb{Q}$, two polynomials are equal exactly when their nodes are the same. Since $\mathbb{Q}$ is infinite, this is also equality as functions. **ADD** and **MUL** are correct by the identities above, and **EVALUATE** by Horner's rule. The full proofs are in [the proof file](proofs/correctness.md).

The tests check canonicity on 300 random expressions with fixed seeds: each expression and a second form of the same polynomial, with the monomials and factors in random order, give the same node, and a changed coefficient gives another node. On 400 more expressions, two nodes are equal exactly when the polynomials, expanded independently, are equal. The tests also check that the $k$-th child of the root is $\frac{1}{k!} \partial^k f / \partial x_v^k$ at $x_v = 0$, that EVALUATE agrees with the expanded polynomial at random rational points, and that the store stays reduced.

## Complexity

| operation | time | notes |
|---|---|---|
| MK, CONST | $O(D)$ expected | one hash of up to $D + 1$ children |
| ADD$(f, g)$ | $O(\lvert f \rvert \cdot \lvert g \rvert \cdot D)$ expected | each pair of nodes once |
| MUL$(f, g)$ | no general polynomial bound is given here | each pair once, but each step runs ADD on intermediate results |
| EVALUATE | $O(\lvert f \rvert \cdot D)$ | all reachable nodes |
| space | $O(\lvert f \rvert \cdot D)$ | up to $D + 1$ children per node |

$D$ is the largest degree of one variable. The times count rational operations as $O(1)$. Coefficients of products can grow large, so exact arithmetic costs more for high degrees and many factors.

## Variants

- **Normalized weighted TEDs.** Ciesielski, Kalla and Askar put multiplicative weights on the edges and normalize them, so that common factors such as the $2^i$ of a bit vector or a constant multiple move into the weights. The rules are chosen so that the normalized form stays canonical.
- **Bit-level variables.** A variable that takes only 0 and 1 obeys $x^2 = x$, so its node has the children for $x^0$ and $x^1$ only. Such a node is a moment node of a [BMD](/binary-moment-diagram/), so a TED over 0-1 variables is a BMD, and a word $X = \sum_i 2^i x_i$ links the word level to the bits.
- **Other bases.** An [ADD](/algebraic-decision-diagram/) uses the Shannon expansion for functions of bits to numbers, and [KFDDs](/kronecker-functional-decision-diagram/) choose an expansion per variable. TEDs are the polynomial case with a Taylor basis per word variable.
- **Polynomials modulo $2^w$.** A real datapath computes modulo $2^w$, where different polynomials can give the same function. A TED over $\mathbb{Q}$ then proves equivalence only when the two polynomials are equal. The canonical forms of polynomial functions modulo $2^w$ need extra rules.

## When to use it

Use a TED to check that two arithmetic datapaths, given as expressions over words, compute the same polynomial: rewrites of a filter, a transform, a sum of products, or a high-level synthesis step. The cost depends on the number of words and their degrees, not on the width of the words. For control logic, comparisons and other bit-level functions, BDDs and SAT are the right tools. For a gate-level multiplier, the structure is not a word-level expression, and the [algebraic method](/algebraic-arithmetic-circuit-verification/) that rewrites the gate polynomials is the usual choice. For one-off identity tests, [random evaluation](/polynomial-identity-testing/) at a few points is cheaper but gives no canonical form.

## Pitfalls

- **Field of characteristic 0.** The Taylor coefficients divide by $k!$, and canonicity uses unique coefficients over a field. Over the integers modulo $2^w$ the same diagram is still a correct representation of a polynomial, but equal functions need not have equal polynomials, so different nodes do not prove that two designs differ.
- **The variable order.** The diagram is canonical only for a fixed order, and its size depends on the order. Both sides of a check must use the same manager and the same order.
- **Evaluation visits all nodes.** As in a BMD, the value is a sum over many paths, not one path.
- **Big numbers.** Coefficients are exact rationals. Fixed-width numbers overflow for large products.
- **Mixed bits and words.** A variable that is really a bit must use $x^2 = x$. Treating it as a word variable makes $x^2$ and $x$ different nodes, and two equal bit-level designs look different.

## Implementations

## History

Ciesielski, Kalla, Zeng and Rouzeyre presented TEDs for register-transfer level verification at the High-Level Design Validation and Test Workshop in 2001 and at DATE 2002. Ciesielski, Kalla and Askar gave the journal paper in the IEEE Transactions on Computers in 2006, with normalized weights and the use for data flow designs. TEDs extend the word-level line of decision diagrams that started with the BMDs of Bryant and Chen (1995), which handle words through their bits.

## References
