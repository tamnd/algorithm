---
tag: XBG4Z9
kind: technique
slug: bijective-proof
name: Bijective proof
aliases:
- combinatorial proof
- proof by bijection
area: combinatorics/counting-algorithms
level: intro
summary: Proves a counting identity by exhibiting a bijection between two sets.
prereqs: [rule-of-sum, rule-of-product]
see_also: [double-counting, stars-and-bars, catalan-numbers, prufer-sequence, euler-partition-theorem, combinatorial-ranking-and-unranking, conjugate-partition]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, What Is Enumerative Combinatorics? (Section 1.1, How to count, on bijective proofs; the partition identities later in the chapter)
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: Chapter Cayley's formula for the number of trees (the bijective proofs)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2 and Chapter 3 (ranking and unranking as bijections with an interval of integers, and the section on labeled trees and Prüfer codes in Chapter 3)
---

A bijective proof shows that two finite sets have the same size by giving a one-to-one correspondence between them: a map from the first set to the second and a map back, each the inverse of the other. If the size of one set is known, the proof counts the other. Bijective proofs explain *why* two counts agree, and each one is also an algorithm: it converts one kind of object into another. [Ranking and unranking](/combinatorial-ranking-and-unranking/), [Prüfer sequences](/prufer-sequence/) and the many equivalent forms of the [Catalan numbers](/catalan-numbers/) are bijective proofs used as code.

## In plain words

In a theater, every seat has one person and every person has one seat. Then the number of people equals the number of seats, and you know it without counting either group. A bijective proof does this with two sets of objects. It gives a rule that turns each object of the first kind into exactly one object of the second kind, and a rule that turns it back.

The proof must check four things: the rule always gives a valid object of the second kind, the rule back always gives a valid object of the first kind, and each rule undoes the other. Once these checks pass, the two sets have the same size, and often the rule is a useful program too.

## When it applies

- An identity says that two counts are equal, and each side has a direct meaning as a set of objects: subsets, paths, trees, strings, partitions.
- One set is easy to count (strings, subsets of a fixed size) and the other is not (trees, partitions with a condition).
- You need to convert between two encodings in a program: a tree and a sequence, a subset and an integer, a multiset and a set.
- An algebraic proof exists but does not explain the identity, and you want a proof that does.

## The template

Notation: $|S|$ is the size of a finite set $S$, $[n] = \{1, \ldots, n\}$, and $\binom{n}{k}$ is the [binomial coefficient](/binomial-coefficient/).

**Lemma.** Let $A$ and $B$ be finite sets, and let $f : A \to B$ and $g : B \to A$ satisfy $g(f(a)) = a$ for all $a \in A$ and $f(g(b)) = b$ for all $b \in B$. Then $f$ is a bijection and $|A| = |B|$.

*Proof.* If $f(a) = f(a')$, then $a = g(f(a)) = g(f(a')) = a'$, so $f$ is one to one. For $b \in B$, the element $a = g(b)$ has $f(a) = b$, so $f$ is onto. A bijection from $A$ onto $B$ composed with a bijection from $B$ onto $[|B|]$ is a bijection from $A$ onto $[|B|]$, so $|A| = |B|$ by the definition of size. $\square$

```pseudo id=main
BIJECTIVE-PROOF(A, B)
L1  define f(a) for each a in A                       ▷ hole: the forward rule
L2  prove f(a) ∈ B for each a in A                    ▷ f is well defined
L3  define g(b) for each b in B                       ▷ hole: the backward rule
L4  prove g(b) ∈ A for each b in B                    ▷ g is well defined
L5  prove g(f(a)) = a for each a in A
L6  prove f(g(b)) = b for each b in B
L7  conclude |A| = |B|
```

All of lines L2 and L4 to L6 are needed. Without line L6, the lemma gives only $|A| \le |B|$. A common shortcut is to prove only that $f$ is one to one and onto, or to give one map and an argument that it is one to one, plus a known equality of sizes; but with two explicit maps the proof also gives the algorithm in both directions.

## Classic examples

**1. Subsets and bit strings.** Map $S \subseteq [n]$ to the string $x_1 \cdots x_n$ with $x_i = 1$ if and only if $i \in S$, and map a string back to the set of positions of its 1s. The two maps are inverse, so $[n]$ has $2^n$ subsets. See [power set enumeration](/power-set-enumeration/).

**2. Symmetry.** The complement $S \mapsto [n] \setminus S$ maps $k$-subsets to $(n-k)$-subsets and is its own inverse, so $\binom{n}{k} = \binom{n}{n-k}$.

**3. Multisets and sets ([stars and bars](/stars-and-bars/)).** Map a multiset $a_1 \le a_2 \le \cdots \le a_k$ of elements of $[n]$ to the set $\{a_1, a_2 + 1, \ldots, a_k + k - 1\}$, a $k$-subset of $[n + k - 1]$, since the values are strictly increasing and the last is at most $n + k - 1$. Map $b_1 < \cdots < b_k$ back to $a_i = b_i - i + 1$, which is non-decreasing and in $[n]$. So there are $\binom{n+k-1}{k}$ multisets of size $k$. See [combinations with repetition](/combinations-with-repetition/).

**4. Compositions and subsets.** A composition $n = c_1 + \cdots + c_r$ into positive parts maps to the set of partial sums $\{c_1, c_1 + c_2, \ldots, c_1 + \cdots + c_{r-1}\} \subseteq [n-1]$. The differences of a sorted subset give the parts back. So $n \ge 1$ has $2^{n-1}$ compositions. See [counting integer compositions](/counting-integer-compositions/).

**5. Distinct parts and odd parts (Glaisher).** For $n \ge 1$, the partitions of $n$ into distinct parts are as many as the partitions into odd parts. Map an odd-part partition to a distinct-part one by merging two equal parts into one part of twice the size, until all parts differ. Map back by splitting each part $m 2^j$, with $m$ odd, into $2^j$ parts equal to $m$. Both maps keep the sum, and each part $m 2^j$ corresponds to bit $j$ of the number of parts equal to $m$, so the maps are inverse by the uniqueness of binary representation. For $n = 6$: $5{+}1 \mapsto 5{+}1$, $3{+}3 \mapsto 6$, $3{+}1{+}1{+}1 \mapsto 3{+}2{+}1$, $1{+}1{+}1{+}1{+}1{+}1 \mapsto 4{+}2$. See [Euler's partition theorem](/euler-partition-theorem/).

**6. Labeled trees and sequences (Prüfer).** For $n \ge 2$, remove the leaf with the smallest label and write down its neighbor, $n - 2$ times. This maps each labeled tree on $[n]$ to a sequence in $[n]^{n-2}$, and a reverse procedure rebuilds the tree. So there are $n^{n-2}$ trees, which is [Cayley's formula](/cayley-formula/). See [Prüfer sequence](/prufer-sequence/).

**7. Ranking.** A rank function is a bijection from a set of $N$ objects onto $\{0, \ldots, N - 1\}$, and its inverse is the unrank function. The [combinatorial number system](/combinatorial-number-system/) does this for $k$-subsets, and the [factorial number system](/factorial-number-system/) for permutations.

## Variations

- **Many to one.** If $f : A \to B$ is onto and each $b$ has exactly $d$ preimages, then $|A| = d\,|B|$. This is the division rule of the [rule of product](/rule-of-product/), and it counts necklaces, committees and circular orders.
- **Injections.** A one-to-one map $A \to B$ proves $|A| \le |B|$. Injections in both directions prove $|A| = |B|$ for finite sets.
- **Sign-reversing involutions.** To prove that a signed sum $\sum_{x \in X} \mathrm{sign}(x)$ equals $|F|$, give an involution on $X \setminus F$ that reverses signs, while all elements of $F$ are positive. The pairs cancel. This proves [inclusion-exclusion](/inclusion-exclusion-principle/) identities and the [Lindström, Gessel and Viennot lemma](/lindstrom-gessel-viennot-lemma/).
- **Bijections that carry a statistic.** A bijection that maps one statistic to another (inversions to the major index, the number of parts to the largest part, as with the [conjugate partition](/conjugate-partition/)) proves that two statistics have the same distribution.

## Pitfalls

- **An image outside the target.** In example 3, the map $a_i \mapsto a_i + i$ lands in $[n + k]$, not in $[n + k - 1]$, and the count comes out wrong. Check line L2 on the extreme objects.
- **One map only.** A map that is onto but not one to one gives only $|A| \ge |B|$. For Prüfer codes, the forward map alone does not show that every sequence is reached; the reverse procedure does.
- **The empty object.** Example 4 needs $n \ge 1$: the empty composition of 0 corresponds to no subset of $[-1]$. State the range of $n$ where the bijection holds.
- **Hidden choices.** A rule such as "pick an element of $S$" is not a function unless the element is named, for example the smallest one. Each rule must give one definite output.

## Exercises

1. For $n \ge 1$, give a bijection between the subsets of $[n]$ of even size and those of odd size, by toggling the element 1.
2. Give a bijection between the lattice paths from $(0, 0)$ to $(a, b)$ with unit steps right and up and the $a$-subsets of $[a + b]$.
3. Show that the number of partitions of $n$ with at most $k$ parts equals the number of partitions of $n$ with all parts at most $k$, by transposing the Young diagram.

## References
