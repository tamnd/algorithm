---
tag: SHFFAB
kind: definition
slug: partial-meet-contraction
name: Partial meet contraction
aliases:
- AGM partial meet contraction
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Contracts a belief set by p as the intersection of a selected subset of its maximal subsets that do not entail p.
prereqs: [agm-postulates]
see_also: [agm-representation-theorem, levi-identity, epistemic-entrenchment, grove-spheres, belief-revision, katsuno-mendelzon-revision]
sources:
  - paper: doi:10.2307/2274239
    title: "Carlos E. Alchourrón, Peter Gärdenfors and David Makinson, On the logic of theory change: partial meet contraction and revision functions, Journal of Symbolic Logic 50(2), 510 to 530 (1985)"
    locator: the whole paper (remainder sets, selection functions, partial meet and relational partial meet contraction and their representation)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 3 (maxichoice, full meet and partial meet contraction, Theorems 3 to 8)
  - paper: "Carlos E. Alchourrón and David Makinson, On the logic of theory change: contraction functions and their associated revision functions, Theoria 48(1), 14 to 37 (1982)"
    locator: the whole paper (maxichoice contraction and the maximality of its revision)
---

Partial meet contraction is the construction of contraction in the AGM theory. To remove $p$ from a belief set $K$, look at the largest parts of $K$ that do not imply $p$, pick the best of them, and keep what all the picked parts share. Picking one part gives maxichoice contraction, picking all gives full meet contraction, and both are extreme. Alchourrón, Gärdenfors and Makinson (1985) showed that the choices in between give exactly the contractions that satisfy the basic [AGM postulates](/agm-postulates/). This is the [AGM representation theorem](/agm-representation-theorem/).

## Definition

Let $\mathrm{Cn}$ be a Tarskian, compact consequence operation that includes classical propositional logic and satisfies the deduction theorem, and let $K$ be a belief set.

**Remainders.** For a sentence $p$, the remainder set $K \perp p$ is the set of the subsets $X \subseteq K$ such that

1. $p \notin \mathrm{Cn}(X)$, and
2. no $Y$ with $X \subsetneq Y \subseteq K$ has $p \notin \mathrm{Cn}(Y)$.

Each remainder is a belief set. If $p \notin K$, then $K \perp p = \{K\}$. If $\vdash p$, then $K \perp p$ is empty. In every other case $K \perp p$ is nonempty: by compactness, each subset of $K$ that does not imply $p$ lies inside a maximal one, and $\mathrm{Cn}(\emptyset)$ is such a subset.

**Selection functions.** A selection function for $K$ maps each nonempty $K \perp p$ to a nonempty subset $\gamma(K \perp p) \subseteq K \perp p$. For empty $K \perp p$ it gives $\{K\}$.

**Partial meet contraction.** The contraction given by $\gamma$ is

$$K \div p = \bigcap \gamma(K \perp p).$$

Two special cases:

- **Maxichoice contraction**: $\gamma(K \perp p)$ always has one member.
- **Full meet contraction**: $\gamma(K \perp p) = K \perp p$ always.

**Relational selection.** Let $M(K)$ be the union of all the sets $K \perp p$. A selection function is relational when there is a relation $\le$ on $M(K)$ such that, for every nonempty $K \perp p$,

$$\gamma(K \perp p) = \{X \in K \perp p : Y \le X \text{ for all } Y \in K \perp p\},$$

that is, $\gamma$ picks the best remainders. It is transitively relational when $\le$ can be chosen transitive.

**The finite propositional case.** Over $n$ atoms, $K = \mathrm{Cn}(\psi)$, and a set of sentences is given by its models. If $p \in K$ and not $\vdash p$, the remainders of $K$ by $p$ are exactly the belief sets with the models $\mathrm{Mod}(\psi) \cup \{w\}$, one for each world $w$ where $p$ is false. So a partial meet contraction picks a nonempty set $S$ of worlds where $p$ is false and sets

$$\mathrm{Mod}(K \div p) = \mathrm{Mod}(\psi) \cup S.$$

A transitively relational one picks the worlds of $\mathrm{Mod}(\neg p)$ that are best under a total preorder on the worlds outside $\mathrm{Mod}(\psi)$. This is the link to [Grove's spheres](/grove-spheres/) and to the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/).

## Examples and non-examples

Take two atoms $a, b$ and $K = \mathrm{Cn}(a \wedge b)$. Up to equivalence $K$ has 8 sentences, one for each set of worlds that contains $ab$.

- **The remainders by $a$.** The worlds where $a$ is false are $\bar a b$ and $\bar a \bar b$. So $K \perp a$ has two members: $\mathrm{Cn}(b)$, with the models $ab$ and $\bar a b$, and $\mathrm{Cn}(a \leftrightarrow b)$, with the models $ab$ and $\bar a \bar b$. Each has 4 of the 8 sentences of $K$.
- **The three choices.** A selection function picks one remainder or both. Picking $\mathrm{Cn}(b)$ gives $K \div a = \mathrm{Cn}(b)$, picking $\mathrm{Cn}(a \leftrightarrow b)$ gives $K \div a = \mathrm{Cn}(a \leftrightarrow b)$, and picking both gives the full meet $K \div a = \mathrm{Cn}(b) \cap \mathrm{Cn}(a \leftrightarrow b) = \mathrm{Cn}(a \to b)$.
- **Counting.** A sentence of $K$ that is false in $k$ worlds has $2^k - 1$ choices. The 7 sentences of $K$ that are not tautologies are false in 1, 1, 1, 2, 2, 2 and 3 worlds, so $K$ has $3^3 \cdot 7 = 189$ partial meet contractions. All satisfy K÷1 to K÷6. Exactly 13 also satisfy K÷7 and K÷8, and these are the transitively relational ones: one for each of the 13 total preorders on the three worlds $\bar a b$, $\bar a \bar b$ and $a \bar b$.
- **Why maxichoice is too strong.** With the [Levi identity](/levi-identity/), the maxichoice contraction that keeps $b$ gives $K * \neg a = \mathrm{Cn}(\neg a \wedge b)$, a complete theory over the two atoms. In general, if $\neg p \in K$, the revision built from a maxichoice contraction decides every sentence: for each $q$, either $q$ or $\neg q$ is in $K * p$ (Alchourrón and Makinson 1982; Gärdenfors 1992, Theorem 4).
- **Why full meet is too weak.** Full meet contraction gives $K * \neg a = \mathrm{Cn}(\neg a)$, which has lost $b$. In general, if $\neg p \in K$, full meet revision gives $K * p = \mathrm{Cn}(p)$ (Gärdenfors 1992, Theorem 6).
- **A non-example.** The contraction $K \div p = \mathrm{Cn}(\emptyset)$ for each nontautological $p \in K$ is not a partial meet contraction for this $K$: it is not the meet of any set of remainders of $K$ by $a$, and it fails recovery.

## Related definitions

- **Characterizations.** Maxichoice contractions are the contractions with K÷1 to K÷6 and fullness: if $q \in K$ and $q \notin K \div p$, then $q \to p \in K \div p$ (Gärdenfors 1992, Theorem 3). Full meet contraction is the one with $K \div p = K \cap \mathrm{Cn}(\neg p)$ for each $p \in K$ that is not a tautology (Theorem 5). In the example, $K \cap \mathrm{Cn}(\neg a) = \mathrm{Cn}(a \to b)$. Partial meet contractions are those with K÷1 to K÷6 (Theorem 7), and transitively relational ones are those with K÷1 to K÷8 (Theorem 8). The proofs are on the [AGM representation theorem](/agm-representation-theorem/) page.
- [Epistemic entrenchment](/epistemic-entrenchment/) gives the same contractions as transitively relational partial meet contraction, from an order on sentences instead of remainders.
- The [Levi identity](/levi-identity/) turns a partial meet contraction into partial meet revision.
- Safe contraction (Alchourrón and Makinson 1985) and kernel contraction remove the minimal subsets that imply $p$ instead of keeping the maximal subsets that do not.

## References
