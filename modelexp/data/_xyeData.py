import numpy as np
from ._data import Data

class XyeData(Data):
  def __init__(self):
    super().__init__()
    self.x = []
    self.y = []
    self.e = []

  def setData(self, x, y, e):
    """Set the data of an .xye file

    Parameters
    ----------
    x : :obj: `array_like`
      Domain
    y : :obj: `array_like`
      Values
    e : :obj: `array_like`
      Errors
    """
    self.x = np.array(x)
    self.y = np.array(y)
    self.e = np.array(e)

  def getData(self):
    return self.x, self.y, self.e

  def getDomain(self):
    return self.x

  def getValues(self):
    return self.y

  def getErrors(self):
    return self.e

  def loadFromFile(self, filename):
    self.filename = filename
    fileData = np.genfromtxt(filename)
    x = fileData[:,0]
    y = fileData[:,1]
    e = fileData[:,2]
    sortedArgs = np.argsort(x)
    x = x[sortedArgs]
    y = y[sortedArgs]
    e = e[sortedArgs]
    self.setData(x, y, e)

  def plotData(self, ax):
    ax.errorbar(self.x, self.y, self.e, ls='None', marker='.', zorder=5)

  def sliceDomain(self, minX=-np.inf, maxX=np.inf):
    slicedDomain = np.logical_and(minX < self.x, self.x < maxX)
    self.xMask = self.x[~slicedDomain]
    self.yMask = self.y[~slicedDomain]
    self.eMask = self.e[~slicedDomain]
    self.x = self.x[slicedDomain]
    self.y = self.y[slicedDomain]
    self.e = self.e[slicedDomain]

  def addDataLine(self, dataline):
    assert len(dataline) == 3, 'Tried to add a dataline that does not have 3 elements to a XYE dataset: ' + str(dataline)
    self.x.append(dataline[0])
    self.y.append(dataline[1])
    self.e.append(dataline[2])