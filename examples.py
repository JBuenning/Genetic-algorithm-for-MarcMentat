import shape

def create_example_polygon():
    return shape.Shape([(0,0),(200,200),(200,100),(100,0)],holes=[[(100,50), (150,100), (125,50)]])
def second_example_polygon():
    return shape.Shape([(0,0), (20,80), (100,100), (100,0)],[[(10,10), (10,20), (20,10)]])
def complicated_polygon():
    return shape.Shape([(0,0), (3,1), (5,4), (7,4), (9,5), (6,7), (3,8), (1,7), (-1,5), (-3,3), (-2,1)])

def get_cool_example():
    shell = [(0,8),(0,9),(0,10),(0,11),(0,12),(0,13),(0,14),(0,15),(0,16),(1,16),(2,16),(2,15),
            (2,14),(3,14),(4,14),(5,14),(6,14),(6,15),(6,16),(7,16),(8,16),(8,15),(8,14),
            (9,14),(10,14),(11,14),(12,14),(13,14),(14,14),(14,15),(14,16),(15,16),(16,16),(16,15),
            (16,14),(17,14),(18,14),(19,14),(20,14),(20,15),(20,16),(21,16),(22,16),
            (22,15),(22,14),(22,13),(22,12),(22,11),(22,10),(22,9),(22,8),
            (21,8),(20,8),(19,8),(18,8),(17,8),(16,8),(15,7),(14,6),
            (14,5),(14,4),(14,3),(14,2),(14,1),(14,0),(13,0),(12,0),(11,0),(10,0),(9,0),(8,0),
            (8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(7,7),(6,8),(5,8),(4,8),(3,8),(2,8),(1,8)]
    
    move_restrictions = [False,False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,False,
                        False,False,False,False,False,False,False,False,False,False,False,False,False,
                        True,True,True,True,True,True,True,
                        False,False,False,False,False,False,False,False,False,False,False,False,False]
    return shape.Shape(shell, move_restrictions=move_restrictions)

def get_realisticreate_example_polygonc_example():
    shell = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),
             (14,1),(14,2),(14,3),
             (13,3),(12,3),(11,3),(10,3),(9,3),(8,3),(7,3),(6,3),(5,3),(4,3),(3,3),
             (3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(3,13),
             (3,14),(2,14),(1,14),
             (0,14),(0,13),(0,12),(0,11),(0,10),(0,9),(0,8),(0,7),(0,6),(0,5),(0,4),(0,3),(0,2),(0,1)]

    move_restrictions = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,
                         True,True,True,
                         False,False,False,False,False,False,False,False,False,False,False,
                         False,False,False,False,False,False,False,False,False,False,
                         True,True,True,
                         True,True,True,True,True,True,True,True,True,True,True,True,True,True]

    return shape.Shape(shell, move_restrictions=move_restrictions)

def merge_example_1():
    shell = [(0,0),(1,2),(1,4),(1,6),(0,8),(2,8),(4,8),(6,8),(8,8),(8,6),(8,4),(8,2),(8,0),(6,0),(4,0),(2,0)]
    
    move_restrictions = [True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    return shape.Shape(shell, move_restrictions=move_restrictions)

def merge_example_2():
    shell = [(2,2),(2,3),(2,4),(2,5),(2,6),(3,6),(4,6),(5,6),(6,6),(6,5),(6,4),(6,3),(6,2),(5,2),(4,2),(3,2)]
    move_restrictions = [False,False,False,False,False,False,False,False,False,False,False,False,True,False,False,False]
    return shape.Shape(shell, move_restrictions=move_restrictions)


def merge_example_2_wrong():
    shell = [(2,6),(3,6),(4,6),(5,6),(6,6),(6,5),(6,4),(6,3),(6,2),(5,2),(4,2),(3,2),(2,2),(2,3),(2,4),(2,5)]   
    move_restrictions = [False,False,False,False,False,False,False,False,False,False,False,False,True,False,False,False]
    return shape.Shape(shell, move_restrictions=move_restrictions)