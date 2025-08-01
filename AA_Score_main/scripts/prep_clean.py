import os
from Bio.PDB import PDBParser, PDBIO, Select
from rdkit import Chem
from rdkit.Chem import AllChem, rdmolfiles


class ProteinOnlySelect(Select):
    def accept_residue(self, residue):
        return residue.id[0] == ' '


def clean_protein(pdb_filepath, pdb_id, verbose=False):
    parser = PDBParser(QUIET=True)
    io = PDBIO()

    try:
        structure = parser.get_structure(pdb_id, pdb_filepath)
        io.set_structure(structure)
        io.save(pdb_filepath, ProteinOnlySelect())
        if verbose:
            print(f"Saved cleaned: {pdb_filepath}")
        return pdb_filepath
    except Exception as e:
        if verbose:
            print(f"Failed to clean {pdb_filepath}: {e}")
        else:
            raise Exception(e)


def clean_ligand(lig_pdb_path):
    mol = Chem.MolFromPDBFile(lig_pdb_path, removeHs=False, sanitize=False)
    if mol is None:
        raise ValueError(f'RDKit failed to parse ligand PDB: {lig_pdb_path}')
    mol.UpdatePropertyCache(strict=False)
    Chem.SanitizeMol(mol)
    mol = Chem.AddHs(mol)
    rdmolfiles.MolToPDBFile(mol, lig_pdb_path)


def split_and_clean_complex(input_path, pdb_id, output_dir_path):
    prot_out_path = os.path.join(output_dir_path, f'{pdb_id}_protein.pdb')
    lig_out_path = os.path.join(output_dir_path, f'{pdb_id}_ligand.pdb')
    water_names = {'HOH', 'WAT'}
    
    with open(input_path, 'r') as fin, open(prot_out_path, 'w') as prot_f, open(lig_out_path, 'w') as lig_f:

        for line in fin:
            rec = line[:6]
            if rec == 'ATOM  ':
                prot_f.write(line)
            elif rec == 'HETATM':
                resname = line[17:20].strip()
                # The following works for our rosetta poses bc the ligand should be 
                # the only mol w hetatms... For other cases, an additional boolean
                # condition is probably needed.
                lig_f.write(line) 
            elif rec in ('TER   ', 'END   '):
                prot_f.write(line)
    
    clean_protein(prot_out_path, pdb_id)
    clean_ligand(lig_out_path)