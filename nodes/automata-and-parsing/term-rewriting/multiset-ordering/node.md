---
tag: SANA5V
kind: definition
slug: multiset-ordering
name: Multiset ordering (Dershowitz-Manna)
aliases:
- Dershowitz-Manna ordering
- multiset extension of an order
area: automata-and-parsing/term-rewriting
level: advanced
summary: A well-founded ordering on finite multisets built from an ordering on elements.
prereqs: [well-founded-relation, termination]
see_also: [recursive-path-ordering, lexicographic-path-ordering, lexicographic-order, well-founded-reduction-ordering, knuth-bendix-ordering, termination, polynomial-interpretation]
sources:
  - paper: doi:10.1145/359138.359142
    title: Nachum Dershowitz and Zohar Manna, Proving termination with multiset orderings, Communications of the ACM 22(8) (1979)
    locator: pp. 465 to 476 (the definition and the theorem that the multiset ordering is well-founded)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.5, Multiset orders (the definition, the Huet-Oppen characterization and the proof of well-foundedness by König's lemma)
  - paper: doi:10.1016/0020-0190(82)90107-7
    title: Jean-Pierre Jouannaud and Pierre Lescanne, On multiset orderings, Information Processing Letters 15(2) (1982)
    locator: pp. 57 to 63 (equivalent definitions of the multiset ordering)
---

The **multiset ordering** lifts an order $>$ on a set $A$ to finite multisets over $A$: a multiset gets smaller when some elements are removed and each is replaced by any finite number of elements that are smaller than it. Dershowitz and Manna proved in 1979 that this ordering is well-founded whenever $>$ is. So a program or a [rewrite system](/term-rewriting-system/) terminates if each step makes a multiset of measures smaller, even when one step replaces one large measure by arbitrarily many smaller ones. The multiset ordering is the main ingredient of the multiset path ordering, a [recursive path ordering](/recursive-path-ordering/), and of many [termination](/termination/) proofs.

## Definition

A finite **multiset** over $A$ is a function $M : A \to \mathbb{N}$ that is non-zero at only finitely many points; $M(x)$ is the number of copies of $x$. Write $\mathcal{M}(A)$ for the set of finite multisets, $\emptyset$ for the empty multiset, $M + N$ for the sum, $(M + N)(x) = M(x) + N(x)$, $M - N$ for the difference, $(M - N)(x) = \max(0, M(x) - N(x))$, and $X \subseteq M$ if $X(x) \le M(x)$ for all $x$. Multisets are written with braces, $\{5, 3, 1, 1\}$.

Let $>$ be a strict partial order on $A$. The **multiset ordering** $>_{\mathrm{mul}}$ on $\mathcal{M}(A)$ is defined by: $M >_{\mathrm{mul}} N$ iff there are $X, Y \in \mathcal{M}(A)$ with

$$\emptyset \ne X \subseteq M, \qquad N = (M - X) + Y, \qquad \forall y \in Y\ \exists x \in X:\ x > y.$$

So $X$ is removed, $Y$ is added, and every added element is dominated by some removed one. $Y$ may be empty, and it may be much larger than $X$.

**Huet-Oppen characterization.** For a strict partial order $>$, $M >_{\mathrm{mul}} N$ holds iff $M \ne N$ and

$$\forall y:\ N(y) > M(y) \implies \exists x:\ x > y \text{ and } M(x) > N(x).$$

That is, every element that $N$ has more copies of is dominated by an element that $M$ has more copies of. This test needs $O(k^2)$ comparisons for multisets with $k$ distinct elements. If $>$ is total, it is the same as sorting both multisets in decreasing order and comparing the sorted lists [lexicographically](/lexicographic-order/), with a proper prefix being smaller.

**Theorem (Dershowitz and Manna, 1979).** $>_{\mathrm{mul}}$ is a strict partial order, and it is [well-founded](/well-founded-relation/) iff $>$ is well-founded.

*Proof of well-foundedness.* If $>$ has an infinite chain $a_1 > a_2 > \cdots$, then $\{a_1\} >_{\mathrm{mul}} \{a_2\} >_{\mathrm{mul}} \cdots$. Conversely, let $>$ be well-founded and suppose $M_0 >_{\mathrm{mul}} M_1 >_{\mathrm{mul}} \cdots$ is infinite. Build a tree whose nodes carry elements of $A$ or a mark $\bot$. Start with a root and one child for each element of $M_0$, counted with multiplicity. Keep the invariant that the leaves not marked $\bot$ carry exactly the multiset $M_i$. For the step $M_i >_{\mathrm{mul}} M_{i+1}$ with sets $X$ and $Y$, pick leaves carrying $X$; give each $y \in Y$ a new node as a child of a picked leaf $x$ with $x > y$, and give each picked leaf that received no child one child marked $\bot$. The invariant holds for $M_{i+1}$. Each step adds at least one node, because $X \ne \emptyset$, so the tree is infinite. Each node receives children in at most one step, and finitely many, so the tree is finitely branching. By König's lemma it has an infinite path. A $\bot$ node never has children, so the path, after the root, carries elements of $A$, and each child carries a smaller element than its parent: an infinite chain in $A$, a contradiction. $\blacksquare$

Transitivity and irreflexivity follow from the Huet-Oppen characterization, or directly by composing the replacements.

## Examples and non-examples

Over the natural numbers with the usual order:

- $\{5, 3, 1, 1\} >_{\mathrm{mul}} \{4, 3, 3, 1\}$: remove $X = \{5, 1\}$ and add $Y = \{4, 3\}$, both below $5$.
- $\{2\} >_{\mathrm{mul}} \{1, 1, 1\}$, and $\{3, 1\} >_{\mathrm{mul}} \{2, 2, 2\}$: one large element beats any number of smaller ones.
- $\{3, 3\} >_{\mathrm{mul}} \{3, 2, 2, 2, 2\}$: one copy of $3$ is kept and the other is replaced.
- $\{1\} >_{\mathrm{mul}} \emptyset$: $Y$ may be empty. The empty multiset is the least element.
- **Not comparable under a partial order.** With $A = \{a, b, c\}$ and only $a > c$, the multisets $\{a\}$ and $\{b\}$ are incomparable, and $\{a, b\} >_{\mathrm{mul}} \{b, c, c\}$.
- **Non-example: a larger sum is not enough.** $\{1, 1, 1\} \not>_{\mathrm{mul}} \{2\}$, since $2$ is not dominated by any element of $\{1, 1, 1\}$. The multiset ordering is not the comparison of sums or sizes.
- **Non-example: multisets of unbounded size with a non-well-founded order.** Over the integers, $\{0\} >_{\mathrm{mul}} \{-1\} >_{\mathrm{mul}} \{-2\} >_{\mathrm{mul}} \cdots$.

**A termination proof.** A program keeps a bag of positive integers and repeatedly replaces some $n > 1$ by any number of copies of $n - 1$, or removes some number. Each step is $M >_{\mathrm{mul}} N$ with $X = \{n\}$, so the program stops whatever choices it makes, although the bag can grow very large first.

**Order type.** If $>$ is a well-order of order type $\alpha$, then $>_{\mathrm{mul}}$ is a well-order of type $\omega^\alpha$. Over $\mathbb{N}$ this is $\omega^\omega$, much longer than $\mathbb{N}$ itself.

## Related definitions

- The multiset path ordering, the [recursive path ordering](/recursive-path-ordering/) with multiset status, compares the arguments of two terms with the same root symbol by the multiset extension of itself. The [lexicographic path ordering](/lexicographic-path-ordering/) uses the lexicographic extension instead.
- The [lexicographic order](/lexicographic-order/) on tuples of fixed length is the other standard way to lift a well-founded order; nested multisets, multisets of multisets, reach the order type $\varepsilon_0$.
- A [well-founded reduction ordering](/well-founded-reduction-ordering/) built from the multiset ordering proves termination of a [term rewriting system](/term-rewriting-system/) when every rule decreases.
- Derivation lengths of systems proved terminating by the multiset path ordering are bounded by primitive recursive functions (Hofbauer, 1992).

## References
