---
tag: X53J8N
kind: problem
slug: coverability
name: Coverability problem
aliases:
- Petri net coverability
- Control-state reachability
area: logic-and-constraints/model-checking
level: research
summary: Decide whether a Petri net can reach a marking that is at least a given marking in each place. Decidable by the Karp-Miller tree and EXPSPACE-complete.
prereqs: [petri-net]
see_also: [karp-miller-tree, petri-net-reachability-decidability, reachability-problem, safety-property, expspace, savitch-theorem, state-explosion-problem]
sources:
  - paper: doi:10.1016/S0022-0000(69)80011-5
    title: Richard M. Karp and Raymond E. Miller, Parallel program schemata, Journal of Computer and System Sciences 3(2), 1969, pages 147 to 195
    locator: the coverability tree, which decides coverability and boundedness
  - paper: doi:10.1016/0304-3975(78)90036-1
    title: Charles Rackoff, The covering and boundedness problems for vector addition systems, Theoretical Computer Science 6(2), 1978, pages 223 to 231
    locator: the doubly exponential bound on the length of a shortest covering sequence, and the exponential space upper bound for coverability and boundedness
  - paper: "Richard J. Lipton, The reachability problem requires exponential space, Research Report 62, Department of Computer Science, Yale University, 1976"
    title: The reachability problem requires exponential space
    locator: the simulation of counters bounded by a doubly exponential value, which gives the exponential space lower bound for coverability
  - paper: "Parosh Aziz Abdulla, Kārlis Čerāns, Bengt Jonsson and Yih-Kuen Tsay, General decidability theorems for infinite-state systems, 11th IEEE Symposium on Logic in Computer Science (LICS 1996), pages 313 to 321"
    title: General decidability theorems for infinite-state systems
    locator: the backward reachability algorithm on upward-closed sets and its termination by a well-quasi-ordering
  - paper: "Alain Finkel and Philippe Schnoebelen, Well-structured transition systems everywhere!, Theoretical Computer Science 256(1-2), 2001, pages 63 to 92"
    title: Well-structured transition systems everywhere!
    locator: coverability for well-structured transition systems and the backward algorithm
  - paper: "Steven M. German and A. Prasad Sistla, Reasoning about systems with many processes, Journal of the ACM 39(3), 1992, pages 675 to 735"
    title: Reasoning about systems with many processes
    locator: the reduction of safety for any number of identical finite-state processes to coverability in a vector addition system
  - paper: doi:10.1109/5.24143
    title: Tadao Murata, Petri nets, properties, analysis and applications, Proceedings of the IEEE 77(4), 1989, pages 541 to 580
    locator: the sections on coverability, boundedness and place invariants
---

The *coverability problem* asks whether a [Petri net](/petri-net/) can reach, from its initial marking, some marking that has at least a given number of tokens in each place. It is the form that most safety questions about nets take: "can two processes be in the critical section at once?" asks whether a marking with two tokens in the critical place can be covered. Coverability is decidable by the [Karp-Miller tree](/karp-miller-tree/) and by a backward search on upward-closed sets. It is complete for [EXPSPACE](/expspace/): Lipton (1976) gave the lower bound and Rackoff (1978) the upper bound. It is much easier than exact reachability, whose decidability is the hard [theorem of Mayr and Kosaraju](/petri-net-reachability-decidability/) and whose complexity is Ackermann-complete.

## In plain words

A Petri net has places that hold tokens, and steps that take tokens from some places and put tokens into others. You start with some tokens. The question is: can you ever have at least this many tokens here, at least that many there, and so on? You do not ask for an exact state, only for a state that has enough. This is easier than asking for an exact state, because having more tokens never stops a step from happening. So if a state with enough tokens is possible, extra tokens never hurt, and the set of "bad" states is closed upward. That makes the problem decidable, but it can still need a very large amount of memory.

## Definition

A Petri net $N$ has a finite set of places $P$ and a finite set of transitions $T$. Each transition $t$ has two vectors $\mathrm{pre}(t), \mathrm{post}(t) \in \mathbb{N}^P$. A marking is a vector $M \in \mathbb{N}^P$. The transition $t$ is enabled in $M$ when $M \ge \mathrm{pre}(t)$ componentwise, and firing it gives $M' = M - \mathrm{pre}(t) + \mathrm{post}(t)$, written $M \xrightarrow{t} M'$. A marking $M$ is reachable from $M_0$ when there is a finite sequence of firings from $M_0$ to $M$.

**Coverability.** Input: a net $N$, an initial marking $M_0$ and a target marking $M_T$, with all numbers written in binary. Question: is there a marking $M$ reachable from $M_0$ with $M \ge M_T$? If so, $M_T$ is *coverable*.

The size of the input is the number of bits needed to write the net and the two markings.

The key fact is *monotonicity*: if $M \xrightarrow{t} M'$ and $L \ge M$, then $t$ is enabled in $L$ and $L \xrightarrow{t} L' $ with $L' - M' = L - M \ge 0$. So the set of markings from which $M_T$ can be covered is upward closed.

## Variants

- **Upward-closed targets.** Given a finite set of markings $B$, can the net reach a marking in the upward closure $\{M : M \ge b \text{ for some } b \in B\}$? This is a finite disjunction of coverability questions.
- **Control-state reachability.** In a vector addition system with states (VASS), a finite control moves while it adds integer vectors to counters that must stay nonnegative. The question is whether a control state can be reached with any counter values. Encoding each control state as a place with one token turns this into coverability, and back.
- **Boundedness.** Is the set of reachable markings finite? **Place boundedness** asks this for one place. The Karp-Miller tree decides both, and Rackoff showed boundedness is in EXPSPACE too.
- **Coverability for well-structured transition systems.** The backward algorithm works for any transition system with a well-quasi-ordering that is compatible with the steps and has computable predecessor bases. Examples are lossy channel systems, broadcast protocols and many extensions of nets.
- **Exact reachability.** Asking for $M = M_T$ instead of $M \ge M_T$ gives the [Petri net reachability problem](/petri-net-reachability-decidability/), which is decidable but Ackermann-complete.

## Examples

**A net that grows.** Take places $(p, q, r)$ and three transitions: $t_1$ takes a token from $p$ and puts it back with a new token in $q$; $t_2$ moves the token from $p$ to $r$; $t_3$ takes one token from $q$ and the token from $r$ and puts a token in $p$. Start from $M_0 = (1, 0, 0)$.

- The target $(0, 5, 1)$ is coverable: fire $t_1$ five times to reach $(1, 5, 0)$, then $t_2$ to reach $(0, 5, 1)$.
- The target $(1, 0, 1)$ is not coverable. Each transition keeps the sum $M(p) + M(r)$ unchanged: $t_1$ changes neither place, $t_2$ moves one token from $p$ to $r$, and $t_3$ moves one token from $r$ to $p$. So every reachable marking has $M(p) + M(r) = 1$, and none has $M(p) \ge 1$ and $M(r) \ge 1$.

Such a linear function that every transition keeps constant is a *place invariant*. Invariants can prove that a target is not coverable, but they do not decide the problem. The [Karp-Miller tree](/karp-miller-tree/) of this net has the labels $(1, 0, 0)$, $(1, \omega, 0)$, $(0, 0, 1)$ and $(0, \omega, 1)$, and it gives both answers above.

**Mutual exclusion for any number of processes.** Places $\mathit{idle}$, $\mathit{lock}$, $\mathit{crit}$. The transition $\mathit{enter}$ takes a token from $\mathit{idle}$ and the token from $\mathit{lock}$ and puts a token in $\mathit{crit}$; $\mathit{exit}$ does the reverse. With $n$ tokens in $\mathit{idle}$ and one in $\mathit{lock}$, the bad states are those with $\mathit{crit} \ge 2$, so the safety question is whether $(0, 0, 2)$ is coverable. It is not, for any $n$, because $\mathit{lock} + \mathit{crit}$ is an invariant equal to 1. If we add a transition $\mathit{spawn}$ that puts a token in $\mathit{idle}$ from nothing, the net is unbounded, but the answer is the same, and the Karp-Miller tree still finds it in finite time.

## Known algorithms

| Algorithm | Idea | Cost |
|---|---|---|
| [Karp-Miller tree](/karp-miller-tree/) (1969) | Forward search; places that grow along a path get $\omega$ | Always terminates, but the tree can be larger than any primitive recursive function of the input |
| Minimal coverability set (Finkel 1993) | Forward search that keeps only maximal $\omega$-markings | Same worst case; often much smaller in practice |
| Backward algorithm (Abdulla et al. 1996) | Compute a finite basis of the markings that can cover $M_T$ | Terminates by Dickson's lemma; doubly exponential time |
| Rackoff's search (1978) | Guess a covering sequence of at most doubly exponential length | Exponential space; optimal |

**Backward algorithm.** Let $U$ be the upward closure of $\{M_T\}$. The predecessors of an upward-closed set under one transition form an upward-closed set, and for the closure of a single marking $b$, the minimal predecessor by $t$ is $\mathrm{pre}(t) + \max(0, b - \mathrm{post}(t))$, with the maximum taken componentwise. Start with the basis $\{M_T\}$ and add the minimal predecessors of each new basis element, keeping only the minimal elements. Each step that changes the set adds a marking not above any earlier one. By Dickson's lemma, $\mathbb{N}^P$ has no infinite sequence in which no element is above an earlier one, so the process stops. Then $M_T$ is coverable if and only if $M_0$ is above some element of the final basis.

**Rackoff's bound.** Rackoff proved that if $M_T$ is coverable, then it is covered by a firing sequence of length at most $2^{2^{c\, n \log n}}$ for a constant $c$, where $n$ is the size of the input. The proof is by induction on the number of places: a covering sequence either keeps all counters below a threshold, so it can be shortened to avoid repeated markings, or a first place exceeds the threshold, after which that place can be ignored. A nondeterministic machine can guess such a sequence one step at a time, keep a step counter and the current marking in exponential space, and accept when the marking covers $M_T$. By [Savitch's theorem](/savitch-theorem/), this gives a deterministic algorithm in space $2^{O(n \log n)}$.

## Bounds

- **Upper bound.** Coverability and boundedness are in [EXPSPACE](/expspace/) (Rackoff 1978), in space $2^{O(n \log n)}$.
- **Lower bound.** Coverability is EXPSPACE-hard (Lipton 1976). Lipton's construction shows that a net of size polynomial in $n$ can simulate a counter machine whose counters are bounded by $2^{2^n}$, so coverability needs space $2^{\Omega(\sqrt{n})}$ in the size $n$ of the input. The same construction gives EXPSPACE-hardness for boundedness and for exact reachability.
- So coverability is **EXPSPACE-complete**. The gap between $2^{\Omega(\sqrt{n})}$ and $2^{O(n \log n)}$ is in the exponent of the space bound only.
- **The Karp-Miller tree** has no primitive recursive bound on its size. Mayr and Meyer (1981) built bounded nets whose reachability sets are larger than any primitive recursive function of the net size, and on a bounded net the tree contains each reachable marking.
- **Exact reachability** is much harder: decidable (Mayr 1981, Kosaraju 1982) and Ackermann-complete (Czerwiński and Orlikowski 2021, Leroux 2021). See [decidability of Petri net reachability](/petri-net-reachability-decidability/).

## Reductions

- **Coverability to reachability.** Add, for each place $p$, a transition $d_p$ that takes one token from $p$ and puts nothing back. Then $M_T$ is coverable in $N$ if and only if $M_T$ is reachable in the new net. If $M \ge M_T$ is reachable, fire $d_p$ exactly $M(p) - M_T(p)$ times for each $p$. Conversely, a run of the new net stays valid when each $d_p$ is moved to the end, because a later removal leaves more tokens at each earlier step, and by monotonicity every other transition stays enabled. The run without the $d_p$ steps reaches some $M$ with $M \ge M_T$. This shows that coverability is no harder than [reachability](/reachability-problem/).
- **Control-state reachability and coverability** reduce to each other in polynomial time, as described under Variants.
- **Hardness from bounded counter machines.** Lipton's lower bound is a reduction from the halting problem of counter machines whose counters are bounded by $2^{2^n}$, which is EXPSPACE-hard. A net cannot test a counter for zero, but with a complement place that holds $2^{2^n} - c$ when the counter holds $c$, the test "is the counter zero" becomes "can the complement place give up $2^{2^n}$ tokens". Lipton builds these large constants by repeated squaring with $O(n)$ levels.
- **Parameterized safety to coverability.** German and Sistla (1992) reduced safety for any number of copies of one finite-state process, with a control process, to coverability in a vector addition system: each place counts how many copies are in a given local state. Such a counting abstraction is exact when the copies are identical and do not use their identities.

## Applications

- **Safety properties of concurrent systems.** For a [safety property](/safety-property/) whose bad states are upward closed, such as "two processes in the critical section", verification is a coverability check. Many mutual exclusion and cache coherence protocols are checked this way, for any number of processes.
- **Multithreaded programs with finite-state threads.** If each thread is a finite-state machine and threads share finite-state variables, the counting abstraction gives a Petri net, and thread-state reachability is coverability.
- **Boundedness of buffers.** Place boundedness tells whether a channel or a buffer in a system modelled as a net can overflow, whatever its capacity.
- **Well-structured systems.** The backward algorithm decides coverability for lossy channel systems and for broadcast protocols, where exact reachability is undecidable.

## References

- Richard M. Karp and Raymond E. Miller, Parallel program schemata, Journal of Computer and System Sciences 3(2), 1969, pages 147 to 195.
- Charles Rackoff, The covering and boundedness problems for vector addition systems, Theoretical Computer Science 6(2), 1978, pages 223 to 231.
- Richard J. Lipton, The reachability problem requires exponential space, Research Report 62, Yale University, 1976.
- Parosh Aziz Abdulla, Kārlis Čerāns, Bengt Jonsson and Yih-Kuen Tsay, General decidability theorems for infinite-state systems, LICS 1996, pages 313 to 321.
- Alain Finkel and Philippe Schnoebelen, Well-structured transition systems everywhere!, Theoretical Computer Science 256(1-2), 2001, pages 63 to 92.
- Steven M. German and A. Prasad Sistla, Reasoning about systems with many processes, Journal of the ACM 39(3), 1992, pages 675 to 735.
- Tadao Murata, Petri nets, properties, analysis and applications, Proceedings of the IEEE 77(4), 1989, pages 541 to 580.
