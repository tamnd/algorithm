---
tag: CPV99G
kind: theorem
slug: log-rank-conjecture
name: Log-rank conjecture
aliases:
- Lovász-Saks conjecture
area: complexity/communication-and-query-complexity
level: research
summary: "Open (Lovász and Saks, 1988): is D^cc(f) at most a polynomial in log2 rank(M_f)? Known: D^cc(f) = O(sqrt(rank)), and some f need about (log rank)^2 bits."
prereqs: [log-rank-lower-bound, deterministic-communication-complexity]
see_also: [log-rank-lower-bound, communication-matrix, fooling-set-method, nondeterministic-communication-complexity, sign-rank, chromatic-number, sensitivity-theorem, randomized-communication-complexity]
sources:
  - paper: doi:10.1109/SFCS.1988.21924
    title: "László Lovász and Michael Saks, Lattices, Möbius functions and communication complexity, Proceedings of the 29th Annual Symposium on Foundations of Computer Science (FOCS 1988), pages 81-90"
    locator: the statement of the conjecture and its form for graphs; this page relies on the conference version
  - paper: "László Lovász and Michael Saks, Communication complexity and combinatorial lattice theory, Journal of Computer and System Sciences 47(2) (1993), pages 322-349"
    locator: the journal version of the FOCS 1988 paper
  - paper: doi:10.1109/SFCS.1994.365711
    title: Noam Nisan and Avi Wigderson, On rank vs. communication complexity, Proceedings of the 35th Annual Symposium on Foundations of Computer Science (FOCS 1994)
    locator: the equivalence with large monochromatic rectangles, and the function of Kushilevitz with cost (log rank)^(log_3 6)
  - paper: doi:10.1145/2724704
    title: "Shachar Lovett, Communication is bounded by root of rank, Journal of the ACM 63(1) (2016), Article 1, pages 1-9 (STOC 2014, pages 842-846)"
    locator: the main theorem, D^cc(f) = O(sqrt(rank) log(rank))
  - paper: doi:10.1007/s10107-024-02117-9
    title: "Benny Sudakov and István Tomon, Matrix discrepancy and the log-rank conjecture, Mathematical Programming 212(1-2) (2025), pages 567-579 (arXiv:2311.18524)"
    locator: the main theorem, D^cc(f) = O(sqrt(rank))
  - paper: doi:10.1137/16M1059369
    title: "Mika Göös, Toniann Pitassi and Thomas Watson, Deterministic communication vs. partition number, SIAM Journal on Computing 47(6) (2018), pages 2435-2450 (FOCS 2015)"
    locator: Theorem 2 and its corollary for rank (a function with deterministic cost about (log rank)^2)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 2, Rank (section Better Upper Bounds Using Rank), and Chapter 8, Lifting (section Separating Rank and Communication)
---

The log-rank conjecture says that the [log-rank lower bound](/log-rank-lower-bound/) is tight up to a polynomial: the deterministic communication cost $D^{cc}(f)$ of every Boolean function should be at most a polynomial in $\log_2 \operatorname{rank}(M_f)$, where $M_f$ is the [communication matrix](/communication-matrix/) and the rank is over the reals. Lovász and Saks stated it in 1988, and it is still open. The best general upper bound is $O(\sqrt{\operatorname{rank}(M_f)})$, exponentially far from the conjecture, and the best separation shows that the polynomial must be at least about quadratic.

## Statement

Let $f : X \times Y \to \{0,1\}$ be a two-party function with communication matrix $M_f$, and write $r = \operatorname{rank}(M_f)$ over $\mathbb{R}$. Let $D^{cc}(f)$ be the [deterministic communication complexity](/deterministic-communication-complexity/), where both players know the answer at the end. The proved bounds are

$$\log_2 r \le D^{cc}(f) \le r + 1.$$

### Conjecture

**Log-rank conjecture (Lovász and Saks, 1988).** There is a constant $C$ such that for every Boolean function $f$ with $r \ge 2$,

$$D^{cc}(f) \le (\log_2 r)^C.$$

This is an open problem, not a theorem. The rank must be over a field of characteristic zero: over $\mathrm{GF}(2)$ the statement is false, since the inner product function has $\mathrm{GF}(2)$ rank $n$ but $D^{cc} = n + 1$.

### Known results

**Theorem (Mehlhorn and Schmidt, 1982).** $D^{cc}(f) \ge \log_2 r$. See the [log-rank lower bound](/log-rank-lower-bound/).

**Theorem (Lovett, 2016).** $D^{cc}(f) = O(\sqrt{r} \log r)$.

**Theorem (Sudakov and Tomon, 2024).** $D^{cc}(f) = O(\sqrt{r})$.

**Theorem (Kushilevitz, 1994, in Nisan and Wigderson).** There are functions with $D^{cc}(f) = \Omega((\log r)^{\log_3 6})$, where $\log_3 6 \approx 1.63$.

**Theorem (Göös, Pitassi and Watson, 2018).** There are functions with $D^{cc}(f) \ge \tilde{\Omega}((\log r)^2)$, where $\tilde{\Omega}$ hides factors polylogarithmic in $\log r$. So the constant $C$, if it exists, is at least 2.

**Theorem (Nisan and Wigderson, 1994).** The conjecture is equivalent to this statement: there is a constant $C'$ such that every 0-1 matrix of rank $r$ has a monochromatic rectangle that holds at least a $2^{-(\log_2 r)^{C'}}$ fraction of its entries.

**Theorem (Lovász and Saks, 1988).** The conjecture is equivalent to a statement about graphs: the [chromatic number](/chromatic-number/) $\chi(G)$ of every graph $G$ satisfies $\log_2 \chi(G) \le (\log_2 \operatorname{rank}(A_G))^{O(1)}$, where $A_G$ is the adjacency matrix of $G$.

## In plain words

Write all the answers of a two-person question in a table. The rank of the table measures how many truly different patterns its rows have. It is known that the two people must talk at least as long as the number of binary digits of the rank.

The conjecture says that this is close to the truth: a table with few patterns should always allow a short talk, not much longer than the number of digits of the rank, raised to some fixed power.

Nobody knows if this is true. The best known method needs a talk about as long as the square root of the rank, which is far longer. On the other side, there are questions where the talk must be about the square of the number of digits of the rank. So the true power, if one exists, is at least two.

## Proof

There is no proof: the statement is open. This section proves the upper bound $D^{cc}(f) \le r + 1$ that every attempt starts from, and sketches how the $O(\sqrt{r})$ bounds are proved.

**The trivial upper bound.** Let $r = \operatorname{rank}(M_f)$. Choose $r$ columns $c_1, \ldots, c_r$ of $M_f$ that span its column space. Every column is a linear combination of them, so two rows that agree on the columns $c_1, \ldots, c_r$ agree everywhere. The entries are 0 or 1, so there are at most $2^r$ different restrictions of a row to these columns, and at most $2^r$ distinct rows. The protocol: Alice sends the $r$ bits of her row on the columns $c_1, \ldots, c_r$. Bob now knows Alice's whole row, so he knows $f(x, y)$, and he sends it. The cost is $r + 1$. $\blacksquare$

**Sketch of the $O(\sqrt{r} \log r)$ bound (Lovett, 2016).** The proof has two steps.

1. Large monochromatic rectangles. Every 0-1 matrix of rank $r$ has a monochromatic rectangle with at least a $2^{-O(\sqrt{r} \log r)}$ fraction of its entries. Lovett proves this with discrepancy: a low-rank sign matrix has a rectangle where it is far from balanced, by a bound that uses John's theorem on convex bodies. Then he samples rows and columns to grow such a biased rectangle into a monochromatic one.
2. From rectangles to a protocol. Let $R$ be a monochromatic rectangle of $M_f$, and split $M_f$ into $R$, the rows of $R$ outside its columns, and the columns of $R$ outside its rows. The ranks of the two strips add up to at most $r + 1$, so one of them has rank at most about $r/2$. If the strip on the rows of $R$ has the small rank, Alice sends one bit that says whether her row is a row of $R$; otherwise Bob does the same for the columns. On one branch the rank about halves; on the other the matrix loses the rows or the columns of $R$, a part of size at least that of $R$. Nisan and Wigderson showed how this recursion gives a protocol, and with the bound of step 1 its cost is $O(\sqrt{r} \log r)$.

The steps left out are the discrepancy bound for low-rank matrices and the count of the recursion. Rao and Yehudayoff (Chapter 2, section Better Upper Bounds Using Rank) give the full proof. Sudakov and Tomon (2024) remove the $\log r$ factor with a sharper discrepancy bound for matrices.

## Consequences

If the conjecture is true:

- $D^{cc}(f)$ and $\log_2 \operatorname{rank}(M_f)$ are polynomially related, so rank, a quantity that [Gaussian elimination](/gaussian-elimination/) computes in polynomial time, would decide the deterministic cost up to a polynomial.
- The log of the partition number $\chi(f)$ would also be within a polynomial of $\log_2 r$, since $\log_2 r \le \log_2 \chi(f) \le D^{cc}(f)$.
- Every graph whose adjacency matrix has low rank would have a small chromatic number, by the form of Lovász and Saks.

What is already known follows from the proved bounds:

- The separation of Göös, Pitassi and Watson shows that $D^{cc}(f)$ can exceed $(\log_2 r)^{2 - o(1)}$, so no proof can give an exponent below 2.
- The analogous question for randomized protocols, with the approximate rank in place of the rank, has a negative answer (Chattopadhyay, Mande and Sherif, 2019): there are functions whose randomized cost is much larger than any polynomial in the log of the approximate rank. So a proof of the conjecture must use exactness, the 0 and 1 entries, in an essential way.
- For nondeterminism the rank says nothing: non-equality has rank $2^n$ and nondeterministic cost $O(\log n)$. See [nondeterministic communication complexity](/nondeterministic-communication-complexity/).

## Tightness

The lower side $\log_2 r$ is tight for equality, greater-than, disjointness and inner product, where $D^{cc} = n + 1$ and $\log_2 r \approx n$. The upper side $r + 1$ is far from tight for these functions.

For the worst function, the truth lies between the separation $\tilde{\Omega}((\log r)^2)$ of Göös, Pitassi and Watson and the upper bound $O(\sqrt{r})$ of Sudakov and Tomon. Closing this gap, from a power of $\log r$ to a power of $r$, is the open problem.

## History

Lovász and Saks stated the conjecture at FOCS 1988, together with its form for graphs, in a paper on lattices and Möbius functions; the journal version appeared in 1993. Nisan and Wigderson (FOCS 1994) proved the equivalence with large monochromatic rectangles and published the example of Kushilevitz with exponent $\log_3 6$. Lovett (STOC 2014, JACM 2016) gave the first upper bound below $O(r)$, with $O(\sqrt{r} \log r)$. Göös, Pitassi and Watson (FOCS 2015, SIAM Journal on Computing 2018) raised the lower exponent to 2 with a lifting theorem. Sudakov and Tomon (arXiv 2023, Mathematical Programming 2025) improved the upper bound to $O(\sqrt{r})$.

## References
