---
tag: G0X523
kind: definition
slug: sc-class
name: SC
aliases:
- Steve's class
area: complexity/complexity-classes
level: advanced
summary: The problems that one deterministic machine solves in polynomial time and polylogarithmic space at the same time. Its first level SC^1 is L.
prereqs: [p, logspace]
see_also: [nc, randomized-logspace, nisan-prg, savitch-theorem, nondeterministic-logspace, pushdown-automaton, context-free-grammar, breadth-first-search]
sources:
  - paper: doi:10.1145/800135.804426
    title: Stephen A. Cook, Deterministic CFL's are accepted simultaneously in polynomial time and log squared space, 11th Annual ACM Symposium on Theory of Computing, 338 to 345 (1979)
    locator: the main theorem, deterministic context-free languages in SC^2
  - paper: doi:10.1007/BF01205052
    title: Noam Nisan, RL ⊆ SC, Computational Complexity 4(1), 1 to 11 (1994)
    locator: the main theorem, randomized logspace in SC
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2), 177 to 192 (1970)
    locator: the reachability procedure in O(log^2 n) space
---

SC is the class of decision problems that a deterministic Turing machine decides in polynomial time and polylogarithmic space *at the same time*, with one machine meeting both bounds. The name stands for "Steve's class", after Stephen Cook, who proved in 1979 that every deterministic context-free language is in it. SC sits inside the intersection of P and polylogarithmic space, but it is not known to equal that intersection: a problem can have a polynomial-time algorithm and a different polylog-space algorithm without having one algorithm that does both. Directed reachability is the main example. Its first level, $\mathsf{SC}^1$, is L, and Nisan proved that randomized logspace is in SC.

## Definition

**Model.** The machine is a deterministic [multitape Turing machine](/multitape-turing-machine/) with a read-only input tape; only the work tapes count toward the space. $\mathsf{TISP}(t(n), s(n))$ is the class of languages decided by one such machine that runs for at most $O(t(n))$ steps and uses at most $O(s(n))$ work cells on every input of length $n$.

**Definition.** For $k \ge 1$,

$$\mathsf{SC}^k = \mathsf{TISP}(n^{O(1)}, \log^k n) = \bigcup_{c \ge 1} \mathsf{TISP}(n^c, \log^k n), \qquad \mathsf{SC} = \bigcup_{k \ge 1} \mathsf{SC}^k.$$

**The first level is L.** A deterministic logspace machine that halts has at most $n^{O(1)}$ configurations and never repeats one, so it runs in polynomial time; see [L](/logspace/). So $\mathsf{L} = \mathsf{TISP}(n^{O(1)}, \log n) = \mathsf{SC}^1$.

**Inclusions.**

- $\mathsf{L} = \mathsf{SC}^1 \subseteq \mathsf{SC}^2 \subseteq \cdots \subseteq \mathsf{SC}$.
- $\mathsf{SC} \subseteq \mathsf{P} \cap \mathsf{polyL}$, where $\mathsf{polyL} = \bigcup_k \mathsf{DSPACE}(\log^k n)$. Whether the two classes are equal is open.
- $\mathsf{SC} \subsetneq \mathsf{PSPACE}$, since $\mathsf{polyL} \subsetneq \mathsf{PSPACE}$ by the [space hierarchy theorem](/space-hierarchy-theorem/).

## Examples and non-examples

**Problems in L.** Every problem in L is in $\mathsf{SC}^1$. Examples are balanced parentheses, binary addition and undirected reachability; see [L](/logspace/).

**Deterministic context-free languages.** Cook (1979) proved that every language accepted by a deterministic [pushdown automaton](/pushdown-automaton/) is in $\mathsf{SC}^2$: the membership test runs in polynomial time and $O(\log^2 n)$ space. The usual parser keeps the whole stack, which can have linear size. General context-free languages are in P by the [CYK algorithm](/cyk-algorithm/) and in $\mathsf{DSPACE}(\log^2 n)$, but they are not known to be in SC.

**Randomized logspace.** Nisan (1994) proved that $\mathsf{RL} \subseteq \mathsf{SC}$; later work states the result for $\mathsf{BPL}$, the two-sided version, which his method also covers. The simulation runs in polynomial time and $O(\log^2 n)$ space. It uses his pseudorandom generator for space-bounded machines, with a seed of $O(\log^2 n)$ bits, but it does not try all seeds, because there are $2^{O(\log^2 n)}$ of them. See [RL](/randomized-logspace/) and [Nisan's generator](/nisan-prg/).

**Directed reachability (not known to be in SC).** Directed reachability has two classic algorithms, and each meets only one bound.

- [Breadth-first search](/breadth-first-search/) runs in linear time, but it keeps a set of visited vertices, which takes $n$ bits.
- [Savitch's algorithm](/savitch-theorem/) uses $O(\log^2 n)$ space, but it is slow. To decide whether $v$ is reachable from $u$ in at most $t$ steps, it tries each of the $n$ vertices $w$ as a midpoint and calls itself on $(u, w, \lceil t/2 \rceil)$ and $(w, v, \lfloor t/2 \rfloor)$. With $\lceil \log_2 n \rceil$ levels of recursion, the number of calls is $C_k = 1 + 2 n C_{k-1}$ with $C_0 = 1$. For $n = 16$ and 4 levels this is 1082401 calls, and for $n = 1024$ and 10 levels it is about $1.3 \times 10^{33}$ calls. In general the time is $n^{O(\log n)}$, which is not polynomial.

No algorithm is known that does both. Directed reachability is NL-complete under logspace reductions, and SC is closed under logspace reductions, so whether $\mathsf{NL} \subseteq \mathsf{SC}$ is the same question as whether directed reachability is in SC. It is open.

**P-complete problems (not known to be in SC).** The [circuit value problem](/circuit-value-problem/) is P-complete under logspace reductions. If it were in SC, then $\mathsf{P} \subseteq \mathsf{SC} \subseteq \mathsf{polyL}$, which is open and not expected.

## Related definitions

- **NC** is the class of problems with polynomial-size circuits of polylogarithmic depth. Its name, "Nick's class", honors Nicholas Pippenger, as SC honors Cook. $\mathsf{NC}^1 \subseteq \mathsf{L} = \mathsf{SC}^1$, but whether $\mathsf{NC} \subseteq \mathsf{SC}$ or $\mathsf{SC} \subseteq \mathsf{NC}$ is unknown. Directed reachability is in $\mathsf{NC}^2$ but not known to be in SC. See [NC](/nc/).
- **polyL** is polylogarithmic space with no bound on the time. It contains SC and NL.
- **L** is the first level $\mathsf{SC}^1$. See [L](/logspace/).
- **P** contains SC. See [P](/p/).
- **TISP** classes with other pairs of bounds use the same idea of one machine with two bounds. They appear in time-space lower bounds for [SAT](/sat/).

## References
