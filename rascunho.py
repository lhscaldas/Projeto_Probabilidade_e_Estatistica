
import numpy as np
import matplotlib.pyplot as plt

# função que plota duas senoides com defasagem temporal
def plot_senoides():
    

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

# plot_senoides()

x=1000
print(1+3.3219*np.log10(x))
print(1+np.log2(x))