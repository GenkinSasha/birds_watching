Birds detection and naive tracking:
 - detect movings with some threshold
 - tracking: measure the Euclide distance between the object and one of objects in previouse frame. 
   If the difference is under a treshold - decide about object's moving ("tracking"), otherwise - decide about
   a new object
 - frames with detected birds are saved in the gallery