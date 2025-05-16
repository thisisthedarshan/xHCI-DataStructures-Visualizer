# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file decodes given data to create a brief overview of what
# the data structure's content represents - meaning of fields/values
# and significances based on the data structure.

from builders.constants import mapRouteString, mapSlotState, mapTTThinkTime


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
            <td> | {bin(routeString[4])[2:]} | {bin(routeString[3])[2:]} | {bin(routeString[2])[2:]} | {bin(routeString[1])[2:]} | {bin(routeString[0])[2:]} | </td>
        </tr>
        <tr>
            <td> Targeted Downstream Port Number </td>
            <td> {bin(routeString[0])[2:]} </td>
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
