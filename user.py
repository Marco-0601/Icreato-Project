# region ------------------------ initialize user related values
# usercode 0
stageNoforChange=23
elements = Elements()

elementsIn23 = [1, 8, 8, 1] # ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber

elements.addStage(23, elementsIn23)

# bullet
prepared = 0    
flying = 2
launch = 1
hit = 3
bulletState = [-1,0,0,0,0,0,0,0]
lastLauchTime = -1
lauchInterval = 0.2
bulletNum = 7

# enemy
enemyState = [0,0,0,0,0,0,0,0]
initime    = [0,0,0,0,0,0,0,0]
scales     = [0,0,0,0,0,0,0,0]
scaleIni     = [0,0,0,0,0,0,0,0]
speedFactor = 0.2
xstartVal2=[0,0,0,0,0,0,0,0]
ystartVal2=[0,0,0,0,0,0,0,0]
deltay=1
'''      
                          init    gesture                     judge
bullet state            prepared -->   launch   -->   flying  -->  hit(or miss)  -->  prepared     
                            0           1               2            3                  0                      

                        
'''

'''      
                          init    size position                     judge
enemy state           prepared -->   launch   -->   flying  -->  hit(or miss)  -->  prepared     
                            0           1               2            3                  0                      

                        
'''


targetGestures = [2]
xmove_max=10

hitEnemy = False
itemNo=0
itemNoC=1
dx=0.1
dy=8

xboundary=480
yboundary=270
xstartVal1= [0,0,0,0,0,0,0,0]
ystartVal1 = [0,0,0,0,0,0,0,0]
xstartVal1_origin= [0,0,0,0,0,0,0,0]
ystartVal1_origin = [0,0,0,0,0,0,0,0]
hit_time = [0,0,0,0,0,0,0,0]
exposionTime = 0.8

out_dis = 200
GoodyNum=1
goodyNo=-1



x=0
y=0
time1=[0,2.5,5]
x1=[-200,0,200]
y1=[-yboundary+10, 0, yboundary-10]


def elementsHit(elementKind1, elementNum1,  elementKind2, elementNum2, distance):
    getit1,x1,y1 = GetStartLocation(currentStage, elementKind1, elementNum1)
    getit2,x2,y2 = GetStartLocation(currentStage, elementKind2, elementNum2)
    dist = sqrt(pow(x2-x1, 2)+pow(y2-y1, 2))
    if getit1 and getit2 and (dist<distance):
        return True
    else:
        return False

def gamewin():
    if GetGoodyNum("star") > 5:
        return True
    else:
        return False

# endregion ------------------------- end of initialize user related values


##**##

# region-----------------this is the start of user input to change things during the desired stage
    
if (currentStage==23):
    get,timeIndex = GetTimeIndex(23)
    loginfoprint(printFilename,1,"timeIndex is "+str(timeIndex))
    if timeIndex==1:
        a_temp = -yboundary-out_dis

        ystartVal2 = [a_temp]
        xstartVal2 = [a_temp]
        for i in range(1,8):
            getit, x, y = GetStartLocation(23, FG, i)  
            xstartVal2.append(x)
            ystartVal2.append(y)
        ystartVal1 = [0]
        xstartVal1 = [0]
        for i in range(1,8):
            getit, x, y = GetStartLocation(23, CG, i)  
            xstartVal1.append(x)
            ystartVal1.append(y)

        enemyState = [0,0,0,0,0,0,0,0]
        bulletState = [-1,0,0,0,0,0,0,0]
        lastLauchTime = -1

        getit,x,y = GetStartLocation(23, CG, 0)
        newx = x

        enemyState = [0,0,0,0,0,0,0,0]
        for i in range(4):
            getit, scaleini, scaleini = GetStartScale(23, CG, i)
            scaleIni[i] = scaleini

    # if bulletState == prepared:
    get, time2=GetTime(23)
    loginfoprint(printFilename,1,"time is "+str(time2)[0:6])
    if (prepared in bulletState) and (lastLauchTime + lauchInterval) < time2:
        bulletindex = bulletState.index(prepared)

        # get right hand gesture and position
        recognized, righthandx, righthandy, confidenceLevel = GetStartLocation(23, HAND, 2)

        if (recognized and confidenceLevel==14):
            recognized,confidenceLevel = False, 0
            bulletState[bulletindex] = flying

            getit,x,y = GetStartLocation(23, FG, 0) # get my ship position
            if getit:
                xstartVal1[bulletindex]=x
                ystartVal1[bulletindex]=y
                lastLauchTime = time2


    for i in range(1,8):
        if bulletState[i] == flying:  
            ystartVal1[i] = ystartVal1[i] - dy
            setit = SetStartLocation(23, FG, i, xstartVal1[i], ystartVal1[i])

            for j in range(4):
                if elementsHit(FG, i, CG, j, 30):
                    bulletState[i] = hit
                    enemyState[j] = hit
                    get, hit_time[j]=GetTime(23)
                    setit = SetStartLocation(23, FG, i, xstartVal1[i], -yboundary-out_dis)   # bullet remove
                    increaseGoodyNum("star",1)
                    bulletState[i] = prepared                    

            if ystartVal1[i]<-yboundary-20:
                ystartVal1[i] = -yboundary-200
                setit = SetStartLocation(23, FG, i, xstartVal1[i], ystartVal1[i])
                bulletState[i] = prepared
        if bulletState[i] == hit:
            setit = SetStartLocation(23, FG, i, xstartVal1[i], -yboundary-out_dis)   # bullet remove
    if gamewin():
        setSingleScriptTransition(23, 1)

    # user jet moves        
    recognized, headx, heady, confidenceLevel = GetStartLocation(23, HEAD, 0)
    getit,x,y = GetStartLocation(23, FG, 0)
    xmove = headx - x
    
    if xmove > xmove_max:
        xmove = xmove_max
    elif xmove < -xmove_max:
        xmove = -xmove_max

    newx = max(-xboundary, min(x+xmove, xboundary))
    SetStartLocation(23, FG, 0, newx, y)

    
    # enemy moves

    for i in range(4):
        if enemyState[i] == prepared:
            scales[i] = 0.5*(1+ random())*scaleIni[i]
            initime[i] = random()
            enemyState[i] = flying
            ystartVal2[i] = -yboundary-10
        elif enemyState[i] == flying:
            ystartVal2[i]=ystartVal2[i]+deltay    
            xstartVal2[i] = xboundary*sin(time2*speedFactor*pi + initime[i]*2*pi)
            SetStartLocation(23, CG, i, xstartVal2[i], ystartVal2[i])
            ScaleChange(23, CG, i, [1], [scales[i]],  [scales[i]])
            SetStartLocation(23, CG, i+4, -xboundary-50, -yboundary-100)
            if (ystartVal2[i] > yboundary+20):
                ystartVal2[i]=-yboundary-20
                enemyState[i] = prepared
        elif enemyState[i] == hit:
            SetStartLocation(23, CG, i, xstartVal2[i], -yboundary-out_dis)
            ScaleChange(23, CG, i, [1], [0.1],  [0.1])
            SetStartLocation(23, CG, i+4, xstartVal2[i], ystartVal2[i])
            get, time_tmp=GetTime(23)

            if time_tmp > hit_time[i] + exposionTime:
                # loginfoprint(printFilename,1,"time = \t"+str(time_tmp) + "\t" )
                SetStartLocation(23, CG, i+4, xstartVal2[i], -yboundary-out_dis)
                SetStartLocation(23, CG, i,   xstartVal2[i], -yboundary-out_dis)
                enemyState[i] = prepared

    


# endregion-----------------End of user input to change things during the desired stage


