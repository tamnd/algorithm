---
tag: DJN991
kind: model
slug: dbsp
name: DBSP
aliases:
- DBSP incremental computation
area: databases/stream-and-incremental-processing
level: research
summary: "A model of incremental computation over streams of changes to Z-sets, with an algorithm that turns any query into an incremental circuit."
prereqs: [delta-rules, incremental-view-maintenance]
see_also: [delta-rules, higher-order-ivm, differential-dataflow, timely-dataflow, incremental-view-maintenance, semi-naive-evaluation, datalog, event-time-watermark]
sources:
  - paper: doi:10.14778/3587136.3587137
    title: "Mihai Budiu, Tej Chajed, Frank McSherry, Leonid Ryzhyk and Val Tannen, DBSP: automatic incremental view maintenance for rich query languages, PVLDB 16(7), 2023, pages 1601 to 1614"
    locator: "Definitions 2.15 and 2.17 (D and I), Theorem 2.20 (inversion), Definition 3.1 and Proposition 3.2 (incremental version and chain rule), Theorems 3.3 and 3.4 (linear and bilinear operators), Section 4.1, Definition 4.3, Propositions 4.4, 4.5 and 4.7 (Z-sets, distinct), Algorithm 4.6, Algorithm 5.3 and Theorem 5.4 (recursion), Section 6 (nested streams)"
  - paper: arxiv:2203.16684
    title: "Mihai Budiu, Tej Chajed, Frank McSherry, Leonid Ryzhyk and Val Tannen, DBSP: automatic incremental view maintenance for rich query languages, extended version"
    locator: the full proofs and the further operators (the numbering of the PVLDB version is used on this page)
  - paper: "Frank McSherry, Derek G. Murray, Rebecca Isaacs and Michael Isard, Differential dataflow, Proceedings of CIDR 2013"
    title: Differential dataflow
    locator: "the model that DBSP simplifies, with differences indexed by partially ordered times"
---

DBSP is a model of computation over streams, in which each value of a stream is a change to a database, and a database is a Z-set: a function from tuples to integer weights. It defines the incremental version of any stream operator $Q$ as $Q^\Delta = D \circ Q \circ I$, where $I$ sums the changes and $D$ takes differences, and proves rules that build $Q^\Delta$ from the incremental versions of its parts. Its rules for linear and bilinear operators are the [delta rules](/delta-rules/) of relational algebra. Unlike [higher-order IVM](/higher-order-ivm/), it stays first order and keeps the integrated inputs as state, and it is a simpler, synchronous cousin of [differential dataflow](/differential-dataflow/) that uses nested streams in place of partially ordered times.

## The machine

**Groups and streams.** Values come from a commutative group $A$, with $+$, $0$ and $-$. A *stream* over $A$ is a function $s : \mathbb{N} \to A$, where $\mathbb{N}$ is logical time: one step per transaction or batch. Streams over $A$ form a group with pointwise $+$. An *operator* maps streams to streams. It is *causal* if its output at time $t$ depends only on the inputs at times up to $t$, and *strict* if only on the inputs before $t$.

**Basic operators.**

- *Lifting*: for a function $f : A \to B$, the operator $\uparrow f$ applies $f$ at each time, $(\uparrow f)(s)[t] = f(s[t])$.
- *Delay*: $z^{-1}(s)[0] = 0$ and $z^{-1}(s)[t] = s[t - 1]$. It is strict.
- *Integration* (Definition 2.17): $I(s)[t] = \sum_{i \le t} s[i]$.
- *Differentiation* (Definition 2.15): $D(s)[t] = s[t] - s[t - 1]$, with $s[-1] = 0$.

A *circuit* is a graph of operators. A cycle must pass through a strict operator such as $z^{-1}$; then the circuit has a unique solution, built time step by time step. $I$ is the circuit $I(s) = s + z^{-1}(I(s))$.

**Incremental versions.** For an operator $Q$, its *incremental version* (Definition 3.1) is

$$Q^\Delta = D \circ Q \circ I.$$

If a stream $s$ is the sequence of changes to an input, then $I(s)$ is the sequence of input states, $Q(I(s))$ the sequence of output states, and $Q^\Delta(s)$ the sequence of output changes. So $Q^\Delta$ is incremental view maintenance for the query $Q$, stated as an operator.

**Z-sets** (Section 4.1). A Z-set over a domain $U$ is a function $m : U \to \mathbb{Z}$ with finite support. Z-sets form a commutative group. A Z-set with only positive weights is a bag. A set is a Z-set with weights 0 and 1, and distinct maps a Z-set to a set: $\mathrm{distinct}(m)[x] = 1$ if $m[x] > 0$ and 0 otherwise (Definition 4.3). The relational operators become Z-set operators: filter and projection are linear, union is $+$, difference is $a + (-b)$ followed by distinct when set semantics is wanted, and the Cartesian product and the join are bilinear, with weights that multiply.

**From a query to an incremental circuit** (Algorithm 4.6). Write the query as a circuit of Z-set operators, remove the distinct operators that the rules of Propositions 4.4 and 4.5 show to be redundant, lift the circuit to streams, wrap it as $D \circ Q \circ I$, and use the chain rule to replace each operator by its incremental version.

**Recursion** (Section 5). A recursive query, such as a [Datalog](/datalog/) program, is a fixed point. Algorithm 5.3 computes it with a circuit that runs on an inner stream: an operator $\delta_0$ turns a value into a stream that holds it at time 0 and 0 later, a feedback loop with $z^{-1}$ applies the rules once per inner step, and an operator $\int$ sums an inner stream that is 0 after finitely many steps. Theorem 5.4 shows that the circuit computes the fixed point of the recursive query. To maintain a recursive query over changing inputs, Section 6 uses *nested streams*, streams whose values are streams: the outer time counts updates and the inner time counts iterations, and $D$ and $I$ act on the outer time.

**Example.** A join $R \bowtie S$ gets three steps of changes. $Q^\Delta$ outputs, at each step, the change of the join; the state is the integrated inputs $I(\Delta R)$ and $I(\Delta S)$.

| $t$ | $\Delta R[t]$ | $\Delta S[t]$ | output change $(R \bowtie S)^\Delta[t]$ | distinct of $\pi_B(R)$, change |
|---|---|---|---|---|
| 0 | $(1, 10)$ +1, $(2, 10)$ +1 | $(10, x)$ +1 | $(1, 10, x)$ +1, $(2, 10, x)$ +1 | $10$ +1 |
| 1 | $(3, 20)$ +1 | $(20, y)$ +1 | $(3, 20, y)$ +1 | $20$ +1 |
| 2 | $(1, 10)$ -1, $(4, 20)$ +1 | $(20, y)$ -1, $(20, z)$ +1 | $(1, 10, x)$ -1, $(3, 20, y)$ -1, $(3, 20, z)$ +1, $(4, 20, z)$ +1 | none |

At $t = 2$ the term $\Delta R \bowtie \Delta S$ gives $(4, 20, y)$ weight -1, and $\Delta R \bowtie z^{-1}(I(\Delta S))$ gives it +1, so it cancels. The weights of $B$ in $\pi_B(R)$ go from 2 and 1 to 1 and 2, both still positive, so the incremental distinct emits nothing.

## What it counts

- **State.** The model makes state explicit: each $z^{-1}$ holds one value. $I$ holds the current integrated value of its input, so the incremental join holds both integrated inputs, and the incremental distinct holds its integrated input. Linear operators hold nothing.
- **Work per step.** The cost of a step is the work of the incremental circuit on the changes of that step. A linear operator costs $O(1)$ per changed tuple in the worst case. A join with a hash index on each integrated input costs expected $O(1)$ per changed tuple plus the number of matches, which can be the size of the other input in the worst case. Distinct, with a hash map of weights, costs expected $O(1)$ per changed tuple. These bounds hold for each step, not amortized.
- **Memory.** The sum of the sizes of the integrated inputs of the join and distinct operators, each counted as the number of tuples with nonzero weight.
- **Inner steps.** For recursive queries, the number of inner iterations of each outer step also counts. The incremental recursive circuit does work only for the tuples whose derivations change.

## Relation to other models

- **Delta rules and IVM.** Theorems 3.3 and 3.4 are the [delta rules](/delta-rules/) of selection, projection, union and join, written for streams, with $z^{-1}(I(\cdot))$ in the role of the old value. The incremental distinct of Proposition 4.7 is the rule that compares the old and new weight of each changed tuple.
- **Higher-order IVM.** [Higher-order IVM](/higher-order-ivm/) also uses a ring of integer weights, but it maintains the delta query itself and stores maps of partial results. DBSP stores the integrated inputs of each nonlinear operator and evaluates the first-order delta.
- **Differential dataflow.** [Differential dataflow](/differential-dataflow/) indexes changes by times in a partial order, such as pairs of an epoch and an iteration, and compacts its state over a frontier. DBSP gets the two dimensions of a recursive query from nested streams, with one total order per level, which makes the proofs simpler.
- **Timely dataflow.** A DBSP circuit is synchronous: every operator takes one step per clock tick. [Timely dataflow](/timely-dataflow/) runs operators asynchronously and needs progress tracking to know when a time is complete.
- **Semi-naive evaluation.** Incrementalizing the inner loop of the recursion circuit gives [semi-naive evaluation](/semi-naive-evaluation/): each iteration joins only the newly derived tuples.
- **Signal processing.** Streams over a group, $z^{-1}$, and linear time-invariant operators come from the theory of discrete-time signals, and $D$ and $I$ are the difference and the running sum of [finite differences](/finite-differences/).
- **Late data.** The model has only logical time. A late tuple is a change in the step in which it arrives, and the output changes retract and replace earlier answers, with negative weights. Event time, and the decision to drop state for windows that are closed, need an [event-time watermark](/event-time-watermark/) outside the model.

## Known results in the model

- **Inversion** (Theorem 2.20). $I$ and $D$ are inverses: $D(I(s)) = I(D(s)) = s$. So the stream of states and the stream of changes carry the same information.
- **Properties of $Q^\Delta$** (Proposition 3.2). Among them is the chain rule $(Q_1 \circ Q_2)^\Delta = Q_1^\Delta \circ Q_2^\Delta$, which lets each operator be replaced on its own. Since $I$, $D$ and $z^{-1}$ are linear and time-invariant, each is its own incremental version by the next result.
- **Linear operators** (Theorem 3.3). If $Q$ is linear and time-invariant, $Q^\Delta = Q$. Lifted filter, projection and union are of this kind.
- **Bilinear operators** (Theorem 3.4). If $\times$ is bilinear, $(a \times b)^\Delta = a \times b + z^{-1}(I(a)) \times b + a \times z^{-1}(I(b))$. This is the three-term join rule.
- **Distinct** (Propositions 4.4, 4.5 and 4.7). Propositions 4.4 and 4.5 give rules that remove distinct operators from the inside of a query, so that a query needs few of them. The incremental version $H$ looks only at the changed tuples: a tuple is emitted with $+1$ when its weight goes from at most 0 to positive, and with $-1$ when it goes from positive to at most 0.
- **Any query** (Algorithm 4.6). Every query built from these operators, which include the relational algebra, has an incremental circuit that the algorithm builds mechanically.
- **Recursion** (Algorithm 5.3, Theorem 5.4, and Section 6). Recursive queries, such as Datalog programs, have circuits that compute their fixed points, and the same construction on nested streams gives incremental circuits for them.

## References
