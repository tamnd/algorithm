---
tag: B1984T
kind: concept
slug: online-algorithm
name: Online algorithm
aliases:
- on-line algorithm
area: online-and-streaming/competitive-analysis
level: intro
summary: An algorithm that must act on each input piece as it arrives, without knowing the future.
see_also: [offline-algorithm, offline-optimum, competitive-ratio, request-answer-game, randomized-online-algorithm, advice-model, ski-rental-problem, paging-problem]
sources:
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1 (online problems, online algorithms and competitive analysis, with list accessing as the first example)
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the comparison of on-line list update and paging rules with the best off-line rule on each sequence
  - book: isbn:9783540649175
    title: Amos Fiat and Gerhard J. Woeginger (eds.), Online Algorithms, The State of the Art, Lecture Notes in Computer Science 1442, Springer, 1998
    locator: Chapter 1 (competitive analysis of algorithms) and the problem chapters
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gabor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the definition of on-line algorithms for request-answer games
---

An online algorithm reads its input as a sequence of requests $\sigma = r_1, r_2, \ldots$ and must give an answer to each request $r_i$ before it sees $r_{i+1}$, and it can not change an answer later. It is the opposite of an [offline algorithm](/offline-algorithm/), which sees the whole input first. The standard measure of an online algorithm is the [competitive ratio](/competitive-ratio/): its cost compared with the [offline optimum](/offline-optimum/) on the same sequence.

## In plain words

Most textbook algorithms get the whole input, think, and then answer. An online algorithm works in a world where the input comes one piece at a time, and each piece needs an answer at once. A cache must decide which page to throw out now, and it does not know which pages the program asks for next. A skier must decide today whether to rent or to buy skis, and does not know how many more days of snow there are.

The algorithm may remember everything it has seen so far. What it does not have is the future. So even with unlimited computing time, it can make choices that look bad later. The theory asks how much this missing knowledge costs.

## The idea

**The formal model.** Fix a set $R$ of requests and a set $A$ of answers. A deterministic online algorithm is a family of functions $g_i : R^i \to A$, one for each $i \ge 1$. On the sequence $\sigma = r_1 r_2 \cdots r_n$ it answers $a_i = g_i(r_1, \ldots, r_i)$. The answer $a_i$ depends on $r_1, \ldots, r_i$ (and so on the earlier answers, which are functions of these), and not on $r_{i+1}, \ldots, r_n$. The algorithm also does not know $n$, the length of the sequence. A cost function gives the cost $\mathrm{ALG}(\sigma)$ of the answers on $\sigma$. This is the [request-answer game](/request-answer-game/) of Ben-David, Borodin, Karp, Tardos and Wigderson (1994).

**What "online" restricts.** The restriction is about information, not about time or memory. An online algorithm may take exponential time per request and store all past requests. So a bad online result is not a statement about computing power. It is a statement that no rule which sees only the past can do well on all futures.

**How it is measured.** For a minimization problem, the online algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$, where $\mathrm{OPT}(\sigma)$ is the [offline optimum](/offline-optimum/) and $b$ is a constant that does not depend on $\sigma$. The [competitive ratio](/competitive-ratio/) page gives the exact definition, the strict form with $b = 0$ and the convention for maximization. The analysis is a game against an adversary who knows the algorithm and picks the worst sequence. For a [randomized online algorithm](/randomized-online-algorithm/), the strength of the adversary must be named: [oblivious](/oblivious-adversary/), [adaptive online](/adaptive-adversary/) or [adaptive offline](/adaptive-offline-adversary/).

**Between online and offline.** Some models give the algorithm a little of the future: a lookahead of the next few requests, the length $n$ in advance, or a few bits from an oracle that knows $\sigma$. The last one is the [advice model](/advice-model/). It measures in bits how much knowledge of the future is worth. Predictions from machine learning give the [learning-augmented algorithms](/learning-augmented-algorithms/).

**Notation used on the competitive analysis pages.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution, $c$ is the competitive ratio, and $k$ is the cache size or the number of servers.

## Examples

- **[Ski rental](/ski-rental-problem/).** Each day the skier rents for 1 or buys for $B$. The online rule "rent for $B - 1$ days, then buy" is the [break-even strategy](/break-even-strategy/). It pays at most $2 - 1/B$ times the offline cost $\min(n, B)$, where $n$ is the number of ski days, and no deterministic online rule does better.
- **[Paging](/paging-problem/).** A cache of $k$ pages serves page requests. [LRU](/lru/) evicts the page used least recently. It is $k$-competitive, and the offline rule of [Belady](/belady-algorithm/) is optimal.
- **[List update](/list-update-problem/).** [Move to front](/move-to-front/) moves each accessed item to the front of a linked list. It is 2-competitive (Sleator and Tarjan 1985).
- **Online scheduling.** Jobs arrive one at a time and each must go to a machine at once. Graham's [list scheduling](/list-scheduling-competitive-ratio/) is $(2 - 1/m)$-competitive for the makespan on $m$ machines.
- **Selection.** In the [secretary problem](/secretary-problem/), candidates arrive in random order and each must be hired or rejected on the spot.
- **Non-example.** [Merge sort](/merge-sort/) reads its whole input before it writes the first output item, so it is offline. [Insertion sort](/insertion-sort/) can keep a sorted prefix as items arrive, so it can run online, but its output is not final until the input ends. Online algorithms in the strict sense of this page commit to each answer at once.
- **Not the same as streaming.** A [streaming algorithm](/streaming-model/) also reads its input once in order, but its limit is memory, and it usually answers only at the end. An online algorithm has no memory limit, but must commit to each answer at once.

## Where it is used

- **Systems.** Caches, page replacement, buffer management, TCP acknowledgments ([TCP acknowledgment problem](/tcp-acknowledgment-problem/)), spin-or-block decisions in locks and power-down of idle devices are all online problems. The rent-or-buy structure of [ski rental](/ski-rental-problem/) appears in many of them.
- **Data structures.** A self-adjusting data structure, such as a move-to-front list or a splay tree, serves an online sequence of operations. Its analysis compares it with the best offline structure for the same sequence.
- **Networks and markets.** Routing and admission of calls, load balancing, ad allocation ([online bipartite matching](/online-bipartite-matching/)) and online auctions decide each request when it arrives.
- **Learning.** In online learning, the learner predicts before it sees each outcome. There the measure is the [regret](/regret/) against the best fixed action in hindsight, as in the [weighted majority](/weighted-majority/) algorithm, and not the competitive ratio.

## References
