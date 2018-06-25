from .plotWidget import PlotWidget
import matplotlib.pyplot as plt

class PlotWidgetInset(PlotWidget):
  def defineAx(self):
    x0, y0 = 0.15, 0.15
    self.ax = self.fig.add_axes([x0, y0, 1-x0-0.02, 1-y0-0.02])
    self.ax.set_xlabel(r"$\mathit{x}$")
    self.ax.set_ylabel(r"$\mathit{y}$")

    x0In, y0In = 0.7, 0.7
    self.axInset = self.fig.add_axes([x0In, y0In, 1-x0In-0.02, 1-y0In-0.02])
    self.axInset.set_xlabel(r"$\mathit{x}_{in}$")
    self.axInset.set_ylabel(r"$\mathit{y}_{in}$")

    self.fig.tight_layout()
    self.draw()

  def getAllAx(self):
    return self.ax, self.axInset
