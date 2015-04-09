import numpy as np
import matplotlib as mpl
from statsmodels.nonparametric.kernel_density import KDEMultivariate
mpl.use("agg")
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.ioff()


def maxwell_boltzman(v, kT, m):
    return \
        (m / (2 * np.pi * kT))**1.5 \
        * 4.0 * np.pi * v**2 \
        * np.exp(- (m * v**2) / (2 * kT))


def set_plt_params(
        relative_fig_width=1.0, landscape=True, page_width=307.3, rescale_h=1):

    fig_width_pt = page_width * relative_fig_width
    inches_per_pt = 1.0 / 72.27               # Convert pt to inch
    golden_mean = (np.sqrt(5.0) - 1.0) / 2.0  # Aesthetic ratio
    fig_width = fig_width_pt * inches_per_pt  # width in inches

    if landscape:
        fig_height = fig_width * golden_mean  # height in inches
    else:
        fig_height = fig_width / golden_mean  # height in inches

    fig_height = fig_height * rescale_h
    fig_size = [fig_width, fig_height]
    params = {
        'font.family': 'serif',
        'axes.labelsize': 7,
        'xtick.labelsize': 5,
        'ytick.labelsize': 5,
        'axes.labelcolor': 'black',
        'ytick.color': 'black',
        'xtick.color': 'black',
        'legend.handlelength': 4,
        'legend.fontsize': 7,
        # 'lines.markersize': 3,
        # 'xtick.labelsize': 7,
        # 'ytick.labelsize': 7,
        'text.usetex': True,
        'text.latex.unicode': True,
        'figure.figsize': fig_size,
        'pgf.texsystem': "xelatex",
        'pgf.rcfonts': False,
    }

    plt.rcParams.update(params)

set_plt_params()

N0 = 2480
N = 4500

data = dict(
    (
        n,
        np.genfromtxt(
            "pdf/v-{0:04d}.csv".format(n),
            delimiter=' ')
    ) for n in range(N))
Tdata = np.genfromtxt("sim.csv", delimiter=' ')
T = Tdata[:, 2]
t = Tdata[:, 1]

x = np.linspace(0, 3, 300)

for n in np.arange(N0, N):
    kde = KDEMultivariate(data[n], bw='normal_reference', var_type='c')
    fig = plt.figure()
    ax = fig.gca()
    fig.subplots_adjust(wspace=0)
    fig.suptitle("Time = {0:.2f} s".format(t[n]), fontsize=7)

    ax.set_ylim(-0.01, 2.5)
    plt.xlabel("Velocity norm")
    plt.ylabel("PDF")
    # Fix the seed for reproducibility
    ax.plot(x, kde.pdf(x), label="Simulation")
    ax.plot(
        x,
        maxwell_boltzman(v=x, m=1, kT=T[n]),
        label="Maxwell-Boltzmann")
    ax.legend(loc='upper right', shadow=True)
    fig.savefig(
        "v-pdf{0:04d}.png".format(n),
        bbox_inches='tight', dpi=300)
    plt.close()
