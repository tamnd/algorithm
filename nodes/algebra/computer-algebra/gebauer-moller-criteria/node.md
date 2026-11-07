---
tag: RTDJFD
kind: technique
slug: gebauer-moller-criteria
name: Gebauer-Möller criteria
aliases:
- Gebauer-Möller installation
- Gebauer-Möller update
- criteria B, F and M
area: algebra/computer-algebra
level: advanced
summary: Pair-selection rules that remove redundant critical pairs in Buchberger's algorithm.
prereqs: [buchberger-criteria, buchberger-algorithm]
see_also: [buchberger-criteria, s-polynomial, syzygy, f4-algorithm, f5-algorithm, sugar-strategy, groebner-basis-computation]
sources:
  - paper: doi:10.1016/S0747-7171(88)80048-8
    title: Rüdiger Gebauer and H. Michael Möller, On an installation of Buchberger's algorithm, Journal of Symbolic Computation 6(2-3), 275-286, 1988
    locator: the procedure UPDATE with the criteria B, F and M, and the proof that applying them in this order removes only pairs that are not needed
  - book: isbn:9780387979715
    title: Thomas Becker and Volker Weispfenning (with Heinz Kredel), Gröbner Bases, A Computational Approach to Commutative Algebra, Graduate Texts in Mathematics 141, Springer, 1993
    locator: Chapter 5, Section 5 (the improved Buchberger algorithm and the procedure UPDATE in the form of Gebauer and Möller)
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 10 (improvements on Buchberger's algorithm, the two criteria and the selection of pairs)
  - paper: "Bruno Buchberger, A criterion for detecting unnecessary reductions in the construction of Gröbner bases, Proceedings of EUROSAM 79, Lecture Notes in Computer Science 72, Springer, 1979, pages 3 to 21"
    locator: the product criterion and the chain criterion that the installation applies
---

The Gebauer-Möller criteria are a way of applying Buchberger's product criterion and chain criterion to the list of critical pairs, each time a new polynomial is added to the basis, so that most pairs whose S-polynomials would reduce to zero are removed before any reduction, and no pair that is needed is ever removed. Buchberger's chain criterion alone is not safe to apply naively: two pairs can each be justified by the other, and removing both loses information. Gebauer and Möller (1988) split the chain criterion into three rules, called B, F and M, and fixed an order of application, the procedure UPDATE, that avoids this circularity. Almost every implementation of [Buchberger's algorithm](/buchberger-algorithm/), and the pair handling of [F4](/f4-algorithm/), use this procedure or a close variant.

## In plain words

Buchberger's algorithm checks pairs of polynomials. Most of these checks end with nothing new, and each one costs time. Two old rules can predict that a check will end with nothing, so it can be skipped.

The trouble is that one rule says "skip this pair because that other pair covers it", and the other pair may be skipped for the same reason, pointing back. Gebauer and Möller found a fixed order of skipping that never removes a pair whose check is really needed. Each time a new polynomial joins the list, it updates the list of pairs in three short passes.

## When it applies

Use it in any algorithm that computes a [Gröbner basis](/groebner-basis/) by adding polynomials one at a time and processing critical pairs: Buchberger's algorithm in any variant, with any selection strategy, and the pair management of F4. The setting is a field $K$, the ring $K[x_1, \ldots, x_n]$, and a fixed monomial order (lex, grlex or grevlex, or any other). For a polynomial $g$, $\operatorname{LT}(g)$, $\operatorname{LM}(g)$ and $\operatorname{LC}(g)$ are its leading term, monomial and coefficient. For a pair $(g_i, g_j)$, write

$$\operatorname{lcm}(i, j) = \operatorname{lcm}(\operatorname{LM}(g_i), \operatorname{LM}(g_j)).$$

The rules use only leading monomials, so they cost no field operations. They are not needed, and do not apply directly, in signature-based algorithms such as [F5](/f5-algorithm/), which have their own criteria.

The rules, for a new polynomial $h$ added to $G = (g_1, \ldots, g_t)$:

- **Criterion B** (on old pairs). Remove an old pair $(g_i, g_j)$ if $\operatorname{LM}(h)$ divides $\operatorname{lcm}(i, j)$, and $\operatorname{lcm}(i, h) \ne \operatorname{lcm}(i, j)$, and $\operatorname{lcm}(j, h) \ne \operatorname{lcm}(i, j)$. This is the chain criterion with $h$ as the middle element, restricted so that the two pairs that justify the removal have strictly smaller lcms.
- **Criterion M** (on new pairs). Remove a new pair $(h, g_i)$ if some other new pair $(h, g_k)$ has $\operatorname{lcm}(h, g_k)$ properly dividing $\operatorname{lcm}(h, g_i)$.
- **Criterion F** (on new pairs). Among new pairs with the same lcm, keep only one, and prefer one that satisfies the product criterion.
- **Product criterion.** Then remove the new pairs $(h, g_i)$ with $\gcd(\operatorname{LM}(h), \operatorname{LM}(g_i)) = 1$.

## The template

```pseudo id=main
UPDATE(G, B, h)                     ▷ G = (g_1, ..., g_t), B the pairs, h the new polynomial
L1  C ← {(i, h) : 1 ≤ i ≤ t}, D ← ∅
L2  while C ≠ ∅ do
L3      remove a pair (i, h) from C
L4      if LM(g_i) and LM(h) are coprime, or no pair (k, h) in C ∪ D has lcm(k, h) dividing lcm(i, h) then
L5          D ← D ∪ {(i, h)}                          ▷ criteria M and F
L6  E ← {(i, h) ∈ D : LM(g_i) and LM(h) are not coprime}   ▷ product criterion
L7  B' ← ∅
L8  for each (i, j) in B do
L9      if LM(h) does not divide lcm(i, j), or lcm(i, h) = lcm(i, j), or lcm(j, h) = lcm(i, j) then
L10         B' ← B' ∪ {(i, j)}                        ▷ criterion B
L11 append h to G as g_{t+1}
L12 return G, B' ∪ E
```

The main loop of the algorithm starts with $G$ and $B$ empty, calls UPDATE for each input polynomial, and then repeats: select a pair from $B$, reduce its S-polynomial by $G$, and if the remainder $h$ is nonzero, call UPDATE$(G, B, h)$. The loop at lines L2 to L5 keeps coprime pairs on purpose: a coprime pair with the same lcm as a non-coprime one must block the other under rule F before it is itself dropped at line L6, since the coprime pair is the one whose S-polynomial is known to reduce to zero.

**Why it is safe.** Gebauer and Möller proved that, after each call, every pair removed so far is covered: its S-polynomial is a combination of S-polynomials of pairs that are still in the list or already processed, whose lcms divide its own lcm, or it satisfies the product criterion. The proof is an induction on the lcm with respect to divisibility, which is well founded. With the main criterion of the [Buchberger criteria](/buchberger-criteria/) page, stated with lcm-representations, the final $G$ is a Gröbner basis. The strict conditions in criterion B and the "properly dividing" in criterion M are what make the induction work: they rule out cycles in which two pairs justify each other.

## Classic examples

A script implemented UPDATE as above and compared it with Buchberger's algorithm that reduces every pair, and with the version that uses only the product criterion. All three versions were run in exact rational arithmetic with grevlex and $x > y > z$, and gave the same reduced Gröbner basis. The table counts the S-polynomials reduced and, in parentheses, those that reduced to zero.

| system | every pair | product criterion | Gebauer-Möller |
|---|---|---|---|
| $x + y + z$, $xy + yz + zx$, $xyz - 1$ | 10 (8) | 6 (4) | 2 (0) |
| $x + 2y + 2z - 1$, $x^2 + 2y^2 + 2z^2 - x$, $2xy + 2yz - y$ | 15 (12) | 7 (4) | 4 (1) |
| $x^2 + y^2 - 4$, $xy - 1$ | 3 (2) | 2 (1) | 2 (1) |

On 150 random systems of up to three polynomials in three variables with both lex and grevlex, the results agreed in every case, and the Gebauer-Möller version reduced 162 S-polynomials against 349 for the version that reduces every pair.

Where the technique is used:

- [Buchberger's algorithm](/buchberger-algorithm/): the standard improved version calls UPDATE after each new basis element.
- [F4](/f4-algorithm/): the pairs of a degree are selected together, but the pair list is maintained with the same criteria.
- [Sugar strategy](/sugar-strategy/): the pair selection by sugar degree is combined with UPDATE in most systems; the criteria decide which pairs exist, the strategy decides their order.
- [Gröbner basis computation](/groebner-basis-computation/) in Singular, CoCoA, Macaulay2 and Magma uses variants of these rules.
- [Syzygy](/syzygy/) computations: the pairs that survive the criteria correspond to a generating set of the module of syzygies of the leading terms.

## Variations

- **Deleting redundant basis elements.** Becker and Weispfenning's version also removes from $G$ every $g$ whose leading monomial is divisible by $\operatorname{LM}(h)$, so that no future pair involves it. The removed polynomials are not needed for the leading monomial ideal, but implementations must keep them available or recompute the reductions accordingly.
- **Applying the chain criterion at selection time.** Buchberger's 1979 version tests the chain criterion when a pair is selected, against the pairs already processed. It needs bookkeeping of the processed pairs and removes fewer pairs.
- **Sugar and normal strategies.** The pairs in $B$ are ordered by lcm degree (the normal strategy) or by sugar degree; UPDATE does not depend on the order.
- **Signature criteria.** F5 and other signature-based algorithms replace B, F and M by the syzygy and rewrite criteria, which remove all reductions to zero for regular sequences.

## Pitfalls

- **Circular removal.** Applying the chain criterion "remove $(i, j)$ if some $k$ with $\operatorname{LM}(g_k) \mid \operatorname{lcm}(i, j)$ exists and pairs $(i, k)$, $(j, k)$ are in the list" to every pair at once can remove both $(i, k)$ and the pairs that justified it. The result can be a set that is not a Gröbner basis. Use the strict conditions.
- **Dropping the coprime pair too early.** If the product criterion is applied before rule F, a non-coprime pair with the same lcm as a coprime one survives, and its useless reduction is performed. Lines L4 to L6 fix the order.
- **Criteria are about leading monomials only.** They are sound only if the leading monomials used are those of the current polynomials. If the basis is interreduced during the run and a leading monomial changes, the pair list must be rebuilt.
- **Counting the savings.** The criteria do not remove all reductions to zero; on the second example above, one zero reduction remains. Algorithms that need to avoid all of them use signatures.

## Exercises

1. Let $G = (x^2 y, x y^2)$ with any degree order and add $h = x y$. List the old and new pairs after UPDATE.
2. Show that if $\operatorname{LM}(h)$ divides $\operatorname{lcm}(i, j)$ and $\operatorname{lcm}(i, h) = \operatorname{lcm}(i, j)$, removing $(i, j)$ by the chain criterion could make the algorithm depend on $(i, h)$ and $(i, j)$ justifying each other.
3. Construct two pairs with the same lcm, one coprime and one not, and trace lines L2 to L6 in both orders of removal from $C$.
4. Run Buchberger's algorithm with and without UPDATE on $x + y + z$, $xy + yz + zx$, $xyz - 1$ in grevlex, and check the counts in the table.
5. Prove that criterion M alone, applied to the new pairs, is safe, by showing that the removed pair's S-polynomial is a combination of two S-polynomials with smaller lcm.

## References
