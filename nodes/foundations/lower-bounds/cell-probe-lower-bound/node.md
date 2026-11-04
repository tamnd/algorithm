---
tag: E3Q68P
kind: technique
slug: cell-probe-lower-bound
name: Cell-probe lower bounds
aliases:
- cell probe lower bound method
- Yao cell-probe bound
- data structure lower bound techniques
area: foundations/lower-bounds
level: research
summary: Methods that prove a data structure must probe many memory cells, by turning a fast structure into a short message, protocol or encoding that cannot exist.
prereqs: [cell-probe-model, communication-complexity, counting-argument]
see_also: [round-elimination, predecessor-lower-bound, dynamic-partial-sums-lower-bound, static-dictionary-lower-bound, dynamic-connectivity-lower-bound, yao-minimax-principle, adversary-argument, randomized-communication-complexity]
sources:
  - paper: doi:10.1145/322261.322274
    title: "Andrew Chi-Chih Yao, Should Tables Be Sorted?, Journal of the ACM 28(3) (1981), 615-628"
    locator: the cell-probe model and the Ramsey argument for implicit tables
  - paper: doi:10.1006/jcss.1998.1577
    title: "Peter Bro Miltersen, Noam Nisan, Shmuel Safra and Avi Wigderson, On Data Structures and Asymmetric Communication Complexity, Journal of Computer and System Sciences 57(1) (1998), 37-49"
    locator: Lemma 1 (from data structures to protocols), Section 3.1 (Lemma 5, the richness lemma), Theorem 9 (membership), and the round elimination lemma
  - paper: doi:10.1145/195058.195415
    title: "Peter Bro Miltersen, Lower bounds for union-split-find related problems on random access machines, Proceedings of the 26th Annual ACM Symposium on Theory of Computing (STOC 1994), 625-634"
    locator: the communication game view of a static cell-probe scheme
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (STOC 1989), 345-354"
    locator: the chronogram method
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 5 (the information transfer method) and Section 3.1 (the limits of the chronogram method)
  - paper: doi:10.1016/j.jcss.2007.06.016
    title: "Pranab Sen and S. Venkatesh, Lower bounds for predecessor searching in the cell probe model, Journal of Computer and System Sciences 74(3) (2008), 364-385"
    locator: Result 2 (the round elimination lemma)
  - paper: doi:10.1145/1132516.1132551
    title: "Mihai Patrascu and Mikkel Thorup, Time-space trade-offs for predecessor search, Proceedings of the 38th Annual ACM Symposium on Theory of Computing (STOC 2006), 232-240"
    locator: the cell-probe elimination lemma and the limits of communication proofs
  - paper: doi:10.1109/focs.2010.82
    title: "Rina Panigrahy, Kunal Talwar and Udi Wieder, Lower Bounds on Near Neighbor Search via Metric Expansion, Proceedings of the 51st Annual IEEE Symposium on Foundations of Computer Science (FOCS 2010), 805-814"
    locator: the cell sampling method
  - paper: doi:10.1109/focs.2012.21
    title: "Kasper Green Larsen, Higher Cell Probe Lower Bounds for Evaluating Polynomials, Proceedings of the 53rd Annual IEEE Symposium on Foundations of Computer Science (FOCS 2012), 293-301"
    locator: cell sampling for static polynomial evaluation
  - paper: doi:10.1145/2213977.2213987
    title: "Kasper Green Larsen, The cell probe complexity of dynamic range counting, Proceedings of the 44th Annual ACM Symposium on Theory of Computing (STOC 2012), 85-94"
    locator: chronogram combined with cell sampling for dynamic range counting
  - paper: doi:10.1145/3188745.3188790
    title: "Kasper Green Larsen, Omri Weinstein and Huacheng Yu, Crossing the logarithmic barrier for dynamic Boolean data structure lower bounds, Proceedings of the 50th Annual ACM Symposium on Theory of Computing (STOC 2018), 978-989"
    locator: super-logarithmic bounds for queries with one-bit answers
---

A cell-probe lower bound shows that every data structure for a problem must read or write many memory cells, whatever operations it may apply to the words it reads. The [cell-probe model](/cell-probe-model/) counts only probes, so such a bound holds on every word RAM and in external memory. All the methods share one plan: assume a structure that is too fast, and turn it into an object that is too small to carry the information the problem needs, such as a short protocol, a short encoding or a small decision tree. This page collects the methods, states their key lemmas exactly, and points to the pages that carry out the full proofs.

## In plain words

A data structure keeps facts in memory words. A question or a change touches some of those words. To show that some touches are unavoidable, pretend that a structure touches only a few words, and then show that this pretence lets you do something impossible. You could send a whole input in a message that is too short. You could win a guessing game with too few questions. Or you could squeeze random data into fewer bits than its size. Each method picks a different impossible task. Some suit structures that never change, some suit structures that change, and some count only how much news flows from old changes to new questions. The answers say how many memory words any method must touch, and so how fast any program can be.

## When it applies

Use the method for a data structure problem whose cost is the number of memory accesses: static problems with space $s$ cells of $w$ bits and query probes $t$, and dynamic problems with update probes $t_u$ and query probes $t_q$. The bound then holds for every instruction set and every amount of free computation.

The method does not apply when the cost is the number of comparisons or algebraic operations, which is the setting of the [decision tree method](/decision-tree-method/). It also gives nothing for a problem that has a cheap structure in the cell-probe model but not on a real machine, since the model ignores computation.

There are known ceilings. For a static problem with $d$ possible queries, a communication proof cannot show more than $t = \lg d / \lceil \lg s \rceil$ (see Pitfalls). For many years the largest known bounds were about $\lg n$ for static problems with linear space and about $\lg^2 n$ for dynamic problems, both by Larsen (2012).

## The template

1. *Fix the model.* State the cell size $w$, the number of cells $s$, the cost ($t$, or $t_u$ and $t_q$), and whether costs are worst case, amortized or expected. For a dynamic problem with amortized costs, bound the total cost of one long sequence of operations.
2. *Choose a hard input distribution.* By the easy direction of the [minimax principle](/yao-minimax-principle/), a bound on the expected cost of deterministic structures on a fixed distribution also bounds randomized Las Vegas structures.
3. *Turn the structure into a small object.* Pick one of the methods below. A static structure becomes a communication protocol or a short encoding. A dynamic structure is cut into time periods, and the reads that cross a period boundary become an encoding.
4. *Show that the object is too small.* Compare its size with the information it must carry, by counting, by a communication lower bound, or by entropy.
5. *Solve for the cost.* The inequality from step 4 contains $t$, $s$ and $w$. Solve it for $t$, and choose free parameters of the hard instance to make the bound as large as possible.

## Classic examples

### Ramsey and an adversary for implicit tables

Yao (1981) defined the model and asked whether a table that holds exactly the $n$ keys should be sorted. When the universe is large enough, Ramsey's theorem shows that every storage rule is the sorted rule on some set of $2n - 1$ keys, and an adversary then forces $\lceil \lg(n+1) \rceil$ probes. The full proof is on [the static dictionary lower bound](/static-dictionary-lower-bound/) page. The method needs a model with very little freedom, and it does not extend to tables with extra cells.

### Communication and the richness lemma

**Lemma (Miltersen 1994; Lemma 1 of MNSW).** A static scheme with $s$ cells of $w$ bits and $t$ probes per query gives a deterministic protocol in which Alice (the query) and Bob (the input) alternate $2t$ messages. Alice speaks first, each of her messages has $\lceil \lg s \rceil$ bits (an address), and each of Bob's has $w$ bits (the contents).

In an $[a, b]$-protocol Alice sends $a$ bits in total and Bob sends $b$ bits in total. Write $f$ as a matrix with Alice's inputs as rows and Bob's inputs as columns. Call $f$ *$(u, v)$-rich* if at least $v$ columns contain at least $u$ entries equal to $1$.

**Lemma (richness; MNSW Lemma 5).** If $f$ is $(u, v)$-rich and has a deterministic $[a, b]$-protocol, then $f$ has an all-ones submatrix with at least $u / 2^a$ rows and at least $v / 2^{a+b}$ columns. With a randomized protocol with one-sided error, the bounds become $u / 2^{a+2}$ and $v / 2^{a+b+2}$.

*Proof of the deterministic case.* Induction on $a + b$. With no communication the answer is a constant, so it is $1$ on the whole matrix, which has at least $u$ rows and $v$ columns. If Alice sends the first bit, her rows split into two halves $f_0$ and $f_1$. Each rich column has at least $u/2$ ones in one of the halves, so one half, say $f_0$, is $(u/2, v/2)$-rich and has an $[a-1, b]$-protocol. The induction gives a rectangle of $(u/2)/2^{a-1}$ by $(v/2)/2^{a-1+b}$. If Bob sends the first bit, his columns split, one half is $(u, v/2)$-rich with an $[a, b-1]$-protocol, and the induction gives $u/2^a$ by $(v/2)/2^{a+b-1}$. $\square$

To use the lemma, show that $f$ is rich and that it has no large all-ones submatrix, then put $a = t \lceil \lg s \rceil$ and $b = t w$. For example, MNSW (Theorem 9) prove that if membership of a point of $\{1, \dots, N\}$ in a set of size $l$ has a one-sided-error $[a, b]$-protocol, then $2^a(a + b) = \Omega(l (\lg N - \lg l))$.

### Round elimination

Round elimination removes the first message of a protocol at a small cost in error, when the sender does not know which of $k$ independent sub-problems matters. The exact lemma of Sen and Venkatesh, the self-reductions, and the full parameter choice are on [the predecessor lower bound](/predecessor-lower-bound/) page, where they give the Beame and Fich bound $\Omega(\lg \ell / \lg\lg \ell)$. See also [round elimination](/round-elimination/).

### The chronogram

Fredman and Saks (1989) proved the first dynamic bounds. Run a long sequence of random updates, cut it into *epochs* that grow geometrically backwards in time, with ratio $\beta$ somewhat larger than $t_u$ and $w$, and end with one query. The epochs after epoch $i$ contain far fewer updates than epoch $i$ itself, so they write too few cells to describe what epoch $i$ did. The query must then read a cell written during epoch $i$, for each of about $\log_\beta n$ epochs. For partial sums over $\mathbb{Z}/2$ this gives $t_q \cdot \lg(w\, t_u) = \Omega(\lg n)$. The method cannot give more than $\max\{t_u, t_q\} = \Omega(\lg n / \lg\lg n)$ for word size $\Theta(\lg n)$.

### Information transfer

Patrascu and Demaine (2004, journal 2006) put the operations as leaves of a balanced binary tree of time. At each node they count the reads in the right half of cells last written in the left half. An encoding argument shows that this count must cover the entropy that the left half's updates give to the right half's answers, about one word per interleaved pair. Every read is counted at one node only, so the levels add up to $\Omega(\lg n)$ per operation. [The dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/) carries out the full proof with explicit constants. The same paper proves $\Omega(\lg n)$ for [dynamic connectivity](/dynamic-connectivity-lower-bound/).

### Cell sampling

Panigrahy, Talwar and Wieder (2010) introduced cell sampling, and Larsen (2012) sharpened it. Pick a random subset $C$ of the $s$ cells of a static structure. A query whose $t$ probes all fall in $C$ can be answered from $C$ alone. With $|C|$ a small fraction of the input size in words, a query is answered from $C$ with probability about $(|C|/s)^t$. If the queries answered from $C$ determine more bits of the input than $|C|$ cells can encode, the structure cannot exist. Larsen used this for evaluating a polynomial of degree $n$ over a field $\mathbb{F}$ with $|\mathbb{F}| \ge n^{1+\Omega(1)}$ and proved $t = \Omega(\lg |\mathbb{F}| / \lg(s w / (n \lg |\mathbb{F}|)))$. For space linear in the input, $s w = O(n \lg |\mathbb{F}|)$, this is $\Omega(\lg |\mathbb{F}|)$.

## Variations

- *Chronogram plus cell sampling.* Larsen (STOC 2012) applies cell sampling inside each epoch and proves $t_q = \Omega((\lg n / \lg(w\, t_u))^2)$ for dynamic weighted orthogonal range counting in the plane.
- *Queries with one-bit answers.* Information transfer as stated needs answers of many bits. Patrascu and Demaine adapt it for connectivity, and Larsen, Weinstein and Yu (2018) proved the first super-logarithmic bounds for dynamic problems with one-bit answers.
- *Cell-probe elimination.* Patrascu and Thorup (2006) eliminate probes directly in the cell-probe model instead of messages in a protocol. This sees the difference between space $n^{1+o(1)}$ and $n^{1+\varepsilon}$, which communication cannot see.
- *Randomization and nondeterminism.* The minimax principle covers Las Vegas structures. The round elimination lemma of Sen and Venkatesh covers protocols with two-sided error, and the richness lemma covers protocols with one-sided error.
- *Other cell sizes.* The [bit-probe model](/bit-probe-model/) is the case $w = 1$. External memory with pages of $B$ items of $\ell$ bits is the case $w = B \ell$.

## Pitfalls

- *Communication proofs have a ceiling.* Alice can send her whole query in $\lceil \lg d \rceil$ bits, where $d$ is the number of queries. A $t$-probe scheme gives her $t \lceil \lg s \rceil$ bits, so a proof that only uses the protocol cannot show $t > \lceil \lg d \rceil / \lceil \lg s \rceil$. For $d$ and $s$ polynomial in $n$ this is a constant. The same reason hides the difference between space $n$ and space $n^2$, since it changes $\lceil \lg s \rceil$ by a factor of $2$ only.
- *Huge cells make bounds empty.* With unbounded $w$ one cell can hold the whole input, and every problem has a one-probe structure. State $w$, and keep it close to the size of a key or an answer.
- *State the space in the right unit.* A bound for $s$ cells is not a bound for $s$ bits. Compare with the [counting](/counting-argument/) bound for the input in bits.
- *Amortized and worst case differ.* The chronogram and information transfer bounds hold for amortized costs. A bound proved only for worst-case costs is weaker.
- *Free computation cuts both ways.* A cell-probe upper bound may hide a large computation. A cell-probe lower bound is strong because of this freedom, but a matching cell-probe structure is not always a fast program.

## Exercises

1. Prove the lemma of Miltersen: from a static scheme with $s$ cells of $w$ bits and $t$ probes, build the protocol with $2t$ messages of $\lceil \lg s \rceil$ and $w$ bits.
2. Show that a static scheme for a problem with $d$ queries and answers of at most $w$ bits exists with $t = 1$ and $s = d$. Explain why this forces every useful lower bound to depend on $s$.
3. Let $f$ be $(u, v)$-rich, and suppose that every all-ones submatrix with at least $u / 2^a$ rows has fewer than $v / 2^{a+b}$ columns. Conclude that $f$ has no deterministic $[a, b]$-protocol. Then put $a = t \lceil \lg s \rceil$ and $b = t w$ and state the resulting bound on $t$.
4. In the time tree of the bit-reversal sequence on [the partial sums page](/dynamic-partial-sums-lower-bound/), compute the total interleaving for $n = 16$. Check that it equals $n + n \lg n / 2 = 48$.
5. A tree of fan-out $B$ stores at each node the prefix sums of its children. Show that it answers partial sums with $t_q = O(\log_B n)$ and $t_u = O(B \log_B n)$, and that this meets the trade-off $t_q \lg(t_u / t_q) = \Omega(\lg n)$ up to a constant factor.
6. Explain why the chronogram with ratio $\beta$ gives about $\log_\beta n$ epochs, and why $\beta$ must exceed $t_u$ for the argument to work.

## References
