import matplotlib.pyplot as plt

def plot_median_and_rps(results):
    
    ordered_results = sorted(results.items())
    x = [i[0] for i in ordered_results]
    ys = [i[1] for i in ordered_results]
    fig, ax1 = plt.subplots()
    median, = ax1.plot(x, [y[2] for y in ys], label='median', color='b')
    ax1.fill_between(x,
                     [y[1] for y in ys],
                     [y[3] for y in ys],
                    alpha=0.3)
    ax1.set_xlabel('# of concurrent clients')
    ax1.set_ylabel('ms', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    rps, = ax2.plot(x, [y[5] for y in ys], label='rps', color='r')
    ax2.set_ylabel('rps', color='r')
    for tl in ax2.get_yticklabels():
            tl.set_color('r')
    ax2.legend(handles=[median, rps])
    plt.show()
