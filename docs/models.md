# Physical model

PEACOCK follows ultraviolet photons from a galaxy through a clumpy outflow. Gas in front of the galaxy absorbs light at particular wavelengths. Some of that light reaches the observer after scattering in the wind, either in the same transition or in a fluorescent line.

```{figure} assets/research/figure-01-clumpy-outflow.png
:alt: Central galaxy and clumpy circumgalactic outflow, with a yellow path illustrating scattered Lyα and metal-line photons escaping toward an observer.
:width: 100%
:target: _static/research/figure-01-clumpy-outflow.pdf

A central source illuminates a clumpy outflow. Clumps have internal Doppler broadening, random motions and a radial bulk velocity. PEACOCK represents the clumps as spheres.
```

(wind)=

## Clump distribution and kinematics

In the baseline wind of {ref}`Li+2026a <li-2026a>`, light from a compact central source travels freely between clumps. The clumps are equal-size spheres, packed more densely near the galaxy and more sparsely farther out. Each clump presents the same radial column of a given ion, wherever it sits in the wind.

In this model, the clump number density falls as $r^{-2}$ between the inner and outer halo radii, and the outer radius is ten times the inner one. The gas between clumps contributes neither line opacity nor dust extinction.

To apply a velocity law to a fixed cloud catalogue, follow the
[C II configuration example](configuring-a-peacock-simulation.md#switch-from-a-constant-outflow-to-a-t15-wind).

### FCC clump placement

To place the clumps without overlap, PEACOCK chooses their centers from sites on a face-centered cubic (FCC) lattice. The volume filling factor sets how much of the shell is occupied and therefore how many equal-size clumps it holds. The desired density profile sets how many of those clumps go into each radial shell.

### Bulk outflow

In the baseline accelerating wind, clumps start with zero radial bulk speed at the inner halo edge. An outward force accelerates them, while halo gravity pulls them back. Depending on the strength of the outward force at launch, the bulk speed can peak inside the halo and then decline. The speed scale $v_0$ and the launch force ratio $R$ describe this velocity law below.

### Random motion and internal broadening

Two kinds of motion broaden a line. Whole clumps move at different velocities, so a photon encounters a different Doppler shift from one clump to the next. Within each clump, thermal and unresolved gas motions broaden its absorption profile. The clump velocity dispersion $\sigma_{\mathrm{cl}}$ describes the first effect, and the Doppler parameter $b_{\mathrm{D,cl}}$ describes the second.

The equations below give the clump velocity and the radial outflow law used in {ref}`Li+2026a <li-2026a>` (§2.1).

### Random and total clump velocity

Clumps at the same radius share a radial bulk speed. Each also receives a random velocity, drawn once and held fixed as photons travel through the wind.

(eq-1)=

```{math}
:nowrap:

\[
\delta v_i \sim \mathcal{N}(0,\sigma_{\rm cl}^{2}),
\qquad i=x,y,z
\tag{1}
\]
```

Each component is an independent Gaussian draw centered on zero. $\sigma_{\mathrm{cl}}$ is the standard deviation along one axis. Using the same value along all three axes gives no preferred direction.

(eq-2)=

```{math}
:nowrap:

\[
\boldsymbol{v}_{\rm cl}(r)
=
v_{\rm cl,\,out}(r)\,\hat{\boldsymbol r}
+
\delta\boldsymbol{v}_{\rm cl}
\tag{2}
\]
```

At radius $r$, add the outward bulk velocity along the radial unit vector $\hat{\boldsymbol r}$ to the clump’s random velocity. This gives the motion of the entire clump.

### Radial acceleration and outflow speed

The wind law starts with a clump at rest at the inner edge of the halo, $R_{\mathrm{in}}$. An outward acceleration $A/r^2$ pushes the clump away from the galaxy, while halo gravity pulls it back. {ref}`Li+2026a <li-2026a>` assumes an isothermal halo with constant circular speed $v_{\mathrm c}$, so the enclosed mass $M(r)=v_{\mathrm c}^2r/G$ makes the inward acceleration $v_{\mathrm c}^2/r$.

To get speed as a function of radius, write the time derivative as $\mathrm{d}v/\mathrm{d}t=v\,\mathrm{d}v/\mathrm{d}r$, where $v$ is the radial bulk speed. Integrating from the launch radius gives the speed law below.

(eq-3)=

```{math}
:nowrap:

\[
\frac{{\rm d}v_{\rm cl,\,out}}{{\rm d}t}
=
-\frac{GM(r)}{r^{2}}+\frac{A}{r^{2}}
=
-\frac{v_{\rm c}^{2}}{r}+\frac{A}{r^{2}}
\tag{3}
\]
```

Integrating the outward term from $R_{\mathrm{in}}$ to $r$ gives $A(1/R_{\mathrm{in}}-1/r)$. Gravity subtracts $v_{\mathrm c}^2\ln(r/R_{\mathrm{in}})$. Their difference equals $v^2/2$, because the wind starts from rest.

(eq-4)=

```{math}
:nowrap:

\[
v_{\rm cl,\,out}(r)
=
v_0\sqrt{
\max\left\{
0,\,
R\left(1-\frac{R_{\rm in}}{r}\right)
-\ln\left(\frac{r}{R_{\rm in}}\right)
\right\}
}
\tag{4}
\]
```

The scale $v_0=\sqrt{2}\,v_{\mathrm c}$ sets the overall speed, and $R=A/(v_{\mathrm c}^{2}R_{\mathrm{in}})$ is the ratio of outward acceleration to gravity at launch. If the expression inside the braces is negative, the bulk speed is zero and the random motion remains.

The wind reaches its highest speed where the driving force and gravity balance, provided the halo extends that far. In equation (5), $q=R_{\mathrm{out}}/R_{\mathrm{in}}$ is the ratio of the halo radii.

(eq-5)=

```{math}
:nowrap:

\[
v_{\rm cl,\,out,\,max}
=
\begin{cases}
v_0\sqrt{R-1-\ln R},
& 1<R\leq q\\
v_0\sqrt{R(1-q^{-1})-\ln q},
& R>q
\end{cases}
\tag{5}
\]
```

If $1<R<q$, the speed peaks inside the halo at $r=R R_{\mathrm{in}}$. If $R\geq q$, its maximum is at the outer edge.

(transport)=

## Radiative transfer in the clumpy wind

In each interaction, PEACOCK calculates the opacity seen by the photon, draws the absorbing transition and the atom’s velocity, then follows the radiative decay. A re-emitted photon can scatter again before escaping.

The equations below follow the three steps of line transfer in {ref}`Li+2026a <li-2026a>` (§2.2.4).

### Line opacity

To decide how far a photon can travel before interacting, PEACOCK evaluates the line opacity in the local gas frame. Gas motion changes the frequency seen by the ions, so it can move a photon closer to or farther from resonance. When line profiles overlap, the photon sees their combined opacity.

(eq-12)=

```{math}
:nowrap:

\[
\begin{split}
\alpha_\nu^{\rm line}
&=\sum_j n_{\ell_j}\sigma_j(\nu)\\
\sigma_j(\nu)
&=\frac{\sqrt{\pi}e^2}{m_{\rm e}c}
\frac{f_j}{\Delta\nu_{{\rm D},j}}H(a_j,x_j)
\end{split}
\tag{12}
\]
```

In the local gas frame, sum the contributions from all included transitions. Each contribution is the lower-level population density $n_{\ell_j}$ times the absorption cross section $\sigma_j$. The oscillator strength $f_j$ and Doppler width $\Delta\nu_{\mathrm{D},j}$ set the strength and width of the profile.

(eq-13)=

```{math}
:nowrap:

\[
H(a,x)
=
\frac{a}{\pi}
\int_{-\infty}^{\infty}
\frac{e^{-y^2}}{(x-y)^2+a^2}\,{\rm d}y
\tag{13}
\]
```

The Voigt–Hjerting profile combines Gaussian Doppler broadening with Lorentzian damping wings. $x$ is the frequency offset in Doppler units and $a$ is the damping parameter. The area under $H$ in $x$ is $\sqrt{\pi}$.

(eq-14)=

```{math}
:nowrap:

\[
\begin{array}{c}
x_j=\frac{\nu-\nu_j}{\Delta\nu_{{\rm D},\,j}},
\qquad
a_j=\frac{\Gamma_{u_j}}{4\pi\Delta\nu_{{\rm D},\,j}}\\
\Gamma_{u_j}=\sum_k A_{u_jk}
\end{array}
\tag{14}
\]
```

Measure the detuning $x_j$ from the rest frequency $\nu_j$ in units of the line’s Doppler width $\Delta\nu_{\mathrm{D},j}=\nu_j b_{\mathrm{D,cl}}/c$. The internal Doppler parameter $b_{\mathrm{D,cl}}=\sqrt{2k_{\mathrm B}T/m_{\mathrm{ion}}+b_{\mathrm{micro}}^2}$ combines thermal motion and unresolved motion within a clump. The upper-level decay rate $\Gamma_{u_j}$ is the sum of its Einstein $A$ coefficients.

(eq-15)=

```{math}
:nowrap:

\[
\begin{array}{c}
x=\frac{\nu-\nu_0}{\Delta\nu_{{\rm D},0}},
\qquad
d_j=\frac{\nu_0-\nu_j}{\Delta\nu_{{\rm D},0}}\\
x_j=x+d_j
\end{array}
\tag{15}
\]
```

For nearby transitions with the same Doppler width, the code can work on a single frequency axis centered on $\nu_0$. Adding $d_j$ gives the photon’s distance from the center of transition $j$ on that axis.

### Absorbing transition and atomic velocity

Once a photon is absorbed, PEACOCK chooses which transition absorbed it and how the atom was moving. These draws are linked because an atom moving at the right speed along the incoming ray can bring the photon closer to resonance. That same atom's motion also affects the frequency of the re-emitted photon.

(eq-16)=

```{math}
:nowrap:

\[
\begin{array}{c}
p(u_\parallel\mid x_j,j)
=
\frac{a_j}{\pi H(a_j,x_j)}
\frac{e^{-u_\parallel^2}}
{(x_j-u_\parallel)^2+a_j^2}
\\
u_\parallel=\frac{v_\parallel}{b_{\rm D,\,cl}}
\end{array}
\tag{16}
\]
```

For a chosen transition, the atom’s speed along the incoming ray is measured by $u_\parallel$. The Gaussian factor describes how common each velocity is. The Lorentzian factor favors atoms for which the photon is close to resonance.

(eq-17)=

```{math}
:nowrap:

\[
p(u_\parallel\mid\nu)
=\sum_j w_j(\nu)\,p(u_\parallel\mid\nu,j)
\tag{17}
\]
```

For overlapping transitions of one ion, the parallel velocity distribution is a mixture of the distributions for the individual transitions.

(eq-18)=

```{math}
:nowrap:

\[
w_j(\nu)
=\frac{n_{\ell_j}\sigma_j(\nu)}
{\sum_k n_{\ell_k}\sigma_k(\nu)}
\tag{18}
\]
```

The weight $w_j$ is transition $j$’s share of the total opacity at the photon’s frequency. PEACOCK draws a transition using these weights, then draws the parallel velocity for that transition.

(eq-19)=

```{math}
:nowrap:

\[
p(u_\perp)=\pi^{-1/2}e^{-u_\perp^2}
\tag{19}
\]
```

The perpendicular velocity component is Gaussian with standard deviation $1/\sqrt{2}$ in Doppler units. The component in the scattering plane enters the frequency update.

### Radiative decay and re-emission

The upper level reached in absorption determines which emission lines are possible. PEACOCK draws a decay channel using the atomic decay rates, then uses the change in atomic energy to find the outgoing frequency. That frequency determines which lines the photon can interact with next.

(eq-20)=

```{math}
:nowrap:

\[
P(u\rightarrow k)=\frac{A_{uk}}{\sum_m A_{um}}
\tag{20}
\]
```

The excited level $u$ decays to level $k$ with probability proportional to its Einstein $A_{uk}$ coefficient. Returning to the starting level gives resonant re-emission. Decay to a different lower level gives fluorescence.

(eq-21)=

```{math}
:nowrap:

\[
\nu_{\rm out}^{\rm atom}
=\nu_{\rm in}^{\rm atom}
-\frac{E_{\ell_{\rm out}}-E_{\ell_{\rm in}}}{h}
\tag{21}
\]
```

For example, if the ion is left in a higher-energy level than it occupied before absorption, the outgoing photon carries less energy and has a lower frequency. The level spacing divided by Planck’s constant $h$ gives the frequency shift. Neglecting recoil, the photon keeps the same offset from the new branch’s line center in the atom’s frame. The same atom’s velocity is used to transform both frequencies.

(source-dust-aperture)=

## Source, dust and aperture

### Photon source

The central source supplies ultraviolet continuum and, where appropriate, intrinsic line emission. Absorbed continuum photons can themselves produce resonant or fluorescent emission. At fixed gas and dust, line and continuum templates can be combined using their input photon ratio.

### Dust

Dust inside a clump can absorb a photon or scatter it. {ref}`Li+2026a <li-2026a>` specifies the absorption optical depth across one clump radius at the reference wavelength and uses Small Magellanic Cloud dust properties to describe scattering.

### Aperture

A spectrum includes escaped photons whose projected distance from the halo center is at most $b_{\max}$. A smaller aperture can exclude scattered light that escapes at larger projected distances.

(scope)=

## Model assumptions and run settings

To adapt the baseline wind to another galaxy, set its geometry, velocities, photon source and dust in the [simulation configuration](configuring-a-peacock-simulation.md). To compare the resulting spectrum with an observation, match the aperture and account for any offset in systemic velocity or continuum level.

{ref}`Li+2026a <li-2026a>` also discusses optically thin nebular and recombination emission and overlap between different ions. The [line guide](choosing-a-line-and-an-observable.md#which-line-should-i-run) lists the transitions that run together in the released code.

(model-parameters)=

## Basic model parameters

Table 2 of {ref}`Li+2026a <li-2026a>` lists the parameters for the clumpy wind, the photon source and the comparison with observations. The applicability column shows which parameters are shared across lines and which depend on the model or fitting setup.

```{list-table}
:header-rows: 1
:class: model-parameters
:widths: 12 20 13 20 35

* - Symbol
  - Parameter
  - Unit
  - Applies to
  - Meaning
* - $F_{\mathrm{V}}$
  - Clump volume filling factor
  - Dimensionless
  - All clumpy models
  - Fraction of the halo shell volume occupied by clumps.
* - $N_{\mathrm{ion,cl}}$
  - Clump ion column density
  - $\mathrm{cm}^{-2}$
  - All clumpy models
  - Column of the selected ion across one clump radius. For C II and Si II the input refers to the reference lower level.
* - $b_{\mathrm{D,cl}}$
  - Clump Doppler parameter
  - $\mathrm{km}\,\mathrm{s}^{-1}$
  - All clumpy models
  - Line broadening from thermal and unresolved motions inside a clump.
* - $\sigma_{\mathrm{cl}}$
  - Random clump velocity dispersion
  - $\mathrm{km}\,\mathrm{s}^{-1}$
  - All clumpy models
  - Standard deviation of one Cartesian component of the clump’s random velocity.
* - $v_0$
  - Outflow velocity normalization
  - $\mathrm{km}\,\mathrm{s}^{-1}$
  - Radially varying wind
  - Sets the overall scale of the coherent radial wind.
* - $R$
  - Acceleration parameter
  - Dimensionless
  - Radially varying wind
  - Ratio of outward acceleration to gravity at the launch radius.
* - $\tau_{\mathrm{d,cl}}$
  - Clump dust optical depth
  - Dimensionless
  - All clumpy models
  - Absorption optical depth across one clump radius at the reference wavelength.
* - $b_{\max}$
  - Maximum photon impact parameter
  - Length (e.g. kpc)
  - Aperture selection for any line
  - Largest projected distance included in the spectrum. It can also be expressed relative to the outer radius as $b_{\max}/R_{\mathrm{out}}$.
* - $\Delta v$
  - Velocity shift
  - $\mathrm{km}\,\mathrm{s}^{-1}$
  - Fits to observations
  - Offset between the model and the adopted systemic velocity.
* - $f_{\mathrm{scale}}$
  - Continuum scaling factor
  - Dimensionless
  - Fits to observations
  - Adjusts the predicted flux normalization when fitting the spectrum.
* - $v_{\mathrm{bulk,sec}}$
  - Secondary population bulk velocity
  - $\mathrm{km}\,\mathrm{s}^{-1}$
  - Second clump population (mainly Lyα)
  - Constant radial velocity of the second clump population. Positive values indicate outflow and negative values indicate inflow.
* - $R_{\mathrm{line}}$
  - Line-to-continuum photon ratio
  - Dimensionless
  - Net-emission models
  - Ratio of injected line photons to continuum photons within the chosen wavelength window.
* - $r_{\mathrm{pop}}$
  - Fine-structure population ratio
  - Dimensionless
  - C II and Si II
  - Population of the excited ground-term level relative to the lowest level.
```

(lines)=

## Supported spectral lines

| Ion | Wavelengths |
| --- | --- |
| H I | Lyα (1216 Å) |
| C II | 1334.53, 1335.66, 1335.71 Å |
| C IV | 1548.19, 1550.77 Å |
| Mg II | 2796.35, 2803.53 Å |
| Al II | 1670.79 Å |
| Fe II | 1608.45 Å |
| N V | 1238.82, 1242.80 Å |
| S II | 1250.58, 1253.81, 1259.52 Å |
| Si II | 1190.42, 1193.29, 1526.71 Å |
