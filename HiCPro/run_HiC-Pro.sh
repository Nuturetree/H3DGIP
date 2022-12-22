python /public/home/xhhuang/soft/H3DGIP/utils/digest_genome.py path/genome.fa -r HIndIII -o HiC-Pro_enzyme_fragments.bed
samtools faidx path/genome.fa -o path/genome.fa.fai
awk -v OFS='\t'  '{print $1, $2}' path/genome.fa.fai > HiC-Pro_chromosome_size.txt
ln -s path/genome.fa
bowtie2-build -f genome --threads 4
sed -i 's/InderDir/\/public\/home\/xhhuang\/biodate\/bio_protocol\/H3DGIP2\/HiCPro/g' HiC-Pro.config
sed -i 's/GenomeName/genome/g' HiC-Pro.config
sed -i 's/ChromosomeSize/\/public\/home\/xhhuang\/biodate\/bio_protocol\/H3DGIP2\/HiCPro\/HiC-Pro_chromosome_size.txt/g' HiC-Pro.config
sed -i 's/EnzymeFragment/\/public\/home\/xhhuang\/biodate\/bio_protocol\/H3DGIP2\/HiCPro\/HiC-Pro_enzyme_fragments.bed/g' HiC-Pro.config
HiC-Pro -c /public/home/xhhuang/soft/H3DGIP/utils/HiC-Pro.config -i Rawdata -o HiCPro_result -p
cd HiCPro_result
sh HiCPro_step1.sh
sh HiCPro_step2.sh
cd ..
