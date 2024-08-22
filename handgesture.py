# ########################################################################
# handgesture.py
# version 0.4
# Wells
# June 1st 2021
# ########################################################################

import math
import iCreatorData

class Point:
    """
    coordinate point
    """
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Line:
    def __init__(self, point1, point2):
        """
        include two point
        :param point1:
        :param point2:
        """
        self.Point1 = point1
        self.Point2 = point2

class Finger:
    def __init__(self, X, Y):
        """
        include 4 points
        :param x of points:
        :param y of points:
        """
        self.X = X
        self.Y = Y

class Gesture:
    def __init__(self, personNo, handNo, gestureNo):
        """
        include 4 points
        :param x of points:
        :param y of points:
        """
        nameString = ['open hand', 'close hand', 'scissor gesture', 'Ok pose', 'spiderman pose', 'gun gesture', 'others']
        self.personNo = personNo
        self.handNo = handNo
        self.gestureNo = gestureNo
        self.name = nameString[self.gestureNo]

def Handset(HandAry,person=0,hand=1):
    '''
    person  0 or 1 , default 0
            P1   P2
    hand    0     or       1 , default 1
            lefthand    righthand

    '''
    personNo = person
    if (hand == 1):
        accNo = HandAry.RHAccNo[person]                          # first person right hand
    else:
        accNo = HandAry.LHAccNo[person]                          # first person right hand
    x = []
    y = []
    for i in range(21):
        # onepeople, 21 point, seach point 3 data of (x, y, z)
        x.append(HandAry.RightHand[i*3+63*person])    
        y.append(HandAry.RightHand[i*3+1+63*person])

    handNo = hand
    
    return personNo,accNo,x,y,handNo


def HandArray(HandAry):
    '''
    MAX_HAND_ENTITIES = 2
    class strHandAry(ctypes.Structure):
        _fields_ = [
        ('mutex', ctypes.c_int),
        ('PeopleNo', ctypes.c_int),
        ('CamWidth', ctypes.c_int),
        ('CamHeight', ctypes.c_int),
        ('LHAccNo', ctypes.c_int*MAX_HAND_ENTITIES),
        ('RHAccNo', ctypes.c_int*MAX_HAND_ENTITIES),
        ('LeftHand', ctypes.c_float*MAX_HAND_POINTS),
        ('RightHand', ctypes.c_float*MAX_HAND_POINTS)
    '''
    
    personNo,accNo,x,y,handNO = Handset(HandAry,person=0,hand=0)
    p1LeftHand= {'personNo':personNo,'AccNo': accNo, 'x': x, 'y':y,'handNo':handNO}
    personNo,accNo,x,y,handNO = Handset(HandAry,person=0,hand=1)
    p1RightHand = {'personNo':personNo,'AccNo': accNo, 'x': x, 'y':y,'handNo':handNO}
    personNo,accNo,x,y,handNO = Handset(HandAry,person=1,hand=0)
    p2LeftHand= {'personNo':personNo,'AccNo': accNo, 'x': x, 'y':y,'handNo':handNO}
    personNo,accNo,x,y,handNO = Handset(HandAry,person=1,hand=1)
    p2RightHand = {'personNo':personNo,'AccNo': accNo, 'x': x, 'y':y,'handNo':handNO}
    hands = {'p1LeftHand':p1LeftHand, 'p1RightHand':p1RightHand, 'p2LeftHand':p2LeftHand, 'p2RightHand':p2RightHand}
    return hands
    
def HandsGesture(hands):
    '''
                   - 'p1LeftHand'        - 'AccNo'
                   - 'p1RightHand' ==    - 'x'
    hands   ===    - 'p2LeftHand'        - 'y'
                   - 'p2RightHand'       - 'handNo'
    '''
    p1LeftHand = HandGesture(personNo=hands['p1LeftHand']['personNo'],accNo=hands['p1LeftHand']['AccNo'], X=hands['p1LeftHand']['x'], Y=hands['p1LeftHand']['y'], handNo=hands['p1LeftHand']['handNo'])
    p1RightHand = HandGesture(personNo=hands['p1RightHand']['personNo'],accNo=hands['p1RightHand']['AccNo'], X=hands['p1RightHand']['x'], Y=hands['p1RightHand']['y'], handNo=hands['p1LeftHand']['handNo'])
    p2LeftHand = HandGesture(personNo=hands['p2LeftHand']['personNo'],accNo=hands['p2LeftHand']['AccNo'], X=hands['p2LeftHand']['x'], Y=hands['p2LeftHand']['y'], handNo=hands['p1LeftHand']['handNo'])
    p2RightHand = HandGesture(personNo=hands['p2RightHand']['personNo'],accNo=hands['p2RightHand']['AccNo'], X=hands['p2RightHand']['x'], Y=hands['p2RightHand']['y'], handNo=hands['p1LeftHand']['handNo'])

    return p1LeftHand, p1RightHand, p2LeftHand, p2RightHand

def gestureOfHand(personNo, handNo, number=True):
    '''
    personNo    0       1
                P1      P2
    handNo      0           1
                LeftHand    RightHand
    number      True        False
        return  gestureNo   gestureClass

    '''
    continueRun = False
    while (not continueRun):
        HandAry, continueRun = iCreatorData.readHandAry()

    hands = HandArray(HandAry)
    p1LeftHand, p1RightHand, p2LeftHand, p2RightHand = HandsGesture(hands)
    if (number == True):
        if (personNo == 0):
            if (handNo == 0):
                return p1LeftHand.isWhichHandGesture()
            elif (handNo == 1):
                return p1RightHand.isWhichHandGesture()
        if (personNo == 1):
            if (handNo == 0):
                return p2LeftHand.isWhichHandGesture()
            elif (handNo == 1):
                return p2RightHand.isWhichHandGesture()
    else:
        if (personNo == 0):
            if (handNo == 0):
                return p1LeftHand.gesture
            elif (handNo == 1):
                return p1RightHand.gesture
        if (personNo == 1):
            if (handNo == 0):
                return p2LeftHand.gesture
            elif (handNo == 1):
                return p2RightHand.gesture

def gestureMatch(personNo1, handNo1, personNo2, handNo2, flip=False):
    '''
    personNo1 / personNo2   0       1
                            P1      P2
    handNo1 / handNo2       0           1
                            LeftHand    RightHand
    flip        True            False
                handNo matters  handNo don't matter
    
    '''
    gsture1 = gestureOfHand(personNo1, handNo1, number=False)   # value is a class object
    gsture2 = gestureOfHand(personNo2, handNo2, number=False)

    if (flip): # different hands is allowed but same gesture is needed
        if (gsture1.gestureNo == gsture2.gestureNo):
            return True
        else:
            return False
    
    else: # must be same hands and same gesture
        if (gsture1.handNo == gsture2.handNo) and (gsture1.gestureNo == gsture2.gestureNo):
            return True
        else:
            return False




class HandGesture:
    def __init__(self, personNo, accNo, X, Y, handNo):
        self.personNo = personNo
        self.accNo = accNo
        self.X = X
        self.Y = Y
        self.handNo = handNo
        self.joint = Point(X[0], Y[0])
        self.thumb        = Finger(X[1:5], Y[1:5])
        self.forefinger   = Finger(X[5:9],   Y[5:9])
        self.middlefinger = Finger(X[9:13],  Y[9:13])
        self.ringfinger   = Finger(X[13:17], Y[13:17])
        self.littlefinger = Finger(X[17:], Y[17:])
        self.thumbTip        = Point(X[4],  Y[4])
        self.forefingerTip   = Point(X[8],  Y[8])
        self.middlefingerTip = Point(X[12], Y[12])
        self.ringfingerTip   = Point(X[16], Y[16])
        self.littlefingerTip = Point(X[20], Y[20])
        self.gesture         = Gesture(personNo, handNo, self.isWhichHandGesture())
        

    def distance(self, point1, point2):
        distance = math.sqrt((point1.X - point2.X)**2 + (point1.Y - point2.Y)**2)
        return distance

    def GetAngle(self,line1, line2):
        """
        function caculating angle between two lines
        :param line1:
        :param line2:
        :return: insideAngle
        """
        dx1 = line1.Point1.X - line1.Point2.X
        dy1 = line1.Point1.Y - line1.Point2.Y
        dx2 = line2.Point1.X - line2.Point2.X
        dy2 = line2.Point1.Y - line2.Point2.Y

        angle1 = math.atan2(dy1, dx1)
        angle1 = angle1 * 180 / math.pi

        angle2 = math.atan2(dy2, dx2)
        angle2 = angle2 * 180 / math.pi

        if angle1 * angle2 >= 0:
            insideAngle = abs(angle1 - angle2)
        else:
            insideAngle = abs(angle1) + abs(angle2)
            if insideAngle > 180:
                insideAngle = 360 - insideAngle

        insideAngle = insideAngle % 180

        return insideAngle
    # distance from finger tips to hand joint

    def disThumbToJoint(self):
        dis = self.distance(self.joint, self.thumbTip)
        return dis

    def disForeToJoint(self):
        dis = self.distance(self.joint, self.forefingerTip)
        return dis

    def disMiddleToJoint(self):
        dis = self.distance(self.joint, self.middlefingerTip)
        return dis

    def disRingfingerToJoint(self):
        dis = self.distance(self.joint, self.ringfingerTip)
        return dis

    def disLittlefingerToJoint(self):
        dis = self.distance(self.joint, self.littlefingerTip)
        return dis    

    def isFingerExtented(self, finger):
        knuckle1 = Point(finger.X[0], finger.Y[0])
        knuckle2 = Point(finger.X[1], finger.Y[1])
        knuckle3 = Point(finger.X[2], finger.Y[2])
        knuckle4 = Point(finger.X[3], finger.Y[3])

        dis1 = self.distance(self.joint, knuckle1)
        dis2 = self.distance(self.joint, knuckle2)
        dis3 = self.distance(self.joint, knuckle3)
        dis4 = self.distance(self.joint, knuckle4)

        if (dis2>dis1 and dis3>dis2 and dis4>dis3):
            return True
        else:
            return False

    def isFingerBent(self, finger):
        knuckle1 = Point(finger.X[0], finger.Y[0])
        knuckle2 = Point(finger.X[1], finger.Y[1])
        knuckle3 = Point(finger.X[2], finger.Y[2])
        knuckle4 = Point(finger.X[3], finger.Y[3])

        dis1 = self.distance(self.joint, knuckle1)
        dis2 = self.distance(self.joint, knuckle2)
        dis3 = self.distance(self.joint, knuckle3)
        dis4 = self.distance(self.joint, knuckle4)

        # if (dis4<dis1 and dis3<dis2 and dis4<dis3):
        # if (dis3<dis2 and dis4<dis3):
        if (dis3<dis2):
            return True
        else:
            return False

    def isThumbBent(self,finger):
        knuckle1 = Point(self.X[17], self.Y[17])      #little finger root        
        knuckle3 = Point(finger.X[2], finger.Y[2])
        knuckle4 = Point(finger.X[3], finger.Y[3])

        dis1 = self.distance(knuckle1, knuckle3)
        dis2 = self.distance(knuckle1, knuckle4)
        dis3 = self.distance(self.joint, knuckle3)
        dis4 = self.distance(self.joint, knuckle4)

        # if (dis4<dis1 and dis3<dis2 and dis4<dis3):
        # if (dis3<dis2 and dis4<dis3):
        if (dis4<dis3 or dis1 > dis2):
            return True
        else:
            return False

    def angleOfFingers(self, finger1, finger2):
        # points of finger1
        point1 = Point(finger1.X[0], finger1.Y[0])
        point2 = Point(finger1.X[3], finger1.Y[3])
        # points of finger2
        point3 = Point(finger2.X[0], finger2.Y[0])
        point4 = Point(finger2.X[3], finger2.Y[3])
        # lines of fingers
        line1 = Line(point1, point2)
        line2 = Line(point3, point4)
        # angle of finger1

        angle = self.GetAngle(line1, line2)
        return angle

    
    def isFingerGun(self):
        L1 = Line(Point(self.X[1], self.Y[1]), Point(self.X[4], self.Y[4]))
        L2 = Line(Point(self.X[5], self.Y[5]), Point(self.X[8], self.Y[8]))

        angle = self.GetAngle(L1, L2)                                    # Angle between thumb and index finger

        h1 = self.isFingerBent(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerBent(self.middlefinger)
        h4 = self.isFingerExtented(self.forefinger)                      # whether finger extented or not                        
        h5 = self.isFingerExtented(self.thumb)      
        h6 = angle > 20                                                  # whether thumb detach from forfinger                  

        if (h1 and h2 and h3 and h4 and h5 and h6):
            return True
        else:
            return False

    def isCloseHand(self):
        h1 = self.isFingerBent(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerBent(self.middlefinger)
        h4 = self.isFingerBent(self.forefinger)                       
        h5 = self.isThumbBent(self.thumb)                      
        
        if h1 and h2 and h3 and h4 and h5:
            return True
        else:
            return False

    def isOpenHand(self):
        h1 = self.isFingerExtented(self.littlefinger)                    # whether finger extented or not 
        h2 = self.isFingerExtented(self.ringfinger)
        h3 = self.isFingerExtented(self.middlefinger)
        h4 = self.isFingerExtented(self.forefinger)                       
        h5 = self.isFingerExtented(self.thumb)                      


        if h1 and h2 and h3 and h4 and h5:
            return True
        else:
            return False

    def isScissorPoseHand(self):
        L1 = Line(Point(self.X[9], self.Y[9]), Point(self.X[13], self.Y[13]))
        L2 = Line(Point(self.X[5], self.Y[5]), Point(self.X[8], self.Y[8]))

        angle = self.GetAngle(L1, L2)                                    # Angle between thumb and index finger
        h1 = self.isFingerBent(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerExtented(self.middlefinger)                    # whether finger extented or not
        h4 = self.isFingerExtented(self.forefinger)                       
        h5 = self.isThumbBent(self.thumb)
        h6 = angle > 10                                                  # whether thumb detach from forfinger                      
        
        if h1 and h2 and h3 and h4 and h5 and h6:
            return True
        else:
            return False

    def isSpidermanHand(self):
        h1 = self.isFingerExtented(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerBent(self.middlefinger)                    # whether finger extented or not
        h4 = self.isFingerExtented(self.forefinger)                       
        h5 = self.isFingerExtented(self.thumb)

        if h1 and h2 and h3 and h4 and h5:
            return True
        else:
            return False

    def isOkPoseHand(self):
        h1 = self.isFingerExtented(self.littlefinger)                    # whether finger extented or not 
        h2 = self.isFingerExtented(self.ringfinger)
        h3 = self.isFingerExtented(self.middlefinger)

        pointa1 = self.thumbTip
        pointa2 = Point(self.thumb.X[2], self.thumb.Y[2])
        pointb1 = self.forefingerTip
        pointb2 = Point(self.forefinger.X[2], self.forefinger.Y[2])
        dis1 = self.distance(pointa1, pointb1)
        dis2 = self.distance(pointa2, pointb2)
        h4 = dis1 < dis2

        if h1 and h2 and h3 and h4:
            return True
        else:
            return False 

    def isStonePoseHand(self):
        return self.isCloseHand(self)

    def isPaperPoseHand(self):
        return self.isOpenHand(self)

    def isWhichHandGesture(self):
        ''' 
         0 for open hand gesture 
         1 for close hand gesture 
         2 for scissor gesture 
         3 for Ok pose hand gesture 
         4 for spiderman pose hand
         5 for gun gesture  
         6 for others      
        '''
        if(self.isOpenHand()):
            return 0      
            
        if(self.isCloseHand()):
            return 1

        if(self.isScissorPoseHand()):
            return 2  
        
        if(self.isOpenHand()):
            return 3

        if(self.isSpidermanHand()):
            return 4

        if(self.isFingerGun()):
            return 5
        else:
            return 6
    
    



        