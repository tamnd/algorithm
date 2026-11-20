---
tag: T25YJS
kind: problem
slug: popular-matching
name: Popular matching
aliases:
- Abraham-Irving-Kavitha-Mehlhorn popular matching
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: Find a matching that no other matching beats in a majority vote of the agents. For strict lists, a linear time algorithm finds one or shows that none exists.
prereqs: [house-allocation-problem, bipartite-matching]
see_also: [house-allocation-problem, serial-dictatorship, condorcet-winner, condorcet-paradox, stable-matching, gallai-edmonds-decomposition, hopcroft-karp, pareto-optimality]
sources:
  - paper: doi:10.1137/06067328X
    title: David J. Abraham, Robert W. Irving, Telikepalli Kavitha and Kurt Mehlhorn, Popular matchings, SIAM Journal on Computing 37(4), 1030 to 1045 (2007)
    locator: the characterization by first and second posts, the linear time algorithm for strict lists and the algorithm for lists with ties
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 7, Popular matchings
---

The popular matching problem is a version of the [house allocation problem](/house-allocation-problem/) where the goal is a matching that wins every majority vote. Agents rank the objects (here called posts), and a matching $M'$ is more popular than $M$ if more agents prefer $M'$ to $M$ than prefer $M$ to $M'$. A matching is popular if no matching is more popular than it. It is the [Condorcet winner](/condorcet-winner/) among the matchings, and like a Condorcet winner it may fail to exist. Abraham, Irving, Kavitha and Mehlhorn (2007) characterized popular matchings for one-sided preferences. Their characterization gives an $O(n + m)$ time algorithm for strict lists, where $n$ counts agents and posts and $m$ is the total length of the lists, and an $O(n^{1/2} m)$ time algorithm when the lists have ties.

## In plain words

People rank rooms. Suppose we propose an assignment and let everyone vote between it and any other assignment. Each person votes for the assignment that gives them the better room, or abstains if they get the same room in both. The proposal is popular if it never loses such a vote.

Sometimes no proposal survives every vote: three people who all rank the rooms the same way can always vote out the current plan, as in the Condorcet paradox. The surprise is that a fast test can tell whether a popular plan exists, and find one, by looking only at each person's first choice and one second choice.

## Definition

**Input.** A set $A$ of agents (applicants) and a set $P$ of posts. Each agent $a$ has a list of acceptable posts, best first. In the main case the lists are strict; in the variant with ties, a list is a sequence of tie classes. Let $n = |A| + |P|$ and let $m$ be the total length of the lists.

**Output.** A popular matching, or the answer that none exists. For matchings $M$ and $M'$, let $\phi(M, M')$ be the number of agents that prefer $M$ to $M'$; an agent prefers any acceptable post to being unmatched. $M'$ is more popular than $M$ if $\phi(M', M) > \phi(M, M')$, and $M$ is popular if no $M'$ is more popular.

**The characterization for strict lists.** Add a new last-resort post $\ell(a)$ at the end of the list of each agent $a$; then every matching can be taken to match every agent, with $\ell(a)$ meaning "unmatched". Let $f(a)$ be the first post on the list of $a$, and call a post an f-post if it is $f(a)$ for some $a$. Let $s(a)$ be the first post on the list of $a$ that is not an f-post; it exists because $\ell(a)$ is not an f-post. Abraham et al. proved: a matching $M$ that matches every agent is popular if and only if

1. every f-post is matched in $M$, and
2. every agent $a$ is matched to $f(a)$ or to $s(a)$.

## Variants

- **Ties.** With ties, $f(a)$ becomes the set of first-ranked posts of $a$. The characterization uses a maximum matching of the graph of first-choice edges and its [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/), and the algorithm takes $O(n^{1/2} m)$ time.
- **Largest popular matching.** Among the popular matchings, find one that matches the most agents to real posts. The same paper shows how to do this within the same time bounds.
- **Capacities and weights.** Posts with several copies, and agents with weights for the vote, have been studied in the same framework; Manlove (2013, Chapter 7) gives an overview.
- **Mixed matchings.** A lottery over matchings that no other lottery beats in expectation always exists, and it can be found by linear programming.
- **Two-sided preferences.** If posts also rank agents, every [stable matching](/stable-matching/) is popular (Gardenfors 1975), so popular matchings always exist in the bipartite two-sided case. In the roommates setting, deciding if a popular matching exists is NP-hard (shown independently by Faenza, Kavitha, Powers and Zhang and by Gupta, Misra, Saurabh and Zehavi in 2019).

## Examples

**No popular matching.** Three agents all rank $a \succ b \succ c$. Write a matching as the posts of agents 1, 2 and 3. The matching $(a, b, c)$ loses to $(c, a, b)$, since agents 2 and 3 improve and only agent 1 loses. In the same way $(c, a, b)$ loses to $(b, c, a)$ and $(b, c, a)$ loses to $(a, b, c)$. A brute force check over all 34 matchings, including those that leave agents unmatched, finds no popular one. The characterization explains why: $a$ is the only f-post, so $s(a) = b$ for every agent, and three agents cannot all be matched inside $\{a, b\}$.

**Two popular matchings of different sizes.** Agent 1 ranks $a \succ b$, agent 2 ranks $a \succ c$, and agent 3 ranks $b \succ a$. The f-posts are $a$ and $b$. Then $s(1) = \ell(1)$, $s(2) = c$ and $s(3) = \ell(3)$. Post $b$ can only be given to agent 3 (it is $f(3)$), and post $a$ goes to agent 1 or agent 2. So the popular matchings are $\{1a, 2c, 3b\}$ and $\{2a, 3b\}$, with agent 1 unmatched in the second. A brute force check confirms that these are the only two. Both are popular, so popularity alone does not ask for a large matching.

**A comparison.** In the second example, the matching $\{1b, 2a\}$ is Pareto optimal (it is serial dictatorship with the order 2, 1, 3), but it is not popular: $\{1a, 2c, 3b\}$ is preferred by agents 1 and 3 and only agent 2 loses.

## Known algorithms

For strict lists (Abraham, Irving, Kavitha and Mehlhorn 2007):

1. Add the last-resort posts and compute $f(a)$ and $s(a)$ for every agent. This is one pass over the lists.
2. Build the reduced graph $G'$ with the edges $\{a, f(a)\}$ and $\{a, s(a)\}$. Each agent has degree at most 2 in it.
3. Find a matching of $G'$ that matches every agent. Because agents have degree at most 2, repeatedly matching a post of degree 1 to its only agent, and then handling the remaining cycles, does this in linear time. If no such matching exists, no popular matching exists.
4. For each f-post $p$ that is still unmatched, pick an agent $a$ with $f(a) = p$; it is matched to $s(a)$, so move it to $p$. The result satisfies both conditions and is popular.

The total time is $O(n + m)$. For lists with ties, the same plan uses a maximum matching of the first-choice graph, computed by [Hopcroft-Karp](/hopcroft-karp/), which gives $O(n^{1/2} m)$.

## Bounds

- Strict lists: $O(n + m)$ time to find a popular matching or report that none exists. Every algorithm must read the lists, so this is optimal.
- Ties: $O(n^{1/2} m)$, the time of a maximum [bipartite matching](/bipartite-matching/) by Hopcroft-Karp. No faster method that avoids a maximum matching is known.
- Existence is not guaranteed, and the example with three equal lists shows that it can fail already for three agents.
- In the roommates setting the existence problem is NP-hard, so the polynomial bounds depend on the one-sided (or bipartite two-sided) structure.

## Reductions

- To [bipartite matching](/bipartite-matching/): by the characterization, a popular matching is a matching of the reduced graph $G'$ that matches every agent and every f-post. With strict lists, $G'$ has agent degree at most 2, which is why linear time suffices.
- Relation to voting: a popular matching is a weak [Condorcet winner](/condorcet-winner/) in the election whose candidates are the matchings and whose voters are the agents. The example without a popular matching is a [Condorcet paradox](/condorcet-paradox/).
- Relation to [Pareto optimality](/pareto-optimality/): every popular matching is Pareto optimal, since a Pareto improvement would win the vote, but the converse fails, as the comparison example shows.

## Applications

Allocation of housing, courses or jobs where the outcome must be defensible against a vote of the participants. Popular matchings also serve as a middle ground between stability and size in two-sided markets, where a popular matching can be larger than every stable matching.

## References
