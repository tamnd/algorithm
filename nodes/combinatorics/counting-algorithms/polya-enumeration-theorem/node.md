---
tag: YQZSVG
kind: theorem
slug: polya-enumeration-theorem
name: Pólya enumeration theorem
aliases:
- Pólya counting
- cycle index method
- Redfield-Pólya theorem
area: combinatorics/counting-algorithms
level: advanced
summary: The colorings of a finite set up to a permutation group, counted by color content, are given by the cycle index of the group with each variable replaced by a power sum of the color weights.
prereqs: [burnside-lemma, permutation-cycles, symmetric-group, generating-functions]
see_also: [burnside-lemma, necklace-counting, counting-labeled-graphs, integer-partitions, cyclic-group, graph-isomorphism-problem, symbolic-method, euler-totient]
sources:
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: Chapter 37, Pólya theory of counting (the cycle index, the theorem and its examples)
  - book: isbn:9780123242457
    title: Frank Harary and Edgar M. Palmer, Graphical Enumeration, Academic Press, 1973
    locator: Chapter 2, Pólya's theorem (statement and proof), and Chapter 4 (graphs counted with the cycle index of the pair group)
  - paper: doi:10.1007/BF02546665
    title: George Pólya, Kombinatorische Anzahlbestimmungen für Gruppen, Graphen und chemische Verbindungen, Acta Mathematica 68, 145 to 254, 1937
    locator: Chapter 1 (the main theorem)
  - paper: doi:10.2307/2370675
    title: J. Howard Redfield, The theory of group-reduced distributions, American Journal of Mathematics 49(3), 433 to 455, 1927
    locator: the whole paper (the cycle index under the name group reduction function)
---

The Pólya enumeration theorem counts the colorings of a finite set up to a group of symmetries, and it sorts them by how many times each color is used. The answer is the *cycle index* of the group, a polynomial that records the cycle types of its permutations, with the variable $x_k$ replaced by the sum of the $k$-th powers of the color weights. It is [Burnside's lemma](/burnside-lemma/) with weights, and it turns a count of orbits into one substitution in a polynomial. Its classic uses are necklaces, chemical isomers and graphs up to isomorphism.

## Statement

Notation: $D$ is a finite set with $n = |D|$ elements (the positions), $C$ is a set of colors, and $G$ is a group of permutations of $D$. A *coloring* is a map $f : D \to C$, and $G$ acts on colorings by $(g \cdot f)(d) = f(g^{-1}(d))$. Two colorings are *equivalent* if they are in the same orbit. Each color $c$ has a *weight* $w(c)$ in a commutative ring $R$ that contains the rationals, for example a polynomial ring $\mathbb{Q}[y_1, \ldots, y_m]$. The weight of a coloring is $W(f) = \prod_{d \in D} w(f(d))$. Since $g$ permutes $D$, $W(g \cdot f) = W(f)$, so each orbit $O$ has a well-defined weight $W(O)$.

For $g \in G$, let $c_k(g)$ be the number of cycles of length $k$ of $g$ on $D$, so $\sum_k k \, c_k(g) = n$. The *cycle index* of $G$ is

$$Z_G(x_1, \ldots, x_n) = \frac{1}{|G|} \sum_{g \in G} x_1^{c_1(g)} x_2^{c_2(g)} \cdots x_n^{c_n(g)}.$$

**Theorem (Pólya, Redfield).** Assume that the sums $p_k = \sum_{c \in C} w(c)^k$ are defined (for example, $C$ is finite). Then

$$\sum_{O \in C^D / G} W(O) = Z_G(p_1, p_2, \ldots, p_n).$$

**Corollary.** With $k$ colors and all weights 1, the number of colorings up to $G$ is $Z_G(k, k, \ldots, k)$.

With colors $y_1, \ldots, y_m$ and $w(y_i) = y_i$, the coefficient of $y_1^{a_1} \cdots y_m^{a_m}$ on the right side is the number of orbits of colorings that use color $i$ exactly $a_i$ times.

Three cycle indices that recur:

- **Cyclic group** $C_n$ (rotations of $n$ beads): $Z = \frac{1}{n} \sum_{d \mid n} \varphi(d) \, x_d^{n/d}$, since the rotation by $r$ has $\gcd(r, n)$ cycles of length $n/\gcd(r, n)$, and exactly $\varphi(d)$ rotations have cycle length $d$.
- **Symmetric group** $S_n$ on $[n]$: $Z = \sum \prod_k \frac{x_k^{j_k}}{k^{j_k} \, j_k!}$, summed over the vectors $(j_1, \ldots, j_n)$ with $\sum_k k j_k = n$, because $n! / \prod_k k^{j_k} j_k!$ permutations have $j_k$ cycles of length $k$ for each $k$.
- **Pair group** $S_n^{(2)}$, the action of $S_n$ on the $\binom{n}{2}$ possible edges: a permutation with $j_k$ cycles of length $k$ moves the edges in cycles as follows. A cycle of odd length $k$ gives $(k-1)/2$ edge cycles of length $k$. A cycle of even length $k$ gives $(k-2)/2$ edge cycles of length $k$ and one of length $k/2$. Two cycles of lengths $k$ and $l$ give $\gcd(k, l)$ edge cycles of length $\mathrm{lcm}(k, l)$.

## In plain words

Suppose you paint the beads of a bracelet and two paintings count as the same when you can turn one into the other. You want to know how many different bracelets have three red beads and three blue beads, and how many have four red and two blue, and so on, all at once.

The theorem says: write down, for each symmetry, how it moves the positions around in closed loops. A painting stays the same under that symmetry exactly when each loop has one color. Collect the loop patterns of all the symmetries into one formula. Then put in, for each loop length, the sum of the color names raised to that length. When you multiply out and average, the number in front of each color mix is the number of different objects with that mix.

## Proof

*Step 1 (weighted Burnside lemma).* Let a finite group $G$ act on a finite set $X$, and let $W : X \to R$ be constant on each orbit. Then $\sum_{O \in X/G} W(O) = \frac{1}{|G|} \sum_{g \in G} \sum_{x \in \mathrm{Fix}(g)} W(x)$.

Count the weighted pairs $(g, x)$ with $g \cdot x = x$, each with weight $W(x)$. Summed by $g$, the total is the right side times $|G|$. Summed by $x$, the total is $\sum_{x} |G_x| \, W(x)$, where $G_x$ is the stabilizer. By the orbit-stabilizer lemma on the [Burnside's lemma](/burnside-lemma/) page, $|G_x| = |G| / |G \cdot x|$. Group the points by orbit; on an orbit $O$ the weight is the constant $W(O)$, so the orbit contributes $\sum_{x \in O} \frac{|G|}{|O|} W(O) = |G| \, W(O)$. Divide by $|G|$, which is invertible in $R$ because $R$ contains the rationals. $\square$

*Step 2 (the fixed colorings of one permutation).* Fix $g \in G$, and let its cycles on $D$ be $D_1, \ldots, D_r$, with lengths $\ell_1, \ldots, \ell_r$. A coloring $f$ satisfies $g \cdot f = f$ if and only if $f(g^{-1}(d)) = f(d)$ for all $d$, that is, if and only if $f$ is constant on each cycle $D_i$. Such a coloring is given by the color $c_i$ of each cycle, chosen independently, and its weight is $\prod_{i} w(c_i)^{\ell_i}$. So

$$\sum_{f \in \mathrm{Fix}(g)} W(f) = \prod_{i=1}^{r} \sum_{c \in C} w(c)^{\ell_i} = \prod_{i=1}^{r} p_{\ell_i} = \prod_{k=1}^{n} p_k^{c_k(g)}.$$

The first equality is the expansion of a product of sums (the distributive law over the independent choices).

*Step 3.* Apply Step 1 with $X = C^D$, using that $W$ is constant on orbits, and insert Step 2:

$$\sum_{O} W(O) = \frac{1}{|G|} \sum_{g \in G} \prod_{k=1}^{n} p_k^{c_k(g)} = Z_G(p_1, \ldots, p_n). \qquad \blacksquare$$

The corollary is the case $w \equiv 1$, where $p_k = k$ for every $k$ when there are $k$ colors (here the letter $k$ is the number of colors, not a cycle length). The three cycle indices follow from counting cycles. For the pair group, the edge $\{a, b\}$ with $a$ and $b$ in one cycle of length $k$ returns to itself after $k$ steps, or after $k/2$ steps when $k$ is even and $b$ is the point opposite $a$. There are $k/2$ such opposite pairs in the cycle, and they form one edge cycle of length $k/2$. With $a$ in a cycle of length $k$ and $b$ in another cycle of length $l$, the edge returns after $\mathrm{lcm}(k, l)$ steps, and the $kl$ such edges split into $kl / \mathrm{lcm}(k, l) = \gcd(k, l)$ cycles.

## Consequences

### Worked examples

**Necklaces of 6 beads in two colors, by the number of black beads.** The cycle index of $C_6$ is $\frac{1}{6}(x_1^6 + x_2^3 + 2x_3^2 + 2x_6)$. Put $x_k = b^k + w^k$:

$$\tfrac{1}{6}\big((b+w)^6 + (b^2+w^2)^3 + 2(b^3+w^3)^2 + 2(b^6+w^6)\big) = b^6 + b^5 w + 3 b^4 w^2 + 4 b^3 w^3 + 3 b^2 w^4 + b w^5 + w^6.$$

So there are 4 necklaces with three black and three white beads, and $1 + 1 + 3 + 4 + 3 + 1 + 1 = 14$ in total, which is the value $Z(2, \ldots, 2)$ and the entry for 6 beads in OEIS A000031.

**Graphs on 4 unlabeled vertices, by the number of edges.** The pair group $S_4^{(2)}$ acts on the 6 possible edges. Its cycle index, from the five cycle types of $S_4$, is

| permutations of the 4 vertices | how many | cycles on the 6 edges |
|---|---|---|
| identity | 1 | $x_1^6$ |
| one transposition | 6 | $x_1^2 x_2^2$ |
| two transpositions | 3 | $x_1^2 x_2^2$ |
| a 3-cycle | 8 | $x_3^2$ |
| a 4-cycle | 6 | $x_2 x_4$ |

So $Z = \frac{1}{24}(x_1^6 + 9x_1^2x_2^2 + 8x_3^2 + 6x_2x_4)$. A graph is a 2-coloring of the edges: present (weight $y$) or absent (weight 1). Put $x_k = 1 + y^k$:

$$Z = 1 + y + 2y^2 + 3y^3 + 2y^4 + y^5 + y^6.$$

There are 11 graphs on 4 vertices up to isomorphism, and 3 of them have 3 edges: the triangle with an isolated vertex, the path, and the star. The same method gives the number of graphs on $n$ unlabeled vertices for $n = 0, 1, \ldots, 10$: 1, 1, 2, 4, 11, 34, 156, 1044, 12346, 274668, 12005168 (OEIS A000088), and the full table by edges is OEIS A008406.

### Where the theorem is used

- **Counting with a cycle index is an algorithm.** For the pair group, the sum runs over the cycle types of $S_n$, which are the [integer partitions](/integer-partitions/) of $n$, not over the $n!$ permutations. Each type needs $O(n^2)$ work to find its edge cycles from the rules above, plus big-integer arithmetic on numbers of about $\binom{n}{2}$ binary digits. This is how the counts of unlabeled graphs are computed.
- **Necklaces and bracelets.** The cyclic and dihedral groups give the formulas on the [necklace counting](/necklace-counting/) page, also by content.
- **Unlabeled versus labeled.** The number of labeled graphs is $2^{\binom{n}{2}}$ (see [counting labeled graphs](/counting-labeled-graphs/)). Pólya's method counts the classes of these under renaming of the vertices, which is the count behind the [graph isomorphism problem](/graph-isomorphism-problem/).
- **Unlabeled constructions.** In the [symbolic method](/symbolic-method/), the multiset and cycle constructions for unlabeled classes are the cycle indices of the symmetric and cyclic groups applied to a generating function. This is Pólya's theorem with infinitely many colors, one for each object of the inner class.
- **Chemistry.** Pólya's 1937 paper applied the method to count chemical isomers, which are tree-like molecules up to symmetry.

## Tightness

The theorem is an exact identity. Its hypotheses are needed in these ways.

- **Division by $|G|$.** The ring must allow division by $|G|$. Over the integers the final polynomial has integer coefficients, but the intermediate sum is $|G|$ times it.
- **The whole group.** As in Burnside's lemma, the sum is over all of $G$. Summing over generators gives wrong numbers.
- **Colors are not permuted.** The theorem treats a group that acts on positions only. When the symmetries may also swap colors (for example, a black and white swap), one needs de Bruijn's extension of the method, which uses the cycle index of the color group as well.

## History

Redfield published the cycle index, under the name group reduction function, in 1927, and the paper went almost unnoticed. Pólya found the method independently and published it in 1937, with applications to chemical compounds, trees and graphs. Harary and Palmer used it as the basis of their book on graphical enumeration in 1973.

## References
