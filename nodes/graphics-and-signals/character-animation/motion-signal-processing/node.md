---
tag: 70Z43X
kind: technique
slug: motion-signal-processing
name: Motion signal processing
aliases:
- motion multiresolution filtering
area: graphics-and-signals/character-animation
level: advanced
summary: "Treat joint angle curves as signals and edit motion by multiresolution filtering, waveshaping and timewarping of frequency bands."
prereqs: [laplacian-pyramid, motion-warping, convolution]
see_also: [gaussian-pyramid, linear-filtering, dynamic-time-warping, motion-blending, registration-curves, b-spline, gaussian-filter]
sources:
  - paper: doi:10.1145/218380.218421
    title: "Armin Bruderlin and Lance Williams, Motion signal processing, SIGGRAPH 95, 1995, 97 to 104"
    locator: "Section 2.1 (multiresolution filtering with the kernel 1/16, 1/4, 3/8, 1/4, 1/16), and the sections on multitarget interpolation, timewarping, waveshaping and motion displacement mapping"
  - paper: doi:10.1109/TCOM.1983.1095851
    title: "Peter J. Burt and Edward H. Adelson, The Laplacian pyramid as a compact image code, IEEE Transactions on Communications 31(4), 1983, 532 to 540"
    locator: the generating kernel and the bands as differences of successive lowpass images
  - paper: doi:10.1145/218380.218422
    title: "Andrew Witkin and Zoran Popović, Motion warping, SIGGRAPH 95, 1995, 105 to 108"
    locator: the displacement curve through keys, which is the same idea as motion displacement mapping
---

Motion signal processing treats each joint angle curve of a motion as a sampled signal and edits it with the tools of signal processing.
The main tool is a band decomposition: repeated lowpass filtering splits each channel into a slow base and a few bands of higher frequency, like a [Laplacian pyramid](/laplacian-pyramid/) in one dimension.
The animator then sets a gain for each band and adds the bands back: more gain on the middle bands makes a walk more lively, less gain on the high bands makes it calmer, and the sum with all gains 1 gives the original motion back exactly.
The same paper also uses waveshaping (a function applied to the channel values), timewarping (to align two motions before a blend), multitarget blends by band, and motion displacement mapping, the idea of [motion warping](/motion-warping/).
Bruderlin and Williams presented the method at SIGGRAPH 95.

## In plain words

A joint angle that changes over time is like a sound.
It has slow parts, such as the large swing of a leg, and fast parts, such as small shakes.
The method splits the curve into layers, from slow to fast, by smoothing it again and again and keeping what each smoothing removed.
You make each layer louder or softer.
Then you add the layers back together.
If you change nothing, you get the same motion.
If you make the middle layers louder, the motion looks more energetic; if you make the fast layers softer, it looks more relaxed.

## When it applies

The technique applies to motion stored as channels sampled at a fixed rate: joint angles, root positions, or the parameters of a face.
Band gains suit stylistic edits that change all frames a little, such as more or less energy.
They do not keep constraints: a gain on the hip and knee bands moves the feet, so contacts need a cleanup afterward.
The decomposition is a linear operation, and the claims about it below are properties of the filter.
That a gain makes a motion look "more lively" or "calmer" is a visual judgment, and the gains are a control of the user.

Angles must be continuous in time: unwrap jumps of $2\pi$ before filtering.
Channels of [Euler angles](/euler-angles/) filter well only away from gimbal lock; three angles of one joint filtered alone can give a rotation that is in neither neighbor frame.

## The template

1. **Choose the levels.** For a channel of $f$ samples, take $L$ levels, few enough that the widest kernel of step 2 still fits in the signal.
2. **Lowpass again and again.** Set $G_0$ to the channel. For $l = 0, \dots, L - 1$, convolve $G_l$ with the kernel $w = (1/16, 1/4, 3/8, 1/4, 1/16)$ widened for level $l$, to get $G_{l+1}$. The kernel at level $l$ spans $2^l$ times the time of the base kernel, made by placing zeros between its taps. The signal is not downsampled, so every $G_l$ has $f$ samples. At the ends, extend the signal, for example by repeating the end value or by reflection.
3. **Form the bands.** $L_l = G_l - G_{l+1}$ for $l = 0, \dots, L - 1$. The last lowpass $G_L$ is the base (the paper calls it the DC band).
4. **Set the gains.** Choose a gain $k_l$ for each band, and possibly a separate gain for each channel.
5. **Reconstruct.** The new channel is $G_L + \sum_{l=0}^{L-1} k_l L_l$. With every $k_l = 1$ the sum telescopes to $G_0$, the original channel, exactly.
6. **Fix constraints.** Restore the foot contacts and other constraints with [inverse kinematics](/inverse-kinematics/) or [footskate cleanup](/footskate-cleanup/).

The kernel is the binomial filter of [B-spline](/b-spline/) smoothing that Burt and Adelson used for the Laplacian pyramid: its taps are positive and sum to 1, so it keeps constants and is a lowpass filter.
Each level costs $5 f$ multiply and add steps, so the decomposition costs $O(f L)$ per channel, and the reconstruction the same.

## Classic examples

**A band gain by hand.**
Take the impulse $G_0 = (0, 0, 0, 0, 1, 0, 0, 0, 0)$ and one level.
The lowpass is $G_1 = (0, 0, 1/16, 1/4, 3/8, 1/4, 1/16, 0, 0)$, and the band is $L_0 = G_0 - G_1 = (0, 0, -1/16, -1/4, 5/8, -1/4, -1/16, 0, 0)$.
With $k_0 = 2$, the result is $G_1 + 2 L_0 = (0, 0, -0.0625, -0.25, 1.625, -0.25, -0.0625, 0, 0)$: the peak is higher and has negative side lobes, so the high frequencies are stronger.
With $k_0 = 0$, the result is $G_1$, a smoother peak.
With $k_0 = 1$, the result is $G_0$ again.
At the next level the kernel with zeros is $(1/16, 0, 1/4, 0, 3/8, 0, 1/4, 0, 1/16)$, which spans 9 samples instead of 5.

**Walking style.**
The paper applies band gains to all joints of a walk and shows how the style changes; for example, higher gains on the middle bands give a more exaggerated walk.

**Waveshaping.**
A shaping function $s$ maps each value of a channel to a new value, $\theta'(t) = s(\theta(t))$.
A function that flattens near a joint limit keeps the joint from overextending; a function with small waves adds an undulation to the motion.

**Timewarping and blends.**
To blend two motions, the paper first aligns them in time with [dynamic time warping](/dynamic-time-warping/) of their signals, then blends band by band, so that the base of one motion can mix with the detail of another.
The same need for alignment is the reason for [registration curves](/registration-curves/).

**Displacement.**
Motion displacement mapping adds a smooth curve through a few keys to a channel; it is the same idea as [motion warping](/motion-warping/) from the same conference.

## Variations

- **Downsampled pyramid.** Downsample each lowpass by 2, as in the image [Laplacian pyramid](/laplacian-pyramid/). It stores less, but the bands no longer have one value per frame, and an edit needs an upsampling step.
- **Fourier methods.** Unuma, Anjyo and Takeuchi (1995) used Fourier series of cyclic motions to interpolate and exaggerate emotions.
- **Wavelets.** Wavelet transforms give bands that are orthogonal, at the cost of a less smooth reconstruction when the gains change.
- **Per joint gains.** Set the gains for each channel, for example to calm the arms and keep the legs.
- **Displacement on top.** Combine the bands with a [motion warping](/motion-warping/) offset to meet keys after the style change.

## Pitfalls

- **Contacts.** Band gains move the feet and hands. Planted feet slide unless a cleanup follows.
- **Ends of the signal.** The kernel reads past the ends of the clip. The choice of extension changes the first and last frames; cyclic motions should wrap around.
- **Angle jumps.** A jump from $\pi$ to $-\pi$ in a channel is a large step to the filter. Unwrap the angles first.
- **Large gains.** A high gain on a low band changes the pose a lot and can put limbs through the body or the floor.
- **Rotations as angles.** Filtering Euler angles channel by channel is not the same as filtering rotations; near gimbal lock the result can twist.
- **The name.** The alias "motion multiresolution filtering" names only the band part of the paper, not the waveshaping or the timewarping.

## Exercises

1. Show that $G_L + \sum_{l=0}^{L-1} L_l = G_0$ for any number of levels and any lowpass filter. *Answer:* the sum telescopes, $G_L + (G_0 - G_1) + (G_1 - G_2) + \dots + (G_{L-1} - G_L) = G_0$.
2. Show that a constant channel has zero bands at every level, so no gain changes it. *Answer:* the taps sum to $1/16 + 1/4 + 3/8 + 1/4 + 1/16 = 1$, so the lowpass of a constant is the same constant, also with zeros between the taps, and every difference $G_l - G_{l+1}$ is 0.
3. How many samples does the widened kernel span at level $l$, and what is the largest $L$ for a walk of 120 frames if the kernel of the last level $L - 1$ must fit? *Answer:* $4 \cdot 2^l + 1$ samples; $4 \cdot 2^{L-1} + 1 \le 120$ gives $2^{L-1} \le 29$, so $L = 5$.
4. Compute the result of the impulse example with $k_0 = 0.5$. *Answer:* $G_1 + 0.5 L_0 = (G_0 + G_1)/2 = (0, 0, 1/32, 1/8, 11/16, 1/8, 1/32, 0, 0)$.

## References
