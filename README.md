# SkoltechGamez
This repository contains the source code and simulations developed for two areas of applied research: Optical Physics (digital signal processing and beam propagation) and Operations Engineering (supply chain management )



# Bessel Beam Generation and Superposition: Numerical Characterization

This section describes the generation and numerical simulation of Bessel beams and their superposition, as presented in the work by Gámez et al. The methods and results cover both experimental setups and MATLAB-based computations.

---

##  Introduction

Bessel beams are particular solutions to the electromagnetic wave equation that exhibit the remarkable property of **diffraction-free** propagation. Unlike ordinary Gaussian beams, which spread with distance, a Bessel beam maintains a constant transverse intensity profile over a certain propagation length $$Z_{\text{max}}$$ . This behaviour arises from a specific transverse intensity distribution described by Bessel functions of the first kind.

The experimental generation of Bessel beams is commonly achieved using an **annular aperture mask** illuminated by a plane wave, followed by a converging lens placed at its focal distance. The light diffracted by the annular slit produces a Bessel beam.

To generate a superposition of two Bessel beams, a **Michelson interferometer** is used to split the beam intensity, with the beam splitter placed just after the lens to ensure operation within the diffraction-free region. By adjusting the optical path difference between the two arms, one can control the separation and relative phase of the two beams—parameters that are systematically characterised.


##  Superposition of Two Bessel Beams

When two Bessel beams (with possibly different amplitudes, phases, and spatial offsets) are superposed, the resulting intensity distribution is obtained by adding their complex fields and taking the squared modulus:

$$ I_{\text{total}}(r, \phi, z) = \left| E_1(r, \phi, z) + E_2(r, \phi, z) \right|^2 $$

This superposition gives rise to characteristic interference patterns that depend on the relative phase and separation. The experimental cross‑sections  and their corresponding numerical simulations  demonstrate excellent agreement.

<div align="center">
  <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/2ad4dededf0504931ff66ec8555e5782915cb15f/interfe.png" alt="Patrón de interferencia de dos haces Bessel" style="width: 50%;"/>
  <br>
  <em>Figure: The experimental superposition of two Bessel beams.</em>
</div>

##  Numerical Simulations in MATLAB


The complete MATLAB script is available in this repository. You can view it online or download it directly using the links below:

- 📄 **[View the full code on GitHub](https://github.com/GamexIan/SkoltechGamez/blob/ec8e202388b58fda8247028848153173a5ad01f9/twobeams.m)** 


<div align="center">
  <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/ec8e202388b58fda8247028848153173a5ad01f9/interfeskol.png" alt="Numerical interference pattern of two Bessel beams" style="width: 50%;"/>
  <br>
  <em>Figure: The numerical superposition of two Bessel beams, showing the characteristic interference fringes.</em>
</div>



# Gaussian Beam Propagation in Nonlinear Media

This section covers the numerical simulation of a Gaussian beam propagating through a thin nonlinear optical medium with local and nonlocal Kerr-type nonlinearities. The implementation uses the **split-step Fourier method** (SSFM) to solve the paraxial wave equation, capturing self-phase modulation, diffraction, and absorption effects.

---

## 1. Introduction

When a material exhibits an intensity‑dependent refractive index, a well‑defined incident intensity distribution is modified as it propagates through the sample. The light–matter interaction determines the nature of the nonlinear response, which can be local or non‑local. This work presents a numerical model to describe the local nonlinear response of a thin medium under Gaussian illumination, considering the field at the exit plane of the material. A Fourier transform is then applied to obtain far‑field diffraction patterns.

The model accounts for locality by modifying the width of the phase‑change profile at the sample exit, referencing the incident intensity profile. Locality also affects the magnitude of the on‑axis nonlinear phase shift and the field amplitude.

---

## 2. Theoretical Model

### 2.1 Gaussian Beam Propagation

A Gaussian beam (see Eq. (2.29) in the original work) with waist \( \omega_0 \) and wavelength \( \lambda \) has a complex amplitude at the exit of the medium given by:

$$
E(r, z) = A_0 \frac{\omega_0}{\omega(z)}\exp\left[-\frac{r^2}{\omega(z)^2}\right]\exp\left[-\frac{\alpha L}{2}\right]\exp\left[-ikz - ik\frac{r^2}{2R(z)} + i\zeta(z)\right], \tag{4.1}
$$

where:
- \( A_0 \) is the amplitude constant,
- \( \omega(z) \) is the beam width at distance \( z \),
- \( R(z) \) is the wavefront curvature radius,
- \( \zeta(z) \) is the Gouy phase,
- \( L \) is the sample thickness,
- \( \alpha \) is the linear absorption coefficient.

For a thin sample (\( L \ll z_0 \), with \( z_0 \) the Rayleigh length), the field is assumed to acquire only a small phase change \( \Delta\phi \) at the output. This phase change is obtained by integrating the refractive‑index change along the sample:

$$
\Delta \phi = k \int_{0}^{L} \Delta n(I) \, dz, \tag{4.2}
$$

where \( \Delta n(I) \) represents the nonlinear contribution to the refractive index.

### 2.2 Nonlocal Nonlinear Response

In the most general case, the nonlinear index change can be expressed as a convolution with a response function \( R(\mathbf{r}) \) [32]:

$$
\Delta n(I) = s \int R(\vec{\xi} - \vec{r})\, I(\vec{\xi}, z)\, d\vec{\xi}, \tag{4.4}
$$

where:
- \( s = +1 \) for self‑focusing (positive nonlinearity),
- \( s = -1 \) for self‑defocusing (negative nonlinearity),
- \( R(\mathbf{r}) \) is a real, symmetric, normalised response function (\( \int R \, d\mathbf{r} = 1 \)).

For a purely local response, \( R(\mathbf{r}) = \delta(\mathbf{r}) \), and we recover:

$$
\Delta n = s \, I(\mathbf{r}, z). \tag{4.5}
$$

In this work we focus on the local case and use a Gaussian response function for numerical implementation:

$$
R(x, y) = \frac{1}{2\pi\sigma_{nl}^2} \exp\left(-\frac{x^2 + y^2}{2\sigma_{nl}^2}\right), \tag{4.6}
$$

where \( \sigma_{nl} \) is the characteristic width of the nonlocal response [42].

---

## 3. Numerical Method: Split‑Step Fourier (SSFM)

We start from the scalar Helmholtz equation for a single frequency component:

$$
\frac{\partial^2 E}{\partial x^2} + \frac{\partial^2 E}{\partial y^2} + \frac{\partial^2 E}{\partial z^2} + \frac{\omega^2}{c^2} n^2(\omega, x, y) E = 0. \tag{4.7}
$$

Under the **paraxial approximation** (slowly varying envelope), the field is written as \( E(x,y,z) = \psi(x,y,z) e^{-ikz} \), leading to the paraxial wave equation:

$$
\nabla_{\perp}^2 \psi - 2ik \frac{\partial \psi}{\partial z} + 2k^2 \frac{\Delta n(I)}{n_0} \psi + ik\alpha(I) \psi = 0, \tag{4.21}
$$

with:
- \( \nabla_{\perp}^2 = \partial_x^2 + \partial_y^2 \),
- \( \Delta n(I) = n_2 I + s (R * I) \) (local and nonlocal contributions),
- \( \alpha(I) = \alpha_0 + \beta I \) (linear and nonlinear absorption),
- \( n_2 \) the Kerr coefficient.

### 3.1 Operator Splitting

Equation (4.21) can be written as:

$$
\frac{\partial \psi}{\partial z} = (\hat{D} + \hat{N}) \psi, \tag{4.22}
$$

where:
- \( \hat{D} = \frac{i}{2k} \nabla_{\perp}^2 \) is the diffraction operator,
- \( \hat{N} = \frac{i k}{n_0} \Delta n(I) - \frac{\alpha(I)}{2} \) is the nonlinear operator.

For a small propagation step \( h \), the formal solution is approximated by the symmetric split‑step:

$$
\psi(z+h) \approx \exp\left(\frac{h}{2}\hat{N}\right) \exp\left(h\hat{D}\right) \exp\left(\frac{h}{2}\hat{N}\right) \psi(z). \tag{4.29}
$$

The diffraction step is performed in the Fourier domain using the paraxial transfer function:

$$
\mathcal{L}_{\text{paraxial}}(\Delta z) = \exp\left[-i \Delta z \frac{k_x^2 + k_y^2}{2k}\right], \tag{4.43}
$$

where \( k_x, k_y \) are transverse spatial frequencies.

### 3.2 Algorithm Steps

For each propagation step \( \Delta z \):

1. **Nonlinear half‑step:**  
   \( \psi^{(1)} = \exp\left(\frac{\Delta z}{2}\hat{N}\right) \psi(z) \)

2. **Diffraction (Fourier domain):**  
   \( \psi^{(2)} = \mathcal{F}^{-1}\left[ \mathcal{L}_{\text{paraxial}}(\Delta z) \cdot \mathcal{F}(\psi^{(1)}) \right] \)

3. **Nonlinear half‑step:**  
   \( \psi(z+\Delta z) = \exp\left(\frac{\Delta z}{2}\hat{N}\right) \psi^{(2)} \)

This symmetric scheme is second‑order accurate in \( \Delta z \) and unconditionally stable.

---



