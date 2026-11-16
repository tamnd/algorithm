---
tag: YNZVQD
kind: definition
slug: randomized-logspace
name: RL
aliases:
- randomized logspace
area: complexity/complexity-classes
level: advanced
summary: The problems that a logspace machine with coin flips decides in polynomial time with one-sided error. It contains L and is contained in NL.
prereqs: [logspace, probabilistic-turing-machine, nondeterministic-logspace]
see_also: [rl-versus-l, nisan-prg, symmetric-logspace, sc-class, bpp, rp, one-sided-error, markov-chain]
sources:
  - paper: doi:10.1137/0206049
    title: John Gill, Computational complexity of probabilistic Turing machines, SIAM Journal on Computing 6(4), 675 to 695 (1977)
    locator: probabilistic Turing machines and their space-bounded classes
  - paper: doi:10.1109/SFCS.1979.34
    title: Romas Aleliunas, Richard M. Karp, Richard J. Lipton, László Lovász and Charles Rackoff, Random walks, universal traversal sequences, and the complexity of maze problems, 20th Annual Symposium on Foundations of Computer Science, 218 to 223 (1979)
    locator: the cover time bound 2|E|(n-1) and undirected reachability in randomized logspace
  - paper: doi:10.1007/BF01205052
    title: Noam Nisan, RL ⊆ SC, Computational Complexity 4(1), 1 to 11 (1994)
    locator: the main theorem, a simulation in polynomial time and O(log^2 n) space
  - paper: doi:10.1006/jcss.1998.1616
    title: Michael Saks and Shiyu Zhou, BP_H SPACE(S) ⊆ DSPACE(S^{3/2}), Journal of Computer and System Sciences 58(2), 376 to 403 (1999)
    locator: the main theorem, BPL in DSPACE(log^{3/2} n)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 7, Randomized Computation (randomized space-bounded computation)
---

RL, randomized logspace, is the class of decision problems that a probabilistic Turing machine decides with $O(\log n)$ work space and polynomial running time, with *one-sided error*: on a yes-instance it accepts with probability at least $1/2$, and on a no-instance it never accepts. It is the logspace analogue of [RP](/rp/). The machine reads its random bits once, in order, and it cannot store more than $O(\log n)$ of them. RL contains L and is contained in NL. The two-sided version is called BPL. Undirected reachability was the first famous problem in RL that was not known to be in L, by a random walk; Reingold later put it in L. Whether $\mathsf{RL} = \mathsf{L}$ is open, and it is widely believed to be true; see [RL versus L](/rl-versus-l/).

## Definition

**Model.** A probabilistic logspace machine is a [probabilistic Turing machine](/probabilistic-turing-machine/) with a read-only input tape, work tapes with $O(\log n)$ cells in total, and a source of random bits. The random bits come on a separate tape that the machine reads from left to right only, one new bit at each coin flip. So the machine cannot go back to an earlier coin unless it wrote that coin on its work tape. As usual, only the work tapes count toward the space.

**Definition.** A language $A$ is in $\mathsf{RL}$ if some probabilistic logspace machine $M$ halts within $p(n)$ steps on every input of length $n$ and every sequence of coins, for a polynomial $p$, and

- if $x \in A$, then $\Pr[M \text{ accepts } x] \ge 1/2$;
- if $x \notin A$, then $\Pr[M \text{ accepts } x] = 0$.

**BPL.** A language $A$ is in $\mathsf{BPL}$, bounded-error probabilistic logspace, if a machine of the same kind accepts every $x \in A$ with probability at least $2/3$ and every $x \notin A$ with probability at most $1/3$. See [one-sided error](/one-sided-error/) and [two-sided error](/two-sided-error/) for the two error types.

**Why the time bound.** Without the polynomial time bound the class changes. A logspace machine with coins can run for exponentially many steps, and with that much time it can decide every problem in NL with one-sided error. On input $\langle G, s, t \rangle$, it repeats the following round. It guesses a path of at most $n - 1$ steps from $s$ with random bits, and it accepts if the path is valid and reaches $t$; this succeeds with probability at least $n^{-n}$ when $t$ is reachable. Then it flips $2 n \lceil \log_2 n \rceil$ coins and rejects if all of them come up heads, which happens with probability at most $n^{-2n}$. The machine needs only a counter for the coins. A yes-instance is accepted with probability at least $1/2$, because a success comes far more often than the stop, and a no-instance is never accepted. But the expected running time is exponential, and some coin sequences never stop. The polynomial time bound excludes such machines.

**Error reduction.** The constant $1/2$ is not important. Run $M$ independently $k$ times and accept if some run accepts. A no-instance is still never accepted, and a yes-instance is rejected with probability at most $2^{-k}$, which is 0.0009765625 for $k = 10$. The new machine stores only a run counter, so the space stays $O(\log n)$. For BPL, take a majority vote of $k$ runs and count the accepting runs; the [Chernoff bound](/chernoff-bound/) makes the error exponentially small in $k$.

**Inclusions.**

- $\mathsf{L} \subseteq \mathsf{RL}$: a deterministic machine is a probabilistic machine that ignores its coins.
- $\mathsf{RL} \subseteq \mathsf{NL}$: a machine accepts $x$ with positive probability if and only if some sequence of coins leads to acceptance. Read the coins as nondeterministic guesses.
- $\mathsf{RL} \subseteq \mathsf{BPL}$, by running the RL machine twice and accepting if one run accepts, which gives success probability at least $3/4$.
- $\mathsf{BPL} \subseteq \mathsf{SC}$, so BPL, and with it RL, can be simulated deterministically in polynomial time and $O(\log^2 n)$ space at the same time. Nisan proved this in 1994, using his pseudorandom generator for space-bounded machines; see [Nisan's generator](/nisan-prg/) and [SC](/sc-class/).
- $\mathsf{BPL} \subseteq \mathsf{DSPACE}(\log^{3/2} n)$ (Saks and Zhou 1999). This uses less space than Nisan's simulation, but it does not give polynomial time.
- $\mathsf{BPL} \subseteq \mathsf{P}$, since the acceptance probability can be computed exactly from the polynomially many configurations.

## Examples and non-examples

**Undirected reachability by a random walk.** Aleliunas, Karp, Lipton, Lovász and Rackoff (1979) proved that a random walk on a connected undirected graph with $n$ vertices and $|E|$ edges visits every vertex within $2|E|(n-1)$ expected steps. So the following machine decides undirected reachability in RL. From $s$, it walks $4|E|(n-1)$ steps, and at each step it moves to a random neighbor of the current vertex. It accepts if the walk meets $t$. The machine stores the current vertex and a step counter. If $t$ is in the component of $s$, then by [Markov's inequality](/markov-inequality/) the walk meets $t$ with probability at least $1/2$. If $t$ is not in that component, the walk never meets it, so the error is one-sided.

Take the path $0 - 1 - 2 - 3 - 4$, with $n = 5$ and $|E| = 4$, and $s = 0$, $t = 4$. The walk has $4 \cdot 4 \cdot 4 = 64$ steps. The exact probability that it meets vertex 4 is 0.99239, so the miss probability is about 0.0076, much less than the bound of $1/2$. The expected number of steps from vertex $v$ to vertex 4 is 16, 15, 12, 7 and 0 for $v = 0, 1, 2, 3, 4$. With three independent walks the miss probability falls to about $4.4 \times 10^{-7}$. The problem is now known to be in L (Reingold 2008); see [SL](/symmetric-logspace/).

**Directed reachability (not known to be in RL).** In a directed graph a random walk can need exponential time. Take the vertices $0, \ldots, n - 1$, an edge $0 \to 1$, and for $1 \le i \le n - 2$ the edges $i \to i + 1$ and $i \to 0$. A walk from 0 reaches $n - 1$ only by going forward $n - 1$ times in a row. The expected number of steps is 766 for $n = 10$ and 3145726 for $n = 22$. For $n = 22$, a walk of $n^3 = 10648$ steps reaches $n - 1$ with probability only about 0.0034. Directed reachability is NL-complete under logspace reductions, so it is in RL if and only if $\mathsf{RL} = \mathsf{NL}$, which is open.

**Problems in L.** Every problem in L, such as balanced parentheses or arithmetic on binary numbers, is in RL with no use of the coins. See [L](/logspace/).

## Related definitions

- **BPL** is the two-sided version, defined above. It contains RL and is contained in SC and in $\mathsf{DSPACE}(\log^{3/2} n)$.
- **coRL** is the class of complements of RL languages, with errors only on no-instances. $\mathsf{ZPL} = \mathsf{RL} \cap \mathsf{coRL}$ is the zero-error version.
- **PL** is the unbounded-error version, with acceptance probability above $1/2$ exactly on yes-instances. It contains NL, and it is contained in $\mathsf{DSPACE}(\log^2 n)$ by results of Jung and of Borodin, Cook and Pippenger.
- **RP and BPP** are the polynomial-time analogues. See [RP](/rp/) and [BPP](/bpp/).
- **NL** contains RL. See [NL](/nondeterministic-logspace/).
- **SL** is contained in RL by the random walk above, and it equals L. See [SL](/symmetric-logspace/).
- **RL versus L.** Whether the coins can be removed is open. The deterministic simulations of Nisan and of Saks and Zhou above are partial answers. See [RL versus L](/rl-versus-l/).

## References
