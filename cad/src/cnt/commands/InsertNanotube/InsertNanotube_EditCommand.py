# Copyright 2007-2008 Nanorex, Inc.  See LICENSE file for details. 
"""
InsertNanotube_EditCommand.py provides an editCommand object for 
generating a nanotube (CNT or BNNT).  This command should be invoked only from 
NanotubeProperties_EditCommand

@author: Mark Sims, Ninad Sathaye
@version: $Id$
@copyright: 2007-2008 Nanorex, Inc.  See LICENSE file for details.

History:
- Mark 2008-03-8: This file created from a copy of InsertDna_EditCommand.py
and edited.
"""
import foundation.env as env

from command_support.EditCommand import EditCommand
from cnt.model.NanotubeSegment import NanotubeSegment
from utilities.Log  import greenmsg
from geometry.VQT import V, vlen

from utilities.exception_classes import PluginBug, UserError
from cnt.commands.InsertNanotube.InsertNanotube_PropertyManager import InsertNanotube_PropertyManager

from utilities.constants import gensym

from cnt.temporary_commands.NanotubeLineMode import NanotubeLine_GM

from utilities.prefs_constants import insertNanotubeEditCommand_cursorTextCheckBox_angle_prefs_key
from utilities.prefs_constants import insertNanotubeEditCommand_cursorTextCheckBox_length_prefs_key
from utilities.prefs_constants import insertNanotubeEditCommand_showCursorTextCheckBox_prefs_key
from utilities.prefs_constants import cursorTextColor_prefs_key

_superclass = EditCommand
class InsertNanotube_EditCommand(EditCommand):
    """
    InsertNanotube_EditCommand that provides an editCommand object for 
    generating carbon or boron nitride nanotube. 

    This command should be invoked only from InsertNanotube_EditCommand 

    User can create as many nanotubes as he/she needs just by specifying 
    two end points for each nanotube. This uses NanotubeLineMode_GM  class as its
    GraphicsMode 
    """
        
    #Graphics Mode set to CntLine graphics mode
    GraphicsMode_class = NanotubeLine_GM
    
    #Property Manager
    PM_class = InsertNanotube_PropertyManager
    
    
    cmd              =  greenmsg("Insert Nanotube: ")
    prefix           =  'Nanotube'   # used for gensym
    cmdname          = "Insert Nanotube"

    commandName      = 'INSERT_NANOTUBE'
    featurename      = "Insert Nanotube"
    from utilities.constants import CL_SUBCOMMAND
    command_level = CL_SUBCOMMAND
    command_parent = 'BUILD_NANOTUBE'

    command_should_resume_prevMode = True
    command_has_its_own_PM = True
    # Generators for DNA, nanotubes and graphene have their MT name 
    # generated (in GeneratorBaseClass) from the prefix.
    create_name_from_prefix  =  True 

    
    #required by NanotubeLine_GM
    mouseClickPoints = []

    #This is set to InsertNanotube_EditCommand.flyoutToolbar (as of 2008-01-14, 
    #it only uses 
    flyoutToolbar = None

    def __init__(self, commandSequencer):
        """
        Constructor for InsertNanotube_EditCommand
        """

        _superclass.__init__(self, commandSequencer)        

        #Maintain a list of segments created while this command was running. 
        self._segmentList = []       
        
    def command_entered(self):
        """
        Overrides superclass method. 
        @see: basecommand.command_entered() for documentation. 
        """
        _superclass.command_entered(self)
        if isinstance(self.graphicsMode, NanotubeLine_GM):
            self._setParamsForCntLineGraphicsMode()
            self.mouseClickPoints = []
    
        #Clear the segmentList as it may still be maintaining a list of segments
        #from the previous run of the command. 
        self._segmentList = []    
        
    def command_will_exit(self):
        """
        Overrides superclass method. 
        @see: basecommand.command_will_exit() for documentation. 
        """
        if isinstance(self.graphicsMode, NanotubeLine_GM):
            self.mouseClickPoints = []
        self.graphicsMode.resetVariables()   
        self._segmentList = []  
        
        _superclass.command_will_exit(self)
        
    def _getFlyoutToolBarActionAndParentCommand(self):
        """
        See superclass for documentation.
        @see: self.command_update_flyout()
        """
        flyoutActionToCheck = 'insertNanotubeAction'
        parentCommandName = None      
        return flyoutActionToCheck, parentCommandName
        
    
    def runCommand(self):
        """
        Overrides EditCommand.runCommand
        """
        self.struct = None
        return

    def createStructure(self):
        """
        Overrides superclass method. Creates the structure (NanotubeSegment) 

        """        
        assert self.propMgr is not None

        if self.struct is not None:
            self.struct = None

        self.win.assy.part.ensure_toplevel_group()
        self.propMgr.endPoint1 = self.mouseClickPoints[0]
        self.propMgr.endPoint2 = self.mouseClickPoints[1]
        ntLength = vlen(self.mouseClickPoints[0] - self.mouseClickPoints[1])

        self.preview_or_finalize_structure(previewing = True)

        #Now append this ntSegment  to self._segmentList 
        self._segmentList.append(self.struct)

        #clear the mouseClickPoints list
        self.mouseClickPoints = [] 
        self.graphicsMode.resetVariables()
        return
    
    def _getStructureType(self):
        """
        Subclasses override this method to define their own structure type. 
        Returns the type of the structure this editCommand supports. 
        This is used in isinstance test. 
        @see: EditCommand._getStructureType() (overridden here)
        """
        return self.win.assy.NanotubeSegment

    def _finalizeStructure(self):
        """
        Finalize the structure. This is a step just before calling Done method.
        to exit out of this command. Subclasses may overide this method
        @see: EditCommand_PM.ok_btn_clicked
        @see: EditNanotube_EditCommand where this method is overridden. 
        """
        #The following can happen in this case: User creates first nanotube, 
        #Now clicks inside 3D workspace to define the first point of the 
        #next nanotube. Now moves the mouse to draw cnt rubberband line. 
        #and then its 'Done' When it does that, it has modified the 
        #'number of base pairs' value in the PM and then it uses that value 
        #to modify self.struct ...which is the first segment user created!
        #In order to avoid this, either self.struct should be set to None after
        #its appended to the segment list (in self.createStructure) 
        #Or it should compute the number of base pairs each time instead of 
        #relying on the corresponding value in the PM. The latter is not 
        #advisable if we support modifying the number of base pairs from the 
        #PM (and hitting preview) while in InsertNanotube command. 
        #In the mean time, I think this solution will always work. 
        if len(self.mouseClickPoints) == 1:
            return
        else:
            _superclass._finalizeStructure(self)
        return

    def _gatherParameters(self):
        """
        Return the parameters from the property manager UI.

        @return: The nanotube, which contains all the attrs.
        @rtype:  Nanotube
        """        

        return self.propMgr.getParameters()       

    def _modifyStructure(self, params):
        """
        Modify the structure based on the parameters specified. 
        Overrides EditCommand._modifystructure. This method removes the old 
        structure and creates a new one using self._createStructure. This 
        was needed for the structures like this (Cnt, Nanotube etc) . .
        See more comments in the method.
        @see: a note in self._createStructure() about use of ntSegment.setProps 
        """    
        #@NOTE: Unlike editcommands such as Plane_EditCommand, this 
        #editCommand actually removes the structure and creates a new one 
        #when its modified. We don't yet know if the CNT object model 
        # will solve this problem. (i.e. reusing the object and just modifying
        #its attributes.  Till that time, we'll continue to use 
        #what the old GeneratorBaseClass use to do ..i.e. remove the item and 
        # create a new one  -- Ninad 2007-10-24

        self._removeStructure()

        self.previousParams = params

        self.struct = self._createStructure()
        return 

    def cancelStructure(self):
        """
        Overrides Editcommand.cancelStructure ..calls _removeSegments which 
        deletes all the segments created while this command was running
        @see: B{EditCommand.cancelStructure}
        """
        _superclass.cancelStructure(self)
        self._removeSegments()
        return

    def _removeSegments(self):
        """
        Remove the segments created while in this command 

        This deletes all the segments created while this command was running
        @see: L{self.cancelStructure}
        """
        segmentList = self._segmentList  #@@@ rename segmentList to nanotubeSegmentList

        for segment in segmentList: 
            #can segment be None?  Lets add this condition to be on the safer 
            #side.
            if segment is not None: 
                segment.kill_with_contents()
            self._revertNumber()


        self._segmentList = []	
        self.win.win_update()

    def _createStructure(self):
        """
        Creates and returns the structure (in this case a L{Group} object that 
        contains the nanotube chunk. 
        @return : group containing the nanotube chunk.
        @rtype: L{Group}  
        @note: This needs to return a CNT object once that model is implemented        
        """

        # self.name needed for done message
        if self.create_name_from_prefix:
            # create a new name
            name = self.name = gensym(self.prefix, self.win.assy) # (in _build_struct)
            self._gensym_data_for_reusing_name = (self.prefix, name)
        else:
            # use externally created name
            self._gensym_data_for_reusing_name = None
                # (can't reuse name in this case -- not sure what prefix it was
                #  made with)
            name = self.name

        # Create the model tree group node. 
        # Make sure that the 'topnode'  of this part is a Group (under which the
        # Nanotube group will be placed), if the topnode is not a group, make it
        # a 'Group' (applicable to Clipboard parts). See part.py
        # --Part.ensure_toplevel_group method. This is an important line
        # and it fixes bug 2585
        self.win.assy.part.ensure_toplevel_group()

        ntSegment = NanotubeSegment(self.name, 
                                    self.win.assy,
                                    self.win.assy.part.topnode,
                                    editCommand = self)
        try:
            # Make the nanotube. <ntGroup> will contain one chunk:
            #  - Axis (Segment)
            # No error checking here; do all error checking in _gatherParameters().
            nanotube = self._gatherParameters()
            position = V(0.0, 0.0, 0.0)
            self.nanotube  =  nanotube  # needed for done msg #@
            ntChunk = nanotube.build(self.name, self.win.assy, position)

            ntSegment.addchild(ntChunk)

            #set some properties such as ntRise and its two endpoints.
            #This information will be stored on the NanotubeSegment object so that
            #it can be retrieved while editing this object. 

            #WARNING 2008-03-05: Since self._modifyStructure calls 
            #self._createStructure() If in the near future, we actually permit 
            #modifying a
            #structure (such as a nanotube) without actually recreating the  
            #entire structure, then the following properties must be set in 
            #self._modifyStructure as well. Needs more thought.
            #props =(nanotube.getChirality(),
            #        nanotube.getType(),
            #        nanotube.getEndings(),
            #        nanotube.getEndPoints())

            ntSegment.setProps(nanotube.getParameters())

            return ntSegment

        except (PluginBug, UserError):
            # Why do we need UserError here? Mark 2007-08-28
            self._segmentList.remove(ntSegment)
            ntSegment.kill_with_contents()
            raise PluginBug("Internal error while trying to create Nanotube.")

    def getCursorText(self, endPoint1, endPoint2):
        """
        This is used as a callback method in CntLine mode 
        @see: NanotubeLineMode.setParams, NanotubeLineMode_GM.Draw
        """
        
        text = ""
        textColor = env.prefs[cursorTextColor_prefs_key] # Mark 2008-08-28
        
        if endPoint1 is None or endPoint2 is None:
            return text, textColor
        
        if not env.prefs[insertNanotubeEditCommand_showCursorTextCheckBox_prefs_key]:
            return text, textColor

        vec = endPoint2 - endPoint1
        ntLength = vlen(vec)
        
        lengthString = self._getCursorText_length(ntLength)
        
        thetaString = ''
        if env.prefs[insertNanotubeEditCommand_cursorTextCheckBox_angle_prefs_key]:
            theta = self.glpane.get_angle_made_with_screen_right(vec)
            thetaString = '%5.2f deg'%theta
            
            
        commaString = ", "
        
        text = lengthString

        if text and thetaString:
            text += commaString

        text += thetaString
        
        return text , textColor
    
    def _getCursorText_length(self, nanotubeLength):
        """
        Returns a string that gives the length of the Nanotube for the cursor 
        text
        """
        nanotubeLengthString = ''
        if env.prefs[insertNanotubeEditCommand_cursorTextCheckBox_length_prefs_key]:
            lengthUnitString = 'A'
            #change the unit of length to nanometers if the length is > 10A
            #fixes part of bug 2856
            if nanotubeLength > 10.0:
                lengthUnitString = 'nm'
                nanotubeLength = nanotubeLength * 0.1
            nanotubeLengthString = "%5.3f%s"%(nanotubeLength, lengthUnitString)
        
        return nanotubeLengthString

    def isRubberbandLineSnapEnabled(self):
        """
        This returns True or False based on the checkbox state in the PM.

        This is used as a callback method in CntLine mode (NanotubeLine_GM)
        @see: NanotubeLine_GM.snapLineEndPoint where the boolean value returned from
              this method is used
        @return: Checked state of the linesnapCheckBox in the PM
        @rtype: boolean
        """
        return self.propMgr.lineSnapCheckBox.isChecked()

    def getDisplayStyleForNtRubberbandLine(self):
        """
        This is used as a callback method in ntLine mode. 
        @return: The current display style for the rubberband line. 
        @rtype: string
        @see: NanotubeLineMode.setParams, NanotubeLineMode_GM.Draw
        """
        return self.propMgr.ntRubberBandLineDisplayComboBox.currentText()

    # Things needed for CntLine_GraphicsMode (NanotubeLine_GM) ======================

    def _setParamsForCntLineGraphicsMode(self):
        """
        Needed for CntLine_GraphicsMode (NanotubeLine_GM). The method names need to
        be revised (e.g. callback_xxx. The prefix callback_ was for the earlier 
        implementation of CntLine mode where it just used to supply some 
        parameters to the previous mode using the callbacks from the 
        previousmode. 
        """
        self.mouseClickLimit = None
        self.nanotube = self.propMgr.nanotube
        self.ntType = self.nanotube.getType()
        self.n, self.m = self.nanotube.getChirality()
        self.ntRise = self.nanotube.getRise()
        self.ntDiameter = self.nanotube.getDiameter()

        self.jigList = self.win.assy.getSelectedJigs()

        self.callbackMethodForCursorTextString = \
            self.getCursorText

        self.callbackForSnapEnabled = self.isRubberbandLineSnapEnabled

        self.callback_rubberbandLineDisplay = \
            self.getDisplayStyleForNtRubberbandLine
