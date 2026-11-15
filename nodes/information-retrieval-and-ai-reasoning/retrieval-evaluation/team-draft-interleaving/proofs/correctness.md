---
title: Team-draft interleaving builds teams that alternate in pairs and is fair under clicks that ignore the documents
proves: [correctness]
status: full
---

Let $A$ and $B$ be rankings with no repeated document. Lines refer to the pseudocode on the page. A pick is one run of lines L4 and L5 or of lines L7 and L8.

**Invariant.** Before each test of line L2:

> **(J1)** $I$ has no repeated document, $T_A \cap T_B = \emptyset$, and $T_A \cup T_B$ is the set of documents of $I$.
>
> **(J2)** $|T_A| - |T_B| \in \{-1, 0, 1\}$, and it is 0 after an even number of picks.
>
> **(J3)** Each document $d \in T_A$ was, at the pick that added it, the first document of $A$ not yet in $I$; the same holds for $T_B$ and $B$.

*Initialization.* All three sets are empty and no pick was made.

*Maintenance.* The body runs only when $A$ and $B$ each have a document not in $I$, so lines L4 and L7 are defined. The picked document is not in $I$, so (J1) still holds after it is appended and added to one team, and (J3) holds by the choice in line L4 or L7. For (J2): if the teams have equal size, either team grows and the difference becomes $\pm 1$; if one team is smaller, line L3 gives the pick to the smaller team (to A when $|T_A| < |T_B|$, and to B otherwise, since then $|T_A| > |T_B|$), and the difference becomes 0. So the difference is 0 after picks 0, 2, 4, and so on, and $\pm 1$ after an odd number of picks.

*Termination.* Each pick adds a new document of $A \cup B$ to $I$, so there are at most $|A \cup B|$ picks.

**Claim 1 (pairs).** For each $m \ge 1$ with $2m \le |I|$, one of $I[2m-1]$ and $I[2m]$ is in $T_A$ and the other is in $T_B$.

*Proof.* By (J2) the teams have equal size before pick $2m - 1$. That pick goes to one team, and by (J2) after it the other team is smaller by 1, so line L3 gives pick $2m$ to the other team. $\square$

The coin is called only when the teams have equal size, that is, once at the start of each pair of picks. Call these calls the coins of rounds $1, 2, \ldots$ The coin of round $m$ decides the team of position $2m - 1$: A for 1 and B for 0, and position $2m$, if it exists, goes to the other team.

**Claim 2 (fair coin per position).** Let $A$ and $B$ be orderings of the same set $D$ of $n$ documents, and let the coins be independent fair bits. Then $|I| = n$, and for each position $i$, $\Pr[I[i] \in T_A] = 1/2$.

*Proof.* As both rankings hold the same set, $A$ has a document not in $I$ exactly when $B$ has one, exactly when $I \ne D$. So the loop runs until $I = D$, and $|I| = n$. Position $2m - 1$ is in $T_A$ exactly when the coin of round $m$ is 1, which has probability $1/2$. Position $2m$ is in $T_A$ exactly when that coin is 0, also with probability $1/2$. $\square$

**Claim 3 (no preference under random clicks).** Under the hypothesis of Claim 2, let the user click a set $S$ of positions drawn from any distribution that does not depend on the shown documents or on the coins. Then the expected outcome of CREDIT is 0.

*Proof.* Let $r = \lceil n / 2 \rceil$ be the number of rounds, and let $\varphi$ flip all $r$ coins. By Claim 2's proof, the set of positions in $T_A$ under coins $x$ is $P_A(x) = \{2m - 1 : x_m = 1\} \cup \{2m \le n : x_m = 0\}$, and $P_A(\varphi(x))$ is the set of the other positions, $P_B(x)$. The documents at these positions can differ between $x$ and $\varphi(x)$, but the clicks depend only on positions. So for a fixed $S$, $h_a(\varphi(x)) = |S \cap P_B(x)| = h_b(x)$ and $h_b(\varphi(x)) = h_a(x)$, and the outcome under $\varphi(x)$ is the negative of the outcome under $x$. Since $\varphi$ is a bijection on $\{0, 1\}^r$ and all coin vectors have probability $2^{-r}$, the sum of the outcomes over all coin vectors is 0 for each $S$, and so is its expectation over $S$. $\square$

**Claim 4 (insensitivity).** There are rankings $A$ and $B$ and a click model where clicks go only to relevant documents, $A$ ranks the only relevant document higher than $B$, and the expected outcome is still 0.

*Proof.* Take $A = (d_2, d_3, d_1)$ and $B = (d_1, d_2, d_3)$ with only $d_3$ relevant. In round 1 one ranking picks its first document and the other picks its first document not yet shown, so positions 1 and 2 hold $d_1$ and $d_2$ in some order. In round 2 the only document left is $d_3$, and it goes to the team that the coin of round 2 picks. So $d_3$ is always at position 3, in $T_A$ with probability $1/2$. A click model that clicks only $d_3$ therefore gives each ranking the win with probability $1/2$ times the click probability at position 3. $\square$

**Cost.** The pointers of $A$ and $B$ only move forward past documents already in $I$, so all the scans together take $O(|A| + |B|)$ steps, and each pick costs $O(1)$ expected time with a hash set. CREDIT reads the clicks once. $\blacksquare$
