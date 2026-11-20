---
tag: B9YY4A
kind: definition
slug: single-peaked-preferences
name: Single-peaked preferences
aliases:
- single-peakedness
- single-peaked profile
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: A profile is single-peaked if the candidates can be put on a line so that each voter likes candidates less the farther they lie from the voter's favourite.
prereqs: [preference-profile]
see_also: [median-voter-theorem, single-peaked-recognition, generalized-median-voter-rule, condorcet-paradox, condorcet-winner, chamberlin-courant-rule, gibbard-satterthwaite-theorem, unimodal-function]
sources:
  - paper: doi:10.1086/256633
    title: "Duncan Black, On the rationale of group decision-making, Journal of Political Economy 56(1) (1948), 23-34"
    locator: the single-peaked curves of preference and the majority winner at the median peak
  - paper: arxiv:2205.09092
    title: "Edith Elkind, Martin Lackner and Dominik Peters, Preference restrictions in computational social choice: a survey, arXiv 2205.09092, version 2, March 2025"
    locator: "Section 3.2 (the definition, the equivalent conditions of Proposition 3.3 and the counting results) and Section 3.4 (Euclidean preferences, Example 14)"
  - paper: doi:10.1007/BF00128122
    title: "Hervé Moulin, On strategy-proofness and single peakedness, Public Choice 35(4) (1980), 437-455"
    locator: the strategyproof voting schemes on the single-peaked domain
---

A [preference profile](/preference-profile/) is single-peaked if the candidates can be put in a left-to-right order, the axis, so that every voter has one favourite candidate, the peak, and likes candidates less the farther they are from the peak on each side. The idea is due to Black (1948), who used it to show that majority voting then has a winner. It is the standard model of a vote on one numerical quantity, such as a budget or a tax rate, or of parties on a left-right scale. On this domain the [Condorcet paradox](/condorcet-paradox/) cannot occur, and simple strategyproof rules exist.

## Definition

Let $A$ be a finite set of $m$ candidates and let $\lhd$ be a linear order on $A$, the axis. A ranking $\succ$ of $A$ with top candidate $p$ is **single-peaked on $\lhd$** if for all candidates $a$ and $b$,

$$p \lhd b \lhd a \ \text{ or } \ a \lhd b \lhd p \quad \Longrightarrow \quad b \succ a.$$

So the ranking goes down on both sides of the peak. A profile $(\succ_1, \ldots, \succ_n)$ is **single-peaked on $\lhd$** if each of its rankings is single-peaked on the same axis $\lhd$, and it is **single-peaked** if there is at least one such axis. The axis is a property of the whole profile: a profile in which each ranking is single-peaked on some axis of its own is not single-peaked in general.

For a ranking $\succ$ and an axis $\lhd$ the following conditions are equivalent (Elkind, Lackner and Peters, Proposition 3.3):

1. $\succ$ is single-peaked on $\lhd$.
2. There is no valley: no three candidates $a \lhd b \lhd c$ with $a \succ b$ and $c \succ b$.
3. There is no valley on three candidates that are adjacent on the axis.
4. For each $k = 1, \ldots, m$, the $k$ best candidates of $\succ$ form an interval of $\lhd$.

Condition 2 shows that single-peakedness is kept when candidates are removed: a profile single-peaked on $\lhd$ stays single-peaked on the restriction of $\lhd$ to any subset of candidates. Condition 4 shows that the bottom candidate of each voter is one of the two ends of the axis. Both facts drive the recognition algorithm.

## Examples and non-examples

- **All rankings on one axis.** Take $m = 4$ and the axis $0 \lhd 1 \lhd 2 \lhd 3$. The rankings single-peaked on it, best first, are $0123$, $1023$, $1203$, $1230$, $2103$, $2130$, $2310$ and $3210$. Read from the bottom, each ranking chooses one of the two ends of the remaining interval, $m - 1$ times, so there are exactly $2^{m-1}$ of them out of $m! = 24$.
- **A ranking that is not single-peaked on this axis.** The ranking $1320$ puts $1$ and $3$ above $2$, and $1 \lhd 2 \lhd 3$, so there is a valley at $2$. Its top two candidates $\{1, 3\}$ are not an interval. The same ranking is single-peaked on the axis $0 \lhd 2 \lhd 3 \lhd 1$, so it can belong to a single-peaked profile with a different axis.
- **The Condorcet cycle.** The profile $012$, $120$, $201$ of the [Condorcet paradox](/condorcet-paradox/) is not single-peaked. Each candidate is last for some voter, and only the two ends of an axis can be last. In general, a profile in which three different candidates are each ranked last by some voter is not single-peaked.
- **Many axes.** A profile is single-peaked on an axis exactly when it is single-peaked on the reversed axis, so a single-peaked profile has at least two axes. A profile with one ranking is single-peaked on $2^{m-1}$ axes.
- **Euclidean preferences.** Put each voter and each candidate at a point of the real line, and let each voter rank the candidates by distance, nearest first, with no ties. Then the profile is single-peaked on the order of the candidate points. The converse is false: some single-peaked profiles cannot be drawn in this way (Elkind, Lackner and Peters, Example 14).
- **Not a unimodal function.** A [unimodal function](/unimodal-function/), also called a single-peaked function, is one numerical function on an ordered domain with one local maximum. A single-peaked profile is a set of rankings, with no numbers, and the axis is not given: it must be the same for all voters and it may have to be found.

## Related definitions

- **Median voter.** On a single-peaked profile with an odd number of voters, the peak of the median voter is the [Condorcet winner](/condorcet-winner/), and the majority relation is transitive. This is the [median voter theorem](/median-voter-theorem/).
- **Recognition.** Whether a profile is single-peaked, and on which axis, can be decided in time $O(mn)$ for $n$ voters; see [recognizing single-peaked profiles](/single-peaked-recognition/).
- **Strategyproof rules.** On the single-peaked domain the median of the peaks, and more generally the [generalized median voter rules](/generalized-median-voter-rule/) of Moulin (1980), are strategyproof. This escapes the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/), which needs the full domain. The same rules appear as mechanisms for [facility location](/facility-location-mechanism/).
- **Multiwinner rules.** Some rules that are NP-hard in general, such as the [Chamberlin-Courant rule](/chamberlin-courant-rule/), become polynomial on single-peaked profiles.
- **Wider domains.** Single-peakedness on a tree, on a circle and in several dimensions, single-crossing profiles and value restriction all generalize parts of the idea (Elkind, Lackner and Peters, Chapter 3).

## References
