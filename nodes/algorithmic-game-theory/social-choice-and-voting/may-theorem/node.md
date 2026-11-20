---
tag: VKZR66
kind: theorem
slug: may-theorem
name: "May's theorem"
aliases:
- majority rule characterization
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: With two candidates, majority rule is the only voting rule that is anonymous, neutral and positively responsive.
prereqs: [preference-profile]
see_also: [plurality-voting, arrow-impossibility-theorem, gibbard-satterthwaite-theorem, condorcet-jury-theorem, social-welfare-function, condorcet-winner, weighted-majority, approval-voting]
sources:
  - paper: doi:10.2307/1907651
    title: "Kenneth O. May, A set of independent necessary and sufficient conditions for simple majority decision, Econometrica 20(4) (1952), 680-684"
    locator: "the main theorem (decisiveness, anonymity, neutrality and positive responsiveness) and the independence of the four conditions"
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 2 (William S. Zwicker, Introduction to the theory of voting)"
---

May's theorem says that, for a choice between two candidates, simple majority rule is the only rule that is decisive, anonymous, neutral and positively responsive. Kenneth May proved it in 1952. It is the positive counterpart of [Arrow's impossibility theorem](/arrow-impossibility-theorem/): with two candidates a few natural conditions pin down one rule, while with three or more no rule meets Arrow's conditions.

## Statement

There are two candidates $a$ and $b$ and $n \ge 1$ voters. Voter $i$ reports $D_i \in \{1, 0, -1\}$: $1$ for "$a$ is better", $-1$ for "$b$ is better" and $0$ for indifference. A *group decision function* maps each profile $D = (D_1, \ldots, D_n)$ to an outcome $F(D) \in \{1, 0, -1\}$, where $0$ is a social tie. Write $p(D)$ and $q(D)$ for the number of voters with $D_i = 1$ and with $D_i = -1$. *Simple majority rule* is

$$F(D) = \operatorname{sign}(p(D) - q(D)).$$

The four conditions are:

1. **Decisive.** $F$ is defined on all $3^n$ profiles and gives exactly one outcome for each.
2. **Anonymous.** $F(D_{\sigma(1)}, \ldots, D_{\sigma(n)}) = F(D)$ for every permutation $\sigma$ of the voters.
3. **Neutral.** $F(-D) = -F(D)$: swapping the names of the two candidates in every report swaps the outcome.
4. **Positively responsive.** If $F(D) \in \{0, 1\}$, and $D'$ arises from $D$ when some voters move towards $a$ ($D'_i \ge D_i$ for all $i$, with $D' \ne D$), then $F(D') = 1$.

**Theorem (May 1952).** A group decision function satisfies conditions 1 to 4 if and only if it is simple majority rule.

When voters must give strict preferences, the profiles are $\{1, -1\}^n$ and the same proof works; for odd $n$ there are no social ties.

## In plain words

Suppose a group must choose between two options. Treat all voters the same, and treat both options the same. If the result is a tie or a win for one option, and someone then moves towards that option, the option must win outright. These demands sound mild. Together they leave only one rule: count the votes for each side and pick the side with more, with a tie when the counts are equal.

## Proof

Majority rule meets the four conditions. It is defined everywhere. It depends on $D$ only through $p$ and $q$, which do not change when the voters are permuted. Replacing $D$ by $-D$ swaps $p$ and $q$ and so changes the sign. If $p - q \ge 0$ and $D' \ge D$ with $D' \ne D$, then some voter moved up by 1 or 2, so $p(D') - q(D') \ge p - q + 1 > 0$ and $F(D') = 1$.

For the converse, let $F$ satisfy the four conditions.

*Step 1: $F$ depends only on $(p, q)$.* Two profiles with the same counts $p$ and $q$ differ by a permutation of the voters, so by anonymity they have the same outcome. Write $F(p, q)$.

*Step 2: equal counts give a tie.* Let $p(D) = q(D) = k$. Then $-D$ also has $k$ ones and $k$ minus ones, so $F(-D) = F(D)$ by Step 1, and $F(-D) = -F(D)$ by neutrality. Hence $F(D) = 0$.

*Step 3: more votes for $a$ give $a$.* Let $p(D) > q(D)$. Pick $p(D) - q(D)$ voters with $D_i = 1$ and set their reports to $0$; call the result $E$. Then $p(E) = q(E) = q(D)$, so $F(E) = 0$ by Step 2. Now $D$ arises from $E$ when those voters move back towards $a$, so $D \ge E$ and $D \ne E$, and positive responsiveness gives $F(D) = 1$.

*Step 4: more votes for $b$ give $b$.* If $p(D) < q(D)$, then $p(-D) > q(-D)$, so $F(-D) = 1$ by Step 3, and $F(D) = -1$ by neutrality.

Steps 2 to 4 give $F(D) = \operatorname{sign}(p(D) - q(D))$ on every profile, and decisiveness says that $F$ has no other values to fix. $\blacksquare$

The proof uses positive responsiveness only from a tie, and only for voters who move from indifference to $a$. A brute-force search over all anonymous functions for $n \le 4$, which are functions of $(p, q)$, confirms that majority is the only one that is neutral and positively responsive.

## Consequences

- **Two-candidate elections have one sensible rule.** With two candidates, [plurality voting](/plurality-voting/), [instant-runoff voting](/instant-runoff-voting/), the [Borda count](/borda-count/) and [approval voting](/approval-voting/) with sincere ballots all reduce to majority rule, up to how they break a tie. May's theorem explains why: any rule with these four properties must agree with them.
- **Majority with two candidates escapes the impossibility theorems.** It satisfies Pareto, independence of irrelevant alternatives and nondictatorship, so [Arrow's theorem](/arrow-impossibility-theorem/) needs three candidates. It is also strategyproof, since a voter can only help the side they report, so the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) needs at least three possible outcomes.
- **Pairwise majority as a building block.** Condorcet methods apply majority to each pair of candidates. May's theorem justifies each pairwise vote, and the [Condorcet paradox](/condorcet-paradox/) shows that the pairwise results need not fit into one ranking.
- **An epistemic counterpart.** The [Condorcet jury theorem](/condorcet-jury-theorem/) gives a different reason for majority rule on two options: if voters are independent and each is right with probability above $1/2$, the majority is right more often than any single voter.

## Tightness

Each of the four conditions is needed: for each one there is a rule that meets the other three and is not majority rule.

- **Without anonymity: weighted majority.** Give voter $i$ a weight $w_i > 0$ and let $F(D) = \operatorname{sign}(\sum_i w_i D_i)$. It is decisive and neutral, and positively responsive because a move towards $a$ raises the sum by at least $\min_i w_i$ when it was 0 or more. With weights $(2, 1, 1)$, the profile $(1, -1, -1)$ is a tie, not a win for $b$. The same form is the [weighted majority](/weighted-majority/) vote of online learning.
- **Without neutrality: majority with ties to $a$.** Let $F(D) = 1$ if $p \ge q$ and $-1$ otherwise. It is decisive, anonymous and positively responsive, but not neutral: when all voters are indifferent, both $D$ and $-D$ give $a$.
- **Without positive responsiveness: the constant tie.** $F \equiv 0$ is decisive, anonymous and neutral. A weaker monotonicity condition, which only forbids a move towards $a$ from hurting $a$, allows more rules, for example the rule that declares a tie unless one side leads by at least $k \ge 2$ votes.
- **Without decisiveness.** A rule that gives no outcome, or several, on some profiles is not a group decision function in May's sense. For example, majority rule that is undefined at a tie meets the other three conditions where it is defined.

May (1952) proved that the four conditions are independent in this sense, as the title of his paper says.

## History

Kenneth O. May published the theorem in Econometrica in 1952, a year after Arrow's book. Later work extended it in several directions: to many alternatives with pairwise majority on restricted domains, to weaker forms of anonymity, and to rules that use more than the order of each voter. Its proof is the template for many axiomatic characterizations in social choice, where symmetry conditions reduce a rule to a function of a few counts and a responsiveness condition fixes that function.

## References
