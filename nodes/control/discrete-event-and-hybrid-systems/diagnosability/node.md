---
tag: 8YQ5W6
kind: definition
slug: diagnosability
name: Diagnosability of discrete-event systems
aliases:
- failure diagnosability
- Sampath diagnosability
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: A system is diagnosable if every unobservable fault is detected with certainty, from the observable events alone, within a bounded number of events after it occurs.
prereqs: [discrete-event-system]
see_also: [diagnoser-automaton, twin-plant-diagnosability-test, observable-language, normal-language, consistency-based-diagnosis, state-estimation, hidden-markov-model]
sources:
  - paper: doi:10.1109/9.412626
    title: "M. Sampath, R. Sengupta, S. Lafortune, K. Sinnamohideen and D. Teneketzis, Diagnosability of discrete-event systems, IEEE Transactions on Automatic Control 40(9), 1995, pages 1555 to 1575"
    locator: the definition of diagnosability, the assumptions on the plant and the diagnoser test
  - paper: doi:10.1109/87.486338
    title: "M. Sampath, R. Sengupta, S. Lafortune, K. Sinnamohideen and D. C. Teneketzis, Failure diagnosis using discrete-event models, IEEE Transactions on Control Systems Technology 4(2), 1996, pages 105 to 124"
    locator: the application of the diagnoser to fault detection in physical systems
  - paper: doi:10.1109/9.940942
    title: "S. Jiang, Z. Huang, V. Chandra and R. Kumar, A polynomial algorithm for testing diagnosability of discrete-event systems, IEEE Transactions on Automatic Control 46(8), 2001, pages 1318 to 1321"
    locator: the polynomial test by a product of the plant with itself
  - paper: doi:10.1109/TAC.2002.802763
    title: "T.-S. Yoo and S. Lafortune, Polynomial-time verification of diagnosability of partially observed discrete-event systems, IEEE Transactions on Automatic Control 47(9), 2002, pages 1491 to 1495"
    locator: the verifier automaton
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 2, Languages and Automata (observers and diagnosers)
---

A [discrete-event system](/discrete-event-system/) is diagnosable if every fault that cannot be seen directly is still detected with certainty after a bounded number of further events, from the observable events alone. A fault such as "valve stuck closed" is an unobservable event: no sensor reports it. But it changes what the plant does next, and a diagnosable plant always shows the change within a fixed delay. Sampath, Sengupta, Lafortune, Sinnamohideen and Teneketzis defined the notion in 1995 and gave a test with the [diagnoser automaton](/diagnoser-automaton/). The [twin plant test](/twin-plant-diagnosability-test/) of Jiang, Huang, Chandra and Kumar (2001) and Yoo and Lafortune (2002) decides it in polynomial time. Diagnosability is a property of the model, checked offline. It is not the same problem as [consistency-based diagnosis](/consistency-based-diagnosis/) in AI, which takes one observation and computes the sets of faulty components that explain it.

## Definition

Let $G = (X, \Sigma, \delta, x_0)$ be a plant automaton with generated language $L = L(G)$. The events split into observable events $\Sigma_o$ and unobservable events $\Sigma_{uo}$, and $P$ is the natural projection onto $\Sigma_o^*$. The fault events form a set $\Sigma_f \subseteq \Sigma_{uo}$, split into fault types $\Sigma_{f_1}, \dots, \Sigma_{f_m}$. For a type $F = \Sigma_{f_i}$:

- $\Psi(F)$ is the set of strings of $L$ whose last event is in $F$;
- $L/s = \{t : st \in L\}$ is the set of continuations of $s$;
- a string $w$ contains $F$ if some event of $w$ is in $F$.

Sampath et al. assume:

1. $L$ is live: every reachable state has at least one outgoing transition;
2. $G$ has no cycle of unobservable events.

> $L$ is **diagnosable** with respect to $P$ and the fault types if for every type $F$ there is an integer $n_F$ such that for all $s \in \Psi(F)$ and all $t \in L/s$ with $|t| \ge n_F$:
> every $w \in L$ with $P(w) = P(st)$ contains $F$.

In words: $n_F$ events after a fault of type $F$, every string that the observer cannot tell apart from the true one has a fault of type $F$. So the observer knows that $F$ occurred. The second assumption makes the condition meaningful: without it, the plant could run unobservable events forever after the fault and the observer would see nothing. The first assumption makes every string extendable, so the plant does not stop before the delay has passed.

The delay $n_F$ counts all events, observable or not. Because there is no unobservable cycle, a delay in all events and a delay in observable events are equivalent up to a factor that depends only on $|X|$.

## Examples and non-examples

The plant $G_1$ has states 0 to 4, initial state 0, and transitions $0 \xrightarrow{a} 1$, $1 \xrightarrow{u} 2$, $2 \xrightarrow{b} 0$, $1 \xrightarrow{f} 3$, $3 \xrightarrow{b} 4$ and $4 \xrightarrow{c} 4$. The events $a$, $b$ and $c$ are observable, $u$ is unobservable, and $f$ is the only fault. The plant is live and has no unobservable cycle.

- **Diagnosable with delay 2.** After the fault in $af$, the only continuations are $b c^k$. With $t = b$, the observer sees $ab$, and the fault-free string $aub$ also gives $ab$. So one event is not enough. With $t = bc$, the observer sees $abc$. No fault-free string gives $abc$, because after $aub$ the plant is in state 0, where only $a$ is possible. So every string with projection $abc$ contains $f$. The same holds after every later fault, so $n_f = 2$ works and is the smallest value. The [diagnoser automaton](/diagnoser-automaton/) of $G_1$ shows this as a state $\{4F\}$ that is certain.
- **Not diagnosable.** Change the part after the fault to $3 \xrightarrow{b} 4$, $4 \xrightarrow{a} 5$ and $5 \xrightarrow{b} 4$. After $af$, the continuation $(ba)^k$ gives the observation $a(ba)^k$, and so does the fault-free string $(aub)^k a$. The observer is never sure, however long it waits. The [twin plant](/twin-plant-diagnosability-test/) finds this as a cycle in which one copy is faulty and the other is not.
- **Observable faults.** If a fault event were observable, it would be detected at once. The definition requires $\Sigma_f \subseteq \Sigma_{uo}$ to make the question nontrivial.
- **No fault-free twin.** If no fault-free string has the same projection as any string with a fault, then the fault is detected at the first observation after it occurs. This is the case when the fault leads to an observable event that the fault-free plant never produces.

## Related definitions

- **Diagnoser.** An automaton over $\Sigma_o$ whose states are sets of pairs (plant state, fault label). Sampath et al. show that $L$ is diagnosable if and only if the diagnoser has no indeterminate cycle. The diagnoser can have exponentially many states. See [diagnoser automaton](/diagnoser-automaton/).
- **Twin plant and verifier.** A product of the plant with itself, where both copies make the same observable moves. $L$ is diagnosable if and only if this product has no cycle in which one copy has seen the fault and the other has not. The test is polynomial in $|X|$. See [twin plant diagnosability test](/twin-plant-diagnosability-test/).
- **Observability of languages.** [Observability](/observable-language/) and [normality](/normal-language/) also compare strings with the same projection. Diagnosability asks that a faulty string and a fault-free string do not keep the same projection for long.
- **State estimation.** Online, a diagnoser keeps the set of states that agree with the observation, as in [state estimation](/state-estimation/). With probabilities on the transitions, the plant becomes a [hidden Markov model](/hidden-markov-model/), and diagnosability gets a stochastic form, where the fault must be detected with probability tending to one.
- **Consistency-based diagnosis.** [Consistency-based diagnosis](/consistency-based-diagnosis/) in AI works on a logical model of components and one set of observations. It returns the minimal sets of faulty components consistent with them. It does not ask whether a fault will always be detected.

## References
