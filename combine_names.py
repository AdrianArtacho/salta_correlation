# importing os module 
import os
  
# VARIABLES----------
file_chosen1 = ''
file_chosen1 = ''
#--------------------

def main(**kwargs):
    print(kwargs)
    for key, value in kwargs.items():
        # print("{0} = {1}".format(key, value))
        if key == 'file_chosen1':
            file_chosen1 = value
        elif key == 'file_chosen2':
            file_chosen2 = value
        # elif key == 'ylabel':
        #     ylabel_value = value

    head_tail_1 = os.path.split(file_chosen1)
    head_tail_2 = os.path.split(file_chosen2)
    
    tail1 = head_tail_1[1]
    tail2 = head_tail_2[1]

    print("Tail 1:", tail1)
    print("Tail 2:", tail2, "\n")

    tail1_splitted = tail1.split('_inter.')
    tail2_splitted = tail2.split('_inter.')

    print(tail1_splitted[0])
    print(tail2_splitted[0])

    combined_name = tail1_splitted[0] + '_x_' + tail2_splitted[0]

    return combined_name






if __name__ == '__main__':
#main(sys.argv)
#main()
    main()