# Copyright 2007-2008 Nanorex, Inc.  See LICENSE file for details. 
"""
NanotubeSegment.py - ... 

@author: Bruce, Mark
@version: $Id$
@copyright: 2007-2008 Nanorex, Inc.  See LICENSE file for details.
"""
import foundation.env as env

from utilities.debug import print_compact_stack, print_compact_traceback
from model.chunk import Chunk
from model.chem import Atom
from model.bonds import Bond
from geometry.VQT import V, norm, vlen

from foundation.Group import Group

from utilities.icon_utilities import imagename_to_pixmap
from utilities.Comparison     import same_vals
from utilities.debug_prefs import debug_pref, Choice_boolean_False

class NanotubeSegment(Group):
    """
    Model object which represents a Nanotube Segment inside a Nanotube Group.

    Internally, this is just a specialized Group containing a single chunk,
    itself containing all the atoms of a nanotube.
    """

    # This should be a tuple of classifications that appear in
    # files_mmp._GROUP_CLASSIFICATIONS, most general first.
    # See comment in class Group for more info. [bruce 080115]
    _mmp_group_classifications = ('NanotubeSegment',)
    
    _nanotubeRise = None
    _endPoint1 = None
    _endPoint2 = None
        # TODO: undo or copy code for those attrs,
        # and updating them when the underlying structure changes.
        # But maybe that won't be needed, if they are replaced
        # by computing them from the atom geometry as needed.
        # [bruce 080227 comment]
        
    autodelete_when_empty = True
        # (but only if current command permits that for this class --
        #  see comment near Group.autodelete_when_empty for more info,
        #  and implems of Command.keep_empty_group)
        
    iconPath = "ui/modeltree/NanotubeSegment.png"
    hide_iconPath = "ui/modeltree/NanotubeSegment-hide.png"
    
    def __init__(self, name, assy, dad, members = (), editCommand = None):
        
        self._nanotubeRise = 3.18 #@      
        Group.__init__(self, 
                       name, 
                       assy, 
                       dad, 
                       members = members, 
                       editCommand = editCommand)
        ###BUG: not all callers pass an editCommand. It would be better
        # to figure out on demand which editCommand would be appropriate.
        # [bruce 080227 comment]
        return
        
    def edit(self):
        """
        Edit this NanotubeSegment. 
        @see: NanotubeSegment_EditCommand
        """
        
        commandSequencer = self.assy.w.commandSequencer       
        
        if commandSequencer.currentCommand.commandName != "NANOTUBE_SEGMENT":
            commandSequencer.userEnterTemporaryCommand('NANOTUBE_SEGMENT')
            
        assert commandSequencer.currentCommand.commandName == 'NANOTUBE_SEGMENT'
        commandSequencer.currentCommand.editStructure(self)
    

    #Following methods are likely to be revised in a fully functional dna data 
    # model. These methods are mainly created to get working many core UI 
    # operations for Rattlesnake.  -- Ninad 2008-02-01
    
    def get_all_content_chunks(self):
        """
        Return all the chunks contained within this NanotubeSegment.
        
        @note: there is only one chunk inside this group.
        """
        all_content_chunk_list = []
        
        for member in self.members:
            if isinstance(member, Chunk):
                all_content_chunk_list.append(member)
        
        return all_content_chunk_list 
    
    def getAxisVector(self):
        """
        Returns the unit axis vector of the segment (vector between two axis 
        end points)
        """
        endPoint1, endPoint2 = self.nanotube.getEndPoints()
        if endPoint1 is not None and endPoint2 is not None:
            return norm(endPoint2 - endPoint1)
        else:
            return V(0, 0, 0)
    
    def setProps(self, props):
        """
        Sets some properties. These will be used while editing the structure. 
        (but if the structure is read from an mmp file, this won't work. As a 
        fall back, it returns some constant values) 
        @see: InsertNanotube_EditCommand.createStructure which calls this method. 
        @see: self.getProps, NanotubeSegment_EditCommand.editStructure        
        """        
        _chirality, _type, _endings, _endPoints = props
        
        _n, _m = _chirality
        _endPoint1, _endPoint2 = _endPoints
        
        from cnt.model.Nanotube import Nanotube
        self.nanotube = Nanotube()
        self.nanotube.setChirality(_n, _m)
        self.nanotube.setType(_type)
        self.nanotube.setEndings(_endings)
        self.nanotube.setEndPoints(_endPoint1, _endPoint2)
        
    def getProps(self):
        """
        Returns nanotube parameters necessary for editing.
        
        @see: NanotubeSegment_EditCommand.editStructure where it is used. 
        @see: NanotubeSegment_PropertyManager.getParameters
        @see: NanotubeSegmentEditCommand._createStructure        
        """
        
        #@ BUG: nanotube does not exist if it wasn't created during the
        # current session (i.e. the nanotube was loaded from an MMP file).
        # Need to save/restore these params in the MMP file. --Mark 2008-04-01.
        props = (self.nanotube.getChirality(),
                 self.nanotube.getType(),
                 self.nanotube.getEndPoints())
        return props
    
    def getNanotubeGroup(self):
        """
        Return the NanotubeGroup we are contained in, or None if we're not
        inside one.
        """
        return self.parent_node_of_class( self.assy.NanotubeGroup)
        
    def isAncestorOf(self, obj):
        """
        Checks whether the object <obj> is contained within the NanotubeSegment
        
        Example: If the object is an Atom, it checks whether the 
        atom's chunk is a member of this NanotubeSegment (chunk.dad is self)
        
        It also considers all the logical contents of the NanotubeSegment to determine
        whether self is an ancestor. (returns True even for logical contents)
        
        @see: self.get_all_content_chunks()
        @see: NanotubeSegment_GraphicsMode.leftDrag
        """
        c = None
        if isinstance(obj, Atom):       
            c = obj.molecule                 
        elif isinstance(obj, Bond):
            chunk1 = obj.atom1.molecule
            chunk2 = obj.atom1.molecule            
            if chunk1 is chunk2:
                c = chunk1
        elif isinstance(obj, Chunk):
            c = obj
        
        if c is not None:
            if c in self.get_all_content_chunks():
                return True        
        
        #NOTE: Need to check if the isinstance checks are acceptable (apparently
        #don't add any import cycle) Also this method needs to be revised 
        #after we completely switch to dna data model. 
        if isinstance(obj, Atom):       
            chunk = obj.molecule                
            if chunk.dad is self:
                return True
            else:
                return False
        elif isinstance(obj, Bond):
            chunk1 = obj.atom1.molecule
            chunk2 = obj.atom1.molecule            
            if (chunk1.dad is self) or (chunk2.dad is self):
                return True               
        elif isinstance(obj, Chunk):
            if obj.dad is self:
                return True
        return False
    
    def node_icon(self, display_prefs):        
        del display_prefs # unused
        
        if self.all_content_is_hidden():    
            return imagename_to_pixmap( self.hide_iconPath)
        else:
            return imagename_to_pixmap( self.iconPath)
        
    # =======================================================================
    # These methods were copied from DnaStrandOrSegment and edited for 
    # this class.
    
    def permits_ungrouping(self): 
        """
        Should the user interface permit users to dissolve this Group
        using self.ungroup?
        [overridden from Group]
        """
        return self._show_all_kids_for_debug() # normally False
            # note: modelTree should modify menu text for Ungroup to say "(unsupported)",
            # but this is broken as of before 080318 since it uses a self.is_block() test.

    def _show_all_kids_for_debug(self):
         #bruce 080207 in deprecated class Block, copied to DnaStrandOrSegment 080318
        classname_short = self.__class__.__name__.split('.')[-1]
        debug_pref_name = "Model Tree: show content of %s?" % classname_short
            # typical examples (for text searches to find them here):
            # Model Tree: show content of DnaStrand?
            # Model Tree: show content of DnaSegment?
        return debug_pref( debug_pref_name, Choice_boolean_False )

    def permit_as_member(self, node, pre_updaters = True, **opts): # in DnaStrandOrSegment
        """
        [friend method for enforce_permitted_members_in_groups and subroutines]

        Does self permit node as a direct member,
        when called from enforce_permitted_members_in_groups with
        the same options as we are passed?

        @rtype: boolean

        [overrides Group method]
        """
        #bruce 080319
        # someday, reject if superclass would reject -- so far, it never does
        del opts
        assy = self.assy
        res = isinstance( node, assy.Chunk) #@ NEEDS SOMETHING MORE.
        return res
    
    def _f_wants_to_be_killed(self, pre_updaters = True, **opts): # in DnaStrandOrSegment
        """
        [friend method for enforce_permitted_members_in_groups and subroutines]
        
        Does self want to be killed due to members that got ejected
        by _f_move_nonpermitted_members (or due to completely invalid structure
        from before then, and no value in keeping self even temporarily)?

        @rtype: boolean

        [overrides Group method]   
        """
        #bruce 080319
        del opts, pre_updaters
        return not self.members

    def MT_DND_can_drop_inside(self): #bruce 080317, revised 080318
        """
        Are ModelTree Drag and Drop operations permitted to drop nodes
        inside self?

        [overrides Node/Group method]
        """
        return self._show_all_kids_for_debug() # normally False
    
    def openable(self): # overrides Node.openable()
        """
        whether tree widgets should permit the user to open/close their view of this node
        """
        # if we decide this depends on the tree widget or on somet for thing about it,
        # we'll have to pass in some args... don't do that unless/until we need to.

        #If there are no MT_kids (subnodes visible in MT under this group) then
        #don't make this node 'openable'. This makes sure that expand/ collapse
        #pixmap next to the node is not shown for this type of Group with 0 
        #MT_kids
        #Examples of such groups include empty groups, DnaStrand Groups,
        #DnaSegments etc -- Ninad 2008-03-15
        return len(self.MT_kids()) != 0
    
    def _raw_MT_kids(self, display_prefs = {}):
        """
        DnaStrand or DnaSegment groups (subclasses of this class) should not 
        show any MT kids.
        @see: Group._raw__MT_kids()
        @see: Group.MT_kids()
        """
        if self._show_all_kids_for_debug(): # normally False
            # bruce 080318
            return self.members
        return ()

    def move_into_your_members(self, node):
        """
        Move node into self's Group members, and if node was not
        already there but left some other existing Group,
        return that Group.
        
        @param node: a node of a suitable type for being our direct child
        @type node: a DnaLadderRailChunk or DnaMarker

        @return: Node's oldgroup (if we moved it out of a Group other than self)
                 or None
        @rtype: Group or None
        """
        oldgroup = node.dad # might be None
        self.addchild(node)
        newgroup = node.dad
        assert newgroup is self
        if oldgroup and oldgroup is not newgroup:
            if oldgroup.part is newgroup.part: #k guess
                return oldgroup
        return None
        
    pass # end of class NanotubeSegment
                
# end
