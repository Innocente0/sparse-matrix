class SparseMatrix:
    def __init__(self, matrix_file_path_or_num_rows, num_cols=None):
        self.elements = {}
        if isinstance(matrix_file_path_or_num_rows, str):
            self.load_matrix(matrix_file_path_or_num_rows)
        else:
            self.rows = matrix_file_path_or_num_rows
            self.cols = num_cols

    def load_matrix(self, matrix_file_path):
        with open(matrix_file_path, 'r') as f:
            lines = f.readlines()

        self.rows = int(lines[0].split('=')[1])
        self.cols = int(lines[1].split('=')[1])

        for line in lines[2:]:
            line = line.strip()
            if line:
                row, col, value = map(int, line[1:-1].split(','))
                self.set_element(row, col, value)

    def get_element(self, curr_row, curr_col):
        return self.elements.get((curr_row, curr_col), 0)

    def set_element(self, curr_row, curr_col, value):
        if value != 0:
            self.elements[(curr_row, curr_col)] = value
        elif (curr_row, curr_col) in self.elements:
            del self.elements[(curr_row, curr_col)]

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError('Matrices dimensions do not match for addition')

        result = SparseMatrix(self.rows, self.cols)

        for key, value in self.elements.items():
            result.elements[key] = value

        for key, value in other.elements.items():
            row, col = key
            new_value = result.get_element(row, col) + value
            result.set_element(row, col, new_value)

        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError('Matrices dimensions do not match for subtraction')

        result = SparseMatrix(self.rows, self.cols)

        for key, value in self.elements.items():
            result.elements[key] = value

        for key, value in other.elements.items():
            row, col = key
            new_value = result.get_element(row, col) - value
            result.set_element(row, col, new_value)

        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError('Matrices dimensions do not match for multiplication')

        result = SparseMatrix(self.rows, other.cols)

        for (row1, col1), value1 in self.elements.items():
            for (row2, col2), value2 in other.elements.items():
                if col1 == row2:
                    new_value = result.get_element(row1, col2) + value1 * value2
                    result.set_element(row1, col2, new_value)

        return result

    def save_result(self, result_file_path):
        with open(result_file_path, 'w') as f:
            f.write(f'rows={self.rows}\n')
            f.write(f'cols={self.cols}\n')
            for (row, col), value in self.elements.items():
                f.write(f'({row}, {col}, {value})\n')

    def __str__(self):
        return f'rows={self.rows}\ncols={self.cols}\n(elements={self.elements})'


def main():
    first_matrix_file_path = 'dsa/sparse_matrix/sample_inputs/matrix1.txt'
    second_matrix_file_path = 'dsa/sparse_matrix/sample_inputs/matrix2.txt'

    matrix1 = SparseMatrix(first_matrix_file_path)
    matrix2 = SparseMatrix(second_matrix_file_path)

    result_add = matrix1.add(matrix2)
    result_sub = matrix1.subtract(matrix2)

    output_add_path = 'dsa/sparse_matrix/sample_results/addition_result.txt'
    output_sub_path = 'dsa/sparse_matrix/sample_results/subtraction_result.txt'

    result_add.save_result(output_add_path)
    result_sub.save_result(output_sub_path)

    print(f'Processed successfully. Output saved for addition and subtraction between '
          f'{first_matrix_file_path} and {second_matrix_file_path}: {output_add_path} {output_sub_path} respectively')


if __name__ == "__main__":
    main()
