---
tag: 0PPKP2
kind: definition
slug: preference-profile
name: Preference profile
aliases:
- profile of rankings
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: A list of the voters' preferences, each a ranking of the candidates. Every voting rule takes one as input.
prereqs: [total-order, permutation]
see_also: [social-welfare-function, plurality-voting, condorcet-winner, condorcet-paradox, single-peaked-preferences, kendall-tau-distance, rank-aggregation, arrow-impossibility-theorem]
sources:
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 1 (the editors, Introduction to computational social choice) and Chapter 2 (William S. Zwicker, Introduction to the theory of voting)"
  - book: "Kenneth J. Arrow, Social Choice and Individual Values, Wiley, 1951; second edition, Yale University Press, 1963"
    title: Social Choice and Individual Values
    locator: the definition of individual orderings and of the social welfare function on lists of them
---

A preference profile is the list of the preferences of all voters over a fixed set of candidates, one ranking per voter. It is the input of every voting rule on ranked ballots, from [plurality voting](/plurality-voting/) to the [Borda count](/borda-count/), and of every [social welfare function](/social-welfare-function/). Most axioms of social choice compare the result on two profiles, so the exact form of a profile matters.

## Definition

Let $A$ be a finite set of $m$ candidates (also called alternatives) and $N = \{1, \ldots, n\}$ a finite set of voters. A *preference* of a voter is a linear order $\succ$ on $A$: a relation that is

- *irreflexive*: no $a \succ a$,
- *transitive*: $a \succ b$ and $b \succ c$ imply $a \succ c$,
- *complete*: for $a \ne b$, $a \succ b$ or $b \succ a$.

This is a strict [total order](/total-order/), the same thing as a ranking of the $m$ candidates from best to worst. Write $\mathcal{L}(A)$ for the set of all linear orders on $A$; it has $m!$ elements, one per [permutation](/permutation/) of $A$.

A *preference profile* is an $n$-tuple $P = (\succ_1, \ldots, \succ_n) \in \mathcal{L}(A)^n$, where $\succ_i$ is the preference of voter $i$. There are $(m!)^n$ profiles. The voters are named, so two profiles that differ only by the order of the voters are different profiles; an axiom such as anonymity then says that a rule gives them the same result.

Some quantities derived from a profile appear everywhere:

- $n_P(a, b) = |\{ i : a \succ_i b \}|$, the number of voters who rank $a$ above $b$. For $a \ne b$, $n_P(a, b) + n_P(b, a) = n$.
- The *margin* $n_P(a, b) - n_P(b, a)$ and the *majority relation*: $a$ beats $b$ when the margin is positive. Its graph is the majority graph, and a candidate that beats all others is the [Condorcet winner](/condorcet-winner/).
- The *position* of $a$ in $\succ_i$, from 1 for the top to $m$ for the bottom, and the number of voters that put $a$ in each position. Every scoring rule reads only these numbers.

In code, a ranking is a sequence of the candidates, best first, and a profile is a sequence of $n$ such sequences, $n m$ entries in total. An *anonymous profile*, also called a preference table, stores each distinct ranking once with the number of voters who hold it. It has at most $\min(n, m!)$ rows, and there are $\binom{n + m! - 1}{n}$ anonymous profiles.

A *domain* is a set of allowed profiles. The *unrestricted domain* is $\mathcal{L}(A)^n$; a restricted domain, such as the profiles of [single-peaked preferences](/single-peaked-preferences/), allows only some rankings.

## Examples and non-examples

**A profile of nine voters.** With $A = \{a, b, c\}$, let voters 1 to 4 have $a \succ b \succ c$, voters 5 to 7 have $b \succ c \succ a$, and voters 8 and 9 have $c \succ b \succ a$. As a preference table it has three rows, with counts 4, 3 and 2. Here $n_P(b, a) = 5$, $n_P(b, c) = 7$ and $n_P(a, c) = 4$, so $b$ beats both other candidates. This profile is the worked example of [plurality voting](/plurality-voting/), [approval voting](/approval-voting/) and [instant-runoff voting](/instant-runoff-voting/).

**The Condorcet cycle.** The profile $(a \succ b \succ c,\; b \succ c \succ a,\; c \succ a \succ b)$ has $n_P(a, b) = n_P(b, c) = n_P(c, a) = 2$: every margin around the cycle $a, b, c, a$ is 1. Each voter is transitive, but the majority relation is not; this is the [Condorcet paradox](/condorcet-paradox/).

**Counting.** With 3 candidates and 3 voters there are $6^3 = 216$ profiles and $\binom{8}{3} = 56$ anonymous profiles. The tests of the rule pages of this area check axioms by brute force over all of them.

**Non-example: a cyclic ballot.** A voter who says $a \succ b$, $b \succ c$ and $c \succ a$ does not give a linear order, because transitivity fails. Such a ballot is not part of a profile in this sense, though the majority relation of a profile can look exactly like it.

**Non-example: ties and partial ballots.** A ballot $a \succ \{b, c\}$, which ranks $a$ first and does not order $b$ and $c$, is a weak order, not a linear order. A ballot that lists only $a$ and $b$ is truncated. Both are common in practice, and rules such as [instant-runoff voting](/instant-runoff-voting/) accept truncated ballots, but they are a different domain, and theorems stated for linear orders need not hold on it.

**Non-example: a position vector.** The tuple $(2, 0, 1)$ can mean the ranking "candidate 2, then 0, then 1" or the vector "candidate 0 is in place 2, candidate 1 in place 0, candidate 2 in place 1". These are inverse permutations, and they are the same only for some rankings. A profile must state which one it uses; this page and the code of this area use the first.

## Related definitions

- **Approval profile.** Each voter gives a set of approved candidates, not a ranking ([approval voting](/approval-voting/)). A ranking with a threshold gives such a set.
- **Utility profile.** Each voter has a number $u_i(a)$ for each candidate. It induces a preference profile when no voter has two equal values, and it is the input of mechanisms with money, such as the [VCG mechanism](/vcg-mechanism/).
- **Social welfare function and social choice function.** A map from profiles to a ranking, or to a winner ([social welfare function](/social-welfare-function/)).
- **Distance between rankings.** The [Kendall tau distance](/kendall-tau-distance/) counts the pairs that two rankings order differently. The [Kemeny ranking](/kemeny-rank-aggregation/) of a profile minimizes the total distance to it, a problem of [rank aggregation](/rank-aggregation/).
- **Impartial culture.** The probability model in which each voter's ranking is uniform on $\mathcal{L}(A)$ and independent of the others. It is the usual model for the frequency of the [Condorcet paradox](/condorcet-paradox/).

## References
