# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains the core logic to process given data and 
# build the final output.

from graphviz import Digraph
from builders.constants import VisualizationException, createInfoTable, supportedStructures
from builders.content import *
from builders.details import *


#########################################################################################
# The following functions contain builders for individual data structures
#########################################################################################
def buildSlotContext(byteData:list[int]) -> str:
  '''
  This function builds visualization for slot context data structure
  '''
  # Check if data is properly available
  if len(byteData) < 16:
    raise VisualizationException(f"Expecting at-least 16 bytes of data. Got {len(byteData)} bytes")
  
  # Get base data
  slotDiagram = slotContext(byteData)
  slotDescription = slotContextDetails(byteData)
  
  return createInfoTable("Slot Context",slotDiagram, slotDescription)

def buildEndpointContext(byteData:list[int], endpointType:str = "") -> str:
  '''
  This function takes in raw bytes, decodes it and creates a visualization of 
  endpoint context data structure. Endpoint number = -1 indicates that we don't know which
  endpoint this data belongs to!
  '''
  
  if len(byteData) < 20: # 4 bytes per row *5 rows since remaining are 0
    raise VisualizationException(f"Expecting at-least 16 bytes of data. Got {len(byteData)} bytes")

  # Get the content
  endpointDiagram = endpointContext(byteData)
  endpointDescription = endpointContextDetails(byteData)
  
  return createInfoTable(f"Endpoint {endpointType}Context",endpointDiagram, endpointDescription)


def buildInputControlContext(byteData:list[int]) -> str:
  '''
  This function takes in raw bytes, decodes it and creates a visualization of 
  input control context data structure.
  '''
  
  if len(byteData) < 32:
    raise VisualizationException(f"Expecting 32 bytes of data. Got {len(byteData)} bytes")

  # Get the content
  inputCtrlCtxData = inputControlContextContext(byteData)
  inputCtrlCtxDataDescription = inputControlContextContextDetails(byteData)
  
  return createInfoTable(f"Input Control Context",inputCtrlCtxData, inputCtrlCtxDataDescription)


#########################################################################################
# The following functions contain logic for building chained/grouped data structures 
# containing more than 1 data structure
#########################################################################################

def buildDeviceContext(byteData:list[int], name:str="head", names:list[str]=[]) -> dict[str,str]:
  '''
  This function takes in raw data, processes it and builds a complex visualization of the 
  device context data structure.
  '''
  
  # Ensure that there are at-least 1024 elements in the byte array.
  # This is because Slot Context takes 32 bytes
  # Endpoint contexts take (32 endpoints) * 32 bytes each = 992
  if len(byteData) < 1024:
    raise VisualizationException(f"Device Context expects al-least 1024 bytes as input. Got {len(byteData)} bytes instead")
  
  # Create a list of dict to be returned
  deviceContextDS:dict[str,str] = {}
  
  # First split into slot data segment and endpoints data segment
  slotSegment:list[int] = byteData[:32] # 4 bytes per row * 8 rows
  endpointSegments:list[int] = byteData[32:] # Remaining Bytes will be for endpoint context
  
  # Build Slot Context
  slotContext = buildSlotContext(slotSegment)
  
  names.append(name)
  
  deviceContextDS[names[-1]] = slotContext
  
  # Build The Endpoint Contexts
  for endpointNumber in range(31):
    if endpointNumber == 0:
      # This is a bi-directional endpoint
      endpointType = "0 - Bi-Directional "
    else:
      endpointType = f"{(endpointNumber//2)+(endpointNumber % 2)} {"- OUT" if endpointNumber % 2 == 1 else "- IN"} "
    
    name = f"Endpoint Context {endpointType}"
    names.append(name)
    endpointSegment = endpointSegments[(endpointNumber*32) : (endpointNumber+1)*32]
    deviceContextDS[names[-1]] = buildEndpointContext(endpointSegment,endpointType)

  return deviceContextDS

def buildInputContext(byteData:list[int], name:str="head", names:list[str] = []) -> Digraph:
  '''
  This function takes in raw bytes and builds input context data structure.
  Input Context Data Structure is nothing but a combination if Input Control Context
  and the Device Context Data Structures.
  '''

  # Ensure that teh input byte list is of at-least 1056 bytes
  # This is because
  # Input Control Context = 32 bytes
  # Slot Context = 32 bytes
  # Endpoint Contexts = 992 bytes (32 endpoints * 32 bytes each)
  
  if len(byteData) < 1056:
    raise VisualizationException(f"Input Context Expects at-least 1056 bytes of data. Currently, we have {len(byteData)} bytes of data")
  
  # Safe to continue
  
  ds:dict[str, str] = {} # This dictionary holds our Data Structures

  # Separate data for input control context and device context
  inputControlCtxData = byteData[:32]
  deviceCtxData = byteData[32:]
  
  # First build Input Control Context Data Structure
  inputCtrlCtx = buildInputControlContext(inputControlCtxData)
  
  # Put data into dictionary
  ds[name] = inputCtrlCtx
  names.append(name)
  
  # Build Device Context Data
  deviceCtx = buildDeviceContext(deviceCtxData, "Slot Context", names)

  # Merge both
  ds.update(deviceCtx)

  return ds

#########################################################################################
# The following functions contain logic to decode inputs and call appropriate builders
#########################################################################################

def createStandaloneDS(byteData:list[int], struct:str, names:list[str] = []) -> Digraph:
  '''
  This function helps visualize individual data structures instead of
  grouped data structures
  '''
  content = ""
  match (struct.strip().lower()):
    case "slotctx":
      content =  buildSlotContext(byteData)
    case "endpctx":
      content =  buildEndpointContext(byteData)
    case "icctx":
      content = buildInputControlContext(byteData)
    case _:
      raise VisualizationException(f"Invalid Data Structure codename {struct}")

  # Create a Digraph and add this standalone data structure
  dot = Digraph()
  dot.clear()
  
  names.append("head")
  dot.node(names[-1], content, shape='none')
  return dot

def processAndBuildData(struct:str, byteData:list[int], names:list[str]=[]) -> Digraph:
  '''
  This function is responsible for processing input and selecting data structure
  to create the final visuals. The function can process individual data structures
  like Slot Context, Endpoint Context, TRB etc. Or complex/combined data structures
  like Device Context Data Structure, Input Context Data Structure etc.
  '''
  
  result:dict[str,str] = {}
      
  match struct:
    case "devctx":
      result = buildDeviceContext(byteData, names=names)
    case "ipctx":
      result = buildInputContext(byteData, names=names)
    case _:
        # Creates standalone data structures and directly return them
        return createStandaloneDS(byteData, struct, names)
      
  dot = Digraph()
  dot.clear()
  
  # Build all nodes
  for name, content in result.items():
    # Create nodes
    dot.node(name, content, shape='none')
  
  # Connect them
  names = list(result.keys())
  for i in range(len(names)-1):
    # Connect them
    dot.edge(names[i], names[i+1])

  return dot
