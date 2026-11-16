---
tag: A2AF8J
kind: technique
slug: fooling-set-method
name: Fooling set method
aliases:
- fooling set argument
- fooling set lower bound
area: complexity/communication-and-query-complexity
level: advanced
summary: A lower bound on deterministic and nondeterministic communication. A set of inputs with the same value, no two of which fit in one monochromatic rectangle, forces at least that many protocol leaves.
prereqs: [deterministic-communication-complexity, communication-matrix]
see_also: [log-rank-lower-bound, nondeterministic-communication-complexity, equality-problem, greater-than-problem, disjointness-problem, discrepancy-method, corruption-bound, adversary-argument]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1, Basics (Section 1.3, Fooling Sets and Rectangle Size), and Chapter 2 (Section 2.1, Covers and Nondeterminism)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 1, Deterministic Protocols (section Lower Bounds)
---

The fooling set method proves lower bounds on the [deterministic communication complexity](/deterministic-communication-complexity/) $D^{cc}(f)$ of a two-party function. It finds a set $S$ of input pairs on which $f$ has the same value $z$, chosen so that no two pairs can share one $z$-rectangle of the [communication matrix](/communication-matrix/). Each pair then needs its own leaf in any protocol tree, so $D^{cc}(f) \ge \log_2 |S|$, and the same bound holds for the nondeterministic cost. The method measures the number of monochromatic rectangles; it differs from the [log-rank lower bound](/log-rank-lower-bound/), which measures the rank of $M_f$, and from the [discrepancy method](/discrepancy-method/) and the [corruption bound](/corruption-bound/), which bound randomized protocols.

## In plain words

A protocol with a short talk has only a few possible endings. All the inputs that end the same way must get the same answer, and they have a special shape: if Alice's input from one of them and Bob's input from another one both lead to this ending, then the mixed pair leads there too.

A fooling set is a list of input pairs, all with the same answer, chosen so that mixing any two of them gives a pair with a different answer. Then no two pairs in the list can share an ending. A wrong answer would follow for the mixed pair.

So the protocol needs at least as many endings as the list has pairs. A talk of a given length has a limited number of endings, which gives a lower bound on the length of the talk.

## When it applies

Use it for a lower bound on $D^{cc}(f)$ or on the nondeterministic cost $N^z(f)$, when you can name many inputs with the same value $z$ that "cross" badly. It works best when $f$ has a large set of value-$z$ entries in which the mixed pairs $(x_i, y_j)$ have a different value, as on the diagonal of equality. It needs no algebra and gives exact constants, often the bound $n + 1$.

It does not apply to randomized protocols. Equality has a fooling set of size $2^n$, yet its public-coin randomized cost is $O(1)$. It also cannot beat the rank bound by much: a fooling set has at most $\operatorname{rank}(M_f)^2$ pairs, as shown under "Variations".

## The template

The **fooling set** condition. A set $S = \{(x_1, y_1), \ldots, (x_s, y_s)\} \subseteq X \times Y$ is a $z$-fooling set for $f$ if $f(x_i, y_i) = z$ for every $i$, and for every $i \ne j$,

$$f(x_i, y_j) \ne z \quad \text{or} \quad f(x_j, y_i) \ne z.$$

**Why it works.** Suppose two pairs $(x_i, y_i)$ and $(x_j, y_j)$ of $S$ reach the same leaf $\ell$. The inputs at $\ell$ form a rectangle $A \times B$, so $x_i, x_j \in A$ and $y_i, y_j \in B$. Then $(x_i, y_j)$ and $(x_j, y_i)$ also reach $\ell$, and the protocol outputs $z$ on both. One of them has a value other than $z$, so the protocol errs. Hence the $s$ pairs reach $s$ different leaves with output $z$.

```pseudo id=main
FOOLING-SET-BOUND(f)
L1  choose the output value ⟨z⟩
L2  choose the pairs ⟨S⟩ = {(x_1, y_1), ..., (x_s, y_s)} with f(x_i, y_i) = z for every i
L3  for every i ≠ j, prove f(x_i, y_j) ≠ z or f(x_j, y_i) ≠ z      ▷ ⟨cross argument⟩
L4  conclude: every protocol for f has at least s leaves with output z
L5  add ⟨the other leaves⟩: at least one leaf for each other value of f
L6  return D^cc(f) ≥ ⌈log2(total number of leaves)⌉
```

The holes are the value $\langle z \rangle$, the set $\langle S \rangle$, the $\langle$cross argument$\rangle$ that two pairs never fit in one $z$-rectangle, and $\langle$the other leaves$\rangle$, which is often a second fooling set for another value. A binary tree with $L$ leaves has depth at least $\lceil \log_2 L \rceil$, which gives line L6.

## Classic examples

All examples have $X = Y = \{0,1\}^n$. Each one fills the holes of the template.

**Equality.** $\langle z \rangle = 1$ and $\langle S \rangle = \{(x, x) : x \in \{0,1\}^n\}$, of size $2^n$. Cross argument: for $x \ne x'$, $\mathrm{EQ}(x, x') = 0$. Other leaves: $\mathrm{EQ}$ takes the value 0, so at least one more leaf. Total $2^n + 1$ leaves, so $D^{cc}(\mathrm{EQ}) \ge n + 1$, which matches the trivial protocol. See the [equality problem](/equality-problem/).

**Greater-than.** $\mathrm{GT}(x, y) = 1$ when $x > y$ as numbers in $\{0, \ldots, 2^n - 1\}$. Fill $\langle z \rangle = 1$ with $S_1 = \{(x, x - 1) : 1 \le x \le 2^n - 1\}$. Cross argument: for $x < x'$, the pair $(x, x' - 1)$ has $x \le x' - 1$, so $\mathrm{GT} = 0$. For the other leaves, use the 0-fooling set $S_0 = \{(x, x)\}$: for $x < x'$, $\mathrm{GT}(x', x) = 1$. Total $(2^n - 1) + 2^n = 2^{n+1} - 1$ leaves, and $\lceil \log_2(2^{n+1} - 1) \rceil = n + 1$. See the [greater-than problem](/greater-than-problem/).

**Disjointness.** Read $x$ and $y$ as subsets of $\{1, \ldots, n\}$. Fill $\langle z \rangle = 1$ (the sets are disjoint) with $S = \{(A, \bar{A}) : A \subseteq \{1, \ldots, n\}\}$, where $\bar{A}$ is the complement. Cross argument: for $A \ne B$, there is an element in $A \setminus B$ or in $B \setminus A$. In the first case $A \cap \bar{B} \ne \emptyset$; in the second, $B \cap \bar{A} \ne \emptyset$. Adding one 0-leaf gives $D^{cc}(\mathrm{DISJ}) \ge n + 1$. See the [disjointness problem](/disjointness-problem/).

**Nondeterministic equality.** The same diagonal set shows that every cover of the 1-entries of $M_{\mathrm{EQ}}$ by 1-rectangles has $2^n$ rectangles, so the nondeterministic cost of equality is $N^1(\mathrm{EQ}) = n$. See [nondeterministic communication complexity](/nondeterministic-communication-complexity/).

These bounds agree with an exhaustive search over all protocol trees for $n = 1, 2, 3$, which gives $D^{cc} = n + 1$ for equality, greater-than and disjointness.

## Variations

- **Two values at once.** As in line L5, a $1$-fooling set $S_1$ and a $0$-fooling set $S_0$ give $D^{cc}(f) \ge \lceil \log_2(|S_1| + |S_0|) \rceil$. This one extra bit is the difference between $n$ and $n + 1$.
- **Covers and nondeterminism.** The proof never uses that the rectangles are disjoint, only that each one is $z$-monochromatic. So a $z$-fooling set of size $s$ shows that every cover of the $z$-entries needs $s$ rectangles, and $N^z(f) \ge \log_2 s$.
- **Rectangle size.** Put a probability distribution $\mu$ on the $z$-entries. If every $z$-rectangle has $\mu$-weight at most $\delta$, then at least $1/\delta$ rectangles are needed. A fooling set is the case of the uniform distribution on $S$ with $\delta = 1/|S|$. This weighted form is the step from fooling sets toward the [corruption bound](/corruption-bound/), which allows a few errors in each rectangle.
- **Limit against rank.** Let $S$ be a 1-fooling set of size $s$, and let $N$ be the $s \times s$ submatrix of $M_f$ on the rows $x_1, \ldots, x_s$ and the columns $y_1, \ldots, y_s$. The entrywise product $N \circ N^{\mathsf T}$ has 1 on the diagonal and $f(x_i, y_j) f(x_j, y_i) = 0$ off it, so it is the identity $I_s$. Since the rank of an entrywise product is at most the product of the ranks, $s \le \operatorname{rank}(N)^2 \le \operatorname{rank}(M_f)^2$, over any field. So the fooling set bound is at most about twice the [log-rank bound](/log-rank-lower-bound/). Dietzfelbinger, Hromkovič and Schnitger (1996) proved this comparison. The rank bound can be much larger. The inner product function has real rank $2^n - 1$, but over $\mathrm{GF}(2)$ its matrix has rank $n$, so every 1-fooling set for it has at most $n^2$ pairs. The rank bound gives about $n$ bits for inner product, and fooling sets give only $O(\log n)$.

## Pitfalls

- The condition is "or", not "and": one of the two mixed pairs must have a different value. Asking for both is too strong and misses good sets, as in greater-than, where $\mathrm{GT}(x', x) = 1$ but $\mathrm{GT}(x, x') = 0$ for $x < x'$.
- All pairs in $S$ must have the same value. A set that mixes 1-entries and 0-entries is not a fooling set, even if no two pairs fit in one monochromatic rectangle; count each value with its own set, as in line L5.
- A fooling set of size $2^n$ gives $D^{cc}(f) \ge n$, not $n + 1$. The extra bit needs the leaves of the other value.
- The bound is for deterministic and nondeterministic protocols. It says nothing about randomized protocols, which may put two fooling pairs in one leaf and accept a small error.
## Exercises

1. Let $f(x, y) = 1$ when $x \subseteq y$, reading $x$ and $y$ as subsets of $\{1, \ldots, n\}$. Show that $\{(A, A)\}$ is a 1-fooling set and that $D^{cc}(f) = n + 1$.
2. Show that the non-equality function $\mathrm{NE} = 1 - \mathrm{EQ}$ has $D^{cc}(\mathrm{NE}) = n + 1$, but that its 1-entries can be covered by $2n$ rectangles. Which bound does the fooling set method give for $N^1(\mathrm{NE})$?
3. Prove that $\operatorname{rank}(A \circ B) \le \operatorname{rank}(A) \operatorname{rank}(B)$, by showing that $A \circ B$ is a submatrix of the Kronecker product $A \otimes B$.
4. Show that every 0-fooling set of the inner product function has at most $(n+1)^2$ pairs. Hint: $J - M_{\mathrm{IP}}$ has rank at most $n + 1$ over $\mathrm{GF}(2)$.
5. The public-coin protocol for equality with three bits has error $1/4$. Explain which step of "Why it works" fails for it.

## References
