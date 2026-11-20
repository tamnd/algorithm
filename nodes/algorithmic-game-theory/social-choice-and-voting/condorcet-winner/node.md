---
tag: QBAWY4
kind: definition
slug: condorcet-winner
name: Condorcet winner
aliases:
- Condorcet candidate
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: A candidate who beats every other candidate in a pairwise majority vote. Condorcet-consistent rules elect one when it exists.
prereqs: [preference-profile]
see_also: [condorcet-paradox, smith-set, copeland-method, ranked-pairs, schulze-method, kemeny-rank-aggregation, median-voter-theorem, plurality-voting]
sources:
  - book: "Marie Jean Antoine Nicolas de Caritat, marquis de Condorcet, Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix, Imprimerie Royale, Paris, 1785"
    title: Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix
    locator: the pairwise majority method and the candidate preferred by a majority to each other candidate
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 2 (William S. Zwicker, Introduction to the theory of voting), Section 2.4 (Condorcet extensions)"
  - paper: "Georges-Théodule Guilbaud, Les théories de l'intérêt général et le problème logique de l'agrégation, Économie Appliquée 5 (1952), 501-584"
    locator: the limit probability that three candidates have no Condorcet winner when every ranking is equally likely
---

A Condorcet winner of a [preference profile](/preference-profile/) is a candidate that a strict majority of the voters prefers to each other candidate, one rival at a time. Condorcet proposed in 1785 that such a candidate, when it exists, should be elected. It need not exist, because pairwise majorities can form a cycle (the [Condorcet paradox](/condorcet-paradox/)), and many common rules, among them [plurality voting](/plurality-voting/), the [Borda count](/borda-count/) and [instant-runoff voting](/instant-runoff-voting/), can fail to elect it when it does.

## Definition

Let $P$ be a profile of $n$ voters with linear orders over a set $A$ of $m$ candidates, and let $n_P(a, b)$ be the number of voters who rank $a$ above $b$.

- Candidate $a$ *beats* $b$ in a pairwise majority vote if $n_P(a, b) > n_P(b, a)$, that is, $2 n_P(a, b) > n$.
- A *Condorcet winner* is a candidate $c$ that beats every other candidate: $2 n_P(c, b) > n$ for all $b \ne c$.
- A *weak Condorcet winner* is a candidate $c$ with $n_P(c, b) \ge n_P(b, c)$ for all $b \ne c$: it beats or ties every other candidate.
- A *Condorcet loser* is a candidate that every other candidate beats.

A voting rule is *Condorcet consistent*, also called a Condorcet extension, if it elects the Condorcet winner, alone, on every profile that has one. A rule satisfies the *Condorcet loser criterion* if it never elects a Condorcet loser.

**Basic facts.**

1. There is at most one Condorcet winner: if $c$ and $c'$ were both, each would beat the other.
2. A Condorcet winner is the unique weak Condorcet winner. With an odd number of voters, every weak Condorcet winner is a Condorcet winner, since no pair can tie.
3. A candidate ranked first by more than half of the voters is the Condorcet winner. The converse fails: in the example below the Condorcet winner has only 3 of 9 first places.
4. When preferences are [single-peaked](/single-peaked-preferences/) and $n$ is odd, the top choice of the median voter is the Condorcet winner ([median voter theorem](/median-voter-theorem/)).

**Finding it.** Store each ranking as a position array, so that one voter's order of $a$ and $b$ is an $O(1)$ test and one pairwise vote is an $O(n)$ count. Run a knockout: keep a current candidate, compare it with each other candidate in turn, and replace it whenever the newcomer beats it. If a Condorcet winner exists, it beats everyone it meets, and once it becomes current it stays, so the survivor is the only possible winner. Check the survivor against all other candidates. This takes $2(m - 1)$ pairwise votes, $O(n m)$ time in total, the size of the input. The full matrix $n_P$, which most Condorcet methods need, takes $O(n m^2)$ time.

## Examples and non-examples

**A Condorcet winner that plurality misses.** With 4 voters $a \succ b \succ c$, 3 voters $b \succ c \succ a$ and 2 voters $c \succ b \succ a$, $b$ beats $a$ by 5 to 4 and $c$ by 7 to 2, so $b$ is the Condorcet winner. [Plurality voting](/plurality-voting/) elects $a$, which is the Condorcet loser here: it loses to $b$ and to $c$ by 4 to 5.

**A Condorcet winner that Borda misses.** With 3 voters $a \succ b \succ c$ and 2 voters $b \succ c \succ a$, $a$ beats $b$ and $c$ by 3 to 2 each, but the Borda scores are $a = 6$, $b = 7$, $c = 2$, and Borda elects $b$.

**A Condorcet winner that instant runoff misses.** With 2 voters $a \succ b \succ c$, 1 voter $b \succ a \succ c$ and 2 voters $c \succ b \succ a$, $b$ beats $a$ and $c$ by 3 to 2 each but has the fewest first places, so [instant-runoff voting](/instant-runoff-voting/) eliminates it first.

**Non-example: a cycle.** The profile $(a \succ b \succ c,\; b \succ c \succ a,\; c \succ a \succ b)$ has $a$ beating $b$, $b$ beating $c$ and $c$ beating $a$, each by 2 to 1. No candidate beats both others, so there is no Condorcet winner and no weak one either.

**Non-example: a tie with an even number of voters.** With 2 voters $a \succ b \succ c$ and $b \succ a \succ c$, $a$ and $b$ tie 1 to 1 and both beat $c$. There is no Condorcet winner, but $a$ and $b$ are both weak Condorcet winners.

**How often it exists.** Let every voter's ranking be uniform and independent (impartial culture), with 3 candidates. Exact enumeration gives the probability of no Condorcet winner as $1/18 \approx 0.056$ for 3 voters, $5/72 \approx 0.069$ for 5 voters and $875/11664 \approx 0.075$ for 7 voters. As $n \to \infty$ over odd values it tends to $1/4 - (3/(2\pi)) \arcsin(1/3) \approx 0.0877$ (Guilbaud 1952). With more candidates the probability grows.

## Related definitions

- **Condorcet methods.** Rules that are Condorcet consistent: the [Copeland method](/copeland-method/), [ranked pairs](/ranked-pairs/), the [Schulze method](/schulze-method/), the [Kemeny rule](/kemeny-rank-aggregation/), the [Dodgson rule](/dodgson-rule/) and the [Slater rule](/slater-rule/). They differ in what they do when there is no Condorcet winner.
- **Smith set.** The smallest nonempty set of candidates that each beat every candidate outside the set ([Smith set](/smith-set/)). It is $\{c\}$ when $c$ is the Condorcet winner.
- **Condorcet paradox.** The cyclic majorities that leave a profile without a Condorcet winner ([Condorcet paradox](/condorcet-paradox/)).
- **Condorcet jury theorem.** A different result of the same author, about the probability that a majority is right ([Condorcet jury theorem](/condorcet-jury-theorem/)).

## References
