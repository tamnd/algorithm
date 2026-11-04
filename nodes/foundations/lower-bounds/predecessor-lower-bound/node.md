---
tag: YGFBK1
kind: theorem
slug: predecessor-lower-bound
name: Predecessor search lower bound
aliases:
- Beame-Fich bound
- Patrascu-Thorup predecessor bound
- predecessor search time-space trade-off
area: foundations/lower-bounds
level: research
summary: A static predecessor structure with polynomial space needs Omega(min(log l / log log l, sqrt(log n / log log n))) probes (Beame and Fich); Patrascu and Thorup found the exact time-space trade-off.
prereqs: [cell-probe-model, predecessor-problem, communication-complexity]
see_also: [round-elimination, fusion-tree, binary-search, cell-probe-lower-bound, static-dictionary-lower-bound, dynamic-partial-sums-lower-bound, sorted-search-lower-bound, randomized-communication-complexity]
sources:
  - paper: doi:10.1006/jcss.2002.1822
    title: "Paul Beame and Faith E. Fich, Optimal Bounds for the Predecessor Problem and Related Problems, Journal of Computer and System Sciences 65(1) (2002), 38-72"
    locator: the journal version of the lower bound and the matching upper bound
  - paper: doi:10.1145/301250.301323
    title: "Paul Beame and Faith E. Fich, Optimal bounds for the predecessor problem, Proceedings of the 31st Annual ACM Symposium on Theory of Computing (STOC 1999), 295-304"
    locator: Theorem 3 (the upper bound), Theorems 5, 6 and 7 (the lower bounds)
  - paper: doi:10.1016/j.jcss.2007.06.016
    title: "Pranab Sen and S. Venkatesh, Lower bounds for predecessor searching in the cell probe model, Journal of Computer and System Sciences 74(3) (2008), 364-385"
    locator: Result 1 (the randomized lower bound) and Result 2 (the round elimination lemma)
  - paper: doi:10.1145/1132516.1132551
    title: "Mihai Patrascu and Mikkel Thorup, Time-space trade-offs for predecessor search, Proceedings of the 38th Annual ACM Symposium on Theory of Computing (STOC 2006), 232-240"
    locator: Section 1.3 (the optimal trade-off and its four branches) and Sections 1.3.1 to 1.3.4 (consequences)
  - paper: doi:10.1006/jcss.1998.1577
    title: "Peter Bro Miltersen, Noam Nisan, Shmuel Safra and Avi Wigderson, On Data Structures and Asymmetric Communication Complexity, Journal of Computer and System Sciences 57(1) (1998), 37-49"
    locator: Lemma 1 (from data structures to protocols), the round elimination lemma, and Section 4.2 (the self-reductions for prefix parity)
  - paper: doi:10.1007/BF02126797
    title: "Miklos Ajtai, A lower bound for finding predecessors in Yao's cell probe model, Combinatorica 8(3) (1988), 235-247"
    locator: the first superconstant lower bound for polynomial space
  - paper: doi:10.1145/195058.195415
    title: "Peter Bro Miltersen, Lower bounds for union-split-find related problems on random access machines, Proceedings of the 26th Annual ACM Symposium on Theory of Computing (STOC 1994), 625-634"
    locator: the communication game view of cell-probe schemes and the colored predecessor problem
  - paper: doi:10.1145/3409371
    title: "Gonzalo Navarro and Javiel Rojas-Ledesma, Predecessor Search, ACM Computing Surveys 53(5) (2021), 1-35"
    locator: survey of upper and lower bounds
---

The predecessor problem stores a set $Y$ of $n$ integers of $\ell$ bits and answers, for a query $x$, the largest element of $Y$ that is at most $x$. In the [cell-probe model](/cell-probe-model/), Beame and Fich (1999) proved that a structure with polynomial space and polylogarithmic word size needs $\Omega(\lg \ell / \lg\lg \ell)$ probes for some $n$, and $\Omega(\sqrt{\lg n / \lg\lg n})$ probes for some $\ell$, and they gave a structure that matches both. Sen and Venkatesh (2008) extended the bound to randomized queries with a sharper round elimination lemma. Patrascu and Thorup (2006) then found the optimal query time for every space bound, which shows that the van Emde Boas bound $O(\lg \ell)$ is optimal for near-linear space.

## Statement

**The problem.** A static structure stores a set $Y \subseteq \{0, \dots, 2^\ell - 1\}$ with $|Y| = n$. A query $x \in \{0, \dots, 2^\ell - 1\}$ returns $\max\{y \in Y : y \le x\}$, or a special value if there is none. In the *colored* version each element of $Y$ has a color bit, and the query returns only the color of the predecessor. A plain structure answers the colored version with one more probe, into a perfect hash table that maps each key to its color and uses $O(n)$ more cells. So lower bounds for the colored version hold for the plain one, up to one probe.

**The model.** A static cell-probe scheme with $s$ cells of $w$ bits each. The table is any function of $Y$. The query is a decision tree that probes cells, and its cost $t$ is the number of probes in the worst case over $Y$ and $x$. Preprocessing time is free. A *randomized* scheme may flip coins during the query, and it must give the right answer with probability at least $2/3$ on every $Y$ and $x$.

**Theorem 1 (Beame and Fich 1999; randomized form by Sen and Venkatesh 2008).** Fix constants for the polynomial and the polylogarithm, and suppose that a randomized scheme with $s = n^{O(1)}$ cells of $w = \ell^{O(1)}$ bits answers predecessor queries with $t$ probes and error less than $1/3$. Then there is a constant $c > 0$ such that:

- for every large enough $\ell$ there is a value of $n$ with $t \ge c \lg \ell / \lg\lg \ell$;
- for every large enough $n$ there is a value of $\ell$ with $t \ge c \sqrt{\lg n / \lg\lg n}$.

Beame and Fich proved this for deterministic schemes. Their bound in terms of $\ell$ holds even with cells of $2^{\ell^{1-\varepsilon}}$ bits for a constant $\varepsilon > 0$ (Theorem 6 of the STOC version).

**Theorem 2 (Patrascu and Thorup 2006).** Let $\lg n \le \ell \le w$ and let the structure use $S$ words of $w$ bits. Write $L(x) = \lceil \log_2(x + 2) \rceil$ and $a = L(S/n) + L(w)$. Then the optimal worst-case query time is, up to constant factors,

$$\min\left\{\ \log_w n,\quad L\!\left(\frac{\ell - L(n)}{a}\right),\quad \frac{L(\ell/a)}{L\!\left(\frac{a}{L(n)} \cdot L(\ell/a)\right)},\quad \frac{L(\ell/a)}{L\!\left(L(\ell/a) \,/\, L\!\left(\frac{L(n)}{a}\right)\right)}\ \right\}.$$

The lower bound holds for deterministic queries on the colored problem in the cell-probe model. When $S \ge n^{1+\varepsilon}$ for a constant $\varepsilon > 0$, it also holds in the communication model with two-sided-error randomization. The upper bound is a deterministic query on a word RAM, and the structure can be built from a sorted list in expected $O(S)$ time.

## In plain words

Finding the largest stored number below a given one looks easy, and binary search does it in a number of steps that grows with the logarithm of the set size. Clever bit tricks do much better on a computer. This theorem says how much better they can ever be. Picture a game between the person who asks and the memory. The person asks for one memory word at a time, and the memory answers. Each question carries a short address and each answer carries one word. A careful argument removes the first exchange of the game at a small cost: the keys get much shorter or the set gets much smaller. After a few such removals nothing is left, yet the answer must still be right. So the game needs a minimum number of exchanges. A later result found the exact best number for every amount of memory.

## Proof

This is a sketch of the proof of Theorem 1 by round elimination, along the route of Miltersen, Nisan, Safra and Wigderson and of Sen and Venkatesh. Each lemma is stated exactly. The bookkeeping of rounding and divisibility in Step 5 is left out. The proof of Theorem 2 uses a different tool, the cell-probe elimination lemma of Patrascu and Thorup, and is not given here.

**Step 1: a simpler problem.** In *prefix parity* $P(\ell, n)$, Alice holds $x \in \{0,1\}^\ell$ and Bob holds a set $Y$ of at most $n$ strings in $\{0,1\}^\ell$. The answer is the parity of $|\{y \in Y : y \le x\}|$, with strings compared as binary numbers. Give each key the parity of its rank as its color. Then colored predecessor answers prefix parity, so a lower bound for prefix parity is a lower bound for predecessor.

**Step 2: from probes to messages (Miltersen 1994; Lemma 1 of MNSW).** A scheme with $s$ cells of $w$ bits and $t$ probes gives a protocol in which Alice (the query) and Bob (the table) alternate $2t$ messages. Alice speaks first. Each message of Alice is an address of $\lceil \lg s \rceil$ bits, and each message of Bob is the $w$-bit contents of that cell. A randomized scheme gives a public-coin protocol with the same error.

**Step 3: round elimination (Sen and Venkatesh 2008, Result 2).** For a function $f(x, y)$ and an integer $k \ge 1$ define $f^{(k),A}$: Alice holds $x_1, \dots, x_k$, Bob holds $i \in \{1, \dots, k\}$, $y$, and $x_1, \dots, x_{i-1}$, and the answer is $f(x_i, y)$. Define $f^{(k),B}$ in the same way with the roles of Alice and Bob exchanged. Suppose that $f^{(k),A}$ has a public-coin protocol with error less than $\varepsilon$ in which Alice sends the first message, of $m_1$ bits, followed by messages of $m_2, \dots, m_r$ bits. Then $f$ has a public-coin protocol with error less than

$$\varepsilon + \tfrac12 \sqrt{2 m_1 \ln 2 / k}$$

in which Bob sends the first message and the messages have $m_2, \dots, m_r$ bits. The same holds with the roles of Alice and Bob exchanged.

**Step 4: two self-reductions (MNSW, Section 4.2).** Both are exact.

- *Alice side.* If $k$ divides $\ell$, then $P(\ell/k, n)^{(k),A}$ reduces to $P(\ell, n)$ with no communication. Alice forms the concatenation $x = x_1 x_2 \cdots x_k$. Bob, who knows $i$ and $x_1, \dots, x_{i-1}$, replaces each key $y$ of his set by $x_1 \cdots x_{i-1}\, y\, 0^{(k-i)\ell/k}$. This key is at most $x$ if and only if $y \le x_i$, so the count, and with it the parity, is unchanged.
- *Bob side.* Let $d = \lceil \lg k \rceil$ and write $[j]$ for the $d$-bit form of $j - 1$. Then $P(\ell', n')^{(k),B}$ reduces to $P(\ell' + d + 1, k(n' + 1))$. Bob holds $Y_1, \dots, Y_k$. He stores the keys $[j]\,0\,y$ for every $y \in Y_j$, and also the key $[j]\,1\,0^{\ell'}$ whenever $|Y_j|$ is odd, so every block holds an even number of keys. Alice, who knows $i$ and $x$, queries $[i]\,0\,x$. The keys at most this query are all keys of the blocks $j < i$, an even number, and the keys $[i]\,0\,y$ with $y \le x$. So the parity is the answer for $(x, Y_i)$.

**Step 5: peel off the rounds.** Start from Step 2 with $2t$ messages, Alice messages of $m_A = \lceil \lg s \rceil$ bits, Bob messages of $w$ bits, and error less than $1/3$. Set $k_A = \lceil 200 \ln 2 \cdot m_A t^2 \rceil$ and $k_B = \lceil 200 \ln 2 \cdot w t^2 \rceil$. Then each use of Step 3 with $k = k_A$ on an Alice message, or with $k = k_B$ on a Bob message, adds at most $\tfrac12 \sqrt{1/(100 t^2)} = 1/(20t)$ to the error. One pair of rounds does the following.

1. The protocol for $P(\ell, n)$ also solves $P(\ell/k_A, n)^{(k_A),A}$ by the Alice side of Step 4. Step 3 removes Alice's first message and gives a protocol for $P(\ell/k_A, n)$ in which Bob speaks first.
2. That protocol also solves $P(\ell', n')^{(k_B),B}$ with $\ell' = \ell/k_A - \lceil \lg k_B \rceil - 1$ and $n' = n/k_B - 1$, by the Bob side of Step 4. Step 3 removes Bob's first message and gives a protocol for $P(\ell', n')$ in which Alice speaks first.

After $t$ pairs no message is left, and the error is less than $1/3 + 2t/(20t) = 13/30 < 1/2$. A protocol with no messages outputs a random bit that does not depend on the inputs. If the final problem still has $\ell_t \ge 1$ and $n_t \ge 1$, then two inputs have different answers, and the protocol errs with probability at least $1/2$ on one of them. This is a contradiction. So a $t$-probe scheme can exist only if the key length or the set size runs out within $t$ pairs, that is only if roughly $\ell < (2k_A)^t \lg k_B$ or $n < (2k_B)^t$.

**Step 6: choose the sizes.** With $s = n^{O(1)}$ and $w = \ell^{O(1)}$, we have $\lg k_A = O(\lg\lg n + \lg t)$ and $\lg k_B = O(\lg \ell + \lg t)$. Take $\lg n = \lceil (\lg \ell)^2 / \lg\lg \ell \rceil$. For $t = c \lg \ell / \lg\lg \ell$ with a small constant $c$, both $t \lg(2k_A) + \lg\lg k_B \le \lg \ell$ and $t \lg(2k_B) < \lg n$ hold for large $\ell$, so Step 5 rules out such a $t$. This gives $t > c \lg \ell / \lg\lg \ell$, and with this choice of $n$ the same quantity is $\Theta(\sqrt{\lg n / \lg\lg n})$. $\blacksquare$

## Consequences

Patrascu and Thorup draw these conclusions from Theorem 2 (Sections 1.3.1 to 1.3.4).

- *Van Emde Boas is optimal for near-linear space.* If $\ell \ge (1 + \varepsilon) \lg n$ and the space is at most $n \cdot 2^{(\lg n)^{1-\varepsilon}}$, which includes $n (\lg n)^{O(1)}$, the optimal time is $\Theta(\lg \ell)$. This is the bound of the van Emde Boas structure, see [the predecessor problem](/predecessor-problem/). It was often conjectured that this bound could be improved.
- *Space separates constant from superconstant time.* For polynomial universes ($\ell = O(\lg n)$), space $n^{1+\varepsilon}$ gives constant time, but space $n^{1+o(1)}$ forces $\omega(1)$ time.
- *B-trees are optimal in external memory.* Only the first branch depends on $w$. With pages of $B$ keys, $w = B\ell$, and $\log_w n = \Theta(\min\{\log_\ell n, \log_B n\})$. So the best structure is a B-tree or the best RAM structure that ignores pages, such as a [fusion tree](/fusion-tree/).
- *Dynamic bounds.* If an insertion costs $t_u$ probes, then $n$ insertions followed by a hash table of the changed cells give a static structure with space $O(n t_u)$. So with fast updates, queries cannot beat $\Theta(\lg \ell)$ in general.

The numbers at real sizes are small. For $n = 2^{20}$ keys of $\ell = 64$ bits, $\lg \ell / \lg\lg \ell \approx 2.32$ and $\sqrt{\lg n / \lg\lg n} \approx 2.15$, while van Emde Boas halves the key length $\lg 64 = 6$ times and [binary search](/binary-search/) makes $\lceil \lg(n + 1) \rceil = 21$ comparisons. The theorems speak about growth up to constant factors, so these numbers do not rank the structures at this size.

### Pitfalls

- *"There exists $n$" is part of the statement.* Theorem 1 does not say that every $(n, \ell)$ pair needs $\Omega(\lg \ell / \lg\lg \ell)$ probes. For $\ell = O(\lg n)$ and space $n^{1+\varepsilon}$, Theorem 2 gives constant time.
- *Space must be stated.* With $2^\ell$ cells a table of all answers gives one probe. Every predecessor lower bound is a time-space trade-off, not a bare time bound.
- *The communication method has a ceiling.* A protocol in which Alice sends $\lceil \lg s \rceil$ bits cannot tell $s = n$ from $s = n^2$ apart by more than a constant factor in message length. So Steps 2 to 6 cannot prove the separation between near-linear and polynomial space. Patrascu and Thorup needed a direct cell-probe argument for that.
- *Randomized queries in Theorem 2.* The 2006 paper proves the lower bound for deterministic queries, and in the communication model for space $n^{1+\varepsilon}$. Patrascu and Thorup extended it to randomized queries in a SODA 2007 paper titled "Randomization does not help searching predecessors".
- *Comparison bounds do not apply.* The $\lceil \lg(n+1) \rceil$ bound for [sorted search](/sorted-search-lower-bound/) counts comparisons. Word operations can do better, which is why the answer here is much smaller than $\lg n$.

## Tightness

Theorem 1 is tight. Beame and Fich give a deterministic static structure with polynomial space and query time $O(\min\{\lg \ell / \lg\lg \ell,\ \sqrt{\lg n / \lg\lg n}\})$ (Theorem 3 of the STOC version, with $O(n^4)$ construction time and space there). Combined with exponential search trees, it gives a dynamic structure with $O(n)$ words and time $O(\min\{\lg\lg n \cdot \lg \ell / \lg\lg \ell,\ \sqrt{\lg n / \lg\lg n}\})$ (Corollary 4 of the STOC version). Theorem 2 is tight by its own statement: Patrascu and Thorup give a matching RAM structure for every branch. Branch 1 is a fusion tree or a B-tree, branch 2 is van Emde Boas with two small changes (stop the recursion at $a$ bits and start with a table on the top $\lg n$ bits), and branches 3 and 4 refine the method of Beame and Fich. Patrascu and Thorup also show that the Beame and Fich time can be reached with space $n^{1 + 1/\exp((\lg \ell)^{1-\varepsilon})}$.

## History

Ajtai (1988) proved the first superconstant lower bound for polynomial space. With a correction by Miltersen, it gives $\Omega(\sqrt{\lg \ell})$ for some $n$ and $\Omega(\sqrt[3]{\lg n})$ for some $\ell$. Miltersen (1994) recast the cell-probe scheme as a communication game and proved the bound for the colored problem. Miltersen, Nisan, Safra and Wigderson (1995, journal 1998) isolated the round elimination lemma and extended the bound to randomized schemes. Beame and Fich (STOC 1999, journal 2002) raised the bounds to $\Omega(\lg \ell / \lg\lg \ell)$ and $\Omega(\sqrt{\lg n / \lg\lg n})$ and matched them with a new structure of quadratic space. Sen and Venkatesh proved a stronger round elimination lemma and reproved the Beame and Fich bounds for randomized schemes. Patrascu and Thorup (STOC 2006) found the full trade-off with a new cell-probe elimination lemma.

## References
