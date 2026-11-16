---
tag: 00MBQ8
kind: technique
slug: market-based-task-allocation
name: Market-based task allocation
aliases:
- auction-based task allocation
area: robotics/multi-robot-systems
level: core
summary: Robots bid their costs for tasks in auctions, and an auctioneer or the group awards each task to the best bidder.
prereqs: [multi-robot-task-allocation, auction-algorithm]
see_also: [contract-net-protocol, consensus-based-bundle-algorithm, assignment-problem, hungarian-algorithm, greedy-algorithm, vehicle-routing-problem, submodular-function, multi-robot-system]
sources:
  - paper: doi:10.1109/JPROC.2006.876939
    title: M. Bernardine Dias, Robert Zlot, Nidhi Kalra and Anthony Stentz, Market-based multirobot coordination, a survey and analysis, Proceedings of the IEEE 94(7), 2006
    locator: pages 1257 to 1270 (single-item, combinatorial and sequential auctions, trading, and the comparison of market methods)
  - paper: doi:10.1109/TC.1980.1675516
    title: Reid G. Smith, The contract net protocol, high-level communication and control in a distributed problem solver, IEEE Transactions on Computers C-29(12), 1980
    locator: pages 1104 to 1113 (announce, bid and award)
  - paper: doi:10.1177/0278364904045564
    title: Brian P. Gerkey and Maja J. Mataric, A formal analysis and taxonomy of task allocation in multi-robot systems, International Journal of Robotics Research 23(9), 2004
    locator: pages 939 to 954 (the analysis of auction-based allocation methods)
---

Market-based task allocation lets robots trade tasks as if in a market: each robot computes what a task would cost it, sends that number as a bid, and an auction gives the task to the best bid. It is a family of methods for [multi-robot task allocation](/multi-robot-task-allocation/), and the [contract net protocol](/contract-net-protocol/) and the [consensus-based bundle algorithm](/consensus-based-bundle-algorithm/) are two of its members. It differs from the [auction algorithm](/auction-algorithm/) of Bertsekas, which raises prices until it reaches an optimal [assignment](/assignment-problem/), because robot markets usually stop after one round of bids per task and accept a greedy result in exchange for speed and few messages.

## In plain words

Each robot knows best what a job would cost it: how far it must drive, how much battery it has. So instead of a boss who must know everything, the team holds auctions. Someone offers a job, every robot that wants it says its price, and the cheapest robot gets it.

The robots can keep trading later. If a robot finds that another robot could do one of its jobs more cheaply, it sells the job. Auctions are quick and need only short messages, and a robot that breaks down can put its jobs up for sale again. The answer is usually good but not always the best possible.

## When it applies

- Each robot can compute its own cost or utility for a task, and these numbers are comparable across robots, for example travel time in seconds.
- The team gains from a quick answer more than from the best answer, and tasks arrive or change during the mission.
- Messages are possible but limited: a broadcast channel, or a connected graph of radio links. Auctions need a few messages per task, not the whole cost matrix in one place.
- Robots may fail or join, and the method should keep working.

It does not apply well when the costs of robots cannot be compared, when strong coupling between tasks makes single bids meaningless, or when the team needs a proven optimal plan.

## The template

1. **Valuation.** Each robot $i$ computes a bid for a task $j$: its cost $c_{ij}$, or for a robot that already holds tasks, its *marginal* cost, the increase of its total cost when $j$ is added to its plan, for example the extra travel when $j$ is inserted into its tour.
2. **Announcement.** An auctioneer, which may be a robot, a manager of the task or a server, announces one task, a set of tasks, or bundles.
3. **Bidding.** Robots send bids. In a sealed-bid auction each robot sends one number per task or bundle.
4. **Winner determination.** The auctioneer awards each task to the best bid, or for bundles, solves the problem of choosing non-overlapping bundles with the best total.
5. **Repeat or trade.** Unawarded tasks go to the next round. Robots may later sell tasks to robots that bid lower, which can only reduce the total cost if each trade does.

The number of robots $r$, the number of tasks $t$, and the communication graph fix the cost: one auction of one task sends one announcement to each robot and up to $r$ bids, so $O(r)$ messages, and a sequence of $t$ such auctions sends $O(r t)$ messages over a broadcast channel. The rounds are usually synchronous: all bids for an auction arrive before the award.

## Classic examples

**Single-item auctions in parallel.** All $t$ tasks are announced at once, each robot bids on its best task, and each task goes to its lowest bid. With three robots and two tasks costing $(1, 2)$, $(10, 3)$ and $(1.5, 2.5)$ seconds, task 0 goes to robot 0 with 1 s and task 1 to robot 1 with 3 s, total 4 s. This is the [contract net protocol](/contract-net-protocol/) with the full window.

**Sequential single-item auctions.** Tasks are auctioned one after the other, and each robot bids its marginal cost given the tasks it already won. In the same example, task 0 goes to robot 0, and then task 1 goes to robot 2 with 2.5 s, total 3.5 s, which is the optimum here. In routing problems, where the marginal cost depends on the tour so far, this method is widely used (heuristic; bounds exist for special cost functions).

**Trading.** Start from the parallel result, total 4 s. Robot 2 is idle and would do task 1 for 2.5 s, while robot 1 holds it at 3 s. Robot 1 sells task 1 to robot 2, and the total drops to 3.5 s. Each such trade lowers the total cost, so a sequence of trades ends, but it may end in a local optimum.

**Combinatorial auctions.** Robots bid on bundles of tasks, which captures synergy, such as two targets next to each other. Choosing the best set of non-overlapping bundles is NP-hard in general, so practical systems limit the bundles, for example to clusters of nearby tasks.

**Consensus auctions.** In the [consensus-based bundle algorithm](/consensus-based-bundle-algorithm/) there is no auctioneer: each robot is both bidder and auctioneer and the winners are agreed by messages between neighbors.

## Variations

- **MiniSum, MiniMax, MiniAve.** The team objective can be the total cost, the largest cost of one robot (the makespan), or the average time to finish a task. The bid rule must match the objective, for example marginal makespan for MiniMax.
- **Price-based optimal methods.** The [auction algorithm](/auction-algorithm/) keeps prices and lets robots outbid each other by at least $\varepsilon$; it ends within $\varepsilon$ of the optimum for one task per robot.
- **Hierarchical markets.** Leaders run auctions for their group and trade with other leaders.
- **Re-auctioning.** Tasks of a failed robot, or tasks whose cost changed, are offered again.
- **Robots that can be wrong.** Bids may be estimates; a robot that wins a task and then finds it too costly can pay a penalty to give it up.

## Pitfalls

- **Greedy losses.** Parallel single-item auctions can have an unbounded cost ratio: with costs $1, 2$ for robot 0 and $2, M$ for robot 1, robot 0 takes task 0, robot 1 pays $M$, while the best total is 4.
- **Wrong valuations.** Bidding full cost instead of marginal cost, for a robot that already holds tasks, makes robots overbid and gives poor allocations.
- **Double awards.** If a robot bids on several tasks in parallel, it can win more than it can do. Bid on one task per round, or let robots refuse.
- **Stale bids.** The cost of a robot changes as it moves. Bids that are too old lead to bad awards.
- **Lost messages.** An auction that waits for every bid stalls when a message is lost. Use time-outs and re-auction.

## Exercises

1. In the three-robot example, show that the order "task 1 first, then task 0" in a sequential auction also gives 3.5 s, and find an order and a cost table where the sequential auction is worse than the parallel one.
2. Show that a trade between two robots, where each task goes to the robot with the lower cost for it, never increases the total cost, and give an example where no single trade helps but a swap of two tasks does.
3. With $r$ robots and $t$ tasks on a broadcast channel, count the messages of $t$ sequential single-item auctions, and compare them with sending the full $r \times t$ cost matrix to one server.

## References
