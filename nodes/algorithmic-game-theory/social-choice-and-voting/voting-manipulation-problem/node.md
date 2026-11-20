---
tag: HAM4CR
kind: problem
slug: voting-manipulation-problem
name: Manipulation of a voting rule
aliases:
- constructive manipulation
- coalitional manipulation
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Given the other ballots, decide whether a voter or coalition can cast ballots that make a chosen candidate win. It is NP-hard for some rules."
prereqs: [gibbard-satterthwaite-theorem, preference-profile, np-complete]
see_also: [election-control-problem, plurality-voting, borda-count, single-transferable-vote, copeland-method, ranked-pairs, schulze-method, partition-problem]
sources:
  - paper: doi:10.1007/BF00295861
    title: "John J. Bartholdi III, Craig A. Tovey and Michael A. Trick, The computational difficulty of manipulating an election, Social Choice and Welfare 6(3) (1989), 227-241"
    locator: "the manipulation problem for one voter, the greedy algorithm that builds the ballot from the top, and the NP-completeness of manipulation of second-order Copeland"
  - paper: doi:10.1007/BF00183045
    title: "John J. Bartholdi III and James B. Orlin, Single transferable vote resists strategic voting, Social Choice and Welfare 8(4) (1991), 341-354"
    locator: "the NP-completeness of manipulation of the single transferable vote by one voter"
  - paper: "Lirong Xia, Michael Zuckerman, Ariel D. Procaccia, Vincent Conitzer and Jeffrey S. Rosenschein, Complexity of unweighted coalitional manipulation under some common voting rules, Proceedings of the 21st International Joint Conference on Artificial Intelligence (IJCAI 2009), 348-353"
    locator: "the NP-completeness of manipulation of ranked pairs, already for one manipulator"
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 6 (Vincent Conitzer and Toby Walsh, Barriers to manipulation): Theorem 6.4 (the greedy algorithm is correct for plurality, Borda, Copeland and maximin), Theorem 6.5 (weighted coalitional manipulation of veto with 3 candidates is NP-complete), Borda with two manipulators, and the polynomial algorithms for Schulze's method; Chapter 7 (Piotr Faliszewski and Jörg Rothe), Theorem 7.11 (manipulation reduces to priced bribery)"
---

The manipulation problem asks whether some voters can change the result of an election by lying about their preferences. The ballots of the other voters are known. The manipulators want a chosen candidate $p$ to win, and the question is whether some ballots for them achieve this. The [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) says that every reasonable rule with at least three candidates can be manipulated in some election, so manipulations exist. Bartholdi, Tovey and Trick asked in 1989 whether they are hard to find. For [plurality](/plurality-voting/) and the [Borda count](/borda-count/), one voter finds a manipulation with a simple greedy algorithm. For the [single transferable vote](/single-transferable-vote/) and [ranked pairs](/ranked-pairs/), the problem is [NP-complete](/np-complete/) already for one manipulator. Hardness of this kind is a possible barrier to strategic voting, but it holds only in the worst case.

## In plain words

An election has a fixed set of ballots, and one more voter still has to vote. This voter wants a certain candidate to win and does not care about being honest. Which ballot should the voter cast? For some voting rules the answer is easy: put the favorite first and the strongest rivals last. For other rules no fast method is known, and the voter may have to try a very large number of ballots. The same question can be asked for a group of voters who act together, and then it is often harder.

## Definition

A voting rule $R$ maps a profile of rankings over a set $C$ of $m$ candidates to a nonempty set of winners. The input of the constructive coalitional manipulation problem is:

- the rule $R$, which is fixed and is not part of the input,
- the candidates $C$ and a candidate $p \in C$,
- the ballots $P_{\mathrm{NM}}$ of the voters who do not manipulate,
- the number $k$ of manipulators, and in the weighted form, their weights $w_1, \ldots, w_k$.

The question is whether there are rankings $v_1, \ldots, v_k$ such that $p$ wins under $R$ on the profile $P_{\mathrm{NM}} + (v_1, \ldots, v_k)$. A weighted voter counts as $w_i$ voters with the same ballot. In the co-winner model, $p$ must be one of the winners. In the unique winner model, $p$ must be the only winner. The two models can have different complexity, so a result must state its model. The single manipulator case is $k = 1$.

## Variants

- **One manipulator.** The problem of Bartholdi, Tovey and Trick. The manipulator can test each ballot, so the problem is in NP for every rule whose winners can be computed in polynomial time.
- **Unweighted coalitional manipulation.** Several manipulators with weight 1 each. The difficulty grows with $k$, and some rules that are easy for one manipulator are hard for two.
- **Weighted coalitional manipulation.** Manipulators with integer weights, usually with a fixed number of candidates. Weights bring number problems such as [partition](/partition-problem/) into the question.
- **Destructive manipulation.** The manipulators want a candidate $d$ not to win. This can be easier than the constructive form, because any candidate other than $d$ may win.
- **Partial information.** The manipulators know only part of the other ballots, or a probability distribution over them. The possible winner problem, where the known ballots are partial orders, includes coalitional manipulation as the special case in which the manipulators' ballots are empty.

## Examples

- **Plurality.** The manipulators rank $p$ first. This adds the most possible points to $p$ and adds none to the rivals, so if this fails, every other choice fails. This holds for weighted coalitions too.
- **Borda with one manipulator.** Take four candidates and the Borda scores $3, 2, 1, 0$. Two voters have cast $a \succ p \succ b \succ c$ and $b \succ c \succ p \succ a$, which give the scores $a = 3$, $p = 3$, $b = 4$ and $c = 2$. The manipulator wants $p$ to be the unique winner. An honest ballot $p \succ b \succ a \succ c$ gives $p = 6$ and $b = 6$, a tie. The greedy method puts $p$ first, for $p = 6$. Then it fills the next places from the top, each time with a candidate that stays below 6. Candidate $b$ cannot take second place, since $4 + 2 = 6$, but $a$ can, with $3 + 2 = 5$. Then $b$ takes third place with $5$, and $c$ the last with $2$. The ballot $p \succ a \succ b \succ c$ makes $p$ the unique winner. The manipulation buries the strongest rival $b$.
- **Weighted veto.** Under veto, a candidate gets a point from every ballot that does not rank it last. With three candidates $p, a, b$, one honest voter of weight $K$ ranks $p$ last. The manipulators have weights that sum to $2K$, and none of them ranks $p$ last. In the co-winner model, $p$ wins exactly when the weight that vetoes $a$ and the weight that vetoes $b$ are each at least $K$, so exactly $K$ each. That is the [partition problem](/partition-problem/) on the weights.

## Known algorithms

- **Greedy construction.** For one manipulator, put $p$ first, and fill the places from the top. At each place, choose any candidate that does not beat $p$ when placed there. If no candidate fits, report that no manipulation exists. Bartholdi, Tovey and Trick gave this method, and the Handbook of Computational Social Choice proves it for plurality, Borda, [Copeland](/copeland-method/) and maximin (Theorem 6.4). It needs $m$ places with $m$ tests each, so it runs in polynomial time.
- **Search over ballots.** For one manipulator and any rule, try the $m!$ rankings. With a constant number of candidates, an unweighted coalition can be handled for any anonymous rule: only the number of manipulators who cast each of the $m!$ rankings matters, so there are $\binom{k + m! - 1}{m! - 1}$ cases to test, a polynomial in $k$.
- **Schulze's method.** The [Schulze method](/schulze-method/) can be manipulated in polynomial time by one voter, and also by coalitions.
- **Exact solvers.** For hard rules, integer programs and SAT solvers search the ballots of the manipulators, and they are often fast on small elections.

## Bounds

- **NP-complete for one manipulator.** Second-order Copeland (Bartholdi, Tovey and Trick 1989), the single transferable vote (Bartholdi and Orlin 1991) and ranked pairs (Xia, Zuckerman, Procaccia, Conitzer and Rosenschein 2009).
- **NP-complete for two manipulators.** The Borda count, which is easy for one manipulator.
- **NP-complete for weighted coalitions with three candidates.** Veto is one example (Theorem 6.5 of the Handbook). Plurality stays easy, by the example above.
- **Worst case only.** These lower bounds say that no polynomial algorithm solves every instance unless P = NP. They do not say that typical elections are hard.
- **Domain restrictions.** When all ballots are [single-peaked](/single-peaked-preferences/), some of the hard cases become polynomial.

## Reductions

- **From partition.** The weighted veto example is a [polynomial-time reduction](/polynomial-time-reduction/) from partition, which shows NP-hardness for a constant number of candidates.
- **To bribery.** Manipulation is a special case of priced bribery, in which the briber pays to change ballots: give each manipulator a price of 0 and every other voter a price above the budget (Handbook, Theorem 7.11). So hardness of manipulation implies hardness of this form of bribery, and bribery algorithms solve manipulation. See [election control and bribery](/election-control-problem/).
- **To possible winners.** Coalitional manipulation is the possible winner problem with complete ballots for the honest voters and empty ballots for the manipulators.

## Applications

- **Design of voting rules.** Hardness of manipulation is one reason to prefer a rule. It is used in the study of rules for groups of software agents, which can compute manipulations fast.
- **Margin of victory.** A related quantity is the least number of voters who must change their ballots to change the winner. It measures the robustness of an election result.
- **Elections with partial ballots.** The algorithms decide which candidates can still win when some votes are missing.

## References
