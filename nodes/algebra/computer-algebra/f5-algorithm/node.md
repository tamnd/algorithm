---
tag: 2QB464
kind: algorithm
slug: f5-algorithm
name: F5 algorithm
aliases:
- Faugère F5
- signature-based Gröbner algorithm
- F5
area: algebra/computer-algebra
level: advanced
summary: Signature-based Gröbner algorithm that avoids reducing many useless syzygy pairs.
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of variables, d: the largest degree of an input polynomial, D: the degree of regularity of a regular sequence, N: the number of monomials of degree at most D, w: the matrix multiplication exponent}
  time: {worst: d^(2^O(n)), best: O(N^w)}
  space: {extra: O(N^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [buchberger-algorithm, syzygy, s-polynomial, monomial-ordering]
see_also: [f4-algorithm, gebauer-moller-criteria, buchberger-criteria, groebner-basis-computation, hilbert-series, macaulay-matrix, fglm-algorithm, syzygy]
sources:
  - paper: doi:10.1145/780506.780516
    title: Jean-Charles Faugère, A new efficient algorithm for computing Gröbner bases without reduction to zero (F5), Proceedings of ISSAC 2002, ACM, pages 75 to 83
    locator: the incremental algorithm with signatures, the F5 criterion, the rewritten criterion and the theorem that regular sequences give no reduction to zero
  - paper: doi:10.1016/j.jsc.2016.07.031
    title: Christian Eder and Jean-Charles Faugère, A survey on signature-based algorithms for computing Gröbner bases, Journal of Symbolic Computation 80, 719-784, 2017
    locator: the signature framework, the syzygy and rewrite criteria, the uniqueness of leading monomials per signature and the termination proofs
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 10, Section 4 (signature-based algorithms and F5, with the signature version of Buchberger's criterion)
  - paper: doi:10.1016/j.jsc.2014.09.025
    title: Magali Bardet, Jean-Charles Faugère and Bruno Salvy, On the complexity of the F5 Gröbner basis algorithm, Journal of Symbolic Computation 70, 49-70, 2015
    locator: the cost of the matrix version for regular and semi-regular sequences in terms of the degree of regularity
  - paper: "Shuhong Gao, Frank Volny IV and Mingsheng Wang, A new framework for computing Gröbner bases, Mathematics of Computation 85(297), 449-465, 2016"
    locator: the GVW algorithm, the cover criterion and a termination proof for signature-based algorithms
---

F5 is a signature-based algorithm for computing Gröbner bases. It attaches to every polynomial it computes a *signature*, the leading term of a record of how the polynomial was built from the input, and uses these signatures to recognize in advance most of the S-polynomials that would reduce to zero, the useless work that dominates [Buchberger's algorithm](/buchberger-algorithm/). For a regular sequence it performs no reduction to zero at all. Faugère introduced it in 2002 as a successor of [F4](/f4-algorithm/); its correctness and termination for all inputs were settled later, and the signature-based family it started, with variants such as GVW and SB, is now the basis of the fastest Gröbner basis software for hard systems.

## In plain words

Buchberger's algorithm checks many pairs of polynomials, and most checks come out empty. An empty check means that the pair was a combination of things already known. F5 keeps track, for each polynomial, of where it came from: which input polynomial it started from, and with which largest multiplier. This tag is its signature.

Two simple rules on signatures predict that a check will come out empty. One rule uses the obvious relations between the inputs, like "f times g minus g times f is zero". The other rule says that two pairs with the same tag do the same work, so only one is needed. With these rules, and by doing the pairs in order of their tags, F5 skips almost all empty checks.

## The problem

Let $K$ be a field and $R = K[x_1, \ldots, x_n]$, with a monomial order $>$ (lex, grlex or grevlex, $x_1 > \cdots > x_n$). For $f \ne 0$, $\operatorname{LT}(f)$, $\operatorname{LM}(f)$ and $\operatorname{LC}(f)$ are its leading term, monomial and coefficient. Write $d$ for the largest degree of an input, $t$ for the number of terms and $M(d)$ for the cost of polynomial multiplication; the analysis below uses the degree of regularity instead.

**Input:** $f_1, \ldots, f_s \in R$ and $>$. **Output:** the [reduced Gröbner basis](/reduced-groebner-basis/) of $I = \langle f_1, \ldots, f_s \rangle$.

**Signatures.** Let $R^s$ have basis $e_1, \ldots, e_s$ and send $\alpha$ to $\bar\alpha = \sum_i \alpha_i f_i$. Order module monomials *position over term*: $u e_i < v e_j$ if $i < j$, or if $i = j$ and $u < v$. The signature of a polynomial $p = \bar\alpha$ is the largest module monomial of $\alpha$; the algorithm stores only this, never $\alpha$. A reduction of $p$ by $t g$ is *regular* if $t \operatorname{sig}(g) < \operatorname{sig}(p)$, so that it does not change the signature. A *syzygy* is an $\alpha$ with $\bar\alpha = 0$, and its leading module monomial is a syzygy signature. The *principal syzygies* $f_j e_i - f_i e_j$ have signature $\operatorname{LM}(f_j) e_i$ for $j < i$, and more generally $\operatorname{LM}(g) e_i$ for any $g$ in the ideal of $f_1, \ldots, f_{i-1}$; see [syzygy](/syzygy/).

## The algorithm

```pseudo id=main
F5(F, >)                            ▷ F = (f_1, ..., f_s); signatures ordered position over term
L1  B ← [], Syz ← [], Q ← [(e_i, f_i) for i = 1, ..., s]
L2  while Q ≠ ∅ do
L3      (σ, p) ← the entry of Q with the smallest signature; skip it if σ was already handled
L4      if σ = e_i then add LM(g) e_i to Syz for every g ∈ B with signature index < i
L5      if some τ ∈ Syz divides σ then continue                  ▷ F5 (syzygy) criterion
L6      r ← regular reduction of p by B
L7      if r = 0 then add σ to Syz; continue                     ▷ a reduction to zero, recorded
L8      if r = t g with t sig(g) = σ in its leading term, for some g ∈ B then continue   ▷ rewrite
L9      for g ∈ B: put the S-pair of r and g in Q, labeled with the larger of its two signatures, unless they are equal
L10     append (σ, r) to B
L11 return the reduced basis of the polynomials of B
```

Line L3 is the second, *rewrite*, criterion in its simplest form: of all candidates with the same signature, only one is reduced. Line L8 discards a result whose leading term and signature are both a multiple $t$ of those of an existing element; such an element is called *singular top-reducible* and adds nothing new. Line L4 uses the order of processing: by the time the first signature of index $i$ is reached, the elements of index below $i$ form a Gröbner basis of $\langle f_1, \ldots, f_{i-1} \rangle$, so their leading monomials give principal syzygy signatures. Faugère's 2002 formulation, with its own rewrite rule based on the order of creation, works incrementally in exactly this way; the version here follows the modern signature framework of the Eder and Faugère survey.

## Example

Let $I = \langle x^2 + y^2 - 4,\ xy - 1 \rangle \subseteq \mathbb{Q}[x, y]$ with grevlex and $x > y$. The trace, from the implementation:

| step | $\sigma$ | entry | outcome |
|---|---|---|---|
| 1 | $e_1$ | $f_1 = x^2 + y^2 - 4$ | irreducible; $g_1 = f_1$ with signature $e_1$ |
| 2 | $e_2$ | $f_2 = xy - 1$ | line L4 adds $x^2 e_2$ to Syz; irreducible; $g_2 = f_2$; the S-pair with $g_1$ has signatures $x e_2$ and $y e_1$, so its label is $x e_2$ |
| 3 | $x e_2$ | $x g_2 - y g_1 = -y^3 - x + 4y$ | irreducible; $g_3 = y^3 + x - 4y$ (up to sign) with signature $x e_2$; S-pairs labeled $x^3 e_2$ (with $g_1$) and $x^2 e_2$ (with $g_2$) |
| 4 | $x^2 e_2$ | S-pair of $g_3, g_2$ | divisible by $x^2 e_2 \in$ Syz: skipped at line L5 |
| 5 | $x^3 e_2$ | S-pair of $g_3, g_1$ | divisible by $x^2 e_2$: skipped at line L5 |

The basis is $\{xy - 1,\ x^2 + y^2 - 4,\ y^3 + x - 4y\}$, reached with three reductions and no reduction to zero. Buchberger's algorithm that reduces every pair performs 3 S-polynomial reductions, 2 of them to zero, and with the [Gebauer-Möller criteria](/gebauer-moller-criteria/) it still performs 2, one of them to zero. The skipped S-pair of step 4 is the one those criteria cannot remove: its S-polynomial is a consequence of the principal syzygy $f_1 e_2 - f_2 e_1$, which the signature reveals.

The tests check on 40 random homogeneous systems, whose regularity is confirmed independently through the [Hilbert series](/hilbert-series/), that no reduction to zero occurs.

## Correctness

The full proof is in the correctness file. Every stored polynomial is the image of a module element with the stored signature, and the entries of Syz are syzygy signatures, by construction. Signatures are handled in strictly increasing order. The key lemma: if the current basis is a *signature Gröbner basis* below $\sigma$, meaning every element of signature below $\sigma$ has a representation that respects both signatures and leading monomials, then all regularly reduced polynomials with signature $\sigma$ have the same leading monomial. This justifies keeping one candidate per signature and discarding singular top-reducible ones. The signature version of Buchberger's criterion then shows, by induction over signatures, that once every non-discarded S-pair has been handled, the basis is a signature Gröbner basis, hence a Gröbner basis. Termination follows from Dickson's lemma applied to the pairs (leading monomial, signature monomial) and the same uniqueness lemma.

## Complexity

The cost model is operations in $K$ on a Blum-Shub-Smale machine; over $\mathbb{Q}$ the bit cost also depends on coefficient growth, not bounded here.

- **Worst case.** F5 computes a Gröbner basis, so it inherits the doubly exponential worst case: Mayr and Meyer (1982) give ideals that need degree $d^{2^{\Theta(n)}}$, and the time is $d^{2^{O(n)}}$ in general.
- **Regular sequences, proved.** For a homogeneous regular sequence, every syzygy is generated by the principal ones, so the F5 criterion removes every pair that would reduce to zero (Faugère 2002). The matrix version of F5 in grevlex costs $O(N^{\omega})$ operations, with $N = \binom{n + D}{n}$ the number of monomials of degree at most $D$, where $D = \sum_i (d_i - 1) + 1$ is the degree of regularity for $n$ equations in $n$ variables (Bardet, Faugère and Salvy 2015). For semi-regular overdetermined systems the same bound holds with the corresponding degree of regularity, which is how the cost of algebraic attacks on cryptosystems is estimated.
- **Zero-dimensional ideals** in general cost $d^{O(n)}$ operations (Lakshman 1991), single exponential.
- **Overhead.** Signature checks cost only monomial comparisons. The price of the criteria is that F5 may keep more, and less reduced, basis elements than Buchberger's algorithm, since some reductions are forbidden by signatures; the reduced basis is computed at the end.
- **Space.** In the matrix version, the Macaulay matrices in degree $D$ dominate, $O(N^2)$ field elements in dense form.

## Properties

- **No reduction to zero on regular sequences**, and few on most others; each reduction to zero that does occur yields a new syzygy signature that prunes later pairs.
- **Incremental.** With position over term, F5 computes Gröbner bases of $\langle f_1 \rangle$, $\langle f_1, f_2 \rangle$, and so on, one after another.
- **Exact and deterministic**, with the same output as any other Gröbner basis algorithm after reduction.
- **Order-sensitive.** The module order matters for efficiency but not for correctness. Position over term is the order of F5; term over position and degree-based orders give other variants.

## Variants and improvements

- **Matrix-F5.** The linear algebra version builds Macaulay matrices degree by degree and removes the rows whose signatures are syzygy signatures before elimination; it is the version analyzed by Bardet, Faugère and Salvy and is close to [F4](/f4-algorithm/) in practice.
- **F5C and F5 with improved rewriting** (Eder and Perry, among others) reduce the intermediate bases between the incremental steps and correct some cases of the original description.
- **GVW** (Gao, Volny and Wang 2016) uses a cover criterion; together with SB of Roune and Stillman, it is among the simplest signature-based algorithms with complete proofs.
- **Rewrite orders.** Eder and Faugère show that any rewrite order compatible with the signatures gives a correct algorithm; the ratio order of Arri and Perry and the creation order of F5 are two choices.
- **Termination.** The original paper's argument for termination was incomplete; proofs for general input were given later for the variants above, and the version here terminates by the argument in the correctness file.

## When to use it

Use F5 or another signature-based algorithm when many reductions to zero are expected: for dense, regular or semi-regular systems such as those of algebraic cryptanalysis and many zero-dimensional systems. For small or structured systems with few useless pairs, F4 with the [Gebauer-Möller criteria](/gebauer-moller-criteria/) is often as fast and simpler. For a lex basis of a zero-dimensional system, compute grevlex with F4 or F5 and convert with [FGLM](/fglm-algorithm/).

## Pitfalls

- **Processing order.** Correctness depends on handling signatures in increasing order. A priority queue sorted by an order that is not the module order, for example by degree only, breaks the uniqueness lemma.
- **Regular reductions only.** Reducing $p$ by $t g$ with $t \operatorname{sig}(g) \ge \operatorname{sig}(p)$ changes the signature and invalidates the labels. Such reductions must be skipped, which is why intermediate elements are often not fully reduced.
- **Principal syzygies need a Gröbner basis.** The F5 criterion with $\operatorname{LM}(g) e_i$ is valid for any $g$ in the earlier ideal, but it is complete only when $g$ runs over a Gröbner basis of $\langle f_1, \ldots, f_{i-1} \rangle$, which the order of processing guarantees.
- **Rewrite rules.** Discarding a candidate because another one with a dividing signature exists is safe only with a consistent rewrite order; ad hoc rules found in some early implementations could remove needed pairs.
- **Input order.** The efficiency depends on the order of the inputs, because the principal syzygies are taken against earlier ones. Sorting by degree is the usual choice.

## Implementations

## History

The use of syzygies to avoid useless pairs goes back to Möller, Mora and Traverso (1992), who computed with module elements. Faugère's F5 (2002) showed that only the leading term of the module element, the signature, is needed, and that for regular sequences no reduction to zero occurs. F5 solved the first HFE challenge of the HFE public key cryptosystem in 2002, which made its reputation. Later work by Eder, Perry, Arri, Gao, Volny, Wang, Roune and Stillman clarified and simplified the criteria and gave complete proofs, summarized in the survey of Eder and Faugère (2017).

## References
