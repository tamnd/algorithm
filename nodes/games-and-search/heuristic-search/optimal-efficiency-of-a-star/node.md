---
tag: 4GR3NX
kind: theorem
slug: optimal-efficiency-of-a-star
name: Optimal efficiency of A*
aliases:
- Dechter-Pearl optimality
area: games-and-search/heuristic-search
level: advanced
summary: With a consistent heuristic, each algorithm that sees the same information and is always optimal must expand every state that A* surely expands. So A* is optimal up to ties at f = C*.
prereqs: [a-star-optimality, consistent-heuristic]
see_also: [a-star-search, heuristic-dominance, admissible-heuristic, pathmax, bidirectional-heuristic-search, iterative-deepening-a-star, completeness-and-optimality-of-search, adversary-argument]
sources:
  - paper: doi:10.1145/3828.3830
    title: Rina Dechter and Judea Pearl, Generalized best-first search strategies and the optimality of A*, Journal of the ACM 32(3) (1985)
    locator: pp. 505 to 536 (four types of optimality, three classes of algorithms and four domains of instances; A* is optimal over the admissible algorithms on consistent instances but not on admissible ones)
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the comparison of A* with other admissible algorithms that are no more informed, proved under the consistency assumption)
  - paper: doi:10.1145/1056777.1056779
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, Correction to "A formal basis for the heuristic determination of minimum cost paths", SIGART Newsletter 37 (1972)
    locator: pp. 28 to 29 (the claim that the optimality result of the 1968 paper holds without the consistency assumption)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (the conditions for node expansion and the optimality of A* among admissible algorithms)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5.3 (search contours and the optimal efficiency of A*)
  - paper: doi:10.1016/0004-3702(77)90002-9
    title: Alberto Martelli, On the complexity of admissible search algorithms, Artificial Intelligence 8(1) (1977)
    locator: pp. 1 to 13 (graphs on which A* with an admissible h makes exponentially many expansions, and algorithm B)
---

The optimal efficiency theorem of [A*](/a-star-search/) compares the work of A* with that of every other algorithm that is guaranteed to find a cheapest path with the same information. Let the heuristic be [consistent](/consistent-heuristic/), and let $C^*$ be the cost of a cheapest solution. A* expands every state with $g^*(n) + h(n) < C^*$ and no state with $g^*(n) + h(n) > C^*$, as [the optimality theorem](/a-star-optimality/) shows. The efficiency theorem says that every algorithm that sees only the start, the successor function, the goal test and the values of $h$, and that is optimal on every problem with a consistent heuristic, must also expand every state with $g^*(n) + h(n) < C^*$. So no such algorithm expands fewer states than A*, except for states with $g^* + h = C^*$, where the result depends on how ties are broken. Hart, Nilsson and Raphael proved a form of this in 1968 under the consistency assumption, and Dechter and Pearl (1985) showed that without consistency A* is not optimal in this sense.

## Statement

An *instance* is a state-space search problem: a start $s_0$, a successor function with nonnegative costs, a goal test, and a heuristic $h$ with values for all states. A *search algorithm* learns about an instance only by these steps: it gets $s_0$, it calls the goal test and $h$ on states that it has seen, and it *expands* a state that it has seen, which means that it calls the successor function on it and so sees the successors and the costs. It is deterministic. It is *admissible on a class* of instances if on each instance of the class it returns a solution of least cost, or reports correctly that there is none.

Let $\mathcal{I}_{\mathrm{con}}$ be the class of instances whose heuristic is consistent.

**Theorem.** Let $B$ be a search algorithm that is admissible on $\mathcal{I}_{\mathrm{con}}$. Let $I \in \mathcal{I}_{\mathrm{con}}$ have a solution, of least cost $C^*$. Then $B$ expands, on $I$, every state $n$ that is reachable from $s_0$ and has $g^*(n) + h(n) < C^*$.

**Corollary.** On $I$, every state that A* expands is expanded by $B$, except perhaps for states with $g^*(n) + h(n) = C^*$. So the number of states that A* expands is at most the number that $B$ expands plus the number of states with $g^*(n) + h(n) = C^*$.

## In plain words

Suppose a state looks promising: the cost to reach it plus the estimate from it is less than the best answer. Suppose an algorithm never looks at the moves out of that state. Then the algorithm cannot know what lies behind the state. There could be a goal right behind it, at exactly the distance that the estimate says, and that goal would be cheaper than the answer the algorithm gives.

So an algorithm that must always be right has to look at every promising state. A* looks at those states and at almost nothing else. With a consistent estimate this means that no algorithm that must always be right does less work than A*, except for states that tie with the best answer.

## Proof

Let $n$ be reachable, with $g^*(n) + h(n) < C^*$, and suppose that $B$ does not expand $n$ on $I$. Since $h(n) < C^* - g^*(n)$, $h(n)$ is finite, and $n$ is not a goal, because a goal would give a solution of cost $g^*(n) \le g^*(n) + h(n) < C^*$.

Build the instance $I'$ from $I$ by adding one new state $t'$, which is a goal with $h(t') = 0$ and no successors, and one new action from $n$ to $t'$ of cost $h(n)$. Nothing else changes.

*$I'$ is in $\mathcal{I}_{\mathrm{con}}$.* The old actions keep their inequalities $h(u) \le c(u, v) + h(v)$. The new action has $h(n) \le h(n) + h(t') = h(n)$. The new goal has $h(t') = 0$. So $h$ is consistent on $I'$.

*$B$ cannot tell $I$ and $I'$ apart.* The two instances differ only in the successors of $n$ and in the state $t'$. The algorithm sees the successors of $n$ only by expanding $n$, and it can see $t'$ only as a successor of $n$. As long as $B$ does not expand $n$, each answer that it gets on $I'$ is the answer that it gets on $I$, so by induction on the steps it makes the same steps on both, and it does not expand $n$ on $I'$ either. So it returns on $I'$ the solution $P$ that it returns on $I$. All actions of $I$ are actions of $I'$, so $P$ is a solution of $I'$, of cost $C^*$.

*$P$ is not optimal on $I'$.* A cheapest path from $s_0$ to $n$, followed by the new action, reaches $t'$ at cost $g^*(n) + h(n) < C^*$. So $B$ returns a solution that is not optimal on an instance of $\mathcal{I}_{\mathrm{con}}$, which contradicts its admissibility. $\square$

*Proof of the corollary.* With a consistent $h$, A* expands no state with $g^*(n) + h(n) > C^*$, by part 5 of the [optimality theorem](/a-star-optimality/). Every state that it expands with $g^* + h < C^*$ is expanded by $B$, by the theorem. The only states that A* can expand and $B$ can skip are those with $g^* + h = C^*$. $\square$

## Consequences

- **To do better, change the information.** No algorithm of the class does much better than A* with the same $h$. The ways to expand fewer states are a larger heuristic, which is the subject of [heuristic dominance](/heuristic-dominance/), or more information, such as a predecessor function for [bidirectional heuristic search](/bidirectional-heuristic-search/), which is outside the class of the theorem.
- **Uniform-cost search.** With $h = 0$, every admissible algorithm that has no heuristic must expand every state with $g^* < C^*$. So [Dijkstra's algorithm](/dijkstra/), stopped at the goal, does the least possible work for a blind search, up to ties.
- **Memory-bounded searches.** [IDA*](/iterative-deepening-a-star/) with a consistent $h$ is admissible, so it expands every state with $g^* + h < C^*$ at least once. It saves memory, not expansions, and it usually expands states many times.
- **The set, not the time.** The theorem counts distinct states that are expanded. It says nothing about the cost of the open list, and nothing about states that are expanded more than once, which can happen only with an inconsistent $h$.

## Tightness

- **Consistency.** The proof needs $I'$ to be in the class. With an admissible $h$ that is not consistent, the new goal can make $h$ overestimate elsewhere. In the instance with the arcs S to A of cost 1, S to B of cost 3, and A to B, B to C and C to G of cost 1 each, with $h(A) = 3$ and $h = 0$ elsewhere, the state B has $g^*(B) + h(B) = 2 < 4 = C^*$. Adding an action from B to a new goal of cost $h(B) = 0$ makes the true cost from A equal to 1, below $h(A) = 3$, so the new instance is not admissible and the argument gives nothing. Dechter and Pearl showed that on the class of instances with admissible heuristics, A* is not optimal among the admissible algorithms, and that no algorithm is optimal there. They also showed that A* is optimal over the best-first algorithms whose evaluation functions can depend on the whole path, on admissible instances. Separately, Martelli (1977) showed that A* with an admissible $h$ can make a number of expansions exponential in the number of states, by expanding states again and again, while his algorithm B needs at most quadratically many.
- **Ties at $f = C^*$.** On the graph of the page [A* search](/a-star-search/), with $C^* = 7$, A* with ties broken toward larger $g$ expands S, A, D, B and C. A* with ties broken first toward goals and then by the name of the state expands only S, A, B and C, and it is also admissible. The state D, with $g^*(D) + h(D) = 5 + 2 = 7 = C^*$, is the difference. So the corollary needs its exception for the states at $f = C^*$.
- **The same information.** An algorithm with a larger consistent $h_2 \ge h$ is in a different comparison, and it can expand fewer states. In the same example, A* with $h = h^*$ expands only S, B and C.

## History

Hart, Nilsson and Raphael (1968) compared A* with every admissible algorithm that is no more informed than it, and proved that A* expands no more states, under an assumption that is consistency in today's terms. In a correction in the SIGART Newsletter of 1972 they claimed that the assumption was not needed. Martelli (1977) showed that A* can make exponentially many expansions with an admissible but inconsistent heuristic, which counts repeated expansions of the same state. Dechter and Pearl (1985) defined four types of optimality, three classes of algorithms and four domains of instances, and found the strongest type that holds for each pair. Their results showed that the claim of 1972 was false: the result needs consistency.

## References
