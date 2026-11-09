---
tag: 8BWFDY
kind: theorem
slug: higher-order-unification-undecidability
name: Undecidability of higher-order unification
aliases:
- Huet's undecidability result
- undecidability of third-order unification
area: logic-and-constraints/unification-and-resolution
level: research
summary: No algorithm decides whether two simply typed λ-terms with third-order variables have a unifier. Huet and Lucchesi proved it in 1972 and 1973 by reduction from Post's correspondence problem.
prereqs: [higher-order-unification-problem, post-correspondence-problem, undecidability, lambda-calculus]
see_also: [second-order-unification-undecidability, huet-pre-unification, pattern-unification-problem, semi-unification-undecidability, undecidability-of-unification-modulo-theories, recursively-enumerable-language]
sources:
  - paper: doi:10.1016/S0019-9958(73)90301-X
    title: Gérard P. Huet, The undecidability of unification in third order logic, Information and Control 22(3), 257 to 267 (1973)
    locator: the whole paper (reduction from Post's correspondence problem)
  - paper: "Cláudio L. Lucchesi, The undecidability of the unification problem for third order languages, Report CSRR 2059, Department of Applied Analysis and Computer Science, University of Waterloo (1972)"
    locator: the whole report (an independent proof)
  - paper: doi:10.1145/3372885.3373832
    title: Simon Spies and Yannick Forster, Undecidability of higher-order unification formalised in Coq, Proceedings of the 9th ACM SIGPLAN International Conference on Certified Programs and Proofs (CPP 2020), 143 to 157
    locator: Section 4 (the reduction from the modified Post correspondence problem, Theorem 4.7), which this page follows
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.4 (Post's correspondence problem and the modified problem)
---

Higher-order unification is undecidable: no algorithm can decide, for two simply typed λ-terms, whether some substitution for their free variables makes them equal up to $\beta\eta$. Gérard Huet (1973) and Cláudio Lucchesi (1972) proved this on their own, both by a reduction from [Post's correspondence problem](/post-correspondence-problem/). The result already holds for one equation with a single free variable of third order. It is the reason why [Huet's pre-unification](/huet-pre-unification/) is a search that can run forever, and why practical systems use decidable fragments such as [patterns](/pattern-unification-problem/). Goldfarb later showed that even [second-order unification is undecidable](/second-order-unification-undecidability/).

## Statement

Types are built from one base type $\iota$ and arrows. The order of a type is $\operatorname{ord}(\iota) = 1$ and $\operatorname{ord}(\sigma \to \tau) = \max(\operatorname{ord}(\sigma) + 1, \operatorname{ord}(\tau))$. A unification problem has third order when its free variables have types of order at most 3.

**Theorem (Huet 1973, Lucchesi 1972).** The [higher-order unification problem](/higher-order-unification-problem/) is undecidable. It stays undecidable for problems with one equation, one free variable of order 3, and one constant of type $\iota$.

Since the problem is semi-decidable (list all substitutions and test each one by normalization), it is in fact complete for the [recursively enumerable](/recursively-enumerable-language/) sets.

## In plain words

Strings can be written as λ-terms: the string 0 1 1 becomes the function that applies "0", then "1", then "1" to its input. Joining strings is then just function composition. We build one equation whose unknown is a function that takes one string for each card of a Post correspondence puzzle. On the left side the unknown gets the top strings of the cards, and on the right side it gets the bottom strings. The unknown cannot look inside the strings, so all it can do is compose some of its inputs in a fixed order. That order is the same on both sides, so a solution of the equation is exactly a list of cards whose top and bottom strings agree. Since no program can solve all such puzzles, no program can solve all such equations.

## Proof

We reduce from the modified Post correspondence problem (MPCP). An instance is a list of cards $l_0/r_0, l_1/r_1, \ldots, l_n/r_n$, where each $l_i$ and $r_i$ is a string over $\{0, 1\}$. It asks whether there are $k \ge 0$ and indices $i_1, \ldots, i_k \in \{1, \ldots, n\}$ with

$$l_0\, l_{i_1} \cdots l_{i_k} = r_0\, r_{i_1} \cdots r_{i_k}.$$

MPCP is undecidable: the standard proof that Post's correspondence problem is undecidable goes through it.

**Encoding strings.** Fix two variables $u_0, u_1 : \iota \to \iota$. A string $w = b_1 \cdots b_m$ is encoded as the term

$$\hat w = \lambda z.\, u_{b_1}(u_{b_2}(\cdots u_{b_m}(z) \cdots)) : \iota \to \iota.$$

Then $\hat w(\hat v(t))$ normalizes to $\widehat{wv}(t)$, so concatenation is composition.

**The equation.** Let $F$ be a free variable of type $(\iota \to \iota)^{n+1} \to \iota$, which has order 3, and let $a : \iota$ be a constant. The instance maps to the single pair

$$\lambda u_0 u_1.\, \hat l_0(F(\hat l_0, \hat l_1, \ldots, \hat l_n)) \;\doteq\; \lambda u_0 u_1.\, \hat r_0(F(\hat r_0, \hat r_1, \ldots, \hat r_n)).$$

This map is computable. We show that the pair has a unifier if and only if the MPCP instance has a solution.

**If.** Let $l_0 l_{i_1} \cdots l_{i_k} = r_0 r_{i_1} \cdots r_{i_k}$. Set $F \mapsto \lambda x_0 \ldots x_n.\, x_{i_1}(x_{i_2}(\cdots x_{i_k}(a) \cdots))$. The left side becomes $\lambda u_0 u_1.\, \hat l_0(\hat l_{i_1}(\cdots \hat l_{i_k}(a)))$, which normalizes to $\lambda u_0 u_1.\, \widehat{l_0 l_{i_1} \cdots l_{i_k}}(a)$. The right side becomes $\lambda u_0 u_1.\, \widehat{r_0 r_{i_1} \cdots r_{i_k}}(a)$. The two strings are equal, so the two terms are equal.

**Only if.** Let $\delta$ be a unifier, and write the $\beta$-normal $\eta$-long form of $\delta(F)$ as $\lambda x_0 \ldots x_n.\, v$ with $v : \iota$. Each $x_j$ has type $\iota \to \iota$, so it takes exactly one argument, and that argument has type $\iota$ and no binder. Take the longest chain

$$v = x_{i_1}(x_{i_2}(\cdots x_{i_k}(v') \cdots))$$

such that $v'$ does not start with any $x_j$. The head of $v'$ is then a constant or a free variable. It is not $u_0$ or $u_1$: these are bound by the outer λ of the equation, and the value $\delta(F)$ is substituted under that λ, so it cannot mention them.

Now substitute the encoded strings for $x_0, \ldots, x_n$. On the left side we get

$$\lambda u_0 u_1.\, \hat l_0(\hat l_{i_1}(\cdots \hat l_{i_k}(v'_l))) = \lambda u_0 u_1.\, \widehat{l_0 l_{i_1} \cdots l_{i_k}}(v'_l),$$

where $v'_l$ is the normal form of $v'$ after the substitution. It has the same head as $v'$, which is not $u_0$ or $u_1$. On the right side we get $\lambda u_0 u_1.\, \widehat{r_0 r_{i_1} \cdots r_{i_k}}(v'_r)$ in the same way, with the same indices $i_1, \ldots, i_k$, because the same term $v$ is used on both sides.

Each side is a chain of applications of $u_0$ and $u_1$, followed by a term whose head is not $u_0$ or $u_1$. Two equal normal terms have the same chain. So the chain on the left, which spells $l_0 l_{i_1} \cdots l_{i_k}$, is equal to the chain on the right, which spells $r_0 r_{i_1} \cdots r_{i_k}$. This is a solution of the MPCP instance.

So a decision procedure for third-order unification would decide MPCP, which is impossible. The equation has one free variable $F$ of order 3 and one constant $a$. $\blacksquare$

## Consequences

- **Only semi-decision procedures.** A complete procedure must be allowed to run forever on problems with no unifier. [Huet's pre-unification](/huet-pre-unification/) is such a procedure.
- **No most general unifiers.** The problem is not unitary or finitary: a solvable problem can need an infinite set of independent unifiers. Undecidability shows that no finite description of all unifiers can be computed in general.
- **Decidable fragments matter.** Systems that need a terminating unifier restrict the input, for example to [higher-order patterns](/pattern-unification-problem/), or to matching.
- **Higher-order logic.** Resolution and tableau provers for higher-order logic cannot rely on a complete unification step. Huet's constrained resolution keeps the hard pairs as constraints instead.

## Tightness

The order 3 is not the least possible. Goldfarb (1981) showed that [second-order unification](/second-order-unification-problem/) is already undecidable, by reduction from [Hilbert's tenth problem](/hilberts-tenth-problem/). Below that, first-order [unification](/unification-problem/) is decidable in linear time, so order 2 is the exact border.

Several restrictions bring back decidability:

- **Matching.** When one side has no free variables, the problem is decidable at all orders. Huet and Lang (1978) showed this for second order, and Stirling (2009) for all orders.
- **Patterns.** If each free variable is applied only to distinct bound variables, the problem is decidable and has most general unifiers (Miller 1991).
- **Monadic second order.** If all constants have at most one argument, second-order unification is decidable (Zhezherun 1979, and Farmer 1988 by reduction to word equations).

## History

Lucchesi (1972, a report from the University of Waterloo) and Huet (1973, Information and Control) proved the result on their own, both by reduction from Post's correspondence problem. Huet's paper came out just before his semi-decision procedure for the same problem (1975). Goldfarb lowered the order to two in 1981. Spies and Forster (2020) checked both proofs in the Coq proof assistant. They simplified Huet's construction to the single equation used above, with a reduction from the modified Post correspondence problem.

## References
