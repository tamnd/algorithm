---
tag: AZCEZ2
kind: theorem
slug: knuth-moore-theorem
name: Knuth-Moore theorem
aliases:
- minimal game tree theorem
area: games-and-search/game-tree-search
level: advanced
summary: On a uniform tree of degree b and depth d, every algorithm that finds the minimax value reads at least b^ceil(d/2) + b^floor(d/2) - 1 leaves; alpha-beta with best-first order reads exactly that many.
prereqs: [alpha-beta-pruning]
see_also: [principal-variation, move-ordering, principal-variation-search, young-brothers-wait, sss-star, branching-factor, decision-tree-complexity, game-tree-evaluation]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326; Section 2 (the conditions on F1 and F2), Section 6 (Theorem 1 on critical positions, Corollary 1, Theorem 2 and Corollary 3, the lower bound for uniform trees) and Section 7 (values with no cutoff)
  - paper: "Timothy P. Hart and Daniel J. Edwards, The tree prune (TP) algorithm, MIT Artificial Intelligence Project Memo 30 (1961), revised as The alpha-beta heuristic (1963)"
    title: Hart and Edwards 1961
    locator: the whole memo (Levin's count of the leaves in the best case, given without proof)
  - paper: "T. Anthony Marsland and Fred Popowich, Parallel game-tree search, IEEE Transactions on Pattern Analysis and Machine Intelligence 7(4) (1985), pp. 442-452"
    title: Marsland and Popowich 1985
    locator: the names PV, CUT and ALL for the node types 1, 2 and 3 of the minimal tree
  - paper: doi:10.1145/358589.358616
    title: Judea Pearl, The solution for the branching factor of the alpha-beta pruning algorithm and its optimality, Communications of the ACM 25(8) (1982)
    locator: pp. 559 to 564 (the expected case on random uniform trees, between the best case of this theorem and the worst case)
---

The Knuth-Moore theorem gives the best case of [alpha-beta pruning](/alpha-beta-pruning/) and shows that it is the best case of every algorithm. On a uniform game tree of branching factor $b$ and depth $d$, any method that finds the [minimax](/minimax/) value for all leaf values must evaluate at least $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves. Alpha-beta evaluates exactly that many when the first move at every node is a best move. The leaves that it then evaluates are the *critical* leaves, and the nodes on the way to them form the *minimal tree*. Knuth and Moore (1975) proved it together with the correctness of alpha-beta in its fail-hard form. This page states all three parts with their hypotheses, adds the fail-soft form and the worst case, and proves them.

## Statement

**Setting.** A game tree is *uniform of degree $b$ and height $d$*, with $b \ge 1$ and $d \ge 0$, if every node on the levels $0, 1, \ldots, d-1$ has exactly $b$ children and every node on level $d$ is terminal. Each terminal node $t$ has a value $f(t)$, a real number, for the player to move at $t$. Every real number is allowed at every leaf, independently of the other leaves. The negamax value is $N(t) = f(t)$ at a leaf and $N(p) = \max_i (-N(p_i))$ over the children $p_1, \ldots, p_b$ of an inner node $p$. A node is named by the sequence $a_1 a_2 \cdots a_l$ of the child numbers on the path from the root, with $1 \le a_i \le b$. The node $a_1 \cdots a_l$ is *critical* if $a_i = 1$ for all even $i$ or $a_i = 1$ for all odd $i$. Let
$$ L(b, d) = b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1. $$

ALPHABETA$(p, \alpha, \beta)$ is the procedure on [alpha-beta pruning](/alpha-beta-pruning/): at a leaf it returns $f(p)$, and at an inner node it sets $m$ to $\alpha$ (the *fail-hard* form, the procedure F2 of Knuth and Moore) or to $-\infty$ (the *fail-soft* form), and for $i = 1, \ldots, b$ it sets $t \leftarrow -$ALPHABETA$(p_i, -\beta, -\max(m, \alpha))$, $m \leftarrow \max(m, t)$, and returns $m$ as soon as $m \ge \beta$.

**Theorem (Knuth and Moore 1975).**

1. **(Bounds on the result.)** On every finite game tree, for every node $p$ and every window $\alpha < \beta$, with $r = $ ALPHABETA$(p, \alpha, \beta)$ in either form:
   - if $N(p) \le \alpha$ then $r \le \alpha$; if $\alpha < N(p) < \beta$ then $r = N(p)$; if $N(p) \ge \beta$ then $r \ge \beta$.
   - In the fail-soft form, also: $r \le \alpha$ implies $N(p) \le r$, and $r \ge \beta$ implies $N(p) \ge r$.

   In particular ALPHABETA$(p, -\infty, +\infty) = N(p)$.
2. **(Lower bound.)** Let a set $S$ of leaves of a uniform tree *determine* the value if every change of the values of the leaves outside $S$ leaves the root value the same. Then every such set has at least $L(b, d)$ leaves, and for every choice of leaf values some such set has exactly $L(b, d)$ leaves. So every algorithm that always computes the right root value, deterministic, randomized or nondeterministic, evaluates at least $L(b, d)$ leaves in every run on every input.
3. **(Perfect ordering.)** If, in addition, the first child of every inner node is a best move, that is $N(p) = -N(p_1)$ (ties allowed), then ALPHABETA$(\text{root}, -\infty, +\infty)$ in either form evaluates exactly the critical leaves. There are $L(b, d)$ of them, and the search examines exactly the critical nodes, $L(b, l)$ of them on each level $l$.
4. **(Worst case.)** For all $b$ and $d$ there are distinct leaf values for which both forms evaluate all $b^d$ leaves.

## In plain words

Even if you knew the right answer, you would still have to prove it to someone who checks each leaf. To prove that the root is worth a value, you must show two things. First, a plan for the player to move that gets at least that value against every reply. Second, a plan for the opponent that holds the player to at most that value against every move. The first plan has to look at every reply of the opponent and one move of the player, and the second the other way round. The two plans meet in one line of play. So any proof uses at least the leaves of the two plans, and that is the count in the theorem.

Alpha-beta finds exactly such a proof when it always tries the best move first. With a bad order it looks at almost everything.

## Proof

**Part 1.** By induction on the height of $p$. At a leaf $r = N(p)$. Let $p$ be an inner node, let $w_i = -N(p_i)$ so that $N(p) = \max_i w_i$, and let $m_0$ be the start value of $m$ and $m_i$ its value after child $i$. The call on $p_i$ has the window $(-\beta, -a_i)$ with $a_i = \max(m_{i-1}, \alpha) < \beta$, since the loop did not stop before child $i$. By the induction hypothesis for $p_i$, after negation: $t_i = w_i$ if $a_i < w_i < \beta$; $t_i \le a_i$ if and only if $w_i \le a_i$; $t_i \ge \beta$ if and only if $w_i \ge \beta$. In the fail-soft form also $w_i \le t_i$ when $t_i \le a_i$, and $w_i \ge t_i$ when $t_i \ge \beta$.

While $m_i < \beta$, we have $\max(m_i, \alpha) = \max(\alpha, w_1, \ldots, w_i)$. This holds for $i = 0$. For the step, $t_i \le m_i < \beta$, so either $t_i = w_i$, or $t_i \le a_i$ and $w_i \le a_i$; in both cases $\max(a_i, t_i) = \max(a_i, w_i)$, which is the claim.

If the loop stops at child $j$, then $r = t_j \ge \beta$, so $w_j \ge \beta$ and $N(p) \ge \beta$, and in the fail-soft form $N(p) \ge w_j \ge t_j = r$. If it does not stop, then $r = m_b < \beta$ and $\max(r, \alpha) = \max(N(p), \alpha)$. This rules out $N(p) \ge \beta$, gives $r = N(p)$ when $N(p) > \alpha$, and gives $r \le \alpha$ when $N(p) \le \alpha$. In the fail-soft form with $r \le \alpha$, every $t_i \le r \le a_i$, so $w_i \le t_i \le r$ and $N(p) \le r$. The window $(-\infty, +\infty)$ makes the middle case hold for every finite value. (The [alpha-beta correctness proof](/alpha-beta-pruning/proofs/correctness/) writes out the same steps in more detail.)

**Part 2.** Write the tree in minimax form, with MAX to move at the root, MIN on the odd levels, and $V$ the value for MAX. A *MAX strategy tree* is a subtree that contains the root, one child of each of its MAX nodes and all children of each of its MIN nodes. A *MIN strategy tree* is defined the other way round.

*Claim A.* Some MAX strategy tree has all its leaves of value at least $V(\text{root})$. Choose at each MAX node a child of the same value; at a MIN node every child has a value at least that of the node. By induction from the root, every node of the subtree has value at least $V(\text{root})$. In the same way, some MIN strategy tree has all its leaves of value at most $V(\text{root})$.

*Claim B.* Let $S$ determine the value $v$. Put a number $M_-$ below $v$ and below every value in $S$ on each leaf outside $S$. The root value stays $v$, so by Claim A there is a MAX strategy tree whose leaves all have a value at least $v > M_-$ after the change. None of them is outside $S$. So $S$ contains all leaves of a MAX strategy tree. With a number $M_+$ above $v$ and above all values in $S$, it also contains all leaves of a MIN strategy tree.

*Counting.* A root to leaf path passes through $\lceil d/2 \rceil$ MAX nodes, on the levels $0, 2, 4, \ldots$, and $\lfloor d/2 \rfloor$ MIN nodes. A MAX strategy tree branches $b$ ways at each MIN node and one way at each MAX node, so it has $b^{\lfloor d/2 \rfloor}$ leaves. A MIN strategy tree has $b^{\lceil d/2 \rceil}$ leaves. A MAX strategy tree $\sigma$ and a MIN strategy tree $\tau$ have exactly one leaf in common: the path that follows $\sigma$ at MAX nodes and $\tau$ at MIN nodes lies in both, and every common path must follow this choice at every node. So $|S| \ge b^{\lfloor d/2 \rfloor} + b^{\lceil d/2 \rceil} - 1 = L(b, d)$.

*Exactness.* Let $\sigma$ and $\tau$ be the strategy trees of Claim A. Their union $U$ has $L(b, d)$ leaves. For any values outside $U$, MAX can still follow $\sigma$ and get at least $v$, and MIN can follow $\tau$ and hold MAX to at most $v$, so the value is $v$: $U$ determines the value.

*Algorithms.* If a run of an algorithm on some input evaluates a set $S$ that does not determine the value, change the leaves outside $S$ so that the value changes. The run sees the same values, so it gives the same answer, which is wrong for one of the two inputs. So every run of a correct algorithm evaluates a determining set.

**Part 3.** Call the critical node $a_1 \cdots a_l$ of *type 1* if all $a_i = 1$. Otherwise let $a_j$ be its first entry larger than 1; it is of *type 2* if $l - j$ is even and of *type 3* if $l - j$ is odd. The children of a type 1 node are one type 1 node (the first) and $b - 1$ type 2 nodes; the critical children of a type 2 node are its first child only, of type 3; all children of a type 3 node are critical and of type 2. We show, by induction along the order of the computation, in either form:
- a type 1 node $p$ is called with $(-\infty, +\infty)$ and returns $N(p)$;
- a type 2 node $p$ is called with some $(\alpha, \beta)$, $\alpha < \beta \le N(p)$, returns a value $\ge \beta$, and calls only its first child;
- a type 3 node $p$ is called with some $(\alpha, \beta)$, $N(p) \le \alpha < \beta$, calls all its children, and returns a value $\le \alpha$.

All leaf values are real, so $N(p)$ is finite. At a leaf the three claims hold by Part 1. *Type 1.* The first child is type 1 and gets $(-\infty, +\infty)$ because $m$ starts at $-\infty$ or at $\alpha = -\infty$; it returns $N(p_1)$, so $m = -N(p_1) = N(p)$ by perfect ordering. Each later child $p_i$ is type 2 and gets $(-\infty, -N(p))$; as $-N(p_i) \le N(p)$ we have $-N(p) \le N(p_i)$, so it returns a value $\ge -N(p)$, which gives $t \le N(p) = m$. So $m$ does not change, no cutoff happens ($\beta = +\infty$), and $p$ returns $N(p)$. *Type 2.* The first child gets $(-\beta, -\alpha)$, it is type 3 and $N(p_1) = -N(p) \le -\beta$, so it returns a value $\le -\beta$ and $t \ge \beta$: the loop stops after one child. *Type 3.* Every child $p_i$ is type 2. Before child $i$, every earlier $t$ was $\le \alpha$, so $\max(m, \alpha) = \alpha$ and $p_i$ gets $(-\beta, -\alpha)$. As $-N(p_i) \le N(p) \le \alpha$ we have $N(p_i) \ge -\alpha$, so it returns a value $\ge -\alpha$ and $t \le \alpha < \beta$. There is no cutoff, and the result is $\le \alpha$.

So the search examines exactly the critical nodes. On level $l$ there are $b^{\lfloor l/2 \rfloor}$ sequences with $a_i = 1$ at all odd $i$, $b^{\lceil l/2 \rceil}$ with $a_i = 1$ at all even $i$, and one sequence in both, which gives $L(b, l)$.

**Part 4.** Work in minimax form. Sort $b^d$ distinct numbers and deal them out from the root: a node gets a block of consecutive numbers, cuts it into $b$ equal blocks, and gives them to its children in increasing order at a MAX node and in decreasing order at a MIN node. Every leaf below an earlier child is then worse for the mover than every leaf below a later child. Let $B_p$ be the block of node $p$; its value $V(p)$ is in $B_p$. We show that each node $p$ is called with a window $(\alpha, \beta)$, written for MAX, with $\alpha < \min B_p$ and $\max B_p < \beta$. This holds at the root. Let it hold at a MAX node $p$. By Part 1 each child that meets the claim returns its exact value. Before child $i$ the lower bound is $\max(\alpha, V(p_{i-1}))$, and $V(p_{i-1}) \le \max B_{p_{i-1}} < \min B_{p_i}$; the upper bound is $\beta > \max B_p \ge \max B_{p_i}$. So the claim holds for child $i$, and $m \le \max B_p < \beta$, so no cutoff happens. MIN nodes are the same with the order reversed. So no cutoff happens anywhere and all $b^d$ leaves are evaluated. $\blacksquare$

## Consequences

- **Alpha-beta is optimal in the best case.** On a uniform tree no algorithm can evaluate fewer leaves than alpha-beta with perfect ordering. Better algorithms can only win on trees that are not perfectly ordered, which is where [SSS*](/sss-star/) and the null-window searches gain.
- **Twice the depth.** $L(b, d)$ is about $2 b^{d/2}$, so in the time that minimax needs for depth $d$, alpha-beta with good ordering reaches about depth $2d$. This is the main reason why programs spend so much effort on [move ordering](/move-ordering/).
- **The odd-even effect.** $L(b, 2k) = 2b^k - 1$ and $L(b, 2k+1) = b^{k+1} + b^k - 1$. One more ply multiplies the work by about $(b+1)/2$ from an even depth and by about $2b/(b+1)$ from an odd depth. For $b = 4$ the counts for $d = 1$ to 6 are 4, 7, 19, 31, 79 and 127.
- **Node types.** The types 1, 2 and 3 of the proof are the PV, CUT and ALL nodes of Marsland and Popowich. Type 1 nodes form the [principal variation](/principal-variation/). At a CUT node one good move is enough, so the order of the other moves matters; at an ALL node every move is searched, so the order of its moves does not change the count. [Principal variation search](/principal-variation-search/) and the parallel rule [young brothers wait](/young-brothers-wait/) are built on these types.
- **A proof is two strategies.** The minimal tree is the union of one strategy for each player. [SSS*](/sss-star/) searches the space of such strategy trees, and [proof-number search](/proof-number-search/) builds them for won and lost positions.

## Tightness

- **The bound is attained on every tree.** Part 2 gives a determining set of exactly $L(b, d)$ leaves for every choice of values, and Part 3 shows that alpha-beta finds one when the order is perfect.
- **The value range must be unbounded.** If the values come from a range with a largest element, the bound can fail. With values in $\{-1, 0, 1\}$, the tree with four leaves of value 1 and $b = d = 2$ has value 1, and the two leaves under the first child already prove it, because no leaf can be larger. With an unbounded range three leaves are needed.
- **The root value must be finite.** Knuth and Moore point out that this hypothesis is needed. If the root value is $+\infty$, alpha-beta examines only $b^{\lfloor l/2 \rfloor}$ positions on level $l$, and if it is $-\infty$, $b^{\lceil l/2 \rceil}$.
- **Perfect ordering is not always best on other trees.** On trees that are not uniform, Knuth and Moore give two trees that differ only in the order of the children, where the perfectly ordered one costs more. Their Theorem 2 shows that some order always lets alpha-beta match any other algorithm.
- **Sorting worst first is not the worst case.** Part 4 needs the strong order, in which whole subtrees are ordered. Sorting the children of every node by value, worst first, is not enough from depth 4 on. Take $b = 2$, $d = 4$, MAX at the root, and the leaves $12, 9, 14, 13, 10, 4, 16, 5, 11, 3, 15, 7, 2, 1, 8, 6$ from left to right, already sorted worst first at every node. The root value is 6. The first subtree gives 5, then the right subtree gets the window $(5, +\infty)$ for MAX. Inside it, the MIN node with the leaves 2 and 1 returns after the leaf 2, because $2 \le 5$, so the leaf 1 is skipped and alpha-beta evaluates 15 of the 16 leaves. Knuth and Moore also give a tree with distinct values on which alpha-beta makes a cutoff under every order of the children.
- **The expected case is in between.** For independent leaf values from a continuous distribution, Pearl (1982) shows that the expected number of leaves grows as $R_b^d$ with $R_b = \xi_b / (1 - \xi_b)$, where $\xi_b$ is the positive root of $x^b + x - 1 = 0$. So $R_b$ lies strictly between $b^{1/2}$ and $b$; see [alpha-beta pruning](/alpha-beta-pruning/).

## History

Michael Levin found the count $L(b, d)$ in 1961. The MIT memo of Hart and Edwards states it and gives, as its proof, a joke about "the new heuristic hand waving technique". Slagle and Dixon published a proof in 1969. Knuth and Moore (1975) gave the definition of critical positions, proved that alpha-beta examines exactly them under perfect ordering, pointed out that the root value must not be $\pm\infty$, and proved with their Theorem 2 that no algorithm does better on a suitably ordered tree. Their Corollary 3 is the lower bound for uniform trees. They note that Adelson-Velsky obtained an equivalent result. Marsland and Popowich (1985) gave the node types the names PV, CUT and ALL that programs use today.

## References
