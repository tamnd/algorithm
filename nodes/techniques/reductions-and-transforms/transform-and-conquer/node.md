---
tag: BEESD7
kind: technique
slug: transform-and-conquer
name: Transform-and-conquer
aliases:
- transform and conquer
area: techniques/reductions-and-transforms
level: intro
summary: Transforming a problem into a different representation or form that is easier to solve, then solving that form.
prereqs: [asymptotic-notation, sorting-problem]
see_also: [presorting, horner-rule, heapsort, gaussian-elimination, balanced-binary-search-tree, reduction, canonicalization, normal-form-representation]
sources:
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition, Pearson, 2012
    locator: Chapter 6, Transform-and-Conquer (6.1 Presorting, 6.2 Gaussian Elimination, 6.3 Balanced Search Trees, 6.4 Heaps and Heapsort, 6.5 Horner's Rule and Binary Exponentiation, 6.6 Problem Reduction)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Heapsort; Section 28.1, Solving systems of linear equations; Section 30.1 (Horner's rule)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.4, Evaluation of polynomials (Horner's rule); Section 4.6.3, Evaluation of powers
---

Transform-and-conquer is a design technique in two stages: first transform the instance into another one that is easier to solve, then solve the new instance and, if needed, map its answer back. Levitin names three kinds of transformation: *instance simplification* (the same problem on a more convenient instance, as in [presorting](/presorting/)), *representation change* (the same instance stored in another form, as in a [heap](/heap/) or the nested form of [Horner's rule](/horner-rule/)), and *problem reduction* (an instance of a different problem with a known algorithm, as in a [reduction](/reduction/)). The technique pays off when the cost of the transformation plus the cost of solving the new form is less than the cost of solving the original directly.

## In plain words

Some problems are hard in the shape in which you get them, and easy in another shape. Before you solve such a problem, change its shape.

There are three ways to do this. You can tidy the input, for example put a list in order, so that later steps are short. You can store the same data in a better structure, for example a tree that stays balanced, so that each search is fast. Or you can turn the problem into a different problem that you already know how to solve, and then translate the answer back.

The change has a cost. It is worth it when the change plus the easy solve cost less than the direct attack, or when one change serves many later questions.

## When it applies

- The direct algorithm repeats work that an order, a structure or a normal form would make unnecessary: all-pairs comparisons, repeated powers of $x$, unbalanced searches.
- Many queries or operations act on the same data, so a structure built once serves all of them.
- The instance has a standard form in which the answer can be read off: a sorted array, a triangular system, a [canonical form](/canonicalization/), a [normal form](/normal-form-representation/).
- The problem is a special case or a disguise of a problem with a known good algorithm: shortest paths, flows, [linear programming](/reduction-to-linear-programming/), sorting.

## The template

The holes are TRANSFORM, SOLVE and BACK. In instance simplification and representation change, BACK is often the identity.

```pseudo id=main
TRANSFORM-AND-CONQUER(x)
L1  y ← TRANSFORM(x)         ▷ simplify x, change its representation, or map it to another problem
L2  z ← SOLVE(y)             ▷ an algorithm that is fast on the new form
L3  return BACK(x, z)        ▷ translate the answer of y into an answer of x
```

The cost is $T(x) = T_{\text{TRANSFORM}}(x) + T_{\text{SOLVE}}(y) + T_{\text{BACK}}(x, z)$. Correctness rests on one lemma for each use: BACK applied to a correct answer for $y$ gives a correct answer for $x$. For instance simplification and representation change, the lemma is that $y$ has the same answer as $x$ (sorting does not change the multiset; row operations do not change the solution set). For problem reduction, it is the correctness of the [reduction](/reduction/).

When the same transformed form serves $k$ queries, the cost becomes $T_{\text{TRANSFORM}} + k \cdot T_{\text{query}}$, and the transformation is worth it once $k$ is large enough.

## Classic examples

The examples are grouped by Levitin's three kinds.

### Instance simplification

- **[Presorting](/presorting/).** Sort the array, then scan it. Element uniqueness and the mode drop from $\Theta(n^2)$ comparisons to $O(n \log n)$.
- **[Gaussian elimination](/gaussian-elimination/).** Replace the system $Ax = b$ by an equivalent upper-triangular system, using row operations that keep the solution set. Back substitution then solves it. For $n$ equations, elimination takes $\Theta(n^3)$ arithmetic operations and back substitution $\Theta(n^2)$. The [LU decomposition](/lu-decomposition/) stores the elimination so that each new right-hand side $b$ costs only $\Theta(n^2)$.
- **[AVL trees](/avl-tree/).** A [binary search tree](/binary-search-tree/) can become a path of height $n - 1$. An AVL tree applies rotations after each update to keep the heights of the two subtrees of every node within $1$ of each other, which keeps the height $O(\log n)$ and each search, insertion and deletion $O(\log n)$.

### Representation change

- **[Horner's rule](/horner-rule/).** Write $p(x) = a_n x^n + \cdots + a_1 x + a_0$ as $(\cdots((a_n x + a_{n-1}) x + a_{n-2}) \cdots) x + a_0$. The nested form uses exactly $n$ multiplications and $n$ additions. For $p(x) = 2x^4 - x^3 + 3x^2 + x - 5$ at $x = 3$, the partial values are $2$, $2 \cdot 3 - 1 = 5$, $5 \cdot 3 + 3 = 18$, $18 \cdot 3 + 1 = 55$, $55 \cdot 3 - 5 = 160$, so $p(3) = 160$ after $4$ multiplications. For a general polynomial whose coefficients are part of the input, no algorithm uses fewer multiplications ([optimality of Horner's rule](/horners-rule-optimality/)).
- **[Binary exponentiation](/binary-exponentiation/).** Write the exponent in binary and apply Horner's idea to its bits. For $a^{13}$ with $13 = 1101_2$: $a \to a^2 \to a^3 \to a^6 \to a^{12} \to a^{13}$, with $3$ squarings and $2$ multiplications instead of $12$ multiplications. In general it uses at most $2 \lfloor \lg n \rfloor$ multiplications.
- **[Heaps](/heap/) and [heapsort](/heapsort/).** Store a set as an array that satisfies the heap order. [Heap construction](/heap-construction/) takes $O(n)$ time, and each deletion of the maximum takes $O(\log n)$, so heapsort sorts in $O(n \log n)$ time in the worst case, in place.
- **[2-3 trees](/two-three-tree/) and [B-trees](/b-tree/).** Allow a node to hold more than one key. All leaves then lie at the same depth, so the tree is balanced by its shape, and the height is $O(\log n)$.

### Problem reduction

- **[Least common multiple](/least-common-multiple/).** Reduce to the [gcd](/gcd-of-two-integers/): $\operatorname{lcm}(m, n) = mn / \gcd(m, n)$ for positive $m, n$ ([gcd and lcm identity](/gcd-lcm-identity/)). For $m = 24$ and $n = 60$, $\gcd = 12$ by the [Euclidean algorithm](/euclidean-algorithm/), and $\operatorname{lcm} = 1440 / 12 = 120$, with no factoring.
- **Counting walks.** The number of walks of length $k$ from vertex $i$ to vertex $j$ of a graph is the entry $(A^k)_{ij}$ of the $k$th power of its [adjacency matrix](/adjacency-matrix/). In the graph on $\{a, b, c, d\}$ with edges $ab$, $ac$, $ad$ and $cd$, $(A^3)_{ac} = 4$: the walks $abac$, $acac$, $adac$ and $acdc$. [Matrix exponentiation](/matrix-exponentiation/) computes $A^k$ with $O(\log k)$ matrix products.
- **[Reduction to linear programming](/reduction-to-linear-programming/)** and **[reduction to sorting](/reduction-to-sorting/).** Formulate the problem as a linear program, or as a sort of derived items, and use the known algorithm.

## Variations

- **Canonical and normal forms.** Transform each object into a fixed form so that equal objects get equal forms ([canonicalization](/canonicalization/)), or so that one algorithm handles one shape ([normal forms](/normal-form-representation/) such as CNF).
- **Coordinate change.** Replace large values by their ranks ([coordinate compression](/coordinate-compression/)), or change the domain, as the FFT does when it multiplies polynomials through their values at roots of unity ([FFT polynomial multiplication](/fft-polynomial-multiplication/)).
- **Preprocessing for queries.** Build a structure once (a sorted array, a heap, a balanced tree) and answer many queries on it. The cost is then shared, and the analysis is per query or [amortized](/amortized-cost/).

## Pitfalls

- **A transformation that costs more than it saves.** Sorting an array to search it once costs $\Theta(n \log n)$, more than the $n$ comparisons of a sequential search.
- **A transformation that changes the answer.** Sorting loses positions, compression loses distances, and Tseitin's CNF changes the set of variables. State what the new form keeps, and prove that it is enough for the question.
- **Blow-up of the new form.** Some normal forms are exponentially larger than the input: the CNF of a DNF by the distributive law is an example. Measure the size of the transformed instance, not only the time per element.
- **Numerical problems.** Gaussian elimination without pivoting divides by small numbers and loses accuracy in floating point. Use partial pivoting, which is part of the standard algorithm.
- **A reduction in the wrong direction.** To solve problem $A$, reduce $A$ to a problem $B$ that you can solve. Reducing $B$ to $A$ proves something about $B$, not an algorithm for $A$.

## Exercises

1. Evaluate $p(x) = 3x^5 - 2x^3 + x - 7$ at $x = -2$ by Horner's rule, and count the multiplications and additions.
2. Count the multiplications that binary exponentiation uses for $a^{100}$, and compare with $99$.
3. Given an array of $n$ numbers and an integer $s$, decide whether two of the numbers sum to $s$. Give a $\Theta(n^2)$ brute-force algorithm and an $O(n \log n)$ algorithm by instance simplification.
4. Reduce the problem "find the maximum of $\sum_i c_i x_i$ subject to $\sum_i a_i x_i \le b$ and $0 \le x_i \le 1$", with all $a_i > 0$, to sorting, and prove the reduction correct.
5. Show that the number of walks of length $k$ from $i$ to $j$ equals $(A^k)_{ij}$, by induction on $k$.
6. For each of Levitin's three kinds, give one example that is not on this page.

## References
