---
tag: 8VN8F2
kind: algorithm
slug: diagnoser-automaton
name: Diagnoser automaton
aliases:
- Sampath diagnoser
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: Builds an automaton over the observable events whose states are sets of plant states with fault labels. It detects faults online and tests diagnosability by a search for indeterminate cycles.
model: word-ram
complexity:
  vars: {n: the number of states of the plant, m: the number of fault types, q: the number of observable events}
  time: {worst: O(2^(n 2^m) n^4 16^m q)}
  space: {extra: O(2^(n 2^m) n^4 16^m q)}
properties: {deterministic: true, exact: true, online: false}
history:
  year: 1995
  people: [Meera Sampath, Raja Sengupta, Stéphane Lafortune, Kasim Sinnamohideen, Demosthenis Teneketzis]
  note: "Sampath et al. defined diagnosability in 1995 and gave the diagnoser as the tool both to detect faults online and to decide diagnosability."
prereqs: [diagnosability, subset-construction]
see_also: [twin-plant-diagnosability-test, diagnosability, subset-construction, observable-language, state-estimation, topological-sort, cycle-detection, hidden-markov-model]
sources:
  - paper: doi:10.1109/9.412626
    title: "M. Sampath, R. Sengupta, S. Lafortune, K. Sinnamohideen and D. Teneketzis, Diagnosability of discrete-event systems, IEEE Transactions on Automatic Control 40(9), 1995, pages 1555 to 1575"
    locator: the construction of the diagnoser and the necessary and sufficient condition for diagnosability in terms of indeterminate cycles
  - paper: doi:10.1109/87.486338
    title: "M. Sampath, R. Sengupta, S. Lafortune, K. Sinnamohideen and D. C. Teneketzis, Failure diagnosis using discrete-event models, IEEE Transactions on Control Systems Technology 4(2), 1996, pages 105 to 124"
    locator: the use of the diagnoser for online fault detection
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 2, Languages and Automata (observers and diagnosers)
---

The diagnoser of a partially observed [discrete-event system](/discrete-event-system/) is a deterministic automaton that reads only the observable events. Each of its states is the set of all pairs (plant state, faults so far) that agree with what has been observed. A state whose pairs all carry a fault of type $F$ says "$F$ has certainly occurred". A state where some pairs carry $F$ and some do not says "uncertain". Online, the diagnoser runs next to the plant and reports a fault as soon as it is certain. Offline, Sampath, Sengupta, Lafortune, Sinnamohideen and Teneketzis (1995) used it to decide [diagnosability](/diagnosability/): the plant is diagnosable exactly when the diagnoser has no indeterminate cycle, a cycle along which a faulty and a fault-free explanation stay together forever. The construction is a [subset construction](/subset-construction/) over the plant states with fault labels, so it can have exponentially many states. The [twin plant test](/twin-plant-diagnosability-test/) answers the offline question in polynomial time, but it does not give an online detector.

## In plain words

You watch a machine, but some of its events are hidden from you, and a fault is one of the hidden events. After each event you see, you write down every place the machine could be in now, and for each place whether a fault has happened on the way there. If every entry says "fault", you raise the alarm. If none does, all is well. If some do and some do not, you wait.

Do this once for every sequence of observations you could ever see, and you get a finite machine: the diagnoser. To learn whether you will always reach a verdict, look for a loop in which a "fault" entry and a "no fault" entry can follow each other forever. If there is such a loop, some faults are never found. If there is none, every fault is found after a bounded wait.

## The problem

The input is a deterministic plant $G = (X, \Sigma, \delta, x_0)$, the observable events $\Sigma_o$, and a map from each fault event to its fault type. Fault events are unobservable, and there are $m$ types. A label $\ell$ is a set of fault types, and $\ell(s)$ is the set of types of the fault events in $s$. The natural projection $P$ erases the unobservable events.

The first output is the diagnoser: the reachable part of the deterministic automaton over $\Sigma_o$ whose state after the observed word $y$ is

$$Q(y) = \{(\delta(x_0, s), \ell(s)) : s \in L(G),\ P(s) = y,\ s = \varepsilon \text{ or } s \text{ ends with an observable event}\}.$$

The second output, for a chosen type $F$, is the answer to: is $F$ [diagnosable](/diagnosability/)? The test assumes, as Sampath et al. do, that $G$ has no cycle of unobservable events.

For a pair $p = (x, \ell)$ and an event $\sigma \in \Sigma_o$, MOVES$(p)[\sigma]$ is the set of pairs $(\delta(x, u\sigma), \ell \cup \ell(u\sigma))$ over all unobservable strings $u$ such that $u\sigma$ is defined at $x$. It is computed by a search over pairs.

## The algorithm

```pseudo id=main
DIAGNOSER(G, Σo, faults)
L1  q0 ← {(x0, ∅)}
L2  states ← {q0};  queue ← [q0]
L3  while queue is not empty do
L4      q ← pop the front of queue
L5      for each σ in Σo do
L6          r ← ∅
L7          for each pair p in q do r ← r ∪ MOVES(p)[σ]
L8          if r ≠ ∅ then δd(q, σ) ← r; if r is not in states then add r to states and to queue
L9  return (q0, states, δd)

DIAGNOSABLE(G, Σo, faults, F)
L10 D ← DIAGNOSER(G, Σo, faults)
L11 T ← the triples (q, a, b) with q a state of D, a and b pairs in q, F in the label of a and F not in the label of b
L12 for each (q, a, b) in T, σ in Σo with δd(q, σ) defined, a' in MOVES(a)[σ], b' in MOVES(b)[σ] with F not in the label of b' do add the edge (q, a, b) → (δd(q, σ), a', b')
L13 return true if the graph on T has no cycle, else false
```

Lines L1 to L9 are a breadth-first [subset construction](/subset-construction/) over pairs. Line L7 follows the unobservable events, collects the fault types they carry into the label, and stops at the next observable event $\sigma$. So a diagnoser state lists the plant states that are entered by an observable event, not those in the middle of an unobservable run. Line L8 keeps only nonempty sets: an observation that the plant cannot produce has no transition.

Lines L10 to L13 are the test. A triple $(q, a, b)$ says that, after the same observation, a faulty explanation $a$ and a fault-free explanation $b$ are both possible. An edge of line L12 extends both explanations by the same observable event, and keeps the second one fault-free. A cycle of triples is an indeterminate cycle: two explanations, one with the fault and one without, that can go on forever with the same observation. Line L13 uses Kahn's algorithm, as in [topological sort](/topological-sort/): remove nodes with in-degree 0 until none is left, and report a cycle if some node remains.

## Example

The plant has states 0 to 4, initial state 0, and transitions $0 \xrightarrow{a} 1$, $1 \xrightarrow{u} 2$, $2 \xrightarrow{b} 0$, $1 \xrightarrow{f} 3$, $3 \xrightarrow{b} 4$ and $4 \xrightarrow{c} 4$. The events $a$, $b$ and $c$ are observable, and $f$ is the fault, of type $F$. A pair $(x, \ell)$ is written $xN$ if the label is empty and $xF$ otherwise. The table shows lines L4 to L8, with the events in the order $a$, $b$, $c$, and only the events where $r$ is not empty.

| step | $q$ at L4 | $\sigma$ at L5 | $r$ at L7 | line L8 | verdict on $r$ |
|---|---|---|---|---|---|
| 1 | $\{0N\}$ | $a$ | $\{1N\}$ | new state | normal |
| 2 | $\{1N\}$ | $b$ | $\{0N, 4F\}$ | new state | uncertain |
| 3 | $\{0N, 4F\}$ | $a$ | $\{1N\}$ | known | normal |
| 3 | $\{0N, 4F\}$ | $c$ | $\{4F\}$ | new state | $F$ certain |
| 4 | $\{4F\}$ | $c$ | $\{4F\}$ | known | $F$ certain |

At step 2, MOVES$((1, \emptyset))[b]$ follows $u$ to $2N$ and then $b$ to $0N$, and it follows $f$ to $3F$ and then $b$ to $4F$. The diagnoser has 4 states and 5 transitions. Online, after the observation $ab$ it is uncertain, and after $abc$ it reports the fault.

For the test, line L11 finds one triple, $(\{0N, 4F\}, 4F, 0N)$. Line L12 adds no edge from it: on $a$, the pair $4F$ has no move, and on $c$, the pair $0N$ has none. The graph has no cycle, so $F$ is diagnosable.

Now change the plant after the fault to $3 \xrightarrow{b} 4$, $4 \xrightarrow{a} 5$ and $5 \xrightarrow{b} 4$, with $a$ and $b$ observable. The diagnoser is $\{0N\} \xrightarrow{a} \{1N\} \xrightarrow{b} \{0N, 4F\} \xrightarrow{a} \{1N, 5F\} \xrightarrow{b} \{0N, 4F\}$. The triples $(\{0N, 4F\}, 4F, 0N)$ and $(\{1N, 5F\}, 5F, 1N)$ form a cycle, so $F$ is not diagnosable: the faulty run $af(ba)^k$ and the normal run $(aub)^k a$ look the same forever. The tests of the implementation check both plants and compare the diagnoser states with a brute force enumeration of strings.

## Correctness

By induction on the observed word, the state that lines L1 to L9 reach on $y$ is exactly $Q(y)$: line L7 extends every explanation of $y$ by an unobservable run and the event $\sigma$, and every explanation of $y\sigma$ arises this way. There are at most $2^{n 2^m}$ sets of pairs, so the construction stops.

For the test: a cycle of triples gives, by the meaning of the states, a faulty string and a fault-free string with the same projection that can both be pumped around the cycle. So the delay after the fault is unbounded and $F$ is not diagnosable. Conversely, if $F$ is not diagnosable, there are arbitrarily long continuations after a fault with a fault-free twin. Because there is no unobservable cycle, a long continuation has many observable events, so it gives a long path of triples, and a path longer than the number of triples repeats one. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/) with hashing. Let $n = |X|$, $m$ the number of fault types and $q = |\Sigma_o|$. There are $n 2^m$ pairs.

- The diagnoser has at most $D \le 2^{n 2^m}$ states. With MOVES cached per pair, one transition at lines L6 and L7 costs $O(n^2 4^m)$ set operations, so lines L1 to L9 take $O(D\,q\,n^2 4^m)$ time.
- Line L11 makes at most $D\,n^2 4^m$ triples, and line L12 gives each at most $q\,n^2 4^m$ edges. Kahn's algorithm is linear in the size of this graph. So lines L10 to L13 take $O(D\,q\,n^4 16^m)$ time and space.

With $D \le 2^{n 2^m}$ this is the bound in the front matter. The bound on $D$ is the bound of the subset construction. Observers of automata can be exponential in $n$, so this growth does occur. In practice, $m$ is small, but $D$ can still grow exponentially in $n$. Online, a precomputed diagnoser takes $O(1)$ time per observed event. Without precomputation, one step of lines L6 and L7 on the current state takes $O(n^2 4^m)$ set operations for the observed $\sigma$, and memory for one state.

## Properties

- **Exact.** The diagnoser state is the exact set of explanations, not an approximation.
- **Deterministic.** The diagnoser is deterministic, even though the plant with its unobservable events is not, seen through the projection.
- **Online use.** It reports a fault of type $F$ at the first observation after which every explanation carries $F$. No observer that uses only the observations can report it earlier without the risk of a false alarm.
- **Several fault types at once.** One diagnoser serves all $m$ types. The test of lines L10 to L13 runs once per type.
- **Exponential size.** Its size is the main cost. The diagnosability test alone does not need it; see the [twin plant](/twin-plant-diagnosability-test/).

## Variants and improvements

- **Twin plant and verifier.** Jiang, Huang, Chandra and Kumar (2001) and Yoo and Lafortune (2002) test diagnosability without the diagnoser, on a product of the plant with itself, in polynomial time. See [twin plant diagnosability test](/twin-plant-diagnosability-test/).
- **On-the-fly diagnoser.** Keep only the current state and compute the next one when an event is observed. This avoids the exponential precomputation, at the cost of the work of line L7 at each step.
- **Decentralized diagnosis.** Several local diagnosers, each with its own observable events, report to a coordinator. Diagnosability then becomes a joint condition on all of them.
- **Stochastic diagnosis.** With probabilities on the transitions, the state becomes a probability distribution over pairs, as in the forward algorithm of a [hidden Markov model](/hidden-markov-model/), and a fault is reported when its probability passes a threshold.
- **Observer.** Without fault labels, the same construction is the observer of the plant, used for [state estimation](/state-estimation/) and for checking [observability](/observable-language/) properties.

## When to use it

Use the diagnoser when you need an online fault detector and the plant is small enough that the set of explanations stays manageable. It also gives the offline verdict and a readable reason for it. If you only need to know whether the plant is diagnosable, use the [twin plant test](/twin-plant-diagnosability-test/), which is polynomial. If the plant is large, run the diagnoser on the fly instead of building it in advance.

## Pitfalls

- **Testing for a cycle of uncertain states instead of triples (line L11).** A cycle of uncertain diagnoser states does not prove that the fault is not diagnosable. In the plant $1 \xrightarrow{a} 1$, $1 \xrightarrow{f} 5$, $5 \xrightarrow{a} 2$, $2 \xrightarrow{b} 6$, $6 \xrightarrow{b} 6$ with $a$ and $b$ observable, the diagnoser state $\{1N, 2F\}$ has an $a$ self-loop and is uncertain. But the fault is diagnosable: the faulty explanation $2F$ cannot follow $a$, so it does not stay on that loop, and the first $b$ reveals the fault. The triples of line L11 track which explanation stays on the cycle, and there the graph has no cycle. The tests check this plant.
- **Cutting the unobservable runs short at line L7.** MOVES must follow unobservable runs of any length before the observable event, and add the fault types of the whole run to the label. If it follows at most one unobservable event, it loses the explanations where two hidden events come in a row, such as a fault and then another hidden event. If it does not record the fault types along the run, every label stays empty and the diagnoser never reports a fault.
- **Letting the fault-free explanation become faulty at line L12.** An edge must keep $F$ out of the label of $b'$. If $b$ may pick up a fault, two faulty explanations can form a cycle, and the test says "not diagnosable" for a diagnosable plant.
- **Unobservable cycles (line L13).** The equivalence needs a plant without a cycle of unobservable events. In the plant $0 \xrightarrow{b} 0$, $0 \xrightarrow{f} 1$, $1 \xrightarrow{u} 1$ with only $b$ observable, the plant can loop on $u$ forever after the fault and no observation ever comes, so the fault is not diagnosable. But the state $1F$ is never entered by an observable event, so it is in no diagnoser state, line L11 finds no triple, and line L13 answers "diagnosable". Check the assumption first, for example with a cycle search on the unobservable transitions.
- **The size of the diagnoser.** Lines L1 to L9 can produce exponentially many states. Do not build the diagnoser only to answer the offline question.

## Implementations

## History

Sampath, Sengupta, Lafortune, Sinnamohideen and Teneketzis introduced diagnosability and the diagnoser in the IEEE Transactions on Automatic Control in 1995, with the condition that the diagnoser has no indeterminate cycle. In 1996 the same group described the use of the diagnoser for fault detection in physical systems in the IEEE Transactions on Control Systems Technology. Because the diagnoser can be exponential, Jiang, Huang, Chandra and Kumar (2001) and Yoo and Lafortune (2002) gave polynomial tests on a product of the plant with itself. The diagnoser stays the standard online detector.

## References
