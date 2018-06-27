#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <math.h>


using namespace std;


int main(int argc, char * argv[])
{
	if(argc < 3)
	{
		printf("usage: %s FS_thickness_file.asc output.raw\n", argv[0]);
		exit(1);
	}

	FILE *fp = fopen(argv[1],"r");
	FILE *wfp = fopen(argv[2],"wb");

	int i_verts = 0;
	float d1, d2, d3, d4, d5;
	float *thick;

	while(!feof(fp))
	{
		fscanf(fp,"%f %f %f %f %f", &d1, &d2, &d3, &d4, &d5);
		i_verts++;
	}

	rewind(fp);

	thick = new float[i_verts];
	for(int i = 0; i < i_verts; i++)
		fscanf(fp,"%f %f %f %f %f", &d1, &d2, &d3, &d4, &thick[i]);

	fwrite(thick, sizeof(float),i_verts,wfp);

	delete [] thick;
	fclose(fp);
	fclose(wfp);

	return 0;
}
