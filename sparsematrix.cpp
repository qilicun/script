#include </usr/local/include/eigen3/Eigen/Sparse>
#include <iostream>
int main()
{
    typedef Eigen::SparseMatrix<double,Eigen::RowMajor> mat;
    typedef Eigen::Triplet<double> T;

    std::vector<T> coef;
    coef.push_back(T(0, 0, 1.));
    coef.push_back(T(0, 3, 2.));
    coef.push_back(T(1, 1, 4.));
    coef.push_back(T(2, 2, 5.));
    coef.push_back(T(2, 3, 6.));
    coef.push_back(T(3, 0, 3.));
    coef.push_back(T(3, 3, 8.));
//    coef.push_back(T(4, 1, 9.));
//    coef.push_back(T(4, 4, 10.));
    mat A(4, 4);
    A.setFromTriplets(coef.begin(), coef.end());
    std::cout << A << std::endl;
    for (int k=0; k < A.rows(); ++k) {
        for (Eigen::SparseMatrix<double>::InnerIterator it(A,k); it; ++it){
            std::cout << it.row() << "  "
                      << it.col() << "  "
                      << it.value() << std::endl;
        }
    }
    
    std::cout << "Non zeros:\n" << A.nonZeros() << std::endl;
    std::cout << "Innerindex:\n";
    for (int i = 0; i < A.nonZeros(); ++i) {
        std::cout << A.innerIndexPtr()[i] << " " << std::endl;
    }

    std::cout << "Outerindex:\n";
    for (int i = 0; i < A.cols(); ++i) {
        std::cout << A.outerIndexPtr()[i] << " " << std::endl;
    }
    std::cout << std::endl;
    int col = 0, num = 0;
    for (int k = 0; k < A.rows(); ++k) {
        int count = 0;
        while (count < (A.outerIndexPtr()[num + 1] - A.outerIndexPtr()[num])) {
            ++count;
            std::cout << k << "  " << A.innerIndexPtr()[col] << "  " << A.valuePtr()[col] << std::endl;
            ++col;
        }
        ++num;
    }
}

 
