# HiC-Pro 
def preparing_HiCPro_file(h3dgipdir, genome, enzyme, input_dir):
    import os
    output_file = "./HiCPro/run_HiC-Pro.sh"
    fp = open(output_file, 'w')
    # 1、Enzyme fragments
    enzyme_fragments_order="python {0}/utils/digest_genome.py {1} -r {2} -o HiC-Pro_enzyme_fragments.bed".format(h3dgipdir, genome, enzyme)
    print(enzyme_fragments_order, file=fp)
    # 2、Chromosome size
    chromosome_size_step1 = "samtools faidx {0} -o {0}.fai".format(genome)
    chromosome_size_step2 = "awk -v OFS='\\t' " + " \'{print $1, $2}\' " + "{0}.fai > HiC-Pro_chromosome_size.txt".format(genome)
    print(chromosome_size_step1, file=fp)
    print(chromosome_size_step2, file=fp)
    # 3、genome index
    ln_order = "ln -s {}".format(genome)
    genomeName = genome.split("/")[-1].split(".")[0]
    build_index_order = "bowtie2-build -f {0} --threads 4".format(genomeName)
    print(ln_order, file=fp)
    print(build_index_order, file=fp)
    # 4、change configure file
    cp_order = "cp {}/utils/HiC-Pro.config .".format(h3dgipdir)
    tmpDir = os.getcwd()
    workDir = tmpDir.replace("/", "\/")
    HiCProDir = "{}\/HiCPro".format(workDir)
    sed_order1 = "sed -i 's/InderDir/{0}/g' HiC-Pro.config".format(HiCProDir)
    sed_order2 = "sed -i 's/GenomeName/{0}/g' HiC-Pro.config".format(genomeName)
    sed_order3 = "sed -i 's/ChromosomeSize/{0}\/HiC-Pro_chromosome_size.txt/g' HiC-Pro.config".format(HiCProDir)
    ## HindIII
    sed_order4 = "sed -i 's/EnzymeFragment/{0}\/HiC-Pro_enzyme_fragments.bed/g' HiC-Pro.config".format(HiCProDir)
    print(sed_order1, file=fp)
    print(sed_order2, file=fp)
    print(sed_order3, file=fp)
    print(sed_order4, file=fp)
    # 4 run HiC-Pro
    HiCPro_step1 = "HiC-Pro -c {0}/utils/HiC-Pro.config -i {1} -o HiCPro_result -p".format(h3dgipdir, input_dir)
    HiCPro_step2 = "cd HiCPro_result"
    HiCPro_step3 = "sh HiCPro_step1.sh"
    HiCPro_step4 = "sh HiCPro_step2.sh"
    HiCPro_step5 = "cd .."
    print(HiCPro_step1, file=fp)
    print(HiCPro_step2, file=fp)
    print(HiCPro_step3, file=fp)
    print(HiCPro_step4, file=fp)
    print(HiCPro_step5, file=fp)
    fp.close()

# Juicer    
def preparing_juicer_file(h3dgipdir, genome, enzyme, input_dir, compartment_resolution, tad_resolution, loop_resolution, name):
    import os
    output_file = "juicer/run_juicer.sh"
    fp = open(output_file, "w")
    genomeName = genome.split("/")[-1].split(".")[0]
    # 1、Enzyme fragm
    enzyme_fragments_order='python {0}/utils/generate_site_positions.py {1} juicer_enzyme_fragments {2}'.format(h3dgipdir, enzyme, genome)
    print(enzyme_fragments_order, file=fp)
    # 2、Chromosome size
    chromosome_size_step1 = "samtools faidx {0} -o {0}.fai".format(genome)
    chromosome_size_step2 = "awk -v OFS='\\t'" + " \'{print $1, $2}\' " + "{0}.fai > juicer_chromosome_size.txt".format(genome)
    print(chromosome_size_step1, file=fp)
    print(chromosome_size_step2, file=fp)    
    # 3、genome index
    ln_order = "ln -s {0} juicer/{0}".format(genome)
    build_index_order = "bwa index {0}".format(genome)
    print(ln_order, file=fp)
    print(build_index_order, file=fp)
    # 4、Generates .hic file
    workDir = os.getcwd()
    genome_name = genome.split("/")[-1].split(".")[0]
    juicer_order = "juicer.sh -z {0} -y {1}/juicer/juicer_enzyme_fragments_{2}.txt -p {1}/juicer/juicer_chromsome_size.txt -d {3} -D juicer_output/ -t 4".format(genome, workDir, enzyme, input_dir)
    print(juicer_order, file=fp)
    # 5、divide Compartment
    juicer_compartment = "java -jar {0}/utils/juicer_scripts/juicer_tools.jar eigenvector KR juicer_output/{1}.hic chr1 BP {2}".format(h3dgipdir, name, compartment_resolution)
    print(juicer_compartment, file=fp)
    print("#divide chr1 compartment", file=fp)
    # 6、Identify TADs
    juicer_TAD = "java -jar {0}/utils/juicer_scripts/juicer_tools.jar arrowhead -m 2000 -r {1} -k KR --threads 4 juicer_output/{2}.hic juicer_output".format(h3dgipdir, tad_resolution, name)
    print(juicer_TAD, file=fp)
    # 7、Infer loops
    juicer_loop = "java -jar {0}/utils/juicer_scripts/juicer_tools.jar hiccups --cpu -r {1} -f 0.1 -p 4 -i 7 -d 20000 -t 0.02,1.5,1.75,2 -k KR --threads 4  juicer_output/{2}.hic juicer_output".format(h3dgipdir, loop_resolution, name)
    print(juicer_loop, file=fp)
    fp.close()
    
# TADLib
def preparing_TADLib_file(h3dgipdir, filename, resolution):
    matrix = '../HiCPro_result/hic_results/matrix/raw/{0}/{1}_{0}.matrix'.format(resolution, filename)
    bins = '../HiCPro_result/hic_results/matrix/raw/{0}/{1}_{0}_abs.bed'.format(resolution, filename)
    output_file = 'TADLib/run_TADLib.sh'
    fp = open(output_file, "w")
    # 1、split chr
    split_chr_order = "python {0}/utils/hicproTocool.py -m {1} -b {2} -o TADLib/intramtx -YN N".format(h3dgipdir, matrix, bins)
    print(split_chr_order, file=fp)
    # 2、to cool
    dataset_file = 'TADLib/dataset'
    fd = open(dataset_file, 'w')
    print("res:{}".format(resolution), file=fd)
    print(" ./intramtx", file=fd)
    fd.close()
    tocool_order = "toCooler -O TADLib/TADLib.cool -d dataset --chromsize-file ../HiCPro/HiC-Pro_chromosome_size.txt"
    print(tocool_order, file=fp)
    # 3、find tad
    meta_file = 'TADLib/meta_file'
    fm = open(meta_file, 'w')
    print("res:{}".format(resolution), file=fm)
    print(" rep1:TADLib/TADLib.cool::{}".format(resolution), file=fm)
    fm.close()
    find_TAD_order = "hitad -O TADLib_result/TADLib_TAD.bed -d meta_file --logFile hitad.log -p 4"
    print(find_TAD_order, file=fp)
    fp.close()

# FitHiC 
def preparing_FitHiC_file(h3dgipdir, filename, resolution):
    matrix = '../HiCPro_result/hic_results/matrix/raw/{0}/{1}_{0}.matrix'.format(resolution, filename)
    bins = '../HiCPro_result/hic_results/matrix/raw/{0}/{1}_{0}_abs.bed'.format(resolution, filename)
    output_file = 'FitHiC/run_FitHiC.sh'
    fp = open(output_file, "w")
    fithic_step1 = "python {0}/utils/hicpro2fithic.py -i {1} -b {2} -r {3} -o ./ -n FitHiC".format(h3dgipdir, matrix, bins, resolution)
    fithic_step2 = "fithic -f ./FitHiC.fithic.fragmentMappability.gz -i ./FitHiC.fithic.interactionCounts.gz -r {} -L 6000 -U 3000000 -p 2 -o FitHiC_result -l FitHiC".format(resolution) # 3 Kb resolution
    print(fithic_step1, file=fp)
    print(fithic_step2, file=fp)
    fp.close()

# hichipper
def preparing_hichipper_file():
    # build the configure file of hichipper
    import os
    workDir = os.getcwd() 
    fy = open('./hichipper/hichipper_configure.yaml', 'w')
    print("peaks:", file=fy)
    print("  - COMBINED,ALL", file=fy)
    print("resfrags:", file=fy)
    print("  - {0}/HiCPro/HiC-Pro_enzyme_fragments.bed".format(workDir), file=fy)
    print("hicpro_output:", file=fy)
    print("  - {0}/HiCPro_result/hic_reuslts".format(workDir), file=fy)
    fy.close()
    # build the run file of hichipper
    output_file = "./hichipper/run_hichipper.sh"
    fp = open(output_file, "w")
    hichipper_order = "hichipper --out hichipper_result hichipper_configure.yaml"
    print(hichipper_order, file=fp)
    fp.close()

# FitHiChIP
def preparing_FitHiChIP_file(h3dgipdir, name):
    output_file = "./FitHiChIP/run_FitHiChIP.sh"
    fp = open(output_file, "w")
    # configure file
    cp_order = "cp {}/utils/configfile_BiasCorrection_ICEBias ./".format(h3dgipdir)
    sed_order1 = "sed -i 's/ValidPairs/..\/HiCPro\/hic_results\/data\/{0}\/{0}.allValidPairs/g' configfile_BiasCorrection_ICEBias".format(name)
    sed_order2 = "sed -i 's/chromSize/..\/HiCPro\/HiC-Pro_chromosome_size.txt/g' configfile_BiasCorrection_ICEBias"
    print(cp_order, file=fp)
    print(sed_order1, file=fp)
    print(sed_order2, file=fp)
    FitHiChIP_order = "bash {0}/utils/FitHiChIP_HiCPro.sh -C configfile_BiasCorrection_ICEBias".format(h3dgipdir)
    print(FitHiChIP_order, file=fp)
    print("# The optional compilation file contains configfile_BiasCorrection_ICEBias, configfile_BiasCorrection_CoverageBias, configfile_P2P_BiasCorrection_CoverageBias, configfile_P2P_BiasCorrection_ICEBias", file=fp)
    fp.close()

# creat directory
def preparing_directory():    
    def make_dir(dirname):
        import os
        work_path = os.getcwd()
        file_path = "{0}/{1}".format(work_path, dirname)
        print(file_path)
        if os.path.exists(file_path):
            print('The folder exists')
        else:
            os.makedirs(file_path)
    all_dir = ['HiCPro', 'TADLib', 'FitHiC', 'hichipper', 'FitHiChIP', 'juicer']
    for d in all_dir:
        make_dir(d)


# build workflows
def H3DGIP_workflows(h3dgipdir, input_dir, genome, enzyme, compartment_resolution, tad_resolution, loop_resolution, name):
    #make directory
    preparing_directory()
    # HiC-Pro
    preparing_HiCPro_file(h3dgipdir, genome, enzyme, input_dir)
    # Juicer
    preparing_juicer_file(h3dgipdir, genome, enzyme, input_dir, compartment_resolution, tad_resolution, loop_resolution, name)
    # TADLib
    preparing_TADLib_file(h3dgipdir, name, tad_resolution)
    # FitHiC 
    preparing_FitHiC_file(h3dgipdir, name, loop_resolution)
    # hichipper
    preparing_hichipper_file()
    # FitHiChIP
    preparing_FitHiChIP_file(h3dgipdir, name)
    # write the pipeline
    fp = open("H3DGIP_pipeline.sh", 'w')
    for i in ['HiCPro', 'juicer', 'TADLib', 'FitHiC', 'FitHiChIP', 'hichipper']:
        print("#{}".format(i), file=fp)
        print("cd {}".format(i), file=fp)
        print("sh run_{}.sh".format(i), file=fp)
        print("cd ..", file=fp)
        print("", file=fp)
    fp.close()

def main(argv):
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-d", "--h3dgip_directory", required=True, help="The directory of H3DGIP")
    parser.add_argument('-i', '--input_directory', required=True, help="The directory of input file")
    parser.add_argument('-n', '--sample_name', required=True, help="Sample name")
    parser.add_argument('-g', '--genome', required=True, help="The genome file")
    parser.add_argument('-e', '--enzyme', required=True, help="The type of restriction enzyme")
    parser.add_argument('-c', '--compartment_resolution', required=True, help="The resolution of compartment")
    parser.add_argument('-t', '--tad_resolution', required=True, help='The resolution of TAD')
    parser.add_argument('-l', '--loop_resolution', required=True, help='The resolution of loop')
    args = parser.parse_args()
    h3dgipdir, input_dir, name, genome, enzyme, compartment_resolution, tad_resolution, loop_resolution  = args.h3dgip_directory, args.input_directory, args.sample_name, args.genome, args.enzyme, args.compartment_resolution, args.tad_resolution, args.loop_resolution
    H3DGIP_workflows(h3dgipdir, input_dir, genome, enzyme, compartment_resolution, tad_resolution, loop_resolution, name)
import sys
if __name__ == "__main__":
    main(sys.argv[1:])
