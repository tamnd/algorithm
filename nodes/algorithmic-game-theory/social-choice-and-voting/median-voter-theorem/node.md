---
tag: SZQKY5
kind: theorem
slug: median-voter-theorem
name: Median voter theorem
aliases:
- Black's theorem
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: On a single-peaked profile the peak of the median voter is a weak Condorcet winner. With an odd number of voters it is the Condorcet winner and majority voting is transitive.
prereqs: [single-peaked-preferences, condorcet-winner]
see_also: [condorcet-paradox, arrow-impossibility-theorem, generalized-median-voter-rule, single-peaked-recognition, gibbard-satterthwaite-theorem, facility-location-mechanism, median, may-theorem]
sources:
  - paper: doi:10.1086/256633
    title: "Duncan Black, On the rationale of group decision-making, Journal of Political Economy 56(1) (1948), 23-34"
    locator: the majority winner at the median optimum for single-peaked curves of preference
  - paper: arxiv:2205.09092
    title: "Edith Elkind, Martin Lackner and Dominik Peters, Preference restrictions in computational social choice: a survey, arXiv 2205.09092, version 2, March 2025"
    locator: "Section 3.2, Proposition 3.4 (median voter theorem), the remark on even numbers of voters, and Corollary 3.5 (transitivity for an odd number of voters)"
  - paper: doi:10.1007/BF00128122
    title: "Hervé Moulin, On strategy-proofness and single peakedness, Public Choice 35(4) (1980), 437-455"
    locator: the median of the peaks as a strategyproof voting scheme on the single-peaked domain
---

The median voter theorem says that on a [single-peaked](/single-peaked-preferences/) profile the favourite candidate of the median voter cannot lose a pairwise majority vote. Here the voters are sorted by the position of their peaks on the axis, and the median voter is the one in the middle. With an odd number of voters this candidate is the [Condorcet winner](/condorcet-winner/), and the whole majority relation is a transitive ranking, so the [Condorcet paradox](/condorcet-paradox/) cannot occur. The result is due to Black (1948).

## Statement

Let $A$ be a set of $m$ candidates with an axis $\lhd$, and let $(\succ_1, \ldots, \succ_n)$ be a profile of strict rankings of $A$, each one single-peaked on $\lhd$. Write $p_i$ for the peak of voter $i$, number the voters so that $p_1 \unlhd p_2 \unlhd \cdots \unlhd p_n$, where $\unlhd$ means $\lhd$ or equal. Say that $a$ beats $b$ if more than $n/2$ voters rank $a$ above $b$, and that $a$ weakly beats $b$ if at least $n/2$ voters do.

**Theorem.**

1. **(odd $n$)** If $n$ is odd, let $c = p_{(n+1)/2}$. Then for every candidate $a \ne c$ at least $(n+1)/2$ voters rank $c$ above $a$, so $c$ is the Condorcet winner.
2. **(transitivity)** If $n$ is odd, the majority relation is a strict linear order of $A$, and this order is itself single-peaked on $\lhd$.
3. **(even $n$)** If $n$ is even, the set of weak Condorcet winners, the candidates that weakly beat every other candidate, is the interval $\{c : p_{n/2} \unlhd c \unlhd p_{n/2+1}\}$ of the axis. It is never empty.

## In plain words

Put the candidates on a line, from left to right, and suppose that each voter has a favourite place on the line and likes the candidates less as they get farther from it. Sort the voters by their favourite place and look at the voter in the middle. Any candidate to the right of this voter's favourite is liked less than it by the middle voter and by everyone to the left of the middle voter, and that is a majority. The same holds on the other side. So the middle voter's favourite wins every head-to-head vote, and with an odd number of voters the group has a clear ranking with no cycles.

## Proof

**Lemma 1.** Let voter $i$ have peak $p_i$, and let $c$ and $a$ be candidates. If $p_i \unlhd c \lhd a$ or $a \lhd c \unlhd p_i$, then $c \succ_i a$.

*Proof.* If $p_i = c$, then $c$ is the top of $\succ_i$. Otherwise $p_i \lhd c \lhd a$ or $a \lhd c \lhd p_i$, and the definition of single-peakedness gives $c \succ_i a$. $\square$

**Part 1.** Let $n$ be odd, $h = (n+1)/2$ and $c = p_h$. Take $a \ne c$. If $c \lhd a$, then each voter $i \le h$ has $p_i \unlhd p_h = c \lhd a$, so $c \succ_i a$ by Lemma 1. That is $h = (n+1)/2$ voters. If $a \lhd c$, then each voter $i \ge h$ has $a \lhd c = p_h \unlhd p_i$, and again $n - h + 1 = (n+1)/2$ voters rank $c$ above $a$. Since $(n+1)/2 > n/2$, $c$ beats every other candidate. $\square$

**Part 2.** Let $n$ be odd. Each voter ranks $a$ above $b$ or $b$ above $a$, so for $a \ne b$ exactly one of the two beats the other: the majority relation is complete and asymmetric. Take three candidates $T = \{a, b, c\}$. The restriction of each ranking to $T$ has no valley on the restriction of $\lhd$ to $T$, so the restricted profile is single-peaked, and by Part 1 it has a Condorcet winner. Pairwise counts do not change when other candidates are removed, so the majority relation has no cycle $a \to b \to c \to a$ on $T$. Now let $a$ beat $b$ and $b$ beat $c$. If $c$ beat $a$, this would be such a cycle, so $a$ beats $c$ by completeness. Hence the relation is transitive, and a complete, asymmetric, transitive relation is a strict linear order.

For the second claim, take $a \lhd b \lhd c$. No voter has a valley at $b$, so each voter ranks $b$ above $a$ or above $c$, and the two counts $|\{i : b \succ_i a\}|$ and $|\{i : b \succ_i c\}|$ add up to at least $n$. One of them is at least $n/2$, hence at least $(n+1)/2$ since $n$ is odd, so $b$ beats $a$ or $c$. Then $b$ is not below both in the majority order, and the order has no valley. $\square$

**Part 3.** Let $n$ be even, $h = n/2$, and let $I = \{c : p_h \unlhd c \unlhd p_{h+1}\}$. It contains $p_h$, so it is not empty.

Take $c \in I$ and $a \ne c$. If $c \lhd a$, then each voter $i \le h$ has $p_i \unlhd p_h \unlhd c \lhd a$ and ranks $c$ above $a$ by Lemma 1: that is $n/2$ voters. If $a \lhd c$, the $n/2$ voters $i \ge h + 1$ rank $c$ above $a$ in the same way. So $c$ weakly beats every other candidate.

Take $c \notin I$, say $c \lhd p_h$, and let $d = p_h$. Each voter $i \ge h$ has $c \lhd d \unlhd p_i$ and ranks $d$ above $c$. These are $n/2 + 1$ voters, so $d$ beats $c$ and $c$ is not a weak Condorcet winner. The case $p_{h+1} \lhd c$ is symmetric, with $d = p_{h+1}$ and the voters $i \le h + 1$. $\square$

## Consequences

- **Condorcet methods agree.** Every Condorcet consistent rule, for example the [Copeland method](/copeland-method/), [ranked pairs](/ranked-pairs/), the [Schulze method](/schulze-method/) and [Kemeny rank aggregation](/kemeny-rank-aggregation/), elects the median peak on a single-peaked profile with an odd number of voters. [Plurality voting](/plurality-voting/) does not: with the axis $0 \lhd 1 \lhd 2$, two voters $012$, two voters $210$ and one voter $102$, plurality elects $0$ by the fixed tie-break, while the median peak $1$ beats both other candidates.
- **An escape from Arrow.** With an odd number of voters, at least 3, pairwise majority is a social welfare function on the single-peaked domain. It satisfies the Pareto condition, independence of irrelevant alternatives and non-dictatorship, so the [Arrow impossibility theorem](/arrow-impossibility-theorem/) needs a domain larger than this one.
- **Strategyproof voting.** The rule that elects the median peak is strategyproof on this domain: a voter can move the median only away from its own peak. Moulin (1980) characterized all such rules; see the [generalized median voter rule](/generalized-median-voter-rule/). This is why the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) fails on single-peaked profiles.
- **Peaks are enough.** To find the Condorcet winner it suffices to know the axis and the peaks: it is a [median](/median/) of $n$ positions, which takes $O(n)$ time.

## Tightness

- **An even number of voters.** With the axis $0 \lhd 1 \lhd 2$ and the two voters $012$ and $120$, the candidates $0$ and $1$ tie, $1$ beats $2$ by $2$ to $0$, and $0$ and $2$ tie. There is no Condorcet winner, both $0$ and $1$ are weak Condorcet winners, and the relation "ties with" is not transitive. So in Part 2 the odd number of voters is needed.
- **Strict rankings.** The proof of Part 2 uses that every voter ranks every pair. If voters may be indifferent, ties come back even for an odd number of voters: with the voters $012$ and $210$ and a third voter who likes all three candidates equally, every pair ties, and the majority relation is not a linear order.
- **Single-peakedness.** The profile $012$, $120$, $201$ is not single-peaked and has the majority cycle $0 \to 1 \to 2 \to 0$, so the theorem fails without the domain condition. A profile that is single-peaked on an axis for each voter separately, but not on a common axis, is no better.
- **The median of the peaks, not of the axis.** The winner is the median of the voters' peaks. It can be far from the middle of the axis: if most voters have peaks at the left end, the winner is at the left end.

## History

Black (1948) stated the theorem for committees voting on motions with single-peaked curves of preference, and he expanded it in his book The Theory of Committees and Elections (1958). Arrow (1951) found the same domain condition independently and used it as the main example of a domain on which majority voting gives a social welfare function. Moulin (1980) moved the focus to strategyproofness, and Elkind, Lackner and Peters survey the modern algorithmic results on this and other restricted domains.

## References
