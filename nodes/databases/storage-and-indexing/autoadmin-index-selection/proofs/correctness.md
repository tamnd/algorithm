---
title: The AutoAdmin tool computes exact what-if costs from atomic configurations and returns a valid configuration that Greedy(m, k) cannot improve by one index
proves: [correctness]
status: full
---

We use the notation of the page and the code. A workload $W$ is a list of weighted statements $Q$, each a select or an update on one table. A configuration $C$ is a set of indexes. $\mathrm{opt}(Q, C)$ is the cost that the optimizer model (`WhatIf.optimize`) gives to $Q$ when exactly the indexes of $C$ exist, and $\mathrm{Cost}(W, C) = \sum_{Q \in W} w_Q \, \mathrm{opt}(Q, C)$. The tool is asked for a configuration of at most $k$ indexes with a small cost. Finding the minimum is NP-hard (Piatetsky-Shapiro, 1983, and Comer, 1978), so the tool is a heuristic, and what we prove is that its costs are exact and its output is valid and locally best.

**Lemma 1 (atomic configurations).** For every statement $Q$ and configuration $C$, `query_cost(Q, C)` equals $\mathrm{opt}(Q, C)$.

*Proof.* For a select, the model costs a full scan and, for each index of $C$ on the table of $Q$ that it can use, one plan with that index, and returns the minimum. A plan uses one index, so its cost depends only on that index: $\mathrm{opt}(Q, \{i\})$ is the minimum of the scan and the plan with $i$. Hence $\mathrm{opt}(Q, C) = \min(\mathrm{opt}(Q, \emptyset), \min_{i \in C} \mathrm{opt}(Q, \{i\}))$, which is what L13 computes; an index that $Q$ cannot use gives the scan, so skipping it changes nothing. For an update, the model charges $1$ plus a fixed amount for each index on the table that holds a changed column, so $\mathrm{opt}(Q, C) - 1 = \sum_{i \in C} (\mathrm{opt}(Q, \{i\}) - 1)$, which is the sum the code takes. The cache returns the value of an earlier call with the same key, and the model has no state, so the cache does not change any value. $\square$

So the *atomic configurations* of a select in this model are $\emptyset$ and the single indexes, and of an update the single indexes. Lemma 1 is the property that the paper requires of atomic configurations: the cost in any configuration follows from the costs in its atomic subsets without a new optimizer call.

**Lemma 2 (number of what-if calls).** If $P$ is the set of all indexes that the tool considers (the final `pool`), the tool makes at most $|W| \, (|P| + 1)$ what-if calls.

*Proof.* Every call has a key $(Q, A)$ with $A = \emptyset$ or $A = \{i\}$, $i \in P$, and each key is computed once. $\square$

Without atomic configurations, each pair of a statement and a configuration that the search costs needs its own call. The tests check that this number (`len(tool.pairs)`) is more than three times the number of calls.

**Lemma 3 (Greedy(m, k)).** Let $S$ be a set of candidates and $G$ the result of `enumerate(W, S, k)`. Then:

1. $G \subseteq S$ and $|G| \le k$.
2. $\mathrm{Cost}(W, G) \le \mathrm{Cost}(W, D)$ for every $D \subseteq S$ with $|D| \le \min(m, k)$, and in particular for $D = \emptyset$.
3. If $|G| < k$, no single index of $S \setminus G$ lowers the cost: $\mathrm{Cost}(W, G \cup \{i\}) \ge \mathrm{Cost}(W, G)$ for all $i \in S \setminus G$.
4. If $m \ge k$, $G$ has the least cost among all subsets of $S$ with at most $k$ indexes.

*Proof.* L7 tries every subset of $S$ of size at most $\min(m, k)$ and keeps one of least cost, starting from $\emptyset$; this gives (2) for the start. Each step of L8 to L11 adds one index of $S$ and is taken only if it lowers the cost strictly, so the cost never rises, which keeps (2), and the size grows by one up to $k$, which gives (1). The loop ends at size $k$, or when L10 finds no index that lowers the cost, which is (3). If $m \ge k$, L7 is already the exhaustive search over all subsets of size at most $k$, and the loop cannot improve it without exceeding $k$, which is (4). The loop runs at most $k$ times, so the procedure ends. $\square$

**Theorem 1 (the tool).** `run` ends and returns a configuration of at most $k$ indexes, each in the pool of admissible indexes, whose cost is at most the cost with no index, and to which no single candidate can be added with a lower cost if it has fewer than $k$ indexes. Each candidate is an index of the best configuration that Greedy(m, k) finds for some single statement, or an index chosen in an earlier iteration.

*Proof.* There are `width` iterations. In each, the per-statement calls at L5 and the workload call at L6 are calls of `enumerate`, which end by Lemma 3. The candidates are the union of their results and of the earlier choice, so they lie in the pool. The final configuration is the result of L6 in the last iteration, so Lemma 3, parts (1) to (3), gives the claims, and Lemma 1 shows that the costs it compares are the optimizer's costs. $\square$

**What the tool does not guarantee.** The output need not be optimal, even among the indexes of the pool. Two ways it can miss are shown by the tests' search over random instances:

- *Candidate selection.* An index that is second best for each of two statements, but serves both, is not the best for either alone, so L5 does not make it a candidate.
- *Multi-column indexes.* MC-LEAD forms an index of width $j$ only from a chosen index of width $j - 1$. If no index on the leading column was chosen, no wider index with that leading column is formed.

The tests compare the tool with an exhaustive search over all configurations of at most $k$ indexes from all admissible indexes, and check that the tool is never better than the optimum (a check of the search and the costs), never worse than no index, and finds the optimum on at least 15 of 40 random instances. They also check Lemma 1 against the optimizer model on random configurations, part (4) of Lemma 3, and that more steps of the greedy loop never raise the cost.
