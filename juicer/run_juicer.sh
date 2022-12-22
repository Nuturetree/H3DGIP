python /public/home/xhhuang/soft/H3DGIP/utils/generate_site_positions.py HIndIII juicer_enzyme_fragments path/genome.fa
samtools faidx path/genome.fa -o path/genome.fa.fai
awk -v OFS='\t' '{print $1, $2}' path/genome.fa.fai > juicer_chromosome_size.txt
ln -s path/genome.fa juicer/path/genome.fa
bwa index path/genome.fa
juicer.sh -z path/genome.fa -y /public/home/xhhuang/biodate/bio_protocol/H3DGIP2/juicer/juicer_enzyme_fragments_HIndIII.txt -p /public/home/xhhuang/biodate/bio_protocol/H3DGIP2/juicer/juicer_chromsome_size.txt -d Rawdata -D juicer_output/ -t 4
java -jar /public/home/xhhuang/soft/H3DGIP/utils/juicer_scripts/juicer_tools.jar eigenvector KR juicer_output/name.hic chr1 BP 100000
#divide chr1 compartment
java -jar /public/home/xhhuang/soft/H3DGIP/utils/juicer_scripts/juicer_tools.jar arrowhead -m 2000 -r 20000 -k KR --threads 4 juicer_output/name.hic juicer_output
java -jar /public/home/xhhuang/soft/H3DGIP/utils/juicer_scripts/juicer_tools.jar hiccups --cpu -r 5000 -f 0.1 -p 4 -i 7 -d 20000 -t 0.02,1.5,1.75,2 -k KR --threads 4  juicer_output/name.hic juicer_output
