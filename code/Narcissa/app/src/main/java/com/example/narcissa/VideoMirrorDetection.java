package com.example.narcissa;

import android.content.Context;
import android.media.MediaMetadataRetriever;
import android.net.Uri;
import android.util.Log;

import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.VideoWriter;
import org.opencv.videoio.Videoio;

import java.io.File;

public class VideoMirrorDetection {

    private AerialMap video_map;
    private File selected_video;
    private File output_video;
    private Point fov_pt1;
    private Point fov_pt2;
    private String file_type;              // METDATA_KEY_MIMETYPE
    private int frame_count;            // METADATA_KEY_VIDEO_FRAME_COUNT
    private int height_reso;            // METADATA_KEY_VIDEO_HEIGHT
    private int width_reso;             // METADATA_KEY_VIDEO_WIDTH

//  Getters
    public AerialMap get_video_map() { return this.video_map; }
    public File get_selected_video() { return this.selected_video; }
    public File get_output_video() { return this.output_video; }
    public Point get_fov_pt1() { return this.fov_pt1; }
    public Point get_fov_pt2() { return this.fov_pt2; }
    public String get_file_type() { return this.file_type; }
    public int get_frame_count() { return this.frame_count; }
    public int get_height_reso() { return this.height_reso; }
    public int get_width_reso() { return this.width_reso; }

//  Setters
    public void set_video_map(AerialMap vm) { this.video_map = vm; }
    public void set_selected_video(File sv) { this.selected_video = sv; }
    public void set_output_video(File ov) { this.output_video = ov; }
    public void set_fov_pt1(int x1, int y1) {
        Point p1 = new Point(x1, y1);
        this.fov_pt1 = p1;
    }
    public void set_fov_pt2(int x2, int y2) {
        Point p2 = new Point(x2, y2);
        this.fov_pt2 = p2;
    }
    public void set_file_type(String ft) { this.file_type = ft; }
    public void set_frame_count(int fc) { this.frame_count = fc; }
    public void set_height_reso(int hr) { this.height_reso = hr; }
    public void set_width_reso(int wr) { this.width_reso = wr; }

//    Constructor
    public VideoMirrorDetection(MediaMetadataRetriever retriever, Uri video_data) {

        File sv = new File(video_data.getPath());
        String ft = retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_MIMETYPE);
        int fc = Integer.parseInt(retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_VIDEO_FRAME_COUNT));
        int hr = Integer.parseInt(retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_VIDEO_HEIGHT));
        int wr = Integer.parseInt(retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_VIDEO_WIDTH));

        set_selected_video(sv);
        set_frame_count(fc);
        set_file_type(ft);
        set_height_reso(hr);
        set_width_reso(wr);

        Log.i("VideoMD", "Initiated video mirror detection.");
    }

    /*
    * 1) TODO: Add Field of View (FoV) to every frame. FoV must be consistent throughout
    * 2) TODO: Keep copy of Main Reference Point (MRP) image on hand
    * 3) TODO: Locate the Main Reference Point (MRP)
    * */

//    public void format_video()

    public void add_fov() {

        VideoCapture curr_vid = new VideoCapture(this.get_selected_video().toString());
        VideoWriter fov_version = new VideoWriter();
//      FoV should be around 100dp from sides and 25-50dp from top and bottom
        Log.i("VideoInfo", "(h x w): (" + this.height_reso + " x " + this.width_reso + ")");

//      Set FoV measurements based on the video's height and width.
//      pt1 and pt2 are for the Imgproc.rectangle() method
        int p1_height = 25;
        int p1_width = 100;
        int p2_height = get_height_reso() - 25;
        int p2_width = get_width_reso() - 100;

        set_fov_pt1(p1_height, p1_width);
        set_fov_pt2(p2_height, p2_width);


        try {

            /*
            *   Read frames, save each frame as an image, draw
            *   the rectangle on each frame, save to a new video.
            *
            *   Note: The final video is the one with a marked FoV and
            *         auxiliary reference points (ARPs)
            *
            *   TODO: figure out how to drawRect()
            * */
            Mat curr_frame = new Mat();
//            Mat fov_frame = new Mat();
//          TODO: Set output area for final videos
            VideoWriter fov_video = new VideoWriter(
                    "fov_video.mp4",
                    VideoWriter.fourcc('M','J','P','G'),
                    curr_vid.get(Videoio.CAP_PROP_FPS),
                    new Size((int)curr_vid.get(Videoio.CAP_PROP_FRAME_WIDTH),
                            (int)curr_vid.get(Videoio.CAP_PROP_FRAME_HEIGHT)),
                    true
            );
            if (fov_video.isOpened()) {
                Log.i("FOVStatus", "VideoWriter opened.");
            } else {
                Log.i("FOVStatus", "VideoWriter still not open!!");
            }

            Log.i("FOVStatus", "Entering FoV update loop...");
            Log.i("FOVStatus", "Frame count: " + this.get_frame_count());
            for (int i = 0; i < this.get_frame_count(); i++) {
                Log.i("FOVStatus","Read current frame...");
                curr_vid.read(curr_frame);
                Log.i("FOVStatus","Draw the FoV...");
                Imgproc.rectangle(
                     curr_frame,
                     get_fov_pt1(),
                     get_fov_pt2(),
                     new Scalar(125, 125, 0),
                     5
                );
                Log.i("FOVStatus","Save frame with FoV...");
                MatOfByte new_frame = new MatOfByte();
//                Issue's here with Imgcodec.imencode()
                Imgcodecs.imencode(".jpg", curr_frame, new_frame);

            }

            Log.i("VideoMD", "If you see this then it works up to here. Check output na lang.");
            curr_vid.release();

        } catch (Exception e) {
        } finally {
            Log.i("hoypota", "Issue here!!");
        }

    }

}
