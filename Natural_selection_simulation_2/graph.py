import matplotlib.pyplot as plt
import numpy as np

def plot(wolfCount, rabbitCount, rabbitMS, rabbitS, rabbitT, wolfMS, wolfS, id):
    
    x = range(0,len(wolfCount))
    plt.plot(x, rabbitCount, color = 'black', label = 'Rabbit count')
    plt.plot(x, wolfCount, color = 'red', label = 'Wolf count')
    plt.plot(x, rabbitMS, color = 'green', label = 'Rabbit movement speed')
    plt.plot(x, rabbitS, color = 'cornflowerblue', label = 'Rabbit sense')
    plt.plot(x, rabbitT, color = 'purple', label = 'Rabbit threat sense')
    plt.plot(x, wolfMS, color = 'darkgreen', label = 'Wolf movement speed')
    plt.plot(x, wolfS, color = 'royalblue', label = 'Wolf sense')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_'+str(id)+'.png')

