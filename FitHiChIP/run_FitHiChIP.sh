cp /public/home/xhhuang/soft/H3DGIP/utils/configfile_BiasCorrection_ICEBias ./
sed -i 's/ValidPairs/..\/HiCPro\/hic_results\/data\/name\/name.allValidPairs/g' configfile_BiasCorrection_ICEBias
sed -i 's/chromSize/..\/HiCPro\/HiC-Pro_chromosome_size.txt/g' configfile_BiasCorrection_ICEBias
bash /public/home/xhhuang/soft/H3DGIP/utils/FitHiChIP_HiCPro.sh -C configfile_BiasCorrection_ICEBias
# The optional compilation file contains configfile_BiasCorrection_ICEBias, configfile_BiasCorrection_CoverageBias, configfile_P2P_BiasCorrection_CoverageBias, configfile_P2P_BiasCorrection_ICEBias
