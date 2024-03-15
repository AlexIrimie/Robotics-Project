def depth_estimate(front_coordinate_x, front_coordinate_y, side_coordinate_x, side_coordinate_y):
    
    # x = front_coordinate_x
    # y = front_coordinate_y
    # z = side_coordinate_x
    
    x = front_coordinate_x
    y = side_coordinate_x
    z = 1 - front_coordinate_y
    
    print(z)
    
    
    return x, y, z