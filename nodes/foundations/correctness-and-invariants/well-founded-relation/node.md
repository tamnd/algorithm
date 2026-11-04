---
tag: ZS4VJQ
kind: definition
slug: well-founded-relation
name: Well-founded relation
aliases:
- Well-founded ordering
- Noetherian ordering
area: foundations/correctness-and-invariants
level: advanced
summary: A relation in which every nonempty subset has a minimal element, or equivalently no infinite descending chain, so that induction over it is valid.
prereqs: [induction]
see_also: [well-ordering-principle, termination-proof, variant-function, lexicographic-order, multiset-ordering, structural-induction, ackermann-function]
sources:
  - url: "https://en.wikipedia.org/wiki/Well-founded_relation"
    locator: article Well-founded relation, sections Induction and recursion, and Examples
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That
    locator: Chapter 2 (abstract reduction systems, termination and well-founded induction)
  - paper: "Nachum Dershowitz and Zohar Manna, Proving termination with multiset orderings, Communications of the ACM 22(8) (1979), doi:10.1145/359138.359142"
    locator: pages 465 to 476
  - paper: "Robert W. Floyd, Assigning meanings to programs, Proceedings of Symposia in Applied Mathematics 19 (1967)"
    locator: pages 19 to 32, the final section (termination by a map into a well-ordered set)
---

A relation $\prec$ on a set $A$ is well-founded when every nonempty subset of $A$ has a minimal element, or, equivalently under the axiom of dependent choice and always for countable sets, when there is no infinite chain $a_0 \succ a_1 \succ a_2 \succ \cdots$. Well-founded relations are the exact condition under which induction is valid, and they are the tool of every [termination proof](/termination-proof/): a loop or a recursion stops when each step goes down in a well-founded relation. The usual order $<$ on the natural numbers is the basic example, and the [lexicographic](/lexicographic-order/) and [multiset](/multiset-ordering/) orders build larger ones from it.

## Definition

Let $\prec$ be a binary relation on a set $A$. Read $x \prec y$ as "$x$ is below $y$". An element $m$ of a subset $S \subseteq A$ is *minimal* in $S$ when no $s \in S$ has $s \prec m$.

**Definition.** The relation $\prec$ is *well-founded* when every nonempty subset $S \subseteq A$ has a minimal element.

The relation need not be transitive, and it need not be total. Two elements can be incomparable, so a subset can have several minimal elements, and none of them needs to be below all the others.

**No infinite descending chain.** A *descending chain* is a sequence $a_0, a_1, a_2, \ldots$ with $a_{i+1} \prec a_i$ for each $i$.

*Claim.* If $\prec$ is well-founded, there is no infinite descending chain. If there is no infinite descending chain, then $\prec$ is well-founded, provided the axiom of dependent choice holds.

*Proof.* Suppose $\prec$ is well-founded and $a_0, a_1, \ldots$ is an infinite descending chain. The set $S = \{a_0, a_1, \ldots\}$ is nonempty, so it has a minimal element $a_k$. But $a_{k+1} \in S$ and $a_{k+1} \prec a_k$, so $a_k$ is not minimal. This is a contradiction.

For the converse, suppose some nonempty $S$ has no minimal element. Pick $a_0 \in S$. Since $a_0$ is not minimal, there is $a_1 \in S$ with $a_1 \prec a_0$. Since $a_1$ is not minimal, there is $a_2 \in S$ with $a_2 \prec a_1$, and so on. The infinite sequence of choices is the axiom of dependent choice. The result is an infinite descending chain. $\square$

When $A$ is countable, list its elements and always pick the first suitable one, so no choice axiom is needed. For the sets of states and values of programs, the two forms of the definition are therefore the same.

**Well-founded induction.** Let $\prec$ be well-founded on $A$, and let $P$ be a property of elements of $A$. Suppose that for each $x \in A$,
$$ \bigl(\forall y \prec x : P(y)\bigr) \implies P(x). $$
Then $P(x)$ holds for each $x \in A$.

*Proof.* Let $S = \{x \in A : P(x) \text{ is false}\}$, and suppose $S$ is nonempty. Let $m$ be a minimal element of $S$. Each $y \prec m$ is not in $S$, so $P(y)$ holds. By the hypothesis, $P(m)$ holds, so $m \notin S$. This is a contradiction, so $S$ is empty. $\square$

There is no separate base case. For an element with nothing below it, the premise $\forall y \prec x : P(y)$ is true with nothing to check, so the step must prove $P(x)$ with no help. The converse also holds: if the induction rule is valid for $\prec$ and every property $P$, then $\prec$ is well-founded. To see this, let $S$ be a nonempty subset, and take $P(x)$ to be $x \notin S$. If $S$ had no minimal element, $P$ would satisfy the hypothesis of the rule: when no $y \prec x$ is in $S$, then $x$ is not in $S$, or it would be minimal. Induction would then give $S = \emptyset$, which is a contradiction.

**Well-founded recursion.** Let $\prec$ be well-founded on $A$. Suppose $G$ gives a value from an element $x$ and a function on $\{y : y \prec x\}$. Then there is exactly one function $F$ on $A$ with $F(x) = G(x, F|_{\{y \,:\, y \prec x\}})$ for each $x$. Uniqueness follows by well-founded induction: if $F$ and $F'$ both satisfy the equation and agree below $x$, they agree at $x$. For existence, call a function an approximation when it is defined on a set closed downwards and satisfies the equation there. Any two approximations agree where both are defined, by well-founded induction, and the union of all approximations is defined on all of $A$, again by well-founded induction, so it is the function $F$ (Jech, *Set Theory*, Theorem 6.4). This is why a recursive definition whose calls go down in a well-founded relation defines a total function.

**Two quick facts.**

- A well-founded relation is irreflexive. If $x \prec x$, then $x, x, x, \ldots$ is an infinite descending chain.
- If $\prec$ is well-founded, so is its transitive closure $\prec^+$. A descending chain in $\prec^+$ has each step made of finitely many $\prec$ steps, and joining them gives an infinite descending chain in $\prec$. This uses the chain form, so it needs dependent choice for uncountable sets, as in the claim above.

## Examples and non-examples

**Examples.**

- The order $<$ on $\mathbb{N}$ is well-founded. This is the [well-ordering principle](/well-ordering-principle/), and well-founded induction on it is strong [induction](/induction/).
- *Inverse image.* Let $f : A \to \mathbb{N}$ be any function, and define $x \prec y$ when $f(x) < f(y)$. A descending chain in $\prec$ gives a descending chain $f(a_0) > f(a_1) > \cdots$ in $\mathbb{N}$, so $\prec$ is well-founded. This is the method of the [variant function](/variant-function/). For Euclid's algorithm on a pair $(a, b)$ with $b > 0$, the step goes to $(b, a \bmod b)$, and $f(a, b) = b$ goes down because $a \bmod b < b$.
- *Lexicographic order on $\mathbb{N} \times \mathbb{N}$.* Define $(a, b) \prec (c, d)$ when $a < c$, or $a = c$ and $b < d$. Given a nonempty $S$, let $a^*$ be the least first coordinate in $S$, and let $b^*$ be the least second coordinate among the pairs in $S$ with first coordinate $a^*$. Then $(a^*, b^*)$ is minimal in $S$. This order is well-founded even though the pair $(1, 0)$ has infinitely many pairs below it: $(0, 0), (0, 1), (0, 2), \ldots$. So a well-founded relation can have elements with infinitely many predecessors.
- *Ackermann function.* The [Ackermann function](/ackermann-function/) is $A(0, n) = n + 1$, $A(m+1, 0) = A(m, 1)$ and $A(m+1, n+1) = A(m, A(m+1, n))$. Each call goes down in the lexicographic order on the argument pair: $(m, 1) \prec (m+1, 0)$, $(m+1, n) \prec (m+1, n+1)$, and $(m, k) \prec (m+1, n+1)$ for each $k$, whatever the value of the inner call. So the recursion stops on every input, although $A(n, n)$ eventually grows faster than every primitive recursive function, so $A$ is not primitive recursive.
- *Proper subterms.* On finite trees, define $s \prec t$ when $s$ is a proper subtree of $t$. The size goes down at each step, so this is an inverse image of $<$ on $\mathbb{N}$, and it is well-founded. Well-founded induction on it is [structural induction](/structural-induction/).
- *Multisets.* Dershowitz and Manna (1979) showed that the [multiset ordering](/multiset-ordering/) over a well-founded order is well-founded. One step replaces an element by any finite number of smaller elements. For example, over $\mathbb{N}$, $\{3\} \succ \{2, 2, 2, 1, 0\}$.

**Non-examples.**

- The order $<$ on $\mathbb{Z}$ is not well-founded: $0 > -1 > -2 > \cdots$.
- The order $<$ on the nonnegative rationals is not well-founded: $1 > 1/2 > 1/4 > \cdots$. The set of positive rationals has no minimal element.
- The dictionary order on strings over $\{a, b\}$, with $a < b$, is not well-founded: $b \succ ab \succ aab \succ aaab \succ \cdots$. Each string is smaller than the one before, because the two first differ at a position where the later string has $a$ and the earlier one has $b$. The *shortlex* order, which compares lengths first and uses the dictionary order only for strings of the same length, is well-founded, because only finitely many strings have each length.
- The relation $>$ on $\mathbb{N}$, read as "below", is not well-founded: $0, 1, 2, \ldots$ is a chain in which each element is below the one before it.

## Related definitions

- **Well-order.** A *well-order* is a strict total order that is well-founded. The order $<$ on $\mathbb{N}$ and the lexicographic order on $\mathbb{N} \times \mathbb{N}$ are well-orders, and the subtree relation is well-founded but not total.
- **Terminating relation.** In rewriting, a relation $\to$ is *terminating*, or strongly normalizing, when there is no infinite sequence $a_0 \to a_1 \to a_2 \to \cdots$. This holds exactly when the converse relation, $y \prec x$ when $x \to y$, is well-founded. Some authors call a terminating relation *Noetherian*, so the direction of the arrow must be read from the context (Baader and Nipkow, Chapter 2).
- **Rank.** Each element of a well-founded relation has a rank, defined by well-founded recursion as the least ordinal greater than the ranks of all elements below it. On $\mathbb{N}$ the rank of $n$ is $n$. On the lexicographic order of $\mathbb{N} \times \mathbb{N}$ the rank of $(a, b)$ is the ordinal $\omega \cdot a + b$. If $x \prec y$, then the rank of $x$ is less than the rank of $y$, so the rank is a variant function into the ordinals. If some element has rank at least $\omega$, no strictly decreasing variant into $\mathbb{N}$ exists, so the proof needs a lexicographic tuple or a variant into the ordinals. In $\mathbb{N} \times \mathbb{N}$, the pair $(1, 0)$ already has rank $\omega$.
- **Variant function and termination proof.** A [variant function](/variant-function/) maps each state of a loop into a set with a well-founded relation, and each iteration goes down. Floyd (1967) proved termination this way, with a map into a well-ordered set. See [termination proof](/termination-proof/).

## References
