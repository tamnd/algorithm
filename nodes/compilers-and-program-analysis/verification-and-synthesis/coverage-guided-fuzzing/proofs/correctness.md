---
title: The invariants of coverage-guided fuzzing, and why they give no completeness
proves: [correctness]
status: full
---

**Setting.** $P$ is a program of the toy IR with $k$ integer parameters and only constants, copies, binary operations and the terminators jump, br and ret. $G$ is its control flow graph with the edge set $E_G$, and $E = |E_G|$. For an input $x$, the run of $P$ on $x$ with fuel $F$ is a function of $x$ alone: the interpreter has no other state. EXEC returns its outcome kind (ret, trap or fuel), its step count and its coverage $\mathrm{cov}(x)$, the set of pairs $(e, \beta(n_e))$ for each edge $e$ that the run took $n_e \ge 1$ times, where $\beta$ is the bucket function with 8 values.

The state of the fuzzer is the queue $\mathcal{Q} = (q_0, q_1, \dots)$, the crash list $\mathcal{C}$, the virgin map $V$ and the crash map $V_C$. Let $s$ be the number of seeds.

## Lemma 1: coverage names real edges

**Claim.** For every input $x$, every pair of $\mathrm{cov}(x)$ is $(e, b)$ with $e \in E_G$ and $b \in \{1, 2, 3, 4, 8, 16, 32, 128\}$.

**Proof.** EXEC increments the counter of $(u, v)$ only when the terminator of $u$ moves the run to $v$, which is a jump to $v$ or a br with $v$ as one target; both make $(u, v)$ an edge of $G$. Each counter is at least 1 once it exists, and $\beta$ maps every $n \ge 1$ to one of the 8 values. $\square$

## Lemma 2: the state invariants

**Claim.** After line L1, and after every later run on lines L7 to L10, the following hold.

- (I1) Every entry $q$ of $\mathcal{Q}$ stores $\mathrm{cov}(q.\mathit{args})$ and the step count of its run, and every entry after the first $s$ comes from a run of kind ret.
- (I2) $V = \bigcup_{q \in \mathcal{Q}} \mathrm{cov}(q.\mathit{args})$.
- (I3) For each $i \ge s$, $\mathrm{cov}(q_i) \not\subseteq \bigcup_{j < i} \mathrm{cov}(q_j)$.
- (I4) Every $x \in \mathcal{C}$ traps, $V_C = \bigcup_{x \in \mathcal{C}} \mathrm{cov}(x)$, and each crash after the first has a pair not in the union of the coverage of the crashes before it.

**Proof.** Induction over the runs. Line L1 runs each seed once, appends it with its own coverage and steps, and adds its coverage to $V$; $\mathcal{C}$ and $V_C$ are empty. So (I1) to (I4) hold, with (I3) and (I4) empty.

A later run of $x$ on line L7 computes $\mathrm{cov}(x)$, since the run is a function of $x$. There are three cases.

- Kind trap. If $\mathcal{C}$ is empty or $\mathrm{cov}(x) \not\subseteq V_C$, then $x$ is appended to $\mathcal{C}$ and $\mathrm{cov}(x)$ is added to $V_C$. By (I4) for the old state, $V_C$ was the union for the old crashes, so the new pair is new among all earlier crashes, and $V_C$ is again the union. $\mathcal{Q}$ and $V$ do not change.
- Kind ret, with $\mathrm{cov}(x) \not\subseteq V$. Then $x$ is appended as $q_i$ with its coverage and steps, and $V \leftarrow V \cup \mathrm{cov}(x)$. By (I2), the old $V$ is $\bigcup_{j < i} \mathrm{cov}(q_j)$, so (I3) holds for $i$, and (I2) holds for the new state. (I1) holds because the kind is ret.
- Otherwise nothing changes. $\square$

## Lemma 3: the favored set covers the queue

**Claim.** For every queue, the set $\Phi$ returned by CULL satisfies $\bigcup_{i \in \Phi} \mathrm{edges}(q_i) = \bigcup_{i} \mathrm{edges}(q_i)$, where $\mathrm{edges}(q)$ is the set of edges of $\mathrm{cov}(q)$.

**Proof.** Line L11 defines $\mathrm{best}[e]$ exactly for the edges $e$ of the right side, and $\mathrm{best}[e]$ is an entry that covers $e$. Line L13 visits each such $e$. If $e$ is already in *covered*, some favored entry covers it. Otherwise $\mathrm{best}[e]$ is added to $\Phi$ and its edges, $e$ among them, to *covered*. So at the end every edge of the right side is covered by a favored entry, and *covered* contains only edges of favored entries, which gives the other inclusion. $\square$

## Theorem

**Claim.** At every point of a run of FUZZ:

1. every queue entry and every crash replays to the stored coverage and outcome, and every crash traps;
2. the virgin map is the union of the coverage of the queue, and each entry after the seeds added a new pair when it was added;
3. the favored set covers every edge covered by the queue;
4. every covered edge is an edge of $G$, and $|\mathcal{Q}| \le s + 8E$; and
5. the number of runs is at most $\max(N, s)$; FUZZ stops surely when some queue entry covers an edge, and with probability 1 otherwise.

**Proof.** Items 1 and 2 are (I1) to (I4), with the determinism of the run. Item 3 is Lemma 3. For item 4, Lemma 1 bounds the pairs: there are at most $8E$ possible pairs. By (I3), each entry after the seeds adds a pair that no earlier entry had, so the non-seed entries add distinct new pairs, at most $8E$ of them. For item 5, line L1 runs the $s$ seeds, and every later run first tests the budget and returns when it is used, so there are at most $\max(N, s)$ runs. The queue is finite by item 4, so each walk on line L3 has finitely many visits. A visit that is not skipped makes at least one run or returns. If some entry covers an edge, the favored set is not empty by Lemma 3, and a favored entry is never skipped, so each walk makes a run, and after at most $N$ walks the budget is used. If no entry covers an edge, every entry is skipped with probability 0.9 on each visit, and a visit that is not skipped comes with probability 1. $\square$

## What is not claimed

The theorem is about the state of the fuzzer, not about the program. It does not say that an edge, a path or a trap reachable by some input is found within the budget, or with any budget.

- Reachability of an edge or a trap is undecidable for programs with loops over unbounded integers, by Rice's theorem, so no procedure can promise to find every reachable one and stop.
- Even over a finite box of inputs, where the question is decidable by enumeration, the fuzzer samples. For the example of the page, an input reaches the trap only if it equals $(17, 21, 100)$. Changing 100 to 99 leaves the deterministic stage unable to make the third value from 0, and every havoc run then reaches the trap with some probability below 1, so no fixed number of runs guarantees the trap.
- Coverage pairs abstract the run. Two runs with the same pairs can follow different paths, so "no new pair" does not mean "no new behavior", and a full set of pairs does not mean that every path was run.

The tests of the page check items 1 to 4 on fixed-seed runs, and nothing else.
