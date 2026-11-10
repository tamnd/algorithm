---
title: The Ladner-Fischer circuit P_k(n) computes all prefixes with depth at most k + ⌈lg n⌉
proves: [correctness]
status: full
---

**Statement.** Let $\oplus$ be an [associative operator](/associative-operator/). For every $n \ge 1$ and $k \ge 0$, the gates that PREFIX$(w[1..n], k)$ adds form a circuit that leaves $v_1 \oplus \cdots \oplus v_j$ on wire $w[j]$ for each $j$, where $v_1, \ldots, v_n$ are the values on the wires before the call. The circuit uses only the wires $w[1..n]$. Its depth is at most $k + \lceil \lg n \rceil$, and the depth of the last output $w[n]$ is at most $\lceil \lg n \rceil$. In particular $P_0(n)$ has the optimal depth $\lceil \lg n \rceil$.

**Conventions.** A gate on line L6, L8 or L10 sets one wire to (an earlier wire) $\oplus$ (that wire), with the earlier wire on the left. The depth of a wire is the largest number of gates on a path from an input of the call to that wire. We use the identity $\lceil \lg \lceil m/2 \rceil \rceil = \lceil \lg m \rceil - 1$ for $m \ge 2$, which is Lemma 1 of the [parallel reduce proof](/parallel-reduce/), and the fact that $\lceil \lg \cdot \rceil$ does not decrease.

## 1. The result

By strong induction on $n$, for all $k$ at once. For $n = 1$, line L1 adds no gate and $w[1] = v_1$. Let $n \ge 2$.

**Case $k = 0$.** Let $c = \lceil n/2 \rceil$, so $1 \le c < n$. The call on line L4 uses only the wires $w[1..c]$, and the call on line L5 uses only $w[c+1..n]$, so the two calls do not interfere. By the induction hypothesis, after them $w[j] = v_1 \oplus \cdots \oplus v_j$ for $j \le c$, and $w[j] = v_{c+1} \oplus \cdots \oplus v_j$ for $j > c$. Line L6 sets $w[j] \leftarrow w[c] \oplus w[j] = (v_1 \oplus \cdots \oplus v_c) \oplus (v_{c+1} \oplus \cdots \oplus v_j)$, which is $v_1 \oplus \cdots \oplus v_j$ by associativity.

**Case $k \ge 1$.** Line L8 sets $w[2i] = v_{2i-1} \oplus v_{2i}$ for $1 \le i \le \lfloor n/2 \rfloor$. The call on line L9 gets the wires $w[2], w[4], \ldots, w[2 \lfloor n/2 \rfloor]$, followed by $w[n]$ if $n$ is odd. These are $\lceil n/2 \rceil < n$ wires, holding $u_i = v_{2i-1} \oplus v_{2i}$ and, for odd $n$, $v_n$ last. By the induction hypothesis, after the call:

- $w[2i] = u_1 \oplus \cdots \oplus u_i = v_1 \oplus \cdots \oplus v_{2i}$;
- for odd $n$, $w[n] = u_1 \oplus \cdots \oplus u_{\lfloor n/2 \rfloor} \oplus v_n = v_1 \oplus \cdots \oplus v_n$.

The wires $w[j]$ with $j$ odd and $j < n$ were not touched, so they still hold $v_j$. Line L10 sets each such $w[j]$ with $j \ge 3$ to $w[j - 1] \oplus w[j] = (v_1 \oplus \cdots \oplus v_{j-1}) \oplus v_j$. The wire $w[1]$ holds $v_1$. So every wire holds its prefix. $\square$

## 2. The depth

We prove both bounds together by strong induction on $n$. For $n = 1$ the depth is 0. Let $n \ge 2$ and $L = \lceil \lg n \rceil \ge 1$.

**Case $k = 0$.** The call on line L4 is $P_1(c)$ with $c = \lceil n/2 \rceil$ and $\lceil \lg c \rceil = L - 1$. By the hypothesis, its outputs have depth at most $1 + (L - 1) = L$, and its last output $w[c]$ has depth at most $L - 1$. The call on line L5 is $P_0(\lfloor n/2 \rfloor)$, whose outputs have depth at most $\lceil \lg \lfloor n/2 \rfloor \rceil \le L - 1$. Each gate of line L6 combines $w[c]$ with one of these outputs, so it has depth at most $(L - 1) + 1 = L$. So every output has depth at most $L = k + L$. The last output $w[n]$ also has depth at most $L$.

**Case $k \ge 1$.** After line L8, every wire has depth at most 1. The call on line L9 is $P_{k-1}(\lceil n/2 \rceil)$, and $\lceil \lg \lceil n/2 \rceil \rceil = L - 1$. By the hypothesis, its outputs have depth at most $1 + (k - 1) + (L - 1) = k + L - 1$, and its last output, which is $w[n]$ in both the even and the odd case, has depth at most $1 + (L - 1) = L$. Each gate of line L10 combines one of these outputs with an input wire of depth 0, so it has depth at most $k + L$. So every output has depth at most $k + L$, and $w[n]$ has depth at most $L$. $\square$

## 3. Size and optimality

Let $s_k(n)$ be the number of gates. Line L6 adds $\lfloor n/2 \rfloor$ gates, line L8 adds $\lfloor n/2 \rfloor$, and line L10 adds one gate for each odd $j$ with $3 \le j < n$, which is $\lfloor n/2 \rfloor - 1$. So $s_k(1) = 0$ and, for $n \ge 2$,
$$
s_0(n) = s_1(\lceil n/2 \rceil) + s_0(\lfloor n/2 \rfloor) + \lfloor n/2 \rfloor, \qquad s_k(n) = s_{k-1}(\lceil n/2 \rceil) + 2 \lfloor n/2 \rfloor - 1 \quad (k \ge 1).
$$
Ladner and Fischer solve these recurrences and get $s_k(n) \le 2(1 + 2^{-k}) n$, so $s_0(n) \le 4n$. The tests check this bound for every $n < 300$ and every $k \le \lceil \lg n \rceil$, and they check the value $s_0(9) = 13$ given in the paper.

No prefix circuit with fan-in 2 has depth less than $\lceil \lg n \rceil$, because the last output depends on all $n$ inputs and a gate at depth $d$ depends on at most $2^d$ inputs. So $P_0(n)$ has optimal depth and linear size. $\blacksquare$
