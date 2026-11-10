---
tag: 7HM42M
kind: theorem
slug: mapreduce-communication-lower-bounds
name: Communication cost lower bounds for MapReduce
aliases:
- replication rate bounds
- Afrati et al. lower bound
area: parallel/mapreduce-and-bsp
level: research
summary: In one MapReduce round with at most q inputs per reducer, the replication rate is at least q|O|/(g(q)|I|), where g(q) bounds the outputs of q inputs. For Hamming distance 1 this is b/log2 q.
history:
  year: 2013
  people: [Foto N. Afrati, Anish Das Sarma, Semih Salihoglu, Jeffrey D. Ullman]
  note: Afrati, Das Sarma, Salihoglu and Ullman gave the recipe and the bounds for Hamming distance 1, triangles and matrix multiplication in PVLDB 2013.
prereqs: [mapreduce-model]
see_also: [mrc-model, shuffle-phase, hamming-distance, triangle-counting, naive-matrix-multiplication, hypercube-shares-join, h-relation, linearity-of-expectation]
sources:
  - paper: doi:10.14778/2535570.2488334
    title: "Foto N. Afrati, Anish Das Sarma, Semih Salihoglu and Jeffrey D. Ullman, Upper and lower bounds on the cost of a map-reduce computation, PVLDB 6(4), 2013"
    locator: pp. 277-288; Section 2.5 (the recipe for lower bounds), Lemma 3.1 and Theorem 3.2 (Hamming distance 1), Section 3.3 (the splitting algorithm), Section 4.1 (triangles), Section 6.1 (matrix multiplication)
  - book: isbn:9781108476348
    title: "Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020"
    locator: Chapter 2, communication cost and the complexity theory of MapReduce (reducer size and replication rate)
  - paper: doi:10.1145/2463664.2465224
    title: "Paul Beame, Paraschos Koutris and Dan Suciu, Communication steps for parallel query processing, PODS 2013"
    locator: one-round load bounds for join queries in the massively parallel communication model
---

In a single round of [MapReduce](/mapreduce-model/), a reducer can produce an output only if it receives every input that the output depends on. If each reducer may receive at most $q$ inputs, then many inputs must be sent to several reducers. Afrati, Das Sarma, Salihoglu and Ullman (2013) turned this into a lower bound on the replication rate $r$, the average number of reducers that an input goes to, as a function of $q$. The bound is tight for Hamming distance 1 and for matrix multiplication, and tight up to a constant factor for triangles.

## Statement

**The model.** A problem has a finite set $I$ of possible inputs and a set $O$ of possible outputs, and each output $o$ depends on a set of inputs. A mapping schema with reducer size $q$ assigns each input to a set of reducers so that:

1. each reducer $i$ receives $q_i \le q$ inputs;
2. for each output $o$, some reducer receives all the inputs that $o$ depends on.

The replication rate is

$$
r = \frac{1}{|I|} \sum_i q_i ,
$$

so the total communication of the round is $r\,|I|$ input words. The bounds assume the worst case, in which every possible input is present.

**Theorem (the recipe of Section 2.5).** Let $g(q)$ be an upper bound on the number of outputs that a reducer with $q$ inputs can cover, such that $g(q)/q$ is nondecreasing in $q$. Then every mapping schema with reducer size $q$ has

$$
r \ge \frac{q\,|O|}{g(q)\,|I|}.
$$

**Lemma (Lemma 3.1).** A set of $q$ strings of $b$ bits contains at most $\frac{q}{2}\log_2 q$ pairs at Hamming distance 1.

**Corollary (Theorem 3.2).** For the problem of finding all pairs at [Hamming distance](/hamming-distance/) 1 among strings of $b$ bits, every mapping schema with reducer size $q \ge 2$ has $r \ge b / \log_2 q$.

## In plain words

Think of a reducer as a table where a group of inputs meet. An answer can be found only at a table where all its inputs sit together. Small tables are cheap to run, but each one can hold only a few inputs, and a few inputs can only produce a few answers. So to find all the answers, the inputs must sit at many tables, and copying each input to many tables costs network traffic. The theorem counts this. If we know the largest number of answers that one small table can find, then we know how many tables we need in total, and from that how many times, on average, each input must be copied. Smaller tables mean more copies. The bound says exactly how much more.

## Proof

**The recipe.** Every output must be covered by some reducer, so $\sum_i g(q_i) \ge |O|$. Since $g(q)/q$ is nondecreasing and $q_i \le q$,

$$
g(q_i) = q_i \cdot \frac{g(q_i)}{q_i} \le q_i \cdot \frac{g(q)}{q}.
$$

So $|O| \le \frac{g(q)}{q} \sum_i q_i$, which gives $\sum_i q_i \ge q|O|/g(q)$. Divide by $|I|$. $\square$

**The lemma.** Let $P(S)$ be the number of pairs at distance 1 in a set $S$. We prove $P(S) \le \frac{|S|}{2}\log_2 |S|$ by induction on $b$. For $b = 0$, or $|S| \le 1$, there are no pairs. For $b \ge 1$, split $S$ by the first bit into $S_0$ and $S_1$, of sizes $a \le c$ with $a + c = q$ (swap the names if needed). A pair at distance 1 either lies inside $S_0$, lies inside $S_1$, or differs in the first bit only. Inside each part, drop the first bit; this keeps the distances, so the induction hypothesis on $b - 1$ applies. A string of $S_0$ has at most one partner of the third kind, the string that differs from it in the first bit only, so there are at most $a$ such pairs. If $a = 0$ we are done. Otherwise, with $x = a/q \in (0, 1/2]$ and the binary entropy $H(x) = -x\log_2 x - (1-x)\log_2(1-x)$,

$$
P(S) \le \frac{a}{2}\log_2 a + \frac{c}{2}\log_2 c + a = \frac{q}{2}\log_2 q - \frac{q}{2}H(x) + xq.
$$

$H$ is concave with $H(0) = 0$ and $H(1/2) = 1$, so $H(x) \ge 2x$ on $[0, 1/2]$, and the last two terms add up to at most $0$. $\square$

**The corollary.** Here $|I| = 2^b$ and $|O| = b\,2^{b-1}$, since each of the $2^b$ strings has $b$ neighbours and each pair is counted twice. By the lemma, $g(q) = \frac{q}{2}\log_2 q$, and $g(q)/q = \frac12 \log_2 q$ is nondecreasing. The recipe gives

$$
r \ge \frac{q \cdot b\,2^{b-1}}{\frac{q}{2}\log_2 q \cdot 2^b} = \frac{b}{\log_2 q}. \qquad \square
$$

## Consequences

**Triangles (Section 4.1).** Find all triangles in a graph on $n$ vertices; the inputs are the $\binom{n}{2}$ possible edges and the outputs are the $\binom{n}{3}$ possible [triangles](/triangle-counting/). The paper shows that $q$ edges cover at most $g(q) = \frac{\sqrt{2}}{3} q^{3/2}$ triangles; the extreme case is a clique on about $\sqrt{2q}$ vertices. The recipe gives

$$
r \ge \frac{q \binom{n}{3}}{\frac{\sqrt 2}{3} q^{3/2} \binom{n}{2}} = \frac{n - 2}{\sqrt{2q}},
$$

which the paper writes as about $n/\sqrt{2q}$.

**Matrix multiplication (Section 6.1).** Multiply two $n \times n$ matrices, as in [naive matrix multiplication](/naive-matrix-multiplication/). The inputs are the $2n^2$ entries and the outputs are the $n^2$ entries of the product; output $(i, k)$ needs row $i$ of the first matrix and column $k$ of the second. A reducer that holds $a$ whole rows and $c$ whole columns uses $q \ge (a + c)n$ inputs and covers $ac \le (q/2n)^2$ outputs, so $g(q) = q^2/(4n^2)$ and

$$
r \ge \frac{q \cdot n^2}{\frac{q^2}{4n^2} \cdot 2n^2} = \frac{2n^2}{q}.
$$

**The trade-off.** In all three cases $r$ falls as $q$ grows, and $q = |I|$ gives $r = 1$ with one reducer that does all the work. A user chooses a point on the curve: a small $q$ gives many small reducers that run in parallel and fit in memory, at the price of more communication. The bounds hold for one round only; with two rounds, matrix multiplication can use less total communication for some values of $q$, as the paper shows.

**Relation to load bounds.** The communication of a round is $r|I|$ in total, and the largest reducer input is $q$. In the [MRC](/mrc-model/) and MPC models, $q$ is the memory of a machine. Beame, Koutris and Suciu prove one-round bounds of the same kind for join queries, stated as the load on the busiest of $p$ servers. In the [h-relation](/h-relation/) view of BSP, $q$ bounds the words that one reducer receives.

## Tightness

**Hamming distance 1: the splitting algorithm (Section 3.3).** Let $k$ divide $b$. Cut each string into $k$ segments of $b/k$ bits. Reducer $(i, z)$ is for segment $i$ and the value $z$ of the other $b - b/k$ bits; it receives every string whose bits outside segment $i$ equal $z$. Two strings at distance 1 differ in one bit, which lies in one segment $i$, and they agree outside it, so they meet at reducer $(i, z)$. Each string goes to $k$ reducers, so $r = k$, and each reducer receives $q = 2^{b/k}$ strings. Then $b/\log_2 q = b/(b/k) = k = r$: the bound holds with equality. The lemma is tight on these sets, since a subcube of dimension $d$ has $q = 2^d$ strings and exactly $d\,2^{d-1} = \frac{q}{2}\log_2 q$ pairs.

| $b$ | $k$ | $q$ | reducers | $r$ | $b/\log_2 q$ |
|---|---|---|---|---|---|
| 4 | 1 | 16 | 1 | 1 | 1 |
| 4 | 2 | 4 | 8 | 2 | 2 |
| 4 | 4 | 2 | 32 | 4 | 4 |
| 12 | 3 | 16 | 768 | 3 | 3 |

For $b = 4$ there are $4 \cdot 2^3 = 32$ pairs at distance 1, and for $k = 4$ each of the 32 reducers finds exactly one of them.

**Matrix multiplication.** Split the rows of the first matrix into $s$ groups of $n/s$ rows, and the columns of the second into $s$ groups. Reducer $(G, H)$ receives row group $G$ and column group $H$, so $q = 2n^2/s$ and each entry goes to $s$ reducers. Then $r = s = 2n^2/q$, equal to the bound.

**Triangles.** Split the vertices into $k$ groups of $n/k$. For each multiset $\{a, b, c\}$ of three groups there is a reducer that receives the edges between vertices of these groups. An edge with ends in groups $a$ and $b$ goes to the $k$ multisets $\{a, b, c\}$, so $r = k$. A reducer with three different groups receives $3(n/k)^2$ edges, so $q = 3n^2/k^2$ and $r = \sqrt{3}\,n/\sqrt{q}$, which is $\sqrt{6} \approx 2.45$ times the bound $n/\sqrt{2q}$.

| $n$ | $k$ | $q$ | reducers | $r$ | $(n-2)/\sqrt{2q}$ |
|---|---|---|---|---|---|
| 6 | 1 | 15 | 1 | 1 | 0.73 |
| 9 | 3 | 27 | 10 | 3 | 0.95 |
| 12 | 4 | 27 | 20 | 4 | 1.36 |
| 30 | 5 | 108 | 35 | 5 | 1.91 |

The implementation of this page checks the splitting algorithm against a brute-force search for all $b \le 10$, checks the lemma on every subset of the strings for $b \le 4$, finds every triangle with the group schema and compares the result with brute force on random graphs, and checks the matrix schema.

## History

Afrati and Ullman studied the communication of multiway joins in one round in 2010, with the shares method that is now called the [hypercube join](/hypercube-shares-join/). Afrati, Das Sarma, Salihoglu and Ullman wrote the general model of inputs, outputs and mapping schemas, the recipe and the bounds above in "Upper and lower bounds on the cost of a map-reduce computation" (PVLDB 2013). The same year, Beame, Koutris and Suciu gave one-round and multi-round load bounds for queries in the massively parallel communication model. The textbook of Leskovec, Rajaraman and Ullman teaches reducer size and replication rate in its MapReduce chapter.

## References
