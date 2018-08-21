from ._reflModel import ReflectometryModel
from fortRefl import nanospheres, algorithms
import numpy as np

class SphereCSStacked6(ReflectometryModel):
  '''
  Model to describe the formfactor of a sphere
  '''
  def initParameters(self):
    self.params.add("i0", 1, min = 0, max = 2, vary = False)
    self.params.add("bg", 2.1000000000000002e-06, min = 0.0, max = 0.0001, vary = False)
    self.params.add("roughness", 11.84, min = 0.0, max = 20, vary = True)
    self.params.add("roughnessIncrease", 0.0659859354001, min = 0.0, max = 1, vary = True)
    self.params.add("packingDensity1", 0.517, min = 0.0, max = 1.0, vary = True)
    self.params.add("packingDensity2", 0.517, min = 0.0, max = 1.0, vary = True)
    self.params.add("packingDensity3", 0.517, min = 0.0, max = 1.0, vary = True)
    self.params.add("packingDensity4", 0.517, min = 0.0, max = 1.0, vary = True)
    self.params.add("packingDensity5", 0.517, min = 0.0, max = 1.0, vary = True)
    self.params.add("packingDensity6", 0.517, min = 0.0, max = 1.0, vary = True)
    self.params.add("layerDistance1", 0, min = -30, max = 30, vary = True)
    self.params.add("layerDistance2", 0, min = -30, max = 30, vary = True)
    self.params.add("layerDistance3", 0, min = -30, max = 30, vary = True)
    self.params.add("layerDistance4", 0, min = -30, max = 30, vary = True)
    self.params.add("layerDistance5", 0, min = -30, max = 30, vary = True)
    self.params.add("layerDistance6", 0, min = -30, max = 30, vary = True)
    self.params.add("r", 50, min = 0, max = 100, vary = True)
    self.params.add("d", 20, min = 0, max = 40, vary = True)
    self.params.add("sigR", 0, min = 0, max = 0.20, vary = True)
    self.params.add('sldCore', 8e-6, min= 0, max = 40e-6, vary=False)
    self.params.add('sldShell', 10e-7, min= 0, max = 40e-6, vary=False)
    self.params.add('sldSubstrate', 2e-6, min= 0, max = 40e-6, vary=False)
    self.params.add('sldBackground', 0e-6, min= 0, max = 40e-6, vary=False)

    self.addConstantParam('sldBackground')

  def initMagneticParameters(self):
    self.params.add('magSldCore', 1e-6)
    self.params.add('magSldShell', 0, vary=False)

    self.addConstantParam('magSldSolvent')

  def calcModel(self):
    if (self.z is not None):
      sphere_shifts = [self.params["layerDistance1"].value,\
                       self.params["layerDistance2"].value,\
                       self.params["layerDistance3"].value,\
                       self.params["layerDistance4"].value,\
                       self.params["layerDistance5"].value,\
                       self.params["layerDistance6"].value]
      packing_densities = [self.params["packingDensity1"].value,
                           self.params["packingDensity2"].value,
                           self.params["packingDensity3"].value,
                           self.params["packingDensity4"].value,
                           self.params["packingDensity5"].value,
                           self.params["packingDensity6"].value]

      sld = nanospheres.sphere_cs_overlapping_stacked(
        self.z, sphere_shifts, packing_densities,
        self.params['r'].value, self.params['sigR'].value, self.params['d'].value,
        self.params['sldCore'].value, self.params['sldShell'].value, self.params['sldSubstrate'].value,
        self.params['sldBackground'].value)
      roughness = self.params["roughness"]*np.ones(len(sld))
      positiveValues = self.z > 0
      roughness[positiveValues] = self.params["roughnessIncrease"]*self.z[positiveValues]
      thickness = (self.z[1] - self.z[0])*np.ones(len(sld))

      self.I = self.params["i0"] * algorithms.parrat(self.q, sld, roughness, thickness)  + self.params["bg"]
      self.sld = algorithms.roughsld_thick_layers(self.z, sld, roughness, thickness).real

  def calcMagneticModel(self):
    self.calcModel()
    # self.I = self.params['i0'] * sphere.magnetic_formfactor(
    #   self.q,
    #   self.params['r'],
    #   self.params['sldCore'],
    #   self.params['sldSolvent'],
    #   self.params['sigR'],
    #   self.params['magSldCore'],
    #   self.params['magSldSolvent'],
    #   self.params['xi'],
    #   self.params['sin2alpha'],
    #   self.params['polarization'],
    # ) + self.params['bg']

    # self.r, self.sld = sphere.sld(
    #   self.params['r'],
    #   self.params['sldCore'],
    #   self.params['sldSolvent']
    # )

    # self.rMag, self.sldMag = sphere.sld(
    #   self.params['r'],
    #   self.params['magSldCore'],
    #   self.params['magSldMatrix']
    # )
