---
tag: G1R5TT
kind: theorem
slug: rubinstein-approximate-nash-lower-bound
name: Rubinstein's lower bound for approximate Nash
aliases:
- Rubinstein's theorem on approximate Nash
area: algorithmic-game-theory/computing-equilibria
level: research
summary: "Under the exponential time hypothesis for PPAD, an epsilon-Nash equilibrium of an n x n bimatrix game, for some constant epsilon, needs time n^(log^(1-o(1)) n)."
prereqs: [ppad, end-of-the-line-problem, epsilon-nash-equilibrium, bimatrix-game, lipton-markakis-mehta-algorithm, quasi-polynomial-time]
see_also: [ppad-completeness-of-nash, dmp-half-approximate-nash, hardness-of-optimal-nash-equilibria, brouwer-fixed-point-theorem, gap-eth, pcp-theorem, query-complexity, nash-equilibrium-computation]
sources:
  - paper: doi:10.1109/FOCS.2016.35
    title: "Aviad Rubinstein, Settling the complexity of computing approximate two-player Nash equilibria, Proceedings of the 57th IEEE Symposium on Foundations of Computer Science (FOCS 2016), 258-265"
    locator: the main theorem, the exponential time hypothesis for PPAD, and the reduction through a Brouwer problem with error-correcting codes and birthday repetition
  - paper: doi:10.1145/779928.779933
    title: "Richard J. Lipton, Evangelos Markakis and Aranyak Mehta, Playing large games using simple strategies, Proceedings of the 4th ACM Conference on Electronic Commerce (EC 2003), 36-41"
    locator: the matching upper bound n^O(log n / epsilon^2)
  - paper: doi:10.1145/2591796.2591829
    title: "Yakov Babichenko, Query complexity of approximate Nash equilibria, Proceedings of the 46th ACM Symposium on Theory of Computing (STOC 2014)"
    locator: the exponential lower bound on payoff queries for games with many players and two actions, and the hard Brouwer functions that later reductions use
  - paper: doi:10.1145/3055399.3055407
    title: "Yakov Babichenko and Aviad Rubinstein, Communication complexity of approximate Nash equilibria, Proceedings of the 49th ACM Symposium on Theory of Computing (STOC 2017)"
    locator: the unconditional lower bounds on communication when each player knows only its own payoffs
---

The [Lipton-Markakis-Mehta algorithm](/lipton-markakis-mehta-algorithm/) finds an [epsilon-Nash equilibrium](/epsilon-nash-equilibrium/) of an $n \times n$ [bimatrix game](/bimatrix-game/) in time $n^{O(\log n / \varepsilon^2)}$, which is [quasi-polynomial](/quasi-polynomial-time/) for each constant $\varepsilon$. Rubinstein (2016) showed that this is close to the best possible: under an exponential time hypothesis for [PPAD](/ppad/), there is a constant $\varepsilon > 0$ for which every algorithm needs time $n^{\log^{1 - o(1)} n}$. So two-player games have no polynomial-time approximation scheme under this hypothesis, and constant approximation is a problem of quasi-polynomial complexity. The result is conditional, because it is not proved that P differs from PPAD.

## Statement

A bimatrix game $(A, B)$ has $n$ pure strategies for each player and payoffs in $[0, 1]$. A pair of mixed strategies $(x, y)$ is an $\varepsilon$-Nash equilibrium if $x^\top A y \ge e_i^\top A y - \varepsilon$ for every pure strategy $i$ of the row player and $x^\top B y \ge x^\top B e_j - \varepsilon$ for every pure strategy $j$ of the column player.

The [END OF THE LINE](/end-of-the-line-problem/) problem gives two circuits $S$ and $P$ of size $s$ on $\{0, 1\}^m$, with $m \le s$, and asks for an end of a line other than $0^m$.

**Exponential time hypothesis for PPAD (ETH for PPAD).** Every algorithm that solves END OF THE LINE on circuits of size $s$ needs time $2^{\tilde\Omega(s)}$, where $\tilde\Omega$ hides factors polylogarithmic in $s$.

**Theorem (Rubinstein 2016).** There is a constant $\varepsilon > 0$ such that, if ETH for PPAD holds, every algorithm that finds an $\varepsilon$-Nash equilibrium of $n \times n$ bimatrix games with payoffs in $[0, 1]$ needs time $n^{\log^{1 - o(1)} n}$.

The problem is in PPAD for every $\varepsilon$, and it is in the class [TFNP](/tfnp/) of total search problems. The theorem does not make it PPAD-complete for constant $\varepsilon$. If constant-$\varepsilon$ Nash were PPAD-complete under polynomial reductions, the LMM algorithm would solve every problem in PPAD in quasi-polynomial time, which contradicts ETH for PPAD.

## In plain words

For two-player games, a rough solution, where each player could gain only a small fixed amount by changing its play, can be found faster than an exact one. The known method checks all small mixes of moves, and its time grows a little faster than any polynomial. This theorem says that no method is much faster, if a natural belief is true: that following a long path in a huge graph needs almost brute-force time. The proof turns any such path puzzle into a game whose rough solutions show the end of the path. The game is only a little larger than needed, so a fast method for games would give a fast method for the puzzle.

## Proof

The full proof is in the FOCS paper. It reduces END OF THE LINE with circuits of size $s$ to an $\varepsilon$-Nash problem of size $n = 2^{\tilde O(\sqrt s)}$. Here are the three steps and the final count.

**Step 1: a robust Brouwer problem.** The first step reduces END OF THE LINE to finding an approximate fixed point of a map $f : [0, 1]^d \to [0, 1]^d$ with $d = O(s)$, where $f$ is Lipschitz and each coordinate of $f(x)$ can be computed from a few coordinates of $x$ and the circuits. The error is measured in the normalized Euclidean norm, $\|x - f(x)\|_2 / \sqrt d$, and the reduction is correct for a constant error. To make a constant error enough, the line of the instance is embedded in the cube with an error-correcting code of constant rate and constant relative distance. Points that encode a vertex of the graph are far apart, so a point with a constant error still determines one vertex. Far from the encoded line, $f$ moves every point by a constant amount toward a fixed direction. Along the line, $f$ moves points to the encoding of the next vertex. So a point that $f$ moves by less than $\varepsilon$ can only be near an end of the line. This is the same idea as the 3-dimensional embedding of [Daskalakis, Goldberg and Papadimitriou](/ppad-completeness-of-nash/), with the code in place of a thin tube. Earlier constructions of Hirsch, Papadimitriou and Vavasis and of Babichenko gave such maps for query lower bounds, and Rubinstein (2015) used them to prove that games with many players and 2 actions are PPAD-hard to solve for a constant $\varepsilon$.

**Step 2: an imitation game on blocks.** The second step makes a two-player game from $f$. Each player picks a set of about $\sqrt d$ coordinates from a fixed family of sets, together with values for these coordinates. The row player gains when its values are close to the values of the column player on the common coordinates. The column player gains when its values are close to the values of $f$ at the row player's point. This is an imitation game, as in the proof that Nash equilibria exist by fixed points. Two random sets of size $\sqrt d$ have a constant expected number of common coordinates, by the birthday paradox, so the players can compare their points without listing all $d$ coordinates. This technique is called birthday repetition, after its use by Aaronson, Impagliazzo and Moshkovitz for free games. In an $\varepsilon$-Nash equilibrium, the row player's values are close to a point $x$ and the column player's values are close to $f(x)$, and the imitation forces $f(x)$ to be close to $x$.

**Step 3: the size of the game.** A strategy is a set of $\sqrt d$ coordinates and a value from a constant-size grid for each, so the number of strategies is $n = 2^{\tilde O(\sqrt d)} = 2^{\tilde O(\sqrt s)}$. The payoffs are computed in time polynomial in $n$, and an $\varepsilon$-Nash equilibrium gives an end of the line in time polynomial in $n$.

**The count.** From $\log n = \tilde O(\sqrt s)$ we get $s = \tilde\Omega(\log^2 n)$. Suppose that some algorithm finds $\varepsilon$-Nash equilibria in time $n^{\log^{1 - \delta} n}$ for a constant $\delta > 0$. That is $2^{\log^{2 - \delta} n} = 2^{s^{1 - \delta / 2} \cdot \mathrm{polylog}(s)}$, which is $2^{o(s / \mathrm{polylog}(s))}$ and contradicts ETH for PPAD. So the time is $n^{\log^{1 - o(1)} n}$. $\square$

## Consequences

- **No PTAS.** Under ETH for PPAD, there is no polynomial-time approximation scheme for two-player Nash equilibria. Chen, Deng and Teng had already ruled out an FPTAS unless PPAD is in P ([PPAD-completeness of Nash](/ppad-completeness-of-nash/)).
- **LMM is nearly optimal.** For a small constant $\varepsilon$, the exponent $\log n$ of the LMM algorithm cannot be replaced by $\log^{1 - \delta} n$ for any constant $\delta > 0$.
- **Quasi-polynomial complexity.** Under these hypotheses, constant-$\varepsilon$ two-player Nash is neither in P nor PPAD-complete. Other problems have the same quasi-polynomial behavior, for example an approximate Nash equilibrium with near-optimal welfare ([hardness of optimal Nash equilibria](/hardness-of-optimal-nash-equilibria/)) and several problems studied under [Gap-ETH](/gap-eth/).
- **Communication and queries.** Babichenko (2014) proved that games with $k$ players and 2 actions each need $2^{\Omega(k)}$ payoff queries for a constant $\varepsilon$, without any hypothesis ([query complexity](/query-complexity/)). Babichenko and Rubinstein (2017) proved unconditional lower bounds on the communication needed, when each player knows only its own payoffs.

## Tightness

The lower bound matches the LMM upper bound $n^{O(\log n / \varepsilon^2)}$ up to the $o(1)$ in the exponent, for one small constant $\varepsilon$. The theorem does not give the best dependence on $\varepsilon$, and it does not say how small the constant must be. A preprint of Golowich (September 2026) claims the bound $n^{(\log n / \varepsilon^2)^{1 - o(1)}}$, under ETH for PPAD and a further "PCP for PPAD" conjecture, and it is not yet peer reviewed as of November 2026.

Polynomial-time algorithms reach constant values of $\varepsilon$: $1/2$ by the [DMP algorithm](/dmp-half-approximate-nash/), and $1/3 + \delta$ for every constant $\delta > 0$ by Deligkas, Fasoulakis and Markakis (2022). The largest $\varepsilon$ for which the quasi-polynomial lower bound holds, and the smallest $\varepsilon$ that has a polynomial-time algorithm, are open problems as of November 2026. ETH for PPAD itself is a hypothesis, and the question whether P equals PPAD is open as of November 2026. The evidence for the hypothesis is that black-box algorithms for END OF THE LINE and for Brouwer fixed points need exponentially many queries (Hirsch, Papadimitriou and Vavasis 1989), and that PPAD contains problems that are hard under cryptographic assumptions.

## History

Lipton, Markakis and Mehta gave the quasi-polynomial algorithm in 2003. After the PPAD-completeness of exact two-player Nash in 2006, the main open question was whether a PTAS exists. Daskalakis and Papadimitriou showed in 2009 that oblivious algorithms, which pick a distribution over supports without looking at the game, cannot be faster than quasi-polynomial. Hazan and Krauthgamer (2011) and Braverman, Ko and Weinstein (2015) gave quasi-polynomial lower bounds for the best equilibrium. Babichenko (2014) gave the query lower bound for many players, and Rubinstein (2015) proved PPAD-hardness of constant approximation for many players. Rubinstein then proved the two-player lower bound, posted in June 2016 and presented at FOCS 2016.

## References
