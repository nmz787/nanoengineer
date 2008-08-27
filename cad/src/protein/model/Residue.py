# Copyright 2008 Nanorex, Inc.  See LICENSE file for details. 

"""
Residue.py -- Residue class implementation.


@author: Piotr
$Id$
@copyright: 2008 Nanorex, Inc.  See LICENSE file for details.

History:

piotr 082708: Re-factored the Residue class out of Protein.py file.
"""

# Renamed this to "Residue" (which is a proper spelling, compared to "Residue",
# as Eric D has pointed out in his email).

# piotr 082008: This class should be re-factored and moved to its own file.
# piotr 082708: The re-factoring completed.

from protein.model.Protein import AA_3_TO_1

# PDB atom name sets for chiral angles for amino acid side chains
chi_angles = { "GLY" : [ None, 
                         None, 
                         None, 
                         None ],
               "ALA" : [ None,
                         None, 
                         None,
                         None ],
               "SER" : [ [ "N"  , "CA" , "CB" , "OG"  ],
                         None,
                         None,
                         None ],
               "GLU" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         [ "CA" , "CB" , "CG" , "CD"  ],
                         [ "CB" , "CG" , "CD" , "OE1" ],
                         None ],
               "GLN" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         [ "CA" , "CB" , "CG" , "CD"  ],
                         [ "CB" , "CG" , "CD" , "OE1" ],
                         None ],
               "ASP" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         [ "CA" , "CB" , "CG" , "OD1" ],
                         None,
                         None ],
               "ASN" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         [ "CA" , "CB" , "CG" , "OD1" ],
                         None,
                         None ],
               "CYS" : [ [ "N"  , "CA" , "CB" , "SG"  ],
                         None,
                         None,
                         None ],
               "MET" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         [ "CA" , "CB" , "CG" , "SD" ],
                         None,
                         None ],
               "THR" : [ [ "N"  , "CA" , "CB" , "CG2" ],
                         None,
                         None,
                         None ],
               "LEU" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         [ "CA" , "CB" , "CG" , "CD1" ],
                         None,
                         None ],
               "ILE" : [ [ "N"  , "CA" , "CB" , "CG1" ],
                         [ "CA" , "CB" , "CG1", "CD1" ],
                         None,
                         None ],
               "VAL" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         None,
                         None,
                         None ],
               "TRP" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         None,
                         None,
                         None ],
               "TYR" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         None,
                         None,
                         None ],
               "LYS" : [ [ "N"  , "CA" , "CB" , "OG"  ],
                         None,
                         None,
                         None ],
               "ARG" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         None,
                         None,
                         None ],
               "HIS" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         None,
                         None,
                         None ],
               "PHE" : [ [ "N"  , "CA" , "CB" , "CG"  ],
                         [ "CA" , "CB" , "CG" , "CD1" ],
                         None,
                         None ] }

# Sets of atoms excluded from chi-angle rotations.
chi_exclusions = { "PHE" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ],
                             None,
                             None ],
                   "THR" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             None, 
                             None,
                             None ],
                   "GLU" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ], 
                             [ "CG", "HG2", "HG3" ],
                             None ],
                   "GLN" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ], 
                             [ "CG", "HG2", "HG3" ],
                             None ],
                   "ASP" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ], 
                             None,
                             None ],
                   "ASN" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ], 
                             None,
                             None ],
                   "CYS" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             None, 
                             None,
                             None ],
                   "MET" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ], 
                             None,
                             None ],
                   "ARG" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             None, 
                             None,
                             None ],
                   "LYS" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             None, 
                             None,
                             None ],
                   "HIS" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             None, 
                             None,
                             None ],
                   "LEU" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ], 
                             None,
                             None ],
                   "ILE" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3" ], 
                             None,
                             None ],
                   "SER" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             None, 
                             None,
                             None ],
                   "TYR" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             [ "CB", "HB2", "HB3"],
                             None,
                             None ],
                   "TRP" : [ [ "N", "H", "C", "O", "CA", "HA" ],
                             None, 
                             None,
                             None ] }

class Residue:
    """
    This class implements a Residue object. The residue is an object
    describing an individual amino acid of a protein chain.
    """
    
    def __init__(self, id, name):
        """
        @param id: PDB residue number.
        @type id: integer
        
        @param name: PDB name (amino acid name in three-letter code.
        @type name: string (3 characters)
        """
        # list of residue atoms in the same order as they occur in PDB file
        self.atom_list = []
        
        # dictionary for atom_name -> atom mapping
        self.atoms = {} 
        
        ##self.id = id

        # amino acid secondary structure        
        self.secondary_structure = SS_COIL

        # True if the residue is expanded. The feature is used by "Edit
        # Rotamers" command for efficient rotamer manipulation in reduced
        # protein display style.
        self.expanded = False
        
        # Rotamer color, used by "Edit Rotamers" command.
        self.color = None
        
        # These Rosetta-related attributes should be probably moved from this
        # class to some Rosetta-related structure. For now, the Residue
        # and Protein classes
        
        # Rosetta name of mutation range. 
        self.mutation_range = "NATAA"
        
        # Rosetta mutation descriptor. If set, it is usually a string of
        # 20 characters, corresponding to amino acid allowed at a given position.
        # Note: the descriptor is actuallt used by Rosetta only if mutation
        # range is set to "PIKAA". Otherwise, it is used only for informational
        # purposes. 
        self.mutation_descriptor = ""
        
        # True if this residue will be using backrub mode.
        self.backrub = False

    def get_atom_name(self, atom):
        """
        For a given PDB atom name, return a corresponding atom.
        """
        if atom.pdb_info and \
           atom.pdb_info.has_key('atom_name'):
            return atom.pdb_info['atom_name']
        else:
            return None
        
    def add_atom(self, atom, pdbname):
        """ 
        Add a new atom to the atom dictionary. 
        """
        self.atoms[pdbname] = atom
        self.atom_list.append(atom)

    def get_first_atom(self):
        """
        Return first atom of the residue, or None.
        """
        if len(self.atom_list):
            return self.atom_list[0]
        else:
            return None
        
    def get_atom_list(self):
        """
        Return a list of atoms for the residue.
        """
        return self.atom_list
    
    def get_side_chain_atom_list(self):
        """
        Return a list of side chain atoms for the residue. Assumes standard
        PDB atom names.
        """
        return [atom for atom in self.atom_list \
                if self.get_atom_name() not in ['C', 'N', 'O', 'H', 'HA']]

    def get_three_letter_code(self):
        """
        Return a three-letter amino acid code (the residue name).
        """
        atom = self.get_first_atom()
        if atom and \
           atom.pdb_info:
            if atom.pdb_info.has_key('residue_name'):
                return atom.pdb_info['residue_name'][:3]
        return None

    def get_name(self):
        """
        Just another version of get_three_letter_code.
        """
        return self.get_three_letter_code()
        
    def get_one_letter_code(self):
        """
        Return a one-letter amino acid code, or "X" if the residue code
        is not recognized.
        """
        if AA_3_TO_1.has_key(self.get_name()):
            return AA_3_TO_1[self.get_name()]
        
        return "X"
    
    def get_id(self):
        """
        Return a residue ID.
        
        The residue ID is a string representing the residue serial number 
        (integer value up to 9999) and concatenated residue insertion code 
        (single letter character). It is represented by a five character string.
        """
        atom = self.get_first_atom()
        if atom and \
           atom.pdb_info:
            if atom.pdb_info.has_key('residue_id'):
                return atom.pdb_info['residue_id']

        return None
    
    def get_index(self):
        """
        Return a residue index.
        """
        atom = self.get_first_atom()
        if atom and \
           atom.pdb_info:
            if atom.pdb_info.has_key('residue_id'):
                return int(atom.pdb_info['residue_id'][:3])

        return None
    
    def get_atom(self, pdbname):
        """
        Return an atom by PDB name.
        
        @param pdbname: a PDB name of an atom.
        @type: string
        """
        if self.atoms.has_key(pdbname):
            return self.atoms[pdbname]
        else:
            return None
    
    def has_atom(self, atom):
        """
        Check if the atom belongs to self. 
        
        @param atom: atom to be checked
        @type atom: Atom        
        """
        if atom in self.atoms.values():
            return True
        else:
            return False
        
    def set_secondary_structure(self, sec):
        """
        Set a secondary structure type for this residue.
        
        @param sec: secondary structure type to be assigned
        @type sec: int
        
        """
        self.secondary_structure = sec
        
    def get_secondary_structure(self):
        """
        Retrieve a secondary structure type.

        @return: secondary structure of this residue. 
        """
        return self.secondary_structure
        
    def get_atom_by_name(self, name):
        """
        Returns a residue atom for a given name, or None if not found.
        
        @param name: name of the atom
        @type name: string
        
        @return: atom
        """
        if self.atoms.has_key(name):
            return self.atoms[name]
        
        return None
    
    def get_c_alpha_atom(self):
        """
        Return an alpha-carbon atom atom (or None).
        
        @return: alpha carbon atom
        """
        return self.get_atom_by_name("CA")
    
    def get_c_beta_atom(self):
        """
        Return a beta carbon atom (or None).
        
        @return: beta carbon atom
        """
        return self.get_atom_by_name("CA")
    
    def get_n_atom(self):
        """
        Return a backbone nitrogen atom.
        
        @return: backbone nitrogen atom
        """
        return self.get_atom_by_name("N")
        
    def get_c_atom(self):
        """
        Return a backbone carbon atom.
        
        @return: backbone carbonyl group carbon atom
        """
        return self.get_atom_by_name("C")
        
    def get_o_atom(self):
        """
        Return a backbone oxygen atom.
        
        @return: backbone carbonyly group oxygen atom
        """
        return self.get_atom_by_name("O")
        
    def set_mutation_range(self, range):
        """
        Sets a mutation range according to Rosetta definition.
        
        @param range: mutation range
        @type range: string
        """
        self.mutation_range = range
        
    def get_mutation_range(self):
        """
        Gets a mutaion range according to Rosetta definition.
        nie,.
        @return: range
        """
        return self.mutation_range
    
    def set_mutation_descriptor(self, descriptor):
        """
        Sets a mutation descriptor according to Rosetta definition.
        
        @param descriptor: Rosetta mutation descriptor 
        @type descriptor: string (20-characters long)
        """
        self.mutation_descriptor = descriptor
        
    def get_mutation_descriptor(self):
        """
        Returns a mutation descriptor according to Rosetta definition.
        
        @return descriptor: string (20-characters long)
        """
        return self.mutation_descriptor
    
    def calc_torsion_angle(self, atom_list):
        """
        Calculates torsional angle defined by four atoms, A1-A2-A3-A4,
        Return torsional angle value between atoms A2 and A3.
        
        @param atom_list: list of four atoms describing the torsion bond
        @type atom_list: list
        
        @return: value of the torsional angle (float)
        """
   
        from Numeric import dot
        from math import atan2, pi, sqrt
        from geometry.VQT import cross
        
        if len(atom_list) != 4:
            # The list has to have four members.
            return 0.0
        
        # Calculate pairwise distances
        v12 = atom_list[0].posn() - atom_list[1].posn()
        v43 = atom_list[3].posn() - atom_list[2].posn()
        v23 = atom_list[1].posn() - atom_list[2].posn()

        # p is a vector perpendicular to the plane defined by atoms 1,2,3
        # p is perpendicular to v23_v12 plane
        p = cross(v23, v12)
        
        # x is a vector perpendicular to the plane defined by atoms 2,3,4.
        # x is perpendicular to v23_v43 plane
        x = cross(v23, v43)
        
        # y is perpendicular to v23_x plane
        y = cross(v23, x)
        
        # Calculate lengths of the x, y vectors.
        u1 = dot(x, x)
        v1 = dot(y, y)
        
        if u1 < 0.0 or \
           v1 < 0.0:
            return 360.0
        
        u2 = dot(p, x) / sqrt(u1)
        v2 = dot(p, y) / sqrt(v1)
        
        if u2 != 0.0 and \
           v2 != 0.0:
            # calculate the angle
            return atan2(v2, u2) * (180.0 / pi)
        else:
            return 360.0
         
    def get_chi_atom_list(self, which):
        """
        Create a list of four atoms for computing a given chi angle.
        Return None if no such angle exists for this amino acid.
        
        @param which: chi angle (0=chi1, 1=chi2, and so on)
        @type which: int
        
        @return: list of four atoms
        """
        if which in range(4):
            residue_name = self.get_name()
            if chi_angles.has_key(residue_name):
                chi_list = chi_angles[residue_name]
                if chi_list[which]:
                    chi_atom_names = chi_list[which]
                    chi_atoms = []
                    for name in chi_atom_names:
                        atom = self.get_atom_by_name(name)
                        if atom:
                            chi_atoms.append(atom)
                    return chi_atoms
        return None
     
    def get_chi_atom_exclusion_list(self, which):
        """
        Create a list of atoms excluded from rotation for a current amino acid.
        Return None if wrong chi angle is requested.
        
        @param which: chi angle (0=chi1, 1=chi2, and so on)
        @type which: int
        
        @return: list of atoms to be excluded from rotation
        """
        if which in range(4):
            residue_name = self.get_name()
            if chi_exclusions.has_key(residue_name):
                chi_ex_list = chi_exclusions[residue_name]
                ex_atoms = [self.get_atom_by_name("OXT")]
                for w in range(0, which + 1):
                    if chi_ex_list[w]:
                        ex_atom_names = chi_ex_list[w]
                        for name in ex_atom_names:
                            atom = self.get_atom_by_name(name)
                            if atom:
                                ex_atoms.append(atom)
                return ex_atoms
        return None
     
    def get_chi_angle(self, which):
        """
        Computes the side-chain Chi angle. Returns None if the angle
        doesn't exist.
        
        @param which: chi angle (0=chi1, 1=chi2, and so on)
        @type which: int
        
        @return: value of the specified chi angle
        """
        chi_atom_list = self.get_chi_atom_list(which)
        if chi_atom_list:
            return self.calc_torsion_angle(chi_atom_list)                  
        else:
            return None

    
    def get_atom_list_to_rotate(self, which):
        """
        Create a list of atoms to be rotated around a specified chi angle.
        Returns an empty list if wrong chi angle is requested.
        
        piotr 082008: This method should be rewritten in a way so it 
        traverses a molecular graph rather than uses a predefined 
        lists of atoms "excluded" and "included" from rotations.
        Current implementation only works for "proper" amino acids
        that have all atoms named properly and don't include any 
        non-standard atoms.
        
        @param which: chi angle (0=chi1, 1=chi2, and so on)
        @type which: int
        
        @return: list of atoms to be rotated for a specified chi angle
        """
        atom_list = []
        
        chi_atom_exclusion_list = self.get_chi_atom_exclusion_list(which)
        
        if chi_atom_exclusion_list:
            all_atom_list = self.get_atom_list()
            for atom in all_atom_list:
                if atom not in chi_atom_exclusion_list:
                    atom_list.append(atom)
                  
        return atom_list
    
    def lock(self):
        """
        Locks this residue (sets Rosetta mutation range to "native rotamer").      
        """
        self.set_mutation_range("NATRO")
        
    def set_chi_angle(self, which, angle):
        """
        Sets a specified chi angle of this amino acid. 
        
        @param which: chi angle (0=chi1, 1=chi2, and so on)
        @type which: int
        
        @param angle: value of the chi angle to be set
        @type angle:float
        
        @return: angle value if sucessfully completed, None if not
        """
        
        from geometry.VQT import norm, Q, V
        from math import pi, cos, sin
        
        chi_atom_list = self.get_chi_atom_list(which)
        if chi_atom_list:
            angle0 = self.calc_torsion_angle(chi_atom_list)
            dangle = angle - angle0
            if abs(dangle) > 0.0:
                vec = norm(chi_atom_list[2].posn() - chi_atom_list[1].posn())
                atom_list = self.get_atom_list_to_rotate(which)
                first_atom_posn = chi_atom_list[1].posn()
                for atom in atom_list:
                    pos = atom.posn() - first_atom_posn
                    
                    cos_a = cos(pi * (dangle / 180.0))
                    sin_a = sin(pi * (dangle / 180.0))
                    
                    q = V(0, 0, 0)
                    
                    # rotate the point around a vector
                    
                    q[0] += (cos_a + (1.0 - cos_a) * vec[0] * vec[0]) * pos[0];
                    q[0] += ((1.0 - cos_a) * vec[0] * vec[1] - vec[2] * sin_a) * pos[1];
                    q[0] += ((1.0 - cos_a) * 
                             vec[0] * vec[2] + vec[1] * sin_a) * pos[2];
                 
                    q[1] += ((1.0 - cos_a) * 
                             vec[0] * vec[1] + vec[2] * sin_a) * pos[0];
                    q[1] += (cos_a + (1.0 - cos_a) * vec[1] * vec[1]) * pos[1];
                    q[1] += ((1.0 - cos_a) * vec[1] * vec[2] - vec[0] * sin_a) * pos[2];
                 
                    q[2] += ((1.0 - cos_a) * vec[0] * vec[2] - vec[1] * sin_a) * pos[0];
                    q[2] += ((1.0 - cos_a) * vec[1] * vec[2] + vec[0] * sin_a) * pos[1];
                    q[2] += (cos_a + (1.0 - cos_a) * vec[2] * vec[2]) * pos[2];
    
                    q += first_atom_posn
                    
                    atom.setposn(q)
                    return angle
                
        return None
        
    def expand(self):
        """
        Expands a residue side chain.
        """
        
        self.expanded = True
        
    def collapse(self):
        """
        Collapse a residue side chain.
        """
        self.expanded = False
        
    def is_expanded(self):
        """
        Return True if side chain of this amino acid is expanded.
        """
        return self.expanded
    
    def set_color(self, color):
        """
        Sets a rotamer color for current amino acid.
        """
        self.color = color
        
    def set_backrub_mode(self, enable_backrub):
        """
        Sets Rosetta backrub mode (True or False).
        
        @param enable_backrub: should backrub mode be enabled for this residue
        @type enable_backrub: boolean
        """
        self.backrub = enable_backrub
        
    def get_backrub_mode(self):
        """ 
        Gets Rosetta backrub mode (True or False).
        
        @return: is backrub enabled for this residue (boolean)
        """
        return self.backrub
    
# End of Residue class.

