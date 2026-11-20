---
tag: PK39JS
kind: theorem
slug: gibbard-satterthwaite-theorem
name: Gibbard-Satterthwaite theorem
aliases:
- Gibbard-Satterthwaite
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Every deterministic voting rule with at least three possible winners that is strategyproof is a dictatorship.
prereqs: [arrow-impossibility-theorem, social-welfare-function]
see_also: [arrow-impossibility-theorem, voting-manipulation-problem, dominant-strategy-incentive-compatibility, revelation-principle, median-voter-theorem, generalized-median-voter-rule, single-peaked-preferences, roberts-theorem]
sources:
  - paper: doi:10.2307/1914083
    title: "Allan Gibbard, Manipulation of voting schemes, a general result, Econometrica 41(4) (1973), 587-601"
    locator: the main theorem, that every nondictatorial game form with at least three outcomes can be manipulated
  - paper: doi:10.1016/0022-0531(75)90050-2
    title: "Mark A. Satterthwaite, Strategy-proofness and Arrow's conditions: existence and correspondence theorems for voting procedures and social welfare functions, Journal of Economic Theory 10(2) (1975), 187-217"
    locator: the theorem that a strategyproof voting procedure with at least three outcomes is dictatorial, and its correspondence with Arrow's conditions
  - paper: "Allan Gibbard, Manipulation of schemes that mix voting with chance, Econometrica 45(3) (1977), 665-681"
    locator: the characterization of strategyproof randomized rules as mixtures of unilateral and duple rules
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: "Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on social choice (the proof of the Gibbard-Satterthwaite theorem by reduction to Arrow's theorem)"
---

The Gibbard-Satterthwaite theorem says that every deterministic voting rule with at least three possible winners can be manipulated, unless it is a dictatorship: for some profile, some voter gets a better result by reporting a ranking that is not their true one. Allan Gibbard proved it in 1973 and Mark Satterthwaite, independently, in 1975. It is the strategic counterpart of [Arrow's impossibility theorem](/arrow-impossibility-theorem/), and it is the reason that mechanism design without money looks for restricted domains, randomization or payments.

## Statement

Let $A$ be a finite set of candidates, $N = \{1, \ldots, n\}$ the voters and $\mathcal{L}(A)$ the linear orders on $A$. A *voting rule*, or social choice function, is a map $f : \mathcal{L}(A)^n \to A$, defined on every profile. For a profile $P = (\succ_1, \ldots, \succ_n)$ write $(P_{-i}, \succ')$ for $P$ with voter $i$'s ranking replaced by $\succ'$.

- $f$ is *strategyproof* if no voter can gain by lying: for all $P$, all $i$ and all $\succ' \in \mathcal{L}(A)$, it is not the case that $f(P_{-i}, \succ') \succ_i f(P)$. Truthful reporting is then a dominant strategy for every voter ([dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/)).
- $f$ is *onto* if every candidate is $f(P)$ for some profile $P$.
- $f$ is a *dictatorship* if there is a voter $d$ such that $f(P)$ is the top candidate of $\succ_d$ for every $P$.

**Theorem (Gibbard 1973, Satterthwaite 1975).** If $|A| \ge 3$ and $f$ is onto and strategyproof, then $f$ is a dictatorship.

**Range form.** If $f$ is strategyproof and its range $R = f(\mathcal{L}(A)^n)$ has at least 3 candidates, then there is a voter $d$ such that $f(P)$ is the candidate of $R$ that $d$ ranks highest, for every $P$. This follows from the onto form, as shown after the proof.

## In plain words

A voting rule asks every voter for a ranking and picks a winner. We would like a rule where telling the truth is always the best thing to do, whatever the others say. If the rule can elect at least three different candidates, this is impossible, except for one bad rule: always elect the favourite of one fixed voter. Every other rule has some situation where a voter does better by reporting a false ranking, for example by voting for a less preferred candidate who has a real chance to win.

## Proof

The proof reduces the theorem to Arrow's theorem, as in Nisan's chapter of the Algorithmic Game Theory book. Let $f$ be onto and strategyproof with $|A| \ge 3$. For a profile $P$ and a set $S \subseteq A$, let $P^S$ be the profile in which every voter moves the candidates of $S$ to the top, keeping their order inside $S$ and outside $S$.

*Lemma 1 (monotonicity).* Let $f(P) = a$, and let $P'$ be a profile in which $a$ drops against no candidate: for every voter $i$ and every $x$, $a \succ_i x$ implies $a \succ'_i x$. Then $f(P') = a$.

Change the voters from $P$ to $P'$ one at a time. Suppose the outcome first changes when voter $i$ switches from $\succ_i$ to $\succ'_i$, from $a$ to some $b \ne a$. If $b \succ_i a$, voter $i$ with true ranking $\succ_i$ gains by reporting $\succ'_i$, which strategyproofness forbids. So $a \succ_i b$, and then $a \succ'_i b$ by the assumption on $P'$. But then voter $i$ with true ranking $\succ'_i$ gains by reporting $\succ_i$, which gives $a$. This is a contradiction, so the outcome stays $a$.

*Lemma 2 (Pareto).* If every voter ranks $a$ above $b$ in $P$, then $f(P) \ne b$.

Since $f$ is onto, $f(Q) = a$ for some $Q$. In $P^{\{a, b\}}$ every voter ranks $a$ first, so $a$ drops against no candidate from $Q$ to $P^{\{a, b\}}$, and $f(P^{\{a, b\}}) = a$ by Lemma 1. If $f(P) = b$, then from $P$ to $P^{\{a, b\}}$ the candidate $b$ rises to second place behind $a$, who was already above it, so $b$ drops against no candidate and Lemma 1 gives $f(P^{\{a, b\}}) = b$, a contradiction.

*The social welfare function.* For a profile $P$ and candidates $a \ne b$, define $a \succ_{F(P)} b$ if $f(P^{\{a, b\}}) = a$. By Lemma 2, $f(P^{\{a, b\}}) \in \{a, b\}$, since every other candidate is below both $a$ and $b$ for every voter. So $F(P)$ orders each pair in exactly one way. It is transitive: suppose $a \succ_{F(P)} b$, $b \succ_{F(P)} c$ and $c \succ_{F(P)} a$, and let $x = f(P^{\{a, b, c\}})$, which is in $\{a, b, c\}$ by Lemma 2. Say $x = a$; the other cases are the same up to renaming. From $P^{\{a, b, c\}}$ to $P^{\{a, c\}}$ only $b$ moves down, so $a$ drops against no candidate, and Lemma 1 gives $f(P^{\{a, c\}}) = a$, that is, $a \succ_{F(P)} c$, a contradiction. So $F$ is a social welfare function.

- *Pareto.* If every voter ranks $a$ above $b$, then so does every voter in $P^{\{a, b\}}$, and Lemma 2 gives $f(P^{\{a, b\}}) = a$.
- *IIA.* If every voter orders $a$ and $b$ the same way in $P$ and $Q$, then $P^{\{a, b\}}$ and $Q^{\{a, b\}}$ have the same top two places for every voter and differ only below them. Change the voters one at a time; the winner is $a$ or $b$, it stays above every other candidate and keeps its order with the other one of the pair, so by Lemma 1 it does not change. Hence $f(P^{\{a, b\}}) = f(Q^{\{a, b\}})$.

By Arrow's theorem, $F$ has a dictator $d$.

*$d$ is a dictator for $f$.* Let $a$ be the top of $\succ_d$ in $P$ and suppose $f(P) = b \ne a$. Since $d$ ranks $a$ above $b$, $a \succ_{F(P)} b$, so $f(P^{\{a, b\}}) = a$. But from $P$ to $P^{\{a, b\}}$ the candidate $b$ only rises against the candidates outside $\{a, b\}$ and keeps its order with $a$, so Lemma 1 gives $f(P^{\{a, b\}}) = b$, a contradiction. So $f(P)$ is always the top of $\succ_d$. $\blacksquare$

*The range form.* Let $f$ be strategyproof with range $R$, $|R| \ge 3$. If $P$ and $Q$ both have $R$ on top for every voter, in the same order, then $f(P) = f(Q)$: change the voters one at a time, and use Lemma 1 with the winner, which is in $R$, above every candidate outside $R$. Also $f(P) = f(P^R)$ by Lemma 1. So $f(P)$ depends only on each voter's order of $R$, and this defines a rule $g$ on $\mathcal{L}(R)^n$ that is onto $R$ and strategyproof, since a lie to $g$ is a lie to $f$. The onto form applied to $g$ gives the dictator.

## Consequences

- **Common rules can be manipulated.** Take [plurality voting](/plurality-voting/) with ties broken towards the first candidate, and the voters $a \succ b \succ c$, $b \succ a \succ c$ and $c \succ b \succ a$. Each candidate has one vote and $a$ wins, the last choice of voter 3. If voter 3 reports $b \succ c \succ a$, $b$ wins with two votes, which voter 3 prefers to $a$. The theorem says that the [Borda count](/borda-count/), [instant-runoff voting](/instant-runoff-voting/) and every [Condorcet method](/condorcet-winner/) can also be manipulated on some profile. [Approval voting](/approval-voting/) is outside the model, since its ballots are sets and not rankings.
- **Mechanism design without money.** By the [revelation principle](/revelation-principle/), any mechanism with dominant strategies can be replaced by a strategyproof direct rule with the same outcomes. So the theorem limits every mechanism, not only voting rules, when the outcome is chosen without payments from at least three options on the full domain of preferences.
- **Hardness as a barrier.** Since manipulation cannot be ruled out, computational social choice asks how hard it is to find. The [voting manipulation problem](/voting-manipulation-problem/) is the computational question: given the other votes, find a manipulating ballot. It is easy for plurality and Borda, and NP-hard for some rules, for example instant-runoff voting (Bartholdi and Orlin 1991). This is a worst-case statement; the theorem itself is about existence.
- **Arrow and Gibbard-Satterthwaite.** The proof above turns a strategyproof rule into an Arrovian social welfare function. Satterthwaite showed a correspondence between the two sets of conditions in this sense.

## Tightness

- **At least three possible winners.** With two candidates, majority rule with a fixed tie-break is strategyproof and not a dictatorship: a voter can only help the side they report. The same holds for a rule on many candidates whose range has two elements, such as a majority vote between $a$ and $b$ that ignores the others.
- **Onto, or a large range.** A constant rule is strategyproof and has no dictator, but its range has one element.
- **Deterministic rules.** Random dictatorship, which picks a voter uniformly at random and elects that voter's top choice, is strategyproof in expected utility and treats all voters equally. Gibbard (1977) showed that the strategyproof randomized rules are exactly the mixtures of unilateral rules, which depend on one voter, and duple rules, which choose between two fixed candidates.
- **Unrestricted domain.** If preferences are [single-peaked](/single-peaked-preferences/) on a known axis, electing the median of the voters' peaks is strategyproof and not dictatorial ([median voter theorem](/median-voter-theorem/)); the [generalized median voter rules](/generalized-median-voter-rule/) are all such rules.
- **No money.** With quasilinear utilities and payments, VCG mechanisms are strategyproof and not dictatorial. Without restrictions on the valuations, [Roberts' theorem](/roberts-theorem/) shows that these are essentially the only ones.

## History

Gibbard proved the theorem in 1973 for game forms, mechanisms in which the voters choose strategies of any kind, and derived the result for voting rules by the revelation argument. Satterthwaite proved it in his 1973 thesis and published it in 1975, with the correspondence to Arrow's conditions. The question was older: Dummett and Farquharson had conjectured in 1961 that every reasonable voting rule can be manipulated. Gibbard extended the result to randomized rules in 1977. From 1989, the work of Bartholdi, Tovey and Trick on the complexity of manipulation started the computational study of the theorem's consequences.

## References
