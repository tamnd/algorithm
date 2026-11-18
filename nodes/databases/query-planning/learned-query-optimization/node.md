---
tag: 9MJVM2
kind: technique
slug: learned-query-optimization
name: Learned query optimization
aliases:
- learned plan selection
area: databases/query-planning
level: research
summary: "Choose join orders, whole plans or optimizer hints with a model trained on the measured latency of executed plans. The gains are measured on benchmarks; there is no guarantee."
prereqs: [query-optimization, join-ordering, cost-model]
see_also: [learned-cardinality-estimation, thompson-sampling, contextual-bandit, q-learning, selinger-join-enumeration, cascades-framework, mid-query-reoptimization, eddies]
sources:
  - paper: doi:10.14778/3342263.3342644
    title: Ryan Marcus, Parimarjan Negi, Hongzi Mao, Chi Zhang, Mohammad Alizadeh, Tim Kraska, Olga Papaemmanouil and Nesime Tatbul, Neo, a learned query optimizer, Proceedings of the VLDB Endowment 12(11) (2019), 1705 to 1718
    locator: the value network on plan trees, the best-first plan search guided by it, the start from the plans of an expert optimizer, and the retraining on measured latencies
  - paper: doi:10.1145/3448016.3452838
    title: "Ryan Marcus, Parimarjan Negi, Hongzi Mao, Nesime Tatbul, Mohammad Alizadeh and Tim Kraska, Bao: making learned query optimization practical, Proceedings of ACM SIGMOD 2021, 1275 to 1288"
    locator: the choice of a hint set per query by a tree convolutional model and Thompson sampling, on top of the PostgreSQL optimizer
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: the Join Order Benchmark used to evaluate learned optimizers, and the measured effect of estimation errors on plan quality
---

Learned query optimization uses a model trained on the observed running times of plans to choose the plan for a new query. A classic [query optimizer](/query-optimization/) searches the plans with a [cost model](/cost-model/) and [cardinality estimates](/cardinality-estimation/) that are written by hand and can be far off. A learned optimizer closes the loop: it runs plans, measures their latency, and trains a model that predicts the latency of a plan, so that later choices improve. Neo (Marcus et al., 2019) learns to build whole plans. Bao (Marcus et al., 2021) keeps the existing optimizer and learns only which set of hints to give it for each query. All results of these systems are measurements; no learned optimizer has a guarantee on the plans it picks. [Learned cardinality estimation](/learned-cardinality-estimation/) is the related technique that learns only the size estimates.

## In plain words

A database chooses how to run a query by guessing the cost of many possible plans. The guesses come from fixed formulas, and they are often wrong. The database does not learn from its mistakes: it makes the same bad choice the next time.

A learned optimizer remembers how long each plan really took. It trains a model that looks at a plan and predicts its time, and it uses the model to pick plans for new queries. Some systems build plans from scratch with the model. Others ask the old optimizer for a few different plans, each made with a different setting, and let the model pick one.

This can fix bad choices for queries like those it has seen. It cannot promise anything for a new kind of query, and while it learns it sometimes picks slow plans.

## When it applies

- **Repeated workloads.** The same kinds of queries run many times, so the measured latencies of past plans tell something about future ones.
- **Bad estimates.** The data has correlations or skew that make the classic estimates wrong, so the classic optimizer often picks slow plans.
- **Room to explore.** The system can afford some slow plans while it learns, or it can test plans on a copy of the data.
- **It does not apply** well to ad hoc queries unlike any seen before, to queries that run once, or where latency must be predictable, because a learned choice can change after each retraining.

## The template

1. **Choose the action space.** Whole plans (Neo), only the join order (earlier work that used [Q-learning](/q-learning/) and other reinforcement learning methods), or a choice among a small set of hint sets for the existing optimizer (Bao). A hint set turns off some operators, for example nested loop joins or index scans.
2. **Encode the plan.** Represent a plan as a tree whose nodes carry the operator type, the tables and estimates of the classic optimizer. Neo and Bao both use tree convolution, a neural network that applies the same small filters to each node and its two children.
3. **Predict the latency.** Train the model on pairs (plan, measured latency). Neo starts from plans of an expert optimizer, so that the first model is not random, and then retrains on its own plans.
4. **Choose.** Neo does a best-first search over partial plans, ordered by the predicted latency of the best completion. Bao asks the optimizer for one plan per hint set and runs the plan with the best prediction.
5. **Explore.** Without exploration, the model never learns that a plan it predicts as slow is fast. Bao uses [Thompson sampling](/thompson-sampling/): it trains the model on a random resample of its experience, so its predictions vary, and picks the best plan under the sampled model.
6. **Retrain and guard.** Retrain on new experience at intervals. Keep the native plan as a fallback, and limit the time a plan may run during exploration.

**What is guaranteed (proved).** In the design of Bao, every candidate plan is a plan the native optimizer builds under some hint set, and the empty hint set gives the native plan. So the plan space is a subset of the native plan space, and if the model predicted perfectly, the chosen plan would be the fastest of the candidates, never slower than the native plan. With an imperfect model, nothing is guaranteed: the model can rank a slow plan first. Regret bounds for Thompson sampling in [multi-armed bandits](/multi-armed-bandit/) assume rewards from fixed distributions, which a changing database does not satisfy, so they do not transfer as a proof.

## Classic examples

**Choosing hints per query.** Take two query templates that occur equally often, and three hint sets with these mean latencies.

| hint set | template X | template Y | mean |
|---|---|---|---|
| none (native plan) | 10 s | 1 s | 5.5 s |
| no nested loop joins | 2 s | 4 s | 3.0 s |
| no index scans | 30 s | 3 s | 16.5 s |

The best single hint set for the whole workload (no nested loop joins) gives a mean of 3.0 s. A choice per query, with no nested loop joins for X and the native plan for Y, gives $(2 + 1)/2 = 1.5$ s, half of the best fixed choice and a quarter of the native optimizer. A model that tells the templates apart can find this choice after a few runs of each. Each exploration run of the third hint set on X costs 30 s, which is why exploration must be limited.

**Neo (measured).** Marcus et al. report that Neo, after training, produced plans that matched or beat those of PostgreSQL and of commercial optimizers on the Join Order Benchmark and other workloads, but needed many hours of training and had to be trained again for a new schema.

**Bao (measured).** Marcus et al. report that Bao, on top of PostgreSQL and a commercial system, lowered the total time and the tail latency of their workloads, trained in much less time than Neo, and adapted to changes in the data and the schema better. These are measurements on their benchmarks and hardware.

## Variations

- **Learned join ordering.** Formulate join ordering as a sequence of decisions and learn a policy or a value function with deep [Q-learning](/q-learning/) or policy gradients. These systems were the first step and learn only the join order.
- **Bandits over hints.** Bao is a [contextual bandit](/contextual-bandit/): the context is the query, the arms are the hint sets, and the reward is the negative latency. Other bandit methods, such as upper confidence bounds, fit the same frame.
- **Learning to correct the cost model.** Keep the search of a [Cascades](/cascades-framework/) or [Selinger](/selinger-join-enumeration/) optimizer and learn corrections to its cost or cardinality estimates, which is the narrowest change.
- **Run-time adaptation.** [Mid-query re-optimization](/mid-query-reoptimization/) and [eddies](/eddies/) fix bad plans while the query runs, using what the query itself shows; learned optimizers fix them across queries, using past runs. The two can be combined.

## Pitfalls

- **Regressions.** A retrained model can pick a much slower plan for a query that was fine before. Production use needs a check against the native plan, for example by running the learned choice only where it has been fast.
- **Cost of training data.** Each training example is a full run of a plan. Slow plans are the most informative and the most expensive to run.
- **Overfitting to a benchmark.** A model trained and tested on the same query templates can look much better than it is on new queries. Test on held-out templates.
- **Inference time.** The model is called once per candidate plan, or many times in a plan search. For short queries, this can cost more than it saves.
- **Unclear failures.** When a learned choice is wrong, it is hard to see why, which makes the system hard to tune and to debug.

## Exercises

1. In the hint example, a system that tries each hint set once on each template and then always picks the best has spent how much time on exploration? (Answer: $10 + 2 + 30 + 1 + 4 + 3 = 50$ s. The best choice for the same six runs costs $3 \cdot 2 + 3 \cdot 1 = 9$ s, so exploration cost 41 s more.)
2. Show that a choice among hint sets that always includes the native plan cannot be worse than the native plan if the latency predictions are exact, and give a case where a small prediction error makes it much worse.
3. Explain why Thompson sampling needs a model whose predictions vary between samples, and how Bao gets this variation.
4. Design a test that separates the effect of better cardinality estimates from the effect of a learned cost model in a learned optimizer.

## References
