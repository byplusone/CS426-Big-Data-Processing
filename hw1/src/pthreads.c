/*
	Matrix Multiplication using Pthreads
*/
#include<stdio.h>
#include<time.h>
#include<pthread.h>
#include<stdlib.h>
#include<unistd.h>
#include<memory.h>
#include<string.h>
#include<stdlib.h>

/*Maximum data element*/
#define RANGE 100
/*
	Matrix A has M rows and N cols
	Matrix B has N rows and M cols
*/
#define M 2000
#define N 2000

int matrixA[M][N];
int matrixB[N][M];
int res[M][M];
/*
	Create a structure to pass the parameters
*/
struct split{
	int startrow;
	int gap;
};
struct v*data[M][M];  

void getMatrix();
void readMatrix();
void printResultSingle();
void printResultMulti();
void* Calculation(void* argv);

void main(int argc, char *argv[]){
	/* number denotes the number of threads */
	int number=0;
	if( argc == 2 ){
    	number=atoi(argv[1]);
    }else if( argc > 2 ){
    	printf("Too many arguments supplied.\n");
    	exit(1);
    }else{
      printf("One argument expected.\n");
      exit(1);
   	}

   	pthread_t matrics[number];
   	struct split* partition[number];
	getMatrix();
	readMatrix();

	int i=0;
	for (i=0;i<number;++i){
		partition[i]=(struct split*)malloc(sizeof(struct split));
		partition[i]->startrow=i;
		partition[i]->gap=number;
	}

	struct timeval tpstart,tpend;
    float timeuse1,timeuse2;
    gettimeofday(&tpstart,NULL);

	int tid=0;
	for(i=0;i<number;++i){
		tid=pthread_create(&matrics[i],NULL,(void*)(&Calculation),(void*)partition[i]);
		if(tid!=0){
			perror("Thread creation failed!");
			exit(1);
		}
	}

	for(i=0;i<number;++i)
		pthread_join(matrics[i],NULL);

	gettimeofday(&tpend,NULL);
    timeuse1=1000000*(tpend.tv_sec-tpstart.tv_sec)+(tpend.tv_usec-tpstart.tv_usec);
    printf("Execution_period_with_pthreads:%.2fseconds\n",(timeuse1)/1000000.0);

	for (i=0;i<number;++i)
		free(partition[i]);

    //printResultMulti();

    // Single Thread
    int j=0,k=0;
    gettimeofday(&tpstart,NULL);
    for(i=0;i<M;i++)                                 
        for(j=0;j<M;j++)
            for(k=0;k<N;k++)
                res[i][j]+=matrixA[i][k]*matrixB[k][j];
    gettimeofday(&tpend,NULL);
    timeuse2=1000000*(tpend.tv_sec-tpstart.tv_sec)+(tpend.tv_usec-tpstart.tv_usec);
    printf("Execution_period_with_single_thread:%.2fseconds\n",(timeuse2)/1000000.0);

    //printResultSingle();

    printf("Speedup ratio is %.2f\n",timeuse2/timeuse1);

    exit(0);
}

void* Calculation(void* argv){
	int start=0,step=0,col=0,k=0;
    struct split* parameter;
    parameter=(struct split*)argv;
    start=parameter->startrow;
    step=parameter->gap;
    for(;start<M;start=start+step)
        for(col=0;col<M;++col)
        	for(k=0;k<N;++k)
        		res[start][col]+=matrixA[start][k]*matrixB[k][col];        	
    pthread_exit(0);
}

void getMatrix()
{
    FILE *file1,*file2;
    file1=fopen("matrixA","wt");
    file2=fopen("matrixB","wt");
    int i,j;
    srand((unsigned)time(NULL));
    for(i=0;i<M;i++)
    {
        for(j=0;j<N;j++)
            fprintf(file1,"%-8d",rand()%RANGE);
        fprintf(file1,"\n");
    }
    fclose(file1);
    for(i=0;i<N;i++)
    {
        for(j=0;j<M;j++)
            fprintf(file2,"%-8d",rand()%RANGE);
        fprintf(file2,"\n");
    }
    fclose(file2);  
}
 
void readMatrix()
{
    FILE *file1,*file2;
    file1=fopen("matrixA","rt");
    file2=fopen("matrixB","rt");
    int i,j;
    for(i=0;i<M;i++)
        for(j=0;j<N;j++)
            fscanf(file1,"%d",&matrixA[i][j]);
    fclose(file1);
    for(i=0;i<N;i++)
        for(j=0;j<M;j++)
            fscanf(file2,"%d",&matrixB[i][j]);
    fclose(file2);
}

void printResultMulti(){
	FILE *file3;
	file3=fopen("matrixResMulti","wt");
	int i,j;
    for(i=0;i<M;i++)
    {
        for(j=0;j<M;j++)
            fprintf(file3,"%-8d",res[i][j]);
        fprintf(file3,"\n");
    }
    fclose(file3);	
}

void printResultSingle(){
	FILE *file4;
	file4=fopen("matrixResSingle","wt");
	int i,j;
    for(i=0;i<M;i++)
    {
        for(j=0;j<M;j++)
            fprintf(file4,"%-8d",res[i][j]);
        fprintf(file4,"\n");
    }
    fclose(file4);	
}

