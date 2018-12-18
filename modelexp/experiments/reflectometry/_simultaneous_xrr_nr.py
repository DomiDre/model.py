from ._refl import Reflectometry

class SimultaneousXRNR(Reflectometry):
  def __init__(self):
    super().__init__()
    self.nDatasets = 2
    self.datasetSpecificParams = {
      'dTheta': ['xrr', 'nr'],
      'dWavelength': ['xrr', 'nr'],
      'i0': ['xrr', 'nr'],
      'bg': ['xrr', 'nr'],
      'sldCore': ['xrr', 'nr'],
      'sldShell': ['xrr', 'nr'],
      'sldSubstrate': ['xrr', 'nr'],
      'sldBackground': ['xrr', 'nr'],
      'sldSpacer': ['xrr', 'nr'],
      }
