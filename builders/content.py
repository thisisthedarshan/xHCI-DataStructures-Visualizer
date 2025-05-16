# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains the Graphviz code templates to create tables for a given
# xHCI Data Structure. It also contains data that is used to build info for that
# Data-structure.

from builders.constants import RsvdZ, mapRouteString
from helpers import bytes2binList


def slotContext(data:list[int]):
  '''This function dumps data from input to a table form, representing'''
  
  # Convert Data to integer list
  rawBinData = bytes2binList(data)
  
  # Now split them according to rows and reverse-order them
  row1 = rawBinData[0][::-1]
  row2 = rawBinData[1][::-1]
  row3 = rawBinData[2][::-1]
  row4 = rawBinData[3][::-1]
  # Create a reserved segment
  reservedSegment32 = RsvdZ(32)
  
  # Build the table
  return f"""
<table border="1" cellborder="1" cellspacing="0" cellpadding="4">
    <!-- Row 0: Bits -->
    <tr>
        {''.join(f'<td colspan="4"><b>{format(i,"02")}</b></td>\n' for i in reversed(range(32)))}
    </tr>
    <!-- Row 1: Context Entries to Route String -->
    <tr>
        <td colspan="20"><b>Context Entries</b></td>
        <td colspan="4"><b>Hub</b></td>
        <td colspan="4"><b>MTT</b></td>
        <td colspan="4"><b>RsvdZ</b></td>
        <td colspan="16"><b>Speed</b></td>
        <td colspan="80"><b>Route String</b></td>
        <td><b>03-00H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row1)}
        <td>—</td>
    </tr>
    <!-- Row 2: Number of Ports & Root Hub Port -->
    <tr>
        <td colspan="32"><b>Number of Ports</b></td>
        <td colspan="32"><b>Root Hub Port Number</b></td>
        <td colspan="64"><b>Max Exit Latency</b></td>
        <td><b>07-04H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row2)}
        <td>—</td>
    </tr>
    <!-- Row 3: Interrupter Target to TT Hub Slot ID -->
    <tr>
        <td colspan="40"><b>Interrupter Target</b></td>
        <td colspan="16"><b>RsvdZ</b></td>
        <td colspan="8"><b>TTT</b></td>
        <td colspan="32"><b>TT Port Number</b></td>
        <td colspan="32"><b>TT Hub Slot ID</b></td>
        <td ><b>0B-08H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row3)}
        <td>—</td>
    </tr>
    <!-- Row 4: Slot State and USB Device Address -->
    <tr>
        <td colspan="20"><b>Slot State</b></td>
        <td colspan="76"><b>RsvdZ</b></td>
        <td colspan="32"><b>USB Device Address</b></td>
        <td><b>0F-0CH</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row4)}
        <td>—</td>
    </tr>
    <!-- Reserved rows -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>13-10H</b></td>
    </tr>
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>17-14H</b></td>
    </tr>
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1B-18H</b></td>
    </tr>
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1F-1CH</b></td>
    </tr>
</table>
"""
