import modelexp
from modelexp.experiments.sas import Saxs
from modelexp.models.sas import Sphere
from modelexp.data import XyeData
from modelexp.fit import LevenbergMarquardt

app = modelexp.App()

app.setExperiment(Saxs)

dataRef = app.setData(XyeData)
dataRef.loadFromFile('./saxsSphereData.xye')
dataRef.plotData()

modelRef = app.setModel(Sphere)
modelRef.setParam("R", 49.900000000000006,  minVal = 0, maxVal = 100, vary = True)
modelRef.setParam("SLDsphere", 4.5e-05,  minVal = 0, maxVal = 0.00045000000000000004, vary = False)
modelRef.setParam("SLDsolvent", 1e-05,  minVal = 0, maxVal = 0.0001, vary = False)
modelRef.setParam("sigR", 0.049800000000000004,  minVal = 0, maxVal = 0.2, vary = True)
modelRef.setParam("I0", 1.02,  minVal = 0, maxVal = 10, vary = True)
modelRef.setParam("bg", 0.0,  minVal = 0, maxVal = 1, vary = False)

app.setFit(LevenbergMarquardt)

app.show()