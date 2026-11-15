---
tag: 4TC48W
kind: algorithm
slug: twin-plant-diagnosability-test
name: Twin plant diagnosability test
aliases:
- verifier for diagnosability
area: control/discrete-event-and-hybrid-systems
level: research
summary: Tests diagnosability in polynomial time. It runs a faulty and a fault-free copy of the plant in step on the observable events and searches for a cycle where the copies never separate.
model: word-ram
complexity:
  vars: {n: the number of states of the plant, q: the number of events}
  time: {worst: O(n^2 q)}
  space: {extra: O(n^2 q)}
properties: {deterministic: true, exact: true, online: false}
history:
  year: 2001
  people: [Shengbing Jiang, Zhongdong Huang, Vigyan Chandra, Ratnesh Kumar, Tae-Sic Yoo, Stéphane Lafortune]
  note: "Jiang, Huang, Chandra and Kumar gave a polynomial test on a product of the plant with itself in 2001. Yoo and Lafortune gave the verifier automaton in 2002."
prereqs: [diagnosability, product-construction]
see_also: [diagnoser-automaton, diagnosability, product-construction, observable-language, cycle-detection, topological-sort, strongly-connected-components, breadth-first-search]
sources:
  - paper: doi:10.1109/9.940942
    title: "S. Jiang, Z. Huang, V. Chandra and R. Kumar, A polynomial algorithm for testing diagnosability of discrete-event systems, IEEE Transactions on Automatic Control 46(8), 2001, pages 1318 to 1321"
    locator: the product of the plant with itself and the test for ambiguous cycles; the abstract gives the order of the complexity
  - paper: doi:10.1109/TAC.2002.802763
    title: "T.-S. Yoo and S. Lafortune, Polynomial-time verification of diagnosability of partially observed discrete-event systems, IEEE Transactions on Automatic Control 47(9), 2002, pages 1491 to 1495"
    locator: the verifier automaton and its cycle condition
  - paper: doi:10.1109/9.412626
    title: "M. Sampath, R. Sengupta, S. Lafortune, K. Sinnamohideen and D. Teneketzis, Diagnosability of discrete-event systems, IEEE Transactions on Automatic Control 40(9), 1995, pages 1555 to 1575"
    locator: the definition of diagnosability and its assumptions
---

The twin plant test decides whether a fault of a partially observed [discrete-event system](/discrete-event-system/) is [diagnosable](/diagnosability/), in time polynomial in the size of the plant. It runs two copies of the plant side by side. The first copy may take the fault and remembers in a flag that it did. The second copy never takes the fault. The copies move alone on unobservable events and together on observable events, so they always show the same observation. A cycle of states where the flag is set is a way for a faulty run and a fault-free run to look the same forever, so the fault is not diagnosable. If there is no such cycle, it is. Jiang, Huang, Chandra and Kumar (2001) gave the first polynomial test of this kind, and Yoo and Lafortune (2002) gave the verifier automaton. The [diagnoser](/diagnoser-automaton/) of Sampath et al. answers the same question, but it can be exponentially large.

## In plain words

You want to know whether a hidden fault always shows itself after a while. Imagine two copies of the machine. One is allowed to break, and the other is not. You make them produce the same visible events, step by step, while each may also do hidden events on its own.

If the broken copy and the healthy copy can go on forever and still look the same, then an observer can never be sure that the fault happened, and the fault is not diagnosable. If every such game ends, because sooner or later the broken copy does something the healthy copy cannot match, then the fault is diagnosable. Both copies have only as many positions as the machine, so the pairs of positions are few, and the search is fast.

## The problem

The input is a deterministic plant $G = (X, \Sigma, \delta, x_0)$, the observable events $\Sigma_o$ and the set $\Sigma_F \subseteq \Sigma \setminus \Sigma_o$ of fault events of one type $F$. As in Sampath et al. (1995), $G$ has no cycle of unobservable events. The output is true if $F$ is [diagnosable](/diagnosability/): there is $N$ such that, for every string $s \in L(G)$ that ends with a fault of type $F$ and every continuation $t$ with $|t| \ge N$, every $w \in L(G)$ with $P(w) = P(st)$ contains a fault of type $F$. Here $P$ is the natural projection onto $\Sigma_o^*$. For several fault types, run the test once per type, and treat the other fault events as ordinary unobservable events.

## The algorithm

$G_N$ is $G$ without its fault transitions. A verifier state is a triple $(x, f, y)$: $x$ is the state of copy 1, $f$ is the flag "copy 1 has taken a fault", and $y$ is the state of copy 2.

```pseudo id=main
TWIN-PLANT(G, Σo, ΣF)
L1  G_N ← G without the transitions labeled by events of ΣF
L2  v0 ← (x0, false, x0);  states ← {v0};  queue ← [v0]
L3  while queue is not empty do
L4      (x, f, y) ← pop the front of queue
L5      for each unobservable e defined at x in G do add the edge to (δ(x, e), f or e ∈ ΣF, y)
L6      for each unobservable e defined at y in G_N do add the edge to (x, f, δ_N(y, e))
L7      for each observable e defined at x in G and at y in G_N do add the edge to (δ(x, e), f, δ_N(y, e))
L8      add each new target of lines L5 to L7 to states and to queue
L9  W ← the states with f = true
L10 return true if the graph restricted to W has no cycle, else false
```

Lines L2 to L8 are a [breadth-first search](/breadth-first-search/) of the [product](/product-construction/) of $G$ and $G_N$ that is synchronized only on observable events. Each path from $v_0$ is a pair of runs, of $G$ and of $G_N$, with the same projection, and the flag tells whether the first run has a fault. Line L10 runs Kahn's algorithm on $W$, as in [topological sort](/topological-sort/): it removes flagged states of in-degree 0 until none is left, and a cycle remains if and only if some state remains. The test of Yoo and Lafortune labels the states of both copies and looks for a cycle where the labels differ. The version here keeps copy 2 fault-free from the start, so one flag is enough.

## Example

The plant has states 0 to 5 and the transitions $0 \xrightarrow{a} 1$, $1 \xrightarrow{u} 2$, $2 \xrightarrow{b} 0$ (the normal cycle), $1 \xrightarrow{f} 3$ (the fault), $3 \xrightarrow{b} 4$, $4 \xrightarrow{a} 5$ and $5 \xrightarrow{b} 4$. The events $a$ and $b$ are observable, and $u$ and $f$ are not. The table lists the verifier states in the order of the search, with the flag written N or F. A label $(e, -)$ is a move of copy 1 alone, $(-, e)$ of copy 2 alone, and $(e, e)$ a joint move.

| order | state | line | edges |
|---|---|---|---|
| 1 | $(0, N, 0)$ | L7 | $(a, a) \to (1, N, 1)$ |
| 2 | $(1, N, 1)$ | L5, L6 | $(u, -) \to (2, N, 1)$; $(f, -) \to (3, F, 1)$; $(-, u) \to (1, N, 2)$ |
| 3 | $(2, N, 1)$ | L6 | $(-, u) \to (2, N, 2)$ |
| 4 | $(3, F, 1)$ | L6 | $(-, u) \to (3, F, 2)$ |
| 5 | $(1, N, 2)$ | L5 | $(u, -) \to (2, N, 2)$; $(f, -) \to (3, F, 2)$ |
| 6 | $(2, N, 2)$ | L7 | $(b, b) \to (0, N, 0)$ |
| 7 | $(3, F, 2)$ | L7 | $(b, b) \to (4, F, 0)$ |
| 8 | $(4, F, 0)$ | L7 | $(a, a) \to (5, F, 1)$ |
| 9 | $(5, F, 1)$ | L6 | $(-, u) \to (5, F, 2)$ |
| 10 | $(5, F, 2)$ | L7 | $(b, b) \to (4, F, 0)$ |

The verifier has 10 states and 13 edges. Line L9 gives the 5 flagged states $(3, F, 1)$, $(3, F, 2)$, $(4, F, 0)$, $(5, F, 1)$ and $(5, F, 2)$. Kahn's algorithm at line L10 removes $(3, F, 1)$ and then $(3, F, 2)$, and stops. The cycle $(4, F, 0) \to (5, F, 1) \to (5, F, 2) \to (4, F, 0)$ remains, so the fault is not diagnosable. The cycle gives a witness: copy 1 runs $afba(ba)^k$ and copy 2 runs $auba(uba)^k$. Both show $abab\cdots$, the first has the fault and the second has not, for every $k$.

If instead the plant ends with $3 \xrightarrow{b} 4$ and $4 \xrightarrow{c} 4$, with $c$ observable, the verifier has 8 states and 10 edges. The flagged state $(4, F, 0)$ has no edge, because copy 1 can only do $c$ and copy 2 can only do $a$. There is no flagged cycle, and the fault is diagnosable. The tests of the implementation check both plants, and compare the test with the [diagnoser](/diagnoser-automaton/) and with the test of Jiang et al. on 600 random plants.

## Correctness

Paths of the verifier from $v_0$ correspond to pairs $(s, s')$ with $s \in L(G)$, $s' \in L(G_N)$ and $P(s) = P(s')$, and the flag of the end state is set if and only if $s$ has a fault. The flag never goes back to false. If the flagged states have a cycle, follow a path to it and pump the cycle: this gives faulty strings with arbitrarily long continuations after the fault and a fault-free twin with the same projection. So $F$ is not diagnosable. The run of copy 1 on the cycle must be nonempty for this, and it is, because copy 2 alone has no cycle of unobservable events. If the flagged states have no cycle, every path inside $W$ has fewer than $|W|$ edges. A continuation $t$ after a fault, with a fault-free twin, gives a path in $W$ with at least $|t|$ edges, one for each event of copy 1. So $N = |W| \le n^2$ is a valid delay bound, and $F$ is diagnosable. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/) with hashing. Let $n = |X|$ and $q = |\Sigma|$.

- The verifier has at most $2 n^2$ states: $n$ choices for each copy and two values of the flag.
- Each state has at most $2q$ edges: lines L5 and L7 together take at most one edge per event of copy 1, and line L6 at most one per event of copy 2. So there are at most $4 n^2 q$ edges.
- Lines L2 to L8 and Kahn's algorithm at line L10 are linear in the size of the verifier.

The total is $O(n^2 q)$ time and space. This bound is derived on this page for the program above. The abstract of Jiang et al. (2001) says that their test is of fourth order in the number of states of the plant and linear in the number of failure types. Their test first builds a nondeterministic automaton over the observable events, which can have many more transitions than $G$, and then takes its product with itself. For $m$ fault types, the version here runs $m$ times, so it is also linear in $m$.

## Properties

- **Exact.** It decides diagnosability, under the assumption on unobservable cycles.
- **Polynomial.** Unlike the diagnoser, its size is at most quadratic in $n$.
- **Witness.** A flagged cycle, with a path to it, gives a faulty run and a fault-free run with the same projection, of any length. The implementation returns one.
- **Delay bound.** If the fault is diagnosable, the number of flagged states bounds the detection delay: $N = |W| \le n^2$ events after the fault.
- **Offline only.** It does not give an online detector. For that, use the [diagnoser](/diagnoser-automaton/).

## Variants and improvements

- **Jiang et al. (2001).** First replace $G$ by its observable reduction: a nondeterministic automaton over $\Sigma_o$ whose states are pairs (state, fault label) and whose transitions jump over unobservable runs. Then build the product of two copies, synchronized on all events, and look for a cycle of states where the two labels differ. The implementation has this test as a second function, and the tests check that it agrees.
- **Yoo and Lafortune (2002).** The verifier keeps the unobservable moves of both copies, as here, and labels both. It avoids the observable reduction, and so the extra transitions it can have.
- **Several fault types.** One flag per type gives $2^m$ copies of each pair. One run per type keeps the size at $2 n^2$.
- **Other properties.** A twin product of the same kind checks the [observability](/observable-language/) of a language, which also asks about two runs with the same observation.
- **Search for strongly connected components.** Instead of Kahn's algorithm, compute the [strongly connected components](/strongly-connected-components/) of $W$; a cycle exists if one has more than one state or a self-loop. Both are linear, as other [cycle detection](/cycle-detection/) methods are.

## When to use it

Use it when you need to know whether a plant is diagnosable, and the plant has many states. It is the method of choice for this offline question. If you also need an online detector, build the [diagnoser](/diagnoser-automaton/) for a small plant, or run it on the fly. Check first that the plant has no cycle of unobservable events.

## Pitfalls

- **Unobservable cycles (lines L6 and L10).** With a cycle of unobservable events, copy 2 can loop alone while copy 1 waits in a flagged state. That is a flagged cycle, and line L10 answers "not diagnosable" even when the fault is diagnosable. In the plant $0 \xrightarrow{f} 1$, $1 \xrightarrow{a} 1$, $0 \xrightarrow{u} 2$, $2 \xrightarrow{u} 2$, $2 \xrightarrow{b} 2$ with $a$ and $b$ observable, every run after the fault shows $a$, and no fault-free run does, so the fault is diagnosable. But copy 2 loops on $u$ at state 2 while copy 1 waits at state 1, and the test says no. A test of the implementation checks this case. Check the assumption first.
- **Letting copy 2 take the fault (line L1).** If copy 2 runs $G$ instead of $G_N$, the flag no longer means "faulty against fault-free". Two faulty runs then give flagged cycles, and the test reports diagnosable plants as not diagnosable.
- **Looking for a flagged state instead of a flagged cycle (line L10).** Every reachable fault gives a flagged state at once, since the other copy can always wait. Only a cycle shows that the ambiguity can last forever.
- **Synchronizing the unobservable events (lines L5 and L6).** If both copies had to make the same unobservable move, the verifier would miss fault-free twins that use other hidden events, such as $u$ against $f$ in the example, and it would answer "diagnosable" too often.

## Implementations

## History

Sampath, Sengupta, Lafortune, Sinnamohideen and Teneketzis defined diagnosability in 1995 and tested it with the diagnoser, which can be exponential in the number of plant states. Jiang, Huang, Chandra and Kumar showed in 2001, in the IEEE Transactions on Automatic Control, that a product of the plant with itself decides diagnosability in polynomial time. Yoo and Lafortune published the verifier in 2002 in the same journal. The name twin plant is common in the literature for this kind of product.

## References
