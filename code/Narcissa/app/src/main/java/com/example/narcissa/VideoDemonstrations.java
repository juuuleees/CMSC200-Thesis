package com.example.narcissa;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.media.MediaMetadataRetriever;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;

import java.io.File;

public class VideoDemonstrations extends AppCompatActivity {

    private Button select_video;
    private MediaMetadataRetriever data_retriever;
    private final int SELECT_VIDEO_REQUEST = 100;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.video_demonstrations);

//      Select a video from gallery
        Intent vid_intent = set_retrieval_intent();

//      Initialize video selection button
        select_video = (Button)findViewById(R.id.select_video_button);
        select_video.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivityForResult(Intent.createChooser(vid_intent, "Select Video")
                        ,SELECT_VIDEO_REQUEST);
            }
        });


    }

    public void onActivityResult(int request, int result, Intent data) {
        if (result == RESULT_OK) {
            if (request == SELECT_VIDEO_REQUEST) {
                MediaMetadataRetriever retriever = new MediaMetadataRetriever();
                Uri video_uri = data.getData();
                retriever.setDataSource(getApplicationContext(), video_uri);
                VideoMirrorDetection mirror_detector = new VideoMirrorDetection(retriever, video_uri);
                mirror_detector.add_fov();
            }
        }
    }

    public Intent set_retrieval_intent() {
        Intent intent;
        if (android.os.Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)) {
//          Everything can access external storage
            intent = new Intent(Intent.ACTION_PICK,
                    MediaStore.Video.Media.EXTERNAL_CONTENT_URI);
        } else {
//          Only the app/system/super processes can access internal storage
            intent = new Intent(Intent.ACTION_PICK,
                    MediaStore.Video.Media.INTERNAL_CONTENT_URI);
        }

        intent.setType("video/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);

        return intent;
    }

}