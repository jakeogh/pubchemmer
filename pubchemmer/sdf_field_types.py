#!/usr/bin/env python3

SDF_FIELD_TYPES = {
    'mol chiral flag': 'Boolean',
    'pubchem_compound_cid': 'Integer',
    'pubchem_compound_canonicalized': 'Boolean',
    'pubchem_cactvs_complexity': 'Numeric',
    'pubchem_cactvs_hbond_acceptor': 'Boolean',
    'pubchem_cactvs_hbond_donor': 'Boolean',
    'pubchem_cactvs_rotatable_bond': 'Boolean',
    'pubchem_cactvs_subskeys': 'Text',
    'pubchem_iupac_openeye_name': 'Text',
    'pubchem_iupac_cas_name': 'Text',
    'pubchem_iupac_name_markup': 'Text',
    'pubchem_iupac_name': 'Text',
    'pubchem_iupac_systematic_name': 'Text',
    'pubchem_iupac_traditional_name': 'Text',
    'pubchem_iupac_inchi': 'Text',
    'pubchem_iupac_inchikey': 'Text',
    'pubchem_xlogp3_aa': 'Numeric',
    'pubchem_exact_mass': 'Numeric',
    'pubchem_molecular_formula': 'Text',
    'pubchem_molecular_weight': 'Numeric',
    'pubchem_openeye_can_smiles': 'Text',
    'pubchem_openeye_iso_smiles': 'Text',
    'pubchem_cactvs_tpsa': 'Numeric',
    'pubchem_monoisotopic_weight': 'Numeric',
    'pubchem_total_charge': 'Integer',
    'pubchem_heavy_atom_count': 'Integer',
    'pubchem_atom_def_stereo_count': 'Integer',
    'pubchem_atom_udef_stereo_count': 'Integer',
    'pubchem_bond_def_stereo_count': 'Integer',
    'pubchem_bond_udef_stereo_count': 'Integer',
    'pubchem_isotopic_atom_count': 'Integer',
    'pubchem_component_count': 'Integer',
    'pubchem_cactvs_tauto_count': 'Integer',
    'pubchem_coordinate_type': 'Text',
    'pubchem_bondannotations': 'Text',
    'openbabel symmetry classes': 'Text',
    'pubchem_substance_id': 'Integer',
    'pubchem_substance_version': '',
    'pubchem_ext_datasource_name': '',
    'pubchem_ext_datasource_regid': '',
    'pubchem_ext_datasource_url': 'Text',
    'pubchem_ext_substance_url': 'Text',
    'pubchem_substance_synonym': '',
    'pubchem_substance_comment': 'Text',
    'pubchem_depositor_record_date': '',
    'pubchem_xref_ext_id': 'Integer',
    'pubchem_xref_substance_id': 'Integer',
    'pubchem_xref_compound_id': 'Integer',
    'pubchem_xref_assay_id': 'Integer',
    'pubchem_pubmed_id': 'Integer',
    'pubchem_genbank_nucleotide_id': 'Integer',
    'pubchem_genbank_protein_id': 'Integer',
    'pubchem_ncbi_taxonomy_id': 'Integer',
    'pubchem_ncbi_omim_id': 'Integer',
    'pubchem_ncbi_mmdb_id': 'Integer',
    'pubchem_pubmed_mesh_term': '',
    'pubchem_ncbi_gene_id': 'Integer',
    'pubchem_ncbi_probe_id': 'Integer',
    'pubchem_ncbi_biosystem_id': 'Integer',
    'pubchem_ncbi_geo_gse_id': 'Integer',
    'pubchem_ncbi_geo_gsm_id': 'Integer',
    'pubchem_mmdb_molecule_name': '',
    'pubchem_mmdb_residue_id': 'Integer',
    'pubchem_mmdb_residue_name': '',
    'pubchem_mmdb_atom_id': 'Integer',
    'pubchem_mmdb_atom_name': 'Text',
    'pubchem_hold_until_date': '',
    'pubchem_subs_auto_structure': '',
    'pubchem_revoke_substance': '',
    'pubchem_cid_associations': '',
    'pubchem_generic_registry_name': '',
    'pubchem_compound_id_type': '',
    'pubchem_nonstandardbond': '',
    'pubchem_xlogp3': '',
    'pubchem_openeye_tauto_count': '',
    'pubchem_conformer_id_list': '',
    'pubchem_conformer_diverseorder': '',
    'pubchem_pharmacophore_features': '',
    'pubchem_effective_rotor_count': 'Integer',
    'pubchem_mmff94_partial_charges': '',
    'pubchem_conformer_rmsd': '',
    'pubchem_conformer_id': 'Integer',
    'pubchem_shape_volume': '',
    'pubchem_mmff94_energy': '',
    'pubchem_shape_multipoles': '',
    'pubchem_shape_fingerprint': '',
    'pubchem_shape_selfoverlap': '',
    'pubchem_feature_selfoverlap': '',
}