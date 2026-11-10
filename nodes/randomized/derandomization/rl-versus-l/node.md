---
tag: Y9DSKC
kind: concept
slug: rl-versus-l
name: RL versus L
aliases:
- RL = L question
- BPL = L
- derandomization of space
area: randomized/derandomization
level: research
summary: The open question whether randomized logspace computation can be simulated deterministically in logspace.
prereqs: [logspace, randomized-logspace, space-complexity]
see_also: [nisan-prg, symmetric-logspace, nondeterministic-logspace, savitch-theorem, read-once-branching-program, graph-reachability, expander-walk-sampler, pseudorandom-generator]
sources:
  - paper: doi:10.1109/sfcs.1979.34
    title: Romas Aleliunas, Richard M. Karp, Richard J. Lipton, László Lovász and Charles Rackoff, Random walks, universal traversal sequences, and the complexity of maze problems, FOCS 1979
    locator: pages 218 to 223 (the cover time bound 2m(n-1) and undirected connectivity in randomized logspace)
  - paper: doi:10.1007/BF01305237
    title: Noam Nisan, Pseudorandom generators for space-bounded computation, Combinatorica 12(4), 1992
    locator: pages 449 to 461 (a generator with seed length O(log^2 n) that fools logspace machines)
  - paper: doi:10.1007/BF01205052
    title: Noam Nisan, RL is contained in SC, Computational Complexity 4(1), 1994
    locator: pages 1 to 11 (BPL in polynomial time and O(log^2 n) space at the same time)
  - paper: doi:10.1006/jcss.1998.1616
    title: Michael Saks and Shiyu Zhou, BP_H SPACE(S) is contained in DSPACE(S^(3/2)), Journal of Computer and System Sciences 58(2), 1999
    locator: pages 376 to 403 (the simulation of BPL in deterministic space O(log^(3/2) n))
  - paper: doi:10.1145/1391289.1391291
    title: Omer Reingold, Undirected connectivity in log-space, Journal of the ACM 55(4), 2008
    locator: article 17 (a deterministic logspace algorithm for undirected s-t connectivity with the zig-zag product, so SL = L)
  - paper: doi:10.4230/LIPIcs.APPROX/RANDOM.2021.28
    title: William M. Hoza, Better pseudodistributions and derandomization for space-bounded computation, RANDOM 2021
    locator: the main theorem (BPL in DSPACE(log^(3/2) n / sqrt(log log n)))
---

**RL versus L** is the open question whether every problem that a randomized machine with logarithmic memory solves with one-sided error can also be solved by a deterministic machine with logarithmic memory. The two-sided version asks whether BPL equals L. The best known deterministic simulation of BPL uses space $O(\log^{3/2} n)$ (Saks and Zhou 1999), a little better after Hoza (2021), and the main example of a problem in RL, undirected connectivity, is now known to be in L (Reingold 2008). It is widely believed that $\mathrm{L} = \mathrm{RL} = \mathrm{BPL}$, but none of these equalities is proved.

## In plain words

Some problems can be solved by a program that uses very little memory if it may also flip coins. The question is whether the coins are really needed.

A logspace program keeps only a few counters and pointers into its input. RL is the set of problems that such a program solves with coins, where it may miss a yes answer but never says yes wrongly. L is the same set without coins. Nobody knows whether the two are equal.

The best known method without coins uses somewhat more memory than the program with coins. A famous test case was whether two points in a maze are connected. A random walk solves it with little memory, and Reingold found a method without coins that uses equally little memory. Most researchers believe that coins never save memory.

## The idea

Notation. $n$ is the input length. $\mathrm{DSPACE}(s)$ is the class of languages decided by deterministic machines with $O(s)$ work space. $\mathrm{L} = \mathrm{DSPACE}(\log n)$ is [logspace](/logspace/).

**The classes.** A randomized logspace machine has $O(\log n)$ work space and a separate tape of random bits that it reads once, from left to right, as if it flips a coin when it needs one. It must halt within time polynomial in $n$ on every input and every random string.

- $\mathrm{RL}$ ([randomized logspace](/randomized-logspace/)): inputs in the language are accepted with probability at least $1/2$, and other inputs are never accepted.
- $\mathrm{BPL}$: inputs in the language are accepted with probability at least $2/3$, and other inputs with probability at most $1/3$.

In both classes, the error can be made $2^{-p(n)}$ for any polynomial $p$ by running the machine again on fresh random bits and counting the results, since a counter fits in logarithmic space. The time bound and the read-once access are part of the definitions; without them the classes change.

**What is known.**

$$\mathrm{L} \subseteq \mathrm{RL} \subseteq \mathrm{NL} \subseteq \mathrm{DSPACE}(\log^2 n), \qquad \mathrm{RL} \subseteq \mathrm{BPL} \subseteq \mathrm{DSPACE}(\log^{3/2} n).$$

- $\mathrm{RL} \subseteq \mathrm{NL}$: an RL machine accepts some input exactly when some random string leads to acceptance, which a [nondeterministic logspace](/nondeterministic-logspace/) machine can guess. [Savitch's theorem](/savitch-theorem/) gives $\mathrm{NL} \subseteq \mathrm{DSPACE}(\log^2 n)$.
- $\mathrm{BPL} \subseteq \mathrm{DSPACE}(\log^2 n)$: on a fixed input, the machine is a Markov chain on its polynomially many configurations. The probability of acceptance is an entry of a power of the transition matrix, which repeated squaring computes in space $O(\log^2 n)$.
- **Nisan's generator (1992).** A [pseudorandom generator](/pseudorandom-generator/) with seed length $O(\log^2 n)$ fools every logspace machine, and more generally every [read-once branching program](/read-once-branching-program/) of polynomial width and length. Trying all seeds gives $\mathrm{BPL} \subseteq \mathrm{DSPACE}(\log^2 n)$ once more. See [Nisan's generator](/nisan-prg/).
- **Nisan (1994): $\mathrm{BPL} \subseteq \mathrm{SC}$.** By reusing the structure of his generator, Nisan showed that BPL can be simulated deterministically in polynomial time and space $O(\log^2 n)$ at the same time. Savitch's simulation, by contrast, takes time $n^{\Theta(\log n)}$.
- **Saks and Zhou (1999): $\mathrm{BPL} \subseteq \mathrm{DSPACE}(\log^{3/2} n)$.** They apply Nisan's generator to compute powers of the transition matrix in stages, and round the intermediate matrices with a small random perturbation, so that the seeds of the stages can be reused.
- **Hoza (2021).** A refinement with weighted pseudorandom distributions gives $\mathrm{BPL} \subseteq \mathrm{DSPACE}(\log^{3/2} n / \sqrt{\log\log n})$, the first improvement on Saks and Zhou.
- **$\mathrm{SL} = \mathrm{L}$ (Reingold 2008).** Undirected s-t connectivity is complete for symmetric logspace ([SL](/symmetric-logspace/)), and it was the main example of a problem in RL not known to be in L. Reingold gave a deterministic logspace algorithm. It turns each connected component into an expander with constant degree by repeated powering and the zig-zag product, which keeps the degree constant, and then tries all paths of logarithmic length. So $\mathrm{L} = \mathrm{SL} \subseteq \mathrm{RL}$.

**What is open.**

- Is $\mathrm{RL} = \mathrm{L}$? Is $\mathrm{BPL} = \mathrm{L}$? Even $\mathrm{BPL} \subseteq \mathrm{DSPACE}(\log^{1.49} n)$ is not known.
- Is $\mathrm{RL} = \mathrm{NL}$? Directed s-t connectivity is complete for NL, and no randomized logspace algorithm for it is known.
- Is there an explicit generator with seed length $o(\log^2 n)$ for all read-once branching programs of polynomial width and length? Nisan's seed length is still the best known for this class with constant error. Better generators are known for restricted classes, such as programs of small width or regular programs.

The belief that $\mathrm{BPL} = \mathrm{L}$ rests on the steady progress above and on conditional results: as for time, hardness assumptions give derandomization, here with a hard function computable in linear space that needs large branching programs. Unlike the question of BPP versus P, the space question is not known to need new circuit lower bounds.

## Examples

- **Undirected connectivity by a random walk (Aleliunas, Karp, Lipton, Lovász and Rackoff 1979).** In a connected [undirected graph](/undirected-graph/) with $n$ vertices and $m$ edges, the expected time for a random walk to visit every vertex is at most $2m(n - 1)$. To decide whether $t$ is reachable from $s$, walk $4m(n - 1)$ steps from $s$ and accept if the walk meets $t$. If $t$ is not reachable, the walk never meets it. If $t$ is reachable, by the [Markov inequality](/markov-inequality/) the walk misses $t$ with probability at most $1/2$. The machine stores the current vertex and a step counter up to $4m(n-1) < 2n^3$, so it uses $O(\log n)$ space, and the problem is in RL. Reingold's algorithm later put it in L.
- **Why directed graphs are harder.** Take vertices $1, \ldots, n$ with an edge from $i$ to $i + 1$ and an edge from $i$ back to $1$, for each $i < n$. A random walk from 1 reaches $n$ only after $n - 1$ forward steps in a row, which has probability $2^{-(n-1)}$ per attempt, so the expected time is exponential. Directed connectivity is in NL, but random walks do not put it in RL.
- **Space bounds for $n = 2^{20}$.** With $\log_2 n = 20$, a deterministic simulation in space $\log^2 n$ needs about 400 cells of $O(1)$ bits each, up to constant factors, and $\log^{3/2} n$ needs about 89. An RL machine needs about 20. The gap between these numbers is the open question.
- **Read-once branching programs.** Fix the input of a logspace machine that uses $R = \mathrm{poly}(n)$ random bits. Its configurations at each step form the layers of a read-once branching program of width $\mathrm{poly}(n)$ and length $R$, which reads the random bits in order. A generator with seed length $O(\log n)$ that fools all such programs and runs in logspace would give $\mathrm{BPL} = \mathrm{L}$, by trying all seeds.

## Where it is used

- **Pseudorandom generators for space.** The question drives the study of generators for read-once [branching programs](/branching-program/), starting with Nisan's generator and the generator of Impagliazzo, Nisan and Wigderson.
- **Streaming algorithms.** A streaming algorithm with small memory is a space-bounded machine, so Nisan's generator can replace stored random bits. Indyk used this to make sketches based on stable distributions use little space; the same idea applies to other linear sketches such as the [AMS sketch](/ams-sketch/).
- **Expanders and graph exploration.** Reingold's algorithm uses the zig-zag product, the same tool that gives explicit expanders for the [expander walk sampler](/expander-walk-sampler/). It also gives explicit universal exploration sequences, which visit every vertex of every graph of a given size.
- **Deterministic logspace algorithms.** After $\mathrm{SL} = \mathrm{L}$, many problems that reduce to undirected connectivity, such as testing whether a graph is bipartite or a forest, are known to be in L. Later work extends derandomization beyond connectivity, for example to approximate solutions of Laplacian systems of undirected graphs in nearly logarithmic space.
- **Related questions.** The question for time is BPP versus P, see [hardness versus randomness](/hardness-versus-randomness/). The question for nondeterministic space was settled in another way by the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/), which shows $\mathrm{NL} = \mathrm{coNL}$.

## References
