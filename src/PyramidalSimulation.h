#ifndef PYRAMIDALSIMULATION_H
#define PYRAMIDALSIMULATION_H
#include <vector>

using namespace std;

class PyramidalSimulation{

 private:
  PyObject *pName, *pModule, *pDict, *pFunc, *pValue, *pClass, *pInstance;
  vector<float> unpackPythonList(PyObject*);

 public:
  int setup();
  vector<float> run();

};

#endif
