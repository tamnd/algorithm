---
tag: 9JCFW4
kind: technique
slug: symbolic-method
name: Symbolic method
aliases:
- Flajolet-Sedgewick symbolic method
- combinatorial specifications
- admissible constructions
area: combinatorics/counting-algorithms
level: advanced
summary: Derives generating functions directly from recursive combinatorial specifications.
prereqs: [generating-functions, exponential-generating-functions]
see_also: [generating-functions, exponential-generating-functions, transfer-matrix-method, catalan-numbers, integer-partition-counting, counting-integer-compositions, bell-numbers, cayley-formula]
sources:
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter I, Sections I.1 and I.2 (combinatorial classes, admissible constructions and specifications), and Chapter II, Sections II.1 and II.2 (labelled classes and labelled constructions)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Chapter 5, Analytic Combinatorics
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Chapter 5, Sections 5.1 and 5.3 (the exponential formula and tree enumeration)
---

The symbolic method turns a grammar that describes a family of combinatorial objects into equations for their [generating functions](/generating-functions/), with no recurrence in between. Each construction of the grammar, such as a disjoint union, a pair, a sequence or a set, has a fixed translation into an operation on series. The method works for unlabeled objects with ordinary series and for labeled objects with [exponential series](/exponential-generating-functions/). Flajolet and Sedgewick made it the first part of their book on analytic combinatorics.

## In plain words

Many families of objects have a short recipe. A binary tree is either empty or a root with two binary trees under it. A composition of a number is a sequence of blocks. A set partition is a set of nonempty blocks. The symbolic method reads such a recipe word by word and replaces each word by an operation on counting series. "Either" becomes a sum, "with" becomes a product, "a sequence of" becomes one over one minus, and "a set of" becomes an exponential.

So you get the counting series of the family from the recipe at once. Then you solve the equation, or you let a program expand it, and you read the counts. The only thing to check is that the recipe builds each object in exactly one way.

## When it applies

- The objects have a size, with finitely many objects of each size, and the question asks for the count of each size.
- The objects have a recursive description in terms of smaller objects of the same or of other families: trees, words, compositions, partitions, permutations, graphs by components.
- The description is unambiguous: each object comes from exactly one derivation. If it is ambiguous, the series counts derivations, not objects.
- The atoms are either all unlabeled (use ordinary series) or all labeled with $[n]$ (use exponential series). Do not mix the two in one specification.

## The template

**Notation.** A *combinatorial class* $\mathcal A$ is a set with a size function $|\cdot|$ such that, for each $n \ge 0$, the number $a_n$ of objects of size $n$ is finite. Its ordinary series is $A(z) = \sum_n a_n z^n$, and for a labeled class its exponential series is $\hat A(z) = \sum_n a_n z^n/n!$. $\mathcal E$ is the class with one object of size 0, and $\mathcal Z$ the class with one atom of size 1. $\mathcal A_{\ge 1}$ means the objects of positive size.

**The dictionary.** A construction is *admissible* if the counts of the new class depend only on the counts of its arguments. The basic admissible constructions and their translations are these.

| construction | unlabeled, ordinary series | labeled, exponential series |
|---|---|---|
| neutral $\mathcal E$, atom $\mathcal Z$ | $1$, $z$ | $1$, $z$ |
| disjoint union $\mathcal A + \mathcal B$ | $A(z) + B(z)$ | $\hat A(z) + \hat B(z)$ |
| product $\mathcal A \times \mathcal B$ (labeled: $\mathcal A \star \mathcal B$) | $A(z)\, B(z)$ | $\hat A(z)\, \hat B(z)$ |
| sequence $\mathrm{SEQ}(\mathcal A)$, needs $a_0 = 0$ | $\frac{1}{1 - A(z)}$ | $\frac{1}{1 - \hat A(z)}$ |
| sequence of exactly $k$ components | $A(z)^k$ | $\hat A(z)^k$ |
| multiset $\mathrm{MSET}(\mathcal A)$, needs $a_0 = 0$ | $\prod_{n \ge 1} (1 - z^n)^{-a_n} = \exp \sum_{k \ge 1} \frac{A(z^k)}{k}$ | |
| set $\mathrm{PSET}(\mathcal A)$ (unlabeled: no repeats), needs $a_0 = 0$ | $\prod_{n \ge 1} (1 + z^n)^{a_n}$ | |
| labeled set $\mathrm{SET}(\mathcal A)$, needs $a_0 = 0$ | | $\exp \hat A(z)$ |
| set of exactly $k$ components (labeled) | | $\hat A(z)^k / k!$ |
| labeled cycle $\mathrm{CYC}(\mathcal A)$, needs $a_0 = 0$ | | $\log \frac{1}{1 - \hat A(z)}$ |

*Proof of the unlabeled rows.* Sum: an object of size $n$ of $\mathcal A + \mathcal B$ is an object of size $n$ of exactly one of the two classes, so $c_n = a_n + b_n$. Product: an object of size $n$ is a pair $(\alpha, \beta)$ with $|\alpha| + |\beta| = n$, so $c_n = \sum_k a_k b_{n-k}$, the coefficient of $z^n$ in $A(z) B(z)$. Sequence of $k$: apply the product rule $k - 1$ times. Sequence: $\mathrm{SEQ}(\mathcal A)$ is the disjoint union over $k \ge 0$ of the sequences of $k$ components. If $a_0 = 0$, then $A(z)^k$ has no term below $z^k$, so only $k \le n$ adds to $c_n$, each $c_n$ is finite, and $\sum_k A^k = 1/(1 - A)$ as formal series. Multiset: a multiset is fixed by the multiplicity $m_\alpha \ge 0$ of each object $\alpha$, with finitely many nonzero. Choosing $m_\alpha$ for one object of size $s$ gives the factor $\sum_m z^{sm} = (1 - z^s)^{-1}$, and the choices for different objects are independent, which gives the product. As $a_0 = 0$, only the factors with $s \le n$ touch $z^n$. Taking logarithms, $\sum_s a_s \sum_k z^{sk}/k = \sum_k A(z^k)/k$. Set without repeats: the same argument with $m_\alpha \in \{0, 1\}$ gives the factor $1 + z^s$. $\square$

*Proof of the labeled rows.* The labeled product is the product rule of [exponential generating functions](/exponential-generating-functions/): choose which labels go to the first component. The sequence rows follow as above. The set row is the exponential formula of that page: a set of $k$ components on disjoint nonempty blocks arises from $k!$ ordered sequences. A cycle of $k$ components arises from $k$ sequences, one for each starting point, so it has the series $\hat A^k/k$, and $\sum_{k \ge 1} \hat A^k / k = \log \frac{1}{1 - \hat A}$. $\square$

The method is the following procedure.

```pseudo id=main
SYMBOLIC-COUNT(family, N)
L1  write a specification: class = expression in E, Z, +, ×, SEQ, MSET, SET, CYC   ▷ hole: the grammar
L2  check that each object has exactly one derivation
L3  check that SEQ, MSET, SET and CYC get only arguments with no object of size 0
L4  replace each construction by its row of the dictionary
L5  if the specification is recursive then
L6      solve the system for the series, or keep it as a fixed point equation
L7  compute a_0, ..., a_N: expand the closed form, or iterate the fixed point
L8      ▷ each iteration fixes at least one more coefficient
L9  return a_0, ..., a_N
```

Line L8 holds for a well founded recursive specification: if $\mathcal T = \Phi(\mathcal T)$ and every use of $\mathcal T$ on the right is inside a product with a class whose objects all have positive size, then the coefficient of $z^n$ of $\Phi(T)$ depends only on the coefficients of $T$ below $z^n$. Starting from $T = 0$, after $n + 1$ rounds the coefficients up to $z^n$ are final. A program needs $N + 1$ rounds of $O(N^2)$ work each by this plain iteration, or $O(N^2)$ in total when it computes one new coefficient at a time.

## Classic examples

**1. Binary strings.** $\mathcal W = \mathrm{SEQ}(\mathcal Z_0 + \mathcal Z_1)$, two atoms of size 1, gives $W(z) = 1/(1 - 2z)$ and $2^n$ strings.

**2. Compositions.** A composition is a sequence of parts, and a part of size $j$ is a nonempty sequence of $j$ atoms: $\mathcal C = \mathrm{SEQ}(\mathrm{SEQ}_{\ge 1}(\mathcal Z))$. So $C(z) = 1/(1 - \frac{z}{1 - z}) = \frac{1 - z}{1 - 2z}$, and there are $2^{n-1}$ compositions of $n \ge 1$. See [counting integer compositions](/counting-integer-compositions/).

**3. Partitions.** A partition is a multiset of parts: $\mathcal P = \mathrm{MSET}(\mathrm{SEQ}_{\ge 1}(\mathcal Z))$, and the part class has one object of each size $n \ge 1$. So $P(z) = \prod_{n \ge 1} (1 - z^n)^{-1}$, with $1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42$ for $n = 0$ to $10$ (OEIS A000041). With PSET instead of MSET, the partitions into distinct parts have $\prod_n (1 + z^n)$ and the counts $1, 1, 1, 2, 2, 3, 4, 5, 6, 8, 10$ (OEIS A000009). See [counting integer partitions](/integer-partition-counting/).

**4. Binary trees and plane trees.** A binary tree is empty or a root with two subtrees: $\mathcal B = \mathcal E + \mathcal Z \times \mathcal B \times \mathcal B$, so $B = 1 + z B^2$, the equation of the [Catalan numbers](/catalan-numbers/). A plane tree is a root with a sequence of plane trees: $\mathcal G = \mathcal Z \times \mathrm{SEQ}(\mathcal G)$, so $G = z/(1 - G)$, and the number of plane trees with $n$ nodes is $C_{n-1}$: $1, 1, 2, 5, 14, 42, 132$.

**5. Unary-binary trees.** A node has zero, one or two ordered children: $\mathcal M = \mathcal Z \times (\mathcal E + \mathcal M + \mathcal M^2)$. So $M = z(1 + M + M^2)$, and the counts for $n = 1$ to $10$ nodes are $1, 1, 2, 4, 9, 21, 51, 127, 323, 835$, the Motzkin numbers (OEIS A001006).

**6. Set partitions and surjections (labeled).** $\mathrm{SET}(\mathrm{SET}_{\ge 1}(\mathcal Z))$ gives $\exp(e^z - 1)$, the series of the [Bell numbers](/bell-numbers/). $\mathrm{SEQ}(\mathrm{SET}_{\ge 1}(\mathcal Z))$ gives $1/(2 - e^z)$, the ordered set partitions.

**7. Permutations and derangements (labeled).** $\mathrm{SET}(\mathrm{CYC}(\mathcal Z))$ gives $\exp \log \frac{1}{1 - z} = \frac{1}{1 - z}$, so $n!$ permutations. Cycles of length at least 2 give $\frac{e^{-z}}{1 - z}$, the [derangements](/derangement/).

**8. Rooted labeled trees.** A rooted tree is a root with a set of rooted trees: $\mathcal T = \mathcal Z \star \mathrm{SET}(\mathcal T)$, so $\hat T = z\, e^{\hat T}$. Lagrange inversion gives $n^{n-1}$ trees on $n$ labeled nodes: $1, 2, 9, 64, 625, 7776$ (OEIS A000169). Dividing by the $n$ choices of root gives [Cayley's formula](/cayley-formula/) $n^{n-2}$.

## Variations

- **Restricted constructions.** $\mathrm{SEQ}_{\ge k}$, $\mathrm{SET}_k$, $\mathrm{CYC}_{= k}$ and so on keep only some numbers of components. Each has a translation, for example $\hat A^k/k!$ for $\mathrm{SET}_k$.
- **Parameters.** A second variable $u$ marks a parameter, such as the number of components or of leaves, and gives a bivariate series. This is how the [Stirling numbers](/stirling-numbers-second-kind/) come out of $\mathrm{SET}(u\, \mathrm{SET}_{\ge 1}(\mathcal Z))$.
- **Regular and context-free specifications.** A specification with only $+$, $\times$ and SEQ on finite classes has a rational series, and the [transfer-matrix method](/transfer-matrix-method/) handles it. A recursive specification with only $+$ and $\times$ has an algebraic series.
- **Pólya theory.** The unlabeled cycle construction and the multiset construction come from the action of a group on the components, as in the [Pólya enumeration theorem](/polya-enumeration-theorem/).
- **Random generation.** The same specification drives the recursive method of Nijenhuis and Wilf and the Boltzmann samplers, which draw a uniform random object of a given size.
- **Asymptotics.** The second part of analytic combinatorics reads the growth of $a_n$ from the singularities of the series that the symbolic method produced.

## Pitfalls

- **An ambiguous grammar.** The specification $\mathcal W = \mathcal E + \mathcal Z_0 + \mathcal Z_1 + \mathcal W \times \mathcal W$ for binary strings gives each string infinitely many derivations, for example $w = \varepsilon w = \varepsilon \varepsilon w$. Its equation $W = 1 + 2z + W^2$ has no power series solution with real coefficients, because the constant term $w$ would solve $w = 1 + w^2$. Write $\mathcal W = \mathrm{SEQ}(\mathcal Z_0 + \mathcal Z_1)$ instead. Test: compare the counts with a brute force list for small $n$.
- **SEQ or SET of a class with an object of size 0.** $\mathrm{SEQ}(\mathcal E + \mathcal Z)$ has infinitely many objects of each size, and $1/(1 - (1 + z))$ is not a power series. Remove the size 0 objects first.
- **MSET is not exp.** For unlabeled classes, $\exp A(z)$ is wrong. Partitions have $\prod (1 - z^n)^{-1}$, but $\exp(z/(1 - z))$ has the coefficients $1, 1, 3/2, 13/6, \ldots$, which are not even integers.
- **Mixing labeled and unlabeled.** A labeled product of an unlabeled class makes no sense. Decide at line L1 which universe the class lives in.
- **A specification that is not well founded.** $\mathcal T = \mathcal T \times \mathcal E + \mathcal Z$ gives $T = T + z$, which fixes nothing. Each recursive use must be inside a product with objects of positive size.

## Exercises

1. Write a specification of the binary strings with no two adjacent 1s, and get the series $\frac{1 + z}{1 - z - z^2}$.
2. Show that the compositions of $n$ with parts in $\{1, 2\}$ have the series $1/(1 - z - z^2)$, with the counts $F_{n+1}$.
3. Use $\mathrm{SET}(\mathrm{CYC}_{\le 2}(\mathcal Z))$ to get the series $\exp(z + z^2/2)$ of the involutions, and compute their counts $1, 1, 2, 4, 10, 26, 76$.
4. Show that $\mathrm{SEQ}(\mathcal Z \times \mathrm{SEQ}(\mathcal Z))$ and $\mathrm{SEQ}(\mathrm{SEQ}_{\ge 1}(\mathcal Z))$ give the same series, and explain the bijection between their objects.
5. Write a program that takes a specification built from $+$, $\times$, SEQ and MSET, and prints the counts up to size $N$. Test it on examples 2, 3 and 5.

## References
