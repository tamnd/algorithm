---
tag: KR890T
kind: definition
slug: logspace
name: L (LOGSPACE)
aliases:
- L
- log space
area: complexity/complexity-classes
level: intro
summary: The decision problems that a deterministic Turing machine solves with O(log n) cells of work tape, with the input on a read-only tape.
prereqs: [space-complexity, multitape-turing-machine, complexity-class]
see_also: [nondeterministic-logspace, symmetric-logspace, randomized-logspace, sc-class, pspace, nc, circuit-value-problem, space-hierarchy-theorem]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 8.4, The Classes L and NL; Section 8.5, NL-Completeness (logspace transducers and reductions)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 4, Space Complexity
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 16, Logarithmic Space
  - paper: doi:10.1016/S0022-0000(75)80050-X
    title: Neil D. Jones, Space-bounded reducibility among combinatorial problems, Journal of Computer and System Sciences 11(1), 68 to 85 (1975)
    locator: logspace reductions and their composition
  - paper: doi:10.1137/0206054
    title: Allan Borodin, On relating time and space to size and depth, SIAM Journal on Computing 6(4), 733 to 744 (1977)
    locator: the inclusions of NC1 in L and of NL in NC2
  - paper: doi:10.1109/FOCS.1965.11
    title: Richard E. Stearns, Juris Hartmanis and Philip M. Lewis II, Hierarchies of memory limited computations, 6th Annual Symposium on Switching Circuit Theory and Logical Design, 179 to 190 (1965)
    locator: the lower bound of log log n on unbounded space
---

L, also written LOGSPACE, is the class of decision problems that a deterministic [multitape Turing machine](/multitape-turing-machine/) decides with $O(\log n)$ cells of work tape on inputs of length $n$. The input sits on a read-only tape that does not count toward the space. With $O(\log n)$ bits, a machine can hold a constant number of pointers into the input and counters up to a polynomial in $n$, and it can do nothing more. That is enough for many basic tasks: compare symbols at two positions, count, add numbers, and follow a path in a graph where each vertex has one exit. L is a subset of NL, which is a subset of P. L is a proper subset of PSPACE. Whether L equals NL, and whether L equals P, are open.

## Definition

**Model.** The machine is a deterministic multitape Turing machine with a read-only input tape and $k$ read-write work tapes. The input tape holds $x$ between two end markers, so its head has $n + 2$ positions and cannot leave that region. The space of a run is the number of distinct work-tape cells that the run visits. The input tape does not count. If it did, every machine would use at least $n$ cells when it reads its whole input, and no bound below $n$ would mean anything. See [space complexity](/space-complexity/) for the general notion.

**Definition.** For a function $s$, $\mathsf{DSPACE}(s(n))$ is the class of languages $A$ such that some deterministic machine of this kind halts on every input, accepts exactly the strings in $A$, and uses at most $c \cdot s(n)$ work cells on every input of length $n$, for a constant $c$. Then

$$\mathsf{L} = \mathsf{DSPACE}(\log n) = \bigcup_{c \ge 1} \mathsf{DSPACE}(c \log n).$$

The constant $c$ does not matter, and neither does the number of work tapes: a machine can pack a block of cells into one cell of a larger alphabet, and it can keep several tapes on the tracks of one tape.

**Configurations.** A configuration of the machine on input $x$ is the state, the position of the input head, the positions of the work heads, and the contents of the work tapes. The input is fixed, so it is not part of the configuration. With $|Q|$ states, a work alphabet $\Gamma$, $k$ work tapes and space $s = c \log n$, the number of configurations is at most

$$|Q| \cdot (n + 2) \cdot s^k \cdot |\Gamma|^{k s} = n^{O(1)},$$

because $|\Gamma|^{k c \log n} = n^{k c \log |\Gamma|}$. A deterministic machine that halts never repeats a configuration, since a repeat would make it loop for ever. So a logspace machine halts within polynomially many steps, and $\mathsf{L} \subseteq \mathsf{P}$.

**Logspace transducers and reductions.** A logspace transducer is a logspace machine with one more tape, a write-only output tape whose head moves only to the right. The output tape does not count toward the space. A function $f$ is *logspace computable* if a logspace transducer outputs $f(x)$ on input $x$ and halts. By the count above, $|f(x)|$ is at most a polynomial in $|x|$. A language $A$ is *logspace many-one reducible* to $B$, written $A \le_{\mathrm{L}} B$, if some logspace computable $f$ satisfies $x \in A \iff f(x) \in B$ for every $x$. Logspace reductions are the reductions for NL-completeness and P-completeness, because polynomial-time reductions are too strong to separate the classes inside P.

**Composition.** Let $f$ and $g$ be logspace computable. To compute $g(f(x))$, run the transducer for $g$ and do not store $f(x)$. When $g$ needs bit $i$ of its input, run the transducer for $f$ on $x$ from the beginning, count its output bits, discard them, and keep only bit $i$. The machine stores $i$, the counter and the work tapes of both transducers. Since $|f(x)|$ is polynomial in $|x|$, all of this fits in $O(\log |x|)$ cells. So $g \circ f$ is logspace computable (Jones 1975). Two consequences follow: $\le_{\mathrm{L}}$ is transitive, and if $A \le_{\mathrm{L}} B$ and $B \in \mathsf{L}$, then $A \in \mathsf{L}$. The time can grow, because $f$ runs again for each bit, but it stays polynomial.

## Examples and non-examples

**Palindromes.** The language of strings $x$ with $x = x^R$ is in L. For $i = 1, \ldots, \lfloor n/2 \rfloor$, the machine compares $x_i$ with $x_{n+1-i}$. It keeps $i$, the position $n + 1 - i$ and one counter to move the input head to a position. Each number is at most $n + 1$, so it needs $\lceil \log_2(n+1) \rceil$ bits. For $n = 10^6$ that is 20 bits per number, so 60 bits of work tape in total, against an input of $10^6$ symbols. The machine moves its input head back and forth, so it uses $O(n^2)$ time; it saves space and pays in time.

**Balanced parentheses.** A string over $\{(, )\}$ is balanced if a counter that adds 1 for "(" and subtracts 1 for ")" never goes below 0 and ends at 0. The counter is at most $n$, so it fits in $O(\log n)$ bits. For "(()(()))" the counter takes the values 1, 2, 1, 2, 3, 2, 1, 0, and the string is accepted. For "())(" the values are 1, 0, -1, and the machine rejects at the third symbol. See [balanced parentheses](/balanced-parentheses/) for the stack method, which uses linear space.

**Arithmetic.** The sum of two $n$-bit numbers is logspace computable: the transducer writes the bits from the least significant one, and it keeps an index and one carry bit. Comparison of two numbers, and the product of two numbers, are also logspace computable; the product needs the column sums, which are at most $n$ and so fit in $O(\log n)$ bits.

**Paths with one exit.** Let $G$ be a directed graph in which each vertex has out-degree at most 1, and let $s$ and $t$ be vertices. Whether $t$ is reachable from $s$ is in L: start at $s$, follow the unique out-edge $n - 1$ times, and accept if the walk meets $t$. The machine keeps the current vertex and a step counter. In a general directed graph this fails, because the machine would have to remember which branch it took at each vertex.

**Directed reachability (not known to be in L).** [Graph reachability](/graph-reachability/) on directed graphs is NL-complete under logspace reductions. So it is in L if and only if $\mathsf{L} = \mathsf{NL}$, which is open. See [NL](/nondeterministic-logspace/).

**Undirected reachability.** Reachability in an undirected graph is in L. This is Reingold's theorem, which shows that SL equals L. See [SL](/symmetric-logspace/).

**Circuit value (not known to be in L).** The [circuit value problem](/circuit-value-problem/) is P-complete under logspace reductions, so it is in L if and only if $\mathsf{L} = \mathsf{P}$, which is open.

**Problems that need more space.** The [space hierarchy theorem](/space-hierarchy-theorem/) gives a language in $\mathsf{DSPACE}(\log^2 n)$ that is not in L. It also gives $\mathsf{L} \ne \mathsf{PSPACE}$. At the low end, a machine of this model that uses $o(\log \log n)$ space in fact uses constant space, so it accepts a regular language (Stearns, Hartmanis and Lewis 1965). Between constant space and $\log \log n$ there is nothing new.

## Related definitions

- **NL** is the nondeterministic version. Directed reachability is complete for it, and $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n)$ by [Savitch's theorem](/savitch-theorem/). See [nondeterministic logspace](/nondeterministic-logspace/).
- **SL** is defined by symmetric machines. Reingold proved $\mathsf{SL} = \mathsf{L}$. See [symmetric logspace](/symmetric-logspace/).
- **RL** is the one-sided-error randomized version. Whether it equals L is open; see [randomized logspace](/randomized-logspace/) and [RL versus L](/rl-versus-l/).
- **SC** is the class of problems solvable in polynomial time and polylogarithmic space at the same time. Its first level is L. See [SC](/sc-class/).
- **FL** is the class of logspace computable functions.
- **Circuits.** Borodin (1977) proved $\mathsf{NC}^1 \subseteq \mathsf{L}$, with logspace-uniform circuits, and $\mathsf{NL} \subseteq \mathsf{NC}^2$. So $\mathsf{NC}^1 \subseteq \mathsf{L} \subseteq \mathsf{NL} \subseteq \mathsf{NC}^2$. See [NC](/nc/).
- **The chain to PSPACE.** $\mathsf{L} \subseteq \mathsf{NL} \subseteq \mathsf{P} \subseteq \mathsf{NP} \subseteq \mathsf{PSPACE}$. Of these inclusions, only $\mathsf{L} \ne \mathsf{PSPACE}$ and $\mathsf{NL} \ne \mathsf{PSPACE}$ are known to be strict. See [PSPACE](/pspace/).
- **L-completeness.** Under logspace reductions, every language in L other than the empty set and the set of all strings is complete for L, so the notion is useless. Completeness for L uses weaker reductions, such as first-order or $\mathsf{NC}^1$ reductions.

## References
