---
tag: 2V9QXK
kind: technique
slug: double-counting
name: Double counting
aliases:
- counting in two ways
area: combinatorics/counting-algorithms
level: intro
summary: Count one set of pairs in two ways and equate the results.
prereqs: [rule-of-sum, rule-of-product]
see_also: [bijective-proof, handshaking-lemma, binomial-coefficient, totient-divisor-sum, cayley-formula, burnside-lemma, linearity-of-expectation, pigeonhole-principle]
sources:
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: Chapter Pigeon-hole and double counting, and Chapter Cayley's formula for the number of trees (the double counting proof of Pitman)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 2.4, Multiple Sums (interchanging the order of summation)
  - book: isbn:9780073383095
    title: Kenneth H. Rosen, Discrete Mathematics and Its Applications, seventh edition
    locator: Section 6.4, Binomial Coefficients and Identities (combinatorial proofs by counting in two ways)
---

Double counting proves an equation by counting one finite set in two different ways: both expressions equal the size of the set, so they are equal. Most often the set is a set of pairs $(a, b)$ with $a$ related to $b$, counted once by grouping on $a$ and once by grouping on $b$. It gives the [handshaking lemma](/handshaking-lemma/), most identities of the [binomial coefficient](/binomial-coefficient/), the [divisor sum of the totient](/totient-divisor-sum/), [Burnside's lemma](/burnside-lemma/) and a short proof of [Cayley's formula](/cayley-formula/). In the analysis of algorithms it is the step "charge the work to the edges instead of to the vertices".

## In plain words

A class has some students and some clubs. You want the total number of club memberships. You can ask each student how many clubs they are in and add the answers. Or you can ask each club how many members it has and add those answers. Both sums count the same memberships, so they are equal.

That is the method. You pick a set that is easy to describe, often a set of pairs, and you count it twice by grouping it in two ways. One side of the equation comes from one grouping and the other side from the other. When one of the two counts is easy, the equation tells you something new about the other.

## When it applies

- The quantity you want is a sum over one kind of object of "how many objects of a second kind are related to it": degrees, sizes of subsets, numbers of divisors, numbers of fixed points.
- Grouping the same pairs by the second kind gives a sum that is easier, or that is already known.
- An identity has a product such as $k \binom{n}{k}$ on one side. A product of two counts often counts pairs, which suggests the set to count.
- The cost of an algorithm is a double sum, and swapping the order of the sums makes it simple.

## The template

Notation: $|S|$ is the size of a finite set $S$, and $[n] = \{1, \ldots, n\}$.

**Lemma (double counting).** Let $A$ and $B$ be finite sets and $R \subseteq A \times B$. For $a \in A$ let $r(a) = |\{b : (a, b) \in R\}|$, and for $b \in B$ let $c(b) = |\{a : (a, b) \in R\}|$. Then

$$\sum_{a \in A} r(a) = |R| = \sum_{b \in B} c(b).$$

*Proof.* The sets $R_a = \{(a, b) \in R\}$ for $a \in A$ are disjoint and their union is $R$, because each pair has one first coordinate. So $|R| = \sum_a |R_a| = \sum_a r(a)$ by the [rule of sum](/rule-of-sum/). Grouping by the second coordinate gives the other sum in the same way. $\square$

In matrix form: the 0-1 matrix $M$ with $M_{ab} = [(a, b) \in R]$ has row sums $r(a)$ and column sums $c(b)$, and the sum of all its entries is the sum of the row sums and also the sum of the column sums. With real entries $M_{ab}$ in place of 0 and 1, the same proof gives $\sum_a \sum_b M_{ab} = \sum_b \sum_a M_{ab}$, which is the interchange of a finite double sum.

```pseudo id=main
DOUBLE-COUNT(question)
L1  choose a finite set R, often of pairs (a, b) with a related to b    ▷ hole: what to count
L2  group R by the first part:  |R| = Σ over a of r(a)                  ▷ hole: count each group
L3  group R by the second part: |R| = Σ over b of c(b)                  ▷ hole: count each group
L4  equate the two sums, and simplify
```

The skill is in line L1. Choose $R$ so that one grouping gives the expression you want to know, and the other grouping gives something easy. When all $r(a)$ are equal to $r$ and all $c(b)$ are equal to $c$, line L4 reads $|A|\,r = |B|\,c$, which is the division rule of the [rule of product](/rule-of-product/).

## Classic examples

**1. The handshaking lemma.** In a graph $G = (V, E)$, count the pairs $(v, e)$ with $v$ an end of $e$. By vertices this is $\sum_v \deg(v)$; by edges it is $2|E|$, since each edge has two ends. So $\sum_v \deg(v) = 2|E|$, and the number of vertices of odd degree is even. The same count shows that a scan of all adjacency lists takes $\Theta(|V| + |E|)$ time, the bound of BFS and DFS. See the [handshaking lemma](/handshaking-lemma/).

**2. The absorption identity.** Count the pairs $(S, x)$ with $S \subseteq [n]$, $|S| = k$ and $x \in S$. Choosing $S$ first gives $k \binom{n}{k}$. Choosing $x$ first, then the other $k - 1$ elements from $[n] \setminus \{x\}$, gives $n \binom{n-1}{k-1}$. So $k \binom{n}{k} = n \binom{n-1}{k-1}$; for $n = 6$, $k = 4$ both sides are 60. Summing over $k$ gives $\sum_{k} k \binom{n}{k} = n 2^{n-1}$, the total size of all subsets of $[n]$.

**3. The average number of divisors.** Count the pairs $(d, m)$ with $1 \le m \le N$ and $d \mid m$. By $m$, this is $\sum_{m \le N} \tau(m)$, where $\tau$ is the [divisor function](/divisor-function/). By $d$, each $d$ divides $\lfloor N/d \rfloor$ numbers up to $N$. So

$$\sum_{m=1}^{N} \tau(m) = \sum_{d=1}^{N} \Bigl\lfloor \frac{N}{d} \Bigr\rfloor,$$

which is 27 for $N = 10$. The right side is $N \ln N + O(N)$ by the [harmonic series](/harmonic-series/), so a number up to $N$ has about $\ln N$ divisors on average. The same count bounds a sieve that loops over all multiples of each $d$ by $O(N \log N)$.

**4. The totient sum.** Count the fractions $j/n$ for $j \in [n]$, each written in lowest terms as $a/d$ with $d \mid n$ and $\gcd(a, d) = 1$. Each $d \mid n$ is the denominator of exactly $\varphi(d)$ of them, where $\varphi$ is [Euler's totient](/euler-totient/). So $\sum_{d \mid n} \varphi(d) = n$. For $n = 12$: $1 + 1 + 2 + 2 + 2 + 4 = 12$. See [totient divisor sum](/totient-divisor-sum/).

**5. Burnside's lemma.** A finite group $G$ acts on a finite set $X$. Count the pairs $(g, x)$ with $g \cdot x = x$. By $g$ this is $\sum_g |\mathrm{Fix}(g)|$. By $x$ it is $\sum_x |G_x|$, and $|G_x| = |G| / |G \cdot x|$ by the orbit-stabilizer theorem, so the sum is $|G|$ times the number of orbits. See [Burnside's lemma](/burnside-lemma/) and [necklace counting](/necklace-counting/).

**6. Cayley's formula (Pitman).** Let $T_n$ be the number of labeled trees on $[n]$. Count the sequences of $n - 1$ directed edges that build a rooted tree from $n$ isolated rooted vertices, where each step adds an edge from any vertex $v$ to the root of another tree. Starting from the tree: there are $n T_n$ rooted trees and $(n-1)!$ orders of their edges, so $n T_n (n-1)!$ sequences. Building forward: after $k$ steps there are $n - k$ trees, and step $k + 1$ has $n(n - k - 1)$ choices (any vertex, and the root of a tree that does not hold it), so the count is $\prod_{k=0}^{n-2} n(n-k-1) = n^{n-1}(n-1)!$. So $T_n = n^{n-2}$. See [Cayley's formula](/cayley-formula/).

## Variations

- **Weighted pairs.** Put a weight $w(a, b)$ on each pair and sum it in two orders. With probabilities as weights, this is [linearity of expectation](/linearity-of-expectation/) for a sum of indicator variables: the expected number of objects with a property is the sum of the probabilities.
- **Interchanging sums with dependent limits.** $\sum_{i=1}^{n} \sum_{j=i}^{n} a_{ij} = \sum_{j=1}^{n} \sum_{i=1}^{j} a_{ij}$, since both sides sum $a_{ij}$ over the pairs $1 \le i \le j \le n$. Concrete Mathematics (Section 2.4) treats this rule in detail.
- **Inequalities.** If one grouping is only bounded, the equation becomes an inequality. The LYM inequality for an antichain $\mathcal F$ of subsets of $[n]$ counts pairs (maximal chain, member of $\mathcal F$ on it): each chain meets $\mathcal F$ at most once, and a set of size $k$ lies on $k!(n-k)!$ chains, so $\sum_{F \in \mathcal F} 1/\binom{n}{|F|} \le 1$.
- **Bijective proofs.** When the two counts are of two different sets, a [bijection](/bijective-proof/) between them replaces the common set $R$.

## Pitfalls

- **Ordered and unordered pairs.** In the handshaking lemma, each edge is counted from both ends. Writing $\sum_v \deg(v) = |E|$ forgets that the pairs are (vertex, edge) and not edges.
- **Two different sets.** The two sides must count exactly the same set. In example 2, $(S, x)$ with $x \in S$ is not the same as $(S, x)$ with $x \notin S$; the second set gives $(n - k)\binom{n}{k} = n \binom{n-1}{k}$, a different identity.
- **Wrong limits after a swap.** $\sum_{i=1}^{n} \sum_{j=i}^{n}$ becomes $\sum_{j=1}^{n} \sum_{i=1}^{j}$, not $\sum_{j=1}^{n} \sum_{i=j}^{n}$. Write the set of index pairs first, then read off the new limits.
- **Infinite sets.** For infinite sums, the order of summation may change the value unless the terms are nonnegative or the sum converges absolutely.

## Exercises

1. Show that $\sum_{k=0}^{n} k(k-1)\binom{n}{k} = n(n-1)2^{n-2}$ for $n \ge 2$, by counting pairs (subset, ordered pair of distinct elements in it).
2. A graph has $n$ vertices, all of degree $d$. Show that $nd$ is even, and that the graph has $nd/2$ edges.
3. Show that the number of pairs $(x, y) \in [N]^2$ with $x \mid y$ is at most $N(1 + \ln N)$.

## References
