import inspect


def analyze_tensor(input_tensor):
    '''
    Input:
        input_tensor - The tensor to be analyzed.
    Output:
        None
    Func:
        This function analyzes the given input tensor and prints information about it.
        It outputs the variable name of the tensor, its shape, and its content.
    '''
    print("\n##### analyze_tensor_st #####")
    # Output the variable name
    print("1.Name:")
    frame = inspect.currentframe().f_back
    var_name = 'Unable'
    for name, value in frame.f_locals.items():
        if value is input_tensor:
            var_name = name
            break
    print(var_name)
    # Shape of the tensor
    print("2.Shape:")
    print(tuple(input_tensor.shape))
    # Content of the tensor
    tensor_content = input_tensor.tolist()
    print("3.Content:")
    print(str(input_tensor))
    print("##### analyze_tensor_ed #####")


def analyze_tensor_s(*args):
    for Unable in args:
        analyze_tensor(Unable)
