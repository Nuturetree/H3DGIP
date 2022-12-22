python /public/home/xhhuang/soft/H3DGIP/utils/hicproTocool.py -m ../HiCPro_result/hic_results/matrix/raw/20000/name_20000.matrix -b ../HiCPro_result/hic_results/matrix/raw/20000/name_20000_abs.bed -o TADLib/intramtx -YN N
toCooler -O TADLib/TADLib.cool -d dataset --chromsize-file ../HiCPro/HiC-Pro_chromosome_size.txt
hitad -O TADLib_result/TADLib_TAD.bed -d meta_file --logFile hitad.log -p 4
