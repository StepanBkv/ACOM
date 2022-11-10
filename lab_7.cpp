#include "opencv2/opencv.hpp"
#include <iostream>
#include <unistd.h>
#include <chrono>
#include <thread>

using namespace std;
using namespace cv;
 
int main(){
    VideoCapture cap("outcpp_3.avi");   //, CAP_DSHOW);
    cap.set(CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);
    if(!cap.isOpened()){
        cout << "Error opening video stream" << endl;
        return -1;
    }
    int frame_width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    int frame_height = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    // VideoWriter video("outcpp_2.avi", cv::VideoWriter::fourcc('M','J','P','G'), 20, Size(frame_width,frame_height));
    while(1){
        Mat frame;
        cap.read(frame);
        if (frame.empty()) break;
        // video.write(frame);
        imshow( "Frame", frame );
        this_thread::sleep_for(std::chrono::milliseconds(150));
        char c = (char)waitKey(1);
        if( c == 27 ) break;
    }
    cap.release();
    // video.release();
    destroyAllWindows();
    return 0;
}