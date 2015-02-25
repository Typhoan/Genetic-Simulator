'''
Created on Feb 4, 2015

@author: Ian McPherson
'''

'''
 Iterates through the list and converts the DNA sequence to a RNA sequence.
'''
def DNAToRNA(seq):
    RNA = ""
    for letter in seq:
        if letter == 'A':
            RNA+='U'
            
        elif letter == 'T':
            RNA+='A'
            
        elif letter == 'C':
            RNA+='G'
            
        elif letter == 'G':
            RNA+='C'
            
    return RNA

'''
 Iterates through the list and converts the RNA sequence to a DNA sequence.
'''
def RNAtoDNA(seq):
    DNA = ""
    for letter in seq:
        if letter == 'A':
            DNA+='T'
            
        elif letter == 'U':
            DNA+='A'
            
        elif letter == 'C':
            DNA+='G'
            
        elif letter == 'G':
            DNA+='C'
            
    return DNA

'''
 Iterates through the RNA sequence and creates codons. Then it checks the amino
 acid dictionary for the corresponding codon. It does this until the protein has
 been fully built.
'''
def RNAToProtien(seq):
    amino = dict([('UUU', 'F'), ('UUC', 'F'), ('UUA', 'L'), ('UUG', 'L'), ('UCU', 'S'),
          ('UCC', 'S'), ('UCA', 'S'), ('UCG', 'S'), ('UAU', 'Y'), ('UAC', 'Y'),
          ('UAA', '*'), ('UAG', '*'), ('UGU', 'C'), ('UGC', 'C'), ('UGA', '*'),
          ('UGG', 'W'), ('CUU', 'L'), ('CUC', 'L'), ('CUA', 'L'), ('CUG', 'L'),
          ('CCU', 'P'), ('CCC', 'P'), ('CCA', 'P'), ('CCG', 'P'), ('CAU', 'H'),
          ('CAC', 'H'), ('CAA', 'Q'), ('CAG', 'Q'), ('CGU', 'R'), ('CGC', 'R'),
          ('CGA', 'R'), ('CGG', 'R'), ('AUU', 'I'), ('AUC', 'I'), ('AUA', 'I'),
          ('AUG', 'M'), ('ACU', 'T'), ('ACC', 'T'), ('ACA', 'T'), ('ACG', 'T'),
          ('AAU', 'N'), ('AAC', 'N'), ('AAA', 'K'), ('AAG', 'K'), ('AGU', 'S'),
          ('AGC', 'S'), ('AGA', 'R'), ('AGG', 'R'), ('GUU', 'V'), ('GUC', 'V'),
          ('GUA', 'V'), ('GUG', 'V'), ('GCU', 'A'), ('GCC', 'A'), ('GCA', 'A'),
          ('GCG', 'A'), ('GAU', 'D'), ('GAC', 'D'), ('GAA', 'E'), ('GAG', 'E'),
          ('GGU', 'G'), ('GGC', 'G'), ('GGA', 'G'), ('GGG', 'G')])
    protien = ""
    counter = 0
    codon = ""
    
    for letter in seq:
        if counter == 3:
            counter = 0
            protien+=amino[codon]
            codon = ''
            
        codon+=letter
        counter = counter + 1
        
    if counter == 3:
        protien+=amino[codon]
        
    return protien
    
