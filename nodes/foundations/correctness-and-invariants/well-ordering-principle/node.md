---
tag: Z2G1ZY
kind: theorem
slug: well-ordering-principle
name: Well-ordering principle
aliases:
- Well-ordering axiom
area: foundations/correctness-and-invariants
level: intro
summary: Every non-empty set of natural numbers has a least element; equivalent to induction.
prereqs: [induction]
see_also: [well-founded-relation, proof-by-contradiction, termination-proof, variant-function, structural-induction]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1, Mathematical induction
  - url: https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_textbook2.pdf
    title: Eric Lehman, F. Thomson Leighton and Albert R. Meyer, Mathematics for Computer Science (2015 version)
    locator: Chapter 2, The Well Ordering Principle, and Chapter 5, Induction
  - url: "https://en.wikipedia.org/wiki/Proof_by_infinite_descent"
    locator: article Proof by infinite descent, section History
  - url: "https://en.wikipedia.org/wiki/Peano_axioms"
    locator: article Peano axioms, section History
  - url: "https://en.wikipedia.org/wiki/Well-ordering_theorem"
    locator: article Well-ordering theorem, introduction
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 0.4, Types of proof (proof by induction)
---

The well-ordering principle says that every non-empty set of natural numbers has a least element. On the natural numbers it is equivalent to [induction](/induction/), in both the weak and the strong form: each of the three statements can be proved from the others. The principle is why a [variant function](/variant-function/) into the natural numbers forces a loop to stop, and why a proof can pick a least counterexample.

## Statement

Write $\mathbb{N} = \{0, 1, 2, \ldots\}$ with the order $<$ and the successor $n \mapsto n+1$. Assume only these properties of the order.

- **(A1)** $<$ is a strict total order on $\mathbb{N}$.
- **(A2)** $0 \le n$ for each $n \in \mathbb{N}$.
- **(A3)** For each $n$, $n < n+1$, and no $k$ satisfies $n < k < n+1$.
- **(A4)** Each $n \ne 0$ equals $k + 1$ for some $k \in \mathbb{N}$.

Consider these three statements, for $P$ ranging over all predicates on $\mathbb{N}$ and $S$ over all subsets of $\mathbb{N}$.

- **(WO)** Well-ordering: each non-empty $S \subseteq \mathbb{N}$ has a least element, that is, an $m \in S$ with $m \le s$ for all $s \in S$.
- **(I)** Weak induction: if $P(0)$ and $\forall n\, (P(n) \Rightarrow P(n+1))$, then $\forall n\, P(n)$.
- **(SI)** Strong induction: if $\forall n\, \big( (\forall k < n\ P(k)) \Rightarrow P(n) \big)$, then $\forall n\, P(n)$.

**Theorem.** Under (A1) to (A4), the statements (WO), (I) and (SI) are equivalent.

## In plain words

Take any group of counting numbers, as long as the group is not empty. Then the group has a smallest member. You can find it by counting up from zero until you meet a member of the group. This sounds obvious, but it has a strong use: you cannot go down for ever inside the counting numbers.

Induction says that if the first number has a property, and each number passes the property to the next one, then all numbers have it. The theorem says that these two ideas are two views of one fact. If you take one as a rule, you can prove the other from it.

## Proof

The proof has three parts: (WO) implies (I), then (I) implies (SI), then (SI) implies (WO). Together they give a cycle, so the three statements are equivalent.

**(WO) implies (I).** Assume (WO). Let $P$ be a predicate with $P(0)$ and $\forall n\, (P(n) \Rightarrow P(n+1))$. Suppose, for a contradiction, that $P(n)$ is false for some $n$. Then $S = \{ n \in \mathbb{N} : \neg P(n) \}$ is not empty. By (WO), $S$ has a least element $m$. Since $P(0)$ holds, $m \ne 0$. By (A4), $m = k + 1$ for some $k$. By (A3), $k < k+1 = m$. Because $m$ is the least element of $S$, $k \notin S$, so $P(k)$ holds. By the step, $P(k+1)$ holds, that is $P(m)$. But $m \in S$ means $\neg P(m)$. This is a contradiction. So $P(n)$ holds for each $n$.

**(I) implies (SI).** Assume (I). Let $P$ satisfy the hypothesis of (SI):

$$(\ast)\qquad \forall n\, \big( (\forall k < n\ P(k)) \Rightarrow P(n) \big).$$

Define $Q(n)$ to be the statement $\forall k < n\ P(k)$. We prove $\forall n\, Q(n)$ by (I).

- *Base case.* $Q(0)$ holds, because no $k$ satisfies $k < 0$. Indeed, if $k < 0$, then (A2) gives $0 \le k$, and so $k < 0 \le k$, which contradicts (A1).
- *Step.* Assume $Q(n)$. Let $k < n+1$. By (A1), $k < n$, or $k = n$, or $n < k$. The last case is impossible: $n < k < n+1$ contradicts (A3). If $k < n$, then $P(k)$ holds by $Q(n)$. If $k = n$, then $(\ast)$ and $Q(n)$ give $P(n)$, that is $P(k)$. So $P(k)$ holds for each $k < n+1$, which is $Q(n+1)$.

By (I), $Q(n)$ holds for each $n$. Now fix $n$. Since $n < n+1$ by (A3), $Q(n+1)$ gives $P(n)$. So $P(n)$ holds for each $n$.

**(SI) implies (WO).** Assume (SI). Let $S \subseteq \mathbb{N}$ be a set with no least element. We show that $S$ is empty. Let $P(n)$ be the statement $n \notin S$. We check the hypothesis of (SI). Let $n$ be a number such that $P(k)$ holds for all $k < n$, so no $k < n$ is in $S$. Suppose $n \in S$. Let $s \in S$. By (A1), $s < n$ or $s = n$ or $n < s$. The case $s < n$ is impossible, because no element below $n$ is in $S$. So $n \le s$. Then $n$ is a least element of $S$, which contradicts the choice of $S$. Hence $n \notin S$, that is $P(n)$. By (SI), $P(n)$ holds for each $n$, so $S$ is empty. Thus each non-empty set has a least element, which is (WO). $\blacksquare$

## Consequences

**Proof by a least counterexample.** To prove $\forall n\, P(n)$, assume that it fails. The set of $n$ with $\neg P(n)$ is non-empty, so it has a least element $m$. You then work with $m$ and use that $P(k)$ holds for all $k < m$. This is a [proof by contradiction](/proof-by-contradiction/) and it is the same as strong induction.

**Termination.** A [variant function](/variant-function/) with values in $\mathbb{N}$ cannot decrease for ever. Suppose that a loop runs for ever, with variant values $v_0 > v_1 > \cdots$. The set $\{v_k\}$ is non-empty, so by (WO) it has a least element $v_j$. But $v_{j+1} < v_j$ is in the set. See the [termination proof](/termination-proof/).

**Division with remainder.** For integers $a$ and $b \ge 1$ there are integers $q$ and $r$ with $a = qb + r$ and $0 \le r < b$. *Proof.* Let $S = \{ a - qb : q \in \mathbb{Z},\ a - qb \ge 0 \}$. It is a set of natural numbers. It is not empty: for $q = -|a|$, the number $a + |a|\,b \ge a + |a| \ge 0$ is in $S$. Let $r = a - qb$ be its least element. If $r \ge b$, then $r - b = a - (q+1)b \ge 0$ is in $S$ and is smaller than $r$, which is impossible. So $0 \le r < b$. $\blacksquare$ This is the fact that makes `a mod b` well defined in [Euclid's algorithm](/euclidean-algorithm/).

**Bézout's identity.** Let $a$ and $b$ be integers, not both 0. Then the least positive integer of the form $ax + by$ with $x, y \in \mathbb{Z}$ is $\gcd(a, b)$. *Proof.* The set $S = \{ ax + by : x, y \in \mathbb{Z},\ ax + by > 0 \}$ is a set of natural numbers. It is not empty, since $a \cdot a + b \cdot b > 0$ is in it. Let $d = ax_0 + by_0$ be its least element. Divide $a$ by $d$: $a = qd + r$ with $0 \le r < d$, by the division result above. Then $r = a(1 - qx_0) + b(-qy_0)$ has the form $ax + by$. If $r > 0$, then $r \in S$ and $r < d$, which is impossible. So $r = 0$ and $d$ divides $a$. In the same way $d$ divides $b$. Each common divisor of $a$ and $b$ divides $ax_0 + by_0 = d$, so it is at most $d$. Hence $d = \gcd(a, b)$. $\blacksquare$ For $a = 1071$ and $b = 462$, $\gcd = 21 = 1071 \cdot (-3) + 462 \cdot 7$. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) computes such $x$ and $y$.

**Generalisation.** The idea of a least element extends to any [well-founded relation](/well-founded-relation/), and the induction principle extends with it.

## Tightness

The three properties (A1) to (A4) do not imply (WO), (I) or (SI) alone. Take the order $\mathbb{N} + \mathbb{Z}$: a copy of $\mathbb{N}$, followed by a copy of $\mathbb{Z}$, so that each integer of the second copy is above each natural number of the first. This order is total (A1), has the least element 0 (A2), and each element has an immediate successor (A3). Each element other than 0 has an immediate predecessor, also in the copy of $\mathbb{Z}$ (A4). But the copy of $\mathbb{Z}$ has no least element, so (WO) fails. Induction fails too: let $P(n)$ say "$n$ is in the first copy". Then $P(0)$ holds and $P(n) \Rightarrow P(n+1)$ holds, but $P$ is false for each element of the second copy. So the equivalence is a statement about orders that satisfy (A1) to (A4), and to pick one of the three as an axiom is a real choice. The principle also fails for the integers $\mathbb{Z}$, for the non-negative rationals and for the non-negative reals with the usual order. For example, the set $\{1/k : k \ge 1\}$ has no least element.

## History

The least-counterexample argument is old. Fermat used it in the 17th century as the method of *infinite descent*: from a solution in positive integers, build a smaller one, so that no solution exists. In the axioms for the natural numbers that Dedekind (1888) and Peano (1889) gave, induction is the axiom, and the well-ordering principle is a theorem proved from it, as above. The equivalence of the three forms is now a standard part of a first course on proofs (Lehman, Leighton and Meyer, Chapters 2 and 5).

The name can confuse. The well-ordering *principle* is about $\mathbb{N}$ with its usual order, and it is provable from the axioms of arithmetic. The well-ordering *theorem* of Zermelo (1904) says that every set has some order in which it is well-ordered, and it is equivalent to the axiom of choice. This page is only about the first.

## References
