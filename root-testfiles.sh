#! /bin/sh

SITE="https://root.cern/files"

mkdir files
pushd files

wget -N ${SITE}/aleph_ref_5.root
wget -N ${SITE}/aleph.root
wget -N ${SITE}/alice3_ref_6.root
wget -N ${SITE}/alice3.root
wget -N ${SITE}/ams_ref_4.root
wget -N ${SITE}/ams.root
wget -N ${SITE}/atlas_ref_6.root
wget -N ${SITE}/atlas.root
wget -N ${SITE}/babar2_ref_4.root
wget -N ${SITE}/babar2.root
wget -N ${SITE}/barres_ref_3.root
wget -N ${SITE}/barres.root
wget -N ${SITE}/belle_ref_3.root
wget -N ${SITE}/belle.root
wget -N ${SITE}/bes_ref_3.root
wget -N ${SITE}/bes.root
wget -N ${SITE}/brahms_ref_3.root
wget -N ${SITE}/brahms.root
wget -N ${SITE}/btev_ref_3.root
wget -N ${SITE}/btev.root
wget -N ${SITE}/cdf_ref_6.root
wget -N ${SITE}/cdf.root
wget -N ${SITE}/chambers_ref_3.root
wget -N ${SITE}/chambers.root
wget -N ${SITE}/cms_ref_4.root
wget -N ${SITE}/cms.root
wget -N ${SITE}/dubna_ref_3.root
wget -N ${SITE}/dubna.root
wget -N ${SITE}/e907_ref_3.root
wget -N ${SITE}/e907.root
wget -N ${SITE}/felix_ref_3.root
wget -N ${SITE}/felix.root
wget -N ${SITE}/ganil_ref_3.root
wget -N ${SITE}/ganil.root
wget -N ${SITE}/gem_ref_5.root
wget -N ${SITE}/gem.root
wget -N ${SITE}/hades2_ref_4.root
wget -N ${SITE}/hades2.root
wget -N ${SITE}/hermes_ref_3.root
wget -N ${SITE}/hermes.root
wget -N ${SITE}/integral_ref_4.root
wget -N ${SITE}/integral.root
wget -N ${SITE}/lhcbfull_ref_4.root
wget -N ${SITE}/lhcbfull.root
wget -N ${SITE}/na35_ref_3.root
wget -N ${SITE}/na35.root
wget -N ${SITE}/na47_ref_3.root
wget -N ${SITE}/na47.root
wget -N ${SITE}/na49_ref_3.root
wget -N ${SITE}/na49.root
wget -N ${SITE}/p326_ref_4.root
wget -N ${SITE}/p326.root
wget -N ${SITE}/phenix_ref_3.root
wget -N ${SITE}/phenix.root
wget -N ${SITE}/phobos2_ref_4.root
wget -N ${SITE}/phobos2.root
wget -N ${SITE}/sdc_ref_3.root
wget -N ${SITE}/sdc.root
wget -N ${SITE}/sld_ref_4.root
wget -N ${SITE}/sld.root
wget -N ${SITE}/star_ref_4.root
wget -N ${SITE}/star.root
wget -N ${SITE}/tesla_ref_4.root
wget -N ${SITE}/tesla.root
wget -N ${SITE}/wa91_ref_3.root
wget -N ${SITE}/wa91.root

wget -N ${SITE}/AtlasGraphs.root
wget -N ${SITE}/europe.root
wget -N ${SITE}/linearIO.root
wget -N ${SITE}/stressHistogram.5.18.00.root
wget -N ${SITE}/tmva_class_example.root
wget -N ${SITE}/tmva_reg_example.root
wget -N ${SITE}/usa.root

for f in *.root ; do ln -s $f $f.ROOT.cachefile ; done

mkdir tutorials
pushd tutorials
wget -N ${SITE}/tutorials/df014_CsvDataSource_MuRun2010B.csv
popd

popd

tar -J -c --group root --owner root -f root-testfiles.tar.xz files
