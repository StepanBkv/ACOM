#include <opencv2/opencv.hpp>
#include <iostream>
#include "string"

using namespace cv;
using namespace std;

//int main(int argc, char** argv )
//{
//    String srt ="/home/qazio/Загрузки/main1.jpg";
//    Mat image;
//    image = imread( srt , 1 );
//    if ( !image.data )
//    {
//        printf("No image data \n");
//        return -1;
//    }
//    namedWindow("Display Image", WINDOW_AUTOSIZE );
//    imshow("Display Image", image);
//    waitKey(0);
//    return 0;
//}

//int main() {
//    Mat image;
//    namedWindow("Display window");
//    VideoCapture cap(0);
//    if (!cap.isOpened()) {
//        std::cout << "cannot open camera";
//    }
//
//    while (true) {
//        cap >> image;
//        imshow("Display window", image);
//        waitKey(25);
//    }
//    return 0;
//}

//int main(int, char**)
//{
//    Mat src;
//    VideoCapture cap(0);
//
//    if (!cap.isOpened()) {
//        std::cerr << "ERROR! Unable to open camera\n";
//        return -1;
//    }
//    cap >> src;
//    if (src.empty()) {
//        std::cerr << "ERROR! blank frame grabbed\n";
//        return -1;
//    }
//    bool isColor = (src.type() == CV_8UC3);
//    VideoWriter writer;
//    int codec = VideoWriter::fourcc('M', 'J', 'P', 'G');
//    double fps = 25.0;
//    std::string filename = "./live.avi";
//    writer.open(filename, codec, fps, src.size(), isColor);
//    if (!writer.isOpened()) {
//        std::cerr << "Could not open the output video file for write\n";
//        return -1;
//    }
//    std::cout << "Writing videofile: " << filename << std::endl
//         << "Press any key to terminate" << std::endl;
//    for (;;)
//    {
//        if (!cap.read(src)) {
//            std::cerr << "ERROR! blank frame grabbed\n";
//            break;
//        }
//        writer.write(src);
//        imshow("Live", src);
//        if (waitKey(5) >= 0)
//            break;
//    }
//    return 0;
//}
//}


#include <stdlib.h>
#include <stdio.h>

int main() {

    Mat image;
    Mat image2;
    namedWindow("Display window");
    VideoCapture cap(1);
    int centW = cap.get(CAP_PROP_FRAME_WIDTH);
    int centH = cap.get(CAP_PROP_FRAME_HEIGHT);
    cout << centW << endl << centH;
    // Rect r = Rect(0, 0, centW, centH); //640 × 480
    Rect r2 = Rect(0, 0, centW, centH); //640 × 480

    Vec3b vec;
    VideoWriter video("outcpp_3.avi", VideoWriter::fourcc('M','J','P','G'), 20, Size(centW,centH));
    while (true) {
        cap >> image;

        cvtColor(image, image2, COLOR_BGR2HSV);

        vec = image2.at<Vec3b>(centH, centW);
        Vec3b vec2;
        int sec = 180 / 3;
        int sec2 = sec / 2;
        if ((vec[0] > sec2) && (vec[0] < (sec2 + sec))) {
            vec2[0] = 0;
            vec2[1] = 255;
            vec2[2] = 0;
        } else if ((vec[0] > sec2 + sec) && (vec[0] < 180 - sec2)) {
            vec2[0] = 255;
            vec2[1] = 0;
            vec2[2] = 0;
        } else {
            vec2[0] = 0;
            vec2[1] = 0;
            vec2[2] = 255;
        }

        rectangle(image, r2, Scalar(vec2), 1, 8, 0);
        // rectangle(image, r2, Scalar(vec2), 1, 8, 0);
        // line(image, Point(centW/2 , centH/2 -10), Point(centW/2, centH/2 +10), (255,0,0), 2);
        // line(image, Point(centW/2 -10, centH/2), Point(centW/2 +10, centH/2), (255,56,22), 2);
        imshow("Display window2", image2);
        imshow("Display window", image);
        video.write(image2);
        char c = (char)waitKey(1);
        if( c == 27 ) break;
    }
    return 0;
}
