# Numerical Methods for Orbital Mechanics

## Overview

This project explores the numerical methods used to solve the equations of motion in orbital mechanics, with a focus on numerical integration using Euler's method and the Fourth-Order Runge-Kutta (RK4) method.

The objective is to understand how a spacecraft's position and velocity can be predicted over time by numerically solving its equations of motion.

The concepts and implementations are studied using [Astrodynamics with Python (AWP)](https://github.com/alfonsogonzalez/AWP) by Alfonso Gonzalez.

## 1. Equations of Motion

The motion of a spacecraft orbiting a central body can be described using its position and velocity vectors.

A Cartesian state vector contains six components:
$$
\mathbf{X} =
\begin{bmatrix}
x \\
y \\
z \\
v_x \\
v_y \\
v_z
\end{bmatrix}
$$
Where:

- \(x,y,z\): Position components.
- \(v_x,v_y,v_z\): Velocity components.

The velocity is the first derivative of position with respect to time:

$$
\mathbf{v}=\frac{d\mathbf{r}}{dt}
$$

Acceleration is the derivative of velocity, or the second derivative of position:

$$
\mathbf{a}=\frac{d\mathbf{v}}{dt}
=\frac{d^2\mathbf{r}}{dt^2}
$$

### Two-Body Equation of Motion

Under the two-body gravitational model, the spacecraft's acceleration is:

$$
\boxed{
\mathbf{a}=-\frac{\mu}{r^3}\mathbf{r}
}
$$

Where:

- $\mu = GM$ is the gravitational parameter of the central body.
- $r = \|\mathbf{r}\|$ is the distance between the spacecraft and the central body (the magnitude of the position vector).
- The negative sign indicates that gravitational acceleration acts towards the central body, opposite to the position vector.
Therefore, the equation of motion is:

$$
\boxed{
\frac{d^2\mathbf{r}}{dt^2}
+\frac{\mu}{r^3}\mathbf{r}=0
}
$$

## 2. Converting the Equation into First-Order ODEs

Numerical integration methods are commonly formulated to solve first-order ordinary differential equations.

The second-order equation of motion can be rewritten as two coupled first-order equations:

$$
\frac{d\mathbf{r}}{dt}=\mathbf{v}
$$

$$
\frac{d\mathbf{v}}{dt}
=-\frac{\mu}{r^3}\mathbf{r}
$$

Combining position and velocity into a single state vector:

$$
\mathbf{X}=
\begin{bmatrix}
\mathbf{r}\\
\mathbf{v}
\end{bmatrix}
$$

The system becomes:

$$
\boxed{
\frac{d\mathbf{X}}{dt}
=
\begin{bmatrix}
\mathbf{v}\\
-\dfrac{\mu}{r^3}\mathbf{r}
\end{bmatrix}
}
$$

This can be expressed in the general form:

$$
\frac{d\mathbf{X}}{dt}=F(t,\mathbf{X})
$$

The objective of an ODE solver is to numerically estimate the spacecraft's state at successive time steps.

## 3. Numerical Integration Methods

Numerical integration methods estimate the solution of a differential equation over a specified time interval.

Instead of obtaining an analytical solution, they use the current state and its derivatives to estimate the next state.

### 3.1 Euler's Method

Euler's method is a first-order numerical integration technique.

For a differential equation:

$$
\frac{dy}{dt}=f(t,y)
$$

The next value is estimated using:

$$
\boxed{
y_{n+1}=y_n+h f(t_n,y_n)
}
$$

Where:

- \(y_n\): Current value.
- \(h\): Integration time step.
- \(f(t_n,y_n)\): Slope at the current point.

Euler's method uses the current slope to predict the next value.

For orbital propagation:

$$
\mathbf{X}_{n+1}
=
\mathbf{X}_n+hF(t_n,\mathbf{X}_n)
$$

Its simplicity makes it useful for understanding numerical integration, although its accuracy is limited by its first-order nature.

### 3.2 Fourth-Order Runge-Kutta Method (RK4)

The Fourth-Order Runge-Kutta method improves the estimate by evaluating the slope four times within each integration interval.

For:

$$
\frac{dy}{dt}=f(t,y)
$$

The four slope evaluations are:

**Initial slope:**

$$
k_1=f(t_n,y_n)
$$

**First midpoint slope:**

$$
k_2=f\left(t_n+\frac{h}{2},
y_n+\frac{hk_1}{2}\right)
$$

**Second midpoint slope:**

$$
k_3=f\left(t_n+\frac{h}{2},
y_n+\frac{hk_2}{2}\right)
$$

**Endpoint slope:**

$$
k_4=f(t_n+h,y_n+hk_3)
$$

The next value is calculated using a weighted average:

$$
\boxed{
y_{n+1}=y_n+
\frac{h}{6}(k_1+2k_2+2k_3+k_4)
}
$$

For orbital propagation, the same method is applied to the complete state vector:

$$
\boxed{
\mathbf{X}_{n+1}
=
\mathbf{X}_n+
\frac{h}{6}(K_1+2K_2+2K_3+K_4)
}
$$

Each \(K_i\) represents an evaluation of the derivative of the spacecraft's state.

RK4 is a fourth-order method and generally provides greater accuracy than Euler's method for smooth problems at comparable step sizes.

## 4. How Numerical Methods Propagate an Orbit

The numerical propagation process follows these steps:

1. Define the initial conditions: spacecraft position and velocity.
2. Define the equations of motion, which determine the spacecraft's acceleration.
3. Select a numerical integration method.
4. Calculate the derivatives of the state vector.
5. Estimate the state at the next time step.
6. Use the newly calculated state as the initial state for the next iteration.
7. Repeat until the required propagation duration is reached.

The output is a time history of the spacecraft's position and velocity.

This information can subsequently be used to reconstruct and analyse its orbital trajectory.

## 5. Implementation Using Python

The AWP project separates the equations of motion from the numerical integration algorithms.

### Two-Body Equations of Motion

The `two_body_ode()` function implements the two-body gravitational model:

```python
def two_body_ode(t, state, mu=pd.earth['mu']):

    r = state[:3]

    a = -mu * r / np.linalg.norm(r)**3

    return np.array([
        state[3],
        state[4],
        state[5],
        a[0],
        a[1],
        a[2]
    ])
```

The function receives the spacecraft's six-dimensional state vector and returns its derivatives:

$$
F(t,\mathbf{X})=
\begin{bmatrix}
\mathbf{v}\\
\mathbf{a}
\end{bmatrix}
$$

### Numerical Propagation

The `propagate_ode()` function in the Numerical Tools Library integrates the equations of motion using the selected numerical method.

```python
ets, states = nt.propagate_ode(
    oc.two_body_ode,
    state0,
    tspan,
    dt,
    method='rk4'
)
```

Here:

- `state0`: Initial position and velocity.
- `tspan`: Propagation duration.
- `dt`: Integration time step.
- `method`: Selected numerical integration method.
- `ets`: Time values.
- `states`: Calculated spacecraft states.

The numerical method can be selected independently of the equations of motion.

This separation allows different integration algorithms to be used with the same physical model.

## 6. Key Takeaways

- A spacecraft's instantaneous Cartesian state is described by three position and three velocity components.
- The equation of motion describes how gravitational forces change the spacecraft's velocity.
- Second-order equations of motion can be rewritten as coupled first-order ODEs.
- Numerical integration estimates the spacecraft's state at successive time steps.
- Euler's method uses one slope evaluation per step.
- RK4 uses four slope evaluations and a weighted average to improve the estimate.
- The choice of integration method, time step and accuracy requirements influences the quality of orbit propagation.

---

**References**

- [Astrodynamics with Python (AWP) – Alfonso Gonzalez](https://github.com/alfonsogonzalez/AWP)
- [AWP YouTube Channel](https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering)
- Numerical methods and ordinary differential equations.