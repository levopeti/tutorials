import numpy as np
from scipy.linalg import toeplitz
import time
from scipy import signal


def matrix_to_vector(input):
    """
    Converts the input matrix to a vector by stacking the rows in a specific way explained here

    Arg:
    input -- a numpy matrix

    Returns:
    ouput_vector -- a column vector with size input.shape[0]*input.shape[1]
    """
    input_h, input_w = input.shape
    output_vector = np.zeros(input_h * input_w, dtype=input.dtype)
    # flip the input matrix up-down because last row should go first
    input = np.flipud(input)
    for i, row in enumerate(input):
        st = i * input_w
        nd = st + input_w
        output_vector[st:nd] = row
    return output_vector


def vector_to_matrix(input, output_shape):
    """
    Reshapes the output of the maxtrix multiplication to the shape "output_shape"

    Arg:
    input -- a numpy vector

    Returns:
    output -- numpy matrix with shape "output_shape"
    """
    output_h, output_w = output_shape
    output = np.zeros(output_shape, dtype=input.dtype)
    for i in range(output_h):
        st = i * output_w
        nd = st + output_w
        output[i, :] = input[st:nd]
    # flip the output matrix up-down to get correct result
    output = np.flipud(output)
    return output


def convolution_as_maultiplication(I, F, mode='full', print_ir=False):
    """
    Performs 2D convolution between input I and filter F by converting the F to a toeplitz matrix and multiply it
      with vectorizes version of I
      By : AliSaaalehi@gmail.com

    Arg:
    I -- 2D numpy matrix
    F -- numpy 2D matrix
    print_ir -- if True, all intermediate resutls will be printed after each step of the algorithms

    Returns:
    output -- 2D numpy matrix, result of convolving I with F
    """
    # number of columns and rows of the input
    I_row_num, I_col_num = I.shape

    # number of columns and rows of the filter
    F_row_num, F_col_num = F.shape

    #  calculate the output dimensions
    output_row_num = I_row_num + F_row_num - 1
    output_col_num = I_col_num + F_col_num - 1
    #if print_ir: print('output dimension:', output_row_num, output_col_num)

    # zero pad the filter
    F_zero_padded = np.pad(F, ((output_row_num - F_row_num, 0),
                               (0, output_col_num - F_col_num)),
                           'constant', constant_values=0)
    #if print_ir: print('F_zero_padded: ', F_zero_padded)

    # use each row of the zero-padded F to creat a toeplitz matrix.
    #  Number of columns in this matrices are same as numbe of columns of input signal
    toeplitz_list = []
    for i in range(F_zero_padded.shape[0] - 1, -1, -1):  # iterate from last row to the first row
        c = F_zero_padded[i, :]  # i th row of the F
        r = np.r_[c[0], np.zeros(I_col_num - 1)]  # first row for the toeplitz fuction should be defined otherwise
        # the result is wrong
        toeplitz_m = toeplitz(c, r)  # this function is in scipy.linalg library
        toeplitz_list.append(toeplitz_m)
        #if print_ir: print('F ' + str(i) + '\n', toeplitz_m)

        # doubly blocked toeplitz indices:
    #  this matrix defines which toeplitz matrix from toeplitz_list goes to which part of the doubly blocked
    c = range(1, F_zero_padded.shape[0] + 1)
    r = np.r_[c[0], np.zeros(I_row_num - 1, dtype=int)]
    doubly_indices = toeplitz(c, r)
    #if print_ir: print('doubly indices \n', doubly_indices)

    ## creat doubly blocked matrix with zero values
    toeplitz_shape = toeplitz_list[0].shape  # shape of one toeplitz matrix
    h = toeplitz_shape[0] * doubly_indices.shape[0]
    w = toeplitz_shape[1] * doubly_indices.shape[1]
    doubly_blocked_shape = [h, w]
    doubly_blocked = np.zeros(doubly_blocked_shape)

    # tile toeplitz matrices for each row in the doubly blocked matrix
    b_h, b_w = toeplitz_shape  # hight and withs of each block
    for i in range(doubly_indices.shape[0]):
        for j in range(doubly_indices.shape[1]):
            start_i = i * b_h
            start_j = j * b_w
            end_i = start_i + b_h
            end_j = start_j + b_w
            doubly_blocked[start_i: end_i, start_j:end_j] = toeplitz_list[doubly_indices[i, j] - 1]

    #if print_ir: print('doubly_blocked: ', doubly_blocked)

    # convert I to a vector
    vectorized_I = matrix_to_vector(I)
    #if print_ir: print('vectorized_I: ', vectorized_I)

    # get result of the convolution by matrix mupltiplication
    result_vector = np.matmul(doubly_blocked, vectorized_I)
    #result_vector = doubly_blocked @ vectorized_I
    #if print_ir: print('result_vector: ', result_vector)

    # reshape the raw rsult to desired matrix form
    out_shape = [output_row_num, output_col_num]
    output = vector_to_matrix(result_vector, out_shape)
    if print_ir: print('Result of implemented method: \n', output)

    if mode == 'full':
        return output

    if mode == 'valid':
        # from left, above, right and below: kernel size - 1
        assert I_row_num > F_row_num, "The size of the filter must be less then the size of the image."
        return output[(F_row_num - 1):-(F_row_num - 1), (F_col_num - 1):-(F_col_num - 1)]

    if mode == 'same':
        # from left and above: floor of (kernel size - 1)
        # from right and below: the rest
        return output[(F_row_num - 1) // 2:-((F_row_num - 1) - ((F_row_num - 1) // 2)), (F_col_num - 1) // 2:-((F_col_num - 1) - ((F_col_num - 1) // 2))]


if __name__ == '__main__':
    # test on different examples

    # fill I an F with random numbers
    I = np.random.randn(10, 20)
    F = np.random.randn(3, 4)

    F = np.random.randn(10, 13)
    I = np.random.randn(30, 70)

    rep = 10
    mode = 'full'
    # print(mode)
    # print(signal.convolve2d(I, F, mode))
    # print(signal.convolve2d(I, F, mode).shape)
    # print(convolution_as_maultiplication(I, F, mode))
    # print(convolution_as_maultiplication(I, F, mode).shape)
    # d = signal.convolve2d(I, F, mode) - convolution_as_maultiplication(I, F, mode)
    # print('OK' if sum(sum(abs(d))) < 1e-10 else 'Fail')
    #
    # mode = 'valid'
    # print(mode)
    # print(signal.convolve2d(I, F, mode))
    # print(signal.convolve2d(I, F, mode).shape)
    # print(convolution_as_maultiplication(I, F, mode))
    # print(convolution_as_maultiplication(I, F, mode).shape)
    # d = signal.convolve2d(I, F, mode) - convolution_as_maultiplication(I, F, mode)
    # print('OK' if sum(sum(abs(d))) < 1e-10 else 'Fail')
    #
    # mode = 'same'
    # print(mode)
    # print(signal.convolve2d(I, F, mode))
    # print(signal.convolve2d(I, F, mode).shape)
    # print(convolution_as_maultiplication(I, F, mode))
    # print(convolution_as_maultiplication(I, F, mode).shape)
    # d = signal.convolve2d(I, F, mode) - convolution_as_maultiplication(I, F, mode)
    # print('OK' if sum(sum(abs(d))) < 1e-10 else 'Fail')
    start = time.time()
    for _ in range(rep):
        my_result = convolution_as_maultiplication(F, I, mode)
    print('np: ', time.time() - start)
    print(my_result.shape)

    start = time.time()
    for _ in range(rep):
        lib_result = signal.convolve2d(I, F, mode)
    print('sp: ', time.time() - start)
    print(lib_result.shape)

    d = my_result - lib_result
    print('OK' if sum(sum(abs(d))) < 1e-10 else 'Fail')
    print(my_result.all() == lib_result.all())

    #######

    start = time.time()
    for _ in range(rep):
        i_my_result = convolution_as_maultiplication(I, F, mode)
    print('np: ', time.time() - start)
    print(i_my_result.shape)

    start = time.time()
    for _ in range(rep):
        i_lib_result = signal.convolve2d(F, I, mode)
    print('sp: ', time.time() - start)
    print(i_lib_result.shape)

    d = i_my_result - i_lib_result
    print('OK' if sum(sum(abs(d))) < 1e-10 else 'Fail')
    print(i_my_result.all() == i_lib_result.all())

    print()
    print(my_result.all() == i_my_result.all())
    print(lib_result.all() == i_lib_result.all())
