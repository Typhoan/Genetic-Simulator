#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//returns an integer representing the zero-indexed number of the alignment, starting at 
//dom[0]->subdom[subDomlen-1] and ending at dom[domLen-1]->subdom[0]
int alignSequencePair(char* dominant, char* subdominant) {
	int domLen = strlen(dominant);
	int subdomLen = strlen(subdominant);
	int numAlignments = domLen + subdomLen - 1;
	int numAlignedNucs[numAlignments];
	int i, j, k;
	int mostAligned = -1;
	int bestAlignment = -1;
	
	memset(numAlignedNucs, 0, sizeof(numAlignedNucs));
	
	for(i = 0; i < domLen; i++) {
		for(j = 0; j < subdomLen; j++) {
			if(dominant[i] == subdominant[j]) {
				numAlignedNucs[(i - j + subdomLen - 1)]++; //this calculation maps the table indices to a particular alignment
				//printf("(%d, %d): algn %d\n", i, j, i-j+subdomLen-1);
				//for(k = 0; k < numAlignments; k++) {
				//	printf("%d ", numAlignedNucs[k]);
				//}
				//printf("\n");
				//getchar();
			}
		}
		//printf("\n");
	}
		
	for(i = 0; i < numAlignments; i++) {
		//printf("%d ", numAlignedNucs[i]);
		if(numAlignedNucs[i] > mostAligned) {
			bestAlignment = i;
			mostAligned = numAlignedNucs[i];
		}
	}

	printf("\n%d\n", bestAlignment);
	return bestAlignment;
	
}

int main() {
	char* seq1 = "GATCGTAGCTGATGCTGTAGTATGCTATCTCGCTTATATAGCTAGCTAGTTAGGC";
	char* seq2 = "AGTCGATTATATTAGCTTAGTCGGCTA";
	alignSequencePair(seq1, seq2); 
	return 0;
}

//--------------------------GATCGTAGCTGATGCTGTAGTATGCTATCTCGCTTATATAGCTAGCTAGTTAGGC
//----------------------AGTCGATTATATTAGCTTAGTCGGCTA





