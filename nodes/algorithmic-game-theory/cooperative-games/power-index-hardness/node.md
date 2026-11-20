---
tag: 328G7A
kind: theorem
slug: power-index-hardness
name: Hardness of computing power indices
aliases:
- Prasad-Kelly theorem
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: "Computing the Shapley-Shubik or Banzhaf index of a player in a weighted voting game is #P-complete, and deciding if it is positive is NP-complete."
prereqs: [weighted-voting-game, shapley-shubik-index, banzhaf-index, subset-sum-problem, np-complete, counting-problem]
see_also: [power-index-dynamic-programming, parsimonious-reduction, turing-reduction, co-np-complete, exact-cover-by-3-sets, weak-np-hardness, fpras, shapley-value-sampling]
sources:
  - paper: doi:10.1007/BF01753703
    title: "Kislaya Prasad and Jerry S. Kelly, NP-completeness of some problems concerning voting games, International Journal of Game Theory 19(1) (1990), 1-9"
    locator: the #P-completeness of the Banzhaf swing count and the NP-completeness of deciding whether a player has positive power in a weighted voting game
  - paper: doi:10.1287/moor.19.2.257
    title: "Xiaotie Deng and Christos H. Papadimitriou, On the complexity of cooperative solution concepts, Mathematics of Operations Research 19(2) (1994), 257-266"
    locator: the #P-completeness of the Shapley value of a weighted voting game
  - paper: arXiv:0801.4585
    title: "Piotr Faliszewski and Lane A. Hemaspaandra, The complexity of power-index comparison, Theoretical Computer Science 410(1) (2009), 101-107"
    locator: the exact form of the completeness of the raw Banzhaf and Shapley-Shubik indices under parsimonious and metric reductions
  - paper: doi:10.15807/jorsj.43.71
    title: "Tomomi Matsui and Yasuko Matsui, A survey of algorithms for calculating power indices of weighted majority games, Journal of the Operations Research Society of Japan 43(1) (2000), 71-86"
    locator: the hardness results for both indices and the pseudo-polynomial algorithms
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 4, Weighted voting games (the hardness of the power indices and of the dummy test)
---

The [Shapley-Shubik](/shapley-shubik-index/) and [Banzhaf](/banzhaf-index/) indices of a [weighted voting game](/weighted-voting-game/) are easy to define, and a [dynamic program](/power-index-dynamic-programming/) computes them in time polynomial in $n$ and the quota. This theorem says that the dependence on the size of the weights cannot be removed: with weights written in binary, computing either index exactly is #P-complete, and even the yes or no question "does this player have any power?" is NP-complete. The reason is that a swing of a player is a set of the other players whose total weight lies in a narrow window, and finding or counting such sets is the [subset sum problem](/subset-sum-problem/).

## Statement

Let a weighted voting game $[q; w_1, \ldots, w_n]$ have nonnegative integer weights and quota written in binary. For a player $i$, let $\eta_i$ be the number of its *swings*, the sets $S \subseteq N \setminus \{i\}$ with $w(S) < q \le w(S) + w_i$, where $w(S) = \sum_{j \in S} w_j$. Recall that #P is the class of functions that count the accepting paths of a nondeterministic polynomial-time machine, that is, the number of certificates of an NP problem.

**Theorem.**

1. *(Prasad and Kelly 1990.)* Computing $\eta_i$, and so the raw Banzhaf index $\eta_i / 2^{n-1}$, is #P-complete.
2. *(Deng and Papadimitriou 1994.)* Computing the Shapley-Shubik index $\varphi_i$ is #P-complete.
3. *(Prasad and Kelly 1990.)* Deciding whether $\eta_i > 0$ is NP-complete. Since $\varphi_i > 0$, $\beta'_i > 0$ and $\eta_i > 0$ are the same condition, this holds for both indices.
4. Deciding whether player $i$ is a dummy ($\eta_i = 0$, which is index 0 for both indices) is [coNP-complete](/co-np-complete/).

For the Shapley-Shubik index, "#P-complete" is meant under polynomial-time [Turing reductions](/turing-reduction/), since $\varphi_i$ is a fraction and not a count.

## In plain words

A player has power when some group of the other players is just short of the quota, and the player's vote lifts the group over it. To check this, we must find a group of players whose votes add up to an amount in a narrow range. That is the classic hard problem of finding numbers that add up to a target. So no fast method can tell whether a player has any power at all, unless a large class of hard problems is easy. Counting the groups, which is what the indices need, is harder still. The hardness needs large weights: when the weights are small numbers, a simple table counts the groups quickly.

## Proof

**Membership.** For part 3, a swing $S$ is a certificate of polynomial size, and the test $w(S) < q \le w(S) + w_i$ takes polynomial time. So the problem is in NP, and part 4, its complement, is in coNP. For part 1, $\eta_i$ is the number of certificates of this NP problem, so it is in #P. For part 2, $n!\,\varphi_i$ is the number of orders of the players in which $i$ is the pivot. An order is a certificate of polynomial size that is checked in polynomial time, so this number is a #P function, and $\varphi_i$ follows from it by one division.

**Hardness of the decision problem.** Reduce from subset sum: given positive integers $a_1, \ldots, a_m$ and a target $t$, is there a set $T \subseteq \{1, \ldots, m\}$ with $a(T) = \sum_{j \in T} a_j = t$? Let $A = a_1 + \cdots + a_m$. Build the game with the players $1, \ldots, m$ of weights $a_1, \ldots, a_m$, one more player $x$ of weight 1, and the quota $q = t + 1$. A set $S$ of the other players is a swing of $x$ exactly when $w(S) < t + 1 \le w(S) + 1$, that is, when $w(S) = t$. So the swings of $x$ are exactly the solutions of the subset sum instance, $\eta_x$ equals the number of solutions, and $x$ has positive power if and only if a solution exists. (If $t > A$ the answer is no, and we output a fixed game with a dummy, so that $q \le w(N)$ holds.) The reduction takes polynomial time, and subset sum is NP-complete, so part 3 follows. Part 4 follows by taking complements.

**Hardness of the Banzhaf count.** The reduction above is *parsimonious* ([parsimonious reduction](/parsimonious-reduction/)): it keeps the number of solutions, since $\eta_x$ equals the number of solutions of the subset sum instance. The counting version #SUBSET-SUM is #P-complete, because the standard reduction from [exact cover by 3-sets](/exact-cover-by-3-sets/) to subset sum writes each set as a number in a large base, so that each exact cover gives exactly one subset with the target sum, and #X3C is #P-complete. So $\eta_x$, and $\beta'_x = \eta_x / 2^{n-1}$, are #P-hard, which proves part 1.

**Hardness of the Shapley-Shubik index.** The index weighs the swings by their sizes, so we force all solutions to have the same size and read off their number. Counting the solutions of subset sum with exactly $k$ elements, where $k$ is part of the input, is #P-hard by a Turing reduction from #SUBSET-SUM: let $M = A + 1$, and for each $k = 0, \ldots, m$ ask for the number of subsets of size $k$ with sum $t$ in the instance with the numbers $a_j + M$ and the target $t + kM$. A subset of size $k'$ has the sum $a(T) + k'M$, and since $a(T) < M$, the sum is $t + kM$ only if $k' = k$ and $a(T) = t$. The sum over $k$ of these counts is the total number of solutions.

Now take the instance with the numbers $a'_j = a_j + M$ and the target $t' = t + kM$, and build the game of the decision reduction: the players $1, \ldots, m$ with weights $a'_j$, the player $x$ with weight 1, and $q = t' + 1$. The swings of $x$ are the sets with $w(S) = t'$, and by the choice of $M$ all of them have size exactly $k$. So

$$\varphi_x = \frac{k!\,(m - k)!}{(m+1)!} \cdot \eta_x,$$

and $\eta_x$, the number of solutions of size $k$, follows from $\varphi_x$ by a multiplication. One query to the index for each $k$ gives all these counts, so computing $\varphi_x$ is #P-hard under Turing reductions, which proves part 2.

## Consequences

- **No polynomial exact algorithm.** Unless P = NP, no algorithm computes either index in time polynomial in the binary input length, and none even decides whether an index is 0.
- **No multiplicative approximation.** A polynomial-time algorithm that approximates $\eta_i$ or $\varphi_i$ within any factor would output 0 exactly when the index is 0, and so decide the NP-complete problem of part 3. So no [FPRAS](/fpras/) or other multiplicative approximation exists unless P = NP (or NP = RP for randomized algorithms).
- **Additive approximation is easy.** [Sampling](/shapley-value-sampling/) estimates each index within an additive error $\varepsilon$ with high probability from $O(\log(n/\delta)/\varepsilon^2)$ random orders or coalitions. This does not contradict the theorem, because an additive error cannot tell a tiny positive index from 0.
- **The dummy test.** Deciding whether a member of a council has any power at all is coNP-complete in general, although the veto test $w(N) - w_i < q$ takes linear time.

## Tightness

- **The weights must be large.** The [dynamic program](/power-index-dynamic-programming/) takes $O(n^2 q)$ arithmetic operations per player, which is polynomial when the weights are bounded by a polynomial in $n$ or written in unary. So the problem is NP-hard only in the weak sense ([weak NP-hardness](/weak-np-hardness/)), and the reduction must use exponentially large weights, as it does through the large-base numbers of the reduction from exact cover by 3-sets.
- **Few distinct weights.** When the players have only a constant number of distinct weights, the coalitions are described by how many players of each weight they hold, and the indices take polynomial time.
- **The exact counting class.** Faliszewski and Hemaspaandra (2009) show that the raw Banzhaf index is #P-parsimonious-complete and that the raw Shapley-Shubik index is complete for #P under metric reductions, a reduction with one query and polynomial-time pre- and post-processing.

## History

Prasad and Kelly (1990) proved that deciding whether a player of a weighted voting game is a swing for some coalition is NP-complete and that counting the swings, the Banzhaf index, is #P-complete. Deng and Papadimitriou (1994), in a paper on the complexity of solution concepts for cooperative games, proved the #P-completeness of the Shapley value of weighted voting games and noted that it has a pseudo-polynomial algorithm. Matsui and Matsui (2000) gave a survey of the hardness results and the algorithms for both indices. Faliszewski and Hemaspaandra (2009) fixed the exact type of completeness and showed that comparing the power of two players is PP-complete.

## References
