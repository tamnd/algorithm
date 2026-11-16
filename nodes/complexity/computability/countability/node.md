---
tag: 8698TB
kind: concept
slug: countability
name: Countability
aliases:
- countable set
- enumerable set
area: complexity/computability
level: intro
summary: A set is countable if it is finite or can be listed as a sequence indexed by the natural numbers. Machines are countable and languages are not, so most languages are undecidable.
prereqs: [alphabet]
see_also: [diagonalization-argument, godel-numbering, undecidability, recursively-enumerable-language, counting-argument, decidable-language, computable-function, computable-real-numbers]
sources:
  - paper: doi:10.1515/crll.1874.77.258
    title: Georg Cantor, Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen, Journal für die reine und angewandte Mathematik 77 (1874)
    locator: pp. 258 to 262 (the algebraic numbers are countable and the real numbers are not)
  - title: Georg Cantor, Über eine elementare Frage der Mannigfaltigkeitslehre, Jahresbericht der Deutschen Mathematiker-Vereinigung 1 (1891)
    locator: pp. 75 to 78 (the diagonal argument, and the theorem that a set has smaller cardinality than its power set)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.2, Undecidability (the diagonalization method, and the corollary that some languages are not Turing-recognizable)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.1 (enumerating the binary strings and the codes of Turing machines)
---

A set is *countable* if it is finite or if its elements can be listed as a sequence $s_0, s_1, s_2, \ldots$ indexed by the natural numbers. A set that is not countable is *uncountable*. In computability the idea gives the first and simplest proof that undecidable problems exist: there are only countably many [Turing machines](/turing-machine/), but uncountably many languages, so most languages have no machine that decides them. Countability says only that *some* listing exists; it does not ask for a listing that a machine can produce, which is the stronger notion of a [computably enumerable](/recursively-enumerable-language/) set.

## In plain words

A collection is countable if you can give its members the numbers zero, one, two and so on, so that every member gets a number. The whole numbers are countable. So are all words over a fixed alphabet: list the short words first, and the words of the same length in dictionary order. Every program is a word, so all programs are countable too.

Some collections are too big for any such list. The classic one is the collection of all infinite sequences of zeros and ones. For any list, you can build a sequence that differs from the first one in its first place, from the second one in its second place, and so on. That sequence is not in your list.

A problem with yes and no answers on words is one such infinite sequence. So there are more problems than programs, and some problems have no program.

## The idea

### Definition

Let $\mathbb{N} = \{0, 1, 2, \ldots\}$. For a set $S$ the following are equivalent, and $S$ is *countable* when they hold:

1. there is an injective map $f : S \to \mathbb{N}$;
2. $S$ is empty, or there is a surjective map $g : \mathbb{N} \to S$;
3. $S$ is finite, or there is a bijection $h : \mathbb{N} \to S$.

A set with a bijection to $\mathbb{N}$ is *countably infinite*. Some books use "countable" for "countably infinite" only; this page includes the finite sets.

*Proof of the equivalence.* (3) implies (2): a finite nonempty set $\{s_0, \ldots, s_{k-1}\}$ is the image of $g(n) = s_{\min(n, k-1)}$, and a bijection is a surjection. (2) implies (1): for a surjection $g$, let $f(s)$ be the least $n$ with $g(n) = s$. This least $n$ exists because $\mathbb{N}$ has no infinite descending chain, and different $s$ get different $n$, so $f$ is injective. (1) implies (3): the image $f(S)$ is a subset of $\mathbb{N}$. If it is finite, so is $S$. If it is infinite, list its elements in increasing order as $a_0 < a_1 < \cdots$; then $h(n) = f^{-1}(a_n)$ is a bijection from $\mathbb{N}$ to $S$. $\square$

### Closure

- Every subset of a countable set is countable: restrict the injection.
- $\mathbb{N} \times \mathbb{N}$ is countable. The *Cantor pairing function* $\pi(x, y) = \tfrac{1}{2}(x + y)(x + y + 1) + y$ is a bijection from $\mathbb{N} \times \mathbb{N}$ to $\mathbb{N}$. It lists the pairs by the diagonals $x + y = 0, 1, 2, \ldots$: the diagonal $x + y = d$ has $d + 1$ pairs, and the $\tfrac{1}{2} d (d + 1)$ pairs of the earlier diagonals come before it. By induction, $\mathbb{N}^k$ is countable for each $k$.
- A countable union of countable sets is countable, when a listing of each set is given. Drop the empty sets; then the map that sends $\pi(i, j)$ to the $j$-th element of the $i$-th set is a surjection from $\mathbb{N}$ onto the union, and (2) applies. In computability the listings are always given explicitly, so no choice principle is needed.
- For a finite [alphabet](/alphabet/) $\Sigma$, the set $\Sigma^*$ of all finite words is countable. The *shortlex order* lists the words by length, and the words of one length in alphabetical order. For $\Sigma = \{0, 1\}$ the word $w$ gets the index $2^{|w|} - 1 + \mathrm{val}(w)$, where $\mathrm{val}(w)$ is the value of $w$ read in binary and $\mathrm{val}(\varepsilon) = 0$.
- So every set of finite objects that can be written as words is countable: the rational numbers, the finite subsets of $\mathbb{N}$, the finite graphs, the formulas of a logic, and the Turing machines, each through a fixed [encoding](/godel-numbering/) $\langle M \rangle \in \{0, 1\}^*$.

### Uncountable sets

**Theorem (Cantor 1891).** For every set $S$, no map $f : S \to \mathcal{P}(S)$ is surjective. In particular the power set $\mathcal{P}(\mathbb{N})$ and the set $\{0, 1\}^{\mathbb{N}}$ of infinite binary sequences are uncountable.

*Proof.* Let $D = \{ s \in S : s \notin f(s) \}$. If $D = f(t)$ for some $t \in S$, then $t \in D$ holds if and only if $t \notin f(t) = D$, a contradiction. So $D$ is not in the image of $f$. For $S = \mathbb{N}$, a surjection $g : \mathbb{N} \to \mathcal{P}(\mathbb{N})$ would be such a map, so none exists, and $\mathcal{P}(\mathbb{N})$ is not countable by (2). A set $A \subseteq \mathbb{N}$ and its characteristic sequence are the same object, so $\{0,1\}^{\mathbb{N}}$ is uncountable too. $\square$

This is the [diagonalization argument](/diagonalization-argument/). The real numbers are uncountable as well. Cantor first proved this in 1874 by nested intervals, and gave the diagonal proof in 1891.

### Machines against languages

A language over $\Sigma$ is a subset of $\Sigma^*$, so the set of all languages is $\mathcal{P}(\Sigma^*)$. Since $\Sigma^*$ is countably infinite, this set is in bijection with $\mathcal{P}(\mathbb{N})$ and is uncountable. The set of Turing machines is countable, and each machine has one language. So:

- the [decidable languages](/decidable-language/) and the computably enumerable languages form countable sets;
- all but countably many languages are not computably enumerable, and so not decidable;
- in the same way, the functions $\mathbb{N} \to \mathbb{N}$ form an uncountable set, and the [computable functions](/computable-function/) only a countable one.

The argument shows that undecidable languages exist, but it names none. A [diagonal argument](/diagonalization-argument/) against the list of machines names one, and the [halting problem](/halting-problem/) is a natural one.

### Countable is not computably enumerable

In computability texts the word *enumerable* often means *computably enumerable* (c.e.): a set that some machine lists. The two notions differ. Every language $L \subseteq \Sigma^*$ is countable, since it is a subset of the countable set $\Sigma^*$. But only countably many languages are c.e., because each c.e. language is listed by some machine. The complement of the [halting problem](/halting-problem/) is a countable set that no machine lists. Countability asks for some listing; computable enumerability asks for a listing that a machine produces.

### Pitfalls

- **Injective, not surjective, into the set.** To show that $S$ is countable, map $S$ injectively into $\mathbb{N}$, or map $\mathbb{N}$ onto $S$. A map from $\mathbb{N}$ into $S$ that misses elements proves nothing.
- **Infinite words.** $\Sigma^*$ holds only finite words. The set $\Sigma^{\mathbb{N}}$ of infinite words is uncountable when $|\Sigma| \ge 2$.
- **A listing need not be computable.** The set of machines that halt on the empty input is countable, and its elements can be listed in some order, but no machine produces a list of the machines that do *not* halt on the empty input.

## Examples

**Shortlex order of binary words.** The first eight words are $\varepsilon, 0, 1, 00, 01, 10, 11, 000$, with indices $0$ to $7$. The word $0110$ has index $2^4 - 1 + 6 = 21$.

**Cantor pairing.** The table gives $\pi(x, y)$ for $x, y \le 3$; the row is $x$ and the column is $y$.

| $x \backslash y$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | 0 | 2 | 5 | 9 |
| 1 | 1 | 4 | 8 | 13 |
| 2 | 3 | 7 | 12 | 18 |
| 3 | 6 | 11 | 17 | 24 |

For example $\pi(3, 5) = \tfrac{1}{2} \cdot 8 \cdot 9 + 5 = 41$. To invert $z = 100$, find the largest $d$ with $\tfrac{1}{2} d(d+1) \le 100$, which is $d = 13$ (giving $91$); then $y = 100 - 91 = 9$ and $x = d - y = 4$.

**A diagonal against four sequences.** Take the rows $0110$, $1010$, $0001$ and $1111$ as the first four bits of four sequences. Flip the diagonal bits $0, 0, 0, 1$ to get $1110$. This differs from row $i$ in position $i$ for each $i$, so no sequence that starts with it is among the four.

**Finite counts.** There are $2^{11} - 1 = 2047$ binary words of length at most $10$, and so $2^{2047}$ languages that contain only such words. The machines with $n$ states over the tape symbols $\{0, 1\}$, in the format of the [busy beaver function](/busy-beaver-function/) (each of the $2n$ table entries writes a bit, moves left or right, and goes to one of $n$ states or a halt state), number $(4n + 4)^{2n}$: $64$ for $n = 1$, $20736$ for $n = 2$ and $16777216$ for $n = 3$. Each size is finite, so the union over all $n$ is countable.

**Countably many computable reals.** Each [computable real number](/computable-real-numbers/) is given by a machine, so there are countably many. The real numbers are uncountable, so almost every real number is not computable.

## Where it is used

- **Existence of undecidable problems.** The count above is the first proof that [undecidability](/undecidability/) exists. It is a non-constructive form of the [diagonalization argument](/diagonalization-argument/).
- **Encodings.** [Gödel numbering](/godel-numbering/) turns the countability of machines and formulas into an explicit computable bijection with $\mathbb{N}$. The [universal Turing machine](/universal-turing-machine/) reads such codes.
- **Counting arguments in complexity.** The finite form of the same idea, more functions than small circuits, is the [counting argument](/counting-argument/) for Boolean circuits. The [incompressibility method](/incompressibility-method/) and [Kolmogorov complexity](/kolmogorov-complexity/) count programs shorter than a string in the same way.
- **Non-uniform models.** A family of circuits has one circuit per input length, so there are uncountably many families, and some decide undecidable languages. See [non-uniform computation](/non-uniform-computation/).

## References
