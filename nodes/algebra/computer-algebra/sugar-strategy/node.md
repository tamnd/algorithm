---
tag: PJ5SDT
kind: technique
slug: sugar-strategy
name: Sugar strategy
aliases: [sugar selection, sugar cube strategy, sugar degree, selection by sugar]
area: algebra/computer-algebra
level: advanced
summary: Pair-selection strategy that orders S-polynomials by a degree-like sugar measure.
prereqs: [buchberger-algorithm, s-polynomial, monomial-ordering]
see_also: [buchberger-criteria, f4-algorithm, f5-algorithm, groebner-basis, reduced-groebner-basis, multivariate-division-algorithm, fglm-algorithm]
sources:
  - paper: doi:10.1145/120694.120701
    title: Alessandro Giovini, Teo Mora, Gianfranco Niesi, Lorenzo Robbiano and Carlo Traverso, One sugar cube, please, or selection strategies in the Buchberger algorithm, ISSAC 1991
    locator: pp. 49 to 54
  - paper: "Bruno Buchberger, Gröbner bases: an algorithmic method in polynomial ideal theory, in N. K. Bose (editor), Multidimensional Systems Theory, Reidel, 1985"
    locator: the normal selection strategy and the criteria for useless pairs
  - paper: doi:10.1016/j.jsc.2010.10.002
    title: Anna M. Bigatti, Massimo Caboara and Lorenzo Robbiano, Computing inhomogeneous Gröbner bases, Journal of Symbolic Computation 46(5), 2011
    locator: pp. 498 to 510 (the double sugar strategy)
  - paper: doi:10.1016/S0022-4049(99)00005-5
    title: Jean-Charles Faugère, A new efficient algorithm for computing Gröbner bases (F4), Journal of Pure and Applied Algebra 139(1-3), 1999
    locator: pp. 61 to 88 (selection of all pairs of least degree, with sugar for inhomogeneous input)
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 10, Improvements on Buchberger's Algorithm (selection strategies)
---

## In plain words

Buchberger's algorithm builds a Gröbner basis by taking pairs of polynomials, forming a combination of each pair, and reducing it. The result is the same whatever order the pairs are taken in, but the work is not. A bad order makes large intermediate polynomials that are later thrown away.

For inputs whose terms all have the same degree, a natural rule works well: treat pairs of the lowest degree first. For other inputs, the degrees can drop during a reduction, and the simple rule is misled. The sugar strategy fixes this. It gives each polynomial a number, its sugar, which is the degree it would have if a homogenizing variable had been added to all the inputs. The algorithm always treats the pair with the least sugar next. So it imitates the well-behaved homogeneous computation, but without the extra variable.

## When it applies

**Notation.** $K$ is a field and $K[x_1, \ldots, x_n]$ the polynomial ring, with a fixed monomial order $>$ (lex, grlex or grevlex, or an elimination order). $\mathrm{LT}$, $\mathrm{LM}$ and $\mathrm{LC}$ are the leading term, monomial and coefficient for $>$, and $\deg$ is the total degree. For a pair $(f, g)$, $L_{fg} = \operatorname{lcm}(\mathrm{LM}(f), \mathrm{LM}(g))$, and the [S-polynomial](/s-polynomial/) is $S(f, g) = \frac{L_{fg}}{\mathrm{LT}(f)} f - \frac{L_{fg}}{\mathrm{LT}(g)} g$.

**Sugar.** Each polynomial $f$ in the computation carries a natural number $\operatorname{sug}(f)$:

- for an input $f_i$, $\operatorname{sug}(f_i) = \deg(f_i)$;
- for a monomial multiple, $\operatorname{sug}(m f) = \deg(m) + \operatorname{sug}(f)$;
- for a sum, $\operatorname{sug}(f + g) = \max(\operatorname{sug}(f), \operatorname{sug}(g))$.

So the sugar of a pair is $\operatorname{sug}(f, g) = \max\left(\operatorname{sug}(f) + \deg\frac{L_{fg}}{\mathrm{LM}(f)}, \; \operatorname{sug}(g) + \deg\frac{L_{fg}}{\mathrm{LM}(g)}\right)$, which is the sugar of $S(f, g)$. Each reduction step $r \leftarrow r - c\, m\, h$ with $h \in G$ sets $\operatorname{sug}(r) \leftarrow \max(\operatorname{sug}(r), \deg(m) + \operatorname{sug}(h))$. So the remainder has sugar at least $\operatorname{sug}(f, g)$, and for lex it can be larger.

**Why it measures the right thing.** Homogenize every input with a new variable $z$, $f^{z} = z^{\deg f} f(x_1/z, \ldots, x_n/z)$. Do every step of the run on these homogeneous polynomials instead: form the same S-polynomials and the same reduction steps, and multiply by a power of $z$ wherever two parts of different degree are added, so that each result is homogeneous. Setting $z = 1$ gives back the original run. By induction, each polynomial of this shadow run is homogeneous, and its degree is exactly the sugar of the corresponding polynomial: the three rules above are the rules for degrees of homogeneous polynomials under products and under sums that are padded with powers of $z$. So sugar is the degree in a "phantom" homogeneous computation, and it is computed without carrying $z$.

**When to use it.** The technique applies to any critical-pair completion that selects pairs one at a time or in batches:

- Buchberger's algorithm on inhomogeneous input, above all for lex and elimination orders, where the *normal strategy* (least $L_{fg}$ in the order $>$, Buchberger 1985) can choose pairs of very high degree first;
- F4, which takes all pairs of least sugar as one batch for the linear algebra step;
- completion procedures of the same shape, such as standard bases and Buchberger-like algorithms for modules.

For homogeneous input with a degree-compatible order, sugar equals degree, and the sugar strategy is the normal strategy.

## The template

```pseudo id=main
SUGAR-BUCHBERGER(F, >)                     ▷ F finite in K[x_1..x_n], > a monomial order
L1  G ← F;  sug(f) ← ⟨initial sugar of f⟩ for f in G
L2  B ← {(f, g) : f, g in G, f ≠ g} minus ⟨pairs removed by the criteria⟩
L3  while B ≠ ∅ do
L4      choose (f, g) in B with least sug(f, g); break ties by ⟨tie-break rule⟩
L5      B ← B \ {(f, g)}
L6      r ← remainder of S(f, g) on division by G, with sug(r) ← sug(f, g) raised by each reduction step
L7      if r ≠ 0 then
L8          for each p in G: add (p, r) to B unless ⟨criteria⟩ show it useless
L9          G ← G ∪ {r}
L10 return G                               ▷ a Gröbner basis of (F) for >
```

The holes are:

- **Initial sugar** (L1). The total degree in the classic form. A weighted degree $\sum w_i e_i$ in the weighted form, which must then also be used in the rules for products.
- **Tie-break rule** (L4). The usual rule is the normal strategy: among pairs of least sugar, the one with least $L_{fg}$ in $>$. Another is the order of creation of the pairs.
- **Criteria** (L2, L8). Buchberger's coprime and chain criteria, or the Gebauer and Möller installation, see [Buchberger criteria](/buchberger-criteria/). They do not interact with sugar, except that a pair removed by the chain criterion must be removed by the same rule in the phantom homogeneous run, which holds.

**Worked example.** In $\mathbb{Q}[x, y]$ with lex, $x > y$, take $f_1 = x^2 - y$ and $f_2 = xy - 1$, both of sugar $2$.

1. $L_{12} = x^2 y$ and $S(f_1, f_2) = y f_1 - x f_2 = x - y^2$, with sugar $\max(2 + 1, 2 + 1) = 3$. It is reduced, since $x$ is not divisible by $x^2$ or $xy$. So $f_3 = x - y^2$ joins $G$ with sugar $3$, although its degree is $2$. In the homogenized run, $y f_1^z - x f_2^z = x z^2 - y^2 z$ has degree $3$.
2. The pairs $(f_1, f_3)$ and $(f_2, f_3)$ both have sugar $\max(2, 3 + 1) = 4$. The tie-break takes $(f_2, f_3)$, since $L_{23} = xy < x^2 = L_{13}$. $S(f_2, f_3) = f_2 - y f_3 = y^3 - 1$, which is reduced and joins $G$ with sugar $4$. The homogenized counterpart is $y^3 z - z^4$.
3. All remaining pairs reduce to $0$, and $G = \{x^2 - y, \; xy - 1, \; x - y^2, \; y^3 - 1\}$ is a Gröbner basis. The reduced Gröbner basis is $\{x - y^2, \; y^3 - 1\}$.

## Classic examples

- **[Buchberger's algorithm](/buchberger-algorithm/).** The original setting of Giovini, Mora, Niesi, Robbiano and Traverso (1991). They compared selection strategies on benchmark systems and found the sugar strategy competitive with the normal strategy for degree orders and much better on many inhomogeneous examples, and it became a default selection in CoCoA, Singular and other systems. This is an observation from experiments, not a theorem.
- **[F4](/f4-algorithm/).** Faugère's F4 selects all critical pairs of least degree at once; on inhomogeneous input the degree used is the sugar, so F4 proceeds degree by degree as it would on the homogenized system.
- **[F5](/f5-algorithm/).** F5 processes signatures in increasing degree, and on inhomogeneous input the degree of a signature plays the role of sugar.
- **Lex and [FGLM](/fglm-algorithm/).** For zero-dimensional systems a common route is a grevlex basis with sugar, then FGLM to lex. Direct lex computation with the sugar strategy is the alternative that the sugar paper measured.

## Variations

- **Weighted sugar.** With weights $w_1, \ldots, w_n > 0$, use the weighted degree in all three rules. This fits inputs that are quasi-homogeneous, which are then treated as homogeneous.
- **Double sugar** (Bigatti, Caboara and Robbiano 2011). Keep a second number that tracks the degree of the lowest homogeneous part, and use it to decide when a remainder is spurious. It refines the choice among pairs of equal sugar.
- **Sugar with degree bounds.** Since the sugar of the selected pairs never decreases along the run (Exercise 2), a run stopped when the least sugar in $B$ exceeds $D$ has treated every pair of sugar at most $D$. This is the analogue of a Gröbner basis truncated at degree $D$ for homogeneous input.
- **Sugar for modules and for syzygies.** The same rules with a degree for each module generator, as in Schreyer's method for [syzygies](/syzygy/).

## Pitfalls

- **Sugar is not the degree.** In the worked example $f_3 = x - y^2$ has degree $2$ and sugar $3$. Code that resets the sugar to the degree after reduction loses the link with the homogeneous run.
- **Ties matter.** Many pairs share the least sugar. A bad tie-break can still give poor runs, so the normal strategy is kept as the second key.
- **No worst-case gain.** The sugar strategy changes the order of the work, not the result, and it does not improve the worst case: Gröbner bases need doubly exponential degree in the worst case (Mayr and Meyer 1982), whatever the selection.
- **Inhomogeneous degree drops.** When an S-polynomial reduces to a polynomial of much smaller degree than its sugar, later pairs with it get sugar values that are too high, and the strategy delays useful work. This is what double sugar addresses.
- **Weighted inputs need weighted sugar.** Using plain degree for inputs that are homogeneous for other weights gives sugar values that do not match any homogeneous run.

## Exercises

1. Show that for homogeneous $F$ and a degree-compatible order, every polynomial in the run is homogeneous and its sugar equals its degree, so the sugar strategy is the normal strategy.
2. Prove that the sugar values of the selected pairs never decrease during a run of SUGAR-BUCHBERGER. (Hint: a new remainder $r$ has $\operatorname{sug}(r) \ge \operatorname{sug}(f, g)$, and every new pair $(p, r)$ has sugar at least $\operatorname{sug}(r)$.)
3. Redo the worked example with $f_1 = x^2 - y$, $f_2 = x y - 1$ in grevlex with $x > y$. Show that the basis gets one new element, $y^2 - x$, with sugar $3$ and degree $2$.
4. For $F = \{x^3 - 1, \; x y - 1\}$ in lex with $x > y$, show that the new basis elements are $y - x^2$, $x - y^2$ and $1 - y^3$, with sugar $4$, $5$ and $6$ and degrees $2$, $2$ and $3$. Then list the sugar values of the pairs in the order that the normal strategy treats them, and show that this list is not monotone, while the sugar strategy gives a monotone list.

## References
