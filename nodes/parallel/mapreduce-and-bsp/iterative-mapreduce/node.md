---
tag: T3JHYW
kind: concept
slug: iterative-mapreduce
name: Iterative MapReduce
aliases:
- multi-round MapReduce
- chained MapReduce jobs
area: parallel/mapreduce-and-bsp
level: advanced
summary: Running an iterative algorithm as a chain of MapReduce jobs, where the output of one round is the input of the next. Each round pays again for the data that does not change.
prereqs: [mapreduce-model]
see_also: [pregel-model, resilient-distributed-datasets, mrc-model, pagerank, power-iteration, connected-components, k-means, distributed-pagerank]
sources:
  - paper: doi:10.14778/1920841.1920881
    title: "Yingyi Bu, Bill Howe, Magdalena Balazinska and Michael D. Ernst, HaLoop: efficient iterative data processing on large clusters, PVLDB 3(1-2), 2010"
    locator: pp. 285-296; the loop-aware scheduler and the reducer input, reducer output and mapper input caches
  - paper: doi:10.1145/1851476.1851593
    title: "Jaliya Ekanayake, Hui Li, Bingjing Zhang, Thilina Gunarathne, Seung-Hee Bae, Judy Qiu and Geoffrey Fox, Twister: a runtime for iterative MapReduce, HPDC 2010"
    locator: pp. 810-818; long-running map and reduce tasks with static data kept in memory
  - paper: "Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma, Murphy McCauley, Michael J. Franklin, Scott Shenker and Ion Stoica, Resilient distributed datasets: a fault-tolerant abstraction for in-memory cluster computing, NSDI 2012"
    locator: Section 3.2.2 (PageRank) and the evaluation, which compares iterative jobs with Hadoop
  - book: isbn:9781108476348
    title: "Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020"
    locator: Chapter 2, algorithms that use MapReduce and extensions of MapReduce for recursion and iteration
---

[MapReduce](/mapreduce-model/) runs one map phase and one reduce phase, and it has no loop. Many algorithms are iterative: [PageRank](/pagerank/), [connected components](/connected-components/), [k-means](/k-means/) and gradient methods repeat the same step until the result stops changing. Iterative MapReduce runs such an algorithm as a chain of jobs, one per iteration, under a driver program that feeds the output of round $t$ into round $t + 1$ and tests when to stop. The total cost is the number of rounds times the cost of one round, and in plain MapReduce each round reads, shuffles and writes the data that never changes, such as the graph.

## In plain words

Imagine a team that must improve a large report many times. The rule of the office is that each improvement is a new task: take the whole report from the archive, copy every page, send the pages to the right people, collect their changes, and put a complete new report back in the archive. Most of the pages do not change from one round to the next, but the rule makes the team carry them every time. If the job needs fifty rounds, the team carries the report fifty times. Two ideas help. Find a method that needs fewer rounds, or change the office so that people keep the pages that do not change on their desks between rounds.

## The idea

**The driver loop.** Iterative MapReduce has a sequential driver around parallel jobs.

```pseudo
procedure ITERATE(input)
    state ← input
    t ← 0
    repeat
        state' ← MAPREDUCE(MAP_t, REDUCE_t, state)   ▷ one job: read, shuffle, write
        done ← STOP(state, state')                   ▷ a counter, or one more job
        state ← state'
        t ← t + 1
    until done
    return state
```

Each job is a [superstep](/superstep/) with a barrier at the end: no reducer of round $t + 1$ starts before every reducer of round $t$ has written its output. The reducer keeps no state between jobs, so everything that round $t + 1$ needs must be in the output of round $t$ or in a side file that the mappers read.

**The cost of a round.** In a system such as Hadoop, a round costs a job start (scheduling the tasks), reading the input from the distributed file system, the shuffle, and writing the output with replication. For a state of $V$ records, one round costs about $c_0 + c_1 V$, and $R$ rounds cost $R(c_0 + c_1 V)$. Two parts of $V$ behave differently:

- the loop-variant data, such as the current ranks or labels, which changes in each round;
- the loop-invariant data, such as the graph or the training points, which is the same in each round but must still be carried, because the reducers forget it.

For PageRank on a graph with $n$ vertices and $m$ edges, the state is the graph plus the ranks. Each mapper emits a share of its rank along each of its out-edges, which is $m$ records, and also re-emits its list of out-edges so that the reducer can rebuild the record for the next round: $n + m$ records per round. Of these, the $n$ adjacency lists are loop-invariant.

**How many rounds?** For PageRank with follow probability $\alpha$ on a graph where every vertex has an out-edge, the update is $x_{t+1} = \frac{1 - \alpha}{n}\mathbf{1} + \alpha M x_t$, with $M$ a column-stochastic matrix. If $x^*$ is the fixed point, then

$$
\lVert x_{t+1} - x^* \rVert_1 = \alpha \lVert M (x_t - x^*) \rVert_1 \le \alpha \lVert x_t - x^* \rVert_1 ,
$$

because a column-stochastic matrix does not increase the $L_1$ norm. Two probability vectors are at $L_1$ distance at most $2$, so after $k$ rounds the error is at most $2\alpha^k$. The number of rounds for an error $\epsilon$ is the least $k$ with $2\alpha^k \le \epsilon$, which does not depend on the size of the graph. For $\alpha = 0.85$ this is $19$ rounds for $\epsilon = 0.1$, $47$ rounds for $\epsilon = 10^{-3}$ and $90$ rounds for $\epsilon = 10^{-6}$.

For label propagation the number of rounds depends on the graph. In the minimum-label method for connected components, each vertex starts with its own number as its label, and in each round it takes the smallest label among itself and its neighbours. By induction, after round $t$ a vertex holds the smallest vertex number within distance $t$. So the labels are final after $D$ rounds, where $D$ is the largest distance from a vertex to the smallest vertex of its component, and the driver sees no change in round $D + 1$. On a path of $n$ vertices this is up to $n$ rounds. Algorithms with $O(\log n)$ rounds exist, and the [MRC model](/mrc-model/) is the setting in which such round counts are compared.

**Making rounds cheaper.** Systems for iterative MapReduce keep the loop-invariant data near the tasks that use it.

- HaLoop (Bu, Howe, Balazinska and Ernst, 2010) adds a loop to the job API, schedules the task for a partition on the machine that ran it in the previous round, and caches the reducer input for the invariant data, so the graph is shuffled only once. It also caches the reducer output, so that the stop test compares with the previous round locally.
- Twister (Ekanayake and others, 2010) keeps map and reduce tasks alive between rounds, with the static data loaded once into memory, and sends only the variable data in each round.
- Spark keeps the data in memory as [resilient distributed datasets](/resilient-distributed-datasets/), and recovers a lost partition from its lineage instead of from files written in each round. Its authors report iterative jobs up to $20$ times faster than on Hadoop.

## Examples

**PageRank with and without a cache.** Take the graph with out-edges $0 \to \{1, 2\}$, $1 \to \{2\}$, $2 \to \{0\}$, $3 \to \{0, 2\}$, so $n = 4$ and $m = 6$, with $\alpha = 0.85$.

| | records per round | 3 rounds |
|---|---|---|
| plain MapReduce (ranks and adjacency lists) | $n + m = 10$ | $30$ |
| graph cached at the reducers | $m = 6$ | $18$ |

Both give the same ranks after three rounds, $(0.3314, 0.2273, 0.4038, 0.0375)$, equal to three steps of the [power iteration](/power-iteration/) from the uniform vector. Vertex $3$ has no in-edge, so with the cache it receives no record at all; the reducer must still output it, with rank $(1 - \alpha)/n = 0.0375$, from the cached list of keys. A first version of the simulator of this page forgot this case and lost vertex $3$ and its edges after one round.

**Minimum labels.** Take the path $3 - 1 - 4 - 0 - 2$. The labels after each round are:

| round | 3 | 1 | 4 | 0 | 2 |
|---|---|---|---|---|---|
| start | 3 | 1 | 4 | 0 | 2 |
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 | 0 |
| 4 | 0 | 0 | 0 | 0 | 0 |

Vertex $3$ is at distance $3$ from vertex $0$, so the labels are final after round $3$, and the driver stops after round $4$ sees no change. Each round emits $n + 2m = 13$ records: each vertex sends its label to itself and to each neighbour.

**k-means.** In [Lloyd's algorithm](/lloyds-algorithm/) as MapReduce, the $k$ centers are a small side file that every mapper reads. A mapper assigns each point to its nearest center and emits (center, point); a reducer averages its points into the new center. The points are loop-invariant and are read again in each round, but they are not shuffled if a combiner sends one partial sum and count per center from each mapper.

## Where it is used

- Graph algorithms on Hadoop before graph systems existed: PageRank, [distributed PageRank](/distributed-pagerank/), components and shortest paths as chains of jobs, often with a separate job to test convergence.
- Machine learning on Hadoop: k-means, [logistic regression](/logistic-regression/) and other [gradient descent](/gradient-descent/) methods, one job per pass over the data.
- The design of later systems. HaLoop and Twister adapt MapReduce to loops; [Pregel](/pregel-model/) keeps each vertex and its edges on one worker for the whole computation and sends only messages; Spark keeps the state in memory. All three remove the per-round cost of the loop-invariant data.
- The theory of MapReduce, where the [MRC model](/mrc-model/) counts rounds as the main cost.

## References
