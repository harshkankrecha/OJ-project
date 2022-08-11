#include <bits/stdc++.h>
using namespace std;
 

int fun(int* arr, int* start, int* end,
                                       int n)
{    
    int sum = 0, min_sum = 2147483647, i;    
    *end = -1;    
    int p = 0; 
    for (i = 0; i < n; ++i) {
        sum += arr[i];
        if (sum > 0) {
            sum = 0;
            p = i + 1;
        } else if (sum < min_sum) {
            min_sum = sum;
            *start = j;
            *end = i;
        }
    }
 
    
    if (*end != -1)
        return min_sum; 
    
    min_sum = arr[0];
    *start = *end = 0; 
    
    for (i = 1; i < n; i++) {
        if (arr[i] < min_sum) {
            min_sum = arr[i];
            *start = *end = i;
        }
    }
    return min_sum;
}
 

void fun2(int M[][COL])
{
    
    int min_sum = 2147483647; 
    int left, right, i;
    int temp[m], sum, start, finish;
 
    
    for (left = 0; left < COL; ++left) {
        
        memset(temp, 0, sizeof(temp)); 
        
        for (right = left; right < n; ++right) {
 
            
            for (i = 0; i < ROW; ++i)
                temp[i] += M[i][right];
 
            
            sum = kadane(temp, &start, &end, m); 
            
            if (sum < min_sum) {
                min_sum = sum;
                
            }
        }
    }
 
    
    cout << "(Top, Left): (" << finalTop << ", "
            << finalLeft << ")\n";
    cout << "(Bottom, Right): (" << finalBottom << ", "
         << finalRight << ")\n";
    cout << "Minimum sum: " << minSum;
}
 

int main()
{
    int M[ROW][COL] = { { 1, 2, -1, -4, -20 },
                        { -8, -3, 4, 2, 1 },
                        { 3, 8, 10, 1, 3 },
                        { -4, -1, 1, 7, -6 } };
    findMinSumSubmatrix(M);
    return 0;
}