def sift_actions(exists_objects, new_objects):
    # sift به معنی الک کردن و قربال کردن است
    # هدف این متد غربال کردن اکشن های جدید و اکشن های پاک شده است
    new_objects_list = []
    removed_objects_list = []

    for item in exists_objects:
        if item not in new_objects:
            removed_objects_list.append(item)
    for item in new_objects:
        if item not in exists_objects:
            new_objects_list.append(item)
    return [new_objects_list, removed_objects_list]
