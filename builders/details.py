# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file decodes given data to create a brief overview of what
# the data structure's content represents - meaning of fields/values
# and significances based on the data structure.

from builders.constants import *


def slotContextDetails(data:list[int]) -> str:
  '''
  @brief This function describes the contents of the slotContext Data Structure
  @param data The list of bytes that make the data structure
  @returns A string containing description of the data structure
  '''
  
  # 1st row of the data structure
  routeString: list[int] = mapRouteString(data) # 20-bit
  speed = f"{bin((data[1]>>4) & 0x0F)[2:]}" # 4-bit
  # 1 bit is reserved 0
  multiTT = "High-speed hub with Multiple TT support enabled." if ((data[0] >> 1) & 0x01) else "Multiple TT not supported or not enabled" # 1 bit flag
  hub = "Device is a HUB" if ((data[0] >> 2) & 0x01) else "This is a USB Function" # 1-bit
  contextEntries = ((data[0] & 0xF8) >> 3 ) # 5-bit
  
  # 2d row
  maxExitLatency=((data[7]<<8) | data[6]) # 16-bit
  rootHubPortNumber=data[5] # 8-bit
  numberOfPorts= f"Device is a hub, supporting {data[4]} downstream ports" if (data[4] > 0) else "Device is not a hub. Not Applicable" # 8-bit
  
  # 3rd row
  parentHubSlotID = "Device is directly connected to root or is high-speed/top-level." if (data[11] == 0) else f"Device is connected through parent hub with Slot ID {data[11]}." # 8-bit
  parentPortNumber = "Device is directly connected to root or is high-speed/top-level." if (data[10] == 0) else f"Device is connected through downstream port {data[10]} of the parent hub." # 8-bit
  ttThinkTime = mapTTThinkTime(data[9] & 0x03) # 2-bit
  # 4-bit reserved 0
  interrupterTarget = (((data[9] & 0xFC) | (data[8] << 8 ) ) >> 2 ) # 10-bit
  
  # 4th row
  usbDeviceAddress = "Invalid" if ((data[12]& 0xF8) == 0) else hex(data[15]) # 8-bit
  # 19-bit reserved 0
  slotState = mapSlotState(data[12]& 0xF8)# 5-bit
  
  return f'''
    <table border="1" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
            <td> Route String </td>
            <td> {hex(routeString[0])} - {hex(routeString[1])} - {hex(routeString[2])} - {hex(routeString[3])} - {hex(routeString[4])} </td>
        </tr>
        <tr>
            <td> Targeted Downstream Port Number </td>
            <td> {hex(routeString[4])} </td>
        </tr>
        <tr>
            <td> Speed </td>
            <td> {speed} </td>
        </tr>
        <tr>
            <td> Multi-TT (Multiple Transaction Translator) </td>
            <td> {multiTT} </td>
        </tr>
        <tr>
            <td> Hub </td>
            <td> {hub} </td>
        </tr>
        <tr>
            <td> Context Entries - Number of active Endpoints </td>
            <td> {contextEntries}. Total Size {(contextEntries+1)*32} bytes. </td>
        </tr>
        <tr>
            <td> Max Exit Latency </td>
            <td> {maxExitLatency}µS </td>
        </tr>
        <tr>
            <td> Root Hub Port Number </td>
            <td> {rootHubPortNumber} </td>
        </tr>
        <tr>
            <td> Number of Ports </td>
            <td> {numberOfPorts} </td>
        </tr>
        <tr>
            <td> Parent Hub Slot ID </td>
            <td> {parentHubSlotID} </td>
        </tr>
        <tr>
            <td> Parent Port Number </td>
            <td> {parentPortNumber} </td>
        </tr>
        <tr>
            <td> TT Think Time (TTT) </td>
            <td> {ttThinkTime} </td>
        </tr>
        <tr>
            <td> Interrupter Target </td>
            <td> {interrupterTarget} </td>
        </tr>
        <tr>
            <td> USB Device Address </td>
            <td> {usbDeviceAddress} </td>
        </tr>
        <tr>
            <td> Slot State </td>
            <td> {slotState} </td>
        </tr>
    </table>
  '''

def endpointContextDetails(data:list[int]) ->str:
    '''This function describes info details of the endpoint from the endpoint context data'''
    
    # First, separate out the data
    
    # Row 1
    endpointState = mapEndpointState((data[3]&0x7))
    mult = f"LEC Depended. If LEC = 0, then Max Number of Bursts = {(data[2] & 0x3)+1}. Else, Reserved"
    maxPStreams = "Streams not supported or Endpoint Type is SS Control, Isoch, Interrupt, or not a SuperSpeed endpoint." if ((data[2] >> 2) & 0x3F) == 0 else f"Primary Stream Array Contains {2**(((data[2] >> 2) & 0x3F)+1)} entries. Width = {(((data[2] >> 2) & 0x3F)+1)}"
    linearStreamArray = "Reserved" if ((data[2] >> 2) & 0x3F) == 0 else "Stream ID = index into Primary Stream Array. Secondary Stream Arrays disabled. MaxPStreams: 1–15." if(data[1] & 0x01) == 1 else f"Stream ID split: low {(((data[2] >> 2) & 0x3F)+1)} → Primary, high bits → Secondary Stream Array. MaxPStreams: 1–7."
    interval = (data[1] >> 1) & 0x7F
    maxESITPayloadHi = data[0]
    
    # Row 2
    errorCount = "Unlimited retries; no bus error counting." if (((data[7]>>1)&0x3) == 0) else "Allow CErr failures before halting. On final error, endpoint halts and error event is generated."
    epType = mapEPType((data[7]>>3)&0x7)
    hostInitiateDisable = "Host-initiated Stream selection is disabled; device controls Stream transitions." if ((data[7]>>7)&0x01) == 1 else "Host-initiated Stream selection is enabled; normal Stream operation."
    maxBurstSize = data[6]+1
    maxPacketSize = data[5]+(data[4]<<8)
    
    # Row 3 & 4
    dcs = data[11]&0x01
    trDequeuePtr = hex((int.from_bytes(data[8:16],'little'))>>4)
    
    # Row 5
    avgTRBLength = data[19] + (data[18]<<8)
    maxESITPayloadLo = data[17]+ (data[16]<<8)
    
    # Then create and return useful data as a table
    return f"""
    <table border="1" cellborder="1" cellspacing="0" cellpadding="4">
        <tr>
            <td> Endpoint State </td>
            <td> {endpointState} </td>
        </tr>
        <tr>
            <td> Mult </td>
            <td> {mult} </td>
        </tr>
        <tr>
            <td> Max Primary Streams </td>
            <td> {maxPStreams} </td>
        </tr>
        <tr>
            <td> Linear Stream Array </td>
            <td> {linearStreamArray} </td>
        </tr>
        <tr>
            <td> Interval. </td>
            <td> {interval} </td>
        </tr>
        <tr>
            <td> Max Endpoint Service Time Interval Payload High </td>
            <td> {maxESITPayloadHi} </td>
        </tr>
        <tr>
            <td> Error Count </td>
            <td> {errorCount} </td>
        </tr>
        <tr>
            <td> Endpoint Type </td>
            <td> {epType} </td>
        </tr>
        <tr>
            <td> Host Initiate Disable </td>
            <td> {hostInitiateDisable} </td>
        </tr>
        <tr>
            <td> Max Burst Size </td>
            <td> {maxBurstSize} </td>
        </tr>
        <tr>
            <td> Max Packet Size </td>
            <td> {maxPacketSize} </td>
        </tr>
        <tr>
            <td> Dequeue Cycle State </td>
            <td> {dcs} </td>
        </tr>
        <tr>
            <td> TR Dequeue Pointer </td>
            <td> {trDequeuePtr} </td>
        </tr>
        <tr>
            <td> Average TRB Length </td>
            <td> {avgTRBLength} </td>
        </tr>
        <tr>
            <td> Max Endpoint Service Time Interval Payload Low </td>
            <td> {maxESITPayloadLo} </td>
        </tr>
        
    </table>

"""

