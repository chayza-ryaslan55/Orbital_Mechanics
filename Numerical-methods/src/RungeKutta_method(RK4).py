
import numpy as np
import matplotlib.pyplot as plt


def rk4_step(f, t, y, h):
    '''
    Calculate one RK4 step
    '''
    k1 = f(t, y)
    k2 = f(t + 0.5*h, y + 0.5*k1*h)
    k3 = f(t + 0.5*h, y + 0.5*k2*h)
    k4 = f(t + h, y + k3*h)

    return y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)


# Differential equation: dy/dt = t
def df(t, y):
    return t


# Analytical solution: y(t) = t²/2
def f(t):
    return t**2 / 2.0


# Numerical integration methods
methods = {
    'rk4': rk4_step
}


if __name__ == '__main__':

    h = 0.2
    xs = np.arange(0, 5 + h, h)
    n_steps = len(xs)

    # Analytical solution
    ys_analytical = f(xs)

    # Initialise RK4 solution
    ys_rk4 = np.zeros(n_steps)

    # Initial condition: y(0) = 0
    ys_rk4[0] = 0.0

    # RK4 integration
    for n in range(1, n_steps):
        ys_rk4[n] = rk4_step(
            df,
            xs[n-1],
            ys_rk4[n-1],
            h
        )

    # Calculate error
    errors = ys_rk4 - ys_analytical

    # Plot results
    plt.figure(figsize=(16, 8))

    plt.plot(xs, ys_analytical, 'm',
             label='Analytical Solution')

    plt.plot(xs, ys_rk4, 'c',
             label='RK4 Method Solution')

    plt.plot(xs, ys_rk4, 'co')

    plt.plot(xs, errors, 'r',
             label='RK4 Method Error')

    plt.plot(xs, errors, 'ro')

    plt.grid(linestyle='dotted')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$y$')

    plt.legend(prop={'size': 15})

    title = "RK4 Method to Solve: "
    title += r'$\dfrac{dy}{dt}=t$, '
    title += r'Solution: $y(t)=\dfrac{t^2}{2}$'

    plt.title(title, fontsize=15)

    plt.show()
