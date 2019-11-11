import numpy as np
import torchvision

CityScapesClasses_converter_index_dict = {
                -1:  [34,  10,  10,   7,   8,],  # license plat
                34:  [34,  10,  10,   7,   8,],  # license plat
                 0:  [0,    0,   0,   0,   1,],  # unlabeled
                 1:  [1,    0,   0,   0,   1,],  # ego vehicle
                 2:  [2,    0,   0,   0,   1,],  # rectification border
                 3:  [3,    0,   0,   0,   1,],  # out of roi
                 4:  [4,    0,   0,   0,   1,],  # static
                 5:  [5,    0,   0,   0,   1,],  # dynamic
                 6:  [6,    0,   0,   0,   1,],  # ground
                 7:  [7,    7,   7,   1,   0,],  # road
                 8:  [8,    8,   8,   1,   2,],  # sidewalk
                 9:  [9,    7,   7,   1,   2,],  # parking
                10:  [10,   7,   7,   1,   2,],  # rail track
                11:  [11,   1,   1,   2,   3,],  # building
                12:  [12,   11,  11,  2,   3,],  # wall
                13:  [13,   2,   2,   2,   3,],  # fence
                14:  [14,   11,  11,  2,   3,],  # guard rail
                15:  [15,   11,  11,  2,   3,],  # bridge
                16:  [16,   11,  11,  2,   3,],  # tunnel
                17:  [17,   5,   5,   3,   4,],  # pole
                18:  [18,   5,   5,   3,   4,],  # polegroup
                19:  [19,   12,  12,  3,   4,],  # traffic light
                20:  [20,   12,  12,  3,   4,],  # traffic sign
                21:  [21,   9,   9,   4,   5,],  # vegetation
                22:  [22,   9,   9,   4,   5,],  # terrain
                23:  [23,   3,   3,   5,   6,],  # sky   # OTHER?
                24:  [24,   4,   4,   6,   7,],  # person
                25:  [25,   4,   4,   6,   7,],  # rider
                26:  [26,   10,  10,  7,   8,],  # car
                27:  [27,   10,  10,  7,   8,],  # truck
                28:  [28,   10,  10,  7,   8,],  # bus
                29:  [29,   10,  10,  7,   8,],  # caravan
                30:  [30,   10,  10,  7,   8,],  # trailer
                31:  [31,   10,  10,  7,   8,],  # train
                32:  [32,   10,  10,  7,   8,],  # motorcycle
                33:  [33,   10,  10,  7,   8,],  # bicycle
            }

CarlaClasses_converter_index_dict = {
     0: [0,    0,   0,   0,   1,],  # None
     1: [11,   1,   1,   2,   3,],  # Buildings
     2: [13,   2,   2,   2,   3,],  # Fences
     3: [23,   3,   3,   5,   6,],  # Other   SKY??
     4: [24,   4,   4,   6,   7,],  # Pedestrians
     5: [17,   5,   5,   3,   4,],  # Poles
     6: [7,    6,   7,   1,   0,],  # RoadLines
     7: [7,    7,   7,   1,   0,],  # Roads
     8: [8,    8,   8,   1,   2,],  # Sidewalks
     9: [21,   9,   9,   4,   5,],  # Vegetation
    10: [26,  10,  10,   7,   8,],  # Vehicles
    11: [12,  11,  11,   2,   3,],  # Walls
    12: [20,  12,  12,   3,   4,],  # TrafficSigns
}

def CityscapesTransform(type_from, type_to):
    if not type_from in ['CityScapesClasses', 'CarlaClasses']:
        raise KeyError
        
    if not type_to in [
            'CityScapesClasses',
            'CarlaClassesWithRoadLines', 'CarlaClassesWithoutRoadLines',
            'Categories', 'CategoriesWithRoad']:
        raise KeyError

    index_converter = None
    
    if type_from == 'CityScapesClasses':
        index_converter = lambda x: CityScapesClasses_converter_index_dict[x][{
            'CityScapesClasses': 0,
            'CarlaClassesWithRoadLines': 1,
            'CarlaClassesWithoutRoadLines': 2,
            'Categories': 3,
            'CategoriesWithRoad': 4
        }[type_to]]
    elif type_from == 'CarlaClasses':
        index_converter = lambda x: CarlaClasses_converter_index_dict[x][{
            'CityScapesClasses': 0,
            'CarlaClassesWithRoadLines': 1,
            'CarlaClassesWithoutRoadLines': 2,
            'Categories': 3,
            'CategoriesWithRoad': 4
        }[type_to]]
        
    def CityScapesSemanticTarget(input):
        mask = np.asarray(input).astype(np.uint8)[..., 2]
#         print(mask[..., 2].max())
        target = np.zeros((
                mask.shape[0],
                mask.shape[1]
        ), dtype=np.long)

        classes_count = 35
        if type_from == 'CarlaClasses':
            classes_count = 13
#             mask = mask[..., 0]

        for city_class in range(classes_count):
            channel = city_class
            target[np.where(mask == channel)] = index_converter(channel)

        return target
    
    return CityScapesSemanticTarget


def decode_cityscapes(image, mode='CityScapesClasses'):
    if not mode in [
        'CityScapesClasses',
        'CarlaClassesWithRoadLines', 'CarlaClassesWithoutRoadLines',
            'Categories', 'CategoriesWithRoad']:
        raise KeyError

    colors = None
    max_classses = 35

    if mode == 'CityScapesClasses':
        colors = np.asarray([
            i.color for i in torchvision.datasets.Cityscapes.classes])
        max_classses = 35

    elif mode == 'CarlaClassesWithRoadLines':
        colors = np.asarray([
            (0, 0, 0),
            (70, 70, 70),
            (190, 153, 153),
            (70, 130, 180),
            (220, 20, 60),
            (153, 153, 153),
            (255, 255, 128),
            (128, 64, 128),
            (244, 35, 232),
            (107, 142, 35),
            (0, 0, 142),
            (102, 102, 156),
            (220, 220, 0)
        ])
        max_classses = 13

    elif mode == 'CarlaClassesWithoutRoadLines':
        colors = np.asarray([
            (0, 0, 0),
            (70, 70, 70),
            (190, 153, 153),
            (70, 130, 180),
            (220, 20, 60),
            (153, 153, 153),
            (128, 64, 128),
            (128, 64, 128),
            (244, 35, 232),
            (107, 142, 35),
            (0, 0, 142),
            (102, 102, 156),
            (220, 220, 0)
        ])
        max_classses = 13

    elif mode == 'Categories':
        colors = np.asarray([
            (0, 0, 0),
            (128, 64, 128),
            (70, 70, 70),
            (153, 153, 153),
            (107, 142, 35),
            (70, 130, 180),
            (220, 20, 60),
            (0, 0, 142), ])
        max_classses = 8

    elif mode == 'CategoriesWithRoad':
        colors = np.asarray([
            (128, 64, 128),
            (0, 0, 0),
            (244, 35, 232),
            (70, 70, 70),
            (153, 153, 153),
            (107, 142, 35),
            (70, 130, 180),
            (220, 20, 60),
            (0, 0, 142), ])
        max_classses = 9

    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)

    for l in range(max_classses):
        idx = image == l
        r[idx] = colors[l, 0]
        g[idx] = colors[l, 1]
        b[idx] = colors[l, 2]

    rgb = np.stack([r, g, b], axis=2)
    return rgb