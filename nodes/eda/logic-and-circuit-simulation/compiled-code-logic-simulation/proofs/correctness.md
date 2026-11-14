---
title: The levelized bit-parallel program computes every output for every vector of the block
proves: [correctness]
status: full
---

Let $C$ be a netlist with primary inputs, gates $g$ with functions $f_g$ built from AND, OR, NAND, NOR, XOR, XNOR, NOT and BUF, and nets that are each driven by one input or one gate. Lines L1 to L8 refer to the pseudocode of the page. The gate graph has an edge from gate $h$ to gate $g$ when $\mathrm{out}(h)$ is an input of $g$.

**Lemma 1 (levelization).** Line L1 gives a level to every gate if and only if the gate graph has no cycle. When it does, the order by increasing level puts every gate after each gate that drives one of its inputs.

*Proof.* Kahn's algorithm keeps, for each gate, the number of distinct gate-driven inputs that have no level yet, and puts a gate into the queue when the number reaches 0. If the graph has a cycle, no gate on the cycle can enter the queue first, because each of them waits for its predecessor on the cycle. So some gate gets no level. If the graph has no cycle, suppose some gates never enter the queue. Each of them has an input driven by another gate that never enters the queue, since all its other inputs got levels and lowered its count. Following these inputs backwards gives an infinite walk among finitely many gates, so a cycle, which is a contradiction. When gate $g$ gets its level, all its inputs have levels, and $\mathrm{level}(\mathrm{out}(g)) = 1 + \max$ of them, so every driver of an input of $g$ has a smaller level and comes before $g$ in the order by level. $\square$

**Lemma 2 (lanes).** For words $x, y$ of $W$ bits and $M = 2^W - 1$, bit $j$ of $x \,\&\, y$, $x \mid y$, $x \oplus y$ and $x \oplus M$ is the AND, OR, XOR of bit $j$ of $x$ and of $y$, and the NOT of bit $j$ of $x$. So, for every gate function $f_g$, bit $j$ of the word expression of L3 equals $f_g$ applied to bit $j$ of the input words.

*Proof.* The bitwise operations are defined bit by bit. Bit $j$ of $M$ is 1 for $0 \le j < W$, and $b \oplus 1 = \lnot b$. The expressions for NAND, NOR and XNOR are the expressions for AND, OR and XOR followed by XOR with $M$. $\square$

**Theorem.** Let $C$ have no loop. For every block of vectors $v_1, \ldots, v_B$ with $B \le W$ and every $j \le B$, after line L7, bit $j - 1$ of $\mathrm{word}[n]$ is the value of net $n$ in $C$ under vector $v_j$, for every net $n$. So line L8 returns the correct output values.

*Proof.* Line L6 makes the claim true for the primary inputs. The program assigns each gate output once, in the order of Lemma 1. Induction along the program: when the statement of gate $g$ runs, every input of $g$ is a primary input or the output of a gate whose statement came earlier, so by induction its word holds the correct value in every lane. By Lemma 2, lane $j - 1$ of the new word is $f_g$ of the correct input values under $v_j$, which is the value of $\mathrm{out}(g)$ under $v_j$, since in a loop-free circuit the value of each net is fixed by its function and the values of its inputs. $\square$

The lanes $B, \ldots, W - 1$ of a short last block hold the values for the all-zero vector. Line L8 reads only the lanes $0$ to $B - 1$, so they do no harm.
