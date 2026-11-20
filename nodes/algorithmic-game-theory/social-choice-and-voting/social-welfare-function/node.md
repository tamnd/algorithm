---
tag: 3DPZS3
kind: definition
slug: social-welfare-function
name: Social welfare function
aliases:
- preference aggregation rule
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: A rule that maps each preference profile to a collective ranking of the candidates. A social choice function maps it to a winner.
prereqs: [preference-profile]
see_also: [arrow-impossibility-theorem, gibbard-satterthwaite-theorem, may-theorem, borda-count, kemeny-rank-aggregation, condorcet-paradox, plurality-voting, rank-aggregation]
sources:
  - book: "Kenneth J. Arrow, Social Choice and Individual Values, Wiley, 1951; second edition, Yale University Press, 1963"
    title: Social Choice and Individual Values
    locator: the definition of a social welfare function and of the conditions on it
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 2 (William S. Zwicker, Introduction to the theory of voting), Section 2.3 (anonymity, neutrality and the Pareto property)"
---

A social welfare function is a rule that maps every [preference profile](/preference-profile/) of a group to one collective ranking of the candidates. Arrow introduced the term in 1951 to ask whether individual rankings can be combined into a social ranking in a reasonable way, and his [impossibility theorem](/arrow-impossibility-theorem/) says that with three or more candidates they cannot. A social choice function is the related rule that maps a profile to one winner, as every voting rule does.

## Definition

Let $A$ be a finite set of $m$ candidates, $N = \{1, \ldots, n\}$ the voters, and $\mathcal{L}(A)$ the set of linear orders on $A$. A profile is $P = (\succ_1, \ldots, \succ_n) \in \mathcal{L}(A)^n$.

- A *social welfare function* (SWF) is a map $F : \mathcal{L}(A)^n \to \mathcal{L}(A)$. Write $\succ_{F(P)}$ for the social ranking on profile $P$. Arrow allowed the output to be a weak order, with ties; his theorem holds for that form too.
- A *social choice function* (SCF) is a map $f : \mathcal{L}(A)^n \to A$. It is also called a resolute voting rule.
- A *social choice correspondence* maps each profile to a nonempty subset of $A$, the tied winners. A fixed tie-breaking rule turns it into an SCF.

A map defined only on a subset $D \subseteq \mathcal{L}(A)^n$, a restricted domain, is an SWF or SCF on $D$. Without a domain named, the domain is all of $\mathcal{L}(A)^n$ (the *unrestricted domain*).

The standard axioms for an SWF $F$, for all profiles $P$ and $Q$ and all candidates $a \ne b$:

- **Pareto (unanimity).** If $a \succ_i b$ for every voter $i$, then $a \succ_{F(P)} b$.
- **Independence of irrelevant alternatives (IIA).** If every voter orders $a$ and $b$ the same way in $P$ and in $Q$, that is, $a \succ_i b$ in $P$ exactly when $a \succ_i b$ in $Q$, then $F(P)$ and $F(Q)$ order $a$ and $b$ the same way.
- **Dictatorship.** Voter $d$ is a dictator if $F(P) = \succ_d$ for every $P$. $F$ is *nondictatorial* if no voter is a dictator.
- **Anonymity.** Permuting the voters does not change $F(P)$.
- **Neutrality.** If every ranking of $P$ is renamed by a permutation $\pi$ of $A$, then $F(P)$ is renamed by $\pi$.

For an SCF $f$ the matching axioms are: *Pareto* ($f(P) \ne b$ when all voters rank some $a$ above $b$), *onto* (every candidate wins on some profile), *dictatorship* ($f(P)$ is the top of $\succ_d$ for every $P$), and *strategyproofness* (no voter $i$ and profile $P$ have a ranking $\succ'$ with $f(P_{-i}, \succ') \succ_i f(P)$). The [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) is the impossibility theorem for these.

**From one kind to the other.** An SWF gives an SCF: elect the top of $F(P)$. An SCF does not give an SWF in general, but most SCFs come from a score or a sequence of eliminations that also ranks the losers. The [Borda count](/borda-count/) and [plurality voting](/plurality-voting/), with a fixed tie-break, are both.

## Examples and non-examples

**The Borda ranking satisfies Pareto but not IIA.** Order the candidates by Borda score, with points 2, 1 and 0, ties by index. In profile $P$, 3 voters have $a \succ b \succ c$ and 2 voters have $b \succ c \succ a$; the scores are $a = 6$, $b = 7$, $c = 2$ and the social ranking is $b \succ a \succ c$. In profile $Q$, the 3 voters have $a \succ c \succ b$ instead and the other 2 do not change; the scores are $a = 6$, $b = 4$, $c = 5$ and the ranking is $a \succ c \succ b$. Every voter orders $a$ and $b$ the same way in $P$ and in $Q$, but the social order of $a$ and $b$ flips, because $c$ moved. Pareto holds: if all voters put $a$ above $b$, each gives $a$ more points.

**The Kemeny ranking satisfies Pareto but not IIA.** The [Kemeny ranking](/kemeny-rank-aggregation/) minimizes the total [Kendall tau distance](/kendall-tau-distance/) to the profile. In $P$ it is $a \succ b \succ c$ (distance 4), and in $Q$ it is $a \succ c \succ b$ (distance 6), so here the order of $a$ and $b$ does not flip. It fails IIA on other profiles, as Arrow's theorem requires. Take 4 voters with $a \succ b \succ c$, $a \succ b \succ c$, $b \succ c \succ a$ and $c \succ a \succ b$; the unique Kemeny ranking is $a \succ b \succ c$. Change them to $a \succ c \succ b$, $b \succ a \succ c$, $c \succ b \succ a$ and $c \succ b \succ a$. Each voter orders $a$ and $c$ as before, but the unique Kemeny ranking is now $c \succ b \succ a$.

**A dictatorship satisfies Pareto and IIA.** $F(P) = \succ_1$ meets both conditions and is neutral, but it is not anonymous. Arrow's theorem says that with $m \ge 3$ it is, up to the choice of the voter, the only SWF with Pareto and IIA.

**A constant ranking satisfies IIA but not Pareto.** $F(P) = (a \succ b \succ c)$ for all $P$ ignores the voters, so IIA holds trivially; Pareto fails when all voters rank $b$ above $a$.

**Non-example: pairwise majority with three candidates.** Put $a$ above $b$ when more voters rank $a$ above $b$. With an odd $n$ this relation is complete, anonymous, neutral, Paretian and satisfies IIA, but it is not always transitive: on the profile $(a \succ b \succ c,\; b \succ c \succ a,\; c \succ a \succ b)$ it is the cycle $a, b, c, a$ ([Condorcet paradox](/condorcet-paradox/)). So it is not a map into $\mathcal{L}(A)$. With two candidates there is no cycle, and pairwise majority is an SWF; [May's theorem](/may-theorem/) characterizes it.

**Non-example: majority on a restricted domain.** On profiles of [single-peaked preferences](/single-peaked-preferences/) with an odd number of voters, the majority relation is transitive, so pairwise majority is an SWF on that domain, with Pareto, IIA, anonymity and neutrality. This does not contradict Arrow's theorem, which needs the unrestricted domain.

## Related definitions

- **Voting rule.** An SCF or a correspondence, such as [plurality voting](/plurality-voting/), [instant-runoff voting](/instant-runoff-voting/) or the [Copeland method](/copeland-method/).
- **Rank aggregation.** The computational problem of finding a consensus ranking of items from several rankings ([rank aggregation](/rank-aggregation/)). An SWF is a rank aggregation method that must work for every input.
- **Social welfare ordering.** In welfare economics, a ranking of the outcomes by a function of the voters' utilities, such as their sum. It needs numbers, not only rankings, and so falls outside Arrow's model.
- **Mechanism.** An SCF together with the strategic question of whether voters report their true rankings, the subject of [dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/).

## References
