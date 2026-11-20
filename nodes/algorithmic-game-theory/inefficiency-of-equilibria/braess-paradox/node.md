---
tag: 9Q4T6J
kind: concept
slug: braess-paradox
name: Braess's paradox
aliases:
- Braess paradox
area: algorithmic-game-theory/inefficiency-of-equilibria
level: intro
summary: Adding a fast link to a network can raise the equilibrium latency of every traveler in selfish routing.
prereqs: [wardrop-equilibrium, system-optimal-flow]
see_also: [braess-paradox-detection-hardness, pigou-example, roughgarden-tardos-four-thirds-bound, pigou-bound, price-of-anarchy, selfish-routing-model, prisoners-dilemma, atomic-congestion-game]
sources:
  - paper: doi:10.1007/BF01918335
    title: "Dietrich Braess, Über ein Paradoxon aus der Verkehrsplanung, Unternehmensforschung 12(1) (1968), 258-268"
    locator: the four-node network in which a new road raises the travel time of all users
  - paper: doi:10.1287/trsc.1050.0127
    title: "Dietrich Braess, Anna Nagurney and Tina Wakolbinger, On a paradox of traffic planning, Transportation Science 39(4) (2005), 446-450"
    locator: English translation of the 1968 paper
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 18, Tim Roughgarden, Routing games, Example 18.4 (Braess's paradox), Remark 18.22 (bounds on Braess's paradox) and Section 18.6 (notes on the zero-latency variant and the spring analogue)
  - paper: doi:10.1016/j.jcss.2005.05.009
    title: "Tim Roughgarden, On the severity of Braess's Paradox: designing networks for selfish users is hard, Journal of Computer and System Sciences 72(5) (2006), 922-953"
    locator: the worst-case size of the paradox in networks with n vertices and the hardness of finding the best subnetwork
  - paper: doi:10.1038/352699a0
    title: "Joel E. Cohen and Paul Horowitz, Paradoxical behaviour of mechanical and electrical networks, Nature 352 (1991), 699-701"
    locator: the analogue with springs and strings and with electrical circuits
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 11 (Braess's paradox)
---

Braess's paradox is the fact that a new road can make traffic slower for everyone. In the [selfish routing model](/selfish-routing-model/), adding an edge to a network can raise the latency of every traveler at the [Wardrop equilibrium](/wardrop-equilibrium/), even though no traveler is forced to use the new edge. Dietrich Braess found it in 1968. It shows that the equilibrium is not a [system optimal flow](/system-optimal-flow/), since the planner's optimum can never get worse when an edge is added. For affine latencies the equilibrium cost can rise by at most a factor $4/3$ ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)).

## In plain words

One thousand drivers go from a town to a city. There are two routes. Each route has one wide road that always takes one hour, and one narrow road that takes as long as the share of drivers on it. The drivers split evenly, and each drive takes an hour and a half. Now a free, instant bridge joins the ends of the two narrow roads. Each driver sees that the narrow roads, joined by the bridge, are never slower than a wide road. So every driver takes both narrow roads, each now takes one hour, and every drive takes two hours. No driver can do better alone, but all are worse off than before the bridge was built.

## The idea

**The network without the shortcut.** Vertices $s, v, w, t$ and rate 1. The path $s \to v \to t$ uses an edge with latency $x$ and then an edge with latency 1. The path $s \to w \to t$ uses an edge with latency 1 and then an edge with latency $x$. By symmetry the equilibrium sends $1/2$ on each path. Each path has latency $1/2 + 1 = 3/2$, and the cost is $3/2$. This flow is also optimal.

**Add the shortcut.** Add the edge $v \to w$ with latency 0. The new path $s \to v \to w \to t$ has latency $f_{sv} + f_{wt}$. At the old flow this is $1/2 + 1/2 = 1 < 3/2$, so the old flow is no longer an equilibrium. The new equilibrium sends all traffic on $s \to v \to w \to t$. Then $f_{sv} = f_{wt} = 1$, and all three paths have latency 2: the zigzag path $1 + 0 + 1$, and each outer path $1 + 1$. It is the unique equilibrium, by the argument in [Wardrop equilibrium](/wardrop-equilibrium/). The cost is 2, and every traveler is worse off.

**The optimum does not change.** The old flow is still feasible, so the optimal cost is at most $3/2$. The marginal costs at the old flow are $2 \cdot 1/2 = 1$ on the two $x$ edges, 1 on the constant edges and 0 on the shortcut, so all three paths have marginal cost 2 and the old flow is still optimal. The shortcut is useless to a planner. It only changes the equilibrium.

**Why it happens.** For each traveler the shortcut route is a dominant choice: $f_{sv} + f_{wt} \le f_{sv} + 1$ and $f_{sv} + f_{wt} \le 1 + f_{wt}$, whatever the others do. But each traveler on the $x$ edges slows all the others there, and pays nothing for it. As in the [prisoner's dilemma](/prisoners-dilemma/), each player's best choice leads to an outcome worse for all. The ratio $2 / (3/2) = 4/3$ of the new equilibrium to the optimum is also the price of anarchy of the new network, the same as in [Pigou's example](/pigou-example/).

## Examples

**Braess's numbers.** The example is often given with these numbers, for 6 units of traffic. The edges $s \to v$ and $w \to t$ have latency $10x$, the edges $v \to t$ and $s \to w$ have latency $x + 50$, and the shortcut $v \to w$ has latency $x + 10$.

- Without the shortcut, each outer path carries 3. Its latency is $10 \cdot 3 + (3 + 50) = 83$, and the total is $6 \cdot 83 = 498$.
- With the shortcut, each of the three paths carries 2. Then $f_{sv} = f_{wt} = 4$, $f_{vt} = f_{sw} = 2$ and $f_{vw} = 2$. The outer paths have latency $40 + 52 = 92$, and the shortcut path has $40 + 12 + 40 = 92$. The total is $6 \cdot 92 = 552$.
- The optimum still keeps the 3 and 3 split. There the outer paths have marginal cost $20 \cdot 3 + (2 \cdot 3 + 50) = 116$, and the shortcut path has $60 + 10 + 60 = 130$, so moving traffic onto the shortcut would raise the total.

Here the latency of each traveler rises from 83 to 92, a factor $92/83 \approx 1.108$, which is below the $4/3$ limit for affine latencies.

**Springs and strings.** Hang a weight from two springs in series, joined by a short string. Add two slack safety strings: one from the support to the top of the lower spring, and one from the bottom of the upper spring to the weight. Then cut the short middle string. The springs now hang in parallel, each with half the load, and the weight rises. Force plays the role of traffic, and the stretch of a spring is a latency linear in its load (Cohen and Horowitz 1991; NRTV notes to Chapter 18). The same effect appears in electrical circuits.

**Atomic players.** The paradox does not need a continuum of travelers. In the unit network with 4 players of weight $1/4$, the profile with all players on the zigzag path is a pure equilibrium with latency 2 each, while 2 and 2 on the outer paths without the shortcut give $3/2$ each ([atomic congestion game](/atomic-congestion-game/)).

**How large can it be.** For affine latencies, the old equilibrium is a feasible flow in the new network, so it costs at least the new optimum. The new equilibrium costs at most $4/3$ times the new optimum, so at most $4/3$ times the old equilibrium. The unit example reaches this (NRTV Remark 18.22). For a class of latencies with Pigou bound $\alpha$, the factor is at most $\alpha$ ([Pigou bound](/pigou-bound/)). With general latencies the factor can grow with the size of the network, about $n/2$ for a network with $n$ vertices, and this is the worst case (Roughgarden 2006).

## Where it is used

- **Network design.** A planner who wants a low equilibrium cost may do better by closing roads. Finding the best set of edges to remove is computationally hard (Roughgarden 2006; [Braess's paradox detection](/braess-paradox-detection-hardness/)).
- **Lower bounds on the price of anarchy.** If adding edges raises the equilibrium cost by a factor $\rho$, the new network has [price of anarchy](/price-of-anarchy/) at least $\rho$. So bounds on the price of anarchy limit the paradox, and examples of the paradox give lower bounds.
- **A test case.** The unit network is a standard check for code that computes equilibria: the equilibrium with the shortcut has cost 2, the optimum has cost $3/2$, and the [Beckmann potential](/beckmann-potential/) is least at the all-zigzag flow.
- **Physics and engineering.** The spring analogue and similar circuits show the same effect outside traffic.

**History.** Braess described the paradox in 1968 for a four-node road network. An English translation by Braess, Nagurney and Wakolbinger appeared in 2005. The version with a zero-latency shortcut and latencies $x$ and 1 is due to L. Schulman, as noted in NRTV. Cohen and Horowitz (1991) found the mechanical and electrical analogues. Roughgarden (2006) found the worst-case size of the paradox and showed that designing networks to avoid it is computationally hard.

## References
