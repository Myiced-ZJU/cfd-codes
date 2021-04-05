#!/usr/bin/env python
# coding: utf-8

# tecplot .q to numpy.array to VTK
import tecplot
import numpy as np
from pyevtk.hl import gridToVTK
import numpy as np

tecplot.session.connect(host='localhost',port=7600,timeout=10,quiet=False)

dataset=tecplot.data.load_plot3d(
                                grid_filenames = 'mesh.x',
                                solution_filenames = ['0005.q'])

valuables_to_save = [dataset.variable(pressure)
                    for pressure in ('X','Y','Z',
                                    'RHO','RHO-U','RHO-V','RHO-W',
                                    'E')]


nmesh = dataset.zone('0000.q:1').values('X').shape
nx,ny,nz = nmesh[0],nmesh[1],nmesh[2]


# 提取.q中所有数据并转换成array
X0 = dataset.zone('0000.q:1').values('X')
Y0 = dataset.zone('0000.q:1').values('Y')
Z0 = dataset.zone('0000.q:1').values('Z')
RHO0 = dataset.zone('0000.q:1').values('RHO')
RHOU0 = dataset.zone('0000.q:1').values('RHO-U')
RHOV0 = dataset.zone('0000.q:1').values('RHO-V')
RHOW0 = dataset.zone('0000.q:1').values('RHO-W')
E0 = dataset.zone('0000.q:1').values('E')

X,Y,Z,RHO,RHO_U,RHO_V,RHO_W,E = X0[:],Y0[:],Z0[:],RHO0[:],RHOU0[:],RHOV0[:],RHOW0[:],E0[:]


# 根据已有数据格式重构三维数组
Xre = X.reshape(nz,ny,nx)
Yre = Y.reshape(nz,ny,nx)
Zre = Z.reshape(nz,ny,nx)
Ere = E.reshape(nz,ny,nx)
RHOre = RHO.reshape(nz,ny,nx)
RHO_Ure = RHO_U.reshape(nz,ny,nx)
RHO_Vre = RHO_V.reshape(nz,ny,nx)
RHO_Wre = RHO_W.reshape(nz,ny,nx)

Xre = Xre.transpose(2,1,0)
Yre = Yre.transpose(2,1,0)
Zre = Zre.transpose(2,1,0)
Ere = Ere.transpose(2,1,0)
RHOre = RHOre.transpose(2,1,0)
RHO_Ure = RHO_Ure.transpose(2,1,0)
RHO_Vre = RHO_Vre.transpose(2,1,0)
RHO_Wre = RHO_Wre.transpose(2,1,0)

# 提取x,y,z网格坐标
Xce,Yce,Zce = [],[],[]
for i in range(nx):
    Xce.append(Xre[i][0][0])
for i in range(ny):
    Yce.append(Yre[0][i][0])
for i in range(nz):
    Zce.append(Zre[0][0][i])
Xce = np.array(Xce)
Yce = np.array(Yce)
Zce = np.array(Zce)


# array 2 vtk
gridToVTK("./output",Xce,Yce,Zce,pointData={'E':Ere,'RHO':RHOre,'RHO_U':RHO_Ure,'RHO_V':RHO_Vre,'RHO_W':RHO_Wre,'Zre':Zre})

