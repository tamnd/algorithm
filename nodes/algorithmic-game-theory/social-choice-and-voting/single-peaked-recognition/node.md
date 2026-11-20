---
tag: HW79QR
kind: algorithm
slug: single-peaked-recognition
name: Recognizing single-peaked profiles
aliases:
- Bartholdi-Trick algorithm
- Escoffier-Lang-Ozturk algorithm
- single-peaked consistency
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Decides whether a profile is single-peaked on some ordering of the candidates, and finds such an axis, in O(mn) time by placing candidates from the two ends inward."
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1986
  people: [John J. Bartholdi III, Michael A. Trick, Jean-Paul Doignon, Jean-Claude Falmagne, Bruno Escoffier, Jérôme Lang, Meltem Öztürk]
  note: "Bartholdi and Trick reduced recognition to the consecutive ones property in 1986. Doignon and Falmagne (1994) and Escoffier, Lang and Ozturk (2008) gave direct algorithms that build the axis from the ends inward."
prereqs: [single-peaked-preferences, preference-profile]
see_also: [median-voter-theorem, consecutive-ones-property, pq-tree, generalized-median-voter-rule, chamberlin-courant-rule, condorcet-paradox]
sources:
  - paper: doi:10.1016/0167-6377(86)90072-6
    title: "John J. Bartholdi III and Michael A. Trick, Stable matching with preferences derived from a psychological model, Operations Research Letters 5(4) (1986), 165-169"
    locator: the recognition of single-peaked preferences
  - paper: doi:10.1006/jagm.1994.1010
    title: "Jean-Paul Doignon and Jean-Claude Falmagne, A polynomial time algorithm for unidimensional unfolding representations, Journal of Algorithms 16(2) (1994), 218-233"
    locator: the direct algorithm that builds the axis
  - paper: doi:10.3233/978-1-58603-891-5-366
    title: "Bruno Escoffier, Jérôme Lang and Meltem Öztürk, Single-peaked consistency and its complexity, Proceedings of ECAI 2008, 366-370"
    locator: the direct algorithm for single-peaked consistency
  - paper: arxiv:2205.09092
    title: "Edith Elkind, Martin Lackner and Dominik Peters, Preference restrictions in computational social choice: a survey, arXiv 2205.09092, version 2, March 2025"
    locator: "Section 4.1 (the consecutive ones reduction, Algorithm 1 and Theorem 4.2) and Section 4.8 (nearly single-peaked profiles, Table 2)"
---

Recognizing single-peaked profiles is the problem of deciding whether a [preference profile](/preference-profile/) is [single-peaked](/single-peaked-preferences/) on some order of the candidates, and of finding such an order, the axis. The axis is not part of the input, and there are $m!$ candidate orders, so a search over all of them is hopeless beyond tiny cases. The algorithm on this page fills the axis from both ends toward the middle: the candidates that voters rank last must go at the ends. It runs in $O(mn)$ time for $n$ voters and $m$ candidates, which is linear in the size of the profile.

## In plain words

In a single-peaked profile, the worst candidate of every voter is at one of the two ends of the line, because every voter likes candidates less as they move away from the favourite. So look at the bottom of every ballot. If three or more different candidates appear there, no line works. If one or two appear, put them at the free ends of the line, delete them from all ballots, and repeat with the rest. The only care needed is to choose the correct end for each candidate. A voter who likes the new candidate more than the candidate at one end and less than the candidate at the other end tells you which end is correct.

## The problem

The input is a profile $P = (\succ_1, \ldots, \succ_n)$ of strict rankings of the candidates $A = \{0, \ldots, m - 1\}$, each ranking stored as a list, best first. The output is an axis $\lhd$, a linear order of $A$, such that each $\succ_i$ is single-peaked on $\lhd$, or NONE if no such axis exists. If an axis exists, its reverse also works, and there may be many more.

The key facts are from the definition. On a single-peaked profile, each voter's last candidate is an end of the axis, so at most two candidates are last for some voter. Removing candidates keeps the profile single-peaked on the restricted axis. Together they suggest the outside-in method, but they do not tell which end a candidate should go to. The test in lines L10 and L11 answers this.

## The algorithm

```pseudo id=main
SP-AXIS(P, m)                       ▷ P = (≻_1, ..., ≻_n), candidates 0, ..., m - 1
L1  pos_i[a] ← position of a in ≻_i, for each voter i and candidate a
L2  left ← (); right ← (); R ← all candidates           ▷ R: the unplaced candidates
L3  while |R| ≥ 2 do
L4      B ← {the candidate that voter i ranks last in R : i = 1, ..., n}
L5      if |B| ≥ 3 then return NONE
L6      if right is empty then                            ▷ first stage: fill both ends
L7          append min B to left; if |B| = 2 then append max B to right
L8      else                                              ▷ second stage
L9          ℓ ← innermost candidate of left; r ← innermost candidate of right
L10         L ← {x in B : some voter i who does not rank x first in R has r ≻_i x ≻_i ℓ}
L11         R' ← {x in B : some voter i who does not rank x first in R has ℓ ≻_i x ≻_i r}
L12         if |L| ≥ 2 or |R'| ≥ 2 or L ∩ R' ≠ ∅ then return NONE
L13         put each x in B that is in neither set into L if L is empty, else into R'
L14         append L to left; append R' to right
L15     R ← R \ B; move each voter's first and last pointers past placed candidates
L16 return left, then R, then right from the outer end inward
```

Line L1 makes every comparison $a \succ_i b$ a comparison of two stored integers. Lines L4 and L5 find the candidates ranked last in the remaining set. In the first stage, line L7 fills the left end, and the right end as soon as two candidates are ranked last. In the second stage a candidate $x$ goes next to $\ell$ if a voter ranks $x$ between $r$ above and $\ell$ below while preferring some other remaining candidate to $x$: putting $x$ next to $r$ would make a valley at $x$ for that voter. Line L11 is the mirror test. The free choices in lines L7 and L13 put the smaller candidate on the left.

## Example

Take five candidates $a, b, c, d, e$, numbered $0$ to $4$, and three voters (Elkind, Lackner and Peters, Example 26):

$$\succ_1 = e\,d\,b\,c\,a, \qquad \succ_2 = e\,d\,c\,b\,a, \qquad \succ_3 = d\,e\,c\,a\,b.$$

| round | $R$ | last candidates $B$ | $\ell$, $r$ | decision | partial axis |
|---|---|---|---|---|---|
| 1 | $\{a, b, c, d, e\}$ | $\{a, b\}$ | none | first stage: $a$ left, $b$ right | $a \ldots b$ |
| 2 | $\{c, d, e\}$ | $\{c\}$ | $a$, $b$ | voter 1 has $b \succ c \succ a$ and prefers $e$ to $c$, so $c \in L$ | $a\,c \ldots b$ |
| 3 | $\{d, e\}$ | $\{d, e\}$ | $c$, $b$ | no voter constrains $d$ or $e$, so $d$ goes left and $e$ right | $a\,c\,d\,e\,b$ |

The loop stops with $R$ empty, and line L16 returns $a \lhd c \lhd d \lhd e \lhd b$. All three rankings are single-peaked on it: voter 3, for example, has peak $d$ and goes down to $c$, $a$ on the left and to $e$, $b$ on the right. If round 2 had put $c$ next to $b$, then voter 1 would have a valley at $c$ between $e$ and $b$. The axes for this profile are $a\,c\,d\,e\,b$, $a\,c\,e\,d\,b$ and their reverses.

## Correctness

The proof is in `proofs/correctness.md`, after Elkind, Lackner and Peters (Theorem 4.2). It has two parts.

If the algorithm returns an axis, suppose some voter had a valley on it. Then there is a valley on three adjacent candidates $a, b, c$. The first of them to be placed is an end one, say $a$, and it was placed in a round with two last candidates. The middle one $b$ is placed no later than $c$. When $b$ is placed, the voter ranks it below $a = \ell$ and, by a lemma on the earlier rounds, above $r$. The voter also prefers $c$ to $b$. So line L11 forces $b$ next to $r$, not next to $a$, which is a contradiction.

If the algorithm returns NONE, the proof finds one of two small patterns that no single-peaked profile can contain: three candidates that are each ranked below the other two by some voter, or four candidates with two voters whose top two sets cannot both be intervals of any axis.

## Complexity

Line L1 takes $O(mn)$ time. There are at most $m$ rounds, because each round places one or two candidates. Each voter keeps a pointer to its first and its last remaining candidate, so line L4 costs $O(n)$, lines L10 and L11 make at most $2n$ comparisons of positions, and line L15 moves each pointer at most $m$ times in the whole run. The total is $O(mn)$ time in the [word RAM](/word-ram/) model, linear in the input, and $O(mn)$ extra space for the position table. If rankings were searched by scanning, each comparison would cost $O(m)$ and the bound would be $O(m^2 n)$.

## Properties

- **Exact.** It returns an axis exactly when one exists, and every returned axis works.
- **One axis, not all.** The output is one axis. The set of all axes has a compact form; a [PQ-tree](/pq-tree/) built by the consecutive ones method describes all of them, and Elkind, Lackner and Peters (Section 4.1) give a direct description of the set.
- **Deterministic.** With the fixed choices in lines L7 and L13 the output depends only on the input.
- **Not neutral in its output.** Renaming the candidates can give a different axis among the valid ones, because free choices go by index.
- **The answer is a certificate.** A returned axis can be checked in $O(mn)$ time with the interval test of the definition; a NONE answer comes with one of the two forbidden patterns in the proof.

## Variants and improvements

- **Consecutive ones.** Bartholdi and Trick (1986) wrote one 0-1 row for each top-$k$ set of each voter, $nm$ rows over $m$ columns, and asked for a column order with the ones of every row consecutive, the [consecutive ones property](/consecutive-ones-property/). The matrix has $\Theta(m^2 n)$ entries, so this route takes $O(m^2 n)$ time, and its PQ-tree gives all axes at once.
- **Direct algorithms.** Doignon and Falmagne (1994) gave a direct algorithm in $O(mn + m^2)$ time, and Escoffier, Lang and Ozturk (2008) one in $O(mn)$ time. The form on this page follows the survey of Elkind, Lackner and Peters.
- **Other domains.** Single-crossing profiles can be recognized in $O(nm \log m)$ time and one-dimensional Euclidean profiles in polynomial time, while for $d$-dimensional Euclidean preferences with a fixed $d \ge 2$ recognition is NP-hard (survey, Theorems 4.8, 4.11 and 4.12).
- **Nearly single-peaked profiles.** Deleting the fewest candidates to make a profile single-peaked takes polynomial time, $O(m^3 n)$, while deleting the fewest voters is NP-complete (survey, Section 4.8, Table 2).

## When to use it

Use it before you rely on any result that needs single-peakedness: the [median voter theorem](/median-voter-theorem/), the strategyproof [generalized median voter rules](/generalized-median-voter-rule/), or the polynomial algorithm for the [Chamberlin-Courant rule](/chamberlin-courant-rule/) on single-peaked profiles, which needs the axis as input. If the axis is known from the problem, such as a numerical scale, check the profile against it directly with the interval test instead.

## Pitfalls

- **Checking each voter alone.** Every single ranking is single-peaked on some axis. The question is whether one axis works for all voters.
- **Choosing the side without the test.** In round 2 of the example, $c$ can go next to $a$ or next to $b$ as far as the end positions go, but only the first choice works. A rule such as "always the left side" works in the first stage and fails in the second, where lines L10 and L11 decide.
- **Slow comparisons.** Lines L10 and L11 compare positions. Looking a candidate up in a list costs $O(m)$ and raises the time to $O(m^2 n)$.
- **Ties and missing candidates.** The algorithm needs strict and complete rankings. Weak orders and partial rankings need other algorithms.

## Implementations

## History

Black (1948) defined single-peaked preferences, but the question of finding the axis came much later. Bartholdi and Trick (1986) met it while studying stable roommates with preferences from a one-dimensional model, and solved it by the consecutive ones property and PQ-trees. Doignon and Falmagne (1994) gave a direct algorithm in the language of unidimensional unfolding in psychology, and Escoffier, Lang and Ozturk (2008) found a direct linear algorithm independently, in computational social choice.

## References
