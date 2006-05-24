# Copyright (c) 2005-2006 Nanorex, Inc.  All rights reserved.
'''
bond_utils.py

Helper functions for bonds, including UI code.

$Id$

History:

created by bruce 050705 to help with higher-order bonds for Alpha6.

050901 bruce used env.history in some places.
'''
__author__ = "bruce"


from VQT import Q
from constants import noop
from bond_constants import *
import env
from HistoryWidget import orangemsg

def intersect_sequences(s1, s2):
    return filter( lambda s: s in s2, s1)

def possible_bond_types(bond):
    """Return a list of names of possible bond types for the given bond,
    based on its atoms' current elements and atomtypes.
       This list is never empty since single bonds are always possible
    (even if they always induce valence errors, e.g. for H bonded to O(sp2) or in O2).
       For warnings about some choices of bond type (e.g. S=S), see the function bond_type_warning.
       [###e we might extend this to optionally also permit bonds requiring other atomtypes
    if those are reachable by altering only open bonds on this bond's actual atoms.]
       Warning: this ignores geometric issues, so it permits double bonds even if they
    would be excessively twisted, and it ignores bond length, bond arrangement in space
    around each atom, etc.
    """
    s1 = bond.atom1.atomtype.permitted_v6_list
    s2 = bond.atom2.atomtype.permitted_v6_list
    s12 = intersect_sequences( s1, s2 )
        #e could be faster (since these lists are prefixes of a standard order), but doesn't need to be
    return map( btype_from_v6, s12)
    
#obs, partly:
#e should we put element rules into the above possible_bond_types, or do them separately?
# and should bonds they disallow be shown disabled, or not even included in the list?
# and should "unknown" be explicitly in the list?

def bond_type_warning(bond, btype): # 050707
    """Return a warning (short text suitable to be added to menu item text), or "" for no warning,
    about the use of btype (bond type name) for bond.
    This can be based on its atomtypes or perhaps on more info about the surroundings
    (#e we might need to add arguments to pass such info).
       Presently, this only warns about S=S being unstable, and about bonds whose type could not
    permit both atoms (using their current atomtypes) to have the right valence
    regardless of their other bonds (which only happens now when they have no other bonds).
       This might return warnings for illegal btypes, even though it's not presently called
    for illegal btypes for the given bond. It doesn't need to return any warning for illegal btypes.
    """
    atype1 = bond.atom1.atomtype
    atype2 = bond.atom2.atomtype
    if btype == 'double' and atype1.is_S_sp2 and atype2.is_S_sp2:
        return "unstable"
    elif btype == 'single' and (atype1.bond1_is_bad or atype2.bond1_is_bad):
        return "bad valence"
    elif btype != 'triple' and (atype1.is_N_sp or atype2.is_N_sp):
        return "bad valence"
    # if there are any other numbonds=1 atoms which show up here, they should be valence-checked too (generalizing the above)
    # (which might be easiest if atomtype stores a "valence-permitted btypes" when numbonds is 1), but I don't think there are others
    return ""
    
def bond_menu_section(bond, quat = Q(1,0,0,0)):
    """Return a menu_spec subsection for displaying info about a highlighted bond,
    changing its bond_type, offering commands about it, etc.
    If given, use the quat describing the rotation used for displaying it
    to order the atoms in the bond left-to-right (e.g. in text strings).
    """
    res = []
    res.append(( bonded_atoms_summary(bond, quat = quat), noop, 'disabled' ))
    res.extend( bond_type_menu_section(bond) )
    return res

def bond_type_menu_section(bond): #bruce 050716; replaces bond_type_submenu_spec for Alpha6
    """Return a menu_spec for changing the bond_type of this bond
    (as one or more checkmark items, one per permitted bond-type given the atomtypes),
    or if the bond-type is unchangeable, a disabled menu item for displaying the type
    (which looks the same as when the bond type is changeable, except for being disabled).
    (If the current bond type is not permitted, it's still present and checked, but disabled,
     and it might have a warning saying it's illegal.)
    """
    v6 = bond.v6
    btype_now = btype_from_v6(v6)
    poss = possible_bond_types(bond) # a list of strings which are bond-type names
    ##e could put weird ones (graphitic, carbomeric) last and/or in parens, in subtext below
    types = list(poss)
    if btype_now not in poss:
        types.append(btype_now) # put this one last, since it's illegal; warning for it is computed later
    assert len(types) > 0
    # types is the list of bond types for which to make menu items, in order;
    # now make them, and figure out which ones are checked and/or disabled;
    # we disable even legal ones iff there is only one bond type in types
    # (which means, if current type is illegal, the sole legal type is enabled).
    disable_legal_types = (len(types) == 1)
    res = []
    for btype in types: # include current value even if it's illegal
        subtext = "%s bond" % btype # this string might be extended below
        checked = (btype == btype_now)
        command = ( lambda arg1=None, arg2=None, btype=btype, bond=bond: apply_btype_to_bond(btype, bond) )
        if btype not in poss:
            # illegal btype (note: it will be the current one, and thus be the only checked one)
            warning = "illegal"
            disabled = True
        else:
            # legal btype
            warning = bond_type_warning(bond, btype) # might be "" (or None??) for no warning
            disabled = disable_legal_types
                # might change this if some neighbor bonds are locked, or if we want to show non-possible choices
        if warning:
            subtext += " (%s)" % warning
        res.append(( subtext, command,
                         disabled and 'disabled' or None,
                         checked and 'checked' or None ))
    ##e if >1 legal value, maybe we should add a toggleable checkmark item to permit "locking" the bond to its current bond type
    return res

##def bond_type_submenu_spec(bond): #bruce 050705 (#e add options??); probably not used in Alpha6
##    """Return a menu_spec for changing the bond_type of this bond,
##    or if that is unchangeable, a disabled menu item for displaying the type.
##    """
##    v6 = bond.v6
##    btype0 = btype_from_v6(v6)
##    poss = possible_bond_types(bond) # a list of strings which are bond-type names
##    ##e could put weird ones (graphitic, carbomeric) last and/or in parens, in subtext below
##    maintext = 'Bond Type: %s' % btype0
##    if btype0 not in poss or len(poss) > 1:
##        # use the menu
##        submenu = []
##        for btype in poss: # don't include current value if it's illegal
##            subtext = btype
##            warning = bond_type_warning(bond, btype)
##            if warning:
##                subtext += " (%s)" % warning
##            command = ( lambda arg1=None, arg2=None, btype=btype, bond=bond: apply_btype_to_bond(btype, bond) )
##            checked = (btype == btype0)
##            disabled = False # might change this if some neighbor bonds are locked, or if we want to show non-possible choices
##            submenu.append(( subtext, command,
##                             disabled and 'disabled' or None,
##                             checked and 'checked' or None ))
##        ##e if >1 legal value could add checkmark item to permit "locking" this bond type
##        return ( maintext, submenu)
##    else:
##        # only one value is possible, and it's the current value -- just show it
##        return ( maintext, noop, 'disabled' )
##    pass


#bruce 060523 unfinished aspects of new more permissive bondtype changing: ####@@@@
# - verify it can't be applied to open bonds from dashboard tools (since not safe yet)
# - make sure changing atomtypes doesn't remove bond (if open)
#   (possible implem of that: maybe remove it, set_atomtype, then add it back, then remake singlets?)
# - then it's safe to let bond cmenu have more entries (since they might be open bonds)

def apply_btype_to_bond(btype, bond):
    """Apply the given bond-type name (e.g. 'single') to the given bond, iff this is permitted by its atomtypes
    (or, new feature 060523, if it's permitted by its real atoms' possible atomtypes and their number of real bonds),
    and do whatever inferences are presently allowed [none are implemented as of 050727].
    Emit an appropriate history message. Do appropriate invals/updates.
    [#e should the inference policy and/or some controlling object be another argument? Maybe even a new first arg 'self'?]
    """
    # Note: this can be called either from a bond's context menu, or by using the Build mode dashboard tool to click on bonds
    # and immediately change their types.
    v6 = v6_from_btype(btype)
    from HistoryWidget import quote_html #e need to clean up from where to import this, orangemsg, etc
    oldname = quote_html( str(bond) )
    def changeit(also_atypes = None):
        if v6 == bond.v6:
            env.history.message( "bond type of %s is already %s" % (oldname, btype))
        else:
            if also_atypes:
                # change atomtypes first (not sure if doing this first matters)
                atype1, atype2 = also_atypes
                def changeatomtype(atom, atype):
                    if atom.atomtype is not atype:
                        msg = "changed %r from %s to %s" % (atom, atom.atomtype.name, atype.name )
                        env.history.message(msg)
                        atom.set_atomtype(atype)
                        ###### note: if we're an open bond, we have to prevent this process from removing us!!!!!
                        # (this is nim, so we're not yet safe to offer on open bonds.)
                        pass
                    return # from changeatomtype
                changeatomtype(bond.atom1, atype1)
                changeatomtype(bond.atom2, atype2)
            bond.set_v6(v6) # this doesn't affect anything else or do any checks ####k #####@@@@@ check that
            ##e now do inferences on other bonds
            bond.changed() ###k needed?? maybe it's now done by set_v6??
            env.history.message( "changed bond type of %s to %s" % (oldname, btype))
            ###k not sure if it does gl_update when needed... how does menu use of this do that?? ###@@@
        return # from changeit
    poss = possible_bond_types(bond)
    if btype in poss:
        changeit()
        return
    # otherwise figure out if we can change the atomtypes to make this work.
    # (The following code is predicted to work for either real or open bonds.)
    permitted1 = bond.atom1.permitted_btypes_for_bond(bond) # dict from v6 to permitting atomtypes
    permitted2 = bond.atom2.permitted_btypes_for_bond(bond)
    poss_v6 = intersect_sequences(permitted1.keys(), permitted2.keys()) # purpose of having whole sequence is just the error message
    poss_v6.sort() # smallest bond order first
    poss = map( btype_from_v6, poss_v6)
    if btype in poss:
        atype1 = best_atype(bond.atom1, permitted1[v6])
        atype2 = best_atype(bond.atom2, permitted2[v6])
        changeit((atype1, atype2))
        return
    env.history.message( orangemsg( "can't change bond type of %s to %s -- permitted types are %s" % (oldname, btype, poss)))
    return # from apply_btype_to_bond

def best_atype(atom, atomtypes = None): #bruce 060523
    """Which atomtype for atom is best, among the given or possible ones,
    where best means the fewest number of bondpoints need removing to get to it?
    (Break ties by favoring current one (never matters as presently called, 060523)
    or those earlier in the list.)
    """
    # I don't think we have to consider types for which bondpoints would be *added*...
    # but in case we do, let those be a last resort, but for them, best means fewest added.
    # Note: this is related to Atom.best_atomtype_for_numbonds, but that has a quite different cost function
    # since it assumes it's not allowed to change the number of bondpoints, only to compare severity of valence errors.
    atomtypes = atomtypes or atom.element.atomtypes
    atomhas = len(atom.bonds)
    def cost(atype):
        atypewants = atype.numbonds
        nremove = atomhas - atypewants
        if nremove >= 0:
            cost1 = nremove
        else:
            nadd = - nremove
            cost1 = 100 + nadd
        if atype is atom.atomtype:
            cost2 = -1
        else:
            cost2 = atomtypes.index(atype)
        return (cost1, cost2)
    costitems = [(cost(atype), atype) for atype in atomtypes]
    costitems.sort()
    return costitems[0][1]

# end
