---
tag: QTSWDF
kind: concept
slug: parallel-rewriting
name: Parallel rewriting
aliases:
- parallel reduction
- multistep reduction
area: automata-and-parsing/term-rewriting
level: advanced
summary: Contracting a set of non-overlapping redexes in one step.
prereqs: [rewrite-step, term-context]
see_also: [orthogonal-rewrite-system, orthogonal-confluence-theorem, church-rosser-theorem, critical-pair, reduction-strategy, linearity, beta-reduction, standardization-theorem]
sources:
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821 (parallel reduction, the parallel moves lemma, and confluence of left-linear systems with parallel-closed critical pairs)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, Confluence (parallel reduction and the confluence of orthogonal systems)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 4, Orthogonality (parallel moves, developments and multi-steps)
  - paper: doi:10.1016/s0747-7171(89)80045-8
    title: Masako Takahashi, Parallel reductions in lambda-calculus, Journal of Symbolic Computation 7(2) (1989)
    locator: pp. 113 to 123
---

A **parallel rewrite step** contracts several redexes of a term at once, as long as none of them lies inside another. It is no stronger than ordinary rewriting, since the redexes can also be contracted one by one, but it behaves better: for [orthogonal](/orthogonal-rewrite-system/) systems two parallel steps from the same term can always be joined by one parallel step on each side. This **diamond property** is the core of the proofs of confluence for orthogonal systems and for the [lambda calculus](/lambda-calculus/), and parallel steps are the moves of the parallel-outermost and Gross-Knuth [strategies](/reduction-strategy/).

## In plain words

Usually a rewrite changes one place in an expression at a time. A parallel step changes several places at once, as long as the places are separate, so that no change is inside another. Doing them all at once gives the same result as doing them in any order.

Why bother, if the result is the same? Because two different single changes from the same expression can be hard to bring back together: one change may copy a part that the other change wants to edit, so the second change must be done several times afterwards. With parallel steps, "several times" is still one step. That makes it easy to show that the order of changes never matters for the final answer.

## The idea

We use the notation of the term rewriting pages: terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure. Two positions $p, q$ are **parallel**, $p \parallel q$, if neither is a prefix of the other.

**Parallel step.** $s \rightrightarrows_R t$ if there are pairwise parallel positions $p_1, \ldots, p_n$ of $s$ ($n \ge 0$), rules $l_i \to r_i$ and substitutions $\sigma_i$ with $s|_{p_i} = l_i\sigma_i$ and $t = s[r_1\sigma_1]_{p_1} \cdots [r_n\sigma_n]_{p_n}$. Since the positions are parallel, the replacements commute. With a [multihole context](/term-context/) $C$: $s = C[l_1\sigma_1, \ldots, l_n\sigma_n]$ and $t = C[r_1\sigma_1, \ldots, r_n\sigma_n]$. Equivalently, $\rightrightarrows_R$ is the smallest relation with

$$x \rightrightarrows x, \qquad l\sigma \rightrightarrows r\sigma \text{ for } l \to r \in R, \qquad s_i \rightrightarrows t_i \ (1 \le i \le n) \implies f(s_1, \ldots, s_n) \rightrightarrows f(t_1, \ldots, t_n).$$

**Basic facts.**

1. $\to_R \subseteq \rightrightarrows_R \subseteq \to_R^*$: a single step is a parallel step with $n = 1$, and a parallel step is $n$ ordinary steps, one per position, in any order. So $\rightrightarrows_R^* = \to_R^*$, and $R$ is confluent iff $\rightrightarrows_R$ is.
2. $\rightrightarrows_R$ is reflexive ($n = 0$), closed under contexts, and closed under substitutions.
3. A relation with the **diamond property** ($u \leftarrow s \to v$ implies $u \to w \leftarrow v$ for some $w$) is confluent, by tiling the plane of a peak $u \leftarrow^* s \to^* v$ with diamonds.

**Parallel moves lemma** (Huet, 1980). Let $R$ be left-linear and let $s \rightrightarrows u$ by contracting redexes at parallel positions $P$, and $s \to v$ by one step at position $q$, with no critical overlap between them. Then $u \rightrightarrows w$ and $v \rightrightarrows w$ for some $w$. *Proof sketch.* If $q$ is parallel to all of $P$, contract $q$ in $u$ and $P$ in $v$. If $q$ is below some $p \in P$, inside the substitution part of the redex $l\sigma$ at $p$ (there is no critical overlap), then $q$ lies below a variable position of $l$; the step at $p$ copies this redex once for each occurrence of the variable in $r$, and these copies are at pairwise parallel positions of $u$, so one parallel step contracts them all. On the other side, the redex at $p$ is still a redex in $v$, because $l$ is linear and changing the instance of one variable occurrence gives another instance of $l$. If $q$ is above some $p \in P$, the roles swap. $\blacksquare$ Without left-linearity the redex at $p$ can be destroyed, which is why the theorem needs it.

**Confluence results built on it.**

- An [orthogonal](/orthogonal-rewrite-system/) system has no critical pairs and is left-linear, so $\rightrightarrows_R$ has the diamond property and $R$ is confluent; see the [orthogonal confluence theorem](/orthogonal-confluence-theorem/).
- **Huet's parallel closure theorem.** A left-linear system is confluent if every [critical pair](/critical-pair/) $\langle u, v \rangle$ satisfies $u \rightrightarrows v$, where $u$ is the result of the step with the inner rule and $v$ the result of the step with the outer rule at the root of the overlap. No termination is needed, which distinguishes this test from the [critical pair lemma](/critical-pair-lemma/) with [Newman's lemma](/newman-lemma/).
- **Lambda calculus.** Tait and Martin-Löf's parallel reduction for beta also allows contraction inside the argument of a contracted redex. It has the diamond property, which proves the [Church-Rosser theorem](/church-rosser-theorem/). Takahashi (1989) gave a short proof: each term $s$ has a **complete development** $s^*$, obtained by contracting all its redexes from the inside out, and $s \rightrightarrows t$ implies $t \rightrightarrows s^*$.

**Developments and multi-steps.** The inductive definition above with $l\sigma \rightrightarrows r\sigma'$, where $\sigma \rightrightarrows \sigma'$ on each variable, contracts nested redexes too: first the inner ones in the substitution part, then the outer one. This **multi-step** contracts any set of redexes, as a complete development. It also has the diamond property for orthogonal systems, and it is the step of the Gross-Knuth strategy.

## Examples

All counts below were checked by enumerating parallel steps with a program.

**Counting parallel steps.** With the one rule $a \to b$, the term $g(a, a, a)$ has 3 redexes at the parallel positions 1, 2 and 3. Each nonempty subset gives a parallel step, so there are $2^3 - 1 = 7$ proper parallel steps, with 7 different results, among them $g(b, b, b)$ in one step. A term with $k$ pairwise parallel redexes has $2^k - 1$.

**Why a single step is not enough.** With $f(x) \to g(x, x)$ and $a \to b$, the peak $g(a, a) \leftarrow f(a) \to f(b)$ needs two ordinary steps on the left, $g(a, a) \to g(b, a) \to g(b, b)$, and one on the right, $f(b) \to g(b, b)$. Ordinary steps do not have the diamond property here. With parallel steps, $g(a, a) \rightrightarrows g(b, b)$ in one step, and the peak closes as a diamond.

**Diamond property, tested.** For 150 random orthogonal systems over $\{f/2, g/1, a/0, b/0\}$ with up to 3 rules, including duplicating and collapsing rules, and 10 random terms each, every pair of parallel steps from the same term was joined by one parallel step on each side: 3048 peaks in total.

**Left-linearity is needed.** $R = \{f(x, x) \to a,\ f(x, g(x)) \to b,\ c \to g(c)\}$ has no critical pairs, since $x = g(x)$ has no solution, but it is not left-linear. Then $f(c, c) \to a$ and $f(c, c) \to f(c, g(c)) \to b$, and $a, b$ are distinct normal forms. The step $c \to g(c)$ destroys the redex $f(c, c)$, so the parallel moves lemma fails.

**Lindenmayer systems.** In an L-system every letter of a word is rewritten at each step, all at once: with $a \to ab$, $b \to a$, the word $a$ becomes $ab$, $aba$, $abaab$, $abaababa$, with lengths given by the Fibonacci numbers. This is maximal parallel rewriting of strings, and unlike a parallel step above it is not a choice of some redexes: all of them must be contracted.

## Where it is used

- Confluence proofs: the [orthogonal confluence theorem](/orthogonal-confluence-theorem/), Huet's parallel closure theorem, and the [Church-Rosser theorem](/church-rosser-theorem/) for [beta reduction](/beta-reduction/).
- [Reduction strategies](/reduction-strategy/): parallel outermost and Gross-Knuth reduction contract sets of redexes in one move, which makes them normalizing for orthogonal systems.
- The [standardization theorem](/standardization-theorem/) and the theory of residuals, which track how the redexes of a term move under parallel steps.
- Parallel implementations of rewriting, which contract independent redexes on different processors; independence of parallel positions is what makes this safe.
- Biological modelling and graphics with Lindenmayer systems.

## References
