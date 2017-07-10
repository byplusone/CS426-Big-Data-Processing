#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <omp.h>

#define MAX_SIZE 1000
int local_size;
int thread_count = 4;
int* mat = NULL;  

/*Generate MAX_SIZE*MAX_SIZE Matrix*/
void genMatrix(int size){
	int i = 0, j = 0; 
	mat = malloc(size*size*sizeof(int));                                           
    srand(time(NULL));                 
                                                
    for (i = 0; i < size; ++i)            
        for (j = 0; j < size; ++j)                                      
            mat[i*size+j] = rand() % 100; 
    //printf("matrix generated!\n");            
}

/*Serial Func*/
void MatrixMutiply1(int n, int mat1[], int mat2[], int result[]){
	int i,j,k;
	int lSum;
	for(i=0;i<n;i++)
  		for(j=0;j<n;j++){
  			lSum=0;
   			for(k=0;k<n;k++)
    			lSum += mat1[i*n+k] * mat2[k*n+j];
   			result[i*n+j]=lSum;
  		}
}

/*Static Scheduling Func*/
void MatrixMutiply2(int n, int mat1[], int mat2[], int result[]){
	int i,j,k;
	int lSum;
	
//	omp_set_num_threads(4);
	#pragma omp parallel shared(mat1,mat2,result) private(i,j,k,lSum) 	
	{
	#pragma omp for schedule(static)
		for(i=0;i<n;i++)
  			for(j=0;j<n;j++){
   				lSum=0;
   				for(k=0;k<n;k++)
    				lSum += mat1[i*n+k] * mat2[k*n+j];
   				result[i*n+j]=lSum;
  			}
  	}
}

/*Dynamic Scheduling Func*/
void MatrixMutiply3(int n, int mat1[], int mat2[], int result[]){
	int i,j,k;
	int lSum;
	
//	omp_set_num_threads(4);
	#pragma omp parallel shared(mat1,mat2,result) private(i,j,k,lSum) 	
	{
	#pragma omp for schedule(dynamic)
		for(i=0;i<n;i++)
  			for(j=0;j<n;j++){
   				lSum=0;
   				for(k=0;k<n;k++)
    				lSum += mat1[i*n+k] * mat2[k*n+j];
   				result[i*n+j]=lSum;
  			}
  	}
}

void MatrixMutiply4(int n, int mat1[], int mat2[], int result[]){
  	int my_rank = omp_get_thread_num();
    //int thread_count = omp_get_num_threads();
    int i, j, k, temp;

    int my_first_row = my_rank*local_size;
    int my_last_row = (my_rank+1)*local_size - 1;

    for(i = my_first_row; i <= my_last_row; i++){
        for(j = 0; j<n; j++){
            temp = 0;
            for(k = 0; k<n; k++)
                temp += mat1[i*n+k] * mat2[k*n+j];
            result[i*n+j] = temp;
        }

    }
}

int main(){
	int i = 200;
	double start, end;
	int* result1 = NULL;
    int* result2 = NULL;
    float ratio = 0;
    float serial_time = 0;

    //freopen("result46.txt","w",stdout);

	for(i=1000;i <= MAX_SIZE; i=i+200){
		genMatrix(i);

		printf("*************current matrix size: %d*************\n", i);

		result1 = malloc(i*i*sizeof(int));
		result2 = malloc(i*i*sizeof(int));
	  	
  		start = omp_get_wtime( );
  		MatrixMutiply1(i,mat,mat,result1);
  		end = omp_get_wtime( );

  		printf("Total time for serial version:%f\n", end-start);
  		serial_time = end-start;
  	
  		start = omp_get_wtime( );
  		MatrixMutiply2(i,mat,mat,result2);
		end = omp_get_wtime( );
  		printf("Total time for parallel version with static scheduling:%f\n", end-start);
		ratio = serial_time/(end-start);
  		printf("ratio = %f\n", ratio);

  		start = omp_get_wtime( );
  		MatrixMutiply3(i,mat,mat,result2);
		end = omp_get_wtime( );
		printf("Total time for parallel version with dynamic scheduling:%f\n", end-start);
		ratio = serial_time/(end-start);
  		printf("ratio = %f\n", ratio);

		local_size = i/thread_count;
  		start = omp_get_wtime( );
  		# pragma omp parallel shared(mat,result2)
  		{	
    		MatrixMutiply4(i,mat,mat,result2);
    	}
  
		end = omp_get_wtime( );
		printf("Total time for parallel version with block scheduling:%f\n", end-start);				
		ratio = serial_time/(end-start);
  		printf("ratio = %f\n", ratio);
    	
  		if(!memcmp(result1,result2,sizeof(int)*i))
  			printf("The two matrices are the same.\n");
  		else
  			printf("The two matrices are not the same.\n");

    //free(mat);
    free(result1);
    free(result2);
	}
	

	return 0;
}
