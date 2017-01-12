
import rhinoscriptsyntax as rs
import sys
import math
import string
import random
import time
import datetime
import os
import scriptcontext
import Rhino
import urllib, json
import calendar
from System.Drawing import Color

sys.path.append(os.path.abspath("C:\Users\Adam\Documents\maya_project_modelling_mdx"))


from ddd import da


all = rs.AllObjects(select=True)
rs.DeleteObjects(all)

pi = math.pi
data_points = []

def prepare_data():
    newDataArray = []
    temp_a =[]
    hh = 0
    dataArray = da
    
    for el in dataArray:
        if el > 80:
            el = 80
        el = el*0.13
        el = int(round(el))
        if el < 0:
            el = 0
            newDataArray.append(el)
        else:
            newDataArray.append(el)

    chunks = [newDataArray[x:x+1400] for x in range(0, len(newDataArray), 240)]

    return (chunks[0])

def precise_range(start, stop, step):
    assert step > 0.0
    total = start
    compo = 0.0
    while total < stop:
        yield total
        y = step - compo
        temp = total + y
        compo = (temp - total) - y
        total = temp


spheres = []
curves = []

def fun(rad, inp):
    pos = 0
    p = 0
    inc = 0.175
    z = 12
    
    a = (round((20*pi), 4))
    b = (round((pi/70), 4))
    
    for a in rs.frange(0.0, a, b):
        if (len(spheres)) < 65:
            inc = 0.055
        elif (len(spheres)) > 1250:
            inc = 0.03
        else:
            inc = 0.175
            
        x = rad * math.sin(a + pi)
        y = rad * math.cos(a + pi)
        
        data_points.append([x, y, z])
        
        h = (inp[pos] * 0.26)
        x = (rad -h)* math.sin(a + pi)
        y = (rad - h)* math.cos(a + pi)

        
        point = rs.AddPoint(x, y, z)
        sphere = rs.AddSphere(point, inp[pos])
        rs.HideObject(point)
        
        if sphere != None:
             spheres.append(sphere)
             rs.SelectObject(sphere)
             
        pos += 1
        z += inc
    
    return ""

print (len(spheres))

curves_list = []
def make_curves(z):
    pos = 0
    rad = 60
    daq = []
    #a = (round((20*pi), 4))
    #b = (round((pi/70), 4))

    for a in rs.frange(0.0, (2*pi), (pi/12)):
        x = rad * math.sin(a + pi)
        y = rad * math.cos(a + pi)
        
        daq.append([x, y, z])
 
        point = rs.AddPoint(x, y, z)

        rs.HideObject(point)
             
        pos += 1
               
    curve = rs.AddInterpCurve(daq, degree=3, knotstyle=4)
    
    curves_list.append(curve)
    daq = []

    return ""


make_curves(0)
make_curves(257)

base_point = (0,0,0)

base_extr = rs.ExtrudeCurvePoint(curves_list[0], base_point)

top_point = (0,0, 257)
top_extr = rs.ExtrudeCurvePoint(curves_list[1], top_point)

data = prepare_data()

rs.EnableRedraw(True)
fun(60, data)

rs.HideObject(curves)
rs.HideObject(curves_list)

spheres.append(rs.AddLoftSrf(curves_list, loft_type=0))

rs.BooleanUnion(spheres)

ready_model = rs.AllObjects(select=True)

#rs.Command('_CreateSolid')


'''

##############------------EXPORTING-------------######################


objs = ready_model


def layerNames(sort=False):
    rc = []
    for layer in scriptcontext.doc.Layers:
        if not layer.IsDeleted: rc.append(layer.FullPath)
    if sort: rc.sort()
    return rc

def GetDAESettings():
    e_str = ""
    return e_str

def GetOBJSettings():
    e_str = "_Geometry=_Mesh "
    e_str+= "_EndOfLine=CRLF "
    e_str+= "_ExportRhinoObjectNames=_ExportObjectsAsOBJGroups "
    e_str+= "_ExportMeshTextureCoordinates=_Yes "
    e_str+= "_ExportMeshVertexNormals=_No "
    e_str+= "_CreateNGons=_No "
    e_str+= "_ExportMaterialDefinitions=_No "
    e_str+= "_YUp=_No "
    e_str+= "_WrapLongLines=Yes "
    e_str+= "_VertexWelding=_Welded "
    e_str+= "_WritePrecision=4 "
    e_str+= "_Enter "

    e_str+= "_DetailedOptions "
    e_str+= "_JaggedSeams=_No "
    e_str+= "_PackTextures=_No "
    e_str+= "_Refine=_Yes "
    e_str+= "_SimplePlane=_No "

    e_str+= "_AdvancedOptions "
    e_str+= "_Angle=50 "
    e_str+= "_AspectRatio=0 "
    e_str+= "_Distance=0.0"
    e_str+= "_Density=0 "
    e_str+= "_Density=0.45 "
    e_str+= "_Grid=0 "
    e_str+= "_MaxEdgeLength=0 "
    e_str+= "_MinEdgeLength=0.001 "

    e_str+= "_Enter _Enter"

    return e_str

def GetSTLSettings():
    eStr = "_ExportFileAs=_Binary "
    eStr+= "_ExportUnfinishedObjects=_Yes "
    eStr+= "_UseSimpleDialog=_No "
    eStr+= "_UseSimpleParameters=_No "
    eStr+= "_Enter _DetailedOptions "
    eStr+= "_JaggedSeams=_No "
    eStr+= "_PackTextures=_No "
    eStr+= "_Refine=_Yes "
    eStr+= "_SimplePlane=_No "
    eStr+= "_AdvancedOptions "
    eStr+= "_Angle=15 "
    eStr+= "_AspectRatio=0 "
    eStr+= "_Distance=1 "
    eStr+= "_Grid=16 "
    eStr+= "_MaxEdgeLength=0 "
    eStr+= "_MinEdgeLength=0.1 "
    eStr+= "_Enter _Enter"
    return eStr

settingsList = {
    'GetDAESettings': GetDAESettings,
    'GetOBJSettings': GetOBJSettings,
    'GetSTLSettings': GetSTLSettings
}

fileName = rs.DocumentName()
filePath = rs.DocumentPath().rstrip(fileName)

arrLayers = layerNames(False)

def initExportByLayer(fileType="obj", visibleonly=False, byObject=False):
    for layerName in arrLayers:
        layer = scriptcontext.doc.Layers.FindByFullPath(layerName, True)
        if layer >= 0:
            layer = scriptcontext.doc.Layers[layer]
            save = True;
            if visibleonly:
                if not layer.IsVisible:
                    save = False
            if  rs.IsLayerEmpty(layerName):
                save = False
            if save:
                cutName = layerName.split("::")
                cutName = cutName[len(cutName)-1]
                objs = scriptcontext.doc.Objects.FindByLayer(cutName)
                if len(objs) > 0:
                    if byObject:
                        i=0
                        for obj in objs:
                            i= i+1
                            saveObjectsToFile(cutName+"_"+str(i), [obj], fileType)
                    else:
                        saveObjectsToFile(cutName, objs, fileType)

def saveObjectsToFile(name, objs, fileType):
    rs.EnableRedraw(False)
    if len(objs) > 0:
        settings = settingsList["Get"+fileType.upper()+"Settings"]()
        rs.UnselectAllObjects()
        for obj in objs:
            obj.Select(True)
        name = "".join(name.split(" "))
        command = '-_Export "{}{}{}" {}'.format(filePath, name, "."+fileType.lower(), settings)
        rs.Command(command, True)
        rs.EnableRedraw(True)



initExportByLayer("obj",True, False)
#initExportByLayer("dae",True, False)
initExportByLayer("stl",True, False)

#Animation()

rs.DocumentModified(False)
#rs.Exit()

'''