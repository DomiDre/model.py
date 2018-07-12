from .._experiment import Experiment
import numpy as np
from ...gui.plotWidgetInset import PlotWidgetInset

class Sas(Experiment):
  def __init__(self):
    super().__init__()
    self.plotWidgetClass = PlotWidgetInset

  def connectGui(self, gui):
    self.ptrGui = gui
    self.fig = self.ptrGui.plotWidget.getFig()
    self.ax, self.axInset = self.ptrGui.plotWidget.getAllAx()

  def setAxProps(self):
    self.ax.set_xlabel(r'$\mathit{q} \, / \, \AA^{-1}$')
    self.ax.set_ylabel(r'$\mathit{I} \, / \, cm^{-1}$')
    self.ax.set_xscale('log')
    self.ax.set_yscale('log')

    self.axInset.set_xlabel(r"$\mathit{x} \, / \, \AA$")
    self.axInset.set_ylabel(r"$SLD$")

    self.ptrGui.plotWidget.draw_idle()# .tight_layout()

  def residuum(self, p):
    self.model.params = p
    self.model.updateModel()
    resi = []
    for i in range(self.model.nModelsets):
      data = self.data.getDataset(i)
      model = self.model.getModelset(i)
      I_data = data.getValues()
      I_error = data.getErrors()
      I_model = model.getValues()
      addResi = (np.log(I_data) - np.log(I_model)) * I_data / I_error
      resi = np.concatenate([resi, addResi])
    return resi

  def getMinMaxDomainData(self):
    minQ = np.inf
    maxQ = -np.inf
    for i in range(self.data.nDatasets):
      data = self.data.getDataset(i)
      qData = data.getDomain()
      minQ = min(minQ, min(qData))
      maxQ = max(maxQ, max(qData))
    return minQ, maxQ

  def getMinMaxValueData(self):
    minI = np.inf
    maxI = -np.inf
    for i in range(self.data.nDatasets):
      data = self.data.getDataset(i)
      IData = data.getValues()
      minI = min(minI, min(IData))
      maxI = max(maxI, max(IData))
    return minI, maxI

  def getMinMaxDomainModel(self):
    minQ = np.inf
    maxQ = -np.inf
    for i in range(self.model.nModelsets):
      model = self.model.getModelset(i)
      qModel = model.getDomain()
      minQ = min(minQ, min(qModel))
      maxQ = max(maxQ, max(qModel))
    return minQ, maxQ

  def getMinMaxValueModel(self):
    minI = np.inf
    maxI = -np.inf
    for i in range(self.model.nModelsets):
      model = self.model.getModelset(i)
      IModel = model.getValues()
      minI = min(minI, min(IModel))
      maxI = max(maxI, max(IModel))
    return minI, maxI

  def adjustAxToAddedData(self):
    qMin, qMax = self.getMinMaxDomainData()
    IMin, IMax = self.getMinMaxValueData()
    self.ax.set_xlim(qMin, qMax)
    self.ax.set_ylim(IMin*0.8, IMax*.12)


  def adjustAxToAddedModel(self):
    qModelMin, qModelMax = self.getMinMaxDomainModel()
    IModelMin, IModelMax = self.getMinMaxValueModel()
    if hasattr(self, 'data'):
      qDataMin, qDataMax = self.getMinMaxDomainData()
      IDataMin, IDataMax = self.getMinMaxValueData()
    else:
      qDataMin, qDataMax = np.inf, -np.inf
      IDataMin, IDataMax = np.inf, -np.inf
    self.ax.set_xlim(
      min(qModelMin, qDataMin),
      max(qModelMax, qDataMax)
    )
    self.ax.set_ylim(
      min(IModelMin, IDataMin)*0.8,
      max(IModelMax, IDataMax)*1.2
    )

    model0 = self.model.getModelset(0)
    r_model = model0.r
    sld_model = model0.sld
    self.axInset.set_xlim(min(r_model)/10, max(r_model)/10)
    self.axInset.set_ylim(0, max(sld_model)/1e-6*1.2)

  def saveModelDataToFile(self, f):
    if hasattr(self, 'data') and hasattr(self, 'model'):
      for i in range(self.model.nModelsets):
        data = self.data.getDataset(i)
        model = self.model.getModelset(i)

        q_data = data.getDomain()
        I_data = data.getValues()
        sI_data = data.getErrors()
        q_model = model.getDomain()
        I_model = model.getValues()
        assert(len(q_data) == len(q_model), 'Data and Model do not have the same length.')
        if isinstance(data.suffix, str):
          f.write(f'\n#[[Data]] {data.suffix}\n')
        elif isinstance(data.suffix, list):
          f.write('\n#[[Data]] '+'_'.join(data.suffix)+'\n')
        f.write('#q / A-1\tI / cm-1\tsI / cm-1\tImodel / cm-1\n')
        for i in range(len(q_data)):
          assert(np.isclose(q_data[i], q_model[i]), 'Data and Model arrays are not defined on same domain' )
          f.write(f'{q_data[i]}\t{I_data[i]}\t{sI_data[i]}\t{I_model[i]}\n')
    elif hasattr(self, 'data'):
      for i in range(self.data.nDatasets):
        data = self.data.getDataset(i)
        q_data = data.getDomain()
        I_data = data.getValues()
        sI_data = data.getErrors()
        if isinstance(data.suffix, str):
          f.write(f'\n#[[Data]] {data.suffix}\n')
        elif isinstance(data.suffix, list):
          f.write('\n#[[Data]] '+'_'.join(data.suffix)+'\n')
        f.write('#q / A-1\tI / cm-1\tsI / cm-1\n')
        for i in range(len(q_data)):
          f.write(f'{q_data[i]}\t{I_data[i]}\t{sI_data[i]}\n')
    elif hasattr(self, 'model'):
      for i in range(self.model.nModelsets):
        model = self.model.getModelset(i)
        q_model = model.getDomain()
        I_model = model.getValues()
        if isinstance(model.suffix, str):
          f.write(f'\n#[[Data]] {model.suffix}\n')
        elif isinstance(model.suffix, list):
          f.write('\n#[[Data]] '+'_'.join(model.suffix)+'\n')
        f.write('#q / A-1\tImodel / cm-1\n')
        for i in range(len(q_model)):
          f.write(f'{q_model[i]}\t{I_model[i]}\n')