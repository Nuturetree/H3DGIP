python /public/home/xhhuang/soft/H3DGIP/utils/hicpro2fithic.py -i ../HiCPro_result/hic_results/matrix/raw/5000/name_5000.matrix -b ../HiCPro_result/hic_results/matrix/raw/5000/name_5000_abs.bed -r 5000 -o ./ -n FitHiC
fithic -f ./FitHiC.fithic.fragmentMappability.gz -i ./FitHiC.fithic.interactionCounts.gz -r 5000 -L 6000 -U 3000000 -p 2 -o FitHiC_result -l FitHiC
