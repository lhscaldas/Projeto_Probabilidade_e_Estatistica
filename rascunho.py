

# função que plota duas senoides com defasagem temporal
def plot_senoides():
    import numpy as np
    import matplotlib.pyplot as plt

    # cria um vetor de tempo
    t = np.linspace(0, 2*np.pi, 1000)

    # cria as senoides
    s1 = np.sin(t)
    s2 = np.sin(t - np.pi/2)

    # plota as senoides
    plt.plot(t, s1, label='seno(t)')
    plt.plot(t, s2, label='seno(t - pi/2)')
    plt.legend()
    plt.show()

plot_senoides()