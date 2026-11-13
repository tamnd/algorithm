---
tag: XKXX36
kind: problem
slug: lights-out-puzzle
name: Lights Out puzzle
aliases:
- Lights Out
area: games-and-search/puzzles
level: core
summary: "Press cells of a grid of lights, each press toggling the cell and its neighbours, until all lights are off; a board is solvable exactly when a linear system over GF(2) is, and on 5 x 5 the rank is 23."
prereqs: [gaussian-elimination, adjacency-matrix]
see_also: [xor-sat, xor-gaussian-elimination, bitset-gaussian-elimination, gaussian-elimination-modular, rank, cellular-automaton, state-space, breadth-first-search]
sources:
  - paper: doi:10.1007/BF03023823
    title: "Klaus Sutner, Linear cellular automata and the Garden-of-Eden, The Mathematical Intelligencer 11(2), 1989"
    locator: "pp. 49-53; on every graph the configuration with all cells on can be turned off"
  - paper: doi:10.1080/0025570X.1998.11996658
    title: "Marlow Anderson and Todd Feil, Turning Lights Out with linear algebra, Mathematics Magazine 71(4), 1998"
    locator: "pp. 300-303; the 5 x 5 board, its rank 23 and its two null vectors"
---

Lights Out is a puzzle on a grid of lights in which pressing a cell toggles it and its orthogonal neighbours, and the goal is to turn every light off. Presses commute and two presses of the same cell cancel, so a solution is a set of cells, and a board $b$ is solvable exactly when the linear system $(A + I)x = b$ over GF(2) has a solution, where $A$ is the [adjacency matrix](/adjacency-matrix/) of the grid. [Gaussian elimination](/gaussian-elimination/) decides this in $O(N^3)$ bit operations for $N$ cells, and light chasing cuts the work to a system with one unknown per column. On the $5 \times 5$ board of the handheld game the matrix has rank 23, so exactly one board in four is solvable, each with 4 solutions.

## In plain words

Picture a five by five grid of buttons, each with a light. Pressing a button flips its own light and the lights directly above, below, left and right of it. You start with some lights on and want all of them off. Two facts make the puzzle simple. The order of the presses does not matter, and pressing a button twice is the same as not pressing it. So a solution is just a choice of which buttons to press once. Whether a light ends off depends only on whether an even or odd number of chosen buttons touch it. That turns the puzzle into a set of yes or no equations, one for each light, which a standard method solves at once. The method also shows that on the five by five board only a quarter of the starting patterns can be solved.

## Definition

**Instance.** A grid of $r \times c$ cells and a board $b \in \{0, 1\}^{rc}$, where $b_v = 1$ means that light $v$ is on.

**Moves.** Pressing cell $v$ toggles $v$ and every cell that shares a side with it.

**Problem.** Decide whether some sequence of presses turns all lights off, and if so find one, often one with the fewest presses.

**Linear form.** Let $N = rc$ and let $M = A + I$, where $A$ is the adjacency matrix of the $r \times c$ grid graph, so column $v$ of $M$ is the set of cells that a press of $v$ toggles. Over GF(2) a set of presses $x \in \{0, 1\}^N$ changes the board by $Mx$, independent of the order, since addition is commutative and $1 + 1 = 0$. So $x$ solves $b$ exactly when
$$Mx = b \pmod 2.$$
The same definition works on any graph, with $A$ its adjacency matrix; this is Sutner's $\sigma^+$ game.

## Variants

- **Other boards.** Rectangles, tori (where the edges wrap around), and arbitrary graphs all give a system $(A + I)x = b$.
- **The $\sigma$ game.** A press toggles only the neighbours, not the cell itself, so the matrix is $A$.
- **More colours.** Each light cycles through $k$ states, and a press adds 1 modulo $k$ to the cell and its neighbours. The system is then over $\mathbb{Z}_k$, solved by [modular Gaussian elimination](/gaussian-elimination-modular/) when $k$ is prime.
- **Fewest presses.** Among all solutions, find one with the fewest presses. All solutions form a coset $x_0 + \ker M$, so this is a minimum-weight search over $2^{\dim \ker M}$ candidates.
- **All on.** Start with every light on. Sutner proved that this board is solvable on every graph.

## Examples

**The $3 \times 3$ board, all lights on.** The matrix has full rank 9, so every board has exactly one solution. For all lights on it presses the four corners and the centre:

```
X . X
. X .
X . X
```

Each corner light is toggled by its own press only, each edge light by the two corner presses next to it and the centre press (three times), and the centre by itself.

**The $5 \times 5$ board.** The rank is 23 and the null space has the two quiet patterns, press sets that change nothing:

```
. X X X .      X . X . X
X . X . X      X . X . X
X X . X X      . . . . .
X . X . X      X . X . X
. X X X .      X . X . X
```

Since $M$ is symmetric, a board $b$ is solvable exactly when it meets each quiet pattern in an even number of cells. So $2^{23}$ of the $2^{25}$ boards are solvable, and each has $2^2 = 4$ solutions: one solution plus any sum of quiet patterns. The board with all lights on needs 15 presses at least.

**Null space dimensions** of the $n \times n$ board:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $n^2 - \operatorname{rank} M$ | 0 | 0 | 0 | 4 | 2 | 0 | 0 | 0 | 8 | 0 | 6 | 0 | 0 | 4 | 0 | 8 | 2 | 0 | 16 | 0 |

A dimension $d$ means that one board in $2^d$ is solvable and each solvable board has $2^d$ solutions; for $d = 0$ every board has exactly one.

## Known algorithms

- **Gaussian elimination over GF(2).** Reduce the $N \times N$ system $Mx = b$. With rows stored as bit sets, as in [bitset Gaussian elimination](/bitset-gaussian-elimination/), it costs $O(N^3 / w)$ word operations on a machine with $w$-bit words, which is $O(n^6 / w)$ for an $n \times n$ board. The same reduction gives the rank and a basis of $\ker M$, and [XOR Gaussian elimination](/xor-gaussian-elimination/) is the same procedure read as a solver for XOR clauses.
- **Light chasing.** Treat the presses in the first row as $c$ unknowns. For each row from the top, press the cell below every light that is still on; this clears all rows but the last, and every light of the last row becomes an affine function of the unknowns. Requiring the last row to be dark gives $c$ equations in $c$ unknowns. Tracking each light as a bit set of $c + 1$ bits, the chase costs $O(rc^2 / w)$ and the small system $O(c^3 / w)$, which is $O(n^3 / w)$ for an $n \times n$ board instead of $O(n^6 / w)$. A player uses the same method with a table of first-row patterns for the last row.
- **Fewest presses.** Take one solution $x_0$ and a basis $q_1, \dots, q_d$ of $\ker M$, and try all $2^d$ sums $x_0 + \sum_{i \in S} q_i$. On the $5 \times 5$ board that is 4 candidates.
- **Brute force.** Trying all $2^N$ press sets is only a check for tiny boards. A [breadth-first search](/breadth-first-search/) over the $2^N$ boards of the [state space](/state-space/) gives fewest presses too, but it ignores the linear structure and is far slower.

## Bounds

**Solvability.** Since $M$ is symmetric, $\operatorname{im} M = (\ker M^{\top})^{\perp} = (\ker M)^{\perp}$. So $b$ is solvable if and only if $b \cdot q = 0$ for every $q \in \ker M$, and then the solution set is a coset of $\ker M$, with $2^{N - \operatorname{rank} M}$ elements.

**All lights on (Sutner).** On every graph the board $\mathbf{1}$ with all lights on is solvable.

*Proof.* Let $M = A + I$ for a graph on $N$ vertices, and let $q \in \ker M$. Over GF(2),
$$0 = q^{\top} M q = \sum_{u, v} M_{uv} q_u q_v = \sum_v M_{vv} q_v + 2 \sum_{u < v} M_{uv} q_u q_v = \sum_v q_v = \mathbf{1} \cdot q,$$
because $M$ is symmetric with ones on the diagonal and $q_v^2 = q_v$. So $\mathbf{1}$ is orthogonal to $\ker M$, and by the solvability criterion it is in the image of $M$. $\square$

**Counts.** On a board whose null space has dimension $d$, exactly $2^{N - d}$ boards are solvable. A shortest solution has at most $N$ presses, and when $d = 0$ the unique solution is the shortest.

**Cost.** Elimination needs $\Theta(N^2)$ bits for the matrix; light chasing needs only $O(rc)$ bit sets of $c + 1$ bits, plus the $c \times c$ system.

## Reductions

- **To XOR-SAT.** The system $Mx = b$ is a set of XOR clauses, one per light, with the presses next to it as variables, so Lights Out is a special case of [XOR-SAT](/xor-sat/).
- **To linear algebra over a field.** Solvability, the number of solutions and the solvable boards follow from the [rank](/rank/) of $M$ and its null space.
- **Cellular automata.** A press pattern $x$ produces the board $Mx$, one step of the linear [cellular automaton](/cellular-automaton/) in which every cell becomes the sum of itself and its neighbours. A board is solvable exactly when it has a predecessor under this rule, which is the Garden-of-Eden question that Sutner studies.

## Applications

- Teaching linear algebra over GF(2): the puzzle shows rank, null space, the solvability criterion and the count of solutions on a concrete grid.
- A model of linear cellular automata and of the question which configurations have predecessors.
- A check for GF(2) solvers, with known ranks such as 23 for $5 \times 5$ and quiet patterns that can be verified by hand.

## References
