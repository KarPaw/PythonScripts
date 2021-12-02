from Bio import SeqIO
from Bio.SeqUtils import GC
import re

# Basic manipulation and reading data
# from genbank ".gb" file

def load_file_with_gene_sequence(file, formatting):

    gene = SeqIO.read(file, formatting)
    return gene


def manipulations(gene_sequence):

    gene = gene_sequence
    transcripted, translated, = gene.seq.transcribe(), gene.seq.translate()
    reverse_complemented = gene.seq.reverse_complement()

    manipulated = [transcripted, translated, reverse_complemented]

    return manipulated


def main():

    gene = load_file_with_gene_sequence("u48392.gb", "genbank")
    print(f"Input sequence:\n {gene.seq}", end="\n")

    manipulated = manipulations(gene)
    names_of_manipulations = ["Transcripted:", "Translated:", "Reverse complemented:"]
    [print(f"\n {elt}") for elt in zip(names_of_manipulations, manipulated)]

    # %GC
    print("\nGC Value:\n" + str(GC(gene.seq)))

    print("\nAnnotations:")
    [print(f"{i} -> {gene.annotations[i]}") for i in iter(gene.annotations)]

    # Restriction
    # 1. EcoRI (GAATTC)
    # 2. BamHI (GGATCC)
    print("\nRestriction sites:\n",
          re.search("GAATTC", str(gene.seq)),
          re.search("GGATCC", str(gene.seq))
          )


main()

