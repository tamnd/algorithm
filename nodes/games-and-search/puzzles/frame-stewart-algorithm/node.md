---
tag: NSH7PT
kind: algorithm
slug: frame-stewart-algorithm
name: Frame-Stewart algorithm
aliases:
- Frame's algorithm
- Stewart's algorithm
area: games-and-search/puzzles
level: advanced
summary: "Solve the Tower of Hanoi with p >= 4 pegs: park the k smallest discs with all pegs, move the rest with p - 1 pegs, then bring the k discs back, with k chosen by a recurrence. Optimal for 4 pegs."
solves: [tower-of-hanoi]
model: word-ram
complexity:
  vars: {n: the number of discs, p: the number of pegs, m: the number of moves output}
  time: {worst: O(n^2 p + m)}
  space: {extra: O(n p)}
properties: {deterministic: true, recursive: true}
history:
  year: 1941
  people: [J. S. Frame, B. M. Stewart]
  note: Frame and Stewart published the method independently in the American Mathematical Monthly in 1941, as solutions of a problem that Stewart had posed in 1939.
prereqs: [tower-of-hanoi, recursion, memoization]
see_also: [tower-of-hanoi, optimal-substructure, binomial-coefficient, hockey-stick-identity, breadth-first-search, pattern-database, state-space]
sources:
  - paper: "J. S. Frame, Solution to advanced problem 3918, American Mathematical Monthly 48(3), 1941"
    locator: pp. 216-217
  - paper: "B. M. Stewart, Solution to advanced problem 3918, American Mathematical Monthly 48(3), 1941"
    locator: "pp. 217-219, with the editor's note on p. 219 that the optimality of the method is assumed and not proved"
  - paper: doi:10.36045/bbms/1420071861
    title: "Thierry Bousch, La quatrième tour de Hanoï, Bulletin of the Belgian Mathematical Society Simon Stevin 21(5), 2014"
    locator: "pp. 895-912, the proof that the Frame-Stewart numbers are optimal for four pegs"
  - paper: doi:10.1137/S0097539703431019
    title: "Xiao Chen and Jian Shen, On the Frame-Stewart conjecture about the Towers of Hanoi, SIAM Journal on Computing 33(3), 2004"
    locator: "pp. 584-589, the bound 2^((1 + o(1)) (n (p - 2)!)^(1/(p - 2))) for both the Frame-Stewart number and the optimum"
  - paper: "Richard E. Korf and Ariel Felner, Recent progress in heuristic search: a case study of the four-peg Towers of Hanoi problem, IJCAI 2007"
    locator: "pp. 2324-2329, the verification for up to 30 discs"
  - paper: doi:10.1016/S0166-218X(01)00287-6
    title: "Sandi Klavžar, Uroš Milutinović and Ciril Petr, On the Frame-Stewart algorithm for the multi-peg Tower of Hanoi problem, Discrete Applied Mathematics 120(1-3), 2002"
    locator: "pp. 141-157, the equivalence of seven published approaches and the formula with increments"
  - book: isbn:9783319737782
    title: "Andreas M. Hinz, Sandi Klavžar and Ciril Petr, The Tower of Hanoi: Myths and Maths, second edition, Birkhäuser, 2018"
    locator: "Chapter 5, The Tower of Hanoi with More Pegs, Sections 5.1 and 5.2 (the conjecture and the Frame-Stewart numbers)"
---

The Frame-Stewart algorithm moves a tower of $n$ discs in the [Tower of Hanoi](/tower-of-hanoi/) with $p \ge 4$ pegs: it moves the $k$ smallest discs to a spare peg with all $p$ pegs, moves the other $n - k$ discs to the target with the remaining $p - 1$ pegs, and moves the $k$ discs onto them with all $p$ pegs again, where $k$ minimizes the total. Its move count $S(n, p)$ grows like $2^{\Theta(n^{1/(p-2)})}$, far below the $2^n - 1$ of three pegs; for four pegs it is $\Theta(\sqrt{n}\, 2^{\sqrt{2n}})$. Frame and Stewart published it in 1941 with the claim that it is optimal. Bousch proved the claim for four pegs in 2014, and it is open for five or more pegs.

## In plain words

With three pegs, the largest disc forces you to stack every other disc on the one free peg, and the work doubles with each disc. A fourth peg gives room to split the tower. First move a group of the smallest discs to a spare peg, using every peg, so that this group is quick to move. Then the larger discs move to the target while the small group sits still, and since one peg is now blocked by the small group, the larger discs have one peg fewer to work with. Last, move the small group on top of them, again with every peg. The art is the size of the small group: too small, and the larger part is slow; too large, and moving the small group twice costs too much. A short table of best costs for smaller towers gives the best size.

## The problem

The input is the number of discs $n \ge 0$, the number of pegs $p \ge 3$, a source peg and a target peg. The discs start as a tower on the source and must end as a tower on the target, with the rules of the [Tower of Hanoi](/tower-of-hanoi/): one top disc moves at a time, and no disc lies on a smaller disc. The output is a legal sequence of moves. The aim is to make it short; the true minimum is called $H(n, p)$, and the [state space](/state-space/) has $p^n$ states.

## The algorithm

The algorithm uses the Frame-Stewart numbers, defined for $n \ge 0$ and $p \ge 3$ by

$$S(0, p) = 0, \qquad S(1, p) = 1, \qquad S(n, 3) = 2^n - 1, \qquad S(n, p) = \min_{1 \le k \le n - 1} \bigl(2\,S(k, p) + S(n - k, p - 1)\bigr) \text{ for } n \ge 2,\ p \ge 4.$$

A table of $S(n', p')$ for $n' \le n$ and $3 \le p' \le p$ is filled in order of increasing $p'$ and $n'$, and $K(n', p')$ stores the smallest $k$ that reaches the minimum.

```pseudo id=main
FRAME-STEWART(n, s, d, P)      ▷ move the n smallest discs on peg s to peg d, using only the pegs in the set P
L1  if n = 0 then return
L2  if n = 1 then move the top disc of s to d; return
L3  a ← a peg of P other than s and d
L4  if |P| = 3 then
L5      FRAME-STEWART(n − 1, s, a, P); move the top disc of s to d; FRAME-STEWART(n − 1, a, d, P); return
L6  k ← K(n, |P|)
L7  FRAME-STEWART(k, s, a, P)
L8  FRAME-STEWART(n − k, s, d, P \ {a})
L9  FRAME-STEWART(k, a, d, P)
```

The top call is FRAME-STEWART$(n, \text{source}, \text{target}, \{0, \dots, p - 1\})$. Line L5 is the classical three-peg recursion. Lines L7 to L9 are the split: the top $k$ discs go to $a$ with all pegs, the other $n - k$ discs go to $d$ without peg $a$, and the $k$ discs go from $a$ to $d$ with all pegs.

## Example

Take $n = 6$ discs and $p = 4$ pegs, numbered 0 to 3, from peg 0 to peg 3. The table gives

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $S(n, 3)$ | 1 | 3 | 7 | 15 | 31 | 63 |
| $S(n, 4)$ | 1 | 3 | 5 | 9 | 13 | 17 |

For $n = 6$ the candidates $2S(k, 4) + S(6 - k, 3)$ are 33, 21, 17, 21 and 29 for $k = 1, \dots, 5$, so $k = 3$ and $S(6, 4) = 17$. The top call picks $a = 1$ at L3. A move "disc 2: 0 to 3" takes disc 2 from peg 0 to peg 3.

| Line | Call | Moves | Count |
|---|---|---|---|
| L7 | 3 discs from 0 to 1 with pegs $\{0, 1, 2, 3\}$; inside, $k = 1$ and the spare is peg 2 | disc 1: 0 to 2; disc 2: 0 to 3; disc 3: 0 to 1; disc 2: 3 to 1; disc 1: 2 to 1 | 5 |
| L8 | discs 4 to 6 from 0 to 3 with pegs $\{0, 2, 3\}$, the three-peg recursion | disc 4: 0 to 3; disc 5: 0 to 2; disc 4: 3 to 2; disc 6: 0 to 3; disc 4: 2 to 0; disc 5: 2 to 3; disc 4: 0 to 3 | 7 |
| L9 | 3 discs from 1 to 3 with pegs $\{0, 1, 2, 3\}$; inside, $k = 1$ and the spare is peg 0 | disc 1: 1 to 0; disc 2: 1 to 2; disc 3: 1 to 3; disc 2: 2 to 3; disc 1: 0 to 3 | 5 |

The total is $5 + 7 + 5 = 17$ moves. In the graph of all $4^6 = 4096$ states the distance between the two towers is also 17, so this solution is shortest.

## Correctness

The full proofs are in the proof file; here is the outline.

- **Legality.** Each call runs under the precondition that the $n$ discs to move are the $n$ smallest discs on the pegs of $P$, that they form a tower on top of $s$, and that every other disc on a peg of $P$ is larger than all of them. Larger discs then act as the floor: any legal sequence for the $n$ discs alone is legal in the whole puzzle. The calls in L5, L7, L8 and L9 meet the precondition. In L8 the $k$ small discs lie on $a$, and $a$ is removed from $P$, so the larger discs never land on them.
- **Result.** By induction on $n$, each call ends with the $n$ discs as a tower on $d$ and every other disc where it was.
- **Move count.** By induction, the call makes exactly $S(n, |P|)$ moves, because L7 and L9 make $S(k, |P|)$ each, L8 makes $S(n - k, |P| - 1)$, and $k$ reaches the minimum in the recurrence.
- **Termination.** Each recursive call has at most $n - 1$ discs, because $1 \le k \le n - 1$.

The algorithm is the best among the strategies that move the tower in this split form; whether some other strategy is shorter is the Frame-Stewart conjecture. For $p = 3$ the count is $2^n - 1$, which is optimal; for $p = 4$, $S(n, 4) = H(n, 4)$ for every $n$ (Bousch 2014).

## Complexity

**Moves.** The increments of $S$ are powers of 2 (Klavžar, Milutinović and Petr 2002): for $n \ge 1$,

$$S(n, p) - S(n - 1, p) = 2^t \quad \text{where } \binom{t + p - 3}{p - 2} < n \le \binom{t + p - 2}{p - 2},$$

so the increment $2^t$ occurs $\binom{t + p - 3}{p - 3}$ times, and the counts add up by the [hockey stick identity](/hockey-stick-identity/). For four pegs this reads: the $n$-th increment is $2^{t}$ when $t(t + 1)/2 < n \le (t + 1)(t + 2)/2$, so the values are $0, 1, 3, 5, 9, 13, 17, 25, 33, 41, 49, 65, \dots$ and $S(n, 4) = \Theta(\sqrt{n}\, 2^{\sqrt{2n}})$. For fixed $p$, $t \approx ((p - 2)!\, n)^{1/(p-2)}$ at the last increment, which gives $S(n, p) = 2^{(1 + o(1))((p - 2)!\, n)^{1/(p - 2)}}$.

| $n$ | 5 | 10 | 15 | 20 | 64 |
|---|---|---|---|---|---|
| $S(n, 3)$ | 31 | 1023 | 32,767 | 1,048,575 | $\approx 1.8 \times 10^{19}$ |
| $S(n, 4)$ | 13 | 49 | 129 | 289 | 18,433 |
| $S(n, 5)$ | 11 | 31 | 71 | 111 | |

**Time.** Filling the table costs $O(n)$ for each of its $O(np)$ entries, so $O(n^2 p)$ in the [word RAM](/word-ram/), with numbers of $O(n)$ bits counted as words. After the top call, every call has at least one disc, because $k \ge 1$ and $n - k \ge 1$ in L7 to L9 and $n - 1 \ge 1$ in L5. So the calls form a tree whose leaves are calls with one disc, each making one move, and whose inner nodes have at least 2 children. A tree with $m$ leaves and branching at least 2 has fewer than $2m$ nodes, and with the peg set $P$ kept as a bit mask each call does $O(1)$ work besides its children, so the moves cost $O(m)$ with $m = S(n, p)$.

**Space.** The table takes $O(np)$ words. The recursion depth is at most $n$, and each frame holds $O(1)$ words, so the stack takes $O(n)$ words; the moves are written to the output and not stored.

**Lower bounds.** Chen and Shen (2004) proved that every solution needs $2^{(1 - o(1))((p - 2)!\, n)^{1/(p - 2)}}$ moves, so the exponent of the Frame-Stewart count is right up to a factor $1 + o(1)$ for each fixed $p$. Any program that lists the moves takes $\Omega(m)$ time.

## Properties

- **Optimal for three and four pegs.** For three pegs it is the classical recursion. For four pegs, $S(n, 4) = H(n, 4)$ for all $n$.
- **Not unique.** For many $n$ two values of $k$ reach the minimum; for four pegs, $k = 1$ and $k = 2$ both give 9 moves for $n = 4$, and $k = 3$ is the only best value for $n = 6$. For four pegs and $n \ge 3$, if $n = t(t + 1)/2$ the only best value of $n - k$ is $t$, and if $t(t + 1)/2 < n < (t + 1)(t + 2)/2$ the best values are $t$ and $t + 1$.
- **Deterministic and recursive.** It uses a precomputed table and a recursion of depth at most $n$.

## Variants and improvements

- **Fixed split.** For four pegs, $k = n - t$ with $t$ the integer nearest to $\sqrt{2n}$ gives a best split, so no table is needed.
- **Search.** For four pegs Korf and Felner (2007) confirmed $S(n, 4) = H(n, 4)$ for all $n \le 30$ with disk-based heuristic search and [pattern databases](/pattern-database/), before Bousch's proof.

## When to use it

Use it to move a full tower with four or more pegs, when a short solution is wanted and the count must be exact. For four pegs the result is optimal. For five or more pegs it gives the best known count, but no proof says it is shortest; for small $n$ a [breadth-first search](/breadth-first-search/) over the $p^n$ states is the only way to get a certified optimum.

## Pitfalls

- **Forgetting to block the parked peg.** In L8 the $n - k$ larger discs must not use peg $a$, which holds the small discs. A program that passes all of $P$ to L8 makes illegal moves.
- **Calling the result optimal for five or more pegs.** It is a conjecture. It holds for the small cases that search can reach, and the asymptotic bounds match only in the exponent.
- **Greedy choices of $k$.** The best $k$ depends on both $n$ and $p$; taking $k = n/2$ or $k = n - 1$ gives far more moves. With $k = n - 1$ and four pegs the algorithm is no faster than three pegs.
- **Deep recursion.** For large $n$ the move list is too long to output, but even for moderate $n$ a language with a small stack limit needs an explicit stack.

## Implementations

## History

H. E. Dudeney posed the four-peg puzzle as the Reve's puzzle in 1907. B. M. Stewart posed the general problem with $p$ pegs as Advanced Problem 3918 in the American Mathematical Monthly in 1939, and in 1941 the Monthly printed two solutions with the same method, by J. S. Frame and by Stewart. The editor noted that both assumed, without proof, that the split strategy is optimal. Klavžar, Milutinović and Petr (2002) showed that seven different published approaches give the same numbers. Chen and Shen (2004) proved that the optimum has the same exponent, Korf and Felner (2007) confirmed the four-peg numbers up to 30 discs by search, and Bousch (2014) proved that the algorithm is optimal for four pegs.

## References
