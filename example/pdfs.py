import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
with PdfPages("multipage_pdf.pdf") as pdf:
    plt.figure(figsize=(3, 3))
    plt.plot(range(7), [3, 1, 4, 1, 5, 9, 2], "r-o")
    plt.title("Page One")
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

    # # if LaTeX is not installed or error caught, change to `usetex=False`
    # plt.rc('text', usetex=False)
    # plt.figure(figsize=(8, 6))
    # x = np.arange(0, 5, 0.1)
    # plt.plot(x, np.sin(x), 'b-')
    # plt.title('Page Two')
    # pdf.attach_note("plot of sin(x)")  # you can add a pdf note to
    #                                    # attach metadata to a page
    pdf.savefig()
    plt.close()

    # plt.rc('text', usetex=False)
    # fig = plt.figure(figsize=(4, 5))
    # plt.plot(x, x ** 2, 'ko')
    # plt.title('Page Three')
    # pdf.savefig(fig)  # or you can pass a Figure object to pdf.savefig
    # plt.close()

    # # We can also set the file's metadata via the PdfPages object:
    # d = pdf.infodict()
    # d['Title'] = 'Multipage PDF Example'
    # d['Author'] = 'Jouni K. Sepp\xe4nen'
    # d['Subject'] = 'How to create a multipage pdf file and set its metadata'
    # d['Keywords'] = 'PdfPages multipage keywords author title subject'
    # d['CreationDate'] = datetime.datetime(2009, 11, 13)
    # d['ModDate'] = datetime.datetime.today()


with PdfPages("multipage.pdf") as pp:
    for i in range(0, 10):
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        x = np.linspace(0, 10)
        ax1.plot(x, np.sin(x + i * np.pi / 10))
        ax2.plot(x, np.cos(x + i * np.pi / 10))
        pp.savefig(fig)


# Initialize:
with PdfPages("foo.pdf") as pdf:
    # As many times as you like, create a figure fig and save it:
    fig = plt.figure()
    pdf.savefig(fig)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    x = np.linspace(0, 10)
    ax1.plot(x, np.sin(x + i * np.pi / 10))
    ax2.plot(x, np.cos(x + i * np.pi / 10))
    # When no figure is specified the current figure is saved
    pdf.savefig()
