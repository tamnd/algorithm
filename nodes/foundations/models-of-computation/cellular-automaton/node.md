---
tag: ER9MYC
kind: model
slug: cellular-automaton
name: Cellular automaton
aliases:
- cellular automata
- CA
area: foundations/models-of-computation
level: advanced
summary: Grid of cells updated in parallel by a local rule; a model of computation and of complex dynamics.
prereqs: [turing-machine]
see_also: [register-machine, church-turing-thesis, halting-problem, boolean-circuit, multitape-turing-machine, turing-completeness, reversible-computation]
sources:
  - title: "Jarkko Kari, Theory of cellular automata: a survey, Theoretical Computer Science 334(1-3) (2005), 3 to 33, doi:10.1016/j.tcs.2004.11.021"
    locator: pp. 3 to 33 (definitions, the Garden of Eden theorem, the Curtis-Hedlund-Lyndon theorem, decision problems)
  - title: "Edward F. Moore, Machine models of self-reproduction, Proceedings of Symposia in Applied Mathematics 14 (1962), 17 to 33, doi:10.1090/psapm/014/9961"
    locator: pp. 17 to 33 (Garden of Eden configurations exist when there are twins)
  - title: "John Myhill, The converse of Moore's Garden-of-Eden theorem, Proceedings of the American Mathematical Society 14(4) (1963), 685 to 686, doi:10.1090/S0002-9939-1963-0155764-9"
    locator: pp. 685 to 686 (the converse)
  - title: "Gustav A. Hedlund, Endomorphisms and automorphisms of the shift dynamical system, Mathematical Systems Theory 3(4) (1969), 320 to 375, doi:10.1007/BF01691062"
    locator: pp. 320 to 375 (the shift-commuting continuous maps; the inverse of an injective map)
  - title: "Daniel Richardson, Tessellations with local transformations, Journal of Computer and System Sciences 6 (1972), 373 to 388, doi:10.1016/S0022-0000(72)80009-6"
    locator: pp. 373 to 388 (an injective global map has an inverse that is a cellular automaton, in every dimension)
  - title: "S. Amoroso and Y. N. Patt, Decision procedures for surjectivity and injectivity of parallel maps for tessellation structures, Journal of Computer and System Sciences 6(5) (1972), 448 to 464, doi:10.1016/S0022-0000(72)80013-8"
    locator: pp. 448 to 464
  - title: "Jarkko Kari, Reversibility and surjectivity problems of cellular automata, Journal of Computer and System Sciences 48(1) (1994), 149 to 182, doi:10.1016/S0022-0000(05)80025-X"
    locator: pp. 149 to 182 (undecidability in two dimensions)
  - title: "Matthew Cook, Universality in elementary cellular automata, Complex Systems 15(1) (2004), 1 to 40, doi:10.25088/ComplexSystems.15.1.1"
    locator: pp. 1 to 40
  - title: "Stephen Wolfram, Statistical mechanics of cellular automata, Reviews of Modern Physics 55(3) (1983), 601 to 644, doi:10.1103/RevModPhys.55.601"
    locator: pp. 601 to 644 (the elementary rules and their numbering)
  - title: "Stephen Wolfram, Universality and complexity in cellular automata, Physica D 10(1-2) (1984), 1 to 35, doi:10.1016/0167-2789(84)90245-8"
    locator: pp. 1 to 35 (the four classes of behavior)
  - title: "John von Neumann, Theory of Self-Reproducing Automata, edited and completed by Arthur W. Burks, University of Illinois Press, 1966"
    locator: Part II, The Theory of Automata, Construction, Reproduction, Homogeneity
  - title: "Martin Gardner, Mathematical Games, Scientific American 223(4), October 1970, doi:10.1038/scientificamerican1070-120"
    locator: pp. 120 to 123, the column that describes Life
  - title: "Elwyn R. Berlekamp, John H. Conway and Richard K. Guy, Winning Ways for your Mathematical Plays, volume 2, Academic Press, 1982"
    locator: Chapter 25, What is Life?
---

A cellular automaton is a model of computation with a grid of cells, each in one of finitely many states, that all change at the same time by the same local rule. The new state of a cell depends only on the states of the cell and of its neighbors. Simple rules give complex behavior: the one-dimensional rule with the Wolfram number 110 is [Turing complete](/turing-completeness/) from an infinite, ultimately periodic starting configuration, and so is Conway's Game of Life in two dimensions. Conway devised Life in 1970, and Gardner described it in Scientific American that year. The model counts parallel time, and it has no tape, head or program apart from the rule.

## The machine

A cellular automaton has four parts:

- a lattice of cells, which is $\mathbb{Z}^d$ for a dimension $d \ge 1$;
- a finite set $S$ of cell states;
- a finite neighborhood $N \subseteq \mathbb{Z}^d$;
- a local rule $f : S^{N} \to S$.

A **configuration** is a map $c : \mathbb{Z}^d \to S$. The **global map** $F$ takes $c$ to the configuration $F(c)$ with

$$
F(c)(x) = f\big( (c(x + v))_{v \in N} \big) \qquad \text{for all } x \in \mathbb{Z}^d .
$$

The **radius** of the automaton is $r = \max_{v \in N} \|v\|_\infty$, the largest distance in any coordinate from a cell to a neighbor. In two dimensions the two common neighborhoods are the von Neumann neighborhood (the cell and its 4 orthogonal neighbors) and the Moore neighborhood (the cell and all 8 surrounding cells). Both have radius 1.

One **step** applies $F$: all cells read their neighbors in the old configuration and change together. A **computation** is the sequence $c, F(c), F^2(c), \ldots$ that starts from a given configuration. A computation has no halting state in the model itself. A machine-like use of the model fixes an input pattern, a rule for the output (for example the state of one cell at some time) and a halting convention.

**Quiescent state and finite configurations.** A state $q$ is **quiescent** if $f$ maps the all-$q$ neighborhood to $q$. Then the all-$q$ configuration does not change. A configuration is **finite** if only finitely many cells are not in the state $q$. When $q$ is quiescent, $F$ maps finite configurations to finite configurations. Without a quiescent state this fails: an elementary rule with $f(0, 0, 0) = 1$ turns the all-$0$ configuration into the all-$1$ configuration.

**Elementary automata.** A one-dimensional elementary automaton has $d = 1$, $S = \{0, 1\}$ and $N = \{-1, 0, 1\}$, so $f$ maps a triple $(a, b, c)$ (left, center, right) to a bit. There are $2^{8} = 256$ such rules. The **Wolfram number** of $f$ (the numbering is from Wolfram, 1983) is

$$
\sum_{(a,b,c) \in \{0,1\}^3} f(a, b, c)\, 2^{4a + 2b + c} \in \{0, \ldots, 255\}.
$$

Written in binary, the number lists the outputs for the triples $111, 110, 101, 100, 011, 010, 001, 000$ in this order, from the high bit to the low bit. Rule 110 is $110 = 01101110_2$, so

| triple | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|---|---|---|---|---|---|---|---|---|
| new state | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |

The new state is $1$ exactly when the center or the right cell is $1$ and the triple is not $111$. As a formula, $f(a, b, c) = (b \lor c) \land \lnot (a \land b \land c)$. Since $f(0,0,0) = 0$, the state $0$ is quiescent.

**A worked row.** Take the row $0010110111$, with the cell to the left and the cell to the right of the row held at $0$. The table gives the new state of each cell from its triple.

| cell | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| triple | 000 | 001 | 010 | 101 | 011 | 110 | 101 | 011 | 111 | 110 |
| new state | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |

The new row is $0111111101$. Starting from a single $1$ on a background of $0$, the pattern grows to the left by one cell in each step, since the triple $001$ gives $1$. It never grows to the right, since the triple $100$ gives $0$. These are the first nine rows, in 16 cells, with $\#$ for $1$ and $.$ for $0$:

```
...............#
..............##
.............###
............##.#
...........#####
..........##...#
.........###..##
........##.#.###
.......#######.#
```

Rule 90 is another case. Its rule is $f(a, b, c) = a \oplus c$. This is linear over the two-element field, so for every $t \ge 0$ the state of cell $x$ at time $t$ is the sum modulo 2 of $c(x + t - 2j)$ over the $j$ in $\{0, \ldots, t\}$ for which the binomial coefficient $\binom{t}{j}$ is odd. This gives the state at time $t$ directly, without the $t$ steps in between.

**The Game of Life.** The Game of Life of Conway has $d = 2$, $S = \{0, 1\}$ (dead and alive) and the Moore neighborhood. A live cell stays alive if it has $2$ or $3$ live neighbors, and a dead cell becomes alive if it has exactly $3$ live neighbors. All other cells are dead in the next generation. This rule is called B3/S23. Three live cells in a row (the blinker) give a column of three cells after one step and the original row after two. The five cells $\{(1,0), (2,1), (0,2), (1,2), (2,2)\}$ (the glider) return to the same shape after four steps, moved by $(1, 1)$.

## What it counts

The **time** is the number of steps, which are parallel steps of the whole lattice. For a pattern that lives in a bounded region, the **space** is the number of cells of the region, and the **work** is the number of cell updates. These are different measures, and a bound must say which one it is.

On a fixed region of $w$ cells, for example a ring of $w$ cells (periodic boundary) or a row with fixed boundary cells, $t$ steps take $w t$ cell updates. On the infinite lattice the region can grow. Information moves by at most $r$ cells in each step, so in one dimension the state of a cell at time $t$ depends on at most $2rt + 1$ cells of the start, and a finite configuration whose non-quiescent cells fill a window of $w$ cells has, after $s$ steps, all its non-quiescent cells in a window of at most $w + 2rs$ cells. So $t$ steps take at most

$$
\sum_{s=0}^{t-1} (w + 2rs) = t w + r t (t - 1) = O(t (w + r t))
$$

cell updates. The quadratic term is real. Rule 110 from a single $1$ has $w = 1$ and grows by one cell in each step: after 40 steps the pattern spans 41 cells, so $t$ steps take $\Theta(t^2)$ updates.

Because all cells work in the same step, the model is a model of massive parallelism with local communication only.

## Relation to other models

A one-dimensional automaton simulates a [Turing machine](/turing-machine/) step for step. Let a cell hold a tape symbol, or a pair of the state and the symbol when the head is there, so that $S = \Gamma \cup (Q \times \Gamma)$ for the tape alphabet $\Gamma$ and the state set $Q$. The new state of a cell depends on the cell and its two neighbors: the cell takes the written symbol if it holds the head, and takes the head and the new state if a neighbor holds the head and moves toward it. So one step of the machine is one step of the automaton, and the radius is 1. Conversely, a [multitape Turing machine](/multitape-turing-machine/) simulates $t$ steps of a one-dimensional automaton from a finite configuration with a starting window of $w$ cells in $O(t (w + r t))$ steps, by one sweep over the current window for each step, with the bound of the previous section. The same holds for configurations that are periodic outside a finite window. So each model simulates the other: the automaton with no loss of time, and the Turing machine with a quadratic slowdown.

A [Boolean circuit](/boolean-circuit/) computes a function of a fixed input length with a fixed network of gates. Unrolling $t$ steps of an automaton on a fixed region of $w$ cells gives a circuit of depth $O(t)$ and size $O(wt)$, where the constants depend on $|S|$ and the rule $f$, since each cell update is a constant-size subcircuit. The [register machine](/register-machine/) builds a computer from a program and a few counters, and the automaton builds it from a lattice of identical finite machines.

A cellular automaton is **reversible** when its global map is a bijection whose inverse is again the global map of a cellular automaton. Reversible automata are a model of [reversible computation](/reversible-computation/).

## Known results in the model

- **The origin.** Von Neumann, with Ulam, introduced cellular automata in the 1940s. His 29-state automaton in two dimensions was built for self-reproduction and universal construction. The account is Part II of von Neumann's Theory of Self-Reproducing Automata, edited by Burks (1966).
- **The global map is characterized topologically (Hedlund 1969).** Give $S^{\mathbb{Z}^d}$ the product topology. The global maps of the cellular automata are exactly the continuous maps that commute with the shifts. This is the Curtis-Hedlund-Lyndon theorem; Hedlund's paper proves it and credits Curtis and Lyndon.
- **Injective means reversible (Hedlund 1969, Richardson 1972).** If the global map is injective, it is bijective and its inverse is the global map of a cellular automaton. So for cellular automata injectivity and reversibility are the same property.
- **Garden of Eden theorem (Moore 1962, Myhill 1963).** Call $F$ **pre-injective** if no two distinct configurations that differ in only finitely many cells have the same image. Then $F$ is surjective if and only if it is pre-injective. When there is a quiescent state, this says: a **Garden of Eden** configuration (one with no preimage) exists exactly when there are *twins*, two different finite configurations with the same image. Moore proved that twins give a Garden of Eden, and Myhill proved the converse. For Rule 110, the finite configurations $1011$ and $1101$ (on a background of $0$, starting at the same cell) have the same image, $11111$ starting one cell to the left. So Rule 110 is not surjective. Indeed, the word $01010$ is the shortest word that appears in no image. Rule 90 shows that pre-injective is weaker than injective: it is surjective, but it maps both the all-$0$ and the all-$1$ configurations to the all-$0$ configuration.
- **Decision problems.** Injectivity and surjectivity are decidable in one dimension (Amoroso and Patt, 1972). Both are undecidable in two dimensions (Kari, 1990 for reversibility, and 1994 for both). Kari's survey treats these results.
- **Rule 110 is Turing complete (Cook, 2004).** Matthew Cook proved that Rule 110 can emulate any cyclic tag system, and cyclic tag systems can emulate Turing machines. The proof builds gliders on a periodic background pattern and uses collisions of the gliders as the computation. The initial configuration is infinite and ultimately periodic, not a finite pattern on a blank background. As a consequence, some reachability questions about Rule 110 from ultimately periodic configurations, such as whether a given pattern ever appears, are undecidable, by the [halting problem](/halting-problem/).
- **The Game of Life is universal.** Berlekamp, Conway and Guy showed in Winning Ways (1982) how to build logic gates and memory from gliders, glider guns and eaters in Life. So Life simulates every Turing machine, and questions about its long-term behavior are as hard as the halting problem.
- **Four classes of behavior (Wolfram 1984).** Wolfram sorted the rules by their behavior from random starting configurations: class I goes to a uniform configuration, class II to stable or periodic structures, class III to chaotic patterns, and class IV to complex localized structures that move and interact. Rule 204, which copies each cell, is in class II, Rule 30 is in class III, and Rule 110 is in class IV. The classes describe observed behavior; they are not a formal definition.
- **Not all rules are rich.** Rule 204 is the identity, and Rule 90 is linear, so its state at any time follows from the formula above. The [Church-Turing thesis](/church-turing-thesis/) is consistent with all of this, since no automaton computes more than a Turing machine.

## References
