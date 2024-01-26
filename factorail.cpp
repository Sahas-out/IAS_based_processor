#include<bits/stdc++.h>
using namespace std;
int main(){
    int n;
    cin>>n;
    int prod=1;
    cin>>prod;
    while(n!=0){
        prod=prod*n;
        n--;
    }
    cout<<prod;
}