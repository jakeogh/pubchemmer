#!/usr/bin/env python3

#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Numeric

from kcl.sqla.model.BaseMixin import BASE
#Base = declarative_base()


class PubChem(BASE):
    __tablename__ = 'pubchem'
    mol_chiral_flag = Column(Boolean())
    pubchem_compound_cid = Column(Integer(), primary_key=True)
    pubchem_compound_canonicalized = Column(Boolean())
    pubchem_cactvs_complexity = Column(Numeric())
    pubchem_cactvs_hbond_acceptor = Column(Boolean())
    pubchem_cactvs_hbond_donor = Column(Boolean())
    pubchem_cactvs_rotatable_bond = Column(Boolean())
    pubchem_cactvs_subskeys = Column(Text())
    pubchem_iupac_openeye_name = Column(Text())
    pubchem_iupac_cas_name = Column(Text())
    pubchem_iupac_name_markup = Column(Text())
    pubchem_iupac_name = Column(Text())
    pubchem_iupac_systematic_name = Column(Text())
    pubchem_iupac_traditional_name = Column(Text())
    pubchem_iupac_inchi = Column(Text())
    pubchem_iupac_inchikey = Column(Text())
    pubchem_xlogp3_aa = Column(Numeric())
    pubchem_exact_mass = Column(Numeric())
    pubchem_molecular_formula = Column(Text())
    pubchem_molecular_weight = Column(Numeric())
    pubchem_openeye_can_smiles = Column(Text())
    pubchem_openeye_iso_smiles = Column(Text())
    pubchem_cactvs_tpsa = Column(Numeric())
    pubchem_monoisotopic_weight = Column(Numeric())
    pubchem_total_charge = Column(Integer())
    pubchem_heavy_atom_count = Column(Integer())
    pubchem_atom_def_stereo_count = Column(Integer())
    pubchem_atom_udef_stereo_count = Column(Integer())
    pubchem_bond_def_stereo_count = Column(Integer())
    pubchem_bond_udef_stereo_count = Column(Integer())
    pubchem_isotopic_atom_count = Column(Integer())
    pubchem_component_count = Column(Integer())
    pubchem_cactvs_tauto_count = Column(Integer())
    pubchem_coordinate_type = Column(Text())
    pubchem_bondannotations = Column(Text())
    openbabel_symmetry_classes = Column(Text())
    pubchem_substance_id = Column(Integer())
    pubchem_substance_version = Column(Text())
    pubchem_ext_datasource_name = Column(Text())
    pubchem_ext_datasource_regid = Column(Text())
    pubchem_ext_datasource_url = Column(Text())
    pubchem_ext_substance_url = Column(Text())
    pubchem_substance_synonym = Column(Text())
    pubchem_substance_comment = Column(Text())
    pubchem_depositor_record_date = Column(Text())
    pubchem_xref_ext_id = Column(Integer())
    pubchem_xref_substance_id = Column(Integer())
    pubchem_xref_compound_id = Column(Integer())
    pubchem_xref_assay_id = Column(Integer())
    pubchem_pubmed_id = Column(Integer())
    pubchem_genbank_nucleotide_id = Column(Integer())
    pubchem_genbank_protein_id = Column(Integer())
    pubchem_ncbi_taxonomy_id = Column(Integer())
    pubchem_ncbi_omim_id = Column(Integer())
    pubchem_ncbi_mmdb_id = Column(Integer())
    pubchem_pubmed_mesh_term = Column(Text())
    pubchem_ncbi_gene_id = Column(Integer())
    pubchem_ncbi_probe_id = Column(Integer())
    pubchem_ncbi_biosystem_id = Column(Integer())
    pubchem_ncbi_geo_gse_id = Column(Integer())
    pubchem_ncbi_geo_gsm_id = Column(Integer())
    pubchem_mmdb_molecule_name = Column(Text())
    pubchem_mmdb_residue_id = Column(Integer())
    pubchem_mmdb_residue_name = Column(Text())
    pubchem_mmdb_atom_id = Column(Integer())
    pubchem_mmdb_atom_name = Column(Text())
    pubchem_hold_until_date = Column(Text())
    pubchem_subs_auto_structure = Column(Text())
    pubchem_revoke_substance = Column(Text())
    pubchem_cid_associations = Column(Text())
    pubchem_generic_registry_name = Column(Text())
    pubchem_compound_id_type = Column(Text())
    pubchem_nonstandardbond = Column(Text())
    pubchem_xlogp3 = Column(Text())
    pubchem_openeye_tauto_count = Column(Text())
    pubchem_conformer_id_list = Column(Text())
    pubchem_conformer_diverseorder = Column(Text())
    pubchem_pharmacophore_features = Column(Text())
    pubchem_effective_rotor_count = Column(Integer())
    pubchem_mmff94_partial_charges = Column(Text())
    pubchem_conformer_rmsd = Column(Text())
    pubchem_conformer_id = Column(Integer())
    pubchem_shape_volume = Column(Text())
    pubchem_mmff94_energy = Column(Text())
    pubchem_shape_multipoles = Column(Text())
    pubchem_shape_fingerprint = Column(Text())
    pubchem_shape_selfoverlap = Column(Text())
    pubchem_feature_selfoverlap = Column(Text())

