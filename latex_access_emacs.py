#!/usr/bin/python

# latex_access_emacs.py
#    A part of the latex-access project at http://latex-access.sourceforge.net/
#    Author: Daniel Dalton <daniel.dalton10@gmail.com>
#    Copyright (C) 2011 Daniel Dalton/latex-access Contributors
#
#    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation;
#    either version 2 of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along with this program; if not, visit <http://www.gnu.org/licenses>
#
# A silly hack, so we don't need to worry about classes to access the
# translate functions.
# Used for communication via pyymacs from within emacs.
# Written by Daniel Dalton <daniel.dalton10@gmail.com>

"""Silly hack to access translate functions as pymacs was difficult to
interact with classes."""

import sys
import speech
import nemeth 
import preprocessor
import table
import motion

n=nemeth.nemeth()
s=speech.speech()
p=preprocessor.preprocessor()
nc=preprocessor.newcommands(p)
t=table
m=motion

if __name__ == "__main__":
  print "This is just a module."
  exit (-1)

def transbrl (arg):
  """Translate latex code into Nemeth Braile.

  Unless you are using pymacs to call this, please use the function
  nemeth.nemeth.translate() instead. Found in nemeth.py."""
  return n.translate(p.translate(arg))

def transsp (arg):
  """Translate a line of LaTeX source into understandable speech.

  Unless calling with pymacs, please use
  speech.speech.translate(). Found in speech.py."""

  return s.translate(p.translate(arg))

def toggle_dollars_nemeth ():
  """Toggle Brailling of dollar signs.

  This function negotiates the class, because pymacs is challenging to
  deal with."""
  n.remove_dollars=not n.remove_dollars
  return n.remove_dollars

def toggle_dollars_speech ():
  """Toggle the speaking of dollar signs.

  This functions is here to negotiate the class, so that pymacs isn't
  able to cause us trouble."""
  s.remove_dollars=not s.remove_dollars
  return s.remove_dollars
  



def preprocessor_add(command,args,translation_string):
  '''A function to add entries to the preprocessor'''
  p.add_from_string(command,args,translation_string)

def preprocessor_from_string(input):
  '''Adds preprocessor entries from a LaTeX string containing \newcommand.'''
  nc.translate(input)

def preprocessor_write(filename):
  p.write(filename)

def preprocessor_read(filename):
  p.read(filename)

# Export the table.* functions to emacs.
def BuildHeaderString (text):
  """Enable access to the BuildHeaderString function for table
  manipulation.

  Consult the documentation in table.py."""

  return t.BuildHeaderString (text)

def WhereAmI (row, headers,table):
  """Access to the WhereAmI function in table.py.

  This exports the WhereAmI function to emacs -- consult documentation
  in table.py for more details."""

  return t.WhereAmI (row, headers,table)

def GetTableTopRow (latextable):
  """Make the GetTopRow function available to emacs for table
  manipulation.

  Consult the documentation in table.py for details."""

  return t.GetTableTopRow (latextable)

def GetTableCurrentRow (latextable):
  """Get the current row of a table.

  Export this function to emacs so to allow for latex table
  accessibility."""

  return t.GetTableCurrentRow (latextable)

def NextTerm (line,cursor):
  """Move to the next term.

  For details see the function definition in motion.py"""

  return m.NextTerm(line,cursor)

def PreviousTerm (line, cursor):
  """Move to previous term on line.

  For details see the function definition in motion.py."""

  return m.PreviousTerm (line, cursor)

def SpeakSegment (text, start, end):
  """Speak a substring of a string of text.

  Consult the function definition in motion.py for details."""

  return m.SpeakSegment(text, start, end)

def BrailleDisplaySize ():
  """Return the size of a Braille display.

  Use Brlapi to figure out the size of the connected Braille display."""

  try:
    import brlapi
    b=brlapi.Connection() # Connect to the display.
    return int(b.displaySize[0]) # Return the number of cells of display.
  except:
    return -1 # Either brlapi not found or display not connected

def DetermineWindowSize (windowwidth, bdisplaywidth):
  """Determine how much the window should be shrunk or increased in
  width.

  A positive value is increase while a negative return value is shrink
  factor."""

  if bdisplaywidth == -1:
    return 0 # Brltty probably isn't running so don't bother

  leftover = windowwidth%bdisplaywidth # How many characters over the
# side of x*display width the source text spans
  minwidth = windowwidth-leftover # Minimum width we're happy to make
# window 
  maxwidth = minwidth+bdisplaywidth # Maximum width we can make window 
  mindiff = windowwidth-minwidth # Difference between window size and
# minimum width 
  maxdiff = maxwidth-windowwidth # Difference between window size and
# maximum width 

  if maxdiff < mindiff: # Which one are we closest too?
    return maxdiff # Increase the window size by maxdiff characters 
  else: # Shrink 
    return 0-mindiff # Shrink the window size by mindiff characters, is negative of course
