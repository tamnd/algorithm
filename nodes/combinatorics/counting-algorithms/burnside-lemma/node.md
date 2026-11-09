---
tag: QNA5R4
kind: theorem
slug: burnside-lemma
name: Burnside's lemma
aliases:
- Cauchy-Frobenius lemma
- orbit-counting lemma
- not Burnside's lemma
area: combinatorics/counting-algorithms
level: advanced
summary: For a finite group acting on a finite set, the number of orbits equals the average number of points that a group element fixes.
prereqs: [finite-group, subgroup, lagranges-theorem-group-theory, double-counting]
see_also: [polya-enumeration-theorem, necklace-counting, necklace, symmetric-group, cyclic-group, automorphism-orbit, graph-automorphism-group, euler-totient]
sources:
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: Chapter 37, Pólya theory of counting (the orbit-counting lemma and its use for colorings)
  - book: isbn:9780123242457
    title: Frank Harary and Edgar M. Palmer, Graphical Enumeration, Academic Press, 1973
    locator: Chapter 2, Pólya's theorem (Burnside's lemma is the first step of the proof)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu (the count of necklaces, a special case of the lemma)
  - paper: "Peter M. Neumann, A lemma that is not Burnside's, The Mathematical Scientist 4, 133 to 141, 1979"
    title: Peter M. Neumann, A lemma that is not Burnside's
    locator: the whole article (the history of the lemma, from Cauchy 1845 and Frobenius 1887 to Burnside 1897)
---

Burnside's lemma counts the orbits of a [finite group](/finite-group/) $G$ that acts on a finite set $X$: the number of orbits is the average, over the elements $g \in G$, of the number of points of $X$ that $g$ fixes. It turns the count of objects "up to symmetry", such as necklaces up to rotation or graphs up to a renaming of the vertices, into a sum of counts of objects that one symmetry does not change, and those counts are often easy. The [Pólya enumeration theorem](/polya-enumeration-theorem/) is its refinement for colorings, and [necklace counting](/necklace-counting/) is its most common application.

## Statement

Notation: $X$ is a finite set, and $G$ is a finite group that acts on $X$. An action assigns to each $g \in G$ and $x \in X$ a point $g \cdot x \in X$ such that $e \cdot x = x$ for the identity $e$ and $g \cdot (h \cdot x) = (gh) \cdot x$ for all $g, h \in G$. The *orbit* of $x$ is $G \cdot x = \{g \cdot x : g \in G\}$. The orbits partition $X$, and $X/G$ denotes the set of orbits. For $g \in G$, the set of *fixed points* is $\mathrm{Fix}(g) = \{x \in X : g \cdot x = x\}$. For $x \in X$, the *stabilizer* is $G_x = \{g \in G : g \cdot x = x\}$.

**Theorem (Burnside's lemma).** Let a finite group $G$ act on a finite set $X$. Then

$$|X/G| = \frac{1}{|G|} \sum_{g \in G} |\mathrm{Fix}(g)|.$$

**Lemma (orbit-stabilizer).** For each $x \in X$, the stabilizer $G_x$ is a [subgroup](/subgroup/) of $G$, and $|G \cdot x| \cdot |G_x| = |G|$.

Two facts help when one applies the theorem.

- $|\mathrm{Fix}(g)|$ depends only on the conjugacy class of $g$, because $\mathrm{Fix}(hgh^{-1}) = h \cdot \mathrm{Fix}(g)$, and $x \mapsto h \cdot x$ is a bijection of $X$. So the sum can run over the conjugacy classes, each weighted by its size.
- If $X = C^D$ is the set of maps from a finite set $D$ to a set $C$ of $k$ colors, and $G$ acts on $D$ by permutations, with $(g \cdot f)(d) = f(g^{-1} d)$, then a coloring $f$ is fixed by $g$ exactly when $f$ is constant on each cycle of $g$. So $|\mathrm{Fix}(g)| = k^{c(g)}$, where $c(g)$ is the number of cycles of $g$ on $D$, counting fixed points as cycles of length 1.

## In plain words

Many counting questions ask how many objects there are when you treat two objects as the same if a symmetry turns one into the other. A bracelet that you can turn is one example: turning it does not give a new bracelet.

Counting these classes directly is hard, because a class can hold many objects or only a few. The lemma gives a way around this. Take each symmetry in turn and count the objects that it leaves exactly as they are. Add these counts, and divide by the number of symmetries. The result is the number of classes.

The reason is that each class gets exactly one unit of weight in total, however large or small the class is. A large class has many objects, but each of its objects is left unchanged by only a few symmetries.

## Proof

*Proof of the orbit-stabilizer lemma.* The identity fixes $x$, and if $g, h \in G_x$ then $(gh) \cdot x = g \cdot (h \cdot x) = x$ and $g^{-1} \cdot x = g^{-1} \cdot (g \cdot x) = e \cdot x = x$, so $G_x$ is a subgroup. Define a map $\Phi$ from the set of left cosets of $G_x$ to the orbit $G \cdot x$ by $\Phi(g G_x) = g \cdot x$. It is well defined and injective: $g \cdot x = h \cdot x$ holds if and only if $(h^{-1} g) \cdot x = x$, that is, $h^{-1} g \in G_x$, that is, $g G_x = h G_x$. It is surjective by the definition of the orbit. So $|G \cdot x|$ equals the number of left cosets of $G_x$, which is $|G| / |G_x|$ by [Lagrange's theorem](/lagranges-theorem-group-theory/). $\square$

*Proof of the theorem.* Let $F = \{(g, x) \in G \times X : g \cdot x = x\}$. Count $F$ in two ways, by [double counting](/double-counting/). Group the pairs by $g$: the pairs with first entry $g$ are the pairs $(g, x)$ with $x \in \mathrm{Fix}(g)$, so $|F| = \sum_{g \in G} |\mathrm{Fix}(g)|$. Group the pairs by $x$: the pairs with second entry $x$ are the pairs $(g, x)$ with $g \in G_x$, so $|F| = \sum_{x \in X} |G_x|$. By the lemma, $|G_x| = |G| / |G \cdot x|$. Hence

$$\sum_{g \in G} |\mathrm{Fix}(g)| = |G| \sum_{x \in X} \frac{1}{|G \cdot x|} = |G| \sum_{O \in X/G} \sum_{x \in O} \frac{1}{|O|} = |G| \sum_{O \in X/G} 1 = |G| \cdot |X/G|.$$

The second equality groups the points of $X$ by their orbit, which is allowed because the orbits partition $X$, and uses $G \cdot x = O$ for each $x \in O$. Divide by $|G| \ge 1$. $\blacksquare$

*Proof of the two facts.* If $g \cdot x = x$, then $(hgh^{-1}) \cdot (h \cdot x) = h \cdot (g \cdot x) = h \cdot x$, so $h \cdot \mathrm{Fix}(g) \subseteq \mathrm{Fix}(hgh^{-1})$. The same argument with $h^{-1}$ and $hgh^{-1}$ in place of $h$ and $g$ gives the reverse inclusion. For colorings, $g \cdot f = f$ means $f(g^{-1} d) = f(d)$ for all $d$, which holds if and only if $f$ takes one value on each cycle of $g$. Choose one of the $k$ colors for each of the $c(g)$ cycles independently, by the [rule of product](/rule-of-product/). $\square$

## Consequences

### Worked examples

**Necklaces of length 4 with 2 colors, up to rotation.** The group is the [cyclic group](/cyclic-group/) of the four rotations of a square, acting on the $2^4 = 16$ colorings of its corners.

| rotation | cycles on the corners | fixed colorings |
|---|---|---|
| by 0 | 4 | $2^4 = 16$ |
| by 1 | 1 | $2^1 = 2$ |
| by 2 | 2 | $2^2 = 4$ |
| by 3 | 1 | $2^1 = 2$ |

The sum is 24, and $24 / 4 = 6$. The six necklaces are 0000, 0001, 0011, 0101, 0111 and 1111. The orbits have sizes 1, 4, 4, 2, 4 and 1, which shows that orbits of different sizes all count once. The general count, $\frac{1}{n}\sum_{d \mid n} \varphi(d) k^{n/d}$, is on the [necklace counting](/necklace-counting/) page.

**The faces of a cube with $k$ colors, up to rotation.** The rotation group of the cube has 24 elements. They fall into five conjugacy classes:

| class | size | cycles on the 6 faces | fixed colorings |
|---|---|---|---|
| identity | 1 | 6 | $k^6$ |
| a quarter turn about a face axis | 6 | 3 | $k^3$ |
| a half turn about a face axis | 3 | 4 | $k^4$ |
| a third turn about a vertex axis | 8 | 2 | $k^2$ |
| a half turn about an edge axis | 6 | 3 | $k^3$ |

So the number of colorings up to rotation is $(k^6 + 3k^4 + 12k^3 + 8k^2)/24$. For $k = 0, 1, 2, \ldots, 7$ this gives 0, 1, 10, 57, 240, 800, 2226, 5390 (OEIS A047780). For two colors, black and white, the 10 classes are: no black face, one black face, two adjacent, two opposite, three around a corner, three in a band, and the complements of the first four.

### Where the lemma is used

- **Counting under symmetry.** Each count of objects up to a symmetry group is an orbit count. This covers [necklaces and bracelets](/necklace-counting/), colorings of the faces or edges of a solid, unlabeled graphs (the action of the [symmetric group](/symmetric-group/) on the possible edges), and binary matrices up to row and column permutations.
- **The Pólya enumeration theorem.** The [Pólya enumeration theorem](/polya-enumeration-theorem/) applies a weighted form of the lemma to colorings, and it counts the orbits of each color content at once through the cycle index.
- **Computation.** The lemma gives an algorithm whose cost is the cost of listing the conjugacy classes of $G$ with their sizes, plus one fixed-point count per class. For the cyclic group of order $n$, there is one class for each divisor $d$ of $n$, with $\varphi(d)$ elements, where $\varphi$ is the [Euler totient](/euler-totient/). So the count of necklaces takes a number of big-integer operations equal to the number of divisors of $n$, not $n$, and not the number $k^n$ of colorings.
- **Orbits of a graph.** The number of orbits of the [automorphism group](/graph-automorphism-group/) of a graph on its vertices is the average number of fixed vertices of an automorphism. Programs that find [automorphism orbits](/automorphism-orbit/) list them directly, but the lemma checks the count.

## Tightness

The formula is an identity, so there is nothing to sharpen, but each hypothesis matters.

- **Finiteness.** For an infinite group or set, the average is not defined. The integers acting on themselves by translation have one orbit, while each element other than $0$ fixes no point.
- **A group, not a set of moves.** Average the fixed counts over only the identity and the rotation by 1 of the first example: $(16 + 2)/2 = 9$, not 6. The lemma needs the whole group. The rotations by 2 and 3 are products of the rotation by 1 with itself, so they must be in the average.
- **Fixed points, not fixed orbits.** One counts points $x$ with $g \cdot x = x$ exactly. A coloring that $g$ maps to a coloring in the same orbit is not a fixed point unless it maps to itself.

## History

The lemma is older than its name. Peter Neumann showed in 1979 that Cauchy knew it in 1845 and that Frobenius published it in 1887. Burnside gave it in his book on finite groups in 1897, with credit to Frobenius, and the name "Burnside's lemma" stuck through later books. For this reason it is also called the Cauchy-Frobenius lemma, and some authors call it "the lemma that is not Burnside's". Redfield in 1927 and Pólya in 1937 built the cycle index method on it.

## References
