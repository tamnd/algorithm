---
tag: Y1RE72
kind: theorem
slug: arrow-impossibility-theorem
name: "Arrow's impossibility theorem"
aliases:
- "Arrow's theorem"
- general possibility theorem
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: With three or more candidates, every social welfare function that is unanimous and independent of irrelevant alternatives is a dictatorship.
prereqs: [social-welfare-function, condorcet-paradox]
see_also: [may-theorem, gibbard-satterthwaite-theorem, condorcet-paradox, single-peaked-preferences, median-voter-theorem, borda-count, kemeny-rank-aggregation, social-welfare-function]
sources:
  - paper: doi:10.1086/256963
    title: "Kenneth J. Arrow, A difficulty in the concept of social welfare, Journal of Political Economy 58(4) (1950), 328-346"
    locator: the conditions on a social welfare function and the first published form of the theorem
  - book: "Kenneth J. Arrow, Social Choice and Individual Values, Wiley, 1951; second edition, Yale University Press, 1963"
    title: Social Choice and Individual Values
    locator: the general possibility theorem and its proof, with the corrected form in the second edition
  - paper: doi:10.1007/s00199-004-0556-7
    title: "John Geanakoplos, Three brief proofs of Arrow's impossibility theorem, Economic Theory 26(1) (2005), 211-215"
    locator: the first proof, with the lemma on extreme candidates and the pivotal voter
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: "Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on social choice (Arrow's theorem, and the Gibbard-Satterthwaite theorem proved by reduction to it)"
---

Arrow's impossibility theorem says that with three or more candidates there is no good way to turn the rankings of the voters into one ranking for the group. Every [social welfare function](/social-welfare-function/) that respects unanimous preferences (Pareto) and decides each pair of candidates only from how the voters rank that pair (independence of irrelevant alternatives) is a dictatorship: it copies the ranking of one fixed voter. Kenneth Arrow proved it in 1950 and 1951. It turns the [Condorcet paradox](/condorcet-paradox/) from a defect of majority rule into a limit on all ranking rules, and it is the starting point of modern social choice theory.

## Statement

Let $A$ be a finite set of $m$ candidates, $N = \{1, \ldots, n\}$ the voters, and $\mathcal{L}(A)$ the linear orders on $A$. A social welfare function is a map $F : \mathcal{L}(A)^n \to \mathcal{L}(A)$, defined on every profile (unrestricted domain). Write $\succ_i$ for voter $i$'s ranking in a profile $P$ and $\succ_P$ for the social ranking $F(P)$. The conditions are:

1. **Pareto.** For all $P$ and $a, b \in A$: if $a \succ_i b$ for every $i$, then $a \succ_P b$.
2. **Independence of irrelevant alternatives (IIA).** For all $P$, $Q$ and $a, b \in A$: if every voter orders $a$ and $b$ the same way in $P$ and in $Q$, then $\succ_P$ and $\succ_Q$ order $a$ and $b$ the same way.
3. **Dictatorship.** Voter $d$ is a *dictator* if $\succ_P = \succ_d$ for every profile $P$.

**Theorem (Arrow).** If $m \ge 3$, every social welfare function that satisfies Pareto and IIA has a dictator.

The theorem also holds when voters and society may have ties (weak orders), which is the form Arrow used. With $m = 2$ it fails: majority rule satisfies both conditions and has no dictator.

## In plain words

Imagine a rule that takes everyone's ranking of some candidates and produces a ranking for the group. Ask for two things. If every voter prefers one candidate to another, so does the group. And the group's view of two candidates depends only on how the voters rank those two, not on where they put a third one. With three or more candidates, the only rules that meet both demands pick one voter and copy that voter's ranking every time. So every fair-looking ranking rule must break one of the two demands.

## Proof

The proof follows Geanakoplos (2005). Fix $F$ with Pareto and IIA and $m \ge 3$. Call a candidate $b$ *extreme* in a ranking if it is first or last.

*Step 1: extreme for everyone means extreme for society.* Let $P$ be a profile in which $b$ is extreme for every voter. Suppose, for a contradiction, that $a \succ_P b \succ_P c$ for some $a$ and $c$ other than $b$. Change each voter's ranking by moving $c$ to just above $a$, if it is not already above $a$, and keep $b$ where it is. Call the result $P'$. Since $b$ is first or last for every voter, no voter changes the order of $a$ and $b$ or of $b$ and $c$. By IIA, $a \succ_{P'} b$ and $b \succ_{P'} c$, so $a \succ_{P'} c$ by transitivity. But every voter ranks $c$ above $a$ in $P'$, so Pareto gives $c \succ_{P'} a$. This is a contradiction, so $b$ is first or last in $\succ_P$.

*Step 2: a pivotal voter.* Fix $b$. Start from a profile $P^0$ in which every voter ranks $b$ last; by Pareto, society ranks $b$ last. For $j = 1, \ldots, n$, let $P^j$ be $P^{j-1}$ with voter $j$ moving $b$ from last to first and the other candidates kept in the same order. In $P^n$ every voter ranks $b$ first, so society does too. In each $P^j$, $b$ is extreme for every voter, so by Step 1 it is first or last for society. Let $j^* = j^*(b)$ be the first index with $b$ first in $\succ_{P^{j^*}}$. Write $P^{\mathrm{I}} = P^{j^* - 1}$, where society ranks $b$ last, and $P^{\mathrm{II}} = P^{j^*}$, where society ranks $b$ first. The two profiles differ only in the ranking of voter $j^*$.

*Step 3: $j^*$ dictates every pair without $b$.* Let $a$ and $c$ be two candidates other than $b$, and let $Q$ be any profile with $a \succ_{j^*} c$ in $Q$. Build a profile $R$: voter $j^*$ ranks $a \succ b \succ c$ at the top of the list in this order, followed by the rest; each voter $i < j^*$ ranks $b$ first and each $i > j^*$ ranks $b$ last; and every voter $i \ne j^*$ orders $a$ and $c$ as in $Q$. Now compare.

- On $\{a, b\}$, every voter in $R$ orders the pair as in $P^{\mathrm{I}}$: voters before $j^*$ put $b$ on top, voters after $j^*$ put $b$ at the bottom, and $j^*$ has $a$ above $b$, as in $P^{\mathrm{I}}$ where $b$ was last for $j^*$. Society ranks $b$ last in $P^{\mathrm{I}}$, so IIA gives $a \succ_R b$.
- On $\{b, c\}$, every voter in $R$ orders the pair as in $P^{\mathrm{II}}$, where $j^*$ ranks $b$ first. Society ranks $b$ first in $P^{\mathrm{II}}$, so IIA gives $b \succ_R c$.

So $a \succ_R c$ by transitivity. Every voter orders $a$ and $c$ the same way in $R$ and in $Q$, so IIA gives $a \succ_Q c$. Since $Q$ was any profile with $a \succ_{j^*} c$, voter $j^*(b)$ decides every pair of candidates other than $b$.

*Step 4: the pivotal voter is the same for every candidate.* Let $b \ne c$. Since $m \ge 3$ there is a third candidate $a$. By Step 3 applied to $c$, voter $j^*(c)$ decides the pair $\{a, b\}$. In the profiles $P^{\mathrm{I}}$ and $P^{\mathrm{II}}$ of Step 2 for $b$, society ranks $a$ above $b$ and then $b$ above $a$, and only voter $j^*(b)$ changes between them. If $j^*(c) \ne j^*(b)$, voter $j^*(c)$ orders $a$ and $b$ the same way in both profiles, and as the decider of $\{a, b\}$ forces the same social order in both, which is false. So $j^*(c) = j^*(b)$, and all candidates have the same pivotal voter $d$.

*Step 5: $d$ is a dictator.* Let $a$ and $b$ be any two candidates and pick a third candidate $c$. By Step 3, $d = j^*(c)$ decides $\{a, b\}$. A ranking is fixed by its order on each pair, so $\succ_P = \succ_d$ for every $P$. $\blacksquare$

For $m = 3$ and $n = 2$ the theorem can also be checked directly. By IIA a rule is three functions, one per pair, each from the two voters' orders of the pair to a social order; Pareto leaves 4 choices for each, so 64 rules. Testing transitivity on all 36 profiles leaves exactly 2 rules, the two dictatorships.

## Consequences

- **Every ranking rule fails a condition.** The [Borda count](/borda-count/) and the [Kemeny ranking](/kemeny-rank-aggregation/) satisfy Pareto and are not dictatorships, so they fail IIA; the [social welfare function](/social-welfare-function/) page shows profiles where they do. Pairwise majority satisfies IIA and Pareto but fails transitivity, as the [Condorcet paradox](/condorcet-paradox/) shows.
- **Rank aggregation must give something up.** Methods that combine rankings of search results, of candidates or of models are social welfare functions in this sense. If they are not dictatorial, the order of two items can depend on where a third item is placed.
- **Manipulation.** The [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) says that every strategyproof voting rule with at least three possible winners is a dictatorship. One standard proof builds a social welfare function from a strategyproof rule and applies Arrow's theorem.
- **Two candidates are special.** For $m = 2$, transitivity says nothing, and [May's theorem](/may-theorem/) shows that majority rule is the only anonymous, neutral and positively responsive rule.

## Tightness

Each assumption is needed.

- **Three candidates.** With $m = 2$ and an odd number $n \ge 3$ of voters, majority rule satisfies Pareto and IIA and has no dictator.
- **Pareto.** The constant ranking $a \succ b \succ c$ satisfies IIA and has no dictator. So does the rule that returns the reverse of voter 1's ranking.
- **IIA.** The Borda ranking with a fixed tie-break satisfies Pareto and has no dictator.
- **Transitivity of the output.** Pairwise majority with an odd number of voters satisfies Pareto, IIA, anonymity and neutrality, but its output can be a cycle.
- **Unrestricted domain.** If all voters have [single-peaked preferences](/single-peaked-preferences/) on a common axis and $n$ is odd, pairwise majority is transitive, and it is a social welfare function with Pareto, IIA and no dictator on that domain ([median voter theorem](/median-voter-theorem/)).
- **Finitely many voters.** The proof needs a first pivotal voter. With infinitely many voters there are nondictatorial rules with Pareto and IIA (Fishburn 1970). The proof of their existence is not constructive: they come from nonprincipal ultrafilters on the set of voters.
- **Only rankings as input.** If the rule may use utilities that can be compared across voters, the sum of utilities gives a social ranking with Pareto and no dictator. Arrow's model uses only the order of each voter.

## History

Arrow stated the theorem in a paper in the Journal of Political Economy in 1950 and gave the full treatment in his book Social Choice and Individual Values (1951), which grew out of his doctoral thesis. Julian Blau (1957) found a gap in the original statement of the conditions, and the second edition of 1963 gives a corrected form. Arrow shared the Nobel Memorial Prize in Economic Sciences with John Hicks in 1972. Many short proofs followed; the pivotal voter proof above is the first of three that Geanakoplos published in 2005. In computer science the theorem is a standard example for automated reasoning: for small numbers of voters and candidates it can be checked by a SAT solver, and an induction reduces the general case to such a base case.

## References
