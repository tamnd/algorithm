---
tag: D88PXW
kind: theorem
slug: de-bruijn-existence-theorem
name: De Bruijn sequence existence theorem
aliases:
- de Bruijn-Good theorem
area: strings/string-combinatorics
level: core
summary: A de Bruijn sequence of every order exists, from an Eulerian circuit in the de Bruijn graph.
prereqs: [de-bruijn-graph, de-bruijn-sequence]
see_also: [eulerian-circuit, hierholzer-algorithm, fkm-algorithm, matrix-tree-theorem, line-graph, hamiltonian-cycle, necklace-enumeration, eulerian-graph]
sources:
  - paper: "Nicolaas G. de Bruijn, A combinatorial problem, Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen 49, 1946, 758-764"
    title: Nicolaas G. de Bruijn, A combinatorial problem
    locator: the existence of binary sequences of every order and their number 2^(2^(n-1) - n), through the graph on words of length n - 1
  - paper: doi:10.1112/jlms/s1-21.3.167
    title: Irving J. Good, Normal recurring decimals, Journal of the London Mathematical Society 21(3), 1946, 167-169
    locator: the existence for every alphabet size, by an Eulerian circuit of the same graph
  - paper: "Tatyana van Aardenne-Ehrenfest and Nicolaas G. de Bruijn, Circuits and trees in oriented linear graphs, Simon Stevin 28, 1951, 203-217"
    title: Tatyana van Aardenne-Ehrenfest and Nicolaas G. de Bruijn, Circuits and trees in oriented linear graphs
    locator: the count of Eulerian circuits of a balanced directed graph through spanning arborescences (the BEST theorem), and the count (k!)^(k^(n-1)) / k^n of de Bruijn cycles
  - paper: doi:10.1090/s0002-9904-1934-05988-3
    title: Monroe H. Martin, A problem in arrangements, Bulletin of the American Mathematical Society 40(12), 1934, 859-864
    locator: an earlier existence proof for every alphabet size, by the greedy construction that prefers the largest letter
  - paper: doi:10.1137/1024041
    title: Harold Fredricksen, A survey of full length nonlinear shift register cycle algorithms, SIAM Review 24(2), 1982, 195-221
    locator: the history of the theorem, including the 1894 solution of Flye Sainte-Marie for two letters
---

## Statement

Let $\Sigma$ be an alphabet of $k \ge 1$ letters and $n \ge 1$. Indices are 0-based, and the windows of a cyclic word are taken modulo its length. The de Bruijn graph $B_{n-1}$ has the vertex set $\Sigma^{n-1}$ and, for each word $x \in \Sigma^n$, one edge labeled $x$ from $x[0..n-2]$ to $x[1..n-1]$.

**Theorem.**

1. $B_{n-1}$ has an Eulerian circuit, a closed walk that uses every edge exactly once.
2. For a closed walk $x_0 \to \cdots$ of $L$ edges in $B_{n-1}$, with edges $x_0, \ldots, x_{L-1}$ in order, let $s = x_0[0]\,x_1[0] \cdots x_{L-1}[0]$. Then the cyclic window of length $n$ of $s$ at $i$ is $x_i$. Conversely, the cyclic windows of any cyclic word of length $L$ form a closed walk of $L$ edges in this way.
3. Hence the map in item 2 is a bijection between the Eulerian circuits of $B_{n-1}$ with a chosen first edge and the de Bruijn sequences of order $n$ over $\Sigma$. In particular a de Bruijn sequence of order $n$ over $k$ letters exists for every $k \ge 1$ and $n \ge 1$.

## In plain words

Make a map whose stops are all words of length $n - 1$ and whose one-way roads are all words of length $n$: a road leads from its first $n - 1$ letters to its last $n - 1$ letters. Every stop has as many roads in as out, and you can get from any stop to any other. A classical fact about such maps says that you can drive a round trip using every road exactly once. Write down the first letter of each road on that trip; the circle of letters you get shows each word of length $n$ exactly once, as the road where it starts.

## Proof

Write $V = \Sigma^{n-1}$ and $E = \Sigma^n$, so $|E| = k^n$.

**Step 1: $B_{n-1}$ is balanced.** The edges leaving a vertex $u$ are the words $u\,c$ for $c \in \Sigma$, and the edges entering $v$ are the words $a\,v$ for $a \in \Sigma$. So every vertex has out-degree $k$ and in-degree $k$, counting a loop once in each. For $n = 1$ there is one vertex, the empty word, with $k$ loops.

**Step 2: $B_{n-1}$ is strongly connected.** Let $u, v \in V$ and $n \ge 2$. For $0 \le t \le n - 1$ let $w_t$ be the suffix of length $n - 1$ of $u\,v[0..t-1]$, so $w_0 = u$ and $w_{n-1} = v$. For $0 \le t \le n - 2$, the suffix $y$ of length $n$ of $u\,v[0..t]$ has its first $n - 1$ letters equal to $w_t$ and its last $n - 1$ letters equal to $w_{t+1}$, so $y$ is an edge from $w_t$ to $w_{t+1}$. This is a walk from $u$ to $v$ with $n - 1$ edges. For $n = 1$ there is one vertex.

**Step 3: a balanced, strongly connected directed multigraph with at least one edge has an Eulerian circuit.** Let $G$ be such a graph; loops and parallel edges are allowed. A trail is a walk without repeated edges.

- *A maximal trail from a vertex returns to it.* Start at a vertex $v$ with an out-edge and extend a trail by unused edges as long as possible. Suppose it stops at $w \ne v$. Each visit of $w$ inside the trail uses one in-edge and one out-edge of $w$, and the last arrival uses one more in-edge, so the trail uses one more in-edge than out-edge at $w$. As $\deg^-(w) = \deg^+(w)$, an out-edge of $w$ is unused, so the trail was not maximal. Hence it stops at $v$, and it is a closed trail.
- *A longest closed trail uses every edge.* Let $C$ be a closed trail with the most edges, which exists since $G$ has an edge and is finite. Suppose an edge $(a, b)$ is not in $C$. Take a vertex $u$ of $C$ and a walk from $u$ to $a$, which exists by strong connectivity, followed by the edge $(a, b)$. Let $f$ be the first edge of this route that is not in $C$. The edges before $f$ are in $C$, so the tail $z$ of $f$ is $u$ or the head of an edge of $C$; in both cases $z$ lies on $C$. In the graph $G'$ of the edges not in $C$, every vertex is still balanced, because $C$ uses as many in-edges as out-edges at each vertex. By the first point applied to $G'$, starting with $f$, there is a closed trail $C'$ in $G'$ through $z$. Inserting $C'$ into $C$ at a visit of $z$ gives a closed trail with more edges than $C$, a contradiction.

With Steps 1 and 2, this proves item 1, since $B_{n-1}$ has $k^n \ge 1$ edges.

**Step 4: windows of a closed walk (item 2).** Let $x_0, \ldots, x_{L-1}$ be the edges of a closed walk, indices modulo $L$. Consecutive edges share a vertex, so $x_{i+1}[0..n-2] = x_i[1..n-1]$, that is, $x_i[j] = x_{i+1}[j-1]$ for $1 \le j \le n - 1$. By induction on $j$, $x_i[j] = x_{i+j}[0] = s[(i + j) \bmod L]$ for $0 \le j \le n - 1$, so the cyclic window of $s$ at $i$ is $x_i$. Conversely, for a cyclic word $s$ of length $L$ let $x_i$ be its window at $i$. Then $x_i[1..n-1] = x_{i+1}[0..n-2]$, both being $s[i+1] \cdots s[i+n-1]$ with indices modulo $L$, so $x_i$ ends where $x_{i+1}$ starts, and $x_0, \ldots, x_{L-1}$ is a closed walk whose first letters spell $s$.

**Step 5: the bijection (item 3).** By Step 4, the windows of $s$ are the edges of the walk, in order. They are pairwise distinct and are all of $\Sigma^n$ exactly when the walk uses each edge of $B_{n-1}$ once, that is, when it is an Eulerian circuit; then $L = k^n$. The two maps of Step 4 are inverse to each other: the walk is read off from the windows of $s$, and $s$ from the first letters of the walk. Together with item 1, a de Bruijn sequence of order $n$ exists. $\blacksquare$

## Consequences

- **Constructions.** Any algorithm for Eulerian circuits, such as [Hierholzer's algorithm](/hierholzer-algorithm/), builds a de Bruijn sequence in $\Theta(k^n)$ time. Other constructions, such as the [FKM algorithm](/fkm-algorithm/), give a de Bruijn sequence without storing the graph.
- **The number of de Bruijn cycles.** By item 3, the de Bruijn sequences correspond to Eulerian circuits with a chosen first edge; a de Bruijn cycle has $k^n$ distinct rotations, since its windows are distinct, and an Eulerian circuit has $k^n$ choices of first edge. So the number of de Bruijn cycles equals the number of Eulerian circuits of $B_{n-1}$ up to rotation. The BEST theorem of van Aardenne-Ehrenfest, de Bruijn, Smith and Tutte counts these through spanning arborescences and the [matrix-tree theorem](/matrix-tree-theorem/), and gives
$$ \frac{(k!)^{k^{n-1}}}{k^n}, $$
which is $2^{2^{n-1} - n}$ for $k = 2$. The values are 1, 2, 16, 2048, 67108864 for $k = 2$ and $n = 2, \ldots, 6$, and 24, 373248 for $k = 3$ and $n = 2, 3$.
- **Hamiltonian form.** $B_n$ is the [line graph](/line-graph/) of $B_{n-1}$: its vertices are the edges of $B_{n-1}$, and $x \to y$ is an edge of $B_n$ exactly when $x$ ends where $y$ starts in $B_{n-1}$. So an Eulerian circuit of $B_{n-1}$ is a [Hamiltonian cycle](/hamiltonian-cycle/) of $B_n$, and the de Bruijn graphs have Hamiltonian cycles of every order.
- **Linear version.** For each de Bruijn sequence $s$, the word $s\,s[0..n-2]$ of length $k^n + n - 1$ contains every word of length $n$ once as a factor.

## Tightness

- **Length.** A cyclic word of length $L$ has only $L$ windows, so a cyclic word containing every word of $\Sigma^n$ has length at least $k^n$; the theorem attains this bound, with each window used once.
- **The balance condition.** Step 3 needs the in-degree and out-degree to agree at every vertex, and without it the conclusion fails. Keep only the binary windows `00`, `10` and `11` of length 2: the vertex `0` has the in-edges `00` and `10` but only the out-edge `00`. Indeed no binary cyclic word of length 3 has exactly these three windows: `000` and `111` have one window each, and the rotations of `001` and `011` all contain `01`.
- **One order at a time.** A de Bruijn sequence of order $n$ has length $k^n$, so it contains only $k^n$ of the $k^{n+1}$ words of length $n + 1$; for $k \ge 2$ no cyclic word is a de Bruijn sequence of two orders.

## History

Flye Sainte-Marie solved the binary case in 1894, in a question of the journal L'Intermédiaire des Mathématiciens, and also counted the sequences. Martin (1934) proved the existence for every alphabet size with the greedy construction that prefers the largest letter. In 1946, de Bruijn rediscovered the binary problem, counted the sequences as $2^{2^{n-1}-n}$ and introduced the graph now named after him, and Good, independently, proved the existence for every alphabet size with Eulerian circuits of the same graph. Van Aardenne-Ehrenfest and de Bruijn (1951), building on Smith and Tutte (1941), proved the count of Eulerian circuits now called the BEST theorem, which gives the number of de Bruijn cycles for every $k$. De Bruijn later noted the priority of Flye Sainte-Marie.

## References
