---
title: Wu's line algorithm gives the tent weights of the line, exactly or within a stated error
proves: [correctness, termination]
status: full
---

Let $(x_0, y_0)$ and $(x_1, y_1)$ be integer points with $x_0 < x_1$ and $0 \le y_1 - y_0 \le x_1 - x_0$. Write $d_x = x_1 - x_0$, $d_y = y_1 - y_0$ and, for an inner column $x = x_0 + i$ with $1 \le i \le d_x - 1$, $Y_i = y_0 + i\,d_y/d_x$ for the exact height of the segment. The *tent weight* of a pixel $(x, j)$ for a height $Y$ is

$$T_j(Y) = \max\big(0,\ 1 - |j - Y|\big).$$

For each real $Y$, only $j = \lfloor Y \rfloor$ and $j = \lfloor Y \rfloor + 1$ can have a positive weight, and these two weights are $1 - f$ and $f$, where $f = Y - \lfloor Y \rfloor$. Indeed $|\lfloor Y \rfloor - Y| = f$ and $|\lfloor Y \rfloor + 1 - Y| = 1 - f$, and each other integer is at distance at least 1 from $Y$.

**Termination.** The loop of line L5 runs $d_x - 1$ times (zero times if $d_x = 1$), and each pass is a fixed number of steps.

## The exact accumulator

In the exact form, the accumulator $D$ starts at 0, each pass adds $d_y$, and if $D \ge d_x$ it subtracts $d_x$ and adds 1 to $y$. Pass $i$ plots $(x, y)$ with weight $1 - D/d_x$ and $(x, y + 1)$ with weight $D/d_x$.

**Claim 1.** After the update of pass $i$, $\; y\,d_x + D = y_0\,d_x + i\,d_y \;$ and $\; 0 \le D < d_x$. So $y = \lfloor Y_i \rfloor$, $D/d_x = Y_i - \lfloor Y_i \rfloor$, and the two weights of pass $i$ are $T_y(Y_i)$ and $T_{y+1}(Y_i)$: the algorithm gives the tent weights exactly.

*Proof.* By induction on $i$. Before pass 1, $y = y_0$ and $D = 0$, so the equation holds for $i = 0$ and $0 \le D < d_x$. Assume it holds for $i - 1$. The pass adds $d_y$ to $D$, so the equation holds for $i$ with the new $D$, and $0 \le D < d_x + d_y \le 2 d_x$ because $d_y \le d_x$. If $D \ge d_x$, the pass subtracts $d_x$ from $D$ and adds 1 to $y$. This keeps $y\,d_x + D$ and gives $0 \le D < d_x$. If $D < d_x$, nothing changes. So after the update, $0 \le D < d_x$. Divide the equation by $d_x$: $y + D/d_x = Y_i$ with $0 \le D/d_x < 1$, so $y = \lfloor Y_i \rfloor$ and $D/d_x$ is the fractional part $f$ of $Y_i$. By the remark on tent weights, the weights $1 - f$ and $f$ of the two plotted pixels are $T_y(Y_i)$ and $T_{y+1}(Y_i)$, and all other pixels of the column have tent weight 0. $\blacksquare$

## The $w$-bit accumulator

This is the program of the page. Line L2 sets $d = \lfloor d_y 2^w / d_x + \tfrac12 \rfloor$. Since $0 \le d_y/d_x \le 1$, we have $0 \le d \le 2^w$, and

$$\left|\frac{d}{2^w} - \frac{d_y}{d_x}\right| \le 2^{-(w+1)}.$$

Write $\hat Y_i = y_0 + i\,d/2^w$.

**Claim 2.** After the update of pass $i$ (lines L6 and L7), $\; y\,2^w + D = y_0\,2^w + i\,d \;$ and $\; 0 \le D < 2^w$. So $y = \lfloor \hat Y_i \rfloor$, and lines L8 and L9 plot the tent weights $T_y(\hat Y_i)$ and $T_{y+1}(\hat Y_i)$. The two weights of each column add up to 1.

*Proof.* The proof of Claim 1 with $d_x$ replaced by $2^w$ and $d_y$ by $d$. It needs $d \le 2^w$, so that one subtraction in line L7 brings $D$ back below $2^w$. The two weights are $1 - D/2^w$ and $D/2^w$, so they add up to 1. $\blacksquare$

**Claim 3 (error bound).** For each pixel $(x_0 + i, j)$ of an inner column, the weight that the program gives (0 if it does not plot the pixel) differs from the exact tent weight $T_j(Y_i)$ by at most

$$|\hat Y_i - Y_i| \le \frac{i}{2^{w+1}} < \frac{d_x}{2^{w+1}}.$$

The endpoints get weight 1, which is their exact tent weight.

*Proof.* The function $t \mapsto \max(0, 1 - |j - t|)$ is 1-Lipschitz: $|\,|j - a| - |j - b|\,| \le |a - b|$ by the triangle inequality, and $v \mapsto \max(0, v)$ does not increase distances. So $|T_j(\hat Y_i) - T_j(Y_i)| \le |\hat Y_i - Y_i|$ for each $j$. By Claim 2, the program gives $T_j(\hat Y_i)$ to each pixel of the column (the pixels it does not plot have $T_j(\hat Y_i) = 0$). Finally $|\hat Y_i - Y_i| = i\,|d/2^w - d_y/d_x| \le i\,2^{-(w+1)}$. $\blacksquare$

**Consequence.** If $d_x \le 2^{w-q}$, the error of each weight is below $2^{-(q+1)}$, half of the step $2^{-q}$ of a $q$-bit intensity. For example, $w = 20$ and $q = 8$ allow lines up to 4096 pixels long.
