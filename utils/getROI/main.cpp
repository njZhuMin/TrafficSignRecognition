#include <opencv2/opencv.hpp>
#include <dirent.h>
#include <fstream>

using namespace cv;
using namespace std;

RNG g_rng(12345);   //生成随机颜色
bool isDrawRect = false;    //是否绘制矩形区域
Point leftPoint = Point(-1,-1);
Point mousePos = Point(-1, -1);
// 输出文件
ofstream outfile("out.txt", ios::out | ios::binary);

void SplitString(const string& s, vector<string>& v, const string& c);
void GetImageList(string dest_dir, vector<string> &file_list);
void GetRegion(string filepath);
// implement of cv::on_mouse()
void on_mouse(int event, int x, int y, int flags, void *ustc);

int main() {
    vector<string> list;
    string dir = "/media/silverlining/000836D40003F837/数据集/GTSDB/test/";
    GetImageList(dir, list);

    for(vector<string>::const_iterator it = list.begin(); it != list.end(); it++) {
        outfile << (*it) << " ";
        string filepath = dir + (*it);
        GetRegion(filepath);
        outfile << endl;
    }
    outfile.close();
}

/**
 * 字符串分割函数（String.split()）
 * @param s 目标字符串
 * @param v 结果字符串容器
 * @param c 分隔符
 */
void SplitString(const string& s, vector<string>& v, const string& c) {
    string::size_type pos1, pos2;
    pos2 = s.find(c);
    pos1 = 0;
    while(string::npos != pos2) {
        v.push_back(s.substr(pos1, pos2-pos1));

        pos1 = pos2 + c.size();
        pos2 = s.find(c, pos1);
    }
    if(pos1 != s.length())
        v.push_back(s.substr(pos1));
}

/**
 * 获取目标路径中的图片文件列表
 * @param dest_dir 目标路径
 * @param file_list 文件列表
 */
void GetImageList(string dest_dir, vector<string> &file_list) {
    int return_code;
    DIR *dir;
    struct dirent entry;
    struct dirent *res;
    //成功打开目录
    if((dir = opendir(dest_dir.c_str())) != NULL) {
        for(return_code = readdir_r(dir, &entry, &res);
            res != NULL && return_code == 0; return_code = readdir_r(dir, &entry, &res)) {
            if(entry.d_type != DT_DIR) {
                string filename = entry.d_name;
                vector<string> filetype;
                // 过滤文件后缀
                SplitString(filename, filetype, ".");
                if("png" == filetype.back())
                    file_list.push_back(string(entry.d_name));
            }
        }
        closedir(dir);
    }
}

/**
 * 获取矩形区域坐标
 * @param filepath 图片路径
 */
void GetRegion(string filepath) {
    Mat org = imread(filepath), temp1, temp2;
    while(waitKey(30) != 27) {
        org.copyTo(temp1);      //用来显示点的坐标以及临时的方框
        namedWindow("img");     //定义一个img窗口
        setMouseCallback("img", on_mouse, (void*)&org);     //调用回调函数
        if(isDrawRect)
            rectangle(temp1, leftPoint, mousePos, cv::Scalar(g_rng.uniform(0, 255),
                g_rng.uniform(0, 255), g_rng.uniform(0, 255)));     //随机颜色
        putText(temp1, "(" + std::to_string(mousePos .x) + "," + std::to_string(mousePos .y)
                       + ")", mousePos, FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 0, 255));
        imshow("img", temp1);
    }
}

/**
 * 监听鼠标事件
 * @param event 鼠标事件
 * @param x 鼠标坐标
 * @param y 鼠标坐标
 * @param flags 拖拽和键盘操作的代号
 * @param ustc
 */
void on_mouse(int event, int x, int y, int flags, void *ustc) {
    Mat& image = *(cv::Mat*) ustc;      //传递Mat信息了
    char temp[16];
    string label;
    switch (event) {
        case CV_EVENT_LBUTTONDOWN: {  //按下左键
            sprintf(temp, "(%d,%d)", x, y);
            putText(image, temp, Point(x, y), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 0, 255));
            isDrawRect = true;
            leftPoint = Point(x, y);
            outfile << x << " " << y << " ";
        } break;
        case CV_EVENT_MOUSEMOVE: {      //移动鼠标
            mousePos  = Point(x, y);
            if(isDrawRect) { }
        } break;
        case EVENT_LBUTTONUP: {
            isDrawRect = false;
            sprintf(temp, "(%d,%d)", x, y);
            putText(image, temp, Point(x, y), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 0, 255));
            //调用函数进行绘制
            cv::rectangle(image, leftPoint, mousePos, cv::Scalar(g_rng.uniform(0, 255),
                g_rng.uniform(0, 255), g_rng.uniform(0, 255))); //随机颜色
            outfile << x << " " << y << " ";
            cout << "input label for sign: ";
            cin >> label;
            outfile << label << " ";
        }break;
    }
}

