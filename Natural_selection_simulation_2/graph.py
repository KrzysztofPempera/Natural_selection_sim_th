import matplotlib.pyplot as plt
import numpy as np

def plot(foodCount ,wolfCount, rabbitCount, rabbitMS, rabbitS, rabbitT, wolfMS, wolfS, id):
    
    x = range(0,len(wolfCount))

    plt.figure(1, figsize=(17,8))
    plt.plot(x, rabbitCount, color = 'black', label = 'Rabbit count')
    plt.plot(x, wolfCount, color = 'red', label = 'Wolf count')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_obj_'+str(id)+'.png')
    

    plt.figure(2, figsize=(17,8))
    plt.plot(x, rabbitMS, color = 'green', label = 'Rabbit movement speed')
    plt.plot(x, rabbitS, color = 'cornflowerblue', label = 'Rabbit sense')
    plt.plot(x, rabbitT, color = 'purple', label = 'Rabbit threat sense')
    plt.plot(x, rabbitCount, color = 'black', label = 'Rabbit count')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_rb_'+str(id)+'.png')

    plt.figure(3, figsize=(17,8))
    plt.plot(x, wolfMS, color = 'darkgreen', label = 'Wolf movement speed')
    plt.plot(x, wolfS, color = 'royalblue', label = 'Wolf sense')
    plt.plot(x, wolfCount, color = 'red', label = 'Wolf count')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_wlf_'+str(id)+'.png')

    plt.figure(4, figsize=(17,8))
    plt.plot(x, wolfMS, color = 'red', label = 'Wolf movement speed')
    plt.plot(x, rabbitMS, color = 'black', label = 'Rabbit movement speed')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_ms_'+str(id)+'.png')

    plt.figure(5, figsize=(17,8))
    plt.plot(x, wolfS, color = 'red', label = 'Wolf sense')
    plt.plot(x, rabbitS, color = 'black', label = 'Rabbit sense')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_sen_'+str(id)+'.png')

    plt.figure(6, figsize=(17,8))
    plt.plot(x, wolfMS, color = 'red', label = 'Wolf movement speed')
    plt.plot(x, rabbitCount, color = 'black', label = 'Rabbit count')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_msW_'+str(id)+'.png')

    plt.figure(7, figsize=(17,8))
    plt.plot(x, rabbitMS, color = 'red', label = 'Rabbit movement speed')
    plt.plot(x, foodCount, color = 'black', label = 'Carrot count')
    plt.ylabel('Stuff')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('plots/plot_msR_'+str(id)+'.png')