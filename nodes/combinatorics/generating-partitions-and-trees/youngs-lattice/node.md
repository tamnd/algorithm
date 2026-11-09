---
tag: E6PB76
kind: definition
slug: youngs-lattice
name: Young's lattice
aliases:
- Lattice of partitions
- Young lattice
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: All integer partitions ordered by containment of Ferrers diagrams; a distributive lattice graded by size whose chains from the empty partition to lambda are the standard tableaux of shape lambda.
prereqs: [ferrers-diagram, lattice]
see_also: [young-tableau, standard-young-tableaux, integer-partitions, partition-lattice, hook-length-formula, integer-partition-function, conjugate-partition, mobius-function]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 3, Partially ordered sets (Young's lattice as an example, finite distributive lattices and the Moebius function of a distributive lattice, and differential posets)
  - paper: "Richard P. Stanley, Differential posets, Journal of the American Mathematical Society 1 (1988), 919-961"
    locator: the definition of a differential poset, Young's lattice as the main example, and the identity DU - UD = I with its counting consequences
  - book: isbn:9780387950679
    title: Bruce E. Sagan, The Symmetric Group, second edition, Springer, 2001
    locator: Chapter 5, Applications to combinatorics (Young's lattice, differential posets and the up and down operators)
---

Young's lattice $Y$ is the set of all integer partitions, ordered by inclusion of their [Ferrers diagrams](/ferrers-diagram/). Meet and join are the intersection and the union of the diagrams, so $Y$ is a distributive lattice, graded by the size $|\lambda|$, with $p(n)$ elements of rank $n$. A step up adds one cell, so the saturated chains from the empty partition to $\lambda$ are exactly the standard Young tableaux of shape $\lambda$. Each partition has exactly one more way up than down, and this one fact proves $\sum_{\lambda \vdash n} (f^\lambda)^2 = n!$.

## Definition

**Notation.** A partition is $\lambda = (\lambda_1 \ge \lambda_2 \ge \cdots)$ with finitely many nonzero parts, $|\lambda| = \sum_i \lambda_i$, and $D(\lambda) = \{(i, j) : 1 \le j \le \lambda_i\}$ is its diagram. $\varnothing$ is the empty partition. $f^\lambda$ is the number of [standard Young tableaux](/young-tableau/) of shape $\lambda$.

**Order.** $Y$ is the set of all partitions of all $n \ge 0$, with

$$\lambda \le \mu \iff \lambda_i \le \mu_i \text{ for all } i \iff D(\lambda) \subseteq D(\mu).$$

**Meet and join.** $(\lambda \wedge \mu)_i = \min(\lambda_i, \mu_i)$ and $(\lambda \vee \mu)_i = \max(\lambda_i, \mu_i)$. Both sequences are non-increasing, so they are partitions, and their diagrams are $D(\lambda) \cap D(\mu)$ and $D(\lambda) \cup D(\mu)$. Since meet and join are intersection and union of sets, they distribute over each other, and $Y$ is a distributive [lattice](/lattice/). Equivalently, $Y$ is the lattice of finite order ideals of $\mathbb{N}_{\ge 1} \times \mathbb{N}_{\ge 1}$ under the componentwise order: a finite set of cells is a diagram exactly when it is closed under moving up and moving left.

**Rank and covers.** $\mu$ covers $\lambda$ exactly when $D(\mu) = D(\lambda) \cup \{a\}$ for one cell $a \notin D(\lambda)$. So $Y$ has least element $\varnothing$ and is graded by $\mathrm{rank}(\lambda) = |\lambda|$. The number of elements of rank $n$ is the [partition number](/integer-partition-function/) $p(n)$. $Y$ has no greatest element.

**Addable and removable cells.** A cell $a$ is addable to $\lambda$ when $D(\lambda) \cup \{a\}$ is a diagram, and a cell $c \in D(\lambda)$ is removable (a corner) when $D(\lambda) \setminus \{c\}$ is a diagram. If $\lambda$ has $m$ distinct nonzero part values, then

$$\#\{\text{addable cells}\} = m + 1, \qquad \#\{\text{removable cells}\} = m.$$

*Proof.* The removable cells are $(i, \lambda_i)$ with $\lambda_{i+1} < \lambda_i$, one at the last row of each run of equal parts, so there are $m$. The addable cells are $(i, \lambda_i + 1)$ with $i = 1$ or $\lambda_{i-1} > \lambda_i$, one at the first row of each run, plus the cell $(\ell + 1, 1)$ below the last row, so there are $m + 1$. $\square$

**Chains and tableaux.** A saturated chain $\varnothing = \lambda^{(0)} \lessdot \lambda^{(1)} \lessdot \cdots \lessdot \lambda^{(n)} = \lambda$ adds one cell at each step. Writing $k$ in the cell added at step $k$ gives an SYT of shape $\lambda$, and every SYT arises once in this way. So the number of saturated chains from $\varnothing$ to $\lambda$ is $f^\lambda$. More generally, the saturated chains from $\lambda$ to $\mu$ are the standard tableaux of the skew shape $\mu / \lambda$.

**Differential poset.** Let $U$ and $D$ be the linear maps on formal sums of partitions with $U\lambda = \sum_{\mu \gtrdot \lambda} \mu$ and $D\lambda = \sum_{\nu \lessdot \lambda} \nu$. Then

$$DU - UD = I.$$

*Proof.* In $DU\lambda$ the term $\lambda$ appears once for each addable cell, and in $UD\lambda$ once for each removable cell, so by the count above its coefficient in $DU\lambda - UD\lambda$ is $(m + 1) - m = 1$. A partition $\nu \ne \lambda$ of the same size appears in $DU\lambda$ once for each common upper cover of $\lambda$ and $\nu$, and in $UD\lambda$ once for each common lower cover. Both are $1$ if $D(\lambda)$ and $D(\nu)$ differ in exactly one cell each, with the cover $\lambda \vee \nu$ or $\lambda \wedge \nu$, and both are $0$ otherwise. $\square$

Stanley called a graded poset with this property, together with a unique least element and local finiteness, a $1$-differential poset. $Y$ is the main example.

**Möbius function.** For $\lambda \le \mu$, the [Möbius function](/mobius-function/) of $Y$ is $\mu(\lambda, \mu) = (-1)^{|\mu| - |\lambda|}$ if no two cells of $D(\mu) \setminus D(\lambda)$ lie in the same row or column, and $0$ otherwise. This is the rule for a finite distributive lattice $J(P)$, where $\mu(I, I') = (-1)^{|I' \setminus I|}$ when $I' \setminus I$ is an antichain of $P$, applied to the poset of cells (Stanley, Chapter 3).

## Examples and non-examples

**The first ranks.** Rank $0$: $\varnothing$. Rank $1$: $(1)$. Rank $2$: $(2)$, $(1, 1)$. Rank $3$: $(3)$, $(2, 1)$, $(1, 1, 1)$. Rank $4$: $(4)$, $(3, 1)$, $(2, 2)$, $(2, 1, 1)$, $(1, 1, 1, 1)$. The rank sizes $1, 1, 2, 3, 5, 7, 11, 15$ are $p(0), \ldots, p(7)$.

**Meet and join.** For $\lambda = (3, 1)$ and $\mu = (2, 2)$, $\lambda \wedge \mu = (2, 1)$ and $\lambda \vee \mu = (3, 2)$. Here $D(\lambda)$ and $D(\mu)$ differ in one cell each, so $(3, 1)$ and $(2, 2)$ have exactly one common upper cover and one common lower cover, as in the proof of $DU - UD = I$.

**Ups and downs.** $\lambda = (3, 3, 1)$ has $m = 2$ distinct parts. Its removable cells are $(2, 3)$ and $(3, 1)$, and its addable cells are $(1, 4)$, $(3, 2)$ and $(4, 1)$.

**An interval.** $[\varnothing, (2, 2)]$ has the six elements $\varnothing, (1), (2), (1, 1), (2, 1), (2, 2)$. It has $f^{(2,2)} = 2$ maximal chains, which go through $(2)$ or through $(1, 1)$: the tableaux $12/34$ and $13/24$.

**Möbius values.** $\mu((1), (2, 1)) = 1$, since the two added cells $(1, 2)$ and $(2, 1)$ are in different rows and columns. $\mu(\varnothing, (2, 1)) = 0$, since $(1, 1)$ and $(1, 2)$ share a row.

**Sum of squares.** From $DU - UD = I$, induction on $n$ gives $D U^n = n U^{n-1} + U^n D$. Since $D \varnothing = 0$, this gives $D U^n \varnothing = n U^{n-1} \varnothing$, and then $D^n U^n \varnothing = n!\, \varnothing$. The coefficient of $\varnothing$ in $D^n U^n \varnothing$ counts the walks that go up $n$ steps from $\varnothing$ to some $\lambda \vdash n$ and down $n$ steps back, which is $\sum_{\lambda \vdash n} (f^\lambda)^2$. So $\sum_{\lambda \vdash n} (f^\lambda)^2 = n!$. For $n = 4$: $1 + 9 + 4 + 9 + 1 = 24$.

**Non-example: dominance order.** The dominance order compares partitions of the same $n$ by partial sums: $\lambda \trianglelefteq \mu$ when $\lambda_1 + \cdots + \lambda_i \le \mu_1 + \cdots + \mu_i$ for all $i$. In $Y$, two different partitions of the same $n$ are never comparable, so the two orders are different. For example $(2, 2) \trianglelefteq (3, 1)$ holds in dominance order, but neither diagram contains the other, so the two are incomparable in $Y$.

**Non-example: the partition lattice.** The [partition lattice](/partition-lattice/) $\Pi_n$ orders the set partitions of $[n]$ by refinement. It is finite, not distributive for $n \ge 3$, and its elements are partitions of a set, not of an integer.

## Related definitions

- [Ferrers diagram](/ferrers-diagram/) and [integer partitions](/integer-partitions/) are the elements; the [conjugate partition](/conjugate-partition/) is an automorphism of $Y$, since transposing diagrams keeps inclusion.
- [Young tableau](/young-tableau/) and [standard Young tableaux enumeration](/standard-young-tableaux/): saturated chains from $\varnothing$.
- The [hook length formula](/hook-length-formula/) counts the maximal chains of the interval $[\varnothing, \lambda]$.
- A distributive [lattice](/lattice/) is a lattice in which meet and join distribute over each other. By Birkhoff's theorem, a finite distributive lattice is the lattice $J(P)$ of order ideals of a poset $P$, and $[\varnothing, \lambda] = J(D(\lambda))$.
- An $r$-differential poset satisfies $DU - UD = rI$. The Fibonacci lattice is another $1$-differential poset, and the product of $r$ copies of $Y$ is $r$-differential.
- The [partition lattice](/partition-lattice/) is the analogous lattice for set partitions.

## References
