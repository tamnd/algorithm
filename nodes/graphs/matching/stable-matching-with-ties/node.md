---
tag: JN2GRA
kind: problem
slug: stable-matching-with-ties
name: Stable matching with ties
aliases:
- weakly stable matching
- stable matching with incomplete lists
area: graphs/matching
level: advanced
summary: Stable matching where preference lists may contain ties or be incomplete.
model: word-ram
complexity:
  vars: {n: the number of agents on both sides, m: the total length of the preference lists}
  time: {worst: O(n + m)}
prereqs: [stable-matching, gale-shapley]
see_also: [stable-roommates-problem, hospitals-residents-problem, stable-matching-rotations, maximum-matching, np-hard, apx, approximation-ratio, maximal-matching]
sources:
  - paper: doi:10.1016/0166-218X(92)00179-P
    title: Robert W. Irving, Stable marriage and indifference, Discrete Applied Mathematics 48(3), 261 to 272 (1994)
    locator: the whole paper (weak, strong and super-stability, and the algorithms for strong and super-stability)
  - paper: doi:10.1016/S0304-3975(01)00206-7
    title: David F. Manlove, Robert W. Irving, Kazuo Iwama, Shuichi Miyazaki and Yasufumi Morita, Hard variants of stable marriage, Theoretical Computer Science 276(1-2), 261 to 279 (2002)
    locator: the whole paper (the NP-hardness of maximum weakly stable matching with ties and incomplete lists)
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 3, The Stable Marriage Problem with Indifference
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: Section 1.4, Incomplete preference lists, and Section 1.5, Indifference
  - paper: "Telikepalli Kavitha, Kurt Mehlhorn, Dimitrios Michail and Katarzyna E. Paluch, Strongly stable matchings in time O(nm) and extension to the hospitals-residents problem, ACM Transactions on Algorithms 3(2), article 15 (2007)"
    locator: the whole paper
---

Stable matching with ties is the form of [stable matching](/stable-matching/) in which an agent may be indifferent between some agents of the other side, and lists may be incomplete. With ties there are three natural notions of a blocking pair, and so three kinds of stable matching: weakly, strongly and super-stable. A weakly stable matching always exists and is found in linear time by breaking the ties and running [Gale-Shapley](/gale-shapley/), but weakly stable matchings can differ in size, and finding a largest one is NP-hard. Strongly and super-stable matchings may not exist; when they do, polynomial algorithms find them. The underlying graph of acceptable pairs is bipartite and unweighted.

## In plain words

In the usual problem, every student ranks every school in a strict order. In real lists, a student may say "these two schools are equally good to me", and may leave some schools off the list. Then "would both rather be together" can mean different things. Must both strictly prefer the swap, or is it enough that one does and the other does not mind?

With the weakest meaning, a stable plan always exists: settle each tie by a coin toss and use the usual method. But the coin tosses change how many students get a school at all, and choosing the tosses that give the most placements is very hard. With the stronger meanings, a stable plan may not exist, but it is easy to check and to find one.

## Definition

The input is two disjoint sets $P$ and $R$, with $n = |P| + |R|$, and for each agent a *list with ties*: a sequence of disjoint nonempty groups of agents of the other side, called ties, from best to worst. Agents in the same tie are equally good. An agent not on the list is unacceptable. A pair $pr$ is acceptable if each is on the list of the other; these pairs form a [bipartite graph](/bipartite-graph/) $G$ without weights, and $m$ is the total length of the lists.

For a matching $M$ and an agent $a$, say that $a$ *strictly prefers* $b$ if $a$ is single in $M$ or $b$ is in a better tie than $M(a)$, and that $a$ *weakly prefers* $b$ if $a$ strictly prefers $b$ or $b$ is in the same tie as $M(a)$. An acceptable pair $pr \notin M$ is

- a **weakly blocking pair** in the sense of weak stability if both $p$ and $r$ strictly prefer each other;
- a **strongly blocking pair** in the sense of strong stability if one of them strictly prefers the other and the other weakly prefers;
- a **super-blocking pair** in the sense of super-stability if both weakly prefer each other.

$M$ is *weakly stable*, *strongly stable* or *super-stable* if no pair of the corresponding kind exists. Super-stable implies strongly stable, which implies weakly stable. Without ties, all three are the usual stability.

The problem names are SMT for ties with complete lists, SMI for incomplete lists without ties, and SMTI for both.

- **Input:** $P$, $R$ and the lists with ties.
- **Output, weak version:** a weakly stable matching; in the optimization form MAX SMTI, a largest weakly stable matching.
- **Output, strong or super version:** a strongly stable or super-stable matching, or "none exists".

## Variants

- **Weak stability with complete lists (SMT).** Every weakly stable matching is perfect when $|P| = |R|$, so the size question disappears. Optimizing over weakly stable matchings, for example minimizing the total rank, is still NP-hard.
- **Weak stability with incomplete lists (SMTI).** Weakly stable matchings exist, but their sizes can differ by a factor of 2. MAX SMTI is NP-hard, even when ties occur on one side only, and it is APX-hard, so it has no approximation scheme unless $\mathsf P = \mathsf{NP}$.
- **Incomplete lists without ties (SMI).** All stable matchings have the same size and match the same agents, so this case is as easy as the classical one.
- **Super-stability.** A super-stable matching may not exist. Irving gave an $O(n + m)$ algorithm, a version of Gale-Shapley in which a receiver rejects all of a tie at once, that finds one or reports that none exists.
- **Strong stability.** A strongly stable matching may not exist. Irving's algorithm decides it in $O(n^4)$ time for complete lists, and Kavitha, Mehlhorn, Michail and Paluch reduced the time to $O(nm)$ for incomplete lists.
- **Many-to-one and one set.** The same three notions apply to the [hospitals/residents problem](/hospitals-residents-problem/) and to the [stable roommates problem](/stable-roommates-problem/); for roommates with ties, even the existence of a weakly stable matching is NP-complete.

## Examples

**Weakly stable matchings of different sizes.** Let $A$ list only $x$; let $B$ list $x$ and $y$ in one tie; let $x$ list $A$ and $B$ in one tie; let $y$ list only $B$. The acceptable pairs are $Ax$, $Bx$ and $By$.

- $\{Bx\}$ is weakly stable: $Ax$ does not block, since $x$ is indifferent between $A$ and $B$; $By$ does not block, since $B$ is indifferent between $x$ and $y$. It has size 1.
- $\{Ax, By\}$ is weakly stable and has size 2. It is also strongly stable. It is not super-stable, since $B$ and $x$ each weakly prefer the other.

The second matching is a [maximum matching](/maximum-matching/) of $G$; the first is only a [maximal matching](/maximal-matching/). In general a weakly stable matching is maximal, so its size is at least half the maximum, and this example reaches the ratio $\frac12$.

**No strongly stable matching.** Let $A$ and $B$ both list $x$ then $y$, strictly; let $x$ list $A$ and $B$ in one tie; and let $y$ list $A$ then $B$. The perfect matching $\{Ax, By\}$ is weakly stable but blocked strongly by $Bx$: $B$ strictly prefers $x$ to $y$, and $x$ is indifferent between $A$ and $B$. The perfect matching $\{Ay, Bx\}$ is blocked strongly by $Ax$ in the same way. Every matching with fewer pairs has a single agent and a pair with both ends strictly preferring each other. So no strongly stable matching exists, and hence no super-stable one.

**Breaking ties.** In the first example, breaking the tie of $x$ as $B$ before $A$ and the tie of $B$ as $x$ before $y$, then running Gale-Shapley with $P$ proposing, gives $\{Bx\}$. Breaking the tie of $x$ as $A$ before $B$ gives $\{Ax, By\}$. Every weakly stable matching arises from some tie-breaking in this way.

**The empty instance.** With no agents, or with no acceptable pair, the empty matching is super-stable, so it is stable in all three senses.

## Known algorithms

| problem | algorithm | time |
|---|---|---|
| a weakly stable matching | break ties arbitrarily, then [Gale-Shapley](/gale-shapley/) | $O(n + m)$ |
| a super-stable matching or "none" | Irving's algorithm | $O(n + m)$ |
| a strongly stable matching or "none" | Kavitha, Mehlhorn, Michail and Paluch | $O(nm)$ |
| MAX SMTI, approximately | any weakly stable matching | ratio 2 |
| MAX SMTI, approximately | the algorithms of Király and of McDermid, with a proposal order that favours single agents | ratio $\frac32$ |
| MAX SMTI, exactly | integer programming or constraint programming | exponential in the worst case |

## Bounds

- **Weak stability.** $\Theta(n + m)$ for finding some weakly stable matching on the [word RAM](/word-ram/).
- **MAX SMTI hardness.** NP-hard, and NP-hard to approximate within some constant greater than 1. Under the [unique games conjecture](/unique-games-conjecture/), no polynomial algorithm has a ratio better than $\frac43 - \varepsilon$. The best known ratio is $\frac32$, so the exact threshold of approximation is open.
- **Strong and super-stability.** Polynomial; $O(n + m)$ for super-stability, $O(nm)$ for strong stability.

## Reductions

- **Weak stability to the strict case.** Every weakly stable matching is stable for some strict refinement of the lists, and every stable matching of a refinement is weakly stable. So the weakly stable matchings are the union over the refinements, and the hardness of MAX SMTI comes from choosing the refinement.
- **From satisfiability.** The NP-hardness of MAX SMTI is shown by reduction from a restricted satisfiability or vertex cover problem, in the paper of Manlove, Irving, Iwama, Miyazaki and Morita.
- **Strong stability to bipartite matching.** The $O(nm)$ algorithm repeatedly finds a [maximum matching](/maximum-matching/) in a bipartite graph of currently acceptable pairs and uses its critical set to decide which proposals to delete.

## Applications

- **Residency matching.** Hospitals often rank many applicants equally. The Scottish Foundation Allocation Scheme for junior doctors used weakly stable matchings with ties and sought a large one, which motivated the study of MAX SMTI.
- **School choice.** Schools rank pupils by coarse priority classes, such as distance or siblings, which creates large ties. The way the ties are broken changes the outcome, and several cities use a single random tie-breaking order.
- **Kidney exchange and other markets.** Agents that cannot tell some options apart create ties in many matching markets.

## References
