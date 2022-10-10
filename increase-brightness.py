import cv2
# import numpy
import sys

DIFF_FROM_TARGET_VALUE = 5

def main():
    videoFile, outputFile, targetValue = getInput()

    if videoFile == None:
        print ("--videofile not provided")
        sys.exit(1)

    # use default outputFile if not provided through cammand argument
    if outputFile == None:
        outputFile = "output.mp4"
        print ("--outputFile not provided using default ", outputFile)

    cap = cv2.VideoCapture(videoFile)
    if cap.isOpened() == False:
        print ("videoFile", videoFile, "is not in the given path")
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    record = cv2.VideoWriter(outputFile, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
    FrameCount = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        frameLen = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        FrameCount += 1
        print ("Processing :", int((FrameCount/frameLen) * 100), "%", end = '\r')
        if ret == True:
            yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            y, u, v = cv2.split(yuv)
            # print ("before: ", y.mean())

            while y.mean() < targetValue - DIFF_FROM_TARGET_VALUE:
                for index in range(len(y)):
                    if (y[index] + targetValue - y.mean()).all() > 255:
                        y[index] = 255
                    else:
                        y[index] = y[index] + int(targetValue - y.mean())

            # print ("after: ", y.mean())
            final_yuv = cv2.merge((y, u, v))
            bright = cv2.cvtColor(final_yuv, cv2.COLOR_YUV2BGR)
            record.write(bright)
        else:
            break

    cap.release()
    record.release()
    cv2.destroyAllWindows()

def getInput():
    videoFile = outputFile = None
    # default target value
    targetValue = 100
    try:
        if sys.argv[1] == "--help":
            helper()
            sys.exit(1)
        elif sys.argv[1] == "--videofile":
            if len(sys.argv) > 2:
                videoFile = sys.argv[2]
    except Exception:
        print ("Invalid usage")
        print ("Try '--help' for more information")
        sys.exit(1)

    try:
        if sys.argv[3] == "--outputfile":
            outputFile = sys.argv[4]
        if sys.argv[3] == "--target-val":
            if int(sys.argv[4]) > 0 and int(sys.argv[4]) < 255:
                targetValue = int(sys.argv[4])
            else:
                print ("invalid target-val: need to between 0 and 255")
                sys.exit(1)
        if sys.argv[5] == "--target-val":
            if sys.argv[6] > 0 and sys.argv[6] < 255:
                targetValue = int(sys.argv[6])
            else:
                print ("invalid target-val: need to between 0 and 255")
                sys.exit(1)
        if sys.argv[5] == "--outputfile":
            outputFile = sys.argv[6]
    except Exception:
        pass
    return videoFile, outputFile, targetValue

def helper():
    print ("Usage: improve-brightness [--videofile] [--outputfile] [--target-val]")
    print ("--videofile    Path to the video file (Mandatory argument)")
    print ("--outputfile   Path for Output file (default if omitted)")
    print ("--target-val   Target brightness to apply in the input video file (default target-val=100)")
    print ("                 target-val need to be between 0 to 255, higher is brighter")

if __name__ == "__main__":
    main()
