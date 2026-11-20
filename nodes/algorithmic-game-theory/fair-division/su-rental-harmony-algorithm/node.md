---
tag: QR1JRG
kind: algorithm
slug: su-rental-harmony-algorithm
name: Su's algorithm for rental harmony
aliases:
- Sperner rent division
area: algorithmic-game-theory/fair-division
level: advanced
summary: "Finds an approximately envy-free rent division by following doors through a triangulated simplex of price vectors, as in the path-following proof of Sperner's lemma."
solves: [rental-harmony]
model: real-ram
complexity:
  vars: {n: the number of rooms and tenants, N: the grid size}
  time: {worst: O(n^2 N^(n-1) + 4^n n! n^2)}
  space: {extra: O(n N^(n-1) + n 4^n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [envy-freeness, rental-harmony, sperner-lemma]
see_also: [scarf-algorithm, lemke-howson-algorithm, end-of-the-line-problem, stromquist-moving-knife, chore-division, ppad, cake-cutting-problem]
sources:
  - paper: "Francis Edward Su, Rental harmony: Sperner's lemma in fair division, American Mathematical Monthly 106(10) (1999), 930-942"
    locator: Sections 3 to 5 (owner labels and the trap-door algorithm for cake), Section 7 (rental harmony and the dual Sperner lemma), Section 8 (the weaker miserly condition)
  - paper: "Harold W. Kuhn, Simplicial approximation of fixed points, Proceedings of the National Academy of Sciences of the USA 61 (1968)"
    locator: the triangulation of the simplex by the cells of a cube grid
  - paper: "Michael J. Todd, The Computation of Fixed Points and Applications, Lecture Notes in Economics and Mathematical Systems, Springer, 1976"
    locator: triangulations and path following for fixed points, as Su cites it for other triangulations
---

Su's algorithm for rental harmony finds rooms and prices for $n$ tenants that share a fixed rent, so that each tenant almost prefers its own room at its price to every other room. It covers the simplex of all ways to split the rent with a grid of small cells, gives each grid point an owner among the tenants, asks the owner which room it would choose at those prices, and walks from cell to cell through "doors" until it finds a cell where the $n$ owners choose $n$ different rooms. The [rental harmony](/rental-harmony/) page states the problem and its existence theorem; this page is the procedure that finds an approximate solution with a finite number of questions. It differs from [Sperner's lemma](/sperner-lemma/) itself in its labels: the room labels are not a Sperner labeling, because a tenant takes a free room, so the walk starts at a door on the boundary next to the corner where one room costs all the rent.

## In plain words

Housemates must split the rent of a house and pick rooms. A helper writes down many price lists, each a small step from its neighbours. Each list gets one housemate as its owner, arranged so that every small group of neighbouring lists has every housemate as an owner once.

The helper starts at a group of lists near the edge, where some rooms are free. For each list it asks the owner: "Which room would you take at these prices?" Then it moves to a neighbouring group, one new list at a time, by a fixed rule that never goes back. It stops at a group where every owner picks a different room. Each housemate gets the room it picked, and the final prices are the average of the lists in that group. They are so close to each list that nobody cares about the difference.

## The problem

There are $n$ rooms and $n$ tenants, numbered $0$ to $n - 1$, and a total rent $R$. A price vector is $p \ge 0$ with $\sum_j p_j = R$. At each price vector, each tenant chooses one room. The tenants are *miserly*: at a price vector with a free room ($p_j = 0$), a tenant chooses a free room. The goal is a permutation $r$ of the rooms and a price vector $q$ such that, for each tenant $i$, room $r_i$ is the choice of tenant $i$ at a price vector within $R/N$ of $q$ in every room. For tenants whose choices change only a little when prices change a little, this is an approximately envy-free rent division.

## The algorithm

Fix a grid size $N \ge n$. A grid point is an integer vector $s$ with $0 \le s_0 \le \dots \le s_{n-2} \le N$, and its prices are $p_j = R x_j / N$ with $x_0 = s_0$, $x_j = s_j - s_{j-1}$ and $x_{n-1} = N - s_{n-2}$. A cell is a set of $n$ grid points $y^0, y^1, \dots, y^{n-1}$ with $y^t = y^{t-1} + e_{\pi_t}$ for a permutation $\pi$; these cells triangulate the region. The owner of $s$ is the tenant $(s_0 + \dots + s_{n-2}) \bmod n$, and the label of $s$ is the room its owner chooses at the prices of $s$. A door is a face of $n - 1$ points of a cell whose labels are exactly the rooms $0, \dots, n - 2$.

```pseudo id=main
SU-RENTAL-HARMONY(n, R, N, tenants)
L1  label(s) ← the room that the owner of s chooses at the prices of s     ▷ ask each point at most once
L2  for each door D on the boundary, in its cell C:
L3      loop
L4          v_0, …, v_{n-1} ← the vertices of C, with their labels
L5          if the labels are all n rooms then
L6              give each owner the label of its vertex
L7              return the rooms and the average of the vertex prices
L8          u ← the vertex of the entry door with the same label as the new vertex
L9          C' ← the other cell that holds the face without u; if C' is outside the region, go to the next door
L10         C ← C', and its new vertex is the one not in that face
```

Lines L9 and L10 use the pivot rules of the Freudenthal (Kuhn) triangulation: removing an inner vertex swaps two neighbours in $\pi$, and removing the first or the last vertex shifts the base point and rotates $\pi$. With miserly tenants, every boundary door lies in a cell whose base point has all coordinates at most $n - 2$, so line L2 searches a part of the region whose size does not depend on $N$.

## Example

Take $n = 3$, $R = 900$ and $N = 6$, so prices move in steps of $150$. In its own eyes, tenant 0 pays half the price for room 0, tenant 1 pays half the price for room 1, and tenant 2 pays the real prices; each picks the room that costs it least, with ties going to the smaller room. A free room costs nothing, so the tenants are miserly. The walk starts at the only boundary door, the face with prices $(0, 0, 900)$ and $(150, 0, 750)$. Each row gives the three vertices of a cell as prices (owner, label):

| Step | Vertex 1 | Vertex 2 | Vertex 3 |
|---|---|---|---|
| 1 | (0, 0, 900) (0, 0) | (0, 150, 750) (1, 0) | (150, 0, 750) (2, 1) |
| 2 | (0, 150, 750) (1, 0) | (150, 0, 750) (2, 1) | (150, 150, 600) (0, 0) |
| 3 | (150, 0, 750) (2, 1) | (150, 150, 600) (0, 0) | (300, 0, 600) (1, 1) |
| 4 | (150, 150, 600) (0, 0) | (300, 0, 600) (1, 1) | (300, 150, 450) (2, 1) |
| 5 | (150, 150, 600) (0, 0) | (150, 300, 450) (1, 0) | (300, 150, 450) (2, 1) |
| 6 | (150, 300, 450) (1, 0) | (300, 150, 450) (2, 1) | (300, 300, 300) (0, 0) |
| 7 | (300, 150, 450) (2, 1) | (300, 300, 300) (0, 0) | (450, 150, 300) (1, 1) |
| 8 | (300, 300, 300) (0, 0) | (450, 150, 300) (1, 1) | (450, 300, 150) (2, 2) |

Each cell after the first shares two vertices with the cell before it, and those two vertices have the labels 0 and 1. The cell of step 8 has the labels 0, 1 and 2, so tenant 0 gets room 0, tenant 1 gets room 1 and tenant 2 gets room 2. The average of its three price vectors is $(400, 250, 250)$. At these prices tenant 0 pays $200$ for room 0 in its own eyes, against $250$ for each other room; tenant 1 pays $125$ for room 1, against $400$ and $250$; tenant 2 pays $250$ for room 2, which ties with room 1 and beats room 0. So in this example the result is exactly envy-free. The algorithm asked 11 questions, out of 28 grid points and 36 cells.

## Correctness

The $n$ vertices of a cell have coordinate sums that are $n$ consecutive integers, so they have $n$ different owners. If the labels are all $n$ rooms, line L6 gives each tenant one room and each room one tenant, and each tenant chose its room at the prices of its vertex. Within one cell each price varies by at most $R/N$, so the average price vector is within $R/N$ of every vertex price in every room.

A cell has two doors, or none, unless it is fully labeled, in which case it has one door. So the walk enters each cell through one door and leaves through the other, it never visits a cell twice, and it stops at a fully labeled cell or at another boundary door. For two and three rooms there is exactly one boundary door, so the walk always succeeds. For more rooms, the number of fully labeled cells and the number of boundary doors have the same parity, and Su proves with a dual form of Sperner's lemma, due to Scarf, that a fully labeled cell exists. The details, and the part of the argument that is only partly proved here, are in `proofs/correctness.md`.

## Complexity

The region has $N^{n-1}$ cells, and the walk visits each at most once. Each step costs $O(n^2)$ operations to build a cell and to compare labels, so the walk costs $O(n^2 N^{n-1})$ in the worst case, in the [real-RAM](/real-ram/) sense with one unit per question to a tenant. The search for boundary doors in line L2 looks at fewer than $4^n$ base points, $(n - 1)!$ cells for each, and $n$ faces for each cell, so it costs $O(4^n n! n^2)$, with no dependence on $N$.

The number of questions is at most the number of grid points, $\binom{N + n - 1}{n - 1}$, and usually far less, because only the points near the walk are asked. For a fixed number of tenants, halving the price step $R/N$ can multiply the worst case by $2^{n-1}$. Path following of this kind can take exponentially many steps in general; finding a fully labeled cell of a Sperner labeling given by a circuit is complete for the class [PPAD](/ppad/).

## Properties

- **Interactive.** It asks one tenant one question at a time and needs no utility numbers, only choices.
- **Approximate.** The price error is at most $R/N$ per room; it is not exactly envy-free in general.
- **Deterministic and simple to state.** Each step changes one vertex and asks at most one new question.
- **Owners, not tenants, label the cells.** Each tenant answers only at the points it owns.

## Variants and improvements

- **Barycentric subdivision.** Su describes the labeling on an iterated barycentric subdivision of the price simplex and notes that other triangulations, with better convergence, can be used. The implementation uses the Freudenthal triangulation, whose cells are easy to step through.
- **The weaker miserly condition.** Su shows that it is enough that a tenant never picks the most expensive room when some room is free.
- **Cake and chores.** The same trap-door walk with owner labels finds an approximately envy-free division of a cake into intervals, and, by treating rent as a burden, an approximately envy-free [chore division](/chore-division/).
- **Exact rent division with money.** If each tenant has a value for each room and its utility is value minus price, an exactly envy-free division can be found in polynomial time by a matching and a linear program. The rental harmony page describes this model.

## When to use it

Use it when the tenants can answer only "which room would you take at these prices?", when their preferences need not be quasi-linear, and when an error of a small amount of rent per room is acceptable. With quasi-linear values, solve the problem exactly with a matching and a linear program instead.

## Pitfalls

- **Tenants who are not miserly.** If a tenant picks a room with a positive price when another room is free, there can be no boundary door near the expensive corner, and the walk may not start or may fail.
- **A grid that is too coarse.** The guarantee is only within $R/N$; with a small $N$ the answer can leave real envy.
- **Asking the wrong tenant.** Each point must be asked of its owner. Asking every tenant at every point is a different, slower method.
- **Reusing answers after preferences change.** The walk relies on fixed answers, so cache them per point and do not ask again.

## Implementations

## History

Forest Simmons used Sperner's lemma with owner labels for cake cutting. He presented the idea to math clubs and school groups and told it to Michael Starbird in 1980, but he never published it. Francis Edward Su published the method in 1999 in the American Mathematical Monthly. He adapted it to rent division, where a twist is needed because the room labels are not a Sperner labeling, and to chore division. He described the trap-door algorithm and invited readers to code it.

## References
