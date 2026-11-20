---
tag: M4H0FX
kind: problem
slug: election-control-problem
name: Election control and bribery
aliases:
- electoral control
- bribery in elections
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Decide whether an organizer can make a candidate win by adding or deleting voters or candidates, or by paying voters to change ballots."
prereqs: [voting-manipulation-problem, plurality-voting, np-complete]
see_also: [condorcet-winner, approval-voting, copeland-method, exact-cover-by-3-sets, knapsack-problem, partition-problem, polynomial-time-reduction, single-peaked-preferences]
sources:
  - paper: doi:10.1016/0895-7177(92)90085-Y
    title: "John J. Bartholdi III, Craig A. Tovey and Michael A. Trick, How hard is it to control an election?, Mathematical and Computer Modelling 16(8-9) (1992), 27-40"
    locator: "the types of control by adding, deleting and partitioning candidates or voters, and the results for plurality and for Condorcet voting"
  - paper: doi:10.1613/jair.2676
    title: "Piotr Faliszewski, Edith Hemaspaandra and Lane A. Hemaspaandra, How hard is bribery in elections?, Journal of Artificial Intelligence Research 35 (2009), 485-532"
    locator: "the bribery problems with and without prices and weights, and the results for plurality and approval voting"
  - paper: doi:10.1613/jair.2697
    title: "Piotr Faliszewski, Edith Hemaspaandra, Lane A. Hemaspaandra and Jörg Rothe, Llull and Copeland voting computationally resist bribery and constructive control, Journal of Artificial Intelligence Research 35 (2009), 275-341"
    locator: "the resistance of Copeland voting and Llull's rule to bribery and to constructive control"
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 7 (Piotr Faliszewski and Jörg Rothe), the definitions of immunity, vulnerability and resistance, Theorem 7.3 (control of Condorcet, approval and plurality voting), Theorem 7.4 (control of Copeland voting), Theorem 7.9 (bribery of plurality) and Theorem 7.11 (manipulation reduces to priced bribery)"
---

Election control asks whether the organizer of an election can change its result by changing its structure. The organizer knows the ballots and wants a chosen candidate $p$ to win. The organizer may add or delete a limited number of voters or candidates, or split them into groups that vote in rounds. Bribery is a related problem: an outside agent pays some voters to change their ballots, within a budget. Bartholdi, Tovey and Trick defined control in 1992 and showed that for some rules and some types of control the problem is [NP-complete](/np-complete/), while for others a simple algorithm solves it. Faliszewski, Hemaspaandra and Hemaspaandra defined bribery in 2009. The results are tables: for each rule and each type of action, the problem is impossible, polynomial or NP-hard.

## In plain words

Think of an official who runs an election and wants one candidate to win. The official cannot change any ballot, but can decide who may vote and who may run. Turning away a few voters, or adding a candidate who takes votes from the leader, may change the result. A second kind of cheater pays some voters to vote differently. For each voting rule we can ask whether such a plan is easy to find. For some rules a simple method finds the best plan quickly. For others no fast method is known, and this makes the cheating harder.

## Definition

A voting rule $R$ maps a profile of rankings, or approval ballots, to a set of winners. Each control problem has the rule $R$ fixed, a candidate $p$ and a bound $k$ in the input. The constructive question is whether some allowed change makes $p$ a winner. The destructive question is whether some allowed change makes a given candidate $d$ not a winner. Bartholdi, Tovey and Trick defined these changes:

- **Adding candidates.** There are registered candidates and a set of spoiler candidates. Add at most $k$ spoilers. The voters rank all candidates.
- **Deleting candidates.** Delete at most $k$ candidates other than $p$.
- **Adding voters.** There are registered voters and a pool of unregistered voters with known ballots. Add at most $k$ of them.
- **Deleting voters.** Delete at most $k$ voters.
- **Partitioning candidates or voters.** Split the candidates or the voters into two groups. The winners of a first round go on to a final round, and the rule decides each round.

A rule is immune to a type of control when that action can never make $p$ win if $p$ does not win already. Otherwise it is susceptible. A susceptible rule is vulnerable when the control problem is in P, and resistant when it is NP-hard.

In the bribery problem, the input also has a budget $B$. In the basic form, the briber may change the ballots of at most $B$ voters in any way. In the priced form, voter $i$ has a price $\pi_i$, and the total price of the changed voters must be at most $B$. In the weighted form, voters have integer weights.

## Variants

- **Constructive and destructive.** Each type of control has both forms, and the complexity can differ.
- **Unique winner and co-winner models.** In the first, $p$ must be the only winner. In the second, $p$ must be one of the winners.
- **Priced and weighted bribery.** Prices and weights bring number problems such as [knapsack](/knapsack-problem/) and [partition](/partition-problem/) into the question.
- **Shift bribery and swap bribery.** The briber pays for each place that $p$ moves up in a ballot, or for each swap of two adjacent candidates in a ballot.
- **Multimode control.** The organizer can combine several actions, for example add some voters and delete some candidates.
- **Restricted domains.** For [single-peaked](/single-peaked-preferences/) profiles, some resistant cases become polynomial.

## Examples

- **A spoiler helps.** Under [plurality](/plurality-voting/), two voters rank $a \succ p \succ d$, three rank $p \succ a \succ d$ and two rank $d \succ a \succ p$, where $d$ is a spoiler. With only $a$ and $p$ registered, $a$ has 4 first places and $p$ has 3, so $a$ wins. Adding $d$ moves two first places from $a$ to $d$, and $p$ wins with 3 against 2 and 2. So plurality is susceptible to constructive control by adding candidates.
- **Condorcet voting and candidates.** The rule elects the [Condorcet winner](/condorcet-winner/) if there is one, and no one otherwise. If $p$ is not the Condorcet winner, some rival beats or ties $p$, and adding candidates keeps that rival, so the rule is immune to constructive control by adding candidates. Deleting candidates is easy: delete every candidate that $p$ does not beat, and answer yes exactly when there are at most $k$ of them.
- **Bribery under plurality.** First places are $a = 5$, $b = 4$, $p = 2$ and $c = 1$. Each bribe moves one voter to $p$. Bribe a voter of $a$: $a = 4$, $b = 4$, $p = 3$. Bribe another voter of $a$: $a = 3$, $b = 4$, $p = 4$. Now $p$ is a co-winner with $b$. One bribe cannot be enough, because $p$ would have 3 and some rival at least 4.

## Known algorithms

- **Plurality and voters.** For control by adding voters, add up to $k$ unregistered voters who rank $p$ first. For deleting voters, repeatedly delete a voter whose first choice is a rival with the most first places. Both run in polynomial time, so plurality is vulnerable to these types (Handbook, Theorem 7.3).
- **Plurality bribery.** For unpriced bribery without weights, repeatedly bribe a voter of a rival with the most first places and move that vote to $p$, until $p$ wins or the budget ends. Each bribe raises $p$ by one and lowers the strongest rival by one, which is the best a single bribe can do (Handbook, Theorem 7.9).
- **Condorcet voting and candidates.** Delete the candidates that $p$ does not beat, as in the example.
- **Constant number of candidates.** For many rules, control by voters and bribery become integer programs in a constant number of variables, one per type of ballot, and [Lenstra's algorithm](/lenstra-algorithm/) solves them in polynomial time.
- **Exact search.** For resistant cases, integer programming and search over the at most $k$ changed voters or candidates solve small instances.

## Bounds

- **Plurality.** Constructive control by adding candidates and by deleting candidates is NP-complete (Bartholdi, Tovey and Trick 1992).
- **Condorcet voting.** Constructive control by adding voters and by deleting voters is NP-complete (Bartholdi, Tovey and Trick 1992).
- **Copeland voting.** Copeland voting and Llull's rule resist bribery and many types of constructive control (Faliszewski, Hemaspaandra, Hemaspaandra and Rothe 2009, and Theorem 7.4 of the Handbook).
- **Priced and weighted bribery.** Weights or prices can make bribery hard even for plurality, through problems such as partition, while the basic form is polynomial (Faliszewski, Hemaspaandra and Hemaspaandra 2009).
- **Worst case only.** As with manipulation, these bounds say that some instances are hard unless P = NP, not that typical instances are hard.

## Reductions

- **From exact cover by 3-sets.** Many resistance proofs for control by voters reduce from [exact cover by 3-sets](/exact-cover-by-3-sets/): each added or deleted voter stands for a set, and the candidates stand for the elements to cover.
- **From partition and knapsack.** Weighted and priced bribery inherit hardness from these number problems.
- **From manipulation.** [Manipulation](/voting-manipulation-problem/) reduces to priced bribery: the manipulators get price 0 and the other voters a price above the budget (Handbook, Theorem 7.11). So a rule that is hard to manipulate is hard to bribe in this form.

## Applications

- **Choice of a voting rule.** Resistance to many types of control is an argument for a rule, for example for Copeland voting.
- **Robustness of results.** The least bribe that changes the winner measures how close an election was, and it can guide audits.
- **Campaigns.** Shift bribery models a campaign that spends money to move a candidate up in the rankings of voters.

## References
