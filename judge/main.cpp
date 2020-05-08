#include <iostream>
using namespace std;
int main(void){
  int A,B;
  cin >> A >> B;
  int C[3];
  int result = 0;
  for(int i=0;i<3;i++){
    cin >> C[i];
    result += C[i];
  }
  cout << result*(A+B) << endl;
}