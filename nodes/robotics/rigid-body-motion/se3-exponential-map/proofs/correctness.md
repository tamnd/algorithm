---
title: EXP-SCREW and EXP-COORDS compute the exponential of a twist
proves: [correctness]
status: full
---

We use the notation of the page.
For $S = (\omega, v)$ with $\omega, v \in \mathbb{R}^3$, the $4 \times 4$ matrix of $S$ is

$$[S] = \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix},$$

where $[\omega]$ is the skew-symmetric matrix of $\omega$.
The exponential of a square matrix $A$ is the series $e^A = \sum_{k \ge 0} A^k / k!$, which converges absolutely for every $A$ (see the page on the matrix exponential).
The proof is in exact arithmetic, in the real RAM.

## Powers of a twist matrix

**Lemma 1.** For every $k \ge 1$,

$$[S]^k = \begin{pmatrix} [\omega]^k & [\omega]^{k-1} v \\ 0 & 0 \end{pmatrix}.$$

*Proof.*
For $k = 1$ this is the definition, with $[\omega]^0 = I$.
If it holds for $k$, then

$$[S]^{k+1} = [S]^k [S] = \begin{pmatrix} [\omega]^k & [\omega]^{k-1} v \\ 0 & 0 \end{pmatrix} \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix} = \begin{pmatrix} [\omega]^{k+1} & [\omega]^k v \\ 0 & 0 \end{pmatrix}.$$

$\square$

**Lemma 2.** If $|\omega| = 1$, then $[\omega]^3 = -[\omega]$.
So for $j \ge 1$, $[\omega]^{2j+1} = (-1)^j [\omega]$ and $[\omega]^{2j+2} = (-1)^j [\omega]^2$.

*Proof.*
For every $x$, $[\omega]^2 x = \omega \times (\omega \times x) = \omega(\omega \cdot x) - x$, because $|\omega| = 1$.
So $[\omega]^2 = \omega\omega^{\mathsf T} - I$, and $[\omega]^3 = [\omega]\omega\omega^{\mathsf T} - [\omega] = -[\omega]$, because $[\omega]\omega = \omega \times \omega = 0$.
The other two formulas follow by induction on $j$. $\square$

## The closed form

**Theorem 1.** Let $S = (\omega, v)$ and $\theta \in \mathbb{R}$.

(a) If $|\omega| = 1$, then

$$e^{[S]\theta} = \begin{pmatrix} R & G(\theta) v \\ 0 & 1 \end{pmatrix}, \quad R = I + \sin\theta\,[\omega] + (1 - \cos\theta)[\omega]^2, \quad G(\theta) = I\theta + (1 - \cos\theta)[\omega] + (\theta - \sin\theta)[\omega]^2.$$

(b) If $\omega = 0$, then

$$e^{[S]\theta} = \begin{pmatrix} I & v\theta \\ 0 & 1 \end{pmatrix}.$$

*Proof.*
By Lemma 1,

$$e^{[S]\theta} = I_4 + \sum_{k \ge 1} \frac{\theta^k}{k!} \begin{pmatrix} [\omega]^k & [\omega]^{k-1} v \\ 0 & 0 \end{pmatrix} = \begin{pmatrix} e^{[\omega]\theta} & \left(\sum_{k \ge 1} \frac{\theta^k}{k!}[\omega]^{k-1}\right) v \\ 0 & 1 \end{pmatrix}.$$

Both series converge absolutely, so we may split and regroup them.

Case (b).
If $\omega = 0$, then $[\omega]^0 = I$ and $[\omega]^k = 0$ for $k \ge 1$.
The upper left block is $I$, and only the term $k = 1$ of the second series is left, which gives $\theta v$.

Case (a).
The upper left block $e^{[\omega]\theta}$ is $R$ by Rodrigues' formula; we repeat the short proof.
Split the series of $e^{[\omega]\theta}$ into the term $k = 0$, the odd terms and the even terms with $k \ge 2$, and use Lemma 2:

$$e^{[\omega]\theta} = I + \Big(\sum_{j \ge 0} \frac{(-1)^j \theta^{2j+1}}{(2j+1)!}\Big)[\omega] + \Big(\sum_{j \ge 0} \frac{(-1)^j \theta^{2j+2}}{(2j+2)!}\Big)[\omega]^2 = I + \sin\theta\,[\omega] + (1 - \cos\theta)[\omega]^2.$$

For the second series, write $G(\theta) = \sum_{k \ge 1} \frac{\theta^k}{k!}[\omega]^{k-1}$.
The term $k = 1$ is $I\theta$.
The terms with $k - 1 = 2j + 1$ odd give $\sum_{j \ge 0} \frac{(-1)^j \theta^{2j+2}}{(2j+2)!}[\omega] = (1 - \cos\theta)[\omega]$.
The terms with $k - 1 = 2j + 2$ even and at least 2 give $\sum_{j \ge 0} \frac{(-1)^j \theta^{2j+3}}{(2j+3)!}[\omega]^2 = (\theta - \sin\theta)[\omega]^2$.
So $G(\theta) = I\theta + (1 - \cos\theta)[\omega] + (\theta - \sin\theta)[\omega]^2$. $\square$

## EXP-SCREW

**Corollary 2.** If $S$ is a screw axis, that is $|\omega| = 1$, or $\omega = 0$ and $|v| = 1$, then EXP-SCREW$(S, \theta)$ returns $e^{[S]\theta}$.

*Proof.*
Line L1 splits $S$.
If $\omega = 0$, line L3 returns the matrix of Theorem 1(b).
Else $|\omega| = 1$, lines L4 to L7 compute $R$, $G(\theta)$ and $p = G(\theta) v$ of Theorem 1(a), and line L8 returns the matrix of Theorem 1(a).
The implementation checks the hypothesis on $S$ with a tolerance of $10^{-9}$ and raises an error if it fails. $\square$

The result is in SE(3).
$R$ is a rotation, because $R = e^{[\omega]\theta}$, $\det e^{A} = e^{\operatorname{tr} A} = 1$ for the trace-free $A = [\omega]\theta$, and $(e^{[\omega]\theta})^{\mathsf T} = e^{-[\omega]\theta} = (e^{[\omega]\theta})^{-1}$.

## EXP-COORDS

**Theorem 3.** For every $\xi = (w, u) \in \mathbb{R}^6$, let $\theta = |w|$.
If $\theta \ge \delta$ or $\theta = 0$, EXP-COORDS$(\xi)$ returns $e^{[\xi]}$.
If $0 < \theta < \delta$, it returns $e^{[\xi]}$ with each of the three scalar factors changed by a relative amount below $3 \cdot 10^{-16}$.

*Proof.*
If $\theta \ge \delta > 0$, let $S = \xi / \theta$.
Then $S = (w/\theta, u/\theta)$ has a unit angular part, so it is a screw axis, and $[\xi] = [S]\theta$.
Line E4 returns $e^{[S]\theta} = e^{[\xi]}$ by Corollary 2.

If $\theta < \delta$, put $K = [w] = \theta[\hat\omega]$ when $\theta > 0$.
Theorem 1(a) with $\hat\omega = w/\theta$ and $v = u/\theta$ gives

$$e^{[\xi]} = \begin{pmatrix} I + a K + b K^2 & (I + b K + c K^2)\, u \\ 0 & 1 \end{pmatrix}, \quad a = \frac{\sin\theta}{\theta},\ b = \frac{1 - \cos\theta}{\theta^2},\ c = \frac{\theta - \sin\theta}{\theta^3}.$$

Indeed, $\sin\theta\,[\hat\omega] = a K$, $(1 - \cos\theta)[\hat\omega]^2 = b K^2$, and $G(\theta) v = (I\theta + (1 - \cos\theta)[\hat\omega] + (\theta - \sin\theta)[\hat\omega]^2)\, u/\theta = (I + b K + c K^2)\, u$.
The same formula also holds for $\theta = 0$, where $K = 0$ and the result is the translation by $u$, as in Theorem 1(b).
Line E5 replaces $a$, $b$ and $c$ by their Taylor polynomials of degree 4 in $\theta$.
The three series alternate, and their terms decrease in size for $\theta < 1$, so the error of each truncation is below the first omitted term: $\theta^6/5040$, $\theta^6/40320$ and $\theta^6/362880$.
For $\theta < \delta = 10^{-2}$ these are below $2 \cdot 10^{-16}$, and relative to $a \approx 1$, $b \approx 1/2$ and $c \approx 1/6$ they are below $3 \cdot 10^{-16}$.
Lines E6 and E7 then compute the matrix above. $\square$

## The inverse map

**Theorem 4.** Let $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix}$ with $R \in SO(3)$, and let $w$ be a vector with $e^{[w]} = R$ and $\theta = |w| < 2\pi$, for example the output of the SO(3) logarithm, which has $\theta \le \pi$.
Then the unique $u$ with $e^{[(w, u)]} = T$ is $u = (I - \tfrac12 [w] + d\,[w]^2)\, p$, where $d = (1 - \tfrac{\theta}{2}\cot\tfrac{\theta}{2}) / \theta^2$ for $\theta > 0$, and $d = 1/12$ for $\theta = 0$.

*Proof.*
By the proof of Theorem 3, the translation part of $e^{[(w, u)]}$ is $M u$ with $M = I + b K + c K^2$ and $K = [w]$.
We show that $N = I - \tfrac12 K + d K^2$ is the inverse of $M$.
If $\theta = 0$, then $K = 0$ and $M = N = I$.
Else write $K = \theta[\hat\omega]$ with the unit vector $\hat\omega = w/\theta$.
Both $M$ and $N$ are polynomials in $K$.
$K$ maps the line of $\hat\omega$ to 0 and maps the plane orthogonal to $\hat\omega$ to itself, so we can check $M N = I$ on the line and on the plane separately.
On the line of $\hat\omega$, $K\hat\omega = 0$, so $M\hat\omega = N\hat\omega = \hat\omega$.
On the orthogonal plane, $K$ acts as $\theta J$, where $J x = \hat\omega \times x$ is the rotation by $\pi/2$ about $\hat\omega$, with $J^2 = -I$.
Identify this plane with the complex numbers, so that $J$ is multiplication by $i$.
Then $M$ acts as the number $m = 1 + b\,\theta i - c\,\theta^2 = \frac{\sin\theta}{\theta} + i\,\frac{1 - \cos\theta}{\theta} = \frac{e^{i\theta} - 1}{i\theta}$.
And $N$ acts as $n = 1 - \tfrac{\theta}{2} i - d\,\theta^2 = h\cot h - i h$, with $h = \theta/2$.
Now $e^{i\theta} - 1 = e^{ih}(e^{ih} - e^{-ih}) = 2i\sin h\, e^{ih}$, so $m = \frac{\sin h}{h} e^{ih}$.
And $n = \frac{h}{\sin h}(\cos h - i\sin h) = \frac{h}{\sin h} e^{-ih}$.
So $m n = 1$, and $M N = I$ on the plane.
Hence $N = M^{-1}$, for $0 < \theta < 2\pi$, where $\sin h \ne 0$.

So $M u = p$ has the unique solution $u = N p$.
The rotation part of $e^{[(w, u)]}$ is $e^{[w]} = R$, so $e^{[(w, u)]} = T$. $\square$

At $\theta = \pi$ the rotation logarithm has two values $\pm\pi\hat\omega$, and each of them gives one $u$ by Theorem 4.
For $\theta$ near 0, the implementation uses the series $d = 1/12 + \theta^2/720 + \theta^4/30240$, the start of the Taylor series of $(1 - h\cot h)/\theta^2$.
