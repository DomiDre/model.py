import modelexp
from modelexp.experiments.sas import Sans
from modelexp.models.sas import Sphere
from modelexp.data import XyeData
from modelexp.fit import LevenbergMarquardt

from modelexp.models.sas import InstrumentalResolution

app = modelexp.App()

app.setExperiment(Sans)

dataRef = app.setData(XyeData)
dataRef.loadFromFile('./sansSphereData_sa.xye', 'sa')
dataRef.loadFromFile('./sansSphereData_la.xye', 'la')
dataRef.plotData()

modelRef = app.setModel(Sphere, InstrumentalResolution)
modelRef.setParam("r", 49.900000000000006,  minVal = 0, maxVal = 100, vary = True)
modelRef.setParam("sldSphere", 4.5e-05,  minVal = 0, maxVal = 0.00045000000000000004, vary = False)
modelRef.setParam("sldSolvent", 1e-05,  minVal = 0, maxVal = 0.0001, vary = False)
modelRef.setParam("sigR", 0.049800000000000004,  minVal = 0, maxVal = 0.2, vary = True)
modelRef.setParam("i0", 1.02,  minVal = 0, maxVal = 10, vary = True)
modelRef.setParam("bg", 0.0,  minVal = 0, maxVal = 1, vary = False)

app.setFit(LevenbergMarquardt)

app.show()