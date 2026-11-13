---
tag: BFC4VM
kind: problem
slug: tower-of-hanoi
name: Tower of Hanoi
aliases:
- Towers of Hanoi
- Hanoi puzzle
area: games-and-search/puzzles
level: intro
summary: "Move a tower of n discs from one of three pegs to another, one disc at a time and never a larger disc on a smaller one; the unique shortest solution has 2^n - 1 moves."
prereqs: [recursion, induction]
see_also: [frame-stewart-algorithm, recurrence-relation, ruler-sequence, binary-reflected-gray-code, trailing-zero-count, state-space, breadth-first-search, strips-plan-existence-pspace-complete]
sources:
  - book: isbn:9783319737782
    title: "Andreas M. Hinz, Sandi Klavžar and Ciril Petr, The Tower of Hanoi: Myths and Maths, second edition, Birkhäuser, 2018"
    locator: "Chapter 0 (history, pp. 1-69), Chapter 2 (the classical puzzle, pp. 93-163), Chapter 5 (more pegs, pp. 207-282)"
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: "Section 1.1, The Tower of Hanoi, and the exercises of Chapter 1"
---

The Tower of Hanoi is the puzzle of moving a tower of $n$ discs of different sizes from one of three pegs to another, one disc at a time, so that a disc never lies on a smaller disc. The shortest solution has $2^n - 1$ moves and is unique, and it comes from a three-line [recursion](/recursion/). Édouard Lucas published the puzzle in 1883. Its state space has $3^n$ states and is a standard example of an exponentially long optimal solution; the version with four or more pegs is the subject of the [Frame-Stewart algorithm](/frame-stewart-algorithm/).

## In plain words

Three pegs stand in a row. On the first peg sit discs that get smaller toward the top. You must rebuild the whole tower on the last peg. You may lift only the top disc of a peg, and you may never put a disc on a smaller one. The trick is to think about the largest disc. It can move only when every other disc is out of the way, stacked on the middle peg. So you first move the smaller tower to the middle peg, then move the largest disc, then move the smaller tower on top of it. Each smaller tower is the same puzzle with one disc fewer. Each new disc doubles the work and adds one move, so ten discs need more than a thousand moves and sixty-four discs need more moves than anyone could ever make.

## Definition

**Instance.** An integer $n \ge 0$ and three pegs $0, 1, 2$. The discs are $1, \dots, n$, numbered from the smallest.

**States.** A state gives the peg of each disc. On each peg the discs lie in order of size, so the map from discs to pegs fixes the state, and there are exactly $3^n$ states. A *perfect* state has all discs on one peg.

**Moves.** A move takes the top (smallest) disc $d$ of a peg $a$ to a peg $b \ne a$ whose discs are all larger than $d$.

**Problem.** Find a shortest sequence of moves from the perfect state on peg 0 to the perfect state on peg 2. The general problem asks for a shortest sequence between two given states.

**The Hanoi graph.** Its vertices are the $3^n$ states and its edges are the moves (a move can be undone, so the graph is undirected). The smallest disc can always move to either other peg, and in a state that is not perfect exactly one other move exists, so the three perfect states have degree 2 and all other states have degree 3. The graph has $(3^{n+1} - 3)/2$ edges.

## Variants

- **More pegs.** With $p \ge 4$ pegs the shortest solution is much shorter. The [Frame-Stewart algorithm](/frame-stewart-algorithm/) is optimal for 4 pegs, and for 5 or more pegs its optimality is open.
- **Arbitrary start and goal.** The start or the goal is any of the $3^n$ states. From any state to a perfect state the shortest solution is unique and has at most $2^n - 1$ moves.
- **Linear Hanoi.** The pegs stand in a line and a disc may move only to a neighbouring peg. Moving the tower from one end to the other then takes $3^n - 1$ moves, and the solution passes through every one of the $3^n$ states.
- **Cyclic Hanoi.** Discs may move only clockwise around the three pegs. The optimal counts satisfy a pair of coupled recurrences and grow like $(1 + \sqrt{3})^n$ (Concrete Mathematics, exercises of Chapter 1).
- **Other rules.** Coloured discs, discs of equal size, and the Tower of London puzzle used in psychology are covered in Chapters 6 to 8 of Hinz, Klavžar and Petr.

## Examples

**Three discs.** The unique shortest solution has 7 moves. With the pegs called A, B and C, it is: disc 1 A to C, disc 2 A to B, disc 1 C to B, disc 3 A to C, disc 1 B to A, disc 2 B to C, disc 1 A to C. The discs moved form the sequence 1, 2, 1, 3, 1, 2, 1.

**Move counts.**

| $n$ | 1 | 2 | 3 | 4 | 5 | 8 | 10 | 64 |
|---|---|---|---|---|---|---|---|---|
| shortest solution $2^n - 1$ | 1 | 3 | 7 | 15 | 31 | 255 | 1023 | 18,446,744,073,709,551,615 |
| states $3^n$ | 3 | 9 | 27 | 81 | 243 | 6561 | 59,049 | $\approx 3.4 \times 10^{30}$ |

At one move per second, 64 discs take about $5.85 \times 10^{11}$ years.

**A distance from a mixed state.** Take $n = 3$ with disc 3 on peg 0, disc 2 on peg 2 and disc 1 on peg 1, and the goal "all on peg 2". Disc 3 is not on peg 2, so it must move once, onto peg 2. That move and the later transfer of discs 1 and 2 onto it cost $1 + 3 = 2^2 = 4$ moves, and before that move discs 1 and 2 must gather on peg 1. Disc 2 is not on peg 1, so in the same way it costs $2^1 = 2$, and disc 1 must first go to peg 0. Disc 1 is on peg 1, so it costs $2^0 = 1$. The distance is $4 + 2 + 1 = 7$, as far as a state can be from a perfect state.

## Known algorithms

- **Recursion.** Move the top $n - 1$ discs to the spare peg, move disc $n$, move the $n - 1$ discs onto it. It makes $2^n - 1$ moves; the recursion depth is $n$, and with an explicit stack the extra memory is $O(n)$.
- **Iterative rule.** On odd-numbered moves, move disc 1 one step around a fixed cycle: $0 \to 2 \to 1 \to 0$ if $n$ is odd and $0 \to 1 \to 2 \to 0$ if $n$ is even. On even-numbered moves, make the only legal move that does not use disc 1. The program needs no stack, only the three pegs.
- **Direct formula for move $k$.** Move $k$ (for $1 \le k \le 2^n - 1$) moves disc $\rho(k) + 1$, where $\rho(k)$ is the number of trailing zero bits of $k$ (the [ruler sequence](/ruler-sequence/), computed with a [trailing zero count](/trailing-zero-count/)). This is the same index that the [binary reflected Gray code](/binary-reflected-gray-code/) changes at step $k$. Disc $d$ always moves around the same cycle: $0 \to 2 \to 1 \to 0$ when $n - d$ is even and $0 \to 1 \to 2 \to 0$ when $n - d$ is odd, and before move $k$ it has moved $\lfloor (k + 2^{d-1})/2^d \rfloor$ times. So both move $k$ and the state after $k$ moves cost $O(n)$ bit operations, with no simulation.
- **Distance to a perfect state.** Go from the largest disc to the smallest with a goal peg $g$, at first the target. If disc $d$ is on $g$, it costs nothing. Otherwise it costs $2^{d-1}$, and the goal for the smaller discs becomes the third peg, the one that is neither the peg of $d$ nor $g$. The sum is the exact distance, in $O(n)$ time, and playing the choices gives the unique shortest path.
- **Search.** A [breadth-first search](/breadth-first-search/) over the [implicit graph](/implicit-graph/) of $3^n$ states finds shortest paths between any two states. It is practical only for small $n$, but it is the standard check for the formulas above. For four pegs, large disk-based searches confirmed the [Frame-Stewart](/frame-stewart-algorithm/) numbers for up to 30 discs.

## Bounds

**Theorem.** For every $n \ge 0$, every solution moves the tower of $n$ discs from one peg to another in at least $2^n - 1$ moves, and exactly one solution has $2^n - 1$ moves.

*Proof.* Induction on $n$. For $n = 0$ the empty sequence is the only shortest solution. Let $n \ge 1$, let the tower go from peg $a$ to peg $b$, and let $e$ be the third peg. Disc $n$ must move at least once. At its first move, from $a$ to some peg $c$, disc $n$ is alone on $a$ and peg $c$ holds no smaller disc, so discs $1, \dots, n - 1$ form a tower on the third peg other than $a$ and $c$. The moves before this move do not move disc $n$, which lies at the bottom of peg $a$ and does not restrict the smaller discs, so they move a tower of $n - 1$ discs from $a$ to another peg; by the induction hypothesis they are at least $2^{n-1} - 1$ moves. In the same way, at the last move of disc $n$, onto $b$, the discs $1, \dots, n - 1$ form a tower on a peg other than $b$, and the moves after it take this tower onto $b$, which is at least $2^{n-1} - 1$ moves. The moves before the first move of disc $n$ and after its last move are disjoint, so a solution has at least $2(2^{n-1} - 1) + m$ moves, where $m \ge 1$ is the number of moves of disc $n$. This is at least $2^n - 1$.

A solution with exactly $2^n - 1$ moves has $m = 1$, so disc $n$ moves once, from $a$ to $b$, and the smaller tower is on $e$ at that time. Both other parts have exactly $2^{n-1} - 1$ moves, so each is the shortest way to move a tower of $n - 1$ discs (from $a$ to $e$, and from $e$ to $b$), and each is unique by the induction hypothesis. The recursion gives a solution with $T(n) = 2T(n - 1) + 1$ moves, and $T(n) = 2^n - 1$ (see [recurrence relation](/recurrence-relation/)). $\square$

**Consequences.**

- In the shortest solution disc $d$ moves exactly $2^{n-d}$ times.
- The distance from the perfect state on one peg to the perfect state on another is $2^n - 1$, and no state is farther from a perfect state; the diameter of the Hanoi graph is $2^n - 1$.
- Any algorithm that lists the moves takes $\Omega(2^n)$ time, because the output has $2^n - 1$ moves. Move $k$ alone costs $O(n)$.

## Reductions

- **Planning.** The puzzle is a [STRIPS](/strips/) instance of size polynomial in $n$ whose shortest plan has $2^n - 1$ steps. It is the standard witness that a plan can be exponentially longer than its instance, which is why a plan is not a polynomial certificate and why [STRIPS plan existence](/strips-plan-existence-pspace-complete/) is studied in PSPACE.
- **Gray codes.** The sequence of discs moved equals the sequence of bits flipped by the binary reflected Gray code, so a Gray code listing and a Hanoi solution can be read off each other (see [Gray code](/gray-code/)).
- **Counting with binary.** Step $k$ moves disc $d$ exactly when the [binary counter increment](/binary-counter-increment/) from $k - 1$ to $k$ turns bit $d - 1$ from 0 to 1.

## Applications

- Teaching [recursion](/recursion/), [induction](/induction/) and [recurrence relations](/recurrence-relation/), where it is the standard first example.
- A benchmark for search and planning: the four-peg version with a [pattern database](/pattern-database/) heuristic and disk-based [breadth-first search](/breadth-first-search/) has been a test problem for large search.
- A rotation scheme for backups: on day $k$ use the backup set $\rho(k) + 1$, so set 1 is overwritten every second day, set 2 every fourth day, and so on.

## References
