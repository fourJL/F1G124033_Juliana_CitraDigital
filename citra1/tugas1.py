def multiply_3d_matrices(A, B):
    b = len(A)
    m = len(A[0])
    n = len(A[0][0])
    
    if len(B) != b or len(B[0]) != n:
        raise ValueError("Dimensi matriks tidak sesuai! Pastikan jumlah matriks sama dan kolom A == baris B.")
        
    p = len(B[0][0])
    
    C = [[[0 for _ in range(p)] for _ in range(m)] for _ in range(b)]
    
    for matriks in range(b):
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[matriks][i][j] += A[matriks][i][k] * B[matriks][k][j]
                    
    return C

def print_3d_matrix(matrix, name="Matrix"):
    print(f"=== {name} ===")
    for matriks_idx, matriks_item in enumerate(matrix):
        print(f"Matriks {matriks_idx + 1}:")
        for row in matriks_item:
            print(f"  {row}")
    print("Bentuk Array 3D:")
    print(f"{matrix}\n")

if __name__ == "__main__":
    print("Program Perkalian Matriks 3D \n" + "-"*42)
    
    A = [
        [[1, 2, 3],
         [4, 5, 6]],
        [[7, 8, 9],
         [1, 2, 3]]
    ]
    
    B = [
        [[1, 2],
         [3, 4],
         [5, 6]],
        [[6, 5],
         [4, 3],
         [2, 1]]
    ]
    
    try:
        print_3d_matrix(A, "Matriks A (2x2x3)")
        print_3d_matrix(B, "Matriks B (2x3x2)")
        
        C = multiply_3d_matrices(A, B)
        
        print_3d_matrix(C, "Hasil Matriks C = A x B (2x2x2)")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")