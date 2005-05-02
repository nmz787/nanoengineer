# Copyright (c) 2004-2005 Nanorex, Inc.  All rights reserved.

""" chem.py -- classes for atoms, bonds.

[elements.py was split out of this module on 041221]
[class molecule, for chunks, was moved into chunk.py circa 041118.]

$Id$
"""
__author__ = "Josh"

from VQT import *
from LinearAlgebra import *
import string
import re
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from drawer import *
from shape import *

from constants import *
from qt import *
from Utility import *
from MoleculeProp import *
from mdldata import marks, links, filler
from povheader import povpoint #bruce 050413

from debug import print_compact_stack, print_compact_traceback, compact_stack

import platform # for atom_debug; note that uses of atom_debug should all grab it
  # from platform.atom_debug since it can be changed at runtime

from elements import *

## no, better to use it directly so changeable at runtime:
## debug_bonds = platform.atom_debug #####@@@@@ DO NOT COMMIT with 1

# from chunk import * -- done at end of file,
# until other code that now imports its symbols from this module
# has been updated to import from chunk directly.
# [-- bruce 041110, upon moving class molecule from this file into chunk.py]


# ==

CPKvdW = 0.25

Gno = 0
def gensym(string):
    # warning, there is also a function like this in jigs.py
    # but with its own global counter!
    """return string appended with a unique number"""
    global Gno
    Gno += 1
    return string + str(Gno)

def genKey():
    """ produces generators that count indefinitely """
    i=0
    while 1:
        i += 1
        yield i

atKey = genKey() # generator for atom.key attribute.
    # As of bruce 050228, we now make use of the fact that this produces keys
    # which sort in the same order as atoms are created (e.g. the order they're
    # read from an mmp file), so we now require this in the future even if the
    # key type is changed.

###Huaicai: This function [povpoint] has been repeated in multiple files, not 
### good, needs to improve. I'll add one more function for transferring
### vector to a string, which is mainly used for color vector
# [bruce 050413: moved povpoint elsewhere]

def stringVec(v):
    return "<" + str(v[0]) + "," + str(v[1]) + "," + str(v[2]) + ">"    

# == Atom

##e bruce 041109 thinks class atom should be renamed Atom so it's easier to find
# all its uses in the code. To ease the change, I'll wait for my rewrites to
# go in before doing the renaming at all, then define atom() to print a warning
# and call Atom().

class atom:
    """An atom instance represents one real atom, or one "singlet"
    (a place near a real atom where another atom could bond to it).
       At any time, each atom has an element, a position in space,
    a list of bond objects it's part of, a list of jigs it's part of,
    and a reference to exactly one molecule object ("chunk") which
    owns it; all these attributes can change over time.
       It also has a never-changing key used as its key in self.molecule.atoms,
    a selection state, a display mode (which overrides that of its molecule),
    and (usually) some attributes added externally by its molecule, notably
    self.index. The attributes .index and .xyz are essentially for the
    private use of the owning molecule; see the methods posn and baseposn
    for details. Other code might add other attributes to an atom; some of
    those might be copied in the private method atom.copy_for_mol_copy().
    """
    # bruce 041109-16 wrote docstring
    def __init__(self, sym, where, mol):
        """create an atom of element sym (e.g. 'C')
        at location where (e.g. V(36, 24, 36))
        belonging to molecule mol, which is part of assembly assy
        """
        self.__killed = 0
        # unique key for hashing
        self.key = atKey.next()
        # element-type object
        self.element = PeriodicTable.getElement(sym)
        # 'where' is atom's absolute location in model space,
        # until replaced with 'no' by shakedown, indicating
        # the location should be found using the formula in self.posn();
        # or it can be passed as 'no' by caller of __init__
        self.xyz = where
        # list of bond objects
        self.bonds = []
        # list of jigs (###e should be treated analogously to self.bonds)
        self.jigs = [] # josh 10/26 to fix bug 85
        # whether the atom is selected; see also assembly.selatoms
        # (note that Nodes also have .picked, with the same meaning, but atoms
        #  are not Nodes)
        self.picked = 0
        # can be set to override molecule or global value
        self.display = diDEFAULT

        # pointer to molecule containing this atom
        # (note that the assembly is not explicitly stored
        #  and that the index is only set later by methods in the molecule)
        self.molecule = None # checked/replaced by mol.addatom
        if mol:
            mol.addatom(self)
            # bruce 041109 wrote addatom to do following for us and for hopmol:
            ## self.molecule = mol
            ## self.molecule.atoms[self.key] = self
            ## # now do the necessary invals in self.molecule for adding an atom
            ## ...
        else:
            # this now happens in mol.copy as of 041113
            # print "fyi: creating atom with mol == None"
            pass
        # (optional debugging code to show which code creates bad atoms:)
        ## if platform.atom_debug:
        ##     self._source = compact_stack()        
        return # from atom.__init__

    def posn(self):
        """Return the absolute position of the atom in space.
        Public method, should be ok to call for any atom at any time.
        Private implementation note (fyi): this info is sometimes stored
        in the atom, and sometimes in its molecule.
        
        """
        #bruce 041104,041112 revised docstring
        #bruce 041130 made this return copies of its data, using unary '+',
        # to ensure caller's version does not change if the atom's version does,
        # or vice versa. Before this change, some new code to compare successive
        # posns of the same atom was getting a reference to the curpos[index]
        # array element, even though this was part of a longer array, so it
        # always got two refs to the same mutable data (which compared equal)! 
        if self.xyz != 'no':
            return + self.xyz
        else:
            return + self.molecule.curpos[self.index]

    def baseposn(self): #bruce 041107; rewritten 041201 to help fix bug 204
        """Like posn, but return the mol-relative position.
        Semi-private method -- should always be legal, but assumes you have
        some business knowing about the mol-relative coordinate system, which is
        somewhat private since it's semi-arbitrary and is changed by some
        recomputation methods. Before 041201 that could include this one,
        if it recomputed basepos! But as of that date we'll never compute
        basepos or atpos if they're invalid.
        """
        #e Does this mean we no longer use baseposn for drawing? Does that
        # matter (for speed)? We still use it for things like mol.rot().
        # We could inline the old baseposn into mol.draw, for speed.
        # BTW would checking for basepos here be worth the cost of the check? (guess: yes.) ###e
        # For speed, I'll inline this here: return self.molecule.abs_to_base( self.posn())
        return self.molecule.quat.unrot(self.posn() - self.molecule.basecenter)

    def setposn(self, pos):
        """set the atom's absolute position,
        adjusting or invalidating whatever is necessary as a result.
        (public method; ok for atoms in frozen molecules too)
        """
        # fyi: called from depositMode, but not (yet?) from movie-playing. [041110]
        # [bruce 050406: now this is called from movie playing, at least for now.
        #  It's also been called (for awhile) from reading xyz files from Minimize.]
        # bruce 041130 added unary '+' (see atom.posn comment for the reason).
        pos = + pos
        if self.xyz != 'no':
            # bruce 041108 added xyz check, rather than asserting we don't need it;
            # this might never happen
            self.xyz = pos
            # The position being stored in the atom implies it's never been used
            # in the molecule (in curpos or atpos or anything derived from them),
            # so we don't need to invalidate anything in the molecule.
            # [bruce 041207 wonders: not even self.molecule.havelist = 0??
            #  I guess so, since mol.draw recomputes basepos, but not sure.
            #  But I also see no harm in doing it, and it was being done by
            #  deprecated code in setup_invalidate below, so I think I'll do it
            #  just to be safe.]
            self.molecule.havelist = 0
        else:
            # the position is stored in the molecule, so let it figure out the
            # proper way of adjusting it -- this also does the necessary invals.
            self.molecule.setatomposn(self.index, pos, self.element)
        # also invalidate the bonds or jigs which depend on our position.
        #e (should this be a separate method -- does anything else need it?)
        for b in self.bonds:
            b.setup_invalidate()
        ##bruce 050406 removing this, since too verbose for movie-playing:
##        if platform.atom_debug and self.jigs:
##            print "bug: atom.setposn needs to invalidate jigs, but that's nim"
        return

    def adjSinglets(self, atom, nupos):
        """We're going to move atom, a neighbor of yours, to nupos,
        so adjust the positions of your singlets to match.
        """
        apo = self.posn()
        # find the delta quat for the average real bond and apply
        # it to the singlets
        #bruce 050406 comment: this first averages the bond vectors,
        # old and new, then rotates old to match new. This is not
        # correct, especially if old or new (average) is near V(0,0,0).
        # The real problem is harder -- find a quat which best moves
        # atom as desired without moving the other neighbors.
        # Fixing this might fix some reported bugs with dragging atoms
        # within their chunks in Build mode. Better yet might be to
        # use old singlet posns purely as hints, recomputing new ones
        # from scratch (hints are useful to disambiguate this). ###@@@
        n = self.realNeighbors()
        old = V(0,0,0)
        new = V(0,0,0)
        for at in n:
            old += at.posn()-apo
            if at == atom: new += nupos-apo
            else: new += at.posn()-apo
        if n:
            q=Q(old,new)
            for at in self.singNeighbors():
                at.setposn(q.rot(at.posn()-apo)+apo)

    def __repr__(self):
        return self.element.symbol + str(self.key)

    def __str__(self):
        return self.element.symbol + str(self.key)

    def prin(self):
        """for debugging
        """
        lis = map((lambda b: b.other(self).element.symbol), self.bonds)
        print self.element.name, lis

    def draw(self, glpane, dispdef, col, level):
        """draw the atom depending on whether it is picked
        and its display mode (possibly inherited from dispdef).
        An atom's display mode overrides the inherited one from
        the molecule or glpane, but a molecule's color overrides the atom's
        element-dependent one. No longer treats glpane.selatom specially
        (caller can draw selatom separately, on top of the regular atom).
        """
        assert not self.__killed
        # note use of basepos (in atom.baseposn) since it's being drawn under
        # rotation/translation of molecule
        pos = self.baseposn()
        disp, drawrad = self.howdraw(dispdef)
        if disp == diTUBES:
            pickedrad = drawrad * 1.8
        else:
            pickedrad = drawrad * 1.1
        color = col or self.element.color
        if disp in [diVDW, diCPK, diTUBES]:
            drawsphere(color, pos, drawrad, level)
        if self.picked:
            #bruce 041217 experiment: show valence errors for picked atoms by
            # using a different color for the wireframe.
            # (Since Transmute operates on picked atoms, and leaves them picked,
            #  this will serve to show whatever valence errors it causes. And
            #  showing it only for picked atoms makes it not mess up any images,
            #  even though there's not yet any way to turn this feature off.)
            color = (self.bad() and ErrorPickedColor) or PickedColor
            drawwiresphere(color, pos, pickedrad)
        return

    def bad(self): #bruce 041217 experiment
        "is this atom breaking any rules?"
        elt = self.element
        if elt == Singlet:
            # should be correct, but this case won't be used as of 041217
            numbonds = 1
        else:
            numbonds = elt.numbonds
        return numbonds != len(self.bonds)

    def overdraw_with_special_color(self, color, level = None):
        "Draw this atom slightly larger than usual with the given special color and optional drawlevel."
        #bruce 050324; meant for use in Fuse Chunks mode;
        # also could perhaps speed up Extrude's singlet-coloring #e
        if level == None:
            level = self.molecule.assy.drawLevel
        pos = self.posn() # note, unlike for draw_as_selatom, this is in main model coordinates
        drawrad = self.selatom_radius() # slightly larger than normal drawing radius
        drawsphere(color, pos, drawrad, level) # always draw, regardless of display mode
        return
    
    def draw_as_selatom(self, glpane, dispdef, color, level):
        #bruce 041206, to avoid need for changeapp() when selatom changes
        # (fyi, as of 041206 the color arg is not used)
        if self.element == Singlet:
            color = LEDon
        else:
            color = orange
        pos = self.baseposn() # note, this is for use in the mol's coordinate system
        drawrad = self.selatom_radius(dispdef)
        drawsphere(color, pos, drawrad, level) # always draw, regardless of disp

    def selatom_radius(self, dispdef = None): #bruce 041207, should integrate with draw_as_selatom
        if dispdef == None:
            dispdef = self.molecule.get_dispdef()
        disp, drawrad = self.howdraw(dispdef)
        if self.element == Singlet:
            drawrad *= 1.02
                # increased radius might not be needed, if we would modify the
                # OpenGL depth threshhold criterion used by GL_DEPTH_TEST
                # to overwrite when depths are equal [bruce 041206]
        else:
            if disp == diTUBES:
                drawrad *= 1.7
            else:
                drawrad *= 1.02
        return drawrad
        
    def setDisplay(self, disp):
        self.display = disp
        self.molecule.changeapp(1)
        self.molecule.assy.changed() # bruce 041206 bugfix (unreported bug)
        # bruce 041109 comment:
        # atom.setDisplay changes appearance of this atom's bonds,
        # so: do we need to invalidate the bonds? No, they don't store display
        # info, and the geometry related to bond.setup_invalidate has not changed.
        # What about the mols on both ends of the bonds? The changeapp() handles
        # that for internal bonds, and external bonds are redrawn every time so
        # no invals are needed if their appearance changes.

    def howdraw(self, dispdef):
        """Tell how to draw the atom depending on its display mode (possibly
        inherited from dispdef, usually the molecule's effective dispdef).
        An atom's display mode overrides the inherited
        one from the molecule or glpane, but a molecule's color overrides the
        atom's element-dependent one (color is handled in atom.draw, not here,
        so this is just FYI).
           Return display mode and radius to use, in a tuple (disp, rad).
        For display modes in which the atom is not drawn, such as diLINES or
        diINVISIBLE, we return the same radius as in diCPK; it's up to the
        caller to check the disp we return and decide whether/how to use this
        radius (e.g. it might be used for atom selection in diLINES mode, even
        though the atoms are not shown).
        """
        #bruce 041206 moved rad *= 1.1 (for TUBES) from atom.draw into this method
        if dispdef == diDEFAULT: #bruce 041129 permanent debug code, re bug 21
            if platform.atom_debug and 0: #bruce 050419 disable this since always happens for Element Color Prefs dialog
                print "bug warning: dispdef == diDEFAULT in atom.howdraw for %r" % self
            dispdef = default_display_mode # silently work around that bug [bruce 041206]
        if self.element == Singlet:
            try:
                disp, rad_unused = self.bonds[0].other(self).howdraw(dispdef)
            except:
                # exceptions here (e.g. from bugs causing unbonded singlets)
                # cause too much trouble in other places to be permitted
                # (e.g. in selradius_squared and recomputing the array of them)
                # [bruce 041215]
                disp = default_display_mode
        else:
            if self.display == diDEFAULT:
                disp = dispdef
            else:
                disp = self.display
        rad = self.element.rvdw
        if disp != diVDW: rad=rad*CPKvdW
        if disp == diTUBES: rad = TubeRadius * 1.1 #bruce 041206 added "* 1.1"
        return (disp, rad)

    def selradius_squared(self):
        """Return square of desired "selection radius",
        or -1.0 if atom should not be selectable (e.g. invisible).
        This might depend on whether atom is selected (and that
        might even override the effect of invisibility); in fact
        this is the case for this initial implem.
        It also depends on the current display mode of
        self, its mol, and its glpane.
        Ignore self.molecule.hidden and whether self == selatom.
        Note: self.visible() should agree with self.selradius_squared() >= 0.0.
        """
        #bruce 041207. Invals for this are subset of those for changeapp/havelist.
        disp, rad = self.howdraw( self.molecule.get_dispdef() )
        if disp == diINVISIBLE and not self.picked:
            return -1.0
        else:
            return rad ** 2

    def visible(self, dispdef = None): #bruce 041214
        """Say whether this atom is currently visible, for purposes of selection.
        Note that this depends on self.picked, and display modes of self, its
        chunk, and its glpane, unless you pass disp (for speed) which is treated
        as the chunk's (defined or inherited) display mode.
        Ignore self.molecule.hidden and whether self == selatom.
        Return a correct value for singlets even though no callers [as of 041214]
        would care what we returned for them.
        Note: self.visible() should agree with self.selradius_squared() >= 0.0.
        """
        if self.picked:
            return True # even for invisible atoms
        if self.element == Singlet:
            disp = self.bonds[0].other(self).display
        else:
            disp = self.display
        if disp == diDEFAULT: # usual case; use dispdef
            # (note that singlets are assumed to reside in same chunks as their
            # real neighbor atoms, so the same dispdef is valid for them)
            if dispdef == None:
                disp = self.molecule.get_dispdef()
            else:
                disp = dispdef
        return not (disp == diINVISIBLE)

    def writemmp(self, mapping): #bruce 050322 revised interface to use mapping
        "[compatible with Node.writemmp, though we're not a subclass of Node]"
        num_str = mapping.encode_next_atom(self) # (note: pre-050322 code used an int here)
##        atnums['NUM'] += 1
##        num = atnums['NUM']
##        alist += [self]
##        atnums[self.key] = num
        disp = mapping.dispname(self.display) # note: affected by mapping.sim flag
        posn = self.posn() # might be revised below
        eltnum = self.element.eltnum # might be revised below
        if mapping.sim and self.element == Singlet:
            # special case for singlets in mmp files meant only for simulator:
            # pretend we're a Hydrogen, and revise posn and eltnum accordingly
            # (for writing only, not stored in our attrs)
            # [bruce 050404 to help fix bug 254]
            eltnum = Hydrogen.eltnum
            posn = self.ideal_posn_re_neighbor( self.singlet_neighbor(), pretend_I_am = Hydrogen )
            disp = "singlet" # kluge, meant as a comment in the file
        xyz = posn * 1000
            # note, xyz has floats, rounded below (watch out for this
            # if it's used to make a hash) [bruce 050404 comment]
        print_fields = (num_str, eltnum,
           int(xyz[0]), int(xyz[1]), int(xyz[2]), disp)
        mapping.write("atom %s (%d) (%d, %d, %d) %s\n" % print_fields)
        # write only the bonds which have now had both atoms written
        bl = [] # (note: in pre-050322 code bl held ints, not strings)
        for b in self.bonds:
            oa = b.other(self)
            #bruce 050322 revised this:
            oa_code = mapping.encode_atom(oa) # None, or true and prints as "atom number string"
            if oa_code:
                bl.append(oa_code)
##            if oa.key in atnums: bl += [atnums[oa.key]]
        if len(bl) > 0:
            mapping.write("bond1 " + " ".join(bl) + "\n")
    
    # write to a povray file:  draw a single atom
    def writepov(self, file, dispdef, col):
        color = col or self.element.color
        disp, rad = self.howdraw(dispdef)
        if disp in [diVDW, diCPK]:
            file.write("atom(" + povpoint(self.posn()) +
                       "," + str(rad) + "," +
                       stringVec(color) + ")\n")
        if disp == diTUBES:
            ###e this should be merged with other case, and should probably
            # just use rad from howdraw [bruce 041206 comment]
            file.write("atom(" + povpoint(self.posn()) +
                       "," + str(rad) + "," +
                       stringVec(color) + ")\n")

    # write to a MDL file.  By Chris Phoenix and Mark for John Burch [04-12-03]
    def writemdl(self, alist, f, dispdef, col):
        color = col or self.element.color
        disp, radius = self.howdraw(dispdef)
        xyz=map(float, A(self.posn()))
        rgb=map(int,A(color)*255)
        atnum = len(alist) # current atom number
#        print "chem.writemdl(): atnum =", atnum,", xyz = ",xyz,", radius = ",radius,", rgb = ",rgb
        
        alist.append([xyz, radius, rgb])
        
        # Write spline info for this atom
        atomOffset = 80*atnum
        (x,y,z) = xyz
        for spline in range(5):
            f.write("CPs=8\n")
            for point in range(8):
                index = point+spline*8
                (px,py,pz)=marks[index]
                px = px*radius + x; py = py*radius + y; pz = pz*radius + z
                if point == 7:
                    flag = "3825467397"
                else:
                    flag = "3825467393"
                f.write("%s 0 %d\n%f %f %f\n%s%s"%
                           (flag, index+19+atomOffset, px, py, pz,
                            filler, filler))
        
        for spline in range(8):
            f.write("CPs=5\n")
            for point in range(5):
                index = point+spline*5
                f.write("3825467393 1 %d\n%d\n%s%s"%
                           (index+59+atomOffset, links[index]+atomOffset,
                            filler, filler))


    def checkpick(self, p1, v1, disp, r=None, iPic=None):
        """Selection function for atoms: [Deprecated! bruce 041214]
        Check if the line through point p1 in direction v1 goes through the
        atom (treated as a sphere with the same radius it would be drawn with,
        which might depend on disp, or with the passed-in radius r if that's
        supplied). If not, or if the atom is a singlet, or if not iPic and the
        atom is already picked, return None. If so, return the distance along
        the ray (from p1 towards v1) of the point closest to the atom center
        (which might be 0.0, which is false!), or None if that distance is < 0.
        """
        #bruce 041206 revised docstring to match code
        #bruce 041207 comment: the only call of checkpick is from assy.findpick
        if self.element == Singlet: return None
        if not r:
            disp, r = self.howdraw(disp)
        # bruce 041214:
        # this is surely bad in only remaining use (depositMode.getCoords):
        ## if self.picked and not iPic: return None 
        dist, wid = orthodist(p1, v1, self.posn())
        if wid > r: return None
        if dist<0: return None
        return dist

    def getinfo(self):
        # Return information about the selected atom for the msgbar
        # [mark 2004-10-14]
        # bruce 041217 revised XYZ format to %.2f, added bad-valence info
        # (for the same atoms as self.bad(), but in case conditions are added to
        #  that, using independent code).
        # bruce 050218 changing XYZ format to %.3f (after earlier discussion with Josh).
        
        if self == self.molecule.assy.ppa2: return
            
        xyz = self.posn()
        ainfo = ("Atom %s [%s] [X = %.3f] [Y = %.3f] [Z = %.3f]" % \
            ( self, self.element.name, xyz[0], xyz[1], xyz[2] ))
        
        # ppa2 is the previously picked atom.  ppa3 is the atom picked before ppa2.
        # They are both reset to None when entering SELATOMS mode.
        # Include the distance between self and ppa2 in the info string.
        if self.molecule.assy.ppa2:
            try:
                ainfo += (". Distance between %s-%s is %.3f." % \
                    (self, self.molecule.assy.ppa2, vlen(self.posn()-self.molecule.assy.ppa2.posn())))
            except:
                print_compact_traceback("bug, fyi: ignoring exception in atom distance computation: ") #bruce 050218
                pass
            
            # Include the angle between self, ppa2 and ppa3 in the info string.
            if self.molecule.assy.ppa3:
                try:
                    # bruce 050218 protecting angle computation from exceptions
                    # (to reduce severity of undiagnosed bug 361).
                    v1 = norm(self.posn()-self.molecule.assy.ppa2.posn())
                    v2 = norm(self.molecule.assy.ppa3.posn()-self.molecule.assy.ppa2.posn())
                    dotprod = dot(v1,v2)
                    if dotprod > 1.0:
                        #bruce 050414 investigating bugs 361 and 498 (probably the same underlying bug);
                        # though (btw) it would probably be better to skip this angle-printing entirely ###e
                        # if angle obviously 0 since atoms 1 and 3 are the same.
                        # This case (dotprod > 1.0) can happen due to numeric roundoff in norm();
                        # e.g. I've seen this be 1.0000000000000002 (as printed by '%r').
                        # If not corrected, it can make acos() return nan or have an exception!
                        dotprod = 1.0
                    elif dotprod < -1.0:
                        dotprod = -1.0
                    ang = acos(dotprod) * 180/pi
                    ainfo += (" Angle for %s-%s-%s is %.2f degrees." %\
                        (self, self.molecule.assy.ppa2, self.molecule.assy.ppa3, ang))
                except:
                    print_compact_traceback("bug, fyi: ignoring exception in atom angle computation: ") #bruce 050218
                    pass
            
            # ppa3 is ppa2 for next atom picked.
            self.molecule.assy.ppa3 = self.molecule.assy.ppa2 
        
        # ppa2 is self for next atom picked.
        self.molecule.assy.ppa2 = self 
            
        if len(self.bonds) != self.element.numbonds:
            # I hope this can't be called for singlets! [bruce 041217]
            ainfo += platform.fix_plurals(" (has %d bond(s), should have %d)" % \
                                          (len(self.bonds), self.element.numbonds))
        return ainfo

    def pick(self):
        """make the atom selected
        """
        if self.element == Singlet: return
        # If select atoms filter is on, only pick element type in the filter combobox
        if self.molecule.assy.w.SAFilter.isChecked() and \
            self.element.name != self.molecule.assy.w.SAFilterList.currentText(): return
        if not self.picked:
            self.picked = 1
            self.molecule.assy.selatoms[self.key] = self
                #bruce comment 050308: should be ok even if selatoms recomputed for assy.part
            self.molecule.changeapp(1)
            # bruce 041227 moved message from here to one caller, pick_at_event
            #bruce 050308 comment: we also need to ensure that it's ok to pick atoms
            # (wrt selwhat), and change current selection group to include self.molecule
            # if it doesn't already. But in practice, all callers might be ensuring these
            # conditions already (this is likely to be true if pre-assy/part code was correct).
            # In particular, atoms are only picked by user in glpane or perhaps by operations
            # on current part, and in both cases the picked atom would be in the current part.
            # If atoms can someday be picked from the mtree (directly or by selecting a jig that
            # connects to them), this will need review.
        return
    
    def unpick(self):
        """make the atom unselected
        """
        # note: this is inlined into assembly.unpickatoms
        # bruce 041214: should never be picked, so Singlet test is not needed,
        # and besides if it ever *does* get picked (due to a bug) you should let
        # the user unpick it!
        ## if self.element == Singlet: return 
        if self.picked:
            try:
                #bruce 050309 catch exceptions, and do this before picked=0
                # so that if selatoms is recomputed now, the del will still work
                # (required by upcoming "assy/part split")
                del self.molecule.assy.selatoms[self.key]
            except:
                if platform.atom_debug:
                    print_compact_traceback("atom_debug: atom.unpick finds atom not in selatoms: ")
            self.picked = 0
            self.molecule.changeapp(1)

    def copy_for_mol_copy(self, numol):
        # bruce 041113 changed semantics, and renamed from copy()
        # to ensure only one caller, which is mol.copy()
        """create a copy of the atom (to go in numol, a copy of its molecule),
        with .xyz == 'no' and .index the same as in self;
        caller must also call numol.invalidate_atom_lists() at least once
        [private method, only suitable for use from mol.copy(), since use of
         same .index assumes numol will be given copied curpos/basepos arrays.]
        """
        nuat = atom(self.element.symbol, 'no', None)
        numol.addcopiedatom(nuat)
        ## numol.invalidate_atom_lists() -- done in caller now
        nuat.index = self.index
        nuat.display = self.display #bruce 041109 new feature, seems best
        try:
            nuat.info = self.info
            # bruce 041109, needed by extrude and other future things
        except AttributeError:
            pass
        return nuat

    def copy(self): # bruce 041116, new method
        # (warning: has previous name of copy_for_mol_copy method)
        """Public method: copy an atom, with no special assumptions;
        new atom is not in any mol but could be added to one using mol.addatom.
        """
        nuat = atom(self.element.symbol, self.posn(), None)
        nuat.display = self.display
        try:
            nuat.info = self.info
            # bruce 041109, needed by extrude and other future things
        except AttributeError:
            pass
        return nuat

    def unbond(self, b):
        """Private method (for use mainly by bonds); remove b from self and
        usually replace it with a singlet (which is returned). Details:
           Remove bond b from self (error if b not in self.bonds).
        Note that bonds are compared with __eq__, not 'is', by 'in' and 'remove'.
        Only call this when b will be destroyed, or "recycled" (by bond.rebond);
        thus no need to invalidate the bond b itself -- caller must do whatever
        inval of bond b is needed (which is nothing, if it will be destroyed).
           Then replace bond b in self.bonds with a new bond to a new singlet,
        unless self or the old neighbor atom is a singlet. Return the new
        singlet, or None if one was not created. Do all necessary invalidations
        of molecules, BUT NOT OF b (see above).
           If self is a singlet, kill it (singlets must always have one bond).
           As of 041109, this is called from atom.kill of the other atom,
        and from bond.bust, and [added by bruce 041109] from bond.rebond.
        """
        # [obsolete comment: Caller is responsible for shakedown
        #  or kill (after clearing externs) of affected molecules.]
        
        # code and docstring revised by bruce 041029, 041105-12
        
        b.invalidate_bonded_mols() #e more efficient if callers did this
        
        try:
            self.bonds.remove(b)
        except ValueError: # list.remove(x): x not in list
            # this is always a bug in the caller, but we catch it here to
            # prevent turning it into a worse bug [bruce 041028]
            msg = "fyi: atom.unbond: bond %r should be in bonds %r\n of atom %r, " \
                  "but is not:\n " % (b, self.bonds, self)
            print_compact_traceback(msg)
        # normally replace an atom (bonded to self) with a singlet,
        # but don't replace a singlet (at2) with a singlet,
        # and don't add a singlet to another singlet (self).
        if self.element == Singlet:
            if not self.bonds:
                self.kill() # bruce 041115 added this and revised all callers
            else:
                print "fyi: bug: unbond on a singlet %r finds unexpected bonds left over in it, %r" % (self,self.bonds)
                # don't kill it, in this case [bruce 041115; I don't know if this ever happens]
            return None
        at2 = b.other(self)
        if at2.element == Singlet:
            return None
        x = atom('X', b.ubp(self), self.molecule) # invals mol as needed
        self.molecule.bond(self, x) # invals mol as needed
        return x # new feature, bruce 041222

    def get_neighbor_bond(self, neighbor):
        '''Return the bond to a neighboring atom, or None if none exists.
        '''
        for b in self.bonds:
            if b.other(self) == neighbor:
               return b
        return None
            
    def hopmol(self, numol): #bruce 041105-041109 extensively revised this
        """If this atom is not already in molecule numol, move it
        to molecule numol. (This only changes the owning molecule -- it doesn't
        change this atom's position in space!) Also move its singlet-neighbors.
        Do all necessary invalidations of old and new molecules,
        including for this atom's bonds (both internal and external),
        since some of those bonds might change from internal to external
        or vice versa, which changes how they need to be drawn.
        """
        # bruce 041222 removed side effect on self.picked
        if self.molecule == numol:
            return
        self.molecule.delatom(self) # this also invalidates our bonds
        numol.addatom(self)
        for atm in self.singNeighbors():
            assert self.element != Singlet # (only if we have singNeighbors!)
                # (since hopmol would infrecur if two singlets were bonded)
            atm.hopmol(numol)
        return
    
    def neighbors(self):
        """return a list of the atoms bonded to this one
        """
        return map((lambda b: b.other(self)), self.bonds)
    
    def realNeighbors(self):
        """return a list of the atoms not singlets bonded to this one
        """
        return filter(lambda atm: atm.element != Singlet, self.neighbors())
    
    def singNeighbors(self):
        """return a list of the singlets bonded to this atom
        """
        return filter(lambda atm: atm.element == Singlet, self.neighbors())

    singletNeighbors = singNeighbors #bruce 050404, soon should just rename it and all the uses ###e ###@@@
    
    def mvElement(self, elt):
        """[Public low-level method:]
        Change the element type of this atom to element elt
        (an element object for a real element, not Singlet),
        and do the necessary invalidations (including if the
        *prior* element type was Singlet).
           Note: this does not change any atom or singlet positions, so callers
        wanting to correct the bond lengths need to do that themselves.
        It does not even delete or add extra singlets to match the new element
        type; for that, use atom.Transmute.
        """
        if (self.element == Singlet) != (elt == Singlet):
            # set of singlets is changing
            #bruce 050224: fix bug 372 by invalidating singlets
            self.molecule.invalidate_attr('singlets')
        if platform.atom_debug:
            if elt == Singlet: #bruce 041118
                # this is unsupported; if we support it it would require
                # moving this atom to its neighbor atom's chunk, too
                # [btw we *do* permit self.element == Singlet before we change it]
                print "atom_debug: fyi, bug?: mvElement changing %r to a singlet" % self
        self.element = elt
        for b in self.bonds:
            b.setup_invalidate()
        self.molecule.changeapp(1)
        # no need to invalidate shakedown-related things, I think [bruce 041112]

    def invalidate_bonds(self): # also often inlined
        for b in self.bonds:
            b.setup_invalidate()
        
    def killed(self): #bruce 041029
        """(Public method) Report whether an atom has been killed.
        Details: For an ordinary atom, return False.
        For an atom which has been properly killed, return True.
        For an atom which has something clearly wrong with it,
        print an error message, try to fix the problem,
        effectively kill it, and return True.
        Don't call this on an atom still being initialized.
        """
        try:
            killed = not (self.key in self.molecule.atoms)
            if killed:
                assert self.__killed == 1
                assert not self.picked
                from chunk import _nullMol
                assert self.molecule == _nullMol or self.molecule == None
                # thus don't do this: assert not self.key in self.molecule.assy.selatoms
                assert not self.bonds
                assert not self.jigs
            else:
                assert self.__killed == 0
            return killed
        except:
            print_compact_traceback("fyi: atom.killed detects some problem" \
                " in atom %r, trying to work around it:\n " % self )
            try:
                self.__killed = 0 # make sure kill tries to do something
                self.kill()
            except:
                print_compact_traceback("fyi: atom.killed: ignoring" \
                    " exception when killing atom %r:\n " % self )
            return True
        pass # end of atom.killed()

    def kill(self):
        """Public method:
        kill an atom: unpick it, remove it from its jigs, remove its bonds,
        then remove it from its molecule. Do all necessary invalidations.
        (Note that molecules left with no atoms, by this or any other op,
        will themselves be killed.)
        """
        if self.__killed:
            if not self.element == Singlet:
                print_compact_stack("fyi: atom %r killed twice; ignoring:\n" % self)
            else:
                # Note: killing a selected mol, using Delete key, kills a lot of
                # singlets twice; I guess it's because we kill every atom
                # and singlet in mol, but also kill singlets of killed atoms.
                # So I'll declare this legal, for singlets only. [bruce 041115]
                pass
            return
        self.__killed = 1 # do this now, to reduce repeated exceptions (works??)
        # unpick
        try:
            self.unpick() #bruce 041029
        except:
            print_compact_traceback("fyi: atom.kill: ignoring error in unpick: ")
            pass
        # bruce 041115 reordered everything that follows, so it's safe to use
        # delatom (now at the end, after things which depend on self.molecule),
        # since delatom resets self.molecule to None.
        
        # josh 10/26 to fix bug 85 - remove from jigs
        for j in self.jigs[:]: #bruce 050214 copy list as a precaution
            try:
                j.rematom(self)
                # [bruce 050215 comment: this might kill the jig (if it has no
                #  atoms left), and/or it might remove j from self.jigs, but it
                #  will never recursively kill this atom, so it should be ok]
            except:
                print_compact_traceback("fyi: atom.kill: ignoring error in rematom %r from jig %r: " % (self,j) )
        self.jigs = [] #bruce 041029 mitigate repeated kills
            # [bruce 050215 comment: this should soon no longer be needed, but will be kept as a precaution]
        
        # remove bonds
        for b in self.bonds[:]: #bruce 050214 copy list as a precaution
            n = b.other(self)
            n.unbond(b) # note: this can create a new singlet on n, if n is real,
                        # which requires computing b.ubp which uses self.posn()
                        # or self.baseposn(); or it can kill n if it's a singlet.
                        #e We should optim this for killing lots of atoms at once,
                        # eg when killing a chunk, since these new singlets are
                        # wasted then. [bruce 041201]
            # note: as of 041029 unbond also invalidates externs if necessary
            ## if n.element == Singlet: n.kill() -- done in unbond as of 041115
        self.bonds = [] #bruce 041029 mitigate repeated kills

        # only after disconnected from everything else, remove it from its molecule
        try:
            ## del self.molecule.atoms[self.key]
            self.molecule.delatom(self) # bruce 041115
            # delatom also kills the mol if it becomes empty (as of bruce 041116)
        except KeyError:
            print "fyi: atom.kill: atom %r not in its molecule (killed twice?)" % self
            pass
        return # from atom.kill

    def Hydrogenate(self):
        """[Public method; does all needed invalidations:]
        If this atom is a singlet, change it to a hydrogen,
        and move it so its distance from its neighbor is correct
        (regardless of prior distance, but preserving prior direction).
        [#e sometimes it might be better to fix the direction too, like in depositMode...]
           If hydrogenate succeeds return number 1, otherwise, 0.
        """
        # Huaicai 1/19/05 added return value.
        if not self.element == Singlet: return 0
        other = self.bonds[0].other(self)
        self.mvElement(Hydrogen)
        #bruce 050406 rewrote the following, so it no longer depends
        # on old pos being correct for self being a Singlet.
        newpos = self.ideal_posn_re_neighbor( other)
        self.setposn(newpos)
        return 1
        
    def ideal_posn_re_neighbor(self, neighbor, pretend_I_am = None): # see also snuggle
        #bruce 050404 to help with bug 254 and maybe Hydrogenate
        """Given one of our neighbor atoms (real or singlet)
        [neighborness not verified! only posn is used, not the bond --
         this might change when we have bond-types #e]
        and assuming it should remain fixed and our bond to it should
        remain in the same direction, and pretending (with no side effects)
        that our element is pretend_I_am if this is given,
        what position should we ideally have
        so that our bond to neighbor has the correct length?
        """
        me = self.posn()
        it = neighbor.posn()
        length = vlen( me - it )
        if not length:
            #e atom_debug warning?
            # choose a better direction? only caller knows what to do, i guess...
            # but [050406] I think an arbitrary one is safer than none!
            ## return me # not great...
            it_to_me_direction = V(1,0,0)
        else:
            it_to_me_direction = norm( me - it )
            it_to_me_direction = norm( it_to_me_direction )
                # for original len close to 0, this might help make new len 1 [bruce 050404]
        my_elem = pretend_I_am or self.element
        its_elem = neighbor.element
        # assume bond-type is single bond for now
        newlen = my_elem.rcovalent + its_elem.rcovalent #k Singlet.rcovalent better be 0, check this
        return it + newlen * it_to_me_direction
        
    def Dehydrogenate(self):
        """[Public method; does all needed invalidations:]
        If this is a hydrogen atom (and if it was not already killed),
        kill it and return 1 (int, not boolean), otherwise return 0.
        (Killing it should produce a singlet unless it was bonded to one.)
        """
        # [fyi: some new features were added by bruce, 041018 and 041029;
        #  need for callers to shakedown or kill mols removed, bruce 041116]
        if self.element == Hydrogen and not self.killed():
            #bruce 041029 added self.killed() check above to fix bug 152
            self.kill()
            # note that the new singlet produced by killing self might be in a
            # different mol (since it needs to be in our neighbor atom's mol)
            #bruce 050406 comment: if we reused the same atom (as in Hydrogenate)
            # we'd be better for movies... just reusing its .key is not enough
            # if we've internally stored alists. But, we'd like to fix the direction
            # just like this does for its new singlet... so I'm not changing this for now.
            # Best solution would be a new method for H or X to fix their direction
            # as well as their distance. ###@@@
            return 1
        else:
            return 0
        pass

    def snuggle(self):
        """self is a singlet and the simulator has moved it out to the
        radius of an H. move it back. the molecule may or may not be still
        in frozen mode. Do all needed invals.
        """
        if not self.bonds:
            #bruce 050428: a bug, but probably just means we're a killed singlet.
            # The caller should be fixed, and maybe is_singlet should check this too,
            # but for now let's also make it harmless here:
            if platform.atom_debug:
                print_compact_stack( "atom_debug: bug (ignored): snuggling a killed singlet: ")
            return
        #bruce 050406 revised docstring to say mol needn't be frozen.
        # note that this could be rewritten to call ideal_posn_re_neighbor,
        # but we'll still use it since it's better tested and faster.
        o = self.bonds[0].other(self)
        op = o.posn()
        np = norm(self.posn()-op)*o.element.rcovalent + op
        # bruce 041112 rewrote last line
        self.setposn(np)
        ## self.molecule.curpos[self.index] = np

    def Passivate(self):
        """[Public method, does all needed invalidations:]
        Change the element type of this atom to match the number of
        bonds with other real atoms, and delete singlets.
        """
        # bruce 041215 modified docstring, added comments, capitalized name
        el = self.element
        PTsenil = PeriodicTable.getPTsenil()
        line = len(PTsenil)
        for i in range(line):
            if el in PTsenil[i]:
                line = i
                break
        if line == len(PTsenil): return #not in table
        # (note: we depend on singlets not being in the table)
        nrn = len(self.realNeighbors())
        for atm in self.singNeighbors():
            atm.kill()
        try:
            newelt = PTsenil[line][nrn]
        except IndexError:
            pass # bad place for status msg, since called on many atoms at once
        else:
            self.mvElement(newelt)
        # note that if an atom has too many bonds we'll delete the
        # singlets anyway -- which is fine

    def is_singlet(self):
        return self.element == Singlet # [bruce 050502 comment: it's possible self is killed and len(self.bonds) is 0]
    
    def singlet_neighbor(self): #bruce 041109 moved here from extrudeMode.py
        "return the atom self (a known singlet) is bonded to, checking assertions"
        assert self.element == Singlet, "%r should be a singlet but is %s" % (self, self.element.name)
            #bruce 050221 added data to the assert, hoping to track down bug 372 when it's next seen
        obond = self.bonds[0]
        atom = obond.other(self)
        assert atom.element != Singlet, "bug: a singlet %r is bonded to another singlet %r!!" % (self,atom)
        return atom

    # higher-valence bonds methods [bruce 050502]
    
    def singlet_v6(self):
        assert self.element == Singlet, "%r should be a singlet but is %s" % (self, self.element.name)
        assert len(self.bonds) == 1, "%r should have exactly 1 bond but has %d" % (self, len(self.bonds))
        return self.bonds[0].v6

    def singlet_reduce_valence_noupdate(self, vdelta):
        assert self.element == Singlet, "%r should be a singlet but is %s" % (self, self.element.name)
        assert len(self.bonds) == 1, "%r should have exactly 1 bond but has %d" % (self, len(self.bonds))
        self.bonds[0].reduce_valence_noupdate(vdelta, permit_illegal_valence = True) # permits in-between, 0, or negative(?) valence
        return
    
    # debugging methods (not yet fully tested; use at your own risk)
    
    def invalidate_everything(self): # for an atom, remove it and then readd it to its mol
        "debugging method"
        if len(self.molecule.atoms) == 1:
            print "warning: invalidate_everything on the only atom in mol %r\n" \
                  " might kill mol as a side effect!" % self.molecule
        # note: delatom invals self.bonds
        self.molecule.delatom(self) # note: this kills the mol if it becomes empty!
        self.molecule.addatom(self)
        return

    def update_everything(self):
        print "atom.update_everything() does nothing"
        return

    def Transmute(self, elt, force = False): #bruce 041215, written to fix bug 131
        """[Public method, does all needed invalidations:]
        If this is a real atom, change its element type to elt (not Singlet),
        and replace its singlets (if any) with new ones (if any are needed)
        to match the desired number of bonds for the new element type.
        Never remove real bonds, even if there are too many. Don't change
        bond lengths (except to replaced singlets) or atom positions.
        If there are too many real bonds for the new element type, refuse
        to transmute unless force is True.
        """
        if self.element == Singlet:
            return
        if self.element == elt and len(self.bonds) == elt.numbonds:
            # leave existing singlet positions alone, if right number
            return
        nbonds = len(self.realNeighbors())
        if nbonds > elt.numbonds:
            # transmuting would break valence rules
            if force:
                msg = "warning: Transmute broke valence rules, made (e.g.) %s with %d bonds" % (elt.name, nbonds)
                self.molecule.assy.w.history.message(msg)
                # fall through
            else:
                msg = "warning: Transmute refused to make (e.g.) a %s with %d bonds" % (elt.name, nbonds)
                self.molecule.assy.w.history.message(msg)
                return
        # in all other cases, replace all singlets with 0 or more new ones
        for atm in self.singNeighbors():
            atm.kill()
                # (since atm is a singlet, this doesn't replace it with a singlet)
        self.mvElement(elt)
        self.make_enough_singlets()

    def make_enough_singlets(self): #bruce 041215, written to fix bug 131
        """[Public method, does all needed invalidations:]
        Add 0 or more singlets to this real atom, until it has as many bonds
        as its element type prefers (but at most 4, since we use special-case
        code whose knowledge only goes that high). Add them in good positions
        relative to existing bonds (if any) (which are not changed, whether
        they are real or open bonds).
        """
        if len(self.bonds) >= self.element.numbonds:
            return # don't want any more bonds
        # number of existing bonds tells how to position new open bonds
        # (for some n we can't make arbitrarily high numbers of wanted open
        # bonds; for other n we can; we can always handle numbonds <= 4)
        n = len(self.bonds)
        if n == 0:
            self.make_singlets_when_no_bonds()
        elif n == 1:
            self.make_singlets_when_1_bond()
        elif n == 2:
            self.make_singlets_when_2_bonds()
        elif n == 3:
            self.make_singlets_when_3_bonds() # (makes at most one open bond)
        else:
            pass # no code for adding open bonds to 4 or more existing bonds
        return

    # the make_singlets methods were split out of the private depositMode methods
    # (formerly called bond1 - bond4), to help implement atom.Transmute [bruce 041215]

    def make_singlets_when_no_bonds(self):
        "[private method; see docstring for make_singlets_when_2_bonds]"
        # unlike the others, this was split out of oneUnbonded [bruce 041215]
        elem = self.element
        if elem.bonds and elem.bonds[0][2]:
            r = elem.rcovalent
            pos = self.posn()
            mol = self.molecule
            for dp in elem.bonds[0][2]:
                x = atom('X', pos+r*dp, mol)
                mol.bond(self,x)
        return
    
    def make_singlets_when_1_bond(self):
        "[private method; see docstring for make_singlets_when_2_bonds]"
        ## print "what the heck is this global variable named a doing here? %r" % (a,)
        ## its value is 0.85065080835203999; where does it come from? it hide bugs. ###@@@
        assert len(self.bonds) == 1
        assert not self.is_singlet()
        el = self.element
        if len(el.quats): #bruce 041119 revised to support "onebond" elements
            # There is at least one other bond we should make (as open bond);
            # this rotates the atom to match the existing bond
            pos = self.posn()
            s1pos = self.bonds[0].ubp(self)
            r = s1pos - pos
            del s1pos # same varname used differently below
            rq = Q(r,el.base)
            # if the other atom has any other bonds, align 60 deg off them
            # [bruce 041215 comment: might need revision if numbonds > 4]
            a1 = self.bonds[0].other(self) # our real neighbor
            if len(a1.bonds)>1:
                # don't pick ourself
                if self == a1.bonds[0].other(a1):
                    a2pos = a1.bonds[1].other(a1).posn()
                else:
                    a2pos = a1.bonds[0].other(a1).posn()
                s1pos = pos+(rq + el.quats[0] - rq).rot(r)
                spin = twistor(r,s1pos-pos, a2pos-a1.posn()) + Q(r, pi/3.0)
            else: spin = Q(1,0,0,0)
            mol = self.molecule
            for q in el.quats:
                q = rq + q - rq - spin
                x = atom('X', pos+q.rot(r), mol)
                mol.bond(self,x)
        return
        
    def make_singlets_when_2_bonds(self):
        """[private method for make_enough_singlets:]
        Given an atom with exactly 2 real bonds (and no singlets),
        see if it wants more bonds (due to its element type),
        and make extra singlets if so,
        in good positions relative to the existing real bonds.
        Precise result might depend on order of existing bonds in self.bonds.
        """
        assert len(self.bonds) == 2 # usually both real bonds; doesn't matter
        el = self.element
        if el.numbonds <= 2: return # optimization
        # rotate the atom to match the 2 bonds it already has
        # (i.e. figure out a suitable quat -- no effect on atom itself)
        pos = self.posn()
        s1pos = self.bonds[0].ubp(self)
        s2pos = self.bonds[1].ubp(self)
        r = s1pos - pos
        rq = Q(r,el.base)
        # this moves the second bond to a possible position;
        # note that it doesn't matter which bond goes where
        q1 = rq + el.quats[0] - rq
        b2p = q1.rot(r)
        # rotate it into place
        tw = twistor(r, b2p, s2pos - pos)
        # now for all the rest
        # (I think this should work for any number of new bonds [bruce 041215])
        mol = self.molecule
        for q in el.quats[1:]:
            q = rq + q - rq + tw
            x = atom('X', pos+q.rot(r), mol)
            mol.bond(self,x)
        return

    def make_singlets_when_3_bonds(self):
        "[private method; see docstring for make_singlets_when_2_bonds]"
        assert len(self.bonds) == 3
        el = self.element
        if el.numbonds > 3:
            # bruce 041215 to fix a bug (just reported in email, no bug number):
            # Only do this if we want more bonds.
            # (But nothing is done to handle more than 4 desired bonds.
            #  Our element table has a comment claiming that its elements with
            #  numbonds > 4 are not yet used, but nothing makes me confident
            #  that comment is up-to-date.)
            pos = self.posn()
            s1pos = self.bonds[0].ubp(self)
            s2pos = self.bonds[1].ubp(self)
            s3pos = self.bonds[2].ubp(self)
            opos = (s1pos + s2pos + s3pos)/3.0
            try:
                assert vlen(pos-opos) > 0.001
                dir = norm(pos-opos)
            except:
                # [bruce 041215:]
                # fix unreported unverified bug (self at center of its neighbors):
                if platform.atom_debug:
                    print "atom_debug: fyi: self at center of its neighbors (more or less)",self,self.bonds
                dir = norm(cross(s1pos-pos,s2pos-pos)) ###@@@ need to test this!
            opos = pos + el.rcovalent*dir
            mol = self.molecule
            x = atom('X', opos, mol)
            mol.bond(self,x)
        return

    pass # end of class atom

def singlet_atom(singlet):
    "return the atom a singlet is bonded to, checking assertions"
    return singlet.singlet_neighbor()

def oneUnbonded(elem, assy, pos):
    """[bruce comment 040928:] create one unbonded atom, of element elem,
    at position pos, in its own new molecule."""
    # bruce 041215 moved this from chunk.py to chem.py, and split part of it
    # into the new atom method make_singlets_when_no_bonds, to help fix bug 131.
    mol = molecule(assy, 'bug') # name is reset below!
    atm = atom(elem.symbol, pos, mol)
    # bruce 041124 revised name of new mol, was gensym('Chunk.');
    # no need for gensym since atom key makes the name unique, e.g. C1.
    mol.name = "Chunk-%s" % str(atm)
    atm.make_singlets_when_no_bonds()
    assy.addmol(mol)
    return atm


# === Bonds [this file should be split in two at this point -- bruce 050502 #####@@@@@]


class bondtype:
    """not implemented
    """
    pass
    # int at1, at2;    /* types of the elements */
    # num r0,ks;           /* bond length and stiffness */
    # num ediss;           /* dissociation (breaking) energy */
    # int order;            /* 1 single, 2 double, 3 triple */
    # num length;          // bond length from nucleus to nucleus
    # num angrad1, aks1;        // angular radius and stiffness for at1
    # num angrad2, aks2;        // angular radius and stiffness for at2

def bonded(a1, a2): #bruce 041119 #e optimized by bruce 050502 (this indirectly added "assert a1 != a2")
    "are these atoms (or singlets) already directly bonded?"
    ## return a2 in a1.neighbors()
    return not not find_bond(a1, a2)

def find_bond(a1, a2): #bruce 050502; there might be an existing function in some other file, to merge this with
    "If a1 and a2 are bonded, return their Bond object; if not, return None."
    assert a1 != a2
    for bond in a1.bonds:
        if bond.atom1 == a2 or bond.atom2 == a2:
            return bond
    return None

def bond_atoms_oldversion(at1,at2): #bruce 050502 renamed this from bond_atoms; it's called from the newer version of bond_atoms
    """Make a new bond between atoms at1 and at2 (and add it to their lists of bonds),
    if they are not already bonded; if they are already bonded do nothing. Return None.
    (The new bond object, if one is made, can't be found except by scanning the bonds
    of one of the atoms.)
       If at1 == at2, this is an error; print a warning and do nothing.
       This increases the number of bonds on each atom (when it makes a new bond) --
    it never removes any singlets. Therefore it is mostly for low-level use.
    It could be called directly, but is usually called via the method molecule.bond,
    purely for historical reasons.
    """
    # bruce 041109 split this out of molecule.bond. Since it's the only caller of
    # Bond.__init__, what it does to the atoms could (and probably should) be put
    # inside the constructor. However, it should not simply be replaced with calls
    # to the constructor, in case we someday want it to return the bond which it
    # either makes (as the constructor does) or doesn't make (when the atoms are
    # already bonded). The test for a prior bond makes more sense outside of the
    # Bond constructor.
    if at1 == at2: #bruce 041119, partial response to bug #203
        print "BUG: bond_atoms was asked to bond %r to itself." % at1
        print "Doing nothing (but further bugs may be caused by this)."
        print_compact_stack("stack when same-atom bond attempted: ")
        return

    b = Bond(at1,at2) # (this does all necessary invals)
    
    #bruce 041029 precautionary change -- I find in debugging that the bond
    # can be already in one but not the other of at1.bonds and at2.bonds,
    # as a result of prior bugs. To avoid worsening those bugs, we should
    # change this... but for now I'll just print a message about it.
    #bruce 041109: when this happens I'll now also remove the obsolete bond.
    if (b in at1.bonds) != (b in at2.bonds):
        print "fyi: debug: for new bond %r, (b in at1.bonds) != (b in at2.bonds); removing old bond" % b
        try:
            at1.bonds.remove(b)
        except:
            pass
        try:
            at2.bonds.remove(b)
        except:
            pass
    if not b in at2.bonds:
        at1.bonds += [b]
        at2.bonds += [b]
    else:
        # [bruce comment 041115: I don't know if this ever happens,
        #  or if it's a good idea for it to be allowed, but it is allowed.
        #  #e should it inval the old bond? I think so, but didn't add that.
        #  later: it happens a lot when entering Extrude; guess: mol.copy copies
        #  each internal bond twice (sounds right, but I did not verify this).]
        pass
        
    return

#bruce 050429: preliminary plan for higher-valence bonds (might need a better term for that):
#
# - Bond objects continue to compare equal when on same pair of atoms (even if they have a
# different valence), and (partly by means of this -- probably it's a kluge) they continue
# to allow only one Bond between any two atoms (two real atoms, or one real atom and one singlet).
#
# - I don't think we need to change anything basic about "internal vs external bonds",
# coordinates, basic inval/draw schemes (except to properly draw new kinds of bonds),
# etc. (Well, not due to bond valence -- we might change those things for other reasons.)
#
# - Each Bond object has a valence. Atoms often sum the valences of their bonds
# and worry about this, but they no longer "count their bonds" -- at least not as a
# substitute for summing the valences. (To prevent this from being done by accident,
# we might even decide that their list of bonds is not really a list, at least temporarily
# while this is being debugged. #?)
#
# This is the first time bonds have any state that needs to be saved,
# except for their existence between their two atoms. This will affect mmpfile read/write,
# copying of molecules (which needs rewriting anyway, to copy jigs/groups/atomsets too),
# lots of things about depositMode, maybe more.
#
# - Any bond object can have its valence change over time (just as the coords,
# elements, or even identities of its atoms can also change). This makes it a lot
# easier to write code which modifies chemical structures in ways which preserve (some)
# bonding but with altered valence on some bonds.
#
# - Atoms might decide they fit some "bonding pattern" and reorder
# their list of bonds into a definite order to match that pattern (this is undecided #?).
# This might mean that code which replaces one bond with a same-valence bond should do it
# in the same place in the list of bonds (no idea if we even have any such code #k).
#
# - We might also need to "invalidate an atom's bonding pattern" when we change anything
# it might care about, about its bonds or even its neighboring elements (two different flags). #?
#
# - We might need to permit atoms to have valence errors, either temporarily or permanently,
# and keep track of this. We might distinguish between "user-permitted" or even "user-intended"
# valence errors, vs "transient undesired" valence errors which we intend to automatically
# quickly get rid of. If valence errors can be long-lasting, we'll want to draw them somehow.
# 
# - Singlets still require exactly one bond (unless they've been killed), but it can have
# any valence. This might affect how they're drawn, how they consider forming new bonds
# (in extrude, fuse chunks, depositMode, etc), and how they're written into sim-input mmp files.
#
# - We represent the bond valence as an integer (6 times the actual valence), since we don't
# want to worry about roundoff errors when summing and comparing valences. (Nor to pay the speed
# penalty for using exactly summable python objects that pretend to have the correct numeric value.)
#
# An example of what we don't want to have to worry about:
#
#   >>> 1/2.0 + 1/3.0 + 1/6.0
#   0.99999999999999989
#   >>> _ >= 1.0
#   False
#
# We do guarantee to all code using these bond-valence constants that they can be subtracted
# and compared as numbers -- i.e. that they are "proportional" to the numeric valence.
# Some operations transiently create bonds with unsupported values of valence, especially bonds
# to singlets, and this is later cleaned up by the involved atoms when they update their bonding
# patterns, before those bonds are ever drawn. Except for bugs or perhaps during debugging,
# only standard-valence bonds will ever be drawn, or saved in files, or seen by most code.

# ==

# Bond valence constants -- exact ints, 6 times the numeric valence they represent.
# If these need an order, their standard order is the same as the order of their numeric valences
# (as shown here).  ###e move these into constants.py? maybe not...

V_SINGLE = 6 * 1
V_GRAPHITE = 6 * 4/3  # (this can't be written 6 * (1+1/3) or 6 * (1+1/3.0) - first one is wrong, second one is not an exact int)
V_AROMATIC = 6 * 3/2
V_DOUBLE = 6 * 2
V_TRIPLE = 6 * 3

BOND_VALENCES = [V_SINGLE, V_GRAPHITE, V_AROMATIC, V_DOUBLE, V_TRIPLE]
BOND_MMPRECORDS = ['bond1', 'bondg', 'bonda', 'bond2', 'bond3'] # some code assumes these all start with "bond"

BOND_LETTERS = ['?'] * (V_TRIPLE+1)
for v6,mmprec in zip(BOND_VALENCES,BOND_MMPRECORDS):
    BOND_LETTERS[v6] = mmprec[4] # '1','g',etc
BOND_LETTERS[0] = '0' # see comment in Bond.draw
BOND_LETTERS = "".join(BOND_LETTERS)
    ## print "BOND_LETTERS:",BOND_LETTERS # 0?????1?ga??2?????3

# == helper functions related to bonding (I might move these lower in the file #e)

def bond_atoms(a1, a2, vnew = None, s1 = None, s2 = None, no_corrections = False):
    """Bond atoms a1 and a2 by making a new bond of valence vnew (which must be one
    of the constants in chem.BOND_VALENCES, not a numerically expressed valence).
    The new bond is returned. If for some reason it can't be made, None is returned
    (but if that can happen, we should revise the API so an error message can be returned).
    Error if these two atoms are already bonded.
       If provided, s1 and s2 are the existing singlets on a1 and a2 (respectively)
    whose valence should be reduced (or eliminated, in which case they are deleted)
    to provide valence for the new bond. (If they don't have enough, other adjustments
    will be made; this function is free to alter, remove, or replace any existing
    singlets on either atom.)
       For now, this function will never alter the valence of any existing bonds
    to real atoms. If necessary, it will introduce valence errors on a1 and/or a2.
    (Or if they already had valence errors, it might remove or alter those.)
       If no_corrections = True, this function will not alter singlets on a1 or a2,
    but will either completely ignore issues of total valence of these atoms, or will
    limit itself to tracking valence errors or setting related flags (this is undecided).
    (This might be useful for code which builds new atoms rather than modifying
    existing ones, such as when reading mmp files or copying existing atoms.)
       vnew should always be provided (to get the behavior documented here).
    For backwards compatibility, when vnew is not provided, this function calls the
    old code [pre-higher-valence-bonds, pre-050502] which acts roughly as if
    vnew = V_SINGLE, s1 = s2 = None, no_corrections = True, except that it returns
    None rather than the newly made bond, and unlike this function doesn't mind
    if there's an existing bond, but does nothing in that case; this behavior might
    be relied on by the current code for copying bonds when copying a chunk, which
    might copy some of them twice.
       Using the old bond_atoms code by not providing vnew is deprecated,
    and might eventually be made impossible after all old calling code is converted
    for higher-valence bonds.
    """
    if vnew == None:
        assert s1 == s2 == None
        assert no_corrections == False
        bond_atoms_oldversion( a1, a2)
        return
    # quick hack for new version, using old version
    assert vnew in BOND_VALENCES
    assert not bonded(a1,a2)
    bond_atoms_oldversion(a1,a2)
    bond = find_bond(a1,a2) ###IMPLEM
    assert bond
    if vnew != V_SINGLE:
        bond.increase_valence_noupdate( vnew - V_SINGLE)
    if not no_corrections:
        if s1:
            s1.singlet_reduce_valence_noupdate(vnew)
        if s2:
            s2.singlet_reduce_valence_noupdate(vnew) ###k
        a1.update_valence() ###k
        a2.update_valence()
    return bond

def bond_v6(bond):
    "Return bond.v6. Useful in map, filter, etc."
    return bond.v6

# ==

#bruce 041109:
# Capitalized name of class Bond, so we can find all uses of it in the code;
# as of now there is only one use, in bond_atoms (used by molecule.bond).
# I also rewrote lots of the code in class Bond.

class Bond:
    """A Bond is essentially a record pointing to two atoms
    (either one of which might be a real atom or a "singlet"),
    representing a bond between them if it also occurs in atom.bonds
    for each atom. It should occur in both or neither of atom.bonds
    of its two atoms, except transiently.
       The two atoms in a bond should always be different objects.
       We don't support more than one bond between the same two
    atoms; trying to add the second one will do nothing, because
    of Bond.__eq__. We don't yet support double or triple bonds...
    but [bruce 050429 addendum] soon after Alpha 5 we'll start
    supporting those, and I'll start prototyping them right now --
    DO NOT COMMIT until post-Alpha5.
       Bonds have a private member 'key' so they can be compared equal
    whenever they involve the same pair of atoms (in either order).
       Bonds sometimes store geometric info used to draw them; see
    the method setup_invalidate, which must be called when the atoms
    are changed in certain ways. Bonds don't store any selection
    state or display-mode state, and they record no info about the
    bonded molecules (but each bonded atom knows its molecule).
       Bonds are called "external" if they connect atoms in two
    different molecules, or "internal" if they connect two atoms
    in the same molecule. This affects what kind of info is
    invalidated by the private method invalidate_bonded_mols, which
    should be called by internal code whenever the bond is actually
    added to or removed from its atoms
    (or is probably about to be added or removed).
       Bonds can be removed from their atoms by Bond.bust, and then
    forgotten about (no need to kill or otherwise explicitly destroy
    them after they're not on their atoms).
    """
    
    def __init__(self, at1, at2, v6 = V_SINGLE): # no longer also called from self.rebond()
        """create a bond from atom at1 to atom at2.
        the key created will be the same whichever order the atoms are
        given, and is used to compare bonds.
        [further comments by bruce 041029:]
        Private method (that is, creating of bond objects is private, for
        affected molecules and/or atoms). Note: the bond is not actually added
        to the atoms' molecules! Caller must do that. But [new feature 041109]
        we will do all necessary invalidations, in case the new bond is indeed
        added to those atoms (as I think it always will be in the current code).
        """
        self.atom1 = at1 ###k are these public attributes? For now I'll assume yes. [bruce 050502]
        self.atom2 = at2
        self.v6 = v6 # bond-valence times 6, as exact int; a public attribute
        assert v6 in BOND_VALENCES
        ## self.picked = 0 # bruce 041029 removed this since it seems unused
        self.changed_atoms()
        self.invalidate_bonded_mols() #bruce 041109 new feature

    def set_v6(self, v6):
        assert v6 in BOND_VALENCES
        self.v6 = v6
        #e update geometric things?? tell the atoms too??
        if self.atom1.molecule == self.atom2.molecule:
            # we're in that molecule's display list
            self.atom1.molecule.changeapp(0)
        return

    def numeric_valence(self): # has a long name so you won't be tempted to use it when you should use .v6
        return self.v6 / 6.0
    
    def changed_atoms(self):
        """Private method to call when the atoms assigned to this bond are changed.
        WARNING: does not call setup_invalidate(), though that would often also
        be needed, as would invalidate_bonded_mols() both before and after the change.
        """
        at1 = self.atom1
        at2 = self.atom2
        assert at1 != at2
        self.key = 65536*min(at1.key,at2.key)+max(at1.key,at2.key)
        #bruce 050317: debug warning for interpart bonds, or bonding killed atoms/chunks,
        # or bonding to chunks not yet added to any Part (but not warning about internal
        # bonds, since mol.copy makes those before a copied chunk is added to any Part).
        #   This covers new bonds (no matter how made) and the .rebond method.
        #   Maybe this should be an actual error, or maybe it should set a flag so that
        # involved chunks are checked for interpart bonds when the user event is done
        # (in case caller plans to move the chunks into the same part, but hasn't yet).
        # It might turn out this happens a lot (and is not a bug), if callers make a
        # new chunk, bond to it, and only then add it into the tree of Nodes.
        if platform.atom_debug and at1.molecule != at2.molecule:
            if (not at1.molecule.assy) or (not at2.molecule.assy):
                print_compact_stack( "atom_debug: bug?: bonding to a killed chunk(?); atoms are: %r, %r" % (at1,at2))
            elif (not at1.molecule.part) or (not at2.molecule.part): # assume false means None, maybe untrue if bugs happen
                if 0: #bruce 050321 this happens a lot when reading an mmp file, so disable it for now
                    print_compact_stack( "atom_debug: bug or fyi: one or both Parts None when bonding atoms: %r, %r" % (at1,at2))
            elif at1.molecule.part != at2.molecule.part:
                print_compact_stack( "atom_debug: likely bug: bonding atoms whose parts differ: %r, %r" % (at1,at2))
        return
    
    def invalidate_bonded_mols(self): #bruce 041109
        """Private method to call when a bond is made or destroyed;
        knows which kinds of bonds are put into a display list by molecule.draw
        (internal bonds) or put into into mol.externs (external bonds),
        though this knowledge should ideally be private to class molecule.
        """
        # assume mols are not None (they might be _nullMol, that's ok)
        mol1 = self.atom1.molecule
        mol2 = self.atom2.molecule
        if mol1 != mol2:
            # external bond
            mol1.invalidate_attr('externs')
            mol2.invalidate_attr('externs')
        else:
            # internal bond
            mol1.havelist = 0
        return

    def setup_invalidate(self):
        """Semi-private method for bonds. Invalidates cached geometric values
        related to drawing the bond.
         This must be called whenever the position or element of either bonded
        atom is changed, or when either atom's molecule changes if this affects
        whether it's an external bond (since the coordinate system used for drawing
        is different in each case).
         (FYI: It need not be called for other changes that might affect bond
        appearance, like disp or color of bonded molecules, though for internal
        bonds, the molecule's .havelist should be reset when those things change.)
          Note that before the "inval/update" revisions [bruce 041104],
        self.setup() (the old name for this method, from point of view of callers)
        did the recomputation now done on demand by __setup_update; now this method
        only does the invalidation which makes sure that recomputation will happen
        when it's needed.
        """
        # just delete all the attrs recomputed by self.__setup_update()
        try:
            del self.c1
        except AttributeError:
            pass # assume other attrs are also not there
        else:
            # assume other attrs are also there
            del self.c2, self.center, self.a1pos, self.a2pos, self.toolong
        # For internal bonds, or bonds that used to be internal,
        # callers need to have reset havelist of affected mols,
        # but the changes in atoms that required them to call setup_invalidate
        # mean they should have done that anyway (except for bond making and
        # breaking, in this file, which does this in invalidate_bonded_mols).
        # Bruce 041207 scanned all callers and concluded they do this as needed,
        # so I'm removing the explicit resets of havelist here, which were often
        # more than needed since they hit both mols of external bonds.
        # This change might speed up some redraws, esp. in move or deposit modes.
        return

    def __setup_update(self):
        """Private method. Before bruce 041104 this was called self.setup()
        and was called more widely; now the method of that name just invalidates
        the same attrs we recompute, by deleting them.
           This method is only called by __getattr__ when we need to recompute one
        or more of certain attributes, to set up the bond for drawing, or to
        compute the unbonding point with bond.ubp() (used to make replacement
        singlets in atom.unbond and atom.kill methods, even if they'll be
        discarded right away as all atoms in some big chunk are killed 1 by 1).
           We store all attributes we compute in the same coordinate system,
        which is mol-relative (basecenter/quat) for internal bonds, but absolute
        for external bonds.
           The specific attributes we recompute (and set, until next invalidated)
        are: a1pos, a2pos (positions of the atoms); c1, c2, and center (points
        along the bond useful for drawing it); toolong (flag) saying whether bond
        is too long. (Before 041112 there was no toolong flag, but center was None
        for long bonds.)
           As of 041201 we'll no longer recompute atpos or basepos if they are
        invalid, so that atom.kill (our caller via unbond and ubp), which
        invalidates them, won't also recompute them.
        """
        # [docstring revised, and inval/update scheme added, by bruce 041104]
        # [docstring improved, and code revised to not recompute basepos, 041201]
        if self.atom1.molecule != self.atom2.molecule:
            # external bond; use absolute positions for all attributes.
            self.a1pos = self.atom1.posn()
            self.a2pos = self.atom2.posn()
        else:
            # internal bond; use mol-relative positions for all attributes.
            # Note 1: this means any change to mol's coordinate system
            # (basecenter and quat) requires calling setup_invalidate
            # in this bond! That's a pain (and inefficient), so I might
            # replace it by a __getattr__ mol-coordsys-version-number check...
            # ##e [bruce 041115]
            self.a1pos = self.atom1.baseposn()
            self.a2pos = self.atom2.baseposn()
        vec = self.a2pos - self.a1pos
        leng = 0.98 * vlen(vec)
        vec = norm(vec)
        # (note: as of 041217 rcovalent is always a number; it's 0.0 for Helium,
        #  etc, so the entire bond is drawn as if "too long".)
        rcov1 = self.atom1.element.rcovalent
        rcov2 = self.atom2.element.rcovalent
        self.c1 = self.a1pos + vec*rcov1
        self.c2 = self.a2pos - vec*rcov2
        self.toolong = (leng > rcov1 + rcov2)
        self.center = (self.c1 + self.c2) / 2.0 # before 041112 this was None when self.toolong
        return

    def __getattr__(self, attr): # bond.__getattr__ #bruce 041104
        """Called when one of the attrs computed by self.__setup_update() is
        needed, but was not yet computed or was deleted since last computed
        (as our way of invalidating it). Also might be called for an arbitrary
        missing attr due to a bug in the calling code. Now that this __getattr__
        method exists, no other calls of self.__setup_update() should be needed.
        """
        if attr[0] == '_' or (not attr in ['a1pos','a2pos','c1','c2','center','toolong']):
            # unfortunately (since it's slow) we can't avoid checking this first,
            # or we risk infinite recursion due to a missing attr needed by setup
            raise AttributeError, attr # be fast since probably common for __xxx__
        self.__setup_update() # this should add the attribute (or raise an exception
          # if it's called too early while initing the bond or one of its molecules)
        return self.__dict__[attr] # raise exception if attr still missing

    def other(self, atm):
        """Given one atom the bond is connected to, return the other one
        """
        if self.atom1 == atm: return self.atom2
        assert self.atom2 == atm #bruce 041029
        return self.atom1

    def othermol(self, mol): #bruce 041123; not yet used or tested
        """Given the molecule of one atom of this bond, return the mol
        of the other one. Error if mol is not one of the bonded mols.
        Note that this implies that for an internal bond within mol,
        the input must be mol and we always return mol.
        """
        if mol == self.atom1.molecule:
            return self.atom2.molecule
        elif mol == self.atom2.molecule:
            return self.atom1.molecule
        else:
            assert mol in [self.atom1.molecule, self.atom2.molecule]
            # this always fails -- it's just our "understandable error message"
        pass
    
    def ubp(self, atom):
        """ unbond point (atom must be one of the bond's atoms) """
        #bruce 041115 bugfixed this for when mol.quat is not 1,
        # tho i never looked for or saw an effect from the bug in that case
        if atom == self.atom1:
            point = self.c1 # this might call self.__setup_update()
        else:
            assert atom == self.atom2
            point = self.c2
        # now figure out what coord system that's in
        if self.atom1.molecule != self.atom2.molecule:
            return point
        else:
            # convert to absolute position for caller
            # (note: this never recomputes basepos/atpos or modifies the mol-
            #  relative coordinate system)
            return self.atom1.molecule.base_to_abs(point)
        pass

    # "break" is a python keyword
    def bust(self):
        """Destroy this bond, modifying the bonded atoms as needed
        (by adding singlets in place of this bond -- they might overlap!),
        and invalidating the bonded molecules as needed.
        Return the added singlets as a 2-tuple.
        (This method is named 'bust' since 'break' is a python keyword.)
        If either atom is a singlet, kill that atom.
        (Note: as of 041115 bust is never called with either atom a singlet.
        If it ever is, retval remains a 2-tuple but has None in 1 or both
        places ... precise effect needs review in that case.)
        """
        # bruce 041115: bust is never called with either atom a singlet,
        # but since atom.unbond now kills singlets lacking any bonds,
        # and since not doing that would be bad, I added a note about that
        # to the docstring.
        x1 = self.atom1.unbond(self) # does all needed invals
        x2 = self.atom2.unbond(self)
        ###e do we want to also change our atoms and key to None, for safety?
        ###e check all callers and decide
        return x1, x2 # retval is new feature, bruce 041222
    
    def rebond(self, old, new):
        """Self is a bond between old (typically a singlet) and some atom A;
        replace old with new in this same bond (self),
        so that old no longer bonds to A but new does.
        Unlike some other bonding methods, the number of bonds on new increases
        by 1, since no singlet on new is removed -- new is intended to be
        a just-created atom, not one with the right number of existing bonds.
        If old is a singlet, then kill it since it now has no bonds.
        Do the necessary invalidations in self and all involved molecules.
           Warning: this can make a duplicate of an existing bond (so that
        atoms A and B are connected by two equal copies of a bond). That
        situation is an error, not supported by the code as of 041203,
        and is drawn exactly as if it was a single bond. Avoiding this is
        entirely up to the caller.
        """
        # [bruce 041109 added docstring and rewrote Josh's code:]
        # Josh said: intended for use on singlets, other uses may have bugs.
        # bruce 041109: I think that means "old" is intended to be a singlet.
        # I will try to make it safe for any atoms, and do all needed invals.
        if self.atom1 == old:
            old.unbond(self) # also kills old if it's a singlet, as of 041115
            ## if len(old.bonds) == 1: del old.molecule.atoms[old.key] --
            ## the above code removed the singlet, old, without killing it.
            self.atom1 = new
        elif self.atom2 == old:
            old.unbond(self)
            self.atom2 = new
        else:
            print "fyi: bug: rebond: %r doesn't contain atom %r to replace with atom %r" % (self, old, new)
            # no changes in the structure
            return
        # bruce 041109 worries slightly about order of the following:
        # invalidate this bond itself
        self.changed_atoms()
        self.setup_invalidate()
        # add this bond to new (it's already on A, i.e. in the list A.bonds)
        new.bonds += [self]
            #e put this in some private method on new, new.add_new_bond(self)??
            #  Note that it's intended to increase number of bonds on new,
            #  not to zap a singlet already bonded to new.
        # Invalidate molecules (of both our atoms) as needed, due to our existence
        self.invalidate_bonded_mols()
        if 1:
            # This debug code helped catch bug 232, but seems useful in general:
            # warn if this bond is a duplicate of an existing bond on A or new.
            # (Usually it will have the same count on each atom, but other bugs
            #  could make that false, so we check both.) [bruce 041203]
            A = self.other(new)
            if A.bonds.count(self) > 1:
                print "rebond bug (%r): A.bonds.count(self) == %r" % (self, A.bonds.count(self))
            if new.bonds.count(self) > 1:
                print "rebond bug (%r): new.bonds.count(self) == %r" % (self, new.bonds.count(self))
        return

    def __eq__(self, ob):
        return ob.key == self.key

    def __ne__(self, ob):
        # bruce 041028 -- python doc advises defining __ne__
        # whenever you define __eq__
        return not self.__eq__(ob)

    def draw(self, glpane, dispdef, col, level):
        """Draw the bond. Note that for external bonds, this is called twice,
        once for each bonded molecule (in arbitrary order)
        (and is never cached in either mol's display list);
        each of these calls gets dispdef, col, and level from a different mol.
        [bruce, 041104, thinks that leads to some bugs in bond looks.]
        Bonds are drawn only in certain display modes (CPK, LINES, TUBES).
        The display mode is inherited from the atoms or molecule (as passed in
         via dispdef from the calling molecule -- this might cause bugs if some
         callers change display mode but don't set havelist = 0, but maybe they do).
        Lines or tubes change color from atom to atom, and are red in the middle
        for long bonds. CPK bonds are drawn in the calling molecule's color or
        in the constant bondColor (which is light gray).
        """
        #bruce 041104 revised docstring, added comments about possible bugs.
        # Note that this code depends on finding the attrs toolong, center,
        # a1pos, a2pos, c1, c2, as created by self.__setup_update().
        # As of 041109 this is now handled by bond.__getattr__.
        # The attr toolong is new as of 041112.
        
        color1 = col or self.atom1.element.color
        color2 = col or self.atom2.element.color

        disp=max(self.atom1.display, self.atom2.display)
        if disp == diDEFAULT: disp= dispdef
        if disp == diLINES:
            if not self.toolong:
                drawline(color1, self.a1pos, self.center)
                drawline(color2, self.a2pos, self.center)
            else:
                drawline(color1, self.a1pos, self.c1)
                drawline(color2, self.a2pos, self.c2)
                drawline(red, self.c1, self.c2)
        if disp == diCPK:
            drawcylinder(col or bondColor, self.a1pos, self.a2pos, 0.1)
        if disp == diTUBES:
            v1 = self.atom1.display != diINVISIBLE
            v2 = self.atom2.display != diINVISIBLE
            ###e bruce 041104 suspects v1, v2 wrong for external bonds, needs
            # to look at each mol's .hidden (but this is purely a guess)
            if not self.toolong:
                if v1:
                    drawcylinder(color1, self.a1pos, self.center, TubeRadius)
                if v2:
                    drawcylinder(color2, self.a2pos, self.center, TubeRadius)
                if not (v1 and v2):
                    drawsphere(black, self.center, TubeRadius, level)
#                print "draw: bond 1---2: ", self.a1pos, self.a2pos    
            else:
                drawcylinder(red, self.c1, self.c2, TubeRadius)
#                print "draw: bond c1--c2: ", self.c1, self.c2    
                if v1:
                    drawcylinder(color1, self.a1pos, self.c1, TubeRadius)
#                    print "draw: bond a1---c1: ", self.a1pos, self.c1    
                else:
                    drawsphere(black, self.c1, TubeRadius, level)
                if v2:
                    drawcylinder(color2, self.a2pos, self.c2, TubeRadius)
#                    print "draw: bond a2---c2: ", self.a2pos, self.c2    
                else:
                    drawsphere(black, self.c2, TubeRadius, level)
        if self.v6 != V_SINGLE or platform.atom_debug: # debug_bonds #####@@@@@
            glDisable(GL_LIGHTING)
            ## glDisable(GL_DEPTH_TEST)
            glPushMatrix()
            font = QFont( QString("Times"), 10)#QFont(QString("Helvetica"), 12, QFont.Normal) ###E optimize this, keep in glpane
            glpane.qglColor(QColor(75, 75, 75))
            p = self.center + glpane.out * 0.6
                ###WRONG -- depends on rotation when display list is made! But quite useful for now.
            v6 = self.v6
            try:
                ltr = BOND_LETTERS[v6]
                    # includes special case of '0' for v6 == 0,
                    # which should only show up for transient states that are never drawn, except in case of bugs
            except IndexError: # should only show up for transient states...
                if v6 < 0:
                    ltr = '-'
                else:
                    ltr = '+'
            glpane.renderText(p[0], p[1], p[2], QString(ltr), font) #k need explicit QString??
            glPopMatrix()
            ## glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
        return # from Bond.draw

    # write to a povray file:  draw a single bond [never reviewed by bruce]
    # [note: this redundantly computes attrs like __setup_update computes for
    #  draw, and instead we should just use those attrs, but I did not make
    #  this change since there is a current bug report which someone might
    #  fix by altering povpoint and the V(1,1,-1) kluges in here,
    #  and I want to avoid a cvs merge conflict. When this is fixed,
    #  note that I have changed self.center and added self.toolong; see
    #  self.draw() for details. -- bruce 041112 ###e]
    def writepov(self, file, dispdef, col):
       ##Huaicai 1/15/05: It seems the attributes from __setup__update() is not correct,
       ## at least for pov file writing, so compute it here locally. To fix bug 346,347
        disp=max(self.atom1.display, self.atom2.display)
        if disp == diDEFAULT: disp= dispdef
        color1 = col or self.atom1.element.color
        color2 = col or self.atom2.element.color
        
        a1pos = self.atom1.posn()
        a2pos = self.atom2.posn()
        
        vec = a2pos - a1pos
        leng = 0.98 * vlen(vec)
        vec = norm(vec)
        # (note: as of 041217 rcovalent is always a number; it's 0.0 for Helium,
        #  etc, so the entire bond is drawn as if "too long".)
        rcov1 = self.atom1.element.rcovalent
        rcov2 = self.atom2.element.rcovalent
        c1 = a1pos + vec*rcov1
        c2 = a2pos - vec*rcov2
        toolong = (leng > rcov1 + rcov2)
        center = (c1 + c2) / 2.0 # before 041112 this was None when self.toolong
        
        
        if disp<0: disp= dispdef
        if disp == diLINES:
            file.write("line(" + povpoint(a1pos) +
                       "," + povpoint(a2pos) + ")\n")
        if disp == diCPK:
            file.write("bond(" + povpoint(a1pos) +
                       "," + povpoint(a2pos) + ")\n")
        if disp == diTUBES:
        ##Huaicai: If rcovalent is close to 0, like singlets, avoid 0 length 
        ##             cylinder written to a pov file    
            DELTA = 1.0E-5
            isSingleCylinder = False
            if  self.atom1.element.rcovalent < DELTA:
                    col = color2
                    isSingleCylinder = True
            if  self.atom2.element.rcovalent < DELTA:
                    col = color1
                    isSingleCylinder = True
            if isSingleCylinder:        
                file.write("tube3(" + povpoint(a1pos) + ", " + povpoint(a2pos) + ", " + stringVec(col) + ")\n")
            else:      
                if not self.toolong:
                        file.write("tube2(" + povpoint(a1pos) +
                           "," + stringVec(color1) +
                           "," + povpoint(center) + "," +
                           povpoint(a2pos) + "," +
                           stringVec(color2) + ")\n")
                else:
                        file.write("tube1(" + povpoint(a1pos) +
                           "," + stringVec(color1) +
                           "," + povpoint(c1) + "," +
                           povpoint(c2) + "," + 
                           povpoint(a2pos) + "," +
                           stringVec(color2) + ")\n")

    def __str__(self):
        return str(self.atom1) + " <--> " + str(self.atom2)

    def __repr__(self):
        return str(self.atom1) + "::" + str(self.atom2)

    pass # end of class Bond

# ==

# class molecule used to be defined here, but now it's in chunk.py. [bruce 041118]

# for the sake of other files which still look for class molecule in this file,
# we'll import it here (this might not work if done at the top of this file):

from chunk import *

# end of chem.py
